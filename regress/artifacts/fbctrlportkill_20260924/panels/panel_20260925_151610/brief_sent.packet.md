# #549 fbctrlportkill -- THE CLOSING §F2 PASS: every closing-pass finding, my disposition on each, and the repair (measured)

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

Check the premises, not just the derivations.  **THE TREE UNDER REVIEW IS `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`**;
other copies of GXemul under the project root are not this fork.  If you read files, read ONLY
`src/devices/dev_fbctrl.c`, `src/include/testmachine/dev_fb.h`, `regress/fbctrl_port_probe.py`,
`regress/gate_mips_folds.sh`, and this round's `regress/artifacts/fbctrlportkill_20260924/{closing2,table4,table4b}/`.
If you cannot read files that is expected: everything you need is inlined, and a premise you cannot settle from the
packet should be NAMED, not guessed.  **FIRST LINE: `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`**, then
numbered findings.  **The load-bearing question: WHICH OF MY DISPOSITIONS BELOW IS WRONG?  Name the count.**  If you
raised a finding, be HARDER on it than on anyone else's, including whether the repair I made for it is right.

## 1. SETTLED PREMISES (re-inlined; do not re-derive)

* `fatal()` PRINTS AND RETURNS; only an explicit `exit(1)` ends the process.
* The fix is unchanged since pass 1 except one comment sentence (narrowed in F2): the PORT arm refuses `idata >= 8` on
  the full `uint64_t`, keeps the previous selector, announces once per device through the struct member `warned_port`
  with the marker `(once)`; the DATA arm's range check and `exit(1)` are KEPT as a tripwire.  The command default and
  the offset default still end the process: out of scope, filed (`fbctrlcmdkill`, `fbctrloffkill`).
* The closing pass (panel_20260925_141420: agy, grok, glm, deepseek, minimax SHIP WITH CHANGES, kimi-k3:cloud SHIP;
  codex WALLED -- usage limit until 2026-09-26 07:01 -- a seat failure; the kimi CLI on its weekly wall, covered) plus
  the dedicated grok job (SHIP WITH CHANGES) and the Opus 5.5 measuring seat (SHIP WITH CHANGES: ten 73/73 escapes
  MEASURED inside the DEPENDS-ON enumeration, one restoring the process exit).
* Owner ruling 2026-09-25: while codex is walled, Fable adjudicates on the seats that answer and Astra confirms after
  the reset; nothing is committed before Astra confirms.

## 2. WHY THE REPAIR IS A CLASS CLOSURE, NOT MORE ROWS

Pass 2 found a width-conditioned escape; F2 found another; the closing pass found edits conditioned on the previous
selector, the COMMAND cell and the read width -- the same class three passes running.  The carrier's rule: when two
consecutive passes find breaches of one class, the next repair ENUMERATES the class from the function's own inputs,
closes every cell in ONE diff, and writes into the contract which cells are covered and which are deliberately not.
So the probe's header is now an ENUMERATION: for each effect (a refusal keeps the selector; the first refusal announces
once and the rest are silent; a PORT read returns the selector; a refusal leaves every cell alone; an accepted selector
is stored) EVERY value of EVERY single axis (width, value class, previous selector 0-7, latch, COMMAND cell, the traffic
between refusals) is held by some row, and joint (two-axis) cells are disclosed as clause (e).

## 3. THE FINDINGS AND MY DISPOSITIONS (each "ROWED" one is MEASURED red in table 4, §5)

* **C1 (Opus E_ref_p1..p4; grok, kimi, grok ded. G1):** refusal skipped or rewritten after selectors 1-4 -> ROWED: V
  reads PORT right after its first refusal (selector 1, COMMAND holding 2); X2 X3 X4 are fresh devices refusing after 2,
  3, 4.
* **C2 (Opus E_ref_cmd -- restores the process exit):** refusal skipped while COMMAND != 0 -> ROWED (V).
* **C3 (Opus E_rd_w4, E_rd_cmd):** PORT read qualified by width / by COMMAND -> ROWED: lb and lh of PORT (W); a PORT
  read with COMMAND holding 2 (V).
* **C4 (Opus E_ann_w4/p1/cmd, E_cmdset; grok ded.):** the announce suppressed by width, previous selector or COMMAND,
  or the latch SET by a command -> ROWED: counts in V (first refusal at selector 1 with COMMAND 2) and W (first refusal
  by sb), and five fresh X devices whose FIRST refusal is by sh/sd/sw/sb/sh after 2/3/4/6/7.
* **C5 (glm; grok ded. G2 G3):** the latch re-armed by a DATA READ, a non-NOP command, GET_RESOLUTION -> ROWED: R's
  traffic between its refusals now includes a DATA read and a GET_RESOLUTION.
* **C6 (glm L1):** a re-announce keyed to a value only W refuses -> ROWED (W's count after its five refusals).
* **C7 (grok ded. G4):** the padding stores (16 by sb/sh) accepted unobserved -> ROWED (P reads both back).
* **C8 (minimax, grok ded. G6):** the announced value truncated to 32 bits -> ROWED: X3's FIRST refusal is
  0x100000003 by sd, and its announce must name that value.
* **C9 (grok ded. G8):** COMMAND's cell cleared only on a refused 8 -> ROWED (V now refuses 8 before reading the cells).
* **C10 (grok ded. G5a, G5b):** the DATA check blinded without deleting it (only `exit(1)` removed; its operand swapped)
  -> DISCLOSED, NOT CLAIMED (2) widened: any edit of the kept check is unreachable while the PORT arm refuses.
* **C11 (grok ded. G7; agy):** joint cells (`ld` sets bit 32 except at selector 5; 3 refused only by sb) -> DISCLOSED,
  NOT CLAIMED (0), new: an edit on TWO axes at once is caught only where a row holds that pair.
* **C12 (agy, deepseek, kimi, glm, grok):** `idata != 10`; a period of twelve -> DISCLOSED, NOT CLAIMED (3), unchanged.
* **C13 (grok):** the gate does not pin row identity (a row replaced by a copy of another keeps every count) ->
  REPAIRED: a row-names-unique check; its fixture MEASURED red only on that check (§5).
* **C14 (grok):** A's "accept selector 0 written by sw" cannot see an ignored store (power-on is 0) -> LIMITS note; the
  cell is held by W's row after PORT=5.
* **C15 (grok, deepseek, minimax):** "each new cell has its own one-edit target" was false -> the targets T_W_sd7,
  T_W_sw8, T_W_sb0 were BUILT (red), and the sentence is replaced by the enumeration.
* **C16 (grok ded., agy, glm):** contract claims true only as measured ("cleared by DATA or command traffic", "a PORT
  read that sets a high bit (by lw and by ld)", "an announce naming another value", "a refusal that writes a port
  cell") -> the contract is REWRITTEN as the enumeration; each claim now names the cells it covers.
* **C17 (grok ded.):** the gate comment's "M_revert ... every refusal row red" was false (V's rows stay green) ->
  rewritten ("51/94 here").  **C18 (deepseek):** "the 8 it discloses" read as exhaustive -> rewritten (14, by category).
* **C19 (the R keeps row; agy/grok keep, grok ded. drop, Opus redundant-but-keep):** KEPT -- with R's traffic now
  including a DATA read and a GET_RESOLUTION it is the keeps-after-command-traffic cell, and Opus's two-part edit
  (R_partAB) reds it (with V's rows).
* **C20 (grok ded.): "R's own session because an edit accepting 8 ends P" is false** -> REJECTED: the header says an
  edit accepting 8 cannot blank P's rows, which is the design reason (R's DATA traffic would end the process inside P
  under M_gt, as the Opus F2 seat measured when D4 sat in P); true as written.

## 4. THE REPAIR DIFF (the closing pass reviewed the 73-row probe; this is 73 -> 94, and the gate block)

### 4a. regress/fbctrl_port_probe.py, 73 -> 94 rows

```diff
--- a/regress/fbctrl_port_probe.py (the 73-row probe the closing pass reviewed)
+++ b/regress/fbctrl_port_probe.py (the 94-row class closure)
@@ -18,44 +18,66 @@
      there, and a banked register WITHOUT command execution would read 123); no `(once)` line may appear.
   A  accept: all EIGHT selectors, written at widths 1, 2, 4 and 8, each read back through PORT; ports 1-7 round-trip
      a distinct DATA value (port 0 is COMMAND and is written only with NOP); no `(once)` line may appear.
-  P  refusal, anchored to a previous selector: PORT=5 (DATA 0x2a), then nine out-of-range writes -- 8, 9, 16 (sw),
-     0x200000000, 0x100000003, all-ones (sd), all-ones (sw), 0xff (sb), 0x100 (sh) -- each PRECEDED by a fresh PORT=5
-     and followed by a PORT read that must still say 5; two more (16 by sb, 16 by sh); then PORT=7 and a refused 9 must
-     leave 7 -- twelve refusals.  The `(once)` count must be exactly 1 right after the FIRST refusal and still 1 after
-     the twelfth, and the one announce must name the first refused value, 0x8.
-  R  re-arm: PORT=5, refuse 9, read PORT, a DATA write to port 5, a NOP command (PORT=0, DATA=0), PORT=5, refuse 9: the
-     count is still 1 and PORT keeps 5.  Its own session, so an edit that accepts 8 cannot blank P's rows.
+  P  refusal, anchored to a previous selector: PORT=5 (DATA 0x2a), then eleven out-of-range writes -- 8, 9, 16 (sw),
+     0x200000000, 0x100000003, all-ones (sd), all-ones (sw), 0xff (sb), 0x100 (sh), 16 (sb), 16 (sh) -- each PRECEDED
+     by a fresh PORT=5 and followed by a PORT read that must still say 5; then PORT=7 and a refused 9 must leave 7 --
+     twelve refusals.  The `(once)` count must be exactly 1 right after the FIRST refusal and still 1 after the twelfth,
+     and the one announce must name the first refused value, 0x8.
+  R  re-arm: PORT=5, refuse 9, read PORT, a DATA write to port 5, a NOP command (PORT=0, DATA=0), a DATA READ of port 5,
+     a GET_RESOLUTION command (PORT=0, DATA=2), PORT=5, refuse 9: the count is still 1 and PORT keeps 5.  Its own
+     session, so an edit that accepts 8 cannot blank P's rows.
   K  the witness pair, repaired: PORT=5, DATA=0x2a, PORT=9 refused, then a DATA READ (must survive and read port 5's
      0x2a) and a DATA WRITE of 0x77 (must land in port 5: read back through PORT=5).
   F  free-running: a refused PORT write at power-on and a guest `lw` of PORT execute INSIDE `continue`, which stops at a
      breakpoint after them; the lw must read 0 and the announce must name 0x9.  This invocation passes -V and no -v,
      so while free-running debug() is below its threshold and returns without printing, while fatal() prints: a refusal
      announced with debug() would pass every stepped row and fail here.
-  V  cells: COMMAND=GET_RESOLUTION, X1=123, one refusal while COMMAND still holds 2 (X1 must stay 123); ports 1-7
-     filled with 0x11*p, four refusals (9, 16, 0x100000003 by sd, 0xff by sb), then all eight cells read back.
+  V  cells: COMMAND=GET_RESOLUTION, X1=123, one refusal while COMMAND holds 2 and PORT=1 -- PORT must still read 1,
+     X1 must stay 123, and that FIRST refusal must announce; ports 1-7 filled with 0x11*p, five refusals (9, 16,
+     0x100000003 by sd, 0xff by sb, 8), then all eight cells read back and the count is still 1.
   W  widths: selector 0 written by sb, sh, sw and sd and selector 7 by sb, sh and sw, each after PORT=5 (accepted);
-     8 by sb, sh and sd after PORT=5 (refused); 0x8000000000000000 by sd after PORT=5 (refused); 9 after PORT=6 (keeps
-     6); an `ld` of PORT with selector 5 (exactly 5).
-
-CONTRACT (clause e).  CATCHES, each with a measured kill in regress/artifacts/fbctrlportkill_20260924/table3/TABLE.out:
-the store reached for an out-of-range value (or a clamped, masked or reset one); the compare narrowed or signed (bit 63
-alone, bits 32-33, 32-bit truncation); a boundary slip at 8; a refusal or an acceptance conditioned on the access width
--- the cells {0, 7} accepted and 8 refused are rowed at EVERY width, 1, 2, 4 and 8 (the class closure, after pass 2 and
-the F2 pass each found a width-conditioned escape); a legal selector refused; a refusal that rewrites the previous
-selector (from 0, 5, 6 and 7); a refusal that writes a port cell or runs a command; a latch never set, set late, keyed
-per value, cleared by DATA or command traffic, re-armed by an accepted selector or by a count whose period is eleven or
-less; an announce on an accepted selector; an announce naming another value; an announce demoted to debug(); a PORT
-read that sets a high bit (by lw and by ld); and the pre-#549 process exit on DATA.
-NOT CLAIMED (disclosed).  (1) A process-global latch instead of the per-instance field, and an announce conditioned on
+     8 by sb, sh and sd after PORT=5 (refused -- the FIRST, by sb, must announce); 0x8000000000000000 by sd after
+     PORT=5 (refused); 9 after PORT=6 (keeps 6); then `lb`, `lh` and `ld` of PORT with selector 5 (exactly 5 each).
+  X2 X3 X4 X6 X7  five fresh devices, each: PORT=k, then its FIRST refusal (9 by sh after 2; 0x100000003 by sd after 3,
+     whose announce must name that wide value; 9 by sw after 4; 9 by sb after 6; 0x100 by sh after 7): it announces
+     exactly once and PORT keeps k.
+
+CONTRACT (clause e) -- AN ENUMERATION, NOT A LIST.  The fixed arm's inputs are the access (a PORT write, refused or
+accepted; a PORT read), its width, the value, and the device state an edit could condition on: the previous selector,
+the latch, and the COMMAND cell.  For each EFFECT below, EVERY value of EVERY one of those axes is held by some row, so
+an edit that conditions the fix on ONE axis value is caught; the kill of each cell's one-axis edit is measured in
+regress/artifacts/fbctrlportkill_20260924/table4/TABLE.out.  This is the class closure: pass 2, the F2 pass and the
+closing pass each found such an edit on an axis the rows had left partly empty.
+  a refusal keeps the previous selector -- width sb/sh/sw/sd (P, W); previous 0 (F), 1 (V), 2 3 4 (X), 5 (P), 6 (W),
+      7 (P, X7); COMMAND 0 (P) and holding 2 (V); latch unset (P's first) and set (the rest)
+  the first refusal announces once, the rest are silent -- first-refusal width sw (P) sb (W) sh (X2, X7) sd (X3);
+      previous 0 (F), 1 (V), 2 3 4 6 7 (X), 5 (P); COMMAND 0 and 2 (V); silence across PORT reads, a DATA write and a
+      DATA read, a NOP and a GET_RESOLUTION (R), accepted selectors and twelve refusals (P); the value named: 0x8 (P),
+      0x9 (F), the wide 0x100000003 (X3)
+  a PORT read returns the selector -- lb lh ld (W) and lw (every session); every selector 0-7 (A); COMMAND holding 2
+      (V); latch unset (A) and set (P)
+  a refusal leaves every cell alone -- all eight cells after refusals of 8, 9, 16, 0x100000003 (sd) and 0xff (sb) with
+      COMMAND holding 2 (V), and port 5's after a refused 9 with COMMAND 0 (K)
+  an accepted selector is stored -- 0 and 7 at every width (W, A), every selector at one width (A)
+Beyond the effects: the store of an out-of-range value, clamped, masked or reset; the compare narrowed or signed (bit
+63 alone, bits 32-33, 32-bit truncation); a boundary slip at 8; an announce on an accepted selector; an announce
+demoted to debug(); and the pre-#549 process exit on DATA.
+NOT CLAIMED (disclosed).  (0) An edit conditioned on TWO axes at once -- a joint cell such as "refuse 9 only by sb after
+PORT=3", or "`ld` sets bit 32 except at selector 5" -- is caught only where a row happens to hold that pair; the
+enumeration above is one-axis by design, and closing every pair is the unbounded growth the carrier's floor rules
+refuse.  (1) A process-global latch instead of the per-instance field, and an announce conditioned on
 the machine's serial number.  The probe's `-E testmips` session has ONE fbctrl.  A second instance IS reachable without
 adding a device -- two testmips machines in one process from a config file, `gxemul @config` -- and there the
 process-global latch reds (measured by the Opus F2 seat, opus549_measured/f2/TABLE_twoinst.out), but that is a new
 launcher this probe does not use: filed as `fbctrltwoinst`.  The latch is per instance by construction, a struct member,
-untested across two machines.  (2) The deletion of the DATA arm's range check, or its `>=` weakened to `>`: unreachable
-while the PORT arm refuses, and the check is KEPT as a tripwire.  It exits before it indexes, so an index of 8 cannot
-reach `warned_port` while it stands, and `port[8]` would be undefined behaviour, not a defined alias of the latch.
-(3) An exception for one value no row writes (`idata != 10`), a re-announce period of twelve or more, and width x value
-cells other than those rowed: the value space is 2^64, and no finite row set closes "except value k".  (4) Equivalent
+untested across two machines.  (2) Any edit of the DATA arm's kept range check -- deleting it, deleting only its
+`exit(1)`, weakening `>=` to `>`, or swapping its operand -- is unreachable while the PORT arm refuses, because no
+out-of-range selector is ever stored; the check is KEPT as a tripwire.  It exits before it indexes, so an index of 8
+cannot reach `warned_port` while it stands, and `port[8]` would be undefined behaviour, not a defined alias of the
+latch.  (3) An exception for one value no row writes (`idata != 10`), a re-announce period of twelve or more, a
+re-arm by SET_RESOLUTION traffic (no row sends command 1: it resizes the framebuffer), and an announce whose value is
+mangled only for a value that is never a session's first refusal: the value space is 2^64, and no finite row set
+closes "except value k".  (4) Equivalent
 edits: storing `(uint32_t) idata` (it compiles to the fix's own binary), reordering the struct's fields, masking the PORT
 read with 7 (the selector is always 0..7).  (5) `printf` in place of `fatal()`: indistinguishable in THIS invocation's
 output.  (6) Narrowing the DATA path's widths, and the device's OTHER two process-ending calls -- fbctrl_command()'s
@@ -64,8 +86,10 @@
 own logic are reviewed, not rowed.
 LIMITS OF A ROW.  Session P re-selects PORT=5 before each refusal, so a refused selector cannot carry over into the next
 row WHEN THE LEGAL SELECTION LANDS; an edit that also refuses legal selections defeats the re-select, and later rows
-then inherit its value (M_acclatch).  And every read-back is taken after its session ends, so a session that dies
-part-way blanks the rows it had already passed (M_acc4: session A died at step 5 and every accept row read `-`).
+then inherit its value (M_acclatch).  Every read-back is taken after its session ends, so a session that dies part-way
+blanks the rows it had already passed (M_acc4: session A died at step 5 and every accept row read `-`).  And session A's
+"accept selector 0 written by sw" cannot see an IGNORED store -- the selector is already 0 at power-on -- so the cell
+"0 by sw is accepted" is held by W's row after PORT=5, not by A's.
 
 Every stepped word is compared with the emulator's own step line (the hand-assembled-encoding trap).
 Output: one row per check, then FBCTRLP_CONTROL=OK|FAILED, FBCTRLP_RESULT=n/t, FBCTRLP_DONE.  The exit status is 0
@@ -92,7 +116,8 @@
 
 REG = dict(zr=0, v0=2, v1=3, a0=4, a1=5, a2=6, a3=7, t0=8, t1=9, t2=10, t3=11, t4=12, t5=13, t6=14, t7=15,
            s0=16, s1=17, s2=18, s3=19, s4=20, s5=21, s6=22, s7=23, t8=24, t9=25)
-OPS = dict(sb=0x28, sh=0x29, sw=0x2b, sd=0x3f, lw=0x23, ld=0x37)
+OPS = dict(sb=0x28, sh=0x29, sw=0x2b, sd=0x3f, lb=0x20, lh=0x21, lw=0x23, ld=0x37)
+LOADS = ("lb", "lh", "lw", "ld")
 
 
 def ins(op, rt, off, base="t0"):
@@ -112,6 +137,8 @@
 assert ins("sh", "t9", 0) == 0xa5190000
 assert ins("ld", "s3", 0) == 0xdd130000
 assert ins("sb", "zr", 0) == 0xa1000000
+assert ins("lb", "a1", 0) == 0x81050000
+assert ins("lh", "a2", 0) == 0x85060000
 assert ANCHOR == 0x3c0f0000
 
 
@@ -324,7 +351,9 @@
           ("sd", "t4", 0x200000000, "0x200000000 (sd)"), ("sd", "t5", 0x100000003, "0x100000003 (sd)"),
           ("sd", "t6", M64, "all-ones (sd)"), ("sw", "t7", 0xffffffff, "all-ones (sw)"),
           ("sb", "t8", 0xff, "0xff (sb)"), ("sh", "t9", 0x100, "0x100 (sh)")]
-EXTRA = [("sb", "t3"), ("sh", "t3")]                                   # 16 by sb and by sh
+#  16 by sb and by sh, each read back into a register whose own value (0x200000000, 0x100000003) is spent by then and
+#  can never read as 5 -- so an ignored read, or a session that died, reds the row too.
+EXTRA = [("sb", "t3", "t4", "16 (sb)"), ("sh", "t3", "t5", "16 (sh)")]
 READ_P = ["s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "v0"]
 PROG_P = [("sw", "a0", 0, None), ("sw", "a1", 16, None)]
 REGS_P = [("t0", FBCTRL), ("a0", 5), ("a1", 0x2a), ("a2", 7)]
@@ -334,16 +363,21 @@
         PROG_P.append(("sw", "a0", 0, None))                   # a fresh PORT=5 before every later refusal
     PROG_P.append((w, r, 0, "r%d" % k))
     PROG_P.append(("lw", READ_P[k], 0, None))
-for w, r in EXTRA:
-    PROG_P += [("sw", "a0", 0, None), (w, r, 0, None)]
+for w, r, rb, _n in EXTRA:
+    PROG_P += [("sw", "a0", 0, None), (w, r, 0, None), ("lw", rb, 0, None)]
 PROG_P += [("sw", "a2", 0, None), ("sw", "t1", 0, "r11"), ("lw", "v1", 0, None)]
-READS_P = READ_P + ["v1"]
+READS_P = READ_P + [e[2] for e in EXTRA] + ["v1"]
 
-#  R: a DATA write and a NOP command between two refusals -- in its own session.
+#  R: between two refusals, a PORT read, a DATA write, a NOP command, a DATA READ and a GET_RESOLUTION -- every kind of
+#  traffic a guest makes except SET_RESOLUTION -- in its own session.
 PROG_R = [("sw", "a0", 0, None), ("sw", "t1", 0, "ra"), ("lw", "s0", 0, None),
-          ("sw", "a1", 16, None), ("sw", "zr", 0, None), ("sw", "zr", 16, None),
+          ("sw", "a1", 16, None),                                        # DATA write: port 5 = 0x2a
+          ("sw", "zr", 0, None), ("sw", "zr", 16, None),                 # PORT=0, DATA=0: a NOP command
+          ("sw", "a0", 0, None), ("lw", "s2", 16, None),                 # PORT=5, DATA READ
+          ("sw", "zr", 0, None), ("sw", "s3", 16, None),                 # PORT=0, DATA=2: GET_RESOLUTION
           ("sw", "a0", 0, None), ("sw", "t1", 0, "rb"), ("lw", "s1", 0, None)]
-REGS_R = [("t0", FBCTRL), ("a0", 5), ("a1", 0x2a), ("t1", 9), ("s0", 0xdead), ("s1", 0xdead)]
+REGS_R = [("t0", FBCTRL), ("a0", 5), ("a1", 0x2a), ("t1", 9), ("s3", 2), ("s0", 0xdead), ("s1", 0xdead),
+          ("s2", 0xdead)]
 
 PROG_K = [("sw", "t1", 0, None), ("sw", "t3", 16, None), ("sw", "t2", 0, None), ("lw", "s0", 16, None),
           ("sw", "t4", 16, None), ("sw", "t1", 0, None), ("lw", "s1", 16, None)]
@@ -357,40 +391,55 @@
 #  V: X1 across a refusal made while COMMAND still holds GET_RESOLUTION, then every cell across four refusals.
 #  Port 0 is never written after the first GET_RESOLUTION: a DATA write there EXECUTES the command.
 REGS_V = [("t0", FBCTRL)] + [("s%d" % p, p) for p in range(1, 8)] + [("t%d" % p, 0x11 * p) for p in range(1, 8)] + \
-         [("t8", 123), ("a0", 9), ("a1", 16), ("a2", 0x100000003), ("a3", 0xff), ("v0", 0xdead), ("v1", 0xdead)]
+         [("t8", 123), ("a0", 9), ("a1", 16), ("a2", 0x100000003), ("a3", 0xff), ("t9", 8), ("s0", 0xdead),
+          ("v0", 0xdead), ("v1", 0xdead)]
 PROG_V = [("sw", "zr", 0, None), ("sw", "s2", 16, None),               # COMMAND = GET_RESOLUTION (X1 = Y1 = 0)
           ("sw", "s1", 0, None), ("sw", "t8", 16, None),               # X1 = 123
-          ("sw", "a0", 0, None),                                        # refuse 9
+          ("sw", "a0", 0, "v1st"),                                      # refuse 9: COMMAND holds 2, the selector is 1
+          ("lw", "s0", 0, None),                                        # PORT must still read 1
           ("sw", "s1", 0, None), ("lw", "v0", 16, None)]                # read X1
 for p in range(1, 8):
     PROG_V += [("sw", "s%d" % p, 0, None), ("sw", "t%d" % p, 16, None)]
-PROG_V += [("sw", "a0", 0, None), ("sw", "a1", 0, None), ("sd", "a2", 0, None), ("sb", "a3", 0, None)]
+PROG_V += [("sw", "a0", 0, None), ("sw", "a1", 0, None), ("sd", "a2", 0, None), ("sb", "a3", 0, None),
+           ("sw", "t9", 0, "vlast")]
 PROG_V += [("sw", "zr", 0, None), ("lw", "v1", 16, None)]
 for p in range(1, 8):
     PROG_V += [("sw", "s%d" % p, 0, None), ("lw", "s%d" % p, 16, None)]
-READS_V = ["v0", "v1"] + ["s%d" % p for p in range(1, 8)]
+READS_V = ["s0", "v0", "v1"] + ["s%d" % p for p in range(1, 8)]
 
 #  W: the width x boundary cells, each after its own non-zero predecessor into a poisoned read-back; then an ld.
-W_CELLS = [("accept 0 written by sb after PORT=5", "a0", "sb", "zr", "s0", 0),
-           ("accept 0 written by sh after PORT=5", "a0", "sh", "zr", "s1", 0),
-           ("accept 0 written by sw after PORT=5", "a0", "sw", "zr", "s2", 0),
-           ("accept 0 written by sd after PORT=5", "a0", "sd", "zr", "s3", 0),
-           ("accept 7 written by sb after PORT=5", "a0", "sb", "t5", "s4", 7),
-           ("accept 7 written by sh after PORT=5", "a0", "sh", "t5", "s5", 7),
-           ("accept 7 written by sw after PORT=5", "a0", "sw", "t5", "s6", 7),
-           ("refuse 8 (sb), PORT keeps 5", "a0", "sb", "t4", "s7", 5),
-           ("refuse 8 (sh), PORT keeps 5", "a0", "sh", "t4", "v0", 5),
-           ("refuse 8 (sd), PORT keeps 5", "a0", "sd", "t4", "v1", 5),
-           ("refuse 0x8000000000000000 (sd), PORT keeps 5", "a0", "sd", "t2", "t6", 5),
-           ("refuse 9 after PORT=6, PORT keeps 6", "a3", "sw", "t1", "t8", 6)]
+W_CELLS = [("accept 0 written by sb after PORT=5", "a0", "sb", "zr", "s0", 0, None),
+           ("accept 0 written by sh after PORT=5", "a0", "sh", "zr", "s1", 0, None),
+           ("accept 0 written by sw after PORT=5", "a0", "sw", "zr", "s2", 0, None),
+           ("accept 0 written by sd after PORT=5", "a0", "sd", "zr", "s3", 0, None),
+           ("accept 7 written by sb after PORT=5", "a0", "sb", "t5", "s4", 7, None),
+           ("accept 7 written by sh after PORT=5", "a0", "sh", "t5", "s5", 7, None),
+           ("accept 7 written by sw after PORT=5", "a0", "sw", "t5", "s6", 7, None),
+           ("refuse 8 (sb), PORT keeps 5", "a0", "sb", "t4", "s7", 5, "w1st"),     # W's FIRST refusal
+           ("refuse 8 (sh), PORT keeps 5", "a0", "sh", "t4", "v0", 5, None),
+           ("refuse 8 (sd), PORT keeps 5", "a0", "sd", "t4", "v1", 5, None),
+           ("refuse 0x8000000000000000 (sd), PORT keeps 5", "a0", "sd", "t2", "t6", 5, None),
+           ("refuse 9 after PORT=6, PORT keeps 6", "a3", "sw", "t1", "t8", 6, "wlast")]
 PROG_W = []
 REGS_W = [("t0", FBCTRL), ("a0", 5), ("a3", 6), ("t1", 9), ("t2", 0x8000000000000000), ("t4", 8), ("t5", 7),
-          ("t9", 0xdead)]
-for _n, pred, w, val, rb, _want in W_CELLS:
-    PROG_W += [("sw", pred, 0, None), (w, val, 0, None), ("lw", rb, 0, None)]
+          ("t9", 0xdead), ("a1", 0xdead), ("a2", 0xdead)]
+for _n, pred, w, val, rb, _want, tag in W_CELLS:
+    PROG_W += [("sw", pred, 0, None), (w, val, 0, tag), ("lw", rb, 0, None)]
     REGS_W.append((rb, 0xdead))
-PROG_W += [("sw", "a0", 0, None), ("ld", "t9", 0, None)]               # ld of PORT with selector 5
-READS_W = [c[4] for c in W_CELLS] + ["t9"]
+PROG_W += [("sw", "a0", 0, None), ("ld", "t9", 0, None),               # ld, lb and lh of PORT with selector 5
+           ("sw", "a0", 0, None), ("lb", "a1", 0, None),
+           ("sw", "a0", 0, None), ("lh", "a2", 0, None)]
+READS_W = [c[4] for c in W_CELLS] + ["t9", "a1", "a2"]
+
+#  X: five fresh devices -- the first-refusal cells (previous selector x width) no other session's first refusal holds.
+#  Each: PORT=k, its FIRST refusal (tag x), then a PORT read into a poisoned register.
+X_CELLS = [("X2", 2, "sh", 9), ("X3", 3, "sd", 0x100000003), ("X4", 4, "sw", 9), ("X6", 6, "sb", 9),
+           ("X7", 7, "sh", 0x100)]
+
+
+def prog_x(k, w, v):
+    return ([("sw", "a0", 0, None), (w, "t1", 0, "x"), ("lw", "s0", 0, None)],
+            [("t0", FBCTRL), ("a0", k), ("t1", v), ("s0", 0xdead)])
 
 
 def main():
@@ -404,6 +453,10 @@
         F = session("F", PROG_F, REGS_F, ["t2"], stub, free_run=True)
         V = session("V", PROG_V, REGS_V, READS_V, stub)
         W = session("W", PROG_W, REGS_W, READS_W, stub)
+        X = []
+        for lab, k, w, v in X_CELLS:
+            prog, regs = prog_x(k, w, v)
+            X.append(session(lab, prog, regs, ["s0"], stub))
     finally:
         try:
             os.unlink(stub)
@@ -423,6 +476,7 @@
     row("C nothing refused, no (once) line", len(ONCE_RE.findall(C["buf"])), 0)
     for lab, S in (("A", A), ("P", P), ("R", R), ("K", K), ("V", V), ("W", W)):
         ctl.append(row("%s disassembly of every stepped word" % lab, len(S["badis"]), 0))
+    ctl.append(row("X2-X7 disassembly of every stepped word", sum(len(S["badis"]) for S in X), 0))
     print("ACCEPT (session A: %s %d/%d)" % (A["status"], A["steps"], A["n"]))
     for k, (p, w) in enumerate(ACC):
         row("accept selector %d written by %s" % (p, w), hx(A["vals"].get(PORT_RB[k])), hx(p))
@@ -433,13 +487,15 @@
     print("REFUSE (session P: %s %d/%d)" % (P["status"], P["steps"], P["n"]))
     for k, (w, r, v, name) in enumerate(REFUSE):
         row("refuse %s, PORT keeps 5" % name, hx(P["vals"].get(READ_P[k])), "0x5")
+    for _w, _r, rb, name in EXTRA:
+        row("refuse %s, PORT keeps 5" % name, hx(P["vals"].get(rb)), "0x5")
     row("refuse 9 after PORT=7, PORT keeps 7", hx(P["vals"].get("v1")), "0x7")
     row("announce: exactly 1 right after the FIRST refusal", P["once_after"].get("r0"), 1)
     row("announce: still exactly 1 after twelve refusals", P["once_after"].get("r11"), 1)
     row("announce names the first refused value, 0x8", first_val(P), "0x8")
     print("RE-ARM (session R: %s %d/%d)" % (R["status"], R["steps"], R["n"]))
-    row("R announce still 1 after DATA and NOP traffic", R["once_after"].get("rb"), 1)
-    row("R refuse 9 after the NOP, PORT keeps 5", hx(R["vals"].get("s1")), "0x5")
+    row("R announce still 1 after DATA, NOP and GET_RESOLUTION", R["once_after"].get("rb"), 1)
+    row("R refuse 9 after that traffic, PORT keeps 5", hx(R["vals"].get("s1")), "0x5")
     print("THE WITNESS PAIR (session K)")
     row("K survives DATA after a refused PORT write", "%s %d/%d" % (K["status"], K["steps"], K["n"]),
         "SURVIVED %d/%d" % (len(PROG_K), len(PROG_K)))
@@ -451,14 +507,28 @@
     row("F lw of PORT after the power-on refusal reads 0", hx(F["vals"].get("t2")), "0x0")
     row("F announce names the refused value, 0x9", first_val(F), "0x9")
     print("CELLS (session V: %s %d/%d)" % (V["status"], V["steps"], V["n"]))
+    row("V refuse 9 while COMMAND holds 2, PORT keeps 1", hx(V["vals"].get("s0")), "0x1")
+    row("V that first refusal (COMMAND holding 2) announces", V["once_after"].get("v1st"), 1)
     row("V X1=123 survives a refusal (COMMAND holds 2)", hx(V["vals"].get("v0")), hx(123))
-    row("V port 0 (COMMAND) still 2 after four refusals", hx(V["vals"].get("v1")), "0x2")
+    row("V port 0 (COMMAND) still 2 after five refusals", hx(V["vals"].get("v1")), "0x2")
     for p in range(1, 8):
-        row("V port %d keeps its fill after four refusals" % p, hx(V["vals"].get("s%d" % p)), hx(0x11 * p))
+        row("V port %d keeps its fill after five refusals" % p, hx(V["vals"].get("s%d" % p)), hx(0x11 * p))
+    row("V announce still exactly 1 after its six refusals", V["once_after"].get("vlast"), 1)
     print("WIDTHS (session W: %s %d/%d)" % (W["status"], W["steps"], W["n"]))
-    for name, _p, _w, _v, rb, want in W_CELLS:
+    for name, _p, _w, _v, rb, want, _t in W_CELLS:
         row(name, hx(W["vals"].get(rb)), hx(want))
+    row("W the first refusal (8 by sb) announces", W["once_after"].get("w1st"), 1)
+    row("W announce still exactly 1 after its five refusals", W["once_after"].get("wlast"), 1)
     row("ld of PORT reads exactly 5", hx(W["vals"].get("t9")), "0x5")
+    row("lb of PORT reads exactly 5", hx(W["vals"].get("a1")), "0x5")
+    row("lh of PORT reads exactly 5", hx(W["vals"].get("a2")), "0x5")
+    print("FIRST REFUSALS (sessions X2-X7: %s)" % " ".join("%s %d/%d" % (S["status"], S["steps"], S["n"])
+                                                          for S in X))
+    for (lab, k, w, v), S in zip(X_CELLS, X):
+        row("%s refuse 0x%x (%s) after PORT=%d, PORT keeps %d" % (lab, v, w, k, k), hx(S["vals"].get("s0")), hx(k))
+        row("%s that FIRST refusal announces exactly once" % lab, S["once_after"].get("x"), 1)
+        if v >= 1 << 32:
+            row("%s the announce names the wide value 0x%x" % (lab, v), first_val(S), "0x%x" % v)
     control = all(ctl)
     n_ok, n = sum(RESULTS), len(RESULTS)
     print("FBCTRLP_CONTROL=%s" % ("OK" if control else "FAILED"))
```

### 4b. regress/gate_mips_folds.sh

```diff
--- a/regress/gate_mips_folds.sh (as the closing pass reviewed it)
+++ b/regress/gate_mips_folds.sh (now)
@@ -43,13 +43,15 @@
 #  this gate's pmax-kernel check: a missing kernel still skips the fold rows below, and
 #  gate_skip reports FAIL, not SKIP, if an fbctrl row failed first.
 #
-#  THE CONTRACT is the probe's header (CATCHES / NOT CLAIMED).  Kill table 3
-#  (regress/artifacts/fbctrlportkill_20260924/table3/TABLE.out) built 62 edits: the 54 the
-#  contract does not disclose are ALL red, HEAD's own arm among them (M_revert, 47/73 here:
-#  every refusal row red, and sessions K and R ended the process); the 8 it discloses score
-#  73/73 -- a process-global latch, the DATA arm's kept check deleted, a serial-number
-#  condition, three equivalent edits and two DATA-width edits.  The device still ends the
-#  process through its command and offset defaults, which are filed, not claimed.
+#  THE CONTRACT is the probe's header (its ENUMERATION and NOT CLAIMED).  Kill table 4
+#  (regress/artifacts/fbctrlportkill_20260924/table4/TABLE.out, plus table4b/ for the one
+#  edit whose first build did not compile) built 101 edits: the 87 the contract does not
+#  disclose are ALL red, HEAD's own arm among them (M_revert, 51/94 here, and sessions K and R
+#  ended the process); the 14 it discloses score 94/94 -- a process-global latch, a serial-
+#  number condition, three edits of the DATA arm's kept check, two joint cells, one value no
+#  row writes, a re-announce period of twelve, three equivalent edits and two DATA-width
+#  edits.  The device still ends the process through its command and offset defaults, which
+#  are filed, not claimed.
 #
 #  `gatedevicesplit` is OWED (#498): one more device probe in a CPU gate, as #548 added to
 #  gate 14.  Recorded, not compounded silently.
@@ -76,8 +78,8 @@
     #  quoted numerator is inert to that tool BY DESIGN -- it reads only the denominator's
     #  line -- and the exit row above and the two reconciliation rows below are what catch a
     #  red or an edited score.
-    check "fbctrl_port rows run" "${fbres#*/}" 73
-    check "fbctrl_port rows correct" "${fbres%/*}" "73"
+    check "fbctrl_port rows run" "${fbres#*/}" 94
+    check "fbctrl_port rows correct" "${fbres%/*}" "94"
     check "fbctrl_port rows failed" "$(grep -c '^  FAIL ' "$FBCLOG")" "0"
     #  RECONCILE the rows the probe PRINTED with the trailer it printed (#549 F2, measured by
     #  the Opus seat): checking the trailer alone, a log with one row deleted and its
@@ -86,6 +88,11 @@
           "$(grep -cE '^  (ok|FAIL) ' "$FBCLOG")" "${fbres#*/}"
     check "fbctrl_port ok rows match the trailer count" \
           "$(grep -c '^  ok ' "$FBCLOG")" "${fbres%/*}"
+    #  And each row name prints ONCE: a row replaced by a copy of another keeps every count
+    #  above intact (the closing pass's grok seat), and only the names can tell.
+    check "fbctrl_port row names are unique" \
+          "$(grep -E '^  (ok|FAIL) ' "$FBCLOG" | sed -E 's/^  (ok|FAIL) +//; s/ +got=.*//' |
+             sort | uniq -d | wc -l)" "0"
 fi
 
 if [ ! -f "$PMAX_KERNEL" ]; then gate_skip "no pmax kernel at $PMAX_KERNEL"; fi
```

## 5. EVIDENCE (measured; durable under regress/artifacts/fbctrlportkill_20260924/)

### 5a. Kill table 4 -- 101 edits of the final fix, FROZEN 94-row probe (summary for packet-fed seats)

Predictions written BEFORE the run: 14 at 94/94 (each disclosed), every other edit red.  All held.  G2_rdrearm
did not compile as first written (a second statement under a braceless if) and was rebuilt with a comma and
scored alone (table4b: red).  The base (the fix) scored 94/94 with CONTROL=OK.

AT 94/94 (14, all disclosed): A1_not10, A2_sb3, B_mod12, G5a_noexit, G5b_checkop, G7_ldbit32, M_noguard, M_static, N_acc32, N_datard16, N_datawr8, N_order, N_rdmask7, T_D9c_serial1

RED (87).  The closing-pass edits, with the rows that went red on each:
```
B_mod11          FBCTRLP_RESULT=93/94 | announce: still exactly 1 after twelve refusals;
C_ann_nw4        FBCTRLP_RESULT=87/94 | announce: exactly 1 right after the FIRST refusal;announce names the first refused value, 0x8;R announce still 1 after DATA, NOP and GET_RESOLUTION;F 
C_ann_p5         FBCTRLP_RESULT=90/94 | announce: exactly 1 right after the FIRST refusal;announce names the first refused value, 0x8;R announce still 1 after DATA, NOP and GET_RESOLUTION;W 
C_rd_w4only      FBCTRLP_RESULT=91/94 | ld of PORT reads exactly 5;lb of PORT reads exactly 5;lh of PORT reads exactly 5;
C_ref_p0         FBCTRLP_RESULT=91/94 | F refusal announced while free-running (fatal);F lw of PORT after the power-on refusal reads 0;F announce names the refused value, 0x9;
C_ref_p7         FBCTRLP_RESULT=91/94 | refuse 9 after PORT=7, PORT keeps 7;X7 refuse 0x100 (sh) after PORT=7, PORT keeps 7;X7 that FIRST refusal announces exactly once;
E_ann_cmd        FBCTRLP_RESULT=92/94 | V that first refusal (COMMAND holding 2) announces;V announce still exactly 1 after its six refusals;
E_ann_p1         FBCTRLP_RESULT=93/94 | V that first refusal (COMMAND holding 2) announces;
E_ann_w4         FBCTRLP_RESULT=88/94 | W the first refusal (8 by sb) announces;X2 that FIRST refusal announces exactly once;X3 that FIRST refusal announces exactly once;X3 the announce name
E_cmdset         FBCTRLP_RESULT=92/94 | V that first refusal (COMMAND holding 2) announces;V announce still exactly 1 after its six refusals;
E_rd_cmd         FBCTRLP_RESULT=92/94 | R refuse 9 after that traffic, PORT keeps 5;V refuse 9 while COMMAND holds 2, PORT keeps 1;
E_rd_w4          FBCTRLP_RESULT=92/94 | lb of PORT reads exactly 5;lh of PORT reads exactly 5;
E_ref_cmd        FBCTRLP_RESULT=90/94 | R refuse 9 after that traffic, PORT keeps 5;V refuse 9 while COMMAND holds 2, PORT keeps 1;V that first refusal (COMMAND holding 2) announces;V announ
E_ref_p1         FBCTRLP_RESULT=92/94 | V refuse 9 while COMMAND holds 2, PORT keeps 1;V that first refusal (COMMAND holding 2) announces;
E_ref_p2         FBCTRLP_RESULT=92/94 | X2 refuse 0x9 (sh) after PORT=2, PORT keeps 2;X2 that FIRST refusal announces exactly once;
E_ref_p3         FBCTRLP_RESULT=92/94 | X3 that FIRST refusal announces exactly once;X3 the announce names the wide value 0x100000003;
E_ref_p4         FBCTRLP_RESULT=92/94 | X4 refuse 0x9 (sw) after PORT=4, PORT keeps 4;X4 that FIRST refusal announces exactly once;
G1_rewrite1      FBCTRLP_RESULT=93/94 | V refuse 9 while COMMAND holds 2, PORT keeps 1;
G3a_cmdrearm     FBCTRLP_RESULT=93/94 | R announce still 1 after DATA, NOP and GET_RESOLUTION;
G3b_getresrearm  FBCTRLP_RESULT=93/94 | R announce still 1 after DATA, NOP and GET_RESOLUTION;
G4_pad16         FBCTRLP_RESULT=92/94 | refuse 16 (sb), PORT keeps 5;refuse 16 (sh), PORT keeps 5;
G6_trunc32       FBCTRLP_RESULT=93/94 | X3 the announce names the wide value 0x100000003;
G8_clob8         FBCTRLP_RESULT=93/94 | V port 0 (COMMAND) still 2 after five refusals;
L1_rebit63       FBCTRLP_RESULT=93/94 | W announce still exactly 1 after its five refusals;
R_partAB         FBCTRLP_RESULT=91/94 | R refuse 9 after that traffic, PORT keeps 5;V that first refusal (COMMAND holding 2) announces;V announce still exactly 1 after its six refusals;
R_state1         FBCTRLP_RESULT=88/94 | refuse 9 (sw), PORT keeps 5;refuse 9 after PORT=7, PORT keeps 7;R refuse 9 after that traffic, PORT keeps 5;K survives DATA after a refused PORT write
S_ann_cp         FBCTRLP_RESULT=92/94 | F refusal announced while free-running (fatal);F announce names the refused value, 0x9;
S_rd_idata       FBCTRLP_RESULT=87/94 | C SIGNATURE: X1 zeroed by GET_RESOLUTION;C SIGNATURE: Y1 zeroed by GET_RESOLUTION;V port 0 (COMMAND) still 2 after five refusals;accept 0 written by s
S_ref_wp         FBCTRLP_RESULT=92/94 | refuse 8 (sh), PORT keeps 5;refuse 8 (sd), PORT keeps 5;
T_W_sb0          FBCTRLP_RESULT=93/94 | accept 0 written by sb after PORT=5;
T_W_sd7          FBCTRLP_RESULT=90/94 | accept selector 7 written by sd;port 6 round-trips its DATA value;port 7 round-trips its DATA value;A nothing refused, no (once) line;
T_W_sw8          FBCTRLP_RESULT=91/94 | refuse 8 (sw), PORT keeps 5;announce: exactly 1 right after the FIRST refusal;announce names the first refused value, 0x8;
G2_rdrearm       FBCTRLP_RESULT=92/94 | R announce still 1 after DATA, NOP and GET_RESOLUTION;V announce still exactly 1 after its six refusals;
```

Also red (54, table 3's carried edits): M_acc4, M_acclatch, M_and5, M_ann_any, M_bit, M_clamp, M_debug, M_decl, M_gt, M_i32, M_i64, M_latch0, M_latchcnt, M_latchinv, M_mod33, M_perval, M_reflatch, M_rej2, M_reset0, M_revert, M_store, M_u32, M_wide, N_clobcell, N_clobcmd, N_cmdport, N_cmdread, N_datarearm, N_rdlatch, N_rdmask3, N_rearm, N_runcmd, T_D10_print0, T_D11a_y1one, T_D11b_y1keep, T_D2_mask63, T_D3_ctor1, T_D3_pwron, T_D4b_cmdrearm, T_D6_rdbit32, T_D7a_sub4zero, T_D7b_sdzero, T_D7c_shzero, T_D8_or1, T_D9a_only9, T_D9b_mod10, T_W_sb7, T_W_sb8, T_W_sh7, T_W_sh8, T_W_sw0, T_W_sw7, T_X_ann6, T_X_w8

### 5b. Gate 16 on the working tree: PASS (26 checks), fbctrl rows 94/94 (gates_t4/gate16.out)

### 5c. The revised gate block on logs derived from that 94-row log (closing/g16_fixtures_t4.out)

```
good                         probe_rc=0  PASS (9 checks)              | red: 
good                         probe_rc=1  FAIL (1 of 9 checks)         | red: fbctrl probe exit 0 (nonzero: a crash or a red row);
row_deleted                  probe_rc=0  FAIL (2 of 9 checks)         | red: fbctrl_port rows emitted match the trailer total;fbctrl_port ok rows match the trailer count;
row_deleted                  probe_rc=1  FAIL (3 of 9 checks)         | red: fbctrl probe exit 0 (nonzero: a crash or a red row);fbctrl_port rows emitted match the trailer total;fbctrl_port ok rows match the trailer count;
row_failed_result_intact     probe_rc=0  FAIL (2 of 9 checks)         | red: fbctrl_port rows failed;fbctrl_port ok rows match the trailer count;
row_failed_result_intact     probe_rc=1  FAIL (3 of 9 checks)         | red: fbctrl probe exit 0 (nonzero: a crash or a red row);fbctrl_port rows failed;fbctrl_port ok rows match the trailer count;
row_duplicated               probe_rc=0  FAIL (3 of 9 checks)         | red: fbctrl_port rows emitted match the trailer total;fbctrl_port ok rows match the trailer count;fbctrl_port row names are unique;
row_duplicated               probe_rc=1  FAIL (4 of 9 checks)         | red: fbctrl probe exit 0 (nonzero: a crash or a red row);fbctrl_port rows emitted match the trailer total;fbctrl_port ok rows match the trailer count;fbctrl_port row names are unique;
row_failed_result_honest     probe_rc=0  FAIL (2 of 9 checks)         | red: fbctrl_port rows correct;fbctrl_port rows failed;
row_failed_result_honest     probe_rc=1  FAIL (3 of 9 checks)         | red: fbctrl probe exit 0 (nonzero: a crash or a red row);fbctrl_port rows correct;fbctrl_port rows failed;
row_deleted_trailer_edited   probe_rc=0  FAIL (2 of 9 checks)         | red: fbctrl_port rows run;fbctrl_port rows correct;
row_deleted_trailer_edited   probe_rc=1  FAIL (3 of 9 checks)         | red: fbctrl probe exit 0 (nonzero: a crash or a red row);fbctrl_port rows run;fbctrl_port rows correct;
row_substituted              probe_rc=0  FAIL (1 of 9 checks)         | red: fbctrl_port row names are unique;
row_substituted              probe_rc=1  FAIL (2 of 9 checks)         | red: fbctrl probe exit 0 (nonzero: a crash or a red row);fbctrl_port row names are unique;
G16FIX_T4_DONE
```

## 6. ONE QUESTION (this packet is for seats that cannot read files; everything needed is above)

**Is there a single-axis edit of `dev_fbctrl.c` -- one of the three predicates dominating the fixed arm, qualified by ONE
value of ONE field the arm reads, or weakened -- that scores 94/94 and is NOT one of the 14 disclosed in §5a?**  Give
the exact tokens and the rows you expect to stay green, derived from the sessions as §4a shows them.  Separately, in one
line each: any disposition in §3 that the evidence in §5 contradicts.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
