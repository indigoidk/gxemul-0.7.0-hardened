#!/bin/bash
#
#  #494 -- propagate the product edit into the NO-VPATH build trees and REBUILD.
#
#      MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash \
#        /mnt/c/.../wdcaltoffset/killtable_20260830/propagate494.sh
#
#  `build/` and `build-asan/` are in-place trees with NO VPATH: an edit that is not
#  copied in leaves them compiling last week's source, and a later measurement then
#  tests code nobody shipped.  precommit_check.sh section B caught this round doing
#  exactly that.
#
#  *** THE CLEARANCE IS TWO-PART AND BOTH PARTS ARE RUN HERE, NOT ASSERTED. ***
#      (1) the propagated source cmps clean against GXEMUL-SEC
#      (2) [ binary -nt source ]
#  Part 2 is the one this project has been burned by twice: a tree whose source cmps
#  clean while its BINARY predates the edit is indistinguishable from a clean tree,
#  and carries no sentinel to warn anybody.  A propagation without a rebuild passes
#  part 1 and fails part 2 silently.
#
set -u

SEC=${GXSEC:-/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC}
ROOT=$(dirname "$SEC")
F=src/devices/dev_wdc.c
J=${J:-8}
rc=0

for T in build build-asan; do
	D="$ROOT/$T"
	echo "=============================================================== $T"
	if [ ! -d "$D" ]; then
		echo "  ABSENT -- nothing to propagate"
		continue
	fi

	cp "$SEC/$F" "$D/$F"
	if cmp -s "$SEC/$F" "$D/$F"; then
		echo "  (1) source cmps clean against GXEMUL-SEC   OK"
	else
		echo "  *** (1) FAILED -- copy did not take"
		rc=8
		continue
	fi

	#  The .o for this file must go, or make may not notice.  Belt and braces: the
	#  generated makefile does track the #included .c files (measured 2026-08-26),
	#  but a stale object costs a wrong measurement while a rebuild costs minutes.
	rm -f "$D/src/devices/dev_wdc.o"
	( cd "$D" && make -j"$J" ) > "$D/.rebuild494.log" 2>&1
	echo "  make rc = $?"

	if [ ! -x "$D/gxemul" ]; then
		echo "  *** NO BINARY.  last 20 lines:"
		tail -20 "$D/.rebuild494.log"
		rc=8
		continue
	fi
	if [ "$D/gxemul" -nt "$D/$F" ]; then
		echo "  (2) [ binary -nt source ]                  OK"
		echo "      $(stat -c '%s bytes  %y' "$D/gxemul")"
	else
		echo "  *** (2) FAILED -- the binary is OLDER than the source it claims to"
		echo "  *** be built from.  THE TREE IS STALE; do not measure it."
		rc=8
	fi
done

echo ""
if [ "$rc" = 0 ]; then
	echo "PROPAGATE494_DONE"
else
	echo "PROPAGATE494_FAILED rc=$rc"
fi
exit "$rc"
