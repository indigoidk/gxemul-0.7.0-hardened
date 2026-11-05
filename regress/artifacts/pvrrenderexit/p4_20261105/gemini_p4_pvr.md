# Gemini 4 Argon -- job `p4_pvr`, banked 2026-11-05 10:47Z

* source: _scratchpad/gweb/jobs_20261105_rounds/p4_pvr/gemini_web.out (mtime 2026-11-05 04:34:30 local, 1699 bytes)
* sender verdict line: GWEBP4PVR: 10 ATTACKS 0 BROKEN 10 HOLDS 0 UNSETTLED DRAFTABLE:YES

---

VERDICT: CLOSE. All enumerations, hardware constraints, and session logic accurately reflect the codebase and constraints provided.

1. VERIFY THE ENUMERATION:
The enumeration is complete and accurate for the class. The input cells total 173. Initial codex is 84 (33 per rasterizer [P1-P8] + 2 fractional + 16 decode). Added cells equal 18 (A1:7, A2:4, A3:4, A7:3). Z-off twins equal 71 ((27 P1-P7 * 2 rasterizers) + 2 fractional + 7 A1 + 4 A2 + 4 A3). 84 + 18 + 71 = 173. Equivalence and undefined behavior classifications hold (e.g., y < -1 and y > ysize read out of bounds). Contract accurately maps the uncovered cells. DENOMINATOR: 173.

2. THE TWINS AND THE CAP:
The Z-off twin want logically matches the Z-on row. Code verification (`dev_pvr.c:687`): `if (!d->zwrite_disabled)` exclusively wraps the `d->vram_z[ofs] = z;` depth store. All geometry, interpolation, and color writing execute identically regardless of the `zwrite_disabled` flag. The 4096-byte refusal is the correct guard. `console.c` FIFO length is 4096. Any input exceeding this before the first maple keyboard tick drains the buffer will truncate (swallowing `quit`). The largest new session is 4060 bytes, safely under the 4096 cap. 

3. THE RECORDS:
The records, errata, and gate block changes hold. `gate_arm.sh` correctly reflects the new 128 row count and 38 render sessions. The errata for `PRETABLE_2.out` (mtime frozen probe exception and Y2 boundary conditions) and `VERDICT.md` (timeout driven by the 4096-byte cap rather than the 90s limit, leaving valid pixel reads intact prior to the truncation hang) are technically precise. 

P-GWEBP4PVR-275f
GWEBP4PVR: 10 ATTACKS 0 BROKEN 10 HOLDS 0 UNSETTLED DRAFTABLE:YES