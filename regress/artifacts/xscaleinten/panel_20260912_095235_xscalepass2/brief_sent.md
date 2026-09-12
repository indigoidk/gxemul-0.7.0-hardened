# `xscaleinten` PASS 2 — review of the fix and its 29-row detector before commit

VERDICT LINE FIRST, then the liveness token `PASS2_XSCALE_20260912`.

**ONE QUESTION: is there a clause-(d) mutant of this fix that stays GREEN on all 29 rows?**
(Second, only if you read the source: is ACCEPT the right disposition? — see the end.)

This is a mutation-testing review of an emulator detector.  **Please do not simply ratify** — on
this very row an earlier pass refuted my claim that opcode fields were "disclosed", and a recent
panel had seven of nine seats confirm a premise a brief stated wrongly.  **Check the premises, not
just the derivations.**  If you find nothing, say WHAT YOU SWEPT (which predicates, which operand
swaps, which cells) — "zero found" and "zero looked for" must not read the same.

## THE TREE

`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\src\` and `...\GXEMUL-SEC\regress\`.  Ignore any other `src/`
under the project root (pristine 2021 copies; line numbers off by hundreds).

## THE FIX (uncommitted), `src/cpus/cpu_arm_coproc.c`, the WHOLE diff

```diff
@@ -309,8 +309,6 @@ void arm_coproc_i80321_6(struct cpu *cpu, int opcode1, int opcode2, int l_bit,
 	case 0:	switch (crn) {
 		case 0:	if (l_bit) {
 				cpu->cd.arm.r[rd] = cpu->cd.arm.i80321_inten;
-				fatal("TODO: XScale read from inten?\n");
-				exit(1);
 			} else
 				cpu->cd.arm.i80321_inten = cpu->cd.arm.r[rd];
 			break;
```

A guest MRC read of the Intel 80321 interrupt-enable register (coprocessor 6, crm 0, crn 0) loaded
the correct value into `rd` and then ended the emulator process.  Disposition: **ACCEPT** (delete the
diagnostic and the exit, keep the value) — the value is already computed, the write arm stores the
same field, and the sibling `crn 4` read (isteer) has no diagnostic and no exit.

## THE ENCLOSING FUNCTION, every exit path (post-fix, lines 304-418)

```c
void arm_coproc_i80321_6(struct cpu *cpu, int opcode1, int opcode2, int l_bit,
	int crn, int crm, int rd)
{
	switch (crm) {
	case 0:	switch (crn) {
		case 0:	if (l_bit) {
				cpu->cd.arm.r[rd] = cpu->cd.arm.i80321_inten;
			} else
				cpu->cd.arm.i80321_inten = cpu->cd.arm.r[rd];
			break;
		case 4:	if (l_bit)
				cpu->cd.arm.r[rd] = cpu->cd.arm.i80321_isteer;
			else {
				cpu->cd.arm.i80321_isteer = cpu->cd.arm.r[rd];
				if (cpu->cd.arm.r[rd] != 0) {
					fatal("ARM xscale interrupt steering"
					    " is not yet implemented\n");
					exit(1);
				}
			}
			break;
		case 8:	if (l_bit)
				cpu->cd.arm.r[rd] = cpu->cd.arm.i80321_isrc;
			else {
				cpu->cd.arm.i80321_isrc = cpu->cd.arm.r[rd];
				fatal("TODO: XScale int ack?\n");
				exit(1);
			}
			break;
		default:goto unknown;
		}
		break;
	case 1:	switch (crn) {       /* timers: tmr0 tmr1 tcr0 tcr1 trr0 trr1 tisr wdtcr, crn 0..7 */
		case 0:	if (l_bit) cpu->cd.arm.r[rd] = cpu->cd.arm.tmr0; else cpu->cd.arm.tmr0 = cpu->cd.arm.r[rd];
			break;
		/* ... crn 1..7 of the same shape; tcr0/tcr1 reads increment the counter first;
		   a tisr write clears bits and deasserts the timer IRQs ... */
		default:goto unknown;
		}
		break;
	default:goto unknown;
	}
	return;
unknown:
	fatal("arm_coproc_i80321_6: unimplemented opcode1=%i opcode2=%i crn="
	    "%i crm=%i rd=%i l=%i)\n", opcode1, opcode2, crn, crm, rd, l_bit);
	exit(1);
}
```

`opcode1` and `opcode2` are **never tested** by this handler.  The interrupt controller elsewhere
consumes `i80321_inten` (an enabled, pending source raises an ARM IRQ, vector 0x18).

## SETTLED PREMISES (do not re-derive; challenge only with evidence)

* `fatal()` does not exit; the `exit(1)` is what ended the process.
* The reads are driven by a real guest instruction through the real coprocessor dispatch on the
  unmodified in-tree machine `-E iq80321` (rung-3 cold-debugger witness), and `machine_iq80321.c`
  installs this handler as coprocessor 6.

## THE DETECTOR — `regress/xscale_inten_probe.py`, 29 rows (its CONTRACT header, verbatim)

> Designed to catch, and each MEASURED in kill table 2: the removed fatal()+exit(1) reinstated
> verbatim (HEAD 12/29); reinstated under a different predicate -- isrc != 0 (M1), opcode1 != 0
> (M_OP1), opcode2 != 0 (M_OPCODE2), rd == 15 (M_RD15), or after the fourth read (M_NREAD); the read
> loading another register (M5: isteer); the crm=1 tmr0 read returning inten (M_CRM); and an inten
> write that also stores isteer (M_ISTEER_WR).
> NOT COVERED: the handler ignores opcode1 and opcode2, and the rows pin that for ONE nonzero value
> of each, not for every encoding; r15 data and flag semantics beyond survival to the marker
> (RD15_SURVIVE); SIB_READ asserts survival only; interrupt-controller behaviour beyond the one
> enable/contrast path the ANCHOR rows drive.  The isteer non-zero write, the isrc write and the
> unknown-tuple exit are host kills this round RETAINS, rowed as controls.

**The rows, by arm** (each arm is a fresh emulator session unless noted):

* **D** (one session, single-step): `mcr` trr0 seed / `mrc` trr0 (`D_TRR0`, liveness); read inten at
  reset into r9 (`D_RESET`, want 0); inten<-S1, read into r4 (`D_S1`); inten<-0, read into r5
  (`D_ZERO`); inten<-S2, read into r6 (`D_S2`); read with **opcode2=1** into r10 (`D_OP2`); then
  `mov r0,#0x5a` (`D_MARKER`).  Plus `D_SURVIVE` (no death), `D_TODO_ABS` (no diagnostic text),
  `P2_VACUITY` (every destination held a poison DIFFERENT from its want before its read).
  S1 = 0xA500005A, S2 = 0x5AA5F00D.
* **LNC**: a conditional `mrceq` whose condition fails must leave r3's poison (`LNC_COND`); a NOP
  destination check (`X4_NOP`); `LNC_P2`; the subject read r3<-S1 (`LNC_SUB`); `LNC_TODO_ABS`; `LNC_MARKER`.
* **E_UNKNOWN**: an unknown tuple (opcode1=3, crn=9, crm=2) still dies with its 6-field message.
* **S_ISRC_WR**: an isrc write still dies.  **SIB_READ**: crn-4 read survives.  **SIB_WRITE**: crn-4
  non-zero write still dies.
* Fresh sessions: **D_OP1** (read with **opcode1=1**, want S1); **INTEN_WRITE_PRESERVES_ISTEER**
  (isteer<-0, inten<-S1, read isteer, want 0); **D_CRM1_TMR0** (tmr0<-0x5A5A0000, inten<-S1, read
  crm=1/crn=0, want 0x5A5A0000).
* **RD15_SURVIVE**: an inten read into r15 survives to the marker.
* **ANCHOR** (free-running): inten<-bit 28; the UART asserts irq 28 (`ANCHOR_ISRC`); read inten while
  isrc != 0 (`ANCHOR_M1`); unmask CPSR.I and spin — the IRQ must reach vector 0x18 (`ANCHOR_EXC`);
  contrast: inten = 0 spins and 0x18 is never reached (`ANCHOR_CONTRAST`).
* `A2_INSTALLED` (CP6 installed).

## MEASURED — kill table 2, frozen 29-row instrument, fresh builds, scratch clone

| leg | score | FAILING (BLOCKED) |
|---|---|---|
| BASE (the fix) | 29/29 CONTROL=OK | none |
| HEAD (committed, pre-fix) | 12/29 | subject reads, markers, anchors (P2_VACUITY and seven more BLOCKED) |
| M1 `if (isrc != 0) {fatal;exit}` after the load | 26/29 | ANCHOR_M1, ANCHOR_CONTRAST (ANCHOR_EXC) |
| M5 read loads isteer | 27/29 | INTEN_WRITE_PRESERVES_ISTEER, ANCHOR_EXC |
| M_OPCODE2 `if (opcode2 != 0)` exit | 26/29 | D_SURVIVE (D_OP2, D_MARKER) |
| M_RD15 `if (rd == 15)` exit | 28/29 | RD15_SURVIVE |
| M_NREAD static count, exit on 5th read | 26/29 | D_SURVIVE (D_OP2, D_MARKER) |
| M_OP1 `if (opcode1 != 0)` exit | 28/29 | D_OP1 only |
| M_ISTEER_WR inten write also stores isteer | 28/29 | INTEN_WRITE_PRESERVES_ISTEER only |
| M_CRM tmr0 read returns inten | 28/29 | D_CRM1_TMR0 only |

Restore cmp-CLEAN, binary FRESH.  Prediction written before the table: 9 of 10 legs exact; HEAD was
predicted 13/29 and measured 12/29 (a BLOCKED row counted as a pass in the prediction's arithmetic).

## QUESTIONS

1. **(the one that matters)** Enumerate DEPENDS-ON for this diff: (1) the predicates DOMINATING the
   edited lines, up to the function boundary (`crm == 0`, `crn == 0`, `l_bit`); (2) operand swaps
   drawn from fields the guarded BODY reads (`rd`, `cpu->cd.arm.r[]`, `i80321_inten`).  For a pure
   deletion the (d) mutant re-introduces the removed behaviour under a DIFFERENT predicate.  **Name
   any such mutant that leaves all 29 rows green**, and say which row you expected to catch it and
   why it cannot.  Candidates I have NOT built, to check or refute: exit only when `i80321_inten`
   has some bit set that neither S1 nor S2 has; exit only when `rd == 0`, or `rd` is some register
   no row reads into; exit only when `isteer != 0`.  Is each a floor cell (the body tests or reads
   the lvalue) or clause-(e) disclosure (the body never distinguishes it)?
2. **Does any row's named channel fail to vary under its named mutant** (vacuous by construction)?
3. **Which statement in the CONTRACT above is false or overclaims?**
4. *(file-reading seats only)* Is ACCEPT right, or should this be a latched announce?  The sibling
   read is quiet; a DC21285 precedent in this tree is ACCEPT for a read the model already answers
   correctly.

Give a verdict line: `NO SURVIVING (d) MUTANT — swept: <list>` or `SURVIVOR: <exact edit>`.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
