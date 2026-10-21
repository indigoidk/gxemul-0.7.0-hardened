VERDICT: 9 wrong records, 10 overtaken, 7 refuted, 2 to file -- HEAD 5dbc000e already carries every correction Argon asked of #566 (it read a pre-commit draft); what survives is in the probe's own text: the #566 note's clause-(b) absence, stale since d42c76a8 measured it at 14/33, and eight more probe sentences that are false of the probe that ships (four are Argon's P:466/521/620/634, four are siblings found while checking them); no new measured-false-pass candidate -- the stall false-green Argon describes is disclosed and filed as `ip30stallgreen`.

Seat: records check, read-only.  Token IP30FLAG_ALIVE_20261020.  Repository GXEMUL-SEC at HEAD 5dbc000e.  Every quote below is
`git --no-optional-locks show HEAD:<path>`, with HEAD's line numbers.  Nothing was built or run except two read-only
re-derivations in this directory (section U on exported copies; a dry-run of edits.diff on copies).

## 0. What Argon read, against what shipped

Argon's packet (`argon_bundle_1.txt` / `_2.txt`, written 2026-10-18 11:41) inlined DRAFTS.  The `#566` commit `8faf4a16`
(15:03 the same day) shipped different bytes for four of the five files:

| file | packet blob (draft) | committed blob | HEAD |
|---|---|---|---|
| regress/gate_arm.sh | 88f7e719 | 887c3302 | = commit |
| regress/artifacts/ip30abortkill/ip30_abort_probe.py | 3c552ed9 | 96252180 | = commit |
| tools/precommit_check.sh | 8ab4e020 | c157ab43 | +#567 lines only |
| OUTSTANDING_BUGS.md | 91df8af2 | 6f1012bd | +later blocks |
| tools/pipeline/check_probe_wiring.py | 9282149c | 9282149c | +#567 lines only |

The probe's body is byte-identical to the packet's: packet P:153-743 == HEAD probe :166-756 (offset +13); only the
docstring note differs.  The committed note is a rewrite (22 -> 35 lines).  One later commit matters here: `d42c76a8`
(ip30abortkill's closure records) measured clause (b) and did not touch the probe.

## 1. Table

| # | Argon item (gemini_web.out line) | disposition | reason |
|---|---|---|---|
| 1 | FLAG `acc 30 rd' left out of the stall disclosure (:4; Q2 :36; Q4 A2 :63) | OVERTAKEN | gate_arm.sh:1527 names it |
| 2 | FLAG six count rows read a stall green (:5; Q2 :43; Q4 A2) | OVERTAKEN | gate_arm.sh:1530-1534 names all six; filed `ip30stallgreen` |
| 3 | FLAG "13 rows" vs 10/33 conflated (:6; Q1 :25; Q3 D2) | OVERTAKEN | probe:36-38 "reds 23 of 33 rows, scoring 10/33" |
| 4 | FLAG first CATCH / clause (b) left unqualified (:7; Q1 :25; Q4 G4 :65) | OVERTAKEN | probe:39-42 qualifies it (clause (a) only) |
| 5 | same sentence, read at HEAD | WRONG RECORD (W1) | stale since d42c76a8: clause (b) measured 14/33 |
| 6 | FLAG note says "later sections were updated" and "five statements" (:8; Q1 :20; Q4 A1) | OVERTAKEN | both sentences gone from probe:15-18 |
| 7 | FLAG P:39, P:109, P:130, P:645-651 also stale (:8) | OVERTAKEN | note bullets 5, 1, 6, 3 (probe:39, :20-21, :43-44, :25-35) |
| 8 | FLAG P:466 "ALL FIVE ISR announces" (:8) | WRONG RECORD (W3) | probe:479; three since F13 |
| 9 | FLAG P:521 "all five ISR sites" (:8) | WRONG RECORD (W4) | probe:534; three since F13 |
| 10 | FLAG P:620 "both decline, both announce" (:8) | WRONG RECORD (W5) | probe:633; read arms decline silently |
| 11 | FLAG P:634 "(the announce still fires)" (:8) | WRONG RECORD (W6) | probe:647; no read-arm announce exists |
| 12 | FLAG CHANGELOG "later sections record the finished 33-row closure" false (:8; Q1 :29) | REFUTED | CHANGELOG.md:237-238 at HEAD is true: probe:650-731 records it |
| 13 | FLAG ten-cell count is the 32-row one (:9; Q1 :23; Q3 D2) | OVERTAKEN | probe:25-35 now historical, `xbit rev2' named as added after |
| 14 | FLAG note omits M9's vanished cell (:9; Q1 :24) | REFUTED | bullets 1-2 already retire both read-arm latch cells |
| 15 | FLAG 568 s vs 567 s; LEGS.out md5s stale (:10; Q1 :17; Q3 D2 (4); Q4.2 :60) | OVERTAKEN | gate_arm.sh:1521; legs/RESCORE.out; CHANGELOG.md:257-259 |
| 16 | FLAG selftest wording; no RESULT=32/33 case (:11; Q2 :45) | REFUTED | words match score_selftest.sh; `rows correct' reds in n9 and the prefix leg |
| 17 | UNSETTLED pin comment / section U (Q1 :27) | REFUTED (settled) | re-derived at 8faf4a16: PINNED=35, PASS, 13 of 35; 0 of 1224 gate comment lines name the stem |
| 18 | UNSETTLED bug-file "Still owed" line; 8 EXEMPT entries (Q1 :28) | REFUTED (settled) | OUTSTANDING_BUGS.md:21644 annotated; 8 entries, dates match |
| 19 | UNSETTLED kill-table 4/5 scores (Q1 :24) | REFUTED (settled) | every figure in note bullet 3 matches the .raw logs |
| 20 | UNSETTLED/"harder": single-site abort() mutants were measured in #531 (Q3 :51; Q4 G4 :65) | REFUTED | a grok READING ("I did not re-run the emulator"); no ip30 driver re-inserts abort() |
| 21 | Q4.1 reset and rebuild /tmp/gx566 before gate 14 (:59) | OVERTAKEN | legs/RESTORE.out both parts; gate14/RUN.txt sentinel absent, md5 25ac428c |
| 22 | Q4.3 ledger `state_note' rows (:61) | OVERTAKEN | 8faf4a16's ledger.json carries both [#566] notes |
| 23 | sibling: CONTRACT "Every CATCH ... MEASURED kill in killtable{,2}" overstates two more CATCHes | WRONG RECORD (W2) | no table deletes the 0x10020 store; M11's kill is in killtable3 |
| 24 | sibling: `latch 1x' note "TWO declined ISR accesses" | WRONG RECORD (W7) | probe:619; they are two WRITES the arms keep (probe:615-616) |
| 25 | sibling: note "the CATCHES list ... the 27-row instrument's" | WRONG RECORD (W8) | probe:16-17 (+CHANGELOG.md:237); its M11 line is row 28 |
| 26 | sibling: "a mutant that scored 12/12" over the PROBE ATTACK rows | WRONG RECORD (W9) | probe:488; a prediction written as a score |
| 27 | ledger cites an untracked PROBEATTACK file as a durable copy | FILE | regress/artifacts/ip30abortkill/PROBEATTACK_grok_20260917.txt is `??` at HEAD |
| 28 | five non-ip30 drivers filed under #531's manifest block | FILE | opus_killtable_20260917/mutate3,4,500,500b,524g.py |

Items Argon raised that are not separate rows: Q3 D1 "keep open holds" (matches HEAD: the row stayed open in #566 and is
`held' since d42c76a8); Q3 D2 "broken as written" = rows 3, 6, 13, 15; Q4 "A1 DEFECTIVE" = rows 3, 6, 13; "A2 WRONG" =
rows 1-2; "G4 INCOMPLETE" = rows 4-5, 20.  Argon's HOLDS items need no disposition.

## 2. Per-flag detail

### Row 1 -- FLAG 1, `acc 30 rd' -- OVERTAKEN
Argon: B:70-75 names only the read sessions and `tick 49'; P:360-361 `acc 30 rd' also reads a stall green alone.
HEAD regress/gate_arm.sh:1526-1529:
> `A stall BEFORE a session's access leaves its `alive' and `no' rows green and its `yes' announce row red.  `acc 30 rd' and `tick 49' carry no `yes' row, and neither do the `kill 20 rd' and `kill 28 rd' sessions, so those read a stall green outright -- the two kill sessions even on a build that would have aborted; the write-arm and bit-50 tick sessions carry one, and red.`

Checked session by session against probe:352-731: the sessions with only `alive'/`no' rows are exactly `acc 30 rd',
`kill 20 rd'(+txt), `kill 28 rd'(+txt) and `tick 49'; every value row reads ABSENT or a wrong earlier print and reds.
The same list is in CHANGELOG.md:225-226 and the `ip30stallgreen' state note.

### Row 2 -- FLAG 2, the six count rows -- OVERTAKEN
HEAD regress/gate_arm.sh:1530-1534:
> `A count row that wants ONE announce (`latch 1x', `latch 28wr', `latch 30wr', `latch tick', `xbit rev', `xbit rev2') reads green whenever exactly one announce was captured, so a stall between its first and second access hides the latch defeat or clobber it exists to catch: on V2_assigntick only `xbit rev2' reds, so that session stalling with one announce captured, every other session passing, leaves all 41 checks green.  Filed as ip30stallgreen.`

"On V2_assigntick only `xbit rev2' reds" is measured: killtable5_20260918/V2_assigntick.raw 32/33, the only FAIL row
`xbit rev2 got=2 want=1'.  `xbit isr'/`xbit tick' are rightly absent from the list: a stall there leaves the ISR count 0.
The false green itself is DERIVED, not measured (`ip30stallgreen' witness: none).  The measurement that would settle it,
for that row and not for this round: in a scratch clone built with V2_assigntick, run the shipped probe with a stall
injected into session 26 alone (`xbit rev2'; probe:723) -- e.g. a PMAX wrapper that, on its 26th invocation, lets the
first ISR store's announce reach the pty and then SIGSTOPs the emulator until the probe's poll kills it -- and score the
log with the block text extracted from gate_arm.sh.  41/41 green measures the false pass; any red refutes it.

### Row 3 -- FLAG 3, 13 rows vs 10/33 -- OVERTAKEN
HEAD probe:36-38: `the pre-fix red is no longer `13 rows': on this instrument the pre-fix build reds 23 of 33 rows,
scoring 10/33 (#566's prefix leg, clause (a): .../legs/probe_prefix.log)`.  Counted in that log: 10 `ok', 23 `FAIL',
`IP30ABORT_RESULT=10/33'.  CHANGELOG.md:254-255 says "10/33, 23 rows and 26 checks red".  Argon's side note (the two read-arm
`txt' rows are green pre-fix only because their sessions die before any new-text announce) is true and no record says
otherwise.

### Rows 4-5 -- FLAG 4 / G4, clause (b) -- OVERTAKEN at #566, WRONG RECORD at HEAD (W1)
HEAD probe:39-42 (the #566 note, bullet 5):
> `* `Every CATCH below has a MEASURED kill in killtable{,2}' overstates the first CATCH: reinstating the four abort() calls rests on the PRE-FIX build (clause (a): the 21-row PREFIX_21row_20260917.out and the 33-row leg above); no table here holds abort() re-inserted into the FIXED file (clause (b));`

That answered Argon's flag in `8faf4a16` (2026-10-18 15:03:25).  The same afternoon `d42c76a8`'s leg (LEGB.out
15:21:19-15:26:46) measured exactly what it says is missing: `close_20261018/CLAUSE_B.txt` -- "the removed defect re-inserted VERBATIM at every fixed site of the FIXED
file ... IP30ABORT_RESULT=14/33, CONTROL=OK" (LEGB.out: `probe b: rc=0 272s IP30ABORT_RESULT=14/33', 22 of 41 checks red).
HEAD's ledger, OUTSTANDING_BUGS.md:21621 and CHANGELOG.md:160-166 all say clause (b) is measured; the probe header, the
file the gate comment sends readers to (gate_arm.sh:1517-1518), still says it is not.  An absence record, time-indexed,
that went false one commit after it was written.
**W1, minimal replacement** (in place, if the #566 note is edited): `no table here holds abort() re-inserted into the
FIXED file (clause (b));` -> `no kill table holds abort() re-inserted into the FIXED file (clause (b)); one leg has since
measured it, 14/33 (regress/artifacts/ip30abortkill/close_20261018/CLAUSE_B.txt);`.  edits.diff carries it as a dated
addendum instead (section 4).

### Rows 6-7 -- FLAG 5, the note's own sentences -- OVERTAKEN
Packet P:16-17 said "The file's later sections were updated and this one was not" and "five statements below are no
longer true".  HEAD probe:15-18:
> `[#566, 2026-10-18 -- a records correction; the text below it is kept as it was written.] The CATCHES list, the fourteen-cell paragraph and "THE CLOSURE IS OWED" below are the 27-row instrument's of 2026-09-18; the DOES NOT CATCH list was updated later and is current.  The probe that ships has 33 rows, and these statements below are no longer true of it:`

No count, no claim about the later sections.  The other stale lines Argon listed inside the CONTRACT are covered:
P:109 (HEAD :122 "All FIVE ISR sites") by bullet 1, probe:20-21 "THREE ISR sites print the shared string, not five (THE
ATTRIBUTION RULE)"; P:130 (HEAD :143 `kill 30 rd') by bullet 6, probe:43-44; P:39 (HEAD :52) by bullet 5 for the first
CATCH (the rest is W2); P:645-651 (HEAD :658-664, the 32-row closure summary) by bullet 3, probe:25-35, and in place by the
file's own probe:705-706 "V2_assigntick SCORED 32/32 AGAINST A CLOSURE THAT CLAIMED BOTH COLLISION DIRECTIONS".

### Rows 8-11 -- FLAG 5, P:466 / P:521 / P:620 / P:634 -- WRONG RECORD (W3-W6)
None of the four is named by the note, and each is false of the probe that ships.  Since the F13 silent decline the
read arms of 0x10020 and 0x10028 do not announce (HEAD src/devices/dev_sgi_ip30.c:210-243 and :258-287 -- no `fatal');
three ISR sites announce, the three writes (:202-208, :250-256, :291-305).

- **W3** probe:479 `#  ALL FIVE ISR announces are BYTE-IDENTICAL, so the row read `yes' from the 0x10020 arm and` ->
  minimal: `ALL FIVE ISR announces (THREE since F13) are BYTE-IDENTICAL`.
- **W4** probe:534 `#  can attribute an announce to one arm -- all five ISR sites print one identical string` ->
  minimal: `all THREE ISR sites (five before F13) print one identical string`.
- **W5** probe:633 `#  cause. ***  The two READ arms are structurally identical -- both decline, both announce,` ->
  minimal: `both decline (silently, since F13), both leave odata 0`.
- **W6** probe:647, inside the `isr 28 rd val' row note (a string literal): `` `kill 28 rd txt' stays GREEN under that
  mutant (the announce still fires), `` -> minimal: `(the arm still declines silently)`.  The verdict "stays GREEN" is
  still true -- `kill 28 rd txt' wants `no' (probe:467) and M11 adds no announce; only the reason is false.  The note is
  truncated at 70 characters when printed, so this text never reaches a log.

These are the siblings of bullet 1's correction: the same "five ISR sites" claim corrected at THE ATTRIBUTION RULE and
left standing twice more in the same file (the carrier's grep-for-siblings rule).  W3-W5 are `#' comments; W6 is a string
literal, so editing it in place changes the AST.  edits.diff names all four in the docstring instead, which keeps the
AST identical and keeps the note's own "the text below it is kept as it was written" true.

### Row 12 -- FLAG 5, the CHANGELOG's "later sections record the closure" -- REFUTED
Packet B:329-330 said "the file's own later sections record the finished 33-row closure".  HEAD CHANGELOG.md:237-238:
"while the file's own later sections record the 33-row closure".  True: THE LATCH-AXIS CLASS CLOSURE and its rows
(probe:650-703) plus the `xbit rev2' section (probe:705-731) record all 33 rows and the escape that added the 33rd.  The sentence does
not claim the later sections are free of stale text, so W3-W6 do not make it false.

### Row 13 -- FLAG 6, the ten cells -- OVERTAKEN
HEAD probe:25-35 now reads as history: "THE LATCH-AXIS CLASS CLOSURE, further down, enumerated TEN cells ... six rowed
before it ... four rowed there ... In kill table 4 (32 rows) ... each killed its mutant; V2_assigntick ... still escaped
that table at 32/32, so `xbit rev2' (ISR -> TICK -> ISR) was added; kill table 5 measured base 33/33, V1_assign20wr 32/33
and V2_assigntick 32/33".  No current cell count is claimed, so Argon's "11 cells across 12 rows" contradicts nothing.

### Row 14 -- FLAG 6, M9's cell -- REFUTED
Argon: bullet 4 names MF's vanished cell (0x10028-READ) and not M9's (0x10020-READ).  Leaving it out makes nothing false.
Bullet 1 (probe:19-22) removes both read-arm announce sites, so both read-arm latch cells.  Bullet 2 (probe:23-24)
re-aims `latch 1x' onto the write arms, which retires CATCHES:65-66's "AT THE 0x10020-READ SITE ONLY (latch 1x / M9)".
Its post-F13 kill is killtable4 V3_nolatch20wr 31/32 [`latch 1x'].

### Row 15 -- FLAG 7, 568 s / 567 s and the md5s -- OVERTAKEN
HEAD regress/gate_arm.sh:1521: `RUN TIME, about 9.5 minutes -- 568 s on build/gxemul (#550), 567 s on a HEAD rebuild
(#566)`.  567 s is legs/LEGS.out `probe base: rc=0 567s`.  568 s is #550's keep_p1_logs.out:8 "ip30 wall from file
mtimes: 568 s", and its build/gxemul attribution is exemptredate_20260925/opus5_p1.md:5,:35 ("a WSL /tmp/opus550 copy of
`build/gxemul`").  The md5s: legs/RESCORE.out re-scores all four leg logs with the shipped scoring text (`gate_arm.sh md5
bf7b6af6', `scoring text ... md5 21d7b874', "the legs ran 5bf04f2d, before #566's docstring note"), and CHANGELOG.md:257-259
says so.  Verified: `git show HEAD:regress/gate_arm.sh | md5sum` = bf7b6af6..., HEAD probe = 7fbf52ab..., the parent's
probe = 5bf04f2d... (the md5 LEGS.out records); probe AST with the docstring excluded is identical parent -> commit.
LEGS.out itself correctly records what ran.

### Row 16 -- FLAG 8, the selftest -- REFUTED
score_selftest.sh's own comments: n3 "one row replaced by a duplicate of another (counts unchanged)"; n8 "RESULT says 33/33
but a row line says FAIL (contradiction)".  CHANGELOG.md:262-263 ("a row turned FAIL, lost, duplicated or renamed ...
RESULT doubled, contradicted or shrunk") describes those cases accurately.  n1 and n8 do share one shape (a row flipped to
FAIL with RESULT left at 33/33) -- 14 distinct shapes in 15 cases.  But a 33-ok log with `RESULT=32/33' cannot pass:
gate_arm.sh:1579 is an exact compare (`check "ip30_abort rows correct" "${ip30res%/*}" "33"'), and it is measured red in n9
(`rows correct got=32') and in the prefix leg (got=10).  SELFTEST.out ran the shipped scoring text: md5 21d7b874 is the
md5 of HEAD's block.

### Row 17 -- UNSETTLED: the pin comment and section U -- settled, the record holds
HEAD tools/precommit_check.sh:350-355: "The checker reads only comment lines (`#', `*' or `//') that contain the stem, and
only a docstring at regress/<stem>_probe.py or regress/<stem>.py; no comment line names ip30_abort and the probe lives under
artifacts/, so for this pin it checks no prose -- only the pin is counted."  check_score_claims.py:117-123 (comment lines
`#', `*', `//') and :172-193 (the pinning gate's own comment lines; docstrings at regress/<stem>_probe.py or <stem>.py)
match.  Of gate_arm.sh's 1224 comment lines, 0 contain `ip30_abort'; neither regress/ip30_abort_probe.py nor
regress/ip30_abort.py exists.  Section U re-derived on 8faf4a16's committed files (`rederive_U_8faf4a16.out' here):
`SCORE_CLAIMS_PINNED=35', `SCORE_CLAIMS_PASS 35 gate comment set(s) checked; 13 of 35 stems also have a probe docstring
checked' -- the CHANGELOG's figure (CHANGELOG.md:269).  (At HEAD: 36, 14 of 36, after #567.)  One untidiness, not counted:
the U figure has no receipt under gatewire_20261018/; R_CONTROLS.out, which the same bullet cites, carries only section R.
The figure is a deterministic function of committed files, and it reproduces.

### Row 18 -- UNSETTLED: the bug-file note -- settled, holds
OUTSTANDING_BUGS.md:21644: `**Still owed before close: panel pass 2 on the real diff.**  *[#566, 2026-10-18: discharged --
see the dated note at the top of this entry.]*`.  check_probe_wiring.py's EXEMPT table holds 8 entries, at 8faf4a16 and
at HEAD (:3198-3247): alpha_tbi 10-22, lca_badval 10-23, lca_widewrite 10-26, lca_isalane 10-27, wdc_altoffset 11-05,
wdc_altoffset_4bit 11-12, wdc_altoffset_sig 11-19, wdc_addtoinbuf 12-03.  That matches OUTSTANDING_BUGS.md:24959-24960
and R_CONTROLS.out "8 dated-exempt".

### Row 19 -- UNSETTLED: kill tables 4 and 5 -- settled, every figure holds
From the committed .raw logs: table 4 (32 rows) V1_assign20wr 31/32 [xbit rev]; V2_assigntick 32/32 (escape);
V3_nolatch20wr 31/32 [latch 1x]; V4 31/32 [latch 28wr]; V5 31/32 [latch 30wr]; V6_nolatchtick 30/32 [latch tick, xbit rev];
V7_nocounter 32/32 (escape); V8_len4 28/32 -- the MIS-BUILT first form that DOES NOT CATCH (probe:110-114) describes, four
tick rows.  Table 5: base 33/33; V1 32/33 [xbit rev]; V2 32/33 [xbit rev2]; V8_len4 33/33 (escape).  Note bullet 3 and
its closing sentence (probe:45-46) state exactly these.

### Row 20 -- "harder on the adopted position": single-site abort() mutants -- REFUTED
Argon inferred from P:479-480 and P:512-513 (HEAD :492-493, :525-526) that #531 measured M_tick_abort, M_wf20_abort_wr and
M_wf28_abort_wr.  It did not.  Of the eight drivers in opus_killtable_20260917/, mutate.py, mutate2.py and mutate5.py
target dev_sgi_ip30.c, and none re-inserts `abort()' (M1-M9: silent/nolatch/sharedbit/noclr28/tickbit49/clr28_isr).  The
other five are not ip30 drivers at all (row 28).  The three names come from grok's PROBE ATTACK, a reading: its own line 3
says "I did not re-run the emulator", and its table gives "MISS, 12/12" as predictions.  The ledger's ip30abortkill
entry by opus5 (2026-09-17) closes them "by construction" and says "The new rows are CONSTRUCTED, not MEASURED".  So
"no kill table holds such a mutant" was true when B:297 / B:359 said it.  Since then the closure-records leg (row 5) has
measured the all-sites form, but not the single-site ones.

### Row 21 -- Q4.1, /tmp/gx566 before the gate run -- OVERTAKEN
legs/RESTORE.out: `part 1: dev_sgi_ip30.c == HEAD' (and the five other sources), `part 2: binary newer than every restored
source (11:39:50)', `sentinel cleared', `gxemul md5 25ac428c...'.  gate14/RUN.txt: `binary /tmp/gx566/gxemul md5
25ac428c...', `clone sentinel absent', `gate_arm.sh md5 bf7b6af6... probe md5 7fbf52ab...' (both = HEAD), `GATE14_PASS'
(1225 checks; the block's 41 lines all `ok').

### Row 22 -- Q4.3, the ledger rows -- OVERTAKEN
8faf4a16:tools/pipeline/ledger.json: `wiringcliff' state_note opens "[2026-10-18, #566] ... wired into gate 14 ... and its
2026-10-30 exemption deleted"; `ip30abortkill' opens "[2026-10-18, #566] the detector runs in gate 14 (41 checks) ..." with
the 33-row pair; `ip30stallgreen' and `fableheldform' filed.  CHANGELOG.md:244-246 lists them.

## 3. Siblings found while settling the flags (not Argon's)

- **W2 -- the CONTRACT header overstates two more CATCHes, and the #566 note names only one.**  HEAD probe:51-52 `Every
  CATCH below has a MEASURED kill in regress/artifacts/ip30abortkill/killtable{,2}_20260917/.`  Against every committed
  kill table (killtable_ 1-5, opusF2_, opus_killtable_ logs): (i) the third CATCH, probe:58 `deleting either surviving
  store (0x10020, 0x10028) (isr keep, isr clr / M1)` -- M1_del28store deletes only the 0x10028 store and reds only `isr
  clr' (20/21, 26/27); no table deletes the 0x10020 store, and no kill-table mutant reds `isr keep' at all (it reds only
  as `died' on the pre-fix and clause-(b) builds); (ii) the sixth CATCH, probe:61-62 `isr 28 rd val / M11` -- M11 is
  killed in killtable3_20260918 (M11_mirror28.raw 27/28), not in killtable{,2}_20260917.  Bullet 5 (probe:39) audited
  that very sentence and said it "overstates the first CATCH".  Minimal: `overstates the first CATCH` -> `overstates
  three CATCHes -- the first (...), the third's 0x10020 half (no table deletes that store) and the sixth's M11 half
  (killed in killtable3_20260918)`.
- **W7 -- probe:619, the `latch 1x' row note**: `"TWO declined ISR accesses, ONE announce -- that is what the unqualified
  `(once)' marker "`.  Since the F13 re-aim the session is `guest_store(A_SETISR, 0x1) + guest_store(A_CLRISR, 0x1)'
  (probe:617), and probe:615-616 calls those arms "member-4 ACCEPT arms that keep their store AND announce".  Its first 70
  characters print in every gate-14 log (gate14/ip30_abort.log: `latch 1x ... ok  TWO declined ISR accesses, ONE announce
  -- that is what the unqualifie').  Minimal: `TWO declined ISR accesses` -> `TWO ISR write accesses`.  It is a string
  literal: the in-place edit changes the AST and the printed line.
- **W8 -- probe:16-17**: `The CATCHES list, the fourteen-cell paragraph and "THE CLOSURE IS OWED" below are the 27-row
  instrument's of 2026-09-18`.  The CATCHES list names `isr 28 rd val / M11` (probe:61-62), the 28th row, added at the F2
  sibling-parity repair: killtable2's base is 27 rows without it, killtable3's base is 28/28 with it, and
  opusF2_20260918/probe.frozen.py -- the 27-row copy -- has a CATCHES list without the M11 line or either qualifier.  The
  same words are in CHANGELOG.md:237 ("were the 27-row instrument's").  Minimal: `the 27-row instrument's` -> `the 27-
  and 28-row instruments' (the CATCHES' M11 line is row 28)`.
- **W9 -- probe:487-488**: `... rows the PROBE ATTACK proved missing` (a dashed rule) / `#  Every one of these closes a
  mutant that scored 12/12 against the probe without it.`  The 12/12s are grok's predictions (row 20); nothing ran these mutants
  against the 12-row probe -- the opus tables of 2026-09-17 ran 18- and 19-row probes.  This is the sentence Argon read as
  a measurement.  Minimal: `that scored 12/12` -> `that the attack (a reading; no emulator run) predicted at 12/12`.

## 4. The proposed edit (edits.diff, NOT applied)

One dated addendum inside the #566 note (after probe:48 "(ip30stallgreen).") naming W1-W9's corrections, and one
bracketed line in the #566 CHANGELOG block for W8's echo.  Why the addendum form and not nine in-place edits: W6 and W7
are string literals (an in-place edit changes the probe's AST and, for W7, its printed output), and an in-place edit of
the comments would make the note's own "the text below it is kept as it was written" false.  The addendum is
docstring-only.  Dry-run on copies of HEAD's blobs (work/applytest/): `git apply --check` passes; the AST with the
docstring excluded is identical to HEAD's; the docstring grows by 20 lines; every added probe line is ASCII, at most 93
columns, with no backslash or quote run that could close the docstring.  On this machine `git apply' outside a repository wrote CRLF; HEAD's blobs are LF -- apply
inside the repo.  The probe's md5 changes from 7fbf52ab; RUN.txt, RESCORE.out and LEGB.out cite 7fbf52ab as what ran,
which stays true.  No re-measurement is owed with the AST unchanged.  A records commit applying it owes its own CHANGELOG
block.

## 5. To file

- **F-1 (records, durable path)**: ledger `ip30abortkill' entries cite
  `regress/artifacts/ip30abortkill/PROBEATTACK_grok_20260917.txt' three times -- entry [44] "Durable copy MADE ... 13,519 b,
  cmp-verified".  The file is untracked at HEAD: `git status' shows `??', 13,519 bytes, md5 d6f667ed; it is committed only
  inside snapshot c0e57d54, on no branch.  It is the only evidence that row 20's three mutants were a reading.
  Consequence: a fresh clone cannot verify entry [15]'s "12/12" table, nor the addendum's W9 line ("that attack ran
  no emulator").  Commit the file before or with edits.diff, or re-point the citations.
- **F-2 (records, misfiled)**: tools/pipeline/check_probe_wiring.py:686-701, under `# -- #531 ip30abortkill', describes
  eight opus_killtable_20260917 drivers as ip30 "kill-table driver"s.  Five are not: mutate3.py and mutate4.py edit
  /tmp/gxo498/.../dev_sgi_re.c (#498), mutate500.py and mutate500b.py edit dev_sgi_re.c in /tmp/gxopus500 (#500;
  "the 0x500 arm"), and mutate524g.py edits cpu_arm_instr.c (#524).  Consequence: the block's "ONE detector and
  twenty-two tools" counts them, and an audit of #531's tables -- the one Argon's Q3 prescribed -- reads them as ip30
  evidence.  Move them, or relabel them.

## 6. Not counted

- Kill-row notes that describe the pre-#531 code in the present tense: probe:448 `case 0x10020 has NO writeflag test`
  (printed), :452 `same missing writeflag test`, :473 `case 0x10030's WRITE arm aborts`, and the constant comments at
  :195-197 (`PREDICTED KILL, and no writeflag test`).  These read as the defect each kill row witnesses, which is the
  probe's stated polarity (probe:157-159), so I do not count them.  The addendum can name them if the round wants every
  pre-#531 present tense qualified -- the same logic as note bullet 6.
- src/devices/dev_sgi_ip30.c:50-52 ("SIX announce paths ... IP30_W_ISR covers FIVE"), :216-217 and :264-265 ("All five ISR
  sites print"): the same stale counts in product comments.  Already carried as #561's held places 7-10 by `heldrecedits'
  (CHANGELOG.md:178-179).

## Evidence produced here (session scratchpad, argonlate/ip30wirep2/)
`head/` -- HEAD copies of the files quoted; `rederive_U_8faf4a16.out`, `rederive_U_5dbc000e.out` -- check_score_claims.py
run on exported committed copies; `work/addendum.txt`, `work/make_diff.py`, `work/check_addendum.py`, `work/applied/`,
`work/applytest/` -- the edit and its dry-run; `edits.diff`.
