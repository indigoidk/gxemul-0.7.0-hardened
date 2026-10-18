#!/bin/bash
#  launch_close527c.sh <seat> -- fire ONE seat (astra | grok) on the #527 closure check.
set -u
H=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$H/../../../.." && pwd)
case "${1:-}" in
astra)
    bash "$R/tools/cxlaunch.sh" "$H/astra_pointer_close527c.md" "$H" close527c > "$H/astra_launch_close527c.log" 2>&1
    echo "launcher rc=$?" >> "$H/astra_launch_close527c.log"; cat "$H/astra_launch_close527c.log" ;;
grok)
    G=$(sed -n 's/^GROK_MODEL="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    ~/.grok/bin/grok --prompt-file "$H/packet_close527c_GROK.md" -m "$G" --effort xhigh --permission-mode plan \
        --cwd "$R" < /dev/null > "$H/grok_close527c.txt" 2> "$H/grok_close527c.err"
    echo "rc=$?" > "$H/grok_close527c.exit"; echo "grok ($G) $(cat "$H/grok_close527c.exit") stdout $(wc -c < "$H/grok_close527c.txt") b" ;;
*) echo "usage: launch_close527c.sh astra|grok"; exit 2 ;;
esac
