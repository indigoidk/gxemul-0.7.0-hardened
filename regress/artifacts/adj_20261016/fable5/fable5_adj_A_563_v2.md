VERDICT: UPHOLD WITH CHANGES (2) -- F4/D7: the D2_and_st variant is not equivalent; the measured CMDOUT occupancy cell (fable5/meas_A/f4_run.txt) shows it raises the interrupt line where HEAD does not, so it is an undetected variant on a floor cell and the next repair owes it a row (N5); every other ruling stands.

FABLE_ADJ_A_20261016 -- Fable 5.1, packet A (#563 wdc473floor), v2, written as myself after the interrupted run. The earlier file, now FALLBACK_opus48_adj_A_563.md, is not credited to me; I used it only as a colleague's notes. The one measurement cited is meas_A/f4_run.txt from that run (HEAD dev_wdc.c md5 71407161, the four D2 variants from r3pass_20261013/opus5/mutants/). Everything else is READ from e483d931 or REASONED from it, and marked so.

## F1-F25

F1  AGREE -- D2_st is undetected by all 159 rows (SCORES.txt) and its differing state (flag 0, atapi_st non-NULL) is left behind by every later command after any packet dispatch (writers :917 vs :1735); a row is owed.
F2  AGREE -- D2_or_st, same cell, same measured escape, same row.
F3  AGREE -- (flag 0, atapi_len > 0) is a reachable state (the reset clears the flag, not the count) that D2_len was only detected on the other cell; Row 2 pins it.
F4  DIFFER -- D2_and_st is NOT equivalent: f4_run.txt shows HEAD `int_assert=0 sink=0 warned_null_xfer=1` and D2_and_st `int_assert=1 sink=1 warned_null_xfer=0` on the same guest-reachable input, so the interrupt line differs, not only the warning latch; floor, row owed.
F5  AGREE -- D2_phase is equivalent: flag and phase are written together (:917-918, :1046-1047) and every other phase store sits inside a flag arm, so the differing states never occur (f4_run.txt also shows it matching HEAD).
F6  AGREE -- D3_ge0 is equivalent: a non-zero count with a NULL transfer never occurs (sole atapi_st writer :1735, never cleared).
F7  AGREE -- D7_lt1 / D8_lt2 are equivalent: diskimage_scsicommand returns only 0, 1, 2 (:282/295/302/315/327, :892/1291, :1388).
F8  AGREE -- D0_nocmd is disclosed debt, not floor: the io guard was not edited by this round and the register selector reaches none of the three repaired bodies; the 0-versus-0x50 status delta is written down.
F9  AGREE -- D6_head is disclosed debt: the dispatch body reads inbuf_head only through a callee, and the guard tests the computed count `== 12`; the tail != 0 state is written down.
F10 AGREE -- D7_latch is disclosed debt: warned_atapi_err is not read by the repaired code (clamp/refill/push/refusal); but record its delta as guest-visible (ireason 0x03 vs 0x00), and drop my earlier sentence "the reject arm reads no field" (it reads the latch at :1766; the grade does not move).
F11 AGREE -- D8else_latch, same class, same reasoning (ireason 0x00 vs 0x01).
F12 AGREE -- bepop_ge4 / lepop_ge4 are disclosed debt: they differ only at widths >= 5; 5/6/7 cannot reach the data register and 8 is bucketed with width 2 (see (a)).
F13 AGREE -- cons_eq2 is disclosed debt: it differs only at widths 3 and 5-8 (see (a)).
F14 AGREE -- cmdlen_ms10 is outside the suite's contract: the stub never reads cmd_len; stated, not rowed.
F15 AGREE -- VD1 is a floor cell: width 1 is a case the body separates and the only width-1 row observes occupancy and a constant fill, which VD1 cannot move; one count read after a 1-byte read (N4) detects it.
F16 AGREE -- the wrap-normalisation variants stay disclosed debt and the "never wraps" reason is a wrong record; the conditional breach is refuted because the drain needs write_in_progress, which every command's reset clears (:919), so it cannot fire in the one-command wrap scenario.
F17 AGREE -- the records corrections (R1-R17 + two) and the R14/R15 oracle additions are right; spot-checked the walk widths 2/4/2/1/2/2, "6 of 159", the LE liveness store, the reject-arm break.
F18 AGREE -- `flag || warned_null_xfer` is disclosed debt: the latch is not read by the repaired code; it uses the same occupancy-boundary mechanism as F4, so write it down as guest-visible debt, not as equivalent.
F19 AGREE -- `writeflag == MEM_READ || warned_null_xfer`, same class.
F20 AGREE -- the joint (flag 0, len 0, received < data_in_len, st non-NULL) is a floor cell (every operand is read by the repair); Row N3 pins it; it is a flag-0 cell, distinct from F4's flag-1 cell.
F21 AGREE -- glm's open premise is settled by F16.
F22 AGREE -- minimax's CLEAN is refuted; it missed both the flag-0 escape and the flag-1 one now measured.
F23 AGREE -- codex panel seat refused, CX answered; ledger only.
F24 AGREE -- with one addition: AR was right to call D2_and_st a real gap, and f4_run.txt bears it out.
F25 AGREE -- the next repair's pre-table must measure every new row on HEAD and the named variants before table 1, and that now includes N5 against D2_and_st and D2_st.

## D1-D7

D1  AGREE -- D2_st floor; minimax argued the wrong cell.
D2  AGREE -- the latch-operand class is disclosed debt, by the repair-path bound; the measured guest deltas are recorded, not erased; this is the line that separates it from F4 (atapi_st IS read by the repair, the latches are not).
D3  AGREE -- VD1 floor; cons_eq2 and the pops disclosed (see (a)).
D4  AGREE -- the width compare does not dominate the repaired lines (both outcomes reach them), so rule D2's edge rule does not bind it, and width 3 is unreachable anyway.
D5  AGREE -- D0_nocmd disclosed; the io guard is not an edited guard.
D6  AGREE -- S4's two new rows over my one-line edit of the shipped PIO row: they keep the measured row intact and also pin F3.
D7  DIFFER -- D2_and_st must be rowed, not disclosed: it is an undetected variant whose differing output is the interrupt line (f4_run.txt), on a cell of the same (flag x atapi_st) joint that already carries two floor rows.

## (a) The access-width cells

Grade: VD1 is floor; cons_eq2, bepop_ge4 and lepop_ge4 are disclosed debt. The width `len` is an input the handler tests directly at :1255 (`len == 4`, `len >= 2`) and at the pop sites; the 2026-10-09 derived-input ruling attaches to the computed local `consumed`, not to those tests, so it does not make the width cells all debt. The tests separate three cases: {1}, {2,3,5,6,7,8}, {4}. VD1 changes only the width-1 case, whose sole row cannot see the change -- floor, one count read fixes it. cons_eq2 and the pops change behaviour only at widths 3 and 5-8, inside the bucket the handler does not split from width 2 -- debt, written down with the width-8 delta.

Can widths 3/5/6/7 reach the data register? No, on any CPU in this tree (READ). The CPUs that carry wdc issue 1/2/4/8-byte accesses only: MIPS lb/lh/lw and lld/ld/sd (cpu_mips_instr.c:2932-2953), and the unaligned ldl/ldr helper reads the ALIGNED 8-byte word (cpu_mips_instr_unaligned.c:46-47, :88-89); PPC lfd, Alpha ldq, M88K ld.d and ARM ldrd are 8. The device-length clamp (memory_rw.c:495-523) shortens only an access that starts PAST offset 0, which is a different register, not the data register. The 1 KB-granule split at memory_rw.c:183-226 applies to translated accesses only and can hand the device a short chunk only if the data register sits at the top of a granule (offset 0x3f9-0x3ff) or at the bottom of one (offset 0) with a successful head chunk from the bytes below it. The wdc bases are 0x1f0/0x170 (ISA and PCI IDE), 0x900001f0 (arc), 0x14000180 (hpcmips) -- none near a granule edge -- and 0x14000000 (landisk, 1 KB-aligned), whose CPU is SH-4: it issues no 8-byte access (an 8-byte fmov is two 4-byte memory_rw calls, cpu_sh_instr.c:798), traps misaligned ones (SH_ALIGN_CHECK_LD, :774), and has nothing mapped immediately below the device for a head chunk to succeed in. Width 8 does reach the register (MIPS lld/ld/sd at the 8-aligned 0x1f0 on arc, evbmips, cobalt, algor), which is why cons_eq2 and the pops are debt with a real delta rather than out of contract.

## (b) The CMDOUT occupancy cell and D2_and_st

Yes: it is a coverage row the next repair owes. The dispatch fires only at occupancy exactly 12 (:1717), and a run of stores can step over it (2, 6, 10, 14, then 2-byte stores to 514) without ever dispatching -- f4_run.txt confirms `st=NULL phase=0x9 dispatched=no` at occupancy 514 with every store driven through the real handler. One width-2 read then pops two bytes before the flag test (occupancy 512), and the PIO branch's 512-boundary test fires. HEAD, with the flag set, takes the transfer-accounting branch, latches warned_null_xfer and raises no interrupt; D2_and_st, finding atapi_st NULL, takes the PIO branch and raises one (`sink=1`). The operand it swaps in, atapi_st, is read by the repaired refill (:1424, :1461), so (flag x atapi_st) is a floor joint -- the coordinator already grades its (flag 0, non-NULL) cells floor (Rows 1 and 2) -- and this is its (flag 1, NULL) cell. No existing row builds that occupancy (the one flag-1/NULL row reads an empty ring and checks only that the process did not terminate), which is why the variant went undetected 159/159. Row N5: enter CMDOUT, drive occupancy to 514 through data-port stores, one width-2 read, want no interrupt and the latch set. It detects D2_and_st and D2_st on this cell; D2_or_st, D2_phase and the equivalents match HEAD here (f4_run.txt), so it cannot redden an unchanged row. Without it the next repair closes half a joint and the pass after finds the other half -- the pattern the repair-chain rule exists to stop.

## Which coordinator disposition is wrong

F4 (with D7). The coordinator described D2_and_st by the field that co-varies -- the warning latch -- instead of by the operand that was swapped -- atapi_st, which the repair reads -- and so graded a floor cell as equivalent. The same discriminator, applied correctly to F10/F11/F18/F19 (latches the repair does not read), gives debt; applied to F4 it gives floor. The measurement in f4_run.txt settles it. Every other accepted disposition rests on a fact I read (the result-code domain, the flag/phase co-writers, the width reachability, the drain's write_in_progress gate, status_byte's 0x50) or on a control that matched HEAD in the same run (D2_phase, D2_or_st).

PS (prescreen_563.md) is present: its 14 LIVE items are records corrections or disclosed-debt sentences (spot-checked the 68930/68928 figure, the "R-rows call the primitive DIRECTLY" sentence, and the un-bracketed stale row comments); none adds a row, none is floor, and they are additional to N5.
