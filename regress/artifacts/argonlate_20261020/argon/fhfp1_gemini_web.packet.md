# Reading task: fableheldform design, pass 1 (Argon) (Gemini web; 2026-10-18)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-FHFP1-1b4c` on a line of its own.

# fableheldform -- recording a reviewer seat's walls when the rows they sit on are already closed (design, pass 1)

**Format:** open with the token `ARGON_FHFP1_20261018`, then ONE line `VERDICT: <option A/B/C/D or other> -- <one line>`, then Q1..Q5.
Every FLAG is a line of its own starting `FLAG:`, citing `<label>:<n>`.  Facts and flags only; agreement is not wanted.

**This is a reading task on the ATTACHED files `argon_bundle_1.txt` and `argon_bundle_2.txt` (read both to the end) and
this message only.**  Bundle 1 is the brief (B) and its census (C).  Bundle 2 is the wide census (W) and the two code
excerpts the brief cites (H, T).  Answer B's questions 1-5 from this material.  Anything it cannot settle is UNSETTLED:
name what would settle it.

Two angles the file-reading seats may miss:
1. W shows the defect is SYSTEMIC (every seat, August onward).  Should the fix stay scoped to the sixteen post-2026-10-17
   Fable entries, with the wider class filed -- and what STRUCTURAL check (not prose) would stop a new untokened
   non-answer being written?  Cite W:<n> and T:<n>.
2. Read T's live_holds discharge rule against C's cxlaunchquotation and dashokclass lines: which of their walls would a
   prefixed token leave LIVE, and which would earlier or later Fable answers discharge?  Cite C:<n> and T:<n>.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`FHFP1: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
