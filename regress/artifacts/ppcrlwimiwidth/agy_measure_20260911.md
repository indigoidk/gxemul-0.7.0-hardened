VERDICT: CLOSED_BY_TWO_PART_REPAIR
AGY38_RLWIMI_20260911
HEAD: `8d372aa`

# ppcrlwimiwidth MEASUREMENT AND REPAIR REPORT -- 2026-09-11

## 1. Executive Summary

This report delivers the complete diagnosis, witness proof, two-part repair, multi-tree propagation, two-part clearance, and frozen kill-table verification for the PowerPC `rlwimi` (Rotate Left Word Immediate then Mask Insert) instruction defect (`ppcrlwimiwidth`) in GXemul (`GXEMUL-SEC`).

- **Target Source**: `src/cpus/cpu_ppc_instr.c`, function `X(rlwimi)`
- **Root Cause**:
  1. *Width Contamination*: `MODE_uint_t` is `uint64_t` in the 64-bit compilation. In `tmp = sh ? ((tmp << sh) | (tmp >> (32-sh))) : tmp;`, `tmp >> (32-sh)` executes a 64-bit shift when `1 <= SH <= 31`, dragging upper 32-bit source bits down into the lower word.
  2. *Missing High-Half Insertion*: PowerPC Book I defines `ROTL32` as duplicating the low word into both 32-bit halves (positions 0:31 and 32:63). The mask `MASK(MB+32, ME+32)` wraps when `MB > ME`, covering every bit in positions 0..31 (the entire upper half). When `MB > ME`, the destination register `RA` must have its upper 32 bits replaced by the rotated low-word data; the unpatched code preserved `ra`'s upper half unconditionally.
- **Repair**:
  1. Cast source read to `uint32_t`: `uint32_t tmp = (uint32_t)reg(ic->arg[0]);`
  2. High-half replacement before the walk loop:
     ```c
     if (mb > me)
         ra = (ra & 0xffffffffULL) | ((uint64_t)tmp << 32);
     ```
  3. Precedence confirmation: The conditional MUST precede the walk loop because the loop terminates when `mb == me`; if placed after the loop, `mb > me` is never true.
- **Witness Results**:
  - Committed Build (`HEAD`): **14/28** (14 failing rows; 93/129 census failures)
  - Repaired Build (`BASE`): **28/28** (0 failing rows; 0/129 census failures)
- **Kill Table**: 9 legs executed in scratch clone `/tmp/gxrlwimi_clone`, all mutants definitively killed, two-part clearance verified, clone-local `.MUTANT` sentinel cleared.

---

## 2. Technical Breakdown of the Defect

### 2.1 The Architectural Contract
According to PowerPC Architecture Book I (v2.01, §3.3.12.1, p. 4008; §3.3.4.1, p. 4310) and PEM (§8.4.1.49):
For `rlwimi RA, RS, SH, MB, ME`:
1. `n <- SH`
2. `r <- ROTL32((RS)[32:63], n)`
3. `m <- MASK(MB+32, ME+32)`
4. `RA <- (r & m) | ((RA) & ~m)`

Key architectural definitions:
- **`ROTL32`**: The value rotated consists of two copies of bits 32:63 of `RS`, one copy in bits 0:31 and the other in bits 32:63 (Book I:4008).
- **`MASK(MB+32, ME+32)`**: Generates 1-bits from `MB+32` through `ME+32` (wrapping if `MB+32 > ME+32`) and 0s elsewhere (Book I:578).
- When `MB <= ME`: `MB+32 <= ME+32`. The mask covers a continuous range within positions 32..63. Positions 0..31 (high half) are 0s. Destination bits 0..31 are preserved.
- When `MB > ME`: `MB+32 > ME+32`. The mask wraps from bit 63 to bit 0. It covers bits `MB+32..63` and bits `0..ME+32`. Because `ME >= 0`, `ME+32 >= 32`, so positions 0..31 are completely covered by 1-bits. Consequently, `RA`'s high 32 bits MUST be replaced by `r`'s high 32 bits (the rotated low word `tmp`).

### 2.2 The Committed Implementation Flaws
In `GXEMUL-SEC/src/cpus/cpu_ppc_instr.c`:
```c
X(rlwimi)
{
	MODE_uint_t tmp = reg(ic->arg[0]), ra = reg(ic->arg[1]);
	uint32_t iword = ic->arg[2];
	int sh = (iword >> 11) & 31;
	int mb = (iword >> 6) & 31;
	int me = (iword >> 1) & 31;   
	int rc = iword & 1;

	tmp = sh ? ((tmp << sh) | (tmp >> (32-sh))) : tmp;

	for (;;) {
		uint64_t mask;
		mask = (uint64_t)1 << (31-mb);
		ra &= ~mask;
		ra |= (tmp & mask);
		if (mb == me)
			break;
		mb ++;
		if (mb == 32)
			mb = 0;
	}
	reg(ic->arg[1]) = ra;
	if (rc)
		update_cr0(cpu, ra);
}
```

1. **Width Contamination**: In 64-bit mode, `tmp` was declared `MODE_uint_t` (`uint64_t`). For `1 <= sh <= 31`, `tmp >> (32-sh)` shifted the high 32 bits of `rS` down into the low 32 bits, corrupting the rotated value. Siblings `rlwinm` and `rlwnm` cast to `uint32_t` first; `rlwimi` did not.
2. **Missing High-Half Insertion**: In the bit loop, `mask = (uint64_t)1 << (31-mb)`. Since `0 <= mb <= 31`, `mask` only ever touched bits 0..31 of `ra` (the low word). The high 32 bits of `ra` were never updated, leaving `ra`'s high half untouched even when `mb > me`.

---

## 3. Rung-3 Witness Probe (`agy_ppc_rlwimi_witness_20260911.py`)

The witness probe runs directly on unmodified `-E bareppc -M 64` (PPC970, 64-bit CPU model). It tests:
- Controls: harness liveness (`li`), register sentinel hold, `rS` integrity, disassembler cross-check, sibling `rlwinm` control, negative apparatus, and 32-bit PPC603 reachability.
- Defect 1: Width contamination across non-wrapping masks with `1 <= SH <= 31` and differing source halves.
- Defect 2: Missing high-half insertion across wrapping masks (`MB > ME`), including the brief test vector (`rlwimi r4,r3,0,31,0`).
- Both defects combined: `SH > 0` with `MB > ME`.
- Register Aliasing: `RA == RS` self-insertion under non-wrapping, wrapping, and combined encodings.
- Record form: `rlwimi.` with `Rc=1` updating condition register `CR0`.
- Comprehensive parameter sweep census: 129 parameter cells across all four quadrants and diagonals.

### Witness Results Comparison

```
Row                 Committed Build (HEAD)   Repaired Build (BASE)    Architectural Want       Status
-----------------------------------------------------------------------------------------------------
session             exit0                    exit0                    exit0                    ok
live                0x1234                   0x1234                   0x1234                   ok
seed holds          0x5a5a5a5a5a5a5a5a       0x5a5a5a5a5a5a5a5a       0x5a5a5a5a5a5a5a5a       ok
src intact          0xdeadbeefcafef00d       0xdeadbeefcafef00d       0xdeadbeefcafef00d       ok
disasm xcheck       3/3                      3/3                      3/3                      ok
ctl rlwinm          0xcafef00d               0xcafef00d               0xcafef00d               ok
neg apparatus       exit1/-0x1               exit1/-0x1               exit1/-0x1               ok
bits32 live         0x1234                   0x1234                   0x1234                   ok
bits32 rlwimi       0xfef00dca               0xfef00dca               0xfef00dca               ok
nowrap sh0          0xcafef00d               0xcafef00d               0xcafef00d               ok
nowrap sh8 mb0      0xfffe0000 (FAIL)        0xfef00000               0xfef00000               FIXED
nowrap sh16 mb8     0xefca00 (FAIL)          0xdca00                  0xdca00                  FIXED
nowrap sh4 mb16     0xeefc (FAIL)            0xdc                     0xdc                     FIXED
wrap mutant         0x5a5a5a5a5a5a5a5b (FAIL)0xf5a5a5a5b              0xf5a5a5a5b              FIXED
wrap sh0 mb24       0x5a5a5a5a005a5a0f (FAIL)0xf005a5a0f              0xf005a5a0f              FIXED
wrap sh8 mb20       0x5a5a5a5aaaba5f00 (FAIL)0xf00001a5f00            0xf00001a5f00            FIXED
wrap sh16 mb28      0x5a5a5a5aaa5a5a50 (FAIL)0xf0000025a5a50          0xf0000025a5a50          FIXED
pres nowrap         0x5a5a5a5afffe5a5a (FAIL)0x5a5a5a5afef05a5a       0x5a5a5a5afef05a5a       FIXED
pres wrap           0x5a5a5a5acada5a0d (FAIL)0xcafef00dcada5a0d       0xcafef00dcada5a0d       FIXED
wrap fullword       0x5a5a5a5acafef00d (FAIL)0xcafef00dcafef00d       0xcafef00dcafef00d       FIXED
alias nowrap        0xdeadbeeffffef00d (FAIL)0xdeadbeeffef0f00d       0xdeadbeeffef0f00d       FIXED
alias wrap          0xdeadbeefcafef00d (FAIL)0xcafef00dcafef00d       0xcafef00dcafef00d       FIXED
alias both          0xdeadbeefeffefefc (FAIL)0xafef00dcaffef0dc       0xafef00dcaffef0dc       FIXED
cr0 record form     exit0                    exit0                    exit0                    ok
disasm total        146/146                  146/146                  146/146                  ok
census run          129                      129                      129                      ok
census wrong        93 (FAIL)                0                        0                        FIXED
census zero         0                        0                        0                        ok
-----------------------------------------------------------------------------------------------------
TOTAL SCORE         14/28                    28/28                    28/28                    CLEAN SWEEP
```

---

## 4. Multi-Tree Propagation & Two-Part Clearance

The repair was propagated to all build and source trees in accordance with the brief:

```
Tree                   Part 1 (cmp -s vs SEC)    Part 2 (binary -nt source)
---------------------- ------------------------- -------------------------
est/                   CLEAN                     N/A (Source tree)
build/                 CLEAN                     FRESH
build-asan/            CLEAN                     FRESH
/tmp/gxsec-build       CLEAN                     FRESH
```

---

## 5. Frozen Kill Table Verification

Executed in scratch clone `/tmp/gxrlwimi_clone` with clone-local `.MUTANT` sentinel dropped before table 1 and removed only after two-part clearance verification. `PRETABLE.out` was written prior to table execution.

### Kill Table Summary (`SCORES.txt`)

| Leg | Mutation Description | Score | Result | Distinguishing Failures |
|---|---|:---:|:---:|---|
| **BASE** | Full candidate repair | **28/28** | **PASS** | *(None)* |
| **M_REV_COND** | Inverted condition: `if (mb < me)` | **13/28** | **KILLED** | `wrap mutant`, `wrap sh0 mb24`, `wrap sh8 mb20`, `pres wrap`, `alias wrap`, census (15 failing) |
| **M_ONLY_CAST** | Only cast `(uint32_t)`, high-half omitted | **19/28** | **KILLED** | `wrap mutant`, `wrap sh0 mb24`, `wrap sh8 mb20`, `pres wrap`, `alias wrap`, census (9 failing) |
| **M_ONLY_HIGH** | Only high-half write, cast omitted | **19/28** | **KILLED** | `nowrap sh8 mb0`, `nowrap sh16 mb8`, `nowrap sh4 mb16`, `pres nowrap`, `alias nowrap`, census (9 failing) |
| **M_POST_LOOP** | Ordering mutant: `if (mb > me)` after loop | **19/28** | **KILLED** | `wrap mutant`, `wrap sh0 mb24`, `wrap sh8 mb20`, `pres wrap`, `alias wrap`, census (9 failing) |
| **M_ORIG** | Committed implementation (`MODE_uint_t`, no high write) | **14/28** | **KILLED** | Both width contamination and missing high-half rows (14 failing) |
| **HEAD** | Whole-file pre-fix checkout (`8d372aa`) | **14/28** | **KILLED** | Identical failure profile to M_ORIG (14 failing) |
| **NULL_MEDIUM** | Unmutated base control pass | **28/28** | **PASS** | *(None)* |
| **RESTORED** | Restored baseline from SEC | **28/28** | **PASS** | *(None)* |

### Sentinel Clearance Receipt
```
=== CLEARANCE & SENTINEL REMOVAL ===
  Clearance: Part 1 (cmp vs SEC)=CLEAN  Part 2 (binary -nt source)=FRESH
  SENTINEL CLEARED: /tmp/gxrlwimi_clone/.MUTANT removed
KILLTABLE_DONE
```

---

## 6. Answers to Brief's Technical Questions

### 6.1 Does the 32-bit compilation stay byte-identical?
**Measurement**:
In `src/cpus/cpu_ppc.c` (via `tmp_ppc_tail.c`), `cpu_ppc_instr.c` is included twice. The second inclusion compiles under `DYNTRANS_DUALMODE_32`, where `MODE_uint_t` is `uint32_t`, generating `ppc32_instr_rlwimi`.
We extracted and compared the disassembly of `ppc32_instr_rlwimi` in `cpu_ppc.o` between the pre-fix HEAD and post-fix builds:
1. **Instruction body**:
   From function entry (`0x15950`) through the entire rotate, mask calculation, bit loop, and register writeback (`0x15950` to `0x15a5f`, 92 instructions / 272 bytes), the machine code is **100% BYTE-IDENTICAL**.
2. **Compiler Optimization Mechanism**:
   In 32-bit compilation, `ra` is `uint32_t`. In `ra = (ra & 0xffffffffULL) | ((uint64_t)tmp << 32);`, `((uint64_t)tmp << 32)` has all 32 low bits as 0. When assigned to `uint32_t ra`, the upper 32 bits are truncated away by C unsigned assignment semantics: `(uint32_t)((uint64_t)tmp << 32) == 0`.
   Thus `(uint32_t)((ra & 0xffffffffULL) | ((uint64_t)tmp << 32)) == ra`.
   GCC optimizes the entire statement `if (mb > me) ra = ra;` away as a complete no-op.
3. The only single instruction difference in the entire object symbol was an operand register inversion in commutative equality comparison `cmp %esi,%eax` vs `cmp %eax,%esi` inside the `update_cr0` inline expansion at offset `0x15a62` prior to `setne %dl` (which evaluates identically for either operand order).

### 6.2 Register Aliasing (`RA == RS`)
**Analysis and Measurement**:
1. In `X(rlwimi)`:
   `uint32_t tmp = (uint32_t)reg(ic->arg[0]);`
   `MODE_uint_t ra = reg(ic->arg[1]);`
   `reg(ic->arg[1]) = ra;`
   Because `RS` and `RA` are read into local variables `tmp` and `ra` before any rotation or masking occurs, host register aliasing does not introduce read-after-write data hazards during execution.
2. However, architecturally, when `RA == RS`, the instruction performs in-place modification of `RA`. Both defect axes manifest distinctly when `RA == RS`:
   - *Width Contamination*: If `RA` has non-zero bits in bits 0..31, `tmp >> (32-sh)` contaminated `RA`'s low word with high-half bits of itself.
   - *Missing High Half*: If `MB > ME`, `RA`'s high half was preserved as its previous high half instead of being overwritten with `ROTL32(RA[32:63], sh)`.
3. Dedicated witness probe rows confirm this behavior:
   - `alias nowrap`: `RA == RS`, `SH=8, MB=0, ME=15` -> failed pre-fix (`0xdeadbeeffffef00d` vs `0xdeadbeeffef0f00d`), passes post-fix.
   - `alias wrap`: `RA == RS`, `SH=0, MB=31, ME=0` -> failed pre-fix (`0xdeadbeefcafef00d` vs `0xcafef00dcafef00d`), passes post-fix.
   - `alias both`: `RA == RS`, `SH=4, MB=20, ME=10` -> failed pre-fix (`0xdeadbeefeffefefc` vs `0xafef00dcaffef0dc`), passes post-fix.

---

## 7. Artifact Manifest

All artifacts are preserved in `regress/artifacts/ppcrlwimiwidth/`:
- `candidate_fix.diff`: The exact two-part patch applied to `src/cpus/cpu_ppc_instr.c`.
- `agy_ppc_rlwimi_witness_20260911.py`: Frozen 28-row Rung-3 witness probe with 129-cell census.
- `witness_committed.out`: Pre-fix witness output (Score 14/28; 14 failing rows; 93 census failures).
- `witness_fix.out`: Post-fix witness output (Score 28/28; 0 failing rows; 0 census failures).
- `check_clearance.sh`: Multi-tree two-part clearance verification script.
- `killtable_20260911/PRETABLE.out`: Timestamped pre-table verification written before table 1.
- `killtable_20260911/mutate_rlwimi.py`: Precise mutant generator for kill table legs.
- `killtable_20260911/killtable.sh`: Kill-table test harness driver.
- `killtable_20260911/SCORES.txt`: Complete kill-table execution log and score receipt.
- `killtable_20260911/build_*.log`, `probe_*.raw`, `mutate_*.txt`: Raw build, mutation, and probe logs for all 9 legs.
- `agy_measure_20260911.md`: This comprehensive measurement, verification, and clearance report.
- `regress/ppc_rlwimi_probe.py`: Canonical probe script in `regress/`.
