#!/bin/bash
#  assemble_f2.sh -- #564's §F2 packets (the panel shares its pass-2 findings).  Code excerpts from the WORKING TREE
#  (the repair is not applied yet, so it is what pass 2 reviewed), each range found by pattern and checked against an
#  anchor; the label clause quoted from the project carrier.  Refuses (exit 9) on a missing anchor or a changed md5.
set -u
H=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$H/../../../.." && pwd)
SRC="$R/src/devices/dev_sgi_re.c"; PROBE="$R/regress/sgi_mte_decline_probe.py"; CAR="$R/../CLAUDE.md"
[ "$(md5sum < "$SRC" | cut -c1-8)" = "1d65cdc1" ] || { echo "ASSEMBLY FAIL: dev_sgi_re.c changed"; exit 9; }
[ "$(md5sum < "$PROBE" | cut -c1-8)" = "86caed24" ] || { echo "ASSEMBLY FAIL: the probe changed"; exit 9; }
rng() {  # rng <file> <start pattern> <end pattern> <anchor> -- lines from the first start match through the next end match
    #  patterns are passed through ENVIRON, not -v: awk processes backslash escapes in a -v value
    RS_S="$2" RS_E="$3" awk '!on && index($0, ENVIRON["RS_S"]) { on = 1; st = NR } on { printf "%5d  %s\n", NR, $0 } on && NR > st && index($0, ENVIRON["RS_E"]) { exit }' "$1" > "$H/.ex"
    grep -qF -- "$4" "$H/.ex" || { echo "ASSEMBLY FAIL: anchor '$4' not in $1 range '$2'" >&2; exit 9; }
    cat "$H/.ex"; rm -f "$H/.ex"
}
body() {
    cat "$H/f2_head.md"
    echo "## 3. The evidence, inlined"
    echo
    echo "### 3a. \`do_mte_transfer()\` (working tree, md5 1d65cdc1): the sibling warning, S1, S2 and the destination dispatch they bypass"
    echo
    echo '```c'; rng "$SRC" 'if (dst_y_step != 0 && dst_y_step' 'int src_x1 = (src0 >> 16)' 'switch (dst_tlb) {' || exit 9; echo '```'
    echo
    echo "### 3b. The linear arm: S3, S4 and S5 sit INSIDE the dispatch (they bypass no dispatch)"
    echo
    echo '```c'; rng "$SRC" 'case MTE_TLB_LIN_A:' ' *  Horrible hack:' 'SGIRE_W_MTE_BYTEMASK' || exit 9; echo '```'
    echo
    echo "### 3c. The latch enum's tail (the five new bits)"
    echo
    echo '```c'; rng "$SRC" 'SGIRE_W_BADMODE   = 1 << 10,' 'SGIRE_W_MTE_BYTEMASK = 1 << 17,' 'SGIRE_W_MTE_STIPPLE' || exit 9; echo '```'
    echo
    echo "### 3d. \`DEVICE_ACCESS(sgi_mte)\`'s tail: START runs the transfer on a read or a write"
    echo
    echo '```c'; rng "$SRC" 'sgi_mte: unimplemented read from address' 'return 1;' 'do_mte_transfer(cpu, d);' || exit 9; echo '```'
    echo
    echo "### 3e. The skipped-dispatch label clause, quoted from the project carrier (\`CLAUDE.md\`)"
    echo
    grep -o '\*\*AND A GUARD THAT SUPPRESSES A DISPATCH.*fit the new device\.\*\*' "$CAR" | sed 's/^/> /' > "$H/.cl"
    [ -s "$H/.cl" ] || { echo "ASSEMBLY FAIL: the clause text was not found in $CAR" >&2; exit 9; }
    cat "$H/.cl"; rm -f "$H/.cl"
    echo
    echo "### 3f. The detector's S1 and S2 sessions (\`regress/sgi_mte_decline_probe.py\`, md5 86caed24) -- the rows F9 is about"
    echo
    echo '```python'; rng "$PROBE" '# ================================================================ S1 STIPPLE' 'row("src once"' 'row("src 3 lin"' || exit 9; echo '```'
    echo
    echo "### 3g. The detector's LATCH session -- the only one that sets a pre-existing bit (F10)"
    echo
    echo '```python'; rng "$PROBE" '# ================================================================ LATCH' 'SGIRE_W_TLBA_LEN set before the new sites stays set after them' 'TLBA_LEN_TEXT' || exit 9; echo '```'
    echo
    echo "### 3h. Kill table 1 rows the findings cite (\`KILLTABLE.txt\`)"
    echo
    echo '```'; grep -A1 -E '^(d1|d2|s2tiled|shared|wrongbit) ' "$R/regress/artifacts/sgirekills/killtable_564_20261017/KILLTABLE.txt"; echo '```'
    echo
}
body > "$H/f2_body.md" || { echo "ASSEMBLY FAIL: body"; exit 9; }
for seat in ASTRA GROK GLM FABLE; do
    tok="${seat}_MTE564F2_20261017"
    { echo "**Your token: \`$tok\`** -- open your answer with it."; echo; cat "$H/f2_body.md" "$H/f2_q.md"; } > "$H/packet_564f2_$seat.md"
    printf '%-6s %7d bytes  token %s\n' "$seat" "$(wc -c < "$H/packet_564f2_$seat.md")" "$tok"
done
echo ASSEMBLY_OK
