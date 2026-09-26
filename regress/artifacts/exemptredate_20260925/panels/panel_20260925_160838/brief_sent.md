# PASS 2 -- `#550` exemptredate and `#551` wdcidselfcheck: the FINAL diffs, as they will be committed

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`** (and its `regress/`, `tools/`).  There are THREE
pristine-2021-upstream copies of GXemul under the project root (`./src/` and two under
`_archive/audit-results-*/builds/`).  They are NOT this fork.  If your line numbers
disagree with mine by hundreds you are reading one of them — say so rather than
reconciling.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — a date, a count, a schedule — ENUMERATE it rather than reasoning
about it.**  And **ENUMERATE THE RIGHT DOMAIN** — a domain is itself a premise.

**VERDICT LINE FIRST** -- `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>` for EACH round (two lines), so your
answer survives truncation.

## 1. WHAT THESE TWO ROUNDS ARE (no emulator code changes in either)

* **`#550` exemptredate.**  `tools/pipeline/check_probe_wiring.py` holds an `EXEMPT` table of probes that no gate runs
  yet, each with a date; an entry is valid ON its date and red the day after, and any red blocks EVERY commit (the
  precommit hook runs the checker).  Ten entries were all dated 2026-09-27 -- a cliff that would have blocked every
  commit from 2026-09-28.  `#550` re-dates them ONE BY ONE, each with its own owed work, and re-dates gate 2's
  `SC_EXEMPT` entry for `ieee_store` (`regress/gate_offline.sh`).
* **`#551` wdcidselfcheck.**  Gate 2 (`regress/gate_offline.sh`) requires each differential it runs either to carry a
  SELFCHECK -- a block that feeds the file's comparators known answers and proves they can still fail -- or to be
  dated-exempt.  `regress/diff_wdc_identify.c` (128 rows) was exempt.  `#551` gives it a self-check on its two
  comparators (`chk()` and a new pure `row_cmp()` split out of `row()`), run FIRST and LAST, and moves it from
  `SC_EXEMPT` to `SC_COVERED`.

## 2. SETTLED PREMISES, RE-INLINED SO NOBODY SPENDS AN ANSWER RE-DERIVING THEM

* **Owner ruling 2026-09-24, verbatim:** "Re-date all ten individually -- each gets its own date and reason now; no
  wiring work this week."  **Owner ruling 2026-09-25:** "Fix wdc_identify now ... done before 09-28.  Only ieee_store
  gets re-dated."  **And #551's scope, owner ruling 2026-09-25:** "24/128 now, file the rest".
* **The checker compares `d < today`** (string compare of ISO dates): valid ON the date, red the next day; an expired
  entry stays in the failure list.  Gate 2's `SC_EXEMPT` expiry reds one gate-2 row, not every commit.
* **Both rounds had a pass 1 and an F2 adjudication before this diff** (panels `panel_20260925_141424` / `_144644` for
  #550 and `_141428` / `_144647` for #551; durable copies under `regress/artifacts/exemptredate_20260925/panels/` and
  `regress/artifacts/wdcidselfcheck_20260925/panels/`).  The Fable 5.1 adjudication of both F2 passes is
  `regress/artifacts/exemptredate_20260925/fable5_f2_550_551.md`: **#550 SHIP WITH CHANGES, 8 of 14 dispositions
  changed; #551 PROCEED WITH CHANGES, 6 of 9 changed.**  THIS diff is the one written to those rulings.  Its main
  instructions, condensed (the file has them in full):
  - #550: split, do not narrow, the per-entry "valid ON / RED from" sentences (R1); a dated supersession line for the
    stale wdc_identify paragraph, quoting it (R2); ieee_store's census is NINE counters, at both sites (R3); ip30's
    reason names the 12 s death poll that cannot simply shrink (R6); 4bit/sig owe an ORACLE, not a single-leg mode,
    and sig's "ciR: image the battery does not build" is false (R7); name the rows `wdcaltoffleg` (a)/(b)/(c) and
    `wdcsingleleg` (R9); the schedule -- weekly Thursdays in owed-work order, the four Alpha probes on consecutive
    days (one owed round: a gate home for `-E alpha -e alphabook1`), 11-26 skipped, ieee_store 12-10 (S1); file
    `exemptdistinct` and widen the header sentence (S2); commit by swapping EVERY edited file that carries another
    unit's parked hunk (S4); and the checker's "--selftest applies 18 mutants" -> 22 as an L4 rider.
  - #551: adopt the Opus seat's "Q" design -- a PURE `row_cmp(why, sectors, got57, got60)` (row()'s eight call sites
    unchanged, byte-identical output); `chk()` probed at (1,2) (2^32,0) (0,1) (0,2^32) must fail and (7,7) must not;
    `row_cmp` at 57-wrong-alone, 60-wrong-alone, zero, and a match; EXACT increments; print RUNTIME call counts, never
    "24 of 128" from a counter; print the G text ONCE, from the last run, only if both runs passed; no sentinel line
    may contain "high byte" or the self-mutant row's text; the stateful pre-`rows ++` edit DISCLOSED; the gate-2
    heading loses its count; the stale paragraph is replaced by a record quoting it; the rest is filed as
    `wdcidcomparators`.
* **What gate 2 greps (and so what #551's lines must and must not contain):** `grep -q 'SELFCHECK the comparator can
  still fail' "$LOGDIR/diff_$_stem.log"` (the G row, per stem); the `@@SELFCHECK@@` token (the H row); `grep -c 'high
  byte'` pinned at 1 on this log; and the self-mutant lane needs exactly one untagged pristine line.
* **The working tree ALSO carries other units' uncommitted hunks** in `check_probe_wiring.py` and
  `precommit_check.sh` (#529's parked lines, #549's manifest line).  The diffs below are #550's and #551's OWN --
  generated against HEAD from the exact blobs that will be committed -- and nothing else.

## 3. THE FILES, DISCLOSED (`git diff --numstat` of the rounds' own blobs against HEAD)

    #550  tools/pipeline/check_probe_wiring.py   INLINED (diff550v2_cpw.diff)
    #550  tools/precommit_check.sh               INLINED (diff550v2_pcc.diff)
    #550  regress/gate_offline.sh                INLINED (diff550v2_goff.diff)
    #551  regress/diff_wdc_identify.c            INLINED (diff551_wdcid.diff, against HEAD)
    #551  regress/gate_offline.sh                INLINED (diff551_goff_on550.diff, on top of #550's version)
    records (CHANGELOG.md, OUTSTANDING_BUGS.md, ledger.json)   NOT SHOWN -- not written yet; they follow this pass

## 4. MEASURED

* **#550, the schedule** -- the checker run on a HEAD export with #550 applied, at `--today` each step date
  (`regress/artifacts/exemptredate_20260925/measured/schedule_v2.out`), verbatim:


```
2026-09-25 rc=0 PROBEWIRING_PASS  71/81 detectors  | 
2026-09-28 rc=0 PROBEWIRING_PASS  71/81 detectors  | 
2026-10-08 rc=0 PROBEWIRING_PASS  71/81 detectors  | 
2026-10-09 rc=1 PROBEWIRING_FAIL  1 problem(s); 71 | ppc_rldicl_probe.py 
2026-10-16 rc=1 PROBEWIRING_FAIL  2 problem(s); 71 | ip30_abort_probe.py ppc_rldicl_probe.py 
2026-10-23 rc=1 PROBEWIRING_FAIL  3 problem(s); 71 | alpha_tbi_probe.py ip30_abort_probe.py ppc_rldicl_probe.py 
2026-10-24 rc=1 PROBEWIRING_FAIL  4 problem(s); 71 | alpha_tbi_probe.py ip30_abort_probe.py lca_badval_probe.py ppc_rldicl_probe.py 
2026-10-27 rc=1 PROBEWIRING_FAIL  5 problem(s); 71 | alpha_tbi_probe.py ip30_abort_probe.py lca_badval_probe.py lca_widewrite_probe.py ppc_rldicl_probe.py 
2026-10-28 rc=1 PROBEWIRING_FAIL  6 problem(s); 71 | alpha_tbi_probe.py ip30_abort_probe.py lca_badval_probe.py lca_isalane_probe.py lca_widewrite_probe.py ppc_rldicl_probe.py 
2026-11-06 rc=1 PROBEWIRING_FAIL  7 problem(s); 71 | alpha_tbi_probe.py ip30_abort_probe.py lca_badval_probe.py lca_isalane_probe.py lca_widewrite_probe.py ppc_rldicl_probe.py wdc_altoffset_probe.py 
2026-11-13 rc=1 PROBEWIRING_FAIL  8 problem(s); 71 | alpha_tbi_probe.py ip30_abort_probe.py lca_badval_probe.py lca_isalane_probe.py lca_widewrite_probe.py ppc_rldicl_probe.py wdc_altoffset_4bit_probe.py wdc_altoffset_probe.py 
2026-11-20 rc=1 PROBEWIRING_FAIL  9 problem(s); 71 | alpha_tbi_probe.py ip30_abort_probe.py lca_badval_probe.py lca_isalane_probe.py lca_widewrite_probe.py ppc_rldicl_probe.py wdc_altoffset_4bit_probe.py wdc_altoffset_probe.py wdc_altoffset_sig_probe.py 
2026-12-03 rc=1 PROBEWIRING_FAIL  9 problem(s); 71 | alpha_tbi_probe.py ip30_abort_probe.py lca_badval_probe.py lca_isalane_probe.py lca_widewrite_probe.py ppc_rldicl_probe.py wdc_altoffset_4bit_probe.py wdc_altoffset_probe.py wdc_altoffset_sig_probe.py 
2026-12-04 rc=1 PROBEWIRING_FAIL  10 problem(s); 7 | alpha_tbi_probe.py ip30_abort_probe.py lca_badval_probe.py lca_isalane_probe.py lca_widewrite_probe.py ppc_rldicl_probe.py wdc_addtoinbuf_probe.py wdc_altoffset_4bit_probe.py wdc_altoffset_probe.py wdc_altoffset_sig_probe.py 
```


* **#550, the checker's own selftest on that export: `PROBEWIRING_SELFTEST_PASS  22/22 mutants behaved as specified`**
  (`measured/selftest_550v2_onHEAD.out`).
* **#551, equivalence** -- the new `diff_wdc_identify.c` against HEAD's, built at -O2 (gate 2's line) and -O0 (with a
  one-line `quiet_mode` stub linked into BOTH arms), on the real `dev_wdc.c` and six variants (the self-mutant, the
  `% 255` revert, a 13-bit cylinder truncation, the pre-#481 reset bit, DRQ dropped, word 57's high byte zeroed): stdout
  byte-identical except the SELFCHECK lines, same exit code, all 14 pairs
  (`regress/artifacts/wdcidselfcheck_20260925/measured/run551v2.out`).
* **#551, the controls** (same file): `chk()` stubbed -> red; `row_cmp()` stubbed -> red; the block deleted -> the run
  prints no G line and no token -- the two things gate 2's G and H rows grep for (read in gate_offline.sh, NOT run
  through gate 2 on that variant); each `row_cmp` disjunct dropped ALONE -> red; `&& got` added to `chk()` -> red.  The disclosed stateful edit (`&& (rows & 127) < 2` before `rows ++`) -> every row green, as disclosed.
* **#551, ONE RESULT AGAINST THE RULING'S EXPECTATION.**  The ruling said the block's own forced failure removed
  (`scnoforce`) must still "go red through `failures`".  Measured: `scnoforce` ALONE changes nothing on a working
  comparator (the forced failure is only reached when a probe answers wrongly), and `scnoforce` + `chk()` stubbed
  prints `FAIL  SELFCHECK(first)` and `(last)`, NO G line -- and the run's own trailer reads `128 rows, 0 failures` /
  `WDC_IDENTIFY_PASS`.  So that double edit is caught ONLY by gate 2's G row (the missing "can still fail" line -- by
  reading gate 2's grep; the variant was not run through gate 2 itself), not through `failures`.  The G row exists for exactly this, but the ruling's sentence is not what happens.
* **Gate 2 with #550 + #551 in the tree, run ALONE: `offline-differential: PASS (359 checks)`, rc 0, 181 s**
  (`regress/artifacts/wdcidselfcheck_20260925/gates/gate2.out`).  In `diff_wdc_identify.log`: `ok    SELFCHECK(first):
  all 9 probes answered right`, `ok    SELFCHECK the comparator can still fail (first and last)`, `note  SELFCHECK
  comparator calls this run: chk() 24, row_cmp() 8`, `128 rows, 0 failures`.

## 5. THE DIFFS (verbatim)


### 5a. #550 -- tools/pipeline/check_probe_wiring.py (HEAD -> #550)

```diff
--- -	2026-09-25 16:05:41.521512300 -0500
+++ /c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/exempt550/cpw_550v2_onHEAD.py	2026-09-25 15:25:31.379707400 -0500
@@ -100,7 +100,7 @@
 *** --selftest IS PART OF THE CHECK, NOT A CONVENIENCE. ***  A gate that cannot be shown to
 go RED is the vacuity class this project names first, and "I ran the mutants once" is a
 remembered grep -- the mrwstore2 shape, where a round's witness left no artefact and a later
-row had to re-cost the work.  `--selftest` applies 18 mutants to COPIES in a temp directory
+row had to re-cost the work.  `--selftest` applies 22 mutants to COPIES in a temp directory
 (never the repo) and asserts the exit status of each.  It is re-runnable by someone who was
 not there, which is the only kind of measurement that survives.
 
@@ -2505,6 +2505,14 @@
 #  *** #548, 2026-09-24: THE OTHER HALF IS GONE TOO. ***  fbpending_drain_probe.py is wired
 #  into gate_arm.sh and its entry deleted, so TEN of those eleven remain, still one block.
 #
+#  *** #550, 2026-09-25: THE BLOCK IS DISPERSED, BY OWNER RULING 2026-09-24. ***  Each of the ten
+#  carries its OWN date, 2026-10-08 to 2026-12-03, and a `#550' line above it giving the reason for
+#  THAT date, in owed-work order: the cheapest first; the four Alpha probes within days of each other,
+#  because one round discharges all four; the four wdc probes a week or more apart, each owing its own
+#  oracle.  NOTHING ENFORCES DISTINCT DATES -- this checker reads each date alone -- and "no date on
+#  another list's date" is a cross-list property no check here sees (gate 9's AB_EXEMPT holds twelve
+#  entries on one date).  Filed as `exemptdistinct'.
+#
 #  These are wiring jobs, not design ones.  NOT every probe here prints a verdict token or exits
 #  nonzero on failure: mk48_nvram_probe.py printed MK48_RESULT=n/m and a DONE sentinel and exited 0
 #  with rows red, so the gate_arm.sh section #536 wired for it scores ROWS, not a token (agy, #536
@@ -2519,11 +2527,11 @@
     #  bump note named for it ("wants an operator who can run that gate").  The entry is
     #  DELETED rather than dated forward, in the SAME edit that added the wiring, because a
     #  wired probe that keeps an exemption is a STALE EXEMPTION and this checker reds on it.
-    #  Seven exemptions remain.
+    #  Seven exemptions remained then.
     #  sh4_bsc_width_probe.py's exemption is DISCHARGED, 2026-08-30 -- wired into
     #  gate_sh_rounding.sh, whose `-E landisk` machine it already used.  Deleted in the
     #  SAME edit as the wiring, because a wired probe that keeps an exemption is a
-    #  STALE EXEMPTION.  Six exemptions remain.
+    #  STALE EXEMPTION.  Six exemptions remained then.
     #  mk48_nvram_probe.py's and hpcmips_ctor_probe.py's exemptions are DISCHARGED, 2026-09-18
     #  (#536) -- both wired into gate_arm.sh, mk48 on the mvme187 machine that file already
     #  drives for the PCC2 probes, hpcmips as a construction check with no rig image.  Deleted
@@ -2535,63 +2543,81 @@
     #  a post-fix one and compare.  No gate builds a second leg, so wiring them is
     #  a change to the instrument -- a single-leg mode asserting only the fix-side
     #  wants against the gate's own binary -- not a line in a gate script.
-    "wdc_altoffset_probe.py":     ("2026-09-27",
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): owes a single-leg ORACLE -- its `ok' needs both legs (b_hit and f_hit) -- queue row `wdcaltoffleg' (a).
+    "wdc_altoffset_probe.py":     ("2026-11-05",
                                    "two-leg differential; wants a single-leg mode "
                                    "before gate 10 can assert anything"),
-    "wdc_altoffset_sig_probe.py": ("2026-09-27",
-                                   "two-leg differential AND needs a ciR: CD-ROM rig "
-                                   "the battery does not build today"),
-    "wdc_altoffset_4bit_probe.py": ("2026-09-27",
-                                    "two-leg differential; shares the single-leg-mode "
-                                    "debt with its two siblings"),
-    "wdc_addtoinbuf_probe.py":     ("2026-09-27",
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): owes a redesign -- its oracle cannot tell the outcomes apart -- `wdcaltoffleg' (c).
+    #  (Its tuple said it needs "a ciR: CD-ROM rig the battery does not build" until #550: false -- the
+    #  probe applies the ciR: prefix itself and gate 10 already carries the malta image.)
+    "wdc_altoffset_sig_probe.py": ("2026-11-19",
+                                   "two-leg differential; its oracle cannot tell the "
+                                   "outcomes apart -- a redesign, wdcaltoffleg (c)"),
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): owes an oracle choice: its want-None cells are recorded, not predicted -- `wdcaltoffleg' (b).
+    "wdc_altoffset_4bit_probe.py": ("2026-11-12",
+                                    "two-leg differential; owes an oracle choice, "
+                                    "wdcaltoffleg (b)"),
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): two-leg AND needs a poisoned CD image the battery does not build -- queue row `wdcsingleleg'.
+    "wdc_addtoinbuf_probe.py":     ("2026-12-03",
                                     "two-leg differential AND needs a poisoned CD "
                                     "image the battery does not build"),
-    #  #520's detector.  NOT a two-leg differential and not awaiting a design -- it is a
-    #  single-leg 15-row instrument that runs green on the fix today.  What it lacks is a
-    #  HOME: no gate in this tree runs an Alpha machine at all.  Dated to fall due with
-    #  the others so the cliff stays one date rather than becoming a rolling excuse.
     #  #522's detector.  Single-leg, 0.2 s, green on the fix.  It lacks a gate that RUNS a
     #  64-bit PowerPC CPU: gate 9 constructs them but has no result oracle, and both PowerPC
     #  gates drive a 32-bit part.  Closing that is a harness round, filed to wiringcliff.
     #  *** ITS REASON EXPIRES WITH THE rlwimi/rldimi WIRING: gate_ppc.sh now EXECUTES -M 64. ***
-    #  What remains is the instrument: this probe prints no RESULT/CONTROL lines, so a gate
-    #  could only score its exit status, which gates here never trust.
-    "ppc_rldicl_probe.py":         ("2026-09-27",
+    #  What remains is the instrument: this probe prints no RESULT/CONTROL lines.  (This sentence went
+    #  on "so a gate could only score its exit status" until #550: false -- it prints ok/FAIL rows,
+    #  `SCORE n/m' and a DONE line, which a gate can score by rows, as gate_arm.sh scores mk48's.)
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): the cheapest of the ten -- 24/24 in under a second on a machine gate_ppc.sh already runs;
+    #  owed: RESULT/CONTROL lines, then a gate_ppc.sh block beside rldimi/rlwimi.  The parked
+    #  working-tree edit of its want_rldimi touches no scored row and is no prerequisite.
+    "ppc_rldicl_probe.py":         ("2026-10-08",
                                     "gate_ppc.sh now executes -M 64 (rlwimi/rldimi); this "
                                     "probe lacks the RESULT/CONTROL protocol a gate parses "
                                     "-- that instrument change is filed to wiringcliff"),
-    "alpha_tbi_probe.py":          ("2026-09-27",
+    #  #520's detector.  NOT a two-leg differential and not awaiting a design -- it is a
+    #  single-leg 15-row instrument that runs green on the fix today.  What it lacks is a
+    #  HOME: no gate in this tree runs an Alpha machine at all.
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): one harness round gives an `-E alpha -e alphabook1' session a gate home and discharges
+    #  all four Alpha probes at once (each already prints its tokens and sends quit), so the four
+    #  are ONE decision, dated within days of each other rather than a week apart.
+    "alpha_tbi_probe.py":          ("2026-10-22",
                                     "no gate runs an Alpha machine; gate_crossfamily.sh "
                                     "is the named home and giving it one is a harness "
                                     "round, filed to wiringcliff"),
-    #  #518's detector.  Same footing as #520's, and deliberately the same date so the
-    #  cliff stays one date: a single-leg 75-row instrument, green on the fix, with no HOME.
-    "lca_badval_probe.py":         ("2026-09-27",
+    #  #518's detector.  Same footing as #520's: a single-leg 75-row instrument, green on the
+    #  fix, with no HOME.
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): the same alphabook1 home as alpha_tbi: one round discharges all four, so they fall due together.
+    "lca_badval_probe.py":         ("2026-10-23",
                                     "no gate runs an Alpha machine; gate_crossfamily.sh "
                                     "is the named home, filed to wiringcliff with #520"),
-    #  #530's detector.  Same footing and the same date as #518's: single-leg, green on the
-    #  fix, and no gate in this tree runs an Alpha machine.
-    #  #530's width row.  SAME footing and SAME date as lca_isalane_probe.py below: no gate in this
-    #  tree runs an Alpha machine, and a later date would hide the debt behind the cliff instead of
-    #  joining it.  Adding it here is stated in #530's record, not done silently.
-    "lca_widewrite_probe.py":      ("2026-09-27",
+    #  #530's detector.  Same footing as #518's: single-leg, green on the fix, and no gate in
+    #  this tree runs an Alpha machine.
+    #  #530's width row.  SAME footing as lca_isalane_probe.py below: no gate in this tree runs an
+    #  Alpha machine.  Adding it here is stated in #530's record, not done silently.
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): the same alphabook1 home as alpha_tbi: one round discharges all four, so they fall due together.
+    "lca_widewrite_probe.py":      ("2026-10-26",
                                     "no gate runs an Alpha machine; gate_crossfamily.sh "
                                     "is the named home, filed to wiringcliff with #518/#520/#530"),
-    "lca_isalane_probe.py":        ("2026-09-27",
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): the same alphabook1 home as alpha_tbi: one round discharges all four, so they fall due together.
+    "lca_isalane_probe.py":        ("2026-10-27",
                                     "no gate runs an Alpha machine; gate_crossfamily.sh "
                                     "is the named home, filed to wiringcliff with #518/#520"),
-    #  #531's detector, and it takes the SAME footing and the SAME date as #518/#520/#530
-    #  rather than a longer one -- a later date would hide this debt behind the cliff instead
-    #  of joining it, and the cliff is already a filed row.  Measured before writing this:
-    #  `grep -ln "E sgi|-e ip30" gate_*.sh` matches ONLY gate_asan_sweep.sh, which CONSTRUCTS
-    #  machines and runs no guest session, so there is no gate in this tree that could host it
-    #  today.  *** NOT classified `witness' to escape the requirement: the flagship seat found
+    #  #531's detector, on the SAME footing as #518/#520/#530 (it took their date too, so the
+    #  cliff stayed one date, until #550 dispersed the block).  This comment said: "`grep -ln
+    #  "E sgi|-e ip30" gate_*.sh` matches ONLY gate_asan_sweep.sh ... no gate in this tree could
+    #  host it today."  CORRECTED by #550: as written that grep matches nothing (`|' is literal in a
+    #  basic regex), and even as an extended regex it searches gate_*.sh, where the machine never
+    #  appears -- the probes exec it themselves; gate_arm.sh already runs seven `-E sgi -e ip32'
+    #  cold-debugger probes, so a home exists.  *** NOT classified `witness' to escape the requirement: the flagship seat found
     #  that exact dodge elsewhere in this manifest -- an ungated DETECTOR relabelled WITNESS,
     #  after which the checker verifies it is ungated -- and named it a check that cannot
     #  fail.  This entry is the honest form: DETECTOR, ungated, dated, and filed. ***
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): gate_arm.sh hosts seven sgi cold-debugger probes of this shape; about 570 s per
+    #  run, because each surviving session waits out the 12 s death poll -- a long gate guest until
+    #  that window shrinks without reading a delayed abort as alive.
     "artifacts/ip30abortkill/ip30_abort_probe.py":
-                                   ("2026-09-27",
+                                   ("2026-10-15",
                                     "no gate runs an SGI IP30 guest session (gate_asan_sweep.sh "
                                     "constructs only); filed to wiringcliff with #518/#520/#530"),
 }
```

### 5b. #550 -- tools/precommit_check.sh (HEAD -> #550)

```diff
--- -	2026-09-25 16:05:41.626369700 -0500
+++ /c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/exempt550/pcc_550v2_onHEAD.sh	2026-09-25 15:25:31.412560800 -0500
@@ -524,7 +524,8 @@
 #  Existing gaps are carried as DATED exemptions that EXPIRE, never as silent grandfathering; the
 #  dates live in check_probe_wiring.py's EXEMPT table, not here.  (They were 2026-09-20, chosen to
 #  fall due with gate_offline's fbpending_bound; #537 discharged that debt and #536 moved the
-#  block to 2026-09-27 by owner ruling.)
+#  block to 2026-09-27 by owner ruling; #550 dispersed it to ten individual dates, 2026-10-08
+#  to 2026-12-03, by owner ruling 2026-09-24.)
 #
 #  THE SELFTEST RUNS ONLY WHEN THE CHECKER ITSELF CHANGES.  --selftest applies its mutants (22, pinned below) to
 #  temp copies and asserts each exit status, which takes ~14 s -- too slow for every commit,
```

### 5c. #550 -- regress/gate_offline.sh (HEAD -> #550)

```diff
--- -	2026-09-25 16:05:41.706279400 -0500
+++ /c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/exempt550/goff_550v2.sh	2026-09-25 15:25:31.443417100 -0500
@@ -2268,8 +2268,10 @@
 #  lines, whose every row could be inert with this gate green.
 #
 #    ieee_store    HAS NO COMPARATOR TO SENTINEL.  No check(), no `rows`, no `failures`: each
-#                  section carries its own counter (abs_bad, rm_rn_bad, rm_rz_bad, rm_d_bad,
-#                  rm_vec_bad, interp_bad) with the comparison written inline dozens of times,
+#                  section carries its own counter -- nine of them are the `== 0' terms of its
+#                  DIFF_PASS test (abs_bad, unexplained, missed, inrange_diff, rm_rn_bad,
+#                  rm_rz_bad, rm_d_bad, rm_vec_bad, interp_bad; this said six until #550) --
+#                  with the comparison written inline dozens of times,
 #                  and this gate greps one summary line per counter for 0.  There is no single
 #                  point to feed a mismatch to.  A probe through a comparator NO REAL ROW USES
 #                  would prove nothing while reading exactly like coverage, so none was
@@ -2286,13 +2288,20 @@
 #                  dev_wdc.c -- which is the OTHER control, already present.  This one needs
 #                  the nine row functions refactored onto a shared helper first: a round, not
 #                  a line.
+#                  *** #550, 2026-09-25: THIS CENSUS IS STALE. ***  "The nine row functions"
+#                  is the 2026-08-19 count; since #484 (2026-08-27) `chk(name, got, want)'
+#                  has carried 24 got/want rows.  #551 replaces this paragraph.
 #  RE-DATED 2026-09-18 BY OWNER RULING, from 2026-09-02 -- a date that passed with no owner row: the
 #  "no exemption is past its dated deadline" row below went RED on every run from 2026-09-03, and the
 #  first run to OBSERVE it was 2026-09-18, the weekly battery having been disabled.  A re-date is not a
-#  discharge: both reasons above stand unchanged, and this list's SM twin was ruled the other way
-#  ("fix it, do not re-date", #537).  The comparison is a strict `<`, so these are valid ON 2026-09-27
-#  and RED from 2026-09-28.  Owner row: `scexempt` -- discharge, re-decide or delete before then.
-SC_EXEMPT="ieee_store:2026-09-27 wdc_identify:2026-09-27"
+#  discharge, and this list's SM twin was ruled the other way ("fix it, do not re-date", #537).
+#  #550, 2026-09-25: DECIDED SEPARATELY BY OWNER RULING 2026-09-25 (row `scexempt'); the comparison is a
+#  strict `<', so each entry is valid ON its own date and RED from the next day.
+#    ieee_store    RE-DATED to 2026-12-10, its reason above standing (nine counters, no comparator:
+#                  the larger refactor, dated after the wdc work).  RED from 2026-12-11.
+#    wdc_identify  NOT re-dated: the owner ruled it FIXED -- #551 gives it a comparator self-check and
+#                  moves it to SC_COVERED.  Until #551 lands, valid ON 2026-09-27, RED from 2026-09-28.
+SC_EXEMPT="ieee_store:2026-12-10 wdc_identify:2026-09-27"
 
 sc_missing=""
 for f in "$HERE"/diff_*.c; do
```

### 5d. #551 -- regress/diff_wdc_identify.c (HEAD -> #551)

```diff
diff --git a/regress/diff_wdc_identify.c b/regress/diff_wdc_identify.c
index c0cf077b..18d66403 100644
--- a/regress/diff_wdc_identify.c
+++ b/regress/diff_wdc_identify.c
@@ -501,14 +501,14 @@ static void build(struct wdc_data *d, uint64_t sectors, int c, int h, int s)
  *  byte this row puts at or past the divergence point -- a row that cannot say
  *  that is a row that would pass unfixed.
  */
-static void row(const char *why, uint64_t sectors)
-{
-	struct wdc_data d;
-	uint64_t got57, got60;
+/*  #551: the comparison is split out of row() as a PURE comparator, so the self-check can feed it each
+    disjunct alone, and a zero, without building a device.  row() and its eight callers are unchanged in
+    what they print.  */
+static int rowcmp_calls;
 
-	build(&d, sectors, 1, 1, 1);
-	got57 = sectors_from_block(&d, 57, 58);
-	got60 = sectors_from_block(&d, 60, 61);
+static void row_cmp(const char *why, uint64_t sectors, uint64_t got57, uint64_t got60)
+{
+	rowcmp_calls ++;
 	rows ++;
 
 	if (got57 != sectors || got60 != sectors) {
@@ -521,6 +521,17 @@ static void row(const char *why, uint64_t sectors)
 	}
 }
 
+static void row(const char *why, uint64_t sectors)
+{
+	struct wdc_data d;
+	uint64_t got57, got60;
+
+	build(&d, sectors, 1, 1, 1);
+	got57 = sectors_from_block(&d, 57, 58);
+	got60 = sectors_from_block(&d, 60, 61);
+	row_cmp(why, sectors, got57, got60);
+}
+
 /*
  *  The anchor. Word 53's bytes are 0x00,0x02 -- asymmetric, so a +0/+1 swap in
  *  the packing is visible here. Word 47 (0x8080) is a palindrome and would not
@@ -4846,14 +4857,17 @@ static void gx_push(struct wdc_data *d, int n, int w, unsigned char v)
     mismatch bumps `failures`.  The seat's private counters are deliberately
     NOT carried over -- a row this file does not count is a row the identity
     pin cannot protect.  */
-static void chk(const char *name, long got, long want)
+static int chk_calls;	/*  #551: counted, so the LAST self-check can print the coverage  */
+
+static void chk(const char *name, long long got, long long want)
 {
+	chk_calls ++;
 	rows ++;
 	if (got != want) {
 		failures ++;
-		printf("  FAIL %-40s got %ld want %ld\n", name, got, want);
+		printf("  FAIL %-40s got %lld want %lld\n", name, got, want);
 	} else
-		printf("  ok   %-40s %ld\n", name, got);
+		printf("  ok   %-40s %lld\n", name, got);
 }
 
 static void row_ring_occupancy_sound(void)
@@ -5627,6 +5641,67 @@ static void row_selfconsistent(void)
 	}
 }
 
+/*
+ *  @@SELFCHECK@@ -- #551.  CAN THIS FILE'S COMPARATORS STILL FAIL?  Feeds chk() and row_cmp() known answers --
+ *  each operand zero and past 32 bits, each of row_cmp()'s two disjuncts alone, and one pair that must NOT
+ *  fail -- and requires the EXACT change in `failures' for each, restoring `rows' and `failures' after every
+ *  probe.  Run FIRST (before any row) and LAST (after every row, before the identity row), so a comparator
+ *  that goes inert partway through is caught at one end or the other.  Only the success arm prints gate 2's G
+ *  text; the failure arm does not, and forces one failure.
+ *
+ *  WHAT IT COVERS: the rows that go through chk() and row_cmp() -- the last run prints how many calls
+ *  each comparator took.  Of chk()'s calls, the ones in row_ring_occupancy_sound() that pass a
+ *  `cond ? 1 : 0' (or `? 0 : 1') hand it a VERDICT computed at the call, not a comparison, and every
+ *  other row in this file compares inline: neither is covered by this block.  NOT CAUGHT, DISCLOSED: a
+ *  rows-keyed or name-keyed test inside either comparator, placed before its `rows ++', keeps every gate-2
+ *  row green while silencing any covered row except the self-mutant's -- the first-and-last placement
+ *  does not close it (after the increment, the same test reds through `failures').  Reviewed in the
+ *  differential, not chased.  No line this block prints carries the self-mutant row's text or "high
+ *  byte" (gate 2 counts both), and gate 2's G text is printed ONCE, by the last run, only when both runs
+ *  passed.  The rest of the file is filed as `wdcidcomparators' (#551; owner ruling 2026-09-25).
+ */
+static int sc_first_bad = -1;	/*  -1 until the FIRST run has happened  */
+
+static void selfcheck(const char *where)
+{
+	static const long long cg[] = { 1, 0x100000000LL, 0, 0, 7 };
+	static const long long cw[] = { 2, 0, 1, 0x100000000LL, 7 };
+	static const uint64_t rw[] = { 2, 2, 1, 3 };
+	static const uint64_t r57[] = { 1, 2, 0, 3 };
+	static const uint64_t r60[] = { 2, 1, 0, 3 };
+	int sc_f = failures, sc_r = rows, sc_c = chk_calls, sc_rc = rowcmp_calls, sc_bad = 0, i, n = 0;
+
+	for (i = 0; i < 5; i++, n++) {
+		chk("@@SELFCHECK@@/chk", cg[i], cw[i]);
+		if (failures != sc_f + (cg[i] != cw[i]))
+			sc_bad++;
+		failures = sc_f; rows = sc_r;
+	}
+	for (i = 0; i < 4; i++, n++) {
+		row_cmp("@@SELFCHECK@@/row", rw[i], r57[i], r60[i]);
+		if (failures != sc_f + (r57[i] != rw[i] || r60[i] != rw[i]))
+			sc_bad++;
+		failures = sc_f; rows = sc_r;
+	}
+	chk_calls = sc_c; rowcmp_calls = sc_rc;
+	if (sc_bad) {
+		printf("  FAIL  SELFCHECK(%s): %d of %d probes answered wrongly\n", where, sc_bad, n);
+		failures = sc_f + 1; rows = sc_r;
+	}
+	if (where[0] == 'f') {
+		sc_first_bad = sc_bad;
+		if (!sc_bad)
+			printf("  ok    SELFCHECK(first): all %d probes answered right\n", n);
+		return;
+	}
+	if (!sc_bad && sc_first_bad == 0)
+		printf("  ok    SELFCHECK the comparator can still fail (first and last)\n");
+	else if (!sc_bad)
+		printf("  FAIL  SELFCHECK(last): the first run did not pass\n");
+	printf("  note  SELFCHECK comparator calls this run: chk() %d, row_cmp() %d\n",
+	    chk_calls, rowcmp_calls);
+}
+
 int main(void)
 {
 	/*  Unbuffered, so a crash mid-run still shows how far it got -- with stdout
@@ -5636,6 +5711,7 @@ int main(void)
 	setvbuf(stdout, NULL, _IONBF, 0);
 
 	printf("ATA IDENTIFY capacity packing (#405), against the REAL dev_wdc.c\n");
+	selfcheck("first");
 
 	/*  Controls: below the divergence point these pass either way, and they
 	    are here to prove the rig reports correct values, not to detect.  */
@@ -5710,6 +5786,7 @@ int main(void)
 	row_wide_geometry();
 	row_no_lba_claim();
 	row_selfconsistent();
+	selfcheck("last");
 
 	/*
 	 *  IDENTITY GUARD.  Two files with this name once differed only by the case of a
```

### 5e. #551 -- regress/gate_offline.sh (#550 -> #551)

```diff
--- /c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/exempt550/goff_550v2.sh	2026-09-25 15:25:31.443417100 -0500
+++ regress/gate_offline.sh	2026-09-25 15:30:34.610907100 -0500
@@ -2243,29 +2243,37 @@
 #  @@SELFCHECK@@ block, so moving a stem from EXEMPT to COVERED and writing no sentinel is
 #  RED.  Without it this would be another G -- a check that a name appears in a list -- which
 #  is precisely the defect being corrected here.
-SC_COVERED="timer memory_rw footbridge m8820x m8invread diskimage_sync diskimage_parse diskimage_io diskimage_geom sh4_tmu rtc_range fbpending_bound"
+SC_COVERED="timer memory_rw footbridge m8820x m8invread diskimage_sync diskimage_parse diskimage_io diskimage_geom sh4_tmu rtc_range fbpending_bound wdc_identify"
 #  *** COVERED IS NOT UNIFORM, AND THE MANIFEST CANNOT SEE THE DIFFERENCE -- READ THIS BEFORE
-#  TREATING A GREEN ROW AS "the file is vouched for". ***  All but three of the COVERED stems
-#  route every row through one or two shared helpers, so the sentinel covers the file.  The
-#  count used to be spelled out here as "seven of the ten" and went stale the first time a
-#  stem was added; a proportion that has to be re-derived on every addition is a comment that
-#  will be wrong more often than right, so it is stated as an exception list instead.  The
-#  three that do NOT route through shared helpers:
+#  TREATING A GREEN ROW AS "the file is vouched for". ***  Most COVERED stems route every row
+#  through one shared helper, so the sentinel covers the file.  No count is kept here: it used to say
+#  "seven of the ten", then "all but three" -- stale the first time a stem was added, and wrong for
+#  geom and sync, which each have two helpers.  The stems whose sentinel does NOT cover every row, or
+#  needs more than one probe:
 #    * sh4_tmu   -- 12 of 18 rows.  row1() is the only comparator in the file that takes an
 #                   expected value; row_three_timers/row_interrupt/row_interrupt_unie_clear/
 #                   row_stopped/row_no_freeze each hardcode their own, and cannot be probed.
 #    * geom      -- every row but the identity row, via BOTH geom() and parse(), which are
 #                   two separate comparators and are probed separately for that reason.
 #    * sync      -- both checks() and checkn(), for the same reason.
+#    * wdc_identify -- 24 of 128 rows compare inside a comparator the sentinel feeds (chk() 16,
+#                   row_cmp() 8); 8 more hand chk() a 0/1 verdict computed at the call (derive:
+#                   grep -cE '\? [01] : [01], 1\);' regress/diff_wdc_identify.c), and the other
+#                   96 compare inline -- NOT covered.  The file prints its comparator call counts
+#                   on every run.  A rows- or name-keyed test inside either comparator, placed
+#                   before its rows ++, keeps every gate-2 row green while silencing any covered
+#                   row but the self-mutant's: disclosed, not chased.  #551, by owner ruling
+#                   2026-09-25 ("24/128 now, file the rest"); the rest is `wdcidcomparators'.
 #  rtc_range is in the UNIFORM group: every row goes through chk(), its single comparator.
-#  Named here rather than left to be re-derived, because the three-file exception list above
+#  Named here rather than left to be re-derived, because the exception list above
 #  is only trustworthy if additions are classified as they arrive.
 #  The per-file comments carry the scope; this is a LIVENESS control, never a census, and
 #  "going from 0 to 1 is not false comfort; calling 1 `the detector works` is".
 #
 #  THE EXEMPTIONS, DATED AND REASONED.  A FORTNIGHT, matching the deadline the owner chose
 #  over the Q4 one I proposed for the selfmutant list: 2 uncovered differentials, 1311 and 766
-#  lines, whose every row could be inert with this gate green.
+#  lines, whose every row could be inert with this gate green.  (Then; #551 moved wdc_identify to
+#  COVERED, so ieee_store is the one left.)
 #
 #    ieee_store    HAS NO COMPARATOR TO SENTINEL.  No check(), no `rows`, no `failures`: each
 #                  section carries its own counter -- nine of them are the `== 0' terms of its
@@ -2279,18 +2287,12 @@
 #                  against TOTAL comparator death, which is this control's own failure mode,
 #                  but by the vacuity-prone `grep -c PASS == 0` form its SM_EXEMPT comment
 #                  already flags, so it is a weaker cover than it looks.
-#    wdc_identify  NOTHING TO FEED A MISMATCH TO.  Read every row function: row_anchor,
-#                  row_slave, row_base_drive, row_identity, row_atapi_flags, row_wide_geometry,
-#                  row_no_lba_claim and row_selfconsistent are ZERO-ARGUMENT with the expected
-#                  value hardcoded in the body, and row(why, sectors) derives its expectation
-#                  FROM ITS INPUT (`got57 != sectors`), so changing the input changes the
-#                  answer too and no mismatch can be produced.  Injecting one means mutating
-#                  dev_wdc.c -- which is the OTHER control, already present.  This one needs
-#                  the nine row functions refactored onto a shared helper first: a round, not
-#                  a line.
-#                  *** #550, 2026-09-25: THIS CENSUS IS STALE. ***  "The nine row functions"
-#                  is the 2026-08-19 count; since #484 (2026-08-27) `chk(name, got, want)'
-#                  has carried 24 got/want rows.  #551 replaces this paragraph.
+#    wdc_identify  DISCHARGED by #551 -- moved to SC_COVERED with a self-check on its comparators (see
+#                  the COVERED list above).  This entry used to say "NOTHING TO FEED A MISMATCH TO"
+#                  and "This one needs the nine row functions refactored onto a shared helper
+#                  first".  The nine were 16 executions -- row() x 8 and eight zero-argument
+#                  functions -- and that census (2026-08-19) went stale when #484 added
+#                  chk(name, got, want) on 2026-08-27: its 24 calls are none of the nine.
 #  RE-DATED 2026-09-18 BY OWNER RULING, from 2026-09-02 -- a date that passed with no owner row: the
 #  "no exemption is past its dated deadline" row below went RED on every run from 2026-09-03, and the
 #  first run to OBSERVE it was 2026-09-18, the weekly battery having been disabled.  A re-date is not a
@@ -2299,9 +2301,7 @@
 #  strict `<', so each entry is valid ON its own date and RED from the next day.
 #    ieee_store    RE-DATED to 2026-12-10, its reason above standing (nine counters, no comparator:
 #                  the larger refactor, dated after the wdc work).  RED from 2026-12-11.
-#    wdc_identify  NOT re-dated: the owner ruled it FIXED -- #551 gives it a comparator self-check and
-#                  moves it to SC_COVERED.  Until #551 lands, valid ON 2026-09-27, RED from 2026-09-28.
-SC_EXEMPT="ieee_store:2026-12-10 wdc_identify:2026-09-27"
+SC_EXEMPT="ieee_store:2026-12-10"
 
 sc_missing=""
 for f in "$HERE"/diff_*.c; do
```


## 6. QUESTIONS

1. **Which of the F2 rulings did this diff implement WRONGLY, or not at all?  Name the count.**  Check #550's R1-R10
   and S1-S4 and #551's rulings 1-9 against the hunks, one by one -- the ruling file is
   `regress/artifacts/exemptredate_20260925/fable5_f2_550_551.md`; its instructions are condensed in section 2.
2. **(#550) Is any re-dated REASON still false?**  Each entry now names its owed work; enumerate them and check each
   against the probe and the gates it names (file-reading seats: open them).  Is the schedule's order right -- cheapest
   first, one owed round per date except the Alpha four?
3. **(#551) The smallest edit to `diff_wdc_identify.c` that keeps gate 2 GREEN while a covered row can no longer
   fail** -- other than the disclosed pre-`rows ++` stateful test.  Name the row you expect to stay green.
4. **(#551) Section 4's result against the ruling:** is gate 2's G row an adequate sole carrier for "forced failure
   removed AND a comparator stubbed", or should the block also red the RUN in that case?  If the latter, what is the
   smallest change, and what does it cost the byte-identity property?
5. **Any wrong record in the added comments** -- a count without its deriver, a quote marked verbatim that is not, a
   present-tense claim that is only true until the next commit?
6. **Option-set completeness** (#550): is re-dating the right disposition for each of the ten, or is one of them
   cheaper to WIRE this week than to re-date (the owner ruled "no wiring work this week" -- so say so as a finding, not
   as an edit)?

If, while verifying a claim, you found something ELSE -- say so.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
