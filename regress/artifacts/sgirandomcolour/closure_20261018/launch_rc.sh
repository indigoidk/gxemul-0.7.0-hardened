#!/bin/bash
#  launch_rc.sh <seat> -- fire ONE seat (astra | grok | glm) on the sgirandomcolour closure-records packet; one call per
#  seat, each run in the background by the caller so each notifies on its own exit.  Refuses unless the packets exist.
#  (launch_f2b.sh's shape.  The Fable seat is an Agent call, not this script.)
set -u
H=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$H/../../../.." && pwd)
seat=${1:-}
for p in ASTRA GROK GLM; do [ -s "$H/packet_rc_$p.md" ] || { echo "REFUSE: packet_rc_$p.md missing"; exit 9; }; done
case "$seat" in
astra)
    bash "$R/tools/cxlaunch.sh" "$H/astra_pointer_rc.md" "$H" rcclose > "$H/astra_launch_rc.log" 2>&1
    echo "launcher rc=$?" >> "$H/astra_launch_rc.log"; cat "$H/astra_launch_rc.log" ;;
grok)
    G=$(sed -n 's/^GROK_MODEL="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    ~/.grok/bin/grok --prompt-file "$H/packet_rc_GROK.md" -m "$G" --effort xhigh --permission-mode plan \
        --cwd "$R" < /dev/null > "$H/grok_rcclose.txt" 2> "$H/grok_rcclose.err"
    echo "rc=$?" > "$H/grok_rcclose.exit"; echo "grok ($G) $(cat "$H/grok_rcclose.exit") stdout $(wc -c < "$H/grok_rcclose.txt") b" ;;
glm)
    M=$(sed -n 's/^OLLAMA1="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    python "$R/tools/panel_ollama.py" "$M" "$H/glm_rcclose.txt" "$H/packet_rc_GLM.md"
    echo "rc=$?" > "$H/glm_rcclose.exit"; echo "glm ($M) $(cat "$H/glm_rcclose.exit") out $(wc -c < "$H/glm_rcclose.txt") b" ;;
*)
    echo "usage: launch_rc.sh astra|grok|glm"; exit 2 ;;
esac
