# Cloud routine answer, banked VERBATIM by extract_teleport.py at 2026-11-04 23:36:53Z

* source: the local transcript of `claude --teleport` -- `C:/Users/User00/.claude/projects/C--Users-User00-AppData-Local-Temp-claude-d0d925bc6bb158fc-ccd8e376-b626-4ae7-b60a-ecf2767f320e-scratchpad-tpfinqhso/1cb76330-1c24-46d2-ac15-19967312a401.jsonl`
* session: `https://claude.ai/code/session_015fEQzHCuGKq1fwDrSKJfQT`   trigger: `trig_01TqYfrVaUdETnuggwSMcqzw`   packet: `_scratchpad/w_qhs/FINAL_QHS_cloud.md`
* the answer's message: timestamp 2026-11-04T23:29:38.825Z, model field `claude-opus-5-5` (all assistant models in the transcript: ['claude-haiku-5-5', 'claude-opus-5-5'])
* delivery token `CLOUDFINALQHS`: present; 6383 characters; PART markers N = 0, present 0, MISSING none; `END OF PARTS`: NO
* safety-classifier notices in the transcript: none
* the run's final line: CLOUDFINALQHS: 8 RULINGS 4 CHANGES 1 FILED VERDICT:APPLY-WITH-CHANGES

---
CLOUDFINALQHS
model: claude-opus-5-5 (the configured id; the serving model may differ)
VERDICT: APPLY-WITH-CHANGES. The C change still stands. P26's sentence rested on a false premise and is replaced (F1). The MSR[ME] gap is filed against ppc_exception() and disclosed in arm (d) (F2). P14's text is amended for the read-ahead route (F4). The window sweep gains a -T continue leg (F5). The clause in arm (b) that contradicted (d) is dropped (F7). The per-CPU checkstop, the inversion re-prediction and table 2's scope are kept.

**F1. CHANGE.** Quotes A and B refute my premise. memory.c's -T halt clears `running` on every CPU and returns true. Neither path sets `single_step`. "Unlike memory.c's -T halt, this does not request single-step mode" is therefore false, and I withdraw it. The second clause goes too. "So the run loop stops this CPU at the end of the batch" says when the stop takes effect, and nothing measured shows that. Final text for (d)'s checkstop fallback:

'''
                Like memory.c's -T halt, this only clears
                running.  Unlike it, it clears this CPU's
                alone; memory.c clears every CPU's.  A
                checkstop is a per-processor state.  pmppc
                has one CPU.
'''

**F2. FILE (option ii), with a disclosure in (d).** Clearing ME only in arm (d) would fix one row of a table that is wrong as a whole. ppc_exception() also leaves IR, DR, FE0, FE1, FP, SE and BE set, which Figure 28 clears on every interrupt. Clearing IR and DR alone changes how every interrupt vector is fetched, for every guest. The one-line fix in (d) also cannot ship with a regression test, because pmppc has nothing that produces it. That conflicts with the fork's rule. SRR1's mask (0x87c0ffff) already keeps the old ME, so a later fix inside ppc_exception() needs nothing from arm (d). (d) tests ME before it calls ppc_exception(), so its branch logic does not change either. Filed: "ppc_exception() does not apply the architected MSR update (Book III Fig. 28; PEM Table 6-8)", with one row per interrupt class. Add to (d)'s machine-check branch:

'''
                ppc_exception() leaves MSR[ME] set, where
                the architecture clears it on a machine
                check, so a second failing fetch here takes
                a second machine check instead of
                checkstopping (#PPP).
'''

#PPP joins #NNN and #MMM in the landing grep for unfilled placeholders.

**F3. KEEP per-CPU.** A checkstop is a state of one processor, so stopping only the failing CPU is the correct model. memory.c's -T halt stops every CPU because -T is a user policy for the whole machine, not hardware behaviour. On an SMP guest, the other CPUs running on and "All machines stopped" not firing is the expected result. No row, because no multiprocessor PPC session exists. F1's text discloses the difference.

**F4. CHANGE P14's text. The rest depends on part 2.**
- **If part 2 reaches arm (a):**
  - A row is owed for the cell, and W7 (arm (a) deleted) must be measured against it.
  - The row pins three things: the halt comes from memory.c, pc is at the last executed instruction, and nothing in the slot is touched.
  - The underlying defect is memory.c's -T report firing on a speculative read-ahead the guest never executed. That is filed separately against memory_rw.c/memory.c.
  - The pre-fix code exited the process on the same cell, so the fix does not make it worse.
- **If part 2 does not reach it:**
  - Disclose the cell as "derived, not measured", the same as P13. Name the condition: a valid non-branch word in a window's last word, under -T, with `continue`.
  - Add that the decoded word is whatever that register returns. A NOT_REACHED therefore holds for the register contents seen during the sweep, not for every state.

Amended P14: "D12 is reachable only (1) through a window that declines an offset inside a page whose other offsets succeed, or (2) through a -T halt raised by read-ahead past a window's end within its page. The window sweep settles both."

**F5. CHANGE (one addition).** Eight windows and 211 offsets, at MSR 0 and MSR[ME], is the measurement I asked for. The NIC mirror and tty1 must stay in, because the mirror's own access path and the second UART instance are separate code paths. Addition: part 2 must run under -T with `continue`, not only `step 1` without -T. Read-ahead never runs while single-stepping, so a step-only sweep cannot reach the F4 cell. Record each window's registered length beside its result. ns16550's length is 8, which equals its register span, so the source argument P13 depended on holds, and the sweep confirms it by measurement.

**F6. KEEP; the re-prediction is right.** RAM fetches take the fast path (quote D), which explains why ctl stayed green under D15. With the inverted test, the slow-path zero-fill at 0x02040000 succeeds on `noT`. The block is entered with running 1 and MSR 0 and checkstops, so `noT unimpl` and `noT chkstop` go red, the same set as D15. On the -T sessions the read fails, the block is skipped, and the uninitialised `ib` is decoded, giving W5's red set. Condition: this holds only if D15's recorded diff is the constant-true form of the test. If the diff differs, re-derive before table 2.

**F7. CHANGE: drop the clause.** Quote C shows ppc_exception() calls ppc32_pc_to_pointers(). (d) relies on that call, so (b) cannot tell the reader not to rely on it. P24's evidence also changes from the isi rows to quote C plus D13. Final ending of (b)'s comment, with everything before it unchanged from P2:

'''
                (#MMM; no producer on any machine measured).
                ppc_exception() has already refreshed
                next_ic; the refresh here repeats it.  */
'''

**F8. KEEP, with bookkeeping.** The scope is right.
- If the F6 inversion is one of the six P15 variants, count it once. The bound stays 24 edits.
- Add W7 only if F4's condition fires.
- Every score line states that it ran on the 51-row probe and shows CONTROL=OK.
- The gate's literals are regenerated for 51 rows: the row-name list, "rows green 51", the key-line counts and the score-claims form.
- D15's exact diff sits beside SCORES.txt.
- D14 must still go red on `T step chkstop` and `again chkstop` after `T me chkstop` is dropped.
- Nothing is removed.

CLOUDFINALQHS: 8 RULINGS 4 CHANGES 1 FILED VERDICT:APPLY-WITH-CHANGES
