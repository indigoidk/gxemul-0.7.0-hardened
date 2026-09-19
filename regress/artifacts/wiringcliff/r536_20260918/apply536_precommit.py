"""#536: precommit_check.sh section R's comment said the exemptions expire "2026-09-20, chosen to fall due with
gate_offline's fbpending_bound" -- false once #537 discharges that debt and #536 moves the block (Opus seat,
#536 pass 2).  The date now lives only in check_probe_wiring.py.  Refuses unless its anchor occurs exactly once."""
import io, sys
p = sys.argv[1]
s = io.open(p, encoding="utf-8", newline="").read()
OLD = ("#  Existing gaps are carried as DATED exemptions that EXPIRE (2026-09-20, chosen to fall due\n"
       "#  with gate_offline's fbpending_bound), never as silent grandfathering.\n")
NEW = ("#  Existing gaps are carried as DATED exemptions that EXPIRE, never as silent grandfathering; the\n"
       "#  dates live in check_probe_wiring.py's EXEMPT table, not here.  (They were 2026-09-20, chosen to\n"
       "#  fall due with gate_offline's fbpending_bound; #537 discharged that debt and #536 moved the\n"
       "#  block to 2026-09-27 by owner ruling.)\n")
k = s.count(OLD)
assert k == 1, "anchor x%d" % k
s = s.replace(OLD, NEW)
#  The same block's sibling, stale since the selftest grew (grok, #536 F2 pass): the pin below it is 22.
OLD2 = "--selftest applies 18 mutants to\n"
NEW2 = "--selftest applies its mutants (22, pinned below) to\n"
k = s.count(OLD2)
assert k == 1, "18-mutants anchor x%d" % k
s = s.replace(OLD2, NEW2)
#  And the domain count two lines up, stale since #471 made the scan recursive (Opus seat, #536 F2 pass).
OLD3 = ("#  HARD, and retroactive rather than forward-only-by-date: the domain is 36 files in one\n"
        "#  flat directory, and a date cutoff would grandfather exactly the four files it exists for.\n")
NEW3 = ("#  HARD, and retroactive rather than forward-only-by-date: the domain was 36 files in one\n"
        "#  flat directory when this was written (#471 has since made the scan recursive), and a date\n"
        "#  cutoff would have grandfathered exactly the four files it existed for.\n")
k = s.count(OLD3)
assert k == 1, "36-files anchor x%d" % k
s = s.replace(OLD3, NEW3)
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("precommit_check.sh section-R comment corrected")
