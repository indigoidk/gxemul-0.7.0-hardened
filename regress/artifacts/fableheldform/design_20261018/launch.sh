#!/bin/bash
#  launch.sh <seat> -- fire ONE seat (astra | astracf | astracf2 | grok | glm) on the fableheldform design brief (pass 1).
set -u
H=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$H/../../../.." && pwd)
case "${1:-}" in
astra)
    bash "$R/tools/cxlaunch.sh" "$H/astra_pointer.md" "$H" fhfp1 > "$H/astra_launch.log" 2>&1
    echo "launcher rc=$?" >> "$H/astra_launch.log"; cat "$H/astra_launch.log" ;;
astracf)
    bash "$R/tools/cxlaunch.sh" "$H/confirm/astra_pointer_cf.md" "$H" fhfcf > "$H/astra_launch_cf.log" 2>&1
    echo "launcher rc=$?" >> "$H/astra_launch_cf.log"; cat "$H/astra_launch_cf.log" ;;
astracf2)
    bash "$R/tools/cxlaunch.sh" "$H/confirm_r2/astra_pointer_cf2.md" "$H" fhfcf2 > "$H/astra_launch_cf2.log" 2>&1
    echo "launcher rc=$?" >> "$H/astra_launch_cf2.log"; cat "$H/astra_launch_cf2.log" ;;
grok)
    G=$(sed -n 's/^GROK_MODEL="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    ~/.grok/bin/grok --prompt-file "$H/packet_GROK.md" -m "$G" --effort xhigh --permission-mode plan \
        --cwd "$R" < /dev/null > "$H/grok_p1.txt" 2> "$H/grok_p1.err"
    echo "rc=$?" > "$H/grok_p1.exit"; echo "grok ($G) $(cat "$H/grok_p1.exit") stdout $(wc -c < "$H/grok_p1.txt") b" ;;
glm)
    M=$(sed -n 's/^OLLAMA1="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    python "$R/tools/panel_ollama.py" "$M" "$H/glm_p1.txt" "$H/packet_GLM.md"
    echo "rc=$?" > "$H/glm_p1.exit"; echo "glm ($M) $(cat "$H/glm_p1.exit") out $(wc -c < "$H/glm_p1.txt") b" ;;
*) echo "usage: launch.sh astra|astracf|astracf2|grok|glm"; exit 2 ;;
esac
