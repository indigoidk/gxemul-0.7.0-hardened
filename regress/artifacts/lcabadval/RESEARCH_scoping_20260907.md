# RESEARCH TASK (read-only) — scope an error-handling round in `dev_lca.c`

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Where I state something as fact, ask whether it is
true. A seat that re-derives a premise from something this task did NOT give it is worth more than one
that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** There are three pristine-2021-upstream copies of
GXemul under the project root (`./src/` and two under `_archive/audit-results-*/builds/`). They are NOT
this fork. If your line numbers disagree with mine by hundreds you are reading one of them.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/` AND `GXEMUL-SEC/regress/*.py`.** Do not read
`GXEMUL-SEC/regress/artifacts/` or `GXEMUL-SEC/tools/pipeline/ledger.json` — they are this project's
archive of past measurements, they are large, and nothing in them is needed here.

**Where this task states an ARITHMETIC claim — a count, a set of values — ENUMERATE it rather than
reasoning about it.** Walk the values. A derivation that skips one masking line reads exactly like a
correct one.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## Context

GXemul is a machine emulator. `src/devices/dev_lca.c` models the DEC LCA (Alpha) chipset bridge. This
fork's standing goal is **robust error handling**: where a device model meets a register value it does
not implement, it should report the condition and continue rather than calling `exit(1)` and ending the
emulator process. A simulated peripheral should degrade gracefully.

This task scopes the remaining sites **before** a design proposal is written. Nothing is being changed.

## 1. THE COUNT AND THE CLASSIFICATION — please re-derive both

A previous reading recorded **eleven** live terminating calls in this file, in four kinds. That reading
was itself corrected once — it listed a `dev >= 21` range check among them, and the source shows that
guard's body is a **commented-out** `fatal()` + `exit(1)` with `dev = 0;` executing instead. So the
count and the classification have both moved before.

**Q1: re-derive the live count and classify each site.** My working classification, offered so you can
disagree with it rather than reconstruct it:

* **two INTERRUPT STUBS** — `lca_interrupt_assert` and `lca_interrupt_deassert`, each a bare
  `fatal("...TODO"); exit(1)` with **no guard at all**;
* **one BUS check** — `bus != 0`;
* **one RANGE check** — `ofs > len`;
* **six VALUE checks** — each accepting a small set and ending the process otherwise, e.g.
  `idata & ~1`, `idata != 0x700000ULL`, `idata != 0x3ff00000ULL`.

**If that split is wrong I want to know before a design brief is written on it.**

## 2. THE DISPOSITION QUESTION — and one disposition may not be available here

When a device model meets input it does not implement, this project recognises seven dispositions:
**1 remove the check · 2 ignore the access silently · 3 ignore it and report once · 4 accept it (the
model already computes the right answer) · 5 signal a bus error to the guest · 6 accept it into
invented storage · 7 implement the missing behaviour.**

**Q2: which disposition does each site want, and do they all want the same one?** A round may cover a
second site only if one design covers both and one test covers both with no new observation — so if
these split across dispositions, this is several rounds and I would rather know now.

**Two things I believe about this file, both stated as questions because I am not certain:**

1. **The two interrupt stubs may need disposition 7, not any refusal.** The other five dispositions all
   presume the access is a *refusal decision* — but a stub has no predicate and no value being refused;
   there is nothing to decline. Is that right, and if so what would implementing them involve?
2. **Disposition 5 may be UNAVAILABLE on this machine.** Signalling a bus error works because
   `memory_rw.c` dispatches an exception on a failed device access — **for MIPS and M88K.** I do not
   believe there is an Alpha equivalent. **Please check this against the source**: if there is none,
   any proposal reaching for disposition 5 here owes Alpha exception delivery first, which is a much
   larger round than it looks.

**And GREP THE FILE AND ITS SIBLINGS FOR THE EXISTING IDIOM before answering.** The tree's own
precedents are part of the design space. In particular, **this file appears to contain its own
precedent**: the `dev >= 21` guard mentioned above already does *delete the check, substitute a safe
default, keep going*. Is that a transferable warrant for the other sites, or is it specific to that
one?

## 3. WHAT WOULD A TEST LOOK LIKE

**Q3: is any of these sites reachable by a guest on a machine this emulator can actually boot**, and
what would a test observe? This file has **no** regression test today. I am not asking you to write
one — I am asking whether one is possible, because if every site needs a machine that cannot boot, the
honest disposition is a documented-only round and I would rather know that now than after a design
panel.

## 4. WHAT I AM NOT ASKING

Do not write the change. Do not write test rows. I want: the count, the classification, whether it is
one round or several, and whether dispositions 5 and 7 are available here at all.

**If, while verifying a claim, you found something ELSE — say so.** The last three rounds' best
findings arrived that way, including two defects in code everyone had called correct.
