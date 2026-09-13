# `mapledmaaddr` (#528) PASS 2 — the real diff, its 16-row detector and a measured kill table, before commit

VERDICT LINE FIRST, then the liveness token `PASS2_MAPLE_20260912`.

**ONE QUESTION: is there a mutant of this fix — inside the clause-(d) enumeration below — that stays GREEN on all 16
rows?**  If you find none, say WHAT YOU SWEPT.  **Please do not simply ratify**: on pass 1 of this very row three seats
found three wrong fixes that passed my brief's summary of the detector; they are rows now, and I want the next three.

Tree: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` (ignore any other `src/` under the project root).

## THE DIFF (uncommitted), `src/devices/dev_dreamcast_maple.c`, WHOLE

```diff
@@ -560,9 +560,11 @@ DEVICE_ACCESS(dreamcast_maple)
 			/* debug("[ dreamcast_maple: dmaaddr set to 0x%08x"
 			    " ]\n", d->dmaaddr);  */
 		} else {
-			fatal("[ dreamcast_maple: TODO: read from dmaaddr ]\n");
+			/*  #528: answered like MAPLE_ENABLE's read -- the field is
+			    the one the write arm stores and maple_do_dma_xfer()
+			    consumes -- with no diagnostic and no exit.  This read
+			    used to compute the value and then end the emulator.  */
 			odata = d->dmaaddr;
-			exit(1);
 		}
 		break;
```

The enclosing function (unchanged elsewhere): `uint64_t idata = 0, odata = 0;` at the top; `switch (relative_addr)`
with arms 0x04 (this one), 0x10 RESET2 (write: fatal() on nonzero; read: odata stays 0), 0x14 ENABLE (read: `odata =
d->enable`), 0x18 STATE (write 1 runs `maple_do_dma_xfer()`; read: 0), 0x80 SPEED, 0x8c RESET, 0xe8, default (fatal, no
exit); common tail `if (writeflag == MEM_READ) memory_writemax64(cpu, data, len, odata); return 1;`.
`memory_rw.c` delivers a failed device access as an exception for MIPS and M88K only — on this SH4 machine a handler
`return 0` silently skips the load.

## SETTLED (pass 1, Fable 5.1 adjudicating; `regress/artifacts/mapledmaaddr/fable_pass1_20260912.md`)

* ACCEPT is right, 9/9.  No `writeflag` other than MEM_READ/MEM_WRITE reaches this handler (279 call sites scanned).
* The FLOOR: the accept cell with a POISONED destination and high + low-five-bit values; silence over the whole read
  interval (any maple text, not one literal); `other read` (the hoist deletes the dominating `relative_addr == 0x04`);
  survival + exit status.  Value-keyed exits (`d->dmaaddr == v`, `& bit`) are clause (e), taken as L1 rows because cheap.
* The post-DMA value is NOT rowed here — deferred by name to the separate row `mapledmaadvance`.

## THE DETECTOR — `regress/maple_dmaaddr_probe.py`, 16 rows, real SH4 `mov.l` on unmodified `-E dreamcast`

Every load destination is seeded 0xa5a55a5a first.  Nine READ sessions (each a fresh emulator process): `read val_a`
(write 0x8c012345, read), `read val_b` (0x0c00001f), `other read` (write 0x8c012345, read RESET2 at +0x10, want 0),
survive (read DMAADDR on a fresh device into r2, then a marker store; rows `marker survive` and `exit status`),
`initial zero`, `read four`, `read all ones` (0xffffffff), `double read 1/2` (write 0x8c012345, read twice), `write
replace` (write 0x8c012345 then 0x13579bdf, read).  `read silent` counts read sessions whose transcript contains the
text `dreamcast_maple` anywhere (want 0/9).  Controls: a RAM round trip at start and end, SH4 IPRD reset value, and
MAPLE_SPEED's shift/mask (0x12345678 -> 0x12340000).

## MEASURED — kill table 1 (`regress/artifacts/mapledmaaddr/killtable_20260912/`), frozen instrument, scratch clone

| leg | edit | score | failing |
|---|---|---|---|
| BASE | the fix | 16/16 | — |
| HEAD | committed (fatal + exit) | 5/16 | 11 rows |
| M_KEEPFATAL / M_REWORD / M_LATCHED | the diagnostic verbatim / reworded / latched `(once)`, no exit | 15/16 each | read silent alone |
| M_EXITONLY | exit(1) after the load, no diagnostic | 6/16 | 10 rows |
| M_RET0 | `return 0` (the FAULT idiom) | 7/16 | 8 value rows + read silent (memory_rw's failed-access `debug()` prints under stepping) |
| M_DECLINE | the assignment deleted | 9/16 | 7 value rows |
| M_HOIST | `odata = d->dmaaddr` at the declaration, the arm emptied | 15/16 | other read alone |
| M_READCLEAR | `d->dmaaddr = 0` after the load | 15/16 | double read 2 alone |
| M_EQ4 / M_BIT30 / M_ZEROEXIT | exit if `== 4` / `& 0x40000000` / `== 0` | 15, 15, 13 | read four / read all ones / initial zero + survive |
| M_MASKLOW | `odata = d->dmaaddr & ~0x1f` | 9/16 | 7 value rows |

## QUESTIONS

1. **(the one that matters)** DEPENDS-ON for this pure deletion: dominating predicates `relative_addr == 0x04` and
   `writeflag != MEM_WRITE`; the guarded body `odata = d->dmaaddr;` reads only `d->dmaaddr` and tests nothing.  **Name
   any edit inside that enumeration — a re-introduced exit or diagnostic under a different predicate, a weakened
   dominating predicate, an operand swap on `d->dmaaddr` or `odata` — that leaves all 16 rows green**, and the row you
   expected to catch it.  Include width: `memory_writemax64(cpu, data, len, odata)` — every row reads 32 bits.
2. **Does any row's channel fail to vary under the mutant it is named for?**
3. **Which CONTRACT statement in the probe header is false or overclaims?**

Verdict line: `NO SURVIVING (d) MUTANT — swept: <list>` or `SURVIVOR: <exact edit>`.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
