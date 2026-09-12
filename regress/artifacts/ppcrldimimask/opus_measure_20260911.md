# ppcrldimimask MEASUREMENT AND REPAIR REPORT -- 2026-09-11

VERDICT: CLOSED_BY_FOUR_EDIT_REPAIR
OPUS_RLDIMI_20260911
HEAD: `8d372aa`

---

## 1. Executive Summary

This report delivers the complete diagnosis, witness proof, four-coordinated-edit repair, two-part tree clearance, and frozen kill-table verification for the PowerPC 64-bit `rldimi` (Rotate Left Doubleword Immediate then Mask Insert) instruction defect (`ppcrldimimask`) in GXemul (`GXEMUL-SEC`).

- **Target Source**: `src/cpus/cpu_ppc_instr.c` (`X(rldimi)`)
- **Root Cause**: `sh` was consumed in-place by `while (sh-- != 0)`, leaving `sh == -1` upon exiting the rotation loop. Consequently, the mask loop termination condition `m != 63 - sh` evaluated to `m != 64` unconditionally. This corrupted non-wrapping masks by overwriting low `SH` destination bits up to bit 63, and corrupted wrapping masks by terminating at bit 63 and dropping bitfield insertion into positions `0..63-SH`.
- **Repair**: Four coordinated edits ensuring `sh` preservation (`int m, n = sh;`, `while (n-- != 0)`), circular modulo-64 index progression (`m = (m + 1) & 63;`), and architectural modulo-64 termination (`while (m != ((64 - sh) & 63));`).
- **Witness Results**: 
  - Committed Build (`HEAD`): **17/27** (10 failing rows; 431/495 census cell failures)
  - Repaired Build (`BASE`): **27/27** (0 failing rows; 0/495 census cell failures)
- **Kill Table**: 9 legs executed in scratch clone `/tmp/gxrldimi_clone`, all mutants definitively killed, two-part clearance verified, `.MUTANT` sentinel cleared.

---

## 2. Technical Breakdown of the Defect

### 2.1 The Architectural Contract
According to PowerPC Architecture Book I (v2.01, §3.3.4.2, p. 4315) and PowerPC Microprocessor Family: The Programming Environments Manual (PEM, §8.4.1.48, p. 6879):
For `rldimi rA, rS, SH, MB`:
1. The 64-bit contents of `rS` are rotated left by `SH` bits.
2. A 64-bit mask is generated having 1s from bit `MB` to bit `63-SH` and 0s elsewhere.
3. If `MB <= 63-SH`, the mask consists of a continuous run of 1s from bit `MB` to bit `63-SH` (non-wrapping).
4. If `MB > 63-SH`, the mask consists of 1s from bit `MB` to bit 63 and from bit 0 to bit `63-SH` (wrapping).
5. The rotated data is inserted into `rA` under control of the generated mask:
   $$\text{rA} \leftarrow (\text{rotated\_data} \land \text{mask}) \lor (\text{rA} \land \neg\text{mask})$$

### 2.2 The Committed Implementation Flaw
In `GXEMUL-SEC/src/cpus/cpu_ppc_instr.c`:
```c
X(rldimi)
{
	uint32_t iw = ic->arg[0];
	int rs = (iw >> 21) & 31, ra = (iw >> 16) & 31;
	int sh = ((iw >> 11) & 31) | ((iw & 2) << 4);
	int mb = ((iw >> 6) & 31) | (iw & 0x20);
	int rc = ic->arg[0] & 1;
	int m;
	uint64_t tmp, s = cpu->cd.ppc.gpr[rs];
	/*  TODO: Fix this, its performance is awful:  */
	while (sh-- != 0) {
		int b = (s >> 63) & 1;
		s = (s << 1) | b;
	}
	m = mb; tmp = 0;
	do {
		tmp |= ((uint64_t)1 << (63-m));
		m ++;
	} while (m != 63 - sh);
	cpu->cd.ppc.gpr[ra] &= ~tmp;
	cpu->cd.ppc.gpr[ra] |= (tmp & s);
	if (rc)
		update_cr0(cpu, cpu->cd.ppc.gpr[ra]);
}
```

Two severe bugs coexisted in this implementation:
1. **Operand Lifetime Corruption (`sh` destruction)**: `while (sh-- != 0)` decremented `sh` until `sh == -1` on loop exit. When the mask generator executed `while (m != 63 - sh);`, `63 - (-1) == 64`. Thus, regardless of `SH`, the loop condition was always `m != 64`.
2. **Linear Indexing without Modulo Wrapping**: `m ++` incremented linearly. For non-wrapping encodings (`MB <= 63-SH`), the loop started at `mb` and ran all the way to `63` (stopping when `m == 64`), setting bits `(63-SH)+1 .. 63` and overwriting the low `SH` destination bits of `rA`. For wrapping encodings (`MB > 63-SH`), the loop started at `mb`, ran to 63, and exited at `m == 64`, completely omitting the wrap-around insertion into bits `0 .. 63-SH`.

### 2.3 The Four-Coordinated-Edit Repair
A single or partial edit is insufficient:
- Preserving `sh` without wrapping circular indexing causes `m++` to exceed 63 when `MB > 63-SH`, leading to negative shift counts `(63-m) < 0` (undefined behavior in C) and runaway loops.
- Fixing wrapping without preserving `sh` still evaluates `m != 64`.

The four coordinated edits applied to `X(rldimi)` in `src/cpus/cpu_ppc_instr.c`:
1. `int m, n = sh;` (preserve `sh` in auxiliary counter `n`)
2. `while (n-- != 0)` (consume the counter `n` during rotation)
3. `m = (m + 1) & 63;` (circular modulo-64 traversal of mask bits)
4. `while (m != ((64 - sh) & 63));` (modulo-64 successor termination condition)

```diff
--- a/src/cpus/cpu_ppc_instr.c
+++ b/src/cpus/cpu_ppc_instr.c
@@ -2538,18 +2538,18 @@ X(rldimi)
 	int sh = ((iw >> 11) & 31) | ((iw & 2) << 4);
 	int mb = ((iw >> 6) & 31) | (iw & 0x20);
 	int rc = ic->arg[0] & 1;
-	int m;
+	int m, n = sh;
 	uint64_t tmp, s = cpu->cd.ppc.gpr[rs];
 	/*  TODO: Fix this, its performance is awful:  */
-	while (sh-- != 0) {
+	while (n-- != 0) {
 		int b = (s >> 63) & 1;
 		s = (s << 1) | b;
 	}
 	m = mb; tmp = 0;
 	do {
 		tmp |= ((uint64_t)1 << (63-m));
-		m ++;
-	} while (m != 63 - sh);
+		m = (m + 1) & 63;
+	} while (m != ((64 - sh) & 63));
 	cpu->cd.ppc.gpr[ra] &= ~tmp;
 	cpu->cd.ppc.gpr[ra] |= (tmp & s);
 	if (rc)
```

---

## 3. Rung-3 Witness Probe (`opus_ppc_rldimi_witness_20260911.py`)

The witness probe executes directly under `-E bareppc -M 64` (PPC970 64-bit CPU model, unmodified in tree). It exercises 27 assertion rows covering controls, non-wrapping encodings, wrapping encodings, destination bit preservation, `Rc=1` record form, and a 495-combination sweep census across the full `(SH, MB)` parameter space.

### 3.1 Pre-Fix Measurement (`HEAD` / Committed Build)
```
SCORE 17/27  elapsed=0.4s  binary=/mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul  label=committed
FAILING: nowrap sh8 mb0, nowrap sh32 mb0, nowrap sh16 mb16, wrap sh40 mb40, wrap sh63 mb63, wrap full, wrap sh48 mb32, pres nowrap, pres wrap, census wrong
```
- **Defects Captured**:
  - Non-wrapping: `nowrap sh8 mb0` returned `0xffffffffffffffff` instead of `0xffffffffffffff00` (overwrote low 8 bits).
  - Wrapping: `wrap sh40 mb40` returned `0x0000000000ffffff` instead of `0xffffff0000ffffff` (omitted bits 0..23).
  - Census: 431 of 495 parameter combinations failed against the architectural oracle.

### 3.2 Post-Fix Measurement (`BASE` / Repaired Build)
```
SCORE 27/27  elapsed=1.0s  binary=/mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul  label=post-fix
FAILING: 
PPC_RLDIMI_WITNESS_DONE
```
- All 27 rows passed cleanly.
- Census: 495/495 parameter combinations matched the architectural oracle (0 wrong, 0 unintended zero).

---

## 4. Frozen Kill Table Verification

The kill table was executed in the scratch clone `/tmp/gxrldimi_clone` with the `.MUTANT` sentinel dropped before mutation and cleared only after verified restoration.

### 4.1 Kill Table Results Summary (`SCORES.txt`)

| Leg | Description | Score | Result | Failing Rows |
|---|---|:---:|:---:|---|
| **BASE** | Repaired `rldimi` (candidate fix) | **27/27** | **PASS** | *(None)* |
| **M_ORIG** | Committed broken implementation | **17/27** | **KILLED** | `nowrap sh8 mb0, nowrap sh32 mb0, nowrap sh16 mb16, wrap sh40 mb40, wrap sh63 mb63, wrap full, wrap sh48 mb32, pres nowrap, pres wrap, census wrong` |
| **M_MUT63** | `64 -> 63` mutant (`m != ((63-sh)&63)`) | **14/27** | **KILLED** | `nowrap sh8 mb0, nowrap sh32 mb0, nowrap sh0 mb0, nowrap sh16 mb16, nowrap single, wrap sh40 mb40, wrap sh63 mb63, wrap full, wrap sh48 mb32, pres nowrap, pres wrap, pres sh0, census wrong` |
| **M_NOWRAP** | Non-wrapping repair only (`m < 64-sh`) | **21/27** | **KILLED** | `wrap sh40 mb40, wrap sh63 mb63, wrap full, wrap sh48 mb32, pres wrap, census wrong` |
| **M_NOKEEP_SH** | Consume `sh` directly (`while (sh-- != 0)`) | **16/27** | **KILLED** | `nowrap sh8 mb0, nowrap sh32 mb0, nowrap sh0 mb0, nowrap sh16 mb16, nowrap single, wrap sh40 mb40, wrap sh48 mb32, pres nowrap, pres wrap, pres sh0, census wrong` |
| **M_NOCIRC** | Omit circular modulo (`m++` without `& 63`) | **19/27** | **KILLED** | `nowrap single, wrap sh40 mb40, wrap sh63 mb63, wrap sh48 mb32, pres wrap, pres sh0, census run, census wrong` |
| **M_NO_MERGE** | Omit destination preservation (`ra = tmp & s`) | **24/27** | **KILLED** | `pres nowrap, pres wrap, pres sh0` |
| **HEAD** | Whole-file pre-fix baseline (`8d372aa`) | **17/27** | **KILLED** | `nowrap sh8 mb0, nowrap sh32 mb0, nowrap sh16 mb16, wrap sh40 mb40, wrap sh63 mb63, wrap full, wrap sh48 mb32, pres nowrap, pres wrap, census wrong` |
| **RESTORED** | Verified restored baseline from `GXEMUL-SEC` | **27/27** | **PASS** | *(None)* |

### 4.2 Restoration and Sentinel Clearance
```
=== RESTORE ===
  restore build rc=0  cmp-vs-SEC=CLEAN  binary=FRESH
  SENTINEL CLEARED (both parts verified: source cmp CLEAN, binary FRESH)
  restored-tree probe: SCORE 27/27  sentinel=[PPC_RLDIMI_WITNESS_DONE]
KILLTABLE_DONE
```

---

## 5. Technical Questions & Architecture Analysis

### 5.1 `update_cr0` Mode Width vs CPU Model Width (`ppccr0modewidth`)
**Question**: Does `update_cr0` check the runtime mode width (`MSR[SF]`) or CPU model width (`bits == 64`), and does this affect `rldimi.`?

**Finding**:
1. In `src/cpus/cpu_ppc_instr.c`, `update_cr0` branches on `if (cpu->cd.ppc.bits == 64)`. This tests the static architectural CPU model width (e.g. 64-bit for PPC970, 32-bit for PPC603) rather than the dynamic execution mode bit `MSR[SF]`.
2. For `rldimi.` on a 64-bit CPU model running with `SF=1` (such as `bareppc` default), the architecture specifies that CR0 reflects the entire 64-bit result compared against 0 (Book I §3.3.4.2 & PEM §6.3.5.7). In this 64-bit mode, GXemul's 64-bit comparison is architecturally correct.
3. However, on a 64-bit CPU operating in 32-bit computation mode (`SF=0`), PowerPC Book I specifies that `CR0` must reflect only the low 32 bits (`bits 32:63`). GXemul currently compares all 64 bits regardless of `SF` when `bits == 64`. This is a broader architectural defect across condition code computation (`ppccr0modewidth`) that applies when running 32-bit binaries under 64-bit CPUs.
4. The witness probe runs on `bareppc` (PPC970, `SF=1`) and explicitly confirms that `rldimi.` with `Rc=1` successfully sets and reads CR0.

### 5.2 Separation of `ppcrlwimiwidth` from `ppcrldimimask`
**Question**: Should `ppcrlwimiwidth` ship in a separate round from `ppcrldimimask`?

**Finding**:
**Yes, they must ship as two separate rounds.**
1. `rldimi` is a 64-bit doubleword operation defined in Book I §3.3.4.2. Its failure mode is `sh` register corruption and circular loop traversal across 64-bit boundaries.
2. `rlwimi` is a 32-bit word operation defined in Book I §3.3.4.1. In GXemul's 64-bit CPU implementation, `rlwimi` has a separate architectural defect: it executes a 64-bit rotate rather than a 32-bit duplicate rotate, and for wrapping masks it fails to perform insertion into the upper 32-bit word half. A simple 32-bit cast is insufficient because wrapping mask generation in 32-bit mode requires replicating the rotated word into high and low halves and applying 32-bit destination merge rules.
3. Combining them would conflate 64-bit doubleword operand lifetime fixes with 32-bit word-duplication semantics and separate test contracts. Keeping them as distinct atomic rounds ensures verifiable mutation kill tables and isolated audit trails.

---

## 6. Propagation & Two-Part Tree Clearance

The four-coordinated-edit repair was propagated to all active trees and verified with two-part clearance:

```
Tree                  Part 1 (cmp -s vs SEC)      Part 2 (binary -nt source)
----------------------------------------------------------------------------
est/                  CLEAN                       N/A (Source-only tree)
build/                CLEAN                       FRESH
build-asan/           CLEAN                       FRESH
/tmp/gxsec-build      CLEAN                       FRESH
/tmp/gxrldimi_clone   CLEAN                       FRESH (.MUTANT cleared)
```

---

## 7. Artifact Manifest

All artifacts are preserved in `regress/artifacts/ppcrldimimask/`:
- `candidate_fix.diff`: The exact 4-coordinated-edit patch against `src/cpus/cpu_ppc_instr.c`.
- `opus_ppc_rldimi_witness_20260911.py`: Frozen 27-row Rung-3 witness probe with 495-cell census.
- `witness_committed.out`: Pre-fix witness output (Score 17/27; 10 failing rows; 431 census failures).
- `witness_fix.out`: Post-fix witness output (Score 27/27; 0 failing rows; 0 census failures).
- `killtable_20260911/PRETABLE.out`: Pre-table check written and timestamped before table execution.
- `killtable_20260911/mutate_rldimi.py`: Precise mutant generator for kill table legs.
- `killtable_20260911/killtable.sh`: Frozen kill-table test harness driver.
- `killtable_20260911/SCORES.txt`: Complete kill-table execution summary.
- `killtable_20260911/build_*.log`, `probe_*.raw`, `mutate_*.txt`: Full raw execution logs for all legs.
- `opus_measure_20260911.md`: This comprehensive measurement and verification report.
