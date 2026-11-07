FABLE_LIVE_20261106_GHOST
# CHECKPOINT -- 2026-11-04 17:0x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)

# RULING -- `ghostround` (#585 as built; #586 once rebuilt), REGRESS stage, Fable 5.1, 2026-11-06

**Subject.** `check_ghost_rounds.py` wired into `tools/precommit_check.sh` as HARD section P2 (owner ruling
2026-11-06, cutoff 2026-11-05): a ROUND block's header-named rows and its named `in work` rows must be
`closed`/`dropped` or name the round.  Kit `_scratchpad/wghost/landing/` (PRETEST.md, REVIEW_BRIEF_pass2.md,
`staged_final/`, `wired/`).  Seats read: GPT-6 Astra (`astra_ghost/codex_GHOSTP2.txt`, 9,812 B, a real answer --
the .err was not needed), agy on Gemini 4 Argon (`agy_ghost.txt`, 29,585 B), Grok 4.7 (`grok_ghost.txt`, 7,689 B).

**What I did.** Read the staged checker (`staged_final/tools/pipeline/check_ghost_rounds.py`, 450 lines), the
staged hook's section P2 (`staged_final/tools/precommit_check.sh:242-270`) and all of its missing-checker
branches, the bank (`wired/run_checker_controls.sh`, `CHECKER_CONTROLS.out`, `RECEIPT.md`, `SYNTHETIC_BLOCK.md`,
`pretest_ghost.py.txt`), the staged records, HEAD's hook, `check_fable_queue.py`, `check_stage_panels.py`,
`gen_codex_wall.py`, the census (`DECISION.md`, `census.out`, `replay_class.out`), and `git log`.  ONE read-only
measurement: `git blame --porcelain --contents <tmp> -- CHANGELOG.md` on HEAD's CHANGELOG with the `#557` header
edited by one space (unmodified: `e1871fa5...`; edited: the all-zero sha).  No build, gate, panel, checker run or
control ran; `git status` unchanged (948 porcelain lines before and after).  Line numbers below are the STAGED
files' unless marked HEAD.

**Baseline fact every reader of this ruling needs:** real HEAD is `54613aa1`, `#585 fbsdrampair` -- the kit's
number is TAKEN.  The kit already requires a rebuild on the landing HEAD (PRETEST.md steps 1-2; `build_ghost.py`
derives the number; `pretest_ghost.py.txt:344` derives the synthetic block's as highest+1).  So a rebuild and
re-pretest are owed REGARDLESS of this ruling, which is why the code repairs below cost little extra.

## A. Every point, ACCEPT / REJECT, with what decides it

Legend: **[all]** = the three seats agree; **[A]** Astra, **[G]** grok, **[Y]** agy.

### A1. The premise audit (brief section 3)

| # | premise / claim | ruling | decided by |
|---|---|---|---|
| 1 | **QP1** -- the hook's `git show :path` reads the index being committed in all three commit paths **[all: TRUE]**; agy adds three "holes" | **ACCEPT** TRUE as the mechanism: `git()` at checker `:182-188` runs `subprocess.run` with no `env=`, so `GIT_INDEX_FILE` is inherited, and the hook (`.git/hooks/pre-commit`) runs `bash tools/precommit_check.sh` in the same environment.  Not measured under a hook by anyone, including me -- see owed control (c) in §B. | agy's holes 1 and 2 are D2 and D3 below (ACCEPTED there).  Hole 3 (a hand run before `git add` reads HEAD's index while H and P read the working tree): **REJECT** as a defect -- that is the stated design, the same narrowing sections A/B make (CHANGELOG `:23-24`), and `--worktree` exists for the other reading (checker `:37`). |
| 2 | **QP2** -- editing an OLD header line re-dates the block to today; a NEW block never gets an old date while blame works **[all agree on the mechanism]** | **ACCEPT, MEASURED HERE**: `#557`'s header (HEAD CHANGELOG line 4332) blames to `e1871fa5` unmodified and to `0000...` after a one-space edit; `porcelain_dates` `:217-218` maps that to TODAY; `landed = bdate or ...` `:282` prefers it; `2026-11-06 > 2026-11-05`.  The census says so in its own words (`census_20261106/DECISION.md:170-171`: "Editing an old block's header line moves its blame date past the cutoff; body edits do not"). | The DIRECTION matters and Astra states it right: an edited old block becomes newly ENFORCED, not exempt; the 13 archived hits at `2632277f` are all `in work` (`census.out:28`), i.e. real ghosts whose write-back is owed anyway.  This is a design with a bounded blast radius, not a code defect -- but the hook comment that denies it is a WRONG RECORD (§A4 R2).  Astra's D5 redesign ("preserve block landing provenance"): **REJECT as owed** -- filed. |
| 3 | **QP3** -- a new block can be written so its number is missed (unbackticked `# #586`, date-first, `## `#586`` at the top of the file) or so it reads as RECORDS **[all: TRUE]** | **ACCEPT** as true of the parser: `OWN_RNUM` `:93-97`, `H2_BLOCK` `:104-107`, `RECORDS` `:114-118`.  All DISCLOSED: docstring `:27-28` ("A ROUND block with no number of its own falls back to the date rule"), `:99-100` (H2 is a block level only in the older stretch), CHANGELOG `:50-53`. | Not a floor matter; clause (e).  agy's option 2 (fail a post-cutoff ROUND block with no extractable number) is a real tightening and is FILED as an owner question -- the fallback exists for the 16 legitimately unnumbered blocks at `2632277f`. |
| 4 | **QP4** -- rows are cited in shapes `span_ids`/`header_ids` miss (bare after `--`, `rowA and rowB`, paths, `/`-separated groups) **[all: TRUE]** | **ACCEPT** as true: `:149-174`.  Disclosed at `:41-45` as `check_bugfile_sync.py`'s idiom, with the 31 path-only pairs counted and named as unchecked (brief QP4; grok and Astra both reproduce the 31). | Clause (e).  Astra's `#534 (stagetokens repair)` example is a correct instance of the disclosed limit. |
| 5 | **QP5** -- "header-named or `in work`" covering all 11 ghosts is a property of the SAMPLE **[all]** | **ACCEPT**: `replay_class.out` -- header-only 6/11, `in work`-only 10/11 (misses `sgirergbroundtrip`, which shipped from `open`), union 11/11.  Disclosed at `:28-29` and CHANGELOG `:50-51`. | agy's hybrid scope (body-named `open`/`held` rows in blocks whose header names nothing) FILED. |
| 6 | **QP6** -- P2 depends on no earlier section's state **[all, in substance; polarity differs]** | **ACCEPT**: `say/bad/soft/good/warn` are defined at hook `:37-46`; P2 `:257-270` assigns its own `out`, reads no `CHANGED`, and `bad` feeds the shared `fail`.  The only inherited dependency is the process ENVIRONMENT -- D2 below. | Astra and agy both found no preceding section setting the `GX*` names. |
| 7 | grok's month arithmetic (54+55+22+10 = 141; 6+12+2+0 = 20; Oct+Nov 32 -> 2) | **ACCEPT** as consistent with `replay_class.out` ("landing commits failed: 20, with a real gap: 13, on references/filings only: 7") and CHANGELOG `:15-16`.  The tsv was not re-summed here. | |
| 8 | Astra's 40 = 30 `ctl` + 10 `absent` = 6+6+4+9+3+2+5+5; 72 = 4 revisions x 3 cutoffs x 6 option sets; 16 unnumbered; 31 path-only | **ACCEPT**: counted from `run_checker_controls.sh:38-130`; `EQUIV.out` ends `72 comparisons, 0 DIFFERENT`; `census.out:7` says 16. | |

### A2. Code defects raised

| # | claim | ruling | decided by |
|---|---|---|---|
| D1 | missing checker -> `warn` is wrong for a HARD section; make it `bad` **[A as defect; Y as option 5; G as a record point only]** | **REJECT as a code defect owed in-round.**  The staged hook has **16 `warn`-on-missing (P2 included) and 5 `bad`-on-missing** (`grep -cE '^\s*(warn|bad) "[a-z_]+\.py MISSING'`; the fifth `bad` is `check_wsl_dollar.py` at `:1069`, an `else` form).  HARD sections U, Q, K, I, H and G all take `warn` here, so "HARD => bad" is not the house rule; the class repair is the warnnotfail kit, in flight and measured against this unit (`WWARN_INTERPLAY.out`: wwarn converts every soft-on-missing branch, P2's included; its `N_SOFT` pin moves 15 -> 16). | The RECORD half is R1 (§A4), ACCEPTED. |
| D2 | P2 inherits `GXLEDGER`, `GXCHANGELOG`, `GXSEC`, `GXGHOST_CUTOFF`, `GXGHOST_TODAY`; Q2 clears its analogues **[A, Y]** | **ACCEPT.**  Checker `:61-69` reads all five; `load()` `:377` skips the index read whenever `GXLEDGER` or `GXCHANGELOG` is set; HEAD hook `:552` already does `env -u GXDOMAIN_BASELINE -u GXLEDGER python "$CED"` for section Q2 -- the project has decided this hazard is worth one `env -u`.  P2 `:261` does not. | Owed, L1 (§B item 2). |
| D3 | a failed `git show :path` in index mode silently reads the WORKING copies and can exit 0; the `note:` is hidden by P2's `grep GHOST_ROUNDS_PASS` **[all]** | **ACCEPT.**  `:377-386`: `print("  note: ...")` then falls through to `json.load(LEDGER)`/`read_text(CHANGELOG)`; P2 `:262` prints only the PASS line.  Contradicts the checker's own `:49` ("A check that read nothing is not a pass") and the claim at `:34` / hook `:252`. | Owed, L1 (§B item 1).  Three seats found it independently. |
| D4 | a failed `git blame` returns `{}` and the header date is then trusted, so a new block with a copy-pasted `(2026-11-05)` header would be ARCHIVED **[A, Y]** | **ACCEPT.**  `blame_contents` `:243` returns `{}` on `rc != 0`; `:282` then takes the header date.  `--no-git` `:38` is the EXPLICIT mode for header-only dating; index mode has no business degrading to it silently. | Owed, L1 (§B item 1, same repair). |
| D5 | header blame measures the LAST edit, not the landing; redesign provenance **[A]** | **REJECT as owed** (see QP2).  FILED with the measurement attached. | |
| -- | P2 accepts rc 0 without the PASS token **[A declined to count it; Y counts it]** | **ACCEPT** as a one-token belt on the line already being edited: `:261-262`.  The bank's own rule is "every control greps the verdict TOKEN, never the exit code alone" (`run_checker_controls.sh:12`); the hook should obey it on the PASS side too. | Folded into §B item 2. |
| -- | agy QP2(b3): a new block with a past header date widens `>= date` in `mentions_round` | **REJECT as a defect**: the header date is the block's own stated date by design (`:76-81`); the hazard needs a wrong header date AND a pre-round entry naming a round that did not yet exist. | |

### A3. "Smallest edit that still passes" (brief Q2) -- each is a control gap, and the controls re-run anyway

| # | mutant | ruling | decided by |
|---|---|---|---|
| M1 | **[A]** `--rule=date` on P2's line: GREEN green, RED red, 40/40 green | **ACCEPT by reading** (not measured): the 40 bypass P2 (`run_checker_controls.sh:21` invokes the checker directly); RED's row `bugfilereverse` has ONE entry, dated `2026-09-17` (staged ledger), so the date rule fails it too.  The hook-level ARGUMENTS are pinned by nothing.  Owed: RED's synthetic row must carry an entry dated the block's date, so RED discriminates `mention` from `date` at hook level -- zero extra runs, since RED re-runs for the renumbering. | L1, §B item 3(d). |
| M2 | **[Y edit A]** `landed = date if src == "header" else (bdate or UNDATED)` | **ACCEPT by reading**: c6a/c8a headers are UNDATED (`run_checker_controls.sh:81,107`) so `bdate` still wins there; c1a-c2c run in file mode outside a repo where `blame_file` `:246-252` returns `{}`, so they already rest on the header date; RED's header date is `2026-11-06 > cutoff`.  Nothing pins the precedence for the ONLY shape that occurs in practice -- a dated header.  Owed: a staged block with a pre-cutoff header date must FAIL with `landed` TODAY. | L1, §B item 3(a). |
| M3 | **[Y edit B]** drop `(e.get("date") or "") >= date` in `mentions_round` `:319` | **ACCEPT by reading**: every write-back control puts `#NNN` in `state_note` (`:87,123`), none in a pre-round entry.  Owed: a row whose only `#NNN` is in an entry dated BEFORE the block must FAIL. | L1, §B item 3(e). |
| M4 | **[Y edit C]** disable multi-row spans or `SUBJECT_AFTER_MARKER` | **REJECT as established.**  c5 pins EXACT archived counts over the real file at `2632277f` (13 / 184 / 268, `run_checker_controls.sh:72-74`), which contains `Round #504 sgirandompixel`-shape headers (`:44`) and multi-row spans; agy did not compute those counts under the edit and neither did I.  A prediction over real-file counts is not "every control stays green". | |
| M5 | **[G]** drop `GIT_INDEX_FILE` from the env in `git()` -- `commit -a`/partial commits invisible, all 40 + GREEN/RED unchanged | **ACCEPT the gap**: no leg sets `GIT_INDEX_FILE` (`:100-130`), GREEN/RED were `git add`ed into the real index.  The landing path here is `commit_unit2.py` (plain index), so the risk is low -- but QP1 was RATIFIED from git's contract by all three seats and measured by none; one leg converts a ratified premise into a test. | L1, §B item 3(c). |
| M6 | **[G]** `TERMINAL = ("closed", "dropped", "held")` | **ACCEPT the gap**: `synth_ledger.json` has NO `held` row (states: open x4, in work, closed); the 13 archived hits are all `in work` (`census.out:28`); RED's row is `open`.  The real ledger has 99 `held` rows and 60 (block, held row) pairs at `2632277f` (`census.out:17`). | L1, §B item 3(b). |
| -- | **[G]** "5 controls that cannot fail" = c8a-e | **REJECT the label**: each of c8a-e carries a discriminating expectation and c8a/c8b differ by exactly the index-vs-worktree bit.  They CAN fail; they do not COVER M5.  That is a gap (accepted as M5), not a check-that-cannot-fail. | |
| -- | **[A]** `run_checker_controls.sh` exits 0 whatever `bad` is | **ACCEPT**: `:133-134` end in `echo`; no `exit`.  The banked OUTPUT (`CONTROLS: 40 ok, 0 BAD`, every row `ok`) is the evidence and I read it line by line -- but a runner whose rc cannot go red is the carrier's "a count printed beside an action is not a check" shape. | L1, one line, §B item 3(f). |
| -- | **[A]** `pretest_ghost.py.txt` asserts nothing (`:359-365`, `:402`) | **ACCEPT the observation; not owed.**  The driver's product is the summary with `PRECOMMIT_PASS 0 hard` / `rc=` tokens, which is what the receipt and this ruling read.  FILED as hygiene for `after_final.py`. | |

### A4. Records (brief Q4)

| # | sentence | ruling | decided by |
|---|---|---|---|
| R1 | CHANGELOG `:28-29`: a missing checker "takes this file's form for every other checker, `warn`" **[all]** | **ACCEPT -- FALSE.**  15 of the 20 other branches `warn`; 5 `bad` (`:576, :757, :789, :961, :1069`).  L4. | |
| R2 | hook `:252-254` / checker `:34-38` / CHANGELOG `:23`: "reads what is being committed", "so no block already in the file can fail" **[A, Y on the first; Y, A on the second]** | **ACCEPT -- both overstate.**  The first is true only once D3/D4 fail closed (an index-read or blame failure today reads something else and can pass).  The second is MEASURED FALSE above: a block already in the file fails once its header line is edited.  L4 -- qualify both, quoting what is replaced. | |
| R3 | README `:29`, `check_probe_wiring.py:3989-3990`, bug-file bracket `:756`: "closed or name the round" omits `dropped` **[G: README; Y: all three]** | **ACCEPT -- `TERMINAL = ("closed", "dropped")` `:72`.**  The bug-file section `:26737` and the ledger `state_note` say "closed or dropped" and match.  L4 at the three sites. | |
| R4 | **[Y]** counts stated without their members (11 rows, 2 of 11, 20/13/7, 14, 16, 13) | **REJECT.**  The count rule asks that a count NAME ITS DERIVER or carry method and date; every one of these names `census_20261106/replay_class.tsv`, `replay.out`, `DECISION.md`, `EQUIV.out` or `CHECKER_CONTROLS.out` (CHANGELOG `:6-16, :26, :35-43`).  Listing every member inline is not the rule. | |
| R5 | **[Y]** fix hint "name the round (#NNN) in its state_note or an entry" vs seven fields and `Round NNN` | **REJECT.**  A fix hint names sufficient common forms; the full rule is at `:14-17` and CHANGELOG `:15` names `Round NNN`.  Not false of the code. | |
| R6 | **[A, Y]** `#585` is taken; the checker's md5 (`999b73aa6b24`), `RECEIPT.md:66`, `CHECKER_CONTROLS.out:1` and `SYNTHETIC_BLOCK.md` (`#586`) go stale on renumbering; never install `staged_final` wholesale (it lacks HEAD's `fbsdramwidth`/`fbsdramwrites` rows) | **ACCEPT** (`git log`: `54613aa1 #585 fbsdrampair`).  `RECEIPT.md:72` says the checker is byte-identical only at the same number; the FINAL run regenerates the bank; the driver derives the synthetic number.  A PROCEDURE precondition the kit already states, not a defect in it. | |
| R7 | **[G]** 40, 72, 53 queue ids, the MANIFEST sentence all match their members | **ACCEPT** (counted above; `fable_queue.md` not re-counted here). | |

### A5. The ledger row (brief Q5) -- **[all]**

**ACCEPT: keep Fable's REGRESS question in `hold_question` and the `[HELD AWAITING SEAT: fable5]` regress
entry.**  `check_fable_queue.py:150-154` (rule 3) refuses a `closed` row with `commits` and no `regress` entry
unless it is queued -- so once the hash follow-up fills `commits`, an empty field and no hold would red section I;
`check_stage_panels.py:64-65` keeps `regress` out of CLOSED-WHILE-HELD (`FABLE_ONLY = {"regress"}`);
`gen_codex_wall.py:137` derives the queue from the marker; and a held stage must carry its question
(`check_stage_panels.py`'s `hold_question` rule).  The owner's wiring question is answered by the ruling and
would misrepresent a settled matter if left.  The `#584` form is the right precedent.

## B. VERDICT: **HOLD**

Not for the seats' disclosed-limit findings (those are clause (e) and filed), but because three seats found the
same fail-open path in the mandatory read, two found the same unguarded environment, five one-line mutants of
predicates the fix DEPENDS ON were traced past every control, and the unit must be rebuilt and re-pretested on
`54613aa1` in any case.  Every item below is pre-ship construction (L1) or a wrong record (L4); none reopens
shipped material.

| # | owed | grade | the change |
|---|---|---|---|
| 1 | **Index mode fails CLOSED** | L1 (code) | In `load()` `:377-386`: when neither `--worktree` nor a `GX*` file override is in force, a failed `git show :<path>` is `GHOST_ROUNDS_VOID` (exit 2) -- no working-copy fallback, no `note:`.  In `blame_contents` `:243` (and `blame_rev` `:231`): `rc != 0` returns a sentinel that index/`--at` mode turns into VOID; only `--no-git` dates by headers.  P2's `else` branch `:267-269` already makes VOID a hard FAIL.  Add legs: `c8h_index_unreadable_VOID` (run with a bogus `GIT_INDEX_FILE` so `git show :path` fails -> exit 2, token VOID, `absent PASS`). |
| 2 | **P2's line** | L1 (hook) | `:261`: `elif out=$(env -u GXLEDGER -u GXCHANGELOG -u GXSEC -u GXGHOST_CUTOFF -u GXGHOST_TODAY python "$GHOSTCHK" 2>&1) && printf '%s' "$out" \| grep -q '^GHOST_ROUNDS_PASS'; then` -- Q2's `:552` form plus the token.  `bash -n`; the wwarn interplay re-checked (`wwarn_interplay.py`) since the anchor line changes. |
| 3 | **Controls** (`run_checker_controls.sh`, re-run in seconds; RED re-runs anyway) | L1 (detector material) | (a) `c8f_staged_dated_FAIL`: a staged block with header date `2026-11-01` -> FAIL, `landed 2026-11-06` (pins `:282`; M2).  (b) `c1d_held_header_FAIL`: `synth_ledger.json` gains a `held` row named in a header with no write-back -> FAIL (pins `:72`; M6).  (c) `c8g_tempindex_FAIL`: `cp .git/index tmp; GIT_INDEX_FILE=tmp git add CHANGELOG.md` with the new block, then the checker under `GIT_INDEX_FILE=tmp` -> FAIL and `read: the index of`; without it -> PASS (measures QP1; M5).  (d) RED's synthetic row chosen or staged so it carries an entry dated the block's date and no `#NNN`, so the hook-level rule is discriminated (M1) -- `pretest_ghost.py:347`'s selection gains that clause.  (e) `c1e_prior_entry_FAIL`: a row whose only `#NNN` sits in an entry dated before the block -> FAIL (pins `:319`; M3).  (f) `:134`: `exit $(( bad > 0 ))` after `CONTROLS_DONE`.  Each new leg is a MEASUREMENT of a mutant that was only predicted here; write the mutant text and its score beside the leg. |
| 4 | **Records** | L4 | R1: CHANGELOG `:28-29` -> "the `warn` form that 15 of the 20 other missing-checker branches take (5 take `bad`); the warnnotfail kit converts the class".  R2: hook `:252-254` and checker `:31-38` -> "...reads the INDEX, and is VOID -- a hard FAIL -- if the index or blame cannot be read; forward-only from CUTOFF, so a block already in the file cannot fail UNLESS its header line is edited, which re-dates it to the editing commit and then demands the write-back its rows owe (measured: `#557`'s header blames `e1871fa5` unmodified and the all-zero sha after a one-space edit)".  R3: `dropped` added at README `:29`, `check_probe_wiring.py:3989`, bug file `:756`.  CHANGELOG `:50-53` ("Not checked") gains: edits to an archived block's header re-date it; a round block written at H2 with a backticked number is not parsed as a block. |
| 5 | **Rebuild on the real HEAD and re-pretest** | procedure | PRETEST.md steps 1-2 as written: `build_ghost.py` on `54613aa1` (number -> #586; the bank's md5s regenerate; the synthetic block -> #587), `launch_final.sh` (plus a RED run, because item 3(d) changes RED's shape), `after_final.py`.  Owner's re-date of the four Alpha/LCA exemptions dated 2026-11-06 is needed for any landing on or after 2026-11-07 (PRETEST.md dependency 2). |
| 6 | **The repaired unit owes one pass 2 on its diff** | rule | Carrier repair-chain rule: one pass per floor-bound diff, closing on the first VALID pass with zero breaches AND a denominator (which cells, which mutants were swept).  Scope effort to the repair hunks; ask the floor question of the composite. |

**FILED, not owed** (each is disclosed in the unit or is a design alternative; carry the seat's wording as
provenance): agy's option 2 (fail an unnumbered post-cutoff ROUND block) -- an OWNER question, since it
tightens a disclosed fallback; agy's hybrid scope for body-named `open`/`held` rows; agy's diff-vs-HEAD
alternative to blame; Astra's D5 landing-provenance redesign; the pretest driver asserting its own verdict;
QP3/QP4 citation shapes beyond the `check_bugfile_sync.py` idiom.

**Agreements worth recording:** QP1 TRUE, QP2 mechanism, QP3-QP4 disclosed, QP5 sample property, QP6 no
sibling dependency, R1 false, D3 fail-open, and the ledger row -- all three seats, independently, and each
verified here against the files rather than counted.  The one place the seats talked past each other was the
polarity of QP6 (Astra TRUE / grok FALSE / agy both) while saying the same thing.

**Seat ledger for this stage:** Astra, agy and grok ANSWERED (real content, verdict line first, no wall text);
this ruling is the Fable 5.1 seat.  No Opus seat, no Ollama seats were fired for this pass (coordinator's
roster), and none is counted as agreement.

FABLEGHOST: 57 ACCEPTED 8 REJECTED VERDICT:HOLD
