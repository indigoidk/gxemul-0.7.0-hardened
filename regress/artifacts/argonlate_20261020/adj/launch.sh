#!/bin/bash
#  launch.sh <seat> -- fire ONE seat (astra | grok | glm) on the late-Argon-review adjudication packet.
#  The repo root is FOUR levels up from this directory (adj -> argonlate_20261020 -> artifacts -> regress).
set -u
H=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$H/../../../.." && pwd)
[ -f "$R/tools/panel.sh" ] && [ -f "$R/tools/cxlaunch.sh" ] || { echo "repo root wrong: $R"; exit 9; }
case "${1:-}" in
astra)
    bash "$R/tools/cxlaunch.sh" "$H/astra_pointer.md" "$H" argonlateadj > "$H/astra_launch.log" 2>&1
    echo "launcher rc=$?" >> "$H/astra_launch.log"; tail -5 "$H/astra_launch.log" ;;
grok)
    G=$(sed -n 's/^GROK_MODEL="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    [ -n "$G" ] || { echo "no GROK_MODEL"; exit 9; }
    ~/.grok/bin/grok --prompt-file "$H/packet_GROK.md" -m "$G" --effort xhigh --permission-mode plan \
        --cwd "$R" < /dev/null > "$H/grok_adj.txt" 2> "$H/grok_adj.err"
    echo "rc=$?" > "$H/grok_adj.exit"; echo "grok ($G) $(cat "$H/grok_adj.exit") stdout $(wc -c < "$H/grok_adj.txt") b" ;;
glm)
    M=$(sed -n 's/^OLLAMA1="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    [ -n "$M" ] || { echo "no OLLAMA1"; exit 9; }
    python "$R/tools/panel_ollama.py" "$M" "$H/glm_adj.txt" "$H/packet_GLM.md"
    echo "rc=$?" > "$H/glm_adj.exit"; echo "glm ($M) $(cat "$H/glm_adj.exit") out $(wc -c < "$H/glm_adj.txt") b" ;;
*) echo "usage: launch.sh astra|grok|glm"; exit 2 ;;
esac
