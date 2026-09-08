# PASS 3 on the `#514` REPAIR diff — does the chain close here?

**VERDICT LINE FIRST.**

**The tree is `GXEMUL-SEC/src/`** — ignore the pristine 2021 copy at the project root.

**This is the repair-chain pass.** `#514` shipped, pass 2 found four things, all four were repaired
in-round, and **a repair made in response to a pass 2 owes its own pass.** The chain closes on the
first pass that finds **zero floor breaches** — and the rule is explicit that a bare zero does not
close it: the zero must carry its denominator, naming which cells and which mutant shapes were
swept.

**REVIEW EFFORT IS SCOPED TO THIS DIFF.** Settled design is not re-litigated. **But the FLOOR
QUESTION is asked of the SHIPPED COMPOSITE**: does a clean-sweep mutant exist against the probe as
it now stands?

## 1. WHAT PASS 2 FOUND AND WHAT WAS DONE

| finding | who | disposition |
|---|---|---|
| **a MEASURED false pass in the harness** — the scorer took `allv0[-1]`, and with the second `print v0` missed it silently reused call 1's value, which under a `v0 = a0` repair IS `C` | codex, by exercising the parser on a synthetic transcript → 4/4 | **REPAIRED**: fewer than two responses is now an apparatus failure; new `v0 pair` row |
| **`a0 land` pinned the implementation, not the architecture** | glm, minimax, kimi, grok — then MEASURED by me | **REPAIRED**: now asserts the negative claim (a0 must not hold the OLD context) |
| **the wrapper does not list a0 among the clobbers** — it is an in-out operand | grok, by reading the asm | **CORRECTED** in the product comment and CHANGELOG |
| **clause (d) was the wrong name** — this diff is an unguarded register-index substitution, so (d)'s enumeration is empty; `v0 = a0` is RHS coverage | grok | **RECORDED**, no mutant owed (5 seats agree) |

**RE-MEASURED IN ALL THREE STATES with the repaired probe, same script:**

    pre-fix (defect reinstated verbatim, scratch clone)   3/5   red on a0 land AND v0 ctx
    fixed (build/)                                        5/5
    correct-but-clobbers-a0 (scratch clone)               5/5   the false fail is gone

## 2. THE PROBE DIFF (2 hunk(s), complete)

```diff
diff --git a/regress/alpha_swpctx_v0_probe.py b/regress/alpha_swpctx_v0_probe.py
index 4201a93..a23f87e 100644
--- a/regress/alpha_swpctx_v0_probe.py
+++ b/regress/alpha_swpctx_v0_probe.py
@@ -30,6 +30,28 @@ THE HANDLER RAN AND WROTE THE WRONG REGISTER, and separates that from "the handl
 executed", which would leave a0 holding N and v0 holding S.  One observation, two hypotheses
 distinguished.
 
+THE CONTRACT -- what this probe is designed to catch, and what it deliberately is not.
+
+CAUGHT: the shipped defect (v0 never written); any repair that returns the NEW context instead
+of the old; and any repair that publishes the OLD context into a0.  NOT CAUGHT, and disclosed
+rather than discovered later: this probe does NOT assert that the new context was actually
+INSTALLED.  An edit leaving `r[ALPHA_V0] = ctx' correct while breaking the subsequent
+load-new-context block would produce v0 == C and a0 == N and score 4/4.  Raised independently
+by deepseek and kimi on the pass-2 panel; filed as coverage debt rather than fixed here,
+because it is a different part of the handler from the fix's own repair and so is not a
+clause-(d) breach.  The row that would close it: a THIRD swpctx call, which should return N as
+its old context.
+
+ALSO NOT CAUGHT, named by grok on the pass-2 panel: a product edit that HARDCODES the planted
+value -- `cpu->cd.alpha.r[ALPHA_V0] = 0x01000000;' -- scores 4/4 here.  Filed rather than chased,
+and the reason is the bound: the contract is "the OLD context in v0", the planted C is ONE old
+context, and rowing every RHS that happens to equal C for this one pair is the unbounded shape.
+The hole is NAMED so a later escape is "outside the contract" rather than a surprise.
+
+THIS PROBE DOES NOT PIN a0's VALUE ON A CORRECT BUILD.  The architecture marks a0
+UNPREDICTABLE after the call; only the negative claim -- a0 does not receive the old context --
+is owed.  See `a0 land' below for the measurement that established this.
+
 WHY THE PROGRAM RELOADS ITS SCRATCH POINTER.  T0 is Alpha t0, which the wrapper's own clobber
 list names.  Whether this model clobbers it is not the point: the guest program is written to
 be correct under the ABI, not under the model's current behaviour.
@@ -159,20 +181,60 @@ txt, alive = session(cmds)
 
 v0_after1 = printed(txt, "v0")
 allv0 = re.findall(r"print\s+v0\s*\n\s*(0x[0-9a-f]+)", txt)
-v0_final = "0x%x" % int(allv0[-1], 16) if allv0 else "absent"
 a0_final = printed(txt, "a0")
 
+#  *** A MEASURED FALSE PASS LIVED HERE UNTIL 2026-09-08, AND A SEAT FOUND IT BY EXERCISING THIS
+#  PARSER IN ISOLATION RATHER THAN BY READING IT. ***  This was `allv0[-1] if allv0 else "absent"'.
+#  The script issues TWO `print v0' commands; if the SECOND response is missed -- a short pty read,
+#  a slow step -- `[-1]' silently returns the FIRST call's value.  Under an incorrect repair that
+#  returns the INCOMING context (`v0 = a0'), call 1 is passed C, so that stale first value IS C,
+#  and the `v0 ctx' row that wants C GOES GREEN ON A BROKEN BUILD.
+#
+#  codex fed exactly that synthetic transcript -- one v0 response of C, plus a0 = N -- to this
+#  scoring code and it returned 4/4.  Not a product escape: a HARNESS false pass, which the
+#  stopping rule says is fixed in-round rather than filed.
+#
+#  THE FIX IS TO REFUSE, NOT TO GUESS.  Fewer than two responses is an APPARATUS failure and must
+#  be loud, because "the apparatus selected nothing" and "the value was wrong" must not render the
+#  same.  The `v0 pair' row below states the denominator, which is the discipline this project
+#  already requires of any search.
+V0_RESPONSES = len(allv0)
+v0_final = ("0x%x" % int(allv0[-1], 16)) if V0_RESPONSES >= 2 else \
+           ("ONLY %d v0 RESPONSE(S)" % V0_RESPONSES)
+
 #  ---- CONTROL 1: LIVENESS -- the guest ran and the debugger answered ---------------------
 row("live", "alive" if alive else "died", "alive",
     "CONTROL: the session survives the whole sequence")
 row("v0 read", "yes" if v0_after1 != "absent" else "absent", "yes",
     "CONTROL: v0 is readable at all through `print' after call 1")
 
-#  ---- CONTROL 2: ATTRIBUTION -- the handler RAN, and we can see where it wrote ------------
-#  On the shipped build a0 holds C: the handler executed and published to the wrong register.
-#  If the handler had never run, a0 would still hold N and this row would read 0x1010000.
-row("a0 land", a0_final, "0x%x" % CTX_N,
-    "ATTRIBUTION: post-fix a0 keeps the INCOMING context; pre-fix it holds the OLD one")
+#  ---- CONTROL 1b: APPARATUS -- the second observation actually arrived --------------------
+#  Without this, a missed second response silently reuses the first and can GREEN a broken build.
+row("v0 pair", "%d of 2" % V0_RESPONSES, "2 of 2",
+    "APPARATUS: both `print v0' responses were captured, so v0_final is call 2's")
+
+#  ---- CONTROL 2: ATTRIBUTION -- did the handler publish the old context into a0? ----------
+#  *** THIS ROW WANTED `a0 == CTX_N' UNTIL 2026-09-08, AND THAT WAS A MEASURED FALSE FAIL. ***
+#  Three pass-2 seats read it as pinning THIS MODEL'S CHOSEN REPAIR rather than the
+#  architecture, and a built mutant settled it: a CORRECT implementation that also clobbers a0
+#  (`r[ALPHA_V0] = ctx' kept, plus `r[ALPHA_A0] = 0xdeadbeef') scored 3/4, failing HERE while
+#  `v0 ctx' stayed green.  Real PALcode does clobber a0, and the fix's own comment invokes a0's
+#  UNPREDICTABLE status -- which permits ANY value.  So the old row required what the round
+#  itself said was not owed.  (kimi: "the probe pins this model's chosen repair, not the
+#  architecture".)
+#
+#  THE HONEST ASSERTION IS THE NEGATIVE ONE: the handler must not publish the OLD context into
+#  a0.  That is exactly the defect, and it leaves a0 otherwise free.  All four states:
+#
+#      shipped defect   (v0=S, a0=C)      RED here      -- the defect, still caught
+#      correct          (v0=C, a0=N)      green
+#      correct+clobber  (v0=C, a0=0xdead) green         -- no longer a false fail
+#      never executed   (v0=S, a0=N)      green here, but `v0 ctx' REDS
+#
+#  The never-executed case is covered by `v0 ctx', so nothing is lost by relaxing this row --
+#  and the OBSERVED a0 is printed either way, which is where the attribution reading lives.
+row("a0 land", "yes" if a0_final != ("0x%x" % CTX_C) else "no", "yes",
+    "ATTRIBUTION: a0 must NOT hold the OLD context (observed a0 = %s)" % a0_final)
 
 #  ---- THE DEFECT ROW ---------------------------------------------------------------------
 #  Asserts the CORRECT behaviour, so: pre-fix RED, post-fix GREEN, same script.
```

## 3. THE PRODUCT DIFF — comment-only (1 hunk(s), complete)

```diff
diff --git a/src/cpus/cpu_alpha_palcode.c b/src/cpus/cpu_alpha_palcode.c
index b511768..97aa499 100644
--- a/src/cpus/cpu_alpha_palcode.c
+++ b/src/cpus/cpu_alpha_palcode.c
@@ -250,15 +250,22 @@ Make sure they are correct, as documented in the Manual.
 		/*  Return old context in v0.  */
 		/*  #514: was ALPHA_A0, contradicting the comment directly above and the
 		    third-party ABI wrapper.  `alpha_pal_swpctx' (alpha_cpu.h) declares
-		    `v0 __asm("$0")' as an OUTPUT and lists a0 as CLOBBERED, so a correct
-		    caller reads the result from v0 and may not rely on a0 -- the model was
-		    publishing into the register the caller is told to discard and leaving
-		    untouched the one it reads.  `:251' was the only `r[ALPHA_A0] =' in this
-		    file; every compiled return here uses ALPHA_V0.  No a0 write is added:
-		    the architecture marks a0 UNPREDICTABLE, which permits it to remain
-		    unchanged, so there is nothing further owed.  Ordering is unaffected --
-		    `a0' at the `ctx = a0' below is the LOCAL captured at function entry
-		    (`:165'), not a live register read, so this store cannot perturb it.  */
+		    `v0 __asm("$0")' as an OUTPUT, so a correct caller reads the result
+		    from v0.  a0 is NOT in that asm's clobber list ($1,$22..$25,memory) --
+		    it is an IN-OUT OPERAND ("=r" (a0) with input "0" (a0)), and the
+		    wrapper's own comment marks it clobbered "(above)", i.e. handled as
+		    that operand.  Either way the caller may not rely on a0, so the model
+		    was publishing into the register the caller discards and leaving
+		    untouched the one it reads.  (An earlier draft of this comment said the
+		    wrapper "lists a0 as clobbered"; a pass-2 seat read the asm and showed
+		    it does not.)  No a0 write is added: the architecture marks a0
+		    UNPREDICTABLE, which permits it to remain unchanged.  Ordering is
+		    unaffected -- `a0' at the `ctx = a0' below is the LOCAL captured at
+		    function entry (`:165'), not a live register read.  Census, corrected
+		    twice and stated as of AFTER this fix: no `r[ALPHA_A0] =' remains in the
+		    file, and the compiled PAL returns to v0 are rdmces, this swpctx,
+		    swpipl, rdps and whami -- three further v0 stores sit inside `#if 0' and
+		    `:118' is alpha_prom_call, not a PAL.  */
 		cpu->cd.alpha.r[ALPHA_V0] = cpu->cd.alpha.ctx;	/*  #514  */
 
 		/*  Load new context:  */
```

## 4. QUESTIONS

**Q1. THE FLOOR, asked of the composite.** Does a clean-sweep mutant exist against the probe **as
it now stands**? Name it, or state that none exists **with the denominator** — which cells, which
mutant shapes you swept. **A bare "no" does not close this chain.**

**Q2. DID THE REPAIR TO `a0 land` REMOVE COVERAGE?** It went from `a0 == N` to `a0 != C`. The
pre-fix run still reds it, measured. **But is there an edit that the OLD row would have caught and
the NEW one does not?** If yes, that is a regression in the detector and I want it now.

**Q3. IS THE `v0 pair` APPARATUS ROW ITSELF SOUND?** It asserts exactly two `print v0` responses.
**Can it be satisfied while `v0_final` is still the wrong observation** — for instance if a stray
`print v0` appears in the transcript, or if the regex matches something other than a response?

**Q4. THE COMMENT-ONLY PRODUCT DIFF.** It changes no code. **Verify that** — and say whether any
claim it now makes is still unexhibited or wrong. It carries a census stated "as of after the fix",
which is the sort of claim this round has already had to correct twice.

**Q5. DOES THE CHAIN CLOSE?** If you find zero floor breaches, say so **with the denominator**. If
you find one, say which clause and whether it is L2 (repair in-round) or coverage debt (file).
**Do not invent work to justify another pass** — the stopping rule exists because a six-pass chain
once failed to converge, and this round has now had two passes on one identifier.
