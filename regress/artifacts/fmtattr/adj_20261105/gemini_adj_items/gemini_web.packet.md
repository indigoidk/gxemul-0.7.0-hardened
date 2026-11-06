# Reading task: code scanning: adjudicate the four queue items (Gemini web; 2026-11-05)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-CSADJ-ff9c` on a line of its own.

# GXemul hardened fork -- adjudicate four queue items from a code-scanning triage (defensive code-quality review)

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises, not just
the derivations.**  Where I state something as fact, ask whether it is true.  A seat that re-derives a premise from something
this brief did NOT give it is worth more than a seat that agrees.  (Earlier today my own first reading of one item, #135 below,
was wrong; a second seat caught it.)

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/` at commit f58105b7.**  There are pristine-2021-upstream copies of GXemul under the
project root (`./src/` and two under `_archive/`).  They are NOT this fork.  If your line numbers disagree with mine by hundreds
you are reading one of them -- say so rather than reconciling.

**If you cannot read files, that is expected** -- the facts you need are inlined in the appendix.  Name any premise you cannot
settle from this packet rather than guessing at it.

## What happened

GitHub CodeQL scanned an old pushed commit (759f7131) and raised 137 alerts.  A triage mapped them onto HEAD and re-scanned the
printf-format class at HEAD by building with `__attribute__((format(printf, ...)))` added to the four diagnostic functions in
`src/include/misc.h` (`debug`, `fatal`, `debugmsg`, `debugmsg_cpu`), so GCC checked every call.  The triage proposes four queue
items.  This pass adjudicates them BEFORE any fix is written.

Everything you need is in the APPENDIX at the end of this message.

## The four proposed items

1. **fmtmissarg** -- three calls whose format names more conversions than arguments: `src/devices/dev_ps2_stuff.c:239` (a guest
   read of timer 2/3's hold register), `src/devices/dev_mb89352.c:305-309` (a guest non-byte access), `src/cpus/cpu_ppc.c:478`
   (the debugger's PPC601 register dump).  Each prints an unspecified value.
2. **disasmnullmnem** -- four `debug("%s\t", mnem)`-style calls where GCC deduces `mnem` may be NULL:
   `src/cpus/cpu_alpha.c:357`, `:651` (two warnings), `src/cpus/cpu_m88k.c:1437`.  A disassembler switch that does not cover an
   opcode leaves `mnem` NULL; glibc prints "(null)", other C libraries may not.  Reached when guest code is disassembled
   (instruction tracing, the debugger).
3. **arcmemdescnr** -- `src/promemul/arcbios.c:1560-1580`, ARC `GetMemoryDescriptor(ptr)`: `int nr = a0 - base; nr /= s; nr++;`,
   then `V0 = base + s * nr; if (nr >= n_memdescriptors) V0 = 0;`.  A guest `a0` below `base` gives `nr <= 0`, which the test
   misses, so the guest gets a pointer below the descriptor table (and `s * nr` can wrap).  The value only goes back to the
   guest in V0; nothing on the host is accessed with it.
4. **fmtattr** -- GCC at HEAD reports 127 lines with a wrong argument TYPE or an extra argument (145 `-Wformat=` + 13
   `-Wformat-extra-args` warnings).  Dominant shape: `%i`/`%x` given a 64-bit value (59 int vs unsigned long, 43 unsigned int
   vs unsigned long).  Effect on x86-64: a truncated or wrong number in a diagnostic.  Proposal: ONE mechanical round that
   fixes all 127 lines with the tree's idiom (`PRIx64` plus a `(uint64_t)` cast, or an `(int)` cast where the value is
   small) AND makes the four attributes permanent in `misc.h` (guarded by `__GNUC__`), so the compiler rejects the class at
   every build.  The 19 `-Wformat-zero-length` warnings are intentional empty lines (`debugmsg(..., "")`) and need
   `-Wno-format-zero-length` or a `"%s", ""` form.

Proposed for NO action, to be dismissed on GitHub once the fixes land: `dev_fdc.c:101` snprintf (CodeQL "overflowing
snprintf": `buf` is `3*DEV_FDC_LENGTH+1` bytes and the loop writes at most `DEV_FDC_LENGTH` three-character items),
`diskimage.c` fopen after a stat (TOCTOU: the emulator opening its own user's image path), two alerts in
`experiments/dump-hp700rx-rom.c` (a standalone tool outside `src/` that the build does not compile), and 15 integer-multiplication alerts graded
BOUNDED or HOST in the triage's table.

## Questions -- answer in this order, VERDICT LINE FIRST

1. **Premise audit.**  Each of these is load-bearing; say TRUE / FALSE / UNSETTLED with your evidence:
   a. Is every one of the 52 GCC warnings that CodeQL did not report already present at 759f7131?  (The triage checked line
      text against `git show 759f7131:<file>`.)
   b. Does `dev_fb_resize()` really cap both sizes at 10..16384 before the copy loop, so `bytes_per_line * y < 2^30`?
   c. In #135, can a guest really supply `a0 < base`, and is V0 the ONLY use of the result?
   d. Does `dev_mb89352.c:305-309`'s format have three conversions and two arguments?
   e. For the NULL `mnem` sites, name one opcode value that reaches the `debug()` with `mnem` still NULL -- or say none can.
2. **Grade each item:** real or not; severity order among the four; and the witness each can carry under this project's
   ladder (a rung-3 cold-debugger probe on an unmodified machine; a construction or build witness; or `detector:` with the
   compiler as the detector).  For fmtattr, what is the right witness term for a compiler-detected class?
3. **Round shape.**  Should fmtattr be ONE round (127 lines + the attribute) or split (per file, or per subsystem)?  Should
   fmtmissarg fold into fmtattr (the attribute catches it) or stay separate because two of its sites are guest-reachable?
   One round for disasmnullmnem's two CPUs, or two?
4. **The smallest edit that breaks each proposed fix and still passes** its proposed detector -- name the row or check that
   would stay green.
5. **Option-set completeness** for arcmemdescnr's fix (`nr < 1 ||` added to the test, the offset computed in a wide type): is
   there a member this brief did not name -- for example declining any `a0` that is not exactly on a descriptor boundary?
6. **The no-action list:** for each entry, agree or disagree with dismissing it, with the reason GitHub should record (false
   positive / won't fix / used in tests).

If, while verifying a claim, you found something ELSE -- say so.

**End with one line:** `CSADJ: <n> ITEMS GRADED, <m> PREMISES FALSE, <k> UNSETTLED; ROUND SHAPE <one phrase>`.


## APPENDIX -- the code the questions are about, inlined (HEAD f58105b7)

### `src/devices/dev_ps2_stuff.c` lines 228-244 (HEAD f58105b7)

```c
  228| 			d->timer_comp[timer_nr] = idata;
  229| 			debug("[ ps2: write timer %i comp: 0x%llx ]\n",
  230| 			    timer_nr, (long long)idata);
  231| 		}
  232| 		break;
  233| 	case 0x0030:	/*  timer hold  */
  234| 		if (writeflag == MEM_READ) {
  235| 			odata = d->timer_hold[timer_nr];
  236| 			debug("[ ps2: read timer %i hold: 0x%llx ]\n",
  237| 			    timer_nr, (long long)odata);
  238| 			if (timer_nr >= 2)
  239| 				fatal("[ WARNING: ps2: read from non-"
  240| 				    "existant timer %i hold register ]\n");
  241| 		} else {
  242| 			d->timer_hold[timer_nr] = idata;
  243| 			debug("[ ps2: write timer %i hold: 0x%llx ]\n",
  244| 			    timer_nr, (long long)idata);
```

### `src/devices/dev_mb89352.c` lines 299-312 (HEAD f58105b7)

```c
  299| DEVICE_ACCESS(mb89352)
  300| {
  301| 	struct mb89352_data *d = (struct mb89352_data *) extra;
  302| 	uint64_t idata = 0, odata = 0;
  303| 
  304| 	if (len != 1) {
  305| 		debugmsg_cpu(cpu, d->subsys, "",
  306| 		    mb89352_abort_on_unimplemented_stuff ? VERBOSITY_ERROR : VERBOSITY_WARNING,
  307| 	    	    "unimplemented LEN: %i-bit access, address 0x%x: 0x%x",
  308| 	    	    len * 8,
  309| 	    	    (int) relative_addr);
  310| 
  311| 		if (mb89352_abort_on_unimplemented_stuff) {
  312| 			cpu->running = 0;
```

### `src/cpus/cpu_ppc.c` lines 470-480 (HEAD f58105b7)

```c
  470| 				debug("\n");
  471| 		}
  472| 	}
  473| 
  474| 	if (coprocs & 2) {
  475| 		debug("cpu%i:  sdr1 = 0x%" PRIx64"\n", x,
  476| 		    (uint64_t) cpu->cd.ppc.spr[SPR_SDR1]);
  477| 		if (cpu->cd.ppc.cpu_type.flags & PPC_601)
  478| 			debug("cpu%i:  PPC601-style, TODO!\n");
  479| 		else {
  480| 			for (i=0; i<8; i++) {
```

### `src/cpus/cpu_alpha.c` lines 300-360 (HEAD f58105b7)

```c
  300| 		break;
  301| 	case 0x08:
  302| 	case 0x09:
  303| 		debug("lda%s\t%s,", opcode == 9? "h" : "", alpha_regname[ra]);
  304| 		alpha_print_imm16_disp(imm, rb);
  305| 		debug("\n");
  306| 		break;
  307| 	case 0x0a:
  308| 	case 0x0b:
  309| 	case 0x0c:
  310| 	case 0x0d:
  311| 	case 0x0e:
  312| 	case 0x0f:
  313| 	case 0x20:
  314| 	case 0x21:
  315| 	case 0x22:
  316| 	case 0x23:
  317| 	case 0x24:
  318| 	case 0x25:
  319| 	case 0x26:
  320| 	case 0x27:
  321| 	case 0x28:
  322| 	case 0x29:
  323| 	case 0x2a:
  324| 	case 0x2b:
  325| 	case 0x2c:
  326| 	case 0x2d:
  327| 	case 0x2e:
  328| 	case 0x2f:
  329| 		floating = 0;
  330| 		switch (opcode) {
  331| 		case 0x0a: mnem = "ldbu"; break;
  332| 		case 0x0b: mnem = "ldq_u"; break;
  333| 		case 0x0c: mnem = "ldwu"; break;
  334| 		case 0x0d: mnem = "stw"; break;
  335| 		case 0x0e: mnem = "stb"; break;
  336| 		case 0x0f: mnem = "stq_u"; break;
  337| 		case 0x20: mnem = "ldf"; floating = 1; break;
  338| 		case 0x21: mnem = "ldg"; floating = 1; break;
  339| 		case 0x22: mnem = "lds"; floating = 1; break;
  340| 		case 0x23: mnem = "ldt"; floating = 1; break;
  341| 		case 0x24: mnem = "stf"; floating = 1; break;
  342| 		case 0x25: mnem = "stg"; floating = 1; break;
  343| 		case 0x26: mnem = "sts"; floating = 1; break;
  344| 		case 0x27: mnem = "stt"; floating = 1; break;
  345| 		case 0x28: mnem = "ldl"; break;
  346| 		case 0x29: mnem = "ldq"; break;
  347| 		case 0x2a: mnem = "ldl_l"; break;
  348| 		case 0x2b: mnem = "ldq_l"; break;
  349| 		case 0x2c: mnem = "stl"; break;
  350| 		case 0x2d: mnem = "stq"; break;
  351| 		case 0x2e: mnem = "stl_c"; break;
  352| 		case 0x2f: mnem = "stq_c"; break;
  353| 		}
  354| 		if (opcode == 0x0b && ra == ALPHA_ZERO) {
  355| 			debug("unop");
  356| 		} else {
  357| 			debug("%s\t", mnem);
  358| 			if (floating)
  359| 				debug("f%i,", ra);
  360| 			else
```

### `src/cpus/cpu_m88k.c` lines 1405-1440 (HEAD f58105b7)

```c
 1405| 				debug(",r%i", s2);
 1406| 
 1407| 			if (running && scale >= 1) {
 1408| 				uint32_t tmpaddr = cpu->cd.m88k.r[s1];
 1409| 				if (iw & 0x200)
 1410| 					tmpaddr += scale * cpu->cd.m88k.r[s2];
 1411| 				else
 1412| 					tmpaddr += cpu->cd.m88k.r[s2];
 1413| 				symbol = get_symbol_name(&cpu->machine->
 1414| 				    symbol_context, tmpaddr, &offset);
 1415| 				if (symbol != NULL && supervisor)
 1416| 					debug("\t; [<%s>]", symbol);
 1417| 				else
 1418| 					debug("\t; [0x%08" PRIx32"]", tmpaddr);
 1419| 			}
 1420| 
 1421| 			debug("\n");
 1422| 		} else switch (op10) {
 1423| 		case 0x20:	/*  clr  */
 1424| 		case 0x22:	/*  set  */
 1425| 		case 0x24:	/*  ext  */
 1426| 		case 0x26:	/*  extu  */
 1427| 		case 0x28:	/*  mak  */
 1428| 		case 0x2a:	/*  rot  */
 1429| 			switch (op10) {
 1430| 			case 0x20: mnem = "clr"; break;
 1431| 			case 0x22: mnem = "set"; break;
 1432| 			case 0x24: mnem = "ext"; break;
 1433| 			case 0x26: mnem = "extu"; break;
 1434| 			case 0x28: mnem = "mak"; break;
 1435| 			case 0x2a: mnem = "rot"; break;
 1436| 			}
 1437| 			debug("%s\tr%i,r%i,", mnem, d, s1);
 1438| 			/*  Don't include w5 for the rot instruction:  */
 1439| 			if (op10 != 0x2a)
 1440| 				debug("%i", w5);
```

### `src/promemul/arcbios.c` lines 1560-1580 (HEAD f58105b7)

```c
 1560| 	case 0x48:		/*  void *GetMemoryDescriptor(void *ptr)  */
 1561| 		debugmsg(SUBSYS_PROMEMUL, "arcbios", VERBOSITY_DEBUG, "GetMemoryDescriptor(0x%08x)",
 1562| 		    (int)cpu->cd.mips.gpr[MIPS_GPR_A0]);
 1563| 
 1564| 		/*  If a0=NULL, then return the first descriptor:  */
 1565| 		if ((uint32_t)cpu->cd.mips.gpr[MIPS_GPR_A0] == 0)
 1566| 			cpu->cd.mips.gpr[MIPS_GPR_V0] =
 1567| 			    machine->md.arc->memdescriptor_base;
 1568| 		else {
 1569| 			int s = machine->md.arc->arc_64bit?
 1570| 			    sizeof(struct arcbios_mem64)
 1571| 			    : sizeof(struct arcbios_mem);
 1572| 			int nr = cpu->cd.mips.gpr[MIPS_GPR_A0] -
 1573| 			    machine->md.arc->memdescriptor_base;
 1574| 			nr /= s;
 1575| 			nr ++;
 1576| 			cpu->cd.mips.gpr[MIPS_GPR_V0] =
 1577| 			    machine->md.arc->memdescriptor_base + s * nr;
 1578| 			if (nr >= machine->md.arc->n_memdescriptors)
 1579| 				cpu->cd.mips.gpr[MIPS_GPR_V0] = 0;
 1580| 		}
```

### `src/devices/dev_fdc.c` lines 92-106 (HEAD f58105b7)

```c
   92| 			debugmsg(SUBSYS_DEVICE, "fdc", VERBOSITY_DEBUG,
   93| 			    "read from reg %i", (int)relative_addr);
   94| 			odata = d->reg[relative_addr];
   95| 		} else {
   96| 			char buf[3 * DEV_FDC_LENGTH + 1];
   97| 			size_t p = 0;
   98| 
   99| 			buf[0] = '\0';
  100| 			for (i=0; i<len && i<DEV_FDC_LENGTH; i++)
  101| 				p += snprintf(buf + p, sizeof(buf) - p,
  102| 				    " %02x", data[i]);
  103| 
  104| 			debugmsg(SUBSYS_DEVICE, "fdc", VERBOSITY_DEBUG,
  105| 			    "write to reg %i:%s", (int)relative_addr, buf);
  106| 			d->reg[relative_addr] = idata;
```

### `src/include/misc.h` lines 255-272 (HEAD f58105b7)

```c
  255| #define	VERBOSITY_INFO		2
  256| #define	VERBOSITY_DEBUG		3
  257| #define	ENOUGH_VERBOSITY(subsys,reqverb)	(debugmsg_current_verbosity[(subsys)] >= (reqverb))
  258| extern int *debugmsg_current_verbosity;
  259| extern int debugmsg_break_on_error;		/*  #261  */
  260| void debug_indentation(int diff);
  261| void debug(const char *fmt, ...);
  262| void fatal(const char *fmt, ...);
  263| void debugmsg_init();
  264| int debugmsg_register_subsystem(const char* name);
  265| void debugmsg_change_settings(char *subsystem_name, char *n);
  266| void debugmsg_print_settings(const char *subsystem_name);
  267| void debugmsg_add_verbosity_level(int subsystem, int verbosity_delta);
  268| void debugmsg_set_verbosity_level(int subsystem, int verbosity);
  269| void debugmsg(int subsystem, const char *name, int verbosity_required, const char *fmt, ...);
  270| void debugmsg_cpu(struct cpu* cpu, int subsystem, const char *name, int verbosity_required, const char *fmt, ...);
  271| int debugmsg_set_breakpoint(const char *subsystem_name, int level);
  272| void debugmsg_print_breakpoints(void);
```

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`CSADJ: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
