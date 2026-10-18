# `#564` sgirekills (MTE half) -- PASS 3: THE REPAIR'S OWN REVIEW

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A repair made in response to a pass 2 owes its own pass.  **Review effort is scoped to the repair diff (section 3);
the FLOOR QUESTION -- does any mutant in the vacuity floor's (d) enumeration sweep the SHIPPED COMPOSITE detector
clean? -- is asked of the whole detector, not just the new rows.**  A zero is a valid closing answer only with its
denominator: say which cells and mutant shapes you swept.  Check the premises, not just the derivations.

**THE TREE IS `GXEMUL-SEC/` AT HEAD `2951694f` PLUS THIS ROUND'S UNCOMMITTED EDITS** to `src/devices/dev_sgi_re.c`,
`regress/gate_arm.sh` and the new `regress/sgi_mte_decline_probe.py` -- the repaired state is inlined below.  Other
uncommitted files belong to another session.  Ignore the pristine upstream copies of GXemul under the project root.

**If you cannot read files that is expected** -- every fact you need is inlined.  Name any premise you cannot settle.

**VERDICT LINE FIRST.**

---

## 1. What pass 2 and the shared-findings pass decided

Pass 2 (`pass2_564_20261017/`): GPT-6 Astra SHIP WITH CHANGES (3), Grok 4.7 SHIP WITH CHANGES (2), GLM 5.3 SHIP WITH
CHANGES (3); Fable 5.1 SEAT FAILURE (HTTP 429, held by owner ruling).  A late Gemini 4 Argon reading of the same packet
(`argon_mte564p2.txt`) rediscovered both floor findings below independently.  The shared-findings pass
(`f2_564_20261017/`): Astra ALL UPHELD, GLM ALL UPHELD, Grok "1 WRONG (F9)" -- the floor upheld and the packet's append
recipe corrected (map B and LIN_B where first used, repaint every cell, linear cells at depth 8 / full mask / no COPY).

**The two floor breaches (L2, repaired in-round):**
* **F9 -- the destination labels.**  S1's and S2's `return` bypasses `switch (dst_tlb)`, so under the 2026-09-25
  skipped-dispatch label clause the floor for EACH is {A, B, C, LIN_A, LIN_B} x latch {CLEAR, SET}: 20 cells, of which
  the 53-row detector held 9.  `if (src > MTE_TLB_C && dst_tlb != MTE_TLB_B)` kept all 53 rows green.  Labels 3 (TEX),
  6 (CLIP) and 7 reach `default:`, which only prints, and are excluded.
* **F10 -- the latch alias.**  `SGIRE_W_MTE_STIPPLE = 1 << 10` (an alias of `SGIRE_W_BADMODE`) kept all 53 green: the only
  pre-existing latch bit any session set was `SGIRE_W_TLBA_LEN`.

**Records and disclosures adopted:** F1 -- a START-tagged READ also runs the transfer (`if (startFlag)
do_mte_transfer(cpu, d);` has no `writeflag` test), so the fix's comment that "the register store that carried START has
already landed" is corrected; F2 -- the probe header's "the paint is read after EVERY transfer" is false for the 32-mask
sweep; F3 -- five PRETABLE statements were wrong (errata file, section 6); F4/F7/F8 -- disclosed in the contract: the
printed VALUES are unchecked, source 1 is never driven, a decline that writes an MTE register is unobserved.  Rejected
on measurement: GLM's "a fourth diff hunk was never shown" (four were).  Added from Astra's F2 answer: accept rows at
tiled B and C, so a guard grown to refuse one tiled label is visible.

## 2. The repair, and its measurements (every number names its log, under `regress/artifacts/sgirekills/`)

* `dev_sgi_re.c` 1d65cdc1 -> **23fa76aa**: F1's comment correction only -- no executable change.
* `sgi_mte_decline_probe.py` 86caed24 -> **8928a02f**, 53 -> **68 rows**: S2 with the latch SET at B, C and LIN_B (appended
  AFTER the S2 session's last existing check, tile B and LIN_B mapped where first used); four new sessions, each
  pairing one S1-CLEAR and one S2-CLEAR cell (S1 at B / S2 at C; S1 at C / S2 at B; S1 at LIN_A / S2 at LIN_B; S1 at
  LIN_B / S2 at LIN_A); legal tiled fills at B and C appended to the ACCEPT session; a CROSSBIT session that sets every
  pre-existing latch bit 0-12 first (the priming sequence `sgi_re_colourdefault_probe.py`'s `allbits` rows proved, plus
  its colour decline for bit 12), proves all 13 announced (`xbit primed`), then wants each new site to announce once
  (`xbit texts`); the contract and NOT CLAIMED list rewritten.
* `gate_arm.sh`: the block now pins all 68 names, rows emitted 68, green 68, red 0.
* **Kill table 3** (`killtable3_564_20261017/`, PRETABLE3.out written BEFORE it): 29 mutants -- the 20 latch-conditioned
  label exemptions, one alias per new latch bit onto a pre-existing one, and S1/S2 grown to refuse every transfer to B
  or to C -- plus base, null and HEAD legs.  Its summary is section 5.
* Tables 1 and 2 stand as evidence for the 53 rows they scored on the old instrument: the repair only APPENDS (no
  existing row's commands before its read changed); aggregate rows can change VALUE under a mutant (`src once` reads
  10 where it read 7 for a missing-suppression mutant) and stay red -- a source-derived argument, not a re-measurement.

## 3. The repair diff (against the pass-2 state, preserved beside this file)

