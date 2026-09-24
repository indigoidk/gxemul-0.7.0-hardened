You are reviewing a test-coverage change in a C hardware emulator (GXemul) before it is committed.  Read-only review.

Read `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\fbdrainwire_20260924\f2_brief.md` first.  It is the
adjudication packet: every finding the whole panel raised on the previous pass, the author's disposition of each, the
disagreements, the measurements of the repair, and the exact diff (HEAD -> revision 3) that will be committed.  The tree
is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\` -- ignore any other `src/`.  In the working tree, `regress/gate_arm.sh` and
`tools/pipeline/check_probe_wiring.py` carry another unit's uncommitted lines too; review the diff in the packet.

FIRST LINE: `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then numbered findings.

Your job is the adversarial one.  Two of this job's earlier findings were accepted and repaired (the zero-count probe
edit, F3; the per-timer lowering behind R5's maximum, F6) -- be HARDER on those repairs than on anything else, and check
the author's FIX, not only that the finding was right.  Then:

1. Name the author's accepted dispositions that are WRONG (count them), and why.
2. For each NEW row in revision 3 -- the FBDRAIN_TIMER pin and `fbd_ran`, the UNCAPPED-3052 pin, the [1, 762] backlog
   range, R6's printed owed/end counts and gate 2's two named-row pins, the distinct-rate R6b -- name the smallest edit
   (file, line, exact tokens) that breaks what the row CLAIMS and still passes every row.  The packet says the ask-again
   cap is spent, so say whether your edit is outside the contract (a breach) or inside what it discloses.
3. What did every seat miss?

Settle by reading the files or by arithmetic.  Say plainly what is a reading and what is a measurement.  No files may be
changed.
