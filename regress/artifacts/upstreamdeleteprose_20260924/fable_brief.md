# FLAGSHIP SEAT, FIRED LAST -- `#547`: upstreamdeleteprose (U) and the follow-up repair R' to `#546`'s attribution rider

**Liveness first:** open your answer with the token `FABLE547_ALIVE` and the first line of
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\CHECKPOINT.md`, verbatim.

You are the ninth seat and the last.  Every other seat -- codex (GPT-6 Astra, max), agy, grok 4.7 xhigh, the kimi seat
through `kimi-k3:cloud` (its CLI is on a weekly limit), glm, deepseek, minimax, the Opus measuring seat, and a dedicated
second codex job each time -- has answered THREE passes: pass 2, the SF2 adjudication pass, and the repair chain's pass on
R'.  You hold two hats: this round's ninth review seat, and the final adjudication of everyone's findings and my
dispositions.  **Be hardest on the rulings that went my way, and on any that adopted a seat's own position.**

The tree under review is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\` (ignore any other `src/`).  READ-ONLY: write nothing
under GXEMUL-SEC, est or the build trees, stage nothing, run no gates or builds.  Where a claim is checkable in under two
minutes, measure it -- in memory, or under `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fable547\` only.

## READ, IN THIS ORDER (all paths under `GXEMUL-SEC\regress\artifacts\`)

1. `upstreamdeleteprose_20260924\rp_brief.md` -- R' and the records as the last pass saw them (diffs inlined).  Since
   then: seven more COMMENT corrections in `tools/pipeline/check_commit_attribution.py` (docstring SOFT paragraph and
   branch order; "never a hard failure"; "cached by the caller"; the regress/artifacts/ exemption; "8 HARD ... is a
   reading"; "consistent with a `git gc`"; the floor inside non-repo notes) -- its AST is unchanged apart from docstrings
   and its output is byte-identical to the golden Q0 -- and three more in-place edits to `#546`'s CHANGELOG block.  Read
   the working diffs directly: `git -C GXEMUL-SEC diff -- tools/pipeline/check_commit_attribution.py CHANGELOG.md
   src/devices/dev_sgi_re.c`.
2. The answers: `upstreamdeleteprose_20260924\panels\panel_20260924_004832\` (pass 2), `...\panel_20260924_012856\`
   (SF2), `...\panel_20260924_020050\` (R' pass), `...\panels\codex_dedicated_{pass2,f2,rp}.txt`, and the Opus seat's
   `upstreamdeleteprose_20260924\opus5_{pass2,f2,rp}.md`.  The rider's two pre-commit reviews:
   `hygienecensus_20260923\attrabbrev_20260924\{codex_rider.txt,grok_rider.txt}`.  (For codex.txt, the answer is the text
   after the LAST line reading `tokens used`.)
3. The measurements: `hygienecensus_20260923\attrabbrev_20260924\RESULT.txt`, and beside it every `PREDICTIONS_*.txt`
   (each sealed before its run), `controls_*.sh`, `verify_*.sh` and `VERIFY_*.out` (each verifier has a negative control).
   U's evidence: `upstreamdeleteprose_20260924\` (`gate8_HEAD_export.out`, `gate8_working.out`, `cpp_both.out`,
   `battery_*`).

## MY SUMMARY -- a claim to check, not evidence

* **U** changes one word of a comment in `src/devices/dev_sgi_re.c` ("delete the kill" -> "remove the kill").  Upstream's
  `test/check_delete_calls.sh` (gate 8's delete row) exits 1 on a `git archive` of HEAD and 0 with U; preprocessed text and
  objects are byte-identical.  Every seat, every pass: SHIP or SHIP WITH NOTES.  Witness `none -- comment-only`.
* **R** (committed, 3e33201d) made section L match ledger shas by prefix of `%H` instead of exact `%h` comparison.  The
  review found, besides many wrong sentences of mine, one regression R introduced (a non-repo note that MENTIONS a sha was
  credited as authorship -- codex, SF2) and two fail-open or shadowing paths it inherited (`git()` dropped its exit
  status; `git show <abbrev>` resolves a same-named ref first).
* **R'** (uncommitted): `lists()` reads `commits` as whole tokens; `git()` fails closed (exit 2, a HARD-shaped line);
  `records_only()` takes `%H`.  On 19 earlier inputs its output is byte-identical to HEAD's; Q19a/Q20/Q21b separate the
  three repairs.  In the R' pass no seat found a defect in R' on current data.  Two codex jobs said DO NOT SHIP -- one on a
  guard variant (`returncode != 0 and not r.stdout`) the controls could not see, now separated by Q23; one on a 6-character
  token inside a non-repo note under `core.abbrev=6`, which Q22 pins as a DELIBERATE narrowing (the pre-R checker fails 7
  HARD at that width anyway).  The Opus seat's default-value survivors are separated by Q24 (the checker run exactly as
  section L runs it), and exit codes by Q25.
* **My rulings you should test hardest:** (a) R' needs no further CODE change, so the repair chain closes on the R' pass;
  (b) the two DO NOT SHIP verdicts are control gaps and a deliberate narrowing, not breaches; (c) the ledger-token
  uniqueness tripwire, the `tools/pipeline/` exemption, the cp1252 decode crash (fail-closed), `GXATTR_DEPTH=0`, `--all`,
  `pass2_ledger.tsv` and the rest are FILED (`attrcheckgaps`, MED), not fixed -- deepseek asked HIGH, kimi asked to build the
  tripwire now; (d) `seat_verdicts.py`'s U+0008 wall patterns are FILED (`svbackspace`, MED), since fixing them needs a
  decision about bare numbers; (e) D1: `reopened` keeps the shared extractor, with codex's exact wording in a comment.
* **To file with #547:** `attrcheckgaps` (MED), `deletecheckhead` (MED: an INDEX-scoped precommit tripwire, and gate 8's
  domain), `batterymissedruns` (MED: no verdict for 2026-09-06 and 09-13; nothing runs the dead-man switch), `svbackspace`
  (MED), `carrierstalecopies` (LOW: stale pristine-copy location in the carrier and template, CR/BEL in MOVED.txt, a
  `GXEMUL-SEC`+CR directory at the root, U+0008 in the carrier).
* **The commit:** U + R' + the records (CHANGELOG `#547` block, the `#546` corrections, the ledger: `hygienecensus.commits`,
  the three U+0008 fixes, new rows `upstreamdeleteprose` and `attrabbrev`, the five filings) -- ledger and matrix as
  HEAD-based blobs, so the peer session's uncommitted rows stay out; staged by path.

## QUESTIONS

1. **VERDICT, first line:** `VERDICT: U=<SHIP|SHIP WITH NOTES|DO NOT SHIP>; R'=<...>; RECORDS=<...>`.
2. **Which of my dispositions is WRONG?**  Name the count you checked.  Include the rulings that adopted a seat's view.
3. **Is the repair chain CLOSED on the R' pass** under the carrier's stop condition -- a VALID pass (diff delivered,
   roster complete or its misses named), zero breaches SURVIVING ADJUDICATION, and a denominator?  If not, what is owed.
4. **The filings:** right rows, right severities, anything mis-sunk (owed now rather than filed), anything missing?
5. **What did all of us miss?**
