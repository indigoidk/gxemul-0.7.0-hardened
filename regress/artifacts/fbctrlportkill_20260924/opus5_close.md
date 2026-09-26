OPUS549CLOSE_ALIVE

VERDICT: SHIP WITH CHANGES

The fix itself is fine. The 73-row probe misses ten edits inside the enumeration you gave me, and neither catches nor discloses them. One of them brings back the original process exit.

**Setup:** a fresh clone of `build/` at `/tmp/gxo549close`. Before any run, `dev_fbctrl.c` (129694b8) and the probe (ad43c3dd) matched the working tree byte for byte. I rebuilt with `rm src/cpus/*.o`; the binary came out b5b99e6d, same as `build/gxemul`, and scored 73/73 with rc=0. I built 25 new one-edit variants; each binary was fresh and had its own md5. None is identical to any of table 3's 62 (I regenerated table 3's edits against the final source to check). The clone was restored from GXEMUL-SEC, checked against the base md5, and its sentinel cleared. The probe and fix were unchanged from start to end. Everything is in `opus549_measured/close/` (`TABLE_close.out`, `TABLE_xrows.out`, `kill_witness.out`).

1. **measured — ten edits score 73/73 (rc=0), none of them among the eight disclosed:**
   - **PORT read qualified by width** — `if (writeflag == MEM_READ && len >= 4)`. A 1- or 2-byte PORT read falls into the write path, selects port 0 and reads 0. Every PORT read in the probe is `lw` or `ld`.
   - **PORT read qualified by COMMAND** — `if (writeflag == MEM_READ && !d->port[DEV_FBCTRL_PORT_COMMAND])`. Session V is the only one with COMMAND ≠ 0, and it never reads PORT.
   - **Refusal skipped by previous selector** — `else if (idata >= DEV_FBCTRL_NPORTS && d->current_port != k)` for k = 1, 2, 3, 4. The bad value is stored. Refusals are only observed after selectors 0, 5, 6 and 7; V's refusal after PORT=1 is overwritten by a legal re-select before any DATA access.
   - **Refusal skipped while COMMAND ≠ 0** — `else if (idata >= DEV_FBCTRL_NPORTS && !d->port[DEV_FBCTRL_PORT_COMMAND])`. **This one ends the emulator:** GET_RESOLUTION, PORT=5, PORT=9, then one DATA read → HOST-DIED, exit 1. The fix survives the same sequence.
   - **Announce suppressed, latch left unset** — `if (!d->warned_port && len == 4)`, `… && d->current_port != 1`, and `… && !d->port[DEV_FBCTRL_PORT_COMMAND]`. Every session that counts announces has its first refusal as an `sw`, after selector 0 or 5, with COMMAND = 0. W and V count nothing.

   The controls on the same axes all go red: the `len == 4` read, previous selector 0, previous selector 7, a `len != 4` announce, previous selector 5, and three operand swaps. So these inputs do reach an observed row; the escaped cells are simply never exercised.

2. **measured — 14 prototype rows kill all of them.** They are in `close_rows_proto.py`, which imports the shipped probe and uses its own `session()`, one fresh emulator per cell. They score 14/14 on the fix:
   - `lb` and `lh` of PORT with selector 5;
   - refuse 9 after PORT=1, 2, 3 and 4;
   - after GET_RESOLUTION: a PORT `lw`, the first refusal counting 1, and PORT keeping 5;
   - the first refusal of a fresh device by `sb`, `sh` and `sd` counting 1;
   - the first refusal after PORT=1 counting 1.

3. **read — how to grade them.** This round closed the width axis "at EVERY width", but only for writes. The read direction and the announce are cells of the same product that were left out, which is the #499 shape. The `current_port` and `port[COMMAND]` edits use fields your brief lists as body-read. Under the joint-cells rule they could count as clause-(e) debt, but only if disclosed, and they are not. Because `E_ref_cmd` is a process exit a guest can reach, I would add a row for at least that cell.

4. **measured — question 2: the R session's "refuse 9 after the NOP, PORT keeps 5" row.** No single-site edit reds it alone.
   - *Read:* at R's second refusal the device is in exactly the state of P's second refusal (selector 5, latch set, port 5 = 0x2a, port 0 = 0, `sw` of 9). So any edit over existing fields that reds this row also reds P's "refuse 9 (sw)".
   - *Measured:* an edit aimed at that state reds this row only together with P's 9 row, P's tail row and K's rows.
   - It catches something alone only if an edit adds command history. A two-part edit ("a command sets latch bit 1" plus "a latched refusal with that bit set stores the value") scores 72/73 with only this row red; each part alone scores 73/73.
   - So it is not vacuous by construction, but it is redundant for every single edit. Either drop it, or keep it and describe it as covering only that case.
   - The real gap on this axis is elsewhere: setting the latch on entry to `fbctrl_command()` (the mirror of table 3's T_D4b) scores 73/73, because R issues its command after its first refusal. The "first refusal after GET_RESOLUTION counts 1" prototype row kills it.

5. **measured — question 3: what my measurements contradict in the contract header.**
   - "CATCHES … the store reached for an out-of-range value" is false as written: the refusal-skipped edits in finding 1 store it and pass.
   - "A refusal or an acceptance conditioned on the access width … EVERY width" is true of writes only.
   - "A latch … set late" is true of M_latchcnt's count only; a latch left unset by width, previous selector or COMMAND state escapes.
   - "Cleared by DATA or command traffic" holds, but its mirror — the latch set by command traffic — escapes.
   - NOT CLAIMED names none of these axes.
   - The period sentence holds as written: modulo 11 is red on the twelve-refusal row, and modulo 12 scores 73/73, as disclosed.

6. **measured — `regress/gate_mips_folds.sh` changed while I was running** (a1acb55b → 1c6bf162). I did not re-measure the gate in this pass.

---
*Recorded by the main loop: agent aabc7b9d2fb013ad5 (resumed from its F2 run), `agent_models.py` = clean, opus-5-5 throughout.
Finding 6 is the main loop's own comment-only edit to the gate block, made after the closing brief was written: a comment
line holding both "checker" and "rows run" tripped check_score_claims.py's loose-line note, and was reworded.*
