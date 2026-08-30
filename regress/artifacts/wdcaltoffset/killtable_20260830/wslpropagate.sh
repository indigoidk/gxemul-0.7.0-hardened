#!/bin/bash
#
#  THE FOURTH BUILD TREE.  `/tmp/gxsec-build` is the WSL arc tree, and it is the one
#  `propagate494.sh` does NOT touch -- that script walks `build/` and `build-asan/`
#  under the Windows project root and never leaves it.
#
#      MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash \
#        /mnt/c/.../wdcaltoffset/killtable_20260830/wslpropagate.sh
#
#  *** IT WAS FOUND STALE BY A MEASURING SEAT, NOT BY A CHECK. ***  On 2026-08-30 it
#  held a PRE-#494 `dev_wdc.c` while `build/`, `build-asan/` and `est/` all carried the
#  fix.  A clone taken from it -- which is how scratch trees get made -- would have
#  measured #494-less code in the very file under review, and `cmp`-ed clean against
#  its own donor.
#
#  precommit section B checks `build/` and `build-asan/` because they sit under the
#  project root and it can see them.  IT CANNOT SEE THIS ONE: it lives in the WSL
#  filesystem, which the Windows-side checker does not walk.  So the no-VPATH rule
#  has a fourth tree and only three of them are enforced.
#
#  Two-part clearance is RUN here, not asserted, exactly as for the other two.
#
set -u

SEC=${GXSEC:-/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC}
T=${WSLTREE:-/tmp/gxsec-build}
F=src/devices/dev_wdc.c
J=${J:-8}

echo "=============================================================================="
echo "the WSL arc build tree -- propagate and rebuild"
echo "=============================================================================="
echo "date $(date '+%Y-%m-%d %H:%M:%S')"
echo "tree $T"

if [ ! -d "$T" ]; then
	echo "  ABSENT -- nothing to propagate, and nothing can measure a stale copy of it"
	echo "WSLPROP_DONE"
	exit 0
fi

if cmp -s "$SEC/$F" "$T/$F"; then
	echo "  already cmp CLEAN against SEC"
else
	echo "  *** STALE -- propagating"
	cp "$SEC/$F" "$T/$F"
	if cmp -s "$SEC/$F" "$T/$F"; then
		echo "  (1) source cmps clean against GXEMUL-SEC   OK"
	else
		echo "  *** (1) FAILED -- the copy did not take"
		echo "WSLPROP_FAILED"
		exit 8
	fi
fi

#  Part 2 is the half this project has been burned by twice: a tree whose SOURCE cmps
#  clean while its BINARY predates the edit is indistinguishable from a clean tree and
#  carries no sentinel to say otherwise.
if [ ! -x "$T/gxemul" ]; then
	echo "  no binary in this tree -- nothing to keep fresh"
	echo "WSLPROP_DONE"
	exit 0
fi

if [ "$T/gxemul" -nt "$T/$F" ]; then
	echo "  (2) [ binary -nt source ]                  OK  (already fresh)"
	echo "WSLPROP_DONE"
	exit 0
fi

echo "  binary is OLDER than the source -- rebuilding"
rm -f "$T/src/devices/dev_wdc.o"
( cd "$T" && make -j"$J" ) > "$T/.rebuild.log" 2>&1
echo "  make rc = $?"

if [ -x "$T/gxemul" ] && [ "$T/gxemul" -nt "$T/$F" ]; then
	echo "  (2) [ binary -nt source ]                  OK"
	echo "      $(stat -c '%s bytes  %y' "$T/gxemul")"
	echo "WSLPROP_DONE"
else
	echo "  *** (2) FAILED -- the tree is STALE; do not measure it.  Last make lines:"
	tail -12 "$T/.rebuild.log"
	echo "WSLPROP_FAILED"
	exit 8
fi
