# FIX DESIGN — `alphaswpctxptbr`: `swpctx` assigns `apcb_ptbr` twice and `apcb_flags` never

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** You have already corrected me four times today on
this file's neighbours. **Assume the framing below is too confident and find where.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies sit under the
project root and are NOT this fork.

**SCOPE:** `GXEMUL-SEC/src/cpus/cpu_alpha_palcode.c`, `src/include/thirdparty/alpha_cpu.h`,
`GXEMUL-SEC/regress/alpha_harness_probe.py`.

**VERDICT LINE FIRST.**

## §C — SETTLED PREMISES

**S1 — THE SITE**, `case 0x30` PAL_OSF1_swpctx, the "load new context" block:

```c
	:275	// Update all variables in the pcb simultaneously:
	:276	cpu->cd.alpha.pcb.apcb_ksp     = new_ksp;
	:277	cpu->cd.alpha.pcb.apcb_usp     = new_usp;
	:278	cpu->cd.alpha.pcb.apcb_ptbr    = new_ptbr;
	:279	cpu->cd.alpha.pcb.apcb_cpc     = new_cpc;
	:280	cpu->cd.alpha.pcb.apcb_asn     = new_asn;
	:281	cpu->cd.alpha.pcb.apcb_unique  = new_unique;
	:282	cpu->cd.alpha.pcb.apcb_ptbr    = new_flags;      <-- apcb_ptbr, again
	:283	cpu->cd.alpha.pcb.apcb_decrsv0 = new_decrsv0;
	:284	cpu->cd.alpha.pcb.apcb_decrsv1 = new_decrsv1;
```

**S2 — DERIVED BY COUNTING, not by reading intent.** Over `:274-292`, `apcb_ptbr` is assigned
**twice** and `apcb_flags` **zero times**; every other field exactly once. The SAVE block above
stores `apcb_flags` to `ctx + 40` and the loader reads `new_flags` from `ctx + 40`, so the value is
loaded and then put in the wrong field.

**S3 — TWO CONSEQUENCES, and the row records only the first.**
1. `apcb_ptbr` ends up holding the flags word — the clobber the witness measures.
2. **`apcb_flags` is never loaded at all**, so a context switch silently drops the new context's flags.

**S4 — MEASURED.** `regress/alpha_harness_probe.py`, rung 3, unmodified `-E alpha -e alphabook1`:
**HEAD 7/9**, `PCB_A+16` reads `0xbbbb2222` (A.flags) where `0xaaaa1111` (A.ptbr) is required. The two
red rows are `swpctx ptbr` and `swpctx notflags`; the other seven are controls.

## The questions

**Q1 — IS `apcb_flags = new_flags` THE WHOLE FIX?** It repairs both consequences with one token. **What
does it break?** `apcb_flags` is currently whatever the previous context left; making it track the
loaded value changes behaviour for any reader of that field. **Enumerate the readers** and say whether
any relies on the present (broken) behaviour.

**Q2 — DOES THE WITNESS GO 9/9, OR ONLY 8/9?** `swpctx ptbr` and `swpctx notflags` should both flip.
**Check that neither depends on `apcb_flags` staying stale** — the probe writes the same PCB fields it
reads.

**Q3 — IS THERE A THIRD CONSEQUENCE?** `:221` (`PAL_OSF1_wrfen`?) also touches `apcb_flags`. **Does
the never-loaded field interact with it**, and does `invalidate_translation_caches(..., INVALIDATE_ALL)`
at `:287` mask anything?

**Q4 — THE SMALLEST EDIT that breaks the fix and still passes.** I expect the clause-(d) family — a
repair conditioned on a field the block reads. Name the row you expect to stay green.

**Q5 — DOES THE ORDER MATTER?** `:275` claims the updates are simultaneous. If a reader observes the
PCB mid-block there is no such thing. **Is that claim false, or is it true because nothing can observe
it?**

## What I am not asking

Do not write a patch and do not run anything. **Nothing ships until the flagship adjudication on
2026-09-09.**

**If, while verifying a claim, you found something ELSE — say so.**
