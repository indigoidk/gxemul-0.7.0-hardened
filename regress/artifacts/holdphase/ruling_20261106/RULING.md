# RULING -- FABLE_QUEUE item 6, ledger row `holdphase` (and the discriminator half of `untokenedanswers`)

> **DURABLE COPY, banked 2026-11-06 by a records commit.**  The original is `_scratchpad/fable_20261106/item6/RULING.md` (scratch, not durable; md5 51300b18), written 2026-11-06 by the Fable 5.1 seat for FABLE_QUEUE item 6 (the `holdphase` rule question, and the discriminator half of `untokenedanswers`); the coordinator verified its author with `agent_models.py` as claude-fable-5-1 (this kit did not re-check it).  This banner and the marked citation rewrites `PROVENANCE.md` lists are the only edits; the ruling's text is otherwise verbatim.

Flagship seat: Fable 5.1 (Agent tool, `model: "fable"`), 2026-11-06.  Liveness `FABLE_LIVE_20261106_I6`;
first line of `_scratchpad/CHECKPOINT.md` [scratch, not durable] read verbatim: `# CHECKPOINT -- 2026-11-04 17:0x RUNNING (087a90
sections rewritten; the peer's sections below are untouched)`.

**Evidence basis.**  `regress/artifacts/holdphase/measure_20261106/EVIDENCE.md` [the durable copy of the scratch original `_scratchpad/wholdphase/EVIDENCE.md`, which adds only a banner and one marked heading] and `analyze.py` / `analysis.out` (HEAD `2632277f`;
`HOLDPHASE_ANALYSIS_DONE` present); `GXEMUL-SEC/tools/pipeline/stage_tokens.py` at HEAD (`git show
HEAD:tools/pipeline/stage_tokens.py`, 243 lines; `is_answer()` `:65-69`, `live_holds()` `:87-110`, the test at
`:106-107`); `check_stage_panels.py` `:160-260` at HEAD; `gen_dashboard.py` `:110-185` at HEAD; the carrier's rule
text (`CLAUDE.md`, the 2026-08-30 correction: *"does the marker name a seat that has answered in THE SAME STAGE,
at a STRICTLY LATER date?"*); the `holdphase` and `untokenedanswers` rows in the working-tree ledger.  Plus
TWO measurements of my own, described under Q2 with their deriver, run on BOTH the HEAD extract
(`wholdphase/ledger_HEAD.json` [scratch original, == `git show 2632277f:tools/pipeline/ledger.json`]) and the working-tree ledger -- identical results on every number quoted.
No gate, panel, build or codex invocation.  **One seat ruling on a rule question; provisional in the carrier's
sense if the owner wants the roster on it, final otherwise -- the carrier routes rule questions to this seat.**

---

## Q1.  SAME-PHASE or ANY-PHASE?   **RULING: SAME-PHASE.  The hold_question's doubt is answered YES -- the
## regress reasoning extends to every phase, on a stronger ground than fable-only-ness.**

### The rule as it stands, and why it stands

1. **The carrier already says SAME STAGE** (corrected 2026-08-30 after the row-scoped sweep mis-cleared twenty
   markers across seventeen rows), every reader implements it (`check_stage_panels.py`, `check_fable_queue.py`,
   `gen_codex_wall.py`, `gen_dashboard.py` all group by phase before calling `live_holds()`), and hand practice
   agrees: of 87 parsed hand-defangs, 85 had a same-phase answer, 1 an other-phase answer only (`n6` [4]), 1 none.
   So this ruling CONFIRMS the standing rule; it does not change it.

2. **The ground that generalises.**  Since the 2026-08-16 directive every (row, phase) is a separate nine-seat
   obligation, and every tool's SEAT TALLY is per-phase (`check_stage_panels.py:184-188`,
   `check_fable_queue.py:116-119`).  A hold is the dual of the tally -- "this seat is still owed HERE" -- so the
   discharge must have the tally's scope or the tools contradict themselves.  EVIDENCE.md section 5 measures the
   contradiction: under ANY-PHASE, `check_stage_panels` turns 4 of the 8 affected stages from HELD into
   **FAIL incomplete** and `check_fable_queue` turns 2 into **FAIL short, not held**, because the hold leaves
   the stage while the seat is still absent from it; `gen_codex_wall` silently drops all 8.  ANY-PHASE does not
   make the stages complete; it makes them red or invisible.

3. **A later phase asks a different question by construction, not by convention.**  Design is pass 1 on the
   brief BEFORE the edit; review is pass 2 on the diff AFTER it; regress is the flagship's review of the detector
   as shipped; assess and research are different briefs again.  A review answer, however good, cannot be the
   design answer -- the design question was "should this be built", asked of a text that no longer exists in that
   form.  The fable-only argument for regress is one instance of this; the general fact is that the ledger's phase
   is the ONLY structural proxy for "which question", and the test has no other (wiringcliff [55], in the ledger's
   own words: *"live_holds() discharges every earlier fable5 hold in a stage on any later-dated fable5 answer"* --
   it matches seat and date, never the question).  ANY-PHASE would remove the one proxy there is.

### The differing set, item by item (11 of 141 marker-seats; EVIDENCE.md section 2)

ANY-PHASE adds eleven discharges and SAME-PHASE loses none (0 of 141 go the other way).  Not one of the eleven is
a discharge a TOOL could know to be right:

| # | marker-seat | what ANY-PHASE would discharge it on | disposition under this ruling |
|---|---|---|---|
| 1 | wdccdbmidxfer regress/fable5 | a research answer + the main loop's restoration note filed under `seat: fable5` ([27], [28]) | **Rejected by the ledger's own words** -- the marker says the row-scoped sweep "should not have".  Stays live.  [28] owes NOTSEAT (Q2). |
| 2, 3 | wiringcliff design/fable5 [28], [41] | a late REVIEW of #565's records ([54]) | The row's own review marker [55] says [54] "answered neither" held review question; it cannot have answered the design pass either.  Stay live. |
| 4 | sgirekills assess/kimi | packet-fed answers to step-1 design and passes 2/4 ([15], [23], [34]) and two NOT FIRED notes ([64], [65]) | Answers to OTHER stages' questions plus non-answers.  Stays live. |
| 5 | sgirekills assess/opus5 | ONLY "preserved for the adjudication" and "NOT FIRED" notes ([18], [27], [37], [60], [61]) | **The decisive case**: ANY-PHASE would discharge a hold on records that say the seat did not answer.  Stays live; those five owe NOTSEAT (Q2). |
| 6 | pcc2widthkills assess/opus5 | first discharger is a SEAT DOWN note ([26]); then twelve review-phase measuring passes | The hold is moot by its own `hold_question` ("No question remains held") -- but it would be closed on the WRONG evidence.  Discharge by hand-defang citing the review passes, when the row is next touched. |
| 7 | lcabadval assess/opus5 | a research rung-3 probe build ([27]) and a review kill table ([34]) | Possibly answered in substance; whether the measurements answer the ASSESS question ("needs the tree and an m88k reading") is a judgment.  Main loop decides; if yes, hand-defang citing [27]/[34]. |
| 8, 9 | sgimtedepth4dead assess/opus5 [7], assess/fable5 [8] | the review measurement [21] and ruling [22] on 7g-1 | 7g-1 was held in two phases and answered in one.  Hand-defang the assess copies citing [21]/[22] -- the form alphatbinegsel [8] already uses. |
| 10 | alphatbinegsel design/opus5, row CLOSED | review [32] and assess [34] | The design question was a pass-1 question; [34] discharged the assess copy by hand-defang already.  Decide whether [32]/[34] answer the design hold; if yes, defang citing them; a live design hold on a closed row is otherwise a CLOSED-WHILE-HELD that no gate evaluates (design is outside `STAGES`) -- a gap of the gates, not of this rule. |
| 11 | fableheldform design/fable5 | a late records review ([10]) | The row's review marker [11] says whether [10] discharges hold question (3) "is the adjudicator's to say" -- it is, and the answer is that a records review of a row is not a pass-1 design answer.  Stays live. |

Seven of the eleven are answers to other stages, three are late records reviews, one rests only on non-firing
notes; the one the ledger rejects in its own words, the one that would close on a SEAT DOWN note and the one that
would close on nothing but non-answers are enough to decide the question.  The four that "look answered elsewhere"
(#6, #8, #9, #10, and #7 if the main loop so judges) are the COST of SAME-PHASE, and the cost is one records act
each, described next.

### Cross-phase discharge is a RECORDS ACT, never an inference

When a later answer in another phase genuinely answers a held question, the marker is **defanged IN PLACE**, the
defang naming the discharging entry by index, phase and date and saying what it answers (alphatbinegsel [8],
*"DISCHARGED by the assess answer below"*, is the form; lcabadval [5], *"answered later in this stage"*, is the
same-phase form).  It is subject to the tool's three conditions -- the named seat, strictly later, `is_answer()` --
PLUS the fourth the tool cannot check and a human can: **it answers the hold's question**, which is why
`hold_question` is mandatory on a held stage.

**Not by a same-phase POINTER ENTRY filed under the seat's name** (armbfxwidth32 [24], *"Discharged with the
review ruling above"*).  That writes an entry under `seat: fable5` that the seat did not write -- exactly the shape
wdccdbmidxfer [28] names as *"MANUFACTURED A SEAT ANSWER"*.  An honest pointer entry carries NOTSEAT, and a
NOTSEAT entry does not discharge; so the defang-in-place is the ONLY honest cross-phase discharge.  The three
armbfxwidth32-style pointers and the n6 cross-phase defang are corrected to the citing form when their rows are
next touched -- not swept.

### The structural landing spot (recommended; FILED, not done here)

The SAME-PHASE scope today is a property of the CALLERS' grouping, not of `live_holds()`: the function itself is
phase-agnostic (it tests seat, `is_answer`, `>`), and every one of the four readers happens to pass it a per-phase
list.  The 2026-08-29 sweep was a fifth, ad-hoc caller that passed a whole row, and that is how twenty markers
went.  The one-line fix is to put the phase test INTO the function -- `e.get("phase") == h.get("phase")` beside
the seat test at `:106`, the shape `analyze.py`'s `discharges()` already uses -- with two controls: (i)
`live_holds(whole_row)` equals the union of `live_holds(per-phase group)` on every row of the HEAD ledger
(92 marker stages, currently 0 mismatches for the per-phase form); (ii) a fixture with a cross-phase later answer
stays live.  A marker with a missing `phase` is its own stage, never a wildcard (one entry in the ledger lacks
`phase`, lethalonly [0]; it is not a marker).  This is the carrier's own thesis: a rule fires when it lives where
the decision happens, and the decision is made inside `live_holds()`.

### Two bounds on the ruling

* **SAME-PHASE is the floor, not the whole rule.**  Within one phase the test still matches seat and date, never
  the question.  What keeps a mis-aimed same-phase answer from discharging a hold is the RESTATED-MARKER idiom
  (a new marker dated at the answer that "answered neither" -- wiringcliff [55], ip30abortkill [55],
  fableheldform [11]), and that idiom depends on `>`: EVIDENCE.md section 1 shows the six same-date siblings that
  `>=` would flip are exactly those restated markers.  The two settled qualifiers are jointly load-bearing;
  neither is redundant given the other.
* **What `holdphase` records.**  The row's `hold_question` is answered: SAME-PHASE, for every phase, on the
  tally-duality ground; the DATE half was already settled.  The row closes with this file as its witness
  (`harness:` -- the subject is the test apparatus) once the function-level phase test lands with its controls,
  or closes documented-only now with that fix FILED; either is honest, and the first is the one I recommend.

---

## Q2.  The untokened "NOT FIRED" / "SEAT DOWN" note counted as an answer -- defect, and what the discriminator is.

### Is it a defect to fix?  **YES -- and it is the gate-passing-falsely class, which is what converts prose into
### machinery under the carrier's own escalation rule.**

`is_answer()` does what its comment says (`:69`, *"so is every untokened entry"*), so the CODE is right against
its spec; the SPEC is wrong against the doctrine the ledger exists to enforce -- *a seat that did not answer is a
SEAT FAILURE, never agreement, and a deliberately unfired seat is a different thing again.*  The measured
consequences are two, in two consumers of the same predicate: (a) section H printed `ok sgirekills assess 9/9`
over two seats whose entries said they never answered (untokenedanswers (a), corrected by tokening [70]/[71]);
(b) `live_holds()` discharges a hold on such a note -- today's row #5 above, and the SEAT DOWN first-discharger
of #6.  (a) is a gate passing falsely.  The carrier's pre-specified trigger for turning a writing rule into a
check is exactly *"a gate passing falsely"*; it has fired.  Already filed as `untokenedanswers`; **no second row**
-- this ruling adds the `live_holds()` consequence as a second consumer under that row and sets the discriminator.

### What the discriminator is NOT -- three correlates, each measured to fail

The question's own finding is that length fails (2 of 3 sub-100-char discharges are genuine terse answers,
EVIDENCE.md section 4).  I measured the other two candidates, on the HEAD extract and the working-tree ledger
(identical):

    deriver: for every entry with is_answer(e) true (HEAD stage_tokens.py), tally the `d' field; for entries
    dated >= 2026-10-01 test the first 400 chars of the note against the 13-phrase net
      NOT FIRED|NOT TRIED|SEAT DOWN|SEAT FAILURE|preserved for the|walled|never answered|DELIBERATELY NOT|
      not on the owner's|outside the owner's|rate_limit|usage limit|429   (case-insensitive)

* **Keyword nets fail in both directions.**  Counted answers since 2026-10-01: 1129.  Net hits: 183 -- 120 with
  no `d`, 63 with `d` = CHECK.  I read all 63 CHECK hits at 150 chars: nearly all are GENUINE answers whose
  panel-record boilerplate names a walled transport in passing (*"the kimi CLI returned 403 ...; its substitute
  kimi-k3:cloud answered VERDICT: GO"*, *"Grok 4.7 ... (mid-line) VERDICT: GO-WITH-CHANGES"*).  A FAIL on the net
  would red roughly sixty honest entries a month and be switched off -- the carrier's switched-off-check shape.
  And the net is BLIND to a non-answer phrased without its words: qhslowifetch [149] (agy, review, no `d`) reads
  *"NO ANSWER (empty: ...)"* and matches nothing.  (Of the 120 no-`d` hits I read 14; those are NOT FIRED roster
  notes -- sgirekills [60]-[69], m88kexcdeliver [99]-[102] -- so "nearly all" is a reading of heads, not a count.)
* **The dashboard glyph is a VERDICT axis, not an answer axis.**  `d` is rendered by `gen_dashboard.py`
  (`D_CLASS`: CHECK ok, CROSS bad, PAUSE hold, ELLIPSIS pend).  56 counted answers carry PAUSE or ELLIPSIS, and
  ELLIPSIS sits on BOTH an honest reading (*"UNKNOWN - cannot read file:line"*, d1 [7]) and a 90-byte stall
  (*"SEAT FAILURE (90 bytes)"*, d1 [8]) -- the carrier says an honest UNKNOWN is an answer and a stall is not, and
  the glyph cannot tell them apart.  Worse, CHECK sits on three self-described non-answers: mipsprimundec [53]
  (*"VERDICT: CANNOT-DESIGN -- a non-answer: it refused"*), [59] (*"SEAT FAILURE -- three tries..."*), [72]
  (*"INCONCLUSIVE -- ... a safety classifier stopped the turn"*).  The project already moved AWAY from reading
  `d` for semantics (`gen_dashboard.py:150-152`: *"a hold renders from its SEMANTICS, never from its `d' field"*);
  this ruling does not move it back.

Three correlates, three measured failures, and the same reason each time: **a correlate returns a plausible
answer whether or not it is reading the property** -- the check-that-cannot-fail family's classification cousin,
which the carrier already names for counts.

### THE DISCRIMINATOR: the RECORDER'S DECLARATION, read as a token -- never a property read off the note.

1. **The non-answer side is already in the schema and is MANDATORY from here on.**  Every entry filed under a
   seat's name that does not carry that seat's answer to THAT stage's question carries NOTSEAT -- the existing
   entry-scoped token, `stage_tokens.py`'s own docstring default (*"NOTSEAT IS THE ENTRY-SCOPED MARKER, and it
   is the one to reach for by default"*) -- or HELD when the question is still owed.  All three non-answer kinds
   take it, and the KIND is spelled in prose after the token so the record stays honest about which it was:
   SEAT FAILURE (wall, 429/529, stall, refusal, empty reply); DELIBERATELY NOT FIRED (owner roster,
   conservation); MAIN-LOOP RECORD filed under the seat (wdccdbmidxfer [28]).  An entry recording a seat's
   substitute transport or a model fallback that DID answer (kimi-k3:cloud for the kimi CLI; Mythos for a
   stopped Fable run) is an answer and says so in prose -- that is a disclosure matter, not a non-answer.
2. **`is_answer()` stays token-only.**  No keyword, length or glyph test goes INTO the classifier -- the file's own
   rule (*"Brief-TITLE matching is deliberately absent: a correlate that missed BOTH real disputed cases"*), and
   the measurements above are three more such correlates.  The classification is a declaration; the tool reads
   the declaration.
3. **Omission is made LOUD forward-only from a cutoff, at the gate, not in the classifier.**  A new
   `precommit_check.sh` section (the `check_stage_panels.py` `HOLDQ_CUTOFF` idiom) REFUSES a commit that adds a
   ledger entry, dated on or after the cutoff and filed under a seat's name, that carries NEITHER a stage token
   NOR a declared verdict glyph (`d` in {CHECK, CROSS}) -- reporting it as **UNCLASSIFIED: add NOTSEAT, HELD or a
   verdict**, by row and index.  This is inference-free: it reads two fields and asks whether the recorder
   classified the entry at all.  It cannot be gamed silently -- a recorder who stamps CHECK on a wall has written
   a FALSE DECLARATION, a wrong record (L4) a reader can correct, which the carrier ranks above a silent default
   that never appears as missing.  Since 2026-10-01 the `d` field is clean (862 CHECK, 267 absent, no other
   values), so the cost is one glyph on the ~24% of answer entries that lack one today, and nothing on legacy
   entries.  The glyph is used here ONLY as "the recorder declared a verdict", never as the verdict's meaning --
   point 2 is why an honest UNKNOWN recorded with ELLIPSIS must ALSO say which it is: a reading (add CHECK or
   CROSS, or write the UNKNOWN as the verdict) or a stall (NOTSEAT).  Forcing that one decision at write time is
   the whole point.
4. **The keyword net survives only as a WARN-level audit of DECLARED answers, with its denominator.**  List new
   CHECK/CROSS entries whose first 400 chars match the net -- *"N of M declared answers read like a wall;
   confirm"* -- for a human read, never a FAIL.  It exists to catch the stamp-on-a-wall case (mipsprimundec
   [53]/[59]/[72]), it must say it is keyword-based, and it is bounded by being advisory on a population the hard
   check has already classified.
5. **Negative controls before any of it ships**: a NOT FIRED note without a token is REFUSED; the same note with
   NOTSEAT passes; a genuine answer quoting "walled" with CHECK passes the hard check and is LISTED by the audit;
   a legacy (pre-cutoff) untokened entry is untouched.  Two per direction, the project's standing requirement
   for harness changes.

### What this ruling deliberately does not decide

* **Owner item (2) of `untokenedanswers`** -- how a deliberately narrowed roster is recorded so that section H
  can read it -- is a STAGE-scoped question and stays the owner's.  Tokening a NOT FIRED note does NOT decide it
  by side effect, which answers GLM 5.3's and Grok 4.7's dissent: `is_answer` is entry-scoped and
  `exempts_stage` is stage-scoped (the docstring's two independent properties); NOTSEAT says only that this entry
  is not this seat's answer, which is true under every answer to (2).  Whether such a stage may then CLOSE short
  needs a stage-scoped exemption token keyed to the DIRECTIVE, not to a seat (a seat-keyed form would also let
  alphavmkill's first-hand Fable hold close) -- the row's option E, for the owner.  Until ruled, a narrowed stage
  reads HELD or short, which is the true state.
* **The historical population** (the row's census: 497 keyword matches among counted answers, 129 rows) is
  corrected row by row when a round touches a row -- item (3) of the row, unchanged.  The five sgirekills
  non-firing notes ([18], [27], [37], [60], [61]), pcc2widthkills [26], wdccdbmidxfer [28] and the two
  mipsprimundec failures stamped CHECK are the first to correct, because each is load-bearing for a hold or a
  tally today.

---

## Verdicts, one line each

* **Q1: SAME-PHASE**, for every phase, because a discharge is the dual of a per-phase tally and the phase is the
  only proxy the ledger has for the question asked; cross-phase discharge is a hand defang that cites the entry
  and the question, never an inference; put the phase test inside `live_holds()` (FILED).
* **Q2: a defect (MED, already filed as `untokenedanswers`; this ruling adds the `live_holds()` consumer).  The
  discriminator is the recorder's DECLARATION -- NOTSEAT/HELD on every non-answer, `is_answer()` token-only, a
  forward-only gate that REFUSES an entry with neither a token nor a declared verdict, a keyword net only as a
  WARN audit of declared answers.**  Length, keywords and the `d` glyph were each measured to fail as classifiers.

*Honest limits: one seat; the "nearly all genuine" reading of the 63 CHECK net hits is from 150-char heads, the
120 no-`d` hits were sampled at 14; the per-tool consequences under ANY-PHASE are EVIDENCE.md's re-statements of
the cited lines, not tool runs; nothing here was run against a gate.*
