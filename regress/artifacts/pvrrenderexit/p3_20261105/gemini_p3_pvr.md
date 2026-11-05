# Gemini 4 Argon (gemini web proxy) -- job `p3_pvr`, banked by the main loop at 2026-11-05 08:54Z

* source: _scratchpad/gweb/jobs_20261105_rounds/p3_pvr/gemini_web.out (mtime 2026-11-05 02:51:31 local, 2890 bytes)
* sender verdict line: GWEBP3PVR: 4 ATTACKS 2 BROKEN 2 HOLDS 0 UNSETTLED DRAFTABLE:NO
* NOTE: the sender RE-SENDS a job whose answer lacked a verdict line and OVERWRITES its .out, so this file is the
  answer on disk at banking time; an earlier answer to the same job, if any, survives only where a disposition quotes it.

---

**VERDICT: REPAIR** (1 floor breach, 1 false record).

**1. FLOOR on the composite:**
The class closure is INCOMPLETE for the bound.
*   **Edit**: Deleting the `z` operand swap in `simpleline` (`1:665`: `tmpf = z1; z1 = z2; z2 = tmpf;`) or the identical operand swap in `texturedline` (`1:738`).
*   **Derivation**: The bound includes "operand swaps drawn only from fields the guarded body reads." The guarded body reads `z1` via `z` for the depth test (`1:682`, `1:686`). However, the `SWAP` geometry provided to exercise the reversed-x path (`2a:49`) uses a flat triangle with a constant `z = 2.0` at all vertices (`2a:265`: `tri(SWAP, 2.0, 0xff0000)`). Because `z1 == z2 == 2.0`, deleting the swap leaves the interpolated depth identical across the reversed span. The depth test and pixel color remain exactly correct, keeping all 68 rows green. (The same applies to the color and texture-coordinate swaps).
*   **Row that would red it**: A reversed-x triangle (arriving `x1 > x2`) with a varying `z` depth slope across its span (e.g., `z1 = 2.0`, `z2 = 1.0`), which would write the wrong depth gradient without the swap and fail a depth-read readback.
*   **Denominator**: The early-return bounds (Y, X), the swap block's operands (`x`, `z`, `r`, `g`, `b`, `u`, `v`), the loop bounds, the depth test, the Z-write guard, and the bit-26 decode.

**2. THE DIFF:**
*   **Geometry claims**: HOLDS. The geometries perfectly map to the tested bounds (`2a`). `TOP` reaches `y = 0` and `BOTTOM` reaches `y = 479` to test the vertical bounds. `RSPAN`'s row 430 mathematically starts at exactly `639.0` to hit the right-side bounds. `SWAP` spans exactly `365.0..435.0` without fractional pixels due to its `dx/dy = +-0.5` slopes, allowing `E1` and `E2` to accurately test the exact integer span end.
*   **Mask25 row**: HOLDS. It is rightfully added. The pass-2 adjudication falsely assumed the `texon` sessions already set bit 25 (texture1). As proven in the docstring (`2b`), the textured headers only set word 0 bit 3 and leave word 1 bit 25 as `0`. Without the `mask25` session explicitly setting this bit (`2a:286`), the `K2` mutation (widening the decode to bits 25-26) would evaluate to `0`, fail to disable Z-write, and falsely leave the test green. 
*   **False records**: BROKEN. The updated gate comment in `gate_arm.sh` (`2c:7`) states the detector now comprises "the witness's nine plus fifteen render sessions." This is a false record. Table 1 contained 12 session rows (`3b` SCORES.txt: `zoff`, `ovoff`, `behind`, `texoff`, `texbeh`, `two`, `sticky`, `edges`, `texedges`, `equal`, `texequal`, `zon`). Repair 2 added 4 new sessions: `yedges`, `texyedges`, `mask`, and `mask25` (the latter split into its own session due to the 90-second timeout documented in `2d`). 12 + 4 = 16 render sessions, not 15.

P-GWEBP3PVR-7dcd
GWEBP3PVR: 4 ATTACKS 2 BROKEN 2 HOLDS 0 UNSETTLED DRAFTABLE:NO