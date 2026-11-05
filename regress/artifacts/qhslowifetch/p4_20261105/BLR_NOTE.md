# qhslowifetch pass 4 -- arm (b) is GUEST-reachable, and on the -T route it floods (measured 2026-11-04 23:5x local)

Trigger: GPT-6 Astra's pass-4 records finding R1 (codex_qhs_p4.txt): this fork's X(mtlr) copies the register into LR unmasked and
X(bclr_20) sets cpu->pc = LR unmasked (cpu_ppc_instr.c), so guest code can make pc unaligned; the translator's prologue keeps pc's
low two bits while it aligns addr, so pc != addr and arm (b) is taken.
MEASURED (blr_witness.py, base build = the fix, -E pmppc unmodified, -T, read-ahead disabled by a far breakpoint; guest code at
0x2000: `mtlr r3` (0x7C6803A6), `blr` (0x4E800020); blr_witness_base.out and blr_base_*.txt):
  r3 = 0x02040000 (aligned, past RAM): ONE halt report, pc parked at 0x02040000 -- arm (c), as designed.
  r3 = 0x02040001 / 0x02040003:        8278 halt reports (`memory READ: from non-existant paddr=0x02040000`), pc 0x02040001 /
                                       0x02040003, exit 0.  Arm (b) refreshes next_ic and returns; the batch re-runs the same
                                       untranslated slot, whose fetch fails again, until the batch ends.
So the fix turns that route's host exit (the pre-fix fatal() + exit(1)) into a one-run burst of ~8K halt lines: a guest-drivable
flood under -T.  Arm (b) runs before arm (c), so with running already 0 it shadows the park.  Candidate repairs (for the ruling,
not applied): test `!cpu->running` (the park) before `pc != addr`; or compare pc's aligned value with addr; plus, separately, the
filed bclr/bcctr masking defect, which removes the guest route but not the debugger one.  D11 and V2 (arm (b) edited) are therefore
NOT in an unreached cell.

MEASURED in a scratch clone (blr_table.run.sh -> blr_table/, blr_table_run.log; clone restored, cmp-clean, rebuilt, sentinel
cleared), the same witness at r3 = 0x02040000 / 0x02040001:
  fix (base)        1 / 8278 halt reports   pc 0x02040000 / 0x02040001
  V2  (arm (b) deleted)          1 / 1      pc 0x02040000 / 0x02040001   -- parks: no flood
  D11 (arm (b)'s refresh gone)   1 / 8270   pc 0x02040000 / 0x02048139   -- runs on through stale slots
  CB  (candidate repair: `if (!cpu->running) { park; return; }` inserted BEFORE arm (b)'s `if (cpu->pc != addr)`)
                                 1 / 1      pc 0x02040000 / 0x02040001   -- and the 69-row probe on CB: 69/69, CONTROL=OK
So a session `T blr` (the witness at 0x02040001) would red the fix itself (nonex 8278, want 1): the defect is in the PRODUCT, not
only in the detector, and CB removes it without moving any existing row.  For the ruling.
