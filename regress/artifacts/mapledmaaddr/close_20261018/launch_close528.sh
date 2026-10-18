#!/bin/bash
#  launch_close528.sh <seat> -- fire ONE seat (astra | grok) on the mapledmaaddr closure check.
set -u
H=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$H/../../../.." && pwd)
case "${1:-}" in
astra)
    bash "$R/tools/cxlaunch.sh" "$H/astra_pointer_close528.md" "$H" close528 > "$H/astra_launch_close528.log" 2>&1
    echo "launcher rc=$?" >> "$H/astra_launch_close528.log"; cat "$H/astra_launch_close528.log" ;;
grok)
    G=$(sed -n 's/^GROK_MODEL="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    ~/.grok/bin/grok --prompt-file "$H/packet_close528_GROK.md" -m "$G" --effort xhigh --permission-mode plan \
        --cwd "$R" < /dev/null > "$H/grok_close528.txt" 2> "$H/grok_close528.err"
    echo "rc=$?" > "$H/grok_close528.exit"; echo "grok ($G) $(cat "$H/grok_close528.exit") stdout $(wc -c < "$H/grok_close528.txt") b" ;;
*) echo "usage: launch_close528.sh astra|grok"; exit 2 ;;
esac
