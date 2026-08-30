#!/bin/bash
#
#  `wdcatapistswap` -- build both legs and run the EXTENDED witness (15 rows / 30).
#
#      MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash \
#        /mnt/c/.../wdcatapistswap/killtable_20260830/runswap.sh
#
#  A FILE, not a `wsl ... -c '<string>'`: that form strips $VARS even inside single
#  quotes, and this project's own PreToolUse guard refuses it.
#
#  *** HOW THIS DIFFERS FROM run495.sh, AND WHY IT HAD TO. ***  That driver built its
#  base from `git archive HEAD` and its fix from HEAD plus the UNCOMMITTED working diff.
#  #495 is now committed (67120fd), so that diff is empty and the same script would
#  refuse to run.  Here the fix leg IS HEAD and the base leg is HEAD with one file
#  replaced by its parent revision -- `git show $PREREV:src/devices/dev_wdc.c`, which is
#  authoritative and needs no patch to reverse-apply.
#
#  THE PRODUCT CODE IS UNTOUCHED BY THIS ROUND.  The only working-tree change measured
#  here is the PROBE, which is a harness change; both legs are stock revisions.
#
#  TWO-PART CLEARANCE RUN PER LEG, not asserted:
#      (1) the source cmps against the revision it should be
#      (2) [ binary -nt source ]   -- MAKE_RC has been observed 0 on a failed build
#
set -u

SEC=${GXSEC:-/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC}
O=${OUT:-/tmp/gxswap}
ART="$SEC/regress/artifacts/wdcatapistswap/killtable_20260830"
WIT="$SEC/regress/artifacts/wdcaddtoinbufbound/rung3_20260830"
J=${J:-8}
LOG="$O/BUILD.log"

rm -rf "$O"; mkdir -p "$O/probe"
: > "$LOG"
say () { echo "$@" | tee -a "$LOG"; }

say "=============================================================================="
say "wdcatapistswap -- base + fix, then the EXTENDED witness (15 rows, 30 predictions)"
say "=============================================================================="
say "date $(date '+%Y-%m-%d %H:%M:%S')"
cd "$SEC" || exit 9
#  *** THE PRE-FIX REVISION IS PINNED BY SHA, NOT WRITTEN AS `HEAD~1`, AND THIS SCRIPT
#  LEARNED THAT THE HARD WAY ON ITS FIRST RUN. ***  It said `HEAD~1` -- true when it was
#  written, and FALSE ninety minutes later, because an unrelated commit (a citation
#  repair in gate_hygiene.sh) landed on top and pushed #495 down to HEAD~1 itself.  Both
#  legs would then have been built from code CONTAINING the fix.
#
#  The refusal below caught it and the run stopped with nothing measured, which is the
#  guard doing its job -- but a relative ref inside a durable artifact is a wrong record
#  waiting for the next commit, and this round is about exactly that class.
FIXREV=${FIXREV:-67120fd}          # the #495 commit
PREREV="$FIXREV^"
say "HEAD    $(git rev-parse --short HEAD)"
say "fix rev $(git rev-parse --short $FIXREV)   (#495)"
say "pre rev $(git rev-parse --short $PREREV)   (its parent -- the base leg)"

#  The probe is the thing under test this round, so pin what we are measuring.
NROWS=$(awk '/^ROWS = \[/,/^\]/' "$SEC/regress/wdc_addtoinbuf_probe.py" | grep -c '^    (')
say "probe ROWS = $NROWS  -> expected denominator $((NROWS * 2))"
if [ "$NROWS" -ne 15 ]; then
	say "*** EXPECTED 15 ROWS.  The M or N accept arm is missing, or the list changed."
	say "*** Refusing to measure a probe that is not the one this round describes."
	exit 8
fi

git show $PREREV:src/devices/dev_wdc.c > "$O/base_dev_wdc.c" || exit 9
git show HEAD:src/devices/dev_wdc.c   > "$O/head_dev_wdc.c" || exit 9
if cmp -s "$O/base_dev_wdc.c" "$O/head_dev_wdc.c"; then
	say "*** THE PINNED PRE-FIX REV AND HEAD AGREE ON dev_wdc.c -- no #495 to measure"
	say "*** against.  Refusing: the two legs would be identical."
	exit 8
fi
say "base and HEAD dev_wdc.c DIFFER (as they must)"

for leg in base fix; do
	say ""
	say "------------------------------------------------------------------ $leg"
	mkdir -p "$O/$leg"
	git archive HEAD | tar -x -C "$O/$leg" || exit 9

	if [ "$leg" = base ]; then
		cp "$O/base_dev_wdc.c" "$O/$leg/src/devices/dev_wdc.c"
		cmp -s "$O/$leg/src/devices/dev_wdc.c" "$O/base_dev_wdc.c" \
		    && say "  cmp: base source == pre-#495              OK" \
		    || { say "  *** cmp FAILED: base leg is not the pinned pre-#495 revision"; exit 8; }
	else
		cmp -s "$O/$leg/src/devices/dev_wdc.c" "$O/head_dev_wdc.c" \
		    && say "  cmp: fix source == HEAD                  OK" \
		    || { say "  *** cmp FAILED: fix is not HEAD"; exit 8; }
	fi

	( cd "$O/$leg" && ./configure > "$O/$leg.conf.log" 2>&1 \
	    && rm -f src/cpus/*.o && make -j"$J" > "$O/$leg.make.log" 2>&1 )
	say "  make rc = $?"
	if [ ! -x "$O/$leg/gxemul" ]; then
		say "  *** NO BINARY.  last 20 make lines:"; tail -20 "$O/$leg.make.log" | tee -a "$LOG"
		exit 8
	fi
	if [ "$O/$leg/gxemul" -nt "$O/$leg/src/devices/dev_wdc.c" ]; then
		say "  [ binary -nt source ]                    OK"
	else
		say "  *** BINARY NOT NEWER THAN ITS SOURCE -- stale build"; exit 8
	fi
done

if cmp -s "$O/base/gxemul" "$O/fix/gxemul"; then
	say ""
	say "*** THE TWO BINARIES ARE IDENTICAL -- refusing to report a measurement. ***"
	exit 8
fi
say ""
say "base and fix binaries DIFFER (as they must)"

python3 "$WIT/mkcd.py" "$O/cd.iso" | tee -a "$LOG"

#  ONE frozen instrument for both legs.  A comparison run owes one instrument, and
#  python re-reads its source between invocations.
cp "$SEC/regress/wdc_addtoinbuf_probe.py" "$O/probe/frozen.py"
say "probe frozen at $O/probe/frozen.py"
say ""

cd "$O/probe" || exit 9
python3 -u "$O/probe/frozen.py" "$O/base/gxemul" "$O/fix/gxemul" "$O/cd.iso" \
    "$O/probe" > "$O/WITNESS.out" 2>&1
say "probe rc = $?"
tail -40 "$O/WITNESS.out" | tee -a "$LOG"

#  A preserved log is verified by its COMPLETION SENTINEL, not by its existence.
if grep -q ADDTOINBUF_RUNG3_DONE "$O/WITNESS.out"; then
	cp "$O/WITNESS.out" "$ART/RESULTS_extended.txt"
	say ""
	say "preserved: wdcatapistswap/killtable_20260830/RESULTS_extended.txt"
	say "RUNSWAP_DONE"
else
	say "*** NO ADDTOINBUF_RUNG3_DONE -- not preserving a truncation"
	exit 8
fi
