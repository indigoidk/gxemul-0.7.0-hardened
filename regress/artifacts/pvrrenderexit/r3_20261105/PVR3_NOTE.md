# pvrrenderexit repair 3, step 2 -- codex pass 3's A-I and the Gemini swap-body cells, MEASURED on the 68-row probe (2026-11-05)

**Result: all fifteen of codex's single-site breaches SURVIVE the current 68-row probe (68/68 each), exactly as codex derived; so do
seven of the nine swap-body deletions both Gemini readings raised, and all eight cells the class closure found (W1-W4 per rasterizer,
step 2c below).**  Every one is a measured floor breach of the shipped detector (L2), repaired in-round by repair 3's rows.  The two swap-body deletions that do NOT survive (Xs, Xt: the x exchange deleted, the attributes
still exchanged) red `yedges swap` + `yedges s end` (or their texturedline twins), as predicted.

## Apparatus

* Instrument: `meas_AI/probe68_frozen.py` and `meas_SW/probe68_frozen.py`, both cmp-identical to `regress/pvr_zwrite_probe.py` at launch
  (md5 d14e90e8ca5f0c6e278f850debb850ff = `pvr_zwrite_probe.py.pre_r3`); the drivers refused to start otherwise.
* Variants: `pvr_variants_AI.py` (16: A-I per rasterizer where codex named two, plus It -- the texturedline twin of I that codex calls
  EQUIVALENT, built to measure that claim) and `pvr_variants_SW.py` (9: one exchange deleted inside each rasterizer's `if (x1 > x2)`
  block).  ONE exact edit of the fix each (GXEMUL-SEC dev_pvr.c == det_20261104/dev_pvr.c.fix, md5 481755b4...), occurrence counts
  checked; every diff is shown by `diff det_20261104/dev_pvr.c.fix meas_*/variants/<name>.c`.
* Drivers: `meas_AI.run.sh` (WSL clone /tmp/gxpvr3) and `meas_SW.run.sh` (WSL clone /tmp/gxpvr3b), each a `cp -a` of build/, each with a
  clone-local `.MUTANT` written before anything else and dev_pvr.c cmp-checked against GXEMUL-SEC; per variant `rm -f dev_pvr.o; make
  -j4` and `[ dev_pvr.o -nt dev_pvr.c ] && [ gxemul -nt dev_pvr.c ] && [ gxemul -nt dev_pvr.o ]` before the probe ran.  The base leg (the
  fix, built in the clone) scored 68/68 in both clones.  RESTORE (both): dev_pvr.c copied from GXEMUL-SEC, cmp clean, rebuilt, `[ gxemul
  -nt source ]`, 68/68, sentinel cleared (`MEAS.log` last lines); re-checked by hand afterwards: no `.MUTANT`, CMP_CLEAN, BIN_FRESH.
* Logs: `meas_AI/` and `meas_SW/` -- `SCORES.txt`, `MEAS.log`, `MD5.txt`, `build_<v>.log`, `probe_<v>.out`, `sessions_<v>/`.
* **Timeout check, as the brief required:** in every leg the ONLY session that ended by TIMEOUT was `texyedges`, every time, on the base
  and restored legs too.  That is not load: it is the STDIN CAP found in this step (below) -- texyedges sent 4104 bytes and its `quit`
  was swallowed.  All six of its pixel reads come before the cut, and no pixel in any leg read `none` (`grep -c none` = only the
  `neg apparatus` line and the `RED=none` line), so every score below is a real pixel reading.  Each leg took ~90.7 s for that reason.

## The table (68-row probe; a variant at 68/68 is a MEASURED SURVIVOR)

| variant | edit (one site) | rasterizer | score | red rows |
|---|---|---|---|---|
| As_start_m1 | `int x = x1` -> `int x = x1 - 1` | simpleline | 68/68 | none -- SURVIVED |
| At_start_m1 | the same | texturedline | 68/68 | none -- SURVIVED |
| Bs_swap_gt_p1 | `if (x1 > x2)` -> `if (x1 > x2 + 1)` | simpleline | 68/68 | none -- SURVIVED |
| Bt_swap_gt_p1 | the same | texturedline | 68/68 | none -- SURVIVED |
| Cs_swap_ge | `if (x1 > x2)` -> `if (x1 >= x2)` | simpleline | 68/68 | none -- SURVIVED |
| Ct_swap_ge | the same | texturedline | 68/68 | none -- SURVIVED |
| Ds_left_x2x2 | `(x1 < 0 && x2 < 0)` -> `(x2 < 0 && x2 < 0)` | simpleline | 68/68 | none -- SURVIVED |
| Dt_left_x2x2 | the same | texturedline | 68/68 | none -- SURVIVED |
| Es_right_x1x1 | `(x1 >= xsize && x2 >= xsize)` -> `(x1 >= xsize && x1 >= xsize)` | simpleline | 68/68 | none -- SURVIVED |
| Et_right_x1x1 | the same | texturedline | 68/68 | none -- SURVIVED |
| Fs_zoff_eq_refused | `vram_z <= z` -> `vram_z < z \|\| (!zwrite_disabled && vram_z == z)` | simpleline | 68/68 | none -- SURVIVED |
| Ft_zoff_eq_refused | the same | texturedline | 68/68 | none -- SURVIVED |
| G_decode_eq1 | `(list[1] >> 26) & 1` -> `== 1` | case-4 decode | 68/68 | none -- SURVIVED |
| H_decode_and5 | `& 1` -> `& 5` | case-4 decode | 68/68 | none -- SURVIVED |
| Is_end_lt_p1 | `x <= x2` -> `x < x2 + 1` | simpleline | 68/68 | none -- SURVIVED |
| It_end_lt_p1 | the same (codex: EQUIVALENT, integer ends) | texturedline | 68/68 | none -- green, as the equivalence predicts |
| Zs_swap_noz | swap body: `tmpf = z1; z1 = z2; z2 = tmpf;` deleted | simpleline | 68/68 | none -- SURVIVED |
| Rs_swap_nor | swap body: the r1/r2 exchange deleted | simpleline | 68/68 | none -- SURVIVED |
| Gs_swap_nog | swap body: the g1/g2 exchange deleted | simpleline | 68/68 | none -- SURVIVED |
| Bs_swap_nob | swap body: the b1/b2 exchange deleted | simpleline | 68/68 | none -- SURVIVED |
| Xs_swap_nox | swap body: `double tmpf = x1; x1 = x2; x2 = tmpf;` -> `double tmpf = x1;` | simpleline | 66/68 | yedges_swap, yedges_s_end (0x0000: the reversed span loops from 435 down and draws nothing) -- REFUTED as a survivor; predicted |
| Zt_swap_noz | swap body: `double tmpf = z1; z1 = z2; z2 = tmpf;` -> `double tmpf = z1;` | texturedline | 68/68 | none -- SURVIVED |
| Ut_swap_nou | swap body: the u1/u2 exchange deleted | texturedline | 68/68 | none -- SURVIVED |
| Vt_swap_nov | swap body: the v1/v2 exchange deleted | texturedline | 68/68 | none -- SURVIVED |
| Xt_swap_nox | swap body: `int tmp = x1; x1 = x2; x2 = tmp;` -> `int tmp = x1; (void) tmp;` | texturedline | 66/68 | texyedges_swap, texyedges_s_end (0x0000) -- REFUTED as a survivor; predicted |

**Codex's fifteen (A-I): 15 of 15 measured survivors; none refuted.**  **Gemini's swap body: 7 of 9 survivors** (z, r, g, b in
simpleline; z, u, v in texturedline) -- the coordinator asked for at least the two z deletions; all nine were built.  Codex's claim that
texturedline's `x < x2 + 1` is EQUIVALENT is consistent with It's 68/68 (green), and table 3 re-measures it on the 85-row probe (predicted
green there too, CLOSURE3.md).

Why each survived (all derived by codex or by Gemini and now measured): every probed span is either forward, wider than one pixel, or flat
(z 2.0 and one colour or texel at every vertex), and no probed pixel sits just before an exact span start, just past a fractional span
end, or on a span whose ends are equal with different attributes; no reversed span crosses a screen edge; no Z-off polygon meets a
stored depth equal to its own; and no header sets bit 26 together with a higher bit, or bits 28-31 without it.

## Step 2c -- the cells the CLASS CLOSURE found beyond codex and Gemini, measured the same way (meas_W/)

The closure (CLOSURE3.md) found four more single-site cells per rasterizer that no 68-row-probe row could see; per the brief's
measure-first discipline they were built and run on the SAME 68-row probe before any row was added for them.  `pvr_variants_W.py`,
driver `meas_W.run.sh` (WSL clone /tmp/gxpvr3d, clone-local `.MUTANT`, frozen probe cmp-identical to `pvr_zwrite_probe.py.pre_r3`,
base 68/68, same build freshness checks, restore cp + cmp + rebuild + freshness before the sentinel goes).

| variant | edit (one site) | score | |
|---|---|---|---|
| W1s / W1t | `x > 0` -> `x > d->zwrite_disabled` (an operand swap from a field the body reads: Z-off polygons lose column 1) | 68/68 each | SURVIVED |
| W2s / W2t | `y < 0` -> `y < d->zwrite_disabled` (Z-off polygons lose row 0) | 68/68 each | SURVIVED |
| W3s / W3t | `(x1 < 0 && ...)` -> `(x1 < d->bytes_per_pixel && ...)` (the left clause's x1 compare moved up by 2) | 68/68 each | SURVIVED |
| W4s / W4t | `(... && x2 < 0)` -> `(... && x2 < d->bytes_per_pixel)` (its x2 compare moved up by 2) | 68/68 each | SURVIVED |

All eight are measured survivors (floor breaches of the shipped detector).  Why: every row-0 and column-1 pixel the 68-row probe read
was drawn by a Z-ON polygon (for which W1 and W2 are the fix itself), and no probed span had an end in [1, 2) on the side the clause
tests -- a move of the left clause by ONE is equivalent (L1, measured green in table 2) because it only changes column 0, which is
never drawn, so TWO is the compare's edge.  Rows added: `zleft row 0` (W1, W2), `edges2 l tip` (W3), `zleft tip` (W4), + textured.

## Found while measuring: THE STDIN CAP (a new wrong record, f)

Every leg above took ~90.7 s, and every leg's texyedges session ended by TIMEOUT, base and restored included.  Table 1's 51-row probe took
0.4 s a run; table 2's 68-row probe took 90.5 s on every one of its 68 legs.  Cause, measured (`stdin_cap_test.out`,
`stdin_cap_test2.out`, both read-only uses of build/gxemul):

* A `reg`-only session acts on stdin of any length (8000 bytes: exit 0) -- so it is not a plain byte limit.
* A session that runs `step 1` loses its input past a fixed point: preamble + `r7/pc/step` loads, 4100 bytes exit 0, 4150 bytes and
  longer TIMEOUT with exactly 349 prompts processed whatever the length.  Moving the first `step` ~1500 bytes later moves the cut by the
  same amount (5600 exit 0; 6000 TIMEOUT at 724 prompts).
* Mechanism, from the source: the debugger's console FIFO (`console.c`, CONSOLE_FIFO_LEN 4096) refills in 100-byte reads while 101 bytes
  are free, so it holds ~4000 bytes ahead of what it has consumed; the first `step` runs the Dreamcast maple keyboard's tick for the first
  time (`machine.c`: every tick starts at ticks_till_next 0; `dev_dreamcast_maple.c` DEVICE_TICK(maple) calls console_readchar on its own
  input-only console handle, which reads the host's stdin when no slave xterms are in use), and that tick takes every byte still in the
  pipe as key presses.  In this probe the first step ends at byte 100 of each session's input, when the FIFO has read 4000 + 100 bytes:
  **the cap is 4100 bytes.**
* texyedges (repair 2) sent **4104 bytes**: its `quit` arrived as `q` (`r2_20261105/base68/sessions_b/texyedges.txt` ends `GXemul> q`) and
  every probe run since repair 2 has waited out the 90 s session timeout.  Its six pixel reads all precede the cut, so its rows -- and
  table 2's scores -- measured what they claim.  base68's first-run "16-command mask session" (6088 bytes) was the same cap: its
  transcript stops after ~4100 bytes of input, mid-`step`, not because the session was slow (a whole probe's other sessions run in
  under a second).
* Records this makes false: the gate comment's "about half a second" (true of the 51-row probe; the 68-row probe took ~90 s), the probe's
  "a session sending sixteen TA commands outran the 90 s session limit", and the brief's instruction "keep each session to about 8 [TA
  commands]" as the limit -- the limit is 4100 bytes of debugger input per session (yedges carries ten TA commands in 4054 bytes).
* Repair: texyedges stores only the red texel it samples (4104 -> 4060 bytes), and `session()` refuses an input longer than STDIN_CAP =
  4096 before running anything (a design-time error, like the existing 16-character row-name assert).  Every repair-3 session is sized
  under it (`sizing/`: largest new session 3972 bytes, largest overall texyedges 4060).  The 91-row probe runs in ~2 s on build/ with no
  session timing out (`base91/`), and the 128-row probe (with the Z-off twins) in ~3 s (`base128/`).
* Table 2's one exception: Y2t's texyedges session died by SIGSEGV (its undefined behaviour) before it could hang -- `probe_Y2t_tex_ltm1.out`
  elapsed 1.4 s.  Every other table-2 leg on a gxemul binary waited the 90 s.

ADDENDUM 2026-11-05 (repair 4; codex pass 4 F5 and F6, upheld by ../adj_p4_20261105/ADJ_MYTHOS_local.md section 3).  Two lines above are
stale against the delivered 128-row probe and are left as written, dated here rather than rewritten:
* F5 -- "table 3 re-measures it on the 85-row probe" (the It paragraph): that was the plan at the 85-row stage.  The delivered table 3
  ran on the 128-row probe (table3/probe128_frozen.py) and measured It green there, 128/128, as predicted (table3/SCORES.txt).
* F6 -- "largest new session 3972 bytes, largest overall texyedges 4060" (the STDIN CAP repair): that was the 91-row stage's sizing.
  The delivered 128-row probe's largest session is ztyedges at 4066 bytes (CLOSURE3.md section 5; codex pass 4's read-only
  enumeration agrees).  Repair 4's 140-row probe keeps ztyedges, 4066, the largest of its 48 sessions; its new and changed sessions
  are swap 4011, zswap 4017, half 3937, zhalf 3943, ramp8 2738, zramp8 3092, texramp8 3235, ztramp8 3241 (../r4_20261105/PVR4_NOTE.md).
