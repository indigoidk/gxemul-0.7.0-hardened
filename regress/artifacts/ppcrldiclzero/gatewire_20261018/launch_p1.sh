#!/bin/bash
#  launch_p1.sh <seat> -- fire ONE seat (astra | grok | glm) on the rldicl gate-wiring design brief, pass 1.
set -u
H=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$H/../../../.." && pwd)
case "${1:-}" in
astra)
    bash "$R/tools/cxlaunch.sh" "$H/astra_pointer_p1.md" "$H" rldiclp1 > "$H/astra_launch_p1.log" 2>&1
    echo "launcher rc=$?" >> "$H/astra_launch_p1.log"; cat "$H/astra_launch_p1.log" ;;
grok)
    G=$(sed -n 's/^GROK_MODEL="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    ~/.grok/bin/grok --prompt-file "$H/packet_p1_GROK.md" -m "$G" --effort xhigh --permission-mode plan \
        --cwd "$R" < /dev/null > "$H/grok_p1.txt" 2> "$H/grok_p1.err"
    echo "rc=$?" > "$H/grok_p1.exit"; echo "grok ($G) $(cat "$H/grok_p1.exit") stdout $(wc -c < "$H/grok_p1.txt") b" ;;
glm)
    M=$(sed -n 's/^OLLAMA1="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    python "$R/tools/panel_ollama.py" "$M" "$H/glm_p1.txt" "$H/packet_p1_GLM.md"
    echo "rc=$?" > "$H/glm_p1.exit"; echo "glm ($M) $(cat "$H/glm_p1.exit") out $(wc -c < "$H/glm_p1.txt") b" ;;
*) echo "usage: launch_p1.sh astra|grok|glm"; exit 2 ;;
esac
