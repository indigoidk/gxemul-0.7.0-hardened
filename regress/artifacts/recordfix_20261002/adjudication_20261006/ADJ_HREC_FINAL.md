# Harness record corrections -- final rulings on the 27 keys (2026-10-06)

Adjudicator: the main loop (Claude Opus 5.5), owner's instruction 2026-10-06.  Evidence: one read-only Opus helper
(ADJ_HREC.md), every key settled against HEAD 96a44fe3; GPT-6 Astra at `ultra` checked all 27 against the files
(`aconf_hrec/codex_aconf_hrec.txt`: 2 of 27 wrong, DENOMINATOR 27 of 27); grok-4.7 xhigh ruled the one floating-point
dispute (`grok_f6.out`: ASTRA RIGHT), per the owner's arrangement that grok rules Astra's findings.

## Rulings

* **25 keys: as ADJ_HREC.md states** (Astra RIGHT on each).
* **hsgideprimopprobe:F3 -- the helper was WRONG, the GOVERNING replacement fits.**  Astra, verified here: every alias
  mutant reds the `xlatch all` row (`regress/artifacts/sgideprimop/killtable_20260902_table10/M_ALIAS0..8.out`, e.g.
  M_ALIAS6 `xlatch all 0 1 ... FAIL`), and `xlatch pre` separately witnesses the six setup events.  The helper conflated
  setup witnessing with alias coverage.
* **hdiffieeestore:F6 -- the helper's new S-format predicate is WRONG; Astra's is exactly right** (grok, traced at
  `src/core/float_emul.c:377-388,663-665` and `regress/diff_ieee_store.c:145-149,296-304`): `trunc(-0.5)` is `-0.0`,
  the kept sign makes `-2^-150` store `0x80000000` where the old path stored `0x00000000`.  The S underflow term is
  `isnormal(x) && 0 < abs(x) < 2^-126 && (signbit(x) || abs(x) >= 2^-149)`.  The D-subnormal half of the helper's
  correction stands.
* **key 17**: verdict stands; Astra flagged its supporting evidence as incorrect -- the replacement stays generic
  ("unwires its detectors"), and the commit that applies it cites no count it has not measured.

## A further wrong record found by grok, not in the 27

`regress/diff_ieee_store.c:296-301` says a sub-quantum input "agrees with upstream"; true for POSITIVE inputs only
(`-2^-150` differs).  The sweep still classifies it correctly (`:420`), so nothing is unexplained or missed; the comment
owes a correction in the same records commit.

## Counts

27 keys: current false 26, current true 1 (key 11 -- the false text is `tools/propagate_all_trees.sh:9-16`, not
`tools/precommit_check.sh:1037`); ruled replacement fits 20 (19 + F3); new wording 7 (F6 as Astra's predicate);
already fixed at HEAD 0; plus 1 extra (the diff_ieee_store.c comment).
