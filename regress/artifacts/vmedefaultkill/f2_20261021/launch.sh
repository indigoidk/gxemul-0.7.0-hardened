#!/bin/bash
#  launch.sh <seat> -- fire ONE seat (astra | grok | glm) on the vmedefaultkill F2 packet.
#  Runs from the session scratchpad; the whole directory is copied to
#  regress/artifacts/vmedefaultkill/f2_20261020/ afterwards.
set -u
H=$(cd "$(dirname "$0")" && pwd)
R=/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
[ -f "$R/tools/panel.sh" ] && [ -f "$R/tools/cxlaunch.sh" ] || { echo "repo root wrong: $R"; exit 9; }
case "${1:-}" in
astra)
    bash "$R/tools/cxlaunch.sh" "$H/out/astra_pointer.md" "$H/out" vmef2 > "$H/out/astra_launch.log" 2>&1
    echo "launcher rc=$?" >> "$H/out/astra_launch.log"; tail -5 "$H/out/astra_launch.log" ;;
grok)
    G=$(sed -n 's/^GROK_MODEL="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    [ -n "$G" ] || { echo "no GROK_MODEL"; exit 9; }
    ~/.grok/bin/grok --prompt-file "$H/out/packet_GROK.md" -m "$G" --effort xhigh --permission-mode plan \
        --cwd "$R" < /dev/null > "$H/out/grok_f2.txt" 2> "$H/out/grok_f2.err"
    echo "rc=$?" > "$H/out/grok_f2.exit"; echo "grok ($G) $(cat "$H/out/grok_f2.exit") stdout $(wc -c < "$H/out/grok_f2.txt") b" ;;
glm)
    M=$(sed -n 's/^OLLAMA1="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    [ -n "$M" ] || { echo "no OLLAMA1"; exit 9; }
    python "$R/tools/panel_ollama.py" "$M" "$H/out/glm_f2.txt" "$H/out/packet_GLM.md"
    echo "rc=$?" > "$H/out/glm_f2.exit"; echo "glm ($M) $(cat "$H/out/glm_f2.exit") out $(wc -c < "$H/out/glm_f2.txt") b" ;;
*) echo "usage: launch.sh astra|grok|glm"; exit 2 ;;
esac
