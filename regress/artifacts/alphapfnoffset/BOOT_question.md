# QUESTION (read-only) — can any Alpha machine in this tree run a guest program at all?

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Where I state something as fact, ask whether it is
true. A seat that re-derives a premise from something this brief did NOT give it is worth more than
one that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/`.** There are three pristine-2021-upstream copies of GXemul
under the project root (`./src/` and two under `_archive/audit-results-*/builds/`). They are NOT this
fork.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/`, `GXEMUL-SEC/regress/*.py`, `GXEMUL-SEC/regress/*.sh` and
`GXEMUL-SEC/doc/`.** Do not read `GXEMUL-SEC/regress/artifacts/` or
`GXEMUL-SEC/tools/pipeline/ledger.json` — they are this project's archive of past measurements, they
are large, and nothing in them is needed here.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## Why I am asking

Four defects have been filed against the Alpha code paths in one night — a page-table walk that drops
the within-page offset, a PALcode register mismatch, an unsupported claim about fault delivery, and a
guest-reachable process exit. **All four are analysed and none has a witness.**

This project's rule is that a defect with no witness gets DOCUMENTED rather than fixed, and that a
round must attempt a real-guest reproduction before settling for that. So before any of these earns a
round, I need to know what is actually runnable.

**I would rather learn the answer is "nothing runs" now than after building a probe.**

## The questions

**Q1: which Alpha machine types does this tree define, and does any of them have a working boot
path?** Look at the machine descriptions and at what they require — a PROM image, a disk image, a
specific file that may or may not be present.

**Q2: does the regression harness exercise Alpha at all?** The gates live in `regress/*.sh` and the
probes in `regress/*.py`. If none mentions Alpha, that is itself the answer and I want it stated
plainly.

**Q3: can a guest program be run WITHOUT a full OS boot?** This project's witness ladder accepts a
"cold-debugger probe" — a real guest instruction executed through real address decode on an
unmodified in-tree machine description, driven by the built-in debugger rather than by booting an OS.
Several existing probes work that way. **Is that possible for an Alpha machine here** — can the
debugger plant instructions in memory, set a breakpoint, and continue, on some `-E` machine?

That third question is the one that matters most. A defect with no OS boot but a working
cold-debugger path is **witnessable**; a defect with neither is **documented-only**.

**Q4: for each of the four filed defects, which of the three is it?** Namely: reachable by a
cold-debugger probe / reachable only by a real OS boot / not reachable by anything runnable here.
I am not asking you to build the probe — only to say which category each falls in, and what the
blocker is where there is one.

## What I am not asking

Do not propose fixes. Do not write probes. **If the honest answer to Q3 is "no Alpha guest can
execute an instruction in this tree", say that plainly** — it is a genuinely useful answer and it
means four rows get documented and closed rather than sitting open pretending to be actionable.

**If, while verifying a claim, you found something ELSE — say so.**
