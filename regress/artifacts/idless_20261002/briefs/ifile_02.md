ID-LESS TABLE CHECK -- part 02: the 40 closing sentences, the 6 unsettled entries, and the entries that open no row

Open with the token `ASTRAIFILE_02_ALIVE` on its own line, then ONE verdict line:
`VERDICT: <s> of 40 closing sentences wrong; <f> of 84 FILED entries wrong; <k> of 35 KEEP-AS-IS entries owe something; <u> of 6 UNSETTLED wrong`.

**Context.**  `OUTSTANDING_BUGS.md` (this project's bug queue) carries some open work in prose only, with no short id.
You scanned for those entries at commit `db8b1a33`, the grok seat ruled each one first-hand, and you confirmed,
overturned or amended each ruling:
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\idless_20261002\IDLESS_DISPOSITIONS.md` (292 dispositions).
A table of what the queue is now owed was derived from it.  Everything below is under
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\idless_20261002\` unless a full path is given:
* `IDLESS_TABLE.tsv` -- 127 NEW rows (part 01 checks those), **40 CLOSE-RECORD, 6 UNSETTLED**;
* `IDLESS_NOTOWED.tsv` -- the dispositions that open no row: **84 FILED** (the entry already has an id) and
  **35 KEEP-AS-IS** (history, or a rule);
* `IDLESS_FILED_CHECK.tsv` -- for each FILED disposition, the id(s) it names and where each exists (a mechanical
  lookup).  It was made before three rows were added to today's filing unit `#554`: `ramspaninval`, `jazzlbmask` and
  `tcpdebugopts` read NOWHERE in it and are now rows `#554` files;
* `grok\grok_icompound.txt` -- part B: seven closing sentences the grok seat wrote out where your amendment governs
  and gives a fragment, a correction or an instruction instead of the sentence.
`#554`'s rows, with their titles, are in
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\draft\section554.draft.md`.

**Please do not simply ratify.**  Read committed source with
`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show 7440e129:<path>`, the queue passages with
`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show db8b1a33:OUTSTANDING_BUGS.md`, the artifacts from disk.  The tree
under review is `GXEMUL-SEC`; ignore any other `src/` under the project root.  Write nothing, build nothing, run
nothing that changes a file.

**A. The 40 CLOSE-RECORD rows.**  Each says: the queue's prose reports something open, the source shows it is not, and
ONE sentence will be added at the passage (the old text stays; this project corrects a record in place and keeps what
it corrects).  One line per failure:
`<queue lines> | the sentence says <X> | should say <Y> | the line (file:line) | confidence`.
1. Is the CLOSURE right -- does the source at `7440e129` show the thing done, for the WHOLE passage?  A passage with
   two open items, of which the sentence closes one, is a failure: name the item left open.
2. Is the SENTENCE true at `7440e129`, and does it say what the governing disposition says?  33 are the grok ruling's
   own quoted sentence; 7 are grok's writing-out of YOUR amendment (`grok\grok_icompound.txt`, part B) -- for those,
   is your amendment carried in full?
3. A sentence that cites a `path:line`: does that line say it?  (The sentence will sit in the queue for years; a line
   number in it will drift.  Say where a function or construct name would serve better.)

**B. The 84 FILED entries.**  One line per failure:
`<queue lines> | filed under <id> | <NOT FOUND / the row does not cover: what is left out> | the line | confidence`.
1. Every id named must exist: a ledger row at `7440e129`, a backticked id in the queue file, or a row `#554` files.
   `IDLESS_FILED_CHECK.tsv` lists four entries with no parseable id (they name `OB-22`, `OB-24`, or none) and four
   ids that exist only in the queue file.
2. The row must COVER the entry.  I believe the commonest failure is a passage with two open items filed under a row
   whose title names one; check each entry's passage against the title of the row it is filed under.
3. Three dispositions name more than one outcome (queue lines 2616, 8148, 16997-17000; `grok\grok_icompound.txt`,
   part A): is each FILED part filed where grok says, and is `armcoprocstop` (your name, in the amendment at
   16997-17000) the same defect as `#554`'s `armcp15cp14exits`?

**C. The 35 KEEP-AS-IS entries and the 6 UNSETTLED.**
`<queue lines> | OWES: <the open work the passage records, with path:line> | confidence` for a KEEP-AS-IS entry whose
passage records work that is not done at `7440e129`; and for an UNSETTLED entry,
`<queue lines> | SETTLED BY THE SOURCE: <which way, path:line>` or `THE MEASUREMENT NAMED IS NOT THE ONE THAT SETTLES IT: <which does>`.

End with `DENOMINATOR: <a> of 40 sentences checked against the source; <b> of 84 FILED entries checked against the
row they are filed under; <c> of 35 KEEP-AS-IS and <d> of 6 UNSETTLED read in the queue text`.
