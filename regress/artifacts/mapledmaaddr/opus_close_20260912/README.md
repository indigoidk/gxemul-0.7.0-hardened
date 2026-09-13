# opus_close #528 — the fourth oracle does NOT close

Compile-and-measure seat, 2026-09-12/13. Scratch clone `/tmp/gxopus528` (cp -a of build/),
clone-local sentinel, probe frozen from `regress/maple_dmaaddr_probe.py` at launch (cmp IDENTICAL),
baseline = SEC `dev_dreamcast_maple.c` (the fix). Every leg: `rm dev_dreamcast_maple.o && make -j4`,
`[ gxemul -nt src ]` checked FRESH before measuring.

## MEASURED

| leg | what | RESULT | read silent |
|---|---|---|---|
| BASE | the shipped fix, unmodified | 37/37 | 0/12 |
| M_LIVE (control) | `fatal("[ ... DMAADDR read ]\n");` DURING the read | 36/37 | 12/12 FAIL |
| **M_ATEXIT** | **deferred diagnostic via `atexit()`, fires at process EXIT** | **37/37** | **0/12 (SURVIVOR)** |

- `probe_BASE.raw`, `probe_M_LIVE.raw`, `probe_M_ATEXIT.raw` — the three probe runs.
- `M_ATEXIT.diff`, `M_LIVE.diff` — the mutated sources as unified diffs vs SEC.
- `build_*.log` — every build (all rc=0, binary FRESH).
- `SCORES.txt` — the driver's per-leg log; ends `OPUS528_DONE`, sentinel CLEARED (restore CLEAN/FRESH).
- `noneq_atexit.txt` — non-equivalence capture (pty held open past `quit`).

## The survivor

```c
static int maple_ax_reg = 0;
static void maple_dmaaddr_atexit(void)
{
	fatal("[ dreamcast_maple: DMAADDR was read ]\n");
}
...
		} else {
			odata = d->dmaaddr;
			if (!maple_ax_reg) { maple_ax_reg = 1; atexit(maple_dmaaddr_atexit); }
		}
```

## Non-equivalence (MEASURED, `noneq_atexit.txt`)

Holding the pty open PAST `quit`:

```
exit=exit0
read-happened (r3 got value): True         (r3 = 0x12345678, the DMAADDR field)
IN_SNAP(pre-quit): False                    -> invisible to noise() -> 37/37
IN_FULL(post-quit): True                     -> it DOES print
tail: 'print r3\r\n0x12345678\r\nGXemul> quit\r\n[ dreamcast_maple: DMAADDR was read ]\r\n'
```

The fix prints nothing; the mutant prints `[ dreamcast_maple: DMAADDR was read ]` at every
process exit that saw a DMAADDR read. Observably different — not equivalent.

## Why it escapes

`session()` snapshots the pty buffer into `SNAP` immediately BEFORE typing `quit`, and
`noise()` reads `SNAP`. Anything the device emits AFTER that snapshot — at `quit` processing,
during shutdown, or from an `atexit`/deferred latch registered during the read — is outside the
window the oracle observes. Table 4→5 moved the blind spot from "a shape inside the grammar"
to "the interval after the last command". Same class, fourth generation.

## Closure

Observe the FULL process transcript through EOF (not the pre-quit snapshot) and `owed()` the
`quit` echo plus the deterministic shutdown lines, so a diagnostic deferred to exit reds
`read silent`. The snapshot-before-quit was adopted to drop table 4's `quit`-echo exemption;
the exemption must instead be MODELLED, not stopped-short-of.
