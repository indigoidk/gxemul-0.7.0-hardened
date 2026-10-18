**Your token: `ASTRA_FHF_CF_20261018`** -- open your answer with it.

# CONFIRM: `fableheldform`'s records commit -- which of my dispositions is wrong, and is every drafted fact exact?

Tree `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`, HEAD `d42c76a8`, READ-ONLY.  The design pass is in
`regress/artifacts/fableheldform/design_20261018/` (your answer `codex_fhfp1.txt`, Grok's `grok_p1.txt`, GLM's `glm_p1.txt`,
Fable's wall `fable5_p1_WALL.txt`, the census `CENSUS.txt` and `CENSUS_wide.txt`).  The drafted commit is in `confirm/`:
`LEDGER_preview.txt` (every changed ledger field, built from HEAD's blob), `OB_section.md` (appended to OUTSTANDING_BUGS.md),
`CHANGELOG_block.md` (prepended; `{CONFIRM}` is this pass), `COMMIT_MSG.txt`.

All three seats chose option A, and the draft implements it: fifteen walls take the HELD token, prose kept; cxlaunchquotation's
2026-10-16 v2 and V3 walls take the non-answer token (Grok: a later pass Fable answered superseded each, and a HELD tag dated
the day of V4 could never discharge); nine rows go closed -> held, closure objects kept, `reopened` naming every commit whose
subject called the row closed (derived from `git log` with section L's own closure regex, `\b(closed|closes|closing)\b`),
a dated warrant, and the walled pass's packet prepended to `hold_question`; wiringcliff gains #565's question;
`fableheldform` goes to held; `untokenedanswers` (MED) is filed.  The owner question (option E) is recorded in
`fableheldform`'s hold_question, not acted on.  Pretests on the unit: H, O, I, L (0 hard; every reopened commit reported
REOPENED) and R all pass; the subject carries no closure word and the message no section-C path.

## Questions
1. **Which disposition is wrong?**  Be hardest on: (a) the nine hold_question packets -- is each the question Fable was
   actually held for (`WALLED_STAGES.txt` maps each walled entry to its sibling seats' evidence)?  (b) cxlaunchquotation [8]
   and [12] taking the non-answer token rather than HELD; (c) `untokenedanswers` -- is its title or note false or
   over-stated (the 497 is a keyword correlate)?
2. **Is every drafted fact exact** -- each date, commit, count, row id and path in `confirm/`?
3. **Anything the commit's own hook (`tools/precommit_check.sh`) would refuse?**

Open with your token, then ONE line `VERDICT: <n> flags -- <one line>`, then `FLAG:` lines with `file:line` evidence and the
replacement text, then short answers to 1-3.
