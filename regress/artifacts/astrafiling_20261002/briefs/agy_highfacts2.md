FACT CHECK 2 -- ten clauses that describe YOUR fact table, and two rows it did not cover

FIRST line of your answer: `VERDICT: <f> of 10 clauses misstate your table; <n> of 3 new sites answered`.
SECOND line: the token `AGY_HIGHFACTS2_ALIVE_1002`.  THIRD line: quote verbatim the first line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`.

READ-ONLY, always: write no file, run nothing that changes a file, build nothing.  The tree under review is
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` (git) at commit `7440e129`; read committed files
(`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show 7440e129:<path>`), and ignore any other `src/` under the project
root.

**Context.**  Earlier today you answered three factual questions for 22 rows of a filing table about this project's
regression harness: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\agy\agy_highfacts.txt`.
Two other seats dispute the grade of ten of those rows, and the filing now says, row by row, what YOUR table shows for
each: `...\astrafiling_20261002\FILING_OVERLAY.tsv`, lines 99 to 108 -- in each line, the clause that begins
`agy's fact table`.  Those clauses were written by another seat reading your lines.  Your agreement is not what is
wanted.  What is wanted is a FLAG wherever a clause says more than your line says, less, or something else.

**Part 1 -- the ten clauses.**  One line per row:
`<id> | CLAUSE MATCHES  or  CLAUSE MISSTATES: <what your line says instead, in one sentence> | agy_highfacts.txt:<your line>`
Compare each clause with your OWN line for that row (two rows were renamed since: your `probewiringvarmap` is now
`wirereassign`, your `wdcnullstatus` is now `wdcchildstatus`).  A clause that is true but leaves out the half of your
line that points the other way is a MISSTATES.

**Part 2 -- the same three questions for three sites your table did not cover.**
* Q1: if the emulator process ENDS (a nonzero exit or a signal) during the run that the row scores, does the row FAIL,
  or CAN it PASS?  Give the `path:line` of the scoring code.
* Q2: on the path the row exercises, does the committed source STILL END THE PROCESS anywhere today, or NO LONGER?
  Give `path:line`.
* Q3: is there a LIVE INSTANCE today -- something a guest can do on an in-tree machine after which the row passes
  although the process ended?  `LIVE INSTANCE: <what>` or `NONE FOUND`, and say how far you looked.
The sites:
  a. `gdromcondhow` -- rows R1b and R2b of `regress/gdrom_cond_probe.py` (their pass conditions are near `:419` and
     `:499`; the helper that collects the child's status is near `:224-233`).
  b. `ptywaitstatus`, site 1 -- rows `pscale noig2` and `ipl noig2` of `regress/pcc2_width_probe.py` (near `:773-778`;
     the liveness verdict and the stored wait status are near `:505-579`).
  c. `ptywaitstatus`, site 2 -- `regress/ppc_rounding_probe.py` (the session helper near `:169-185`, the row verdicts
     near `:1176-1184`).
One line per site: `<site> | Q1: FAILS or CAN PASS -- <path:line> | Q2: STILL ENDS THE PROCESS or NO LONGER -- <path:line> | Q3: ...`

End with `DENOMINATOR: <a> of 10 clauses compared with my own lines; <b> of 3 sites read in the source`.
