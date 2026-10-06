PASSAGES #555 POINTS AT AN ID, part 3 -- does the id cover the passage?

FIRST line of your answer: `VERDICT: <f> of 34 passages flagged, <n> not checked`.  SECOND line: the token `AGY_IFILED2_3_ALIVE_1002`.
THIRD line: quote verbatim the first line of `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`.

READ-ONLY, always: write no file, run nothing that changes a file, build nothing, and stay in the foreground.  The
tree under review is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` (git) at commit `c29a5fd3`; read committed files
(`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show c29a5fd3:<path>`), and ignore any other `src/` under the project root -- the working
tree also carries another session's uncommitted edits.  Queue line numbers below are commit `db8b1a33`'s: read that
text with `git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show db8b1a33:OUTSTANDING_BUGS.md`.

**Context.**  This project's bug queue, `OUTSTANDING_BUGS.md`, names most rows by a short backticked id; some entries
recorded open work in prose only.  Commit `c29a5fd3` (`#555`) gave those entries ids: its section is at the end of the
queue file at that commit, and its tables are in `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\idless_20261002` (`IDLESS_TABLE2.tsv`, `IDLESS_CARRIED.tsv`).  Each row was
ruled by one seat and confirmed by another.  YOUR AGREEMENT IS NOT WHAT IS WANTED.  What is wanted is a FLAG: a line
that the committed source or the queue text does not support.  A line you cannot check is `NOT CHECKED: <why>`, never
a pass.

Each line below is a prose passage of the queue that gets no row of its own because an id is said to carry it.  That
is only right if the named row really covers what the passage says is open.  A note in brackets says what kind of id
it is: a row `#555` filed (its title is in that commit's section of the queue file), a ledger row and its state
(`tools/pipeline/ledger.json` at `c29a5fd3`), or an id that only the queue file names.

**For each passage, ONE line:**
`<n> | <id> | EXISTS: <where you found the row> / NOT FOUND | COVERS: YES / PARTLY: <what the passage says is open that the row leaves out> / NO: <why> | <the lines you read>`
* `PARTLY` matters most: a passage with two open items pointed at a row that names one of them loses the other.
* Where the only carrier is closed or dropped, say whether the passage still records work that is NOT done at
  `c29a5fd3`: `STILL OPEN: <what, path:line>` or `NOTHING OPEN`.

Then `DENOMINATOR: <s> of 34 passages read in the queue and in the row each is pointed at`.

**The passages** (n | queue lines at db8b1a33 | the id or ids, as `#555` lists them):
1. 5701-5709 | `optrow` (ledger: held)
2. 5868-5881 | `fbsdrampair`
3. 5894-5898 | `fbmode` (ledger: held)
4. 5899-5902 | `fbmode` (ledger: held)
5. 5903-5907 | `fbmode` (ledger: held)
6. 5908-5911 | `fbmode` (ledger: held)
7. 5913-5920 | `i8253zero` (ledger: held)
8. 6082-6086 | `m8latch` (ledger: closed; the row the passage names; it does not carry the open work), `closeassessrows` (a `#555` row above; the open work)
9. 6095-6096 | `m8snprintf` (ledger: dropped), `m8latch` (ledger: closed)
10. 6097-6099 | `gcsections` (ledger: closed; the row the passage names; it does not carry the open work), `closeassessrows` (a `#555` row above; the open work)
11. 6101-6140 | `ns16550` (ledger: closed; the row the passage names; it does not carry the open work), `closeassessrows` (a `#555` row above; the open work)
12. 6804-6805 | `pit8253bcdbinary`
13. 6806-6809 | `pitcount` (ledger: held)
14. 6823-6826 | `changelogroundgap`
15. 7326-7338 | `qhguestasan` (a `#555` row above)
16. 8144 | `sh4prio0` (ledger: closed)
17. 8678-8690 | `sh4iprunpinned`
18. 8691-8694 | `shdmteupper` (named in this file only: no ledger row of its own)
19. 9063-9067 | `gdrompiooddlen`
20. 9148-9152 | `hlen` (ledger: held)
21. 10258-10261 | `asicpermute`
22. 10412-10418 | `gdrompionull` (ledger: closed; the row the passage names; it does not carry the open work), `gdromtailcov` (a `#555` row above; the open work)
23. 13612-13617 | `outcomegap`
24. 14302-14306 | `gxprobepccache`
25. 16630-16633 | `printedvariants`
26. 16756-16763 | `armuserpageshift` (named in this file only: no ledger row of its own)
27. 16972-16975 | `armcpsrprint` (a `#555` row above)
28. 16997-17000 | `xscalecp6exits`, `armendianexit`
29. 17093-17096 | `m88ktrapmask` (named in this file only: no ledger row of its own)
30. 17097-17102 | `mipsextshift`
31. 17979-17980 | `guardfailsopen`
32. 19984-19987 | `pit8253bcdbinary`
33. 20735-20738 | `adjudglmtag`
34. 20873-20878 | `heartirqdelivery` (a `#555` row above)
