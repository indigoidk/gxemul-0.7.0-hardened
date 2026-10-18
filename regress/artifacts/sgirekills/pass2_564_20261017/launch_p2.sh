#!/bin/bash
#  launch_p2.sh <seat> -- fire ONE #564 pass-2 seat (astra | grok | glm) on its assembled packet; one call per seat, each
#  run in the background by the caller so each notifies on its own exit.  Refuses unless assemble_p2.sh's packets exist
#  and are newer than every input the assembler reads, so a seat can never be fired on a stale packet.
set -u
H=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$H/../../../.." && pwd)
K="$H/../killtable_564_20261017"
seat=${1:-}
for p in ASTRA GROK GLM FABLE; do [ -s "$H/packet_564p2_$p.md" ] || { echo "REFUSE: packet_564p2_$p.md missing -- run assemble_p2.sh"; exit 9; }; done
for f in "$H/p2_head.md" "$H/q2_all.md" "$H/q2_astra.md" "$K/KILLTABLE2.txt" "$R/src/devices/dev_sgi_re.c" "$R/regress/sgi_mte_decline_probe.py" "$R/regress/gate_arm.sh"; do
    [ "$H/packet_564p2_GROK.md" -nt "$f" ] || { echo "REFUSE: the packets are older than $f -- re-run assemble_p2.sh"; exit 9; }
done
case "$seat" in
astra)
    #  the pointer form: codex reads the packet itself (tools/cxlaunch.sh -- an AUP refusal re-runs once on Daybreak)
    bash "$R/tools/cxlaunch.sh" "$H/astra_pointer.md" "$H" mte564p2 > "$H/astra_launch.log" 2>&1
    echo "launcher rc=$?" >> "$H/astra_launch.log"; cat "$H/astra_launch.log" ;;
grok)
    #  plan mode is read-only; --prompt-file has no argv cap.  The model and effort are panel.sh's.
    G=$(sed -n 's/^GROK_MODEL="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    ~/.grok/bin/grok --prompt-file "$H/packet_564p2_GROK.md" -m "$G" --effort xhigh --permission-mode plan \
        --cwd "$R" < /dev/null > "$H/grok_mte564p2.txt" 2> "$H/grok_mte564p2.err"
    echo "rc=$?" > "$H/grok_mte564p2.exit"; echo "grok ($G) $(cat "$H/grok_mte564p2.exit") stdout $(wc -c < "$H/grok_mte564p2.txt") b" ;;
glm)
    #  packet-fed: panel_ollama.py prepends its PACKET_PREAMBLE and POSTs the whole packet; no num_predict cap
    M=$(sed -n 's/^OLLAMA1="\([^"]*\)".*/\1/p' "$R/tools/panel.sh")
    python "$R/tools/panel_ollama.py" "$M" "$H/glm_mte564p2.txt" "$H/packet_564p2_GLM.md"
    echo "rc=$?" > "$H/glm_mte564p2.exit"; echo "glm ($M) $(cat "$H/glm_mte564p2.exit") out $(wc -c < "$H/glm_mte564p2.txt") b" ;;
*)
    echo "usage: launch_p2.sh astra|grok|glm  (the Fable seat is an Agent call, not this script)"; exit 2 ;;
esac
