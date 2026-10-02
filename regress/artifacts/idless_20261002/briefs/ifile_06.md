ID-LESS TABLE CHECK -- part 06: the three repairs of your part 05

Open with the token `ASTRAIFILE_06_ALIVE` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CLOSES -- the three repairs are right and nothing else changed`
`VERDICT: <n> things wrong`

This is a RECORDS check: whether three corrected statements match the tables, the committed code and the manual they
cite.  Write nothing, build nothing, run no emulator.  Please do not simply ratify: a repair is new text and can be
wrong in its own way.

**Where things are.**  Everything is under
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\idless_20261002\`.  Read committed files with
`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show HEAD:<path>` (HEAD is `1202d342`).  The manuals are in
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\`.

**THE DELTA, whole:** `draft\REPAIRS_since_ifile05.diff` -- unified diffs of the tables and the draft texts from what
your part 05 read (kept in `before_ifile05_repairs\`) to what stands now.  Nine hunks.  A change there that is none of
the three repairs below, or of the numbers that follow from them, is a finding.

1. **E1 -- "six, not five".**  The count is no longer made from a phrase.  `draft\prep555.py.txt` (search `live =`)
   counts the sentences that name a LIVE row: a row this unit files, a ledger row whose state is open, held or in
   work, or a row the queue lists with no ledger row of its own.  It gives 6 of 43, and the section names the ids:
   `qhppcdecode`, `arcpartlba`, `qhppcni`, `armalignexc`, `closeassessrows`, `pcc2c040kill`, `pcc2lineexit` (seven ids,
   because one sentence names two).  Are those your six sentences (`IDLESS_SENTENCES.tsv:4,9,13,23,33,43`), and do
   the section (`draft\section555.draft.md`), the changelog (`draft\changelog555.draft.md`) and the manifest now
   agree with each other?
2. **B2 -- "require" to "permit".**  The sentence for 5655-5661 (`IDLESS_SENTENCES.tsv`, and as placed in
   `draft\inplace555.draft.diff`, search `SETTLED BY THE MANUALS`) now reads "... leave ll_bit set on that path,
   which those sentences permit; they do not require it, because Book III also lets a partly executed `stwcx.` have
   cleared the reservation (`ppc_oea_book3_v201.txt:4067-4070`)."  Is that what Book III 5.6 says, and is the whole
   sentence now a fair reading?
3. **C -- the stale clause.**  The changelog's paragraph on the agy seat's audits now says the passage of `qhshsqat`
   is also pointed at `sh4sqexpevt` for the PREF exception kind, and that the ruling had named `sh4sqwrite` as well
   until your part 04 and grok's concession.  `prep555.py.txt` refuses to generate the text unless the table's
   carriers for that ruling are exactly `sh4sqexpevt`.  Does the changelog now agree with `IDLESS_CARRIED.tsv` and
   with its own later paragraph?

Also read the changelog's new account of your part 05 (search `ifile_05`): is anything said there of your answer
that is not so?  The line `<OWED: GPT-6 Astra's verdict on the three repairs>` is where this job's verdict line goes.

For each: `<n> | RIGHT / WRONG: <why, path:line>`.  End with `DENOMINATOR: <a> of 3 repairs read; <h> of 9 hunks
read`.
