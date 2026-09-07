# DESIGN BRIEF — `dev_sgi_re.c`: a local buffer whose assigned length and transferred length are decided independently

*(This is a REWORDED version of `PASS1_brief.md`, which the codex seat's content filter rejected after
43,839 tokens of work. The technical content is unchanged; what is removed is the framing of the
CONSEQUENCE — the original described the defect in terms of host memory becoming visible to the
guest. The design question does not depend on that framing, so this asks the same question about
initialisation and about where to place it. **Recorded as a deliberate rewording so nobody later
mistakes the two briefs for the same request answered twice.**)*

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** A seat that re-derives a premise from something
this brief did NOT give it is worth more than one that agrees. **Four briefs of mine this week stated
premises that were false or too broad**, and each was caught by a seat reading the code rather than
my description of it.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies of GXemul sit
under the project root and are NOT this fork.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/` AND `GXEMUL-SEC/regress/*.py`.**

**Where this brief states an arithmetic claim, ENUMERATE it rather than reasoning about it.**

**VERDICT LINE FIRST.**

---

## §C — SETTLED PREMISES

**S1.** `horrible_getputpixel()` declares `uint8_t buf[8];` with no initialiser and no `memset`. It is
a fresh automatic on every call, and the function is called once per pixel.

**S2.** Two independent fields of the same guest-written mode word decide, separately, how many bytes
get ASSIGNED and how many get TRANSFERRED:

```c
	uint32_t color_mode = mode & DE_MODE_TYPE_MASK;   /* bits 4-7 : which arm assigns buf */
	int bufdepth = 1 << ((mode >> 8) & 3);            /* bits 8-9 : how many bytes move   */
```

The colour arm assigns a count fixed by the **type**; the transfer moves **`bufdepth`** bytes.
`bufdepth` enumerates to 1, 2, 4, 8. Nothing constrains the two to agree.

**S3 — THE TWO MISMATCH DIRECTIONS.**
* **Transfer longer than the assignment.** At `bufdepth` 8 **no colour arm assigns `buf[4..7]`** — not
  one of the five — yet all eight bytes are passed to `memory_rw(..., MEM_WRITE, ...)`.
  `DE_MODE_TYPE_CI` assigns only `buf[0]`, so CI at any depth above 1 transfers more than it assigned.
* **Assignment longer than the fill.** At `bufdepth` 1 or 2 the read fills only that many bytes, and
  the RGB / RGBA / ABGR arms then read `buf[2..3]` regardless.

**S4 — THE FORK HAS AN ESTABLISHED PATTERN FOR THIS.** `memory_rw.c` zero-fills at three sites, and
the fork's own comments call it *"the same zero-fill ethos as the failed-device-read path (#95)"* and
*"root-cause fix for the uninit-read class (cf. per-device #91/#93/#94)"*.

**S5.** `#505` changed the RGB GET's indices from `buf[1..3]` to `buf[0..2]` — three bytes either way
— so it neither created nor changed any of the above.

---

## The questions

**Q1 — IS ZERO-FILL THE RIGHT REPAIR, and is it the whole repair?** The obvious edit is
`uint8_t buf[8] = { 0 };`. S4 supports it. **But zero-fill produces a defined-but-still-wrong value
where there was an unspecified one** — a CI pixel at `bufdepth` 4 would transfer `{value,0,0,0}`.
**Is defined-but-wrong better here, or does it mask a defect better fixed by making each arm assign
`bufdepth` bytes?** Argue both sides.

**Q2 — WHERE SHOULD IT GO?** (a) at the declaration, costing a fill on every pixel; (b) only on the
write side, before the switch; (c) only where `bufdepth` exceeds what the chosen arm assigns, which
is a computed guard. The file's own comments call this helper per-pixel and hot — **is that cost real
enough to decide it?**

**Q3 — THE ORACLE, which is the hard part.** The value of an unassigned automatic is unspecified, so
no value row can pin it. Two things already constrain the answer here: a determinism oracle is
refuted (stack reuse can make a wrong value repeat), and for a neighbouring round a seat proposed
counting **`MEM_WRITE` calls** rather than asserting a value. **What oracle distinguishes "the buffer
was filled" from "the buffer happened to contain zeros"?** If no black-box guest-visible oracle can,
say so plainly — that is a real answer and it changes the round's shape.

**Q4 — WHICH DEFECT OWNS WHICH BYTES?** Two neighbouring rows overlap: a dead branch that forces
every *tiled* MTE transfer to CI colour, and a default arm that assigns `random()` bytes. **Draw the
boundary.** If this is repaired first, what remains of the other two?

**Q5 — THE SMALLEST EDIT.** Once repaired, what is the smallest edit that breaks it and still passes
a detector built as Q3 describes? Name the row you expect to stay green. I am after the clause-(d)
family — a repair conditioned on a field the guarded body reads. A neighbouring round's detector was
swept clean by exactly that shape at a transfer width no row drove, and again at an addressing mode
no row used.

## What I am not asking

Do not write a patch and do not run anything.

**If, while verifying a claim, you found something ELSE — say so.**
