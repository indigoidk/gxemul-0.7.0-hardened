# PASS 5 on the `#514` step-binding repair — the chain closes here or it names what is left

**VERDICT LINE FIRST.**  **The tree is `GXEMUL-SEC/src/`.**

**This is the fifth pass on a one-identifier product change.** Every prior pass found a real,
measured defect — which is the condition under which this chain is not the runaway the stopping
rule exists to prevent. **But that condition has to keep being met.** If you find nothing, say so
plainly; do not invent work to justify another pass.

## The chain so far

| pass | found | disposition |
|---|---|---|
| 2 | four findings incl. a false-failing row and a wrong clobber claim | repaired |
| 3 | **two MEASURED apparatus false passes, one introduced by the pass-2 repair** | repaired |
| 4 | a **coloured prompt makes a CORRECT build score 1/5**; two ORDER escapes | repaired |

**Pass 4's two order escapes are what this diff closes.** Anchoring fixed a response's SHAPE and
could not fix its ORDER: a second read moved BEFORE the second step, and the first response REPLAYED
as the second, are both well-formed responses in the wrong place.

**REPAIR:** `response_after()` locates the second `step` command's own echo and takes the first
genuine response following it; a `v0 bound` row scores that binding.

**MEASURED** (`ORDER_ATTACK_20260908.out`), with the shipped code extracted from the probe file:

    GENUINE: the response AFTER step 2 is call 2's     0x1010000   ok
    seat A: second read moved BEFORE the second step   None        rejected
    seat B: first response REPLAYED as the second      None        rejected
    (old count rule on A)                              2 of 2      WOULD HAVE PASSED
    (old count rule on B)                              2 of 2      WOULD HAVE PASSED

Four states, same script, six rows: FIXED 6/6; PREFIX 5/6 failing `v0 ctx` alone;
correct-but-clobbers-a0 6/6; CLICOLOR=1 6/6.

## The diff (3 hunk(s), complete)

```diff
diff --git a/regress/alpha_swpctx_v0_probe.py b/regress/alpha_swpctx_v0_probe.py
index 194f7ed..ff9b074 100644
--- a/regress/alpha_swpctx_v0_probe.py
+++ b/regress/alpha_swpctx_v0_probe.py
@@ -208,6 +208,30 @@ def responses(t, reg):
        lookalike command cannot supply one."""
     return re.findall(RESP % reg, t, re.M)
 
+
+def responses_at(t, reg):
+    """(value, offset) for every genuine response -- the offset is what lets a caller bind an
+       observation to the STEP it followed."""
+    return [(m.group(1), m.start()) for m in re.finditer(RESP % reg, t, re.M)]
+
+
+#  *** BINDING THE OBSERVATION TO ITS STEP, and it closes the last two escapes a pass-4 seat
+#  reported. ***  Anchoring fixed the SHAPE of a response; it cannot fix the ORDER.  Two variants
+#  still swept 5/5: a second read moved BEFORE the second step, and the first response REPLAYED as
+#  the second.  Both are correctly-formed responses in the wrong place, so no pattern over a single
+#  response can reject them -- what distinguishes them is WHERE they sit relative to the second
+#  `step'.  This finds that command's own echo and requires the second observation to follow it.
+def response_after(t, reg, marker):
+    """The first genuine <reg> response occurring AFTER `marker' appears in the transcript.
+       Returns None if the marker is absent or no response follows it."""
+    k = t.find(marker)
+    if k < 0:
+        return None
+    for val, pos in responses_at(t, reg):
+        if pos > k:
+            return val
+    return None
+
 def printed(t, reg):
     r = responses(t, reg)
     return "absent" if not r else "0x%x" % int(r[0], 16)
@@ -264,8 +288,9 @@ a0_final = ("0x%x" % int(alla0[-1], 16)) if alla0 else "absent"
 #  THE POSITIONAL FORM SAYS WHAT IS MEANT: v0_final is THE SECOND RESPONSE, and the row below
 #  requires EXACTLY two so a third match is loud rather than silently re-indexing.
 V0_RESPONSES = len(allv0)
-v0_final = ("0x%x" % int(allv0[1], 16)) if V0_RESPONSES == 2 else \
-           ("%d v0 RESPONSE(S), WANTED EXACTLY 2" % V0_RESPONSES)
+STEP2 = "GXemul> step %d" % len(second)
+v0_bound = response_after(txt, "v0", STEP2)
+v0_final = ("0x%x" % int(v0_bound, 16)) if v0_bound else "NO v0 RESPONSE AFTER STEP 2"
 
 #  ---- CONTROL 1: LIVENESS -- the guest ran and the debugger answered ---------------------
 row("live", "alive" if alive else "died", "alive",
@@ -276,7 +301,14 @@ row("v0 read", "yes" if v0_after1 != "absent" else "absent", "yes",
 #  ---- CONTROL 1b: APPARATUS -- the second observation actually arrived --------------------
 #  Without this, a missed second response silently reuses the first and can GREEN a broken build.
 row("v0 pair", "%d of 2" % V0_RESPONSES, "2 of 2",
-    "APPARATUS: EXACTLY two `print v0' responses, so v0_final is positionally call 2's")
+    "APPARATUS: EXACTLY two `print v0' responses")
+
+#  ---- CONTROL 1c: the observation is BOUND TO ITS STEP -----------------------------------
+#  Closes the two ORDER escapes anchoring could not: a read moved before the second step, and
+#  the first response replayed as the second.  Both are well-formed responses in the wrong
+#  place, so only position relative to `step' can reject them.
+row("v0 bound", "yes" if v0_bound else "no", "yes",
+    "APPARATUS: the scored v0 is the response FOLLOWING the second `step', not merely the 2nd match")
 
 #  ---- CONTROL 2: ATTRIBUTION -- did the handler publish the old context into a0? ----------
 #  *** THIS ROW WANTED `a0 == CTX_N' UNTIL 2026-09-08, AND THAT WAS A MEASURED FALSE FAIL. ***
```

## QUESTIONS

**Q1. Does the chain close?** Zero floor breaches **with the denominator** — which cells, which
mutant shapes. A bare "yes" does not close it.

**Q2. Is `response_after` itself sound?** It does `t.find(marker)` for `"GXemul> step <n>"` and takes
the first response after that offset. **Can that marker appear EARLIER in the transcript for an
unrelated reason** — a banner, an echo, a step of the same count elsewhere — and bind the wrong
observation? The probe issues `step len(first)` then `step len(second)`; **what if those counts are
equal?**

**Q3. Did binding lose coverage?** `v0_final` is now "the response after step 2" rather than "the
second response". **Name a transcript where those differ and the new rule is the WRONG one.**

**Q4. Six rows now. Is any of them vacuous** — green under every mutant in the enumeration, or
unable to vary under the mutant it names?

**Q5. If nothing is left, say so.** Five passes on one identifier is at the edge of what the
stopping rule contemplates, and I would rather close on an honest zero than keep going.
