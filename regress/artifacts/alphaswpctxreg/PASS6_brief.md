# PASS 6 on `#514` — and the real question is whether this chain should still be running

**VERDICT LINE FIRST.**  **The tree is `GXEMUL-SEC/src/`.**

**I am asking you to rule on the STOPPING QUESTION as well as the diff**, because I do not trust my
own judgement on it after five passes.

## The pattern I think I see, and want tested

| pass | found | where |
|---|---|---|
| 2 | four findings | product comment + one row |
| 3 | two measured apparatus false passes, one I introduced | **the probe's parser** |
| 4 | a coloured prompt makes a correct build score 1/5; two order escapes | **the probe's parser** |
| 5 | my binding repair LOST coverage the positional rule had | **the probe's parser** |

**THE PRODUCT FIX — one identifier, `ALPHA_A0` → `ALPHA_V0` — HAS BEEN RATIFIED SINCE PASS 2 AND
UNCHALLENGED SINCE.** The floor question has answered "no undisclosed breaches" since pass 3. Every
finding from pass 3 onward is in the *test apparatus*, found by running synthetic transcripts
against a parser — **which is an unbounded space, and unbounded spaces are what the stopping rule
exists to refuse.**

**But pass 5's finding was real and important** — my repair genuinely lost coverage — so the passes
are still buying something. That is exactly the tension I cannot resolve from inside.

## What this diff does

Composes the two rules that each let the other's escapes through: the scored value is the SECOND
response positionally **AND** must follow a **UNIQUE** second-step echo. Plus a CHANNEL line naming
the mutant `a0 obs` kills (the a0 observation being lost), which a pass-5 seat asked for.

**MEASURED, full escape corpus, helpers extracted from the shipped file (5/5):** genuine → correct;
both pass-4 variants rejected on *"2nd response precedes 2nd step"*; codex's rebinding case rejected
on *"2 `step 4` echoes, wanted exactly 1"*; codex's unique-marker case correctly accepted.
Four build states unchanged: 6/6, 5/6 on `v0 ctx` alone, 6/6, 6/6.

## The diff (5 hunk(s))

```diff
diff --git a/regress/alpha_swpctx_v0_probe.py b/regress/alpha_swpctx_v0_probe.py
index ff9b074..9f81f0c 100644
--- a/regress/alpha_swpctx_v0_probe.py
+++ b/regress/alpha_swpctx_v0_probe.py
@@ -70,6 +70,13 @@ establishes the plain response shape; it does not support the accompanying unive
 pattern to chase it.  Whitespace and hex case are widened too, because a parser that fails CLOSED
 on a genuine response is still a defect.
 
+WHAT `v0 bound' PROVES IS ORDER, NOT PROVENANCE -- a pass-5 seat's precision and it is worth
+keeping.  The rule establishes that a v0-shaped response follows a unique second-step echo and is
+the second such response.  It does NOT establish that the line is the debugger's answer to the
+second `print v0' rather than a correctly-placed replay.  Both genuine reads in a passing run carry
+the same value, so no row here can distinguish those.  **The claim the row is entitled to is
+positional, and the note says so.**
+
 THIS PROBE DOES NOT SCORE a0's VALUE AT ALL.  `a0 obs' scores only that the observation was
 MADE; the value is printed as diagnostic.  Two measured findings forced that: scoring `a0 != C'
 passed a MISSING observation, and it also failed a PERMITTED implementation that copies the
@@ -221,16 +228,45 @@ def responses_at(t, reg):
 #  the second.  Both are correctly-formed responses in the wrong place, so no pattern over a single
 #  response can reject them -- what distinguishes them is WHERE they sit relative to the second
 #  `step'.  This finds that command's own echo and requires the second observation to follow it.
-def response_after(t, reg, marker):
-    """The first genuine <reg> response occurring AFTER `marker' appears in the transcript.
-       Returns None if the marker is absent or no response follows it."""
-    k = t.find(marker)
-    if k < 0:
-        return None
-    for val, pos in responses_at(t, reg):
-        if pos > k:
-            return val
-    return None
+def step_marker(t, nsteps):
+    """Every occurrence of the `step <nsteps>' command echo, as (start, end) offsets.
+       Whole-token: a plain find() also matches `step 40' and `step 4 extra'."""
+    return [(m.start(), m.end())
+            for m in re.finditer(r"^GXemul>[ \t]+step[ \t]+%d[ \t]*$" % nsteps, t, re.M)]
+
+
+def bound_second(t, reg, nsteps):
+    """The SECOND genuine <reg> response, required to sit AFTER a UNIQUE `step <nsteps>' echo.
+
+       *** THIS COMPOSES TWO RULES THAT EACH LET THE OTHER'S ESCAPES THROUGH, AND A SEAT MEASURED
+       BOTH FAILURES OVER 65 SYNTHETIC TRANSCRIPTS. ***
+
+         POSITIONAL ALONE (`allv0[1]')   -- rejected an out-of-order read, but a first response
+                                            REPLAYED as the second passed.
+         BINDING ALONE (`first response  -- rejected the replay, but an EARLIER `step 4' echo
+         after the marker')                rebinds to call 1 and returns C: measured 6/6 FALSE
+                                            PASS on the incoming-context mutant, where the
+                                            positional rule had correctly scored 4/5.
+                                            *The binding repair LOST coverage the positional rule
+                                            had.*
+
+       So the scored observation must satisfy BOTH: it is the second response, AND it follows the
+       second step.  The marker must also be UNIQUE -- with two `step 4' echoes there is no fact
+       of the matter about which one bounds call 2, and guessing is what produced the false pass.
+
+       Returns (value, why) so the caller can report WHICH condition failed rather than a bare
+       absent."""
+    marks = step_marker(t, nsteps)
+    if len(marks) != 1:
+        return None, "%d `step %d' echoes, wanted exactly 1" % (len(marks), nsteps)
+    resp = responses_at(t, reg)
+    if len(resp) != 2:
+        return None, "%d %s responses, wanted exactly 2" % (len(resp), reg)
+    val, pos = resp[1]
+    if pos <= marks[0][1]:
+        return None, "the 2nd %s response precedes the 2nd step" % reg
+    return val, "ok"
+
 
 def printed(t, reg):
     r = responses(t, reg)
@@ -288,9 +324,8 @@ a0_final = ("0x%x" % int(alla0[-1], 16)) if alla0 else "absent"
 #  THE POSITIONAL FORM SAYS WHAT IS MEANT: v0_final is THE SECOND RESPONSE, and the row below
 #  requires EXACTLY two so a third match is loud rather than silently re-indexing.
 V0_RESPONSES = len(allv0)
-STEP2 = "GXemul> step %d" % len(second)
-v0_bound = response_after(txt, "v0", STEP2)
-v0_final = ("0x%x" % int(v0_bound, 16)) if v0_bound else "NO v0 RESPONSE AFTER STEP 2"
+v0_bound, v0_why = bound_second(txt, "v0", len(second))
+v0_final = ("0x%x" % int(v0_bound, 16)) if v0_bound else ("UNBOUND: " + v0_why)
 
 #  ---- CONTROL 1: LIVENESS -- the guest ran and the debugger answered ---------------------
 row("live", "alive" if alive else "died", "alive",
@@ -308,7 +343,7 @@ row("v0 pair", "%d of 2" % V0_RESPONSES, "2 of 2",
 #  the first response replayed as the second.  Both are well-formed responses in the wrong
 #  place, so only position relative to `step' can reject them.
 row("v0 bound", "yes" if v0_bound else "no", "yes",
-    "APPARATUS: the scored v0 is the response FOLLOWING the second `step', not merely the 2nd match")
+    "APPARATUS: the scored v0 is the 2nd response AND follows a UNIQUE 2nd step (%s)" % v0_why)
 
 #  ---- CONTROL 2: ATTRIBUTION -- did the handler publish the old context into a0? ----------
 #  *** THIS ROW WANTED `a0 == CTX_N' UNTIL 2026-09-08, AND THAT WAS A MEASURED FALSE FAIL. ***
@@ -346,6 +381,19 @@ row("v0 bound", "yes" if v0_bound else "no", "yes",
 #  what it holds is printed for the reading that made this a witness -- pre-fix it is C, which
 #  says the handler RAN and published to the wrong register -- but no architecturally permitted
 #  value is scored against.  `v0 ctx' is what catches the defect, and it does so alone.
+#  *** THE CHANNEL LINE FOR THIS ROW, because a pass-5 seat correctly asked what mutant it now
+#  kills. ***  Its ORIGINAL mutant was "the handler publishes the old context into a0", and that
+#  is no longer scored -- the architecture permits it, which is why the value became diagnostic.
+#  So the row would be VACUOUS BY CONSTRUCTION unless it names a different one.
+#
+#      MUTANT IT KILLS:  the a0 OBSERVATION IS LOST -- the final `print a0' deleted, its response
+#                        missed by a short read, or the register unreadable.
+#      OBSERVABLE:       `a0_final' is "absent" rather than a hex value.
+#
+#  That is not hypothetical: the pass-3 repair scored `a0 != C', and "absent" != "0x1000000" is
+#  TRUE, so a lost observation PASSED.  A seat measured the same transcript at 3/4 before that
+#  repair and 5/5 after.  This row exists to make that state red, and it is the only row that can
+#  -- `v0 ctx' says nothing about a0.
 row("a0 obs", "seen" if a0_final != "absent" else "absent", "seen",
     "APPARATUS: a0 was observed.  DIAGNOSTIC, not scored: a0 = %s%s" %
     (a0_final, "  <- the OLD context: the handler ran and published to the wrong register"
```

## QUESTIONS

**Q1. SHOULD THIS CHAIN CLOSE?** Not "is the diff perfect" — **is another pass a good use of the
panel**, given the product has been settled for four passes and the remaining findings are in a
parser that no gate runs and whose failure mode is a red row on a correct build? **Argue the case
for CONTINUING first, then say which you hold.**

**Q2. Is the composition actually sound**, or does requiring BOTH conditions create a new rejection
of a genuine transcript? Name one if it exists.

**Q3. Is `a0 obs`'s named mutant the right one?** It claims to kill "the a0 observation is lost".
**Is there a cheaper row that kills the same thing, or is this row now doing two jobs?**

**Q4. What would you STOP measuring?** If you were spending the next pass, what would you NOT look
at — and does that list include the parser?

**Q5. If you think it closes, say so with the denominator.** If you think it does not, name the
specific defect and whether it is a floor breach or apparatus debt. **Do not invent work.**
