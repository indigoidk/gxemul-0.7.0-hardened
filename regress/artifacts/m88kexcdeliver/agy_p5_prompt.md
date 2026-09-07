You are the agy MEASURING seat on pass 5 of GXemul round #502 (`m88kexcdeliver`: MC88100 exception delivery in
`GXEMUL-SEC/src/cpus/cpu_m88k.c`; an ordinary emulator-correctness round, plain engineering vocabulary).  Open your answer with the
liveness token AGY_M88KEXC_P5_ALIVE_20260906 and quote the first line of
C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\m88kexc\brief_m88kexc_p5.md verbatim.  Then READ THAT BRIEF IN FULL -- it inlines the repair
diff, table 5, the contract closure, the denominator and THE ONE QUESTION: does a clean-sweep mutant exist in the (d) DEPENDS-ON
enumeration of the SHIPPED COMPOSITE (the #502 fix + probe v5, 29 fault rows)?  You BUILD AND MEASURE; do not only read.

ONE CANDIDATE IS ALREADY NAMED BY A READING SEAT AND MUST BE MEASURED FIRST: in `m88k_exception()` the fallback predicate
`if (vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented)` (M88K_EXCEPTION_USER_TRAPS_START == 128) -- change it to
`vector < 127` (equivalently `M88K_EXCEPTION_USER_TRAPS_START - 1`).  Prediction: 29/29, because no row names vector 127 (the rows
that pin the fallback window are resid50 and sfu1h in its middle and usertb at 128 just outside it).  Measure it.  Then build up to
FIVE MORE candidates of your own from the enumeration (predicates dominating the diff's edited lines up to the function boundary:
switch 1's class labels, the fallback predicate, the SFRZ re-route's `PSR & SFRZ` and `is_trap`, the tail switch's labels; operand
swaps drawn only from fields the guarded bodies read; joint cells where the body tests them) and score each.  A 29/29 on a mutant that is
not equivalent by construction is a floor breach: give the exact edit and the row that should have caught it.

HARD RULES (each measured on this project):
* The tree is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\src\` -- there is a pristine 2021 copy at `C:\DocumentNoSnc\CC\GXEMUL\src\` and two
  under `_archive\`; they are NOT the fork.  NEVER write to GXEMUL-SEC, build, build-asan, est, or the WSL tree /tmp/gxsec-build.
* Build and run inside WSL: `wsl -d Gentoo` (the default distro has no make).  Make a SCRATCH CLONE: inside WSL,
  `rm -rf /tmp/gxagy502 && cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build /tmp/gxagy502` -- build/ is the FIX build and its
  `src/cpus/cpu_m88k.c` is byte-identical to GXEMUL-SEC's (verify with `cmp`; if not, `cp` from
  /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/cpu_m88k.c).  Rebuild the baseline in the clone FIRST:
  `cd /tmp/gxagy502/src/cpus && rm -f cpu_m88k.o && make -s -j4 && cd /tmp/gxagy502 && make -s -j4`, then check
  `[ /tmp/gxagy502/gxemul -nt /tmp/gxagy502/src/cpus/cpu_m88k.c ]` -- make has reported exit 0 on a failed build here, so the
  timestamp check is the real test.  Put your scripts in C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\m88kexc\agy_p5\ and invoke them by
  path (`wsl -d Gentoo -- bash /mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/m88kexc/agy_p5/<script>.sh`); do not pass multi-line
  bodies on the command line.
* For each mutant: write a `.MUTANT` file into the clone first; apply the edit with a script that asserts the find-text occurs EXACTLY
  ONCE (a missing find-text is a null mutant, not a kill); rebuild (`rm -f cpu_m88k.o` first); check the binary is newer than the
  source; run the probe; then restore the file by `cp` FROM GXEMUL-SEC (never from a backup), `cmp`, rebuild, and remove the sentinel.
* The probe: `cp /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/m88k_exc_probe.py /tmp/gxagy502/probe.frozen.py` (md5 must be
  96ab47a0) and run `python3 -u /tmp/gxagy502/probe.frozen.py /tmp/gxagy502/gxemul > <log>` inside WSL (~40 s per run; WSL's python3
  is real -- git-bash's `python3` is a Windows Store stub).  It prints `M88KEXC_ROW=<name> RESULT=<word> ...` lines,
  `M88KEXC_RESULT=<delivered>/29` and `M88KEXC_DONE`; cite only logs carrying the DONE sentinel; keep every log under
  C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\m88kexc\agy_p5\ (BASE.out, M_<name>.out).
* Do not run any gate or battery; do not touch the panel directories.

DELIVERABLE, written to C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\m88kexc\agy_p5.md AND printed: VERDICT LINE FIRST (CLOSE THE CHAIN /
ONE MORE REPAIR: <which>), then a table of every mutant you built (exact edit, score X/29, red rows), then your own denominator,
then anything else -- under a page.  If you cannot build or run, say so plainly and stop; that is a real answer.
