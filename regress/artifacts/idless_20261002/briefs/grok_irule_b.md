THE ID-LESS TABLE -- GPT-6 Astra's check of the closing sentences, the FILED entries, the KEEP-AS-IS entries and the UNSETTLED ones: concede or hold

FIRST line of your answer: `VERDICT: <c> conceded, <h> held, of 43 items`.
SECOND line: the token `GROK_IRULE_B_ALIVE_1002`.  THIRD line: quote verbatim the first line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`.

**Context.**  You ruled the id-less entries of this project's bug queue; GPT-6 Astra confirmed or amended each ruling;
a table of what the queue is owed was derived from that
(`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\idless_20261002\IDLESS_TABLE.tsv`, with
`IDLESS_NOTOWED.tsv` for the entries that open no row).  Astra has now checked everything except the NEW rows:
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\idless_20261002\ifile_02\codex_ifile_02.txt`
("6 of 40 closing sentences wrong; 16 of 84 FILED entries wrong; 18 of 35 KEEP-AS-IS entries owe something; 3 of 6
UNSETTLED wrong").  You are the ruling seat of this scan, and Astra wrote the scan: nothing in its answer is adopted
on its say-so.  Each of the 43 items needs your first-hand ruling.

**The tree.**  `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` (git) at commit `7440e129`; the queue line numbers are commit
`db8b1a33`'s.  If `git show` is refused to you, say so and read the files on disk (the queue by its text).  The rows
that today's filing unit `#554` adds are in
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\draft\section554.draft.md`; existing rows
are in `tools/pipeline/ledger.json` and in the queue file.  Never read any other `src/` under the project root; never
`git status` or `git diff`.  Write nothing.

**For each item, in the order of Astra's answer, ONE line:**
`<S1..S6 / F1..F16 / K1..K18 / U1..U3> | <queue lines> | CONCEDE / HOLD: <why, with path:line> / CONCEDE IN PART: <which part> | RESULT: <see below> | <the lines you read>`

* **S1-S6, the closing sentences.**  Astra says each closes more than the source supports, or is cut short.  RESULT:
  the sentence that should stand (one or two sentences, true at `7440e129`, naming a function or a construct rather
  than a line number), and, where the passage keeps an open item, WHERE that item is filed: an existing id, a row of
  the table, or `NEW <grade> <id> "<title>"`.
* **F1-F16, entries filed under an id.**  Twelve are coverage failures: Astra says the row the entry is filed under
  does not cover everything the passage says is open.  RESULT: `FILED <id> covers it` / `FILED <id> for <part>, and
  <the rest> is filed under <id>` / `NEW <grade> <id> "<title>" for <the rest>`.  Four are `OB-22` / `OB-24`: those
  ids exist as plain text in the queue's table (`OUTSTANDING_BUGS.md:2909`, `:2916`) and have no ledger row.  RESULT
  for those: is the plain-text entry a real open filing that the passage can point at, yes or no.
* **K1-K18, entries you ruled KEEP-AS-IS.**  Astra says each passage still records open work.  For sixteen it names
  an id that already carries the work; for two it says a NEW row was lost (`qhmipstlbwarn`, `armcpsrprint`).  RESULT:
  `NOTHING OWED` (hold) / `CROSS-REFERENCE <id>` (the passage should point at that row; no new row) /
  `NEW <grade> <id> "<title>"`.  A cross-reference is owed only if the named row really carries that work: check it.
* **U1-U3, the UNSETTLED entries.**  RESULT: `SETTLED: <which way, and what the passage should then say>` /
  `STILL UNSETTLED: <the measurement or the source that would settle it>`.

I believe -- check it, do not take it -- that the commonest real failure here is a passage with TWO open items of
which the table handled one.  Where you concede, say what happens to the second item; where you hold, say why the
passage has no second item.

End with `DENOMINATOR: <s> of 43 items read in the source or the queue; <t> ruled from the dispositions text alone`.
