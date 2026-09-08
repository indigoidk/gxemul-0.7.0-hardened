# armbfiwidth -- FIX DESIGN (pass 1).  `#510` fixed two of three sites of one idiom.

**PLEASE DO NOT SIMPLY RATIFY.**  This brief exists because a round of mine corrected an expression
in two places and left the third; the failure mode under review is *believing a claim that has
already been checked once*.  **CHECK THE PREMISES, NOT JUST THE DERIVATIONS.**  If you cannot settle
a premise from this packet, SAY SO by name -- an honest "not checkable here" outranks a confident
guess, and P4 below is one I expect you may be able to refute.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**  There are FOUR pristine-2021-upstream copies under
the project root; a seat reading one reports line numbers off by hundreds.

---

## 1.  THE DEFECT

`src/cpus/cpu_arm_instr.c`, `X(bfi)` -- ARM Bit-Field Insert.  Full function, verbatim:

```c
1443| /*
1444|  *  bfi:  Bit-Field Insert.
1445|  *
1446|  *  arg[0] = ptr to rd
1447|  *  arg[1] = ptr to rn
1448|  *  arg[2] = (msb << 16) + lsb
1449|  */
1450| X(bfi)
1451| {
1452| 	uint32_t x = reg(ic->arg[1]);
1453| 
1454| 	int lsb = (uint8_t)ic->arg[2];
1455| 	int msb = ic->arg[2] >> 16;
1456| 	int width = msb - lsb + 1;
1457| 
1458| 	x <<= lsb;
1459| 
1460| 	uint32_t mask = (1 << width) - 1;
1461| 
1462| 	mask <<= lsb;
1463| 
1464| 	reg(ic->arg[0]) &= ~mask;
1465| 	reg(ic->arg[0]) |= (x & mask);
1466| }
1467| Y(bfi)
```

`(1 << width) - 1` at the marked line is undefined over most of its domain.

## 2.  SETTLED PREMISES (inlined -- the packet-fed seats cannot read files)

* **P1 -- the decoder gives `msb` and `lsb` INDEPENDENTLY, each 0..31.**  Verbatim from the `bfi`
  arm, `(iword & 0x0fe00070) == 0x07c00010`:

```c
4564| 			} else if ((iword & 0x0fe00070) == 0x07c00010) {
4565| 				ic->f = cond_instr(bfi);
4566| 				ic->arg[0] = (size_t)(&cpu->cd.arm.r[rd]);
4567| 				ic->arg[1] = (size_t)(&cpu->cd.arm.r[rm]);
4568| 				int lsb = (iword >> 7) & 31;
4569| 				int msb = (iword >> 16) & 31;
4570| 				ic->arg[2] = (msb << 16) + lsb;
```

* **P2 -- so `width = msb - lsb + 1` spans [-30, 32], and `1 << width` is undefined THREE ways:**

        width <= 0    negative shift count                    C99 6.5.7p3
        width == 32   count >= width of the promoted type     C99 6.5.7p3
        width == 31   `1' is int; 2^31 is not representable   C99 6.5.7p4 (signed overflow)

  **Brute-forced over all 1024 (msb, lsb) pairs on this machine:** 465 negative, 31 zero
  (**496 nonpositive**), 1 pair at width 32, 2 pairs at width 31 -- **499 of 1024 reach an
  undefined shift.**  *That arithmetic was derived three independent ways (a seat's closed form, my
  own, and brute force) because my first attempt at it was wrong.*

* **P3 -- `#510` repaired the SAME expression at `X(ubfx)` and `X(sbfx)`, which now read:**

        uint32_t mask = (width == 32) ? 0xffffffffU : ((1U << width) - 1);

  **That form does NOT transfer.**  BFX decodes `width = 1 + ((iword >> 16) & 31)`, domain {1..32},
  so a `== 32` case is sufficient there.  **BFI's width can be zero or negative and no `== 32` test
  catches it** -- a repair copied from the sibling closes one third of this site's undefined domain
  and looks correct.

* **P4 -- THERE IS NO PRIMARY SOURCE FOR BFI ON THIS MACHINE.**  `_scratchpad/ddi0100i.txt` (ARM ARM,
  DDI 0100I) contains **ZERO** occurrences of `BFI` or `BFC` -- it is the ARMv5 manual and BFI/BFC
  are ARMv6T2 additions.  **Refute me if you know a section that covers it.**  *This project has
  twice had an "absent source" note be load-bearing and wrong.*

* **P5 -- I BELIEVE ARM specifies `msb < lsb` as UNPREDICTABLE for BFI**, so a conforming assembler
  never emits it.  **I cannot verify this from anything on this machine (see P4) and it is stated
  here as a QUESTION, not a fact.**  Note it does not settle the round either way: the emulator must
  not invoke host UB on a non-conforming instruction, which is the argument `#510` shipped on.

* **P6 -- `x <<= lsb` on the line above the defect is SAFE** (`lsb <= 31` by construction) and must
  not be "repaired" alongside it.

* **P7 -- the existing detector plants UBFX/SBFX words ONLY.**  `regress/arm_bfx_width_probe.py`
  cannot see this site, which is why the sibling miss went unnoticed.  It DOES already plant and
  execute instruction words on an unmodified machine, so it is the cheap vehicle for a witness.

**NOT CLAIMED:** that any host misbehaviour has been measured.  **No witness exists yet.**  `#510`
shipped on a UBSAN differential (1 diagnostic pre-fix, 0 post-fix) plus a source pin, and this row
owes the same before any edit lands.

## 3.  THE PROPOSED FIX (not adjudicated -- no panel has seen this)

```c
    uint32_t mask = (width <= 0) ? 0 :
        (width == 32) ? 0xffffffffU : ((1U << width) - 1);
```

with `mask = 0` leaving `rd` unchanged for the nonpositive case -- the only reading that inserts no
bits, and a defensible choice for UNPREDICTABLE.

## 4.  THE THREE QUESTIONS

**Q1 (THE DISPOSITION FOR `width <= 0`).**  Is `mask = 0` right?  The alternatives are: fault, decline
with a latched announce (the house idiom for guest-drivable events), or clamp `width` into {1..32}.
**Argue from what the instruction means, not from what is easiest to write** -- and if this is a case
where the fork's own option set (DELETE / DECLINE / DECLINE+LATCH / ACCEPT / FAULT / BACKED ACCEPT /
IMPLEMENT) has a member I have not named, name it.  *A latched announce on a path a conforming guest
never takes may be noise; say so if you think it.*

**Q2 (THE WITNESS).**  What is the cheapest rung-3 attempt?  Specifically: **what does UBSAN actually
report for a NEGATIVE shift count versus a too-large one** -- are they the same diagnostic, and can
one planted `bfi` distinguish the two halves of P2's domain?  A witness that greens on the repair for
the wrong reason is worse than none.  Note `#510`'s probe already plants words and executes them on
an unmodified machine.

**Q3 (PREMISE AUDIT).**  Which of P1-P7 is wrong?  **P4 and P5 are the ones I am least sure of.**
Also: is `X(bfi)` reachable on any machine this tree can actually boot or probe, and does the
enclosing decoder arm gate it behind a CPU-model check I have not noticed?

**VERDICT LINE FIRST** -- one line at the top saying IMPLEMENT-AS-PROPOSED / IMPLEMENT-WITH-REVISIONS
/ REFUSE, so it survives truncation.  **A verdict that merely agrees is the least useful thing you
can send**; if you find nothing wrong, say what you CHECKED and how.
