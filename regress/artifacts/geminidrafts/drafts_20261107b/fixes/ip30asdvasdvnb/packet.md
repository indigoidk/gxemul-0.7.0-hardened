# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ip30asdvasdvnb` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at lines the coordinator LOCATED from names the row uses (the row cites none) (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ip30asdvasdvnb`, state `open`, severity `LOW`)

**title:** dev_sgi_ip30.c DEVICE_ACCESS(sgi_ip30_2) case 0x114+0x40*(12-8) carries an UNLATCHED guest-drivable fatal() whose message is a keyboard mash (asdvasdvnb), on an arm that is actually implemented and returns the documented 0x80000000 alive value

**state_note (head):**

FILED 2026-09-17 by the #531 pass-2 grok seat; every element verified here before filing.  NOT one of #531's four sites -- it carries no abort() and no exit(, so it kills nothing.  The round-scope rule takes ONE site, and a second joins only in the SAME semantic class; a host kill and a log flood are different classes, which is why this is filed rather than folded in.  UPSTREAM RESIDUE, checked against HEAD rather than assumed: present before #531 and never touched by the fork.  TWO defects in one line -- UNLATCHED (every guest read prints; floodclass already records guest-drivable log floods as a CLASS, and the house idiom is N=1 per device instance with an unqualified '(once)' marker) and a MEANINGLESS MESSAGE that tells a reader nothing.  DISPOSITION when it is taken: member 1 DELETE, not member 3.  The arm computes the right value and refuses nothing, so there is no event to announce, and a bounded announce would ship a wrong record in product code -- exactly what the footbridge +0x188 case established.  WITNESS when it is taken: a rung-3 probe reading that offset and counting emissions.  The #531 probe's vehicle already reaches this device, so the cost is one session, not a new rig.  *** WARRANT CORRECTED 2026-09-18 after the kimi seat named it in the §F2 adjudication: 'a host kill and a log flood are different classes' KEYS ON IMPACT, which is a CORRELATE of the defect -- committed in the very sentence excluding a row, during a session spent cataloguing that error. ***  The reopening rule's test is its own parenthetical, SO ONE FIX DESIGN COVERS BOTH.  The filing stands and is stronger than the reason given: (1) NOT the same device -- sgi_ip30_2 is a separate DEVICE_ACCESS and registration, and sharing a .c file is not sharing a device; (2) NOT one fix design -- #531 de-fatalises, while this arm computes the right value and needs member 1 DELETE; (3) NOT the same detector -- no row reaches that offset, so it needs a NEW ORACLE, which the rule excludes outright.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- simply delete the meaningless and unlatched fatal() string on a perfectly functional arm

## The code at the cited lines

### `src/devices/dev_sgi_ip30.c` around line 103 -- LOCATED BY THE COORDINATOR from the name `abort` the row uses (the row cites no line; check this is the defect's site) (HEAD 8d9df658, lines 1-223)

```c
    1| /*
    2|  *  Copyright (C) 2004-2018  Anders Gavare.  All rights reserved.
    3|  *
    4|  *  Redistribution and use in source and binary forms, with or without
    5|  *  modification, are permitted provided that the following conditions are met:
    6|  *
    7|  *  1. Redistributions of source code must retain the above copyright
    8|  *     notice, this list of conditions and the following disclaimer.
    9|  *  2. Redistributions in binary form must reproduce the above copyright  
   10|  *     notice, this list of conditions and the following disclaimer in the 
   11|  *     documentation and/or other materials provided with the distribution.
   12|  *  3. The name of the author may not be used to endorse or promote products
   13|  *     derived from this software without specific prior written permission.
   14|  *
   15|  *  THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
   16|  *  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
   17|  *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
   18|  *  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE   
   19|  *  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
   20|  *  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
   21|  *  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
   22|  *  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
   23|  *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
   24|  *  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
   25|  *  SUCH DAMAGE.
   26|  *   
   27|  *
   28|  *  COMMENT: SGI IP30 ("Octane") stuff
   29|  *
   30|  *  NOTE/TODO: This is just comprised of hardcoded guesses so far. (Ugly.)
   31|  */
   32| 
   33| #include <stdio.h>
   34| #include <stdlib.h>
   35| #include <string.h>
   36| 
   37| #include "cpu.h"
   38| #include "device.h"
   39| #include "machine.h"
   40| #include "memory.h"
   41| #include "misc.h"
   42| 
   43| 
   44| #define	DEV_SGI_IP30_LENGTH		0x80000
   45| 
   46| /*
   47|  *  #531: warn-once latches, ONE BIT PER DISTINCT MESSAGE.  The struct is
   48|  *  memset(0) at DEVINIT (as dev_pcc2.c and dev_wdc.c do), so these start clear.
   49|  *
   50|  *  SIX announce paths share TWO bits, and that is deliberate: IP30_W_ISR covers
   51|  *  FIVE (0x10020 write and read, 0x10028 write and read, 0x10030 write), which
   52|  *  all print the SAME string byte for byte.
   53|  *
   54|  *  THE INVARIANT IS THAT LATCH GRANULARITY MATCHES THE MARKER'S QUALIFICATION.
   55|  *  Both messages end in an UNQUALIFIED "(once)", which claims exactly one
   56|  *  emission per device instance -- so one bit apiece is what makes the marker
   57|  *  true.  Reporting each offset separately would be a different promise: it
   58|  *  would need the qualified spelling this tree also uses ("(once per offset per
   59|  *  direction)") and five bits on the ISR side.  Do not add bits without
   60|  *  changing the strings; do not qualify the strings without adding bits.
   61|  *
   62|  *  TWO BITS RATHER THAN ONE, AND THE REASON IS MEASURABLE: a single shared bit
   63|  *  would let an ordinary guest write to Set-ISR silence the TIMER diagnostic
   64|  *  forever, because the first ISR-side announce would consume it.  The two are
   65|  *  different messages reached by unrelated guest actions, and must latch apart.
   66|  */
   67| #define	IP30_W_TICK	(1 << 0)	/*  #531: DEVICE_TICK delivery  */
   68| #define	IP30_W_ISR	(1 << 1)	/*  #531: ISR-side rewrite  */
   69| 
   70| struct sgi_ip30_data {
   71| 	/*  ip30:  */
   72| 	uint64_t                imask0;         /*  0x10000  */
   73| 	int                     warned;         /*  #531: IP30_W_* latches  */
   74| 	uint64_t                reg_0x10018;
   75| 	uint64_t                isr;            /*  0x10030  */
   76| 	uint64_t                reg_0x20000;
   77| 	uint64_t                reg_0x30000;
   78| 
   79| 	/*  ip30_2:  */
   80| 	uint64_t                reg_0x0029c;
   81| 
   82| 	/*  ip30_3:  */
   83| 	uint64_t                reg_0x00284;
   84| 
   85| 	/*  ip30_4:  */
   86| 	uint64_t                reg_0x000b0;
   87| 
   88| 	/*  ip30_5:  */
   89| 	uint64_t                reg_0x00000;
   90| };
   91| 
   92| 
   93| DEVICE_TICK(sgi_ip30)
   94| {
   95| 	struct sgi_ip30_data *d = (struct sgi_ip30_data *) extra;
   96| 
   97| 	d->reg_0x20000 += 1000;
   98| 
   99| 	if (d->imask0 & ((int64_t)1<<50)) {
  100| 		/*  TODO: Only interrupt if reg 0x20000 (the counter)
  101| 			has passed the compare (0x30000).  */
  102| 		/*
  103| 		 *  #531: was fatal() + abort(), and a guest reached it by
  104| 		 *  ARMING imask0 BIT 50 AND WAITING -- one `sd' plus one
  105| 		 *  step, measured (row `tick 50').  Interrupt DELIVERY is a
  106| 		 *  whole subsystem this device does not have, so the host
  107| 		 *  stops dying and the timer interrupt is simply not
  108| 		 *  delivered.  The counter update above still runs.
  109| 		 *
  110| 		 *  *** AND NO ROW PINS THAT, WHICH THIS COMMENT HAS NOW CLAIMED
  111| 		 *  TWICE AND BEEN WRONG BOTH TIMES.  MEASURED 2026-09-18. ***
  112| 		 *  It first credited `tick 49' (the grok seat caught that: the
  113| 		 *  row only scored `alive').  The correction moved the credit to
  114| 		 *  `acc 20000' -- and the opus5 F2 seat then MEASURED that row
  115| 		 *  green with this very increment deleted (`MH_nocounter',
  116| 		 *  27/27).  Its oracle accepts `(readback - 0x1234) % 1000 == 0'
  117| 		 *  and **N = 0 IS ADMISSIBLE**, so a counter that never moves
  118| 		 *  reads back exactly 0x1234, residue 0, and the row passes.
  119| 		 *
  120| 		 *  A CORRECTION IS NOT SAFER THAN THE THING IT CORRECTS, AND
  121| 		 *  THIS COMMENT HAS NOW PROVED IT THREE TIMES.  The third error
  122| 		 *  was in the sentence that replaced this one: it graded the
  123| 		 *  unpinned counter an L3 DE-ESCALATION OBLIGATION.  The fable5
  124| 		 *  adjudicator refuted that, and the refutation is two lines up
  125| 		 *  in this very function --
  126| 		 *
  127| 		 *      d->reg_0x20000 += 1000;              <- UNCONDITIONAL
  128| 		 *      if (d->imask0 & ((int64_t)1<<50)) {  <- the de-fatalised
  129| 		 *                                              predicate
  130| 		 *
  131| 		 *  The counter runs on EVERY tick regardless of bit 50.  The fix
  132| 		 *  neither introduces it nor gates it, so deleting it mutates
  133| 		 *  PRE-EXISTING, FIX-INDEPENDENT behaviour: COVERAGE DEBT, not a
  134| 		 *  clause-(d) obligation.  And the de-escalation ACCEPT SIDE of
  135| 		 *  the predicate that WAS de-fatalised is pinned, by `tick 50'
  136| 		 *  (alive) plus `tick 50 txt' (announce).
  137| 		 *
  138| 		 *  SO THE HONEST STATE IS NARROWER THAN THE LAST TWO SENTENCES
  139| 		 *  CLAIMED: no row observes this counter, that is optional
  140| 		 *  coverage debt, and the round's accept-side claim is TRUE.
  141| 		 *  Each correction here arrived with more confidence than the
  142| 		 *  one before and two of the three were wrong -- which is the
  143| 		 *  rule about corrections earning a SECOND reading, failed
  144| 		 *  three times on seven lines of comment.
  145| 		 */
  146| 		if (!(d->warned & IP30_W_TICK)) {
  147| 			d->warned |= IP30_W_TICK;
  148| 			fatal("[ sgi_ip30: timer interrupt delivery not "
  149| 			    "implemented  (once) ]\n");
  150| 		}
  151| //		cpu_interrupt(cpu, 8+1 + 50);
  152| 	}
  153| }
  154| 
  155| 
  156| DEVICE_ACCESS(sgi_ip30)
  157| {
  158| 	struct sgi_ip30_data *d = (struct sgi_ip30_data *) extra;
  159| 	uint64_t idata = 0, odata = 0;
  160| 
  161| 	if (writeflag == MEM_WRITE)
  162| 		idata = memory_readmax64(cpu, data, len);
  163| 
  164| 	switch (relative_addr) {
  165| 
  166| 	case 0x20:
  167| 		/*  Memory bank configuration:  */
  168| 		odata = 0x80010000ULL;
  169| 		break;
  170| 
  171| 	case 0x10000:	/*  Interrupt mask register 0:  */
  172| 		if (writeflag == MEM_WRITE) {
  173| 			d->imask0 = idata;
  174| 		} else {
  175| 			odata = d->imask0;
  176| 		}
  177| 		break;
  178| 
  179| 	case 0x10018:
  180| 		/*
  181| 		 *  If this is not implemented, the IP30 PROM complains during
  182| 		 *  bootup:
  183| 		 *
  184| 		 *           *FAILED*
  185| 		 *    Address: 0xffffffffaff10018, Expected:
  186| 		 *        0x0000000000000001, Received: 0x0000000000000000
  187| 		 */
  188| 		if (writeflag == MEM_WRITE) {
  189| 			d->reg_0x10018 = idata;
  190| 		} else {
  191| 			odata = d->reg_0x10018;
  192| 		}
  193| 		break;
  194| 
  195| 	case 0x10020:	/*  Set ISR (heart.h: set_isr, WRITE-side)  */
  196| 		/*
  197| 		 *  #531: this arm had NO writeflag test and ran the store
  198| 		 *  FIRST, so a guest LOAD zeroed the ISR and then killed the
  199| 		 *  host -- `idata' is 0 on a read.  Rows `kill 20 rd' and
  200| 		 *  `isr keep' pin both halves.
  201| 		 */
  202| 		if (writeflag == MEM_WRITE) {
  203| 			d->isr = idata;
  204| 			if (!(d->warned & IP30_W_ISR)) {
  205| 				d->warned |= IP30_W_ISR;
  206| 				fatal("[ sgi_ip30: interrupt-status rewrite "
  207| 				    "not implemented  (once) ]\n");
  208| 			}
  209| //		cpu_interrupt(cpu, 8);
  210| 		} else {
  211| 			/*
  212| 			 *  #531: MEMBER 2 -- SILENT DECLINE.  Adopted on the
  213| 			 *  fable5 adjudication of 2026-09-18, and it replaces an
  214| 			 *  announce that was WRONG IN PRODUCT CODE TWO WAYS.
  215| 			 *
  216| 			 *  (1) IT SAID THE WRONG THING.  All five ISR sites print
  217| 			 *  one byte-identical string, "interrupt-status rewrite
  218| 			 *  not implemented" -- and a READ is not a rewrite.
  219| 			 *
  220| 			 *  (2) IT STOLE THE BIT.  One shared IP30_W_ISR latch
  221| 			 *  serves every ISR path, so a single BENIGN guest read
  222| 			 *  of this write-side register consumed the only announce
  223| 			 *  there is and silenced the genuine write-side
```

## The data structures those files define (every field that exists)

### `src/devices/dev_sgi_ip30.c` -- `struct sgi_ip30_data {` (HEAD lines 70-90)

```c
   70| struct sgi_ip30_data {
   71| 	/*  ip30:  */
   72| 	uint64_t                imask0;         /*  0x10000  */
   73| 	int                     warned;         /*  #531: IP30_W_* latches  */
   74| 	uint64_t                reg_0x10018;
   75| 	uint64_t                isr;            /*  0x10030  */
   76| 	uint64_t                reg_0x20000;
   77| 	uint64_t                reg_0x30000;
   78| 
   79| 	/*  ip30_2:  */
   80| 	uint64_t                reg_0x0029c;
   81| 
   82| 	/*  ip30_3:  */
   83| 	uint64_t                reg_0x00284;
   84| 
   85| 	/*  ip30_4:  */
   86| 	uint64_t                reg_0x000b0;
   87| 
   88| 	/*  ip30_5:  */
   89| 	uint64_t                reg_0x00000;
   90| };
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

End with one line: `FIXDRAFT_IP30ASDVASDVNB: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
