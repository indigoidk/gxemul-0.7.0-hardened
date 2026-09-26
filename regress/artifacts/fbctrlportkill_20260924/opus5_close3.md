The narrowings escape as predicted, and the control shows the channel works when a row holds the bit alone. Writing the re-issued answer.

VERDICT: SHIP WITH CHANGES

The earlier answer's SHIP was wrong. That answer came from a model fallback, and my review found one wrong conclusion and three smaller errors. The v5 probe has a clean-sweep floor mutant that brings back the process exit.

**1. The floor question: I found a breach (measured).**
- The earlier "no breach" was drawn from a thin denominator. Its 15 edits were 8 equivalents plus 7 behaviour-changers, and two of those 7 were already in table 5 (`BR_ge9` compiles to `M_gt`'s binary; `BR_acc_w8` is `CELL_keep_w8`). None of them tested the compare narrowed by a bit range, so I built that shape.
- **These score 111/111 (the probe's full total):**
  - `else if ((idata & ~0xfffffe00ULL) >= DEV_FBCTRL_NPORTS) {` — ignores bits 9–31;
  - the same with `~0xe0ULL` — ignores bits 5–7;
  - the same with `~0x7ffffffc00000000ULL` — ignores bits 34–62.
- **The control goes red:** ignoring bit 8 alone (`~0x100ULL`) scores 107/111, because v5 refuses 0x100, whose only high bit is bit 8.
- **The bits 9–31 narrowing brings back the process exit.** A guest writes 0x200 to PORT, then does one DATA read: HOST-DIED, exit 1. The fix survives the same sequence.
- **Why it stays green:** no v5 refusal has all of its bits from bit 3 up inside those ranges. All-ones sets every bit but never one alone.
- **The contract does not cover it.** Disclosure (3) covers a single excepted value and says thresholds are not in its class. A bit range is neither. So the floor paragraph's claim that "the value's … class" is held is false.
- **Grade:** a floor breach (L2) on the bit class the body's `>= 8` test reads. Fix it in this round.
- **Remedy:** refuse each single-bit value 2^k for k = 3..63 in one session. That catches every narrowed mask, not just these three ranges.
- **Denominator, corrected:**
  - 8 equivalents, all 111/111. **Six**, not five, compile to the fix's own binary; `EQ_dir_new` and `EQ_latch_ne1` build to different binaries but behave the same.
  - 5 new behaviour-changers, all red.
  - 3 bit-range narrowings, all 111/111 — the breach.
  - 1 narrowing control, red.
  - Plus table 5's 108 generated cells.

**2. My eleven closing-F2 escapes against v5 (measured): 8 red, 3 green but disclosed.**
- Red: `ref_colorb` 110, `ref_y1` 110, `ref_colorr` 110, `ref_cmd1` 106, `rd_colorb` 110, `rd_cmd1` 109, `ann_bit63` 109, `ann_cmd1` 108.
- `ref_colorb` is the one that brought back the process exit. My adopted row, "V PORT keeps 7 after its later refusals", is the only row that catches it.
- Still 111/111: `cl_len2`, `cl_p5`, `cl_c0`. These are refusal-time cell writes, correctly disclosed under clause (8).

**3. CELLMAP (read from table 5's raw logs, not re-run by me).**
- The header's listed cells produced 108 generated one-axis edits: 98 built, and 10 identical in text to an existing mutant. Every one is red except `CELL_rd_s0`, which is correctly marked equivalent.
- The named holders I spot-checked all match: keep_p5→P, keep_p6→W/X6, ann_p0→F, ann_p2→Z+X2, sil_p0→Z, sil_p5→P/R/W/Y, the cell_* edits→V.
- **One correction to my earlier answer.** `CELL_rd_s5`'s collateral is not "pty desync". Sessions A and R die, A at step 17 and R at step 3. The misrouted read resets the selector to 0, and the next DATA write runs an unimplemented command, hitting the out-of-scope command-default exit. Its clean in-scope kill is C's liveness row (0x0).
- No cell is mislabelled and none is unheld.

**4. Closing-F2 dispositions I think wrong: 1 of 5, disposition #1.**
- Its ruling that the seats' COMMAND, cell and selector edits are off-floor stands.
- Its warrant — "Table 4 holds the genuine floor axes: idata magnitude, width and class" — is measured false for the class axis. The same values went unrefused in tables 4 and 5.
- **#4 is borne out:** the repair did owe its own pass, and this pass found the breach, so the chain does not close here.
- #2, #3 and #5 stand.

Outputs are in `opus549_measured/c3/`: `TABLE_mask.out`, `TABLE_c3.out`, `logs/`, and `gen_mask.py.txt` / `mask_witness.py.txt`. The clone was restored to the fix and its md5 checked, the sentinel is cleared, and leftover stubs are removed.

---
*Recorded by the main loop: agent aabc7b9d2fb013ad5, RE-ISSUED after its first verifying-pass answer (opus5_close3_FALLBACK_opus48.md) was written by claude-opus-4-8 in a fallback.  This text is claude-opus-5-5's (2026-09-25T22:06:10.149Z UTC, `agent_models.py`); the mask table and the kill witness (opus549_measured/c3/TABLE_mask.out) ran in this segment.  Badge s.*
