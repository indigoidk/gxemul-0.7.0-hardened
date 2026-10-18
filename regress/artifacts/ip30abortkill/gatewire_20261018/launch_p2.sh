#!/bin/bash
#  launch_p2.sh <seat> -- fire ONE seat (astra | grok | glm) on the ip30 gate-wiring diff (#566), pass 2.
set -u
H=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$H/../../../.." && pwd)
case "${1:-}" in
astra)
    bash "$R/tools/cxlaunch.sh" "$H/astra_pointer_p2.md" "$H" ip30wirep2 > "$H/astra_launch_p2.log" 2>&1
    echo "launcher rc=$?" >> "$H/astra_launch_p2.log"; cat "$H/astra_launch_p2.log" ;;
grok)
    G=$(sed -n 's/^GROK_MODEL="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    ~/.grok/bin/grok --prompt-file "$H/packet_p2_GROK.md" -m "$G" --effort xhigh --permission-mode plan \
        --cwd "$R" < /dev/null > "$H/grok_p2.txt" 2> "$H/grok_p2.err"
    echo "rc=$?" > "$H/grok_p2.exit"; echo "grok ($G) $(cat "$H/grok_p2.exit") stdout $(wc -c < "$H/grok_p2.txt") b" ;;
glm)
    M=$(sed -n 's/^OLLAMA1="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    python "$R/tools/panel_ollama.py" "$M" "$H/glm_p2.txt" "$H/packet_p2_GLM.md"
    echo "rc=$?" > "$H/glm_p2.exit"; echo "glm ($M) $(cat "$H/glm_p2.exit") out $(wc -c < "$H/glm_p2.txt") b" ;;
*) echo "usage: launch_p2.sh astra|grok|glm"; exit 2 ;;
esac
