# FULL PANEL — `dev_sgi_re.c`: a local buffer whose assigned length and transferred length are decided independently

*(Consolidated from two prior audits. The first version of this brief was rejected by one seat's
content filter after 43,839 tokens; a reworded version with the same technical content was answered in
full. **This packet uses the reworded register deliberately, and says so** — the removed material was
the sentence characterising the consequence, not any premise.)*

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** **Seven briefs of mine this week stated premises
that were false or too broad**, and a full panel on a sibling row rejected a correction of mine
because a grep for a symbolic constant cannot enumerate the class it was standing in for. **Where a
premise below rests on a search, ask what the search would miss.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies of GXemul sit
under the project root and are NOT this fork.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/` AND `GXEMUL-SEC/regress/*.py`.**

**Where this packet states a COUNT or a REACHABILITY claim, ENUMERATE it.**

**VERDICT LINE FIRST.**

---

## §C — SETTLED PREMISES

**S1.** `horrible_getputpixel()` declares `uint8_t buf[8];` with no initialiser and no `memset`. It is
a fresh automatic per call, and the function is called once per pixel from three callers (LINE,
RECTANGLE, tiled MTE). It is declared **after** the coordinate / `tlb_mode` / `tileptr`-valid early
returns, so a fill at that site is not paid on declined pixels.

**S2.** Two independent fields of the same guest-written mode word decide, separately, how many bytes
are **assigned** and how many are **transferred**:

```c
	uint32_t color_mode = mode & DE_MODE_TYPE_MASK;   /* bits 4-7 : which arm assigns buf */
	int bufdepth = 1 << ((mode >> 8) & 3);            /* bits 8-9 : how many bytes move   */
```

Nothing couples them on the DE path. **On the MTE path they are not two guest fields at all**:
`src_mode`/`dst_mode` are built as `(tlb << 10) + (depth_field << 8)` with no type bits, so
`color_mode` is pinned at `0` (CI) unless a dead branch fires — *a constant colliding with a guest
depth*.

**S3 — the mismatch table, enumerated by a prior audit rather than described:**

| arm | assigns | depth 1 | 2 | 4 | 8 |
|---|---|---|---|---|---|
| CI | `buf[0]` | — | `buf[1]` | `buf[1..3]` | `buf[1..7]` |
| RGB / RGBA / ABGR / default | `buf[0..3]` | — | — | — | `buf[4..7]` |

**CI at depth 4 already transfers three unassigned bytes**, and the MTE path forces CI. The
reverse direction also exists: at depth 1 or 2 the read fills only that many bytes and the
multi-byte arms then read `buf[2..3]` regardless.

**S4 — the fork's existing pattern.** `memory_rw.c` fills at three sites, its own comments calling it
*"the same zero-fill ethos as the failed-device-read path (#95)"* and *"root-cause fix for the
uninit-read class (cf. per-device #91/#93/#94)"*. **A prior audit judged that warrant WEAKER than I
had claimed**: `#95` fills a READ buffer for `len` bytes on a FAILED access, so it does nothing for a
write and never covers bytes beyond `bufdepth`.

**S5 — TWO SEATS ALREADY AGREE ON THE FIX**: zero-initialise all eight bytes at the existing
declaration; it completes the local repair in both directions and does **not** repair pixel-format or
MTE behaviour.

**S6 — AND BOTH AGREE NO ORACLE CAN PROVE IT.** *"No guest-visible value or write-count oracle can
reliably prove initialization occurred… Unexpected values can expose a failure; expected values cannot
prove definedness."* A determinism oracle is separately refuted — stack reuse can make a wrong value
repeat.

---

## The questions

**Q1 — IS ZERO-FILL RIGHT, or does it mask the real defect?** It makes a **defined-but-still-wrong**
value where there was an unspecified one: CI at depth 4 would transfer `{value,0,0,0}`. **Argue that
the arms should instead assign `bufdepth` bytes each**, and say what that costs.

**Q2 — GIVEN S6, WHAT DETECTOR IS HONEST?** If no guest-visible oracle can prove definedness, the
candidates are an offline differential over the arms, or a `harness:` witness under the ladder's fifth
term. **Which, and what exactly would it assert?** If your answer is that no detector can defend this
fix, say so — that is a real answer and it changes whether the round should ship at all.

**Q3 — WHICH DEFECT OWNS WHICH BYTES?** Two neighbouring rows overlap: a dead branch forcing every
*tiled* MTE transfer to CI colour, and a default arm assigning `random()` bytes. **Draw the boundary**
— if this is repaired first, what remains of the other two?

**Q4 — THE SMALLEST EDIT that breaks the fix and still passes. Name the row you expect to stay green.**
A neighbouring round's detector was swept clean three times by the clause-(d) shape — at a transfer
width no row drove, an addressing mode no row used, and finally the joint cell of the two.

**Q5 — IS S4's WARRANT STRONG ENOUGH TO CARRY THIS?** The prior audit weakened it. **Is `#95` a
precedent for this fix, or merely an ethos?** If merely an ethos, the addition licence wants a
measured delta instead, and there is none.

## What I am not asking

Do not write a patch or run anything. **Nothing ships until the flagship adjudication** — this packet
exists to be complete, not to authorise work.

**If, while verifying a claim, you found something ELSE — say so.**
