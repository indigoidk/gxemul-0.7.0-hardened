LEDGER CENSUS -- confirm or overturn the grok seat's reading of 37 closed rows that have no commit

Open with the token `ASTRACENSUS_ALIVE_1002` on its own line, then ONE verdict line:
`VERDICT: <c> confirmed, <w> wrong, <u> not checked, of 37 rows; commits to fill: <f> confirmed of 9`.

This is a RECORDS check: whether a ledger row's state matches the committed tree.  Write nothing, build nothing, run
no emulator.  The tree is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` at HEAD `c29a5fd3`; read committed files with
`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show HEAD:<path>` and history with `git -C ... log`; ignore any other
`src/` under the project root.  Please do not simply ratify: the grok seat read the WORKING tree (it cannot run git),
so where a file is dirty on disk its lines may be the working copy's; you can read the commit.

**Context.**  Commit `c29a5fd3` (`#555`) filed the class row `closeassessrows`: a 2026-08-27 sweep closed ledger rows
on the adjudicator's note `CLOSE (assess)`, which signs off a row's assess STAGE, and eight of those rows still name
undone work.  The population the class can draw from is every row that is `closed` with an empty `commits` field: 47.
grok had read ten; it has now read the other 37 (`regress\artifacts\closeassess_20261002\grok\grok_closedcensus.txt`,
brief `briefs\grok_closedcensus.md`): 20 SHIPPED (work in the tree, the commits field never filled), 14 NOTHING OWED,
3 WORK STILL ALIVE (`cmtattr`, `gdromcontractresidual`, `unreadseats23`).  It names the commit or round for 9 of the
20 and found no sha for 11.  Nothing of this is applied yet: the plan is a records round that fills the 20 commits
fields where a commit can be named, adds the 3 members to `closeassessrows` with a note on each, and leaves the 14.

**Part A -- the 37 lines.**  For each: is grok's reading right?  Report only the wrong ones:
`<n> | <id> | WRONG: <what grok missed or misread, path:line> | <what the row's disposition should be: SHIPPED <sha or #NNN> / NOTHING OWED / WORK STILL ALIVE: <what, and the open row that carries it, or "no carrier">>`
For the three WORK STILL ALIVE rows, say whether you agree they belong to `closeassessrows` (undone work, no open
carrier) or whether an open row already carries the work.

**Part B -- the commits to fill.**  grok names: `wdcwidth4` = e61ccd8; `m88kexcrrtrapmode` = #502;
`alphatbinegsel` = #520; `mk48nvramkill` = #521; `ppcrldiclzero` = #522; `scorehyphenfp` = #529 (7440e129);
`lcalenzerodrop` = #538; `nineseatreminder` = #554; `panelargvcap` = "Round panelargvcap" (no sha).  Using `git log`
(`git -C ... log --oneline --all -- <path>` or a grep of the subject lines for the round number), give the SHA for each
of the nine and, where you can, for the eleven grok found no sha for (`fbwitness`, `ledgerwitness`, `smhang`,
`asanunbuildable`, `hookctlgate`, `hookdurability`, `propagatecpsilent`, `divsweeplines`, `novpadfourth`,
`boilerplateprefix`, `wiringshghost`).  One line each: `<id> | <sha> <subject, cut short> / NO COMMIT FOUND: <why>`.
A sha must be a commit that touched the file the row is about or whose subject names the row or its round number;
say which.

End with `DENOMINATOR: A <rows read> of 37; B <rows looked up in git log> of 20`.
