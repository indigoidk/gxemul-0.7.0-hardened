FABLEGHOSTREPAIR4: 18 ACCEPTED 5 AMENDED 0 REJECTED VERDICT:LAND -- zero floor breaches survive adjudication, with the denominator (3 guards, 14 read/blame cells = 9 legged + 5 disclosed, 69 checks, 16 mutants + PRE + NEG, 3 escape candidates MEASURED here through the bank's own harness, 8 record sites): Astra's "nonempty-short blame" cell is a split the guarded body never makes (`complete()` tests `is None` and `len(bl) != nlines(cb)`, never emptiness) and no production git writes such a map (measured, porcelain headers stay 40-hex even under blame.markIgnoredLines), so the three single edits that pass 69/69 (`if bl: return bl`, `len(bl) == 0`, a bound relaxed by one line) are clause (e) -- DISCLOSED in the records, not legged; the one wrong record is my own R4's "read a PASS", false of the CHANGELOG cell (it FAILs, CLOSE_RULING item 4) -- corrected in place; every edit is records-only, the checker (f20d249eeb21) and P2 block (9e234aa86586) the FINAL pinned are untouched, so the FINAL is NOT re-opened and the live hook gates the exact bytes at the commit

FABLE_SEAT_ALIVE_20261107_GHOSTREPAIR4

First line of `C:/DocumentNoSnc/CC/GXEMUL/_scratchpad/wghost/landing/REVIEW_BRIEF_pass4.md`, verbatim:
`# Pass 4 -- the closing pass's REPAIR on `#587` ghostround (Fable 5.1, CLOSE_RULING.md s.4 R6): the repair diff, bounded`

# RULING -- pass 4 of `#587` ghostround: the bounded pass on the closing pass's repair, Fable 5.1, 2026-11-07

**Subject.** HEAD `8d9df658`; the kit `_scratchpad/wghost/landing/` -- `staged_final/` (checker md5 `f20d249eeb21`, hook
`b678efd6e315` -- UNCHANGED since the closing pass, which recorded the same hook md5 -- P2 block `9e234aa86586`), the bank `wired/`
(md5-by-md5 identical to `staged_final/regress/artifacts/ghostround/wired_20261106/`, 29 files; controls `14c229af13db`, mutants
driver `3131adb18176`), the pre-repair checker `work/check_ghost_rounds.filled.py` (`999b73aa6b24`), and the two pass-4 seats.  Line
numbers are the STAGED files' unless marked.

**What I did (read-only; `git -C GXEMUL-SEC status --porcelain | wc -l` = 953 BEFORE and 953 AFTER; no git command that writes in any
project tree; scratch only under the session scratchpad `.../scratchpad/gr4/`).**
1. Read the brief, both seat answers in full, my CLOSE_RULING, the staged checker (524 lines), `run_checker_controls.sh` (333 lines, legs
   c8l/c8m at `:194-216`), `run_mutants.sh` (M15/M16 at `:104-107`; `sort -u` at `:41`), `MUTANTS.out`, `MUTANTS_NEGCTL.out`,
   `CHECKER_CONTROLS.out` (69 `ok`, 0 BAD), `RECEIPT.md`, `PRETEST_FINAL.summary` (rc=0 in 1439 s, `PRECOMMIT_PASS 0 hard, 6 soft`),
   `AFTER_FINAL.out`, `STAGED_MD5.txt`, CHANGELOG `:1-90`, the bug file `:26778-26782`, the ledger row (witness, state_note,
   hold_question, the fable5 entry), `commit_ghost.msg`, the pass-4 brief (parts 1-6), `commit_ghost.DRAFT.spec.json` and
   `commit_unit2.py`'s hook contract (exit 4 when the pre-commit hook fails: the live gate runs at the landing commit).
2. **Validity of the pass:** the diff was delivered (31 hunks in 8 of 9 parts, the hook's part 0 -- "refused at zero"); both seats
   answered with a `GHOSTREPAIR4:` line and a denominator; no wall or quota text.  A VALID pass, so its zero can close.
3. **RAN the bank's own `run_checker_controls.sh` on a fresh read-only clone of GXEMUL-SEC at `8d9df658`** (23-28 s a run):
   the staged checker -> `CONTROLS: 69 ok, 0 BAD`, the 69 `ok` lines identical to the banked `CHECKER_CONTROLS.out` (one cosmetic
   difference: my hook copy's filename in the `p2_block_cut` line).  Then THREE single-edit guards on `complete()`, built with the
   driver's own exact-once `mutate` idiom on the unique line `    if len(bl) != nlines(cb):`:
   * Astra's candidate -- `if bl:` / `return bl` inserted immediately before it -> **69 ok, 0 BAD, `ok` lines identical to base**;
   * Grok's narrowing -- `if len(bl) == 0:` -> **69 ok, 0 BAD, identical**;
   * a bound relaxed by one line -- `if len(bl) + 1 < nlines(cb):` -> **69 ok, 0 BAD, identical**.
   (`scratchpad/gr4/ctl_{base,astra,grok,relax}.out`, `RUN.log`; volatile, so the numbers are written here and this file is banked.)
   c8j's cell under the staged checker prints `dated 0 of 7 lines`, so the two short-blame legs hold the point len = 0 of a 7-line file.
4. **Measured the premise under the dispute -- that no production git writes a NONEMPTY short map.**  A scratch repo with
   `blame.ignoreRevsFile`, `blame.markIgnoredLines=true` and `blame.markUnblamableLines=true` (the only blame options that mark lines)
   marks the NON-porcelain output (`^?4328c2`) and leaves every porcelain header 40-hex; the staged `porcelain_dates` dated **5 of 5**
   lines of a `--contents` file (four committed shas, one all-zero).  No global `blame.*` config exists on this machine.
5. Verified the bank's identity, every count the records carry (69/69; 16 of 16; M15 2 of 69 on c8l only; M16 2 of 69 on c8m only; PRE
   15 of 69 = 11 + 2 + 2; NEG `NOT BUILT` rc=1), the hook unchanged, and the 29 banked files byte-identical to the staged bank.

## 1. The dispute: is NONEMPTY-short a cell of the floor?

**No -- it is clause (e), on three independent grounds, the third measured.  Astra's OBSERVATION stands (both short-blame legs drive the
empty map and assert `dated 0 of`); its GRADE falls.**

(a) **The body-tested partition.**  `complete()` (`:412-424`) tests exactly two things on `bl`: `bl is None` (`:417`) and
`len(bl) != nlines(cb)` (`:420`).  The partition the body induces on `bl` is therefore {None, len != nlines, len == nlines} -- three
members, and ALL THREE ARE ROWED: None by c4d/c8i (M9, M14), `!=` by c8j/c8k (M10), `==` by every PASS/FAIL leg.  Emptiness is never
tested; `if bl:` and `len(bl) == 0` INTRODUCE a predicate the body does not have.  The joint-cells rule says exactly this: "A value or
combination the body never tests as a case ... is DISCLOSED under clause (e)"; and 7n-5 says it of a derived input by name -- "A DERIVED
INPUT IS GRADED BY WHAT THE BODY TESTS ON IT, NEVER BY THE FLOW THAT REACHES IT" (`tile_nr`, tested `>= 256` and `>= 32`, never for
zero: clause (e)).  `len(bl)` is tested against `nlines(cb)`, never for zero.  It is the `&& idata != 2` shape of pcc2 pass 11, which
escaped and was graded (e): a single-operand exemption of values INSIDE a body-tested cell.

(b) **D2 does not reach it, and not only by its letter.**  D2 pins a region at its edge for "a relational compare against a CONSTANT bound
B"; here the bound is `nlines(cb)`, a derived input, and the compare is `!=`, which has NO slack region: the one-token bound move
`!= nlines(cb) - 1` reds every complete-map leg (they become VOID), so c8j/c8k are not a "far row" of any bound a one-token edit can
move.  My relaxed-bound mutant escapes only by changing `!=` to `<` AND adding `+ 1` -- two edits -- and it lands in the same slice as
the other two.  A rule question for the owner, filed not ruled: whether D2's warrant extends to a VARIABLE bound.  It changes nothing
here, because of (c).

(c) **Reachability -- derived from the WRITERS, then measured.**  `porcelain_dates` (`:233-260`) has exactly two skip branches: the 40-hex
header regex (`:240`) and the committer-time lookup (`:254-255`, `if t is None: continue`).  The first is UNIFORM PER REPOSITORY -- in a
SHA-1 repository every header matches, in a SHA-256 one none does (c8j, c8k) -- so it yields an EMPTY map or a COMPLETE one, never a
mixture.  The second never fires on git's own porcelain: the full header, committer-time included, is printed at the first occurrence of
every sha, `times` is keyed by sha across the whole output, and the all-zero sha is handled before the lookup (`:251-253`).  Measured
today (item 4): the only blame options that mark lines leave porcelain untouched, 5 of 5 dated.  So the map git hands `complete()` is
None, EMPTY or COMPLETE; **a NONEMPTY short map has no production writer**.  A leg for it needs a doctored `git` -- a row for a cell
nothing writes, which is the addition licence's "cannot hurt" wearing detector clothes; the carrier's own form for such a cell is
"disclosed as UNREACHABLE with its derivation ... the honest form of a cell nobody rows."

**What the dispute actually was.**  Both seats read the code right.  Astra built the mutant and measured its behaviour in memory (a
nonempty short map's missing header line silently gets its textual date -- true, by `:420-424` and `parse_blocks` `:307-318`: an unlisted
line takes its header date or TODAY); Grok read that the two shortfalls are one cell of the body's partition and that counting the
narrowing "would be a new cell per pass".  Grok is right on the grade and Astra is right that the escape is REAL and MEASURABLE -- it is
now measured through the harness, 69/69 three ways.  **Neither seat said the measured escape must then be WRITTEN DOWN**: above the
floor, a measured escape is coverage debt that is FILED and DISCLOSED, not forgotten.  That is edit E2/E3 below.

## 2. The floor question on the COMPOSITE -- the (d) enumeration of the three guards, and the denominator

| guard | weakening | result | disposition |
|---|---|---|---|
| `--at` show `:440` (`lb is None or cb is None`) | one-sided working-copy fallback x2; both; a HEAD fallback | every one passes 69/69 BY CONSTRUCTION -- no `--at` leg fails a show (Grok's clean sweep) | DISCLOSED (contract `:55-56` "either read or both ... no leg -- the hook never runs --at"); filed CLOSE_RULING s.5; P2 `:270` passes no `--at`.  Outside the contract, as stated: not a breach |
| index show `:447` (same form) | ledger-side fallback | M15 **2 of 69**: c8l's ctl (PASS printed, VOID wanted) + absent-PASS | legged |
| | CHANGELOG-side fallback | M16 **2 of 69**: c8m's ctl (FAIL printed) + absent-FAIL | legged |
| | both (the pre-repair joint fallback) | PRE **15 of 69** (c4d, c8h, c8i, c8j, c8k, c8l, c8m, c9e; = 11 + 2 + 2) | legged |
| | HEAD fallback on the ledger read | c8l reds: HEAD's ledger lacks `#904`, the staged CHANGELOG has the block -> FAIL, not VOID (read; Grok) | legged |
| | `or` -> `and` | one-sided failure falls through to `json.loads(None...)`: traceback rc 1, no token -> c8l/c8m red (read) | legged |
| `complete()` `:417-424` | delete the `is None` arm | `len(None)` TypeError, rc 1, no token -> c4d/c8i red (read) | legged |
| | `!=` -> `if False:` | M10 **4 of 69** (c8j x2, c8k x2) | legged |
| | `!=` -> `<` | equivalent in production (`>` has no writer: blame of N lines keys N lines) -- a result, not an escape | equivalent |
| | `== 0`; `if bl: return bl`; `+ 1 <` | **69/69, MEASURED here, three forms** | clause (e): the slice has no production writer (s.1c); disclosed by E2/E3 |

**The cells.**  Per mode: three show-fail cells + three blame cells = 6; two modes = 12; plus "ledger not JSON" (an exception path the
contract discloses) x2 = **14 cells: 9 legged** (index: c8h, c8l, c8m, c8i, c8j, the complete cell by every PASS/FAIL leg; `--at`: c4d,
c8k, the complete cell by c5/c4/c7) **+ 5 disclosed** (the three `--at` show-fail cells; not-JSON x2).  The kit's six part-3 rows are these
cells grouped by code path -- one row per guard outcome, the two modes collapsed where one function (`complete()`) serves both, the three
`--at` show cells collapsed into one disclosed row because all three are disclosed.  **The kit's enumeration is the class's true space.**
Astra's 16 adds one axis -- empty vs nonempty short -- that the body never tests; it is a SAMPLE axis (clause (e)), not a floor axis.
In the 7n-5 vocabulary: the partition on `len(bl)` is EXHAUSTED (both members rowed); the `!=` member is driven at one value (0) and its
other members have no writer -- which is what E2 writes down.

**The chain.**  Passes 2 and 3 each found a CELL of one class (a degraded read silently accepted); pass 4's finding is a within-cell
sample of a cell already rowed, reachable only by a doctored git.  The enumeration is verified, not extended: **zero floor breaches
survive adjudication**, the zero carries the denominator above (3 guards; 14 cells; 69 checks; 16 mutants + PRE + NEG; 3 escape candidates
measured; 8 record sites), the diff was delivered, both seats answered.  **The repair chain CLOSES on this pass.**

## 3. Every finding, ACCEPT / AMEND / REJECT (counted by argument, not by seat)

### 3a. GPT-6 Astra (`pass4_seats/codex_GHOSTREPAIR4_ASTRA.txt`, 4,226 B; the 221 KB `.err` is its stderr stream) -- 4 ACCEPT, 4 AMEND

| # | finding | ruling | settled by |
|---|---|---|---|
| A1 | R6(i): M15 red on c8l only (ctl + absent-PASS), M16 on c8m only (ctl + absent-FAIL), 2/69 each; PRE 11 -> 15 by two per new leg | **ACCEPT** | `MUTANTS.out`; CLOSE_RULING item 4's table (PASS / FAIL by cell); legs `:199-216` read |
| A2 | R6(ii): c8h/c8l/c8m observe their cells; the three `--at` show cells disclosed; c4d/c8i the blame failure | **ACCEPT** | read; `CHECKER_CONTROLS.out` |
| A3 | c8j/c8k build EMPTY maps and assert `dated 0 of`; no leg observes a NONEMPTY incomplete map -> "2 cells without a leg or a disclosure" | **AMEND** -- the observation is true (`dated 0 of 7`, measured); the grade is wrong: not a cell of the body's partition (s.1a), no production writer (s.1c) -> clause (e), a DISCLOSURE is owed (E2/E3), no leg | s.1; item 3-4 |
| A4 | R6(iii): `if bl: return bl` before the length guard escapes every control; measured in memory; "69/69 is a control-flow deduction, not a harness rerun" | **AMEND** -- now a HARNESS MEASUREMENT: 69 ok, 0 BAD, `ok` lines identical to base (item 3).  The mutant is real and outside the (d) enumeration: clause (e), not a floor breach | item 3 |
| A5 | 1 wrong record: CHANGELOG `:57-58` says either fallback "read a PASS"; the CHANGELOG fallback returns FAIL; the error originates in R4; correct the narrative, preserve the dated ruling | **ACCEPT** -- L4, mine (R4's text, and CLOSE_RULING's own first line says it too); E1 corrects in place quoting what it refutes; CLOSE_RULING is banked and dated and is not edited | CLOSE_RULING item 4 (`rc 1 GHOST_ROUNDS_FAIL` for the CHANGELOG-read mutant) |
| A6 | the other R4 replacements and the beyond-R4 edits are supported; counts reconcile; 9 unit hashes and 28 bank entries match; 29 bank files match their staged copies; checker code and the whole hook unchanged from OLD | **ACCEPT** -- bank identity re-derived (29 files); hook `b678efd6e315` both passes; the checker diff is 4 docstring hunks | item 5; brief part 4.1 |
| A7 | denominator: 16 cells = four show outcomes + four blame partitions {failed, empty-short, nonempty-short, complete} per mode | **AMEND** -- the body's blame partition has THREE members; the true space is 14 cells (s.2); the fourth is a clause-(e) sample axis | s.2 |
| A8 | fix first: add distinguishing nonempty-short coverage with a measured mutant kill, and correct the PASS/FAIL narrative | **AMEND** -- the record fix yes (E1); the LEG no: a row for a cell no production git writes is the "cannot hurt" addition; the disclosure (E2/E3) is the honest form | s.1c |

### 3b. Grok 4.7 (`pass4_seats/grok_GHOSTREPAIR4.txt`, 6,557 B) -- 9 ACCEPT, 1 AMEND

| # | finding | ruling | settled by |
|---|---|---|---|
| G1 | R6(i): the 2-of-69 split is settled from CLOSE_RULING item 4 because the driver `sort -u`s the BAD names; c8l's pair is ctl + absent-PASS, c8m's ctl + absent-FAIL; PRE 15 = 11 + 4; the other mutants' scores unchanged | **ACCEPT** -- `run_mutants.sh:41`; `MUTANTS.out` (M5 5, M9 1, M10 4, M14 1 unchanged) | read |
| G2 | R6(ii): each new leg sees its own cell (c8l: `rm --cached` the ledger, CHANGELOG staged, the write-back in the working ledger; c8m: `rm --cached` CHANGELOG after a reset); the `--at` disclosure; c4d/c8i; c8j/c8k; not-JSON disclosed | **ACCEPT** | `:199-216` read; `CHECKER_CONTROLS.out` |
| G3 | R6(iii): on the index guard and `complete()` no single class edit stays green (one-sided = M15/M16; both = PRE; HEAD fallback fails c8l; the length test's removal = M10) | **ACCEPT** -- for the (d) enumeration, every weakening is killed (s.2 table); the HEAD-fallback reading confirmed | s.2 |
| G4 | the `--at` show guard's working-copy fallback is a clean sweep; already disclosed ("either read or both ... no leg") and filed in CLOSE_RULING s.5; not a cell without a disclosure | **ACCEPT** -- contract `:55-56`; hook `:270` | read |
| G5 | the narrowing to `len(bl) == 0` stays green and header-dates a nonempty short map; the body does not distinguish the two shortfalls -- one cell, M10 kills its removal; counting it "would be a new cell per pass" | **AMEND** -- the grade is right and now MEASURED (69/69, item 3); but a measured escape above the floor is coverage debt that is DISCLOSED and FILED, not left unwritten (E2/E3) | item 3; s.1 |
| G6 | records: R4's replacements present at every site; hook zero hunks; the P2 block md5 in the mutant log equals the receipt's | **ACCEPT** | `MUTANTS.out:2`; `RECEIPT.md` |
| G7 | the one false record: "read a PASS" is true of the ledger cell only; "passed all 63 checks" true of both; R4's text copied exactly | **ACCEPT** (= A5) | CLOSE_RULING items 3-4 |
| G8 | the beyond-R4 edits check out (three reviews; leg or disclosure; c6a wants `dated by blame`; `--no-git` in no control; c9b exports GXLEDGER only; M7's find-text; the receipt's new sentence matches `repair2_runs/PRETEST_FINAL.summary`; 29 = 17 + 12 synth; the controls row's "both reviews'" accurate) | **ACCEPT** -- `work/repair2_runs/PRETEST_FINAL.summary` exists; 29 files counted; the controls row names c8l/c8m outside the parenthesis | read |
| G9 | not settled from the bank alone: which two checks each "2" is; md5s not recomputed (hashing refused), prefixes match | **ACCEPT** as an honest limit -- the md5s are recomputed here (checker `f20d249eeb21`, hook `b678efd6e315`, controls `14c229af13db`, PRE `999b73aa6b24`; bank 29/29) | item 5 |
| G10 | fix first -- the one record | **ACCEPT** -- records only; on the code and the bank the verdict is LAND | |

### 3c. The implementer's five edits beyond R4 (records only) -- 5 ACCEPT

| # | edit | ruling | settled by |
|---|---|---|---|
| I1 | "both reviews' legs" -> "the three reviews' legs" (round block `:69`, ledger witness, commit message `:21`) | **ACCEPT** -- REVIEW, REVIEW 2, REVIEW 3 legs exist (`run_checker_controls.sh:16-32`) | read |
| I2 | "the two reviews traced" -> "the three reviews traced" (round block `:71`) | **ACCEPT** -- M1-M3, M5-M8 (pass 2), M9-M14 (REVIEW 2), M15-M16 (REVIEW 3): 15 single-edit mutants, three reviews | `MUTANTS.out` |
| I3 | "every other cell ... with its leg" -> "... with its leg or its disclosure" (round block `:87`) | **ACCEPT** -- consistent with the contract's no-leg cells | read |
| I4 | the receipt header names `CLOSE_RULING.md`; "The builds before this one" gains one sentence | **ACCEPT** -- `RECEIPT.md:3`, `:33-34`; its claims (0 -> 0, 9 identical, FINAL rc=0 0 hard) match `work/repair2_runs/PRETEST_FINAL.summary` (Grok verified; file present) | read |
| I5 | the builder lists only M9-M14 in "six mutants ..." and M15/M16 in the closing-pass sentence (bug bracket `:26780`) | **ACCEPT** -- true of the bank and of the passes that traced them | read |

**One argument separated the seats** (A3/A4 vs G5: floor or one cell) and it is settled by the body's own tests plus a measurement neither
seat ran (s.1).  Everything else the two say agrees with the bank and with each other.

## 4. VERDICT: LAND -- the record edits the landing carries (exact old -> new; each old occurs ONCE in its staged file; the SOURCE the
## builder regenerates from is named, since the landing build re-derives the unit on the landing HEAD)

**E1 -- the false sentence (L4).**  `staged_final/CHANGELOG.md:58` (source `src/changelog_block.md`):
old: `63 checks (measured) and in its cell read a PASS from the working copy while printing read: the index; two legs, c8l and c8m`
new: `63 checks (measured) and in its cell read a verdict from the working copy -- a PASS for the ledger alone, a FAIL for CHANGELOG alone (CLOSE_RULING.md item 4; that ruling's own headline said PASS of both, and is false of the second) -- while printing read: the index; two legs, c8l and c8m`

**E1b -- the round block names its fourth pass.**  Same file, `:59` (source `src/changelog_block.md`):
old: `close the product, and the --at disclosure names both reads.  The`
new: `close the product, and the --at disclosure names both reads.  The pass on that repair (GPT-6 Astra, Grok 4.7; ruled by Fable 5.1, LAND: PASS4_RULING.md) found no floor breach: this block's account of the fallback's verdict was false (corrected above) and one clause-(e) sample is disclosed below.  The`

**E2 -- the clause-(e) disclosure.**  Same file, `:87` (source `src/changelog_block.md`):
old: `` `git show` in `--at` mode (either read) is VOID with no leg of its own; every other cell is in the docstring's contract with its leg or its disclosure.``
new: `` `git show` in `--at` mode (either read) is VOID with no leg of its own; the short-blame legs (c8j, c8k) drive the one short map real git writes -- the EMPTY map of a SHA-256 repository -- so a length guard narrowed to the empty map (len(bl) == 0, an if-bl return before the test, or a bound relaxed by one line) passes all 69 controls (measured, PASS4_RULING.md) and would date a NONEMPTY short map by its headers; no production git writes such a map (the porcelain parser's two skip branches are uniform per repository or never fire on git's own output), so it is disclosed as clause-(e) coverage debt, not legged; every other cell is in the docstring's contract with its leg or its disclosure.``

**E3 -- the filing.**  `staged_final/OUTSTANDING_BUGS.md:26782` (source `src/bugs_section.md`): after the line
`* **Owed:** Fable's REGRESS review of the round as committed, held on `ghostround`'s regress stage with its question.`
add the line
`* **Filed (clause (e), pass 4):** a NONEMPTY short blame map -- the short-blame legs drive only the empty map real git writes (a SHA-256 repository), so a length guard narrowed to the empty map passes all 69 controls (measured); no production git writes a nonempty short map (the porcelain parser's two skip branches are uniform per repository or never fire on git's own output), so it is disclosed, not legged (`regress/artifacts/ghostround/wired_20261106/PASS4_RULING.md`).`

**E4 -- the ledger's fable5 entry, true at landing.**  `tools/pipeline/ledger.json`, the `ghostround` review entry's note (source
`src/ledger_entry_review.txt`; the ledger is CRLF on disk -- write it as the builder does):
old: `the pass on its repair is drafted on that diff.`
new: `the pass on its repair (GPT-6 Astra, Grok 4.7; Fable 5.1, LAND: wired_20261106/PASS4_RULING.md) found no floor breach -- one record false and corrected, one clause-(e) sample disclosed.`

**E5 -- bank this ruling** as `regress/artifacts/ghostround/wired_20261106/PASS4_RULING.md`, byte-identical to this file, as the three
rulings before it were (`mk_receipt.py`'s CLOSE_RULING pattern): a `PASS4_RULING.md` row in the receipt's table ("the ruling on the
repair's pass, Fable 5.1, VERDICT LAND, 18 accepted, 5 amended, 0 rejected: the nonempty-short blame slice is clause (e), disclosed;
one record corrected"), its md5 and size in the "This directory" list, the receipt's `:3` history gaining "and its repair's pass
(`PASS4_RULING.md`), records only", and the receipt's "(29 files)" at `:37` -> "(30 files)".  The bank's MEASURED files do not change.

**E6 -- the commit message** `commit_ghost.msg:24` (source `src/commit_msg.txt`): old `the three rulings.` -> new `the four rulings.`

**None of E1-E6 adds a backticked row id, a `file.ext:NNN` citation or a path that will not exist at landing** (E3/E4 name the banked
copy of this file, which E5 creates).  The P2 checker reads a block's HEADER ids and backticked body spans that are row ids; none is added.

**Does the FINAL re-open?  NO -- and the distinction from my R5 is the identity pinned.**  R5 re-opened the FINAL because R3 changed the
CHECKER's bytes, which is the identity `after_final.py` pins (RECEIPT: "refuses unless its checker and block are these bytes", the checker
`f20d249eeb21`, the P2 block `9e234aa86586`).  E1-E6 touch neither, nor any measured bank file; the receipt itself says the records files
"follow that HEAD and that day", and the kit already records such deltas as fills (lines differing BEFORE -> AFTER a token replacement).
So: (i) the landing's `PRETEST.md` / receipt record the delta the same way -- "lines differing between the FINAL-tested unit and the landing
unit: CHANGELOG.md 3 (the `#587` block), OUTSTANDING_BUGS.md 1, ledger.json 1, commit_ghost.msg 1, RECEIPT.md k, PASS4_RULING.md added;
checker and P2 block 0 -> 0, byte-identical" -- with the two pinned md5s re-asserted; (ii) the live hook runs on the EXACT landing bytes at
the commit (`commit_unit2.py`: rc 4 and restore if the hook fails), which is the gate the FINAL rehearsed.  A FINAL re-run (24 min) is
PERMITTED today and is NOT OWED.  Land today; if midnight is crossed the fills move (`CALENDAR.json`), as before.

## 5. FILED, not owed

* **Rule question for the owner:** does D2's warrant (a far row discharges the branch, never the bound) extend to a relational compare
  against a VARIABLE bound such as `nlines(cb)`?  Here it is moot -- `!=` has no slack and the slice has no writer -- but the next device
  with a `len(x) < limit(y)` guard will meet it.  One line; it changes nothing in this round.
* The `--at` mixed-cell legs, the `--no-git` leg, hardening the `read:` line (CLOSE_RULING s.5) -- unchanged.
* A doctored-git leg for the nonempty-short slice: NOT filed as owed -- a row for a cell nothing writes.  If a production writer is ever
  found (a git version whose porcelain omits a committer-time, or a mixed-format output), the disclosure E2 names the edit that would then
  be a floor breach, and the leg costs one PATH shim.

## 6. Seat ledger for this stage

GPT-6 Astra (ultra) and Grok 4.7 (xhigh) **both ANSWERED** -- real content, verdict line present, denominators stated, no wall or quota
text (Astra's `cxlaunch.out` and 221 KB `.err` are its normal stderr stream).  **Tooling note, second instance:** Grok's `GHOSTREPAIR4:`
line is on line 1 but PRECEDED on that line by three streamed preamble sentences, so an anchored `^GHOSTREPAIR4:` grep misses a present
verdict; `seat_verdicts.py`'s position discriminator should be checked against this shape (same note as CLOSE_RULING s.6).  No agy, Opus
or Ollama seat was fired for this pass (the owner's roster for the repair chain: Astra and Grok, then Fable); none is counted as agreement.
This ruling is the Fable 5.1 seat.  **Where the two disagreed, both read the code correctly; the question was whether a sub-slice the
guard's own test does not distinguish is a cell, and the body's tests plus one reachability measurement answered it.**

**Honest limits.**  The GREEN/RED/FINAL outputs were read, not re-run; EQUIV's 72 read from the receipt; M15/M16's per-check split
settled by reading the legs and CLOSE_RULING item 4, not by rebuilding them here; Astra's in-memory PASS on a mocked nonempty short map
accepted by reading `:420-424` and `:307-318`, not re-run -- the behaviour is undisputed and the cell has no writer.  My own R4 wrote the
false sentence, and CLOSE_RULING's first line carries the same overstatement ("reading a PASS from the working copy in its cell" -- true of
the ledger cell, false of the CHANGELOG cell, which FAILs); it is corrected here by quotation and not edited in place, as REPAIR_RULING was
not, because that file is banked and dated.

FABLEGHOSTREPAIR4: 18 ACCEPTED 5 AMENDED 0 REJECTED VERDICT:LAND -- zero floor breaches survive adjudication, with the denominator (3 guards, 14 read/blame cells = 9 legged + 5 disclosed, 69 checks, 16 mutants + PRE + NEG, 3 escape candidates MEASURED here through the bank's own harness, 8 record sites): Astra's "nonempty-short blame" cell is a split the guarded body never makes (`complete()` tests `is None` and `len(bl) != nlines(cb)`, never emptiness) and no production git writes such a map (measured, porcelain headers stay 40-hex even under blame.markIgnoredLines), so the three single edits that pass 69/69 (`if bl: return bl`, `len(bl) == 0`, a bound relaxed by one line) are clause (e) -- DISCLOSED in the records, not legged; the one wrong record is my own R4's "read a PASS", false of the CHANGELOG cell (it FAILs, CLOSE_RULING item 4) -- corrected in place; every edit is records-only, the checker (f20d249eeb21) and P2 block (9e234aa86586) the FINAL pinned are untouched, so the FINAL is NOT re-opened and the live hook gates the exact bytes at the commit
