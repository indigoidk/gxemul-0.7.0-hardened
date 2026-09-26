# #550 exemptredate + #551 wdcidselfcheck -- THE §F2 PASS ON PASS 2: every seat's findings, my disposition on each, and the repair (measured)

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/`** (`tools/`, `regress/`).  Pristine-2021-upstream copies of GXemul sit under the
project root (`./src/` and two under `_archive/`); they are NOT this fork -- say so if your line numbers are off by
hundreds.  **If you cannot read files that is expected**: every fact you need is inlined; name any premise you cannot
settle from this packet rather than guessing.

**VERDICT LINES FIRST, one per round:** `VERDICT #550: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>` and
`VERDICT #551: <...>`.  Then numbered findings.  **The load-bearing question: WHICH OF MY DISPOSITIONS BELOW IS WRONG?
Name the count.**  If you raised a finding, be HARDER on it than on anyone else's -- including whether the fix I made for
it is right, which is a different claim from whether the finding was.  If a disposition ADOPTS your position, scrutinise
it more, not less.

## 1. SETTLED PREMISES, RE-INLINED

* `#550` re-dates, ONE BY ONE (owner ruling 2026-09-24), the ten probe-wiring exemptions that were all dated 2026-09-27
  in `tools/pipeline/check_probe_wiring.py` (valid ON the date, red the day after; any red blocks every commit), and
  re-dates gate 2's `SC_EXEMPT` `ieee_store` (owner ruling 2026-09-25: "Only ieee_store gets re-dated").  Comments and
  dates only; no emulator code.  The dates are the Fable 5.1 F2 ruling's (`exemptredate_20260925/fable5_f2_550_551.md`,
  S1): ppc_rldicl 10-08, ip30 10-15, alpha_tbi 10-22, lca_badval 10-23, lca_widewrite 10-26, lca_isalane 10-27,
  wdc_altoffset 11-05, 4bit 11-12, sig 11-19, addtoinbuf 12-03, ieee_store 12-10.  **No date moves in this repair.**
* `#551` gives `regress/diff_wdc_identify.c` a self-check on its comparators `chk()` and a new pure `row_cmp()` (split
  out of `row()`), run FIRST and LAST, and moves it from gate 2's `SC_EXEMPT` to `SC_COVERED`; owner ruling 2026-09-25:
  "24/128 now, file the rest".  Gate 2 greps the per-stem log for `SELFCHECK the comparator can still fail` (the G row)
  and the source for `@@SELFCHECK@@` (the H row); `grep -c 'high byte'` is pinned at 1; the self-mutant lane needs
  exactly one untagged pristine line.
* The pass 2 you are adjudicating: `panel_20260925_160838` (brief `wdcidselfcheck_20260925/p2_brief_550_551.md`) --
  agy SHIP/SHIP; grok, glm, deepseek, minimax, kimi-k3:cloud SHIP WITH CHANGES on both; the dedicated grok job SHIP WITH
  CHANGES on both; the Opus 5.5 measuring seats SHIP WITH CHANGES (#550: `exemptredate_20260925/opus5_p2.md`, #551:
  `wdcidselfcheck_20260925/opus5_p2.md`).  **codex WALLED** (usage limit until 2026-09-26 07:01) -- a seat failure; its
  re-fire and the Astra adjudication follow after the reset, and nothing is committed before Astra confirms (owner
  ruling 2026-09-25).  The kimi CLI is on its weekly wall, covered by kimi-k3:cloud.

## 2. THE FINDINGS AND MY DISPOSITIONS (every "FIXED" is in the repair diffs in section 4)

### #550 -- all comment text; every fix is L4 (a wrong record corrected in place)

* **P1 (Opus, deepseek): the stale-census supersession line said `chk()` "has carried 24 got/want rows"** -- 16 of its
  24 calls are got/want and 8 hand it a 0/1 verdict; the line also quoted a fragment ("The nine row functions").
  **FIXED:** "It counts the nine row functions (2026-08-19) and leaves out `chk(name, got, want)`, which #484 added on
  2026-08-27: 24 chk() calls, 16 got/want and 8 handing it a 0/1 verdict."  No quote.
* **P2 (Opus; kimi-k3 on the internal contradiction): "even as an extended regex it searches gate_*.sh, where the
  machine never appears" is FALSE** -- `gate_asan_sweep.sh` (gate 9) runs `-E sgi -e "$s"` for every subtype.
  **FIXED:** "as an extended regex it matches only gate 9's construction sweep ... guest-session probes exec the machine
  themselves", with the seven probes' deriver.
* **P3 (Opus): three Alpha lines said "so they fall due together"** -- they fall due on four different days.
  **FIXED:** "same alphabook1 home as alpha_tbi; one round discharges all four."
* **P4 (Opus): R1 as implemented dropped ieee_store's owner action.**  **FIXED:** "Owner row `scexempt': discharge,
  re-decide or delete before then."  *And a consequence I found while fixing it: once #551 lands, `scexempt` must stay
  OPEN for ieee_store -- closing it would leave that exemption with no owner row, the exact failure the row was filed
  for.  Records only; the row is re-scoped, not closed.*
* **P5 (Opus; grok, grok ded. on the parts): the parent altoffset probe's line said it "owes a single-leg ORACLE ...
  `wdcaltoffleg' (a)"** -- but the queue row's (a) is an EXIT STATUS (the probe exits 0 whatever its `ok` says), and the
  rows' fix-side wants already exist.  **FIXED:** "owes queue row `wdcaltoffleg' two things -- its item (a), an exit
  status ..., and a single-leg form, because every ROWS entry carries a want for the committed leg (`wb`) that the
  gate's one binary cannot supply."
* **P6 (Opus): the sig correction said "gate 10 already carries the malta image"** -- imprecise (`wdc-scratch-64m.img`
  runs on landisk; gate 10's malta session writes its own disk).  **FIXED:** "the probe takes any image as argv[2] and
  applies the ciR: prefix itself."
* **P7 (Opus): the ppc line was committed text about UNcommitted state** ("the parked working-tree edit of its
  want_rldimi touches no scored row").  **FIXED:** "Its scored rows call none of want_rldimi, want_rlwimi, want_rlwinm or
  mask32, so an edit of those helpers is no prerequisite."
* **P8 (Opus, glm, kimi-k3): counts without derivers** -- "about 570 s", "24/24 in under a second", "seven sgi ...
  probes", "twelve entries".  **FIXED:** 568 s and 24/24 now cite the preserved runs
  (`exemptredate_20260925/opus550_measured_p2/p1_runs/`); seven and twelve carry derivers, each RUN before it was
  written (`grep -cE '^python3 sgi_[a-z_]+_probe[.]py' regress/gate_arm.sh` -> 7;
  `grep -A13 '^AB_EXEMPT="' regress/gate_asan_sweep.sh | grep -c ':2026-11-30'` -> 12).
* **P9 (the dedicated grok job): "no gate runs an Alpha machine" is FALSE** -- gate 9 walks every `-H` machine,
  alphabook1 included (checked: `gxemul -H` lists `alphabook1`; the sweep execs `-V -E "$t" -e "$s"`).  The ip30 tuple
  was already narrowed to "guest session"; the four Alpha tuples were not.  **FIXED at every sibling copy** (the four
  tuples, their three comments, one MANIFEST note): "no gate runs an Alpha guest session (gate 9 only constructs one)".
* **P10 (glm, kimi-k3): two quotes were not verbatim** -- checked against HEAD: the sig tuple read "... does not build
  **today**", and the ip30 comment read "no gate in this tree **that** could host it today".  **FIXED** both.
* **P11 (deepseek, glm, grok): the header's "the four wdc probes ... each owing its own oracle" is false** for the parent
  (an exit status and a single-leg form) and for addtoinbuf (a poisoned image).  **FIXED:** "each owing its own
  instrument work".
* **P12 (glm, kimi-k3): the Thursday 10-29 is skipped and nothing says why.**  **FIXED:** "(10-29 is left free, in that
  round's week)" -- the Alpha round's.
* **P13 (minimax): the brief's condensation said "consecutive days"; the dates are Thu/Fri/Mon/Tue.**  The dates are the
  ruling's own list, and the header's "within days of each other" was accurate.  **FIXED the wording to what is there:**
  "on four working days in a row, 10-22 to 10-27".
* **P14 (minimax): ip30 (10-15) before the Alpha four contradicts "cheapest first"?**  **NO CHANGE:** "cheapest" is the
  work to DISCHARGE, not the run time -- ip30's home exists (a gate_arm.sh block like its seven siblings), while the
  Alpha four need a gate home that does not exist.  The order is the ruling's.
* **P15 (Opus, deepseek, glm, grok, kimi-k3, agy): `ppc_rldicl` is cheaper to WIRE than to carry to 10-08** (glm: a
  rows-scored gate_ppc.sh block would do, without the RESULT/CONTROL lines).  **RECORDED AS A FINDING, NO EDIT** -- the
  owner ruled no wiring this week; it is the first date.
* **P16 (glm, kimi-k3, grok): `schedule_v2.out`'s 12-04 line reads "10 problem(s); 7 |"** where the others read "71" --
  my measurement script's fixed-width cut once "10" is one digit wider, not the checker.  **NOTE in the artifact.**
* **P17 (grok): `exemptdistinct` and `wdcidcomparators` are cited as filed and are not in `OUTSTANDING_BUGS.md` yet**, and
  its `scexempt` paragraph (:21901) still says "nine row functions ... before 2026-09-28".  **The records land in the
  SAME commit** as each round (drafted); the `scexempt` paragraph is updated there.
* **P18 (grok): the working tree's `precommit_check.sh` pins `SCORE_CLAIMS_MANIFEST=32`** (another unit's parked line).
  **Handled by the swap recipe** (S4): the committed blob is HEAD-based and keeps 30.
* **P19 (kimi-k3): `chk()`'s `long` -> `long long` on an LLP64 build would change output.**  **NOT APPLICABLE:** the
  differential is built and run under WSL (LP64), where it is a no-op; the F2 ruling kept it for that reason.

### #551

* **Q1 (Opus MEASURED; grok, grok ded., kimi-k3, glm): the disclosure's increment-order sentence was BACKWARDS, and
  "except the self-mutant's" was false.**  The post-increment `(rows & 127) < 2` escapes (the last self-check sees 128);
  the pre-increment one is caught (it sees 127); a name-keyed test escapes on either side; and the self-mutant's row
  compares INLINE, so no covered row is protected.  **FIXED:** the disclosure no longer mentions increment order: "a test
  keyed on a value, a name or a position the probes do not present, in either comparator, and an edit of the code that
  FEEDS them ... keep every gate-2 row green -- measured; reviewed in the differential, not chased."
* **Q2 (Opus MEASURED, grok ded.): `&& want-165` in `chk()` escapes** (keyed on a value no probe presents).
  **DISCLOSED** by the rewritten sentence (a value-keyed test).
* **Q3 (Opus MEASURED; agy, grok, glm, deepseek, kimi-k3): the FEED edit escapes** -- `row()` calling `row_cmp(why,
  sectors, sectors, sectors)`, or a call site `chk(name, want, want)`: the self-check tests the comparators directly and
  never the code that feeds them.  **DISCLOSED** ("an edit of the code that FEEDS them"), and the bullet now says
  "covered" means the COMPARATOR is live, not that a row is (Opus's finding 7).
* **Q4 (Opus MEASURED; grok ded.): `row_cmp()` narrowed to `uint16_t`, or `&& sectors<4`, escapes** -- its probe
  operands never exceeded 3.  **FIXED:** two WIDE probes, each disjunct wrong only above bit 32 -- (2^32, 0, 2^32) and
  (2^32, 2^32, 0).  Measured: both edits now red (2 of 11 probes); output byte-identical otherwise.  This also makes the
  comment's "each operand zero and past 32 bits" true of `row_cmp()` (glm).
* **Q5 (Opus MEASURED; kimi-k3, glm, deepseek): with the forced failure removed AND a comparator stubbed, the RUN printed
  `WDC_IDENTIFY_PASS`, exit 0** -- only gate 2's G row caught it.  **FIXED:** `static int sc_g`, set only where the G
  line prints; `PASS` needs it, and the exit status is `(failures || !sc_g)`.  Measured: that double edit now prints
  `WDC_IDENTIFY_FAIL`, exit 1; healthy runs are byte-identical (14 pairs).  **This is the one DISAGREEMENT -- section 3.**
* **Q6 (minimax): the bullet's "(chk() 16, row_cmp() 8)" reads as chk()'s total**, while the file prints chk() 24.
  **FIXED:** "24 of 128 rows compare inside a comparator the sentinel feeds: 16 of chk()'s 24 calls and all 8 of
  row_cmp()'s.  chk()'s other 8 are handed a 0/1 verdict ...".
* **Q7 (minimax): "the first run did not pass" also prints when the first run never RAN.**  **FIXED:** "the first run did
  not run, or did not pass" (a FAIL-path string; healthy output unchanged).
* **Q8 (glm): "2 uncovered differentials, 1311 and 766 lines" has no deriver.**  It is a sentence from an earlier round,
  true when written.  **FIXED the marker #551 appended:** "(True when written; #551 moved wdc_identify to COVERED ...)".
* **Q9 (deepseek): the verdict deriver `grep -cE '\? [01] : [01], 1\);'` looks malformed.**  **CHECKED: it prints 8**
  (the Opus #550 seat and grok both ran it; eight lines).  No change.
* **Q10 (mine): the "block deleted" control no longer compiled after Q5** -- deleting the block leaves `sc_g` undefined in
  `main()`.  A deletion as it would really be written removes the verdict's use of the flag too; re-measured that way:
  the run passes, prints no G line and no token -- exactly what gate 2's G and H rows grep for.

## 3. THE DISAGREEMENT, BOTH SIDES IN THEIR OWN WORDS

**Q5 -- should the RUN itself go red when its self-check has failed and its forced failure is gone?**

* **Yes (Opus, measured):** "The run's own verdict is false to anything reading the trailer or the exit status ...
  Smallest change: make PASS depend on the flag only the G arm sets ... Byte-identity cost: none."  kimi-k3: "not
  adequate to the file's own contract ... any consumer of the file's own verdict (human, trailer-grep battery) is
  misled."  glm: "The G row alone leaves the run's own verdict a lie outside gate 2."
* **No (grok, panel):** "Leave the run's trailer alone ... Putting another `failures++` on the success path would turn
  every good run red and would break the byte-identity the measurement just established.  One sentence in the block,
  stating that this double edit is caught by gate 2's G row, is the record."  agy: "Yes [G is adequate] ... That is
  precisely why the G check was created."
* **My disposition: ADOPT the flag.**  grok's objection is to a `failures++` on the success path, which the flag is
  not: `sc_g` is 0 only when the G line did not print, so a healthy run is unchanged -- measured byte-identical on seven
  device variants at -O2 and -O0.  **grok and agy: is there a case where `sc_g` changes a healthy run, or a reason the
  run's verdict should stay PASS when its self-check failed?**

## 4. THE REPAIR (measured) -- disclosure: every file the repair touches is INLINED below as a diff against pass 2's
## version; `CHANGELOG.md`, `OUTSTANDING_BUGS.md` and `ledger.json` NOT SHOWN (drafted, land with each commit)

* **#551b, measured** (`wdcidselfcheck_20260925/measured/run551b.out`, `run551b_nosc.out`; MINE md5 d0339493): (a) the new
  file against HEAD's, -O2 and -O0, seven device variants: 14 of 14 byte-identical except the SELFCHECK lines, same exit
  codes; (b) red: chk() stubbed, row_cmp() stubbed, each disjunct dropped, `&& got`, u16, sect4, and the double edit
  (now `WDC_IDENTIFY_FAIL`, rc 1, pristine AND drqring); the block deleted: PASS with no G line and no token; green, as
  disclosed: the post-increment rows test, the name test, `want-165`, and the feed edit (`row_cmp(why, sectors,
  sectors, sectors)` on the word-57-high-byte variant: rc 0, PASS).
* **#550 v3**: comments only; the checker still compiles and `gate_offline.sh` parses; the schedule is unchanged (no date
  moved), so section 4 of the pass-2 brief stands -- RE-MEASURED on v3, not asserted: the same problem count on every step date and `--selftest` 22/22 (`exemptredate_20260925/measured/schedule_v3.out`, `selftest_550v3.out`).

### 4a. #550 v2 -> v3: tools/pipeline/check_probe_wiring.py

```diff
--- tools/pipeline/check_probe_wiring.py	2026-09-25 15:25:31.379707400 -0500
+++ tools/pipeline/check_probe_wiring.py	2026-09-25 16:30:52.754970400 -0500
@@ -1228,7 +1228,7 @@
     #  against the exact instrument that produced them.
     #  lcaisalane's is a WITNESS as-run copy, red on HEAD by design and not a green row anyone may wire.
     #  #518 lcabadval, landed with the round: the live detector (DETECTOR + dated EXEMPT below -- no
-    #  gate runs an Alpha machine, the #520 precedent) and its table-5 mutator.
+    #  gate runs an Alpha guest session, the #520 precedent) and its table-5 mutator.
     "lca_isalane_probe.py":
         (CLASS_DETECTOR, "lcaisalane (#530): 37 rows on unmodified -E alphabook1 -- the 16-row rung-3 witness (sentinel re-pinned to 0x0bad1d8a) plus 21 detector rows for disposition B (byte for port P at (P & 3) % len on both arms; the six host-death cells, reads AND writes, rowed alive + value).  HEAD 19/37, fix 37/37 (artifacts/lcaisalane/fix530_20260914/); kill table 1 in that dir"),
     "lca_badval_probe.py":
@@ -2507,11 +2507,13 @@
 #
 #  *** #550, 2026-09-25: THE BLOCK IS DISPERSED, BY OWNER RULING 2026-09-24. ***  Each of the ten
 #  carries its OWN date, 2026-10-08 to 2026-12-03, and a `#550' line above it giving the reason for
-#  THAT date, in owed-work order: the cheapest first; the four Alpha probes within days of each other,
-#  because one round discharges all four; the four wdc probes a week or more apart, each owing its own
-#  oracle.  NOTHING ENFORCES DISTINCT DATES -- this checker reads each date alone -- and "no date on
+#  THAT date, in owed-work order: the cheapest first; the four Alpha probes on four working days in a
+#  row, 10-22 to 10-27, because one round discharges all four (10-29 is left free, in that round's
+#  week); the four wdc probes a week or more apart, each owing its own instrument work.  NOTHING
+#  ENFORCES DISTINCT DATES -- this checker reads each date alone -- and "no date on
 #  another list's date" is a cross-list property no check here sees (gate 9's AB_EXEMPT holds twelve
-#  entries on one date).  Filed as `exemptdistinct'.
+#  entries on one date: grep -A13 '^AB_EXEMPT="' regress/gate_asan_sweep.sh | grep -c ':2026-11-30').
+#  Filed as `exemptdistinct'.
 #
 #  These are wiring jobs, not design ones.  NOT every probe here prints a verdict token or exits
 #  nonzero on failure: mk48_nvram_probe.py printed MK48_RESULT=n/m and a DONE sentinel and exited 0
@@ -2543,13 +2545,16 @@
     #  a post-fix one and compare.  No gate builds a second leg, so wiring them is
     #  a change to the instrument -- a single-leg mode asserting only the fix-side
     #  wants against the gate's own binary -- not a line in a gate script.
-    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): owes a single-leg ORACLE -- its `ok' needs both legs (b_hit and f_hit) -- queue row `wdcaltoffleg' (a).
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): owes queue row
+    #  `wdcaltoffleg' two things -- its item (a), an exit status (the probe exits 0 whatever its `ok'
+    #  says), and a single-leg form, because every ROWS entry carries a want for the committed leg
+    #  (`wb') that the gate's one binary cannot supply.
     "wdc_altoffset_probe.py":     ("2026-11-05",
                                    "two-leg differential; wants a single-leg mode "
                                    "before gate 10 can assert anything"),
     #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): owes a redesign -- its oracle cannot tell the outcomes apart -- `wdcaltoffleg' (c).
-    #  (Its tuple said it needs "a ciR: CD-ROM rig the battery does not build" until #550: false -- the
-    #  probe applies the ciR: prefix itself and gate 10 already carries the malta image.)
+    #  (Its tuple said it needs "a ciR: CD-ROM rig the battery does not build today" until #550: false -- the
+    #  probe takes any image as argv[2] and applies the ciR: prefix itself.)
     "wdc_altoffset_sig_probe.py": ("2026-11-19",
                                    "two-leg differential; its oracle cannot tell the "
                                    "outcomes apart -- a redesign, wdcaltoffleg (c)"),
@@ -2568,54 +2573,69 @@
     #  What remains is the instrument: this probe prints no RESULT/CONTROL lines.  (This sentence went
     #  on "so a gate could only score its exit status" until #550: false -- it prints ok/FAIL rows,
     #  `SCORE n/m' and a DONE line, which a gate can score by rows, as gate_arm.sh scores mk48's.)
-    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): the cheapest of the ten -- 24/24 in under a second on a machine gate_ppc.sh already runs;
-    #  owed: RESULT/CONTROL lines, then a gate_ppc.sh block beside rldimi/rlwimi.  The parked
-    #  working-tree edit of its want_rldimi touches no scored row and is no prerequisite.
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): the cheapest of
+    #  the ten -- 24/24 in under a second on a machine gate_ppc.sh already runs (the run:
+    #  regress/artifacts/exemptredate_20260925/opus550_measured_p2/p1_runs/); owed: RESULT/CONTROL
+    #  lines, then a gate_ppc.sh block beside rldimi/rlwimi.  Its scored rows call none of
+    #  want_rldimi, want_rlwimi, want_rlwinm or mask32, so an edit of those helpers is no
+    #  prerequisite.
     "ppc_rldicl_probe.py":         ("2026-10-08",
                                     "gate_ppc.sh now executes -M 64 (rlwimi/rldimi); this "
                                     "probe lacks the RESULT/CONTROL protocol a gate parses "
                                     "-- that instrument change is filed to wiringcliff"),
     #  #520's detector.  NOT a two-leg differential and not awaiting a design -- it is a
     #  single-leg 15-row instrument that runs green on the fix today.  What it lacks is a
-    #  HOME: no gate in this tree runs an Alpha machine at all.
+    #  HOME: no gate in this tree runs an Alpha guest session -- gate 9's sweep constructs alphabook1
+    #  and runs nothing on it (this said "an Alpha machine at all" until #550).
     #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): one harness round gives an `-E alpha -e alphabook1' session a gate home and discharges
     #  all four Alpha probes at once (each already prints its tokens and sends quit), so the four
     #  are ONE decision, dated within days of each other rather than a week apart.
     "alpha_tbi_probe.py":          ("2026-10-22",
-                                    "no gate runs an Alpha machine; gate_crossfamily.sh "
+                                    "no gate runs an Alpha guest session (gate 9 only "
+                                    "constructs one); gate_crossfamily.sh "
                                     "is the named home and giving it one is a harness "
                                     "round, filed to wiringcliff"),
     #  #518's detector.  Same footing as #520's: a single-leg 75-row instrument, green on the
     #  fix, with no HOME.
-    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): the same alphabook1 home as alpha_tbi: one round discharges all four, so they fall due together.
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): same alphabook1
+    #  home as alpha_tbi; one round discharges all four.
     "lca_badval_probe.py":         ("2026-10-23",
-                                    "no gate runs an Alpha machine; gate_crossfamily.sh "
+                                    "no gate runs an Alpha guest session (gate 9 only "
+                                    "constructs one); gate_crossfamily.sh "
                                     "is the named home, filed to wiringcliff with #520"),
     #  #530's detector.  Same footing as #518's: single-leg, green on the fix, and no gate in
-    #  this tree runs an Alpha machine.
+    #  this tree runs an Alpha guest session.
     #  #530's width row.  SAME footing as lca_isalane_probe.py below: no gate in this tree runs an
-    #  Alpha machine.  Adding it here is stated in #530's record, not done silently.
-    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): the same alphabook1 home as alpha_tbi: one round discharges all four, so they fall due together.
+    #  Alpha guest session.  Adding it here is stated in #530's record, not done silently.
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): same alphabook1
+    #  home as alpha_tbi; one round discharges all four.
     "lca_widewrite_probe.py":      ("2026-10-26",
-                                    "no gate runs an Alpha machine; gate_crossfamily.sh "
+                                    "no gate runs an Alpha guest session (gate 9 only "
+                                    "constructs one); gate_crossfamily.sh "
                                     "is the named home, filed to wiringcliff with #518/#520/#530"),
-    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): the same alphabook1 home as alpha_tbi: one round discharges all four, so they fall due together.
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): same alphabook1
+    #  home as alpha_tbi; one round discharges all four.
     "lca_isalane_probe.py":        ("2026-10-27",
-                                    "no gate runs an Alpha machine; gate_crossfamily.sh "
+                                    "no gate runs an Alpha guest session (gate 9 only "
+                                    "constructs one); gate_crossfamily.sh "
                                     "is the named home, filed to wiringcliff with #518/#520"),
     #  #531's detector, on the SAME footing as #518/#520/#530 (it took their date too, so the
     #  cliff stayed one date, until #550 dispersed the block).  This comment said: "`grep -ln
-    #  "E sgi|-e ip30" gate_*.sh` matches ONLY gate_asan_sweep.sh ... no gate in this tree could
+    #  "E sgi|-e ip30" gate_*.sh` matches ONLY gate_asan_sweep.sh ... no gate in this tree that could
     #  host it today."  CORRECTED by #550: as written that grep matches nothing (`|' is literal in a
-    #  basic regex), and even as an extended regex it searches gate_*.sh, where the machine never
-    #  appears -- the probes exec it themselves; gate_arm.sh already runs seven `-E sgi -e ip32'
-    #  cold-debugger probes, so a home exists.  *** NOT classified `witness' to escape the requirement: the flagship seat found
+    #  basic regex), and as an extended regex it matches only gate 9's construction sweep
+    #  (gate_asan_sweep.sh runs `-E sgi -e "$s"') -- guest-session probes exec the machine
+    #  themselves; gate_arm.sh already runs seven `-E sgi -e ip32' cold-debugger probes (grep -cE
+    #  '^python3 sgi_[a-z_]+_probe[.]py' regress/gate_arm.sh; each execs -e ip32 itself), so a home
+    #  exists.  *** NOT classified `witness' to escape the requirement: the flagship seat found
     #  that exact dodge elsewhere in this manifest -- an ungated DETECTOR relabelled WITNESS,
     #  after which the checker verifies it is ungated -- and named it a check that cannot
     #  fail.  This entry is the honest form: DETECTOR, ungated, dated, and filed. ***
-    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): gate_arm.sh hosts seven sgi cold-debugger probes of this shape; about 570 s per
-    #  run, because each surviving session waits out the 12 s death poll -- a long gate guest until
-    #  that window shrinks without reading a delayed abort as alive.
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): gate_arm.sh hosts
+    #  seven sgi cold-debugger probes of this shape; 568 s for 33/33 on build/gxemul (the run:
+    #  regress/artifacts/exemptredate_20260925/opus550_measured_p2/p1_runs/), because each surviving
+    #  session waits out the 12 s death poll -- a long gate guest until that window shrinks without
+    #  reading a delayed abort as alive.
     "artifacts/ip30abortkill/ip30_abort_probe.py":
                                    ("2026-10-15",
                                     "no gate runs an SGI IP30 guest session (gate_asan_sweep.sh "
```

### 4b. #550 v2 -> v3: regress/gate_offline.sh

```diff
--- regress/gate_offline.sh	2026-09-25 15:25:31.443417100 -0500
+++ regress/gate_offline.sh	2026-09-25 16:30:52.800983200 -0500
@@ -2288,9 +2288,10 @@
 #                  dev_wdc.c -- which is the OTHER control, already present.  This one needs
 #                  the nine row functions refactored onto a shared helper first: a round, not
 #                  a line.
-#                  *** #550, 2026-09-25: THIS CENSUS IS STALE. ***  "The nine row functions"
-#                  is the 2026-08-19 count; since #484 (2026-08-27) `chk(name, got, want)'
-#                  has carried 24 got/want rows.  #551 replaces this paragraph.
+#                  *** #550, 2026-09-25: THIS CENSUS IS INCOMPLETE. ***  It counts the nine row
+#                  functions (2026-08-19) and leaves out `chk(name, got, want)', which #484 added
+#                  on 2026-08-27: 24 chk() calls, 16 got/want and 8 handing it a 0/1 verdict.
+#                  #551 replaces this paragraph.
 #  RE-DATED 2026-09-18 BY OWNER RULING, from 2026-09-02 -- a date that passed with no owner row: the
 #  "no exemption is past its dated deadline" row below went RED on every run from 2026-09-03, and the
 #  first run to OBSERVE it was 2026-09-18, the weekly battery having been disabled.  A re-date is not a
@@ -2298,7 +2299,8 @@
 #  #550, 2026-09-25: DECIDED SEPARATELY BY OWNER RULING 2026-09-25 (row `scexempt'); the comparison is a
 #  strict `<', so each entry is valid ON its own date and RED from the next day.
 #    ieee_store    RE-DATED to 2026-12-10, its reason above standing (nine counters, no comparator:
-#                  the larger refactor, dated after the wdc work).  RED from 2026-12-11.
+#                  the larger refactor, dated after the wdc work).  RED from 2026-12-11.  Owner
+#                  row `scexempt': discharge, re-decide or delete before then.
 #    wdc_identify  NOT re-dated: the owner ruled it FIXED -- #551 gives it a comparator self-check and
 #                  moves it to SC_COVERED.  Until #551 lands, valid ON 2026-09-27, RED from 2026-09-28.
 SC_EXEMPT="ieee_store:2026-12-10 wdc_identify:2026-09-27"
```

### 4c. #551 -> #551b: regress/diff_wdc_identify.c

```diff
--- regress/diff_wdc_identify.c	2026-09-25 15:30:34.592530900 -0500
+++ regress/diff_wdc_identify.c	2026-09-25 16:29:27.233710200 -0500
@@ -5652,23 +5652,26 @@
  *  WHAT IT COVERS: the rows that go through chk() and row_cmp() -- the last run prints how many calls
  *  each comparator took.  Of chk()'s calls, the ones in row_ring_occupancy_sound() that pass a
  *  `cond ? 1 : 0' (or `? 0 : 1') hand it a VERDICT computed at the call, not a comparison, and every
- *  other row in this file compares inline: neither is covered by this block.  NOT CAUGHT, DISCLOSED: a
- *  rows-keyed or name-keyed test inside either comparator, placed before its `rows ++', keeps every gate-2
- *  row green while silencing any covered row except the self-mutant's -- the first-and-last placement
- *  does not close it (after the increment, the same test reds through `failures').  Reviewed in the
- *  differential, not chased.  No line this block prints carries the self-mutant row's text or "high
- *  byte" (gate 2 counts both), and gate 2's G text is printed ONCE, by the last run, only when both runs
- *  passed.  The rest of the file is filed as `wdcidcomparators' (#551; owner ruling 2026-09-25).
+ *  other row in this file compares inline: neither is covered by this block.  "Covered" means the
+ *  COMPARATOR is live, not that a row is.  NOT CAUGHT, DISCLOSED: a test keyed on a value, a name or a
+ *  position the probes do not present, in either comparator, and an edit of the code that FEEDS them
+ *  (row() handing row_cmp() its own want), keep every gate-2 row green -- measured, pass 2 of #551;
+ *  reviewed in the differential, not chased.  No line this block prints carries the self-mutant row's
+ *  text or "high byte" (gate 2 counts both).  Gate 2's G text is printed ONCE, by the last run, only
+ *  when both runs passed -- and the run's own PASS needs that line (sc_g), so a self-check that failed
+ *  fails the run even if its forced failure is gone.  The rest of the file is filed as
+ *  `wdcidcomparators' (#551; owner ruling 2026-09-25).
  */
 static int sc_first_bad = -1;	/*  -1 until the FIRST run has happened  */
+static int sc_g;	/*  set ONLY where gate 2's G line prints: the run's PASS needs it  */
 
 static void selfcheck(const char *where)
 {
 	static const long long cg[] = { 1, 0x100000000LL, 0, 0, 7 };
 	static const long long cw[] = { 2, 0, 1, 0x100000000LL, 7 };
-	static const uint64_t rw[] = { 2, 2, 1, 3 };
-	static const uint64_t r57[] = { 1, 2, 0, 3 };
-	static const uint64_t r60[] = { 2, 1, 0, 3 };
+	static const uint64_t rw[] = { 2, 2, 1, 3, 0x100000000ULL, 0x100000000ULL };
+	static const uint64_t r57[] = { 1, 2, 0, 3, 0, 0x100000000ULL };
+	static const uint64_t r60[] = { 2, 1, 0, 3, 0x100000000ULL, 0 };
 	int sc_f = failures, sc_r = rows, sc_c = chk_calls, sc_rc = rowcmp_calls, sc_bad = 0, i, n = 0;
 
 	for (i = 0; i < 5; i++, n++) {
@@ -5677,7 +5680,7 @@
 			sc_bad++;
 		failures = sc_f; rows = sc_r;
 	}
-	for (i = 0; i < 4; i++, n++) {
+	for (i = 0; i < 6; i++, n++) {
 		row_cmp("@@SELFCHECK@@/row", rw[i], r57[i], r60[i]);
 		if (failures != sc_f + (r57[i] != rw[i] || r60[i] != rw[i]))
 			sc_bad++;
@@ -5694,10 +5697,11 @@
 			printf("  ok    SELFCHECK(first): all %d probes answered right\n", n);
 		return;
 	}
-	if (!sc_bad && sc_first_bad == 0)
+	if (!sc_bad && sc_first_bad == 0) {
+		sc_g = 1;
 		printf("  ok    SELFCHECK the comparator can still fail (first and last)\n");
-	else if (!sc_bad)
-		printf("  FAIL  SELFCHECK(last): the first run did not pass\n");
+	} else if (!sc_bad)
+		printf("  FAIL  SELFCHECK(last): the first run did not run, or did not pass\n");
 	printf("  note  SELFCHECK comparator calls this run: chk() %d, row_cmp() %d\n",
 	    chk_calls, rowcmp_calls);
 }
@@ -5807,9 +5811,9 @@
 	}
 
 	printf("\n%d rows, %d failures\n", rows, failures);
-	if (failures == 0)
+	if (failures == 0 && sc_g)
 		printf("WDC_IDENTIFY_PASS\n");
 	else
 		printf("WDC_IDENTIFY_FAIL\n");
-	return failures ? 1 : 0;
+	return (failures || !sc_g) ? 1 : 0;
 }
```

### 4d. #551 -> #551b: regress/gate_offline.sh (this diff also carries 4b's two hunks, since #551 sits on #550)

```diff
--- regress/gate_offline.sh	2026-09-25 15:29:15.981166600 -0500
+++ regress/gate_offline.sh	2026-09-25 16:30:53.012469700 -0500
@@ -2256,14 +2256,17 @@
 #    * geom      -- every row but the identity row, via BOTH geom() and parse(), which are
 #                   two separate comparators and are probed separately for that reason.
 #    * sync      -- both checks() and checkn(), for the same reason.
-#    * wdc_identify -- 24 of 128 rows compare inside a comparator the sentinel feeds (chk() 16,
-#                   row_cmp() 8); 8 more hand chk() a 0/1 verdict computed at the call (derive:
-#                   grep -cE '\? [01] : [01], 1\);' regress/diff_wdc_identify.c), and the other
-#                   96 compare inline -- NOT covered.  The file prints its comparator call counts
-#                   on every run.  A rows- or name-keyed test inside either comparator, placed
-#                   before its rows ++, keeps every gate-2 row green while silencing any covered
-#                   row but the self-mutant's: disclosed, not chased.  #551, by owner ruling
-#                   2026-09-25 ("24/128 now, file the rest"); the rest is `wdcidcomparators'.
+#    * wdc_identify -- 24 of 128 rows compare inside a comparator the sentinel feeds: 16 of
+#                   chk()'s 24 calls and all 8 of row_cmp()'s.  chk()'s other 8 are handed a 0/1
+#                   verdict computed at the call (derive: grep -cE '\? [01] : [01], 1\);'
+#                   regress/diff_wdc_identify.c), and the other
+#                   96 compare inline -- NOT covered.  "Covered" means the COMPARATOR is live,
+#                   not that a row is: an edit of the code that feeds it (row() handing
+#                   row_cmp() its own want), or a test keyed on a value, a name or a position
+#                   the probes do not present, keeps gate 2 green -- measured on #551's pass 2,
+#                   disclosed, not chased.  The file prints its comparator call counts on every
+#                   run, and its PASS needs the G line.  #551, by owner ruling 2026-09-25
+#                   ("24/128 now, file the rest"); the rest is `wdcidcomparators'.
 #  rtc_range is in the UNIFORM group: every row goes through chk(), its single comparator.
 #  Named here rather than left to be re-derived, because the exception list above
 #  is only trustworthy if additions are classified as they arrive.
@@ -2272,8 +2275,8 @@
 #
 #  THE EXEMPTIONS, DATED AND REASONED.  A FORTNIGHT, matching the deadline the owner chose
 #  over the Q4 one I proposed for the selfmutant list: 2 uncovered differentials, 1311 and 766
-#  lines, whose every row could be inert with this gate green.  (Then; #551 moved wdc_identify to
-#  COVERED, so ieee_store is the one left.)
+#  lines, whose every row could be inert with this gate green.  (True when written; #551 moved
+#  wdc_identify to COVERED, so ieee_store is the one left.)
 #
 #    ieee_store    HAS NO COMPARATOR TO SENTINEL.  No check(), no `rows`, no `failures`: each
 #                  section carries its own counter -- nine of them are the `== 0' terms of its
@@ -2300,7 +2303,8 @@
 #  #550, 2026-09-25: DECIDED SEPARATELY BY OWNER RULING 2026-09-25 (row `scexempt'); the comparison is a
 #  strict `<', so each entry is valid ON its own date and RED from the next day.
 #    ieee_store    RE-DATED to 2026-12-10, its reason above standing (nine counters, no comparator:
-#                  the larger refactor, dated after the wdc work).  RED from 2026-12-11.
+#                  the larger refactor, dated after the wdc work).  RED from 2026-12-11.  Owner
+#                  row `scexempt': discharge, re-decide or delete before then.
 SC_EXEMPT="ieee_store:2026-12-10"
 
 sc_missing=""
```

## 5. QUESTIONS

1. **Which of my dispositions in section 2 is wrong?  Name the count.**  Especially P14 (no change), P15 (no edit),
   P19 (not applicable), Q2/Q3 (disclosed, not closed) and Q9 (no change).
2. **Q5, the disagreement (section 3)** -- grok and agy especially: does `sc_g` change any healthy run, or should the
   run's verdict stay PASS when its self-check failed?
3. **The repair's own defects:** does any v3 or #551b hunk write a new false sentence while correcting one?  (Every
   correction here quotes or replaces something; a correction is not safer than the thing it corrects.)
4. **#551b: the smallest edit to the FINAL file that keeps gate 2 green while a covered row can no longer fail**,
   outside the disclosed classes (value/name/position-keyed tests; the feed edit).

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
