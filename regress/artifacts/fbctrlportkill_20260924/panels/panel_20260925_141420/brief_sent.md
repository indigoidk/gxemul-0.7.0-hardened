# #549 fbctrlportkill -- THE CLOSING PASS on the repair the F2 adjudication produced (a repair owes its own pass)

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  **THE TREE UNDER REVIEW IS `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`**; other copies of
GXemul under the project root are not this fork.  If you read files, read ONLY `src/devices/dev_fbctrl.c`,
`src/include/testmachine/dev_fb.h`, `regress/fbctrl_port_probe.py`, `regress/gate_mips_folds.sh`, and this round's
`regress/artifacts/fbctrlportkill_20260924/closing/` and `.../table3/` -- nothing else under `regress/artifacts/`, and
not `tools/pipeline/ledger.json`.  If you cannot read files that is expected: everything you need is inlined, and a
premise you cannot settle from the packet should be NAMED, not guessed.
**VERDICT LINE FIRST**: `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then numbered findings.

## 1. SETTLED PREMISES (re-inlined; do not re-derive)

* **`fatal()` PRINTS AND RETURNS; only an explicit `exit(1)` ends the process** (`src/core/debugmsg.c`: `fatal()` has
  no early-out and no exit).
* **The fix** (unanimous in pass 1, unchanged through pass 2 and F2 except one comment sentence): the PORT arm refuses
  `idata >= 8` compared on the full `uint64_t`, keeps the previous selector, and announces once per device through
  the struct member `warned_port` with the marker `(once)`; the DATA arm's range check and its `exit(1)` are KEPT as a
  tripwire.  The command default (`fbctrl_command()`, any command other than 0-2) and the offset default (any offset
  other than 0x00/0x10) still end the process: OUT OF SCOPE, filed as `fbctrlcmdkill` and `fbctrloffkill`.
* **The §F2 adjudication** (nine seats, the dedicated codex "Astra" and grok jobs, then Fable 5.1 on 8 of 9 seats, then
  a fresh Opus 5.5 seat that MEASURED every corrected row): the detector was changed, the fix was not.  Rulings adopted:
  record reconciliation in the gate (a log with a row deleted passed); the probe exits nonzero on a red row; D2 as
  `sd 0x8000000000000000` after PORT=5 (the proposed `0x8000000000000005` was vacuous: its int conversion IS 5);
  D3 as a guest `lw` of PORT inside the free-run (printing an unloaded GPR was vacuous: cpu_new() zero-fills it); D7
  with a NON-ZERO predecessor before each zero-selector store; D9 with the count sampled after the twelfth refusal;
  D10 keeping the broad announce counter and adding a separate first-value check; D11 NOT owed as a kill row and
  added as a CONTROL extension; the A-silence row and `sd 8` (both measured as the only rows killing their edits); the
  docstring's `r` prefix dropped so the score checker can read it.  **The two-machine config (`gxemul @config` with
  two testmips machines) was MEASURED to work by the Opus seat and ruled FILED by Fable** -- a new launcher with an
  unmeasured console interaction -- as `fbctrltwoinst`; the contract says the latch is per instance by construction
  and untested across two machines.

## 2. WHERE THE NINTH SEAT (Opus, measured) AND THE ADJUDICATOR (Fable) DIFFERED -- my dispositions, for you to check

* `sh 0` accepted after PORT=5: Fable "disclose"; Opus measured that an sh-only edit escapes without the row.
  **ADOPTED as a row**, and the whole width x boundary class CLOSED: pass 2 found a width-conditioned escape (D7) and
  F2 found another (`sd 8`), which is two consecutive passes of one class, so every cell {0, 7 accepted; 8 refused} x
  {sb, sh, sw, sd} is rowed and each new cell has its own one-edit target in the kill table.
* Y1 (D11): **added as a CONTROL** (inside the device-signature control), as Fable ruled, not as a kill row.
* D4 (re-arm by DATA/NOP traffic): **its own session R**, because Opus measured that inside session P an edit accepting
  8 ends the session and blanks fourteen P rows.
* Two-machine: **FILED**, per Fable; Opus's recipe goes into the filing.

## 3. WHAT CHANGED SINCE F2 -- every file, disclosed

    git diff --numstat (vs HEAD f4f601c4), the round's files:
      src/devices/dev_fbctrl.c        18 / 5   INLINED (§4a: only the comment sentence changed since F2)
      regress/fbctrl_port_probe.py    new, 471 lines   INLINED as the diff from the 41-row probe F2 reviewed (§4b)
      regress/gate_mips_folds.sh      55 / 0   INLINED as the diff from the block F2 reviewed (§4c)
      regress/gate_hygiene.sh          2 / 2   NOT SHOWN -- two census pins (74/25), unchanged since pass 2
      tools/pipeline/check_probe_wiring.py, tools/precommit_check.sh -- SUMMARIZED: one MANIFEST line classifying
          fbctrl_port_probe.py as a detector, and SCORE_CLAIMS_MANIFEST 30 -> 31; unchanged since pass 2

## 4. THE REPAIR DIFF

### 4a. src/devices/dev_fbctrl.c since F2 (the only change: the R1 history sentence, narrowed to what was measured)

```diff
--- a/src/devices/dev_fbctrl.c (the fix as reviewed in pass 2 and F2)
+++ b/src/devices/dev_fbctrl.c (now: the R1 sentence)
@@ -120,9 +120,11 @@
 		else if (idata >= DEV_FBCTRL_NPORTS) {
 			/*  #549: an out-of-range selector is REFUSED, and
 			    current_port keeps its previous, always-valid value.
-			    It used to be stored with only a warning, and the
-			    next DATA access then ended the emulator in the
-			    range check below.  Announced once per device.  */
+			    It used to be stored as an int with only a warning:
+			    9 made the next DATA access end the emulator in the
+			    range check below, and a wide value was truncated
+			    onto a legal port (0x100000003 selected port 3).
+			    Announced once per device.  */
 			if (!d->warned_port) {
 				fatal("[ fbctrl: port number 0x%llx is out of range; "
 				    "the selector is unchanged (once) ]\n",
```

### 4b. regress/fbctrl_port_probe.py: the 41-row probe F2 reviewed -> the 73-row probe

```diff
--- a/regress/fbctrl_port_probe.py (the 41-row probe reviewed in pass 2 and F2)
+++ b/regress/fbctrl_port_probe.py (the 73-row probe, now)
@@ -1,48 +1,75 @@
 #!/usr/bin/env python3
-r"""#549 fbctrlportkill -- the DETECTOR for dev_fbctrl.c's port selector, on an UNMODIFIED `-E testmips`.
+"""#549 fbctrlportkill -- the DETECTOR for dev_fbctrl.c's port selector, on an UNMODIFIED `-E testmips`.
 
 machine_test.c installs `fbctrl addr=0x12f00000` in testmips's own setup (and in default_test() for the other test
-machines).  Every access below is a real guest sb/sh/sw/sd/lw placed with `put w` and executed through real address decode
-and memory_rw -- stepped one instruction at a time, except session F, which free-runs to a breakpoint.  No machine or
-device is added to reach the site.  t0 = 0xffffffffb2f00000, kseg1 of DEV_FBCTRL_ADDRESS; PORT is +0x00, DATA +0x10.
-
-THE DEFECT (HEAD before #549): the PORT arm STORED any selector with only a warning, and the DATA arm then called exit(1)
-on the stored int -- `sw 9` to PORT followed by any DATA access ended the emulator process.  #549 REFUSES a selector >= 8
-at the PORT arm (the previous, valid selector is kept) and announces the refusal once per device, `(once)`.
+machines).  Every access below is a real guest sb/sh/sw/sd/lw/ld placed with `put w` and executed through real address
+decode and memory_rw -- stepped one instruction at a time, except session F, which free-runs to a breakpoint.  No machine
+or device is added to reach the site.  t0 = 0xffffffffb2f00000, kseg1 of DEV_FBCTRL_ADDRESS; PORT is +0x00, DATA +0x10.
+
+THE DEFECT (HEAD before #549): the PORT arm STORED the selector, as an int, with only a warning.  An int out of range --
+`sw 9` -- made the next DATA access end the emulator process in the DATA arm's range check; a wide value was truncated
+onto a legal port and serviced (0x100000003 selected port 3: kill table 2's M_revert).  #549 REFUSES any selector >= 8,
+compared on the full 64-bit value, at the PORT arm (the previous, valid selector is kept) and announces the refusal
+once per device, `(once)`.
 
 SESSIONS (each on a fresh emulator)
-  C  controls: PORT=5, DATA=0x2a, read both back (LIVENESS); X1=123, COMMAND=GET_RESOLUTION, read X1 (DEVICE SIGNATURE:
-     the model zeroes X1/Y1 without X11 -- RAM at +0x10 would read back 2, the last value written there, and a banked
-     register WITHOUT command execution would read 123); no `(once)` line may appear (nothing is refused).
+  C  controls: PORT=5, DATA=0x2a, read both back (LIVENESS); X1=123 and Y1=123, COMMAND=GET_RESOLUTION, read X1 and Y1
+     (DEVICE SIGNATURE: the model zeroes both without X11 -- RAM at +0x10 would read back 2, the last value written
+     there, and a banked register WITHOUT command execution would read 123); no `(once)` line may appear.
   A  accept: all EIGHT selectors, written at widths 1, 2, 4 and 8, each read back through PORT; ports 1-7 round-trip
-     a distinct DATA value (port 0 is COMMAND and is written only with NOP).
-  P  refusal, anchored to a previous selector: PORT=5 (DATA 0x2a), then nine out-of-range writes -- 9, 8, 16 (sw),
-     0x200000000, 0x100000003, all-ones (sd), all-ones (sw), 0xff (sb), 0x100 (sh) -- each PRECEDED by a fresh
-     PORT=5 and followed by a PORT read that must still say 5, so every row fails only on its own value; then
-     PORT=7 and a refused 9 must leave 7.  The `(once)` count must be exactly 1 right
-     after the FIRST refusal and still 1 after the last.
+     a distinct DATA value (port 0 is COMMAND and is written only with NOP); no `(once)` line may appear.
+  P  refusal, anchored to a previous selector: PORT=5 (DATA 0x2a), then nine out-of-range writes -- 8, 9, 16 (sw),
+     0x200000000, 0x100000003, all-ones (sd), all-ones (sw), 0xff (sb), 0x100 (sh) -- each PRECEDED by a fresh PORT=5
+     and followed by a PORT read that must still say 5; two more (16 by sb, 16 by sh); then PORT=7 and a refused 9 must
+     leave 7 -- twelve refusals.  The `(once)` count must be exactly 1 right after the FIRST refusal and still 1 after
+     the twelfth, and the one announce must name the first refused value, 0x8.
+  R  re-arm: PORT=5, refuse 9, read PORT, a DATA write to port 5, a NOP command (PORT=0, DATA=0), PORT=5, refuse 9: the
+     count is still 1 and PORT keeps 5.  Its own session, so an edit that accepts 8 cannot blank P's rows.
   K  the witness pair, repaired: PORT=5, DATA=0x2a, PORT=9 refused, then a DATA READ (must survive and read port 5's
      0x2a) and a DATA WRITE of 0x77 (must land in port 5: read back through PORT=5).
-  F  free-running: one refused PORT write, then `continue` to a breakpoint.  Stepping raises debug()'s verbosity, so a
-     refusal announced with debug() instead of fatal() would pass every stepped row; free-running it does not print.
-
-CONTRACT (clause e).  CATCHES: the store reached for an out-of-range value (or a clamped/masked/reset one), the compare
-narrowed or signed (bit 63, bits 32-33, 32-bit truncation), a boundary slip at 8, a refusal applied to some widths only,
-a legal selector refused, a refusal that rewrites the previous selector, a latch never set / set late / keyed per value,
-an announce demoted to debug(), and the pre-#549 process exit on DATA (kill table 1: 20 of 20 such edits red,
-regress/artifacts/fbctrlportkill_20260924/table1/TABLE.out).  NOT CLAIMED: a process-global latch instead of the
-per-instance field (every machine installs ONE fbctrl; adding a device to reach a second would be laundering); the
-deletion of the DATA arm's range check, which a correct PORT arm makes unreachable -- it is KEPT as a tripwire, and it
-matters beyond style: `warned_port` sits right after `port[8]`, so an index of 8 that got past a broken PORT arm would
-land on the latch itself; and the device's OTHER two process-ending calls -- fbctrl_command()'s default (any command
-other than 0-2, including the documented but unimplemented FILL/COPY; a refused selector at power-on leaves COMMAND
-selected, so a following DATA write of such a value reaches it) and the access function's default (any offset other
-than 0x00/0x10).  Those are filed.  Session P re-selects PORT=5 before each refusal: kill table 1 ran without the
-re-select, and one corrupted selector then turned every later "keeps 5" row red, overstating which row catches
-what (the flagship seat, pass 1).
+  F  free-running: a refused PORT write at power-on and a guest `lw` of PORT execute INSIDE `continue`, which stops at a
+     breakpoint after them; the lw must read 0 and the announce must name 0x9.  This invocation passes -V and no -v,
+     so while free-running debug() is below its threshold and returns without printing, while fatal() prints: a refusal
+     announced with debug() would pass every stepped row and fail here.
+  V  cells: COMMAND=GET_RESOLUTION, X1=123, one refusal while COMMAND still holds 2 (X1 must stay 123); ports 1-7
+     filled with 0x11*p, four refusals (9, 16, 0x100000003 by sd, 0xff by sb), then all eight cells read back.
+  W  widths: selector 0 written by sb, sh, sw and sd and selector 7 by sb, sh and sw, each after PORT=5 (accepted);
+     8 by sb, sh and sd after PORT=5 (refused); 0x8000000000000000 by sd after PORT=5 (refused); 9 after PORT=6 (keeps
+     6); an `ld` of PORT with selector 5 (exactly 5).
+
+CONTRACT (clause e).  CATCHES, each with a measured kill in regress/artifacts/fbctrlportkill_20260924/table3/TABLE.out:
+the store reached for an out-of-range value (or a clamped, masked or reset one); the compare narrowed or signed (bit 63
+alone, bits 32-33, 32-bit truncation); a boundary slip at 8; a refusal or an acceptance conditioned on the access width
+-- the cells {0, 7} accepted and 8 refused are rowed at EVERY width, 1, 2, 4 and 8 (the class closure, after pass 2 and
+the F2 pass each found a width-conditioned escape); a legal selector refused; a refusal that rewrites the previous
+selector (from 0, 5, 6 and 7); a refusal that writes a port cell or runs a command; a latch never set, set late, keyed
+per value, cleared by DATA or command traffic, re-armed by an accepted selector or by a count whose period is eleven or
+less; an announce on an accepted selector; an announce naming another value; an announce demoted to debug(); a PORT
+read that sets a high bit (by lw and by ld); and the pre-#549 process exit on DATA.
+NOT CLAIMED (disclosed).  (1) A process-global latch instead of the per-instance field, and an announce conditioned on
+the machine's serial number.  The probe's `-E testmips` session has ONE fbctrl.  A second instance IS reachable without
+adding a device -- two testmips machines in one process from a config file, `gxemul @config` -- and there the
+process-global latch reds (measured by the Opus F2 seat, opus549_measured/f2/TABLE_twoinst.out), but that is a new
+launcher this probe does not use: filed as `fbctrltwoinst`.  The latch is per instance by construction, a struct member,
+untested across two machines.  (2) The deletion of the DATA arm's range check, or its `>=` weakened to `>`: unreachable
+while the PORT arm refuses, and the check is KEPT as a tripwire.  It exits before it indexes, so an index of 8 cannot
+reach `warned_port` while it stands, and `port[8]` would be undefined behaviour, not a defined alias of the latch.
+(3) An exception for one value no row writes (`idata != 10`), a re-announce period of twelve or more, and width x value
+cells other than those rowed: the value space is 2^64, and no finite row set closes "except value k".  (4) Equivalent
+edits: storing `(uint32_t) idata` (it compiles to the fix's own binary), reordering the struct's fields, masking the PORT
+read with 7 (the selector is always 0..7).  (5) `printf` in place of `fatal()`: indistinguishable in THIS invocation's
+output.  (6) Narrowing the DATA path's widths, and the device's OTHER two process-ending calls -- fbctrl_command()'s
+default (any command other than 0-2, including the documented but unimplemented FILL/COPY) and the access function's
+default (any offset other than 0x00/0x10): filed as `fbctrlcmdkill` and `fbctrloffkill`.  (7) Edits to this instrument's
+own logic are reviewed, not rowed.
+LIMITS OF A ROW.  Session P re-selects PORT=5 before each refusal, so a refused selector cannot carry over into the next
+row WHEN THE LEGAL SELECTION LANDS; an edit that also refuses legal selections defeats the re-select, and later rows
+then inherit its value (M_acclatch).  And every read-back is taken after its session ends, so a session that dies
+part-way blanks the rows it had already passed (M_acc4: session A died at step 5 and every accept row read `-`).
 
 Every stepped word is compared with the emulator's own step line (the hand-assembled-encoding trap).
-Output: one row per check, then FBCTRLP_CONTROL=OK|FAILED, FBCTRLP_RESULT=n/t, FBCTRLP_DONE.
+Output: one row per check, then FBCTRLP_CONTROL=OK|FAILED, FBCTRLP_RESULT=n/t, FBCTRLP_DONE.  The exit status is 0
+only when the controls are OK and every row is green: a red row is a nonzero exit, not only a crash.
 usage: fbctrl_port_probe.py <gxemul-binary>
 """
 import os
@@ -60,10 +87,12 @@
 FBCTRL = 0xffffffffb2f00000
 
 ONCE_RE = re.compile(r"\[ fbctrl: port number 0x[0-9a-f]+ is out of range; the selector is unchanged \(once\) \]")
+#  The refused value, captured whole: "0x8" can match only 0x8, never 0x80 (the digits run to " is").
+VAL_RE = re.compile(r"\[ fbctrl: port number (0x[0-9a-f]+) is out of range; the selector is unchanged \(once\) \]")
 
 REG = dict(zr=0, v0=2, v1=3, a0=4, a1=5, a2=6, a3=7, t0=8, t1=9, t2=10, t3=11, t4=12, t5=13, t6=14, t7=15,
            s0=16, s1=17, s2=18, s3=19, s4=20, s5=21, s6=22, s7=23, t8=24, t9=25)
-OPS = dict(sb=0x28, sh=0x29, sw=0x2b, sd=0x3f, lw=0x23)
+OPS = dict(sb=0x28, sh=0x29, sw=0x2b, sd=0x3f, lw=0x23, ld=0x37)
 
 
 def ins(op, rt, off, base="t0"):
@@ -81,6 +110,8 @@
 assert ins("sd", "t5", 0) == 0xfd0d0000
 assert ins("sb", "t8", 0) == 0xa1180000
 assert ins("sh", "t9", 0) == 0xa5190000
+assert ins("ld", "s3", 0) == 0xdd130000
+assert ins("sb", "zr", 0) == 0xa1000000
 assert ANCHOR == 0x3c0f0000
 
 
@@ -245,21 +276,23 @@
     return "-" if v is None else "0x%x" % v
 
 
-M64 = 0xffffffffffffffff
-
+def first_val(S):
+    """the value the FIRST announce of a session names, or '-'"""
+    m = VAL_RE.findall(S["buf"])
+    return m[0] if m else "-"
 
-def lw32(v):
-    """what `lw` of a 32-bit device answer yields in a 64-bit register (sign-extended)"""
-    v &= 0xffffffff
-    return v | 0xffffffff00000000 if v & 0x80000000 else v
 
+M64 = 0xffffffffffffffff
 
 # ---------------------------------------------------------------- sessions
 PROG_C = [("sw", "t1", 0, None), ("sw", "t3", 16, None), ("lw", "t4", 16, None), ("lw", "t5", 0, None),
-          ("sw", "t6", 0, None), ("sw", "t7", 16, None), ("sw", "s0", 0, None), ("sw", "s1", 16, None),
-          ("sw", "t6", 0, None), ("lw", "s2", 16, None)]
+          ("sw", "t6", 0, None), ("sw", "t7", 16, None),               # PORT=1 (X1), X1 = 123
+          ("sw", "s1", 0, None), ("sw", "t7", 16, None),               # PORT=2 (Y1), Y1 = 123
+          ("sw", "s0", 0, None), ("sw", "s1", 16, None),               # PORT=0 (COMMAND), DATA=2: GET_RESOLUTION
+          ("sw", "t6", 0, None), ("lw", "s2", 16, None),               # read X1
+          ("sw", "s1", 0, None), ("lw", "s3", 16, None)]               # read Y1
 REGS_C = [("t0", FBCTRL), ("t1", 5), ("t3", 0x2a), ("t6", 1), ("t7", 123), ("s0", 0), ("s1", 2),
-          ("t4", 0xdead), ("t5", 0xdead), ("s2", 0xdead)]
+          ("t4", 0xdead), ("t5", 0xdead), ("s2", 0xdead), ("s3", 0xdead)]
 
 #  A: selector p written at a rotating width and read back through PORT into s<k> (poisoned 0xdead first, so a
 #  read that never ran cannot pass -- selector 0 would otherwise match a register's reset value); DATA value 0x11*p
@@ -285,11 +318,13 @@
         PROG_A.append(("lw", SEL_REG[k], 16, None))
 READS_A = PORT_RB + SEL_REG[1:]
 
-#  P: previous selector 5, then nine refusals, then previous 7 and one more.
-REFUSE = [("sw", "t1", 9, "9 (sw)"), ("sw", "t2", 8, "8 (sw)"), ("sw", "t3", 16, "16 (sw)"),
+#  P: previous selector 5, then nine refusals with read-backs (the FIRST is 8), two count-only refusals, and the
+#  twelfth after PORT=7.  The count is sampled after the twelfth, so a latch re-armed every N refusals, N <= 11, reds.
+REFUSE = [("sw", "t2", 8, "8 (sw)"), ("sw", "t1", 9, "9 (sw)"), ("sw", "t3", 16, "16 (sw)"),
           ("sd", "t4", 0x200000000, "0x200000000 (sd)"), ("sd", "t5", 0x100000003, "0x100000003 (sd)"),
           ("sd", "t6", M64, "all-ones (sd)"), ("sw", "t7", 0xffffffff, "all-ones (sw)"),
           ("sb", "t8", 0xff, "0xff (sb)"), ("sh", "t9", 0x100, "0x100 (sh)")]
+EXTRA = [("sb", "t3"), ("sh", "t3")]                                   # 16 by sb and by sh
 READ_P = ["s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "v0"]
 PROG_P = [("sw", "a0", 0, None), ("sw", "a1", 16, None)]
 REGS_P = [("t0", FBCTRL), ("a0", 5), ("a1", 0x2a), ("a2", 7)]
@@ -299,25 +334,76 @@
         PROG_P.append(("sw", "a0", 0, None))                   # a fresh PORT=5 before every later refusal
     PROG_P.append((w, r, 0, "r%d" % k))
     PROG_P.append(("lw", READ_P[k], 0, None))
-PROG_P += [("sw", "a2", 0, None), ("sw", "t1", 0, "r9"), ("lw", "v1", 0, None)]
+for w, r in EXTRA:
+    PROG_P += [("sw", "a0", 0, None), (w, r, 0, None)]
+PROG_P += [("sw", "a2", 0, None), ("sw", "t1", 0, "r11"), ("lw", "v1", 0, None)]
 READS_P = READ_P + ["v1"]
 
+#  R: a DATA write and a NOP command between two refusals -- in its own session.
+PROG_R = [("sw", "a0", 0, None), ("sw", "t1", 0, "ra"), ("lw", "s0", 0, None),
+          ("sw", "a1", 16, None), ("sw", "zr", 0, None), ("sw", "zr", 16, None),
+          ("sw", "a0", 0, None), ("sw", "t1", 0, "rb"), ("lw", "s1", 0, None)]
+REGS_R = [("t0", FBCTRL), ("a0", 5), ("a1", 0x2a), ("t1", 9), ("s0", 0xdead), ("s1", 0xdead)]
+
 PROG_K = [("sw", "t1", 0, None), ("sw", "t3", 16, None), ("sw", "t2", 0, None), ("lw", "s0", 16, None),
           ("sw", "t4", 16, None), ("sw", "t1", 0, None), ("lw", "s1", 16, None)]
 REGS_K = [("t0", FBCTRL), ("t1", 5), ("t3", 0x2a), ("t2", 9), ("t4", 0x77), ("s0", 0xdead), ("s1", 0xdead)]
 
-PROG_F = [("sw", "t1", 0, None)]
-REGS_F = [("t0", FBCTRL), ("t1", 9)]
+#  F: the free-run executes the refused sw AND a guest lw of PORT into a poisoned t2 (a GPR nothing loads would
+#  print the zero cpu_new() gave it on every device -- the channel has to be a guest load).
+PROG_F = [("sw", "t1", 0, None), ("lw", "t2", 0, None)]
+REGS_F = [("t0", FBCTRL), ("t1", 9), ("t2", 0xdead)]
+
+#  V: X1 across a refusal made while COMMAND still holds GET_RESOLUTION, then every cell across four refusals.
+#  Port 0 is never written after the first GET_RESOLUTION: a DATA write there EXECUTES the command.
+REGS_V = [("t0", FBCTRL)] + [("s%d" % p, p) for p in range(1, 8)] + [("t%d" % p, 0x11 * p) for p in range(1, 8)] + \
+         [("t8", 123), ("a0", 9), ("a1", 16), ("a2", 0x100000003), ("a3", 0xff), ("v0", 0xdead), ("v1", 0xdead)]
+PROG_V = [("sw", "zr", 0, None), ("sw", "s2", 16, None),               # COMMAND = GET_RESOLUTION (X1 = Y1 = 0)
+          ("sw", "s1", 0, None), ("sw", "t8", 16, None),               # X1 = 123
+          ("sw", "a0", 0, None),                                        # refuse 9
+          ("sw", "s1", 0, None), ("lw", "v0", 16, None)]                # read X1
+for p in range(1, 8):
+    PROG_V += [("sw", "s%d" % p, 0, None), ("sw", "t%d" % p, 16, None)]
+PROG_V += [("sw", "a0", 0, None), ("sw", "a1", 0, None), ("sd", "a2", 0, None), ("sb", "a3", 0, None)]
+PROG_V += [("sw", "zr", 0, None), ("lw", "v1", 16, None)]
+for p in range(1, 8):
+    PROG_V += [("sw", "s%d" % p, 0, None), ("lw", "s%d" % p, 16, None)]
+READS_V = ["v0", "v1"] + ["s%d" % p for p in range(1, 8)]
+
+#  W: the width x boundary cells, each after its own non-zero predecessor into a poisoned read-back; then an ld.
+W_CELLS = [("accept 0 written by sb after PORT=5", "a0", "sb", "zr", "s0", 0),
+           ("accept 0 written by sh after PORT=5", "a0", "sh", "zr", "s1", 0),
+           ("accept 0 written by sw after PORT=5", "a0", "sw", "zr", "s2", 0),
+           ("accept 0 written by sd after PORT=5", "a0", "sd", "zr", "s3", 0),
+           ("accept 7 written by sb after PORT=5", "a0", "sb", "t5", "s4", 7),
+           ("accept 7 written by sh after PORT=5", "a0", "sh", "t5", "s5", 7),
+           ("accept 7 written by sw after PORT=5", "a0", "sw", "t5", "s6", 7),
+           ("refuse 8 (sb), PORT keeps 5", "a0", "sb", "t4", "s7", 5),
+           ("refuse 8 (sh), PORT keeps 5", "a0", "sh", "t4", "v0", 5),
+           ("refuse 8 (sd), PORT keeps 5", "a0", "sd", "t4", "v1", 5),
+           ("refuse 0x8000000000000000 (sd), PORT keeps 5", "a0", "sd", "t2", "t6", 5),
+           ("refuse 9 after PORT=6, PORT keeps 6", "a3", "sw", "t1", "t8", 6)]
+PROG_W = []
+REGS_W = [("t0", FBCTRL), ("a0", 5), ("a3", 6), ("t1", 9), ("t2", 0x8000000000000000), ("t4", 8), ("t5", 7),
+          ("t9", 0xdead)]
+for _n, pred, w, val, rb, _want in W_CELLS:
+    PROG_W += [("sw", pred, 0, None), (w, val, 0, None), ("lw", rb, 0, None)]
+    REGS_W.append((rb, 0xdead))
+PROG_W += [("sw", "a0", 0, None), ("ld", "t9", 0, None)]               # ld of PORT with selector 5
+READS_W = [c[4] for c in W_CELLS] + ["t9"]
 
 
 def main():
     stub = stub_path()
     try:
-        C = session("C", PROG_C, REGS_C, ["t4", "t5", "s2"], stub)
+        C = session("C", PROG_C, REGS_C, ["t4", "t5", "s2", "s3"], stub)
         A = session("A", PROG_A, REGS_A, READS_A, stub)
         P = session("P", PROG_P, REGS_P, READS_P, stub)
+        R = session("R", PROG_R, REGS_R, ["s1"], stub)
         K = session("K", PROG_K, REGS_K, ["s0", "s1"], stub)
-        F = session("F", PROG_F, REGS_F, [], stub, free_run=True)
+        F = session("F", PROG_F, REGS_F, ["t2"], stub, free_run=True)
+        V = session("V", PROG_V, REGS_V, READS_V, stub)
+        W = session("W", PROG_W, REGS_W, READS_W, stub)
     finally:
         try:
             os.unlink(stub)
@@ -332,21 +418,28 @@
     ctl.append(row("C LIVENESS: PORT reads back 5", hx(C["vals"].get("t5")), "0x5"))
     ctl.append(row("C SIGNATURE: X1 zeroed by GET_RESOLUTION", hx(C["vals"].get("s2")), "0x0",
                    "(RAM: 2; banked w/o command: 123)"))
+    ctl.append(row("C SIGNATURE: Y1 zeroed by GET_RESOLUTION", hx(C["vals"].get("s3")), "0x0",
+                   "(prefilled 123)"))
     row("C nothing refused, no (once) line", len(ONCE_RE.findall(C["buf"])), 0)
-    for S in (A, P, K):
-        ctl.append(row("%s disassembly of every stepped word" % "APK"[(A, P, K).index(S)], len(S["badis"]), 0))
+    for lab, S in (("A", A), ("P", P), ("R", R), ("K", K), ("V", V), ("W", W)):
+        ctl.append(row("%s disassembly of every stepped word" % lab, len(S["badis"]), 0))
     print("ACCEPT (session A: %s %d/%d)" % (A["status"], A["steps"], A["n"]))
     for k, (p, w) in enumerate(ACC):
         row("accept selector %d written by %s" % (p, w), hx(A["vals"].get(PORT_RB[k])), hx(p))
     for k, (p, w) in enumerate(ACC):
         if k:
             row("port %d round-trips its DATA value" % p, hx(A["vals"].get(SEL_REG[k])), hx(0x11 * p))
+    row("A nothing refused, no (once) line", len(ONCE_RE.findall(A["buf"])), 0)
     print("REFUSE (session P: %s %d/%d)" % (P["status"], P["steps"], P["n"]))
     for k, (w, r, v, name) in enumerate(REFUSE):
         row("refuse %s, PORT keeps 5" % name, hx(P["vals"].get(READ_P[k])), "0x5")
     row("refuse 9 after PORT=7, PORT keeps 7", hx(P["vals"].get("v1")), "0x7")
     row("announce: exactly 1 right after the FIRST refusal", P["once_after"].get("r0"), 1)
-    row("announce: still exactly 1 after ten refusals", P["once_after"].get("r9"), 1)
+    row("announce: still exactly 1 after twelve refusals", P["once_after"].get("r11"), 1)
+    row("announce names the first refused value, 0x8", first_val(P), "0x8")
+    print("RE-ARM (session R: %s %d/%d)" % (R["status"], R["steps"], R["n"]))
+    row("R announce still 1 after DATA and NOP traffic", R["once_after"].get("rb"), 1)
+    row("R refuse 9 after the NOP, PORT keeps 5", hx(R["vals"].get("s1")), "0x5")
     print("THE WITNESS PAIR (session K)")
     row("K survives DATA after a refused PORT write", "%s %d/%d" % (K["status"], K["steps"], K["n"]),
         "SURVIVED %d/%d" % (len(PROG_K), len(PROG_K)))
@@ -355,12 +448,24 @@
     print("FREE-RUNNING (session F)")
     row("F free-run reached its breakpoint", F["status"], "SURVIVED")
     row("F refusal announced while free-running (fatal)", F["once_after"].get("free"), 1)
+    row("F lw of PORT after the power-on refusal reads 0", hx(F["vals"].get("t2")), "0x0")
+    row("F announce names the refused value, 0x9", first_val(F), "0x9")
+    print("CELLS (session V: %s %d/%d)" % (V["status"], V["steps"], V["n"]))
+    row("V X1=123 survives a refusal (COMMAND holds 2)", hx(V["vals"].get("v0")), hx(123))
+    row("V port 0 (COMMAND) still 2 after four refusals", hx(V["vals"].get("v1")), "0x2")
+    for p in range(1, 8):
+        row("V port %d keeps its fill after four refusals" % p, hx(V["vals"].get("s%d" % p)), hx(0x11 * p))
+    print("WIDTHS (session W: %s %d/%d)" % (W["status"], W["steps"], W["n"]))
+    for name, _p, _w, _v, rb, want in W_CELLS:
+        row(name, hx(W["vals"].get(rb)), hx(want))
+    row("ld of PORT reads exactly 5", hx(W["vals"].get("t9")), "0x5")
     control = all(ctl)
     n_ok, n = sum(RESULTS), len(RESULTS)
     print("FBCTRLP_CONTROL=%s" % ("OK" if control else "FAILED"))
     print("FBCTRLP_RESULT=%d/%d" % (n_ok, n))
     print("FBCTRLP_DONE")
+    return 0 if control and n_ok == n else 1
 
 
 if __name__ == "__main__":
-    main()
+    sys.exit(main())
```

### 4c. regress/gate_mips_folds.sh: the block F2 reviewed -> now

```diff
--- a/regress/gate_mips_folds.sh (as reviewed in pass 2 and F2)
+++ b/regress/gate_mips_folds.sh (now)
@@ -34,19 +34,22 @@
 if [ ! -x "$PMAX" ]; then gate_skip "no gxemul binary at $PMAX"; fi
 
 #  ---------------------------------------------------------------------------------------
-#  #549 fbctrlportkill: dev_fbctrl.c's PORT selector, on -E testmips.  Before #549 a guest
-#  store of 8 or more to PORT was STORED with only a warning, and the next DATA access ended
-#  the emulator in the DATA arm's range check.  #549 refuses the selector (the previous one
-#  is kept) and announces the refusal once.  regress/fbctrl_port_probe.py drives real guest
-#  sb/sh/sw/sd/lw on an unmodified testmips -- no kernel, no rig image -- so it runs BEFORE
+#  #549 fbctrlportkill: dev_fbctrl.c's PORT selector, on -E testmips.  Before #549 the PORT
+#  arm STORED the selector as an int with only a warning: 9 made the next DATA access end the
+#  emulator in the DATA arm's range check, and a wide value was truncated onto a legal port.
+#  #549 refuses any selector >= 8 (the previous one is kept) and announces the refusal once.
+#  regress/fbctrl_port_probe.py drives real guest sb/sh/sw/sd/lw/ld on an unmodified
+#  testmips -- no kernel, no rig image -- so it runs BEFORE
 #  this gate's pmax-kernel check: a missing kernel still skips the fold rows below, and
 #  gate_skip reports FAIL, not SKIP, if an fbctrl row failed first.
 #
-#  THE CONTRACT is the probe's header (CATCHES / NOT CLAIMED).  Kill table 1 was red on 20 of
-#  20 edits of the fix's own predicate, store and latch; a process-global latch and the
-#  deletion of the DATA arm's kept check are DISCLOSED escapes; and the device still ends the
-#  process through its command and offset defaults, which are filed, not claimed.  HEAD before
-#  #549 scored 25/41 here, every refusal row red.
+#  THE CONTRACT is the probe's header (CATCHES / NOT CLAIMED).  Kill table 3
+#  (regress/artifacts/fbctrlportkill_20260924/table3/TABLE.out) built 62 edits: the 54 the
+#  contract does not disclose are ALL red, HEAD's own arm among them (M_revert, 47/73 here:
+#  every refusal row red, and sessions K and R ended the process); the 8 it discloses score
+#  73/73 -- a process-global latch, the DATA arm's kept check deleted, a serial-number
+#  condition, three equivalent edits and two DATA-width edits.  The device still ends the
+#  process through its command and offset defaults, which are filed, not claimed.
 #
 #  `gatedevicesplit` is OWED (#498): one more device probe in a CPU gate, as #548 added to
 #  gate 14.  Recorded, not compounded silently.
@@ -65,12 +68,23 @@
     check "fbctrl probe output parses" "yes" "yes"
     grep -E '^  FAIL ' "$FBCLOG" | sed 's/^/       /'
     check "fbctrl probe controls" "$(sed -n 's/^FBCTRLP_CONTROL=//p' "$FBCLOG")" "OK"
-    check "fbctrl probe exit status" "$fbrc" "0"
+    #  The probe exits nonzero on a crash OR a red row (#549 F2), so this is a second catcher
+    #  of a red score, not only of a Python failure.
+    check "fbctrl probe exit 0 (nonzero: a crash or a red row)" "$fbrc" "0"
     fbres=$(sed -n 's/^FBCTRLP_RESULT=//p' "$FBCLOG")
-    #  Pinned UNQUOTED under a one-token stem, so check_score_claims.py sees the pin.
-    check "fbctrl_port rows run" "${fbres#*/}" 41
-    check "fbctrl_port rows correct" "${fbres%/*}" "41"
+    #  Pinned UNQUOTED under a one-token stem, so check_score_claims.py sees the pin.  The
+    #  quoted numerator is inert to that checker BY DESIGN -- it keys on `rows run' -- and the
+    #  exit row above and the two reconciliation rows below are what catch a red or edited score.
+    check "fbctrl_port rows run" "${fbres#*/}" 73
+    check "fbctrl_port rows correct" "${fbres%/*}" "73"
     check "fbctrl_port rows failed" "$(grep -c '^  FAIL ' "$FBCLOG")" "0"
+    #  RECONCILE the rows the probe PRINTED with the trailer it printed (#549 F2, measured by
+    #  the Opus seat): checking the trailer alone, a log with one row deleted and its
+    #  RESULT line intact passed every check above.
+    check "fbctrl_port rows emitted match the trailer total" \
+          "$(grep -cE '^  (ok|FAIL) ' "$FBCLOG")" "${fbres#*/}"
+    check "fbctrl_port ok rows match the trailer count" \
+          "$(grep -c '^  ok ' "$FBCLOG")" "${fbres%/*}"
 fi
 
 if [ ! -f "$PMAX_KERNEL" ]; then gate_skip "no pmax kernel at $PMAX_KERNEL"; fi
```

## 5. EVIDENCE (all measured; durable under regress/artifacts/fbctrlportkill_20260924/)

### 5a. Kill table 3 -- 62 edits of the final fix, each built in a scratch clone and scored by a FROZEN copy of the probe

Predictions were written BEFORE the run (PRETABLE_ADDENDUM_t3.out, whose mtime precedes table3/): 54 red and 8 at 73/73,
with HEAD's arm (M_revert) at 47/73 -- every prediction held.  `rc` is the probe's own exit status.  Row lists are
trimmed at 200 characters; the raw per-edit logs are table3/<name>.raw.

```
#549 kill table 3 -- started 2026-09-25 13:53:56
probe md5 ad43c3dd  mutants549_t3 md5 b8df0fa7
base: fix build md5 b5b99e6d  build/gxemul md5 b5b99e6d  13:54:02
base_fix rc=0 FBCTRLP_RESULT=73/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE
M_acc4 md5=8696b6ba rc=1 FBCTRLP_RESULT=53/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | accept selector 0 written by sw;accept selector 1 written by sb;accept selector 2 written by sh;accept selector 3 writte ...
M_acclatch md5=cf5d817b rc=1 FBCTRLP_RESULT=64/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | refuse 9 after PORT=7, PORT keeps 7;V port 0 (COMMAND) still 2 after four refusals;V port 1 keeps its fill after fou ...
M_and5 md5=c3e2ba53 rc=1 FBCTRLP_RESULT=71/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | refuse 9 after PORT=7, PORT keeps 7;refuse 9 after PORT=6, PORT keeps 6;
M_ann_any md5=23dca4fc rc=1 FBCTRLP_RESULT=70/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | C nothing refused, no (once) line;A nothing refused, no (once) line;announce names the first refused value, 0x8;
M_bit md5=4a18f0ed rc=1 FBCTRLP_RESULT=69/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | refuse 16 (sw), PORT keeps 5;refuse 0x200000000 (sd), PORT keeps 5;refuse 0x100 (sh), PORT keeps 5;refuse 0x8000000000000 ...
M_clamp md5=d1ce1dfe rc=1 FBCTRLP_RESULT=54/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | refuse 8 (sw), PORT keeps 5;refuse 9 (sw), PORT keeps 5;refuse 16 (sw), PORT keeps 5;refuse 0x200000000 (sd), PORT keep ...
M_debug md5=147b5bf4 rc=1 FBCTRLP_RESULT=71/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | F refusal announced while free-running (fatal);F announce names the refused value, 0x9;
M_decl md5=e4401cf2 rc=1 FBCTRLP_RESULT=71/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | refuse all-ones (sd), PORT keeps 5;refuse 0x8000000000000000 (sd), PORT keeps 5;
M_gt md5=9b21ac29 rc=1 FBCTRLP_RESULT=67/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | refuse 8 (sw), PORT keeps 5;announce: exactly 1 right after the FIRST refusal;announce names the first refused value, 0x8; ...
M_i32 md5=16b41df0 rc=1 FBCTRLP_RESULT=68/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | refuse 0x200000000 (sd), PORT keeps 5;refuse 0x100000003 (sd), PORT keeps 5;refuse all-ones (sd), PORT keeps 5;refuse all ...
M_i64 md5=2b14831f rc=1 FBCTRLP_RESULT=71/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | refuse all-ones (sd), PORT keeps 5;refuse 0x8000000000000000 (sd), PORT keeps 5;
M_latch0 md5=49ac83fe rc=1 FBCTRLP_RESULT=71/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | announce: still exactly 1 after twelve refusals;R announce still 1 after DATA and NOP traffic;
M_latchcnt md5=fb8f352b rc=1 FBCTRLP_RESULT=67/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | announce: exactly 1 right after the FIRST refusal;announce: still exactly 1 after twelve refusals;announce names the ...
M_latchinv md5=b82afb90 rc=1 FBCTRLP_RESULT=67/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | announce: exactly 1 right after the FIRST refusal;announce: still exactly 1 after twelve refusals;announce names the ...
M_mod33 md5=c8961157 rc=1 FBCTRLP_RESULT=71/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | refuse 0x200000000 (sd), PORT keeps 5;refuse 0x8000000000000000 (sd), PORT keeps 5;
M_noguard md5=45d19e00 rc=0 FBCTRLP_RESULT=73/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | 
M_perval md5=357444fa rc=1 FBCTRLP_RESULT=72/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | announce: still exactly 1 after twelve refusals;
M_reflatch md5=8b7f1381 rc=1 FBCTRLP_RESULT=59/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | refuse 9 (sw), PORT keeps 5;refuse 16 (sw), PORT keeps 5;refuse 0x200000000 (sd), PORT keeps 5;refuse 0x100000003 (s ...
M_rej2 md5=7565d641 rc=1 FBCTRLP_RESULT=70/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | accept selector 2 written by sh;port 1 round-trips its DATA value;V port 1 keeps its fill after four refusals;
M_reset0 md5=fce0ab37 rc=1 FBCTRLP_RESULT=53/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | refuse 8 (sw), PORT keeps 5;refuse 9 (sw), PORT keeps 5;refuse 16 (sw), PORT keeps 5;refuse 0x200000000 (sd), PORT kee ...
M_revert md5=9fa0c1f9 rc=1 FBCTRLP_RESULT=47/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | refuse 8 (sw), PORT keeps 5;refuse 9 (sw), PORT keeps 5;refuse 16 (sw), PORT keeps 5;refuse 0x200000000 (sd), PORT kee ...
M_static md5=1d4530bc rc=0 FBCTRLP_RESULT=73/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | 
M_store md5=04b6a0c8 rc=1 FBCTRLP_RESULT=52/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | refuse 8 (sw), PORT keeps 5;refuse 9 (sw), PORT keeps 5;refuse 16 (sw), PORT keeps 5;refuse 0x200000000 (sd), PORT keep ...
M_u32 md5=30db6cfd rc=1 FBCTRLP_RESULT=70/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | refuse 0x200000000 (sd), PORT keeps 5;refuse 0x100000003 (sd), PORT keeps 5;refuse 0x8000000000000000 (sd), PORT keeps 5;
M_wide md5=127e60d2 rc=1 FBCTRLP_RESULT=69/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | refuse 0xff (sb), PORT keeps 5;refuse 0x100 (sh), PORT keeps 5;refuse 8 (sb), PORT keeps 5;refuse 8 (sh), PORT keeps 5;
N_acc32 md5=b5b99e6d rc=0 FBCTRLP_RESULT=73/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | 
N_clobcell md5=b4083199 rc=1 FBCTRLP_RESULT=68/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | V X1=123 survives a refusal (COMMAND holds 2);V port 0 (COMMAND) still 2 after four refusals;V port 1 keeps its fill ...
N_clobcmd md5=e23dd83d rc=1 FBCTRLP_RESULT=72/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | V port 0 (COMMAND) still 2 after four refusals;
N_cmdport md5=c960fc3f rc=1 FBCTRLP_RESULT=69/73 FBCTRLP_CONTROL=FAILED FBCTRLP_DONE | C SIGNATURE: X1 zeroed by GET_RESOLUTION;C SIGNATURE: Y1 zeroed by GET_RESOLUTION;V X1=123 survives a refusal (CO ...
N_cmdread md5=dadbbf71 rc=1 FBCTRLP_RESULT=70/73 FBCTRLP_CONTROL=FAILED FBCTRLP_DONE | C SIGNATURE: X1 zeroed by GET_RESOLUTION;C SIGNATURE: Y1 zeroed by GET_RESOLUTION;V port 0 (COMMAND) still 2 afte ...
N_datard16 md5=a952d677 rc=0 FBCTRLP_RESULT=73/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | 
N_datarearm md5=12843f44 rc=1 FBCTRLP_RESULT=72/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | R announce still 1 after DATA and NOP traffic;
N_datawr8 md5=d48be2cf rc=0 FBCTRLP_RESULT=73/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | 
N_order md5=66caf9d0 rc=0 FBCTRLP_RESULT=73/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | 
N_rdlatch md5=ff845eda rc=1 FBCTRLP_RESULT=55/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | refuse 8 (sw), PORT keeps 5;refuse 9 (sw), PORT keeps 5;refuse 16 (sw), PORT keeps 5;refuse 0x200000000 (sd), PORT ke ...
N_rdmask3 md5=52d27852 rc=1 FBCTRLP_RESULT=48/73 FBCTRLP_CONTROL=FAILED FBCTRLP_DONE | C LIVENESS: PORT reads back 5;accept selector 4 written by sd;accept selector 5 written by sb;accept selector 6 w ...
N_rdmask7 md5=799cca49 rc=0 FBCTRLP_RESULT=73/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | 
N_rearm md5=76977668 rc=1 FBCTRLP_RESULT=71/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | announce: still exactly 1 after twelve refusals;R announce still 1 after DATA and NOP traffic;
N_runcmd md5=16fd0156 rc=1 FBCTRLP_RESULT=70/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | V X1=123 survives a refusal (COMMAND holds 2);V port 1 keeps its fill after four refusals;V port 2 keeps its fill afte ...
T_D10_print0 md5=a12718ca rc=1 FBCTRLP_RESULT=71/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | announce names the first refused value, 0x8;F announce names the refused value, 0x9;
T_D11a_y1one md5=5fb229f9 rc=1 FBCTRLP_RESULT=72/73 FBCTRLP_CONTROL=FAILED FBCTRLP_DONE | C SIGNATURE: Y1 zeroed by GET_RESOLUTION;
T_D11b_y1keep md5=b32bf781 rc=1 FBCTRLP_RESULT=72/73 FBCTRLP_CONTROL=FAILED FBCTRLP_DONE | C SIGNATURE: Y1 zeroed by GET_RESOLUTION;
T_D2_mask63 md5=4d17e028 rc=1 FBCTRLP_RESULT=72/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | refuse 0x8000000000000000 (sd), PORT keeps 5;
T_D3_ctor1 md5=119740b1 rc=1 FBCTRLP_RESULT=72/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | F lw of PORT after the power-on refusal reads 0;
T_D3_pwron md5=caa267d0 rc=1 FBCTRLP_RESULT=72/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | F lw of PORT after the power-on refusal reads 0;
T_D4b_cmdrearm md5=7e91c1fd rc=1 FBCTRLP_RESULT=72/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | R announce still 1 after DATA and NOP traffic;
T_D6_rdbit32 md5=2168ccad rc=1 FBCTRLP_RESULT=72/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | ld of PORT reads exactly 5;
T_D7a_sub4zero md5=189f2cc3 rc=1 FBCTRLP_RESULT=71/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | accept 0 written by sb after PORT=5;accept 0 written by sh after PORT=5;
T_D7b_sdzero md5=0f9e761e rc=1 FBCTRLP_RESULT=72/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | accept 0 written by sd after PORT=5;
T_D7c_shzero md5=2a8d4957 rc=1 FBCTRLP_RESULT=72/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | accept 0 written by sh after PORT=5;
T_D8_or1 md5=fb016055 rc=1 FBCTRLP_RESULT=71/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | F lw of PORT after the power-on refusal reads 0;refuse 9 after PORT=6, PORT keeps 6;
T_D9a_only9 md5=227c96fb rc=1 FBCTRLP_RESULT=71/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | announce: exactly 1 right after the FIRST refusal;announce names the first refused value, 0x8;
T_D9b_mod10 md5=400bca95 rc=1 FBCTRLP_RESULT=72/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | announce: still exactly 1 after twelve refusals;
T_D9c_serial1 md5=0b8351e5 rc=0 FBCTRLP_RESULT=73/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | 
T_W_sb7 md5=6c64ceee rc=1 FBCTRLP_RESULT=72/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | accept 7 written by sb after PORT=5;
T_W_sb8 md5=323511fe rc=1 FBCTRLP_RESULT=72/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | refuse 8 (sb), PORT keeps 5;
T_W_sh7 md5=964158bb rc=1 FBCTRLP_RESULT=72/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | accept 7 written by sh after PORT=5;
T_W_sh8 md5=e66de4a1 rc=1 FBCTRLP_RESULT=72/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | refuse 8 (sh), PORT keeps 5;
T_W_sw0 md5=137ac045 rc=1 FBCTRLP_RESULT=67/73 FBCTRLP_CONTROL=FAILED FBCTRLP_DONE | C SIGNATURE: X1 zeroed by GET_RESOLUTION;C SIGNATURE: Y1 zeroed by GET_RESOLUTION;C nothing refused, no (once) line ...
T_W_sw7 md5=3be82c1a rc=1 FBCTRLP_RESULT=68/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | port 7 round-trips its DATA value;A nothing refused, no (once) line;refuse 9 after PORT=7, PORT keeps 7;V port 6 keeps  ...
T_X_ann6 md5=cdda0301 rc=1 FBCTRLP_RESULT=72/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | A nothing refused, no (once) line;
T_X_w8 md5=fd65fcac rc=1 FBCTRLP_RESULT=70/73 FBCTRLP_CONTROL=OK FBCTRLP_DONE | refuse 8 (sb), PORT keeps 5;refuse 8 (sh), PORT keeps 5;refuse 8 (sd), PORT keeps 5;
restored: cmp SEC clean, binary fresh, md5 == base; sentinel cleared
probe source unchanged during the run
TABLE3_DONE 14:01:17
```

### 5b. Gate 16 on the working tree: PASS (25 checks), 27 s, fbctrl rows 73/73 (gates_f2/gate16.out)

### 5c. The revised gate block on logs derived from that 73-row log (g16_fixtures_t3.out)

```
good                         probe_rc=0  PASS (8 checks)              | red: 
good                         probe_rc=1  FAIL (1 of 8 checks)         | red: fbctrl probe exit 0 (nonzero: a crash or a red row);
row_deleted                  probe_rc=0  FAIL (2 of 8 checks)         | red: fbctrl_port rows emitted match the trailer total;fbctrl_port ok rows match the trailer count;
row_deleted                  probe_rc=1  FAIL (3 of 8 checks)         | red: fbctrl probe exit 0 (nonzero: a crash or a red row);fbctrl_port rows emitted match the trailer total;fbctrl_port ok rows match the trailer count;
row_failed_result_intact     probe_rc=0  FAIL (2 of 8 checks)         | red: fbctrl_port rows failed;fbctrl_port ok rows match the trailer count;
row_failed_result_intact     probe_rc=1  FAIL (3 of 8 checks)         | red: fbctrl probe exit 0 (nonzero: a crash or a red row);fbctrl_port rows failed;fbctrl_port ok rows match the trailer count;
row_duplicated               probe_rc=0  FAIL (2 of 8 checks)         | red: fbctrl_port rows emitted match the trailer total;fbctrl_port ok rows match the trailer count;
row_duplicated               probe_rc=1  FAIL (3 of 8 checks)         | red: fbctrl probe exit 0 (nonzero: a crash or a red row);fbctrl_port rows emitted match the trailer total;fbctrl_port ok rows match the trailer count;
row_failed_result_honest     probe_rc=0  FAIL (2 of 8 checks)         | red: fbctrl_port rows correct;fbctrl_port rows failed;
row_failed_result_honest     probe_rc=1  FAIL (3 of 8 checks)         | red: fbctrl probe exit 0 (nonzero: a crash or a red row);fbctrl_port rows correct;fbctrl_port rows failed;
row_deleted_trailer_edited   probe_rc=0  FAIL (2 of 8 checks)         | red: fbctrl_port rows run;fbctrl_port rows correct;
row_deleted_trailer_edited   probe_rc=1  FAIL (3 of 8 checks)         | red: fbctrl probe exit 0 (nonzero: a crash or a red row);fbctrl_port rows run;fbctrl_port rows correct;
G16FIX_T3_DONE
```

## 6. QUESTIONS

1. **The floor, asked of the SHIPPED COMPOSITE (the 73-row detector), not only of the repair:** is there an edit of
   `dev_fbctrl.c` inside the DEPENDS-ON enumeration -- the predicates dominating the fixed arm (`writeflag == MEM_READ`,
   `idata >= DEV_FBCTRL_NPORTS`, `!d->warned_port`), weakened or qualified, or their operands swapped for fields the
   guarded body reads (`idata`, `current_port`, `warned_port`, `port[]`) -- that scores 73/73 and is NOT one of the eight
   the contract discloses?  Give the exact tokens and the rows you expect to stay green.
2. **What is the smallest edit that breaks the fix and still passes all 73 rows?**  Name the edit and the row(s) you
   expect to stay green.  An edit already in the table (§5) is worth nothing; say so if yours is one.
3. **Is any row vacuous by construction** -- its named channel cannot differ under its named edit?  In particular the
   R session's "refuse 9 after the NOP, PORT keeps 5" killed nothing on its own in table 3: keep it, or drop it?
4. **The contract (the probe's header, §4b):** is any sentence false, or true only of the case measured?  The same for
   the gate comment (§4c) and the one changed sentence in `dev_fbctrl.c` (§4a).
5. **The gate's reconciliation rows:** can a probe log pass all eight gate checks while a row is wrong?
6. **The dispositions in §2** -- which one is wrong?  Name the count.

If, while verifying a claim, you found something ELSE -- say so.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
