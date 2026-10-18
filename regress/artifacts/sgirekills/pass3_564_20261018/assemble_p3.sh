#!/bin/bash
#  assemble_p3.sh -- #564's PASS-3 packets: the repair's own review.  The repair diff is taken against the pass-2 state
#  preserved beside this file (dev_sgi_re.pass2_1d65cdc1.c, gate_arm.pass2.sh, sgi_mte_decline_probe.pass2_86caed24.py);
#  the fixed function, the repaired probe and the gate block are inlined whole from the working tree; kill table 3, its
#  PRETABLE3 and the errata are inlined whole; the per-row catcher table is computed by p3_tables.py.  Refuses (exit 9)
#  on: a HEAD other than 2951694f, an md5 other than the repaired one, a diff with ZERO hunks, a void or incomplete
#  table, or a missing anchor.
set -u
H=$(cd "$(dirname "$0")" && pwd)
A=$(cd "$H/.." && pwd)
R=$(cd "$H/../../../.." && pwd)
K3="$A/killtable3_564_20261017"
[ "$(git -C "$R" rev-parse --short=8 HEAD)" = "2951694f" ] || { echo "ASSEMBLY FAIL: HEAD moved"; exit 9; }
SRC="$R/src/devices/dev_sgi_re.c"; PROBE="$R/regress/sgi_mte_decline_probe.py"; GATE="$R/regress/gate_arm.sh"
m() { md5sum < "$1" | cut -c1-8; }
[ "$(m "$SRC")" = "23fa76aa" ] || { echo "ASSEMBLY FAIL: dev_sgi_re.c is $(m "$SRC")"; exit 9; }
[ "$(m "$PROBE")" = "8928a02f" ] || { echo "ASSEMBLY FAIL: the probe is $(m "$PROBE")"; exit 9; }
for f in p3_head.md q3_all.md q3_astra.md p3_tables.py dev_sgi_re.pass2_1d65cdc1.c gate_arm.pass2.sh sgi_mte_decline_probe.pass2_86caed24.py; do
    [ -s "$H/$f" ] || { echo "ASSEMBLY FAIL: missing $f"; exit 9; }; done
for f in PRETABLE3.out mutants_564c.py KILLTABLE3.txt; do [ -s "$K3/$f" ] || { echo "ASSEMBLY FAIL: missing $K3/$f"; exit 9; }; done
grep -q '^base all-green, null all-red: table valid$' "$K3/KILLTABLE3.txt" || { echo "ASSEMBLY FAIL: table 3 is void"; exit 9; }
grep -qE 'MISSING|INCOMPLETE' "$K3/KILLTABLE3.txt" && { echo "ASSEMBLY FAIL: table 3 has a missing or incomplete run"; exit 9; }
D1=$(diff -u "$H/dev_sgi_re.pass2_1d65cdc1.c" "$SRC"); D2=$(diff -u "$H/gate_arm.pass2.sh" "$GATE")
D3=$(diff -u "$H/sgi_mte_decline_probe.pass2_86caed24.py" "$PROBE")
h1=$(printf '%s\n' "$D1" | grep -c '^@@'); h2=$(printf '%s\n' "$D2" | grep -c '^@@'); h3=$(printf '%s\n' "$D3" | grep -c '^@@')
[ "$h1" -gt 0 ] && [ "$h2" -gt 0 ] && [ "$h3" -gt 0 ] || { echo "ASSEMBLY FAIL: diff hunks $h1/$h2/$h3"; exit 9; }
fn() {  # the function whole, from its signature line through its first column-0 `}'
    RS_S="$2" awk 'index($0, ENVIRON["RS_S"]) == 1 { on = 1 } on { printf "%5d  %s\n", NR, $0 } on && /^}/ { exit }' "$1" > "$H/.ex"
    tail -1 "$H/.ex" | grep -q '  }$' || { echo "ASSEMBLY FAIL: '$2'" >&2; exit 9; }
    cat "$H/.ex"; rm -f "$H/.ex"
}
blk() {  # the gate's sgi_mte block, from its header through the block's own closing `fi'
    awk '/^#  ---- #564 sgirekills/ { on = 1 } on { printf "%5d  %s\n", NR, $0 } on && /^fi$/ { exit }' "$GATE" > "$H/.ex"
    grep -q 'sgi_mte rows red' "$H/.ex" || { echo "ASSEMBLY FAIL: gate block" >&2; exit 9; }
    cat "$H/.ex"; rm -f "$H/.ex"
}
T=$(python "$H/p3_tables.py" "$A") || { echo "ASSEMBLY FAIL: p3_tables -- $T"; exit 9; }
body() {
    cat "$H/p3_head.md"
    echo "Diff hunks inlined: \`dev_sgi_re.c\` $h1, \`gate_arm.sh\` $h2, \`sgi_mte_decline_probe.py\` $h3."
    echo
    echo "### 3a. \`src/devices/dev_sgi_re.c\` -- 1d65cdc1 -> 23fa76aa (comment only)"
    echo; echo '```diff'; printf '%s\n' "$D1"; echo '```'; echo
    echo "### 3b. \`regress/gate_arm.sh\` -- the block re-pinned to 68 rows"
    echo; echo '```diff'; printf '%s\n' "$D2"; echo '```'; echo
    echo "### 3c. \`regress/sgi_mte_decline_probe.py\` -- 86caed24 -> 8928a02f"
    echo; echo '```diff'; printf '%s\n' "$D3"; echo '```'; echo
    echo "## 4. The shipped composite, whole"
    echo
    echo "### 4a. \`do_mte_transfer()\` (working tree, 23fa76aa) -- every exit path"
    echo; echo '```c'; fn "$SRC" 'void do_mte_transfer(struct cpu* cpu, struct sgi_re_data *d)' || exit 9; echo '```'; echo
    echo "### 4b. The latch enum's tail"
    echo; echo '```c'; awk 'NR>=139 && NR<=187 { printf "%5d  %s\n", NR, $0 }' "$SRC"; echo '```'; echo
    echo "### 4c. \`regress/sgi_mte_decline_probe.py\` (8928a02f, $(wc -l < "$PROBE") lines), whole"
    echo; echo '```python'; awk '{ printf "%4d  %s\n", NR, $0 }' "$PROBE"; echo '```'; echo
    echo "### 4d. \`regress/gate_arm.sh\`'s sgi_mte block, whole"
    echo; echo '```sh'; blk || exit 9; echo '```'; echo
    echo "## 5. Kill table 3"
    echo
    echo "### 5a. \`PRETABLE3.out\` -- written $(date -r "$K3/PRETABLE3.out" '+%Y-%m-%d %H:%M:%S'), before table 3's first log ($(date -r "$(ls -tr "$K3"/raw3/*.out | head -1)" '+%Y-%m-%d %H:%M:%S'))"
    echo; echo '```'; cat "$K3/PRETABLE3.out"; echo '```'; echo
    echo "### 5b. \`mutants_564c.py\`, whole"
    echo; echo '```python'; cat "$K3/mutants_564c.py"; echo '```'; echo
    echo "### 5c. \`KILLTABLE3.txt\`"
    echo; echo '```'; cat "$K3/KILLTABLE3.txt"; echo '```'; echo
    echo "### 5d. Per row: its HEAD 2951694f value and the table-3 mutants that turned it red (computed from raw3/)"
    echo; echo '```'; printf '%s\n' "$T"; echo '```'; echo
    echo "## 6. \`PRETABLE_ERRATA.txt\` (corrections to table 1's PRETABLE.out), whole"
    echo; echo '```'; cat "$A/killtable_564_20261017/PRETABLE_ERRATA.txt"; echo '```'; echo
}
body > "$H/body.md" || { echo "ASSEMBLY FAIL: body"; exit 9; }
for seat in ASTRA GROK GLM FABLE; do
    tok="${seat}_MTE564P3_20261018"
    q="$H/q3_all.md"; [ "$seat" = ASTRA ] && q="$H/q3_astra.md"
    { echo "**Your token: \`$tok\`** -- open your answer with it."; echo; cat "$H/body.md" "$q"; } > "$H/packet_564p3_$seat.md"
    printf '%-6s %7d bytes  token %s\n' "$seat" "$(wc -c < "$H/packet_564p3_$seat.md")" "$tok"
done
echo "diff hunks inlined: dev_sgi_re.c $h1, gate_arm.sh $h2, probe $h3"
echo ASSEMBLY_OK
