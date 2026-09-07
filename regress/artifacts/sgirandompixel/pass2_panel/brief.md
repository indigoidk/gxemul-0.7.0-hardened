# PASS 2 -- `sgirandompixel`: the diff, the table, and one question.  2026-09-06.  SHORT BY DESIGN.

## WHAT THIS IS
An ordinary correctness review of a graphics-engine device model in a hardware simulator for obsolete
workstations (GXemul 0.7.0, a maintained fork).  Plain engineering vocabulary; no security framing intended.
**Tree: `GXEMUL-SEC/src/`** -- ignore any other `src/` under the project root.  **VERDICT LINE FIRST.**

## PLEASE DO NOT SIMPLY RATIFY -- and if every premise holds, say so plainly
A previous brief of mine closed by insisting one premise must be wrong; a seat correctly named that
instruction itself as the unsupported assumption.  So: check them, and "all hold" is a valid answer.

## SETTLED PREMISES (re-inlined; packet-fed seats cannot check these)
1. **`fatal()` PRINTS AND RETURNS in this fork** -- `src/core/debugmsg.c`, `void fatal` is
   `va_start`/`va_debug`/`va_end`, **no exit of any kind**.  The early-out is on `debug()`, not `fatal()`.
2. `horrible_getputpixel()` switches on `tlb_mode = (mode >> 10) & 0x7` and implements 0, 1, 2, 4.
   `DE_MODE_LIN_B` is `0x1400` -> **5**, unhandled.  It is one of the FIVE modes `crmfbreg.h` documents.
3. The helper is **PER-PIXEL** -- called inside line, rectangle and tiled-MTE loops.
4. The panel chose **member 3 (DECLINE + LATCHED ANNOUNCE)** in grok's MINIMAL scope; codex's fuller form
   (an explicit success result, every GET site suppressing its dependent PUT) is FILED as `sgirandomskipput`.

## THE DIFF (product code; the only behavioural change)
The arm previously did `fatal(...)` with its `exit(1)` commented out, then `*color = random(); return;`.
Now it declines: `*color` is left alone, and the announce is latched on a FRESH bit at the enum's documented
next-free position (`SGIRE_W_BADMODE = 1 << 10`), preserving the file's scan-to-the-last-enumerator property.
The caller's own `uint32_t color = fg;` therefore stands, so the PUT writes **fg** -- deterministic, and still
a write the guest did not ask for, which is exactly what `sgirandomskipput` records.

## TEST-FIRST, IN THE ORDER THE ORACLE-CORRECTION RULE REQUIRES
The oracle was **re-pinned first**, the **committed build measured RED** under the new expectations
(`7/8`, preserved as `prefix_repinned_RED.out`), and only then was the code changed.  Post-fix: **8/8**.

## THE KILL TABLE (`killtable/`, BASE 8/8 opening AND closing, clone clean, no sentinel)
Every score re-derived by DIFFING each result against `BASE.out`, not from the driver's echo.

| mutant | score | rows red |
|---|---|---|
| `M_RANDOM` -- verbatim reinstatement (random + unlatched announce) | 6/8 | value, latch count |
| `M_ZERO` -- guard kept, repair nulled (`*color = 0`) | 7/8 | value only (`0x0`) |
| `M_NOLATCH` -- drop the latch guard | 7/8 | latch count, **4 vs 1** |
| `M_SILENT` -- member 2 instead of 3 | 6/8 | both diag rows |
| `M_EXIT` -- restore `exit(1)` | 4/8 | four rows; machine dies |

## TWO DEFECTS THE FIRST TABLE FOUND IN MY OWN INSTRUMENT, disclosed rather than left for you
* **`lin_b diag once` was VACUOUS BY CONSTRUCTION.**  The probe drew a **1x1** rectangle, so an *unlatched*
  announce also fired exactly once and `M_NOLATCH` escaped **8/8**.  Repaired by making the rectangle
  **1 wide x 4 tall** -- HEIGHT not width, because LIN_A addressing is `ofs = x & 4095` (y ignored), so four
  rows rewrite the same byte and the value oracle survives, while four columns would overlap and destroy it.
* **`M_RANDOM` was MIS-BUILT** -- it also silenced the announce, so it reddened three rows and died for two
  reasons.  Corrected to restore both halves the fix changed, which is what clause (b) actually asks for.

## THE QUESTION
**Which of these is wrong?**  (i) member 3 in the minimal scope, rather than codex's fuller form now;
(ii) leaving `*color` untouched so the PUT writes fg, rather than zeroing it; (iii) the latch on its own fresh
bit; (iv) `lin_b not src` kept as a non-discriminating regression guard (true before AND after) rather than
dropped; (v) the five filed residuals -- `sgirandomskipput`, `sgirelinb`, `sgirandomcolour`,
`sgitileptrsilent`, `sgirenamedstmode` -- being filed rather than taken in-round.

VERDICT LINE FIRST (`SHIP` / `ONE MORE REPAIR: <which>` / `DO NOT SHIP`), then the answer with its
denominator -- which cells and which mutant shapes you swept -- then anything else.  Under a page.
