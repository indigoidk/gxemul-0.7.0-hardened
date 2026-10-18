#!/bin/bash
#  launch_close527b.sh <seat> -- fire ONE seat (astra | grok) on the #527 closure check.
set -u
H=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$H/../../../.." && pwd)
case "${1:-}" in
astra)
    bash "$R/tools/cxlaunch.sh" "$H/astra_pointer_close527b.md" "$H" close527b > "$H/astra_launch_close527b.log" 2>&1
    echo "launcher rc=$?" >> "$H/astra_launch_close527b.log"; cat "$H/astra_launch_close527b.log" ;;
grok)
    G=$(sed -n 's/^GROK_MODEL="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    ~/.grok/bin/grok --prompt-file "$H/packet_close527b_GROK.md" -m "$G" --effort xhigh --permission-mode plan \
        --cwd "$R" < /dev/null > "$H/grok_close527b.txt" 2> "$H/grok_close527b.err"
    echo "rc=$?" > "$H/grok_close527b.exit"; echo "grok ($G) $(cat "$H/grok_close527b.exit") stdout $(wc -c < "$H/grok_close527b.txt") b" ;;
*) echo "usage: launch_close527b.sh astra|grok"; exit 2 ;;
esac
