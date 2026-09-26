OPUS_SEAT_ALIVE_20260925_551f2
# CHECKPOINT -- 2026-09-25 ~19:35 (087a90 sections rewritten; the peer's sections below are untouched)

VERDICT: The pipe close is REQUIRED, not optional. M19 is a real, built escape via the gate's file redirect; the pipe kills it; M18's four cells are all caught. File the pipe with `wdcidlane` before the chain closes.

All three were built and run, not reasoned. MINE_f.c 7fd15d1d; repo sources untouched (diff_wdc_identify.c ef662cb5, dev_wdc.c 71407161, gate_offline.sh 7e7927e2). Scored with gate 2's real `lib.sh` + H + G and the real `selfmutant.py`. Artifacts: `regress/artifacts/wdcidselfcheck_20260925/opus551_measured_f2/` (`analyze_f2.out`, `reallane_f2.out`, `verify.out`, variant sources, logs).

**1. M19 — grok's heal handler is MEASURED, and it escapes on the file channel.**
Built as grok describes: a `constructor` registers an `atexit` handler that, when `cmp_fails>0 && failures==cmp_fails`, `fflush`es, `fseek`s stdout to 0, writes a healthy log over it, and buries the old tail (I embedded the real pristine healthy log and padded newlines; `ftruncate` is hidden by `-std=c99`, so grok's newline-pad is the buildable form). Comparators, rows, tallies and self-check untouched.
- **File redirect (what the gate runs), per device: GREEN / GREEN / GREEN / GREEN on pristine, dropold, drqring, w57hi — all `128/0 PASS`. ESCAPES = dropold, drqring, w57hi.** The gate's `[0-9]+ failures` capture sees exactly one match, `0`, in the rewritten log. Proof it rewrote: drqring's file log is 65984 lines ending `128 rows, 0 failures` / `WDC_IDENTIFY_PASS`; the same run's pipe log is the real `128 rows, 2 failures` / `WDC_IDENTIFY_FAIL` with both report lines.
- **The self-mutant lane does NOT catch it.** `selfmutant.py` on the pristine device (the device the real gate's lane uses) returns SELFMUTANT_OK for M19 — heal never fires on pristine (`cmp_fails==0`). The lane goes SETUP only on drqring/w57hi/dropold, which the real gate never runs.
So in the real regression scenario — someone breaks `dev_wdc.c` so a covered comparison fails — M19 rewrites the file-redirected log and the gate passes. Neither the main checks nor the pristine lane see it. This is the boundary's own class, and it is real.

**2. M18 — all four resets are caught, both channels.**
Unconditional `failures = 0` and `cmp_fails = 0`, each before the reconciliation and after the count printf: **red on every defect device, green on pristine, ESCAPES = none, on file and pipe alike.** The (B) report line prints at the moment of failure, so a trailer reset cannot take it back — the same result the roster's other resets gave. "Reasoned red" is now measured red.

**3. The pipe close works, and its negative control passes.**
Re-running M19 with `"$bin" 2>&1 | cat > "$log"`: **red / red / red on the three defect devices** (`128/2 FAIL` etc.) — `fseek` on an unseekable pipe returns non-zero, heal bails, the real failing log reaches the checks. **ESCAPES = none.** And it does not disturb the healthy path:
- pristine under the pipe is GREEN, and the pristine log is byte-identical file-vs-pipe (`cmp` clean) for both F and M19;
- the lane is inherently pipe-based (`selfmutant.py` uses `Popen(stdout=PIPE)`), so it is unchanged — F and M19 both SELFMUTANT_OK on pristine.
So the one-line change (`"$WDCBIN" 2>&1 | cat > "$WDCLOG"`, or `tee`) closes M19 with its own negative control satisfied, and costs the healthy run and the lane nothing.

**Bearing on the contract.** M19 confirms Fable's M19 refinement: it is not (C) "rows not run" and not the (B) residual — the rows run and report; the process rewrites the log afterward. (C) must generalise to "observables forged: rows skipped with their labels, OR the log rewritten by the process after the rows ran," and the close is the pipe, filed with `wdcidlane`. Until the pipe is in the gate, (B)'s "a printed line cannot be taken back" is true of an in-file check but false of the process that owns the file descriptor — the sentence should be scoped to "no in-file edit takes it back; a process that rewrites the fd is closed by reading the log through a pipe (filed)." M18 needs no wording change; it was already inside (B), now measured.

---
*Recorded by the main loop: agent a088149d37f1fac24 (resumed to measure M19, M18 and the pipe control), final text by claude-opus-4-8 at 2026-09-26T01:04:52.473Z, extracted verbatim from the agent transcript.  Badge s.*

**FALLBACK -- NOT COUNTED AS THE OPUS SEAT.**  `agent_models.py` on the transcript: a REFUSAL event by claude-opus-5-5 at 00:54:51Z, then 26 runs by claude-opus-4-8; this text is the fallback model's.  Its MEASUREMENTS are artifacts (`opus551_measured_f2/`) and were re-scored by the main loop against #551g's own gate-2 wdc block, extracted verbatim, with the tree's `lib.sh` (`measured/rescore_m19.out`): M19's file-redirect log on drqring 0 failures (green), its pipe log 2 (red), the two saved M18 logs 2 each (red); the 551g block's executable lines are identical to the tree gate's (73 checks each), so the seat's scoring against the tree gate is equivalent.

