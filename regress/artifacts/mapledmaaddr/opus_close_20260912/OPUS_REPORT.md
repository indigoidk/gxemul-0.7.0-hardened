OPUS_CLOSE528_20260912 — the Opus 5 measuring seat's CLOSING-PASS report on `mapledmaaddr` (#528), verbatim, saved
because an Agent seat leaves no file in a panel dir.  Brief: _scratchpad/brief_maple_close_20260912.md (scriptable seats
in _scratchpad/panel_20260912_190504/).  Every artifact it cites is in this directory.  (The harness rendered `>` as an
HTML entity in the returned text; restored here, nothing else changed.)

---

OPUS_CLOSE528_20260912

First line of CHECKPOINT.md, verbatim:
`# CHECKPOINT -- 2026-09-12 ~15:1x   HEAD 7457c04 (records)   #528 mapledmaaddr IN FLIGHT`

**VERDICT: SURVIVOR:** a diagnostic deferred to process exit via `atexit()` registered in the read arm — `static void maple_dmaaddr_atexit(void){ fatal("[ dreamcast_maple: DMAADDR was read ]\n"); }` plus, after `odata = d->dmaaddr;`, `if (!maple_ax_reg) { maple_ax_reg = 1; atexit(maple_dmaaddr_atexit); }` — **scored 37/37** (`regress/artifacts/mapledmaaddr/opus_close_20260912/probe_M_ATEXIT.raw`). The oracle does **not** close.

---

## What I measured (scratch clone `/tmp/gxopus528`, sentinel cleared, SEC never written)

| leg | edit | RESULT | `read silent` | log |
|---|---|---|---|---|
| BASE | the shipped fix | 37/37 | 0/12 | `probe_BASE.raw` |
| M_LIVE (control) | `fatal("[ … DMAADDR read ]\n");` **during** the read | 36/37 | **12/12 FAIL** | `probe_M_LIVE.raw` |
| **M_ATEXIT** | the same diagnostic **deferred to exit** | **37/37** | **0/12** | `probe_M_ATEXIT.raw` |

All builds rc=0, binary FRESH (`[ gxemul -nt src ]`). The live-diagnostic control proves the oracle *does* catch an in-line announce; deferring the identical announce to `atexit` walks straight past it. Artifacts (diffs, build logs, non-eq capture, README) are in `regress/artifacts/mapledmaaddr/opus_close_20260912/`.

**Non-equivalence — MEASURED** (`noneq_atexit.txt`, pty held open past `quit`):
```
exit=exit0   read-happened: True (r3 = 0x12345678, the DMAADDR field)
IN_SNAP(pre-quit):  False      -> invisible to noise()  -> 37/37
IN_FULL(post-quit): True       -> it DOES print
tail: 'print r3\r\n0x12345678\r\nGXemul> quit\r\n[ dreamcast_maple: DMAADDR was read ]\r\n'
```
The fix emits nothing; the mutant emits `[ dreamcast_maple: DMAADDR was read ]` at every process exit that saw a DMAADDR read. Not equivalent, and it reinstates the diagnostic half of the removed defect (the interval-silence-is-FLOOR target) — just outside the window the oracle watches.

## Q1 — a diagnostic the exact-transcript oracle cannot see

**Yes: any byte the device emits AFTER `SNAP` is captured.** `session()` sets `SNAP = buf` immediately *before* typing `quit`, and `noise()` reads `SNAP`. So the whole interval `quit` → shutdown → `atexit` → stdio-flush is unobserved. `atexit` is the concrete, reachable C edit from this arm (MEASURED above). The channel is real, in-band (same pty/stdout — `IN_FULL: True`), and non-equivalent. This is the class recurring a **fourth** time: table 4→5 moved the blind spot from "a shape inside the grammar" to "the interval after the last command," and the repair reproduced the class inside itself.

The other candidates in the brief, assessed:
- **Text inside a partially-compared line** (disasm mnemonic/comment; a `print` line matched only as one hex line): **not reachable from this arm.** The disassembly line and its `; rN = 0x…` annotation are printed by `cpu_dyntrans.c`/`sh_cpu_disassemble_instr` *before* `I;` executes the instruction (READING, confirmed in source); the device read runs during execution, after that line's newline. No injection point into an owed line's uncompared tail. Correctly disclosed.
- **Newline-less output (glue / stdio line-buffering):** **caught** — it flushes onto the next prompt line and reds the echo (this is exactly M_GLUEPROMPT 36/37 from table 5). In every read session the maple read is the last stepped instruction, so the glue target is the prompt, never an owed-line tail. READING, consistent with the prior measurement.
- **Output that REPLACES (bare `\r`):** caught by the `bare_cr` term (M_CRDIAG 36/37, table 5).
- **stderr:** the pty carries stderr too (`pty.fork` dups slave to 0/1/2); and stderr is unbuffered, so it would appear live and red. Not an escape.

## Q2 — is the oracle sound?

- **False red on a CLEAN session (real):** the owed model is strict and the read windows are fixed (`spin=1.2 s` on the last command, `0.20 s` between). Under host load a not-yet-arrived owed line reads as "line missing" → red, with no tolerance in the silence row itself. Mitigated by the four controls and by BASE measuring 37/37 five times here, but it **is** a load-sensitive oracle (Fable's pass-2 point) — gate 10 must run ALONE. The trailing-`tail ∈ {"", "GXemul> "}` clause correctly absorbs the final-prompt race; that part is sound.
- **Dead session passing (does not happen):** a crash/`exit(1)` truncates the transcript → owed lines missing → red (HEAD reds at 11/37). So dead → red. Good.

## Q3 — does the repair chain close?

**No — one MEASURED survivor.** Denominator I swept: the two live controls (M_LIVE killed 36/37; BASE 37/37) plus the atexit deferral (37/37), on top of the 20+ mutants tables 1–5 already killed (reinstatement whole/half, the eight-cell selector generating set, consumer-keyed declines/exits, width, value cells, sibling write, read-clear, third-read, and every in-window diagnostic shape incl. blank/CR/prompt/glue/quit-line). The class is unchanged: **a silence oracle that stops observing at a point in time has, by construction, an interval to hide in** — the whitelist-of-shapes became a whitelist-of-*time*. A future escape here is **"a breach of the contract, as stated"**, not "outside it": the interval-silence-is-FLOOR ruling says a diagnostic of *any* shape announcing the read must red `read silent`, and this announces it. Closure: read the **full** transcript through EOF and have `owed()` model the `quit` echo plus the deterministic shutdown lines, so exit-time output reds. (The snapshot-before-quit was adopted to drop table 4's `quit`-echo *exemption*; the fix is to MODEL that echo, not to stop short of it.)

## Q4 — which of the brief's claims is wrong

- **"The only disguise left is a diagnostic that emits no byte (`fatal("")`: EQUIVALENT)."** (Diff comment line, docstring, and the pass-history box.) **MEASURED FALSE.** A diagnostic that emits a full line still hides — if it emits it *after the snapshot*. `fatal("")` is not the only survivor; `atexit(fatal…)` is one too, and it emits bytes.
- **"the snapshot is taken before `quit` … so nothing is exempt."** (docstring / diff.) **FALSE as written** — precisely *because* the snapshot is taken before quit, **everything after it is exempt.** The exemption wasn't removed; it was generalised from one line (`GXemul> quit`) to an unbounded time window.
- Everything I could check from the tree held: `fatal()` prints unconditionally and returns (READING, `debugmsg.c:384-390`, no early-out); the disasm-before-execute ordering (READING, `cpu_dyntrans.c:272-312`); "no 8-byte callback" (READING). The premise I could **not** independently settle from this packet is the completeness of tables 1–4's own kills — I re-measured only the silence channel and the two controls, and trusted killtable5's SCORES for the rest.

*Seat note: agy was not fired (measuring seat held per the roster reservation); this is the Opus compile-and-measure seat's own build+measure.*
