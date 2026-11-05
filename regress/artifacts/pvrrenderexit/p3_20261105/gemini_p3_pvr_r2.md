# Gemini 4 Argon (gemini web proxy) -- job `p3_pvr_r2`, banked by the main loop at 2026-11-05 08:54Z

* source: _scratchpad/gweb/jobs_20261105_rounds/p3_pvr_r2/gemini_web.out (mtime 2026-11-05 02:51:25 local, 2523 bytes)
* sender verdict line: GWEBP3PVRR: 4 ATTACKS 2 BROKEN 2 HOLDS 0 UNSETTLED DRAFTABLE:NO
* NOTE: the sender RE-SENDS a job whose answer lacked a verdict line and OVERWRITES its .out, so this file is the
  answer on disk at banking time; an earlier answer to the same job, if any, survives only where a disposition quotes it.

---

VERDICT: REPAIR

**1. FLOOR on the composite:**
*   **BROKEN (Floor Breach):** An edit deleting only the `z1` swap `tmpf = z1; z1 = z2; z2 = tmpf;` at 1:665 (or 1:738) leaves all 68 rows green.
*   **Derivation:** The bounds explicitly mandate covering operand swaps drawn from fields the guarded body reads. `simpleline` reads `z1` at 1:682 (`double z = z1`) and uses it for the depth test (1:686). However, the probe's `SWAP` geometry is defined as `tri(SWAP, 2.0, 0xff0000)`, giving all three vertices a uniform Z value of 2.0. Because `z1` and `z2` are identical, skipping their swap leaves `z = 2.0` completely unchanged. (The exact same vulnerability applies to the swaps of `r1`, `g1`, and `b1`).
*   **Row that would red it:** None. `yedges_swap` and `texyedges_swap` expect the swapped X coordinates to draw correctly, but since Z and color are perfectly uniform across the span, the rendered pixels are identical whether the swap occurs or not.
*   **Denominator:** The 68-row shipped composite detector.

**2. THE DIFF:**
*   **HOLDS (Geometry):** The geometry sweep perfectly matches the claims. `RSPAN`'s dx/dy slopes yield a span of exactly 639.0 to 669.5 at y=430. `TOP` accurately spans 275..325 at y=0. `BOTTOM` spans from y=450 down to y=509, correctly reaching 479 and 480. `SWAP` reaches y=180 exactly at `startx = 435.0` and `stopx = 365.0`.
*   **BROKEN (False Record):** In `regress/gate_arm.sh` (2c), the gate comment claims there are "fifteen render sessions". This is mathematically false. Pass 2 originally had 12 sessions. Repair 2 added `yedges`, `texyedges`, and a `mask` session that was explicitly split into two (`mask` and `mask25`) due to the 16-command timeout documented in `base68/SPLIT_NOTE.md` (2d). 12 + 4 = 16 sessions, not 15. The comment missed the timeout split.
*   **HOLDS (mask25 row):** The `mask25` row was rightly added. The pass 2 ruling falsely claimed textured headers set word 1 bit 25. As stated in Section 0 and 2b, the probe's `header()` writes word 1 as `0` or `0x04000000` (bit 26) and the `texture1` bit is completely ignored. Without adding the dedicated `mask25` session, the `K2_mask25_and3` widening variant would have been completely green (a missed floor breach).

**3. VERDICT:**
REPAIR the missing variable-swap detection inside the `x1 > x2` block (e.g., varying the Z or color across the `SWAP` triangle) and correct the session count in the gate comment from 15 to 16.

P-GWEBP3PVRR-3a86
GWEBP3PVRR: 4 ATTACKS 2 BROKEN 2 HOLDS 0 UNSETTLED DRAFTABLE:NO