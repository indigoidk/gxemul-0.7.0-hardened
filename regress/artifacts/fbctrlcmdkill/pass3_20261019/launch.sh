#!/bin/bash
#  launch.sh <seat> -- fire ONE seat (astra | grok | glm) on the fbctrlcmdkill PASS 3 packet (the repair's own pass).
#  The repo root is FOUR levels up from this directory (pass3_20261019 -> fbctrlcmdkill -> artifacts -> regress).
set -u
H=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$H/../../../.." && pwd)
[ -f "$R/tools/panel.sh" ] && [ -f "$R/tools/cxlaunch.sh" ] || { echo "repo root wrong: $R"; exit 9; }
case "${1:-}" in
astra)
    bash "$R/tools/cxlaunch.sh" "$H/astra_pointer.md" "$H" fbcmdp3 > "$H/astra_launch.log" 2>&1
    echo "launcher rc=$?" >> "$H/astra_launch.log"; cat "$H/astra_launch.log" ;;
grok)
    G=$(sed -n 's/^GROK_MODEL="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    [ -n "$G" ] || { echo "no GROK_MODEL"; exit 9; }
    ~/.grok/bin/grok --prompt-file "$H/packet_GROK.md" -m "$G" --effort xhigh --permission-mode plan \
        --cwd "$R" < /dev/null > "$H/grok_p3.txt" 2> "$H/grok_p3.err"
    echo "rc=$?" > "$H/grok_p3.exit"; echo "grok ($G) $(cat "$H/grok_p3.exit") stdout $(wc -c < "$H/grok_p3.txt") b" ;;
glm)
    M=$(sed -n 's/^OLLAMA1="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    [ -n "$M" ] || { echo "no OLLAMA1"; exit 9; }
    python "$R/tools/panel_ollama.py" "$M" "$H/glm_p3.txt" "$H/packet_GLM.md"
    echo "rc=$?" > "$H/glm_p3.exit"; echo "glm ($M) $(cat "$H/glm_p3.exit") out $(wc -c < "$H/glm_p3.txt") b" ;;
*) echo "usage: launch.sh astra|grok|glm"; exit 2 ;;
esac
