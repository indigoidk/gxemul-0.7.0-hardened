#!/bin/bash
#
#  #494 pass 2 -- build the BASE (HEAD) and the SHIPPED FIX (HEAD + working diff).
#
#      MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash \
#        /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/wdcaltoffset/killtable_20260830/build494.sh
#
#  A FILE, not a `wsl ... -c '<string>'`: that form strips $VARS even inside single
#  quotes.  Every path is /mnt/c, because a Windows path handed to `wsl -- bash`
#  fails while wsl itself exits 0.
#
#  THE FIX LEG IS `git archive HEAD` PLUS THE WORKING DIFF, never a `cp -a` of the
#  working tree: a copy inherits .o files and untracked residue, so the tree measured
#  would not be the tree named.  A patch onto a clean archive is mechanical.
#
#  NO PROJECT BUILD TREE IS TOUCHED, so no .MUTANT sentinel is owed.
#
#  THE TWO-PART CLEARANCE IS RUN PER LEG, NOT ASSERTED:
#      (1) the source cmps against what it should be
#      (2) [ binary -nt source ]   -- MAKE_RC has been observed 0 on a failed build
#
set -u

SEC=${GXSEC:-/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC}
O=${OUT:-/tmp/gx494}
J=${J:-8}
ART="$SEC/regress/artifacts/wdcaltoffset/killtable_20260830"
LOG="$O/BUILD.log"

rm -rf "$O"
mkdir -p "$O"
: > "$LOG"
say () { echo "$@" | tee -a "$LOG"; }

say "=============================================================================="
say "#494 wdcaltoffset pass 2 -- build base + shipped fix"
say "=============================================================================="
say "date  $(date '+%Y-%m-%d %H:%M:%S')"
say "SEC   $SEC"
say "O     $O"
say ""

cd "$SEC" || exit 9
HEADSHA=$(git rev-parse --short HEAD)
say "HEAD  $HEADSHA"

#  The working diff, captured ONCE so both the patch and the record cite one text.
git diff HEAD -- src/devices/dev_wdc.c > "$O/shipped.diff"
DIFFBYTES=$(wc -c < "$O/shipped.diff")
say "working diff on dev_wdc.c: $DIFFBYTES bytes"
if [ "$DIFFBYTES" -lt 100 ]; then
	say "*** THE WORKING DIFF IS EMPTY OR TINY -- refusing to measure a fix that is"
	say "*** not there.  (A denominator: 0 bytes and 0 changed hunks are different"
	say "*** claims from a run that found a real file.)"
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
		    >> "$LOG" 2>&1
		if [ $? -ne 0 ]; then
			say "  *** PATCH FAILED -- refusing to build a leg that is not the fix"
			exit 8
		fi
		#  Clearance part 1: the patched source must equal the working tree's.
		if cmp -s "$O/$leg/src/devices/dev_wdc.c" "$SEC/src/devices/dev_wdc.c"; then
			say "  cmp: patched source == working tree      OK"
		else
			say "  *** cmp FAILED: the fix leg is not the working tree ***"
			exit 8
		fi
	else
		#  Clearance part 1 for base: it must equal HEAD's committed file.
		git show HEAD:src/devices/dev_wdc.c > "$O/headfile.c"
		if cmp -s "$O/$leg/src/devices/dev_wdc.c" "$O/headfile.c"; then
			say "  cmp: base source == HEAD                 OK"
		else
			say "  *** cmp FAILED: base is not HEAD ***"
			exit 8
		fi
	fi

	cd "$O/$leg" || exit 9
	./configure > "$O/$leg.configure.log" 2>&1
	rm -f src/cpus/*.o
	make -j"$J" > "$O/$leg.make.log" 2>&1
	MAKE_RC=$?
	say "  make rc = $MAKE_RC"

	if [ ! -x "$O/$leg/gxemul" ]; then
		say "  *** NO BINARY.  last 25 lines of the make log:"
		tail -25 "$O/$leg.make.log" | tee -a "$LOG"
		exit 8
	fi
	#  Clearance part 2.  The sentinel protects the source; the thing measured is
	#  the binary, and MAKE_RC has lied before.
	if [ "$O/$leg/gxemul" -nt "$O/$leg/src/devices/dev_wdc.c" ]; then
		say "  [ binary -nt source ]                    OK"
	else
		say "  *** BINARY IS NOT NEWER THAN ITS SOURCE -- stale build ***"
		exit 8
	fi
	say "  binary  $(stat -c '%s bytes  %y' "$O/$leg/gxemul")"
	cd "$SEC" || exit 9
done

say ""
if cmp -s "$O/base/gxemul" "$O/fix/gxemul"; then
	say "*** THE TWO BINARIES ARE IDENTICAL.  The edit changed nothing that the"
	say "*** compiler kept -- refusing to report a measurement. ***"
	exit 8
fi
say "base and fix binaries DIFFER (as they must)"
say ""
say "BUILD494_DONE"
