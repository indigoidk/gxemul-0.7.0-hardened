VERDICT:
AGY38_ALTDIGIN_20260911
HEAD: `8d372aa`

# Witness and Verification Report: WDC Alternate Status / Drive Address Register (`wdcaltdigin`) Read Decode Defect

## 1. Executive Summary

- **Target Defect**: In `src/devices/dev_wdc.c:609`, `DEVICE_ACCESS(wdc_altstatus)` registers a 2-byte region (`wdc_altstatus` at `0x3f6` and Drive Address register at `0x3f7`). In execution order:
  - `idata = data[0];`
  - `odata = status_byte(d, cpu);` (unconditional status calculation, `relative_addr` not consulted)
  - `if (writeflag == MEM_READ) debug(...);`
  - `else if (relative_addr != 0) { ... }` (#494 write-decline arm)
  - `else { ... }` (#481 Alt Ctrl write path)
  - Common tail: `if (writeflag == MEM_READ) data[0] = odata; return 1;`
  `relative_addr` is evaluated in exactly ONE place, strictly inside the `else` of `writeflag == MEM_READ`. As a result, the READ path never decodes its offset. A guest read of offset 1 (`0x3f7` on the PC layout) incorrectly returns the alternate status byte rather than declining the unmapped read.
- **Symmetric Defect & Four-Cell Closure**:
  `#494` repaired the WRITE path at offset 1 (`relative_addr != 0`) to decline stores to `0x3f7` so they do not trigger a soft reset. The READ path remained open in the preceding `if`. This round completes the four-cell table:
  | Cell | Offset 0 (`0x3f6`) | Offset 1 (`0x3f7`) |
  | :--- | :--- | :--- |
  | **WRITE** | Alt Ctrl (#481): `WDCTL_RST` triggers soft reset | Drive Address reg (#494): declined store (no reset) |
  | **READ**  | Alt Status: returns status byte S (S != 0) | Drive Address reg (`wdcaltdigin`): declined read (0x00) |
- **The Ruled Repair**:
  Decode `relative_addr` on the read path while preserving unconditional status calculation, common tail, and `return 1`:
  ```c
  if (writeflag == MEM_READ) {
      if (relative_addr != 0) {
          /*  Declined read convention: emulator policy pre-zeroes
              registered-device read buffers (#95); return 0 here
              for unmapped offset 1 (Drive Address register / digin).  */
          odata = 0;
      } else {
          debug("[ wdc: read from ALTSTATUS: 0x%02x ]\n",
              (int)odata);
      }
  } else if (relative_addr != 0) {
      /*  existing #494 write-decline arm, unchanged  */
  ```
  Zero's warrant is the emulator's deterministic declined-read policy (`#95` pre-zeroes registered-device read buffers) — an emulator convention, not a claim about physical ATA bus float.
- **Results Summary**:
  - Committed HEAD (`8d372aa`): **14 / 16** (both core offset-1 read rows FAIL, returning status byte S).
  - Candidate Fix (`BASE`): **16 / 16** (clean pass across all 16 rows; offset 1 returns 0x00).
  - Measured S Values: `S = 0x51` (power-on) and `S_armed = 0x58` (armed). Strictly non-zero, eliminating the oracle trap.
  - Mutant Kill Table: All mutants (`HEAD`, `M_NULL_EFFECT`, `M_REINSTATE`, `M_NULL_MEDIUM`) decisively killed. `M_NULL_EFFECT` is killed specifically by the non-zero S measurement; `M_NULL_MEDIUM` is killed specifically by the legal offset-0 accept rows.
  - Write behaviors unregressed: Both `#481` (WRITE offset 0 SRST) and `#494` (WRITE offset 1 decline) pass cleanly across all legs.
  - Two-part restoration verified clean in scratch clone `/tmp/gxaltdigin_clone`.

---

## 2. Witness Design & Test Environment

- **Machine & Architecture**: Unmodified in-tree machine `evbmips -e malta` (MIPS 5Kc, Little-endian, 128 MB RAM).
- **Device Registration & Fixture**:
  - PCI PIIX4 IDE (`piix4_ide`) registers `wdc` at ISA port base `0x18000000 + 0x1f0` (KSEG1 `0xffffffffb80001f0`).
  - `wdc_altstatus` registered two bytes wide at `0x18000000 + 0x3f6` (KSEG1 `0xffffffffb80003f6`).
  - Offset 0 (`0x3f6`): Alt Status (read) / Device Control (write).
  - Offset 1 (`0x3f7`): Drive Address register (digin), read-only on PC hardware, not mapped for altstatus.
  - Disk attached via `-d iR:<image>` (8 MB zero image with pid-unique overlay), establishing `diskimage_exist() == true`.
- **Witness Level**: Rung 3 cold interactive debugger witness. Real guest instructions, real address decode, real `memory_rw`. MIPS binary code injected directly at KSEG0 `0xffffffff80100000` via command line. Execution controlled via pseudoterminal (`pty`), verified with disassembly check (`unassemble`), continued to halt breakpoint at `0xffffffff8010016c`, and state inspected via `print <reg>`.
- **The Oracle Trap & Non-Zero S Control**:
  - The clause-(d) mutant `M_NULL_EFFECT` decodes `if (relative_addr != 0)` but omits `odata = 0;`. If S were 0, the mutant and the fix would return the identical byte, rendering the row vacuous.
  - The fixture explicitly establishes and reports non-zero S:
    - At devinit: `dev_wdc_init()` sets `d->error = 1`. With disk attached, `status_byte()` computes `WDCS_DRDY | WDCS_DSC | WDCS_ERR = 0x40 | 0x10 | 0x01 = 0x51`.
    - When armed: `arm_a_write()` issues `WDCC_WRITE` (clearing error and setting `write_in_progress`), yielding `WDCS_DRDY | WDCS_DSC | WDCS_DRQ = 0x40 | 0x10 | 0x08 = 0x58`.
    - Both S values are measured and reported in the log: `0x51` and `0x58`.
- **Dual Rejection of Null Vehicle**:
  - A null medium returning 0 for every read without exercising `wdc` would pass an offset-1 zero check alone.
  - The detector carries legal offset-0 reads (`ACCEPT_READ_OFF0_POWERON` wanting `0x51`, and `ACCEPT_READ_OFF0_ARMED` wanting `0x58`).
  - A null medium fails both accept rows, proving that the test suite discriminates active device decode from trivial zero returns.
- **Write Cell Non-Regression Guard**:
  - Phase W1 (WRITE offset 0): Poking `0x06` (`SRST`) to `0x3f6` asserts `#481` soft reset: DRQ clears to `0x50` and the input ring purges to `0xff`.
  - Phase W2 (WRITE offset 1): Poking `0x06` (`SRST`) to `0x3f7` asserts `#494` write decline: DRQ remains `0x58` and ring bytes remain intact (`0x71`).

---

## 3. Pre-Fix Baseline Measurement (Committed HEAD `8d372aa`)

- **Binary**: `/tmp/gxaltdigin_clone/gxemul` (built clean from unmodified committed HEAD `8d372aa`).
- **Raw Log**: `regress/artifacts/wdcaltdigin/witness_committed.out`.
- **Total Score**: **14 / 16**.
- **Measured Status & Offset-1 Samples**:
  - Power-on Altstatus (offset 0): `S = 0x51` (want `0x51`).
  - Power-on Offset 1 (offset 1): `0x51` (BASE want `0x00`, HEAD defect is `0x51`).
  - Armed Altstatus (offset 0): `S_armed = 0x58` (want `0x58`).
  - Armed Offset 1 (offset 1): `0x58` (BASE want `0x00`, HEAD defect is `0x58`).

### Row-by-Row Baseline Breakdown

| Row Name | Reg | Category | Result | Want | Got | Description |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| `CONTROL_RAM_LIVENESS` | `v0` | Control | **PASS** | `0x55` | `0x55` | RAM byte round-trip |
| `CONTROL_CYL_LO_LIVENESS` | `v1` | Control | **PASS** | `0x55` | `0x55` | `cyl_lo` readback (#481 idiom) |
| `CONTROL_CYL_HI_LIVENESS` | `a0` | Control | **PASS** | `0x66` | `0x66` | `cyl_hi` readback (#481 idiom) |
| `CONTROL_FIFO_DEVSIG_1` | `a1` | Control | **PASS** | `0x5a` | `0x5a` | FIFO data port 1st read |
| `CONTROL_FIFO_DEVSIG_2` | `a2` | Control | **PASS** | `0xa5` | `0xa5` | FIFO data port 2nd read |
| `CONTROL_STATUS_POWERON` | `a3` | Control | **PASS** | `0x51` | `0x51` | Status byte at power-on (+7) |
| `ACCEPT_READ_OFF0_POWERON` | `s0` | Accept | **PASS** | `0x51` | `0x51` | Legal offset-0 read returns S (`0x51 != 0`) |
| `CORE_READ_OFF1_POWERON` | `s1` | Core Defect | **FAIL** | `0x00` | `0x51` | Offset-1 read declined: want `0x00 != S` |
| `CONTROL_STATUS_ARMED` | `s2` | Control | **PASS** | `0x58` | `0x58` | Armed status (+7) has DRQ set (`0x58`) |
| `ACCEPT_READ_OFF0_ARMED` | `s3` | Accept | **PASS** | `0x58` | `0x58` | Legal offset-0 read returns S_armed (`0x58 != 0`) |
| `CORE_READ_OFF1_ARMED` | `s4` | Core Defect | **FAIL** | `0x00` | `0x58` | Offset-1 read armed declined: want `0x00 != S_armed` |
| `WRITE0_SRST_DRQ_CLEAR` | `s5` | Write Guard | **PASS** | `0x50` | `0x50` | `#481`: offset-0 SRST clears DRQ (`0x50`) |
| `WRITE0_SRST_RING_PURGED` | `s6` | Write Guard | **PASS** | `0xff` | `0xff` | `#481`: offset-0 SRST purges ring (`0xff`) |
| `CONTROL_STATUS_ARMED_W2` | `s7` | Control | **PASS** | `0x58` | `0x58` | Re-armed status for Phase W2 (`0x58`) |
| `WRITE1_DECLINE_DRQ_SET` | `t8` | Write Guard | **PASS** | `0x58` | `0x58` | `#494`: offset-1 SRST declined: DRQ set (`0x58`) |
| `WRITE1_DECLINE_RING_INTACT` | `t9` | Write Guard | **PASS** | `0x71` | `0x71` | `#494`: offset-1 SRST declined: byte `0x71` intact |

**Baseline Failing Rows (2)**:
- `CORE_READ_OFF1_POWERON`: want `0x00`, got `0x51` (unconditional status byte leak).
- `CORE_READ_OFF1_ARMED`: want `0x00`, got `0x58` (unconditional armed status byte leak).

---

## 4. Post-Fix Measurement (`BASE`)

- **Binary**: `/tmp/gxaltdigin_clone/gxemul` with ruled repair applied.
- **Raw Log**: `regress/artifacts/wdcaltdigin/witness_fix.out` (and `killtable_20260911/probe_BASE.raw`).
- **Total Score**: **16 / 16** (clean pass across all 16 rows).
- **Measured Values on `BASE`**:
  - Power-on Altstatus (offset 0): `s0 = 0x51` (PASS, legal read preserved).
  - Power-on Offset 1 (offset 1): `s1 = 0x00` (PASS, declined read returns 0).
  - Armed Altstatus (offset 0): `s3 = 0x58` (PASS, legal armed read preserved).
  - Armed Offset 1 (offset 1): `s4 = 0x00` (PASS, declined read returns 0).
  - Write cells: `s5 = 0x50`, `s6 = 0xff`, `t8 = 0x58`, `t9 = 0x71` (all PASS, `#481` and `#494` unperturbed).

---

## 5. Mutant Kill Table

Pre-table check `PRETABLE.out` was written and timestamped before table execution (`09:44:27`), establishing that the channels and failing observables were derived in advance.
The table ran in scratch clone `/tmp/gxaltdigin_clone` with object invalidation (`rm -f src/devices/*.o`), binary freshness validation (`[ gxemul -nt dev_wdc.c ]`), and sentinel verification on every leg.

| Leg | Description | Score | Status | Kill Rationale / Failing Observables |
| :--- | :--- | :---: | :---: | :--- |
| **`BASE`** | Ruled repair: decode `relative_addr != 0` on read, `odata = 0;` | **16/16** | **PASS** | Clean run across all 16 rows. Offset 1 returns 0x00, offset 0 returns S, write cells intact. |
| **`HEAD`** | Committed HEAD `8d372aa`: no read decode | **14/16** | **KILLED** | **KILLED BY CORE READS.** 2 rows fail (`CORE_READ_OFF1_POWERON` got `0x51`, `CORE_READ_OFF1_ARMED` got `0x58`). Symptom confirmed. |
| **`M_NULL_EFFECT`** | Clause-(d) mutant: decode branch kept, `odata = 0;` deleted | **14/16** | **KILLED** | **KILLED BY CORE READS.** 2 rows fail (`CORE_READ_OFF1_POWERON` got `0x51`, `CORE_READ_OFF1_ARMED` got `0x58`). Decisively killed because S != 0. |
| **`M_REINSTATE`** | Verbatim pre-fix read arm (`if (writeflag == MEM_READ) debug(...)`) | **14/16** | **KILLED** | **KILLED BY CORE READS.** 2 rows fail (`CORE_READ_OFF1_POWERON` got `0x51`, `CORE_READ_OFF1_ARMED` got `0x58`). Verbatim pre-fix defect reconfirmed. |
| **`M_NULL_MEDIUM`** | Null medium stub: `data[0] = 0; return 1;` on all reads | **14/16** | **KILLED** | **KILLED BY ACCEPT ROWS.** 2 rows fail (`ACCEPT_READ_OFF0_POWERON` got `0x00` vs want `0x51`; `ACCEPT_READ_OFF0_ARMED` got `0x00` vs want `0x58`). Rejects all-zero medium. |
| **`RESTORED`** | Reinstatement of pristine HEAD `8d372aa` after two-part clearance | **14/16** | **CONFIRMED** | Byte-for-byte identical output and score to baseline `witness_committed.out`. |

---

## 6. Two-Part Restoration Verification

Following execution of the mutant legs, two-part restoration of the scratch clone was strictly enforced:
1. **Source Restoration**: Pristine `dev_wdc.c` restored from saved baseline.
   - `cmp -s /tmp/gxaltdigin_clone/src/devices/dev_wdc.c GXEMUL-SEC/src/devices/dev_wdc.c` evaluated **CLEAN** (exit code 0).
2. **Binary Freshness**: Recompiled with `rm -f src/devices/*.o && make -C /tmp/gxaltdigin_clone -j8`.
   - `[ /tmp/gxaltdigin_clone/gxemul -nt /tmp/gxaltdigin_clone/src/devices/dev_wdc.c ]` evaluated **TRUE**.
3. **Sentinel Removal**:
   - Clone-local `.MUTANT` sentinel dropped before Leg 1 was unlinked **only after** both Part 1 and Part 2 were verified.
4. **Confirmation Run**:
   - Leg `RESTORED` executed against the rebuilt binary and confirmed score `14/16`, matching `witness_committed.out`.

---

## 7. Clause (e) Disclosure of Instrument Limitations

In accordance with project verification standards, the following instrument boundaries are disclosed:
1. **`wdcaltwidth` and `len == 2` Access Behavior**:
   - The alternate status region is registered 2 bytes wide (`alt_status_addr, 2`). All test rows in this harness exercise 1-byte accesses (`len == 1`, `lbu`/`sb`).
   - Under `DEVICE_ACCESS(wdc_altstatus)`, the handler executes `idata = data[0];` and `data[0] = odata;`, operating strictly on byte 0.
   - In GXemul, `memory_rw.c:560` pre-zeroes registered-device read buffers via `memset(data, 0, len)` under policy `#95`.
   - Consequently, a 16-bit little-endian read at offset 0 (`0x3f6`) receives `data[0] = odata` and `data[1] = 0x00`, yielding 16-bit value `S` (low byte S, high byte 0x00).
   - A 16-bit read at offset 1 (`0x3f7`) spans from `0x3f7` across `0x3f8` (the end of the 2-byte device registration), falling through device search in `memory_rw`.
   - On 16-bit writes, `idata = data[0]` means only the low byte is decoded for `WDCTL_RST`.
2. **Single IDE Channel Scope**: The test exercises the primary IDE channel at `0x1f0`/`0x3f6`. Secondary channels (`0x170`/`0x376`) and dual-channel PIIX4 configurations share the same C device model but were not separately driven.
3. **Absence of Real Floppy Multiplexing**: On physical PC hardware, I/O port `0x3f7` multiplexes the floppy disk controller Digital Input Register (DIR / digin) and the ATA Drive Address Register. GXemul isolates `wdc` and does not implement DIR multiplexing at `0x3f7`.
4. **Non-Interrupt Polled Verification**: The probe verifies controller status and command completion through polled status register reads. Interrupt line asserting/deasserting (`nIEN` interrupt disable) was not separately wired to an interrupt service routine in this harness.

---

## 8. Artifact Inventory

All artifacts are preserved under `regress/artifacts/wdcaltdigin/`:
- `agy_witness_20260911.md`: This comprehensive report.
- `agy_altdigin_witness_20260911.py`: Frozen Rung-3 witness and detector probe script.
- `witness_committed.out`: Raw baseline output on committed HEAD `8d372aa` (Score 14/16).
- `witness_fix.out`: Raw post-fix output on `BASE` (Score 16/16).
- `killtable_20260911/PRETABLE.out`: Pre-table derivation, claims mapping, and predicted scores.
- `killtable_20260911/mutate_altdigin.py`: Mutation driver script.
- `killtable_20260911/killtable.sh`: Automated kill table harness with two-part restoration checks.
- `killtable_20260911/SCORES.txt`: Recorded scores across all mutant legs.
- `killtable_20260911/probe_*.raw`: Raw logs for all legs (`BASE`, `HEAD`, `M_NULL_EFFECT`, `M_REINSTATE`, `M_NULL_MEDIUM`, `RESTORED`).
- `killtable_20260911/KILLTABLE_DONE`: Completion sentinel.
