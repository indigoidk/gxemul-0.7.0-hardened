OPUS_SEAT_ALIVE_20260918_534F2
`# CHECKPOINT -- 2026-09-18 12:29   HEAD: e16a8b7 #533 landiskaux: landisk's wdc aux register sat at the PC-layout +0x206, so the kernel's soft reset landed on unmapped memory`

**VERDICT: DO NOT RATIFY (as-is).** F6 and F7 hold up on the real ledger. But the repaired composite has **eight new mutants that each score 33/33, SELFCHECK included**. Two of them are floor breaches of dispositions this round claims to have made:
- **N10**: with `held_seats` returning only the first seat, the owner's `pcc2c040assertrow` hold shrinks from 4 awaited seats to 1, and no exit status changes.
- **N1**: F8's "clause (i) binds EVERY exemption token" is pinned by nothing. Reverting it has zero effect on the fixture and zero effect on the real ledger.

F6's live-hold rule also covers only the full-count branch. On the real ledger, 4 short stages are reported HOLD for a seat that has already answered. All of these are L1 fixes, since nothing is committed, and they are small.

**SELF-REVIEW DISCLOSED:** F4, F5, F6, F7, F8 (the measurement), F12, F13 and F14 were mine.

**PROCESS DEFECT OF MINE, disclosed first:** I imported `gen_dashboard` to call `cell()`. It has no `__main__` guard, so the import **rewrote the tracked `tools/pipeline/matrix.html`**. The md5 went from ff403165… to c7b04803…. The new bytes are identical to `gen_dashboard.py --out` from the current ledger and generator (`cmp` SAME). I checked the md5 of every `*.py`, `ledger.json` and `fable_queue.md` against my pre-run snapshot, and all are unchanged. So the **old file was stale against the current tree** and my write made it current. I could not restore the old bytes: they were an untracked working-tree state and no copy exists. `git status --short` is identical before and after (it was already ` M`). **Author: regenerate the file yourself before commit, and do not trust my copy.**

## 1. Q3 floor on the repaired composite: MEASURED

Commands: `python drive2.py` (wraps `run_controls.run()` unmodified, adds mutants; the SELFCHECK leg is in the 33) → `drive2.out`. Then `PYTHONIOENCODING=utf-8 python real2.py` diffs each mutant against the real ledger (CSP, FQ, check_fix_seats, wall `--check`, dashboard) → `real2.out`, `real2b.out`. Base: 33/33, all 18 shipped mutants killed (`base_all.out`).

| mutant | 33 ctrl | real-ledger effect | row owed |
|---|---|---|---|
| **N10** `held_seats` → `[:1]` (only the first named seat) | 33/33 | **pcc2c040assertrow HOLD awaiting `glm, deepseek, minimax, kimi` → `glm`**. The same happens at asiceventaddr and wdcrearmzero. Dashboard: 3 awaited columns revert to `pend`. rc unchanged. | a **multi-seat** hold, e.g. t_fullhold `glm, deepseek]` with `awaiting: glm, deepseek$` **anchored**, plus `cell_classes == ["hold","hold"]`. Every fixture hold names ONE seat, which is the exact 2026-08-17 exitsweep under-report class. |
| **N1** clause (i) → `if nop and d > newest_tok` (undoes F8) | 33/33 | **NO EFFECT** | ANNOTATION + an untokened answer dated later → TOKEN-REFUSED. Also a RE_READ variant. `t_annot2`/`t_reread2` are same-day, so they cannot see it. |
| N2 clause (ii) → `if tok:` (makes it retroactive) | 33/33 | H loses 8 grandfathered stages; FQ FAIL (r420, fbmode, m8sarpurge) | ANNOTATION stage whose answers cite an unnamed panel → still exempt. Only the real ledger catches this today. |
| N3 discharge by ANY seat's later answer | 33/33 | names change on 7 HOLD lines. The dashboard drops 4 hold cells (`hold`→`tok`/`none`). | 9/9 + live hold + a LATER answer by a *different* seat → still HOLD |
| N4 discharge by any later entry, not only an answer | 33/33 | NO EFFECT | a later HELD/NOTSEAT entry by the named seat must not discharge |
| N5 dashboard `_latest(ents)` → `ents[-1]` | 33/33 | 2 real cells show an older answer | F7's "latest-by-date" has no row: one seat, two answers recorded out of date order |
| N6 dashboard unparseable-marker fallback off | 33/33 | NO EFFECT (0 real instances) | disclose, or add a row with `[HELD AWAITING SEAT:]` in a bad shape |
| N7 CSP `names = []` | 33/33 | discharged seats get listed as awaited | covered by the N3/N10 rows |

## 2. F6/F7 on the REAL ledger (`verify.py` → `verify.out`, `discharged.out`, `livecells.out`)

- **H:** `HOLD pcc2c040assertrow review 9/9 awaiting: glm, deepseek, minimax, kimi`, rc=0. **F6 VERIFIED.**
- **Closed copy** (`state held`→`closed`): `STAGE_PANELS_FAIL … pcc2c040assertrow CLOSED-WHILE-HELD review 9/9`, **rc=1**. **VERIFIED.** FQ stays PASS, which is correct: it is not FQ's rule.
- **Render** (`--out` to scratch only): `cell()` returns `hold` for **35/35** live (seat, stage) holds. **32** appear on the page as `awaiting …` cells. The other 3 are `design`-phase holds (alphaswpctxreg, alphatbinegsel, armbfiwidth), and `PHASES` has no design column. The page has 52 `hold` cells in total; the other 20 are `d`-derived. **F7 VERIFIED.** The design-phase gap predates this round and should be disclosed.

**NEW, and it is F6 half-applied.** `live_holds` gates only `len(got) >= n_seats`. The `<9` branch still enters on *any* marker, and when nothing is live it falls back to the marker's names. On the real ledger, **4 stages hold only discharged markers and report HOLD for a seat that already answered strictly later**, which masks a real gap:
- `pcc2c040kill review`: 8/9. Reported "awaiting: fable5", but fable5 answered on 09-09. The seat actually missing is **agy**.
- `pcc2c040kill assess`: 3/9. The same fable5 discharge.
- `proberowsubset assess`: 3/9. codex was discharged on 09-08.
- `lcabadval research`: fable5 was discharged on 09-09.

This is heldmasked's mirror: a discharged marker masks a short stage. It also means `CLOSED-WHILE-HELD` fires on a discharged marker. Either route the `<9` branch through `live` (these 4 then turn red and need an honest disposition) or defang the 4 markers. Row: 5/9 + a discharged hold → incomplete, not HOLD.

## 3. Q1: adjudication, one line each
- F1, F2, F3, F4, F5: **UPHOLD**. Each is killed by its row (`base_all.out`).
- F6: **REFINE**. It is correct at ≥9 (verified). It is half-applied below 9 (the 4 stages above) and blind to multi-seat holds (N10).
- F7: **UPHOLD**. 35/35 via `cell()`. But the latest-by-date part is unpinned (N5), and the 3 design-phase holds have no column.
- F8: **REFINE**. The rule is right, but **nothing measures it** (N1). The n6 retag is TRUE: a single fable5 READING seat on 08-30. But note the structure: any later answer can put itself inside `tok` by carrying a token, and it then *is* newest_tok. **Clause (i) can therefore always be disarmed by tagging the late entry.** Say so in the docstring.
- F9, F10, F11, F12: **UPHOLD** (killed). kimi's `+`-concatenation escape is correctly disclosed.
- F13: **UPHOLD**, with a caveat. It is the same parser but **not the same discharge rule**. The wall lists 29 held stages, discharged markers included, while H reports 17 HOLD. They disagree about what counts as held.
- F14: **UPHOLD as filing**, provided the shipped `stage_tokens.py` docstring does not imply the tool is covered.
- F15, F16: **UPHOLD**.
- D1: **HOLD STANDS.** It is a burn (`response ""`, `length`, 65536) and the ledger has no deepseek entry on that stage.
- D2: **settled, L3.** The dashboard rendered the hold as `pend`, so it did not carry it.

## 4. Q2: which accepted dispositions are wrong
1. **F8** is recorded as delivered, but N1 shows it unobserved. It is L1 (a row is owed).
2. **F6's "nothing closed newly reds"** is true of the ≥9 branch only. The <9 branch still honours discharged markers (4 real stages).
3. **F7's "latest-by-date"** has no row (N5).
4. **F13's "same parser as live_holds"** reads as agreement, but the two tools still disagree on discharge.

## 5. Q4: what all nine missed
- **Every fixture hold names exactly one seat** (N10). A multi-seat under-report is this checker's own documented historical bug, and the owner's live hold names four seats.
- **Short stages with discharged-only markers**: 4 real stages, including a real missing-agy gap.
- **A stage whose only entry is a HELD marker is skipped entirely** (`"seats" not in info` → `continue` runs before the hold test), so a closed row can carry such a hold in assess/research/review with H green. Derived by reading. The only real instances are in `regress`, which CSP does not scope.
- **`gen_dashboard.py` writes the tracked file on import.** It bit me.
- **The tracked matrix.html was stale against the current ledger and generator** before my write.

Tree: `git -C GXEMUL-SEC status --short` is identical before and after (`status_before.txt`/`status_after.txt`). The md5 of every `*.py`, `ledger.json` and `fable_queue.md` is unchanged. `matrix.html` changed, as disclosed above.
