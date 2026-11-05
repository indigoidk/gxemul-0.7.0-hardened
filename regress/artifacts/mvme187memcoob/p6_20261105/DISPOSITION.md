# mvme187memcoob PASS 2 on REPAIR 6 -- disposition (main loop, 2026-11-05)

Seats: GPT-6 Astra (codex, `ultra`) ANSWERED (codex_codex_memc_p6.txt; `CODEXP6MEMC: 693 CELLS SWEPT 0 BREACHES 2 FALSE RECORDS
VERDICT:REPAIR`; static analysis plus the recorded measurements).  Gemini 4 Argon: SEAT FAILURE -- the web route is down.
glm-5.3 and grok-4.7: walled.

THE OWN-LATCH CLASS IS CLOSED.  Codex enumerated it over 11 position/target pairs x 9 gates x 5 walker operations, plus the |= and &=
latch forms the walker lacks: 693 cells in all, 414 nonvacuous and detected, 279 no-op or unreachable.  31 cells fail only on
R18_lines; they map to the twelve measured representatives.  No undisclosed survivor was found.  This is the class closure the
premise asked for.  Codex's warning about counting is recorded: the 198 |=/&= cells are STATIC, not table-6 measurements.  Also
noted: R18's seven rows are one latch witness (R18_lines) plus collateral controls, and must not be counted as seven catches.
R18_18_r2 cannot see D12_def_store, which existing rows already catch.

TWO RECORDS, both applied by the main loop and each checked against its cited record:
1. probe :92, the NOCHANGE definition: "fired on the 206 rows, state unchanged" -> "fired on the 206 rows with no field byte or latch
   truth value changed".  Latch INTEGER state can change; the walker compares truth values (memc_variants_5.py:375-389).
   Text-only proof against table 6's frozen instrument: PASS (r7_20261105/TEXTONLY_PROOF_p6rec.out; diff .p6rec.diff).
2. The ruling's F1(b) sentence is not exhaustive inside its own scope.  L_ME_M_idat_W.nC is UNOBSERVED (PRETABLE_5.out:8017-8019)
   and still green at 213/213 (table6/SCORES.txt:92); its discriminator is the controller condition (address bit 8, tested only at
   the fold, :73-76).  An explicit erratum was added to ERRATA_r7_20261105.md item 1(a), saying the retarget does not validate the
   sentence; the contract already discloses the survivor.
THE FLOOR CHAIN CLOSES on this zero-breach pass, which carries its denominator.  A narrow second reading of the two record edits is
fired (recp6_20261105/).
