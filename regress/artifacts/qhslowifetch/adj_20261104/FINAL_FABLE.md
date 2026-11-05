# Cloud routine answer, banked VERBATIM by extract_teleport.py at 2026-11-04 23:36:49Z

* source: the local transcript of `claude --teleport` -- `C:/Users/User00/.claude/projects/C--Users-User00-AppData-Local-Temp-claude-d0d925bc6bb158fc-ccd8e376-b626-4ae7-b60a-ecf2767f320e-scratchpad-tpfinqhsf/e1151302-14e4-406f-8efd-2eed953e057b.jsonl`
* session: `https://claude.ai/code/session_015fEQzJxcbDNYfsemzM1zvy`   trigger: `trig_01TH7Mv4UA9ZDmhcQPEDVQYy`   packet: `_scratchpad/w_qhs/FINAL_QHS_cloud.md`
* the answer's message: timestamp 2026-11-04T23:28:41.778Z, model field `claude-fable-5-1` (all assistant models in the transcript: ['claude-fable-5-1', 'claude-haiku-5-5'])
* delivery token `CLOUDFINALQHS`: present; 7555 characters; PART markers N = 0, present 0, MISSING none; `END OF PARTS`: NO
* safety-classifier notices in the transcript: none
* the run's final line: CLOUDFINALQHS: 8 RULINGS 4 CHANGES 3 FILED VERDICT:APPLY-WITH-CHANGES

---
CLOUDFINALQHS
model: claude-fable-5-1 (the configured id; the serving model may differ)
VERDICT: APPLY-WITH-CHANGES. Eight rulings: four change (F1, F2, F4, F7), four keep (F3, F5, F6, F8), three items filed (ppc_exception's MSR table, the multiprocessor checkstop, the -T halt on read-ahead). The C change stays sound; the sweep runs first, then table 2 runs once on the final row count.

F1. CHANGE. Quotes A and B settle it: memory.c clears `running` on every CPU and returns true, and nothing on that path touches single_step. My sentence was false as written and grok's refutation stands. The replacement states the one difference the code shows, which is F3's scope difference, and still says nothing about how a non-interactive run ends. Final text, appended to arm (d)'s comment:

```
                Only this CPU's running is cleared: a
                checkstop is a per-processor state, and
                the run loop stops this CPU at the end of
                the batch.  memory.c's -T halt clears
                every CPU's running; on a multiprocessor
                the other CPUs keep running past this
                checkstop (#PPP; no multiprocessor PowerPC
                machine in the measured set).
```

The landing check that fills #NNN and #MMM must fill #PPP and #QQQ (F2) too: grep the landed file for any unfilled "#[A-Z]{3}".

F2. CHANGE, option (iii). The architecture is unambiguous (Book III v2.01 Figure 28; PEM Table 6-8), and the consequence is inside this fix's own arm: with ME left set, a second failing fetch takes a second machine check where hardware checkstops, and if the machine-check vector itself is unreadable the emulator loops on machine checks forever instead of stopping. One line after ppc_exception() in the ME-set branch of arm (d), SRR1 already holding the old MSR:

```
                ppc_exception(cpu, PPC_EXCEPTION_MC);
                /*  A machine check clears MSR[ME] (Book III
                    v2.01 Figure 28; SRR1 holds the old MSR),
                    so a second failing fetch checkstops as
                    hardware does.  ppc_exception() clears
                    only EE, RI and PR (#QQQ).  */
                cpu->cd.ppc.msr &= ~PPC_MSR_ME;
```

Row: ME-set, pc at a declining address, step, then reg; want ME clear after the exception and a checkstop on a second decline. Needs a producer pmppc does not have, disclosed next to D6, D9 and D10. FILE one row for ppc_exception()'s MSR modelling as a whole: per-interrupt clearing of IR, DR, FE0, FE1, FP, SE, BE and ME, with the local line above moving into ppc_exception() when that row is done. That change touches every guest's exception entry and is not this fix's scope.

F3. KEEP per-CPU in the code, FILE the multiprocessor case. A checkstop is a per-processor state in the architecture; what other processors do is platform behaviour, not architectural. Per-CPU is correct for the arm. The filed defect is grok's: on a two-CPU machine the process does not return to the prompt after the checkstop. Measurement as grok gave it: a two-CPU PowerPC machine, force the fallback on CPU 0, read CPU 1's running and whether the prompt returns. The arm's comment now states the scope (F1), so the shipped text is true either way.

F4. CHANGE the P14 disclosure to name both routes to the cell: a device window declining an offset inside a page whose other offsets succeed, and a -T halt on a read-ahead that walks past a window's end inside the same page. Ruling on part 2, conditionally:
- If part 2 reaches arm (a) on any window: a row is owed. `T cont` with pc at that window's last word, pinning the halt line's address (the word past the window end, which the guest never fetched), running 0, pc after the batch, and the halt count. W7 (arm (a) deleted) then becomes a measured variant, since the failure falls to (c)'s park during read-ahead and the park's batch-ending effect survives the read-ahead return. HEAD exits on this row. The cell is then measured, not disclosed.
- If part 2 reaches no window's arm (a): the disclosure says "measured", not "derived". Part 2 covers every window `device list` names, the slack top is page-aligned, and read-ahead never crosses a page, so there is no interior left to derive. One condition: the sweep records the word fetched at each last word, since reachability depends on it decoding to a valid non-branch instruction and the RTC window's words can be time-varying.
- FILE regardless: memory_rw's -T path halts on a read-ahead fetch the guest has not reached, and arm (a) cannot undo it. That is a -T false positive owned by memory_rw.c, not this fix.

F5. KEEP. Eight windows, 211 offsets, MSR 0 and 0x1000, step from the debugger in real mode without -T is the measurement I asked for, and the offset count matches the lengths. The NIC mirror and the second UART belong in it and are in it. Nothing is missing. Two requirements on the pass criterion: NOT_REACHED must be backed by evidence the word was fetched (pc advanced or the unimplemented-instruction line), not only by the absence of the checkstop and machine-check text; and the cpc700_pci data word is measured in the reset state of its address register, which the record should say.

F6. KEEP; the re-prediction is right. RAM fetches take the host-page fast path (quote D), so `ctl live` cannot red. On `noT` the zero-fill at 0x02040000 succeeds, the inverted test enters the block with running 1 and MSR 0, and the checkstop reds `noT unimpl` and `noT chkstop`, the same two rows as D15. On the -T sessions the read fails, the block and (c)'s park are both skipped, and the uninitialised word decodes: W5's red set, including `again`. Record the inversion's red set as D15's `noT` reds plus W5's -T reds, so the gate's reader sees why D15 and the inversion agree on `noT` and differ under -T.

F7. CHANGE. Quote C shows ppc_exception() calls ppc32_pc_to_pointers(), and (d) relies on it. Drop the clause. The refresh code in (b) stays, since removing code from an arm no session reaches buys nothing. Final text for arm (b):

```
            /*  (b) The translation in memory_rw raised an
                ISI or 603 IMISS: ppc_exception() saved
                SRR0/SRR1 and moved pc to the vector.
                Reached on no measured session (the
                dispatch pc lookup translates this address
                first); kept so a delivered exception is
                not doubled by (d).  Not watertight: when
                the vector equals the failing address, pc
                equals addr again, (b) is skipped and (d)
                delivers a second exception over SRR0/SRR1
                (#MMM; no producer on any machine measured).
                next_ic must follow pc; ppc_exception()
                re-resolves it, and (d) relies on that.
                The refresh here is redundant and harmless.  */
```

F8. KEEP the list; nothing to add or remove. Three preconditions. First, the window sweep (parts 1 and 2) runs before table 2, and if part 2 owes a row the count becomes 52 again and table 2 runs once on that count, never twice. Second, "base" is the final candidate with the F2 line in it, so the base run is also the measurement that the ME clear reds no pmppc row. Third, the gate's literals (row-name list, "rows green N", key-line counts, score-claims form) are regenerated for the final count, and every SCORES line states the row count it ran on, which repairs table 1b's record too.

CLOUDFINALQHS: 8 RULINGS 4 CHANGES 3 FILED VERDICT:APPLY-WITH-CHANGES
