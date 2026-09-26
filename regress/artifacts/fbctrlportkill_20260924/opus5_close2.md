OPUS549CF2_ALIVE

VERDICT: SHIP WITH CHANGES

The fix is still fine. The probe's claim that every value of every axis is held by a row is false: 11 one-axis edits score 94/94, none of them among the 14 disclosed, and one brings back the original process exit.

1. **measured — how I ran it.**
   - Fresh clone of `build/` at `/tmp/gxo549cf2`. Before any run, `dev_fbctrl.c` (129694b8) and the probe (e1d01763) matched the working tree byte for byte.
   - Rebuilt with `rm src/cpus/*.o`: b5b99e6d, the same as `build/gxemul`, scoring 94/94 with rc=0.
   - Built 17 new edits, each fresh with its own md5. I regenerated table 4's 101 edits with its own generator; none of mine matches any of them.
   - Restored the clone, checked its md5 against the base, cleared the sentinel. The inputs were unchanged at the end.
   - Everything is in `opus549_measured/close2/`: `TABLE_cf2.out`, `kill_witness2.out`, `vkeeps_summary.out`.

2. **measured — question 2: 11 edits score 94/94 (rc=0).**
   - **Refusal skipped, so the bad value is stored:**
     - `else if (idata >= DEV_FBCTRL_NPORTS && !d->port[DEV_FBCTRL_PORT_COLOR_B]) {` — **this brings back the process exit.** PORT=7, DATA=0x77, PORT=5, PORT=9, then one DATA read → HOST-DIED, exit 1. The fix survives the same sequence.
     - `… && !d->port[DEV_FBCTRL_PORT_Y1]` and `… && d->port[DEV_FBCTRL_PORT_COLOR_R] != 0x55` — the same mechanism.
     - `… && d->port[DEV_FBCTRL_PORT_COMMAND] != 1`.
   - **A PORT read falls into the write path:** `if (writeflag == MEM_READ && !d->port[DEV_FBCTRL_PORT_COLOR_B])` and `… && d->port[DEV_FBCTRL_PORT_COMMAND] != 1`.
   - **The announce is suppressed:** `if (!d->warned_port && (int64_t) idata >= 0) {` and `if (!d->warned_port && d->port[DEV_FBCTRL_PORT_COMMAND] != 1) {`.
   - **Effect 4 ("a refusal leaves every cell alone") broken on one value**, inserted after the latch block: `if (len == 2) d->port[idata & 7] = idata;`, `if (d->current_port == 5) …`, and `if (!d->port[DEV_FBCTRL_PORT_COMMAND]) …`.
   - *Read — why they stay green:*
     - V's five later refusals are the only refusals made with cells 2-7 non-zero. V then re-selects PORT=0 before reading anything, so their selector outcome is never seen.
     - No row ever puts 1 in COMMAND.
     - No session's first refusal is a value with bit 63 set.
     - Cells are read back only after V's refusals (sw, sd, sb; previous selector 1 or 7; COMMAND 2) and after K's (port 5 only).
   - Controls on the same axes all go red: X1 non-zero, COLOR_R non-zero, a cell write by `sb`, a cell write at previous selector 7. A weakened bound, `idata >= DEV_FBCTRL_NPORTS - 1`, also goes red (85/94).

3. **measured — one added row closes most of this.** A PORT `lw` right after V's last refusal, into `a0` (whose value is spent by then), checking "V PORT keeps 7 after its later refusals". It scores 95/95 on the fix and kills the COLOR_B, Y1 and COLOR_R refusal edits and the COLOR_B read edit (each 94/95). The COMMAND = 1 edits still need a SET_RESOLUTION session, or a disclosure.

4. **measured and read — question 1: the header's enumeration.**
   - **Claimed but not held:** none. Every listed cell has a row that kills its one-axis edit (table 4, plus my controls).
   - **Omitted:**
     - (a) COMMAND = 1, for every effect. The header lists only "0 and holding 2", and disclosure (3) mentions SET_RESOLUTION only as re-arm traffic.
     - (b) Cells 1-7 as state axes. The refusal and read effects are never observed with cells 2-7 non-zero.
     - (c) Effect 4, which lists only sessions V and K:
       - width `sh` — no cell is read after an `sh` refusal;
       - previous selectors 0, 2, 3, 4 and 6, and 5 for any cell but port 5;
       - COMMAND 0 for any cell but port 5.
     - (d) Effect 2's first-refusal value. No first refusal is a bit-63, 16, 0xff, 0x200000000 or all-ones value.
   - **Wording:** effect 2's "COMMAND 0 and 2 (V)" — V holds only 2; COMMAND 0 is held by P, F, W, X and R.

5. **measured — question 3: one disposition is wrong, C16.**
   - The rewritten contract's claim that every value of every axis is held is measured false (finding 2).
   - §2's statement that the class is closed falls with it. The rows closed the named instances in C1-C4, not the class: finding 2's edits have the same shape as C2 (a state only V's later refusals hold), reached through a different cell.
   - **C19 (KEEP) is right, and now for a measured reason.** `idata >= DEV_FBCTRL_NPORTS && !(d->warned_port && d->port[DEV_FBCTRL_PORT_COMMAND])` reds R's keeps row alone (93/94). It is the only row holding the "COMMAND non-zero and latched" joint cell. Record that as a joint cell (disclosure (0)'s class), not as an enumeration cell.
   - **C20 (REJECT) is right.** My F2 measurement showed that with D4's traffic inside P, M_gt ends the emulator at P's step 4 and blanks 14 rows (`opus549_measured/f2/proto_d4inP_summary.out`).
   - I have no objection to C10, C11 or C12.

---
*Recorded by the main loop: agent aabc7b9d2fb013ad5 (resumed), `agent_models.py` = clean, opus-5-5 throughout.*
