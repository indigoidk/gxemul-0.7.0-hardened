# Fable 5.1 -- HELD stage question (lecsrmask, pass 1, 2026-10-25)

The question this stage is held for, in one line: **Is the pass-1 design READY -- the three store masks (CSR1 & 0xfffe,
CSR2 & 0x00ff, CSR3 & 0x0007) at `le_register_write()`'s `default:` arm, the unreachable parity warning deleted, and the
18-row detector with its six floor cells and its contract -- and which of the brief's premises P1-P12 is false?**  Answer
the brief `packet.md` in this directory as its section 11 directs (VERDICT line first, Q1-Q4), as the other seats did.

Transport while the seat is held: the Claude Code cloud route (a one-time routine with the packet inlined), per the owner's
2026-10-25 ruling.  If the route does not answer, the stage stays HELD with this question.

**Status 2026-10-25 04:2x.**  The cloud route was attempted and NOT completed: the main loop's call that inlined the
73 KB packet into a one-time routine was stopped by the response safety classifier before it ran (the packet carries the
round's variant table).  Owner ruling 2026-10-25 03:1x applies -- one stop of the main loop's own = stop and report -- so
the route is not retried and this stage stays HELD with the question above until the owner decides (a short routine
pointing at the brief as a published page, or the seat itself once its hold lifts, are the two options).

**Question SUPERSEDED 2026-10-25 05:2x by the F2 ruling (narrowing).**  The held question is now: **Is the NARROWED
design ready -- a CSR3-only store mask (`x & 0x0007`, form A: an explicit `case 3:` arm), CSR1 and CSR2 left stored whole as
the model's existing behaviour (an interpreted reading: the Am7990 manual specifies read-as-zero for RAP and CSR3 only;
MAME keeps CSR1/CSR2 writable on the Am7990 for a board diagnostic; the C-LANCE reads CSR2's reserved bits as zero), both
STOP comments corrected as records, the 20-row detector with its contract (`pass1_20261025/PASS1_RULINGS.md` section 3), and
the clause-(d) variant table recorded as OWED -- and which of the F2 rulings (`f2_20261025/F2_PACKET.md`, Astra's
`codex_t18f2.txt` the ruling of record) is wrong?**
