# #549 fbctrlportkill -- THE VERIFYING PASS: the closing-F2 repair's own pass (the chain closes on a valid zero)

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`** (and `GXEMUL-SEC/regress/`).  There are THREE pristine-2021-upstream
copies of GXemul under the project root (`./src/` and two under `_archive/audit-results-*/builds/`).  They are NOT this
fork.  If your line numbers disagree with mine by hundreds you are reading one of them — say so rather than reconciling.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any premise you cannot settle from
this packet rather than guessing at it.  **ENUMERATE rather than reason** where a claim is arithmetic, and ask what the
PRODUCER of a value can actually emit before walking a domain.

**VERDICT LINE FIRST**: `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then numbered findings.

## 1. WHAT THIS PASS IS

`src/devices/dev_fbctrl.c` (the test machines' framebuffer controller) STORED an out-of-range PORT selector with only a
warning; the next DATA access then ended the emulator process in the DATA arm's range check (rung-3 witness at HEAD:
`regress/artifacts/fbctrlportkill_20260924/witness_HEAD/witness_HEAD.out`, arm K `HOST-DIED ... exit=1`).  `#549`
REFUSES any selector >= 8, compared on the full 64-bit value, keeps the previous one, and announces the refusal once per
device.  **The fix has not changed since pass 2**; every seat that read it agrees it is right.  The detector,
`regress/fbctrl_port_probe.py`, has been through pass 2, an F2 pass, a closing pass and a closing F2 pass, each of which
found cells its rows had left empty.

The closing F2 pass's adjudication (Fable 5.1, `closing2/fable5_close2.md`) ruled: **no floor breach**; the claim was
wrong (L4); and **the repair owes its own pass** -- "build table 5; run ONE pass scoped to the repair diff, the floor
question asked of the shipped 101-row composite; it closes on the first valid zero carried with its denominator."
**This is that pass.**  The composite is now 111 rows (section 3).

## 2. SETTLED PREMISES, RE-INLINED SO NOBODY SPENDS AN ANSWER RE-DERIVING THEM

* **The fixed PORT arm -- verbatim except that the #549 comment is CONDENSED to its first sentence and `...`**
  (`src/devices/dev_fbctrl.c`, `DEVICE_ACCESS(fbctrl)`; the enclosing function's common
  tail is `if (writeflag == MEM_READ) memory_writemax64(cpu, data, len, odata); return 1;`):

```c
	case DEV_FBCTRL_PORT:
		if (writeflag == MEM_READ)
			odata = d->current_port;
		else if (idata >= DEV_FBCTRL_NPORTS) {
			/*  #549: an out-of-range selector is REFUSED, and
			    current_port keeps its previous, always-valid value.  ...  */
			if (!d->warned_port) {
				fatal("[ fbctrl: port number 0x%llx is out of range; "
				    "the selector is unchanged (once) ]\n",
				    (unsigned long long) idata);
				d->warned_port = 1;
			}
		} else
			d->current_port = idata;
		break;
```
  `idata` is `uint64_t` (loaded only on writes, so it is 0 on a read); `current_port`, `warned_port` and `port[8]` are
  `int`.  The DATA arm keeps its old range check (`fatal` + `exit(1)`) as a tripwire, unreachable while PORT refuses.
* **The floor, as Fable ruling 1 states it:** the arm's body tests the access direction, `idata >= DEV_FBCTRL_NPORTS`
  and `!d->warned_port`, and reads and writes `current_port`.  The previous selector's VALUE, the COMMAND cell
  (`port[0]`) and the data cells (`port[1..7]`) are NOT tested by the body -- no partition of them is in the fix -- so
  an edit conditioned on them is clause-(e) coverage, held only where the contract lists it.
* **SET_RESOLUTION at X1 = Y1 = 0 is safe to send** (MEASURED on the fix): `fbctrl_command()` calls
  `dev_fb_resize(vfb, 0, 0)`, which prints `dev_fb_resize(): size too small (0 x 0); ignored.` and returns.  Both of
  session Y's commands printed exactly that (`<scratchpad>/fbctrl549/v5/y_buf.out`).

## 3. WHAT CHANGED (the repair, v4 -> v5, 94 -> 111 rows, 13 -> 15 sessions)

* **X3's first refusal 0x100000003 -> 0x100000005** (grok, grok dedicated): as an int 0x100000003 is 3 -- the kept
  selector itself -- so X3's keep row could not tell a refusal from a store.
* **A name row for every X session and for V** (grok dedicated, glm): the announce must name the refused value.
* **X4's first refusal 9 by sw -> all-ones by sd**: the largest value, negative when signed -- so an announce suppressed
  above ANY threshold or on the sign bit reds (minimax's `idata < K`, the Opus seat's `(int64_t) idata >= 0`).
* **V: a PORT read right after its later refusals, "V PORT keeps 7"** (the Opus seat, measured): the only state with
  cells 1-7 non-zero during a refusal was never followed by a PORT read.
* **A new session Y holding COMMAND = 1** (deepseek, grok, the Opus seat): SET_RESOLUTION (declined at 0 x 0), its first
  refusal (keeps 5, announces once, names 0x9), SET_RESOLUTION again between refusals, a second refusal (keeps 5, count
  still 1), COMMAND read back 1 as a control.
* **A new session Z**: later refusals at previous selectors 0-4 (no session refused twice there), so "the later refusals
  are silent" holds at every selector.
* **The header**: the floor warrant naming `current_port`; the enumeration restated cell by cell with its holders; the
  disclosures widened ((0) the one held pair; (3) the except-value and demotion forms; (8) cell values and effect 4);
  and R's basis corrected -- it said an edit accepting 8 would blank P's rows; what was MEASURED is that D4's traffic,
  placed inside P after its refused 8, ended the process under M_gt at P's step 4.
* **Table 5 GENERATES one one-axis edit per listed cell** from the listing itself (`mutants549_t5.py`, `CELLMAP.out`).
  **Found while building it (L4, mine): table 4 built no one-axis announce edit for previous 2, 3, 4, 6, 7 or for the
  single widths sb, sh, sd, while v4's header said every listed cell was measured.**

## 4. MEASURED

* The fix (build/gxemul, md5 b5b99e6d) under v5: 111/111, CONTROL=OK, 8.9 s.  Table 5's base line: `base_fix rc=0 FBCTRLP_RESULT=111/111 FBCTRLP_CONTROL=OK FBCTRLP_DONE`.
* **Kill table 5**: 212 edits of the fix -- table 4's 101 plus 111 new (the generated cells and the closing-F2 seats'
  edits) -- each built in a WSL scratch clone and scored by a frozen copy of v5.  **192 red, 20 at the total,
  0 against their written prediction, 0 build failures.**  The pre-table addendum
  (`PRETABLE_ADDENDUM_t5.out`) and the predictions (`table5/MANIFEST.out`) were written before the run; their mtimes
  prove the order.
* **Gate 16 on the working tree** (the v5 probe + the 111-pin block), run alone: `gate 16: MIPS fold witness (#388): PASS (26 checks)`, 13 s (`gates_t5/gate16.out`).  **Its negative fixtures, re-run on that 111-row log**: the good log passes, and a deleted row, a failed row with the trailer left intact, a duplicated row, an honest failed row, a deleted row with the trailer edited and a SUBSTITUTED row each go red on the check designed for them (`closing3/g16_fixtures_t5.out`).

## 5. THE EVIDENCE, INLINED (disclosure: `regress/fbctrl_port_probe.py` INLINED as a diff against v4;
## `regress/gate_mips_folds.sh` INLINED as a diff against the 94-row block; `src/devices/dev_fbctrl.c` UNCHANGED since
## pass 2, its PORT arm inlined in section 2; `tools/` and the records NOT SHOWN -- unchanged by this repair)

### 5a. table 5, per mutant (regress/artifacts/fbctrlportkill_20260924/table5/TABLE.out; predictions from mutants_t5/MANIFEST.out, written before the run)

```
A1_not10                   111/111  predicted GREEN(e)  measured GREEN 
A2_sb3                     111/111  predicted GREEN(e)  measured GREEN 
B_mod11                    110/111  predicted RED       measured RED   
B_mod12                    111/111  predicted GREEN(e)  measured GREEN 
CELL_acc_0_w1              110/111  predicted RED       measured RED   
CELL_acc_0_w2              110/111  predicted RED       measured RED   
CELL_acc_0_w4              107/111  predicted RED       measured RED   
CELL_acc_0_w8              110/111  predicted RED       measured RED   
CELL_acc_7_w1              110/111  predicted RED       measured RED   
CELL_acc_7_w2              110/111  predicted RED       measured RED   
CELL_acc_7_w4              105/111  predicted RED       measured RED   
CELL_acc_7_w8              108/111  predicted RED       measured RED   
CELL_acc_l0                 47/111  predicted RED       measured RED   
CELL_acc_l1                100/111  predicted RED       measured RED   
CELL_acc_s0                104/111  predicted RED       measured RED   
CELL_acc_s1                 81/111  predicted RED       measured RED   
CELL_acc_s2                107/111  predicted RED       measured RED   
CELL_acc_s3                107/111  predicted RED       measured RED   
CELL_acc_s4                106/111  predicted RED       measured RED   
CELL_acc_s5                 74/111  predicted RED       measured RED   
CELL_acc_s6                106/111  predicted RED       measured RED   
CELL_acc_s7                102/111  predicted RED       measured RED   
CELL_ann_c0                 92/111  predicted RED       measured RED   
CELL_ann_c1                108/111  predicted RED       measured RED   
CELL_ann_c2                108/111  predicted RED       measured RED   
CELL_ann_p0                109/111  predicted RED       measured RED   
CELL_ann_p2                108/111  predicted RED       measured RED   
CELL_ann_p3                109/111  predicted RED       measured RED   
CELL_ann_p4                109/111  predicted RED       measured RED   
CELL_ann_p6                109/111  predicted RED       measured RED   
CELL_ann_p7                109/111  predicted RED       measured RED   
CELL_ann_w1                108/111  predicted RED       measured RED   
CELL_ann_w2                107/111  predicted RED       measured RED   
CELL_ann_w8                107/111  predicted RED       measured RED   
CELL_cell_c0own            110/111  predicted RED       measured RED   
CELL_cell_c2               108/111  predicted RED       measured RED   
CELL_cell_p1               110/111  predicted RED       measured RED   
CELL_cell_p5own            110/111  predicted RED       measured RED   
CELL_cell_p7               107/111  predicted RED       measured RED   
CELL_cell_w1               110/111  predicted RED       measured RED   
CELL_cell_w4               108/111  predicted RED       measured RED   
CELL_cell_w8               110/111  predicted RED       measured RED   
CELL_keep_c0                63/111  predicted RED       measured RED   
CELL_keep_c1               106/111  predicted RED       measured RED   
CELL_keep_c2               105/111  predicted RED       measured RED   
CELL_keep_l0                53/111  predicted RED       measured RED   
CELL_keep_p5                83/111  predicted RED       measured RED   
CELL_keep_p6               107/111  predicted RED       measured RED   
CELL_keep_w1               103/111  predicted RED       measured RED   
CELL_keep_w2               102/111  predicted RED       measured RED   
CELL_keep_w4                85/111  predicted RED       measured RED   
CELL_keep_w8                98/111  predicted RED       measured RED   
CELL_name_c0               104/111  predicted RED       measured RED   
CELL_name_c1               110/111  predicted RED       measured RED   
CELL_name_c2               110/111  predicted RED       measured RED   
CELL_name_p0               110/111  predicted RED       measured RED   
CELL_name_p1               110/111  predicted RED       measured RED   
CELL_name_p2               110/111  predicted RED       measured RED   
CELL_name_p3               110/111  predicted RED       measured RED   
CELL_name_p4               110/111  predicted RED       measured RED   
CELL_name_p5               109/111  predicted RED       measured RED   
CELL_name_p6               110/111  predicted RED       measured RED   
CELL_name_p7               110/111  predicted RED       measured RED   
CELL_name_w1               110/111  predicted RED       measured RED   
CELL_name_w2               109/111  predicted RED       measured RED   
CELL_name_w4               107/111  predicted RED       measured RED   
CELL_name_w8               109/111  predicted RED       measured RED   
CELL_rd_c0                  64/111  predicted RED       measured RED   
CELL_rd_c1                 109/111  predicted RED       measured RED   
CELL_rd_c2                 108/111  predicted RED       measured RED   
CELL_rd_l0                  92/111  predicted RED       measured RED   
CELL_rd_l1                  79/111  predicted RED       measured RED   
CELL_rd_s0                 111/111  predicted GREEN(eq) measured GREEN 
CELL_rd_s1                  95/111  predicted RED       measured RED   
CELL_rd_s2                  95/111  predicted RED       measured RED   
CELL_rd_s3                  95/111  predicted RED       measured RED   
CELL_rd_s4                  94/111  predicted RED       measured RED   
CELL_rd_s5                  73/111  predicted RED       measured RED   
CELL_rd_s6                  94/111  predicted RED       measured RED   
CELL_rd_s7                  90/111  predicted RED       measured RED   
CELL_rd_w1                 110/111  predicted RED       measured RED   
CELL_rd_w2                 110/111  predicted RED       measured RED   
CELL_rd_w4                  63/111  predicted RED       measured RED   
CELL_rd_w8                 110/111  predicted RED       measured RED   
CELL_sil_c0                108/111  predicted RED       measured RED   
CELL_sil_c1                110/111  predicted RED       measured RED   
CELL_sil_c2                109/111  predicted RED       measured RED   
CELL_sil_p0                110/111  predicted RED       measured RED   
CELL_sil_p1                110/111  predicted RED       measured RED   
CELL_sil_p2                110/111  predicted RED       measured RED   
CELL_sil_p3                110/111  predicted RED       measured RED   
CELL_sil_p4                110/111  predicted RED       measured RED   
CELL_sil_p5                107/111  predicted RED       measured RED   
CELL_sil_p6                110/111  predicted RED       measured RED   
CELL_sil_p7                109/111  predicted RED       measured RED   
CELL_sil_tr_nop            110/111  predicted RED       measured RED   
CELL_sil_tr_portread       106/111  predicted RED       measured RED   
CELL_sil_tr_setres         110/111  predicted RED       measured RED   
CELL_sil_w1                109/111  predicted RED       measured RED   
CELL_sil_w2                109/111  predicted RED       measured RED   
CELL_sil_w4                106/111  predicted RED       measured RED   
CELL_sil_w8                107/111  predicted RED       measured RED   
CF2_DM_ge16                111/111  predicted GREEN(e)  measured GREEN 
CF2_G_mask8                108/111  predicted RED       measured RED   
CF2_G_namesel              102/111  predicted RED       measured RED   
CF2_KM_not16               111/111  predicted GREEN(e)  measured GREEN 
CF2_MX_thresh              109/111  predicted RED       measured RED   
CF2_O_ann_bit63            109/111  predicted RED       measured RED   
CF2_O_cl_c0                111/111  predicted GREEN(e)  measured GREEN 
CF2_O_cl_len2              111/111  predicted GREEN(e)  measured GREEN 
CF2_O_cl_p5                111/111  predicted GREEN(e)  measured GREEN 
CF2_O_rd_colorb            110/111  predicted RED       measured RED   
CF2_O_ref_colorb           110/111  predicted RED       measured RED   
CF2_O_ref_colorr           110/111  predicted RED       measured RED   
CF2_O_ref_y1               110/111  predicted RED       measured RED   
C_ann_nw4                  100/111  predicted RED       measured RED   
C_ann_p5                   104/111  predicted RED       measured RED   
C_rd_w4only                108/111  predicted RED       measured RED   
C_ref_p0                   108/111  predicted RED       measured RED   
C_ref_p7                   106/111  predicted RED       measured RED   
E_ann_cmd                  105/111  predicted RED       measured RED   
E_ann_p1                   110/111  predicted RED       measured RED   
E_ann_w4                   100/111  predicted RED       measured RED   
E_cmdset                   105/111  predicted RED       measured RED   
E_rd_cmd                   106/111  predicted RED       measured RED   
E_rd_w4                    109/111  predicted RED       measured RED   
E_ref_cmd                  100/111  predicted RED       measured RED   
E_ref_p1                   109/111  predicted RED       measured RED   
E_ref_p2                   107/111  predicted RED       measured RED   
E_ref_p3                   108/111  predicted RED       measured RED   
E_ref_p4                   107/111  predicted RED       measured RED   
G1_rewrite1                110/111  predicted RED       measured RED   
G2_rdrearm                 109/111  predicted RED       measured RED   
G3a_cmdrearm               109/111  predicted RED       measured RED   
G3b_getresrearm            110/111  predicted RED       measured RED   
G4_pad16                   109/111  predicted RED       measured RED   
G5a_noexit                 111/111  predicted GREEN(e)  measured GREEN 
G5b_checkop                111/111  predicted GREEN(e)  measured GREEN 
G6_trunc32                 109/111  predicted RED       measured RED   
G7_ldbit32                 111/111  predicted GREEN(e)  measured GREEN 
G8_clob8                   110/111  predicted RED       measured RED   
L1_rebit63                 110/111  predicted RED       measured RED   
M_acc4                      91/111  predicted RED       measured RED   
M_acclatch                 100/111  predicted RED       measured RED   
M_and5                     104/111  predicted RED       measured RED   
M_ann_any                  101/111  predicted RED       measured RED   
M_bit                      101/111  predicted RED       measured RED   
M_clamp                     81/111  predicted RED       measured RED   
M_debug                    109/111  predicted RED       measured RED   
M_decl                     106/111  predicted RED       measured RED   
M_gt                       103/111  predicted RED       measured RED   
M_i32                       98/111  predicted RED       measured RED   
M_i64                      106/111  predicted RED       measured RED   
M_latch0                   105/111  predicted RED       measured RED   
M_latchcnt                  85/111  predicted RED       measured RED   
M_latchinv                  85/111  predicted RED       measured RED   
M_mod33                    109/111  predicted RED       measured RED   
M_noguard                  111/111  predicted GREEN(e)  measured GREEN 
M_perval                   107/111  predicted RED       measured RED   
M_reflatch                  92/111  predicted RED       measured RED   
M_rej2                     107/111  predicted RED       measured RED   
M_reset0                    79/111  predicted RED       measured RED   
M_revert                    53/111  predicted RED       measured RED   
M_static                   111/111  predicted GREEN(e)  measured GREEN 
M_store                     78/111  predicted RED       measured RED   
M_u32                      103/111  predicted RED       measured RED   
M_wide                      94/111  predicted RED       measured RED   
N_acc32                    111/111  predicted GREEN(e)  measured GREEN 
N_clobcell                 106/111  predicted RED       measured RED   
N_clobcmd                  109/111  predicted RED       measured RED   
N_cmdport                  107/111  predicted RED       measured RED   
N_cmdread                  107/111  predicted RED       measured RED   
N_datard16                 111/111  predicted GREEN(e)  measured GREEN 
N_datarearm                108/111  predicted RED       measured RED   
N_datawr8                  111/111  predicted GREEN(e)  measured GREEN 
N_order                    111/111  predicted GREEN(e)  measured GREEN 
N_rdlatch                   79/111  predicted RED       measured RED   
N_rdmask3                   75/111  predicted RED       measured RED   
N_rdmask7                  111/111  predicted GREEN(e)  measured GREEN 
N_rearm                    105/111  predicted RED       measured RED   
N_runcmd                   108/111  predicted RED       measured RED   
R_partAB                   104/111  predicted RED       measured RED   
R_state1                   105/111  predicted RED       measured RED   
S_ann_cp                   109/111  predicted RED       measured RED   
S_rd_idata                 104/111  predicted RED       measured RED   
S_ref_wp                   108/111  predicted RED       measured RED   
T_D10_print0               102/111  predicted RED       measured RED   
T_D11a_y1one               110/111  predicted RED       measured RED   
T_D11b_y1keep              110/111  predicted RED       measured RED   
T_D2_mask63                110/111  predicted RED       measured RED   
T_D3_ctor1                 110/111  predicted RED       measured RED   
T_D3_pwron                 110/111  predicted RED       measured RED   
T_D4b_cmdrearm             109/111  predicted RED       measured RED   
T_D6_rdbit32               110/111  predicted RED       measured RED   
T_D7a_sub4zero             109/111  predicted RED       measured RED   
T_D7b_sdzero               110/111  predicted RED       measured RED   
T_D7c_shzero               110/111  predicted RED       measured RED   
T_D8_or1                   105/111  predicted RED       measured RED   
T_D9a_only9                102/111  predicted RED       measured RED   
T_D9b_mod10                110/111  predicted RED       measured RED   
T_D9c_serial1              111/111  predicted GREEN(e)  measured GREEN 
T_W_sb0                    110/111  predicted RED       measured RED   
T_W_sb7                    110/111  predicted RED       measured RED   
T_W_sb8                    109/111  predicted RED       measured RED   
T_W_sd7                    107/111  predicted RED       measured RED   
T_W_sh7                    110/111  predicted RED       measured RED   
T_W_sh8                    110/111  predicted RED       measured RED   
T_W_sw0                    103/111  predicted RED       measured RED   
T_W_sw7                    103/111  predicted RED       measured RED   
T_W_sw8                    107/111  predicted RED       measured RED   
T_X_ann6                   109/111  predicted RED       measured RED   
T_X_w8                     107/111  predicted RED       measured RED   
```

### 5b. the probe, v4 -> v5 (regress/fbctrl_port_probe.py)

```diff
--- regress/fbctrl_port_probe.py	2026-09-25 15:52:10.923727600 -0500
+++ regress/fbctrl_port_probe.py	2026-09-25 16:04:41.095787200 -0500
@@ -25,7 +25,9 @@
      and the one announce must name the first refused value, 0x8.
   R  re-arm: PORT=5, refuse 9, read PORT, a DATA write to port 5, a NOP command (PORT=0, DATA=0), a DATA READ of port 5,
      a GET_RESOLUTION command (PORT=0, DATA=2), PORT=5, refuse 9: the count is still 1 and PORT keeps 5.  Its own
-     session, so an edit that accepts 8 cannot blank P's rows.
+     session because DATA traffic inside P can end the process: when the F2 prototype put such traffic in P, after
+     its refused 8, an edit that accepts 8 (M_gt) ended the emulator at P's step 4 and blanked 14 of P's rows
+     (regress/artifacts/fbctrlportkill_20260924/opus549_measured/f2/proto_d4inP_summary.out).
   K  the witness pair, repaired: PORT=5, DATA=0x2a, PORT=9 refused, then a DATA READ (must survive and read port 5's
      0x2a) and a DATA WRITE of 0x77 (must land in port 5: read back through PORT=5).
   F  free-running: a refused PORT write at power-on and a guest `lw` of PORT execute INSIDE `continue`, which stops at a
@@ -33,39 +35,62 @@
      so while free-running debug() is below its threshold and returns without printing, while fatal() prints: a refusal
      announced with debug() would pass every stepped row and fail here.
   V  cells: COMMAND=GET_RESOLUTION, X1=123, one refusal while COMMAND holds 2 and PORT=1 -- PORT must still read 1,
-     X1 must stay 123, and that FIRST refusal must announce; ports 1-7 filled with 0x11*p, five refusals (9, 16,
-     0x100000003 by sd, 0xff by sb, 8), then all eight cells read back and the count is still 1.
+     X1 must stay 123, and that FIRST refusal must announce, naming 0x9; ports 1-7 filled with 0x11*p (the last fill
+     selects 7), five refusals (9, 16, 0x100000003 by sd, 0xff by sb, 8), PORT read at once (it must still say 7),
+     then all eight cells read back and the count is still 1.
   W  widths: selector 0 written by sb, sh, sw and sd and selector 7 by sb, sh and sw, each after PORT=5 (accepted);
      8 by sb, sh and sd after PORT=5 (refused -- the FIRST, by sb, must announce); 0x8000000000000000 by sd after
      PORT=5 (refused); 9 after PORT=6 (keeps 6); then `lb`, `lh` and `ld` of PORT with selector 5 (exactly 5 each).
-  X2 X3 X4 X6 X7  five fresh devices, each: PORT=k, then its FIRST refusal (9 by sh after 2; 0x100000003 by sd after 3,
-     whose announce must name that wide value; 9 by sw after 4; 9 by sb after 6; 0x100 by sh after 7): it announces
-     exactly once and PORT keeps k.
-
-CONTRACT (clause e) -- AN ENUMERATION, NOT A LIST.  The fixed arm's inputs are the access (a PORT write, refused or
-accepted; a PORT read), its width, the value, and the device state an edit could condition on: the previous selector,
-the latch, and the COMMAND cell.  For each EFFECT below, EVERY value of EVERY one of those axes is held by some row, so
-an edit that conditions the fix on ONE axis value is caught; the kill of each cell's one-axis edit is measured in
-regress/artifacts/fbctrlportkill_20260924/table4/TABLE.out.  This is the class closure: pass 2, the F2 pass and the
-closing pass each found such an edit on an axis the rows had left partly empty.
-  a refusal keeps the previous selector -- width sb/sh/sw/sd (P, W); previous 0 (F), 1 (V), 2 3 4 (X), 5 (P), 6 (W),
-      7 (P, X7); COMMAND 0 (P) and holding 2 (V); latch unset (P's first) and set (the rest)
-  the first refusal announces once, the rest are silent -- first-refusal width sw (P) sb (W) sh (X2, X7) sd (X3);
-      previous 0 (F), 1 (V), 2 3 4 6 7 (X), 5 (P); COMMAND 0 and 2 (V); silence across PORT reads, a DATA write and a
-      DATA read, a NOP and a GET_RESOLUTION (R), accepted selectors and twelve refusals (P); the value named: 0x8 (P),
-      0x9 (F), the wide 0x100000003 (X3)
-  a PORT read returns the selector -- lb lh ld (W) and lw (every session); every selector 0-7 (A); COMMAND holding 2
-      (V); latch unset (A) and set (P)
-  a refusal leaves every cell alone -- all eight cells after refusals of 8, 9, 16, 0x100000003 (sd) and 0xff (sb) with
-      COMMAND holding 2 (V), and port 5's after a refused 9 with COMMAND 0 (K)
-  an accepted selector is stored -- 0 and 7 at every width (W, A), every selector at one width (A)
+  X2 X3 X4 X6 X7  five fresh devices, each: PORT=k, then its FIRST refusal (9 by sh after 2; 0x100000005 by sd after 3
+     -- wide, and 5 as an int, never 3; all-ones by sd after 4 -- the largest value, and negative as a signed one; 9 by
+     sb after 6; 0x100 by sh after 7): it announces exactly once, the announce names that value, and PORT keeps k.
+  Y  COMMAND = 1: PORT=0 and DATA=1 run SET_RESOLUTION with X1 = Y1 = 0 from power-on, which dev_fb_resize() declines
+     with a message ("size too small ... ignored"), so nothing is resized; PORT=5; its FIRST refusal, 9 by sw -- PORT
+     keeps 5, and it announces once, naming 0x9; SET_RESOLUTION again, as traffic between refusals; PORT=5 and a second
+     refusal, 0x100000003 by sd (3 as an int, never 5) -- PORT keeps 5 and the count is still 1; COMMAND reads back 1.
+  Z  silence across selectors: PORT=2 and its FIRST refusal (9), then PORT=0, 1, 2, 3 and 4, each followed by a refusal
+     of 9 -- the count is still 1 after all six, and PORT keeps 4.
+
+CONTRACT (clause e) -- AN ENUMERATION, NOT A LIST.
+THE FLOOR.  The fixed PORT arm's body tests three things -- the access direction, the written value (`idata >=
+DEV_FBCTRL_NPORTS`, on all 64 bits) and the latch (`!warned_port`) -- and it reads and writes `current_port`.  Every
+cell of those is held: the value's magnitude, width and class, the latch unset and set, a read and a write.  The
+previous selector (current_port's VALUE), the COMMAND cell and the data cells are NOT tested by the body -- the fix
+makes no partition of them -- so an edit conditioned on one of them is coverage beyond the floor (clause e): the rows
+hold the values listed below and claim nothing more.  For each EFFECT, each value listed is held by the session(s)
+named, and the one-axis edit of every listed cell is measured red in
+regress/artifacts/fbctrlportkill_20260924/table5/TABLE.out.  This is the class closure: pass 2, the F2 pass, the
+closing pass and the closing F2 pass each found such an edit on a value the rows had left empty.
+  a refusal keeps the previous selector -- width sb sh sw sd (P, W); previous 0 (F), 1 (V), 2 3 (X), 4 (X4, Z), 5 (P,
+      W, Y), 6 (W, X6), 7 (P, V, X7); COMMAND 0 (P), 1 (Y), 2 (V); latch unset (each session's first refusal) and set
+      (the rest)
+  the first refusal announces once -- width sw (P, V, F, Y, Z) sb (W, X6) sh (X2, X7) sd (X3, X4); previous 0 (F), 1
+      (V), 2 (X2, Z), 3 4 6 7 (X), 5 (P, W, Y); COMMAND 0 (P, F, W, X, Z), 1 (Y), 2 (V); the first-refused value from 8
+      (P, W) to all-ones (X4)
+  the later refusals are silent -- width sb (P) sh (P, W) sw (P, V, W, R, Z) sd (P, V, W, Y); previous 0-4 (Z), 5 (P, W,
+      R, Y), 6 (W), 7 (P, V); COMMAND 0 (P, W, Z), 1 (Y), 2 (V, R); across PORT reads, a DATA write, a DATA read, a NOP
+      and a GET_RESOLUTION (R), a SET_RESOLUTION (Y), accepted selectors and twelve refusals (P)
+  the announce names the refused value -- 0x8 (P), 0x9 (F, V, X2, X6, Y), 0x100 (X7), the wide 0x100000005 (X3),
+      all-ones (X4): width sw (P, F, V, Y) sb (X6) sh (X2, X7) sd (X3, X4); previous 0 (F), 1 (V), 2 3 4 6 7 (X), 5 (P,
+      Y); COMMAND 0 (P, F, X), 1 (Y), 2 (V)
+  a PORT read returns the selector -- lb lh ld (W) and lw (every session); every selector 0-7 (A); COMMAND 0 (A), 1
+      (Y), 2 (V); latch unset (A) and set (P)
+  a refusal leaves the cells alone -- all eight cells after refusals of 9, 16, 0x100000003 (sd), 0xff (sb) and 8 at
+      previous selector 7 with COMMAND 2 (V); X1 after a refusal of 9 (sw) at previous 1 with COMMAND 2 (V); port 5's
+      cell after a refused 9 (sw) at previous 5 with COMMAND 0 (K) -- and no other cell, width, selector or COMMAND
+      value (NOT CLAIMED (8))
+  an accepted selector is stored -- 0 and 7 at every width (W, A), every selector at one width (A); latch unset (A, W)
+      and set (V's fills and Z's selections, after their first refusals)
 Beyond the effects: the store of an out-of-range value, clamped, masked or reset; the compare narrowed or signed (bit
 63 alone, bits 32-33, 32-bit truncation); a boundary slip at 8; an announce on an accepted selector; an announce
-demoted to debug(); and the pre-#549 process exit on DATA.
+demoted to debug() (F); an announce suppressed above or below any threshold, or on the sign bit (the first refusals
+run from 8 to all-ones); and the pre-#549 process exit on DATA.
 NOT CLAIMED (disclosed).  (0) An edit conditioned on TWO axes at once -- a joint cell such as "refuse 9 only by sb after
 PORT=3", or "`ld` sets bit 32 except at selector 5" -- is caught only where a row happens to hold that pair; the
 enumeration above is one-axis by design, and closing every pair is the unbounded growth the carrier's floor rules
-refuse.  (1) A process-global latch instead of the per-instance field, and an announce conditioned on
+refuse.  One pair is held and is recorded as a pair, not as a class: COMMAND non-zero with the latch set, before a PORT
+read (R's second refusal; V's and Y's later ones) -- in the 94-row probe R was its only holder (the Opus closing-F2
+seat, J_ref_cmdlatch).  (1) A process-global latch instead of the per-instance field, and an announce conditioned on
 the machine's serial number.  The probe's `-E testmips` session has ONE fbctrl.  A second instance IS reachable without
 adding a device -- two testmips machines in one process from a config file, `gxemul @config` -- and there the
 process-global latch reds (measured by the Opus F2 seat, opus549_measured/f2/TABLE_twoinst.out), but that is a new
@@ -74,16 +99,22 @@
 `exit(1)`, weakening `>=` to `>`, or swapping its operand -- is unreachable while the PORT arm refuses, because no
 out-of-range selector is ever stored; the check is KEPT as a tripwire.  It exits before it indexes, so an index of 8
 cannot reach `warned_port` while it stands, and `port[8]` would be undefined behaviour, not a defined alias of the
-latch.  (3) An exception for one value no row writes (`idata != 10`), a re-announce period of twelve or more, a
-re-arm by SET_RESOLUTION traffic (no row sends command 1: it resizes the framebuffer), and an announce whose value is
-mangled only for a value that is never a session's first refusal: the value space is 2^64, and no finite row set
-closes "except value k".  (4) Equivalent
-edits: storing `(uint32_t) idata` (it compiles to the fix's own binary), reordering the struct's fields, masking the PORT
-read with 7 (the selector is always 0..7).  (5) `printf` in place of `fatal()`: indistinguishable in THIS invocation's
-output.  (6) Narrowing the DATA path's widths, and the device's OTHER two process-ending calls -- fbctrl_command()'s
-default (any command other than 0-2, including the documented but unimplemented FILL/COPY) and the access function's
-default (any offset other than 0x00/0x10): filed as `fbctrlcmdkill` and `fbctrloffkill`.  (7) Edits to this instrument's
-own logic are reviewed, not rowed.
+latch.  (3) An exception for one value no row writes (`idata != 10`), a re-announce period of twelve or more, an
+announce suppressed or mangled only for one value no session refuses first (`idata != 16`), and an announce demoted to
+debug() for some values but not F's 9 -- only a free-running session tells debug() from fatal() here, and F is the
+only one: the value space is 2^64, and no finite row set closes "except value k".  (A threshold is not in this class;
+see "Beyond the effects".)  (4) Equivalent edits: storing `(uint32_t) idata` (it compiles to the fix's own binary),
+reordering the struct's fields, masking the PORT read with 7 (the selector is always 0..7).  (5) `printf` in place of
+`fatal()`: indistinguishable in THIS invocation's output.  (6) Narrowing the DATA path's widths, and the device's OTHER
+two process-ending calls -- fbctrl_command()'s default (any command other than 0-2, including the documented but
+unimplemented FILL/COPY) and the access function's default (any offset other than 0x00/0x10): filed as `fbctrlcmdkill`
+and `fbctrloffkill`.  (7) Edits to this instrument's own logic are reviewed, not rowed.  (8) The data cells' VALUES are
+not an axis the rows enumerate.  An edit conditioned on a cell's value (`port[COLOR_B] == 0`, `port[Y1] != 0`) is
+caught only where a row's refusal or read holds a triggering state, and the states held are: every cell 0 (F, W, X),
+port 5 at 0x2a (P, K, R), X1 at 123 with COMMAND 2 (V's first refusal), ports 1-7 at 0x11*p with COMMAND 2 (V's later
+refusals and the PORT read right after them), and COMMAND 1 (Y).  Effect 4 is claimed only as listed: no cell is read
+back after an `sh` refusal, after a refusal at previous selector 0, 2, 3, 4 or 6, or under COMMAND 1, and port 5's is
+the only cell read back after a refusal at previous 5 or under COMMAND 0.
 LIMITS OF A ROW.  Session P re-selects PORT=5 before each refusal, so a refused selector cannot carry over into the next
 row WHEN THE LEGAL SELECTION LANDS; an edit that also refuses legal selections defeats the re-select, and later rows
 then inherit its value (M_acclatch).  Every read-back is taken after its session ends, so a session that dies part-way
@@ -401,11 +432,12 @@
 for p in range(1, 8):
     PROG_V += [("sw", "s%d" % p, 0, None), ("sw", "t%d" % p, 16, None)]
 PROG_V += [("sw", "a0", 0, None), ("sw", "a1", 0, None), ("sd", "a2", 0, None), ("sb", "a3", 0, None),
-           ("sw", "t9", 0, "vlast")]
+           ("sw", "t9", 0, "vlast"),
+           ("lw", "a0", 0, None)]                                 # PORT at once: must still read 7 (a0 is spent)
 PROG_V += [("sw", "zr", 0, None), ("lw", "v1", 16, None)]
 for p in range(1, 8):
     PROG_V += [("sw", "s%d" % p, 0, None), ("lw", "s%d" % p, 16, None)]
-READS_V = ["s0", "v0", "v1"] + ["s%d" % p for p in range(1, 8)]
+READS_V = ["s0", "v0", "v1", "a0"] + ["s%d" % p for p in range(1, 8)]
 
 #  W: the width x boundary cells, each after its own non-zero predecessor into a poisoned read-back; then an ld.
 W_CELLS = [("accept 0 written by sb after PORT=5", "a0", "sb", "zr", "s0", 0, None),
@@ -431,9 +463,30 @@
            ("sw", "a0", 0, None), ("lh", "a2", 0, None)]
 READS_W = [c[4] for c in W_CELLS] + ["t9", "a1", "a2"]
 
+#  Y: COMMAND holds 1.  SET_RESOLUTION with X1 = Y1 = 0 (power-on) is declined by dev_fb_resize() with a message,
+#  so nothing is resized; it runs twice, the second time between the two refusals.  The second refused value,
+#  0x100000003, is 3 as an int -- never the kept 5.
+PROG_Y = [("sw", "zr", 0, None), ("sw", "a1", 16, None),               # PORT=0, DATA=1: SET_RESOLUTION (0 x 0)
+          ("sw", "a0", 0, None), ("sw", "t1", 0, "y1st"),               # PORT=5, refuse 9 while COMMAND holds 1
+          ("lw", "s0", 0, None),                                        # PORT must still read 5
+          ("sw", "zr", 0, None), ("sw", "a1", 16, None),                # SET_RESOLUTION again: traffic
+          ("sw", "a0", 0, None), ("sd", "t2", 0, "ylast"),              # PORT=5, refuse 0x100000003 (sd)
+          ("lw", "s1", 0, None),                                        # PORT must still read 5
+          ("sw", "zr", 0, None), ("lw", "s2", 16, None)]                # COMMAND reads back 1
+REGS_Y = [("t0", FBCTRL), ("a0", 5), ("a1", 1), ("t1", 9), ("t2", 0x100000003), ("s0", 0xdead), ("s1", 0xdead),
+          ("s2", 0xdead)]
+
+#  Z: later refusals at selectors 0-4 (the X sessions and F refuse only once, so nothing else holds silence there).
+PROG_Z = [("sw", "s2", 0, None), ("sw", "t1", 0, "z1st")]               # PORT=2, the FIRST refusal
+for _r in ("zr", "s1", "s2", "s3", "s4"):                             # PORT=0..4, each then refused
+    PROG_Z += [("sw", _r, 0, None), ("sw", "t1", 0, None)]
+PROG_Z[-1] = ("sw", "t1", 0, "zlast")
+PROG_Z += [("lw", "s0", 0, None)]                                       # PORT must still read 4
+REGS_Z = [("t0", FBCTRL), ("s1", 1), ("s2", 2), ("s3", 3), ("s4", 4), ("t1", 9), ("s0", 0xdead)]
+
 #  X: five fresh devices -- the first-refusal cells (previous selector x width) no other session's first refusal holds.
 #  Each: PORT=k, its FIRST refusal (tag x), then a PORT read into a poisoned register.
-X_CELLS = [("X2", 2, "sh", 9), ("X3", 3, "sd", 0x100000003), ("X4", 4, "sw", 9), ("X6", 6, "sb", 9),
+X_CELLS = [("X2", 2, "sh", 9), ("X3", 3, "sd", 0x100000005), ("X4", 4, "sd", M64), ("X6", 6, "sb", 9),
            ("X7", 7, "sh", 0x100)]
 
 
@@ -453,6 +506,8 @@
         F = session("F", PROG_F, REGS_F, ["t2"], stub, free_run=True)
         V = session("V", PROG_V, REGS_V, READS_V, stub)
         W = session("W", PROG_W, REGS_W, READS_W, stub)
+        Y = session("Y", PROG_Y, REGS_Y, ["s0", "s1", "s2"], stub)
+        Z = session("Z", PROG_Z, REGS_Z, ["s0"], stub)
         X = []
         for lab, k, w, v in X_CELLS:
             prog, regs = prog_x(k, w, v)
@@ -474,7 +529,7 @@
     ctl.append(row("C SIGNATURE: Y1 zeroed by GET_RESOLUTION", hx(C["vals"].get("s3")), "0x0",
                    "(prefilled 123)"))
     row("C nothing refused, no (once) line", len(ONCE_RE.findall(C["buf"])), 0)
-    for lab, S in (("A", A), ("P", P), ("R", R), ("K", K), ("V", V), ("W", W)):
+    for lab, S in (("A", A), ("P", P), ("R", R), ("K", K), ("V", V), ("W", W), ("Y", Y), ("Z", Z)):
         ctl.append(row("%s disassembly of every stepped word" % lab, len(S["badis"]), 0))
     ctl.append(row("X2-X7 disassembly of every stepped word", sum(len(S["badis"]) for S in X), 0))
     print("ACCEPT (session A: %s %d/%d)" % (A["status"], A["steps"], A["n"]))
@@ -509,7 +564,9 @@
     print("CELLS (session V: %s %d/%d)" % (V["status"], V["steps"], V["n"]))
     row("V refuse 9 while COMMAND holds 2, PORT keeps 1", hx(V["vals"].get("s0")), "0x1")
     row("V that first refusal (COMMAND holding 2) announces", V["once_after"].get("v1st"), 1)
+    row("V the announce names the refused value 0x9", first_val(V), "0x9")
     row("V X1=123 survives a refusal (COMMAND holds 2)", hx(V["vals"].get("v0")), hx(123))
+    row("V PORT keeps 7 after its later refusals", hx(V["vals"].get("a0")), "0x7")
     row("V port 0 (COMMAND) still 2 after five refusals", hx(V["vals"].get("v1")), "0x2")
     for p in range(1, 8):
         row("V port %d keeps its fill after five refusals" % p, hx(V["vals"].get("s%d" % p)), hx(0x11 * p))
@@ -522,13 +579,23 @@
     row("ld of PORT reads exactly 5", hx(W["vals"].get("t9")), "0x5")
     row("lb of PORT reads exactly 5", hx(W["vals"].get("a1")), "0x5")
     row("lh of PORT reads exactly 5", hx(W["vals"].get("a2")), "0x5")
+    print("COMMAND 1 (session Y: %s %d/%d)" % (Y["status"], Y["steps"], Y["n"]))
+    ctl.append(row("Y COMMAND reads back 1 (SET_RESOLUTION held)", hx(Y["vals"].get("s2")), "0x1"))
+    row("Y refuse 9 while COMMAND holds 1, PORT keeps 5", hx(Y["vals"].get("s0")), "0x5")
+    row("Y that first refusal (COMMAND holding 1) announces", Y["once_after"].get("y1st"), 1)
+    row("Y the announce names the refused value 0x9", first_val(Y), "0x9")
+    row("Y refuse 0x100000003 (sd) after SET_RESOLUTION, PORT keeps 5", hx(Y["vals"].get("s1")), "0x5")
+    row("Y announce still exactly 1 after SET_RESOLUTION and a second refusal", Y["once_after"].get("ylast"), 1)
+    print("SILENCE ACROSS SELECTORS (session Z: %s %d/%d)" % (Z["status"], Z["steps"], Z["n"]))
+    row("Z the first refusal (after PORT=2) announces", Z["once_after"].get("z1st"), 1)
+    row("Z announce still exactly 1 after refusals at selectors 0-4", Z["once_after"].get("zlast"), 1)
+    row("Z PORT keeps 4 after its refusals", hx(Z["vals"].get("s0")), "0x4")
     print("FIRST REFUSALS (sessions X2-X7: %s)" % " ".join("%s %d/%d" % (S["status"], S["steps"], S["n"])
                                                           for S in X))
     for (lab, k, w, v), S in zip(X_CELLS, X):
         row("%s refuse 0x%x (%s) after PORT=%d, PORT keeps %d" % (lab, v, w, k, k), hx(S["vals"].get("s0")), hx(k))
         row("%s that FIRST refusal announces exactly once" % lab, S["once_after"].get("x"), 1)
-        if v >= 1 << 32:
-            row("%s the announce names the wide value 0x%x" % (lab, v), first_val(S), "0x%x" % v)
+        row("%s the announce names the refused value 0x%x" % (lab, v), first_val(S), "0x%x" % v)
     control = all(ctl)
     n_ok, n = sum(RESULTS), len(RESULTS)
     print("FBCTRLP_CONTROL=%s" % ("OK" if control else "FAILED"))
```

### 5c. gate 16's block (regress/gate_mips_folds.sh), 94 -> 111

```diff
--- regress/gate_mips_folds.sh	2026-09-25 16:37:44.881098300 -0500
+++ regress/gate_mips_folds.sh	2026-09-25 16:37:53.913279300 -0500
@@ -43,15 +43,18 @@
 #  this gate's pmax-kernel check: a missing kernel still skips the fold rows below, and
 #  gate_skip reports FAIL, not SKIP, if an fbctrl row failed first.
 #
-#  THE CONTRACT is the probe's header (its ENUMERATION and NOT CLAIMED).  Kill table 4
-#  (regress/artifacts/fbctrlportkill_20260924/table4/TABLE.out, plus table4b/ for the one
-#  edit whose first build did not compile) built 101 edits: the 87 the contract does not
-#  disclose are ALL red, HEAD's own arm among them (M_revert, 51/94 here, and sessions K and R
-#  ended the process); the 14 it discloses score 94/94 -- a process-global latch, a serial-
-#  number condition, three edits of the DATA arm's kept check, two joint cells, one value no
-#  row writes, a re-announce period of twelve, three equivalent edits and two DATA-width
-#  edits.  The device still ends the process through its command and offset defaults, which
-#  are filed, not claimed.
+#  THE CONTRACT is the probe's header (its ENUMERATION and NOT CLAIMED).  Kill table 5
+#  (regress/artifacts/fbctrlportkill_20260924/table5/TABLE.out) built 212 edits -- table 4's
+#  101, one one-axis edit GENERATED for every cell the header lists (table5/CELLMAP.out), and
+#  the closing-F2 seats' edits -- each with its prediction written first (table5/MANIFEST.out):
+#  the 192 the contract does not disclose are ALL red, HEAD's own arm among them (M_revert,
+#  53/111 here, and sessions K and R ended the process); the 20 it discloses score 111/111 --
+#  a process-global latch, a serial-number condition, three edits of the DATA arm's kept check,
+#  two joint cells, one value no row writes, a re-announce period of twelve, four equivalent
+#  edits, two DATA-width edits, three refusal-time cell writes no row reads back, and two
+#  announce forms keyed to one value or a value range.  Every prediction held.  The device
+#  still ends the process through its command and offset defaults, which are filed, not
+#  claimed.
 #
 #  `gatedevicesplit` is OWED (#498): one more device probe in a CPU gate, as #548 added to
 #  gate 14.  Recorded, not compounded silently.
@@ -78,8 +81,8 @@
     #  quoted numerator is inert to that tool BY DESIGN -- it reads only the denominator's
     #  line -- and the exit row above and the two reconciliation rows below are what catch a
     #  red or an edited score.
-    check "fbctrl_port rows run" "${fbres#*/}" 94
-    check "fbctrl_port rows correct" "${fbres%/*}" "94"
+    check "fbctrl_port rows run" "${fbres#*/}" 111
+    check "fbctrl_port rows correct" "${fbres%/*}" "111"
     check "fbctrl_port rows failed" "$(grep -c '^  FAIL ' "$FBCLOG")" "0"
     #  RECONCILE the rows the probe PRINTED with the trailer it printed (#549 F2, measured by
     #  the Opus seat): checking the trailer alone, a log with one row deleted and its
```

## 6. QUESTIONS

1. **THE FLOOR QUESTION, of the shipped 111-row composite: is there a CLEAN-SWEEP mutant in the fix's DEPENDS-ON
   enumeration** -- an edit of the access direction, of `idata >= 8` (value, width, class), of `!warned_port`, or of
   what the arm writes to `current_port`, alone or at a joint cell of those, that scores 111/111?  Name the edit and
   the row you expect to stay green.  A zero is only a zero WITH ITS DENOMINATOR: say which cells and which edit shapes
   you swept.
2. **VERIFY THE ENUMERATION, not the table.**  For each cell the header lists (section 5b, the CONTRACT), is its
   generated edit (section 5a; the `CELL_*` names say the cell) really an edit of THAT cell, and does the row the header
   names really hold it?  Is any listed cell held by no row, or any row credited to a cell it cannot see?
3. **The disclosures (0)-(8)**: is anything disclosed actually held now (so it should be claimed), or anything claimed
   that the rows do not hold?  Is (8) -- the cell values and effect 4 -- stated exactly?
4. **The smallest edit to the FIX that keeps all 111 rows green**, outside the disclosed classes.
5. **Wrong records** in the v5 header or the gate comment: a quote marked verbatim that is not; a count without its
   source; R's corrected basis; anything true of v4 and false of v5.

If, while verifying a claim, you found something ELSE -- say so.
