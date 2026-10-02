PANEL SEAT -- the codex seat's answer to a full-panel brief (a device finding and two severity disputes)

Open your answer with the token `CODEXPACK_HPANEL_DEV_ALIVE`, then answer the brief at
`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\panel_high\brief_high_dev.md`
exactly as its own sections direct (its VERDICT line first, then Q1-Q4 and the standing license).  You are one seat
of a nine-seat panel; the others answer the same brief separately and nobody sees your answer before writing theirs.

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
