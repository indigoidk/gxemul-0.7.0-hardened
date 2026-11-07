# Gemini-web work on the oldest open issues -- the second bank, 2026-11-07 (PROPOSALS: none adjudicated, none applied)

HEAD when banked: `61629244`.  The first bank is `regress/artifacts/geminidrafts/drafts_20261107/` (8d9df658); this one adds what came after it, in a new directory so
the first bank's citations keep pointing at what it said.  Every count below is derived by `tools/build_bank2.py.txt`'s
source (`_scratchpad/wgemdrafts/build_bank2.py`) from the files banked here.

## Fix drafts -- `fixes/`, `plan/fixcheck_results.tsv`

159 rows drafted (oldest first; the FIX-NOW rows that cite a source line, plus 20 that name a file whose line was LOCATED by a
specific identifier -- `tools/mk_fixpacket_located.py.txt`).  Compile check: BUILD_OK 111, SKIP 48.
**Every BUILD_OK draft changes code** (`plan/commentonly.tsv`: {'CODE': 108, 'COMMENT_ONLY': 3}; the COMMENT_ONLY rows are RECORD rows whose defect is a
comment).  The check now scores an empty edit list NO_EDITS -- the first bank's "74 compile" counted 4 such drafts and 3
comment-only drafts on code defects (corrected in place there).

## Reviews -- `reviews/`, `plan/FIXREVIEWS.md`

Every compiling draft has a second-lens review of its CURRENT version (the row, the diff, every edited function in full):
{'SOUND': 72, 'DEFECT': 34, 'UNSETTLED': 5}.  ONE revision round, capped: the DEFECT drafts were revised once with the review's findings (the drafter accepting or
rejecting each); a DEFECT on a revised draft is NOT revised again -- it is a pointer for the adjudication.  Same model drafted
and reviewed (badge `s`).

## Records checks -- `records/`

Every HELD row that carries a commit (34 at 8d9df658) has had a records check of its round block or commit message; every
claimed contradiction was settled against the round's own artifacts (`records/HELD6_RECORDS.md`, `CLOSED8_RECORDS.md`,
`OLDEST3_RECORDS.md`).  Gemini's packet-fed claims were mostly compressed sentences or two instruments read as one.

## Closures and next steps -- `plan/CLOSEDRAFTS.md`, `plan/NEXTSTEPS.md`

For the 80 oldest open rows the triage proposed closing (DOCUMENT-AND-CLOSE / DROP / CLOSE-OVERTAKEN): a closure record, or a
DISAGREE where the row still names work owed (CLOSE-OVERTAKEN drafts name the discriminating control as OWED, never done).  For
the rows it disagreed on: ONE next step each (fix round, measurement, reading, record, owner decision), drafted where the row's
own text settles a reading or a record.  Where the two passes disagree, a row is NOT closed on either pass's word.

## The plan -- `plan/FIXPLAN.md`

The rows that need a decision before any round (peer-held files, held-back rows, APPLY_FAIL, UNSETTLED with a named gap),
Gemini's candidate shared-round groups under the round-scope rule, and two same-function CONFLICTS.
