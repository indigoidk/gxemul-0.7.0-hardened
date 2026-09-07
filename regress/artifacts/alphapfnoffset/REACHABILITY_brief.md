# REACHABILITY QUESTION (read-only) — is the Alpha page-table walk reached on any machine this emulator can boot?

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Where I state something as fact, ask whether it is
true. A seat that re-derives a premise from something this brief did NOT give it is worth more than
one that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** There are three pristine-2021-upstream copies of
GXemul under the project root (`./src/` and two under `_archive/audit-results-*/builds/`). They are
NOT this fork. If your line numbers disagree with mine by hundreds you are reading one of them.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/`, `GXEMUL-SEC/regress/*.py` AND `GXEMUL-SEC/doc/` if it
exists.** Do not read `GXEMUL-SEC/regress/artifacts/` or `GXEMUL-SEC/tools/pipeline/ledger.json` —
they are this project's archive of past measurements, they are large, and nothing in them is needed
here.

**Where this brief states an ARITHMETIC claim, ENUMERATE it rather than reasoning about it.**

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## 1. THE SITUATION — one question, and the answer decides a severity

`alpha_translate_v2p()` in `src/cpus/memory_alpha.c` ends its page-table walk with:

    (*return_paddr) = ALPHA_PTE_TO_PFN(pte3) << pageSizeShift;

That is a **page-base** address: the within-page offset of the incoming `vaddr` is not added. Its
caller path, `memory_rw.c`, then computes

    offset = paddr & offset_mask;

which is **zero** for a page-base address. **If that walk is reached, every access within a page
resolves to the page's first bytes.**

**Two early returns avoid it, and I verified both**: the kernel direct-mapped K0SEG arm and the
`ptbr == 0` bootstrap arm each do `*return_paddr = vaddr & 0x000003ffffffffffULL`, which **masks**
the vaddr and therefore **keeps** the offset bits. Only the full walk drops them.

## 2. THE QUESTION

**Q1: can any machine this emulator can actually boot reach the full walk?**

The walk is reached when the early returns do *not* fire — i.e. in user mode, or outside K0SEG once
`apcb_ptbr` is non-zero. What I cannot settle by reading alone is whether any supported Alpha guest
gets that far.

**Evidence that it may NOT, which I want you to test rather than accept:**

* `memory_alpha.c` carries **seven** `TODO`s.
* It has an explicit `fatal("Alpha kernel virtual memory seems to want to be used. Not yet
  implemented.\n"); exit(1);` on `vaddr == 0xfffffffd80000000`.
* The `ptbr == 0` arm is introduced by a comment calling itself an **"UGLY hack for now"**.

**So which is it:** is this defect **LIVE** (some bootable Alpha guest walks page tables and silently
gets page-base addresses), or **LATENT** (Alpha VM is incomplete enough that nothing reaches the
walk, and the defect is real but unreachable)?

**Q2: what would settle it empirically?** Name the smallest observation — a machine type, a boot, a
debugger probe — that would decide it. This project's witness ladder wants a real guest instruction
through real address decode on an unmodified in-tree machine description; if that is impossible for
Alpha here, say so plainly and say why.

**Q3: does `apcb_ptbr` ever become non-zero on a bootable configuration?** That is the hinge. Trace
where it is written and whether any code path this emulator supports gets there.

## 3. WHAT I AM NOT ASKING

Do not propose a fix — the fix is obvious (add the offset back) and it is not the hard part. Do not
write test rows. **I want to know whether this is a live defect or a latent one**, because that
decides whether it outranks everything else in the queue or is documented-only.

**If the honest answer is "cannot be settled by reading", say that** — it is a real answer and I will
route it to a measuring seat rather than guessing.

**If, while verifying a claim, you found something ELSE — say so.** Tonight's best findings arrived
that way, including three defects in code nobody had looked at.
