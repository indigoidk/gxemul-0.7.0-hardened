**Your token: `ASTRA_CLOSE531B_20261018`** -- open your answer with it.

# CONFIRM: `ip30abortkill`'s closure records, revised after the closure check -- which of my dispositions is wrong?

**Please do not simply ratify.**  Tree: `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`, HEAD `8faf4a16`.  READ-ONLY.  Judge the
ledger by `git show HEAD:tools/pipeline/ledger.json` (the working tree carries other units' lines).

You answered the first closure check (`regress/artifacts/ip30abortkill/close_20261018/codex_close531.txt`).  Grok 4.7
(`grok_close531.txt`) and GLM 5.3 (`glm_close531.txt`, packet-fed) answered the same packet; Fable 5.1 walled
(`fable5_close531_WALL.txt`).  The revised records are in `close_20261018/draft_r2/`: `LEDGER_preview.txt` (every changed
field, now with the three seat entries), `OB_preview.diff`, `CHANGELOG_block.md` (`{CONFIRM}` is this pass),
`COMMIT_MSG.txt` (`{CONFIRM_LINE}` likewise).  The first drafts the seats read are in `close_20261018/draft/`.

## My dispositions (10 of 10 accepted or overruled by me -- attack them)

| # | seat | finding | disposition |
|---|---|---|---|
| A1 | Astra | three questions #531's CHANGELOG block filed (string truth, per-instance latch, fall-through) were on no row | TAKEN: `ip30abortresidual` item (3) |
| A2 | Astra | the Fable closure-check entry said "not tried" | TAKEN in substance, NOT in form: a `[NOT A SEAT ANSWER]` entry with the wall receipt, because a review-stage `[HELD AWAITING SEAT: fable5]` on a CLOSED row is refused by `tools/pipeline/check_stage_panels.py` (CLOSED-WHILE-HELD; `STAGES` is assess/research/review, so the REGRESS hold does not block).  Fable's closure-review question rides on the REGRESS hold's `hold_question` |
| G1 | Grok | no carrier for V7/V8; delete `ip30abortresidual` | OVERRULED 2-1 (you and GLM upheld a carrier); A1's three questions decide it; V7/V8 ride on it as FILED coverage debt; Grok's dissent recorded on the row |
| G2 | Grok | #561's places 7-10 are #561's held set; moving four splits one obligation; "three sentences that still count five ISR sites" is inexact (place 8 counts BITS) | TAKEN: the four stay on #561's list; a NEW row `heldrecedits` carries all 37 held edits (#560's 20, #561's 17) as one obligation, pointing at the bug file's two held lists |
| G3 | Grok | the same Fable record as A2 | TAKEN, as A2 |
| L1 | GLM | Fact 1's line numbers contradict Fact 2 | TAKEN as a packet defect (Fact 1 was `grep -n` over the diff text) |
| L2 | GLM | drafts cite `gatewire_20260918/` and `close_20260918/` | REJECTED: zero such paths in the packet or any draft |
| L3 | GLM | the shipped `acc 20000` row should red V7 | REJECTED: its oracle accepts `_d20000 >= 0`, so N = 0 passes (`ip30_abort_probe.py`, the `_got20000` line), and `killtable4_20260918/V7_nocounter.raw` shows that row green; now stated in the residual |
| L4 | GLM | place 8 "three bits on the ISR side" may write a false comment | REJECTED on reading: it replaces `dev_sgi_ip30.c`'s "five bits on the ISR side" (the per-offset hypothetical), and three write arms announce after F13 |
| L5 | GLM | "matrix" vs "dashboard" | TAKEN as wording |

## Questions

1. **Which of the ten dispositions is wrong?**  Be hardest on A2's FORM (is a `[NOT A SEAT ANSWER]` entry plus a REGRESS
   hold an honest record of a walled closure review, or does it hide the stage from section H in a way the owner's
   2026-10-17 directive -- "Fable stages HELD with a question" -- forbids?) and on G1/G2 (is `heldrecedits` the right
   reconciliation, or a third place tracking one obligation?).
2. **Are the revised texts exact?**  Check every number and path in `draft_r2/` -- especially the new row
   `heldrecedits` (37 = 20 + 17; 29 `src/` comments = 12 + 17; 3 edits to then-never-commit files; 5 to
   `regress/diff_ieee_store.c`) against `OUTSTANDING_BUGS.md`'s `### #560` and `### #561` sections and
   `regress/artifacts/recordfix_20261002/adjudication_20261006/EDITS_561.json`.
3. **Did the revision introduce any new false sentence?**

Answer format: open with your token, then ONE line `VERDICT: <n> flags -- <one line>`, then one `FLAG:` line per defect
with `file:line` evidence and the replacement text, then short answers to 1-3.
