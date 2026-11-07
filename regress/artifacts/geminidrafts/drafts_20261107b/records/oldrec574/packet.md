# Reading task: oldrec574 (Gemini web; 2026-11-06)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC574-7f6e` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #574 i8259eoiirr (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 1427-1566 at HEAD 116c5aa9; each line carries its own number -- cite those numbers)

```text
 1427| # `#574` Records (follow-up, 2026-10-25): `i8259eoiirr` names its landing commit `c1c74b2b`; the committed-tree proofs; the pass-2 receipt
 1428| 
 1429| `git ls-tree c1c74b2b` shows `regress/i8259_eoi_probe.py` at `100644 blob 94d94b9ad433470e72fc4a941cef12fb2a5eaa01` with blob md5 `c1fa683e3a9295eb62491af043189500` -- the banked frozen v2g copy every leg of
 1430| `regress/artifacts/i8259eoiirr/pass2_20261025/fixlegs_132736/` ran (LF, no CR byte); the committed `src/devices/dev_8259.c`, `src/devices/dev_gt.c` and
 1431| `src/include/devices.h` blob md5s are `de16fa14ac321c473d52c9abb1d1d24f`, `4c3bdbb1594013e5fca4dfbe44cb12ec` and `9802103c72d891de4a257acf6e09f732`, the files the fix legs were built from (every RUN_IDENTITY names them);
 1432| the committed `regress/gate_arm.sh` carries the #574 block and its `rows run` pin, `tools/precommit_check.sh` SCORE_CLAIMS_MANIFEST=42,
 1433| `regress/gate_hygiene.sh` EXPECT_PTY_PROBES=80 with `i8259_eoi_probe.py` grandfathered, `tools/pipeline/check_probe_wiring.py` the MANIFEST
 1434| key.  Landing numstat (4275 files): 56 0 regress/gate_arm.sh; 3 2 regress/gate_hygiene.sh; 1128 0 regress/i8259_eoi_probe.py; 78 29 src/devices/dev_8259.c; 18 1 src/devices/dev_gt.c; 2 0 src/include/devices.h; 9 0 tools/pipeline/check_probe_wiring.py; 1 1 tools/precommit_check.sh.  PROPAGATED after the landing: the three product files copied into `est/` (source tree, part 2
 1435| N/A), `build/`, `build-asan/` and `/tmp/gxsec-build`, each build tree rebuilt at once; `regress/artifacts/i8259eoiirr/landing_clearance/CLEARANCE.out`
 1436| records the OUTPUT of both clearance parts (cmp clean against GXEMUL-SEC for every copy; each binary newer than both edited sources).
 1437| The ledger row's `commits` field names `c1c74b2b`; its state stays `held` (the Fable question and the roster question -- `hold_question`).  The
 1438| PASS-2 RECEIPT line is appended to `regress/pass2_ledger.tsv` (precommit section F).  Argon's web-route answers for every pass of this
 1439| round are still QUEUED behind the single sender and are OWED to a later records commit (the late-dissent rule).
 1440| 
 1441| # `#574` (2026-10-25) -- `i8259eoiirr`: the 8259 model gains its interrupt acknowledge; the specific EOI stops clearing the request bit of a line in service; the 8253's pending event is retired at the acknowledge  [research batch T19; MED WRONG-RESULT]
 1442| 
 1443| **The defect.**  `src/devices/dev_8259.c` had no interrupt acknowledge.  The OCW3 poll read (`case 0x0c:`) returned a poll byte
 1444| scanned from the raw IRR -- masked lines included -- and set no in-service (ISR) bit; the GT64120 interrupt-acknowledge read
 1445| (`src/devices/dev_gt.c`, `case GT_PCI0_INTR_ACK:`) returned the last asserted line and acknowledged nothing (its own comment said
 1446| `TODO: Actually ack the interrupt?`); and the specific EOI arm cleared the REQUEST bit of the EOI'd line (`d->irr &= ~(1 << (idata
 1447| & 7))`), standing in for the acknowledge the model lacked.  On the chip an EOI resets an in-service bit only; the request bit is
 1448| cleared by the acknowledge (Intel 8259A datasheet, `_scratchpad/i8259/8259A.txt` :223-256, :491-566, :596-612).  Both documented
 1449| malta guests acknowledge and then EOI specifically -- NetBSD by the OCW3 poll (`sys/arch/evbmips/malta/pci/pcib.c`, `pcib_intr`),
 1450| Linux by the GT IACK read (`arch/mips/mti-malta/malta-int.c`, `mips_pcibios_iack`, installed by `i8259_set_poll`; `drivers/irqchip/
 1451| irq-i8259.c`, `mask_and_ack_8259A`) -- so in this model neither acknowledge did anything and the EOI did the acknowledge's job late and
 1452| wrongly.  Two guest-visible consequences, both MEASURED on the unmodified `evbmips -e malta` (rung 3, guest instructions through the
 1453| real decode): a request a device still held was dropped by the EOI until the device re-asserted (`regress/artifacts/i8259eoiirr/
 1454| witness_20261025/`, 19 rows, 06:51 WSL clock, before any edit), and the 8253 timer -- whose pending-event count nothing ever retired, because the
 1455| only decrement sat in `bus_isa.c`'s `isa_interrupt_deassert()` behind a pointer `bus_isa_init` snapshots BEFORE `DEVINIT(8253)`
 1456| publishes it, in a deassert the 8253 never issues -- was re-delivered once per 2^14-instruction tick instead of once per programmed
 1457| period: **7,415 IRQ 0 deliveries in 180M guest instructions at a programmed 18 Hz**, counted by a guest handler at the general
 1458| exception vector (`pass1_20261025/rate_explore_20261025/RUN_IDENTITY.txt`).  Linux/malta programs that PIT and requests IRQ 0 (`arch/mips/Kconfig`
 1459| `select I8253`, `arch/mips/kernel/i8253.c` `setup_pit_timer`), so the storm is a documented guest's.
 1460| 
 1461| **The fix (design (G'), ruled at the pass-1 adjudication).**  `pic8259_acknowledge()` -- new, in `dev_8259.c`, declared in
 1462| `devices.h` -- moves the highest-priority UNMASKED request to service: ISR bit set, IRR bit cleared, the 8253's pending event retired
 1463| when the line is pic1's line 0 (read through `machine->isa_pic_data.pending_timer_interrupts` at call time, the pointer `DEVINIT(8253)`
 1464| publishes), then the PIC's output recomputed on its own `irq` (for pic2 that is the ISA cascade line, which `bus_isa.c` folds into
 1465| pic1 bit 2 -- no manual fold here: the adjudication found that a pre-fold swallows the transition `isa_interrupt_common()` needs and
 1466| strands a second slave request).  The read after an OCW3 poll calls it and is ONE-SHOT (`current_command` reverts to the IRR; the
 1467| `default` read arm is byte-identical to HEAD and acknowledges nothing).  The GT IACK READ calls it -- pic1, then pic2 through the
 1468| cascade -- and returns the line (0-15, as `last_int` did); a write, a machine without ISA PICs (MVME5500), or nothing pending leave
 1469| `last_int` as before.  The specific EOI resets the ISR bit when the line is in service and otherwise CONSUMES the request as it always
 1470| did here -- the legacy path kept on purpose for machines whose vector read acknowledges nothing (`dev_prep.c`, `dev_footbridge.c`;
 1471| their guests EOI without an acknowledge and that consume is the only one they have).  The non-specific EOI resets the lowest set ISR
 1472| bit (fixed priority) and nothing else.  Edge-only: both guests program ICW1 0x11; LTIM still only prints (filed `i8259ltim`).  Diff:
 1473| `src/devices/dev_8259.c` +78 -29, `src/devices/dev_gt.c` +18 -1, `src/include/devices.h` +2 -0.  **Three sketch defects the
 1474| adjudication caught before the edit**: the manual cascade pre-fold (four seats), the acknowledging `default` read arm and a sticky poll
 1475| latch (three seats), and the removal of the EOI consume on unconverted machines (Astra, Grok) -- all three repaired in the design that
 1476| shipped, none measured against a guest first.
 1477| 
 1478| **The panel.**  Pass 1 (`pass1_20261025/`, 29.5 KB brief from the template with five candidate designs): Astra NOT READY, Grok NOT READY,
 1479| GLM READY WITH CHANGES x3, DeepSeek READY WITH CHANGES / NOT READY x2 -- every seat accepted the ISR-only EOI semantics and five of eight
 1480| refused it ALONE (the 8253 then has no consumer), which the exploratory measurement then confirmed (`timer_explore_20261025/`: IRR bit 0
 1481| cleared by the EOI and back within a tick).  Twelve premise corrections (`PASS1_RULINGS.md` C1-C12), four of them checked at the guests'
 1482| sources (NetBSD polls and EOIs specifically; Linux reads the GT IACK, not the poll; Linux programs the PIT; the ns16550 deasserts
 1483| synchronously -- the brief's "churn" argument was wrong).  The pass-1 adjudication (`f2_20261025/F2_RULINGS.md`): Astra NOT RATIFY with
 1484| six overturns, the others RATIFY WITH CHANGES; dispositions A1-A13 adopted.  Pass 2 (`pass2_20261025/`, the diff and the v2c
 1485| instrument inlined): Astra VERDICT: DO NOT SHIP -- the one-shot coverage claim is false, GT consumer compatibility remains unproved, and the provenance record needs correction.  Grok VERDICT: SHIP WITH CHANGES -- the device diff is (G') and the 77/77 measurement is real; do not treat `M_sticky` as killed, because `poll once` stays green if the one-shot assignment is deleted.  GLM VERDICT: SHIP WITH CHANGES -- no premise in 2.1-2.8 falls from the packet and the inlined diff is consistent with every stated warrant, but the row table leaves at least one clause of the fix (the one-shot l // VERDICT: SHIP WITH CHANGES -- the diff is internally sound and the row arithmetic verifies, but one design-bearing fact (the bus_isa cascade fold's re-entrancy) is unsettled and reachable on malta's own devi  DeepSeek VERDICT: SHIP WITH CHANGES — Q1(iii) unverified, Q2 third escape uncovered. // VERDICT: SHIP WITH CHANGES -- Q3(c) unresolved CPU-line stall with two slave requests; Q1(iii) unresolved GT IACK line vs vector byte..  Pass 2 found NO defect in the diff and TWO in the instrument, both L1 (pre-ship construction) and
 1486| both repaired before the measurement of record: the one-shot row `poll once` as built read the command port after a SECOND poll made
 1487| with nothing pending, so a sticky latch and the intended IRR read both returned 0x00 (Astra, Grok, GLM -- and the first kill table
 1488| measured it: `M_sticky` ESCAPED 77/77, `killtable_20261025/SCORES_v2c.txt`, 12 of 15 killed, kept as the record of what it
 1489| measured); and no row pinned the GT read's RETURNED line against a dropped `odata = n` (Astra, Grok).  v2d moves the one-shot row to
 1490| the masked session (the masked poll acknowledges nothing; the next command-port read returns the IRR 0x10 under the fix, the poll
 1491| byte 0x00 under a sticky latch, 0x84 on HEAD) and adds the `gtboth` session (UART IRQ 4 and RTC IRQ 8 pending together: the
 1492| acknowledge returns 8, HEAD's flat scan 4) with the mutant `D_gt_noassign`; `PRETABLE.out` carries the correction in place and the
 1493| table of record re-ran every mutant on v2d.  Four records corrections in place (`PASS2_RULINGS.md` R1-R4: the pass-1 witness ran at
 1494| 06:51, not 03:49; the guest-source quotes live in `f2_20261025/F2_PACKET.md` 1.7/1.8, not F2_RULINGS; the fix clone (07:56) predates
 1495| the v2 re-pin (08:01) and what every FIX measurement follows is the HEAD run of the same instrument revision; a zero 8253 count gives a
 1496| timer that does not fire within any run, not one that never fires).  Its adjudication (`pass2_20261025/f2b_20261025/`): Astra (adjudicating) VERDICT: RATIFY WITH CHANGES -- retain the product design; reopen instrument and compatibility-evidence closure before landing.  Grok VERDICT: RATIFY WITH CHANGES -- ship the unchanged product diff; Astra's three grounds are dead on the measurements; amend D5's reason, and relabel the both-columns value rows as contract before the probe la  GLM VERDICT: RATIFY WITH CHANGES -- all twenty-one dispositions stand; the only changes owed are records-level (F16's correction not yet applied to §2.8's own wording) and a verification debt carried to part B ( // VERDICT: RATIFY WITH CHANGES -- the ruling (SHIP WITH CHANGES, diff unchanged) stands: I re-derived D4 with no stall and D3 independently of Grok's quotes; what is owed is records- and instrument-side, not p  DeepSeek VERDICT: RATIFY WITH CHANGES — F14 must be repaired (add `i8259cascline` row) before ship; F3 cannot be settled from packet. // VERDICT: RATIFY WITH CHANGES — D3 is not checkable from the packet; require the actual ICW2 base source before final ratification, otherwise the diff is sound..
 1497| The adjudicating seat WITHDREW its one-shot ground on the measured kill and the pass converged on the diff; what it raised is
 1498| INSTRUMENT cells of the fix's own predicates that no row observed -- an EOI of a line both in service and MASKED (Linux's
 1499| mask-then-EOI order), the one-shot latch after a SUCCESSFUL poll, the acknowledge's recompute with a second request pending
 1500| (the CPU line), a specific EOI clearing the whole ISR, a GT read with nothing pending, the GT WRITE -- each MEASURED as a mutant
 1501| against v2d before any repair (`killtable_20261025/table_v2d_extra/SCORES.txt`: 7 escaped the v2d instrument (D_eoi_maskcond, D_latch_cond, B_spec_isr0, D_deassert, D_gt_always, D_retire_anypic, D_retire_anyline), 0 killed (none); `killtable_20261025/table_v2f_extra/SCORES.txt`: 3 escaped the v2f instrument (D_recompute_raw, D_eoi_anyisr, D_gt_nocasc2), 3 killed (D_recompute_true, D_recompute_none, D_scan_high)), then closed in ONE instrument revision (v2e: the sessions `maskeoi` and `speceoi`;
 1502| the rows `poll once2`, `nonspec ip2` (CP0 Cause bit 10 read with the line still pending), `quiet iack`, `gt write isr`; the
 1503| both-columns device values relabelled CONTRACT rows, so a mutant that reds a poll byte or an IACK value is a kill and not an
 1504| instrument failure).  Records corrections from F2b, in place: `irq_base` is not write-only globally (`dev_footbridge.c` reads
 1505| it; only `dev_8259.c`/`dev_gt.c` never read it); GLM's pass-2 position on the retire guard was a REQUEST for a banded
 1506| mixed-source row, not "no row exists" (the band-row construction is filed as `pit8253retireguard`); the pass-2 verdict split
 1507| was one seat against three (five answers), not "1-4"; the returned-line warrant is Grok's re-fetch of Linux's ICW2 bases (0
 1508| and 8) and `MALTA_INT_BASE` 0 on F2b, which the inlined quotes did not carry.  The repair's own pass (F2c, scoped to the
 1509| instrument diff): Astra (adjudicating) VERDICT: RATIFY WITH CHANGES -- the named repairs are valid, but three uncovered predicate cases prevent instrument closure; provisional until the roster completes.  Grok VERDICT: RATIFY WITH CHANGES -- the six new kill rows kill the mutants they name; the helper recompute's false branch is still unobserved, so this pass does not close.  GLM VERDICT: RATIFY WITH CHANGES -- all thirteen new rows are valid by construction and none is vacuous, the nine relabels are sound, and the table of record is read right; but one half-predicate of the fix's ow // VERDICT: RATIFY WITH CHANGES -- one clause-(d) cell of the fix's recompute predicate (the `~d->ier` mask term) is observed by no row in the 101-row table and covered by no filing; row it (one session), add t  DeepSeek VERDICT: NOT RATIFY -- three escaped mutants remain, so zero floor breaches is not met. // VERDICT: RATIFY -- zero floor breaches in the v2e instrument diff; one F2b disposition (A6) is partially wrong and was already corrected in the shipped v2f..  F2c found the SAME CLASS again -- the recompute's other partition cells (nothing remaining; only a
 1510| masked request remaining), the EOI predicate weakened to "any line in service", the GT cascade conjunct -- each measured as a
 1511| mutant against v2f first and closed in v2g as the CLASS CLOSURE the repair-chain amendment requires: the sessions `maskrem`,
 1512| `isrother` and `gtmask`, the rows `ack ip2` and `pit ip2` (CP0 Cause bit 10 read right after an acknowledge, the CPU line
 1513| observed synchronously), and the contract's ENUMERATION of every predicate the fix adds with a row or a written disclosure
 1514| per cell (`PRETABLE.out`'s v2g block; the OUTSIDE list names `pic1`/`pic2` NULL as unobservable on a one-machine instrument,
 1515| `n2 < 0` as unreachable while bus_isa re-folds the cascade bit, the retire-guard conjuncts as host-timed and filed, the
 1516| two-slave stall as owed).  The closing pass, verifying the enumeration (F2d, `pass2_20261025/f2d_20261025/F2D_RULINGS.md`): Astra (adjudicating) VERDICT: RATIFY WITH CHANGES -- the new rows close the three prior holes; correct the enumeration mappings, disclosure wording, and measurement chronology. Provisional until the roster completes.  Grok VERDICT: RATIFY -- the v2g enumeration's cells are closed: each added predicate's body partition has a row that sees its mutant, or an honest disclosure.  GLM VERDICT: RATIFY WITH CHANGES -- the enumeration substantively closes every listed predicate (all six F2c shapes measured against v2f first, every new row's construction verified to see its mutant, escapes ex // VERDICT: RATIFY WITH CHANGES — the §2 partition is closed as a cell set and I overturn none of C1–C9 outright, but two disclosures are constructible by composing techniques the packet's own rows already demo  DeepSeek VERDICT: RATIFY -- the enumeration in section 2 is complete and every rowed cell has a row that can see its mutant, as far as the packet shows. // VERDICT: RATIFY — C1-C9 stand; the denominator is closed, with no missing enumeration cell or invalid disclosure..  F2d CLOSED THE CHAIN
 1517| (no new measured breach; the three escapes are the three disclosed) and changed records only: the retire-guard pair's warrant
 1518| *"observable only with a pending count >= 2, which only host time produces"* is WITHDRAWN -- Astra and GLM B derived, and
 1519| `dev_8253.c:118-129` confirms, a construction after ONE event (line 0 masked, a foreign acknowledge, the legacy EOI of line 0, the
 1520| next tick re-asserts on the fix and not on the mutant) -- so `D_retire_anypic` / `D_retire_anyline` are OWED REPAIR under
 1521| `pit8253retireguard`, not a disclosure; **the attempt to write those rows was classifier-stopped at 15:5x and, by the standing rule,
 1522| not retried, so this round lands with that debt named** (the #567 precedent).  Also from F2d: the (pic2, line != 0) cell added to the
 1523| enumeration; two mappings, the sweep/re-pin chronology (concurrent, not sequential) and `B_eoi`'s prescription corrected in
 1524| `PRETABLE.out`'s dated note; `D_nonspec_high` and the non-specific arm's IRR-half reinstatement unbuilt and owed; the probe
 1525| docstring's ">= 2" sentence a wrong record left byte-identical to the measured copy.
 1526| Seats not fired by roster (kimi, minimax, the Opus review seat) recorded by name; agy
 1527| quota-walled; Argon's web-route answers OWED for pass 1, F2, pass 2 and F2b -- the web route's single sender slept on the meter (8.3% at 07:44) until 12:32:15 CDT; the agy transport quota-walled until ~2026-10-30; Fable HELD with its question (`FABLE_HOLD_QUESTION.md`).
 1528| 
 1529| **The detector** -- `regress/i8259_eoi_probe.py` (md5 c1fa683e, 1128 lines; 123 rows in 17 sessions on the unmodified
 1530| `evbmips -e malta`; every guest word checked against the emulator's disassembler, every park pc-verified, RAM liveness per session,
 1531| the device signature in `quiet *`).  **The oracle was re-pinned FIRST** (the oracle-correction order): the pass-1 witness rows `eoi
 1532| irr4` / `eoi x8` wanted the request bit KEPT after an un-acknowledged EOI; under (G') such an EOI keeps the legacy consume, so they
 1533| became the CONTRACT row `eoi noack` (both columns 0), and the symptom rows are the acknowledge rows -- `poll isr`, `poll irr4`, `poll
 1534| again`, `poll once` (the one-shot latch, in the masked session), `eoi acked` (the line in service and re-asserted; the row that pins the fix's own predicate), the same on IRQ 3 (`poll3 isr`,
 1535| `eoi acked3`, the n != 4 anchor), `poll masked` (the mask-blind scan), `poll second` / `isr both` / `nonspec lowest` (two lines in
 1536| service; the non-specific EOI), `casc isr2` / `casc isr8` (the cascade by poll), `pit poll irr0`, `gt isr` / `gt irr4 after` / `gtcasc
 1537| isr2` / `gtcasc isr8` / `gtboth iack` / `gtboth isr2` / `gtboth isr8` (the GT read: master, cascade, and the returned line with a master and a slave line pending together), `poll once2` (the latch after a SUCCESSFUL poll), `spec isr both` / `spec eoi one` (a specific EOI with two lines in service clears exactly its bit), and `rate storm` (a BAND: HEAD >= 5000 deliveries per 180M instructions, the
 1538| fix 1..1000).  Measured, one frozen copy per run: `witness_20261025b/` (v2 on unmodified HEAD, 69/69 HEAD column, 08:01, before any fix
 1539| measurement) `witness_20261025c/` (v2d on unmodified HEAD, 84/84), `witness_20261025d/` (v2e, 101/101), `witness_20261025e/` (v2f, 101/101) and `witness_20261025f/` (v2g, the shipped
 1540| revision, 123/123), each before any fix measurement of its revision [corrected 2026-11-02, records: said `witness_20261025e/` was "v2f, the shipped revision, 123/123"]; `pass2_20261025/fixlegs_132736/` (v2g [corrected 2026-11-02, records: said v2d], HEAD column on the base clone 123/123, FIX column on the fix clone 123/123, CONTROL OK
 1541| both; rate HEAD 7300 / FIX 3); `pass2_20261025/legs_133457/` -- **L0, the pre-fix build in GATE mode: 91/123 with
 1542| exactly the 32 symptom rows red** (`(a): measured at` `L0/RESULTS_L0_base_gate.txt`); **L3, `/bin/false`: CONTROL FAIL, 0/123** (`(c):
 1543| measured at` `L3/RESULTS_L3_null_gate.txt`).  **The kill table** (`killtable_20261025/`, `PRETABLE.out` written 08:1x before table 1:
 1544| sibling parity, claim->row, guard/body fields, the channel per symptom row, the prescribed list): 29 mutants built and measured in scratch clones against the frozen probe in GATE mode: 26 KILLED (B_eoi, B_poll, B_gt, B_nonspec, D_eoi_n4, D_eoi_n3, D_eoi_ier, D_scan_raw, D_noretire, M_sticky, M_noack_isr, M_noack_irr, D_gt_nocasc, D_gt_noassign, D_gt_write, D_eoi_maskcond, D_latch_cond, B_spec_isr0, D_deassert, D_gt_always, D_recompute_raw, D_recompute_true, D_recompute_none, D_eoi_anyisr, D_gt_nocasc2, D_scan_high); 3 ESCAPED (D_fold, D_retire_anypic, D_retire_anyline)  Contract (clause (e)):
 1545| CATCHES a reinstated IRR clear in the specific-EOI arm in any form, an acknowledge that sets no ISR or clears no IRR, a sticky poll
 1546| latch, a mask-blind poll, a GT read that acknowledges nothing or skips the slave, an acknowledge that does not retire the 8253's event,
 1547| a non-specific EOI that clears every ISR bit.  OUTSIDE: the `default` read arm, priority inhibition by ISR, level-triggered mode, the
 1548| PReP/footbridge vector reads, the OCW2 bytes that stop the emulation, a zero 8253 count,
 1549| the two-slave-request CPU-line case (owed as a filed row) [2026-11-02, records: 'the spurious IACK, a write to the IACK register' removed; rowed by `quiet iack` and `gt write isr`].  Gate: a `gate_arm.sh` block (the tree's device-probe gate by
 1550| accretion; `gatedevicesplit` stays OWED) with the sentinel first, the control line, 123 named rows and four denominators pinned by
 1551| equality (`rows run` 123 -- SCORE_CLAIMS_MANIFEST 41 -> 42); `check_probe_wiring.py` MANIFEST key; EXPECT_PTY_PROBES 79 -> 80, the probe grandfathered as promptless.
 1552| 
 1553| **Records and filings.**  `OUTSTANDING_BUGS.md` 2026-10-25: `i8259eoiirr` FIXED (state `held` for the Fable question and the roster
 1554| question); `i8259isrnever` NARROWED to the PReP/footbridge vector reads (the poll and the GT read now set ISR); `8259cmdhalt` gains the
 1555| reachability this round READ (0x21-0x27 are non-specific EOIs the model treats as specific, 0xa0-0xa7 and 0x6c reach `cpu->running = 0`);
 1556| new rows `pit8253pendingptr` (the dead decrement), `pit8253count0` (a zero count maps to a timer that does not fire within any run (clamped to 1e-8 Hz), MEASURED) [corrected 2026-11-02, records: said "a timer that never fires"], `i8259ocw2
 1557| nonspec`, `algorisaintclear` (dev_algor.c's status reads clear PIC request bits), `i8259ltim`, `i8259priority`, `i8259cascline` (the
 1558| two-slave-request CPU-line row owed to D_fold), `i8259aeoi` (ICW4 AEOI is unsupported while the acknowledge always sets ISR; pass 2,
 1559| Astra), `i8259icwreset` (ICW1 resets neither ISR nor `current_command`; pass 2, Astra and GLM), `i8259ocw3revert` (the one-shot
 1560| poll reverts to the IRR, not to the last RR/RIS selection; F2b, GLM), `i8259smm` (OCW3 0x68 special mask mode is an empty arm
 1561| while NetBSD sets it at attach; F2b, GLM) and `pit8253retireguard` (the retire guard's two conjuncts, rowable only as a band
 1562| with a pending count >= 2; F2b, Astra and GLM -- declined this round on cost, construction recorded).  The mask-blind poll (`i8259pollmask` in the pass-1 record) is closed by construction
 1563| here, not filed.  Witness term: `probe:regress/i8259_eoi_probe.py` with ORDER evidence `witness_20261025/` (pass 1, 06:51 WSL clock),
 1564| `witness_20261025b/` (the v2 re-pin, 08:01), `witness_20261025c/` (v2d, 08:58), `witness_20261025d/` (v2e, 11:24), `witness_20261025e/`
 1565| (v2f) and `witness_20261025f/` (v2g, the shipped revision) [corrected 2026-11-02, records: said `witness_20261025e/` was "v2f, the shipped revision"], each before any fix measurement of its instrument revision.
 1566| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_574: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC574: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
