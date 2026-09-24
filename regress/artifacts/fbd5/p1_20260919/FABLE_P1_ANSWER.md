FABLE_SEAT_ALIVE_20260919_FBD5

`# CHECKPOINT -- 2026-09-19 07:0x   HEAD: f685d75 (peer records) > 9c28ca5 #539 receipt (7836071 = #539 n6, the footbridge IRQEnable read ACCEPTED)`

## VERDICT: PROCEED AMENDED. Main loop's Q1 call (28Ch NOT this round) STANDS, on the reopening rule's witness clause rather than on the addition licence; codex's offline split (Q2) ACCEPTED as detector-only with one implementation hazard; five `int` latches (Q3), N0 still owed; two accepted dispositions NARROWED (C1's "direct datasheet warrant", B4's dismissal of :1652), one adopted item (C2) carries a NULL-callback obligation; armdesc3kill MED, armdacr2kill MED-LOW; IRQSoft is its OWN row and the next easy item -- it is also the missing guest route to a nonzero `irq_status`.

## Q1 -- the 28Ch twin

**Main loop is right; Grok's reason is incomplete; Opus's argument is true and does not buy what it claims.**

Grok rests on the addition licence's *measured delta* leg. The licence has a second leg -- a *transferred warrant* -- and it is available here: `:6801` ("the control registers for the nFIQ and nIRQ control are identical") plus this round's own disposition at 18Ch. So the licence does not bar the edit. What bars it is the reopening rule: a second site joins only if **witnessed**. A read of +0x28c returns 0 on HEAD and returns 0 after any latched announce is added (`:633-636`, measured by Opus). There is no red-pre-fix/green-post-fix symptom; the only observable that changes is a host log line, which is a detector channel, not a defect symptom. Unwitnessed sites are ineligible, however cheap.

Opus's parity point is correct as a fact and wrong as a warrant: adding one field takes the controller from four dispositions to three (190h/290h stay unlatched through `default:`), so parity is not restored, and the honest disposition for the whole FIQ half -- `fiq_status` unwritten, `fiq_enable` unreadable at +0x288 -- is ONE FIQ round, which is what `fiqenableread` already is. Three obligations, all cheap: the contract line D8 (in the probe header, not only `PRETABLE.out`, which is an artifact); `fiqenableread` facet (2) carries Opus's sentence VERBATIM as the dissent; and that round's fix uses whatever latch form Q3 sets, so the choice below is being made for six sites, not five.

## Q2 -- the offline split

**Acceptable, and correctly graded: rung-1 DETECTOR rows, never a witness.** `regress/diff_footbridge.c:99` `#include`s the shipped device and calls `dev_footbridge_access` directly (`:382-603` already do), so seeded-`irq_status` rows are in the file's existing shape.

What it discharges: `m_swallow` and the store-into-status class become MEASURED KILLS (seed `irq_status = 0x10`, `irq_enable = 0x30`; a constant-0 read arm and a `&=`-style store both red) -- coverage, not disclosure. What it only NARROWS: `m_fiqraw`. Seeding `fiq_status` pins the read EXPRESSION against a field no product code writes; the disclosure "no guest can reach a nonzero FIQ status" stays in clause (e) verbatim. The contract must name the split exactly as C2 says: guest rows = reachability, survival, latch count, TEXT; differential rows = preservation, expression.

**One hazard the seats did not name, and it is the carrier's NULL-callback stub artefact:** the differential stubs `interrupt_assert`/`deassert` only on `timer_irq[i]` (`:106-107`); `d->irq`'s callbacks stay NULL under `calloc`. A P-row that seeds the enable via a +0x188/+0x18c WRITE calls `INTERRUPT_ASSERT(d->irq)` on a NULL pointer. Seed by direct field write; drive only the five declined accesses and the legal status READS through the handler. Also `fatal()` is stubbed as a counter that discards the text (`:50-51`), so the offline rows may COUNT announces but the misname check (C6) stays a guest-row obligation.

## Q3 -- latch form

**Five `int` fields.** (1) The file has no idiom of its own, so the house plurality governs -- per-site latch fields (`dev_wdc.c`'s eleven `warned_*`). (2) Both of Opus's total escapes (`m_sharebit`, `m_onebit`) are edits that EXIST only in the bit-field form; five ints make the shared-bit class impossible by construction, whereas the enum-plus-`_NBITS` defence is a second mechanism buying back what ints give free. (3) `#490`'s lesson is that a shared bitfield's hazard is "who else writes this field"; today the answer is nobody, but `fiqenableread` will add writers.

**N0 is still owed.** Under ints the residual copy-paste shape is two arms testing/setting the SAME field, which produces the identical observable (4 of 5, or 1 of 5), and N0 is the ONLY row that runs two sites in one process -- the sole carrier of the (d) DEPENDS-ON cell for the latch operand. Storage choice changes which mutant is buildable, not whether the row is owed.

## Q4 -- which accepted dispositions are wrong

**C1 -- NARROW. "Table 7-1 is a DIRECT datasheet warrant" overstates it.** Table 7-1 is §7.1's *PCI Configuration Space* access legend (`:4505-4520`), and the extraction is STAGGERED -- six abbreviations in one column, six definitions in the other; `R` = "Read only. Writes have no effect." only by pairing strictly in order. The CSR sections reuse `R`/`WO` in their R/W columns, so the legend TRANSFERS; it is not a sentence about these registers. The direct sentence is `:6803`: **"The Status and RawStatus are read-only, and EnableClear and Soft are write-only."** Cite that first, the legend second with the stagger noted, or the template ships a citation a reader cannot reproduce.

**B4 -- NARROW the dismissal.** "These registers exist" is true of 18Ch for WRITES; Table 7-10's read column at 18Ch is `--`, so in the read direction no CSR is selected, and `:1652`'s "nonexistent CSR ... zeros are read" is closer than "analogy" -- Figure 7-2 (`:6814`) shows only RawStatus driving the CSR read path. Keep the word POLICY; record `:1652` + Figure 7-2 as the nearest datasheet support rather than waving it off.

**D7 -- SETTLE, do not defer to pass 2.** With C2 adopted the answer is: no free-running row (a load-sensitive oracle the sites probe's header already refuses), P-row offline, clause (e) says "no GUEST row observes a nonzero status." Leaving "pass 2 decides" in the template invites the frozen-decision class.

**C2 -- adopted WITH the NULL-callback condition above.** Everything else (B1-B3, D1-D6, D8-D10, C3-C8) I checked against the source or the datasheet and would not move. D6's token is verified: `machine.c:240` is `fatal("\nSorry, emulation \"%s\"", stype)`. D1's ids: the probe emits A1/A2/A2b/C1-C4/E*/I1/K1/D1 and nothing in S*/N*.

## Q5 -- filing

**`armdesc3kill` -- MED.** A LEGAL ARMv4/v5 descriptor (fine page table, `d&3 == 3`) ends the process at `memory_arm.c:252-254`. Legal value beats reserved value. Note member 5 IS available here -- this is the translation path, not device access; `fs = FAULT_TRANS_S; goto exception_return` (`:257`) is the cheap decline, IMPLEMENT (1 KB pages) is the honest one.

**`armdacr2kill` -- MED-LOW.** DACR value 2 is architecturally reserved/UNPREDICTABLE; `cpu_arm_coproc.c:203` stores it unfiltered, `memory_arm.c:153` derives `dav`, `:78-79` kills. Fix is one `case 2:` treated as no-access. Both need a rung-3 witness with MMU ON; the sites probe's arm T already builds that scaffold.

**IRQSoft belongs on its OWN row (`fbirqsoftunimpl`), not as `fiqenableread`'s sixth facet, and it is the next EASY item.** Two reasons. It is IRQ-side and live, while `fiqenableread` is the dead FIQ half. And §7.3.34 (`:6952-6962`) says IRQSoft sets RawStatus bit [1] -- **the only guest-controllable path to a NONZERO `irq_status` under single-step.** Implementing it (member 7: one `case`, set/clear bit 1 of `irq_status`, reassert; ~8 lines) converts this round's D7/`m_swallow` disclosure into a GUEST row in a later pass, retires an unlatched guest-drivable `fatal()` flood, and has a trivial rung-3 witness (write +0x190, read +0x184 -> bit 1). Rank it MED, above `fiqenableread`.

## Seat record
Model: Claude Fable 5.1 (`claude-fable-5-1`), review/adjudication seat, fired last.
Read: `fable_p1_packet.md`; `CHECKPOINT.md` (first line); `brief_fbd5_design.tpl.md`; `p1_findings.md`; `OPUS_P1_ANSWER.md` (whole); `GXEMUL-SEC/src/devices/dev_footbridge.c:498-760` plus field greps; `dc21285.txt:1640-1655, 4500-4522, 6795-6835, 6905-6962`; `regress/diff_footbridge.c` (include, stubs, call sites by grep); `src/cpus/memory_arm.c:70-85, 148-156, 240-262`; `src/cpus/cpu_arm_coproc.c:198-206`; `src/machines/machine.c:240` (grep); `regress/footbridge_sites_probe.py` row ids (grep); `OUTSTANDING_BUGS.md` OPEN LIST head and `fiqenableread` entries.
Ran: nothing -- no build, no probe, no gate; file reads only (cat/awk/grep). Edited nothing except this answer file.
