RETRO-REVIEW, DRAFT DISPOSITIONS -- batch 3b (25 findings in 4 answers)

Open your answer with the token `CODEXPACK_DRAFT_3B_ALIVE`.  Second line: the VERDICT line specified at the end.

**The tree.**  `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` (git): a hardened fork of the GXemul 0.7.0 full-system machine emulator, in C99.  Read
COMMITTED files only, at commit `8ea26abb`: `git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show 8ea26abb:<path>` (number the lines with
`awk '{print NR": "$0}'` or use `grep -n`).  The WORKING TREE carries other people's uncommitted work -- do not read
source files from disk.  Ignore every other `src/` under the project root (`src/`, `est/`, `build/`, `build-asan/`,
`_archive/` are other copies; a copy reports line numbers off by hundreds).

**Reading scope.**  `src/`, `regress/*.py`, `regress/*.sh`, `regress/*.c`, `OUTSTANDING_BUGS.md` and `CHANGELOG.md`
(all at `8ea26abb`), the hardware manuals `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\*.txt` (on disk), and the files this
brief names by path.  Do not read anything else under `regress/artifacts/`, and not `tools/pipeline/ledger.json`.

**This is a reading task.**  Build nothing, run nothing, write nothing.  Do not write programs or patches: describe
behaviour and cite lines.  Cite `path:line` at `8ea26abb` for every claim and quote the line when the claim rests on its
exact text.  Say "not checked" rather than guessing.  Where a claim is ARITHMETIC (an offset, an index range, a count)
enumerate the values rather than reasoning about them.

**Context.**  A reviewing model read this fork's accumulated changes to several source files at commit `8ea26abb` --
the fork's NET change since the upstream import `39748e3c` -- and reported findings, each one block:
`F<n> | path:line | round | CODE / RECORD / TEST-GAP | live | consequence | smallest check | confidence`.  HEAD has
since moved to `db8b1a33` by one records-only commit (#553: CHANGELOG.md, OUTSTANDING_BUGS.md, the ledger,
regress/diff_wdc_identify.c, tools/pipeline/check_probe_wiring.py; no file under src/), so read SOURCE at `8ea26abb`
and the two record files at `db8b1a33` where this brief says so.

**The answers to draft dispositions for:**
- `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\cpumips\codex_cpumips.txt`  (its brief: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\briefs\cpumips.md`)
- `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\cpumipsinstr\codex_cpumipsinstr.txt`  (its brief: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\briefs\cpumipsinstr.md`)
- `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\devsgiip30\codex_devsgiip30.txt`  (its brief: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\briefs\devsgiip30.md`)
- `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\devsgire\codex_devsgire.txt`  (its brief: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\briefs\devsgire.md`)

**You are preparing a DRAFT for the adjudicator, not a ruling.**  The same reviewing model (or a sibling of it) wrote
the findings, so agreement is not independent evidence; the value of this pass is the MECHANICAL work the adjudicator
otherwise spends its budget on -- the lookups, the duplicate checks and the replacement texts -- and any finding the
first reading got wrong.  For EACH finding `F<n>` of each answer:
 (i)   RE-CHECK it against the source at `8ea26abb` (the commit the answers cite; their line numbers are that commit's).
       Quote the line(s) the finding rests on.  If the finding is wrong or overstated, say exactly how.
 (ii)  ALREADY RECORDED?  Search `OUTSTANDING_BUGS.md` at HEAD (`git show db8b1a33:OUTSTANDING_BUGS.md`) for an existing
       entry -- by a backticked id AND by prose describing the same defect without an id.  Quote the line range.
       (Six of one earlier batch's thirty dispositions were overturned for ruling NEW what prose already recorded.)
 (iii) DUPLICATE?  Check `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\DISPOSITIONS.md` (the rows earlier batches already
       proposed, with ids) and the OTHER answers in this batch for the same defect.
 (iv)  For a RECORD finding: draft the EXACT replacement text for the false comment or sentence.
 (v)   SEVERITY by the rule: HIGH -- input under the guest's control makes the emulator process end, makes a memory
       access leave a buffer's bounds, or stops it making progress; MED -- guest-visible behaviour differs from the
       hardware documentation; LOW -- diagnostics, latent code, test coverage.  Grade by what the source shows.
One line per finding, in this form, then ONE line `Checked:` naming the lines you read:
`<job>:F<n> | DRAFT NEW <HIGH/MED/LOW> <proposed-id> "<title>" | DRAFT FILED <id> | DRAFT FILED-BY-PROSE <OUTSTANDING_BUGS.md line range> <proposed-id> | DRAFT RECORD "<exact replacement text>" | DRAFT TEST-GAP <proposed-id> | DOUBTFUL "<why>" | DUPLICATE <job>:F<n> | DUPLICATE-OF-ROW <id>`
A proposed id is short, lowercase, no spaces, must not already exist in OUTSTANDING_BUGS.md or in DISPOSITIONS.md,
and must not contain the word "kill".  Then: **(a)** the findings you think are wrong or overstated, with the line
that shows it; **(b)** cross-answer duplicates; **(c)** the DENOMINATOR -- findings checked against the source versus
ruled on from the text alone.
VERDICT line (the second line of your answer): `VERDICT: DRAFT -- <c> new, <f> filed (<p> of them by prose without
an id), <r> record, <t> test-gap, <x> doubtful, <d> duplicate, of <n> findings`.
