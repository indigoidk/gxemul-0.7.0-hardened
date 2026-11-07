# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `ecoffclampdead` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `ecoffclampdead`, state `open`)

**title:** src/file/file_ecoff.c:513-534 -- the clamp of the last chunk to s_size is dead code because the next line reassigns len from fread(), so each section loads in whole chunk_size pieces and can write up to chunk_size - 1 bytes of the following file data past s_vaddr + s_size into emulated memory -- OOB-WRITE (loaded file content; emulated memory, not host memory)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- `len = fread(buf, 1, chunk_size, f);` at line 523.

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/file/file_ecoff.c b/src/file/file_ecoff.c
index 6bac4224..ddd431bb 100644
--- a/src/file/file_ecoff.c
+++ b/src/file/file_ecoff.c
@@ -520,7 +520,7 @@ skip_normal_coff_symbols:
 				len = chunk_size;
 				if (total_len + len > s_size)
 					len = s_size - total_len;
-				len = fread(buf, 1, chunk_size, f);
+				len = fread(buf, 1, len, f);
 				if (len == 0) {
 					debug("!!! total_len = %i, "
 					    "chunk_size = %i, len = %i\n",
```

## Every edited function, after the fix

### `src/file/file_ecoff.c` -- post-edit lines 63-674 (`+` marks a line the diff added or the point of a deletion)

```c
   63|  {
   64|  	struct ecoff_exechdr exechdr;
   65|  	int f_magic, f_nscns, f_nsyms;
   66|  	int a_magic;
   67|  	off_t f_symptr, a_tsize, a_dsize, a_bsize;
     | [... lines 68-412 not shown ...]
  413|  		    reading them (otherwise a malformed header drives a huge malloc
  414|  		    -> OOM, or an over-read).  */
  415|  		if (issExtMax < 0 || iextMax < 0 ||
  416|  		    (uint64_t) cbSsExtOffset + (uint64_t) issExtMax + 1
  417|  		        > (uint64_t) file_size ||
  418|  		    (uint64_t) cbExtOffset + (uint64_t) iextMax *
  419|  		        sizeof(struct ecoff_extsym) > (uint64_t) file_size ||
  420|  		    (uint64_t) issExtMax + 1 > LOADER_MAX_TABLE_BYTES ||
  421|  		    (uint64_t) iextMax * sizeof(struct ecoff_extsym)
  422|  		        > LOADER_MAX_TABLE_BYTES) {
  423|  			fatal("[ ECOFF: bogus symbol-table sizes ]\n");
  424|  			goto skip_normal_coff_symbols;
  425|  		}
  426|  
  427|  		CHECK_ALLOCATION(symbol_data = (char *) malloc(issExtMax + 2));
  428|  		memset(symbol_data, 0, issExtMax + 2);
  429|  		fseek(f, cbSsExtOffset, SEEK_SET);
  430|  		if (fread(symbol_data, 1, issExtMax + 1, f) != (size_t) issExtMax+1) {
  431|  			fprintf(stderr, "error reading symbol data from %s\n", filename);
  432|  			exit(1);
  433|  		}
  434|  
  435|  		nsymbols = iextMax;
  436|  
  437|  		CHECK_ALLOCATION(extsyms = (struct ecoff_extsym *)
  438|  		    malloc(iextMax * sizeof(struct ecoff_extsym)));
  439|  		memset(extsyms, 0, iextMax * sizeof(struct ecoff_extsym));
  440|  		fseek(f, cbExtOffset, SEEK_SET);
  441|  		if (fread(extsyms, 1, iextMax * sizeof(struct ecoff_extsym), f) !=
  442|  		    iextMax * sizeof(struct ecoff_extsym)) {
  443|  			fprintf(stderr, "error reading extsyms from %s\n", filename);
  444|  			exit(1);
  445|  		}
  446|  
  447|  		/*  Unencode the strindex and value first:  */
  448|  		for (sym_nr=0; sym_nr<nsymbols; sym_nr++) {
  449|  			uint64_t value, strindex;
  450|  
  451|  			unencode(strindex, &extsyms[sym_nr].es_strindex,
  452|  			    uint32_t);
  453|  			unencode(value, &extsyms[sym_nr].es_value, uint32_t);
  454|  
  455|  			extsyms[sym_nr].es_strindex = strindex;
  456|  			extsyms[sym_nr].es_value    = value + relocationOffset;
  457|  		}
  458|  
  459|  		for (sym_nr=0; sym_nr<nsymbols; sym_nr++) {
  460|  			/*  debug("symbol%6i: 0x%08x = %s\n",
  461|  			    sym_nr, (int)extsyms[sym_nr].es_value,
  462|  			    symbol_data + extsyms[sym_nr].es_strindex);  */
  463|  
  464|  			/*  es_strindex is file-controlled; skip out-of-range
  465|  			    offsets so we never read past symbol_data.  */
  466|  			if ((uint32_t) extsyms[sym_nr].es_strindex >
  467|  			    (uint32_t) issExtMax)
  468|  				continue;
  469|  
  470|  			add_symbol_name(&m->symbol_context,
  471|  			    extsyms[sym_nr].es_value, 0,
  472|  			    symbol_data + extsyms[sym_nr].es_strindex, 0, -1);
  473|  		}
  474|  
  475|  		free(symbol_data);
  476|  
  477|  skip_normal_coff_symbols:
  478|  		;
  479|  	}
  480|  
  481|  	/*  Then, load the sections that are loadable:  */
  482|  	for (secn=0; secn<f_nscns; secn++) {
  483|  		off_t s_scnptr, s_relptr, s_lnnoptr;
  484|  		unsigned int s_nreloc, s_nlnno, s_flags, s_size;
  485|  		uint64_t s_paddr, s_vaddr;
  486|  
  487|  		/*  Read a section header:  */
  488|  		fseek(f, sectionHeadersPos + sizeof(scnhdr) * secn, SEEK_SET);
  489|  		len = fread(&scnhdr, 1, sizeof(scnhdr), f);
  490|  		if (len != sizeof(scnhdr)) {
  491|  			fprintf(stderr, "%s: incomplete section "
  492|  			    "header %i\n", filename, secn);
  493|  			exit(1);
  494|  		}
  495|  
  496|  		unencode(s_paddr,   &scnhdr.s_paddr,   uint32_t);
  497|  		unencode(s_vaddr,   &scnhdr.s_vaddr,   uint32_t);
  498|  		unencode(s_size,    &scnhdr.s_size,    uint32_t);
  499|  		unencode(s_scnptr,  &scnhdr.s_scnptr,  uint32_t);
  500|  		unencode(s_relptr,  &scnhdr.s_relptr,  uint32_t);
  501|  		unencode(s_lnnoptr, &scnhdr.s_lnnoptr, uint32_t);
  502|  		unencode(s_nreloc,  &scnhdr.s_nreloc,  uint16_t);
  503|  		unencode(s_nlnno,   &scnhdr.s_nlnno,   uint16_t);
  504|  		unencode(s_flags,   &scnhdr.s_flags,   uint32_t);
  505|  
  506|  		s_vaddr += relocationOffset;
  507|  		end_addr = s_vaddr + s_size;
  508|  
  509|  		/*  Loadable? Then load the section:  */
  510|  		if (s_scnptr != 0 && s_size != 0 &&
  511|  		    s_vaddr != 0 && !(s_flags & 0x02)) {
  512|  			/*  Load the section into emulated memory:  */
  513|  			fseek(f, s_scnptr, SEEK_SET);
  514|  			total_len = 0;
  515|  			chunk_size = 1;
  516|  			if ((s_vaddr & 0xf) == 0)	chunk_size = 0x10;
  517|  			if ((s_vaddr & 0xff) == 0)	chunk_size = 0x100;
  518|  			if ((s_vaddr & 0xfff) == 0)	chunk_size = 0x1000;
  519|  			while (total_len < s_size) {
  520|  				len = chunk_size;
  521|  				if (total_len + len > s_size)
  522|  					len = s_size - total_len;
  523|+ 				len = fread(buf, 1, len, f);
  524|  				if (len == 0) {
  525|  					debug("!!! total_len = %i, "
  526|  					    "chunk_size = %i, len = %i\n",
  527|  					    total_len, chunk_size, len);
  528|  					break;
  529|  				}
  530|  
  531|  				m->cpus[0]->memory_rw(m->cpus[0], mem, s_vaddr,
  532|  				    &buf[0], len, MEM_WRITE, NO_EXCEPTIONS);
  533|  				s_vaddr += len;
  534|  				total_len += len;
  535|  			}
  536|  
  537|  			if (relocated && s_relptr != 0) {
  538|  				// Relocate.
  539|  				fseek(f, s_relptr, SEEK_SET);
  540|  				struct mips_ecoff_reloc* relocs;
  541|  				CHECK_ALLOCATION(relocs = (struct mips_ecoff_reloc*)
  542|  				    	malloc(s_nreloc * sizeof(struct mips_ecoff_reloc)));
  543|  				len = fread(relocs, 1, s_nreloc * sizeof(struct mips_ecoff_reloc), f);
  544|  				if ((size_t)len != s_nreloc * sizeof(struct mips_ecoff_reloc)) {
  545|  					fprintf(stderr, "%s: could not read relocation entries for section  %i\n", filename, secn);
  546|  					exit(1);
  547|  				}
  548|  				
  549|  				for (size_t ri = 0; ri < s_nreloc; ++ri) {
  550|  					uint32_t vaddr = ntohl(relocs[ri].vaddr);
  551|  					uint32_t symbolIndexAndType = ntohl(relocs[ri].symbolIndexAndType);
  552|  
  553|  					vaddr += relocationOffset;
  554|  
  555|  					int isExternal = symbolIndexAndType & 1;
  556|  					int relType = (symbolIndexAndType >> 1) & 15;
  557|  					int symbolIndex = symbolIndexAndType >> 8;
  558|  
  559|  					if (symbolIndex < 0 || symbolIndex >= nsymbols) {
  560|  						fprintf(stderr, "%s: relocation for out-of-range symbol %i\n", filename, symbolIndex);
  561|  						exit(1);
  562|  					}
  563|  
  564|  					/*
  565|  					 *  This is a wild guess. If isExternal is false,
  566|  					 *  then perhaps different relocations should be
  567|  					 *  used for text, data, rdata, etc. (TODO.)
  568|  					 */
  569|  					uint32_t r;
  570|  					if (isExternal)
  571|  						r = extsyms[symbolIndex].es_value;
  572|  					else
  573|  						r = relocationOffset;
  574|  
  575|  					// printf("symbolIndex = %i: %08x\n", symbolIndex, r);
  576|  
  577|  					uint16_t relHi = r >> 16;
  578|  					uint16_t relLo = r & 0xffff;
  579|  
  580|  					/*
  581|  					 *  Relocation types for MIPS ECOFF:
  582|  					 *
  583|  					 *  REFHALF	1
     | [... lines 584-644 not shown ...]
  645|  					} else {
  646|  						fprintf(stderr, "%s: unimplemented relType %i\n", filename, relType);
  647|  						exit(1);
  648|  					}
  649|  				}
  650|  				
  651|  				free(relocs);
  652|  			}
  653|  		}
  654|  	}
  655|  
  656|  	fclose(f);
  657|  
  658|  	if (extsyms != NULL)
  659|  		free(extsyms);
  660|  
  661|  	*entrypointp = a_entry;
  662|  	*gpp = a_gp;
  663|  	m->file_loaded_end_addr = end_addr;
  664|  
  665|  	if (program_byte_order != -1)
  666|  		encoding = program_byte_order;
  667|  
  668|  	if (encoding == ELFDATA2LSB)
  669|  		*byte_orderp = EMUL_LITTLE_ENDIAN;
  670|  	else
  671|  		*byte_orderp = EMUL_BIG_ENDIAN;
  672|  
  673|  	n_executables_loaded ++;
  674|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_ECOFFCLAMPDEAD: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

1. Does the diff remove the defect the issue describes, at every site the issue names?  Name any site it misses.
2. CONTROL FLOW: does any added `return`, `goto`, `break` or early exit skip code the function would otherwise run -- above
   all its COMMON TAIL (for example, code after a switch that writes a read's result to the guest, then `return 1;`)?
   Quote the tail line it skips.  An edit that skips the tail hands the guest an unwritten result.
3. RETURN VALUE: does any path now return something different?  Say what the shown code implies the value means.
4. What ELSE does the diff change -- state left set or cleared, a value the guest can now see, a message on a path that
   did not print one -- beyond removing the defect?
5. House idioms (low severity): a diagnostic a guest can trigger repeatedly should print ONCE per device instance (a latch
   field) with `(once)` in the message; a new comment carries a `/* #NNN: ... */` tag; lines stay within 79 columns.

Each finding: `file:line` in the POST-EDIT numbering shown above, severity DEFECT / QUESTION / STYLE, and the smallest fix
in ONE line.  When the excerpt does not show what a question needs, say UNSETTLED and name what is missing.

End with one line: `FIXREVIEW_ECOFFCLAMPDEAD: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
