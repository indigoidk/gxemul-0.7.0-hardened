# sgireunmapped -- MEASURED MUTANT TABLE (opus5 seat)

Scratch clone /tmp/gxopus_sgire (cp -a of build/).  Baseline NAMED and checked:
`base' variant is BYTE-IDENTICAL to HEAD's dev_sgi_re.c; the run's own restore
step re-verified `cmp vs SEC: CLEAN'.  Every build checked `[ binary -nt source ]';
all nine variant binaries have DISTINCT md5s.

TWO INDEPENDENT RUNS.  Table 1 = table1_scores.txt, Table 2 = table2_repaired.txt
(after repairing one vacuous row).  They agree on 8 of 9 variants byte-for-byte;
the ninth changed exactly as predicted and for the predicted reason.

  variant      T1      T2     killed by
  base       10/14   10/14    survive w, survive r, read0 REAL, read defatal
  fix        14/14   14/14    --
  mret0      12/14   12/14    read0 REAL, no DBE
  mlatch     13/14   13/14    latch fresh
  mwonly     11/14   11/14    survive r, read0 REAL, read defatal
  mshrink    13/14   13/14    accept lina
  mshrinkb   13/14   13/14    accept linb
  mtexshrink 13/14   13/14    accept tex
  mnolatch   14/14*  13/14    msg once (got=2 want=1)
     * ESCAPED in T1 because `msg once' was vacuous -- see INSTRUMENT_FINDING.md

`base' is RED: test-first is satisfied.  `fix' is the only clean sweep.

## ROW COVERAGE, stated rather than glossed: 10 of 14 rows ever fired
Undischarged (never failed on ANY variant):
  accept tlba, accept tlbb, accept tlbc   -- no shrink mutant was built for the
      three TLB windows, so by the failability rule these three accept rows are
      NOT discharged: an accept row is discharged by a MEASURED KILL, not by
      existing.  Three more mutants are owed; each build is ~1.5 s.
      NOTE TLB_A/TLB_B bound by THE NEXT CONSTANT, so shrinking them perturbs
      two arms at once -- a different mutant shape from TLB_C/TEX/LIN_A/LIN_B,
      which bound by base+size.
  read0 VACUOUS -- deliberately never fires.  It is the CONTROL that
      demonstrates the brief's stated pin is vacuous: same load, v0 pre-set 0
      instead of 0xa5a5a5a5, and it PASSES on mret0 where the real row fails.
