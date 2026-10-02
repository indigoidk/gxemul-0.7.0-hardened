`lw +0x00` runs from a normal pc and does not take it. **M3 121/121.**
  - `crime_interrupt_reassert`'s assert branch fires in the gate session before its refused `sh 0x0800` — but gate has no `-- declined.` count row — and in the IRQ sessions only at the final accepted `lw`. Ticks never take it (INTSTAT&INTMASK is 0 until the setup completes, and only the first tick fires per session). **M4 121/121.**

  The enumeration "in EVERY switch arm an accepted access reaches first in some counted session" is *true as stated* — every arm head is covered (`c2_pre_irq`, `c2_pre_rev` measured) — but the class the project rule says must be closed whole is "pre-set by an accepted access", and these are live members of it. Only HARD_RESET is disclosed; the implication that the other branches are rowed is false.

  What I verified as *complete*: the fall-through floor ({1,2}×{R,W} per observable label, all six named arms plus default; CONTROL-reads and DOG correctly identified as body-less); the answer class at every named label over nonzero lanes (the CONTROL lb cell is vacuous — low byte of 0x100 is 0 — and the enumeration honestly rows `ctl v0` at lh only, covered by the superset argument); the landing class as enumerated; the re-arm branch coverage against `KINDS`.

  ## Q2 — Floor gap? Yes; four, all measured 121/121 on the repair-7 instrument in my own clone.

  1. **Headline** (the class this pass was convened to verify): replace line 91 `#define CRIME_W_LEN (1 << 0)` with `#define CRIME_W_LEN (1 << ((relative_addr & 0x100) >> 8))` (bit 7 with `0x80 >> 7` works identically). Row expected to catch it: `mid once` — it cannot, because every refusal in the mid session has bit 8 set (keyed bit constant at 2) and no other session refuses with bit 8 set (bit constant at 1). Behaviour undone: refusals alternating between bit-8-set and bit-8-clear addresses announce twice, breaking the per-instance `(once)`.
  2. Insert `d->warned |= CRIME_W_LEN;` inside `if (idata & CRIME_CONTROL_DOG_ENABLE)`. No row can see it: `rearm once` takes the branch only after the session's first refusal; `latch x5`'s prologue write is 0x01.
  3. Insert `d->warned |= CRIME_W_LEN;` as the first statement of the `0xbfc05100` redirect branch. Same shape via `PROBE_PC`.
  4. Insert `d->warned |= CRIME_W_LEN;` beside `INTERRUPT_ASSERT(d->irq);` in `crime_interrupt_reassert`. The gate session takes it pre-refusal but has no count row; the IRQ sessions take it only at the final `lw`.

  Minimal repairs owed (naming, per the panel rule, not driving): the mid session needs a follow-up refusal with bits 7/8 clear (mirror `hi once`'s `+0x07`); a counted session needs an accepted `sw +0x08 0x200` before its first refusal (0x200 clears to 0 — no text, CPUs keep running); a counted prologue needs an accepted `lw +0x00` at `PROBE_PC` with `ra` set; the gate session needs a `-- declined.` count row. And the class rule now bites twice: keyed-latch (F2/closing → second-closing → this pass) and pre-set (glm pass-2 → this pass) — repair 8 must close both whole, at bit/branch granularity, with the contract saying which cells are covered.

  ## Q3 — Wrong statements.

  - **POSTTABLE 5's DENOMINATOR: "every address bit 0-9 carried both ways by each kind of refused access (answer 1R/2R, landing 1W/2W, notice, fall-through, re-arm, latch)" — false for latch × bits 7 and 8** (measured, M1). The same sentence is in the probe header's mid-section comment ("every address bit is now carried both ways by a refused access of each kind") and in the brief's DISCLOSED bullet ("An effect keyed on a single ADDRESS BIT is NOT in this class…"). The mid session carries those bits one way for the latch kind; only the mask shape was measured, and the shift shape escapes.
  - **The pre-set closure implied by CONTRACT item 4 + DISCLOSED is overstated**: only HARD_RESET is called unrowable, but the DOG_ENABLE, PROM-redirect, and reassert-assert branches are equally unrowed (measured M2/M3/M4). Either row them or disclose them next to HARD_RESET.
  - Minor, conservative direction: the DISCLOSED accept-cell list ("offsets other than +0x00, +0x30, +0x210, +0x1f8 and +0x278") omits cells the probe does row — +0x34 (`acc4 rlo`/`acc4 wlo`), +0x214 (`top4 anchor`), +0x27c (`top4 rlo`, `top4 w`).

  **Could not check**: the 47 PRETABLE-5 predictions themselves (I verified `check_pred` outputs and the named red sets, not every mutant's diff); tables 1–3 (taken as recorded); the time rows' 66–990 window beyond the 5 agreeing runs I produced; the quoted earlier-pass seat reports except where inlined; and my measurements are mine (fresh clone, this gcc), not the frozen table drivers — though the probe script and baseline md5 are identical.

  **NO-GO** — the 121-row repair-7 test still has floor breaches, one of them in the exact class (single-axis keyed latch) this closing pass exists to verify; the chain cannot close here.

To resume this session: kimi -r session_f040a72c-17da-41d9-9721-3b614b12b494
