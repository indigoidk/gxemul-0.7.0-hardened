<!-- the Opus 5 measuring seat's answer, extracted from its subagent transcript; model claude-opus-5-5; 2026-09-24T06:22:18.934Z -->
OPUS547_ALIVE_0924
# CHECKPOINT -- 2026-09-24 00:55 (087a90 sections rewritten; the peer's sections below are untouched)

VERDICT: U=SHIP WITH NOTES; R=SHIP WITH NOTES

Nothing was written under GXEMUL-SEC, est or the build trees. One early `git status --porcelain` may have refreshed the index's stat cache; after that I used `--no-optional-locks`. I read the ledger through a copy (GXLEDGER), as you told me to, but only the ids, states, commits and reopened fields. I did not read anything inside regress/artifacts/, so Q0–Q7 below are my rebuild from the brief's table. The full command list is in `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\opus547\COMMANDS.log`, and the scripts and outputs are in `...\opus547\r\`.

## U

**U-1 MEASURED — the premise holds, on the right domain.**
- HEAD export (`git archive HEAD src test | tar -x`), then `sh test/check_delete_calls.sh`: exit 1, "Error: src/devices/dev_sgi_re.c is not in check_delete_calls.exceptions!". Same result in git-bash (grep 3.0) and WSL Gentoo (grep 3.12).
- The same export with only `u.diff` applied: exit 0 in both shells.
- A copy of the working tree: exit 0.
- No other file at HEAD fails.

**U-2 MEASURED — four corrections to U1's premise.**
- **The check is a regex, not a substring test.** The exceptions test is an unanchored basic regex with `$a` unquoted, so `.` matches any character.
- **Two other files pass only by accident.** At HEAD, four src files contain "delete ": debugger.c, debugger_cmds.c, refcount_ptr.h and dev_sgi_re.c (`git grep -l "delete " HEAD -- src`). Only refcount_ptr.h is excused by its own entry.
  - `grep -n $a` shows debugger.c matching lines 2 **and** 3 of the exceptions list. Line 3 matches only because `.` matches `_` in `./src/debugger/debugger_cmds.cc`.
  - debugger_cmds.c matches the stale C++-era line `./src/debugger/debugger_cmds.cc`.
  - 8 of the 9 exception entries name files that do not exist in the tree.
  - Pristine upstream passes its own check by the same accident. The fork's de1398e1 (rounds 17–25) added two "delete " help strings to debugger_cmds.c that the check never saw.
- **Binary files are dropped by different routes.** Under WSL grep 3.12 the "binary file matches" notice goes to stderr, so `grep -v "inary file"` has nothing to filter. Under git-bash grep 3.0 the notice goes to stdout and the filter removes it.
- **The gate scans the dirty working tree, not HEAD.** Gate 8 runs `cd $SEC`, i.e. the working tree, which holds 224 ignored `.o` files plus generated files. `debugger.o` matches.
- Wording nit: "delete" is six characters; the matched string "delete " is seven, counting the space.

**U-3 MEASURED — option (b) is the wrong choice.**
- I looped over all 764 working-tree files under src. The line (b) would add excuses exactly one file, dev_sgi_re.c, and does so permanently.
- After (b), all 4 files that contain the string today would be excused, so the check could not fail on any of them.
- Both upstream files are byte-identical to pristine 2021 upstream and untouched since 39748e3c. Options (b) and (c) would be the fork's first edit to upstream's test, which undercuts gate 8's stated reason for existing.
- A fourth option you did not name, **(d)**: run gate 8's check on a HEAD export instead of the working tree. It complements (a); it does not replace it.

**U-4 MEASURED — house phrasing.** From `git grep -i` over src at HEAD:
- "drop(ping) the exit(1)/exit": 7 times, all in dev_sh4.c.
- "deleting exit(1)/the exit": 2 times (gdrom, luna88k). "deleting" does not trip the check.
- "delete the kill": 1 time, this line.
- "remove the kill" appears nowhere else. It is fine as written; "drop the exit(1)" is the most common idiom if you want house style.
- No probe or tool pins the wording.

**U-5 MEASURED — comment-only, confirmed without a compiler.**
- `strip_comments.py` on HEAD vs the working copy: only line 510 differs, and the comment-stripped text is identical (sha1 96f928f02e08 for both).
- The change is already propagated: `cmp` is identical in est, build, build-asan and /tmp/gxsec-build.
- `[ binary -nt source ]` holds in all three build trees.

**U-6 MEASURED — commit by path.** Plain `git diff --numstat` lists 24 modified tracked files, 7 of them under src/. "The only file" is true only of the diff scoped to dev_sgi_re.c. The index still holds the old line (`git grep --cached` lists dev_sgi_re.c).

**U-7 MEASURED (U3) — a precommit check is cheap, but only sound if it checks the index.**
- Cost: `git grep --cached` takes 0.05 s. A `checkout-index` export of src+test plus the unmodified upstream script takes 0.52 s and correctly exits 1 today.
- The working tree is the wrong thing to check: right now the working-tree copy exits 0 while the index and HEAD exit 1. A working-tree check would pass a commit whose tree fails. It would also block one unit on another unit's uncommitted text (the dev_sh4.c instance on 09-20). And running the script in the repo root writes `tmp_delete.out` there.
- Gate 8 has the same problem: if the battery ran now, it would report green over a failing HEAD.
- File both (precommit spot, gate 8 domain). This is a tooling change that owes its own controls, not this round's work.

**U-8 MEASURED — cadence does not explain the sixteen days.** `_scratchpad/nightly/` has no verdict for 09-06 or 09-13. The first battery after #513 (09-13, five days later) produced nothing. The weekly cadence accounts for five days; the missing battery accounts for a week, which is the dead-man switch's territory.

**U-9 REASONED (U4) — `none` is the honest witness term.** No compiled code shipped, and that is measured. `harness:` would claim the test apparatus was the subject, but the apparatus is unchanged and was right. The note should name the evidence (HEAD export exit 1, HEAD+U exit 0, comment-stripped identity) so it does not read as "nothing checkable".
- MEASURED: the worktree ledger has no row with id `upstreamdeleteprose` yet. It is only mentioned in stateaudit0923's note. Write the row in the U commit.

## R

**R-1 MEASURED — the fix is correct on all current data.**
- 0 HARD at depths 60, 130 and 795, at both 7- and 8-character abbreviations, on the worktree ledger and the HEAD/index ledger.
- `git cat-file --batch-check`: all 184 unique ledger tokens are unambiguous commits in HEAD's history.
- The brief's P0 (6 HARD) and P2 (11 HARD) reproduce.
- The pre-fix code at full depth gave 50 HARD. 49 are pure abbreviation artifacts: the row holds a true 7-character prefix of that commit. The 50th, b78bb0f6/pcc2widthkills, is now REOPENED as its field says. Nothing is over-credited.
- My rebuilt Q0–Q7 are green on the committed code, and {6,40} is killed only by Q7, which matches the brief's Q8/Q9.

**R-2 MEASURED (R2) — yes, such edits exist.** Command: `battery.py`, 40 mutants over the lines 3e33201d changed.
- **N11**, `SHA.findall(field or "")[:2]`, and **N10**, `SHA.findall((field or "")[:40])`, print output byte-identical to the committed code on all eight control inputs (`identity_on_controls.py`). No verifier over those inputs can see them.
- They flip the full-history verdict. At GXATTR_DEPTH=795 the committed code gives "ATTRIBUTION_PASS 0 hard".
  - N11 gives "ATTRIBUTION_FAIL 5 hard": 6014b7e7 selfmutant6, 7e3b1204 gate3scope, 9f666a8d sgireunmapped, and c43ce978 and eae8c8c2 gdromexitsix.
  - N10 gives 2 HARD. The result is the same on the HEAD ledger.
- Why the controls miss it: of 102 full-history attributions, the 8 that match a token at position 3 or later in a commits list all sit at depths 149–489. Within depth 130, no match uses anything past position 2, and no control scans past 130.

**R-3 MEASURED (R3) — the checker's first documented HARD rule is not pinned for ordinary rows.** That rule is "closure word in the subject, row not closed". Q7 is the only control that reaches it, and Q7's row has a `reopened` field; 580 of 582 rows do not.
- **C4**, `names(row.get("reopened") or row.get("commits"), full)`, is byte-identical on all eight controls.
- It brings back the defect the file's own "ORDER IS LOAD-BEARING" comment records. With fbdeclinefive set to "in work" (4264ee20's subject says "closed", and the row names 4264ee20), the committed code gives HARD "commit says CLOSED; row is 'in work'", while C4 gives REOPENED.
- **N7**, `SHA.findall(field or full)`, excuses every such row. At the default depth 60 it also removes 5 SOFT grades (21 attributed becomes 26). Only a golden-output verifier would see that; the brief's table asserts HARD counts.

**R-4 MEASURED — two cheap controls close all of the above.**
- **QFULL:** current ledger, GXATTR_DEPTH=100000, both abbreviation widths, expect 0 HARD.
- **QORD:** the fbdeclinefive-to-"in work" injection, expect HARD.
- The committed code passes both. Together they kill N4–N7, N10–N12, C2–C5, S2, Lg1 and Lg2.
- What survives both is equivalent on current data, except Lg5 (join subjects from the wrong unpacked field). Lg5 changes the NEVER NAMED line from 114 to 135, which shows up in the full output of every control.

**R-5 MEASURED (R1) — note 2's "recorded, not changed" is right, but not for the brief's reason.**
- The branch that reads `reopened` is entered exactly once in 795 commits (b78bb0f6). lcaisalane is closed, so its `reopened` field is never read.
- The seats' remedy is harmful if applied inside the shared `names()`. "Leading token only" (N5/N12) turns Q0 red, because stagetokens and wiringcliff are credited on their second commits token. If done at all, it must be applied at the `reopened` call site only (N8, which is equivalent on current data).
- "The old test saw it" was true only while `%h` was 7 characters. With direct calls: with an 8-character `%h`, the old substring test missed every 7-character form.

**R-6 MEASURED (R1) — note 3 is the weak disposition: the code should have changed, not just the comment.** `git show <abbrev>` resolves a ref with the same name before the object; git's "refname is ambiguous" warning goes to stderr, which `git()` discards.
- In a scratch clone with tag `030e961` pointing at fd150657, the committed code graded wdcaltdigin "open row, commits=599a7a8" instead of "records-only commit".
- `records_only(full)` graded it correctly and is equivalent on all current data. Low severity; a one-token follow-up or a filing.

**R-7 MEASURED — wrong record (L4): "six correctly attributed rows" is five rows.** P0's six HARD lines cover five rows; stagetokens fails twice (09ded75c and 686d179c). The same holds at the pre-fix HEAD, where the window is positions 2–61 and the next HARD is at 96. Correct it in place in the committed comment near line 146 and in brief §4.

**R-8 MEASURED — what actually lengthened `%h`.** The abbreviation length is set by how many objects are packed, not by history.
- In a fresh scratch clone, 20,576 packed objects print 8 characters. After `unpack-objects` leaves them all loose, the same 795 commits print 7.
- This repo has 24,350 packed objects (at least 2^14, hence 8), and three packs are stamped 23:57, seven minutes after 4264ee20. So "after 4264ee20" was a repack, not the commit. The pre-fix verdict depended on local gc state; the fix is immune to that.

**R-9 MEASURED — found something else (pre-existing): the check passes when git cannot read the repo.**
- `GIT_DIR=/nonexistent python .../check_commit_attribution.py` exits 0 with "scanned 0 commits deep … ATTRIBUTION_PASS 0 hard, 0 soft". Section L greps only for ATTRIBUTION_PASS.
- The sibling check_checkpoint.py refuses this case (CHECKPOINT_NO_GIT).
- A one-line "scanned too few commits" guard would fix it. File it. A WSL run reads the repo fine, so I found no live trigger.

**R-10 MEASURED — found something else: a ledger text defect.** lcaisalane's `reopened` field contains two U+0008 backspace characters where `\b(closing)\b` was meant. JSON decodes `\b` as backspace. The field is inert because the row is closed; it needs a records fix.

**Also found (MEASURED):**
- The brief's "three pristine copies under the project root" is out of date. They moved on 2026-09-13 to `C:\DocumentNoSnc\CC\GXEMUL_upstream_2021\`.
- The MOVED.txt notes contain a literal CR and BEL where `\r` and `\a` in the path were meant, so the paths they give are wrong.
- A directory literally named `GXEMUL-SEC\r`, with a trailing carriage return, sits at the project root and holds one file, INSTRUMENT.md5.

I deleted every source-tree copy and the scratch clone I made, so no new stray `src/` copies are left under the project root.
