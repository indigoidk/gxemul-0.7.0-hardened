#!/bin/bash
#  assemble_p2.sh -- the #564 (sgirekills, MTE half) pass-2 packets: one per seat.  The diff and the two fixed functions
#  come from the WORKING TREE (the round is uncommitted), every excerpt checked against a text anchor; the detector,
#  PRETABLE, both mutant definitions and both kill tables are inlined whole; the shipped-instrument join and the
#  never-red table are COMPUTED from the logs by p2_tables.py.  Refuses (exit 9) on: a HEAD other than 2951694f, a
#  working-tree file whose md5 is not the one tabled/shipped, a diff with ZERO hunks (a `git show | head` once inlined a
#  commit message and no diff into three panels), a log without its sentinel, or a void kill table.
set -u
H=$(cd "$(dirname "$0")" && pwd)
A=$(cd "$H/.." && pwd)
R=$(cd "$H/../../../.." && pwd)
K="$A/killtable_564_20261017"
HEADSHA=$(git -C "$R" rev-parse --short=8 HEAD)
[ "$HEADSHA" = "2951694f" ] || { echo "ASSEMBLY FAIL: HEAD is $HEADSHA, the brief is written against 2951694f"; exit 9; }
SRC="$R/src/devices/dev_sgi_re.c"; PROBE="$R/regress/sgi_mte_decline_probe.py"
m() { md5sum < "$1" | cut -c1-8; }
[ "$(m "$SRC")" = "1d65cdc1" ] || { echo "ASSEMBLY FAIL: dev_sgi_re.c is $(m "$SRC"), not the tabled 1d65cdc1"; exit 9; }
[ "$(m "$PROBE")" = "86caed24" ] || { echo "ASSEMBLY FAIL: the probe is $(m "$PROBE"), not the shipped 86caed24"; exit 9; }
[ "$(m "$K/sgi_mte_decline_probe.tabled.py")" = "8d625289" ] || { echo "ASSEMBLY FAIL: tabled instrument md5"; exit 9; }
for f in p2_head.md q2_all.md q2_astra.md p2_tables.py; do [ -s "$H/$f" ] || { echo "ASSEMBLY FAIL: missing $f"; exit 9; }; done
for f in PRETABLE.out mutants_564.py mutants_564b.py KILLTABLE.txt KILLTABLE2.txt; do
    [ -s "$K/$f" ] || { echo "ASSEMBLY FAIL: missing $K/$f"; exit 9; }; done
grep -q '^KILL TABLE: 34/34 killed$' "$K/KILLTABLE.txt" || { echo "ASSEMBLY FAIL: table 1 is not the 34/34 run"; exit 9; }
for t in KILLTABLE.txt KILLTABLE2.txt; do
    grep -q '^base all-green, null all-red: table valid$' "$K/$t" || { echo "ASSEMBLY FAIL: $t is void"; exit 9; }
    grep -qE 'MISSING|INCOMPLETE' "$K/$t" && { echo "ASSEMBLY FAIL: $t has a missing or incomplete run"; exit 9; }
done
D1=$(git -C "$R" diff HEAD -- src/devices/dev_sgi_re.c); D2=$(git -C "$R" diff HEAD -- regress/gate_arm.sh)
h1=$(printf '%s\n' "$D1" | grep -c '^@@'); h2=$(printf '%s\n' "$D2" | grep -c '^@@')
[ "$h1" -gt 0 ] && [ "$h2" -gt 0 ] || { echo "ASSEMBLY FAIL: diff hunks inlined: dev_sgi_re.c $h1, gate_arm.sh $h2"; exit 9; }
fn() {  # fn <file> <signature line, exact at column 0> -- the function whole, through its first column-0 `}'
    awk -v s="$2" 'index($0, s) == 1 { on = 1 } on { printf "%5d  %s\n", NR, $0 } on && /^}/ { exit }' "$1" > "$H/.ex"
    [ -s "$H/.ex" ] || { echo "ASSEMBLY FAIL: no function '$2' in $1" >&2; exit 9; }
    tail -1 "$H/.ex" | grep -q '  }$' || { echo "ASSEMBLY FAIL: '$2' did not end at a column-0 brace" >&2; exit 9; }
    cat "$H/.ex"; rm -f "$H/.ex"
}
J=$(python "$H/p2_tables.py" "$A" join) || { echo "ASSEMBLY FAIL: join -- $J"; exit 9; }
N=$(python "$H/p2_tables.py" "$A" neverred) || { echo "ASSEMBLY FAIL: neverred -- $N"; exit 9; }
PT=$(date -r "$K/PRETABLE.out" '+%Y-%m-%d %H:%M:%S'); R1=$(ls -tr "$K"/raw/*.out | head -1); R1T=$(date -r "$R1" '+%Y-%m-%d %H:%M:%S')
body() {
    cat "$H/p2_head.md"
    echo '```'
    git -C "$R" diff --numstat HEAD -- src/devices/dev_sgi_re.c regress/gate_arm.sh | \
        awk '{ printf "%s\t%s\t%s    INLINED (%s)\n", $1, $2, $3, ($3 ~ /gate_arm/ ? "section 3d" : "section 3a, and 3b-3c whole") }'
    printf '%s\t0\tregress/sgi_mte_decline_probe.py    NEW FILE, INLINED WHOLE (section 4)\n' "$(wc -l < "$PROBE")"
    echo '```'
    echo
    echo "No other file is this round's.  Diff hunks inlined: \`dev_sgi_re.c\` $h1, \`gate_arm.sh\` $h2."
    echo
    echo "### 3a. \`src/devices/dev_sgi_re.c\` -- the whole diff against HEAD (working tree md5 1d65cdc1, HEAD 60203f67)"
    echo
    echo '```diff'; printf '%s\n' "$D1"; echo '```'
    echo
    echo "### 3b. \`do_mte_transfer()\` AFTER the fix -- WHOLE, every exit path, working-tree line numbers"
    echo
    echo '```c'; fn "$SRC" 'void do_mte_transfer(struct cpu* cpu, struct sgi_re_data *d)' || exit 9; echo '```'
    echo
    echo "### 3c. \`DEVICE_ACCESS(sgi_mte)\` -- WHOLE (unchanged): the only caller, and the common tail after \`do_mte_transfer()\` returns"
    echo
    echo '```c'; fn "$SRC" 'DEVICE_ACCESS(sgi_mte)' || exit 9; echo '```'
    echo
    echo "### 3d. \`regress/gate_arm.sh\` -- the whole diff (the targeted gate's new block)"
    echo
    echo '```diff'; printf '%s\n' "$D2"; echo '```'
    echo
    echo "## 4. The detector, WHOLE -- \`regress/sgi_mte_decline_probe.py\` as shipped (md5 86caed24, $(wc -l < "$PROBE") lines)"
    echo
    echo "The TABLED instrument (md5 8d625289) differs from this file in one place only: the row-name field is 14 columns"
    echo "there and 16 here (section 2)."
    echo
    echo '```python'; awk '{ printf "%4d  %s\n", NR, $0 }' "$PROBE"; echo '```'
    echo
    echo "## 5. The kill tables"
    echo
    echo "### 5a. \`PRETABLE.out\` -- written $PT, before table 1's first log ($R1T)"
    echo
    echo '```'; cat "$K/PRETABLE.out"; echo '```'
    echo
    echo "### 5b. The mutants: \`mutants_564.py\` (table 1) and \`mutants_564b.py\` (table 2), whole"
    echo
    echo '```python'; cat "$K/mutants_564.py"; echo '```'
    echo
    echo '```python'; cat "$K/mutants_564b.py"; echo '```'
    echo
    echo "### 5c. \`KILLTABLE.txt\` -- table 1, the TABLED instrument (8d625289), 34 mutants"
    echo
    echo '```'; cat "$K/KILLTABLE.txt"; echo '```'
    echo
    echo "### 5d. \`KILLTABLE2.txt\` -- table 2, the SHIPPED instrument (86caed24): the two accept-side growth mutants table 1 lacked"
    echo
    echo '```'; cat "$K/KILLTABLE2.txt"; echo '```'
    echo
    echo "### 5e. Per row: how many mutants turned it red (computed from every raw log of both tables)"
    echo
    echo '```'; printf '%s\n' "$N"; echo '```'
    echo
    echo "## 6. The SHIPPED instrument on both builds (md5 86caed24), row by row"
    echo
    echo '```'; printf '%s\n' "$J"; echo '```'
    echo
}
body > "$H/body.md" || { echo "ASSEMBLY FAIL: body"; exit 9; }
for seat in ASTRA GROK GLM FABLE; do
    tok="${seat}_MTE564P2_20261017"
    q="$H/q2_all.md"; [ "$seat" = ASTRA ] && q="$H/q2_astra.md"
    { echo "**Your token: \`$tok\`** -- open your answer with it."; echo; cat "$H/body.md"; cat "$q"; } > "$H/packet_564p2_$seat.md"
    printf '%-6s %7d bytes  token %s\n' "$seat" "$(wc -c < "$H/packet_564p2_$seat.md")" "$tok"
done
echo "diff hunks inlined: dev_sgi_re.c $h1, gate_arm.sh $h2"
echo ASSEMBLY_OK
