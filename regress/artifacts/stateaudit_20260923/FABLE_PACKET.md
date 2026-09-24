# Fable 5.1 -- adjudication of the 2026-09-23 records-versus-tree audit (you are the LAST seat; two others have answered)

Open your answer with the token `FABLE_SEAT_ALIVE_20260923_VERIFY` and the FIRST LINE of
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\CHECKPOINT.md` quoted verbatim.  Then ONE verdict line:
`VERDICT: DISPOSITIONS SOUND` or `VERDICT: <n> DISPOSITIONS WRONG`.  Then Q1-Q5 by number.  End with a seat record
(model, files read, commands run).  **READ-ONLY: read files and run read-only git; edit, stage, commit, delete, build
and run nothing.**  Plain engineering language throughout.

## What happened, in five lines

Windows Update rebooted the machine 2026-09-22 21:32; both working sessions had been idle since 2026-09-21.  The owner
asked whether progress was lost and for every uncommitted patch to be reviewed against the records, with any
discrepancy reviewed by Codex GPT-6 Astra, Grok 4.7 and you.  The main loop measured the state (`INVENTORY.md`); Codex
and Grok reviewed it (round 1) and then independently checked 81 recorded "applied" changes against the tree
(round 2); the main loop checked every claim the seats made before accepting or rejecting it.

## Read, in this order (all in `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\verify_20260923\`)

1. `INVENTORY.md` -- the state as first written (its errors are the subject of round 1).
2. `seats/grok_verify.txt`, `seats/codex_verify.txt` -- round 1.  `DISPOSITIONS_grok.md`, `DISPOSITIONS_codex.md` --
   the main loop's rulings on them, each with the check that settled it.
3. `APPLIED_CLAIMS.txt` (81 claims), `seats/grok_reconcile.txt`, `seats/codex_reconcile.txt` -- round 2.
   `DISPOSITIONS_r2.md` -- rulings, including the two places the seats disagreed and how each was settled.
4. Evidence files beside them: `cited_paths_missing.txt` (883 recent citations, 16 not on disk, classified),
   `untracked_cited_dirs.txt`, `status_counts.txt`, `checkers/*.out`, `vs_ff7ab93.txt`, `diffs/`.
The tree is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC` (HEAD `f685d75`); ignore every other `src/` under the project root.

## The main loop's current conclusions (check them; do not ratify them)

* **Nothing on disk was lost to the reboot.**  Name-status against the 09-21 full-tree snapshot: 0 deleted.  Of 883
  paths cited by records from 2026-09-12 on, none points at lost evidence (16 do not resolve: prose fragments, one spec
  deliberately never built, three name mismatches, two scratch helpers, and TWO durable copies that were promised and
  never made, whose sources survive in `_scratchpad`).
* **The records and the tree disagree in these places, all pre-dating the reboot:** two recorded-as-applied changes
  that are absent (round 2: `gdromdmadefault` [11]'s fourth comment correction; `stagetokens` [18]'s "ALL REPAIRED",
  whose dashboard half is unrepaired); a wrong record in the owner-held #545's draft (now corrected, and its M9 claim
  RE-MEASURED today on the final instrument: 33/37, predicted first); stale numbers in #529's uncommitted comments;
  `CHANGELOG.md:4285`, flagged 2026-09-18 and corrected nowhere; and 18 artifact directories cited by COMMITTED records
  that have no tracked file at all.
* **What was lost is synthesis, not evidence:** the peer session's work after its last checkpoint (09-21 15:0x) --
  #541's pass 6 (4-2 does not close, a codex seat refused on wording), its v8 instrument measured 34/36 -- exists as
  files but is in no ledger entry, changelog draft or checkpoint.
* **Verified work waits uncommitted in one shared tree** (units U1-U16 in `INVENTORY.md` section B, corrected by the
  dispositions), protected by `refs/snapshots/*` (latest 60b28f6, 2026-09-23).  Thirteen dated exemptions lapse on
  2026-09-28; the weekly battery on 2026-09-27 18:00 will fail gate 6 on the current files.

## Questions

**Q1 -- which of the main loop's ACCEPTED dispositions is wrong?**  About two dozen seat findings were accepted
(`DISPOSITIONS_grok.md` 8, `DISPOSITIONS_codex.md` 14, `DISPOSITIONS_r2.md` 3).  A review that accepts everything has
either had very good seats or stopped arguing; say which this is.  Name at least one disposition you would reverse or
narrow, or say plainly that none is wrong and why you are confident.  Be HARDER on the two round-2 disagreements the
main loop settled itself (the "row 9" attribution and claim 081): a ruling in favour of one seat is the one least
likely to have been tested.

**Q2 -- the loss claim, final wording.**  Is "nothing on disk was lost to the reboot; the records and the tree disagree
in the places listed, none caused by the reboot" supported by the evidence as it now stands?  If not, give the wording
the evidence supports.  What check, not yet run, would still falsify it?

**Q3 -- order of work.**  Rank the open repairs (R1-R8 in the three disposition files) and the uncommitted units by
SEVERITY, and split them into (a) records repairs the main loop may make now without an owner decision -- for example
copying a scratch source to the durable path a record already cites -- and (b) decisions that belong to the owner
(commits of held or other sessions' work, the census population, the thirteen exemptions).  Say which of (a) must NOT
be done by this session because another session owns the round.

**Q4 -- the 2026-09-27 battery.**  The two seats propose different minimal decision sets for gate 6 (codex: settle the
census population, then derive the pins; grok: change one spelling in the crime probe, grandfather two probes, write
three pins to the counts the 09-20 run printed).  Which is right, and is either one a check fitted to the current tree
rather than a decision about what the census should count?

**Q5 -- what did all three of us miss?**
