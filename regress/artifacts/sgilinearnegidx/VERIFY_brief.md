# VERIFY (read-only) — a claimed negative-index path in `dev_sgi_re.c`, and whether it has siblings

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Where I state something as fact, ask whether it is
true. **This brief's whole content is a chain I assembled, and I want it attacked rather than
confirmed** — one of its links came from a seat that could not read the repo, and I supplied the
rest. A seat that re-derives a step from something this brief did NOT give it is worth more than one
that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** There are three pristine-2021-upstream copies of
GXemul under the project root. They are NOT this fork.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/` AND `GXEMUL-SEC/regress/*.py`.** Do not read
`GXEMUL-SEC/regress/artifacts/` or `GXEMUL-SEC/tools/pipeline/ledger.json`.

**Where this brief states an ARITHMETIC claim — an index, an offset, a reachable value — ENUMERATE
it rather than reasoning about it.** Walk the values.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## The claimed chain

    1. guest stores to CRIME_RE_TEX, filling re_tex[110] and re_tex[111]
    2. guest sets CRIME_DE_XFER_STEP_X negative (int32_t; the check at :734 announces and CONTINUES)
    3. src_x += step_x drives src_x negative in the XFER loop
    4. horrible_getputpixel with a LINEAR src_mode: the `x < 0' guard is skipped, because it reads
           if (!linear && (x < 0 || y < 0 || x >= 2048 || y >= 2048)) return;
    5. case 4: tile_nr = x >> 12 = -1, and `if (tile_nr >= 32)' does not reject a negative
    6. tileptr = 0x80000000 | (d->re_linear_a[tile_nr] << 12)
    7. tileptr &= ~0x80000000; memory_rw(..., tileptr + ofs, buf, bufdepth, MEM_WRITE, PHYSICAL)

**One thing is already measured rather than argued:** `offsetof` says `re_tex` ends at 1760 and
`re_linear_a` begins at 1760 — zero padding — so `re_linear_a[-1]` is `re_tex[110]` and
`re_tex[111]`, which the guest writes.

## The questions

**Q1 — is each step right?** Steps 2, 3 and 5 are the ones I am least sure of. Specifically:

* Can `src_x` actually reach a negative value in that loop, or does something clamp or mask it
  before the call? The destination loop masks `x` with `& 0x7ff`; **I do not know whether the
  source coordinate is masked the same way**, and if it is, the chain dies at step 3.
* Is `step_x` really guest-written and really signed at the point of use?
* Is a LINEAR `src_mode` reachable together with an XFER, or does one exclude the other?

**If the chain breaks at any step, say which and why — that is the most useful answer.**

**Q2 — are there SIBLING negative-index paths in this file?** The shape is *a guard whose
precondition excludes the mode a later guard assumes*. `case 4` bounds `tile_nr` above only. **Check
the other cases and the other arrays** — `re_tlb_a/b/c`, `re_linear_b`, `re_tex` — for the same
asymmetry, and for any other index derived from a signed value.

**Q3 — what does the value actually control?** Step 6 shifts the read value left 12 and step 7 adds
`ofs`. Enumerate the reachable address range, and say whether `PHYSICAL` here bypasses any bound the
emulator would otherwise apply.

**Q4 — is `sgitexindex`'s overlapping TEX write a real obstacle to controlling those two
halfwords?** That row records that the TEX store advances its index four per eight-byte register, so
consecutive registers overlap by three entries. I believe that affects *which* values land in
`[110..111]` but not *whether* the guest can place chosen values there. **Confirm or refute.**

## What I am not asking

Do not write a fix, a test, or a guest program. Do not design a witness. I want the chain checked
link by link, and any siblings named.

**If, while verifying a claim, you found something ELSE — say so.**
