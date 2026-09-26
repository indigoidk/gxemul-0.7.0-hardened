# #549 v6 -- THE ADJUDICATION PASS: every seat's findings on v6, shared, for the panel to adjudicate

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  A seat that re-derives a premise from something this brief did NOT give it is worth more
than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/`.**  Three pristine-2021-upstream copies of GXemul sit under the project root
(`./src/` and two under `_archive/`); they are NOT this fork.  The working tree's `regress/fbctrl_port_probe.py` IS v6
(117 rows, 16 sessions) and gate 16 pins 117.  The fix, `src/devices/dev_fbctrl.c`, has not changed since pass 2.

**If you cannot read files that is expected** -- every fact you need is inlined below.  Name any premise you cannot
settle from this packet rather than guessing at it.  Where a claim is ARITHMETIC, enumerate it.

**VERDICT LINE FIRST:** `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>` -- SHIP: v6 closes the repair chain with
wording and records fixes only; SHIP WITH CHANGES: a change to the probe's ROWS is owed (name it); DO NOT SHIP: the fix
itself is wrong.  Then numbered findings.

## 1. WHAT THIS PASS IS

v6's own pass fired every seat.  Their answers are consolidated in section 8 as N1..N24, each with MY disposition.
This pass SHARES them: each seat now sees what the other seats found, and adjudicates.  The flagship adjudication
follows this pass, and a second adjudicator confirms before anything is committed.

The repair chain's stop condition: it closes on the first VALID pass that finds zero floor breaches surviving
adjudication, carried with its denominator (the shapes tried).  Two floor questions are open, so this pass decides
whether v6 closes the chain or a v7 is owed.

## 2. THE DISAGREEMENTS

* **D1 = N1 (latch-unset x bit).**  The dedicated grok job: a FLOOR cell -- the refusal body reads `warned_port`, so
  its clear state is a body-read state lvalue, and the joint-cell rule's generating set ("at each floor cell, every
  idata bit the guarded body TESTS is written both clear and set") is incomplete at latch-clear: only bits 3, 8 and 32
  are held alone there.  agy, glm and the Opus fallback text: a two-axis joint, disclosed by NOT CLAIMED (0), with
  the DATA arm's kept range check as the tripwire.  The seats' own words are in N1, N5 and N14.
* **D2 = N21 (a refusal that writes the constant 5).**  Raised by the panel grok alone, in this same pass, so no
  other seat has addressed it: every value only session B stores is refused at previous selector 5, so a refuse-path
  write of 5 reads back exactly like "kept 5".  Is it one-axis and outside (0)-(8)?  Does ONE second anchor (a width
  group selecting 7 before its stores) close it, or move it to a constant equal to the new anchor on the bits only
  that width carries?

## 3. QUESTIONS

1. **Adjudicate N1..N24 and D1, D2** -- UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with a reason.
2. **WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?**  I accepted every wording and records finding raised -- about
   eighteen in a row.  That is a suspicious number, and agreement is not evidence.
3. **WHAT DID ALL OF US MISS?**  You now have the whole panel's output.

**Self-review, disclosed:** grok raised D1 (the dedicated job) and D2 (the panel seat).  If you are grok, be HARDER
on those two than on anyone else's finding, and check that the REPAIR each implies is right -- that it terminates,
and that it does not open the mirror cell -- not only that the gap exists.

## 4. SETTLED PREMISES (re-inlined from the v6 pass brief; each checked against the tree)

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
  `FBCTRLP_RESULT=n/t`, `FBCTRLP_CONTROL=OK`, exit 0, `t` pinned at 117, `n == t`, no FAIL lines,
  the printed rows reconciled with the trailer, and every row name printed once.

## 5. THE PROBE'S OWN HEADER, VERBATIM (`regress/fbctrl_port_probe.py`, v6): SESSIONS, THE CONTRACT, NOT CLAIMED (0)-(8), LIMITS

```
#549 fbctrlportkill -- the DETECTOR for dev_fbctrl.c's port selector, on an UNMODIFIED `-E testmips`.

machine_test.c installs `fbctrl addr=0x12f00000` in testmips's own setup (and in default_test() for the other test
machines).  Every access below is a real guest sb/sh/sw/sd/lw/ld placed with `put w` and executed through real address
decode and memory_rw -- stepped one instruction at a time, except session F, which free-runs to a breakpoint (session B
also steps a `dsll` between its stores, to double its value register).  No machine
or device is added to reach the site.  t0 = 0xffffffffb2f00000, kseg1 of DEV_FBCTRL_ADDRESS; PORT is +0x00, DATA +0x10.

THE DEFECT (HEAD before #549): the PORT arm STORED the selector, as an int, with only a warning.  An int out of range --
`sw 9` -- made the next DATA access end the emulator process in the DATA arm's range check; a wide value was truncated
onto a legal port and serviced (0x100000003 selected port 3: kill table 2's M_revert).  #549 REFUSES any selector >= 8,
compared on the full 64-bit value, at the PORT arm (the previous, valid selector is kept) and announces the refusal
once per device, `(once)`.

SESSIONS (each on a fresh emulator)
  C  controls: PORT=5, DATA=0x2a, read both back (LIVENESS); X1=123 and Y1=123, COMMAND=GET_RESOLUTION, read X1 and Y1
     (DEVICE SIGNATURE: the model zeroes both without X11 -- RAM at +0x10 would read back 2, the last value written
     there, and a banked register WITHOUT command execution would read 123); no `(once)` line may appear.
  A  accept: all EIGHT selectors, written at widths 1, 2, 4 and 8, each read back through PORT; ports 1-7 round-trip
     a distinct DATA value (port 0 is COMMAND and is written only with NOP); no `(once)` line may appear.
  P  refusal, anchored to a previous selector: PORT=5 (DATA 0x2a), then eleven out-of-range writes -- 8, 9, 16 (sw),
     0x200000000, 0x100000003, all-ones (sd), all-ones (sw), 0xff (sb), 0x100 (sh), 16 (sb), 16 (sh) -- each PRECEDED
     by a fresh PORT=5 and followed by a PORT read that must still say 5; then PORT=7 and a refused 9 must leave 7 --
     twelve refusals.  The `(once)` count must be exactly 1 right after the FIRST refusal and still 1 after the twelfth,
     and the one announce must name the first refused value, 0x8.
  R  re-arm: PORT=5, refuse 9, read PORT, a DATA write to port 5, a NOP command (PORT=0, DATA=0), a DATA READ of port 5,
     a GET_RESOLUTION command (PORT=0, DATA=2), PORT=5, refuse 9: the count is still 1 and PORT keeps 5.  Its own
     session because DATA traffic inside P can end the process: when the F2 prototype put such traffic in P, after
     its refused 8, an edit that accepts 8 (M_gt) ended the emulator at P's step 4 and blanked 14 of P's rows
     (regress/artifacts/fbctrlportkill_20260924/opus549_measured/f2/proto_d4inP_summary.out).
  K  the witness pair, repaired: PORT=5, DATA=0x2a, PORT=9 refused, then a DATA READ (must survive and read port 5's
     0x2a) and a DATA WRITE of 0x77 (must land in port 5: read back through PORT=5).
  F  free-running: a refused PORT write at power-on and a guest `lw` of PORT execute INSIDE `continue`, which stops at a
     breakpoint after them; the lw must read 0 and the announce must name 0x9.  This invocation passes -V and no -v,
     so while free-running debug() is below its threshold and returns without printing, while fatal() prints: a refusal
     announced with debug() would pass every stepped row and fail here.
  V  cells: COMMAND=GET_RESOLUTION, X1=123, one refusal while COMMAND holds 2 and PORT=1 -- PORT must still read 1,
     X1 must stay 123, and that FIRST refusal must announce, naming 0x9; ports 1-7 filled with 0x11*p (the last fill
     selects 7), five refusals (9, 16, 0x100000003 by sd, 0xff by sb, 8), PORT read at once (it must still say 7),
     then all eight cells read back and the count is still 1.
  W  widths: selector 0 written by sb, sh, sw and sd and selector 7 by sb, sh and sw, each after PORT=5 (accepted);
     8 by sb, sh and sd after PORT=5 (refused -- the FIRST, by sb, must announce); 0x8000000000000000 by sd after
     PORT=5 (refused); 9 after PORT=6 (keeps 6); then `lb`, `lh` and `ld` of PORT with selector 5 (exactly 5 each).
  X2 X3 X4 X6 X7  five fresh devices, each: PORT=k, then its FIRST refusal (9 by sh after 2; 0x100000005 by sd after 3
     -- wide, and 5 as an int, never 3; all-ones by sd after 4 -- the largest value, and negative as a signed one; 9 by
     sb after 6; 0x100 by sh after 7): it announces exactly once, the announce names that value, and PORT keeps k.
  Y  COMMAND = 1: PORT=0 and DATA=1 run SET_RESOLUTION with X1 = Y1 = 0 from power-on, which dev_fb_resize() declines
     with a message ("size too small ... ignored"), so nothing is resized; PORT=5; its FIRST refusal, 9 by sw -- PORT
     keeps 5, and it announces once, naming 0x9; SET_RESOLUTION again, as traffic between refusals; PORT=5 and a second
     refusal, 0x100000003 by sd (3 as an int, never 5) -- PORT keeps 5 and the count is still 1; COMMAND reads back 1.
  Z  silence across selectors: PORT=2 and its FIRST refusal (9), then PORT=0, 1, 2, 3 and 4, each followed by a refusal
     of 9 -- the count is still 1 after all six, and PORT keeps 4.
  B  single bits: PORT=5, then EVERY single-bit value from 2^3 up that the width can carry -- 2^3..2^7 by sb,
     2^3..2^15 by sh, 2^3..2^31 by sw, 2^3..2^63 by sd, 108 refusals -- with PORT set to 5 again before each width
     and read back once after it; a register doubles between stores (dsll).  A refusal that let one of them through
     would store it as an int -- 2^k, INT_MIN or 0, never 5 -- and every later refusal of that width would keep it,
     so one read per width sees it.  The count must be exactly 1 after all 108.  Added by the verifying pass (the
     Opus 5.5 seat): the compare narrowed to ignore bits 5-7, 9-31 or 34-62 scored the full 111 rows, because no v5
     refusal had all of its bits from 3 up inside one of those ranges.

CONTRACT (clause e) -- AN ENUMERATION, NOT A LIST.
THE FLOOR.  The fixed PORT arm's body tests three things -- the access direction, the written value (`idata >=
DEV_FBCTRL_NPORTS`, on all 64 bits) and the latch (`!warned_port`) -- and it reads and writes `current_port`.  Every
cell of those is held: the value's magnitude, width and class, every bit the compare tests set alone at every width
(B), the latch unset and set, a read and a write.  The
previous selector (current_port's VALUE), the COMMAND cell and the data cells are NOT tested by the body -- the fix
makes no partition of them -- so an edit conditioned on one of them is coverage beyond the floor (clause e): the rows
hold the values listed below and claim nothing more.  For each EFFECT, each value listed is held by the session(s)
named, and the one-axis edit of every listed cell is measured red in
regress/artifacts/fbctrlportkill_20260924/table6/TABLE.out (under an earlier edit's name where the generated text
was identical to it: table5/CELLMAP.out) -- except the read of selector 0, whose edit is EQUIVALENT (NOT CLAIMED
(4)).  This is the class closure: pass 2, the F2 pass, the closing pass and the closing F2 pass each found such an
edit on a value the rows had left empty, and the verifying pass found one on a range of bits (B).
  a refusal keeps the previous selector -- width sb sh sw sd (P, W, B); previous 0 (F), 1 (V), 2 3 (X), 4 (X4, Z), 5
      (P, W, Y, B), 6 (W, X6), 7 (P, V, X7); COMMAND 0 (P, B), 1 (Y), 2 (V); latch unset (the first refusal of P, F,
      V, W, X2-X7, Y and B -- Z's and R's first refusals are never read back) and set (the rest)
  the first refusal announces once -- width sw (P, V, F, Y, Z) sb (W, X6) sh (X2, X7) sd (X3, X4); previous 0 (F), 1
      (V), 2 (X2, Z), 3 4 6 7 (X), 5 (P, W, Y); COMMAND 0 (P, F, W, X, Z), 1 (Y), 2 (V); the first-refused value from 8
      (P, W) to all-ones (X4)
  the later refusals are silent -- width sb (P, V, B) sh (P, W, B) sw (P, V, W, R, Z, B) sd (P, V, W, Y, B); previous
      0-4 (Z), 5 (P, W, R, Y, B), 6 (W), 7 (P, V); COMMAND 0 (P, W, Z, B), 1 (Y), 2 (V, R); across PORT reads, a DATA
      write, a DATA read, a NOP and a GET_RESOLUTION (R), a SET_RESOLUTION (Y), accepted selectors, twelve refusals
      (P) and 108 (B)
  the announce names the refused value -- 0x8 (P), 0x9 (F, V, X2, X6, Y), 0x100 (X7), the wide 0x100000005 (X3),
      all-ones (X4): width sw (P, F, V, Y) sb (X6) sh (X2, X7) sd (X3, X4); previous 0 (F), 1 (V), 2 3 4 6 7 (X), 5 (P,
      Y); COMMAND 0 (P, F, X), 1 (Y), 2 (V)
  a PORT read returns the selector -- lb lh ld (W) and lw (every session but K); every selector 0-7 (A), though a
      read of selector 0 cannot tell a skipped load from a real one (odata starts at 0: NOT CLAIMED (4)); COMMAND 0
      (A), 1 (Y), 2 (V); latch unset (A) and set (P)
  a refusal leaves the cells alone -- all eight cells after refusals of 9, 16, 0x100000003 (sd), 0xff (sb) and 8 at
      previous selector 7 with COMMAND 2 (V); X1 after a refusal of 9 (sw) at previous 1 with COMMAND 2 (V); port 5's
      cell after a refused 9 (sw) at previous 5 with COMMAND 0 (K); COMMAND itself after a refused 0x100000003 (sd) at
      previous 5 with COMMAND 1 (Y -- its second refusal only: the SET_RESOLUTION before it rewrites COMMAND, so a
      write by the first refusal would be overwritten before the read) -- and no other cell, width, selector or
      COMMAND value (NOT CLAIMED (8))
  an accepted selector is stored -- 0 and 7 at every width (W, A), every selector at one width (A); latch unset (A, W)
      and set (V's fills and Z's selections, after their first refusals)
Beyond the effects: the store of an out-of-range value, clamped, masked or reset; the compare narrowed or signed (bit
63 alone, bits 32-33, 32-bit truncation) or made to ignore any set of the bits it tests, at any width (B: every
single-bit value is refused); a boundary slip at 8; an announce on an accepted selector; an announce
demoted to debug() (F); an announce suppressed above or below any threshold, or on the sign bit (the first refusals
run from 8 to all-ones); and the pre-#549 process exit on DATA.
NOT CLAIMED (disclosed).  (0) An edit conditioned on TWO axes at once -- a joint cell such as "refuse 9 only by sb after
PORT=3", or "`ld` sets bit 32 except at selector 5" -- is caught only where a row happens to hold that pair; the
enumeration above is one-axis by design, and closing every pair is the unbounded growth the carrier's floor rules
refuse.  One pair is held and is recorded as a pair, not as a class: COMMAND non-zero with the latch set, before a PORT
read (R's second refusal; V's and Y's later ones) -- in the 94-row probe R was its only holder (the Opus closing-F2
seat, J_ref_cmdlatch).  (1) A process-global latch instead of the per-instance field, and an announce conditioned on
the machine's serial number.  The probe's `-E testmips` session has ONE fbctrl.  A second instance IS reachable without
adding a device -- two testmips machines in one process from a config file, `gxemul @config` -- and there the
process-global latch reds (measured by the Opus F2 seat, opus549_measured/f2/TABLE_twoinst.out), but that is a new
launcher this probe does not use: filed as `fbctrltwoinst`.  The latch is per instance by construction, a struct member,
untested across two machines.  (2) Any edit of the DATA arm's kept range check -- deleting it, deleting only its
`exit(1)`, weakening `>=` to `>`, or swapping its operand -- is unreachable while the PORT arm refuses, because no
out-of-range selector is ever stored; the check is KEPT as a tripwire.  It exits before it indexes, so an index of 8
cannot reach `warned_port` while it stands, and `port[8]` would be undefined behaviour, not a defined alias of the
latch.  (3) An exception for one value no row writes (`idata != 10`), a latch that re-arms only after more refusals than
any session makes (B makes 108), an announce suppressed or mangled only for one value no session refuses first
(`idata != 16`) or only for a CLASS of values no first refusal belongs to (values whose bits all lie in 9..31, say:
the first refusals are 8, 9, 0x100, 0x100000005 and all-ones, and the latch lets only a session's first refusal
announce), and an announce demoted to debug() for some values but not F's 9 -- only a free-running session tells
debug() from fatal() here, and F is the only one: the value space is 2^64, and no finite row set closes "except
value k".  (A threshold is not in this class, nor is a range of bits the COMPARE ignores: see "Beyond the
effects".)  (4) Equivalent edits: storing `(uint32_t) idata`, `(int) idata` or `idata & 7` (only 0..7 reach that
store, and each compiles to the fix's own binary), reordering the struct's fields, masking the PORT read with 7
(the selector is always 0..7), a PORT read that skips its load at selector 0 (odata starts at 0), and a latch set
to any nonzero value in place of 1.  (5) `printf` in place of `fatal()`, or the announce without its trailing
newline: indistinguishable in THIS invocation's output.  (6) Narrowing the DATA path's widths, and the device's OTHER
two process-ending calls -- fbctrl_command()'s default (any command other than 0-2, including the documented but
unimplemented FILL/COPY) and the access function's default (any offset other than 0x00/0x10): filed as `fbctrlcmdkill`
and `fbctrloffkill`.  (7) Edits to this instrument's own logic are reviewed, not rowed.  (8) The data cells' VALUES are
not an axis the rows enumerate.  An edit conditioned on a cell's value (`port[COLOR_B] == 0`, `port[Y1] != 0`) is
caught only where a row's refusal or read holds a triggering state, and the states held are: every cell 0 (F, W, X,
Z, B),
port 5 at 0x2a (P, K, R), X1 at 123 with COMMAND 2 (V's first refusal), ports 1-7 at 0x11*p with COMMAND 2 (V's later
refusals and the PORT read right after them), and COMMAND 1 (Y).  The cells-alone effect is claimed only as listed:
no cell is read back after an `sh` refusal or after a refusal at previous selector 0, 2, 3, 4 or 6, and after a
refusal at previous 5 the only cells read back are port 5's under COMMAND 0 (K) and COMMAND's under COMMAND 1 (Y,
its second refusal only).
LIMITS OF A ROW.  Session P re-selects PORT=5 before each refusal, so a refused selector cannot carry over into the next
row WHEN THE LEGAL SELECTION LANDS; an edit that also refuses legal selections defeats the re-select, and later rows
then inherit its value (M_acclatch).  Every read-back is taken after its session ends, so a session that dies part-way
blanks the rows it had already passed (M_acc4: session A died at step 5 and every accept row read `-`).  And session A's
"accept selector 0 written by sw" cannot see an IGNORED store -- the selector is already 0 at power-on -- so the cell
"0 by sw is accepted" is held by W's row after PORT=5, not by A's.  Session B reads PORT once per width, so each of
its rows says that SOME single-bit value of that width got through, not which: the row prints the last one's stored
int.

Every stepped word is compared with the emulator's own step line (the hand-assembled-encoding trap).
Output: one row per check, then FBCTRLP_CONTROL=OK|FAILED, FBCTRLP_RESULT=n/t, FBCTRLP_DONE.  The exit status is 0
only when the controls are OK and every row is green: a red row is a nonzero exit, not only a crash.
usage: fbctrl_port_probe.py <gxemul-binary>
```

## 6. SESSION B, VERBATIM (the v6 repair)

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
```

## 7. VARIANT TABLE 6 -- EVERY EDIT AT THE FULL 117, WITH ITS WRITTEN PREDICTION AND REASON (`table6/TABLE.out`, `table6/MANIFEST.out`)

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

## 8. THE FINDINGS PACKET, VERBATIM (`pass_v6/f2_v6_findings.md`)

# #549 v6's own pass -- EVERY SEAT'S FINDINGS, WITH MY DISPOSITION ON EACH (for the adjudication)

Pass: `pass_v6_brief.md` (51 KB: the fixed PORT arm, the v5->v6 probe diff, the gate-16 diff, variant table 6 and the
verifying pass's findings V1-V20 inlined).  Seats: the dedicated grok job (below); the nine-seat panel and the Opus
measuring seat's re-issue (appended when they land).  **The Opus seat's FIRST v6 answer (SHIP) was written by
claude-opus-4-8 after three refusal events and is NOT counted** (`opus5_pass_v6_FALLBACK_opus48.md`; the seat was
resumed for a re-issue).  Codex (GPT-6 Astra) walled until 07:01; the kimi CLI failed with a new 403 (subscription
access), covered by kimi-k3.

## WHAT HELD (measured)

* Table 6: 297 edits, 267 red, 30 at 117/117, **zero predictions missed**, and every one-bit and one-width narrowing red
  on EXACTLY the session-B width rows the pre-table addendum named (the channel check).  The three narrowings that swept
  v5 are red.  Gate 16 PASS with v6 (26 checks, 17 s); the gate's seven log fixtures behave as designed.

## FINDINGS

* **N1 -- LATCH-UNSET x BIT: THE COMPARE WEAKENED ONLY WHILE THE ONCE-LATCH IS CLEAR SCORES 117/117 AND RESTORES THE
  DATA-ARM EXIT** (the dedicated grok, walked, not built; the Opus seat's fallback segment named the same cell and
  witnessed the exit on a fresh device for `LB_unset16`, `opus549_measured/v6/unset_witness.out`).
  `else if ((d->warned_port ? idata : (idata & ~(1ULL << 4))) >= DEV_FBCTRL_NPORTS) {` -- accepts 16..23 while the
  latch is clear.  Every session's FIRST refusal (the only latch-clear write) is 8 or 9 (bit 3), 0x100 (bit 8),
  0x100000005 (bit 32) or all-ones (no single decisive bit); session B's first store is 8, which sets the latch before
  its single bits run.  So at latch-unset only bits 3, 8 and 32 are held alone; **58 bits are open** (4-7, 9-31,
  33-63).  grok's argument that this is FLOOR, not clause (0): the refusal block READS `warned_port`, and the carrier's
  joint-cell floor is *"the cross-product of the guard's dominating predicates with the device-STATE lvalues the fix's
  own repair path reads"*, with the generating-set rule *"at each floor cell, every idata bit the guarded body TESTS is
  written both clear and set"* -- latch-unset is a floor cell and its generating set is incomplete.  grok's remedy: 58
  fresh devices in one diff, each `PORT=5` (legal, does not set the latch), one `sw` of 2^k, one PORT read that must
  still say 5 -- one width, since a third qualifier (width) is a genuine (0) joint.
  The Opus fallback segment's reading, recorded but not counted: disclosed coverage debt under (0), *"closing it would
  need a fresh device per value (the unbounded growth the floor forbids)"* -- 58 is bounded, which is grok's point.
  **MY DISPOSITION: FLOOR (L2), repair in-round as v7** -- grok's reading follows the carrier's joint-cell rule as
  adjudicated on 2026-09-04 (the latch is a body-read state lvalue; the (d) enumeration's operand-swap clause draws
  exactly from body-read fields), and the cost is bounded and measurable (58 short sessions).  **This is the decision I
  most want tested**, together with the cost: 58 fresh emulator processes add to gate 16's wall time.
* **N2 -- `(idata & 7) != 6` as a one-axis edit scores 117/117 outside the literal text of (0)-(8)** (dedicated grok):
  bits 0-2 never change `idata >= 8`, so it is a predicate on bits the compare does not distinguish -- a value-class
  exception (a store of 14 is accepted and the exit returns).  **ACCEPTED as a disclosure sentence in (3)** ("an
  exception keyed on the low three bits"), not a row, per grok.
* **N3 -- grok's denominator** (walked): every mask of a bit 3..63 at any width, bound moves, 32-bit and signed compares
  -- red (table 6 measured the same channel); `idata != k`, finite windows, re-arm periods > 108, a previous-selector
  condition, the accept-path pairs, `lb`/`lh`/`ld` returning 0 while the latch is clear, `len == 3` -- inside (0)-(8).

## OPUS -- A SEAT FAILURE FOR THIS PASS

The seat was resumed twice; **both answers were written by claude-opus-4-8 after refusal events** (`agent_models.py`:
FALLBACK) -- `opus5_pass_v6_FALLBACK_opus48.md` (SHIP) and `opus5_pass_v6b_FALLBACK_opus48.md` (SHIP).  Neither is
counted.  Their MEASUREMENTS are checkable artifacts and are cited as such (`opus549_measured/v6/TABLE_v6floor.out`,
`RECHECK_v6b.out`, `unset_witness.out`): `WB_sh32` (accept 2^5 only by sh) 116/117 red on B's sh row; `LB_set16` (accept
16 only with the latch set) 109/117 red; `SN_signed` 111/117 red; and 117/117 for `LB_unset16` (accept 16 only with the
latch CLEAR -- N1's cell, the DATA-arm exit witnessed on a fresh device), `MB_v18` (accept 0x18), `PB_prev3_16` (accept
16 at previous 3) and `MB_pc4` (accept every value with exactly four bits set).  The fallback text classes N1 as clause
(0) debt and asks that NOT CLAIMED (3) be widened from "one value" to value CLASSES (`MB_pc4`); the second fallback
segment says its first had "briefly treated the value x latch escape as a possible L2 floor breach".

* **N4 -- `MB_pc4`: accept every value with exactly four bits set scores 117/117; (3)'s accept-side sentence names only
  "one value".**  **ACCEPTED -- wording**: (3) covers value classes on the accept side too, and says each reinstates the
  DATA-arm exit that NOT CLAIMED (2) keeps as the tripwire.

## THE PANEL (`_scratchpad/panel_20260925_194340/`; codex walled, the kimi CLI a subscription-access 403 covered by
## kimi-k3; grok and glm appended when they land)

* **N5 -- agy (SHIP WITH CHANGES) independently found N1's cell** ("the Latch x Bit gap": the only latch-clear values
  are the first refusals 8, 9, 0x100, 0x100000005 and all-ones) and classes it as the two-axis joint of NOT CLAIMED
  (0), bounded by the kept DATA-arm tripwire.  **So the seats split on N1: the dedicated grok says FLOOR (58 cells owed);
  agy and the Opus fallback text say (0).**
* **N6 -- agy: my brief's premise "the working tree's probe is still v5" is FALSE** -- I installed v6 (a9a2be3d) after
  drafting that line and before firing.  **ACCEPTED -- a stale brief premise; no effect on the review** (the inlined v6
  is the tree's file, byte for byte).
* **N7 -- deepseek: "every one-bit narrowing red on EXACTLY the predicted session-B width rows" overclaims** -- MKB_03,
  _04, _32, _33, _63 and MK_b8_ctl also red rows in P, W, V, X3, X7, Y (values sharing that bit).  **ACCEPTED --
  wording**: "the session-B rows red are exactly the widths that carry the bit; other sessions' rows also red where
  their refused values share it" (gate comment and brief).
* **N8 -- deepseek: "all 61 one-bit narrowings (MKB_03 .. MKB_63)" -- MKB_08 is MK_b8_ctl's text, so 60 MKB rows plus
  the control.**  **ACCEPTED -- wording.**
* **N9 -- kimi-k3: NOT CLAIMED (3)'s "a latch that re-arms only after MORE refusals than any session makes (B makes
  108)" is off by one** -- a latch that re-arms after exactly 108 (the second announce landing on a 109th refusal no
  session makes) also scores 117/117.  **ACCEPTED -- wording**: "only after 108 refusals or more".
* **N10 -- kimi-k3: session B depends on the emulated `dsll` EXECUTING, which the encoding pins and the disassembly
  control do not verify** -- but table 6's width-differentiated channel (bit 9 red on sh/sw/sd, never sb; bit 16+ never
  sh; bit 32+ never sw) is positive evidence that each 2^k reached the compare at each width.  **ACCEPTED -- a LIMITS
  sentence naming the dependency and that evidence** (a pinning row is optional; not adopted without a ruling).
* **N11 -- kimi-k3: "every bit the compare tests set alone at every width (B)" overclaims for narrow widths** -- sb
  carries bits 3-7 only.  **ACCEPTED -- wording**: "at every width that can carry it".
* **N12 -- kimi-k3: X5 appears in no holder list though the control row says "X2-X7".**  **EXPLAINED**: there is no X5
  -- previous selector 5 is P's, W's and Y's; the label is a range.  Wording: "X2, X3, X4, X6, X7".
* **N13 -- minimax: SHIP**, no findings beyond a timing assumption on the count sample (the announce is `fatal()`,
  unbuffered in this invocation's pty; the fix's count row is green on every run).

## GROK (panel) / GLM (appended as each lands)

### glm-5.3:cloud -- SHIP WITH CHANGES (`ollama_glm.txt`, 10,927 chars, packet-fed)

* **N14 -- glm on N1: two-axis, (0)-class, CONDITIONAL on (0)'s full text** (F1; the packet cut (0) mid-sentence).  The
  probe's (0) reads generally (`regress/fbctrl_port_probe.py`, "NOT CLAIMED (disclosed).  (0) An edit conditioned on TWO
  axes at once ..."), so glm's condition is met.  **glm joins agy and the fallback text on the (0) side; the dedicated
  grok alone says FLOOR.**  Count the arguments, not the seats: the question for the adjudication is unchanged -- is
  the latch a body-read state lvalue whose clear state is a floor cell under the joint-cell rule.
* **N15 -- V2 says five behaviour changers; table 6 carries six `BR_*` edits** (F2).  MANIFEST.out lists six, all
  RED.  **ACCEPTED -- records.**
* **N16 -- LIMITS OF A ROW's "not which" is imprecise** (F3): the row prints the last stored int, which names the bit
  for bits up to 30.  **ACCEPTED -- wording.**
* **N17 -- NOT CLAIMED (8)'s exclusivity rests on R's program order, which the packet does not inline** (F4; CANNOT
  SETTLE from the packet).  R's entry is at `regress/fbctrl_port_probe.py` ("#  R: between two refusals, ...").
  **OPEN -- for the file-reading adjudicators (Fable, Astra) to settle by reading R's rows.**
* **N18 -- the commit must carry the v6 probe with the gate's 117 pin** (F5).  **ACCEPTED -- already so** (the tree
  holds v6, a9a2be3d; N6).
* **N19 -- the pre-table addendum was not inlined** (F6).  **ACCEPTED** -- cited by path for the adjudication.
* **N20 -- an unstated invariant: only K and R read DATA without re-selecting PORT first** (glm's "what did all of us
  miss").  **ACCEPTED -- one LIMITS sentence.**
* glm's Q1 zero carries its denominator (one-axis shapes across width, bit, range, bound, truncation, accept map, read
  side, announce side, latch period, direction; previous selector and COMMAND single-axis).  V1-V20: all UPHOLD (V2
  with N15).

### grok-4.7 xhigh (panel) -- SHIP WITH CHANGES (`grok.txt`, 8,011 bytes, file-reading; walked, not built)

* **N21 -- grok: A FLOOR BREACH OUTSIDE (0)-(8), SINGLE-AXIS.**  A refusal that WRITES THE CONSTANT 5 for a value the
  probe refuses only after `PORT=5` reads back exactly like a refusal that KEEPS 5 -- and every B value (and P's
  0x200000000, W's 2^63) is refused only at previous selector 5.  So a value-keyed constant write on the refuse path
  (grok names 32, 64, 128, 0x200 and any value whose low 32 bits are zero) is predicted 117/117.  The SESSIONS text's
  "never 5" covers only a STORE of the truncated value (2^k, INT_MIN or 0), which table 6 shows red.  **grok's remedy:
  one anchor other than 5 -- e.g. B's sd group selecting 7 before its stores -- so that neither a stored 2^k nor a
  written 5 reads back as the anchor.**  **MY DISPOSITION: FOR THE ADJUDICATION -- the second floor question of this
  pass, beside N1.**  It is one-axis (the value alone selects it), so (0) does not reach it; it is the "kept" reading
  that the anchor cannot tell from "re-written to the anchor", which is clause (f)'s shape (a relative oracle) on the
  refusal side.  Open for the ruling: whether one second anchor closes it or merely moves it (a constant equal to the
  new anchor, on bits only that width carries).
* **N22 -- NOT CLAIMED (4) names SEVEN equivalents; the gate comment says the contract discloses THIRTEEN** (grok 2; V9
  and V18 REFINE).  Six measured equivalents (`EQ_gt7`, `EQ_maskhi`, `EQ_ge8lit`, `EQ_dir_new`, `EQ_latch_ne1`,
  `EQ_ann_idata`) are in no header sentence.  **ACCEPTED -- wording** ((4) names all thirteen, or the gate comment
  says seven).
* **N23 -- the pre-table addendum's CHANNEL lines are wrong in four places** (grok 3): the count row catches latch
  periods through 107, not "up to 106"; `MK_b5_7` is red on all four widths, not sb alone; `MK_b9_31` is also red at
  sd; `B_mod11` is also red on P's twelve-refusal row.  Every RED/GREEN prediction held; the per-row channel lists
  were incomplete.  **ACCEPTED -- records**: the addendum is pre-registered and is not edited; the correction is
  recorded here and in the round block.  (grok checks (3)'s "more than 108" bound against these: it holds.)
* **N24 -- the addendum's latch witness names the wrong edit** (grok 4): `CELL_keep_l0` never sets the latch, so every
  value is stored and the sb read is the LAST store, not the first.  The effect the addendum wanted is real and is
  shown by `MKB_03` (all four widths stay 0x8).  **ACCEPTED -- records.**
* grok's Q1 denominator (from table 6's raw got-values): each single bit 3..63, the three ranges, the four one-width
  ignores, the bound moves both ways, the 32-bit window, reset-to-0, `idata & 7`, store-`idata` -- red.  Green and no
  behaviour change: the six equivalents of N22 and the thirty disclosed.  Green WITH a behaviour change: N21 only.
  V1-V20: UPHOLD except V2, V9, V18 REFINE (N22) and V16 CANNOT SETTLE (a record note grok did not reopen).
* On N1 the panel grok says nothing directly; it classes a width x value joint as (0).

## THE SEATS, FINAL: agy, deepseek, minimax, kimi-k3 (covering the kimi CLI's 403), glm, grok (panel), grok
## (dedicated) ANSWERED.  codex WALLED (usage limit to 07:01).  Opus: SEAT FAILURE (two fallback answers, not
## counted; their measurements cited as artifacts).  Fable: THIS ADJUDICATION.  Astra: owed after 07:01.

## THE QUESTIONS FOR THE ADJUDICATION

1. **N1** (latch-unset x bit): FLOOR -- a repair in-round -- or NOT CLAIMED (0)?  Tally: the dedicated grok FLOOR;
   agy, glm and the fallback text (0).  Count the arguments.
2. **N21** (a constant-5 write on the refuse path for values refused only at previous 5): FLOOR, or disclosed?  If
   FLOOR, does one second anchor close it, and what is the stop condition?
3. **Which of my ACCEPTED dispositions is wrong?**  (N2, N4, N6-N20, N22-N24.)
4. **N17** (NOT CLAIMED (8) against R's program order) is OPEN: settle it by reading R's session in
   `regress/fbctrl_port_probe.py`.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
