#!/bin/bash
#  launch_cf.sh <seat> -- fire ONE seat (astra | grok | glm) on the rldicl gate-wiring diff, the confirm pass.
set -u
H=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$H/../../../.." && pwd)
case "${1:-}" in
astra)
    bash "$R/tools/cxlaunch.sh" "$H/astra_pointer_cf.md" "$H" rldiclcf > "$H/astra_launch_cf.log" 2>&1
    echo "launcher rc=$?" >> "$H/astra_launch_cf.log"; cat "$H/astra_launch_cf.log" ;;
grok)
    G=$(sed -n 's/^GROK_MODEL="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    ~/.grok/bin/grok --prompt-file "$H/packet_cf_GROK.md" -m "$G" --effort xhigh --permission-mode plan \
        --cwd "$R" < /dev/null > "$H/grok_cf.txt" 2> "$H/grok_cf.err"
    echo "rc=$?" > "$H/grok_cf.exit"; echo "grok ($G) $(cat "$H/grok_cf.exit") stdout $(wc -c < "$H/grok_cf.txt") b" ;;
glm)
    M=$(sed -n 's/^OLLAMA1="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    python "$R/tools/panel_ollama.py" "$M" "$H/glm_cf.txt" "$H/packet_cf_GLM.md"
    echo "rc=$?" > "$H/glm_cf.exit"; echo "glm ($M) $(cat "$H/glm_cf.exit") out $(wc -c < "$H/glm_cf.txt") b" ;;
*) echo "usage: launch_cf.sh astra|grok|glm"; exit 2 ;;
esac
