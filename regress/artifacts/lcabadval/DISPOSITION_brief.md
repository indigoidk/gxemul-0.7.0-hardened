# DISPOSITION (read-only) — what does this tree already do for each of `dev_lca.c`'s five refusal kinds?

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Where I state something as fact, ask whether it is
true. A seat that re-derives a premise from something this brief did NOT give it is worth more than
one that agrees. **A recent panel had seven of nine seats confirm a premise stated wrongly.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** There are three pristine-2021-upstream copies of
GXemul under the project root. They are NOT this fork.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/` AND `GXEMUL-SEC/regress/*.py`.** Do not read
`GXEMUL-SEC/regress/artifacts/` or `GXEMUL-SEC/tools/pipeline/ledger.json`.

**Where this brief states an ARITHMETIC claim — an accepted set, a reachable value — ENUMERATE it
rather than reasoning about it.**

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## What is settled, so you need not re-derive it

An earlier read of this file established the census, and I am carrying it forward rather than asking
for it again. **Correct it if it is wrong**, but it is not the question:

    line  kind                    site and condition
     73   INTERRUPT stub          lca_interrupt_assert; UNCONDITIONAL, no guard
     85   INTERRUPT stub          lca_interrupt_deassert; likewise
    134   BUS/cycle-type          bus != 0
    163   RANGE/lane              ofs > len   -- ofs is guest ADDRESS BITS 5-6, not a written value
    206   VALUE                   IOC_CONF     accepts {0, 1}
    226   VALUE                   IOC_TB_ENA   accepts {0, 0x80}
    241   VALUE                   W_BASE0      accepts {0, 0x300800000}
    256   VALUE                   W_MASK0      accepts {0x700000}
    280   VALUE                   W_BASE1      accepts {0x240000000}
    295   VALUE                   W_MASK1      accepts {0x3ff00000}
    315   ADDRESS/dispatch        unhandled IOC register address, reads AND writes

Also settled: the device struct is `memset` to zero at init and those registers are written **only**
by the guest store path — so each **reads back 0** while the last three accept only one non-zero
value. **An ordinary read-modify-write on `W_MASK0`, `W_BASE1` or `W_MASK1` therefore ends the
process.** And the `315` default covers the header-declared `STAT0`/`STAT1`, so "unsupported
address" does not mean "nonexistent register".

## The question

The project recognises seven dispositions for an unimplemented access: **1 remove the check ·
2 ignore silently · 3 ignore and report once · 4 accept (the model already computes the right
answer) · 5 signal a bus error · 6 accept into invented storage · 7 implement.**

**Q1 — For each of the five KINDS above, what does this tree ALREADY DO in comparable situations?**
GREP FOR THE IDIOM; do not reason from first principles. This project's rule is that the tree's own
precedents are part of the design space, and it has twice found whole dispositions that way. A
recent example that settled a different round: `dev_sgi_gbe.c`'s `#196` renders an unimplemented
guest-controlled colour mode as **black** — defined zeros, explicitly *not* a `fatal()` flood,
because the helper is per-pixel.

**I want precedent with file and construct, not opinion.**

**Q2 — Which disposition does each kind want, and where do the precedents CONFLICT?** If two
comparable sites in this tree answer the same question differently, say so — that is more useful
than a clean recommendation, because it tells me the choice is genuinely open.

**Q3 — Is disposition 5 available here at all?** I believe not: `memory_rw.c` dispatches an
exception on a failed device access for MIPS and M88K, and I have seen no Alpha equivalent — a
separate reading found that a failed Alpha access is simply abandoned with no exception delivered.
**Confirm or refute.** If it is unavailable, any proposal reaching for it owes Alpha exception
delivery first, which is a far larger round.

**Q4 — Which kinds can share a round?** The reopening rule allows a second site only if one fix
design covers both and one test covers both with no new observation. An earlier read said this
needs several rounds; I want the grouping, and the reason for each split.

## What I am not asking

Do not write a fix, a test, or a program. Do not design a witness. I want precedent, grouping, and
the availability of disposition 5.

**If, while verifying a claim, you found something ELSE — say so.**
