#!/bin/bash
#
#  CONTROLS for `propagatecpsilent` -- a propagate script that reports success after a
#  cp that did not happen.
#
#      MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash \
#        /mnt/c/.../makercfalse/propagate_controls_20260830/cpguard.sh
#
#  THE DEFECT, measured 2026-08-29 on this project's own tooling: the script did
#  `cp "$SEC/$F" "$D/$F"` then UNCONDITIONALLY `echo "  propagated"`.  With a wrong
#  path the log read
#
#      cp: cannot stat '...': No such file or directory
#      propagated
#
#  -- a CLAIM OF ACTION printed at the exact moment of the failure, which is the shape
#  this project already names as worse than a stale citation because it reassures the
#  one person who could still fix it.
#
#  WHAT IS BEING CONTROLLED HERE is not that cp fails -- that is obvious -- but that
#  the REPLACEMENT IDIOM reports the failure, and that it ALSO catches the case cp's
#  exit status cannot see: a cp that SUCCEEDS while copying the wrong bytes.  That
#  second case is why the shipped form verifies with `cmp` rather than with `|| exit`.
#
#  Controlled in BOTH directions.  A check that only ever passes is the shape this
#  whole class is about.
#
set -u
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
bad=0

say () { echo "$@"; }
chk () {   # $1 = label, $2 = want, $3 = got
	if [ "$2" = "$3" ]; then
		printf "  ok    %-46s want %-8s got %s\n" "$1" "$2" "$3"
	else
		printf "  FAIL  %-46s want %-8s got %s\n" "$1" "$2" "$3"
		bad=$((bad + 1))
	fi
}

say "=============================================================================="
say "propagatecpsilent -- cp-guard controls"
say "=============================================================================="
say "date $(date '+%Y-%m-%d %H:%M:%S')"
say ""

mkdir -p "$T/src" "$T/dst"
printf 'REAL CONTENT\n' > "$T/src/f.c"
printf 'STALE CONTENT\n' > "$T/dst/f.c"

#  --- 1. THE OLD IDIOM: cp, then announce unconditionally. -------------------------
old_form () {   # $1 = source path
	cp "$1" "$T/dst/f.c" 2>/dev/null
	echo "propagated"
}
r=$(old_form "$T/src/NOSUCHFILE.c")
chk "OLD idiom, source MISSING" "propagated" "$r"
say "        ^ that is the defect: it announces the action it did not perform"
say ""

#  --- 2. THE SHIPPED IDIOM: cp, then VERIFY BY cmp. --------------------------------
printf 'STALE CONTENT\n' > "$T/dst/f.c"
new_form () {   # $1 = source path
	cp "$1" "$T/dst/f.c" 2>/dev/null
	if cmp -s "$1" "$T/dst/f.c" 2>/dev/null; then echo "ok"; else echo "FAILED"; fi
}
chk "NEW idiom, source MISSING          (must FAIL)" "FAILED" "$(new_form "$T/src/NOSUCHFILE.c")"

printf 'STALE CONTENT\n' > "$T/dst/f.c"
chk "NEW idiom, source PRESENT          (must pass)" "ok" "$(new_form "$T/src/f.c")"
chk "  and the destination really changed" "REAL CONTENT" "$(cat "$T/dst/f.c")"
say ""

#  --- 3. THE CASE cp's EXIT STATUS CANNOT SEE. -------------------------------------
#  A `cp || exit` guard passes here: cp succeeds.  It copied the WRONG FILE, because
#  the path resolved to something that exists and is not what was meant.  Only a
#  content comparison against the INTENDED source catches it.
printf 'WRONG FILE\n' > "$T/src/other.c"
printf 'STALE CONTENT\n' > "$T/dst/f.c"
cp "$T/src/other.c" "$T/dst/f.c"
chk "cp of the WRONG file exits 0       (so || exit passes)" "0" "$?"
if cmp -s "$T/src/f.c" "$T/dst/f.c"; then v=ok; else v=FAILED; fi
chk "  cmp against the INTENDED source   (must FAIL)" "FAILED" "$v"
say "        ^ this is why the shipped form verifies content, not exit status"
say ""

say "=============================================================================="
if [ "$bad" = 0 ]; then
	say "CPGUARD_PASS   6 checks, both directions"
else
	say "CPGUARD_FAIL   $bad check(s) wrong"
fi
exit "$bad"
