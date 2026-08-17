#!/bin/bash
#  THE ONE ENTRY POINT FOR THE FULL BATTERY -- nightly OR session.  Always run
#  the battery through this script so the lock below actually coordinates.
#
#  It exists to kill two failure modes, both MEASURED on 2026-08-14:
#    * ORPHANED.  A battery launched from a Claude Code background shell dies
#      when that process exits.  One reached 7 of 16 gates with 0 FAIL rows,
#      wrote NO verdict token, and the only tell was a log mtime 4.4 h stale.
#      There is no error marker for this.  Running from Windows Task Scheduler
#      removes the Claude Code process from the dependency chain entirely.
#    * CONTAMINATED.  gate_ab carries a WALL-CLOCK oracle (300 s per luna88k
#      boot against a ~100 s normal), so interactive work on the host yields a
#      FAIL indistinguishable from a real capability regression.  Unattended at
#      03:00 is the mitigation UNTIL queue #35 makes that oracle deterministic.
#
#  Written to a FILE deliberately: $VARS and $? do NOT survive
#  `wsl -- bash -c '...'` -- git-bash expands first, which once made a
#  REGRESS_FAIL run read as exit 0.

set -u
#  ROOT IS DERIVED FROM THIS SCRIPT'S OWN LOCATION, not hardcoded.  This file lives in
#  GXEMUL-SEC/tools/, so the project root is two levels up.  It used to carry an absolute
#  path, which is only half-tracked: a fresh clone anywhere else would have run against
#  whatever happened to be at the old address, or nothing.  $GXROOT overrides for testing.
_HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
ROOT="${GXROOT:-$(cd "$_HERE/../.." && pwd)}"
SEC=$ROOT/GXEMUL-SEC
OUT=$ROOT/_scratchpad/nightly
STAMP=$(date +%Y%m%d_%H%M%S)
LOG=$OUT/battery_$STAMP.log
SUM=$OUT/verdict_$STAMP.txt
LOCK=$OUT/.lock

mkdir -p "$OUT"

#  selftest_mutation.sh does rm -rf on the shared gate workdir, so a second
#  battery would delete the first one's tree mid-run.  mkdir is the atomic test.
if ! mkdir "$LOCK" 2>/dev/null; then
	echo "LOCK HELD ($LOCK) -- another battery is running.  Refusing." > "$SUM"
	exit 8
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

#  *** STAMP THE COMMIT.  A verdict that does not name what it tested cannot be
#  attributed to anything -- 24 commits once shipped against a battery that was
#  never run, and a red result could not have been pinned on any of them. ***
#  safe.directory: the repo is Windows-owned, and WSL git otherwise refuses.
#  Read-only only; NEVER push from WSL.
HEADSHA=$(git -C "$SEC" -c safe.directory='*' rev-parse --short HEAD 2>/dev/null || echo UNKNOWN)
DIRTY=$(git -C "$SEC" -c safe.directory='*' status --porcelain 2>/dev/null | head -5)

cd "$SEC/regress" || { echo "no regress dir at $SEC/regress" > "$SUM"; exit 9; }

{
	echo "HEAD=$HEADSHA"
	if [ -n "$DIRTY" ]; then
		#  A dirty tree means the verdict describes something that is not in
		#  any commit.  Report it rather than letting it read as a clean pass.
		echo "TREE_DIRTY=YES  *** VERDICT DOES NOT DESCRIBE A COMMIT ***"
		echo "$DIRTY" | sed 's/^/    /'
	else
		echo "TREE_DIRTY=no"
	fi
	echo "START=$(date '+%F %T')"
} > "$SUM"

./run.sh > "$LOG" 2>&1
rc=$?

#  FOUR signals, cross-checked.  No single one has ever been trustworthy: the
#  exit status was mis-captured once, and REGRESS_PASS_WITH_GAPS (exit 3) is NOT
#  a pass -- a SKIP is a coverage gap, not evidence.
{
	echo "END=$(date '+%F %T')"
	echo "RUN_SH_EXIT=$rc"
	echo "VERDICT_TOKEN=$(grep -oE 'REGRESS_(PASS_WITH_GAPS|PASS|FAIL|NOTHING_RAN)' "$LOG" | tail -1)"
	echo "COVERAGE=$(grep -oE 'GATE_COVERAGE=[^ ]*' "$LOG" | tail -1)"
	echo "TALLY=$(grep -oE 'passed [0-9]+ +failed [0-9]+ +skipped [0-9]+' "$LOG" | tail -1)"
	echo "LOG=$LOG"
	echo "---- per-gate ----"
	sed -n '/^## SUMMARY/,$p' "$LOG" | grep -E '^  (PASS|FAIL|SKIP)'
	echo "---- FAIL rows ----"
	grep -n '^  FAIL' "$LOG" | head -25
	echo "---- gate_ab luna88k triple ----"
	echo "     LOAD DISCRIMINATOR: prebatch is a HARDCODED commit (2ffc91e), so"
	echo "     if PREBATCH's own timing moved between runs, the HOST moved -- not"
	echo "     the source.  Gate 5 boots the same luna88k with the same binary"
	echo "     and is the independent witness."
	grep -E '^ +(pristine|prebatch|HEAD) ' "$LOG" || echo "(gate_ab printed no triple)"
	echo "---- gate 5 luna88k markers (the independent witness) ----"
	grep -E 'MARKER_login_|BOOT_REACHED' "$LOG" | head -4
} >> "$SUM"

#  Plain copy, not a symlink: /mnt/c does not carry symlinks reliably.
cp -f "$SUM" "$OUT/LATEST.txt" 2>/dev/null
exit $rc
