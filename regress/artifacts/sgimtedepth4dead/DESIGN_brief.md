# DESIGN — `sgimtedepth4dead`: `if (depth == 4)` can never be true, so MTE never builds RGBA

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** You found this defect yourself, unasked, on an
unrelated brief — so the framing below is partly my reconstruction of your finding and may have
drifted from it. Today five separate counts of mine were wrong. **Assume something here is too
confident and find it.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies sit under the
project root and are NOT this fork.

**SCOPE:** `GXEMUL-SEC/src/devices/dev_sgi_re.c`, `src/include/thirdparty/crmfbreg.h`,
`GXEMUL-SEC/regress/sgi_re_*.py`.

**VERDICT LINE FIRST.**

## §C — SETTLED PREMISES, verified at HEAD today

**S1 — THE UNITS MISMATCH.**

```c
	:1311	int depth = 8 << ((mode & MTE_MODE_DEPTH_MASK) >> MTE_DEPTH_SHIFT);
	:1359	src_x1 /= (depth / 8);                       /* author converting bits -> bytes */
	:1368	// Hack. The MTE perhaps doesn't deal with colors per se,
	:1369	// but this makes sure that we copy 32 bits when doing 32-bit transfers.
	:1371	if (depth == 4) {
	:1372		src_mode |= DE_MODE_TYPE_RGBA;
	:1373		dst_mode |= DE_MODE_TYPE_RGBA;
		}
```

`MTE_MODE_DEPTH_MASK` is `0x00000300` and `MTE_DEPTH_SHIFT` is 8, so the field is **two bits** and
`depth` takes exactly **8, 16, 32, 64**. `depth == 4` is never true. **`depth` is in BITS and the test
compares it to a BYTE count** — and `:1359` shows the author converting between the two four lines
earlier.

**S2 — THE CONSTANTS DEFINE ONLY THREE OF THE FOUR VALUES.** `crmfbreg.h:268-270` gives
`MTE_DEPTH_8 = 0`, `MTE_DEPTH_16 = 1`, `MTE_DEPTH_32 = 2`. **Field value 3 (depth 64) is named
nowhere.**

**S3 — WHAT THE DEAD BRANCH COSTS.** `:1365-1366` build `src_mode`/`dst_mode` as
`(tlb << 10) + (field << 8)` with **no type bits**, so `color_mode` is `0` = CI. With the branch dead,
every tiled MTE transfer runs in colour-index mode. `horrible_getputpixel`'s CI arm assigns
**`buf[0]` only**, while `bufdepth = 1 << ((mode >> 8) & 3)` transfers **1, 2, 4 or 8 bytes**.

**S4 — SO THIS IS THE MECHANISM OF A SIBLING ROW.** `sgirebufuninit` is about that same `uint8_t
buf[8]`. The dead branch is why the MTE path reaches it: the producer *tries* to select RGBA and
fails silently.

**S5 — MY ARITHMETIC FOR THE OBVIOUS FIX.** `depth == 32` is field value 2, giving
`bufdepth = 1 << 2 = 4` bytes and RGBA, which assigns `buf[0..3]` — matching the 4-byte transfer
exactly. **But that repairs only the 32-bit case**: field 1 (16-bit) still transfers 2 bytes with
`buf[0]` assigned, and field 3 (64-bit) transfers 8 with `buf[0]` assigned.

## The questions

**Q1 — IS `depth == 32` THE FIX, OR IS IT THE SAME BUG ONE LAYER UP?** The comment says *"copy 32 bits
when doing 32-bit transfers"*, which reads as a narrow patch for one width. **Should the type instead
be selected per width**, and if so what type does a 16-bit or 64-bit MTE transfer want? Say plainly if
the source cannot settle it.

**Q2 — WHAT IS FIELD VALUE 3?** S2 says nothing names it. **Is depth 64 reachable from a guest**, and
if so is a 64-bit MTE transfer meaningful on this hardware, or is the two-bit field simply wider than
the encodings that exist? That decides whether the fix owes a decline for value 3.

**Q3 — DOES FIXING THIS CHANGE `sgirebufuninit`'s DISPOSITION?** If MTE at 32 bits starts assigning
`buf[0..3]`, one leak path closes. **Enumerate what remains** — and say whether that makes the
zero-fill unnecessary, still necessary, or necessary for different reasons.

**Q4 — THE WITNESS.** This row has none. Can a rung-3 cold-debugger probe on stock `-E sgi -e ip32`
drive an MTE tiled transfer at MTE_DEPTH_32 and observe the destination? The sibling
`regress/sgi_re_rgb_probe.py` drives the DE path; **MTE is a different register set.** If you conclude
it cannot be witnessed, say so and say what blocks it — that is a real answer.

**Q5 — THE SMALLEST EDIT that breaks the fix and still passes. Name the row you expect to stay green.**
The neighbouring `#505` detector was swept clean three times by the clause-(d) shape — at a transfer
width no row drove, an addressing mode no row used, and the joint cell of the two.

## What I am not asking

Do not write a patch or a probe, and do not run anything. **Nothing ships until the flagship
adjudication on 2026-09-09.**

**If, while verifying a claim, you found something ELSE — say so.**
