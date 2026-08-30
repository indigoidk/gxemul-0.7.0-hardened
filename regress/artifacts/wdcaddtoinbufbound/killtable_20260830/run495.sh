#!/bin/bash
#
#  #495 -- build both legs and run the rung-3 witness against the SHIPPED fix.
#
#      MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash \
#        /mnt/c/.../wdcaddtoinbufbound/killtable_20260830/run495.sh
#
#  A FILE, not a `wsl ... -c '<string>'`: that form strips $VARS even inside single
#  quotes, and this project's own PreToolUse guard refuses it.
#
#  THE FIX LEG IS `git archive HEAD` PLUS THE WORKING DIFF, never a `cp -a` of the
#  working tree -- a copy inherits .o files and untracked residue, so the tree measured
#  would not be the tree named.  No project build tree is touched; no .MUTANT is owed.
#
#  TWO-PART CLEARANCE RUN PER LEG, not asserted:
#      (1) the source cmps against what it should be
#      (2) [ binary -nt source ]   -- MAKE_RC has been observed 0 on a failed build
#
set -u

SEC=${GXSEC:-/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC}
O=${OUT:-/tmp/gx495}
ART="$SEC/regress/artifacts/wdcaddtoinbufbound/killtable_20260830"
WIT="$SEC/regress/artifacts/wdcaddtoinbufbound/rung3_20260830"
J=${J:-8}
LOG="$O/BUILD.log"

rm -rf "$O"; mkdir -p "$O/probe"
: > "$LOG"
say () { echo "$@" | tee -a "$LOG"; }

say "=============================================================================="
say "#495 wdcaddtoinbufbound -- build base + shipped fix, then the rung-3 witness"
say "=============================================================================="
say "date $(date '+%Y-%m-%d %H:%M:%S')"
cd "$SEC" || exit 9
say "HEAD $(git rev-parse --short HEAD)"

git diff HEAD -- src/devices/dev_wdc.c > "$O/shipped.diff"
DB=$(wc -c < "$O/shipped.diff")
say "working diff on dev_wdc.c: $DB bytes"
if [ "$DB" -lt 100 ]; then
	say "*** THE WORKING DIFF IS EMPTY OR TINY -- refusing to measure a fix that is"
	say "*** not there.  (0 bytes and 0 hunks are different claims from a real file.)"
	exit 8
fi
cp "$O/shipped.diff" "$ART/shipped.diff"

for leg in base fix; do
	say ""
	say "------------------------------------------------------------------ $leg"
	mkdir -p "$O/$leg"
	git archive HEAD | tar -x -C "$O/$leg" || exit 9

	if [ "$leg" = fix ]; then
		( cd "$O/$leg" && patch -p1 --batch --forward < "$O/shipped.diff" ) \
		    >> "$LOG" 2>&1 || { say "  *** PATCH FAILED"; exit 8; }
		cmp -s "$O/$leg/src/devices/dev_wdc.c" "$SEC/src/devices/dev_wdc.c" \
		    && say "  cmp: patched source == working tree      OK" \
		    || { say "  *** cmp FAILED: the fix leg is not the working tree"; exit 8; }
	else
		git show HEAD:src/devices/dev_wdc.c > "$O/head.c"
		cmp -s "$O/$leg/src/devices/dev_wdc.c" "$O/head.c" \
		    && say "  cmp: base source == HEAD                 OK" \
		    || { say "  *** cmp FAILED: base is not HEAD"; exit 8; }
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
	say "*** THE TWO BINARIES ARE IDENTICAL -- the edit changed nothing the compiler"
	say "*** kept.  Refusing to report a measurement. ***"
	exit 8
fi
say ""
say "base and fix binaries DIFFER (as they must)"

#  The poisoned image.  Its bytes at the chunk-2 boundary are what make the oracle
#  ABSOLUTE: the fixed leg returns disk content through a channel outside the ring.
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
tail -30 "$O/WITNESS.out" | tee -a "$LOG"

#  A preserved log is verified by its COMPLETION SENTINEL, not by its existence.
if grep -q ADDTOINBUF_RUNG3_DONE "$O/WITNESS.out"; then
	cp "$O/WITNESS.out" "$ART/RESULTS_shipped.txt"
	say ""
	say "preserved: killtable_20260830/RESULTS_shipped.txt"
	say "RUN495_DONE"
else
	say "*** NO ADDTOINBUF_RUNG3_DONE -- not preserving a truncation"
	exit 8
fi
