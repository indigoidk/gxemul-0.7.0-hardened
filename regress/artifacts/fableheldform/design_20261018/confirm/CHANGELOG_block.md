# Records, 2026-10-18: `fableheldform` -- seventeen walled Fable entries carry a stage token; nine rows that shut while a stage awaited Fable go back to held; the wider class is filed

**The defect** (filed by `#566`).  The owner's 2026-10-17 directive records a Fable wall as a SEAT FAILURE with a HELD
marker and a question, never as agreement.  Seventeen `fable5` entries since 2026-10-16 recorded one in untokened prose
("NOT FIRED", "SEAT FAILURE", "HTTP 429"), and `stage_tokens.is_answer()` counts any untokened entry as an answer -- so
the checkers read Fable as having answered, and nine rows passed section H's no-close-while-held rule and were shut on
2026-10-17 and 2026-10-18 with a Fable stage still owed.  GPT-6 Astra's confirm on `ip30abortkill`'s closure records
(`d42c76a8`, an hour earlier) is what exposed it: a review stage then reads complete on older answers.

**What this commit does** (records only):
* tags fifteen walls with the HELD token, keeping each entry's prose and receipt, and `cxlaunchquotation`'s 2026-10-16
  v2 and V3 walls with the non-answer token instead -- a later pass superseded each and Fable answered that one (V4,
  2026-10-17), so a HELD tag dated that day could never be discharged under the strictly-later rule (Grok 4.7);
* moves nine rows `closed` -> `held` -- `sgirekills`, `sgirandomcolour`, `mapledmaaddr`, `xscaleinten`,
  `ppcrldimimask`, `ppcrlwimiwidth`, `ppcgateimageskip`, `cxlaunchquotation`, `dashokclass` -- each keeping its closure
  object as the record of the close, naming in `reopened` every commit whose subject called it closed (section L),
  heading its state note with the warrant, and adding to its `hold_question` the packet of the pass Fable walled on;
* adds `#565`'s two Fable stages to `wiringcliff`'s held work, with their question;
* moves `fableheldform` `open` -> `held` (its own review is Fable's), with the design pass's seat entries;
* FILES `untokenedanswers` (MED): the same defect for every seat and date -- about 497 entries on 129 rows by a keyword
  correlate (`regress/artifacts/fableheldform/design_20261018/CENSUS_wide.txt`), including deliberate owner-roster
  exclusions that section H's nine-seat count reads as answers.  Not swept: a forward-only check and an owner ruling on
  how an excluded seat is recorded are owed first.

**Design pass 1** (`regress/artifacts/fableheldform/design_20261018/`): GPT-6 Astra, Grok 4.7 and GLM 5.3 all chose
option A (tag in place, reopen to held).  Astra added option E -- an owner-authorized policy allowing a close with an
explicitly deferred Fable review, changing section H and the state semantics together -- and ruled that only E needs
the owner, the state correction being licensed by the ledger's own `_RETROACTIVE_OR_FORWARD_ONLY` semantics (`state` is
a live field; correcting it rewrites no history); Grok agreed no fresh ruling is needed; GLM held that reopening
committed closures is the owner's call and drafted the question.  **The owner question is recorded in
`fableheldform`'s `hold_question`**: may a row close while its research or review question is held for Fable?  Until it
is answered, rulings and commits proceed and closes wait.  Flags taken: the census's date cutoff missed
`cxlaunchquotation`'s 2026-10-16 wall (Astra, GLM); `cxlaunchquotation` walled on V3 and V6 as well as V7 (all three);
my brief said `ip30abortkill` "was committed held" while that commit was still in its hook (GLM); `ppcgateimageskip`'s
review is 9/9 only through seven untokened notes for owner-excluded seats (Grok).  Fable 5.1 walled (HTTP 429,
`fable5_p1_WALL.txt`), held.  {CONFIRM}  Opus 5.5, agy, kimi, deepseek and minimax deliberately not fired (the owner's
2026-10-17 roster).  `ledger.json`, `OUTSTANDING_BUGS.md`, `fable_queue.md`, `matrix.html` and this block only.
