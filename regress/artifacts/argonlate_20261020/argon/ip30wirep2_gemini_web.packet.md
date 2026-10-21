# Reading task: #566 ip30 gate wiring, pass 2 (Argon) (Gemini web; 2026-10-18)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-IP30WIREP2-92ab` on a line of its own.

# #566 -- wiring a regression probe into a test gate: pass 2 on the diff

**Format:** open with the token `ARGON_IP30WIREP2_20261018`, then ONE line `VERDICT: ANSWERED (<n> flags) -- <one line>`, then Q1..Q4.
Every FLAG is a line of its own starting `FLAG:`, citing `<label>:<n>`.  Facts and flags only; agreement is not wanted.

**This is a reading task on the ATTACHED files `argon_bundle_1.txt` and `argon_bundle_2.txt` (read both to the end) and
this message only.**  Bundle 1 is the brief the other seats answer (B): my dispositions of pass 1 and two disagreements
(B, section 0), the diff (section 2), the receipts (section 3).  Bundle 2 holds the edited probe in full (P), the commit
copy of the checker's lines that name the probe (X) and the two shell helpers the gate block uses (L).  Answer B's
section-4 questions Q1-Q4 from this material.  Anything it cannot settle is UNSETTLED: name what would settle it.

Two angles the file-reading seats may miss, because they have the whole tree and you have only these lines:
1. Read the dated correction note at the top of P's CONTRACT against P's own later sections and B's receipts: is any of
   its five statements false or over-qualified (row names, cell counts, which mutant each row closes, the 10/33)?
   Cite P:<n> and B:<n>.
2. Read the block's stall disclosure (B, section 2a) against every session() call in P: which rows read a stalled
   session (one the 12 s poll kills before its stepped access ran) green, and does the comment name exactly those?
   Cite P:<n>.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`IP30WIREP2: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
