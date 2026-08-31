#!/bin/bash
#  panelargvcap controls.  Takes the panel.sh to test as $1 so the SAME script can be run
#  against the pre-fix form -- proving the test can fail, not just that it passes.
P="${1:?usage: ctl_argv.sh <panel.sh>}"
DECIDE=$(sed -n '/^ARGV_CAP=/,/^fi$/p' "$P")
BUILD=$(sed -n '/^PTR_PROMPT=/,/^fi$/p' "$P")
if [ -z "$DECIDE" ] || [ -z "$BUILD" ]; then
    echo "  EXTRACT FAILED (decision=${#DECIDE}b build=${#BUILD}b) -- this form has no"
    echo "  cap branch at all: the brief goes on argv unconditionally."
    echo "ARGVCAP_CONTROLS_DONE rc=9"
    exit 9
fi
echo "extracted from $P: decision $(printf '%s' "$DECIDE" | wc -l) lines, build $(printf '%s' "$BUILD" | wc -l) lines"
run () {
    BRIEF=/tmp/ctl_brief.txt
    head -c "$2" /dev/zero | tr '\0' 'x' > "$BRIEF"
    BRIEF_ABS="$BRIEF"
    if [ -n "$3" ]; then PANEL_ARGV_CAP="$3"; else unset PANEL_ARGV_CAP; fi
    eval "$DECIDE"; eval "$BUILD" >/dev/null 2>&1
    case "$CODEX_ARG" in "Read "*) got=pointer;; *) got=inline;; esac
    same=$([ "$CODEX_ARG" = "$KIMI_ARG" ] && echo yes || echo NO)
    [ "$got" = "$4" ] && r="ok  " || { r="FAIL"; FAILED=1; }
    printf "  %s %-34s %8sb cap=%-9s -> %-7s want=%-7s both-agree=%s\n" \
           "$r" "$1" "$2" "${3:-default}" "$got" "$4" "$same"
}
FAILED=0
echo "=== NEGATIVE CONTROLS, both directions ==="
run "small brief, default cap"      1000     ""          inline
run "big brief, default cap"        40000    ""          pointer
run "small brief, cap forced to 1"  1000     1           pointer
run "big brief, cap forced huge"    40000    99999999    inline
run "exactly AT the cap (30000)"    30000    ""          inline
run "one byte OVER the cap"         30001    ""          pointer
echo "ARGVCAP_CONTROLS_DONE rc=$FAILED"
exit $FAILED
