# MEASUREMENT TASK — score two mutants against the shipped `m88k_exc_probe.py`

You are the **measurement seat**. This is not a review: I want two numbers and the logs that produced
them. Two other seats predicted a hole in this detector and neither could build it; you can.

## *** SANDBOX RULES — READ THESE FIRST, THEY ARE NOT BOILERPLATE ***

You run with `--dangerously-skip-permissions`, so this brief is the only thing keeping you out of the
project tree. **Every one of these has been violated before and each cost a round:**

1. **NEVER write to `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`, `build/`, `build-asan/`, `est/`, or WSL
   `/tmp/gxsec-build`.** Those are the project trees and two of them carry gate binaries.
2. **COPY THE TREE FIRST.** `cp -a` a fresh clone to your own scratch directory under WSL `/tmp`, and
   do all building and mutating there.
3. Build inside `wsl -d Gentoo` — the default distro has no `make`.
4. **`rm src/cpus/*.o` before each build.** Kept as a conservative clean-build precaution.
5. **CHECK `[ binary -nt source ]` after every build.** `MAKE_RC` has been observed reporting **0 on a
   failed build**, so exit status alone is not proof a binary was produced.
6. **Copy every log you cite into `regress/artifacts/m88kexcdetectorl2/` when you are done** — `/tmp`
   evaporates, and a measurement cited from a volatile path is not a citation.

## THE CLAIM TO TEST

`src/cpus/cpu_m88k.c` has **eleven** `implemented = true;` sites. Four sit on exception classes that
`regress/m88k_exc_probe.py` (59 rows) never drives:

    line 700  case M88K_EXCEPTION_RESET:
    line 705  case M88K_EXCEPTION_INTERRUPT:
    line 710  case M88K_EXCEPTION_INSTRUCTION_ACCESS:
    line 715  case M88K_EXCEPTION_DATA_ACCESS:

(The seven at 720–750 are the `#502` fix's own arms and **are** probed.)

**The prediction is that deleting the flag on an unprobed class re-opens `#502` for that class while
every row stays green — a clean sweep.** I verified the premise by reading; **the score is what I do
not have.**

## WHAT TO RUN

**BASE first.** Build the clone unmodified and run `regress/m88k_exc_probe.py` exactly as
`gate_m88k_rounding.sh` invokes it. Record the score. **If BASE is not a full pass, STOP and say so** —
every later number is meaningless if the baseline is not clean, and I would rather have that sentence
than a table built on a broken base.

Then, each as a **separate build from a fresh copy of the baseline source** (never stacked):

* **M1 — `DATA_ACCESS`**: delete `implemented = true;` at line 715 only. *This is the important one:
  `DATA_ACCESS` is an ordinary page/bus fault, so it is the most guest-reachable of the four.*
* **M2 — `RESET`**: delete `implemented = true;` at line 700 only.

Report for each: **score `n/59`**, and **which rows changed colour relative to BASE**, derived by
diffing the row lines against the BASE log — **not** from the driver's own summary. A driver that
echoes a score it did not recompute is a known failure mode here.

## WHAT I AM ASKING, PRECISELY

1. **BASE score.**
2. **M1 score, and the rows that differ from BASE.**
3. **M2 score, and the rows that differ from BASE.**
4. **Did the mutant text actually land?** Show the `diff` of the mutated file against baseline for
   each. A mutant whose text was never applied scores like a clean build and is indistinguishable
   from a pass — treat MUTANT-TEXT-NOT-FOUND as a hard failure, not a silent skip.

## WHAT I AM NOT ASKING

Do not design a fix. Do not add rows. Do not touch the probe. **If a mutant does not sweep, that is a
result and I want it** — a mutant that refuses to die is a finding about the code or about the mutant,
not a failed errand, and this project treats it as one.

**If the build or the run fails in a way you cannot resolve, say so plainly and stop.** A clear "I
could not build this, here is the error" is worth more than a number I cannot trust — and it is
explicitly what I want rather than a best effort.
