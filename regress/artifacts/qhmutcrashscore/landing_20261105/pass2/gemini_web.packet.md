# Reading task: kdc_p2 (Gemini web; 2026-11-06)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBKDCP2-bb09` on a line of its own.

# PASS 2 -- #585 qhmutcrashscore: gate 3 stops scoring a mutant run that never printed its verdict as a detection

VERDICT LINE FIRST, exactly this shape, so it survives truncation:

    QHMUTP2: <n> PREMISES FALSE, <n> BREAKS, <n> RECORD ERRORS; VERDICT ship | fix first

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise its brief stated wrongly.  **Check the premises, not just
the derivations.**  Where this packet states something as fact, ask whether the inlined text supports it.  A seat that
re-derives a premise from the text below is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/`** (HEAD 2632277f).  If you cannot read files, that is expected: every fact you
need is inlined below.  Name any premise you cannot settle from this packet rather than guessing at it.

**Where a claim is arithmetic -- a count of checks, which runs are refused -- ENUMERATE it: walk the seven mutants and
the control through the inlined function rather than reasoning about them.**

This is ordinary regression-harness engineering: a test script that runs a numerical differential against
deliberately broken copies of a source file, and must report a broken copy only when the differential itself said so.

## 1. What the round changes, and why

`regress/selftest_mutation.sh` (gate 3 of 16) checks that gate 2's float_emul differential can fail.  It copies
`src/core/float_emul.c` seven times, breaks each copy a different way ("mutants"), builds the differential
`regress/diff_ieee_store.c` against each, runs it, and requires each run to report failure; an unbroken build must
report success.  The differential prints exactly one verdict line, `DIFF_PASS -- ...` or `DIFF_FAIL`, as its last line
(section 3).

At HEAD the run step was `"$T/$1" > "$T/$1.out" 2>&1` followed by `grep -c 'DIFF_PASS' "$T/$1.out"`, and a mutant's
check wanted `0`.  A run that crashed, called exit(1) or printed nothing has zero DIFF_PASS lines, so it scored
`DETECTED (must fail)` without ever reaching its verdict.  Measured with a stub differential whose seven mutants all
raise SIGFPE before any output: HEAD's gate printed `PASS (15 checks)` (section 5).

The fix: keep the run's exit status, and before counting require a line beginning `DIFF_PASS` or `DIFF_FAIL`; without
one, print `NOLOG rc=<status>`.  Nothing else in the gate changes.

## 2. The full diff of the gate (HEAD -> staged; +11 -1, all inside build_and_run())

```diff
--- HEAD:regress/selftest_mutation.sh
+++ staged:regress/selftest_mutation.sh
@@ -166,10 +166,20 @@
     [ $? -eq 0 ] && echo ok || echo FAIL
 }
 
-build_and_run() {   # label, source file -> prints DIFF_PASS count
+build_and_run() {   # label, source file -> prints DIFF_PASS count, BUILDFAIL, or NOLOG rc=<n>
     $CC -O2 -I"$TREE/src/include" -o "$T/$1" \
         "$HERE/diff_ieee_store.c" "$2" -lm > "$T/$1.build" 2>&1 || { echo "BUILDFAIL"; return; }
     "$T/$1" > "$T/$1.out" 2>&1
+    local rc=$?
+    #  #585 qhmutcrashscore (task #55): a run that never printed its verdict is NOT a detection.
+    #  Counting DIFF_PASS alone scored a mutant run that crashed, called exit(1) or printed
+    #  nothing as "DETECTED (must fail)"; with all seven mutants killed by SIGFPE before any
+    #  output this gate went PASS -- measured with a stub differential, kept at
+    #  regress/artifacts/qhmutcrashscore/wkdc_20261105/witness/g3/W2_HEAD.allcrash.log.
+    #  The differential's verdict line is its last line, so it is the sentinel: a run without
+    #  one prints NOLOG and its check reds.  A run that HANGS still wedges this gate -- there is
+    #  no per-run time bound (ledger row gate3runbound).
+    grep -qE '^DIFF_(PASS|FAIL)' "$T/$1.out" || { echo "NOLOG rc=$rc"; return; }
     grep -c 'DIFF_PASS' "$T/$1.out"
 }
 
```

**The whole enclosing function as staged** (every exit path: the BUILDFAIL return, the NOLOG return, the count):

```bash
build_and_run() {   # label, source file -> prints DIFF_PASS count, BUILDFAIL, or NOLOG rc=<n>
    $CC -O2 -I"$TREE/src/include" -o "$T/$1" \
        "$HERE/diff_ieee_store.c" "$2" -lm > "$T/$1.build" 2>&1 || { echo "BUILDFAIL"; return; }
    "$T/$1" > "$T/$1.out" 2>&1
    local rc=$?
    #  #585 qhmutcrashscore (task #55): a run that never printed its verdict is NOT a detection.
    #  Counting DIFF_PASS alone scored a mutant run that crashed, called exit(1) or printed
    #  nothing as "DETECTED (must fail)"; with all seven mutants killed by SIGFPE before any
    #  output this gate went PASS -- measured with a stub differential, kept at
    #  regress/artifacts/qhmutcrashscore/wkdc_20261105/witness/g3/W2_HEAD.allcrash.log.
    #  The differential's verdict line is its last line, so it is the sentinel: a run without
    #  one prints NOLOG and its check reds.  A run that HANGS still wedges this gate -- there is
    #  no per-run time bound (ledger row gate3runbound).
    grep -qE '^DIFF_(PASS|FAIL)' "$T/$1.out" || { echo "NOLOG rc=$rc"; return; }
    grep -c 'DIFF_PASS' "$T/$1.out"
}
```

**Its callers, verbatim from the staged file -- the only two uses of its output, and the end of the gate:**

```bash
for m in revert287 tiesaway modeignored wlegacyrounds revert303 maskcarry flushband; do
    check "mutant $m could be applied" "$(mutate $m)" "ok"
done

note "control: differential against the shipped float_emul.c"
real=$(build_and_run real "$TREE/src/core/float_emul.c")
check "unmutated source passes gate 2" "$real" "1"

for m in revert287 tiesaway modeignored wlegacyrounds revert303 maskcarry flushband; do
    note "mutant $m: the differential must go red"
    out=$(build_and_run "mut_$m" "$T/mutant_$m.c")
    check "mutant $m is DETECTED (must fail)" "$out" "0"
done

gate_end
exit $?
```

**`check()` from regress/lib.sh (HEAD, unchanged) -- a string comparison of got against want:**

```bash
check() {
    _checks=$((_checks+1))
    if [ "$2" = "$3" ]; then
        printf "  ${C_OK}ok${C_OFF}   %-52s %s\n" "$1" "$2"
    else
        printf "  ${C_BAD}FAIL${C_OFF} %-52s got=%s want=%s\n" "$1" "$2" "$3"
        _fails=$((_fails+1))
    fi
}
```

## 3. The differential's verdict, the tail of main() in regress/diff_ieee_store.c (HEAD, unchanged)

```c
	if (abs_bad == 0 && unexplained == 0 && missed == 0 && should_differ > 0 &&
	    inrange_diff == 0 && dD > 0 && dS > 0 &&
	    e_clamp == 129 && e_255 == 128 && e_diff == -149 &&
	    rm_rn_bad == 0 && rm_rz_bad == 0 && rm_mode_diff > 1000000 &&
	    rm_d_bad == 0 && rm_vec_bad == 0 && interp_bad == 0)
		printf("DIFF_PASS -- change-set is exactly the three predicted classes.\n");
	else
		printf("DIFF_FAIL\n");
	return 0;
}
```

## 4. The stub differential the controls used in place of diff_ieee_store.c (preserved as evidence)

It tests nothing; it prints the differential's verdict tokens and picks each run's ending by the binary's own name
(the gate names them `real` and `mut_<name>`).

```c
/*
 *  STUB stand-in for regress/diff_ieee_store.c -- killdrivercrash harness witness, gate 3.
 *  It is NOT the differential and tests NOTHING in float_emul.c (which is linked in, unused).
 *  It prints the differential's verdict tokens -- "DIFF_PASS ..." or "DIFF_FAIL" as the last
 *  line, exactly as HEAD's diff_ieee_store.c does -- and chooses each run's ENDING by the binary's
 *  own name, which selftest_mutation.sh sets to "real" or "mut_<name>".
 *
 *  STUBSET=mixed (default):
 *      real              DIFF_PASS                       the control arm
 *      mut_revert287     a FAIL row, DIFF_FAIL           a GENUINE kill
 *      mut_flushband     a FAIL row, DIFF_FAIL           a GENUINE kill
 *      mut_tiesaway      DIFF_PASS                       a GENUINE survivor (gate 3 must go red)
 *      mut_modeignored   raise(SIGFPE) before any output (buffered output lost)
 *      mut_wlegacyrounds a FAIL row (flushed), then raise(SIGFPE): no verdict token
 *      mut_revert303     a FAIL row, fatal + exit(1): no verdict token (the "host kill" shape)
 *      mut_maskcarry     prints NOTHING and returns 0
 *  STUBSET=allkill: every mut_* is a genuine kill (a FAIL row, DIFF_FAIL); real passes.
 *  STUBSET=allcrash: every mut_* raises SIGFPE before printing anything; real passes.
 */
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*  float_emul.c references fatal(); the real differential supplies it the same way.  */
void fatal(const char *fmt, ...)
{
	(void) fmt;
}

int main(int argc, char **argv)
{
	const char *b = strrchr(argv[0], '/');
	const char *set = getenv("STUBSET");
	b = b ? b + 1 : argv[0];
	(void) argc;
	if (set != NULL && strcmp(set, "allkill") == 0 && strncmp(b, "mut_", 4) == 0) {
		printf("  FAIL stub row\nDIFF_FAIL\n");
		return 0;
	}
	if (set != NULL && strcmp(set, "allcrash") == 0 && strncmp(b, "mut_", 4) == 0)
		raise(SIGFPE);
	if (strcmp(b, "real") == 0) {
		printf("  ok   stub row\nDIFF_PASS -- stub\n");
		return 0;
	}
	if (strcmp(b, "mut_revert287") == 0 || strcmp(b, "mut_flushband") == 0) {
		printf("  FAIL stub row\nDIFF_FAIL\n");
		return 0;
	}
	if (strcmp(b, "mut_tiesaway") == 0) {
		printf("  ok   stub row\nDIFF_PASS -- stub survivor\n");
		return 0;
	}
	if (strcmp(b, "mut_modeignored") == 0) {
		printf("  ok   stub row (buffered, lost)\n");
		raise(SIGFPE);
	}
	if (strcmp(b, "mut_wlegacyrounds") == 0) {
		printf("  FAIL stub row\n");
		fflush(stdout);
		raise(SIGFPE);
	}
	if (strcmp(b, "mut_revert303") == 0) {
		printf("  FAIL stub row\n");
		fprintf(stderr, "fatal: stub host kill\n");
		exit(1);
	}
	if (strcmp(b, "mut_maskcarry") == 0)
		return 0;
	printf("stub: unknown binary name %s\n", b);
	return 2;
}
```

## 5. The measured controls (byte-for-byte; expectations written in compare.py before the logs were read)

The gate run whole in a fake root directory holding HEAD's gate (or the fix) and HEAD's lib.sh, with the stub in place
of the differential -- or, for the `real` set, HEAD's real differential and float_emul.c with the seven real mutants.
W1 and W3 are two frozen kill-table drivers from older rounds, measured the same way; they are context for the class,
not part of this diff.

```
PASS W1 kill479.sh, stub detectors                ~5 rows, 0 failures FIX byte-identical to HEAD
PASS W1 kill479.sh, stub detectors                Mk_kill        FIX byte-identical to HEAD
PASS W1 kill479.sh, stub detectors                Ms_survive     FIX byte-identical to HEAD
PASS W1 kill479.sh, stub detectors                Mc_early       HEAD scored it as a table result; FIX refused it
        HEAD:   Mc_early       *ESCAPED* (clean sweep of 5 rows)
        FIX :   Mc_early       NOLOG     rc=136: no WDC_IDENTIFY_ sentinel -- not scored
PASS W1 kill479.sh, stub detectors                Mc_late        HEAD scored it as a table result; FIX refused it
        HEAD:   Mc_late        KILLED    1 red: stub row b
        FIX :   Mc_late        NOLOG     rc=136: no WDC_IDENTIFY_ sentinel -- not scored
PASS W1 kill479.sh, stub detectors                Mx_exit1       HEAD scored it as a table result; FIX refused it
        HEAD:   Mx_exit1       KILLED    1 red: stub row b
        FIX :   Mx_exit1       NOLOG     rc=1: no WDC_IDENTIFY_ sentinel -- not scored
PASS W1 kill479.sh, stub detectors                Mcf_nocompile  HEAD scored it as a table result; FIX refused it
        HEAD:   Mcf_nocompile  KILLED    does not compile
        FIX :   Mcf_nocompile  BUILDFAIL does not compile -- not a measurement
PASS W1R kill479.sh, REAL #479 detector (80 rows) whole driver output FIX byte-identical to HEAD
PASS W2 gate 3, mixed                             control row    FIX byte-identical to HEAD
PASS W2 gate 3, mixed                             revert287      FIX byte-identical to HEAD
PASS W2 gate 3, mixed                             flushband      FIX byte-identical to HEAD
PASS W2 gate 3, mixed                             tiesaway       FIX byte-identical to HEAD
PASS W2 gate 3, mixed                             modeignored    HEAD scored it as a table result; FIX refused it
        HEAD:   ok   mutant modeignored is DETECTED (must fail)           0
        FIX :   FAIL mutant modeignored is DETECTED (must fail)           got=NOLOG rc=136 want=0
PASS W2 gate 3, mixed                             wlegacyrounds  HEAD scored it as a table result; FIX refused it
        HEAD:   ok   mutant wlegacyrounds is DETECTED (must fail)         0
        FIX :   FAIL mutant wlegacyrounds is DETECTED (must fail)         got=NOLOG rc=136 want=0
PASS W2 gate 3, mixed                             revert303      HEAD scored it as a table result; FIX refused it
        HEAD:   ok   mutant revert303 is DETECTED (must fail)             0
        FIX :   FAIL mutant revert303 is DETECTED (must fail)             got=NOLOG rc=1 want=0
PASS W2 gate 3, mixed                             maskcarry      HEAD scored it as a table result; FIX refused it
        HEAD:   ok   mutant maskcarry is DETECTED (must fail)             0
        FIX :   FAIL mutant maskcarry is DETECTED (must fail)             got=NOLOG rc=0 want=0
PASS W2 gate 3, mixed                             GATE VERDICT   HEAD scored it as a table result; FIX refused it
        HEAD: selftest-float-emul-can-fail: FAIL (1 of 15 checks)
        FIX : selftest-float-emul-can-fail: FAIL (5 of 15 checks)
PASS W2 gate 3, allcrash                          control row    FIX byte-identical to HEAD
PASS W2 gate 3, allcrash                          revert287      HEAD scored it as a table result; FIX refused it
        HEAD:   ok   mutant revert287 is DETECTED (must fail)             0
        FIX :   FAIL mutant revert287 is DETECTED (must fail)             got=NOLOG rc=136 want=0
PASS W2 gate 3, allcrash                          tiesaway       HEAD scored it as a table result; FIX refused it
        HEAD:   ok   mutant tiesaway is DETECTED (must fail)              0
        FIX :   FAIL mutant tiesaway is DETECTED (must fail)              got=NOLOG rc=136 want=0
PASS W2 gate 3, allcrash                          modeignored    HEAD scored it as a table result; FIX refused it
        HEAD:   ok   mutant modeignored is DETECTED (must fail)           0
        FIX :   FAIL mutant modeignored is DETECTED (must fail)           got=NOLOG rc=136 want=0
PASS W2 gate 3, allcrash                          wlegacyrounds  HEAD scored it as a table result; FIX refused it
        HEAD:   ok   mutant wlegacyrounds is DETECTED (must fail)         0
        FIX :   FAIL mutant wlegacyrounds is DETECTED (must fail)         got=NOLOG rc=136 want=0
PASS W2 gate 3, allcrash                          revert303      HEAD scored it as a table result; FIX refused it
        HEAD:   ok   mutant revert303 is DETECTED (must fail)             0
        FIX :   FAIL mutant revert303 is DETECTED (must fail)             got=NOLOG rc=136 want=0
PASS W2 gate 3, allcrash                          maskcarry      HEAD scored it as a table result; FIX refused it
        HEAD:   ok   mutant maskcarry is DETECTED (must fail)             0
        FIX :   FAIL mutant maskcarry is DETECTED (must fail)             got=NOLOG rc=136 want=0
PASS W2 gate 3, allcrash                          flushband      HEAD scored it as a table result; FIX refused it
        HEAD:   ok   mutant flushband is DETECTED (must fail)             0
        FIX :   FAIL mutant flushband is DETECTED (must fail)             got=NOLOG rc=136 want=0
PASS W2 gate 3, allcrash                          GATE VERDICT   HEAD scored it as a table result; FIX refused it
        HEAD: selftest-float-emul-can-fail: PASS (15 checks)
        FIX : selftest-float-emul-can-fail: FAIL (7 of 15 checks)
PASS W2 gate 3, allkill                           whole gate output FIX byte-identical to HEAD
PASS W2 gate 3, real                              whole gate output FIX byte-identical to HEAD
PASS W3 killrow5c.sh scorer, stub census          BASE           FIX byte-identical to HEAD
PASS W3 killrow5c.sh scorer, stub census          Ms             FIX byte-identical to HEAD
PASS W3 killrow5c.sh scorer, stub census          Mk             FIX byte-identical to HEAD
PASS W3 killrow5c.sh scorer, stub census          Mc             HEAD scored it as a table result; FIX refused it
        HEAD:   Mc   census crashes before any token           ///            killed
        FIX :   Mc   census crashes before any token           NOLOG rc=1     NOLOG -- the census did not finish; not scored
PASS W3 killrow5c.sh scorer, stub census          Mc2            HEAD scored it as a table result; FIX refused it
        HEAD:   Mc2  census crashes after 2 of 4 tokens        6/6//          killed
        FIX :   Mc2  census crashes after 2 of 4 tokens        NOLOG rc=1     NOLOG -- the census did not finish; not scored
CONTROLS: 33 of 33 rows as expected
COMPARE_DONE
```

**HEAD's gate, all seven mutants crashed (the gate's own output):**

```
## GATE: selftest-float-emul-can-fail
############################################################
  ok   mutant revert287 could be applied                    ok
  ok   mutant tiesaway could be applied                     ok
  ok   mutant modeignored could be applied                  ok
  ok   mutant wlegacyrounds could be applied                ok
  ok   mutant revert303 could be applied                    ok
  ok   mutant maskcarry could be applied                    ok
  ok   mutant flushband could be applied                    ok
  --   control: differential against the shipped float_emul.c
  ok   unmutated source passes gate 2                       1
  --   mutant revert287: the differential must go red
  ok   mutant revert287 is DETECTED (must fail)             0
  --   mutant tiesaway: the differential must go red
  ok   mutant tiesaway is DETECTED (must fail)              0
  --   mutant modeignored: the differential must go red
  ok   mutant modeignored is DETECTED (must fail)           0
  --   mutant wlegacyrounds: the differential must go red
  ok   mutant wlegacyrounds is DETECTED (must fail)         0
  --   mutant revert303: the differential must go red
  ok   mutant revert303 is DETECTED (must fail)             0
  --   mutant maskcarry: the differential must go red
  ok   mutant maskcarry is DETECTED (must fail)             0
  --   mutant flushband: the differential must go red
  ok   mutant flushband is DETECTED (must fail)             0

selftest-float-emul-can-fail: PASS (15 checks)
```

**The fixed gate on the same set** (the copy the controls ran; the staged file differs from it in full-line comments
only):

```
## GATE: selftest-float-emul-can-fail
############################################################
  ok   mutant revert287 could be applied                    ok
  ok   mutant tiesaway could be applied                     ok
  ok   mutant modeignored could be applied                  ok
  ok   mutant wlegacyrounds could be applied                ok
  ok   mutant revert303 could be applied                    ok
  ok   mutant maskcarry could be applied                    ok
  ok   mutant flushband could be applied                    ok
  --   control: differential against the shipped float_emul.c
  ok   unmutated source passes gate 2                       1
  --   mutant revert287: the differential must go red
  FAIL mutant revert287 is DETECTED (must fail)             got=NOLOG rc=136 want=0
  --   mutant tiesaway: the differential must go red
  FAIL mutant tiesaway is DETECTED (must fail)              got=NOLOG rc=136 want=0
  --   mutant modeignored: the differential must go red
  FAIL mutant modeignored is DETECTED (must fail)           got=NOLOG rc=136 want=0
  --   mutant wlegacyrounds: the differential must go red
  FAIL mutant wlegacyrounds is DETECTED (must fail)         got=NOLOG rc=136 want=0
  --   mutant revert303: the differential must go red
  FAIL mutant revert303 is DETECTED (must fail)             got=NOLOG rc=136 want=0
  --   mutant maskcarry: the differential must go red
  FAIL mutant maskcarry is DETECTED (must fail)             got=NOLOG rc=136 want=0
  --   mutant flushband: the differential must go red
  FAIL mutant flushband is DETECTED (must fail)             got=NOLOG rc=136 want=0

selftest-float-emul-can-fail: FAIL (7 of 15 checks)
```

## 6. Every file the commit carries (`git diff --numstat` disclosure, template section F)

```
  (paths under regress/artifacts/qhmutcrashscore/ are shown relative to it; every one of those files is new)
  +77 -0      CHANGELOG.md                                                             SUMMARIZED (section 6): records
  +28 -2      OUTSTANDING_BUGS.md                                                      SUMMARIZED (section 6): records
  +16 -0      landing_20261105/CITE.txt                                                NOT SHOWN (evidence or kit record)
  +86 -0      landing_20261105/STAGED_DIFF.txt                                         NOT SHOWN (evidence or kit record)
  +47 -0      wkdc_20261105/MD5SUMS.txt                                                NOT SHOWN (evidence or kit record)
  +152 -0     wkdc_20261105/RECEIPT.txt                                                NOT SHOWN (evidence or kit record)
  +21 -0      wkdc_20261105/census/AFFECTED.tsv                                        NOT SHOWN (evidence or kit record)
  +101 -0     wkdc_20261105/census/RETRO_LOGS.out                                      NOT SHOWN (evidence or kit record)
  +50 -0      wkdc_20261105/census/retro_logs.py                                       NOT SHOWN (evidence or kit record)
  +73 -0      wkdc_20261105/controls/CONTROLS.txt                                      INLINED (section 5)
  +126 -0     wkdc_20261105/controls/compare.py                                        NOT SHOWN (evidence or kit record)
  +12 -0      wkdc_20261105/controls/ks_unit.frozen.out                                NOT SHOWN (evidence or kit record)
  +12 -0      wkdc_20261105/controls/ks_unit.out                                       NOT SHOWN (evidence or kit record)
  +37 -0      wkdc_20261105/controls/ks_unit.sh                                        NOT SHOWN (evidence or kit record)
  +9 -0       wkdc_20261105/controls/mm_parse_control.out                              NOT SHOWN (evidence or kit record)
  +47 -0      wkdc_20261105/controls/mm_parse_control.py                               NOT SHOWN (evidence or kit record)
  +6 -0       wkdc_20261105/controls/rerun_ks_legs.log                                 NOT SHOWN (evidence or kit record)
  +15 -0      wkdc_20261105/controls/rerun_ks_legs.sh                                  NOT SHOWN (evidence or kit record)
  +23 -0      wkdc_20261105/controls/run_controls.log                                  NOT SHOWN (evidence or kit record)
  +34 -0      wkdc_20261105/controls/run_controls.sh                                   NOT SHOWN (evidence or kit record)
  +3 -0       wkdc_20261105/controls/run_w1r479.log                                    NOT SHOWN (evidence or kit record)
  +9 -0       wkdc_20261105/controls/run_w1r479.sh                                     NOT SHOWN (evidence or kit record)
  +32 -0      wkdc_20261105/fix/kill479.diff                                           NOT SHOWN (evidence or kit record)
  +27 -0      wkdc_20261105/fix/killrow5c.diff                                         NOT SHOWN (evidence or kit record)
  +42 -0      wkdc_20261105/fix/killscore.sh                                           NOT SHOWN (evidence or kit record)
  +20 -0      wkdc_20261105/fix/selftest_mutation.diff                                 NOT SHOWN (evidence or kit record)
  +51 -0      wkdc_20261105/witness/g3/W2_FIX.allcrash.log                             INLINED, the gate-output part (section 5)
  +44 -0      wkdc_20261105/witness/g3/W2_FIX.allkill.log                              NOT SHOWN (evidence or kit record)
  +46 -0      wkdc_20261105/witness/g3/W2_FIX.mixed.log                                NOT SHOWN (evidence or kit record)
  +44 -0      wkdc_20261105/witness/g3/W2_FIX.real.log                                 NOT SHOWN (evidence or kit record)
  +51 -0      wkdc_20261105/witness/g3/W2_HEAD.allcrash.log                            INLINED, the gate-output part (section 5)
  +44 -0      wkdc_20261105/witness/g3/W2_HEAD.allkill.log                             NOT SHOWN (evidence or kit record)
  +46 -0      wkdc_20261105/witness/g3/W2_HEAD.mixed.log                               NOT SHOWN (evidence or kit record)
  +44 -0      wkdc_20261105/witness/g3/W2_HEAD.real.log                                NOT SHOWN (evidence or kit record)
  +29 -0      wkdc_20261105/witness/k479/W1_FIX.log                                    NOT SHOWN (evidence or kit record)
  +29 -0      wkdc_20261105/witness/k479/W1_HEAD.log                                   NOT SHOWN (evidence or kit record)
  +7 -0       wkdc_20261105/witness/k479real/r479src/FIX/driver.out                    NOT SHOWN (evidence or kit record)
  +7 -0       wkdc_20261105/witness/k479real/r479src/HEAD/driver.out                   NOT SHOWN (evidence or kit record)
  +15 -0      wkdc_20261105/witness/k479real/r479src/W1R_FIX.log                       NOT SHOWN (evidence or kit record)
  +15 -0      wkdc_20261105/witness/k479real/r479src/W1R_HEAD.log                      NOT SHOWN (evidence or kit record)
  +76 -0      wkdc_20261105/witness/mkstub_wdc.py                                      NOT SHOWN (evidence or kit record)
  +15 -0      wkdc_20261105/witness/r5c/W3_FIX.log                                     NOT SHOWN (evidence or kit record)
  +15 -0      wkdc_20261105/witness/r5c/W3_HEAD.log                                    NOT SHOWN (evidence or kit record)
  +25 -0      wkdc_20261105/witness/stub_census.py                                     NOT SHOWN (evidence or kit record)
  +73 -0      wkdc_20261105/witness/stub_diff_ieee_store.c                             INLINED (section 4)
  +44 -0      wkdc_20261105/witness/w1_kill479.sh                                      NOT SHOWN (evidence or kit record)
  +32 -0      wkdc_20261105/witness/w1r_kill479_real.sh                                NOT SHOWN (evidence or kit record)
  +46 -0      wkdc_20261105/witness/w2_gate3.sh                                        NOT SHOWN (evidence or kit record)
  +36 -0      wkdc_20261105/witness/w3_killrow5c.sh                                    NOT SHOWN (evidence or kit record)
  +11 -1      regress/selftest_mutation.sh                                             INLINED (section 2)
  +21 -0      tools/pipeline/check_probe_wiring.py                                     SUMMARIZED (section 6): one MANIFEST block, five (class, note) entries, no logic change
  +2 -2       tools/pipeline/fable_queue.md                                            SUMMARIZED (section 6): records
  +60 -4      tools/pipeline/ledger.json                                               SUMMARIZED (section 6): records
  +6 -6       tools/pipeline/matrix.html                                               SUMMARIZED (section 6): records
  (this)      landing_20261105/BRIEF_PASS2.md                                          NOT SHOWN -- this packet, committed as sent
```

The records, summarized: the ledger row `qhmutcrashscore` (a member of the class row `idlesslow`) is promoted to its own
row and closed with witness `harness:` naming the controls above; the class row `killdrivercrash` (kill-table drivers
that score a dead run by how far it got: 20 affected, one live -- this gate -- and 19 frozen records that are not
patched) is held for the owner's decision on a shared scoring helper; a new LOW row `gate3runbound` records that gate 3
runs each differential with no time bound, so a hanging mutant wedges the gate; `check_probe_wiring.py` gains MANIFEST
entries (class and note) for five preserved scripts; CHANGELOG, OUTSTANDING_BUGS, fable_queue and matrix carry the
round.

## 7. SETTLED PREMISES: none carried -- first brief of this round's review.

## 8. The questions

**Q1 -- the premise audit.  Each premise is stated as a question; answer each TRUE / FALSE / NOT CHECKABLE FROM THIS
PACKET, with the line of the packet that settles it.**

* P1.  Does the differential print exactly one line beginning `DIFF_` -- its verdict, last -- and nothing else that
  `^DIFF_(PASS|FAIL)` could match (section 3)?
* P2.  Does `local rc=$?` capture the status of the run on the line above it, with nothing between them that resets
  `$?` (section 2)?
* P3.  Can `NOLOG rc=<n>` ever equal a check's want (`1` for the control, `0` for a mutant) under `check()`'s string
  comparison, for any status n (sections 2 and lib.sh's check())?
* P4.  Walk all eight runs (the control and seven mutants) through the staged function for each of these endings:
  verdict printed and exit 0; killed by a signal before any output; `exit(1)` after one output line; no output and
  exit 0; verdict printed and then killed.  Which endings does the fix score, which does it refuse, and is each right?
* P5.  Does the gate still run exactly 15 checks with the same names (seven "could be applied", one control, seven
  "is DETECTED"), so nothing that reads the gate's output by check name or count changes?
* P6.  The controls say the whole gate output is byte-identical to HEAD's on completed runs (`allkill`, `real`).  Is
  there any COMPLETED run -- one whose log carries its verdict line -- on which HEAD and the fix print different
  values?

**Q2 -- the smallest edit that breaks the fix and still passes.**  Name the smallest change to the staged function
that re-admits a crashed run as a detection while every row in section 5's `allkill` and `real` sets stays green --
and name the row you expect to stay green.  (Example shapes to consider, not exhaustive: weakening the pattern,
inverting the `||`, moving `local rc=$?`, grepping the wrong file.)

**Q3 -- option-set completeness.**  Other dispositions for a run with no verdict: score it SKIP or SETUP rather than a
failed check; require the verdict on the LAST non-blank line (a proposed shared helper does that for other drivers);
also require exit status 0; count `DIFF_FAIL` instead of DIFF_PASS.  Is the chosen one right for this gate, and is
there a member this list did not name?  (The repository has a sibling, `selftest_mutation_295.sh`, recorded as
refusing a run with `grep M295_RESULT= || SETUP_FAIL` -- its source is not inlined here; say so if that matters.)

**Q4 -- records.**  Is each of these true by the inlined evidence: "with all seven mutants killed by SIGFPE the gate
printed PASS (15 checks)"; "the fixed gate printed FAIL (7 of 15 checks), every mutant NOLOG rc=136"; "the gate's
fifteen checks, their names and its output on completed runs are unchanged"?

If, while verifying a claim, you found something ELSE -- say so.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBKDCP2: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
