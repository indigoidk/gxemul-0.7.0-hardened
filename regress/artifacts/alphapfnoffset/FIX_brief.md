# FIX DESIGN — `alphapfnoffset`: restore the within-page offset in the walk's result

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** You designed the witness for this row today and
refuted the premise I built its brief around. On the sibling `swpctx` round you ratified a one-token
fix and then **refused to ratify it as the round**, because the witness could not distinguish it from
a lesser edit — and you were right; the row you demanded caught a real second consequence.
**Do the same here.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**

**SCOPE:** `GXEMUL-SEC/src/cpus/memory_alpha.c`, `memory_rw.c`, `cpu_alpha_instr_loadstore.c`,
`GXEMUL-SEC/regress/alpha_pfnoffset_probe.py`.

**VERDICT LINE FIRST.**

## §C — SETTLED PREMISES

**S1 — THE SITE**, `alpha_translate_v2p`, after the third-level PTE is validated:

```c
	:163	if (!(pte3 & ALPHA_PTE_VALID)) { fatal("TODO: pte3 not valid.\n"); goto not_found; }
	:168	(*return_paddr) = ALPHA_PTE_TO_PFN(pte3) << pageSizeShift;
	:170	// TODO.
	:171	return 2;
```

`pageSizeShift` is 13. The result is a page BASE; `memory_rw.c` then takes
`offset = paddr & offset_mask`, which is zero.

**S2 — MEASURED, rung 3.** `regress/alpha_pfnoffset_probe.py` on unmodified `-E alpha -e alphabook1`:
**HEAD 5/6**. One cold guest `ldq` of `vaddr + 8`, through a hand-built three-level table, returns the
`data + 0` value (`0xaaaa0000aaaa`) where `data + 8` (`0xbbbb0000bbbb`) is required. Four controls
green, including a three-way sentinel that separates *walk never completed* / *landed on unmapped
physical* / *right page, wrong offset*.

**S3 — THE IDIOM IS ALREADY IN THIS FUNCTION.** The direct-mapped arms preserve the offset by masking:

```c
	:63	*return_paddr = vaddr & 0x000003ffffffffffULL;
	:81	*return_paddr = (vaddr & 0x7fff)  + HWRPB_PADDR;
	:88	*return_paddr = (vaddr & 0x1fff)  + PROM_ARGSPACE_PADDR;
```

`:88` is exactly the shape the walk needs — mask the low bits, add the base — **twelve lines from the
defect, in the same function.**

## The questions

**Q1 — IS `| (vaddr & ((1 << pageSizeShift) - 1))` THE WHOLE FIX?** State the exact expression you
would write, and say whether `|` or `+` is right here (the PFN is shifted left by 13, so the low bits
are known zero — does that make them equivalent, and does it matter for readability or for a future
edit?).

**Q2 — WHAT ELSE CONSUMES THIS RESULT?** `return 2` is the success path. **Enumerate the callers** and
say whether any relies on receiving a page base — a caller that adds its own offset would then double
it, which is the mirror defect and would be invisible to my probe.

**Q3 — DOES THE WITNESS GO 6/6, AND IS IT ENOUGH?** This is the `swpctx` question again. My probe has
one defect row (`walk off`) and four controls. **What lesser edit also scores 6/6?** I am specifically
worried about an edit that masks with the wrong width — `0xfff` or `0x3fff` instead of `0x1fff` —
which would be correct at `N = 8` and wrong further into the page. **If a second row is owed, name the
address and the expected values**, as you did for `A+40`.

**Q4 — THE `// TODO.` AT `:170`.** It sits immediately after the assignment. **Does it refer to this
line, to the missing protection checks, or to something else?** If the walk is meant to also return
protection bits, a fix that only restores the offset leaves the TODO true and the round should say so
rather than deleting it.

**Q5 — DOES THIS INTERACT WITH THE CACHED PATH?** You established that the fast path caches from
`paddr & ~offset_mask`, so the walked paddr is wrong only for the fill. **After the fix, does anything
double-count the offset** — the fill now returning an offset address while `update_translation_table`
still masks it off?

## What I am not asking

Do not write a patch and do not run anything. **Nothing ships until the flagship adjudication on
2026-09-09.**

**If, while verifying a claim, you found something ELSE — say so.**
