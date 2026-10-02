FILING TABLE CHECK -- part 12 (last): the list of files this commit adds, and one clause written after part 11

Open with the token `ASTRAFILE_12_ALIVE` on its own line, then ONE verdict line:
`VERDICT: <w> files wrongly in the list; <m> files wrongly left out; <r> sentences wrong`
-- and, if all three numbers are 0, the single word `CLOSES` on the next line.

**Context.**  Your part 11 closed the chain on the table and the records text.  The first attempt to commit then
stopped before touching anything, for two reasons that concern what the commit ADDS rather than what it says:
the commit spec gave relative paths, and the committer refuses a zero-byte file, of which the artifact list held 37.
The spec is corrected, the 37 are left out, and one clause saying so was added to the CHANGELOG block.  Nobody but the
main loop has looked at the list of files, and it is 1,096 files long.  Everything below is under
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\` unless a full path is given.

Read-only: write nothing, build nothing, run nothing that changes a file.  Reading commands (`git ls-files`,
`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show 7440e129:<path>`, listing a directory, counting) are what this check
needs.  The repository is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`.

**A. The file list: `draft\spec554.files.txt`** (one path per line, relative to the repository).  The rule that made
it is in `draft\prep554.py.txt` (the walk over `DIRS`, about lines 95-125): every file under seven artifact
directories -- `astraretro_20260926`, `astraretro_harness_20260926`, `grokjobs_20260930`, `agypack_20261001`,
`codexpack_20260928`, `codexfarm_20260926`, `astrafiling_20261002`, all under `regress/artifacts/` -- EXCEPT a file
whose name ends `.err` (a seat's stderr stream), a zero-byte file, and a file git already tracks.  The list will be
recomputed by the same rule when the commit is staged, so files written after this export -- this brief, your answer,
and the list itself -- will join it.
1. Is any file in the list that the rule excludes, or that lies outside those seven directories?
   `<path> | why it should not be in the list`.
2. Is any file under those seven directories MISSING from the list that the rule includes (apart from the files written
   after the export)?  `<path> | why it should be in the list`.
3. This project keeps a never-commit list: `regress/ppc_rldicl_probe.py`,
   `tools/{BRIEF_TEMPLATE.md,CLAUDE.md,PIPELINE.md,panel.sh}`, `tools/pipeline/fable_queue.md`,
   `tools/pipeline/check_fix_seats.py`, `regress/artifacts/gdromdefault_461/`, any `regress/*.bin` at the top level, any
   `run_*/disk.img`, and no credential or API key in any file.  Is anything of that kind in the list?  Sample the text
   files for a key or token (the pattern of one is enough to flag; do not print it).
4. A launch log (`*.launch.log`) in the list records one seat job.  Is there one that shows a job still running -- no
   line saying the seat answered, walled, refused or returned a code?

**B. The six tracked files the commit changes** (first line of `draft\spec554.files.txt`): `CHANGELOG.md`,
`OUTSTANDING_BUGS.md`, `regress/pass2_ledger.tsv`, `tools/hooks/round_reminder.sh`, `tools/pipeline/ledger.json`,
`tools/pipeline/matrix.html`.  Does the CHANGELOG block's own list under "**The files.**"
(`draft\changelog554.draft.md:86-102`) name exactly these and say truly what each change is?

**C. The sentences added since part 11.**  One line per false one: `<file>:<line> | says <X> | should say <Y> | why`.
1. `draft\changelog554.draft.md:102-103`: "37 zero-byte files -- answer files of jobs that produced no output -- are
   left out as well: the committer refuses an empty file."  Count them yourself by the rule above.  Is every one an
   answer file of a job that produced no output, or is some other kind of empty file among them?
2. `draft\changelog554.draft.md:78-80`: the sentence that names this check (the string `DRY-ASTRA12` stands where your
   verdict will go).
3. `draft\changelog554.draft.md:106-107`: "five closing checks (`afile_08` to `afile_12`)".
4. The artifact-file count in the block and in `draft\msg554.draft.txt` is the list's length at staging time; say only
   whether it is DERIVED from the list (in `draft\prep554.py.txt`), not whether it equals a number of yours.

End with `DENOMINATOR: <a> of the list's lines checked against the rule; <b> of the seven directories walked;
<c> launch logs read`.
