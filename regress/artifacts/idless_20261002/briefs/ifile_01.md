ID-LESS TABLE CHECK -- part 01: the 127 NEW rows

Open with the token `ASTRAIFILE_01_ALIVE` on its own line, then ONE verdict line:
`VERDICT: <w> of 127 NEW rows wrong; <m> rows missing; <d> duplicate pairs; qhppcdecode: CONCEDE or HOLD`.

**Context.**  `OUTSTANDING_BUGS.md` (this project's bug queue) carries some open work in prose only, with no short id.
You scanned for those entries at commit `db8b1a33`, the grok seat ruled each one first-hand, and you confirmed,
overturned or amended each ruling.  The record of all that is
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\idless_20261002\IDLESS_DISPOSITIONS.md` (292 dispositions).
A table of what the queue is now owed was derived from it.  Everything below is under
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\idless_20261002\` unless a full path is given:
* `IDLESS_FILING.tsv` -- the mechanical derivation (`mk_ifiling.py.txt`): the governing line per disposition is your
  amendment where one exists, else grok's ruling;
* `IDLESS_OVERLAY.tsv` -- 37 titles the grok seat wrote where your amendment governs and gives an instruction instead
  of a title (`briefs\grok_ititles.md` -> `grok\grok_ititles.txt`: 37 written, none of your amendments disputed), and
  two ids that each cover two queue passages;
* `grok\grok_icompound.txt` -- grok on three dispositions whose governing line names MORE THAN ONE outcome (the
  derivation reads one), which adds two NEW rows the derivation had dropped;
* **`IDLESS_TABLE.tsv` -- the result: 127 NEW rows (7 HIGH, 27 MED, 93 LOW), 40 CLOSE-RECORD, 6 UNSETTLED.**  This part
  checks the 127 NEW rows; part 02 checks the rest.
A filing unit prepared today, `#554`, files the open rows of your two reviews; its rows, with their titles, are in
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\draft\section554.draft.md` (being
committed as the tail of `OUTSTANDING_BUGS.md`).

**Please do not simply ratify.**  The table was assembled by scripts of the main loop's from free text, and its titles
come from three places.  Read committed source with
`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show 7440e129:<path>`, the queue passages with
`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show db8b1a33:OUTSTANDING_BUGS.md`, the artifacts from disk.  The tree
under review is `GXEMUL-SEC`; ignore any other `src/` under the project root.  Write nothing, build nothing, run
nothing that changes a file.

**A. The rows.**  One line per failure:
`<id> | table says <X> | should be <Y> | the line (file:line) | confidence`.
1. For every NEW row: the id, the grade and the queue passage are the governing disposition's.  A grade of yours that
   RAISES grok's is marked in your amendment; say which rows rest on such a raise, because a raise by the family that
   made the scan is not adopted on its say-so and goes back to grok.
2. The 88 titles taken from a quoted title in the governing line (80 from grok's ruling, 8 from your amendment; the
   last column of `IDLESS_TABLE.tsv` says which): is each the title the governing line gives?
3. The 37 titles grok wrote (`IDLESS_OVERLAY.tsv`, the `title` lines): does each state the row AS YOU AMENDED IT, no
   wider and no narrower, and is it true of the source at `7440e129`?  These are the rows where a paraphrase is most
   likely to have dropped a condition.
4. The two merged ids (`qharmexalign`, `qhnetxlog`): is each ONE defect recorded at two passages?

**B. Rows that are missing.**  `<queue lines> | <dispositions file:line> | the row that is owed`.
1. Any disposition whose governing outcome is NEW and which has no row in the table.
2. Any OTHER disposition whose governing line names more than one outcome (a FILED part and a NEW part, or two ids).
   A scan for two kind words in one governing field found four -- queue lines 1705-1716, 2616, 8148 and 16997-17000 --
   and I believe that scan can miss a second outcome written without its kind word; check.

**C. Duplicates.**  `<id> | <the other id> | where the other row is | why they are one defect`.
Two rows of the table that are one defect; a row that duplicates a row `#554` files; a row that duplicates a row
already in `tools/pipeline/ledger.json` at `7440e129`.

**D. One amendment grok disputes: queue lines 1705-1716.**  Your amendment (`IDLESS_DISPOSITIONS.md`, slice 01) made
the entry `FILED HIGH ppcfmasingle` for `fmadds`/`fmsubs` plus `NEW HIGH qhppcdecode` for the other eight pending
PowerPC encodings.  grok's answer (`grok\grok_icompound.txt`, part A): `ppcfmasingle`, as `#554` files it, covers the
opcode-59 `fnmadds`/`fnmsubs` and says in its own title that `fmadds`/`fmsubs` stay in the queue's PROSE at
`OUTSTANDING_BUGS.md:1705` and `:1712` -- which is this very entry -- so `qhppcdecode` must cover all TEN encodings
that `regress/ppc_halt_probe.py:257-279` lists as still stopping emulation, `fmadds` and `fmsubs` included, or those two
are filed nowhere.  The table follows grok.  Check `...\astrafiling_20261002\draft\section554.draft.md` (the
`ppcfmasingle` row) and the probe, then say `CONCEDE` (ten) or `HOLD` (eight, with the id that files the other two).

End with `DENOMINATOR: <a> of 127 NEW rows checked against their governing line; <b> of the 37 grok titles checked
against the source; read <c> of the ten slices of IDLESS_DISPOSITIONS.md for part B`.
