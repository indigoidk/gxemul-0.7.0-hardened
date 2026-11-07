# GXemul hardened fork -- DRAFT A FIX for one filed issue, `mb89352fmtargs` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `mb89352fmtargs`, state `open`, severity `MED`)

**title:** devices/dev_mb89352.c:DEVICE_ACCESS -- the "unimplemented LEN" message has three conversions and two arguments (debugmsg_cpu has no format attribute) -- HOST-UB (guest-triggered undefined behaviour in the host, just before the halt; a crash is not established)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T141 (class HOST-UB; reach K, guest kernel, firmware or device registers; effort: one-line; report rows: A1-22, A(c)#15).  Source URLs: https://github.com/retroprom/gxemul/commit/8f4c717f.  Our site at de8c7547: src/devices/dev_mb89352.c:305-309; src/include/misc.h:270.  Portable fix: yes -- port upstream 8f4c717f.  Filing check (TRIAGE.md): 0 hits.  Class HOST-UB, at least MED (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md B): guest-triggered host undefined behaviour, not hygiene; a crash is not established.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port upstream 8f4c717f.

## The code at the cited lines

### `src/devices/dev_mb89352.c` around the row's cited line 305 (HEAD 2d25df65, lines 260-350)

```c
  260| 		/*  #338: publish how many bytes ACTUALLY arrived. This is the
  261| 		    only place that knows -- transfer_bufpos counted them one
  262| 		    at a time above -- and it is reached exactly when the
  263| 		    buffer has filled, so the command now becomes eligible
  264| 		    because the data is present rather than because it was
  265| 		    promised.  */
  266| 		d->xferp->data_out_offset = d->transfer_bufpos;
  267| 
  268| 		res = diskimage_scsicommand(cpu,
  269| 	    	    d->target, DISKIMAGE_SCSI, d->xferp);
  270| 
  271| 		// TODO: How about failure results?
  272| 		d->phase = PH_STAT;
  273| 		break;
  274| 
  275| 	case PH_CMD:
  276| 		res = diskimage_scsicommand(cpu,
  277| 	    	    d->target, DISKIMAGE_SCSI, d->xferp);
  278| 
  279| 		if (res == 2)
  280| 			d->phase = PH_DATAOUT;
  281| 		else if (d->xferp->data_in != NULL)
  282| 			d->phase = PH_DATAIN;
  283| 		else
  284| 			d->phase = PH_STAT;
  285| 		break;
  286| 
  287| 	default:
  288| 		debugmsg_cpu(cpu, d->subsys, "", VERBOSITY_ERROR,
  289| 	    	    "DREG write: UNIMPLEMENTED PHASE %i", d->phase);
  290| 	    	cpu->running = 0;
  291| 	}
  292| 	
  293| 	d->reg[PSNS] |= PSNS_REQ;
  294| 	d->reg[SSTS] &= ~SSTS_XFR;
  295| 	d->reg[INTS] |= INTS_CMD_DONE;
  296| }
  297| 
  298| 
  299| DEVICE_ACCESS(mb89352)
  300| {
  301| 	struct mb89352_data *d = (struct mb89352_data *) extra;
  302| 	uint64_t idata = 0, odata = 0;
  303| 
  304| 	if (len != 1) {
  305| 		debugmsg_cpu(cpu, d->subsys, "",
  306| 		    mb89352_abort_on_unimplemented_stuff ? VERBOSITY_ERROR : VERBOSITY_WARNING,
  307| 	    	    "unimplemented LEN: %zu-bit access, address 0x%x",
  308| 	    	    len * 8,
  309| 	    	    (int) relative_addr);
  310| 
  311| 		if (mb89352_abort_on_unimplemented_stuff) {
  312| 			cpu->running = 0;
  313| 			return 0;
  314| 		}
  315| 	}
  316| 
  317| 	int regnr = (relative_addr >> 2) & (MB89352_NREGS - 1);
  318| 
  319| 	if (writeflag == MEM_WRITE)
  320| 		idata = memory_readmax64(cpu, data, len);
  321| 	else
  322| 		odata = d->reg[regnr];
  323| 
  324| 	reg_debug(cpu, d, writeflag, regnr, idata);
  325| 
  326| 	switch (regnr) {
  327| 
  328| 	case BDID:
  329| 		if (writeflag == MEM_WRITE) {
  330| 			d->reg[BDID] = idata;
  331| 			if (idata != 7)
  332| 				debugmsg_cpu(cpu, d->subsys, "",
  333| 				    VERBOSITY_INFO, "unimplemented BDID value: 0x%x",
  334| 			    	    (int) idata);
  335| 		} else {
  336| 			odata = (1 << d->reg[BDID]);
  337| 		}
  338| 		break;
  339| 
  340| 	case SCTL:
  341| 		if (writeflag == MEM_WRITE) {
  342| 			d->reg[SCTL] = idata;
  343| 
  344| 			if (idata & SCTL_DIAG)
  345| 				debugmsg_cpu(cpu, d->subsys, "",
  346| 				    VERBOSITY_ERROR,
  347| 			    	    "Diagnostics mode NOT IMPLEMENTED");
  348| 
  349| 			if (idata & SCTL_CTRLRST) {
  350| 				debugmsg(d->subsys, "", VERBOSITY_INFO, "resetting controller");
```

### `src/include/misc.h` around the row's cited line 270 (HEAD 2d25df65, lines 225-315)

```c
  225| /*  bootblock_apple.c:  */
  226| int apple_load_bootblock(struct machine *m, struct cpu *cpu,
  227| 	int disk_id, int disk_type, int *n_loadp, char ***load_namesp);
  228| 
  229| 
  230| /*  bootblock_iso9660.c:  */
  231| int iso_load_bootblock(struct machine *m, struct cpu *cpu,
  232| 	int disk_id, int disk_type, int iso_type, unsigned char *buf,
  233| 	int *n_loadp, char ***load_namesp);
  234| 
  235| 
  236| /*  dec_prom.c:  */
  237| int decstation_prom_emul(struct cpu *cpu);
  238| 
  239| 
  240| /*  debugmsg.c:  */
  241| #define	SUBSYS_ALL		-1
  242| #define	SUBSYS_STARTUP		0	/*  Startup messages  */
  243| #define	SUBSYS_EMUL		1	/*  Emulation setup related  */
  244| #define	SUBSYS_DISK		2	/*  Disk I/O related  */
  245| #define	SUBSYS_NET		3	/*  Network related  */
  246| #define	SUBSYS_MACHINE		4	/*  Machine related  */
  247| #define	SUBSYS_DEVICE		5	/*  Device specific  */
  248| #define	SUBSYS_CPU		6	/*  General CPU  */
  249| #define	SUBSYS_MEMORY		7	/*  Memory related  */
  250| #define	SUBSYS_EXCEPTION	8	/*  CPU exceptions  */
  251| #define	SUBSYS_PROMEMUL		9	/*  PROM emulation related  */
  252| #define	SUBSYS_X11		10	/*  X11 related  */
  253| #define	VERBOSITY_ERROR		0
  254| #define	VERBOSITY_WARNING	1
  255| #define	VERBOSITY_INFO		2
  256| #define	VERBOSITY_DEBUG		3
  257| #define	ENOUGH_VERBOSITY(subsys,reqverb)	(debugmsg_current_verbosity[(subsys)] >= (reqverb))
  258| extern int *debugmsg_current_verbosity;
  259| extern int debugmsg_break_on_error;		/*  #261  */
  260| /*  #584: the diagnostic functions are printf-like; with GCC or clang a format
  261|     that does not match its arguments is a compiler warning, which gate 1
  262|     refuses.  Other compilers see nothing.  */
  263| #ifdef __GNUC__
  264| #define	GX_PRINTF(f, a)	__attribute__((format(printf, f, a)))
  265| #else
  266| #define	GX_PRINTF(f, a)
  267| #endif
  268| void debug_indentation(int diff);
  269| void debug(const char *fmt, ...) GX_PRINTF(1, 2);
  270| void fatal(const char *fmt, ...) GX_PRINTF(1, 2);
  271| void debugmsg_init();
  272| int debugmsg_register_subsystem(const char* name);
  273| void debugmsg_change_settings(char *subsystem_name, char *n);
  274| void debugmsg_print_settings(const char *subsystem_name);
  275| void debugmsg_add_verbosity_level(int subsystem, int verbosity_delta);
  276| void debugmsg_set_verbosity_level(int subsystem, int verbosity);
  277| void debugmsg(int subsystem, const char *name, int verbosity_required, const char *fmt, ...) GX_PRINTF(4, 5);
  278| void debugmsg_cpu(struct cpu* cpu, int subsystem, const char *name, int verbosity_required, const char *fmt, ...) GX_PRINTF(5, 6);
  279| int debugmsg_set_breakpoint(const char *subsystem_name, int level);
  280| void debugmsg_print_breakpoints(void);
  281| 
  282| 
  283| /*  dreamcast.c:  */
  284| void dreamcast_machine_setup(struct machine *);
  285| void dreamcast_emul(struct cpu *cpu);
  286| 
  287| 
  288| /*  dreamcast_scramble.c:  */
  289| void dreamcast_descramble(char *from, char *to);
  290| 
  291| 
  292| /*  file.c:  */
  293| int file_n_executables_loaded(void);
  294| void file_load(struct machine *machine, struct memory *mem,
  295| 	char *filename, uint64_t *entrypointp,
  296| 	int arch, uint64_t *gpp, int *byte_order, uint64_t *tocp);
  297| 
  298| 
  299| /*  luna88kprom.c:  */
  300| void luna88kprom_init(struct machine *machine);
  301| int luna88kprom_emul(struct cpu *cpu);
  302| 
  303| 
  304| /*  misc.c:  */
  305| void color_prompt();
  306| void color_normal();
  307| void color_error(bool bold);
  308| void color_debugmsg_subsystem();
  309| void color_debugmsg_name();
  310| void color_banner();
  311| void color_pc_indicator();
  312| const char* color_symbol_ptr();
  313| const char* color_normal_ptr();
  314| unsigned long long mystrtoull(const char *s, char **endp, int base);
  315| int mymkstemp(char *templ);
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

End with one line: `FIXDRAFT_MB89352FMTARGS: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
