# WITNESS + FIX — `sgimtedepth4dead`: `if (depth == 4)` is dead, so MTE never builds RGBA

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** You have refused three of my rounds today by
ratifying the edit and rejecting the witness — each time correctly, and each time the missing row
caught something I had not considered. **Do that again here; I expect this witness to be the weakest
of the four.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**

**SCOPE:** `GXEMUL-SEC/src/devices/dev_sgi_re.c`, `src/include/thirdparty/crmfbreg.h`,
`GXEMUL-SEC/regress/sgi_re_*.py`.

**VERDICT LINE FIRST.**

## §C — SETTLED PREMISES

**S1 — THE UNITS BUG.** `:1311` `int depth = 8 << ((mode & MTE_MODE_DEPTH_MASK) >> MTE_DEPTH_SHIFT);`
The field is two bits, so `depth` is **8, 16, 32 or 64** — in BITS. `:1371` tests `depth == 4`, a BYTE
count, and is never true. `:1359` (`src_x1 /= (depth / 8)`) shows the author converting between the
two units twelve lines earlier. The comment at `:1369` states the intent: *"this makes sure that we
copy 32 bits when doing 32-bit transfers."*

**S2 — THE COST.** `:1365-1366` build the modes with addressing and depth bits and **no type bits**,
so `color_mode` is CI. CI's PUT assigns **`buf[0]` only** while `bufdepth` transfers 1/2/4/8 bytes.

**S3 — `depth == 32` IS THE FIX, AND IT IS NECESSARILY NARROW** (established by a prior seat):
`*color` is a `uint32_t`, so **no implemented type can carry a 64-bit transfer at all**; at 16 bits CI
loses a byte and RGBA would over-read two. So this repairs the 32-bit case and leaves the others.

**S4 — FIELD VALUE 3 IS GUEST-STORABLE AND UNVALIDATED** on the tiled path, and its hardware meaning
is unknown: `crmfbreg.h` names only `MTE_DEPTH_8/16/32`, which proves the header names three
encodings, **not that the fourth is reserved**.

**S5 — THE ORACLE PROBLEM, which is why this brief exists.** A prior seat: *"An affected copy can
appear correct if the PUT's uninitialized tail happens to retain bytes from the preceding GET. These
are separate automatic objects; that preservation is neither guaranteed nor evidence of
correctness."* **So a copy-equality row cannot be trusted.**

## The questions

**Q1 — CAN THIS BE WITNESSED AT ALL, AND HOW?** MTE is registered unconditionally beside DE and
dispatches synchronously to guest physical memory, so it is *reachable*. **The problem is the oracle.**
Name a channel that is deterministic under the defect — I am thinking of a destination pre-painted
with a known pattern, so an untouched tail is DISTINGUISHABLE from a correctly-written one rather than
accidentally equal. **Does that work, or does the CI PUT write `buf[0]` over the whole span?**

**Q2 — IF NO WITNESS IS POSSIBLE, SAY SO.** This project has a `detector:` term for a fix that ships
with a measured detector and no guest-path witness, and it explicitly does NOT satisfy the
reproduce-first step — a round using it still owes the attempt and must record what the attempt found.
**Is this such a round?** That is a real answer, not a failure.

**Q3 — WHAT DISPOSITION FOR FIELD 3?** Decline as unimplemented, or leave it? Note `:1341`'s tiled
dispatch has no depth guard while the LINEAR path exits on non-8-bit depth — **so the two paths
already disagree**, and a fix that touches only the comparison leaves them disagreeing.

**Q4 — THE SMALLEST EDIT that breaks the fix and still passes.** A prior seat named `32` → `33` (the
branch dead again). **Is there a subtler one** — e.g. selecting RGBA for the source but not the
destination, which `:1372-1373` set together?

**Q5 — DOES THE FIX INTERACT WITH THE THREE ROUNDS HELD IN THIS FILE'S FAMILY?** `#505` changed the
RGB GET's byte container; `sgirebufuninit` proposes zero-filling `buf`; `sgirandomcolour` proposes
declining the colour default. **If MTE starts selecting RGBA at 32 bits, which of those three changes
meaning?**

## What I am not asking

Do not write a patch or a probe and do not run anything. **Nothing ships until the flagship
adjudication on 2026-09-09.**

**If, while verifying a claim, you found something ELSE — say so.**
