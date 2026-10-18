#!/bin/bash
#  launch_fid.sh <seat> -- fire ONE seat (astra | grok) on the rulings-fidelity verification brief.
set -u
H=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$H/../../../.." && pwd)
case "${1:-}" in
astra)
    bash "$R/tools/cxlaunch.sh" "$H/astra_pointer_fid.md" "$H" fid > "$H/astra_launch_fid.log" 2>&1
    echo "launcher rc=$?" >> "$H/astra_launch_fid.log"; cat "$H/astra_launch_fid.log" ;;
grok)
    G=$(sed -n 's/^GROK_MODEL="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    ~/.grok/bin/grok --prompt-file "$H/packet_fid_GROK.md" -m "$G" --effort xhigh --permission-mode plan \
        --cwd "$R" < /dev/null > "$H/grok_fid.txt" 2> "$H/grok_fid.err"
    echo "rc=$?" > "$H/grok_fid.exit"; echo "grok ($G) $(cat "$H/grok_fid.exit") stdout $(wc -c < "$H/grok_fid.txt") b" ;;
*) echo "usage: launch_fid.sh astra|grok"; exit 2 ;;
esac
