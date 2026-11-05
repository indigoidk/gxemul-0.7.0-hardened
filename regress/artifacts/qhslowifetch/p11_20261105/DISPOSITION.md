# qhslowifetch PASS 11 -- disposition (main loop, 2026-11-05)

Seats: GPT-6 Astra (codex, `ultra`) ANSWERED (codex_codex_qhs_p11.txt; `CODEXP11QHS: 16 CELLS SWEPT 1 BREACHES 2 FALSE RECORDS
VERDICT:REPAIR`; source-derived).  Gemini 4 Argon: SEAT FAILURE -- the web route is down (control errors since ~11:07Z; bank_gweb.py
blocked the transport at 11:38Z).  glm-5.3 and grok-4.7: walled.

* B1: `if (translation_readahead || (msr & PPC_MSR_RI)) msr ^= PPC_MSR_RI;` -- the first visit sets RI, the second clears it, the
  partner does neither: a mutation that creates and consumes its own intermediate condition, which the pairing invariant's equal-
  baseline premise does not reach.  THE GRADING IS A RULE QUESTION: the block tests MSR only through `msr & ME`; MSR[RI] is a bit it
  never tests, and the condition reads the state the toggle writes.  PROPOSED (not ruled): clause-(e) DEBT, with the pairing invariant's
  scope stated honestly.  Sent to the ruler (local Mythos 5.1): prompt mythos_local/prompt_qhs_adj11.md -> ../adj_p11_20261105/.
* R1 (L4): the contract's universal pairing guarantee is false as stated.  R2 (L4): next_ic is WRITTEN by the block (:4177, :4207);
  the exclusion must say its value is not read.

## The ruling (2026-11-05): ../adj_p11_20261105/ADJ_MYTHOS_local.md -- `0 FLOOR 1 DEBT 2 RECORDS UPHELD VERDICT:CLOSE-AFTER-RECORDS`

The ruler (local Mythos 5.1) graded B1 clause-(e) DEBT.  Its discriminator against the caught read-ahead-only member is `msr & RI`, a
test of a bit the block never masks or compares (the `#549` latch x bit shape, NOT CLAIMED).  The same self-referential shape on a
TESTED bit (ME; pc's low bits) is caught by the generating-set rows; the ruler derived both from the code, not by measuring them.
It CORRECTED the main loop's proposal: the pairing invariant does not "cover" self-referential toggles on tested state.  Those are
caught by OTHER rows, and the contract must say which rows catch them; the family splits by whether the marker bit is in the
generating set.  R1 and R2 were upheld, with replacement text.  The records corrections are contract text, so no pass 12 is owed; a
second reading of the corrected text is still owed, because a correction is not safer than what it corrects.  Applied by the round's
implementer (Opus 5.5, resumed), who was told to verify each claim in the ruler's text before writing it.

*Corrected 2026-11-05 (main loop): this file's time-of-day stamps (removed: ~13:1xZ, ~13:5xZ) were GUESSES that ran up to 3.5 hours AHEAD of the clock; the qhs landing-kit agent found them by checking against the files' own timestamps.  The file's own timestamps are the record: created 11:41Z, last written 11:45Z before this note (UTC).*
