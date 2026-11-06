# ARTSET_RULE.md -- which files of a round's artifact folder a landing commits, and the .gitignore that carries the choice

Written for the qhslowifetch landing (2026-11-05) to be reused by the memc and pvr kits.  The rule is the coordinator's; the tools
that apply it are templates in the qhs kit: `artset_qhs.py` (the selection), `artgi_qhs.py` (the .gitignore and its proof),
`mk_manifest_qhs.py` (MANIFEST entries for the committed scripts only).

**Why.**  Whole round folders are large (qhs 446 MB, pvr 622 MB, memc 136 MB, against 540 MB for every artifact tracked so far)
and blobs never leave history.  Adding a file later is cheap; removing one is impossible.  Excluded files stay on disk.

## The selection

COMMIT, and nothing else from the folder:
1. **Every file a committed record or docstring cites by path**, closed transitively: a committed record's citations are committed,
   and if they are records their citations too, until nothing new appears.  Citing sources: the unit's own records (round block,
   commit message, the round's ledger rows, its bug-file section, the probe docstring, the gate block, the MANIFEST *descriptions*
   -- never its keys, which are generated from the selection), the kit's banked files, and every committed record in the folder.
   Resolve a token against the citing file's directory, then the folder, then (if it has a directory part) a unique path suffix.
   A glob (`table12/probe_*.out`) cites what it matches in its directory.  A cited directory of at most 256 KB goes in whole; a
   larger one only has to keep a committed file.  Probe logs and session transcripts are not records: their text cites nothing.
2. **The round's records**: every `*.md` (DISPOSITION.md included), the seat answers (`codex_*.txt`, `gemini_*.md`, `ADJ_*.md`,
   `REG_*.md`, `ollama_*.txt`), `VERDICT*` `SCORES*` `TALLY*` `MD5*` `PRETABLE*` `COMPARE*` `PAIRS*`, the `*_frozen.py`
   instruments, the `.pre_*` backups, the proofs (`*proof*`) and the diffs (`*.diff`).
3. **Each table's base, HEAD and null-leg probe logs** (`probe*_base*`, `probe*_HEAD*`, `probe*_null_*`, `probe*_dead{true,false,
   absent}*`, `.out`/`.raw`; a witness's own null legs).

EXCLUDE everything else -- per-variant build logs, session-transcript directories, per-variant probe logs not cited, binaries and
objects (a NUL byte or an ELF header, even when cited), clone residue.

Record the result as three committed files beside the kit's records: the path list, each path with its rule and first citing
file, and the excluded files grouped by size.  Every count in the round block names one of them.

## The .gitignore: a DENY list, never an allow list

An allow list (`*`, `!*/`, `!/path`...) hides every file added to the folder later -- an erratum, a new reading -- from
`git status`, which is the uncommitted-record trap.  So the folder's `.gitignore` denies the **bulk classes** by pattern, denies the
**uncited one-off files present at the landing** by anchored lines (`/dir/name`, so the same name elsewhere stays visible), and
re-includes with `!/path` each file the selection takes that a deny line would hide.  Any file matching no line stays visible.

* Never a bare directory pattern (`sessions_*/`): git cannot re-include a file under an excluded directory.  Write `sessions*/**`,
  which ignores the contents and leaves the directory re-includable.
* All `!` lines come after all deny lines (the last matching line wins).
* When every probe log of one directory is selected, one `!/dir/probe*.out` line may stand for them.
* The qhs classes: `**/sessions*/**`, `**/*_sessions*/**`, `**/build_*.log`, `**/apply_*.err`, `**/table*/probe*.{out,raw}`,
  `**/*_table/probe*.{out,raw}`, `**/cell_*.txt` `**/blr_*.txt` `**/traodd_*.txt` `**/explore_*.txt`, `**/codex_*.err`,
  `**/cxlaunch.log`, `**/*.launch.log`, `**/*.launch[0-9]*.log`, `**/*_run.log`, `**/*_run_[a-z].log`.  Check them against your
  own folder's names; what no class covers becomes an anchored one-off line.

**Prove it, do not assume it**: in a scratch repo, mirror the folder's untracked files as empty files (plus the repo's root
`.gitignore` and the files the spec writes there), drop the candidate `.gitignore` in, and run `git add -n -- <folder>`.  It must
take EXACTLY the selection plus the spec's files, no more and no fewer.  `git check-ignore -v -n --stdin` gives each line's reach.

## The commit

The spec carries the `.gitignore` as a `files` entry and keeps `add_dirs: [<folder>]`, so one argument adds the folder and git
applies the deny list.  A long explicit path list will not do: about 1,000 paths gave WinError 206 in commit_unit2's `git add`.
If paths must be listed, use `git add --pathspec-from-file`.  Section R reads `git ls-files`, so the MANIFEST must list exactly the
committed `.py` files: an entry for an uncommitted script is a GHOST, a committed script without one is UNCLASSIFIED.
