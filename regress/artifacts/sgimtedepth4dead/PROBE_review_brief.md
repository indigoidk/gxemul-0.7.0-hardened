# PROBE REVIEW — `regress/sgi_mte_fill_probe.py`, written to your design, NOT YET RUN

## READ THIS FIRST

**You designed this witness; I built it. Review the BUILD, not the design.** When you reviewed
`alpha_harness_probe.py` you found that every structure was planted past the end of RAM, where writes
are discarded and reads return zeros — **three rows would have gone green measuring nothing**. Assume
I have done the equivalent here and find it.

**THE TREE IS `GXEMUL-SEC/`.** HEAD `7a41b3f`, plus this untracked probe.

**THE FILE TO READ:** `GXEMUL-SEC/regress/sgi_mte_fill_probe.py`. Compare against
`src/devices/dev_sgi_re.c`, `src/include/thirdparty/crmfbreg.h`, and the sibling
`regress/sgi_re_rgb_probe.py` whose conventions it copies.

**VERDICT LINE FIRST.**

## What it claims to do

Program a tiled 32-bit MTE **FILL** at pixel (0,0), then read `dest[0]` and assert the **top byte**:

    bg = 0x11223344     CI PUT  -> dest[0] = 0x44   (the DEFECT, expected on HEAD)
                        RGBA    -> dest[0] = 0x11   (correct, after `depth == 32')

Rows: `live`, `devsig`, `fill alive`, `fill ran` (top byte != paint 0x99), `fill top` (== 0x11, the
defect row, expected RED on HEAD). `dest[1..3]` are deliberately never read.

## The values I chose, each of which could be wrong

    MODE_TILED_FILL = 0x200         dst_tlb = (mode & 0x1c) >> 2 = MTE_TLB_A = 0
                                    depth   = 8 << ((mode & 0x300) >> 8) = 8 << 2 = 32
                                    MTE_MODE_COPY 0x800 CLEAR = fill
    MTE_DST1_START  = 0xb5003838    CRIME_MTE_DST1 0x3038 | CRIME_DE_START 0x800
    DST0 = DST1 = 0                 x = (v>>16)&0xfff, y = v&0xfff -> one pixel at (0,0)
    RE_TLB_A store  = TLBA_TILE << 48 via `sd'   -> re_tlb_a[0] = 0x8002
    DEST = 0xa0000000 + ((0x8002 << 16) & ~0x80000000) = 0xa0020000

## The questions

**Q1 — WHAT MAKES THIS GO GREEN WHILE MEASURING NOTHING?** The question that found the past-RAM
defect. Specifically: if the fill never runs, does `fill ran` catch it, or can the destination change
for some other reason? And if `re_tlb_a[0]` ends up without bit 15, is the failure distinguishable
from a wrong byte?

**Q2 — IS `MODE_TILED_FILL = 0x200` RIGHT?** Check the three fields independently. I am least sure
that leaving every other mode bit zero is legal rather than accidentally selecting something —
`MTE_MODE_DST_ECC`, `SRC_ECC`, `STIPPLE` and the bytemask all default to 0 here, and `:1415` kills on
an unimplemented bytemask. **Does a zero bytemask reach that kill?**

**Q3 — DOES WRITING `DST1 | START` ACTUALLY FIRE IT, AND IS DST1 WRITTEN BY THEN?** The handler does
`relative_addr &= ~CRIME_DE_START` before storing, so the value should land in DST1 and then fire.
**Confirm the order** — if it fires before storing, DST1 is stale and the rectangle is wrong.

**Q4 — IS THE `sd` PACKING RIGHT FOR `re_tlb_a[0]`?** The sibling probe uses `TLBA_TILE << 48` and its
comment records that getting RE's 64-bit word order wrong once left the tile pointer 0 and sent every
pixel to physical address 0. **MTE's own register handler uses the OPPOSITE convention**
(`mte_reg[regnr] = idata`, `mte_reg[regnr+1] = idata >> 32`), which is why I used 32-bit `sw` for the
MTE registers. **Is that inconsistency real, and did I get each side right?**

**Q5 — IS THE POLARITY RIGHT?** `fill top` asserts `0x11` and should FAIL on HEAD. My first attempt at
a different witness this session scored `6/6` on the committed build by asserting the DEFECT as the
passing state. **Check I have not done it again**, and check that `fill ran` is not vacuous — it must
distinguish "wrote the wrong byte" from "never landed".

## What I am not asking

Do not edit the probe and do not run it. **Nothing ships until the flagship adjudication on
2026-09-09.**

**If, while verifying a claim, you found something ELSE — say so.**
