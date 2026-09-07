# DESIGN BRIEF pass 1 — `sgirandomcolour`: the colour-mode PUT default writes four `random()` bytes into guest memory

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Where I state something as fact, ask whether it is
true. A seat that re-derives a premise from something this brief did NOT give it is worth more than
one that agrees.

**Two briefs of mine this week stated premises that were simply false, and I built conclusions on
both before a seat read the code.** One was a variable's declared *type* (`unsigned int`, three lines
above the code I quoted — it refuted a HIGH finding I had already committed). The other was *which of
two arms is authoritative* — circular, and four seats said so. **If a premise below is wrong, that is
the most valuable thing you can tell me.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** There are three pristine-2021-upstream copies of
GXemul under the project root. They are NOT this fork; their line numbers differ by hundreds, and a
seat reading one reports arms that do not exist here.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/` AND `GXEMUL-SEC/regress/*.py`.** Do not read
`GXEMUL-SEC/regress/artifacts/` or `GXEMUL-SEC/tools/pipeline/ledger.json`.

**Where this brief states an ARITHMETIC or COUNTING claim — a set of modes, a byte count — ENUMERATE
it rather than reasoning about it.** Walk the values.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## §C — PREMISES ALREADY SETTLED, RE-INLINED SO NOBODY SPENDS AN ANSWER RE-DERIVING THEM

**S1. The defect, quoted verbatim.** In `horrible_getputpixel()`, the PUT branch's colour switch:

```c
	if (put) {
		switch (color_mode) {
		case DE_MODE_TYPE_CI:
			buf[0] = *color;
			break;
		case DE_MODE_TYPE_RGB:
			buf[0] = *color >> 24;
			buf[1] = *color >> 16;
			buf[2] = *color >> 8;
			buf[3] = 0;
			break;
		case DE_MODE_TYPE_RGBA:
			buf[0] = *color >> 24;
			buf[1] = *color >> 16;
			buf[2] = *color >> 8;
			buf[3] = *color;
			break;
		case DE_MODE_TYPE_ABGR:
			buf[0] = *color;
			buf[1] = *color >> 8;
			buf[2] = *color >> 16;
			buf[3] = *color >> 24;
			break;
		default:buf[0] = random();
			buf[1] = random();
			buf[2] = random();
			buf[3] = random();
			// TODO.
			fatal("[ put: color mode = 0x%x ]\n", color_mode);
		}

		cpu->memory_rw(cpu, cpu->mem, tileptr + ofs,
		    buf, bufdepth, MEM_WRITE, NO_EXCEPTIONS | PHYSICAL);
	} else {
		...
	}
```

**There is no `break` in the default arm and no decline.** Control falls out of the switch into the
`memory_rw(..., MEM_WRITE, ... | PHYSICAL)` immediately below it, so four bytes of host `random()`
are written to guest memory at a guest-influenced tile offset. `fatal()` in this fork does **not**
exit — it is a diagnostic — so this is not a host kill; it is a silent write of host RNG output.

**S2. The mode constants** (`src/include/thirdparty/crmfbreg.h`), enumerated rather than totalled:

```
DE_MODE_TYPE_CI    0x00      implemented
DE_MODE_TYPE_RGB   0x10      implemented
DE_MODE_TYPE_RGBA  0x20      implemented
DE_MODE_TYPE_ABGR  0x30      implemented
DE_MODE_TYPE_YCRCB 0xf0      *** DOCUMENTED, NAMED, AND NOT IMPLEMENTED ***
DE_MODE_TYPE_MASK  0xf0
```

Since the mask is `0xf0`, `color_mode` takes **sixteen** values: `0x00, 0x10, … 0xf0`. Four are
implemented. **Twelve reach the default arm**, and one of those twelve — `0xf0` — is a mode the
header names.

**S3. Guest reachability, established by reading the whole path.** `color_mode = mode &
DE_MODE_TYPE_MASK`, where `mode` is the caller's `src_mode`/`dst_mode`. Those come from
`d->de_reg[(CRIME_DE_MODE_SRC - 0x2000)/4]` and the `_DST` equivalent — **read straight out of the
register array with no filtering, validation or masking anywhere on the path.** A guest writing
`CRIME_DE_MODE_DST` selects the arm directly.

**S4. What `#504` did, and what it did NOT do.** `#504` (`257f56f`) de-fanged a *different* default —
the **addressing-mode** switch, whose arm read `default: fatal("unimplemented dst_mode %i …"); *color
= random();`. It replaced that with a decline plus a latched announce on its own bit,
`SGIRE_W_BADMODE = 1 << 10`. **The colour-mode default in S1 was not touched and is still live.**
*I nearly recorded this as the `#499` "repaired one cell, left the mirror" shape and it is not — they
are two different `switch` statements. Related by idiom, not by that pattern.*

**S5. The house latch idiom, and why `#504` used its own bit.** The four `dev_sgi_re` handlers share
one malloc'd struct, so a latch bit shared with another site is silenced by that site's ordinary
register traffic and the announce never fires — measured at `#498`, repeated at `#500`. `#504`'s
comment records that the enum ends at `1 << 10` on purpose so the next maintainer finds the next free
bit, which is `1 << 11`.

---

## The questions

**Q1 — WHICH OPTION-SET MEMBER IS RIGHT, and is there one this brief has not named?** The project's
set is DELETE · DECLINE (silent) · DECLINE + LATCHED ANNOUNCE · ACCEPT · FAULT · BACKED ACCEPT ·
IMPLEMENT. My position is **DECLINE + LATCHED ANNOUNCE with its own bit `1 << 11`**, transferring
`#504`'s in-tree warrant. **Argue against it.** In particular: is IMPLEMENT defensible for `YCRCB`
specifically, given the header names it and a real driver might select it? And **grep the fork for
the existing idiom before answering** — this project has twice found an option-set member by looking
rather than by reasoning.

**Q2 — WHAT DOES "DECLINE" MEAN HERE, exactly?** The write is *after* the switch, shared with all
five arms. So a decline must either (a) `return` before it — but **read the full function first**,
because an early `return` in this same file's GET branch would skip a common tail, and four
independent readers once proposed exactly that mistake — or (b) leave `buf` untouched and skip only
the write, or (c) something else. **Name the control-flow shape, not just the intent.**

**Q3 — WHAT IS THE ORACLE?** This is the hard part and I want it attacked. The defect's output is
`random()`, so **no value row can pin it.** `#504` faced this and asserted that the destination still
held its *pre-paint* value — i.e. that the write was declined. **A determinism oracle is refuted in
advance**: two seats showed on `#504` that stack reuse can make a wrong value deterministic, so "the
same value twice" proves nothing. Is the pre-paint assertion sufficient? What does it fail to
distinguish?

**Q4 — THE SMALLEST EDIT.** Once the fix is in, what is the smallest edit that breaks it and still
passes a detector built as Q3 describes? **Name the row you expect to stay green.** I am specifically
interested in the clause-(d) shape — guard kept, repair conditioned on a field the guarded body reads
— because that shape swept a detector of mine clean *today* on the neighbouring round: the repair
applied only at the transfer width every row happened to use.

**Q5 — IS `bufdepth` A SECOND AXIS HERE TOO?** The write length is `bufdepth = 1 << ((mode >> 8) & 3)`
∈ {1, 2, 4, 8}, from bits 8-9 of the same word whose bits 4-7 select the arm. The default arm fills
only `buf[0..3]`. **At `bufdepth` 8, does it write four `random()` bytes plus four uninitialised stack
bytes?** If so this is worse than the row says, and it overlaps `sgirebufuninit` — say which defect
owns which bytes.

## What I am not asking

Do not write the fix as a patch and do not run anything. I want the disposition settled, the
control-flow shape named, and the oracle attacked before any code changes.

**If, while verifying a claim, you found something ELSE — say so.** That channel has produced most of
this week's filed rows, including three from seats answering a question about something else.
