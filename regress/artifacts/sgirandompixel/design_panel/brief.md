# `sgirandompixel` DESIGN -- pass 1.  The witness is BUILT and GREEN; what should the arm do instead?  2026-09-06.

## WHAT THIS IS
An ordinary correctness review of a graphics-engine device model in a hardware simulator for obsolete
workstations (GXemul 0.7.0, a maintained fork).  Plain engineering vocabulary; no security framing is intended
or wanted, and none of this concerns a production system.

**The tree under review is `GXEMUL-SEC/src/`; the file is `src/devices/dev_sgi_re.c`.  Ignore any other `src/`
you find** -- three pristine-2021 upstream copies sit under the project root and are NOT this fork.  Cite by
grep anchor.  **VERDICT LINE FIRST.**

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY
Check the premises, not just the derivations.  **If they all hold, say so plainly** -- a previous brief of mine
closed by insisting one must be wrong and a seat correctly named that instruction as the unsupported
assumption.

## SETTLED PREMISES (each verified by opening the file; re-inlined because packet-fed seats cannot check them)
1. **`fatal()` PRINTS AND RETURNS in this fork.**  `src/core/debugmsg.c`: `fatal()` is `va_start` / `va_debug` /
   `va_end` with **no `exit` of any kind**.  The early-out lives on `debug()`, not on `fatal()`.  *A seat ruled
   the opposite on the witness panel because I failed to inline this; it is the one fact that decides whether
   the code below is reachable.*
2. `horrible_getputpixel()` takes `tlb_mode = (mode >> 10) & 0x7` and implements cases 0, 1, 2 and 4.
3. `crmfbreg.h` defines five modes: TLB_A `0x0000`, TLB_B `0x0400`, TLB_C `0x0800`, LIN_A `0x1000`,
   **LIN_B `0x1400`**.  Those extract to 0, 1, 2, 4 and **5** -- so LIN_B, a documented mode, is unhandled.
4. `src_mode` and `dst_mode` are `d->de_reg[]` entries, written by ordinary stores.

## THE ARM, verbatim
```c
	default:fatal("unimplemented dst_mode %i for horrible_getputpixel (%s), x=%i y=%i\n",
			mode, put ? "put" : "get", x, y);
		// exit(1);
		*color = random();
		return;
	}
```
`*color` is the CALLER'S variable.  On a `get` the caller then writes it to the destination in the same loop
iteration of `draw_primitive()`.

## THE WITNESS, BUILT AND MEASURED TONIGHT (`regress/sgi_re_randompixel_probe.py`, 7/7 on HEAD `79cd12e`)
Real guest instructions, unmodified committed `-E sgi -e ip32`, no `device_add`:

    live           0x5a5a5a5a                LIVENESS through RAM
    devsig         0x1e000000                CRIME_DE_STATUS; RAM reads 0
    copy lin_a     0xaabbccdd                ACCEPT: a LIN_A source copies correctly
    lin_b not src  0x2ee4b4df  NOT 0xaabbccdd    the copy did not happen
    lin_b written  0x2ee4b4df  NOT 0x11111111    the destination WAS written
    lin_b alive    alive                     the host survives
    lin_b diag     yes                       the arm's own diagnostic fired

Two runs gave `0x4b1763a1` and `0x2ee4b4df`, both with bit 31 CLEAR -- glibc `random()` is 31-bit, so
inequality with a source of `0xaabbccdd` is certain rather than 2^-32.

## THE QUESTION: which member of the option set, and what happens to `*color`?
**DELETE · DECLINE (silent) · DECLINE + LATCHED ANNOUNCE · ACCEPT · FAULT · BACKED ACCEPT · IMPLEMENT.**
Member 7 was added yesterday for stubbed PATHS; member 5 (FAULT) IS mechanically available here -- this is the
IP32/MIPS path and `memory_rw.c` dispatches `EXCEPTION_DBE` on a failed device access (anchors
`res <= 0 && !no_exceptions`).

1. **What should `*color` be on a failed GET?**  The three candidates each have a cost: leave it UNTOUCHED (the
   caller's `color` was initialised to `fg`, so the destination gets the foreground -- plausible-looking wrong
   data rather than obviously wrong data); zero it; or **propagate failure so the caller SKIPS the dependent
   PUT**, which is what the pass-2 seat proposed for the sibling `tileptr` arm.  Only the third stops a write
   happening at all, and it needs a return value this `void` function does not have.
2. **Should `LIN_B` simply be IMPLEMENTED?**  Case 4 (LIN_A) is four lines:
   `tile_nr = x >> 12; tileptr = 0x80000000 | (d->re_linear_a[tile_nr] << 12); ofs = x & 4095;`
   and `re_linear_b[]` exists and is written by the same width-checked store path.  **Is LIN_B just LIN_A with
   the other array, or is that a guess that would ship invented behaviour?**  The addition licence wants a
   measured delta or a transferred warrant, never "it cannot hurt".
3. **What is the latch granularity?**  `horrible_getputpixel()` is PER-PIXEL -- called inside line, rectangle
   and tiled-MTE loops, sometimes repeatedly per pixel -- so an announce here without a latch is a per-pixel
   flood.  The house idiom is `N = 1` per device instance with `(once)` in the message text; this file already
   uses `SGIRE_W_UNMAP_RD/WR` bits.  **Does the announce belong here at all, or at the command-wide validation
   point before the loops?**

## THE OBLIGATION THIS ROUND OWES, stated so the panel can check it
The witness currently PASSES when the defect is PRESENT.  After the fix its oracle must INVERT.  The
oracle-correction rule is explicit about the order: **re-pin the oracle FIRST, measure the committed build RED
under the new expectations, and only THEN change the code** -- otherwise the re-pin is indistinguishable from
fitting the test to the binary.  **Which rows should the post-fix instrument assert?**  That depends on the
answer to question 1, which is why it is asked first.

## THE SECOND QUESTION, with the count named
Of the four premises above -- (i) `fatal()` returns; (ii) cases 0/1/2/4 implemented; (iii) LIN_B is documented
and extracts to 5; (iv) both mode words are ordinary writable device registers -- **is any wrong?**

VERDICT LINE FIRST (`MEMBER <n>: <what happens to *color>` / `PREMISE <n> IS WRONG: <what>`), then the
post-fix row set, then anything else.  Under a page.
