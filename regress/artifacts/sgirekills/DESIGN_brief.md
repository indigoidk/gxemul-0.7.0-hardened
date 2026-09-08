# DESIGN — `sgirekills`: twelve live host kills in `dev_sgi_re.c`, in TWO classes the row treats as one

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** On the sibling `lcabadval` brief an hour ago you
found that my class count was wrong in its own headline, my accept-row count under-counted a second
time, and **my cited in-file precedent was itself a filed defect**. This brief is the same shape on a
different file. **Assume the same three errors are here and look for them.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** HEAD is `7a41b3f`.

**SCOPE:** `GXEMUL-SEC/src/devices/dev_sgi_re.c`, `src/include/thirdparty/crmfbreg.h`,
`GXEMUL-SEC/regress/sgi_re_*.py`.

**VERDICT LINE FIRST.**

## §C — SETTLED PREMISES, enumerated today rather than carried

**S1 — TWELVE LIVE `exit(1)`, and they are TWO classes, not one.**
`grep -cE '^[[:space:]]+exit\(1\);'` = 12, each preceded by its own `fatal()`:

    READ ARMS -- a guest READ of a register the model already STORES
      :437 CRIME_RE_TLB_A   :456 TLB_B   :475 TLB_C
      :494 CRIME_RE_TEX     :586 LINEAR_A  :644 LINEAR_B

    MTE FEATURE ARMS -- an unimplemented transfer mode or width
      :1330 MTE_MODE_STIPPLE  :1338 unimplemented SRC  :1399 MTE_MODE_COPY
      :1404 MTE_DEPTH_x       :1415 bytemask           :1537 read/write len

**S2 — THE READ ARMS LOOK LIKE MEMBER 4 (ACCEPT).** The device already keeps `re_tlb_a/b/c`,
`re_tex`, `re_linear_a/b` and services WRITES to them; only the READ path kills. That is the same
shape as `lcabadval`'s six value guards — *the model computes/stores the right thing and then refuses
to hand it back*.

**S3 — THE WITNESS SHOULD BE EASY AND I WANT THAT CHECKED.** A guest `lw` of each register kills the
host on HEAD and returns the stored value after a fix, so the rows are RED pre-fix by construction —
unlike `lcabadval`, where you showed an accept-only detector is **green on HEAD** because the legal
writes already survive. **Is that asymmetry real, or am I about to repeat the floor-(a) miss in a new
place?**

**S4 — `sgi_re_rgb_probe.py` ALREADY DRIVES THIS DEVICE** on stock `-E sgi -e ip32`, writes
`re_tlb_a[0]` and `re_linear_a[0]`, and knows the `TLBA_TILE = 0x8002` valid-bit trap. It never
issues a READ of those registers.

**S5 — THE ROW CARRIES A HELD QUESTION ABOUT TEX ONLY**: whether TEX may be ACCEPTed in a MIRRORED
form (the same `>> 3` the store uses), which round-trips per frame while shipping hardware-wrong reads
at overlapping offsets — versus DECLINING that one arm until `sgitexindex` lands.

## The questions

**Q1 — IS THE READ-ARM CLASS ONE ROUND?** Six arms, one shape. **Or does TEX split out** on S5's
grounds, making it five plus a held one? Say which, and whether a five-arm round can honestly claim
"the RE read arms no longer kill".

**Q2 — WHAT DOES EACH READ RETURN?** For each of the six, name the expression. `re_tlb_a` is
`uint16_t[256]` and `re_linear_a` is `uint32_t[]` — **so a naive `odata = d->re_tlb_a[idx]` differs in
width from a naive LINEAR read**, and `#508` was a defect of exactly that kind (a shift and its mask
drifting apart). Is there an index bound, and what does an out-of-range index do today?

**Q3 — THE FLOOR-(a) QUESTION, sharpened by `lcabadval`.** There, rows writing only *legal* values
were green under verbatim reinstatement of all six guards. **Here the analogous miss would be a
detector that reads only registers whose read arm was fixed.** What must the detector do so that
re-instating any ONE of the six kills reddens it — and does that need a row per arm, or does one row
per arm plus a survival oracle suffice?

**Q4 — DO THE MTE ARMS BELONG IN THIS ROUND AT ALL?** They are guarded by *unimplemented feature*
rather than *implemented but unreadable*. **I think they are a different member and a different
round.** Argue against that if it is wrong — and note `:1404` `MTE_DEPTH_x` is adjacent to
`sgimtedepth4dead`, whose `if (depth == 4)` dead branch is a separate open row.

**Q5 — THE SMALLEST EDIT that breaks the fix and still passes. Name the row you expect to stay
green.** On `lcabadval` you named site omission and disjunct-dropping rather than an operand swap.
**What is the analogue here?** I expect leaving one of the six arms fatal, but say if there is
something subtler — a read that returns the right value at the wrong width, say, which a survival
oracle cannot see.

## What I am not asking

Do not write a patch or a probe and do not run anything. **Nothing ships until the flagship
adjudication on 2026-09-09.**

**If, while verifying a claim, you found something ELSE — say so.**
