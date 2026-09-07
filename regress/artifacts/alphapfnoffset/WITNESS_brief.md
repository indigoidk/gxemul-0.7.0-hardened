# WITNESS DESIGN — `alphapfnoffset`: the Alpha page-table walk drops the within-page offset

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** You reviewed the sibling harness for this same file
today and found that **every structure was planted past the end of RAM**, where writes are discarded
and reads return zeros — three rows would have gone green measuring nothing. **Assume this brief has
an equivalent defect and find it.** Separately, my first draft of the `lcaconfwidth` witness had its
**oracle polarity inverted** (it scored 6/6 on the committed build by asserting the defect as the
passing state); check that this design does not repeat it.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies sit under the
project root and are NOT this fork.

**SCOPE:** `GXEMUL-SEC/src/cpus/memory_alpha.c`, `cpu_alpha*.c`, `src/machines/machine_alpha.c`,
`GXEMUL-SEC/regress/alpha_harness_probe.py`, `GXEMUL-SEC/regress/lca_confwidth_probe.py`.

**VERDICT LINE FIRST.**

---

## §C — SETTLED PREMISES

**S1 — THE DEFECT.**

```c
	memory_alpha.c   (*return_paddr) = ALPHA_PTE_TO_PFN(pte3) << pageSizeShift;
	memory_rw.c      offset = paddr & offset_mask;
```

The walk returns a **page-base** address, so `paddr & offset_mask` is zero and a walked access
resolves to the page's first bytes.

**S2 — CONFIRMED BY EXHAUSTIVE ENUMERATION, not by argument.** A codex reachability pass walked all
**8,192 offsets**: the walk expression produces offset zero throughout, differing from the
offset-preserving address for **8,191** of them. It also confirmed the direct-mapped arms are safe —
K0SEG (`vaddr & 0x000003ffffffffff`) and the `ptbr == 0` bootstrap both **mask** the vaddr and keep
the offset bits — and that there are **three** bootstrap alias regions, not the two I had read.

**S3 — THE BLAST RADIUS IS NARROWER THAN THIS ROW ORIGINALLY CLAIMED.** My summary said *"every
walked access would land at its page base"*. Corrected: *"slow-path accesses consume the incorrect
physical offset, but cached Alpha loads/stores calculate `addr & 8191` themselves, so subsequent
cache hits can access the correct within-page bytes."* **The corruption is confined to the slow
path.**

**S4 — THE CONFOUND IS NOW MEASURED, WHICH IS WHY THIS BRIEF EXISTS TODAY.** The sibling row
`alphaswpctxptbr` — `swpctx` overwriting `apcb_ptbr` with the flags word — got a rung-3 witness this
afternoon: `regress/alpha_harness_probe.py`, HEAD **7/9**, `PCB_A+16` reading `0xbbbb2222` (A.flags)
where `0xaaaa1111` (A.ptbr) is required. **So any probe that establishes a context via `swpctx` and
then observes a bad translation cannot attribute it to the walk rather than to the swap.**

**S5 — THE HARD PART, in the words of the seat that named it.** The walk needs page-table state, and
*the ordinary bootstrap identity mapping bypasses the walk*. So a probe must first establish a
non-zero `apcb_ptbr` **and** a valid three-level table. Its own classification called this row
**COLD-DEBUGGER REACHABLE** but the hardest of five Alpha rows for exactly this reason.

**S6 — TWO WORKING PRECEDENTS EXIST NOW, both mine, both run today on stock `alphabook1`:**
`alpha_harness_probe.py` (7/9) and `lca_confwidth_probe.py` (4/6). Both plant 64-bit values with
debugger `put d` into RAM below 64 MB and load them with a guest `ldq` **while `ptbr` is still 0**;
both carry a control that separates *measured the thing* from *read an unmapped zero*.

---

## The questions

**Q1 — CAN `apcb_ptbr` BE SET WITHOUT `swpctx`?** S4 says the swap is a confound; S6's bootstrap
writes memory directly while `ptbr == 0`. **Is there a route that establishes a non-zero `ptbr` and a
valid three-level page table using only `put d` plus guest instructions** — or does every route pass
through the defective swap? If the latter, say so: this row then genuinely waits on
`alphaswpctxptbr`'s fix, which is a real answer.

**Q2 — WHAT IS THE MINIMUM PAGE TABLE?** Three levels, and the probe must build every entry by hand.
**Name the exact structure**: how many pages, at which physical addresses (all below 64 MB — see the
S6 trap), what each PTE must contain, and which `ALPHA_PTE_*` bits are load-bearing for the walk to
succeed rather than fault.

**Q3 — THE ORACLE, and it must be red pre-fix.** The defect makes a walked access land at the page
base. So: store a distinguishing value at `page + 0` and a different one at `page + N`, then read
`vaddr + N` through the walk. **Pre-fix it returns the `page + 0` value; post-fix it returns the
`page + N` value.** Is that right, and what N avoids the cached-path escape S3 describes — i.e. what
guarantees the access takes the SLOW path?

**Q4 — THE CONTROL that separates "the walk is wrong" from "the walk never ran".** If the mapping is
malformed the access faults or returns zero, which looks like a defect and is not. The sibling probes
use a legal round-trip through the same decode. **What is the equivalent here** — a K0SEG access to
the same physical page, proving the memory holds what we think?

**Q5 — IS THIS EVEN THE STRONGEST FORM?** `memory_rw.c` derives `offset` from the returned paddr, so
the defect might also be visible as a *write* landing at the page base and clobbering byte 0.
**Which direction makes the better witness**, and does the write form need fewer page-table entries?

## What I am not asking

Do not write the probe and do not run anything. **Nothing ships until the flagship adjudication on
2026-09-09.**

**If, while verifying a claim, you found something ELSE — say so.**
