# #549 v6 -- THE REPAIR'S OWN PASS: the fbctrl port-selector test after the verifying pass found a gap (measured)

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/`.**  There are THREE pristine-2021-upstream copies of GXemul under the
project root (`./src/` and two under `_archive/audit-results-*/builds/`); they are NOT this fork.  **The working
tree's `regress/fbctrl_port_probe.py` is still v5 (111 rows)**; v6 exists as the generated file named below and the
diff inlined in section 5.  Review the INLINED v6, not the checkout.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any premise you cannot settle
from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — a count, a stored value, a bit range — ENUMERATE it rather than
reasoning about it.**  Walk the values.

**VERDICT LINE FIRST:** `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then numbered findings.

## 1. WHAT THIS IS

`src/devices/dev_fbctrl.c`'s PORT register selects which of eight data ports the DATA register reaches.  Before
#549 it STORED any written selector as an int with only a warning; a selector of 8 or more then made the next DATA
access stop the emulator in the DATA arm's range check, and a wide value was truncated onto a legal port.  **#549
refuses any selector >= 8, compared on the full 64-bit value, keeps the previous (always valid) selector, and
announces the refusal once per device.**  The fix itself has not changed since pass 2; every later pass has been
about the TEST that pins it, `regress/fbctrl_port_probe.py`, a real-guest probe on an unmodified `-E testmips`.

The chain so far: pass 1 (design), pass 2 (diff), F2 (findings shared), a closing pass, a closing F2, and a
**verifying pass on v5** (111 rows) -- which found a **floor breach**: the compare narrowed to ignore a RANGE of bits
scored the full 111 rows.  **v6 is the repair, and under the repair-chain rule it owes ITS OWN pass: this one.**  The
chain closes on the first VALID pass that finds zero floor breaches, carried with its denominator (the shapes tried).

## 2. SETTLED PREMISES (re-inlined; each checked against the tree)

* **The fixed PORT arm, verbatim** (`dev_fbctrl.c`, `case DEV_FBCTRL_PORT:`):

```c
	case DEV_FBCTRL_PORT:
		if (writeflag == MEM_READ)
			odata = d->current_port;
		else if (idata >= DEV_FBCTRL_NPORTS) {
			/*  #549: an out-of-range selector is REFUSED, and
			    current_port keeps its previous, always-valid value.
			    ... (comment condensed)  */
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

  `DEV_FBCTRL_NPORTS` is 8.  `idata` and `odata` are `uint64_t`, initialised to 0; `current_port` and `warned_port`
  are `int` fields of the device struct.  The common tail writes `odata` back for a read (`memory_writemax64(cpu,
  data, len, odata)`) and returns 1.
* **What `idata` holds for a store of width `len`**: the `len` bytes the guest stored, zero-extended (`memory_readmax64`
  assembles bytes; it does not sign-extend).  So `sb` gives 0..0xff, `sh` 0..0xffff, `sw` 0..0xffffffff, `sd` the
  full 64 bits.
* **An int store of a wide value keeps its low 32 bits** on this compiler (gcc, x86-64): `(int) 2^k` is 2^k for k <
  31, INT_MIN for k = 31, and 0 for k >= 32.  A PORT read returns `current_port` sign-extended into `odata`.
* **How the probe runs**: each session is a fresh `gxemul -V -E testmips`; the program's words are planted with
  `put w`, registers set with `name=value`, and each instruction is executed with `step 1`, except session F, which
  free-runs to a breakpoint.  Every stepped word's disassembly is compared with the emulator's own step line (a
  mismatch is a CONTROL failure).  Register read-backs are printed with `print <reg>` after the session.  `(once)`
  announces are counted in the session's output, and a tag on a step samples that count right after it.
* **Gate 16** (`regress/gate_mips_folds.sh`) runs the probe and requires: one `FBCTRLP_DONE`, a parseable
  `FBCTRLP_RESULT=n/t`, `FBCTRLP_CONTROL=OK`, exit 0, `t` pinned (111 today, 117 for v6), `n == t`, no FAIL lines,
  the printed rows reconciled with the trailer, and every row name printed once.

## 3. THE VERIFYING PASS'S FINDINGS, SHARED -- WITH HOW v6 DISPOSED OF EACH

Seats that answered the verifying pass on v5 (`panel_20260925_163907` + the dedicated grok job + the Opus 5.5 measuring
seat): **agy, grok, glm, deepseek, minimax, kimi-k3** (all SHIP WITH CHANGES) and **Opus 5.5** (SHIP WITH CHANGES --
re-issued after its first answer came from a model fallback, which is kept apart and not counted).  **Codex (GPT-6
Astra) and the kimi CLI were walled** (usage limits) -- seat failures, not agreement.

* **V1 -- THE FLOOR BREACH (Opus, MEASURED, `opus549_measured/c3/TABLE_mask.out`).**  `else if ((idata &
  ~0xfffffe00ULL) >= DEV_FBCTRL_NPORTS)` (bits 9-31 ignored), the same with `~0xe0ULL` (bits 5-7) and with
  `~0x7ffffffc00000000ULL` (bits 34-62) each scored 111/111; the control, bit 8 alone, scored 107/111 (v5 refuses 0x100).
  The first of them brings back the DATA arm's range-check exit: a guest writes 0x200 to PORT, then reads DATA once.
  Why v5 missed it: no v5 refusal had all of its bits from 3 up inside one of those ranges; all-ones sets every bit but
  never one alone.  **FIXED by session B** (section 4): every single-bit value 2^3.. at each width, refused after PORT=5,
  one PORT read per width.  Measured in table 6: the three narrowings, the control, all 61 one-bit narrowings (MKB_03 ..
  MKB_63) and four one-width narrowings (MKW_*).
* **V2 -- Opus's own denominator, corrected**: 8 equivalents (6 compile to the fix's own binary; `writeflag !=
  MEM_WRITE` and `warned_port != 1` build differently and behave the same), 5 behaviour changers, all red.  **Carried
  into table 6** (EQ_*, BR_*).
* **V3 -- CELL_rd_s0 is equivalent, and the header said every listed cell's edit is red while listing "every selector
  0-7" under the PORT read** (grok; Opus confirmed from table 5's logs).  A read that skips its load at selector 0 still
  returns 0 (`odata` starts at 0).  **FIXED**: the header now excepts it and NOT CLAIMED (4) names it.
* **V4 -- NOT CLAIMED (8) was false against session Y** (grok, glm, kimi-k3): Y reads COMMAND back under COMMAND 1 after
  its second refusal at previous 5, so "no cell is read back under COMMAND 1" and "port 5's is the only cell read back
  after a refusal at previous 5" were both false; and (8)'s held states omitted Z (every cell 0).  grok's detail: the
  SET_RESOLUTION between Y's refusals rewrites COMMAND, so only a write by the SECOND refusal is visible.  **FIXED** in
  (8) and in the cells-alone effect.
* **V5 -- "Effect 4" was a stale v4 cross-reference** (agy, kimi-k3): v5 has seven effects and cells-alone is the sixth.
  **FIXED**: named, not numbered.
* **V6 -- "lw (every session)" is false for K**, which never reads PORT (grok).  **FIXED**: "every session but K".
* **V7 -- "latch unset (each session's first refusal)" is false for Z** (grok): Z's first refusal is followed by an
  accepted PORT=0 before any read.  **FIXED**: the holders are listed (P, F, V, W, X2-X7, Y, B), and Z's and R's first
  refusals are named as never read back.
* **V8 -- "the later refusals are silent -- width sb (P)" omits V**, whose fourth refusal is 0xff by sb (minimax,
  kimi-k3).  **FIXED**: "sb (P, V, B)".
* **V9 -- equivalents missing from NOT CLAIMED (4)**: the accept store masked with 7 or cast to int (deepseek, grok;
  Opus measured both at the fix's own binary), and a latch set to any nonzero value (glm; agy's `warned_port++`).
  **FIXED** in (4); table 6 measures `EQ_acc_and7`, `EQ_acc_castint`, `EQL_latch2`.
* **V10 -- the announce's trailing newline is not checked** (agy).  **DISCLOSED** in (5); table 6 measures `DSC_nonl`.
* **V11 -- the re-announce period disclosure ("twelve or more") and the B_mod11 / B_mod12 counting convention**
  (kimi-k3).  **OVERTAKEN**: session B makes 108 refusals, so a latch re-armed every 12 now announces nine times there;
  (3) now reads "a latch that re-arms only after more refusals than any session makes (B makes 108)", and table 6
  predicts B_mod12 RED.
* **V12 -- an announce suppressed for a CLASS of values no first refusal belongs to** (raised by the bit-range finding:
  the first refusals are 8, 9, 0x100, 0x100000005 and all-ones, and only a session's first refusal announces).
  **DISCLOSED** in (3); table 6 measures `DSC_ann_hibits` (no announce for a value whose bits all lie above bit 8).
* **V13 -- "the one-axis edit of every listed cell is measured" was not checkable from the packet** (glm, kimi-k3); ten
  generated edits were textually identical to earlier ones and measured under the earlier names (Opus read CELLMAP and
  confirmed every listed cell red except CELL_rd_s0).  **FIXED**: the header points at `table5/CELLMAP.out` for the
  mapping; section 6 inlines the manifest lines for every full-score edit.
* **V14 -- the W session's width x value records conflict with the table-4 names T_W_sd7 and T_W_sw8** (glm).
  **REJECTED**: those names are EDITS of the cells "7 accepted by sd" and "8 refused by sw", held by A (7 by sd) and P
  (8 by sw); W's description is right.
* **V15 -- "0x8 (P, W)" in the first-announce effect vs no W name row** (minimax).  **REJECTED**: that list is the
  ANNOUNCE-ONCE effect (W's first refusal, 8 by sb, is counted there); the NAMING effect lists 0x8 (P) only.
* **V16 -- CELL_rd_s5's collateral was misdescribed** (Opus): sessions A and R end the process -- the misrouted read
  resets the selector to 0 and the next DATA write runs an unimplemented command, the command-default exit
  (out of scope, filed as `fbctrlcmdkill`).  **ACCEPTED** into the round record.
* **V17 -- the closing-F2 disposition's warrant "table 4 holds ... idata magnitude, width and class" is measured false
  for class** (Opus).  **ACCEPTED** into the round record; V1 is the measurement.
* **V18 -- the kill-table's gate comment counted "four equivalent edits" without a source** (glm).  **ACCEPTED**: the
  gate comment is re-derived from table 6's manifest (section 6).
* **V19 -- smaller wording**: the brief's quote of "the 101-row composite" (101 was table 4's edit count; the probe was
  94 rows) (glm, agy); the brief's manifest path (agy).  **ACCEPTED** as brief wording; neither is in the probe.
* **V20 -- rows not credited to every session that holds them** (kimi-k3: V's and Y's reads after a refusal hold "latch
  set").  **NO CHANGE**: the lists name holders, they do not claim to be exhaustive; nothing reads a missing holder as a
  gap.  (Its other item, R's first refusal as a first-announce holder, is not held: R samples the count only after its
  SECOND refusal.)

### WHERE I MIGHT BE FOOLING MYSELF

* **Session B's four rows are aggregates**: each reads PORT once per width, so it says that SOME single-bit value got
  through, not which.  Is a per-width aggregate enough, or does a width-and-bit joint edit exist that B cannot see?
* **B's count row makes a DIFFERENT class of edit red that was disclosed before** (B_mod12).  That is a record change
  ((3)) as much as a detector change; say if either text overclaims.
* The channel line in the pre-table addendum (`PRETABLE_ADDENDUM_t6.out`) was written before the table: section 6
  says whether every named edit went red on exactly the named rows.

## 4. SESSION B -- THE REPAIR (v6, inlined from the generated probe, md5 a9a2be3d)

The encoder gains one R-type instruction, `dsll rt,rt,sa`, pinned by two literal encodings and checked at run time
against the emulator's own disassembly of every stepped word:

```python
def ins(op, rt, off, base="t0"):
    if op == "dsll":                                     # SPECIAL dsll rt,rt,off: rd == rt, the shift in sa
        return (REG[rt] << 16) | (REG[rt] << 11) | ((off & 31) << 6) | 0x38
    return (OPS[op] << 26) | (REG[base] << 21) | (REG[rt] << 16) | (off & 0xffff)


def text(op, rt, off, base="t0"):
    if op == "dsll":
        return "dsll %s,%s,%d" % (rt, rt, off)
    return "%s %s,%d(%s)" % (op, rt, off, base)


ANCHOR = (0x0f << 26) | (REG["t7"] << 16)                   # lui t7,0 -- the breakpoint anchor, never executed
#  Pinned independently of the helper: a wrong register field would otherwise pass silently.
assert ins("sw", "t1", 0) == 0xad090000
assert ins("lw", "t2", 0x10) == 0x8d0a0010
assert ins("sd", "t5", 0) == 0xfd0d0000
assert ins("sb", "t8", 0) == 0xa1180000
assert ins("sh", "t9", 0) == 0xa5190000
assert ins("ld", "s3", 0) == 0xdd130000
assert ins("sb", "zr", 0) == 0xa1000000
assert ins("lb", "a1", 0) == 0x81050000
assert ins("lh", "a2", 0) == 0x85060000
assert ANCHOR == 0x3c0f0000
assert ins("dsll", "t1", 1) == 0x00094878
assert ins("dsll", "t4", 1) == 0x000c6078
```

The session and its rows:

```python
#  B: every single-bit value from 2^3 up that each width can carry, refused after PORT=5.  One register per width
#  starts at 8 and doubles after each store (dsll); PORT is read once per width, after all of that width's refusals
#  -- a refusal that let a value through would store it as an int (2^k, INT_MIN or 0, never 5), and the later
#  refusals of that width would keep it.  The count is sampled after the last of the 108 refusals.
B_GROUPS = [("sb", "t1", 8, "s0"), ("sh", "t2", 16, "s1"), ("sw", "t3", 32, "s2"), ("sd", "t4", 64, "s3")]
PROG_B, REGS_B = [], [("t0", FBCTRL), ("a0", 5)]
for _w, _r, _bits, _rb in B_GROUPS:
    REGS_B += [(_r, 8), (_rb, 0xdead)]
    PROG_B.append(("sw", "a0", 0, None))                               # PORT=5
    for _k in range(3, _bits):
        PROG_B += [(_w, _r, 0, None), ("dsll", _r, 1, None)]
    PROG_B.append(("lw", _rb, 0, None))
READS_B = [g[3] for g in B_GROUPS]
NB = sum(g[2] - 3 for g in B_GROUPS)
assert NB == 108
#  the tag goes on the LAST refusal (2^63 by sd), so the count is read after all of them
_last = max(i for i, s in enumerate(PROG_B) if s[0] in ("sb", "sh", "sw", "sd") and s[1] != "a0")
PROG_B[_last] = PROG_B[_last][:3] + ("blast",)

# ... in main(), after session Z:
#     B = session("B", PROG_B, REGS_B, READS_B, stub)
# ... and B joins the per-session disassembly CONTROL loop.

    print("SINGLE BITS (session B: %s %d/%d)" % (B["status"], B["steps"], B["n"]))
    for _w, _r, bits, rb in B_GROUPS:
        row("B refuse every single bit 2^3..2^%d (%s), PORT keeps 5" % (bits - 1, _w), hx(B["vals"].get(rb)),
            "0x5")
    row("B announce exactly 1 across its %d refusals" % NB, B["once_after"].get("blast"), 1)
```

On the fixed binary: `session B  SURVIVED  steps=224/224 exit=0 once=1`; the four width rows read 0x5; the count row
reads 1; B's disassembly row reads 0 mismatches.  v6 scores 117/117 (`table6/v6_fix.out`), 14 s wall for the whole
probe.

## 5. THE DIFFS

### 5a. regress/fbctrl_port_probe.py, v5 -> v6 (the whole diff: session B, the dsll encoder, and the record fixes)

```diff
--- regress/fbctrl_port_probe.py.v5
+++ regress/fbctrl_port_probe.py.v6
@@ -3,7 +3,8 @@
 
 machine_test.c installs `fbctrl addr=0x12f00000` in testmips's own setup (and in default_test() for the other test
 machines).  Every access below is a real guest sb/sh/sw/sd/lw/ld placed with `put w` and executed through real address
-decode and memory_rw -- stepped one instruction at a time, except session F, which free-runs to a breakpoint.  No machine
+decode and memory_rw -- stepped one instruction at a time, except session F, which free-runs to a breakpoint (session B
+also steps a `dsll` between its stores, to double its value register).  No machine
 or device is added to reach the site.  t0 = 0xffffffffb2f00000, kseg1 of DEV_FBCTRL_ADDRESS; PORT is +0x00, DATA +0x10.
 
 THE DEFECT (HEAD before #549): the PORT arm STORED the selector, as an int, with only a warning.  An int out of range --
@@ -50,39 +51,54 @@
      refusal, 0x100000003 by sd (3 as an int, never 5) -- PORT keeps 5 and the count is still 1; COMMAND reads back 1.
   Z  silence across selectors: PORT=2 and its FIRST refusal (9), then PORT=0, 1, 2, 3 and 4, each followed by a refusal
      of 9 -- the count is still 1 after all six, and PORT keeps 4.
+  B  single bits: PORT=5, then EVERY single-bit value from 2^3 up that the width can carry -- 2^3..2^7 by sb,
+     2^3..2^15 by sh, 2^3..2^31 by sw, 2^3..2^63 by sd, 108 refusals -- with PORT set to 5 again before each width
+     and read back once after it; a register doubles between stores (dsll).  A refusal that let one of them through
+     would store it as an int -- 2^k, INT_MIN or 0, never 5 -- and every later refusal of that width would keep it,
+     so one read per width sees it.  The count must be exactly 1 after all 108.  Added by the verifying pass (the
+     Opus 5.5 seat): the compare narrowed to ignore bits 5-7, 9-31 or 34-62 scored the full 111 rows, because no v5
+     refusal had all of its bits from 3 up inside one of those ranges.
 
 CONTRACT (clause e) -- AN ENUMERATION, NOT A LIST.
 THE FLOOR.  The fixed PORT arm's body tests three things -- the access direction, the written value (`idata >=
 DEV_FBCTRL_NPORTS`, on all 64 bits) and the latch (`!warned_port`) -- and it reads and writes `current_port`.  Every
-cell of those is held: the value's magnitude, width and class, the latch unset and set, a read and a write.  The
+cell of those is held: the value's magnitude, width and class, every bit the compare tests set alone at every width
+(B), the latch unset and set, a read and a write.  The
 previous selector (current_port's VALUE), the COMMAND cell and the data cells are NOT tested by the body -- the fix
 makes no partition of them -- so an edit conditioned on one of them is coverage beyond the floor (clause e): the rows
 hold the values listed below and claim nothing more.  For each EFFECT, each value listed is held by the session(s)
 named, and the one-axis edit of every listed cell is measured red in
-regress/artifacts/fbctrlportkill_20260924/table5/TABLE.out.  This is the class closure: pass 2, the F2 pass, the
-closing pass and the closing F2 pass each found such an edit on a value the rows had left empty.
-  a refusal keeps the previous selector -- width sb sh sw sd (P, W); previous 0 (F), 1 (V), 2 3 (X), 4 (X4, Z), 5 (P,
-      W, Y), 6 (W, X6), 7 (P, V, X7); COMMAND 0 (P), 1 (Y), 2 (V); latch unset (each session's first refusal) and set
-      (the rest)
+regress/artifacts/fbctrlportkill_20260924/table6/TABLE.out (under an earlier edit's name where the generated text
+was identical to it: table5/CELLMAP.out) -- except the read of selector 0, whose edit is EQUIVALENT (NOT CLAIMED
+(4)).  This is the class closure: pass 2, the F2 pass, the closing pass and the closing F2 pass each found such an
+edit on a value the rows had left empty, and the verifying pass found one on a range of bits (B).
+  a refusal keeps the previous selector -- width sb sh sw sd (P, W, B); previous 0 (F), 1 (V), 2 3 (X), 4 (X4, Z), 5
+      (P, W, Y, B), 6 (W, X6), 7 (P, V, X7); COMMAND 0 (P, B), 1 (Y), 2 (V); latch unset (the first refusal of P, F,
+      V, W, X2-X7, Y and B -- Z's and R's first refusals are never read back) and set (the rest)
   the first refusal announces once -- width sw (P, V, F, Y, Z) sb (W, X6) sh (X2, X7) sd (X3, X4); previous 0 (F), 1
       (V), 2 (X2, Z), 3 4 6 7 (X), 5 (P, W, Y); COMMAND 0 (P, F, W, X, Z), 1 (Y), 2 (V); the first-refused value from 8
       (P, W) to all-ones (X4)
-  the later refusals are silent -- width sb (P) sh (P, W) sw (P, V, W, R, Z) sd (P, V, W, Y); previous 0-4 (Z), 5 (P, W,
-      R, Y), 6 (W), 7 (P, V); COMMAND 0 (P, W, Z), 1 (Y), 2 (V, R); across PORT reads, a DATA write, a DATA read, a NOP
-      and a GET_RESOLUTION (R), a SET_RESOLUTION (Y), accepted selectors and twelve refusals (P)
+  the later refusals are silent -- width sb (P, V, B) sh (P, W, B) sw (P, V, W, R, Z, B) sd (P, V, W, Y, B); previous
+      0-4 (Z), 5 (P, W, R, Y, B), 6 (W), 7 (P, V); COMMAND 0 (P, W, Z, B), 1 (Y), 2 (V, R); across PORT reads, a DATA
+      write, a DATA read, a NOP and a GET_RESOLUTION (R), a SET_RESOLUTION (Y), accepted selectors, twelve refusals
+      (P) and 108 (B)
   the announce names the refused value -- 0x8 (P), 0x9 (F, V, X2, X6, Y), 0x100 (X7), the wide 0x100000005 (X3),
       all-ones (X4): width sw (P, F, V, Y) sb (X6) sh (X2, X7) sd (X3, X4); previous 0 (F), 1 (V), 2 3 4 6 7 (X), 5 (P,
       Y); COMMAND 0 (P, F, X), 1 (Y), 2 (V)
-  a PORT read returns the selector -- lb lh ld (W) and lw (every session); every selector 0-7 (A); COMMAND 0 (A), 1
-      (Y), 2 (V); latch unset (A) and set (P)
+  a PORT read returns the selector -- lb lh ld (W) and lw (every session but K); every selector 0-7 (A), though a
+      read of selector 0 cannot tell a skipped load from a real one (odata starts at 0: NOT CLAIMED (4)); COMMAND 0
+      (A), 1 (Y), 2 (V); latch unset (A) and set (P)
   a refusal leaves the cells alone -- all eight cells after refusals of 9, 16, 0x100000003 (sd), 0xff (sb) and 8 at
       previous selector 7 with COMMAND 2 (V); X1 after a refusal of 9 (sw) at previous 1 with COMMAND 2 (V); port 5's
-      cell after a refused 9 (sw) at previous 5 with COMMAND 0 (K) -- and no other cell, width, selector or COMMAND
-      value (NOT CLAIMED (8))
+      cell after a refused 9 (sw) at previous 5 with COMMAND 0 (K); COMMAND itself after a refused 0x100000003 (sd) at
+      previous 5 with COMMAND 1 (Y -- its second refusal only: the SET_RESOLUTION before it rewrites COMMAND, so a
+      write by the first refusal would be overwritten before the read) -- and no other cell, width, selector or
+      COMMAND value (NOT CLAIMED (8))
   an accepted selector is stored -- 0 and 7 at every width (W, A), every selector at one width (A); latch unset (A, W)
       and set (V's fills and Z's selections, after their first refusals)
 Beyond the effects: the store of an out-of-range value, clamped, masked or reset; the compare narrowed or signed (bit
-63 alone, bits 32-33, 32-bit truncation); a boundary slip at 8; an announce on an accepted selector; an announce
+63 alone, bits 32-33, 32-bit truncation) or made to ignore any set of the bits it tests, at any width (B: every
+single-bit value is refused); a boundary slip at 8; an announce on an accepted selector; an announce
 demoted to debug() (F); an announce suppressed above or below any threshold, or on the sign bit (the first refusals
 run from 8 to all-ones); and the pre-#549 process exit on DATA.
 NOT CLAIMED (disclosed).  (0) An edit conditioned on TWO axes at once -- a joint cell such as "refuse 9 only by sb after
@@ -99,28 +115,37 @@
 `exit(1)`, weakening `>=` to `>`, or swapping its operand -- is unreachable while the PORT arm refuses, because no
 out-of-range selector is ever stored; the check is KEPT as a tripwire.  It exits before it indexes, so an index of 8
 cannot reach `warned_port` while it stands, and `port[8]` would be undefined behaviour, not a defined alias of the
-latch.  (3) An exception for one value no row writes (`idata != 10`), a re-announce period of twelve or more, an
-announce suppressed or mangled only for one value no session refuses first (`idata != 16`), and an announce demoted to
-debug() for some values but not F's 9 -- only a free-running session tells debug() from fatal() here, and F is the
-only one: the value space is 2^64, and no finite row set closes "except value k".  (A threshold is not in this class;
-see "Beyond the effects".)  (4) Equivalent edits: storing `(uint32_t) idata` (it compiles to the fix's own binary),
-reordering the struct's fields, masking the PORT read with 7 (the selector is always 0..7).  (5) `printf` in place of
-`fatal()`: indistinguishable in THIS invocation's output.  (6) Narrowing the DATA path's widths, and the device's OTHER
+latch.  (3) An exception for one value no row writes (`idata != 10`), a latch that re-arms only after more refusals than
+any session makes (B makes 108), an announce suppressed or mangled only for one value no session refuses first
+(`idata != 16`) or only for a CLASS of values no first refusal belongs to (values whose bits all lie in 9..31, say:
+the first refusals are 8, 9, 0x100, 0x100000005 and all-ones, and the latch lets only a session's first refusal
+announce), and an announce demoted to debug() for some values but not F's 9 -- only a free-running session tells
+debug() from fatal() here, and F is the only one: the value space is 2^64, and no finite row set closes "except
+value k".  (A threshold is not in this class, nor is a range of bits the COMPARE ignores: see "Beyond the
+effects".)  (4) Equivalent edits: storing `(uint32_t) idata`, `(int) idata` or `idata & 7` (only 0..7 reach that
+store, and each compiles to the fix's own binary), reordering the struct's fields, masking the PORT read with 7
+(the selector is always 0..7), a PORT read that skips its load at selector 0 (odata starts at 0), and a latch set
+to any nonzero value in place of 1.  (5) `printf` in place of `fatal()`, or the announce without its trailing
+newline: indistinguishable in THIS invocation's output.  (6) Narrowing the DATA path's widths, and the device's OTHER
 two process-ending calls -- fbctrl_command()'s default (any command other than 0-2, including the documented but
 unimplemented FILL/COPY) and the access function's default (any offset other than 0x00/0x10): filed as `fbctrlcmdkill`
 and `fbctrloffkill`.  (7) Edits to this instrument's own logic are reviewed, not rowed.  (8) The data cells' VALUES are
 not an axis the rows enumerate.  An edit conditioned on a cell's value (`port[COLOR_B] == 0`, `port[Y1] != 0`) is
-caught only where a row's refusal or read holds a triggering state, and the states held are: every cell 0 (F, W, X),
+caught only where a row's refusal or read holds a triggering state, and the states held are: every cell 0 (F, W, X,
+Z, B),
 port 5 at 0x2a (P, K, R), X1 at 123 with COMMAND 2 (V's first refusal), ports 1-7 at 0x11*p with COMMAND 2 (V's later
-refusals and the PORT read right after them), and COMMAND 1 (Y).  Effect 4 is claimed only as listed: no cell is read
-back after an `sh` refusal, after a refusal at previous selector 0, 2, 3, 4 or 6, or under COMMAND 1, and port 5's is
-the only cell read back after a refusal at previous 5 or under COMMAND 0.
+refusals and the PORT read right after them), and COMMAND 1 (Y).  The cells-alone effect is claimed only as listed:
+no cell is read back after an `sh` refusal or after a refusal at previous selector 0, 2, 3, 4 or 6, and after a
+refusal at previous 5 the only cells read back are port 5's under COMMAND 0 (K) and COMMAND's under COMMAND 1 (Y,
+its second refusal only).
 LIMITS OF A ROW.  Session P re-selects PORT=5 before each refusal, so a refused selector cannot carry over into the next
 row WHEN THE LEGAL SELECTION LANDS; an edit that also refuses legal selections defeats the re-select, and later rows
 then inherit its value (M_acclatch).  Every read-back is taken after its session ends, so a session that dies part-way
 blanks the rows it had already passed (M_acc4: session A died at step 5 and every accept row read `-`).  And session A's
 "accept selector 0 written by sw" cannot see an IGNORED store -- the selector is already 0 at power-on -- so the cell
-"0 by sw is accepted" is held by W's row after PORT=5, not by A's.
+"0 by sw is accepted" is held by W's row after PORT=5, not by A's.  Session B reads PORT once per width, so each of
+its rows says that SOME single-bit value of that width got through, not which: the row prints the last one's stored
+int.
 
 Every stepped word is compared with the emulator's own step line (the hand-assembled-encoding trap).
 Output: one row per check, then FBCTRLP_CONTROL=OK|FAILED, FBCTRLP_RESULT=n/t, FBCTRLP_DONE.  The exit status is 0
@@ -152,10 +177,14 @@
 
 
 def ins(op, rt, off, base="t0"):
+    if op == "dsll":                                     # SPECIAL dsll rt,rt,off: rd == rt, the shift in sa
+        return (REG[rt] << 16) | (REG[rt] << 11) | ((off & 31) << 6) | 0x38
     return (OPS[op] << 26) | (REG[base] << 21) | (REG[rt] << 16) | (off & 0xffff)
 
 
 def text(op, rt, off, base="t0"):
+    if op == "dsll":
+        return "dsll %s,%s,%d" % (rt, rt, off)
     return "%s %s,%d(%s)" % (op, rt, off, base)
 
 
@@ -171,6 +200,8 @@
 assert ins("lb", "a1", 0) == 0x81050000
 assert ins("lh", "a2", 0) == 0x85060000
 assert ANCHOR == 0x3c0f0000
+assert ins("dsll", "t1", 1) == 0x00094878
+assert ins("dsll", "t4", 1) == 0x000c6078
 
 
 def stub_path():
@@ -490,6 +521,26 @@
            ("X7", 7, "sh", 0x100)]
 
 
+#  B: every single-bit value from 2^3 up that each width can carry, refused after PORT=5.  One register per width
+#  starts at 8 and doubles after each store (dsll); PORT is read once per width, after all of that width's refusals
+#  -- a refusal that let a value through would store it as an int (2^k, INT_MIN or 0, never 5), and the later
+#  refusals of that width would keep it.  The count is sampled after the last of the 108 refusals.
+B_GROUPS = [("sb", "t1", 8, "s0"), ("sh", "t2", 16, "s1"), ("sw", "t3", 32, "s2"), ("sd", "t4", 64, "s3")]
+PROG_B, REGS_B = [], [("t0", FBCTRL), ("a0", 5)]
+for _w, _r, _bits, _rb in B_GROUPS:
+    REGS_B += [(_r, 8), (_rb, 0xdead)]
+    PROG_B.append(("sw", "a0", 0, None))                               # PORT=5
+    for _k in range(3, _bits):
+        PROG_B += [(_w, _r, 0, None), ("dsll", _r, 1, None)]
+    PROG_B.append(("lw", _rb, 0, None))
+READS_B = [g[3] for g in B_GROUPS]
+NB = sum(g[2] - 3 for g in B_GROUPS)
+assert NB == 108
+#  the tag goes on the LAST refusal (2^63 by sd), so the count is read after all of them
+_last = max(i for i, s in enumerate(PROG_B) if s[0] in ("sb", "sh", "sw", "sd") and s[1] != "a0")
+PROG_B[_last] = PROG_B[_last][:3] + ("blast",)
+
+
 def prog_x(k, w, v):
     return ([("sw", "a0", 0, None), (w, "t1", 0, "x"), ("lw", "s0", 0, None)],
             [("t0", FBCTRL), ("a0", k), ("t1", v), ("s0", 0xdead)])
@@ -508,6 +559,7 @@
         W = session("W", PROG_W, REGS_W, READS_W, stub)
         Y = session("Y", PROG_Y, REGS_Y, ["s0", "s1", "s2"], stub)
         Z = session("Z", PROG_Z, REGS_Z, ["s0"], stub)
+        B = session("B", PROG_B, REGS_B, READS_B, stub)
         X = []
         for lab, k, w, v in X_CELLS:
             prog, regs = prog_x(k, w, v)
@@ -529,7 +581,7 @@
     ctl.append(row("C SIGNATURE: Y1 zeroed by GET_RESOLUTION", hx(C["vals"].get("s3")), "0x0",
                    "(prefilled 123)"))
     row("C nothing refused, no (once) line", len(ONCE_RE.findall(C["buf"])), 0)
-    for lab, S in (("A", A), ("P", P), ("R", R), ("K", K), ("V", V), ("W", W), ("Y", Y), ("Z", Z)):
+    for lab, S in (("A", A), ("P", P), ("R", R), ("K", K), ("V", V), ("W", W), ("Y", Y), ("Z", Z), ("B", B)):
         ctl.append(row("%s disassembly of every stepped word" % lab, len(S["badis"]), 0))
     ctl.append(row("X2-X7 disassembly of every stepped word", sum(len(S["badis"]) for S in X), 0))
     print("ACCEPT (session A: %s %d/%d)" % (A["status"], A["steps"], A["n"]))
@@ -590,6 +642,11 @@
     row("Z the first refusal (after PORT=2) announces", Z["once_after"].get("z1st"), 1)
     row("Z announce still exactly 1 after refusals at selectors 0-4", Z["once_after"].get("zlast"), 1)
     row("Z PORT keeps 4 after its refusals", hx(Z["vals"].get("s0")), "0x4")
+    print("SINGLE BITS (session B: %s %d/%d)" % (B["status"], B["steps"], B["n"]))
+    for _w, _r, bits, rb in B_GROUPS:
+        row("B refuse every single bit 2^3..2^%d (%s), PORT keeps 5" % (bits - 1, _w), hx(B["vals"].get(rb)),
+            "0x5")
+    row("B announce exactly 1 across its %d refusals" % NB, B["once_after"].get("blast"), 1)
     print("FIRST REFUSALS (sessions X2-X7: %s)" % " ".join("%s %d/%d" % (S["status"], S["steps"], S["n"])
                                                           for S in X))
     for (lab, k, w, v), S in zip(X_CELLS, X):
```

### 5b. regress/gate_mips_folds.sh (the pin and the comment)

```diff
--- regress/gate_mips_folds.sh.v5
+++ regress/gate_mips_folds.sh.v6
@@ -43,18 +43,25 @@
 #  this gate's pmax-kernel check: a missing kernel still skips the fold rows below, and
 #  gate_skip reports FAIL, not SKIP, if an fbctrl row failed first.
 #
-#  THE CONTRACT is the probe's header (its ENUMERATION and NOT CLAIMED).  Kill table 5
-#  (regress/artifacts/fbctrlportkill_20260924/table5/TABLE.out) built 212 edits -- table 4's
-#  101, one one-axis edit GENERATED for every cell the header lists (table5/CELLMAP.out), and
-#  the closing-F2 seats' edits -- each with its prediction written first (table5/MANIFEST.out):
-#  the 192 the contract does not disclose are ALL red, HEAD's own arm among them (M_revert,
-#  53/111 here, and sessions K and R ended the process); the 20 it discloses score 111/111 --
-#  a process-global latch, a serial-number condition, three edits of the DATA arm's kept check,
-#  two joint cells, one value no row writes, a re-announce period of twelve, four equivalent
-#  edits, two DATA-width edits, three refusal-time cell writes no row reads back, and two
-#  announce forms keyed to one value or a value range.  Every prediction held.  The device
-#  still ends the process through its command and offset defaults, which are filed, not
-#  claimed.
+#  THE CONTRACT is the probe's header (its ENUMERATION and NOT CLAIMED).  Variant table 6
+#  (regress/artifacts/fbctrlportkill_20260924/table6/TABLE.out) built 297 edits -- table 5's
+#  212 (one one-axis edit GENERATED for every cell the header lists, table5/CELLMAP.out), the
+#  verifying pass's equivalents and behaviour changers, its three bit-range narrowings of the
+#  compare and their control, a one-bit narrowing for EVERY bit 3-63, four one-width
+#  narrowings, and three measured disclosures -- each with its prediction written first
+#  (table6/MANIFEST.out): the 267 the contract does not disclose are ALL red, HEAD's own arm
+#  among them (M_revert, 54/117 here, and sessions K and R ended the process); the 30 it
+#  discloses score 117/117 -- a process-global latch, a serial-number condition, three edits of
+#  the DATA arm's kept check, two joint cells, one value no row writes, thirteen equivalent
+#  edits, two DATA-width edits, three refusal-time cell writes no row reads back, three announce
+#  forms keyed to one value, a value range or a value class no first refusal belongs to, and the
+#  announce without its trailing newline.  Every prediction held, and every one-bit and
+#  one-width narrowing reddened exactly the session-B width rows the pre-table addendum named
+#  (PRETABLE_ADDENDUM_t6.out).  Session B -- every single-bit value at each width -- is v6's
+#  repair of a floor breach the verifying pass MEASURED: the compare narrowed to ignore bits 9-31
+#  scored the full 111 rows of v5 and brought back the DATA arm's exit
+#  (opus549_measured/c3/TABLE_mask.out).  The device still ends the process through its command
+#  and offset defaults, which are filed, not claimed.
 #
 #  `gatedevicesplit` is OWED (#498): one more device probe in a CPU gate, as #548 added to
 #  gate 14.  Recorded, not compounded silently.
@@ -81,8 +88,8 @@
     #  quoted numerator is inert to that tool BY DESIGN -- it reads only the denominator's
     #  line -- and the exit row above and the two reconciliation rows below are what catch a
     #  red or an edited score.
-    check "fbctrl_port rows run" "${fbres#*/}" 111
-    check "fbctrl_port rows correct" "${fbres%/*}" "111"
+    check "fbctrl_port rows run" "${fbres#*/}" 117
+    check "fbctrl_port rows correct" "${fbres%/*}" "117"
     check "fbctrl_port rows failed" "$(grep -c '^  FAIL ' "$FBCLOG")" "0"
     #  RECONCILE the rows the probe PRINTED with the trailer it printed (#549 F2, measured by
     #  the Opus seat): checking the trailer alone, a log with one row deleted and its
```

## 6. MEASURED -- VARIANT TABLE 6 (`regress/artifacts/fbctrlportkill_20260924/table6/TABLE.out`)

Each edit is one text change of the FINAL fixed `dev_fbctrl.c`, built in a scratch clone of the build tree and scored
by a frozen copy of the v6 probe.  Its prediction was written BEFORE the run (`table6/MANIFEST.out`, and
`PRETABLE_ADDENDUM_t6.out` for the reasoning; the addendum's mtime is earlier than the table's first line).

```
#549 variant table 6 -- started 2026-09-25 18:00:14
probe md5 a9a2be3d  mutants549_t6 md5 509bf090  edits 297
base: fix build md5 b5b99e6d  build/gxemul md5 b5b99e6d  18:00:20
base_fix rc=0 FBCTRLP_RESULT=117/117 FBCTRLP_CONTROL=OK FBCTRLP_DONE
...
restored: cmp SEC clean, binary fresh, md5 == base; sentinel cleared
probe source unchanged during the run
TABLE6_DONE 19:20:19
```

**297 edits scored; 267 red, 30 at the full 117; predictions that did not hold: NONE.**

Every edit v6 added to the table, and B_mod12 (disclosed in table 5, now reached by session B), with the rows it
turned red:

```
BR_acc_map0      rc=1 109/117 FAILED | C SIGNATURE: X1 zeroed by GET_RESOLUTION;C SIGNATURE: Y1 zeroed by GET_RESOLUTION;accept selector 0 written by sw;V port 0 (COMMAND) still 2 after five refusals;accept 0 written by sb after PORT=5;accept 0 written by sh after PORT=5;accept 0 written by sw after PORT=5;accept 0 written by sd after PORT=5;
BR_ann_gt8       rc=1 114/117 OK | announce: exactly 1 right after the FIRST refusal;announce names the first refused value, 0x8;W the first refusal (8 by sb) announces;
BR_ge9           rc=1 105/117 OK | refuse 8 (sw), PORT keeps 5;announce: exactly 1 right after the FIRST refusal;announce names the first refused value, 0x8;V PORT keeps 7 after its later refusals;refuse 8 (sb), PORT keeps 5;refuse 8 (sh), PORT keeps 5;refuse 8 (sd), PORT keeps 5;W the first refusal (8 by sb) announces;B refuse every single bit 2^3..2^7 (sb), PORT keeps 5;B refuse every single bit 2^3..2^15 (sh), PORT keeps 5;B refuse every single bit 2^3..2^31 (sw), PORT keeps 5;B refuse every single bit 2^3..2^63 (sd), PORT keeps 5;
BR_no_hi32       rc=1 104/117 OK | refuse 0x200000000 (sd), PORT keeps 5;refuse 0x100000003 (sd), PORT keeps 5;refuse all-ones (sd), PORT keeps 5;V PORT keeps 7 after its later refusals;refuse 0x8000000000000000 (sd), PORT keeps 5;Y refuse 0x100000003 (sd) after SET_RESOLUTION, PORT keeps 5;B refuse every single bit 2^3..2^63 (sd), PORT keeps 5;X3 refuse 0x100000005 (sd) after PORT=3, PORT keeps 3;X3 that FIRST refusal announces exactly once;X3 the announce names the refused value 0x100000005;X4 refuse 0xffffffffffffffff (sd) after PORT=4, PORT keeps 4;X4 that FIRST refusal announces exactly once;X4 the announce names the refused value 0xffffffffffffffff;
BR_rd_drop0      rc=1 79/117 FAILED | C LIVENESS: PORT reads back 5;accept selector 1 written by sb;accept selector 3 written by sw;accept selector 5 written by sb;accept selector 7 written by sd;refuse 8 (sw), PORT keeps 5;refuse 9 (sw), PORT keeps 5;refuse 16 (sw), PORT keeps 5;refuse 0x200000000 (sd), PORT keeps 5;refuse 0x100000003 (sd), PORT keeps 5;refuse all-ones (sd), PORT keeps 5;refuse all-ones (sw), PORT keeps 5;refuse 0xff (sb), PORT keeps 5;refuse 0x100 (sh), PORT keeps 5;refuse 16 (sb), PORT keeps 5;refuse 16 (sh), PORT keeps 5;refuse 9 after PORT=7, PORT keeps 7;R refuse 9 after that traffic, PORT keeps 5;V refuse 9 while COMMAND holds 2, PORT keeps 1;V PORT keeps 7 after its later refusals;accept 7 written by sb after PORT=5;accept 7 written by sh after PORT=5;accept 7 written by sw after PORT=5;refuse 8 (sb), PORT keeps 5;refuse 8 (sh), PORT keeps 5;refuse 8 (sd), PORT keeps 5;refuse 0x8000000000000000 (sd), PORT keeps 5;ld of PORT reads exactly 5;lb of PORT reads exactly 5;lh of PORT reads exactly 5;Y refuse 9 while COMMAND holds 1, PORT keeps 5;Y refuse 0x100000003 (sd) after SET_RESOLUTION, PORT keeps 5;B refuse every single bit 2^3..2^7 (sb), PORT keeps 5;B refuse every single bit 2^3..2^15 (sh), PORT keeps 5;B refuse every single bit 2^3..2^31 (sw), PORT keeps 5;B refuse every single bit 2^3..2^63 (sd), PORT keeps 5;X3 refuse 0x100000005 (sd) after PORT=3, PORT keeps 3;X7 refuse 0x100 (sh) after PORT=7, PORT keeps 7;
BR_refuse_lt     rc=1 106/117 OK | accept selector 7 written by sd;port 6 round-trips its DATA value;A nothing refused, no (once) line;refuse 9 after PORT=7, PORT keeps 7;V PORT keeps 7 after its later refusals;V port 6 keeps its fill after five refusals;accept 7 written by sb after PORT=5;accept 7 written by sh after PORT=5;accept 7 written by sw after PORT=5;X7 refuse 0x100 (sh) after PORT=7, PORT keeps 7;X7 the announce names the refused value 0x100;
B_mod12          rc=1 116/117 OK | B announce exactly 1 across its 108 refusals;
DSC_ann_hibits   rc=0 117/117 OK | 
DSC_nonl         rc=0 117/117 OK | 
EQL_latch2       rc=0 117/117 OK | 
EQ_acc_and7      rc=0 117/117 OK | 
EQ_acc_castint   rc=0 117/117 OK | 
EQ_ann_idata     rc=0 117/117 OK | 
EQ_dir_new       rc=0 117/117 OK | 
EQ_ge8lit        rc=0 117/117 OK | 
EQ_gt7           rc=0 117/117 OK | 
EQ_latch_ne1     rc=0 117/117 OK | 
EQ_maskhi        rc=0 117/117 OK | 
MKB_03     bit  3  79/117  B rows red: sb,sh,sw,sd  (predicted sb,sh,sw,sd)  other rows red: 34
MKB_04     bit  4  109/117  B rows red: sb,sh,sw,sd  (predicted sb,sh,sw,sd)  other rows red: 4
MKB_05     bit  5  113/117  B rows red: sb,sh,sw,sd  (predicted sb,sh,sw,sd)  other rows red: 0
MKB_06     bit  6  113/117  B rows red: sb,sh,sw,sd  (predicted sb,sh,sw,sd)  other rows red: 0
MKB_07     bit  7  113/117  B rows red: sb,sh,sw,sd  (predicted sb,sh,sw,sd)  other rows red: 0
MKB_09     bit  9  114/117  B rows red: sh,sw,sd     (predicted sh,sw,sd)  other rows red: 0
MKB_10     bit 10  114/117  B rows red: sh,sw,sd     (predicted sh,sw,sd)  other rows red: 0
MKB_11     bit 11  114/117  B rows red: sh,sw,sd     (predicted sh,sw,sd)  other rows red: 0
MKB_12     bit 12  114/117  B rows red: sh,sw,sd     (predicted sh,sw,sd)  other rows red: 0
MKB_13     bit 13  114/117  B rows red: sh,sw,sd     (predicted sh,sw,sd)  other rows red: 0
MKB_14     bit 14  114/117  B rows red: sh,sw,sd     (predicted sh,sw,sd)  other rows red: 0
MKB_15     bit 15  114/117  B rows red: sh,sw,sd     (predicted sh,sw,sd)  other rows red: 0
MKB_16     bit 16  115/117  B rows red: sw,sd        (predicted sw,sd)  other rows red: 0
MKB_17     bit 17  115/117  B rows red: sw,sd        (predicted sw,sd)  other rows red: 0
MKB_18     bit 18  115/117  B rows red: sw,sd        (predicted sw,sd)  other rows red: 0
MKB_19     bit 19  115/117  B rows red: sw,sd        (predicted sw,sd)  other rows red: 0
MKB_20     bit 20  115/117  B rows red: sw,sd        (predicted sw,sd)  other rows red: 0
MKB_21     bit 21  115/117  B rows red: sw,sd        (predicted sw,sd)  other rows red: 0
MKB_22     bit 22  115/117  B rows red: sw,sd        (predicted sw,sd)  other rows red: 0
MKB_23     bit 23  115/117  B rows red: sw,sd        (predicted sw,sd)  other rows red: 0
MKB_24     bit 24  115/117  B rows red: sw,sd        (predicted sw,sd)  other rows red: 0
MKB_25     bit 25  115/117  B rows red: sw,sd        (predicted sw,sd)  other rows red: 0
MKB_26     bit 26  115/117  B rows red: sw,sd        (predicted sw,sd)  other rows red: 0
MKB_27     bit 27  115/117  B rows red: sw,sd        (predicted sw,sd)  other rows red: 0
MKB_28     bit 28  115/117  B rows red: sw,sd        (predicted sw,sd)  other rows red: 0
MKB_29     bit 29  115/117  B rows red: sw,sd        (predicted sw,sd)  other rows red: 0
MKB_30     bit 30  115/117  B rows red: sw,sd        (predicted sw,sd)  other rows red: 0
MKB_31     bit 31  115/117  B rows red: sw,sd        (predicted sw,sd)  other rows red: 0
MKB_32     bit 32  110/117  B rows red: sd           (predicted sd)  other rows red: 6
MKB_33     bit 33  115/117  B rows red: sd           (predicted sd)  other rows red: 1
MKB_34     bit 34  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_35     bit 35  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_36     bit 36  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_37     bit 37  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_38     bit 38  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_39     bit 39  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_40     bit 40  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_41     bit 41  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_42     bit 42  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_43     bit 43  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_44     bit 44  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_45     bit 45  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_46     bit 46  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_47     bit 47  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_48     bit 48  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_49     bit 49  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_50     bit 50  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_51     bit 51  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_52     bit 52  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_53     bit 53  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_54     bit 54  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_55     bit 55  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_56     bit 56  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_57     bit 57  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_58     bit 58  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_59     bit 59  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_60     bit 60  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_61     bit 61  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_62     bit 62  116/117  B rows red: sd           (predicted sd)  other rows red: 0
MKB_63     bit 63  115/117  B rows red: sd           (predicted sd)  other rows red: 1
MKW_sb05         rc=1 116/117 OK | B refuse every single bit 2^3..2^7 (sb), PORT keeps 5;
MKW_sd40         rc=1 116/117 OK | B refuse every single bit 2^3..2^63 (sd), PORT keeps 5;
MKW_sh12         rc=1 116/117 OK | B refuse every single bit 2^3..2^15 (sh), PORT keeps 5;
MKW_sw09         rc=1 116/117 OK | B refuse every single bit 2^3..2^31 (sw), PORT keeps 5;
MK_b34_62        rc=1 116/117 OK | B refuse every single bit 2^3..2^63 (sd), PORT keeps 5;
MK_b5_7          rc=1 113/117 OK | B refuse every single bit 2^3..2^7 (sb), PORT keeps 5;B refuse every single bit 2^3..2^15 (sh), PORT keeps 5;B refuse every single bit 2^3..2^31 (sw), PORT keeps 5;B refuse every single bit 2^3..2^63 (sd), PORT keeps 5;
MK_b8_ctl  bit  8  110/117  B rows red: sh,sw,sd     (predicted sh,sw,sd)  other rows red: 4
MK_b9_31         rc=1 114/117 OK | B refuse every single bit 2^3..2^15 (sh), PORT keeps 5;B refuse every single bit 2^3..2^31 (sw), PORT keeps 5;B refuse every single bit 2^3..2^63 (sd), PORT keeps 5;
CHANNEL CHECK: every one-bit edit red on exactly the predicted session-B width rows
```

Every edit at the full score, with its written prediction and the reason the contract gives:

```
A1_not10         GREEN(e)  table 5: rc=0
A2_sb3           GREEN(e)  table 5: rc=0
CELL_rd_s0       GREEN(eq) table 5: rc=0
CF2_DM_ge16      GREEN(e)  table 5: rc=0
CF2_KM_not16     GREEN(e)  table 5: rc=0
CF2_O_cl_c0      GREEN(e)  table 5: rc=0
CF2_O_cl_len2    GREEN(e)  table 5: rc=0
CF2_O_cl_p5      GREEN(e)  table 5: rc=0
DSC_ann_hibits   GREEN(e)  (e, NOT CLAIMED (3)): no announce for a value whose bits all lie above bit 8
DSC_nonl         GREEN(e)  (e, NOT CLAIMED (5)): the announce without its trailing newline
EQL_latch2       GREEN(eq) (eq, NOT CLAIMED (4)): the latch set to 2
EQ_acc_and7      GREEN(eq) c3 equivalent: accept stores idata & 7
EQ_acc_castint   GREEN(eq) c3 equivalent: accept stores (int) idata
EQ_ann_idata     GREEN(eq) c3 equivalent: latch test also requires idata (never 0 there)
EQ_dir_new       GREEN(eq) c3 equivalent: direction writeflag != MEM_WRITE
EQ_ge8lit        GREEN(eq) c3 equivalent: bound idata >= 8, the literal
EQ_gt7           GREEN(eq) c3 equivalent: bound idata > 7
EQ_latch_ne1     GREEN(eq) c3 equivalent: latch test warned_port != 1
EQ_maskhi        GREEN(eq) c3 equivalent: bound (idata & ~7ULL) nonzero
G5a_noexit       GREEN(e)  table 5: rc=0
G5b_checkop      GREEN(e)  table 5: rc=0
G7_ldbit32       GREEN(e)  table 5: rc=0
M_noguard        GREEN(e)  table 5: rc=0
M_static         GREEN(e)  table 5: rc=0
N_acc32          GREEN(e)  table 5: rc=0
N_datard16       GREEN(e)  table 5: rc=0
N_datawr8        GREEN(e)  table 5: rc=0
N_order          GREEN(e)  table 5: rc=0
N_rdmask7        GREEN(e)  table 5: rc=0
T_D9c_serial1    GREEN(e)  table 5: rc=0
```

## 7. QUESTIONS

1. **The floor question, asked of the SHIPPED COMPOSITE (the fix plus v6), not only of the v5->v6 diff:** is there an
   edit of the fixed PORT arm, outside NOT CLAIMED (0)-(8), that scores the full 117?  Name it and the rows that stay
   green.  **A zero needs its denominator** -- the shapes you tried.
2. **Is session B's aggregate reading enough?**  Each width row reads PORT once, after all of that width's refusals.
   Is there a narrowing -- by width, by bit, by the previous selector, by the latch -- that B cannot see and no other
   row sees?
3. **Adjudicate V1-V20**: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each.  If you raised a finding, be HARDER
   on v6's fix for it than on anyone else's.
4. **Which of v6's header sentences is false** -- the SESSIONS text for B, the enumeration's new holders, NOT CLAIMED
   (3), (4), (5), (8), LIMITS OF A ROW?
5. **Did every edit the pre-table addendum named go red on exactly the rows it named** (section 6 against
   `PRETABLE_ADDENDUM_t6.out`, section 4)?  A channel that was wrong is a finding.
6. **What did all of us miss?**

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
