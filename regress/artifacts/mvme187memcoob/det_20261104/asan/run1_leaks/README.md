# Run 1 of the sanitizer legs: CONFOUNDED, kept as run, not used

Every session of every leg (the fix included) ended with LeakSanitizer's exit report ("ERROR: LeakSanitizer: detected memory leaks",
exit code 23), so the probe's `asan reports` row counted one hit per session (13) and every session row read a non-zero exit.  The
memory-error question these legs ask was not measured.  The repo's own ASAN gate runs with leak detection off
(regress/gate_asan_sweep.sh: `export ASAN_OPTIONS=detect_leaks=0:abort_on_error=0:print_summary=1:verify_asan_link_order=0` and
`export UBSAN_OPTIONS=print_stacktrace=0`); run 2 (the parent directory) uses exactly those.  PREDICTION_asan.md was written before run 1
and still precedes run 2.
