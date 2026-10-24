# #571 (`ppcdsformxo`) pass-2 brief -- drafter's notes

Drafted 2026-10-24 09:1x-09:5x against HEAD `add098b9` plus the round's uncommitted working-tree edits.  Read-only on the
project: no `git status` / `git diff` / `git add`, no build, no emulator run, nothing written under `GXEMUL-SEC/`.
Dispositions are questions for the panel; the drafter rules on nothing.

## Files and sizes

| file | bytes | what it is |
|---|---:|---|
| `brief_FULL.md` | **228,802** | file-reading seats (GPT-6 Astra, Grok 4.7); the AUTHORITY |
| `brief_COMPACT.md` | **88,607** | Gemini 4 Argon through agy (file-reading); under the 90,000 aim |
| `brief_PACKET.md` | **74,373** | packet-fed seats (GLM 5.3, DeepSeek); stands alone.  With the launcher's Q12/Q34 line inserted (simulated in memory with `launch_p2.sh`'s own strings): 74,589 / 74,629 -- under 75,000 |
| `C0_OUTPUT.txt` | 6,869 | the §C0 commands' output (git log / show / ls-files only), run 09:25 |
| `LS_PERMITTED.txt` | 6,862 | the `[ -e ]` + HEAD-equality check of every path the briefs invite a seat to open, run 09:26; no MISSING line |

* Sections 6 (settled premises), 7 (the drafter's checks K1-K14) and 11 (QUESTIONS) are byte-identical in all three
  briefs (checked by the builder).  Each brief has exactly one line matching `^## [0-9]+[.] QUESTIONS.*`, and it is exactly
  `## 11. QUESTIONS`.  Every `~~~~` fence is balanced.  All three files are UTF-8, LF only.
* Every verbatim excerpt was copied from its file at build time by a script (`t2/brief2v/build2.py` with the templates
  `full.tpl`, `compact.tpl`, `packet.tpl` and the shared fragments `shared_*.md` in the same directory), never retyped.
  The three `.patch` files were checked to reproduce the working-tree files exactly when applied (`patch`) to the HEAD blobs.
* The CHANGELOG round-block draft, the witness-term draft and the OUTSTANDING_BUGS draft were FROZEN at drafting
  (`t2/brief2v/frozen_*`; md5 `2f9af871`, `3f755d68`, `51b949ae`, identical to `t2/landing/` at 09:2x) and inlined into
  FULL section 9; the briefs tell the seats not to open the scratchpad.
* Records with their own `#` headings (BASELINE, PRETABLE, C0, the drafts, BUILD_REPORT, LS_PERMITTED, the gate-log excerpt)
  are indented two spaces inside their fences in FULL; the briefs say so.

## Deviations from DRAFTER_INPUTS.md, with the reason

1. **Q2's ask-again is put in the COVERAGE form, not as "name the smallest edit".**  BRIEF_TEMPLATE §C5 rule 3: a brief
   that reaches codex must not ask for "the smallest edit that re-opens this" (the construction ask was measured to draw
   content-filter refusals); its own substitute is "which inputs does the repair change the answer for, and which does it
   leave alone -- enumerate the partition".  Q2(e) asks the seats to enumerate the case bodies' input cells, mark each
   OBSERVED (with its row) or UNOBSERVED, and for an unobserved cell give the shipped result, the observable that would
   differ and the NOT CLAIMED bullet that discloses it (or say none does: a floor question).  That yields the same three
   things the input asked for (where an edit would live, its predicted channel, which disclosed cell) without asking for a
   construction.  The same wording is in all three forms (section 11 is shared).
2. **The detector's session programs are a CONDENSED table in COMPACT and PACKET** (generated from the probe's own program
   objects, imported with bytecode writing disabled -- no emulator run, nothing written), and PACKET's `prefix_BASE.out` rows
   are condensed to name / got / want / status; FULL carries both VERBATIM.  This is what fit PACKET under 75,000.
3. **The verdict vocabulary is READY TO LAND | LAND WITH CHANGES | DO NOT LAND** (the task's instruction) -- see item 16.
4. A glossary sentence in each section 0 explains the records' mutation-testing shorthand ("kills" a leg = turns red under
   it), because the FULL brief quotes `PRETABLE.out`'s CHANNEL column verbatim and FULL reaches the codex seat (§C5 rule 1);
   the drafter's own text uses "detects" / "table of variant legs".

## Inconsistencies found -- the records against the files (17)

Each was read or run at drafting; K-numbers are the brief's section-7 checks, where the panel is asked about it.

1. **The detector's line count (K5).**  `wc -l regress/ppc_dsform_probe.py` = 836 (40,883 bytes, md5 `0266228...`);
   `DETECTOR_FREEZE.txt` says 836; `DRAFTER_INPUTS.md`, `BUILD_REPORT.md` section 1 and the CHANGELOG draft say **834**.
2. **The names-cap reason (K1).**  `PASS1_RULINGS.md` F2 (B12): "a 15-character name passes the assert and MISSES the pin";
   carried into `BUILD_SPEC.md` 10b item 3, the probe's `row()` comment ("14, not 15: gate 13 pins each row as `^name  `
   (two spaces) inside this %-16s column") and the CHANGELOG draft ("Grok also caught the padded-column trap ...").  Measured:
   the format `"%-16s %-20s ..."` gives a 15-character name two spaces; `lib.sh`'s `count` (`grep -ac -- "^$v  .*ok$"`) on four
   synthetic lines counts 13-, 14- and 15-character names 1 and a 16-character name 0.  The cap of 14 is harmless; its
   stated reason is false.
3. **The session count (K2).**  `gate_ppc.sh`'s new comment: "Eight debugger-stepped sessions (loads, stores and five stop
   sessions ...) and one bogus-machine session" (lists seven, reads as nine).  The CHANGELOG draft: "EIGHT stepped sessions
   on `-E bareppc -M 64`" including the negative apparatus, which runs `-E nosuchmachine`; `DETECTOR_FREEZE.txt`'s header
   "SESSIONS (eight), each `-E bareppc -M 64'" while its item 8 is `-E nosuchmachine`; the OUTSTANDING_BUGS draft "eight
   debugger-stepped sessions".  The probe's docstring ("SESSIONS -- eight", counting the negative one) is the consistent
   form: seven guest sessions + one negative.
4. **SCORES.txt L5b and gate 13 (K3).**  "the gate's sentinel pin reds" -- but `gate_ppc.sh` :103 `need_exec "$PMAX"` SKIPs
   gate 13 on an absent binary before the `#571` block runs (`lib.sh` :153-157); the `#565` block's comment (:180-181) says
   so for its own probe.
5. **SCORES.txt's driver names (K4).**  "`s6_leg.run-083332.sh` + `legs571.run-083332.py`"; `s6_all.out` line 1 and the
   files on disk are `s6_leg.run-083428.sh` / `legs571.run-083428.py` (session scratchpad `t2/build/`; no `083332` copy
   exists; none is frozen under `table1_20261024/`).
6. **PRETABLE's CHANNEL for `lwa ra0 value` (K6).**  "kills L5, L8a, L8b, L9b"; measured green under L9b
   (`L9b_xo0plus1.out`) and red under BASE, L3, L4b, L5, L7, L8a, L8b, L8c, L10.  `DETECTOR_FREEZE.txt`'s notes carry the
   correction; PRETABLE (correctly unedited) does not.
7. **A line citation the commit moves (K8).**  The CHANGELOG draft cites the RA = 0 guard as `:4338-4342` (HEAD's numbering);
   in the committed file it will be `cpu_ppc_instr.c` :4367-4371.
8. **What ships (K9).**  The CHANGELOG draft: "one product file ...; three harness files" -- omits `tools/precommit_check.sh`
   (SCORE_CLAIMS_MANIFEST 38 -> 39), which `BUILD_REPORT.md` section 2 and `diff_precommit.patch` list.
9. **The stores list (K10).**  The CHANGELOG draft's "`std` at DS = 0 and RA = 0" reads as the DS = 0 x RA = 0 joint, which is
   NOT CLAIMED; the detector has two separate words (`std ds0`, `std ra0`).
10. **"eight amendments accepted" (K11).**  The CHANGELOG draft's count for Astra's adjudication; `PASS1_RULINGS.md` F1 lists
    eleven amended items (A3, A6, A9/B9, B2, B7, B10, B11/B13, B12, C4, Q3, Q5); `BUILD_SPEC.md` section 10 has eight items.
11. **Spec-required report sentences missing, and C4's qualifications (K12).**  `BUILD_SPEC.md` section 10 item 7 ("The C4
    census in the report says 'at least fourteen' ... and notes `extsw`'s MODE32 handler diagnoses and returns") and section
    8 ("No boot A/B is owed ...; say so in the report"): `BUILD_REPORT.md` carries neither (grep: no "fourteen", "extsw" or
    "boot").  The CHANGELOG draft has "at least fourteen" but no `extsw` note.  The OUTSTANDING_BUGS draft gives
    `ppc64on32gate` as "LOW, open, design" (PASS1_RULINGS C4 and DRAFTER_INPUTS: "design") and says "the uniform
    `rld*`-idiom fix is its own round" against F1's "the filing does not pre-authorise a uniform sweep".
12. **Times (K13).**  `PRETABLE.out`'s header "written 2026-10-24 ~08:0x" -- mtime 07:56:54 (BUILD_REPORT: 07:56).
    `BUILD_REPORT.md` section 6 "09:03:54-09:1x" -- the gate log ends "=== 2026-10-24 09:05:23 done".  `BUILD_REPORT.md`
    "08:30 PREDICTIONS.txt" -- mtime 08:32:01.  Every order proof still holds.
13. **A PRETABLE window the detector lacks (K14).**  PRETABLE section 4: the stores session is "seeded ... at 0x21000.. and at
    0x7100.. / 0x0.. for RA = 0 / DS = 0"; the frozen detector seeds 0x21000-0x210bf and 0x70f0-0x711f only (`ST_REGIONS`);
    the 0x0 window belonged to the `std both val` row F2 removed.
14. **DRAFTER_INPUTS line numbers.**  "src/cpus/cpu_ppc_instr.c ~:4307 and ~:4330 after the edit" -- `case PPC_HI6_LD:` is at
    :4307, `case PPC_HI6_STD:` at **:4339** (HEAD :4320).
15. **DRAFTER_INPUTS's BASELINE description.**  "every tree at HEAD 87a766e0" -- `87a766e0` is the md5 of
    `src/cpus/cpu_ppc_instr.c` at HEAD (`BASELINE.out`); HEAD is `add098b9`.
16. **The launcher's verdict vocabulary.**  `t2/launch_p2.sh`'s Astra pointer and agy prompt say "VERDICT line first (READY |
    READY WITH CHANGES | NOT READY)"; the briefs (per this task) ask for READY TO LAND | LAND WITH CHANGES | DO NOT LAND.  The
    launcher's closing `grep -m1 -oE 'VERDICT[^|]{0,160}'` works for either, but the two seats would see two vocabularies.
    Align the pointer text (or the brief) before firing.
17. **The roster record vs the launcher.**  `pass2_20261024/roster_NOT_FIRED.txt`: "GLM 5.3 + DeepSeek + Grok 4.7 + Argon
    review; GPT-6 Astra adjudicates"; `DRAFTER_INPUTS.md` and `launch_p2.sh` fire Astra on the FULL brief as a reviewer too
    (as in pass 1).  The briefs' roster says "reviews this pass, then ADJUDICATES".  Also: `launch_p2.sh`'s agy prompt limits
    artifacts to `witness_20261024\` and `table1_20261024\` "ONLY", while COMPACT also permits `pass1_20261024/PASS1_RULINGS.md`
    and `BUILD_SPEC.md` (the records section 6 cites) -- harmless, but the two texts differ.

## Checked and consistent (so nobody re-checks them)

* `PASS1_RULINGS.md` B1 / the CHANGELOG draft name the BASE binary's source as `c8fcb5ff`; `BASELINE.out` names HEAD
  `add098b9`; C0: no commit `c8fcb5ff..HEAD` touches `src/` (`add098b9` is records-only) -- both names are right.
* Every leg's `RED=` list and score in `SCORES.txt` equals its `.out` file (seventeen results plus L5b); 14 of 16 legs at
  prediction, L9a and L10 two rows redder, as `SCORES.txt` says.  `prefix_BASE.out` and `L3_armHEAD.out` have the same 17
  red rows; L3's rebuilt binary has the BASE binary's md5 (`3cd0501c`) and the HEAD blob's source md5 (`87a766e0`).
* Gate 13: the `#571` block's 53 checks (1 + 1 + 4 + 4 + 39 + 1 + 3), `PASS (193 checks)`, `REGRESS_PASS`, `RUN_RC=0`;
  `gate13_ppc_dsform.log`'s 39 row lines equal `fixed.out`'s.
* Clearance re-run read-only at drafting: md5 `2015e243` in SEC, est/, build/, build-asan/, /tmp/gxsec-build; build/
  (`a142d92a`), build-asan/ (`79d75442`), /tmp/gxsec-build (`14ede3bd`) FRESH; no `.MUTANT` sentinel.
* The staged copies: `staged/gate_ppc.sh.txt` == `regress/gate_ppc.sh` (md5 `d361db09`); `staged/check_probe_wiring.py.txt`
  == the HEAD blob plus exactly the two keys; the working-tree checker = HEAD + 15 peer lines + the same two keys.
* The four filing ids have zero rows in the HEAD ledger; the working-tree ledger's `ppcdsformxo` row is unchanged from HEAD
  (its nine changed rows are other sessions'); `CHANGELOG.md` and `regress/pass2_ledger.tsv` do not name the row.
* `cpu_ppc.c` :1495 / :1498 / :1517 (C1) and :1468-1489 (C2), Book I :2297-2621 and PEM :6253 say what the records cite.
* The witness's `MANIFEST.md5` (6 of 6) and `receipts/MANIFEST.md5` (6 of 6) verify.
