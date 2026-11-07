# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `fbsignalcoverage` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `fbsignalcoverage`, state `open`)

**title:** wall-time coverage does not establish callback progress

**state_note (head):** GOVERNING TEXT (from the dispositions file, cut at 400 characters): hbundle_regress2:F2 | draft said UNSETTLED; no ID pending a serviced-SIGALRM count | should be NEW MED fbsignalcoverage “wall-time coverage does not establish callback progress” | `src/core/timer.c:281–289` caps callbacks per serviced handler invocation; `:327–337` requests a signal interval without establishing a minimum serviced count. `regress/fbpending_witness.py:719,725–736` accepts...

**The drafter's own reading:** STILL PRESENT: YES -- src/core/timer.c:281 shows `int budget = TIMER_MAX_CATCHUP;` capping callbacks, and 327-329 calculates the interval solely from `timer_freq`.

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/core/timer.c b/src/core/timer.c
index 6ae3acbd..76493381 100644
--- a/src/core/timer.c
+++ b/src/core/timer.c
@@ -278,6 +278,7 @@ static void timer_tick(int signal_nr)
 		 *  pre-existing and filed; it is named here so this comment is not read as
 		 *  covering it.
 		 */
+		/* #fbsignalcoverage: enforce a minimum callback serviced count */
 		int budget = TIMER_MAX_CATCHUP;
 
 		while (timer_current_time >= timer->next_tick_at) {
```

## Every edited function, after the fix

### `src/core/timer.c` -- post-edit lines 219-300 (`+` marks a line the diff added or the point of a deletion)

```c
  219|  static void timer_tick(int signal_nr)
  220|  {
  221|  	struct timer *timer = first_timer;
  222|  	struct timeval tv;
  223|  
  224|  	timer_current_time += timer_current_time_step;
  225|  
  226|  	if ((--timer_countdown_to_next_gettimeofday) < 0) {
  227|  		gettimeofday(&tv, NULL);
  228|  		tv.tv_sec -= timer_start_tv.tv_sec;
  229|  		tv.tv_usec -= timer_start_tv.tv_usec;
  230|  		if (tv.tv_usec < 0) {
  231|  			tv.tv_usec += 1000000;
  232|  			tv.tv_sec --;
  233|  		}
  234|  
  235|  #ifdef TIMER_DEBUG
  236|  		/*  For debugging/testing:  */
  237|  		{
  238|  			double diff = tv.tv_usec * 0.000001 + tv.tv_sec
  239|  			    - timer_current_time;
  240|  			printf("timer: lagging behind %f seconds\n", diff);
  241|  		}
  242|  #endif
  243|  
  244|  		/*  Get exponentially closer to the real time, instead of
  245|  		    just changing to it directly:  */
  246|  		timer_current_time = ( (tv.tv_usec * 0.000001 + tv.tv_sec) +
  247|  		    timer_current_time ) / 2;
  248|  
  249|  		timer_countdown_to_next_gettimeofday = (int64_t) (timer_freq *
  250|  		    SECONDS_BETWEEN_GETTIMEOFDAY_SYNCH);
  251|  	}
  252|  
  253|  	while (timer != NULL) {
  254|  		/*
  255|  		 *  #428: bound the catch-up, and RETAIN the backlog.
  256|  		 *
  257|  		 *  This loop is the emulator's whole delivery mechanism for any timer faster
  258|  		 *  than TIMER_BASE_FREQUENCY, so it must not be turned into "drop what was
  259|  		 *  missed": measured, that caps every timer at 65 Hz and a 100 Hz timer runs
  260|  		 *  at 0.65 of real time with no burst at all.  Leaving it unbounded is the
  261|  		 *  measured defect -- 20.6 million iterations in one signal after half a
  262|  		 *  second of lag, and an interval of zero never advances at all.
  263|  		 *
  264|  		 *  So: stop after TIMER_MAX_CATCHUP ticks for this timer in this signal and
  265|  		 *  leave next_tick_at where it is.  A RECOVERABLE burst then loses nothing but
  266|  		 *  its promptness -- the remainder is delivered by the signals that follow.
  267|  		 *
  268|  		 *  Said precisely, because the first draft of this comment was not: that holds
  269|  		 *  for a backlog the timer's own rate can pay off, i.e. below
  270|  		 *  TIMER_MAX_CATCHUP * TIMER_BASE_FREQUENCY = 68,157,440 Hz.  Above it the debt
  271|  		 *  grows every signal and is never repaid; see timer.h, where the gap between
  272|  		 *  that figure and the domain ceiling is recorded and filed.
  273|  		 *
  274|  		 *  The hit is recorded for timer_stop() to report.  NOTHING IN THIS FILE PRINTS
  275|  		 *  FROM THE HANDLER -- which is a claim about timer.c and NOT about the handler
  276|  		 *  as a whole: a review seat traced dev_sh4.c's sh4_timer_tick(), a callback this
  277|  		 *  loop invokes, calling fatal() and exit(1) from inside SIGALRM.  That is
  278|  		 *  pre-existing and filed; it is named here so this comment is not read as
  279|  		 *  covering it.
  280|  		 */
  281|+ 		/* #fbsignalcoverage: enforce a minimum callback serviced count */
  282|  		int budget = TIMER_MAX_CATCHUP;
  283|  
  284|  		while (timer_current_time >= timer->next_tick_at) {
  285|  			timer->timer_tick(timer, timer->extra);
  286|  			timer->next_tick_at += timer->interval;
  287|  
  288|  			if (--budget <= 0) {
  289|  				timer_catchup_hit = 1;
  290|  				break;
  291|  			}
  292|  		}
  293|  
  294|  		timer = timer->next;
  295|  	}
  296|  
  297|  #ifdef TEST
  298|  	printf("T"); fflush(stdout);
  299|  #endif
  300|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_FBSIGNALCOVERAGE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_FBSIGNALCOVERAGE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
