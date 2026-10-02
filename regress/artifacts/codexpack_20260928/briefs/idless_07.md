QUEUE HYGIENE -- `OUTSTANDING_BUGS.md` lines 15601-18200 of 22670 at `db8b1a33`: entries that record an OPEN defect or owed work WITHOUT a short id

Open your answer with the token `CODEXPACK_IDLESS_07_ALIVE`.  Second line: the VERDICT line specified at the end.

**The tree.**  `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` (git): a hardened fork of the GXemul 0.7.0 full-system machine emulator, in C99.  Read
COMMITTED files only, at commit `db8b1a33`: `git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show db8b1a33:<path>` (number the lines with
`awk '{print NR": "$0}'` or use `grep -n`).  The WORKING TREE carries other people's uncommitted work -- do not read
source files from disk.  Ignore every other `src/` under the project root (`src/`, `est/`, `build/`, `build-asan/`,
`_archive/` are other copies; a copy reports line numbers off by hundreds).

**Reading scope.**  `src/`, `regress/*.py`, `regress/*.sh`, `regress/*.c`, `OUTSTANDING_BUGS.md` and `CHANGELOG.md`
(all at `db8b1a33`), the hardware manuals `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\*.txt` (on disk), and the files this
brief names by path.  Do not read anything else under `regress/artifacts/`, and not `tools/pipeline/ledger.json`.

**This is a reading task.**  Build nothing, run nothing, write nothing.  Do not write programs or patches: describe
behaviour and cite lines.  Cite `path:line` at `db8b1a33` for every claim and quote the line when the claim rests on its
exact text.  Say "not checked" rather than guessing.  Where a claim is ARITHMETIC (an offset, an index range, a count)
enumerate the values rather than reasoning about them.

**Context.**  The queue file names most rows by a short backticked id (`wdcnien`, `sh4sqexpevt`, ...).  Some entries
record a defect, an owed measurement or an owed correction in PROSE only -- and an adjudication pass was overturned
six times in one batch for filing as new what such prose already recorded.  Read `git show db8b1a33:OUTSTANDING_BUGS.md`
lines 15601-18200 ONLY (number them with awk; do not read outside the range except to see whether an entry that starts
before line 15601 or ends after line 18200 is cut by the range -- say so and stop there).

For EVERY entry in the range that records something OPEN -- a defect not fixed, a measurement or correction owed, a
row "to file" -- and carries NO backticked id of its own, write one line:
`<line range> | <the entry's own words, one clause, quoted> | STILL OPEN AT HEAD: yes / no / not checkable by reading (<why>) | <one sentence of source evidence, path:line at db8b1a33, when you checked> | PROPOSED ID: <short, lowercase, no spaces, not already in the file, no "kill"> | SEVERITY by the rule (HIGH: the process ends, a memory access leaves a buffer, or progress stops; MED: differs from the hardware documentation; LOW: records, diagnostics, coverage)`
Skip: entries with an id; closed, resolved, superseded or withdrawn entries; pure narrative.  Where the range holds a
"dated tail" entry that is a diary line rather than a queue item, say so once and skip those.
Then: **(a)** entries in the range whose prose says OPEN but whose source at `db8b1a33` shows the defect gone (quote the
line that shows it) -- these are false records; **(b)** the DENOMINATOR: how many entries the range holds, how many
you classified, how many you could not.
VERDICT line (the second line of your answer): `VERDICT: <m> id-less open entries in lines 15601-18200 -- <h> HIGH, <e> false records`.
