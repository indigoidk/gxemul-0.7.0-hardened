# Portable-C99 review: a mask expression in an ARM bit-field instruction handler

This is a **C99 conformance and portability** question about one arithmetic expression in an
instruction-set simulator, plus how to test the correction. It is ordinary correctness-engineering
review, of the same kind as an integer-promotion or signed-overflow audit.

**PLEASE DO NOT SIMPLY RATIFY.** A previous round of mine corrected this same expression in two
places and missed a third, so the failure mode under review is *trusting a claim that has already
been checked once*. **CHECK THE PREMISES, NOT JUST THE DERIVATIONS**, and if a premise is not
settleable from this packet, say so by name.

**The tree under review is `GXEMUL-SEC/src/`.** Several pristine upstream copies exist elsewhere
under the project root; a seat reading one will report line numbers off by hundreds.

---

## 1. The expression

`src/cpus/cpu_arm_instr.c`, function `X(bfi)` (ARM Bit-Field Insert). Full function, verbatim:

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

The mask is built as `(1 << width) - 1`.

## 2. Premises, each verified on this machine

* **P1 -- the decoder writes `msb` and `lsb` independently, each in 0..31.** Verbatim:

```c
4564| 			} else if ((iword & 0x0fe00070) == 0x07c00010) {
4565| 				ic->f = cond_instr(bfi);
4566| 				ic->arg[0] = (size_t)(&cpu->cd.arm.r[rd]);
4567| 				ic->arg[1] = (size_t)(&cpu->cd.arm.r[rm]);
4568| 				int lsb = (iword >> 7) & 31;
4569| 				int msb = (iword >> 16) & 31;
4570| 				ic->arg[2] = (msb << 16) + lsb;
```

* **P2 -- so `width = msb - lsb + 1` takes values in [-30, 32], and `1 << width` is not portable C
  at three parts of that range:**

        width <= 0    negative right-hand operand           C99 6.5.7p3
        width == 32   operand >= width of the promoted type  C99 6.5.7p3
        width == 31   `1' has type int; 2^31 is not representable in a 32-bit int  6.5.7p4

  **Enumerated over all 1024 (msb, lsb) pairs:** 465 negative, 31 zero, 1 at width 32, 2 at width
  31 -- **499 pairs land outside the portable range**. *This arithmetic was derived three ways
  because my first attempt at it was wrong.*

* **P3 -- a sibling round already corrected the same expression at `X(ubfx)` and `X(sbfx)`:**

        uint32_t mask = (width == 32) ? 0xffffffffU : ((1U << width) - 1);

  **That form does not transfer here.** Those handlers decode `width = 1 + ((iword >> 16) & 31)`,
  so their domain is {1..32} and a `== 32` case suffices. **`X(bfi)`'s width can be zero or
  negative**, which no `== 32` test covers -- so a repair copied from the sibling would look right
  and still leave most of the non-portable range open.

* **P4 -- no local reference covers this instruction.** `_scratchpad/ddi0100i.txt` (the ARM ARM,
  DDI 0100I) contains **zero** occurrences of `BFI` or `BFC`; it is the ARMv5 manual and these are
  ARMv6T2 additions. **Refute me if you know a section that does cover it.**

* **P5 -- I believe the architecture specifies `msb < lsb` as UNPREDICTABLE for BFI**, so an
  assembler would not emit it. **I cannot verify that from anything on this machine** and state it
  as a question. Either way the simulator should compute a defined result for every encoding it
  decodes, which is the argument the sibling round shipped on.

* **P6 -- `x <<= lsb` on the line above is fine** (`lsb <= 31` by construction) and should not be
  changed alongside it.

* **P7 -- the existing test plants only UBFX/SBFX instruction words**, which is why the third site
  went unnoticed. It does already assemble and execute planted words on an unmodified machine
  configuration, so it is the cheap vehicle for a test.

**Not claimed:** that any host has been observed computing a wrong result. Nothing has been
measured yet; the sibling round shipped on a sanitizer differential (1 diagnostic before, 0 after)
plus a source pin, and this correction should meet the same bar before it lands.

## 3. Proposed correction (not yet reviewed by anyone)

```c
    uint32_t mask = (width <= 0) ? 0 :
        (width == 32) ? 0xffffffffU : ((1U << width) - 1);
```

`mask = 0` leaves the destination register unchanged for the nonpositive case -- the only reading
that inserts no bits.

## 4. Questions

**Q1.** Is `mask = 0` the right result for `width <= 0`? Alternatives: compute nothing and return
early (note the function's control flow above before proposing that), clamp `width` into {1..32}, or
emit a one-time diagnostic. **Argue from what the instruction means.**

**Q2.** What is the cheapest test? Specifically: **does a sanitizer report a negative shift operand
and an over-wide one as the same diagnostic**, and can one planted instruction word distinguish the
two parts of P2's range? A test that passes after the correction for the wrong reason is worse than
none.

**Q3.** Which of P1-P7 is wrong? **P4 and P5 are the ones I am least sure of.** Also: is `X(bfi)`
reachable on a machine configuration this tree can actually run, and does the decoder gate it behind
a CPU-model check I have missed?

**Please put a one-line verdict first** -- IMPLEMENT-AS-PROPOSED / IMPLEMENT-WITH-REVISIONS /
REFUSE -- then the body. **A verdict that merely agrees is the least useful reply**; if you find
nothing wrong, say what you checked and how.
