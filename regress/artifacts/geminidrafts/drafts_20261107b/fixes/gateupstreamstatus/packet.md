# GXemul hardened fork -- DRAFT A FIX for one filed issue, `gateupstreamstatus` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `gateupstreamstatus`, state `open`, severity `HIGH`)

**title:** gate_upstream.sh run_case pipe to sed hides loader exit status

**state_note (head):**

GOVERNING TEXT (from the dispositions file, cut at 400 characters): hbundle_regress33:F5 | STATUS-LAUNDERED | RIGHT | DRAFT: NEW HIGH gateupstreamstatus "gate_upstream.sh run_case pipe to sed hides loader exit status" | regress/gate_upstream.sh:73-77,110-140; src/file/file_elf.c:331,387

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Prevent the sed pipe from masking the loader exit status using pipefail or PIPESTATUS

## The code at the cited lines

### `src/file/file_elf.c` around the row's cited line 331 (HEAD 8d9df658, lines 211-451)

```c
  211| 		}
  212| 		break;
  213| 	case ARCH_ALPHA:
  214| 		switch (emachine) {
  215| 		case EM_ALPHA:
  216| 		case -28634:
  217| 			ok = 1;
  218| 		}
  219| 		break;
  220| 	case ARCH_ARM:
  221| 		switch (emachine) {
  222| 		case EM_ARM:
  223| 			ok = 1;
  224| 		}
  225| 		break;
  226| 	/*  case ARCH_AVR:
  227| 		switch (emachine) {
  228| 		case EM_AVR:
  229| 			ok = 1;
  230| 		}
  231| 		break;
  232| 	case ARCH_AVR32:
  233| 		switch (emachine) {
  234| 		case 6317:
  235| 			ok = 1;
  236| 		}
  237| 		break;
  238| 	case ARCH_HPPA:
  239| 		switch (emachine) {
  240| 		case EM_PARISC:
  241| 			ok = 1;
  242| 		}
  243| 		break;  */
  244| 	case ARCH_I960:
  245| 		switch (emachine) {
  246| 		case EM_960:
  247| 			ok = 1;
  248| 		}
  249| 		break;
  250| 	/*  case ARCH_IA64:
  251| 		switch (emachine) {
  252| 		case EM_IA_64:
  253| 			ok = 1;
  254| 		}
  255| 		break;
  256| 	case ARCH_M68K:
  257| 		switch (emachine) {
  258| 		case EM_68K:
  259| 			ok = 1;
  260| 		}
  261| 		break;
  262| 	case ARCH_M32R:
  263| 		switch (emachine) {
  264| 		case EM_M32R:
  265| 			ok = 1;
  266| 		}
  267| 		break;*/
  268| 	case ARCH_MIPS:
  269| 		switch (emachine) {
  270| 		case EM_MIPS:
  271| 		case EM_MIPS_RS3_LE:
  272| 			ok = 1;
  273| 		}
  274| 		break;
  275| 	case ARCH_PPC:
  276| 		switch (emachine) {
  277| 		case EM_PPC:
  278| 		case EM_PPC64:
  279| 			ok = 1;
  280| 		}
  281| 		break;
  282| 	case ARCH_RISCV:
  283| 		switch (emachine) {
  284| 		case 243:
  285| 			ok = 1;
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
  377| 			unencode(p_offset,  &phdr32.p_offset,  Elf32_Off);
  378| 			unencode(p_vaddr,   &phdr32.p_vaddr,   Elf32_Addr);
  379| 			unencode(p_paddr,   &phdr32.p_paddr,   Elf32_Addr);
  380| 			unencode(p_filesz,  &phdr32.p_filesz,  Elf32_Word);
  381| 			unencode(p_memsz,   &phdr32.p_memsz,   Elf32_Word);
  382| 			unencode(p_flags,   &phdr32.p_flags,   Elf32_Word);
  383| 			unencode(p_align,   &phdr32.p_align,   Elf32_Word);
  384| 		}
  385| 
  386| 		if (!allRead) {
  387| 			fprintf(stderr, "Could not read Phdr from %s. Aborting.\n", filename);
  388| 			exit(1);
  389| 		}
  390| 
  391| 		/*
  392| 		 *  Hack for loading PPC kernels that are linked to high
  393| 		 *  addresses. (This requires enabling of instruction and
  394| 		 *  data virtual address translation.)
  395| 		 */
  396| 		if (arch == ARCH_PPC) {
  397| 			if ( (elf64 && (p_vaddr >> 60) != 0) ||
  398| 			    (!elf64 && (p_vaddr >> 28) != 0) )
  399| 				m->cpus[m->bootstrap_cpu]->
  400| 				    cd.ppc.msr |= PPC_MSR_IR | PPC_MSR_DR;
  401| 		}
  402| 
  403| 		if (p_memsz != 0 && (p_type == PT_LOAD ||
  404| 		    (p_type & PF_MASKPROC) == PT_MIPS_REGINFO)) {
  405| 			debug("chunk %i (", i);
  406| 			if (p_type == PT_LOAD)
  407| 				debug("load");
  408| 			else
  409| 				debug("0x%08" PRIx32, (uint32_t) p_type);
  410| 
  411| 			debug(") @ 0x%" PRIx64", vaddr 0x", (uint64_t) p_offset);
  412| 
  413| 			if (elf64)
  414| 				debug("%016" PRIx64, (uint64_t) p_vaddr);
  415| 			else
  416| 				debug("%08" PRIx32, (uint32_t) p_vaddr);
  417| 
  418| 			debug(" len=0x%" PRIx64"\n", (uint64_t) p_memsz);
  419| 
  420| 			if (p_vaddr != p_paddr) {
  421| 				if (elf64)
  422| 					debug("NOTE: vaddr (0x%" PRIx64") and "
  423| 					    "paddr (0x%" PRIx64") differ; using "
  424| 					    "vaddr\n", (uint64_t) p_vaddr,
  425| 					    (uint64_t) p_paddr);
  426| 				else
  427| 					debug("NOTE: vaddr (0x%08" PRIx32") and "
  428| 					    "paddr (0x%08" PRIx32") differ; usin"
  429| 					    "g vaddr\n", (uint32_t) p_vaddr,
  430| 					    (uint32_t)p_paddr);
  431| 			}
  432| 
  433| 			if (p_memsz < p_filesz) {
  434| 				fprintf(stderr, "%s: memsz < filesz. TODO: how"
  435| 				    " to handle this? memsz=%016" PRIx64
  436| 				    " filesz=%016" PRIx64"\n", filename,
  437| 				    (uint64_t) p_memsz, (uint64_t) p_filesz);
  438| 				exit(1);
  439| 			}
  440| 
  441| 			fseek(f, p_offset, SEEK_SET);
  442| 			align_len = 1;
  443| 			if ((p_vaddr & 0xf)==0)		align_len = 0x10;
  444| 			if ((p_vaddr & 0x3f)==0)	align_len = 0x40;
  445| 			if ((p_vaddr & 0xff)==0)	align_len = 0x100;
  446| 			if ((p_vaddr & 0xfff)==0)	align_len = 0x1000;
  447| 			if ((p_vaddr & 0x3fff)==0)	align_len = 0x4000;
  448| 			if ((p_vaddr & 0xffff)==0)	align_len = 0x10000;
  449| 			ofs = 0;  len = chunk_len = align_len;
  450| 			while (ofs < p_filesz && len==chunk_len) {	/* OB-19 */
  451| 				unsigned char *ch;
```


RULES FOR THE EDITS: change ONLY text that appears in this packet; use ONLY fields, functions and macros that appear in it
(a draft that calls an undeclared function or a field that does not exist does not compile); make each `old` long enough to
occur exactly once in its file -- include a distinctive neighbouring line when a statement repeats.

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
