# ppcrlwimiwidth NULL-MEDIUM KILL-TABLE LEG & VACUITY-FLOOR REPORT -- 2026-09-11

## 1. Overview and Floor Breach Closure

Vacuity-floor clause (c) requires test instruments to fail when evaluated against a **null medium** -- an implementation carrying none of the behaviour under test, proving that passing rows observe actual instruction behaviour rather than passing by construction or apparatus bias.

In the initial kill-table run (`regress/artifacts/ppcrlwimiwidth/killtable_20260911/SCORES.txt`), the leg labeled `NULL_MEDIUM` was implemented in `mutate_rlwimi.py:179` as:
```python
if leg in ("BASE", "NULL_MEDIUM", "RESTORED"):
    replacement = FIXED_BLOCK
```
`NULL_MEDIUM` compiled byte-identical code to `BASE` and `RESTORED`, scoring 28/28 solely because it was an unmutated third copy of the base leg under a misleading name. This constituted an L2 vacuity-floor clause (c) breach.

This work repairs the breach in-round:
1. Implements the honest null medium for `X(rlwimi)` as an identity body (decodes and retires, but performs zero insertion into the destination register).
2. Executes the leg in scratch clone `/tmp/gxrlwimi_clone` under strict house rules (clone-local `.MUTANT` sentinel, Gentoo WSL, binary freshness verification, two-part clearance before sentinel removal).
3. Records all artifacts under `regress/artifacts/ppcrlwimiwidth/killtable_nullmedium_20260911/`.
4. Enters an explicit correction into `regress/artifacts/ppcrlwimiwidth/killtable_20260911/SCORES.txt` quoting what it refutes without overwriting historical records.
5. Provides an exhaustive census of all 28 rows under the null medium, proving every row observing `rlwimi` went RED.

---

## 2. Null-Medium Design for `X(rlwimi)`

### Function Body in `src/cpus/cpu_ppc_instr.c`
```c
X(rlwimi)
{
	/*  NULL MEDIUM: decode and retire, insert nothing.  */
	MODE_uint_t ra = reg(ic->arg[1]);
	uint32_t iword = ic->arg[2];
	int rc = iword & 1;

	reg(ic->arg[1]) = ra;
	if (rc)
		update_cr0(cpu, ra);
}
```

### Architectural & Engineering Rationale:
1. **Zero Insertion / Pure Identity**: `ra` is loaded from destination `reg(ic->arg[1])` and written back unmodified via `reg(ic->arg[1]) = ra;`. No bits from source register `rS` (`ic->arg[0]`) are shifted, rotated, masked, or inserted.
2. **Preservation of `rc` / `update_cr0` Axis**: `rc = iword & 1` and `if (rc) update_cr0(cpu, ra);` are retained. This preserves condition register CR0 update behaviour on `rlwimi.`, isolating the test to the data-insertion axis without introducing confounding failures from disabled CR0 updates.
3. **Clean Warning-Free Compilation**: Variables `ra`, `iword`, `rc`, and function parameters `cpu`, `ic` are all utilized, ensuring zero compiler warnings under `-Wall -Werror`.

---

## 3. Kill-Table Measurement Receipt (`killtable_nullmedium_20260911`)

Executed in scratch clone `/tmp/gxrlwimi_clone` using the frozen instrument `agy_ppc_rlwimi_witness_20260911.py`.

```
ppcrlwimiwidth NULL_MEDIUM (IDENTITY) LEG   2026-09-11T06:28:11Z
clone=/tmp/gxrlwimi_clone  baseline=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/cpu_ppc_instr.c (GXEMUL-SEC, the repo source)
probe=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/ppcrlwimiwidth/agy_ppc_rlwimi_witness_20260911.py  (frozen copy -- one instrument for every leg)

SENTINEL DROPPED: /tmp/gxrlwimi_clone/.MUTANT

=== LEG NULL_MEDIUM ===
  mutate rc=0 : MUTATION NULL_MEDIUM: successfully applied
  build rc=0  binary=FRESH
  probe rc=0  sentinel=1
  SCORE 12/28  elapsed=0.1s  binary=/tmp/gxrlwimi_clone/gxemul  label=NULL_MEDIUM
  FAILING: bits32 rlwimi, nowrap sh0, nowrap sh8 mb0, nowrap sh16 mb8, nowrap sh4 mb16, wrap mutant, wrap sh0 mb24, wrap sh8 mb20, wrap sh16 mb28, pres nowrap, pres wrap, wrap fullword, alias nowrap, alias wrap, alias both, census wrong

=== LEG RESTORED ===
  mutate rc=0 : MUTATION RESTORED: successfully applied
  build rc=0  binary=FRESH
  probe rc=0  sentinel=1
  SCORE 28/28  elapsed=0.0s  binary=/tmp/gxrlwimi_clone/gxemul  label=RESTORED
  FAILING: 

=== CLEARANCE & SENTINEL REMOVAL ===
  Clearance: Part 1 (cmp vs SEC)=CLEAN  Part 2 (binary -nt source)=FRESH
  SENTINEL CLEARED: /tmp/gxrlwimi_clone/.MUTANT removed
NULLMEDIUM_DONE
```

---

## 4. Comprehensive Row-by-Row Census Under Null Medium

Score: **12/28** (12 PASS, 16 FAIL).

### 4.1 Surviving Rows (12/12 GREEN) -- Analysis of Legitimacy

| Row | Got | Want | Classification | Rationale |
|---|---|---|---|---|
| `session` | `exit0` | `exit0` | Harness Control | Verifies control session executes to completion (`quit`). Does not invoke `rlwimi`. |
| `live` | `0x1234` | `0x1234` | Harness Control | Evaluates `li r9,0x1234` to verify host can read back guest register state. Does not invoke `rlwimi`. |
| `seed holds` | `0x5a5a5a5a5a5a5a5a` | `0x5a5a5a5a5a5a5a5a` | Harness Control | Verifies un-targeted register `r30` preserves pre-seeded sentinel value. |
| `src intact` | `0xdeadbeefcafef00d` | `0xdeadbeefcafef00d` | Harness Control | Verifies source register `r3` (`rS`) is not modified by instruction side effects. |
| `disasm xcheck` | `3/3` | `3/3` | Disassembly Control | Confirms emulator disassembler matches encoder on control instructions (`li`, `nop`, `rlwinm`). |
| `ctl rlwinm` | `0xcafef00d` | `0xcafef00d` | Sibling Control | Differential negative control executing sibling instruction `rlwinm` (extract low word). |
| `neg apparatus` | `exit1/-0x1` | `exit1/-0x1` | Apparatus Control | Verifies invalid machine `nosuchmachine` fails fast and does not produce false-positive passes. |
| `bits32 live` | `0x1234` | `0x1234` | Architecture Control | Verifies 32-bit CPU model (`PPC603`) harness liveness (`li r9,0x1234`). |
| `cr0 record form` | `exit0` | `exit0` | CR0 Axis Control | Checks that `rlwimi.` (`Rc=1`) executes and register dump contains `cr` without crashing. Retained `update_cr0` handles this legitimately. |
| `disasm total` | `146/146` | `146/146` | Disassembly Accounting | Verifies emulator disassembler parses all 146 placed words. Instruction disassembly is independent of execution semantics. |
| `census run` | `129` | `129` | Census Accounting | Verifies all 129 scheduled `(SH,MB,ME)` parameter combinations completed without hang or emulator crash. |
| `census zero` | `0` | `0` | Anomaly Detection | Detects illegal register wipe to 0. Destination registers were pre-seeded with sentinel `0x5A5A5A5A5A5A5A5A` and retain it, so 0 cells wipe to 0. |

**Verdict on Surviving Rows**: **ALL 12 SURVIVING ROWS ARE NON-VACUOUS.** They comprise 8 harness/architecture controls, 1 sibling instruction control, 1 CR0 liveness check, 1 disassembler accounting check, and 1 zero-wipe anomaly detector. Not one surviving row asserts `rlwimi` data transformation semantics.

---

### 4.2 Failing Rows (16/16 RED) -- Every `rlwimi` Semantic Row Goes Red

| Row | Got | Want | Status | Observed Defect Axis Under Identity Body |
|---|---|---|:---:|---|
| `bits32 rlwimi` | `0x5a5a5a5a` | `0xfef00dca` | **FAIL (RED)** | 32-bit execution: destination unchanged (`SENT`), zero insertion occurred. |
| `nowrap sh0` | `0x0` | `0xcafef00d` | **FAIL (RED)** | Non-wrapping, SH=0: destination seeded to 0, zero insertion occurred. |
| `nowrap sh8 mb0` | `0x0` | `0xfef00000` | **FAIL (RED)** | Non-wrapping, SH=8: destination seeded to 0, zero insertion occurred. |
| `nowrap sh16 mb8` | `0x0` | `0xdca00` | **FAIL (RED)** | Non-wrapping, SH=16: destination seeded to 0, zero insertion occurred. |
| `nowrap sh4 mb16` | `0x0` | `0xdc` | **FAIL (RED)** | Non-wrapping, SH=4: destination seeded to 0, zero insertion occurred. |
| `wrap mutant` | `0x5a5a5a5a5a5a5a5a` | `0xf5a5a5a5b` | **FAIL (RED)** | Wrapping brief mutant `(31,0)`: destination retains `SENT`, no high/low insertion. |
| `wrap sh0 mb24` | `0x5a5a5a5a5a5a5a5a` | `0xf005a5a0f` | **FAIL (RED)** | Wrapping `(24,8)`, SH=0: destination retains `SENT`, no insertion. |
| `wrap sh8 mb20` | `0x5a5a5a5a5a5a5a5a` | `0xf00001a5f00` | **FAIL (RED)** | Wrapping `(20,10)`, SH=8: destination retains `SENT`, no insertion. |
| `wrap sh16 mb28` | `0x5a5a5a5a5a5a5a5a` | `0xf0000025a5a50` | **FAIL (RED)** | Wrapping `(28,4)`, SH=16: destination retains `SENT`, no insertion. |
| `pres nowrap` | `0x5a5a5a5a5a5a5a5a` | `0x5a5a5a5afef05a5a` | **FAIL (RED)** | Destination preservation non-wrapping: no bits inserted into low half. |
| `pres wrap` | `0x5a5a5a5a5a5a5a5a` | `0xcafef00dcada5a0d` | **FAIL (RED)** | Destination preservation wrapping: no bits inserted into either half. |
| `wrap fullword` | `0x5a5a5a5a5a5a5a5a` | `0xcafef00dcafef00d` | **FAIL (RED)** | Full-word wrapping mask `(1,0)`: no bits replaced. |
| `alias nowrap` | `0xdeadbeefcafef00d` | `0xdeadbeeffef0f00d` | **FAIL (RED)** | `RA == RS` non-wrapping: register retains initial `RS_VAL` unaltered. |
| `alias wrap` | `0xdeadbeefcafef00d` | `0xcafef00dcafef00d` | **FAIL (RED)** | `RA == RS` wrapping: register retains initial `RS_VAL` unaltered. |
| `alias both` | `0xdeadbeefcafef00d` | `0xafef00dcaffef0dc` | **FAIL (RED)** | `RA == RS` wrapping with shift: register retains initial `RS_VAL` unaltered. |
| `census wrong` | `126` | `0` | **FAIL (RED)** | 126 of 129 sweep combinations differ from expected architectural result. |

---

## 5. Vacuity Floor Clause (c) Clearance

Vacuity floor clause (c) mandates that the test instrument must fail on a null medium carrying none of the behaviour under test, proving that passing rows observe genuine instruction functionality rather than vacuous tautologies.

- **16 of 16** rows that observe `rlwimi` functionality turn **RED**.
- **0** rows observing `rlwimi` functionality survive.
- The **12** surviving rows are completely accounted for as non-vacuous apparatus controls, sibling instruction controls, and accounting/shape checks.
- **Clause (c) is completely discharged.**

---

## 6. SCORES.txt Correction Receipt

In `regress/artifacts/ppcrlwimiwidth/killtable_20260911/SCORES.txt`:
```
=== LEG NULL_MEDIUM ===
  mutate rc=0 : MUTATION NULL_MEDIUM: successfully applied
  build rc=0  binary=FRESH
  probe rc=0  sentinel=1
  SCORE 28/28  elapsed=0.1s  binary=/tmp/gxrlwimi_clone/gxemul  label=NULL_MEDIUM
  FAILING: 
  CORRECTION (2026-09-11): Leg above ("SCORE 28/28 ... label=NULL_MEDIUM") was byte-identical to BASE/RESTORED (third copy of base leg, not a null medium). Honest identity null medium measured at killtable_nullmedium_20260911: SCORE 12/28 (all 16 rlwimi-observing rows RED).
```

Historical records are preserved without silent overwrite, and the true null-medium measurement is formally recorded.
