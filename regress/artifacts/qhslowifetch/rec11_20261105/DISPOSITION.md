# qhslowifetch -- second reading of the pass-11 records corrections (main loop, 2026-11-05)

GPT-6 Astra (codex, `ultra`) ANSWERED (codex_codex_qhs_rec11.txt; `CODEXRECP11QHS: 6 ACCEPTED 2 TO FIX VERDICT:FIX`).
* ACCEPTED: R2, the gate comment, and ALL FOUR of the implementer's deviations from the ruler's wording.  On deviation 1 codex
  confirmed that the block does not test pc's low two bits (`(pc & ~3)` at :4168).  Low-bit self-referential toggles are caught by
  the marker-set cells and exact final-pc rows.  B1's DEBT grading stays consistent: the operational line is existing marker-set
  coverage, not which bits a block predicate tests.
* FIX: R1's sentence and the partner-loop comment still inferred two firings from an unchanged condition alone.  Codex's
  counterexample, derived from the source: `if (msr & ME) pc ^= 0xfec02000` keeps its condition but moves pc's page bits, so the next
  slot fetches RAM and the second failed visit never comes.  It is a records defect, not a detector escape.
Applied by the main loop as a PROVISO, with no new explanation: "provided both failed-fetch visits still happen and nothing between
them changes the toggled state", in the docstring (with codex's counterexample, marked DERIVED) and in the partner-loop comment
(r7_20261105/ppc_ifetch_probe.py.rec11.diff; copy .pre_rec11).  Text-only proof re-run: r7_20261105/rec11_proof.out, all six
EQUAL, negative control DIFFERENT, docstring max width 131.  A third reading, scoped to the proviso, is fired (rec12_20261105/).

*Corrected 2026-11-05 (main loop): this file's time-of-day stamps (removed: ~15:2xZ) were GUESSES that ran up to 3.5 hours AHEAD of the clock; the qhs landing-kit agent found them by checking against the files' own timestamps.  The file's own timestamps are the record: created 12:14Z, last written 12:14Z before this note (UTC).*
