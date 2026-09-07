# AUDIT (read-only) — can `PAL_OSF1_swpctx`'s page-table-base corruption be witnessed at rung 3?

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Where I state something as fact, ask whether it is
true. A seat that re-derives a premise from something this brief did NOT give it is worth more than
one that agrees.

**Two briefs of mine this week stated false premises and I built conclusions on both.** One was a
variable's declared *type*; the other was *which of two arms is authoritative*. **If a premise below
is wrong, that is the most valuable thing you can tell me — and I am proposing a witness DESIGN here,
which is exactly the kind of thing that looks right and is not.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** There are three pristine-2021-upstream copies of
GXemul under the project root. They are NOT this fork.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/` AND `GXEMUL-SEC/regress/*.py`.** Do not read
`GXEMUL-SEC/regress/artifacts/` or `GXEMUL-SEC/tools/pipeline/ledger.json`.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## §C — PREMISES ALREADY SETTLED, RE-INLINED

**S1. The defect, verbatim** from `src/cpus/cpu_alpha_palcode.c`, `case 0x30: /* PAL_OSF1_swpctx */`.
Nine fields are saved, nine locals are loaded in the same order from the same offsets, and nine are
assigned — but the **seventh assignment names the wrong field**:

```c
			// Update all variables in the pcb simultaneously:
			cpu->cd.alpha.pcb.apcb_ksp = new_ksp;
			cpu->cd.alpha.pcb.apcb_usp = new_usp;
			cpu->cd.alpha.pcb.apcb_ptbr = new_ptbr;      /* correct */
			cpu->cd.alpha.pcb.apcb_cpc = new_cpc;
			cpu->cd.alpha.pcb.apcb_asn = new_asn;
			cpu->cd.alpha.pcb.apcb_unique = new_unique;
			cpu->cd.alpha.pcb.apcb_ptbr = new_flags;     /* *** should be apcb_flags *** */
			cpu->cd.alpha.pcb.apcb_decrsv0 = new_decrsv0;
			cpu->cd.alpha.pcb.apcb_decrsv1 = new_decrsv1;
```

Two consequences: `apcb_ptbr` is written twice and the **second write wins**, so the page-table base
becomes the flags word; and `apcb_flags` is **never assigned at all**, so it keeps the outgoing
context's value. The comment directly above says *"Update all variables in the pcb simultaneously"*.

**S2. `apcb_ptbr` is load-bearing for address translation**, not merely storage.
`src/cpus/memory_alpha.c` opens its page-table walk with
`uint64_t base = cpu->cd.alpha.pcb.apcb_ptbr << ALPHA_PAGESHIFT;`. It is the only consumer outside
the PALcode file.

**S3. The save side, same handler, runs BEFORE the load side** and writes the *current* pcb out to
the old context in guest memory, at these offsets:

```
    ctx +0  apcb_ksp     ctx +24 apcb_cpc      ctx +40 apcb_flags
    ctx +8  apcb_usp     ctx +28 apcb_asn      ctx +48 apcb_decrsv0
    ctx +16 apcb_ptbr    ctx +32 apcb_unique   ctx +56 apcb_decrsv1
```

**S4. MEASURED 2026-09-07 — the Alpha family is not dead.** `-H` advertises four subtypes and three
of them construct a machine and begin executing: `alphabook1` (21066), `alphaserver4100` (21164A-2)
and `eb164` (21164PC) all reach the debugger prompt on an unmodified command line. **The fourth,
`3000/300`, aborts the host** at `interrupt_handler_lookup("0") failed` during machine construction —
that is a separate, already-filed defect and is not this one.

---

## The questions

**Q1 — CAN A RUNG-3 WITNESS BE BUILT?** This project's ladder calls a witness rung 3 when a **real
guest instruction** travels **real dispatch** on an **unmodified in-tree machine description**, with
two controls: a LIVENESS control (a known value returns by the same route) and a control proving the
observed value came from the mechanism under test rather than from elsewhere. **Is that reachable for
`swpctx` on any of the three constructing Alpha machines?** If it is not, say so plainly and say what
blocks it — that is a real answer and the round proceeds as documented-only.

**Q2 — MY PROPOSED DESIGN, WHICH I WANT ATTACKED RATHER THAN POLISHED.** The obvious observable —
"translation goes wrong" — needs the MMU active and a page-table walk, which is a lot of guest setup.
**I think the corruption is observable with no MMU at all, because the handler writes the pcb back to
guest memory on the *next* switch:**

1. Guest builds two context blocks in RAM, A and B, with **distinguishable** `ptbr` and `flags`
   values at `+16` and `+40`.
2. `call_pal swpctx` with `a0 = A`. The buggy line sets `apcb_ptbr = A.flags`.
3. `call_pal swpctx` with `a0 = B`. The **save** side now stores `apcb_ptbr` to `A+16`.
4. Read `A+16` from the guest. **Correct code leaves `A.ptbr` there; the defect leaves `A.flags`.**

**Is that sound?** Specifically: (a) does step 3's save write to the *old* context, i.e. is
`cpu->cd.alpha.ctx` still A when the save runs — note the handler assigns `cpu->cd.alpha.ctx = a0`
*inside* the load block, after the save; (b) does anything between the two calls overwrite
`apcb_ptbr`; (c) is `call_pal 0x30` actually dispatched to this handler from a guest instruction on
these machines, or is PALcode entry gated by something I have not read?

**Q3 — WHAT ELSE WOULD THE PROPOSED WITNESS NEED TO CONTROL FOR?** A witness that shows the wrong
value for the wrong reason is worse than none. Name the controls you would require.

**Q4 — IS THE FIX REALLY ONE TOKEN?** I believe it is `apcb_ptbr` → `apcb_flags` on that one line.
**Is there any reading on which the current code is deliberate** — for instance, a PALcode convention
where the flags word carries the PTBR? I doubt it, but I have doubted correctly and been wrong twice
this week, and the neighbouring line `cpu->cd.alpha.r[ALPHA_A0] = cpu->cd.alpha.ctx;` sits under a
comment reading *"Return old context in **v0**"* while assigning **a0** — so this handler has at least
one other place where the comment and the code disagree.

## What I am not asking

Do not write the fix, do not write the probe, and do not run anything. I want to know whether a
witness is BUILDABLE and whether my design is sound, before any code changes.

**If, while verifying a claim, you found something ELSE — say so.**
