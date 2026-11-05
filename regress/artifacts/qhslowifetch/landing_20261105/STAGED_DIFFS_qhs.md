# STAGED_DIFFS_qhs.md -- what the qhslowifetch landing commits for each shared file, against HEAD and the working copy

HEAD acdf8ce4.  Round number #582 (derived: max round heading in HEAD's CHANGELOG.md (#581) + 1).  Built by build_staged_qhs.py at 2026-11-05 14:03:22 local.  Every hunk is printed.

## src/cpus/cpu_ppc_instr.c

HEAD 153707 bytes md5 6efa6781b20375b984e209850277ef29; staged 156906 bytes md5 dbd192fbc9501334e0ba3610f4829dcf; working copy 156866 bytes md5 54c9802bd12fde426372343cdbc828a8, which IS the source table 12 measured (`regress/artifacts/qhslowifetch/r7_20261105/cpu_ppc_instr.c.fix7`, md5 in `table12/MD5.txt`).  The staged file before its fill (HEAD + the qhs hunk) is md5 54c9802bd12fde426372343cdbc828a8: the working copy each tree must hold when update_trees_qhs.sh runs (staged/UPDATE.md5).

THE TREE UPDATE HAS RUN: the working copy holds the FILLED file (md5 dbd192fbc9501334e0ba3610f4829dcf, == the staged file); everything below is built from its unfilled form (kit_qhs.unfill_c), md5 54c9802bd12fde426372343cdbc828a8.

Hunk attribution of the working copy against HEAD (kit_qhs.classify_c; anything unattributable refuses the build):

* qhslowifetch: X(to_be_translated), HEAD line 4130, 4 -> 79 line(s) -- the one hunk staged

The four placeholders, filled (the coordinator's decision 1; comment-only: kit_qhs.comment_free(staged) == comment_free(HEAD + the qhs hunk) -- True): #NNN -> #582; #MMM -> `ppcvecaddr` (filed); #QQQ -> `ppcintentrymsr` (the existing row it names, re-wrapped onto two lines); #PPP -> `ppcmpcheckstop` (filed).

### staged vs HEAD (the commit's whole change to this file)

1 hunk(s):

```
@@ replace  left line 4130 (4 lines) -> right line 4130 (80 lines)
-             fatal("PPC to_be_translated(): "
-                 "read failed: TODO\n");
-             exit(1);
-             /*  goto bad;  */
+             /*  #582: the instruction fetch failed.  This
+                 used to be fatal() + exit(1).  Four states
+                 reach here; none may run this slot, and
+                 the slot stays TO_BE_TRANSLATED, so a fetch
+                 that later reaches it re-enters this arm.
+                 (A -T halt is terminal whichever exit is
+                 taken: memory.c cleared running, so the run
+                 loop no longer enters this CPU and a further
+                 step or continue runs nothing.  (c)'s park
+                 only ends the current batch and keeps pc
+                 here.)  */
+             /*  (a) Read-ahead: the guest has not reached
+                 this address.  Touch nothing, as bad:
+                 does.  */
+             if (cpu->translation_readahead)
+                 return;
+             /*  (b) The translation in memory_rw raised an
+                 ISI or 603 IMISS: ppc_exception() saved
+                 SRR0/SRR1 and moved pc to the vector.
+                 That route is reached on no measured
+                 session (the dispatch pc lookup translates
+                 this address first); kept so a delivered
+                 exception is not doubled by (d).  Not
+                 watertight: when the vector equals the
+                 failing address, pc equals addr again, (b)
+                 is skipped and (d) delivers a second
+                 exception over SRR0/SRR1, or checkstops if
+                 MSR[ME] is clear (`ppcvecaddr`; no producer on any
+                 machine measured).  pc is compared ALIGNED:
+                 the prologue aligns addr but not pc, and a
+                 guest can make pc unaligned (mtlr and bclr
+                 copy LR unmasked), so a bare pc != addr
+                 took this arm for such a pc, re-ran the
+                 slot and, under -T, printed thousands of
+                 halt reports instead of parking in (c).
+                 next_ic must follow pc; ppc_exception()
+                 re-resolves it, and (d) relies on that.
+                 The refresh here is redundant and harmless.  */
+             if ((cpu->pc & ~(uint64_t)3) != addr) {
+                 quick_pc_to_pointers(cpu);
+                 return;
+             }
+             /*  (c) -T: memory.c cleared running and printed
+                 the non-existant line.  No PowerPC exception
+                 is involved.  Park at this pc (set above) so
+                 the debugger shows the failing fetch.  */
+             if (!cpu->running) {
+                 cpu->cd.ppc.next_ic = &nothing_call;
+                 return;
+             }
+             /*  (d) A device declined an instruction-width
+                 read while running.  A fetch the bus
+                 terminates with an error is a machine check
+                 (vector 0x200) when MSR[ME] is set and a
+                 checkstop when it is clear.  SRR1 status
+                 bits are not modelled.  */
+             if (cpu->cd.ppc.msr & PPC_MSR_ME) {
+                 /*  ppc_exception() leaves MSR[ME] set,
+                     where the architecture clears it on a
+                     machine check, so a further failing
+                     fetch here takes a second machine check
+                     instead of checkstopping
+                     (`ppcintentrymsr`).  */
+                 ppc_exception(cpu, PPC_EXCEPTION_MC);
+                 return;
+             }
+             /*  Clears only this CPU's running and parks
+                 next_ic on nothing_call, which ends the
+                 current batch.  memory.c's -T halt clears
+                 every CPU's running; a checkstop is a
+                 per-processor state.  pmppc has one CPU,
+                 so what the other CPUs of a multiprocessor
+                 do after this checkstop is not measured
+                 (`ppcmpcheckstop`).  */
+             fatal("[ ppc: instruction fetch from 0x%" PRIx64
+                 " declined with MSR[ME]=0: checkstop ]\n",
+                 (uint64_t) addr);
+             cpu->running = 0;
+             cpu->cd.ppc.next_ic = &nothing_call;
+             return;
```

### staged vs HEAD + the qhs hunk (the fill alone)

4 hunk(s):

```
@@ replace  left line 4130 (1 lines) -> right line 4130 (1 lines)
-             /*  #NNN: the instruction fetch failed.  This
+             /*  #582: the instruction fetch failed.  This
@@ replace  left line 4157 (1 lines) -> right line 4157 (1 lines)
-                 MSR[ME] is clear (#MMM; no producer on any
+                 MSR[ME] is clear (`ppcvecaddr`; no producer on any
@@ replace  left line 4191 (1 lines) -> right line 4191 (2 lines)
-                     instead of checkstopping (#QQQ).  */
+                     instead of checkstopping
+                     (`ppcintentrymsr`).  */
@@ replace  left line 4202 (1 lines) -> right line 4203 (1 lines)
-                 (#PPP).  */
+                 (`ppcmpcheckstop`).  */
```

### staged vs the working copy (what the working copy lacks, and what stays uncommitted)

4 hunk(s): placeholder fill at working-copy line 4130 (#NNN); placeholder fill at working-copy line 4157 (#MMM); placeholder fill at working-copy line 4191 (#QQQ); placeholder fill at working-copy line 4202 (#PPP).

## src/include/cpu_ppc.h (staged == the working copy; PART OF THE UNIT, the coordinator's decision 2)

HEAD 11317 bytes md5 f2097d94e6b9d550411500f1e5075353; staged = working copy 11382 bytes md5 30544e73fcedac91264b92694a490c9a, equal to table 12's baseline header (`regress/artifacts/qhslowifetch/det_20261104/cpu_ppc.h.fix`, md5 in `table12/MD5.txt`).  The machine-check arm's `ppc_exception(cpu, PPC_EXCEPTION_MC)` needs this define.

### staged vs HEAD

1 hunk(s):

```
@@ insert  left line 252 (0 lines) -> right line 252 (1 lines)
+ #define    PPC_EXCEPTION_MC    0x2    /*  Machine check, vector 0x200  */
```

## regress/gate_ppc.sh

HEAD 31453 bytes md5 50265c7e9e8a96a2af115c3d466ead74; staged 40240 bytes md5 b4d4e002bb0179c92a34bc8b0c9e6e51; working copy 40240 bytes md5 68768d047f1480ac4bb527b906b5118b (READ only; the regress review's R-A is in its qhs block, r7_20261105/gate_ppc.sh.regrec.diff).  The qhs block: 52 lines, working-copy lines 287-338, extracted by anchor; header and title `#NNN' -> `#582'.  #575's block in the working copy: lines 340-374 (never read).  `bash -n` is run by the pretest.

Hunk attribution of the working copy against HEAD:

* HEAD line 98: the gate_begin title, ` + #NNN ifetch' appended -- qhslowifetch
* HEAD line 287: one 53-line insert after the #579 block = the qhs block (working-copy lines 287-338) -- qhslowifetch, and 1 blank line(s)

### staged vs HEAD (the title, and the qhs block plus one blank line directly below the #579 block)

2 hunk(s):

```
@@ replace  left line 98 (1 lines) -> right line 98 (1 lines)
- gate_begin "gate 13: PowerPC FP conversion + FPSCR (#304/#305/#324-#330) + rlwimi/rldimi/rldicl + #571 DS-form + #579 llsc"
+ gate_begin "gate 13: PowerPC FP conversion + FPSCR (#304/#305/#324-#330) + rlwimi/rldimi/rldicl + #571 DS-form + #579 llsc + #582 ifetch"
@@ insert  left line 287 (0 lines) -> right line 287 (53 lines)
+ # ---- qhslowifetch (#582): a failed slow-path instruction fetch no longer ends the emulator process -- its 249-row detector ------
+ # X(to_be_translated) read the word with memory_rw and, on failure, printed `read failed: TODO' and called exit(1).  The arm now
+ # returns on read-ahead, refreshes next_ic when the translation already delivered an exception, PARKS the CPU on a -T halt, and
+ # delivers a machine check (MSR[ME] set) or a checkstop (clear) when a device declines the fetch while running.  `-E pmppc' with a
+ # raw four-byte word needs no image, so this block runs BEFORE the NetBSD prerequisite, like the #579 block above.  Thirty-one cold
+ # sessions: controls (a live word, a bogus machine, the ISI route by continue and by step, the no -T route), four -T sessions at
+ # 0x02040000 -- step, continue, step-step-continue-continue, and a step with MSR[ME] set -- each pinning the park (pc, SRR0), the
+ # exact halt-report count, the final MSR and the absence of the fatal, UNIMPLEMENTED, exception and checkstop text (the ME-set
+ # step pins the same), eight -T continues from cpc700_pci's last word whose read-ahead reaches arm (a) -- pc's low two bits {00,
+ # 01, 10, 11} x MSR[ME] {clear, set}, entered at 0xfec00004 | low bits, each pinning the same nine channels: survival, the park pc,
+ # the two halt reports, the halted address, the stop, the final MSR, no checkstop line, SRR0 untouched and no UNIMPLEMENTED text
+ # (repair 7 completed the grid, repairs 7b and 8 the channels; repair 6 added the first unaligned cell), eight one-entry PARTNERS
+ # at the same full pc and MSR as those eight (pc set to 0xfec00008 | low bits directly, so the first fetch fails once; repair 11):
+ # each pair presents the failure block with the same pc, addr, MSR, running and slot and differs only in translation_readahead, so a
+ # toggle inserted before arm (a) whose condition reads only that shared entry state fires on the partner's one visit exactly when it
+ # fires on the two-entry session's first visit (the probe's docstring; codex rec13; regress review R-A) -- and six -T continues
+ # into a guest-made unaligned pc (mtlr; blr), low bits 11, 01 and 10 with MSR[ME] clear and set, that arm (c) must park: one-entry
+ # failures, which see a change the block makes under pc's low bits and ME that the two-entry read-ahead sessions undo (repairs 5,
+ # 6, 9 and 10; with `T cont`, `T step`, `again` and `T me` they give every (low bits, ME) cell a one-entry session).
+ # The rung-3 witness is the 17-row probe frozen at regress/artifacts/qhslowifetch/witness_20261104/; the detector scores 108/249 (141
+ # rows red) on the pre-fix build and 249/249 on the fix (regress/artifacts/qhslowifetch/r7_20261105/table12/SCORES.txt).  Scored in the
+ # #579 shape: the completion sentinel once and last; each protocol key once in any form and once accepted; every row by name; the
+ # emitted, green and red row counts pinned to literals.  Names are at most 16 characters in an 18-wide column.  Test-variant tables:
+ # regress/artifacts/qhslowifetch/det_20261104/table1/ (the 50-row probe), table2/ (the 56-row probe), r3_20261105/table3/
+ # (the 62-row probe), r4_20261105/table4/ (the 69-row probe), r5_20261105/table5/ (the 79-row probe), r6_20261105/table6/ (the
+ # 82-row probe), r7_20261105/table7/ (the 103-row probe), r7_20261105/table8/ (the 129-row probe), r7_20261105/table9/ (the 137-row
+ # probe), r7_20261105/table10/ (the 153-row probe), r7_20261105/table11/ (the 177-row probe) and r7_20261105/table12/ (this probe,
+ # the record; its pairing check, table12/PAIRS_base.out).
+ IFLOG=$LOGDIR/ppc_ifetch.log
+ python3 -u ppc_ifetch_probe.py "$PMAX" gate "$LOGDIR/ppc_ifetch" > "$IFLOG" 2>&1 || true
+ if [ "$(grep -cx 'PPC_IFETCH_PROBE_DONE' "$IFLOG")" != 1 ]; then
+     note "ppc_ifetch: completion sentinel missing or duplicated; last lines follow"
+     tail -5 "$IFLOG" | sed 's/^/       /'
+     check "ppc_ifetch probe completed" "no" "yes"
+ else
+     check "ppc_ifetch probe completed" "yes" "yes"
+     check "ppc_ifetch sentinel is the last line" "$(tail -n 1 "$IFLOG")" "PPC_IFETCH_PROBE_DONE"
+     for k in RESULT CONTROL SYMPTOM RED; do
+         check "ppc_ifetch $k= lines" "$(grep -c "^PPC_IFETCH_$k=" "$IFLOG")" "1"
+     done
+     check "ppc_ifetch RESULT=249/249"  "$(grep -cx 'PPC_IFETCH_RESULT=249/249' "$IFLOG")" "1"
+     check "ppc_ifetch CONTROL=OK"      "$(grep -cx 'PPC_IFETCH_CONTROL=OK' "$IFLOG")" "1"
+     check "ppc_ifetch SYMPTOM=ABSENT"  "$(grep -cx 'PPC_IFETCH_SYMPTOM=ABSENT' "$IFLOG")" "1"
+     check "ppc_ifetch RED=none"        "$(grep -cx 'PPC_IFETCH_RED=none' "$IFLOG")" "1"
+     for v in "ctl session" "ctl live" "ctl srr0 kept" "neg apparatus" "isi session" "isi srr0" "isi pc" "isi text" "isi nonex" "isi1 session" "isi1 srr0" "isi1 pc" "isi1 nonex" "noT session" "noT pc" "noT srr0 kept" "noT unimpl" "noT chkstop" "T cont session" "T cont text" "T cont prompt" "T cont pc" "T cont srr0" "T cont nonex" "T cont unimpl" "T cont exc" "T cont chkstop" "T cont msr" "T step session" "T step text" "T step prompt" "T step pc" "T step srr0" "T step nonex" "T step unimpl" "T step exc" "T step chkstop" "T step msr" "T me session" "T me pc" "T me srr0" "T me nonex" "T me text" "T me exc" "T me unimpl" "T me chkstop" "T me msr" "again session" "again pc" "again srr0" "again nonex" "again text" "again unimpl" "again exc" "again chkstop" "again prompt" "again msr" "T ra session" "T ra pc" "T ra nonex" "T ra addr" "T ra stopped" "T ra msr" "T ra chkstop" "T ra srr0" "T ra unimpl" "T ra me session" "T ra me pc" "T ra me nonex" "T ra me addr" "T ra me stopped" "T ra me chkstop" "T ra me msr" "T ra me srr0" "T ra me unimpl" "T ra odd session" "T ra odd pc" "T ra odd nonex" "T ra odd addr" "T ra odd stopped" "T ra odd msr" "T ra odd chkstop" "T ra odd srr0" "T ra odd unimpl" "T ra o1m session" "T ra o1m pc" "T ra o1m nonex" "T ra o1m addr" "T ra o1m stopped" "T ra o1m msr" "T ra o1m chkstop" "T ra o1m srr0" "T ra o1m unimpl" "T ra o2 session" "T ra o2 pc" "T ra o2 nonex" "T ra o2 addr" "T ra o2 stopped" "T ra o2 msr" "T ra o2 chkstop" "T ra o2 srr0" "T ra o2 unimpl" "T ra o2m session" "T ra o2m pc" "T ra o2m nonex" "T ra o2m addr" "T ra o2m stopped" "T ra o2m msr" "T ra o2m chkstop" "T ra o2m srr0" "T ra o2m unimpl" "T ra o3 session" "T ra o3 pc" "T ra o3 nonex" "T ra o3 addr" "T ra o3 stopped" "T ra o3 msr" "T ra o3 chkstop" "T ra o3 srr0" "T ra o3 unimpl" "T ra o3m session" "T ra o3m pc" "T ra o3m nonex" "T ra o3m addr" "T ra o3m stopped" "T ra o3m msr" "T ra o3m chkstop" "T ra o3m srr0" "T ra o3m unimpl" "T rp session" "T rp pc" "T rp nonex" "T rp addr" "T rp stopped" "T rp msr" "T rp chkstop" "T rp srr0" "T rp unimpl" "T rp me session" "T rp me pc" "T rp me nonex" "T rp me addr" "T rp me stopped" "T rp me msr" "T rp me chkstop" "T rp me srr0" "T rp me unimpl" "T rp odd session" "T rp odd pc" "T rp odd nonex" "T rp odd addr" "T rp odd stopped" "T rp odd msr" "T rp odd chkstop" "T rp odd srr0" "T rp odd unimpl" "T rp o1m session" "T rp o1m pc" "T rp o1m nonex" "T rp o1m addr" "T rp o1m stopped" "T rp o1m msr" "T rp o1m chkstop" "T rp o1m srr0" "T rp o1m unimpl" "T rp o2 session" "T rp o2 pc" "T rp o2 nonex" "T rp o2 addr" "T rp o2 stopped" "T rp o2 msr" "T rp o2 chkstop" "T rp o2 srr0" "T rp o2 unimpl" "T rp o2m session" "T rp o2m pc" "T rp o2m nonex" "T rp o2m addr" "T rp o2m stopped" "T rp o2m msr" "T rp o2m chkstop" "T rp o2m srr0" "T rp o2m unimpl" "T rp o3 session" "T rp o3 pc" "T rp o3 nonex" "T rp o3 addr" "T rp o3 stopped" "T rp o3 msr" "T rp o3 chkstop" "T rp o3 srr0" "T rp o3 unimpl" "T rp o3m session" "T rp o3m pc" "T rp o3m nonex" "T rp o3m addr" "T rp o3m stopped" "T rp o3m msr" "T rp o3m chkstop" "T rp o3m srr0" "T rp o3m unimpl" "T blr session" "T blr pc" "T blr nonex" "T blr srr0" "T blr msr" "T blr chkstop" "T blr unimpl" "T blr lr" "T blr o1 session" "T blr o1 pc" "T blr o1 nonex" "T blr o1 srr0" "T blr o1 msr" "T blr o1 chkstop" "T blr o1 unimpl" "T blr o1 lr" "T blr o2 session" "T blr o2 pc" "T blr o2 nonex" "T blr o2 srr0" "T blr o2 msr" "T blr o2 chkstop" "T blr o2 unimpl" "T blr o2 lr" "T blr m1 session" "T blr m1 pc" "T blr m1 nonex" "T blr m1 srr0" "T blr m1 msr" "T blr m1 chkstop" "T blr m1 unimpl" "T blr m1 lr" "T blr m2 session" "T blr m2 pc" "T blr m2 nonex" "T blr m2 srr0" "T blr m2 msr" "T blr m2 chkstop" "T blr m2 unimpl" "T blr m2 lr" "T blr m3 session" "T blr m3 pc" "T blr m3 nonex" "T blr m3 srr0" "T blr m3 msr" "T blr m3 chkstop" "T blr m3 unimpl" "T blr m3 lr"; do
+         check "ppc_ifetch row: $v" "$(count "$IFLOG" "^$v  .*ok$")" "1"
+     done
+     ifok=$(count "$IFLOG" " ok$"); ifbad=$(count "$IFLOG" " FAIL$"); ifrun=$((ifok + ifbad))
+     check "ppc_ifetch rows run"   "$ifrun" 249
+     check "ppc_ifetch rows green" "$ifok" 249
+     check "ppc_ifetch rows red"   "$ifbad" 0
+ fi
+ 
```

### staged vs the working copy (what stays uncommitted, and the staged-only number)

2 hunk(s) with #575's block set aside on both sides (kit_qhs.strip575), then that block:

* the title's round number (staged only)
* the block header's round number (staged only)
* not this round's: #575's block, HEAD's committed text equal to the working copy's (working-copy lines 340-374)

## regress/ppc_ifetch_probe.py (new file; only this round's)

Staged = the working copy with the round number re-set.  PROBE_IDENTITY_qhs.md: tree minus docstring, strings kept, equal to the working copy (True), the pre-decision-3 copy (True) and table 12's frozen instrument (True); section U clean with the real checker.

### staged vs the working copy

1 hunk(s):

```
@@ replace  left line 8 (1 lines) -> right line 8 (1 lines)
- THE FIX (#581).  The read-failure arm has four exits and a fallback: (a) read-ahead returns untouched; (b) a fetch whose
+ THE FIX (#582).  The read-failure arm has four exits and a fallback: (a) read-ahead returns untouched; (b) a fetch whose
```

## tools/precommit_check.sh

HEAD md5 538bb143d2b108f10d550bfba2c85076 (SCORE_CLAIMS_MANIFEST=47); staged md5 0150bf2341a494f9c8b5658f7e7a6eed (=48).  The working copy's raises -- qhslowifetch (naming a stale 56-row pin: the gate pins 249), mvme187memcoob, pvrrenderexit -- are not carried; this raise is written fresh against HEAD.

### staged vs HEAD

1 hunk(s):

```
@@ replace  left line 378 (1 lines) -> right line 378 (3 lines)
-     SCORE_CLAIMS_MANIFEST=47
+     #  RAISED 47 -> 48 ON 2026-11-05, DELIBERATELY.  One newly gated probe: ppc_ifetch_probe.py
+     #  (#582 qhslowifetch, pinned UNQUOTED in gate_ppc.sh at 249 rows under the stem ppc_ifetch; its docstring is checked).
+     SCORE_CLAIMS_MANIFEST=48
```

## the four trees and the post-#575 rehearsal (TREES_qhs.txt)

```
est                                      part 1 cpu_ppc_instr.c PASS (== SEC working copy), cpu_ppc.h PASS; part 2 N/A (source tree, no binary); .MUTANT absent; .LANDING575 absent; .LANDINGQHS absent
                                           vs HEAD: qhs X(to_be_translated) L4130 (4->80); cpu_ppc.h: qhs PPC_EXCEPTION_MC insert.  vs staged: == the staged file (updated)
build                                    part 1 cpu_ppc_instr.c PASS (== SEC working copy), cpu_ppc.h PASS; part 2 PASS: binary newer than both (gxemul 11-05 13:46:30; cpu_ppc_instr.c 11-05 13:46:19, cpu_ppc.h 11-04 13:47:23); .MUTANT absent; .LANDING575 absent; .LANDINGQHS absent
                                           vs HEAD: qhs X(to_be_translated) L4130 (4->80); cpu_ppc.h: qhs PPC_EXCEPTION_MC insert.  vs staged: == the staged file (updated)
build-asan                               part 1 cpu_ppc_instr.c PASS (== SEC working copy), cpu_ppc.h PASS; part 2 PASS: binary newer than both (gxemul 11-05 13:47:04; cpu_ppc_instr.c 11-05 13:46:19, cpu_ppc.h 11-04 13:47:23); .MUTANT absent; .LANDING575 absent; .LANDINGQHS absent
                                           vs HEAD: qhs X(to_be_translated) L4130 (4->80); cpu_ppc.h: qhs PPC_EXCEPTION_MC insert.  vs staged: == the staged file (updated)
//wsl.localhost/Gentoo/tmp/gxsec-build   part 1 cpu_ppc_instr.c PASS (== SEC working copy), cpu_ppc.h PASS; part 2 PASS: binary newer than both (gxemul 11-05 13:47:11; cpu_ppc_instr.c 11-05 13:46:19, cpu_ppc.h 11-04 13:47:23); .MUTANT absent; .LANDING575 absent; .LANDINGQHS absent
                                           vs HEAD: qhs X(to_be_translated) L4130 (4->80); cpu_ppc.h: qhs PPC_EXCEPTION_MC insert.  vs staged: == the staged file (updated)
post-#575 rehearsal (HEAD simulated by #575's landing-kit staged files: cpu_ppc_instr.c md5 6efa6781b203, gate_ppc.sh md5 50265c7e9e8a, precommit_check.sh md5 81d10dfc8e95; its CHANGELOG.md -> round #581):
  cpu_ppc_instr.c: attribution against it = qhs; HEAD + the qhs hunk == the working copy byte for byte: True; staged vs the working copy = the four fills only: True -> update_trees_qhs.sh's precondition (every tree == WT_BEFORE) holds once #575 has landed
  gate_ppc.sh: wt_gate_r1.patch on the working copy: already present; the qhs block extracted unchanged: True; staged built from the working copy == staged built from the patched one: True; vs the working copy: the title's round number (staged only); the block header's round number (staged only); not this round's: #575's block, HEAD's committed text equal to the working copy's (working-copy lines 340-374); vs the patched one: the title's round number (staged only); the block header's round number (staged only); not this round's: #575's block, HEAD's committed text equal to the working copy's (working-copy lines 340-374)
  precommit_check.sh: SCORE_CLAIMS_MANIFEST 46 -> 47
TREES_SUMMARY ATTRIBUTED; TREE UPDATE DONE; TREE UPDATE DONE (the working copy and every tree hold the staged file dbd192fbc950)
```
