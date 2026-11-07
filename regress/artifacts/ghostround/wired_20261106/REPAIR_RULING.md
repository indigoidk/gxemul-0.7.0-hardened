FABLEGHOSTREP: 24 ACCEPTED 5 AMENDED 1 REJECTED VERDICT:HOLD -- the `--at` blame site is a clause-(b) breach no leg sees (real-git trigger measured), two passes found one fail-open class, so the class closes in ONE diff (a completeness guard, four legs, a counting harness, a driver fix) plus four wrong records; the FINAL run is owed again regardless

# RULING -- the REPAIR of `#587` ghostround (check_ghost_rounds.py + precommit section P2), pass 2 of the repair, Fable 5.1, 2026-11-07

**Subject.** The repaired unit at `_scratchpad/wghost/landing/staged_final/` (staged bytes dated 2026-11-07, on HEAD `8d9df658`),
its bank `regress/artifacts/ghostround/wired_20261106/` (54 legs, 8 mutants, 72 equivalence cells), and the two pass-2 reviews:
GPT-6 Astra (`pass2_seats/codex_GHOSTREPAIR_ASTRA.txt`, 7,296 B, a real answer; the 253 KB `.err` is its stderr stream) and
Grok 4.7 (`pass2_seats/grok_ghostrepair.txt`, 8,749 B).  My earlier ruling (`fable_20261106/ghost/RULING.md`, HOLD) is the
pass this repair answers.  Line numbers are the STAGED files' unless marked otherwise.

**What I did (all read-only; `git status --porcelain` 953 lines before and after; scratch files only in the session scratchpad
and `%TEMP%`).**
1. Read the staged checker (484 lines), P2 at hook `:242-275` and the helpers `:33-45`, `run_mutants.sh`, the `--at` legs and
   `ctl()` of `run_checker_controls.sh`, `MUTANTS.out`, `CHECKER_CONTROLS.out`, `SYNTHETIC_BLOCK.md`, `commit_ghost.msg`,
   CHANGELOG `:38-53`, bug file `:26780`, ledger `:28938`, PRETEST.md `:85-100` and `:155-166`, the driver's `:59-61`.
2. **Ran the staged checker in memory** (index mode, `git_show` and `blame_contents` mocked, nothing written): blame rc 0 with an
   EMPTY map -> `GHOST_ROUNDS_PASS 1 archived`; rc 0 with the header line omitted -> PASS; a complete map (all-zero -> TODAY)
   -> `GHOST_ROUNDS_FAIL`; `None` -> `GHOST_ROUNDS_VOID`.  Astra's demonstration reproduces exactly.
3. **Measured real git on GXEMUL-SEC** (object format `sha1`, git 2.45.1): `git show 'HEAD^{tree}:CHANGELOG.md'` rc 0 while
   `git blame --porcelain 'HEAD^{tree}' -- CHANGELOG.md` rc 128 `fatal: Non commit HEAD^{tree}?` -- a real trigger for
   `blame_rev` failing where `git_show` succeeds.  The full porcelain blame of CHANGELOG.md at HEAD (38,716 lines, 0.66 s):
   **38,716 header lines, 38,716 distinct final lines, 0 gaps, 408 shas, 408 with `committer-time`, 0 missing**; the
   `--contents` form (what index mode runs) identical; one line prepended -> that line is the all-zero sha.  `git init -h`
   lists `--object-format`.
4. **Replayed the c5 census legs at `2632277f` under M3 and M6 in memory, against the real repo**: baseline 13 / 184 / 268;
   M6 13 / **162** / **263**; M3 **12** / **161** / 268.  Astra's four numbers reproduce.
5. One apparatus error of mine, recorded because it is the carrier's class: my first porcelain analysis piped blame into
   `python - <<EOF`, and the heredoc replaced the pipe, so it read ZERO bytes and reported 0 lines; the 0.058 s runtime was
   the tell.  Re-run from a script file.

## 1. The disputed cell, settled by the code

`parse_blocks` `:284-295`: `bdate, bsha = blame.get(ln, ("", ""))` ... `landed = bdate or (date if src == "header" else UNDATED)`.
`blame_rev` `:243` and `blame_contents` `:256` return `None` ONLY on `rc != 0`; `load()` `:398`/`:408` turns `None` into VOID.
A blame that exits 0 but whose map lacks the block's header line gives `bdate == ""`, and a dated header then supplies `landed`
-- the fallback written for file mode (`blame_file` `{}`, `:263/:265`) and `--no-git` (`:397/:407`), reached in index/`--at`
mode with no guard.  `porcelain_dates` can omit a line in two ways: a header line the regex `^([0-9a-f]{40}) \d+ (\d+)` does not
match (`:217` -- every line of a 64-hex SHA-256 repo), or a sha with no `committer-time` (`:231-232`, `continue`).

**Both seats read the code right.**  Astra: the path exists and PASSes (reproduced, item 2).  Grok: "the code path is fail-open;
the git trigger is not shown" -- and item 3 now measures the trigger NEGATIVE on this repo: real porcelain attributes every
line and every sha carries `committer-time`, in both forms the checker uses.  The only writer that reaches the cell is a
non-SHA-1 object format, which GXEMUL-SEC cannot become.

**Ruling: not a measured floor breach at the production site (the cell's writer cannot produce it here), but a MEMBER OF THE
CLASS this chain has now found on two consecutive passes -- a degraded read silently taking a weaker source -- and the class
closure (section 4) closes it in the same diff, because the guard is two lines and has a REAL-GIT leg (a
`git init --object-format=sha256` scratch repo makes the map empty with rc 0).**  Astra's grade "code defect" is AMENDED to
"class cell, closed by construction"; Grok's "not counted" is AMENDED to "counted, in the class".

## 2. Every finding, ACCEPT / AMEND / REJECT

### 2a. GPT-6 Astra (14 ACCEPT, 3 AMEND, 0 REJECT)

| # | finding | ruling | decided by |
|---|---|---|---|
| A1 | incomplete successful blame -> header fallback -> PASS (code defect) | **AMEND** -- path TRUE and reproduced; reachability measured negative on this repo; closed as a class cell (s.1, s.4) | items 2-3 |
| A2 | `run_mutants.sh` ignores `mutate()`'s status; a stale `$WORK/<name>.check_ghost_rounds.py` would be re-scored | **ACCEPT** -- `leg()` `:46-50`: `mutate` is called, its rc dropped, then `[ -f "$ch" ]`.  Latent: `MUTANTS.out` carries no `MUTANT TEXT FOUND` line, so the banked run applied every edit.  L1, one line (s.4 item 6) | read |
| A3 | QR1: TRUE for rc != 0 -> VOID; FALSE that it exhausts fail-open; malformed JSON = uncaught `JSONDecodeError` = hard FAIL in P2, not fail-open | **ACCEPT** -- `json.loads` `:400/:411` sits outside any `except`; a traceback is rc 1 with no token -> P2 `else` `:272-273` `bad` | read |
| A4 | QR2 TRUE: P2 cannot select file mode (`env -u` the two names, no `--worktree`, no message argument forwarded) | **ACCEPT** -- `load()` `:402`; hook `:266` | read |
| A5 | QR3 TRUE: c8i pins the branch (`no such ref: HEAD`); it does not cover failed revision-mode blame or incomplete output | **ACCEPT** -- and the second half is the breach at A9 | read |
| A6 | QR4 FALSE as full-hook equivalence: the stubs omit the `fail` counter and exit behaviour | **ACCEPT** -- harness stubs `run_checker_controls.sh` (brief 4.8 `:417-426`): `bad` is a `printf`; hook `:37` increments `fail` | read |
| A7 | QR5 TRUE; M1 also reds c9b because the same-day fixture passes under `--rule=date` | **ACCEPT** -- `SAMEDAY` row carries only an entry dated the block's day; c9b runs the same block under M1's hook | read; MUTANTS.out |
| A8 | smallest escaping edit: `(bad "...")` in a subshell -- `fail` not incremented, c9a/c9b stay green (stub prints HOOK-FAIL), a sole P2 failure ends `PRECOMMIT_PASS` | **ACCEPT** as a hook-level coverage escape.  The RED pretest run (`PRECOMMIT_FAIL 1 hard`) does catch it, but the mutant table cannot; the harness owes a counting `bad` (s.4 item 5) | read |
| A9 | one-token escape: `blame_rev()` `else None` -> `else {}`; every `--at` leg uses a successful blame | **AMEND -- grade UP to L2.**  Clause (b) demands the detector fail on a verbatim reinstatement at EVERY fixed site; `:243` is a fixed site (repair hunk `@@ -231 +243`) and the only legs that reach `blame_rev` are c4a-c, c5 x3, c7a-b, all on real commits where blame succeeds -- so the mutated branch is never taken: 54/54 by construction, not by prediction.  The real-git trigger exists (item 3: `--at=HEAD^{tree}`).  The checker's own `:44-45` CLAIMS `--at` "is VOID on the same failures" with nothing pinning it | item 3; run_checker_controls.sh `:78-112` |
| A10 | records: "five ... that every control passed" is false -- M3 and M6 red the old c5 counts (12/161; 162/263) | **ACCEPT, MEASURED HERE** (item 4).  L4 at CHANGELOG `:41-42`, bug file `:26780` ("five uncaught one-line mutants"), and in MY OWN `PASS2_RULING.md` §A3 (M3, M6 "ACCEPT by reading") and §B ("traced past every control") -- I rejected agy's M4 for predicting real-file counts and then predicted them myself for M3 and M6.  The banked table already showed it (`M3 ... c5_HEAD_all c5_HEAD_subject`, `M6 ... c5_HEAD_all c5_HEAD_date_all`) and nobody read the record against it | item 4; MUTANTS.out |
| A11 | ledger `:28938` "each one-line mutant ... 8 of 8" counts seven one-line mutants plus PRE, a whole-checker replacement | **AMEND -- ACCEPT and add a site**: `commit_ghost.msg:21-22` "the one-line mutants the review traced, each killed by its leg, 8 of 8" is the same conflation; CHANGELOG `:52-53` has it right ("Every one-line mutant ... and the code before the repair") | read |
| A12 | PRETEST.md `:92-93` names `#586`/`bugfilereverse`; the bank's RED is `#587`/`codeqlscope` | **ACCEPT** (L4, kit file) -- `SYNTHETIC_BLOCK.md` reads `#587 ... codeqlscope` | read |
| A13 | PRETEST.md `:96` describes a `wired/run_x_control.sh` step | **ACCEPT** (L4, kit) -- absent from the staged bank; CHANGELOG hunk 4.5 removed the X_CONTROL sentences | `ls` |
| A14 | PRETEST.md `:161-162` says the driver reads its own bytes at END | **ACCEPT** (L4, kit) -- `pretest_ghost.final-20261107_031240.py:59-61`: "read now, at start, never at the end -- the first banked run read its file at the end"; the lines describe round 1's defect as current | read |
| A15 | option-set members missing: attribution-completeness validation; failed revision-blame coverage; assertions on the hook's accumulated failure state; propagation of mutant-construction failure | **ACCEPT** -- all four land in the closure diff | s.4 |
| A16 | zero controls that cannot fail; the gaps are coverage, not tautology | **ACCEPT** -- same as my last ruling on "5 controls that cannot fail" | |
| A17 | denominator 54 = 8+6+4+9+3+2+5+13+4; 15 warn / 5 bad; 72; 35 manifest; 26 identities | **ACCEPT** -- 54 recounted from `CHECKER_CONTROLS.out` (s8 = 5+1+1+1+3+2 = 13); 15/5 and 72 from my earlier ruling and `EQUIV.out`; manifest and identities not re-counted here | |

### 2b. Grok 4.7 (10 ACCEPT, 2 AMEND, 1 REJECT)

| # | finding | ruling | decided by |
|---|---|---|---|
| G1 | QR1 TRUE for a short map; JSON is a crash the hook hard-fails; "the git trigger is not shown" | **ACCEPT** -- and now measured negative for this repo (item 3) | |
| G2 | QR2 **FALSE** | **AMEND -- polarity only.**  Its substance (P2 never enters file mode; `GXROOT` is not a mode switch) is correct and is Astra's TRUE.  The same QP6 talking-past as last pass | read |
| G3 | QR3 TRUE; reverting the branch still reds c8i (`w_PRE/.../c8i` PASS dated `header`) | **ACCEPT** | MUTANTS.out |
| G4 | QR4 TRUE on the current 14 lines, with caveats: no `set -u` in the harness; `awk` stops at the first bare `fi`; `p2_block_cut` only checks `GHOSTCHK` present and last line `fi` | **ACCEPT** -- the harness tweak in s.4 item 5 adds `set -u`; the cut is sound for the staged block (`:262-275`, 14 lines) | read |
| G5 | QR5 **FALSE**: each kill is the mutated predicate; M5's third BAD is c8h's `absent` line; PRE is 4 lines over two names | **AMEND -- polarity only**; the table is right and matches Astra's | MUTANTS.out |
| G6 | floor edit 1: `env -u GIT_INDEX_FILE env -u GXLEDGER ...` in P2 -- the hook drops the temporary index of `commit -a`/partial commits; c8g is checker-level; c9a-c stage into the real index; M7's find-text survives | **ACCEPT** -- escapes all 54 AND the GREEN/RED pretest (both `git add` into the real index).  This is the de-escalation ACCEPT ROW for the env-clearing predicate: the names NOT cleared must still land, and `GIT_INDEX_FILE` is the load-bearing one.  Owed: c9d (s.4 item 4) | read |
| G7 | floor edit 2: an `elif ... GHOST_ROUNDS_VOID -> good` before the FAIL branch; c8h/c8i never run the hook; c9c's stub prints neither token | **ACCEPT** -- escapes all 54; GREEN/RED never produce VOID.  CLAIM -> ROW: hook `:253` ADDS "it is VOID -- a hard FAIL below" and no row observes the hook on VOID.  Owed: c9e (s.4 item 4) | read |
| G8 | option set: "the hook must KEEP `GIT_INDEX_FILE`" is unnamed and load-bearing | **ACCEPT** (= G6) | |
| G9 | verdict line: "2 CONTROLS THAT CANNOT FAIL" | **REJECT the label** -- the body names no control that returns the same answer in both states; G6/G7 are coverage GAPS (accepted as such).  A gap and a check-that-cannot-fail are different defects with different repairs | read |
| G10 | ledger witness "8 of 8" | **ACCEPT** (= A11) | |
| G11 | counted and true: 15/5 at `8d9df658`; 54 call sites; 35 + 5 index legs; `EQUIV: 72 ... 0 DIFFERENT`; `HEADER_REDATE.out`; the regress hold and `hold_question` intact; bracket and `#587` section say `dropped`; the 2026-11-06 bullet stays as the dated record | **ACCEPT** | |
| G12 | the brief's "Not checked gains the header re-dating and the H2 block" is half true of the bug file (H2 only; re-dating is in the FIXED sentence) | **ACCEPT as an observation about the BRIEF**; no sentence in the unit is false by it; nothing owed | read |
| G13 | "as section Q2 does" is the `env -u` form, not the token rule | **ACCEPT** -- CHANGELOG `:28` scopes the comparison to the clearing; hook `:587` is `env -u GXDOMAIN_BASELINE -u GXLEDGER` | read |

**Not re-derived by either seat and not by me:** the 141 / 11 / 20 replay arithmetic (accepted last pass against
`replay_class.out`).

## 3. The repair-chain stop rule, applied

This is the second pass on this checker.  **Pass 1 found** a failed `git show` reading the working copies (D3) and a failed blame
trusting the header dates (D4).  **Pass 2 finds** the `--at` blame site reinstatable with no leg (A9), a successful-but-incomplete
blame trusting the header dates (A1), the hook passing a degraded VERDICT (G7) and a degraded ENVIRONMENT (G6), and the hook's
effect pinned by branching only (A8).  **One class, two passes: a degraded read, dating or verdict silently taking a weaker
source.**  By the amendment, the next repair owes the CLASS CLOSURE -- the space enumerated from the function's own inputs,
every cell closed in ONE diff, the contract naming which cells are covered and which are deliberately not -- and the closing pass
then VERIFIES THE ENUMERATION rather than hunting cells.

## 4. VERDICT: **HOLD** -- the class closure, in one diff

**The space, from `load()`'s and P2's own inputs.**  Checker: mode in {`--at`, index, file}; `--no-git`; `git show` (ledger,
CHANGELOG) in {ok, fail}; blame in {rc != 0, rc 0 complete, rc 0 incomplete}; ledger in {parses, malformed}.  Hook: the checker's
outcome in {rc 0 + PASS, rc 0 no token, rc 1 + FAIL, rc 2 + VOID, crash}; environment in {GX* set, `GIT_INDEX_FILE` set}; effect in
{branch taken, `fail` counted}.

| cell | staged behaviour | pinned by | owed |
|---|---|---|---|
| `--at`: show fails | VOID `:395-396` (pre-repair: `SystemExit` rc 1 -- never fail-open) | nothing | disclose only |
| **`--at`: blame rc != 0** | VOID `:398-399` | **NOTHING** | **leg c4d (item 1); L2** |
| **`--at` / index: blame rc 0, map incomplete** | header date `:295` -- OPEN | nothing | **guard (item 2) + leg c8j; class cell** |
| `--at` / index: ledger malformed | `JSONDecodeError` traceback, rc 1 -> P2 `else` hard FAIL | nothing | disclose (VOID wrapper optional, not owed) |
| index: show fails | VOID `:404-406` | c8h | -- |
| index: blame rc != 0 | VOID `:408-410` | c8i (also kills a one-token `{}` at `:256`, by reading) | -- |
| `--no-git`; file mode outside a repo or blame failing | header dates BY DESIGN `:45-47`, `:263-265` | c1, c2, c6 | disclosed already |
| hook: rc 0 + PASS / rc 0 no token / rc 1 + FAIL | good / bad / bad | GREEN / c9c / c9a + RED | -- |
| **hook: rc 2 + VOID** | bad (`else` `:272`) | **NOTHING at hook level** | **leg c9e (item 4)** |
| hook: crash | bad (same `else`) | c9c covers "no token" | disclose |
| hook: GX* set | cleared `:266` | c9b | -- |
| **hook: `GIT_INDEX_FILE` set, block only in the temp index** | passes through -> FAIL | **NOTHING at hook level** (c8g is checker-level) | **leg c9d (item 4)** |
| **hook: `fail` counted** | `bad` increments `:37` | RED run only; the mutant table cannot see it | **harness counts (item 5)** |

**Owed, each in its smallest form, with the control or mutant it needs:**

| # | owed | grade | the change |
|---|---|---|---|
| 1 | **Leg c4d_at_tree_blame_VOID** | **L2** (clause (b) at fixed site `:243`) | `CTL_ENV="GXSEC=$SEC" CTL_ARGS="--at=HEAD^{tree}"` (or the tree sha) -> want rc 2, `GHOST_ROUNDS_VOID`, must-contain `git blame`; `absent ... GHOST_ROUNDS_PASS`; `absent ... GHOST_ROUNDS_FAIL`.  Mutant **M9**: `blame_rev`'s `else None` -> `else {}` -- the find-text must be the TWO lines `git(["blame", "--porcelain", rev, "--", CHANGELOG_REL])` + `return ... else None`, because the one-line form occurs twice and the driver's one-occurrence rule refuses it.  Expected: c4d BAD, every other leg ok. |
| 2 | **Completeness guard** in `load()`, index and `--at` modes | L1 (class cell) | After each `bl = ... blame_*(...)`, `if bl is None or len(bl) != nlines(cb): raise Void("git blame dated %d of %d lines of %s ..." )` where `nlines(b) = b.count(b"\n") + (0 if b.endswith(b"\n") or not b else 1)`.  **Leg c8j_blame_incomplete_VOID**: a scratch repo `git init --object-format=sha256`, CHANGELOG and synth ledger committed, a block with header `(2026-11-01)` staged -> want rc 2, VOID, must-contain `dated 0 of`; `absent PASS`.  Pre-guard it PASSes (header archived).  Mutant **M10**: delete the `len(bl) != ...` clause -> c8j BAD.  Contract line: "a repository whose object format is not SHA-1 is VOID -- the porcelain parser reads 40-hex shas". |
| 3 | **Docstring / hook-comment contract** | L1 | Write the table's dispositions into the checker's docstring (`:38-48`) and P2's comment: VOID cells; by-design header dating (file, `--no-git`); malformed JSON = a traceback the hook hard-fails; hook: VOID, crash and no-token are hard FAIL; `GIT_INDEX_FILE` passes through. |
| 4 | **Hook-level legs c9d and c9e** | L3-shaped (accept row; CLAIM -> ROW) | **c9d_hook_tempindex_FAIL**: c8g's setup (`.git/index.ghost`, block added only there), then `CTL_ENV="GIT_INDEX_FILE=$RW/.git/index.ghost" hookctl c9d_hook_tempindex_FAIL FAIL "GHOST    ghostopen"`.  Mutant **M11** (Grok's): `env -u GXLEDGER` -> `env -u GIT_INDEX_FILE -u GXLEDGER` in the hook -> c9d BAD.  **c9e_hook_void_FAIL**: c8h's setup (`.git/index.bogus`), `CTL_ENV="GIT_INDEX_FILE=$RW/.git/index.bogus" hookctl c9e_hook_void_FAIL FAIL "reached no verdict"`.  Mutant **M12** (Grok's): insert `elif printf '%s' "$out" \| grep -q '^GHOST_ROUNDS_VOID'; then good "void"` before the FAIL `elif` -> c9e BAD. |
| 5 | **The harness counts** | L1 | `p2_harness.sh`: `set -u`; `fail=0`; `bad () { fail=$((fail+1)); printf "HOOK-FAIL  %s\n" "$*"; }`; after `. "$2"` print `HOOK-fail=$fail`.  Every `hookctl ... FAIL` leg adds must-contain `HOOK-fail=1`.  Mutant **M13** (Astra's): `bad "A ROUND BLOCK'S ROWS ..."` -> `(bad "...")` -> c9a, c9b, c9d BAD on `HOOK-fail=0`. |
| 6 | **`run_mutants.sh`** | L1 | In `leg()`: `rm -f "$WORK/$name.check_ghost_rounds.py" "$WORK/$name.hook.sh"` before `mutate`, and `mutate ... \|\| { e=$((e+1)); n=$((n+1)); echo "$name  NOT BUILT: mutant text"; return; }`.  Negative control: a deliberately wrong find-text must print NOT BUILT and end `exited nonzero`. |
| 7 | **Records** | L4 | (a) CHANGELOG `:41-42` "five one-line mutants of predicates the rule depends on that every control passed" -> "five one-line mutants ... traced past the controls BY READING (`PASS2_RULING.md` §A3 -- a reading this table then corrected): M3 (12/161 against 13/184) and M6 (162/263 against 184/268) were already red on the census count legs c5; M1, M2 and M5 passed every earlier leg and the GREEN/RED runs".  (b) bug file `:26780` "five uncaught one-line mutants" -> "five one-line mutants traced by reading, three of them (M1, M2, M5) caught by no earlier control".  (c) ledger `:28938` and (d) `commit_ghost.msg:21-22` -> "the seven one-line mutants and the pre-repair checker, each killed by its leg, 8 of 8".  (e) PRETEST.md `:92-93` (`#587`, `codeqlscope`), `:96` (drop the `run_x_control.sh` step or mark it round 1's), `:161-162` ("at its START").  (f) `PASS2_RULING.md` is a banked dated artifact: not edited; (a) names it as the source.  The CHANGELOG block also carries THIS pass: the class, the table, the five new legs and five new mutants with their measured scores. |
| 8 | **Rebuild, FINAL, and one more pass 2** | procedure / rule | The bank regenerates (checker md5, `CHECKER_CONTROLS.out` 54 -> 59 legs, `MUTANTS.out` 8 -> 13 mutants); GREEN and RED re-run.  Then ONE pass on the closure diff, scoped to **verify the enumeration above** -- every row of the table has a leg or a disclosure, every new leg a measured kill -- with the diff delivered (hunks > 0, printed and refused at zero), the roster named per the seat ledger, and the zero carried with its denominator.  It closes on zero breaches surviving adjudication. |

**Timing, stated and not weighed.**  The staged bytes are dated 2026-11-07 and the FINAL run is owed again whatever this ruling
said, because items 1-6 change the checker, the hook's bank and the driver.  If the landing crosses midnight the date fills move
(the `CALENDAR.json` comparison covers that) and PRETEST.md's dependency 2 (the four Alpha/LCA exemptions) returns.  None of
that moves the verdict: a clause-(b) site with no leg is L2 whatever the calendar says.

**FILED, not owed (clause (e), each disclosed or a design alternative):** a `Void` wrapper on malformed JSON (a hard FAIL already);
widening the porcelain regex to 64-hex (correctness on SHA-256 repos -- an owner question, since it would REMOVE c8j's trigger
and the guard would then need a synthetic one); Grok's `p2_block_cut` strengthening beyond `set -u` (an inserted bare `fi`
sources a different program -- true, and the 14-line count printed beside the cut is the tell); the hook forwarding its message
argument (not P2's concern).

**Seat ledger for this stage.**  GPT-6 Astra and Grok 4.7 ANSWERED -- real content, verdict line first, no wall or quota text,
both with denominators.  No agy, Opus or Ollama seat was fired for this pass (the owner's roster for the repair: Astra and Grok,
then Fable); none is counted as agreement.  This ruling is the Fable 5.1 seat.  **Where the two disagreed (A1 vs G1) neither was
wrong about the code; the difference was the grade, and item 3's measurement is what settled it.**  Count the arguments, not the
seats: Grok's two escapes and Astra's two were four DIFFERENT cells of one class, which is itself the evidence that the class, not
the instance, is what the next diff must close.

FABLEGHOSTREP: 24 ACCEPTED 5 AMENDED 1 REJECTED VERDICT:HOLD -- the `--at` blame site is a clause-(b) breach no leg sees (real-git trigger measured), two passes found one fail-open class, so the class closes in ONE diff (a completeness guard, four legs, a counting harness, a driver fix) plus four wrong records; the FINAL run is owed again regardless
