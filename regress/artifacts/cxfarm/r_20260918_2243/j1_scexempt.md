# J1 -- `scexempt`: two SELFCHECK comparator-control exemptions in gate 2 come due 2026-09-28.  Which disposition?

## READING SCOPE AND FORM

The tree under review is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` (git HEAD cdbe7d7).  Pristine 2021 copies of GXemul
under the project root (`./src/`, `_archive/`) are NOT this fork.  Do not read `regress/artifacts/`, the ledger, the
CHANGELOG or OUTSTANDING_BUGS; the facts you need are here.  Read-only: no edits, builds or runs.
VERDICT LINE FIRST.  Mark claims READ (file:line), REASONED or NOT CHECKED; counts carry denominators; check the
premises rather than ratifying them.

## THE SITUATION

`regress/gate_offline.sh` ("gate 2") requires every offline differential `regress/diff_*.c` to carry a
`@@SELFCHECK@@` block -- a deliberate mismatch fed through the file's comparator, proving the comparator can fail
(a "liveness control, never a census").  Two files are exempt, with dates, in `SC_EXEMPT` (grep `^SC_EXEMPT=`):

    ieee_store    "HAS NO COMPARATOR TO SENTINEL": each section carries its own counter (abs_bad, rm_rn_bad,
                  rm_rz_bad, rm_d_bad, rm_vec_bad, interp_bad) with the comparison inline dozens of times; the gate
                  greps one summary line per counter for 0.  "A probe through a comparator NO REAL ROW USES would
                  prove nothing."
    wdc_identify  "NOTHING TO FEED A MISMATCH TO": row_anchor, row_slave, row_base_drive, row_identity,
                  row_atapi_flags, row_wide_geometry, row_no_lba_claim, row_selfconsistent are zero-argument with
                  the expected value hardcoded in the body, and row(why, sectors) derives its expectation from its
                  input.  "This one needs the nine row functions refactored onto a shared helper first: a round,
                  not a line."

Both dates were 2026-09-02; nobody owned them; gate 2's row "SELFCHECK manifest: no exemption is past its dated
deadline OR malformed" has read `got= ieee_store wdc_identify want=none` on every run since 2026-09-03 and was first
observed red on 2026-09-18.  The owner re-dated both to 2026-09-27 (the comparison is a strict `<`, so red returns on
2026-09-28) and wants a decision before then.  The sibling list, SM_EXEMPT (self-mutant lanes), was ruled "fix it, do
not re-date" the same day.

## QUESTIONS

1. **wdc_identify, enumerate before judging.**  Open `regress/diff_wdc_identify.c`.  List EVERY row-emitting
   function and every call site (name, line, how its expected value is obtained: hardcoded literal / derived from
   an argument / derived from device state).  Is "nine row functions" the right count today?  Which of them could
   route through ONE shared comparator helper WITHOUT changing what any existing row asserts, and which cannot
   (say why: e.g. the expected value is computed inside the body)?  Give the minimal helper signature that would
   let a `@@SELFCHECK@@` mismatch row be fed through the same path real rows use.  Estimate the diff size (lines
   touched, rows unchanged).
2. **ieee_store, re-check the premise.**  Open `regress/diff_ieee_store.c`.  Is it still true that no single
   comparator exists?  Count the inline comparison sites per counter.  Is there a form of `@@SELFCHECK@@` that a
   REAL row path uses (e.g. one of the counters' own increment sites), so the control would not be "a comparator
   no real row uses"?  If not, say so with the count.
3. **How does the rest of gate 2 treat these two?**  Grep `gate_offline.sh` for `ieee_store` and `wdc_identify`:
   which rows already cover each file (verdict token, row count, the selfmutant lane for wdc_identify -- it IS in
   SM_COVERED), and does that existing coverage change the cost of a permanent exemption?
4. **Disposition per file**, from: (a) discharge before 09-28 (a bounded harness change -- say what it is),
   (b) re-date with a reason and a named prerequisite, (c) delete the entry and take the permanent red,
   (d) a far-future date with its reason recorded, the form `ieee_store:2099-01-01` already uses in SM_EXEMPT.
   Give one per file, with the fact that decides it.
5. **Standing licence:** anything else you found in these two files or the SC block while verifying (a stale
   comment, a row that cannot fail, a count that disagrees with the file).
