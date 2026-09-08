# MEASUREMENT JOB — build ONE mutant and score it against a shipped detector

**You are being asked to MEASURE, not to design.** Report the score and what reddened. If you
cannot build or cannot run, **say so plainly and stop** — an honest "could not" is worth more than
a guess, and this project treats an unmeasured prediction differently from a measured result.

---

## *** SANDBOX RULES — READ FIRST.  You run with no sandbox. ***

**NEVER write to `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`, `build/`, `build-asan/`, `est/`, or
`/tmp/gxsec-build`.** Those are the project's live trees and one stray write costs a day.

**COPY THE TREE, BUILD THE COPY:**

```sh
rm -rf /tmp/gxm88k && cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build /tmp/gxm88k
cd /tmp/gxm88k
```

Everything below happens in `/tmp/gxm88k`. Verify at the end that
`git -C /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC status --porcelain` is unchanged by your work.

## Build traps — all three are real and none is guessable

1. Build inside **`wsl -d Gentoo`**. The default distro has no `make`.
2. **`rm src/cpus/*.o` before every build.** Conservative clean-build precaution in this tree.
3. ***`MAKE_RC` HAS BEEN OBSERVED REPORTING 0 ON A FAILED BUILD.*** Do not trust the exit status —
   check **`[ /tmp/gxm88k/gxemul -nt /tmp/gxm88k/src/cpus/cpu_m88k.c ]`**, i.e. that the binary is
   genuinely NEWER than the source you edited. If it is not, the build failed and any score you
   report is of the OLD binary.

---

## Step 1 — BASELINE

Build the copy **unmodified** and score it:

```sh
cd /tmp/gxm88k && rm -f src/cpus/*.o && make
python3 -u /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/m88k_exc_probe.py /tmp/gxm88k/gxemul BASE
```

**Report the baseline RESULT line verbatim.** If it is not a full score, STOP and report that —
a mutant score means nothing against a baseline that is already failing.

## Step 2 — THE MUTANT

In `/tmp/gxm88k/src/cpus/cpu_m88k.c`, change every **`implemented = true;`** inside the exception
dispatch to:

```c
		implemented = (cpu->machine->ncpus < 2);
```

**DERIVE THE SITE LIST; DO NOT TRUST A COUNT FROM ME.** Run:

```sh
grep -n 'implemented = true' /tmp/gxm88k/src/cpus/cpu_m88k.c
```

*** A PREMISE OF MINE TO CHECK, AND I BELIEVE IT IS WRONG. ***  The queue row that prompted this job
says the edit applies to **seven** arms. My own grep of the tree returns **eleven** occurrences.
**Report how many you actually found and how many you changed**, and if some are outside the
exception dispatch (a different function, or a path the detector cannot reach), say which and leave
them alone — then tell me. The count discrepancy is itself a finding.

Rebuild (with the `rm` and the freshness check) and score it the same way, label `M1`.

## Step 3 — REPORT

* the BASELINE result line and the MUTANT result line, verbatim;
* **exactly which rows reddened**, by name, or "none";
* how many sites you found and changed;
* the freshness check result for both builds.

**The prediction under test is that the mutant scores a CLEAN SWEEP — every row still green.** Two
seats predicted that independently from reading, neither could build it, and both said so honestly.

* **If it sweeps**, that is a real coverage hole in the detector, and saying so with a number is the
  whole point of this job.
* **If it does NOT sweep**, the prediction was wrong and the row closes as a measured non-finding.
  **That is an equally good outcome** — record which rows killed it.

## Restore

Nothing to restore: you worked in `/tmp/gxm88k`, which is disposable. Confirm the project tree is
untouched and say so.

## Rules

* Report what the commands PRINTED, not what you expected them to print.
* If a step fails, report the failure and stop rather than working around it.
* Do not edit the probe. Do not edit anything under `GXEMUL-SEC`.
