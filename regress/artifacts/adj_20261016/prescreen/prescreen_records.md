# Prescreen -- records and harness group (the 2026-10-13 agy pack, re-read by grok, grok-reconcile and Gemini Argon)

PRESCREEN_RECORDS_20261016.  Prepared 2026-10-16 for the adj_20261016 adjudicators.  It sorts the seats' findings into
a short table per job.  It does not re-grade anything already ruled, and agreement between seats counts for nothing.

**Mode.**  READ-ONLY: nothing was built, no test, probe, gate or project tool was run.  Every check is a read: `git
show`, grep, `sed -n`, `ls`/`find`/`stat`, a hash, or an in-memory `python -I` read.  One fork also ran two read-only
system queries, `wsl -d Gentoo -- id -u` and `schtasks /query`.  This is the only file written.  (Disclosure: the
prescreen agent once wrote a stray read-copy of the ledger to `/tmp` and deleted it within the minute, confirmed
gone.)  **Tree:** `GXEMUL-SEC` HEAD `e483d931` (2026-10-09 20:53).  CK's "NOTHING COMMITTED SINCE 10-13" line says nothing
has been committed since; it was :18 when read at 11:26.  CK is being rewritten by another session, so CK is cited here
by anchor text, with the line number seen at 11:26.  Committed text was read with `git show e483d931:<path>`.  Where the working tree differs, that is noted: it
carries uncommitted edits to `tools/pipeline/ledger.json`, `tools/panel.sh`, `tools/CLAUDE.md`, `tools/BRIEF_TEMPLATE.md`
and others.

**Timeline (it decides DISPOSED vs LIVE).**  The briefs were written 2026-10-13 (20:3x-21:xx).  Then came:
- HARVEST.md's 22:0x-23:1x sections;
- the records adjudication: v1 at 22:1x, and the v2 reconciliation (from its line 164) at 22:4x;
- Astra v1 REJECT at 22:22, and Astra v2 REJECT-narrowly at 23:03.

After that:
- grok answered 2026-10-14 22:24 -> 10-15 01:31;
- grok's reconcile runs (agy vs grok) ran 10-15 02:57-04:28;
- Argon answered 10-14 22:33 -> 10-16 03:42.

Argon is packet-fed: it saw only its `argon_bundle_*`.  Neither grok nor Argon was given the adjudication, so a
finding that repeats it is DISPOSED.  grok **auto-compacted mid-answer** on five jobs: dash_okclass, carrier_citations,
pass2ledger_schema, nullmedium_census and adj_pcc2_ruling.  The tell is a 67-byte `grok_<id>.err` reading
`Auto-compacting conversation (8x% full)...`.  Read those answers' early facts with that in mind.

**Seats.**
- `grok` = grok-4.7 xhigh, its first answer (`grok_<id>.txt`).
- `grok-rec` = grok's reconcile run (`grok_reconcile_<id>.txt`).
- `Argon` = Gemini 4 Argon (`_scratchpad/gweb/jobs_20261014_argonpack6/<id>/gemini_web.out`).

Argon's TRANSPORT flags (a file omitted or truncated in its bundle) are facts about the packet: they are counted per
job and not graded.  agy's own flags are not listed: they were already harvested.

**Categories.**
- DISPOSED: handled by HV, ADJ v1/v2 or AST1/AST2 (cited).  Three qualifiers mark a stretch of that definition, so
  an adjudicator can re-label:
  - "(prior filing)" / "(prior record)": the finding is already filed, or already ruled, in a committed record that
    predates this pack.
  - "(immaterial)": true, but nothing relied on carries the error.  That is, a seat answer, or an artifact line no
    record cites.
- LIVE: applies to a spec, record or tool as it now stands, and is not already ruled.  "(spec)" marks a confirmed
  defect whose fix spec has never been adjudicated (set 4: harness_five, agentrefusal_spec, probewiring_three).
  "(owner D2)" and "(owner ROUTE PARITY)" feed the open owner rule questions.  "(ruling)" means a ruling is asked for,
  not only a records fix.
- REFUTED: committed text or a receipt contradicts it.  "(as a defect)" means the statement is true but is dated
  history, which the record already marks, so it is not a defect.  "(the doubt)" means a seat said it could not verify
  something and the files settle it.
- CANNOT SETTLE: the table names the one read or run that would settle it.

Evidence tags: **READ** = opened, grepped or measured here; **REASONED** = inferred.

**Abbreviations.**
- HV = `regress/artifacts/agypack_20261013/HARVEST.md`.
- ADJ = `regress/artifacts/recordfix_20261013/adj_20261013/fable5_records_adjudication.md` (v1 = :1-161, v2 = :164-276).
- AST1 = `.../adj_20261013/astra/codex_recadj.txt`.
- AST2 = `.../adj_20261013/astra_v2/codex_recadjv2.txt`.
- PL = the production launcher `_scratchpad/codexpack_20260928/cxlaunch_pack.run-rule7n4-1009.sh`.  It classifies a
  codex run only when rc != 0 or stdout is empty (:61-74).
- CK = `_scratchpad/CHECKPOINT.md`.

**Jobs (16):** seatverdict_refusal, cxlaunch_quota, dash_okclass, stagetokens_controls, edits560, carrier_citations,
carrier_counts, carrier_d2_texts, pass2ledger_schema, nullmediumlegs_wiring, probewiring_three, harness_five,
agentrefusal_spec, adj_8n_regress, adj_pcc2_ruling, nullmedium_census.  nullmedium_census has grok only: Argon dropped
it by design (`ARGON_SKIPPED.txt`: the bundle carried 3 of the paths the census needs).

**The seat answers, as each seat tallied itself (sizes in bytes; these are not dispositions):**

| job | grok (`VERDICT: ANSWERED (n flags)`) | grok-rec (`agreed / disagreements / wrong-in-all`) | Argon (`ATTACKS / BROKEN / HOLDS / UNSETTLED`) |
|---|---|---|---|
| seatverdict_refusal | 12,229 b, 9 | 10,476 b, 9 / 6 / 0 | 20,316 b, 6 / 1 / 3 / 2 |
| cxlaunch_quota | 12,976 b, 4 | 8,591 b, 11 / 4 / 0 | 19,483 b, 5 / 2 / 2 / 1 |
| dash_okclass | 13,975 b, 7 (compacted) | 9,106 b, 16 / 5 / 0 | 15,958 b, 6 / 1 / 3 / 2 |
| stagetokens_controls | 10,186 b, 3 | 10,067 b, 12 / 7 / 0 | 17,083 b, 11 / 2 / 5 / 4 |
| edits560 | 19,087 b, 3 | 10,465 b, 40 / 3 / 0 | 26,995 b, 34 / 0 / 5 / 29 |
| carrier_citations | 23,548 b, 16 (compacted) | -- | 27,462 b, 36 / 0 / 1 / 35 |
| carrier_counts | 12,900 b, 14 | -- | 29,531 b, 8 / 3 / 1 / 4 |
| carrier_d2_texts | 16,709 b, 12 | 10,406 b, 8 / 6 / 0 | 33,536 b, 15 / 11 / 3 / 1 |
| pass2ledger_schema | 16,019 b, 22 (compacted) | -- | 46,504 b, 15 / 14 / 0 / 1 |
| nullmediumlegs_wiring | 14,923 b, 3 | -- | 23,264 b, 7 / 5 / 0 / 2 |
| probewiring_three | 21,877 b, 5 | -- | 33,264 b, 12 / 4 / 5 / 3 |
| harness_five | 27,996 b, 7 | -- | 31,620 b, 9 / 0 / 5 / 4 |
| agentrefusal_spec | 29,135 b, 8 | -- | 43,107 b, 15 / 8 / 3 / 4 |
| adj_8n_regress | 13,848 b, 5 | 15,895 b, 14 / 8 / 0 | 48,328 b, 21 / 4 / 11 / 6 |
| adj_pcc2_ruling | 14,232 b, 9 (compacted) | 12,345 b, 15 / 4 / 0 | 13,749 b, 22 / 5 / 10 / 7 |
| nullmedium_census | 23,289 b, 36 (compacted) | -- | skipped by design |

**Files read (common to all jobs):**
- HV, ADJ, AST1, AST2, PL, CK;
- `_scratchpad/gweb/HARVEST_ARGON.md`;
- `regress/artifacts/agypack_20261013/reconcile_briefs/`;
- at HEAD: `tools/cxlaunch.sh`, `tools/pipeline/seat_verdicts.py`, `tools/panel.sh` and `tools/pipeline/ledger.json` (grep).

Per job, the files read were the brief, grok, grok-rec where it exists, and Argon, plus every file named in that job's
evidence column.  **Work split:** the prescreen agent did seatverdict_refusal and the ledger check.  The other fifteen
jobs went to four read-only forks of it (same context, same rules).  The prescreen agent then re-opened the files
behind a SAMPLE of about 30 of the forks' LIVE and REFUTED items, covering every job.  Each one held.  Those evidence
cells say "(re-checked by the prescreen agent)".  Every other cell is the fork's own reading, tagged READ or REASONED
as the fork reported it.

## Ledger rows asked about (grep of `git show e483d931:tools/pipeline/ledger.json`, 62,523 lines)

- **`seatverdictrefusal` -- ABSENT.**  0 hits at HEAD, and 0 in the working-tree ledger.  The row is still owed:
  ADJ:72 says "PENDING filing per CHECKPOINT.md:73; not yet a ledger row", and CK lists it under "PENDING FILINGS
  (next records commit)" (:80 at 11:26).  The similar id `seatverdictsubs` (:56018) is a different row.
- **`wdczerolendatain` -- ABSENT.**  0 hits at HEAD and in the working tree.  It is owed: HV:109-111 names it a "NEW
  FILING for the commit unit", and CK's same "PENDING FILINGS" line lists it.
- Filed sibling rows, for reference: `wdc473floor` :62360, `cxlaunchdaybreak` :62410, `cxlaunchquotation` :62483,
  `stagetokenscontrols` :62492, `dashokclass` :62501.

## seatverdict_refusal

Files read:
- the brief, `grok_seatverdict_refusal.txt`, `grok_reconcile_seatverdict_refusal.txt` and Argon `gemini_web.out`;
- at HEAD: `seat_verdicts.py:355-540` and `panel.sh:335-340`, `:444-460`, `:517-522`, `:564-575`, `:688-712`;
- `tools/pipeline/codex_answer.py:40-100`;
- both refused `codex.txt`, the scratch copy and the artifact copy of each (hashed);
- `close_20261013/.../SEATS.txt` and `SEAT_VERDICTS.txt`;
- `adj_20261013/v3/classes_sv_head.tsv`;
- a read-only census of the 1,312 `codex*.txt` files under `_scratchpad/panel_*` and `regress/artifacts/`.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| SV1 | grok, grok-rec, Argon | the refusal was missed because `is_refused` is gated on `(not v)`, which runs after a whole-file `verdicts_of`; the 4000-char window did hold the ERROR lines | DISPOSED | ADJ:24 ("the window is not the defect, the `(not v)` gate is"); AST1:78; HEAD `seat_verdicts.py:365`, `:475-477`, `:530` READ | none: the v3 spec (ADJ:194-218) |
| SV2 | grok, grok-rec | `Trusted Access for Cyber` is absent from both files, so the second disjunct "matches nothing here" | DISPOSED (immaterial) | true of the two files.  READ census: 44 `codex*.txt` carry the phrase, and 34 of them carry it as the terminal `ERROR:` line, so the disjunct is live elsewhere.  v3 keeps it (ADJ:196-197) | none |
| SV3 | grok, grok-rec, Argon | a refusal substring anywhere in the file false-refuses answers that quote it (e.g. 211021 `:2760`, `:2792`, which are grep dumps) | DISPOSED | ADJ:36 (44 of 84 hits are quotes).  ADJ:190-191 measured agy's sentence-anywhere draft and the anchored-anywhere Part A.  AST2:88-89 corrects the counts: Part A has 6 wrong, and agy's 46 include some genuinely walled files.  The v3 terminal test is ADJ:200-219; AST2:44-46 supports it.  READ: `:2760` and `:2792` carry the phrase inside `path:NNN:` grep output | none |
| SV4 | grok, grok-rec, Argon | credit verdicts only after the last `codex` line.  That still credits `:3538` and `:5452`.  Argon's `_answer_body` also cuts at the next `exec` | DISPOSED | ADJ:37 (necessary and insufficient).  ADJ:192 WITHDREW last-turn scope and v3b, the exec-cut variant (row ADJ:179).  AST2:85-87 re-measured Part B alone: 17 class and 57 verdict-only changes, 12 rows / 9 healthy transcripts lost; v3b loses 10 rows / 7 transcripts.  Withdrawal supported | none |
| SV5 | grok | file 1's credited column may be `IMPLEMENT` or a SPLIT, because the MENU_RE count at `:2758` was not computed | REFUTED | grok-rec:20.  READ: `:2758` carries 2 `VERDICT` tokens, so MENU_RE != 1 and `:301` skips it.  ADJ:24 measured `SHIP WITH CHANGES answered`; AST1:75 | none |
| SV6 | grok | `SEATS.txt` says `333022b` and `SEAT_VERDICTS.txt` says `329895`; the two do not reconcile | REFUTED | READ: `io.open` text-mode `len(t)` = 329,895 (333,022 bytes, minus 2,937 CRLFs, minus 190 multibyte bytes).  The units differ: `panel.sh:449` uses `wc -c`; `seat_verdicts.py:361`/`:535` use `len(t)` | none |
| SV7 | grok, grok-rec | scratch and artifact `codex.txt` were never hashed against each other, and the directory listings differ | DISPOSED | HV:206-207.  READ: the md5s match pairwise (`1c06624c...` and `0c3e7b27...`).  The f2 copy lacks only the four `ollama_*.err` | none |
| SV8 | grok, Argon | neither measured file can serve as the answered control; a healthy fixture with its own final-turn verdict is needed | DISPOSED | ADJ:85 (N1); v2 controls N1/N2 at ADJ:221; AST1:96 | none |
| SV9 | grok, grok-rec | the selftest (`:855`) exercises `verdict_of` only, so no CASES row can show REFUSED | DISPOSED | ADJ:89 and :221; AST1:98 | none |
| SV10 | grok, grok-rec | HEAD `panel.sh` has no `flagged for possible` anchor (the brief's premise is false) | DISPOSED | ADJ:34 (BRIEF DEFECT); AST1:90 | none |
| SV11 | grok, grok-rec | `panel.sh`'s own seat check scores a refused codex as `answered`.  Causes: the whole-file token grep at `:568`, the quota-only tail at `:519`, and the tally at `:692`/`:708-709`, which counts `ok` for any non-wall file of 800 bytes or more.  The working-tree diff (+32/-9) adds no test | **LIVE** | READ: HEAD `panel.sh:568` and `:708-709`.  `flagged\|cybersecurity` has 0 hits at HEAD and 0 in the working tree.  `close_20261013/.../SEATS.txt:2` reads `333022b  answered` for a refusal.  v3 changes `seat_verdicts.py` only (ADJ:211) | File it as a `panel.sh` sibling of `seatverdictrefusal`: add the codex terminal-refusal test to `check()` and to the tally.  Or record that `SEATS.txt` is not authoritative for refusals.  A `panel.sh` edit waits on its review: `panel.sh` is on CK's "NEVER COMMIT" list (:84 at 11:26) |
| SV12 | grok-rec | agy's asiceventaddr control line is `VERDICT: CHANGES (8)` at `:5657`, not `SHIP WITH CHANGES (4)` (which is at `:4328`) | DISPOSED | ADJ:37 and :158; AST1:96 | none |
| SV13 | grok-rec | agy's far-from-EOF "refusals" (m88k `:2402`/`:8670`, ppcpass2 `:2518`) are quotations with no `^ERROR:` line | DISPOSED | ADJ:36; AST1:92 | none |
| SV14 | grok-rec | widening the test to every seat would be a separate ruling | DISPOSED | ADJ:178 (v3 is codex-only); N1 control ADJ:221 | none |
| SV15 | grok-rec, Argon | `:208` and `:4907` are the seat's own one-line progress notes; agy called them tool turns | DISPOSED (immaterial) | READ: `:208` and `:4907` are prose; `:209` and `:4908` are `exec`.  ADJ:35's "the text after it is tool output" is loose by one line, but no seat-authored verdict follows, so the conclusion holds | none |
| SV16 | grok-rec | grok's `VERDICT_RE` citation `:155` is a comment; the pattern is at `:149-150` | DISPOSED (immaterial) | a seat-answer citation; no record cites it | none |
| SV17 | Argon | `is_walled` (`:469`) carries the same `and not v` gate, so a codex wall that follows a quoted verdict could score answered | REFUTED (as an instance; latent only) | READ `:469`.  Census: 69 `codex.txt` end in a usage-limit `ERROR:` line, and all 69 score WALLED in `v3/classes_sv_head.tsv` (0 masked) | optional: a synthetic control, if the state ladder ever gets a selftest (ADJ:89) |
| SV18 | Argon | `GREP_OUTPUT_LINE` matches `.packet.md:683:` grep lines, so file 1's credited line lies past its bundle cut | DISPOSED | ADJ:24 (credited `:3538`); AST1:75 | none |

Transport flags (Argon, packet only, not graded): 4.  F6 `panel.sh` was omitted; F2 and F4 were cut at `:2366`; F5 was
cut at `:3612`.

LIVE (this job):
- **SV11:** `tools/panel.sh` `check()` and the seat tally report a content-filter-refused codex as `answered`.  The v3
  scorer fixes only `SEAT_VERDICTS.txt`.  The change would be a terminal-refusal test in `panel.sh`, or a recorded
  statement that `SEATS.txt` is not a refusal authority.

Prescreen note (derived here; no seat raised it as a defect): grok and grok-rec describe `tools/pipeline/codex_answer.py`.
Its `blocks()` (`:48-55`) and verdict test (`:98`) apply the same "prose from a `codex` header up to the next `exec`"
rule that ADJ:192 withdrew.  An in-memory replica (READ) finds 0 verdict blocks in 6 of the 9 healthy transcripts
ADJ:192 names.  It is a hand tool for `.err` streams (`:2`, `:24`), so no ruling is proposed here.

counts: DISPOSED 14 (3 of them immaterial) / LIVE 1 / REFUTED 3 / CANNOT SETTLE 0 (18 findings)

## cxlaunch_quota

Files read:
- the brief, grok, grok-rec; Argon `gemini_web.out`, its manifest, and the `argon_bundle_1.txt` headers (its
  `panel.sh` is HEAD's 795 lines);
- at HEAD: `tools/cxlaunch.sh`, `tools/panel.sh:444-530` and `:676-760`;
- `fablequeue8n_20261009/astra_confirm/` (ls, the stdout capture, wc);
- `adj_20261013/cxctl/{ctl_receipt_cxlaunch_v2.txt, wall.err, block_optA.sh}`;
- `exemptredate_20260925/final550/{astra550.launch.log, codex_astra550.err, codex_astra550.txt}`;
- OB:22494-22525 and :24700-24716; ledger :55892 and :62483-62489; PL;
- `SEATS.txt` and the seat files of panels 20260817_174701, 20260820_005715, 20260921_154943 and 20260925_144647,
  plus a census over every `SEATS.txt`.

OB = `git show e483d931:OUTSTANDING_BUGS.md`.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| CX1 | grok, grok-rec, Argon | `cxlaunch.sh:44` greps the `^ERROR:` lines plus the whole stdout.  `quota` matches "quotation" at `codex_astra_asicconverge.txt:22`, so a complete rc-0 answer exits 8 | DISPOSED | ADJ:91-101 (v1 §2B), ADJ:223-232 (v2.2); ledger :62483.  READ stdout capture :2-4 (rc=0, wall 1, SEAT WALLED) | none |
| CX2 | grok, Argon | the fix is the wall test on stderr `ERROR:` lines only (Option B; Argon adds `\b`).  grok: the script's comments at :34-40 argue for it | DISPOSED | ADJ:223-232 adopted B; AST2:11-26 refutes its sufficiency.  READ final550 (re-checked by the prescreen agent): rc 0, a 4,265 b answer, and six line-start usage-limit lines quoted in stderr (`:5625-5626`, `:5653-5654`, `:5891-5892`); `astra550.launch.log` = SEAT WALLED.  HV:235-236 HELD.  REASONED: word anchors cannot tell a quoted line from codex's own | goes to the v3 reconciliation (CX3) |
| CX3 | grok (§1), grok-rec (agreed 2) | the wall decision (`:56`) comes before the rc test (`:58`), so rc 0 with an answer still exits 8; `$verd` (`:45`) is only echoed (`:48`) and never decides anything | **LIVE** | READ HEAD `:45`, `:48`, `:56`, `:58`; the working tree is identical (re-checked by the prescreen agent).  PL:53-74 classifies only when rc != 0 or stdout is empty, and its comment names astra550, AST2's final550 counterexample.  ADJ v1/v2 and AST1/AST2 never weigh rc | v3 of `cxlaunchquotation`: rule PL's rc/empty-stdout gate for `tools/cxlaunch.sh`.  Controls: the four v2.2 fixtures with rc stated; final550 (rc 0); a real wall (rc 1, empty stdout) |
| CX4 | grok-rec (D1), Argon | `:41` "stdout ... may be grepped freely" contradicts `:34-38` and `:40` | DISPOSED | AST1:111; ADJ:232 | rewrite `:41` with whatever v3 adopts |
| CX5 | grok | Option A's VERDICT gate fails the wall control, because the echoed brief carries VERDICT | REFUTED | READ `cxctl/ctl_receipt_cxlaunch_v2.txt:6,:16` (A on the real wall gives WALLED rc 8), and `block_optA.sh:3-5` (stderr `ERROR:` lines are counted regardless); grok-rec D2 | none |
| CX6 | grok, Argon | other prose false-matches `:44`'s patterns: "usage limits", "rate limited"; Argon adds "separate/accurate limit" and "not authenticated" | DISPOSED | REASONED: moot once stdout is not scanned (ADJ:223-232 B; PL) | none |
| CX7 | grok, Argon (Form A) | Option A: a word-anchored stdout scan when there is no VERDICT | DISPOSED | ADJ:96 rejected it.  ADJ:230 measured it: on verdict-less quota prose, A walls and B answers | OB:24716 and ledger :62489 still prescribe A.  Correct them when v3 lands (see "records consequences" below) |
| CX8 | grok | the answer's 10,466 bytes were not re-measured | REFUTED (the doubt) | READ `wc -c` = 10,466; `cxctl/ans.txt` = 10,466 | none |
| CX9 | grok, grok-rec | there is no stderr file, so "0 `ERROR:`-line wall hits" is an inference | DISPOSED | ADJ:232 (v2.2 (i)); AST1:113; AST2:129 | none |
| CX10 | grok, grok-rec (FA4) | stdout capture `:5` (`LAUNCH_RC=8`), `:6-8` (the answer's opening) and `:10` (`[exited with code 0]`) are not cxlaunch.sh output | DISPOSED (immaterial) | READ: `:1-10` are wrapper lines; every receipt cites only `:1-4` (ADJ:99; AST2:129) | none |
| CX11 | grok | offers an alternative wall fixture, `_scratchpad/panel_20260817_174701/codex.txt:110-111` | DISPOSED | READ: these are real usage-limit lines.  The adopted fixture is `panel_20260925_151610:15-16` (ADJ:98; `cxctl/wall.err`) | none |
| CX12 | grok, grok-rec, Argon | `panel.sh:497`'s `quota[^.]*` matches "quotation", but the gates at `:492` and `:700-702` keep this answer out, and `:708` counts it ok | DISPOSED | ADJ:39.  READ `panel.sh:491-500` and `:692-709` | none |
| CX13 | grok-rec (D3, D4, FA3) | the payload is sz−BSZ = 7,934; the echo test is at `:492`, not `:493`; the answer does not echo `brief.md:3` | DISPOSED (immaterial) | READ `:491-493`.  It corrects agy's answer only; the classification is unchanged | none |
| CX14 | Argon | `panel.sh:519`'s tail-400 test fires on healthy answers that cite `402`/`403` or quote a wall phrase, labelling them `WALLED MID-ANSWER` | DISPOSED (prior filing) | `panelwallquote` (ledger :55892; OB:22511-22525).  READ census: 41 MID-ANSWER labels on disk (copies included).  Three are healthy answers: `panel_20260921_154943`'s codex (its tail quotes `"http_status": 402`; the verdict is at `:4435`) and agy ("Grok 402"), and `panel_20260925_144647`'s minimax (verdict at `:1`).  The 402-citation shape is not named in the filing | add the 154943 codex/agy pair to `panelwallquote` as a second control shape |
| CX15 | Argon | the echo-only branch at `panel.sh:497` prints `head -1` of the first match in file order, so the `wall:` reason is often echoed-brief text | **LIVE** | READ (re-checked by the prescreen agent): `panel_20260820_005715/SEATS.txt:3` "wall: quota wall -- kimi was answering..." is brief text at `codex.txt` offset 11,333 of 21,330, and the real notice ends the file.  Census: 7 ECHO-branch reasons in 5 panels are brief text.  The class is right; only the label is wrong.  Not filed (grep of OB and ledger: 0) | cosmetic.  Fold it into `panelwallquote`: take the reason from the file's tail.  Control: `panel_20260820_005715` |
| CX16 | Argon | the tally at `:692`/`:728` labels echo-only and sub-800-byte files `rated` on a bare `quota\|401\|403\|429` match in brief text | REFUTED | READ: the design text calls the pattern "deliberately broad" (`:719-723`); rated ⊂ miss; the message says "read each seat file for the ACTUAL status" (`:741-742`).  The genuine short-answer half is the deepseek-712 remedy (ADJ:262) | none |

Transport flags (Argon, packet only, not graded): 1.

**Prescreen note (not a seat finding):** OB:22494-22503 already files this class: `cxlaunchwallfp` (LOW, harness, filed
2026-09-26).  It names both halves:
- #549's stdout matched "quotation";
- #550's stderr held quoted `^ERROR:` lines (the same run as AST2's final550).

Its fix shape: "key the stderr test on codex's own error block at the END of the stream".  It has **no ledger row**
(grep: 0), and neither ADJ v1/v2 nor AST1/AST2 cites it (READ, re-checked by the prescreen agent).  v3 should merge it
with `cxlaunchquotation`, or row it.

LIVE (this job): CX3 and CX15 (see "LIVE items").

counts: DISPOSED 11 (2 immaterial, 1 prior filing) / LIVE 2 / REFUTED 3 / CANNOT SETTLE 0 (16 findings)

## dash_okclass

Files read:
- the brief, grok (grok compacted mid-task), grok-rec, Argon `gemini_web.out` and its manifest;
- at HEAD: ledger :62501-62507; `run_controls.py:1-40` (49 `^            (` tuples); the `controls_534/` listing;
  `check_stage_panels.py`, `check_fable_queue.py` and `stage_tokens.py` (grepped for a `d` key); OB:24704-24716;
- an in-memory python read of all 439 `"d": "OK"` entries in the HEAD ledger.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| DA1 | grok, grok-rec | the "365 OK cells, all pend" claim (ledger :62506-62507) was never counted; grok's figure of 79 for `>OK<` is a line count | DISPOSED | ADJ:44 verified 365, all `c pend`; AST1:134 TRUE; grok-rec:29 | none |
| DA2 | grok (settled by grok-rec) | the ledger's "sections H and I never read `d`" was not re-checked | REFUTED (the doubt) | READ: HEAD `check_stage_panels.py`, `check_fable_queue.py` and `stage_tokens.py` carry no `"d"`/`'d'` literal (0/0/0); grok-rec:23 | none: the row's sentence stands |
| DA3 | grok, grok-rec | no `json.dumps` round trip of the ledger blob was run | DISPOSED | AST1:133 verified a byte-identical round trip; ADJ:43 and :104 | none |
| DA4 | grok, grok-rec | `run_controls.py` is tracked, but the brief said untracked | DISPOSED | ADJ:42 (F1, BRIEF DEFECT); AST1:131 | none |
| DA5 | grok, grok-rec (Argon via its bundle) | no `tools/pipeline/*.py` writes the ledger as indent=1 + CRLF; the recipe is `ledger_audit0923.py` | DISPOSED | ADJ:43; AST1:132-133 | none |
| DA6 | grok, grok-rec | 958 `d` values are neither OK nor a glyph, and 1,980 entries have no `d` | DISPOSED | ADJ:44 and :238 (399 residual); AST1:136; AST2:117-119.  READ: 958 = 253+89+128+31+22+7+29+399 | none |
| DA7 | grok, grok-rec | the other 438 OK notes were not scanned for stage tokens | REFUTED (the doubt) | READ: none of the 439 OK notes carries any of the five tokens at `stage_tokens.py:18-22`, so all 439 are answers | none.  Whether an answer is an approval is a separate axis (AST2:28-42) |
| DA8 | grok, grok-rec, Argon | fix it by mapping `"OK": "ok"`, plus a DASH control and mutant.  A map alone still prints `OK` (`:178`) and leaves `n["OK"]` off the `:407` strip | DISPOSED | the mapping was REJECTED at ADJ:105; AST1:24 and :152; ADJ:237 (v2.3) | records consequence (see below): ledger :62507 and OB:24712-24713 still offer the rejected one-line option |
| DA9 | grok-rec | agy's "53,887 lines" and blob `d352cecf` are wrong (actual: 62,524 lines, blob `c120bd52`) | DISPOSED (immaterial) | READ: only the automatic HARVEST_AUTO.md:145 carries `d352cecf`; no disposition relies on either number | none |
| DA10 | grok-rec | the ten implement-phase OK entries are 9 in gdromcondlies and 1 in widthkillclass (opus5), not all ten in gdromcondlies | DISPOSED (immaterial) | READ python tally {gdromcondlies 9, widthkillclass 1}.  ADJ:44 and AST1:134 say only "ten" | none |
| DA11 | grok-rec | agy's mutant comments out the line and swallows the closing `}` (a syntax error); grok's whole-line restore is valid | DISPOSED (immaterial) | READ: no adopted spec carries either mutant, since the mapping fix is rejected (ADJ:105) | none |
| DA12 | grok-rec | choose map or sweep; the byte-safe sweep is a literal replace of the 439 lines | DISPOSED | the all-439 sweep was WITHDRAWN at ADJ:236.  AST2:28-42: 262/177 reproduces as 272/167, and an explicit disposition manifest is owed.  HELD at HV:235-236 | none |
| DA13 | Argon | `run_controls.py:16-17` says the disclosed escapes were "measured passing 48/48", but the instrument has 49 expectations | **LIVE** | READ HEAD `:16-17`; also `:125` "F_selfseat_skip 48/48".  The cited log `scratchpad fable534/drive_fable.out` exists nowhere under the project or the session temp dirs (find: 0; re-checked by the prescreen agent).  `controls_20260918_v3.out:1` says base 49/49 | low.  Annotate the disclosure as measured on a 48-row instrument with a non-durable log, or re-measure the four escapes on the 49-row instrument |

Transport flags (Argon, packet only, not graded): 3.

LIVE (this job): DA13.

counts: DISPOSED 10 (3 immaterial) / LIVE 1 / REFUTED 2 / CANNOT SETTLE 0 (13 findings)

## stagetokens_controls

Files read:
- the brief, grok, grok-rec, Argon `gemini_web.out` and its manifest;
- at HEAD: ledger :62492-62498 and OB:24706-24710;
- `fablequeue8n_20261009/regress_harness/`: `never_reddened.txt`, `extra_mutants.out`, `rgh_extra_mutants.py.txt:1-16`
  and the file mtimes.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| ST1 | grok, grok-rec, Argon | `never_reddened.txt` has 16 lines, but the row says "13 of 49" | DISPOSED | READ: 16 lines.  ADJ:47 and :158 (header or trim); AST1:144 | correct the artifact in the stagetokenscontrols commit, as ruled |
| ST2 | grok, grok-rec, Argon | lines 14-16 are reddened by shipped variants (`controls_HEAD.out`; `controls_20260918_v3.out:4,11,14,20,23,27,29`) | DISPOSED | ADJ:48 verified line by line; AST1:145 | as ruled |
| ST3 | Argon | the cause: those three names contain commas, and `never_reddened.txt` predates the substring-matching script | DISPOSED (a detail) | READ `rgh_extra_mutants.py.txt:1-2` "by SUBSTRING (three expectation names carry commas)"; mtimes 19:33 < 19:34 < 19:35.  ADJ:48 says "kept from the first pass" | can supply the header line's wording |
| ST4 | grok, grok-rec | the pin text quoted in ledger :62498 (`..    t_reread  review  1/9  filed`) is not a literal listing line | DISPOSED (immaterial) | READ: the adopted re-pin is a `\s+` regex (ADJ:48); AST1:148 executed it, TRUE | none: the commit uses the regex, not the prose |
| ST5 | grok-rec | which re-pin regex?  grok's requires ", not yet panelled"; all three candidates match "filed" and miss "grandfathered" | DISPOSED | ADJ:48 adopts agy's first form; AST1:148 | none |
| ST6 | grok, Argon | adopting `X_filing_is_zero` without the re-pin turns the harness red, because every mutant must red at least one expectation | DISPOSED | READ: ledger :62498 and OB:24709-24710 already say "one commit" (OB re-checked by the prescreen agent); ADJ:48 | none |
| ST7 | Argon | `X_filing_is_zero`'s score after the re-pin is unsettled (48/49?) | DISPOSED | ADJ:273 (v2.6) gives 48/49.  AST2:158: that comes from reading the source, with no execution receipt | the commit's control run supplies the receipt |
| ST8 | grok-rec | line corrections to the seat answers: the state_note is `:62498`; `X_filing_is_zero` is `extra_mutants.out:22` (grok said `:21`); the violation print is `:293`; the grandfathered print is `:247-248`; `:282` is a second id-first print | DISPOSED (immaterial) | READ.  ADJ:47-48 cite the lines correctly | none |

Transport flags (Argon, packet only, not graded): 4.

LIVE (this job): none.

counts: DISPOSED 8 (2 immaterial) / LIVE 0 / REFUTED 0 / CANNOT SETTLE 0 (8 findings)

## edits560

Files read:
- the brief, grok, grok-rec; `agy_edits560.txt`, for the attribution check only; Argon `gemini_web.out` and its
  manifest;
- `inputs/EDITS_560.json`;
- `OUTSTANDING_BUGS.md` at HEAD and at 1329d894;
- `ls est/`; `tools/est_divergence.txt`.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| E51 | grok | `EDITS_560.json` has no "held" key; the holds come from 3d7c61bb | DISPOSED | ADJ:51 (F1); AST1:156 | none |
| E52 | grok, grok-rec, Argon | 34 held corrections, all still applying | DISPOSED | ADJ:51 and :137: the held set is 37, because hrec 2/9/10 fall outside the brief's 29+5 scope; AST1:207 | none |
| E53 | grok (grok-rec credits agy) | the replacement text for place 14 cites `OUTSTANDING_BUGS.md:14809-14812`, which is no longer where that paragraph sits at HEAD | **LIVE** | READ (re-checked by the prescreen agent): `EDITS_560.json`'s place14 `new` text cites `OUTSTANDING_BUGS.md:14809-14812`.  The cited paragraph ("And it is the second such fact in the same audit") was at `:14809` at 1329d894 and is at `:14821` at HEAD | re-key to a grep anchor before applying held correction #1 (ADJ §3 row 1, `dev_sgi_re.c:465`) |
| E54 | grok, grok-rec | `diff_ieee_store.c` has no est/ twin | **LIVE** | READ (re-checked by the prescreen agent): `est/` has no `regress/` directory, and the `tools/est_divergence.txt` header scopes byte-identity to `src/`.  This contradicts ADJ:271 (v2.6) and HV:226, which say "regress/ edits owe est/ byte-identity" | erratum to ADJ v2.6 and HV: a regress/ edit owes only precommit E's identity guard.  ADJ:271's withdrawal of "or exempt" stands |
| E55 | grok-rec | the ten span flags are not defects, and their ADJ line numbers are wrong | DISPOSED | ADJ:52; AST1:216 | none |
| E56 | grok-rec | grok-rec's own attributions in the disagreements (who flagged the OB citation, who said "est/: Yes", who raised the ten span flags) | REFUTED | READ: agy has 11 FLAG lines, 0 hits on `14809`, and says "Shared: Yes".  grok has 3 FLAG lines, including `:304` (the OB citation) and "not est/ twins".  The reconcile swapped the seats | credit by file, not by the reconcile |

Transport flags (Argon, packet only, not graded): 29.

LIVE (this job): E53 and E54.

counts: DISPOSED 3 / LIVE 2 / REFUTED 1 / CANNOT SETTLE 0 (6 findings)

## carrier_citations

The carrier copies: HEAD:n = `git show e483d931:tools/CLAUDE.md` line n; live:n = the project-root `CLAUDE.md`.  `cmp`
shows the root `CLAUDE.md` is byte-identical to the working-tree `tools/CLAUDE.md`: 4,088 lines, against 3,846 at HEAD.

Files read: the brief, grok (grok compacted mid-task), Argon `gemini_web.out` and its manifest (its bundle held only the
two carrier copies), and the HEAD source at every cited and every proposed line.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| CC1 | grok | HEAD:570's `diskimage.c:1763` is not the prefix guard | **LIVE** | READ (re-checked by the prescreen agent): `src/disk/diskimage.c:1763` is `"NULL ptr");`, and the guard `if (prefix_i + prefix_f + prefix_s > 1)` is at `:1879`.  The live copy is unchanged | re-key to a grep anchor |
| CC2 | grok | HEAD:881's `cpu_sh.c:780-796` is not the four exception arms | **LIVE** | READ: `:780` is the XF debug dump; the arms are at `:1046`, `:1060-1061` and `:1075`; live:911 | re-key |
| CC3 | grok | HEAD:882's `dev_sh4.c:700-702` is stale | REFUTED | READ HEAD:880-883: the sentence reports `:700-702` as the seat's upstream number, not as a claim about the fork.  Argon agrees | none |
| CC4 | grok | HEAD:882's fork raise site `:1159` is stale | **LIVE** | READ: `:1159` is `itlb_lo[`; the raise `sh_exception(..EXPEVT_RESET_TLB_MULTI_HIT..)` is at `:1177-1179`.  grok compared it with the `INTERRUPT_ASSERT` sites, the wrong construct | re-key |
| CC5 | grok | HEAD:2520's `gate_arm.sh:561` no longer holds the "261" sentence | **LIVE** | READ: it is now at `:564`; live:2750 | re-key, or mark historical |
| CC6 | grok | HEAD:2602's `footbridge_sites_probe.py:111` is not the `-E cats` exec | **LIVE** | READ: the exec is at `:300` (`run_arm` at `:293`) | re-key |
| CC7 | grok (STALE) vs Argon (ALREADY-MARKED) | HEAD:2605's `dev_footbridge.c:548` (console_putchar) and the timer mask at `:640` | **LIVE** | READ: the parenthetical states the 08-26 locations as current; at HEAD they are `:558` and `:663`.  Argon's ALREADY-MARKED reading is wrong | re-key |
| CC8 | grok | HEAD:2654's `check_witness.py:56` regex and `:24-28` header | **LIVE** | READ: `:56` is a cutoff-date comment.  The regex is at `:87` and now includes `detector:`; the gap sentence is at `:30-32` | re-key |
| CC9 | grok | HEAD:2657's `precommit_check.sh:678` does not repeat the harness gap | **LIVE** | READ: `:678` is section X; the gap comment is at `:776-777` | re-key |
| CC10 | grok | HEAD:2828's `gate_build.sh:64-65` and `:302-305` | **LIVE** | READ: the withdraw calls are at `:67-68`; the publish lines are `:304` and `:307` | re-key |
| CC11 | grok | HEAD:2845's `gate_asan_sweep.sh:60,62` are not oracle lines | **LIVE** | READ: `:60-62` is the "not bounded" comment.  The substance holds: `timeout 25` sits at `:266` and `:268` | re-key to `:266`/`:268` |
| CC12 | grok | HEAD:3221's `gate_sh_rounding.sh:615` is not the `-u` warning | **LIVE** | READ: the warning is at `:626-628` | re-key |
| CC13 | grok | HEAD:3593's `cpu_sh.c:255-258` is not the IRQ-level loop | **LIVE** | READ: the loop is at `:390-394` | re-key |
| CC14 | grok | HEAD:3621: `cpu_sh.c:312-316`, "whose `exit(1)` sits in the assert path" | **LIVE** | READ (re-checked by the prescreen agent): `:312-316` is the Table 19.5 comment.  The file's only `exit(1)` calls are `:101` (SH64) and `:1085` (`sh_exception`'s default), so the present tense "sits" is also stale | mark historical |
| CC15 | grok | HEAD:3636's `gate_hygiene.sh:402` is a bare `#` | **LIVE** | READ: the logic is at `:864` and `:868` | re-key |
| CC16 | grok | the product comment at `src/cpus/cpu_sh.c:458` cites `dev_sh4.c:2386-2388` as the IRLM refusal | **LIVE** | READ (re-checked by the prescreen agent): HEAD `dev_sh4.c:2386` is `case SH4_RTCOR:`.  The IRLM `fatal` is at `:2507-2509` (`:2635` in the working tree, where the peer has added 126 lines) | a comment-only fix to a src file: grep anchor, propagation to all four trees, the two-part clearance.  Or file it |
| CC17 | grok | HEAD:1999's "ONLY counter-style bound" is unverified | REFUTED (the doubt) | READ: two censuses (function-static counters with a numeric bound; named warn/msg counters) both find only `memory_rw.c:504-508` | none |
| CC18 | Argon | the carrier copies diverge by 242 lines although section J hard-fails on divergence | DISPOSED | ADJ:55; AST1:222 and :231.  READ: `cmp` of the root against the working `tools/CLAUDE.md` is clean | none |
| CC19 | Argon | `Makefile.skel:194` is ambiguous | REFUTED | READ: `src/cpus/Makefile.skel:194` is the `cpu_sh.o` rule, current; HEAD:3553 names `src/cpus/Makefile` beside it | none |
| CC20 | grok / Argon | totals of 35 vs 36 citations | DISPOSED (immaterial) | READ: the grep finds 35 tokens.  Argon's 36 includes `Makefile.skel`, which is outside the brief's form.  No record carries either total | none |

Transport flags (Argon, packet only, not graded): 36.

LIVE (this job):
- **14 stale cross-file line citations in the carrier:** CC1, CC2, CC4-CC15 (the live copy is unchanged; the fork
  wrote "13" and the list holds 14).  They fall under the CITATION-FORM RULE (HEAD:3492 / live:3734) and its
  no-checker escalation (HEAD:3523).
- **CC16:** a stale cross-file citation in product code.

counts: DISPOSED 2 (1 immaterial) / LIVE 15 / REFUTED 3 / CANNOT SETTLE 0 (20 findings)

## carrier_counts

Files read:
- the brief, grok, Argon `gemini_web.out` and its manifest;
- the derivers, re-run read-only at HEAD (`git show` / `git grep`);
- `_scratchpad/nightly/battery_20261011_180002.log`; `ls _scratchpad/*.pdf` and `find _scratchpad -name '*.pdf'`;
- ledger row `sgirekills`.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| CN1 | grok, Argon | the `80/13/51` block is absent from HEAD; grok says it is "only in a diff artifact" | DISPOSED | ADJ:55 (uncommitted carrier lag).  READ: present at live:2178, so grok's "only" is wrong | none |
| CN2 | grok | the JOIN+MARK latch-marker census has drifted from 80/13/51% | **LIVE** | READ re-run: **92 markers / 14 spellings / `(once)` 52 = 56.5%**.  grok's 91 missed the `dev_vga.c:914-915` wrap.  8 hits sit inside comments, among them `dev_dreamcast_g2.c:66`'s "(once for each channel)", which is a register comment, not a latch.  The 14th "spelling" is a comment-wrapped marker at `dev_sgi_ip30.c:58-59`, so the block's own "more than 13 spellings means a broken join" self-check would misread a correct join | file under the counts rule (HEAD:3371 / live:3613); the deriver also needs a comment exclusion |
| CN3 | grok | the line-based once-family count is 75, against the carrier's 64 | **LIVE** | READ: 75 | as CN2 |
| CN4 | grok | the whole-file once-family count is 83, against 71 | **LIVE** | READ: 83 | as CN2 |
| CN5 | grok | HEAD:2033's `(once)` 24 is stale, and `reported once` is 4 | REFUTED (as a defect) | READ HEAD:2026-2032: the 24 is given as dated output ("On 2026-08-30 that printed") beside its deriver, and live:2236 already marks it superseded.  `reported once` counts 5, unchanged | none |
| CN6 | grok | the latch sites, 30 in 13 files (28/11 latches), are now 28/13 (26/11) | **LIVE** | READ: the two-pattern grep gives 28 sites in 13 files.  Two are periodic counters (`dev_algor.c`, `dev_mc146818.c`).  Two pcc2 `w` sites were removed (`dev_pcc2.c:680-711`) | file (counts rule) |
| CN7 | grok | the wall-clock oracles, 47 in 27 files, are now 55 in 31 | **LIVE** | READ `git grep -c`: 55 hits in 31 files | file (counts rule) |
| CN8 | grok | the "45" has no deriver | REFUTED (as a defect) | READ HEAD:2841-2844: the carrier says the value moves with the regex and only the growth matters | none |
| CN9 | grok, Argon | `gate_build.sh` states no 41/58 census | DISPOSED (immaterial) | READ: the carrier cites `gate_asan_sweep.sh` for 41/58 (HEAD:2530-2532), never `gate_build.sh`.  The premise came from the brief | none |
| CN10 | grok | no machine-list file is committed | DISPOSED (immaterial) | READ: the list is the runtime `$LOGDIR/mtypes.txt`.  The brief said "if a list file exists" | none |
| CN11 | grok | "no line says SIX active" | REFUTED | READ: the ledger row `sgirekills` (HEAD :29906) is titled "SIX active exit(1) statements remain", and the 6 active calls hold (`:1498`, `:1506`, `:1582`, `:1587`, `:1598`, `:1720`) | none |
| CN12 | Argon | the `sgirekills` census lines (`:1463…:1685`) and its "six further in comments" have drifted | **LIVE** | READ: the census is dated 2026-09-08 (ledger :30359).  At HEAD the lines are +35, and there are 7 comment texts (`:273`, `:315`, `:453`, `:457`, `:931`, `:1187`, `:1493`) | annotate when the row is next touched (counts rule: FILE, no sweep) |
| CN13 | grok, Argon | the carrier says "FIFTEEN PDFs", but its fence lists 19 | **LIVE** | READ HEAD:2890 / live:3120.  `ls _scratchpad/*.pdf` = 20 (re-checked by the prescreen agent) | correct it, with the deriver and a date |
| CN14 | grok, Argon | `ata2_x3t10_948d.pdf`/`.txt` is present but in neither inventory, although `dev_wdc.c:640` cites its `.txt` | **LIVE** | READ (re-checked by the prescreen agent): 20 top-level PDFs; HEAD `src/devices/dev_wdc.c:640` cites `_scratchpad/ata2_x3t10_948d.txt:1529-1531` | add it to the PDF and txt fences |
| CN15 | grok | `_scratchpad/lance/` holds 6 PDFs that `ls _scratchpad/*.pdf` cannot see | **LIVE** | READ `find`: 26 PDFs, 6 of them under `lance/` (re-checked by the prescreen agent: 26) | widen the deriver to `find _scratchpad -name '*.pdf'` |
| CN16 | Argon | the txt fence lists 15 and omits vmesbcp2, 21066, ddi0406 and ppc_uisa | **LIVE** | READ HEAD:2995-3009 | the same edit as CN13 and CN14 |
| CN17 | Argon (stale) vs grok (SAME) | gate 14's "358 checks" | **LIVE** | READ (re-checked by the prescreen agent): `battery_20261011_180002.log:6188` reads `gate 14: ARM/Thumb flags ...: PASS (1110 checks)`.  grok's SAME compared against the gate's own historical comment (`gate_arm.sh:564`).  Argon's method (counting call sites) was wrong, but its conclusion holds | correct HEAD:2517 / live:2747, with the deriver and a date |
| CN18 | Argon | `gate_build.sh`'s DIVERGENT list omits `.index` | REFUTED | READ: `list_diffs` (`gate_build.sh:81-92`) compares only `*.c`, `*.h`, `*.cc` and `*.skel`, so `.index` is outside its set | none |
| CN19 | Argon | the carrier copies diverge despite section J | DISPOSED | ADJ:55 | none |

Transport flags (Argon, packet only, not graded): 5.

LIVE (this job):
- **Decayed dated counts** (the carrier's counts rule says FILE, no sweep): CN2-CN4, CN6, CN7, CN12 and CN17.
- **The primary-source inventory** (CN13-CN16): the carrier says FIFTEEN, its fence lists 19, and there are 20 on
  disk.  `ata2` is missing although product code cites it; 4 extracted texts are unlisted; `lance/` is outside the
  `ls` deriver.

counts: DISPOSED 4 (2 immaterial) / LIVE 11 / REFUTED 4 / CANNOT SETTLE 0 (19 findings)

## carrier_d2_texts

Files read:
- the brief, grok, grok-rec, Argon `gemini_web.out`;
- live:1538-1550; the working-tree `BRIEF_TEMPLATE.md:652-661` (702 lines at HEAD, 854 in the working tree);
- `wdc473floor/pass1_20261009/fable5_pass1.md:31`; `fable5_meas/det128.txt` and `det137.txt`;
- `asiceventaddr/f2_20261013/opus5_final/work/mk_media_t2.py:70,:74`; `table2_20261013/SCORES.txt`.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| CD1 | grok, Argon | D2 is absent at HEAD | DISPOSED | ADJ:56 (F2) | none |
| CD2 | grok, Argon, grok-rec | the carrier copies diverge; agy's "316 lines" and "only in live" are wrong | DISPOSED | ADJ:55; ADJ:268 (v2.6: +263/−21).  READ `cmp` | none |
| CD3 | Argon | §C7 is absent from HEAD's `BRIEF_TEMPLATE.md` | DISPOSED | ADJ:57 (F3) | none |
| CD4 | grok, Argon | D2 contradicts itself at `e < 96` (its formula vs its criterion) | DISPOSED | ADJ:58 (F4); ADJ:141 (§4: draft (a) recommended) | none |
| CD5 | grok, grok-rec | the WDC exemplar's "rows at 32769 and 32767 red each one" comes from the 137-row extension (one edge family per mutant); the shipped detector is the 128-row one | **LIVE** (owner D2) | READ: in det137, M2c/M3b/M2d/M3c redden only their own edge rows; det128 scores all four 0/128 | owner's D2 wording: add the det137 qualifier |
| CD6 | grok, grok-rec | "`< 97` detected at 96" is a truth-table derivation, not a scored mutant | **LIVE** (owner D2) | READ (re-checked by the prescreen agent): `mk_media_t2.py` has `nohigh` (`:70`, drops `(e) < 96`) and `hightight` (`:74`, `< 96` → `< 95`) but no `< 97` medium.  Draft (a) as recorded says "detected" (ADJ:141) | owner's D2 draft (a): say "differs at 96 (derived)" and cite the scored `nohigh`/`hightight` |
| CD7 | grok, grok-rec | §C7's CHANNEL column names `> B-1`, which at a clamp is the EQUIVALENT mutant; the below-edge move that reddens is `> B-2` (`> 32766`) | **LIVE** (owner D2) | READ (re-checked by the prescreen agent): `fable5_pass1.md:31` (`> 32767` is EQUIVALENT); det137 M3b/M3c; working-tree `BRIEF_TEMPLATE.md:655-656` "(`> B+1`, `> B-1`)" | fix §C7 together with the D2 ruling |
| CD8 | grok | §C7's "rows at 68928 and 4998 let every one-token bound move pass all 128 rows" overclaims | **LIVE** (owner D2) | READ: det128 scores only 4 moves (65536/16384/32769/32766, all 0/128).  REASONED: a move past 68928 would redden the 68928 row | say "the four measured moves" |
| CD9 | grok, grok-rec | §C7's `:659` cites the 09-25 block instead of D2 | DISPOSED | ADJ:59 (F5) and :141 | none |
| CD10 | grok, grok-rec | the SIBLING PARITY row's own "catches" cell describes a row-KIND gap, while the appended sentence says "not of row kinds".  And the live:1484-1486 corollary uses a row-name census, while the sentence says matching names discharge nothing | **LIVE** (owner ROUTE PARITY) | READ live:1708 and live:1484-1486 | owner's ROUTE PARITY wording, e.g. "in addition to row kinds; a name census can reveal, never discharge" |
| CD11 | grok-rec | the corollary "compares labels and routes" is false for routes | DISPOSED | AST1:229.  Note: ADJ:60 (F6, "VERIFIED") stands uncorrected in v2 | carry an erratum to ADJ:60 into the packet |
| CD12 | grok, grok-rec | where the parity sentence goes in `BRIEF_TEMPLATE.md`: after `:659`; §F has no parity item | DISPOSED | ADJ:143 | none |
| CD13 | grok, grok-rec | "route" is unbounded, and the two recorded bounds DIFFER: the enclosing function vs the block or file under test | **LIVE** (owner ROUTE PARITY) | READ (HV re-checked by the prescreen agent): HV:138-139 vs HV:161-163; ADJ:143 vs `asiceventaddr/adj_20261013/fable5_asic_adjudication.md:543-548` | owner: choose one bound |
| CD14 | grok, grok-rec | label clause: the binary result-`if` split | DISPOSED | ADJ:145; ADJ:272 (v2.6) | none |
| CD15 | Argon | JOIN clause: HEAD lacks the #529 third disjunct | DISPOSED | ADJ:61 (F7) | none |
| CD16 | Argon | the GUARD FIELD row's 7n-5 sentence exists only in the live copy | DISPOSED | ADJ:55 (the lag) | none |
| CD17 | Argon | the "LOCAL GIT ONLY" header conflicts with `:138` "Commit+push at every green gate" and with lifecycle step 7's "commit, push" | **LIVE** | READ HEAD:138 and HEAD:2847 / live:138 and live:3077, unchanged since the 08-22 supersession.  The header names the `:138` line as superseded, but the line carries no marker of its own | carrier wording: mark or delete the superseded conclusion (the carrier's own rule) |
| CD18 | Argon | the agy reservation contradicts the 09-15 directive | DISPOSED | the HEAD lag (ADJ:55).  READ live:809-810 marks the 08-30 text "HISTORY", so live:837 is no contradiction | none |
| CD19 | Argon | the Codex row: live:782's header "(xhigh)" and its invocation `model_reasoning_effort="xhigh"` vs ultra; HEAD:1138/1207 still say 5.6-SOL | **LIVE** | READ live:782; live:1238 is already corrected | fold into the recorded `:782` L4 (ADJ:101) |
| CD20 | Argon | a Kimi status contradiction at HEAD (`:813` vs `:1089`/`:1202`) | DISPOSED | the HEAD lag (ADJ:55).  live:843 was corrected 2026-09-17 and agrees with live:1119/1232 | none |
| CD21 | Argon | the option set says "SIX MEMBERS" but lists 7, and calls ALIAS "A seventh" | **LIVE** | READ HEAD:1889/1893/1931; live:2004/2008/2046 | carrier wording fix |
| CD22 | Argon | "FIFTEEN" vs 19 PDFs, and the 15-entry txt list | **LIVE** | READ; the same item as CN13/CN16 | one record with CN13-CN16 |
| CD23 | grok-rec | the verbatim parity row starts with `> \|` | DISPOSED (immaterial) | seat quote formatting only | none |

Transport flags (Argon, packet only, not graded): 0.

LIVE (this job):
- **For owner question D2** (CD5-CD8): the exemplar and the §C7 wording.
- **For owner question ROUTE PARITY** (CD10, CD13).
- **Carrier wording** (CD17, CD19, CD21, CD22).

counts: DISPOSED 13 (1 immaterial) / LIVE 10 / REFUTED 0 / CANNOT SETTLE 0 (23 findings)

## pass2ledger_schema

No agy answer exists for this job: agy was walled, and ADJ:17 records it NOT LANDED.  Only HV:11-16 and the asic
adjudication cover anything here, namely the line-93 numbers.  ASICADJ =
`regress/artifacts/asiceventaddr/adj_20261013/fable5_asic_adjudication.md`.

Files read:
- the brief, grok (grok compacted mid-task), Argon `gemini_web.out` and its manifest;
- HEAD `regress/pass2_ledger.tsv`: an in-memory field census, lines `:1-19`, `:55-56`, `:93-94`, `:121-131`,
  `:145-146`, and blame;
- HEAD `tools/precommit_check.sh:884-907`; `git ls-tree` for `check_pass2*`;
- the 9ca9cca header `:50-92`; 29b450ce's `dev_dreamcast_asic.c` diff; the sibling citation at 9ca9cca, 29b450ce and
  HEAD; `git grep` of the event call sites at 9ca9cca;
- `_scratchpad/panel_20260826_222557` (sizes, `len(t)`, `SEATS.txt`);
- ASICADJ:101, :130, :386-413; `build_20261009/SUMMARY.txt:7`;
- the ledger and OB, grepped for a schema filing; the working-tree diff of `pass2_ledger.tsv` (empty).

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| PS1 | grok, Argon (from its bundle) | `tools/pipeline/check_pass2_ledger*.py` does not exist | DISPOSED (immaterial: a wrong pointer in the brief) | READ `git ls-tree -r e483d931 \| grep -c check_pass2` = 0 | none |
| PS2 | grok, Argon | only precommit section F reads the file, and its awk tests `$1` as a SHA prefix (`:894`).  Columns 4-5 are never read, so a text cell passes | **LIVE** (feeds PS3's ruling) | READ `precommit_check.sh:887-907` (re-checked by the prescreen agent); `check_seats_read.py` reads `ledger.json`, not this file | rule it together with PS3: e.g. a format check from a dated cutoff, or none |
| PS3 | grok, Argon (origin: Astra's sentence) | the seat columns are not a schema.  Titles sit in seats-answering with counts in seats-READ (`:61-70`, `:93`, `:95-122`, `:125-126`, plus grok's "N fired:" rows); `:123-124` have no 5th field; the 49 rows from `:127` (2026-08-31) to `:177` have no seat cells at all; cells mix counts and prose (`9of9*` at `:105`, "6 of 6 READ IN FULL" at `:129`); there is no token grammar, and `date` is undefined.  So seats-READ cannot establish historical READ counts | **LIVE** (ruling) | READ census of the HEAD blob: 81 rows have 6 fields, 49 have 3, 2 have 4, plus 3 one-field continuation lines (re-checked by the prescreen agent).  The header at `:10-18` calls seats-READ "the one that means anything".  No ledger row, OB entry or ruling names this (grep) | records ruling: annotate the header (the columns are free text; READ is recorded only where a cell says so; none after 2026-08-31), or file a row.  No retro-fill |
| PS4 | grok | `:93`'s `7of9` sits in seats-READ but is an answer census; `fable5_asiceventaddr.md:77` reads it as answered | **LIVE** (an instance of PS3) | READ: `:93`'s column 5 is `7of9`, and its verdict text says "SIX SCRIPTABLE ANSWERED ... plus the opus5 Agent seat".  ASICADJ:408 repeats "7of9" unqualified | R8 already annotates `:93`; it could add "an answer count" |
| PS5 | grok, Argon | three receipts are split by raw newlines (`:55/56`, `:93/94`, `:145/146`); the continuation lines become extra awk records | **LIVE** | READ (re-checked by the prescreen agent): each split falls where the text meant the two characters backslash-n.  Lines `:56`, `:94` and `:146` are one-field continuations; `:93-94` blame 29b450ce.  ASICADJ:391 (R8) says to append "to the LAST COLUMN of the same line", but the 9ca9cca record ends at `:94` | put R8's erratum at the end of `:94`, or repair the three splits in the same records commit |
| PS6 | grok, Argon | section F's echo `grep "^$PREV"` (`:901`) uses the full SHA while rows hold short SHAs, so the "receipt found" line prints nothing | **LIVE** | READ (re-checked by the prescreen agent): `:889` sets `%H` (full); the comment at `:895-899` records the same short-vs-full fix, applied only to the awk test at `:894` | a one-line prefix match with a control.  Low: the gate's verdict is unaffected |
| PS7 | grok, Argon | `:93`'s "5.5x", "352 values across nine mask words" and the single clobber domain [128,479] contradict the diff (288 values, 4.5x) | DISPOSED | HV:11-16; ASICADJ:130 (F23) and R8 at `:391`; the Astra asic answer at `:108` | as ruled (R8) |
| PS8 | Argon | "of which it named 64" is contradicted: the comment never writes 64 | REFUTED | READ 9ca9cca `:82-84`: it names 128..159 and 256..287, which is 64 values | none |
| PS9 | Argon | "moved the macro to :92 ... the citation pointed at the new comment" is contradicted | REFUTED | READ the hunk `@@ -71,6 +71,24 @@`: the comment is at `:74-91` and the macro at `:92`; `dev_dreamcast_asic.c:184` at 9ca9cca still cites `:74` | none |
| PS10 | grok | the `:190` sibling citation does not match 9ca9cca, where it is at `:189` | REFUTED | READ: `:93` was written in 29b450ce, where the citation is at `:190`, as it is at HEAD | none |
| PS11 | grok | "Fixed by RE-KEYING" is not in the header diff | REFUTED | READ: 29b450ce's `dev_dreamcast_asic.c` hunk re-keys to the construct name; ASICADJ:101 | none |
| PS12 | Argon | `#define SYSASIC_EVENT_FOO 96` is not in 9ca9cca | REFUTED | READ: it is absent at 9ca9cca and first appears in 29b450ce, the commit that wrote `:93` | none |
| PS13 | Argon | "mispaired 96..127 -> +0x0c,+0x1c" drops the comment's ", ..." | REFUTED | READ 9ca9cca `:80`: 4*(96>>5) = 0x0c only.  ASICADJ:403-404 (R9) calls this a wrong shipped claim | none |
| PS14 | grok | "nothing >= 96 anywhere in src/" is not established | REFUTED (the doubt) | READ: at 9ca9cca every `SYSASIC_TRIGGER_EVENT` call passes a named constant ≤ 35, and the 21 defines max out at 67 | none |
| PS15 | grok, Argon | the seat sizes on `:93` (968,024 b ... 142,525; eval_count 65536) are unverified | REFUTED (the doubt) | READ: each equals seat_verdicts' `len(t)` on `panel_20260826_222557`, i.e. decoded characters labelled "b" (the byte sizes differ).  `"eval_count": 65536` is present | none; only the unit label is noted |
| PS16 | grok, Argon | C99/C11, V0-V3 and 202311L cannot be verified from the diff | DISPOSED | ASICADJ:404-405 (R9) and :413; `build_20261009/SUMMARY.txt:7` | none |
| PS17 | Argon | only 39 of 145 rows have 6 fields; 55 have 7-13; `:125`, `:126` and `:129` are malformed; 47 rows have 3 fields | REFUTED | READ HEAD census, histogram {1:3, 3:49, 4:2, 6:81} (re-checked by the prescreen agent).  No row exceeds 6 fields; `:125`, `:126` and `:129` have 6; 49 rows have 3.  grok's 81/49 is right | none |

Transport flags (Argon, packet only, not graded): 1.

LIVE (this job):
- **The seat-column schema** (PS3, with PS2 and PS4).
- **The raw-newline splits** (PS5).
- **Section F's echo** (PS6).

counts: DISPOSED 3 (1 immaterial) / LIVE 5 / REFUTED 9 / CANNOT SETTLE 0 (17 findings)

## nullmediumlegs_wiring

Files read:
- the brief, grok, Argon `gemini_web.out` and its manifest;
- at HEAD: `regress/ppc_rldicl_probe.py`, `regress/alpha_tbi_probe.py`, and
  `tools/pipeline/check_probe_wiring.py:1702-1710` and `:3036-3065`;
- ledger rows `nullmediumlegs` :62429, `ppcprobescorestale` :47456, `probeexitzero` :47440 and `wiringcliff` :29655;
- the 15 `regress/gate_*.sh` and `run.sh`, at HEAD and in the working tree;
- the md5 of the t2 frozen probe, against the `a05660af^` and HEAD blobs;
- the working-tree diff of `check_probe_wiring.py`.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| NL1 | grok (Argon via its manifest) | no gate runs either probe: `alpha_tbi_probe.py` appears only in the `gate_hygiene.sh:420` name list and the `:430` comment.  No row count is pinned by equality, `check_min` or sentinel.  Both are EXEMPT until 2026-10-22 | DISPOSED (prior filing) | READ: a grep of all gate scripts, at HEAD and in the working tree, finds only hygiene `:420`/`:430`.  The EXEMPT dates are at `check_probe_wiring.py:3038` and `:3050`.  This is already recorded in `nullmediumlegs`' state_note and in `wiringcliff` (in work) | none.  Both exemptions go red from 2026-10-23 (`d < today`); `wiringcliff` owns that (see PW6) |
| NL2 | grok, Argon | the ppc probe's `:538-541` and `:604-607` say "THIS FILE HAS 19 ROWS, NOT 24 ... 19/19, 14/19", but the file makes 24 `row(` calls, and the manifest says 24/24 and 16/24 | DISPOSED (prior filing) | READ: 24 `^row(` calls at HEAD.  Filed as `ppcprobescorestale` (:47456, LOW, open since 09-11) | repair under `ppcprobescorestale` |
| NL3 | Argon (grok noted "kept below" in the second copy) | `:522-541` and `:588-607` are a verbatim 20-line duplicate, one on each side of the pass-2 rows | DISPOSED (prior filing) | READ: the two ranges diff identical.  `ppcprobescorestale` covers the row-count "comments" (plural) | the repair should delete the second copy, not correct both |
| NL4 | grok | `:36` calls the naive-fix row CARRIED-NOT-COUNTED, but `row()` appends it and SCORE uses `len(rows)` | DISPOSED (prior filing) | READ `:107-114` and `:639-642`.  This is `ppcprobescorestale`'s second defect | as NL2 |
| NL5 | Argon | the ppc probe exits 0 when rows fail; there is no `sys.exit` after SCORE | DISPOSED (prior filing) | READ: the only `sys.exit(2)` is the apparatus guard at `:89`.  Ledger `probeexitzero` (:47440, MEDIUM, open) records exit-0 as the house idiom, and the EXEMPT comment says the gate block scores rows | none |
| NL6 | Argon | `:58` says "Four controls:" and then lists five (live, seed holds, neg apparatus, disasm xcheck, rldicr) | **LIVE** | READ `:58-73`.  No record mentions it (grep of the ledger, CHANGELOG and OB for "four controls") | a minor L4 in the shipped docstring; fold it into `ppcprobescorestale`'s repair |
| NL7 | grok | `check_probe_wiring.py:1710` says the t2 frozen probe is "byte-identical to the shipped" probe, which has been false since `a05660af` | **LIVE** | READ (re-checked by the prescreen agent): the frozen t2 md5 `7ea10ea4` equals the `a05660af^` blob, and HEAD's probe is `0a0c2f88`.  Neither `a05660af`'s message nor the working-tree diff touches `:1710` | L4 in the manifest text, e.g. "identical as shipped at e777ff06; a05660af changed helper oracles only" (REASONED, from grok's diff note) |
| NL8 | Argon | the probe headers make no clause-(c) claim, "whereas" the ledger says both owe a leg | REFUTED | READ: ledger :62429's title says clause (c) is UNMEASURED and a leg is OWED, so silent headers are consistent with it | none |
| NL9 | Argon | `nullmediumlegs` names only ppc's 2026-10-22 exemption, not alpha's | REFUTED | READ: the :62429 state_note says "their exemptions sit in tools/pipeline/check_probe_wiring.py", covering both.  Only ppc's date is spelled out, which is immaterial | none |

Transport flags (Argon, packet only, not graded): 1.

LIVE (this job): NL6 and NL7.

counts: DISPOSED 5 (5 prior filing) / LIVE 2 / REFUTED 2 / CANNOT SETTLE 0 (9 findings)

## probewiring_three

Files read:
- the brief, grok; Argon `gemini_web.out` (its flags, the three diffs, the controls) and its manifest;
- at HEAD: `check_probe_wiring.py:3092-3102`, `:3240-3290`, `:3411`, `:3566-3632`, `:3865-3873`, `:3930-3946`;
  `precommit_check.sh:540-600`; `dev_sh4.c:1590-1602`; `gate_sh_rounding.sh:1324-1341`;
- a census of the EXEMPT dates; the working-tree diff (+15 MANIFEST lines only);
- ledger rows :59922, :59944 and :59966 (state_notes and entries); `HARNESS_DISPOSITIONS.md:718-723`;
- a census of heredocs and `-c` across `run.sh`, `lib.sh` and the 16 gates; `git ls-tree` of the ip30 probe.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| PW1 | grok, Argon | the heredoc check `ln.strip() == pend` closes `<<WORD` on an indented `  WORD`, and the regex at `:3271` does not tell `<<` from `<<-`, so the data lines that follow count as invocations | **LIVE** (spec) | READ HEAD `:3263-3273`, unchanged in the working tree.  Row `probewiringheredocstrip` is open, NOT FIXED (:59966) | adjudicate grok's `_heredoc_ends` diff.  Argon's diff has a syntax error (`pend_ tab = False`, its `gemini_web.out:64`).  Prefer grok's HEAD-only `fresh()` fixture to Argon's copy of the working regress/.  No committed terminator moves: READ `:900`, `:918` and the two `:165`s are exact column-0 words |
| PW2 | grok, Argon | only `toks[0]` is tested for `-c` (`:3282`), so `python3 -u -c "pass" probe.py` credits probe.py | **LIVE** (spec) | READ `:3281-3283`.  The only `-c` in the battery is at `gate_arm.sh:90`, where `-c` comes first | adjudicate grok's minimal `_c_is_option` (`-m` out of scope) against Argon's first-non-option rewrite (which also covers `-m`, `-`, `-h`, `-V`).  Neither was run |
| PW3 | grok, Argon | the variable map is one pre-pass that keeps only `.py` values (`:3243-3249`) and ignores assignment order | **LIVE** (spec) | READ `:3243-3249`, used at `:3288`.  Every live assignment precedes its use | adjudicate grok's ordered list against Argon's in-loop map with `(\S*)` |
| PW4 | grok, Argon | the rows' citations are stale at HEAD: `:2833-2883` is now `:3243-3309`, and `gate_sh_rounding.sh:1326-1331` is now `:1335-1340` | REFUTED (as wrong records) | READ: the citations sit in verbatim "GOVERNING TEXT" quoted from `HARNESS_DISPOSITIONS.md:720-722`, and the findings were pinned to 798cff34 and 85bc6ab4, where they resolve | none.  The fix commit should cite HEAD constructs and leave the quotes alone |
| PW5 | grok | the BSC "process termination" citation (`dev_sh4.c:1592-1600`) is a comment about the removed `exit(1)`; nothing live terminates | **LIVE** (an already-recorded rule question) | READ: `dev_sh4.c:1590-1602` is the #441 comment.  The three state_notes say "HIGH IS DISPUTED ... A RULE QUESTION for the flagship" | attach it to that severity question; no new filing |
| PW6 | Argon | the EXEMPT entry for `artifacts/ip30abortkill/ip30_abort_probe.py` is dated 2026-10-15.  From today (2026-10-16) the checker reports EXPIRED EXEMPTION, so precommit section R goes red, and so does the checker's selftest M0 when it runs | **LIVE (URGENT)** | READ (re-checked by the prescreen agent): HEAD `:3097-3099` and working-tree `:3112-3114` both carry `"2026-10-15"`.  `elif d < today` is at `:3941`, and `today` defaults to `date.today()` (`:3873`).  Precommit R runs `python "$PWCHK"` with no `--today` (`precommit_check.sh:546`), and M0 (`:3622`) runs a fresh copy the same way.  The red is PREDICTED by reading, not run.  Next due: 10-22 ×2, 10-23, 10-26, 10-27 | before the next commit: re-date it with a reason, or wire the probe (the 09-28 cliff precedent) |
| PW7 | grok, Argon | none of the three fixes moves a gate verdict, because the checker reads scripts, not logs | DISPOSED (immaterial; supports PW1-PW3) | READ the heredoc and `-c` census above; Argon `:16-17` | none |

Transport flags (Argon, packet only, not graded): 3.

LIVE (this job): PW1-PW3 (specs), PW5 (an attached rule question), and **PW6 (URGENT)**.

counts: DISPOSED 1 (1 immaterial) / LIVE 5 / REFUTED 1 / CANNOT SETTLE 0 (7 findings)

## harness_five

Files read:
- the brief, grok, Argon `gemini_web.out` and its manifest;
- the HEAD ledger state_notes at :58888, :59460, :59658, :60208 and :60384;
- `regress/lib.sh:99-120` and `:326-331`;
- `gate_hygiene.sh`, at HEAD and at db8b1a33, at the cited lines (and `:23`);
- `gate_upstream.sh:8-22`, `:73-77`, `:100-145`; `file_elf.c:386-388` (both commits);
- `check_optpin.py:52` and `:93-98`; `gate_offline.sh:483-485` and `:983`; `gate_arm.sh:74` and `:1397`;
  `run.sh:80-96`;
- `diff_wdc_identify.c`, at HEAD, at db8b1a33 and at its working-tree location;
- OB:11864 and :11912 (both commits); WSL `id -u` (read-only); the working-tree `diff --stat`.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| HF1 | grok, Argon | `countunreadable` holds: `count()` echoes 0 when grep fails on an existing file, and the want-0 hygiene rows read that as clean | **LIVE** (spec) | READ `lib.sh:326-331` (re-checked by the prescreen agent); `gate_hygiene.sh:893-897` and `:913-915` | adjudicate it with HF2 and HF3 |
| HF2 | grok | under root `[ -r ]` is always true, so the chmod RED controls in both drafts cannot redden; only grep's status 2 reaches the new branch | **LIVE** (spec) | READ `wsl -d Gentoo -- id -u` = 0, and the battery task runs `wsl.exe -d Gentoo -- bash …nightly_battery.sh` | the RED control must be a status-2 stand-in.  The adjudicators may re-grade the row's HIGH, since its trigger is unreachable under the battery's uid |
| HF3 | grok | both drafts make `count` print a word, but `count` feeds `$(( ))` under `set -u` | **LIVE** (spec) | READ (re-checked by the prescreen agent): `gate_arm.sh:1397` is `"$(( $(count …) + $(count …) ))"`, with `set -u` at `:74`; `run.sh:90-93` scores any exit other than 0/77 as FAIL.  REASONED: the word becomes an unbound-variable abort, so the gate fails loudly but its remaining checks never run | rule it: an abort is acceptable, or use a numeric sentinel plus a status |
| HF4 | grok, Argon | `gateupstreamstatus` holds: there is no pipefail, the status is sed's, and `:114-116` discard it | **LIVE** (spec) | READ `:73-77`, `:114-118`, `:135`; pipefail count 0 (re-checked by the prescreen agent) | adjudicate after HF5 |
| HF5 | grok, Argon | the drafts disagree on what a healthy status is: grok accepts 0 or 124 and wants 0 for every case; Argon wants 0 for the six positive cases and 1 for NonsenseFile | CANNOT SETTLE | READ `gate_upstream.sh:15`: NonsenseFile is a NEGATIVE case, so grok's draft reds if it exits 1.  If grok's 124 reading holds, Argon's draft reds all six positives.  grok says 124 was never executed | one run per case: `timeout 20 <build>/gxemul -V -E <m> <T>/<f> </dev/null >/dev/null 2>&1; echo $?`, for the 7 cases |
| HF6 | grok | the governing text's `file_elf.c:387` is the fprintf; the exit is at `:388` | DISPOSED (immaterial) | READ `:386-388`, the same at both commits | none |
| HF7 | grok, Argon | `hygienesweepmissing` holds: with python3 present and the sweep absent, the gate only notes it and passes | **LIVE** (spec) | READ `gate_hygiene.sh:793-844`; `lib.sh:101` and `:106-120` | rule the scope.  grok degrades the gate only when python is present and the sweep is missing (the Astra-narrowed text, ledger :60384).  Argon also degrades it when python3 is missing, which is wider than the row |
| HF8 | grok, Argon | `optpinor` holds: `:52` accepts any `-fno-` flag, and `:93-98` accept either lane | **LIVE** (spec) | READ.  Both live lanes carry the flag (`gate_offline.sh:483`, `:983`), so nothing flips | adjudicate; the two drafts are equivalent in substance |
| HF9 | grok, Argon | `wdcchildstatus` holds: waitpid's return is ignored, and a non-signalled non-zero exit prints `ok` | **LIVE** (spec) | READ HEAD `:1595-1605`.  The working tree is +555 lines (#563 in flight, other session), but this function is untouched (waitpid at working-tree `:1665`) | adjudicate; land the hunk on #563's working copy |
| HF10 | grok | the governing line ranges miss the code at HEAD (`gate_hygiene :872-879`, `:899-906`, `:790-838`; wdc `:1591-1600`; OB:11864-11879) | REFUTED (as wrong records) | READ: each resolves exactly at db8b1a33, the commit `HARNESS_DISPOSITIONS.md` reviewed; they have drifted since | optional: add "lines as of db8b1a33" to the state_notes |

Transport flags (Argon, packet only, not graded): 4.

LIVE (this job): HF1-HF4 and HF7-HF9 (specs).  HF5 is CANNOT SETTLE.

counts: DISPOSED 1 (1 immaterial) / LIVE 7 / REFUTED 1 / CANNOT SETTLE 1 (10 findings)

## agentrefusal_spec

Files read:
- the brief, grok, Argon `gemini_web.out` and its manifest;
- the HEAD ledger at :52947-52953, :39977, :39988, :40437, :50806, :50925, :54502, :55080 and :58954;
- HEAD OB:22070-22087, :22354-22361, :22484-22492, :24108 and :24170 (and db8b1a33 `:5490-5496`);
- `fable_queue.md:104-111`; `precommit_check.sh:38-46`;
- `_scratchpad/agent_models.py` (on disk) and `lcaisalane/refable_20260919/agent_models_20260919.out`;
- the 40 subagent `meta.json` files of this session;
- `gate_asan_sweep.sh` at HEAD (`:270-300`, `:355-420`, `:488-500`, and a grep for "fifteen");
- `HARNESS_DISPOSITIONS.md:158-165` and `:199-203`; `codex_hbundle_regress10.txt:1-12`; `machine_macppc.c` (HEAD
  grep); `batteryreds/battery_20260829_160646.log:1712-1856`;
- HEAD `nightly_check.sh:40-121`; `README.md`; `git grep nightly_check`;
- `.claude/settings.local.json`; `.claude/hooks/round_reminder.sh` (the shim) and `tools/hooks/round_reminder.sh`;
- `schtasks /query` (read-only); `_scratchpad/nightly/verdict_*.txt`.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| AR1 | grok, Argon | no tracked tool reads `stop_reason` or `model`; the hand-run scorer `_scratchpad/agent_models.py` is untracked and exits 0 whatever it finds | **LIVE** (spec) | READ `agent_models.py:33` (it exits non-zero only when there are no transcripts), `:81`, `:91`.  `git ls-tree e483d931 -- _scratchpad` is empty.  `git grep stop_reason\|thinking_drop -- tools/` hits only the ledger and the matrix.  `fable_queue.md:110` says to check by hand; OB:22085 says "Owed: a tracked checker" | adjudicate the spec (AR6) |
| AR2 | Argon | refusals are printed but never enter flag/bad, so a refuse-and-stop, or a same-model resume, scores `clean` | **LIVE** (spec) | READ `:51-58` vs `:71-81`.  grok's draft has the same gap: `scan()` returns None unless a later turn or a thinking_drop names another model (grok `:86-91`) | the tracked check should fail any refusal not followed by a clean same-model end_turn |
| AR3 | Argon | a missing or unknown `meta.json` `model` makes `fam` None, so MISROUTED is skipped | **LIVE** (spec) | READ `:42`, `:70`, `:73`.  In this session, 2 of 40 `meta.json` files lack `model` and 1 says `sonnet` | treat an unknown requested model as UNVERIFIABLE, not as clean |
| AR4 | Argon | FAILED is excluded from `bad`, yet `:91` says FAILED "is counted separately", and no such counter exists | **LIVE** (spec) | READ `:81`, `:91`.  The out file's `:72-76` show a `<synthetic>` final scored FALLBACK | low: print the count, or drop the clause |
| AR5 | Argon | `PROJ` is hard-coded and the CLI takes only a session id, so fixtures cannot be hermetic | **LIVE** (spec) | READ `:23-34` | low.  Moot if the tracked checker takes paths (grok's does) |
| AR6 | grok, Argon | the spec drafts: grok writes a new tracked `check_agent_refusal.py` plus a precommit G2 that runs only `--selftest`; Argon patches the untracked scratch file | **LIVE** (spec) | READ: the row owes a TRACKED credit gate (OB:22085; ledger :52947 note), so Argon's target cannot discharge it.  REASONED from grok `:161-183`: G2 only proves the file and its fixtures exist, and nothing makes a credit require a scan.  AR2 applies too | adjudicate: a tracked file, invoked at credit time, with a refuse-and-stop row |
| AR7 | grok, Argon | the counts do not reconcile.  The witness (:52953) says "six refusal turns, each followed by a thinking_drop"; OB:22074-22076 says "six agents … thinking_drop"; `agent_models.py:17` says "all five switches" | **LIVE** | READ the out file (re-checked by the prescreen agent): 6 agents FALLBACK (`:90`); 7 REFUSAL lines (`:30`, `:42`, `:44`, `:63`, `:74`, `:79`, `:85`); 6 thinking_drops.  The opus-5 refusal at `:63` (06:59:34) has none | L4 in the witness and in OB: "six agents, seven refusal turns, one (opus-5, 06:59:34) with no thinking_drop", with the out file as the deriver |
| AR8 | grok | the lcalenzerodrop assess refusal (00:24:32Z) is the same agent as both lcaisalane notes, so it is not a fifth refusal | DISPOSED (immaterial) | READ ledger :39977/:39988/:50806 = out `:28-32`; :50925/:40437 = agent aaf391c2.  The title counts five entries, not five refusals | none |
| AR9 | grok | `agent_models.py` is not in e483d931, and the copy on disk (Oct 1; `:34`) post-dates the 09-19 out file | DISPOSED (immaterial) | READ: the witness names the durable out file | none |
| AR10 | grok, Argon | `asanexit1subtype` holds: `:297` turns exit 1 into ok, `:384-393` are skipped, and a sibling satisfies `:374-377`/`:415-418` and `:493`.  The drafts: grok adds a `--classify` stdin mode; Argon reclassifies built=no subtypes as `exit$rc` | **LIVE** (spec) | READ `gate_asan_sweep.sh` at HEAD; the saved table `:1856` says "PASS (16 checks)".  Every built=no subtype is an abort, so neither draft flips it.  Argon's RED control execs `/tmp/gx-asan-head/gxemul.real`, which its recipe never creates (REASONED), and it predicts 12 checks where the log has 16 | adjudicate: grok's control is buildable as written; Argon's is not |
| AR11 | grok | the row's macppc/g4 example is not a live kill: `machine_macppc.c` has no `exit`, `:201` is a subtype registration, and all macppc subtypes are built=yes | DISPOSED (immaterial) | READ `codex_hbundle_regress10.txt:6` states it as a hypothetical fixture; log `:1791-1794`.  No record claims a live death | none |
| AR12 | Argon | the comments' "15/fifteen" vs 12 AB_EXEMPT entries | DISPOSED (prior filing) | `asanfifteen` (ledger :55080; OB:22484-22492).  READ grep: `:42`, `:120-121`, `:138`, `:315`, `:318`, `:356` | none |
| AR13 | grok, Argon | nothing invokes `nightly_check.sh` | **LIVE** (spec) | READ: `git grep` finds only the usage comment and a comment at `check_commit_attribution.py:40`.  The hooks call only the round_reminder shim and wsl_dollar_guard.  `schtasks`: the only GXemul task, `\GXemul-weekly-battery`, runs `nightly_battery.sh` (last run 10/11 18:00, result 0).  That settles grok's "scheduler not queried" | the row is open HIGH (:54502); see AR17 |
| AR14 | grok, Argon | `nightly_check.sh:65` names `GXemul-nightly-battery`; the real task is `GXemul-weekly-battery` | **LIVE** | READ (re-checked by the prescreen agent): `:45` says weekly and `:65` says nightly; `README.md:13`, `:49`; `schtasks`.  Not filed (OB 0, ledger 0); the working tree is unchanged | an L4 one-word fix (both drafts carry it) |
| AR15 | grok | every recent verdict is TREE_DIRTY=YES and `:113-116` FAIL on that, so a caller keyed on NIGHTLY_CHECK_FAIL would be red every week | **LIVE** (spec) | READ (re-checked by the prescreen agent): the 08-30, 09-20, 09-27, 10-04 and 10-11 verdicts are all TREE_DIRTY=YES, 5 of 5.  grok's hook keys on NEVER_RAN, which is right; Argon wires no caller | design input: separate NEVER_RAN from RAN_BADLY, or the switch is permanently red |
| AR16 | Argon | only the newest verdict is checked (`:69-85`), so the 09-06/09-13 gap is invisible now | **LIVE** (spec) | READ `:69-85` | rule whether closure needs gap history, or only a timely invoker (OB:22361) |
| AR17 | grok | the spec: a NIGHTLY_CLASS token, plus a SessionStart hook that `exit 2`s on NEVER_RAN | **LIVE** (spec) | REASONED from grok `:401-427`: the `exit 2` comes before the SessionStart JSON, so the panel-directive reinjection is lost exactly when the alert fires.  READ: the live shim execs the tracked hook, so the target file is right | adjudicate: alert on stderr, and keep emitting the JSON |
| AR18 | grok | OB:22356-22357's "last run 09-20 … next 09-27" is stale | REFUTED (as a defect) | READ: it is a dated 09-24 filing, true at its date | none |

Transport flags (Argon, packet only, not graded): 5.  Argon's OB:24170 one resolves cleanly: the index is "lines as of
db8b1a33" (`:24108`), and db8b1a33 `:5492-5495` is the dead-man-switch passage.

LIVE (this job):
- **agentrefusal:** AR1-AR6 (specs) and the AR7 L4.
- **asanexit1subtype:** AR10.
- **batterymissedruns:** AR13, AR15, AR16 and AR17 (specs), and the AR14 L4.

counts: DISPOSED 4 (3 immaterial, 1 prior filing) / LIVE 13 / REFUTED 1 / CANNOT SETTLE 0 (18 findings)

## adj_8n_regress

agy's answer here is 0 bytes, and ADJ:148 (§5) records the job as NOT LANDED.  These findings are graded against the
committed record of commit e483d931.

Files read:
- the brief, grok, grok-rec, Argon `gemini_web.out` and its manifest;
- at HEAD: CHANGELOG.md:1-40; OB:12-15, :785-799, :20150-20154;
- the ledger at :28375, :28384, :28388, :28586, :28588, :28698, :38043, :38044, :51180, :51182, :51419, :51421 and
  :62453;
- `fable_queue.md:44` and `:63`, at `e483d931^` and at `e483d931`;
- `fable5_regress_devices.md:12-14` and `:95-125`; `offline_out/io_HEAD_armswap.out`; `fq_HEAD.out:35`;
- `pcc2c040kill/opus_mien_20260918/*` and `r535_20260918/opus535/r2_*`.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| BN1 | grok, grok-rec | the `stagetokenscontrols` state_note (:62498) cites `never_reddened.txt` for 13 expectations, but the file has 16 lines | DISPOSED | ADJ:47-48; HV:129; AST1:144-145 | as ruled: a header, or trim it |
| BN2 | grok, grok-rec (Argon called it applied) | the F2.1 annotation says "10 rows red" before the abort, but the log has 17, and `gate_offline.sh` is not named | **LIVE** | READ (re-checked by the prescreen agent): `offline_out/io_HEAD_armswap.out` has 19 FAIL lines, 17 of them not selfcheck rows (`:64`, `:67`, `:73`, `:75`, `:79-82`, `:85-86`, `:92`, `:94`, `:97`, `:99`, `:102`, `:106`, `:110`), with the abort at `:113`.  The "10" appears at OB:20152, ledger :28698, and the review's `:14` and `:98`.  OB:20152 does not name `gate_offline` | L4: 10 becomes 17 at both committed sites, with the review artifact annotated; name `gate_offline.sh` |
| BN3 | grok, grok-rec, Argon | F2.2 ticked diskimagesign in place under "### OPEN" (OB:787-789), against OB's charter "Resolved ones are removed, not annotated" (OB:14) | **LIVE** (ruling) | READ OB:14 and :789, and propagatecpsilent's tick at :799 | ruling: remove both ticked lines, or amend the charter |
| BN4 | grok, grok-rec, Argon | the ledger note at :28588 still says the witness names the cascade directory, and that "the human-facing file was right" | **LIVE** | READ: :28586's re-key against :28588 | L4: date both sentences as history |
| BN5 | grok, grok-rec, Argon | the F5.1 witness (:51419) attributes the 18-row scores to `opus_mien_20260918/`, which holds 16/16, 13/16, 17/17 and 16/17 | **LIVE** | READ the `opus_mien` raw and run files.  `r535_20260918/opus535/r2_A` and `r2_F` are 17/18 and `r2_BASE` is 18/18; the review cites `opus535/` at `:242-244` | L4: cite `r535_20260918/opus535/` and the re-measure |
| BN6 | Argon, grok-rec | CHANGELOG.md:17 credits the review with dating pcc2's hold, but the main loop did it | REFUTED | READ: `:15-17` list it under "Applied in place here", and ledger :51421 says "dated ... by the main loop" | none |
| BN7 | Argon, grok-rec (asks for a ruling) | CHANGELOG.md:14-15 says "every finding a record, none a defect in shipped code", though three harness gaps were filed | **LIVE** (ruling) | READ: the sentence is at `:14-15` (Argon's `:11-12` is wrong).  The review's `:12` grades finding 3 as coverage debt, and the same block names the filings at `:19-26`.  The commit message repeats the sentence and cannot change | a minor wording ruling, e.g. qualify it to "none in src/" |
| BN8 | Argon, grok-rec | `fablequeueregress` (:62453) gives "(2 at HEAD)" and "20 regress:fable5 holds" with no date or unit | **LIVE** | READ `fq_HEAD.out:35`: the wall line had 20 solo / 21 total before the commit, and 19 / 20 at e483d931 | minor L4: "at a05660af; 20 = solo tags" |
| BN9 | Argon (grok-rec: NEITHER) | 11/128 and 12/128 are failure counts, printed beside pass-count fractions | **LIVE** | READ CHANGELOG.md:10, next to `:14`'s 17/18; ledger :27984; `wdc_HEAD_*.out:446/:448` say "11/12 failures" | minor L4: add "red" to both |
| BN10 | Argon, grok-rec | the :51182 outcome_note still says "48/48 with 32 killed" | REFUTED | READ: it describes what the 09-18 entry recorded and adds "before adding one more fixture", consistent with :51180's correction | none |
| BN11 | Argon, grok-rec | the sgirergb state_note (:38044) still says the 10-row prefix re-measure was "Recorded, not re-run" | **LIVE** | READ :38044.  :38043 now cites `killtable6_20260907/prefix10row.raw` (4/10) and the 10-09 re-measure | minor L4: date the sentence as overtaken |
| BN12 | Argon | the landiskaux witness (:28388) omits 1/6 → 6/6, while :28375 says 8/17 → 17/17 | REFUTED | READ: these are two instruments, the rung-3 lax_probe (17 rows) and the 6-row detector (:28384); no number conflicts | none |
| BN13 | Argon | heldmasked "reds 7 expectations" against 42/49 | REFUTED | REASONED: 49 − 42 = 7 (grok-rec READ `controls_HEAD.out:12`) | none |
| BN14 | grok-rec | the seats' tallies disagree | DISPOSED (immaterial) | seat-answer arithmetic only | none |
| BN15 | grok, Argon | the wdcaltctrlbit note adds 12/128 but keeps the 867c697 96-row counts | REFUTED (as a defect) | READ: the review's verdict `:13` carries both, and the old counts are dated 2026-08-27 | none |
| BN16 | grok | dashokclass's 439/365 counts have no artifact | DISPOSED | ADJ:44 (F3 VERIFIED); AST1:134 | none |
| BN17 | Argon | the sgirergb witness keeps the cross-instrument pair 4/6 → 10/10 | REFUTED (as a defect) | READ: :38043 itself says "the denominators differ", and the 10-09 bracket adds the same-script pair | none |

Confirmations, not graded: the commit's six score pairs match their artifacts (grok and grok-rec).

Transport flags (Argon, packet only, not graded): 6.  Their record halves are graded above.

LIVE (this job): BN2, BN3, BN4, BN5, BN7, BN8, BN9 and BN11.

counts: DISPOSED 3 (1 immaterial) / LIVE 8 / REFUTED 6 / CANNOT SETTLE 0 (17 findings)

## adj_pcc2_ruling

ADJ:148 (§5) records this job NOT LANDED for agy.  Findings are graded against the ruling files and the e483d931
record.

Files read:
- the brief, grok (grok compacted mid-task), grok-rec, Argon `gemini_web.out` and its manifest;
- the ledger at :42685-42712, :42749-42785, :42807 and :62471, plus the 10 sibling lines; the seat catalog at :55-90
  (HEAD and the working tree);
- CHANGELOG.md:40-54; the e483d931 commit message; `fable_queue.md:44`, `:112`, `:2585`;
- the v1/v2/v3 ruling files and `RULING_PROVENANCE.txt`; `build_and_run.sh.txt`; `repaired_M_return.raw`;
- HEAD `panel.sh` (`:175`, `:218`); the working-tree diff of `dev_pcc2.c`; the md5s of the frozen and HEAD probes;
- a grep for the owner's answer across CK, memory and the artifacts.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| PC1 | grok, grok-rec, Argon | v3:50 says to record the four re-fired answers as packet-fed MANUAL entries, but the committed grades are verdict strings | **LIVE** | READ (re-checked by the prescreen agent): :42755, :42764, :42773 and :42782 are graded `ROW OWED`, `ROW OWED`, `CLOSED (refuted in part by measurement)` and `ROW OWED`, while the same row's 09-17 entries (:42685-:42712) say "MANUAL" | re-grade them to MANUAL with the verdict kept in the note, or rule that verdict strings stand |
| PC2 | grok, grok-rec, Argon | entry [11] (:42749) still opens with the live literal `[HELD AWAITING SEAT: glm, deepseek, minimax, kimi]`, although v3:49 says "Clear the HELD marker" | **LIVE** | READ :42749 (re-checked by the prescreen agent) and v3:49.  It has no tool effect today: the strictly-later rule discharges it, and the generated wall at `fable_queue.md:44` omits the id | defang it in place (the carrier's quoted-marker rule) |
| PC3 | grok, grok-rec | the record says "caught by c040 noassert, 9/10 and 14/16", but on the 16-row table two rows are red | **LIVE** | READ `repaired_M_return.raw:13-14` FAIL and `:21` 14/16.  The phrase sits at ledger :42697 and :42807, CHANGELOG.md:43 and v3:49 | minor L4: "14/16, with noassert and noassert2 red" |
| PC4 | grok, grok-rec, Argon | the owner's answer "KEEP THE WRITTEN RULE" is recorded with no source in the packet, while v3 leaves the question open | CANNOT SETTLE | READ: :62471 names "AskUserQuestion, 2026-10-09", and the commit message's `:26` repeats it.  v3 deferring to the owner is a sequence of events, not a contradiction.  A grep of CK, memory and the artifacts finds nothing | one read of the 10-09 session's AskUserQuestion exchange, or a one-line owner confirmation |
| PC5 | grok, grok-rec, Argon | the comment at `dev_pcc2.c:377-378` at HEAD still says the return mutant passes every shipped row | DISPOSED | ADJ:116 (§3 row 2, place22); AST1:165.  READ: the working tree carries +20 lines at `@@ -377` (peer) | lands with the held #560/#561 comment batch |
| PC6 | grok, grok-rec | the deepseek and kimi notes say "MEASURED 18/18" without naming the main loop as the measurer, and paraphrase "all 13" as "every row" | **LIVE** | READ :42758 names the main loop; :42767 says "13-row instrument inlined"; :42785 | minor L4: "by the main loop"; "all 13 (packet)" |
| PC7 | grok, grok-rec, Argon | `build_and_run.sh.txt:2` says "13 rows", and :42807 cites it rather than `run.out` | REFUTED | READ: :42807 cites `probe_*.raw`, whose `:23` lines carry the 18/18 results.  The script header is stale text inside an untracked receipt | none |
| PC8 | grok, grok-rec | the grader model strings `glm-5.3:cloud` and `kimi-k3:cloud` appear nowhere in the panel and disagree with the seat catalog | REFUTED | READ HEAD `panel.sh:175` `OLLAMA1="glm-5.3:cloud"` and `:218` `OLLAMA4="kimi-k3:cloud"`: these are the transports that actually fired | none for the graders |
| PC9 | grok | (aside) the ledger's seat catalog still says `glm-5.2:cloud` | **LIVE** | READ catalog `:66`/`:70`, at HEAD and in the working tree; stale since the 08-29 migration | minor L4 in the catalog |
| PC10 | grok, grok-rec | the L4 sits only on :42697 and :42706, while the same refuted 09-17 sentences stand on five other rows | **LIVE** | READ :19391/:19402 (sh4dmacie), :21919/:21930 (gdromdmadefault), :24848/:24859 (lethalonly), :28643/:28654 (diskimagesign), :42894/:42903 (pcc2genctlc040alias) | annotate the 10 copies (the carrier's "grep for siblings" rule), or rule them out of scope |
| PC11 | grok | v2:44 says all four seats flagged the stale comment, but deepseek did not | DISPOSED (immaterial) | v3 supersedes v2, and no record repeats the sentence | none |
| PC12 | Argon | v2:15 and v3:5 cite a pre-copy v1 name and a scratchpad Astra path | DISPOSED (immaterial) | READ `RULING_PROVENANCE.txt:1-3` maps both | none |
| PC13 | Argon (grok-rec: grok right) | `c040 recover`'s final write enters the arm with assert == 1 | DISPOSED (immaterial) | READ probe `:542`: `then_genctl` 0x02 lacks C040 (0x04).  A seat correction | none |

Confirmations, not graded: the product facts, the 18/18 runs, the seat split, and frozen probe == HEAD probe (md5
1c09f729).

Transport flags (Argon, packet only, not graded): 7.

LIVE (this job): PC1, PC2, PC3, PC6, PC9 and PC10.  PC4 is CANNOT SETTLE.

counts: DISPOSED 4 (3 immaterial) / LIVE 6 / REFUTED 2 / CANNOT SETTLE 1 (13 findings)

## nullmedium_census (grok only; Argon skipped it by design)

Files read:
- the brief, grok (grok compacted mid-task); ledger `nullmediumsweep` :62438;
- `fablequeue7n_20261009/fable5_rule7n_12.md:20-70` and `:100-106`; the 23012be9 commit message;
- `check_probe_wiring.py:1627-1640`, `:1703`, `:1765`, `:1780`, `:1849`, `:3059`;
- CHANGELOG at HEAD: `:4577`, `:5259`, `:5535`, `:15978`, `:17255`, `:17486`, `:17605`;
- these artifacts:
  - `lcabadval`: `killtable_20260910/PRETABLE.out:88-95`, plus a grep of `killtable5`;
  - `lcaisalane`: `table7/PRETABLE.out:72-78`;
  - `wdcaltdigin`: `mutate_altdigin.py:44-52`;
  - `armbdt`: `killtable_20260911`'s PRETABLE and SCORES;
  - `wdcdataoutdrain`: `TABLE.txt:39-43`;
  - `ppcrldimimask`: `PRETABLE.out:64-72`, `SCORES.txt:52-56`;
  - the two identity-body mutators;
  - `sgimtedepth4dead`: `repair_20260909/PRETABLE.out:150-157`;
  - `wdccmdreset`'s `TABLE.txt`;
- `X(rlwimi)` at HEAD;
- a read-only directory walk of `regress/artifacts/`.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| NC1 | grok | the census: 87 qualifying directories; 30 carry a clause-(c) label; 7 of those are pre-fix legs; 57 have no clause-(c) leg | **LIVE** | READ: a walk with grok's own criterion reproduces 87, 32 of them after `scexempt/`, so the "listing truncated" worry did not change the count.  `nullmediumsweep` (:62438) is still open with no durable artifact | adopt it as the draft census, with a written deriver, at a durable path |
| NC2 | grok | 87 does not reconcile with "~165", and no "~16" list exists | DISPOSED (prior record) | READ the `nullmediumsweep` state_note; `fable5_rule7n_12.md:27` and `:102` (item 3) already say neither list exists | none |
| NC3 | grok | pre-fix legs labelled "null medium" on alphatbinegsel, mk48nvramkill, ppcrldiclzero, ppcrldimimask and sgirandomcolour (killtable, killtable3, and killtable4's M11_null) | DISPOSED (prior record) | READ: the 23012be9 L4s (CHANGELOG blocks and witness fields; the four descriptions at `check_probe_wiring.py:1703/:1765/:1780/:1849`); ppcrldimimask's in-file correction at `PRETABLE.out:69-72` and `SCORES.txt:54`; 7n-1.5 items 1-2 | none; the artifacts' driver lines stay as receipts |
| NC4 | grok | `lcabadval/killtable_20260910/PRETABLE.out:93-94` labels M22_null "the null medium here is the PRE-FIX file" | **LIVE** | READ the label (re-checked by the prescreen agent).  7n-1 found no clause-(c) claim in #518's committed block, and said lcabadval enters the population "only if the sweep artifact says why" (`fable5_rule7n_12.md:27`); this census says why.  `killtable5` has no clause-(c) leg (grep: none).  `lca_badval_probe.py` is run by no gate and is EXEMPT until 2026-10-23 (`check_probe_wiring.py:3059`) | one L4 sentence in the artifact.  By 7n-1.4 a measured leg is owed, which makes a third member beside `nullmediumlegs`' two (REASONED).  The row is peer-owned (dev_lca.c rows) |
| NC5 | grok | `ppcrlwimiwidth/killtable_20260911`'s NULL_MEDIUM 28/28 was byte-identical to BASE | DISPOSED (prior record) | READ CHANGELOG.md:4577; 7n-1.3 item 3 and 7n-1.5 item 1 (released) | none |
| NC6 | grok | six 2026-08-27 `Mc_null` "compile failed" tables never say what the medium was | REFUTED | READ CHANGELOG.md:17605 (#473): "comment-only source, caught at compile".  `:17486`, `:17255` and `:15978` say compile failure.  Sibling `wdcdataoutdrain TABLE.txt:41-42` says "comment-only dev_wdc.c", and 7n-1.2 cites wdcchunking's Mc_null | classify these as comment-only in the census |
| NC7 | grok | wdcaltdigin's `M_NULL_MEDIUM` is a read stub (`data[0]=0; return 1;`), none of the named media, yet the round claims floor clause (c) on it | **LIVE** (ruling) | READ `mutate_altdigin.py:49-52`; CHANGELOG.md:5535 "(c) M_NULL_MEDIUM fails the accept rows" | ruling: either the stub counts as the device-absent analogue, or it is a mislabel that owes an L4 plus the by-construction reading |
| NC8 | grok | `lcaisalane/table7` calls the noff (`dev_8253.c`) and nox (`dev_pckbc.c`) negative controls "IDENTITY ROWS (floor clause (c))" | **LIVE** (ruling) | READ `PRETABLE.out:75-78`.  The committed CHANGELOG never mentions noff or nox | ruling: channel controls are not a null product medium under the 10-09 clause-(c) block, so an L4 is owed in the artifact.  Peer-owned (#530) |
| NC9 | grok | armbdt predicted 4/25 for M_NULL_MEDIUM and measured 6/25 | DISPOSED (prior record) | READ CHANGELOG.md:5259 records the miss | none |
| NC10 | grok | mk48's M_NULL (a clause-(d) null repair) sits beside a HEAD leg labelled "null medium", and M_NULL as run differed (`PRETABLE.out:250`) | DISPOSED (prior record) | READ `fable5_rule7n_12.md:104` item 5; the CHANGELOG.md:5884 L4 | none |
| NC11 | grok | the rlwimi identity block is shorter than rldimi's | DISPOSED (immaterial) | READ: `X(rlwimi)`'s tail `reg(ic->arg[1]) = ra;` writes `ra` back unchanged, so both are identity bodies; 7n-1.1 released both measured legs | none |
| NC12 | grok | the census filter excludes real clause-(c) receipts: `shortread/nullmedium_20261009`, widthkillclass's `/bin/true`, asiceventaddr build/pass1, sgimtedepth4dead NULL_dead, `PRETABLE2-7.out`, `PRETABLE13a-16.out`, `TABLE1.txt`, `SCORES3/4.txt`, fix530 | **LIVE** | READ the brief's filter at `:16-17`; `sgimtedepth4dead PRETABLE.out:153-157` | the durable deriver must match numbered filenames and directories not named "table", or the population undercounts |
| NC13 | grok | 13 flags exclude incidental tokens ("option (c)", "comment-only" edits, "IDENTITY PIN", M0_identity, asic's family-d "null" row, ...), plus method notes | DISPOSED (immaterial) | census bookkeeping, with no record consequence | none |

LIVE (this job): NC1, NC4, NC7, NC8 and NC12.

counts: DISPOSED 7 (2 immaterial, 5 prior record) / LIVE 5 / REFUTED 1 / CANNOT SETTLE 0 (13 findings)

## LIVE items for the adjudicators

93 LIVE findings, grouped by the decision each needs.  Each entry says what it applies to and what the change would be.
The ids point at the job tables above.

### 1. Time-bound: blocks the next commit

**PW6.**  The EXEMPT entry for `artifacts/ip30abortkill/ip30_abort_probe.py` in
`tools/pipeline/check_probe_wiring.py` is dated 2026-10-15 (HEAD `:3097-3099`, working tree `:3112-3114`).  With
`date.today()` = 2026-10-16:
- precommit section R reports EXPIRED EXEMPTION;
- so does the checker's selftest M0, when it runs.

This is PREDICTED by reading; nothing was run.  Change: re-date the entry with a reason, or wire the probe, before
any commit.  The next expiries:
- 2026-10-22 ×2: `ppc_rldicl_probe.py` and `alpha_tbi_probe.py` (NL1, owned by `wiringcliff`);
- 2026-10-23: `lca_badval_probe.py` (NC4);
- 2026-10-26 and 2026-10-27.

### 2. Held fix specs with new deciding evidence (ADJ v2 / AST2 left them open)

- **CX3, `cxlaunchquotation`.**  HEAD `tools/cxlaunch.sh` decides the wall (`:56`) before it tests rc (`:58`).
  - Option B is refuted by AST2's final550: rc 0, with usage-limit lines quoted in stderr.
  - PL's gate, "classify only when rc != 0 or stdout is empty" (PL:61-74), has never been ruled.

  Change: rule PL's gate for the tracked launcher.  Its fixtures must carry rc: the four v2.2 fixtures, final550, and
  a real wall.  Merge with OB `cxlaunchwallfp` (prescreen note below).
- **SV11, `tools/panel.sh` seat check.**  `check()` (`:568`) and the tally (`:708-709`) score a content-filter-refused
  codex `answered`; see `SEATS.txt:2` of both refused panels.  The v3 scorer fixes only `seat_verdicts.py`.

  Change: file a sibling of `seatverdictrefusal` (a terminal codex-refusal test in `panel.sh`), or record that
  `SEATS.txt` is not authoritative for refusals.  `panel.sh` is on CK's never-commit list.

### 3. Fix specs never adjudicated (set 4): the rows hold by reading; choose between the drafts

- **agentrefusal** (AR1-AR6).  No tracked credit gate exists: `_scratchpad/agent_models.py` is untracked and exits 0
  whatever it finds.
  - grok's draft adds a G2 that runs only `--selftest`; Argon's patches the untracked file (AR6).
  - Both drafts miss three cases: refuse-and-stop (AR2), an unknown requested model (AR3), and the FAILED count (AR4).
  - Fixtures cannot be hermetic (AR5).
- **asanexit1subtype** (AR10).  grok's RED control is buildable and Argon's is not.  Neither draft flips the saved
  16-check table.
- **batterymissedruns** (AR13, AR15-AR17).
  - Nothing invokes `nightly_check.sh`.
  - All five verdicts since 08-30 are TREE_DIRTY=YES, so a caller keyed on FAIL would be red every week.
  - Should closure check gap history, or only the newest verdict?
  - grok's SessionStart hook does `exit 2` before it emits the JSON.
- **harness_five** (HF1-HF4, HF7-HF9).
  - `count()` returns 0 on an unreadable log (HF1).  The RED control cannot be built under root (HF2), and a word
    token aborts `$(( ))` under `set -u` (HF3).
  - `gate_upstream.sh` loses its pipe status (HF4).  HF5 needs one run per case first.
  - The hygiene-sweep scope differs: Argon's draft is wider than the row (HF7).
  - `optpinor`: the two drafts are equivalent (HF8).
  - `wdcchildstatus`: land the hunk on #563's working copy (HF9).
- **probewiring** (PW1-PW3): the heredoc indent and `<<-`, the `-c` position, and the variable map.
  - Argon's heredoc diff does not compile, and neither `-c` draft was run.
  - PW5 attaches grok's BSC point to the HIGH-severity rule question already recorded.

### 4. Open owner rule questions (recommendations only, unchanged since 10-13)

- **D2** (CD5-CD8).
  - The WDC exemplar's 32769/32767 rows come from the 137-row extension.
  - "`< 97` detected at 96" is derived: no `< 97` medium exists.
  - §C7's CHANNEL `> B-1` is the EQUIVALENT mutant at a clamp; the move that reddens is `> B-2`.
  - "Every one-token move" overclaims: four moves were measured.
- **ROUTE PARITY** (CD10, CD13).
  - The row's own "catches" cell describes a row-kind gap, and the corollary uses a name census.  Both contradict the
    sentence's "not of row kinds" and "matching names discharge nothing".
  - The two recorded route bounds differ: the enclosing function (HV:138-139, ADJ:143) against the block or file
    (HV:161-163, ASICADJ:543-548).

### 5. Rulings asked for (more than a records fix)

- **PS3** (with PS2 and PS4).  The seat columns of `regress/pass2_ledger.tsv` are not a schema:
  - titles sit in seats-answering, and prose in seats-READ;
  - there are no seat cells after 2026-08-31;
  - only section F reads the file.

  Change: annotate the header, or file a row.  No retro-fill.
- **BN3.**  OB's "### OPEN" lines are ticked in place (diskimagesign, propagatecpsilent), against its charter
  "removed, not annotated" (OB:14).
- **BN7.**  CHANGELOG.md:14-15 says "none a defect in shipped code" beside three filed harness gaps.  Qualify it.
- **NC7.**  wdcaltdigin's read stub (`data[0]=0; return 1;`) is claimed as clause (c).  Either it is an admissible
  device-absent analogue, or it owes an L4.
- **NC8** (peer-owned, #530).  The lcaisalane table7 channel controls noff/nox are labelled clause (c).  An L4 is owed
  in the artifact.

### 6. Records corrections (L4 class), not yet ruled

**Carrier** (root `CLAUDE.md`, identical to the working `tools/CLAUDE.md`):
- **CC1, CC2, CC4-CC15:** 14 stale cross-file line citations.  Re-key them to grep anchors (the citation-form rule).
- **CN2-CN4, CN6, CN7, CN12, CN17:** decayed counts.  File them per the counts rule, with no sweep.
  - The marker census is now 92/14/56.5%, and its "13 spellings" self-check misfires on a comment-wrapped marker.
  - Latch sites: 28 in 13 files.  Wall-clock oracles: 55 in 31 files.
  - The `sgirekills` census is off by +35 lines and now has 7 comment texts.
  - Gate 14 reads `PASS (1110 checks)`, not 358.
- **CN13-CN16 and CD22:** the PDF inventory.
  - The carrier says "FIFTEEN"; its list holds 19; there are 20 on disk, and 26 counting `lance/`.
  - `ata2_x3t10_948d` is missing, though `dev_wdc.c:640` cites it.
  - 4 extracted txt files are unlisted.
- **CD17:** push lines sit under the LOCAL GIT ONLY directive.
- **CD19:** the Codex row's header still says "(xhigh)".  Fold it into ADJ:101's `:782` L4.
- **CD21:** "SIX MEMBERS" heads a list of seven.

**Product source comment:**
- **CC16:** `src/cpus/cpu_sh.c:458` cites `dev_sh4.c:2386-2388`.  That line is now `case SH4_RTCOR:`; the IRLM refusal
  is at `:2507-2509`.  A src edit owes four-tree propagation and the two-part clearance.

**Adjudication and harvest records:**
- **E54:** ADJ:271 (v2.6) and HV:226 say regress/ edits owe est/ byte-identity, but `est/` has no `regress/`.
  Erratum.
- **E53:** held correction #1's text cites `OUTSTANDING_BUGS.md:14809-14812`; the paragraph is now at `:14821`.
  Re-key it before applying.

**Ledger, OB and CHANGELOG (batch 8n, e483d931):**
- **BN2:** "10 rows red" should be 17, at OB:20152 and ledger :28698; name `gate_offline.sh`.
- **BN4:** the stale sentences at :28588.
- **BN5:** :51419 credits `opus_mien_20260918/` with the 18-row scores; they are in `r535_20260918/opus535/`.
- **BN8:** the undated count at :62453.
- **BN9:** 11/128 and 12/128 are failure counts.
- **BN11:** :38044's "Recorded, not re-run" has been overtaken.

**The pcc2 C040 ruling record:**
- **PC1:** the four re-fired grades are verdict strings; v3:50 asked for MANUAL.
- **PC2:** entry [11] at :42749 still opens with a live `[HELD AWAITING SEAT: ...]` literal.  Defang it.
- **PC3:** "14/16" hides two red rows.
- **PC6:** the 18/18 notes do not name who measured.
- **PC9:** the seat catalog still says glm-5.2.
- **PC10:** ten refuted 09-17 sentences remain on five sibling rows.

**Harness text and tool records:**
- **AR7:** the agentrefusal witness and OB say six refusal turns; there are six agents and seven refusal turns.
- **AR14:** `nightly_check.sh:65` names a task that does not exist (`GXemul-nightly-battery`).
- **PS5:** three receipts are split by raw newlines.  R8's "same line" erratum would land mid-record; put it at `:94`.
- **PS6:** section F's `grep "^$PREV"` uses a full SHA and never prints.
- **DA13:** `run_controls.py:16-17` says "48/48" on a 49-row instrument, and its log exists nowhere.
- **NL6:** the ppc probe's "Four controls" lists five.
- **NL7:** `check_probe_wiring.py:1710`'s "byte-identical" has been false since a05660af.
- **CX15:** `panel.sh`'s echo-branch `wall:` reason is brief text.  Fold it into `panelwallquote`.

**The clause-(c) census:**
- **NC1 and NC12:** adopt the 87-directory census, with a written deriver widened beyond the brief's filename filter,
  at a durable path.
- **NC4** (peer-owned): lcabadval's M22_null is labelled a null medium but is a pre-fix leg.  This implies a third
  owed leg.

### Records consequences of DISPOSED findings (not counted as LIVE)

- **DA8:** ledger :62507 and OB:24712-24713 still offer the rejected one-line `"OK": "ok"` mapping, with its DASH-row
  control.
- **CX7:** OB:24716 and ledger :62489 still prescribe Option A.  ADJ:232 said to correct both to B, which AST2 then
  refuted.  Correct them to whatever v3 adopts.
- **CD11:** ADJ:60 (F6, "VERIFIED") still stands for "routes"; AST1:229 refuted it.  Carry the erratum.

### Prescreen notes (derived here; no seat raised them)

- **`cxlaunchwallfp`:** OB:22494-22503 (filed 2026-09-26) already names both halves of the cxlaunch class.  It has no
  ledger row, and neither ADJ nor AST cites it.
- **`tools/pipeline/codex_answer.py`:** its `blocks()` (`:48-55`, `:98`) applies the header-to-`exec` rule that
  ADJ:192 withdrew.  An in-memory replica finds 0 verdict blocks in 6 of the 9 healthy transcripts ADJ:192 lists.  It
  is a hand tool for `.err` streams, so no ruling is proposed.
- **Outside this group:** `_scratchpad/panel_20260921_154943` (full codex, agy and grok answers) is cited by neither
  the ledger nor OB at HEAD.  CK's peer section names it as #544's pass-5 panel.  A possible section-G unread-review
  candidate (peer-owned).

## Counts

| job | DISPOSED (of which immaterial / prior filing or record) | LIVE | REFUTED | CANNOT SETTLE | findings | Argon transport flags (not graded) |
|---|---|---|---|---|---|---|
| seatverdict_refusal | 14 (3 / 0) | 1 | 3 | 0 | 18 | 4 |
| cxlaunch_quota | 11 (2 / 1) | 2 | 3 | 0 | 16 | 1 |
| dash_okclass | 10 (3 / 0) | 1 | 2 | 0 | 13 | 3 |
| stagetokens_controls | 8 (2 / 0) | 0 | 0 | 0 | 8 | 4 |
| edits560 | 3 (0 / 0) | 2 | 1 | 0 | 6 | 29 |
| carrier_citations | 2 (1 / 0) | 15 | 3 | 0 | 20 | 36 |
| carrier_counts | 4 (2 / 0) | 11 | 4 | 0 | 19 | 5 |
| carrier_d2_texts | 13 (1 / 0) | 10 | 0 | 0 | 23 | 0 |
| pass2ledger_schema | 3 (1 / 0) | 5 | 9 | 0 | 17 | 1 |
| nullmediumlegs_wiring | 5 (0 / 5) | 2 | 2 | 0 | 9 | 1 |
| probewiring_three | 1 (1 / 0) | 5 | 1 | 0 | 7 | 3 |
| harness_five | 1 (1 / 0) | 7 | 1 | 1 | 10 | 4 |
| agentrefusal_spec | 4 (3 / 1) | 13 | 1 | 0 | 18 | 5 |
| adj_8n_regress | 3 (1 / 0) | 8 | 6 | 0 | 17 | 6 |
| adj_pcc2_ruling | 4 (3 / 0) | 6 | 2 | 1 | 13 | 7 |
| nullmedium_census | 7 (2 / 5) | 5 | 1 | 0 | 13 | n/a (grok only) |
| **total** | **93 (26 / 12)** | **93** | **39** | **2** | **227** | **109** |

How the 93 LIVE break down:
- 1 time-bound (PW6);
- 2 held specs with new evidence (CX3, SV11);
- 22 never-adjudicated spec items: AR ×11, HF ×7, PW1-PW3, plus PW5;
- 6 for owner rule questions (D2 ×4, ROUTE PARITY ×2);
- 7 ruling requests (PS2, PS3, PS4, BN3, BN7, NC7, NC8);
- 55 records corrections.

DISPOSED strictly by HV, ADJ v1/v2 or AST1/AST2: 55 of the 93.  The other 38 are the immaterial and prior-record
qualifiers named in the column.

The two CANNOT SETTLE items, each settled by one action:
- **HF5:** one `timeout 20 <build>/gxemul -V -E <m> <T>/<f>; echo $?` per `gate_upstream.sh` case.
- **PC4:** one read of the 2026-10-09 AskUserQuestion exchange, or a one-line owner confirmation.

Ledger rows: `seatverdictrefusal` is ABSENT, and so is `wdczerolendatain`.  Both are owed filings (see the top of this
file).
