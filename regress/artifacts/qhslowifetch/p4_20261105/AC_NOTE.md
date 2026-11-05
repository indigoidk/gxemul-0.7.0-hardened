# qhslowifetch -- the repair-5 ruling's premise and repair, measured (2026-11-05 00:2x local; ac_table.run.sh -> ac_table/, ac_table_run.log)

The ruling (p4_20261105/ADJ_MYTHOS.md R2) rejected CB because, it derived, the same guest witness WITHOUT -T would spin silently in arm
(b), and it named as unsettled and load-bearing the premise that memory_rw returns failure on a non-existent fetch when -T is off.
MEASURED on the fix (base) and on AC (arm (b)'s test made `(cpu->pc & ~(uint64_t)3) != addr`), guest `mtlr r3; blr`, far breakpoint:
                      -T, r3=0x02040000   -T, r3=0x02040001        no -T, r3=0x02040000   no -T, r3=0x02040001
  fix (base)          1 report, parks     8278 reports, pc ...01   1 line, UNIMPLEMENTED   1 line, UNIMPLEMENTED, pc ...01
  AC                  1 report, parks     1 report, parks ...01    1 line, UNIMPLEMENTED   1 line, UNIMPLEMENTED, pc ...01
  (every run exit 0; LR reads the value stored; no checkstop text anywhere)
So the premise is FALSE on pmppc: without -T the read past RAM prints the non-existant line once, zero-fills and SUCCEEDS, the zero
word decodes as unimplemented, and the run stops -- no failure block, no spin, on the fix or on AC.  AC removes the -T flood exactly
as CB did, and the 69-row probe on AC is 69/69 (ac_table/probe69_AC.out).  Consequences for the ruled rows: the `T blr` session (-T)
stands; the ruled no -T session (terminates, chkstop present, pc) would exercise no arm of the fix -- the measured behaviour is
UNIMPLEMENTED, not a checkstop, on every build -- so it can red no variant of the fix: put back to the ruler with this measurement.
