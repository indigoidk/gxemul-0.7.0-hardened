# Cloud routine answer, banked VERBATIM by extract_teleport.py at 2026-11-04 23:11:59Z

* source: the local transcript of `claude --teleport` -- `C:/Users/User00/.claude/projects/C--Users-User00-AppData-Local-Temp-claude-d0d925bc6bb158fc-ccd8e376-b626-4ae7-b60a-ecf2767f320e-scratchpad-tpadjqhso/afafac43-bd1a-412d-adc9-37f9f82254ea.jsonl`
* session: `https://claude.ai/code/session_015fEQzGjHbVksHjqLrwg9Kr`   trigger: `trig_01PjPaDyZNk9KvHWCrwjvmLt`   packet: `_scratchpad/w_qhs/ADJ_QHS_cloud.md`
* the answer's message: timestamp 2026-11-04T23:02:17.791Z, model field `claude-opus-5-5` (all assistant models in the transcript: ['claude-haiku-5-5', 'claude-opus-5-5'])
* delivery token `CLOUDADJQHS`: present; 7668 characters; PART markers N = 0, present 0, MISSING none; `END OF PARTS`: NO
* safety-classifier notices in the transcript: none
* the run's final line: CLOUDADJQHS: 31 RULINGS 5 CHANGES 2 FILED VERDICT:APPLY-WITH-CHANGES

---
CLOUDADJQHS
model: claude-opus-5-5 (the configured id; the model actually serving this turn may differ)
VERDICT: APPLY-WITH-CHANGES. The C code stands. You need to change four dispositions (P1, P9, P15, P24) and amend the cited evidence in one (P8). The probe is now 52 rows, so every score claim has to be measured again on it before it lands.

## 1. Rulings P1–P28

**P1: UPHOLD, with the text amended.** The scope belongs to a different clause than the one your text puts it on. GLM's "reaches (c)" was a limit on the park claim. Once the cause is corrected, the claim is about `running`, and memory.c clears `running` on any -T report. On a step, that report comes from the single-step read before the arm ever runs. So "a -T halt that reaches (c) leaves running at 0" wrongly gives (c)'s route the credit. Your text also leaves out the second job the park does, which D3 shows: without the park, pc moves on to 0x2040004. Final text:
```
                (After a -T halt memory.c has left running
                at 0, so the run loop does not enter this
                CPU again: a further step or continue runs
                nothing.  The park in (c) only ends the
                current batch and keeps pc at addr.)  */
```

**P2: UPHOLD**, both the comment change now and filing the signal as a LOW latent row. I checked the scenario. An ISI is a translation failure, not a missing-memory report, so `running` stays 1 even under -T, and (d) does run. I also dropped "rather than rely on ppc_exception having done so" (see P24). Final text:
```
            /*  (b) The translation in memory_rw raised an
                ISI or 603 IMISS: ppc_exception() saved
                SRR0/SRR1 and moved pc to the vector.
                Reached on no measured session (the
                dispatch pc lookup translates this address
                first); kept so a delivered exception is
                not doubled by (d).  Except when the
                vector is addr itself (a fetch at the ISI
                or IMISS vector): pc == addr again and (d)
                runs over the saved SRR0/SRR1 (filed).
                next_ic must follow pc; refresh it here.  */
```

**P3–P7: UPHOLD.**
- P5: I recounted and there are nine sessions.
- P6: after P9, the reworded gate comment must also stop saying UNIMPLEMENTED is absent on `noT`, because `noT unimpl` now requires it to be present.

**P8: UPHOLD, with the evidence amended.** Cite "(D3, D4: also without the park)". D3 is the cleaner witness: no park, pc moved, and `again nonex` still reads 2.

**P9: OVERTURN, for being incomplete.** Adding both rows is right. "Repaired in this round" isn't true yet, for two reasons:
- Only base, D14 and D15 have been run on the 52-row probe. The 18 variants of table 1, HEAD (predicted 33/52), the three null media and the gate's "rows green 50" pin all still stand on the 50-row probe.
- D15's description doesn't fit its own score (see P15).

The replacement: rerun everything on p52, update every 50-row claim to 52, and record D15's exact diff.

**P10: UPHOLD.** D14 is caught only by the three chkstop rows.

**P11: UPHOLD**, with Mythos's notes. One correction: the step-count rows pin "a single-step read plus a translator read per step" (P20's transcript), not a "trace read". All nine stay green on B1, which fits their role as premises.

**P12–P14: UPHOLD.**
- P13: the measured claim covers the device bases and the slack only. The device interiors are still open (section 4, item 3).
- P14: record it as a derivation, not a measurement.

**P15: UPHOLD measuring the six, but OVERTURN the prediction for the inversion.** Mythos predicts that the inverted failure test reds `ctl live` with a checkstop at 0x2000. That requires ctl's first fetch to go through this `memory_rw`. If it does, D15 (the block running after a successful read too) would also have hit that checkstop on ctl, yet D15 scored ctl green. Either D15 is not the edit it is described as, or ctl never reaches the slow path and the inversion is caught elsewhere (the new `noT` rows, plus W5-style rows from decoding garbage). Re-predict before you run table 2.

**P16, P17: UPHOLD.** For P16, the docstring has to say the `again` session measures nothing about re-entry.

**P18: UPHOLD.** The errata should also say that D14 is where the chkstop rows are the sole channel.

**P19–P23: UPHOLD.** For P20, the docstring wording is: "the single-step read's report, its 'could not read the instruction' line, then the translator's report."

**P24: UPHOLD no code change, OVERTURN the rationale.** By P2's and P11's own statements, the ISI rows deliver the ISI in the dispatch lookup and never enter this arm. So they can't show that `ppc_exception` itself refreshes `next_ic`; Mythos's premise is wrong. Whether (d)'s machine-check exit continues at the vector rests on `ppc_exception`'s source. Settle it by reading its body for `quick_pc_to_pointers`. Meanwhile, the P2 text drops the clause that contradicted (d).

**P25: UPHOLD.**

**P26: UPHOLD**, conditional on `memory_rw.c` really setting `single_step` on its -T path (grep it). Text for (d):
```
                Unlike memory.c's -T halt this does not
                set single_step: without -V the emulator
                stops after the line below.
```

**P27, P28: UPHOLD.**

## 2. Disagreements

- **D-A:** keep all three chkstop rows. D14 measured them as owed, which refutes Grok. Opus's duplication point is true but costs nothing.
- **D-B:** `again nonex` becomes a control, labelled "a -T halt is terminal for the session" (Opus). A red control still fails the gate, which answers GLM.
- **D-C:** Opus's cause, worded as in P1. GLM's scope no longer applies once the park claim is gone. Grok's direction is the same as Opus's.

## 3. The accepted disposition that is wrong

**P9.** The rows are right, but the "repaired" status rests on one variant's run on p52. D15's described edit also conflicts with the ctl prediction behind P15. A smaller error: P1's proposed text puts "reaches (c)" on the wrong clause.

## 4. What every seat missed, by severity

1. **Medium: the p52 baseline was never measured.**
   - What's missing: no seat or disposition required the full rerun.
   - Settled by: SCORES.txt for table 1, table 2, D14/D15, HEAD and the three null media, all on the 52-row probe, with CONTROL=OK on every variant.
2. **Medium: D15 and the inversion prediction contradict each other.**
   - What's missing: one of the two is wrong, and nobody noticed.
   - Settled by: the recorded D15 diff, plus a breakpoint or one-line trace on this `memory_rw` call during the `ctl` session. Does ctl's 0x2000 fetch take the slow path?
3. **Low: the device interiors.**
   - What's missing: the sweep stepped only into each device's base address. ns16550's one `return 0` is reachable inside the window if its mapped length exceeds its register span.
   - Settled by: a fetch at every 4-byte offset of each pmppc device window, plus the last word of each, with MSR 0 and 0x1000. Look for the checkstop text or "[ PPC Exception 0x2".
4. **Low: a -T halt during read-ahead.**
   - What's missing: memory.c clears `running` and prints before arm (a) returns. A read-ahead the guest hasn't reached would still halt the CPU, and (a)'s "touch nothing" can't undo it. It is unreachable on pmppc because 0x02040000 is page-aligned.
   - Settled by: reading `memory_rw.c` to see whether its -T path checks `translation_readahead`. File it if it doesn't.
5. **Info: P24's evidence.**
   - Settled by: reading `ppc_exception`'s body for `quick_pc_to_pointers`.

CLOUDADJQHS: 31 RULINGS 5 CHANGES 2 FILED VERDICT:APPLY-WITH-CHANGES
