#!/bin/bash
#  launch_close531.sh <seat> -- fire ONE seat (astra | astrab | astrac | grok | glm) on ip30abortkill's closure check (astrab = the confirm, astrac = the micro-confirm).
set -u
H=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$H/../../../.." && pwd)
case "${1:-}" in
astra)
    bash "$R/tools/cxlaunch.sh" "$H/astra_pointer_close531.md" "$H" close531 > "$H/astra_launch_close531.log" 2>&1
    echo "launcher rc=$?" >> "$H/astra_launch_close531.log"; cat "$H/astra_launch_close531.log" ;;
astrab)
    bash "$R/tools/cxlaunch.sh" "$H/astra_pointer_close531b.md" "$H" close531b > "$H/astra_launch_close531b.log" 2>&1
    echo "launcher rc=$?" >> "$H/astra_launch_close531b.log"; cat "$H/astra_launch_close531b.log" ;;
astrac)
    bash "$R/tools/cxlaunch.sh" "$H/astra_pointer_close531c.md" "$H" close531c > "$H/astra_launch_close531c.log" 2>&1
    echo "launcher rc=$?" >> "$H/astra_launch_close531c.log"; cat "$H/astra_launch_close531c.log" ;;
grok)
    G=$(sed -n 's/^GROK_MODEL="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    ~/.grok/bin/grok --prompt-file "$H/packet_close531_GROK.md" -m "$G" --effort xhigh --permission-mode plan \
        --cwd "$R" < /dev/null > "$H/grok_close531.txt" 2> "$H/grok_close531.err"
    echo "rc=$?" > "$H/grok_close531.exit"; echo "grok ($G) $(cat "$H/grok_close531.exit") stdout $(wc -c < "$H/grok_close531.txt") b" ;;
glm)
    M=$(sed -n 's/^OLLAMA1="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    python "$R/tools/panel_ollama.py" "$M" "$H/glm_close531.txt" "$H/packet_close531_GLM.md"
    echo "rc=$?" > "$H/glm_close531.exit"; echo "glm ($M) $(cat "$H/glm_close531.exit") out $(wc -c < "$H/glm_close531.txt") b" ;;
*) echo "usage: launch_close531.sh astra|astrab|astrac|grok|glm"; exit 2 ;;
esac
