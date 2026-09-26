OPUS549F2_ALIVE

VERDICT: SHIP WITH CHANGES

All results are in `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\fbctrlportkill_20260924\opus549_measured\f2\` (the `TABLE_*.out` files; the probe copy is `fbctrl_port_probe.f2proto.py`).

**How I ran it:** in a new clone of `build/` at `/tmp/gxo549f2m`. Before the first run, `cmp` showed the clone's `dev_fbctrl.c` and the probe identical to the working tree (`2387e252`, `4a31bf36`). The base build used `rm src/cpus/*.o` and came out `4cc158f6`, the same binary as `build/gxemul`. For the 56 variant builds I deleted only `dev_fbctrl.o`, not the CPU objects, because the variants change only that one file. Every variant was checked fresh (`gxemul -nt` the source). All 25 table-2 rebuilds match table 2's recorded md5s exactly. The clone was restored from SEC, its md5 re-checked, and its sentinel cleared. At the end the working-tree inputs were still unchanged.

1. **measured — every D-target really does escape today.** All 17 target edits I built, plus N_clobcell, N_clobcmd, N_datarearm and N_runcmd, score 41/41 on the shipped probe (`TABLE_shipped_T.out`).

2. **measured — every corrected form goes red on its target and stays green on the fix.** The prototype scores 68/68 on the fix, plus 7/7 on the uncorrected-form ("diag") rows (`TABLE_proto_TN.out`).
   - **D2:** `sd 0x8000000000000000` after PORT=5 goes red on the bit-63 mask. **The uncorrected `sd 0x8000000000000005` stays green, so that form is vacuous.**
   - **D3:** a guest `lw` of PORT in session F, into a poisoned register, goes red on "store when the previous selector is 0". It also goes red on grok's constructor edit (`current_port = 1`). **The uncorrected form (printing a register nothing loaded) stays green on both, so it is vacuous.**
   - **D4:** red on N_datarearm and on a latch clear at the entry of `fbctrl_command()`.
   - **D5:**
     - N_clobcell: 5 rows red (X1, ports 0/1/3/7).
     - N_clobcmd: the port-0 row.
     - N_runcmd: X1 and ports 1 and 2.
   - **D6:** the `ld` reads `0x100000005` on the bit-32 edit, so it goes red.
   - **D7:** with a non-zero selector before each store, `sb`/`sh` of 0 go red on the len<4 edit and `sd` of 0 on the len==8 edit. An sh-only edit is caught **only** by an `sh` row, so add one. **The uncorrected form (stores from power-on) stays green on both edits, so it is vacuous.**
   - **D8:** "previous 6" goes red on `|= 1`; "previous 7" stays green, so both rows of the pair are needed.
   - **D9:**
     - Making 8 the first refusal reds the only-9 edit.
     - With twelve refusals and the count sampled at the **last** refusal (its own tag), `% 10` goes red.
     - Sampled at the 10th refusal it stays green, which confirms grok's point about where the count is read.
     - The serial_nr edit is 68/68 under `-E`, so vacuous there (see 6).
   - **D10:** the separate first-value check (the value followed by " is") reds print-0 in P and in F. The broad counter stays green on that edit. **The brief's narrow ONCE_RE (0x8/0x9 only) also reds print-0, but it loses the `% 10` kill:** the 11th re-announce (value 0x10) is not counted.
   - **D11:** with Y1 prefilled to 123 before GET_RESOLUTION, the row goes red on "Y1 set to 1" and on "Y1 line deleted". *Read:* without the prefill, the deleted-line version stays invisible, because Y1 starts at 0.
   - **Two rows the F2 list does not have, each the only row that kills its edit:**
     - Astra's "no announce anywhere in session A" row: kills an announce on accepted selector 6.
     - `sd` of 8 after PORT=5: kills grok's edit that refuses 8 only for 4-byte writes.

3. **measured — p2 variants against the prototype.**
   - Now red (they were 41/41): N_clobcell, N_clobcmd, N_datarearm, N_runcmd.
   - Still red: N_cmdport, N_cmdread, N_rdlatch, N_rdmask3, N_rearm.
   - Still 68/68:
     - **N_acc32 compiles to a binary identical to the fix (md5 `4cc158f6`).** It is an equivalent mutant, not an escape.
     - N_order: struct layout only.
     - N_datard16 and N_datawr8: DATA-width, out of scope.
     - N_rdmask7: *read* — equivalent as long as the selector stays in 0..7.

4. **measured — no table-2 regression.** The prototype keeps all 23 table-2 kills; M_static and M_noguard are still 68/68, as disclosed (`TABLE_proto_M.out`).

5. **measured — put D4 in its own session, not in P.** Placed in P as the brief wrote it, D4 still catches both of its targets. But M_gt (accepts 8) then ends the emulator at P's step 4 and blanks 14 P rows. In its own session, M_gt shows only its own 5 rows (`proto_d4inP_summary.out`).

6. **measured — Q2: a second instance is reachable without adding a device.**
   - `gxemul -V @cfg` with two `testmips` machine sections (only type, memory and load) builds two machines in one process, serials 1 and 2. `focus 0,<m>` selects each machine, and every `step 1` ran exactly one instruction on each machine, with no step where that failed.
   - With staggered programs on the fix: announce count is 1 after machine 0's first refusal and 2 after machine 1's; repeats stay silent; PORT keeps 5 on both. So the latch is per instance.
   - **M_static goes red** (machine 1's first refusal is silent: count 1, want 2).
   - The serial_nr edit goes red here, and also on a one-machine `serial_nr(2)` config (0 announces).
   - **On the correct build, running the shipped P program on both machines turns both shipped `== 1` count rows red (they read 2).**
   - Leaving machine 1 idle and changing only the probe's command line gives 41/41 on the fix, on M_static and on the serial_nr edit — no false red, but nothing caught either.
   - So a two-machine row has to count per instance, with programs staggered so each announce can be tied to its machine.
   - *Read:* whether a second machine from a config file counts as "added in order to reach the site" (witness ladder, clause iii) is for the adjudicator to decide. No code or device is added.

7. **measured — Q3: the row-deleted fixture passes gate 16 today.**
   - The block, verbatim from `gate_mips_folds.sh` lines 53-74, **passes `out_row_deleted` with 6 checks**.
   - One line added before the block's closing `fi` fixes it:
     `check "fbctrl_port rows emitted" "$(grep -cE '^  (ok|FAIL) ' "$FBCLOG")" "${fbres#*/}"`
     - Row-deleted: red (40 vs 41).
     - Good: still PASS (7 checks).
     - All 10 other fixtures: still red.
   - The alternative (count of `ok` lines against the numerator) behaves the same on these fixtures.
   - *Read:* the denominator form also catches a duplicated row whatever its status.
   - Details are in `TABLE_gate16.out`; the patched block is `g16_block_plus_rows.sh`.

8. **read — not examined:** P1-P3 and R1-R6. The `INPUTS.md5` already in f2/ belongs to the earlier seat and was not used; mine is `INPUTS_opusf2m.md5`. The built binaries exist only in `/tmp`; their md5s are in that file.

---
*Recorded by the main loop: agent aabc7b9d2fb013ad5, `agent_models.py` = clean, opus-5-5 throughout (17:29:02-18:02:56 UTC,
2026-09-25).  A FRESH seat: the previous Opus seat's F2 re-fire was stopped by a safety classifier on its very long resumed
context before it measured anything (a seat failure, recorded as one).  This answer landed AFTER Fable's F2 ruling.*
