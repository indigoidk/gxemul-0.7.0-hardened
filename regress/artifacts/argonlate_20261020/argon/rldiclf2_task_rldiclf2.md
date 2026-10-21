# #565 -- wiring a regression probe into a test gate: the shared-findings pass

**Format:** open with the token `ARGON_RLDICLF2_20261018`, then ONE line `VERDICT: ANSWERED (<n> flags) -- <one line>`, then Q1..Q4.
Every FLAG is a line of its own starting `FLAG:`, citing `<label>:<n>`.  Facts and flags only; agreement is not wanted.

**This is a reading task on the ATTACHED files `argon_bundle_1.txt` and `argon_bundle_2.txt` (read both to the end) and
this message only.**  Bundle 1 is the packet the other seats answer (B): every pass-2 finding (F1-F13) with my
disposition, two disagreements (D1, D2), the repair diff and the re-run receipts.  Bundle 2 holds the FINAL probe in
full (P), the staged checker's lines that name the probe (X) and the two shell helpers the gate block uses (L).  Answer
B's section-6 questions Q1-Q4.  Anything this material cannot settle is UNSETTLED: name what would settle it.

Two angles the file-reading seats may miss, because they have the whole tree and you have only these lines:
1. Read P end to end against B's dispositions: is any sentence in P, AFTER the repair, false or over-qualified -- a
   receipt cited wrongly, a count that does not match the code (count the `row(` calls yourself), a qualifier that says
   more than its receipt?  Cite P:<n>.
2. D2: from P alone, does a dead-run medium (absent binary, `/bin/true`) exercise what an identity-body build would --
   i.e. which of P's rows can tell "rldicl wrote nothing" from "no instruction ran at all"?
