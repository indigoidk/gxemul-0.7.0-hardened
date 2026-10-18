# #566 -- wiring `ip30_abort_probe.py` into gate 14: pass 2 on the real diff

**Please do not simply ratify.**  Check every sentence of the diff and the draft records against the files and the
receipts; a pass-2 seat on `#565` found four wrong sentences in MY repair wording, and pass 1 of this round found three
in my brief.  The tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` at HEAD 2036a3d5; ignore any other `src/`.  READ-ONLY:
write nothing to any project tree.  The working tree carries this round's edits (section 2) AND other units'
uncommitted lines in other files -- including `tools/pipeline/check_probe_wiring.py`, whose working copy also holds
another unit's MANIFEST lines; the COMMIT copy of that file is HEAD plus exactly the hunks in section 2b.

## 0. Where pass 1 left it, and my dispositions -- say which of these is WRONG

Pass 1: GPT-6 Astra 4 flags, Grok 4.7 7, GLM 5.3 11 (packet-fed).  Fable 5.1 NOT FIRED (owner's hold, 2026-10-17).

| # | finding (seat) | disposition |
|---|---|---|
| A1 | the probe header's CONTRACT is the 27-row instrument's: six announce sites, fourteen latch cells, "THE CLOSURE IS OWED" -- while the same file's THE LATCH-AXIS CLASS CLOSURE section records four sites, ten cells, done (Astra) | TAKEN: a dated note above the CONTRACT (2c); the file's AST, docstring excluded, is identical to HEAD's |
| A2 | the load disclosure must name the false green: a session the poll kills reports `alive' (Astra) | TAKEN and narrowed by reading the probe: rows wanting `alive' or `no' read a stall green; only the write-arm and bit-50 tick sessions carry a `yes' announce row; the two read sessions read green twice, `tick 49' once (2a) |
| A3 | the `ip30_tick_probe.py' comment in the checker still says `dated-exempt in the open' (Astra) | TAKEN (2b) |
| A4 | OUTSTANDING_BUGS' `ip30abortkill' entry says 28 rows, PRE-FIX owed, pass 2 owed (Astra, Grok) | TAKEN: a dated note in place, with the measured 10/33 vs 33/33 pair (2e) |
| A5 | controls missing: a good log under a non-zero status, CONTROL doubled/malformed, DONE doubled, a missing probe file, section R's UNWIRED leg (Astra, Grok) | TAKEN: selftest cases n11-n15 and six section R legs (section 3) |
| G1 | the pin comment says section U governs this gate's comments; no comment line names `ip30_abort', so U checks no prose for it (Grok) | TAKEN (2d) |
| G2 | the STALE result was cited at `gate_arm.sh:1528'; exec_sites records the interpreter line, which moves with every comment edit (Grok) | TAKEN: the records cite no gate line; R_S's final line is in section 3 |
| G3 | the quoted PASS line was truncated before `, 44 witnesses correctly ungated' (Grok) | TAKEN |
| G4 | the pre-fix leg is clause (a) only -- (b) is a reinstatement at each fixed site of the FIXED file (Grok) | TAKEN: relabelled; no kill table holds such a mutant for `#531', so (b) goes to the closure as a question |
| g1 | `count' echoes 0 for an absent file is self-contradictory (GLM) | REJECTED: lib.sh's `count()' opens with `[ -f "$1" ] || { echo 0; return; }' |
| g2 | LOGDIR may be unset at the block (GLM) | REJECTED: lib.sh sets `LOGDIR=${LOGDIR:-/tmp/gxregress}' and exports it; HEAD's gate_arm.sh uses `$LOGDIR/' on 28 lines |
| g3 | a never-terminating probe is unbounded (GLM) | REJECTED: every wait in `session()' is wall-clock bounded, ending in SIGKILL after the 12 s poll |
| g4 | no commit after #531 may have touched dev_sgi_ip30.c (GLM) | CHECKED: `git log 686d179c..HEAD -- src/devices/dev_sgi_ip30.c' is empty |
| g5 | battery or scheduled-task duration caps (GLM) | CHECKED: nightly_check.sh's MAX_AGE_H 176 is verdict age; the task XML has no ExecutionTimeLimit (Astra: Windows' 72 h default) |
| g6 | a device-less build may be owed (GLM) | NOT OWED: the 2026-10-09 ruling accepts an absent or non-emulator binary for a runtime probe (Astra) |
| g7 | "HEAD's checker" misdescribes the runs (GLM) | REJECTED: the cliff and STALE runs used `git show HEAD:', byte-checked (section 3); the four other expiries are COMMITTED entries for another session's probes |
| g8 | the absent leg reds at `need_exec' in the full gate (GLM, Grok) | TAKEN as a record: SKIP in the gate, red only in the extracted block |

**D1 -- close `ip30abortkill` in this commit?**  Astra: yes, once records are reconciled; "#527's separate closure
repaired a forgotten state, it does not require separate closure commits".  Grok: no -- "close it later, in a records
commit of the #527 shape: move the width and counter escapes onto a carrier that survives the close ... and stop the
witness presenting the 21-row pair as the shipping instrument".  GLM: separate, on the #527 precedent.  **Mine: separate.**
**D2 -- edit the probe in this commit?**  Astra: "Qualify the historical contract and state the current one in place".
Grok: "Leaving the file where it is keeps that text out of section U, which is why this wiring commit leaves the probe
unmodified."  **Mine: edit it (records only)** -- the block's comment sends readers to the header's CONTRACT, which said
the closure was owed; a wrong record the round cites is an L4.

## 1. What is still to come before commit
One full gate 14 run, alone, with `PMAX` = a HEAD binary rebuilt in the scratch clone (build/'s binary carries another
session's uncommitted sources); then a confirm pass; then the commit and a hash follow-up.

## 2. The diff

### 2a. regress/gate_arm.sh (working tree vs HEAD)
```diff
diff --git a/regress/gate_arm.sh b/regress/gate_arm.sh
index d0259026..88f7e719 100644
--- a/regress/gate_arm.sh
+++ b/regress/gate_arm.sh
@@ -1507,6 +1507,73 @@ else
     check "sgi_mte rows red"     "$(count "$MTELOG" " FAIL$")" "0"
 fi
 
+#  ---- #566 ip30abortkill (#531, 686d179c): dev_sgi_ip30.c's four guest-reachable abort() calls -- a guest load or
+#  ---- store at 0x0ff10020 or 0x0ff10028, a store to 0x0ff10030, and DEVICE_TICK once a legal imask0 write sets bit
+#  ---- 50 -- have declined with a latched announce since #531.  Its detector shipped with that fix and ran in no gate:
+#  ---- check_probe_wiring.py held it EXEMPT, dated 2026-09-20 and re-dated three times (eec0f4a3 to 09-27, #550's
+#  ---- 04500deb to 10-15, 7b23b785 on 2026-10-16 to 10-30), and HEAD's checker run with --today 2026-10-31 FAILS on it
+#  ---- (measured 2026-10-18).  This block discharges that exemption.  The probe's CONTRACT, its MEASURED ESCAPES and
+#  ---- its DOES NOT CATCH list are in its header; its kill tables are in regress/artifacts/ip30abortkill/.  At depth 0,
+#  ---- so another probe's missing sentinel cannot swallow it.
+#  ----
+#  ---- RUN TIME, about 9.5 minutes: 568 s for the 33 rows on build/gxemul (#550 and #566 each measured it), because every
+#  ---- session that survives waits out the probe's 12 s death poll.  That poll is what stops a slow abort reading as
+#  ---- `alive', so it is not shortened here.  The waits are wall-clock, and a load stall is NOT always a red: a
+#  ---- session the poll kills before its stepped access has run reports `alive', and every row that wants `alive' or
+#  ---- `no' reads it green.  The three write-arm sessions and the bit-50 tick session also score an announce row that
+#  ---- wants `yes', which reds; the `kill 20 rd' and `kill 28 rd' sessions do not -- their `txt' rows want NO announce,
+#  ---- since the read arms decline silently -- so a stalled read session reads GREEN twice on a build that would have
+#  ---- aborted, and a stalled `tick 49' session reads green alone.  gate_arm.sh runs in the weekly battery, alone,
+#  ---- and as an attended targeted gate -- never per commit.
+#  ----
+#  ---- Run from its artifacts path, as gate_sh_rounding.sh runs gdrom_pio_null_probe.py; a missing file fails the parse
+#  ---- check below -- a FAIL, never a SKIP.
+IP30LOG=$LOGDIR/ip30_abort.log
+ip30rc=0
+python3 -u artifacts/ip30abortkill/ip30_abort_probe.py "$PMAX" gate > "$IP30LOG" 2>&1 || ip30rc=$?
+
+#  PARSE BEFORE SCORE: exactly one well-formed RESULT, CONTROL and DONE line.  A crash, a killed run or a missing file
+#  leaves none and reds here.
+if [ "$(grep -c '^IP30ABORT_RESULT=' "$IP30LOG")" != "1" ] ||
+   ! grep -Eq '^IP30ABORT_RESULT=(0|[1-9][0-9]*)/(0|[1-9][0-9]*)$' "$IP30LOG" ||
+   [ "$(grep -c '^IP30ABORT_CONTROL=' "$IP30LOG")" != "1" ] ||
+   ! grep -Eq '^IP30ABORT_CONTROL=(OK|DEAD)$' "$IP30LOG" ||
+   [ "$(grep -cx 'IP30ABORT_DONE' "$IP30LOG")" != "1" ]; then
+    note "ip30_abort probe produced no unique, valid completion record; last lines follow"
+    tail -5 "$IP30LOG" | sed 's/^/       /'
+    check "ip30_abort probe output parses" "no" "yes"
+else
+    check "ip30_abort probe output parses" "yes" "yes"
+    grep -E '^  .* got=.* want=.* FAIL  ' "$IP30LOG" | sed 's/^/       /'
+    #  CONTROLS: `live' (a RAM plant returns through a guest load) and `devsig' (0x20 answers 0x80010000, which RAM
+    #  cannot).  A DEAD vehicle prints a zero-row RESULT and rows with no status token, so every row check below reds too.
+    check "ip30_abort controls" "$(sed -n 's/^IP30ABORT_CONTROL=//p' "$IP30LOG")" "OK"
+    check "ip30_abort probe exit status" "$ip30rc" "0"
+
+    #  EVERY ROW BY NAME, EXACTLY ONCE -- identity and uniqueness, which the counts below cannot give.  The probe prints
+    #  `  %-12s got=%-12s want=%-12s <ok|FAIL>  <note>': the status token is NOT at the end of the line, so ` ok$'
+    #  matches nothing here, and six names (`kill 20 rd txt', `isr 20 rd val', ...) are longer than their 12-column
+    #  field.  So a row is matched by position -- its name, the got= and want= tokens (no value carries a space), then
+    #  the status and its two trailing spaces -- and `^  <name>  *got=' cannot match a longer name beginning with this
+    #  one (`kill 20 rd' / `kill 20 rd txt', `xbit rev' / `xbit rev2').  count() is plain grep: every `*' is BRE.
+    for v in "live" "devsig" "acc 18" "acc 30 rd" "acc 20000" "acc 30000" "acc imask" "kill 20 rd" "kill 20 rd txt" "kill 28 rd" "kill 28 rd txt" "kill 30 wr" "kill 30 txt" "tick 50" "tick 50 txt" "tick 49" "kill 20 wr" "kill 20 wr txt" "kill 28 wr" "kill 28 wr txt" "isr keep" "isr clr" "isr drop 30" "xbit isr" "xbit tick" "latch 1x" "isr 20 rd val" "isr 28 rd val" "latch 28wr" "latch 30wr" "latch tick" "xbit rev" "xbit rev2"; do
+        check "ip30_abort row: $v" "$(count "$IP30LOG" "^  $v  *got=[^ ]*  *want=[^ ]*  *ok  ")" "1"
+    done
+
+    #  DENOMINATORS, pinned to LITERALS: `rows run' is the probe's own count (RESULT's), `rows emitted' the row lines it
+    #  printed -- two, because one cannot tell a LOST row from a failing one.  `[^=]*' stops at the first `=', which in a
+    #  row line is got='s.  All 33 green on build/gxemul, measured before these pins were written
+    #  (regress/artifacts/ip30abortkill/gatewire_20261018/).
+    ip30res=$(sed -n 's/^IP30ABORT_RESULT=//p' "$IP30LOG")
+    ip30ok=$(count "$IP30LOG" '^  [^=]* got=[^ ]*  *want=[^ ]*  *ok  ')
+    ip30bad=$(count "$IP30LOG" '^  [^=]* got=[^ ]*  *want=[^ ]*  *FAIL  ')
+    check "ip30_abort rows run"     "${ip30res#*/}" 33
+    check "ip30_abort rows correct" "${ip30res%/*}" "33"
+    check "ip30_abort rows emitted" "$((ip30ok + ip30bad))" "33"
+    check "ip30_abort rows green"   "$ip30ok" "33"
+    check "ip30_abort rows red"     "$ip30bad" "0"
+fi
+
 #  ---- *** MOVED OUT ONE NESTING LEVEL, 2026-08-31.  It was pasted INSIDE the
 #  ---- sgi_re_width probe's success branch, so if THAT probe missed its sentinel this
 #  ---- block was never invoked at all -- 28 rows, three denominators and its own
```
### 2b. tools/pipeline/check_probe_wiring.py (HEAD vs the COMMIT copy)
```diff
diff --git a/tools/pipeline/check_probe_wiring.py (HEAD) b/tools/pipeline/check_probe_wiring.py (commit copy)
index 22a1c55e..9282149c 100644
--- a/tools/pipeline/check_probe_wiring.py (HEAD)
+++ b/tools/pipeline/check_probe_wiring.py (commit copy)
@@ -663,11 +663,14 @@ MANIFEST = {
     #  TURNED THIS CHECKER RED -- the same shape as #532's stage gates: completing the
     #  record is what made the gap visible.  That is the manifest working as designed (an
     #  unlisted file is RED so a new detector cannot arrive unnoticed), not a defect. ***
+    #  [#566, 2026-10-18] WIRED: gate_arm.sh (gate 14) runs it and scores every row by name, with its run,
+    #  correct, emitted, green and red counts pinned; its EXEMPT entry is DISCHARGED below.
     "artifacts/ip30abortkill/ip30_abort_probe.py":
         (CLASS_DETECTOR, "#531 ip30abortkill: four guest-reachable abort() calls in dev_sgi_ip30.c. "
                          "33 rows, base 33/33, GREEN once the fix is in -- a DETECTOR by this file's own "
                          "definition at the top, and labelled one rather than filed as a `witness' to "
-                         "dodge the gate requirement.  *** RUNS IN NO GATE: see EXEMPT. ***"),
+                         "dodge the gate requirement.  *** RAN IN NO GATE until #566 (2026-10-18) wired it into "
+                         "gate_arm.sh; its EXEMPT entry is discharged. ***"),
     "artifacts/ip30abortkill/ip30_abort_probe.18row_20260917.frozen.py":
         (CLASS_TOOL, "the FROZEN 18-row instrument table 1 ran against"),
     "artifacts/ip30abortkill/opusF2_20260918/probe.frozen.py":
@@ -706,7 +709,8 @@ MANIFEST = {
     #  KNOWN DODGE IN THIS VERY FILE. ***  The flagship seat found ungated DETECTORS relabelled
     #  WITNESS here so that the checker would then verify they are ungated -- a check that
     #  cannot fail.  This is not that: #531's shipped detector is `ip30_abort_probe.py` above,
-    #  classed DETECTOR and dated-exempt in the open.  THIS file is a REACHABILITY measurement
+    #  classed DETECTOR and dated-exempt in the open [#566: until it was wired into gate_arm.sh on
+    #  2026-10-18; its EXEMPT entry is discharged].  THIS file is a REACHABILITY measurement
     #  -- its own docstring calls itself an "ip30 TICK-ROW BUILDABILITY MEASUREMENT" and asks
     #  whether the FOURTH abort(), inside DEVICE_TICK, can be reached from a STEPPING probe at
     #  all.  It answered a disagreement between two seats by combining them, and the answer is
@@ -3176,6 +3180,11 @@ EXEMPT = {
     #  after three re-dates by owner ruling (2026-09-18 in eec0f4a3, 2026-09-24, 2026-10-09), and would have
     #  refused every commit from 2026-10-23 (`d < today').
     #  Deleted in the SAME edit as the wiring, for the same reason.
+    #  artifacts/ip30abortkill/ip30_abort_probe.py's exemption is DISCHARGED, 2026-10-18 (#566) -- wired into
+    #  gate_arm.sh beside the sgi probes, from its artifacts path, every row scored by name.  It was dated
+    #  2026-09-20 with #531 and re-dated three times (eec0f4a3 to 2026-09-27, 04500deb to 2026-10-15, 7b23b785
+    #  to 2026-10-30), and would have refused every commit from 2026-10-31 (`d < today').
+    #  Deleted in the SAME edit as the wiring, for the same reason.
     #  Both #494 probes are TWO-LEG DIFFERENTIALS: they take a PRE-FIX binary and
     #  a post-fix one and compare.  No gate builds a second leg, so wiring them is
     #  a change to the instrument -- a single-leg mode asserting only the fix-side
@@ -3236,34 +3245,6 @@ EXEMPT = {
                                     "no gate runs an Alpha guest session (gate 9 only "
                                     "constructs them); gate_crossfamily.sh "
                                     "is the named home, filed to wiringcliff with #518/#520"),
-    #  #531's detector, on the SAME footing as #518/#520/#530 (it took their date too, so the
-    #  cliff stayed one date, until #550 dispersed the block).  This comment said: "`grep -ln
-    #  "E sgi|-e ip30" gate_*.sh` matches ONLY gate_asan_sweep.sh ... no gate in this tree that could
-    #  host it today."  CORRECTED by #550: as written that grep matches nothing (`|' is literal in a
-    #  basic regex), and as an extended regex it matches one line, gate 9's #450 row, which constructs
-    #  ip12, ip28, ip30, ip32 and ip35 on /dev/null and runs no guest session; guest-session probes exec
-    #  the machine themselves, and gate_arm.sh already runs seven cold-debugger probes of this shape
-    #  (grep -cE '^python3 sgi_[a-z0-9_]+_probe[.]py' regress/gate_arm.sh), each naming `-e ip32' in its
-    #  own exec line, so a home exists.  *** NOT classified `witness' to escape the requirement: the flagship seat found
-    #  that exact dodge elsewhere in this manifest -- an ungated DETECTOR relabelled WITNESS,
-    #  after which the checker verifies it is ungated -- and named it a check that cannot
-    #  fail.  This entry is the honest form: DETECTOR, ungated, dated, and filed. ***
-    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): gate_arm.sh hosts
-    #  seven sgi cold-debugger probes of this shape; 33/33 on build/gxemul in 568 s (the rows:
-    #  regress/artifacts/exemptredate_20260925/opus550_measured_p2/p1_runs/; the time, from the logs'
-    #  mtimes: keep_p1_logs.out one directory up), because each surviving
-    #  session waits out the 12 s death poll -- a long gate guest until that window shrinks without
-    #  reading a delayed abort as alive.
-    #  Re-dated 2026-10-15 -> 2026-10-30 on 2026-10-16, in its own commit, by a four-seat ruling (Fable 5.1, GPT-6
-    #  Astra, Grok 4.7 and GLM 5.3 answered; three ruled re-date now, Astra ruled wire now): it came due with no gate
-    #  running it and refused every commit in both sessions (regress/artifacts/adj_20261016/wiringcliff/).  A re-date is
-    #  not a discharge: the wiring is owed by wiringcliff.  #550 measured the probe at 568 s standalone for its 33 rows
-    #  (regress/artifacts/exemptredate_20260925/opus550_measured_p2/keep_p1_logs.out); gate_arm.sh runs in the weekly
-    #  battery and as an attended targeted gate, never per commit.
-    "artifacts/ip30abortkill/ip30_abort_probe.py":
-                                   ("2026-10-30",
-                                    "no gate runs an SGI IP30 guest session (gate_asan_sweep.sh "
-                                    "constructs only); filed to wiringcliff with #518/#520/#530"),
 }
 
 DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
```
### 2c. regress/artifacts/ip30abortkill/ip30_abort_probe.py (working tree vs HEAD)
```diff
diff --git a/regress/artifacts/ip30abortkill/ip30_abort_probe.py b/regress/artifacts/ip30abortkill/ip30_abort_probe.py
index 30a45f6e..3c552ed9 100644
--- a/regress/artifacts/ip30abortkill/ip30_abort_probe.py
+++ b/regress/artifacts/ip30abortkill/ip30_abort_probe.py
@@ -11,6 +11,28 @@ sentence above said "not a shipped detector" long after two kill tables had made
 corrected 2026-09-18. ***  8/21 pre-fix -> 21/21 post-fix on one instrument, then 27 rows after
 the pass-2 class closure.
 
+================================================================================
+[#566, 2026-10-18 -- a records correction; the CONTRACT below is kept as it was written on
+2026-09-18, for the 27-row instrument.  The file's later sections were updated and this one
+was not.]  The probe that ships has 33 rows, and five statements below are no longer true:
+  * the F13 silent-decline repair made both READ arms (0x10020, 0x10028) decline WITHOUT an
+    announce, so there are FOUR announce sites, not six, and `kill 20 rd txt' / `kill 28 rd
+    txt' now pin the SILENCE (want `no');
+  * `latch 1x' was re-aimed onto the two WRITE arms (0x10020-WR, then 0x10028-WR) when the
+    read arms went silent;
+  * the latch axis is {4 announce sites} x {announce fires, latch sets} + {2 collision
+    directions} = TEN cells, all rowed (THE LATCH-AXIS CLASS CLOSURE, below);
+  * "THE CLOSURE IS OWED" was DONE in-round: `latch 1x' (0x10020-WR), `latch 28wr', `latch
+    30wr', `latch tick' (ME_nolatchsettick) and `xbit rev' (MA_assign20wr) -- kill table 4,
+    32 rows -- and `xbit rev2' after V2_assigntick (MD's shape) scored 32/32 there; kill table
+    5 then: base 33/33, V1_assign20wr 32/33, V2_assigntick 32/33 (regress/artifacts/
+    ip30abortkill/killtable4_20260918/, killtable5_20260918/).  MF's cell, a latch set on the
+    0x10028 READ, no longer exists: that arm no longer announces;
+  * the pre-fix red is no longer `13 rows': on this instrument the pre-fix build scores 10/33
+    (#566's prefix leg, regress/artifacts/ip30abortkill/gatewire_20261018/legs/probe_prefix.log).
+V7_nocounter (MH's shape, 32/32 in table 4) and the WIDTH axis (V8_len4, 33/33 in table 5)
+remain DISCLOSED, as DOES NOT CATCH says.  Since #566 this probe runs in gate 14
+(regress/gate_arm.sh).
 ================================================================================
 THE CONTRACT -- vacuity-floor clause (e).  A detector that says what it catches is
 FALSIFIABLE; one that claims completeness is not.  Every CATCH below has a MEASURED
```
### 2d. tools/precommit_check.sh
```diff
diff --git a/tools/precommit_check.sh b/tools/precommit_check.sh
index 29749a96..8ab4e020 100644
--- a/tools/precommit_check.sh
+++ b/tools/precommit_check.sh
@@ -347,7 +347,12 @@ elif out=$(python "$SCORECHK" 2>&1); then
 	#  (#562, pinned UNQUOTED in gate_arm.sh at 47 rows).
 	#  RAISED 33 -> 34 ON 2026-10-18, DELIBERATELY.  One newly gated probe: ppc_rldicl_probe.py
 	#  (#565, pinned UNQUOTED in gate_ppc.sh at 24 rows).
-	SCORE_CLAIMS_MANIFEST=34
+	#  RAISED 34 -> 35 ON 2026-10-18, DELIBERATELY.  One newly gated probe:
+	#  artifacts/ip30abortkill/ip30_abort_probe.py (#566, pinned UNQUOTED in gate_arm.sh at 33 rows
+	#  under the stem ip30_abort).  The checker reads only `#' lines that contain the stem, and only a
+	#  docstring at regress/<stem>_probe.py or regress/<stem>.py; no comment line names ip30_abort and
+	#  the probe lives under artifacts/, so for this pin it checks no prose -- only the pin is counted.
+	SCORE_CLAIMS_MANIFEST=35
 	_spinned=$(printf '%s\n' "$out" | sed -n 's/^SCORE_CLAIMS_PINNED=//p')
 	if [ -z "$_spinned" ]; then
 		bad "check_score_claims printed no SCORE_CLAIMS_PINNED line -- the count cannot be pinned"
```
### 2e. OUTSTANDING_BUGS.md
```diff
diff --git a/OUTSTANDING_BUGS.md b/OUTSTANDING_BUGS.md
index 53b2d078..91df8af2 100644
--- a/OUTSTANDING_BUGS.md
+++ b/OUTSTANDING_BUGS.md
@@ -21615,6 +21615,8 @@ the pile-up formed.
 > *** THE SHIPPED INSTRUMENT IS NOW **28 ROWS**, NOT 21, AND THE WITNESS PAIR ABOVE WAS NOT RE-MEASURED ON IT.  Stated rather than smoothed. ***  The instrument grew twice AFTER the witness pair was taken -- 21 -> 27 at the pass-2 class closure, 27 -> 28 at the §F2 sibling-parity repair -- and every added row exists for DETECTOR STRENGTH, not to witness the defect.  The pair is therefore valid for what it claims (the fix changes the behaviour, measured on one instrument, pre and post) and is NOT a claim about the instrument that ships.
 >
 > **The shipped instrument's POST-FIX figure IS measured: 28/28** (`killtable3_20260918/base.raw`, sentinel `IP30ABORT_DONE`).  What is not measured is its PRE-FIX counterpart.  **OWED: one clone build to take PRE-FIX at 28 rows**, which would give a matched pair on the instrument that actually ships.  Deliberately not run while a measuring seat is in flight.  *(The 18-row pair 11/18 -> 18/18 is SUPERSEDED: pass 2 found four defects, and repairing them grew the instrument.  The re-pin's own order proof stays on the 18-row form by design.)*
+>
+> *** [#566, 2026-10-18] THE SHIPPED INSTRUMENT IS **33 ROWS**, AND ITS PRE-FIX COUNTERPART IS NOW MEASURED ON IT. ***  The latch-axis class closure took it 28 -> 32 (kill table 4) -> 33 (`xbit rev2`, kill table 5, base 33/33).  `#566` rebuilt HEAD in a scratch clone with `dev_sgi_ip30.c` set to `686d179c^`'s (all four `abort()` calls back): **PRE-FIX 10/33, POST-FIX 33/33 on the one 33-row instrument** (`regress/artifacts/ip30abortkill/gatewire_20261018/legs/`) -- the matched pair owed above.  The 8/21 -> 21/21 pair is unchanged: a 21-row witness, not a claim about the file that ships.  The "Still owed before close: panel pass 2" line below was discharged on 2026-09-18 by `#531`'s own pass 2, its F2 adjudication (fable5, roster 9/9) and kill tables 3-5.
 
 Four guest-reachable `abort()` calls in `dev_sgi_ip30.c` on the advertised `-E sgi -e ip30`.
 **Three `exit(` sweeps of this queue walked past all four**, because `abort()` contains no
@@ -24947,3 +24949,16 @@ Fable 5.1, GPT-6 Astra, Grok 4.7).  Each row's ledger `state_note` carries its s
   the Rc=1-only insertion skip, `CENSUS_SHRINK`, `R_NOGUARD`), moved here from `ppcrldimimask`, which the 2026-10-02
   disposition had made their carrier.  Coverage debt and named measurements; none a floor breach.
 * **`ppcgateimageskip` CLOSED as discharged** -- the rlwimi, rldimi and rldicl blocks run before `need_file` in gate 13.
+
+### 2026-10-18 -- `#566`: `ip30_abort_probe.py` wired into gate 14 (`wiringcliff` stays open; `ip30abortkill` stays in work)
+
+* **`wiringcliff` (MED, in work)** -- `#566` wired `regress/artifacts/ip30abortkill/ip30_abort_probe.py` into gate 14
+  (`regress/gate_arm.sh`, 41 checks: one parse check, controls, exit status, the 33 rows by name, five pinned counts) and
+  deleted its 2026-10-30 exemption.  Next due: `alpha_tbi_probe.py` 2026-10-22 and the three `lca_*` probes 10-23 / 10-26
+  / 10-27 (the other session's), then the four `wdc_*` probes 11-05 .. 12-03.
+* **`ip30abortkill` (HIGH, in work)** -- its detector now runs in gate 14, and the pre-fix counterpart on the shipped
+  33-row instrument is measured (10/33 against 33/33).  Still owed before it closes, in a records commit of `#527`'s
+  shape: a carrier row for the two measured escapes (`V7_nocounter` 32/32 in kill table 4; the width axis, `V8_len4`
+  33/33 in kill table 5), a witness field naming the 33-row pair rather than the 21-row one, and an answer to whether
+  `#531`'s clause (b) -- `abort()` re-inserted at each fixed site of the FIXED file -- was ever measured (no kill table
+  holds such a mutant; `#566`'s pre-fix leg is clause (a)).
```
### 2f. The CHANGELOG block (draft; its two PENDING markers are filled after the gate run and the passes)
```
# `#566` (wiringcliff): `regress/artifacts/ip30abortkill/ip30_abort_probe.py` is wired into gate 14 thirteen days before its exemption would refuse every commit -- 41 checks score all 33 rows by name; floor clauses (a) and (c) measured through the block; the probe's stale CONTRACT and the bug file's stale `ip30abortkill` entry corrected

**The cliff.**  Section R (`tools/pipeline/check_probe_wiring.py`) held `#531`'s detector for four guest-reachable
`abort()` calls in `src/devices/dev_sgi_ip30.c` (`686d179c`) in its EXEMPT table: dated 2026-09-20 with `#531`, then
re-dated three times -- `eec0f4a3` to 2026-09-27, `04500deb` (`#550`) to 2026-10-15, `7b23b785` (2026-10-16, a four-seat
ruling, GPT-6 Astra dissenting "wire now") to 2026-10-30.  HEAD's checker run with `--today 2026-10-31` names it
EXPIRED.  Witness `harness:` -- the round's subject is the test apparatus.

**What ships.**
* `regress/gate_arm.sh` -- a block at depth 0 after the `#564` `sgi_mte_decline` block, running the probe from its
  artifacts path (as `gate_sh_rounding.sh` runs `gdrom_pio_null_probe.py`): PARSE BEFORE SCORE -- exactly one
  well-formed `IP30ABORT_RESULT=`, `IP30ABORT_CONTROL=` and `IP30ABORT_DONE` line, so a crash, a killed run or a
  missing probe file is a FAIL, never a SKIP; then CONTROL `OK`, the probe's exit status 0, EVERY row by name exactly
  once (`^  NAME  *got=[^ ]*  *want=[^ ]*  *ok  ` -- the status token sits mid-line, before the note, so gate 14's usual
  ` ok$` would match nothing; six names overflow their 12-column field), and five counts pinned to literals: rows run
  (the RESULT denominator) 33, rows correct 33, rows emitted 33, green 33, red 0.  41 checks when green.  Its comment
  discloses the cost -- about 9.5 minutes, each surviving session waiting out the probe's 12 s death poll -- and that a
  load stall is not always a red: a session the poll kills before its stepped access has run reports `alive', every
  row wanting `alive' or `no' reads it green, and only the write-arm and bit-50 tick sessions carry an announce row
  that reds -- a stalled `kill 20 rd' or `kill 28 rd' session reads green twice, a stalled `tick 49' session once.
* `tools/pipeline/check_probe_wiring.py` -- the EXEMPT tuple and its 24-line comment deleted; a dated DISCHARGED note
  beside `#565`'s; the MANIFEST entry's own `*** RUNS IN NO GATE: see EXEMPT. ***` corrected, and the
  `ip30_tick_probe.py` comment's `dated-exempt in the open` qualified (GPT-6 Astra).
* `tools/precommit_check.sh` -- `SCORE_CLAIMS_MANIFEST` 34 -> 35, for the new `ip30_abort rows run ... 33` pin.  Section U
  checks no prose for this pin: no comment line names the stem, and the probe has no `regress/<stem>_probe.py` (Grok 4.7
  corrected the first draft of that comment).
* `regress/artifacts/ip30abortkill/ip30_abort_probe.py` -- records only: a dated note above its CONTRACT, which was the
  27-row instrument's (six announce sites, fourteen latch cells, "THE CLOSURE IS OWED") while the file's own later
  sections record the finished 33-row closure.  Its AST, docstring excluded, is identical to HEAD's.
* `OUTSTANDING_BUGS.md` -- the `ip30abortkill` entry's "28 ROWS ... PRE-FIX owed ... pass 2 owed" corrected in place, and
  a `#566` section.

**Measured** (all under `regress/artifacts/ip30abortkill/gatewire_20261018/`).
* Gate 14, alone: [PENDING -- the full run, before commit].
* The probe through the block's own scoring text, in a scratch clone of `build/` with the other session's five
  uncommitted sources set back to HEAD (`legs/LEGS.out`): HEAD rebuilt 33/33, 41 of 41 green, 567 s; HEAD with
  `dev_sgi_ip30.c` set to `686d179c^`'s -- clause (a), all four `abort()` calls back -- 10/33 and 26 checks red, every
  abort site among them (`kill 20 rd`, `kill 28 rd`, `kill 30 wr`, `tick 50`, `kill 20 wr`, `kill 28 wr` read DEAD);
  `/nonexistent/gxemul` and `/bin/true` -- clause (c), the null media for a runtime probe -- CONTROL=DEAD and 38 checks
  red.  In the full gate an absent binary stops at `need_exec` first, a SKIP; `/bin/true` reaches the block.
* The scoring text against doctored copies of the 33/33 log (`selftest/SELFTEST.out`): 15 cases, each red where it
  should be -- a row turned FAIL, lost, duplicated or renamed; a DEAD vehicle; an empty log; DONE removed or doubled;
  RESULT doubled, contradicted or shrunk; CONTROL doubled or malformed; the good log under a non-zero exit status; and a
  REAL invocation of a probe file that does not exist (python3 exits 2).
* Section R (`controls/R_CONTROLS.out`): the commit checker with the wired gate passes (77/85 detectors run by a gate,
  8 dated-exempt, 44 witnesses correctly ungated); HEAD's checker reports STALE EXEMPTION; the exec line commented out
  reports UNWIRED DETECTOR; HEAD's checker with the gate unwired passes today and at `--today 2026-10-31` reports the
  probe EXPIRED.  Section U: `SCORE_CLAIMS_PINNED=35`, PASS, 13 of 35 stems with a docstring checked.

**Panel.**  Pass 1 (`brief_p1_body.md`): GPT-6 Astra 4 flags, Grok 4.7 7, GLM 5.3 11 (packet-fed; most "not settleable
from the packet", settled here by reading `lib.sh`, `git log` and the checker).  Taken: the stall disclosure (Astra), the
stale CONTRACT and bug-file entry and the tick-probe comment (Astra, Grok), the U comment and the cited checker lines
(Grok), the pre-fix leg is clause (a) only (Grok), and five more doctored cases and the section R legs (Astra, Grok).
Fable 5.1 NOT FIRED (held by the owner's 2026-10-17 directive).  [PENDING: pass 2 and its F2.]

**Not done here, and why.**  `ip30abortkill` stays `in work`: it closes in a records commit of `#527`'s shape, with a
carrier row for its two measured escapes (`V7_nocounter`, 32/32 in kill table 4; the width axis `V8_len4`, 33/33 in kill
table 5) and a witness naming the 33-row pair (Grok 4.7 and GLM 5.3; GPT-6 Astra would close here).  `#531`'s clause (b)
-- `abort()` re-inserted at each fixed site of the FIXED file -- is held by no kill table; that question goes to the
closure.  The stall false-green is disclosed, not repaired: shortening the poll is what reads a slow abort as alive.
```

## 3. Receipts (all under regress/artifacts/ip30abortkill/gatewire_20261018/)

legs/LEGS.out:
```
LEGS566 start 2026-10-18 11:08:02
probe md5 5bf04f2de35af34d517bd286499d5b98  gate_arm.sh md5 1081135176b00493e301c15737b995cf
set to HEAD: src/cpus/cpu_alpha_palcode.c
set to HEAD: src/devices/dev_lca.c
set to HEAD: src/devices/dev_pcc2.c
set to HEAD: src/devices/dev_sh4.c
set to HEAD: src/include/thirdparty/mvme_pcctworeg.h
clone dev_sgi_ip30.c == HEAD
make rc=0 (base)
binary fresh (base): 11:08:38 6159736
probe base: rc=0 567s  IP30ABORT_RESULT=33/33  last=[IP30ABORT_DONE]
clone dev_sgi_ip30.c := 686d179c^ (the upstream import): 4 abort() calls
make rc=0 (prefix)
binary fresh (prefix): 11:18:35 6159736
probe prefix: rc=0 272s  IP30ABORT_RESULT=10/33  last=[IP30ABORT_DONE]
probe absent: rc=0 0s  IP30ABORT_RESULT=0/0  last=[IP30ABORT_DONE]
probe nonemu: rc=0 0s  IP30ABORT_RESULT=0/0  last=[IP30ABORT_DONE]
scoring text: 42 lines, md5 bc71bb535db4692030c6328dd97986e6
LEG base    gate checks=41  fails=0   GREEN as required
LEG prefix  gate checks=41  fails=26  RED   as required
      red: [ip30_abort row: kill 20 rd got=0] [ip30_abort row: kill 28 rd got=0] [ip30_abort row: kill 30 wr got=0] [ip30_abort row: kill 30 txt got=0] [ip30_abort row: tick 50 got=0] [ip30_abort row: tick 50 txt got=0] [ip30_abort row: kill 20 wr got=0] [ip30_abort row: kill 20 wr txt got=0] [ip30_abort row: kill 28 wr got=0] [ip30_abort row: kill 28 wr txt got=0] [ip30_abort row: isr keep got=0] [ip30_abo
LEG absent  gate checks=41  fails=38  RED   as required
      red: [ip30_abort controls got=DEAD] [ip30_abort row: live got=0] [ip30_abort row: devsig got=0] [ip30_abort row: acc 18 got=0] [ip30_abort row: acc 30 rd got=0] [ip30_abort row: acc 20000 got=0] [ip30_abort row: acc 30000 got=0] [ip30_abort row: acc imask got=0] [ip30_abort row: kill 20 rd got=0] [ip30_abort row: kill 20 rd txt got=0] [ip30_abort row: kill 28 rd got=0] [ip30_abort row: kill 28 rd txt 
LEG nonemu  gate checks=41  fails=38  RED   as required
      red: [ip30_abort controls got=DEAD] [ip30_abort row: live got=0] [ip30_abort row: devsig got=0] [ip30_abort row: acc 18 got=0] [ip30_abort row: acc 30 rd got=0] [ip30_abort row: acc 20000 got=0] [ip30_abort row: acc 30000 got=0] [ip30_abort row: acc imask got=0] [ip30_abort row: kill 20 rd got=0] [ip30_abort row: kill 20 rd txt got=0] [ip30_abort row: kill 28 rd got=0] [ip30_abort row: kill 28 rd txt 
clone left at /tmp/gx566 with its .MUTANT sentinel (scratch; build/ untouched)
LEGS566 end 2026-10-18 11:23:09
LEGS566_DONE
```
The pre-fix leg's rows (legs/probe_prefix.log), status and got:
```
ok    live            got=0x11223344 want=0x11223344
ok    devsig          got=0xffffffff80010000 want=0xffffffff80010000
ok    acc 18          got=0xffffffffdeadbeef want=0xffffffffdeadbeef
ok    acc 30 rd       got=alive want=alive
ok    acc 20000       got=stored+N*1000 want=stored+N*1000
ok    acc 30000       got=0x5678 want=0x5678
ok    acc imask       got=0x40000 want=0x40000
FAIL  kill 20 rd      got=DEAD want=alive
ok    kill 20 rd txt  got=no want=no
FAIL  kill 28 rd      got=DEAD want=alive
ok    kill 28 rd txt  got=no want=no
FAIL  kill 30 wr      got=DEAD want=alive
FAIL  kill 30 txt     got=no want=yes
FAIL  tick 50         got=DEAD want=alive
FAIL  tick 50 txt     got=no want=yes
ok    tick 49         got=no want=no
FAIL  kill 20 wr      got=DEAD want=alive
FAIL  kill 20 wr txt  got=no want=yes
FAIL  kill 28 wr      got=DEAD want=alive
FAIL  kill 28 wr txt  got=no want=yes
FAIL  isr keep        got=died want=0x5a5a
FAIL  isr clr         got=died want=0x5050
FAIL  isr drop 30     got=died want=0x5a5a
FAIL  xbit isr        got=died want=1
FAIL  xbit tick       got=died want=1
FAIL  latch 1x        got=died want=1
FAIL  isr 20 rd val   got=died want=0x0
FAIL  isr 28 rd val   got=died want=0x0
FAIL  latch 28wr      got=died want=1
FAIL  latch 30wr      got=died want=1
FAIL  latch tick      got=died want=1
FAIL  xbit rev        got=died want=1
FAIL  xbit rev2       got=died want=1
```
selftest/SELFTEST.out:
```
scoring text: 42 lines, md5 bc71bb535db4692030c6328dd97986e6
n15: python3 on a missing probe file exited 2; log: /usr/lib/python-exec/python3.13/python3: can't open file '/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/ip
good            rc=0  checks=41  fails=0   GREEN as-expected
n1_onefail      rc=0  checks=41  fails=3   RED   as-expected
      red: [ip30_abort row: kill 30 wr got=0] [ip30_abort rows green got=32] [ip30_abort rows red got=1]
n2_rowlost      rc=0  checks=41  fails=3   RED   as-expected
      red: [ip30_abort row: tick 49 got=0] [ip30_abort rows emitted got=32] [ip30_abort rows green got=32]
n3_rowdup       rc=0  checks=41  fails=2   RED   as-expected
      red: [ip30_abort row: tick 50 got=2] [ip30_abort row: tick 49 got=0]
n4_dead         rc=0  checks=41  fails=38  RED   as-expected
      red: [ip30_abort controls got=DEAD] [ip30_abort row: live got=0] [ip30_abort row: devsig got=0] [ip30_abort row: acc 18 got=0] [ip30_abort row: acc 30 rd got=0] [ip30_abort row: acc 20000 got=0] [ip30_abort row: acc 30000 go
n5_empty        rc=0  checks=1   fails=1   RED   as-expected
      red: [ip30_abort probe output parses got=no]
n6_nodone       rc=0  checks=1   fails=1   RED   as-expected
      red: [ip30_abort probe output parses got=no]
n7_tworesult    rc=0  checks=1   fails=1   RED   as-expected
      red: [ip30_abort probe output parses got=no]
n8_contra       rc=0  checks=41  fails=3   RED   as-expected
      red: [ip30_abort row: latch tick got=0] [ip30_abort rows green got=32] [ip30_abort rows red got=1]
n9_shrunk       rc=0  checks=41  fails=5   RED   as-expected
      red: [ip30_abort row: xbit rev2 got=0] [ip30_abort rows run got=32] [ip30_abort rows correct got=32] [ip30_abort rows emitted got=32] [ip30_abort rows green got=32]
n10_renamed     rc=0  checks=41  fails=1   RED   as-expected
      red: [ip30_abort row: acc imask got=0]
n11_goodrc1     rc=1  checks=41  fails=1   RED   as-expected
      red: [ip30_abort probe exit status got=1]
n12_twocontrol  rc=0  checks=1   fails=1   RED   as-expected
      red: [ip30_abort probe output parses got=no]
n13_badcontrol  rc=0  checks=1   fails=1   RED   as-expected
      red: [ip30_abort probe output parses got=no]
n14_twodone     rc=0  checks=1   fails=1   RED   as-expected
      red: [ip30_abort probe output parses got=no]
n15_noprobe     rc=2  checks=1   fails=1   RED   as-expected
      red: [ip30_abort probe output parses got=no]
SCORE_SELFTEST_DONE
```
controls/R_CONTROLS.out:
```
commit checker md5 07b31a6ce4e19c745b2804b02f284a78; HEAD checker md5 175bf266dc076c17c14f061fffba64cd
HEAD checker == git show HEAD:
G    rc=0  last: PROBEWIRING_PASS  77/85 detectors run by a gate, 8 dated-exempt, 44 witnesses correctly ungated
S    rc=1  last: PROBEWIRING_FAIL  1 problem(s); 77/85 detectors run by a gate, 8 dated-exempt
        18:  FAIL  STALE EXEMPTION  artifacts/ip30abortkill/ip30_abort_probe.py is RUN by gate_arm.sh:1532 and still carries an exemption dated 2026-10-30 -- the debt is paid, delete the line
G1   rc=1  last: PROBEWIRING_FAIL  4 problem(s); 77/85 detectors run by a gate, 8 dated-exempt
U    rc=1  last: PROBEWIRING_FAIL  1 problem(s); 76/85 detectors run by a gate, 8 dated-exempt
        18:  FAIL  UNWIRED DETECTOR  artifacts/ip30abortkill/ip30_abort_probe.py is run by NO gate and has no dated exemption.
H0   rc=0  last: PROBEWIRING_PASS  76/85 detectors run by a gate, 9 dated-exempt, 44 witnesses correctly ungated
H1   rc=1  last: PROBEWIRING_FAIL  5 problem(s); 76/85 detectors run by a gate, 9 dated-exempt
        19:  FAIL  EXPIRED EXEMPTION  artifacts/ip30abortkill/ip30_abort_probe.py came due 2026-10-30 (today 2026-10-31) and is still run by no gate
RESTORE: gate_arm.sh cmp-clean against its backup
RESTORE: exec lines now 1
R_CONTROLS_DONE
```

## 4. Questions
**Q1.**  Is any sentence in section 2 -- the block comment, the probe's correction note, the checker notes, the pin
comment, the bug-file note, the CHANGELOG draft -- false, over-qualified or under-qualified against the files and the
receipts?  Cite `file:line` or the receipt line.
**Q2.**  The block as it will ship: does any control above miss a way it can pass on a broken run?  Is the stall
disclosure now exact about which sessions read a stall green?
**Q3.**  D1 and D2: rule on each, with the reason.  A seat whose position I did not adopt: be harder on mine; a seat
whose position I adopted: be harder on yours.
**Q4.**  Anything else owed IN this commit (the ledger rows `wiringcliff' and `ip30abortkill', a queue entry, the gate run's
binary choice) -- and which of my accepted dispositions in section 0 is wrong?

**Format:** your token first, then ONE line `VERDICT: <n> flags -- <one line>`, then Q1..Q4.  Every defect is a line
starting `FLAG:`.  Facts and flags only.
