FABLE_M88KCLOSE_20261016
VERDICT: DO NOT CLOSE (the closing pass's 56-cell denominator omits `cpu->delay_slot` -- the one CPU-state lvalue `m88k_exception()`'s repair path TESTS -- and {MISALIGN, UNIMPL, PRIV, OVF} x {delay slot set} are unrowed; `implemented = !cpu->delay_slot` at any of those four arms is a PREDICTED 59/59 sweep, and one measurement either discharges it or makes it an L2 class repair); m88ksfd1row: KEEP

Seat: Fable 5.1 (Agent, file-reading, read-only).  Evidence basis: HEAD `7b23b785`, committed text via `git show HEAD:`; every
artifact cited below was opened.  No build, no run -- every score I quote is READ from a preserved log and every score I
predict is marked PREDICTED.  The other three answers in this directory were NOT opened.  Nothing in any project tree was
written except this file.

## 0. The packet's six facts, checked

1. READ.  `regress/m88k_exc_probe.py` at HEAD is byte-identical to `m88k_exc_probe.v21.frozen.py` and to the working tree; its
   only commit is `79cd12e8`; ROWS holds 61 entries = 59 fault rows + 2 controls, and gate 11 pins `M88KEXC_RESULT=59/59`
   (`gate_m88k_rounding.sh:354`).  Witness: `probe2_head.out` 0/9, `probe2_fix.out` 9/9, `probe_v3_head.out` 3/22,
   `probe_v3_fix_final.out` 22/22.  The fix in `cpu_m88k.c` is seven `implemented = true;` lines (`:720-750`) plus the seven-label
   tail arm (`:923-961`).
2. READ.  `CELLCENSUS.out`: v16 34/42 (SER open at six arms + the two MODE-unreachable), v17 40/42.  `killtable14/driver.log`:
   M_DIV0SER, M_FBNOSER, M_RRNOSER each 54/54 on frozen v16 and 56/57 on v17, one named row red apiece (`div0tbc`, `resid50ser`,
   `errser`); CTL_DIV0SERINV 30/57.
3. READ.  `killtable15/ANALYSIS.out` + `driver.log`: M_RRTRAPMODE 58/59 (`trapfrozenuser`), M_RRTRAPSFD1 57/59 (`trapfrozenuser`,
   `trapfrozensfd1`), both 57/57 on frozen v17; CTL_RRTRAPINV 44/59 (fifteen MODE-set trap rows); BASE 59/59 opening and closing,
   identical.  Overturned by grok AND kimi on pass 11 (ledger entry, OUTSTANDING_BUGS `:15660-15662`), not grok alone.
4. READ.  `pass12_codex/codex.txt`: CLOSE, 40+6+5+5 = 56/56, "not fresh simulator runs", roster misses named as the packet says.
5. READ.  `tools/pipeline/fable_queue.md:1306-1332`, verbatim as summarised.
6. READ.  `fable_queue.md:1491-1507`, the ledger `hold_question`, the probe comment at `m88k_exc_probe.py:416-432`.  Table 15
   confirms the zero delta against the row's OWN mutant (57/59 with it, 58/58 claimed without it -- the latter is the round's
   arithmetic, not a preserved run).

## 1. CLOSE or DO NOT CLOSE -- DO NOT CLOSE, on the denominator

**What the closing pass counted.**  Codex's 56 cells are {site} x {six PSR bits} at four sites.  I re-derived the arithmetic from
`CELLCENSUS.out` and the row table and it holds.  It is the wrong denominator, not a wrong count.

**What the floor actually enumerates here (REASONED from the committed function, `cpu_m88k.c:689-981`).**  The carrier's bound:
cells are enumerated where the guarded body's OWN tests distinguish them, and the floor is the cross-product of the edited lines'
dominating predicates with the state lvalues the fix's repair path reads that are jointly reachable.  The repair path is
everything the seven `implemented = true` lines newly admit: the SFRZ block, the PSR write, the shadow-register branch,
`pc = VBR + 8*vector`, the delay-slot write, the tail switch.  The lvalues that path TESTS -- "tests" meaning masks or compares
as a case, pinned 2026-09-25 -- are exactly four: `vector` (the labels), `PSR & SFRZ` (`:811`), `is_trap` (`:816`), and
**`cpu->delay_slot` (`:840` and `:865`)**.  The chain closed {arm} x {SFRZ} x {is_trap} at every reachable cell.  It never
enumerated {arm} x {delay_slot}: the only row that faults inside a delay slot is `dslot` (DIV0, unfrozen, non-trap -- the one
`BR_N_` use in ROWS), so by the chain's own cell criterion (settled premise 3 of the pass-12 brief: closed iff two rows reach the
site with different values) the cells (MISALIGN, UNIMPL, PRIV, OVF) x {delay_slot set} are OPEN.

**The edit, against the real control flow (sketch rule observed):** `case M88K_EXCEPTION_INTEGER_OVERFLOW: implemented =
!cpu->delay_slot;` (or the same at MISALIGNED_ACCESS, PRIVILEGE_VIOLATION, UNIMPLEMENTED_OPCODE).  Outside a delay slot
`implemented` is true and delivery is unchanged; inside one -- `cpu->delay_slot` is `TO_BE_DELAYED` when the slot instruction
runs, which the `dslot` row's DELIVER with SNIP = pc+4 and SFIP = delay_target proves reaches `:840` -- the arm falls to the
fallback at `:799` and stops every guest CPU, the pre-fix symptom, for an overflowing `add` (or a misaligned load) that a
compiler scheduled into a `.n` slot.  PREDICTED scores on the shipped 59-row instrument: the mutant 59/59 at each of the four
arms (no row at those arms is in a slot); its polarity twin `implemented = (cpu->delay_slot != 0)` reds every row that reaches
the arm -- OVF 9 rows (50/59), MISALIGN 8 (51/59), PRIV 6 (53/59), UNIMPL 5 (54/59) -- which proves the edit lands.  These are
inferences from the row table; the carrier says a sweep is a measurement, never an inference, and I have not measured.

**Why this is floor and not clause (e), and why it blocks closure rather than filing.**  (i) `delay_slot` is TESTED by the
repair path, which is a stronger claim than the chain accepted for the PSR bits it graded floor (those are only READ, see Q2).
(ii) The chain's own practice treated the equally pre-existing re-route (`if (!is_trap)`, `:816`) and its PSR read as floor
axes and repaired them in-round on passes 5, 7, 8 and 11; a bound that admits those and excludes a tested lvalue in the same
path has no principle behind it.  (iii) The stop condition closes on a VALID pass carrying its denominator; a denominator that
omits an enumerated axis is "zero looked for" on that axis -- correction 1 of the repair-chain rule, exactly.  (iv) The floor's L2
rule fires on a MEASURED false pass; a prediction with a verified premise is a candidate (the `m88kexcdetectorl2` precedent), so
the chain does not close on this adjudication and it does not repair on it either -- it MEASURES: one scratch clone, one mutant
and its twin on the frozen v21 instrument, under a PRETABLE16 written before the build.  If the mutant reds a row I have
missed, the cell is discharged and the chain closes on that receipt.  If it sweeps, it is L2 and the repair owes the CLASS
closure in one diff (four rows in `dslot`'s shape -- `br.n +16` with the faulting instruction in the slot: `ovfdslot`
[BR_N_PLUS16, ADD_R2_R3_R4], `misaligndslot` [BR_N_PLUS16, LD_R2_R3_0], `privdslot` and `unimpldslot` after an `stcr` to user mode;
the classifier's `dslot`-only special case becomes a per-row delay-target want), a gate re-pin, and ONE pass on that diff.

**Bounds and disclosures of the claim, so it cannot become `#392`.**  The floor claimed is the single-axis {arm} x {delay_slot},
the same level at which the chain closed the PSR bits; the joints {delay_slot} x {SFRZ} and {delay_slot} x {is_trap} are
multi-axis and stay clause (e), disclosed by count.  BOUNDS and ERROR x {delay_slot}: reachable in the emulator by a `tb1` in a
`.n` slot (`X(tb1)`, `cpu_m88k_instr.c:2553-2565`, carries no delay-slot guard), but whether the architecture permits a trap
instruction in a slot I could NOT settle from `mc88100.txt` (`:3720-3728` and `:9433-9440` read; neither answers it) -- disclosed,
not counted.  The same axis at the fallback and at the re-route is the same class; a frozen handler with a `.n` slot fault
(`errdslot`) is cheap and I recommend it ride with the repair, but it is not in the floor as bounded here.  One caution for the
repair itself: `dslot` pins the delay-slot else-arm AS IMPLEMENTED, which `m88kdslotshadow` records as architecturally wrong;
four more rows pinned to it must carry the same re-pin-first note, and when that round lands all five are re-pinned before the
code moves (oracle-correction order).

## 2. Is the deferred cut question moot?  No -- it is ANSWERED, and the answer touches this row's record

The question asked whether "the arm reads no PSR bit" is the right DEPENDS-ON test.  Since 2026-09-06 the carrier pinned the
answer twice: TESTS means masks or compares as a case, not depends-on (09-25), and an input is graded by what the body tests on
it, never by the flow that reaches it (10-09).  `m88k_exception()` tests ONE PSR bit, SFRZ.  So {site} x {MODE, SFD1, IND, C, SER}
is clause-(e) coverage at EVERY site -- the dispatch arms, the fallback, and BOTH sides of the re-route.  The round's cut was
right about the arms and wrong about the re-route: grok's pass-7 warrant ("the re-route predicate READS PSR, so a conjunct there
is clause (d) floor") is the reads-not-tests reading the 09-25 pin excludes, and PRETABLE12's "L2, in-round" and the pass-11
overturn (which cited PRETABLE12 as precedent, plus kimi's claim that the vector-conditioned mutants "condition on a field the
body does not test either" -- false: `vector` IS tested, by both switches, which is why the LABEL clause made those floor) rest
on it.  The asymmetry the question suspected ran the other way.

What rests on it: nothing in row DEMAND (all 56 cells are closed and none is lost), so the coordinator is right that no row
depends on the cut; but the record's GRADES do -- v16/v17/v19 are recorded as L2 repairs, and pass 11 used this round's own grade
as its precedent, which is how an over-grade propagates to the next round that de-fatalises something that reads a status
register.  Disposition: not an L4 (no coverage claim is refuted), one sentence in the `m88kexcdeliver` closure note: "the PSR-bit
cells at all four sites are clause-(e) coverage closed voluntarily; graded L2 at the time under a reads-PSR criterion the
carrier's 09-25 pin does not support."  The queue's second half -- which pass-7 disposition was wrong -- is overtaken: the
narrowed disclosure was measured wrong three ways by opus5 on pass 8 (named OVF, which `ovfc`/`indclr` already closed; claimed
{arm} x {SFD1} closed everywhere; omitted BOUNDS and ERROR), and v16 corrected it; the docstring says so.

## 3. `m88ksfd1row` -- KEEP, and no wording change

1. The addition licence governs PRODUCT code; it is the wrong instrument for a detector row.  Row demand ("per enumerated
   mutant, never per attribution need") bounds what is OWED, not what is PERMITTED.  Neither says delete.
2. The row is not vacuous: its named channel varies under its named mutant (M_RRTRAPSFD1 reds it, 57/59, READ).  Redundancy with
   `trapfrozenuser` is not vacuity -- the CHANNEL check asks whether the row can red under its mutant, not whether it reds alone.
3. "Zero delta" is a property of WHICH mutant it is scored against, not of the row.  The trap side's {MODE} x {SFD1} joint has
   four cells: (1,1) thirteen rows, (0,0) `trapfrozenuser`, (1,0) `trapfrozensfd1` ONLY, (0,1) nobody.  The joint mutant
   `if (!is_trap || ((PSR & M88K_PSR_MODE) && !(PSR & M88K_PSR_SFD1)))` reds `trapfrozensfd1` and no other row (REASONED:
   `trapfrozenuser` has MODE clear, the other thirteen have SFD1 set).  That is a coverage benefit -- three of four disclosed
   joint cells held instead of two -- not an attribution benefit, and codex's "loses none of the 56 cells" is true only of the
   single-axis count.  PREDICTED, not measured; it is clause (e) and not owed, which is exactly why "not owed" and "remove" are
   different verdicts.
4. Cost: one session; table 15 shows the two v19 rows perturbed no other row's result (BASE identical, every other mutant's red
   set unchanged from table 14's shape).
5. The shared-constant hazard is real for the trap-side SFD1 cell only (`errdiv0` carries SFD1-clear at the non-trap side via
   `PSR_FRZSUP`, untouched by a `PSR_FRZUSER` edit).  `trapfrozensfd1` uses `PSR_FRZSUP`, so keeping it is what gives that cell two
   carriers on two constants.  The structural defence is not the comment at `:431-432` (a comment is memory): two import-time
   asserts in the probe, `assert not (PSR_FRZUSER & (M88K MODE | SFD1))` and `assert PSR_FRZSUP & MODE and not PSR_FRZSUP & SFD1`,
   named for the cells they carry, so an edit that re-sets a bit fails the probe at startup.  Hygiene, not owed; it rides with the
   delay-slot repair if one lands, else files LOW.
6. Wording: the licence stays as written.  The row-demand rule stays as written.  The ruling lands in the ledger row and in the
   probe comment at `:416-432`, whose "KEPT PENDING THE 2026-09-09 ADJUDICATION" is now a stale clause (records tidy, same diff).
   One instance does not earn carrier prose.  Close `m88ksfd1row` as "kept, not owed".

## 4. Which of the coordinator's dispositions is wrong -- two of three

* **CLOSE -- wrong.**  A four-seat roster cures the pass-12 roster gap; it cannot cure a denominator that omits an enumerated
  floor axis.  Hold the row in work for one measurement (above).
* **MOOT -- wrong.**  The rule question is answered by the carrier's own later pins, the answer re-grades three of this round's
  repairs from L2 to voluntary clause-(e) closure, and leaving it "for a future round" leaves the over-grade standing as the
  precedent that future round will cite.
* **KEEP, no licence change -- right**, with the reason strengthened: the row's delta is nonzero against a nameable disclosed
  joint mutant, so the "cannot hurt" framing does not apply at all; add the two asserts.

## 5. Not established here

No simulator run: the delay-slot sweep and the joint-mutant kill are predictions from the row table and the committed source.
The legality of a trap instruction in a `.n` delay slot on the MC88100 is unsettled from the manual on disk.  The 58/58 figure for
the row's removal is the round's arithmetic, not a preserved log.
