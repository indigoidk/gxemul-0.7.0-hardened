# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `mc146818reg63` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `mc146818reg63`, state `open`)

**title:** devices/dev_mc146818.c:mc146818_update_time -- DEC register 63 (NVRAM) is overwritten with the year on every time read -- WRONG-RESULT (NVRAM byte clobbered)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T56 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-34).  Source URLs: https://github.com/rpajarola/gxemul/commit/871e551340226bdc3ed3c3b1c9e0e1fea824aa70.  Our site at de8c7547: src/devices/dev_mc146818.c:258, :272, :529.  Portable fix: yes -- port rpajarola 871e551.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/devices/dev_mc146818.c` -- AT HEAD, lines 185-277 (`*` marks a line your previous draft changed)

```c
  185|  static void mc146818_update_time(struct mc_data *d)
  186|  {
  187|  	struct tm *tmp;
  188|  	time_t timet;
  189|  
  190|  	timet = time(NULL);
  191|  	tmp = gmtime(&timet);
  192|  
  193|  	d->reg[4 * MC_SEC]   = tmp->tm_sec;
  194|  	d->reg[4 * MC_MIN]   = tmp->tm_min;
  195|  	d->reg[4 * MC_HOUR]  = tmp->tm_hour;
  196|  	d->reg[4 * MC_DOW]   = tmp->tm_wday + 1;
  197|  	d->reg[4 * MC_DOM]   = tmp->tm_mday;
  198|  	d->reg[4 * MC_MONTH] = tmp->tm_mon + 1;
  199|  	d->reg[4 * MC_YEAR]  = tmp->tm_year;
  200|  
  201|  	/*
  202|  	 *  Special hacks for emulating the behaviour of various machines:
  203|  	 */
  204|  	switch (d->access_style) {
  205|  	case MC146818_ALGOR:
  206|  		/*
  207|  		 *  NetBSD/evbmips sources indicate that the Algor year base
  208|  		 *  is 1920. This makes the time work with NetBSD in Malta
  209|  		 *  emulation. However, for Linux, commenting out this line
  210|  		 *  works better.  (TODO: Find a way to make both work?)
  211|  		 */
  212|  		d->reg[4 * MC_YEAR] += 80;
  213|  		break;
  214|  	case MC146818_ARC_NEC:
  215|  		d->reg[4 * MC_YEAR] += (0x18 - 104);
  216|  		break;
  217|  	case MC146818_CATS:
  218|  		d->reg[4 * MC_YEAR] %= 100;
  219|  		break;
  220|  	case MC146818_SGI:
  221|  		/*
  222|  		 *  NetBSD/sgimips assumes data in BCD format.
  223|  		 *  Also, IRIX stores the year value in a weird
  224|  		 *  format, according to ../arch/sgimips/sgimips/clockvar.h
  225|  		 *  in NetBSD:
  226|  		 *
  227|  		 *  "If year < 1985, store (year - 1970), else
  228|  		 *   (year - 1940). This matches IRIX semantics."
  229|  		 *
  230|  		 *  Another rule: It seems that a real SGI IP32 box
  231|  		 *  uses the value 5 for the year 2005.
  232|  		 */
  233|  		d->reg[4 * MC_YEAR] =
  234|  		    d->reg[4 * MC_YEAR] >= 100 ?
  235|  			(d->reg[4 * MC_YEAR] - 100) :
  236|  		      (
  237|  			d->reg[4 * MC_YEAR] < 85 ?
  238|  			  (d->reg[4 * MC_YEAR] - 30 + 40)
  239|  			: (d->reg[4 * MC_YEAR] - 40)
  240|  		      );
  241|  		/*  Century:  */
  242|  		d->reg[72 * 4] = 19 + (tmp->tm_year / 100);
  243|  		break;
  244|  	case MC146818_DEC:
  245|  		/*
  246|  		 *  DECstations must have 72 or 73 in the Year field, or
  247|  		 *  Ultrix screems. This is also mentioned in NetBSD's
  248|  		 *  mcclock.c.  Unfortunately, this means that NetBSD cannot
  249|  		 *  know what year it actually is, so it has to deduce it
  250|  		 *  from the filesystem.
  251|  		 */
  252|  		d->reg[4 * MC_YEAR] = 72;
  253|  
  254|* 		/*
  255|* 		 *  Linux on DECstation stores the year in register 63,
  256|* 		 *  but no other DECstation OS does? (Hm.)
  257|* 		 */
  258|* 		d->reg[4 * 63]  = tmp->tm_year - 100;
  259|  		break;
  260|  	}
  261|  
  262|  	if (d->use_bcd) {
  263|  		d->reg[4 * MC_SEC]   = to_bcd(d->reg[4 * MC_SEC]);
  264|  		d->reg[4 * MC_MIN]   = to_bcd(d->reg[4 * MC_MIN]);
  265|  		d->reg[4 * MC_HOUR]  = to_bcd(d->reg[4 * MC_HOUR]);
  266|  		d->reg[4 * MC_DOW]   = to_bcd(d->reg[4 * MC_DOW]);
  267|  		d->reg[4 * MC_DOM]   = to_bcd(d->reg[4 * MC_DOM]);
  268|  		d->reg[4 * MC_MONTH] = to_bcd(d->reg[4 * MC_MONTH]);
  269|  		d->reg[4 * MC_YEAR]  = to_bcd(d->reg[4 * MC_YEAR]);
  270|  
  271|* 		/*  Used by Linux on DECstation: (Hm)  */
  272|* 		d->reg[4 * 63]       = to_bcd(d->reg[4 * 63]);
  273|* 
  274|  		/*  Used on SGI:  */
  275|  		d->reg[4 * 72]       = to_bcd(d->reg[4 * 72]);
  276|  	}
  277|  }
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


## Your previous draft's edits

```json
[
  {
    "file": "src/devices/dev_mc146818.c",
    "old": "\t\t/*\n\t\t *  Linux on DECstation stores the year in register 63,\n\t\t *  but no other DECstation OS does? (Hm.)\n\t\t */\n\t\td->reg[4 * 63]  = tmp->tm_year - 100;\n",
    "new": "",
    "why": "Stop clobbering NVRAM register 63 on every time read."
  },
  {
    "file": "src/devices/dev_mc146818.c",
    "old": "\t\t/*  Used by Linux on DECstation: (Hm)  */\n\t\td->reg[4 * 63]       = to_bcd(d->reg[4 * 63]);\n\n",
    "new": "",
    "why": "Remove corresponding BCD conversion for NVRAM register 63."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_MC146818REG63: DEFECT, 1 FINDINGS
1. The diff removes the register 63 overwrites at two sites (lines 251 and 268, which likely correspond to the issue's 258 and 272), but completely misses the third site named in the issue at line 529.
2. No added `return`, `goto`, `break`, or early exit is introduced to skip any code; the existing `break` remains in place, and the common tail runs as before.
3. The function returns `void`, so no return value paths are changed.
4. The diff changes nothing else beyond removing the defect; no other state is left set or cleared.
5. No new comments or diagnostics were added that would violate house idioms.
src/devices/dev_mc146818.c:529 DEFECT The diff misses the third site named in the issue (line 529). Fix: remove the overwriting of register 63 at line 529 as well.
```

## WHAT TO RETURN

1. For EACH review finding, one line: `ACCEPT` or `REJECT`, and why, citing the code shown.  A suggestion that uses a
   function, macro or field that appears nowhere in this packet does not exist in HEAD: reject it or replace it with an
   idiom the packet shows.
2. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code that shows it>`.
3. If YES: EXACTLY ONE fenced ```json block -- the COMPLETE corrected edit list (not a delta), applying to the HEAD text
   above: [{"file": "src/...", "old": "<exact HEAD text, occurring EXACTLY ONCE in that file>", "new": "<replacement>",
   "why": "<one line>"}].  JSON escapes (\t, \n); tabs stay tabs; lines within 79 columns; a new comment carries
   `/* #NNN: ... */`.  Never an empty list and never comment-only edits for a defect in behaviour.  If every finding is
   rejected, return the previous edits unchanged.
4. After the block: what the fix deliberately does not change.

End with two lines: `REVISION_MC146818REG63: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_MC146818REG63: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
