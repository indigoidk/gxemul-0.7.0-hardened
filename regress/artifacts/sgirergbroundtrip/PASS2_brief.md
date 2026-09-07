# PANEL PASS 2 — `#505` sgirergbroundtrip, on the real diff

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Where I state something as fact, ask whether it is
true. **Pass 1 of this very round refuted my central premise** — I claimed the GET arm was wrong on
two grounds and four seats showed one was circular and the other neutralised. They were right. So
this brief's premises have already been wrong once today; assume they can be again.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies of GXemul sit
under the project root and are NOT this fork.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/` AND `GXEMUL-SEC/regress/*.py`.** Do not read
`GXEMUL-SEC/regress/artifacts/` or `GXEMUL-SEC/tools/pipeline/ledger.json`.

**VERDICT LINE FIRST.**

---

## §C — SETTLED PREMISES, re-inlined so nobody spends an answer re-deriving them

**S1 — THE DEFECT.** `horrible_getputpixel()`'s RGB PUT wrote the three channels at `buf[0..2]` and
an explicit pad at `buf[3]`; its RGB GET read `buf[1..3]`. RGB was the only 32-bit colour mode in the
file failing its own round trip.

**S2 — WHY THE *GET* IS THE WRONG ARM, settled on pass 1 and NOT by the argument I first gave.**
My original grounds were refuted as circular. The surviving warrant comes from a **different device**:
`dev_sgi_gbe.c`'s scanout reads the same tile memory back for display as
`(buf[i]<<24)+(buf[i+1]<<16)+(buf[i+2]<<8)+buf[i+3]`, and `CRMFB_MODE_TYP_RGB8` — commented in-tree
as *"Used by NetBSD's X11 server"* — takes R, G and B from bits 31..24, 23..16 and 15..8. **Byte 0
is R and byte 3 is unused.** The pad sits at `buf[3]` because the *consumer* ignores `buf[3]`, which
is what makes the warrant independent of either arm under test.

A pass-1 seat added the other half: **RGBA and ABGR write identical memory bytes `[R,G,B,A]`** and
differ only in register word order, so all three 4-byte PUT arms agree on the container and the RGB
GET is the lone outlier.

**S3 — THE POST-FIX VALUE IS NOT THE SOURCE VALUE.** RGB carries three channels, so a corrected read
of `0xaabbccdd` yields **`0xaabbcc00`**. My pre-panel oracle pinned `0xaabbccdd` and would have
failed a correct fix; four seats named `0xaabbcc00` independently. The oracle was re-pinned **before**
the code changed and the committed build re-measured RED under the new expectation.

**S4 — MEASURED.** Pre-fix `4/6`, post-fix `8/8`, same script, on an unmodified `-E sgi -e ip32`,
with a liveness control, a device-signature control and a sibling accept control (`copy lin_a`, an
RGBA source through the same helper) green throughout.

**S5 — TWO KILL TABLES. Table 1 found a floor breach in my own detector.**

| mutant | table 1 (6 rows) | table 2 (8 rows) |
|---|---|---|
| base | 6/6 | 8/8 |
| `M1_verbatim` (clause b) | 4/6 | 4/8 |
| `M2_off1` | 5/6 | 5/8 |
| `M3_pad` (returns the source word) | 5/6 | 6/8 |
| `M4_or` (`+`→`|`) | 6/6 | 8/8 |
| `M5_rev` | 5/6 | 5/8 |
| `M6_cond` (clause d, exempts bufdepth 4) | **6/6 SWEEP** | **7/8** |
| `M7_cond8` (the mirror, exempts bufdepth 8) | — | **7/8** |
| `M8_put` (corrupts the RGB PUT arm) | — | **7/8** |
| null medium | 1/6 | 1/8 |

`M6_cond` kept the guard and conditioned the repair on `bufdepth == 4` — and **every session then
used `BUFDEPTH_32`, so bufdepth was 4 in all of them and the mutant's fix branch was the only one the
detector executed.** Repaired in-round (L2) by `rgb depth64`, a session at `BUFDEPTH_64`. `M7_cond8`
was then built specifically to test whether I had repaired only the cell the mutant named; it dies.

**S6 — `M4_or` IS AN EQUIVALENT MUTANT.** The three byte fields are disjoint (bits 24-31, 16-23,
8-15), so `+`, `|` and `^` compute the same value — enumerated over 80 byte triples with zero
disagreements, and its row values are byte-identical to base. It is unkillable by construction, not a
coverage hole.

## THE PRODUCT DIFF, inlined verbatim

```diff
diff --git a/src/devices/dev_sgi_re.c b/src/devices/dev_sgi_re.c
index 2a81d79..b3239b4 100644
--- a/src/devices/dev_sgi_re.c
+++ b/src/devices/dev_sgi_re.c
@@ -324,7 +324,30 @@ void horrible_getputpixel(int put, struct cpu* cpu, struct sgi_re_data* d,
 			*color = buf[0];
 			break;
 		case DE_MODE_TYPE_RGB:
-			*color = (buf[1] << 24) + (buf[2] << 16) + (buf[3] << 8);
+			/*  #505: this read buf[1..3] while the PUT arm above
+			    writes the three channels at buf[0..2] and an
+			    explicit pad at buf[3] -- so an RGB pixel did not
+			    survive its own round trip, shifting one byte left
+			    with a zero fill on every RGB source read.
+
+			    The PUT arm is the authoritative one, and the
+			    warrant is OUTSIDE this function: dev_sgi_gbe.c's
+			    scanout reads the same tile memory back for display
+			    as (buf[0]<<24)+(buf[1]<<16)+(buf[2]<<8)+buf[3],
+			    then CRMFB_MODE_TYP_RGB8 takes R,G,B from bits
+			    31..24, 23..16 and 15..8 -- byte 0 is R and byte 3
+			    is UNUSED.  So the pad sits at buf[3] because the
+			    consumer ignores buf[3], not because PUT writes a
+			    zero there; that is what makes this non-circular.
+			    The RGBA and ABGR PUT arms independently agree --
+			    both lay [R,G,B,x] in memory despite opposite
+			    register word orders -- which leaves this GET the
+			    lone container outlier among the 32-bit arms.
+
+			    The low byte stays ZERO on purpose: RGB carries
+			    three channels, so a corrected read of 0xaabbccdd
+			    yields 0xaabbcc00, NOT the source word.  */
+			*color = (buf[0] << 24) + (buf[1] << 16) + (buf[2] << 8);
 			break;
 		case DE_MODE_TYPE_RGBA:
 			*color = (buf[0] << 24) + (buf[1] << 16) + (buf[2] << 8) + buf[3];
```

## THE DETECTOR, its eight rows as shipped

```python
261:row("live", printed(t, "v0") if alive else "died", "0x%x" % LIVE_VAL,
266:row("devsig", printed(t, "v0") if alive else "died", DE_STAT,
275:row("copy lin_a", printed(t, "v0") if alive else "died", "0x%x" % SRC_VAL,
296:row("rgb chan", got_rgb, "0x%x" % RGB_FIXED,
303:row("rgb not corrupt", got_rgb, "0x%x" % RGB_CORRUPT,
306:row("rgb alive", "alive" if alive else "died", "alive",
331:row("rgb samemode", got_same, "0x%x" % RGB_FIXED,
363:row("rgb depth64", got_d64, "0x%x" % RGB_FIXED,
```

## THE GATE BLOCK, inlined

```diff
diff --git a/regress/gate_arm.sh b/regress/gate_arm.sh
index 9658468..9dfcc16 100644
--- a/regress/gate_arm.sh
+++ b/regress/gate_arm.sh
@@ -1293,6 +1293,54 @@ else
     check "sgi_re randompixel rows red"   "$(count "$RANDLOG" " FAIL$")" "0"
 fi
 
+#  ------------------------------------------------------------ #505 sgirergbroundtrip
+#  horrible_getputpixel()'s RGB GET read buf[1..3] while its RGB PUT writes the three channels at
+#  buf[0..2] and an explicit pad at buf[3] -- so an RGB pixel did not survive its own round trip and
+#  the red channel was dropped.  RGB was the ONLY 32-bit colour mode in the file failing this way.
+#
+#  THE ARM WAS CHOSEN ON EVIDENCE FROM A DIFFERENT DEVICE, which is what makes the warrant
+#  non-circular: dev_sgi_gbe.c's scanout reads the same tile memory back as
+#  (buf[0]<<24)+(buf[1]<<16)+(buf[2]<<8)+buf[3], and CRMFB_MODE_TYP_RGB8 takes R,G,B from bits
+#  31..24 / 23..16 / 15..8 -- byte 0 is R and byte 3 is UNUSED.  The pad sits at buf[3] because the
+#  CONSUMER ignores buf[3], not because PUT writes a zero there.
+#
+#  `rgb depth64' IS NOT DECORATION -- IT CLOSES A MEASURED CLAUSE-(d) FLOOR BREACH.  The first kill
+#  table's M6_cond (guard kept, repair conditioned on `bufdepth == 4') scored a CLEAN SWEEP 6/6,
+#  because every session then used BUFDEPTH_32 and the mutant's fix branch was the only one the
+#  detector ever executed.  Its mirror M7_cond8 (exempting bufdepth 8 instead) also dies, so the
+#  WIDTH AXIS is closed rather than the one cell the mutant happened to use.
+#
+#  `rgb samemode' reaches the RGB *PUT* arm, which no other row executes -- every other session is
+#  RGB->RGBA.  Measured, not assumed: M8_put corrupts that arm alone and reds exactly this row.
+RGBLOG=$LOGDIR/sgi_re_rgb.log
+python3 sgi_re_rgb_probe.py "$PMAX" gate > "$RGBLOG" 2>&1 || true
+
+if ! grep -q "SGIRGB_DONE" "$RGBLOG"; then
+    check "sgi_re rgb probe completed" "no" "yes"
+else
+    check "sgi_re rgb probe completed" "yes" "yes"
+    check "sgi_re rgb witness verdict" "$(count "$RGBLOG" '^SGIRGB_WITNESS=PASS$')" "1"
+    #  TWO SPACES AFTER $v, NOT ONE -- the sibling blocks above were both bitten by the one-space
+    #  form, in both of its directions.  Pre-flighted mechanically for this row set before the gate
+    #  ever ran: no name is a prefix of another, and every pattern matches exactly one rendered row.
+    #
+    #  The probe prints names with "%-16s" plus an explicit space, so a name of N chars is followed
+    #  by (16-N)+1 spaces.  The longest here is `rgb not corrupt' at 15, leaving exactly two -- ONE
+    #  CHARACTER of margin.  A name of 16 or more makes the two-space pattern UNSATISFIABLE and the
+    #  check silently stops testing anything while staying green.  If a name must grow past 15,
+    #  widen the probe's "%-16s" in the same diff.
+    for v in "live" "devsig" "copy lin_a" "rgb chan" "rgb not corrupt" "rgb alive" "rgb samemode" "rgb depth64"; do
+        check "sgi_re rgb row: $v" "$(count "$RGBLOG" "^$v  .*ok$")" "1"
+    done
+
+    #  DENOMINATOR, SUMMED ARITHMETICALLY: a row that stops being emitted at all is otherwise
+    #  invisible -- its named check goes 0, but so does a check for a row that never existed.
+    check "sgi_re rgb rows emitted" \
+          "$(( $(count "$RGBLOG" " ok$") + $(count "$RGBLOG" " FAIL$") ))" "8"
+    check "sgi_re rgb rows green" "$(count "$RGBLOG" " ok$")"   "8"
+    check "sgi_re rgb rows red"   "$(count "$RGBLOG" " FAIL$")" "0"
+fi
+
 #  ------------------------------------------------------------ #500 sgideprimop
 #  draw_primitive()'s default arm ended the host on a guest-written drawing op.
 #  Now a latched decline.  The detector is its OWN probe rather than rows bolted
```

---

## The questions

**Q1 — THE PREMISE AUDIT.** Every claim in §C is stated as settled. **Which of them is wrong?** The
one I most want challenged is S2: the scanout warrant. It rests on a 32-bit path in `dev_sgi_gbe.c`
whose `color_mode` is a **GBE** register (`CRMFB_MODE_TYP_*`), while the arm I edited switches on a
**DE** register (`DE_MODE_TYPE_*`). Those are different registers. **Does the argument actually
close, or does it need a guest to have programmed both consistently — and if so, is that an
assumption I have smuggled in?**

**Q2 — WHAT IS THE SMALLEST EDIT THAT BREAKS THIS AND STILL PASSES?** Name the row you expect to stay
green. I am specifically after the clause-(d) family: predicates the fix depends on, weakened to the
least-restrictive form that still reads like the corrected code. **Table 2 already covers the WIDTH
axis in both directions** (`M6_cond`, `M7_cond8`) — so tell me which *other* axis is unpinned. The
guarded body reads `buf[0..2]`, `bufdepth`, `color_mode`, `tileptr` and `ofs`; the guard reads
`mode & DE_MODE_TYPE_MASK`.

**Q3 — THE ASK-AGAIN.** The table is clean. **Give me one more mutant.** This is capped at a single
ask per detector per round, and anything found is disposed of individually under L1–L4 — a floor
breach among the findings is still L2 and still repaired in-round, because the cap counts ASKS and
never FINDINGS.

**Q4 — IS THE DETECTOR'S CONTRACT HONEST?** It claims to catch edits that move RGB channel bytes, at
transfer widths 4 and 8, in both the GET and PUT directions. **What does it NOT catch that a reader
would assume it does?** Clause (e) says a detector that names its limits is falsifiable and one
claiming completeness is not — so I would rather add a disclosure than discover a gap.

**Q5 — THE ROW SET.** Eight rows: three controls (`live`, `devsig`, `copy lin_a`), and five on the
defect (`rgb chan`, `rgb not corrupt`, `rgb alive`, `rgb samemode`, `rgb depth64`). **Is any of them
vacuous — able to stay green under the mutant it exists to catch?** For each, its channel is the
destination word read back through a guest load, except `rgb alive` (process survival) and `devsig`
(a device register value RAM would not produce).

**Q6 — THE GATE BLOCK.** It greps row names with **two** spaces, because the probe pads with `%-16s`
plus one explicit space and the longest name is 15 characters — one character of margin. **Is there a
failure mode in that block I have not defended against?** The two known ones are a name matching two
rows (one-space form) and a name ≥ 16 characters making the pattern unsatisfiable so the check goes
silently green.

## What I am not asking

Do not run anything and do not rewrite the fix. This is a review of a diff that is already measured.

**If, while verifying a claim, you found something ELSE — say so.**
