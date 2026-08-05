# GXemul est/ — Outstanding bug candidates (not yet fixed)

> ## 2026-08-01 — OPEN LIST, at a glance
> **Only genuinely OPEN items live here.** Resolved ones are removed, not annotated: an
> index that accumulates its own history stops being an index, and a section headed
> "everything genuinely open" that is mostly ticks is the dishonest-listing class #270
> exists to prevent. The dated blocks below and the CHANGELOG carry what was fixed and
> why. Rounds 60–65 (#295–#300) cleared the entire floating-point feasibility queue;
> what follows is what they left, plus what they found on the way.
>
> **Ready to work — reproduced, and an instrument already exists**
> - ✅ **MIPS `cvt.d.l` (and `cvt.s.l`) ignore the rounding mode → RESOLVED as #301**
>   (round 66). L→D is exact integer rounding in the requested mode (the discarded low
>   bits ARE the remainder — no fma); L→S goes via round-to-odd so the single store
>   rounds correctly in every mode. The L→S half was deferred in the first draft and the
>   panel refused, each seat with its own witness class (tie-down-twice, and
>   one-below-a-midpoint rounded onto it). Covered by the new gate 12 on the arc rig —
>   including an FR=0 row, because every other row ran with Status.FR set and the
>   pair-assembly path deserved a measurement, not a reading — plus 34 offline vectors
>   with both helpers' negative controls failing exactly their five predicted rows.
>   pmax raises Reserved Instruction on the `ldc1` (cvt.d.l is MIPS-III+), so the blast
>   radius is R4000+ and the R3000 rig is untouched by construction.
>   Indexed, not modelled: some real silicon (the VR4300 famously) raises Unimplemented
>   Operation for L operands beyond 2^53 and lets the kernel softfloat complete —
>   architecturally the same FCSR-rounded value; GXemul's no-trap depth here matches its
>   pre-existing modelling (#246 covers denormals only).
> - ✅ **m88k float→int conversions → RESOLVED as #302** (round 67), and the scope GREW
>   in review: `trnc.ss`/`trnc.sd` were raw C casts (host-UB on specials — x86 answered
>   0x80000000 for everything), and `int`/`nint` — the other two thirds of the MC88100
>   triad — were **absent from the decoder entirely**, so a legal guest instruction
>   halted the emulator ("All machines stopped", reproduced for both). The contract is
>   OpenBSD's kernel completion (the MC88100 traps on every special and writes nothing;
>   the manual's trap window even catches in-range [2^30, 2^31), which the handler
>   completes): SoftFloat saturation with **all NaN forced positive** — a third table,
>   distinct from SH's (#297) and MIPS's (#273). One shared mode-parametric ladder
>   serves the triad: trnc→toward-zero, int→fcr63 via the #298 decode, nint→nearest.
>   Thirteen new gate-11 rows (38 total); the trnc mutant failed exactly its four
>   discriminators.
> - ~~**`ieee_interpret_float_value` mis-decodes subnormals with an implicit 1**~~ —
>   **RESOLVED as #303 (round 68)**: biased exponent 0 now decodes without the implicit
>   1 at exponent 1−bias; exhaustive both-signs S + 400k D offline rows, all bit-exact.
>   The "invisible through stores that flush" theory was HALF-wrong: the pass-1 claim
>   that MIPS was fully masked by #246 was refuted by two panel seats and the rig —
>   `fpu_unimpl_trap()` returns 0 on EXC3K (R3010 interrupt pin unwired), so
>   **pmax/R3000 consumed the garble** (measured `0x32000001` for S-min×2^100, now
>   `0x27000000`), as did m88k, SH, Alpha and PPC (`lfs` alone: `0x3800000020000000` →
>   `0x36a0000000000000`). arc/R4000 keeps the trap — the no-change control. Sixteen
>   new gate rows across gates 2/10/11/12 + mutant `revert303`; two pinned KNOWN-CHANGE
>   flip rows (garbled S-normal products → true subnormal results → deliberate
>   #287/#292 store flush → +0) are the before/after evidence the store-side round
>   below inherits.
> - ~~**Store-side subnormal ENCODE**~~ — **RESOLVED as #331–#334 (round 72)**, and the
>   entry as filed named the wrong line for half of it. Measured on the committed build
>   first, against oracles that are not the code under test — for D the identity (every
>   finite double is exactly representable, so nothing is rounded and the owed answer is
>   the input's own bit pattern), for S the host's correctly-rounded cast under the
>   matching mode: **D 220/220 wrong** (no gradual underflow in double precision *at
>   all* — the arm was an empty `// TODO`) and **S 65737/65740 wrong, of which 65736 came
>   through the `FP_NORMAL` arm and one through the `FP_SUBNORMAL` arm this entry
>   blamed.** A single-subnormal value like `1e-40` is a NORMAL host double; it was lost
>   to the exponent clamp and the flush, not to the TODO.
>   **Both of #292's stated rationales were false.** "MIPS routes non-flush denormal
>   results away (#246)" holds only for EXC4K+ with FS clear — `fpu_unimpl_trap()` returns
>   0 on EXC3K so R3000 fell through, and the FS=1 arm *deliberately skips* the routing,
>   so **R4000 was getting its flush from the bug**. "SH DN=1 silicon" was true of the
>   silicon and not of this tree: `SH_FPSCR_DN_ZERO` was read by nothing, and FPSCR resets
>   with DN set, so the encoder fix alone would have changed the DEFAULT SH configuration.
>   Both now state their policy at their own store sites (#332, #334), as does Alpha
>   (#333). pmax is deliberately **left flushing**: a panel seat established from the IDT
>   manual that the R3010 leaves the destination unchanged on UnImp and that software
>   completion is a later action, so recording `0x80000002` as the hardware answer would
>   have been a false row — and GXemul wires no R3010 interrupt pin, so declining to write
>   would leave a stale register instead. Nine new named vectors, two new mutants.
>
> - ~~**PowerPC `fmadd`/`fmsub` modelled unfused**~~ — **RESOLVED as #335 (round 92)**.
>   Book I rounds the product-sum once; `fra.f * frc.f + frb.f` rounds twice unless the
>   compiler contracts it, so correctness was a property of the BUILD HOST. Measured
>   `0000000000000000` where the ISA owes `b970000000000000`, with a `2.0*3.0+1.0 → 7.0`
>   control passing on both sides to rule out a wrong register field. Now `fma()`.
>
> - ~~**`fmadd`/`fmsub` raise none of their exception causes**~~ — **RESOLVED as #343
>   (round 95)**. Measured at `00001000` (FPCC alone, no cause bits) on every row before
>   the fix. `ppc_invalid_cause_fma()` treats the three conditions as independent, which
>   `ppc_invalid_cause()` cannot: it returns a single cause and abandons its op test at the
>   first NaN. The `Inf × 0` with sNaN addend case now correctly owes **both** `VXIMZ` and
>   `VXNAN` (`a1101000`), and the four VXISI rows are a 2×2 on identical operands pinning
>   `fmsub`'s addend-sign inversion. Eight new gate-13 rows.
> - **`fnmadd`/`fnmsub` are not decoded and halt** (`ppc_halt_probe.py:260` has them
>   pending). When implemented they must negate the **already-rounded** result —
>   `-fma(a,c,b)` and `-fma(a,c,-b)` — because the ISA rounds before the final negation,
>   so moving those signs inside the FMA is NOT equivalent under directed rounding. The
>   single-precision `fmadds`/`fmsubs` family must stay fused as well and cannot alias
>   the double handlers, whose final rounding is to D.
> - ~~**PowerPC `FPSCR[RN]` is not wired to arithmetic**~~ — **RESOLVED as #336 (round 91)
>   for `fadd`/`fsub`/`fmul`/`fdiv`**, which now use #300's `_rm` helpers. Measured
>   `1.0 + 3*2^-54` under RZ answering `3ff0000000000001` (the nearest result) where
>   toward-zero owes `3ff0000000000000`, with an RN control row pinned unmoved.
>   **`fmadd`/`fmsub` remain unwired**: #335 made them correctly fused, but `fma()` rounds
>   per the HOST mode, so a directed-mode fused rounding needs an exact product-sum rather
>   than a two-operand helper. That is the residue of this item.
>
> - **(historical) PowerPC `FPSCR[RN]` was not wired to arithmetic at all.** `fadd`, `fsub`, `fmul`,
>   `fdiv`, `fmadd` and `fmsub` all compute in host double under the HOST rounding mode
>   and store through the legacy entry point (`cpu_ppc_instr.c:1746/1800/1849/1907/1961/
>   2024`); only the conversions `frsp` (`:1546`) and `fctiw` (`:1687`) read the mode.
>   #300's `ieee_add_round_rm`/`ieee_mul_round_rm`/`ieee_div_round_rm` already exist and
>   are wired on MIPS, SH and m88k. The fused `fmadd` case is harder than the other four:
>   `fma()` rounds once but per the host mode, so a directed-mode fused rounding needs an
>   exact product-sum rather than a helper call. Gate 13 exists with 121 rows to build on.
>
> - **The ARM instruction COMBINER changes observable flags — and NO probe in this
>   harness can currently see it.** Source-verified: a data-processing immediate with the
>   S bit set updates C from the shifter carry-out, which this tree approximates as "if
>   the encoded immediate is > 255 it was rotated, so C := its bit 31"
>   (`cpu_arm_instr_dpi.c:121-140`). The standalone `teqs`/`tsts` do that. The
>   `*_samepage` handlers a `teq`/`tst`-followed-by-branch is folded into do **not touch
>   C at all** (`cpu_arm_instr.c:2589`, `:2610`, `:2628`, `:2651`), and the `teqs`
>   combiner has **no guard on the operand whatsoever** (`:2973`, `:2989`) while the
>   `tsts` one guards only bit 31 — which is about N (with the top bit clear `a & b`
>   cannot be negative), not about C. So folding changes the flags a guest observes.
>   **Why it is not fixed here:** `cpu_dyntrans.c:1888` disables combining whenever
>   `single_step` is set, and every probe in `regress/` drives the guest with the
>   debugger's `step`. Rows written against a `teq`+`beq` pair therefore measure the
>   STANDALONE path while appearing to measure the combined one — five such rows were
>   written, measured "correct", and withdrawn rather than committed, because a row that
>   cannot fail is worse than no row. A real witness needs FREE-RUNNING execution with
>   `allow_instruction_combinations` on and a breakpoint after the sequence — the same
>   "gates are only provable free-running" constraint this project has hit before. The
>   whole combined-handler family (`cmps_*`, `teqs_*`, `tsts_*`, `netbsd_*`, `strlen`,
>   `xchg`) is unguarded by the harness for the same reason, which is a wider hole than
>   this one defect.
>
> - **Still open, from round 72's own findings** (recorded, not guessed at):
>   - **PPC-D, Alpha, and SH PR=1 D arithmetic have no gate rows at all**, so #331 changed
>     them without a witness. Alpha has no rig, which is why #333 is deliberately
>     bit-identical to previous behaviour rather than a refinement; whether the
>     architecture wants `+0` for a negative tiny cannot be measured here.
>   - **The #246 trap predicate is pre-rounding.** `fabs(nf) < FLT_MIN` at
>     `cpu_mips_coproc.c` traps values in `(2^-126 - 2^-150, 2^-126)` that round *up* to
>     `FLT_MIN` and are therefore normal results; MIPS specifies tininess after rounding.
>     #332's substitution classifies on the encoded word and is correct; the trap check
>     above it was left alone because moving it changes WHEN the trap fires for a band the
>     committed arc trap rows sit near, and that measurement was not made this round.
>   - **PowerPC `NI`** is defined and never consumed — another architecture-level FTZ
>     policy that must not contaminate the generic encoder.
>
> - ~~**PowerPC, four measured defects**~~ — **RESOLVED as #304/#305 (round 69)**, with
>   **gate 13** built first on the probe path: 50 rows, every committed byte recorded
>   before a line of the fix existed. `frsp` now narrows by exact bit surgery under
>   `FPSCR[1:0]` (three of four modes had been unreachable behind a host cast) and keeps
>   a NaN instead of delivering +0.0; `stfs`/`stfsx` implement Book I's denormalization
>   band; and #305 stopped all four conversion instructions destroying a NaN's sign and
>   payload (`lfs(0xffc00001)` used to arrive as `0x7fffffffffffffff`). All 25
>   discriminators flipped to pre-registered bytes on the first run; all 25 pins held.
>   The fourth "defect" was REFUTED by measurement — finite values ≥2^128 already give
>   ±Inf (#287) — and closes as a pin.
>   **Still true, still enforced:** do NOT wire `stfs` to FPSCR.RN; it does not round.
>
> **PowerPC, filed by round 69's panel and each owed its own round**
> - **The single-precision arithmetic family does not narrow**: `fmuls` is an alias of
>   `fmul` (and the rest follow), so `float` arithmetic keeps double precision. #304's
>   helper now exists, so this is wiring — but it needs the store-side subnormal contract
>   settled first, or it bakes in a policy that round may change.
> - ~~**The update-form conversions are not decoded at all**~~ — **RESOLVED as #310
>   (round 70B)**, and the family was twice the size this entry named: the four primary
>   opcodes (`lfsu`/`lfdu`/`stfsu`/`stfdu`, whose defines were missing outright) *and*
>   the four indexed forms (extended opcodes 567/631/695/759). All eight were measured
>   halting the emulator; eighteen gate-13 rows now assert both the value transferred and
>   the base-register update, with non-update controls proving the base stays put.
>   A prevalence claim made for this fix was **withdrawn**: restricted to the executable
>   section, the NetBSD/macppc kernel contains none of these forms — the hundreds first
>   reported were data in the read-write-execute segment.
> - **The exception-enable bits (OE/UE/VE) and the FPRF class bits are unmodelled.** Not
>   forced piecemeal, for the reason the SH exception model is not: a lone enabled bit
>   implies the others work. Round 73's after-pass added two specifics and a warning:
>   `fctiwz` owes **VXCVI** (and **VXSNAN** for a signalling operand). ~~and `mtfsf`
>   must not copy FEX and VX~~ — **RESOLVED as #327 (round 88)**, together with the
>   recompute it had to land beside: VX and FEX are now DERIVED from the causes and
>   enables rather than stored, in both directions, so the phantom "VX set with no
>   cause" state #326 made reachable is gone. `frsp`'s unconditional FX set and an
>   order-dependence in FEX went with it. The warning, and it is load-bearing: `fctiwz`'s existing
>   `>= 2147483647.0` / `<= -2147483648.0` branches give the right *result* but are not a
>   correct *classification* of "out of range" — the model range-checks after rounding,
>   so under round-toward-zero an operand stays convertible while `x < 2147483648.0`.
>   Reusing those branches to raise VXCVI would flag endpoints that are not invalid.
> - ~~**Seven FP control/convert encodings are absent from the tree entirely**~~ —
>   **largely RESOLVED as #326 (round 87)**, and the entry understated it badly: a 28-row
>   sweep measured **twenty-four** legal encodings halting the emulator, not seven. The
>   biggest was not an instruction at all but `if (rc) goto bad;` at both floating-point
>   entries, so **every record form** halted — `fadd.`, `frsp.`, `fmr.` — including those
>   of instructions that worked with Rc=0. Twelve are decoded now (the Rc forms, `mcrfs`,
>   `mtfsb0`, `mtfsb1`, `mtfsfi`, `fctiw`, `fnabs`, `fsel`); gate 15 holds the line.
> - **Twelve encodings still halt, deliberately, and gate 15 asserts that they do.** Split
>   by reason, because the reasons are not the same:
>   - `fctid`, `fctidz`, `fcfid`, `fsqrt`, `fsqrts` — **64-bit-only, or outside the G4's
>     instruction groups.** On a 32-bit G4 real silicon raises a program interrupt, so
>     implementing them unconditionally would make the model *less* faithful. These ride
>     on the missing exception model, not on decode work.
>   - `fres`, `frsqrte` — estimate instructions, accuracy implementation-defined.
>   - `fcmpo`, `fnmadd`, `fnmsub`, `fmadds`, `fmsubs` — **no technical blocker.** A few
>     dozen lines each at the fidelity bar already shipped (`fadds` and `fmuls` are
>     aliases of their double forms today). Out of #326 for round size alone. Do
>     `fmadds` first: gcc emits it for ordinary `float` arithmetic, so it is likely the
>     most frequently executed instruction still in this set.
> - **The splice letter is deliberately not followed** for finite values around 2^129:
>   Book I's `SINGLE()` would WRAP the exponent (2^129 → a 2.0f-class pattern, 1.5·2^128
>   → the NaN pattern `0x7FC00000`), and this fork keeps #287's ±Inf instead. Panel
>   3–1 with the dissent recorded; reopen only on silicon evidence or a guest victim.
>
> **Instruction-coverage gaps (the decoder rejects legal encodings)**
> - ~~**m88k `fdiv.dds`** and **mixed-format S-destination arithmetic**~~ — **RESOLVED as
>   #306 (round 70A)**, and the census found the entry understated it: the size field is a
>   format *triple*, so each of `fadd`/`fsub`/`fmul`/`fdiv` has eight legal forms and
>   **twelve** were missing, not two. Six were measured halting the emulator on the
>   luna88k rig. Eighteen gate-11 rows cover them — including the `fmul.ssd` mode rows
>   that caught a double rounding in the fix itself, registered by a panel seat before the
>   code was tested.
> - ~~**m88k `tcnd` absent from the decoder**~~ — **RESOLVED as #307**: modelled from the
>   manual's four-class condition mask (the zero test is the NOR of the low *31* bits, so
>   `0x80000000` is its own class), with `tb0`/`tb1`'s privilege-then-condition order,
>   plus disassembly. Upstream's own narrow patch was refused: it leaves `tcnd eq0,r0`
>   halting, and `0 == 0` is the case that must trap.
> - ~~**`fdiv_sss` double-rounds**~~ — **WITHDRAWN as a phantom** in the same review that
>   filed it. Inexact is not the same as double-rounds-wrong: with two single sources the
>   quotient's error can never reach a single-precision midpoint (the exclusion-zone
>   argument), and 400,000 random single÷single quotients found no disagreement with a
>   single correct rounding. The arms that genuinely had the hazard were the six #306
>   introduced, and they were fixed in the same round by **#308**'s round-to-odd helpers —
>   which also revealed that #300's `_rm` helpers return the host result unchanged under
>   nearest, correct for a double destination and a double rounding for a narrower one.
>   **The "still open elsewhere" clause that used to close this entry is WITHDRAWN too**,
>   as the same phantom wearing a different architecture's name. It read: the narrowing
>   question "applies to MIPS `div.s`, SH `fdiv`, and both architectures' single-precision
>   `sqrt`" — but that is the *same arithmetic* the paragraph above refutes, single sources
>   into a single destination, and the sentence sat ten lines under its own refutation for
>   five rounds. Neither instruction has a mixed-format form: `cpu_mips_coproc.c:1301`
>   and `cpu_sh_instr.c:3425` divide S by S, `:1313` and `:3212` take the root of an S.
>   The bound is explicit — for singles `a`, `b` and any single-format value or midpoint
>   `s`, `q* - s = (a - s*b)/b` where `a - s*b` is an integer multiple of
>   `2^min(ea, es+eb)` with a significand product under 2^48, so a nonzero difference is at
>   least `2^-48*|q*|` (`2^-49` against midpoints), while harmful double rounding needs the
>   exact value inside the intermediate double's half-ulp at `~2^-53*|q*|`. That is a
>   32-fold gap, 16-fold against midpoints; the same argument through `s^2` gives
>   `>= 2^-49*sqrt(a)`. Measured as well as argued, against exact-rational oracles using no
>   host FP, in all four modes: 157,920 random quotients and 120,006 random radicands, plus
>   219,888 **constructed** division cases and 95,628 constructed root cases built to land
>   *on* grid points and midpoints — 0 mismatches, closest approach `2^-41.29`, twelve
>   binades short of where a double rounding could bite. Two review seats reached this
>   independently, one analytically and one by sweep. The hazardous class is
>   wide-source/narrow-destination, which is exactly where #308's helpers were applied
>   (`cpu_m88k_instr.c:1668`); MIPS and SH have no such instruction to apply them to.
>   **The deliverable for this item was the search, and this paragraph is it** — recorded
>   at length so the next triage does not re-file it a third time.
> - ~~**m88k `bcnd`'s condition table is NULL for legal unnamed masks**~~ — **RESOLVED as
>   #323 (round 76)**. Reproduced first: all nine named masks ran, and all eight unnamed
>   ones tested (0, 4, 6, 9, 0xa, 0xb, 0xf, 0x11) halted the emulator. Fixed the way #307
>   fixed `tcnd` — the manual's four-class mask written once, replacing the enumeration of
>   nine named comparisons rather than sitting beside it, so `print_operator()` is gone.
>   Seven gate-11 rows assert the branch DECISION, including the pair `m5=4` vs `m5=0xc`
>   that differs only on the most negative value and would catch an implementation that
>   collapsed those two classes.
> - **MIPS paired-single arithmetic is unmodelled.** Deferred on purpose: the FIR
>   advertisement sits inside `#if 0`, so the emulator makes no false claim a test could
>   reproduce. This is feature work, not defect work. Reopen when a rig boots a
>   PS-capable CPU or a guest binary executes PS.
> - **SH `ftrc` with an odd m under PR=1** decodes as an odd `fr[]` pair (reserved
>   encoding, pre-existing dispatch behaviour).
> - ~~**ARM's subtract carry, ADCS's overflow flag, and the undefined space**~~ —
>   **RESOLVED as #311/#313/#312 (round 71)**, the first ARM work in this fork, opened
>   with a new instrument (gate 14, 58 rows on a `testarm` cold debugger; the pre-fix
>   build scored 39 of the 56 rows then present, failing exactly the 17 predicted rows
>   and nothing else). #311: the carry-out was `a >= b` for the whole
>   subtract family, which is right for SUB/CMP/RSB but ignores the borrow SBC/RSC just
>   subtracted — wrong exactly when `a == b` with carry-in clear, i.e. the ordinary way
>   multi-word arithmetic makes a zero limb. #313, found by a panel seat reading the `#if`
>   nesting: ADC was named in the outer guard that CLEARS V but matched neither inner
>   formula, so `ADCS` could only ever clear the overflow flag. #312: unmatched encodings
>   in the `main_opcode >= 6, bit 4` space halted the emulator, and the halt fired at
>   DECODE — so a *conditional* undefined word whose condition was false stopped the
>   machine too. The tree's own correct routing sat a few lines below, unreachable behind
>   an identical predicate; three seats verified the identity and it was deleted.
> - **The `A__PC` operand at the very top of the address space** (`cpu_arm_instr_dpi.c`,
>   raised by three seats reviewing #311, one of them calling it a regression the round would
>   introduce rather than a pre-existing corner). With Rn = PC the operand is recomputed as
>   page base + slot + 8 in 64-bit arithmetic, which passes 2^32 for the last two instruction
>   slots of the 4GB space, and #311's `c32 == c64` would then differ from the old truncating
>   test. **FIXED as part of #311** by truncating that operand to 32 bits — correct
>   independently of the carry change, since ARM's PC is 32 bits and reading it must wrap, and
>   it also removes a spurious carry the ADD family has reported at those two addresses since
>   long before this round. **Still open is the measurement:** the fix is a provable no-op for
>   every operand below 2^32, which is everything these rigs can reach, so its effect at the
>   top of the address space is reasoned rather than measured. Reaching it needs RAM mapped at
>   `0xfffff000` — a `dev_ram` config statement is the only route found so far.
> - ~~**Three more guest-reachable halts in the ARM decoder**~~ — **RESOLVED as #319/#320
>   (round 78)**, and the round found a fourth defect that never halted: the immediate
>   guard exempted an imm8 of zero, so `movs r0,#0 ROR 4` shipped with the wrong carry
>   instead of stopping loudly. Also **#321**: `mvns` with an immediate took its shifter
>   carry from the COMPLEMENTED operand (the decoder rewrites `mvn #imm` to `mov #~imm`),
>   which is wrong in every band — measured setting the carry where the architecture
>   leaves it alone, setting it where the architecture clears it, and clearing it where
>   the architecture sets it.
> - **The combined TST/TEQ handlers never update the carry** — established by reading,
>   **NOT reproduced**, and deliberately not fixed. `tsts_lo_beq_samepage`,
>   `teqs_beq_samepage` and their `bne` twins all do
>   `flags &= ~(ARM_F_Z | ARM_F_N)` and never write C, while the uncombined path does
>   write C whenever the immediate was rotated. The combiner installs them from
>   `COMBINE(beq_etc)` on `ic[-1].f == instr(tsts)` with only a bit-31 guard on the
>   immediate — which prevents the case where C would need to be SET and not the case
>   where it must be CLEARED.
>
>   **What defeated the reproduction, recorded so the next attempt starts further on:**
>   instruction combination is gated on `!single_step && !single_step_breakpoint`, so a
>   `step`-driven probe can never reach it — and on `testarm` a free-running `continue`
>   never returns to the prompt (the machine's halt stub leaves the guest spinning), so
>   there is no way back to read the result. Driving it with a breakpoint DOES return,
>   but a differential run with and without `-J` (which forces combining off) produced
>   **identical** flags, so either the breakpoint suppressed the combination or it fired
>   without changing the answer. The two cannot be told apart without a positive control
>   that the combination actually occurred — the instruction counter is the obvious one,
>   since a combined handler counts one instruction where two executed.
>
>   Until that control exists this stays open and unfixed: the reading is suggestive,
>   but a fix with no reproduction is exactly what this project does not ship.
> - **`sxtab` and `sxtah` are not decoded at all** — the encodings `0x06a00070` and
>   `0x06b00070` appear nowhere in `cpu_arm_instr.c` (confirmed by a round-78 diff seat and
>   verified). #319 gave the UNSIGNED extend-and-add pair its rotation; the signed pair has
>   no handler in any form and has raised Undefined since #312. A missing instruction, not
>   a halt — the "half a family" shape again, and it belongs with the rest of the
>   unimplemented ARMv6 media set.
> - ~~**#320's PC carve-out survives for `rn == PC`**~~ — **RESOLVED as #322**, after four
>   of the five diff-review seats independently named it and one supplied the witness
>   (`tst pc, #4 ROR 2`, measured leaving the carry set where the architecture clears it).
>   The stated reason for leaving it — that a cold handler could not reach the PC+8
>   reconstruction — was false; it needs only `ic`, `cur_ic_page` and `cpu->pc`.
>   `rd == PC` remains excluded and correctly so: writing the PC with S set is an
>   exception return whose flags come from SPSR, so the carry there is overwritten
>   rather than lost.
> - ~~**ARM Thumb `add`/`sub` take Z from the untruncated 64-bit result**~~ — **RESOLVED as
>   #328 (round 77)**, and the entry was wrong in three ways worth recording. There were
>   **four** near-identical blocks, not three. Carry was **not** "correctly read from bit
>   32": subtracting zero produced no carry-out at all, so `cmp r0,#0` reported a borrow
>   that never happened. And a **third** flag was wrong that the entry never mentioned —
>   V came from the sign of the *negated* subtrahend, which fails at `0x80000000`, the one
>   value that is its own negation; it was inverted in both directions, and `x - x` at that
>   value claimed overflow. Only N was right, because it truncated first.
>
>   Reproduced first, as owed: Thumb is reached by an ARM `bx` to an odd address, and all
>   thirteen defect rows were measured failing on the committed build before any edit.
>   V is reachable only in the two REGISTER forms — imm3 and imm8 cannot encode
>   `0x80000000` — so that one defect was in two copies while Z and C were in four.
> - **The ARMv6 media encodings decode on every ARM model**, including the ARMv4 SA1110
>   this rig runs, where silicon would raise Undefined. Pre-existing fidelity gap rather
>   than a halt; deliberately not entangled with #312.
>
> **Round 71B — the non-ARM upstream candidates, triaged. Two refuted, one promoted.**
> - ~~**MIPS "early-store hazard"** (`cpu_mips.c`, the `store_32bit_word` to
>   `0xffffffff9fc00000` in `mips_cpu_new`)~~ — **REFUTED by measurement, no change.** The
>   worry was that a store issued at CPU-creation time lands before the machine has
>   installed RAM. Read back on the pmax rig, that address holds `0x00c0de0c` repeated
>   every 8 bytes — the DEC PROM emulation's own vectors — not the `0x00c0de0d` the CPU-init
>   store writes. So the store is not lost into a void; it is *overridden by
>   machine-specific initialisation*, which is precisely what the comment above it says
>   should happen. The mechanism is working as designed. Left open, and much weaker than the
>   original claim: whether the default ever survives on a machine that does NOT override it
>   (`testmips` did not construct in the configuration tried), which would make it a dead
>   default rather than a hazard.
> - ~~**m88k `PFAR`**~~ — **REFUTED as a defect: the register is not modelled at all.**
>   `PFAR` appears nowhere in `src/`. That is a missing feature, not a wrong behaviour, and
>   there is no reproducer to write for it.
> - ~~**SH `synco` (0x00ab) is undecoded and HALTS the emulator**~~ — **RESOLVED, much
>   wider than filed, as #314 (round 79).** The premise recorded here was wrong twice over:
>   `synco` is an SH-4A instruction and this tree models no SH-4A core (landisk is an
>   SH7751R), so a nop would have made an SH-4 execute an SH-4A instruction; and the claim
>   that `PREF` was "already a nop" was false — `pref_rn` is a store-queue writeback engine.
>   A sweep then found **eight** legal encodings halting, three of them BASE ISA (`MAC.L`,
>   `MAC.W`, `TST.B`, present since SH-1/SH-2 and legal on the modelled part). Fixed the way
>   #309 and #312 fixed their architectures: the ten unimplemented-opcode `goto bad` sites
>   now decode to `instr(reserved)` and raise the illegal-instruction exception at EXECUTE
>   time. Eight of eight halted before, none after.
> - **Legal SH encodings that no longer halt but are still UNIMPLEMENTED** (they now raise
>   the exception, which is honest, but the instructions are absent): `ICBI`, `MOVLI.L`,
>   `MOVCO.L`, the `SGR` and `DBR` load/store forms, and `FPCHG`. `MOVLI.L`/`MOVCO.L` are
>   the guest's atomics and must be implemented rather than nopped if anything ever needs
>   them.
> - ~~**Four legal SH-4 sequences reach `ABORT_EXECUTION`**~~ — **three RESOLVED as #315/#316
>   (round 80)**, and they were worse than filed: two of them did not stop the emulator at
>   all, they called `exit()` and killed the gxemul process. `fmov drM,@rN` with SZ=1 exited
>   the host for HALF of all rN, because the odd-register check read its parity from the
>   address register instead of the floating-point one. `fneg`/`fabs` with an odd field under
>   PR=1 exited too. Also fixed in passing: the register-pair alignment class (8 bytes, asked
>   for 4), a second word that was never byte-swapped, and — a prerequisite the panel found —
>   `sh_exception` had no case for EITHER delay-slot event, so `trapa` in a delay slot and an
>   FP instruction in a delay slot with FD=1 both killed the process. Lazy-FPU kernels run
>   user code with FD=1, so that one is plausibly reachable by a real guest.
> - ~~**The store-queue prefetch with the MMU on STILL HALTS**~~ — **RESOLVED as #318
>   (round 81)** via a dedicated entry point, `sh_translate_sq_v2p`, since the general one
>   deliberately maps the range identically and must keep doing so for ordinary queue-filling
>   stores. The load/store question two rounds could not settle was decided on the manual's
>   own evidence rather than by count: an SQ page's UTLB entry keeps the `D` bit meaningful
>   while `C` and `WT` are explicitly meaningless, and `D` is consulted only on a write. The
>   dissenting reading came from the manual's *plain* `PREF` description — the sentence quoted
>   in the comment above that very handler — which is true of every other address range.
>   Measured with a composition witness, not just survival: operand `0xE00000E7` lands at
>   page + `0xE0`, proving `[9:5]` carried and `[4:0]` zeroed.
> - **The `SQMD` user-access check is still wrong in three ways** (round 81 deferred it,
>   deliberately): it raises reserved-instruction where hardware raises a data address error,
>   it is gated on `AT=1` though the rule is not, and ordinary queue-filling stores skip UTLB
>   validation altogether. Two seats wanted it folded into #318 and two did not — and they
>   disagreed on the correct event code, which is the argument for a round that can measure
>   it. Needs a user-mode witness, which does not exist yet.
> - ~~**SH `MOVCA.L` is decoded as a nop but architecturally STORES R0 to `@Rn`**~~ —
>   **RESOLVED as #317**: it decodes to the existing longword store, which has the same
>   alignment class and exception behaviour.
> - **Adjacent store-queue model gaps** (same function, same audit, not fixed): the SQMD
>   user-access check raises reserved-instruction where hardware raises an address error
>   (`EXPEVT_ADDR_ERR_ST`, which `sh_exception` already implements) and is only consulted
>   when AT=1, though the manual's SQMD rule is not AT-conditioned — so with AT=0, SQMD=1
>   and a user-mode guest, the flush proceeds where hardware would fault; queue-filling
>   stores under AT=1 take the identity map and skip UTLB judgment entirely, where real
>   hardware exception-judges SQ-area writes too; and UTLB multiple-hit detection is
>   unimplemented.
>
>   **Correction, 2026-08-01 (retrospective review of round 81).** This entry used to add
>   that "the identity mapping ignores address bits [25:6], so a guest filling a queue
>   through a non-zero offset stores where the flush will not read it." That is **not
>   true**, and it was a bug report against correct behaviour. `memory_sh.c:301` passes the
>   **full** vaddr through, and the SQ device wraps with `% sizeof(d->sq)` (`dev_sh4.c:952`),
>   so bits [5:0] — the queue select and the offset within it — survive intact. An aliased
>   fill lands exactly where the flush reads, which is hardware's own don't-care treatment
>   of [25:6]. Removed rather than annotated in place, per this file's rule, but the
>   correction is recorded because a false entry in a bug list costs a future round the time
>   to re-derive it.
>
> **Known and deliberately not forced — each with the reason it stays**
> - **The SH FPU exception model does not exist**: no instruction sets any FPSCR cause
>   bit and no arithmetic trap is delivered. #297 made it observable (`STS FPSCR` after
>   `ftrc(+Inf)` reads V=0 where hardware reads 1). Not patched piecemeal, because a lone
>   V bit would imply the other flags work. OpenBSD leaves the enables clear at exec.
> - **MIPS FCSR exception flags** — deferral re-confirmed 4–0. The blockers are
>   structural: `ieee_float_value` carries a single `nan` flag (no qNaN/sNaN
>   discrimination, so V is uncomputable) and the stores return a bare value with no flag
>   channel. **New reopen condition:** #299/#300's residual machinery computes exact
>   inexactness as a byproduct, which makes the I flag nearly free and inverts the
>   original "I last" sketch.
> - **#300's accepted-nearest bands** — div/sqrt below a 2^-969 operand, mul below a
>   2^-969 product — are real divergences from IEEE, pinned as named gate vectors rather
>   than hidden. Closing them needs scaled residuals, not a threshold.
> - **SH `fsca` and `fsrra` stay on the truncating store**: transcendental
>   approximations where silicon deviates by roughly 2^-21, so no witness exists whose
>   correct answer is decided by `FPSCR.RM`. Untestable by this project's rule.
> - **#291 was a symptom fix**: 32 ARM CPU table entries still have an unpopulated
>   `dcache_shift`, `iway`/`dway` are ignored, and ARMv6 parts use a different cache-type
>   register format than the v4/v5 layout hardcoded for every CPU.
> - The console overrun's remaining two sites are **X11-only** and this project runs
>   headless; the SuperH `RDF` status bit is never set (patched and measured — it was not
>   the input-loss cause), and the SSR verbatim-write and FDR-width warts stand.
> - Items 4, 6, 7 and 9 of the rounds 41–46 block: LANCE `STP` on chained frames
>   (unreachable on both rigs), the Class-A diagnostic remainder, `dev_wdc.c`'s
>   guest-reachable `exit()` (out of scope), and the #182-shaped stale length on the
>   VGA's accepted mode paths.
> - **OB-22** (`dev_jazz.c:613` jazzio vector-read blanket deassert) — self-healing, and
>   a change there would touch the verified arc boot.

> ## ✅ 2026-07-30 — RESOLVED as #294: cvt.w honours the rounding mode (item 2 of the rounds 41–46 block)
> `cvt.w` of 3.5 under the default mode now yields 4 (nearest-even); `trunc.w` still
> truncates regardless of the mode, as the architecture requires — and the live probe
> proves both, on both rigs, under all four FCSR modes (32 rows, PROBE294_PASS). The
> panel-refuted proof (a computed remainder can equal 0.5 for a non-tie) and the repaired
> midpoint comparison, the mode-by-mode boundary table, and the non-discriminating
> +2147483647.5 case are all recorded in CHANGELOG "Fifty-ninth round". The related trap
> is now enforced by a mutation self-test: the W arm rounding under LEGACY is a mutant the
> gate must detect.

> ## 2026-07-30 — NEW, well-scoped next candidate: round.w / ceil.w / floor.w / cvt.l are not decoded
> Found by the #294 panel and verified by two seats independently. The COP1 dispatcher
> admits these by format, `fpu_function()` matches no function code (upstream's own TODO
> at ~:1056 lists exactly these opcodes), and the tail raises a Coprocessor-Unusable
> exception for CP1 **with CU1 already enabled** (`cpu_mips_coproc.c` ~:2373-2381). A BSD
> kernel answers CpU(1) by granting the FPU and retrying the same instruction — a retry
> livelock plus a host-log flood. Latent on both rigs: zero `UNIMPLEMENTED coproc1
> function` markers across green boots, and OpenBSD 2.2's base system does not emit these
> opcodes. With #294's forced-mode parameter the fix is three copies of the trunc.w decode
> block — `round.w` forces nearest, `ceil.w` toward-+Inf, `floor.w` toward--Inf — plus a
> decision about `cvt.l` (MIPS III; the ISA-gating question recorded under #290/#273
> applies). Directly testable with the #294 probe pattern: `round.w.d(2.5)=2`,
> `ceil.w.d(2.25)=3`, `floor.w.d(-2.25)=-3` under FCSR mode 1, proving the override.

> ## 2026-07-30 — #26 re-review (four seats, unanimous): the FCSR exception-flag defer STANDS after #292
> #292 thinned exactly one blocker — target-format rounding now exists, so the
> Overflow/Underflow/Inexact flags are computable in principle. Everything load-bearing is
> untouched, verified in-tree: the store has no channel to return flag events (an API
> change across five CPU families); `struct ieee_float_value` still carries a single `nan`
> flag, so signalling-NaN Invalid is undetectable; trap delivery does not exist (only
> `MIPS_FPU_EXCEPTION_UNIMPL` is ever raised, and the CTC1 enable-bit TODO stands);
> R3000 FCSR bit-identity (#246) still constrains; and the guest enables no FP traps and
> reads no sticky flags (the kernel zeroes FCSR on exec and after every FP trap), so the
> in-scope consumer count is zero. If a consumer ever appears, the panel's first slice is
> STICKY FLAGS ONLY — Z and O first (both cleanly detectable post-#292), V only after
> qNaN/sNaN discrimination exists, I last — R4000-gated, with no cause/trap semantics.

> ## ✅ 2026-07-30 — RESOLVED as #292: S-format round-to-nearest (was item 8 / "round 55 unblocked")
> Fixed via a mode-aware sibling `ieee_store_float_value_rm()`; the historical entry point
> is a bit-identical wrapper and only the MIPS store passes `FCSR & 3`. Measured before:
> 50.12% of in-range single-precision stores 1 ulp low. Measured after: 0 mismatches
> against the host's correctly-rounded oracle over ~10M finite inputs, and a live-rig probe
> shows `ctc1` RM=0 → `cvt.s.d(1/3)` = `0x3eaaaaab`, RM=1 → `0x3eaaaaaa` on both pmax and
> arc. See CHANGELOG "Fifty-seventh round". **Kept open under this entry, deliberately:**
> - ~~**SH FPSCR.RM is stored but decoded nowhere**~~ — **RESOLVED as #296** (round 61).
>   The blocker recorded here was "no live test until the landisk rig can run FP (its
>   ramdisk has no FP-capable tool)". That premise was wrong: no FP-capable *tool* is
>   needed, because the guest does not have to be booted at all. A cold debugger seeds the
>   registers, the guest executes one instruction and stores the result with its own
>   `fmov.s`, and the value is read back from memory. That is now gate 10, and it is how
>   the defect was reproduced before the fix.
> - ~~PPC `stfs` rounding is DISPUTED between panel seats~~ — **SETTLED 2026-07-30** from
>   Power ISA v3.0B Book I §4.6.3, quoted verbatim by a panel seat: `stfs` is a defined
>   bit-EXTRACTION (fraction truncated at bit 23; a denormalization band; no rounding, no
>   FPSCR.RN, "Special Registers Altered: None"); `frsp` is the rounding instruction. Do
>   NOT wire `stfs` to FPSCR.RN — that would move away from the architecture. The real
>   PPC defects found instead are listed in the at-a-glance section above.
> - ~~m88k models no rounding register at all~~ — **WRONG as recorded; see the
>   at-a-glance section above** (fcr file modeled and retained; live 1-ulp defect on
>   luna88k userland; queued as its own round).

> ## ✅ 2026-07-30 — RESOLVED as #293: the SuperH console input loss (2026-07-27 entry below)
> The mechanism was none of the recorded suspects: on landisk nothing claimed
> `machine->main_console_handle`, so handle 0 (polled each tick for CTRL-C) raced the
> SCIF's console handle for the same host stdin and stole whole lines —
> `console_charavail()` imports up to 100 bytes into whichever handle polls first. Fixed
> by the one-line claim `dev_dreamcast_maple.c` / `dev_luna88k.c` / `dev_vr41xx.c` already
> make; Dreamcast is unaffected (maple still overrides, it initialises later). Measured:
> 10/12 commands stolen before, 12/12 delivered after; a side-effect probe proved the
> stolen commands never executed. **Instrument warning kept for the next console mystery:**
> a global chars-in/chars-out counter pair balanced at 77/77 *while lines were being
> stolen*, because the debugger's exit-time drain of handle 0 evened the books — count
> per-handle or not at all. The never-set RDF status bit remains a modelling gap (patching
> it changed nothing here); the SSR verbatim-write and FDR-width warts are recorded in the
> round-58 panel record.

> ## ✅ 2026-07-29 — RESOLVED as #291 (see CHANGELOG "Fifty-sixth round")
> Fixed: an unspecified cache size now encodes as 0 and each field is masked to its own
> width. `rpi` goes from 1 sanitizer report to 0; `cats`, `netwinder`, `iq80321`, `iyonix`
> and `testarm` stay at 0; both trees rebuild 0/0. Worth keeping from the investigation:
> it affected **32** CPU table entries, not just `rpi`, and casting to unsigned would have
> silenced the sanitizer while leaving the register byte-identically corrupt.
>
> **2026-07-30 retroactive review (one seat) — the fix stands, and it is a SYMPTOM fix.**
> Per the ARM ARM, a size field of 0 means a **512-byte cache**, not "unspecified" — the
> real defect is that those 32 table entries in `arm_cpu_types.h` simply never had their
> `dcache_shift` populated. So the register is no longer undefined or corrupt, but it
> under-reports the D-cache on those CPUs. The only reader is the guest's
> `MRC p15,0,Rd,c0,c0,1`, and GXemul executes cache flushes as no-ops, so nothing a guest
> does changes — the visible effect is a wrong size in a guest kernel's boot messages.
> Follow-on candidates recorded, none taken up (all latent, none testable on the rigs):
> populate the 32 missing `dcache_shift` values from CPU datasheets; honour the table's
> `iway`/`dway` fields instead of the hardcoded 32-way/8-word constants; shifts above 16
> would silently wrap in the 3-bit field (no current entry exceeds 16); and ARMv6 parts
> (ARM1136) architecturally use a different cache-type register format than the v4/v5
> layout GXemul hardcodes for every CPU.

> ## 2026-07-29 — NARROWED: the console/keyboard overrun is X11-only, and mostly guarded
> The earlier entry (item 5 of the rounds 41–46 block) says three ring buffers share the
> "overrun discards the whole queue" shape, one fixed and two still broken. The *code
> pattern* is identical in all three, but two of them have **feeder-level guards the entry
> does not mention**, so the exposure is far narrower than it reads:
>
> * `console/console.c:311` — the site is unguarded, but `console_charavail()` refuses to
>   read when the FIFO has less than 101 bytes of room, and **that guard is upstream's**
>   (`git log -S roomLeftInFIFO` shows only the import commit). The stdin path therefore
>   cannot overrun. Bypassing callers: `x11.c` (42 sites), `debugger.c` (11),
>   `dev_ns16550.c`, `dev_vr41xx.c` (24).
> * `devices/dev_dc7085.c:109` — the site is unguarded, but `lk201.c:253` loops on
>   `space_available_in_queue()`, which reserves 20 slots, before feeding console input.
>   The bypasses are the X11 keyboard/mouse expansions (`lk201.c:135-148`, `199-203`,
>   `290-291`), each adding up to ~4 bytes per event unchecked — so an overrun needs more
>   than five X11 events between drains.
> * `devices/dev_pckbc.c:159` — already fixed by #288.
>
> **Net: the residual exposure on both remaining sites is X11-only.** This project runs its
> rigs headless, so the bug cannot be reproduced in our own configuration — which under
> "only change what we can test for" means it is not fixed here. Recorded so the next
> reader does not act on the older entry's wider framing.

> ## 2026-07-29 — (superseded, kept for the trail) undefined behaviour in the ARM cache-type register, on `rpi`
> **What's wrong.** `cpus/cpu_arm.c:144` builds the ARM cache-type register like this:
>
> ```c
> | ((cpu->cd.arm.cpu_type.dcache_shift - 9) << ARM_CACHETYPE_DSIZE_SHIFT)
> ```
>
> On the Raspberry Pi machine (`-E rpi`) `dcache_shift` is 0, so this shifts **−9** left,
> which is undefined behaviour in C. The same site is used for `icache_shift` two lines
> below.
>
> **How it was found.** Gate 9 (the AddressSanitizer machine sweep) reports it on *both*
> upstream 0.7.0 and this fork:
>
> ```
> cpu_arm.c:144:49: runtime error: left shift of negative value -9
> ```
>
> So it is **inherited from upstream, not introduced here** — one of only two machines in
> the whole sweep still dirty on both sides, against 13 where this fork already fixed the
> memory errors.
>
> **Why it wasn't fixed in this round.** The fork has touched `cpu_arm.c` (two lines), but
> not this site, and it is outside the pmax/arc priority scope. It is also *latent*: the
> register is documented in-source as "aren't used yet". The fix is the same pattern as
> corrections #24/#25 — compute in an unsigned type, or guard the subtraction so it cannot
> go negative — but per the project rule, it needs a test that reproduces the wrong
> behaviour first. Gate 9 already is that test, which makes this a well-scoped next round.


> ## 2026-07-27 — (superseded, kept for the trail) the SuperH console loses guest input non-deterministically
> **→ RESOLVED as #293 — see the ✅ entry at the top of this file. The mechanism was none
> of the suspects recorded below** (it was an unclaimed main console stealing lines before
> the serial port saw them), but the refuted-hypothesis measurements below are what made
> the real diagnosis fast, so they stay.
> Found while building the landisk rig for round 55's harness, and **not yet diagnosed** —
> recorded here with its measurement so a future round starts from evidence rather than
> from the symptom.
>
> **Symptom.** Driving OpenBSD 7.6 / landisk (`-E landisk -M 64 openbsd76-landisk-bsd.rd`)
> to the installer's `(S)hell` and then typing commands, individual commands vanish
> **whole**: no terminal echo, no output, no error. The shell is alive — a command sent
> moments later runs correctly and prints the right answer.
>
> **What it is not.** Three hypotheses were tested and refuted:
> - *Timing.* Adding a settle delay before each write, and raising the post-write wait from
>   8 s to 25 s, changed nothing.
> - *Line terminator.* Switching from `\r` to `\n` (what the long-standing pmax and arc
>   rigs use) improved matters but did not fix them.
> - *Input length.* One boot, ten `echo` commands of increasing length: the **15, 23 and
>   33** byte lines ran; the **9, 17, 27 and 41** byte lines were lost. Neither a length
>   ceiling nor a strict alternation. Roughly one write in three survives.
>
> Retrying a command up to six times still failed to land `$((6*7))` or `uname -m`
> reliably, and even a bare `echo` succeeded only sometimes.
>
> **Where to look.** `dev_scif.c` (the SH SCIF serial console) and the console host-glue in
> `core/console.c`. Rounds 26/27 (#251/#252) already found two real bugs in that glue — an
> output-flush bookkeeping error and a stdin-EOF freeze — so an input-side defect in the
> same area is plausible. The alternative is a receiver-ready/interrupt-timing issue in the
> SCIF model itself, where a byte written while the guest has not armed its receiver is
> dropped instead of held.
>
> **Why it was not chased in round 55.** The rig only needed a dependable boot gate, and
> `BOOT_REACHED` is 1 on every run, so the harness asserts the boot and the chip identity
> the guest's own PCI probe prints (`shpcic0 at mainbus0: HITACHI SH7751R`) and sends no
> input at all. That is honest coverage; this is a separate bug and deserves its own round.
> **Reproduce with** `regress/drive_guest.py` by giving the `landisk` rig a `steps` list.

> ## 2026-07-27 — (superseded, kept for the trail) Round 55: the harness UNBLOCKED an item that was dropped as un-testable
> **→ RESOLVED as #292 — see the ✅ entry at the top of this file.** This entry records the
> moment the obstacle turned out to be the instrument rather than the bug.
> **S-format round-to-nearest** (`core/float_emul.c` ~277: `ieee_store_float_value()` truncates to 23
> fraction bits, so single-precision inexact results are 1 ulp low — pre-existing, all ops, all five
> calling CPU families) was previously set aside as **un-testable**: exercising it live was thought to
> need hand-written single-precision assembly, because the OpenBSD 2.2 rig image has no working `cc`
> and gcc never emits the relevant instruction forms.
>
> **That reasoning was wrong, and round 55's `regress/diff_ieee_store.c` is the counter-example.**
> `ieee_store_float_value()` is a **pure function**, so it needs no guest at all: it can be
> differentialled offline over tens of millions of inputs in seconds, and — unlike the #287 overflow
> case, where the differential compared old against new — round-to-nearest has an **independent
> oracle** available. The host's own `(float)x` conversion *is* correctly-rounded IEEE-754, so the
> test is not "did the answer change" but "is the answer right", which is a strictly stronger claim
> than anything the project has been able to make about this function.
>
> The measurement to run first, per the standing "only change what we can test for" rule: sweep random
> doubles, compare `store(x, IEEE_FMT_S)` against the host `(float)` result, and count how many differ
> and by how much. If the 1-ulp-low characterization is right, the differential will show it directly
> and bound the blast radius before a line is edited. **Still un-fixed — this entry records that the
> obstacle was the instrument, not the bug.**
>
> Note the one thing the offline route does *not* cover, so it is not oversold: SH-4 resets to
> round-to-zero (established in round 51), so any rounding change must be FCSR/FPSCR-aware rather than
> unconditionally round-to-nearest. The differential can prove the arithmetic; it cannot by itself
> decide the per-architecture rounding-mode policy.

> ## 2026-07-26 — Rounds 41–46 (#271–#279): the backlog this batch DOCUMENTED rather than fixed
> Six rounds shipped **nine corrections** (#271–#279) across `devices/dev_vga.c`, `core/float_emul.c`,
> `devices/dev_le.c`, `devices/dev_asc.c` and `cpus/cpu_mips.c` — see CHANGELOG / REVIEW_FINDINGS
> "Forty-first" … "Forty-sixth round". Each round was gated on its own; the batch was then closed with a
> **holistic regression at HEAD `b38cc4f` built from committed source** (clean rebuild **0 warnings / 0 errors**
> both trees, 223 pmax / 224 arc objects; **pmax 15/15 + arc 13/13 → `uid=0(root)`**; log hygiene **0** for
> every string the batch touched; live pmax ping **3/3, 0 % loss**; in-guest `sprintf("%d", ±1e30)` →
> `+2147483647` both signs; all twelve per-correction probe rigs re-run on the final binaries, plus the
> `trunc.l` addendum; the #274 would-fire counter still **0** on both a healthy boot and a flood, byte-identical
> to the pre-change reading; 20/20 machines byte-identical to a pre-batch binary rebuilt from `be95418` on both
> trees; divergence set still exactly the five known files).
>
> **The items below were found and characterized during this batch and deliberately NOT fixed.** Each is
> recorded with the evidence a next round needs, so the backlog is a record rather than folklore. Line numbers
> are at HEAD `b38cc4f`; items 8 and 9 were added later and re-verified at HEAD `895af34`, which touches only
> `README.md` and this file, so every number in the block refers to the same source.
>
> **STATUS AS OF 2026-07-30 — five of the nine have since been dealt with; the items keep their original
> text as the historical record, each with a pointer:**
> - item 1 → partly resolved as **#290** (round 54: the ISA gate); the PS-arithmetic half is still open
> - item 2 → resolved as **#294** (round 59), and its round-to-nearest tail as **#292** (round 57)
> - item 3 → defer **re-confirmed 4–0** on 2026-07-30 (entry at the top of this file)
> - item 5 → the pckbc third fixed as **#288** (round 52); the rest narrowed to X11-only (2026-07-29 entry)
> - item 8 → resolved as **#287** (round 51)
> - items 4, 6, 7, 9 → still open, unchanged
>
> 1. **[→ partly resolved as #290, round 54: the ISA gate shipped; the PS-arithmetic half for
>    5Kc/5KE/SB1/SR7100 remains open]** **COP1 ISA-level routing — the best-scoped next-round candidate (fidelity, not hygiene).** An R4000 is
>    MIPS III, but `cpus/cpu_mips_instr.c:4991-4995` admits `COP1_FMT_PS` (along with S/D/W/L) to `cop1_slow`,
>    so `add.ps` **executes** on an R4000/R3000 and silently writes `fd = 0x00000000` instead of raising
>    **Reserved Instruction**. Measured in round 46: one `add.ps` produced 8.0 host lines and a zeroed `fd`,
>    identically on arc/R4000 and pmax/R3000A; only PS reaches `float_emul.c` at all — every *other* reserved
>    fmt hits the decoder's own `fatal()` + `goto bad` at `:5006-5008` (fmt 18 and fmt 23 controls: **0**
>    `float_emul` lines). **The constraint already established, and the reason this is not a one-line deletion:
>    `include/mips_cpu_types.h` DOES contain `isa_level == 64` CPUs that have FPUs — `5Kc` (:103), `5KE` (:104),
>    `SB1` (:111), `SR7100` (:112) — for which PS is architecturally plausible (MIPS64r1 defines it; r6 removes
>    it). So the routing cannot simply be deleted.** The fix has **two halves**: an ISA gate that raises RI below
>    MIPS-V, *and* the fact that `float_emul.c` models no PS arithmetic whatsoever, so gating alone would leave
>    those CPUs without a format they are entitled to. Whoever picks this up must decide both. Same family:
>    **`trunc.l` executes on an R3000A** although it is MIPS III and an R3010 would raise RI — measured in
>    round 42 and re-measured in this regression. That measurement has a trap worth keeping: the obvious
>    `sdc1` read-back of the result is itself a MIPS-II 64-bit store an R3000 does not have, so the RI it
>    raises is easily mistaken for the instruction under test faulting; reading `$f2`/`$f3` back with two
>    MIPS-I `swc1`s (`probe_273_pmax_l.py`) shows `trunc.l.d` really did run and returned the pinned values.
>    So the COP1 decoder does not enforce ISA level **anywhere**.
> 2. **[→ resolved as #294, round 59; the round-to-nearest tail as #292, round 57]**
>    **FP rounding mode — `cvt.w` truncates, and `FCSR.RM` is read nowhere.** `cvt.w` of `3.5` yields **3**
>    where the MIPS default rounding mode (RN, round-to-nearest-even) gives **4**; measured as a deliberate
>    control in the #273 probe, which carries both a rounding-*sensitive* case (`3.5`) and a rounding-*insensitive*
>    one (`3.25`) so this defect can never be confused with the conversion defect #273 fixed. A tree-wide grep
>    finds `MIPS_FPU_FCSR` touched **only** for the condition-code bits and the flush-to-zero bit
>    (`MIPS_FPU_FLUSH_BIT`, #246): the **rounding-mode field is never decoded anywhere**. **Record the trap:
>    `cvt.w` should honour `FCSR.RM`, but `trunc.w` is architecturally round-toward-zero *regardless* of RM, so
>    a future fix must NOT "fix" `trunc.w`.** That is not academic here — `cpu_mips_coproc.c` routes
>    `cvt.w.fmt` (`:1574`), `trunc.w.fmt` (`:1498`) and `trunc.l.fmt` (`:1485`) through the **same**
>    `FPU_OP_CVT` call with the same target format, so `cvt.w` and `trunc.w` are currently indistinguishable
>    downstream: honouring RM requires separating them first. Related and also unfixed: **S-format round-to-nearest** in `ieee_store_float_value()` (truncates the
>    fraction instead of rounding → single-precision results 1 ulp low), already recorded under round 28 and
>    still blocked on the same thing — gcc never emits the single-precision compares, so only hand-assembled
>    tests reach it.
> 3. **[→ defer re-confirmed 4–0 on 2026-07-30 after #292 — see the entry at the top of this file]**
>    **FCSR Invalid-flag signalling — still the documented deferred TODO.** #273 corrected only the *result* of
>    an invalid FP→integer conversion (the pinned `0x7fffffff` / `0x7fff…ffff`); the Invalid flag is still not
>    raised on these conversions, and the wider FCSR V/Z/O/U/I cause/flag maintenance + enabled-exception
>    trapping remains deferred for the reasons recorded under round 28 (needs qNaN/sNaN discrimination,
>    target-format rounding, R4000-gating so R3000 FCSR stays bit-identical per #246). Noted here because #273's
>    W bound was deliberately given slack that *would* matter only if Invalid signalling were added later.
> 4. **LANCE `STP` stamped on the last descriptor of a chained frame** (`devices/dev_le.c`): the end-of-packet
>    block clears `d->rx_middle_bit` at **`:604`** (and frees the frame), and the `STP` block at **`:610-611`**
>    then sets `LE_STP` *because* `rx_middle_bit` is clear — so the **last** descriptor of a chained frame is
>    stamped `STP` as well as `ENP`, and it carries the **whole frame length** in rmd3. A BSD driver reads that
>    as a complete single-buffer packet (`am7990_rint()` accepts only `STP|ENP` and otherwise prints "dropping
>    chained buffer"). **Pre-existing** (not introduced by #262 or #274) and **unreachable on both rigs** —
>    neither guest chains RX, which the #274 would-fire instrumentation measured directly (`rx_calls=14
>    frames=14` on a healthy boot + ping, `321/321` under flood, `la_extra_reject = 0` in both). Recorded so
>    that anyone who makes chaining reachable fixes this first.
> 5. **[→ the pckbc third fixed as #288, round 52; the remaining two narrowed to X11-only exposure on
>    2026-07-29 — see that entry — and left, since this project runs headless]**
>    **Console/keyboard FIFO overrun discards the WHOLE queue, not one byte.** Three ring buffers share one
>    shape — the producer advances/stores and *then* warns, leaving `head == tail`, which every consumer reads
>    as **EMPTY**: `console/console.c:306-315` (`console_makeavail`, `"console fifo overrun"`),
>    `devices/dev_dc7085.c:103-110` (`add_to_rx_queue`, `"rx_queue overrun!"`) and
>    `devices/dev_pckbc.c:129-137` (`pckbc_add_code`, `"queue overrun"` — this one advances the head, warns,
>    then stores at the new head). So an overrun does not drop the newest byte, it **silently discards every
>    byte already queued**. **Host-input-driven, not guest-driven** (it needs input arriving faster than the
>    guest drains it), which is why it is out of the guest→host charter and was not fixed in this batch; it is
>    also why the boot rigs never hit it (**0** occurrences of all three strings on the pmax and arc boot logs).
>    A fix would drop the incoming byte and keep the queue, not the other way round.
> 6. **The Class-A "ungated diagnostic a guest can repeat" remainder in the pmax/arc set.** Rounds 41/44/45/46
>    fixed the sites that were measured at 1.00+ host lines per guest access; these were **swept and left**:
>    - **MEASURED on the final binaries** (fresh boot logs, this regression — so these fire during an ordinary
>      healthy boot): `devices/dev_asc.c:406` `{ asc: data in, lenIn=%i lenIn2=%i }` — **1** hit on pmax, **5**
>      on arc; `devices/dev_fdc.c:75-78` `[ fdc: write to reg %i: … ]` (a **2+len-call** site: one `fatal()`
>      for the prefix, one per data byte, one for the closer; the read arm at `:71` is one call) — **2** hits on
>      arc, 0 on pmax; `devices/dev_pckbc.c:718`
>      `[ pckbc: TODO: hack for non-8242 … ]` — **1** hit on arc (this is the long-known pre-existing arc-log
>      line the hygiene greps whitelist). All other swept strings measured **0** on both logs:
>      `dev_pckbc.c:944` (`write to DATA`), `dev_jazz.c:199` (`dma not enabled?`) and `:207`
>      (`wrong direction?`), the `promemul/arcbios.c` escape-sequence loop (`:255-266`, one `fatal()` per byte
>      of an unimplemented sequence), the remaining `dev_le.c` register/SRAM write dumps (`:899-902`,
>      `:948-951`, `:964-968`), and `cpus/cpu_mips_coproc.c:1327` (`fpu_op(): unimplemented op`) / `:2365`
>      (`UNIMPLEMENTED coproc%i function`).
>    - **READ ONLY (static sweep — reachability reasoned from source, amplification not measured):** the
>      `dev_asc.c` tail — `:357`, `:369`, `:373`, `:396`, `:455` (a bare `printf("WARNING!!!!!!!!! BUG!!!!…")`),
>      `:487`, `:505`, `:579`, `:611`, `:648`, `:655`, `:760`, `:766`, `:780`. Two neighbours that a naive grep
>      would add are **compiled out** and are deliberately excluded: `:641` (`#ifdef MACH`) and `:943`
>      (`#if 0`).
>    None of these was reproduced test-first, so under the project rule ("only change what we can test for")
>    none was touched. The two that fire on a healthy boot (`asc: data in`, `fdc: write to reg`) are the
>    cheapest next targets **because they are already reproducible without a rig**; the rest need a trigger
>    designed first. Note the sweep's original line numbers were taken at `be95418` and rounds 43–44 have since
>    shifted them; the numbers above are re-located at HEAD `b38cc4f`.
> 7. **`devices/dev_wdc.c` guest-reachable `exit()` — out of scope, and stated precisely.** Four
>    guest-reachable `exit(1)` calls remain at **`:654`, `:669`, `:708`, `:730`**, and **`:708` fires on any
>    failed ATAPI command** (`WDC: ATAPI scsi error?`). **`machines/machine_pmax.c` does not instantiate the
>    device at all, and `machines/machine_arc.c`'s `device_add(machine, "wdc addr=0x900001f0, irq=38")` at
>    `:235` sits inside a `#if 0` (`:232`) whose body begins `Not yet.` (`:233`).** That precision matters: an
>    earlier, looser phrasing of this item said only "not instantiated", which was corrected during round 41 —
>    the `device_add` line *does* exist in `machine_arc.c`, it is simply compiled out. So the site is real and
>    the `exit()` is a genuine defect of the same class as #167/#240/#264/#271, but it is unreachable on either
>    rig and belongs to a tree-wide `fatal()`/`exit()` hygiene round rather than to the pmax/arc mandate.
> 8. **[→ resolved as #287, round 51 — CHANGELOG "Fifty-first round"]**
>    **S-format store: an overflow produces a NaN encoding where hardware gives ±Inf.** In
>    `core/float_emul.c`, `ieee_store_float_value()` (`:245`) reaches the shared S/D arm at `:309-310`, whose
>    `FP_NORMAL` case (`:330`) writes the fraction bits into `r` at `:354-360` and *then* **clamps** the biased
>    exponent at `:367-368` (`if (exponent >= ((int64_t)1 << n_exp)) exponent = ((int64_t)1 << n_exp) - 1;`)
>    and ORs it in at `:369` — **without clearing the fraction it has already written**. Exponent 255 with a
>    non-zero fraction is a **NaN** encoding. The `FP_INFINITE` arm two cases up (`:318-323`) holds the right
>    answer (`0x7f800000`) and is simply never reached, because the *double* being stored is finite; it is the
>    single-precision destination that overflows. Measured in this batch's class-B sweep: `1e40` →
>    **`0x7feb194f`**; a second seat independently measured `1e39` → **`0x7fbc143f`**, `1e300` →
>    **`0x7fbf21e4`** and `-1e300` → **`0xffbf21e4`**, where hardware gives `0x7f800000` / `0xff800000`. **All
>    four reproduce bit-for-bit** when the function's own arithmetic is replayed on host doubles, which also
>    pins the threshold: the clamp first fires at |x| ≥ 2^128 ≈ `3.4028e38`, just above `FLT_MAX` — `3.4e38`
>    still stores exactly (`0x7f7fc99e`, identical to a host `(float)` cast) while `3.5e38` already yields
>    `0x7f83a7c6`. (That is a re-derivation, not a live reading; an in-emulator measurement still wants a
>    hand-assembled `-V step` probe of the round-46 shape.) **The interaction that lets this survive #255 is
>    the part worth keeping:** the NaN canonicalizer #255 added (`cpus/cpu_mips_coproc.c:1123-1133`) gates on
>    `fpclassify(nf) == FP_NAN` at `:1128`, and `nf` is the *host double* result — `fpclassify(1e300)` is
>    `FP_NORMAL`, so the canonicalizer never fires and the bogus NaN reaches `fd` untouched.
>    **Reachable from ordinary guest FP code**, not only from hand-assembly: `cvt.s.d` of any double past the
>    threshold (`cpu_mips_coproc.c:1552`, `output_fmt = COP1_FMT_S`) and any `add.s` / `mul.s` / `div.s` whose
>    result overflows single precision (`:1392`, `:1416`, `:1428`, each passing `output_fmt = fmt`); all of them
>    reach `fpu_store_float_value()` (`:1105`) → `ieee_store_float_value()` (`:1121`). **Distinct from the
>    S-format round-to-nearest item in 2 above** — that one is a 1-ulp truncation of the fraction (the same
>    `:354-360` loop), this one produces the wrong *class* of value.
>    **The blast radius is wider than #273's, which is the reason it is recorded rather than fixed.** #273 was
>    confined to the MIPS-only W/L arm and said so; the S/D arm is shared. On the **store** side mips, m88k
>    (`cpu_m88k_instr.c`), ppc (`cpu_ppc_instr.c:2421`, `:2444`) and sh (`cpu_sh_instr.c`) all store S, and
>    alpha stores D (`cpu_alpha_instr.c` has zero `IEEE_FMT_S` references); `dev_pvr.c` touches the S arm on the
>    **interpret** side only (13 `ieee_interpret_float_value(…, IEEE_FMT_S)` calls, no stores). So this needs
>    the non-MIPS blast-radius gate #279 used, not a MIPS-only one.
>    **Fix shape one seat proposed, recorded because it is a better shape than three separate S-format
>    patches:** follow the **#254** precedent and route the S store to the host FPU — a single `(float)` cast
>    plus a `memcpy` into a `uint32_t` — which collapses **three** defects into one change: this one, the
>    round-to-nearest truncation (item 2), and the **underflow sign loss** at `:365-366` + `:372-373`, where a
>    value too small for single precision is clamped to exponent 0 and then `r = 0` discards the sign bit set at
>    `:312-313` (`-1e-40` stores as `0x00000000`, not `0x80000000`; same replay). On MIPS that third half is
>    partly masked — #246's guard at `cpu_mips_coproc.c:1115-1119` traps an S-format result below `FLT_MIN`
>    rather than storing it — but only on EXC4K parts and only while `FCSR.FS` is clear (`fpu_unimpl_trap()`
>    returns 0 for EXC3K at `:1091-1092`), and the other four families have no such guard at all.
> 9. **The #182-shaped stale length is still live on the VGA's *accepted* mode paths — latent, and deliberately
>    left.** In `devices/dev_vga.c` the geometry block that follows a mode change assigns `d->fb_size`
>    **unconditionally** in both arms — `:924-925` (charcell) and `:929-930` (graphics) — immediately after
>    calling `dev_fb_resize()` at `:921-923` / `:927-928`, which returns `void` and whose effect is never
>    checked. `dev_fb_resize()` (`devices/dev_fb.c:123`) has **five** early returns that leave the old buffer
>    and the old `d->framebuffer_size` in place: `:129-132` (`d == NULL`), `:134-142` (#184, a dimension < 10),
>    `:147-151` (#156, a dimension > 16384), `:153-157` (`bytes_per_line` overflow) and `:161-165` (total-size
>    overflow); the buffer and its length are updated only at `:189-190`, past all five. `fb_size` is then used
>    as a **write bound** at `dev_vga.c:381` (graphics redraw) and `:488` (text redraw), each gating a
>    `dev_fb_access(…, MEM_WRITE, d->fb)`. That is the same shape as **#182** — a length outliving the resize
>    that was supposed to change it — which was rated CRITICAL. **Two independent review seats found it.**
>    **It is NOT guest-reachable on pmax/arc, so it is latent, and the panel's explicit call was to document it
>    rather than expand round 41 into it:** #271 now `return`s at `:917`, before the block, on a rejected mode,
>    and all eleven accepted mode bytes are self-consistent — at the default `scaleup == 1`
>    (`machines/machine.c:91`) every accepted arm resizes to 640×400, 640×350 or 640×480, far inside
>    `dev_fb_resize()`'s [10, 16384] window, so no accepted mode can take an early return. The only route found
>    is host configuration rather than guest input: `-Y -26` or lower (`core/main.c:490-501`, and the same shape
>    in `core/emul_parse.c:545-547`) makes `scaleup > 25` and pushes a charcell width past 16384 — reasoned
>    from source, **not** exercised.
>    **Two qualifications, so the item is neither over- nor under-stated.** (a) A stale-too-large `fb_size`
>    would **not** overrun the host through these two sites: `dev_fb_access()` re-bounds every access against
>    `d->framebuffer_size` at `dev_fb.c:719-721` (the OB-1 end-span guard), so the observable consequence is
>    dropped or mis-shaped paint, not a write past the allocation. The *shape* is #182's; the severity is not,
>    and #182's own severity came from feeding the dyntrans fast-map (`core/memory.c:339`,
>    `memory_device_update_length()`), which this does not. (b) Noticed while verifying, and belonging to the
>    same fix: `d->fb_max_x` / `d->fb_max_y`, which supply the **stride** in both bounded expressions
>    (`:379-380`, `:486-487`), are assigned **only** in `dev_vga_init()` (`:1307-1311`) and are never
>    recomputed on a mode change — so after even a *successful* resize the address arithmetic still uses the
>    initial geometry while `fb_size` describes the new one. Whoever fixes the `fb_size` assignment should fix
>    that in the same pass.
>
> **Resolved by this batch — do not carry these forward:**
> - **"In-guest FP microtest blocked" (recorded under round 28) — RESOLVED for the paths that matter.** That
>   note assumed a future round would have to install a toolchain or inject a static MIPS binary, because the
>   OpenBSD 2.2 rig image has no working `cc`. Round 42 found the route with no compiler at all: `awk`'s
>   `printf`/`sprintf` **`%d`** casts a double to a C `long`, which on 32-bit MIPS is exactly the double→int
>   conversion, so `sprintf("%d", 1e30)` → **2147483647** and `sprintf("%d", -1e30)` → **+2147483647** proves
>   #273 end-to-end in ordinary compiled guest code (round 28's regression had already reached `div.d`/`sqrt.d`/
>   `c.lt.d` through plain `awk` arithmetic). Recorded with its trap: **`awk`'s `int()` does NOT exercise this
>   path** — it stays in floating point (`int(1e30)` prints `1.0000…e+30`, `int(3.9)` yields `4`), so a test
>   built on `int()` proves nothing. What remains genuinely blocked is only the **single-precision** S-format
>   work in item 2, which needs hand-assembled instructions gcc never emits.
> - The open question under #279 — whether the COP1 PS routing could simply be removed — is **answered** (item
>   1: no, `mips_cpu_types.h` has MIPS64 CPUs with FPUs), so it is no longer an open question, only an
>   unimplemented fix.
> - Older, and noticed while auditing this file for stale entries: the seventeenth/eighteenth-round blocks below
>   still list **"#185 `dev_asc.c` DATA_OUT `data_out_len==0` `exit(1)`"** as deferred. It was **resolved as
>   #264** (round 35) — the branch now `fatal()`s and returns 0, which the `NCRCMD_TRANS`/`NCRCMD_TRPAD` caller
>   converts into a guest-visible SCSI disconnect. Recorded here rather than by editing the historical blocks,
>   which are kept as the audit record.

> ## 2026-07-19 — Post-batch pmax/arc fidelity cluster: CONCLUDED (2 refuted, 2 un-testable, 2 left untriaged)
> After rounds 28-39 (#254-#268) a final pmax/arc fidelity cluster of 6 candidates was scoped under the rule
> **"only change what we can test for"** + a full 4-model panel per change. Outcome — **no further corrections
> made; the pmax/arc hardening is considered complete for this pass:**
> - **REFUTED by test-first** (details in the entry below): unaligned-ifetch TLBL-vs-AdEL (already correct via
>   #228) and arc VGA text-console char-drop (faithful differential repaint, mis-measured).
> - **Un-testable on the rigs → not changed** (per the rule): **S-format FP round-to-nearest**
>   (`core/float_emul.c:~277`, `ieee_store_float_value` truncates the fraction instead of round-to-nearest →
>   single-precision 1 ulp low) — reaching it needs hand-assembled single-precision ops (gcc never emits
>   c.olt.s/etc.; the rig image has no in-guest `cc`), AND the function is SHARED across alpha/m88k/mips/ppc/sh so
>   the blast radius exceeds pmax/arc; **arc partition LBA signed `int*512`** (`arcbios.c`, defeats the #168 bound
>   on a hostile partition table) — needs a crafted large-LBA partition image to exercise. Both remain genuine
>   pre-existing candidates; deferred until a test fixture exists.
> - **LEFT UNTRIAGED this pass** (low value, deferred): **OB-22** (`dev_jazz.c:613` jazzio vector-read blanket
>   `mips_irq_3` deassert without clearing `int_asserted` → possible stuck/missed non-timer JAZZ IRQ) — latent
>   (the arc boot reaches 13/13 without hitting it, so a repro needs a crafted multi-IRQ sequence and the fix
>   would touch the verified arc boot); **NE2000 invalid-TX log-flood** (`dev_ne2000.c`, SEC-only) — cosmetic log
>   hygiene, gate the diagnostic if pursued. Neither triaged; recorded here so they aren't lost.

> ## 2026-07-19 — GXEMUL trueness candidates TEST-FIRST TRIAGED → both REFUTED (no change; "only change what we can test for")
> Two gxemul candidates were raised from the cross-arch trueness campaign, then reproduced test-first on the
> committed builds before any change. **Both NOT-REPRODUCED — neither is a real reachable bug; no fix made:**
> - **unaligned instruction-fetch exception class (TLBL vs AdEL) — ALREADY CORRECT.** Correction **#228** guards
>   all six register-indirect PC-setting sites (`cpu_mips_instr.c` 1343/1373/1396/1424/1462/1495: `if (pc & 3)
>   → EXCEPTION_ADEL`). Live test: pmax `jr ra`/`jalr` with ra=0x42424242 → `cause: ADEL (exccode 4)` on BOTH
>   R3000 and R4000. `jr`/`jalr` are the only genuine MIPS instructions that can produce an unaligned PC (j/branch
>   targets are word-aligned by encoding), so the reachable path is fully covered. The residual TLBL appears ONLY
>   when `pc` is *forced* unaligned in the debugger (non-instruction) — present identically on R3000 AND R4000, so
>   not R3000-specific and not guest-reachable. The trueness note's "R3000 TLBL" was that debugger artifact.
> - **arc VGA text-console character-drop — FAITHFUL differential repaint, not a drop.** `vga_update_textmode`
>   (`dev_vga.c:276`) emits `ESC[y;xH`+char only for cells that CHANGED vs `charcells_outputed`, and never emits
>   `\n` — correct for a persistent 2D ANSI terminal / the real VGA screen. Live test: a 25-line rapid burst
>   renders all visible lines + `FINALMARKER…DONE` byte-perfect on a faithful 2D render. The campaign's
>   `BOUND`→`BOUN` was a LINEARIZATION artifact (ANSI-stripping the paint stream without a terminal model makes
>   skipped-because-unchanged cells look dropped) plus an INVALID test (arc root shell is `csh`; the burst used
>   `sh` `while`/`$((…))` → "Illegal variable name"). `console_putchar` writes every byte with the #251 flush
>   guarantee — nothing is lost at the console layer.
> Test scripts (scratchpad): `itemA_pmax.py`/`itemA_pmax_jalr.py`/`itemA_arc.py`, `itemB3_arc.sh`/`itemB3_parse.py`.
> (Latent/optional, NOT live bugs: the generic-fetch-path TLBL divergence is arch-neutral + debugger-only-reachable.)
> Already-resolved trueness items (NOT open): **L12** serial-drop → #251; **L5** pty/forkpty hang → #252; **L13**
> UDP-inetd handoff → dispositioned (userspace-NAT topology, reachable via tap **#253**). Inherent GAPs (not
> fixable without a rewrite): **L1** not-cycle-accurate; **L7** FP/uninitialized-memory lowest-confidence (FP
> largely #254/#255; uninit zero-fill #244). **[FAITHFUL]** L2 strict-alignment + LE endianness are correct
> reproductions — do NOT touch. All the trueness doc's #5–#23 security items are [FAITHFUL] gxemul reproductions
> (they *confirm* fidelity), not emulator defects.

> ## 2026-07-18 — Twenty-eighth round (#254, #255): MIPS FPU result-correctness (4-model panel)
> Item #1 of the 8-item TODO-triage batch. Applied **#254** (div/sqrt/compare result bugs in `fpu_op`) + **#255**
> (NaN → legacy-MIPS quiet-NaN canonicalization), 4-model-panel designed+reviewed (Codex xhigh + agy + Fable +
> Ollama), build 0/0 both, pmax 15/15 + arc 13/13 boot, host-side FP-logic microtest 11/11 (rig image lacks an
> in-guest compiler).
> **DEFERRED (own future corrections, documented):**
> - **FCSR V/Z/O/U/I cause/flag maintenance + enabled-exception trapping** — needs qNaN/sNaN discrimination (`struct
>   ieee_float_value` keeps only one `nan` flag), target-format rounding for O/U/I, R4000-gating (R3000 FCSR must
>   stay bit-identical per #246), and the CTC1-writes-enabled-cause TODO (`cpu_mips_coproc.c` ~2216). ~0 benefit for
>   OpenBSD 2.2 (no FP traps enabled); medium-high risk. Panel unanimous DEFER.
> - **S-format round-to-nearest** in `ieee_store_float_value` (`float_emul.c` ~277 truncates to 23 fraction bits →
>   single-precision inexact results 1 ulp low). Pre-existing, all ops; own correction.
>   **[→ resolved as #292, round 57; and the FCSR item above was re-confirmed deferred 4–0 on 2026-07-30]**
> - **In-guest FP microtest blocked** — the OpenBSD 2.2 rig image has no comp set / working `cc`; a future round
>   could install a toolchain or inject a static MIPS test binary to exercise c.olt/c.ole live (gcc never emits them,
>   so only hand-asm reaches those paths).

> ## 2026-07-18 — Twenty-seventh round (#253): Linux tun/tap enablement — L13 inbound now DELIVERABLE (Codex + Fable)
> Round 26 dispositioned L13 (inetd UDP `dgram/wait`) as "not an emulator bug — the userspace NAT has no
> unsolicited-inbound path; resolve via tap or an outbound hole-punch." A Codex `gpt-5.6-sol` + Fable panel enabled
> the tap path on Linux. **Applied + verified live:** **#253** `net/net_tap.c` `net_tap_init()` gains a
> `#if defined(__linux__)` branch opening `/dev/net/tun` + `ioctl(TUNSETIFF, IFF_TAP|IFF_NO_PI, ifr_name=tapdev)`
> (Linux tapdev = tap interface **name**; BSD `open(tapdev)` device-path unchanged in `#else`; shared FIONBIO/tail →
> non-Linux compiles byte-identical). Build 0/0 both trees; both NAT boot regressions still pass (pmax 15/15 + arc
> 13/13 → `uid=0(root)`, zero NAT-path impact since `net_tap_init` is only reached when `tapdev != NULL`). **Live
> proof (pmax rig):** `gxemul -e 3max -L tap0 -d 1:disk bsd.pmax` attaches (host `tap0` → `UP,LOWER_UP`); guest
> `ifconfig le0 10.0.0.10`; then host→guest **unsolicited** `ping` = 4/4 replies and a UDP datagram reached the guest
> kernel (ICMP port-unreachable) — the delivery the NAT structurally can't do.
> **=> The L13 class (unsolicited-inbound UDP services: inetd dgram/wait, portmap, photurisd) is now reachable via
> `-L tap0`.** Host setup: `ip tuntap add dev tap0 mode tap user $USER; ip addr add 10.0.0.1/8 dev tap0; ip link set
> tap0 up`. **Use the pmax rig** (arc/pica SONIC `dev_sn.c` is an RX/TX-less register stub; 3max LANCE `dev_le.c` is
> complete). Under WSL2 the tap is host↔guest only (VM net not bridged to the LAN) — sufficient for the proof. Header
> choice (`<net/if.h>`+`<linux/if_tun.h>`, not `<linux/if.h>`) resolved by test-compiling all three variants.

> ## 2026-07-18 — Twenty-sixth round (#251, #252): console host-glue fidelity (3-view panel)
> An OpenBSD 2.2 pmax/arc audit reported three "emulation-layer" bugs. A source-verified panel (Codex `gpt-5.6-sol`
> high + Fable + reviewer holistic pass, each `diff`-checked vs pristine `src/`) **converged** that the audit
> mis-attributed the subsystem in all three; the two real defects are in the shared host-console glue
> (`console/console.c`, byte-identical to stock 0.7.0). **Applied (both trees, build 0/0, pmax 15/15 + arc 13/13
> boot PASS, reproduced+fixed on the pmax rig):**
> - **#251** `console_putchar` cleared the stdout flush-pending flag on `'\n'` assuming libc line-flush — false
>   when stdout is a pipe/file (fully buffered), so newline-terminated bursts sit unflushed and are lost on
>   kill/wedge (the audit's "L12 serial drops output"). Always mark pending → `console_flush()` drains it. Not the
>   UART (DZ/ns16550 TX is lossless).
> - **#252** `console_charavail` drain loop spins forever on stdin EOF (`select`→readable, `read`→0), *inside a
>   device tick*, wedging the whole emulator (the audit's "L5 pty/forkpty hang"). `if (len < 1) break;`. Repro:
>   `gxemul -e 3max -d 1:disk bsd.pmax < /dev/null` froze at 0 bytes; post-fix boots to `root device?` like an
>   open-stdin control.
>
> **Triaged / DEFERRED / DO-NOT (documented — not applied):**
> - **L13 inetd UDP `dgram/wait` — NOT an emulator/device bug.** The userspace NAT (`net/net_ip.c` `net_ip_udp` /
>   `net_udp_rx_avail`) creates mappings only from guest-*outbound* traffic and has **no unsolicited-inbound path**;
>   an `inetd dgram wait` service waits on purely unsolicited inbound → never delivered (once `inetd`'s `select()`
>   is readable, the datagram is already in the guest socket buffer — nothing is lost in the fork+exec window). The
>   real axis is *solicited vs unsolicited*, not inetd-vs-standalone. Resolutions: tap networking
>   (`net/net_tap.c`, already implemented) or a one-datagram outbound "hole-punch" in the test — NOT a
>   `dev_le`/`dev_sn`/`net.c` change. True inbound port-forwarding = a new feature with new state/options, out of
>   the minimal-surgical ethos.
> - **L12 UART model — not a bug** (lossless; the ready-always TX status is a fidelity simplification, not a
>   data-loss source).
> - **`dev_jazz.c` R4030 `EXT_IMASK` IP3/4/6 namespace gating** — real interrupt-model issue in the *est/* copy
>   (ANDs CPU-IP funnel enables directly against Jazz device-line bits, arc-only). **SEC's `dev_jazz.c` already
>   carries the corrected split** (the SEC-only jazz boot-enablement layer the arc rig runs), and pmax has no
>   jazzio — so it affects neither rig and is not the L5 hang. Companion **OB-22** (`dev_jazz.c` vector-read
>   blanket deassert) stays deferred (self-healing; would touch the verified arc boot).
> - Minor `console/console.c` residual (not applied, low value): `d_avail()` retries *all* `select()` errors as if
>   `EINTR` (incl. `EBADF`); could tighten to `errno==EINTR` only. #252's `break` already resolves the reachable
>   (EOF) freeze.

> ## 2026-07-17 — Twenty-fifth round (#248, #250): debugger QoL for the audit (4-model panel)
> Scoped the author's `doc/TODO.html` for **debuggability** wins for the OpenBSD 2.2 pmax/arc audit. A **4-model
> panel** (Codex `gpt-5.6-sol` + agy Gemini + Ollama `gpt-oss:120b-cloud` + Kimi `kimi-k2.5`; Fable seat down on
> credits) reviewed the verified-undone candidates. **Applied (both trees, build 0/0, pmax+arc boot + live feature
> verification):** **#248** breakpoint hit-counts + "run N then break" (`breakpoint add addr[, N]`, counts on
> `show`/CTRL-T); **#250** data write-watchpoints (`watchpoint add addr[, len]` → break on guest store, report
> writer pc/value; physical-address match via `host_store` suppression + early `memory_rw` check). Both opt-in and
> guest-invisible (single `n!=0` early-out when unset). See CHANGELOG / REVIEW_FINDINGS "Twenty-fifth round".
> **Already implemented — candidate withdrawn (recon before coding):**
> - **C3 disk fsync-on-write toggle → the shipped `-f` option** (`main.c` `case 'f'`, opts string, `usage()`).
>   Its tentative number **#249 is VOID / unconsumed.**
> - The rest of the panel's "already-done" set: `find`, `put s/z`, `step call`, `verbosity`, subsystem/`debugmsg`
>   breakpoints, prefix-abbrev subcmds, `tlbdump`, CTRL-T-while-single-stepping (all the #120–#128 author-TODO round).
> **Assessed, DEFERRED / DO-NOT (documented — not applied):**
> - **CTRL-T in the main emul (run) loop — DEFER (unanimous):** async stdin polling under `-x` is historically
>   fiddly and risks console regression, for mostly-observational value; subsystem breakpoints + halt cover the need.
> - **PC / execution statistics (profil-style coverage) — DO-NOT (unanimous):** hot-path per-instruction counters
>   are a fuzzer feature, out of the accuracy-or-debuggability charter and against the minimal-changes ethos.
> - **Watchpoint limitations (documented, by design):** matches on physical addresses (so it needs the typed vaddr
>   to be translatable at add-time — trivial for kseg0/kseg1, needs a mapped TLB entry for kseg2/kuseg); write-only
>   (no read watchpoints); the shared expression parser doesn't accept bare register names (`r29`) — use literals.

> ## 2026-07-17 — Twenty-fourth round (#245–#246): debuggability logging + FPU denormal fidelity (5-model panel)
> A **5-model panel** (Codex `gpt-5.6-sol` + Fable + agy Gemini + Ollama `gpt-oss:120b-cloud` + Kimi `kimi-k2.5`)
> reviewed the round-23 Part-B suggestions. **Applied:** #245 (C5) route the rounds-18–23 guest-reachable
> fault-conversion diagnostics (`dev_asc`/`dec_prom`/`arcbios`, 8 sites) through the verbosity-gated
> `debugmsg`/`ENOUGH_VERBOSITY` channel (`VERBOSITY_DEBUG`) so a guest/fuzzer can't flood the host log; #246 (C3)
> FPU denormals → real Unimplemented-Operation trap (FCSR cause E + `EXCEPTION_FPE`, no result written), **gated to
> EXC4K+ (arc)** — EXC3K/pmax bit-identical. Build 0/0, pmax+arc boot (trap active on arc, no misfire). See
> CHANGELOG "Twenty-fourth round". **Assessed, intentionally left (not bugs to force):**
> - **C1 (R3000 IsC cache) — already correct:** GXemul allocates real per-cache buffers (`cpu_mips.c`
>   `cache[i] = malloc(...)`) + `memory_cache_R3000()` routes isolated data accesses to them. Faithful already.
> - **C2 (R4000 TLB-Shutdown on overlap) — DO-NOT:** no machine-check delivery (`EXCEPTION_MCHECK` never raised, no
>   `STATUS_TS`/DS state); R4000 multiple-match is architecturally undefined (reset-latched wedge, not an
>   exception); MIPS32 ExcCode 24 would be anachronistic + panic-prone on OpenBSD 2.2; upstream's own duplicate
>   detector is `#if 0`'d as unreliable; first-match is a valid concretization of UNDEFINED. **#247 unconsumed.**
> - **C4 (R3000 delayed-IE / IRQ-in-delay-slot) — already correct where it matters:** the delay-slot
>   `Cause.BD`+`EPC=branch` signature is textbook; only the 1–2-instruction IE cycle-timing hazard is unmodeled and
>   nothing depends on it (functional emulator, no cycle timing).
> - Residual (deferred, low value): FCSR *flag* bits still never set; CTC1-written cause bits don't trap
>   (pre-existing TODO); the optional C2 write-time overlap **debug warning** (resurrect the `#if 0` block at
>   `cpu_mips_coproc.c` as a `debugmsg` — tooling, not fidelity) was left unimplemented.

> ## 2026-07-16 — Twenty-third round (#234–#244): guest-reachable host-halt tail → hardware-plausible faults
> A **Fable (source-verified) + agy** panel took the remaining guest-reachable **host-halt** tail of the Codex
> round-19 backlog (~13 candidates). **10 DO-NOW** (all MIPS/pmax/arc audit path) converted to the correct fault
> or graceful return: #234 failed ifetch `goto bad`→`return` (cf. #210); #235 `break 0x30378` reboot sentinel gated
> to the reset stub (phys `0x1fc00000`), else real BP; #236 reserved COP0 fn→RI; #237 COP0 STANDBY/SUSPEND/HIBERNATE
> → R4100 idle / else RI (was HIBERNATE `goto bad`, SUSPEND reboot-at-any-PC); #238 `memory_mips_v2p` supervisor/
> reserved KSU→TLB walk not `exit(1)`; #239 R3000 `tlbw*` under IsC→`return`; #240 `dev_asc` unimplemented cmd→
> deliver the ILL IRQ, no exit; #241 `dec_prom` unsupported services→`V0=-1`+return; #242 `arcbios` non-SGI private
> call / `0x888` / unimplemented vector→`V0=ARCBIOS_EINVAL`+return; #243 `diskimage_scsicmd` `malloc(0)`→`malloc(1)`;
> #244 `memory_rw` zero-fill the read buffer on a failed/`NO_EXCEPTIONS` translation (whole class; DEC-PROM uninit
> buf). Build 0/0, pmax+arc boot. See CHANGELOG "Twenty-third round". **Clears ~10 of the ~15 remaining Codex
> round-19 items; ~5 remain for #245+** (all off the MIPS audit path or verified unreachable there):
> **DEFERRED / NOT reachable on pmax/arc (documented — not bugs to force):**
> - **#10 PPC/ARM slow-path ifetch `exit`** (`cpu_ppc_instr.c` ifetch fail; `cpu_arm.c` `running=0`) — direct analog
>   of #234 but off the MIPS audit path; the PPC data side is already fixed (#216). Fix = `return`/RI when promoted.
> - **#11 PPC `MSR.IP` reboot hack** (`cpu_ppc.c`) and **#12 m88k CMMU / `dev_mb89352`** fatal errors — off-path.
> - **SPECIAL3 `RDHWR` selector halt + `HWREna` gate** (`cpu_mips_instr.c`): Fable verified SPECIAL3 is ISA-gated to
>   RI on R3000/R4000, so the halt is **unreachable** on pmax/arc (MIPS32r2-only). Cheap hardening for a future
>   round; no audit-path exposure.

> ## 2026-07-16 — Twenty-second round (#230–#233): MIPS fault-signature fidelity (FULL 4-model panel)
> A **full 4-model panel** — Codex `gpt-5.6-sol` + agy `Gemini` + Ollama (`gpt-oss:20b`; the `480b-cloud` model
> returned HTTP 410) + Fable — fixed 4 fidelity items and DEFERRED 2. **FIXED:** #230 R3000 RFE KUo/IEo preserve
> (`~0x0f`); #231 ERET-on-R3000 → RI (decode-gate); #232 J/JAL region from the delay-slot PC `(branch+4)[31:28]`;
> #233 `mtc0`/`dmtc0` `cop0_availability_check` (writes only). Build 0/0, pmax+arc boot. See CHANGELOG
> "Twenty-second round". Clears 4 of the ~19 remaining Codex round-19 items; ~15 remain for #234+.
> **DEFERRED by the panel (documented — NOT bugs to force):**
> - **Privilege-transition fast-map bleed (Codex #17):** the dyntrans fast host-page map is not privilege-tagged,
>   so a kseg mapping cached in kernel mode can be hit by a later user access, bypassing AdEL/AdES (the slow
>   `memory_mips_v2p` path raises it correctly). The proposed invalidate-all-on-RFE/Status-write fix is a
>   non-starter — R3000 RFE fires on every syscall/interrupt/TLB-miss return, so a full invalidate there causes
>   continuous re-translation and would **hang the boot**; a Status-write-only hook misses R3000 RFE entirely
>   (RFE rotates Status directly in `X(rfe)`); the only correct+cheap fix is privilege-tagging the fast map = a
>   structural refactor the ethos forbids. agy+Fable ruled DEFER; Codex+Ollama conceded HIGH risk. Documented as
>   a known fast-map-vs-slow-path privilege-boundary fidelity limitation for the audit.
> - **#233 remainder:** the mfc0/dmfc0 READ-side availability check (side-effect-free fast paths), the
>   `rt==$zero`→nop fold, and the EXC3K user-mode-from-PC heuristic (in-code comment: forcing KUc "crashes
>   Linux") — invasive/risky for marginal exploit value; deferred.

> ## 2026-07-16 — Twenty-first round (#227–#229): fault-signature fidelity trio (multi-model panel, unanimous 3-0)
> A **multi-model advisory panel** — Codex `gpt-5.6-sol` + agy `Gemini` + Fable (Ollama not installed on host) —
> unanimously (3-0) FIXED the three fault-signature-fidelity items promoted from the Codex round-19 backlog:
> **#227** `SWL/SWR` store pre-read mislabeled every fault as TLBS → map only load→store codes (TLBL→TLBS,
> AdEL→AdES; DBE/Mod correctly left alone); **#228** misaligned `jr`/`jalr` silently rounded down → raise AdEL
> (BadVAddr=EPC=rs, BD=0) in all 6 register-jump handlers; **#229** `mtc0 $8` `BadVAddr` → read-only. Build 0/0,
> pmax+arc boot. The panel resolved the earlier BadVAddr disagreement (Codex "fix" vs a prior Fable
> "Irix-compat/document-only") **3-0 to fix**, after Codex extracted the OpenBSD 2.2 kernel source and confirmed
> pmax/arc only `mfc0`-read CP0 $8 → no boot regression. See CHANGELOG "Twenty-first round".
> This clears **3 of the ~22 Codex round-19 backlog items**; ~19 remain for #230+ — the rest of the
> fault-signature fidelity set (`J/JAL` region from page-base not PC+4; R3000 `RFE` Status bits; `ERET`-on-R3000
> → RI; CP0 availability check; privilege-transition fast-map bleed) plus the guest-reachable host-halt tail
> (`goto bad`, `malloc(0)`, PPC/Thumb/m88k slow-path, dec_prom/arcbios unsupported-service, DEC-PROM uninit buf).

> ## 2026-07-16 — Twentieth round (#224–#226) + Codex round-19 backlog recorded
> Applied **3 HIGH MIPS-FPU memory-safety fixes** to both trees (build 0/0, pmax boots): #224 `ldc1`/`sdc1`
> `ft=31` → `reg[32]` OOB into `tlbs`; #225 `ldc1` uninitialised-`fpr` leak on a faulting load; #226 coproc
> paired-store `fd+1` sign-extension OOB. See CHANGELOG "Twentieth round".
> **Codex round-19 backlog — 22 items NOT yet applied (future rounds; full text saved in the session scratchpad
> `codex_round19.txt`, 2026-07-16):**
> - **HIGH (done this round):** Codex #23→#225, #24→#224, #25→#226.
> - **Fault-signature fidelity (recommended next — directly affects controlled-PC / BADVADDR trust):** misaligned
>   `JR/JALR` silently rounded down (should raise instruction-fetch AdEL with BadVAddr); `SWL/SWR` pre-read
>   rewrites every fault as TLBS (should preserve AdES/DBE); `mtc0`-writable `BadVAddr` (Codex: fix for
>   fault-signature auditing — Fable-B had called it Irix-compat/document-only, so reconcile); `J/JAL` region from
>   translated page base not `PC+4`; R3000 BEV=1 vector base `0xbfc00200` vs `0xbfc00100`; R3000 `RFE` Status bits;
>   `ERET` accepted on R3000 (should RI); CP0 availability check omitted; privilege-transition fast-map bleed
>   (stale kseg mapping bypasses AdEL/AdES after kernel→user).
> - **More guest-reachable host-halts:** `cpu_mips_instr` `goto bad`/BREAK-reboot-sentinel/RDHWR/SUSPEND;
>   `memory_mips_v2p` KSU=supervisor `exit(1)`; TLBWI/TLBWR under Status.IsC; `dev_asc` unsupported-command exit;
>   `dec_prom`/`arcbios` unsupported-firmware-service halts; `diskimage_scsicmd` `malloc(0)`→NULL→exit; PPC/Thumb
>   slow-path; PPC `MSR.IP` reboot hack; m88k CMMU / `dev_mb89352` protocol errors.
> - **Category 3:** `dec_prom` uninitialised `ch`/`buf` on a failed `NO_EXCEPTIONS` translation (silent
>   nondeterminism / unbounded string scan).

> ## 2026-07-16 — Nineteenth round (#210–#223): MIPS exception fidelity/debuggability + host-halt sweep
> Codex `gpt-5.6-sol`/ultra + a 2-agent Fable panel + per-site verification applied **14 corrections #210–#223**
> to both trees (build **0/0**, all tags matched, **pmax boot regression PASS**) — see CHANGELOG /
> REVIEW_FINDINGS "Nineteenth round". Highlights: #210 wire MIPS exceptions to the trappable `SUBSYS_EXCEPTION`
> breakpoint (catches controlled-PC-into-unmapped that `-p` can't reach); #211 AdEL/AdES no longer clobber
> Context/EntryHi (BadVAddr only, like silicon); #212 unaligned LL/SC → AdEL/AdES; #213/#214 CONFIG/ENTRYLO1;
> #215–#217 Alpha/PPC/SH host-crashes → guest faults; #218–#223 OF + footbridge/mp/kn02ba/8253 guest-reachable
> `exit(1)`s → graceful.
> **New deferred (broad device-exit tail):** the same untagged `fatal("…TODO/unimplemented…"); exit(1)` inside
> many other guest-writable `DEVICE_ACCESS` handlers persists (Fable-A's list: `dev_adb.c`, `dev_clmpcc.c`,
> `dev_igsfb.c`, `dev_lca.c`, `dev_m8820x.c`, the `dev_pcc2.c` remainder, `dev_mb8696x.c`, `dev_mvme187.c`,
> dreamcast gdrom/maple/g2, and `cpu_arm_coproc.c` CP15 writes 165/252/407/518). Each is guest-reachable when its
> machine is selected; extending the #118/#119 warn-once-and-continue pattern would close them — a future round.
> **Document-only (assessed, not bugs):** R3000 BEV=1 bootstrap-vector base (`0xbfc00200` vs `0xbfc00100`; off the
> exploit window — OpenBSD clears BEV early); `mtc0`-writable `BADVADDR` (Irix compat); the SH `sh_exception()`
> default and the dyntrans `bad:` halt (both already emit a trappable SUBSYS message — an intentional
> "unimplemented" signal the maintainers want surfaced).

> ## 2026-07-16 — Eighteenth round (#188–#208): accuracy/debuggability pass (Codex 5.6-Sol-Ultra + Fable panel)
> A fresh full-tree Codex `gpt-5.6-sol`/ultra review (17 findings) + a 4-reviewer Fable panel + per-site
> verification, narrowed to **hardware-accuracy + debuggability + ethos** (not new hardening for its own sake),
> applied **21 corrections #188–#208** to both `est/` and `GXEMUL-SEC/` (build **0/0**, all 21 tags matched) —
> see CHANGELOG / REVIEW_FINDINGS "Eighteenth round". This **clears one deferred item below: the `dev_ram.c`
> MAP_FAILED-vs-NULL #175 straggler → now fixed as #208.** Highlights: R4000 invalid-PageMask host-`exit()`
> (#188 write-canonicalize / #189 translate-refill), `TLBWR` divide-by-zero (#190), DEC/ARC PROM `malloc` DoS
> (#191/#192), ARM/Alpha/m88k page-walk & signed-div host-crashes → guest faults (#193–#195), and Codex HIGH
> guest→host OOBs (#202 SII, #203 MEC, #204 flat-CD, #205 MODE SELECT, #207 PX copyspans).
> **Still deferred (unchanged):** #185 ASC DATA_OUT `exit(1)`; the four PVR render/texture-loop `exit(1)`s
> (868/1084/1245/1419); CUE symlink-follow; cross-memblock invalidation gap (#165); overlay write
> silent-success; Jazz `LB_IE` / dual-pending IRQ; ARC partition signed-`*512`; TCP-debug over-read; NE2000 TX
> log-flood.
> **New "not changed" (documented):** the MIPS `add/addi/sub` Integer-Overflow *trap* (`cpu_mips_instr.c`) —
> defined 2's-complement wrap in practice; a real trap is the hottest instruction path + boot-regression risk,
> so left per OB-24.

> ## 2026-07-10 — Cross-model re-review (Codex 5.6-Sol-Ultra + Fable panel): #182–#187 applied; deferred candidates
> A full-tree adversarial re-review (Codex `gpt-5.6-sol`/ultra, 17 findings, + a 4-reviewer Fable panel, each
> source-verified) fixed a **CRITICAL fb-resize stale-length OOB (#182)**, a HIGH X11 alloc overflow (#183), and the
> clean part of the guest-`exit(1)` cluster (#184 dev_fb, #186 mb89352, #187 eight dev_pvr MMIO sites) — see
> CHANGELOG / REVIEW_FINDINGS "Seventeenth round". Build 0/0 (gcc 15.2.1); applied to both `est/` and `GXEMUL-SEC/`.
> **Deferred candidates (recorded for a follow-up fix pass; not yet applied):**
> - **#185 `devices/dev_asc.c` DATA_OUT `data_out_len==0` `exit(1)` (med DoS):** reachable via `NCRCMD_TRPAD|DMA`
>   before a SELECT (TRPAD allocates `xferp`, so the #167 null-guard passes, then the DATA_OUT phase has len 0).
>   The fix needs a structural transfer-skip (wrap the ~40-line copy in `if (len != 0)`), so it is held for its own pass.
> - **`devices/dev_pvr.c` render/texture-loop `exit(1)`s (med DoS): lines 868 (texture pixelformat), 1084 (non-RGB565
>   render cfg), 1245, 1419 (unimplemented TA list-cmd).** Reachable via STARTRENDER; converting these safely needs
>   flood-free per-iteration recovery, unlike the simple MMIO-write fall-through used for #187.
> - **CUE symlink/junction bypass of #158 (`disk/diskimage.c`, med, host-side threat):** the #158 guard rejects only
>   *lexical* `..`/absolute paths; `fopen()` still follows a symlink/junction inside an attacker-supplied CUE bundle.
>   Needs an attacker-supplied disk image (host-side), not a malicious guest — lower priority under the guest→host charter.
> - **Cross-memblock dyntrans invalidation gap in #165 (`cpus/memory_rw.c`, med):** a bulk RAM write spanning a
>   memblock boundary invalidates only the endpoint pages, so translated code in interior pages can go stale.
> - **Lower-severity Codex findings:** overlay write rejected-but-reported-GOOD (`diskimage.c`, silent data loss);
>   Jazz `LB_IE` not implemented + dual-pending-IRQ loss (`dev_jazz.c`); ARC partition LBA signed-`int *512` overflow
>   (`arcbios.c`, defeats the #168 bound); TCP-debug options over-read (`net_ip.c`, debug-verbosity only); NE2000
>   invalid-TX log-flood (`dev_ne2000.c`, SEC-only); one `dev_ram.c` `MAP_FAILED`-vs-NULL check (#175 straggler).

> ## ✅ 2026-06-28 — OB-35 RESOLVED (correction #117; build 0/0, Codex+agy APPROVE FOR COMMIT, regression-clean)
> Added a **7445/7455 CPU model** as a NEW, purely-additive macppc subtype **`-e g4plus`** (→ MPC7455, PVR
> 0x80010000) so the existing `-e g4` (MPC7400) and g3/g5 are unchanged and OpenBSD 3.4/macppc stays
> regression-safe. **Verified:** on `-e g4plus`, NetBSD 8.2/macppc sets HID0[HIGH_BAT_EN] → #116's extended
> BATs **engage** (gate-opened=1, confirmed via a temporary ppc_bat debug) → it advances past the BAT/MMU
> layer; on `-e g4` the gate stays closed. Files: `cpu_ppc.h` (cpu_type row), `machine.h`
> (MACHINE_MACPPC_G4PLUS=4), `machine_macppc.c` (CPU map + subtype). See CHANGELOG/REVIEW_FINDINGS
> "Eleventh round".
> - **Known residual (NOT a safety bug, pre-existing): macppc OpenFirmware is skeletal.** Past the MMU,
>   NetBSD 8.2/macppc stalls in GXemul's incomplete OpenFirmware (`machine_macppc.c` skeletal model + `of.c`
>   device-tree `getprop` gaps). Reaching a full NetBSD-8.2/macppc multiuser boot is open-ended OF/device
>   work beyond OB-35's CPU-model scope — left as a future enhancement, not tracked as an OOB/safety OB.


> ## ✅ 2026-06-28 — OB-27..34 RESOLVED (corrections #106–#113; build 0/0, pmax+arc regression-clean)
> All 8 deferred Phase-B/C candidates were Claude-verified (**all confirmed real**) and fixed — see
> CHANGELOG / REVIEW_FINDINGS "Eighth round". Map: OB-27→#106 (dev_fb from_x), OB-28→#108 (ps2_gif),
> OB-29→#107 (pvr span), OB-30→#109 + OB-31→#110 (iso9660), OB-32→#111 (bootblock n_blocks), OB-33→#112
> (diskimage %s), OB-34→#113 (SCSI CDB-length).
> ~~Still open: OB-25 / OB-26~~ → **now also RESOLVED: OB-25→#115 (mymkstemp unpredictable overlay temp
> names), OB-26→#114 (osiop skip data phase instead of exit(1)) — see "Ninth round". ALL OB-1..34 are now
> resolved.**

> ## 2026-06-28 — Phase-C deeper audit (3-agent fan-out): #101–#105 applied; 1 new candidate
> Agents swept network/NAT, SCSI/ATA storage, and the remaining devices + dyntrans. Claude verified +
> fixed 5 bugs (#101–#105, incl. 2 CRITICAL: dev_scc OOB heap write + net_arp heap overflow — see
> CHANGELOG / REVIEW_FINDINGS "Seventh round"). One candidate deferred:
> - **OB-34 `disk/diskimage_scsicmd.c` short-CDB over-read (med):** `diskimage_scsicommand()` only checks
>   `cmd_len >= 1`, then every opcode reads fixed CDB offsets (up to `cmd[8]`) — so a guest that submits a
>   short CDB (the SCSI/ATA controllers allocate `cmd[]` to the guest's byte count) causes an OOB read of
>   the host `cmd` buffer, influencing the computed LBA/transfer length. Fix with a per-opcode CDB-length
>   table (6/10/12/16) validated before the reads, under its own regression (touches every controller).

> ## 2026-06-28 — Phase-B new-surface audit (3-agent fan-out): #96–#100 applied; 7 new candidates
> Agents swept the PROMs (all CLEAN), the framebuffer renderers, and the disk parsers; Claude verified +
> fixed 5 bugs (#96–#100, incl. a CRITICAL ps2_gs OOB heap write and a HIGH Apple-partition stack
> over-read — see CHANGELOG / REVIEW_FINDINGS "Sixth round"). These further agent-found candidates are
> **not yet exact-fix-verified by Claude** (record for a follow-up fix pass):
> - **OB-27 `devices/dev_fb.c` `framebuffer_blockcopyfill` (high):** in copy mode the source column
>   `from_x` is not clipped (dst `x1/x2` and `from_y` are), so the `memmove` source over-reads the host
>   framebuffer; reachable from dev_ps2_gif blockcopy and dev_igsfb scroll → host-heap info leak.
> - **OB-28 `devices/dev_ps2_gif.c` TA-putchar (high):** pixel source offset `(24 + y*xsize)*4` uses
>   guest `xsize`/`ysize` (≤65535) with no check against the input `len` → large OOB read of the host DMA
>   buffer (also an `int addr` overflow).
> - **OB-29 `devices/dev_pvr.c:2438` (med):** the 24-bit `pvr_fb_tick` copy wraps only the start
>   `vram_ofs % VRAM_SIZE`, not the span → reads past the 8 MB VRAM; also signed `vram_ofs` can go
>   negative. Other pixelmodes wrap each access.
> - **OB-30 `disk/bootblock_iso9660.c:188` (med):** the root-directory walk reads the 8-byte record
>   header + up to 64 name bytes past `dirbuf` (guard only checks `dp < dirbuf+dirlen` at the top).
> - **OB-31 `disk/bootblock_iso9660.c:308` (med):** `if (i < len - strlen(filename))` underflows
>   `size_t` when `strlen(filename) > len`, defeating the bound → over-read.
> - **OB-32 `disk/bootblock.c` (low):** the bootblock/OSLoader size "WARNING" checks call `fatal()`,
>   which does NOT exit (debugmsg.c:334), so a disk-controlled `n_blocks*512` proceeds with int-overflow
>   UB → `malloc` abort (DoS). Make the checks `return`; use size_t math + an upper bound.
> - **OB-33 `disk/diskimage.c:321` (low):** `fatal("… type %i …", id, diskimage_types[type])` passes a
>   `char *` to `%i` (UB on the not-found path); use `%s`.

> ## 2026-06-28 — multi-model review (Codex + agy + Claude): #89–#94 applied; 2 new candidates
> A three-engine review (Codex `gpt-5.5`/xhigh, agy `Gemini 3.1 Pro`/High, Claude verification + a
> consensus rebuttal loop) of the full hardening diff fixed **6 confirmed bugs (#89–#94** — see
> `CHANGELOG.md` / `REVIEW_FINDINGS.md` "Fifth round") and **rejected 3 false positives** (both models
> conceded). **2 lower-severity items remain open:**
> - **OB-25 `disk/diskimage.c` temp-file TOCTOU (low, local-only).** #7/#20 create the overlay temp
>   files with `fopen "wx"` but then close and **reopen them by name** in `diskimage_add_overlay()`,
>   leaving a swap/symlink race window. Fix: `mkstemp()` + pass the fd; never reopen by name.
> - **OB-26 `devices/dev_osiop.c` guest-reachable `exit(1)` (low DoS).** The #10 NULL-`xferp` guard
>   calls `exit(1)` on a state a guest can drive (SCSI data phase, no active transfer) → a guest can
>   halt the emulator. Prefer aborting the phase (`break`) over killing the process. (Replaced a worse
>   null-deref, so not a regression — a hardening-quality improvement.)

> ## ✅ RESOLVED 2026-06-27 — see CHANGELOG.md "#70–#88"
> All 24 candidates below were triaged (Codex `gpt-5.5` *xhigh* proposals + independent source audit):
> - **19 fixed → corrections #70–#88** (builds 0/0; pmax + arc rigs re-verified):
>   OB-1 #70 · OB-2 #71 · OB-3 #72 · OB-6 #73 · OB-7 #74 · OB-8 #75 · OB-9 #76 · OB-11 #77 ·
>   OB-12 #78 · OB-13 #79 · OB-14 #80 · OB-15 #81 · OB-16 #82 · OB-17 #83 · OB-18 #84 · OB-19 #85 ·
>   OB-20 #86 · OB-21 #87 · OB-23 #88.
> - **3 false positives (not real)** — OB-4, OB-5, OB-10: `cpus/memory_rw.c:288` clamps `len` to the
>   device length before the handler runs, and these three are registered with length == backing size
>   and have no direct callers, so the "end-span" is unreachable.
> - **1 deferred** — OB-22 (jazz jazzio vector-ack): emulation correctness, not host-OOB;
>   medium-confidence; in the #69 arc interrupt path — deferred to avoid regressing the verified arc boot.
> - **1 skipped** — OB-24 (signed `byte<<24` in CPU instruction cores): UBSan-only, hottest path, no
>   exploit path; consistent with the pre-existing "intentionally left" decision (shared decoder fixed in #27).
>
> The per-finding analysis below is retained as the audit record.

---

Consolidated from two **read-only** Codex reviews (model `gpt-5.5`, effort `high` + `xhigh`)
on 2026-06-27, plus the manual audit. These are **static-analysis findings** — bounds/overflow
reasoning from reading the source; most are **not yet runtime-confirmed** (several need a specific
guest/board, e.g. Dreamcast, SGI, TURBOchannel framebuffers). They are candidates for the next
correction set (#70+). The 69 already-applied corrections are in `REVIEW_FINDINGS.md` / `CHANGELOG.md`
and are **not** repeated here. `src/` (pristine baseline) is untouched.

**Threat model:** the emulator runs untrusted guest OS images (device MMIO/DMA) and loads untrusted
executable files (loaders). HIGH = a malicious guest or input file can cause a guest→**host**
memory-safety violation (OOB read/write of host memory). MED/LOW = host DoS / UB / device-state
corruption without a clear host-OOB path.

**Two dominant root patterns** (almost every HIGH below is one of these):
1. **End-span not checked.** An MMIO handler validates the *start* (`addr < size`) but then
   `memcpy`/indexes `len` bytes, so a 2/4/8-byte access at the last valid offset crosses the host
   buffer. Fix shape: require `addr + len <= size` (or clamp `len`).
2. **MMIO window larger than its backing array.** The registered device length exceeds the
   allocation, so high offsets index past it. Fix shape: bound the offset to the real backing size.

---

> ## STATUS OF THIS SECTION, re-verified against the source 2026-08-01
>
> **The tables below are the ORIGINAL audit listing and are largely historical.** Nineteen
> of the twenty-four entries have since been corrected and carry an `OB-N` marker comment
> at the fixed site: OB-1, 2, 3, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21 and
> 23. Treat a row below as closed unless it is named here.
>
> **OB-4, OB-5 and OB-10 are NOT DEFECTS — closed by round 84 after a full review, no
> source changed.** All three copy `len` bytes at `buffer + relative_addr` with no end
> check *in the handler*, which is why the original audit flagged them; but
> `memory_rw.c` clamps `len` to the device length before dispatching to any handler, so
> `relative_addr + len <= length` is guaranteed on entry. Adding the checks would have
> been three tests that can never fire — and worse than inert, since a handler returning
> 0 raises a guest bus error rather than doing nothing.
>
> **The rule, now stated so this does not get re-filed:** a handler reachable only
> through the memory layer relies on that central clamp. A handler that another handler
> calls DIRECTLY bypasses it and needs its own bound — which is exactly why OB-1
> (`dev_fb_access`, called straight from `dev_dec21030.c` and `dev_sgi_mardigras.c`) was
> a real defect and carries its own overflow-safe check. The three above are registered
> and never called directly; that was checked, not assumed.
>
> **A different shape the clamp does NOT cover:** "window larger than backing" (OB-2,
> OB-12, OB-15). The clamp bounds against the REGISTERED LENGTH, not the allocation, so
> a device registering a window bigger than its buffer satisfies the clamp and overruns
> anyway. Those three carry fix markers and are believed done — but that is the shape
> that genuinely needs a per-device check.
> - **OB-22** — left as recorded: self-healing, correctness-only.
> - **OB-24** — the residual signed `byte<<24` UB; real C UB that never reaches a host
>   pointer, size or index. Deliberately not chased (see the "Not changed" note).
>
> Two rows were checked by hand during that pass and are worth recording because the first
> reading of each was wrong: **OB-6** is fixed, and **OB-7** is fixed at the index-WRITE
> site (`idata & 0xff`), not at the data-write site where the indexing itself looks
> unguarded. Reading only the second site suggests a defect that is not there.

## High — guest → host OOB read/write

| ID | Site | Pattern | Trigger / impact |
|----|------|---------|------------------|
| OB-1 | `devices/dev_fb.c:646` (+ callers `dev_dec21030.c:135`, `dev_sgi_mardigras.c:200`) | end-span | `dev_fb_access()` checks `relative_addr >= framebuffer_size` only, then `memcpy(framebuffer+addr,…,len)` — wide access at last pixel → host fb heap OOB R/W |
| OB-2 | `devices/dev_px.c:608` | window>backing | PX SRAM MMIO window is 512 KB (`0x200000..0x27ffff`) but `sram[]` is 128 KB; offsets >`0x21ffff` corrupt host heap — any PX/PXG TURBOchannel guest |
| OB-3 | `devices/dev_px.c:315` (+`:414`,`:531`) | unchecked rows | PX STAMP DMA copyspans/fill/putchar use guest `span_src/span_dst` rows in fb pointer math with only `span_len` capped → fb heap OOB R/W |
| OB-4 | `devices/dev_pvr.c:2551` / `:2567` | end-span | `dev_pvr_vram_access()` copies to/from `vram+relative_addr` without `addr+len <= VRAM_SIZE` (distinct from the fixed #65/#68 render/texture paths) |
| OB-5 | `devices/dev_asc.c:778` / `:794` | end-span | ASC 128 KB DMA window: raw `memcpy(dma+addr,…,len)` with no end check |
| OB-6 | `devices/dev_adb.c:300` / `:305` | unbounded append | `output_buf[MAX_BUF=100]` appended via `output_buf[cur_output_offset++]=c` with no cap; guest toggles ACK in output mode → heap OOB write past `struct adb_data` |
| OB-7 | `devices/dev_igsfb.c:183` | unbounded index | DAC `palette_write_index` unclamped; `rgb_palette[index*3+sub]` past the 256-entry palette (start at 255) |
| OB-8 | `devices/dev_kn01.c:171` | unbounded index | KN01 VDAC overlay palette has 16 entries but `cur_write_addr_overlay` is raw guest data → `rgb_palette_overlay+3*addr` OOB |
| OB-9 | `devices/dev_sgi_mardigras.c:220` / `:224` | end-span | microcode-RAM MMIO validates `< MICROCODE_END` only, copies `len` → OOB past `microcode_ram` |
| OB-10 | `devices/dev_ether.c:82` / `:89` | end-span | test-ethernet `buf` MMIO copies to/from `buf+addr` with no end check |
| OB-11 | `devices/dev_pcc2.c:327` (+`:372`) | end-span | `relative_addr %= PCC2_SIZE` folds the *start* only; wide access near end of the 0x40-byte `pcctwo_reg[]` spans past it |
| OB-12 | `devices/dev_pmagja.c:111` | window>backing | PMAG-JA treats all `>=0x200000` as 8-bit pixels up to `0x3c0000`, but `pixeldata` is only 1280×1024 → OOB (and drives `dev_fb_access` out of range) |
| OB-13 | `devices/dev_sgi_gbe.c:706` | unmasked index | GBE palette store `selected_palette[color_index]` instead of `[color_index & 0xff]`; cmap 1..31 writes far past the 256-entry cache |
| OB-14 | `devices/dev_sgi_gbe.c:274` | stack over-read | tile convert: `fb_buf` sized for 512 px but guest partial-tile fields make `fb_len` up to 992 px → `dev_fb_access` copies past `fb_buf` (stack-byte leak into emulated fb) |
| OB-15 | `devices/dev_vga.c:607` | window>backing | VGA gfx window is fixed `0x18000` but `gfx_mem_size` is realloc'd per mode (e.g. 64,000 for mode 0x13) → access in-window but past `gfx_mem` → heap OOB |
| OB-16 | `devices/dev_vga.c:412` | unchecked index | VGA CRTC guest-programmed `base` (start hi/lo) added to every visible charcell index without `base+end` check → charcell heap OOB read on redraw |

## Medium — host DoS / overflow / device-state corruption

| ID | Site | Issue |
|----|------|-------|
| OB-17 | `devices/dev_dec21143.c:763` | TX descriptor chain: many non-`LS` descriptors → repeated `realloc(cur_tx_buf_len+bufsize)` (unbounded host alloc); `int cur_tx_buf_len` can wrap → alloc/copy size bug |
| OB-18 | `file/file_android.c:103` / `:146` / `:186` | file-controlled `page_size`: `==0` → divide-by-zero; very large → 32-bit page/seek overflow → crash/misload |
| OB-19 | `file/file_elf.c:94` (loop `:450`–`:482`) | PT_LOAD copy cursor `ofs` is `int` vs file-controlled `p_filesz` → signed overflow/UB on huge segments (chunk buffer itself is bounded) |
| OB-20 | `devices/dev_dreamcast_gdrom.c:183` (`:90`) | `READ_SECTORS` with `cnt==0` derives `cnt = 2048*sector_count` from guest bytes, then allocates it → guest-triggered host OOM/hard-exit |
| OB-21 | `devices/dev_dreamcast_g2.c:94` | EXTDMA maps `0x100` but `extdma_reg[]` is 0x80; offsets `0x90..0xbc` index `extdma_reg[>=36]` → C subobject OOB into adjacent `misc_reg` (device-state corruption) |
| OB-22 | `devices/dev_jazz.c:613` (`jazz_jazzio`) | **pre-existing, correctness only** (NOT a #69 regression): after reporting a vector it deasserts `mips_irq_3` without clearing `int_asserted` → possible stuck/missed non-timer JAZZ IRQs until next edge/mask write |

## Low / reviewed

| ID | Site | Note |
|----|------|------|
| OB-23 | `devices/dev_sgi_re.c:1127` | MTE fill subtracts `sizeof(zerobuf)` from `dstlen` while writing only `fill_len` → mis-accounting → guest hang / wrong emulated writes (no host OOB observed) |
| OB-24 | `cpus/*` (e.g. `cpu_arm_instr_loadstore.c:297`; ARM/MIPS/PPC/m88k/PROM) | residual signed `byte<<24` UB; real C UB but does not feed host pointers/sizes/indices — sanitizer/portability cleanup, no exploit path found |

## Confirmed clean
- **#69 (arc Jazz interrupt-enable mask)** — both review passes independently found **no regression**:
  assert/deassert gate on `int_asserted & int_enable_mask`, `EXT_IMASK` recomputes IRQ3/6 on mask
  change, and masked pendings stay in `int_asserted` (delivered when later enabled).

## Suggested remediation order
1. **Window>backing (OB-2, OB-12, OB-15):** straight host-heap corruption from any access in-window;
   bound the offset to the real allocation size. Highest priority.
2. **End-span family (OB-1, OB-4, OB-5, OB-9, OB-10, OB-11):** add `addr+len <= size`; many share the
   `dev_fb_access` helper (fix once in OB-1 covers OB-1's direct callers).
3. **Unbounded index/append (OB-6, OB-7, OB-8, OB-13, OB-14, OB-16, OB-3):** clamp/mask the
   guest-controlled index; size the temp buffer to the max (OB-14).
4. **Loader/alloc (OB-17..OB-21):** reject `page_size==0`, cap aggregate/realloc sizes, widen `int`
   cursors to `off_t`/`size_t`, validate `cnt`.

> Generated read-only; no source was modified. Raw review transcripts:
> session scratchpad `codex_review.txt` (high) and `codex_review_xhigh.txt` (xhigh).
>
> **That last sentence is true only of the ORIGINAL audit pass.** Nineteen of these have
> been corrected in the source since, and the remediation order above is therefore stale as
> a work list — see the status block at the head of this section for what is actually left
> (OB-4, OB-10, and OB-5 pending re-location). Round 84 carries them.

> ## 2026-08-02 — round 85 (#57) partial: `fsrra`'s store settled, the rest still open
> **#339** records why `X(fsrra_frn)` uses the LEGACY store while its neighbours use the
> mode-aware one: FSRRA is an approximation instruction, specified only to a relative error
> bound, so there is no rounding mode for it to honour. That is now a comment in the source
> instead of a recurring re-file. **Everything else in round 85 remains open** — the
> unimplemented legal encodings, the missing SH FPU exception model (which #334 also
> depends on: DN=0 should raise an FPU error rather than deliver a value), and `fsca`'s
> store. None of those is a comment-sized change.

> ## 2026-08-03 — the free-running witness IS buildable; recipe recorded
> Round 83 was blocked because `cpu_dyntrans.c:1888` disables instruction combining under
> single-step and every probe in `regress/` drives the guest with `step`. Checked whether a
> breakpoint-and-continue harness can work instead. **It can**, and the one thing that
> looked fatal is not:
> - `single_step_breakpoint` appears in the SAME guard, but it is **transient, not a mode**:
>   set only when the PC equals a breakpoint address (`:1802-1823`) and cleared at `:1930`
>   after that one instruction executes and is marked for re-translation. It suppresses
>   combining for the instruction **at** the breakpoint, not globally.
> - `allow_instruction_combinations` already defaults to 1 (`machine.c:86`) and is a
>   registered runtime setting (`machine.c:109`). Nothing to turn on.
> - `breakpoint` and `continue` both exist (`debugger_cmds.c:2022`, `:2028`).
>
> **Recipe.** Put the breakpoint on an instruction AFTER the sequence under test, never on
> the sequence. Keep the pair in straight-line code within one page so the combiner sees
> `ic[-1]` at translation time. Drive with `continue`. **Do not enable instruction tracing**
> — `!cpu->machine->instruction_trace` is in the same guard, so a probe that switches on
> tracing to observe what happened disables the thing it is measuring. That is the identical
> failure mode as the five `step`-driven rows that passed green while measuring the
> standalone path; it is written down here rather than rediscovered.
>
> This unblocks round 83 (#55) and is the likely route for round 82's user-mode SH witness
> (#54) as well, since that one also needs real execution rather than stepped instructions.
> It also closes the wider hole: the whole combined-handler family (`cmps_*`, `teqs_*`,
> `tsts_*`, `netbsd_*`, `strlen`, `xchg`) is ungated today for exactly this reason.

> ### RESOLVED as #340 (round 83): the witness was built and the defect measured
> The two corrections below were both right, and together they made the witness buildable.
> See the round-83 block in CHANGELOG.md. Original notes kept:
>
> ### Correction: breakpoint-and-continue is NECESSARY but NOT SUFFICIENT
> Built the free-running driver described above and measured with it. The combined rows
> **still** read the standalone answer. The recipe was incomplete, and the missing piece is
> not about how execution is driven at all:
>
> `arm_combine_instructions` rewrites **`ic[-1].f`** — the PREVIOUS instruction — while the
> BRANCH is being translated. In straight-line code the `teq` has already executed by then.
> So the combined handler is reached only on a **second pass** over the same code; a single
> forward run cannot reach it no matter whether it is stepped, continued, or breakpointed.
>
> A working witness therefore needs the sequence inside a **loop** executed at least twice,
> publishing flags on the second iteration — with the breakpoint after the loop, still not
> on the pair, and tracing still off. The two facts recorded above (that
> `single_step_breakpoint` is transient and that `allow_instruction_combinations` defaults
> on) remain correct and are still prerequisites; they were just not the whole story.
>
> The rows were withdrawn rather than committed, for the second time in this file's
> history, and for the same reason: they passed green while measuring the wrong code path.
> That is now the strongest argument for building this witness properly — the defect has
> twice looked absent under instrumentation that could not see it.

> ## 2026-08-03 — three MORE combined handlers diverge in flags (found by #340's after-panel)
> #340 fixed the four `teqs`/`tsts` `*_samepage` handlers. A review seat then swept the rest
> of the family and found three that are **still** wrong, all pre-existing:
> - **`netbsd_cacheclean`** never writes flags at all, though the loop it replaces contains
>   a `subs` (`cpu_arm_instr.c:2067`, `:2072`). It also skips the loads, leaving r2 stale.
> - **`netbsd_cacheclean2`** skips its `subs` entirely (`:2087`, `:2093`) and leaves r0/r1
>   unchanged despite the ADD/SUB loop it stands in for.
> - **`netbsd_idle`** skips both TEQs on its fast paths without updating N/Z (`:2141`,
>   `:2172`); C/V happen to be right only because both immediates are zero. It also reads
>   rX into a local without writing the guest destination register.
>
> Two non-flag divergences in the same sweep: **`xchg`** has no `a != b` guard
> (`:2889`), so where standalone `eor r,r,r` would zero the register the folded form leaves
> it unchanged; and **`netbsd_memcpy`** bypasses its LDMs without publishing the final
> r3/r4/ip/lr.
>
> These are now MEASURABLE: #340 built the two-pass free-running probe driver that reaches
> folded handlers, which is what made the sweep worth doing. Verified equivalent and needing
> no work: all `cmps_*`, `tsts_lo_*` (after #340), `netbsd_memset`, `netbsd_scanc`,
> `netbsd_copyin/out`, `strlen`.

> ## 2026-08-03 — round 86 (#58) scoped accurately; the queue text was wrong
> The item said "32 table entries have no feature data". Measured against the tree, that is
> not the shape of the problem:
> - `ARM_CPU_TYPE_DEFS` has **51** entries (`src/include/arm_cpu_types.h:50`), not 32.
> - The `flags` field is not partly-filled — it holds exactly **three** bits, and they are
>   all it has ever held: `ARM_NO_MMU`, `ARM_DUAL_ENDIAN`, `ARM_XSCALE` (`:38-42`). There is
>   **no architecture-level field at all**. The file says so itself, twice:
>   `/* TODO: Include "ARM level", i.e. ARMv5 */` and `/* NOTE: Most of these are bogus! */`.
> - `cpu_type.flags` is read in exactly **three** places tree-wide — `cpu_arm.c:178`,
>   `cpu_arm.c:498`, `memory_arm.c:198` — and every one is XScale coprocessor/cache/memory
>   behaviour. **No instruction-decode path consults the CPU model at all**, which is why a
>   v6 media encoding decodes happily on an ARMv4: nothing is gating it, rather than a table
>   row being blank.
>
> So the real round is: add an architecture-level to the struct, populate it correctly for
> all 51 models from ARM's own documentation, and then gate the decoder on it. Populating it
> WRONG would be worse than leaving it — a model marked too high silently permits encodings
> that should trap, and too low breaks working guests — so this needs per-model primary
> sources, not inference from the names. Scoped, not started.

> ## 2026-08-03 — round 82 (#54): the "no user-mode witness" blocker is FALSE
> This item was parked on "needs a user-mode witness, which does not exist yet", and round
> 81's note recorded that debugger writes do not reach SR's mode fields. That is true of
> `sr` and it is the wrong register to write.
>
> **`rte` performs the transition architecturally**: `cpu_sh_instr.c:2767` calls
> `sh_update_sr(cpu, cpu->cd.sh.ssr)`, which applies MD and performs the r0-r7 bank swap —
> precisely what a kernel returning to user code does. So the witness is: debugger-write
> **`ssr`** with MD clear and **`spc`** to the user code address, plant `rte` plus its delay
> slot, and run. No SR write is involved and none is needed.
>
> Combined with #340's free-running two-pass driver, the remaining pieces are ordinary:
> set MMUCR.SQMD through the MMIO window (round 81's probe already writes MMUCR), plant a
> handler at the exception vector to publish EXPEVT and TEA, breakpoint after it, tracing
> off. The event-code dispute recorded above (ADDR_ERR_LD vs ADDR_ERR_ST) is exactly what
> such a probe settles by measurement instead of by argument — which is why it was left
> open rather than guessed.
>
> Scoped and unblocked; not built. The three code defects are unchanged: the check raises
> reserved-instruction where hardware raises a data address error, it is nested inside the
> `AT=1` branch though the rule is not conditioned on address translation, and the
> queue-FILL path (`memory_sh.c:298-303`) has no privilege check at all.

> ## 2026-08-03 — #341: dev_wdc's ATAPI read accounted for bytes it never delivered
> Found by #337's review sweep, and it is the READ-side twin of #338. The data-register
> read consumes one byte, two if `len >= 2`, four only if `len == 4` — so a 3- or 8-byte
> access consumes 1 or 2 — but the accounting used the REQUESTED `len`:
> `d->atapi_len -= len; d->atapi_received += len;`. For `len == 8` that subtracts 8 for 2
> bytes delivered, which lets `atapi_len` step PAST zero; its `== 0` test then never
> matches, `PHASE_COMPLETED` never fires, and the guest is told a transfer is further along
> than the data it actually got. Fixed to account for what was consumed.
>
> Same class as #283 (ASC) and #338 (mb89352): **the count reported has to be the count
> that happened.** Reachability-argued rather than rig-measured, like #337 — the landisk
> ATAPI witness is still its own round, and no gate row asserts this yet.
>
> **Still open from the same sweep**, none of them mine and all now measurable with #340's
> free-running driver: `netbsd_cacheclean` and `netbsd_cacheclean2` skip their `subs` flag
> updates entirely; `netbsd_idle` skips both TEQs without updating N/Z and never writes its
> guest destination register; `xchg` has no `a != b` guard, so where standalone
> `eor r,r,r` zeroes a register the folded form leaves it unchanged; `netbsd_memcpy`
> bypasses its LDMs without publishing the final r3/r4/ip/lr. On the PowerPC side:
> `fmadd`/`fmsub` raise none of their exception causes, `fnmadd`/`fnmsub` are undecoded and
> halt, and `NI` is defined but never consumed.


> ## 2026-08-05 — #342 resolves the `xchg` entry above
> The XOR-swap fold had no `a != b` guard. With one register the three encodings are
> `eor rX,rX,rX` three times over, each of which ZEROES rX, while `X(xchg)` exchanges rX
> with itself and leaves it unchanged. Measured on the committed build with #340's two-pass
> free-running driver: **0x5a where the architecture owes 0**. That byte is the row's own
> proof that the fold occurred — three standalone EORs cannot leave a nonzero value — which
> matters because this project has twice shipped combiner rows that were silently measuring
> the standalone path instead.
>
> **The other combined-handler entries above still stand**, and all four remain measurable
> with the same driver: `netbsd_cacheclean` and `netbsd_cacheclean2` skip their `subs` flag
> updates entirely, `netbsd_idle` skips both TEQs without updating N/Z and never writes its
> guest destination register, and `netbsd_memcpy` bypasses its LDMs without publishing the
> final r3/r4/ip/lr. Those four are harder than `xchg` was: each needs the exact NetBSD
> instruction sequence its combiner matches, reconstructed from the match conditions, before
> a row can be written at all.

> ## 2026-08-05 — netbsd_cacheclean2 is worse than its sibling, and #345 did not touch it
> #345 fixed variant 1's missing register check. Variant 2 has the same hole **and a second,
> larger one**. Its matcher (`cpu_arm_instr.c:2833-2839`) pins the two MCRs exactly by their
> instruction words, then accepts `add rX,rX,#32` and `subs rY,rY,#32` **without checking
> either register** — the same shape-not-registers defect #345 measured. But
> `X(netbsd_cacheclean2)` (`:2085-2089`) only advances `n_translated_instrs` and sets
> `next_ic = &ic[5]`. **It updates no registers whatsoever.**
>
> So it skips the two MCRs, the `add`, the `subs` and the branch, and leaves every register
> exactly as it found them. The loop it replaces would end with the add's register advanced
> by 32 per iteration and the subs's register at zero. This is wrong *even for the NetBSD
> sequence it was written for* — unlike variant 1, which at least performs
> `r[0] += r[1]; r[1] = 0`. It also reads `r[1]` for its instruction count without ever
> having checked that `r1` is the loop's counter.
>
> The fix is therefore two-part, and larger than #345's one-line guard: pin the registers as
> #345 did, **and** perform the update the fold is standing in for
> (`r[0] += r[1]; r[1] = 0`, the same closed form variant 1 uses). A witness needs the two
> exact MCRs plus add/subs/branch, run twice, with both registers seeded and published —
> the `run_cacheclean` driver in `arm_flags_probe.py` is the right starting shape.
>
> **The flag divergence originally filed against both variants still stands and is separate**:
> neither writes flags though the loops they replace end on a `subs` reaching zero, which
> owes Z=1 N=0 C=1 V=0.
