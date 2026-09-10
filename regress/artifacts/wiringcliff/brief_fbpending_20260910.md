# wiringcliff / fbpending -- WIRING READING: the exact edits that wire fbpending_witness.py into a gate and discharge the selfmutant exemption lane

Please do not simply ratify. Check the premises, not just the derivations. ANALYSIS with exact proposed
shell/text edits quoted (no file is to be written by you). VERDICT LINE FIRST. Test-harness engineering.

## THE TREE
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`. Read `regress/fbpending_witness.py` (its header, usage, verdict
block near the end: FBPENDING_CONTROL / FBPENDING_COVERAGE / FBPENDING_SYMPTOM / FBPENDING_VERDICT,
`sys.exit(0 if good else 1)`), `regress/gate_offline.sh` (the selfmutant manifest: `SM_EXEMPT` near `:1084`,
the loop near `:1090-1120`, `selfmutant_one` calls, `exempt_expired` near `:1143-1167`, and the
`diff_fbpending_bound.c` mentions near `:1259-1277`), `regress/selfmutants/` (the `fbpending_bound.old`,
`.new`, `.why` fragments), `regress/gate_hygiene.sh` (a comment mentions fbpending near `:485`),
`regress/lib.sh` (`check`, `check_min`, `degrade`, `gate_skip`), and
`tools/pipeline/check_probe_wiring.py`'s EXEMPT entry for `fbpending_witness.py`.

## SETTLED (say which you cannot verify)
S1. `fbpending_witness.py <gxemul-binary> <four-byte-raw-stub> [--slices N] [--slice-seconds S]` free-runs
    a footbridge (`cats`) guest for ~86 s and exits 0 iff FBPENDING_VERDICT=PASS (control OK, coverage OK,
    symptom ABSENT). Its report-only mode ends on eleven control rows. The 2026-09-09 wiringcliff ruling:
    wire it with NO CAP as an APPARATUS-ROT row (its `--expect-cap` and `--learn` modes are the wrong
    instrument; the bound's VALUE is already gated by an equality in `diff_fbpending_bound.c` via
    gate_offline.sh), and discharge the `fbpending_bound:2026-09-20` SM_EXEMPT lane in the same edit.
S2. `gate_offline.sh:1082` says the `.old/.new/.why` fragments for fbpending_bound are committed and "the
    lane is a wiring job, not a design one". The selfmutant manifest requires every `diff_*.c` stem to be
    COVERED by a real `selfmutant_one` call or dated-exempt.
S3. Wiring a load-sensitive ~90 s probe belongs in a gate that already runs long free-running guests and
    has no wall-clock oracle of its own that the extra load would perturb; it must not sit after a
    `gate_skip` that exits the gate (silent coverage loss scored SKIP).

## THE QUESTIONS -- answer with the exact text you would add, quoted
Q1. The selfmutant lane: what does `selfmutant_one` take (read two existing calls and quote them), what
    do `fbpending_bound.old/.new/.why` contain, and what is the EXACT `selfmutant_one ...` line that covers
    the stem so `fbpending_bound:2026-09-20` can be deleted from SM_EXEMPT? Does the `.why` warn against a
    particular mutant form or CC flag? Does the differential build under the gate's line as-is?
Q2. Which gate hosts the witness (gate_hygiene.sh, gate_ab.sh, or gate_offline.sh?): name the one whose
    existing sections already free-run guests without a load-sensitive oracle, quote the section you would
    place it AFTER, and write the section: the invocation with the gate's own binary variable and the raw
    stub it needs (does the gate already have a four-byte stub, or does the witness create one?), a `check`
    on `FBPENDING_VERDICT=PASS`, `check`s on CONTROL=OK and COVERAGE=OK separately (so "not run long
    enough" and "broken" cannot render alike), and a `degrade` (not `gate_skip`) branch when the binary or
    the stub is missing. Estimate the wall cost.
Q3. The `check_probe_wiring.py` side: quote the EXEMPT entry to delete and confirm the checker will then
    derive the invocation from the gate script (how does it derive -- by grepping the probe's basename in
    `regress/*.sh` at command position?). Would a `python3 "$HERE/fbpending_witness.py"` form be found?
Q4. What could make this row a check-that-cannot-fail? (E.g. a stub path that always exists, a verdict
    grep that matches the echoed command line.) Name the negative control: the mutant of `dev_footbridge.c`
    that must make FBPENDING_SYMPTOM=PRESENT, and whether the differential already carries it.
State what you read versus what you took from this packet.
