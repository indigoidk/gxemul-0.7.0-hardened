# GXemul hardened fork -- DRAFT A FIX for one filed issue, `gateupstreamstatus` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `gateupstreamstatus`, state `open`, severity `HIGH`)

**title:** gate_upstream.sh run_case pipe to sed hides loader exit status

**state_note (head):**

GOVERNING TEXT (from the dispositions file, cut at 400 characters): hbundle_regress33:F5 | STATUS-LAUNDERED | RIGHT | DRAFT: NEW HIGH gateupstreamstatus "gate_upstream.sh run_case pipe to sed hides loader exit status" | regress/gate_upstream.sh:73-77,110-140; src/file/file_elf.c:331,387

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Prevent the sed pipe from masking the loader exit status using pipefail or PIPESTATUS

## The code at the cited lines

### `src/file/file_elf.c` around the row's cited line 331 (HEAD 2d25df65, lines 286-376)

```c
  286| 		}
  287| 		break;
  288| 	case ARCH_SH:
  289| 		switch (emachine) {
  290| 		case EM_SH:
  291| 			ok = 1;
  292| 		}
  293| 		break;
  294| 	/*case ARCH_SPARC:
  295| 		switch (emachine) {
  296| 		case EM_SPARC:
  297| 		case EM_SPARCV9:
  298| 			ok = 1;
  299| 		}
  300| 		break;
  301| 	case ARCH_X86:
  302| 		switch (emachine) {
  303| 		case EM_386:
  304| 		case EM_486:
  305| 			*tocp = 1;
  306| 			ok = 1;
  307| 			break;
  308| 		case EM_AMD64:
  309| 			*tocp = 2;
  310| 			ok = 1;
  311| 			break;
  312| 		}
  313| 		break;  */
  314| 	default:
  315| 		fatal("file.c: INTERNAL ERROR: Unimplemented arch %i!\n", arch);
  316| 	}
  317| 	if (!ok) {
  318| 		fprintf(stderr, "%s: this is a ", filename);
  319| 		if (emachine >= 0 && emachine < N_ELF_MACHINE_TYPES)
  320| 			fprintf(stderr, "%s", elf_machine_type[emachine]);
  321| 		else
  322| 			fprintf(stderr, "machine type '%i'", emachine);
  323| 		fprintf(stderr, " ELF binary!\n");
  324| 		exit(1);
  325| 	}
  326| 
  327| 	s = "entry point";
  328| 	if (elf64 && arch == ARCH_PPC)
  329| 		s = "function descriptor at";
  330| 
  331| 	debug("ELF%i %s, %s 0x", elf64? 64 : 32,
  332| 	    encoding == ELFDATA2LSB? "LSB (LE)" : "MSB (BE)", s);
  333| 
  334| 	if (elf64)
  335| 		debug("%016" PRIx64"\n", (uint64_t) eentry);
  336| 	else
  337| 		debug("%08" PRIx32"\n", (uint32_t) eentry);
  338| 
  339| 	/*
  340| 	 *  SH64: 32-bit instruction encoding?
  341| 	 */
  342| 	if (arch == ARCH_SH && (eentry & 1)) {
  343| 		fatal("SH64: 32-bit instruction encoding: TODO\n");
  344| 		/*  m->cpus[0]->cd.sh.compact = 0;  */
  345| 		m->cpus[0]->cd.sh.cpu_type.bits = 64;
  346| 		exit(1);
  347| 	}
  348| 
  349| 	/*  Read the program headers:  */
  350| 
  351| 	for (i=0; i<ephnum; i++) {
  352| 		int p_type;
  353| 		uint64_t p_offset;
  354| 		uint64_t p_vaddr;
  355| 		uint64_t p_paddr;
  356| 		uint64_t p_filesz;
  357| 		uint64_t p_memsz;
  358| 		int p_flags;
  359| 		int p_align;
  360| 		int allRead;
  361| 
  362| 		fseek(f, ephoff + i * ephentsize, SEEK_SET);
  363| 
  364| 		if (elf64) {
  365| 			allRead = fread(&phdr64, 1, sizeof(Elf64_Phdr), f) == sizeof(Elf64_Phdr);
  366| 			unencode(p_type,    &phdr64.p_type,    Elf64_Half);
  367| 			unencode(p_flags,   &phdr64.p_flags,   Elf64_Half);
  368| 			unencode(p_offset,  &phdr64.p_offset,  Elf64_Off);
  369| 			unencode(p_vaddr,   &phdr64.p_vaddr,   Elf64_Addr);
  370| 			unencode(p_paddr,   &phdr64.p_paddr,   Elf64_Addr);
  371| 			unencode(p_filesz,  &phdr64.p_filesz,  Elf64_Xword);
  372| 			unencode(p_memsz,   &phdr64.p_memsz,   Elf64_Xword);
  373| 			unencode(p_align,   &phdr64.p_align,   Elf64_Xword);
  374| 		} else {
  375| 			allRead = fread(&phdr32, 1, sizeof(Elf32_Phdr), f) == sizeof(Elf32_Phdr);
  376| 			unencode(p_type,    &phdr32.p_type,    Elf32_Word);
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

End with one line: `FIXDRAFT_GATEUPSTREAMSTATUS: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
