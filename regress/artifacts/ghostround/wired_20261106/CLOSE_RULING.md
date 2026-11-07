FABLEGHOSTCLOSE: 15 ACCEPTED 2 AMENDED 1 REJECTED VERDICT:HOLD -- the index guard tests its two reads separately (`lb is None or cb is None`), so "show fails" is a {ok,fail} x {ok,fail} product and my ruling's table rowed it as ONE cell; the two mixed cells are reachable with one `git rm --cached`, and a one-sided working-copy fallback on either read scores 63/63 (MEASURED here, both sides) while reading a PASS from the working copy in its cell -- two legs, two mutants, two contract lines and the counts, then GREEN/RED/FINAL again; every other row of the enumeration verified against the bank

FABLE_SEAT_ALIVE_20261107_GHOSTCLOSE

First line of `C:/DocumentNoSnc/CC/GXEMUL/_scratchpad/wghost/landing/REVIEW_BRIEF_pass3.md`, verbatim:
`# The class-closure pass on `#587` ghostround -- VERIFY THE ENUMERATION (Fable 5.1, REPAIR_RULING.md, s.4 item 8)`

# RULING -- the CLASS-CLOSURE (pass 3) review of `#587` ghostround, Fable 5.1, 2026-11-07

**Subject.** HEAD `8d9df658`; the kit `_scratchpad/wghost/landing/` -- `staged_final/` (checker md5 `6b545d3d57ec`, hook
`b678efd6e315`, P2 block `9e234aa86586` by `after_final.py`'s `p2block()` cut, recomputed here), the bank `wired/` (byte-identical
to `staged_final/regress/artifacts/ghostround/wired_20261106/`: `run_checker_controls.sh` `73168aa1ed11`, `run_mutants.sh`
`42fd9f359ac2`, `REPAIR_RULING.md` `37feaec30c8e` = my `ghostrepair/RULING.md`), and the two pass-3 seats.  Line numbers are
the STAGED files' unless marked.

**What I did (read-only; `git -C GXEMUL-SEC status --porcelain | wc -l` = 953 BEFORE and 953 AFTER; no git command that writes;
scratch only under the session scratchpad `.../scratchpad/ghostclose/`).**
1. Read the brief, both seat answers in full, my own REPAIR_RULING, the staged checker (520 lines), the hook's P2 comment and block
   (`:244-279`), `run_checker_controls.sh` (306 lines), `run_mutants.sh`, `CHECKER_CONTROLS.out` (63 `ok` lines, 46 names, 0 BAD),
   `MUTANTS.out`, `MUTANTS_NEGCTL.out` (LF only, `od -c`), `RECEIPT.md`, `PRETEST_FINAL.summary`, `AFTER_FINAL.out`, `commit_ghost.msg`,
   CHANGELOG `:1-82`, bug file `:26778-26783`, the ledger row (witness, state_note, hold_question, the fable5 review entry), the
   pre-repair checker `work/check_ghost_rounds.filled.py` (`999b73aa6b24`) `load()` `:367-386`.
2. **Ran the bank's own `run_checker_controls.sh` on an independent rig** (a scratch clone of GXEMUL-SEC for the `--at` legs; the
   staged hook): the staged checker -> `CONTROLS: 63 ok, 0 BAD`, the 63 `ok` lines IDENTICAL to the banked `CHECKER_CONTROLS.out`.
3. **Built Astra's two one-sided fallbacks as mutants** (one line each after `:442`: `lb = lb if lb is not None else
   open(LEDGER, "rb").read()` / the same for `cb`/`CHANGELOG`) and ran the same 63 checks against each: **63 ok, 0 BAD -- both
   ESCAPE, line-for-line identical to the baseline.**  Astra's static deduction is now a measurement.
4. **Built the two mixed cells with real git** in a leg-8-shaped repo (`git rm --cached` one file, the other staged):

   | cell (index mode) | staged checker | mutant on the ledger read | mutant on the CHANGELOG read |
   |---|---|---|---|
   | ledger ABSENT from the index, CHANGELOG present (block staged; the WORKING-COPY ledger carries the write-back) | rc 2 `GHOST_ROUNDS_VOID` | **rc 0 `GHOST_ROUNDS_PASS`**, printing `read: the index of ...` | rc 2 VOID |
   | CHANGELOG ABSENT from the index, ledger present (the working copy holds the block) | rc 2 VOID | rc 2 VOID | **rc 1 `GHOST_ROUNDS_FAIL`**, printing `read: the index of ...` |
   | control -- c8h's cell (bogus `GIT_INDEX_FILE`, BOTH reads fail) | VOID | VOID | VOID |

   So each mixed cell is reachable, each mutant is fail-open in exactly its own cell (a PASS from the working copy, with the `read:`
   line asserting the index), and c8h's cell cannot see either -- the De Morgan shape this project measured on `pcc2widthkills`
   pass 10: the disjunction is true in every rowed cell, so a per-disjunct mutant never fires.
5. Recomputed the kit's hashes Grok could not (`6b545d3d57ec`, `73168aa1ed11`, `9e234aa86586`); re-derived PRE's 11, M5's 5, M9/M14's 1,
   M10's 4, M11's 2, M13's 3 from the legs' setups; confirmed the kit's PRETEST.md corrections from my s.4 item 7(e) are made
   (`#586`/`bugfilereverse` gone; `run_x_control.sh` marked ROUND 1 ONLY at `:99`; "at its START" at `:166`).

## 1. The dispute, ruled from my ruling's own space

My s.4 wrote the space as "`git show` (ledger, CHANGELOG) in {ok, fail}" and then rowed it as ONE cell per mode ("index: show
fails | c8h").  **The prose named two reads; the table collapsed them.**  The code settles which was right: the guard at `:443` is
`if lb is None or cb is None` -- two operands, each tested, each with its own {None, bytes} partition.  By the joint-cells rule
(DEPENDS-ON enumerates joint cells exactly when the guarded body's own code distinguishes them) that is a 2 x 2 product: {both ok,
ledger-only fail, CHANGELOG-only fail, both fail}.  c8h holds (fail, fail); every other index leg holds (ok, ok); **the two mixed
cells had no row and no disclosure.**  Reachability is measured (item 4: one `git rm --cached`), the escaping mutants are measured
(item 3), and the mutant's effect in-cell is the class itself -- a degraded read silently taking a weaker source, with the checker's
own `read:` line misreporting the source.  **Floor breach, L2, repaired in-round.**  Not clause (b): the pre-repair fallback
(`filled.py:379-383`) was ONE joint site (`if lb is not None and cb is not None` ... else both working copies), so the one-sided form
is a clause-(d) weakening of the guard, not a verbatim reinstatement -- which is why PRE is killed by c8h and the mutant is not.

**The `--at` mixed cells stay DISCLOSED**, not legged: the hook never runs `--at` (P2 `:270` passes no `--at`), and pre-repair the
`--at` guard was a `SystemExit` (never fail-open), which is the warrant my ruling gave for disclosing the whole `--at` show-fail row
and both seats accepted.  The disclosure must SAY it covers either read or both (edit below).  Legs for them are filed as clause-(e)
debt: trivially buildable, outside the hook's path.  **No hook-level leg is owed for the mixed cells**: the hook sees a verdict, not a
read, and c9e pins VOID -> hard FAIL whatever failed.

**Astra is right and Grok is wrong on the one question that separates them, and the difference is not a reading of the code -- both
read the guard correctly -- but whether a cell the guard's own `or` distinguishes may be folded into its neighbour.  It may not.**  The
enumeration error is MINE (the table under the prose), and this pass found it, which is what a pass "scoped to verifying the
enumeration" exists to do.

## 2. Every finding, ACCEPT / AMEND / REJECT

### 2a. GPT-6 Astra (`pass3_seats/codex_GHOSTCLOSE_ASTRA.txt`, 3,194 B; the 458 KB `.err` is its stderr stream) -- 7 ACCEPT, 1 AMEND

| # | finding | ruling | settled by |
|---|---|---|---|
| A1 | 2 cells without a leg or a disclosure: index mode, ledger-only / CHANGELOG-only read failure | **ACCEPT** -- reachable with real git; unrowed; the class | item 4; `:443`; part 3 of the brief |
| A2 | c8h fails BOTH reads, so a one-sided fallback before the guard survives c8h and every other check (static) | **ACCEPT, MEASURED** -- 63/63 for each side, identical `ok` lines | item 3 (`ctl_mutL.out`, `ctl_mutC.out` in my scratchpad) |
| A3 | the other 17 rows match the implementation and their coverage or disclosure | **ACCEPT** -- s.3 below, row by row against `MUTANTS.out` and the legs' setups | read |
| A4 | c9b behaviourally tests only GXLEDGER; the other four names are pinned by M7's exact find-text plus NOT BUILT; not counted as breaches | **ACCEPT** -- `run_checker_controls.sh:279`, `run_mutants.sh:83`, NEGCTL rc 1.  A TEXT pin is weaker than a leg and the contract must say which it is (edit R3c) | read |
| A5 | every new leg has its measured kill: c4d/M9, c8j+c8k/M10, c9d/M11, c9e/M12, HOOK-fail=1/M13, c8i's tightening/M14 | **ACCEPT** | `MUTANTS.out` |
| A6 | 3 wrong records: CHANGELOG `:52-55`, bug file `:26780`, the ledger row's "one class, closed in one diff" | **AMEND** -- CHANGELOG and bug file ACCEPTED as false of the bank (two cells unlegged; "every cell and the leg that pins it" also contradicts the contract's own no-leg disclosures, G6).  The ledger sentence becomes TRUE once the repair lands in the same diff, but the row must then name the closing pass's finding, so the edit is owed either way | read |
| A7 | counts: 63 checks, 46 names, 13 + PRE = 14; BAD-name lists are deduplicated; NEG NOT BUILT rc 1; hashes and GREEN/RED/FINAL agree | **ACCEPT** -- 63 `ok` / 46 names counted; md5s match `STAGED_MD5.txt` and `RECEIPT.md`; `P2_GREEN.out:134` PASS 0 hard, `P2_RED.out` exactly one `  FAIL` (`:19`) and `PRECOMMIT_FAIL 1 hard` | measured |
| A8 | fix first: close the two cells with observable controls and measured kills, then reconcile the closure claims | **ACCEPT** -- s.4 | |

### 2b. Grok 4.7 (`pass3_seats/grok_ghostclose.txt`, 5,590 B) -- 8 ACCEPT, 1 AMEND, 1 REJECT

| # | finding | ruling | settled by |
|---|---|---|---|
| G1 | 0 cells without a leg or disclosure; "index show fails" is one cell pinned by c8h | **REJECT** -- the guard's own `or` distinguishes the two reads; both mixed cells reachable; both one-sided mutants escape 63/63 and are fail-open in-cell | items 3-4 |
| G2 | row-by-row: `load()`, `complete()`, P2's branches and the pre-repair checker do what part 3 says; each named leg observes its cell | **ACCEPT** for 17 rows (s.3); the show row is G1 | read |
| G3 | the contract cites `c6a` for header dating, but c6a REQUIRES `dated by blame` -- it is file mode where git CAN date; c1a-c3 are the header-dating cell | **ACCEPT** -- `run_checker_controls.sh:124`; and `--no-git` has NO leg at all (0 occurrences in the controls).  Precision edit R3d | read |
| G4 | each new leg's kill traced for the stated reason; PRE's 11 = two checks each on c4d, c8h, c8i, c8j, c8k + c9e; M3/M6's 12/161 and 162/263 are in the saved `c5_HEAD_*.out` | **ACCEPT** -- PRE's 11 re-derived the same way | `MUTANTS.out` |
| G5 | c9b exports only GXLEDGER; the other four are M7's find-text; one GX* cell, not five | **ACCEPT** (= A4; edit R3c) | |
| G6 | 2 wrong records: CHANGELOG "names every cell and the leg that pins it" (the block's own `:81-82` carves two cells back out) and the bug file's "names every cell and its leg ... each with a leg" with no carve-out | **ACCEPT** -- and both are false a second way (A1) | read |
| G7 | the ledger witness, state_note and commit message do not claim "every cell"; their 63 / 14 match the logs | **ACCEPT** as read today -- the counts move with the repair (R4) | read |
| G8 | M11's "by `c9d` (2 of 63)" is the true total; the second red check is c9e, unnamed | **ACCEPT** as an observation; not a wrong record -- the parenthetical is the mutant's SCORE as `MUTANTS.out` prints it (M10's names both legs because both are its targets).  No edit owed | `MUTANTS.out` |
| G9 | fix first -- the two record sentences | **AMEND** -- the verdict is right and the reason is larger: a floor breach, not records only | |
| G10 | denominator 18 cells / 63 checks / 14 mutants + NEG; the three hashes not recomputed ("shell hashing was refused") | **ACCEPT** -- hashes recomputed here, all three match | item 5 |

**Counted by argument, not by seat:** one argument separated them (G1 vs A1) and it is settled by a measurement neither seat ran.
Everything else the two seats say agrees with the bank and with each other.

## 3. The enumeration, verified row by row (the denominator)

18 rows of part 3; for each, the staged code read, the leg's setup read, and the bank's score checked:

| row | code (staged) | leg / disclosure | bank | verdict |
|---|---|---|---|---|
| --at: show fails | `:436-437` VOID | disclosed, no leg | -- | ok; **disclosure must say "either read or both"** (R3b) |
| --at: blame rc != 0 | `complete()` `:413` "failed in" | c4d (3 checks) | M9 1/63 = c4d's ctl (missing "failed in"); absent-PASS/FAIL stay green | ok |
| --at: blame rc 0, short | `:416` "dated N of M" | c8k (2) | M10 4/63 = c8j x2 + c8k x2 | ok |
| --at: ledger not JSON | `json.loads` `:439` outside `except Void` | disclosed | -- | ok |
| **index: show fails** | `:443` -- TWO operands | c8h (3) holds (fail, fail) ONLY | PRE 11/63 includes c8h x2; M5 5/63 includes c8h x2 | **TWO CELLS MISSING** (s.1) |
| index: blame rc != 0 | `:446` -> `complete()` "failed in" | c8i (2, wants `git blame --contents` AND `failed in`) | M14 1/63 = c8i's ctl; PRE | ok -- the "failed in" tightening is correct: M14's `{}` is VOID as "dated 0 of", distinguishable only by the message |
| index: blame rc 0, short | `:446` -> `:416` | c8j (2; `--object-format=sha256`, 65-char sha asserted) | M10 | ok |
| index: ledger not JSON | as --at | disclosed | -- | ok |
| index: temporary index | `git()` keeps the environment `:215` | c8g, c8g2 | M5 5/63 (c8g, c8h x2, c9d, c9e) | ok |
| file mode; `--no-git` | `blame_file` `{}` `:282/:284`; `nogit` `{}` | "c1-c3, c6" | -- | ok as design; **c6 is the wrong citation and `--no-git` has no leg** (G3; R3d) |
| hook: rc 0 + PASS | `:270-271` | GREEN | `P2_GREEN.out:134` | ok |
| hook: rc 0, no token | `:276-277` `else` | c9c | M8 1/63 | ok |
| hook: rc 1 + FAIL | `:272-275` | c9a, c9b | M1 2/63 (c9a, c9b -- the SAMEDAY fixture passes under `--rule=date`); M7 1/63 | ok |
| hook: rc 2 + VOID | same `else` | c9e (wants "reached no verdict" AND `GHOST_ROUNDS_VOID` AND HOOK-fail=1) | M12 1/63 | ok |
| hook: crash | same `else` | disclosed (c9c's branch) | -- | ok |
| hook: GX* exported | `env -u` x5 `:270` | c9b (GXLEDGER only) | M7 (whole-prefix find-text) | ok, with the text-pin disclosure (R3c) |
| hook: GIT_INDEX_FILE kept | not in `:270` | c9d | M11 2/63 (c9d, and c9e collaterally) | ok |
| hook: `fail` counted | `bad()` `:37` increments | c9a, c9b, c9d want `^HOOK-fail=1$` | M13 3/63 (c9e uses the other `bad` and stays green) | ok |

Also checked: the brief's "39 hunks in 8 of 8 parts" (7+1+14+6+5+1+3+2 = 39); `c8k` is a true twin (`complete()` is the one guard both
modes call, `:438/:446`); `M14` is the true index twin of M9 (`blame_contents` `:275` `else None`); `MUTANTS_NEGCTL.out` is LF text ending
`rc=1 / NEGCTL_DONE`; the driver's `mutate` refuses a find-text found 0 or 2 times (`:31-33`), so `if lb is None or cb is None:` (2
occurrences) cannot be a find-text and the unique `:442` line is the one to anchor the new mutants on.

**New legs vacuous?**  None: c4d, c8i, c8j, c8k each red under a measured mutant (and under PRE); c9d, c9e, HOOK-fail=1 each red under
M11/M12/M13.  **Not re-derived by me:** EQUIV's 72 cells (accepted twice before against `EQUIV.out`, tail re-read: `72 comparisons, 0
DIFFERENT`); the GREEN/RED/FINAL runs themselves (their outputs read, not re-run).

## 4. VERDICT: HOLD -- the smallest repair, and it RE-OPENS the FINAL run

**R1. Two legs** in `run_checker_controls.sh`, leg 8, after c8h's cleanup (`:189`) and before the c8i repo -- the setup is item 4's,
the WORKING-COPY ledger carrying the write-back so a fallback to it is a PASS (the loudest form of the class):

```
#  REVIEW 3 (the closing pass, CLOSE_RULING.md s.1): the index guard tests its TWO reads separately (`lb is None or cb is
#  None`), so "show fails" is a {ok,fail} x {ok,fail} product; c8h holds only the both-fail cell, from which a ONE-SIDED
#  working-copy fallback cannot be seen (measured: 63/63 for each side).  Real git writes each mixed cell with one `git rm --cached`.
#    mutant M15: `lb = lb if lb is not None else open(LEDGER, "rb").read()` after the index git_show line    measured: <MUTANTS.out>
#    mutant M16: `cb = cb if cb is not None else open(CHANGELOG, "rb").read()` after the same line           measured: <MUTANTS.out>
( cd "$R" && cm rm -q --cached tools/pipeline/ledger.json && { printf "$NEWB"; git show HEAD:CHANGELOG.md; } > CHANGELOG.md && cm add CHANGELOG.md )
python - "$S/synth_ledger.json" "$R/tools/pipeline/ledger.json" <<'PYEOF'
import io, json, sys
d = json.load(io.open(sys.argv[1], encoding="utf-8"))
for r in d["rows"]:
    if r["id"] == "ghostopen":
        r["state_note"] = "[#904, today: landed.]"      # the WORKING copy records the round; the index has no ledger at all
io.open(sys.argv[2], "w", encoding="utf-8", newline="\n").write(json.dumps(d, indent=1))
PYEOF
CTL_ENV="$X" CTL_ARGS="" ctl c8l_ledger_unstaged_VOID 2 GHOST_ROUNDS_VOID "cannot be read"
absent c8l_ledger_unstaged_VOID GHOST_ROUNDS_PASS
absent c8l_ledger_unstaged_VOID GHOST_ROUNDS_FAIL
( cd "$R" && cm reset -q && git checkout -q -- . )
( cd "$R" && cm rm -q --cached CHANGELOG.md && { printf "$NEWB"; git show HEAD:CHANGELOG.md; } > CHANGELOG.md )
CTL_ENV="$X" CTL_ARGS="" ctl c8m_changelog_unstaged_VOID 2 GHOST_ROUNDS_VOID "cannot be read"
absent c8m_changelog_unstaged_VOID GHOST_ROUNDS_PASS
absent c8m_changelog_unstaged_VOID GHOST_ROUNDS_FAIL
( cd "$R" && cm reset -q && git checkout -q -- . )
```
63 -> **69 checks**.  The legs want the TOKEN and the absence of the other two; they must NOT want the `read:` line, which under the
mutant still says "the index of" (item 4) -- the checker's report of its source is a claim, not an observation.

**R2. Two mutants** in `run_mutants.sh` after M14 (the find-text occurs exactly once in the staged checker):
```
leg M15 checker c8l_ledger_unstaged_VOID '        lb, cb = git_show("", LEDGER_REL), git_show("", CHANGELOG_REL)' '        lb, cb = git_show("", LEDGER_REL), git_show("", CHANGELOG_REL)
        lb = lb if lb is not None else open(LEDGER, "rb").read()'
leg M16 checker c8m_changelog_unstaged_VOID '        lb, cb = git_show("", LEDGER_REL), git_show("", CHANGELOG_REL)' '        lb, cb = git_show("", LEDGER_REL), git_show("", CHANGELOG_REL)
        cb = cb if cb is not None else open(CHANGELOG, "rb").read()'
```
**Expected (a PREDICTION, to be measured, never copied into a record):** M15 BAD on c8l's ctl and absent-PASS only (2 of 69); M16 BAD on
c8m's ctl and absent-FAIL only (2 of 69); PRE rises from 11 to 15 (its joint fallback is fail-open in both new cells); every other
mutant's score unchanged except the denominator.  14 -> **16 mutants**.

**R3. The contract (docstring) and two precision lines** -- these change the CHECKER's bytes (comment only; `load()`/`complete()`
untouched):
* (a) `:58` `index   git show fails: VOID (c8h; the pre-repair checker).` -> `index   git show fails -- either read, or both: VOID (c8h
  both; c8l the ledger alone, c8m CHANGELOG alone -- the guard tests the two reads separately, so a one-sided fallback is its own cell;
  M15, M16, the pre-repair checker).`
* (b) `:55` `--at    git show fails: VOID (no leg; before the repair it was a SystemExit, rc 1 -- never a pass).` -> `--at    git show
  fails, either read or both: VOID (no leg -- the hook never runs --at, and before the repair it was a SystemExit, rc 1, never a pass).`
* (c) `:65-66` `The five GX* names are cleared (c9b; M7)` -> `The five GX* names are cleared (c9b exports GXLEDGER; the other four are
  pinned by M7's find-text -- a presence pin, not a behavioural leg)`.
* (d) `:61-62` `file mode (--worktree, GXLEDGER/GXCHANGELOG) and --no-git: header dates where git cannot date -- BY DESIGN (c1-c3, c6).`
  -> `file mode (--worktree, GXLEDGER/GXCHANGELOG): header dates where git cannot date -- BY DESIGN (c1-c3; c6 is file mode where git
  CAN date, by blame); --no-git: header dates by design, no leg.`
* `run_checker_controls.sh` `:22-28` header: add the REVIEW 3 sentence (two legs, the product).  `run_mutants.sh` `:2-6`: add M15/M16.

**R4. Records (exact old -> new; counts are placeholders for the MEASURED values of the re-run):**
* CHANGELOG `:53-54` `the checker's docstring names every cell and the leg that pins it (THE CONTRACT)` -> `the checker's docstring
  names every cell and the leg that pins it, or the disclosure that stands in for one (THE CONTRACT)`.  After `:55` `... M14 by c8i (1
  of 63 checks BAD).` insert: `The closure's own pass (GPT-6 Astra, Grok 4.7; ruled by Fable 5.1, CLOSE_RULING.md) found the
  enumeration one axis short: the index guard tests its two reads separately and the ruling's table had rowed "show fails" as one
  cell, so a one-sided working-copy fallback -- the ledger alone, or CHANGELOG alone -- passed all 63 checks (measured) and in its
  cell read a PASS from the working copy while printing read: the index; two legs, c8l and c8m (one git rm --cached each), and two
  mutants, M15 by c8l (<n> of 69), M16 by c8m (<n> of 69), close the product, and the --at disclosure names both reads.`
  `:65` `63 of 63` -> `69 of 69`; `:66-67` `(13 of them: M12 inserts two lines, every other changes one) ... 14 of 14` -> `(15 of
  them: M12, M15 and M16 insert lines, every other changes one) ... 16 of 16`; `:81-82` `a failed git show in --at mode is VOID with
  no leg of its own` -> `a failed git show in --at mode (either read) is VOID with no leg of its own`.
* OUTSTANDING_BUGS `:26780` `the contract in the checker's docstring names every cell and its leg, five legs and six mutants.  All
  repaired before landing, each with a leg.` -> `the contract in the checker's docstring names every cell and its leg or its
  disclosure, five legs and six mutants; the closure's own pass found the index guard's two reads rowed as one cell and added two
  legs and two mutants (c8l, c8m; M15, M16).  All repaired before landing, each with a leg or a named disclosure.`
* ledger `ghostround` witness: `63 of 63` -> `69 of 69`; `the 13 single-edit mutants and the pre-repair checker, each killed by its
  leg, 14 of 14` -> `the 15 single-edit mutants and the pre-repair checker, each killed by its leg, 16 of 16`.  state_note:
  `REPAIR_RULING.md -- one class, closed in one diff)` -> `REPAIR_RULING.md -- one class, closed in one diff; its closing pass,
  wired_20261106/CLOSE_RULING.md, found the index guard's two reads rowed as one cell and added c8l, c8m)`.  The fable5 review
  entry: `one class, closed in one diff.  Those seats' own entries` -> `one class, closed in one diff; the closure's own pass (GPT-6
  Astra, Grok 4.7; Fable 5.1, HOLD: wired_20261106/CLOSE_RULING.md) found two cells of the index guard unrowed, legged before
  landing.  Those seats' own entries`; and `The closure's own pass, scoped to verifying the enumeration, is drafted on its diff.` ->
  `The closure's own pass is ruled (CLOSE_RULING.md); the pass on its repair is drafted on that diff.`
* `commit_ghost.msg` `:21-23` `63 of 63; the 13 single-edit mutants the two reviews traced and the pre-repair checker, each killed by
  its leg, 14 of 14; ... the two rulings.` -> `69 of 69; the 15 single-edit mutants the three reviews traced and the pre-repair
  checker, each killed by its leg, 16 of 16; ... the three rulings.`
* `RECEIPT.md`: the CHECKER_CONTROLS row gains `c8l, c8m (one read absent from the index)`; the MUTANTS row `the two reviews` ->
  `the three reviews`; a `CLOSE_RULING.md` row (this file, verbatim, md5 recorded); the "Results, verbatim" counts; the md5 table.
* **Bank this ruling** as `regress/artifacts/ghostround/wired_20261106/CLOSE_RULING.md`, byte-identical to this file, as
  `PASS2_RULING.md` and `REPAIR_RULING.md` were.  `REPAIR_RULING.md` is a banked, dated artifact and is NOT edited: this file is its
  correction and the records cite it.

**R5. Re-run.**  `run_checker_controls.sh` (-> 69 ok), `run_mutants.sh` with PRE and the NEGCTL (-> 16/16, NOT BUILT rc 1), then GREEN,
RED and the FINAL on the re-staged unit.  **The FINAL run IS re-opened** -- not arguably: R3 changes the checker's bytes, which is the
identity `after_final.py` pins (`6b545d3d57ec`), and the brief defines FINAL as "the exact landing unit with its bank".  The change is
comment-only, so green is EXPECTED; that is the reason to expect it, not a reason to skip it.  Time: it is 06:4x; the FINAL took 1,684 s,
so controls + mutants + GREEN + RED + FINAL fit today with hours to spare.  If midnight is crossed the fills move (`CALENDAR.json`).

**R6. The chain.**  One more pass on the repair diff (R1-R4), scoped to: (i) `MUTANTS.out` shows M15 red on c8l only and M16 on c8m only,
and PRE's new score; (ii) the enumeration now reads four show cells per mode, two disclosed in `--at`, two legged and one both-legged
in index mode; (iii) the floor question on the composite -- is there a clean-sweep mutant in the (d) enumeration of the three guards
(`:436`, `:443`, `complete()`)?  Roster: Astra and Grok, then this seat.  It closes on zero breaches surviving adjudication, with its
denominator; a bare zero does not close.  **Stop condition honoured:** the two breaches here are ONE class cell-pair that the class
closure's own enumeration missed, closed in one diff with the enumeration corrected -- not a new cell per pass.

## 5. FILED, not owed (clause (e), each disclosed)

* `--at` legs for the mixed cells (`--at=HEAD` on a scratch repo whose HEAD lacks one of the two files): outside the hook's path;
  the disclosure now names both reads.
* A `--no-git` leg (header dates by design): not a class cell -- an explicit flag is not a silent degradation.
* Hardening the `read:` line so it names the SOURCE ACTUALLY READ per file: today it is a template string.  A records-quality
  improvement; under the staged code it is true in every reachable cell, and the legs now key on the token.
* M11's record form "(2 of 63 checks BAD)" beside "by c9d": true as a score; G8's suggested "the other c9e" is a nicety.

## 6. Seat ledger for this stage

GPT-6 Astra (ultra) and Grok 4.7 (xhigh) **both ANSWERED** -- real content, verdict line present, denominators stated, no wall or
quota text (Astra's `cxlaunch.out` and 458 KB `.err` are its normal stderr stream).  **One tooling note:** Grok's `GHOSTCLOSE:` line is
on line 1 but PRECEDED on that line by three streamed preamble sentences, so an anchored `^GHOSTCLOSE:` grep misses it while the
token is present; `seat_verdicts.py`'s position discriminator should be checked against this shape.  No agy, Opus or Ollama seat was
fired for this pass (the owner's roster for the repair: Astra and Grok, then Fable); none is counted as agreement.  This ruling is
the Fable 5.1 seat.  **Where the two disagreed, neither argued from a wrong reading of the code; the question was which cells a
disjunctive guard owns, and a two-minute scratch run answered it where two readings could not.**

**Honest limits.**  The M15/M16 scores and PRE's new score are predictions until the re-run; the GREEN/RED/FINAL outputs were read,
not re-run; EQUIV's 72 was read from its tail.  My own earlier enumeration (REPAIR_RULING s.4) is the record this pass corrects, and
it is corrected here rather than in place because that file is banked and dated.

FABLEGHOSTCLOSE: 15 ACCEPTED 2 AMENDED 1 REJECTED VERDICT:HOLD -- the index guard tests its two reads separately (`lb is None or cb is None`), so "show fails" is a {ok,fail} x {ok,fail} product and my ruling's table rowed it as ONE cell; the two mixed cells are reachable with one `git rm --cached`, and a one-sided working-copy fallback on either read scores 63/63 (MEASURED here, both sides) while reading a PASS from the working copy in its cell -- two legs, two mutants, two contract lines and the counts, then GREEN/RED/FINAL again; every other row of the enumeration verified against the bank
