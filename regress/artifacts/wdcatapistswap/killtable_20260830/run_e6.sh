#!/bin/bash
#
#  E6 alone, in its own output tree so the twelve-leg TABLE.txt cannot be clobbered.
#
#  *** A WRAPPER RATHER THAN AN `env` PREFIX, AND THAT IS THE POINT. ***  The first
#  attempt passed OUT/MUTANTS/TABLETAG through `wsl -- env VAR=... bash script`.  The
#  tree was extracted and then the child died before `configure` -- no conf.log, no
#  make.log, and NO GUARD MESSAGE, which is the tell: the script did not exit through
#  one of its own checks, it was torn down.  Setting the variables INSIDE a file that
#  wsl runs plainly is the form that has worked all round.
#
set -u
export OUT=/tmp/gxkswap6
export MUTANTS=E6
export TABLETAG=_E6
exec bash /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/wdcatapistswap/killtable_20260830/killswap.sh
