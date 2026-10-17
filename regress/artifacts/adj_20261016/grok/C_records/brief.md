# Grok adjudicator -- packet C (READ-ONLY; plan mode)

Open with the token `GROK_ADJ_C_20261016`.  You are one of three independent adjudicators (Grok 4.7, Fable 5.1, GPT-6 Astra).  The packet follows in full; every file it cites is on disk under C:/DocumentNoSnc/cc/GXEMUL -- open what you rely on, say READ vs REASONED, and answer its QUESTIONS section exactly as it directs, VERDICT LINE FIRST.  The tree under review is GXEMUL-SEC at HEAD e483d931 (`git show e483d931:<path>`); the working tree carries two sessions' uncommitted edits (dev_wdc.c is not one of them); ignore the project root's pristine 2021 `src/`.  Write nothing.

---

# ADJUDICATION PACKET C -- records and harness: what Astra's v2 REJECT left open, plus the pending filings

Prepared 2026-10-16 ~11:5x CDT by the main loop (Opus 5.5, session 087a90).  Owner directive of 2026-10-16:
**"Adjudicate any pending findings with both the Fable, Astra, and Grok."**  Three adjudicators answer independently:
Fable 5.1 (Agent seat), GPT-6 Astra (codex, ultra), Grok 4.7 (xhigh, plan mode).  An ordinary records and test-harness
review.  **READ-ONLY: write nothing to any project tree.**

## 0. Ground rules

- Repo `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` at HEAD **e483d931** (`git show e483d931:<path>` for committed text;
  the working tree carries two sessions' uncommitted edits, including `tools/pipeline/ledger.json`, `tools/panel.sh`,
  `tools/BRIEF_TEMPLATE.md`, `tools/CLAUDE.md`).  Never read the project root's pristine `src/`.
- The records adjudication under review: `GXEMUL-SEC/regress/artifacts/recordfix_20261013/adj_20261013/` --
  `fable5_records_adjudication.md` (v1 sections 0-6; v2 reconciliation from its line 164), receipts in `v2/ v3/ cxctl/
  launcherctl/ panels/ agyprobe/`, Astra's answers `astra/codex_recadj.txt` (REJECT) and `astra_v2/codex_recadjv2.txt`
  (REJECT narrowly).  Call that directory **RA** below.
- New receipts made today by the main loop (durable): `GXEMUL-SEC/regress/artifacts/adj_20261016/cxctl_optionC/`
  (RECEIPT.txt, the frozen launcher, the fake codex) and `.../adj_20261016/agyprobe_rc/` (rc-captured agy probes,
  MANIFEST.md5).
- Separate READ / REASONED / MEASURED.  Count arguments, not seats.

## 1. Findings F1..F10 with MY DISPOSITION

**F1. `cxlaunchquotation` -- Option B is refuted; replace it with the rule the production launcher already runs.**
Astra v2 (RA `astra_v2/codex_recadjv2.txt` item 1): `exemptredate_20260925/final550/` is an rc-0 run with a complete
answer whose stderr carries SIX line-start `ERROR: You've hit your usage limit` lines QUOTED from old transcripts codex
read (`codex_astra550.err` ~:5625-5892; its launch receipt `astra550.launch.log` says `SEAT WALLED`); Option B (count
wall words in stderr `ERROR:` lines only) still walls it.  **MINE: ACCEPT the refutation.**  The fix already exists and
has run every Astra job since 2026-09-26: `_scratchpad/codexpack_20260928/cxlaunch_pack.sh` (frozen copies
`cxlaunch_pack.run-*.sh`; header "cxlaunch_u.sh") classifies a run by its `ERROR:` lines ONLY when `rc != 0` or stdout
is empty, and treats rc 0 with an answer as an answer ("note: N ERROR:-shaped line(s) in stderr IGNORED").  Its own
comment records why: astra549, astra550 and rec529audit (rc 0; 11,472 / 4,265 / 13,442 bytes) were reported WALLED by
the anchored form.  **MEASURED TODAY** (`adj_20261016/cxctl_optionC/RECEIPT.txt`, the frozen launcher driven by a fake
codex through its `CX_CODEX_BIN` override):

| fixture (rc, stdout, stderr `ERROR:` lines) | launcher exit | reading |
|---|---|---|
| P1 real wall (1, 0 b, 2 -- `panel_20260925_151610/codex.txt:15-16`) | 8 | WALLED -- right |
| P2 real refusal (1, 0 b, 1 "flagged for possible cybersecurity risk") | 7 | REFUSED -- right |
| N1 final550 (0, 4,265 b, 6 quoted) | 0 | answered -- right (Option B: walled) |
| N2 verdict-less quota prose (0, 100 b, 0) | 0 | answered -- right |
| N3 empty (0, 0 b, 0) | 6 | seat down -- right |
| N4 SYNTHETIC: rc 1 WITH final550's answer and its 6 quoted lines | 8 | WALLED -- a residual misread |

**Disposition: land the production rule into the tracked `tools/cxlaunch.sh`** (which also brings `ultra` and the
Daybreak AUP fallback the carrier row and `panel.sh` already describe -- closing `cxlaunchdaybreak`); rewrite its
`:41` comment; correct OUTSTANDING_BUGS.md:24714-24716 and the ledger row (:62489 per v2) from Option A/B to this rule;
the six fixtures become its controls; **N4 is recorded as the residual** (no real instance on record: every real wall
and refusal in the launch logs is rc 1 with empty stdout).  Question in D1.

**F2. `dashokclass` -- every mechanical sweep is withdrawn.**  Astra v2 item 2: the v2 "mechanically safe 262"
predicate passes `wdcatapistswap/review/deepseek`, whose ledger note is `REJECT-AS-WRITTEN` (HEAD ledger.json ~:29552)
-- an objection would be rendered as approval; the literal predicate gives 272/167, not 262/177; the covered-by-
substitute kimi entries are 11, not 7.  **MINE: ACCEPT.**  New disposition: (a) no batch rewrite of any `"d": "OK"`;
(b) `gen_dashboard.py` renders `OK` as its OWN class, "OK (legacy, unread)", visibly distinct from ✓, ⏸, the
seat-failure glyph and pend, and counts it in the strip; (c) the forward domain check with Astra's four completeness
conditions (missing `d` = the existing `…` default; annotation/hold/record entries pass whatever their `d`; an inclusive
cutoff tested before, on and after; a positive control for a valid post-cutoff glyph beside the negative and the
cutoff-removed mutant); (d) an `OK` becomes ✓ or anything else only when a reader rewrites that one entry.  Question in
D2: v1 REJECTED `D_CLASS["OK"] = "ok"` as canonising an off-domain spelling -- is (b) the same mistake?

**F3. "Both agy probes exit 1" -- now MEASURED.**  Astra v2: unsupported (the 10-13 `agyprobe/` held no exit status).
`adj_20261016/agyprobe_rc/`: `--model gemini-9-nope --effort high` -> rc 1, stdout 0 b, stderr `error: invalid model
selection ...`; `--model gemini-3.8-flash-high --effort ultrahigh` -> rc 1, stdout 0 b, stderr `invalid --effort
"ultrahigh" (valid: low, medium, high, xhigh, max)`; agy 1.4.0.  **MINE: the claim now stands on a receipt.**

**F4. NEW, found while measuring F3: agy replaces its own binary on invocation.**  The first probe at 11:21 left
`agy.exe` new (199,837,848 b, 11:21) beside `agy.exe.1792167684245670300.old`, whose own mtime is 2026-10-13 22:33 --
the minute of the 10-13 probe (RA `agyprobe/probe_time.txt` 22:33:40), so that probe also coincided with a self-update.  A second invocation launched during the swap failed with `timeout: failed to
run command 'agy': No such file or directory` (rc 127; kept as `agyprobe_rc/bogus2.APPARATUS_FAIL*`).  A launcher that
fires agy jobs concurrently can therefore lose a seat to the swap, and a rc-127 "No such file" is an apparatus failure,
not a seat answer.  **MINE: FILE a row (`agyselfupdate`), severity low; the agy launcher's gate should treat rc 127 /
"No such file" as LAUNCH FAILURE and re-fire once.**

**F5. Astra v2's minor corrections to v2** -- C3 is 19 bytes, not 20; the launcher table has seven controls (five stream
fixtures + two preflights), six after C3's withdrawal; the `armbdt` example's lines are 5805/6215/6355, not
5796/6206/6346; "no receipt anywhere was true when written" is not historically supportable (say "none was found when
it was written"); the stage-controls 48/49 expectation is supported by reading only (a post-repin receipt is owed);
11 kimi-substitute entries.  **MINE: ACCEPT all as L4 corrections, recorded in this adjudication's output (the 10-13
artifact is left as written, corrected by reference).**

**F6. `seatverdictrefusal` v3** (RA v2.1, measured over 621 directories / 4,357 rows): Astra v2 SUPPORTED it.
**MINE: ACCEPT; FILE the ledger row if absent** (`adj_20261016/prescreen/prescreen_records.md` answers present/absent if
it exists when you read this).

**F7. `wdczerolendatain`** (the #563 harvest's filing).  **MINE: FILE if absent** (same check).

**F8. The #560/#561 held corrections** (RA v1 §3: 37 textual applications at HEAD, all still pending; Astra v1 :154-205:
TRUE that all 37 remain pending, and its per-entry assessment of the 17 #561 replacements).  **MINE: ACCEPT RA §3 as
the edit list, with Astra v1's per-entry assessments as amendments; execution is a records commit staged from HEAD
blobs** -- `dev_pcc2.c` carries the PEER's uncommitted edits (land the comment on HEAD's copy, never the working file);
the two `tools/panel.sh` items stay HELD (never-commit list); `regress/diff_ieee_store.c` owes precommit E's identity
guard in the same commit (Astra v2: the "or exempt" alternative was "correctly withdrawn").

**F9. RA v2.5's closing overrulings.**  Astra v2's table: every one supported or correctly withdrawn except Option B
(F1).  **MINE: ACCEPT.**

**F10. The three OWNER rule questions** (D2 edge wording; ROUTE PARITY; the label-clause scope for a binary
result-`if`): RA §4 holds graded drafts; Astra v2: "They remain recommendations".  **MINE: not adjudicable here -- the
owner decides; I list them so their pending state is visible.**

## 2. DISAGREEMENTS

**D1. Is the production rule (F1) complete?**  For: it is measured on six fixtures and has run every Astra job for three
weeks.  Against: N4 -- a nonzero exit with a full answer whose stderr quotes wall text is read as WALLED, and the rule
leans on the empirical claim "every real wall is rc 1 with empty stdout".  A refinement would read only codex's FINAL
`ERROR:` line (its own diagnostic sits at the end of stderr; quoted source sits earlier) whenever rc != 0 and stdout
is non-empty.  **Ruling (mine): land the rule as measured; record N4 as the residual; do NOT add the tail-only
refinement without a real instance (the addition licence: a measured delta or a transferred warrant).**  Astra: your
REJECT produced this -- is the residual acceptable?

**D2. The legacy-`OK` class (F2(b)).**  For: it ends the false "pend" rendering of 439 entries without asserting
approval for any of them, and needs no per-entry read.  Against: v1 rejected `D_CLASS["OK"] = "ok"` because it canonises
one of ~300 off-domain spellings; (b) canonises the same spelling under another name.  **Ruling (mine): adopt (b)** --
the objection to "ok" was that it reads as approval; "legacy, unread" asserts the opposite, and the domain check (c)
stops new `OK`s.  Fable: you made the v1 objection -- be hardest on this.

## 3. What is still owed, and where I may be fooling myself

- I accepted all ten findings.  That is the most suspicious count in the three packets.
- F1's measurement drove the launcher with a FAKE codex; the real codex's exit status in a mid-answer wall is not
  measured anywhere (N4 is synthetic).
- F4 rests on two coincident `.old` timestamps and one failed second launch -- one race, observed once.
- F8's execution touches ~20 files across `src/` and `regress/`; RA §3's "STILL APPLIES" was checked on 10-13 and HEAD
  has not moved since (e483d931), but the working tree has.

## 4. QUESTIONS (VERDICT LINE FIRST)

Open with your seat token and ONE verbatim line from `GXEMUL-SEC/regress/artifacts/adj_20261016/cxctl_optionC/RECEIPT.txt`.

`VERDICT: UPHOLD ALL / UPHOLD WITH CHANGES (<n> rulings changed) / OVERTURN (<the load-bearing ruling>) -- <one line>`

1. Adjudicate F1..F10 and D1..D2: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with the reason.
2. **WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?**  I accepted all ten.
3. **WHAT DID ALL OF US MISS?**
4. If `adj_20261016/prescreen/prescreen_records.md` exists: rule on each item in its LIVE list.

Seat-specific:
- **Fable 5.1**: RA is your adjudication; F1, F2 and F5 overturn or correct parts of it -- self-review, be harder.
- **Astra**: your two REJECTs produced F1, F2, F5 -- check that my fixes answer your objections rather than merely
  citing them.  You cannot run code; say where a claim needs a run.
- **Grok**: you have not seen this material before -- read RA v2 and Astra v2 first, then attack my dispositions.
