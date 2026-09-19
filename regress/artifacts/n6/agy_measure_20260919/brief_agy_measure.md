# agy -- ONE BOUNDED MEASUREMENT for round #539 (n6): build the fixed footbridge tree in YOUR OWN COPY and score three runs

You are the independent compile-and-measure front end (the road that does not share the Agent-tool budget).  READ-ONLY on
every project tree: NEVER write under `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`, `est`, `build`, `build-asan` or `/tmp/gxsec-build`,
and NEVER run any `regress/gate_*.sh`.  Work only in a copy.  Ordinary bounds-and-error-handling language.  If any step
below cannot be done, say so plainly and stop -- a partial answer that says what failed is a real answer.

## THE ROUND, in three lines
`GXEMUL-SEC/src/devices/dev_footbridge.c` (working tree, uncommitted #539): the `case IRQ_ENABLE_SET` READ branch no longer
ends the process; `odata = d->irq_enable` is kept.  `GXEMUL-SEC/regress/footbridge_sites_probe.py` (working tree) gained arm E
with rows EC1,EA1,E0,E1,E2,E3,E6,E5,E4 (19 rows) and its kill arm K now reads `+0x18c`.  The main loop measured: base 19/19;
mutant (a) = the removed fatal()+exit(1) reinstated verbatim -> 10/19 (the E arm dies at E0); z_silentexit = the CLEAR read's
complaint deleted, its exit(1) kept -> 18/19 (K1 red).  YOUR job is the INDEPENDENT measurement of exactly those three.

## STEPS (all inside WSL Gentoo: `wsl -d Gentoo` -- the default distro has no make)
1. `rm -rf /tmp/gxagy539 && cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build /tmp/gxagy539` (a configured tree; no `./configure` needed).
2. Restore every uncommitted `src/` file OTHER than dev_footbridge.c to HEAD:
   `cd /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC && git status --porcelain -- src` lists them; for each,
   `git show HEAD:<path> > /tmp/gxagy539/<path>`.  Then copy the WORKING-TREE footbridge in:
   `cp /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_footbridge.c /tmp/gxagy539/src/devices/dev_footbridge.c`
   and print `md5sum` of both copies (they must match).
3. Build: `cd /tmp/gxagy539 && rm -f src/cpus/*.o src/devices/*.o src/machines/*.o gxemul && make -j4 > /tmp/gxagy539/make_base.log 2>&1; echo rc=$?`
   then CHECK FRESHNESS yourself: `[ gxemul -nt src/devices/dev_footbridge.c ] && echo FRESH || echo STALE` -- make's rc has
   been observed 0 on a failed build; STALE means stop and report.
4. Freeze the probe: `cp /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/footbridge_sites_probe.py /tmp/gxagy539/probe.frozen.py`
   (md5sum it); the stub: `printf '\x00\x00\xa0\xe1' > /tmp/gxagy539/arm_stub.bin`.
5. BASE run: `cd /tmp/gxagy539 && python3 -u probe.frozen.py /tmp/gxagy539/gxemul /tmp/gxagy539/arm_stub.bin > /tmp/gxagy539/base.raw 2>&1`;
   report the `ROWS=` line, `FOOTBRIDGE_SITES_CONTROL=`, `FOOTBRIDGE_SITES_PASS/FAIL`, and every row line that ends in FAIL.
6. MUTANT (a): in /tmp/gxagy539/src/devices/dev_footbridge.c, inside `case IRQ_ENABLE_SET:`'s `else` (the READ branch), after
   the line `odata = d->irq_enable;` insert these two lines (tab-indented like their neighbours):
       fatal("[ WARNING: footbridge read from ENABLE SET? ]\n");
       exit(1);
   Show the edited branch with `grep -n -B3 -A6 'ENABLE SET' src/devices/dev_footbridge.c`.  Rebuild as in step 3 (rm the .o
   and the binary first; check FRESH).  Run the probe to `/tmp/gxagy539/mut_a.raw`; report as in step 5.
7. RESTORE: copy the working-tree footbridge back, `cmp` it against `/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_footbridge.c`
   (must be identical), rebuild, check FRESH.
8. MUTANT z_silentexit: in `case IRQ_ENABLE_CLEAR:`'s READ branch (`else`), DELETE the two-line `fatal("[ WARNING: footbridge read from "
   "ENABLE CLEAR? ]\n");` statement and KEEP `exit(1);`.  Show it with grep as above.  Rebuild (FRESH), run to
   `/tmp/gxagy539/mut_z.raw`, report.  Then RESTORE as in step 7 and say the final cmp result.
9. Copy `base.raw`, `mut_a.raw`, `mut_z.raw`, `make_base.log` and the probe md5 to
   `/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/n6/agy_measure_20260919/` (this scratch directory is the ONLY project-side
   place you may write).

## REPORT (VERDICT LINE FIRST)
Three lines: `base: ROWS=x of 19 <PASS|FAIL> reds=<list>`, `mutant_a: ...`, `z_silentexit: ...`; then the freshness checks,
the md5s, the final restore cmp, and anything that surprised you.  Expected if the main loop is right: 19/19 PASS;
10/19 FAIL with the E-arm rows red (EC1,EA1,E0,E1,E2,E3,E6,E5,E4); 18/19 FAIL with K1 red.  If you see something else,
that is the finding -- report it exactly.
