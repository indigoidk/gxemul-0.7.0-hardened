# PASS 2 — `#510` armbfxwidth32: UBFX/SBFX built their mask with an undefined shift

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

Tonight's other two passes each found real defects in my briefs — a wrong line count, a
false claim about mask equivalence, an overclaiming comment in shipped code. **Check the
premises, not just the derivations.** Where I state something as fact, ask whether it is true.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies exist
under the project root and are NOT this fork. Line numbers off by hundreds mean you are
reading one of them.

**If you cannot read files that is expected** — the entire product diff is inlined below,
verbatim (2 hunks, 47 changed lines, counted before sending).

**Where this brief states an ARITHMETIC claim, ENUMERATE it rather than reasoning about it.**

**VERDICT LINE FIRST.**

### If you can read files
Scope your reading to `GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/*.py`.
**Do not read `regress/artifacts/` or `tools/pipeline/ledger.json`.**

---

## 1. PREMISES ALREADY SETTLED, RE-INLINED

Settled by a six-seat pass 1 (`panel_20260907_174941`) and a codex fix-check, and re-verified
by reading before this brief:

* `ubfx` and `sbfx` decode `width = 1 + ((iword >> 16) & 31)` at `:4486` / `:4493`, so
  **`width ∈ {1..32}`**.
* `1` is a plain `int`. `1 << 32` shifts by the type's own width (C99 6.5.7p3); `1 << 31`
  overflows a signed `int` (6.5.7p4). **Both are undefined.**
* **ONLY THE 32 CASE IS OBSERVABLE, and that is MEASURED, not argued.** At 31 the expression
  is undefined TWICE and wraps back to the correct answer: `1 << 31` gives `INT_MIN`,
  `INT_MIN - 1` gives `INT_MAX` = `0x7fffffff`, which IS the right 31-bit mask.
* The fork's own idiom is `cpu_m88k_instr.c:532` / `:539` (`X(clr)`, `X(set)`):
  `w == 0 ? 0xffffffff : ((uint32_t)1 << w) - 1`, with `w ∈ {0..31}` — **the guard defends
  the full-width case and the CAST defends 31.**
* A codex fix-check examined 6/6 supplied sites, both m88k examples and 13 comparable
  decisions, and ratified both halves of this repair at the boundaries 1, 31, 32.

## 2. THE WITNESS, rung 3, unmodified `-E testarm`

`regress/arm_bfx_width_probe.py`. A cold guest plants one instruction word with `put w`,
sets `pc`, steps once, and reads `r0` and `pc` back.

    HEAD   9/11    witness_HEAD_20260907.raw
    FIX   11/11    witness_FIXED_20260907.raw     (same script)

    row      HEAD        FIX         want
    w32      0x0         0x89abcdef  0x89abcdef   UBFX #0,#32 must return the WHOLE register
    s w32    0x0         0x89abcdef  0x89abcdef   SBFX #0,#32, and its topBitMask is the 2nd UB
    w31      0x9abcdef   0x9abcdef   0x9abcdef    UB that WRAPS BACK to correct -- must STAY right
    mid      0xde        0xde        0xde         small NONZERO anchor
    pc adv   0x8004      0x8004      0x8004       on EVERY row, w32 included

**`pc adv` is the load-bearing control.** The width-32 symptom is *exactly zero*, which is
indistinguishable from a mis-encoded word that never executed — and this project has been
bitten four times by hand-assembled encodings, once in a committed gate row that measured the
wrong register for months. `pc adv = 0x8004` proves the instruction EXECUTED and returned a
wrong value. `mid` = `0xde` is the second, independent anchor.

## 3. THE DIFF

```diff
diff --git a/src/cpus/cpu_arm_instr.c b/src/cpus/cpu_arm_instr.c
index 8059125..fa48a70 100644
--- a/src/cpus/cpu_arm_instr.c
+++ b/src/cpus/cpu_arm_instr.c
@@ -1313,7 +1313,23 @@ X(ubfx)
 	int lsb = (uint8_t)ic->arg[2];
 	int width = ic->arg[2] >> 16;
 
-	uint32_t mask = (1 << width) - 1;
+	/*  #510: was `(1 << width) - 1'.  `width' is `1 + ((iword >> 16) & 31)', so
+	    it reaches 32 -- and `1' is a plain int, so the old expression was
+	    undefined at BOTH ends of that range: a shift count equal to the type's
+	    width at 32 (C99 6.5.7p3), and a signed overflow at 31 (6.5.7p4).
+
+	    ONLY THE 32 CASE IS OBSERVABLE, which is measured rather than argued:
+	    `UBFX r0,r1,#0,#32' of 0x89abcdef returned 0x0 on the committed build,
+	    because the mask became 0.  At 31 the expression is undefined TWICE and
+	    wraps back to the right answer -- `1 << 31' gives INT_MIN and
+	    `INT_MIN - 1' gives INT_MAX, which IS the correct 31-bit mask -- so it
+	    returned 0x9abcdef, correct.  The repair is owed by the language at both
+	    widths; only one of them was returning a wrong value.
+
+	    `1U' is load-bearing and not style: it is what defends width 31.  The
+	    guard defends 32.  This is `cpu_m88k_instr.c's own idiom in X(clr) and
+	    X(set), where `w == 0' encodes 32 for that architecture.  */
+	uint32_t mask = (width == 32) ? 0xffffffffU : ((1U << width) - 1);
 
 	x >>= lsb;
 	x &= mask;
@@ -1337,12 +1353,35 @@ X(sbfx)
 	int lsb = (uint8_t)ic->arg[2];
 	int width = ic->arg[2] >> 16;
 
-	uint32_t mask = (1 << width) - 1;
+	/*  #510: was `(1 << width) - 1'.  `width' is `1 + ((iword >> 16) & 31)', so
+	    it reaches 32 -- and `1' is a plain int, so the old expression was
+	    undefined at BOTH ends of that range: a shift count equal to the type's
+	    width at 32 (C99 6.5.7p3), and a signed overflow at 31 (6.5.7p4).
+
+	    ONLY THE 32 CASE IS OBSERVABLE, which is measured rather than argued:
+	    `UBFX r0,r1,#0,#32' of 0x89abcdef returned 0x0 on the committed build,
+	    because the mask became 0.  At 31 the expression is undefined TWICE and
+	    wraps back to the right answer -- `1 << 31' gives INT_MIN and
+	    `INT_MIN - 1' gives INT_MAX, which IS the correct 31-bit mask -- so it
+	    returned 0x9abcdef, correct.  The repair is owed by the language at both
+	    widths; only one of them was returning a wrong value.
+
+	    `1U' is load-bearing and not style: it is what defends width 31.  The
+	    guard defends 32.  This is `cpu_m88k_instr.c's own idiom in X(clr) and
+	    X(set), where `w == 0' encodes 32 for that architecture.  */
+	uint32_t mask = (width == 32) ? 0xffffffffU : ((1U << width) - 1);
 	x >>= lsb;
 	x &= mask;
 
-	uint32_t topBitMask = 1 << (width-1);
-	if (x & topBitMask && width < 32)
+	/*  #510: was `uint32_t topBitMask = 1 << (width-1);' followed by
+	    `if (x & topBitMask && width < 32)'.  A SECOND undefined shift, and the
+	    `width < 32' test that would have made it moot sat on the NEXT line --
+	    the operand was computed before the guard that excludes it.  Reordering
+	    the && is semantically identical for every width in {1..32} (both are
+	    ordinary locals with no side effects) and short-circuits before the
+	    shift.  At width 32 the field IS the whole register, so there is no sign
+	    to extend -- which is what the original test already said.  */
+	if (width < 32 && (x & (1U << (width - 1))))
 		x |= ~mask;
 
 	reg(ic->arg[0]) = x;
```

## 4. SCOPE — what is deliberately NOT in this round

* **`bfi` (`:1409`)** — same class, same file, and **left alone**. Its `width = msb - lsb + 1`
  spans **-30..32**, so 496 of 1024 encodings give a NEGATIVE shift count, which is undefined
  by the same clause. ARM calls `msb < lsb` UNPREDICTABLE. **No seat could settle from the
  tree what the model should do there**, and the obvious route is wrong as written: `X(und)`
  expects `arg[0]` to hold a PC offset and `bfi`'s holds a register pointer.
* **`:2685` / `:2823`** (`is_userpage`, `1 << (index & 31)`) — different semantic class, no row.
* **`m88k_rot:513` and MIPS `X(ext):1757`** — different CPUs; found by the fix-check, filed.

## 5. QUESTIONS

1. **The premise audit.** Is the repair correct at 1, 31 and 32? Is the `&&` reorder in `sbfx`
   semantically identical to the original for every width, or does it change behaviour at any
   value? **Does the added comment claim anything the rows do not establish?**
2. **What is the smallest edit that re-opens this and still scores 11/11?** Name the row you
   expect to stay green. *(Codex seat: skip this one — answer 1, 3, 4 instead.)*
3. **Is the SCOPE right?** `bfi` is the same expression in the same file and is untouched.
   Is leaving it a correct application of the round-scope rule, or is it a partial repair
   presented as complete?
4. **Is the witness honest about what it does not cover?** It drives four widths on one
   register value. Name a cell it should assert and does not.

If, while verifying a claim, you found something ELSE — say so.
