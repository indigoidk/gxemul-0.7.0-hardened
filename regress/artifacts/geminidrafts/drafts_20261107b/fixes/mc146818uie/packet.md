# GXemul hardened fork -- DRAFT A FIX for one filed issue, `mc146818uie` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `mc146818uie`, state `open`, severity `MED`)

**title:** devices/dev_mc146818.c tick -- no once-a-second UF with a UIE interrupt (only a polled UF hack) -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T57 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-36).  Source URLs: https://github.com/rpajarola/gxemul/commit/871e551340226bdc3ed3c3b1c9e0e1fea824aa70.  Our site at de8c7547: src/devices/dev_mc146818.c:357-379.  Portable fix: yes -- port rpajarola 871e551.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- portable fix is ready from rpajarola 871e551

## The code at the cited lines

### `src/devices/dev_mc146818.c` around the row's cited line 357 (HEAD 2d25df65, lines 312-402)

```c
  312| 			} else {
  313| 				data[0] = d->last_addr;
  314| 				return 1;
  315| 			}
  316| 		} else if (relative_addr == 0x00)
  317| 			relative_addr = d->last_addr * 4;
  318| 		else {
  319| 			fatal("[ mc146818: not accessed as an "
  320| 			    "MC146818_ARC_NEC device! ]\n");
  321| 		}
  322| 		break;
  323| 	case MC146818_ARC_JAZZ:
  324| 		/*  See comment for dev_mc146818_jazz_access().  */
  325| 		relative_addr = d->last_addr * 4;
  326| 		break;
  327| 	case MC146818_DEC:
  328| 	case MC146818_SGI:
  329| 		/*
  330| 		 *  This device was originally written for DECstation
  331| 		 *  emulation, so no changes are necessary for that access
  332| 		 *  style.
  333| 		 *
  334| 		 *  SGI access bytes 0x0..0xd at offsets 0x0yz..0xdyz, where yz
  335| 		 *  should be ignored. It works _almost_ as DEC, if offsets are
  336| 		 *  divided by 0x40.
  337| 		 */
  338| 		break;
  339| 	case MC146818_PMPPC:
  340| 		relative_addr *= 4;
  341| 		break;
  342| 	default:
  343| 		;
  344| 	}
  345| 
  346| #ifdef MC146818_DEBUG
  347| 	if (writeflag == MEM_WRITE) {
  348| 		fatal("[ mc146818: write to addr=0x%04x (len %i): ",
  349| 		    (int)relative_addr, (int)len);
  350| 		for (i=0; i<len; i++)
  351| 			fatal("0x%02x ", data[i]);
  352| 		fatal("]\n");
  353| 	}
  354| #endif
  355| 
  356| 	/*
  357| 	 *  Sprite seems to wants UF interrupt status, once every second, or
  358| 	 *  it hangs forever during bootup.  (These do not cause interrupts,
  359| 	 *  but it is good enough... Sprite polls this, iirc.)
  360| 	 *
  361| 	 *  Linux on at least sgimips and evbmips (Malta) wants the UIP bit
  362| 	 *  in REGA to be updated once a second.
  363| 	 */
  364| 	if (relative_addr == MC_REGA*4 || relative_addr == MC_REGC*4) {
  365| 		timet = time(NULL);
  366| 		tmp = gmtime(&timet);
  367| 		d->reg[MC_REGC * 4] &= ~MC_REGC_UF;
  368| 		if (tmp->tm_sec != d->previous_second) {
  369| 			d->n_seconds_elapsed ++;
  370| 			d->previous_second = tmp->tm_sec;
  371| 		}
  372| 		if (d->n_seconds_elapsed > d->uip_threshold) {
  373| 			d->n_seconds_elapsed = 0;
  374| 
  375| 			d->reg[MC_REGA * 4] |= MC_REGA_UIP;
  376| 
  377| 			d->reg[MC_REGC * 4] |= MC_REGC_UF;
  378| 			d->reg[MC_REGC * 4] |= MC_REGC_IRQF;
  379| 
  380| 			/*  For some reason, some Linux/DECstation KN04
  381| 			    kernels want the PF (periodic flag) bit set,
  382| 			    even though interrupts are not enabled?  */
  383| 			d->reg[MC_REGC * 4] |= MC_REGC_PF;
  384| 		} else
  385| 			d->reg[MC_REGA * 4] &= ~MC_REGA_UIP;
  386| 	}
  387| 
  388| 	/*  RTC data is in either BCD format or binary:  */
  389| 	if (d->use_bcd)
  390| 		d->reg[MC_REGB * 4] &= ~(1 << 2);
  391| 	else
  392| 		d->reg[MC_REGB * 4] |= (1 << 2);
  393| 
  394| 	/*  RTC date/time is always Valid:  */
  395| 	d->reg[MC_REGD * 4] |= MC_REGD_VRT;
  396| 
  397| 	if (writeflag == MEM_WRITE) {
  398| 		/*  WRITE:  */
  399| 		switch (relative_addr) {
  400| 		case MC_REGA*4:
  401| 			if ((data[0] & MC_REGA_DVMASK) == MC_BASE_32_KHz)
  402| 				d->timebase_hz = 32000;
```

## The data structures those files define (every field that exists)

### `src/devices/dev_mc146818.c` -- `struct mc_data {` (HEAD lines 65-88)

```c
   65| struct mc_data {
   66| 	int		access_style;
   67| 	int		last_addr;
   68| 
   69| 	int		register_choice;
   70| 	int		reg[N_REGISTERS];
   71| 	int		addrdiv;
   72| 
   73| 	int		use_bcd;
   74| 
   75| 	int		timebase_hz;
   76| 	int		interrupt_hz;
   77| 	int		old_interrupt_hz;
   78| 	struct interrupt irq;
   79| 	struct timer	*timer;
   80| 	volatile int	pending_timer_interrupts;
   81| 
   82| 	int		previous_second;
   83| 	int		n_seconds_elapsed;
   84| 	int		uip_threshold;
   85| 
   86| 	int		ugly_netbsd_prep_hack_done;
   87| 	int		ugly_netbsd_prep_hack_sec;
   88| };
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

End with one line: `FIXDRAFT_MC146818UIE: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
