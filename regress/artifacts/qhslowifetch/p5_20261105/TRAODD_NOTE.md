# qhslowifetch pass 5 -- Mythos breach 2 (MYTHOS.md, MYTHOS_r2.md), MEASURED 2026-11-05 before its repair
traodd_table.run.sh -> traodd_table/ (scratch clone /tmp/gxqhs10, clone-local .MUTANT, restored cmp-clean against GXEMUL-SEC, rebuilt,
cleared).  `T ra` (a -T continue from cpc700_pci's last word; no breakpoint, so read-ahead runs) entered at 0xfec00004 and at the
UNALIGNED 0xfec00005 (traodd_witness.py):
                          pc 0xfec00004                    pc 0xfec00005
  fix (repair 5)          pc 0xfec00008, 2 reports         pc 0xfec00009, 2 reports
  A1 `&& cpu->pc == addr` pc 0xfec00008, 2 reports         pc 0xfec00009, 1 report
  A2 `&& !(cpu->pc & 3)`  pc 0xfec00008, 2 reports         pc 0xfec00009, 1 report
  (every run exit 0; every halt names 0xfec00008; SRR0 and MSR unchanged; no checkstop or UNIMPLEMENTED text)
The 79-row probe on A1 and on A2: 79/79, CONTROL=OK, RED=none (traodd_table/probe79_A1.out, probe79_A2.out).  So the breach is REAL:
from an unaligned pc the read-ahead fetch reaches the failure block with pc != addr, the conjoined guard sends it on to arm (c), which
parks it at read-ahead time, and the real fetch's second report never comes.  Row: a `T ra odd` session (0xfec00005) pinning exit 0,
pc 0xfec00009 and two reports.

*Corrected 2026-11-05 (main loop): this file's time-of-day stamp(s) (removed: ~08:3xZ) were GUESSES from the main loop's wrong clock -- later than this file's own creation time, so impossible as written.  The file's own timestamps are the record: created 07:47Z, last written 07:47Z before this note (UTC).*
