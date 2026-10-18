#!/bin/bash
#  assemble_p1.sh -- the #564 (sgirekills, MTE half) pass-1 packets: one per seat, every code excerpt taken from HEAD
#  by `git show` with its real line numbers, each excerpt checked against a text anchor so a line shift REFUSES rather
#  than inlining the wrong lines.  Writes packet_564p1_<SEAT>.md here.
set -u
H=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$H/../../../.." && pwd)
HEADSHA=$(git -C "$R" rev-parse --short=8 HEAD)
[ "$HEADSHA" = "2951694f" ] || { echo "ASSEMBLY FAIL: HEAD is $HEADSHA, the brief is written against 2951694f"; exit 9; }
W="$R/regress/artifacts/sgirekills/witness_20261017/witness_HEAD_2951694f.out"
[ "$(tail -1 "$W")" = "MTEEXIT_DONE" ] || { echo "ASSEMBLY FAIL: the witness log has no sentinel"; exit 9; }
for f in p1_head.md p1_tail.md q_all.md q_astra.md; do [ -s "$H/$f" ] || { echo "ASSEMBLY FAIL: missing $f"; exit 9; }; done
SRC=$(mktemp); HDR=$(mktemp)
git -C "$R" show HEAD:src/devices/dev_sgi_re.c > "$SRC"
git -C "$R" show HEAD:src/include/thirdparty/crmfbreg.h > "$HDR"
ex() {  # ex <file> <from> <to> <anchor that must appear in the range>
    awk -v a="$2" -v b="$3" 'NR>=a && NR<=b {printf "%5d  %s\n", NR, $0}' "$1" > "$H/.ex"
    grep -qF -- "$4" "$H/.ex" || { echo "ASSEMBLY FAIL: anchor '$4' not in $1:$2-$3" >&2; exit 9; }
    cat "$H/.ex"; rm -f "$H/.ex"
}
body() {
    cat "$H/p1_head.md"
    cat "$W"
    echo '```'
    echo
    echo "## 3. The code, verbatim from HEAD 2951694f (\`src/devices/dev_sgi_re.c\`, md5 60203f67), real line numbers"
    echo
    echo "### 3a. \`do_mte_transfer()\` -- WHOLE, every exit path (the function under edit)"
    echo
    echo '```c'; ex "$SRC" 1458 1682 'void do_mte_transfer(struct cpu* cpu, struct sgi_re_data *d)' || exit 9; echo '```'
    echo
    echo "### 3b. \`DEVICE_ACCESS(sgi_mte)\` -- WHOLE: its only caller, and the common tail a \`return\` in 3a cannot skip"
    echo
    echo '```c'; ex "$SRC" 1684 1814 'do_mte_transfer(cpu, d);' || exit 9; echo '```'
    echo
    echo "### 3c. \`DEVICE_ACCESS(sgi_de_status)\` -- the status a guest polls (a constant)"
    echo
    echo '```c'; ex "$SRC" 1833 1873 'CRIME_DE_MTE_IDLE' || exit 9; echo '```'
    echo
    echo "### 3d. The house idiom in this file: the latch enum's head and tail, and one complete latched decline"
    echo
    echo '```c'; ex "$SRC" 58 75 'enum {' || exit 9; echo '  ...'; ex "$SRC" 139 170 'SGIRE_W_BADCOLOR  = 1 << 12,' || exit 9
    echo '  ...'; ex "$SRC" 257 309 'SGIRE_W_BADMODE' || exit 9; echo '```'
    echo
    echo "## 4. The constants (\`src/include/thirdparty/crmfbreg.h\` at HEAD)"
    echo
    echo '```c'; ex "$HDR" 238 275 'MTE_MODE_COPY' || exit 9; echo '  ...'; ex "$HDR" 422 426 'CRIME_DE_MTE_IDLE' || exit 9; echo '```'
    echo
    cat "$H/p1_tail.md"
}
body > "$H/body.md" || { echo "ASSEMBLY FAIL: body"; exit 9; }
for seat in ASTRA GROK GLM FABLE; do
    tok="${seat}_MTE564P1_20261017"
    q="$H/q_all.md"; [ "$seat" = ASTRA ] && q="$H/q_astra.md"
    { echo "**Your token: \`$tok\`** -- open your answer with it."; echo; cat "$H/body.md"; cat "$q"; } > "$H/packet_564p1_$seat.md"
    printf '%-6s %7d bytes  token %s\n' "$seat" "$(wc -c < "$H/packet_564p1_$seat.md")" "$tok"
done
rm -f "$SRC" "$HDR"
echo ASSEMBLY_OK
