# GXemul hardened fork -- DRAFT A FIX for one filed issue, `mc146818reg63` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `mc146818reg63`, state `open`, severity `MED`)

**title:** devices/dev_mc146818.c:mc146818_update_time -- DEC register 63 (NVRAM) is overwritten with the year on every time read -- WRONG-RESULT (NVRAM byte clobbered)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T56 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-34).  Source URLs: https://github.com/rpajarola/gxemul/commit/871e551340226bdc3ed3c3b1c9e0e1fea824aa70.  Our site at de8c7547: src/devices/dev_mc146818.c:258, :272, :529.  Portable fix: yes -- port rpajarola 871e551.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- portable fix is ready from rpajarola 871e551

## The code at the cited lines

### `src/devices/dev_mc146818.c` around the row's cited line 258 (HEAD 2d25df65, lines 213-303)

```c
  213| 		break;
  214| 	case MC146818_ARC_NEC:
  215| 		d->reg[4 * MC_YEAR] += (0x18 - 104);
  216| 		break;
  217| 	case MC146818_CATS:
  218| 		d->reg[4 * MC_YEAR] %= 100;
  219| 		break;
  220| 	case MC146818_SGI:
  221| 		/*
  222| 		 *  NetBSD/sgimips assumes data in BCD format.
  223| 		 *  Also, IRIX stores the year value in a weird
  224| 		 *  format, according to ../arch/sgimips/sgimips/clockvar.h
  225| 		 *  in NetBSD:
  226| 		 *
  227| 		 *  "If year < 1985, store (year - 1970), else
  228| 		 *   (year - 1940). This matches IRIX semantics."
  229| 		 *
  230| 		 *  Another rule: It seems that a real SGI IP32 box
  231| 		 *  uses the value 5 for the year 2005.
  232| 		 */
  233| 		d->reg[4 * MC_YEAR] =
  234| 		    d->reg[4 * MC_YEAR] >= 100 ?
  235| 			(d->reg[4 * MC_YEAR] - 100) :
  236| 		      (
  237| 			d->reg[4 * MC_YEAR] < 85 ?
  238| 			  (d->reg[4 * MC_YEAR] - 30 + 40)
  239| 			: (d->reg[4 * MC_YEAR] - 40)
  240| 		      );
  241| 		/*  Century:  */
  242| 		d->reg[72 * 4] = 19 + (tmp->tm_year / 100);
  243| 		break;
  244| 	case MC146818_DEC:
  245| 		/*
  246| 		 *  DECstations must have 72 or 73 in the Year field, or
  247| 		 *  Ultrix screems. This is also mentioned in NetBSD's
  248| 		 *  mcclock.c.  Unfortunately, this means that NetBSD cannot
  249| 		 *  know what year it actually is, so it has to deduce it
  250| 		 *  from the filesystem.
  251| 		 */
  252| 		d->reg[4 * MC_YEAR] = 72;
  253| 
  254| 		/*
  255| 		 *  Linux on DECstation stores the year in register 63,
  256| 		 *  but no other DECstation OS does? (Hm.)
  257| 		 */
  258| 		d->reg[4 * 63]  = tmp->tm_year - 100;
  259| 		break;
  260| 	}
  261| 
  262| 	if (d->use_bcd) {
  263| 		d->reg[4 * MC_SEC]   = to_bcd(d->reg[4 * MC_SEC]);
  264| 		d->reg[4 * MC_MIN]   = to_bcd(d->reg[4 * MC_MIN]);
  265| 		d->reg[4 * MC_HOUR]  = to_bcd(d->reg[4 * MC_HOUR]);
  266| 		d->reg[4 * MC_DOW]   = to_bcd(d->reg[4 * MC_DOW]);
  267| 		d->reg[4 * MC_DOM]   = to_bcd(d->reg[4 * MC_DOM]);
  268| 		d->reg[4 * MC_MONTH] = to_bcd(d->reg[4 * MC_MONTH]);
  269| 		d->reg[4 * MC_YEAR]  = to_bcd(d->reg[4 * MC_YEAR]);
  270| 
  271| 		/*  Used by Linux on DECstation: (Hm)  */
  272| 		d->reg[4 * 63]       = to_bcd(d->reg[4 * 63]);
  273| 
  274| 		/*  Used on SGI:  */
  275| 		d->reg[4 * 72]       = to_bcd(d->reg[4 * 72]);
  276| 	}
  277| }
  278| 
  279| 
  280| DEVICE_ACCESS(mc146818)
  281| {
  282| 	struct mc_data *d = (struct mc_data *) extra;
  283| 	struct tm *tmp;
  284| 	time_t timet;
  285| 	size_t i;
  286| 
  287| 	/*  NOTE/TODO: This access function only handles 8-bit accesses!  */
  288| 
  289| 	relative_addr /= d->addrdiv;
  290| 
  291| 	/*  Different ways of accessing the registers:  */
  292| 	switch (d->access_style) {
  293| 	case MC146818_ALGOR:
  294| 	case MC146818_CATS:
  295| 	case MC146818_PC_CMOS:
  296| 		if ((relative_addr & 1) == 0x00) {
  297| 			if (writeflag == MEM_WRITE) {
  298| 				d->last_addr = data[0];
  299| 				return 1;
  300| 			} else {
  301| 				data[0] = d->last_addr;
  302| 				return 1;
  303| 			}
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

End with one line: `FIXDRAFT_MC146818REG63: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
