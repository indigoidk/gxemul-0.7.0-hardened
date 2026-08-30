#!/bin/bash
#
#  CONTROLS for `panelrefire` -- what panel.sh says when a seat walls.
#
#      bash regress/artifacts/makercfalse/panelrefire_controls_20260830/wallmsg.sh
#
#  Runs in git-bash; no WSL needed, which is deliberate -- this exercises a bash
#  FUNCTION, and routing it through `wsl ... -c` would strip the very variables the
#  test exists to prove are in scope.  The project's own guard refused that form.
#
#  HISTORY.  `panel.sh` used to print "re-firing once (a wall can be minutes long)"
#  and re-fire NOTHING: every caller is a bare `check "name" "$file"` whose exit
#  status is discarded, so the `return 2` never had a consumer.  That is worse than a
#  stale citation -- it printed a CLAIM OF ACTION at the moment a seat was lost, so
#  the one person who could re-fire it by hand was told it had been done.
#
#  The message is now an INSTRUCTION.  This control pins two things about it:
#    * a WALLED seat gets the instruction AND is told where the command lives, with
#      $BRIEF and $f expanded to real values rather than empty strings;
#    * a HEALTHY seat gets NONE of it.
#
#  AUTOMATIC RE-FIRING IS STILL NOT DONE.  The seven launches would have to be
#  refactored into re-runnable units first -- a change to the script every panel
#  runs, owing its own two negative controls.  That is its own round, and this
#  control does not pretend otherwise.
#
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
SEC=$(cd "$HERE/../../../.." && pwd)
PANEL="$SEC/tools/panel.sh"
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
bad=0

chk () {   # $1 label, $2 want(yes/no), $3 got(yes/no)
	if [ "$2" = "$3" ]; then printf "  ok    %-52s want %-4s got %s\n" "$1" "$2" "$3"
	else printf "  FAIL  %-52s want %-4s got %s\n" "$1" "$2" "$3"; bad=$((bad + 1)); fi
}

mkfn () {   # $1 = output script, $2 = seat file
	{ printf 'say () { echo "$@"; }\nBRIEF=/tmp/thebrief.md\n'
	  sed -n '/^check() {/,/^}/p' "$PANEL"
	  printf 'check "seat" "%s"\n' "$2"; } > "$1"
}

echo "=============================================================================="
echo "panelrefire -- walled-seat message controls"
echo "=============================================================================="
echo "date  $(date '+%Y-%m-%d %H:%M:%S')"
echo "panel $PANEL"
echo ""

#  Both fixtures must clear the SUSPECT size threshold, or the size branch fires
#  first and the walled branch is never reached.  The first version of this control
#  used a 59-byte file and tested nothing -- the apparatus selected the wrong branch
#  and would have reported a pass.
pad () { head -c 4000 /dev/urandom | base64 | head -40; }

{ pad; printf '\nprovider.auth_error: 403 You have reached your usage limit\n'; } > "$T/walled.txt"
{ pad; printf '\nVERDICT: GO -- the fix is sound\n'; } > "$T/healthy.txt"
echo "  fixtures: walled $(wc -c < "$T/walled.txt")b, healthy $(wc -c < "$T/healthy.txt")b"
echo ""

mkfn "$T/w.sh" "$T/walled.txt";  W=$(bash "$T/w.sh" 2>&1)
mkfn "$T/h.sh" "$T/healthy.txt"; H=$(bash "$T/h.sh" 2>&1)

echo "--- WALLED seat ---"; echo "$W" | sed 's/^/    /'
echo "--- HEALTHY seat ---"; echo "$H" | sed 's/^/    /'
echo ""

has () { echo "$1" | grep -q "$2" && echo yes || echo no; }

chk "walled: reaches the WALL branch at all"        yes "$(has "$W" 'WALLED MID-ANSWER')"
chk "walled: gets the re-fire instruction"          yes "$(has "$W" 'RE-FIRE THIS SEAT ONCE')"
chk "walled: is told it is NOT automatic"           yes "$(has "$W" 'NOT done automatically')"
chk "walled: is told WHERE the command lives"       yes "$(has "$W" 'seat table in tools/CLAUDE.md')"
chk "walled: \$BRIEF expanded, not empty"            yes "$(has "$W" 'brief is /tmp/thebrief.md')"
chk "walled: \$f expanded, not empty"                yes "$(has "$W" 'walled.txt')"
chk "HEALTHY: no re-fire instruction   (negative)"  no  "$(has "$H" 'RE-FIRE THIS SEAT ONCE')"
chk "HEALTHY: no command pointer       (negative)"  no  "$(has "$H" 'seat table in tools/CLAUDE.md')"
chk "HEALTHY: scored as answered"                   yes "$(has "$H" 'answered')"

echo ""
if [ "$bad" = 0 ]; then echo "WALLMSG_PASS   9 checks, both directions"
else echo "WALLMSG_FAIL   $bad check(s) wrong"; fi
exit "$bad"
