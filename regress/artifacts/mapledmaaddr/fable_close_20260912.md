FABLE_CLOSE528_20260912 — Fable 5.1 (claude-fable-5-1)

(Verbatim answer of the flagship adjudicating seat on the CLOSE of `mapledmaaddr` (#528)'s repair chain, fired LAST on
2026-09-12 as an Agent-tool subagent pinned to `model: fable`, READ-ONLY (gate 10 running), after the closing pass
(`panel_20260912_190504/`, `opus_close_20260912/`), the final pass (`panel_20260912_201452/`, `opus_final_20260912/`) and
kill tables 5-7.  Brief: `_scratchpad/brief_maple_fable_close_20260912.md`.  The harness rendered `<`, `>` and `&` as HTML
entities in the returned text; they are restored here and nothing else is changed.)

---

FABLE_CLOSE528_20260912
claude-fable-5-1
`# CHECKPOINT -- 2026-09-12 ~21:4x   HEAD 7457c04 (records)   #528 mapledmaaddr IN FLIGHT (table 7)`

**VERDICT: CLOSES on table 7 — the chain closes, and I am RATIFYING the ruling I held for, with one of my OWN pass-2 dispositions marked WRONG. Denominator checked: table 7's 21 runs (16 legs on the shipped FROZEN7 + 5 on FROZEN6), 21/21 exactly on POSTTABLE prediction, on top of tables 1-6's cumulative kills and Opus's close/final sweeps — every measured mutant is killed except the two that are DISCLOSED outside the contract (M_TICKPERIODIC4, emulated-time-beyond-span, 37/37 by construction; M_FILE, off-pty channel). I can construct NO survivor inside the stated contract: the in-band pty channel is closed within the session's emulated span (full-line owed() compare + bare-CR term), the termination axis is closed for every read session (unclean(): EOF-within-cap AND exit0), and the only hiding spots left are the two genuinely-unbounded/off-channel axes that are correctly disclosed plus fatal("") which is MEASURED EQUIVALENT. NOT ready to commit until gate 10 is re-run ALONE on FROZEN7 (the current gate log certifies a superseded T4 instrument), the gate comment is corrected to cite tables 2-7, and the CHANGELOG/OUTSTANDING/ledger/manifest land with the grades below; the FIX has been committable since pass 1. Evidence basis: I read the tree and every table's PRETABLE/SCORES/POSTTABLE and both Opus reports; I built and ran nothing (gate 10 concurrent, per instruction).**

I verified against source, not the packet: `dev_dreamcast_maple.c:547-590` (the fix and the read arm), `fix.diff`, `maple_dmaaddr_probe.py` (owed/disasm_line/noise/unclean/session), `cpu_sh.c:1108-1135` (disassembler prefix), `cpu.c:400-422` (`cpu_run_deinit`, the two shutdown ticks), `cpu_dyntrans.c:206/272-282` (disasm-before-execute, single-step tick), `dev_dreamcast_maple.c:68/135/666` (`MAPLE_TICK_SHIFT 17`), `debugmsg.c` (fatal path), the table-7 mutator, and `gate_sh_rounding.sh:1641-1668`.

---

## Q1 — does the chain close on table 7? Is the enumeration complete and each disposition right?

**Yes, it closes.** The verification is measured, not asserted, which is the bar my pass-2 rule set ("the closing pass VERIFIES the enumeration rather than hunts cells"): POSTTABLE.out records 21/21 on prediction, the four table-6 escapes (`M_EXITATQUIT`, `M_ABORTAT4`, `M_SLOWATEXIT4`, `M_DISASMHOOK`) reproduced 37/37 on FROZEN6 and then killed 36/37 on FROZEN7 on the *same binaries*, and BASE 37/37 ×3 (×6 with table 6) gives the load-sensitivity control.

I re-derived the two load-bearing comparisons rather than trusting them:

- **disasm_line() is exact — read AND measured.** `cpu_sh.c:1133` prints `"%08x"` then `":  %04x %s"` with `"   "` (non-delay) then the running-mode indicator `"    "` (`cpu.c:438`, else-branch) = 8 spaces after the opcode, then the mnemonic, then `"\t; r%i = 0x%08x"` (`cpu_sh.c:1304`). `disasm_line()` produces byte-for-byte that. It is additionally proven by BASE=37/37 (the line matches) together with M_DISASMHOOK=36/37 (a changed tail reds). No stepped instruction is a delay slot or draws the `" <- "` arrow (running=1 during step), so the single non-delay/4-space model is complete for what the probe steps.
- **Every read session's termination is now folded in.** `noise()+unclean()` is applied over all 12 entries of `READS` at line 468, so the "exit status read in ONE session" gap Opus found is closed for all twelve.

**Each enumeration cell's disposition is right:**

| axis | cell | disposition | check |
|---|---|---|---|
| channel | stdout ±newline, stderr | COMPARED | glue reds the next prompt (M_GLUEPROMPT 36/37); stderr on the pty, live (opus_final M_STDERR) |
| channel | a file / syslog | DISCLOSED | off the operator console (M_FILE 37/37, opus_final) — correct |
| timing | during step; first-step + 2 deinit ticks | COMPARED | defer-1/2 killed 12/12, defer-3 killed 2/12 (opus_final ladder) |
| timing | a later emulated tick | DISCLOSED WINDOW | M_TICKPERIODIC4 37/37 — unbounded axis, survives by construction |
| exit | normal / nonzero / signal, every read session | COMPARED | M_EXITATQUIT/ABORTATQUIT 36/37, M_ABORTAT4 36/37 |
| no-byte | fatal("") | EQUIVALENT | va_debug emits nothing for an empty format (verified) |

The one adversarial cell I pushed hardest on — a synchronous in-window print that reproduces an owed line in position — cannot escape: `noise()` compares in order line-by-line, so any extra line shifts the rest to mismatch, and the only zero-net-line outcomes are `fatal("")` (EQUIVALENT) or output beyond EOF/off-channel (disclosed). **The in-band, in-span channel is genuinely closed.**

## Q2 — the emulated-time window: disclose vs row; bound; coupling

**Disclosing it is the RIGHT grade, and it is forced, not chosen.** A session has no terminal event in *emulated* time (unlike process exit), so free-running F ticks only moves the boundary to F — the axis is unbounded and cannot be closed into a floor. The carrier lists "effects keyed on the environment (time, ...)" as clause (e) precisely for this. Grading it floor would be the unbounded-row-growth (#392) shape.

**The stated bound is correct as written.** `MAPLE_TICK_SHIFT=17` → 2^17 steps per tick in free-run; under single-step `ticks_till_next` starts at 0 so the tick fires once on the first step and then needs 2^17 more (no session reaches it); `cpu_run_deinit()` (`cpu.c:411-416`) runs two ticks of every device unconditionally. So a session sees the first-step tick + two shutdown ticks ≈ three. This is not reasoned — Opus MEASURED the 2/3/4 ladder (defer-2 caught everywhere, defer-3 only where the read is the first instruction, defer-4 never), which is exactly the "it would sweep the table is a MEASUREMENT, never an inference" rule.

**The coupling is disclosed adequately for a record, and I recommend one cheap strengthening (FILE, not a blocker).** The header states that because the transcript runs through the two shutdown ticks, `read silent` also asserts every dreamcast device is silent on them, and that a future device print would red all twelve and "read as the DMAADDR read speaking." That warns a future reader. It is satisfied today (BASE 37/37 ×6 proves no dreamcast device prints at shutdown now), so the hazard is purely future. **A one-session control that runs `quit`→deinit WITHOUT reading DMAADDR and asserts ITS transcript is silent would convert the coupling from disclosed to OBSERVABLE** — if another device ever prints at shutdown, that control reds too, distinguishing "another device speaking" from "the read speaking." Worth filing; not owed for close, because disclosure meets the bar the brief itself sets and no such print exists.

## Q3 — grades for the CHANGELOG

- **(a) exit-status-at-exit** (`M_EXITATQUIT`/`M_ABORTATQUIT`/`M_ABORTAT4`, 36/37): the `exit(1)` half of the removed defect, deferred to process exit and keyed on the read — a FLOOR breach (clause (b) reinstatement of the exit half at a new site), caught by `unclean()`'s per-session exit0/EOF check. **L1** (pre-ship construction; the detector never shipped). Not L2 — L1/L2 only diverge for *shipped* material.
- **(b) atexit / time-axis** — split, and the split is the point: the HOST-process-exit `atexit` announce (`M_ATEXIT`, 36/37) is a FLOOR breach (a diagnostic shape, now in-window because the transcript reads through EOF), caught, **L1**; the EMULATED-time-beyond-span periodic report (`M_TICKPERIODIC4`, 37/37) is **clause (e), DISCLOSED window** — correctly NOT floor, and it MUST survive (a kill would mean the window is narrower than stated and the record wrong).
- **(c) disassembly prefix** (`M_DISASMHOOK`, 36/37): FLOOR breach — text passed off as a disassembly line is a diagnostic shape the contract claims — caught by the full-line `owed()` compare. **L1**.
- **(d) bounded read** (`M_SLOWATEXIT4`, 36/37): an oracle-COMPLETENESS fix (`rd(10.0)`'s result now gates `unclean()`), not a shipped-mutant escape; **L1** construction. Note it is double-caught (no-EOF AND non-exit0), so either check alone would hold.
- **(e) proportion — NOT fully proportionate, and partly my fault.** Seven tables for a two-line ACCEPT fix, almost all on the silence oracle. The honest split: tables 3→4→5 were a cell-by-cell grind on ONE class (a whitelist oracle has a shape to hide in — literal → grammar → count → exemption), and the class-closure amendment ("two consecutive passes finding one class → close the whole space in ONE diff") should have short-circuited that directly into table 6's whole-transcript-through-EOF model. Table 5 was worse than idle: it *regressed* the class onto a new time axis. Tables 6→7 were legitimate — the emulated-time axis is a genuinely new, unbounded axis that required Opus's tick-ladder to discover and bound, and the floor-channel hardenings (full-line disasm, exit0, EOF) could NOT be filed because they are floor breaches. **Net ≈ two avoidable tables (4,5).** It could not have "disclosed earlier and filed the rest" for the in-band channel — that channel is floor. The durable lesson is structural and already a CHECKPOINT candidate: **build a silence oracle as an exact whole-transcript compare from the start, never iterate up from a whitelist.**

## Q4 — WHICH OF MY DISPOSITIONS IS WRONG (count named: one of substance)

**My pass-2 §Q3 closure PRESCRIPTION was wrong, and the round adopted it as table 5.** I wrote: *"Closure, in one diff: (i) `session()` snapshots the buffer BEFORE it writes `quit` and `noise()` reads the snapshot — then no exemption is needed."* That snapshot is exactly what created the atexit/time blind spot Opus measured in the closing pass (`M_ATEXIT` 37/37). I correctly diagnosed the disease — *a count with an exemption is a whitelist* — and then prescribed a cure that **generalised the one-line exemption (`GXemul> quit`) into an unbounded time window after the snapshot.** The correct closure was table 6's, which Opus stated against me directly: *"the fix is to MODEL that echo, not to stop short of it"* — read the FULL transcript through EOF and model the `quit` echo. This is the sharpest thing in the round: the seat holding the class-closure gavel handed the round a repair that reproduced the class on a new axis. It is the #499 shape (a breach reproduced inside its own repair) arriving from the adjudicator's chair, and it cost table 5's entire pass.

Everything else of mine held and was adopted correctly: D1 (alignment is a clause-(e) value cell of the body-read field, not "outside the BOUND" — the header now says so, and the old L4 sentence is gone), D2 (`case 0x00` is FLOOR via the eight-cell single-bit selector generating set — all eight now rowed), F3/F5 (the two (e) sub-reasons stated separately), and the HOLD-for-class-closure itself. I checked the header for any residual overclaim: the unqualified "ANY ... printed late" that Opus graded L4 is corrected to the stated window; "however long it waits" now correctly refers to HOST-exit handlers, which red via `unclean()` even when their output is never read, and is distinguished from the emulated-time disclosure.

## Q5 — ready to commit once gate 10 is green on this probe?

**Not on gate-green alone.** Ready when ALL of:
1. **Gate 10 re-run ALONE on FROZEN7.** CHECKPOINT records the current gate log (`..._T4INSTRUMENT.log`) certifies a *superseded* probe; the gate reads `regress/maple_dmaaddr_probe.py` at invocation, so update `rungate_shr528.sh`'s cmp line to FROZEN7 and re-run with nothing else running (the oracle is load-sensitive; this is the third independent BASE sample I required in pass 2). **Do not edit the probe between now and that invocation** — Python loads the file at startup, and a concurrent gate would measure whichever version is on disk when it gets there.
2. **Records fixes:** the gate comment at `gate_sh_rounding.sh:1645` cites "kill tables 2-5" — correct to 2-7; and the `exit status` row note (`marker survive` carries the exit(0)-at-read case) — though `unclean()` now also catches it via transcript truncation.
3. **CHANGELOG/OUTSTANDING/ledger(fable)/manifest** land with the grades above and the two disclosed axes named.

The fix itself (`odata = d->dmaaddr;`, ACCEPT, undisputed by any seat across five passes) has been committable since pass 1; the detector is the thing that reached completeness only now. **Optional strengthening to FILE:** the non-DMAADDR silence-control session for the shutdown-tick coupling (Q2).

*Seat note: this is the flagship adjudicating seat (Fable 5.1, `claude-fable-5-1`), fired LAST as instructed, READ-ONLY (gate 10 concurrent). agy held per the measuring reservation. I ratify CLOSES on measured evidence while recording my own pass-2 closure prescription as the round's one wrong disposition of substance.*
