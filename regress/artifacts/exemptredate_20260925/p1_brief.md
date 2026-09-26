# #550 exemptredate -- PASS 1 on the exact proposed diff: eleven dated test exemptions re-dated one by one

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  Where I state something as fact, ask whether it is true.  A seat that re-derives a premise
from something this brief did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`.**  Other copies of GXemul under the project root
are not this fork.  **Do not read `regress/artifacts/` other than this round's own directory,
`regress/artifacts/exemptredate_20260925/`, and do not read `tools/pipeline/ledger.json`.**

**If you cannot read files that is expected** -- every fact you need is inlined.  Name any premise you cannot settle
from this packet rather than guessing at it.  **VERDICT LINE FIRST**: `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`,
then numbered findings.

## 0. HAS THIS ALREADY SHIPPED?  (run before writing this brief)

    git log -1 -- tools/pipeline/check_probe_wiring.py   ->  f4f601c4 2026-09-24 #548 fbdrainwire ...
    git log -1 -- regress/gate_offline.sh                ->  f4f601c4 (same commit)
    grep exemptredate CHANGELOG.md                        ->  nothing
No.  This is a new round, #550.

## 1. WHAT THIS IS

A test-harness change only -- no emulator code.  `tools/pipeline/check_probe_wiring.py` is a pre-commit checker: every
detector script under `regress/` must be run by a gate, or carry a DATED exemption.  An exemption is valid ON its date
and the checker FAILS from the day after (`d < today`), which blocks every commit.  Ten exemptions all carry
2026-09-27, so every commit from 2026-09-28 would be blocked.  Gate 2 (`regress/gate_offline.sh`) has a second,
separate list, SC_EXEMPT (two offline differentials exempt from a comparator self-check), also dated 2026-09-27; there
the expiry turns one gate row red rather than blocking commits.

## 2. PREMISES ALREADY SETTLED, RE-INLINED SO NOBODY SPENDS AN ANSWER RE-DERIVING THEM

* **Owner ruling 2026-09-24 (verbatim):** "Re-date all ten individually -- each gets its own date and reason now; no
  wiring work this week."  So wiring any of the ten probes is OUT of scope for this round, by decision, not oversight.
* **Owner ruling 2026-09-25, on SC_EXEMPT:** "Fix wdc_identify now" -- a separate round (#551) moves that differential's
  rows onto a shared comparator with a sentinel before 2026-09-28; only `ieee_store` is re-dated here.
* **The comparison is a strict `d < today`**, so an entry is GREEN on its own date and RED the day after.  The checker's
  own selftest derives its two boundary days (M5a on the earliest detector exemption's date, M5b the day after) from the
  table -- they are not literals (#536), so a re-date does not break the selftest by construction.
* **The constraint the re-date answers** (ledger row `exemptcliff`, filed 2026-09-17): eleven, then ten, entries were
  aligned on ONE date twice, so the checker reds on all of them at once and the natural response is a bulk re-date.
  "A date nobody chose is a date nobody owns."

## 3. THE PROPOSED DIFF, EXACT (three files; nothing else changes)

### 3a. tools/pipeline/check_probe_wiring.py

```diff
--- a/tools/pipeline/check_probe_wiring.py (HEAD f4f601c4)
+++ b/tools/pipeline/check_probe_wiring.py (proposed)
@@ -2505,6 +2505,12 @@
 #  *** #548, 2026-09-24: THE OTHER HALF IS GONE TOO. ***  fbpending_drain_probe.py is wired
 #  into gate_arm.sh and its entry deleted, so TEN of those eleven remain, still one block.
 #
+#  *** #550, 2026-09-25: THE BLOCK IS DISPERSED, BY OWNER RULING 2026-09-24. ***  Each of the ten
+#  carries its OWN date, 2026-10-08 to 2026-11-17, no two alike, and a `#550' line above it giving
+#  the reason for THAT date.  A slip now expires ONE entry and forces a decision about that entry --
+#  never a bulk push, which is what `exemptcliff' was filed against: a date nobody chose is a date
+#  nobody owns.
+#
 #  These are wiring jobs, not design ones.  NOT every probe here prints a verdict token or exits
 #  nonzero on failure: mk48_nvram_probe.py printed MK48_RESULT=n/m and a DONE sentinel and exited 0
 #  with rows red, so the gate_arm.sh section #536 wired for it scores ROWS, not a token (agy, #536
@@ -2535,63 +2541,74 @@
     #  a post-fix one and compare.  No gate builds a second leg, so wiring them is
     #  a change to the instrument -- a single-leg mode asserting only the fix-side
     #  wants against the gate's own binary -- not a line in a gate script.
-    "wdc_altoffset_probe.py":     ("2026-09-27",
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): the single-leg mode is an instrument change shared with the 4bit sibling; this probe builds it.
+    "wdc_altoffset_probe.py":     ("2026-11-02",
                                    "two-leg differential; wants a single-leg mode "
                                    "before gate 10 can assert anything"),
-    "wdc_altoffset_sig_probe.py": ("2026-09-27",
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): needs the single-leg mode AND a ciR: CD-ROM rig the battery does not build -- rig work after the mode.
+    "wdc_altoffset_sig_probe.py": ("2026-11-16",
                                    "two-leg differential AND needs a ciR: CD-ROM rig "
                                    "the battery does not build today"),
-    "wdc_altoffset_4bit_probe.py": ("2026-09-27",
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): reuses the single-leg mode its sibling builds, so it falls due the day after that sibling.
+    "wdc_altoffset_4bit_probe.py": ("2026-11-03",
                                     "two-leg differential; shares the single-leg-mode "
                                     "debt with its two siblings"),
-    "wdc_addtoinbuf_probe.py":     ("2026-09-27",
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): two-leg AND needs a poisoned CD image the battery does not build -- image work, last of the ten.
+    "wdc_addtoinbuf_probe.py":     ("2026-11-17",
                                     "two-leg differential AND needs a poisoned CD "
                                     "image the battery does not build"),
     #  #520's detector.  NOT a two-leg differential and not awaiting a design -- it is a
     #  single-leg 15-row instrument that runs green on the fix today.  What it lacks is a
-    #  HOME: no gate in this tree runs an Alpha machine at all.  Dated to fall due with
-    #  the others so the cliff stays one date rather than becoming a rolling excuse.
+    #  HOME: no gate in this tree runs an Alpha machine at all.  (It was dated with the block,
+    #  so the cliff stayed one date, until #550 dispersed the block by owner ruling.)
     #  #522's detector.  Single-leg, 0.2 s, green on the fix.  It lacks a gate that RUNS a
     #  64-bit PowerPC CPU: gate 9 constructs them but has no result oracle, and both PowerPC
     #  gates drive a 32-bit part.  Closing that is a harness round, filed to wiringcliff.
     #  *** ITS REASON EXPIRES WITH THE rlwimi/rldimi WIRING: gate_ppc.sh now EXECUTES -M 64. ***
     #  What remains is the instrument: this probe prints no RESULT/CONTROL lines, so a gate
     #  could only score its exit status, which gates here never trust.
-    "ppc_rldicl_probe.py":         ("2026-09-27",
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): its rldimi-oracle repair (the wrapping MASK) is parked in the working tree and is adopted with the
+    #  parked work after #549 (owner ruling 2026-09-24); the RESULT/CONTROL protocol follows that repair.
+    "ppc_rldicl_probe.py":         ("2026-10-15",
                                     "gate_ppc.sh now executes -M 64 (rlwimi/rldimi); this "
                                     "probe lacks the RESULT/CONTROL protocol a gate parses "
                                     "-- that instrument change is filed to wiringcliff"),
-    "alpha_tbi_probe.py":          ("2026-09-27",
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): one harness round gives gate_crossfamily.sh an Alpha machine; it follows the parked LCA/Alpha adoption.
+    "alpha_tbi_probe.py":          ("2026-10-20",
                                     "no gate runs an Alpha machine; gate_crossfamily.sh "
                                     "is the named home and giving it one is a harness "
                                     "round, filed to wiringcliff"),
-    #  #518's detector.  Same footing as #520's, and deliberately the same date so the
-    #  cliff stays one date: a single-leg 75-row instrument, green on the fix, with no HOME.
-    "lca_badval_probe.py":         ("2026-09-27",
+    #  #518's detector.  Same footing as #520's: a single-leg 75-row instrument, green on the
+    #  fix, with no HOME.
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): the same Alpha home; one day apart, so each falls due as its own decision and never as a block.
+    "lca_badval_probe.py":         ("2026-10-21",
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
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): the same Alpha home, one day apart.
+    "lca_widewrite_probe.py":      ("2026-10-22",
                                     "no gate runs an Alpha machine; gate_crossfamily.sh "
                                     "is the named home, filed to wiringcliff with #518/#520/#530"),
-    "lca_isalane_probe.py":        ("2026-09-27",
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): the same Alpha home, one day apart.
+    "lca_isalane_probe.py":        ("2026-10-23",
                                     "no gate runs an Alpha machine; gate_crossfamily.sh "
                                     "is the named home, filed to wiringcliff with #518/#520"),
-    #  #531's detector, and it takes the SAME footing and the SAME date as #518/#520/#530
-    #  rather than a longer one -- a later date would hide this debt behind the cliff instead
-    #  of joining it, and the cliff is already a filed row.  Measured before writing this:
+    #  #531's detector, on the SAME footing as #518/#520/#530 (it took their date too, so the
+    #  cliff stayed one date, until #550 dispersed the block by owner ruling).  Measured before
+    #  writing this:
     #  `grep -ln "E sgi|-e ip30" gate_*.sh` matches ONLY gate_asan_sweep.sh, which CONSTRUCTS
     #  machines and runs no guest session, so there is no gate in this tree that could host it
     #  today.  *** NOT classified `witness' to escape the requirement: the flagship seat found
     #  that exact dodge elsewhere in this manifest -- an ungated DETECTOR relabelled WITNESS,
     #  after which the checker verifies it is ungated -- and named it a check that cannot
     #  fail.  This entry is the honest form: DETECTOR, ungated, dated, and filed. ***
+    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): a binary-only cold-debugger probe (no rig image, no disk), so the cheapest wiring of the ten --
+    #  it is dated first.
     "artifacts/ip30abortkill/ip30_abort_probe.py":
-                                   ("2026-09-27",
+                                   ("2026-10-08",
                                     "no gate runs an SGI IP30 guest session (gate_asan_sweep.sh "
                                     "constructs only); filed to wiringcliff with #518/#520/#530"),
 }
```

### 3b. tools/precommit_check.sh

```diff
--- a/tools/precommit_check.sh (HEAD f4f601c4)
+++ b/tools/precommit_check.sh (proposed)
@@ -524,7 +524,8 @@
 #  Existing gaps are carried as DATED exemptions that EXPIRE, never as silent grandfathering; the
 #  dates live in check_probe_wiring.py's EXEMPT table, not here.  (They were 2026-09-20, chosen to
 #  fall due with gate_offline's fbpending_bound; #537 discharged that debt and #536 moved the
-#  block to 2026-09-27 by owner ruling.)
+#  block to 2026-09-27 by owner ruling; #550 dispersed it to ten individual dates, 2026-10-08
+#  to 2026-11-17, by owner ruling 2026-09-24.)
 #
 #  THE SELFTEST RUNS ONLY WHEN THE CHECKER ITSELF CHANGES.  --selftest applies its mutants (22, pinned below) to
 #  temp copies and asserts each exit status, which takes ~14 s -- too slow for every commit,
```

### 3c. regress/gate_offline.sh

```diff
--- a/regress/gate_offline.sh (HEAD f4f601c4)
+++ b/regress/gate_offline.sh (proposed)
@@ -2292,7 +2292,14 @@
 #  discharge: both reasons above stand unchanged, and this list's SM twin was ruled the other way
 #  ("fix it, do not re-date", #537).  The comparison is a strict `<`, so these are valid ON 2026-09-27
 #  and RED from 2026-09-28.  Owner row: `scexempt` -- discharge, re-decide or delete before then.
-SC_EXEMPT="ieee_store:2026-09-27 wdc_identify:2026-09-27"
+#  #550 (2026-09-25), OWNER RULING 2026-09-25 -- the two are decided SEPARATELY, not as a pair.
+#    ieee_store    RE-DATED to 2026-11-30, its reason above unchanged: it has no comparator at all,
+#                  so a sentinel needs its six inline counters moved onto one first -- the larger
+#                  refactor, dated after the wdc work so it falls due as its own decision.
+#    wdc_identify  NOT re-dated: the owner ruled it FIXED -- #551 moves its rows onto a shared
+#                  comparator with a sentinel and moves the stem to SC_COVERED before 2026-09-28.
+#                  Until #551 lands, its 2026-09-27 date stands and reds from the 28th.
+SC_EXEMPT="ieee_store:2026-11-30 wdc_identify:2026-09-27"
 
 sc_missing=""
 for f in "$HERE"/diff_*.c; do
```

## 4. MEASURED (on a `git archive` export of HEAD's `tools/` and `regress/*.py|*.sh`, with the proposed checker swapped in)

Control first: HEAD's own checker on that export -- `--today 2026-09-27` PASS; `--today 2026-09-28` FAIL with 10
problems, all `EXPIRED EXEMPTION`.  Then the proposed checker (`measured/schedule.out`, abridged to the transitions):

    2026-09-25 .. 2026-10-08   rc=0  PROBEWIRING_PASS
    2026-10-09  rc=1  expired: ip30_abort_probe.py
    2026-10-16  rc=1  + ppc_rldicl_probe.py
    2026-10-21  rc=1  + alpha_tbi_probe.py
    2026-10-22  rc=1  + lca_badval_probe.py
    2026-10-23  rc=1  + lca_widewrite_probe.py
    2026-10-24  rc=1  + lca_isalane_probe.py
    2026-11-03  rc=1  + wdc_altoffset_probe.py
    2026-11-04  rc=1  + wdc_altoffset_4bit_probe.py
    2026-11-17  rc=1  + wdc_altoffset_sig_probe.py
    2026-11-18  rc=1  + wdc_addtoinbuf_probe.py   (all ten)

`--selftest` on the proposed checker: `PROBEWIRING_SELFTEST_PASS  22/22 mutants behaved as specified`
(`measured/selftest_550_onHEAD.out`), M5a/M5b now derived from 2026-10-08.
Gate 2's `exempt_expired` helper, extracted and run on the proposed SC_EXEMPT: 09-27 none; 09-28 wdc_identify;
11-30 wdc_identify; 12-01 ieee_store wdc_identify.

## 5. QUESTIONS

1. **Premise audit.**  Each `#550` comment line states a FACT about the owed work and a REASON for its date.  Check the
   facts against the tree: is `ip30_abort_probe.py` really binary-only (no rig image, no disk)?  Is the rldimi-oracle
   repair of `ppc_rldicl_probe.py` really parked in the working tree (`git diff -- regress/ppc_rldicl_probe.py`)?  Do the
   four LCA/Alpha probes really share one missing gate?  Is `ieee_store`'s "six inline counters" right?  Any comment
   this diff edits or leaves that is now FALSE is a finding.
2. **What is the smallest edit to THIS diff that the checker, its selftest and gate 2 would all still pass, while the
   intent (each entry falls due ALONE, on a date someone chose) is broken?**  Name the edit and what stays green.
3. **Option-set completeness.**  Individual dates were chosen by the owner; within that, is anything in this diff a
   choice that should have been different -- a date order that will collide with the work queue, an entry that should
   be DELETED rather than re-dated because its prerequisite already exists, a comment that should name a queue row?
4. **The two lists are handled differently on purpose** (the checker blocks commits; gate 2 reds one row).  Is there any
   path by which the proposed SC_EXEMPT change blocks a commit or hides a red it should show?

If, while verifying a claim, you found something ELSE -- say so.
