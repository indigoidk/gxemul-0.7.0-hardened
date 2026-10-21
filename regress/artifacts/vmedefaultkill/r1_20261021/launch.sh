#!/bin/bash
#  launch.sh <seat> -- fire ONE seat (astra | grok | grokadv | glm) on the vmedefaultkill R1 (repair-diff) packet.
#  Runs from the session scratchpad; the whole directory is copied to
#  regress/artifacts/vmedefaultkill/r1_20261021/ afterwards.
set -u
H=$(cd "$(dirname "$0")" && pwd)
R=/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
[ -f "$R/tools/panel.sh" ] && [ -f "$R/tools/cxlaunch.sh" ] || { echo "repo root wrong: $R"; exit 9; }
case "${1:-}" in
astra)
    bash "$R/tools/cxlaunch.sh" "$H/out/astra_pointer.md" "$H/out" vmer1 > "$H/out/astra_launch.log" 2>&1
    echo "launcher rc=$?" >> "$H/out/astra_launch.log"; tail -5 "$H/out/astra_launch.log" ;;
grok|grokadv)
    G=$(sed -n 's/^GROK_MODEL="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    [ -n "$G" ] || { echo "no GROK_MODEL"; exit 9; }
    P=$H/out/packet_GROK.md; [ "$1" = grokadv ] && P=$H/out/packet_GROKADV.md
    ~/.grok/bin/grok --prompt-file "$P" -m "$G" --effort xhigh --permission-mode plan \
        --cwd "$R" < /dev/null > "$H/out/${1}_r1.txt" 2> "$H/out/${1}_r1.err"
    echo "rc=$?" > "$H/out/${1}_r1.exit"; echo "$1 ($G) $(cat "$H/out/${1}_r1.exit") stdout $(wc -c < "$H/out/${1}_r1.txt") b" ;;
glm)
    M=$(sed -n 's/^OLLAMA1="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    [ -n "$M" ] || { echo "no OLLAMA1"; exit 9; }
    python "$R/tools/panel_ollama.py" "$M" "$H/out/glm_r1.txt" "$H/out/packet_GLM.md"
    echo "rc=$?" > "$H/out/glm_r1.exit"; echo "glm ($M) $(cat "$H/out/glm_r1.exit") out $(wc -c < "$H/out/glm_r1.txt") b" ;;
*) echo "usage: launch.sh astra|grok|grokadv|glm"; exit 2 ;;
esac
