# Round 2 (reverse reconciliation of 81 applied-change claims) -- main-loop dispositions

Seats: Codex GPT-6 Astra (`seats/codex_reconcile.txt`, 20,673 b, 0 refusal / 0 wall) -> `VERDICT: 2 ABSENT of 81`;
Grok 4.7 (`seats/grok_reconcile.txt`, 12,463 b) -> `VERDICT: 1 ABSENT of 81`.  Both found the calibration case.

## Reconciled result: 2 ABSENT of 81, both PRE-DATING the reboot (present in ff7ab93 and 60b28f6)

1. **Claim 015 -- `gdromdmadefault` entry [11] (2026-09-17).**  "FOUR APPLIED"; three are present (`gdrom_default_probe.py`
   :108 no-data latch-scope wording, :116 arming/SET disclosure, :132/:133 clause-(e) grading).  *** CORRECTED by the
   Fable 5.1 adjudication (W1), verified by reading: the fourth WAS applied, at `:160-166` and `:1608-1610`; `:1187` is a
   THIRD sibling that was MISSED ("BOTH are on the ARMING arm"), and `:1186`'s "true when written" is false.  This
   section first said "was never applied", my brief's calibration premise said the same, and both seats ratified it. ***
2. **Claim 081 -- `stagetokens` entry [18] (codex, 2026-09-18), in a CLOSED, COMMITTED round (#534, 686d179 09ded75).**
   The entry's Q4 list ends "ALL REPAIRED".  Settled by READING, not by vote: the original finding
   (`_scratchpad/panel_20260918_124702/codex.txt`, Q4 item 1) has two halves -- the CLOSURE half ("a closed row passes H
   and I; the wall omits it"), which WAS repaired (CHANGELOG.md:992), and the DASHBOARD half ("The dashboard's
   malformed-marker fallback also disappears when the filer has an answer"), which was NOT: `tools/pipeline/
   gen_dashboard.py:143-146` keeps the fallback inside `if not ents:` (seats with no answer only) and `:173` excludes
   held records from an answered seat's cell.  Codex: ABSENT.  Grok: PRESENT-HEAD "half-fix", i.e. it saw the same fact
   and classified by the better half, against the brief's "classify by its worst part".  **Codex's class stands.**
   Disposition under the late-dissent rule (closure changes the licence, not the truth): the "ALL REPAIRED" sentence
   is an L4 wrong record, corrected in place by a later ledger entry; the unrepaired dashboard half is a FILED item
   (render a malformed hold in an answered seat's cell), low severity -- a display defect, the closure checks are right.

## Disagreements between the seats, and how each was settled

| topic | Codex | Grok | settled by | result |
|---|---|---|---|---|
| "row 9's repair" (claims 014, 018, 019, 024, 027, 033, 034, 037, 055, 056) | PRESENT-WT at `gdrom_default_probe.py:1579` (the tightened `accept dma` oracle, "Transfering 408 bytes") | PRESENT-HEAD at `dev_dreamcast_gdrom.c:1497` | `git log -S'd->data_len'`: :1497's `d->data_len` is #462's PRODUCT fix (7c9dd9e, 2026-08-24).  Row 9 = `gdromacceptdmanum`, whose repair is the DETECTOR oracle -- working tree only (HEAD's `accept dma` tests bare "Transfering"). | **Codex right; Grok conflated the product fix with the oracle repair.**  No ABSENT verdict moves. |
| claim 081 | ABSENT | PRESENT-HEAD (half-fix) | reading the original Q4 finding and gen_dashboard.py (above) | **Codex right.** |
| class boundaries (ip30abortkill [1][2][11][22][27][38]; crimewidthkill [106][147]; lcaisalane [98][107]; n6 [25]) | mostly SUPERSEDED / PRESENT-WT | mostly PRESENT-HEAD / NOT-A-CHANGE | not settled here -- none changes an ABSENT verdict | left for the adjudicating seat if it matters |

Per-class totals as each seat reported them (not reconciled): Codex PRESENT-WT 25 / PRESENT-HEAD 26 / ABSENT 2 /
SUPERSEDED 10 / NOT-A-CHANGE 18; Grok 12 / 38 / 1 / 4 / 26.  The ~13-claim swing between WT and HEAD is mostly the
row-9 conflation.

## New repairs from round 2 (NOT applied yet)

* R7 (U5's owner, with U5): apply the fourth `gdromdmadefault` [11] correction at `gdrom_default_probe.py:1187`.
* R8 (records): a ledger entry on `stagetokens` correcting [18]'s "ALL REPAIRED", and a FILED row for the dashboard
  half (answered-seat malformed hold renders as a plain answer).
