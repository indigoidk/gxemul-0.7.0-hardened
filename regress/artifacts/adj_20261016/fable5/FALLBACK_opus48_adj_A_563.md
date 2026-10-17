FABLE_ADJ_A_20261016

Verbatim line from REPAIR3.c.txt, from the block beginning `CONTRACT (vacuity floor clause (e))` (R3:1150):

```
 *    `consumed' (`len == 4', `len >= 2')  a derived input, graded by what the body tests on it (the
```

VERDICT: UPHOLD WITH CHANGES (2 rulings changed: F4, D7) -- D2_and_st is a FLOOR cell, not an equivalent/disclosed one: MEASURED to assert INTRQ where HEAD does not, in a guest-reachable (flag 1, atapi_st NULL, phase CMDOUT, ring occupancy 514) cell; REPAIR4 as drafted (N1-N4) is INSUFFICIENT and owes a fifth row N5 closing the (flag x atapi_st) joint's (flag 1, NULL) half. Everything else the coordinator ruled stands, including the whole PS LIVE list as records/(e).

Seat: Fable 5.1, adjudicator. I answer independently; I did NOT open adj_20261016/astra/ or adj_20261016/grok/. Self-review is disclosed where FR / my own earlier readings are under review.

READ vs REASONED vs MEASURED is tagged on every load-bearing claim. The ONE measurement I made is the F4 harness under `fable5/meas_A/` (private WSL clone of e483d931, nothing written to any project tree but my own answer dir); its log is `fable5/meas_A/f4_run.txt`, the harness `scratch_f4.c`, the build script `build_f4.sh`.

What I opened: the packet; `git show e483d931:src/devices/dev_wdc.c` (md5 714071619d8f98e85fe48ae566139345, = the clone's and the working tree's), in full across the three edited sites, the read/write arms, the dispatch, the drain, status_byte, the CYL/SECCNT/STATUS read arms, wdc_new_command_reset, DEVINIT, and the inbuf primitives; `git show e483d931:` of `src/cpus/memory_rw.c` (the device dispatch and length clamp at :467-523, the MEMORY_RW split at :183-226), `src/disk/diskimage_scsicmd.c` (the result-code returns), `src/cpus/cpu_mips_instr.c` (lld :2932, ldl/ldr), `cpu_mips_instr_unaligned.c`, `cpu_ppc_instr_loadstore.c` (LS_GENERIC_N), `cpu_alpha_instr_loadstore.c` (LS_Q), `cpu_m88k_instr_loadstore.c`, `cpu_arm_instr_loadstore.c` (ldrd datalen), `src/include/thirdparty/wdcreg.h` (phase constants), `src/machines/{machine_landisk,machine_arc,machine_evbmips,machine_cobalt,machine_algor,machine_cats,machine_iyonix}.c` and `src/devices/{bus_isa,bus_pci}.c` (the wdc carriers and base addresses); REPAIR3.c.txt (the CONTRACT block :997-1319, the fixtures the scratch row reuses, main's row registry); SCORES.txt, STATUS.md, the 48 mutants' MANIFEST and the four D2 mutant sources; FR, GP, GA, S4, S4A, CX, the four packet-fed seats, SEATS.txt, AR; the 10-13 adjudication (v1+v2); the carrier floor-rules excerpt; and the PS prescreen `prescreen_563.md` (present).

================================================================================
THE TWO QUESTIONS THE ADJUDICATORS SPLIT ON
================================================================================

## Q2 of the packet: F4 -- can a CMDOUT ring sit so the PIO 512-boundary fires before any dispatch? MEASURED: YES.

**Answer: YES, and therefore D2_and_st HAS a guest INTRQ delta -- F4 is NOT equivalent.**

The dispatch fires only at `inbuf_len == 12` EXACTLY (dev_wdc.c:1717), and the ring is empty on entry to CMDOUT (wdc_new_command_reset flushes it at :923, run unconditionally at :938 before ATAPI_PKT_CMD sets flag+CMDOUT at :1046-1047). But a guest can STEP PAST 12 without landing on it and keep pushing: a 2-byte store then three 4-byte stores give occupancy 2 -> 6 -> 10 -> 14 (the exact stride the packet's question names), after which the dispatch guard never matches again (occupancy only grows, `== 12` is never revisited), so 2-byte stores walk it to any even value. Occupancy 514 is reachable in CMDOUT with flag 1, atapi_st still NULL. A width-2 DATA read then pops 2 FIRST (occupancy 514 -> 512, the pops at :1198-1213 precede the flag test), and the PIO else-branch at :1468 checks `inbuf_tail != inbuf_head && (tail-head) % 512 == 0` -- 512 is a nonzero multiple of 512, so it asserts.

MEASURED (fable5/meas_A/f4_run.txt), driving the REAL `dev_wdc_access` for every store and the read, with the CMDOUT state produced only by what the writers produce (output confirms `st=NULL phase=0x9 dispatched=no`):

```
HEAD       STATE occ=514 ... dispatched=no   READ int_assert=0 sink=0 warned_null_xfer=1
D2_st      STATE occ=514 ... dispatched=no   READ int_assert=1 sink=1 warned_null_xfer=0
D2_or_st   STATE occ=514 ... dispatched=no   READ int_assert=0 sink=0 warned_null_xfer=1
D2_and_st  STATE occ=514 ... dispatched=no   READ int_assert=1 sink=1 warned_null_xfer=0
D2_phase   STATE occ=514 ... dispatched=no   READ int_assert=0 sink=0 warned_null_xfer=1
```

HEAD takes the ATAPI arm (`if (d->atapi_cmd_in_progress)`), finds atapi_len 0 and atapi_st NULL, latches `warned_null_xfer`, asserts NO interrupt. D2_and_st (`flag && atapi_st != NULL`) finds st NULL, takes the PIO arm, and asserts INTRQ at the 512-boundary. So the two differ on a GUEST channel (INTRQ: sink 1 vs 0), not merely on the host latch. F4's premise "differs ONLY in the host latch warned_null_xfer" is FALSE.

**Grade: FLOOR.** The read-arm flag guard (:1228) dominates the re-arm repair (clamp :1427, refill :1460). The repair path reads `d->atapi_st` (:1424 `d->atapi_st->data_in_len`, :1461 `d->atapi_st->data_in[...]`), so `atapi_st` is a repair-path lvalue and (flag x atapi_st) is in pass-11's floor cross-product -- the SAME joint that makes D2_st and D2_or_st FLOOR (coordinator agrees for those). D2_and_st pins the (flag 1, st NULL) cell of that joint; it is reachable (measured) and guest-distinguishable (measured). FLOOR. The 159-row table scores it 0/159 (SCORES.txt), i.e. it ESCAPES; no existing row builds the occ-514-CMDOUT state (the only (flag 1, st NULL) row, `row_null_atapi_st`, does one read on an EMPTY ring in DATAIN and forks checking only WIFSIGNALED). This is exactly the #499 shape the repair-chain amendment warns of: the coordinator's N1/N2 close the (flag 0, *) half of the joint and leave the (flag 1, NULL) half open for the next pass.

This is distinct from F18/F19 (the `|| warned_null_xfer` escapes). Those swap the flag to `warned_null_xfer`, which is NOT read by the repair path, so they are (e) by the repair-path bound (the coordinator's grade stands). D2_and_st swaps to `atapi_st`, which IS read by the repair path -> FLOOR. The coordinator conflated the two by describing F4 in terms of the latch; the operand is the discriminator.

## Q1 of the packet: D3 -- the width `len` grade and reachability of widths 3,5,6,7. Ruling: (iii), the coordinator's reading, with a firmer warrant.

`len` is a FUNCTION INPUT the guarded body tests directly (dev_wdc.c:1255 `consumed = len == 4 ? 4 : (len >= 2 ? 2 : 1)`, and the pop tests at :1201/:1203/:1208/:1210). The 2026-10-09 derived-input ruling (carrier :1598-1608) governs `consumed` -- the derived LOCAL, graded by what the body tests on IT (`consumed > atapi_len`) -- and it does NOT demote the tests the body performs on the input `len` itself. So reading (ii) is wrong: the derived-input ruling does not make the width mutants all (e).

The body-induced partition on `len` (for the consume/pop logic, which is all that reaches a guest channel; the width-8 debug-format branch at :1222 is a no-op `debug()`) is `{1}, {2,3,5,6,7,8}, {4}` -- the ternary's three arms, with width 8 BUCKETED WITH width 2 (both give consumed 2 and pop 2 at HEAD). That is the case-partition reading (iii).

**Reachability of widths 3, 5, 6, 7 at the WDC data port: NONE, on any CPU here (READ).** Every CPU that carries wdc issues only widths 1, 2, 4, 8 at a device data port:
- MIPS (arc R4000/R4400, evbmips 5Kc, cobalt/algor RM5200 -- the ISA and PCI IDE carriers): `lb/lh/lw` = 1/2/4; `lld/ld/sd` issue `sizeof(uint64_t)` = 8 (cpu_mips_instr.c:2932, :2952). `ldl/ldr` go through mips_unaligned_loadstore with `wlen=8` but issue the ALIGNED 8-byte word to the device (cpu_mips_instr_unaligned.c:46-47, 88), never a 3-byte access.
- PPC `lfd/stfd/ld` = 8, Alpha `ldq/stq` = 8, M88K `ld.d` = 8, ARM `ldrd` = 8 -- all power-of-two.
- The device-length clamp (memory_rw.c:495 `paddr + len > device.length`) can only PRODUCE an odd width if an access starts PAST wd_data (device offset > 0), which lands on a different register (`case wd_err` etc.), not `case wd_data`. wd_data is device offset 0.
- The MEMORY_RW split (:183-226) fires at the 1024-byte granule for TRANSLATED accesses only, and its head "can never be a device" (:160, device dispatch `goto do_return_ok`s first). At every real wdc base (0x1f0, 0x170, 0x14000000, 0x900001f0) wd_data (offset 0) is 1024-aligned or far from a 1024 boundary, so an 8-byte read does not straddle; and a straddle's tail chunk starts at device offset >= 8 (>= length), i.e. not this device. So no 3/5/6/7-byte access reaches wd_data.

Width 8 IS reachable (MIPS `lld/ld/sd` on the MIPS wdc carriers), confirming GA's `lld` reading and the #337 comment at dev_wdc.c:1597.

**Ruling (iii):**
- **VD1 (`consumed = len == 4 ? 4 : 2`) -> FLOOR.** It differs from HEAD ONLY at width 1 (widths 2,3,4,5,6,7,8 already consume 2 or 4). Width 1 is the BELOW-the-bound region of `len >= 2` (rule D2, carrier :1538-1550), and the body's own third ternary arm -- a distinguished case. The only width-1 reader (`write route: 1-byte store is refused`, 32768 width-1 reads) has an oracle of occupancy + a constant 0xc3 fill, blind to the consumed change. A floor cell with a blind row. UPHELD (my FR graded it FLOOR; I uphold it harder below).
- **cons_eq2 and bepop_ge4/lepop_ge4 -> (e) DISCLOSED.** cons_eq2 (`len >= 2` -> `len == 2`) and the pops (`len == 4` -> `len >= 4`) differ ONLY at widths {3,5,6,7,8}. Widths 3,5,6,7 are unreachable; width 8 is reachable but BUCKETED with width 2 (not a case the body distinguishes from 2), so it is a value inside the `{2,3,5,6,7,8}` bucket -- clause-(e) coverage debt with a named width-8 delta, exactly as the contract already discloses for `n_C6`/`n_E_cons_ge4`. The far (past-bound) region of `len >= 2` has its BRANCH discharged by the width-2 rows; a width-8 row would only pin the branch, and there is no further bound to pin. So no floor row is owed.

The coordinator wrote it was "least sure of this ruling of any." It is sound: the derived-input ruling attaches to `consumed`, not to `len`; width 1 is a genuine below-bound/case cell with a blind row (floor); the width-8 delta is real (reachable) but bucketed (disclosed). One OPTIONAL width-8 read row would collapse cons_eq2, both pops, n_C6 and n_E_cons_ge4 at once (GA, kimi substitute) -- worth noting as cheap coverage, but NOT floor-owed.

================================================================================
Q1 (packet section 5.1): F1..F25 and D1..D7
================================================================================

F1  D2_st floor -- UPHOLD. MEASURED 0/159; (flag 0, st non-NULL) reachable (writers :917 vs :1735); atapi_st is a repair-path lvalue. FR (mine) predicted it; correct.
F2  D2_or_st floor -- UPHOLD. Same joint, same cell; MEASURED 0/159.
F3  (flag 0, atapi_len>0) floor, Row 2 -- UPHOLD. atapi_len read by the repair at :1424-1427; reset keeps the count (:917-919).
F4  D2_and_st -- **OVERTURN: FLOOR, not equivalent.** MEASURED INTRQ delta (sink 1 vs 0) in the (flag 1, st NULL, CMDOUT, occ 514) cell; atapi_st is a repair-path lvalue. Owes row N5.
F5  D2_phase EQUIVALENT -- UPHOLD. flag and phase written together (:917-918, :1046-1047); every later phase store is inside a flag arm. (flag 0, phase!=0) and (flag 1, phase 0) unreachable.
F6  D3_ge0 EQUIVALENT -- UPHOLD. (atapi_len>0, st NULL) unreachable; sole atapi_st writer :1735 never NULLs.
F7  D7_lt1/D8_lt2 EQUIVALENT -- UPHOLD. diskimage_scsicommand returns only {0,1,2} (returns at :282/:295/:302/:315/:327=0, :892/:1291=2, :1388=1); `res<1`=`==0`, `res<2`=`==1` among {1,2}.
F8  D0_nocmd (e) -- UPHOLD. `!io_enabled` dominates but is NOT a #473/#495-edited guard; the selector `relative_addr != wd_command` flows into none of the three repair bodies (label clause, carrier :1487). Delta 0-vs-0x50 (status_byte ORs DRDY|DSC = 0x50, dev_wdc.c:584-589) disclosed. (= D5.)
F9  D6_head (e) -- UPHOLD. inbuf_head read only through the callee wdc_get_inbuf; DEPENDS-ON stops at the callee (carrier :1433-1434); the body tests the derived local `inbuf_len == 12`. tail!=0 delta disclosed.
F10 D7_latch (e), latch class -- UPHOLD. warned_atapi_err is NOT a repair-path lvalue (the clamp/refill/push/#495-refusal do not read it), so (res x warned_atapi_err) is not a floor joint. BUT note the delta is GUEST-visible (ireason 0x03 vs 0x00), so record it as guest-visible (e) debt, not equivalent. My FR sentence "the reject arm reads no field" was FALSE (:1766 reads it) -- the grade is unchanged (the operand still is not a repair-path lvalue), but the record must drop that sentence. (See D2.)
F11 D8else_latch (e), latch class -- UPHOLD, same as F10 (ireason 0x00 vs 0x01; warned_atapi_dataout not a repair-path lvalue).
F12 bepop_ge4/lepop_ge4 (e) -- UPHOLD. Differ only at width >= 5; widths 5,6,7 unreachable, width 8 bucketed with 2. See D3.
F13 cons_eq2 (e) -- UPHOLD. Differ only at widths {3,5,6,7,8}; 3,5,6,7 unreachable, 8 bucketed. See D3.
F14 cmdlen_ms10 OUT OF CONTRACT -- UPHOLD. The stub copies 12 bytes and never reads cmd_len; the real MODE SENSE(10) switches on it (diskimage_scsicmd.c:569-579). Stated, not rowed.
F15 VD1 FLOOR -- UPHOLD (self-review below). Width-1 below-bound cell, blind sole row. N4 repair is correct (one count read after a 1-byte read distinguishes: HEAD atapi_len n, VD1 n-1).
F16 wrap-normalisation (e), reason corrected, conditional breach REFUTED -- UPHOLD. CHECKED: the drain's guest-visible arm (:1846) requires `write_in_progress` set; wdc_new_command_reset clears write_in_progress (:919) on every command incl. ATAPI_PKT_CMD, so in ATAPI/CMDOUT phases (the only place a one-command ring wrap is reachable) the drain cannot fire; an ATA WRITE drains every 512*count and never accumulates to wrap. Only warned_empty_drain (host latch) differs. (e) stands; R4 corrects the false "never wraps" reason.
F17 Records (17 + 2) -- UPHOLD. Spot-checked: the six walk widths 2/4/2/1/2/2, cmd_len, "6 of 159", the reject-arm break-before-tail, the LE-liveness-stores-0x34/0x12. The R14/R15 upgrades (DATA-OUT count, disabled-DATA-read INTRQ) are free L1 oracle additions on fixtures that already read the channel. ACCEPT.
F18 S4A `flag || warned_null_xfer` (e), latch class -- UPHOLD as (e) BY THE REPAIR-PATH BOUND (warned_null_xfer not read by the repair), but it has the same guest INTRQ mechanism as F4; record it as guest-visible (e) debt. S4A itself conceded "strict pass-11 grading would call the cell (e)."
F19 S4A `writeflag==MEM_READ || warned_null_xfer` (e), latch class -- UPHOLD (same reasoning; occupancy-2-vs-0 delta, warned_null_xfer not a repair-path lvalue).
F20 S4A joint (flag 0, atapi_len 0, received<data_in_len, st non-NULL) FLOOR, Row N3 -- UPHOLD. Every operand is a repair-path lvalue; reachable (S4A's derivation). This is a flag-0 cell, distinct from N5's flag-1 cell.
F21 glm NOT CHECKABLE -> settled by F16 -- UPHOLD. The drain premise is settled by reading write_in_progress's writers.
F22 minimax CLEAN REFUTED -- UPHOLD. minimax reasoned only about (flag 1, st NULL) as the latch cell and missed both the (flag 0, st non-NULL) escape AND (measured here) the (flag 1, st NULL) INTRQ escape.
F23 codex panel REFUSED; CX answered -- UPHOLD (seat ledger).
F24 AR's four BROKEN = F4/F1-2/F10-11/F12-13; its D0_nocmd/D6_head "EQUIVALENT" refuted -- UPHOLD, with the caveat that AR was RIGHT to call F4 ("D2_and_st") a real gap: the measurement vindicates AR over the coordinator on F4.
F25 scratch-row stage never run; REPAIR4 PRETABLE must measure every new row -- UPHOLD, and strengthen: it must also measure N5 on HEAD and on D2_and_st (and D2_st), since N5 is the row the un-run stage would have forced.

D1 D2_st floor -- UPHOLD (minimax addressed only (flag 1, st NULL); measured 159/159 + reachable (flag 0, non-NULL)).
D2 latch-operand class (F10/F11/F18/F19) = (e) -- UPHOLD. The operands (warned_atapi_err/dataout/null_xfer) are not read by the repair path, so they fall outside pass-11's floor; (e) coverage debt with the guest deltas named. FR's "reads no field" is refuted and must go, but the GRADE does not move (the field it reads is not a repair-path lvalue). **This is the correct line, and it is exactly what separates D2 from F4**: F4's operand (atapi_st) IS a repair-path lvalue, so F4 is floor while the latch class is (e). The coordinator drew that line for F10/F11/F18/F19 and then failed to apply it to F4.
D3 VD1 floor, cons_eq2/pops (e) -- UPHOLD (reading iii; warrant and reachability above).
D4 GA's "D2 edge is length 3" does not bind cons_eq2 -- UPHOLD. The ternary's `len >= 2` does not dominate the edited lines (both branches reach them), so D2 does not bind it; width 3 is unreachable anyway. Folded into D3.
D5 D0_nocmd (e) under the third disjunct -- UPHOLD (= F8). `!io_enabled` is not an edited guard; the 2026-09-25 disjunct binds the EDITED guard's repair.
D6 S4's two new rows over FR's one-line edit of the shipped PIO row -- UPHOLD. The new rows keep the measured row byte-identical and also hold F3's cell; FR's edit leaves F3 open. (Self-review: S4's shape is the right call over my FR's.)
D7 D2_and_st host-latch-only: disclose -- **OVERTURN: ROW IT.** Measured guest INTRQ delta -> floor (see F4). Owes N5.

================================================================================
Q2: WHICH ACCEPTED DISPOSITION IS WRONG? -- F4 / D7.
================================================================================

Of the coordinator's 21 accepted-or-refined dispositions, the wrong one is **F4 (and its disagreement-ruling D7)**: D2_and_st was graded "EQUIVALENT ON GUEST CHANNELS, disclosed; no row," and it is a FLOOR cell with a measured guest INTRQ delta. The coordinator's own section-4 self-doubt pointed here ("agreement is not evidence"; the packet even posed it as question 2), and the discriminator the coordinator applied correctly elsewhere -- *is the swapped operand a repair-path lvalue?* -- answers YES for atapi_st (F4) and NO for the latches (F10/F11/F18/F19). The coordinator described F4 by the field that co-varies (warned_null_xfer, a latch) instead of by the operand that was swapped (atapi_st, a repair-path lvalue), and that framing produced the wrong grade. It is a one-row cost and, because REPAIR4 is pre-ship, L1 construction -- but left unfixed it is a clean-sweep escape the closing pass would find (the #499 pattern: the symmetric half of a joint left open).

No other accepted disposition is wrong on my check. The 20 EQUIVALENT/(e)/OUT/RECORD grades each rest on a fact I either read (the result domain {0,1,2}, the phase/flag co-writers, the width reachability, the drain's write_in_progress gate, status_byte's 0x50) or measured (the D2_phase/D3_ge0/D7_lt1/D8_lt2 controls came back matching HEAD in the same harness run).

================================================================================
Q3: WHAT DID ALL OF US MISS?
================================================================================

**The class is NAMED correctly** ("the operand-swap axis of every dominating guard"). **The ENUMERATION is incomplete by one floor cell, and S4's G0-G13 + S4A's additions mis-graded it.** S4 §1's G3 bullet enumerated the (flag x atapi_st) joint and wrote the (flag 1, st NULL) cell as "guest-EQUIVALENT ... only warned_null_xfer differs." That is the cell I measured as a guest INTRQ escape. So the missing member is:

> **(flag 1, atapi_st NULL, phase CMDOUT, ring occupancy a nonzero multiple of 512 after the read's pops)** -- reached by: ATAPI_PKT_CMD, then data-port writes stepping occupancy 2,6,10,14 (one 2-byte then three 4-byte stores) and 2-byte stores on to 514, then one width-2 DATA read. HEAD latches warned_null_xfer and asserts nothing; D2_and_st (and D2_st) take the PIO arm and assert INTRQ. MEASURED, fable5/meas_A/f4_run.txt.

S4A came CLOSEST -- it built the 514-byte boundary read -- but applied it to the `warned_null_xfer` operand (correctly (e)) and never to the `atapi_st` operand (which is floor). The coordinator, FR (mine), minimax and the ruling all treated the (flag 1, st NULL) cell as latch-only. The complete (flag x atapi_st) floor joint has FOUR cells: (0,NULL) HEAD-equal; (0,non-NULL) Row 1/Row 2 [N1/N2]; (1,NULL) **N5 [missing]**; (1,non-NULL) the existing re-arm rows. REPAIR4 must close all four in one diff.

================================================================================
Q4: IS REPAIR4 (N1-N4 + R14/R15 + contract) SUFFICIENT FOR THE CLOSING PASS?
================================================================================

**No.** As drafted it closes only the flag-0 half of the (flag x atapi_st) joint, so the closing pass re-measuring the enumeration would find D2_and_st escaping 159/159 -- the exact repair-chain failure mode (a symmetric cell left open). The smallest change that makes it sufficient:

1. **Add row N5** `CMDOUT boundary read, no transfer` (name <= 36 chars): fixture = enter CMDOUT (flag 1, phase CMDOUT, st NULL, atapi_len 0), push occupancy to 514 through real data-port stores stepping past 12 (2,6,10,14,... as above), one width-2 DATA read; ORACLE `rep_asserts == 0 && warned_null_xfer == 1` (HEAD's behaviour). It reddens D2_and_st AND D2_st on this cell (both take PIO and assert; both set warned_null_xfer 0). It cannot redden an unchanged row: no existing fixture builds occ-514-CMDOUT, and D2_or_st/D2_phase/the equivalents stay on HEAD's ATAPI arm here. CHANNEL: INTRQ (and the latch), knowable at writing time. Measured basis: fable5/meas_A/f4_run.txt.
2. **Write the full (flag x atapi_st) cross-product into the contract**: four cells, which rows cover which (N1/N2 the flag-0 pair; N5 the (1,NULL) cell; the re-arm rows the (1,non-NULL) cell), so the closing pass VERIFIES the enumeration rather than hunts cells -- the class-closure amendment's own requirement.
3. **N1-N4 otherwise stand** (D6: S4's two rows over FR's one-line edit; N3 for F20; N4 for VD1). R14/R15 oracle additions stand.
4. The PRETABLE for REPAIR4 must MEASURE N5 on HEAD, D2_st, D2_or_st, D2_and_st and D2_phase before table 1 (F25), since N5 is precisely the row the un-run scratch-row stage would have forced.

With N5 added, the closing pass can report a VALID zero (diff delivered, roster stated, the enumeration named with its denominator) and the chain closes -- provided that pass finds zero further breaches of the class.

================================================================================
Q5: PS (prescreen_563.md) -- rule on each LIVE item.
================================================================================

PS IS present (it was populated after my first directory listing). Its 14 distinct LIVE items are all READ-backed, and PS itself states none is floor; I spot-checked the load-bearing ones against the frozen REPAIR3 and confirm every one is a records correction or a clause-(e) sentence. **None adds a row; none changes REPAIR3's shippability; all are distinct from and additional to my N5 floor finding.** Rulings:

In R3 as frozen (ride the REPAIR4 records batch):
1. c563_edges F15 -- UPHOLD (records L4). CONFIRMED: R3:837 "68930 remain" vs R3:6241 "68928" -- an internal inconsistency; the row's `min(remaining,32768)=32768` logic is unaffected, the number is wrong. Correct R3:837 (and OUTSTANDING_BUGS.md:24607) to 68928 at the compare.
2. c563_contract F16 -- UPHOLD (records L4). CONFIRMED: R3:1230-1231 "the R-rows ... call the primitive DIRECTLY" contradicts R3:5242 "R7 and R8 cover the BULK arm, which bypasses wdc_addtoinbuf() entirely." Bracket-correct in place.
3. c563_widths F2 -- UPHOLD (records L4). CONFIRMED: R3:1449 "what the reads actually POP" vs dev_wdc.c:1229-1245 "counts ATTEMPTS too" (ledger `wdcconsumedattempts`). Bracket.
4. c563_widths F3 -- UPHOLD (records L4). CONFIRMED: R3:1996-1998 ("NO PHASE CHECK") and R3:2172-2173 ("default: arm only latches") are pre-#495 present-tense claims without the bracket R3:919 carries. Bracket both.
5. c563_edges F24 -- UPHOLD (records L4). CONFIRMED: R3:2778 ("NOTHING RESETS THE PHASE") and R3:2818-2819 stand uncorrected beside the row's own oracle correction; the carrier's laundering rule (a re-pinned oracle beside an uncorrected claim) requires the bracket. The quoted pre-#479 CODE is legitimate provenance; the present-tense PROSE is not.
6. adj_563_ruling F5 -- UPHOLD. R3:7462-7463 cites the uncommitted 2026-10-09 clause-(c) ruling; add it to R4SPEC R5's uncommitted-citation list (moot if the carrier copy lands in the same commit).
7. c563_edges F6 -- UPHOLD ((e)). A write-side `case 3:` accept mutant in CMDOUT: width 3 is unreachable (my D3 reachability analysis), and its two badlen cells are both rowed; one (e) sentence beside R3:1177, or build the one-line mutant and record its score.

In the records the commit carries:
8. adj_563_ruling F4 -- UPHOLD (records). RULING:38-39/ASTRA:50 cite an owner "write-target exclusion" with no text in any carrier (0 grep hits). The RULING errata must name the warrant actually used (the committed DEPENDS-ON bound / the derived-input ruling) or the owner says where it lives; the CHANGELOG must not cite it as carrier text. (This is the same hazard my D2/F10 handling avoids: ground the latch grade in the repair-path-lvalue bound, which IS committed, not in an unwritten exclusion.)
9. changelog_563_draft F11 -- UPHOLD (records). The BE case-4 byte-lane shift is called "Filed" with no ledger slug; file it as coverage debt or correct the errata.
10. changelog_563_draft F14 -- UPHOLD (records). "eight one-token variants" (ledger title :62365) vs CHANGELOG.md:197-198 "four one-token moves ... four content variants"; the commit uses the committed split and may correct the title.

Outside #563's material (file separately, not part of this detector round):
11. c563_seats F4 -- UPHOLD (outside #563). seat_verdicts.py:354 labels a column "bytes" but prints `len(decoded_text)`; a one-line harness fix (os.path.getsize or relabel). Ledger figures already use wc -c, so no #563 record is wrong.
12. wdcrearmwalk_tape F3 -- UPHOLD (outside #563). The `wdcrearmwalk` row's ranking omits that its own `ciR:` CD-ROM reaches multi-re-arm transfers via READ(10) > 128 blocks; record the reachable command on that row.
13. wdcrearmwalk_tape F4 -- UPHOLD (outside #563). The state_note arithmetic (ledger.json:26688) is inconsistent (8 x 32768 = 262144, not 262656); correct or qualify on that row.
14. wdcrearmwalk_tape F6 -- UPHOLD (outside #563). doc/misc.html:254-256 `t4:` = SCSI, but IDE-default machines make it an IDE tape; file a LOW doc row.

I did not find a PS item mis-classified. The PS LIVE list and my N5 are complementary: PS screened the grok/Argon readings of the #563 briefs (records/(e)); N5 came from re-measuring the operand-swap joint the measuring seat left unmeasured.

================================================================================
SEAT-SPECIFIC (self-review)
================================================================================

**F1, harder on it.** My FR reading (fable5_r3pass.md) got D2_st right as FLOOR but had the SAME hole the coordinator has: I enumerated the (flag 1, st NULL) difference site and then dismissed it -- "the ONE site with the flag SET and atapi_st NULL is :1974, row_null_atapi_st ... GREEN under the mutant" -- treating that cell as reachable only by the one empty-ring DATAIN fixture. I missed that a guest can reach (flag 1, st NULL) at ring occupancy 514 in CMDOUT, where the PIO 512-boundary makes it a live INTRQ escape. So my own "Prediction: 159/159" for the denominator was right about the score and wrong about the grade of one cell. The measurement corrects me, not just the coordinator.

**F15, harder on it.** I uphold my FR grade of VD1 as FLOOR, and I checked the REPAIR, not just the finding: N4 (one count read -- CYL_LO/CYL_HI -- after the first 1-byte DATA read, want the un-decremented count) reddens VD1 (HEAD leaves atapi_len n, VD1 leaves n-1) and is a pure oracle addition on the existing 1-byte walk, so it perturbs no other mutant and width 1 is unchanged for all of them. Sound. The one thing to watch: N4's oracle must read a COUNT register (CYL_LO/HI), not occupancy or the fill -- that is the whole point of the finding (the existing width-1 row's channel is blind).

**Checking the coordinator's REPAIR, not just the findings.** N1/N2/N3/N4 + R14/R15 are correct as far as they go. The gap is N5 (F4/D7), above. With N5 the operand-swap class is closed in one diff as the repair-chain amendment requires; without it the closing pass finds D2_and_st and the chain runs another pass.

FABLE_ADJ_A_20261016 -- end of answer.
