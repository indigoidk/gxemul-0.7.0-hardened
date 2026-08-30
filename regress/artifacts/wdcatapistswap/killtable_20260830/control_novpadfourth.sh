#!/bin/bash
#
#  NEGATIVE CONTROL for the fourth-build-tree section added to precommit_check.sh.
#
#  A harness change owes controls in BOTH directions, and this project's own rule is
#  that a check which cannot fail is worse than no check.  So this drives the ACTUAL
#  SHIPPED LINES -- extracted from precommit_check.sh by grep anchor, never retyped --
#  against three tree states, with a synthetic CHANGED list because this round edits no
#  src/ file and the real one would leave the loop empty.
#
#  Run:  bash regress/artifacts/wdcatapistswap/killtable_20260830/control_novpadfourth.sh
#
set -u
cd "$(git rev-parse --show-toplevel)" || exit 9

SRCF=tools/precommit_check.sh
#  End on the block's own terminator, not on its last MESSAGE: the first draft anchored
#  the range on `rows skipped, not failed"` and stopped ONE LINE SHORT of the closing
#  `fi`, so `eval` died with "unexpected end of file".  A range that ends on prose ends
#  wherever the prose happens to sit.
BLOCK=$(awk '/^WSLT=\$\{GXWSLTREE/,/^fi$/' "$SRCF")
NL=$(printf '%s\n' "$BLOCK" | wc -l)
echo "extracted $NL lines of the shipped block (anchor: WSLT=\${GXWSLTREE)"
if [ "$NL" -lt 15 ]; then
	echo "*** THE EXTRACTION SELECTED ALMOST NOTHING.  A range that selects the empty"
	echo "*** set produces a clean, confident, wrong answer.  Refusing."
	exit 8
fi

SEC=$(pwd)
FAILS=0; PASSES=0
good () { echo "    good  $*"; PASSES=$((PASSES+1)); }
bad  () { echo "    BAD   $*"; FAILS=$((FAILS+1)); }
say  () { echo "$*"; }
CHANGED="src/devices/dev_wdc.c"

run_case () {   #  $1 = label, $2 = tree path, $3 = expect  (good|bad|skip)
	FAILS=0; PASSES=0
	echo "--- $1"
	GXWSLTREE="$2" eval "$BLOCK"
	case "$3" in
	good) [ "$FAILS" -eq 0 ] && [ "$PASSES" -ge 1 ] && echo "    ==> CONTROL OK (green as intended)" || { echo "    ==> *** CONTROL FAILED"; exit 8; } ;;
	bad)  [ "$FAILS" -ge 1 ] && echo "    ==> CONTROL OK (red as intended)" || { echo "    ==> *** CONTROL FAILED -- THE CHECK CANNOT FAIL"; exit 8; } ;;
	skip) [ "$FAILS" -eq 0 ] && [ "$PASSES" -eq 0 ] && echo "    ==> CONTROL OK (skipped, not failed)" || { echo "    ==> *** CONTROL FAILED"; exit 8; } ;;
	esac
	echo
}

#  1. POSITIVE -- the real tree, currently in sync.
run_case "1. real WSL tree, in sync -> expect GREEN" \
         "//wsl.localhost/Gentoo/tmp/gxsec-build" good

#  2. NEGATIVE -- a copy whose dev_wdc.c differs by ONE byte.  This is the control that
#     matters: without it the section is a claim, not a check.
T=$(mktemp -d)
mkdir -p "$T/src/devices"
cp "$SEC/src/devices/dev_wdc.c" "$T/src/devices/dev_wdc.c"
printf '/* control divergence */\n' >> "$T/src/devices/dev_wdc.c"
run_case "2. tree with a ONE-LINE divergence -> expect RED" "$T" bad
rm -rf "$T"

#  3. ABSENT -- must SKIP, never fail.  A gate that hard-fails because a VM is asleep
#     is a gate that gets switched off.
run_case "3. absent tree -> expect SKIP (not a failure)" \
         "/nonexistent/gxsec-build-$$" skip

echo "CONTROL_NOVPADFOURTH_DONE -- all three states behaved as specified"
