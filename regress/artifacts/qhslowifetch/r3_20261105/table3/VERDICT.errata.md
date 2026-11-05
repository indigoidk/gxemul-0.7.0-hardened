# table3/VERDICT.md -- errata (VERDICT.md itself stays unedited)

1. 2026-11-05 (repair 7b; the late-replication cross-check, ../../LATE_REPLICATIONS_20261105.md row 11, OPEN item 1).
   VERDICT.md line 13 says D12_else_ra's predicted set `T_ra_pc,T_ra_nonex,T_ra_addr,T_ra_me_pc,T_ra_me_nonex` was "carried from
   table 2's measured T ra reds".  That holds for the first three rows only.  Table 2's instrument
   (../../det_20261104/table2/probe56_frozen.py) has ONE read-ahead session, `T ra` (rows: session, pc, nonex, addr, stopped), and
   no `T ra me` session; table 2 measured D12_else_ra at 53/56 with RED=T_ra_pc,T_ra_nonex,T_ra_addr
   (../../det_20261104/table2/SCORES.txt).  So `T_ra_me_pc` and `T_ra_me_nonex` were not carried from any measurement: PRETABLE_3
   extended table 2's `T ra` reds to the new ME-set session by analogy.  ../PRETABLE_3.errata.md item 1 does not say so either.
   Nothing measured changes: D12 is red in every table, and the probe records it as build-dependent.
