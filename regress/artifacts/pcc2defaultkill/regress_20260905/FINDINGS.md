# FABLE_REGRESS_501_20260905 -- regress seat (fable-only), #501 pcc2defaultkill (ecc4d3b).  Preserved by the main loop from the
# Agent seat's final message (the harness refused the seat's own findings-file write).  Measurement artifacts beside this file.

VERDICT: CONFIRMED -- PASS--reds-on-regression-today--lethal-only-survival-rows-correct--alias-msg-BASE-anchored--disclosures-honest-and-complete.

The shipped 46-row instrument is a sound regression detector for this fix.  MEASURED in a scratch clone of build/ with the LIVE
probe (md5 f7385ca0, the one gate 14 runs): committed fix 46/46 (FABLE_BASE.out); the verbatim exit(1) arm reinstated (the as-run
script's exact DKN->DKO text) 7/46 (FABLE_MEXIT.out) with a 39-row red list byte-identical to table 4's archived M_EXIT.out.
Replaying the gate's own count pattern: BASE 46 per-row checks green / emitted 46 / green 46 / red 0; M_EXIT 7 green / 39 red ->
41 gate checks fail.  Gate 14 goes red on a regression today.

Q1 gate anchor: the 46 row("...") names and the gate's `for v in' list are IDENTICAL, in order.  Longest name 14; the printf is
"%-16s %-14s ..." so a name of length L is followed by (16-L) pad spaces + one separator and the anchor `^name  ' needs two --
THE REAL BOUND IS L <= 15, NOT 14 (both records said 14; safe today, do not inherit 14 as the constant).  Prefix collisions
(named rd / named rd msg; wide wr / wide wr msg) are disambiguated by the two-space anchor.  A too-long name would FAIL loudly
(the per-row check wants exactly 1), not silently stop being counted -- the round's own status-first draft proved it (25/844).
PRETABLE_501c.out mtime 09:08:39 < driver.log 10:45:35.

Q2 lethal-only carve-out (matrix from the 22 table-4 .out files): the seven pure-survival rows (named wr/rd, inword wr/rd, unnamed
wr/rd, alias 0x6a) are killed only by lethal mutants and that is CORRECT -- their got is fate(alive, how), so a non-lethal kill is
impossible by construction, and they DISCRIMINATE (write-side rows stay green under M_RDKILL; in-word rows red under M_OFFKILL
while named/unnamed stay green).  ONE content row is lethal-only: `alias msg' (count "offset 0x2a" == 1) -- no mutant in tables
1/3/4 changes the `%= PCC2_SIZE' fold, so its discrimination is verified at BASE only: derived, not measured (the lethalonly
shape).  LOW; the fold predates #501 and is not in the fix's diff.  FILE: one fold mutant at the next instrument change, or
annotate the row BASE-anchored.  `genctl rt' / `t1cmp word rt' are BASE-anchored negative controls (no mutant perturbs a cased arm).

Q3 contract vs gate: every "edit -> row" line maps to a row with a MEASURED non-lethal kill of the named shape, except the fold
line (Q2).  Disclosed = measured escapes, honest and complete (M_RELOAD 46/46 by design; the pass-4 grid cells, each 46/46; the
`(once)' marker; debug()/fatal(); len 8; end-span; single-offset scoping; per-instance latch).  gate14_501c.log and
gate14_501d.log are byte-identical (91,843 B) -- expected after docstring-only edits.

Q4 what ran: measure.sh (script-file form under WSL): cp -a build/ -> /tmp/gxfable501r; rm dev_pcc2.o; make -j4; [ binary -nt
source ]; BASE 46/46 (13:15:32); .MUTANT dropped; DKN->DKO applied (24 diff lines vs SEC == the as-run's own); rebuilt; M_EXIT
7/46 (13:17:56); restored from SEC + rebuilt + cmp-clean; sentinel cleared (13:17:58); FABLE501R_DONE.  verify.sh: the 39-row red
list byte-identical to the archived M_EXIT.out; BASE/M_EXIT row tables byte-identical to the archived ones (header excluded).
Hygiene verified: build/, build-asan/, est/ untouched (mtimes predate the run; no sentinels); git status shows only the pre-existing
regress/sgi_de_primop_probe.py edit and the untracked _scratchpad/.

Filed / next instrument change (none blocks closure): (1) a fold mutant for `alias msg'; (2) the name-length bound is 15, not 14;
(3) `genctl rt' / `t1cmp word rt' are BASE-anchored negative controls -- say so in the contract.
