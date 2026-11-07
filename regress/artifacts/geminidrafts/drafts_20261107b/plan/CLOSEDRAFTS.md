# Gemini closure drafts for the 80 oldest open rows proposed for closing -- 2026-11-07 06:4x (PROPOSALS for the adjudication)

The earlier triage pass proposed DOCUMENT-AND-CLOSE / DROP / CLOSE-OVERTAKEN for each row; this pass, with the row's title,
state_note head (1,400 characters -- two rows came back UNSETTLED for the cut) and hold_question, drafted the closure record
or DISAGREED.  **Where the two passes disagree, the row is NOT to be closed on either pass's word.**  Packets and replies:
`closedraft_<k>/`; maker `mk_closedraft.py`.
**Tally: 43 AGREE (closure record drafted), 37 DISAGREE** -- batch 15 re-drafted batch 05's two UNSETTLED-by-truncation rows with their FULL state notes and supersedes them (`wdcperopcode` now AGREE, `offlinescope` DISAGREE).


## Batch 01 -- `citestale` (DROP), `auditmap` (DOCUMENT-AND-CLOSE), `b101` (DOCUMENT-AND-CLOSE), `hlen` (CLOSE-OVERTAKEN), `seam` (DOCUMENT-AND-CLOSE), `stateaudit0923` (CLOSE-OVERTAKEN)

### `citestale`
1. DISAGREE. The text rejects the WARN detector but explicitly identifies the underlying defect (bare `:NNN` stale citations that "never passed green") as a live, unmitigated vulnerability (`citestale:state_note:(a)`).
2. N/A
3. FACT TO CHECK: Does another row currently track and address the bare citation parsing failure?

### `auditmap`
1. DISAGREE. The row's `state_note` is entirely empty (`auditmap:state_note`), making the triage claim of "explicitly grandfathered" unverifiable from this text alone.
2. N/A
3. UNSETTLED: Settle via the project's dashboard architecture documentation or the owner's decision ledger file.

### `b101`
1. AGREE. The text proves structurally that `timer_hz` is a numerator, meaning a 0 value safely stops advancement without division by zero, which is the correct behavior for a stopped timer (`b101:state_note`).
2. RECORD: Assessed 2026-08-27: mechanism confirmed but structurally safe. `timer_hz` acts as a numerator, preventing division by zero. Correct behavior is a timer that does not advance. No code changes required.
3. FACT TO CHECK: Verify `timer_hz` is never used as a divisor in any other unlisted execution path or macro within `dev_sh4.c`.

### `hlen`
1. DISAGREE. The triage reason admits the class fixes have only "largely shipped" (`hlen:triage`), and an empty `state_note` leaves the remainder unaddressed, meaning work is still owed for the rest of the handlers.
2. N/A
3. FACT TO CHECK: Are all device handlers comprehensively verified to honor access length?

### `seam`
1. DISAGREE. The `state_note` explicitly mandates "the row stays HELD pending the named next step" (`seam:state_note`), directly contradicting the triage pass's proposal to close it now.
2. N/A
3. FACT TO CHECK: Has the "named next step" from the Codex research actually been completed and verified?

### `stateaudit0923`
1. DISAGREE. The `hold_question` lists items (4) and (5) as unaddressed with no resolution record (`stateaudit0923:hold_question`), and it lacks the discriminating control required for an OVERTAKEN closure (`PROJECT FRAMING:paragraph 1`).
2. N/A
3. FACT TO CHECK: Have hold conditions (4) and (5) been resolved in subsequent commits?

CLOSEDRAFT_01: 1 AGREE, 5 DISAGREE

## Batch 02 -- `strad` (DROP), `fbvolatile` (DOCUMENT-AND-CLOSE), `m8invpred` (DROP), `dfreq` (DOCUMENT-AND-CLOSE), `killartifacts` (DROP), `m88kexit` (DOCUMENT-AND-CLOSE)

1. `strad`
AGREE: No text describes a live reachable defect; the triage pass explicitly ruled to drop it (ROW strad triage pass).
RECORD: Dropped as currently filed. The assessor explicitly ruled to drop this row without further action.
FACT TO CHECK: Whether the "three mutant shapes" actually cause a guest-observable failure at HEAD.

2. `fbvolatile`
AGREE: The state note confirms the missing volatile is latent and "not what that path currently fails on" (ROW fbvolatile state_note).
RECORD: Documented and closed as latent. The missing `volatile` causes no demonstrated miscompile on live access paths, and `volatile` would not make the `--` versus `++` operation atomic. 
FACT TO CHECK: Whether a modern compiler optimization actually miscompiles the `pending_bound` check at HEAD.

3. `m8invpred`
AGREE: The row's residual value is only a lesson already recorded elsewhere in the carrier (ROW m8invpred triage pass).
RECORD: Dropped. The row only contains a lesson about reading seat predictions that is already preserved in the carrier.
FACT TO CHECK: Whether the predicted state-dependent mutant class represents an unfixed, live vulnerability.

4. `dfreq`
DISAGREE: The state note explicitly states "the row stays HELD pending the named next step and the batched flagship close pass" (ROW dfreq state_note) and a witness was built, contradicting the immediate closure proposed.
FACT TO CHECK: What the built witness actually demonstrates regarding guest-observable consequences.

5. `killartifacts`
AGREE: The defect is explicitly folded into another row (`killdriverunTracked`), meaning this specific row can be dropped as superseded (ROW killartifacts triage pass).
RECORD: Dropped. The issue of kill-table drivers preserving no per-row artifacts is explicitly folded into row `killdriverunTracked`.
FACT TO CHECK: Whether `killdriverunTracked` is actually open and successfully tracking the missing `#462` base logs.

6. `m88kexit`
AGREE: The `exit(1)` calls are structurally unreachable at HEAD because all 7 `goto exception` sites have preceding fault assignments (ROW m88kexit state_note).
RECORD: Documented and closed. The `exit(1)` calls in `memory_m88k.c` exist but are dormant and unreachable because fault assignments precede every jump to the exception label.
FACT TO CHECK: Whether there is any hidden or implicit control flow path to the `exception:` label at `:373` that bypasses the fault assignments.

CLOSEDRAFT_02: 5 AGREE, 1 DISAGREE

## Batch 03 -- `stalecopies` (DOCUMENT-AND-CLOSE), `queuesubstr` (DOCUMENT-AND-CLOSE), `sh4pcicvoid` (DOCUMENT-AND-CLOSE), `stdbufasan` (DOCUMENT-AND-CLOSE), `hpcshcpu` (DROP)

1. `stalecopies`
1. AGREE: The hazard was reading-only and the files were already moved out of the tree.
2. RECORD: Assessed: three stale copies of dev_wdc.c caused a reading hazard. The files were moved to an external directory on 2026-09-13, removing the hazard. No code changes required.
3. FACT: A file-reading seat still actively targets the new external location of the stale copies.

2. `pcicmergeA`
1. AGREE: The defect is documented and adding a detector row would incorrectly cement the defect.
2. RECORD: Assessed: the PCICONF0 latch-merge reproduction lacks a detector row. Closing as documented because creating the row would cement the defect.
3. FACT: The third fault class has landed, which would now make writing the detector row possible and necessary.

3. `queuesubstr`
1. AGREE: The defect was a test framework false-positive that was already found and fixed.
2. RECORD: Assessed: check_fable_queue substring matching falsely passed the gate. Closing as OVERTAKEN. OWED: a control neutralizing the substring fix to reproduce the false green, and the rows that carry this coverage.
3. FACT: The substring fix was reverted or incomplete, leaving the gate still vulnerable to false greens.

4. `sh4pcicvoid`
1. AGREE: The void line is an accepted proof gap rather than a functional defect in the fix.
2. RECORD: Assessed: `odata = 0` in #443's fix is void in the unimplemented-CPU arm. Closing as documented because it is a known proof gap, not a reachable defect.
3. FACT: The unimplemented-CPU PCICONF0 arm is actually reachable and the void line affects guest execution.

5. `stdbufasan`
1. AGREE: The environment hazard and the silent failure of ASan are already documented and fixed in the gate script.
2. RECORD: Assessed: stdbuf breaks ASan startup and ASan ignores bogus flags. Closing as OVERTAKEN. OWED: a control removing `verify_asan_link_order=0` to trigger the abort, and the rows that carry this coverage.
3. FACT: The gate script `regress/gate_asan_sweep.sh` has been modified to remove the documented fixes.

6. `hpcshcpu`
1. AGREE: A defect that cannot be reproduced or test-first'd within the tree must be dropped as unactionable.
2. RECORD: Assessed: repo contradiction on hpcsh being SH-3 vs SH-4. Dropped because the claim cannot be settled in this tree without an external SH3/SH4 manual.
3. FACT: An external SH3 or SH4 manual was obtained that definitively settles the identity.

CLOSEDRAFT_03: 6 AGREE, 0 DISAGREE

## Batch 04 -- `sh4itlbpr` (DOCUMENT-AND-CLOSE), `gdromkeyindex` (CLOSE-OVERTAKEN), `gdromdriverclaims` (DOCUMENT-AND-CLOSE), `panelcite0824` (DOCUMENT-AND-CLOSE), `probeslow` (CLOSE-OVERTAKEN), `asicarray4` (DROP)

### ROW `sh4itlbpr`
1. AGREE. `<ROW sh4itlbpr:state_note>` explicitly states that "RETURNING 0x20 IS ARCHITECTURALLY PERMITTED, NOT WRONG," meaning this is a fidelity nit rather than a live defect.
2. RECORD: Closed as documented. Assessed as a fidelity nit because returning 0x20 for reserved bit 5 is architecturally permitted per the manual's "undefined read value" clause, requiring no changes to the shipped mask. 
3. FACT: We must check that no specific guest OS translation logic strictly relies on that bit being exactly 0 despite the manual's definition.

### ROW `gdromkeyindex`
1. DISAGREE. `<ROW gdromkeyindex:state_note>` explicitly names work still owed by stating "Four gaps remain as debt: cross-window state preservation..."
2. N/A (Disagree with closure).
3. FACT: We must check if the four remaining gaps have been split into newly filed, tracked issues before this specific row can be considered overtaken or closed.

### ROW `gdromdriverclaims`
1. DISAGREE. `<ROW gdromdriverclaims:title>` describes a live defect by stating that one of the guest-driver claims `#462`'s design rests on was "measured false the same day".
2. N/A (Disagree with closure).
3. FACT: We must check the actual operational impact of the false claim to determine if `#462`'s design is fundamentally broken or if it handles the false premise safely.

### ROW `panelcite0824`
1. DISAGREE. `<ROW panelcite0824:state_note>` explicitly names work still owed by identifying eight actionable, unharvested panel directories (including a pass 2 on a shipped commit).
2. N/A (Disagree with closure).
3. FACT: We must check the contents of the eight actionable directories to ensure no late dissent or critical bugs were missed before dismissing them.

### ROW `probeslow`
1. AGREE. `<ROW probeslow:title>` confirms the overrun was "measured false at 52", and the text frames the row filter complexity as an architectural discussion rather than a live code defect.
2. RECORD: Closed as overtaken (folding into probetimebased). OWED: A discriminating control measured at HEAD to verify the 1800s overrun symptom returns when neutralized; the rows that now carry this coverage; and preserving that control at a durable path.
3. FACT: We must check that the `probetimebased` issue actually inherits the context and architectural retrofitting costs documented in this row.

### ROW `asicarray4`
1. AGREE. `<ROW asicarray4:state_note>` describes a proposed alternative that was rejected because "the mutant escapes" and is explicitly noted as a "TRADE, not a fix".
2. RECORD: Dropped. Expanding the array to [4] is a rejected trade-off, not a fix. It costs a mutant kill by creating an untouched slot that survives `DEVICE_TICK`, validating its rejection.
3. FACT: We must check that the out-of-bounds class this trade-off attempted to de-fang is adequately mitigated by other existing boundaries (such as `asicindexcase`).

CLOSEDRAFT_04: 3 AGREE, 3 DISAGREE

## Batch 05 -- `gdrompiooddlen` (DOCUMENT-AND-CLOSE), `wdcperopcode` (DOCUMENT-AND-CLOSE), `fbclearidempotent` (DOCUMENT-AND-CLOSE), `gdromdefaultstatusless` (CLOSE-OVERTAKEN), `offlinescope` (DOCUMENT-AND-CLOSE), `wdcnullxfer` (DOCUMENT-AND-CLOSE)

Here is the evaluation of the 6 proposed closures based strictly on the provided text.

### ROW `gdrompiooddlen`
1. **DISAGREE.** BROKEN: The title claims the defect is latent because "no path can produce an odd length," but the text explicitly contradicts this by stating "an ODD count is expressible" and the subsequent adjustments "do not remove oddness," describing a live, reachable out-of-bounds read.
3. **Fact to check:** Whether a guest can actually trigger the out-of-bounds read by writing an odd count that reaches the vulnerable guard.

### ROW `wdcperopcode`
1. **DISAGREE.** UNSETTLED: The justification text cuts off mid-sentence at `"THE SHIPPED SP [... 962 more characters not shown]"`, making it impossible to verify the final adjudication on the shipped spec; the full ledger file or `dev_wdc.c` is needed to settle this.
3. **Fact to check:** Whether the shipped specification completely bounds the flood without breaking legitimate distinct guest actions.

### ROW `fbclearidempotent`
1. **DISAGREE.** HOLDS: The row names work still owed, explicitly stating it "Needs a row of its own and a reading of what the reload is actually for," and the active hold question confirms the required fix differs based on this uncompleted reading.
3. **Fact to check:** Whether the unconditional timer reload is a mere shortcut or an intentional model of the clear write itself.

### ROW `gdromdefaultstatusless`
1. **DISAGREE.** HOLDS: The text explicitly names work still owed, stating that neither new row has a MEASURED RED on disk yet and that this is "Owed before #490 closes."
3. **Fact to check:** Whether the new `stale quiet` and `stale how` rows can actually produce a measured red kill on disk when tested against a broken state.

### ROW `offlinescope`
1. **DISAGREE.** UNSETTLED: The explanation of why `b115` was the cheapest possible start cuts off at `"diff_diskimage_io.c alre [... 4559 more characters not shown]"`, making it impossible to verify the final conclusion on fixture reuse; the full ledger file or `diff_diskimage_io.c` is needed to settle this.
3. **Fact to check:** Whether reusing the existing fixtures is actually sufficient to test the ring-buffer section without requiring massive, uncounted new stubbing work.

### ROW `wdcnullxfer`
1. **DISAGREE.** HOLDS: The hold question explicitly asks if anything is still owed (such as promoting the rung-3 witness probe into `regress/`), leaving the completeness of the closure in question.
3. **Fact to check:** Whether the rung-3 witness probe must be promoted to the regression suite before the defect can be considered safely closed.

CLOSEDRAFT_05: 0 AGREE, 6 DISAGREE

## Batch 06 -- `exitcensus` (DROP), `exit0oracle` (DROP), `gxprobepccache` (CLOSE-OVERTAKEN), `pcc2pscaleflood` (DROP), `wdcwidthmatrix` (DOCUMENT-AND-CLOSE), `m88kexctaildefault` (DOCUMENT-AND-CLOSE)

1. `exitcensus`
1. DISAGREE: The row's title describes a live defect (bucket inflation), and the triage's claim that the tool was "correctly restored" is UNSETTLED because it cannot be verified from the provided text.
2. 
3. The file `exit_census.py` and its history must be checked to confirm if the original tool was indeed restored and per-function attribution removed.

2. `exit0oracle`
1. DISAGREE: The state note explicitly contains an open question that is cut off ("THE OPEN QUESTION IS WHETHER TH"), indicating work still owed, and the triage's claim of a "never-commit list" is unsupported by the text.
2. 
3. The full text of the cut-off open question must be read from the source or issue tracker to determine what work remains, and the existence of the never-commit list for `regress/sgi_re_unmapped_probe.py` must be verified.

3. `gxprobepccache`
1. DISAGREE: The proposed CLOSE-OVERTAKEN fails to provide the three mandatory conditions (discriminating control, carrier rows, durable path) required by the project framing, and the triage note itself names work still owed ("must check if gxprobe.py is tracked").
2. 
3. The source of `send()` must be checked to verify the fix, and it must be determined whether `gxprobe.py` is tracked so the mandatory OVERTAKEN conditions can be correctly formulated.

4. `pcc2pscaleflood`
1. DISAGREE: The state note explicitly conditions closure on pending work ("close as duplicate when the nine-site latch lands"), meaning it cannot be dropped until that prerequisite is met.
2. 
3. The commit log or `dev_pcc2.c` must be checked to verify whether the "nine-site latch" (from `pcc2huhflood`) has actually landed at HEAD.

5. `wdcwidthmatrix`
1. AGREE: The text explicitly confirms the omitted controls are "NOT A LIVE HOLE" and provides the arithmetic proof that overshoots are covered.
2. Row wdcwidthmatrix closed. Documented that full matrix and exact-fit controls were omitted. Completeness check confirms this is not a live hole because a one-byte read cannot step past zero.
3. Someone must check if there are any architectural edge cases where a one-byte read could consume zero bytes and bypass the remainder arithmetic.

6. `m88kexctaildefault`
1. AGREE: The title explicitly states this is a "DESIGN OPTION RECORD ... NOT adopted", meaning there is no defect to fix and no work owed.
2. Row m88kexctaildefault closed. The row serves solely as a record for a design option (D4 of #502) that was deliberately not adopted due to blast radius.
3. Someone must confirm that no subsequent triage pass or issue decided to mandate this design option after it was initially rejected.

CLOSEDRAFT_06: 2 AGREE, 4 DISAGREE

## Batch 07 -- `m88ksfrzfatal` (DOCUMENT-AND-CLOSE), `cxseatcheck` (CLOSE-OVERTAKEN), `dec21143deadclamp` (DOCUMENT-AND-CLOSE), `gdrommappedvacuous` (DROP), `mtesrcdup` (DOCUMENT-AND-CLOSE), `negrowclass` (DROP)

### 1. `m88ksfrzfatal`
1. AGREE: The text states this is an unlatched diagnostic (a floodclass instance) and not a correctness defect, meaning no fix is owed and it can be documented and closed.
2. RECORD: Assessed the SFRZ re-route's fatal() diagnostic. It acts as an unlatched floodclass instance rather than a correctness defect, requiring no logic changes. No code was altered; state is preserved as documented.
3. Fact to check: Verify that triggering this diagnostic merely logs a warning and does not actually halt the emulator or corrupt guest state.

### 2. `cxseatcheck`
1. DISAGREE: The text states the fix (#544) is still "IN WORK" rather than merged at HEAD, and that the defects were "all mine," which violates the OVERTAKEN condition that someone else's fix removed the defect at HEAD.
2. (N/A)
3. Fact to check: Verify whether commit `e8a2bc` has actually been merged into HEAD and is no longer just in flight.

### 3. `dec21143deadclamp`
1. AGREE: The text confirms the guards are mathematically unreachable because `bufsize` is bounded by its own masks, meaning this is dead code rather than a live defect.
2. RECORD: Assessed the size guards in dev_dec21143.c. Variables are safely bounded (0..2047) by their own masks, rendering the guards mathematically unreachable. No code was modified.
3. Fact to check: Verify that the masks bounding `bufsize` cannot be bypassed, overflowed, or mutated prior to reaching the guards.

### 4. `gdrommappedvacuous`
1. DISAGREE: The title describes a live, reachable defect (vacuous testing controls satisfied by zero-filled reads), so it is a defect worth a round and dropping it merely because it is tracked in another file violates the rule for dropping rows.
2. (N/A)
3. Fact to check: Verify if the test framework has already been updated to reject zero-filled reads for these specific controls.

### 5. `mtesrcdup`
1. AGREE: The text confirms the two variables compute byte-identical expressions and cannot disagree today, meaning it is not a live defect and requires no immediate fix.
2. RECORD: Assessed do_mte_transfer variable declarations for `src` and `src_tlb`. They compute byte-identical expressions and present no hazard unless future edits decouple them. Left documented without code changes.
3. Fact to check: Verify that `MTE_MODE_SRC_BUF_MASK` and `MTE_SRC_TLB_SHIFT` are static constants and not volatile or state-dependent macros that could change between the two evaluations.

### 6. `negrowclass`
1. DISAGREE: The row text explicitly notes "two GATED ones still open", indicating live defects and work still owed, making it completely ineligible to be dropped.
2. (N/A)
3. Fact to check: Verify if the two gated instances have actually been repaired in a separate, unlinked commit.

CLOSEDRAFT_07: 3 AGREE, 3 DISAGREE

## Batch 08 -- `printedvariants` (DROP), `probeneedleterm` (DROP), `ubsanshiftlane` (DOCUMENT-AND-CLOSE), `uninorthdevscan` (DOCUMENT-AND-CLOSE), `codexcyberflag` (DOCUMENT-AND-CLOSE), `splitscorer` (DROP)

## 1. ROW `printedvariants`
1. DISAGREE, because the row's text explicitly describes a live defect ("20 copies of printed() with FOUR different contracts") that still exists in the codebase.
2. N/A (Disagree)
3. The one fact that would make closing wrong: That the 20 copies of `printed()` with differing contracts still exist unresolved in the running code.

## 2. ROW `probeneedleterm`
1. DISAGREE, because the row's text explicitly describes a live, reachable defect ("unterminated needles accept longer numbers").
2. N/A (Disagree)
3. The one fact that would make closing wrong: That the unterminated needles still accept longer numbers at HEAD.

## 3. ROW `ubsanshiftlane`
1. DISAGREE, because the text describes a live defect ("two one-line regressions that re-open real UB") and names work still owed ("A lane added after a pass is a lane nobody reviewed"). 
2. N/A (Disagree)
3. The one fact that would make closing wrong: That the two regressions re-opening undefined behavior are still present and the new measurement lane remains unreviewed.

## 4. ROW `uninorthdevscan`
1. DISAGREE, because the row's text describes a live defect (the loop unconditionally evaluates `1 << 31`, triggering signed-shift UB regardless of guest-visibility) and names work still owed ("WHAT IS NOT ESTABLISHED").
2. N/A (Disagree)
3. The one fact that would make closing wrong: That the C-level undefined behavior at `dev == 31` remains reachable and unfixed in `dev_uninorth.c:71`.

## 5. ROW `codexcyberflag`
1. DISAGREE, because the row's text explicitly names work still owed ("needs formal promotion to a rule").
2. N/A (Disagree)
3. The one fact that would make closing wrong: That the circumvention technique has not actually been formally promoted to a rule yet.

## 6. ROW `splitscorer`
1. AGREE, because the text confirms the defect was introduced and repaired in the same session, leaving a population of zero at HEAD (not a defect worth a round).
2. RECORD: Dropped. The editing hazard was introduced and repaired within the same session, leaving a population of zero across all candidate probes at HEAD. It is not a defect worth a round.
3. The one fact that would make closing wrong: That the population of this defect is not actually zero across all 73 candidate probes at HEAD (8d9df658).

CLOSEDRAFT_08: 1 AGREE, 5 DISAGREE

## Batch 09 -- `agentmodelwall` (DOCUMENT-AND-CLOSE), `wdcaddr2` (DROP), `wdcrowpin` (CLOSE-OVERTAKEN), `wdcverdictone` (CLOSE-OVERTAKEN), `armcpabsent` (DOCUMENT-AND-CLOSE), `armdwordalign` (DOCUMENT-AND-CLOSE)

1. `agentmodelwall`
1. AGREE: The issue describes operational limits of external AI/LLM models (`ROW:agentmodelwall:title`), not a defect in the GXemul codebase.
2. CLOSURE RECORD: CLOSED as DOCUMENT-AND-CLOSE. Assessed as an operational rule for external tool usage (Agent tool/sonnet/opus) with no changes to the GXemul codebase.
3. FACT TO CHECK: That "Agent tool", "sonnet", and "opus" do not coincidentally refer to actual internal GXemul subsystems.

2. `wdcaddr2`
1. AGREE: The text explicitly states there is no measured delta/symptom today (`ROW:wdcaddr2:hold_question`), making it an invalid target for a defensive fix right now.
2. CLOSURE RECORD: CLOSED as DROP. The hazard of a second wdc on landisk has no measured delta today. Will reopen if the PCIIDE TODO at machine_landisk.c:41 introduces a second wdc.
3. FACT TO CHECK: That no current GXemul machine instance (e.g., landisk) currently instantiates a second WDC device.

3. `wdcrowpin`
1. AGREE: The symptom (uncaught row deletion) is claimed to be superseded and caught by `#551e`'s call counts (`ROW:wdcrowpin:the triage pass's reason`).
2. CLOSURE RECORD: CLOSED as OVERTAKEN by #551e. OWED: A discriminating control measured at HEAD demonstrating that neutralising #551e restores the symptom (an uncaught deleted inline row), preserved at a durable path alongside the coverage rows.
3. FACT TO CHECK: That `#551e` genuinely fails the self-check if the specific inline row in `diff_wdc_identify.c` is deleted.

4. `wdcverdictone`
1. AGREE: The failure mode is claimed to be superseded by `#551f` which reds the count check anyway (`ROW:wdcverdictone:the triage pass's reason`).
2. CLOSURE RECORD: CLOSED as OVERTAKEN by #551f. OWED: A discriminating control measured at HEAD that neutralises #551f and restores the symptom (accepting a log with both PASS and FAIL), preserved at a durable path.
3. FACT TO CHECK: That `#551f`'s count check reliably triggers a failure when a log contains BOTH `WDC_IDENTIFY_PASS` and `WDC_IDENTIFY_FAIL`.

5. `armcpabsent`
1. DISAGREE: The row describes a live, reachable defect ("fatals and falls through, with Undefined Instruction delivery still commented out" - `ROW:armcpabsent:title`), leaving work owed.
3. FACT TO CHECK: Whether the emulator actually fatals and falls through on an uninstalled ARM coprocessor access instead of injecting a guest Undefined Instruction exception.

6. `armdwordalign`
1. DISAGREE: The row describes a live defect where ARMv6 LDRD/STRD instructions incorrectly mask addresses instead of permitting word alignment (`ROW:armdwordalign:title`), leaving work owed.
3. FACT TO CHECK: Whether an ARMv6 guest with U=1 performing a word-aligned LDRD/STRD experiences the incorrect `~7` masking at HEAD.

CLOSEDRAFT_09: 4 AGREE, 2 DISAGREE

## Batch 10 -- `ascoutresid` (DOCUMENT-AND-CLOSE), `m88kconvdelivery` (DROP), `qharmarchlevel` (DROP), `qharmexalign` (DROP), `qharmmediaver` (DROP), `cxlaunchcov` (DOCUMENT-AND-CLOSE)

### `ascoutresid`
1. DISAGREE - The state_note explicitly says "the repair is the report only", naming work that is still owed.
2. (N/A)
3. Closing would be wrong if the repair to the report has not actually been implemented and merged.

### `m88kconvdelivery`
1. AGREE - The row is only an ID assigned to an existing prose entry, meaning no new defect needs to be tracked here.
2. Row dropped. This row was created merely as an ID for an existing prose entry. The defect (m88k float-to-int conversion exceptions) is already tracked in OUTSTANDING_BUGS.md lines 1549-1558 at db8b1a33, making this duplicate row not worth a round.
3. Closing would be wrong if OUTSTANDING_BUGS.md lines 1549-1558 at db8b1a33 do not actually track this specific defect.

### `qharmarchlevel`
1. AGREE - The row acts as an ID for an existing prose entry without opening a new entry.
2. Row dropped. This row serves as an ID for an existing prose entry. The defect (ARM CPU table missing architecture level) is already tracked in OUTSTANDING_BUGS.md lines 3022-3040 at db8b1a33, so this redundant row is not a defect worth a round.
3. Closing would be wrong if OUTSTANDING_BUGS.md lines 3022-3040 at db8b1a33 do not actually describe the ARM CPU table architecture level defect.

### `qharmexalign`
1. AGREE - The row assigns an ID to an existing prose entry without a second entry being opened.
2. Row dropped. This row is just an ID for an existing prose entry. The unaligned LDREX and STREX defect is tracked in OUTSTANDING_BUGS.md (lines 3625-3626 and 4181-4202 at db8b1a33), so this row is not a new defect worth a round.
3. Closing would be wrong if OUTSTANDING_BUGS.md lines 3625-3626 and 4181-4202 at db8b1a33 do not actually track this LDREX and STREX defect.

### `qharmmediaver`
1. AGREE - The row is an ID for an existing prose entry, and no second entry is opened.
2. Row dropped. This row serves as an ID for an existing prose entry. The ARMv6 media encodings decoding issue on ARMv4 CPUs is tracked in OUTSTANDING_BUGS.md lines 1870-1872 at db8b1a33, making this duplicate row not worth a round.
3. Closing would be wrong if OUTSTANDING_BUGS.md lines 1870-1872 at db8b1a33 do not actually track the ARMv6 media encodings issue.

### `cxlaunchcov`
1. AGREE - The coverage debt is above the floor, graded as no floor breach, and is already disclosed in the controls' CONTRACT, requiring no changes.
2. Row closed as documented. The launcher controls' coverage debt (`wc -w` passing after-column checks and PK keys codex rc 7/8 on row names) was assessed and not changed. It is disclosed in the controls' CONTRACT and causes no floor breach.
3. Closing would be wrong if the controls' CONTRACT does not actually disclose this specific coverage debt.

CLOSEDRAFT_10: 5 AGREE, 1 DISAGREE

## Batch 11 -- `dupidcheck` (CLOSE-OVERTAKEN), `m88kwtbit` (DOCUMENT-AND-CLOSE), `mipspagemaskdead` (CLOSE-OVERTAKEN), `i8259aeoi` (DOCUMENT-AND-CLOSE), `i8259ltim` (DOCUMENT-AND-CLOSE), `i8259ocw3revert` (DOCUMENT-AND-CLOSE)

1. `dupidcheck`
1. DISAGREE. The row's own text names work still owed (a separate harness round that "owes two negative controls"). 
2. (N/A)
3. The separate harness round has already merged at HEAD, bringing the uniqueness guard and making this duplicate-id defect truly absent.

2. `m88kwtbit`
1. DISAGREE. The row's own text describes a live, reachable defect (the `.wt` bit CPU-STOP halt reaches valid `lda` and `xmem` instructions in user mode).
2. (N/A)
3. The MC88100 manual explicitly mandates a CPU halt/exception for user-mode `lda` and `xmem` instructions when the `.wt` bit is set.

3. `mipspagemaskdead`
1. DISAGREE. The row's own text names work still owed (the VR41xx 1 KB-page round T11 "should delete or justify the arm").
2. (N/A)
3. The VR41xx T11 round has already merged at HEAD and fully removed the dead `case 0x00007ff:` arm.

4. `i8259aeoi`
1. AGREE. The text states a documented approximation where no interrupt is lost and no documented guest is affected.
2. RECORD: Closed as DOCUMENTED. The i8259 model does not store the ICW4 byte to clear the ISR bit upon acknowledge, but this approximation leaves no interrupts lost because the output line does not consult the ISR and documented guests use specific EOI instead of AEOI.
3. A newly documented or supported guest OS specifically programs and relies on ICW4 AEOI behavior and the ISR bit state to function.

5. `i8259ltim`
1. AGREE. The text confirms the model's edge-only limitation is unobserved since documented guests program edge mode.
2. RECORD: Closed as DOCUMENTED. The i8259 model provides an edge-only implementation and drops ELCR writes. This approximation is sufficient and unobserved because both documented malta guests explicitly program ICW1 for edge-triggered mode (0x11).
3. A supported guest attempts to program and rely on level-triggered mode (LTIM), causing interrupts to be lost due to the edge-only approximation.

6. `i8259ocw3revert`
1. DISAGREE. The row's own text explicitly names work still owed (the ISR-selected-prior case "is the row owed with any implementation").
2. (N/A)
3. The owed ISR-selected-prior case has already been fully implemented or filed as its own tracked ledger row.

CLOSEDRAFT_11: 2 AGREE, 4 DISAGREE

## Batch 12 -- `i8259priority` (DOCUMENT-AND-CLOSE), `i8259smm` (DOCUMENT-AND-CLOSE), `lecsr12readback` (DOCUMENT-AND-CLOSE), `lecsr3inert` (DOCUMENT-AND-CLOSE), `pit8253pendingptr` (DOCUMENT-AND-CLOSE), `lancetxtempty` (DOCUMENT-AND-CLOSE)

1. `i8259priority`
1. AGREE. The row explicitly confirms that priority rotation is unimplemented and no known guest depends on the missing inhibition, as they mask in the handler (`i8259priority:state_note`).
2. RECORD: Assessed the missing priority inhibition and rotation; left unchanged because known guests mask in handlers and do not depend on it.
3. FACT TO CHECK: That no newly added or other guest OS depends on the OCW2 R bit for priority rotation.

2. `i8259smm`
1. DISAGREE. The row's own text explicitly names work still owed by stating "Impact otherwise NOT CHECKED (the 0x68 arm and the datasheet's SMM semantics)" (`i8259smm:state_note`).
2. N/A
3. FACT TO CHECK: The actual hardware SMM semantics from the datasheet to ensure the 0x68 arm does not affect state beyond the absent ISR inhibition.

3. `lecsr12readback`
1. AGREE. The read-back behavior is confirmed as stored-whole, pinned by contract rows, and documented as satisfying MAME diagnostic requirements (`lecsr12readback:state_note`).
2. RECORD: Assessed CSR1 bit 0 and CSR2 bits 15:8 read-back ambiguities; left as stored-whole to satisfy MAME requirements, pinned by #573 contract rows.
3. FACT TO CHECK: That the contract rows in #573 actually assert and test the stored-whole read-back for these specific bits.

4. `lecsr3inert`
1. DISAGREE. The state note only explains that BSWP governs un-emulated DMA byte lanes, leaving the impact and safety of the ACON and BCON bits completely unassessed (`lecsr3inert:state_note`).
2. N/A
3. FACT TO CHECK: The hardware function of ACON and BCON to verify the model safely ignores them without breaking guest expectations.

5. `pit8253pendingptr`
1. DISAGREE. The row describes a WRONG-RESULT defect that was removed by #574 retiring the event at acknowledge (`pit8253pendingptr:state_note`), meaning the honest closure is OVERTAKEN (requiring a discriminating control) rather than DOCUMENT-AND-CLOSE.
2. N/A
3. FACT TO CHECK: That the stale pointer left in `machine->isa_pic_data.pending_timer_interrupts` is strictly dead code and never dereferenced during a machine reset or teardown.

6. `lancetxtempty`
1. AGREE. The row correctly identifies a documentation hazard with empty carrier files rather than a product code defect (`lancetxtempty:title`).
2. RECORD: Assessed empty Am7990 scratchpad datasheets; documented that their watermark-only content cannot be used to prove datasheet absences.
3. FACT TO CHECK: That the 3,015 bytes in Am7990_ds.txt strictly consist of watermark lines and do not contain accidentally obscured datasheet text.

CLOSEDRAFT_12: 3 AGREE, 3 DISAGREE

## Batch 13 -- `leiadrbit0` (DOCUMENT-AND-CLOSE), `pciabsentallones` (DOCUMENT-AND-CLOSE), `rs5c313gmtime` (DROP), `sprstringsbound` (DOCUMENT-AND-CLOSE), `srecbytecount` (DROP), `ppcifetchdeclineprod` (CLOSE-OVERTAKEN)

### 1. `leiadrbit0`
1. AGREE: `leiadrbit0:triage_pass` establishes that this is a documented interpretation of the datasheet that safely issues a warning.
2. RECORD: Closed as DOCUMENTED. The emulator's treatment of CSR1 bit 0 in the `init_block_addr` was assessed; it remains unchanged as it is a documented interpretation of the datasheet that appropriately issues a warning.
3. FACT TO CHECK: The actual silicon behavior of the physical hardware when CSR1 bit 0 is set, to ensure the emulator's interpretation does not fatally diverge from real devices.

### 2. `pciabsentallones`
1. AGREE: `pciabsentallones:triage_pass` states the behavior is explicitly documented as an intentional emulator-compatibility oracle.
2. RECORD: Closed as DOCUMENTED. The config read returning all-ones only for register 0 (and zero for others) on an absent PCI device was assessed; it remains unchanged because it is an intentional, documented compatibility oracle.
3. FACT TO CHECK: Whether this specific non-standard absence response actually causes guest OS PCI probes or drivers to hang or crash instead of safely skipping the absent device.

### 3. `rs5c313gmtime`
1. AGREE: `rs5c313gmtime:triage_pass` claims the missing check is strictly unreachable by guest input.
2. RECORD: Closed as DROPPED. The missing NULL check on `gmtime()` returning from `time(NULL)` is dropped because it cannot be reached or exploited via guest input; it strictly consumes the host environment's time.
3. FACT TO CHECK: Whether the host's standard C library is ever deployed in an environment where `gmtime()` can legitimately return NULL for valid `time_t` values, crashing the emulator unconditionally.

### 4. `sprstringsbound`
1. AGREE: `sprstringsbound:triage_pass` states the bounded input from the in-tree header makes the OOB write impossible.
2. RECORD: Closed as DOCUMENTED. The latent OOB-WRITE in the build tool's array indexing was assessed; it remains unchanged because the strictly bounded input from the in-tree `ppc_spr.h` (topping out at 0x3ff) inherently prevents the overflow.
3. FACT TO CHECK: Whether any out-of-tree builds, user-supplied configurations, or future automated header generators could inject an SPR value >= 1024 into the build tool.

### 5. `srecbytecount`
1. AGREE: `srecbytecount:triage_pass` claims the overflow is benign, affecting only a debug print for impractical files.
2. RECORD: Closed as DROPPED. The integer overflow on the byte counter is dropped because it strictly affects a debug print and practically requires loading an impossibly large (> 2 GiB) S-record file.
3. FACT TO CHECK: Whether the `int` byte counter is silently reused elsewhere in the parsing logic for memory allocation or buffer indexing, which would turn a print error into memory corruption.

### 6. `ppcifetchdeclineprod`
1. DISAGREE: `ppcifetchdeclineprod:state_note` names work still owed by stating the regress review "names the cheaper measurement: a window sweep" on bebox, prep, macppc, and mvmeppc, which have not been recorded as completed.
2. (Skipped because DISAGREE)
3. FACT TO CHECK: Whether the `vgagfxwindowend` fix actually eliminates the declining instruction-width read on all referenced arms (bebox, prep, macppc, mvmeppc), which can only be proven by executing and verifying the owed sweeps.

CLOSEDRAFT_13: 5 AGREE, 1 DISAGREE

## Batch 14 -- `ppcifetchibinit` (DOCUMENT-AND-CLOSE), `fmtmissargwitness` (DROP)

### ROW `ppcifetchibinit`

1. AGREE. The text confirms the stale decode is already neutralized because the shipped fix returns on every failed read (`ppcifetchibinit:state_note`), leaving no reachable defect.
2. RECORD: Closed as documented. Assessed the uninitialized `ib[4]` causing stale stack word decodes on build-dependent variants. The issue is neutralized because the shipped fix returns on all failed reads, meaning `ib` is never decoded after a failure.
3. CHECK: Someone must verify that in every listed build-dependent variant (W5, D7, V7, D12, V12), the shipped fix definitively returns on a failed read and cannot bypass the failed-read block to decode `ib`.

### ROW `fmtmissargwitness`

1. AGREE. The text explicitly declares "the fix is in" and that the owner is authorized to drop it as documented-only (`fmtmissargwitness:state_note`), indicating no further work is owed.
2. RECORD: Dropped by ruling (fable 5.1 code-scanning final ruling). The missing single rung-3 ATTEMPT for the PS2 timer-hold read and non-byte MB89352 access is recorded as an honest NON-attempt. The fix is already in. 
3. CHECK: Someone must verify that the `fmtmissarg` witness field genuinely renders as an honest NON-attempt and does not accidentally output the same rendering as a "tried-and-could-not" attempt.

CLOSEDRAFT_14: 2 AGREE, 0 DISAGREE


## Batch 15 -- `wdcperopcode` (DOCUMENT-AND-CLOSE), `offlinescope` -- FULL state notes; SUPERSEDES their batch-05 entries

### Row `wdcperopcode`

1. `AGREE`: The text successfully refutes the claim that this is a defect by defining it as a "SPEC choice" that actively bounds guest flooding, which is already pinned by an existing coverage row (`wdcperopcode:state_note`).
2. RECORD: Closed as documented: The per-device unimplemented command latch is an intentional specification choice to bound guest flooding, not a defect. The `unimpl 2op` coverage row actively pins this scalar behavior by verifying that two different opcodes yield only one line.
3. The ONE fact that would make closing wrong: A verification at HEAD showing that the `unimpl 2op` row does not exist or fails to enforce the single-line output constraint for multiple differing opcodes.

### Row `offlinescope`

1. `DISAGREE`: The text explicitly names work still owed, stating that three differentials do not compile and admitting "the flags are mine to fix" (`offlinescope:state_note`). 
2. (N/A)
3. The ONE fact that would make closing wrong: Verification that the three failing differentials (`diff_diskimage_geom`, `diff_fbpending_bound`, `diff_ieee_store`) remain uncompilable at HEAD and their gate flags have not been corrected.

CLOSEDRAFT_15: 1 AGREE, 1 DISAGREE
