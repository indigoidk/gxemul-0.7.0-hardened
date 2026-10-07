#!/bin/bash
#
#  PROPAGATE ONE EDITED FILE INTO EVERY NO-VPATH BUILD TREE, AND REBUILD EACH.
#
#      MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash \
#        /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/tools/propagate_all_trees.sh \
#        src/devices/dev_wdc.c
#
#  *** THERE ARE FOUR TREES.  precommit_check.sh compares est/ in section A and
#  build/, build-asan/ and -- when //wsl.localhost is reachable -- WSL
#  /tmp/gxsec-build in section B; source cmp only, no binary-freshness check
#  (#560). ***
#
#  On 2026-08-30 `/tmp/gxsec-build` -- the WSL arc tree -- was found holding a PRE-#494
#  `dev_wdc.c` while all three visible trees carried the fix, by a MEASURING SEAT that
#  cmp'd its clone's donor before trusting it.  Filed as `novpadfourth`.
#
#  WHY THAT IS WORSE THAN AN UNCHECKED TREE: scratch clones are made FROM these trees.
#  A clone of a stale donor cmps CLEAN against its donor and carries no sentinel, so
#  the two-part clearance PASSES on it -- the stale-binary trap reached from a
#  direction the sentinel discipline cannot cover.
#
#  THE CLEARANCE IS TWO-PART AND BOTH PARTS ARE RUN HERE, NEVER ASSERTED:
#      (1) the propagated source cmps clean against GXEMUL-SEC
#      (2) [ binary -nt source ]      -- MAKE_RC has been observed 0 on a failed build
#
#  Part 2 is the half this project has been burned by twice.  A tree whose SOURCE cmps
#  clean while its BINARY predates the edit is indistinguishable from a clean tree and
#  carries nothing to say otherwise.
#
set -u

SEC=${GXSEC:-/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC}
ROOT=$(dirname "$SEC")
F=${1:?usage: propagate_all_trees.sh <path-relative-to-tree-root>}
J=${J:-8}
rc=0
n=0

#  est/ is a SOURCE twin with no build of its own -- it gets the copy and the cmp,
#  never a rebuild.  The other three are no-VPATH build trees.
TREES="$ROOT/est $ROOT/build $ROOT/build-asan ${WSLTREE:-/tmp/gxsec-build}"

echo "=============================================================================="
echo "propagate $F into every no-VPATH tree"
echo "=============================================================================="
echo "date $(date '+%Y-%m-%d %H:%M:%S')"
echo "from $SEC"
echo ""

if [ ! -f "$SEC/$F" ]; then
	echo "*** $SEC/$F does not exist -- refusing to propagate nothing"
	echo "PROPAGATE_ALL_FAILED"
	exit 8
fi

for T in $TREES; do
	echo "--------------------------------------------------------------- $T"
	if [ ! -d "$T" ]; then
		echo "  ABSENT -- skipped (and nothing can clone a stale copy of it)"
		continue
	fi
	if [ ! -f "$T/$F" ]; then
		echo "  no $F in this tree -- skipped"
		continue
	fi
	n=$((n + 1))

	cp "$SEC/$F" "$T/$F"
	#  Verified by CONTENT, not by cp's exit status: a cp of the wrong file exits 0.
	#  Measured in makercfalse/propagate_controls_20260830/.
	if cmp -s "$SEC/$F" "$T/$F"; then
		echo "  (1) source cmps clean against SEC          OK"
	else
		echo "  *** (1) FAILED -- the copy did not take"
		rc=8; continue
	fi

	if [ ! -x "$T/gxemul" ]; then
		echo "      no binary in this tree (source twin) -- part 2 not applicable"
		continue
	fi
	if [ "$T/gxemul" -nt "$T/$F" ]; then
		echo "  (2) [ binary -nt source ]                  OK (already fresh)"
		continue
	fi

	echo "      binary older than source -- rebuilding"
	rm -f "$T/${F%.c}.o"
	( cd "$T" && make -j"$J" ) > "$T/.propagate.log" 2>&1
	echo "      make rc = $?"
	if [ -x "$T/gxemul" ] && [ "$T/gxemul" -nt "$T/$F" ]; then
		echo "  (2) [ binary -nt source ]                  OK"
		echo "      $(stat -c '%s bytes  %y' "$T/gxemul")"
	else
		echo "  *** (2) FAILED -- THE TREE IS STALE; DO NOT MEASURE IT.  Last lines:"
		tail -12 "$T/.propagate.log"
		rc=8
	fi
done

echo ""
echo "$n tree(s) carried $F"
if [ "$rc" = 0 ]; then echo "PROPAGATE_ALL_DONE"; else echo "PROPAGATE_ALL_FAILED rc=$rc"; fi
exit "$rc"
