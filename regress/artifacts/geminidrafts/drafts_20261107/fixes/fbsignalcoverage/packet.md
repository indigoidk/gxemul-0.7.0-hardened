# GXemul hardened fork -- DRAFT A FIX for one filed issue, `fbsignalcoverage` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `fbsignalcoverage`, state `open`, severity `MED`)

**title:** wall-time coverage does not establish callback progress

**state_note (head):**

GOVERNING TEXT (from the dispositions file, cut at 400 characters): hbundle_regress2:F2 | draft said UNSETTLED; no ID pending a serviced-SIGALRM count | should be NEW MED fbsignalcoverage “wall-time coverage does not establish callback progress” | `src/core/timer.c:281–289` caps callbacks per serviced handler invocation; `:327–337` requests a signal interval without establishing a minimum serviced count. `regress/fbpending_witness.py:719,725–736` accepts...

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Enforce a minimum callback serviced count rather than relying solely on wall-time

## The code at the cited lines

### `src/core/timer.c` around the row's cited line 281 (HEAD 2d25df65, lines 236-326)

```c
  236| 		/*  For debugging/testing:  */
  237| 		{
  238| 			double diff = tv.tv_usec * 0.000001 + tv.tv_sec
  239| 			    - timer_current_time;
  240| 			printf("timer: lagging behind %f seconds\n", diff);
  241| 		}
  242| #endif
  243| 
  244| 		/*  Get exponentially closer to the real time, instead of
  245| 		    just changing to it directly:  */
  246| 		timer_current_time = ( (tv.tv_usec * 0.000001 + tv.tv_sec) +
  247| 		    timer_current_time ) / 2;
  248| 
  249| 		timer_countdown_to_next_gettimeofday = (int64_t) (timer_freq *
  250| 		    SECONDS_BETWEEN_GETTIMEOFDAY_SYNCH);
  251| 	}
  252| 
  253| 	while (timer != NULL) {
  254| 		/*
  255| 		 *  #428: bound the catch-up, and RETAIN the backlog.
  256| 		 *
  257| 		 *  This loop is the emulator's whole delivery mechanism for any timer faster
  258| 		 *  than TIMER_BASE_FREQUENCY, so it must not be turned into "drop what was
  259| 		 *  missed": measured, that caps every timer at 65 Hz and a 100 Hz timer runs
  260| 		 *  at 0.65 of real time with no burst at all.  Leaving it unbounded is the
  261| 		 *  measured defect -- 20.6 million iterations in one signal after half a
  262| 		 *  second of lag, and an interval of zero never advances at all.
  263| 		 *
  264| 		 *  So: stop after TIMER_MAX_CATCHUP ticks for this timer in this signal and
  265| 		 *  leave next_tick_at where it is.  A RECOVERABLE burst then loses nothing but
  266| 		 *  its promptness -- the remainder is delivered by the signals that follow.
  267| 		 *
  268| 		 *  Said precisely, because the first draft of this comment was not: that holds
  269| 		 *  for a backlog the timer's own rate can pay off, i.e. below
  270| 		 *  TIMER_MAX_CATCHUP * TIMER_BASE_FREQUENCY = 68,157,440 Hz.  Above it the debt
  271| 		 *  grows every signal and is never repaid; see timer.h, where the gap between
  272| 		 *  that figure and the domain ceiling is recorded and filed.
  273| 		 *
  274| 		 *  The hit is recorded for timer_stop() to report.  NOTHING IN THIS FILE PRINTS
  275| 		 *  FROM THE HANDLER -- which is a claim about timer.c and NOT about the handler
  276| 		 *  as a whole: a review seat traced dev_sh4.c's sh4_timer_tick(), a callback this
  277| 		 *  loop invokes, calling fatal() and exit(1) from inside SIGALRM.  That is
  278| 		 *  pre-existing and filed; it is named here so this comment is not read as
  279| 		 *  covering it.
  280| 		 */
  281| 		int budget = TIMER_MAX_CATCHUP;
  282| 
  283| 		while (timer_current_time >= timer->next_tick_at) {
  284| 			timer->timer_tick(timer, timer->extra);
  285| 			timer->next_tick_at += timer->interval;
  286| 
  287| 			if (--budget <= 0) {
  288| 				timer_catchup_hit = 1;
  289| 				break;
  290| 			}
  291| 		}
  292| 
  293| 		timer = timer->next;
  294| 	}
  295| 
  296| #ifdef TEST
  297| 	printf("T"); fflush(stdout);
  298| #endif
  299| }
  300| 
  301| 
  302| /*
  303|  *  timer_start():
  304|  *
  305|  *  Set the interval timer to timer_freq Hz, and install the signal handler.
  306|  */
  307| void timer_start(void)
  308| {
  309| 	struct timer *timer = first_timer;
  310| 	struct itimerval val;
  311| 	struct sigaction saction;
  312| 
  313| 	if (timer_is_running)
  314| 		return;
  315| 
  316| 	timer_is_running = 1;
  317| 
  318| 	gettimeofday(&timer_start_tv, NULL);
  319| 	timer_current_time = 0.0;
  320| 
  321| 	/*  Reset all timers:  */
  322| 	while (timer != NULL) {
  323| 		timer->next_tick_at = timer->interval;
  324| 		timer = timer->next;
  325| 	}
  326| 	val.it_interval.tv_sec = 0;
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

End with one line: `FIXDRAFT_FBSIGNALCOVERAGE: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
