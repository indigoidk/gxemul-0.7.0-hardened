**Your token: `ASTRA_CLOSE531C_20261018`** -- open your answer with it.

# MICRO-CONFIRM: did the third draft apply your four confirm flags exactly, and did it add any false sentence?

Tree `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`, HEAD `8faf4a16`, READ-ONLY.  Your confirm is
`regress/artifacts/ip30abortkill/close_20261018/codex_close531b.txt`.  The third draft is `close_20261018/draft_r3/`
(`LEDGER_preview.txt`, `OB_preview.diff`, `CHANGELOG_block.md`, `COMMIT_MSG.txt`); the second, which you reviewed, is
`draft_r2/`.

What changed, per your flags:
1. `ip30abortkill` is NOT closed: state `in work` -> `held`, no `closure` object, the walled closure review is a review-stage
   `[HELD AWAITING SEAT: fable5]` marker with the wall receipt as `ev`, and `hold_question` carries the closure review plus
   the REGRESS measurement; no REGRESS hold is added until the close.  `check_stage_panels.py` on the unit's ledger: PASS,
   reporting `HOLD ip30abortkill review 9/9 awaiting: fable5`.
2. `heldrecedits` carries 30 items -- the 29 `src/` comments (#560's 12, #561's 17) and #560's `hrec extra` -- and names
   the seven `hrecordowed` members as staying there.
3. No "no commit has made"; the lists are dated 2026-10-06 and reconciled against HEAD before applying.
4. No seat note quotes a stage token; `stage_tokens.is_answer()` on the unit's ledger returns True for the codex, grok, glm
   and confirm entries and False (held) for fable5.

Questions: (1) is each flag applied exactly?  (2) any new false sentence in `draft_r3/`?  (3) anything that would make the
commit's own hook (`tools/precommit_check.sh`) refuse it -- e.g. a `held` row whose stage lacks the question, or a new row
id named in the subject?

Open with your token, then ONE line `VERDICT: <n> flags -- <one line>`, then `FLAG:` lines with `file:line` evidence.
