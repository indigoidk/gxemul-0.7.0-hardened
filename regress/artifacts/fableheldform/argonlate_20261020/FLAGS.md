VERDICT: 3 wrong records, 10 overtaken, 1 refuted, 1 live defects, 2 to file -- every Argon flag was already taken on the design pass or is refuted (its same-day index fix would reopen the documented 2026-08-30 same-date mis-clears); the residue is records wording (stalls and not-fired passes recorded as walls; the "V3-V6 answered" premise surviving in fableheldform's state_note) and one live instance of the filed class in its DISCHARGE direction: sgirekills' assess stage reads `ok 9/9` through two "never answered" notes that also release its hold.

# Records check of Argon's late reading of the `fableheldform` design pass (fhfp1)

**What was compared.** Argon read only the design-pass packet (`argon_bundle_1.txt`, `argon_bundle_2.txt`, built before the
commit). Each item below is judged against what `6c2840d7` and HEAD actually do. HEAD was `5dbc000e` when the work began;
`1a59a47e` landed during it and changes only `fbctrlcmdkill.commits` in the ledger, so every finding holds at both, and
`edits.diff` applies to both (`git -c core.autocrlf=false apply --check`; CHANGELOG hunks land at offset +4 on `1a59a47e`).
None of the rows `6c2840d7` touched changed after it: a ledger diff `6c2840d7` -> `5dbc000e` touches only other rows.

Everything here is read-only on the repository: `git --no-optional-locks show/cat-file`, and Python over **copies** of the
ledger in `work\`. The receipts are listed at the end. `ST` below means `tools/pipeline/stage_tokens.py` at HEAD, `CSP` means
`tools/pipeline/check_stage_panels.py`, `CFQ` means `tools/pipeline/check_fable_queue.py`, and `DP1` means
`regress/artifacts/fableheldform/design_20261018/`.

| # | Argon item | Disposition | One line |
|---|---|---|---|
| F1 | BROKEN: cx history (B:52) | **WRONG RECORD** (WR-1, WR-2) | The brief's premise was flagged by all three seats and taken. Two residues survive: the premise in fableheldform's own state_note, and the correction calling the v2/V3 stalls walls |
| F2 | BROKEN: earlier answers don't discharge | OVERTAKEN | At HEAD, live_holds gives fable5 on cx review, dashok review, and sgirekills research+review; all three rows are held |
| F3 | BROKEN: "LATER" means strictly later date | OVERTAKEN | The records say "strictly-later". cx [12] got NOTSEAT for exactly this reason. The brief is a preserved packet |
| F4 | BROKEN: census incomplete / systemic | OVERTAKEN | [8] was converted (17, not 16). The class is filed as `untokenedanswers`. A keyword-free read finds zero residue since 10-16 |
| F5 | BROKEN: wiringcliff [28] is design | OVERTAKEN (implication refuted) | Section I *does* read design (CFQ:122). [28]/[32] are HELD and carry #565's question |
| F6 | BROKEN: ip30abortkill in work vs held | OVERTAKEN | `held` was in Astra's micro-confirmed draft, with closure omitted. GLM's timing flag was taken |
| F7 | HOLDS: why the nine passed H | OVERTAKEN (mechanism nuance) | The hold set was empty because no HELD literal existed; is_answer is what filled the count |
| F8 | HOLDS: prefix in place | OVERTAKEN (verified) | For all 17 entries only `note` changed; date, phase, seat and index are intact |
| F9 | UNSETTLED (a)(b)(c) | OVERTAKEN (settled) | (a) Zero residue for fable5 since 10-16. (b) No check forbids a held row with a closure object. (c) Token constants read |
| M1 | Option E as owner alternative | OVERTAKEN | Already item (2) of fableheldform's hold_question. Argon adds one scoping caution (below) |
| M2 | NOTSEAT on superseded same-stage walls | OVERTAKEN (extension refuted) | [8]/[12] have it. [26] and the other pairs cannot change any reading, and wiringcliff's are a different round |
| M3 | "T:39 same-day discharge fix" | **REFUTED** | A deliberate rule with a measured warrant. Zero instances at HEAD. An index order would fail open |
| S1 | Q1 structural check | **FILE** (part 2) | (1) keyword check: owed already; (2) positive answer marker: FILE; (3) ledger-writer prefix: no tracked writer exists |
| X1a | *(mine, from F7/M3)* sgirekills assess | **LIVE DEFECT** | Hold [2] for kimi/opus5 is discharged by #564-close notes that say "never answered". CSP prints `ok 9/9` |
| X1b | *(mine)* fableheldform's own review stage | **FILE** | It goes 1/9 -> 2/9 and turns H RED when Fable's answer is recorded |
| WR-3 | *(mine, sibling of WR-2)* not-fired passes called walls | **WRONG RECORD** | Five rows' state_note/reopened, and the CHANGELOG/OB summaries, contradict each row's own hold_question |

---

## F1 -- `cxlaunchquotation` pass history (B:52 vs C:39-45) -> premise OVERTAKEN, two residual WRONG RECORDS

**The premise is corrected and acted on.** All three design seats flagged "Fable answered V3-V6 and walled only on V7":
* Astra: `DP1/codex_fhfp1.txt`, "`[12]` V3 stalled and `[26]` V6 walled".
* Grok: `DP1/grok_p1.txt`, "V3 [12] is a stall".
* GLM: `DP1/glm_p1.txt`.

At HEAD (ledger `cxlaunchquotation`):
* [4] PASS 2, [18] V4 and [22] V5 are Fable answers.
* [8] v2 and [12] V3 carry `[NOT A SEAT ANSWER]`, and both notes say STALLED (stream watchdog).
* [26] V6 and [30] V7 carry `[HELD AWAITING SEAT: fable5]`.
* `hold_question` reads "Fable walled on V6 and V7".

That matches Argon exactly.

**WR-1, L4.** `#566`'s filing text survives inside `fableheldform.state_note` (the `||` segment from `8faf4a16`):

> "of the 32 fable5 entries dated since 2026-10-17, 10 are HELD markers, 6 are Fable's own answers (the cxlaunchquotation
> and dashokclass V3-V6 passes, read by hand)"

The count 6 is right. The parenthetical is the refuted premise: in that window cx's answers are V4 [18] and V5 [22] only, and
its V3 stalled and its V6 walled. Grok named this sibling on pass 1 ("the paired 'six answers are the V3–V6 passes'"). The
round took the flag and left the sibling, which is the carrier's mechanical rule 2 (`tools/CLAUDE.md:2500`, "grep for its
siblings"). `OUTSTANDING_BUGS.md:24977` says only "6 are Fable's own answers", which is fine.
**Replacement** (`edits.diff`): "(cxlaunchquotation's V4 and V5 passes and dashokclass's V3-V6, read by hand -- corrected
2026-10-20: this said `the cxlaunchquotation and dashokclass V3-V6 passes', but cxlaunchquotation's V3 stalled and its V6
walled, as design pass 1 found)".

**WR-2, L4: two stalls recorded as walls.** Both entries say STALLED. Astra called [8] a "failure" and [12] "stalled"; Grok
called [12] "a stall"; GLM called [8] "a stall that wrote nothing". The committed text says otherwise:
* `CHANGELOG.md:115-118`: "`cxlaunchquotation`'s 2026-10-16 v2 and V3 walls with the non-answer token", and "one on the v2
  wall would already be cleared".
* `CHANGELOG.md:139-140`: "missed `cxlaunchquotation`'s 2026-10-16 wall (Astra, GLM); `cxlaunchquotation` walled on V3 and
  V6 as well as V7 (all three)". Two of the three seats it credits said V3 *stalled*.
* `OUTSTANDING_BUGS.md:25015-25017`: "v2 wall and its V3 wall", and "the v2 wall would already be cleared".
* ledger `fableheldform.state_note`: "cxlaunchquotation's 2026-10-16 v2 wall".
* `fableheldform.hold_question` (1): "two superseded walls".
* `fableheldform` [0] (codex): "(cxlaunchquotation's 2026-10-16 v2 wall is the same defect); cxlaunchquotation walled on V3
  and V6 as well as V7". This misquotes Astra.
* `fableheldform` [2] (glm): "walled on V3 and V6 too; ... (cxlaunchquotation's 2026-10-16 v2 wall)". GLM's own word for [8]
  was "stall".

The ledger's own counts confirm it. The four Fable walls of 2026-10-17 reconcile **without** V3:
1. V6 at 07:17 ([26]);
2. V6's re-fire at 07:5x, which "walled again" ([26]);
3. `dashokclass` V7 at 09:13, "its third wall that morning" ([29]);
4. cx V7, "its fourth wall that day" ([30]).

GLM's inference ("four walls ... consistent only if cxlaunchquotation walled V3") missed the V6 re-fire.

The distinction is not cosmetic. The V3 note says the stall was "most likely the whole 18-mutant kill table run as ONE
foreground command". That is a task-shape cause with its own remedy, which a "wall" label hides. Minimal replacements are in
`edits.diff`, with a dated correction note at the end of the CHANGELOG block and the OB section. The commit subject and the
CHANGELOG heading keep "walled", and the note says so.

## F2 -- earlier Fable answers do not discharge cx / dashok / sgirekills -> OVERTAKEN

`ST:106-107` discharges a hold only with a same-seat, same-phase answer dated strictly after the hold. `live_holds` at HEAD
(`work\measure_HEAD.txt` section 1):

| row / stage | live_holds | from |
|---|---|---|
| cx review | ['fable5'] | [26], [30] |
| dashok review | ['fable5'] | [29] |
| sgirekills research | ['fable5'] | [45] |
| sgirekills review | ['fable5'] | [49], [56] |

All three rows are `held`. The design pass ruled the same: Astra p1 #2, Grok p1 #2 ("A SHIP WITH CHANGES pass is not the
zero-breach closing pass"), and GLM p1 #2.

## F3 -- "later" means a strictly later DATE -> OVERTAKEN

Astra p1 #2 says: "'later' means a strictly greater recorded date, not a later index or pass". Grok's distinct ruling, taken
in ledger `fableheldform` [1], gave [12] NOTSEAT precisely because a same-day V4/V5 answer cannot clear a HELD tag dated that
day. The committed text states the rule correctly (`CHANGELOG.md:117`, `OUTSTANDING_BUGS.md:25016-25017`), and Astra's
confirm removed "forever". `brief_body.md` is the preserved packet and is left as sent.

## F4 -- census incomplete; defect systemic -> OVERTAKEN

The conversion took 17 entries, not 16: cx [8] (2026-10-16) is included as NOTSEAT, per Astra's and GLM's p1 flags. The
class across every seat and date is filed as `untokenedanswers` (MED, open), with GLM's keyword-free review owed there.

**Settled here for the converted slice, keyword-free.** Every `fable5` entry dated on or after 2026-10-16 that is_answer()
still counts was listed and read (`work\fable5_answers_since_1016.txt`):
* 52 fable5 entries, 13 counted as answers, and all 13 are genuine;
* cx PASS 2, V4 and V5;
* dashok v1, v2 and V3-V6;
* m88kexcdeliver passes 12-16.

**Zero untokened Fable non-answers remain since 2026-10-16.**

## F5 -- `wiringcliff` [28] is design, outside STAGES -> OVERTAKEN; the implication REFUTED

Astra p1 flagged that section H excludes design, and Grok and GLM agreed that [28]/[32] take the token while the row stays in
work. HEAD did this:
* [28] and [32] carry HELD;
* `hold_question` gains "#565 (held 2026-10-18 by fableheldform; Fable was not fired on #565's passes ...)";
* the state stays `in work`.

The implication that a design entry sits outside "the checkers" is false. **Section I reads design**: CFQ skips only `regress`
(`:122`) and credits a flagship answer in any other phase (`:126`). The tokens changed no live seat, because [41]/[48]
already held both stages. Their job is the record of #565's question, which is a different round from #566's.

## F6 -- `ip30abortkill`: "retain `in work`" vs "committed `held`" -> OVERTAKEN

Astra's confirm (`regress/artifacts/ip30abortkill/close_20261018/codex_close531b.txt`) did say "retain `state: in work`, omit
the closure object". The revised draft it then checked (`draft_r3/LEDGER_preview.txt`) reads:

    state: in work -> held
    closure: ABSENT (not closed)

and Astra's micro-confirm on it (`codex_close531c.txt`) says "All four corrections are applied; no new false sentence found".

At HEAD, `ip30abortkill` is `held` with no `closure` key. `held` is the ledger's defined state for this case: "waiting on a
NAMED party or event, and carrying the QUESTION it is held for" (`state_semantics.held`). No check distinguishes held from
in work: CSP tests only `state == "closed"` (`:198`, `:224`). The brief's timing slip ("committed held" while the commit was in
its hook) was GLM's flag, and it was taken (`CHANGELOG.md:141`).

## F7 -- the nine closures passed H; regress holds do not block -> OVERTAKEN (with a mechanism nuance)

The substance is HEAD's own warrant for reopening. The mechanism needs one correction. `live_holds()` was empty on those stages
because **no entry carried the HELD literal** (`ST:53-54`), not because `is_answer()` returned True. `is_answer()` is what made
the stage **counts** full (`CSP:184-188`, `:212`).

Astra p1 flagged the same thing ("It counts distinct answering seats"), and it was taken (`fableheldform` [0]). `regress` is
outside `STAGES` (`CSP:65`), as stated.

## F8 -- prefix in place keeps the wall's date -> OVERTAKEN (verified)

`work\diff_parent_6c28.txt` covers the parent `d42c76a8` to `6c2840d7`. For all 17 converted entries, `note` is the only
changed key; date, phase, seat and list index are unchanged. That is 15 HELD and 2 NOTSEAT, and each prefix keeps the
original prose and receipt. This was GLM's reasoning ("keeps the hold's date at the wall").

## F9 -- UNSETTLED (a)(b)(c) -> OVERTAKEN / settled

* **(a)** Post-10-17 non-answers outside the keyword list: none, for fable5, by the keyword-free read in F4. The all-dates
  review stays owed under `untokenedanswers`.
* **(b)** How `by_stage` is filled (`CSP:165-188`):
  * HELD entries go to `_held` and are skipped;
  * non-answers are skipped;
  * answers fill `seats` and `newest`.

  No section enforces held vs in work, and none forbids a `closure` object on a non-closed row. `closure` is read only by
  `gen_dashboard.py:199` (tooltip and badge); section L reads `reopened`. The ledger's `state_semantics._TENSE` says `state`
  is present tense and `closure.note` past tense, "independent BY DESIGN". Astra's confirm ran H, I, L and Q2 in memory and
  found them green.
* **(c)** The constants:
  * `HELD = "[HELD AWAITING SEAT:"` (`ST:37`);
  * `NOTSEAT = "[NOT A SEAT ANSWER]"` (`ST:41`);
  * `HELD_SEATS` (`ST:72`) is a strict `[a-z0-9_]+` comma list, case-sensitive like `is_held`;
  * a malformed marker holds as `?malformed-hold` (`ST:98-104`).

## M1 -- Option E as the owner alternative -> OVERTAKEN; the owner question stays OPEN

Astra named E on the design pass. It is item (2) of `fableheldform.hold_question`: "does the 2026-10-17 directive permit a
CLOSED row whose research or review question is held for Fable (option E, a change to section H and the state semantics)".
That question is not decided here.

**What Argon's argument adds is one point, and it is a caution about Argon's own mechanism.** Argon would let H accept "a
closed row whose only live holds are fable5". That is keyed to the **seat**, not to the directive.

At HEAD, 14 rows hold STAGES stages for fable5 alone (`work\optionE_scope.txt`). One of them is `alphavmkill` research [12],
dated 2026-09-19: "the first-hand Fable ruling on the pass-1 design is owed" after a refusal fallback. That has nothing to do
with the 2026-10-17 wall directive. So if the owner chooses E, the carve-out has to be keyed to holds recorded under the
2026-10-17 directive, not to `fable5`.

Two things Argon does not add:
* The regress analogy is already in the brief (B:20-21, 28) and in Grok p1. It is also disanalogous: regress is a post-close
  review by its own standing directive, while a research or review hold asks whether the work the close rests on stands.
* Argon's E omits the state-semantics change Astra pairs with it. `closed` is defined as "Nothing outstanding; the claim was
  discharged BY WORK".

## M2 -- `[NOT A SEAT ANSWER]` on superseded same-stage walls -> OVERTAKEN; the extension REFUTED

HEAD already gives NOTSEAT to cx [8] and [12], with the criterion written on each: "(a later pass superseded it and Fable
answered that one: V4, 2026-10-17)". Argon would extend NOTSEAT to:
* cx [26] (V6);
* sgirekills [49];
* sgirandomcolour [28];
* wiringcliff [28]/[32].

**No reading can change.** For one seat in one stage, `live_holds` reports the seat if and only if it has no answer dated
after its **latest** hold. Earlier holds for the same seat never change the result, and HELD and NOTSEAT both drop the entry
from the seat counts (`CSP:171-185`). So the extension has no measurable consequence in H, I or the codex wall.

For wiringcliff it is also wrong on substance. [28]/[32] are `#565`'s passes, a different round whose question Fable never
answered. NOTSEAT would leave that question in `hold_question` with no marker carrying it, which is the "substitutes a
non-answer record for the review hold" form Astra overturned on `ip30abortkill`.

V6 does not meet HEAD's criterion, because Fable answered no later pass. It stays HELD, with its packet named in cx's
`hold_question`.

## M3 -- "a `T:39` same-day discharge fix" (compare `(date, index)`) -> REFUTED

* **The date rule is deliberate and has a measured warrant.** The carrier (`tools/CLAUDE.md:3161-3177`) says discharge needs a
  seat answer "dated STRICTLY AFTER D". When "later" was implemented as `>=`, "All six 2026-08-30 mis-clears were discharged
  by SAME-DATE siblings written by the very batch that created the marker to record the stage as NOT done." `ST:88-91` cites
  it as "the carrier's discharge rule".
* **An index tie-break re-admits that failure.** Any same-day sibling written after the marker would discharge it again. With
  `untokenedanswers` open, an untokened "NOT FIRED" sibling still counts as an answer, so the fix would widen the
  false-discharge surface.
* **It buys nothing at HEAD.** Zero live holds anywhere in the ledger would be discharged by a same-day, later-index answer
  from the named seat (`work\measure_HEAD.txt` section 2, TOTAL 0).
* **The one case Argon cites is already handled.** cx [12] carries NOTSEAT, and the same-date V6/V7 holds dominate anyway.
* **It fails in the wrong direction.** The date rule fails safe: a hold stays visible until a later-dated answer. An index rule
  fails open.

## S1 -- Q1's structural check

1. **A precommit check that reds untokened entries with failure keywords: OVERTAKEN.** This is `untokenedanswers`' owed item
   (1): "a STRUCTURAL check, forward-only from a cutoff ... keyword-based, so it must say so and carry negative controls".
2. **A positive answer marker on every new answer: FILE.** This is not in `untokenedanswers`, and it has measured
   consequences. The round's own first count, keyed on `NOT FIRED`, found 8 of 16 (`fableheldform.state_note`). Since
   2026-10-01, entries counted as answers break down as follows (`work\dkw_census.txt`):
   * **7** carry `d` and match a 12-phrase non-answer net in their first 400 characters. All 7 are genuine answers (for
     example `fableheldform` [1], [2] and `ip30abortkill` [48]), so a keyword check would red them.
   * All 17 converted entries, and `sgirekills` [70]/[71], carry no `d`.
   * **The cost**: 185 of the 319 entries counted since 2026-10-01 carry no `d`. A positive marker is a writer habit not yet
     held, which makes it forward-only.

   The proposed text is item (c) of the `untokenedanswers` amendment in `edits.diff`.
3. **"Make the ledger-writer prepend the token": REFUTED as stated.** No tracked tool appends ledger entries (`git grep`
   finds no `entries.append` under `tools/`), so the precommit check is the only structural landing spot.

## X1a (mine) -- an untokened non-answer DISCHARGES a live hold: `sgirekills` assess -> LIVE DEFECT

This was found while checking F7 and M3. The class is filed (`untokenedanswers`); this direction of it is not.

**The input.** Ledger `sgirekills` at HEAD:
* assess [2] (opus5, 2026-08-30) reads `[HELD AWAITING SEAT: codex, grok, kimi, opus5]`.
* codex and grok answered later.
* kimi [70] and opus5 [71] (2026-10-18) read: "#564 close: NOT FIRED -- this assess stage (2026-08-30) asked for this seat and
  it never answered; it is outside the owner's roster for #564".

Being untokened, they are answers to `ST:65-69`, so `live_holds` discharges [2] by them, and `CSP --list` prints
**`ok    sgirekills     assess    9/9`** (`work\H_on_HEAD_list.out`).

**The measurement** (`work\sim_sgirekills.py`, copies only):

| copy | live_holds(sgirekills/assess) | section H |
|---|---|---|
| HEAD-form, row re-closed after a simulated Fable answer | `[]` | **PASS** |
| NOTSEAT on [70]/[71], re-closed | `['kimi', 'opus5']` | **CLOSED-WHILE-HELD assess 7/9**, rc 1 |
| NOTSEAT on [70]/[71], still held | `['kimi', 'opus5']` | HOLD, rc 0 |

So `6c2840d7` reopened `sgirekills` for Fable, but its re-close will pass H through two notes that say the seats never
answered.

**Population.** Across the ledger, 36 (hold, seat) pairs are discharged. Five match a broad non-answer keyword net
(`work\discharge_census.txt`). Read by hand, three are genuine answers and these two are the only non-answers.

**How it settles:** the owner ruling owed as `untokenedanswers` item (2), applied before `sgirekills` re-closes. The filing
text is item (a) of the amendment in `edits.diff`.

## X1b (mine) -- `fableheldform`'s own review stage reds H when Fable's answer lands -> FILE

At HEAD that stage is codex [4]/[6] plus the Fable hold [5], which CSP reports as `HOLD fableheldform review 1/9`. The roster
exclusions are recorded only in CHANGELOG prose ("Opus 5.5, agy, kimi, deepseek and minimax deliberately not fired").

Appending a simulated Fable answer (`work\sim_fable_answers_all.py`, `work\H_sim_D.out`) gives:

    STAGE_PANELS_FAIL ... fableheldform held review 2/9 missing: opus5, agy, grok, kimi, glm, deepseek, minimax

That simulation covers every held Fable stage on the 12 rows involved, and this is the only failure.

The natural repair would be untokened "NOT FIRED" entries, which is the defect this row exists to remove. So this waits on the
same owner ruling as X1a. The filing text is item (b) of the amendment.

## WR-3 (mine, sibling of WR-2) -- passes Fable was not fired on, recorded as walls -> WRONG RECORD

Of the 15 HELD entries, 7 are walls (HTTP 429) and 8 record a pass Fable was **not fired on** after an earlier wall that day:
* `wiringcliff` [28] and [32];
* `sgirandomcolour` [32];
* `mapledmaaddr` [50];
* `xscaleinten` [21];
* `ppcrldimimask` [21];
* `ppcrlwimiwidth` [21];
* `ppcgateimageskip` [3].

The carrier keeps these apart (`tools/CLAUDE.md:209-211`: "a seat that was deliberately not fired is a different thing again
— conflating the two is how a two-seat review gets reported as a panel"). The 2026-10-17 directive says "Still try Fable once
per pass". Astra p1 said "Preserve 'not fired' honestly". The entries and the `hold_question`s do: for example
`mapledmaaddr`'s reads "Fable was not fired on the closure check, having walled that morning".

The summaries do not, and so contradict the row's own question:
* The `state_note` head and `reopened` of the five closure-check rows say "held a Fable wall written as untokened prose" /
  "recorded as an untokened note".
* `CHANGELOG.md:108` says "recorded one" (that is, a wall), and `:115` says "fifteen walls".
* `CHANGELOG.md:122` and `OUTSTANDING_BUGS.md:25023-25027` say "the pass Fable walled on" and "held a Fable wall".
* `fableheldform.state_note` says "17 walled Fable entries", and its `hold_question` (1) says "the walls tokened HELD".

Minimal replacements are in `edits.diff`. In the five `reopened` fields the commit hashes section L reads are unchanged
(checked: the same SHA tokens before and after).

---

## The proposed edits (`edits.diff`, not applied)

**Files:** `CHANGELOG.md` (the `fableheldform` block: five in-place fixes and a dated correction note),
`OUTSTANDING_BUGS.md` (its `fableheldform` section: five fixes and a correction bullet), and `tools/pipeline/ledger.json`.

**Ledger fields changed:**
* in `fableheldform`: `state_note`, `hold_question`, and the notes of entries [0] and [2];
* the `state_note` and `reopened` of `mapledmaaddr`, `xscaleinten`, `ppcrldimimask`, `ppcrlwimiwidth` and
  `ppcgateimageskip`;
* `untokenedanswers.state_note`, appended with (a) X1a, (b) X1b and (c) S1.2.

**Checked on copies** (`work\build_edits.py`, `work\patched\`):
* the result is valid JSON;
* CRLF is kept, there is no trailing newline, and the line count is unchanged;
* no quote or backslash enters a string;
* `CSP` still prints `STAGE_PANELS_PASS` on the patched ledger;
* the diff applies cleanly, and the result is byte-identical to `patched\` on `5dbc000e`.

**Before landing:**
* **Apply:** in the repo use `git apply` (the repo sets `core.autocrlf=false`). Outside it, use `git -c core.autocrlf=false
  apply`, because this machine's global git converts to CRLF.
* **Sync:** the working tree holds another session's staged `CHANGELOG.md` and `ledger.json`, so rebase the hunks on whatever
  HEAD is when this lands.
* **Regenerate:** run `matrix.html` (`gen_dashboard.py`) after the ledger edit. The codex-wall block does not change, because
  no hold changes.
* **Receipts:** `untokenedanswers` item (a)-(c) cites `regress/artifacts/fableheldform/argonlate_20261020/`. Copy the
  receipts there **before** committing, because `work\` is a volatile scratchpad. The receipts include `.py` scripts, and
  section R wants MANIFEST entries for a new artifacts dir's `.py`.

## Receipts

All under `C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\argonlate\fhfp1\work\`.

| file | what it holds |
|---|---|
| `ledger_HEAD.json` (= `ledger_HEAD_blob.json`) | `git cat-file -p HEAD:tools/pipeline/ledger.json` at `5dbc000e` |
| `st\stage_tokens.py`, `st\check_stage_panels.py` | HEAD copies of the checkers the measurements ran |
| `diff_parent_6c28.txt`, `diff_6c28_HEAD.txt`, `diff_ledgers.py` | what `6c2840d7` changed, and that HEAD left those rows alone |
| `measure_holds.py`, `measure_HEAD.txt` | live holds per stage; same-day later-index answers (TOTAL 0); keyword-only discharges |
| `discharge_census.py`, `discharge_census.txt` | 36 discharged (hold, seat) pairs, 5 net hits read |
| `sim_sgirekills.py`, `sim_sgirekills.txt`, `H_sim_A_head_reclosed.out`, `H_sim_B_tokened_reclosed.out`, `H_sim_C_tokened_held.out` | X1a |
| `H_on_HEAD.out`, `H_on_HEAD_list.out` | section H at HEAD (`STAGE_PANELS_PASS`; `ok sgirekills assess 9/9`) |
| `sim_fable_answers_all.py`, `H_sim_D.out` | X1b |
| `fable5_since1016.py`, `fable5_answers_since_1016.txt` | F4 and F9(a), keyword-free |
| `dkw_census.py`, `dkw_census.txt` | S1.2 (`d` x keyword cross-tab since 2026-10-01) |
| `optionE_scope.py`, `optionE_scope.txt` | M1 (14 fable5-only held rows, alphavmkill among them) |
| `build_edits.py`, `patched\`, `diff_HEAD_patched.txt`, `H_on_patched.out` | how `edits.diff` was built and checked |
