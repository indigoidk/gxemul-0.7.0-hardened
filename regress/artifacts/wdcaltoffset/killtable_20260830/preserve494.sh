#!/bin/bash
#
#  #494 -- copy every measurement a durable record will cite OUT of /tmp.
#
#      MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash \
#        /mnt/c/.../wdcaltoffset/killtable_20260830/preserve494.sh
#
#  WHY IT IS A SEPARATE FILE.  Two reasons, both measured today:
#    * `wsl ... -c '<string>'` strips $VARS even inside single quotes.  The project's
#      own PreToolUse guard refused the inline form of this very command, correctly.
#    * /tmp evaporates.  The 36/36 eighteen-row run existed ONLY at
#      /tmp/gx494/run/RESULTS.txt while the pass-2 brief was citing that number
#      against `RESULTS_shipped.txt`, which holds the earlier 15-row instrument at
#      30/30.  A reviewing seat found the mismatch from the log itself.
#
#  EVERY COPY IS SENTINEL-CHECKED FIRST.  A preserved log is verified by its
#  completion sentinel, not by its existence -- copying a still-running job's output
#  captures a truncation that looks complete.
#
set -u

SEC=${GXSEC:-/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC}
A="$SEC/regress/artifacts/wdcaltoffset/killtable_20260830"
n=0
skip=0

keep () {   # $1 = src, $2 = dest name, $3 = required sentinel
	if [ ! -f "$1" ]; then
		echo "  SKIP  $2  -- source absent: $1"
		skip=$((skip + 1))
		return
	fi
	if ! tail -3 "$1" | grep -q "$3"; then
		echo "  SKIP  $2  -- no '$3' sentinel; NOT preserving a truncation"
		skip=$((skip + 1))
		return
	fi
	cp "$1" "$A/$2"
	echo "  ok    $2  ($(wc -c < "$1") bytes, sentinel $3)"
	n=$((n + 1))
}

echo "=============================================================================="
echo "#494 -- preserving measurements out of /tmp"
echo "=============================================================================="

#  The eighteen-row detector run.  THIS is the 36/36 artifact; RESULTS_shipped.txt is
#  the fifteen-row witness at 30/30 and must never be cited for 36/36.
keep /tmp/gx494/run/RESULTS.txt RESULTS_detector18.txt ALTOFF_DET_DONE

#  Per-mutant logs.  kill494.sh originally copied four `main.out` to ONE name; three
#  were destroyed and the survivor identified no mutant.
for M in m1 m2 m3 m4; do
	keep "/tmp/gxk494/run_$M/main.out" "main_$M.out" ALTOFF_DET_DONE
	keep "/tmp/gxk494/run_$M/sig.out"  "sig_$M.out"  ALTOFF_SIG_DONE
done

echo ""
echo "preserved $n, skipped $skip"
echo "PRESERVE494_DONE"
