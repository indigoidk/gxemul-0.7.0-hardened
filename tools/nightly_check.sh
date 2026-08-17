#!/bin/bash
#  THE DEAD-MAN SWITCH.  Run it from git-bash or WSL any time after the nightly window:
#      bash /c/DocumentNoSnc/cc/GXEMUL/nightly_check.sh [max_age_hours]
#
#  *** WHY THIS EXISTS, and it is the sharpest thing an adjudicating seat said on
#  2026-08-15: THE NIGHTLY BATTERY IS UNCONDITIONAL, YET NOTHING MAKES THE ABSENCE OF A
#  TERMINAL RECORD A FAIL.  Every threshold in this harness assumes the gate ran.  A run
#  that never starts -- logged-out session, task never fired, process killed by a reboot --
#  produces NO RED ROW ANYWHERE.  It is the one false pass no gate row can see, because
#  every gate row lives inside the run that did not happen. ***
#
#  This is the generalisation of a task that was being tracked by hand ("check tomorrow
#  whether the battery fired"), which is itself the tell: a check a human has to remember is
#  a check that will eventually not happen.
#
#  Two failure modes it separates, because they need different fixes:
#    NEVER RAN   no verdict file at all, or the newest is older than the window.
#                The scheduled task is "Interactive only", so a logged-out or sleeping
#                machine skips it SILENTLY with no error recorded anywhere.
#    RAN BADLY   a verdict exists but its four signals disagree, or it is not REGRESS_PASS.
#
#  It deliberately does NOT parse the battery's gate output.  That is the battery's job and
#  it already does it.  This asks the only question the battery cannot ask about itself.
set -u
#  ROOT IS DERIVED FROM THIS SCRIPT'S OWN LOCATION, not hardcoded.  This file lives in
#  GXEMUL-SEC/tools/, so the project root is two levels up.  It used to carry an absolute
#  path, which is only half-tracked: a fresh clone anywhere else would have run against
#  whatever happened to be at the old address, or nothing.  $GXROOT overrides for testing.
#
#  THE MIGRATION GOT THIS WRONG ONCE AND THE CHECK CAUGHT ITSELF.  The old two-line form was
#  `ROOT=${ROOT:-/abs/path}` followed by `[ -d "$ROOT" ] || ROOT=/mnt/abs/path`, and the
#  rewrite replaced only the second path -- leaving `[ -d "$ROOT" ] ||` dangling, which then
#  swallowed the new _HERE assignment as its right-hand side.  So _HERE was set ONLY when the
#  old path was missing, ROOT resolved EMPTY, and this script looked for its verdicts in
#  `/_scratchpad/nightly`.  It reported NIGHTLY_CHECK_FAIL rather than passing quietly, which
#  is precisely what a dead-man switch is for -- including when the thing that broke is itself.
_HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
ROOT="${GXROOT:-$(cd "$_HERE/../.." && pwd)}"
[ -n "$ROOT" ] && [ -d "$ROOT/_scratchpad" ] || {
	echo "NIGHTLY_CHECK_FAIL  cannot resolve the project root from $_HERE" >&2
	exit 1
}
OUT=$ROOT/_scratchpad/nightly
MAX_AGE_H=${1:-176}         # WEEKLY cadence: small unit tests any time, but the FULL
                            # battery runs SUNDAYS 18:00 (task GXemul-weekly-battery),
                            # moved there from Saturday 03:00 so the batched regression
                            # review has a fresh battery to review. 176 h = 7 days + 8 h
                            # of slack. Pass a smaller window explicitly after an
                            # on-demand run.
                            #
                            # (The value was moved to 176 with the schedule; this comment
                            # still said "170 h" and "Saturdays 03:00" afterwards, which is
                            # the stale-record class -- corrected 2026-08-15.)
rc=0

say () { printf '%s\n' "$*"; }
bad () { rc=1; printf '  FAIL  %s\n' "$*"; }
ok  () { printf '  ok    %s\n' "$*"; }

say "=== nightly dead-man check  ($(date '+%F %H:%M:%S'), window ${MAX_AGE_H}h) ==="

if [ ! -d "$OUT" ]; then
    bad "NO VERDICT DIRECTORY AT ALL ($OUT) -- the battery has never produced output."
    say  "        The scheduled task is 'Interactive only': a logged-out or sleeping"
    say  "        machine skips it silently.  Check: schtasks /query /TN GXemul-nightly-battery"
    say  "NIGHTLY_CHECK_FAIL"; exit 1
fi

newest=$(ls -1t "$OUT"/verdict_*.txt 2>/dev/null | head -1)
if [ -z "$newest" ]; then
    bad "NO VERDICT FILE -- the directory exists but nothing has completed."
    say  "NIGHTLY_CHECK_FAIL"; exit 1
fi

#  Age.  A stale verdict is the SAME failure as a missing one: it means the most recent
#  scheduled run did not happen, and reading yesterday's green as today's is exactly the
#  "a green row means nothing" class this harness exists to prevent.
age_s=$(( $(date +%s) - $(stat -c %Y "$newest") ))
age_h=$(( age_s / 3600 ))
if [ "$age_h" -gt "$MAX_AGE_H" ]; then
    bad "NEWEST VERDICT IS ${age_h}h OLD (limit ${MAX_AGE_H}h): $(basename "$newest")"
    say  "        A stale verdict is not evidence about today.  The run did not happen."
else
    ok "verdict is ${age_h}h old: $(basename "$newest")"
fi

#  All four signals, cross-checked.  No single one has ever been trustworthy here: the exit
#  status was mis-captured once, and REGRESS_PASS_WITH_GAPS (exit 3) is NOT a pass -- a SKIP
#  is a coverage gap, not evidence.
get () { grep -m1 "^$1=" "$newest" 2>/dev/null | cut -d= -f2-; }
exitst=$(get RUN_SH_EXIT); token=$(get VERDICT_TOKEN)
cov=$(get COVERAGE);       tally=$(get TALLY)
head_sha=$(get HEAD);      dirty=$(get TREE_DIRTY)

[ "$exitst" = 0 ] && ok "RUN_SH_EXIT=0" || bad "RUN_SH_EXIT=${exitst:-(absent)}"
case "$token" in
*REGRESS_PASS) ok "VERDICT_TOKEN=$token" ;;
*PASS_WITH_GAPS*) bad "VERDICT_TOKEN=$token -- exit 3 is NOT a pass; a SKIP is a coverage gap" ;;
*) bad "VERDICT_TOKEN=${token:-(absent)}" ;;
esac
case "$tally" in
*"failed 0"*"skipped 0"*) ok "TALLY=$tally" ;;
"") bad "TALLY absent -- the battery did not reach its summary" ;;
*) bad "TALLY=$tally -- any non-zero failed/skipped needs reading" ;;
esac
[ -n "$cov" ] && ok "$cov" || bad "COVERAGE absent"

#  A verdict that does not name what it tested cannot be attributed to anything.
[ -n "$head_sha" ] && ok "HEAD=$head_sha" || bad "HEAD not stamped -- verdict unattributable"
case "$dirty" in
no) ok "TREE_DIRTY=no" ;;
"") bad "TREE_DIRTY not recorded" ;;
*)  bad "TREE_DIRTY=$dirty -- the verdict describes something that is in no commit" ;;
esac

say ""
[ $rc = 0 ] && say "NIGHTLY_CHECK_PASS" || say "NIGHTLY_CHECK_FAIL"
exit $rc
