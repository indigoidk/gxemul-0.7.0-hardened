# qhslowifetch pass 5 -- the widened-mask breach (codex B1 = glm breach 1), MEASURED 2026-11-05 before its adjudication
mask7_table.run.sh -> mask7_table/ (scratch clone /tmp/gxqhs9 under a clone-local .MUTANT sentinel, restored, cmp-clean, rebuilt).
M7 = arm (b)'s test widened to `(cpu->pc & ~(uint64_t)7) != addr`.  Guest `mtlr r3; blr` (blr_witness.py, far breakpoint):
                    -T r3=0x02040003      -T r3=0x02040007      no -T (both)
  fix5 (base)       1 report, parks       1 report, parks       UNIMPLEMENTED, 1 line
  M7                1 report, parks       8278 reports          UNIMPLEMENTED, 1 line
The 79-row probe on M7: PPC_IFETCH_RESULT=79/79, CONTROL=OK, RED=none (mask7_table/probe79_M7.out).  So the breach is REAL: the
shipped composite cannot see a mask widened past bit 1, because T blr's 0x02040003 has bit 2 clear (pc & ~7 == addr == 0x02040000).
At 0x02040007 the prologue gives addr = 0x02040004, the fix compares 0x02040004 == addr and parks, M7 compares 0x02040000 != addr,
takes arm (b) and re-runs the slot.  Remedy both seats name: re-seed T blr at r3 = 0x02040007 (bits 0-2 set): the fix parks; ~1 gives
0x..06, ~2 gives 0x..05, ~7 gives 0x..00, the revert gives 0x..07 -- all != addr, all flood.

*Corrected 2026-11-05 (main loop): this file's time-of-day stamp(s) (removed: ~06:4xZ) were GUESSES from the main loop's wrong clock -- later than this file's own creation time, so impossible as written.  The file's own timestamps are the record: created 06:31Z, last written 06:31Z before this note (UTC).*
