VERDICT: PROCEED WITH CHANGES (3)

FABLE_SEAT_ALIVE_20261102_577P1
Brief, first line, verbatim: `# PANEL PASS 1 -- `shblreset` (#577): a SuperH general exception taken with SR.BL set stores the power-on reset code where the manual says manual reset, and clobbers the TLB multiple-hit code`

Fable 5.1 review seat, pass 1 of #577 (`shblreset`). READ-ONLY: nothing built, nothing run, nothing modified. Everything below was checked against `git -C GXEMUL-SEC show HEAD:<path>` at `987cb596`, the HEAD copies of `regress/sh_tlbmulti_probe.py` and `regress/gate_sh_rounding.sh`, the four witness files under `regress/artifacts/shblreset/witness_20261102/`, and `_scratchpad/sh7750_hardware.txt` by absolute path. Where a premise is marked SETTLED it was re-derived from the tree or the manual, not from the brief.

The three changes, in order of weight:

1. REQUIRED, blocking the gate: the two proposed row names are too long for the gate's anchor. `tlbm bl general` is 15 characters and `tlbm bl multihit` is 16. The probe prints names through `%-14s` (probe :87) and the gate's per-row check is `count "$TMLOG" "^$v  .*ok$"` with TWO spaces (gate :257). A name longer than 13 characters leaves one space, the count is 0 against an expected 1, and both new per-row checks go red for a reason unrelated to the code. The gate's own comment at :203-207 states this cap ("Row names are capped at 13 CHARACTERS ... Two of #454's first-draft names broke it. Measure after any rename."). I simulated the probe's format string against the gate pattern: both proposed names fail the anchor; `tlbm blgen` (10) and `tlbm blmulti` (12), or `bl general` (10) and `bl multihit` (11), pass. Shorten the names (or widen the column and re-measure every existing row). This would be caught loudly by the first gate run, so it is not a silent trap, but it costs a gate cycle to find the hard way.

2. RECORDS, in the code comment and the round record: (a) the fix comment cites `:678-681` for EXPEVT H'020. That passage is the manual's REVISION HISTORY table (`:670` reads "Item Page Revision (See Manual for Details)"), a summary of an amendment, not the body text. The normative sentences are `:12376` (5.6.1 (2) Manual Reset, Sources: "When a general exception other than a user break occurs while the BL bit is set to 1 in SR"), `:12383-12384` ("Exception code H'020 is set in EXPEVT, initialization of VBR and SR is performed, and a branch is made to PC = H'A000 0000") and the usage note at `:13162-13166`. Cite the body; the revision row may stay as a second cite. (b) The brief's Q1(d) reasoning is wrong in its reason while right in its conclusion, see Q1(d) below; carry the corrected walk into the CHANGELOG block rather than the brief's version. (c) The brief's candidate (e) is described as two different things, see Q3(e); fix the wording before it is copied into a mutant table. (d) The user-break sentence in the new comment should say the manual SUPPRESSES a user break under BL at the UBC (CMF flag set, "exception handling is not started", `:41450-41452`), so no arm of this function will ever need a user-break case; "would be the other exemption" invites a future reader to add one here.

3. RECOMMENDED, not owed by the floor: one more general-code row at a code BELOW H'100 raised from a DIFFERENT site, a misaligned longword load (`mov.l @r1,r0` with an odd address, `SH_ALIGN_CHECK_LD` at `cpu_sh_instr.c:209-213`, EXPEVT_ADDR_ERR_LD H'0E0, no MMU setup, one instruction like TRAPA), want H'020 under BL. It reddens the brief's own disclosed escape (f) and the general half of (e) as written, and witnesses the load/store raise site under BL, which TRAPA does not. One more session of about ten seconds; pin 6 -> 9; name 13 characters or fewer (`tlbm bladdr`). UNMEASURED by me; the author should run it once before counting it.

## Q1, premise audit

Q1 (a) SETTLED, holds. Only H'140 needs exempting at HEAD. The brief gave the raiser of H'140; it did not give the full set of codes that reach `sh_exception()`. Enumerated by `git grep 'sh_exception(' HEAD -- src/`: RES_INST (`cpu_sh_instr.c:53`, `:245`, `:3212`, `:3237`, `:3294`, `:3713`), FPU_SLOT_DISABLE (`:62`), FPU_DISABLE (`:64`), ADDR_ERR_LD (`:212`), ADDR_ERR_ST (`:218`), SLOT_INST (`:2853`, `:3210`, `:3235`, `:3292`), TRAPA (`:2858`), TLB_PROT_LD/ST and TLB_MOD (`memory_sh.c:236-249`), TLB_MISS_LD/ST (`memory_sh.c:368-369`), and RESET_TLB_MULTI_HIT (`dev_sh4.c:1178-1179`), plus the one interrupt caller (`cpu_dyntrans.c:250`). Every exception code in that list except H'140 is in Table 5.2's General exception category, which 5.5.3 maps to a manual reset. EXPEVT_FPU (H'120) and EXPEVT_BREAK (H'1E0) have no raiser. H-UDI (H'000) has none. So the exemption set at HEAD is exactly {H'140}.

Q1 (b) SETTLED for the tree, OPEN for guests. No committed row runs with BL set: a grep of `regress/` at HEAD for an SR pre-set with bit 28 set (`sr=0x[13579bdf]`) matches only ARM `cpsr=` lines, and no probe but `sh_tlbmulti_probe.py` reads `expevt`. The in-tree readers of `cpu->cd.sh.expevt` are three: the EXPEVT register arm (`dev_sh4.c:1880-1884`, guest-visible), the register dump (`cpu_sh.c:795`) and the PROM layer (`sh_ipl_g.c:101`, which tests `== EXPEVT_TRAPA`; both H'000 and H'020 are "not TRAPA", so its behaviour is unchanged). Whether any guest OS reset handler branches on H'000 versus H'020 I could not settle (no guest source in scope); the fix moves the value to what the hardware produces, so a guest written for hardware cannot be worse off.

Q1 (c) SETTLED, holds, with a refinement. EXPEVT_BREAK appears only in its define (`sh4_exception.h:73`); no `0x1e0` raiser exists. The refinement is the manual's: under BL a UBC break does not raise an exception at all (`:41448-41452`), so the exemption lives at the (unmodelled) raiser, never in this block. See change 2(d).

Q1 (d) The CONCLUSION holds and the REASON in the brief is false. Walk: the only call with `intevt > 0` is `cpu_dyntrans.c:250`, gated at `:247` by `!(cpu->cd.sh.sr & SH_SR_BL)`; the SLEEP handler at `cpu_sh_instr.c:260-263` uses the same predicate. So no interrupt enters `sh_exception()` with BL set. But suppose one did: the block at `:910-918` rewrites the LOCAL `expevt` (0 for an interrupt call); then `:945-947` takes the `intevt > 0` branch, sets `expevt = -1` and never writes `cpu->cd.sh.expevt`; the switch takes `case -1` (`:961`). The rewrite is discarded before it is latched or dispatched on. So the block is inert for interrupts BY CONSTRUCTION, and the dyntrans gate is load-bearing for the manual's "held pending under BL" behaviour (`:12306-12307`), not for protecting EXPEVT. The brief's sentence "an interrupt delivered with BL set would be rewritten too, so the cpu_dyntrans.c gate is load-bearing" should not go into the record. The fix comment's text ("Interrupts do not reach this path: cpu_dyntrans.c gates their delivery on BL") is true as written and can stay. NMI: `SH_INTEVT_NMI` (H'1C0) appears only at `cpu_sh.c:208` (table init) and its define; nothing asserts it; ICR/NMIB is not modelled (`dev_sh4.c:2489-2509`). The old comment's NMI worry has no code behind it, and would be inert for the same reason as any interrupt.

Q1 (e) SETTLED, holds. TRAPA #imm is `1100 0011 iiiiiiii`, so `0xc301` is `trapa #1`. The three stores are the committed probe's own words (`:77-79`): `0x2102` = `mov.l r0,@r1`, `0x2542` = `mov.l r4,@r5`, `0x2762` = `mov.l r6,@r7` (`0010 nnnn mmmm 0010`). Wants match the header: H'020 (`:58`), H'160 (`:70`), H'140 (`:59`), PC `0xa0000000` (`cpu_sh.c:1018`). The `print expevt` channel is proven by the control row returning H'160. Both `.out` files carry `binary newer than cpu_sh.c: yes` and the completion sentinel; the fixed clone's `.MUTANT` line says "scratch clone, intentional", which is the honest form. `apply_fix577.py`'s find and replace text is byte-identical to the brief's diff. I did not open `product.diff`.

Other premises re-derived: the three `cpu_sh.c` quotes and the `cpu_dyntrans.c` quote are byte-identical to HEAD; all five EXPEVT and three SR constants match; `EXPEVT_RESET_MANUAL` appears only at `sh4_exception.h:58` and `cpu_sh.c:1016`; `git log -L910,918` returns one commit, `39748e3c`, the upstream import; `grep -c shblreset CHANGELOG.md` is 0; `OUTSTANDING_BUGS.md:24063` carries the id; the ledger row is open, MED, with no stages. The probe's `:55-57` note is as quoted. Gate `:254` pins 6 by equality and `:256-259` is the per-row loop. The landisk default SR is BL clear from two independent sources: `cpu_sh.c:123` initialises `sr = SH_SR_MD | SH_SR_IMASK` and the PROM layer sets only `vbr` (`sh_ipl_g.c:55`); and the committed `tlbm expevt` row reads H'140 on HEAD, which under the BL rewrite would read H'000.

## Q2, the partition

Over {general exception, TLB multiple hit, interrupt, user break} x {BL clear, BL set}:

| cell | reachable at HEAD | fix changes it | member |
|---|---|---|---|
| general, BL clear | yes | no | not this detector; the gate's round-80 rows `trapa in slot`, `fp in slot` (gate `:213-218`) and the other SH probes |
| general, BL set | yes | YES: H'000 -> H'020 | new `bl general` row |
| multiple hit, BL clear | yes | no | committed `tlbm expevt` (H'140), `tlbm pc`, `tlbm vbr`, `tlbm sr` |
| multiple hit, BL set | yes | YES: H'000 -> H'140 | new `bl multihit` row |
| interrupt, BL clear | yes | no (does not pass the block's effect; `:945-947`) | `sh_intprio` and #455 rows elsewhere |
| interrupt, BL set | NOT reachable (`cpu_dyntrans.c:247`, `cpu_sh_instr.c:260`), and inert if it were | no | none; by construction, say so in the contract |
| user break, either | NOT reachable (no raiser); hardware suppresses it under BL | no | none |

The two changed cells each get a row; the two unchanged reachable cells are held by committed rows; the two unreachable cells need no row and the contract should name them as by-construction. Within "general, BL set" the body tests `expevt` only as {== H'140, != H'140}, so the body-tested partition is two cells and both are rowed; the general codes other than TRAPA are a sampled slice, which is what change 3 widens by one.

## Q3, the brief's six candidate edits

Assessed by reading, none built. "First differing input" is the first value a caller passes at HEAD on which the edit's EXPEVT differs from the fixed form.

| edit | equivalent? | first differing input | row that reds | class |
|---|---|---|---|---|
| (a) the HEAD line kept | no | any BL-set exception | `bl general` (H'000 vs H'020) and `bl multihit` (H'000 vs H'140); both MEASURED red on HEAD in `witness_head.out` | floor (b) |
| (b) block deleted | no | TRAPA under BL: H'160 latched, general vector taken | `bl general` red (H'160); `bl multihit` GREEN by construction, as the brief says; the `fatal()` print also disappears and no row reads it | floor (c), carried by `bl general` alone; state it |
| (c) exemption removed | no | multiple hit under BL: H'020 | `bl multihit` red | floor (d) |
| (d) exemption keyed to TRAPA | no | TRAPA under BL: H'160; multiple hit under BL: H'020 | both red | floor (d) |
| (e) as WRITTEN, `< 0x100` | no, and the brief describes it as two different edits | multiple hit under BL: H'140 is NOT below H'100, so it is rewritten to H'020 | `bl multihit` red | the caught half is floor (d); the other half, keeping H'040..H'0E0 (TLB miss, protection, initial write, address error load) under BL instead of H'020, differs at inputs no row drives: clause (e), reddened by change 3 |
| (e) as GLOSSED, "every reset-category code" exempted | YES, equivalent | none: no caller passes H'000 or H'020 as `expevt`, so exempting them too changes nothing reachable | none, correctly | an equivalent form, not a gap |
| (f) rewrite only when `expevt == TRAPA` | no | every general code other than TRAPA under BL (RES_INST, address error, TLB miss, FPU disable, slot) | NONE of the proposed rows; escapes 8/8 | clause (e) under the body-tested-partition bound; change 3 reddens it |

Should a second general-code row ride? Not owed: the floor is the body-tested partition, and TRAPA plus the multiple hit occupy both cells. Recommended anyway, as change 3, because one row at a sub-H'100 code from a different raise site reddens both disclosed shapes ((f), and the general half of (e) as written) for one session, and it is the cheapest row that does.

## Q4, option-set completeness

Members, with disposition: (1) document only: rejected, the value is guest-visible through the EXPEVT register and the witness shows both halves. (2) correct the constant with no exemption: wrong for the multiple hit, Table 5.2 `:12006/:12010` and `:12461`. (3) constant plus the one-code exemption, the proposal: correct for every code raised at HEAD (Q1 (a)). (4) exempt by CATEGORY (every code the reset arm at `:1015-1017` handles): equivalent today, slightly more future-proof if a raiser for H-UDI or another reset code ever appears; a three-term predicate; either (3) or (4) is acceptable, and (3) is the minimal one since the comment already names the category. (5) model the manual reset's module initialisation (Initialize_CPU, Initialize_Module(Manual)): that is the open MED row `shresetinit`, correctly out of this round. (6) remove the `fatal()`: no, it announces a real guest event (a fault taken under BL ends in a reset), which is the diagnostic a guest developer wants. (7) latch the `fatal()`: see below. ALIAS and FAULT do not apply (no address decode, no bus).

The latch. Keep it with `floodclass`; do not ride it here, and the reason is sharper than "second behaviour change". A `(once)` claim owes a row that the second occurrence does not print (claim -> row), and that row needs a channel this probe does not read (a count of the print across a two-fault session), so the rider is two lines of product code plus a new oracle, not two lines. The flood itself is real on HEAD and unchanged by the fix: after a BL fault the CPU restarts at `0xa0000000` with BL set, and if whatever it fetches there faults again the print repeats without bound. I could not settle what landisk executes at physical 0 (the 2 MB "boot ROM area" RAM, `machine_landisk.c:131-133`), so I state the loop as plausible, not measured. Record this site under `floodclass`.

## Q5, the vehicle

The committed rows do not re-pin: all six run BL clear, proved two ways in Q1 (above), and the fix touches nothing on the BL-clear path. `print expevt` works (`cpu_sh.c:137`, and the control row measured it). The pin 6 -> 8 by equality and the two names in the loop are the right shape; the names must shrink (change 1), and the pin becomes 9 if change 3 rides.

The SR pre-set `0x500000f0` is right in effect, and the brief's mechanism is slightly off. The debugger's `sr=` assignment writes the field directly through `CPU_SETTINGS_ADD_REGISTER32("sr", ...)` (`cpu_sh.c:129`); it does NOT go through `sh_update_sr()` (`:846-860`), so no bank swap happens at pre-set time whatever RB is set to. The `r0..r7` assignments and the program's stores both see `cpu->cd.sh.r[]` with nothing swapping banks in between, so the program works with RB clear or set. What RB clear buys is the SAME transition as the committed rows: the exception's `sh_update_sr(sr | MD | RB | BL)` then flips RB 0 -> 1 and swaps banks AFTER the stores, exactly as `tlbm sr` does, and the `sr` readback, if ever added, would be `0x700000f0` for both. Keep RB clear; reword the reason. IMASK 0xf is right: it keeps the dyntrans gate from delivering a pending interrupt on the step before the fault.

## Found while checking

* SLEEP under BL. The manual says interrupts are accepted in sleep mode even when BL is 1 (`:13170-13171`, `:17633`). The tree blocks acceptance on BL with no sleep exception, in both the dyntrans gate (`cpu_dyntrans.c:247`) and the SLEEP handler (`cpu_sh_instr.c:260-263`), so a guest that executes SLEEP with BL set never wakes in the emulator. Unwitnessed; probably not hit by shipped kernels (idle loops run with BL clear). Filing candidate, outside this round.
* The #457 comment at `cpu_sh.c:985-989` ("EXPEVT survives the grouping by construction ... the guest's reset handler can tell a multiple hit from a power-on or a manual reset") was true only with BL clear; this fix makes it true unconditionally. One clause there naming #577 would close the astraretro L4 rider on that passage.
* `ollama_glm.txt` in this pass-1 directory is 70 bytes; I did not read it, but a 70-byte cloud-seat file is the error-file size, not an answer. Check the seat.

## Not settled from this packet or the tree

* Whether any guest OS reset handler distinguishes H'000 from H'020 (no guest source in scope).
* What landisk fetches at `0xa0000000` after a BL fault, hence whether the `fatal()` repeats without bound (relevant only to the flood disclosure).
* Change 3 is a reading, not a measurement; the misaligned-load macro is unconditional on alignment, so I expect it to raise, but run it once.
* `product.diff` was not opened; `apply_fix577.py` carries the same edit text as the brief.

VERDICT: PROCEED WITH CHANGES (3)
