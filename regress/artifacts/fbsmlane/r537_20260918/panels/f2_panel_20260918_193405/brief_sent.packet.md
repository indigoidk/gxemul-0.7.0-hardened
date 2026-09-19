# §F2 ADJUDICATION PASS -- #536 (probe wiring) and #537 (fbpending self-mutant lane): EVERY SEAT'S PASS-2 FINDINGS, SHARED

## READ THIS FIRST

You answered pass 2 blind to the other seats.  This packet puts every seat's findings side by side, with MY
disposition on each, and the disagreements with both sides in their own words.  **Please adjudicate -- do not
ratify.**  A seat reviewing its OWN finding is asked to be HARDER on it, including on whether my FIX is right,
not merely whether the finding was.  I have accepted most of what the panel raised; that is a suspicious number,
and the question I most need answered is **WHICH OF MY DISPOSITIONS IS WRONG**.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/` at HEAD `3c41f01` plus the working-tree changes described here.**  Scope
your reading to `GXEMUL-SEC/regress/*.sh`, `regress/*.c`, `regress/*.py`, `regress/selfmutants/` and
`tools/pipeline/check_probe_wiring.py`.  Do not read `regress/artifacts/` or `tools/pipeline/ledger.json`.  If you
cannot read files, that is expected: the repairs are inlined in section 4.  **VERDICT LINE FIRST.**

Pass-2 roster: codex (GPT-6 Astra, max) GO-WITH-CHANGES; agy GO-WITH-CHANGES; grok RATIFY-with-one-L4; glm, deepseek,
minimax, kimi-k3:cloud (the kimi CLI is walled; its substitute answered) -- no false premise; Opus 5 (measuring):
SHIP BOTH, after one adjudicated question and records edits (MEASURED: P1-P5 hold; Q2 (a), (c), (e) caught and (b), (d), (f) not; NEW: the R4 pin is verdict-equivalent; M5a ON the stamped date closes the `<=` gap 22/22 -> 21/22 on the mutant).  Fable 5 has NOT fired yet: it adjudicates after this pass.

---

## 1. FINDINGS, NUMBERED, WITH MY DISPOSITION

**F1 -- the hpcmips section comment named the wrong completion sentinel** (kimi, grok, glm, codex -- four seats
independently).  It said the verdict line "doubles as the completion sentinel"; the check greps
`^HPCMIPS_CTOR_RESULT=`, the line BEFORE the verdict.  ACCEPTED, L1 (unshipped): the comment now says the RESULT line
is the sentinel and a run killed before its tally reds the first check.

**F2 -- a present-tense wrong record in gate_offline.sh** (grok).  Right under the new `SM_COVERED ... fbpending_bound`,
the paragraph that justified the old exemption still said the lane "DOES NOT RUN YET" and that finding out why was
"its own piece of work".  ACCEPTED, L4: rewritten as a discharge note that states the reason (the token), keeps the
four hand-measured 2026-08-20 mutants, and says the lane automates the second.

**F3 -- a false sentence in the checker comment I added** (codex).  "BOTH HALVES OF THAT PAIRING ARE GONE" -- but the
pairing was #442's TWO debts: the self-mutant lane (#537 discharges it) and `fbpending_drain_probe.py`'s exemption,
which remains (re-dated to 2026-09-27 with the other ten).  ACCEPTED, L4: now "ONE HALF OF THAT PAIRING IS GONE",
naming the half that remains.

**F4 -- the checker selftest never tests the STAMPED DATE** (codex, executed the checker in memory; the Opus seat
measured the same independently -- O3 below).  With the comparison mutated `d < today` -> `d <= today`: 2026-09-26
PASS/PASS, **2026-09-27 PASS vs FAIL**, 2026-09-28 FAIL/FAIL -- so M5a (the day before) and M5b (the day after) both
accepted the off-by-one.  PRE-EXISTING: the old literals (09-19 / 09-21) skipped 09-20 the same way.  **My FIRST
disposition was FILE; I REVERSED it on O3's measurement: ADOPTED in-round, L1** (rows this round is building) -- M5a
now runs ON the earliest stamped date: 22/22 on the staged table, **21/22 on the `<=` mutant**, no new case, so the
denominator precommit pins at 22 is untouched.  What it gives up is the day-before case, which caught only `!=`
(expires every exemption on every other day, so it cannot stay quiet in production).  **Is giving up `!=` right?**

**F5 -- the newly gated hpcmips probe pins an UNRELATED live defect** (codex).  Control C2 requires `-E mvmeppc -e
mvme1600` construction to abort in `bus_pci_add()` ("pci_data == NULL!"), so a future fix to THAT machine turns this
gate red.  ACCEPTED as DISCLOSURE, in-round: the section comment now says so and that the fixing round owes C2's
re-derivation (F3 covers the classifier synthetically).  The independence fix is FILED as `hpcmipsc2`.  Loud, not a
false pass -- which is why I did not rewrite a shipped probe's control in a wiring round.

**F6 -- the §F table mixed units** (agy, codex, kimi).  Git's numstat counts every line; my grep counted non-blank
ones; the header said "non-blank".  `.why` is 3 lines added, 2 non-blank.  ACCEPTED; corrected table in section 3.
**glm's companion claim is REFUTED by counting:** it read the checker diff's third hunk as 15 added / 15 removed
against a header of net +2, and 20 removed in total.  Counted: that hunk is 18 context + 9 added + 7 removed
(`-2150,25 +2163,27`, consistent), and the file totals 50 added / 22 removed, as the table said.

**F7 -- my brief's Q2(e) premise was false** (grok, codex).  Dropping `"$PMAX"` does not leave "no binary argument": the
line still passes `gate`, which becomes `sys.argv[1]`, the binary.  The consequence is unchanged (no
`MK48_WITNESS_DONE`, the completion check reds); the mechanism I stated was wrong.  ACCEPTED as a brief defect.

**F8 -- Q2(b): loosening gate 2's verdict grep to `FBBOUND_` passes silently** (glm, deepseek, codex, agy, kimi).
`FBBOUND_FAIL` also matches, so the #442 row can no longer fail.  DISCLOSED, no row: this is an edit to the GATE's own
grep, which no self-mutant of the HARNESS can see -- the check-guards-the-check regress.  The anchored `^FBBOUND_PASS$`
this round ships is the strong form.

**F9 -- Q2(d): R4 as `failures <= 1` escapes the lane** (all seats that answered it).  The committed mutant produces
seven failures, so R4 still reds.  DISCLOSED as clause-(e) debt: a single-failure regression is still caught, because
the harness's own verdict is `failures ? FAIL : PASS` -- so what escapes is a weaker PIN, not a missed defect.

**F10 -- Q2(f): deriving from the LATEST date passes today** (all).  All eleven share 2026-09-27.  DISCLOSED: it becomes
loud (M5a reds) the first day the dates differ; earliest is the correct anchor because M5a needs a day on which nothing
has expired.

**F11 -- the lane's object paths need `$SEC` absolute** (glm).  SETTLED by reading: `lib.sh` sets
`ROOT=${ROOT:-/mnt/c/DocumentNoSnc/CC/GXEMUL}` and gate_offline.sh `SEC=$ROOT/GXEMUL-SEC`.  The gate run will show it.

**F12 -- compiler identity** (codex, P3).  Gate 2 picks `$CC = cc` before `gcc`; the helper hardcodes `gcc`.  SETTLED
by measurement on this machine: `cc` and `gcc` resolve to the same binary, `x86_64-pc-linux-gnu-gcc` 15.2.1.

**F13 -- "7 row failure(s)" vs eight FAIL rows** (kimi, glm).  SETTLED by reading: R4 prints `%d row failure(s) above`,
evaluated before R4 itself counts, so seven R3 failures + R4 = eight FAIL lines, and the text says seven.

**F14 -- stale-build inheritance** (glm): the lane links whatever build/ holds, with no freshness guard, exactly as the
#442 main lane does.  NOTED: build/'s freshness is the two-part clearance's job, run at round boundaries.

**F15 -- the #442 lane's `rows actually run` floor is 15 against 27/28** (kimi).  PRE-EXISTING, no action: the harness's
IDENTITY row pins the exact count.

**THE OPUS SEAT'S FINDINGS (measuring; it built and ran everything below in its own /tmp copy):**

**O1 -- the #537 lane's R4 pin is VERDICT-EQUIVALENT** (measured).  Blind R3 (`>= 1` -> `>= 0`) AND tighten R1
(`trough >= 0` -> `>= 1`): the lane still reports SELFMUTANT_OK, "killed by the named row: FAIL R4", while R3 detects
nothing.  Each edit alone is green on the fix; R3 blinded ALONE reds the lane -- so today the lane does protect R3, but
only because no other row happens to see this mutant.  **My disposition: FILE as `fbsmr3pin`** (pin an R3-only aggregate;
IDENTITY becomes 29/28) -- the detector still DETECTS the mutant (through R1), so what escapes is WHICH row, and gate 2's
own comment scopes the lane as "a LIVENESS CONTROL ... not a census".  Changing #442's harness rows and identity counts is
not a wiring round's.  **Is that right, or is it in-round?**

**O2 -- two more stale mk48 passages in the checker** (reading): a MANIFEST comment ("EXEMPT below rather than wired ...
gate_m88k_rounding.sh is the only gate on this CPU family") and an EXEMPT-block paragraph describing the entry this very
edit deletes ("#521's detector ... lacks a HOME").  ACCEPTED, L4: the first rewritten (wired by #536, and why the old
reason was true of that gate and false of the tree), the second deleted with its entry.

**O3 -- M5a on the stamped date** (measured, independently of codex's F4): moving M5a to `_d5` keeps 22/22 on the staged
table and scores 21/22 (`FAIL M5a rc=1 want=0`) on the `<=` mutant.  **This REVERSES my F4 disposition: ADOPTED in-round,
L1** -- these are rows this round is still building.  Re-measured here: 22/22 staged; 21/22 on `d <= today`.  The one
thing moving M5a gives up is the day-before case, which caught only `!=` -- a comparison that expires every exemption on
every OTHER day and so cannot stay quiet in production.

**O4 -- stale records OUTSIDE both diffs, each made false by these rounds** (reading).  ALL ACCEPTED, L4, and each joins
its round: `precommit_check.sh`'s section-R comment ("2026-09-20, chosen to fall due with gate_offline's fbpending_bound")
-> #536 (the date now lives only in the checker); gate_offline.sh's "The other five are uncovered debt" -> #537 (every
one discharged, ieee_store alone left); `selfmutant.py`'s "the margins below are ~88x and ~190x" -> #537 (a dated line:
the new lane builds in 3.9-4.5 s and runs in 1.9-2.1 s, so the margins are ~27x and ~29x).

**O5 -- P4, measured** (supports D1's ruling): with lib.sh, a gate whose only missing piece is `note`d ends PASS rc 0; with
`degrade` it ends SKIP rc 77.  Today the new lane's red is the ONLY thing stopping a buildless gate 2 from reporting PASS.
It also names a defect in the red itself: it appears under the row name "the detector still detects" -- folded into
`fbnobuild`.

**O6 -- the `t536/` dry-run logs it read are the NEGATIVE-CONTROL copies** (one flipped row each).  CLARIFIED, no change:
the clean logs are preserved in the artifacts dir (mk48 57 ok / 0 FAIL, hpcmips 28 ok / 0 FAIL, md5-matched to the runs),
and the seat itself reports the sections score 93/0 once the flipped lines are restored -- so section 3's bullet stands.

**O7 -- Q3, by the round's own reasoning**: alpha_tbi, lca_badval, lca_isalane, lca_widewrite and ip30_abort have mk48's
shape (a cold-debugger probe needing only the binary) and the same "no home" reason #536 set aside -- and the Alpha probes
write `alpha_dummy.bin` into GXEMUL-SEC/regress, so a gate running them would write into the source tree.  RECORDED for
`wiringcliff`'s next round; the owner ruled two this time.  (Also: `diff_fbpending_bound.c` is the one CRLF `.c` in regress/
-- pre-existing, kept; and the harness's bare `#include "dev_footbridge.c"` means a stray `regress/dev_footbridge.c` would
silently feed #442's main lane -- NOTED, pre-existing.)

## 2. DISAGREEMENTS -- please adjudicate your own side

**D1 -- what the new lane does when build/ has no objects.**  Today: the pristine arm cannot link, the helper says
SETUP, the gate row REDS -- while the #442 main lane in the same file `note`s "SKIPPED, not passed" and adds no check.

* **kimi:** "SETUP-from-absent-`build/` is an environment state ... A red on a machine without `build/` is noise ... test
  the object list for emptiness up front -> empty => NOTE-skip mirroring the main lane."
* **grok:** "Skip-when-unbuilt is the one I would still take."  **glm:** "Mirror the NOTE, assert build/ once for both, or
  make both red -- pick one and record it."
* **agy:** "This asymmetry is right: selfmutants operate under a fail-closed doctrine ... gate 2 runs after `gate_build`
  in `run.sh`, so `build/` objects are always present during battery runs."
* **codex:** "Do not copy the note-only skip.  ... the later `SELFCHECK manifest: every COVERED detector ran its
  sentinel` also requires `diff_fbpending_bound.log`.  An absent log fails; a retained previous log can satisfy it
  because the no-object branch does not regenerate it.  If buildless operation is supported, use the existing
  `degrade()` mechanism ... and coordinate both lanes and sentinel accounting."
* minimax: a defensible trade-off; deepseek: a policy question.
* **Opus (MEASURED with lib.sh):** a gate whose only missing piece is `note`d ends PASS rc 0; with `degrade` it ends SKIP
  rc 77.  "Today the new lane's red is the ONLY thing stopping gate 2 from reporting PASS when build/ has no objects."
  Right fix: `degrade` in BOTH lanes and truncate the log before the main lane.

**My ruling: KEEP RED this round, and FILE `fbnobuild`** -- gate 2's whole buildless behaviour as ONE explicit `degrade()`
SKIP across the #442 lane, this lane and the SC sentinel accounting.  Warrant: codex's finding means copying the NOTE
would add a SECOND path by which a buildless gate 2 reports green (the #442 lane already has one, through a stale log),
while red is loud and unreachable in the battery; the right fix touches #442's lane, which is not this round's.
**kimi, grok, glm: is that warrant sound, or is red-on-bare-host the worse harm?**

**D2 -- the option set** (every seat named members).  Widen `selfmutant.py`'s token grammar; print both tokens; stagger
the eleven; retire an undischargeable probe; reclassify detector -> witness.  **The owner's rulings stand** (fix
#537 rather than re-date; wire two and re-date eleven as one block).  Recorded, not re-litigated -- but if a member
is WRONG to reject for a reason the rulings did not weigh, say so.

## 3. THE CORRECTED DISCLOSURE TABLE (git numstat -- all lines -- against HEAD 3c41f01, staged content)

added	removed	file   (ALL lines, blank included; staged content vs HEAD 3c41f01)
5	1	regress/diff_fbpending_bound.c   (#537)
29	15	regress/gate_offline.sh   (#537)
3	0	regress/selfmutant.py   (#537)
3	0	regress/selfmutants/fbpending_bound.why   (#537)
45	0	regress/gate_arm.sh   (#536, staged blob)
61	31	tools/pipeline/check_probe_wiring.py   (#536, staged blob)
4	2	tools/precommit_check.sh   (#536, staged blob; comment only)
plus two NEW artifact dirs: regress/artifacts/fbsmlane/r537_20260918/ (#537), regress/artifacts/wiringcliff/r536_20260918/ (#536, incl. four .py tools, classified)

## 4. THE REPAIRS MADE SINCE PASS 2, INLINED

```diff
--- a/regress/gate_offline.sh (as reviewed in pass 2)
+++ b/regress/gate_offline.sh (now)
@@ -1079,16 +1079,15 @@
 #  Oct/Nov unilaterally; asked, the owner chose a fortnight -- 148 uncovered rows across five
 #  differentials is urgent, not a Q4 item.  Recorded because a deadline nobody chose is a
 #  deadline nobody owns, and this gate goes RED on that date whether or not the work is done.
-#  fbpending_bound, dated 2026-09-20.  *** THE HARNESS HAS A FAILABILITY CONTROL -- its
-#  @@SELFCHECK@@ block is present and the SC manifest covers it -- but the SELF-MUTANT LANE
-#  DOES NOT RUN YET, and the two catch different failures, so this is a real gap and not a
-#  formality. ***  The lane builds in a MIRRORED tree and this harness is the only one that
-#  links against ~221 build objects rather than compiling standalone; its pristine arm builds
-#  in the mirror but does not emit the PASS token, and finding out why is its own piece of
-#  work rather than a flag.
+#  fbpending_bound's exemption, dated 2026-09-20, is DISCHARGED by #537 -- its lane runs above.
+#  This paragraph said the SELF-MUTANT LANE "DOES NOT RUN YET" because its pristine arm "does not
+#  emit the PASS token", with the reason left as its own piece of work.  The reason was the token:
+#  the harness printed `FBBOUND_VERDICT=PASS` where selfmutant.py reads `<WORD>_PASS` (found as
+#  `fbsmlane`, 2026-08-27), so no run of it could pass.  The @@SELFCHECK@@ control was always live;
+#  the two catch different failures, which is why the missing one was a real gap.
 #
-#  WHAT IS NOT MISSING, so the exemption is not read as "untested": the mutants were built and
-#  run by hand against the tracked tree on 2026-08-20, and every one is killed by a named row.
+#  THE FOUR MUTANTS MEASURED BY HAND against the tracked tree on 2026-08-20, each killed by a named
+#  row -- the lane automates the second one, pinned through R4:
 #    pre-fix          FAIL R1 x7 and R2 with trough -2147483648 (the overflow itself)
 #    reset to 0       FAIL R3 x7   (R1 stays green -- the bound still works, only the debt)
 #    one callback     FAIL R1 x7
@@ -1126,8 +1125,9 @@
       "${sm_unbacked:-none}" "none"
 #  ieee_store carries a far-future date because GATE 3 covers it -- against TOTAL comparator
 #  death only, and by the vacuity-prone `grep -c PASS == 0` form this helper was written to
-#  avoid, so it is a weaker exemption than it looks.  The other five are uncovered debt with
-#  real deadlines.
+#  avoid, so it is a weaker exemption than it looks.  The other five WERE uncovered debt with
+#  real deadlines; every one is discharged -- the last, fbpending_bound, by #537 -- so
+#  ieee_store is the only entry left.
 #
 #  DATED ENTRIES, NOT A COUNT.  The first version asserted `wc -w == 6` under a row named
 #  "6, shrinking not growing" -- and a seat measured that SHRINKING IT IS RED (got=5 want=6),
diff --git a/regress/selfmutant.py b/regress/selfmutant.py
index ec2d780..815b18b 100644
--- a/regress/selfmutant.py
+++ b/regress/selfmutant.py
@@ -119,6 +119,9 @@ def io_write(path, text):
 #  and ~190x, deliberately enormous: `gate_ab` uses 3x and that MEASURABLY false-FAILed a
 #  45-minute battery under subagent load.  A too-tight timeout turns a busy host into a red
 #  gate, which is the fastest way to get a gate switched off.
+#  #537, 2026-09-18: a 13th lane, fbpending_bound, links ~221 build/ objects -- build 3.9-4.5 s,
+#  run 1.9-2.1 s (Opus seat, 8 runs) -- so the margins are now ~27x and ~29x, still an order of
+#  magnitude above gate_ab's 3x.
 BUILD_TIMEOUT = float(os.environ.get("SELFMUTANT_BUILD_TIMEOUT", "120"))
 RUN_TIMEOUT = float(os.environ.get("SELFMUTANT_RUN_TIMEOUT", "60"))
 
--- a/regress/gate_arm.sh (staged, as reviewed)
+++ b/regress/gate_arm.sh (staged, now)
@@ -1612,7 +1612,11 @@
 #  ------------------------------------------------------------ hpcmipsctor (#444) + #536
 #  Three of eight advertised hpcmips subtypes SIGABRTed during construction (#444).  Its rung-2
 #  detector (~8 s, no rig image) shipped EXEMPT for want of a construction gate; #536 wires it here.
-#  Its last line is the verdict (HPCMIPS_CTOR_PASS / _FAIL) and doubles as the completion sentinel.
+#  It ends by printing HPCMIPS_CTOR_RESULT=<ok>/<rows> and then its verdict, HPCMIPS_CTOR_PASS / _FAIL; the
+#  RESULT line is the completion sentinel, so a run killed before its tally reds the first check.
+#  C2 pins an UNRELATED live defect ON PURPOSE, as its unrelated-abort control: mvme1600's construction
+#  aborts in bus_pci_add() ("pci_data == NULL!").  A round that fixes that machine turns C2 red and owes
+#  its re-derivation -- F3 already covers the classifier with a synthetic abort.  Filed as `hpcmipsc2`.
 HPCLOG=$LOGDIR/hpcmips_ctor.log
 python3 -u hpcmips_ctor_probe.py --binary "$PMAX" > "$HPCLOG" 2>&1 || true
 if ! grep -q "^HPCMIPS_CTOR_RESULT=" "$HPCLOG"; then
--- a/tools/pipeline/check_probe_wiring.py (staged, as reviewed)
+++ b/tools/pipeline/check_probe_wiring.py (staged, now)
@@ -180,13 +180,15 @@
         (CLASS_TOOL, "#530 pass 2: generates the one-edit variants from the 8bd97e4 blob, each an exact-once replacement"),
     "artifacts/lcalenzerodrop/opus_p2_20260918/scripts/summarize.py":
         (CLASS_TOOL, "#530 pass 2: tabulates score and getenv value per (cell, binary); refuses a leg with no sentinel"),
-    #  #536 wiringcliff: the three editors that produced this round's staged blobs, preserved as run.
+    #  #536 wiringcliff: the four editors that produced this round's staged blobs, preserved as run.
     "artifacts/wiringcliff/r536_20260918/apply536_gate.py":
         (CLASS_TOOL, "#536: inserts the mk48 + hpcmips sections into gate_arm.sh at a unique anchor; refuses otherwise"),
     "artifacts/wiringcliff/r536_20260918/apply536_exempt.py":
         (CLASS_TOOL, "#536: drops the two wired exemptions, re-dates eleven to 2026-09-27, derives the selftest's M5 days"),
     "artifacts/wiringcliff/r536_20260918/apply536_manifest.py":
-        (CLASS_TOOL, "#536: adds these three MANIFEST lines -- the round's own tools, classified by the round"),
+        (CLASS_TOOL, "#536: adds these MANIFEST lines -- the round's own tools, classified by the round"),
+    "artifacts/wiringcliff/r536_20260918/apply536_precommit.py":
+        (CLASS_TOOL, "#536: corrects precommit_check.sh section R's comment, which named the old 2026-09-20 date"),
     "artifacts/lcaisalane/opus_c5_20260915/instrument/check_pred.py":
         (CLASS_TOOL, "closing pass 5: checks each mutant's score against its written prediction"),
     "artifacts/lcaisalane/opus_c5_20260915/instrument/disc530c5.py":
@@ -919,12 +921,10 @@
     "artifacts/mk48nvramkill/opus_mk48_nvram_witness_20260910.py":
         (CLASS_WITNESS, "mk48nvramkill (#521): eight offsets inside the device's own 8192-byte registration reach a default: arm that calls exit(1) -- rung 3 on unmodified -E mvme88k -e mvme187, SIXTEEN cells driven (8 offsets x read/write), committed 15/47 with all 15 controls green, fixed 46/47"),
     # -- #521 mk48nvramkill -------------------------------------------------------------
-    #  CLASS_DETECTOR, and EXEMPT below rather than wired.  It is a fast (0.4 s) single-leg
-    #  instrument that runs green on the fix today, so unlike a witness it COULD be gated --
-    #  what it lacks is a home: gate_m88k_rounding.sh is the only gate on this CPU family and
-    #  it drives luna88k, not mvme88k/mvme187.  Giving it an mvme187 leg is a gate change
-    #  owing its own negative controls, i.e. a harness round, not a rider on a device fix.
-    #  Filed to `wiringcliff'.
+    #  CLASS_DETECTOR, WIRED by #536 (2026-09-18) into gate_arm.sh.  It stood EXEMPT on the
+    #  reason "gate_m88k_rounding.sh is the only gate on this CPU family and it drives luna88k,
+    #  not mvme88k/mvme187" -- true of that gate, false of the tree: gate_arm.sh already drives
+    #  mvme187 for the PCC2 probes, so the home existed and the wiring was the harness round.
     # -- ppcrldiclzero + siblings ------------------------------------------------------
     #  CLASS_WITNESS and correctly ungated: RED on the committed build by design (19/27),
     #  so a gate row would be permanently red until the fix ships.  It is also a FAMILY
@@ -2141,11 +2141,12 @@
 #  owner set the SM dates and set them TIGHTER than the ones proposed, and a deadline nobody
 #  chose is a deadline nobody owns.
 #
-#  *** #536/#537, 2026-09-18: BOTH HALVES OF THAT PAIRING ARE GONE. ***  #537 discharged
-#  fbpending_bound's SM_EXEMPT line -- its self-mutant lane runs now -- and #536 wired
-#  mk48_nvram_probe.py and hpcmips_ctor_probe.py into gate_arm.sh.  The eleven exemptions left
-#  at 2026-09-20 moved to 2026-09-27 BY OWNER RULING, so they again fall due as ONE block: the
-#  cliff `exemptcliff` names is re-created a week out, deliberately and dated, not by copying.
+#  *** #536/#537, 2026-09-18: ONE HALF OF THAT PAIRING IS GONE. ***  #537 discharged
+#  fbpending_bound's SM_EXEMPT line -- its self-mutant lane runs now.  The other half,
+#  fbpending_drain_probe.py below, is still exempt: #536 wired mk48_nvram_probe.py and
+#  hpcmips_ctor_probe.py into gate_arm.sh and moved the eleven left at 2026-09-20 to 2026-09-27
+#  BY OWNER RULING, so those eleven again fall due as ONE block: the cliff `exemptcliff` names
+#  is re-created a week out, deliberately and dated, not by copying.
 #
 #  These are wiring jobs, not design ones -- each probe already prints a verdict token and
 #  exits nonzero on failure.  What each needs is a gate that owns it, its rig preconditions,
@@ -2190,9 +2191,6 @@
     #  single-leg 15-row instrument that runs green on the fix today.  What it lacks is a
     #  HOME: no gate in this tree runs an Alpha machine at all.  Dated to fall due with
     #  the others so the cliff stays one date rather than becoming a rolling excuse.
-    #  #521's detector.  Single-leg, fast, green on the fix -- it lacks a HOME, not a design:
-    #  the only gate on this CPU family drives luna88k, not mvme88k/mvme187.  Dated to fall
-    #  due with the others so the cliff stays one date rather than a rolling excuse.
     #  #522's detector.  Single-leg, 0.2 s, green on the fix.  It lacks a gate that RUNS a
     #  64-bit PowerPC CPU: gate 9 constructs them but has no result oracle, and both PowerPC
     #  gates drive a 32-bit part.  Closing that is a harness round, filed to wiringcliff.
@@ -2820,8 +2818,12 @@
     #  GREEN, and failed the selftest.  The frozen-claim-about-a-table-designed-to-change that
     #  _pick_exempt_detector() refuses for M1-M3, one mutant group further down.  The
     #  comparison is `d < today`, so an exemption is valid ON its stamped date: the earliest
-    #  DETECTOR date minus one day is green and plus one day is red.  No dated detector
-    #  exemption left is two FAILS, never a skip -- the denominator must not shrink.
+    #  DETECTOR date ITSELF is green and the day after is red.  M5a runs ON the date, not the
+    #  day before, because that is the one day on which `<` and `<=` differ: with `d <= today`
+    #  both day-before and day-after cases passed (codex, #536 pass 2, executed; Opus measured
+    #  22/22 -> 21/22 once M5a moved).  The day-before case caught only `!=`, which expires
+    #  every exemption on every other day and cannot stay quiet in production.  No dated
+    #  detector exemption left is two FAILS, never a skip -- the denominator must not shrink.
     _m5 = sorted(EXEMPT[_n][0] for _n in EXEMPT
                  if MANIFEST.get(_n, (None,))[0] == CLASS_DETECTOR
                  and DATE_RE.match(EXEMPT[_n][0] or ""))
@@ -2832,8 +2834,8 @@
         import datetime as _dt5
         _d5 = _dt5.date.fromisoformat(_m5[0])
         rg, chk = fresh()
-        case("M5a a live exemption is GREEN the day before", 0, "PROBEWIRING_PASS", chk, rg,
-             extra=("--today", (_d5 - _dt5.timedelta(days=1)).isoformat()))
+        case("M5a a live exemption is GREEN ON its stamped date", 0, "PROBEWIRING_PASS", chk, rg,
+             extra=("--today", _d5.isoformat()))
         case("M5b the same tree is RED the day after", 1, "EXPIRED EXEMPTION", chk, rg,
              extra=("--today", (_d5 + _dt5.timedelta(days=1)).isoformat()))
 
--- a/tools/precommit_check.sh (HEAD)
+++ b/tools/precommit_check.sh (#536 staged)
@@ -520,8 +520,10 @@
 #
 #  HARD, and retroactive rather than forward-only-by-date: the domain is 36 files in one
 #  flat directory, and a date cutoff would grandfather exactly the four files it exists for.
-#  Existing gaps are carried as DATED exemptions that EXPIRE (2026-09-20, chosen to fall due
-#  with gate_offline's fbpending_bound), never as silent grandfathering.
+#  Existing gaps are carried as DATED exemptions that EXPIRE, never as silent grandfathering; the
+#  dates live in check_probe_wiring.py's EXEMPT table, not here.  (They were 2026-09-20, chosen to
+#  fall due with gate_offline's fbpending_bound; #537 discharged that debt and #536 moved the
+#  block to 2026-09-27 by owner ruling.)
 #
 #  THE SELFTEST RUNS ONLY WHEN THE CHECKER ITSELF CHANGES.  --selftest applies 18 mutants to
 #  temp copies and asserts each exit status, which takes ~14 s -- too slow for every commit,
```

## 5. QUESTIONS

1. Adjudicate F1-F15 (and the Opus findings) and D1-D2: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each,
   with a reason.
2. **Which of my dispositions is wrong?**  I accepted or disclosed nearly everything and filed two; that is suspicious.
3. **What did all of us miss?**  You now have the whole panel's output.
4. The repair chain: section 4's repairs are new material.  Is any of them itself wrong?

**Standing licence:** if, while verifying a claim, you found something ELSE -- say so.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
