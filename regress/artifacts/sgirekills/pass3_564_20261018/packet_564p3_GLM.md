**Your token: `GLM_MTE564P3_20261018`** -- open your answer with it.

# `#564` sgirekills (MTE half) -- PASS 3: THE REPAIR'S OWN REVIEW

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A repair made in response to a pass 2 owes its own pass.  **Review effort is scoped to the repair diff (section 3);
the FLOOR QUESTION -- does any mutant in the vacuity floor's (d) enumeration sweep the SHIPPED COMPOSITE detector
clean? -- is asked of the whole detector, not just the new rows.**  A zero is a valid closing answer only with its
denominator: say which cells and mutant shapes you swept.  Check the premises, not just the derivations.

**THE TREE IS `GXEMUL-SEC/` AT HEAD `2951694f` PLUS THIS ROUND'S UNCOMMITTED EDITS** to `src/devices/dev_sgi_re.c`,
`regress/gate_arm.sh` and the new `regress/sgi_mte_decline_probe.py` -- the repaired state is inlined below.  Other
uncommitted files belong to another session.  Ignore the pristine upstream copies of GXemul under the project root.

**If you cannot read files that is expected** -- every fact you need is inlined.  Name any premise you cannot settle.

**VERDICT LINE FIRST.**

---

## 1. What pass 2 and the shared-findings pass decided

Pass 2 (`pass2_564_20261017/`): GPT-6 Astra SHIP WITH CHANGES (3), Grok 4.7 SHIP WITH CHANGES (2), GLM 5.3 SHIP WITH
CHANGES (3); Fable 5.1 SEAT FAILURE (HTTP 429, held by owner ruling).  A late Gemini 4 Argon reading of the same packet
(`argon_mte564p2.txt`) rediscovered both floor findings below independently.  The shared-findings pass
(`f2_564_20261017/`): Astra ALL UPHELD, GLM ALL UPHELD, Grok "1 WRONG (F9)" -- the floor upheld and the packet's append
recipe corrected (map B and LIN_B where first used, repaint every cell, linear cells at depth 8 / full mask / no COPY).

**The two floor breaches (L2, repaired in-round):**
* **F9 -- the destination labels.**  S1's and S2's `return` bypasses `switch (dst_tlb)`, so under the 2026-09-25
  skipped-dispatch label clause the floor for EACH is {A, B, C, LIN_A, LIN_B} x latch {CLEAR, SET}: 20 cells, of which
  the 53-row detector held 9.  `if (src > MTE_TLB_C && dst_tlb != MTE_TLB_B)` kept all 53 rows green.  Labels 3 (TEX),
  6 (CLIP) and 7 reach `default:`, which only prints, and are excluded.
* **F10 -- the latch alias.**  `SGIRE_W_MTE_STIPPLE = 1 << 10` (an alias of `SGIRE_W_BADMODE`) kept all 53 green: the only
  pre-existing latch bit any session set was `SGIRE_W_TLBA_LEN`.

**Records and disclosures adopted:** F1 -- a START-tagged READ also runs the transfer (`if (startFlag)
do_mte_transfer(cpu, d);` has no `writeflag` test), so the fix's comment that "the register store that carried START has
already landed" is corrected; F2 -- the probe header's "the paint is read after EVERY transfer" is false for the 32-mask
sweep; F3 -- five PRETABLE statements were wrong (errata file, section 6); F4/F7/F8 -- disclosed in the contract: the
printed VALUES are unchecked, source 1 is never driven, a decline that writes an MTE register is unobserved.  Rejected
on measurement: GLM's "a fourth diff hunk was never shown" (four were).  Added from Astra's F2 answer: accept rows at
tiled B and C, so a guard grown to refuse one tiled label is visible.

## 2. The repair, and its measurements (every number names its log, under `regress/artifacts/sgirekills/`)

* `dev_sgi_re.c` 1d65cdc1 -> **23fa76aa**: F1's comment correction only -- no executable change.
* `sgi_mte_decline_probe.py` 86caed24 -> **8928a02f**, 53 -> **68 rows**: S2 with the latch SET at B, C and LIN_B (appended
  AFTER the S2 session's last existing check, tile B and LIN_B mapped where first used); four new sessions, each
  pairing one S1-CLEAR and one S2-CLEAR cell (S1 at B / S2 at C; S1 at C / S2 at B; S1 at LIN_A / S2 at LIN_B; S1 at
  LIN_B / S2 at LIN_A); legal tiled fills at B and C appended to the ACCEPT session; a CROSSBIT session that sets every
  pre-existing latch bit 0-12 first (the priming sequence `sgi_re_colourdefault_probe.py`'s `allbits` rows proved, plus
  its colour decline for bit 12), proves all 13 announced (`xbit primed`), then wants each new site to announce once
  (`xbit texts`); the contract and NOT CLAIMED list rewritten.
* `gate_arm.sh`: the block now pins all 68 names, rows emitted 68, green 68, red 0.
* **Kill table 3** (`killtable3_564_20261017/`, PRETABLE3.out written BEFORE it): 29 mutants -- the 20 latch-conditioned
  label exemptions, one alias per new latch bit onto a pre-existing one, and S1/S2 grown to refuse every transfer to B
  or to C -- plus base, null and HEAD legs.  Its summary is section 5.
* Tables 1 and 2 stand as evidence for the 53 rows they scored on the old instrument: the repair only APPENDS (no
  existing row's commands before its read changed); aggregate rows can change VALUE under a mutant (`src once` reads
  10 where it read 7 for a missing-suppression mutant) and stay red -- a source-derived argument, not a re-measurement.

## 3. The repair diff (against the pass-2 state, preserved beside this file)

Diff hunks inlined: `dev_sgi_re.c` 1, `gate_arm.sh` 2, `sgi_mte_decline_probe.py` 7.

### 3a. `src/devices/dev_sgi_re.c` -- 1d65cdc1 -> 23fa76aa (comment only)

```diff
--- /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/sgirekills/pass3_564_20261018/dev_sgi_re.pass2_1d65cdc1.c	2026-10-18 00:50:24.468556100 -0500
+++ /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_sgi_re.c	2026-10-17 21:39:54.655070000 -0500
@@ -1512,9 +1512,11 @@
 
 	/*  #564: S1-S5 below DECLINE an unsupported transfer, with a latched
 	    announcement; each used to end the process (fatal() + exit(1)).  The
-	    decline returns before any TRANSFER data is written -- the register
-	    store that carried START has already landed in the caller and stays,
-	    and the caller's common tail still answers.  Each site has its own
+	    decline returns before any TRANSFER data is written.  On a
+	    START-tagged write the register store has already landed in the
+	    caller and stays; a START-tagged READ reaches here too (filed
+	    separately), and either way the caller's common tail still answers.
+	    Each site has its own
 	    latch bit (see the enum), and the `return' is OUTSIDE the latch, so
 	    every refused transfer is refused and only the announcement is once.
 	    Each old message's key phrase is kept in the new one.  */
```

### 3b. `regress/gate_arm.sh` -- the block re-pinned to 68 rows

```diff
--- /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/sgirekills/pass3_564_20261018/gate_arm.pass2.sh	2026-10-18 00:50:24.444020500 -0500
+++ /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gate_arm.sh	2026-10-17 22:14:05.541682700 -0500
@@ -1475,7 +1475,8 @@
 #  ---- destination -- each DECLINE with a latched announcement, where each used to end the process.  Wired
 #  ---- IN THE SAME COMMIT as the fix.  Measured with one instrument: 8/53 on the pre-fix build (HEAD
 #  ---- 2951694f; only the controls and the five ACCEPT rows green) and 53/53 on the fix
-#  ---- (regress/artifacts/sgirekills/detector_564_20261017/).  Modelled on the sgi_re_width_probe block
+#  ---- (regress/artifacts/sgirekills/detector_564_20261017/); the pass-2 repair took it to 68 rows
+#  ---- (regress/artifacts/sgirekills/killtable3_564_20261017/).  Modelled on the sgi_re_width_probe block
 #  ---- (find it with `grep -n 'sgi_re_width_probe.py "$PMAX"' gate_arm.sh`), at depth 0 so a sibling
 #  ---- probe's missing sentinel cannot swallow it.
 MTELOG=$LOGDIR/sgi_mte_decline.log
@@ -1495,14 +1496,14 @@
 
     #  PER ROW, ONE LINE.  The probe prints a name of at most 14 characters in a 16-column field, so every
     #  name is followed by TWO spaces and "^<name>  " cannot match a longer name that starts with it.
-    for v in "live" "devsig" "mode rt" "stip a" "stip b" "stip c" "stip copy" "stip lin a" "stip lin b" "stip surv" "stip once" "src 3" "src 4" "src 5" "src 6" "src 7" "src 3 copy" "src 3 lin" "src c fill" "src c copy" "src surv" "src once" "copy lin a" "copy lin b" "copy surv" "copy once" "depth a 16" "depth a 32" "depth a 64" "depth b 16" "depth b 32" "depth b 64" "depth surv" "depth once" "mask unwritten" "mask unw surv" "mask 0000ffff" "mask fffffffe" "mask 7fffffff" "mask sweep" "mask lin b" "mask surv" "mask once" "lin fill a" "lin fill b" "lin fill ecc" "tile mask" "tile copy mask" "latch paint" "latch texts" "latch old bit" "after fill" "after status"; do
+    for v in "live" "devsig" "mode rt" "stip a" "stip b" "stip c" "stip copy" "stip lin a" "stip lin b" "stip surv" "stip once" "src 3" "src 4" "src 5" "src 6" "src 7" "src 3 copy" "src 3 lin" "src c fill" "src c copy" "src surv" "src once" "copy lin a" "copy lin b" "copy surv" "copy once" "depth a 16" "depth a 32" "depth a 64" "depth b 16" "depth b 32" "depth b 64" "depth surv" "depth once" "mask unwritten" "mask unw surv" "mask 0000ffff" "mask fffffffe" "mask 7fffffff" "mask sweep" "mask lin b" "mask surv" "mask once" "lin fill a" "lin fill b" "lin fill ecc" "tile mask" "tile copy mask" "latch paint" "latch texts" "latch old bit" "after fill" "after status" "src 3 b" "src 3 c" "src 3 lin b" "stip b clr" "src c clr" "stip c clr" "src b clr" "stip la clr" "src lb clr" "stip lb clr" "src la clr" "fill b ok" "fill c ok" "xbit primed" "xbit texts"; do
         check "sgi_mte row: $v" "$(count "$MTELOG" "^$v  .*ok$")" "1"
     done
 
     #  DENOMINATOR PINNED TO A LITERAL, summed arithmetically (count() is plain grep: a `|' would be literal).
     check "sgi_mte rows emitted" \
-          "$(( $(count "$MTELOG" " ok$") + $(count "$MTELOG" " FAIL$") ))" "53"
-    check "sgi_mte rows green"   "$(count "$MTELOG" " ok$")"   "53"
+          "$(( $(count "$MTELOG" " ok$") + $(count "$MTELOG" " FAIL$") ))" "68"
+    check "sgi_mte rows green"   "$(count "$MTELOG" " ok$")"   "68"
     check "sgi_mte rows red"     "$(count "$MTELOG" " FAIL$")" "0"
 fi
 
```

### 3c. `regress/sgi_mte_decline_probe.py` -- 86caed24 -> 8928a02f

```diff
--- /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/sgirekills/pass3_564_20261018/sgi_mte_decline_probe.pass2_86caed24.py	2026-10-18 00:50:24.419442400 -0500
+++ /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/sgi_mte_decline_probe.py	2026-10-17 21:39:54.697620800 -0500
@@ -22,20 +22,32 @@
 #    row reads the paint back.  Tiled destinations use the #509 tile (re_tlb_[abc][0] = 0x8002 -> phys
 #    0x20000); linear ones map phys page 0x30 in ONLY the array the arm reads (`sd 0x8000003000000000' to
 #    CRIME_RE_LINEAR_A or _B), cleared again after use;
-#  * a guard scoped to fewer destinations, sources, depths or masks than today's: S1 at tiled A/B/C, tiled A
-#    COPY, LIN_A and LIN_B (at depth 8 with a full mask, so S4/S5 cannot hide the escape); S2 at every refused
-#    source value {3,4,5,6,7} on a tiled fill, at 3 on a tiled COPY and on a linear fill; S3 and S4 at both
-#    linear labels, S4 at every refused depth {16,32,64}; S5 at the reset default (BYTEMASK never written), at
-#    0x0000ffff, 0xfffffffe, 0x7fffffff, at LIN_B, and across all 32 single-zero masks (one row);
+#  * a guard scoped to fewer destinations, sources, depths or masks than today's: S1 and S2 at EVERY destination
+#    label whose arm writes guest memory -- tiled A/B/C, LIN_A, LIN_B -- each in BOTH latch states (the first
+#    refusal of its site in a session, and a later one).  Their `return' bypasses `switch (dst_tlb)', so under
+#    the 2026-09-25 skipped-dispatch label clause a guard exempting ONE label in ONE latch state is a floor cell:
+#    20 cells, each held by a row (linear ones at depth 8 with a full mask, so S4/S5 cannot hide the escape).  S1
+#    also on a tiled A COPY; S2 at every refused source value {3,4,5,6,7} on a tiled fill and at 3 on a tiled
+#    COPY.  S3 and S4 at both linear labels, S4 at every refused depth {16,32,64}; S5 at the reset default
+#    (BYTEMASK never written), at 0x0000ffff, 0xfffffffe, 0x7fffffff, at LIN_B, and across all 32 single-zero
+#    masks (one row);
 #  * a guard grown to refuse legal transfers -- the ACCEPT side: a tiled fill and a tiled COPY at src C
 #    (the S2 bound), linear fills at both labels and at the PROM's own mode 0x11 (DST_ECC), and tiled
 #    fill/COPY with a non-full BYTEMASK (the linear restrictions must stay inside their branch);
 #  * the latch: a missing announcement, a missing suppression, a `return' moved INSIDE the latch (the paint is
-#    read after EVERY transfer, including the repeats), a bit shared between two new sites (one session drives
-#    S1..S5 then S1 again and wants five distinct texts once each), and an assignment that clears an EXISTING
-#    bit (SGIRE_W_TLBA_LEN, set first by one 4-byte store to CRIME_RE_TLB_A, must not announce again).
+#    read after every transfer, including the repeats -- except the 32-mask sweep, whose paint is read ONCE, at
+#    its end), a bit shared between two new sites (one session drives S1..S5 then S1 again and wants five
+#    distinct texts once each), an assignment that clears an EXISTING bit (SGIRE_W_TLBA_LEN, set first by one
+#    4-byte store to CRIME_RE_TLB_A, must not announce again), and a new site's bit ALIASED onto a pre-existing
+#    one: one session sets every pre-existing bit 0-12 first -- the priming sequence sgi_re_colourdefault_probe.py's
+#    `allbits' rows proved -- shows all thirteen announced (`xbit primed'), then wants each new site to announce
+#    exactly once (`xbit texts').  Measured for one alias per new site; every other (site, bit) pair is held BY
+#    CONSTRUCTION via `xbit primed'.
 #
-#  NOT CLAIMED: the rendering result of any ACCEPTED transfer beyond "it landed" (tiled fill: the word left the
+#  NOT CLAIMED: source value 1 (never driven: a guard grown to refuse it alone would pass -- the two edges of
+#  `src > MTE_TLB_C', 2 and 3, are rowed); the VALUES each announcement prints (rows match the key phrase and the
+#  suffix only); an MTE register written by a declined transfer (no row reads one back after a START); a START-tagged
+#  READ, which also runs the transfer (filed); the rendering result of any ACCEPTED transfer beyond "it landed" (tiled fill: the word left the
 #  paint; tiled COPY: the source's first byte; linear fill: 0x44444444) -- #509's own detector owns the tiled
 #  colour channel; the `dst_y_step' and `default:' sibling arms (rows mtetlbflood, sgimtetlbdefault); START
 #  honoured on a READ (filed); destination labels 3, 6, 7 (they reach the default arm, which writes nothing,
@@ -64,6 +76,8 @@
 OP_SW_T0_A3 = 0xace80000          # sw   $t0, 0($a3)
 OP_SD_T0_A3 = 0xfce80000          # sd   $t0, 0($a3)
 OP_LW_V0_AT = 0x8c220000          # lw   $v0, 0($at)
+OP_SB_T0_A3 = 0xa0e80000          # sb   $t0, 0($a3)
+OP_LD_V0_AT = 0xdc220000          # ld   $v0, 0($at)
 OP_B_SELF   = 0x1000ffff          # b    .
 OP_NOP      = 0x00000000
 
@@ -174,6 +188,11 @@
         registers, so a skipped store is the same machine state)."""
         if force or self.reg.get(addr) != val:
             self.sw(addr, val); self.reg[addr] = val
+    def sb(self, addr, val):
+        self.cmds += ["a3=0x%x" % addr, "t0=0x%x" % val]; self._ops([OP_SB_T0_A3])
+    def load(self, addr, op):
+        """A load whose value is not read back (it exists for its side effect: the device's announcement)."""
+        self.cmds += ["at=0x%x" % addr]; self._ops([op])
     def check(self, addr, label):
         self.cmds += ["at=0x%x" % addr, "v0=0x%x" % SENTINEL]; self._ops([OP_LW_V0_AT])
         self.cmds += ["print v0"]; self.checks.append(label)
@@ -259,6 +278,12 @@
 lin_map(s, "a"); s.sw(LDEST, PAINT); s.go(SRC(3) | DST_LA | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "lin3")
 s.sw(TDEST, PAINT); s.go(SRC(2) | DST_A | D32); s.check(TDEST, "fillc")
 s.sw(TDEST + 4, SRC_WORD); s.sw(TDEST, PAINT); s.go(COPY | SRC(2) | DST_A | D32, src0=SRC_PIX); s.check(TDEST, "copyc")
+#  #564 pass-2 repair (F9): S2 at the other three writing labels with the latch SET -- appended AFTER every existing
+#  check of this session, so no earlier row's observable can move.
+tiles(s, a=False, b=True)                       # tile B mapped HERE, so the session's prefix is unchanged
+s.sw(TDEST, PAINT); s.go(SRC(3) | DST_B | D32); s.check(TDEST, "b3")
+s.sw(TDEST, PAINT); s.go(SRC(3) | DST_C | D32); s.check(TDEST, "c3")
+lin_map(s, "b"); s.sw(LDEST, PAINT); s.go(SRC(3) | DST_LB | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "lb3")
 s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "live")
 t, alive, r = s.run()
 for v in (3, 4, 5, 6, 7):
@@ -267,8 +292,29 @@
 row("src 3 lin", kept(r["lin3"]), "paint kept", "S2 at a linear destination")
 row("src c fill", landed(r["fillc"]), "landed", "ACCEPT: src 2 = MTE_TLB_C, the bound")
 row("src c copy", top(r["copyc"]), "0x1a", "ACCEPT: a COPY from TLB_C lands the source's first byte")
-row("src surv", "survived" if r["live"] == "0x%x" % LIVE_VAL else "died", "survived", "seven refused transfers, then RAM")
-row("src once", ntext(t, "S2") if alive else "died", 1, "seven refusals, one announcement")
+row("src 3 b", kept(r["b3"]), "paint kept", "S2 at tiled B, latch SET")
+row("src 3 c", kept(r["c3"]), "paint kept", "S2 at tiled C, latch SET")
+row("src 3 lin b", kept(r["lb3"]), "paint kept", "S2 at LIN_B, latch SET")
+row("src surv", "survived" if r["live"] == "0x%x" % LIVE_VAL else "died", "survived", "ten refused transfers, then RAM")
+row("src once", ntext(t, "S2") if alive else "died", 1, "ten refusals, one announcement")
+
+# ================================================================ S1 / S2 with the latch CLEAR at B, C, LIN_A, LIN_B
+#  #564 pass-2 repair (F9).  A CLEAR cell is the FIRST refusal of its site in its session, so each needs a session of
+#  its own; one S1 cell and one S2 cell share each session (different latch bits, and S2's refusal is the first S2 of
+#  that session).  Tiled A's CLEAR cells are `stip a' and `src 3' above.
+def refuse(s, flags, lab, key):
+    """One refused transfer at destination `lab' (b, c, la, lb), painted first, read back under `key'."""
+    if lab in ("b", "c"):
+        s.sw(TDEST, PAINT); s.go(flags | (DST_B if lab == "b" else DST_C) | D32); s.check(TDEST, key)
+    else:
+        lin_map(s, lab[1]); s.sw(LDEST, PAINT)
+        s.go(flags | (DST_LA if lab == "la" else DST_LB) | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, key)
+for s1lab, s2lab in (("b", "c"), ("c", "b"), ("la", "lb"), ("lb", "la")):
+    s = Sess(); tiles(s, a=True, b=True, c=True)
+    refuse(s, STIPPLE, s1lab, "s1"); refuse(s, SRC(3), s2lab, "s2")
+    t, alive, r = s.run()
+    row("stip %s clr" % s1lab, kept(r["s1"]), "paint kept", "S1 at %s, latch CLEAR (first S1 of the session)" % s1lab)
+    row("src %s clr" % s2lab, kept(r["s2"]), "paint kept", "S2 at %s, latch CLEAR (first S2 of the session)" % s2lab)
 
 # ================================================================ S3 linear COPY, both labels
 s = Sess()
@@ -329,12 +375,17 @@
 lin_map(s, "a"); s.sw(LDEST, PAINT); s.go(ECC | DST_LA | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "ecc")
 s.sw(TDEST, PAINT); s.go(DST_A | D32, bytemask=0x0000ffff); s.check(TDEST, "tmask")
 s.sw(TDEST + 4, SRC_WORD); s.sw(TDEST, PAINT); s.go(COPY | DST_A | D32, bytemask=0x0000ffff, src0=SRC_PIX); s.check(TDEST, "tcopy")
+tiles(s, a=False, b=True, c=True)               # appended: the existing rows' commands are unchanged
+s.sw(TDEST, PAINT); s.go(DST_B | D32, bytemask=0xffffffff); s.check(TDEST, "fb")
+s.sw(TDEST, PAINT); s.go(DST_C | D32); s.check(TDEST, "fc")
 t, alive, r = s.run()
 row("lin fill a", r["la"], "0x44444444", "ACCEPT: LIN_A, depth 8, full mask -- BG's low byte")
 row("lin fill b", r["lb"], "0x44444444", "ACCEPT: LIN_B")
 row("lin fill ecc", r["ecc"], "0x44444444", "ACCEPT: the PROM's own linear mode 0x11 (DST_ECC)")
 row("tile mask", landed(r["tmask"]), "landed", "ACCEPT: tiled fill with BYTEMASK 0x0000ffff")
 row("tile copy mask", top(r["tcopy"]), "0x1a", "ACCEPT: tiled COPY with BYTEMASK 0x0000ffff")
+row("fill b ok", landed(r["fb"]), "landed", "ACCEPT: a legal tiled fill at B (no S1/S2 growth onto B)")
+row("fill c ok", landed(r["fc"]), "landed", "ACCEPT: a legal tiled fill at C")
 
 # ================================================================ LATCH: an existing bit first, then S1..S5 and S1 again, in one session
 s = Sess(); tiles(s, a=True)
@@ -358,6 +409,56 @@
 row("latch old bit", len(re.findall(re.escape(TLBA_LEN_TEXT), t)) if alive else "died", 1,
     "SGIRE_W_TLBA_LEN set before the new sites stays set after them")
 
+# ================================================================ CROSSBIT: every pre-existing bit set FIRST, then S1..S5
+#  #564 pass-2 repair (F10).  A new site whose bit is aliased onto a pre-existing one (`SGIRE_W_MTE_STIPPLE = 1 << 10'
+#  is SGIRE_W_BADMODE) is silenced only once that bit is set, and no other session here sets bits 1-12.  The priming
+#  sequence is the one sgi_re_colourdefault_probe.py's `allbits' rows proved (bits 0-11), plus that probe's colour
+#  decline, which sets bit 12.  `xbit primed' counts the thirteen priming announcements, so a priming access that stops
+#  firing reds the row instead of leaving a hole; `xbit texts' wants each new site to announce exactly once.
+RE_WINDOWS = (0xb5001000, 0xb5001200, 0xb5001400, 0xb5001600, 0xb5001700, 0xb5001780)   # TLB_A..LINEAR_B
+DE_BASE, OUTSIDE, TEX_BASE = 0xb5002000, 0xb5001800, 0xb5001600
+DE_MODE_DST, DE_DRAWMODE, DE_FG = 0xb5002008, 0xb5002018, 0xb50020d0
+DE_XVERTEX_0, DE_XVERTEX_1, DE_PRIM_START = 0xb5002070, 0xb5002074, 0xb5002860
+PRIM_RECT, PRIM_BAD = 0x03020000, 0x05020000
+MODE_LINB_RGBA, MODE_YCRCB = 0x1620, 0x12f0
+def de_put(s, mode):
+    """One DE pixel PUT (sgi_re_colourdefault_probe.py's setup_put): LIN_A page 0x10, then a 1x1 rectangle."""
+    s.sd(RE_LIN_A, 0x0000001000000000); s.sw(0xa0010000, PAINT)
+    for a, v in ((DE_MODE_DST, mode), (DE_DRAWMODE, 0xf8), (DE_FG, 0xaabbccdd), (DE_XVERTEX_0, 0), (DE_XVERTEX_1, 0),
+                 (DE_PRIM_START, PRIM_RECT)):
+        s.sw(a, v)
+PRIME_LIT = ["for CRIME_RE_%s -- declined." % n for n in ("TLB_A", "TLB_B", "TLB_C", "TEX", "LINEAR_A", "LINEAR_B")] + [
+    "[ sgi_de: unimplemented len=",                        # bit 6  DE_LEN
+    "unimplemented write to address 0x1800",               # bit 7  UNMAP_WR
+    "unimplemented read from address 0x1800",              # bit 8  UNMAP_RD
+    "UNIMPLEMENTED drawing op",                            # bit 9  PRIM_OP
+    "unimplemented dst_mode",                              # bit 10 BADMODE
+    "unimplemented read from CRIME_RE_TEX -- declined.",   # bit 11 TEX_RD
+    "unimplemented colour type in horrible_getputpixel"]   # bit 12 BADCOLOR
+s = Sess()
+for w in RE_WINDOWS:
+    s.sb(w, 0x1)                                        # bits 0-5
+s.sb(DE_BASE, 0x1)                                      # bit 6
+s.sb(OUTSIDE, 0x1)                                      # bit 7
+s.load(OUTSIDE, OP_LW_V0_AT)                            # bit 8
+de_put(s, MODE_LINB_RGBA)                               # bit 10
+s.sw(DE_PRIM_START, PRIM_BAD)                           # bit 9
+s.load(TEX_BASE, OP_LD_V0_AT)                           # bit 11
+de_put(s, MODE_YCRCB)                                   # bit 12
+tiles(s, a=True)
+s.sw(TDEST, PAINT); s.go(STIPPLE | DST_A | D32); s.check(TDEST, "s1")
+s.sw(TDEST, PAINT); s.go(SRC(3) | DST_A | D32); s.check(TDEST, "s2")
+lin_map(s, "a")
+s.sw(LDEST, PAINT); s.go(COPY | DST_LA | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "s3")
+s.sw(LDEST, PAINT); s.go(DST_LA | D16, linear=True, bytemask=0xffffffff); s.check(LDEST, "s4")
+s.sw(LDEST, PAINT); s.go(DST_LA | D8, linear=True, bytemask=0x0000ffff); s.check(LDEST, "s5")
+t, alive, r = s.run()
+fired = sum(1 for lit in PRIME_LIT if lit in t)
+row("xbit primed", "%i/%i" % (fired, len(PRIME_LIT)) if alive else "died", "%i/%i" % (len(PRIME_LIT), len(PRIME_LIT)),
+    "all thirteen pre-existing latches PROVEN set before S1..S5")
+row("xbit texts", "/".join(str(ntext(t, k)) for k in ("S1", "S2", "S3", "S4", "S5")) if alive else "died",
+    "1/1/1/1/1", "with bits 0-12 set, each new site still announces once")
+
 # ================================================================ AFTER a decline: the engine still works and the status reads idle
 s = Sess(); tiles(s, a=True)
 s.sw(TDEST, PAINT); s.go(STIPPLE | DST_A | D32); s.check(TDEST, "decl")
```

## 4. The shipped composite, whole

### 4a. `do_mte_transfer()` (working tree, 23fa76aa) -- every exit path

```c
 1485  void do_mte_transfer(struct cpu* cpu, struct sgi_re_data *d)
 1486  {
 1487  	uint32_t mode = d->mte_reg[(CRIME_MTE_MODE - 0x3000) / sizeof(uint32_t)];
 1488  	uint32_t src0 = d->mte_reg[(CRIME_MTE_SRC0 - 0x3000) / sizeof(uint32_t)];
 1489  	uint32_t src1 = d->mte_reg[(CRIME_MTE_SRC1 - 0x3000) / sizeof(uint32_t)];
 1490  	uint32_t dst0 = d->mte_reg[(CRIME_MTE_DST0 - 0x3000) / sizeof(uint32_t)];
 1491  	uint32_t dst1 = d->mte_reg[(CRIME_MTE_DST1 - 0x3000) / sizeof(uint32_t)];
 1492  	int32_t src_y_step = d->mte_reg[(CRIME_MTE_SRC_Y_STEP - 0x3000) / sizeof(uint32_t)];
 1493  	int32_t dst_y_step = d->mte_reg[(CRIME_MTE_DST_Y_STEP - 0x3000) / sizeof(uint32_t)];
 1494  	uint32_t dstlen = dst1 - dst0 + 1, fill_addr;
 1495  	unsigned char zerobuf[4096];
 1496  	int depth = 8 << ((mode & MTE_MODE_DEPTH_MASK) >> MTE_DEPTH_SHIFT);
 1497  	int src = (mode & MTE_MODE_SRC_BUF_MASK) >> MTE_SRC_TLB_SHIFT;
 1498  	uint32_t bytemask = d->mte_reg[(CRIME_MTE_BYTEMASK - 0x3000) / sizeof(uint32_t)];
 1499  	uint32_t bg = d->mte_reg[(CRIME_MTE_BG - 0x3000) / sizeof(uint32_t)];
 1500  
 1501  	debug("[ sgi_mte: STARTING: mode=0x%08x src0=0x%08x src1=0x%08x src_y_step=%i dst0=0x%08x,"
 1502  	    " dst1=0x%08x dst_y_step=%i bg=0x%x bytemask=0x%x ]\n",
 1503  	    mode,
 1504  	    src0, src1, src_y_step,
 1505  	    dst0, dst1, dst_y_step,
 1506  	    bg, bytemask);
 1507  
 1508  	if (dst_y_step != 0 && dst_y_step != 1 && dst_y_step != -1) {
 1509  		fatal("[ sgi_mte: TODO! unimplemented dst_y_step %i ]", dst_y_step);
 1510  		// exit(1);
 1511  	}
 1512  
 1513  	/*  #564: S1-S5 below DECLINE an unsupported transfer, with a latched
 1514  	    announcement; each used to end the process (fatal() + exit(1)).  The
 1515  	    decline returns before any TRANSFER data is written.  On a
 1516  	    START-tagged write the register store has already landed in the
 1517  	    caller and stays; a START-tagged READ reaches here too (filed
 1518  	    separately), and either way the caller's common tail still answers.
 1519  	    Each site has its own
 1520  	    latch bit (see the enum), and the `return' is OUTSIDE the latch, so
 1521  	    every refused transfer is refused and only the announcement is once.
 1522  	    Each old message's key phrase is kept in the new one.  */
 1523  	if (mode & MTE_MODE_STIPPLE) {
 1524  		if (!(d->warned & SGIRE_W_MTE_STIPPLE)) {
 1525  			d->warned |= SGIRE_W_MTE_STIPPLE;
 1526  			fatal("[ sgi_mte: unimplemented MTE_MODE_STIPPLE (mode "
 1527  			    "0x%08x) -- transfer declined (once) ]\n", mode);
 1528  		}
 1529  		return;
 1530  	}
 1531  
 1532  	int src_tlb = (mode & MTE_MODE_SRC_BUF_MASK) >> MTE_SRC_TLB_SHIFT;
 1533  	int dst_tlb = (mode & MTE_MODE_DST_BUF_MASK) >> MTE_DST_TLB_SHIFT;
 1534  	
 1535  	if (src > MTE_TLB_C) {
 1536  		/*  #564: kept as `src > MTE_TLB_C' for fills AND copies.  A fill
 1537  		    never reads the source, but nothing establishes what the
 1538  		    hardware does with SRC_BUF on a fill (filed separately).  */
 1539  		if (!(d->warned & SGIRE_W_MTE_SRC)) {
 1540  			d->warned |= SGIRE_W_MTE_SRC;
 1541  			fatal("[ sgi_mte: unimplemented SRC %i -- transfer "
 1542  			    "declined (once) ]\n", src);
 1543  		}
 1544  		return;
 1545  	}
 1546  
 1547  	switch (dst_tlb) {
 1548  	case MTE_TLB_A:
 1549  	case MTE_TLB_B:
 1550  	case MTE_TLB_C:
 1551  		// Used by NetBSD's crmfb_fill_rect. It puts graphical
 1552  		// coordinates in dst0 and dst1.
 1553  		{
 1554  			int x1 = (dst0 >> 16) & 0xfff;
 1555  			int y1 = dst0 & 0xfff;
 1556  			int x2 = (dst1 >> 16) & 0xfff;
 1557  			int y2 = dst1 & 0xfff;
 1558  			x1 /= (depth / 8);
 1559  			x2 /= (depth / 8);
 1560  
 1561  			int src_x1 = (src0 >> 16) & 0xfff;
 1562  			int src_y1 = src0 & 0xfff;
 1563  			// int src_x2 = (src1 >> 16) & 0xfff;
 1564  			// int src_y2 = src1 & 0xfff;
 1565  			src_x1 /= (depth / 8);
 1566  			// src_x2 /= (depth / 8);
 1567  
 1568  			int dx = x1 > x2 ? -1 : 1;
 1569  			int dy = y1 > y2 ? -1 : 1;
 1570  			
 1571  			uint32_t src_mode = (src_tlb << 10) + (((mode & MTE_MODE_DEPTH_MASK) >> MTE_DEPTH_SHIFT) << 8);
 1572  			uint32_t dst_mode = (dst_tlb << 10) + (((mode & MTE_MODE_DEPTH_MASK) >> MTE_DEPTH_SHIFT) << 8);
 1573  
 1574  			// Hack. The MTE perhaps doesn't deal with colors per se,
 1575  			// but this makes sure that we copy 32 bits when doing 32-bit
 1576  			// transfers.
 1577  			/*  #509: was `depth == 4' -- UNREACHABLE.  `depth' is
 1578  			    a count of BITS (8 << a two-bit field, so 8/16/32/64
 1579  			    only); 4 is the corresponding BYTE count, which the
 1580  			    author used correctly in the `/ (depth / 8)' lines
 1581  			    just above.  So both assignments were dead, every
 1582  			    tiled transfer took the CI arm, and at 32 bits CI
 1583  			    assigns buf[0] alone while memory_rw copies four --
 1584  			    publishing three bytes of host stack into guest
 1585  			    memory.  The comment above states the intended
 1586  			    condition in words: 32-bit transfers.
 1587  
 1588  			    This repairs the 32-bit cell ONLY.  The 16-bit and
 1589  			    reserved-encoding-3 cells assign fewer bytes than
 1590  			    they copy for the same reason and are NOT closed
 1591  			    here -- see the uninitialised-buffer sibling.  */
 1592  			if (depth == 32) {	/*  #509  */
 1593  				src_mode |= DE_MODE_TYPE_RGBA;
 1594  				dst_mode |= DE_MODE_TYPE_RGBA;
 1595  			}
 1596  
 1597  			int src_y = src_y1;
 1598  			for (int y = y1; y != y2+dy; y += dy) {
 1599  				int src_x = src_x1;
 1600  				
 1601  				for  (int x = x1; x != x2+dx; x += dx) {
 1602  					if (mode & MTE_MODE_COPY) {
 1603  						horrible_getputpixel(0, cpu, d,
 1604  							src_x, src_y, &bg, src_mode);
 1605  						src_x += dx;
 1606  					}
 1607  
 1608  					horrible_getputpixel(1, cpu, d, x, y, &bg, dst_mode);
 1609  				}
 1610  				
 1611  				src_y += dy;
 1612  			}
 1613  		}
 1614  		break;
 1615  	case MTE_TLB_LIN_A:
 1616  	case MTE_TLB_LIN_B:
 1617  		// Used by the PROM to zero-fill memory (?).
 1618  		if (mode & MTE_MODE_COPY) {
 1619  			if (!(d->warned & SGIRE_W_MTE_COPY)) {
 1620  				d->warned |= SGIRE_W_MTE_COPY;
 1621  				fatal("[ sgi_mte: unimplemented MTE_MODE_COPY to "
 1622  				    "linear dst_tlb %i -- transfer declined (once)"
 1623  				    " ]\n", dst_tlb);
 1624  			}
 1625  			return;
 1626  		}
 1627  
 1628  		if (depth != 8) {
 1629  			if (!(d->warned & SGIRE_W_MTE_DEPTH)) {
 1630  				d->warned |= SGIRE_W_MTE_DEPTH;
 1631  				fatal("[ sgi_mte: unimplemented MTE_DEPTH_x: depth "
 1632  				    "%i to linear dst_tlb %i -- transfer declined "
 1633  				    "(once) ]\n", depth, dst_tlb);
 1634  			}
 1635  			return;
 1636  		}
 1637  
 1638  		debug("[ sgi_mte: LINEAR TRANSFER: mode=0x%08x dst0=0x%016llx,"
 1639  		    " dst1=0x%016llx (length 0x%llx), dst_y_step=%i bg=0x%x, bytemask=0x%x ]\n",
 1640  		    mode,
 1641  		    (long long)dst0, (long long)dst1,
 1642  		    (long long)dstlen, dst_y_step, (int)bg, (int)bytemask);
 1643  
 1644  		if (bytemask != 0xffffffff) {
 1645  			/*  #564: BYTEMASK is zeroed at init, so a guest that never
 1646  			    stores it reaches this decline.  */
 1647  			if (!(d->warned & SGIRE_W_MTE_BYTEMASK)) {
 1648  				d->warned |= SGIRE_W_MTE_BYTEMASK;
 1649  				fatal("[ sgi_mte: unimplemented MTE bytemask 0x%08x "
 1650  				    "to linear dst_tlb %i -- transfer declined (once)"
 1651  				    " ]\n", (int)bytemask, dst_tlb);
 1652  			}
 1653  			return;
 1654  		}
 1655  
 1656  		/*
 1657  		 *  Horrible hack:
 1658  		 *
 1659  		 *  During bootup, the PROM fills memory at 0x40000000 and
 1660  		 *  forward. This corresponds to the lowest possible RAM address.
 1661  		 *  However, these fills are not going via the CPU's cache,
 1662  		 *  which contains things such as the return address on the
 1663  		 *  stack. If we _really_ write this data in the emulator (which
 1664  		 *  doesn't emulate the cache), it would overwrite the stack.
 1665  		 *
 1666  		 *  So let's not.
 1667  		 *
 1668  		 *  (If some guest OS or firmware variant actually depends on
 1669  		 *  the ability to write to the start of memory this way,
 1670  		 *  it would not work in the emulator.)
 1671  		 */
 1672  		// if (dst0 >= 0x40000000 && dst0 < 0x40004000 && dst1 > 0x40004000) {
 1673  		//	dst0 += 0x4000;
 1674  		//	dstlen -= 0x4000;
 1675  		// }
 1676  
 1677  		/*
 1678  		 *  HUH?
 1679  		 *
 1680  		 *  Note that due to a bug (?) in the PROM firmware when it
 1681  		 *  is setting up the TLB entries, only every _second_ page is
 1682  		 *  actually put correctly in the TLB. This means that even
 1683  		 *  though it then tries to fill 0x40000000 .. 0x40007fff with
 1684  		 *  zeroes, it only fills 0x40001000 .. 0x40001fff,
 1685  		 *  0x40003000 .. 0x40003fff and so on!
 1686  		 *
 1687  		 *  So the Horrible hack above is not needed.
 1688  		 *
 1689  		 *  Ironic.
 1690  		 */
 1691  
 1692  		memset(zerobuf, bg, dstlen < sizeof(zerobuf) ? dstlen : sizeof(zerobuf));
 1693  		fill_addr = dst0;
 1694  		while (dstlen != 0) {
 1695  			uint64_t fill_len;
 1696  			if (dstlen > sizeof(zerobuf))
 1697  				fill_len = sizeof(zerobuf);
 1698  			else
 1699  				fill_len = dstlen;
 1700  
 1701  			uint64_t starting_page = fill_addr & ~0xfff;
 1702  			uint64_t ending_page = (fill_addr + fill_len - 1) & ~0xfff;
 1703  			if (starting_page != ending_page) {
 1704  				fill_len = starting_page + 4096 - fill_addr;
 1705  			}
 1706  
 1707  			// Find starting_page in the TLB in question.
 1708  			starting_page >>= 12;
 1709  			uint32_t *tlb = dst_tlb == MTE_TLB_LIN_A ? d->re_linear_a : d->re_linear_b;
 1710  			int match = 0;
 1711  			for (int i = 0; i < 32; ++i) {
 1712  				uint32_t entry = tlb[i];
 1713  				if (entry & 0x80000000) {
 1714  					entry &= ~0x80000000;
 1715  					if (entry == starting_page) {
 1716  						match = 1;
 1717  						break;
 1718  					}
 1719  				}
 1720  			}
 1721  			
 1722  			if (match) {
 1723  				cpu->memory_rw(cpu, cpu->mem, fill_addr, zerobuf, fill_len,
 1724  					MEM_WRITE, NO_EXCEPTIONS | PHYSICAL);
 1725  			} else {
 1726  				debug("[ sgi_mte: WARNING: address 0x%x not found in TLB? Ignoring fill. ]\n",
 1727  					(long long)fill_addr);
 1728  			}
 1729  
 1730  			fill_addr += fill_len;
 1731  			dstlen -= (uint32_t)fill_len;	/* OB-23: subtract bytes actually filled */
 1732  		}
 1733  		break;
 1734  	default:
 1735  		fatal("[ sgi_mte: TODO! unimplemented dst_tlb 0x%x ]", dst_tlb);
 1736  	}
 1737  }
```

### 4b. The latch enum's tail

```c
  139  	SGIRE_W_BADMODE   = 1 << 10,
  140  
  141  	/*
  142  	    #513: THE TEX READ DECLINE GETS ITS OWN BIT, not SGIRE_W_TEX_LEN.
  143  	    Sharing one was measured at 23/25 for SGIRE_W_DE_LEN in #498: an
  144  	    ordinary narrow write fires the width latch, and the read decline is
  145  	    then silently suppressed for the life of the instance.  The detector
  146  	    has a row for exactly this (`tex xbit', which fires all six width
  147  	    latches before reading).
  148  
  149  	    (This comment used to end "THE NEXT FREE BIT IS 1 << 12, AND THIS
  150  	    IS THE LAST ENUMERATOR".  #519 added SGIRE_W_BADCOLOR = 1 << 12
  151  	    BELOW this line and moved the sentence with it, as this comment
  152  	    itself instructed.  Demoted, not deleted, for the same reason as
  153  	    the two demotions above it.)
  154  	 */
  155  	SGIRE_W_TEX_RD    = 1 << 11,
  156  
  157  	/*  #519 (sgirandomcolour): the colour-type PUT decline in
  158  	    horrible_getputpixel() gets its OWN bit, per the rule every entry
  159  	    above records: the helper is per-pixel, the struct is shared by
  160  	    four handlers, and a latch shared with any other site is silenced
  161  	    by that site's ordinary traffic.  SGIRE_W_BADMODE (1 << 10) is the
  162  	    TLB/mode switch's decline in the same function and is a different
  163  	    event with a different text; sharing it would collapse the two.
  164  
  165  	    (This comment used to end "THE NEXT FREE BIT IS 1 << 13, AND THIS
  166  	    IS THE LAST ENUMERATOR".  #564 added SGIRE_W_MTE_STIPPLE ..
  167  	    SGIRE_W_MTE_BYTEMASK = 1 << 13 .. 1 << 17 BELOW this line and moved
  168  	    the sentence with them, as this comment itself instructed.  Demoted,
  169  	    not deleted, for the same reason as the demotions above it.)  */
  170  	SGIRE_W_BADCOLOR  = 1 << 12,
  171  
  172  	/*  #564 (sgirekills, MTE half): do_mte_transfer()'s five declines, ONE
  173  	    BIT PER SITE, for the reason every entry above records -- a latch
  174  	    shared with another site is silenced by that site's traffic.  LIN_A
  175  	    and LIN_B are two values of ONE guard at S3-S5, the shape of
  176  	    SGIRE_W_BADMODE (one bit, the value in the text).
  177  
  178  	    THE NEXT FREE BIT IS 1 << 18, AND THIS IS THE LAST ENUMERATOR --
  179  	    which is where that claim belongs, per the convention above.  A
  180  	    maintainer adding a bit BELOW this line must move this sentence
  181  	    with it and demote the copy here.  */
  182  	SGIRE_W_MTE_STIPPLE  = 1 << 13,
  183  	SGIRE_W_MTE_SRC      = 1 << 14,
  184  	SGIRE_W_MTE_COPY     = 1 << 15,
  185  	SGIRE_W_MTE_DEPTH    = 1 << 16,
  186  	SGIRE_W_MTE_BYTEMASK = 1 << 17,
  187  };
```

### 4c. `regress/sgi_mte_decline_probe.py` (8928a02f, 473 lines), whole

```python
   1  #!/usr/bin/env python3
   2  #
   3  #  #564 sgirekills (MTE half) -- DETECTOR: dev_sgi_re.c's do_mte_transfer() refuses five unsupported transfer
   4  #  parameters by DECLINING the transfer with a latched announcement, where it used to end the process:
   5  #
   6  #      S1  mode & MTE_MODE_STIPPLE              (before the destination switch: every destination)
   7  #      S2  src > MTE_TLB_C                      (before the switch: every destination, fill or copy)
   8  #      S3  mode & MTE_MODE_COPY                 (MTE_TLB_LIN_A / LIN_B only -- tiled COPY is implemented)
   9  #      S4  depth != 8                           (linear only)
  10  #      S5  bytemask != 0xffffffff               (linear only)
  11  #
  12  #  Every row is a REAL GUEST STORE or LOAD through real address decode and memory_rw on the unmodified
  13  #  `-E sgi -e ip32' machine (session mechanics from regress/sgi_mte_fill_probe.py, #509): the MTE is programmed
  14  #  with `sw', the RE TLBs with `sd', and a transfer fires on the write whose ADDRESS carries CRIME_DE_START.
  15  #
  16  #  ---------------------------------------------------------------------------------------------
  17  #  CONTRACT (vacuity-floor clause (e)) -- WHAT THIS DETECTOR IS DESIGNED TO CATCH.
  18  #
  19  #  * the terminating call put back at any site (every session ends at its first refused transfer);
  20  #  * the decline removed but the announcement kept -- the transfer proceeding with the refused parameter
  21  #    ignored (member 1): every refused transfer is aimed at a destination it WOULD write, pre-painted, and the
  22  #    row reads the paint back.  Tiled destinations use the #509 tile (re_tlb_[abc][0] = 0x8002 -> phys
  23  #    0x20000); linear ones map phys page 0x30 in ONLY the array the arm reads (`sd 0x8000003000000000' to
  24  #    CRIME_RE_LINEAR_A or _B), cleared again after use;
  25  #  * a guard scoped to fewer destinations, sources, depths or masks than today's: S1 and S2 at EVERY destination
  26  #    label whose arm writes guest memory -- tiled A/B/C, LIN_A, LIN_B -- each in BOTH latch states (the first
  27  #    refusal of its site in a session, and a later one).  Their `return' bypasses `switch (dst_tlb)', so under
  28  #    the 2026-09-25 skipped-dispatch label clause a guard exempting ONE label in ONE latch state is a floor cell:
  29  #    20 cells, each held by a row (linear ones at depth 8 with a full mask, so S4/S5 cannot hide the escape).  S1
  30  #    also on a tiled A COPY; S2 at every refused source value {3,4,5,6,7} on a tiled fill and at 3 on a tiled
  31  #    COPY.  S3 and S4 at both linear labels, S4 at every refused depth {16,32,64}; S5 at the reset default
  32  #    (BYTEMASK never written), at 0x0000ffff, 0xfffffffe, 0x7fffffff, at LIN_B, and across all 32 single-zero
  33  #    masks (one row);
  34  #  * a guard grown to refuse legal transfers -- the ACCEPT side: a tiled fill and a tiled COPY at src C
  35  #    (the S2 bound), linear fills at both labels and at the PROM's own mode 0x11 (DST_ECC), and tiled
  36  #    fill/COPY with a non-full BYTEMASK (the linear restrictions must stay inside their branch);
  37  #  * the latch: a missing announcement, a missing suppression, a `return' moved INSIDE the latch (the paint is
  38  #    read after every transfer, including the repeats -- except the 32-mask sweep, whose paint is read ONCE, at
  39  #    its end), a bit shared between two new sites (one session drives S1..S5 then S1 again and wants five
  40  #    distinct texts once each), an assignment that clears an EXISTING bit (SGIRE_W_TLBA_LEN, set first by one
  41  #    4-byte store to CRIME_RE_TLB_A, must not announce again), and a new site's bit ALIASED onto a pre-existing
  42  #    one: one session sets every pre-existing bit 0-12 first -- the priming sequence sgi_re_colourdefault_probe.py's
  43  #    `allbits' rows proved -- shows all thirteen announced (`xbit primed'), then wants each new site to announce
  44  #    exactly once (`xbit texts').  Measured for one alias per new site; every other (site, bit) pair is held BY
  45  #    CONSTRUCTION via `xbit primed'.
  46  #
  47  #  NOT CLAIMED: source value 1 (never driven: a guard grown to refuse it alone would pass -- the two edges of
  48  #  `src > MTE_TLB_C', 2 and 3, are rowed); the VALUES each announcement prints (rows match the key phrase and the
  49  #  suffix only); an MTE register written by a declined transfer (no row reads one back after a START); a START-tagged
  50  #  READ, which also runs the transfer (filed); the rendering result of any ACCEPTED transfer beyond "it landed" (tiled fill: the word left the
  51  #  paint; tiled COPY: the source's first byte; linear fill: 0x44444444) -- #509's own detector owns the tiled
  52  #  colour channel; the `dst_y_step' and `default:' sibling arms (rows mtetlbflood, sgimtetlbdefault); START
  53  #  honoured on a READ (filed); destination labels 3, 6, 7 (they reach the default arm, which writes nothing,
  54  #  so a paint row there cannot see an S1/S2 escape -- disclosed, not rowed); masks with two or more zero bits
  55  #  beyond the four rowed ones (sampled, not exhausted).
  56  #
  57  #  Clause (c), the null medium: an absent or non-emulator binary -- every session dies, every row that reads a
  58  #  value or a survival reds (measured, not claimed: see the round's artifacts).
  59  #
  60  #  Usage:  sgi_mte_decline_probe.py <gxemul-binary> [label]
  61  import os, sys, pty, select, time, re, tempfile
  62  
  63  BIN   = sys.argv[1]
  64  LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
  65  
  66  rows = []
  67  def row(name, got, want, note=""):
  68      ok = (got == want)
  69      rows.append((name, ok))
  70      #  16 columns for a name of at most 14: the gate greps "^<name>  .*ok$" (TWO spaces), and a name as long as
  71      #  its column leaves one -- the padded-column trap.  (The kill table ran the 14-column draft; only this
  72      #  width differs, see the round's artifacts.)
  73      print("%-16s %-22s %-12s %-56s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
  74      return ok
  75  
  76  OP_SW_T0_A3 = 0xace80000          # sw   $t0, 0($a3)
  77  OP_SD_T0_A3 = 0xfce80000          # sd   $t0, 0($a3)
  78  OP_LW_V0_AT = 0x8c220000          # lw   $v0, 0($at)
  79  OP_SB_T0_A3 = 0xa0e80000          # sb   $t0, 0($a3)
  80  OP_LD_V0_AT = 0xdc220000          # ld   $v0, 0($at)
  81  OP_B_SELF   = 0x1000ffff          # b    .
  82  OP_NOP      = 0x00000000
  83  
  84  CODE      = 0x80001000
  85  SCRATCH   = 0xa0001800
  86  LIVE_VAL  = 0x5a5a5a5a
  87  SENTINEL  = 0xdeadbeef
  88  DE_STATUS = 0xb5004000
  89  DE_STAT   = "0x1e000000"          # CRIME_DE_STATUS: IDLE|SETUP_IDLE|PIXPIPE_IDLE|MTE_IDLE; RAM reads 0
  90  
  91  DUMMY = os.path.join(tempfile.gettempdir(), "sgi_mte_decline_dummy.bin")
  92  if not os.path.exists(DUMMY):
  93      with open(DUMMY, "wb") as f:
  94          f.write(b"\0" * 8)
  95  
  96  #  CRIME base 0xb5000000 (KSEG1); offsets from src/include/thirdparty/crmfbreg.h.
  97  RE_TLB_A, RE_TLB_B, RE_TLB_C = 0xb5001000, 0xb5001200, 0xb5001400
  98  RE_LIN_A, RE_LIN_B           = 0xb5001700, 0xb5001780
  99  MTE_MODE       = 0xb5003000
 100  MTE_BYTEMASK   = 0xb5003008
 101  MTE_BG         = 0xb5003018
 102  MTE_SRC0       = 0xb5003020
 103  MTE_DST0       = 0xb5003030
 104  MTE_DST1_START = 0xb5003838       # CRIME_MTE_DST1 0x3038 | CRIME_DE_START 0x0800
 105  
 106  #  MTE_MODE: DST_BUF 0x1c >> 2, SRC_BUF 0xe0 >> 5, DEPTH 0x300 >> 8 (depth = 8 << field), STIPPLE 0x400, COPY 0x800.
 107  DST_A, DST_B, DST_C, DST_LA, DST_LB = 0 << 2, 1 << 2, 2 << 2, 4 << 2, 5 << 2
 108  D8, D16, D32, D64 = 0x000, 0x100, 0x200, 0x300
 109  STIPPLE, COPY, ECC = 0x400, 0x800, 0x001
 110  def SRC(v): return v << 5
 111  
 112  TILE      = 0x8002                # re_tlb_[abc][0]: bit 15 valid -> phys 0x20000 (the #509 tile)
 113  TDEST     = 0xa0020000            # tiled pixel (0,0), KSEG1
 114  LPAGE     = 0x80000030            # linear entry: valid | page 0x30
 115  LDEST     = 0xa0030000            # linear destination, KSEG1 of phys 0x30000
 116  LDST0, LDST1 = 0x00030000, 0x00030003
 117  PAINT     = 0x99999999
 118  BG_VAL    = 0x11223344
 119  SRC_WORD  = 0x1a2b3c4d            # first byte < 0x80 (sgirebufshiftub), four distinct bytes
 120  SRC_PIX   = 4 << 16               # SRC0: x = 4 bytes -> pixel 1 at depth 32
 121  
 122  #  Each site's announcement.  The key phrase is HEAD's own text (the witness attributes on it); the suffix is the
 123  #  decline's -- so a count of the SUFFIXED text counts declines, never a HEAD-style death message.
 124  DECL = "transfer declined (once)"
 125  KEY = {"S1": "unimplemented MTE_MODE_STIPPLE", "S2": "unimplemented SRC", "S3": "unimplemented MTE_MODE_COPY",
 126         "S4": "unimplemented MTE_DEPTH_x", "S5": "unimplemented MTE bytemask"}
 127  TLBA_LEN_TEXT = "for CRIME_RE_TLB_A -- declined.  (once)"
 128  
 129  def ntext(t, site):
 130      return len(re.findall(re.escape(KEY[site]) + r"[^\]\n]*" + re.escape(DECL), t))
 131  
 132  def session(cmds, settle=1.5, spin=1.8):
 133      pid, fd = pty.fork()
 134      if pid == 0:
 135          os.execv(BIN, [BIN, "-V", "-x", "-E", "sgi", "-e", "ip32", "-M", "64", "0x%x:" % CODE + DUMMY])
 136          os._exit(127)
 137      buf = ""
 138      def rd(t):
 139          nonlocal buf
 140          end = time.time() + t
 141          while time.time() < end:
 142              r, _, _ = select.select([fd], [], [], 0.1)
 143              if not r:
 144                  continue
 145              try:
 146                  d = os.read(fd, 65536)
 147                  if not d:
 148                      return False
 149                  buf += d.decode("latin-1", "replace")
 150              except OSError:
 151                  return False
 152          return True
 153      alive = rd(settle)
 154      for i, c in enumerate(cmds):
 155          try:
 156              os.write(fd, (c + "\n").encode("latin-1"))
 157          except OSError:
 158              alive = False; break
 159          if not rd(spin if i == len(cmds) - 1 else 0.22):
 160              alive = False; break
 161      try:
 162          os.write(fd, b"quit\n"); rd(0.4)
 163      except OSError:
 164          pass
 165      try:
 166          os.close(fd)
 167      except OSError:
 168          pass
 169      return buf.replace("\r", ""), alive
 170  
 171  class Sess(object):
 172      """One emulator session: a growing list of debugger commands, each check a labelled `lw' + `print v0'.
 173      Values come back IN ORDER; a check after the session ended reads 'died'."""
 174      def __init__(self):
 175          self.a = CODE; self.cmds = []; self.checks = []; self.reg = {}
 176      def _ops(self, ops):
 177          at = self.a; self.a += 4 * (len(ops) + 2) + 0x20
 178          put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
 179          put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
 180                  "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, OP_NOP)]
 181          self.cmds += put + ["pc=0x%x" % at, "step %d" % len(ops)]
 182      def sw(self, addr, val):
 183          self.cmds += ["a3=0x%x" % addr, "t0=0x%x" % val]; self._ops([OP_SW_T0_A3])
 184      def sd(self, addr, val):
 185          self.cmds += ["a3=0x%x" % addr, "t0=0x%x" % val]; self._ops([OP_SD_T0_A3])
 186      def mte(self, addr, val, force=False):
 187          """An MTE register store, skipped when the register already holds the value (the transfer reads the
 188          registers, so a skipped store is the same machine state)."""
 189          if force or self.reg.get(addr) != val:
 190              self.sw(addr, val); self.reg[addr] = val
 191      def sb(self, addr, val):
 192          self.cmds += ["a3=0x%x" % addr, "t0=0x%x" % val]; self._ops([OP_SB_T0_A3])
 193      def load(self, addr, op):
 194          """A load whose value is not read back (it exists for its side effect: the device's announcement)."""
 195          self.cmds += ["at=0x%x" % addr]; self._ops([op])
 196      def check(self, addr, label):
 197          self.cmds += ["at=0x%x" % addr, "v0=0x%x" % SENTINEL]; self._ops([OP_LW_V0_AT])
 198          self.cmds += ["print v0"]; self.checks.append(label)
 199      def go(self, mode, linear=False, bytemask=None, src0=None):
 200          if bytemask is not None:
 201              self.mte(MTE_BYTEMASK, bytemask)
 202          self.mte(MTE_MODE, mode)
 203          self.mte(MTE_BG, BG_VAL)
 204          if src0 is not None:
 205              self.mte(MTE_SRC0, src0)
 206          self.mte(MTE_DST0, LDST0 if linear else 0)
 207          self.sw(MTE_DST1_START, LDST1 if linear else 0)        # START: always stored, never skipped
 208      def run(self):
 209          t, alive = session(self.cmds)
 210          vals = re.findall(r"print\s+v0\s*\n\s*(0x[0-9a-f]+)", t)
 211          res = {}
 212          for i, lab in enumerate(self.checks):
 213              #  `lw' SIGN-EXTENDS: the paint 0x99999999 reads back as 0xffffffff99999999.  Compare the 32 bits the
 214              #  guest loaded.  (The first draft compared the whole register, so every `paint kept' row read
 215              #  "written" on the fixed build and every `landed' row was vacuous -- a paint that survived also
 216              #  differed from the 32-bit literal.  Measured 2026-10-17, probe_FIX_564.v1_signext.out.)
 217              res[lab] = ("0x%x" % (int(vals[i], 16) & 0xffffffff)) if i < len(vals) else "died"
 218          return t, alive, res
 219  
 220  def tiles(s, a=True, b=False, c=False):
 221      if a: s.sd(RE_TLB_A, TILE << 48)
 222      if b: s.sd(RE_TLB_B, TILE << 48)
 223      if c: s.sd(RE_TLB_C, TILE << 48)
 224  
 225  def lin_map(s, which):
 226      """Map phys page 0x30 in ONLY the named linear array; clear the other."""
 227      s.sd(RE_LIN_A, (LPAGE << 32) if which == "a" else 0)
 228      s.sd(RE_LIN_B, (LPAGE << 32) if which == "b" else 0)
 229  
 230  P = "0x%x" % PAINT
 231  def top(v):
 232      return v if not v.startswith("0x") else "0x%02x" % ((int(v, 16) >> 24) & 0xff)
 233  def landed(v):
 234      return "died" if v == "died" else ("paint" if v == P else "landed")
 235  def kept(v):
 236      return "died" if v == "died" else ("paint kept" if v == P else "written")
 237  
 238  print("# sgi_mte_decline_probe -- binary=%s label=%s machine=sgi/ip32, %s" % (BIN, LABEL, time.strftime("%Y-%m-%d %H:%M:%S")))
 239  print("%-16s %-22s %-12s %-56s %s" % ("row", "got", "want", "note", ""))
 240  
 241  # ================================================================ controls
 242  s = Sess(); s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "v")
 243  t, alive, r = s.run()
 244  row("live", r["v"], "0x%x" % LIVE_VAL, "RAM round-trip: the session and the CPU run")
 245  
 246  s = Sess(); s.check(DE_STATUS, "v")
 247  t, alive, r = s.run()
 248  row("devsig", r["v"], DE_STAT, "CRIME_DE_STATUS: only the device answers this")
 249  
 250  s = Sess(); s.mte(MTE_MODE, STIPPLE | D32); s.check(MTE_MODE, "v")
 251  t, alive, r = s.run()
 252  row("mode rt", r["v"], "0x%x" % (STIPPLE | D32), "an MTE register through the sgi_mte decode; no START")
 253  
 254  # ================================================================ S1 STIPPLE: every destination
 255  s = Sess(); tiles(s, a=True, b=True, c=True)
 256  for lab, mode in (("a", DST_A | D32), ("b", DST_B | D32), ("c", DST_C | D32)):
 257      s.sw(TDEST, PAINT); s.go(STIPPLE | mode); s.check(TDEST, "t" + lab)
 258  s.sw(TDEST + 4, SRC_WORD); s.sw(TDEST, PAINT); s.go(STIPPLE | COPY | DST_A | SRC(0) | D32, src0=SRC_PIX); s.check(TDEST, "tcopy")
 259  for lab in ("a", "b"):
 260      lin_map(s, lab); s.sw(LDEST, PAINT)
 261      s.go(STIPPLE | (DST_LA if lab == "a" else DST_LB) | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "l" + lab)
 262  s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "live")
 263  t, alive, r = s.run()
 264  row("stip a", kept(r["ta"]), "paint kept", "S1, tiled A fill at depth 32")
 265  row("stip b", kept(r["tb"]), "paint kept", "S1, tiled B")
 266  row("stip c", kept(r["tc"]), "paint kept", "S1, tiled C")
 267  row("stip copy", kept(r["tcopy"]), "paint kept", "S1, tiled A COPY (the tiled COPY arm would run)")
 268  row("stip lin a", kept(r["la"]), "paint kept", "S1, LIN_A depth 8 full mask (S3-S5 all pass)")
 269  row("stip lin b", kept(r["lb"]), "paint kept", "S1, LIN_B depth 8 full mask")
 270  row("stip surv", "survived" if r["live"] == "0x%x" % LIVE_VAL else "died", "survived", "six refused transfers, then RAM")
 271  row("stip once", ntext(t, "S1") if alive else "died", 1, "six refusals, one announcement")
 272  
 273  # ================================================================ S2 src > MTE_TLB_C: the refused domain {3..7}
 274  s = Sess(); tiles(s, a=True, c=True)
 275  for v in (3, 4, 5, 6, 7):
 276      s.sw(TDEST, PAINT); s.go(SRC(v) | DST_A | D32); s.check(TDEST, "f%d" % v)
 277  s.sw(TDEST + 4, SRC_WORD); s.sw(TDEST, PAINT); s.go(COPY | SRC(3) | DST_A | D32, src0=SRC_PIX); s.check(TDEST, "copy3")
 278  lin_map(s, "a"); s.sw(LDEST, PAINT); s.go(SRC(3) | DST_LA | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "lin3")
 279  s.sw(TDEST, PAINT); s.go(SRC(2) | DST_A | D32); s.check(TDEST, "fillc")
 280  s.sw(TDEST + 4, SRC_WORD); s.sw(TDEST, PAINT); s.go(COPY | SRC(2) | DST_A | D32, src0=SRC_PIX); s.check(TDEST, "copyc")
 281  #  #564 pass-2 repair (F9): S2 at the other three writing labels with the latch SET -- appended AFTER every existing
 282  #  check of this session, so no earlier row's observable can move.
 283  tiles(s, a=False, b=True)                       # tile B mapped HERE, so the session's prefix is unchanged
 284  s.sw(TDEST, PAINT); s.go(SRC(3) | DST_B | D32); s.check(TDEST, "b3")
 285  s.sw(TDEST, PAINT); s.go(SRC(3) | DST_C | D32); s.check(TDEST, "c3")
 286  lin_map(s, "b"); s.sw(LDEST, PAINT); s.go(SRC(3) | DST_LB | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "lb3")
 287  s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "live")
 288  t, alive, r = s.run()
 289  for v in (3, 4, 5, 6, 7):
 290      row("src %d" % v, kept(r["f%d" % v]), "paint kept", "S2, tiled A fill, src field %d" % v)
 291  row("src 3 copy", kept(r["copy3"]), "paint kept", "S2's active side: a COPY from src 3")
 292  row("src 3 lin", kept(r["lin3"]), "paint kept", "S2 at a linear destination")
 293  row("src c fill", landed(r["fillc"]), "landed", "ACCEPT: src 2 = MTE_TLB_C, the bound")
 294  row("src c copy", top(r["copyc"]), "0x1a", "ACCEPT: a COPY from TLB_C lands the source's first byte")
 295  row("src 3 b", kept(r["b3"]), "paint kept", "S2 at tiled B, latch SET")
 296  row("src 3 c", kept(r["c3"]), "paint kept", "S2 at tiled C, latch SET")
 297  row("src 3 lin b", kept(r["lb3"]), "paint kept", "S2 at LIN_B, latch SET")
 298  row("src surv", "survived" if r["live"] == "0x%x" % LIVE_VAL else "died", "survived", "ten refused transfers, then RAM")
 299  row("src once", ntext(t, "S2") if alive else "died", 1, "ten refusals, one announcement")
 300  
 301  # ================================================================ S1 / S2 with the latch CLEAR at B, C, LIN_A, LIN_B
 302  #  #564 pass-2 repair (F9).  A CLEAR cell is the FIRST refusal of its site in its session, so each needs a session of
 303  #  its own; one S1 cell and one S2 cell share each session (different latch bits, and S2's refusal is the first S2 of
 304  #  that session).  Tiled A's CLEAR cells are `stip a' and `src 3' above.
 305  def refuse(s, flags, lab, key):
 306      """One refused transfer at destination `lab' (b, c, la, lb), painted first, read back under `key'."""
 307      if lab in ("b", "c"):
 308          s.sw(TDEST, PAINT); s.go(flags | (DST_B if lab == "b" else DST_C) | D32); s.check(TDEST, key)
 309      else:
 310          lin_map(s, lab[1]); s.sw(LDEST, PAINT)
 311          s.go(flags | (DST_LA if lab == "la" else DST_LB) | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, key)
 312  for s1lab, s2lab in (("b", "c"), ("c", "b"), ("la", "lb"), ("lb", "la")):
 313      s = Sess(); tiles(s, a=True, b=True, c=True)
 314      refuse(s, STIPPLE, s1lab, "s1"); refuse(s, SRC(3), s2lab, "s2")
 315      t, alive, r = s.run()
 316      row("stip %s clr" % s1lab, kept(r["s1"]), "paint kept", "S1 at %s, latch CLEAR (first S1 of the session)" % s1lab)
 317      row("src %s clr" % s2lab, kept(r["s2"]), "paint kept", "S2 at %s, latch CLEAR (first S2 of the session)" % s2lab)
 318  
 319  # ================================================================ S3 linear COPY, both labels
 320  s = Sess()
 321  for lab in ("a", "b"):
 322      lin_map(s, lab); s.sw(LDEST, PAINT)
 323      s.go(COPY | (DST_LA if lab == "a" else DST_LB) | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, lab)
 324  s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "live")
 325  t, alive, r = s.run()
 326  row("copy lin a", kept(r["a"]), "paint kept", "S3, LIN_A")
 327  row("copy lin b", kept(r["b"]), "paint kept", "S3, LIN_B")
 328  row("copy surv", "survived" if r["live"] == "0x%x" % LIVE_VAL else "died", "survived", "")
 329  row("copy once", ntext(t, "S3") if alive else "died", 1, "")
 330  
 331  # ================================================================ S4 linear depth != 8: {16,32,64} x both labels
 332  s = Sess()
 333  for lab in ("a", "b"):
 334      lin_map(s, lab)
 335      for dn, dv in (("16", D16), ("32", D32), ("64", D64)):
 336          s.sw(LDEST, PAINT); s.go((DST_LA if lab == "a" else DST_LB) | dv, linear=True, bytemask=0xffffffff)
 337          s.check(LDEST, lab + dn)
 338  s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "live")
 339  t, alive, r = s.run()
 340  for lab in ("a", "b"):
 341      for dn in ("16", "32", "64"):
 342          row("depth %s %s" % (lab, dn), kept(r[lab + dn]), "paint kept", "S4, LIN_%s depth %s" % (lab.upper(), dn))
 343  row("depth surv", "survived" if r["live"] == "0x%x" % LIVE_VAL else "died", "survived", "")
 344  row("depth once", ntext(t, "S4") if alive else "died", 1, "six refusals, one announcement")
 345  
 346  # ================================================================ S5 bytemask: the reset default, in a session that never stores it
 347  s = Sess(); lin_map(s, "a"); s.sw(LDEST, PAINT); s.go(DST_LA | D8, linear=True); s.check(LDEST, "v")
 348  s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "live")
 349  t, alive, r = s.run()
 350  row("mask unwritten", kept(r["v"]), "paint kept", "S5 at BYTEMASK's reset value 0, never stored")
 351  row("mask unw surv", "survived" if r["live"] == "0x%x" % LIVE_VAL else "died", "survived", "")
 352  
 353  # ================================================================ S5 bytemask: edges, LIN_B, and the 32 single-zero masks
 354  s = Sess(); lin_map(s, "a")
 355  for m in (0x0000ffff, 0xfffffffe, 0x7fffffff):
 356      s.sw(LDEST, PAINT); s.go(DST_LA | D8, linear=True, bytemask=m); s.check(LDEST, "m%08x" % m)
 357  s.sw(LDEST, PAINT)
 358  for b in range(32):
 359      s.mte(MTE_BYTEMASK, 0xffffffff ^ (1 << b)); s.sw(MTE_DST1_START, LDST1)
 360  s.check(LDEST, "sweep")
 361  lin_map(s, "b"); s.sw(LDEST, PAINT); s.go(DST_LB | D8, linear=True, bytemask=0x0000ffff); s.check(LDEST, "linb")
 362  s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "live")
 363  t, alive, r = s.run()
 364  for m in (0x0000ffff, 0xfffffffe, 0x7fffffff):
 365      row("mask %08x" % m, kept(r["m%08x" % m]), "paint kept", "S5, LIN_A")
 366  row("mask sweep", kept(r["sweep"]), "paint kept", "S5, all 32 single-zero masks, paint read once at the end")
 367  row("mask lin b", kept(r["linb"]), "paint kept", "S5, LIN_B")
 368  row("mask surv", "survived" if r["live"] == "0x%x" % LIVE_VAL else "died", "survived", "")
 369  row("mask once", ntext(t, "S5") if alive else "died", 1, "thirty-six refusals, one announcement")
 370  
 371  # ================================================================ ACCEPT: what must still land
 372  s = Sess(); tiles(s, a=True)
 373  lin_map(s, "a"); s.sw(LDEST, PAINT); s.go(DST_LA | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "la")
 374  lin_map(s, "b"); s.sw(LDEST, PAINT); s.go(DST_LB | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "lb")
 375  lin_map(s, "a"); s.sw(LDEST, PAINT); s.go(ECC | DST_LA | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "ecc")
 376  s.sw(TDEST, PAINT); s.go(DST_A | D32, bytemask=0x0000ffff); s.check(TDEST, "tmask")
 377  s.sw(TDEST + 4, SRC_WORD); s.sw(TDEST, PAINT); s.go(COPY | DST_A | D32, bytemask=0x0000ffff, src0=SRC_PIX); s.check(TDEST, "tcopy")
 378  tiles(s, a=False, b=True, c=True)               # appended: the existing rows' commands are unchanged
 379  s.sw(TDEST, PAINT); s.go(DST_B | D32, bytemask=0xffffffff); s.check(TDEST, "fb")
 380  s.sw(TDEST, PAINT); s.go(DST_C | D32); s.check(TDEST, "fc")
 381  t, alive, r = s.run()
 382  row("lin fill a", r["la"], "0x44444444", "ACCEPT: LIN_A, depth 8, full mask -- BG's low byte")
 383  row("lin fill b", r["lb"], "0x44444444", "ACCEPT: LIN_B")
 384  row("lin fill ecc", r["ecc"], "0x44444444", "ACCEPT: the PROM's own linear mode 0x11 (DST_ECC)")
 385  row("tile mask", landed(r["tmask"]), "landed", "ACCEPT: tiled fill with BYTEMASK 0x0000ffff")
 386  row("tile copy mask", top(r["tcopy"]), "0x1a", "ACCEPT: tiled COPY with BYTEMASK 0x0000ffff")
 387  row("fill b ok", landed(r["fb"]), "landed", "ACCEPT: a legal tiled fill at B (no S1/S2 growth onto B)")
 388  row("fill c ok", landed(r["fc"]), "landed", "ACCEPT: a legal tiled fill at C")
 389  
 390  # ================================================================ LATCH: an existing bit first, then S1..S5 and S1 again, in one session
 391  s = Sess(); tiles(s, a=True)
 392  s.sw(RE_TLB_A, 0)                                       # a 4-byte store: SGIRE_W_TLBA_LEN, announced once
 393  s.sw(TDEST, PAINT); s.go(STIPPLE | DST_A | D32); s.check(TDEST, "s1")
 394  s.sw(TDEST, PAINT); s.go(SRC(3) | DST_A | D32); s.check(TDEST, "s2")
 395  lin_map(s, "a")
 396  s.sw(LDEST, PAINT); s.go(COPY | DST_LA | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "s3")
 397  s.sw(LDEST, PAINT); s.go(DST_LA | D16, linear=True, bytemask=0xffffffff); s.check(LDEST, "s4")
 398  s.sw(LDEST, PAINT); s.go(DST_LA | D8, linear=True, bytemask=0x0000ffff); s.check(LDEST, "s5")
 399  tiles(s, a=True)
 400  s.sw(TDEST, PAINT); s.go(STIPPLE | DST_A | D32); s.check(TDEST, "s1again")
 401  s.sw(RE_TLB_A, 0)                                       # the existing bit again: must NOT announce a second time
 402  s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "live")
 403  t, alive, r = s.run()
 404  paints = [r[k] for k in ("s1", "s2", "s3", "s4", "s5", "s1again")]
 405  row("latch paint", "all kept" if all(v == P for v in paints) else ("died" if "died" in paints else "written"),
 406      "all kept", "six refusals incl. a repeat of S1 after the latch is set")
 407  row("latch texts", "/".join(str(ntext(t, k)) for k in ("S1", "S2", "S3", "S4", "S5")) if alive else "died",
 408      "1/1/1/1/1", "five distinct sites in one session: five bits, not one")
 409  row("latch old bit", len(re.findall(re.escape(TLBA_LEN_TEXT), t)) if alive else "died", 1,
 410      "SGIRE_W_TLBA_LEN set before the new sites stays set after them")
 411  
 412  # ================================================================ CROSSBIT: every pre-existing bit set FIRST, then S1..S5
 413  #  #564 pass-2 repair (F10).  A new site whose bit is aliased onto a pre-existing one (`SGIRE_W_MTE_STIPPLE = 1 << 10'
 414  #  is SGIRE_W_BADMODE) is silenced only once that bit is set, and no other session here sets bits 1-12.  The priming
 415  #  sequence is the one sgi_re_colourdefault_probe.py's `allbits' rows proved (bits 0-11), plus that probe's colour
 416  #  decline, which sets bit 12.  `xbit primed' counts the thirteen priming announcements, so a priming access that stops
 417  #  firing reds the row instead of leaving a hole; `xbit texts' wants each new site to announce exactly once.
 418  RE_WINDOWS = (0xb5001000, 0xb5001200, 0xb5001400, 0xb5001600, 0xb5001700, 0xb5001780)   # TLB_A..LINEAR_B
 419  DE_BASE, OUTSIDE, TEX_BASE = 0xb5002000, 0xb5001800, 0xb5001600
 420  DE_MODE_DST, DE_DRAWMODE, DE_FG = 0xb5002008, 0xb5002018, 0xb50020d0
 421  DE_XVERTEX_0, DE_XVERTEX_1, DE_PRIM_START = 0xb5002070, 0xb5002074, 0xb5002860
 422  PRIM_RECT, PRIM_BAD = 0x03020000, 0x05020000
 423  MODE_LINB_RGBA, MODE_YCRCB = 0x1620, 0x12f0
 424  def de_put(s, mode):
 425      """One DE pixel PUT (sgi_re_colourdefault_probe.py's setup_put): LIN_A page 0x10, then a 1x1 rectangle."""
 426      s.sd(RE_LIN_A, 0x0000001000000000); s.sw(0xa0010000, PAINT)
 427      for a, v in ((DE_MODE_DST, mode), (DE_DRAWMODE, 0xf8), (DE_FG, 0xaabbccdd), (DE_XVERTEX_0, 0), (DE_XVERTEX_1, 0),
 428                   (DE_PRIM_START, PRIM_RECT)):
 429          s.sw(a, v)
 430  PRIME_LIT = ["for CRIME_RE_%s -- declined." % n for n in ("TLB_A", "TLB_B", "TLB_C", "TEX", "LINEAR_A", "LINEAR_B")] + [
 431      "[ sgi_de: unimplemented len=",                        # bit 6  DE_LEN
 432      "unimplemented write to address 0x1800",               # bit 7  UNMAP_WR
 433      "unimplemented read from address 0x1800",              # bit 8  UNMAP_RD
 434      "UNIMPLEMENTED drawing op",                            # bit 9  PRIM_OP
 435      "unimplemented dst_mode",                              # bit 10 BADMODE
 436      "unimplemented read from CRIME_RE_TEX -- declined.",   # bit 11 TEX_RD
 437      "unimplemented colour type in horrible_getputpixel"]   # bit 12 BADCOLOR
 438  s = Sess()
 439  for w in RE_WINDOWS:
 440      s.sb(w, 0x1)                                        # bits 0-5
 441  s.sb(DE_BASE, 0x1)                                      # bit 6
 442  s.sb(OUTSIDE, 0x1)                                      # bit 7
 443  s.load(OUTSIDE, OP_LW_V0_AT)                            # bit 8
 444  de_put(s, MODE_LINB_RGBA)                               # bit 10
 445  s.sw(DE_PRIM_START, PRIM_BAD)                           # bit 9
 446  s.load(TEX_BASE, OP_LD_V0_AT)                           # bit 11
 447  de_put(s, MODE_YCRCB)                                   # bit 12
 448  tiles(s, a=True)
 449  s.sw(TDEST, PAINT); s.go(STIPPLE | DST_A | D32); s.check(TDEST, "s1")
 450  s.sw(TDEST, PAINT); s.go(SRC(3) | DST_A | D32); s.check(TDEST, "s2")
 451  lin_map(s, "a")
 452  s.sw(LDEST, PAINT); s.go(COPY | DST_LA | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "s3")
 453  s.sw(LDEST, PAINT); s.go(DST_LA | D16, linear=True, bytemask=0xffffffff); s.check(LDEST, "s4")
 454  s.sw(LDEST, PAINT); s.go(DST_LA | D8, linear=True, bytemask=0x0000ffff); s.check(LDEST, "s5")
 455  t, alive, r = s.run()
 456  fired = sum(1 for lit in PRIME_LIT if lit in t)
 457  row("xbit primed", "%i/%i" % (fired, len(PRIME_LIT)) if alive else "died", "%i/%i" % (len(PRIME_LIT), len(PRIME_LIT)),
 458      "all thirteen pre-existing latches PROVEN set before S1..S5")
 459  row("xbit texts", "/".join(str(ntext(t, k)) for k in ("S1", "S2", "S3", "S4", "S5")) if alive else "died",
 460      "1/1/1/1/1", "with bits 0-12 set, each new site still announces once")
 461  
 462  # ================================================================ AFTER a decline: the engine still works and the status reads idle
 463  s = Sess(); tiles(s, a=True)
 464  s.sw(TDEST, PAINT); s.go(STIPPLE | DST_A | D32); s.check(TDEST, "decl")
 465  s.sw(TDEST, PAINT); s.go(DST_A | D32); s.check(TDEST, "fill")
 466  s.check(DE_STATUS, "stat")
 467  t, alive, r = s.run()
 468  row("after fill", landed(r["fill"]), "landed", "a legal fill after a declined one lands")
 469  row("after status", r["stat"], DE_STAT, "CRIME_DE_STATUS after a decline")
 470  
 471  ok = sum(1 for _, k in rows if k)
 472  print("MTEDECL_RESULT=%d/%d" % (ok, len(rows)))
 473  print("MTEDECL_DONE")
```

### 4d. `regress/gate_arm.sh`'s sgi_mte block, whole

```sh
 1473  #  ---- #564 sgirekills (MTE half): do_mte_transfer()'s five refusals of an unsupported transfer parameter --
 1474  #  ---- stipple, a source buffer past MTE_TLB_C, and COPY / depth != 8 / a partial BYTEMASK to a LINEAR
 1475  #  ---- destination -- each DECLINE with a latched announcement, where each used to end the process.  Wired
 1476  #  ---- IN THE SAME COMMIT as the fix.  Measured with one instrument: 8/53 on the pre-fix build (HEAD
 1477  #  ---- 2951694f; only the controls and the five ACCEPT rows green) and 53/53 on the fix
 1478  #  ---- (regress/artifacts/sgirekills/detector_564_20261017/); the pass-2 repair took it to 68 rows
 1479  #  ---- (regress/artifacts/sgirekills/killtable3_564_20261017/).  Modelled on the sgi_re_width_probe block
 1480  #  ---- (find it with `grep -n 'sgi_re_width_probe.py "$PMAX"' gate_arm.sh`), at depth 0 so a sibling
 1481  #  ---- probe's missing sentinel cannot swallow it.
 1482  MTELOG=$LOGDIR/sgi_mte_decline.log
 1483  python3 sgi_mte_decline_probe.py "$PMAX" gate > "$MTELOG" 2>&1 || true
 1484  
 1485  if ! grep -q "MTEDECL_DONE" "$MTELOG"; then
 1486      note "sgi_mte decline probe did not reach its completion sentinel; last lines follow"
 1487      tail -5 "$MTELOG" | sed 's/^/       /'
 1488      check "sgi_mte decline probe completed" "no" "yes"
 1489  else
 1490      grep -E " ok$| FAIL$" "$MTELOG" | sed 's/^/       /'
 1491  
 1492      #  CONTROLS BY NAME: a run whose controls died is an APPARATUS failure, not 50 product failures.
 1493      for c in "live" "devsig" "mode rt"; do
 1494          check "sgi_mte control: $c" "$(count "$MTELOG" "^$c  .*ok$")" "1"
 1495      done
 1496  
 1497      #  PER ROW, ONE LINE.  The probe prints a name of at most 14 characters in a 16-column field, so every
 1498      #  name is followed by TWO spaces and "^<name>  " cannot match a longer name that starts with it.
 1499      for v in "live" "devsig" "mode rt" "stip a" "stip b" "stip c" "stip copy" "stip lin a" "stip lin b" "stip surv" "stip once" "src 3" "src 4" "src 5" "src 6" "src 7" "src 3 copy" "src 3 lin" "src c fill" "src c copy" "src surv" "src once" "copy lin a" "copy lin b" "copy surv" "copy once" "depth a 16" "depth a 32" "depth a 64" "depth b 16" "depth b 32" "depth b 64" "depth surv" "depth once" "mask unwritten" "mask unw surv" "mask 0000ffff" "mask fffffffe" "mask 7fffffff" "mask sweep" "mask lin b" "mask surv" "mask once" "lin fill a" "lin fill b" "lin fill ecc" "tile mask" "tile copy mask" "latch paint" "latch texts" "latch old bit" "after fill" "after status" "src 3 b" "src 3 c" "src 3 lin b" "stip b clr" "src c clr" "stip c clr" "src b clr" "stip la clr" "src lb clr" "stip lb clr" "src la clr" "fill b ok" "fill c ok" "xbit primed" "xbit texts"; do
 1500          check "sgi_mte row: $v" "$(count "$MTELOG" "^$v  .*ok$")" "1"
 1501      done
 1502  
 1503      #  DENOMINATOR PINNED TO A LITERAL, summed arithmetically (count() is plain grep: a `|' would be literal).
 1504      check "sgi_mte rows emitted" \
 1505            "$(( $(count "$MTELOG" " ok$") + $(count "$MTELOG" " FAIL$") ))" "68"
 1506      check "sgi_mte rows green"   "$(count "$MTELOG" " ok$")"   "68"
 1507      check "sgi_mte rows red"     "$(count "$MTELOG" " FAIL$")" "0"
 1508  fi
```

## 5. Kill table 3

### 5a. `PRETABLE3.out` -- written 2026-10-17 21:40:46, before table 3's first log (2026-10-17 22:15:47)

```
PRETABLE3 -- #564 sgirekills (MTE half), the PASS-2 REPAIR.  Written 2026-10-17 BEFORE kill table 3 (its mtime is the
order proof).  Detector regress/sgi_mte_decline_probe.py, md5 8928a02f, 68 rows (53 before the repair); the fix
src/devices/dev_sgi_re.c md5 23fa76aa (1d65cdc1 plus F1's comment correction only -- no executable change).
Mutant list: mutants_564c.py beside this file, 29 mutants, each with its predicted catchers.
The findings and their adjudication: regress/artifacts/sgirekills/pass2_564_20261017/ (Astra, Grok, GLM SWC; Fable 429)
and f2_564_20261017/ (Astra ALL UPHELD, GLM ALL UPHELD, Grok "1 WRONG (F9)" -- the floor upheld, the packet's append
recipe corrected: B and LIN_B mapped inline, every cell repainted, linear cells at depth 8 / full mask / COPY clear).

== 1. SIBLING PARITY
N/A: the repair adds rows, not arms.  The five arms and their parity were PRETABLE.out section 1.

== 2. CLAIM -> ROW (every ADDED or CHANGED sentence asserting an observable consequence)
* dev_sgi_re.c, F1: "On a START-tagged write the register store has already landed in the caller and stays" -- no row
  reads an MTE register after a START; disclosed (probe contract NOT CLAIMED, and PRETABLE.out section 2).
  "a START-tagged READ reaches here too (filed separately)" -- no row drives a START-tagged read; disclosed in the
  contract and filed (mtestartread).  "either way the caller's common tail still answers" -- `after status', the
  `*surv' rows (a write); the read tail has no row (same disclosure).
* probe contract: "S1 and S2 at EVERY destination label whose arm writes guest memory ... each in BOTH latch states"
  -> the 20 cell rows of section 3; "a new site's bit ALIASED onto a pre-existing one" -> `xbit primed' + `xbit
  texts'; "the paint is read ONCE, at its end" (the sweep) -> `mask sweep' (unchanged); the NOT CLAIMED additions
  (source 1, the printed VALUES, an MTE register written by a decline, a START-tagged READ) are explicit no-row
  sentences.

== 3. GUARD FIELD vs BODY FIELD -- the skipped-dispatch cells (2026-09-25 clause, first reuse; fit checked)
S1's and S2's `return' bypasses `switch (dst_tlb)'.  Guest-observable labels: A, B, C (tiled arm writes via
horrible_getputpixel) and LIN_A, LIN_B (memory_rw fill); 3 (TEX), 6 (CLIP), 7 reach `default:', which only prints
(dev_sgi_re.c:1732-1733) -- excluded as host-debug only.  Each repair path tests its OWN latch bit, so the floor is
labels x {CLEAR, SET} per site.  The partition the body induces on each lvalue: d->warned -- one bit per site, tested
as a case (set / clear); dst_tlb -- not read by S1/S2's body, an axis only through the bypassed dispatch.
    cell                 row(s) that hold it
    S1 A   CLEAR         stip a                       S1 A   SET   stip copy; latch paint (s1again)
    S1 B   CLEAR         stip b clr          (new)    S1 B   SET   stip b
    S1 C   CLEAR         stip c clr          (new)    S1 C   SET   stip c
    S1 LA  CLEAR         stip la clr         (new)    S1 LA  SET   stip lin a
    S1 LB  CLEAR         stip lb clr         (new)    S1 LB  SET   stip lin b
    S2 A   CLEAR         src 3; latch paint           S2 A   SET   src 4..7, src 3 copy
    S2 B   CLEAR         src b clr           (new)    S2 B   SET   src 3 b       (new)
    S2 C   CLEAR         src c clr           (new)    S2 C   SET   src 3 c       (new)
    S2 LA  CLEAR         src la clr          (new)    S2 LA  SET   src 3 lin
    S2 LB  CLEAR         src lb clr          (new)    S2 LB  SET   src 3 lin b   (new)
The ACCEPT face at each label (guard false): A (tile mask, after fill, src c fill), LIN_A / LIN_B (lin fill a / b) and,
new, B and C (fill b ok, fill c ok).  The latch-conditioned accept-face variants are DISCLOSED (clause e), not rowed.

== 4. CHANNEL -- per new row, the mutant it is for and the observable that differs under it
    stip/src <lab> clr   the CLEAR-conditioned label exemption at <lab>    the paint at that label is overwritten
    src 3 b / 3 c / 3 lin b   the SET-conditioned exemption at B / C / LB      the paint is overwritten
    fill b ok / fill c ok     S1 or S2 grown to refuse every transfer to B / C  the legal fill does NOT land (paint kept)
    xbit primed          (setup proof) a priming access that stops announcing  fewer than 13 priming texts
    xbit texts           a new site's bit aliased onto a pre-existing one      that site's count reads 0
Every new linear cell runs at depth 8, BYTEMASK 0xffffffff, COPY clear, so S3-S5 cannot hide an escape; every tiled
cell maps its own tile (B and C are mapped where they are first used) and repaints before its transfer -- A, B and C
share one physical page, so an unrepainted cell could red on its neighbour's write.  CHECKED AT WRITING TIME: no new
row's channel is a survival oracle at a refusal-effect site.

== 5. CLAUSE (c) -- the null medium
`null' (/bin/true) in this table: every session dies, every row that reads a value or a survival reds.  Measured, not
claimed, below.

== 6. THE (d) DEPENDS-ON ENUMERATION for the repair, and what table 3 measures
* the 20 latch-conditioned label exemptions (S1, S2) x {A, B, C, LA, LB} x {SET, CLEAR} -- each predicted to red ONLY
  its own cell's row(s), section 3.  A plain label exemption exempts a superset of cells; its detection follows from
  either conditioned variant's and is recorded as that consequence, not as a measurement.
* one alias per new latch bit onto a pre-existing bit no other session sets: STIPPLE -> 10, SRC -> 6, COPY -> 11,
  DEPTH -> 12, BYTEMASK -> 8 -- each predicted to red `xbit texts' only.  Every other (site, pre-existing bit) pair
  -- 60 of them -- is covered BY CONSTRUCTION via `xbit primed' (all 13 set) AND `xbit texts' (each site announced
  once): every writer of d->warned is `|=', so a site whose bit equals a primed one takes its silent branch.  Not
  covered: a compound mutation that also CLEARS warning state.
* the ACCEPT face at B and C: S1 and S2 grown by `|| dst_tlb == B' / `== C' -- each predicted to red `fill b ok' /
  `fill c ok' (and nothing else: the refused transfers stay refused).
* `head' -- HEAD 2951694f's build, clause (a) for the repaired instrument: every row that drives a refused transfer
  dies there; the new rows must all red, the controls stay green.
TABLE 1 (34) and TABLE 2 (2) stand as OLD-INSTRUMENT evidence for the 53 rows they scored: the repair APPENDS -- the
S2 session's new transfers come after its last existing check, the ACCEPT session's after its last, and the other new
rows are new sessions -- so no existing row's command sequence before its read changed.  Aggregate rows CAN change
value under a mutant (`src once' counts the whole session: a missing-suppression mutant now reads 10 where it read 7;
a death in the appended tail reads `died') -- both still red.  This is a source-derived argument, not a re-measurement.
```

### 5b. `mutants_564c.py`, whole

```python
#!/usr/bin/env python3
"""mutants_564c.py <fixed dev_sgi_re.c> <out dir> -- TABLE 3 of #564's kill table, for the pass-2 repair (F9, F10):
  * the 20 LATCH-CONDITIONED LABEL-SWAP variants the 2026-09-25 skipped-dispatch clause enumerates for S1 and S2,
    whose `return' bypasses `switch (dst_tlb)': each exempts ONE destination label in ONE latch state --
    {A, B, C, LIN_A, LIN_B} x {SET, CLEAR} x {S1, S2}.  (A plain label exemption exempts a superset of cells, so
    its detection follows from either conditioned variant's.)  Labels 3 (TEX), 6 (CLIP) and 7 reach `default:',
    which writes nothing, and are excluded as host-debug only;
  * one ALIAS per new latch bit onto a PRE-EXISTING bit no other session sets (F10): STIPPLE -> 10 (BADMODE) and
    COPY -> 11 (TEX_RD), the two the pass-2 seat named, plus SRC -> 6 (DE_LEN), DEPTH -> 12 (BADCOLOR) and
    BYTEMASK -> 8 (UNMAP_RD).  Every other (site, bit) pair is covered BY CONSTRUCTION via the `xbit primed' row;
  * the ACCEPT face at tiled B and C: S1 and S2 grown to refuse every transfer to B, or to C (`fill b ok', `fill c ok').
    The latch-conditioned accept-face variants are disclosed in the probe's contract, not measured.
Each line names its predicted catchers; the table is scored against the repaired instrument."""
import io, os, sys

G1 = 'if (mode & MTE_MODE_STIPPLE) {\n\t\tif (!(d->warned & SGIRE_W_MTE_STIPPLE))'
G2 = 'if (src > MTE_TLB_C) {\n'
DST = "((mode & MTE_MODE_DST_BUF_MASK) >> MTE_DST_TLB_SHIFT)"     # dst_tlb is not yet computed at S1
LAB = (("a", "MTE_TLB_A"), ("b", "MTE_TLB_B"), ("c", "MTE_TLB_C"), ("la", "MTE_TLB_LIN_A"), ("lb", "MTE_TLB_LIN_B"))
#  the rows that hold each (site, label, state) cell in the repaired instrument
CELL = {
    ("s1", "a", "clr"): "stip a",   ("s1", "a", "set"): "stip copy, latch paint (s1again)",
    ("s1", "b", "clr"): "stip b clr", ("s1", "b", "set"): "stip b",
    ("s1", "c", "clr"): "stip c clr", ("s1", "c", "set"): "stip c",
    ("s1", "la", "clr"): "stip la clr", ("s1", "la", "set"): "stip lin a",
    ("s1", "lb", "clr"): "stip lb clr", ("s1", "lb", "set"): "stip lin b",
    ("s2", "a", "clr"): "src 3, latch paint", ("s2", "a", "set"): "src 4, src 5, src 6, src 7, src 3 copy",
    ("s2", "b", "clr"): "src b clr",  ("s2", "b", "set"): "src 3 b",
    ("s2", "c", "clr"): "src c clr",  ("s2", "c", "set"): "src 3 c",
    ("s2", "la", "clr"): "src la clr", ("s2", "la", "set"): "src 3 lin",
    ("s2", "lb", "clr"): "src lb clr", ("s2", "lb", "set"): "src 3 lin b",
}
M = []
for site, guard in (("s1", G1), ("s2", G2)):
    for lab, sym in LAB:
        for st in ("set", "clr"):
            bit = "SGIRE_W_MTE_STIPPLE" if site == "s1" else "SGIRE_W_MTE_SRC"
            latch = "(d->warned & %s)" % bit if st == "set" else "!(d->warned & %s)" % bit
            if site == "s1":
                new = guard.replace("if (mode & MTE_MODE_STIPPLE) {",
                                    "if ((mode & MTE_MODE_STIPPLE) && !(%s == %s && %s)) {" % (DST, sym, latch))
            else:
                new = guard.replace("if (src > MTE_TLB_C) {",
                                    "if (src > MTE_TLB_C && !(dst_tlb == %s && %s)) {" % (sym, latch))
            M.append(("%s%s%s" % (site, lab, st), [(guard, new)], CELL[(site, lab, st)]))
ALIAS = (("xs1b10", "SGIRE_W_MTE_STIPPLE  = 1 << 13,", "1 << 10", "xbit texts"),
         ("xs2b6",  "SGIRE_W_MTE_SRC      = 1 << 14,", "1 << 6",  "xbit texts"),
         ("xs3b11", "SGIRE_W_MTE_COPY     = 1 << 15,", "1 << 11", "xbit texts"),
         ("xs4b12", "SGIRE_W_MTE_DEPTH    = 1 << 16,", "1 << 12", "xbit texts"),
         ("xs5b8",  "SGIRE_W_MTE_BYTEMASK = 1 << 17,", "1 << 8",  "xbit texts"))
for name, line, val, pred in ALIAS:
    M.append((name, [(line, line.rsplit("=", 1)[0] + "= " + val + ",")], pred))
#  the ACCEPT face at tiled B and C (Astra, F2 Q4): a guard grown to refuse every transfer to ONE label
for lab, sym in (("b", "MTE_TLB_B"), ("c", "MTE_TLB_C")):
    M.append(("s1g" + lab, [(G1, G1.replace("if (mode & MTE_MODE_STIPPLE) {",
                                             "if ((mode & MTE_MODE_STIPPLE) || %s == %s) {" % (DST, sym)))],
              "fill %s ok" % lab))
    M.append(("s2g" + lab, [(G2, G2.replace("if (src > MTE_TLB_C) {",
                                             "if (src > MTE_TLB_C || dst_tlb == %s) {" % sym))],
              "fill %s ok" % lab))

def main():
    src, out = sys.argv[1], sys.argv[2]
    t = io.open(src, encoding="utf-8", newline="").read()
    os.makedirs(out, exist_ok=True)
    for name, edits, pred in M:
        m = t
        for a, b in edits:
            n = m.count(a)
            if n != 1:
                print("MUTANT ANCHOR FAIL %s: %d occurrences" % (name, n)); sys.exit(9)
            m = m.replace(a, b)
        io.open(os.path.join(out, name + ".c"), "w", encoding="utf-8", newline="").write(m)
        print("%-9s predicted: %s" % (name, pred))
    print("mutants written: %d" % len(M))

if __name__ == "__main__":
    main()
```

### 5c. `KILLTABLE3.txt`

```
base      68/68
null      0/68
head      10/68
base all-green, null all-red: table valid

s1aset    66/68 KILLED   caught by: stip copy, latch paint
                         predicted: stip copy, latch paint (s1again)
s1aclr    64/68 KILLED   caught by: stip a, latch paint, latch texts, xbit texts
                         predicted: stip a
s1bset    67/68 KILLED   caught by: stip b
                         predicted: stip b
s1bclr    67/68 KILLED   caught by: stip b clr
                         predicted: stip b clr
s1cset    67/68 KILLED   caught by: stip c
                         predicted: stip c
s1cclr    67/68 KILLED   caught by: stip c clr
                         predicted: stip c clr
s1laset   67/68 KILLED   caught by: stip lin a
                         predicted: stip lin a
s1laclr   67/68 KILLED   caught by: stip la clr
                         predicted: stip la clr
s1lbset   67/68 KILLED   caught by: stip lin b
                         predicted: stip lin b
s1lbclr   67/68 KILLED   caught by: stip lb clr
                         predicted: stip lb clr
s2aset    63/68 KILLED   caught by: src 4, src 5, src 6, src 7, src 3 copy
                         predicted: src 4, src 5, src 6, src 7, src 3 copy
s2aclr    59/68 KILLED   caught by: src 3, src 4, src 5, src 6, src 7, src 3 copy, latch paint, latch texts, xbit texts
                         predicted: src 3, latch paint
s2bset    67/68 KILLED   caught by: src 3 b
                         predicted: src 3 b
s2bclr    67/68 KILLED   caught by: src b clr
                         predicted: src b clr
s2cset    67/68 KILLED   caught by: src 3 c
                         predicted: src 3 c
s2cclr    67/68 KILLED   caught by: src c clr
                         predicted: src c clr
s2laset   67/68 KILLED   caught by: src 3 lin
                         predicted: src 3 lin
s2laclr   67/68 KILLED   caught by: src la clr
                         predicted: src la clr
s2lbset   67/68 KILLED   caught by: src 3 lin b
                         predicted: src 3 lin b
s2lbclr   67/68 KILLED   caught by: src lb clr
                         predicted: src lb clr
xs1b10    67/68 KILLED   caught by: xbit texts
                         predicted: xbit texts
xs2b6     67/68 KILLED   caught by: xbit texts
                         predicted: xbit texts
xs3b11    67/68 KILLED   caught by: xbit texts
                         predicted: xbit texts
xs4b12    67/68 KILLED   caught by: xbit texts
                         predicted: xbit texts
xs5b8     67/68 KILLED   caught by: xbit texts
                         predicted: xbit texts
s1gb      67/68 KILLED   caught by: fill b ok
                         predicted: fill b ok
s2gb      67/68 KILLED   caught by: fill b ok
                         predicted: fill b ok
s1gc      67/68 KILLED   caught by: fill c ok
                         predicted: fill c ok
s2gc      67/68 KILLED   caught by: fill c ok
                         predicted: fill c ok

KILL TABLE 3: 29/29 killed
```

### 5d. Per row: its HEAD 2951694f value and the table-3 mutants that turned it red (computed from raw3/)

```
row              new  HEAD 2951694f          table-3 mutants that turned it red
live                  0x5a5a5a5a ok          -
devsig                0x1e000000 ok          -
mode rt               0x600 ok               -
stip a                died FAIL              s1aclr
stip b                died FAIL              s1bset
stip c                died FAIL              s1cset
stip copy             died FAIL              s1aset
stip lin a            died FAIL              s1laset
stip lin b            died FAIL              s1lbset
stip surv             died FAIL              -
stip once             died FAIL              -
src 3                 died FAIL              s2aclr
src 4                 died FAIL              s2aclr, s2aset
src 5                 died FAIL              s2aclr, s2aset
src 6                 died FAIL              s2aclr, s2aset
src 7                 died FAIL              s2aclr, s2aset
src 3 copy            died FAIL              s2aclr, s2aset
src 3 lin             died FAIL              s2laset
src c fill            died FAIL              -
src c copy            died FAIL              -
src 3 b          NEW  died FAIL              s2bset
src 3 c          NEW  died FAIL              s2cset
src 3 lin b      NEW  died FAIL              s2lbset
src surv              died FAIL              -
src once              died FAIL              -
stip b clr       NEW  died FAIL              s1bclr
src c clr        NEW  died FAIL              s2cclr
stip c clr       NEW  died FAIL              s1cclr
src b clr        NEW  died FAIL              s2bclr
stip la clr      NEW  died FAIL              s1laclr
src lb clr       NEW  died FAIL              s2lbclr
stip lb clr      NEW  died FAIL              s1lbclr
src la clr       NEW  died FAIL              s2laclr
copy lin a            died FAIL              -
copy lin b            died FAIL              -
copy surv             died FAIL              -
copy once             died FAIL              -
depth a 16            died FAIL              -
depth a 32            died FAIL              -
depth a 64            died FAIL              -
depth b 16            died FAIL              -
depth b 32            died FAIL              -
depth b 64            died FAIL              -
depth surv            died FAIL              -
depth once            died FAIL              -
mask unwritten        died FAIL              -
mask unw surv         died FAIL              -
mask 0000ffff         died FAIL              -
mask fffffffe         died FAIL              -
mask 7fffffff         died FAIL              -
mask sweep            died FAIL              -
mask lin b            died FAIL              -
mask surv             died FAIL              -
mask once             died FAIL              -
lin fill a            0x44444444 ok          -
lin fill b            0x44444444 ok          -
lin fill ecc          0x44444444 ok          -
tile mask             landed ok              -
tile copy mask        0x1a ok                -
fill b ok        NEW  landed ok              s1gb, s2gb
fill c ok        NEW  landed ok              s1gc, s2gc
latch paint           died FAIL              s1aclr, s1aset, s2aclr
latch texts           died FAIL              s1aclr, s2aclr
latch old bit         died FAIL              -
xbit primed      NEW  died FAIL              -
xbit texts       NEW  died FAIL              s1aclr, s2aclr, xs1b10, xs2b6, xs3b11, xs4b12, xs5b8
after fill            died FAIL              -
after status          died FAIL              -
new rows emitted: 15 of 15
new rows red under no table-3 mutant: xbit primed
```

## 6. `PRETABLE_ERRATA.txt` (corrections to table 1's PRETABLE.out), whole

```
PRETABLE_ERRATA -- corrections to PRETABLE.out beside this file, written 2026-10-17 AFTER kill tables 1 and 2 from the
pass-2 panel (pass2_564_20261017/: GPT-6 Astra, Grok 4.7, GLM 5.3) and the shared-findings pass (f2_564_20261017/, all
three upholding).  PRETABLE.out itself is NOT edited: its mtime, before table 1's first log, is the order proof.  Each
entry quotes the text it corrects.

1. Section 3: "0 and 1 are SAMPLED by every other row (src 0)".  Source 1 is never driven -- every mode word the probe
   builds carries SRC(0), SRC(2) or SRC(3..7).  A guard grown to refuse source 1 alone (`|| src == 1') keeps every row
   green; disposed as clause-(e) disclosure (an equality at an interior accept value the body never tests as a case;
   the compare's two edges, 2 and 3, are rowed), and the repaired probe's contract names it.

2. Section 4: `after status` "cannot vary under any mutant in the list ... only a mutant of sgi_de_status (out of scope)
   could red it".  Measured otherwise: `b1` reddens it (KILLTABLE.txt -- the stipple exit ends the session before the
   status read, which then reads `died').  It is a control that also catches session death; the claim was wrong.

3. Section 4: `after fill` "(no mutant rowed for that shape -- disclosed)".  `s5hoist' is that shape and reddened it
   (KILLTABLE.txt, unpredicted).  The disclosure was wrong; the row has a measured catcher.

4. Section 4: a `d2' escape of `src 3 copy' "lands the source byte".  Source 3 is MTE_TLB_TEX; horrible_getputpixel's
   tlb_mode switch reaches its default and returns without writing *color, so the COPY's PUT stores BG (0x11223344),
   not the source byte -- still not the paint, so `kept()' still reds.  Mechanism corrected; the row's validity stands.

5. Section 3 / the S2 rows: "S2 at B/C ... OWED: none".  Wrong under the 2026-09-25 skipped-dispatch label clause: S2's
   (and S1's) `return' bypasses `switch (dst_tlb)', so the floor is {A, B, C, LIN_A, LIN_B} x {latch CLEAR, SET} per
   site -- 20 cells, of which S1 held 6 and S2 held 3.  The 11 empty cells were S1 at B/C/LIN_A/LIN_B with the latch
   CLEAR, and S2 at B/C/LIN_A/LIN_B CLEAR plus B/C/LIN_B SET.  Grok's `if (src > MTE_TLB_C && dst_tlb != MTE_TLB_B)'
   kept all 53 rows green.  Repaired by the pass-2 repair (killtable3_564_20261017/PRETABLE3.out section 3 maps every
   cell to its row) and measured in kill table 3.

6. Section 3 (the latch writers census): the census counted the writers of d->warned but prescribed no row that SETS
   the pre-existing bits before the new sites run.  Only SGIRE_W_TLBA_LEN was ever set; `SGIRE_W_MTE_STIPPLE = 1 << 10'
   (an alias of SGIRE_W_BADMODE) kept all 53 rows green (Grok).  The `#490' lesson -- "who else writes this field, and
   can they set my bit?" -- applied.  Repaired by the `xbit primed' / `xbit texts' rows.

7. Channel split, recorded for clarity (Grok, F11): the `*surv' rows and `after status' separate exit(1) from a return
   -- their catchers are the b-mutants -- and stay green under the d-mutants (return removed, the transfer runs), which
   the paint rows catch.  No change.

8. Wording (Grok, F5): "CRIME_DE_STATUS is the constant 0x1e000000" -- CRIME_DE_STATUS is the OFFSET 0x4000; the word
   the device answers there is CRIME_DE_IDLE | SETUP_IDLE | PIXPIPE_IDLE | MTE_IDLE = 0x1e000000.  The probe's expected
   word is right.
```


## 7. Questions

Answer in this order, each with its number.  Facts you checked carry `path:line` or a quoted line.

**Q1 -- PREMISE AUDIT OF THE REPAIR.  Test these; do not ratify them:**
  1. every one of the 20 label x latch cells is held by the row PRETABLE3 section 3 names, and each CLEAR cell really
     is the FIRST refusal of its site in its session (no earlier refusal of that site in the same session);
  2. every new cell's transfer would WRITE if its guard were exempted -- the tile it targets is mapped, the paint is
     repainted immediately before, and a linear cell runs at depth 8, BYTEMASK 0xffffffff, COPY clear;
  3. the crossbit session sets all 13 pre-existing bits BEFORE S1..S5, and `xbit primed` proves each with a distinct
     announcement text;
  4. the repair only APPENDS -- no existing row's commands before its read changed -- and the gate pins exactly the
     68 names the probe emits, both denominators 68.

**Q2 -- THE FLOOR QUESTION, ASKED OF THE SHIPPED COMPOSITE.**  Against the fixed `do_mte_transfer()` and the latch enum:
is there any mutant in the (d) DEPENDS-ON enumeration (the predicates dominating the five edited sites, walked only to
the enclosing function, with the skipped-dispatch label cells and the latch states) under which ALL 68 rows stay green?
Name it and the row you expect to stay green -- or answer zero WITH the cells and shapes you swept.

**Q3 -- ROW VALIDITY OF THE NEW ROWS.**  Is any new row's observable unable to differ under the mutant PRETABLE3
section 4 names for it?  Does pairing an S1-CLEAR and an S2-CLEAR cell in one session confound either?

**Q4 -- RECORDS.**  Every ADDED or CHANGED sentence (the comment, the contract, PRETABLE3, the errata) that asserts an
observable consequence: true of the code, and carried by a row or by an explicit no-row sentence?

If, while verifying a claim, you found something ELSE -- say so.

Format: open with your token, then ONE line `VERDICT: CLOSE / SHIP WITH CHANGES (<n>) / DO NOT SHIP (<one line>)`, then
Q1-Q4.
