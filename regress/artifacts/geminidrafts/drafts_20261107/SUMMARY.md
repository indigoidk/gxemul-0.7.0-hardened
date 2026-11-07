# Gemini-web drafts for the oldest open issues -- banked 2026-11-07 (PROPOSALS: none adjudicated, none applied)

Made 2026-11-06/07 by the main loop (Opus 5.5) driving Gemini web (gemini-4-argon, the local web2api proxy, one Google
session; up to six parallel senders, no unusual-traffic check).  Owner directions: "keep utilizing gemini web on the oldest
set of the issues that we need to resolve"; "land everything".  HEAD when banked: `521d136a`.

## 1. Adjudication drafts -- `adjudication/OLDBATCH_DRAFTS.md`

Every open/held ledger row (asanstale and gateflr excepted, ruled and held for Mythos), oldest first by the earliest date in
the row, seven per packet, 158 batch replies banked.  COVERAGE, measured against HEAD `521d136a`: 1045 of its 1045 open/held rows have a
proposal (the ledger changed while the queue ran -- two records commits filed rows and closed one -- so each batch was cut from
the ledger of its moment; the rows filed after the queue passed them went out as a top-up batch, `oldbatch_900`).
One PROPOSED disposition per row: FILE 518, FIX-NOW 312, OWNER-DECISION 103, DOCUMENT-AND-CLOSE 56, CLOSE-OVERTAKEN 27, DROP 22, UNSETTLED 7.
A second pass with each row's FULL text (`oldbatch_911`-`918`) re-drafted the rows first proposed UNSETTLED; its
proposals supersede the first ones in the tally above.  `adjudication/ownerdigest/` groups the OWNER-DECISION rows into
themes with recommended defaults -- two of which conflict with standing owner rulings (a Fable bypass; a CI that does not
exist here) and are Gemini's suggestions only.
**The main loop's commits check** (a FIX-NOW or CLOSE-OVERTAKEN proposal on a row whose `commits` field is set -- its own
round shipped, and what it owes is its held stage) is written into the file after each batch: Gemini cannot tell "fixed,
awaiting review" from "live", so neither proposal is to be acted on without that check.

## 2. Fix drafts -- `fixes/`

For the oldest rows proposed FIX-NOW that carry no commit and cite a source line (101 rows; Alpha/LCA rows and rows with an
earlier fix draft excluded): one packet per row with HEAD's code at each cited line (and, from the second version of the
packet, the data structures it names), asking whether the defect is still present and for the minimal fix as exact edits.
101 answered.  Each "still present" draft was applied to a scratch clone at HEAD and built (`fixcheck_all.sh`):
APPLY_FAIL 1, BUILD_OK 74, SKIP 26 (`fixes/fixcheck_results.tsv`). [2026-11-07, records: 4 of these 74 applied NO edit (an empty edit list, scored BUILD_OK on an unchanged HEAD) and 3 change only a comment where the defect is in code -- 67 are real fixes; the check now scores NO_EDITS, and `regress/artifacts/geminidrafts/drafts_20261107b/SUMMARY.md` carries the current counts]  BUILD_OK means applied once per edit and compiled with no new error -- NOT reviewed, NOT
witnessed, NOT measured; each still needs the round's full process.

## 3. The attachment budget -- `attachments/`

One message's attachments share ONE budget of about 60-70 KB (~25k tokens of C source): a 30 KB and a 60.5 KB file arrived
whole; 120.5 KB was cut at 64-70 KB, 240.6 KB at 43-56 KB, three 30.5 KB files at ~68 KB in all (`ATTTEST_SCORES.txt`).
So attachments add no capacity over a 60 KB inline packet; the drafts above were all sent inline.
