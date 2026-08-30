#!/bin/bash
#
#  `wdcatapistswap` -- the whole measurement in ONE invocation, deliberately.
#
#      MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash \
#        /mnt/c/.../wdcatapistswap/killtable_20260830/runall.sh
#
#  *** SERIALISED ON PURPOSE, AND THE REASON IS MEASURED TWICE OVER. ***  #495 found
#  that a pty-driven wall-clock instrument corrupts silently under load -- three runs
#  were scored `KILLED (20 red)` while measuring nothing, every one carrying the
#  completion sentinel.  And on THIS round a measuring seat independently reported
#  seeing `killswap.sh` appear at 13:09 while its own table was building, and said so.
#  The machine was confirmed quiet (0 panel seat processes, 0 WSL builds) before this
#  was launched, and running both halves under one parent is what keeps it that way.
#
#  NO `set -e`.  A build-and-measure script must not die on a comparison's exit status;
#  this project has already had a runner end in `diff` and skip both its probe runs
#  while its wrapper reported rc=0.
#
set -u

A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/wdcatapistswap/killtable_20260830

echo "############################################################################"
echo "#  PART 1 of 2 -- base + fix legs, then the extended witness"
echo "############################################################################"
bash "$A/runswap.sh"
RC=$?
if [ "$RC" -ne 0 ]; then
	echo "*** runswap.sh FAILED rc=$RC -- NOT running the kill table."
	echo "*** A table built on legs that did not verify is not a measurement."
	exit 8
fi

echo
echo "############################################################################"
echo "#  PART 2 of 2 -- the kill table (leg 0 + 11 mutants)"
echo "############################################################################"
bash "$A/killswap.sh"
RC=$?
if [ "$RC" -ne 0 ]; then
	echo "*** killswap.sh FAILED rc=$RC"
	exit 8
fi

echo "RUNALL_DONE"
