# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ecoffclampdead` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ecoffclampdead`, state `open`, severity `MED`)

**title:** src/file/file_ecoff.c:513-534 -- the clamp of the last chunk to s_size is dead code because the next line reassigns len from fread(), so each section loads in whole chunk_size pieces and can write up to chunk_size - 1 bytes of the following file data past s_vaddr + s_size into emulated memory -- OOB-WRITE (loaded file content; emulated memory, not host memory)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- fread overwrites the clamped length by reading the full chunk_size, causing out-of-bounds writes.

## The code at the cited lines

### `src/file/file_ecoff.c` around the row's cited line 513 (HEAD 2d25df65, lines 468-558)

```c
  468| 				continue;
  469| 
  470| 			add_symbol_name(&m->symbol_context,
  471| 			    extsyms[sym_nr].es_value, 0,
  472| 			    symbol_data + extsyms[sym_nr].es_strindex, 0, -1);
  473| 		}
  474| 
  475| 		free(symbol_data);
  476| 
  477| skip_normal_coff_symbols:
  478| 		;
  479| 	}
  480| 
  481| 	/*  Then, load the sections that are loadable:  */
  482| 	for (secn=0; secn<f_nscns; secn++) {
  483| 		off_t s_scnptr, s_relptr, s_lnnoptr;
  484| 		unsigned int s_nreloc, s_nlnno, s_flags, s_size;
  485| 		uint64_t s_paddr, s_vaddr;
  486| 
  487| 		/*  Read a section header:  */
  488| 		fseek(f, sectionHeadersPos + sizeof(scnhdr) * secn, SEEK_SET);
  489| 		len = fread(&scnhdr, 1, sizeof(scnhdr), f);
  490| 		if (len != sizeof(scnhdr)) {
  491| 			fprintf(stderr, "%s: incomplete section "
  492| 			    "header %i\n", filename, secn);
  493| 			exit(1);
  494| 		}
  495| 
  496| 		unencode(s_paddr,   &scnhdr.s_paddr,   uint32_t);
  497| 		unencode(s_vaddr,   &scnhdr.s_vaddr,   uint32_t);
  498| 		unencode(s_size,    &scnhdr.s_size,    uint32_t);
  499| 		unencode(s_scnptr,  &scnhdr.s_scnptr,  uint32_t);
  500| 		unencode(s_relptr,  &scnhdr.s_relptr,  uint32_t);
  501| 		unencode(s_lnnoptr, &scnhdr.s_lnnoptr, uint32_t);
  502| 		unencode(s_nreloc,  &scnhdr.s_nreloc,  uint16_t);
  503| 		unencode(s_nlnno,   &scnhdr.s_nlnno,   uint16_t);
  504| 		unencode(s_flags,   &scnhdr.s_flags,   uint32_t);
  505| 
  506| 		s_vaddr += relocationOffset;
  507| 		end_addr = s_vaddr + s_size;
  508| 
  509| 		/*  Loadable? Then load the section:  */
  510| 		if (s_scnptr != 0 && s_size != 0 &&
  511| 		    s_vaddr != 0 && !(s_flags & 0x02)) {
  512| 			/*  Load the section into emulated memory:  */
  513| 			fseek(f, s_scnptr, SEEK_SET);
  514| 			total_len = 0;
  515| 			chunk_size = 1;
  516| 			if ((s_vaddr & 0xf) == 0)	chunk_size = 0x10;
  517| 			if ((s_vaddr & 0xff) == 0)	chunk_size = 0x100;
  518| 			if ((s_vaddr & 0xfff) == 0)	chunk_size = 0x1000;
  519| 			while (total_len < s_size) {
  520| 				len = chunk_size;
  521| 				if (total_len + len > s_size)
  522| 					len = s_size - total_len;
  523| 				len = fread(buf, 1, chunk_size, f);
  524| 				if (len == 0) {
  525| 					debug("!!! total_len = %i, "
  526| 					    "chunk_size = %i, len = %i\n",
  527| 					    total_len, chunk_size, len);
  528| 					break;
  529| 				}
  530| 
  531| 				m->cpus[0]->memory_rw(m->cpus[0], mem, s_vaddr,
  532| 				    &buf[0], len, MEM_WRITE, NO_EXCEPTIONS);
  533| 				s_vaddr += len;
  534| 				total_len += len;
  535| 			}
  536| 
  537| 			if (relocated && s_relptr != 0) {
  538| 				// Relocate.
  539| 				fseek(f, s_relptr, SEEK_SET);
  540| 				struct mips_ecoff_reloc* relocs;
  541| 				CHECK_ALLOCATION(relocs = (struct mips_ecoff_reloc*)
  542| 				    	malloc(s_nreloc * sizeof(struct mips_ecoff_reloc)));
  543| 				len = fread(relocs, 1, s_nreloc * sizeof(struct mips_ecoff_reloc), f);
  544| 				if ((size_t)len != s_nreloc * sizeof(struct mips_ecoff_reloc)) {
  545| 					fprintf(stderr, "%s: could not read relocation entries for section  %i\n", filename, secn);
  546| 					exit(1);
  547| 				}
  548| 				
  549| 				for (size_t ri = 0; ri < s_nreloc; ++ri) {
  550| 					uint32_t vaddr = ntohl(relocs[ri].vaddr);
  551| 					uint32_t symbolIndexAndType = ntohl(relocs[ri].symbolIndexAndType);
  552| 
  553| 					vaddr += relocationOffset;
  554| 
  555| 					int isExternal = symbolIndexAndType & 1;
  556| 					int relType = (symbolIndexAndType >> 1) & 15;
  557| 					int symbolIndex = symbolIndexAndType >> 8;
  558| 
```

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_ECOFFCLAMPDEAD: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
