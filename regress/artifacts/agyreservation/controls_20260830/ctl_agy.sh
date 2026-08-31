#!/bin/bash
P="$1"
DECL=$(sed -n '/^AGY_FIRE=/,/^AGY_MODEL=/p' "$P" | head -1)
BAN=$(sed -n '/^AGY_BANNER=/,/^\[ -z "\$AGY_FIRE" \]/p' "$P")
[ -z "$DECL" ] && { echo "  EXTRACT FAILED: no AGY_FIRE declaration"; exit 9; }
run () {  # $1 label  $2 env value  $3 want
    if [ -n "$2" ]; then PANEL_FIRE_AGY="$2"; else unset PANEL_FIRE_AGY; fi
    eval "$DECL"
    AGY_MODEL=m; AGY_EFFORT=e
    eval "$BAN"
    case "$AGY_BANNER" in *RESERVED*) got=reserved;; *) got=fired;; esac
    [ "$got" = "$3" ] && r="ok  " || r="FAIL"
    printf "  %s %-34s PANEL_FIRE_AGY=%-6s -> %-9s want=%s\n" "$r" "$1" "${2:-unset}" "$got" "$3"
}
run "default: held out of panels" ""  reserved
run "opt-in: fired deliberately"  "1" fired
echo "AGYCTL_DONE"
