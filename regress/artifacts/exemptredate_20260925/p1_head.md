# #550 exemptredate -- PASS 1 on the exact proposed diff: eleven dated test exemptions re-dated one by one

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  Where I state something as fact, ask whether it is true.  A seat that re-derives a premise
from something this brief did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`.**  Other copies of GXemul under the project root
are not this fork.  **Do not read `regress/artifacts/` other than this round's own directory,
`regress/artifacts/exemptredate_20260925/`, and do not read `tools/pipeline/ledger.json`.**

**If you cannot read files that is expected** -- every fact you need is inlined.  Name any premise you cannot settle
from this packet rather than guessing at it.  **VERDICT LINE FIRST**: `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`,
then numbered findings.

## 0. HAS THIS ALREADY SHIPPED?  (run before writing this brief)

    git log -1 -- tools/pipeline/check_probe_wiring.py   ->  f4f601c4 2026-09-24 #548 fbdrainwire ...
    git log -1 -- regress/gate_offline.sh                ->  f4f601c4 (same commit)
    grep exemptredate CHANGELOG.md                        ->  nothing
No.  This is a new round, #550.

## 1. WHAT THIS IS

A test-harness change only -- no emulator code.  `tools/pipeline/check_probe_wiring.py` is a pre-commit checker: every
detector script under `regress/` must be run by a gate, or carry a DATED exemption.  An exemption is valid ON its date
and the checker FAILS from the day after (`d < today`), which blocks every commit.  Ten exemptions all carry
2026-09-27, so every commit from 2026-09-28 would be blocked.  Gate 2 (`regress/gate_offline.sh`) has a second,
separate list, SC_EXEMPT (two offline differentials exempt from a comparator self-check), also dated 2026-09-27; there
the expiry turns one gate row red rather than blocking commits.

## 2. PREMISES ALREADY SETTLED, RE-INLINED SO NOBODY SPENDS AN ANSWER RE-DERIVING THEM

* **Owner ruling 2026-09-24 (verbatim):** "Re-date all ten individually -- each gets its own date and reason now; no
  wiring work this week."  So wiring any of the ten probes is OUT of scope for this round, by decision, not oversight.
* **Owner ruling 2026-09-25, on SC_EXEMPT:** "Fix wdc_identify now" -- a separate round (#551) moves that differential's
  rows onto a shared comparator with a sentinel before 2026-09-28; only `ieee_store` is re-dated here.
* **The comparison is a strict `d < today`**, so an entry is GREEN on its own date and RED the day after.  The checker's
  own selftest derives its two boundary days (M5a on the earliest detector exemption's date, M5b the day after) from the
  table -- they are not literals (#536), so a re-date does not break the selftest by construction.
* **The constraint the re-date answers** (ledger row `exemptcliff`, filed 2026-09-17): eleven, then ten, entries were
  aligned on ONE date twice, so the checker reds on all of them at once and the natural response is a bulk re-date.
  "A date nobody chose is a date nobody owns."

## 3. THE PROPOSED DIFF, EXACT (three files; nothing else changes)
