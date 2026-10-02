ID-LESS QUEUE SCAN -- SECOND-SEAT VERIFICATION, slice 07: `OUTSTANDING_BUGS.md` lines 15601-18200 at `db8b1a33`

Open your answer with the token `AGYPACK_IDLESSVERIFY_07_ALIVE`.  Second line: the VERDICT line specified at the end.

**The tree.**  `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC` (git): a hardened fork of the GXemul 0.7.0 full-system machine
emulator, C99.  Read COMMITTED files at `db8b1a33` (`git -C C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC show db8b1a33:<path>`,
numbered with `awk '{print NR": "$0}'` or `grep -n`); the WORKING TREE carries other people's uncommitted work --
do not read source from disk.  Never read `C:\DocumentNoSnc\cc\GXEMUL\src\`, `est/`, `build/`, `build-asan/` or
`_archive/` (other copies; a copy reports line numbers off by hundreds).  Read nothing under `regress/artifacts/` except
the files this brief names.  Hardware manuals: `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\*.txt`.
**Write nothing; run nothing; build nothing; change nothing.**  Return text only.  Cite `path:line` at `db8b1a33` for every
claim; say "not checked" rather than guess.  Where a claim is arithmetic, enumerate the values.

**Context.**  The queue file `OUTSTANDING_BUGS.md` names most rows by a short backticked id (`wdcnien`, `sh4sqexpevt`,
...).  Some entries record a defect, an owed measurement or an owed correction in PROSE only, with no id -- and an
adjudication pass was once overturned six times in one batch for filing as new what such prose already recorded.  A
reviewing model (GPT-6 Astra) scanned lines 15601-18200 and claims **9 id-less OPEN entries**, each with a line
range, the entry's own words, a STILL-OPEN-AT-HEAD judgement with source evidence, a proposed id and a severity:
`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\codexpack_20260928\idless_07\codex_idless_07.txt`
(its brief: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\codexpack_20260928\briefs\idless_07.md`).  That is ONE reviewer's reading.  Nothing has been filed or closed from it.  **You are the
second seat**: a records round will assign ids to the live entries and close the dead ones ONLY on claims two seats
agree on, so an unverified claim is worth nothing to it and a WRONG claim costs a wrong id or a wrong closure.

**For EVERY row of that answer's table write one line:**
`<line range> | ID-LESS: yes / no "<the backticked id it carries>" | OPEN-CLAIM: RIGHT / WRONG: <why> / UNSETTLED: <what would settle it> | SEVERITY: <HIGH/MED/LOW> (<agree / raise / lower, why>) | <the lines you read, path:line at db8b1a33>`
ID-LESS means: no backticked id in the entry's own heading or first line and none in its enclosing `###` heading --
quote the heading.  OPEN-CLAIM: re-derive the "STILL OPEN AT HEAD" judgement yourself from the source at `db8b1a33`
(open the cited file; if the entry says a fix is owed, is the defect still in the code? if it says a record is wrong,
is it?).  A "false record" claim (the prose says OPEN while the source shows the defect gone) gets the SAME treatment:
RIGHT only if you saw the fix in the source.  SEVERITY in plain engineering terms: **HIGH** -- guest-controlled input
ends the emulator process, makes a memory access leave a buffer's bounds, or stops it making progress; **MED** --
guest-visible behaviour differs from the hardware documentation; **LOW** -- diagnostics, latent code, records, test
coverage.  Grade from the source, not from the queue's or the reviewer's grade.
Be hardest on: the HIGH grades (an id assigned HIGH gets a round); the "false record" claims (each is a closure); a
proposed id that already exists anywhere in `OUTSTANDING_BUGS.md` at `db8b1a33` (grep the whole file for it); and rows
whose quoted words are not actually in the cited lines.
Then: **(a)** entries in lines 15601-18200 that record something OPEN without an id and that the reviewer MISSED (scan
the range yourself; the reviewer's own count may be wrong in either direction); **(b)** rows that are the same entry
recorded twice, or two rows for one defect; **(c)** DENOMINATOR: rows checked in the source versus ruled on from the
reviewer's text alone.
VERDICT line (second line): `VERDICT: <r> right, <w> wrong, <u> unsettled of 9 claimed entries -- <m> missed by the reviewer, <h> HIGH confirmed`.
