PASSAGES #555 POINTS AT AN ID, part 2 -- does the id cover the passage?

FIRST line of your answer: `VERDICT: <f> of 35 passages flagged, <n> not checked`.  SECOND line: the token `AGY_IFILED2_2_ALIVE_1002`.
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
1. 3042-3063 | `sh4sqexpevt` (named in this file only: no ledger row of its own; in part: the PREF exception kind)
2. 3200-3202 | `armbdtcombined`
3. 3227-3233 | `armcachecleanload`
4. 3326-3331 | `armcachecleanload`
5. 3401-3408 | `armbdtcombined`
6. 3409-3413 | `armmemcpyoverlap`
7. 3500-3508 | `qharmmemsetdead` (a `#555` row above), `qhmemsetalias` (a `#555` row above)
8. 3617-3618 | `qharmvsixunal` (a `#555` row above)
9. 3740 | `qhusertlbmeas` (a `#555` row above)
10. 3903-3905 | `qharmmemsetdead` (a `#555` row above)
11. 4139-4145 | `armalignexc`, `armsa1110areset` (a `#555` row above)
12. 4251-4287 | `lunabackhard` (named in this file only: no ledger row of its own)
13. 4676-4682 | `m88kidleslotsem`
14. 4745-4746 | `qhcpycoldremeas` (a `#555` row above)
15. 4802-4803 | `OB-24` (named in this file only: no ledger row of its own)
16. 4966-4967 | `qharmstaleprompt` (a `#555` row above), `qhctrlcwait` (a `#555` row above)
17. 5046-5047 | `armoddpair`
18. 5085-5097 | `armoddpair`
19. 5142 | `armdwordalign` (in whole)
20. 5142-5143 | `armoddpair`
21. 5215-5223 | `b126` (ledger: held)
22. 5225-5232 | `b126` (ledger: held)
23. 5262-5266 | `loadfragile` (ledger: in work; in part: the 5262-5266 transport sweep only), `qhshelltimeout` (a `#555` row above)
24. 5310-5319 | `loadfragile` (ledger: in work)
25. 5405-5409 | `strad` (ledger: held)
26. 5492-5495 | `batterymissedruns`
27. 5500-5503 | `census` (ledger: closed)
28. 5504-5506 | `auditmap` (ledger: held)
29. 5563-5573 | `capgap` (ledger: dropped)
30. 5575-5580 | `capN` (ledger: dropped)
31. 5582-5585 | `cflood` (ledger: dropped)
32. 5587-5605 | `sigunsafe` (ledger: dropped)
33. 5678-5682 | `mrwstore2` (ledger: held)
34. 5686-5691 | `mrwgrind` (ledger: dropped)
35. 5692-5697 | `mrwstore2` (ledger: held)
