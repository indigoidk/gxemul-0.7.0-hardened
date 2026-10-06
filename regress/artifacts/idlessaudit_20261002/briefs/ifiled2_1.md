PASSAGES #555 POINTS AT AN ID, part 1 -- does the id cover the passage?

FIRST line of your answer: `VERDICT: <f> of 35 passages flagged, <n> not checked`.  SECOND line: the token `AGY_IFILED2_1_ALIVE_1002`.
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

Then `DENOMINATOR: <s> of 35 passages read in the queue and in the row each is pointed at`.

**The passages** (n | queue lines at db8b1a33 | the id or ids, as `#555` lists them):
1. 1526-1528 | `m88kidleslotsem`, `qhidlefoldloss` (a `#555` row above)
2. 1616-1622 | `ppcfmarn`
3. 1646-1649 | `alphatinyzero`
4. 1650-1655 | `mipstinyprerm`
5. 1672-1675 | `ppcsinglealias`
6. 1685-1697 | `ppcfprfclass`, `ppcveinhibit`, `ppcenabldeliv` (a `#555` row above)
7. 1705-1716 | `qhppcdecode` (a `#555` row above)
8. 1774-1777 | `qhmipsps` (a `#555` row above)
9. 1778-1779 | `shoddprfield`
10. 1931-1936 | `sh4sqexpevt` (named in this file only: no ledger row of its own), `sh4sqwrite`, `qhshsqat` (a `#555` row above)
11. 1940-1958 | `sh4utlbmultihit`, `sh4sqexpevt` (named in this file only: no ledger row of its own), `sh4sqwrite`, `qhshsqat` (a `#555` row above)
12. 1965-1970 | `qhfcsrflags` (a `#555` row above)
13. 1971-1973 | `optinyband`
14. 1977-1979 | `armcachegeom`, `armv6cachefmt` (a `#555` row above)
15. 1980-1982 | `qhx11fifo` (a `#555` row above; in part: the console-overrun clause)
16. 1983-1986 | `qhlancestp` (a `#555` row above), `qhdiagrest` (a `#555` row above), `qhvgasizestate` (a `#555` row above)
17. 1987-1988 | `OB-22` (named in this file only: no ledger row of its own)
18. 2038-2049 | `qhfcsrflags` (a `#555` row above)
19. 2086-2088 | `qhscifssr` (a `#555` row above)
20. 2097-2109 | `armcachegeom`, `armv6cachefmt` (a `#555` row above)
21. 2291-2297 | `qhfcsrflags` (a `#555` row above)
22. 2307-2318 | `qhx11fifo` (a `#555` row above)
23. 2453-2455 | `arcpartlba` (named in this file only: no ledger row of its own)
24. 2456-2459 | `OB-22` (named in this file only: no ledger row of its own)
25. 2597-2599 | `qhfcsrflags` (a `#555` row above), `qhmipstlbwarn` (a `#555` row above)
26. 2614-2615 | `armthumbabortkill` (in part: the Thumb half only)
27. 2616 | `m88kexit` (ledger: held)
28. 2636-2638 | `mipsreadpriv`
29. 2685-2689 | `exitunowned76`
30. 2721-2723 | `pvrrenderexit`
31. 2727-2728 | `ramspaninval`
32. 2730 | `jazzlbmask`, `OB-22` (named in this file only: no ledger row of its own)
33. 2730-2731 | `arcpartlba` (named in this file only: no ledger row of its own)
34. 2731 | `tcpdebugopts`
35. 3004-3005 | `armcachecleanload`
