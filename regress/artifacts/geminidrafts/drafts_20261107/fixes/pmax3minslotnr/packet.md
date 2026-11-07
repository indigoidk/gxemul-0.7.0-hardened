# GXemul hardened fork -- DRAFT A FIX for one filed issue, `pmax3minslotnr` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `pmax3minslotnr`, state `open`, severity `LOW`)

**title:** machines/machine_pmax.c 3MIN arm -- option slots 1 and 2 are registered as slot 0 (feeds only a debug message) -- HYGIENE (cosmetic)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T152 (class HYGIENE; reach C, configuration, debugger, host environment or a non-default build; effort: one-line; report rows: A2-46).  Source URLs: https://github.com/rpajarola/gxemul/commit/042b61b040deedf4c1aafb361a563fdc4f9eedb9.  Our site at de8c7547: src/machines/machine_pmax.c:330, :338.  Portable fix: yes -- port rpajarola 042b61b.  Filing check (TRIAGE.md): 0 hits.  Reach C, not build-only (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md B).  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rpajarola 042b61b

## The code at the cited lines

### `src/machines/machine_pmax.c` around the row's cited line 330 (HEAD d2a6f233, lines 285-375)

```c
  285| 
  286| ////fatal("TODO: kmin dev_le_init.\n");
  287| ////abort();
  288| //		dev_le_init(machine, mem, 0x1c0c0000, 0, 0,
  289| //		    KMIN_INTR_LANCE + 8, 4 * 65536);
  290| 
  291| 		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i.kn02ba.0x%x",
  292| 		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC3, KMIN_INTR_SCC_0);
  293| 		dev_scc_init(machine, mem, 0x1c100000, tmpstr,
  294| 		    machine->x11_md.in_use, 0, 1);
  295| 
  296| 		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i.kn02ba.0x%x",
  297| 		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC3, KMIN_INTR_SCC_1);
  298| 		dev_scc_init(machine, mem, 0x1c180000, tmpstr,
  299| 		    machine->x11_md.in_use, 1, 1);
  300| 
  301| 
  302| 		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i.kn02ba.0x%x",
  303| 		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC3, KMIN_INTR_CLOCK);
  304| 		dev_mc146818_init(machine, mem,
  305| 		    KMIN_SYS_CLOCK, tmpstr, MC146818_DEC, 1);
  306| 		    
  307| 		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i.kn02ba.0x%x",
  308| 		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC3, KMIN_INTR_SCSI);
  309| 		dev_asc_init(machine, mem, 0x1c300000, tmpstr,
  310| 		    NULL, DEV_ASC_DEC, NULL, NULL);
  311| 
  312| 		/*
  313| 		 *  TURBOchannel slots 0, 1, and 2 are free for
  314| 		 *  option cards.  These are by default filled with
  315| 		 *  zero or more graphics boards.
  316| 		 *
  317| 		 *  TODO: irqs 
  318| 		 */
  319| 
  320| 		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i",
  321| 		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC0);
  322| 		dev_turbochannel_init(machine, mem, 0,
  323| 		    KMIN_PHYS_TC_0_START, KMIN_PHYS_TC_0_END,
  324| 		    machine->n_gfx_cards >= 1?
  325| 			turbochannel_default_gfx_card : "",
  326| 		    tmpstr);
  327| 
  328| 		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i",
  329| 		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC1);
  330| 		dev_turbochannel_init(machine, mem, 0,
  331| 		    KMIN_PHYS_TC_1_START, KMIN_PHYS_TC_1_END,
  332| 		    machine->n_gfx_cards >= 2?
  333| 			turbochannel_default_gfx_card : "",
  334| 		    tmpstr);
  335| 
  336| 		snprintf(tmpstr, sizeof(tmpstr), "%s.cpu[%i].%i",
  337| 		    machine->path, machine->bootstrap_cpu, KMIN_INT_TC2);
  338| 		dev_turbochannel_init(machine, mem, 0,
  339| 		    KMIN_PHYS_TC_2_START, KMIN_PHYS_TC_2_END,
  340| 		    machine->n_gfx_cards >= 3?
  341| 			turbochannel_default_gfx_card : "",
  342| 		    tmpstr);
  343| 
  344| 		/*  (kmin shared irq numbers (IP) are offset by +8 in the
  345| 		    emulator)  */
  346| 		/*  kmin_csr = dev_kmin_init(cpu, mem, KMIN_REG_INTR);  */
  347| 
  348| 		framebuffer_console_name = "osconsole=0,3";	/* fb,keyb(?) */
  349| 		serial_console_name      = "osconsole=3";	/* ? */
  350| 		break;
  351| 
  352| 	case MACHINE_DEC_3MAXPLUS_5000:	/*  type 4, KN03  */
  353| 		machine->machine_name = strdup("DECsystem 5900 or 5000 (3MAX+) (KN03)");
  354| 
  355| 		/*  5000/240 (KN03-GA, R3000): 40 MHz  */
  356| 		/*  5000/260 (KN05-NB, R4000): 60 MHz  */
  357| 		/*  TODO: are both these type 4?  */
  358| 		if (machine->emulated_hz == 0)
  359| 			machine->emulated_hz = 40000000;
  360| 		if (machine->physical_ram_in_mb > 480)
  361| 			fprintf(stderr, "WARNING! Real KN03 machines cannot "
  362| 			    "have more than 480MB RAM. Continuing anyway.\n");
  363| 
  364| 		/*  KN03 interrupts:  */
  365| fatal("TODO: Legacy rewrite\n");
  366| abort();
  367| //		machine->md_interrupt = kn03_interrupt;
  368| 
  369| 		/*
  370| 		 *  tc0 at mainbus0: 25 MHz clock (slot 0)	(0x1e000000)
  371| 		 *  tc0 slot 1					(0x1e800000)
  372| 		 *  tc0 slot 2					(0x1f000000)
  373| 		 *  ioasic0 at tc0 slot 3 offset 0x0		(0x1f800000)
  374| 		 *    something that has to do with interrupts? (?)(0x1f840000?)
  375| 		 *  le0 at ioasic0 offset 0xc0000		(0x1f8c0000)
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

End with one line: `FIXDRAFT_PMAX3MINSLOTNR: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
