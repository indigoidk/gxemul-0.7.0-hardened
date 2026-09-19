# PASS 2 -- #536 (two probes wired, eleven exemptions re-dated) and #537 (the fbpending_bound self-mutant lane)

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/` (its `regress/` and `tools/pipeline/`).**  There are THREE
pristine-2021-upstream copies of GXemul under the project root (`./src/` and two under
`_archive/audit-results-*/builds/`).  They are NOT this fork.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — a count, a date window — ENUMERATE it rather than reasoning
about it.**  And ENUMERATE THE RIGHT DOMAIN: a domain is itself a premise.

**Scope your reading to `GXEMUL-SEC/regress/*.py`, `GXEMUL-SEC/regress/*.sh`, `GXEMUL-SEC/regress/*.c`,
`GXEMUL-SEC/regress/selfmutants/` and `GXEMUL-SEC/tools/pipeline/check_probe_wiring.py`.  Do not read
`regress/artifacts/` or `tools/pipeline/ledger.json`** -- everything from them that a question depends on is
inlined below.  The frozen copies of the reviewed files are named in §6.

**VERDICT LINE FIRST**, so your answer survives truncation.

Both rounds are TEST-APPARATUS rounds (no emulator source changes).  Both are due by 2026-09-20, the day the
harness's dated exemptions expire.

---

## 1. WHAT EACH ROUND IS, AND WHY

### #537 -- `fbsmlane`: the fbpending_bound harness's self-mutant lane never ran

`regress/gate_offline.sh` (gate 2) runs a SELF-MUTANT lane for each offline differential harness: the helper
`regress/selfmutant.py` mirrors the tree with symlinks, writes the subject file for real, builds the harness
twice -- pristine and with ONE committed mutation (`selfmutants/<stem>.old` -> `.new`) -- and requires
(a) the pristine arm to print a `<WORD>_PASS` token, (b) the pinned row id to name exactly one row, green on
pristine, (c) the two binaries to differ, and (d) the mutant arm to print a `<WORD>_FAIL` token with the
pinned row among its FAIL lines.  Only then does it print `SELFMUTANT_OK`; the gate row wants exactly one.

`diff_fbpending_bound.c` (#442's harness for a bounded interrupt counter in the Footbridge device) was the one
harness NOT in the lane: `SM_EXEMPT="ieee_store:2099-01-01 fbpending_bound:2026-09-20"`.  A ledger row
diagnosed why on 2026-08-27, mechanically: the helper reads tokens as

    passtok = re.search(r"\b([A-Z0-9_]+_PASS)\b", stdout)
    failtok = re.search(r"\b([A-Z0-9_]+_FAIL)\b", stdout)

and this harness printed `FBBOUND_VERDICT=PASS` -- `=` where the pattern needs `_` -- so the pristine arm
could never pass.  Every other harness prints the house form (`RTC_RANGE_PASS`, `SH4_TMU_PASS`, ...).
**Owner ruling 2026-09-18: fix it, do not re-date it.**

The mutant (committed since 2026-08-20, unchanged here):

    selfmutants/fbpending_bound.old:   		d->pending_timer_interrupts[nr] = 1;
    selfmutants/fbpending_bound.new:   		d->pending_timer_interrupts[nr] = 0;

(the reset of the bounded counter "still owes one interrupt"; 0 drops it.  Caught only by row R3, which
prints once per case -- seven cases -- so the lane pins the aggregate row R4, which is red whenever any row
above it is.)

### #536 -- `wiringcliff` / `exemptcliff`: thirteen probe exemptions expire together

`tools/pipeline/check_probe_wiring.py` (run by precommit on every commit) requires each committed DETECTOR
probe to be run by a gate, or to carry a DATED exemption; `d < today` makes an exemption expired, so an
entry is valid ON its stamped date.  At HEAD, thirteen DETECTOR exemptions are all dated 2026-09-20.
**Owner ruling 2026-09-18: wire the two that are cheap, re-date the other eleven to 2026-09-27.**

* `mk48_nvram_probe.py` (#521; 57 rows; `-E mvme88k -e mvme187`) -> `gate_arm.sh`.  Its exemption reason
  said "no gate drives mvme88k/mvme187"; `gate_arm.sh` already drives mvme187 for three PCC2 probes.
* `hpcmips_ctor_probe.py` (#444; 28 rows; construction of every advertised hpcmips subtype, ~8 s, no
  disk image) -> `gate_arm.sh`.
* the other eleven -> 2026-09-27 (listed in §3).

---

## 2. THE DIFFS, INLINED

### 2a. #537 -- `git diff HEAD` of its three files

```diff
diff --git a/regress/diff_fbpending_bound.c b/regress/diff_fbpending_bound.c
index 836c28d..d76b06e 100644
--- a/regress/diff_fbpending_bound.c
+++ b/regress/diff_fbpending_bound.c
@@ -358,6 +358,10 @@ int main(int argc, char *argv[])
 	    "%d rows (expect %d with R2, %d without)",
 	    rows + 1, IDENT_DEEP, IDENT_SHALLOW);
 
-	printf("\nFBBOUND_VERDICT=%s\n", failures ? "FAIL" : "PASS");
+	/*  #537: the house verdict token, `<WORD>_PASS' / `<WORD>_FAIL'.  This printed
+	    `FBBOUND_VERDICT=PASS', which selfmutant.py's `\b([A-Z0-9_]+_PASS)\b' can never
+	    match -- the one deviation that kept this harness's self-mutant lane out of gate 2
+	    since #442 (diagnosed as `fbsmlane', 2026-08-27).  gate_offline.sh greps this line.  */
+	printf("\nFBBOUND_%s\n", failures ? "FAIL" : "PASS");
 	return failures ? 1 : 0;
 }
diff --git a/regress/gate_offline.sh b/regress/gate_offline.sh
index 3b60bf9..f093f04 100644
--- a/regress/gate_offline.sh
+++ b/regress/gate_offline.sh
@@ -1046,7 +1046,21 @@ selfmutant_one diff_diskimage_geom.c  src/disk/diskimage.c   diskimage_geom "mus
 #  selfmutant.py's and the outputs are byte-identical.
 selfmutant_one diff_sh4_tmu.c        src/devices/dev_sh4.c       sh4_tmu    "boundary"
 selfmutant_one diff_rtc_range.c      src/devices/dev_rtc.c       rtc_range  "2^32: timer NOT removed"
-' ' ') -lm -L/usr/X11R6/lib -lX11"
+#  #537 (owner: fix it, do not re-date): fbpending_bound's lane.  Two things kept it out since #442.
+#  (1) selfmutant.py reads a verdict only as `<WORD>_PASS'/`<WORD>_FAIL', which this harness's
+#  `FBBOUND_VERDICT=PASS' could never match -- it now prints the house form FBBOUND_PASS/_FAIL, and
+#  the #442 verdict row further down greps that (the fix shape `fbsmlane' named on 2026-08-27).
+#  (2) it is the one harness that links build/ objects instead of compiling standalone, so the
+#  flags carry them.
+#  The -I paths are RELATIVE on purpose: the lane builds in `<mirror>/regress', so ../src/devices
+#  is the MIRROR's copy of dev_footbridge.c -- the mutated one.  An absolute -I to GXEMUL-SEC would
+#  compile the PRISTINE copy in both arms; selfmutant.py's binary-identity check then reports SETUP,
+#  so the row reds rather than lies -- but the lane would never test anything.
+#  The stray line that stood below the rtc_range call since #442, `' ' ') -lm ... -lX11"', opened a
+#  quote that ran to the apostrophe in "run.sh's" six lines later and executed a command named ' '
+#  on every run (`command not found', rc 127; harmless under set -u, but a fragment, not code).
+selfmutant_one diff_fbpending_bound.c src/devices/dev_footbridge.c fbpending_bound "R4 every case bounded" \
+    "-std=gnu99 -I../src/include -I../src/include/thirdparty -I../src/devices $(find "$SEC/../build/src" -name '*.o' ! -name 'main.o' ! -name 'dev_footbridge.o' 2>/dev/null | sort | tr '\n' ' ') -L/usr/X11R6/lib -lX11"
 
 #  THE MANIFEST -- the part that stops this being a five-instance fix.
 #
@@ -1060,7 +1074,7 @@ selfmutant_one diff_rtc_range.c      src/devices/dev_rtc.c       rtc_range  "2^3
 #  Filed as `selfmutant6` -- doing them silently in this round would break the
 #  stopping rule, and leaving them unnamed after writing the helper would repeat
 #  the "grep for its siblings" miss this project keeps making.
-SM_COVERED="timer memory_rw footbridge m8820x m8invread diskimage_sync diskimage_parse wdc_identify diskimage_io diskimage_geom sh4_tmu rtc_range"
+SM_COVERED="timer memory_rw footbridge m8820x m8invread diskimage_sync diskimage_parse wdc_identify diskimage_io diskimage_geom sh4_tmu rtc_range fbpending_bound"
 #  DEADLINES SET BY THE OWNER, 2026-08-17, TIGHTER THAN THE ONES I PROPOSED.  I had picked
 #  Oct/Nov unilaterally; asked, the owner chose a fortnight -- 148 uncovered rows across five
 #  differentials is urgent, not a Q4 item.  Recorded because a deadline nobody chose is a
@@ -1081,7 +1095,7 @@ SM_COVERED="timer memory_rw footbridge m8820x m8invread diskimage_sync diskimage
 #    no ceiling       FAIL R1 on the two high-emulated_hz cases; R2 peak 2147483647
 #  The `.old`/`.new`/`.why` fragments are committed and describe exactly that, so the lane is
 #  a wiring job, not a design one.
-SM_EXEMPT="ieee_store:2099-01-01 fbpending_bound:2026-09-20"
+SM_EXEMPT="ieee_store:2099-01-01"   # #537: fbpending_bound moved to SM_COVERED
 sm_missing=""
 for f in "$HERE"/diff_*.c; do
     stem=$(basename "$f" .c); stem=${stem#diff_}
@@ -1272,7 +1286,7 @@ else
         #  pins that R2 actually ran.
         "$FBBIN" 2147487744 > "$FBLOG" 2>&1
         sed 's/^/       /' "$FBLOG" | tail -20
-        check "fbpending bound: offline verdict" "$(grep -c 'FBBOUND_VERDICT=PASS' "$FBLOG")" "1"
+        check "fbpending bound: offline verdict" "$(grep -c '^FBBOUND_PASS$' "$FBLOG")" "1"
         check "fbpending bound: R2 actually ran (not SKIPPED)"               "$(grep -c 'R2 no signed overflow.*direct ticks' "$FBLOG")" "1"
         check_min "fbpending bound: rows actually run"               "$(grep -cE '^  (ok|FAIL) ' "$FBLOG")" 15
     fi
diff --git a/regress/selfmutants/fbpending_bound.why b/regress/selfmutants/fbpending_bound.why
index 51040c0..412bb0a 100644
--- a/regress/selfmutants/fbpending_bound.why
+++ b/regress/selfmutants/fbpending_bound.why
@@ -28,3 +28,6 @@ This harness calls timer_tickN() directly, which the witness ladder classes as n
 reproduction.  Both ship because neither alone catches what the other does -- measured: a
 mutant deleting the absolute ceiling PASSES the rung-3 probe on every timer and is caught
 only here, at an emulated_hz above 68 MHz.
+
+#537, 2026-09-18: the harness now prints the house verdict token, FBBOUND_PASS / FBBOUND_FAIL.  The
+table above is the 2026-08-20 output as it printed THEN (FBBOUND_VERDICT=...), kept verbatim.
```

### 2b. #536 -- `regress/gate_arm.sh`, HEAD vs the staged blob (insert-only)

```diff
--- a/regress/gate_arm.sh (HEAD 3c41f01)
+++ b/regress/gate_arm.sh (#536 staged)
@@ -1587,6 +1587,47 @@
 fi
 
 
+
+
+#  ------------------------------------------------------------ mk48nvramkill (#521) + #536
+#  Eight of the nine MK48T08 clock-block offsets ended the emulator through default: (#521).  Its
+#  57-row detector shipped EXEMPT because "no gate drives mvme88k/mvme187" -- a reason that expired
+#  when this file began driving mvme187 for the PCC2 probes.  #536 (wiringcliff, owner ruling
+#  2026-09-18) wires it.
+MK48LOG=$LOGDIR/mk48_nvram.log
+python3 -u mk48_nvram_probe.py "$PMAX" gate > "$MK48LOG" 2>&1 || true
+if ! grep -q "MK48_WITNESS_DONE" "$MK48LOG"; then
+    check "mk48 nvram probe completed" "no" "yes"
+else
+    check "mk48 nvram probe completed" "yes" "yes"
+    for v in "live" "nvram0" "neg apparatus" "devsig yr" "devsig mon" "devsig mday" "devsig wday" "shape" "ok rd 1fef" "ok wr 1fef" "ok rd 1ff8" "ok wr 1ff8" "ok rd 1ff9" "ok wr 1ff9" "csr rise" "rt 1fef" "rt 1ff0" "rt 1ff1" "rt 1ff2" "rt 1ff3" "rt 1ff4" "rt 1ff5" "rt 1ff6" "rt 1ff7" "rd 1ff0" "rd 1ff0 obs" "rd 1ff1" "rd 1ff1 obs" "rd 1ff2" "rd 1ff2 obs" "rd 1ff3" "rd 1ff3 obs" "rd 1ff4" "rd 1ff4 obs" "rd 1ff5" "rd 1ff5 obs" "rd 1ff6" "rd 1ff6 obs" "rd 1ff7" "rd 1ff7 obs" "wr 1ff0" "wr 1ff0 obs" "wr 1ff1" "wr 1ff1 obs" "wr 1ff2" "wr 1ff2 obs" "wr 1ff3" "wr 1ff3 obs" "wr 1ff4" "wr 1ff4 obs" "wr 1ff5" "wr 1ff5 obs" "wr 1ff6" "wr 1ff6 obs" "wr 1ff7" "wr 1ff7 obs" "msg silent"; do
+        check "mk48 nvram row: $v" "$(count "$MK48LOG" "^$v  .*ok$")" "1"
+    done
+    check "mk48 nvram rows emitted" "$(( $(count "$MK48LOG" " ok$") + $(count "$MK48LOG" " FAIL$") ))" "57"
+    check "mk48 nvram rows green"   "$(count "$MK48LOG" " ok$")"   "57"
+    check "mk48 nvram rows red"     "$(count "$MK48LOG" " FAIL$")" "0"
+fi
+
+
+#  ------------------------------------------------------------ hpcmipsctor (#444) + #536
+#  Three of eight advertised hpcmips subtypes SIGABRTed during construction (#444).  Its rung-2
+#  detector (~8 s, no rig image) shipped EXEMPT for want of a construction gate; #536 wires it here.
+#  Its last line is the verdict (HPCMIPS_CTOR_PASS / _FAIL) and doubles as the completion sentinel.
+HPCLOG=$LOGDIR/hpcmips_ctor.log
+python3 -u hpcmips_ctor_probe.py --binary "$PMAX" > "$HPCLOG" 2>&1 || true
+if ! grep -q "^HPCMIPS_CTOR_RESULT=" "$HPCLOG"; then
+    check "hpcmips ctor probe completed" "no" "yes"
+else
+    check "hpcmips ctor probe completed" "yes" "yes"
+    for v in P1 P2 P3 F1 F2 F3 F4 F5 E1 A1 A2 A3 A4 A5 B1 C1 C2 C3 C4 C5 S0 S1 S4 S5 S2 S3 R1 I1; do
+        check "hpcmips ctor row: $v" "$(grep -c "^  \[ok\] $v " "$HPCLOG")" "1"
+    done
+    check "hpcmips ctor rows green" "$(grep -c '^  \[ok\] ' "$HPCLOG")"   "28"
+    check "hpcmips ctor rows red"   "$(grep -c '^  \[FAIL\] ' "$HPCLOG")" "0"
+    check "hpcmips ctor verdict"    "$(grep -c '^HPCMIPS_CTOR_PASS$' "$HPCLOG")" "1"
+fi
+
+
 PITLOG=$LOGDIR/pit8253_latch.log
 python3 pit8253_latch_probe.py "$PMAX" "$STUB" > "$PITLOG" 2>&1 || true
 
```

### 2c. #536 -- `tools/pipeline/check_probe_wiring.py`, HEAD vs the staged blob

```diff
--- a/tools/pipeline/check_probe_wiring.py (HEAD 3c41f01)
+++ b/tools/pipeline/check_probe_wiring.py (#536 staged)
@@ -180,6 +180,13 @@
         (CLASS_TOOL, "#530 pass 2: generates the one-edit variants from the 8bd97e4 blob, each an exact-once replacement"),
     "artifacts/lcalenzerodrop/opus_p2_20260918/scripts/summarize.py":
         (CLASS_TOOL, "#530 pass 2: tabulates score and getenv value per (cell, binary); refuses a leg with no sentinel"),
+    #  #536 wiringcliff: the three editors that produced this round's staged blobs, preserved as run.
+    "artifacts/wiringcliff/r536_20260918/apply536_gate.py":
+        (CLASS_TOOL, "#536: inserts the mk48 + hpcmips sections into gate_arm.sh at a unique anchor; refuses otherwise"),
+    "artifacts/wiringcliff/r536_20260918/apply536_exempt.py":
+        (CLASS_TOOL, "#536: drops the two wired exemptions, re-dates eleven to 2026-09-27, derives the selftest's M5 days"),
+    "artifacts/wiringcliff/r536_20260918/apply536_manifest.py":
+        (CLASS_TOOL, "#536: adds these three MANIFEST lines -- the round's own tools, classified by the round"),
     "artifacts/lcaisalane/opus_c5_20260915/instrument/check_pred.py":
         (CLASS_TOOL, "closing pass 5: checks each mutant's score against its written prediction"),
     "artifacts/lcaisalane/opus_c5_20260915/instrument/disc530c5.py":
@@ -2134,6 +2141,12 @@
 #  owner set the SM dates and set them TIGHTER than the ones proposed, and a deadline nobody
 #  chose is a deadline nobody owns.
 #
+#  *** #536/#537, 2026-09-18: BOTH HALVES OF THAT PAIRING ARE GONE. ***  #537 discharged
+#  fbpending_bound's SM_EXEMPT line -- its self-mutant lane runs now -- and #536 wired
+#  mk48_nvram_probe.py and hpcmips_ctor_probe.py into gate_arm.sh.  The eleven exemptions left
+#  at 2026-09-20 moved to 2026-09-27 BY OWNER RULING, so they again fall due as ONE block: the
+#  cliff `exemptcliff` names is re-created a week out, deliberately and dated, not by copying.
+#
 #  These are wiring jobs, not design ones -- each probe already prints a verdict token and
 #  exits nonzero on failure.  What each needs is a gate that owns it, its rig preconditions,
 #  and ONE clean gate run proving it green before it ships.  That last part is why they are
@@ -2150,25 +2163,27 @@
     #  gate_sh_rounding.sh, whose `-E landisk` machine it already used.  Deleted in the
     #  SAME edit as the wiring, because a wired probe that keeps an exemption is a
     #  STALE EXEMPTION.  Six exemptions remain.
-    "fbpending_drain_probe.py": ("2026-09-20",
+    #  mk48_nvram_probe.py's and hpcmips_ctor_probe.py's exemptions are DISCHARGED, 2026-09-18
+    #  (#536) -- both wired into gate_arm.sh, mk48 on the mvme187 machine that file already
+    #  drives for the PCC2 probes, hpcmips as a construction check with no rig image.  Deleted
+    #  in the SAME edit as the wiring, for the same reason.
+    "fbpending_drain_probe.py": ("2026-09-27",
                                  "REPORT-ONLY by default: EXPECT_CAP must be set before a "
                                  "gate row can mean anything, so wiring is a design step first"),
-    "hpcmips_ctor_probe.py":    ("2026-09-20",
-                                 "rung 2, ~8 s, no rig image -- wants a construction gate"),
     #  Both #494 probes are TWO-LEG DIFFERENTIALS: they take a PRE-FIX binary and
     #  a post-fix one and compare.  No gate builds a second leg, so wiring them is
     #  a change to the instrument -- a single-leg mode asserting only the fix-side
     #  wants against the gate's own binary -- not a line in a gate script.
-    "wdc_altoffset_probe.py":     ("2026-09-20",
+    "wdc_altoffset_probe.py":     ("2026-09-27",
                                    "two-leg differential; wants a single-leg mode "
                                    "before gate 10 can assert anything"),
-    "wdc_altoffset_sig_probe.py": ("2026-09-20",
+    "wdc_altoffset_sig_probe.py": ("2026-09-27",
                                    "two-leg differential AND needs a ciR: CD-ROM rig "
                                    "the battery does not build today"),
-    "wdc_altoffset_4bit_probe.py": ("2026-09-20",
+    "wdc_altoffset_4bit_probe.py": ("2026-09-27",
                                     "two-leg differential; shares the single-leg-mode "
                                     "debt with its two siblings"),
-    "wdc_addtoinbuf_probe.py":     ("2026-09-20",
+    "wdc_addtoinbuf_probe.py":     ("2026-09-27",
                                     "two-leg differential AND needs a poisoned CD "
                                     "image the battery does not build"),
     #  #520's detector.  NOT a two-leg differential and not awaiting a design -- it is a
@@ -2184,21 +2199,17 @@
     #  *** ITS REASON EXPIRES WITH THE rlwimi/rldimi WIRING: gate_ppc.sh now EXECUTES -M 64. ***
     #  What remains is the instrument: this probe prints no RESULT/CONTROL lines, so a gate
     #  could only score its exit status, which gates here never trust.
-    "ppc_rldicl_probe.py":         ("2026-09-20",
+    "ppc_rldicl_probe.py":         ("2026-09-27",
                                     "gate_ppc.sh now executes -M 64 (rlwimi/rldimi); this "
                                     "probe lacks the RESULT/CONTROL protocol a gate parses "
                                     "-- that instrument change is filed to wiringcliff"),
-    "mk48_nvram_probe.py":         ("2026-09-20",
-                                    "no gate drives mvme88k/mvme187; gate_m88k_rounding.sh "
-                                    "is the named home and giving it an mvme187 leg is a "
-                                    "harness round, filed to wiringcliff"),
-    "alpha_tbi_probe.py":          ("2026-09-20",
+    "alpha_tbi_probe.py":          ("2026-09-27",
                                     "no gate runs an Alpha machine; gate_crossfamily.sh "
                                     "is the named home and giving it one is a harness "
                                     "round, filed to wiringcliff"),
     #  #518's detector.  Same footing as #520's, and deliberately the same date so the
     #  cliff stays one date: a single-leg 75-row instrument, green on the fix, with no HOME.
-    "lca_badval_probe.py":         ("2026-09-20",
+    "lca_badval_probe.py":         ("2026-09-27",
                                     "no gate runs an Alpha machine; gate_crossfamily.sh "
                                     "is the named home, filed to wiringcliff with #520"),
     #  #530's detector.  Same footing and the same date as #518's: single-leg, green on the
@@ -2206,10 +2217,10 @@
     #  #530's width row.  SAME footing and SAME date as lca_isalane_probe.py below: no gate in this
     #  tree runs an Alpha machine, and a later date would hide the debt behind the cliff instead of
     #  joining it.  Adding it here is stated in #530's record, not done silently.
-    "lca_widewrite_probe.py":      ("2026-09-20",
+    "lca_widewrite_probe.py":      ("2026-09-27",
                                     "no gate runs an Alpha machine; gate_crossfamily.sh "
                                     "is the named home, filed to wiringcliff with #518/#520/#530"),
-    "lca_isalane_probe.py":        ("2026-09-20",
+    "lca_isalane_probe.py":        ("2026-09-27",
                                     "no gate runs an Alpha machine; gate_crossfamily.sh "
                                     "is the named home, filed to wiringcliff with #518/#520"),
     #  #531's detector, and it takes the SAME footing and the SAME date as #518/#520/#530
@@ -2222,7 +2233,7 @@
     #  after which the checker verifies it is ungated -- and named it a check that cannot
     #  fail.  This entry is the honest form: DETECTOR, ungated, dated, and filed. ***
     "artifacts/ip30abortkill/ip30_abort_probe.py":
-                                   ("2026-09-20",
+                                   ("2026-09-27",
                                     "no gate runs an SGI IP30 guest session (gate_asan_sweep.sh "
                                     "constructs only); filed to wiringcliff with #518/#520/#530"),
 }
@@ -2803,11 +2814,28 @@
     case("M4  a WITNESS wired into a gate reddens", 1,
          "GATED WITNESS  sh4pcic_witness.py", chk, rg)
 
-    rg, chk = fresh()
-    case("M5a a live exemption is GREEN the day before", 0, "PROBEWIRING_PASS", chk, rg,
-         extra=("--today", "2026-09-19"))
-    case("M5b the same tree is RED the day after", 1, "EXPIRED EXEMPTION", chk, rg,
-         extra=("--today", "2026-09-21"))
+    #  #536: THE TWO DAYS ARE DERIVED FROM THE TABLE, NEVER LITERALS.  They were 2026-09-19 and
+    #  2026-09-21, the days either side of the block every dated exemption then shared -- so
+    #  the day that block was re-dated, M5b would have run on a tree with nothing expired, gone
+    #  GREEN, and failed the selftest.  The frozen-claim-about-a-table-designed-to-change that
+    #  _pick_exempt_detector() refuses for M1-M3, one mutant group further down.  The
+    #  comparison is `d < today`, so an exemption is valid ON its stamped date: the earliest
+    #  DETECTOR date minus one day is green and plus one day is red.  No dated detector
+    #  exemption left is two FAILS, never a skip -- the denominator must not shrink.
+    _m5 = sorted(EXEMPT[_n][0] for _n in EXEMPT
+                 if MANIFEST.get(_n, (None,))[0] == CLASS_DETECTOR
+                 and DATE_RE.match(EXEMPT[_n][0] or ""))
+    if not _m5:
+        results.extend([False, False])
+        print("  FAIL  M5a/M5b -- no well-formed dated DETECTOR exemption to derive the days from.")
+    else:
+        import datetime as _dt5
+        _d5 = _dt5.date.fromisoformat(_m5[0])
+        rg, chk = fresh()
+        case("M5a a live exemption is GREEN the day before", 0, "PROBEWIRING_PASS", chk, rg,
+             extra=("--today", (_d5 - _dt5.timedelta(days=1)).isoformat()))
+        case("M5b the same tree is RED the day after", 1, "EXPIRED EXEMPTION", chk, rg,
+             extra=("--today", (_d5 + _dt5.timedelta(days=1)).isoformat()))
 
     for tag, bad in (("M5c unpadded (the ieee_store shape)", '"2026-9-20"'),
                      ("M5d empty", '""'),
```

**File disclosure (§F):**

```
files this pass reviews (NON-BLANK added / removed lines vs HEAD 3c41f01; the diffs are inlined, count them)  -- disposition
5	1	regress/diff_fbpending_bound.c   INLINED (2a)
18	4	regress/gate_offline.sh   INLINED (2a)
3	0	regress/selfmutants/fbpending_bound.why   INLINED (2a)
35	0	regress/gate_arm.sh   INLINED (2b)
50	22	tools/pipeline/check_probe_wiring.py   INLINED (2c)
NEW, not shown: regress/artifacts/wiringcliff/r536_20260918/ (the three editors, the section file, dry-run and checker logs)
  and regress/artifacts/fbsmlane/r537_20260918/ (the driver and both runs' outputs) -- SUMMARIZED in section 3.
NOT SHOWN: the round records (CHANGELOG block, ledger rows), written after this pass.  The working tree's
uncommitted #529 hunks in gate_arm.sh / check_probe_wiring.py belong to neither round and are not staged.
```

---

## 3. SETTLED PREMISES (measured this round; re-derive any you doubt)

**#537, `regress/artifacts/fbsmlane/r537_20260918/` (the driver `run537.sh` and every arm's full output).**  One run of
five arms, WSL Gentoo, 221 build/ objects linked (build/gxemul of 08:49 today):

    arm  what                                                    helper verdict (its own words)
    L0   post-fix harness, the gate's exact lane call            SELFMUTANT_OK  -- "pristine arm through the same tree:
                                                                 FBBOUND_PASS, row id unique and green" / "mutant killed by
                                                                 the named row: FAIL R4 every case bounded ... 7 row failure(s)"
    L1   PRE-FIX: HEAD's harness (prints FBBOUND_VERDICT=PASS)   SELFMUTANT_SETUP -- "pristine arm did not PASS through the
         through the same lane                                   mutant tree shape"  (the fbsmlane symptom, reproduced)
    N1   post-fix harness with R3 `worst_trough >= 1` -> `>= 0`  SELFMUTANT_FAIL -- "mutant applied but the detector did NOT
         (the detector blinded to the mutant)                    report a failure"  (the lane reds when the detector goes blind)
    N2   post-fix harness, ABSOLUTE -I$SEC/src/... in place of   SELFMUTANT_SETUP -- "both arms produced a byte-identical
         the relative ../src/...                                 binary"  (the claim the new gate comment makes)
    D0   the harness built as gate 2's #442 lane builds it       with the depth argument: 28 rows, IDENTITY ok, FBBOUND_PASS;
                                                                 WITHOUT it (as the lane runs it): 27 rows, IDENTITY ok,
                                                                 FBBOUND_PASS; FBBOUND_VERDICT lines: 0

*Disclosed: a first run of the same driver SETUP'd L1 and N1 on a compile error -- its scratch copies lacked the
configure-generated `GXEMUL-SEC/config.h`, which `src/include/misc.h` includes as `"../../config.h"`.  The helper's own
mirror reaches it through its SYMLINKED `src/include`, so L0 and N2 were unaffected.  The driver was fixed (copy
`config.h`) and re-run whole; run 1's outputs are preserved beside run 2's as `out_run1_apparatus_defect/`.*

**#536, `regress/artifacts/wiringcliff/r536_20260918/`.**  In a scratch tree built from HEAD `3c41f01`'s tracked `regress/`
(every script plus every artifact `.py`) with both #536 edits applied:

* `check_probe_wiring.py` (re-run at HEAD `3c41f01`): PASS, `70/81 detectors run by a gate, 11 dated-exempt, 32 witnesses
  correctly ungated`;
  `--today 2026-09-26` PASS; `--today 2026-09-28` FAIL naming exactly these eleven, each `came due 2026-09-27`:
  alpha_tbi_probe.py, artifacts/ip30abortkill/ip30_abort_probe.py, fbpending_drain_probe.py, lca_badval_probe.py,
  lca_isalane_probe.py, lca_widewrite_probe.py, ppc_rldicl_probe.py, wdc_addtoinbuf_probe.py,
  wdc_altoffset_4bit_probe.py, wdc_altoffset_probe.py, wdc_altoffset_sig_probe.py.
* Negative controls on the WIRING: HEAD's checker + the new gate_arm.sh -> `STALE EXEMPTION` for exactly the two wired
  probes (`hpcmips_ctor_probe.py is RUN by gate_arm.sh:1617`, `mk48_nvram_probe.py is RUN by gate_arm.sh:1598`), so the
  checker SEES both invocations; the new checker + HEAD's gate_arm.sh -> `UNWIRED DETECTOR` for exactly those two.
* `--selftest`: `PROBEWIRING_SELFTEST_PASS 22/22`, M5a `rc=0 want=0`, M5b `rc=1 want=1`.
* Negative control on the M5 DERIVATION: the same re-dated table with M5a/M5b's OLD literals (2026-09-19 / 2026-09-21)
  -> `PROBEWIRING_SELFTEST_FAIL 21/22`, `FAIL M5b the same tree is RED the day after rc=0 want=1`.  So the derivation is
  load-bearing, not tidying.
* The two new gate sections, dry-run against the probes' real logs on build/gxemul (mk48 57/57, hpcmips 28/28): 93/93
  checks green; one flipped row in each log reddens its section and names the row.
* Both #536 edits COMMUTE with the uncommitted #529 hunks in the same two files (HEAD+536+529 == working tree+536, by
  `cmp`), so the commit ships #536 alone.
* **The gates themselves (gate_offline.sh with the new lane, gate_arm.sh with the new sections) run AFTER this pass**,
  alone on the machine -- this project runs no gate concurrently with a panel.

---

## 4. QUESTIONS

**Q1 -- premise audit.  Each of these is load-bearing; tell me which is false.**

* (P1) The lane compiles the MIRROR's mutated `dev_footbridge.c`, not GXEMUL-SEC's, because the harness's
  `#include "dev_footbridge.c"` resolves through `-I../src/devices`, relative to the lane's working directory
  `<mirror>/regress`.  The helper's own compile line comes first and is
  `gcc -O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -I../src -I../src/include
  -I../src/include/thirdparty -ffunction-sections -fdata-sections -Wl,--gc-sections <EXTRA> -o <bin> <harness> -lm`,
  and none of ITS -I directories holds a dev_footbridge.c.  Is that the resolution gcc performs?  Does the fact
  that `<mirror>/regress/diff_fbpending_bound.c` is itself a SYMLINK into GXEMUL-SEC/regress change it?
* (P2) The helper runs the built harness with NO arguments, so row R2 (which needs a depth argument) is SKIPPED
  and the harness's IDENTITY row expects its shallow count -- and the pinned R4 still goes red under the mutant.
* (P3) `-O2` differs between the lane and gate 2's own build of this harness only by the extra
  `-D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections -Wl,--gc-sections` and by
  `-std=c99` being overridden by the later `-std=gnu99`.  Does any of those change what the harness measures?
* (P4) When build/ has NO objects, gate 2's main #442 lane prints a NOTE ("SKIPPED, not passed") and adds no
  check, while the new lane will RED (the pristine arm fails to link -> SETUP).  Is that asymmetry right, or
  should the lane skip the same way?  (A skip that reads as a pass is this project's fifth vacuity class; a
  red on a machine without build/ is noise.)
* (P5) M5a/M5b now derive their two days from the EARLIEST dated DETECTOR exemption, because expiry is only
  evaluated for DETECTOR entries (the checker's witness branch never reads an EXEMPT date).  Is the population
  right?  (The selftest refuses to start -- `PROBEWIRING_SELFTEST_SETUP` -- unless every MANIFEST file is on
  disk, so the earliest-dated detector is always present in its copy.  Check that claim too.)

**Q2 -- candidate weakenings.  For each, say whether gate 2 / gate_arm.sh / precommit still passes, and which
check line (if any) goes red.**

  (a) the harness prints `FBBOUND_PASS` unconditionally (`printf("\nFBBOUND_PASS\n")`)
  (b) gate 2's #442 verdict row greps `FBBOUND_` instead of `^FBBOUND_PASS$`
  (c) the lane's EXTRA flags drop `! -name 'dev_footbridge.o'` from the object list
  (d) R4's condition becomes `failures <= 1`
  (e) gate_arm.sh's mk48 section loses `"$PMAX"` (the probe then runs with no binary argument)
  (f) M5b's derivation uses the LATEST dated exemption instead of the earliest

**Q3 -- option-set completeness.**  #537 renamed the token (one verdict line, the house form) rather than
printing a second token beside the old one.  #536 wired two and re-dated eleven as ONE block again, one week
out, by ruling.  Is there a disposition neither round named?  (The owner's rulings stand; name the member
anyway if it exists.)

**Standing licence:** if, while verifying a claim, you found something ELSE — say so.

---

## 5. SETTLED ELSEWHERE -- do not re-derive

* The stray line removed from gate_offline.sh, `' ' ') -lm -L/usr/X11R6/lib -lX11"`, ran a command named `' '`
  with one long argument: its second `'` opened a quote that closed at the apostrophe in `run.sh's` six lines
  down, and every line inside was a comment (blank, `#  THE MANIFEST ...`, `#`, `#  Without it ...`,
  `#  is EXACTLY how ...`, `#  Same idiom as run.sh's`).  `command not found`, rc 127; the gate has no `set -e`.
  No code was swallowed, so removing it changes nothing else.
* `diff_fbpending_bound.c` is the only differential gate 2 builds against build/ objects (gate_offline.sh has
  exactly two `build/src` references, the lane and the #442 main lane).

## 6. FROZEN COPIES (file-reading seats: open these, not the working files)

Frozen at build time; file-reading seats open THESE, never the working files (absolute paths, outside the repo):

    C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\p2_536_537\frozen\check_probe_wiring.staged.py
        #536 the STAGED blob: HEAD 3c41f01 + the EXEMPT edit + the M5 derivation
    C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\p2_536_537\frozen\diff_fbpending_bound.c
        #537 harness, post-fix (the working tree carries only #537 in this file)
    C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\p2_536_537\frozen\fbpending_bound.why
        #537 the mutant's rationale, +1 line
    C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\p2_536_537\frozen\gate_arm.staged.sh
        #536 the STAGED blob: HEAD 3c41f01 + the two sections (NOT the working tree, which also carries #529)
    C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\p2_536_537\frozen\gate_offline.sh
        #537 gate 2, post-fix (the working tree carries only #537 in this file)
    C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\p2_536_537\frozen\run537.sh
        #537 the measurement driver, as run (run 2)
    C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\p2_536_537\frozen\run537_SUMMARY.txt
        #537 the five arms' verdicts
    C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\p2_536_537\frozen\selftest_536_NEG_literals.txt
        #536 the negative control: the re-dated table with M5a/M5b's old literal days
    C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\p2_536_537\frozen\selftest_536_at_3c41f01.txt
        #536 --selftest of the staged checker in a scratch tree of HEAD 3c41f01


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
