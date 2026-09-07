# DESIGN BRIEF pass 1 — `sgirebufuninit`: uninitialised host stack reaches guest-visible memory

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Where I state something as fact, ask whether it is
true. A seat that re-derives a premise from something this brief did NOT give it is worth more than
one that agrees.

**Four briefs of mine this week stated premises that were false or too broad, and every one was
caught by a seat reading the code instead of my description of it** — a variable's declared type,
which of two arms is authoritative, what a sibling probe's oracle asserts, and the scope of "every
MTE transfer". **If a premise below is wrong, that is the most valuable thing you can tell me.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies of GXemul sit
under the project root and are NOT this fork.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/` AND `GXEMUL-SEC/regress/*.py`.** Do not read
`GXEMUL-SEC/regress/artifacts/` or `GXEMUL-SEC/tools/pipeline/ledger.json`.

**Where this brief states an ARITHMETIC or COUNTING claim, ENUMERATE it rather than reasoning about
it.** Walk the values.

**VERDICT LINE FIRST.**

---

## §C — SETTLED PREMISES

**S1 — THE BUFFER IS NEVER INITIALISED.** `horrible_getputpixel()` declares `uint8_t buf[8];` with no
initialiser and no `memset` anywhere in the function. It is a fresh automatic on every call, and the
function is called per pixel.

**S2 — TWO INDEPENDENT FIELDS DECIDE HOW MUCH OF IT IS USED**, both from the same guest-written mode
word, with nothing making them agree:

```c
	uint32_t color_mode = mode & DE_MODE_TYPE_MASK;   /* bits 4-7 : which arm fills buf   */
	int bufdepth = 1 << ((mode >> 8) & 3);            /* bits 8-9 : how many bytes move   */
```

The colour arm fills a number of bytes fixed by the **type**; the transfer moves **`bufdepth`** bytes.
`bufdepth` enumerates to 1, 2, 4, 8.

**S3 — TWO REACHABLE PATHS, IN OPPOSITE DIRECTIONS.**

* **PUT — host stack into guest memory.** At `bufdepth` 8, **no colour arm writes `buf[4..7]`** — not
  one of the five, including the correct ones — and all eight bytes go to
  `memory_rw(..., tileptr + ofs, buf, bufdepth, MEM_WRITE, NO_EXCEPTIONS | PHYSICAL)`.
  `DE_MODE_TYPE_CI` writes only `buf[0]`, so CI at any depth above 1 ships the rest.
* **GET — host stack into `*color`.** At `bufdepth` 1 or 2, `memory_rw` fills only that many bytes,
  and the RGB / RGBA / ABGR arms then read `buf[2..3]` regardless.

**S4 — THE FORK ALREADY HAS A POLICY FOR THIS CLASS, and it is not my invention.** `memory_rw.c`
zero-fills at three sites, and the fork's own comments name the doctrine:

```c
	/*  ... instead of uninitialised host stack. Same zero-fill
	    ethos as the failed-device-read path (#95).  */
	if (writeflag == MEM_READ)
		memset(data, 0, len);
```

and, at a third site, *"Root-cause fix for the uninit-read class (cf. per-device #91/#93/#94)."*

**S5 — WHAT `#505` DID AND DID NOT DO.** `#505` corrected the RGB GET's byte indices. It changed
`buf[1..3]` to `buf[0..2]` — **three bytes either way**, so it neither created nor cured any part of
this. Its own pre-table check found this disagreeing state and deliberately declined to row it.

---

## The questions

**Q1 — IS ZERO-FILL THE RIGHT FIX, and is it the whole fix?** The obvious edit is
`uint8_t buf[8] = { 0 };` or a `memset`. S4 says the fork's policy supports it. **But zero-fill makes
a wrong-but-defined value where there was an undefined one** — a CI pixel at `bufdepth` 4 would write
`{value,0,0,0}` instead of `{value,junk,junk,junk}`. **Is defined-but-wrong actually better here, or
does it mask a defect that should be fixed by making each arm fill `bufdepth` bytes?** Argue both.

**Q2 — WHERE SHOULD IT GO?** Three candidate sites, and I want the trade-offs named rather than a
vote: (a) at the declaration, costing a zero-fill on every pixel; (b) only on the PUT side before the
switch; (c) only where `bufdepth` exceeds what the chosen arm fills, which is a computed guard.
**(a) is a per-pixel cost in a function the file's own comments call per-pixel and hot** — is that
cost real enough to matter?

**Q3 — *** THE ORACLE, AND THIS IS THE HARD PART. *** ** The defect's output is **uninitialised**, so
no value row can pin it. This project has already established two things that constrain the answer:
a determinism oracle is refuted (stack reuse can make a wrong value repeat), and for a neighbouring
round a seat proposed observing **zero `MEM_WRITE` calls** instead of a value. **What oracle
distinguishes "the buffer was zero-filled" from "the buffer happened to contain zeros"?** If the
honest answer is that no black-box guest-visible oracle can, say so — that is a real answer and it
changes the round's shape.

**Q4 — WHICH DEFECT OWNS WHICH BYTES?** Two neighbouring rows overlap this one:
`sgimtedepth4dead` (a dead branch that forces every *tiled* MTE transfer to CI colour, which is this
row's strongest reachability) and `sgirandomcolour` (a default arm writing `random()` bytes).
**Draw the boundary.** If this row is fixed first, what remains of the other two?

**Q5 — THE SMALLEST EDIT.** Once fixed, what is the smallest edit that breaks it and still passes a
detector built as Q3 describes? Name the row you expect to stay green. I am after the clause-(d)
family: a repair conditioned on a field the guarded body reads. Note that a neighbouring round's
detector was swept clean by exactly that shape at a transfer width no row happened to drive, and
again at a *location* no row happened to use.

## What I am not asking

Do not write a patch and do not run anything. I want the disposition and the oracle settled first.

**If, while verifying a claim, you found something ELSE — say so.**
