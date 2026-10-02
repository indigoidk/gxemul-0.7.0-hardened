ID-LESS TABLE CHECK -- part 03: six of your findings the grok seat HOLDS against; concede or hold

Open with the token `ASTRAIFILE_03_ALIVE` on its own line, then ONE verdict line:
`VERDICT: <c> conceded, <h> held, of 6`.

**Context.**  Your parts 01 and 02 found 68 things wrong with the table of what the queue's id-less entries owe
(`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\idless_20261002\ifile_01\codex_ifile_01.txt`,
`...\ifile_02\codex_ifile_02.txt`).  The grok seat, which ruled the scan, went through all 68 first-hand
(`...\idless_20261002\grok\grok_irule_a.txt`: 25 conceded, 0 held; `grok_irule_b.txt`: 37 conceded, 6 held).  The 62 it
conceded are being applied as it wrote them.  These are the six it holds; its reasons are in `grok_irule_b.txt` under
the item numbers given.  Read them there -- I quote only the gist.

Read committed source with `git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show 7440e129:<path>` and the queue with
`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show db8b1a33:OUTSTANDING_BUGS.md`.  The tree under review is
`GXEMUL-SEC`; ignore any other `src/` under the project root.  Write nothing, build nothing.

**For each, ONE line:** `<item> | CONCEDE / HOLD: <why, with path:line> | <what the table should then say>`

1. **F6, queue 1987-1988** and **2. F8, queue 2456-2459** and **3. F13, queue 4802-4803** -- you called these FILED
   entries "NOT FOUND through the stipulated existence routes" because `OB-22` and `OB-24` are plain-text ids of the
   queue's old table (`OUTSTANDING_BUGS.md:2909`, `:2916`) with no ledger row and no backticks; you also said the
   plain-text entries do exist.  grok holds that each is a real, open filing the passage can point at.  The existence
   rule in my brief was mine and was too narrow.  Is there any SUBSTANTIVE objection left -- is `OB-22` (or `OB-24`)
   closed, or does it fail to cover the passage -- or do you concede that a pointer to the plain-text entry is right?
4. **F9, queue 2730** -- the Jazz sentence has two halves; grok holds that `jazzlbmask` (a row `#554` files) carries
   the unused local-bus enable bits and `OB-22` the vector-acknowledge half, so nothing is unfiled.  Same question.
5. **F12, queue 4676-4682** -- you: `m88kidleslotsem` does not cover the passage, because its title covers premature
   idling after a polled-word write while the passage is about accumulating, MMIO and order-sensitive delay slots
   running once per BREAK.  grok: one recorded approximation -- those slots ARE the once-per-BREAK limit that
   `m88kidleslotsem` names, and the crosspage sentence starts at 4683, outside this passage.  Read the row as `#554`
   files it (`...\regress\artifacts\astrafiling_20261002\draft\section554.draft.md`, search `m88kidleslotsem`) and
   `src/cpus/cpu_m88k_instr.c` around the idle fold: would fixing what that row's title states leave the passage's
   slots still wrong?  If yes, HOLD and give the row that is owed: `NEW <grade> <id> "<title>"`.
6. **K10, queue 2742-2745** -- you: the passage OWES deferred macppc OpenFirmware and device completion.  grok:
   NOTHING OWED -- the passage itself calls it a future enhancement outside the safety scope, no defect is stated, and
   no row carries an enhancement.  This project's queue files defects, owed measurements and owed records; is there
   one here?  If you hold, name it as a row: `NEW <grade> <id> "<title>"`.

End with `DENOMINATOR: <a> of 6 read in the queue and the source`.
