# Audit the adjudication packet against the tree -- before another model builds on it

## 0. WHAT TO READ

* **`GXEMUL-SEC/tools/pipeline/ADJUDICATION_20260909.md`** -- the artifact under audit
* `GXEMUL-SEC/src/devices/dev_sgi_re.c`, `regress/sgi_re_width_probe.py`, `regress/gate_arm.sh`
* `src/cpus/cpu_alpha_palcode.c`, `src/cpus/memory_alpha.c`, `src/cpus/cpu_arm_instr.c`
* `regress/artifacts/sgirekills/killtable_20260908/*.txt` and the `*_20260908.out` logs there --
  **these are the measurement records the packet cites; reading them is the point of this brief**

Please still avoid `tools/pipeline/ledger.json` (it is large and not the subject).

Tree: `GXEMUL-SEC/src/`. Ignore the pristine 2021 `src/` at the project root.

*** NO MUTANT, NO EVASION, NO GUEST SEQUENCE IS WANTED. *** This is a factual audit of a document
against the code and logs it cites.

## 1. WHY

That packet is what a different model reads tomorrow to adjudicate this queue. **This project has
measured that a wrong premise in a brief comes back CONFIRMED** -- a recent panel had seven of nine
seats ratify a census that was wrong by a factor of four, and one seat "corrected" it by silently
narrowing the claim, which hid the defect rather than fixing it.

So: **the packet is a set of claims, not a summary.** I wrote it. Check it.

## 2. THE ONE QUESTION

**Does every factual claim in that document hold against the tree and the cited logs?**

Quote the claim, quote the evidence, say which is wrong. Please separate:

* **WRONG** -- contradicted by the code or a log;
* **UNSUPPORTED** -- not contradicted, but the cited artifact does not establish it;
* **OVERSTATED** -- true in a narrower form than written.

The third category is the one I most want, because it is the one I keep producing: this round has
already had a claim of mine that `M8_texaccept` "measures the store-first design" withdrawn, because
that mutant also removes the announce and so cannot isolate what I said it isolated.

## 3. SPECIFIC THINGS TO CHECK HARDEST

**Q1. Every number.** `30/44`, `44/44`, `46/46`, `12 of 12`, `M4/M7 43/44`, `M8 40/44`,
`M13 44/46`, `M_bit6/7 45/46`, `M_bit9/10 46/46`, `35 - 6 + 14 + 1 + 2 = 46`. **Each should be
recoverable from a named log.** Say which, if any, are not.

**Q2. Section A2's account of the repair chain.** It says pass 2 found one latch cell, my repair
closed it, and pass 3 found four more of the same one-token shape. **Is the bit enumeration right?**
`d->warned` bits in use, which the widened `tex xbit` now fires, and which the two new rows cover.

**Q3. The Alpha claims in section B1/B2.** `ALPHA_TBIA()` passing `a1 = 0`; the `a0 >= 1` dispatch;
`vaddr_mask` defaulting to `(int64_t)-1`; `ALPHA_V0` being the idiom at eight sites in
`cpu_alpha_palcode.c` while `swpctx` uses `ALPHA_A0`. **I re-derived these myself but from the same
files you would read -- so tell me if I mis-transcribed any.**

**Q4. Section D's seat claims.** It asserts codex refused exactly two briefs, one prompt-level (zero
file reads) and one late, and that a records-only framing draws none. **You are the subject of those
claims.** If the characterisation is wrong, say so -- I would rather have that corrected than
flattering.

**Q5. Anything the packet OMITS that an adjudicator would need.** It is an index with dispositions,
not a summary; but if a decision it invites cannot be made from what it contains, name what is
missing. **In particular: does it state clearly enough where I have applied my own judgment versus
where a seat's finding is being reported?**
