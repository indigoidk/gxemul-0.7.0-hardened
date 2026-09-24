<!-- the Opus 5 measuring seat's answer, extracted from its subagent transcript; model claude-opus-5-5; 2026-09-24T06:48:06.660Z -->
OPUS547F2_ALIVE
# CHECKPOINT -- 2026-09-24 00:55 (087a90 sections rewritten; the peer's sections below are untouched)

VERDICT: U=SHIP WITH NOTES; R=SHIP WITH NOTES

U is a correct comment-only change. R's committed code is correct on all current data. But four of your in-place corrections carry new errors, two of them errors I handed you, and they need fixing before #547 lands.

I wrote nothing under GXEMUL-SEC, est or the build trees, and ran no gates or builds; HEAD is still 3e33201d. To check the fixes to my own findings I did read, narrowly: the worktree diffs of `check_commit_attribution.py` and `CHANGELOG.md`, the named ledger fields at JSON level, and `.git/objects/pack/` timestamps. Commands 36–59 are in `_scratchpad\opus547\COMMANDS.log`; scripts and outputs are in `...\opus547\r\`.

## (1) Adjudication

**On U**
- **F1 — REFINE. MEASURED: I had one number wrong.** `git ls-tree HEAD -- HISTORY` shows `100644 blob fe69d3e…`, so HISTORY exists at the repo root. That makes it **7 of 9** entries naming files that do not exist, not 8. My pass-2 existence check ran in an export holding only src/ and test/, so it could not see the root. The rest stands: debugger.c is excused by lines 2 and 3, debugger_cmds.c by line 3, and option (b) would excuse only dev_sgi_re.c.
- **F2 — UPHOLD. MEASURED.** `schtasks /query` shows the battery task runs `wsl.exe -d Gentoo -- bash …/nightly_battery.sh`. Gate 8 therefore uses grep 3.12, which prints the binary-file notice on stderr.
- **F3 — UPHOLD** (wording).
- **F4 — UPHOLD. REASONED.** The rest of gate 8 compares binaries, and U cannot move them. Still, "not measured" should stay in the record.
- **F5 — UPHOLD. MEASURED.** schtasks: last run 9/20 18:00, result 1, next run 9/27 18:00. `git grep nightly_check` over tracked tooling and `grep -rn nightly_check .claude/` find only documentation. Nothing runs the dead-man switch.
- **F6 — REFINE. MEASURED: the precommit check must read the index, not "index or HEAD".** The HEAD export exits 1 and HEAD+U exits 0. So a precommit check scoped to HEAD would **block U's own commit**, and would pass a commit that adds the string. HEAD is right only for gate 8, where the battery grades committed state. glm's point about the shared `tmp_delete.out` file stands.
- **F7 — UPHOLD, with an obligation.** MEASURED: the live ledger has no `upstreamdeleteprose` row yet, and no `deletecheckhead`, `attrcheckgaps`, `batterymissedruns` or `carrierstalecopies` rows either.
- **F8 — REFINE** (wording). All seven "drop the exit(1)" sites are in dev_sh4.c, so it is one file's idiom rather than a house idiom.
- **F9 — UPHOLD.**

**On R**
- **F10 — OVERTURN part (b).** MEASURED: the worktree file still says at line 254 "git resolves the abbreviation it has just printed -- a lookup, never a comparison". The corrections touched only part (a). Part (a)'s new comment has its own errors; see (2).
- **F11 — UPHOLD** as a filing. REASONED: I found no live trigger. But one assertion closes it; see (3).
- **F12–F16 — UPHOLD. MEASURED** with `battery_f2.py`: Q0–Q15 rebuilt from your table, 49 mutants.
  - Every construction you named dies on the control you named: codex's on Q10a/b (8 HARD at 12 and at 40), grok's `t in full` on Q11, first-token-only on Q0 and Q12, my N10/N11 on Q13, and my C4/N7 on Q15.
  - **Two gaps remain:**
    - **Lg5** — it rebuilds the `subjects` join, a line 3e33201d changed, from the wrong field. It survives all of Q0–Q15 and changes the NEVER NAMED count on current data (114 → 135 at depth 60).
    - **C1** — it passes `h` instead of `full` at the reopened call site and survives Q0–Q15. That argument is unpinned because Q5 has no twin for `reopened`. A Q16 in `q16.py` — reopened opening with the full 40-character hash at depth 130 — gives REOPENED on the committed code and HARD under C1.
- **F17 — UPHOLD, with a cheap tripwire.** MEASURED: `git cat-file --batch-check` over all 184 ledger tokens takes 0.106 s and reports 184 commits; `effaced` and `deadbee` come back "missing". One call covers this finding and note 1.
- **F18 — UPHOLD.**
- **F19 — REFINE. MEASURED: this is F6's problem, in section L.** Graded against the worktree ledger the check reports `21 attributed, 0 hard, 10 soft`. Against the index ledger it reports `20, 0 hard, 11 soft`. The extra line is a hygienecensus "closed documented-only" line that appears only in the index. Section L grades a file other than the one the commit records.
- **F20 — SKIP.** It needs regress/artifacts/, which I did not read.
- **F21 / D4 — UPHOLD the refutation. MEASURED.** numstat is 23/6, and hunk 1 has 15 added lines in git, in brief.md and in f2_brief.md.
- **F22 — UPHOLD.**
- **F23 — REFINE. MEASURED: the fix carries my own error.**
  - The 23:57 times on three `.pack` files are mtime refreshes from later writes, not creation times.
  - The `.idx` and `.rev` files are written once when a pack is created. They show the only pack created that night, pack-366ba631, at **23:54:45** (9,101 objects). `packed-refs` was rewritten at 23:54:32, the signature of a `git gc`.
  - The four older packs hold 15,249 objects, below 2^14 = 16,384, so abbreviations were 7 characters. Adding 9,101 gives 24,350, so they became 8.
  - "Object count" is also wrong. The same 20,576 objects print 7-character hashes when loose and 8 when packed (my pass-2 clone). Your CHANGELOG correction says "packed-object count", which is right; the code comment says "object count". Both say 23:57.
- **F24 — UPHOLD.** The fix text is right.
- **F25 — OVERTURN "that field only" and the provenance. MEASURED** (`ctrlscan.py`, a history bisect).
  - Two more ledger fields hold two U+0008 characters each: citestale.state_note (since fe28fbc8) and fbsmlane.state_note (since 18ea5646).
  - lcaisalane's came in with **3c41f011**, not e0be9b2a: e0be9b2a's parent already has it.
  - Your fix itself verified clean: +2 bytes, only that field changed, 51,448 CRLFs unchanged, no trailing newline.
- **F26 — UPHOLD, LOW.** MEASURED: BRIEF_TEMPLATE.md:31–32 and CLAUDE.md:867 (both copies) still say the copies are under the root.
- **F27 — REFINE. MEASURED: its premise is false.** A `records_only()` that always returns False dies on Q0, and one that always returns True dies on Q3, Q4 and Q11. Only which object `git show h` resolves to is unpinned, which is F10(b).

**Disagreements**
- **D1 — UPHOLD the ruling; fix the reason and the proposed text.**
  - kimi's "fails loud" holds only for false negatives. A hex word that prefixes a commit's hash excuses the closure silently, in the old code and the new.
  - MEASURED: `names('éb78bb0f')` is True and `names('sha_b78bb0f')` is True. Your sentence must say "glued to an ASCII letter or digit".
- **D2 — UPHOLD.** One addition: the old exact comparison with git's short hash failed loud on an ambiguous token, because git lengthens the abbreviation for it. Prefix matching fails silent, which is why note 1 deserves the 0.1 s tripwire.
- **D3 — UPHOLD.**

## (2) Which of your dispositions is wrong

Every one that is wrong is a fix or a record written in answer to a finding. The findings held; the corrections picked up new errors.

1. **F25** is incomplete: two more ledger fields, and the same defect in live tool code (item (3)-1). Its provenance commit is also wrong.
2. **F23's fix** has the wrong time (23:57 instead of about 23:54) in both the code comment and the CHANGELOG, and "object count" in the code comment. Both errors came from my pass-2 finding.
3. **F10.** Part (b) was never corrected. Part (a)'s new comment has two problems:
   - "3 of the 60 scanned commits edit pipeline code" is mislabelled. MEASURED: 28 of the 60 touch `tools/pipeline/*.py|*.sh`. Three of them — 4653ecfb, e2e5a195, 7d7e0559 — count as records only because of that exemption.
   - "Changes no verdict today" is true at depth 60 and **false at full depth.** MEASURED with `q14.py` at depth 800: dropping the exemption gives 8 HARD and ATTRIBUTION_FAIL. The eight are 0a7c4687 (probewiringscope), 180afaa3 (verdictprose), 748c9daf, 86ea7c0e, 8b5fc437, **bbfc942e** (the comment's own example), c677764d and c8a483f5. Several look like genuinely shipped checker code, so attrcheckgaps is also a records backlog.
4. **F1:** 7 of 9, not 8 (my error). **F6:** the index, not HEAD. **F19:** a domain defect, not only a coverage gap. **F27:** its premise is refuted. **D1:** needs the ASCII qualifier.

On your section-4 question: fix every wrong record in #547, since they are all comment or text edits. Keep attrcheckgaps as the sink for the logic, but schedule it rather than park it. It already has its control set, and its full-depth list above is real drift.

## (3) What all nine of us missed

1. **The U+0008 defect is in live tool code.** In `tools/pipeline/seat_verdicts.py`, the wall detector's `\b429\b` (WALL_STRONG) and `\berror\b` (WALL_MARK) have held literal backspaces since 1cec2daf on 2026-08-27; d64a1fc3 had `\b429\b` correctly. MEASURED with `sv_wall.py`, comparing `_is_wall` as shipped against a copy with `\b` restored:

   | text | as shipped | with `\b` |
   |---|---|---|
   | `{"error":"rate limit exceeded for this model"}` | False | True |
   | `Error code: 429 - rate limited, retry later` | False | True |
   | `we saw 429 rows in the table` | False | True |

   The selftest has no case for either alternative, which is why it never noticed. Restoring `\b429\b` blindly would also flag the third line, a bare number the file's own rules forbid, so the fix needs a decision first. The same character also sits at line 3631 of both CLAUDE.md copies, in `matrix.html`, and in the two ledger fields above.
2. **One assertion closes both Lg5 and F11.** "NEVER NAMED < 135 rows-with-commits, and scanned == 60." MEASURED with `nevernamed.py`, the committed code passes it (114, 60). Lg5 fails it (135), and so does a run with `GIT_DIR=/nonexistent` (135, 0), even though all three print ATTRIBUTION_PASS.
3. **Committing #547 as a whole ledger file would sweep in other work.** MEASURED: the index and worktree ledgers differ in 10 rows: alphaifetchkill, alphavmkill, cxseatcheck, hygienecensus, lcabadval, lcaconfbus1kill, lcairqstubkill, lcaisalane, lcaisaphys, untrackeddetectors, plus the `updated` field. The packet accounts for lcaisalane only. Stage the ledger by hunk and check `git diff --cached` before committing.
4. **Two control gaps.** The reopened call site's hash argument is unpinned (Q16 above). Your closure control Q15 pins only the "in work" state, so a mutant excusing "held" rows (K4) survives everything. REASONED: running Q15 per non-closed state closes that.
5. **Where the recurrence comes from.** REASONED: the phrase "delete the kill" is carrier vocabulary (tools/CLAUDE.md:2879), and #513 copied it into src. That is the reason deletecheckhead's tripwire is worth having.
