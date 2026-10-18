#!/bin/bash
#  launch_close526.sh <seat> -- fire ONE seat (astra | grok) on the xscaleinten closure check.
set -u
H=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$H/../../../.." && pwd)
case "${1:-}" in
astra)
    bash "$R/tools/cxlaunch.sh" "$H/astra_pointer_close526.md" "$H" close526 > "$H/astra_launch_close526.log" 2>&1
    echo "launcher rc=$?" >> "$H/astra_launch_close526.log"; cat "$H/astra_launch_close526.log" ;;
grok)
    G=$(sed -n 's/^GROK_MODEL="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    ~/.grok/bin/grok --prompt-file "$H/packet_close526_GROK.md" -m "$G" --effort xhigh --permission-mode plan \
        --cwd "$R" < /dev/null > "$H/grok_close526.txt" 2> "$H/grok_close526.err"
    echo "rc=$?" > "$H/grok_close526.exit"; echo "grok ($G) $(cat "$H/grok_close526.exit") stdout $(wc -c < "$H/grok_close526.txt") b" ;;
*) echo "usage: launch_close526.sh astra|grok"; exit 2 ;;
esac
