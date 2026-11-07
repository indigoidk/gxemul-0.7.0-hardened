#!/bin/bash
#  killscore.sh -- ONE scoring rule for kill-table drivers.  Source it; it defines one function and
#  sets nothing else.  Proposed landing path: GXEMUL-SEC/regress/killscore.sh (ledger row
#  `killdrivercrash`).
#
#  WHY IT EXISTS.  A driver that counts FAIL lines in a log, or compares extracted tokens with an
#  expected value, scores a run by HOW FAR IT GOT.  Measured on HEAD's own drivers with stub
#  detectors (_scratchpad/wkdc/): a run killed by SIGFPE before its first FAIL row scores
#  "*ESCAPED* (clean sweep)", one killed after a FAIL row scores "KILLED 1 red", a run that called
#  exit(1) -- the host-kill shape this project removes -- scores "KILLED", and gate 3 goes GREEN with
#  every one of its seven mutants crashed.  Scoring from an END TOKEN is not enough on its own:
#  killrow5c.sh does that, and a missing token reads as a MISMATCH, and a mismatch reads "killed".
#
#  THE RULE: only a run whose LAST LINE is its completion sentinel is scored.  Anything else is
#  NOLOG -- with the run's exit status, so a signal death (rc >= 128) is visible -- and NOLOG is
#  never KILLED and never ESCAPED.  A mutant that crashes the detector is a RESULT, but it is a
#  different result from a measured kill, and it must not render the same.  (A build failure is the
#  driver's to report as BUILDFAIL: precommit E2's rule -- "a build fault is a FAULT, not a
#  detection".)  This is mutmeasure.py's parse() rule (NOLOG before any score) in ten lines of shell.
#
#  ks_score LOG RC SENTINEL_ERE COUNT_ERE
#      LOG          the run's captured stdout+stderr
#      RC           the run's exit status ($? straight after it)
#      SENTINEL_ERE an extended regex the LOG's LAST NON-BLANK LINE must match -- the detector's
#                   completion sentinel (WDC_IDENTIFY_(PASS|FAIL), *_DONE, the last token it prints)
#      COUNT_ERE    the lines to count in a COMPLETED log (e.g. '^  FAIL'); "-" counts nothing
#  prints exactly one word-group on stdout:
#      NOLOG rc=<RC>     the LOG is absent, empty, or its last line is not the sentinel
#      <n>               a completed run: the number of COUNT_ERE lines (0 when COUNT_ERE is "-")
#  returns 0 for a completed run, 3 for NOLOG.
ks_score() {
	if [ "$#" -ne 4 ]; then
		echo "NOLOG rc=usage"; return 3
	fi
	#  the last NON-BLANK line: a trailing newline or blank line is not a lost sentinel, but anything
	#  printed after the sentinel is (it is refused loudly, never scored silently).
	if [ ! -s "$1" ] || ! grep -v '^[[:space:]]*$' "$1" | tail -n 1 | grep -qE -- "$3"; then
		echo "NOLOG rc=$2"; return 3
	fi
	if [ "$4" = "-" ]; then echo 0; else grep -cE -- "$4" "$1"; fi
	return 0
}
