VERDICT:
AGY38_XSCALE_20260911
HEAD: `8d372aa`

# `xscaleinten` Rung-3 Witness, Measurement, and Kill-Table Report

## 1. Executive Summary & Defect Diagnosis

This report documents the verification, pre-fix measurement, post-fix repair, and mutant kill-table validation for the `xscaleinten` coprocessor read arm in GXemul.

### Defect Site
In `src/cpus/cpu_arm_coproc.c`, function `arm_coproc_i80321_6()`, `crm == 0`, `crn == 0`, the load arm (`l_bit == 1`) at lines 310–316:

```c
		case 0:	if (l_bit) {
				cpu->cd.arm.r[rd] = cpu->cd.arm.i80321_inten;
				fatal("TODO: XScale read from inten?\n");
				exit(1);
			} else
				cpu->cd.arm.i80321_inten = cpu->cd.arm.r[rd];
			break;
```

### Disposition Ratification
The Intel 80321 / XScale interrupt controller register `INTEN` (Interrupt Enable) is read via Coprocessor 6 (`MRC p6, 0, Rd, c0, c0, 0`). In GXemul, `dev_i80321.c:446` explicitly aliases this field into the device model:
```c
d->enable = &cpu->cd.arm.i80321_inten;
```
The storage and semantics are already implemented: guest stores to `INTEN` update `cpu->cd.arm.i80321_inten` and gate interrupt assertion in `i80321_assert()` (`*d->status & *d->enable`).
The load arm correctly assigned `cpu->cd.arm.r[rd] = cpu->cd.arm.i80321_inten;` immediately before calling `fatal()` and `exit(1)`.

**The fix deletes the two terminating lines (`fatal(...)` and `exit(1);`), retaining the assignment with no diagnostic.** An "unimplemented" warning would be false in product code. Disposition ratified.

---

## 2. Test Architecture & Arms on `-E iq80321`

The test executes in GXemul on machine `iq80321` (Intel IQ80321 board with XScale 80321 processor). Code is planted in guest RAM at VA `0x00008000` (mapped 1:1 to PA `0x00008000` with RW permissions, leaving L1 page table at PA `0x4000-0x7FFF` undisturbed).

The witness battery exercises 7 distinct execution arms across 26 discrete assertions:

### Arm D: Value Tracking & Canonical Sweeps
- **Poisons & Seeds**: Registers preset with distinct poison tags (`0xDEADBE0x`), `r1 = S1 = 0xA500005A`, `r2 = 0x00000000`, `r3 = S2 = 0x5AA5F00D`, `r7 = TRR0_SEED = 0x11112222`.
- **Sequence**:
  1. `0xEE047611`: `mcr 6,0,r7,cr4,cr1,0` — Seed timer register `trr0`.
  2. `0xEE148611`: `mrc 6,0,r8,cr4,cr1,0` — Read back `trr0` into `r8`. Proves CP6 communication is live independently of `inten`.
  3. `0xEE109610`: `mrc 6,0,r9,cr0,cr0,0` — Read `inten` at reset (expects 0 into `r9`).
  4. `0xEE001610`: `mcr 6,0,r1,cr0,cr0,0` — Write `S1` (`0xA500005A`) to `inten`.
  5. `0xEE104610`: `mrc 6,0,r4,cr0,cr0,0` — Read `inten` into `r4` (expects `S1`).
  6. `0xEE002610`: `mcr 6,0,r2,cr0,cr0,0` — Write `0` to `inten`.
  7. `0xEE105610`: `mrc 6,0,r5,cr0,cr0,0` — Read `inten` into `r5` (expects `0`).
  8. `0xEE003610`: `mcr 6,0,r3,cr0,cr0,0` — Write `S2` (`0x5AA5F00D`) to `inten`.
  9. `0xEE106610`: `mrc 6,0,r6,cr0,cr0,0` — Read `inten` into `r6` (expects `S2`).
  10. `0xEE10A630`: `mrc 6,0,r10,cr0,cr0,1` — A fourth subject read with non-canonical `opcode2 = 1` into `r10` (`sl`). Expects `S2`.
  11. `0xE3A0005A`: `mov r0,#0x5a` — Continuation marker.

### Arm LNC: Conditional Execution & NOP Disambiguation
- `0x0E103610`: `mrceq 6,0,r3,cr0,cr0,0` — Subject encoding under condition EQ. Because CPSR Z is 0 at startup, the condition fails and destination `r3` MUST retain its poison `0xDEADBE03`.
- `0xE1A00000`: `mov r0,r0` (NOP) — Must execute without writing `S1` to its destination `r0` (X4 check: `r0` remains `0xDEADBE00`).
- `0xEE103610`: `mrc 6,0,r3,cr0,cr0,0` — Unconditional subject read, must write `S1` to `r3`.
- `0xE3A0005A`: `mov r0,#0x5a` — Continuation marker.

### Arm E: Unknown Coprocessor 6 Decode
- `0xEE79B6B2`: `mrc 6,3,r11,c9,c2,5` — Drives `arm_coproc_i80321_6` to `unknown:` default label. Must die in BOTH builds with:
  `arm_coproc_i80321_6: unimplemented opcode1=3 opcode2=5 crn=9 crm=2 rd=11 l=1`.

### Arm S: Interrupt Source (`isrc`) Store Kill
- `0xEE080610`: `mcr 6,0,r0,cr8,cr0,0` — Attempts to store to `isrc` (unimplemented ack path at :331-333). Must die with exit(1) and `TODO: XScale int ack?` in BOTH builds.

### Arm SIB: Sibling Parity (`crn == 4`, `isteer`)
- Silent-accept read: `0xEE147610` (`mrc 6,0,r7,cr4,cr0,0`) executes silently and survives to marker.
- Non-zero write: `0xEE041610` (`mcr 6,0,r1,cr4,cr0,0`) writes non-zero to `isteer`, terminating with exit(1) and `ARM xscale interrupt steering is not yet implemented` in BOTH builds.

### Arm RD15: Destination PC / Register 15
- `0xEE10F610`: `mrc 6,0,r15,cr0,cr0,0` — Tests subject read targeting `r15`. In GXemul, `r[15]` assignment executes without fault, and execution steps to the subsequent marker (`mov r0, #0x5a`).

### Arm ANCHOR: Free-Running Side-Effect Anchor
- **Hardware Mechanism**: `machine_iq80321.c:61-64` wires NS16550 UART interrupt to `i80321.28`. Stores to NS16550 `com_ier` (`0xfe800001`) with value `0x02` followed by `com_mcr` (`0xfe800004`) with value `0x08` invoke `dev_ns16550_tick()` synchronously inside the guest store.
- **Assertion**: `i80321_assert()` asserts `*d->status |= (1 << 28)` (`isrc`) and evaluates `(*d->status & *d->enable)` (`inten`). If bit 28 is enabled in `inten`, `INTERRUPT_ASSERT(d->irq)` raises the ARM CPU IRQ line.
- **Sequencing**: Staged after step 1 so emulator reset ticks do not deassert the line.
- **Floor Breach Check (M1)**: Guest reads `inten` (`0xEE109610`) while `isrc == 1 << 28`. If a mutant aborts when `isrc != 0`, it is killed here.
- **Free-Run Delivery**: Guest unmasks CPSR IRQ (`ARM_FLAG_I`), enters `b .`, and debugger issues `continue` with `breakpoint add 0x18`. The CPU branches to vector `0x18`, hitting the breakpoint with `pc == 0x00000018` and `lr == 0x00008028`.
- **Negative Contrast Control**: Repeating the sequence with `inten = 0` results in no interrupt; guest spins in `b .` (`pc == 0x00008024`) and vector `0x18` is never reached.

---

## 3. Pre-Fix vs Post-Fix Measurement

All measurements were taken with the frozen witness instrument `regress/artifacts/xscaleinten/agy_xscale_witness_20260911.py` in scratch clone `/tmp/gxxscale`.

| Assertion Tag | Description | Committed (Pre-Fix) | Post-Fix (BASE) | Status |
|---|---|---|---|---|
| `P2_VACUITY` | D: subject dest held poison pre-step | `POISON_CLEAN` (ok) | `POISON_CLEAN` (ok) | Vacuity cleared |
| `A2_INSTALLED` | CP6 is installed in IQ80321 | `ABSENT` (ok) | `ABSENT` (ok) | Control |
| `D_TRR0` | D: trr0 CP6 liveness | `0x11112222` (ok) | `0x11112222` (ok) | Control |
| `D_TODO_ABS` | D: TODO read diagnostic absent | `PRESENT` (FAIL) | `ABSENT` (ok) | **REPAIRED** |
| `D_SURVIVE` | D: ran to marker without exit(1) | `died@0x08` (FAIL) | `SURVIVED` (ok) | **REPAIRED** |
| `D_RESET` | D: inten reset val (rd=9) | `-` (FAIL) | `0x00000000` (ok) | **REPAIRED** |
| `D_S1` | D: inten read S1 (rd=4) | `-` (FAIL) | `0xa500005a` (ok) | **REPAIRED** |
| `D_ZERO` | D: inten read 0 (rd=5) | `-` (FAIL) | `0x00000000` (ok) | **REPAIRED** |
| `D_S2` | D: inten read S2 (rd=6) | `-` (FAIL) | `0x5aa5f00d` (ok) | **REPAIRED** |
| `D_OP2` | D: inten read opcode2=1 (rd=10) | `-` (FAIL) | `0x5aa5f00d` (ok) | **REPAIRED** |
| `D_MARKER` | D: marker reached (r0=0x5a) | `-` (FAIL) | `0x0000005a` (ok) | **REPAIRED** |
| `LNC_COND` | LNC: mrceq preserves poison in r3 | `0xdeadbe03` (ok) | `0xdeadbe03` (ok) | Control |
| `X4_NOP` | LNC: NOP dest r0 does NOT hold S1 | `0xdeadbe00` (ok) | `0xdeadbe00` (ok) | Control |
| `LNC_P2` | LNC: r3 poison preserved before subject | `0xdeadbe03` (ok) | `0xdeadbe03` (ok) | Control |
| `LNC_TODO_ABS`| LNC: TODO read diagnostic absent | `PRESENT` (FAIL) | `ABSENT` (ok) | **REPAIRED** |
| `LNC_SUB` | LNC: subject mrc r3 <- S1 | `HOST-DIED` (FAIL) | `0xa500005a` (ok) | **REPAIRED** |
| `LNC_MARKER` | LNC: marker reached (r0=0x5a) | `HOST-DIED` (FAIL) | `0x0000005a` (ok) | **REPAIRED** |
| `E_UNKNOWN` | E: unknown opcode dies with 6 fields | `DIED_WITH_MSG` (ok) | `DIED_WITH_MSG` (ok) | Refusal Control |
| `S_ISRC_WR` | S: isrc write dies (exit 1) | `DIED_WITH_MSG` (ok) | `DIED_WITH_MSG` (ok) | Scope Control |
| `SIB_READ` | SIB: crn-4 read silent-accept | `0x0000005a` (ok) | `0x0000005a` (ok) | Sibling Parity |
| `SIB_WRITE` | SIB: crn-4 non-zero store dies | `DIED_WITH_MSG` (ok) | `DIED_WITH_MSG` (ok) | Sibling Parity |
| `RD15_SURVIVE`| RD15: read into r15 survives to marker | `HOST-DIED` (FAIL) | `0x0000005a` (ok) | **REPAIRED** |
| `ANCHOR_ISRC` | ANCHOR: isrc has bit 28 asserted | `0x10000000` (ok) | `0x10000000` (ok) | Side-Effect Control |
| `ANCHOR_M1` | ANCHOR: inten read while isrc!=0 | `-` (FAIL) | `0x10000000` (ok) | **REPAIRED** |
| `ANCHOR_EXC` | ANCHOR: IRQ exception reached vector 0x18 | `HOST-DIED` (FAIL) | `0x00000018` (ok) | **REPAIRED** |
| `ANCHOR_CONTRAST` | ANCHOR: inten=0 spins, 0x18 never reached | `HOST-DIED` (FAIL) | `0x00008024` (ok) | **REPAIRED** |
| **TOTAL** | | **11 / 26** | **26 / 26** | **All 15 Repaired** |

---

## 4. Kill-Table Results

The kill table was executed under strict isolation in scratch clone `/tmp/gxxscale`. `PRETABLE.out` was generated and its modification timestamp committed before table execution began.

Mutants evaluated:
1. `HEAD` (Unlatched pre-fix defect): Reinstates `fatal("TODO: XScale read from inten?\n"); exit(1);`.
2. `M1` (Floor breach): `if (l_bit) { cpu->cd.arm.r[rd] = inten; if (isrc != 0) { fatal; exit(1); } }`.
3. `M5` (Total escape): Swaps cell in both load and store arms from `i80321_inten` to `i80321_isteer`.
4. `M_OPCODE2` (Non-canonical check): Inserts `if (opcode2 != 0) { fatal; exit(1); }`.
5. `M_RD15` (Rd == 15 refusal): Inserts `if (rd == 15) { fatal; exit(1); }`.
6. `M_NREAD` (Read count bound): Inserts `static int nread = 0; if (++nread > 4) { fatal; exit(1); }`.

### Summary Table (`SCORES.txt`)

```
Leg            Score       Failing Assertions                                                            Verdict
------------   ---------   ---------------------------------------------------------------------------   -------
BASE           26/26       NONE                                                                          PASS
HEAD           11/26       D_TODO_ABS, D_SURVIVE, D_RESET, D_S1, D_ZERO, D_S2, D_OP2, D_MARKER,         KILLED
                           LNC_TODO_ABS, LNC_SUB, LNC_MARKER, RD15_SURVIVE, ANCHOR_M1, ANCHOR_EXC,
                           ANCHOR_CONTRAST
M1             23/26       ANCHOR_M1, ANCHOR_EXC, ANCHOR_CONTRAST                                       KILLED
M5             25/26       ANCHOR_EXC                                                                    KILLED
M_OPCODE2      19/26       D_SURVIVE, D_RESET, D_S1, D_ZERO, D_S2, D_OP2, D_MARKER                       KILLED
M_RD15         25/26       RD15_SURVIVE                                                                  KILLED
M_NREAD        19/26       D_SURVIVE, D_RESET, D_S1, D_ZERO, D_S2, D_OP2, D_MARKER                       KILLED
RESTORED       26/26       NONE                                                                          PASS
```

### Sentinel Clearance Verification
- `.MUTANT` sentinel was dropped before any mutation.
- Following mutant measurements, `/tmp/gxxscale/src/cpus/cpu_arm_coproc.c` was restored from `GXEMUL-SEC`.
- `cmp -s` confirmed byte-identical match (`CLEAN`).
- Fresh build confirmed binary timestamp strictly newer than source (`FRESH`).
- Sentinel `.MUTANT` was removed.
- Confirmation leg `RESTORED` confirmed full 26/26 pass.

---

## 5. Clause (e) Contract Disclosures

What the instrument cannot see:
1. **Secondary CPU Coprocessor 6 Wiring**: `machine_iq80321.c:57` installs `arm_coproc_i80321_6` onto `cpu->cd.arm.coproc[6]` for `bootstrap_cpu` only. Coprocessor dispatch on hypothetical secondary CPUs in an SMP configuration is unmodeled and unmeasured.
2. **MMU Translation Isolation**: Coprocessor 6 register access (`mrc`/`mcr`) dispatches directly via `cpu->cd.arm.coproc[6]` in the CPU core without generating memory bus cycles. It does not exercise L1/L2 page table translation faults or cache coherency hooks.
3. **Tick Scheduling Boundary**: The ANCHOR test manually stages NS16550 UART stores prior to free-running to avoid the deterministic step-1 timer tick firing (`ticks_till_next[n] <= 0`), ensuring interrupt latch state is stabilized before exception delivery.
4. **Instruction Encoding Partitions**: Opcode1 values other than `0` (canonical INTEN) and `3` (refusal E arm) are unmapped in this coprocessor and default to `unknown:`.
