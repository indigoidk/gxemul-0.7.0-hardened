#!/bin/bash
# P4: how lib.sh renders the two ways of not running a lane.  A synthetic gate, LOGDIR in scratch.
set -u
export LOGDIR=/tmp/gxopus536p2/degrade_logdir; mkdir -p "$LOGDIR"
. /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/lib.sh
( gate_begin "synthetic-note";    check "some other row" "x" "x"; note "fbpending bound: no build/ objects -- SKIPPED, not passed"; gate_end; echo "rc=$?" ) | tail -2
( gate_begin "synthetic-degrade"; check "some other row" "x" "x"; degrade "fbpending bound: no build/ objects -- NOT run"; gate_end; echo "rc=$?" ) | tail -2
