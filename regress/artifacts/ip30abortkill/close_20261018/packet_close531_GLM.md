**Your token: `GLM_CLOSE531_20261018`** -- open your answer with it.

# Closing ledger row `ip30abortkill` (#531) -- is anything still owed?  A records check (PACKET-FED)

You cannot read files.  Every fact you need is inlined below; where a question needs a fact this packet does not hold,
say "not checkable from the packet" rather than guessing.  **Please do not simply ratify** -- check the premises, not
just the derivations.

## What this is

`#531` (commit `686d179c`, committed 2026-09-18) took four guest-reachable `abort()` calls out of
`src/devices/dev_sgi_ip30.c` (an SGI IP30 device model in an emulator).  Its detector is a 33-row probe,
`regress/artifacts/ip30abortkill/ip30_abort_probe.py`, wired into gate 14 by `#566` (`8faf4a16`, this morning).  The
ledger row `ip30abortkill` (HIGH) is still `in work`.  `#566`'s note listed what was owed before close:

> Still owed before close (target: before the 2026-10-25 battery): the witness field still leads with the 21-row
> pair; clause (b) -- abort() re-inserted at each fixed site of the FIXED file, re-run at 33 rows -- is held by no kill
> table; and a ruling on whether V7_nocounter and V8_len4 need a carrier that survives the close (Grok 4.7: no).

The project's vacuity floor: a detector must (a) fail on the pre-fix build, (b) fail on "a VERBATIM REINSTATEMENT of
the removed defect at EVERY fixed site", (c) fail on a null medium.  (a) was measured by `#566`: PRE-FIX 10/33 (23 rows
red), POST-FIX 33/33, on the shipped 33-row instrument.  (c) by `#566`: an absent and a non-emulator binary give
CONTROL=DEAD.  This commit would CLOSE the row; it changes only the ledger, the bug file, the CHANGELOG, a generated
queue and a dashboard.  No `src/` file.

## Fact 1 -- what 686d179c removed (its diff of dev_sgi_ip30.c, the removed `fatal`/`abort` lines only)

44:-fatal("IP30 legacy interrupt rewrite: TODO\n");
45:-abort();
105:-fatal("IP30 legacy interrupt rewrite: TODO\n");
106:-abort();
161:-fatal("IP30 legacy interrupt rewrite: TODO\n");
162:-abort();
213:-fatal("IP30 legacy interrupt rewrite: TODO\n");
214:-abort();

No line ADDED by 686d179c contains abort().

## Fact 2 -- the PRE-FIX arms (686d179c^:src/devices/dev_sgi_ip30.c, lines 68-80 and 123-150)

```c
68: DEVICE_TICK(sgi_ip30)
69: {
70: 	struct sgi_ip30_data *d = (struct sgi_ip30_data *) extra;
71: 
72: 	d->reg_0x20000 += 1000;
73: 
74: 	if (d->imask0 & ((int64_t)1<<50)) {
75: 		/*  TODO: Only interrupt if reg 0x20000 (the counter)
76: 			has passed the compare (0x30000).  */
77: fatal("IP30 legacy interrupt rewrite: TODO\n");
78: abort();
79: //		cpu_interrupt(cpu, 8+1 + 50);
80: 	}
123: 	case 0x10020:	/*  Set ISR, according to Linux/IP30  */
124: 		d->isr = idata;
125: 		/*  Recalculate CPU interrupt assertions:  */
126: fatal("IP30 legacy interrupt rewrite: TODO\n");
127: abort();
128: //		cpu_interrupt(cpu, 8);
129: 		break;
130: 
131: 	case 0x10028:	/*  Clear ISR, according to Linux/IP30  */
132: 		d->isr &= ~idata;
133: 		/*  Recalculate CPU interrupt assertions:  */
134: fatal("IP30 legacy interrupt rewrite: TODO\n");
135: abort();
136: //		cpu_interrupt(cpu, 8);
137: 		break;
138: 
139: 	case 0x10030:	/*  Interrupt Status Register  */
140: 		if (writeflag == MEM_WRITE) {
141: 			/*  Clear-on-write  (TODO: is this correct?)  */
142: 			d->isr &= ~idata;
143: 			/*  Recalculate CPU interrupt assertions:  */
144: fatal("IP30 legacy interrupt rewrite: TODO\n");
145: abort();
146: //			cpu_interrupt(cpu, 8);
147: 		} else {
148: 			odata = d->isr;
149: 		}
150: 		break;
```

## Fact 3 -- the clause (b) mutant: diff of HEAD's file against it (normal diff format; '>' = added)

```
150a151,152
> fatal("IP30 legacy interrupt rewrite: TODO\n");
> abort();
243a246,247
> fatal("IP30 legacy interrupt rewrite: TODO\n");
> abort();
287a292,293
> fatal("IP30 legacy interrupt rewrite: TODO\n");
> abort();
305a312,313
> fatal("IP30 legacy interrupt rewrite: TODO\n");
> abort();
```

Context of each insertion in the mutant (line numbers are the mutant's):
```c
146: 		if (!(d->warned & IP30_W_TICK)) {
147: 			d->warned |= IP30_W_TICK;
148: 			fatal("[ sgi_ip30: timer interrupt delivery not "
149: 			    "implemented  (once) ]\n");
150: 		}
151: fatal("IP30 legacy interrupt rewrite: TODO\n");
152: abort();
153: //		cpu_interrupt(cpu, 8+1 + 50);
195: 		break;
196: 
197: 	case 0x10020:	/*  Set ISR (heart.h: set_isr, WRITE-side)  */
198: 		/*
199: 		 *  #531: this arm had NO writeflag test and ran the store
200: 		 *  FIRST, so a guest LOAD zeroed the ISR and then killed the
201: 		 *  host -- `idata' is 0 on a read.  Rows `kill 20 rd' and
202: 		 *  `isr keep' pin both halves.
203: 		 */
204: 		if (writeflag == MEM_WRITE) {
205: 			d->isr = idata;
243: 			    second read path for a register that already has one
244: 			    at 0x10030.  */
245: 		}
246: fatal("IP30 legacy interrupt rewrite: TODO\n");
247: abort();
248: 		break;
249: 
250: 	case 0x10028:	/*  Clear ISR (heart.h: clear_isr, WRITE-side)  */
251: 		/*  #531: same missing writeflag test as 0x10020.  On a READ
252: 		    `idata' is 0, so `&= ~0' was a no-op that still killed the
253: 		    host -- row `kill 28 rd'.  */
254: 		if (writeflag == MEM_WRITE) {
255: 			d->isr &= ~idata;
290: 			 */
291: 		}
292: fatal("IP30 legacy interrupt rewrite: TODO\n");
293: abort();
294: 		break;
297: 		if (writeflag == MEM_WRITE) {
298: 			/*
299: 			 *  #531: THE FILE'S OWN "TODO: is this correct?" IS
300: 			 *  ANSWERED **NO** by the header this device cites.
301: 			 *  heart.h marks isr "(read-only)"; clearing goes
302: 			 *  through clear_isr at 0x10028.  So the clear-on-
303: 			 *  write is DROPPED rather than kept -- applying it
304: 			 *  would be inventing a second clear path.  Row
305: 			 *  `kill 30 wr' pins that the host survives.
306: 			 */
307: 			if (!(d->warned & IP30_W_ISR)) {
308: 				d->warned |= IP30_W_ISR;
309: 				fatal("[ sgi_ip30: interrupt-status rewrite "
310: 				    "not implemented  (once) ]\n");
311: 			}
312: fatal("IP30 legacy interrupt rewrite: TODO\n");
313: abort();
314: //			cpu_interrupt(cpu, 8);
315: 		} else {
```

## Fact 4 -- the prediction (PREDICT_clause_b.txt, file mtime 15:20:53 -- the build log is 15:21:46, the probe log 15:26:18)

```
#531 clause (b), PREDICTED 2026-10-18 15:21 -- written BEFORE the leg runs, so this file's mtime precedes probe_b.log's.
(A first write at 15:20:43 was truncated by an unquoted shell heredoc; this is its rewrite, before any run.)

THE MUTANT (mutant_b_dev_sgi_ip30.c.txt): HEAD's dev_sgi_ip30.c with the two lines #531 removed,
    fatal("IP30 legacy interrupt rewrite: TODO\n");
    abort();
re-inserted VERBATIM at each fixed site, the rest of the fix kept: inside DEVICE_TICK's bit-50 block (after the
latched announce), at the end of case 0x10020 and case 0x10028 (both branches -- the pre-fix arms had no writeflag
test), and in case 0x10030's write branch (after the latched announce).

PREDICTION, row by row (33 rows):
  RED (19): the six kill rows read DEAD -- kill 20 rd, kill 28 rd, kill 30 wr, tick 50, kill 20 wr, kill 28 wr -- and
    the thirteen rows whose session touches an abort site before its observation read `died':
    isr keep, isr clr, isr drop 30, xbit isr, xbit tick, latch 1x, isr 20 rd val, isr 28 rd val, latch 28wr,
    latch 30wr, latch tick, xbit rev, xbit rev2.
  GREEN (14): the seven controls and accept rows (live, devsig, acc 18, acc 30 rd, acc 20000, acc 30000, acc imask);
    the two read arms' txt rows (they want `no', and the read arms print nothing of the post-fix announce before the
    abort); tick 49 (bit 49 does not reach the bit-50 block); and the four `yes' txt rows (kill 30 txt, tick 50 txt,
    kill 20 wr txt, kill 28 wr txt), because the latched announce prints before the reinstated abort and a
    pty-attached stdout is line-buffered.
  So: IP30ABORT_RESULT=14/33.  IF the announce text is lost to the abort (not flushed), those four `yes' rows red
  too: 10/33.  Either way the gate block reds (rows correct, green and red), and clause (b) holds.
```

## Fact 5 -- the measurement (probe_b.log, each row's name, got, want and status; notes cut)

```
ip30_abort_probe -- binary=/tmp/gx566/gxemul label=clause_b machine=sgi/ip3
IP30ABORT_CONTROL=OK
  live         got=0x11223344   want=0x11223344   ok  LIVENESS: a known val
  devsig       got=0xffffffff80010000 want=0xffffffff80010000 ok  DEVICE-SI
  acc 18       got=0xffffffffdeadbeef want=0xffffffffdeadbeef ok  case 0x10
  acc 30 rd    got=alive        want=alive        ok  case 0x10030 IS write
  acc 20000    got=stored+N*1000 want=stored+N*1000 ok  case 0x20000 is wri
  acc 30000    got=0x5678       want=0x5678       ok  case 0x30000, writefl
  acc imask    got=0x40000      want=0x40000      ok  case 0x10000 (imask0)
  kill 20 rd   got=DEAD         want=alive        FAIL  *** A GUEST **LOAD*
  kill 20 rd txt got=no           want=no           ok  DIAGNOSIS ONLY, nev
  kill 28 rd   got=DEAD         want=alive        FAIL  case 0x10028, same 
  kill 28 rd txt got=no           want=no           ok  DIAGNOSIS ONLY, nev
  kill 30 wr   got=DEAD         want=alive        FAIL  case 0x10030's WRIT
  kill 30 txt  got=yes          want=yes          ok  DIAGNOSIS sibling for
  tick 50      got=DEAD         want=alive        FAIL  *** ARM imask0 BIT 
  tick 50 txt  got=yes          want=yes          ok  *** THE POST-FIX HALF
  tick 49      got=no           want=no           ok  DISCRIMINATOR for `ti
  kill 20 wr   got=DEAD         want=alive        FAIL  A guest WRITE at th
  kill 20 wr txt got=yes          want=yes          ok  DIAGNOSIS for the 2
  kill 28 wr   got=DEAD         want=alive        FAIL  A guest WRITE at th
  kill 28 wr txt got=yes          want=yes          ok  DIAGNOSIS for the 2
  isr keep     got=died         want=0x5a5a       FAIL  *** ISR UNCHANGED A
  isr clr      got=died         want=0x5050       FAIL  *** 0x5a5a & ~0x0a0
  isr drop 30  got=died         want=0x5a5a       FAIL  *** THE WRITE MUST 
  xbit isr     got=died         want=1            FAIL  *** TICK FIRST, THE
  xbit tick    got=died         want=1            FAIL  The other half of t
  latch 1x     got=died         want=1            FAIL  TWO declined ISR ac
  isr 20 rd val got=died         want=0x0          FAIL  A declined READ at
  isr 28 rd val got=died         want=0x0          FAIL  A declined READ at
  latch 28wr   got=died         want=1            FAIL  TWO accesses at THI
  latch 30wr   got=died         want=1            FAIL  TWO accesses at THI
  latch tick   got=died         want=1            FAIL  *** TWO TICKS IN ON
  xbit rev     got=died         want=1            FAIL  *** TICK -> ISR -> 
  xbit rev2    got=died         want=1            FAIL  *** ISR -> TICK -> 
IP30ABORT_RESULT=14/33
IP30ABORT_DONE
```

## Fact 6 -- the driver's receipt (LEGB.out)

```
LEGB start 2026-10-18 15:21:19
make rc=0 (mutant_b)
binary fresh (mutant_b): md5 68afa8ddffa7ec06da0cc6f5b2963d40
probe md5 7fbf52ab362fd4ee0801c83aa1206621
probe b: rc=0 272s  IP30ABORT_RESULT=14/33 last=[IP30ABORT_DONE]
gate_arm.sh md5 bf7b6af63fd5cfae9674eabc09ebe05d, scoring text md5 21d7b87406948ce0c1f69eb03dec0c11
LEG b  gate checks=41 fails=22 RED (clause b holds)
     red: [ip30_abort row: kill 20 rd got=0] [ip30_abort row: kill 28 rd got=0] [ip30_abort row: kill 30 wr got=0] [ip30_abort row: tick 50 got=0] [ip30_abort row: kill 20 wr got=0] [ip30_abort row: kill 28 wr got=0] [ip30_abort row: isr keep got=0] [ip30_abort row: isr clr got=0] [ip30_abort row: isr drop 30 got=0] [ip30_abort row: xbit isr got=0] [ip30_abort row: xbit tick got=0] [ip30_abort row: latch 1x got=0] [ip30_abort row: isr 20 rd val got=0] [ip30_abort row: isr 28 rd val got=0] [ip30_abort row: latch 28wr got=0] [ip30_abort row: latch 30wr got=0] [ip30_abort row: latch tick got=0] [ip30_abort row: xbit rev got=0] [ip30_abort row: xbit rev2 got=0] [ip30_abort rows correct got=14] [ip30_abort rows green got=14] [ip30_abort rows red got=19]
--- restore
make rc=0 (restore)
binary fresh (restore): md5 25ac428c659292aa837e2ee8721419c0
part 1: src/devices/dev_sgi_ip30.c == HEAD
part 2: binary newer than src/devices/dev_sgi_ip30.c
sentinel cleared
LEGB end 2026-10-18 15:26:46
LEGB_DONE
```

## Fact 7 -- the two disclosed escapes, from their kill-table logs

```
killtable4_20260918/V7_nocounter.raw: IP30ABORT_RESULT=32/32
killtable4_20260918/base.raw: IP30ABORT_RESULT=32/32
killtable5_20260918/V8_len4.raw: IP30ABORT_RESULT=33/33
killtable5_20260918/base.raw: IP30ABORT_RESULT=33/33
```
V7_nocounter deletes `d->reg_0x20000 += 1000;` in DEVICE_TICK (a line ABOVE the de-fatalised guard; it runs on every
tick).  V8_len4 adds `&& len == 4` to the 0x10020 write guard (the guarded body never tests len).  The probe's CONTRACT
lists V7 under MEASURED ESCAPES and V8 under DOES NOT CATCH.

## Fact 8 -- #561's HELD corrections to dev_sgi_ip30.c (EDITS_561.json, key `held`; ruled replacement text)

* place 7 devsgiip30:F2 -> 'FOUR announce paths share TWO bits, and that is deliberate: IP30_W_ISR covers THREE (the 0x10020, 0x10028 and 0x10030 WRITES), which all print the SAME string byte for byte; the 0x10020 and 0x10028 READS are silent declines and touch no latch.'
* place 8 devsgiip30:F2 -> 'three bits on the ISR side'
* place 9 devsgiip30:F2 -> 'All five ISR sites PRINTED (before this decline was adopted)'
* place 10 devsgiip30:F2 -> 'All five ISR sites PRINTED (before this decline was adopted)'

HEAD's dev_sgi_ip30.c, the latch comment (lines 50-52): "SIX announce paths share TWO bits, and that is deliberate:
IP30_W_ISR covers FIVE (0x10020 write and read, 0x10028 write and read, 0x10030 write), which all print the SAME string
byte for byte."  At HEAD the 0x10020 and 0x10028 READ arms print nothing (a silent decline, #531's F13 ruling); the three
WRITE arms share IP30_W_ISR and one message; DEVICE_TICK has its own bit, IP30_W_TICK.  OUTSTANDING_BUGS.md's `### #561`
section lists all seventeen held src/ comments and ends "Still owed: the HELD edits."  #561 held them because a src/
comment owes est/ byte-identity and build-tree propagation.  No ledger row carries the seventeen.

## The drafted records

### Ledger (every changed field)

```
DRAFT LEDGER CHANGES (tools/pipeline/ledger.json, built from HEAD 8faf4a16's blob)

== ip30abortkill
  state: in work -> closed
  commits: 686d179 -> 686d179 8faf4a16
  closure (NEW): by=opus5-mainloop badge=A
    note: CLOSED by its closure-records commit (2026-10-18): #531 (686d179c, committed 2026-09-18) took dev_sgi_ip30.c's four guest-reachable abort() calls out -- the 0x10020 and 0x10028 loads decline silently, their stores keep their effect with one latched announce (IP30_W_ISR), the 0x10030 store is dropped with that same announce, and DEVICE_TICK's bit-50 arm announces once on its own bit.  Detector: regress/artifacts/ip30abortkill/ip30_abort_probe.py, 33 rows, wired into gate 14 by #566 (8faf4a16; gate 14 PASS 1225 on a HEAD binary, regress/artifacts/ip30abortkill/gatewire_20261018/gate14/).  The floor on the shipped instrument, each leg in one HEAD-source scratch clone: clause (a) 10/33 with 686d179c^'s file (gatewire_20261018/legs/); clause (b) 14/33 with the removed fatal()+abort() pair re-inserted verbatim at all four fixed sites of the fixed file, the 19 reds named before the run (regress/artifacts/ip30abortkill/close_20261018/); clause (c) CONTROL=DEAD for an absent and a non-emulator binary (gatewire_20261018/legs/).  Kill tables 1-5 closed the latch-axis class (table 5: base 33/33, V1_assign20wr and V2_assigntick killed).  Disclosed, not owed before close, and carried on by ip30abortresidual: V7_nocounter (32/32 in kill table 4), the width axis V8_len4 (33/33 in kill table 5), and #561's four HELD corrections to the fixed file's comments.  A load stall can read green in gate 14 (ip30stallgreen).
  witness (new head; HEAD's witness follows it unchanged):
    probe:regress/artifacts/ip30abortkill/ip30_abort_probe.py -- rung 3 on unmodified `-E sgi -e ip30'; in gate 14 since #566 (8faf4a16).  THE SHIPPED 33-ROW INSTRUMENT, one instrument, HEAD's sources in a scratch clone: PRE-FIX 10/33, 23 rows red, every abort site among them (regress/artifacts/ip30abortkill/gatewire_20261018/legs/probe_prefix.log); POST-FIX 33/33 (gatewire_20261018/legs/probe_base.log); the removed fatal()+abort() re-inserted at every fixed site of the fixed file 14/33, the 19 reds named before the run (regress/artifacts/ip30abortkill/close_20261018/probe_b.log, PREDICT_clause_b.txt, CLAUSE_B.txt).  HISTORY, kept as written:  
  state_note (new head; HEAD's note follows it unchanged after '  ||  '):
    [2026-10-18, CLOSED] The closure-records commit closed the row: clause (b) measured 14/33 on the shipped instrument (close_20261018/); the witness now leads with the 33-row pair; V7_nocounter, V8_len4 and #561's four held corrections to dev_sgi_ip30.c's comments are carried by ip30abortresidual (LOW).  REGRESS and the closure review are held for the flagship (hold_question).  The `Still owed before close' paragraph in the #566 note below is discharged by this commit.  ||  
  hold_question (NEW):
    (held 2026-10-18 at ip30abortkill's closure, under the owner's 2026-10-17 Fable hold) REGRESS: does regress/artifacts/ip30abortkill/ip30_abort_probe.py still score 33/33 with CONTROL=OK on a build of HEAD, 10/33 with 686d179c^'s dev_sgi_ip30.c, and 14/33 with regress/artifacts/ip30abortkill/close_20261018/mutant_b_dev_sgi_ip30.c.txt (the clause (b) leg)?  CLOSURE REVIEW: does the closure stand -- the witness led by the 33-row pair and the clause (b) leg, and V7_nocounter, V8_len4 and #561's four held dev_sgi_ip30.c comment corrections carried by ip30abortresidual rather than done before the close?
  entries appended (2; the closure check's seat entries are added after it answers):
    {"date": "2026-10-18", "phase": "review", "seat": "fable5", "grade": "UNKNOWN", "grader": "", "ev": "not tried", "note": "ip30abortkill [HELD AWAITING SEAT: fable5] the CLOSURE CHECK: not tried  The question is in the row's hold_question."}
    {"date": "2026-10-18", "phase": "regress", "seat": "fable5", "grade": "UNKNOWN", "grader": "", "ev": "not fired", "note": "ip30abortkill [HELD AWAITING SEAT: fable5] closed by its closure-records commit and owes the REGRESS review, a distinct phase under the regress-is-fable-only directive.  The question is in the row's hold_question."}

== ip30abortresidual (NEW ROW)
  sev: LOW
  state: open
  opened: 2026-10-18
  witness: none
  commits: 
  title: #531's residuals, carried here from ip30abortkill at its closure: V7_nocounter (delete `d->reg_0x20000 += 1000': 32/32 in kill table 4), the width axis V8_len4 (`&& len == 4' on the 0x10020 write guard: 33/33 in kill table 5), and #561's four HELD corrections to dev_sgi_ip30.c's comments (the latch comment still counts SIX announce paths, IP30_W_ISR covering FIVE, both read arms among them; the shipped code has FOUR and THREE) -- coverage debt, clause (e) debt and wrong records in product comments; none a floor breach
  state_note: filed 2026-10-18 by ip30abortkill's closure-records commit, so that row could close without dropping them.  (1) V7_nocounter -- the probe's CONTRACT has it under MEASURED ESCAPES (MH_nocounter): the counter is UNCONDITIONAL, above the de-fatalised guard, so fix-independent (the fable5 ruling of 2026-09-18); measured on the 32-row instrument, not re-run at 33.  (2) V8_len4 -- under DOES NOT CATCH: the guarded body never tests len, so by the pcc2widthkills bound it is a single-operand marginal; cheap -- len takes at most four values and the probe already has guest_store64/guest_load64.  (3) places 7-10 of #561's HELD list (regress/artifacts/recordfix_20261002/adjudication_20261006/EDITS_561.json, `held'; OUTSTANDING_BUGS.md's #561 section: `Still owed: the HELD edits'): ruled replacements for the latch comment above IP30_W_TICK in src/devices/dev_sgi_ip30.c, which says `SIX announce paths share TWO bits ... IP30_W_ISR covers FIVE (0x10020 write and read, 0x10028 write and read, 0x10030 write)' -- #531's own F13 ruling made both read arms decline silently, so the shipped code has four and three -- and for three sentences that still speak of five ISR sites.  #561 held them because a src/ comment owes est/ byte-identity and build-tree propagation; they are named here so the dev_sgi_ip30.c obligation is on a ledger row, not only in the bug file.  Owed when this row's round runs: a row each for (1) and (2) or a recorded decision not to, and (3) applied in all four trees.  The load-stall green is a separate row, ip30stallgreen.

== wiringcliff
  commits: 8404520 eec0f4a 8d038908 -> 8404520 eec0f4a 8d038908 8faf4a16
```

### OUTSTANDING_BUGS.md (normal diff)

```
21619a21620,21621
> >
> > *** [2026-10-18, the closure-records commit] CLOSED.  CLAUSE (b) IS MEASURED ON THE SHIPPED INSTRUMENT. ***  HEAD's `dev_sgi_ip30.c` with the removed `fatal("IP30 legacy interrupt rewrite: TODO\n"); abort();` pair re-inserted verbatim at all four fixed sites -- after DEVICE_TICK's latched bit-50 announce, after the `0x10020` and `0x10028` arms' if/else, after the `0x10030` write announce -- scores **14/33**: the six kill rows DEAD and thirteen state rows `died`, the 19 reds named row by row before the run (`regress/artifacts/ip30abortkill/close_20261018/`, `CLAUSE_B.txt`).  The witness field now leads with the 33-row pair and that leg; the 21-row pair and the 18-row order proof stay as history.  `V7_nocounter`, `V8_len4` and `#561`'s four held corrections to this file's comments (places 7-10) are carried by `ip30abortresidual` (LOW, open).  REGRESS and the closure review are held for the flagship (the row's `hold_question`).
24982a24985,25001
> 
> ### 2026-10-18 -- `ip30abortkill` closes (clause (b) measured, 14/33); its residuals move to `ip30abortresidual`
> 
> * **`ip30abortkill` (HIGH) CLOSED** -- `#531` (`686d179c`, committed 2026-09-18) and its 33-row detector, in gate 14
>   since `#566` (`8faf4a16`).  The floor on the shipped instrument: clause (a) 10/33 (`686d179c^`'s file, `#566`'s
>   legs); clause (b) 14/33 -- the removed `fatal()` + `abort()` pair re-inserted verbatim at all four fixed sites of the
>   fixed file, the 19 reds named before the run (`regress/artifacts/ip30abortkill/close_20261018/`); clause (c)
>   CONTROL=DEAD for an absent and a non-emulator binary (`#566`).  The witness field now leads with the 33-row pair; the
>   21-row pair and the 18-row order proof stay as history.  REGRESS and the closure review held for the flagship.
> * **`ip30abortresidual` (LOW, open)** -- `V7_nocounter` (delete `d->reg_0x20000 += 1000`: 32/32 in kill table 4, on
>   the 32-row instrument) and the width axis `V8_len4` (`&& len == 4` on the `0x10020` write guard: 33/33 in kill
>   table 5), both disclosed in the probe's CONTRACT; and places 7-10 of `#561`'s HELD list -- ruled replacements for
>   `dev_sgi_ip30.c`'s latch comment, which still counts SIX announce paths with `IP30_W_ISR` covering FIVE, both read
>   arms among them (the shipped code has four and three, since `#531`'s own F13 silent-decline ruling), and for three
>   sentences that still count five ISR sites.  Coverage debt, clause (e) debt and wrong records in product comments;
>   none a floor breach.  The `#561` section above still lists the four among its held edits.
> * **`wiringcliff`** -- its commits field gains `#566`'s `8faf4a16`.
```

### CHANGELOG.md block (prepended; {CLOSURE_CHECK} is filled in from this check)

```
# Records, 2026-10-18: `ip30abortkill` closes -- clause (b) measured on the shipped 33-row instrument, 14/33 as named before the run; its residuals move to `ip30abortresidual`; REGRESS held

`#531` (`686d179c`, committed 2026-09-18) took the four guest-reachable `abort()` calls out of
`src/devices/dev_sgi_ip30.c`: the `0x10020` and `0x10028` loads decline silently, their stores keep their effect with
one latched announce (`IP30_W_ISR`), the `0x10030` store is dropped with that same announce, and DEVICE_TICK's bit-50
arm announces once on its own bit.  Its detector, `regress/artifacts/ip30abortkill/ip30_abort_probe.py` (33 rows),
runs in gate 14 since `#566` (`8faf4a16`).  `#566` named three things still owed before the row could close; this
commit discharges them and closes it:

* **CLAUSE (b), MEASURED** (`regress/artifacts/ip30abortkill/close_20261018/`).  HEAD's `dev_sgi_ip30.c` with the
  removed `fatal("IP30 legacy interrupt rewrite: TODO\n"); abort();` pair re-inserted verbatim at all four fixed sites
  -- after DEVICE_TICK's latched bit-50 announce, after the `0x10020` and `0x10028` arms' if/else, after the `0x10030`
  write announce -- built in `#566`'s scratch clone: **14/33**, the six kill rows DEAD and thirteen state rows `died`;
  gate 14's block text on that log, 41 checks and 22 red.  `PREDICT_clause_b.txt`, written before the build, named
  the same 19 red rows and the same 14 green ones; `CLAUSE_B.txt` records the file times, which git does not carry.
  The clone was restored to HEAD and cleared both parts.  `build/` was not touched.
* **THE WITNESS** now leads with the shipped instrument's pair -- PRE-FIX 10/33, POST-FIX 33/33 (`#566`'s legs) --
  and the clause (b) leg; the 21-row pair and the 18-row oracle-correction order proof stay, as history.
* **THE RESIDUALS** move to a new row, `ip30abortresidual` (LOW, open), rather than close with `ip30abortkill`, as
  `#527`'s closure did with `ppc527residual`: `V7_nocounter` (delete `d->reg_0x20000 += 1000`; 32/32 in kill table 4,
  on the 32-row instrument) and the width axis `V8_len4` (`&& len == 4` on the `0x10020` write guard; 33/33 in kill
  table 5), both disclosed in the probe's CONTRACT; and places 7-10 of `#561`'s HELD list, ruled replacements for
  `dev_sgi_ip30.c`'s latch comment -- which still counts SIX announce paths with `IP30_W_ISR` covering FIVE, both
  read arms among them, where the shipped code has four and three -- and for three sentences that still count five ISR
  sites.  `#561` held them because a `src/` comment owes `est/` byte-identity and build-tree propagation; the row puts
  that `dev_sgi_ip30.c` obligation on the ledger.  None is a floor breach.
* **REGRESS and the closure review held for the flagship**: the row's `hold_question` asks for 33/33, 10/33 and 14/33
  on the three builds, and whether the closure stands.
* `wiringcliff`'s commits field gains `#566`'s `8faf4a16`.

{CLOSURE_CHECK}  Ledger, bug file, matrix, queue and this block only; no `src/` touched.
```
## My dispositions -- the ones to attack

* **D1 -- close now.**  The three owed items are discharged: the witness leads with the 33-row pair, clause (b) is
  measured, and the residual question is ruled (D2).
* **D2 -- a new carrier row, `ip30abortresidual` (LOW).**  `V7_nocounter` and `V8_len4` are disclosed in the probe's
  CONTRACT; Grok 4.7 said at `#566` that they need no carrier.  I chose one on `#527`'s precedent, where GPT-6 Astra
  found that its residuals had been made the closing row's to carry, so closing that row bare would have dropped them
  (they went to `ppc527residual`).  Here nothing assigned them to `ip30abortkill` in so many words; `#566`'s note only
  asked whether they need a carrier that survives the close.
* **D3 -- `#561`'s four HELD `dev_sgi_ip30.c` comment corrections (places 7-10) join that carrier.**  I first thought
  the file's latch comment (`SIX announce paths share TWO bits ... IP30_W_ISR covers FIVE (0x10020 write and read,
  0x10028 write and read, 0x10030 write)`) was a NEW finding; it is not -- `#561` ruled a replacement and HELD it with
  sixteen other `src/` comments (`regress/artifacts/recordfix_20261002/adjudication_20261006/EDITS_561.json`, key
  `held`; `OUTSTANDING_BUGS.md`'s `### #561` section ends "Still owed: the HELD edits.").  No ledger row carries those
  seventeen.  I put the four `dev_sgi_ip30.c` ones on the new row and left the `#561` section as it is.
* **D4 -- Fable: two HELD markers and one `hold_question`** covering the closure review and REGRESS (the owner's
  2026-10-17 directive: Astra + Grok + GLM rule; Fable held, tried once per pass, a wall recorded as a SEAT FAILURE).
* **D5 -- the stale product comment is NOT fixed in this commit.**  A records commit touches no `src/`; a `src/`
  comment owes `est/` byte-identity and build-tree propagation, which `#561` also declined to do in a records commit.

## Questions

1. **Is anything still owed before `ip30abortkill` may close** that the drafted records drop?  Judge from `#566`'s
   owed list and the facts above; say which part of the answer the packet cannot settle.
2. **Is the leg a valid clause-(b) measurement?**  Clause (b): the detector fails "on a VERBATIM REINSTATEMENT of the
   removed defect at EVERY fixed site".  I believe placing the pair AFTER the if/else of `case 0x10020` and
   `case 0x10028` is the faithful reinstatement because the pre-fix arms had no `writeflag` test, so both a load and a
   store reached it -- check `git show 686d179c^:src/devices/dev_sgi_ip30.c`.  Is anything else about the mutant, the
   order (prediction before measurement) or the scoring wrong?
3. **D2/D3: which carrier is right?**  A new row; or close with the row (they are disclosed); or an existing row
   (`ip30setisrassign` is open on the same file; `hrecordowed` carries the harness's unplaced records); and should
   `#561`'s four places be carried at all, given the `#561` section already lists them as owed?
4. **Is every drafted fact exact** -- each number, path, hash and date in the three drafts?
5. **Which of D1-D5 is wrong?**

Answer format: open with your token, then ONE line `VERDICT: <n> flags -- <one line>`, then one `FLAG:` line per
defect with its evidence (a fact number from this packet) and the replacement text, then short answers to 1-5.  A flag must be checkable.
