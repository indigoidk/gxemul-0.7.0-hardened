TERMINATING-CALL CENSUS -- `src/cpus/`, group 5: 6 files, 13 live calls

Open your answer with the token `CODEXPACK_CENSUS_CPUS5_ALIVE`.  Second line: the VERDICT line specified at the end.

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

**The files, with the live count and EVERY line number (the census tool's comment stripper and pattern, applied to the files at the commit named above):**

- `src/cpus/cpu_mips_instr.c` -- 3 live: lines 123, 2650, 3798
- `src/cpus/cpu_sh.c` -- 2 live: lines 101, 1085
- `src/cpus/cpu_sh_instr.c` -- 2 live: lines 3834, 4004
- `src/cpus/generate_arm_r.c` -- 2 live: lines 320, 333
- `src/cpus/memory_arm.c` -- 2 live: lines 79, 254
- `src/cpus/memory_m88k.c` -- 2 live: lines 394, 413

For EVERY live call to `exit(`, `abort(` or `_exit(` in the files below at `db8b1a33` -- calls inside comments do not
count; the project's comment-stripping census tool counts 13 live calls in these files, per file as listed -- write
ONE line:
`<path>:<line> | <enclosing function> | WHEN: construction (machine or device setup, command line, file loading) / guest access (run time, under guest control) / debugger command / unreachable | CONDITION: <the test that leads to it, quoted> | GUEST LEVEL: user / privileged / n.a. | RECORDED: <id> / prose <OUTSTANDING_BUGS.md line range> / NONE | DISPOSITION: <member 1-7 below, or KEEP for a legitimate setup-time failure> | confidence`
The dispositions: (1) delete the terminating call; (2) decline silently; (3) decline and announce once (the house
`(once)` latch idiom); (4) accept -- the right value is already computed; (5) fault -- deliver the architecture's
exception; (6) accept into invented backing store; (7) implement the missing behaviour.
Rules: your count per file must match the tool's, or say which lines differ and why.  RECORDED means the queue
(`git show db8b1a33:OUTSTANDING_BUGS.md`) names this site or this defect -- search by the function name, the message
text and the file name; quote what you found.  Then: **(a)** the GUEST-ACCESS sites ranked by how ordinary the
triggering access is (an access a stock operating system makes first; a malformed or reserved one last), with one
line of reasoning each; **(b)** sites in the same files that stop the CPU (`cpu->running = 0`) rather than end the
process, listed the same way -- they are the same class one grade down; **(c)** the DENOMINATOR: functions read,
functions not read.
VERDICT line (the second line of your answer): `VERDICT: <n> live calls classified -- <g> reachable by guest access
at run time, <u> of those not recorded`.
