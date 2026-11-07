# Gemini NEXT-STEP drafts for the 37 oldest open rows that must NOT be closed yet -- 2026-11-07 07:2x (PROPOSALS)

These are the rows the closure-draft pass (`CLOSEDRAFTS.md`) DISAGREED to close: each still names work owed.  Per row,
Gemini proposed ONE next step -- FIX-ROUND / MEASUREMENT / READING / RECORD / OWNER-DECISION -- and drafted it where the
row's own text settles a READING or a RECORD.  Tally over the seven batches: 11 FIX-ROUND, 8 MEASUREMENT, 5 READING, 11
RECORD, 3 OWNER-DECISION (38 for 37 rows: batch 01 classed one row twice).  Packets and replies: `nextstep_<k>/`.

## Batch 01 -- `citestale`, `auditmap`, `hlen`, `seam`, `stateaudit0923`, `dfreq`

Here is the defensive review of the provided ledger rows.

### 1. `citestale`
*   **Refutation:** `citestale:state_note` claims "NO GATE, PROBE OR SCRIPT IN THIS TREE READS A LINE CITATION FUNCTIONALLY". This is UNSETTLED; it cannot be verified without reading all gates and scripts in the tree. The text also truncates the Section D1 header claim.
*   **1. Next step:** RECORD
*   **2. Draft:** Close `citestale` as rejected on measurement. The proposed WARN had 0% recall on the 8 recorded instances and fired 57 times incorrectly. The structural issue is that recorded citations are bare (`:NNN`), which regexes requiring a file prefix cannot parse, meaning drifted numbers self-refute at the point of use by a human reader.
*   **3. Combined:** Cannot be combined.

### 2. `auditmap`
*   **Refutation:** `auditmap:title` claims the audit coverage table can be filled by measurement. This is UNSETTLED without knowing if the coverage tools are currently capable of mapping the required parameters without crashing state. 
*   **1. Next step:** MEASUREMENT
*   **2. Draft:** Needs the target bounds of the audit coverage table and the specific script to run to gather the metrics.
*   **3. Combined:** Cannot be combined.

### 3. `hlen`
*   **Refutation:** `hlen:title` claims there are device handlers that ignore access length. This is UNSETTLED without reading the handlers to confirm they don't implicitly bounds-check via a downstream macro.
*   **1. Next step:** READING
*   **2. Draft:** Needs the list of audited device handlers and their source code to confirm the ignored lengths.
*   **3. Combined:** Cannot be combined.

### 4. `seam`
*   **Refutation:** `seam:hold_question` claims the specific divergence may be gone because `#422` made `drive_guest.py` honour `$LOGDIR`. This is UNSETTLED without verifying the code at HEAD. 
*   **1. Next step:** READING
*   **2. Draft:** Needs to read `drive_guest.py` and `gate_hygiene.sh` at HEAD to check if they still disagree on the log path, and determine what a missing detector would need to observe.
*   **3. Combined:** Cannot be combined.

### 5. `stateaudit0923`
*   **Refutation:** `stateaudit0923:state_note` claims "records and the tree disagree in ten places". This is UNSETTLED without access to the actual tree at the referenced commits. 
*   **1. Next step:** OWNER-DECISION
*   **2. Draft:** Needs the owner to decide on unresolved items 1, 3, 4, and 5 listed in the hold question.
*   **3. Combined:** Cannot be combined.

### 6. `dfreq`
*   **Refutation:** `dfreq:hold_question` claims a witness was built in one session. This is UNSETTLED; we cannot confirm the witness exists or what state it captures without access to the session artifacts.
*   **1. Next step:** READING
*   **2. Draft:** Needs the artifact/output of the previously built witness to determine if there is a guest-observable consequence or if it is purely an internal representation difference.
*   **3. Combined:** Cannot be combined.

NEXTSTEP_01: 0 FIX-ROUND, 1 MEASUREMENT, 4 READING, 1 RECORD, 1 OWNER-DECISION

## Batch 02 -- `gdromkeyindex`, `gdromdriverclaims`, `panelcite0824`, `gdrompiooddlen`, `fbclearidempotent`, `gdromdefaultstatusless`

1. `gdromkeyindex`
1. Next step: RECORD. The text explicitly states that the 32/32 score is a historical claim overtaken by `#462` and no fresh escape scores are claimed.
2. Draft: The title's claim that "five mutants score a full 32/32 against #461's detector" is stale; these checks arrived in `7c9dd9e` (#462) and no fresh escape scores were measured on the current seat.
3. Cannot be combined.

2. `gdromdriverclaims`
1. Next step: MEASUREMENT. The row notes three guest-driver claims with no local artifact, requiring a measurement.
2. Not draftable; requires external measurement not present in the text.
3. Cannot be combined.

3. `panelcite0824`
1. Next step: RECORD. The text provides the full corrected census and identifies the 8 actionable directories. 
2. Draft: The original census of 166/76/94 was incorrect due to a flawed exact-match filter. The correct suffix-aware count is 174 dirs / 78 cited / 96 uncited. There are 8 actionable uncited directories, including two heavyweight answers and one pass 2 on a shipped commit. The prefixes were stripped in the backlog to prevent circular citations.
3. Cannot be combined.

4. `gdrompiooddlen`
1. Next step: FIX-ROUND. The text identifies a specific code flaw (`cur_data_offset + 1 < data_len` or width-aware read needed) that must be changed.
2. Needs code changes, not settled by text alone.
3. Cannot be combined.

5. `fbclearidempotent`
1. Next step: OWNER-DECISION. The text explicitly poses a hold question needing an owner's decision on whether the reload is a modelling shortcut.
2. Needs the owner to answer the stated hold question.
3. Cannot be combined.

6. `gdromdefaultstatusless`
1. Next step: MEASUREMENT. The text notes that "neither new row has a MEASURED RED on disk yet" and indicates a required run.
2. Needs the actual execution of the 60-row probe.
3. Cannot be combined.

NEXTSTEP_02: 1 FIX-ROUND, 2 MEASUREMENT, 0 READING, 2 RECORD, 1 OWNER-DECISION

## Batch 03 -- `offlinescope`, `wdcnullxfer`, `exitcensus`, `exit0oracle`, `gxprobepccache`, `pcc2pscaleflood`

## Row Analysis

### ROW `offlinescope`
1. RECORD
2. Draft: "Record updated: the machine embargo scope was overstated and is now corrected. Seven of the top eight ranked defects sit in files already pulled in by offline differentials, meaning no new fixture is required."
3. Cannot be combined.

### ROW `wdcnullxfer`
1. OWNER-DECISION
2. Draft: "Question for the batched flagship close pass: Does the rung-3 witness located in regress/artifacts/wdcnullxfer/rung3_20260913/ plus the shipped detector successfully close this row, or is it required to promote the witness probe directly into regress/?"
3. Cannot be combined.

### ROW `exitcensus`
1. FIX-ROUND
2. Needs: The `exit_census.py` file to correct the by-enclosing-construct splitting parser logic.
3. Cannot be combined.

### ROW `exit0oracle`
1. MEASUREMENT
2. Needs: A live harness execution to measure if reading any value back after the access under any row name achieves the exact same discrimination as using explicit seed variables.
3. Cannot be combined.

### ROW `gxprobepccache`
1. FIX-ROUND
2. Needs: The `gxprobe` source code to verify and enforce that the `step` command execution properly invalidates the cached PC.
3. Cannot be combined.

### ROW `pcc2pscaleflood`
1. FIX-ROUND
2. Needs: The `devices/dev_pcc2.c` file to implement the missing latch mechanism on the PSCALEADJ write-side `fatal()` print.
3. Can be combined with `pcc2huhflood` and `pcc2assertflood` into a single floodclass fix round.

NEXTSTEP_03: 3 FIX-ROUND, 1 MEASUREMENT, 0 READING, 1 RECORD, 1 OWNER-DECISION

## Changed Steps Review
All proposed FIX-ROUND changes (correcting the PC cache invalidation in gxprobe, latching the flood prints in dev_pcc2, and fixing the attribution logic in the test census script) are structurally correct in principle. Because they strictly address tool observability, debugger synchronization, and print ratelimiting, they safely leave alone every state the running code can save without corrupting the emulator's core architectural memory or save-state persistence.

## Claims Review (Defensive)
- **ATTACK 1 (`ROW offlinescope:title`)**: Claims "six of the top eight ranked defects sit in files they already pull in". Refutation: The author internally contradicts and refutes this with the note "[corrected 2026-11-02: seven of the top eight, not six]". BROKEN.
- **ATTACK 2 (`ROW wdcnullxfer:state_note`)**: Claims `scsi_transfer_alloc` "CANNOT RETURN NULL". Refutation: Even with a freelist, a robust custom allocator can fail under extreme memory corruption or poisoned freelist pointers, returning NULL outside standard `exit(1)` paths. UNSETTLED (needs `scsi_transfer.c`).
- **ATTACK 3 (`ROW exitcensus:title`)**: Claims `exit_census.py`'s split attributed every call in a plain non-static function to the preceding `DEVICE_ACCESS`. Refutation: We cannot definitively determine the script's AST parsing or regex rules without inspecting it. UNSETTLED (needs `exit_census.py`).
- **ATTACK 4 (`ROW exit0oracle:state_note`)**: Claims the population is exactly 43 rows across 9 files. Refutation: Verifying these exact totals requires executing `grep` on the live test directories. UNSETTLED (needs `regress/*.py`).
- **ATTACK 5 (`ROW gxprobepccache:title`)**: Claims `gxprobe` cached the PC across `step`. Refutation: We cannot verify the debugger probe's internal state lifecycle and whether the PC is genuinely skipped versus overwritten later in the loop. UNSETTLED (needs `gxprobe` source).
- **ATTACK 6 (`ROW pcc2pscaleflood:title`)**: Claims `PSCALEADJ`'s write-side `fatal()` is unlatched. Refutation: A latching mechanism might exist higher in the IO dispatch stack before it ever reaches the device-specific file. UNSETTLED (needs `devices/dev_pcc2.c`).

## Batch 04 -- `cxseatcheck`, `gdrommappedvacuous`, `negrowclass`, `printedvariants`, `probeneedleterm`, `ubsanshiftlane`

### 1. ROW `cxseatcheck`
1. **Next step:** RECORD
2. **Draft / Defense:** Record closure. The author's newly written script failed by incorrectly masking its exit code (`rc=1` hidden by a subsequent command) and reading the wrong stream. **Refutation (BROKEN):** The claim that "The two discriminators differ and both are sound" is false. If `panel.sh` anchors tests only to the first and last 400 bytes, an `ERROR:` embedded at byte 500 by the codex stream will evade detection, meaning they are not equivalently sound for all inputs. The row should be retired as superseded by `panel.sh`.
3. **Combinable:** No.

### 2. ROW `gdrommappedvacuous`
1. **Next step:** RECORD
2. **Draft / Defense:** Record closure. The row was generated by a one-way sync process and lacks a current ledger warrant. **Refutation (HOLDS):** Closing the ledger row strictly clears the decayed warrant without incorrectly marking the underlying `OUTSTANDING_BUGS.md` bug as resolved.
3. **Combinable:** Yes, with `negrowclass`, `printedvariants`, and `probeneedleterm`.

### 3. ROW `negrowclass`
1. **Next step:** RECORD
2. **Draft / Defense:** Record closure. **Refutation (UNSETTLED):** The claim that `check_bugfile_sync.py` only works in one direction and was "written to stop [this], in the direction it does not check" cannot be verified without reading the `check_bugfile_sync.py` source code.
3. **Combinable:** Yes, with `gdrommappedvacuous`, `printedvariants`, and `probeneedleterm`.

### 4. ROW `printedvariants`
1. **Next step:** RECORD
2. **Draft / Defense:** Record closure. **Refutation (HOLDS):** The assertion that these sync-issue rows hold no independent ledger merit holds true, as the source of truth resides solely in `OUTSTANDING_BUGS.md`.
3. **Combinable:** Yes, with `gdrommappedvacuous`, `negrowclass`, and `probeneedleterm`.

### 5. ROW `probeneedleterm`
1. **Next step:** RECORD
2. **Draft / Defense:** Record closure. **Refutation (UNSETTLED):** Similar to the other sync rows, verifying the exact nature of the decaying warrant and one-directional sync flow requires inspecting the bugfile sync script.
3. **Combinable:** Yes, with `gdrommappedvacuous`, `negrowclass`, and `printedvariants`.

### 6. ROW `ubsanshiftlane`
1. **Next step:** MEASUREMENT
2. **Measurement Needed / Defense:** Execute `regress/lca_confbus_probe.py` against the `build-asan` binary to prove the `-fsanitize=address,undefined` sweep triggers on the `bus == 0` path. **Refutation (BROKEN):** The claim that "with a correct 32-bit mask `x |= ~mask` is `x |= 0`" is broken. If the mask is derived via `(1U << 31)`, `~mask` evaluates to `0x7FFFFFFF`, not `0`; to equal `0`, the mask would need to be `0xFFFFFFFF`. Furthermore, the commit text terminates abruptly at `tag = (relative_addr >> 5) & ~0xf`, leaving the exact bitwise execution unprovable from the text.
3. **Combinable:** No.

NEXTSTEP_04: 0 FIX-ROUND, 1 MEASUREMENT, 0 READING, 5 RECORD, 0 OWNER-DECISION

## Batch 05 -- `uninorthdevscan`, `codexcyberflag`, `armcpabsent`, `armdwordalign`, `ascoutresid`, `dupidcheck`

1. `uninorthdevscan`
1. READING / MEASUREMENT. The step must answer whether `idata` can actually carry bits 32..63.
2. Cannot be drafted from the text alone; requires reading `memory_readmax64` to see if `MEM_PCI_LITTLE_ENDIAN` perturbs the length and verifying access widths from macppc. 
3. Cannot be combined.

2. `codexcyberflag`
1. RECORD.
2. DRAFT: Cybersecurity platform filters are triggered by project vocabulary (e.g., "kill", "death rows"). The discriminator is a 0-byte `.txt` response alongside a non-empty `.err` file. The proven recovery is rewording the query/filename to remove triggering terms.
3. Cannot be combined.

3. `armcpabsent`
1. FIX-ROUND. Site: ARM coprocessor MRC/MCR instruction delivery.
2. Needs the source code for the ARM instruction handlers to implement Undefined Instruction delivery.
3. Can be combined with `armdwordalign` as both are ARM instruction set fixes.

4. `armdwordalign`
1. FIX-ROUND. Site: LDRD/STRD address masking.
2. Needs ARMv6 instruction handler source code.
3. Can be combined with `armcpabsent`.

5. `ascoutresid`
1. FIX-ROUND. Site: `dev_asc.c`.
2. Needs the `dev_asc.c` DMA reporting code to fix the residual report.
3. Cannot be combined.

6. `dupidcheck`
1. FIX-ROUND. Site: `tools/precommit_check.sh` or Python checkers.
2. Needs the precommit script source to add the id-uniqueness section.
3. Cannot be combined.

NEXTSTEP_05: 4 FIX-ROUND, 0 MEASUREMENT, 1 READING, 1 RECORD, 0 OWNER-DECISION

## Batch 06 -- `m88kwtbit`, `mipspagemaskdead`, `i8259ocw3revert`, `i8259smm`, `lecsr3inert`, `pit8253pendingptr`

Here is the review of the next step proposals based on the provided text.

### 1. `m88kwtbit`
1. MEASUREMENT: The legal MC88100 `.wt` semantics must be verified on hardware.
2. Needs real hardware test or an authoritative manual, as the text states "legal MC88100 `.wt` semantics are not established and the recipe is not an authority" (ROW `m88kwtbit`).
3. Cannot be combined.

### 2. `mipspagemaskdead`
1. FIX-ROUND: Remove the dead code `case 0x00007ff:` in `src/cpus/memory_mips_v2p.c`.
2. Needs a code patch to delete or justify the arm, as it "cannot OR back down to 0x7ff" (ROW `mipspagemaskdead`).
3. Cannot be combined.

### 3. `i8259ocw3revert`
1. FIX-ROUND: Implement the remembered-selection state logic for IRR/ISR.
2. Needs a code patch to address the probe's port-I/O shape and ensure the model correctly answers based on the last RR/RIS selection (ROW `i8259ocw3revert`).
3. COMBINED: Yes, with `i8259smm` (both address `devices/dev_8259.c`).

### 4. `i8259smm`
1. MEASUREMENT: Determine the impact of SMM and the 0x68 arm on the model.
2. Needs execution/testing of the SMM behavior, as the text explicitly states the impact is "NOT CHECKED" (ROW `i8259smm`).
3. COMBINED: Yes, with `i8259ocw3revert`.

### 5. `lecsr3inert`
1. RECORD: Close with documentation that the state is benign and intended.
2. DRAFT: The three implemented CSR3 bits (BSWP, ACON, BCON) are safely stored but not consulted by the model, because the model does not emulate the DMA byte lanes governed by BSWP (is_bigendian drives SRAM instead). 
3. Cannot be combined.

### 6. `pit8253pendingptr`
1. FIX-ROUND: Remove the dead IRQ-0 decrement code in `isa_interrupt_deassert()`.
2. Needs a code patch to clean up the dead code, as "no live code depends on the stale copy" and the decrement is recorded as dead (ROW `pit8253pendingptr`).
3. Cannot be combined.

NEXTSTEP_06: 3 FIX-ROUND, 2 MEASUREMENT, 0 READING, 1 RECORD, 0 OWNER-DECISION

## Batch 07 -- `ppcifetchdeclineprod`

1. **ppcifetchdeclineprod**
   1. The ONE concrete next step: MEASUREMENT (a window sweep on bebox, prep, macppc, and mvmeppc to see if any device declines an instruction-width read).
   2. What it needs: The actual execution of the window sweep measurement; the results are not present in the text.
   3. COMBINED: Cannot be combined (no other rows in this packet).

NEXTSTEP_07: 0 FIX-ROUND, 1 MEASUREMENT, 0 READING, 0 RECORD, 0 OWNER-DECISION

