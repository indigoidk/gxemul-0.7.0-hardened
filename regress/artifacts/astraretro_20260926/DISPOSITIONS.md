# Astra retro-review (2026-09-26) -- FINAL dispositions, batch by batch

Owner 2026-09-26: "If astra hasn't reviewed old patches; please do that as well" / "keep pushing astra".  Each batch is:
GPT-6 Astra's retro answers (`<job>/codex_<job>.txt`) -> the Fable seat's adjudication (`adjudication/fable_batch*.md`,
model verified by `agent_models.py`) -> GPT-6 Astra's confirmation (`adjudication/codex_astraconfirm_batch*.txt`).  A
disposition is FINAL here only when both have ruled; Astra's amendments are applied in the text below.  Rule applied
throughout: the LATE-DISSENT rule -- closure changes the licence, never the truth-value; nothing is fixed by this record.
Batches 3f, 3g and 3h were RULED BY THE GROK SEAT (grok-4.7 xhigh, first-hand: `adjudication/grok_20261002/`) and
confirmed by GPT-6 Astra -- owner 2026-10-02: the working seats are Astra, agy and grok, and the Fable seat was
deliberately not fired.  Each batch header names its ruler.  A flagship sign-off on those three is batched, not waived.

Legend: NEW = a new queue row (severity); FILED = the defect already has a queue id; L4 = a false comment or record, to
be corrected in place by a records round; GAP = a test-coverage row to file; UNSETTLED = a named measurement owed.

---

## Batch 1b -- src/include/ bundles (19 findings).  Fable: 6 NEW, 3 FILED, 9 L4, 1 GAP (claude-fable-5-1, clean).
## Astra: 0 of 19 wrong, 8 amended (codex_astraconfirm_batch1b.txt).

NEW
* `ppcbatppkill` HIGH -- PPC: a BAT hit with PP=00, or a store through a read-only BAT, reaches `fatal()` + `exit(1)`
  (memory_ppc.c `ppc_bat_block` -> `:273-276`) instead of a DSI/ISI (ppc_pem32_rev2_2001.txt:13503-13519).  Also
  precedes the FLAG_NOEXCEPTIONS test, so a debugger `dump` of such a block ends the process.  Rung-3 witness owed.
* `ppcfmasingle` HIGH -- PPC opcode-59 `fnmadds`/`fnmsubs` (and Rc forms) are undecoded and stop the emulator
  (cpu_ppc_instr.c:5197-5218 -> `goto bad`).  `fmadds`/`fmsubs` are ALREADY FILED by prose (OUTSTANDING_BUGS.md:1705,
  :1712) -- cross-reference or consolidate, do not double-file.  L4 rider: the stale double-form lines at
  OUTSTANDING_BUGS.md:1610, :1712 and :3085 (the double forms decode at cpu_ppc_instr.c:5263-5269).
* `ppcbatstale` MED -- mtspr to a BAT / HID0[HIGH_BAT_EN] (and MSR IR/DR) never invalidates the translation cache; isync
  is a nop.  Source-derived, no witness; rung-3 probe owed before any edit.
* `divbyinfnan` MED -- `ieee_div_round_rm()` / `ieee_div_round_to_odd()`: a finite dividend with |a| >= 2^-969 over an
  infinite divisor yields a NaN or +/-2^-1074 where the ISA owes a signed zero (float_emul.c:895-902, :987-1009; below
  2^-969 the quotient returns before the residual -- Astra's qualifier).  `_to_odd` is wrong under NEAREST too (m88k
  OpenBSD default).  L4 rider: float_emul.h:91 "non-finite operands and results pass through untouched".
* `m88ksddovf` MED -- m88k single-destination arms with a double source: an intermediate overflowing DOUBLE stores
  +/-Inf where MC88100 Table 2-6 owes the largest finite value (mc88100.txt:2484-2505).  Wrong in 4 of 6 directed-mode
  cells (Astra's corrected count); fmul/fdiv `.ssd/.sds/.sdd` need only one double source.
* `scsicapnosense` MED -- the #163 transfer-cap refusals (READ, WRITE) return CHECK CONDITION with the sense latch
  cleared (diskimage_scsicmd.c:773-778, :880-885).  Reachable via a guest MODE SELECT block size (:1319-1324) or the
  fixed-block tape READ's 24-bit count (:704-713) -- NOT via diskimage.c:1988, which is inside `#if 0` (Astra).  L4
  rider: CHANGELOG.md:27202.

FILED (confirmed at HEAD): `wdcpktstatus`, `OB-24`, `m88kidledup`.

L4 (corrected text in fable_batch1b.md unless amended here)
* include1:F7 CHANGELOG.md:27318-27321 (diskimage size bound: the divisor, not the product).
* include1:F8 float_emul.h:66-69 -- AMENDED (Astra): "RZ and LEGACY return nf unchanged; callers requiring an
  integral value must supply truncation or a guarded integer cast" (cpu_ppc_instr.c:1687 feeds comparisons uncast).
* include1:F9 float_emul.h:50-53 + siblings float_emul.c:410-412, :705-711 (the #331 qualifier).
* include1:F10 dreamcast_sysasicvar.h:102-111 (288 values in three ranges, not 352).
* include1:F11 CHANGELOG.md:32666 (ten raised rows over seven causes).
* include2:F3 timer.h:57-59 -- AMENDED (Astra): condition equivalence on all due callbacks fitting the per-signal
  budget (timer.c:281-289; diff_timer.c:388-396 shows a stalled 100 kHz timer hitting the cap).
* include2:F4 timer.h:46-53 -- AMENDED (Astra): distinguish frequency normalisation (+INF -> 2,147,483,647 Hz) from the
  callback budget (at most 1,048,576 per timer per signal).
* include2:F5 machine.h:63-67 + debugger_cmds.c:65 -- AMENDED (Astra): "`breakpoint add addr, N` skips the first N
  ordinary hits and starts stopping at hit N+1", with the delay-slot exception.
* include2:F6 CHANGELOG.md:22086-22091 (the missing-swap signature).

GAP: `timerupdrow` LOW -- diff_timer.c never reaches timer_update_frequency()'s store on a CHANGE (both calls re-send the
already-normalised rate).

UNSETTLED: none.

---

## Batch 1a -- dev_wdc.c, dev_dreamcast_gdrom.c, dev_sh4.c (30 findings).
## Fable: the dispositions were written by claude-opus-4-8 after two refusals (a fallback, NOT a seat answer); the
## Fable seat then reviewed them FIRST-HAND on its resumed agent (claude-fable-5-1): 29 kept, 1 changed
## (adjudication/fable_batch1a_ruling.md).  Astra: 4 of 30 wrong, 6 amended (codex_astraconfirm_batch1a.txt).

NEW
* `gdromdmareentr` HIGH -- GD-ROM DMA aimed at its own `+0x18` trigger re-enters `dev_dreamcast_gdrom_dma_access`
  through `memory_rw(PHYSICAL)` with the arming words and `d->data` unchanged: unbounded recursion, the process ends
  (dev_dreamcast_gdrom.c:1502-1503; memory_rw.c dispatches back into the same handler).  No in-flight guard.
* `sh4tmupending` MED (Fable first-hand: LOW -> MED) -- unacknowledged SH4 TMU underflows accumulate unsaturated in
  `timer_interrupts_pending[]` (dev_sh4.c:527) and DEVICE_TICK re-asserts while pending > 0, even for a stopped timer
  (:604-607); the manual defines UNF as one status bit (sh7750_hardware.txt:20741-20755).
* `wdcnien` MED -- nIEN is read nowhere in dev_wdc.c; every completion asserts INTRQ with nIEN set (ATA-2 :1311-1314).

FILED (confirmed at HEAD): `wdcpktstatus`, `wdcbeoddtail`, `wdcresetirq`, `wdcsrstnoedge` (Astra: the model acts on the
asserted RST LEVEL of each control write -- there is no edge detection), `wdcaltdecode`, `wdccylwrap`, `pcicmergeA`.

UNDISCHARGED L2 OBLIGATIONS, FILED AS ROWS (Astra overturned Fable's CONFIRMED-FILED: CHANGELOG records them, no queue
row exists):
* `M2_gdromnodatawidth` -- CHANGELOG.md:2896-2909 grades it L2; the committed gdrom_default_probe.py has no
  `nodata byte`/`accept byte` row (only an untracked diff artifact does); the no-data session uses word stores
  (:899-902).  File with its L2 status.
* `M1_sh4latchleak` -- CHANGELOG.md:2896-2903 grades it L2; sh4_chcr_probe.py:572-577 stores once per tested channel
  (only channel 0 repeats, :550-553), so the (1,set) and (7,set) cells have no row.  File with its L2 status.

L4 (Fable's replacement texts in fable_batch1a.md unless amended here)
* wdc:F8 dev_wdc.c:402-407 (65,280 sectors IS reachable since #414).
* wdc:F9 dev_wdc.c:1373-1423 -- AMENDED (Astra): "#484 repaired capacity handling; #495 repaired DATA-IN write
  injection" (dev_wdc.c:1576-1578); and OUTSTANDING_BUGS.md:11591-11598's live-phase statement is itself stale.
* wdc:F10 dev_wdc.c:1660-1682 ("NOTHING RESETS THE PHASE" is false since #479; SRST also clears the flag).
* wdc:F11 -- OVERTURNED (Astra): not UNSETTLED but L4.  dev_wdc.c:1716-1717 requires CMDOUT before the free at
  :1733-1734, so the #495 rationale at :1535-1538 is statically false: a flag-only push refusal would block legitimate
  CDB collection, not recreate the DATA-IN free.
* wdc:F12 CHANGELOG.md:27774-27777 (MODE SELECT cannot reach logical_block_size through dev_wdc.c).
* gdrom:F2 dev_dreamcast_gdrom.c:1493-1499 -- AMENDED (Astra): "requests d->data_len; the completed transfer size is
  not established" (memory_rw truncates at a device boundary, memory_rw.c:495-524, :626).
* gdrom:F3 :418-424 (sum == all-ones is necessary, not sufficient -- {1,1,5}).
* gdrom:F4 :1329-1333 (an alignment guard would be redundant, not unreachable).
* gdrom:F5 :1033-1040 (all four de-fatalised predicates carry rows; `accept w8` carries the width one).
* gdrom:F6 CHANGELOG.md:16753 -- AMENDED (Astra): "every release restores the pointer/length invariant before
  returning; transient disagreement remains representable during allocation and release" (:664-665, :654-658).
* gdrom:F7 :258-260 (ELEVEN writers of d->warned; three read-settable).
* gdrom:F8 :714 (65,127, not 65,527).
* sh4:F2 dev_sh4.c:454-457 (OVF is guest-writable at :2381; what the device never does is GENERATE a compare/overflow).
* sh4:F3 :1600-1605 (drop RTCNT from the width-served list; it has no case).
* sh4:F4 :1691-1696 -- AMENDED (Astra): "reports when a call contributes any previously unreported bit, permitting at
  most 32 reporting calls per class/instance" (:1711-1714 return one Boolean; :459-462).
* sh4:F5 CHANGELOG.md:24626-24627 (reuse would be EQUIVALENT, not a collision).
* sh4:F6 -- OVERTURNED (Astra): not UNSETTLED but L4.  CHANGELOG.md:18814-18815 says the detector polls TCNT; the
  committed sh_pclock_probe.py plants TCR stores and reads TCR (:187-193, :240, :370-379).  Replacement: "The committed
  detector reads TCR, comparing refused 0 with accepted 1; it does not poll TCNT."  And OUTSTANDING_BUGS.md:8835-8837
  says the numerical citation was corrected while CHANGELOG.md:18824 keeps it.  (Whether a separate experiment
  measured 0x20 remains unestablished.)

GAP
* `sh4chcrdualdiag` LOW -- AMENDED (Astra): R7/L0 count only VAL_RE (the probe's helpers are `diags()`/`any_diag()`;
  X3/X4 also count only IE_RE), so a `return` -> `break` in the RS switch escapes them.

UNSETTLED: none remain (both became L4).

Fable's own additions (first-hand review): an UNLATCHED `fatal()` in DEVICE_ACCESS(sh4)'s default arm
(dev_sh4.c:2824-2835) is a guest-drivable flood (floodclass, LOW -- check it is not already implied by a floodclass row).

---

## Batch 2a -- cpu_arm_instr.c, cpu_ppc_instr.c (30 findings).
## Fable: 15 NEW, 5 FILED, 10 L4 (claude-fable-5-1; one refusal turn, no fallback -- adjudication/fable_batch2a.md).
## Astra: 6 of 30 wrong, 7 amended (codex_astraconfirm_batch2a.txt).  All six "wrong" are ONE correction: a defect
## already recorded in OUTSTANDING_BUGS.md prose WITHOUT a short id is FILED, not NEW -- name the existing entry.

NEW
* `armendianexit` HIGH -- a CP15 c1 write that toggles the B bit reaches `fatal()` + `exit(1)` (cpu_arm_coproc.c:157-178;
  #378's comment calls the exit load-bearing).  Option set: decline-and-announce vs implement; a bare deletion breaks
  the translate-time byte-order premise.
* `ppcllscrcexit` HIGH -- `lwarx`/`ldarx` with Rc=1, or `stwcx.`/`stdcx.` with Rc=0, reach `fatal()` + `exit(1)` in
  `X(llsc)` (cpu_ppc_instr.c:2305-2308, :2331-2334); the decoder keys on xo alone (:4614, :4866-4871).  #216
  de-fatalised the two memory-fault exits in the same function and left these.
* `armmemcpyoverlap` MED -- the `netbsd_memcpy` fold publishes pre-store source words and calls `memcpy` on
  overlapping ranges (cpu_arm_instr.c:2309-2318).  AMENDED (Astra): state the overlap in EFFECTIVE WORD-ALIGNED
  addresses -- genuine transfers align (generate_arm_multi.c:117), so a destination 1-3 bytes above an aligned source
  has the same effective base.
* `armcachecleanload` MED -- the `netbsd_cacheclean` fold never performs the `ldr`: r2 stays stale and a walk over an
  unmapped page cannot fault (cpu_arm_instr.c:2355-2416; arm_flags_probe.py:1619 pins the stale seed).
* `ppcllscsrr0` MED -- `X(llsc)` never synchronizes `cpu->pc` before `memory_rw`, so a DSI in `lwarx`/`stwcx.` records a
  stale SRR0.  By reading; the settling probe must free-run (single-step keeps pc exact).
* `ppcnanpayload` MED -- NaN operands lose their payload through `ieee_interpret`/`ieee_store`; fnmadd/fnmsub also flip
  the sign.  AMENDED (Astra): scope is add/subtract/multiply/divide and the fused handlers -- `fsel` copies raw bits
  and preserves the payload (cpu_ppc_instr.c:1245-1246).
* `ppcfpstatus` MED -- AMENDED (Astra): "arithmetic and conversion handlers do not derive numerical rounding status"
  (FR/FI/XX/OX/UX); the explicit FPSCR control handlers CAN set those bits (cpu_ppc_instr.c:1029-1030, :1103-1116).
* `armuserpageshift` LOW, `ppccrlogicshift` LOW -- signed `1 << 31` forms (language-level; class row `shiftubcensus`).

FILED -- an existing entry, confirmed at HEAD
* `excvecrecurse` -- SEVERITY RAISED to HIGH (Astra): cpu_arm.c:733 -> quick_pc_to_pointers.h:16 ->
  cpu_dyntrans.c:679 -> memory_arm.c:269 re-enters exception handling without a bound; host stack exhaustion ends the
  process.  OUTSTANDING_BUGS.md:21950 says MED.  (Fable accepted the queue's MED without re-tracing the recursion,
  and said so.)
* `ppccr0modewidth` -- SEVERITY RAISED to MED (Astra): bareppc supplies a PPC970 (machine_test.c:434-450) whose model
  width is 64 with SF clear (cpu.c:71, cpu_ppc.c:99-103), so the LOW rationale at OUTSTANDING_BUGS.md:19199-19201 fails.
* `armbfiwidth`, `armbdtcombined`, `OB-24`.

FILED BY PROSE, NO ID -- Astra overturned Fable's NEW; assign the id to the EXISTING entry, open no new row
* OUTSTANDING_BUGS.md:1256-1264 (`armbdt`'s alignment-enforcement residual) -- proposed id `armalignexc`, MED.  Drop
  `:5660` as corroboration: that passage is PPC `lwarx`.
* :1620-1622 (the fused forms ignore FPSCR[RN]) -- `ppcfmarn`, MED.
* :1671-1675 (fadds/fsubs/fmuls/fdivs never narrow) -- `ppcsinglealias`, MED.
* :1685-1687 (FPRF class / exception enables) -- `ppcfprfclass`, MED ("result classification never updates C"; explicit
  FPSCR writes can), and `ppcveinhibit`, MED (frsp overwrites FRT and FPRF; fctiw/fctiwz overwrite FRT despite VE).
* :1971-1973 (#300's accepted-nearest bands) -- ONE id for it, `optinyband` (batch 2b names it); Fable's `mulrmband`
  is the same entry.  AMENDED (Astra): remove `fadd` from its scope -- the addition helper has no OPTINY cutoff
  (float_emul.c:1054-1087).

L4 (replacement texts in fable_batch2a.md unless amended here)
* cpuarminstr:F9 cpu_arm_instr.c:3345-3349 + CHANGELOG.md:32364-32367 (the fold is reachable on the first pass when no
  breakpoint is set).
* cpuarminstr:F10 CHANGELOG.md:31075-31079 -- AMENDED (Astra): qualify "a store sets host_store" to SUCCESSFUL ordinary
  accesses ELIGIBLE FOR FULL-PAGE dyntrans caching (memory_rw.c:738-745 suppresses caching for MEMORY_NOT_FULL_PAGE,
  which memory_arm.c:202-235 produces for 1 KiB pages and mixed permissions).
* cpuarminstr:F11 cpu_arm_instr.c:2878-2886 (a marker-free instrument exists and #358 measured it).
* cpuarminstr:F12 cpu_arm_instr.c:2730-2735 -- AMENDED (Astra): "at most one folded iteration; a warm iteration adds 2
  to the incoming count" -- :2742-2745 can delegate with zero folded iterations, and :2758 adds 2 even when the
  incoming count already exceeds the limit, so the total excess is not bounded by 2.
* cpuarminstr:F13 cpu_arm_instr.c:1495-1496 (SWP: from ARMv6 an alignment exception, not "true unaligned access").
* cpuppcinstr:F13 cpu_ppc_instr.c:3455-3458 (the stfs splice comment; the +/-Inf POLICY is NOT reopened).
* cpuppcinstr:F14 cpu_ppc_instr.c:5338-5344 + CHANGELOG.md:33049-33050 ("three of the eight", not four).
* cpuppcinstr:F15 cpu_ppc_instr.c:1982-1984 + CHANGELOG.md:32531-32534 (stale two hours after it was written: #336).
* cpuppcinstr:F16 cpu_ppc_instr.c:2492-2493 (rldimi/rlwimi were fixed by #527).
* cpuppcinstr:F17 cpu_ppc_instr.c:82-87 (the predicate's stated reason describes the pre-#335 shape).

Fable's own additions: `armcp15c1fallthrough` (proposed MED, CONTINGENT on which ARM models the machines instantiate):
a CP15 c1 write with opcode2 not in {0,1} prints and then FALLS THROUGH into the control-register write
(cpu_arm_coproc.c:124-135; upstream code).  Unmeasured.

---

## Batch 2b -- float_emul.c, cpu_sh_instr.c, cpu_mips_coproc.c (34 findings).
## Fable: 10 NEW, 5 FILED, 12 L4, 3 GAP, 4 DUPLICATE (claude-fable-5-1, clean -- adjudication/fable_batch2b.md).
## Astra: 0 of 34 wrong, 5 amended (codex_astraconfirm_batch2b.txt).

NEW
* `oddoptinyband` MED -- the OPTINY guard copied into `ieee_div_round_to_odd()` suppresses the odd-force for normal
  operands below 2^-969 and breaks NEAREST single rounding on m88k `fdiv.sdd` (float_emul.c:999; the #308 witness
  scaled by 2^-1000).
* `addovftie` MED -- `ieee_add_round_rm()` returns the nearest sum when 2Sum's intermediate overflows; the gate row
  `D add ovf-tie RZ` (diff_ieee_store.c:898-899) PINS THE DEVIATION, so a fix is an oracle correction (re-pin first).
* `shnestedbranch` MED -- a delayed branch in a delay slot is re-run as a plain branch; the manual makes it a Slot
  Illegal Instruction exception, EXPEVT H'1A0 (sh4_programming.txt:4541-4549).  19 sites; their "architecturally
  unpredictable" comments are false and are corrected with the fix.
* `shslotres` MED -- `X(reserved)` raises H'180 in a delay slot where H'FFFD owes H'1A0 (cpu_sh_instr.c:242-246).
  Rider (Fable): the upstream `RES_INST_IF_NOT_MD` macro has the same omission.
* `mipscmpdenorm` MED -- the #246 denormal-operand trap fires for C.cond.fmt on R4000; the manual exempts Compare
  (cpu_mips_coproc.c:1293; mips_r4000.txt:1627).
* `mipstinyenable` MED -- the tiny-result guard tests FS alone; the R4000 traps whenever Underflow OR Inexact is
  enabled (cpu_mips_coproc.c:1173; mips_r4000.txt:1623).
* `mipstinyhostzero` MED -- a D result the host already rounded to +/-0 escapes the tiny trap (cpu_mips_coproc.c:1174).
* `shdnoperand` MED (Fable's own) -- with FPSCR.DN=1, the reset default, a denormalized OPERAND is treated as zero on
  silicon (sh4_programming.txt:999); the fork decodes it to its true value and `sh_dn()` touches results only.
* `shoddprfield` -- SEVERITY DISPUTED, both positions kept.  PR=1 arithmetic and compare handlers accept an odd
  register field and read or write `fr[n+1]`; field 15 lands on `xf[0]` (cpu_sh_instr.c:3376-3387; cpu_sh.h:104-105).
  Fable: LOW -- "an out-of-ARRAY index that stays inside the cpu struct; no host-memory hazard ... an odd field under
  PR=1 is a reserved combination whose hardware behaviour is 'not guaranteed'".  Astra: HIGH -- "Remaining inside the
  containing structure does not keep the access inside that array", i.e. the severity rule's outside-a-buffer clause
  by its letter.  AMENDED (Astra, undisputed): FCNVSD/FCNVDS are NOT affected -- their decoder masks require even
  fields (cpu_sh_instr.c:5061, :5065).  This is a RULE QUESTION (does an intra-struct out-of-array access meet the
  HIGH clause?) and goes to the panel and the flagship seat; until ruled, the row is filed with both grades.
  Absorbs the id-less OUTSTANDING_BUGS.md:1778 (the ftrc member).

CROSS-BATCH DUPLICATES (the main loop's reading, 2026-09-28 -- neither seat had both batches in view)
* 2b `divinfnan` IS batch 1b's `divbyinfnan` (both: float_emul.c:895-902 and :987-1009).  ONE row, `divbyinfnan`, MED,
  carrying 2b's additions: the +/-2^-1074 shape, and AMENDED (Astra) -- the round-to-odd callers are m88k
  `fdiv.ssd/sds/sdd` (`fdiv.sss` is plain division, cpu_m88k_instr.c:1367), and the erroneous residual path needs
  |dividend| >= 2^-969.  Wrong-record riders: float_emul.c:802-803 and CHANGELOG.md:22350-22352.
* 2b `sddexprange` overlaps batch 1b's `m88ksddovf` (the overflow side is the same defect).  ONE row, `m88ksddovf`,
  MED, widened by 2b's UNDERFLOW side.  AMENDED (Astra) boundaries: overflow begins at 2^1024 - 2^970; a nonzero
  product rounds to zero for |exact| <= 2^-1075 (between 2^-1075 and 2^-1074 it rounds to the minimum subnormal and
  can still give the correct directed single result).

FILED (confirmed at HEAD): `sh4sqexpevt`, `sh4sqwrite`; `mipstiny` -- RE-GRADED from "unresolved disagreement" to a
defect, MED: the owed manual sentence is mips_r4000.txt:1623 ("computed as though the exponent range were unbounded"),
which is not the destination's subnormal grid that `fpu_subst_tiny()` classifies on.
FILED BY PROSE, NO ID: OUTSTANDING_BUGS.md:1971-1973 -> `optinyband` (see batch 2a); :1650-1655 -> `mipstinyprerm`,
with its boundary corrected in place ("[2^-126 - 2^-151, 2^-126) under nearest", mode-dependent).

L4 (replacement texts in fable_batch2b.md unless amended here)
* floatemul:F6 CHANGELOG.md:20471 (W's upper bound has no slack).
* floatemul:F7 float_emul.c:217-225 and floatemul:F8 :652-654 (DN: the result side is modelled since #334; DN=0
  DELIVERS the denormalized result; the FPU error is for a denormalized INPUT).
* floatemul:F9 float_emul.c:789 and :1024-1026 (2^-1018 -> 2^-969, IEEE_DIR_OPTINY).
* floatemul:F10 float_emul.c:1224-1228 (the subnormal-grid argument, not the 2^-298 floor).
* cpushinstr:F8 cpu_sh_instr.c:119-125 (double arithmetic is corrected since #300).
* cpushinstr:F9 cpu_sh_instr.c:150-151, :159-164 and CHANGELOG.md:32605-32606 (the DN=0 claim; `shsweep` item 4).
* cpushinstr:F10 cpu_sh_instr.c:238-240 (SLEEP does not halt).
* cpushinstr:F11 cpu_sh_instr.c:3726-3733 (masking cannot drop bits [9:5]).
* cpumipscoproc:F8 cpu_mips_coproc.c:716-718 + CHANGELOG.md:20029 (the reg-3 write IS stored).
* cpumipscoproc:F9 cpu_mips_coproc.c:1185-1191 -- AMENDED (Astra): RN/RP/RM pre-round finite values to an integral;
  RZ leaves truncation to the integer cast AFTER the range guards (float_emul.c:314, :465, :481-491).
* cpumipscoproc:F10 cpu_mips_coproc.c:1302-1303 (double goes through ieee_add_round_rm since #300).

GAP
* `badfmtlatchrow` LOW -- #279's two one-shot latches have no committed row that fires them.
* `ftrvfourstores` LOW -- only the fr0 store of `ftrv`'s four is observed (sh_rounding_probe.py:94-98).
* `mipscvtsdlive` LOW -- AMENDED (Astra): the gap is the `cvt.s.d` RN/RZ CONTRAST specifically; the nearest-mode
  single-store wiring IS observed live (mips_rounding_probe.py:63, the `cvt.s.l` row).  And mips_subnorm_probe.py is
  #303, not #331/#332.

DUPLICATE (ruled once under floatemul): cpushinstr:F2, cpushinstr:F7, cpumipscoproc:F1, cpumipscoproc:F7.

Fable's design note (UNMEASURED, a hypothesis for the fix round): the OPTINY guards may never be load-bearing for
correctness -- a residual below the subnormal quantum can only read as a false zero, which returns what the guard
returns -- so the true accepted-nearest set would be "the residual rounds to zero", a strict subset of the band.

---

## CORRECTIONS 2026-09-28 (from the codex work pack; the Fable seat has not ruled on these -- recorded, not final)

* Batch 2a, `armendianexit` -- NOT NEW: the codex seat's panel answer (`codexpack_20260928/hpanel_arm/`) found it
  recorded by prose at OUTSTANDING_BUGS.md:18721-18722 ("SEVEN sibling guest-reachable host kills ... CP15 endian"),
  together with the other six live exits of `cpu_arm_coproc.c` (62, 264, 322, 331, 417, 528).  Disposition becomes
  FILED-BY-PROSE, id `armendianexit` assigned to that entry; the six siblings are one entry, one id owed.
* Batch 2a, `excvecrecurse` HIGH -- corroborated by the same answer (the recursion is real and unbounded; PowerPC and
  M88K share the shape, SH does not).
* NEW CANDIDATE (hpanel_arm, standing license): the SPSR-WRITE handler's `default:` stops the CPU in USR32/SYS32 while
  the SPSR-read sibling returns zero (cpu_arm_instr.c:856, :892, :932; decoder :4294) -- the same absent-SPSR class as
  the user-mode `LDM ^` halt.  Unruled.
* Batch 2b, `shoddprfield`: the codex seat grades HIGH by the rule's letter (intra-struct; not a host escape) and names
  FLOAT (cpu_sh_instr.c:2925-2929, :5027-5030) as a sibling with the same odd-field pattern.  The RULE QUESTION stands.
* Batch 1a, `gdromdmareentr`: re-entry is data-dependent (bytes 0..7 of the staged data fold into the trigger value); a
  diskless TOC staging sequence reaches it.  Separate finding: the DMA arm ignores `memory_rw`'s result and announces
  completion.  Unruled.

---

## Batch 2c -- bundle_cpus1, bundle_cpus2, bundle_machines (27 findings).
## Fable: 5 NEW, 10 FILED (3 by prose), 7 L4, 1 GAP, 4 DUPLICATE (claude-fable-5-1, first-hand, 2026-09-30; ruled with
## the codex draft in view and changed it in 5 places -- adjudication/fable_batch2c.md).  Astra: 0 of 27 wrong,
## 4 amended (codex_astraconfirm_batch2c.txt).  Grok's interim check: adjudication/grok_20260930/grok_check2c.txt.

NEW
* `i960disasmspan` HIGH (by the rule's letter; bounded consequence stated) -- i960: disassembling a long two-word MEMB
  instruction reads `ib[4..7]` of a four-byte local buffer, on the `bad:` path every instruction word takes
  (cpu_i960_instr.c:165, :198-201; cpu_i960.c:451-464; cpu_dyntrans.c:2011-2012) -- a four-byte over-read of the
  emulator's own stack feeding a diagnostic, after which the CPU stops.  Same shape as `shoddprfield`'s open rule
  question; Astra kept the grade.
* `ppctblcarry` MED -- PPC: an `mftb` polled at TBL == 0xffffffff pushes the 64-bit TBL cell to 2^32; the #141 batch
  update truncates it and the carry into TBU is lost (cpu_ppc_instr.c:2789-2795; cpu_dyntrans.c:455-458;
  ppc_pem_32and64_2005.txt:1716).  Rare, deterministic; keep TBL 32-bit in `X(mftb)`.
* `armmrcr15flags` MED -- i80321 CP6: an MRC with Rd=R15 stores into `r[15]` and leaves NZCV untouched; the ARM ARM
  routes bits 31:28 to the flags (cpu_arm_coproc.c:310-311; ddi0100i.txt:9335-9341).  #526's survival left the R15
  semantics unsupplied; fix site is the dispatcher (cpu_arm.c:2653-2655).
* `mipssuperseg` MED -- MIPS R4000+: in Supervisor mode (KSU=01) sseg/xsseg/csseg are refused with AdEL/AdES where the
  manual makes them mapped supervisor spaces (memory_mips_v2p.c:166-184, :231-247; mips_r4000.txt:661, :665, :1001).
  AMENDED (Astra): qualify both the finding and the L4 comment -- "In Supervisor mode with EXL=ERL=0, translation
  rejects sseg with SX=0 and xsseg/csseg with SX=1; addresses within the selected user-space limit still reach the
  TLB".  L4 rider: the #238 comment at :178-182 says "the normal (kernel-style) TLB walk"; the walk reached is the
  user-style predicate (only KSU_KERNEL translates above useg) -- replacement text in fable_batch2c.md.
* `mipssamepcstore` MED (contrived; last of the MEDs) -- swl/swr/sdl/sdr: the #227 load-to-store ExcCode conversion is
  gated on `cpu->pc != oldpc`, false when the faulting store is the first instruction at its own exception vector
  (cpu_mips_instr_unaligned.c:83-110; cpu_mips.c:2190-2203).  AMENDED (Astra): drop "vector, BadVAddr and EPC are all
  correct" -- the aligned pre-read can also discard the effective address's low bits from BadVAddr.

FILED (existing id, confirmed at HEAD): `OB-24` (x2: cpu_ppc_instr_loadstore.c:116/:124 and cpu_i960.c:462/:464 --
Astra's "no matching ID" corrected), `sh4sqwrite`, `sh4sqexpevt` (RIDER: fold the AT=0 half in -- the entry never
mentions it; only the archived clause at OUTSTANDING_BUGS.md:1942-1944 does), `alphaifetchkill`, `armdesc3kill`
(SEVERITY RAISED MED -> HIGH: any guest using fine page tables ends the process at its first translation),
`alphafaultclaim` (verified here; four replacement texts in fable_batch2c.md).
FILED BY PROSE, NO ID -- assign the id to the existing entry: OUTSTANDING_BUGS.md:1946-1947 -> `sh4utlbmultihit` MED
(the first-match walker serves every translated access, not only the SQ PREF -- the draft's `shsqmultihit` scoped it
wrong); :1645-1649 -> `alphatinyzero` MED (21066_66a_hrm.txt:1889-1891: unqualified T ops deliver exact +0 "whether or
not the correct result would have been negative zero"; the entry's "no Alpha rig" premise is stale since #505-#508);
:18721-18722 -> `xscalecp6exits` HIGH (the three CP6 sites 322/331/417; the other three of the seven -- :62 CP15 rd==PC,
:264 CP15 PID, :528 CP14 unknown -- keep their owed id).

DUPLICATE of earlier rows: bundle_cpus1:F1 -> `ppcbatppkill` (1b); F3 -> `armuserpageshift` (2a; the draft's
"filed as armbfxwidth32" names a SHIPPED round, not a live id); F4 -> `ppcbatstale` (1b) -- AMENDED (Astra):
`mtsr`/`mtsrin` and the `tlb*` handlers invalidate mappings, BAT/HID0 writes use generic `mtspr` without (evidence
corrected, ruling unchanged); bundle_cpus2:F4 -> `armendianexit` (2a, FILED-BY-PROSE at :18721-18722, ratified here).

L4 (replacement texts in fable_batch2c.md unless amended here)
* cpus1:F10 memory_sh.c:87-93 (the URC comment) -- AMENDED (Astra): replace the "only runs on a COLD translation"
  passage with "Ordinary accesses served by dyntrans host-page mappings bypass this function and its URC update; SQ
  PREF invokes this walker directly on each translated transfer; URC therefore does not consistently track hardware
  UTLB accesses" (the ITLB-first placement point stands).
* cpus1:F11 cpu_alpha_instr.c:515-519 + CHANGELOG.md:32603 ("no Alpha rig" -- overtaken by #505-#508) + the
  OUTSTANDING_BUGS.md:1647-1649 rider.
* cpus2:F11 cpu_arm_coproc.c:169-174 (`invalidate_translation_caches(INVALIDATE_ALL)` drops address mappings only; the
  code translations need `arm_invalidate_code_translation` for handlers to be re-picked).
* machines:F1 CHANGELOG.md:25101-25103 (the two mutants are identical to EACH OTHER, not to the fix).
* machines:F2 CHANGELOG.md:19330-19335 + sh_intprio_probe.py:262-268 (overtaken by #458/#459 one day later; dated
  bracket, not a rewrite).
* machines:F3 machine_arc.c:131-132 (NetBSD/arc ran on SERIAL console under PICA per the tree's own HISTORY:1055-1061;
  the draft's DOUBTFUL overturned -- HISTORY is a committed file).
* machines:F4 machine_sgi.c:111-112 (present tense false since #446).

GAP: `testmipshighramrow` LOW -- nothing at HEAD observes testmips's >256 MB mirror/high mapping (#120's
"regression-gated" has no carrier; every `-M` under regress/ is 32 or 64).

Fable's own additions: sh4sqexpevt's cross-reference drift (:7955 cites the archived clause as ":441-443"; it is
:1940-1947); cpus1:F5's `mftb` also hands 0x1_00000000 to the GPR after the rollover (same defect, mask the cell);
cpus2:F7's stray `r[15]` store's visibility is unestablished (one probe row in the fix round).

---

## Batch 2d -- bundle_devices1..5 (28 findings).
## Fable: 15 NEW, 3 FILED, 6 L4, 4 GAP (claude-fable-5-1, first-hand, 2026-09-30; read the codex draft AFTER its own
## reading and changed 3 of its dispositions -- adjudication/fable_batch2d.md).  Astra: 0 of 28 wrong, 6 amended
## (codex_astraconfirm_batch2d.txt).  Grok's interim check: adjudication/grok_20260930/grok_check2d.txt.

NEW
* `mboutcapacity` HIGH -- MB89352: the WRITE path re-sizes `data_out_len` without reallocating, and DREG writes bound
  on that length -- a store through a NULL `data_out` after the CDB returns 2, or past a 16-byte block allocated by an
  earlier small XFR DATAOUT (dev_mb89352.c:225-246, :268-280, :476-495; diskimage_scsicmd.c:888-892).
* `vgadirtyarm` HIGH (unmeasured; precondition stated) -- VGA: an UNTRACKED charcells write below the CRTC start leaves
  a ~-1.7e9 dirty-row origin unclipped and the graphics redraw walks it for hours (dev_vga.c:738-764, :545-558,
  :352-356).  Untracked only through `MEMORY_NOT_FULL_PAGE`, whose live producer is ARM subpage/tiny-page translation
  (memory_arm.c:235); the one ARM machine with a VGA is cats.  AMENDED (Astra): graphics widths are 160/320/640, not
  80 (80 is text mode) -- wording only.
* `dectxzero` HIGH -- DEC21143: an empty continuation of an empty first TX segment calls `realloc(p, 0)`, which glibc
  answers with NULL, and CHECK_ALLOCATION ends the process (dev_dec21143.c:772-802; misc.h:181-193).
* `mbcdbincomplete` -- RAISED LOW -> MED (Astra): the MB89352 dispatches a CDB whose uncollected bytes are uninitialised
  heap (dev_mb89352.c:500-501, :409-429, :259-269; the #113 check tests the ALLOCATED length); unsupplied parameters
  reach disk operations (diskimage_scsicmd.c:853, :868).  Fable's LOW rationale (the opcode must come from residue) was
  the wrong test.
* `rtcpendovf` -- RAISED LOW -> MED (Astra): dev_rtc's `pending_interrupts` increments without saturation and wraps
  negative under an unacknowledged high-rate timer; positivity controls delivery and an ACK cannot decrement a negative
  count -- documented pending-interrupt behaviour compromised (dev_rtc.c:54-82, :158; doc/experiments.html:512).
* `gssiglblid` MED -- ps2_gs: `N_GS_REGS 0x108` excludes the file's own highest register, so SIGLBLID (0x108) is refused
  (writes dropped, reads 0) by #99's guard (dev_ps2_gs.c:46, :77-81, :94-105).  No GS manual on disk; ruled on the
  file's own table (the draft's DOUBTFUL overturned).
* `mpstartupsp` MED -- dev_mp STARTUPCPU sets the startup stack pointer for MIPS and PPC only; every other test machine
  starts the CPU with its old SP against `doc/experiments.html:279-282` (dev_mp.c:98-115, :147-151).  Broadened from
  the codex's ARM to all non-MIPS/PPC test machines.
* `gberesizezero` LOW -- GBE keeps a rejected VCMAP/HCMAP dimension and reads it back through negative shifts
  (dev_sgi_gbe.c:542-552, :495, :536).  AMENDED (Astra): execution still reaches the conversion and the framebuffer
  call; a rejected resize preserves the whole old framebuffer -- the bounds explanation corrected, the grade kept.
* `vgacursoronly` LOW -- headless VGA console: the OB-16 guard returns before the cursor-only tick can reposition the
  terminal cursor (dev_vga.c:581-584, :268-269).
* `pxdmatail` LOW, `gifputcharovf` LOW (residual of the RESOLVED OB-28 -- a closed row is not a filing), `pxfilladd` LOW,
  `lunaintshift` LOW, `kn02banameshift` LOW, `macesignedshift` LOW (operator wiring needed for line 31) -- the three
  signed-shift rows are one class; a records round may file them as children of `shiftubcensus`.

FILED (confirmed at HEAD): `fbctrlcmdkill` (HIGH), `rtclen`, `sgigbeconvover`.

L4 (replacement texts in fable_batch2d.md unless amended here)
* devices1:F6 dev_mb89352.c:438 (the #295 "declares it FULL / DEFERRED on purpose" sentences are historical since
  #338; the #263 history is kept).
* devices1:F7 makeautodev.sh:72-74 (the anchor is the load-bearing half; dropping `set -f` is MEASURED to change
  nothing -- diff_autodev_gen.sh mutant 3).
* devices2:F2 CHANGELOG.md:20766-20768 (the pckbc room guard bounds the drain only through queue room) -- AMENDED
  (Astra): restrict to converters 2 and 3 -- converter 1 unconditionally queues a shift make/release code
  (dev_pckbc.c:227-230), so its drain consumes room.
* devices2:F3 dev_dreamcast_asic.c:182-191 (the fourth-word header hazard is closed by #468/#469's compile-time
  assertion; `asiceventaddr` now names the BITMASK sibling).
* devices2:F4 CHANGELOG.md:28088-28091 (the rs5c313 read-side mask is NOT dead code: a pre-1900 host clock yields
  0xfa in YEAR1).
* devices4:F3 CHANGELOG.md:21714-21716 (the OB-14 over-read was the CONVERTED copy, 2976 bytes into a 1536-byte
  `fb_buf`, not the 992-byte line read).

GAP
* `autodevregorder` LOW -- diff_autodev_gen.sh's ordered rows compare PROTOTYPE lines; the registration loops are a
  separate scrape no row observes.
* `lunad3diag` LOW -- no row observes luna_intmask_probe.py's D3 diagnostic (its "kills a narrowed guard" sentence is
  ambiguous, not false).
* `fdcdiagrows` LOW -- CHANGELOG #20522's "asserted rather than assumed" fdc measurement has no committed carrier.
* `mk48aliasrow` LOW -- mk48_nvram_probe.py's nine round-trip rows each run one offset per session, so the DISTINCT
  bytes cannot see a mutant folding offsets onto one cell; the kill table carried no folding mutant.  L4 rider on
  CHANGELOG.md:4736-4737 and the probe comment at :286-288 -- AMENDED (Astra): "another row's scratch" is the wrong
  rationale (each row is a fresh process) and the replacement must cover the whole comment at :286-288.

Fable's own additions: mboutcapacity's cheaper witness is the NULL-`data_out` route after the CDB returns 2; the `res`
discarded at dev_mb89352.c:271-272 is the `mb89352halt` class (name it in that row, do not re-file); gberesizezero
covers VT_VPIX_EN (:536) and the HCMAP mirror (:546) with one row; the fix for gssiglblid is `N_GS_REGS 0x109`.

---

## Batch 2e -- devasc, diskimage, diskimagescsicmd, bundle_file (29 findings).
## Fable: 10 NEW, 2 FILED, 8 L4, 5 GAP, 4 DUPLICATE (claude-fable-5-1, first-hand, 2026-09-30; changed 3 of the codex
## draft's dispositions -- adjudication/fable_batch2e.md).  Astra: 0 of 29 wrong, 4 amended
## (codex_astraconfirm_batch2e.txt).

NEW
* `symdemanglebound` HIGH -- the C++ demangler copies a length-prefixed name component without testing source
  termination, over-reading a NUL-terminated loader string by up to MAXLEN bytes (symbol_demangle.c:79-92; all four
  loaders feed it).  Input: a file the operator names, or the OS loader the boot block extracts from a disk image --
  the fork's src/file threat model (#14-#66).
* `ecoffoffsetspan` HIGH -- ECOFF table-offset guards admit a sign-extended negative offset (file.c:85-89), seek
  unchecked and `exit(1)` on the resulting short read, or read the WRONG bytes (file_ecoff.c:322-337, :414-444);
  defeats the #59/#62 skip-a-bad-table policy.
* `ascwidecount` HIGH (DEC/pmax only; on PICA the jazz callback's `(int32_t)len` guard makes it a survivable zero move)
  -- a 32-bit ASC transfer-count write during a continued DATA_OUT DMA yields a negative `len2` that both span guards
  pass, and the DEC `memcpy` takes it as size_t (dev_asc.c:577-583, :610-622, :662-665, :1155).
* `ascoutresid` MED -- a DATA_OUT DMA clamped to the target's remaining length still reports residual 0 with Terminal
  Count set (dev_asc.c:755-761; #281 fixed the DATA_IN twin).  The `:707` decision is a MEASURED choice (#283) and
  stays; the repair is the report only.
* `asccmddma` MED -- COMMAND-phase DMA reads the CDB from the private DEC buffer even when an external DMA controller is
  configured (PICA): the CDB is `len` zero bytes, opcode 0x00 runs as TEST UNIT READY when the #113 length check passes
  (dev_asc.c:984-1000).
* `ascpiozero` MED -- PIO DATA_IN pushes zeros from the never-populated `incoming_data` (dev_asc.c:367-392; the stub
  REVIEW_FINDINGS.md:965 acknowledges; assign the id there).  AMENDED (Astra): the PIO DATA_OUT sibling (:573-574) is
  NOT "inert": `all_done` stays 1, `:856-860` advances to STATUS and `:1284-1287` reports success -- premature
  successful completion, MED, in the same row.
* `writeflusherr` MED -- under `-f`, a guest WRITE reports GOOD after `fflush()`/`fsync()` fail (diskimage.c:1207-1212,
  :1265-1268, :1315-1318 discard the results; `diskimage_sync()` checks both).
* `drecalccap` MED -- READ CAPACITY, READ SUBCHANNEL/CD CAPACITY and READ TRACKINFO (diskimage_scsicmd.c:489, :1139,
  :1222) re-run `diskimage_recalc_size()` on a `d:`-retyped floppy and replace its exact geometry with 16/63: 2,880
  blocks become 3,024 phantom-tailed (diskimage.c:232-236, :268-272, :2066-2067).  Fix the helper, not one caller.
* `stalelbsbound` MED -- MODE SELECT changes `logical_block_size` without refreshing `nr_of_logical_blocks`, so the read
  bound shrinks until a capacity command recalculates (diskimage_scsicmd.c:1319-1324; diskimage.c:1592-1593).
* `cuebomparse` -- RAISED LOW -> MED (Astra): the CUE sniffer skips a UTF-8 BOM the parser keeps in its first keyword,
  so a BOM-prefixed FILE line is dropped and the image falls back to flat -- the guest-visible BIN mapping documented at
  diskimage.c:1999-2004 breaks (:623-625, :685-715, :767-772, :1054-1058).

FILED (confirmed at HEAD): `ovsync` (SYNCHRONIZE CACHE(16) undefined); `lbsmask` -- RAISED LOW -> MED (Astra): non-power-
of-two block sizes are accepted (diskimage_scsicmd.c:1319-1324), the mask computes the wrong capacity (diskimage.c:305-
307) and reads are refused on it (:1592-1599); RIDER: READ TRACKINFO (:1224-1226) carries the same mask.  (Fable had
kept the row's LOW "until its owner re-grades it"; the confirmer re-graded it.)

DUPLICATE: diskimagescsicmd:F1 -> batch 2d's `mboutcapacity` (a SECOND disk-layer re-sizing site, :1283-1287, the
#285 unconditional `data_out_len = 12` -- add it as a rider; the ASC is not exposed, `dev_asc_newxfer()` frees the
transfer on every SELECT); diskimagescsicmd:F2 -> `drecalccap`; diskimagescsicmd:F3 -> batch 1b's `scsicapnosense`
(the draft's "DUPLICATE-OF-ROW" named a row that does not exist at HEAD); diskimagescsicmd:F5 -> `lbsmask`.

L4 (replacement texts in fable_batch2e.md unless amended here)
* devasc:F5 dev_asc.c:835-841 + CHANGELOG.md:20491 ("this arm sets no interrupt" -- it reaches the common epilogue,
  which forces PHASE_STATUS and raises NCRSTAT_INT | NCRINTR_BS; the latch rationale survives on the corrected basis).
* devasc:F6 dev_asc.c:1495-1498 ("shown at -v" -- it takes `-v -v` during the run, since main.c drops one level after
  startup) -- AMENDED (Astra): the alternative is `breakpoint subsystem device debug`, not "`break device`"
  (debugger_cmds.c:49-53, :88-90, :270-273).
* diskimage:F6 diskimage.c:1643-1645 (an in-bounds short result is also an overlay write `fwrite_helper` declined).
* diskimage:F7 diskimage.c:1498-1500 (the memset is a no-op on `len` and a whole-buffer zero-fill on 0; keep the measured
  "NOT dead" sentences).
* diskimage:F8 CHANGELOG.md:25608-25610 (the `diskimage_sync` self-mutant leaves the fsync COUNT intact while the fflush
  count drops -- the .why file says so).
* diskimagescsicmd:F6 diskimage_scsicmd.c:507-510 (an empty disk reports ONE block: READ CAPACITY(10) has no encoding
  for none; CHANGELOG #412 already records the ambiguity).
* diskimagescsicmd:F7 diskimage_scsicmd.c:203-206 (NO SENSE + FILEMARK is a defined pairing the tape READ returns).
* diskimagescsicmd:F8 CHANGELOG.md:25618 (the ordering row WAS built by e051fc5, `m437ord`; dated bracket).

GAP: `fileloaderrows` LOW (no ECOFF/Mach-O/SREC/Android corpus row; gate_upstream.sh says so itself); `ascaccountrows`
LOW (no committed row asserts NCR_TCL/NCR_TCM/NCRSTAT_TC); `cuemapgap` LOW (#127's "each regression-gated" CUE claims
have no carrier; diff_diskimage_io.c routes reads away from the CUE path); `modeselectrow` LOW (no diff_diskimage_*.c
row issues opcode 0x15); `scsicaprow` LOW (diff_diskimage_parse.c asserts the PARSER's count, never READ CAPACITY --
which is how `drecalccap` shipped past "advertised blocks exact"; discharged by drecalccap's detector; rider: the
row label says "advertised" of a parser value).

Fable's own additions: the ASC PIO DATA_OUT stub belongs with `ascpiozero` (Astra: as MED, above); `stalelbsbound`'s
one-line fix is a recalc at :1324; the MB89352 return-2 NULL-buffer route re-derived independently and found to be
batch 2d's `mboutcapacity` sequence (i).

---

## Batch 3a -- cpum88k, cpum88kinstr, generatem88kbcnd, tmpm88kbcnd (25 findings).
## Ruled by Fable (claude-fable-5-1, first-hand): 8 confirmed-new, 7 confirmed-filed, 1 record-L4, 0 test-gap, 0 refuted, 0 unsettled, 9 duplicate, of 25 findings (adjudication/fable_batch3a.md).
## Astra: 0 of 25 dispositions wrong (5 more need a change of wording or severity) (adjudication/codex_astraconfirm_3a.txt).  Mechanically assembled (mk_disp.py): every line below is VERBATIM from
## one of those two files; where an Astra amendment touches a finding, the AMENDMENT governs.

RULINGS (each finding's disposition statement, up to its `Checked:` line)
* cpum88k:F1 | CONFIRMED-FILED m88kexcsfu1
* cpum88k:F2 | CONFIRMED-FILED m88kdslotshadow
* cpum88k:F3 | CONFIRMED-FILED m88kexcfrozendmt
* cpum88k:F4 | CONFIRMED-NEW MED m88kdivcontext "Integer-divide (and precise FP) exception delivery writes no fcr2/fcr4/fcr5 and clears the destination scoreboard bit"
* cpum88k:F5 | CONFIRMED-FILED m88kidledup
* cpum88kinstr:F1 | CONFIRMED-NEW MED m88kextcross "ext with offset+width > 32 no longer sign-extends from bit 31"
* cpum88kinstr:F2 | CONFIRMED-NEW LOW m88ktrapmask "tb0/tb1 build their bit mask with a signed 1 << d (undefined at d = 31); m88k_rot's (1 << n) - 1 is the same class"
* cpum88kinstr:F3 | CONFIRMED-NEW MED m88knegdiv "div completes negative-operand divisions that the MC88100 traps on; the #195 comment states a false premise"
* cpum88kinstr:F4 | CONFIRMED-NEW HIGH m88kconvodd "int.sd/nint.sd/trnc.sd reject an odd source register, and flt.ds an odd destination, by stopping the CPU"
* cpum88kinstr:F5 | CONFIRMED-NEW HIGH m88kfpr0stop "every FP arithmetic/convert decode with rD = r0 stops the CPU instead of raising the FP unimplemented-opcode exception"
* cpum88kinstr:F6 | CONFIRMED-FILED OUTSTANDING_BUGS.md:1549-1558 (prose, no id) -- proposed id m88kconvdelivery
* cpum88kinstr:F7 | CONFIRMED-NEW MED m88kpairpadding "a double result into rD = r31 writes r[32], which later double-source reads return as the pair's low word (hardware ignores the write and reads r0)"
* cpum88kinstr:F8 | DUPLICATE-OF-ROW oddoptinyband
* cpum88kinstr:F9 | DUPLICATE-OF-ROW divbyinfnan
* cpum88kinstr:F10 | DUPLICATE-OF-ROW m88ksddovf
* cpum88kinstr:F11 | DUPLICATE cpum88k:F1
* cpum88kinstr:F12 | CONFIRMED-FILED m88kexchwtraps
* cpum88kinstr:F13 | DUPLICATE cpum88k:F3
* cpum88kinstr:F14 | DUPLICATE cpum88k:F2
* cpum88kinstr:F15 | CONFIRMED-FILED OUTSTANDING_BUGS.md:4675-4682 (prose, no id) -- proposed id m88kidleslotsem
* cpum88kinstr:F16 | DUPLICATE include2:F6 (batch 1b, RECORD-L4; DISPOSITIONS.md:54)
* cpum88kinstr:F17 | RECORD-L4 "HISTORICAL (#298), FIXED by #299: these arms once computed in host double before the store, so a residue finer than 2^-53 collapsed before a directed mode could see it -- hardware's sticky bit (MC88100UM: the OR of ALL infinitely-precise result bits) rounds 1.0 + 2^-60 UP under toward-+Inf, and this model stored 1.0.  fadd.sss, fsub.sss, fsub.sds and the mixed-width single-destination add/sub arms (#306) now route through ieee_sum_round_to_odd() before the modal single store (float_emul.c), and gate 11's `fadd band toward+Inf` row pins 0x3f800001.  fmul's product was always exact in double and a nonzero fdiv residue always survives; RN and RZ were never affected."
* cpum88kinstr:F18 | DUPLICATE cpum88k:F5
* generatem88kbcnd:F1 | CONFIRMED-NEW HIGH m88kbcndnest "a delayed branch entered as another delayed branch's delay slot: unbounded host recursion, and a dispatch pointer walked off its object"
* tmpm88kbcnd:F1 | DUPLICATE generatem88kbcnd:F1

ASTRA'S AMENDMENTS (5)
* cpum88k:F4 | Fable said CONFIRMED-NEW MED `m88kdivcontext`, covering integer-divide “and precise FP” delivery clearing the scoreboard | should be CONFIRMED-NEW MED, scoped to delivered integer-divide exceptions; cross-reference precise FP to `m88kexcsfu1` | `src/cpus/cpu_m88k.c:753` and `:799` show SFU1 stopping and returning before the scoreboard clear at `:835`. Missing FP context is already recorded at `OUTSTANDING_BUGS.md:490`. | confidence HIGH
* cpum88kinstr:F7 | Fable said CONFIRMED-NEW MED with replacement claiming `st.d r31` reads the spare element and `ld.d r31` becomes `ld` | should be CONFIRMED-NEW MED with corrected replacement: “Double-result FP handlers can write r[32], and double-source FP handlers read it back. Doubleword loads and stores starting at r31 are currently rejected by the decoder.” | `src/cpus/cpu_m88k_instr.c:3081` and `:3634` reject both load/store forms through `goto bad`; `src/cpus/cpu_dyntrans.c:2014` stops the CPU. | confidence HIGH
* cpum88kinstr:F15 | Fable said CONFIRMED-FILED MED, with “one host sleep per fold entry” and progress delayed by exactly one sleep | should remain CONFIRMED-FILED MED, saying the stale pre-slot value can request premature idling and potentially delay progress | `src/cpus/cpu_m88k_instr.c:2763` requests idle; `src/cpus/cpu_dyntrans.c:382` can cancel it for an interrupt. `src/core/emul.c:987` through `:1015` makes sleeping conditional on other CPUs and console input. A fixed sleep count is unsupported. | confidence HIGH
* cpum88kinstr:F17 | Fable said RECORD-L4 with replacement retaining “RN and RZ were never affected” | should remain RECORD-L4 LOW, deleting the replacement’s final sentence beginning “fmul’s product…” | `regress/diff_ieee_store.c:662` explicitly covers `1−2^-60` under RZ, expecting `0x3f7fffff`; the former double intermediate lost that residue. Repaired subtraction routing is at `src/cpus/cpu_m88k_instr.c:1082` and `:1107`. The blanket exemption is false. | confidence HIGH
* generatem88kbcnd:F1 | Fable said CONFIRMED-NEW HIGH with incorporated riders describing the outer branch’s “own delay_target” and a fixed nesting-depth boundary crossing | should remain CONFIRMED-NEW HIGH, describing the shared target overwritten by the inner branch and making boundary crossing dependent on the target’s array position | `src/cpus/tmp_m88k_bcnd.c:313` through `:318` overwrite the shared field subsequently read at `:325`; `:328` increments the dispatch pointer. `src/include/cpu.h:81` establishes the array boundary. | confidence HIGH

THE RULER'S OWN ADDITIONS (its section (b))
(b) Findings Astra missed, noticed while checking (mine unless credited):
* `m88kpsrbokill` NEW HIGH (raised by the draft check's section (b); verified here, absent from the draft): a
  supervisor `stcr` (or `rte`) writing PSR with the BO bit flipped relative to the machine's byte order reaches
  cpu_m88k.c:522-532 (`cpu->running = false`), and X(stcr) at cpu_m88k_instr.c:843-847 aborts; manual :2001-2006
  (BO "is set by an stcr or xcr instruction").  OUTSTANDING_BUGS.md:374-375's `m88kmxmkill` names the MXM bit of the
  same function only; greps for `endianness`, `PSR_BO`, `byte order` + m88k find nothing.  Supervisor-only; batch 2a's
  `armendianexit` is the ARM precedent at HIGH.  Smallest witness: supervisor `stcr` of PSR with BO toggled on
  testm88k, cold.
* `m88kexchwtraps` rider (the check's, verified): a software trap naming vector 2 also sets SXIP_E at
  cpu_m88k.c:859-860, which the row's text does not list.
* `m88kbcndnest` riders, by reading, unmeasured: (i) with an inner delayed branch TAKEN and three or more untaken
  outer ones, each outer `next_ic ++` (tmp_m88k_bcnd.c:328) advances from the target page's entry past
  `ics[ENTRIES+1]` (cpu.h:81 declares `ics[ENTRIES+2]`) -- the same walk as tmpm88kbcnd:F1 on a different object;
  (ii) an exception raised IN the inner slot is abandoned: m88k_exception sets EXCEPTION_IN_DELAY_SLOT
  (cpu_m88k.c:865-866), the inner handler clears it (:329-330), and a TAKEN outer then overwrites pc with its own
  delay_target (:324-326), so the handler at VBR never runs.
* L4 riders already placed above: cpu_m88k_instr.c:734-736 (under `m88knegdiv`), cpu_m88k.h:246-252 (under
  `m88kpairpadding`), CHANGELOG.md:23018-23020 (under `m88kexchwtraps`).  One more, LOW, under the existing
  `divbyinfnan` (which already carries L4 riders): cpu_m88k_instr.c:1836-1838 says fdiv.dds's quotient is "rounded
  once, correctly"; through `ieee_div_round_rm` (float_emul.c:880-902) that holds for finite divisors with
  |dividend| >= 2^-969 and fails in the row's infinite-divisor shape under the directed modes.
* Scope widenings recorded in the lines above: `m88kfpr0stop` (8 sites), `m88kconvodd` (+ flt.ds :3235-3238),
  `m88kpairpadding` (17 writers), `m88ktrapmask` (+ the :513 rotate site).

---

## Batch 3b -- cpumips, cpumipsinstr, devsgiip30, devsgire (25 findings).
## Ruled by Fable (claude-fable-5-1, first-hand): 9 confirmed-new, 9 confirmed-filed, 6 record-L4, 1 test-gap, 0 refuted, 0 unsettled, 0 duplicate, of 25 findings (adjudication/fable_batch3b.md).
## Astra: 0 of 25 dispositions wrong (3 more need a change of wording or severity) (adjudication/codex_astraconfirm_3b.txt).  Mechanically assembled (mk_disp.py): every line below is VERBATIM from
## one of those two files; where an Astra amendment touches a finding, the AMENDMENT governs.

RULINGS (each finding's disposition statement, up to its `Checked:` line)
* **cpumips:F1 | CONFIRMED-NEW MED `mipsbadvpnscale` "R4000 Context/XContext BadVPN2 is scaled by the matched (or last-scanned) TLB entry's page size instead of fixed VA bits 31:13 / 39:13"**
* **cpumips:F2 | TEST-GAP-FILE `mipslowrefrow` (LOW)**
* **cpumipsinstr:F1 | CONFIRMED-NEW HIGH `mipscop0tail` "Five COP0 decoder arms still `goto bad` (CPU stops) on guest-executable encodings: EI/DI off-R5900, MFMCz non-ei/di, BC0x, unknown rs"**
* **cpumipsinstr:F2 | CONFIRMED-NEW HIGH `mipsresetalias` "The reboot sentinel is gated on the VIRTUAL address's low 29 bits, so `break 0x30378` at any VA with low bits 0x1fc00000 stops the emulator (or raises CpU instead of BP)"**
* **cpumipsinstr:F3 | CONFIRMED-NEW LOW `mipsaddiuub` "ADDIU and seven fused-ADDIU handlers add two `int32_t` in signed arithmetic (UB on the wrap ADDIU is defined to perform)"**
* **cpumipsinstr:F4 | CONFIRMED-NEW LOW `mipsjregionub` "MODE32 J/JAL/JAL_trace: `page_base + (int32_t)arg[1]` overflows `int32_t` for a jump in the last two slots of page 0x7ffff000"**
* **cpumipsinstr:F5 | CONFIRMED-NEW MED `mipssubmin` "SUB/DSUB test overflow on the NEGATED subtrahend: MIN-MIN traps, 0-MIN does not"**
* **cpumipsinstr:F6 | CONFIRMED-NEW MED `mipscachepriv` "The R3000 cache-invalidate fold mutates the loop register and skips to the final MTC0 before any COP0 availability check runs"**
* **cpumipsinstr:F7 | CONFIRMED-FILED (by prose, no id) `OUTSTANDING_BUGS.md:2636-2638` -> propose id `mipsreadpriv`, MED**
* **cpumipsinstr:F8 | CONFIRMED-FILED (by prose, no id) `OUTSTANDING_BUGS.md:2636-2638` -> propose id `mipsr3kpcpriv`, MED (contrived)**
* **cpumipsinstr:F9 | CONFIRMED-NEW MED `mipspsfault` "PS-format COP1 on an R3000/R4000-class FPU raises RI; the R4000 owes an FPU Unimplemented-Operation exception (Cause.E, FPE), and CpU when CU1 is clear"**
* **cpumipsinstr:F10 | CONFIRMED-NEW MED `mipssynci` "SYNCI has no REGIMM decoder case, so modelled Release-2 CPUs (4KEc, 24KEc, 5KE) raise RI on a defined instruction"**
* **cpumipsinstr:F11 | RECORD-L4 `CHANGELOG.md:19998-20000` [HEAD :20082-20084]**
* **cpumipsinstr:F12 | RECORD-L4 `CHANGELOG.md:23042-23044` [HEAD :23126-23128] + source rider `cpu_mips_instr.c:5377-5379`**
* **devsgiip30:F1 | CONFIRMED-FILED `ip30setisrassign` (queue MED, kept)**
* **devsgiip30:F2 | RECORD-L4 `dev_sgi_ip30.c:50-52, :57-60` + rider `:216-218, :264-266`**
* **devsgiip30:F3 | RECORD-L4 `CHANGELOG.md:2097` [HEAD :2181] + rider `regress/artifacts/ip30abortkill/ip30_abort_probe.py:187`** **Draft CHANGED (DOUBTFUL -> RECORD-L4).**  The draft and the check both left this unchecked as "outside the permitted artifact scope"; the probe is TRACKED at `8ea26abb` (`git ls-tree`: blob `a1259e35`), so it is a committed file and in scope.  Checked: `:467` `t, alive = session(...)` scores BOTH `tick 50` (`:468`) and `tick 50 txt` (`:474`); `:553` one session scores `xbit isr` (`:554`) and `xbit tick` (`:559`), deliberately ("it needs both announce classes in ONE lifetime", `:557-558`).  The probe's own docstring at `:187` says "One fresh process per scored row." -- false of itself. Replacement for the CHANGELOG: "one fresh process per SESSION -- most sessions score one row, but `tick 50`/`tick 50 txt` and `xbit isr`/`xbit tick` each score two rows from ...
* **devsgire:F1 | CONFIRMED-FILED `sgirespanchk` -- with the row's open question ANSWERED and its grade re-opened: RULE-QUESTION shoddprfield (consequence shown: MED; by the rule's letter: HIGH).  Rider to `sgilinearoob`.**
* **devsgire:F2 | CONFIRMED-FILED `sgirebufuninit` (queue HIGH "under active adjudication"; by this brief's rule MED)**
* **devsgire:F3 | CONFIRMED-FILED `sgirebufshiftub` (LOW)**
* **devsgire:F4 | CONFIRMED-FILED `sgiretlbshiftub` (queue "med"; by this brief's rule LOW)**
* **devsgire:F5 | CONFIRMED-FILED `sgirandomskipput` (queue MED, kept), with the draft's ROP/stipple qualification**
* **devsgire:F6 | RECORD-L4 `dev_sgi_re.c:294-295`**
* **devsgire:F7 | RECORD-L4 `dev_sgi_re.c:465-469` -- discharges the owed sentence at `OUTSTANDING_BUGS.md:14775-14778`** **Draft CHANGED (FILED-BY-PROSE + new id `sgirewidthrationale` -> RECORD-L4, no id).**  Checked: `:465-469` says a narrower access "simply runs fewer iterations and stays in bounds -- there the guard is modelling fidelity only"; the loop at `:500-501` (and `:563-564`, `:587-588`) reads `data[hwi]*256 + data[hwi+1]`, so `len == 1` would read `data[1]`, one past the caller's `uint8_t data[LS_SIZE]` (`cpu_mips_instr_loadstore.c:46`); the `:491` guard is what prevents it; `memory.c:55-77` adds no even-width filter.  The queue ALREADY records the correct reason at `:14770-14773` and says "The round owes a sentence, not a row" -- so this is a false comment (the brief's rule 1, corrected in place), and giving it an id would manufacture the row the queue declined.  Replaceme...
* **devsgire:F8 | CONFIRMED-FILED `sgidefatalstale` (LOW)**

ASTRA'S AMENDMENTS (3)
* **devsgire:F1 | Fable said CONFIRMED-FILED `sgirespanchk`, severity left as RULE-QUESTION/MED | should be CONFIRMED-FILED HIGH |** The existing row is correctly identified at `OUTSTANDING_BUGS.md:16292`. Guest-mediated accesses cross declared array bounds at `src/devices/dev_sgi_re.c:501`, `:564` and `:707`; the firmware path exists at `src/promemul/arcbios.c:1140`. Remaining inside the enclosing allocation does not exempt these accesses from your explicit outside-buffer HIGH rule. Retain the `sgilinearoob` and record riders. **| confidence high**
* **cpumipsinstr:F11 | Fable said RECORD-L4, with replacement asserting ADD/ADDI/DADD/DADDI “raise EXCEPTION_OV correctly” | should be RECORD-L4 with qualified replacement |** `src/cpus/cpu_mips_instr.c:4606–4607` and `:4797–4798` replace zero-destination arithmetic instructions with `nop`, bypassing overflow detection. Use: “All six handlers contain overflow detection. The ADD/ADDI/DADD/DADDI predicates are correct when their handlers execute; SUB/DSUB predicates fail for a minimum signed subtrahend. Zero-destination decoding separately suppresses these handlers and their overflow exceptions.” Retain the unsigned-arithmetic explanation; qualify the queue rider likewise. **| confidence high**
* **cpumipsinstr:F3 | Fable said CONFIRMED-NEW LOW, “ADDIU and seven fused-ADDIU handlers” | should be CONFIRMED-NEW LOW, “ADDIU and seven addition sites across six fused handlers” |** `src/cpus/cpu_mips_instr.c:3579` defines one handler containing both cited additions at `:3591` and `:3595`. The defect and severity stand; the handler count needs correction. **| confidence high**

THE RULER'S OWN ADDITIONS (its section (b))
## (b) What Astra missed, noticed while checking (mine unless credited)

1. **cpumips:F1's REFILL half (mine):** `vaddr_vpn2` is recomputed for every scanned entry before the match test
   (`memory_mips_v2p.c:286-287, :313-314`), so on a MISS the Context/XContext BadVPN2 handed to `mips_cpu_exception`
   (`:452-453`) carries the LAST scanned entry's page-size scaling -- a refill's PTE pointer depends on an unrelated TLB
   entry's PageMask.  Same row `mipsbadvpnscale`; it widens the reach from invalid/modified faults on large pages to every
   refill while a large-page entry sits at the scan's last index.
2. **`mipstrapgate` MED (candidate; the REGIMM half raised by the codex draft CHECK's section (b), verified here; the
   SPECIAL half is mine):** `cpu_mips_instr.c:5358-5369` replaces TGEI/TGEIU/TLTI/TLTIU/TEQI/TNEI with `instr(reserved)`
   when `isa_level < 32`, so the R4000 (isa 3, `mips_cpu_types.h:73`), R4400, R5000 and R10000 raise RI on instructions
   their manual defines (`mips_r4000.txt:1141` Trap exception "when a TGE, ..., TGEI, ..., or TNEI instruction results in a
   TRUE condition"; `:5683` TEQI) -- the gate should be `< 2` (MIPS II).  **The SPECIAL-form traps have the opposite
   defect:** `:4535-4540` decode TGE/TGEU/TLT/TLTU/TEQ/TNE with NO ISA gate, so an R3000 (MIPS I) executes them where RI
   is owed.  One row, both halves.  Not filed (`grep -i 'TGEI|TEQI|Trap opcode|trap-immediate'` in `OUTSTANDING_BUGS.md`:
   0; absent from `DISPOSITIONS.md`).  L4 riders: `CHANGELOG.md:23049-23051` [HEAD :23133-23135] and the comment at
   `cpu_mips_instr.c:5384-5386` cite that gate as "the tree's own shape" -- the shape is the defect.
3. **`_scratchpad/idt_r30xx.txt` is EMPTY (0 bytes, 2026-07-25)** while `CLAUDE.md` lists it among the extracted manual
   texts and the PDF (1.2 MB) is present.  Any past "checked against the IDT R3000 manual" claim that used the text file
   checked nothing.  Apparatus/records, LOW; one line in the carrier's manual list, not a queue row.
4. **cpumipsinstr:F7 scope note:** the `rt == $zero -> nop` fold also drops CFC0 (`:4950-4951`); include it in
   `mipsreadpriv`.
5. **cpumipsinstr:F9/F2 record riders** are listed under those findings (the `#290` RI prescription at `:5071-5074` and
   `OUTSTANDING_BUGS.md:2260-2261`; the `#235` "phys" wording at `:4660-4665`, `CHANGELOG.md:20152-20154` and
   `OUTSTANDING_BUGS.md:2604-2605`).

## Draft dispositions changed, and why

| finding | draft | ruling | why |
|---|---|---|---|
| cpumipsinstr:F1 | FILED-BY-PROSE :2668-2671 | CONFIRMED-NEW HIGH `mipscop0tail` | the backlog line is CLOSED by `#234/#236/#237` (:2601-2619); a closed item is not a filing for its residual; the five arms are named nowhere |
| cpumipsinstr:F2 | FILED-BY-PROSE :2668-2671 "reopen" | CONFIRMED-NEW HIGH `mipsresetalias` | `#235` is recorded DONE at :2604-2605 with a false description; same rule |
| devsgiip30:F3 | DOUBTFUL (probe "out of scope") | RECORD-L4 | the probe is a committed file at `8ea26abb`; read, and it scores two rows per session twice (:467-474, :553-559) |
| devsgire:F7 | FILED-BY-PROSE + new id `sgirewidthrationale` | RECORD-L4, no id | a false comment is corrected in place (rule 1); the queue paragraph it cites says "owes a sentence, not a row" |

Severities qualified against the draft: devsgire:F1 (draft HIGH -> RULE-QUESTION shoddprfield, MED by consequence);
devsgire:F2 (MED under the rule, the queue's HIGH left to its pending adjudication); the rest of the draft's grades kept.
Against the CHECK: it was right on F1/F2 (NEW) and left F3 (ip30) and F7 (re) where the draft had them; both changed here.

---

## Batch 3e -- devm8820x, devpcc2, devosiop, devle (25 findings).
## Ruled by Fable (claude-fable-5-1, first-hand): 7 confirmed-new, 7 confirmed-filed, 6 record-L4, 2 test-gap, 0 refuted, 3 unsettled, 0 duplicate, of 25 findings (adjudication/fable_batch3e.md).
## Astra: 0 of 25 dispositions wrong (3 more need a change of wording or severity) (adjudication/codex_astraconfirm_3e.txt).  Mechanically assembled (mk_disp.py): every line below is VERBATIM from
## one of those two files; where an Astra amendment touches a finding, the AMENDMENT governs.

RULINGS (each finding's disposition statement, up to its `Checked:` line)
* devm8820x:F1 | UNSETTLED "obtain the MC88200 User's Manual (2nd ed. 1990, the bitsavers PDF both seats cite), `pdftotext -layout` it into `_scratchpad/`, and read the SCR command table (p.2-10): if the PATC-flush codes 0x38-0x3f are documented as aliases (command bit 3 ignored), file `m8flushalias` MED -- an alias is dropped by the default arm and the guest's TLB flush silently does not happen; if they are undefined commands, complain-and-drop is the correct behaviour and the finding is REFUTED"
* devm8820x:F2 | UNSETTLED "same acquisition; read section 6.2.1.2 / p.6-4: if the BATC write ports do not decode A5 (0x420-0x43c alias BWP0-7), file `m8bwpalias` MED -- a BATC write through an alias is dropped at :492-523 and the shadow `batc[]` at :479 is never updated, so a 512 KB block the guest believes it mapped does not exist; if A5 is decoded, dropping 0x420-0x43c is correct"
* devm8820x:F3 | CONFIRMED-NEW MED m8dirtyfast "m88k: a READ of a writable page installs a writable fast-path mapping, so the first store through it never sets the page descriptor's M bit"
* devm8820x:F4 | CONFIRMED-FILED m8seg
* devm8820x:F5 | UNSETTLED "same acquisition; read section 6.2.1.1 pp.6-4..6-5 against the 'IDR read-only' technical summary Astra itself cites: if the ID field (bits 31-24) is software-writable on the 88200 rev 9 the fork models (dev_luna88k.c:949, :960), file `m8idfield` MED (writes at :262-272 are dropped, and diff_m8820x.c:749 `E3` PINS the drop, so the fix is an oracle re-pin first); if IDR is read-only, the drop is correct and the finding is REFUTED"
* devm8820x:F6 | CONFIRMED-FILED m8probe
* devm8820x:F7 | RECORD-L4 "memory_m88k.c:344-366 writes PG_U (and PG_M on a write) back into the page descriptor IN EMULATED MEMORY after every SUCCESSFUL table walk (a walk that faults writes nothing); a PATC READ hit sets PG_U only in the PATC copy (:228-229), but a PATC WRITE hit on an entry whose PG_M is clear ALSO updates the guest descriptor, through m8820x_mark_page_as_modified() (:217-224; it ORs PG_M|PG_U into the descriptor at :86 and writes it back at :93). So evicting an entry that a narrower flush would have spared can set a U bit the guest had cleared, on the next READ."
* devm8820x:F8 | RECORD-L4 "SAR is read in two places: by guest readback through the generic `odata = regs[relative_addr / 4]` at :258, and at :110 as the address operand of a flush command -- and that command's arm does its own INVALIDATE_ALL at :187, so the SAR write owes no purge. SCTR is stored at :460 and read back to the guest through :258; NO TRANSLATION CONSUMER in src/ reads reg[CMMU_SCTR] (the only other occurrences are the definitions at thirdparty/m8820x.h:64,118-120)."
* devm8820x:F9 | TEST-GAP-FILE m8supersegrow
* devpcc2:F1 | CONFIRMED-NEW MED pcc2timerlanes "PCC2: byte and halfword writes that START inside one of the four 32-bit counter/compare words are declined"
* devpcc2:F2 | CONFIRMED-FILED pcc2widecompose
* devpcc2:F3 | CONFIRMED-FILED pcc2counter8
* devpcc2:F4 | CONFIRMED-FILED pcc2iackmodel
* devpcc2:F5 | RECORD-L4 "`assert = 0' -> `return' at THIS line WAS a one-token mutant every one of the first seven rows passed (killtable_20260907); the #512 L2 repair's `c040 noassert' / `c040 noassert2' rows start with the line ALREADY ASSERTED, so the `return', which skips the INTERRUPT_DEASSERT below, leaves it asserted and reddens both: KILLED 9/10 in table 2 (killtable_20260908) and 14/16 on the repaired probe (ctlq_20260909/repaired_M_return.raw)."
* devpcc2:F6 | RECORD-L4 "RESIDUAL, disclosed under clause (e): these rows establish delivery and suppression for SCC TX at one priority, across two C040 encounters, recovery after C040 is cleared (`c040 recover', M_sticky killed 11/12), and GENCTL readback with MIEN preserved (`c040 genctl', M_mienclobber killed 12/13). They do not cover suppression that corrupts MASK or the pending counts, or other sources and priorities. Suppression by a different implementation route is not a defect -- the contract is behaviour, not the use of a particular local variable."
* devosiop:F1 | CONFIRMED-FILED exitunowned76 (FILED-BY-PROSE at the file level; the site id to assign when a round takes it: `osiopselectzero`, HIGH)
* devosiop:F2 | CONFIRMED-NEW MED osiopzeroram "OSIOP: a SCRIPTS or DMA read from RAM whose 1 MB memblock was never written stops the script engine instead of reading zeros"
* devosiop:F3 | CONFIRMED-FILED exitunowned76 (FILED-BY-PROSE at the file level; the site id to assign: `osiopregexit`, HIGH)
* devosiop:F4 | RECORD-L4 "full sweep + pmax deep (disk/net -- the pmax machines attach ASC or SII, never osiop, so the #114/#118 osiop guards were not exercised by that run) + arc clean"
* devle:F1 | CONFIRMED-NEW MED lebufsize "LANCE: the 12..1900 byte-count window rejects legal buffers -- RX buffers above 1900 bytes and TX continuation fragments under 12"
* devle:F2 | CONFIRMED-NEW MED letxrestart "LANCE: STOP then STRT does not restore TXON after a transmit abort or MERR -- only INIT does"
* devle:F3 | CONFIRMED-NEW MED letxshortage "LANCE: a chip-owned TX continuation that is not yet available leaves the partial frame pending with no BUFF, no TINT and TXON still set"
* devle:F4 | CONFIRMED-NEW MED lerxstaleenp "LANCE: RMD1 status is OR-ed into the host-written word, so a stale ENP (and stale ERR/FRAM/OFLO/CRC/BUFF/STP) survives into the status the chip returns"
* devle:F5 | RECORD-L4 for dev_le.c:548-556: "#274: The descriptor is owned by the chip, but it is not usable. The lookahead below only lets a frame continue into a descriptor that this very test accepted AT LOOKAHEAD TIME, so within one call this is the FIRST buffer of a frame: nothing has been filled in, and the descriptor is deliberately NOT written back. Drop the frame just like the exhaustion case above. Two caveats: receive DMA (:576-577) can overwrite descriptor storage that the ring overlaps, and the full-ring exit at :663-667 returns with a partial frame retained (le_register_fix keeps it, :767-770), so a LATER call can reach this arm mid-frame; it then drops the partial frame with MISS. (The manual gives no status for a descriptor violating the '1111' rule; reporting it as a missed packet is emulator policy, not documented Am7990 behaviour.)" -- and in CHANGELOG.md@8ea26abb:20...
* devle:F6 | TEST-GAP-FILE leregrows

ASTRA'S AMENDMENTS (3)
* devm8820x:F7 | Fable said RECORD-L4, “after every SUCCESSFUL table walk” | should be RECORD-L4 LOW with the qualification **“when FLAG_NOEXCEPTIONS is absent.”** That qualification also applies to PATC-hit U/M updates. Replace “a walk that faults writes nothing” with “does not update the guest descriptor”; PATC refill can precede the protection fault. | Evidence: [memory_m88k.c:217](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/memory_m88k.c:217), [:319](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/memory_m88k.c:319), [:344](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/memory_m88k.c:344); [diff_m8820x.c:331](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/diff_m8820x.c:331) explicitly uses translations without these side effects. | confidence HIGH
* devosiop:F2 | Fable said CONFIRMED-NEW MED `osiopzeroram`, but also denies the read-side “would have been a host NULL deref” claim | should be **keep CONFIRMED-NEW MED; correct that explanation.** NULL legitimately represents zero-filled RAM, but the unguarded helpers would still dereference NULL. The defect is rejecting valid zero-filled RAM and stopping SCRIPTS. | Evidence: [memory.c:537](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/core/memory.c:537) defines the zero-read contract; [dev_osiop.c:233](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_osiop.c:233) and [:259](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_osiop.c:259) perform actual pointer dereferences after the guards. | confidence HIGH
* devle:F3 | Fable said CONFIRMED-NEW MED `letxshortage`, “a chip-owned TX continuation that is not yet available” | should be **CONFIRMED-NEW MED, “a host-owned TX continuation (OWN clear)”**; retain the pending-frame and missing-error findings. | Evidence: [dev_le.c:343](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_le.c:343) explicitly identifies OWN clear as unavailable, and the following branch returns without aborting the partial frame. | confidence HIGH

THE RULER'S OWN ADDITIONS (its section (b))
## (b) What Astra missed, noticed while checking (mine unless marked)

1. **OSIOP DNAD/ADDER 32-bit access ends the process** -- dev_osiop.c:942 and :946 whitelist OSIOP_DNAD (0x28) and OSIOP_ADDER (0x3c) for 32-bit width, then the register switch at :969-1143 has NO case for either (verified: the only occurrences of those names in the file are :333, :942, :946), so one aligned `ld` of DNAD or ADDER falls into `default:` and `exit(1)` at :1152 with no fault path and no lane swap needed. HIGH; under `exitunowned76`; site id to assign `osiopdnadexit`. Astra's checked-clean list does not cover it; the draft and the check missed it.
2. **LANCE CSR1-3 access comments have the STOP polarity reversed** -- dev_le.c:986-991 and :996-1001 say reads are undefined / writes ignored "if the stop bit is set"; TM1986.txt:1572-1582 says CSR1-3 are accessible only when STOP IS set, and that with STOP clear a read returns undefined data and a write is ignored. Upstream comment, wrong record, LOW; a records round can take it with devle:F5. (Also named by the check.)
3. **PCC2 OVF counter semantics** -- dev_pcc2.c:246-250 and :270-274 increment OVF when the count crosses 0x7fffffff -> 0x80000000; vmesbcp2.txt:5211-5213 says the overflow counter "is incremented each time the tick timer sends an interrupt" (:5025-5026 likewise, on compare). With COC set the model's OVF never moves; without it, once per 35.8 minutes. Upstream tick code the fork's rounds did not change, so outside this batch by the brief's own scope rule; recorded as a candidate (`pcc2ovfcount`, MED if adopted). (Named by the check; verified here.)
4. **m8820x E3 pins the IDR write-drop** (diff_m8820x.c:749), so if devm8820x:F5 resolves to "writable", the fix is an oracle correction and E3 is re-pinned RED first.
5. **`osiop_hostpage_fault()`'s message** (dev_osiop.c:207-209) claims a NULL dereference "would have been" the alternative; on the read side it would not (memory.c:537) -- folds into `osiopzeroram`.
6. Riders already attached above and worth a records round's attention: OB:6254-6255 (the superseded SCTR wording), the `pcc2iackmodel` ordering precondition now discharged, the `pcc2c040returnmutant` closure, and D6b's 0x15 oracle being the over-invalidation `m8seg` will have to re-pin.

---

## Batch 3d -- cpush, devpvr, cpuppc, cpualpha, cpualphapalcode, devlca (31 findings).
## Ruled by Fable (claude-fable-5-1, first-hand): 7 confirmed-new, 9 confirmed-filed, 13 record-L4, 2 test-gap, 0 refuted, 0 unsettled, 0 duplicate, of 31 findings (adjudication/fable_batch3d.md).
## Astra: 0 of 31 dispositions wrong (5 more need a change of wording or severity) (adjudication/codex_astraconfirm_3d.txt).  Mechanically assembled (mk_disp.py): every line below is VERBATIM from
## one of those two files; where an Astra amendment touches a finding, the AMENDMENT governs.

RULINGS (each finding's disposition statement, up to its `Checked:` line)
* cpush:F1 | CONFIRMED-NEW HIGH shifetchkill "SH: a privileged instruction fetch from 0xe4000000-0xffffffff ends the process at memory_sh.c:379-381 -- reached through the guest's own VBR (+0x100 / +0x600) on the next exception or interrupt, or by a direct branch"
* cpush:F2 | CONFIRMED-NEW MED shresetinit "SH reset arm (power-on, manual, TLB multiple-hit) sets PC, VBR and SR only; FPSCR, MMUCR and the on-chip module registers keep their pre-reset values"
* cpush:F3 | CONFIRMED-FILED shsweep
* cpush:F4 | CONFIRMED-NEW MED shinttieorder "SH INTC: equal-priority requests are ordered by arrival (assert path) or by lowest INTEVT code (rescan), not by Table 19.5 -- SCIF RXI loses to an earlier TXI"
* cpush:F5 | CONFIRMED-FILED OUTSTANDING_BUGS.md:8691-8694 (prose, no id) -- proposed id shdmteupper, LOW
* cpush:F6 | RECORD-L4 cpu_sh.c:147-148: "Two mutants of #458 -- dropping the RTC and IPRB blocks (`m_iprconly`), and dropping the three RTC lines (`m_nortc`) -- were MEASURED escaping a ten-row behavioural detector with a clean 10/10, because the sources they affect have no INTERRUPT_ASSERT anywhere in this tree."
* cpush:F7 | RECORD-L4 CHANGELOG.md:19058-19066 (HEAD :19142-19150): "So `#458` exposes `int_prio_and_pending[]` through the settings interface as `iprio_<intevt>`, and two rows read the table directly: after a guest `IPRB := 0xa000` the WDT slot must read `0xa`, and after `IPRA := 0x000c` the RTC slot must read `0xc`.  **Those two rows are the reason the exposure exists**; without them it is an unused convenience.  `int_to_assert` and `int_level` are deliberately NOT exposed (cpu_sh.c says why: no row reads them, and they are a software cache rather than architectural state).  *Each entry is registered with `CPU_SETTINGS_ADD_REGISTER8`, matching the table's `uint8_t` declaration; the macros take the variable's ADDRESS, so a mismatched width would read neighbouring bytes.*"
* cpush:F8 | RECORD-L4 CHANGELOG.md:19183-19185 (HEAD :19267-19269): "landisk programs IPRC -- the boot witness shows it.  The other SH machines in the tree are `testsh` (machine_test.c), `dreamcast` and `hpcsh` (both select an SH7750: machine_dreamcast.c, machine_hpcsh.c); whether their guests program IPRC before enabling SCIF interrupts is not established here, so the no-regression claim covers landisk and the regression battery, not every SH machine."
* devpvr:F1 | CONFIRMED-NEW HIGH pvrdirtyregion "PVR pvr_extend_update_region(): with zero display width it divides by zero (SIGFPE) on any multi-byte VRAM write whose span straddles DIWADDRL; with ordinary geometry an unclipped lower endpoint below the display start yields an inverted region and the visible update is discarded"
* devpvr:F2 | CONFIRMED-NEW LOW pvrofssignedovf "PVR fb tick: `int vram_ofs` is advanced with signed arithmetic (DIWADDRL + y1*bytes_per_line, then per line) BEFORE the unsigned `% VRAM_SIZE`; a DIWADDRL near INT_MAX overflows it (UB; the index is still masked, no out-of-bounds access shown)"
* devpvr:F3 | CONFIRMED-NEW LOW pvrrgbuninit "PVR TA: `wf_r/g/b[4]` are not zero-initialised (#12 covered x/y/z/u/v only); a textured strip's slide at :1407/:1411 copies indeterminate values"
* devpvr:F4 | CONFIRMED-FILED OUTSTANDING_BUGS.md:2721-2723 (prose, no id; repeated at :2704-2705) -- proposed id pvrrenderexit, HIGH
* devpvr:F5 | CONFIRMED-NEW LOW pvrpaletteend "PVR texture sampler: the #55 clamp `addr > VRAM_SIZE-2` is sized for two-byte texels; it redirects the one legal one-byte sample at VRAM_SIZE-1 (8-bit palette, format 6) to VRAM_SIZE-2, and never fires for the two-byte formats, whose addresses are even"
* devpvr:F6 | CONFIRMED-FILED sh4dmacintr
* devpvr:F7 | RECORD-L4 dev_pvr.c:2619-2624 and CHANGELOG.md:21629-21633 (HEAD :21713-21717): comment -> "Extend the dirty region once per bank instead of once per byte -- far fewer calls than the original, and without dirtying the whole 4 MB gap between the banks when a write touches both.  Within a bank this matches the per-byte result for spans inside the visible frame.  It is NOT equivalent for a span that straddles the visible-FB start: pvr_extend_update_region() does not clip a lower endpoint below DIWADDRL, so `low / bytes_per_line` of the wrapped unsigned difference can land above fb_update_y2 and the tick discards the inverted region -- the visible bytes are not redrawn until something else dirties their line (row pvrdirtyregion).  The per-byte form never produced such a span."  CHANGELOG :21630-21632 -> "Behaviour-wise it marks the same dirty line range for spans inside the vi...
* cpuppc:F1 | RECORD-L4 cpu_ppc.c:1918-1921: "Raise one or more FPSCR exception CAUSES, apply the implicit-FX rule, and let the summaries follow.  Every arithmetic and convert handler that detects an exception goes through here, so that a future cause cannot be added without FX and the summaries coming with it -- with ONE exception kept as written: frsp's signalling-NaN arm (cpu_ppc_instr.c, the #327 block) tests and sets VXNAN and FX itself and calls ppc_fpscr_recompute() directly; for a single cause its per-bit test is this same rule."
* cpuppc:F2 | TEST-GAP-FILE ppcmixedfx LOW
* cpualpha:F1 | RECORD-L4 CHANGELOG.md:19713 (HEAD :19797): "`READ_WORD_LE/BE` macros (uint32_t-cast instruction-word assembly); 9 instruction-word fetch sites converted -- 5 in disassemblers (cpu_alpha.c, cpu_arm.c x2, cpu_i960.c x2) and 4 in the execution translators' `X(to_be_translated)` (cpu_arm_instr.c x2, cpu_i960_instr.c x2)"
* cpualphapalcode:F1 | CONFIRMED-FILED alphapcbbvirt
* cpualphapalcode:F2 | TEST-GAP-FILE alphatbilowerwidth LOW FOR-PEER
* cpualphapalcode:F3 | RECORD-L4 cpu_alpha_palcode.c:348 and :356-357 FOR-PEER: ":348 'the live probe has since grown to 13 rows' -> 'has since grown (15 rows at #520's close)'; :356-357 'The SHIPPED 13-row detector scores 10/13 and 13/13 on those two builds (killtable_20260910/t2/probe_{HEAD,BASE}.raw)' -> 'The t2 13-row instrument scored 10/13 and 13/13 on those two builds (killtable_20260910/t2/probe_{HEAD,BASE}.raw); the SHIPPED 15-row detector scores 11/15 and 15/15 (killtable_20260910/t3/SCORES.txt, legs HEAD and BASE).'"
* cpualphapalcode:F4 | RECORD-L4 cpu_alpha_palcode.c:406-409 FOR-PEER: "an announce here has no measured delta, and no OSF/1-ABI guest ISSUES an unrecognised selector -- the five macros are the ABI's documented values.  It is REACHABLE: alpha_pal_tbi(op, va) forwards any `op`, CALL_PAL 0x33 checks nothing but privilege, and this file's own detector drives 0, 4 and 0x100000001 through it."
* cpualphapalcode:F5 | RECORD-L4 cpu_alpha_palcode.c:330-332 FOR-PEER: "(#520: the upstream comment here said 'a0 is ignored for now. TODO.' while the code already tested `a0 >= 1` -- as an UNSIGNED compare, which is the defect below.  a0 was always read; the comment was removed rather than left to mislead.)"
* cpualphapalcode:F6 | RECORD-L4 CHANGELOG.md:4870 (HEAD :4954): "(`alpha_tbi_probe.frozen.py`; the shipped `regress/alpha_tbi_probe.py` differs from it by 27 comment-only lines -- 6 removed, 21 added, all in the module docstring or in display-only row notes; see below)"
* cpualphapalcode:F7 | RECORD-L4 CHANGELOG.md:6807-6808 (HEAD :6891-6892): "Three red rows now read TWO distinct cells: `swpctx ptbr` and `swpctx notflags` both read A+16 (the value, and that it is not the flags word), and `swpctx flags` reads A+40 -- so the second consequence has its own cell instead of being inferred from the PTBR word."
* devlca:F1 | CONFIRMED-FILED lcaisaphys (and lcaisaphyshit) FOR-PEER
* devlca:F2 | CONFIRMED-FILED lcauninitbyte
* devlca:F3 | CONFIRMED-FILED lcaconfbit1
* devlca:F4 | CONFIRMED-FILED lcaiocstat0
* devlca:F5 | RECORD-L4 CHANGELOG.md:5528-5531 (HEAD :5612-5615) and regress/lca_confbus_probe.py:96-98 FOR-PEER: CHANGELOG -> "`lca_pci_conf` tests `writeflag` and, in the refusal arm, `reg == 0` (all-ones for register 0, zero elsewhere) and `bus == 0`; it never branches on `len` or `func`.  The register axis is therefore a body-tested partition and its two rows (`t1 reg0`, `t1 reg4`) were owed as floor, not clause (e); the bus-value partition {0, other} is body-tested but observationally identical through this channel (a type-1 cycle to any other bus reaches bus_pci's empty-slot answer, the same all-ones/zero pair), so it stays disclosed; `len` and `func` fall to clause (e)."  Probe :96-98 -> "this handler's own code tests `writeflag`, `reg == 0` and `bus == 0`; it never branches on `len` or `func`.  The register partition is rowed (`t1 reg0`/`t1 reg4`); the bus partition is body-test...
* devlca:F6 | RECORD-L4 CHANGELOG.md:5335-5342 (HEAD :5419-5426) FOR-PEER: "M8 (`|=` -> `=` on the assert arm) measured EQUIVALENT on #516's detector, and the warrant is time-indexed: at #516 `warned` held only the two IRQ bits, so the first assert -- the only one that assigns -- saw `warned == 0`.  Since #518 the same word carries six IOC announce bits (dev_lca.c:53-60, written at :331 and :495), so an IOC announce before the first ISA interrupt makes `=` erase those latches: M8 is NOT equivalent at HEAD (whether #516's table would red on a re-run depends on row order and is not measured).  The aggregate-edge reasoning (`irr & ~ier`) is unchanged and still right."

ASTRA'S AMENDMENTS (5)
* cpush:F6 | Fable said RECORD-L4 with a fragment replacement for the probe’s “sole killer” clause | should be RECORD-L4 with the complete sentence: “This WDT row kills the RTC-and-IPRB deletion (`m_iprconly`); the RTC row also kills it.” The literal proposed substitution leaves the row identified as the mutant | [regress/sh_iprbcd_probe.py:322](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/sh_iprbcd_probe.py:322); [CHANGELOG.md:19119](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/CHANGELOG.md:19119) explicitly records both failing rows | HIGH confidence
* cpush:F7 | Fable said RECORD-L4 retaining “without [the WDT/RTC rows] it is an unused convenience” | should be RECORD-L4 stating that **eight shipped rows** use the exposed table: WDT, RTC, two IPRD checks and four SCIF checks. Removing WDT/RTC leaves six consumers | [regress/sh_iprbcd_probe.py:351](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/sh_iprbcd_probe.py:351) contains the IPRD readers; the four SCIF readers follow at line 382 | HIGH confidence
* cpush:F8 | Fable said RECORD-L4 listing `testsh`, `dreamcast` and `hpcsh` as the other SH machines | should be RECORD-L4 also including **`baresh`** | [src/machines/machine_test.c:519](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/machines/machine_test.c:519) defines its setup, line 535 selects SH7750, and line 545 registers it separately; [src/include/machine.h:264](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/include/machine.h:264) assigns its distinct machine identifier | HIGH confidence
* cpualphapalcode:F4 | Fable said RECORD-L4 replacing the claim with “no OSF/1-ABI guest ISSUES an unrecognised selector” | should be RECORD-L4 saying: “The five macros use documented selectors. Privileged callers can supply other selectors, which take the conservative all-invalidation arm.” The universal claim about guests remains unsupported | [src/include/thirdparty/alpha_cpu.h:479](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/include/thirdparty/alpha_cpu.h:479) forwards arbitrary `op`; [src/cpus/cpu_alpha_palcode.c:430](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/cpu_alpha_palcode.c:430) handles other values; [regress/alpha_tbi_probe.py:550](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/alpha_tbi_probe.py:550) begins the shipped boundary cases that issue unrecognised selectors | HIGH confidence
* devlca:F1 | Fable said CONFIRMED-FILED, retaining MED pending an image or executed witness | should be **CONFIRMED-FILED HIGH**, recording the recursion consequence now | [src/devices/dev_lca.c:301](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_lca.c:301) forwards without `PHYSICAL`; [src/cpus/memory_rw.c:245](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/memory_rw.c:245) translates it, and line 587 redispatches devices without a recursion guard. Unbounded re-entry can terminate the emulator. The MED premise at [OUTSTANDING_BUGS.md:310](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/OUTSTANDING_BUGS.md:310) does not override your explicit HIGH rule | HIGH confidence, static derivation

THE RULER'S OWN ADDITIONS (its section (b))
(b) Findings of my own, noticed while checking (mine unless marked; two were raised by the draft check's section (b) and are verified here):
* `pvrpal8888trunc` MED (raised by the check, verified): dev_pvr.c:838 declares `uint16_t c32` and loads a 32-bit palette entry into it, so in `PVR_PALETTE_CFG_MODE_ARGB8888` (:857-861; dreamcast_pvr.h:292) alpha and red are always 0 and `a == 0` takes neither output arm at :871-890 -- every ARGB8888-palette texel renders nothing.  A one-token fix (`uint32_t`).
* RECORD-L4 OUTSTANDING_BUGS.md:14920-14924 (identical at HEAD): the census dated 2026-08-31 says the `dev_pvr.c` `idata != 0x0cff0000` arm "fails the 64-bit compare and the host dies"; that arm (:370-375) has carried `fatal()` without `exit(1)` since #166 (de1398e1, 2026-07-17), six weeks before the census.  The truncated-diagnostic half is still true; the kill is not.  Bracket: "(the arm has been fatal()-only since #166; the truncated diagnostic survives, the kill does not)".
* RECORD-L4 regress/alpha_tbi_probe.py:85-89 FOR-PEER (raised by the check, verified): the ITB/DTB note says BOTH `bnd lo` and `bnd mid` would red under a correct split.  Each row's want string (:571-574) requires `obs_x == x_new`, i.e. X's translation flushed.  Under a correct ITB-only flush (`bnd lo`, a0 = 1) the observing DATA load of X keeps its old translation and the row reds; under a correct DTB flush (`bnd mid`, a0 = 2) the data translation IS flushed and the row stays green.  Only `bnd lo` depends on the unified cache.
* Records nit: the `shsweep` row cites the BL rewrite as `cpu_sh.c:653` (:8145, :8201); it is :917 at 8ea26abb.
* Riders already placed above: regress/sh_iprbcd_probe.py:321-322 (cpush:F6), regress/lca_confbus_probe.py:96-98 (devlca:F5), cpu_sh.c:980-983 and CHANGELOG.md:19280-19281 (cpush:F2), cpu_sh.c:985-989 (cpush:F3), cpu_ppc.c:1939 (cpuppc:F2), cpu_alpha_palcode.c:379-383 (cpualphapalcode:F2).

---

## Batch 3c -- cpuarm, cpuarminstrloadstore, dev8253, devfootbridge (27 findings).
## Ruled by Fable (claude-fable-5-1, first-hand): 4 confirmed-new, 12 confirmed-filed, 8 record-L4, 2 test-gap, 0 refuted, 0 unsettled, 1 duplicate, of 27 findings (adjudication/fable_batch3c.md).
## Astra: 0 of 27 dispositions wrong (5 more need a change of wording or severity) (adjudication/codex_astraconfirm_3c.txt).  Mechanically assembled (mk_disp.py): every line below is VERBATIM from
## one of those two files; where an Astra amendment touches a finding, the AMENDMENT governs.

RULINGS (each finding's disposition statement, up to its `Checked:` line)
* **cpuarm:F1 | CONFIRMED-FILED OB-24** -- LOW.  Six residual promoted-`int` `byte << 24` assemblies remain in `cpu_arm.c`: the Thumb interpreter's PC-relative load (`:1562`/`:1564`, buffer `uint8_t word[4]` at `:1263`) and SP-relative load (`:1634`/`:1636`), and the disassembler's loaded-value annotation (`:2482-2486`, `unsigned char tmpw[4]` at `:2463`); the instruction-word fetch at `:1858-1860` already uses `misc.h:203-206`'s cast-before-shift macros, so `#45` fixed the fetch and left these siblings.  `OUTSTANDING_BUGS.md:2916` files `OB-24` as "`cpus/*` ... residual signed `byte<<24` UB" -- Astra's "no matching filing" is wrong.  One sharpening Astra missed: `:1562` and `:1634` are EXECUTION paths (any Thumb guest loading a word with bit 31 set reaches them), not annotation paths needing tracing; still LOW -- language-level, no host pointer, size or index is fed.
* **cpuarm:F2 | CONFIRMED-FILED OUTSTANDING_BUGS.md:2097-2109 (prose, no id) -- propose `armcachegeom`, MED.**  `arm_cpu_types.h:78` gives ARM1136JSR1 `12, 1, 0, 1` (field order `cpu_arm.h:44-47`: icache_shift, iway, dcache_shift, dway), so `cpu_arm.c:158-172` assembles D-size 0, D-assoc 5, D-line 2 -> `0x0b02a0ea`.  Per DDI 0100I B6.6.3 (`ddi0100i.txt:32275,32292,32313,32328,32336`) that is a 512-byte, 32-way, 32-byte-line D-cache with NSETS exponent 0+6-5-2 = -1, which the manual calls invalid.  The I-cache half (size 3: 4 KB, exponent 2) is consistent.  The queue already records "a size field of 0 means a 512-byte cache, not 'unspecified'", the ignored `iway`/`dway`, the 3-bit wrap and the v6 format difference -- that entry IS the filing; it has no id.  MED by the rule: the register is guest-readable (`cpu_arm_coproc.c:79-80`) and encodes a geometry no hardware reports.  **L4 rider (...
* **cpuarm:F3 | RECORD-L4** -- LOW.  `CHANGELOG.md:21344-21345` says "The register is still marked 'aren't used yet' in the source, so nothing observable to a guest changes today."  The source note (`cpu_arm.c:163`) is about the table's `iway`/`dway` fields; the register itself is returned to the guest by `MRC p15,0,Rd,c0,c0,1` (`cpu_arm_coproc.c:79-80`), so the change from `0xffdea0ea` to `0x0b02a0ea` is guest-visible on the 32 affected CPUs.  Replace with: "The 'aren't used yet' note in the source is about the table's `iway`/`dway` fields, not about the register: a guest reads the Cache Type register directly (`MRC p15,0,Rd,c0,c0,1`; `cpu_arm_coproc.c`'s case 1 returns `cachetype`), so the value change from 0xffdea0ea to 0x0b02a0ea IS guest-visible on the 32 affected CPUs.  What the guest now reads is a well-formed encoding of the table's data; that the data encodes an impossible D-ca...
* **cpuarm:F4 | RECORD-L4** -- LOW.  `CHANGELOG.md:32804-32808` says Thumb is never entered by a debugger T-bit write because "a debugger write reaches `cpsr` but not the separate `flags` field the handlers read, so it would preset nothing."  `cpu_dyntrans.c:255` dispatches on `cpu->cd.arm.cpsr & ARM_FLAG_T` directly and `cpu_arm.c:196` registers `cpsr` for the debugger, so a debugger write DOES set T; the flags-field separation concerns NZCV only.  The real reason is `cpu_arm.c:1216`: the interpreter stops the CPU unless `pc` is odd AND T is set, and `bx` is what establishes both.  `arm_flags_probe.py:1253-1261` already says so; the CHANGELOG does not.  Replace with: "Thumb is entered **architecturally** here -- an ARM `bx` to an odd address sets `ARM_FLAG_T` and leaves the low bit in `pc`, and `cpu_dyntrans.c` dispatches to the interpreter -- and not by writing the T bit with the debu...
* **cpuarm:F5 | TEST-GAP-FILE `thumbrorstale`** -- LOW.  `arm_flags_probe.py:1506-1509`: both `T RORS clears Z` and `T RORS clears N` pass `cin=1`; `run_thumb` (`:1327-1332`) presets flags with `SUBS r8, r8, r9` on `(1, 0)`, result 1, so N=0 Z=0 C=1 on entry.  The `#329` repair under test is `cpu_arm.c:1454-1455` (clear Z|N before re-deriving); with the pre-fix OR-only form a preset of N=0 Z=0 yields exactly the expected flags for both rows (0x81234567 -> N1 Z0; 0x00000001 -> N0 Z0), so deleting the clear passes both.  The SHIFT_ROWS table (`:1500-1527`) has no other ROR row, and `gate_arm.sh:360` names only these two.  Cheap partial repair: `cin=0` on the N row presets `SUBS 0-1` -> N=1 (and C=0, which that row wants anyway); a stale-Z preset needs an equal-operand SUBS the fixture does not offer.  **L4 rider:** the fixture comment at `:1504-1505` ("Z stale after an equal compare, N st...
* **cpuarminstrloadstore:F1 | CONFIRMED-NEW MED `armabortdest` "A faulting word load zero-fills its destination after Data Abort entry (LE hosts)".**  `cpu_arm_instr_loadstore.c:123-124`: for a word LOAD on a little-endian host the buffer IS the destination register (`data = (unsigned char *) ic->arg[2]`, the `#372` alias).  `:233-234` calls `memory_rw`; on a translation failure `memory_arm.c:271-273` raises `ARM_EXCEPTION_DATA_ABT` -- `cpu_arm.c:669-733` saves the bank, switches to ABT32, loads the ABT bank, writes `r[LR] = retaddr` and `r[PC] = vector` -- and then, back in `memory_rw.c:259-268`, the `#244` zero-fill runs `memset(data, 0, 4)` on `&r[Rd]` and returns failure.  Consequences by Rd (the decoder puts `&r[rd]` in `arg[2]` for every load including Rd=PC, `cpu_arm_instr.c:4719`): r0-r12 lose the value the architecture requires preserved (`ddi0100i.txt:2316`: "the value in that...
* **cpuarminstrloadstore:F2 | CONFIRMED-FILED OB-24** -- LOW.  `:259-260` (general word load, both byte orders) and `:494-502` (fast-path word load) shift promoted `data[i]`/`page[i]` by 24 without the `(uint32_t)` casts the LDRD arm uses at `:280-289`.  `OUTSTANDING_BUGS.md:2916` names this very file for `OB-24`.  Different sites from cpuarm:F1 under one umbrella row.
* **cpuarminstrloadstore:F3 | CONFIRMED-NEW MED `armliteralrot` "Same-page PC-relative LDR shortcut assembles the unaligned bytes and skips the U=0 rotation".**  `cpu_arm_instr.c:4739-4773`: for `ldr Rd,[pc,#+/-imm]` whose target lies in the current page, the decoder replaces the load handler by a `mov` of a constant read at translation time with `memcpy(cbuf, p + (a & 0xfff), 4)`, `a` NOT word-aligned, then `cbuf[0] + (cbuf[1]<<8) + ...`.  The template the shortcut stands in for masks to the aligned word and rotates by `8 * addr[1:0]` (`cpu_arm_instr_loadstore.c:490-505`, the `#362` fix), as A4.1.23 requires for U=0 (`ddi0100i.txt:8248-8249`).  Worked case, little-endian, bytes 11 22 33 44 55 from aligned P: `ldr` at P+1 gives 0x55443322 through the shortcut and 0x11443322 through the template.  So the same instruction yields two different values depending on whether the page was warm ...
* **cpuarminstrloadstore:F4 | DUPLICATE-OF-ROW armalignexc.**  `DISPOSITIONS.md:164-166` assigned `armalignexc` (MED) to `OUTSTANDING_BUGS.md:1256-1264` ("`ARM_CONTROL_ALIGN` is initialised enabled but never enforced ... an alignment exception is owed"); `:4139-4145` records the same (A is "decorative", read only to be printed at `cpu_arm_coproc.c:144-147`).  Confirmed in this file: `:229` (`addr &= ~(datalen - 1)`) and the fast-path masks at `:474`, `:492`, `:513`, `:522` run with no test of `ARM_CONTROL_ALIGN`, which `cpu_arm.c:128-129` sets at reset.  What this finding adds to the row: the load/store template is a third unenforced site beside the block-transfer paths and the coproc print, and `cpu_arm.c:129`'s reset value contradicts the SA-1110 reset state the queue quotes.
* **cpuarminstrloadstore:F5 | CONFIRMED-FILED OUTSTANDING_BUGS.md:5140-5144 (prose, task "#74 the ARMv6 U=1 ~7 mask") -- propose `armdwordalign`, MED.**  `:99-101` sets `datalen = 8` for LDRD/STRD and `:229` masks with `~7`; A4.1.26/A4.1.102 (`ddi0100i.txt:8507-8511,14533-14538`) permit word alignment when U=1 and access `address` and `address+4`.  U=1 is reachable: `cpu_arm_coproc.c:135` stores the whole guest control word, so the absence of an `ARM_CONTROL_U` macro means the model never READS the bit, not that the guest cannot SET it.  Requested 0x10004/0x10008 become 0x10000/0x10004.  One of the U=1 class (see F7 and (b) below); the numbered task is the filing.
* **cpuarminstrloadstore:F6 | CONFIRMED-FILED OUTSTANDING_BUGS.md:5142-5143 and :5093-5097 (prose, task "#76 odd-Rd UNDEFINED") -- propose `armoddpair`, MED.**  The mode-3 decoder `cpu_arm_instr.c:4345-4380` tests only `rd == ARM_PC || rn == ARM_PC` (`:4351`); an odd Rd reaches the pair transfer at `cpu_arm_instr_loadstore.c:278-289` / `:344-362`, where A4.1.26/A4.1.102 (`ddi0100i.txt:8478-8480,14503`) make the instruction UNDEFINED.  No host bound is crossed: Rd=15 is redirected to `tmp_pc_data[2]` by `#390`, and Rd=13 pairs r13/r14.  MED (an owed exception, guest-visible).
* **cpuarminstrloadstore:F7 | RECORD-L4** -- LOW.  `cpu_arm_instr_loadstore.c:210-214`, `CHANGELOG.md:30917-30921` and `OUTSTANDING_BUGS.md:3610-3613` say that under v6+ with U=1 "masking and rotating are wrong equally -- so this is never worse than what it replaces, in any combination."  Per input that is false: aligned P holding 11 22 33 11 22 33 11, loaded at P+3 with U=1, requires 0x11332211; mask-only returns 0x11332211 (right by coincidence); mask-plus-ROR24 returns 0x33221111.  The DECISION (unconditional rotation, recorded divergence) stands; the dominance sentence does not.  Replace the sentence, in all three places, with: "Rotation is the architected result for ARMv3/v4/v5 and for v6+ with U == 0.  For v6+ with U == 1 the architecture wants a true unaligned access, which NEITHER masking nor masking-plus-rotation implements: each returns the required word only by coincidence of...
* **dev8253:F1 | CONFIRMED-FILED `pitclobber` (OUTSTANDING_BUGS.md:6793-6797) = `pitmodebyteshared` (:20787-20799)** -- MED.  `dev_8253.c:78` declares one scalar `mode_byte`; `:310` is its only writer, for whichever counter the control word selects; `:166`, `:259` and `:280` read it as the format of whichever counter is being accessed.  So after counter 1 is programmed LSB-only, counter 0's accesses are decoded LSB-only (low byte twice; a latched read releases after one byte).  `i8254.txt:234-235` ("The format of the initial count is determined by the Control Word used") and `:351-357`.  **Records finding:** the queue carries this ONE defect under TWO ids, filed four weeks apart; the records round should keep one (the `pitmodebyteshared` write-up is the fuller; `pitclobber` is the earlier sighting) and cross-reference the other -- Astra correctly named both.
* **dev8253:F2 | CONFIRMED-FILED `pit8253lsbnotimer` (OUTSTANDING_BUGS.md:19833,19860-19888).**  `dev_8253.c:174-177`: the LSB arm writes the low byte and `break`s; only the MSB arm (`:178-203`) recomputes `hz[]` and calls `timer_add`/`timer_update_frequency`.  A counter programmed RW=01 (`i8254.txt:219`) never starts, or keeps its old rate.  The queue entry states exactly this, both halves.  By the brief's rule this is MED (guest-visible: no interrupts / wrong rate; the emulator makes progress); the queue's MED-HIGH weighs guest impact -- noted, not changed here.
* **dev8253:F3 | CONFIRMED-FILED `pit8253lsbnotimer` (OUTSTANDING_BUGS.md:19838-19853, the WIDENED half).**  `:175` keeps the stale MSB (`&= 0xff00`), `:179` keeps the stale LSB (`&= 0x00ff`); `:310-321` clears neither at the control word, where `i8254.txt:168-172` says CRM and CRL are cleared ("the other byte will be zero").  Astra's arithmetic holds: prior 0x12ff, MSB-only 0x10 -> model 0x10ff (4351, 274 Hz) vs required 0x1000 (4096, 291 Hz) at `I8253_TIMER_FREQ` 1193182 (`i8253reg.h:75`, rounding at `dev_8253.c:181-184`).  The queue says "the composed count is WRONG IN BOTH ARMS" and names the fix site.
* **dev8253:F4 | CONFIRMED-FILED `pit8253bcdbinary` (OUTSTANDING_BUGS.md:19918-19938)** -- MED.  `:339-343` only announces BCD; `:310` keeps the bit; `:181-184` divides by the binary value.  BCD 0x9999 -> 39321 -> 30 Hz where decimal 9999 -> 119 Hz (`i8254.txt:213-216`).  The queue has the same worked example and already corrected the grade to MED by reach.
* **dev8253:F5 | RECORD-L4** -- LOW.  `CHANGELOG.md:20046` (a table row): "five guest-writable i8253-timer paths (DMA-refresh TODO, latch-mode msb/lsb, BCD-mode, unimplemented offset) warn and continue".  The five `#223` sites are `dev_8253.c:198-199` (write), `:204-207` (write `default`), `:270-273` (a READ `default`), `:339-343` (write), `:350-357` (the outer `default`, which no access reaches: `DEV_8253_LENGTH` is 4 at `:70`, registered once at `:386-388`, `memory_rw.c:480-494` hands the handler `relative_addr` in {0,1,2,3}, and all four have cases -- `OUTSTANDING_BUGS.md:19630-19635` already calls it dead code).  "Latch-mode msb/lsb" also misdescribes the two `default:` arms, which fire when no RW format has been programmed (`rw == 0`).  Replace the row's second clause with: "five `exit(1)` sites warn and continue -- the counter-1 DMA-refresh TODO, a count WRITE and a count READ to ...
* **dev8253:F6 | RECORD-L4** -- LOW.  `CHANGELOG.md:25262-25267` says "across the ordinary two-read `gettick()` the two designs are indistinguishable ... which is why #439's measured behaviour is unchanged".  Checked against BOTH sources: `#439`'s arm (`git show 020a672f:src/devices/dev_8253.c`, `:172-174`) is `odata = 0; break;` -- 0 for every latched read regardless of parity; HEAD's arm (`:218,259-261,280-285`) releases on `rw == MSB` and toggles `rd_msb`, so a pair entered at odd parity reads 00 then the live low byte: 0x9c00 for the 0x2e9c example where `#439` gave 0x0000.  The CHANGELOG's own pass-2 note at `:25354-25359` and the source at `:236-247` record this; the original sentence stands unqualified.  Replace with: "**This corrects #439's stated reasoning where the two fixes meet.** #439's read arm took an early `break` 'so no counter byte was consumed, leave the selector alon...
* **dev8253:F7 | TEST-GAP-FILE `pitonebytelatch`** -- LOW.  `dev_8253.c:259-261` releases a latch after ONE read whenever the programmed format is not 16-bit.  Every latch-issuing arm in `regress/pit8253_latch_probe.py` (D/F/T via `body` `:138`, L via `body_latch` `:268`, M via `body_mid` `:299`; W/X use `body_rewind` with 0x34/0xb6) programs RW=11; `regress/lca_isalane_probe.py:1256-1378` uses 0x34/0x74/0xb4 (all RW=11) and issues no latch.  So the one-byte release branch that `#440`'s "consumed per the programmed format" claims has no row.  One row per single-byte format (CW 0x14 or 0x24, latch, read, read: the second read must be live) would discharge it.  `pitlatch2` (`OUTSTANDING_BUGS.md:6907-6908`) is a different question (does the latch rewind the flip-flop).
* **devfootbridge:F1 | CONFIRMED-NEW MED `fbpcibus255zero` "A PCI-config read decoding to bus 255 returns 0, not the no-device answer".**  `dev_footbridge.c:486-491`: after `bus_pci_setaddr`, bus 255 prints and `return 1` BEFORE `bus_pci_data_access()` (`:498-499`) and before the read writeback (`:501-502`); `memory_rw.c:491-492` has pre-zeroed the buffer, so the guest reads 0.  Everywhere else an absent device answers all ones for the vendor-ID word (`bus_pci.c:110-113`), which is what the datasheet gives for a configuration read that master-aborts (`dc21285.txt:1825`).  Reachable: the config window is 16 MB (`:904-906`) and `bus_pci_decompose_1` takes the bus from bits 23:16 (`bus_pci.c:74`).  MED; no filing by `bus 255`/`bus255` in the queue, none in DISPOSITIONS.  Rider: the `fatal()` at `:487-488` is unlatched -- a guest polling bus 255 floods the log (`floodclass`; check it is not...
* **devfootbridge:F2 | CONFIRMED-NEW MED `fbexternalclock` "TIMER_EXTERNAL runs the timer from the internal clock; hardware counts irq_in_l edges".**  `footbridge_effective_cycles()` (`:248-261`) returns the unprescaled load for bits 3:2 = 11; `reload_timer_value()` (`:274-277,339-348`) then requests `emulated_hz / load` (or `/ 2^24` for a zero load, `:239-240`; clamped at `timer.c:131`) and the timer core repeats it (`timer.c:283-285`).  The datasheet (`dc21285.txt:4124-4127`) advances an external-mode timer by one count per assertion edge on `irq_in_l[n]`, a pin this model has no signal for -- so a conforming guest selecting external mode gets ticks the hardware would not produce.  Astra's "selecting ... creates a repeating timer" is right via the LOAD write (`:663-664` reloads unconditionally); the CONTROL write path schedules only with `TIMER_ENABLE` set (`:695-699`).  Not filed: th...
* **devfootbridge:F3 | CONFIRMED-FILED `fiqenableread` (OUTSTANDING_BUGS.md:21826, :21982-21985 facet 1).**  `:649-652` handles only `MEM_WRITE`; a read falls through with `odata = 0` (`:511`) to `:777-778`.  The IRQ sibling at `:600-607` reads back (`#539`).  `dc21285.txt:6831,6911-6924`: FIQEnable at 288h is a readable register.  MED by the rule (documented readable state returned wrong); the queue grades the five-facet row LOW -- noted.
* **devfootbridge:F4 | CONFIRMED-FILED `fbm2findings` (OUTSTANDING_BUGS.md:21991-21993, "periodic CLEAR reload").**  `:719-722`: any CLEAR write with `TIMER_MODE_PERIODIC` set calls `reload_timer_value()`, which sets `timer_value = timer_load` (`:279`) and re-adds or re-times the host timer (`:339-348`), before and independently of the pending test at `:724` and of `TIMER_ENABLE`.  `dc21285.txt:7139-7140`: the write "has no effect if the associated interrupt was already clear".  Guest-visible through `TIMER_1_VALUE` reads (`:672-674`).  MED by the rule; it sits inside a LOW "records" bundle -- if it is to be fixed it wants its own id, but it IS filed.
* **devfootbridge:F5 | CONFIRMED-FILED `fbcsrdecodelanes` (OUTSTANDING_BUGS.md:21979-21980).**  A byte read at `+0x189` misses the timer fold (`:517-520`), misses every `case` in the exact-offset `switch` (`:522`), reaches `default:` (`:768-770`) and returns the zero `odata`; hardware selects the CSR by A[10:2] (`dc21285.txt:1651-1653`) and the SA-110 takes lane 1, so with enable bit 8 set the byte is 1.  `IRQ_ENABLE` is 0x188 (`dc21285reg.h:334`); `footbridge_sites_probe.py` E3/E6 (`:125-128,283-285`) exercise only `+0x188` and `:167-169` discloses the lanes.  The queue entry is exact (measured at +0x189).  MED by the rule; queue LOW -- noted.  The `default:` arm's `fatal()` is unlatched (same flood rider as F1).
* **devfootbridge:F6 | RECORD-L4** -- LOW.  `CHANGELOG.md:20043`: "a PCI-config access decoding to bus 255 reads as no-device instead of `exit(1)`".  It does not read as no-device: the early return at `:491` skips `bus_pci_data_access()` and the writeback, so a read returns the pre-zeroed buffer, where the model's no-device answer for the vendor-ID word is all ones (`bus_pci.c:112-113`).  Replace the clause with: "a PCI-config access decoding to bus 255 announces itself and returns handled instead of `exit(1)` -- WITHOUT going through `bus_pci_data_access()` or the read writeback, so a read there returns the pre-zeroed buffer (0), not the no-device answer the model gives elsewhere (all ones for the vendor-ID word).  Filed as `fbpcibus255zero`."
* **devfootbridge:F7 | RECORD-L4** -- LOW.  `dev_footbridge.c:257-260` ("is genuinely not derivable here and is NOT invented: the unprescaled period keeps the timer sane"), `:690-694` ("UNKNOWN and is NOT invented") and `CHANGELOG.md:26002-26003` ("so it is not invented").  The code supplies a rate -- `fclk_in / load` -- for a mode in which the hardware counts external edges; what is not invented is an external RATE, but a behaviour is substituted, and the records should say so.  Replace `:257-260` with: "The RATE an external source would give depends on a pin this model has no signal for (irq_in_l): the hardware advances the counter once per assertion edge (datasheet 6.4, dc21285.txt:4124-4127) and would not advance at all with no edges.  That is not derivable here, so this SUBSTITUTES the unprescaled internal period -- fclk_in / load, or / 2^24 for a zero load, clamped by the timer co...
* **devfootbridge:F8 | RECORD-L4** -- LOW.  (Changed from the draft's FILED-BY-PROSE `fbzerowraprecord`; the check's WRONG verdict is right.)  `CHANGELOG.md:26021-26025` still rests the zero-load mapping "on arithmetic (the 24-bit mask aliases a legitimate write of `0x1000000` to zero, so full-period is the unique choice that keeps the rate continuous across the register's own truncation)".  `dc21285.txt:7073-7079`: TimerNLoad bits 23:0 are R/W and 31:24 "Read only as 0" -- bit 24 is outside the writable field.  The source withdrew the argument (`dev_footbridge.c:192-200`: "There is no wrap to be continuous across") and `OUTSTANDING_BUGS.md:6196-6209` is a RECORDS CORRECTED note recording that withdrawal as DONE; it files nothing, and a note that a correction was made is not a queue row for the sentence it missed (DISPOSITIONS.md:399's precedent: a closed row is not a filing).  The live...

ASTRA'S AMENDMENTS (5)
* **cpuarm:F3** | Fable said RECORD-L4, with `0xffdea0ea → 0x0b02a0ea` applying to all 32 affected entries | should remain RECORD-L4, but scope that numeric example to ARM1136JSR1. All 32 change observably; they do not all produce the same value | [arm_cpu_types.h:61](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/include/arm_cpu_types.h:61) and [:88](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/include/arm_cpu_types.h:88), combined with [cpu_arm.c:160](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/cpu_arm.c:160), give `0x0b02a12a` for ARM740T8K and `0x0b02a1ea` for the PXA entries | confidence: high.
* **cpuarm:F4** | Fable said RECORD-L4, replacing the explanation with BX being “the one operation” establishing odd PC and T together | should remain RECORD-L4; say “The probe’s BX establishes both conditions together in one guest instruction.” The uniqueness claim is too broad | BLX also establishes both: [cpu_arm_instr.c:445](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/cpu_arm_instr.c:445) and [:486](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/cpu_arm_instr.c:486) | confidence: high; wording only.
* **cpuarminstrloadstore:F7** | Fable said RECORD-L4, with rotation unconditionally described as architected for the listed architectures/U settings | should remain RECORD-L4, but qualify the replacement with **alignment checking disabled (`A=0`)** and otherwise valid accesses. With `A=1`, an unaligned access requires an alignment Data Abort. The U=1 explanation needs the same qualification | [OUTSTANDING_BUGS.md:1262](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/OUTSTANDING_BUGS.md:1262); [cpu_arm.c:129](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/cpu_arm.c:129) actually initializes A enabled | confidence: high.
* **devfootbridge:F2** | Fable said CONFIRMED-NEW MED `fbexternalclock`, because the external input is “a pin this model has no signal for” | should remain CONFIRMED-NEW MED, but describe **missing timer consumption of external interrupt edges**, not missing input signals | [dc21285reg.h:305](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/include/thirdparty/dc21285reg.h:305) defines the inputs; [dev_footbridge.c:832](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_footbridge.c:832) registers their handlers, and [:385](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_footbridge.c:385) receives assertions without advancing timers | confidence: high.
* **devfootbridge:F7** | Fable said RECORD-L4, retaining “a pin this model has no signal for” in its replacement | should remain RECORD-L4, with: “The model exposes the external interrupt inputs, but its timers do not count their assertion edges; external mode instead substitutes the internal timer cadence.” Apply that correction to the proposed CHANGELOG replacement too | [dev_footbridge.c:857](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_footbridge.c:857) connects actual ISA sources to those inputs; [:248](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_footbridge.c:248) implements the internal-clock substitution | confidence: high.

THE RULER'S OWN ADDITIONS (its section (b))
## (b) Findings Astra missed (mine, each checked at 8ea26abb)

* **`fbsdrampair` is graded LOW and is HIGH by the brief's rule.**  `dev_footbridge.c:732-735` and `:757-760`: a guest READ of SDRAM_BA_MASK or SDRAM_BA_OFFSET reaches `fatal()` + `exit(1)` -- the emulator process ends on a guest-controlled read.  `OUTSTANDING_BUGS.md:21966-21972` knows they are two of the seven remaining exits and still says LOW.  Regrade the existing row HIGH; no new id.  (The check's (b) raised this; verified here.)
* **Stale queue prose on the PIT probe.**  `OUTSTANDING_BUGS.md:6810-6815` ("`pit8253_latch_probe.py` still ships UNWIRED into any gate") and the `witnessunwired` held row at `:6877-6878` ("runs in no gate") are overtaken: `gate_arm.sh:1787-1799` at `8ea26abb` runs the probe and checks its `PIT8253_LATCH_DONE` sentinel, wired by `105c15c7` (#496, 2026-08-30) and `e363582a` (#497 pass 2).  L4: date-bracket both passages; `witnessunwired`'s premise no longer holds for this probe (its general class may still).
* **The U=1 siblings** (halfword loads/stores `:474`/`:513`, word stores `:522`, all masked down where ARMv6 U=1 wants raw-address accesses, `ddi0100i.txt:3046-3050,8674-8675,14724-14725`) are the same modelling gap as the recorded divergence at `OUTSTANDING_BUGS.md:3617-3618` and as `#74`; named in the cpuarminstrloadstore:F7 replacement, no separate row.
* **The `#244` zero-fill reaches other architectures' aliases only if they alias.**  Not checked here (out of this batch's files); a fix round for `armabortdest` should grep the other `*_instr_loadstore.c` templates for a `data = ... ic->arg[2]` alias before calling it ARM-only.
* **Two unlatched guest-drivable `fatal()`s** in the footbridge (`:487-488` bus 255; `:768-774` the CSR `default:`, which the `fbcsrdecodelanes` lane reads traverse) -- `floodclass`; check against existing floodclass rows before filing.

---

## Batch 3g -- memoryrw, debuggercmds, debugmsg, bundle_debugger, symbol, bundle_console, emul (23 findings).
## Ruled by grok (grok-4.7 xhigh, first-hand): 8 confirmed-new, 1 confirmed-filed, 8 record-L4, 4 test-gap, 0 refuted, 0 unsettled, 2 duplicate, of 23 findings (adjudication/grok_20261002/grok_rule3g.txt).
## Astra: 0 of 23 dispositions wrong (1 more need a change of wording or severity) (adjudication/codex_astraconfirm_3g.txt).  Mechanically assembled (mk_disp.py): every line below is VERBATIM from
## one of those two files; where an Astra amendment touches a finding, the AMENDMENT governs.

RULINGS (each finding's disposition statement, up to its `Checked:` line)
* memoryrw:F1 | CONFIRMED-NEW MED subpagecache "A 1 KB guest page is cached as a full host page"
* memoryrw:F2 | CONFIRMED-NEW MED ramnulltail "A read that starts in an unallocated memblock zeroes the whole request, including a later allocated memblock, and returns success"
* memoryrw:F3 | CONFIRMED-FILED ramspaninval
* memoryrw:F4 | RECORD-L4 "Show the store (writer pc, target, width, value) and request debugger entry when the emulation loop next consumes about_to_enter_single_step; further guest instructions may execute before entry. NOP unless a watchpoint is set."
* memoryrw:F5 | RECORD-L4 "A nonfinal worker failure zeroes this chunk and the unprocessed suffix; earlier successful bytes remain. This is not #244's whole-buffer zero."
* memoryrw:F6 | RECORD-L4 "The memblock split fires at 1 MiB boundaries, one boundary per 1,024 split granules. Without the exemption, an aligned 16 MiB transfer would require 16,384 worker calls at the 1 KiB granule."
* memoryrw:F7 | RECORD-L4 "(The worker's host-page granule is 8 KB under MEM_ALPHA and 4 KB otherwise; the split granule is 1 KB.)"
* memoryrw:F8 | RECORD-L4 "Post-#430, the memblock split can be reached by PHYSICAL accesses or when translate_v2p is NULL; translated accesses are split at the 1 KB granule first."
* debuggercmds:F1 | CONFIRMED-NEW LOW dbgexprambig "Breakpoint and watchpoint adds treat PARSE_MULTIPLE as success and then read the output"
* debuggercmds:F2 | CONFIRMED-NEW LOW findaddrwrap "Debugger memory search can wrap its scan address into low addresses"
* debuggercmds:F3 | CONFIRMED-NEW LOW findcountovf "Debugger search counts matches and unreadable chunks in unbounded signed ints"
* debuggercmds:F4 | DUPLICATE-OF-ROW include2:F5
* debuggercmds:F5 | TEST-GAP-FILE LOW dbgignorow "No committed row observes breakpoint ignore-count stops"
* debuggercmds:F6 | TEST-GAP-FILE LOW mipsbpnormrow "No committed row observes MIPS breakpoint sign-extension of an unextended address"
* debugmsg:F1 | RECORD-L4 "The override semantics are deliberately unchanged (panel-unanimous); the listing now states them explicitly. ARC's NE2000 transmit of an unimplemented IPv4 broadcast reaches debugmsg(SUBSYS_NET, ..., VERBOSITY_ERROR) through net_ethernet_tx. The caller gate is ENOUGH_VERBOSITY(SUBSYS_NET, VERBOSITY_ERROR), and the default verbosity is INFO (2), so the call is made. Clearing the net breakpoint does not clear debugmsg_break_on_error, so the global override still requests debugger entry."
* debugmsg:F2 | TEST-GAP-FILE LOW subsysbprow "No committed row arms a subsystem breakpoint and observes debugger entry"
* debugmsg:F3 | TEST-GAP-FILE LOW dbglisterow "No committed row observes the global break-on-ERROR listing after one subsystem is cleared"
* bundle_debugger:F1 | CONFIRMED-NEW LOW stepcallfocus "Changing machine focus leaves step-call running cached untraced handlers"
* symbol:F1 | DUPLICATE-OF-ROW symdemanglebound
* bundle_console:F1 | CONFIRMED-NEW HIGH x11alloc32 "X11 resize allocation wraps when size_t is 32 bits, inside the 16384 cap"
* bundle_console:F2 | RECORD-L4 "On a pipe, every character now marks stdout pending for the next console_flush(); the periodic check uses the first machine's bootstrap CPU instruction counter, so it does not guarantee a per-burst instruction bound when that CPU stops progressing."
* emul:F1 | CONFIRMED-NEW HIGH emulgzipfail "A gzip load that fails to decompress terminates the process"
* emul:F2 | RECORD-L4 "**#42** prefer /bin/gunzip and /usr/bin/gunzip, with a PATH lookup fallback and the inherited environment retained, plus the fd != STDOUT_FILENO close guard and the -- option-injection guard"

ASTRA'S AMENDMENTS (1)
* `memoryrw:F5 | grok said RECORD-L4 “A nonfinal worker failure zeroes this chunk and the unprocessed suffix” | should be RECORD-L4 “On a read, a nonfinal worker failure zeroes the failed chunk and unprocessed suffix; earlier successful bytes remain. This is not #244’s whole-buffer zero.” | src/cpus/memory_rw.c:214 guards the memset with writeflag == MEM_READ; :220 advances the buffer after successful chunks. Failed writes do not receive that zeroing. The retained disposition is correct, but its replacement needs the read qualifier. | confidence HIGH`

THE RULER'S OWN ADDITIONS (its section (b))
**(b)** Mine, not one of the 23. `emul.c:600–603` calls `exit(1)` when `mkstemp` fails. That is host temporary-directory failure. Propose LOW `emulmkstempexit`. `x11.c:632` is the second site of `x11alloc32`. `OUTSTANDING_BUGS.md:5697` still says the split "fires 256x more often", and `regress/diff_memory_rw.c:460–462` still says a 16 MB access "reads 4096"; both should say 1024 per memblock and 16384 calls. The pin at `:490` is already 16384. The agy and codex checks' "phantom symbol at address 0" does not survive `symbol.c:224`.

---

## Batch 3f -- devne2000, netip, net, bundle_net, devjazz (24 findings).
## Ruled by grok (grok-4.7 xhigh, first-hand): 15 confirmed-new, 3 confirmed-filed, 5 record-L4, 0 test-gap, 0 refuted, 1 unsettled, 0 duplicate, of 24 findings (adjudication/grok_20261002/grok_rule3f.txt).
## Astra: 0 of 24 dispositions wrong (5 more need a change of wording or severity) (adjudication/codex_astraconfirm_3f.txt).  Mechanically assembled (mk_disp.py): every line below is VERBATIM from
## one of those two files; where an Astra amendment touches a finding, the AMENDMENT governs.

RULINGS (each finding's disposition statement, up to its `Checked:` line)
* devne2000:F1 | CONFIRMED-NEW LOW ne2krxbudget "Enabled NE2000 reception with an invalid ring has no per-tick packet budget"
* devne2000:F2 | CONFIRMED-NEW MED ne2ktsrstale "A rejected transmit leaves the previous TSR value"
* devne2000:F3 | CONFIRMED-NEW MED ne2kdmacmd "Remote DMA follows the CPU access, not the CR command"
* devne2000:F4 | CONFIRMED-NEW MED ne2kzerordc "Reissued exhausted remote-DMA command does not complete at the command write"
* devne2000:F5 | CONFIRMED-NEW MED ne2kparsync "A page-1 PAR write does not update the address the backend filters on"
* devne2000:F6 | CONFIRMED-NEW MED ne2krxfilter "RCR accept-broadcast and accept-multicast are stored and never applied"
* devne2000:F7 | CONFIRMED-NEW MED ne2krxfcs "Receive reserves four FCS bytes and never writes them"
* devne2000:F8 | CONFIRMED-NEW MED ne2kloopback "TCR and DCR loopback bits are stored and transmit still leaves the card"
* devne2000:F9 | CONFIRMED-NEW MED ne2krxphy "Every stored receive status is PRX with PHY clear"
* devne2000:F10 | CONFIRMED-NEW MED ne2kmontally "Monitor mode frees frames and the missed-packet tally reads as zero"
* netip:F1 | CONFIRMED-FILED tcpdebugopts
* netip:F2 | CONFIRMED-NEW LOW netipurgptr "TCP reply checksum covers an urgent pointer the reply never stores"
* netip:F3 | CONFIRMED-NEW LOW netipseqarith "TCP sequence difference is a signed subtraction before the mismatch reject"
* netip:F4 | CONFIRMED-NEW LOW netipbcastmask "Broadcast mask shifts a signed 1 by an accepted prefix"
* netip:F5 | RECORD-L4 "Source comment replacing net_ip.c:1027-1030: #177: the request debug dump's fixed reads stop at packet[33]; bytes from 34 are logged only while i < len. The later field dump, including packet[85], runs after packet = lp->data on the 307-byte reply. Frames shorter than 278 bytes are rejected before the memcpy of the request. The len < 86 guard does not protect a fixed request read of packet[85]. Changelog: keep the Fifteenth-round sentence at CHANGELOG.md:19890-19893, and append: Annotation at 8ea26abb: the DHCP debug over-read clause for #177 does not match the dumps in that tree. The request dump's fixed reads stop at packet[33] and then use i < len. packet[85] is read only after packet = lp->data, on the allocated reply. At 39748e3c the text packet[85] does not occur in src/net/net_ip.c; at de1398e1a the only occurrence is this comment."
* net:F1 | RECORD-L4 "The callers guarantee an Ethernet-frame length of at least 20 bytes; after removing the 14-byte Ethernet header, this function may receive a 6-byte body. Reject bodies shorter than 28 bytes before fixed-field accesses or debug output."
* net:F2 | RECORD-L4 "Keep the #119 cell at CHANGELOG.md:19818, including the device files, and append: Correction, net/net.c at 8ea26abb: the ARP path (net.c:195) and the RARP path (net.c:221) each use one WARNING-level debugmsg, and the once-only latch is set after the call returns even when debugmsg returns without printing because verbosity is below WARNING and no subsystem breakpoint or single-step is active."
* bundle_net:F1 | CONFIRMED-NEW LOW taprxquota "TAP receive poll never increments its packet budget"
* devjazz:F1 | UNSETTLED "Read the R4030 interval-timer definition of reload 0 and compare it with the frequency request and the delivery predicates."
* devjazz:F2 | CONFIRMED-NEW LOW jazzpendingovf "Interval-timer backlog is a signed counter with no saturation"
* devjazz:F3 | CONFIRMED-FILED OB-22
* devjazz:F4 | CONFIRMED-FILED jazzlbmask
* devjazz:F5 | RECORD-L4 "At 8ea26abb, JAZZ pending-line bits and R4030 EXT_IMASK CPU-IP enable bits occupy separate namespaces. Timer pending is 0x8000; its IP6 enable is 0x10. IRQ3 requires a pending local-bus line and EXT_IP3 (0x02); IRQ6 requires pending timer line 15 and EXT_IP6 (0x10). EXT_IMASK writes recompute these predicates, and timer delivery uses jazz_timer_irq."
* devjazz:F6 | RECORD-L4 "(the resulting address is passed to the guest physical-memory dispatcher; the DMA controller does not confine it to RAM, and this observation does not establish a host buffer overrun)"

ASTRA'S AMENDMENTS (5)
* devne2000:F1 | grok said CONFIRMED-NEW LOW ne2krxbudget | should be **CONFIRMED-NEW HIGH, conditional on sustained ingress** | [src/devices/dev_ne2000.c:333](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_ne2000.c:333) rejects invalid rings without setting OVW; its receive loop at :452 has no budget. [src/net/net.c:302](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/net/net.c:302) polls distributed-network input again on every iteration. A separately running peer can replenish input while this guest is paused; the queue-size cap does not bound execution time. **Grok’s change from the draft’s conditional HIGH was wrong.** | confidence: high, with the sustained-input condition.
* devne2000:F4 | grok said CONFIRMED-NEW MED ne2kzerordc, unqualified command reissue | should be **CONFIRMED-NEW MED: “Reissuing exhausted remote DMA alongside a transmit command fails to assert RDC immediately”** | [src/devices/dev_ne2000.c:408](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_ne2000.c:408) handles the command without updating RDC; :197 and :213 raise it on subsequent data access. The documented immediate-completion case includes transmit overlap. The draft retained that premise; grok omitted it. [DP8390 datasheet, printed p19](https://media.digikey.com/pdf/Data%20Sheets/Texas%20Instruments%20PDFs/DP8390D,NS32490D.pdf#page=20). | confidence: high.
* devne2000:F5 | grok said CONFIRMED-NEW MED ne2kparsync, “the address the backend filters on” | should be **CONFIRMED-NEW MED, explicitly scoped to TAP unicast filtering with promiscuous mode clear** | [src/devices/dev_ne2000.c:607](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_ne2000.c:607) updates PAR alone; [src/net/net_tap.c:89](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/net/net_tap.c:89) filters against the unchanged `nic.mac_address`. Local and distributed delivery in `src/net/net.c:443` and :323 do not apply that MAC filter. Restore the draft’s explicit TAP qualification. | confidence: high.
* bundle_net:F1 | grok said CONFIRMED-NEW LOW taprxquota | should be **CONFIRMED-NEW HIGH, conditional on sustained incoming traffic** | [src/net/net_tap.c:104](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/net/net_tap.c:104) initializes the never-incremented counter; :112 therefore cannot enforce the budget. Nonblocking reads at :116 need not return a negative result while incoming traffic continues. The synchronous caller, [src/net/net.c:294](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/net/net.c:294), consequently need not return to emulation. A finite burst returning does not refute the finding’s continuing-input premise. **Grok’s downgrade from the draft was wrong.** | confidence: high, with the sustained-input condition.
* devjazz:F2 | grok said CONFIRMED-NEW LOW jazzpendingovf | should be **CONFIRMED-NEW MED, with overflow consequences qualified** | [src/devices/dev_jazz.c:276](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_jazz.c:276) increments the signed counter without saturation; :294 and :307 gate delivery on positivity, and :442 cannot acknowledge a negative count. On wrapping builds, overflow compromises interrupt delivery. This matches the campaign’s MED treatment of `rtcpendovf` at [DISPOSITIONS.md:385](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/astraretro_20260926/DISPOSITIONS.md:385). Do not claim portable signed wrapping or a measured deadline. Here **grok’s agreement with the draft retained the undergrade**. | confidence: high on defect; medium-high on severity.

THE RULER'S OWN ADDITIONS (its section (b))
(b) Found while checking, not among the 24. `src/devices/dev_ne2000.c:147-148` says `net.c` filters by `nic.mac_address`; `src/net/net.c:443-451` does not. `OUTSTANDING_BUGS.md:2919-2921` still says the Jazz assert/deassert gates on `int_asserted & int_enable_mask`; the live predicates are `src/devices/dev_jazz.c:143-146`. Replacement for that note: "At 8ea26abb the pending-line bits and the EXT_IMASK CPU-IP enables are separate. IRQ3 is a pending local-bus line and EXT_IP3; IRQ6 is pending timer line 15 and EXT_IP6." `src/net/net.c:221` labels the RARP once-only warning with the component string `"ARP"`. `src/devices/dev_jazz.c:244-249` comments a 16- or 256-byte copy and sets `ncpy` to 15 or 255; the surrounding loop still advances, so the span is still transferred. `src/net/net_tap.c:230` assigns `strdup(tapdev)` with no allocation check.

SEVERITY DISPUTE -- RETURNED TO THE RULER (brief adjudication/grok_brief_dispute3fh.md; answer
adjudication/grok_20261002/grok_dispute3fh.txt).  Astra, the family that wrote the findings, RAISED these grades over
the grok seat's independent ruling; a raise by the author family is not adopted on its say-so, so each came back to
grok with Astra's reasons verbatim.  grok: "VERDICT: 3 conceded, 0 held, of 3 disputed severities; 0 of 2 adopted amendments objected to".  Lines below are verbatim from that answer.
* devne2000:F1 `ne2krxbudget` -- D1 | CONCEDE HIGH.  (d) CONCEDE HIGH, conditional on that flood plus the guest-armed ring. A finite burst stays outside the finding. The LOW grade treated the finite-burst exit as the whole effect.
* bundle_net:F1 `taprxquota` -- D2 | CONCEDE HIGH.  (c) CONCEDE HIGH, conditional on a flood that keeps `read` nonnegative. Requiring a guest arming state would grade this wider trigger lower than D1. A finite burst still returns, and that does not cover the continuing-input regime.
  Its one open sub-point: Whether a TAP can deliver a zero-length frame, which would take the `continue` at `:128-129` and spin, is UNSETTLED; settling it takes a read of the host tun/tap driver or a nonblocking `read` on an idle TAP versus a TAP fed a zero-length write.
* devjazz:F2 `jazzpendingovf` (Astra: MED, matching `rtcpendovf`) -- A2 | AGREE
* The rule grok applied to all three -- RULE: A precondition the guest does not control alone leaves a termination, an out-of-bounds access, or a stop in progress at HIGH when that precondition is input the emulator already accepts on the path in question — packets from a peer, traffic on an attached TAP, or a `-k` value inside the range `main.c` parses — and the grade is LOW only when no input that path accepts can produce the effect.
* DENOMINATOR: opened 31 of the 31 cited locations; D1 D2 D3 A1 A2 each answered or marked UNSETTLED
RESULT: `ne2krxbudget` and `taprxquota` are CONFIRMED-NEW HIGH, each CONDITIONAL as Astra's amendment states (a guest-armed
invalid ring plus sustained ingress; sustained TAP traffic); `jazzpendingovf` is CONFIRMED-NEW MED with Astra's qualifier.
The grades rest on a RULE about who controls the input (above), which no flagship seat has ruled on: it is a RULE
QUESTION for the batched sign-off, beside `shoddprfield`'s.
MAIN-LOOP CHECKS (the main loop's own reading, not a seat's): `src/net/net_tap.c:104-135` -- the counter is set at :104,
compared at :112 and never incremented, and the loop leaves only at :118-121; `src/net/net.c:302-330` -- up to 100
`recvfrom` per call; `src/net/net_tap.c:89-90` and `src/cpus/memory_rw.c:214-220` bear out Astra's two scope amendments
(devne2000:F5's TAP qualifier; memoryrw:F5's read qualifier in batch 3g).

---

## Batch 3h -- arcbios, bundle_core, bundle_devices6, bundle_disk, bundle_include3, bundle_promemul (26 findings).
## Ruled by grok (grok-4.7 xhigh, first-hand): 9 confirmed-new, 5 confirmed-filed, 7 record-L4, 0 test-gap, 0 refuted, 0 unsettled, 5 duplicate, of 26 findings (adjudication/grok_20261002/grok_rule3h.txt).
## Astra: 1 of 26 dispositions wrong (3 more need a change of wording or severity) (adjudication/codex_astraconfirm_3h.txt).  Mechanically assembled (mk_disp.py): every line below is VERBATIM from
## one of those two files; where an Astra amendment touches a finding, the AMENDMENT governs.

RULINGS (each finding's disposition statement, up to its `Checked:` line)
* arcbios:F1 | CONFIRMED-FILED arcpartlba
* arcbios:F2 | CONFIRMED-NEW LOW arcseekshift "ARC Seek retains a signed byte-decoding shift"
* arcbios:F3 | CONFIRMED-NEW LOW arcstdinlimit "ARC stdin Read overflows its signed loop counter at length 2147483647"
* arcbios:F4 | CONFIRMED-NEW HIGH arccursorbound "Unbounded ARC cursor column makes erase-line walk 2^31 cells"
* arcbios:F5 | CONFIRMED-NEW HIGH arczeroalloc "Zero-length ARC disk I/O calls malloc(0) and CHECK_ALLOCATION exits if that returns NULL"
* arcbios:F6 | CONFIRMED-FILED arcsgiprivate
* arcbios:F7 | CONFIRMED-FILED arcbioswalk64
* arcbios:F8 | RECORD-L4 "ARC's missing-handler and ordinary unsupported-vector state dumps require SUBSYS_PROMEMUL verbosity VERBOSITY_DEBUG; a promemul subsystem breakpoint alone does not enable them."
* bundle_core:F1 | CONFIRMED-NEW LOW dyncacheoffset32 "Oversized configured translation caches truncate published page offsets"
* bundle_core:F2 | CONFIRMED-NEW MED fbresizeoverlap "Framebuffer growth overlaps its controller mapping"
* bundle_core:F3 | DUPLICATE-OF-ROW rtcpendovf
* bundle_core:F4 | RECORD-L4 "Diagnostics are suppressed when the clamped frequency equals the stored frequency; there is no per-timer warning latch. Alternating requests with different normalized frequencies can report repeatedly when clamping occurs. dev_rtc pre-clamps, and dev_footbridge's effective-period calculation cannot produce an above-ceiling request."
* bundle_core:F5 | RECORD-L4 "as a whole: dev_sh4.c's sh4_timer_tick() still calls fatal() from SIGALRM when reporting newly seen refresh-interrupt enable bits. #449 removed the exit(1); the callback now continues into TMU processing."
* bundle_core:F6 | DUPLICATE-OF-ROW timerupdrow
* bundle_devices6:F1 | CONFIRMED-NEW LOW irqcmaskshift "IRQ mask and unmask writes still use a signed 1 shifted by the guest selector"
* bundle_devices6:F2 | RECORD-L4 "Unsigned casts for interrupt-controller and setup shifts, including type consistency in the KN02 and KN230 constructors."
* bundle_disk:F1 | CONFIRMED-NEW LOW isopathptr "ISO path-table checks form pointers beyond one-past"
* bundle_include3:F1 | DUPLICATE bundle_core:F2 Same resize-then-`memory_device_update_length` defect as `fbresizeoverlap`. One row.
* bundle_include3:F2 | CONFIRMED-FILED sh4sqwrite
* bundle_include3:F3 | CONFIRMED-FILED sh4sqexpevt
* bundle_include3:F4 | DUPLICATE-OF-ROW sh4utlbmultihit
* bundle_include3:F5 | RECORD-L4 "Do not replace __attribute__ or __noreturn__ with empty macros: the firmware function-pointer declarations below carry __attribute__((__noreturn__)) annotations. This header has no packed structure declarations."
* bundle_include3:F6 | DUPLICATE-OF-ROW cpushinstr:F11
* bundle_promemul:F1 | CONFIRMED-NEW HIGH ofopenexit "OpenFirmware open exits the host on any nonempty pathname"
* bundle_promemul:F2 | RECORD-L4 "Stop copying after a failed guest-memory write. The returned length remains the precomputed minimum of the property length and the requested maximum; it is not adjusted to the number of bytes copied."
* bundle_promemul:F3 | RECORD-L4 "Eight diagnostic sites were changed. The DEC unsupported-vector handlers replace their register dumps and A0 string scans with verbosity-gated summary messages; the ARC missing-handler and ordinary unsupported-vector handlers retain their dumps behind ENOUGH_VERBOSITY."

ASTRA'S AMENDMENTS (4)
* arcbios:F6 | grok said CONFIRMED-FILED arcsgiprivate | should be **CONFIRMED-NEW HIGH arcsgiprivate** | `src/promemul/arcbios.c:1271` dispatches to the SGI handler whose default stops the CPU at `:1226`. No such ID or specific SGI-private residual filing exists at HEAD. `OUTSTANDING_BUGS.md:2670` is the historical backlog subsequently addressed at `:2608–2619`; the enumerated residuals omit this defect. Although #242 accurately limits its repair to non-SGI calls, that does not establish a surviving SGI filing. The campaign already rejects this historical backlog as a filing for missed residuals (`DISPOSITIONS.md:646–647`). Grok inherited this mistake from the draft. | confidence medium-high on classification; high on the live defect
* bundle_core:F1 | grok said CONFIRMED-NEW LOW dyncacheoffset32 | should be **CONFIRMED-NEW HIGH**, conditional on the oversized configured cache | `src/cpus/cpu_dyntrans.c:797–804` narrows the allocation cursor and reconstructs a different page; `:830–833` publishes instruction pointers from it, and `:114` calls the resulting host function pointer. The allocation also contains non-instruction data (`src/cpus/cpu.c:319–324`). Remaining inside that allocation does not prevent invalid indirect calls and host termination. Both draft and grok stopped their impact analysis too early. | confidence high, static analysis
* arcbios:F1 | grok said CONFIRMED-FILED arcpartlba | should be **CONFIRMED-FILED BY PROSE, LOW; proposed ID arcpartlba** | The ID does not exist at HEAD. The exact defect is nevertheless recorded at `OUTSTANDING_BUGS.md:2730–2731` and explicitly remains deferred at `:2453–2455`; signed arithmetic survives at `src/promemul/arcbios.c:1010–1017`. Preserve that filing without adding another row. Grok should retain the draft’s explicit “by prose” qualification. | confidence high
* bundle_include3:F5 | grok said RECORD-L4 at src/include/sgi_arcbios.h | should be **RECORD-L4 at src/include/thirdparty/sgi_arcbios.h:17–20**, retaining the replacement text | The committed header is under `thirdparty`; its declarations contain the stated `__noreturn__` annotations and no packed declarations. Grok changed the draft’s correct path incorrectly. This is a citation-only amendment. | confidence high

THE RULER'S OWN ADDITIONS (its section (b))
(b) Noticed while checking, and not one of the 26. `of.c:394` is `exit(1)` on `peer()` when the handle is not the root and the lookup misses: guest-controlled host termination, absent from `OUTSTANDING_BUGS.md` and from `DISPOSITIONS.md`. Proposed id `ofpeerexit`, HIGH. Five other `exit(1)` sites in that file (`:549`, `:577`, `:1100`, `:1120`, `:1201`) were seen and left untraced; `:1185` says one of them exists to defeat the debugger. `dec_prom.c:188` and `:650` still say a promemul breakpoint restores full state after those dumps were removed. Rider on promemul:F3, replacement of that parenthetical: "The #245 summary is the whole diagnostic: the register dump and A0 string scan were removed, so neither promemul verbosity nor `break promemul` restores them." The ISO second loop allocates 512 bytes at `bootblock_iso9660.c:269` and reads 256; the agy 2048-byte heap over-read does not match that allocation. A duplicate-filename `exit(1)` in that file is disk-image input, under the host-side image charter, and is not given a HIGH row. The AT-off SQ path already masks the address with `0x03ffffe0` before the AT block; there is no missing 32-byte alignment there.

SEVERITY DISPUTE -- RETURNED TO THE RULER (brief adjudication/grok_brief_dispute3fh.md; answer
adjudication/grok_20261002/grok_dispute3fh.txt).  Astra, the family that wrote the findings, RAISED these grades over
the grok seat's independent ruling; a raise by the author family is not adopted on its say-so, so each came back to
grok with Astra's reasons verbatim.  grok: "VERDICT: 3 conceded, 0 held, of 3 disputed severities; 0 of 2 adopted amendments objected to".  Lines below are verbatim from that answer.
* bundle_core:F1 `dyncacheoffset32` -- D3 | CONCEDE HIGH.  (c) CONCEDE HIGH, conditional on `-k` at least 4097 on a 64-bit host and on the guest translating enough distinct pages for the cursor to cross 2^32. The LOW grade stopped at "aliases inside the allocation."
* arcbios:F6 `arcsgiprivate` (Astra: CONFIRMED-NEW HIGH, not FILED) -- A1 | AGREE
* The rule grok applied to all three -- RULE: A precondition the guest does not control alone leaves a termination, an out-of-bounds access, or a stop in progress at HIGH when that precondition is input the emulator already accepts on the path in question — packets from a peer, traffic on an attached TAP, or a `-k` value inside the range `main.c` parses — and the grade is LOW only when no input that path accepts can produce the effect.
* DENOMINATOR: opened 31 of the 31 cited locations; D1 D2 D3 A1 A2 each answered or marked UNSETTLED
RESULT: `dyncacheoffset32` is CONFIRMED-NEW HIGH, CONDITIONAL on a host-operator `-k` of at least 4097 on a 64-bit host
(grok's (a), in the answer file) -- the same RULE QUESTION as batch 3f's two rows; `arcsgiprivate` is CONFIRMED-NEW HIGH.
MAIN-LOOP CHECKS (the main loop's own reading, not a seat's): at HEAD `db8b1a33` the 2026-07-16 backlog closure
(`OUTSTANDING_BUGS.md:2601-2619`) names only `#242` "`arcbios` non-SGI private call / `0x888` / unimplemented vector";
no row names the SGI default at `src/promemul/arcbios.c:1220-1226`; this campaign's own rule on the same backlog lines is
"a closed item is not a filing for its residual" (batch 3b, `cpumipsinstr:F1`/`F2`).  `src/core/main.c:401` sets the cache
size from the command line.  `src/include/thirdparty/sgi_arcbios.h` exists and `src/include/sgi_arcbios.h` does not
(Astra's path amendment to bundle_include3:F5).
