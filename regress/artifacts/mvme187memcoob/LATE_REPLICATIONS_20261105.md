# mvme187memcoob -- one LATE replication, adjudicated against the current state (2026-11-05)

A read-only records pass: nothing else was edited, built or run, and no git.  The replication was answered by a cloud routine
(model field `claude-mythos-5-1`) at 05:57Z and banked at 08:41Z -- after repair 4 had already implemented its sibling's ruling and
table 4 had run (23:36 local), so nothing in it had been weighed before now.  The rule applied is the late-dissent rule: a late
answer is adjudicated like any other, and nothing it found may silently disappear.

    ADJ r2   p3_20261105/ADJ_MYTHOS_r2.md   pass-3 adjudication   sibling ADJ_MYTHOS.md (repair 4 applied ITS seven changes)
             verdict line: 17 FAMILIES RULED 8 NEW BREACHES 7 CHANGES VERDICT:APPLY-WITH-CHANGES

**Current state read.**  `regress/mvme187_memc_probe.py` (206 rows, mtime 01:54:06 local; repair 5 =
`p4_20261105/CONS_MYTHOS_local.md` section 4, `r5_20261105/IMPL_NOTE.md`); `gate_arm.sh`'s memc block (206-row pins);
`src/devices/dev_mvme187.c:59-144` (unchanged since fix2); `r4_20261105/` (PRETABLE_4, its errata, table 4);
`r5_20261105/PRETABLE_5.out`, `T5_PREP.md`, `table5/PRED_MAP.txt`.  **Table 5 was still running while this was written**
(`table5/SCORES.txt`: 634 of 3,580 legs, only table 4's carried variants so far), so every status below that names a PRETABLE_5
cell is its exact PREDICTION -- the frozen probe run against a modelled device -- not yet a measurement.  Each replication shape
was looked up in PRETABLE_5.out by its cell name (for example `K_MB_chipid_or_C` = a keep into chipid at the memconf latch body,
gated on controller, op `|=`).  **NOCHANGE** there means the statement fires and changes nothing the probe reads; T5_PREP.md counts
that as probe-equivalent, NOT as a survivor.  Line numbers are of mvme187_memc_probe.py unless named.

**How the classes are used.**  SAME AS SIBLING only where the first run made the finding AND it was dealt with (the row says how).
Where the first run made it too but nothing acted on it, the row is OPEN and says so.  A ruling the round did not adopt is
SUPERSEDED, with what replaced it -- recorded here so a dissent never reads as agreement.

| # | finding (quoted briefly) | class | where / why |
|---|---|---|---|
| 1 | premises + R6: R10's pc implies eight accesses where the packet named seven; the pass-2 clause "about 116" rows; "the probe's R10 instruction list should be quoted in the contract" | SUPERSEDED | R10's list has eight accesses (:401-402) and its comment names all eight; `R10 pc` wants CODE+32, "eight instructions retired" (:414).  The seven came from the packet's description, not the probe.  "about 116" appears nowhere in the 206-row probe. |
| 2 | premise + change 1 + change 7(iv): R12's word memconf store precedes every +0x00/+0x04 access -- "write it into the probe as an asserted invariant", and disclose it | SUPERSEDED | It was load-bearing only for NB6 (no other session made a served store before a first memconf store).  Repair 5's R16 (phase 00) and R17 (phase 01) do exactly that, so NB6's cell is carried by `R16 cnf line` and `R17 cnf line` whatever R12's order.  The R12 comment states the order (:437); no assert was added. |
| 3 | §1: sixteen families IN and rowed -- A_B1 to A_B12, G_1, G_3, G_5, G_6 (A_B10 IN; G_6 enumerated: 16 cells, 15 caught, bit 3 by D3(d)) | SAME AS SIBLING | ADJ_MYTHOS.md §1 ruled the same sixteen IN (A_B10 as the G_5 cell).  Repair 4 rowed them: table 4 "the pass-3 seats' 33 in-bound families each red on the repair-4 row named for it" (r4_20261105/table4/VERDICT.md).  G_6's bit-3 cell: R14 at +0xe7, and R17 at +0xf3 since repair 5. |
| 4 | §1 and §3 ("D1: right"): G_2 (`&& len == 1` on the default latch test) is IN, rowed by D3(g) -- R4's first default access becomes a word load; "Nothing is OUT" | ADDRESSED | Dissent, recorded here.  The first run ruled G_2 OUT (len is read by neither guarded body), and CONS_MYTHOS_local.md §2 re-ruled it OUT ("r2 N3 is the len twin, OUT by the pass-3 ruling"); D3(g) was never applied.  The cell is red anyway: table 4 G_2_dlen1 146/148 on R13_line_text and R13_lines (PRETABLE_4.errata.md); clause (e) records "an incidental catch, NOT claimed" (:52-53).  No live consequence. |
| 5 | glm's FILED items stand: fold bit 9 and `>= 0x100` (equivalent), the unpinned notice prefix `[ mvme187_memc: ` | SAME AS SIBLING | ADJ_MYTHOS.md names bit 9 and `>= 0x100` as equivalents; the prefix is glm's own filing (p3_20261105/ollama_glm.txt), which the first run did not mention.  Unchanged and still right: DEVINIT registers a 0x200 window (dev_mvme187.c:174-176), and every `lines` row counts the `mvme187_memc:` token, so only the leading `[ ` is unpinned. |
| 6 | glm's FILED item stands: the undriven controller-1 WIDE memconf store | SUPERSEDED | Driven since repair 4 (the first run's change 5): R9's word store of 0xffffffff at +0x108 (:381), pinned by `R9 no wide` (:392). |
| 7 | NB1: a first default store ANDed into a served field before the latch under `write && !controller` (and the inside-latch `write` form); row: R14 readbacks | ADDRESSED | `R14 00 r2`, `R14 04 r4`, `R14 08 r5` after R14's zero store (repair 4; the first run's B4 and change 2).  Table 4 measured the inside-latch form (M_B4_* red on R14); PRETABLE_5 predicts the pre-latch form (`K_DT_*_and_W.nC`) red on the same three rows. |
| 8 | NB2: inside the default latch, `if (controller) F &= idata;`, green "today"; change 2: R13's word value 0x1234567e | ADDRESSED | As written (no direction gate) it is caught: R10's first default access is a controller-1 READ (idata 0), and PRETABLE_5 predicts `K_DB_chipid_and_C`, `_chiprev_`, `_memconf_` red on R10 00 r9, R10 04 r10, R10 08 r8.  The write-gated form is the residual CONS_MYTHOS_local.md §1 E names and FILES as a disclosed three-way joint ("invisible because R13's first c1 default store is 0xffffffff"); PRETABLE_5 scores it NOCHANGE.  Change 2 was not adopted (R13 stores 0xffffffff, the first run's change 1). |
| 9 | NB3 + change 5: inside the memconf latch, `if (controller) chipid \|= idata;` (also `^=`, also chiprev); row: R7 gains LD +0x00 and LD +0x04 | OPEN | Still uncovered.  The only controller-1 FIRST memconf stores are R7's 0x07, never followed by a chipid or chiprev read (:351-352), and R9's 0x00, the OR and XOR identity; repair 5's R7 tail reads memconf only.  PRETABLE_5 predicts `K_MB_chipid_or_C`, `K_MB_chipid_xor_C` and the chiprev twins `none -- UNOBSERVED` (survivors).  T5_PREP.md found the same gap independently and names the remedy ("chipid/chiprev read-backs at the end of R5, R7, R9, R13, R15, R17"). |
| 10 | NB4 (chipid): inside the memconf latch, `if (!controller) chipid &= idata;` | ADDRESSED | Caught since repair 5: R16's first memconf store is 0x07 through controller 0, and phase 10 reads chipid back (0x80 & 0x07 = 0).  PRETABLE_5: `K_MB_chipid_and_nC` red on R16_100b_r12, R16_00b_r13, R16_100c_r18, R16_00c_r19. |
| 11 | NB4 (chiprev, memconf), and change 1's word value 0x1234567c meant for it | OPEN | Still uncovered.  Every controller-0 first memconf store is 0x07, 0xff or 0xffffffff (R3, R5, R8, R12, R13, R15, R16, R17), so `chiprev &= idata` (1) and `memconf &= idata` (3) change nothing.  PRETABLE_5 scores `K_MB_chiprev_and_nC` and `K_MB_memconf_and_nC` NOCHANGE, which T5_PREP.md does not count as a survivor -- so table 5 will not surface it.  Same shape as NB2's filed residual, but at the memconf latch, and no ruling names it. |
| 12 | NB5: the served `case 0x00` keeping `&= idata` under `write && controller`; row: controller-1 stores of 0x7f / 0xfe | ADDRESSED | R12's controller-1 pairs (0xff then 0x00, one readback; repair 4, :445-447) red it on `R12 100 r10` and `R12 104 r11` (0x80 & 0 = 0).  PRETABLE_5: the W.C cell sits under `K_CI_chipid_and_C` (red on R12_100_r10 and the R16/R17 readbacks).  0x7f / 0xfe were not needed. |
| 13 | NB6: `case 0x00` (and 0x04): `if (writeflag == MEM_WRITE) d->warned_memconf = 1;` | ADDRESSED | Repair 5: R16 phase 00 and R17 phase 01 store to the served fields before their first memconf store.  PRETABLE_5 (`L_CI_M_set` and `L_CR_M_set` under W): red on R16_cnf_line, R16_lines, R17_cnf_line, R17_lines. |
| 14 | NB7: `case 0x08: if (controller) d->warned_default = 1;` | ADDRESSED | Repair 5 (CONS F2): R9's tail makes a default read after its controller-1 memconf stores (`R9 def line`).  PRETABLE_5 `L_MT_D_set_C`: red on R9_lines, R9_def_line, R16_def_line, R16_lines. |
| 15 | NB8: `case 0x00` (and 0x04): `if (controller) d->warned_memconf = 1;` | ADDRESSED | Repair 5: R16 and R17 make controller-1 served accesses before their first memconf store.  PRETABLE_5 (`L_CI_M_set_C`, `L_CR_M_set_C`): red on R16_cnf_line, R16_lines, R17_cnf_line, R17_lines. |
| 16 | "D3(b) as written REGRESSES" served `&=` (0xff is the AND identity; R12's 0 stores catch it today) | SAME AS SIBLING | ADJ_MYTHOS.md B3.  Repair 4 kept the 0x00 store after the 0xff (the first run's change 3); table 4: M_B3_chipid red on R12_00_r2, R12_100_r10, R12_w00_r6 and M_B3_chiprev on R12_04_r4, R12_104_r11 -- the ruling's freshness check. |
| 17 | premise: if the text rows match a fragment, a value guard dropped to unconditional (": 0x0" on the read notices) may pass | ADDRESSED | Every text row matches through the notice's closing " (once) ]" (docstring :25-26), e.g. `R4 line text`, so an inserted ": 0x0" fails it. |
| 18 | D2 / change 6: rewrite the value axis (per field, one value with every bit set and one clearing the field's own set bits) and add a gate axis {none, write, read, ctl0, ctl1, latch clear}, single gates rowed, two-gate joints disclosed | SUPERSEDED | Replaced by CONS_MYTHOS_local.md §3's closed enumeration L (ten positions, both latches, keep forms, every conjunction over direction, controller and the two latches, single value and offset bits), which repair 5 implements and PRETABLE_5 walks.  The value-axis principle survives in rows 9 and 11. |
| 19 | change 1: R12's served stores of 0x7f / 0xfe (or keep the 0 stores); controller-1 stores of 0x7f / 0xfe; a readback after every store | SUPERSEDED | The first run's design was adopted: 0xff then 0x00 per field and controller, one readback (repair 4, :445-447); it reds all four operators and NB5.  Change 1's word value is row 11; its assert is row 2. |
| 20 | change 3: R14 gains LD +0x00, +0x04, +0x08 (pc CODE+20) | SAME AS SIBLING | The first run's change 2 adds the same readbacks; present as `R14 00 r2`, `R14 04 r4`, `R14 08 r5`, `R14 pc` CODE+20 (:493-503). |
| 21 | change 4: R15 rebuilt as LD +0x00, ST +0x100 0x7f, LD +0x04, ST +0x104 0xfe, ST +0x108 0x07, LD +0x0c | SUPERSEDED | Not built.  Its targets (A_B5, A_B6, NB6-NB8: every single-gated latch set at the served arms) are carried by repair 5's R16/R17 phase design and the R9 tail (rows 13-15). |
| 22 | change 7 (i) and (iii): disclose the masked OR into a field's own set bits, and widths other than 1 and 4 | ADDRESSED | Clause (e) discloses both: "an OR-keep of a served field's own set bits (chipid bit 7, chiprev bit 0, memconf bits 0-1)" (:70-71) and "access width -- G_2 is outside the bound, halfword first accesses are not driven ..." (:72-73). |
| 23 | change 7 (ii): disclose all two-gate joints | SUPERSEDED | CONS §3 CLAIMS every conjunction over direction, controller and the two latches instead; its disclosures are a bit jointly with a predicate, multi-bit masks, len, and even-count toggles. |
| 24 | change 7: "PRETABLE_4 must predict NB1-NB8 plus the 17 families" | SUPERSEDED | Banked after table 4 had run; PRETABLE_4 predicted the first run's B1-B6.  PRETABLE_5 (written 02:32 local) walks every NB shape as a cell of L -- rows 7-15 give each prediction. |
| 25 | R1 upheld: the notice is three fatal() calls with its own value guard; A_B7 and G_1 are single edits | SAME AS SIBLING | ADJ_MYTHOS.md R1; clause (e) rewritten by repair 4 ("the write notice's value guard or direction conditioned on the controller (A_B7, G_1: R13)"). |
| 26 | R2 upheld: "DERIVED" held for `=` only | SAME AS SIBLING | ADJ_MYTHOS.md R2; clause (e): "a served store kept by =, \|=, ^= or &=". |
| 27 | R3 upheld: say "no bit of 0xff outside the size code was kept" | SAME AS SIBLING | ADJ_MYTHOS.md R3; the `R3 cnf r2` note says exactly that (:283). |
| 28 | R5 (nit): "+0x7c (first byte past the struct)" and "+0x7c reads 0: no image byte forwarded" are imprecise -- +0x7c is past memcreg but inside struct mvme187_data (the first latch byte); say "past the register image" | OPEN | Still there: `rd 0x7c` note "first byte past the struct" (:265), `R3 7c r4` "the past-struct load reads 0" (:284), R8's comment and row notes "no image byte forwarded" (:365, :371).  The sibling did not raise it. |
| 29 | verdict: APPLY-WITH-CHANGES (seven changes) | SAME AS SIBLING | Both runs ruled APPLY-WITH-CHANGES; repair 4 applied the first run's seven (PRETABLE_4, table 4: 112 of 112 red). |

**Counts.**  29 findings: ADDRESSED 10, SAME AS SIBLING 8, SUPERSEDED 8, OPEN 3.

## OPEN items only

1. (row 9) NB3: a keep into chipid or chiprev with `|=` / `^=` at the memconf latch body, gated on controller, is green -- no
   controller-1 first memconf store is followed by a chipid/chiprev read except R9's, whose value 0x00 is the identity.
   PRETABLE_5 already predicts it a survivor (UNOBSERVED) and T5_PREP.md names the owed read-backs, so table 5's ruling will see it.
2. (row 11) NB4 for chiprev and memconf: an `&=` keep at the memconf latch body under `!controller` is green -- every
   controller-0 first memconf store keeps bit 0 and bits 0-1 set.  **At risk of disappearing:** PRETABLE_5 scores it NOCHANGE,
   which table 5's verdict does not count as a survivor.  Remedy as the replication says: a controller-0 first memconf store whose
   low byte clears those bits, then chiprev and memconf read back -- or a ruling that discloses it as NB2's residual was disclosed.
3. (row 28) The `rd 0x7c`, `R3 7c r4` and R8 notes say "past the struct" / "no image byte" where +0x7c is past memcreg, on the
   latches; wording only.

Notes for the ruling that takes rows 9 and 11.  CONS §3's keep-form map assigns controller-gated keeps to "R3/R9 (memconf 0x00
stores)", which cannot see either: R3's 0x00 store is not a first store, and 0x00 is the OR/XOR identity.  The current clause (e)
still carries repair 4's disclosure of "three-way joints of a gate, a position (first or non-first) and an operator", which reads
on both shapes, but CONS §3's contract sentence -- the one repair 5 is implementing -- claims any gate over the function's own tests
at any position.  And under the replication's own D2 gate axis ("inside either latch" is a gate value) NB2-NB4 are two-gate
joints that its change 7(ii) would disclose: weigh that before treating them as floor breaches.
