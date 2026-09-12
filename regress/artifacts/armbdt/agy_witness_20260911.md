VERDICT:
AGY38_ARMBDT_20260911
HEAD: `8d372aa`

# Witness and Verification Report: ARM Block Data Transfer (`armbdt`) Unaligned Address Defect

## 1. Executive Summary

- **Target Defect**: Unaligned base register addresses in ARM Block Data Transfer operations (`LDM`, `STM`, and Thumb `POP`/`PUSH`) cause silent memory corruption or incorrect register loads on cold host pages.
- **Root Cause**: Located in `src/cpus/cpu_arm_instr.c` within `arm_pop()` (:1653) and `arm_push()` (:1842).
  - When the host page is resident in the GXemul cache (`page != NULL`), the fast path computes `p32[(addr & 0xfff) >> 2]`. The right-shift by 2 drops bits `[1:0]`, which is architecturally conformant with ARM DDI 0100I (Section A4-37 for LDM(1), Section A4-190 for STM(1)).
  - When the host page is cold / unmapped (`page == NULL`), execution enters the slow fallback path calling `cpu->memory_rw()`. GXemul passed the **raw, unmasked `addr`** to `memory_rw`.
  - In `src/memory_rw.c` (:728-782), `offset = paddr & offset_mask` is computed at page granularity rather than word-aligned granularity, and raw `memcpy` transfers bytes directly across architectural word boundaries.
- **The Core Symptom**: The identical instruction operating on the exact same unaligned address yields **different byte values** depending on host page cache warmth—a software-invisible condition.
- **The Fix Shape & Entry-Mask Trap**:
  - The correct fix masks strictly at the two slow-path `memory_rw` call sites:
    ```c
    cpu_arm_instr.c:1653:
    if (!cpu->memory_rw(cpu, cpu->mem, addr & ~3, data, sizeof(data), MEM_READ, CACHE_DATA))

    cpu_arm_instr.c:1842:
    if (!cpu->memory_rw(cpu, cpu->mem, addr & ~3, data, sizeof(data), MEM_WRITE, CACHE_DATA))
    ```
  - **Never mask at function entry**: Mode 4 writeback (`if (w_bit) *np = addr;` at :1715 and :1858) updates the base register with the unmasked arithmetic progression. Masking at function entry (`addr = *np & ~3`) corrupts the final base register value. In-tree precedent in `src/cpus/generate_arm_multi.c:117` confirms that access masking (`addr &= 0xffc;`) must remain separated from base register writeback.
- **Results Summary**:
  - Pre-fix committed HEAD (`8d372aa`): **17 / 25** (all 4 cold data rows and all 4 divergence checks fail).
  - Post-fix candidate build (`BASE`): **25 / 25** (clean pass across all 25 rows).
  - Mutant kill table: All mutants (`HEAD`, `M_ENTRY`, `M_POP_ONLY`, `M_PUSH_ONLY`, `M_NULL_MEDIUM`) decisively killed. `M_ENTRY` is killed specifically by the mandatory writeback rows.
  - Two-part restoration verified clean in scratch clone (`/tmp/gxarmbdt_clone`).

---

## 2. Witness Design & Test Environment

- **Machine & Mode**: Unmodified in-tree ARM machine `testarm` (`gxemul -V -A -T -E testarm -M 64`). No custom devices or synthetic configurations were added.
- **Witness Level**: Rung 3 cold interactive debugger witness. Commands and binary code injections are driven via a Unix pseudoterminal (`pty`), querying machine state and CPU registers directly from the debugger prompt.
- **Page Cache Conditioning**:
  - Cold page seeding: Debugger `put b <addr> <val>` writes byte-by-byte with flags `CACHE_NONE | NO_EXCEPTIONS`. This populates physical RAM without updating GXemul's internal CPU translation tables (`host_load` and `host_store` remain unmapped/NULL).
  - Warm page seeding: Debugger `put w <addr> <val>` writes 32-bit words with flags `CACHE_DATA`, warming the host page translation cache.
  - Path Verification: Before every test transfer, the witness queries `tlbdump 0,r` to verify that the target address is genuinely absent from the host cache during cold runs and resident during warm runs.
- **Call Sites & Sibling Parity Covered (All 4 Callers)**:
  1. `X(bdt_load)` (`cpu_arm_instr.c:1889`) — ARM Mode 4 LDM
  2. `X(bdt_store)` (`cpu_arm_instr.c:1921`) — ARM Mode 4 STM
  3. Thumb POP (`cpu_arm.c:1677` -> `arm_pop`)
  4. Thumb PUSH (`cpu_arm.c:1670` -> `arm_push`)
- **Dual Controls**:
  - `CONTROL_LIVENESS`: Aligned round-trip block transfer at `0x20000` verifying basic transfer execution (`want 0xcafebabe`).
  - `CONTROL_ATTRIB_PLUS1`: Attribution control asserting the exact predictable spliced byte pattern `0x88112233` produced by cold unaligned read at base `0x20001` (splicing byte `0x11` from `0x20000` and bytes `0x33,0x22` from `0x20004`).
- **Mandatory Writeback Rows**:
  - `ARM_LDM_WB_UNAL1`: Base `0x20001` with 1 register -> asserts writeback `r0 == 0x20005`.
  - `ARM_LDM_WB_UNAL2`: Base `0x20001` with 2 registers -> asserts writeback `r0 == 0x20009`.
  - `ARM_STM_WB_UNAL`: Base `0x21001` with 1 register -> asserts writeback `r0 == 0x21005`.
  - `THUMB_POP_WB_UNAL`: Base `0x22001` with 1 register -> asserts writeback `sp == 0x22005`.
  - `THUMB_PUSH_WB_UNAL`: Base `0x23005` with 1 register (decrement-before) -> asserts writeback `sp == 0x23001`.

---

## 3. Pre-Fix Baseline Measurement (Committed HEAD `8d372aa`)

- **Binary**: `/tmp/gxarmbdt_clone/gxemul` (built clean from unmodified `8d372aa`)
- **Raw Log**: `regress/artifacts/armbdt/witness_committed.out`
- **Total Score**: **17 / 25**

### Row-by-Row Baseline Breakdown

| Row Name | Category | Result | Actual vs Expected |
| :--- | :--- | :---: | :--- |
| `CONTROL_LIVENESS` | Control | **PASS** | `r1 == 0xcafebabe` (aligned round-trip) |
| `CONTROL_ATTRIB_PLUS1` | Control | **PASS** | `cold r1 == 0x88112233` (exact spliced pattern) |
| `ARM_LDM_COLD_DATA` | Data Transfer | **FAIL** | `r1 == 0x88112233` (want `0x44332211`) |
| `ARM_LDM_WARM_DATA` | Data Transfer | **PASS** | `r1 == 0x44332211` |
| `ARM_LDM_PATH_COLD` | Path Audit | **PASS** | `cold page unmapped in host_load` |
| `ARM_LDM_PATH_WARM` | Path Audit | **PASS** | `warm page resident in host_load` |
| `ARM_LDM_DIV_CHECK` | Divergence | **FAIL** | Cold `0x88112233` != Warm `0x44332211` |
| `ARM_LDM_WB_UNAL1` | Writeback | **PASS** | `r0 == 0x20005` (unmasked writeback preserved) |
| `ARM_LDM_WB_UNAL2` | Writeback | **PASS** | `r0 == 0x20009` (unmasked writeback preserved) |
| `ARM_STM_COLD_DATA` | Data Transfer | **FAIL** | `w0 == 0x000000aa` (want `0xaabbccdd`) |
| `ARM_STM_WARM_DATA` | Data Transfer | **PASS** | `w0 == 0xaabbccdd` |
| `ARM_STM_PATH_COLD` | Path Audit | **PASS** | `cold page unmapped in host_store` |
| `ARM_STM_PATH_WARM` | Path Audit | **PASS** | `warm page resident in host_store` |
| `ARM_STM_DIV_CHECK` | Divergence | **FAIL** | Cold `0x000000aa` != Warm `0xaabbccdd` |
| `ARM_STM_COLD_CLOBBER` | Side Effect | **PASS** | Word 1 byte at `0x21004` clobbered by spliced store |
| `ARM_STM_WB_UNAL` | Writeback | **PASS** | `r0 == 0x21005` (unmasked writeback preserved) |
| `THUMB_POP_COLD_DATA` | Thumb Data | **FAIL** | `r1 == 0x88112233` (want `0x44332211`) |
| `THUMB_POP_WARM_DATA` | Thumb Data | **PASS** | `r1 == 0x44332211` |
| `THUMB_POP_DIV_CHECK` | Divergence | **FAIL** | Cold `0x88112233` != Warm `0x44332211` |
| `THUMB_POP_WB_UNAL` | Writeback | **PASS** | `sp == 0x22005` (unmasked writeback preserved) |
| `THUMB_PUSH_COLD_DATA` | Thumb Data | **FAIL** | `w0 == 0x000000aa` (want `0xaabbccdd`) |
| `THUMB_PUSH_WARM_DATA` | Thumb Data | **PASS** | `w0 == 0xaabbccdd` |
| `THUMB_PUSH_DIV_CHECK` | Divergence | **FAIL** | Cold `0x000000aa` != Warm `0xaabbccdd` |
| `THUMB_PUSH_WB_UNAL` | Writeback | **PASS** | `sp == 0x23001` (unmasked writeback preserved) |
| Sentinel check | Lifecycle | **PASS** | `ARMBDT_WITNESS_DONE` emitted |

Pre-fix failing row list:
`FAILING: ARM_LDM_COLD_DATA,ARM_LDM_DIV_CHECK,ARM_STM_COLD_DATA,ARM_STM_DIV_CHECK,THUMB_POP_COLD_DATA,THUMB_POP_DIV_CHECK,THUMB_PUSH_COLD_DATA,THUMB_PUSH_DIV_CHECK`

---

## 4. Post-Fix Measurement (`BASE`)

- **Binary**: `/tmp/gxarmbdt_clone/gxemul` with candidate fix applied
- **Raw Log**: `regress/artifacts/armbdt/witness_fix.out`
- **Total Score**: **25 / 25**
- **Failing Rows**: **None** (`FAILING: none`)
- All 4 cold data rows now read/write the architecturally correct word values (`0x44332211` and `0xaabbccdd`).
- All 4 divergence checks now evaluate to clean parity (`cold == warm`).
- All 5 writeback checks remain green (`r0 == 0x20005`, `0x20009`, `0x21005`; `sp == 0x22005`, `0x23001`).

---

## 5. Mutant Kill Table

Pre-table record `PRETABLE.out` was frozen before table execution. The table was executed in `/tmp/gxarmbdt_clone` with compiler object invalidation (`rm src/cpus/*.o`) and binary freshness validation (`[ gxemul -nt source ]`) on each leg.

| Leg | Description | Score | Status | Kill Rationale / Failing Rows |
| :--- | :--- | :---: | :---: | :--- |
| **`BASE`** | Candidate fix: mask `addr & ~3` at `memory_rw` callsites only | **25/25** | **PASS** | Clean run. All 4 callers green, cold==warm, writebacks unmasked. |
| **`HEAD`** | Committed HEAD `8d372aa`: unmasked `addr` at `memory_rw` callsites | **17/25** | **KILLED** | 8 rows fail: 4 cold data rows + 4 divergence checks. Splicing defect confirmed. |
| **`M_ENTRY`** | Mask-at-entry mutant: `addr = *np & ~3` in `arm_pop`/`arm_push` | **20/25** | **KILLED** | **KILLED BY WRITEBACK.** 5 rows fail (`ARM_LDM_WB_UNAL1`, `ARM_LDM_WB_UNAL2`, `ARM_STM_WB_UNAL`, `THUMB_POP_WB_UNAL`, `THUMB_PUSH_WB_UNAL`). All data rows pass, demonstrating that ONLY the writeback rows can distinguish the proper fix from this defect. |
| **`M_POP_ONLY`** | Fix applied to `arm_pop` only; `arm_push` unmasked | **21/25** | **KILLED** | **KILLED BY STORES.** 4 store rows fail (`ARM_STM_COLD_DATA`, `ARM_STM_DIV_CHECK`, `THUMB_PUSH_COLD_DATA`, `THUMB_PUSH_DIV_CHECK`). |
| **`M_PUSH_ONLY`** | Fix applied to `arm_push` only; `arm_pop` unmasked | **21/25** | **KILLED** | **KILLED BY LOADS.** 4 load rows fail (`ARM_LDM_COLD_DATA`, `ARM_LDM_DIV_CHECK`, `THUMB_POP_COLD_DATA`, `THUMB_POP_DIV_CHECK`). |
| **`M_NULL_MEDIUM`** | Identity null: `arm_pop` and `arm_push` return immediately | **6/25** | **KILLED** | **KILLED BY ALL TRANSFERS.** 19 rows fail, including `CONTROL_LIVENESS`, `CONTROL_ATTRIB_PLUS1`, all data transfers, divergence, and writebacks. Proves every witness row genuinely measures block transfer execution. |
| **`RESTORED`** | Reinstatement of pristine committed HEAD `8d372aa` | **17/25** | **CONFIRMED** | Score and row output byte-for-byte identical to baseline `witness_committed.out`. |

---

## 6. Two-Part Restoration Verification

Following execution of the mutant legs, two-part restoration of the scratch clone was strictly enforced:
1. **Source Restoration**: Pristine `cpu_arm_instr.c` restored from saved baseline.
   - `cmp -s /tmp/gxarmbdt_clone/src/cpus/cpu_arm_instr.c GXEMUL-SEC/src/cpus/cpu_arm_instr.c` evaluated **CLEAN** (exit code 0).
2. **Binary Freshness**: Recompiled with `rm -f src/cpus/*.o && make -j4`.
   - `[ /tmp/gxarmbdt_clone/gxemul -nt /tmp/gxarmbdt_clone/src/cpus/cpu_arm_instr.c ]` evaluated **TRUE**.
3. **Sentinel Removal**:
   - The clone-local `.MUTANT` sentinel was dropped before Leg 1 and remained in place throughout all mutations. It was unlinked **only after** both Part 1 and Part 2 were verified.
4. **Restoration Run**:
   - The `RESTORED` leg was executed against the restored binary and yielded exactly 17/25, matching `witness_committed.out`.

---

## 7. Clause (e) Disclosure of Instrument Limitations

In accordance with project verification standards, the following boundaries of this instrument are disclosed:
1. **Physical Flat RAM Scope**: The witness exercises physical memory mapped into the flat 32-bit address space of the `testarm` machine. It does not exercise MMU page-fault or abort behaviors during unaligned block transfers.
2. **Transfer Length**: The witness specifically isolates 1-register and 2-register transfers to inspect address truncation, byte splicing, and writeback arithmetic. Multi-register transfers spanning across physical page boundaries (4KB transitions) are not explicitly driven.
3. **Privileged Mode Banking**: Mode 4 block transfers with the `S` bit set (`arm_pop`/`arm_push` user register load/store from privileged mode) share the exact same masking logic, but banking mode transitions were not separately exercised.
4. **I/O Device Block Transfers**: Block transfers directed at MMIO device addresses were not tested, as ARM specifications treat block transfers to device registers as unpredictable or architecture violations.

---

## 8. Artifact Inventory

All artifacts are preserved under `regress/artifacts/armbdt/`:
- `agy_witness_20260911.md`: This comprehensive report.
- `agy_armbdt_witness_20260911.py`: Frozen Rung-3 witness probe script.
- `witness_committed.out`: Raw pre-fix baseline log on committed HEAD `8d372aa` (Score 17/25).
- `witness_fix.out`: Raw post-fix candidate log on `BASE` (Score 25/25).
- `killtable_20260911/PRETABLE.out`: Pre-table analysis, claims mapping, and predicted scores.
- `killtable_20260911/mutate_armbdt.py`: Mutation driver script.
- `killtable_20260911/killtable.sh`: Automated kill table runner script with restoration checks.
- `killtable_20260911/SCORES.txt`: Recorded scores across all mutant legs.
- `killtable_20260911/probe_*.raw`: Raw execution logs for all legs (`BASE`, `HEAD`, `M_ENTRY`, `M_POP_ONLY`, `M_PUSH_ONLY`, `M_NULL_MEDIUM`, `RESTORED`).
- `killtable_20260911/KILLTABLE_DONE`: Completion sentinel.
