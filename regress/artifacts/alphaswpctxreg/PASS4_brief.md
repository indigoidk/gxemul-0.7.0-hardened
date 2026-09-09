# PASS 4 on the `#514` pass-3 repair — does the chain close now?

**VERDICT LINE FIRST.**  **The tree is `GXEMUL-SEC/src/`.**

Pass 3 measured two apparatus false passes and I repaired both. **A repair made in response to a
pass owes its own pass**, and this chain closes on the first pass finding **zero floor breaches**
— a bare zero does not close it; the zero must carry its denominator.

## What pass 3 found and what was done

* **A regression I introduced in the pass-2 repair:** scoring `a0 != C` passed a MISSING
  observation, because `"absent" != "0x1000000"`. Measured 3/4 before, 5/5 after.
* **The same row was still architecturally wrong:** UNPREDICTABLE does not imply `a0 != C`; an
  implementation that also copies the result into a0 is permitted and scored 4/5.
* **Three parser escapes:** a `trace: print v0` line could SUBSTITUTE for a missing response so the
  count still read 2; `sprint v0` matched as a command; `0x1000000: diagnostic` matched as a value.

**REPAIRED:** observations are ANCHORED to their prompt; `v0_final` is positional with exactly two
required; and `a0 land` became `a0 obs`, scoring APPARATUS INTEGRITY only, with the value printed
as diagnostic.

**MEASURED, not asserted** — `ATTACK_20260908.out` runs the SHIPPED regex, extracted from the probe
file rather than retyped, against all three attacks plus both genuine shapes: **5/5**. Three build
states: FIXED 5/5, PREFIX 4/5 failing `v0 ctx` alone, correct-but-clobbers-a0 5/5.

## The repair diff (7 hunk(s), complete)

```diff
diff --git a/regress/alpha_swpctx_v0_probe.py b/regress/alpha_swpctx_v0_probe.py
index a23f87e..af746f5 100644
--- a/regress/alpha_swpctx_v0_probe.py
+++ b/regress/alpha_swpctx_v0_probe.py
@@ -35,12 +35,19 @@ THE CONTRACT -- what this probe is designed to catch, and what it deliberately i
 CAUGHT: the shipped defect (v0 never written); any repair that returns the NEW context instead
 of the old; and any repair that publishes the OLD context into a0.  NOT CAUGHT, and disclosed
 rather than discovered later: this probe does NOT assert that the new context was actually
-INSTALLED.  An edit leaving `r[ALPHA_V0] = ctx' correct while breaking the subsequent
-load-new-context block would produce v0 == C and a0 == N and score 4/4.  Raised independently
-by deepseek and kimi on the pass-2 panel; filed as coverage debt rather than fixed here,
-because it is a different part of the handler from the fix's own repair and so is not a
-clause-(d) breach.  The row that would close it: a THIRD swpctx call, which should return N as
-its old context.
+INSTALLED.  Raised independently by deepseek and kimi on the pass-2 panel; filed as coverage
+debt rather than fixed here, because it is a different part of the handler from the fix's own
+repair and so is not a clause-(d) breach.  The row that would close it: a THIRD swpctx call,
+which should return N as its old context.
+
+*** AND THE HOLE AS FIRST WRITTEN WAS OVERSTATED, which kimi caught on the NEXT pass. ***  It
+said "an edit breaking the subsequent load-new-context block would score full marks".  That is
+FALSE of a WHOLESALE break, because `cpu->cd.alpha.ctx = a0;' is the FIRST statement inside
+that block: delete the block and `ctx' never advances, so call 2 publishes the STALE context
+and `v0 ctx' REDS.  **Only a PARTIAL break that spares the `ctx = a0' bookkeeping -- killing,
+say, the PCB field loads alone -- sweeps clean.**  Source-derived from the block's own layout,
+not measured.  *A disclosure that overstates its hole is a wrong record in the direction that
+looks humble, which is why it survived a pass.*
 
 ALSO NOT CAUGHT, named by grok on the pass-2 panel: a product edit that HARDCODES the planted
 value -- `cpu->cd.alpha.r[ALPHA_V0] = 0x01000000;' -- scores 4/4 here.  Filed rather than chased,
@@ -48,6 +55,11 @@ and the reason is the bound: the contract is "the OLD context in v0", the plante
 context, and rowing every RHS that happens to equal C for this one pair is the unbounded shape.
 The hole is NAMED so a later escape is "outside the contract" rather than a surprise.
 
+THIS PROBE DOES NOT SCORE a0's VALUE AT ALL.  `a0 obs' scores only that the observation was
+MADE; the value is printed as diagnostic.  Two measured findings forced that: scoring `a0 != C'
+passed a MISSING observation, and it also failed a PERMITTED implementation that copies the
+result into a0 as well.  The defect is caught by `v0 ctx' alone.
+
 THIS PROBE DOES NOT PIN a0's VALUE ON A CORRECT BUILD.  The architecture marks a0
 UNPREDICTABLE after the call; only the negative claim -- a0 does not receive the old context --
 is owed.  See `a0 land' below for the measurement that established this.
@@ -152,9 +164,27 @@ def session(cmds, settle=1.6, spin=2.2):
         pass
     return buf.replace("\r", ""), alive
 
+#  *** THE LOOSE FORM OF THIS REGEX PRODUCED THREE MEASURED CLEAN SWEEPS, found by a seat that
+#  exercised the scorer against 31 SYNTHETIC TRANSCRIPTS rather than reading it. ***  It was
+#  `print\s+REG\s*\n\s*(0x..)' with `re.search', and it accepted all of:
+#
+#      "trace: print v0\n0x1000000"      a TRACE LINE, not a response -- and it can SUBSTITUTE
+#                                        for a genuinely missing one, so the count still says 2
+#      "sprint v0\n0x1000000"            `sprint' matched because nothing anchored the word
+#      "0x1000000: diagnostic"           a value with trailing text
+#
+#  Anchoring on the PROMPT and requiring the value to be the whole line rejects all three: a real
+#  response is always `GXemul> print <reg>' followed by a line that is exactly a hex number.
+RESP = r"^GXemul> print +%s *\n *(0x[0-9a-f]+) *$"
+
+def responses(t, reg):
+    """Every genuine `print <reg>' response, in order.  Anchored, so a trace line or a
+       lookalike command cannot supply one."""
+    return re.findall(RESP % reg, t, re.M)
+
 def printed(t, reg):
-    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
-    return "absent" if not m else "0x%x" % int(m.group(1), 16)
+    r = responses(t, reg)
+    return "absent" if not r else "0x%x" % int(r[0], 16)
 
 print("alpha_swpctx_v0_probe -- binary=%s label=%s machine=%s" % (BIN, LABEL, MACH))
 print("%-14s %-22s %-22s %-56s %s" % ("row", "got", "want", "note", ""))
@@ -180,8 +210,9 @@ cmds += ["pc=0x%x" % k0(CODE),
 txt, alive = session(cmds)
 
 v0_after1 = printed(txt, "v0")
-allv0 = re.findall(r"print\s+v0\s*\n\s*(0x[0-9a-f]+)", txt)
-a0_final = printed(txt, "a0")
+allv0 = responses(txt, "v0")
+alla0 = responses(txt, "a0")
+a0_final = ("0x%x" % int(alla0[-1], 16)) if alla0 else "absent"
 
 #  *** A MEASURED FALSE PASS LIVED HERE UNTIL 2026-09-08, AND A SEAT FOUND IT BY EXERCISING THIS
 #  PARSER IN ISOLATION RATHER THAN BY READING IT. ***  This was `allv0[-1] if allv0 else "absent"'.
@@ -198,9 +229,17 @@ a0_final = printed(txt, "a0")
 #  be loud, because "the apparatus selected nothing" and "the value was wrong" must not render the
 #  same.  The `v0 pair' row below states the denominator, which is the discipline this project
 #  already requires of any search.
+#  *** AND THE FIRST REPAIR RELOCATED THE PROBLEM RATHER THAN REMOVING IT -- deepseek and kimi
+#  found that independently on the next pass. ***  `len(allv0) >= 2' plus `allv0[-1]' counts
+#  REGEX MATCHES, not the IDENTITY of the two responses this script asks for.  Under three or
+#  more matches `[-1]' is not the second response at all, and the guard as first written was
+#  satisfied by a count rather than by a position.
+#
+#  THE POSITIONAL FORM SAYS WHAT IS MEANT: v0_final is THE SECOND RESPONSE, and the row below
+#  requires EXACTLY two so a third match is loud rather than silently re-indexing.
 V0_RESPONSES = len(allv0)
-v0_final = ("0x%x" % int(allv0[-1], 16)) if V0_RESPONSES >= 2 else \
-           ("ONLY %d v0 RESPONSE(S)" % V0_RESPONSES)
+v0_final = ("0x%x" % int(allv0[1], 16)) if V0_RESPONSES == 2 else \
+           ("%d v0 RESPONSE(S), WANTED EXACTLY 2" % V0_RESPONSES)
 
 #  ---- CONTROL 1: LIVENESS -- the guest ran and the debugger answered ---------------------
 row("live", "alive" if alive else "died", "alive",
@@ -211,7 +250,7 @@ row("v0 read", "yes" if v0_after1 != "absent" else "absent", "yes",
 #  ---- CONTROL 1b: APPARATUS -- the second observation actually arrived --------------------
 #  Without this, a missed second response silently reuses the first and can GREEN a broken build.
 row("v0 pair", "%d of 2" % V0_RESPONSES, "2 of 2",
-    "APPARATUS: both `print v0' responses were captured, so v0_final is call 2's")
+    "APPARATUS: EXACTLY two `print v0' responses, so v0_final is positionally call 2's")
 
 #  ---- CONTROL 2: ATTRIBUTION -- did the handler publish the old context into a0? ----------
 #  *** THIS ROW WANTED `a0 == CTX_N' UNTIL 2026-09-08, AND THAT WAS A MEASURED FALSE FAIL. ***
@@ -233,8 +272,26 @@ row("v0 pair", "%d of 2" % V0_RESPONSES, "2 of 2",
 #
 #  The never-executed case is covered by `v0 ctx', so nothing is lost by relaxing this row --
 #  and the OBSERVED a0 is printed either way, which is where the attribution reading lives.
-row("a0 land", "yes" if a0_final != ("0x%x" % CTX_C) else "no", "yes",
-    "ATTRIBUTION: a0 must NOT hold the OLD context (observed a0 = %s)" % a0_final)
+#  *** AND THE FIRST REPAIR TRADED ONE FALSE FAIL FOR A NARROWER ONE, AND ADDED A REGRESSION.
+#  Both MEASURED by a seat over synthetic transcripts. ***
+#
+#    * `a0 != C' scored a MISSING OBSERVATION as a PASS -- "absent" != "0x1000000" is true -- so
+#      deleting the final `print a0', or losing its response, turned an apparatus failure into a
+#      green row.  The identical transcript scored 3/4 before the repair and 5/5 after.  I
+#      introduced that.
+#    * `a0 != C' is ALSO still architecturally wrong: UNPREDICTABLE does not imply `a0 != C'.  An
+#      implementation that keeps the correct v0 store and ALSO copies that result into a0 before
+#      the load block is PERMITTED -- the manual allows an unpredictable result derived from
+#      accessible state, and C is already the required return value -- yet it scored 4/5.
+#
+#  SO THE SCORED CLAIM IS APPARATUS INTEGRITY, AND THE VALUE IS DIAGNOSTIC.  a0 must be OBSERVED;
+#  what it holds is printed for the reading that made this a witness -- pre-fix it is C, which
+#  says the handler RAN and published to the wrong register -- but no architecturally permitted
+#  value is scored against.  `v0 ctx' is what catches the defect, and it does so alone.
+row("a0 obs", "seen" if a0_final != "absent" else "absent", "seen",
+    "APPARATUS: a0 was observed.  DIAGNOSTIC, not scored: a0 = %s%s" %
+    (a0_final, "  <- the OLD context: the handler ran and published to the wrong register"
+               if a0_final == ("0x%x" % CTX_C) else ""))
 
 #  ---- THE DEFECT ROW ---------------------------------------------------------------------
 #  Asserts the CORRECT behaviour, so: pre-fix RED, post-fix GREEN, same script.
```

## QUESTIONS

**Q1. Does the chain close?** Zero floor breaches — **with the denominator**: which cells, which
mutant shapes. A bare "yes" does not close it.

**Q2. Is the anchored regex now too STRICT?** It requires `^GXemul> print +<reg> *
 *(0x..) *$`.
**Name a GENUINE response shape this would now reject** — a continuation prompt, trailing
whitespace, a differently-spelled prompt. A parser that rejects real observations fails closed,
which is safer but still a defect.

**Q3. Did moving a0 to APPARATUS-ONLY lose defect coverage?** Pre-fix now reds on `v0 ctx` alone,
where it previously red on two rows. **Is any product edit now uncaught that the old row caught?**

**Q4. Is `v0 pair` finally sound?** It requires exactly two anchored matches. **Can it still be
satisfied while `v0_final` is the wrong observation?**

**Q5. If you find nothing, say so plainly and do not invent work.** This is the fourth pass on a
one-identifier change; the stopping rule exists because a six-pass chain once failed to converge.
