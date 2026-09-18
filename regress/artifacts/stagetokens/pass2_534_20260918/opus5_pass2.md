OPUS_SEAT_ALIVE_20260918_534
`# CHECKPOINT — 2026-09-18 ~11:3x`

**VERDICT: DO NOT RATIFY.** Two dispositions are wrong on measurement. **R1** does not do what it claims on the real ledger: none of the 25 real held cells renders as `hold`. **`heldmasked`** should not be filed. It is an L3: you can close `pcc2c040assertrow` over the owner's live hold and H, I and the wall all stay green. The floor question (Q1) has 13 answers: 13 of 13 mutants I built score 16/16 and pass H2.

All scratch work is in `opus534/`: `drive.py`/`drive.out` (the controls), `real.py`/`real.out` (effect on the real ledger), `p1.py`, `p3.py`, the `p4*.out` files and `p3_close.out`. Nothing under GXEMUL-SEC was changed. `git status --short tools/pipeline` matches the snapshot I took before starting, and the md5 of every `*.py` and `ledger.json` is unchanged. The only side effect is `.pyc` files in the git-ignored `tools/pipeline/__pycache__/`.

## Q1: mutants that misclassify and still pass 16/16 and `--selfcheck`

Driver: `python drive.py`. It imports `run_controls.run()` unchanged, adds my mutants to its `MUTANTS`, and runs `--selfcheck` on each mutated copy. `real.py` runs each mutant against a copy of the **real** ledger and diffs the output against the base run.

| mutant (one edit) | controls | H2 | effect on the real ledger |
|---|---|---|---|
| `check_fix_seats.py`: `not st.is_answer(e)` → `st.is_held(e)`. This puts back #532's measured defect. | 16/16 | PASS | 26 → 22 fail rows. asiceventaddr and r418/419/420 get flagship credit from token entries. **Nothing gates it**: the tool is not in precommit, does not read GXLEDGER, and already fails 26 rows, so its exit status cannot show the change. |
| `STAGE_EXEMPT` without ANNOTATION | 16/16 | PASS | H goes red on 4 stages and I on 3 (r420, fbmode, m8sarpurge). `t_annot` is dated 08-10, so the date cutoff covers it and the fixture never tests the exemption. |
| `STAGE_EXEMPT` without RE_READ | 16/16 | PASS | H goes red on pitlatch2. `t_reread` has one seat, so it is filed before the exemption is ever consulted. |
| `exempts_stage`: drop `not is_held(e)` | 16/16 | PASS | no effect. **Silent.** |
| guard: `newest_tok = min(...)` | 16/16 | PASS | no effect. **Silent.** |
| guard (ii): `findall(ev)[:1]` | 16/16 | PASS | no effect. **Silent.** |
| guard `tok` keeps HELD+NOPANEL entries | 16/16 | PASS | no effect. **Silent.** |
| guard (i) `>` → `>=` | 16/16 | PASS | H goes red on unreadseats23, whose answers are dated the same day as the token. |
| guard also applied to ANNOTATION (the P1 alternative) | 16/16 | PASS | H goes red, I goes red |
| FQ skips the guard when `newest < 2026-09-12` | 16/16 | PASS | no effect. **Silent.** |
| CSP adds `or "PRE-2026-08-16 POLICY" in note` | 16/16 | **PASS** | no effect. This is a partial literal, and H2 only matches whole tokens (or HELD without its bracket), so H2 misses it. |
| `gen_codex_wall`: `st.HELD` → `st.NOTSEAT` | 16/16 | PASS | the real-ledger `--check` reports STALE. The controls never run the wall. |
| dashboard `recs[-1]` → `recs[0]` | 16/16 | PASS | one cell's tooltip changes |

**The smallest serious one is the `check_fix_seats` swap.** It is the defect the new module's own docstring gives as its reason for existing, and it needs a one-token change. No control, no gate and no exit status can see it. Closing it needs two things: `check_fix_seats.py` has to honour `GXLEDGER`, and the fixture needs a fix row (with `commits`) whose only fable5 entry is a token entry. **Also, brief §7 leaves out this file.** It is untracked and new, it imports `stage_tokens`, and no seat was shown it.

Fixture rows needed for the silent ones:
- one entry carrying both HELD and NOPANEL (catches the `is_held` drop and `tok_held_ok`);
- two NOPANEL entries with an answer dated between them (catches `min`);
- an answer whose `ev` cites two panels, only the first of them named (catches `[:1]`);
- a post-cutoff ANNOTATION stage and a two-seat RE_READ stage (catches both `STAGE_EXEMPT` drops at the fixture level).

## Q2: the premises

**P1: a hole, and the scope is drawn along the wrong line.** I split the guard by clause and ran it over the real ledger (`p1.py`):

| token | clause (i): later answer | clause (ii): uncited panel |
|---|---|---|
| ANNOTATION | **1**: `n6:assess` has a fable5 answer on 2026-08-30, fourteen days after the annotation | 7: r418, r419 ×2, r420 ×2, fbmode, m8sarpurge |
| RE_READ | 0 | 1 (pitlatch2 cites another round's panel) |
| NOPANEL | 0 | 0 |

The "retroactive requirement nobody owed" argument is true of clause (ii) only: legacy annotations never named their panels. Clause (i) is not retroactive. It is exactly fixture C's shape, and on the real ledger it hits one stage, `n6`, whose annotation now exempts a post-cutoff answer. **Recommendation:** apply (i) to all three exemption tokens (it costs nothing for RE_READ, which has zero hits) and (ii) to NOPANEL only. `n6` then needs an explicit decision rather than a silent exemption.

**P2: holding deepseek is right, and it is required.** Measured `panel_20260826_222557/ollama_deepseek.txt`: `response` is empty, `thinking` is 142,280 characters, `done_reason` is `length`, `eval_count` is 65536. That is a burn, so the seat failed. H's HELD branch accepts any live hold whatever the count. If deepseek were not named, its missing answer would read as agreement. I also confirmed F1's premise from `brief_sent.md`'s title: it is pass 2 on `9ca9cca` (#466 asiceventaddr). Per the carrier, the thinking should still be read.

**P3: it is an L3, not a filing.** From `p3.py`: three stages have 9/9 answers and a hold marker.
- `sgimtedepth4dead` and `alphatbinegsel`: every held seat answered **strictly later in the same stage**. Those markers are stale and should be defanged, not tolerated. So the "a reorder would newly red a closed row" cost is really a stale-marker record defect.
- `pcc2c040assertrow`: the only genuinely masked hold.

I set its state to `closed` in a copy (`p3_close.out`): `STAGE_PANELS_PASS`, `FABLE_QUEUE_PASS` and `CODEX_WALL_OK` all came back, rc=0. The wall does **list** the hold. But CLOSED-WHILE-HELD, the only rule that stops a round closing over the owner's hold, never fires. The fix is small: reorder the checks, defang the two stale markers, and add a fixture row with 9/9 answers plus a hold.

**P4: yes, two misleading states (measured in `p4*.out`).**
1. **R1 is not delivered.** Real HELD entries carry `d` values of `HELD` (25), `--` (5), `N/A` (6), `''` (4) or none (6); **not one uses `⏸`**. `cell()` classifies by `d`, not by `is_held`. So of the 25 real cells that render a HELD entry, **0 are `hold`**. All 25 are `pend`, which is the "no answer / seat failure" state, and 4 of those show an empty glyph. The control passes only because `t_held` uses `d="⏸"`, a shape the ledger does not contain. Fix: `if st.is_held(ent): cls, d = "hold", "⏸"`.
2. **A hold renders in the column of the seat it is filed under, not the seats it awaits.** `pcc2c040assertrow`'s hold for glm/deepseek/minimax/kimi is filed under fable5, so it shows in fable5's column (fable5 did answer), while the four awaited columns show their old answers. The same happens at `pcc2widthkills` (filed under codex). There is also a smaller one: the cell takes the list-last entry rather than the date-latest, so a stale HELD listed after an answer wins.

## Q3: which dispositions are wrong
1. **R1: wrong as delivered** (P4.1). It holds on the fixture only.
2. **`heldmasked` filed: wrong.** It is an L3 (P3), and the reorder's cost is really two stale markers.
3. **R4's scope (P1): half right.** Restrict clause (ii) only, not the whole guard.
4. **R5: incomplete.** The controls cover three of the five readers. `check_fix_seats.py` has no control and no gate, and `gen_codex_wall` is covered only by the real-ledger `--check`. The H2 selfcheck misses partial literals.
5. **R2, R3, F1 (including deepseek): measured right.** I did not re-measure F3.
