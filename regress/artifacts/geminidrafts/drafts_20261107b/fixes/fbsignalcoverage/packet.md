# GXemul hardened fork -- DRAFT A FIX for one filed issue, `fbsignalcoverage` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `fbsignalcoverage`, state `open`, severity `MED`)

**title:** wall-time coverage does not establish callback progress

**state_note (head):**

GOVERNING TEXT (from the dispositions file, cut at 400 characters): hbundle_regress2:F2 | draft said UNSETTLED; no ID pending a serviced-SIGALRM count | should be NEW MED fbsignalcoverage “wall-time coverage does not establish callback progress” | `src/core/timer.c:281–289` caps callbacks per serviced handler invocation; `:327–337` requests a signal interval without establishing a minimum serviced count. `regress/fbpending_witness.py:719,725–736` accepts...

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Enforce a minimum callback serviced count rather than relying solely on wall-time

## The code at the cited lines

### `src/core/timer.c` around the row's cited line 281 (HEAD 8d9df658, lines 161-401)

```c
  161| 		cur = cur->next;
  162| 	}
  163| 
  164| 	if (cur == t) {
  165| 		if (prev == NULL)
  166| 			first_timer = cur->next;
  167| 		else
  168| 			prev->next = cur->next;
  169| 		free(cur);
  170| 	} else {
  171| 		fprintf(stderr, "attempt to remove timer %p which "
  172| 		    "doesn't exist. aborting\n", t);
  173| 		exit(1);
  174| 	}
  175| }
  176| 
  177| 
  178| /*
  179|  *  timer_update_frequency():
  180|  *
  181|  *  Changes the frequency of an existing timer.
  182|  */
  183| void timer_update_frequency(struct timer *t, double new_freq)
  184| {
  185| 	int clamped;
  186| 
  187| 	/*
  188| 	 *  #427/#429: CLAMP FIRST, THEN compare, THEN store.
  189| 	 *
  190| 	 *  The order is load-bearing and the shipped order was wrong twice over.  The old
  191| 	 *  code stored the RAW value into t->freq and clamped only the local, so t->freq
  192| 	 *  named a rate the timer did not run at.  Clamping at the store alone is not a
  193| 	 *  repair but a REGRESSION: the early-out below would then compare a CLAMPED record
  194| 	 *  against a RAW request, and five identical absurd writes would reset next_tick_at
  195| 	 *  five times instead of once -- measured, on five of six input classes.  Clamping
  196| 	 *  above the comparison makes a repeated request idempotent again, as it is today for
  197| 	 *  ordinary values.
  198| 	 */
  199| 	new_freq = timer_clamp_freq(new_freq, &clamped);
  200| 	if (clamped && t->freq != new_freq)
  201| 		fatal("[ timer: requested rate is above %f Hz; clamped ]\n",
  202| 		    (double) TIMER_MAX_FREQUENCY);
  203| 
  204| 	if (t->freq == new_freq)
  205| 		return;
  206| 
  207| 	t->freq = new_freq;
  208| 
  209| 	t->interval = 1.0 / new_freq;
  210| 	t->next_tick_at = timer_current_time + t->interval;
  211| }
  212| 
  213| 
  214| /*
  215|  *  timer_tick():
  216|  *
  217|  *  Timer tick handler. This is where the interesting stuff happens.
  218|  */
  219| static void timer_tick(int signal_nr)
  220| {
  221| 	struct timer *timer = first_timer;
  222| 	struct timeval tv;
  223| 
  224| 	timer_current_time += timer_current_time_step;
  225| 
  226| 	if ((--timer_countdown_to_next_gettimeofday) < 0) {
  227| 		gettimeofday(&tv, NULL);
  228| 		tv.tv_sec -= timer_start_tv.tv_sec;
  229| 		tv.tv_usec -= timer_start_tv.tv_usec;
  230| 		if (tv.tv_usec < 0) {
  231| 			tv.tv_usec += 1000000;
  232| 			tv.tv_sec --;
  233| 		}
  234| 
  235| #ifdef TIMER_DEBUG
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
  327| 	val.it_interval.tv_usec = (int) (1000000.0 / timer_freq);
  328| 	val.it_value.tv_sec = 0;
  329| 	val.it_value.tv_usec = (int) (1000000.0 / timer_freq);
  330| 
  331| 	memset(&saction, 0, sizeof(saction));
  332| 	saction.sa_handler = timer_tick;
  333| 	saction.sa_flags = SA_RESTART;
  334| 
  335| 	sigaction(SIGALRM, &saction, NULL);
  336| 
  337| 	setitimer(ITIMER_REAL, &val, NULL);
  338| }
  339| 
  340| 
  341| /*
  342|  *  timer_stop():
  343|  *
  344|  *  Deinstall the signal handler, and disable the interval timer.
  345|  */
  346| void timer_stop(void)
  347| {
  348| 	struct itimerval val;
  349| 	struct sigaction saction;
  350| 
  351| 	if (!timer_is_running)
  352| 		return;
  353| 
  354| 	timer_is_running = 0;
  355| 
  356| 	val.it_interval.tv_sec = 0;
  357| 	val.it_interval.tv_usec = 0;
  358| 	val.it_value.tv_sec = 0;
  359| 	val.it_value.tv_usec = 0;
  360| 
  361| 	setitimer(ITIMER_REAL, &val, NULL);
  362| 
  363| 	memset(&saction, 0, sizeof(saction));
  364| 	saction.sa_handler = NULL;
  365| 
  366| 	sigaction(SIGALRM, &saction, NULL);
  367| 
  368| 	/*  #428: the handler cannot say this safely, so it is said here.  */
  369| 	if (timer_catchup_hit) {
  370| 		timer_catchup_hit = 0;
  371| 		fatal("[ timer: a timer asked for more ticks than a host period can "
  372| 		    "deliver; the backlog was spread over later periods ]\n");
  373| 	}
  374| }
  375| 
  376| 
  377| #ifdef TEST
  378| static void timer_tick_test(struct timer *t, void *extra)
  379| {
  380| 	printf((char *) extra); fflush(stdout);
  381| }
  382| #endif
  383| 
  384| 
  385| /*
  386|  *  timer_init():
  387|  *
  388|  *  Initialize the timer framework.
  389|  */
  390| void timer_init(void)
  391| {
  392| 	first_timer = NULL;
  393| 	timer_current_time = 0.0;
  394| 	timer_is_running = 0;
  395| 	timer_countdown_to_next_gettimeofday = 0;
  396| 
  397| 	timer_freq = TIMER_BASE_FREQUENCY;
  398| 	timer_current_time_step = 1.0 / timer_freq;
  399| 
  400| #ifdef TEST
  401| 	timer_add(0.5, timer_tick_test, "X");
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

End with one line: `FIXDRAFT_FBSIGNALCOVERAGE: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.

## YOUR PREVIOUS DRAFT SAID `STILL PRESENT: UNSETTLED` -- here is what it said was missing

```text
Review of claims:
- Claim: "wall-time coverage does not establish callback progress" -> UNSETTLED: Requires dynamic tracing or execution logs not present in the provided text to verify progress stalling.
- Claim: "`src/core/timer.c:281–289` caps callbacks per serviced handler invocation" -> BROKEN: The `int budget = TIMER_MAX_CATCHUP;` declaration at line 281 is inside the `while (timer != NULL)` loop, meaning it caps callbacks per *timer* per handler invocation, not globally per invocation.
- Claim: "`:327–337` requests a signal interval without establishing a minimum serviced count" -> HOLDS: Lines 327-330 set `it_interval` purely based on `timer_freq` and wall-time calculations, with no logic enforcing a minimum callback count.
STILL PRESENT: UNSETTLED -- missing definition or macro for the minimum callback serviced count to enforce, or how to calculate it (would need `timer.h` or the explicit requirement).
What the fix deliberately does NOT change: It cannot change the interval setup or the budget logic without the exact macro or threshold to enforce a minimum count.
What could not be settled: The definition of the "serviced-SIGALRM count" minimum, as it is not present in the provided source text or available macros.
FIXDRAFT_FBSIGNALCOVERAGE: UNSETTLED PRESENT, 0 EDITS
```

## What you said was missing, from HEAD

### `src/core/timer.c` lines 37-53 (where HEAD defines `timer`)

```c
   37| 
   38| #include "misc.h"
   39| #include "timer.h"
   40| 
   41| 
   42| /*  #define TEST  */
   43| 
   44| 
   45| struct timer {
   46| 	struct timer	*next;
   47| 
   48| 	double		freq;
   49| 	void		(*timer_tick)(struct timer *timer, void *extra);
   50| 	void		*extra;
   51| 
   52| 	double		interval;
   53| 	double		next_tick_at;
```

### `src/core/timer.c` lines 114-130 (where HEAD defines `timer`)

```c
  114| 
  115| /*
  116|  *  timer_add():
  117|  *
  118|  *  Adds a virtual timer to the list of timers.
  119|  *
  120|  *  Return value is a pointer to a timer struct.
  121|  */
  122| struct timer *timer_add(double freq, void (*timer_tick)(struct timer *timer,
  123| 	void *extra), void *extra)
  124| {
  125| 	struct timer *newtimer;
  126| 	int clamped;
  127| 
  128| 	CHECK_ALLOCATION(newtimer = (struct timer *) malloc(sizeof(struct timer)));
  129| 
  130| 	/*  #427: clamp before anything is stored, so freq and interval agree.  */
```

### `src/include/timer.h` lines 74-90 (where HEAD defines `TIMER_MAX_CATCHUP`)

```c
   74|  *  is simply untrue -- measured, a timer at the domain ceiling sits 0.9683 s behind after
   75|  *  one simulated second and falls further every period.  The domain admits 32x more than
   76|  *  the cap can ever serve.  That gap is real, it is not made worse by this change (the old
   77|  *  code spun 33 million iterations per signal at the same rate), and closing it is a policy
   78|  *  question filed rather than answered here.
   79|  */
   80| #define	TIMER_MIN_FREQUENCY	0.00000001	/*  Hz  */
   81| #define	TIMER_MAX_FREQUENCY	2147483647.0	/*  Hz; INT_MAX, see above  */
   82| #define	TIMER_MAX_CATCHUP	1048576		/*  ticks per timer per signal  */
   83| 
   84| struct timer *timer_add(double freq, void (*timer_tick)(struct timer *timer,
   85| 	void *extra), void *extra);
   86| void timer_remove(struct timer *t);
   87| 
   88| void timer_update_frequency(struct timer *t, double new_freq);
   89| 
   90| void timer_start(void);
```


Now draft the fix, or -- if it still cannot be written from what is shown -- say `STILL PRESENT: UNSETTLED` and name the
exact definition or function still missing.  A name that appears in no section of this packet does not exist in HEAD; do
not use it.  Do not return an empty edit list, and do not return edits that change only comments.
