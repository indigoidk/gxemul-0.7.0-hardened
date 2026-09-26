# #551e's enumeration-verifying pass -- EVERY SEAT'S FINDINGS, WITH MY DISPOSITION ON EACH (for the adjudication)

Pass: `pass551e_brief.md` (30 KB: the contract, the self-check with the call-count pin, the trailer, the d->e diffs and
`measured/run551e.out` inlined).  Answered: **agy** SHIP WITH CHANGES; **glm** SHIP WITH CHANGES; **minimax** SHIP WITH
CHANGES; **kimi-k3:cloud** SHIP WITH CHANGES; **deepseek** DO NOT SHIP; **grok** (panel) DO NOT SHIP; the **dedicated
grok** job DO NOT SHIP; the **Opus 5.5** measuring seat: see the OPUS section at the end.  **Codex (GPT-6 Astra) and the
kimi CLI walled** (usage limits) -- seat failures, not agreement.  Panel dir `_scratchpad/panel_20260925_182627/`
(durable copy to follow in `panels/`).

The adjudication's stop rule for this pass (Fable, `pass551d/fable5_pass551d.md`): *"it closes on a valid zero where a
composite inside the four named classes is a contract fact, not a finding; only a single edit outside the four classes,
or a class the contract does not name, reopens."*

## FINDINGS

* **H1 -- THE CALL-COUNT PIN CHECKS TWO WRITABLE COUNTERS, NOT THE CALLS.**  Five seats, independently:
  - **grok (panel) and the dedicated grok: ONE edit** -- a statement at the top of `row_ring_occupancy_sound()` that, on
    its first entry, adds 24 to `chk_calls` and to `rows`, registers the function with `atexit`, and returns.  The last
    self-check then sees 24 and 8, the trailer prints `0 failures` and PASS, and the 24 real `chk()` calls run after
    `main` returns.  Walked, not compiled.  Every gate-2 check reads the whole log, so rows printed after the token
    still satisfy the presence checks, and the lane's row is inline and unmoved.
  - **deepseek, glm, minimax: a composite** -- the covered rows moved past the verdict plus 24 dummy `chk()` calls added
    before the last self-check (each also a `rows ++`, so the identity row needs no re-pin).
  - **kimi-k3: a composite** -- the move plus `chk_calls = 24;` before `selfcheck("last")`, with the identity re-pinned.
  So the new sentences **"Nor is moving the covered rows past the verdict: the LAST run requires chk() 24 and row_cmp()
  8 calls"** (block comment) and **"so is moving the covered rows past the verdict"** (gate bullet) are false as
  universals: the pin catches a BARE move (`move_repin`, measured red), not one with the counts forged.
  **MY DISPOSITION: THIS REOPENS, by the stop rule's letter** -- the `atexit` form is one edit outside the four classes
  (it touches no comparator, no feed operand, no trailer text, no self-check line), and the counter-forging composites
  are a class the contract does not name.  **The repair is the contract, not another mechanism**, for the reason kimi-k3
  gave and glm put generally: every in-file check reads file-scope state (the two tallies, the call counts, `rows`,
  `sc_g`, `sc_first_bad`) that any edit in the file can write, and runs rows whose order and timing any edit can change
  -- *"in-file evidence is either stored (forgeable by a write) or computed (erasable by an inlining)"*.  I propose the
  contract state that boundary ONCE, as the class, instead of enumerating composites: the self-check detects an INERT
  or NARROWED comparator; an edit that writes the state the checks read, or reorders or defers the rows, is disclosed,
  and its close is gate-side (`wdcidlane`).
* **H2 -- CAN THE TRAILER BE PINNED IN-FILE? (the adjudication's caution, asked exactly).**  **grok (panel) and the
  dedicated grok: YES** -- a third counter (`cmp_sticky` / `cmp_latch`) incremented beside `cmp_fails` in both
  comparators and read at TWO sites (a self-check line matching `[0-9]+ failures`, or two `atexit` handlers), so one
  inlining edit removes one reader and the named reset (`failures = cmp_fails = 0`) does not write the third counter.
  **kimi-k3: YES BY THE LETTER, NO BY THE CLASS** -- *"the reset's target set is the attacker's free parameter"*:
  `if (failures == cmp_fails) failures = cmp_fails = cmp_f2 = 0;` is still one inserted conditional reset.  **agy,
  minimax: NO** (the single-call-site argument).  **glm: NO, for a stronger reason** -- the conditional reset is a no-op
  on BOTH logs gate 2 reads (pristine: 0 == 0; the self-mutant: 1 != 0), so the edited file is output-identical to the
  healthy one on every input gate 2 has, and nothing in-file can observe a difference there.
  **MY DISPOSITION: kimi-k3 and glm are right about the class, grok about the letter.**  The caution named one reset;
  the reset it named is one member of "write the state the checks read", and any stored witness is in that state.  I
  propose the contract say "no in-file check closes this: whatever it reads, an edit can write" rather than "no in-file
  probe can pin a single call site", which grok's two-reader construction does falsify as worded.
* **H3 -- "conditional on their equality, anywhere" is false** (grok): before the covered rows the tallies are equal and
  zero, so a reset there fires harmlessly and later increments stand.  It is green AFTER the covered rows' failures and
  while no inline row has split the tallies -- which is why it is green at the trailer on drqring and w57hi and red on
  the self-mutant.  **ACCEPTED** -- wording.
* **H4 -- the trailer class's description is wrong about what must be consistent** (grok, kimi-k3): gate 2 discards the
  exit status; `grep -c WDC_IDENTIFY_PASS` accepts a log that ALSO carries WDC_IDENTIFY_FAIL; the lane needs FAIL
  present, not PASS absent.  So ONE trailer edit -- print `0 failures`, PASS and FAIL -- is green on a covered defect and
  keeps the lane.  It is inside class (3), so it does not reopen, but "today two coordinated edits, each red alone" is
  false.  **ACCEPTED** -- wording; and **FILE** a gate-side check that a log carries exactly one of the two tokens
  (cheap, but a gate change with its own controls).
* **H5 -- my brief's "sixteen named rows" is false** (agy, grok): the wdc block has 69 named-row presence checks, plus
  the PASS-count and `high byte` checks (my count, 71 `== "1"` checks in the block; agy counted 70, the dedicated grok 68
  presence checks).  No conclusion rested on it -- moved rows still print their named lines -- but it came from my
  #551d packet and went unchecked for a pass.  **ACCEPTED** -- records.
* **H6 -- drqring's two failing rows are the VERDICT-HANDED `chk()` rows** (`cond ? 1 : 0`, the DRQ status), not the 16
  data comparisons (grok).  My briefs called drqring "two chk() rows fail", true but it is not a covered-comparison
  defect in the contract's sense; Opus's `dropold` variant is the one that fails covered comparisons.  **ACCEPTED** --
  records; the measurements' conclusions stand (a chk()-level edit silences both kinds).
* **H7 -- the measurement caption "rc=1 / 0 PASS is red" fights the exit-status premise** (grok, glm):
  `nopin_move_repin` on drqring is rc=1 but prints 0 failures and one PASS -- gate-2 GREEN.  **ACCEPTED** -- the caption
  becomes "red = no PASS token or a nonzero printed count; rc is not a gate-2 input".
* **H8 -- "the failure arm does not, and forces one failure" is imprecise** (kimi-k3): the probe-failure arm forces one;
  the "first run did not run, or did not pass" arm forces nothing itself -- the trailer's `!sc_g` line counts it.
  **ACCEPTED** -- wording.
* **H9 -- "requires every covered call to have run before it (chk() 24, row_cmp() 8)"** counts calls, and 24 includes the
  8 verdict-handed ones (kimi-k3).  **ACCEPTED** -- "requires the call counts".  (Its other note-line claim -- "0/0 on the
  first run" -- is REJECTED: the note line prints only on the last run, after the first run's early return.)
* **H10 -- the pin also catches conditional call suppression** (`if (got == want) chk(...)` with no else: the count drops
  on any input where the row would fail) (glm).  **ACCEPTED** -- one sentence, so a later reader does not undo it.
* **H11 -- minimax: the self-mutant lane catches the dummy-call composite.**  **REJECTED**: the lane's row
  (`row_wide_geometry`) is not moved, so its failure still lands before the token; the lane stays green.  glm and grok
  walked the same shape and reached the same conclusion as mine.
* **H12 -- minimax: `MINE_phase selfmut` is not measured.**  **ACCEPTED** for the next measurement (a phase key inside a
  comparator cannot reach the inline geometry row, so it cannot turn the lane's FAIL into PASS; measuring it is cheap).
* **H13 -- `MINE_nosc` looks irreproducible from the inlined code** (kimi-k3).  **EXPLAINED**: the variant also removes
  `sc_g` from the verdict, the return and the trailer's backstop (its definition is in `xform551e.py`), which is why it
  prints PASS with no G line and no token -- gate 2's G and H rows are what catch it.

## DISAGREEMENTS

* **D1 -- H2: is the trailer closable in-file?**  grok (both jobs): yes, a twice-read third counter survives the named
  reset and any one inlining.  kimi-k3 and glm: only against a fixed reset; the reset's targets are free.  **My ruling:
  kimi-k3 and glm** -- see H2.
* **D2 -- H1: reopen, or absorb by amendment?**  glm: it reopens under the stop rule's letter.  kimi-k3: absorb it into
  class (3) by naming the mechanism ("write what the verdict reads"), since the contract already believes it about two
  tallies.  **My ruling: it reopens by the letter, and the repair is the amendment** -- a CONTRACT-ONLY #551f (no code
  change), stated as the general class rather than as more members.  Whether a comment-only #551f owes another panel
  pass is the question I most want ruled on.
* **D3 -- deepseek: DO NOT SHIP** (the dummy-call composite).  **My ruling:** real, a composite, and inside the
  general class H1 proposes -- no code change; the contract amendment.

## WHAT IS STILL OWED, AND WHERE I MIGHT BE FOOLING MYSELF

* **None of H1's shapes is MEASURED.**  Both groks walked the `atexit` form without compiling; it is plausible (the
  deferred body rebuilds its own device and `stdout` is unbuffered) but a crash in the deferred body before a named
  label prints would make it red.  **I will measure it (and kimi-k3's counter write, and the dummy calls) before the
  amendment ships**, so the contract's new class carries measured members.
* The pattern across #551b-e is five passes of an adversary with full control of the source finding a new way to write
  or reorder what the checks read.  I am proposing to stop chasing members and state the boundary.  If that is the
  wrong reading of the carrier's class-closure rule, say what closes the class instead.
* Astra (codex GPT-6 Astra) has not seen #551b-e; nothing commits before it confirms after 07:01.
* Accepted: H3-H10, H12 (and H1/H2 as dispositions).  Rejected: H9's second half, H11.  Explained: H13.

## OPUS (the measuring seat, `opus5_pass551e.md`; clean opus-5-5; 424 builds, 51 shapes, table
## `opus551_measured_e/analyze7.out`)

* **J1 -- MEASURED: the unnamed class is real and green.**  `E_movefake` (the covered `chk()` calls moved past the verdict
  + 24 `chk("x", 0, 0)` before the last self-check: two edits) is GREEN on dropold and drqring, the identity row still
  128; `E_movefake_row` (the same with the `row()` block and 8 fed `row_cmp()` calls) GREEN on w57hi; `E_countforge`
  (`chk_calls = 24;` + the move + a re-pin: three edits) GREEN on dropold and drqring.  All 24 single edits outside the
  classes still red; `move_repin` red everywhere; #551e whole-log identical to #551d on nine device variants.  **So H1
  is MEASURED, and "Nor is moving the covered rows past the verdict" is measured false** -- Opus: *"this class is not
  merely unnamed -- it is denied.  Under the stop rule it reopens the chain."*
* **J2 -- MEASURED: a pin ON the trailer does not survive.**  A verdict function the last self-check probes at (0,0,1),
  (1,0,1), (0,1,1), (0,0,0), used for the token and the exit status: one inserted conditional reset -- green on all
  three defects; one inlining edit plus its partner subtraction -- green on all three.
* **J3 -- MEASURED: THE TRAILER CLASS CAN BE CLOSED IN THE FILE, by a different mechanism.**  Gate 2's failure-count check
  greps `[0-9]+ failures` over the WHOLE log, not the trailer.  If each comparator, on a covered failure (probe calls
  excluded), prints `  FAIL  covered comparator failure, N failures so far` at the moment it fails, then no later edit
  can take that line back: `E_emit` is red on every defect, and ALL SIX stacked attacks are red with it -- the
  conditional reset after the covered rows (`E_emit_cond_mid`) and at the trailer (`E_emit_cond_trailer`), the
  both-tally reset (`E_emit_reset2`), both two-edit trailer rewrites (`E_emit_v_eq_printf_sub`,
  `E_emit_v_nocmp_sub_after`) and the move with fed calls (`E_emit_movefake`).  Healthy runs are whole-log identical to
  #551e (real device, self-mutant, cyl13, srstbit); failing runs gain exactly one line per covered failure (+2 drqring,
  +3 dropold, +4 w57hi, +5 w58lo, +6 rev255).  **Residual: switching the emission off inside a comparator is a class
  (1) edit; with both emissions off plus a reset it is green again** (`E_emit_off_cond_trailer`, three edits).
* **J4 -- Opus on the contract: four sentences false or overclaiming** -- "conditional on their equality, anywhere"
  (MEASURED red at `main()`'s start and after the printed count; true form: "anywhere after the covered rows and before
  the count is printed"); "Nor is moving ..." (J1); "requires every covered call" (it counts `chk()` calls of any kind,
  including the 8 verdict-handed ones and fed calls); "the close is gate-side" (J3 is an in-file close).  True:
  "four classes, each measured"; "24 measured, #551d"; "a reset of `failures` alone ... wherever it sits"; the placement
  of the unconditional both-tally reset.
* **J5 -- Opus's recommendation (#551f):** adopt the emission line; keep the pin (now redundant against the move,
  harmless); class (3) collapses into class (1); fix the four sentences.  Alternative: keep the design, name the
  move-with-supplied-counts class, fix "anywhere", drop "the close is gate-side".

**MY DISPOSITIONS, REVISED BY J3.**  H1: REOPENS (measured, J1); **the repair is J3's emission line, not a contract-only
amendment** -- it is a measured in-file close, and the adjudication's own warrant for adopting the call-count pin
applies with more force: *"disclosing a closable cell while filing a six-line fix is the addition licence inverted."*
H2 / D1: grok was right that the trailer is closable in-file and wrong about how -- a third STORED counter is still
forgeable by the reset (kimi-k3's point, which stands); an EMITTED line is neither stored nor computed: once printed, only
preventing it at the source -- inside the comparator, class (1) -- can hide it.  So the adjudication's "not closable
in-file" is overturned by measurement (J2 confirms its narrower half: a pin on the trailer does not survive).  D2: not a
contract-only #551f -- **#551f = the emission line + the contract rewritten (class (3) folded into class (1)'s
"switching the emission off" residual; H3, H4, H8, H9, H10, J4 wording) + the measurement caption (H7) + records (H5,
H6).  A floor-bound diff: it owes its own pass.**  D3 (deepseek): closed by J3 (`E_emit_movefake` red).

## MINE -- H1 MEASURED (`measured/run551e_h1.out`; scored by gate 2's greps, the exit status shown but not a gate-2 input)

```
MINE_atexit_defer  drqring   | 128 rows, 0 failures | 1 PASS | 0 FAIL | G 1 | DRQ-asserted 1 | geomFAIL 0 | rc=0
MINE_atexit_defer  selfmut   | 128 rows, 1 failures | 0 PASS | 1 FAIL | G 1 | DRQ-asserted 1 | geomFAIL 1 | rc=1
MINE_forge_move    drqring   | 128 rows, 0 failures | 1 PASS | 0 FAIL | G 1 | DRQ-asserted 1 | geomFAIL 0 | rc=1
MINE_dummies_move  drqring   | 128 rows, 0 failures | 1 PASS | 0 FAIL | G 1 | DRQ-asserted 1 | geomFAIL 0 | rc=1
MINE_phase         selfmut   | 128 rows, 1 failures | 0 PASS | 1 FAIL | G 1 | DRQ-asserted 1 | geomFAIL 1 | rc=1
```

* **K1 -- grok's ONE-statement `atexit` deferral is gate-2 GREEN on drqring** (the deferred rows still print their named
  lines, after the token; the lane's FAIL and geometry line intact on the self-mutant).  **A single edit outside the four
  classes: the chain reopens by the stop rule's letter, measured.**  `forge_move` (kimi-k3, grok) and `dummies_move`
  (deepseek, glm, minimax) are green the same way; all three stay red on w57hi because they move only `chk()` rows.
* **K2 -- H12 settled:** a phase key inside `chk()` leaves the lane intact on the self-mutant (FAIL + geometry line).
