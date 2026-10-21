# `vmedefaultkill` (#568) -- THE REPAIR-DIFF PASS: review the repair the adjudication ordered, and ask the floor question of the shipped composite

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

Check the premises, not just the derivations.  **THE TREE UNDER REVIEW IS `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/`'s
working tree, committed HEAD `86114a90`** (the round is uncommitted there; another session's uncommitted `dev_pcc2.c`,
`dev_lca.c`, `dev_sh4.c`, `cpu_alpha_palcode.c` and `mvme_pcctworeg.h` edits are NOT part of it).  Three pristine-2021
copies of GXemul sit under the project root; line numbers off by hundreds mean you are reading one.  **If you cannot read
files that is expected** -- the diffs and the measurement are inlined; name any premise you cannot settle from this
packet.  **VERDICT LINE FIRST.**

## 1. What this pass is, and the rule that stops it

Pass 2 of `#568` found ONE floor breach -- `if (writeflag == MEM_WRITE)` read as `if (idata)` in the population-2
announce arm passed every row of the 34-row rev-2 probe, MEASURED 34/34, because every population-2 store the probe made
was non-zero -- plus records defects.  The adjudication pass (Fable 5.1, GPT-6 Astra, GLM 5.3, Grok 4.7; all PROCEED WITH
CHANGES) ordered a repair; it is built and measured.  **This is that repair's own pass (the repair-chain rule).**  Review
EFFORT is scoped to the repair diff -- settled design is not re-litigated.  The FLOOR QUESTION -- does any one-edit mutant
inside the fix's DEPENDS-ON enumeration still pass all 38 rows -- is asked of the SHIPPED COMPOSITE (fix568b + rev 3).
**The chain CLOSES on the first pass that finds zero floor breaches, and that zero must carry its denominator: which
predicates, lvalues and mutant shapes you swept.**  A bare "no breaches" does not close it.

## 2. Settled (re-inlined)

* Census: 10 cased offsets; 26 population-2 registers (the header's word starts 0x04..0x8c minus the cased); 988
  population-1 word starts 0x90..0xffc; every sub-word start inside a population-1 or population-2 word faults; a
  sub-word access at a CASED base is serviced by that arm (population 4, `vmewidthlanes`).
* The m88k load/store path delivers naturally-aligned accesses only; `ld.d`/`st.d` is ONE len-8 call; the debugger's
  NO_EXCEPTIONS callers never reach the handler; a second fault while PSR.SFRZ is set becomes ERROR.
* `fatal()` prints and RETURNS; `debug()` is silent while free-running at verbosity 0.  A free-running population-1 fault
  prints NO host line at all -- MEASURED (8 faults, 0 `[ vme:`, 0 DATA_ACCESS lines; the stepped run prints 8).
* M_IDATA measured 34/34 on frozen rev 2 (PRETABLE_IDATA.txt written before the build).

## 3. The repair, verbatim

### 3a. The fix: fix568 -> fix568b (`src/devices/dev_vme.c`)

```diff
{FIXDIFF}
```

**The object comparison** (`killtable2_20261021/OBJDUMP_fix568_vs_fix568b.txt`, GCC 15.2.1 -O3, x86-64): the objects
differ BEYOND the read announce's format string -- the added comment lines move DEVINIT's `__LINE__` (231 -> 234, via
`CHECK_ALLOCATION`'s `FAILURE()`), and the `(unsigned long long)` cast changes `-O3`'s layout of `dev_vme_access`
(registers, padding, two branches, the read-announce call duplicated; `.text` 1890 -> 1970 bytes).  Behaviour is what
table 2 measured.

### 3b. The probe: rev 2 (34 rows, md5 19de15b3) -> rev 3 (38 rows, md5 ddcebfe3)

{PROBEDIFF}

### 3c. The gate-14 block, verbatim (`regress/gate_arm.sh`)

```sh
{GATEBLOCK}
```

## 4. Kill table 2, measured (rev 3 frozen, fix568b, a fresh clone of HEAD 1a59a47e's tree)

{KT2}

## 5. Questions

1. **The repair against the adjudication.**  Does it implement every ordered change -- F1's zero-store row (own
   session, `st r0`, the WRITE-FORM literal checked), F10's rows (`p2 nw rd 2`/`p2 nw wr 2` in the SAME process; `p1
   quiet` over the census AND `p1 widths`' free runs; two lane-0 accesses in `p1 widths`), the CONTROL split and its
   definition, the per-site neutral wording, the docstring repairs, the comment/typedef changes, D1's `%llx`?  Name any
   that is missing, wrong, or stronger than its measurement.
2. **THE FLOOR QUESTION, on the composite.**  Enumerate the predicates dominating the fix's edited lines (to the function
   boundary) and the body-read lvalues (`writeflag`, `relative_addr`, `len`, `idata`, `odata`, `d->warned_unimpl`).  For
   each operand swap or weakening, name the row that reds it -- the table's measurement where it exists, your reading
   where not.  **Give the denominator.**  In particular: is the zero-store row enough for the `if (idata)` CLASS, or does
   another data-dependent swap of the direction predicate, the latch test or the label dispatch pass 38/38?
3. **Records.**  Anything in the rev-3 docstring, PRETABLE2, the table-2 summary or the gate comment that is false or
   stronger than the measurement -- in particular any place that still calls fix568b "comment-only".
4. Anything else you found.

## 6. Answer format

Your token first, then ONE line `VERDICT: CLOSE | REPAIR AGAIN | CANNOT SETTLE -- <one line>`, then Q1..Q4.  Every
proposed escaping mutant as a one-line diff, marked OWED (it will be built and measured).  Facts and flags only.
