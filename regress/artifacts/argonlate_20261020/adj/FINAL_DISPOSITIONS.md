# Late-review adjudication -- FINAL DISPOSITIONS (main loop, 2026-10-20 ~20:4x)

Evidence basis: **4 of 4 roster seats + Argon on its own flags** -- GPT-6 Astra (`codex_argonlateadj.txt`), grok-4.7
(`grok_adj.txt`), GLM 5.3 (`glm_adj.txt`), Fable 5.1 (`fable5_adj.md`), Argon (`_scratchpad/gweb/jobs_20261020_argonpack20/
argonadj/gemini_web.out`).  All five: ADOPT WITH CHANGES.  No seat overturned a GRADE except on B5; the changes are to
replacement TEXTS and to three dispositions.  Opus, agy, kimi, deepseek, minimax: deliberately not fired (owner roster).

## Disputes, decided by argument (both sides recorded)

* **B5 `sgirekills` [70]/[71] -- TOKEN NOW, and file the policy question for the owner.**  For: Astra, Fable, Argon --
  `[NOT A SEAT ANSWER]` states only that an entry saying "it never answered" is not an answer, true under EVERY
  possible owner ruling; today `check_stage_panels.py --list` prints `ok sgirekills assess 9/9` and `live_holds` returns
  [] -- false displays (Argon: "LIVE", not "latent"); `6c2840d7` tokened cxlaunchquotation [8]/[12] without waiting.
  Against: GLM, Grok -- `untokenedanswers` item (2) asks the owner how a deliberately excluded seat is recorded, so
  tokening decides it by side effect.  Decided: the token corrects a record to match its own text; what the owner owns
  is whether a roster-narrowed stage may CLOSE short, and the restored hold blocks a re-close until the owner rules --
  the conservative default.  The policy question goes to the owner with this dissent.  sgirekills' `state_note` /
  `hold_question` gain the restored kimi/opus5 assess hold (Argon).
* **C2's W7 -- IN PLACE.**  For: Astra, Fable -- `latch 1x`'s note prints "TWO declined ISR accesses" in every gate-14 log
  (`note[:70]`), no log reader ever sees a docstring addendum, and A2 already edits a printed banner in place on the
  same ground (no gate reads note text).  Against: GLM, Grok -- keep the AST, disclose in the block.  Decided: in place;
  the unit records "AST identical but for one note string", the form `check_probe_wiring.py` already uses for #565.
  W6's stale clause lies past the 70-character cut and never prints -- it stays in the block (my packet's premise that
  W6 prints was wrong; Astra, Grok, Fable, Argon).
* **A3's `src/cpus/cpu_ppc_instr.c:2470` sentence -- OUT of this unit (all four seats but Astra), landed on the
  `heldrecedits` ROW** (Fable), not as a round-block note; the row's scope sentence widened to name it.  Replacement to
  carry: "The rldicl general-register expected values come from the rldiclx RTL ..." (Astra's wording).

## Replacement-text corrections (each a seat finding, verified before adoption)

* A2 banner: scope it -- "rldicl/rldicr register-value wants derived from ... :29736 (rldiclx), :29748 (Rc=1), :29822
  (rldicrx), :6878 (ROTL64)" (GLM, Grok, Astra; `:29748` from Argon -- VERIFY that line before using it); its comment
  cites only the first sentence of the `:178-179` contract (Grok).
* A3: narrow the "apparatus rows" clause to the NON-architectural wants -- decoder text, exit status, disassembly and
  census counts (Grok); bracket the `:178-179` sibling "Every row calls want_rldicl / want_rldicr" with "The
  rldicl/rldicr register-value oracles use want_rldicl / want_rldicr; no row consumes the other helpers" (Astra).
* A4: M_MB5 measures the loss of `mb5` only -- the low five MB bits are reasoned (Astra, Argon); the mask end-bound and
  bit-position entries share ONE built mutant (M_MASKEND, whose construction contains the UB shift) and the loop-bound
  form is derivation only (Fable, Astra); include M_NOAND in the measured list (Argon).
* A6: bracketed correction beside the original words, as t1's header was done (Fable).
* B (CHANGELOG/OB correction note): "four Fable walls of 2026-10-17" is FALSE -- `sgirekills` [45]/[49] are 10-17 walls
  too; rewrite as ORDINALS ("Fable's third wall that morning", "its fourth wall that day") (Fable, GLM, Argon);
  "(all three)" -> "(all three seats)" (Fable).  Grok's own summary "V3 wall" -> "V3 stall" (Astra); the
  cxlaunchquotation [8]/[12] token gloss "a wall is a SEAT FAILURE" on STALLED entries (Grok).  Do NOT edit GLM's
  `fableheldform` [2] to say "V3 stalled" -- GLM inferred V3 WALLED (Argon); quote each seat as it spoke.
* B4: qualify the refutation -- the recorded 08-30 experiment concerns `>=`; state the index-ordering consequence as a
  RISK, not as a measured re-opening (Astra).
* B7: "a later-dated Fable review answer that discharges the hold", not any recorded answer; distinguish the 9-vs-4
  roster mismatch from the two-seat confirm (Astra).
* C1/C2: say which sets "four fixed sites" (the clause-(b) re-insertion sites) and "three ISR sites" (the ISR announce
  sites since F13) are (GLM); the synopsis "two unmeasured" is false of M11 -- measured in killtable3, not
  killtable{,2} (Astra, Fable, Argon); one clause on the printed present-tense pre-#531 kill notes (`:448-449`, `:452`,
  `:473`) giving the probe's polarity line (`:157-161`) as the reason they stay (Fable, Grok).
* C0'/F8: SPLIT -- the wording objection is refuted; the absence of an all-green `RESULT=32/33` case in
  `score_selftest.sh` is TRUE: FILE as test-coverage debt (Astra, Argon).
* C4: an exact replacement hunk for the five misattributed driver notes (Astra, Argon).
* `ppcrldiclbanner` (LOW, open): this unit touches the docstring and the print block, which is that row's closure
  condition -- fix the `RUNG-3 WITNESS` labels (`:2`, the usage string `:101`, the banner `:389`) to DETECTOR and close
  the row if section H allows, else record "condition met" (Fable, Astra, Grok).

## Filed (new rows or row amendments)
* `untokenedanswers`: the S1 positive-answer-marker check; the automatic token-writer proposal (Astra: no existing writer
  does not refute creating one); the roster-waiver policy question (B5, with the dissent).
* B7 `fableheldform`'s review roster (a later Fable answer reds H) -- FILE.
* C0'/F8 -- `ip30selftest3233` (LOW): `score_selftest.sh` has no all-green-rows `RESULT=32/33` case.
* rldiclf2 F9 -- a value anchor for gate 13 (design debt, LOW).
* `heldrecedits` widened to carry `cpu_ppc_instr.c:2470`.
* `ip30stallgreen` gains Argon's stall derivation as provenance (late-dissent rule: dissent verbatim).
* Credit, in the record: Argon's rldiclf2 Angle 2 PREDICTED the identity-body leg row for row (16 green / 8 red), and
  `IDENTITY.out` measured exactly that set (Fable).  rldiclf2 F7 (relative artifact paths): settled, every cited file
  exists at HEAD (Fable).
