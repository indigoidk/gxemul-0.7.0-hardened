# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `mc146818reg63` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `mc146818reg63`, state `open`)

**title:** devices/dev_mc146818.c:mc146818_update_time -- DEC register 63 (NVRAM) is overwritten with the year on every time read -- WRONG-RESULT (NVRAM byte clobbered)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T56 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-34).  Source URLs: https://github.com/rpajarola/gxemul/commit/871e551340226bdc3ed3c3b1c9e0e1fea824aa70.  Our site at de8c7547: src/devices/dev_mc146818.c:258, :272, :529.  Portable fix: yes -- port rpajarola 871e551.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- src/devices/dev_mc146818.c:258

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_mc146818.c b/src/devices/dev_mc146818.c
index ec89e02b..fe9560c8 100644
--- a/src/devices/dev_mc146818.c
+++ b/src/devices/dev_mc146818.c
@@ -251,11 +251,6 @@ static void mc146818_update_time(struct mc_data *d)
 		 */
 		d->reg[4 * MC_YEAR] = 72;
 
-		/*
-		 *  Linux on DECstation stores the year in register 63,
-		 *  but no other DECstation OS does? (Hm.)
-		 */
-		d->reg[4 * 63]  = tmp->tm_year - 100;
 		break;
 	}
 
@@ -268,9 +263,6 @@ static void mc146818_update_time(struct mc_data *d)
 		d->reg[4 * MC_MONTH] = to_bcd(d->reg[4 * MC_MONTH]);
 		d->reg[4 * MC_YEAR]  = to_bcd(d->reg[4 * MC_YEAR]);
 
-		/*  Used by Linux on DECstation: (Hm)  */
-		d->reg[4 * 63]       = to_bcd(d->reg[4 * 63]);
-
 		/*  Used on SGI:  */
 		d->reg[4 * 72]       = to_bcd(d->reg[4 * 72]);
 	}
```

## Every edited function, after the fix

### `src/devices/dev_mc146818.c` -- post-edit lines 185-269 (`+` marks a line the diff added or the point of a deletion)

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
  254|+ 		break;
  255|  	}
  256|  
  257|  	if (d->use_bcd) {
  258|  		d->reg[4 * MC_SEC]   = to_bcd(d->reg[4 * MC_SEC]);
  259|  		d->reg[4 * MC_MIN]   = to_bcd(d->reg[4 * MC_MIN]);
  260|  		d->reg[4 * MC_HOUR]  = to_bcd(d->reg[4 * MC_HOUR]);
  261|  		d->reg[4 * MC_DOW]   = to_bcd(d->reg[4 * MC_DOW]);
  262|  		d->reg[4 * MC_DOM]   = to_bcd(d->reg[4 * MC_DOM]);
  263|  		d->reg[4 * MC_MONTH] = to_bcd(d->reg[4 * MC_MONTH]);
  264|  		d->reg[4 * MC_YEAR]  = to_bcd(d->reg[4 * MC_YEAR]);
  265|  
  266|+ 		/*  Used on SGI:  */
  267|  		d->reg[4 * 72]       = to_bcd(d->reg[4 * 72]);
  268|  	}
  269|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_MC146818REG63: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_MC146818REG63: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
