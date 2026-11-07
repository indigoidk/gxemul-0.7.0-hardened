# GXemul hardened fork -- DRAFT A FIX for one filed issue, `pmaxsystype` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `pmaxsystype`, state `open`, severity `MED`)

**title:** machines/machine_pmax.c environment + promemul/dec_prom.c:dec_jumptable_func -- no `systype` variable (Ultrix 3.1D panics) and the old jump table's close() at 0x50 returns -1 -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T74 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-65).  Source URLs: https://github.com/rpajarola/gxemul/commit/12306ee4747fd15a0c67cb2ecc3318ff2f7256d4.  Our site at de8c7547: src/machines/machine_pmax.c:935-940; src/promemul/dec_prom.c:186-195.  Portable fix: yes -- port rpajarola 12306ee.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Port available from rpajarola 12306ee

## The code at the cited lines

### `src/machines/machine_pmax.c` around the row's cited line 935 (HEAD d2a6f233, lines 890-980)

```c
  890| 	store_buf(cpu, DEC_MEMMAP_ADDR,
  891| 	    (char *)machine->md.pmax->memmap, sizeof(struct dec_memmap));
  892| 
  893| 	/*  Environment variables:  */
  894| 	addr = DEC_PROM_STRINGS;
  895| 
  896| 	if (machine->x11_md.in_use && machine->n_gfx_cards > 0)
  897| 		/*  (0,3)  Keyboard and Framebuffer  */
  898| 		add_environment_string(cpu, framebuffer_console_name, &addr);
  899| 	else
  900| 		/*  Serial console  */
  901| 		add_environment_string(cpu, serial_console_name, &addr);
  902| 
  903| 	/*
  904| 	 *  The KN5800 (SMP system) uses a CCA (console communications
  905| 	 *  area):  (See VAX 6000 documentation for details.)
  906| 	 */
  907| 	{
  908| 		char tmps[300];
  909| 		snprintf(tmps, sizeof(tmps), "cca=%" PRIx32,
  910| 		    (uint32_t) (DEC_DECCCA_BASEADDR + 0xa0000000ULL));
  911| 		add_environment_string(cpu, tmps, &addr);
  912| 	}
  913| 
  914| 	/*  These are needed for Sprite to boot:  */
  915| 	{
  916| 		char tmps[500];
  917| 
  918| 		snprintf(tmps, sizeof(tmps), "boot=%s", machine->bootarg);
  919| 		tmps[sizeof(tmps)-1] = '\0';
  920| 		add_environment_string(cpu, tmps, &addr);
  921| 
  922| 		snprintf(tmps, sizeof(tmps), "bitmap=0x%" PRIx32, (uint32_t)
  923| 		    ( (DEC_MEMMAP_ADDR + sizeof(uint32_t) /* skip the
  924| 			page size and point to the memmap */
  925| 		    ) & 0xffffffffULL) );
  926| 		tmps[sizeof(tmps)-1] = '\0';
  927| 		add_environment_string(cpu, tmps, &addr);
  928| 
  929| 		snprintf(tmps, sizeof(tmps), "bitmaplen=0x%" PRIx32, (uint32_t)
  930| 		    ( machine->physical_ram_in_mb * 1048576 / 4096 / 8) );
  931| 		tmps[sizeof(tmps)-1] = '\0';
  932| 		add_environment_string(cpu, tmps, &addr);
  933| 	}
  934| 
  935| 	add_environment_string(cpu, "scsiid0=7", &addr);
  936| 	add_environment_string(cpu, "bootmode=a", &addr);
  937| 	add_environment_string(cpu, "testaction=q", &addr);
  938| 	add_environment_string(cpu, "haltaction=h", &addr);
  939| 	add_environment_string(cpu, "more=24", &addr);
  940| 
  941| 	/*  Used in at least Ultrix on the 5100:  */
  942| 	add_environment_string(cpu, "scsiid=7", &addr);
  943| 	add_environment_string(cpu, "baud0=9600", &addr);
  944| 	add_environment_string(cpu, "baud1=9600", &addr);
  945| 	add_environment_string(cpu, "baud2=9600", &addr);
  946| 	add_environment_string(cpu, "baud3=9600", &addr);
  947| 	add_environment_string(cpu, "iooption=0x1", &addr);
  948| 
  949| 	/*  The end:  */
  950| 	add_environment_string(cpu, "", &addr);
  951| }
  952| 
  953| 
  954| MACHINE_DEFAULT_CPU(pmax)
  955| {
  956| 	if (machine->machine_subtype > 2)
  957| 		CHECK_ALLOCATION(machine->cpu_name = strdup("R3000A"));
  958| 
  959| 	if (machine->machine_subtype > 1 && machine->cpu_name == NULL)
  960| 		CHECK_ALLOCATION(machine->cpu_name = strdup("R3000"));
  961| 
  962| 	if (machine->cpu_name == NULL)
  963| 		CHECK_ALLOCATION(machine->cpu_name = strdup("R2000"));
  964| }
  965| 
  966| 
  967| MACHINE_DEFAULT_RAM(pmax)
  968| {
  969| 	switch (machine->machine_subtype) {
  970| 	case MACHINE_DEC_PMAX_3100:
  971| 		machine->physical_ram_in_mb = 24;
  972| 		break;
  973| 	case MACHINE_DEC_3MAX_5000:
  974| 		machine->physical_ram_in_mb = 64;
  975| 		break;
  976| 	default:machine->physical_ram_in_mb = 32;
  977| 	}
  978| }
  979| 
  980| 
```

### `src/promemul/dec_prom.c` around the row's cited line 186 (HEAD d2a6f233, lines 141-231)

```c
  141| 			int disk_id = diskimage_bootdev(cpu->machine, NULL);
  142| 			int res;
  143| 			unsigned char *tmp_buf;
  144| 
  145| 			CHECK_ALLOCATION(tmp_buf = (unsigned char *)
  146| 			    malloc(cpu->cd.mips.gpr[MIPS_GPR_A2]));
  147| 
  148| 			res = diskimage_access(cpu->machine, disk_id,
  149| 			    DISKIMAGE_SCSI, 0, current_file_offset, tmp_buf,
  150| 			    cpu->cd.mips.gpr[MIPS_GPR_A2]);
  151| 
  152| 			/*  If the transfer was successful, transfer the data
  153| 			    to emulated memory:  */
  154| 			if (res) {
  155| 				uint64_t dst = cpu->cd.mips.gpr[MIPS_GPR_A1];
  156| 				store_buf(cpu, dst, (char *)tmp_buf,
  157| 				    cpu->cd.mips.gpr[MIPS_GPR_A2]);
  158| 				cpu->cd.mips.gpr[MIPS_GPR_V0] =
  159| 				    cpu->cd.mips.gpr[MIPS_GPR_A2];
  160| 				current_file_offset +=
  161| 				    cpu->cd.mips.gpr[MIPS_GPR_A2];
  162| 			}
  163| 
  164| 			free(tmp_buf);
  165| 		}
  166| 		break;
  167| 	case 0x58:	/*  lseek(handle, offset[, whence])  */
  168| 		/*  TODO  */
  169| 		if (cpu->cd.mips.gpr[MIPS_GPR_A2] == 0)
  170| 			current_file_offset = cpu->cd.mips.gpr[MIPS_GPR_A1];
  171| 		else
  172| 			fatal("WARNING! Unimplemented whence in "
  173| 			    "dec_jumptable_func()\n");
  174| 		cpu->cd.mips.gpr[MIPS_GPR_V0] = 0;
  175| 		break;
  176| 	case 0x68:	/*  putchar()  */
  177| 		console_putchar(cpu->machine->main_console_handle,
  178| 		    cpu->cd.mips.gpr[MIPS_GPR_A0]);
  179| 		break;
  180| 	case 0x88:	/*  printf()  */
  181| 		return 0x30;
  182| 	case 0x108:	/*  getenv2()  */
  183| 		return 0x64;
  184| 	default:
  185| 		/*  #245: emit one verbosity-gated line instead of an
  186| 		    unconditional register dump + a0 string scan, so a guest
  187| 		    spamming bad jump-table vectors can't flood the host log
  188| 		    (raise promemul verbosity / `break promemul` for full state). */
  189| 		debugmsg_cpu(cpu, SUBSYS_PROMEMUL, "dec", VERBOSITY_DEBUG,
  190| 		    "unimplemented JUMP TABLE vector 0x%x (decimal function %i)",
  191| 		    vector, vector/8);
  192| 		/*  #241: return an error to the guest instead of halting.  */
  193| 		cpu->cd.mips.gpr[MIPS_GPR_V0] = (int32_t) -1;
  194| 	}
  195| 
  196| 	return 0;
  197| }
  198| 
  199| 
  200| /*
  201|  *  decstation_prom_emul():
  202|  *
  203|  *  DECstation PROM emulation.
  204|  *
  205|  *  Callback functions:
  206|  *	0x0c	strcmp()
  207|  *	0x14	strlen()
  208|  *	0x24	getchar()
  209|  *	0x28	gets()
  210|  *	0x2c	puts()
  211|  *	0x30	printf()
  212|  *	0x38	iopoll()
  213|  *	0x54	bootinit()
  214|  *	0x58	bootread()
  215|  *	0x64	getenv()
  216|  *	0x6c	slot_address()
  217|  *	0x70	wbflush()
  218|  *	0x7c	clear_cache()
  219|  *	0x80	getsysid()
  220|  *	0x84	getbitmap()
  221|  *	0x88	disableintr()
  222|  *	0x8c	enableintr()
  223|  *	0x9c	halt()
  224|  *	0xa4	gettcinfo()
  225|  *	0xa8	execute_cmd()
  226|  *	0xac	rex()
  227|  */
  228| int decstation_prom_emul(struct cpu *cpu)
  229| {
  230| 	int i, j, ch, argreg, argdata;
  231| 	int vector = cpu->pc & 0xfff;
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

End with one line: `FIXDRAFT_PMAXSYSTYPE: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
