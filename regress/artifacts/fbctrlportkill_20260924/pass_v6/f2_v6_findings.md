# #549 v6's own pass -- EVERY SEAT'S FINDINGS, WITH MY DISPOSITION ON EACH (for the adjudication)

Pass: `pass_v6_brief.md` (51 KB: the fixed PORT arm, the v5->v6 probe diff, the gate-16 diff, variant table 6 and the
verifying pass's findings V1-V20 inlined).  Seats: the dedicated grok job (below); the nine-seat panel and the Opus
measuring seat's re-issue (appended when they land).  **The Opus seat's FIRST v6 answer (SHIP) was written by
claude-opus-4-8 after three refusal events and is NOT counted** (`opus5_pass_v6_FALLBACK_opus48.md`; the seat was
resumed for a re-issue).  Codex (GPT-6 Astra) walled until 07:01; the kimi CLI failed with a new 403 (subscription
access), covered by kimi-k3.

## WHAT HELD (measured)

* Table 6: 297 edits, 267 red, 30 at 117/117, **zero predictions missed**, and every one-bit and one-width narrowing red
  on EXACTLY the session-B width rows the pre-table addendum named (the channel check).  The three narrowings that swept
  v5 are red.  Gate 16 PASS with v6 (26 checks, 17 s); the gate's seven log fixtures behave as designed.

## FINDINGS

* **N1 -- LATCH-UNSET x BIT: THE COMPARE WEAKENED ONLY WHILE THE ONCE-LATCH IS CLEAR SCORES 117/117 AND RESTORES THE
  DATA-ARM EXIT** (the dedicated grok, walked, not built; the Opus seat's fallback segment named the same cell and
  witnessed the exit on a fresh device for `LB_unset16`, `opus549_measured/v6/unset_witness.out`).
  `else if ((d->warned_port ? idata : (idata & ~(1ULL << 4))) >= DEV_FBCTRL_NPORTS) {` -- accepts 16..23 while the
  latch is clear.  Every session's FIRST refusal (the only latch-clear write) is 8 or 9 (bit 3), 0x100 (bit 8),
  0x100000005 (bit 32) or all-ones (no single decisive bit); session B's first store is 8, which sets the latch before
  its single bits run.  So at latch-unset only bits 3, 8 and 32 are held alone; **58 bits are open** (4-7, 9-31,
  33-63).  grok's argument that this is FLOOR, not clause (0): the refusal block READS `warned_port`, and the carrier's
  joint-cell floor is *"the cross-product of the guard's dominating predicates with the device-STATE lvalues the fix's
  own repair path reads"*, with the generating-set rule *"at each floor cell, every idata bit the guarded body TESTS is
  written both clear and set"* -- latch-unset is a floor cell and its generating set is incomplete.  grok's remedy: 58
  fresh devices in one diff, each `PORT=5` (legal, does not set the latch), one `sw` of 2^k, one PORT read that must
  still say 5 -- one width, since a third qualifier (width) is a genuine (0) joint.
  The Opus fallback segment's reading, recorded but not counted: disclosed coverage debt under (0), *"closing it would
  need a fresh device per value (the unbounded growth the floor forbids)"* -- 58 is bounded, which is grok's point.
  **MY DISPOSITION: FLOOR (L2), repair in-round as v7** -- grok's reading follows the carrier's joint-cell rule as
  adjudicated on 2026-09-04 (the latch is a body-read state lvalue; the (d) enumeration's operand-swap clause draws
  exactly from body-read fields), and the cost is bounded and measurable (58 short sessions).  **This is the decision I
  most want tested**, together with the cost: 58 fresh emulator processes add to gate 16's wall time.
* **N2 -- `(idata & 7) != 6` as a one-axis edit scores 117/117 outside the literal text of (0)-(8)** (dedicated grok):
  bits 0-2 never change `idata >= 8`, so it is a predicate on bits the compare does not distinguish -- a value-class
  exception (a store of 14 is accepted and the exit returns).  **ACCEPTED as a disclosure sentence in (3)** ("an
  exception keyed on the low three bits"), not a row, per grok.
* **N3 -- grok's denominator** (walked): every mask of a bit 3..63 at any width, bound moves, 32-bit and signed compares
  -- red (table 6 measured the same channel); `idata != k`, finite windows, re-arm periods > 108, a previous-selector
  condition, the accept-path pairs, `lb`/`lh`/`ld` returning 0 while the latch is clear, `len == 3` -- inside (0)-(8).

## OPUS -- A SEAT FAILURE FOR THIS PASS

The seat was resumed twice; **both answers were written by claude-opus-4-8 after refusal events** (`agent_models.py`:
FALLBACK) -- `opus5_pass_v6_FALLBACK_opus48.md` (SHIP) and `opus5_pass_v6b_FALLBACK_opus48.md` (SHIP).  Neither is
counted.  Their MEASUREMENTS are checkable artifacts and are cited as such (`opus549_measured/v6/TABLE_v6floor.out`,
`RECHECK_v6b.out`, `unset_witness.out`): `WB_sh32` (accept 2^5 only by sh) 116/117 red on B's sh row; `LB_set16` (accept
16 only with the latch set) 109/117 red; `SN_signed` 111/117 red; and 117/117 for `LB_unset16` (accept 16 only with the
latch CLEAR -- N1's cell, the DATA-arm exit witnessed on a fresh device), `MB_v18` (accept 0x18), `PB_prev3_16` (accept
16 at previous 3) and `MB_pc4` (accept every value with exactly four bits set).  The fallback text classes N1 as clause
(0) debt and asks that NOT CLAIMED (3) be widened from "one value" to value CLASSES (`MB_pc4`); the second fallback
segment says its first had "briefly treated the value x latch escape as a possible L2 floor breach".

* **N4 -- `MB_pc4`: accept every value with exactly four bits set scores 117/117; (3)'s accept-side sentence names only
  "one value".**  **ACCEPTED -- wording**: (3) covers value classes on the accept side too, and says each reinstates the
  DATA-arm exit that NOT CLAIMED (2) keeps as the tripwire.

## THE PANEL (`_scratchpad/panel_20260925_194340/`; codex walled, the kimi CLI a subscription-access 403 covered by
## kimi-k3; grok and glm appended when they land)

* **N5 -- agy (SHIP WITH CHANGES) independently found N1's cell** ("the Latch x Bit gap": the only latch-clear values
  are the first refusals 8, 9, 0x100, 0x100000005 and all-ones) and classes it as the two-axis joint of NOT CLAIMED
  (0), bounded by the kept DATA-arm tripwire.  **So the seats split on N1: the dedicated grok says FLOOR (58 cells owed);
  agy and the Opus fallback text say (0).**
* **N6 -- agy: my brief's premise "the working tree's probe is still v5" is FALSE** -- I installed v6 (a9a2be3d) after
  drafting that line and before firing.  **ACCEPTED -- a stale brief premise; no effect on the review** (the inlined v6
  is the tree's file, byte for byte).
* **N7 -- deepseek: "every one-bit narrowing red on EXACTLY the predicted session-B width rows" overclaims** -- MKB_03,
  _04, _32, _33, _63 and MK_b8_ctl also red rows in P, W, V, X3, X7, Y (values sharing that bit).  **ACCEPTED --
  wording**: "the session-B rows red are exactly the widths that carry the bit; other sessions' rows also red where
  their refused values share it" (gate comment and brief).
* **N8 -- deepseek: "all 61 one-bit narrowings (MKB_03 .. MKB_63)" -- MKB_08 is MK_b8_ctl's text, so 60 MKB rows plus
  the control.**  **ACCEPTED -- wording.**
* **N9 -- kimi-k3: NOT CLAIMED (3)'s "a latch that re-arms only after MORE refusals than any session makes (B makes
  108)" is off by one** -- a latch that re-arms after exactly 108 (the second announce landing on a 109th refusal no
  session makes) also scores 117/117.  **ACCEPTED -- wording**: "only after 108 refusals or more".
* **N10 -- kimi-k3: session B depends on the emulated `dsll` EXECUTING, which the encoding pins and the disassembly
  control do not verify** -- but table 6's width-differentiated channel (bit 9 red on sh/sw/sd, never sb; bit 16+ never
  sh; bit 32+ never sw) is positive evidence that each 2^k reached the compare at each width.  **ACCEPTED -- a LIMITS
  sentence naming the dependency and that evidence** (a pinning row is optional; not adopted without a ruling).
* **N11 -- kimi-k3: "every bit the compare tests set alone at every width (B)" overclaims for narrow widths** -- sb
  carries bits 3-7 only.  **ACCEPTED -- wording**: "at every width that can carry it".
* **N12 -- kimi-k3: X5 appears in no holder list though the control row says "X2-X7".**  **EXPLAINED**: there is no X5
  -- previous selector 5 is P's, W's and Y's; the label is a range.  Wording: "X2, X3, X4, X6, X7".
* **N13 -- minimax: SHIP**, no findings beyond a timing assumption on the count sample (the announce is `fatal()`,
  unbuffered in this invocation's pty; the fix's count row is green on every run).

## GROK (panel) / GLM (appended as each lands)

### glm-5.3:cloud -- SHIP WITH CHANGES (`ollama_glm.txt`, 10,927 chars, packet-fed)

* **N14 -- glm on N1: two-axis, (0)-class, CONDITIONAL on (0)'s full text** (F1; the packet cut (0) mid-sentence).  The
  probe's (0) reads generally (`regress/fbctrl_port_probe.py`, "NOT CLAIMED (disclosed).  (0) An edit conditioned on TWO
  axes at once ..."), so glm's condition is met.  **glm joins agy and the fallback text on the (0) side; the dedicated
  grok alone says FLOOR.**  Count the arguments, not the seats: the question for the adjudication is unchanged -- is
  the latch a body-read state lvalue whose clear state is a floor cell under the joint-cell rule.
* **N15 -- V2 says five behaviour changers; table 6 carries six `BR_*` edits** (F2).  MANIFEST.out lists six, all
  RED.  **ACCEPTED -- records.**
* **N16 -- LIMITS OF A ROW's "not which" is imprecise** (F3): the row prints the last stored int, which names the bit
  for bits up to 30.  **ACCEPTED -- wording.**
* **N17 -- NOT CLAIMED (8)'s exclusivity rests on R's program order, which the packet does not inline** (F4; CANNOT
  SETTLE from the packet).  R's entry is at `regress/fbctrl_port_probe.py` ("#  R: between two refusals, ...").
  **OPEN -- for the file-reading adjudicators (Fable, Astra) to settle by reading R's rows.**
* **N18 -- the commit must carry the v6 probe with the gate's 117 pin** (F5).  **ACCEPTED -- already so** (the tree
  holds v6, a9a2be3d; N6).
* **N19 -- the pre-table addendum was not inlined** (F6).  **ACCEPTED** -- cited by path for the adjudication.
* **N20 -- an unstated invariant: only K and R read DATA without re-selecting PORT first** (glm's "what did all of us
  miss").  **ACCEPTED -- one LIMITS sentence.**
* glm's Q1 zero carries its denominator (one-axis shapes across width, bit, range, bound, truncation, accept map, read
  side, announce side, latch period, direction; previous selector and COMMAND single-axis).  V1-V20: all UPHOLD (V2
  with N15).

### grok-4.7 xhigh (panel) -- SHIP WITH CHANGES (`grok.txt`, 8,011 bytes, file-reading; walked, not built)

* **N21 -- grok: A FLOOR BREACH OUTSIDE (0)-(8), SINGLE-AXIS.**  A refusal that WRITES THE CONSTANT 5 for a value the
  probe refuses only after `PORT=5` reads back exactly like a refusal that KEEPS 5 -- and every B value (and P's
  0x200000000, W's 2^63) is refused only at previous selector 5.  So a value-keyed constant write on the refuse path
  (grok names 32, 64, 128, 0x200 and any value whose low 32 bits are zero) is predicted 117/117.  The SESSIONS text's
  "never 5" covers only a STORE of the truncated value (2^k, INT_MIN or 0), which table 6 shows red.  **grok's remedy:
  one anchor other than 5 -- e.g. B's sd group selecting 7 before its stores -- so that neither a stored 2^k nor a
  written 5 reads back as the anchor.**  **MY DISPOSITION: FOR THE ADJUDICATION -- the second floor question of this
  pass, beside N1.**  It is one-axis (the value alone selects it), so (0) does not reach it; it is the "kept" reading
  that the anchor cannot tell from "re-written to the anchor", which is clause (f)'s shape (a relative oracle) on the
  refusal side.  Open for the ruling: whether one second anchor closes it or merely moves it (a constant equal to the
  new anchor, on bits only that width carries).
* **N22 -- NOT CLAIMED (4) names SEVEN equivalents; the gate comment says the contract discloses THIRTEEN** (grok 2; V9
  and V18 REFINE).  Six measured equivalents (`EQ_gt7`, `EQ_maskhi`, `EQ_ge8lit`, `EQ_dir_new`, `EQ_latch_ne1`,
  `EQ_ann_idata`) are in no header sentence.  **ACCEPTED -- wording** ((4) names all thirteen, or the gate comment
  says seven).
* **N23 -- the pre-table addendum's CHANNEL lines are wrong in four places** (grok 3): the count row catches latch
  periods through 107, not "up to 106"; `MK_b5_7` is red on all four widths, not sb alone; `MK_b9_31` is also red at
  sd; `B_mod11` is also red on P's twelve-refusal row.  Every RED/GREEN prediction held; the per-row channel lists
  were incomplete.  **ACCEPTED -- records**: the addendum is pre-registered and is not edited; the correction is
  recorded here and in the round block.  (grok checks (3)'s "more than 108" bound against these: it holds.)
* **N24 -- the addendum's latch witness names the wrong edit** (grok 4): `CELL_keep_l0` never sets the latch, so every
  value is stored and the sb read is the LAST store, not the first.  The effect the addendum wanted is real and is
  shown by `MKB_03` (all four widths stay 0x8).  **ACCEPTED -- records.**
* grok's Q1 denominator (from table 6's raw got-values): each single bit 3..63, the three ranges, the four one-width
  ignores, the bound moves both ways, the 32-bit window, reset-to-0, `idata & 7`, store-`idata` -- red.  Green and no
  behaviour change: the six equivalents of N22 and the thirty disclosed.  Green WITH a behaviour change: N21 only.
  V1-V20: UPHOLD except V2, V9, V18 REFINE (N22) and V16 CANNOT SETTLE (a record note grok did not reopen).
* On N1 the panel grok says nothing directly; it classes a width x value joint as (0).

## THE SEATS, FINAL: agy, deepseek, minimax, kimi-k3 (covering the kimi CLI's 403), glm, grok (panel), grok
## (dedicated) ANSWERED.  codex WALLED (usage limit to 07:01).  Opus: SEAT FAILURE (two fallback answers, not
## counted; their measurements cited as artifacts).  Fable: THIS ADJUDICATION.  Astra: owed after 07:01.

## THE QUESTIONS FOR THE ADJUDICATION

1. **N1** (latch-unset x bit): FLOOR -- a repair in-round -- or NOT CLAIMED (0)?  Tally: the dedicated grok FLOOR;
   agy, glm and the fallback text (0).  Count the arguments.
2. **N21** (a constant-5 write on the refuse path for values refused only at previous 5): FLOOR, or disclosed?  If
   FLOOR, does one second anchor close it, and what is the stop condition?
3. **Which of my ACCEPTED dispositions is wrong?**  (N2, N4, N6-N20, N22-N24.)
4. **N17** (NOT CLAIMED (8) against R's program order) is OPEN: settle it by reading R's session in
   `regress/fbctrl_port_probe.py`.
