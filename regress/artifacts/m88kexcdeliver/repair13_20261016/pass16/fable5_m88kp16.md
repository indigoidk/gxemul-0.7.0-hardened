FABLE_M88KP16_20261016
# CHECKPOINT -- 2026-10-07 11:3x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)
VERDICT: CLOSE (the 48-cell enumeration verifies 48/48 against ROWS, the raise-site census and the t20b logs -- no mis-credited cell, no vacuous row, no fifth tested input, no single-edit sweep inside the grid; the eight unreachable cells are unreachable as ENTRY cells on a sourced warrant.  CLOSE with the denominator RESTATED, because the packet's closing sentence is false as worded: the 24 slot cells are killed in table 20/20b (14 under a single-cell discriminator, 10 under a 2-to-4-cell mutant that contains the cell), and the 24 slot-0 cells are killed in killtable5/7/10/11/13 on earlier instruments -- NOT "each under its own mutant in table 20".  Four records items ride on the v24 commit and none is a floor breach: name the `no instr(tbnd)' warrant under the unreachable cells; disclose the fallback's trap-in-slot clause-(e) sub-cell (`&& !(cpu->delay_slot && is_trap)' at :799, PREDICTED 84/84); the commit names THREE probe md5s, and the packet's "table 20 scored this code" premise is off by one instrument (it is table 20b's); file the two measured user-trap escapes under a tracker id, not only a docstring line.)

Seat: Fable 5.1 (Agent, file-reading, read-only).  Pass 16 of `m88kexcdeliver' (#502), the closing pass on repair 15
(probe v24).  Nothing built, nothing run against a binary; the only measurement I made was in-memory (an AST compare
and a name-set census, no file written); the only file written is this one.  Every score is marked READ (a preserved
log under `repair13_20261016/') or PREDICTED (traced from the source and the row table).

## 0. Evidence basis, and three provenance facts the packet states imprecisely

1. **Table 20 and table 20b are complete and self-consistent.**  All 39 `t20_*.out` and all 7 `t20b_*.out` end in
   `M88KEXC_DONE` (every one, read); `driver20.out` / `driver20b.out` carry `MUT20_OK' for every mutant, "clone source
   restored (cmp vs HEAD clean); sentinel cleared", `TABLE20_DONE 20:49:56' / `TABLE20B_DONE 21:02:50'.  Every score in
   the packet's section 3 matches the `M88KEXC_RESULT=' line of its log (READ, all 46).  `PRETABLE_20.out' (19:55)
   precedes `t20_BASE.out' (19:57); `PRETABLE_20b.out' (20:51) precedes `t20b_BASE.out' (20:53).  The one prediction
   miss (M_DS865 73/84 against 72/84) is the trapfrozen9dslot geometry, diagnosed in PRETABLE_20b and re-measured.
2. **The working-tree probe is code-identical to table 20b's instrument, NOT table 20's.**  Measured in memory:
   `ast.dump' of the working tree (md5 c44c97ae) with the module docstring dropped EQUALS that of
   `m88k_exc_probe_v24b.FROZEN.py' (md5 a1359e12, `probe_v24b.md5'); the full ASTs differ (docstring only; the line
   diff is 52a53-57, 209-213c214-222, 215c224-225, all inside the docstring, which runs from line 2 to the `"""' at
   :259, `import' at :260).  Against table 20's `m88k_exc_probe_v24.FROZEN.py' (md5 a035efeb) the code DIFFERS: 17
   changed lines = the docstring block plus `trapfrozen9dslot''s handler word (`BR_N_PLUS8' -> `BR_N_PLUS16' and five
   comment lines).  So section 2's last premise ("the frozen instrument table 20 scored ... AST-identical") names the
   wrong table.  The measurement is still complete: each row runs in its own `Sess()', so table 20's scores transfer to
   v24b for every row but trapfrozen9dslot, and table 20b re-ran every mutant that can reach that row's second fault
   (the OVF arm's four, `:816''s RRDS_OVF and the label-free RRTDS, `:865''s DS865 -- I enumerated the other 32:
   ARMTSU_OVF exempts SFRZ-clear only, RRNTDS keeps traps, the fallback and user-trap forms never see vector 9, and
   every other arm mutant is at a label the row never enters frozen; its first fault at DIV0 is slot-0 and no table-20
   mutant exempts a slot-0 cell).
3. **Gate 11 on v24b: PASS, 111 checks** (READ, `gate11_v24.out', 21:03-21:08): `M88KEXC_RESULT=84/84', the two slot
   checks `ok' at 12 and 14, on `cpu_m88k.c' md5 3593a8a5 = `base.md5' with `[gxemul -nt src]' in the runner.
4. **The ledger at HEAD (16512e9c) carries what K8 says it does** (READ): 104 entries on `m88kexcdeliver', the four
   pass-15 seats and the five unfired seats (opus5, agy, kimi, deepseek, minimax) by name and reason, dated
   2026-10-16; `m88ksfd1row' is `closed' with its KEEP ruling in the `closure' field (by `opus5-mainloop', badge A).
   The working-tree ledger diff touches only the peer's lca rows -- NO pass-16 entry has been written ahead of the
   seats, which is the right state for a frozen-number-averse record.  Pass 16 and repair 15 are therefore OWED by
   the v24 commit (CHANGELOG.md and OUTSTANDING_BUGS.md are also unmodified in the tree).
5. **The deriver's hand table matches the probe today, measured**: the 84 `FAULTS' keys in `derive_cells.py' equal
   the probe's 84 fault-row names (86 `ROWS' entries minus the `live'/`attrib' controls); nothing is in one set and
   not the other.  The script still does not assert it (my pass-15 tooling note stands).

## 1. Q1 -- the 48 cells, each credited row checked against ROWS, the raise sites and a log.  NO MIS-CREDITED CELL.

How each coordinate was verified rather than assumed:
* LABEL and is_trap -- the raise-site census, re-run: `grep -rn 'm88k_exception(' src/' gives 81 call sites.  Every
  one passes a LITERAL with is_trap 0 -- OVERFLOW (`cpu_m88k_instr.c:585/:639/:697'), ILLEGAL_INTEGER_DIVIDE
  (`:612/:624/:719/:731'), PRIVILEGE (`:816-:863, :2233/:2245, :2515/:2546/:2559'), UNIMPLEMENTED (`:2450'),
  MISALIGNED (`cpu_m88k_instr_loadstore.c:172'), SFU1_PRECISE (the rest), INTERRUPT (`cpu_dyntrans.c:214'),
  INSTRUCTION/DATA_ACCESS (`memory_rw.c:620'; `memory_m88k.c:417' whose `exception_type' is `instr ?
  INSTRUCTION_ACCESS : DATA_ACCESS' at `:109-110', domain {2, 3}) -- EXCEPT the three `ic->arg[2]' sites with is_trap
  1 (`:2529/:2551/:2564', tcnd/tb0/tb1), whose `arg[2]' is `iword & 0x1ff' (decoder `:3542/:3553').  No literal is 7
  or 10.  The ERROR written at `:817' is INTERNAL (a rewrite after switch 1, never an entry value).
  *A wrong record of MINE on pass 15, corrected here: I wrote "MISALIGNED through `memory_m88k.c:417'".  That site's
  domain is {INSTRUCTION_ACCESS, DATA_ACCESS}; the MISALIGNED raise is `cpu_m88k_instr_loadstore.c:172'.  The
  conclusion was unaffected; the citation was wrong.*
* SLOT -- unfrozen rows carry the else-arm shadows (SFIP = delay_target|V = 0x10016 against SNIP+4 = 0x10012), which
  only `:840''s slot branch produces (READ, t20b_BASE, all twelve dslot* rows); frozen rows skip the shadow update, so
  their slot evidence is M_DS865: all twelve STOP at the SELF their br.n targets (READ, t20b_M_DS865: 0x48 for
  trapfrozen4/5/6/7/10dslot and the two-word errdslot*, 0x4c for the three-word errdslot*, 0x50 for trapfrozen8dslot
  and trapfrozen9dslot) -- X(br_n) jumps there only if the exception ran mid-branch, and on BASE the same rows DELIVER.
* SFRZ -- the second fault of every two-fault row runs under the PSR the first delivery left (0x8000000b) or the
  handler's FRZ* value, every one with bit 0 set; the frozen rows show the first fault's shadows (SXIP 0x10006) and
  the refatal diagnostic exactly where REFATAL_EXPECT says (READ).

Cell by cell (first row named; +N as the deriver prints it; every credit re-read in ROWS :357-:577):
* (SFRZ 0, slot 0, fault): misalign +1 (umisalign); unimpl; priv +1 (privtb: a USER tb1 naming 8 takes X(tb1)'s
  filter at `:2559' and raises PRIVILEGE with is_trap 0 -- correctly NOT in TRAPAT); div0 +37 (udiv0 and the first
  fault of every two-fault row, including the five new trapfrozen4/5/6/9dslot and sfu1hdslot); indclr +5 (ovf, ovfc,
  uovf, trapfrozen8 and trapfrozen8dslot's first faults -- `add 0x7fffffff + 1'); BOUNDS / ERROR unreachable.
* (0, 0, trap): misaligntb; unimpltb +1 (unimpltbc); privsuptb +1 (privtbc); bounds +2 (vbrtb, boundstbc); div0tb +1
  (div0tbc); ovftb +1 (ovftbser); errortb +1 (errortbc) -- supervisor tb1 naming 4..10 with r3 bit 0 set, `:2564'.
* (0, 1, fault): dslot, dslotmisalign, dslotunimpl (user, prom_call), dslotpriv (user, ldcr), dslotovf -- `br.n +16'
  immediately before the faulting word, SFRZ clear; delivered at 0x40/0x20/0x28/0x30/0x48 with the else-arm shadows.
* (0, 1, trap): dslotbounds, dsloterror (v23) and the five v24 `dslot<L>tb' = `[BR_N_PLUS16, TB1_0_R3_L]', r3 = 1,
  PSR_RESET.  READ on t20b_BASE: pc = entry (0x20/0x28/0x30/0x40/0x48), sxip 0x0001000a, snip 0x0001000e, sfip
  0x00010016, psr 0x8000000b, epsr 0x80000002, r2 0xdeadbeef.  Trace (dslotmisaligntb): MARK at 0x10000 copies r10 to
  r9; br.n at 0x10004 sets delay_target 0x10014 and `delay_slot = TO_BE_DELAYED' (X(br_n):96) and calls the slot
  word; tb1 at 0x10008, MODE set so the filter is skipped, r3 & 1 -> m88k_exception(4, 1); MISALIGN implemented;
  `:811' SFRZ clear -> EPSR = 0x80000002; PSR |= 0x9 -> 0x8000000b; SXIP = 0x10008|2; `:840' truthy, vector not 2/3
  -> SNIP = 0x1000c|2, SFIP = 0x10014|2; pc = 0x20; `:865' -> EXCEPTION_IN_DELAY_SLOT; switch 2 breaks; back in
  X(br_n) `:99' the bit is set so pc stays 0x20 -> breakpoint -> DELIVER with exactly the logged values.
* (1, 0, fault): errc +3 (error, errind, errser -- MISALIGN via the odd ld in the handler); errunimpl; errpriv;
  errdiv0 (stcr PSR_FRZSUP first so SFD1 is clear); errovf.  (1, 0, trap): trapfrozen4/5/6/8/9/10 and trapfrozen +4
  (ind, c, ser, sfd1) at BOUNDS.
* (1, 1, fault): errdslotmisalign, errdslotovf, errdslotdiv0, errdslotpriv, errdslotunimpl (verified on pass 15,
  unchanged in v24).
* (1, 1, trap): trapfrozen7dslot, trapfrozen10dslot (v23) and the five v24 `trapfrozen<L>dslot'.  READ on t20b_BASE:
  delivered at 0x20/0x28/0x30/0x40/0x48 with the FROZEN shadows (sxip 0x00010006, snip 0x0001000a, sfip 0x0001000e),
  psr 0x8000000b, epsr 0x80000002 (the first delivery's), r2 0xdeadbeef, no refatal.  Trace (trapfrozen6dslot): divu
  r2,r3,r0 at 0x10004 with SFD1 clear -> `:624' DIV0 unfrozen, shadows written, pc 0x40; handler `br.n +8' at 0x40
  (target 0x48 = the SELF planted after the handler), tb1 0,r3,6 at 0x44 in the slot, supervisor, r3 = 0x11 ->
  m88k_exception(6, 1); PRIV implemented; `:811' SFRZ set -> `:816' is_trap -> exempt, no fatal, update_shadow_regs
  false; pc = 0x30; `:865' -> EXCEPTION_IN_DELAY_SLOT; X(br_n) keeps pc -> breakpoint 0x30 -> DELIVER.
  trapfrozen8dslot: first fault OVERFLOW (handler_at = V_OVF, 0x48), `br.n +8' from 0x48 targets 0x50 = the SELF
  planted after its two-word handler, breakpoint 0x40.  trapfrozen9dslot (v24b): `br.n +16' from 0x40 targets 0x50
  (the ERROR entry, which the vector loop fills with SELF), breakpoint 0x48.  I re-derived every frozen row's
  (branch target, breakpoint) pair: 4/5/6dslot (0x48; 0x20/0x28/0x30), 7dslot (0x48; 0x38), 8dslot (0x50; 0x40),
  9dslot (0x50; 0x48), 10dslot (0x48; 0x50), errdslot* (0x48 or 0x4c; 0x50) -- no collision remains.

**The eight unreachable cells are unreachable AS ENTRY CELLS, on the census above -- and the warrant must be
named in the contract.**  The packet says "there is no `tbnd'".  Sharpen it: the DISASSEMBLER names tbnd
(`cpu_m88k.c:1649', `:1675'); the DECODER has no handler (`grep -c 'instr(tbnd)' src/cpus/cpu_m88k_instr.c' = 0;
the trap-form switch at `:3538-:3558' decodes only 0x34 tb0, 0x36 tb1, 0x3a tcnd and sends the rest to `bad').  So
the true absence record is "no non-trap raise site names 7 or 10 AND no `instr(tbnd)' exists" -- and it is
TIME-INDEXED: this fork implemented tcnd (#307); implementing tbnd the same way creates a non-trap route into
BOUNDS and turns four of the eight unreachable cells reachable.  The carrier's rule is that an absence record names
its warrant so the edit touching it re-runs the census.  One sentence in the probe contract (records, not floor).
Two further non-cells worth one sentence each, so the question is not re-asked: the re-routed state (vector = 10,
is_trap 0, SFRZ set, slot) is reached INTERNALLY by the five errdslot* rows (and the five slot-0 err* rows) -- it is
not an entry cell and it is exercised; and `cpu->delay_slot''s domain at entry for the seven labels is {NOT_DELAYED,
TO_BE_DELAYED} only (X(br_n):96 writes TO_BE_DELAYED before calling the slot word; DELAYED is never written in the
m88k files; EXCEPTION_IN_DELAY_SLOT is written at `:866' and cleared at X(br_n):101/:105 before any further guest
instruction), and the body's truthiness tests at `:840'/`:865' partition that domain exactly as the grid's D0/D1.

## 2. Q2 -- none of the eleven new rows is vacuous; each reds under its credited mutant through the predicted channel

All READ from the raw logs, not from `analyze_t20*.py' (whose summaries I would otherwise be ratifying):
* `dslot<L>tb' (five) under M_ARMTSU_<L> (`implemented = !(cpu->delay_slot && is_trap && !SFRZ)' at L, verified
  verbatim in `driver20.out'): 83/84 each, the row HALT at pc 0x00010014 with sxip/snip/sfip 0 -- the fallback halted
  inside the slot, `:865' never ran, X(br_n) jumped to delay_target.  HALT replaces DELIVER.  Also red under
  M_ARMTS_<L> (82/84, with trapfrozen<L>dslot) and M_DSNOT_<L> (80/84).
* `trapfrozen<L>dslot' (five) under M_RRDS_<L> (`!is_trap || (vector == L && cpu->delay_slot)' at `:816'): 83/84
  each (20b for OVF), the row STOP at pc 0x00000050 -- re-routed to ERROR, spinning on 0x50's SELF, the breakpoint
  at its own vector never reached.  Also red under M_ARMTS/M_DSNOT/M_DSFRZ_<L> (HALT at the SELF its br.n targets:
  0x48, or 0x50 for 8dslot/9dslot), M_DS865 (STOP, 20b: 0x48/0x48/0x48/0x50/0x50) and M_RRTDS (77/84, STOP at 0x50).
* `sfu1hdslot' under M_FBFRZDS (`&& !(cpu->delay_slot && SFRZ)' at `:799'): 83/84, the row STOP at pc 0x50 -- the
  fallback skipped, `:816' re-routed the frozen SFU1 fault to ERROR, no `unimplemented ... vector=0x072' diagnostic,
  so `halted' is false and the result is not HALT.  Also under M_FBDS (82/84, with usfu1dslot).  On BASE it HALTs
  with pc 0x48 (the fallback returned without `:865', X(br_n) jumped to the +8 target, the machine was already
  stopped) and the diagnostic names 0x072; a halt on the FIRST divu would name 0x008 and score STOP, so the row
  cannot pass for the pre-fix reason.
* The trapfrozen9dslot geometry: in table 20 (the +8 draft) it read DELIVER at 0x48 under M_DS865 -- the lost
  delivery landed on its own breakpoint -- and in 20b (+16) STOP at 0x50.  An L1 construction defect, caught by the
  PRETABLE prediction mismatch before any commit: the order discriminator doing its job.

## 3. Q3 -- the four-input claim is right; no fifth input; no sweeping single edit inside the 48 cells

Line by line over `:689-:981': switch 1 (`:696') tests `vector'; `:799' tests `vector < 128 && !implemented'
(`implemented' derived from vector); `:811' masks ONE PSR bit, SFRZ; `:816' tests `is_trap'; `:840' and `:865' test
`cpu->delay_slot''s truthiness; `:841/:844/:859' and `:882' and switch 2 test `vector'; `:902' tests `delay_slot &
EXCEPTION_IN_DELAY_SLOT' inside the INSTRUCTION_ACCESS arm only (not one of the seven).  Everything else is copied
(`:824' EPSR, `:837' pc, `:842/:847/:852' delay_target, `:910-:915' dmt/dmd/dma), ORed (`:827-:831') or written;
`:804''s `ncpus' is a loop bound in the fallback.  The callees `m88k_stcr' and `m88k_pc_to_pointers' are outside the
DEPENDS-ON bound.  Four inputs: vector, PSR & SFRZ, delay_slot, is_trap.  No fifth.

Mutant forms traced beyond table 20's 38, all PREDICTED, none a sweep:
* `:811' `(PSR & SFRZ) && !(delay_slot && is_trap)': the seven frozen slot traps get a shadow UPDATE (sxip = the slot
  pc) -> BADREGS -> 77/84.
* `:824' `if (!is_trap) EPSR = PSR': every unfrozen TRAP row, slot 0 and slot 1, reads epsr 0 -> BADREGS.  (So the
  is_trap axis at SFRZ-clear cells has an observable channel, EPSR, besides the arm-level HALT.)
* `:834' `update_shadow_regs && !(is_trap && delay_slot)': the seven unfrozen slot traps lose sxip -> BADREGS, 77/84.
* `:840' `delay_slot && !is_trap': those seven get slot-0 shadows (sfip 0x10012, not 0x10016) -> BADREGS, 77/84.
* `:841'/`:844' `|| vector == L': the (L, S0, D1, *) rows get snip = delay_target or sfip 0 -> BADREGS.
* `:863' conditioned on `!(delay_slot && is_trap)': the twelve slot traps STOP, 72/84.
* `:865' `&& !is_trap': the twelve slot traps lose the vector to X(br_n) -> STOP, 72/84; `&& is_trap': the ten slot
  faults, 74/84; `== DELAYED': all 24 slot rows, 60/84; `== TO_BE_DELAYED': EQUIVALENT on the reachable domain (an
  identity, not an escape).
* `:818' `if (!cpu->delay_slot) fatal(...)': the five errdslot* lose the diagnostic -> BADREGS refatal, 79/84.
* switch 2's seven-label arm gaining `if (delay_slot && is_trap) SNIP = SFIP = 0': the twelve slot traps BADREGS (the
  frozen ones too -- the write ignores update_shadow_regs), 72/84.
* The arm-level single-cell forms table 20 did not build: `!(delay_slot && !is_trap && !SFRZ)' at L5 (dslot<L>
  HALT), `!(delay_slot && !is_trap && SFRZ)' at L5 (errdslot<L> HALT), `!(delay_slot && !SFRZ)' at BOUNDS/ERROR
  (dslotbounds/dsloterror HALT), `!(delay_slot && is_trap && SFRZ)' at L5 (trapfrozen<L>dslot HALT): 83/84 each.
  Each is CONTAINED in a measured mutant's exemption set with the row red there (READ: dslot<L> and errdslot<L> HALT
  under M_DSNOT_<L>, errdslot<L> under M_DSFRZ_<L>, dslotbounds/dsloterror under M_DSNOT/M_ARMTS_BOUNDS/ERROR), and
  a row is its own session, so narrowing the exemption to the row's cell cannot turn it green.
Every cell has a row whose channel (pc / HALT / STOP / sxip / snip / sfip / psr / epsr / refatal / level) varies under
an edit conditioned on the four tested inputs at that cell.  The only single edits that sweep 84/84 are OUTSIDE the
grid: M_RRUT and M_DS840UT (measured, disclosed) and the fallback form in section 4.

## 4. Q4 -- the disclosures: complete except ONE unnamed clause-(e) sub-cell; the classifications are right

* user-trap labels x {slot}: measured (M_RRUT 84/84, M_DS840UT 84/84, READ), disclosed in the working-tree
  docstring.  Clause (e) is right: those labels take no edit, and the fix's repair (`implemented = true') is not on
  their path.  See D6 for what the carrier still requires of a disclosed measured escape.
* {slot} x {MODE, SER, C, SFD1, IND}: clause (e), correctly -- ORed at `:827-:831', copied at `:824', never tested.
* vectors 0..3's own delay-slot code: outside the seven labels; HEAD's docstring (`:216') carries the corrected
  pointer `m88kexcdebt' with `m88kexchwtraps' for the tail arms (K5 verified).
* **MISSING, and it should be named: {fallback} x {slot} x {is_trap = 1}** -- a supervisor trap IN A SLOT naming a
  residual vector (11..113, 116..127) or 114/115 by number.  The fallback at `:799' tests neither delay_slot nor
  is_trap, so it is clause (e) by the pass-14 four-seat ruling; v23/v24 rowed its two slot FAULT cells on measured
  escapes and the docstring now reads as if the fallback's slot cells were covered.  The trap sub-cell is not:
  `&& !(cpu->delay_slot && is_trap)' at `:799' is a PREDICTED 84/84 sweep (every slot trap row names one of the seven
  labels; the only fallback slot rows are divu-raised faults with is_trap 0).  Disclose it by name with that mutant,
  or row it for one session on the sfu1hdslot precedent (`residtbdslot': `[BR_N_PLUS16, TB1_0_R3_50]', r3 = 1,
  V_RESID, 0x10008, PSR_RESET, expected HALT naming 0x032 -- PREDICTED on HEAD: HALT with pc 0x10014, the fallback's
  slot-blind halt; under the mutant the trap is delivered to 0x190's SELF and reads STOP).  Not a floor item.
* And the `tbnd' warrant of section 1 belongs in the same contract paragraph.

## 5. Q5 -- D5 and D6, with me harder on my own side of each

**D5 -- is `is_trap' a floor axis?  Yes, on the carrier's text, and the ruling stands.**  The text: *"At each floor
cell, every idata bit the guarded body TESTS is written both clear and set.  The bare state floor above does not
catch M_ICLR -- an idata-bit x state joint -- and would grade the pass-11 escape as debt while the CHANGELOG grades it
L2"* (the 09-04 generating-set clause); *"'TESTS' MEANS MASKS OR COMPARES AS A CASE"* (09-25); *"A DERIVED INPUT IS
GRADED BY WHAT THE BODY TESTS ON IT"* (10-09).  `is_trap' is this function's per-call INPUT bit, compared as a case
at `:816'.  Grok and Astra are right that it is a per-raise selector and not persistent state -- and so is `idata',
the clause's own exemplar; the clause was added BESIDE the state floor precisely for the input-bit category that the
state floor cannot see.  Nothing in the carrier confines "input bit" to a register write, and the #549 D1 pin ("a
single bit of a COMPARED value is a two-axis joint ... NOT CLAIMED") is about a bit of a RELATIONALLY compared
value, which this is not -- `!is_trap' is the case test of a one-bit input whose generating set is {0, 1}.  Harder on
myself: the one narrower reading (the body tests is_trap only inside the SFRZ block, so the generating set applies
at the fourteen SFRZ-set cells only) would make the five unfrozen slot-trap cells clause (e) and the five frozen
ones floor; both readings forbade CLOSE on pass 15 and both are satisfied by v24, so no live disposition turns on
it.  The grade question: under the adopted reading passes 5 and 7 were L2, as the CHANGELOG records; under Grok's
they were clause (e), and the chain's own record would then grade one shape two ways -- the inconsistency the
coordinator named, and the reason the broad reading is the one consistent with the chain.

**D6 -- the user-trap labels: rows or disclosure?  Disclosure is in-rule, and I was too quick to say only that.**
My pass-15 position: disclose, because the labels are outside the fix's seven and trapfrozen128/450/496/511 were
voluntary closures.  Harder on myself: the chain's precedent IN THIS SAME REPAIR cuts the other way -- usfu1dslot and
sfu1hdslot are clause-(e) cells ROWED on measured escapes, and the user-trap slot cells have measured 84/84 escapes
and were not rowed.  Both dispositions are in-rule (row demand is per enumerated FLOOR mutant; an (e) row is an
addition-licence question, and a measured delta is exactly the licence).  What the carrier REQUIRES of a disclosed
(e) escape is *"FILE them, with the escape list recorded"* -- a docstring sentence is a disclosure, not a filing.
So: either GLM's two rows (`usertbdslot': `[BR_N_PLUS16, TB1_0_R3_128]', r3 = 1, V_USER0, 0x10008, PSR_RESET,
else-arm shadows PREDICTED, kills M_DS840UT by BADREGS sfip; `trapfrozen128dslot': `[DIVU_R2_R3_R0]', r3 = 0x11,
handler `[BR_N_PLUS8, TB1_0_R3_128]', breakpoint 0x400, frozen shadows, no refatal PREDICTED, kills M_RRUT by STOP at
0x50 -- two sessions), or a tracker id carrying both mutants with their 84/84 scores.  I hold CLOSE for neither; I
ask that the filing exist by name before the commit, which is a records line.

## 6. Q6 -- which ACCEPTED disposition is wrong

None of K1-K8 is wrong in substance.  Verified: K1 (the five M_RRDS 73/73, READ `ANALYSIS_19.out' and the t19 logs);
K2 (M_ARMTS_<L> 82/84 and M_ARMTSU_<L> 83/84, READ -- "measured on v24" is the honest form, since my 73/73 on v23
was never run); K3 (84/84 twice, READ); K4 (83/84, READ); K5 (HEAD `:216'); K7 (the floor alone, right); K8 (HEAD's
ledger, section 0.4).  **K6 is INCOMPLETE and its premise is a wrong record in the packet**: "the commit names the
md5s" is true of 16512e9c (1d400b64 / ac72cab1, read in its message) and the v24 commit owes THREE -- a035efeb (table
20, the +8 draft; 32 of its 38 scores stand), a1359e12 (table 20b, the shipped code), c44c97ae (committed,
docstring-only delta, proven by AST) -- and the packet's "the frozen instrument table 20 scored (AST-identical)" must
read table 20b.  Add my own pass-15 citation error (section 1) to the wrong-record list; this file is its correction.

## 7. Q7 -- the denominator, restated so the zero carries it

The proposed sentence -- *"all rowed and each killed under its own mutant in table 20"* -- is FALSE as worded for the
24 slot-0 cells: no table-20 mutant exempts a slot-0 cell (every arm mutant there carries `cpu->delay_slot &&', and
every site mutant conditions on delay_slot), so their kills live in killtable5 ({SFRZ set, non-trap} x class),
killtable7 (the frozen traps per class), killtable10/11/13 and the PSR tables -- measured on the instruments of
their day, unchanged rows, not re-run on v24.  The true statement:

> The floor is the 48 reachable cells of {7 labels} x {SFRZ} x {delay_slot} x {is_trap}; the 8 unreachable cells
> carry their warrant (no literal 7/10 raise site, no `instr(tbnd)').  All 48 are rowed (name set measured, 84 = 84).
> The 24 slot cells are each killed in table 20/20b (READ): 14 under a single-cell discriminator (ARMTSU_<L5>,
> RRDS_<L5>, DSFRZ_BOUNDS/ERROR) and 10 under a 2-to-4-cell mutant containing the cell (DSNOT_<L5> for dslot<L>,
> DSFRZ_<L5> for errdslot<L>, DSNOT/ARMTS_BOUNDS/ERROR for dslotbounds/dsloterror), their single-cell forms PREDICTED
> by containment.  The 24 slot-0 cells are killed in killtable5/7/10/11/13 on earlier instruments.  Everything else
> enumerated is clause (e): the PSR-bit cells (closed voluntarily, tables 11-15), the user-trap labels x slot (two
> measured 84/84 escapes, disclosed -- to be FILED), the fallback x slot (two cells rowed on measured escapes, the
> trap sub-cell disclosed with a PREDICTED 84/84), vectors 0..3 (`m88kexcdebt').

With that denominator: zero floor breaches surviving this pass, the diff delivered (nine hunks, verified against the
working tree), the roster complete or named (four seats; five unfired by name in the ledger).  CLOSE.

## 8. Records to carry into the v24 commit (L4 class; none blocks the verdict)

1. Commit message: the three probe md5s with their roles; "code-identical to table 20b's instrument".
2. Probe contract: the `tbnd' warrant sentence under the eight unreachable cells; the fallback trap-in-slot
   clause-(e) line with its mutant; one sentence on `delay_slot''s entry domain (optional).
3. `derive_cells.py': assert the FAULTS key set equals the probe's fault-row names (the unsafe direction is a row
   deleted from the probe and left in FAULTS, which prints ROWED).
4. A tracker id (or a fold into `m88kexcdebt') for the user-trap x slot escapes, naming M_RRUT and M_DS840UT, 84/84.
5. Ledger: pass 16 (four seats, five unfired by name), repair 15 with its table-20/20b artifacts; a CHANGELOG round
   block for repairs 13-15 (none exists in the tree); PRETABLE_20's miss stays as written, corrected by PRETABLE_20b.

## 9. Not established here

No build, no run.  Every score not quoted from a t19/t20/t20b/gate log is PREDICTED from X(br_n), X(tb1),
m88k_exception and the row table.  The decoder's `bad' behaviour was not read (irrelevant to the census: the only
UNIMPLEMENTED raise is `:2450').  The legality of a trap in a `.n' slot on MC88100 silicon remains unsettled from the
manual on disk and remains irrelevant to whether the cells are owed.  The broad-versus-narrow generating-set reading
is settled by the coordinator's ruling, which the owner may overturn; the verdict does not depend on it.
