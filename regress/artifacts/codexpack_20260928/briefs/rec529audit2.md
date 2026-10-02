RECORDS AUDIT -- change #529 (crimewidthkill), the drafts as they stand on 2026-09-28

Open your answer with the token `CODEXPACK_REC529AUDIT2_ALIVE`.  FIRST LINE AFTER IT:
`VERDICT: <N> false or unsupported sentences`.

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

You are an independent auditor.  These DRAFT records will be committed with change #529.  They were audited once on
2026-09-26 (`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\final529r17_20260926\codex_jobs\codex_rec529audit.txt`, eleven false or
unsupported sentences, all corrected since) and have CHANGED since that audit:
* the filed row `crimectllane` is now graded HIGH instead of MED, in three places, with a paragraph giving the reason
  (the confirmation pass on the codex farm's f1c adjudication overturned the adjudicator's MED);
* the base leg on the final probe text ran: 226 of 226 rows, controls OK
  (`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\final529r18_20260926\probe_base_r18.raw`, `MD5.txt`, `DIFF_vs_table16_base.txt`);
* HEAD moved from 8ea26abb to db8b1a33 by change #553 (records only).

The drafts are inlined, with the ledger changes as code, in
`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\final529r18_20260926\records_drafts.md`.  Its dated second header line says what changed.
Angle-bracket placeholders (`<OWED-...>`) are owed, not claims.

Audit EVERY factual sentence of the drafts against the evidence under `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\` (the tables'
`PRETABLE*`/`POSTTABLE*`/`check*.out`, the panels, the rulings, the base-leg files above) and against the tree at
`db8b1a33` -- but be HARDEST on the sentences that changed since the last audit, and on these three questions:
1. Is the HIGH grade for `crimectllane` supported by the source?  `src/devices/dev_sgi_ip32.c` (the CRIME_CONTROL
   arm and the 4-byte width arm), `src/core/emul.c` (what happens when no machine is still running), `src/core/main.c`.
   The MED argument was: the guest gains no capability it lacks through the legitimate 64-bit hard-reset write.
2. Does the base-leg description match the files?  Re-derive the diff count against table 16's base log
   (`table16_20260926/logs/probe_base.raw`) yourself: which rows differ, and why.
3. Are the commit message, the CHANGELOG block, the OUTSTANDING_BUGS section and the ledger entries CONSISTENT with
   each other (the same counts, the same grades, the same commit list)?

Then each false or unsupported sentence: the sentence, the file and line, the evidence that contradicts it, and the
corrected sentence.  Re-derive every count (row counts, leg counts, table scores, entry counts) rather than trusting
it; say which you re-derived.  Also: anything the records should say and do not (an owed obligation, a dissent, a
seat failure) -- name it.  End with the DENOMINATOR: what you read, and what you did not.
