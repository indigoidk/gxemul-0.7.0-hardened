#557, THE closeassessrows AUDIT -- the closing check of what it commits

Open with the token `ASTRA557_ALIVE_1002` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CLOSES -- nothing wrong in parts A to D`
`VERDICT: <n> things wrong (A: <a>, B: <b>, C: <c>, D: <d>)`

This is a RECORDS check: a ledger, two queue texts and one checker's comment against the commits and the code they
cite.  Write nothing, build nothing, run no emulator.  Please do not simply ratify: the shas are yours, the
overturns are yours, and the checker's corrected comment follows your review -- those are the parts you are least
likely to test.

**Where things are.**  The tree is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` at HEAD `1329d894` (`#556`); committed files
with `git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show HEAD:<path>`, history with `git -C ... log`.  Everything else is
under `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\closeassess_20261002\`.

**What the unit does** (`draft\changelog557.draft.md` says it in full):
* fills the commits field of 18 closed rows from your census confirmation (`aconf_census\codex_aconf_census.txt`,
  part B); leaves `asanunbuildable` empty on purpose; the staging script re-checked every sha (the commit exists and
  touches the file you named, or names the row or its round in its subject);
* notes four rows as new members of `closeassessrows` (`cmtattr`, `gdromcontractresidual`, `unreadseats23`, `smhang`),
  re-opening none;
* lands the parked `tools/pipeline/check_boilerplate.py` repair with its comment corrected per your `aconf_parked`
  review (`draft\parked_check_boilerplate_v2.diff` is the diff against HEAD as it will be committed); its commits
  field is filled with the new commit's own sha by the post step;
* holds the parked `regress/gdrom_default_probe.py` edit, as you advised, with the reason recorded.

**Part A -- the ledger** (`draft\ledger557.draft.txt`: every changed row, its commits before and after, the note's
start).  For each of the 18 fills: is the sha the right one (the commit that did the row's work)?  For the four
member notes and the `asanunbuildable` note: is anything said that the row or the commit does not support?  Report
only the wrong ones: `A | <id> | <what is wrong, with the commit or line>`.

**Part B -- the checker.**  `draft\parked_check_boilerplate_v2.diff`.  Your `aconf_parked` 1b named four things wrong
in the comment: the preamble length (81, not 66), "the day it landed", the recall overstatement, the stale header.  Is
each corrected, and is anything new in the comment untrue?  Is the code change still exactly the key change
(`strip_seat(note, seat).casefold()`), `EXCERPT = 60` display-only, and the `[:72]` slice?  `B | <line> | <what>`.

**Part C -- the texts** (`draft\changelog557.draft.md`, `draft\section557.draft.md`, `draft\msg557.draft.txt`).  Any
sentence that is false, any number the artifacts do not give (18 filled, 1 empty, 4 members, 12 members now, 14
nothing owed, 20 shipped, 37 read).  In particular the account of your own two answers and of the three overturns.
`C | <text:line> | <what>`.

**Part D -- anything else**, including whether `xfamscope` (whose two edits grok found made) should have had its
commit looked up too.

End with `DENOMINATOR: A <rows read> of 24 changed rows; B <hunks read> of the checker diff; C <texts read> of 3`.
