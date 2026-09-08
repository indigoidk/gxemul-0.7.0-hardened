# PASS 2 on `01a0339` -- two rows added to a shipped detector, and a comment-only source edit

**VERDICT LINE FIRST**, then the body.

## Why this pass exists, stated plainly

`01a0339` is a REPAIR made in response to a pass 2 on `c0c7f55`. This project's repair-chain rule is
that such a repair **owes its own pass 2** -- one pass per floor-bound diff, scoped to that diff,
closing on the first pass that finds **zero** floor breaches. The gate is currently RED refusing the
next commit for want of this receipt, which is the second time that has happened here.

**So the question is not "was the earlier finding right".** It was, and the repair is below. The
question is whether **this diff** is sound and whether the SHIPPED COMPOSITE detector now has a
clause-(d) hole.

## PLEASE DO NOT SIMPLY RATIFY

A recent panel here had seven of nine seats confirm a premise the brief stated wrongly. **Check the
premises, not just the derivations.** An honest "not checkable from this packet" beats a guess.

The tree under review is **`GXEMUL-SEC/src/`** -- ignore any other `src/` you can reach; three
pristine 2021 upstream copies sit under the project root and give line numbers off by hundreds.

---

# SETTLED PREMISES (inlined; you need not read files)

**1. What `c0c7f55` fixed.** `ubfx`/`sbfx` built their field mask with `(1 << width) - 1`, where
`width = 1 + ((iword >> 16) & 31)` reaches 32. `1` is a plain `int`, so the old expression was
undefined at the two highest widths: a shift count equal to the type width at 32 (C99 6.5.7p3) and a
signed overflow at 31 (6.5.7p4). The repair is
`uint32_t mask = (width == 32) ? 0xffffffffU : ((1U << width) - 1);` at two sites, plus hoisting the
sign-bit test under `if (width < 32 && ...)` at a third. `bfi` carries the same shape and was
DELIBERATELY left alone and disclosed (one-site rule).

**2. What the pass 2 on `c0c7f55` found, and what it cost.** The round asserted -- in the probe
comment, the CHANGELOG **and the commit message** -- that the `pc` control held *"on EVERY row, w32
included"*. **It did not.** Only `pc adv`, `mid pc` and `w32 pc` asserted pc, and all three are
MOV/UBFX rows; **no SBFX row checked pc at all.** The SBFX rows are exactly the ones whose expected
FAILURE value is also exactly zero -- i.e. the case a pc control exists to disambiguate from a word
that never executed. A commit message cannot be amended, so the CHANGELOG and probe comment carry
the correction.

**3. Measurement.** Pre-fix `9/11`, post-fix `11/11`, `12/12` after `s clear`, and **`14/14`** after
this diff (`regress/artifacts/armbfxwidth32/witness_FIXED14_20260907.raw`, sentinel `ARMBFX_DONE`).
All four build trees cleared two-part (est/ is a source tree: part 2 N/A).

**4. The probe's shape.** A cold guest plants one instruction word with `put w` on unmodified
`-E testarm`, sets `pc`, steps once, reads `r0` and `pc`. `SRC = 0x89abcdef` in r1. `CODE = 0x8000`,
so an executed word leaves `pc = 0x8004`. Encodings are DERIVED from the decoder, and the source
register is **`rm` = `iword & 15`**, not `rn` -- `rn`'s bits 19:16 hold `widthm1`.

**5. Two escapes are DISCLOSED as unkillable by any value row, and this is structural.** `1U`->`1`
in the ternary, and restoring `topBitMask` above the `if`. Both are DEFINEDNESS repairs, and
definedness has no guest-visible value on a non-trapping host: `1 << 31` and `1U << 31` give the
same mask after the `- 1`, and with a correct 32-bit mask `x |= ~mask` is `x |= 0`. They are filed
as `ubsanshiftlane` for a UBSAN differential, since `build-asan` carries
`-fsanitize=address,undefined`. **Do not re-report these as new; do challenge the claim that they
are unkillable BY A ROW.**

---

# THE DIFF -- the whole of it, both files

## `regress/arm_bfx_width_probe.py` (2 hunks)

```diff
diff --git a/regress/arm_bfx_width_probe.py b/regress/arm_bfx_width_probe.py
index a41c0a0..71da57e 100644
--- a/regress/arm_bfx_width_probe.py
+++ b/regress/arm_bfx_width_probe.py
@@ -37,9 +37,14 @@
 #  indistinguishable from the defect this probe exists to witness.  THREE independent controls,
 #  because one is not enough:
 #
-#    * `pc adv'  -- pc must advance by exactly 4.  An untranslatable word reaches the shared `bad'
-#                  label, which sets cpu->running = 0 and redirects to nothing_call (it does NOT
-#                  exit the host), so a bad encoding STOPS THE MACHINE and pc does not move.
+#    * `pc adv'  -- pc must advance by exactly 4.  A word the decoder cannot translate does not
+#                  quietly do nothing.  *** AN EARLIER DRAFT SAID IT ALWAYS REACHES THE SHARED
+#                  `bad' LABEL AND SETS cpu->running = 0.  THAT IS STALE: `#312' added an
+#                  UNDEFINED-INSTRUCTION route, and cpu_arm_instr.c says so in its own words --
+#                  "Routing to und fixes that", "This is where the und routing lives now" -- while
+#                  a `goto bad' remains for other cases.  So the claim is true of SOME encodings
+#                  and false as stated.  Either way pc does not land on CODE+4 with r0 set, which
+#                  is what this row actually tests. ***
 #    * `mid'     -- UBFX r0,r1,#4,#8 must give 0xde.  A small nonzero answer that only a correctly
 #                  encoded, correctly executed instruction produces.
 #    * `live'    -- a plain MOV proves plant/step/print works before any bitfield word is tried.
@@ -249,10 +254,26 @@ row("s w32", r0 if alive else "died", "0x89abcdef",
 #  field.  No row had an SBFX field whose top bit is CLEAR, so nothing could see it. ***
 #      SBFX #1,#4 of 0x89abcdef: (V >> 1) & 0xf = 0x7, bit 3 CLEAR -> NOT sign-extended -> 0x7
 #      under always-extend:      0x7 | ~0xf = 0xfffffff7
+row("s w32 pc", pc if alive else "died", "0x%x" % (CODE + 4),
+    "CONTROL: the SBFX word EXECUTED -- see the note below")
+#  *** ADDED BY PASS 2.  An earlier draft of this probe, its CHANGELOG block AND its commit
+#  message all said `pc adv = 0x8004' holds "on EVERY row".  IT DID NOT: only `pc adv', `mid pc'
+#  and `w32 pc' asserted pc, and all three are MOV/UBFX.  NO SBFX ROW CHECKED PC AT ALL -- and the
+#  SBFX rows are the ones whose expected failure value is also EXACTLY ZERO, which is precisely
+#  the case the pc control exists to disambiguate.  Named by the codex seat. ***
+
 t, alive, r0, pc = run_word(sbfx(1, 4))
 row("s clear", r0 if alive else "died", "0x7",
     "SBFX #1,#4 -> field 0x7, top bit CLEAR: must NOT sign-extend")
 
+#  *** ADDED BY PASS 2: SBFX AT WIDTH 31 WAS ENTIRELY UNTESTED. ***  The round's headline claim --
+#  "only the width-32 case is observable" -- rested on a UBFX width-31 row and generalised to SBFX
+#  with no evidence.  SBFX #0,#31 of 0x89abcdef masks to 0x09abcdef, whose bit 30 is CLEAR, so it
+#  must NOT sign-extend.  (codex.)
+t, alive, r0, pc = run_word(sbfx(0, 31))
+row("s w31", r0 if alive else "died", "0x9abcdef",
+    "SBFX #0,#31: bit 30 CLEAR, so no sign extension -- and it pins SBFX at width 31 at all")
+
 ok = sum(1 for _, o in rows if o)
 print()
 print("ARMBFX_RESULT=%d/%d" % (ok, len(rows)))
```

## `src/cpus/cpu_arm_instr.c` (4 hunks) -- claimed COMMENT-ONLY

```diff
diff --git a/src/cpus/cpu_arm_instr.c b/src/cpus/cpu_arm_instr.c
index 6baff8f..976ae66 100644
--- a/src/cpus/cpu_arm_instr.c
+++ b/src/cpus/cpu_arm_instr.c
@@ -1315,12 +1315,19 @@ X(ubfx)
 
 	/*  #510: was `(1 << width) - 1'.  `width' is `1 + ((iword >> 16) & 31)', so
 	    it reaches 32 -- and `1' is a plain int, so the old expression was
-	    undefined at BOTH ends of that range: a shift count equal to the type's
-	    width at 32 (C99 6.5.7p3), and a signed overflow at 31 (6.5.7p4).
+	    undefined at THE TWO HIGHEST VALUES of that range: a shift count equal
+	    to the type's width at 32 (C99 6.5.7p3), and a signed overflow at 31
+	    (6.5.7p4).  (An earlier draft said "at BOTH ends", which is wrong for
+	    {1..32} -- the low end, width 1, is perfectly well defined.)
 
-	    ONLY THE 32 CASE IS OBSERVABLE, and the probe measured it: `UBFX
+	    IN THE WITNESS RUNS, ONLY THE WIDTH-32 RESULT ROWS FAILED: `UBFX
 	    r0,r1,#0,#32' of 0x89abcdef returned 0x0 on the committed build, while
-	    `#0,#31' returned the correct 0x9abcdef.
+	    `#0,#31' returned the correct 0x9abcdef.  (An earlier draft said "ONLY
+	    THE 32 CASE IS OBSERVABLE", which claims more than the runs establish --
+	    and at the time SBFX at width 31 was not tested AT ALL, so the claim
+	    generalised a UBFX row to the other function.  `s w31' now covers it.)
+	    Note also that a width-32 extract returns the whole register only for a
+	    LEGAL field, i.e. lsb = 0; the decoder does not enforce that.
 
 	    *** WHAT THAT MEASUREMENT IS, STATED PRECISELY, BECAUSE A PASS-2 SEAT
 	    CAUGHT AN EARLIER DRAFT OVERSTATING IT.  The rows observe the RESULT
@@ -1333,9 +1340,14 @@ X(ubfx)
 	    a wrong value on this host.  `1U' defends 31 and the guard defends 32 --
 	    but a guest-VALUE probe cannot establish that, because `1 << 31' and
 	    `1U << 31' yield the SAME mask after the `- 1'.  No row can kill a
-	    `1U' -> `1' regression; UBSAN or a source pin can.  This is
-	    `cpu_m88k_instr.c's idiom in X(clr) and X(set), where `w == 0' encodes 32
-	    for that architecture.  */
+	    UBSAN or a source pin can.
+
+	    The SHAPE comes from `cpu_m88k_instr.c's X(clr)/X(set), but the analogy
+	    needs care and an earlier draft ran the two together: there `w == 0'
+	    ENCODES full width and the guard selects the full-width mask instead of
+	    zero.  **It is not defending against a shift by 32 -- m88k's encoded
+	    count never reaches 32.**  Here the guard IS doing that job.  Same
+	    shape, different reason.  */
 	uint32_t mask = (width == 32) ? 0xffffffffU : ((1U << width) - 1);
 
 	x >>= lsb;
@@ -1362,13 +1374,20 @@ X(sbfx)
 
 	/*  #510: was `(1 << width) - 1'.  `width' is `1 + ((iword >> 16) & 31)', so
 	    it reaches 32 -- and `1' is a plain int, so the old expression was
-	    undefined at BOTH ends of that range: a shift count equal to the type's
-	    width at 32 (C99 6.5.7p3), and a signed overflow at 31 (6.5.7p4).
+	    undefined at THE TWO HIGHEST VALUES of that range: a shift count equal
+	    to the type's width at 32 (C99 6.5.7p3), and a signed overflow at 31
+	    (6.5.7p4).  (An earlier draft said "at BOTH ends", which is wrong for
+	    {1..32} -- the low end, width 1, is perfectly well defined.)
 
-	    ONLY THE 32 CASE IS OBSERVABLE, and the probe measured it HERE, on SBFX:
-	    the `s w32' row returned 0x0 on the committed build.  (An earlier draft
-	    of this block was a VERBATIM COPY of the ubfx one and quoted a UBFX
-	    measurement -- a sentence about the other function.)
+	    IN THE WITNESS RUNS, ONLY THE WIDTH-32 RESULT ROWS FAILED: the `s w32'
+	    row returned 0x0 on the committed build.  (An earlier draft of this block
+	    was a VERBATIM COPY of the ubfx one and quoted a UBFX measurement -- a
+	    sentence about the other function.)
+
+	    *** AND WHEN THAT SENTENCE WAS FIRST WRITTEN, SBFX AT WIDTH 31 WAS NOT
+	    TESTED AT ALL -- the claim generalised a UBFX row to this function, which
+	    is the same copy-the-neighbour defect one paragraph up, committed while
+	    correcting it.  `s w31' now pins it.  A pass-2 seat named both. ***
 
 	    *** WHAT THAT MEASUREMENT IS, STATED PRECISELY, BECAUSE A PASS-2 SEAT
 	    CAUGHT AN EARLIER DRAFT OVERSTATING IT.  The rows observe the RESULT
@@ -1381,9 +1400,14 @@ X(sbfx)
 	    a wrong value on this host.  `1U' defends 31 and the guard defends 32 --
 	    but a guest-VALUE probe cannot establish that, because `1 << 31' and
 	    `1U << 31' yield the SAME mask after the `- 1'.  No row can kill a
-	    `1U' -> `1' regression; UBSAN or a source pin can.  This is
-	    `cpu_m88k_instr.c's idiom in X(clr) and X(set), where `w == 0' encodes 32
-	    for that architecture.  */
+	    UBSAN or a source pin can.
+
+	    The SHAPE comes from `cpu_m88k_instr.c's X(clr)/X(set), but the analogy
+	    needs care and an earlier draft ran the two together: there `w == 0'
+	    ENCODES full width and the guard selects the full-width mask instead of
+	    zero.  **It is not defending against a shift by 32 -- m88k's encoded
+	    count never reaches 32.**  Here the guard IS doing that job.  Same
+	    shape, different reason.  */
 	uint32_t mask = (width == 32) ? 0xffffffffU : ((1U << width) - 1);
 	x >>= lsb;
 	x &= mask;
```

**The comment-only claim was PROVEN, not asserted:** comment delimiters 317/317 before and after;
the three `#510` code expressions identical in count; and stripping every comment from both
revisions yields **byte-identical** files. **Check that claim against the diff above** -- if any
hunk touches code, say so, because the round's whole justification for not re-measuring behaviour
rests on it.

---

# QUESTIONS

1. **CHANNEL, for each of the two added rows.** Name **the mutant it kills** and **the observable
   that differs under that mutant**. A row whose named channel cannot vary under its named mutant is
   vacuous by construction, and that is knowable now, without running anything.
   * `s w32 pc` asserts `pc == 0x8004` on an SBFX word. Under which edit does it RED that some other
     row does not already catch? If the answer is "none", it is a control, not a kill -- say so.
   * `s w31` drives `SBFX #0,#31` on `0x89abcdef`; the masked field is `0x09abcdef`, whose bit 30 is
     CLEAR, so a correct build must NOT sign-extend. Which mutant does it kill?

2. **THE FLOOR QUESTION, asked of the SHIPPED COMPOSITE and not of this diff.** Is there a
   clause-(d) mutant -- keep the guard, null its repair; weaken a predicate the fix DEPENDS ON to
   the least-restrictive form that still reads like the same check -- that sweeps the **14-row**
   detector clean? The predicates in scope are `width == 32` in the ternary and `width < 32` in the
   sign-extend guard. **A measured clean sweep here is an L2 breach and is repaired in-round.**

3. **Is `s w31` actually load-bearing, or does `w31` already cover it?** `w31` is the UBFX row at
   width 31 and was green pre-fix and post-fix. The round's claim is that SBFX at width 31 was
   untested and that generalising `w31` to SBFX was unwarranted. **Is that right, or is `s w31`
   green under every edit that `w31` is green under -- i.e. a row that adds a name and no coverage?**

4. **Did the correction go far enough?** The CHANGELOG and probe comment now say only three rows
   assert pc and name which. Are there OTHER claims in this diff's prose that a measurement would
   refute? The round has now shipped three false statements about its own rows in two commits, so
   assume the fourth exists rather than that the pattern stopped.

5. **A records question with a real answer.** `c0c7f55`'s commit message is permanently false and
   cannot be edited. The round put the correction in the CHANGELOG and the probe comment. **Is that
   sufficient, or does something else need to carry it** so a future reader following the commit
   message alone is not misled?

## Rules

* Answer from the packet. Where you assert tree behaviour beyond it, name the file and function and
  flag that you are going past what was inlined.
* Disagreements are settled by measurement, never by vote -- prefer "measure X" to "I think X".
* If, while checking this, you found something ELSE -- say so.
