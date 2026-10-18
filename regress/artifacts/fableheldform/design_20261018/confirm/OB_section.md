### 2026-10-18 -- `fableheldform`: seventeen walled Fable entries carry a stage token; nine rows that shut while a stage awaited Fable go back to held; the wider class is filed

* **`fableheldform` (MED) HELD for fable5** -- the conversion is done.  Under the owner's 2026-10-17 directive a Fable
  wall is a SEAT FAILURE recorded as a HELD marker with a question, never agreement; seventeen entries had recorded one
  in untokened prose, which `stage_tokens.is_answer()` counts as an answer.  Fifteen now carry the HELD token (prose and
  receipt kept); `cxlaunchquotation`'s 2026-10-16 v2 wall and its V3 wall carry the non-answer token instead, because a
  later pass superseded each and Fable answered that one (V4, 2026-10-17) -- a HELD tag dated the day of V4 would stay
  live forever under the strictly-later discharge rule (Grok 4.7).  Design pass 1 (`regress/artifacts/fableheldform/
  design_20261018/`): GPT-6 Astra, Grok 4.7 and GLM 5.3 all chose this (option A); Fable 5.1 walled, so this row's own
  review is held.
* **NINE ROWS REOPENED, `closed` -> `held`**: `sgirekills`, `sgirandomcolour`, `mapledmaaddr`, `xscaleinten`,
  `ppcrldimimask`, `ppcrlwimiwidth`, `ppcgateimageskip`, `cxlaunchquotation`, `dashokclass`.  Each was shut on 2026-10-17
  or 2026-10-18 while its review stage (and `sgirekills`' research stage) held a Fable wall written as an untokened
  note; a row may not close while a stage awaits a seat (`check_stage_panels.py`, CLOSED-WHILE-HELD), so with the token
  in place each is held until Fable answers.  Each keeps its closure object (the record of that close), names in
  `reopened` every commit whose subject called it closed (section L), heads its state note with the warrant, and adds to
  its `hold_question` the packet of the pass Fable walled on.  GPT-6 Astra's confirm on `ip30abortkill` earlier the same
  afternoon is the precedent.  **The owner question the panel named** -- may a row close while its research or review
  question is held for Fable (a change to section H and the state semantics)? -- is in `fableheldform`'s
  `hold_question`; until it is answered, rulings and commits proceed and closes wait.
* **`wiringcliff`** -- `#565`'s two Fable stages (pass 1, pass 2 + F2) carry the HELD token and their question.
* **`untokenedanswers` (MED, open)** -- the same defect for every seat and date: a keyword correlate (known false
  positives) finds about 497 untokened non-answers on 129 rows, 81 of them closed, among them deliberate owner-roster
  exclusions that section H's nine-seat count reads as seats that answered (`ppcgateimageskip`'s review is 9/9 only that
  way).  Owed: a forward-only structural check that reds a NEW untokened non-answer, an owner ruling on how an excluded
  seat is recorded, and row-by-row correction of the history when a round touches it (no sweep).
