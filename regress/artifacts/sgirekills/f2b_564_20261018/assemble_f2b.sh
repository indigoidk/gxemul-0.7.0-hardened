#!/bin/bash
#  assemble_f2b.sh -- #564's §F2 packets for pass 3: one scope question.  The rule texts are quoted VERBATIM from the
#  project carrier by anchor (a missing anchor refuses, exit 9), so a seat rules from the words that govern.
set -u
H=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$H/../../../.." && pwd)
CAR="$R/../CLAUDE.md"
for f in f2b_head.md f2b_q.md; do [ -s "$H/$f" ] || { echo "ASSEMBLY FAIL: missing $f"; exit 9; }; done
quote() {  # quote <label> <start anchor> <end anchor> -- the carrier lines from start through end, as a blockquote
    S="$2" E="$3" awk 'index($0, ENVIRON["S"]) && !on { on = 1 } on { print } on && index($0, ENVIRON["E"]) { exit }' "$CAR" > "$H/.q"
    [ -s "$H/.q" ] && grep -qF -- "$3" "$H/.q" || { echo "ASSEMBLY FAIL: rule text '$1' not found" >&2; exit 9; }
    echo "### $1"; echo; cat "$H/.q"; echo; rm -f "$H/.q"
}
body() {
    cat "$H/f2b_head.md"
    quote "4a. The joint-cell rule (2026-09-04)" "**DEPENDS-ON enumerates JOINT cells over the guard's operands" "is DISCLOSED under clause (e)." || exit 9
    quote "4b. The floor, as bounded on pass 11 (2026-09-04)" "#### *** THE LETTER OVER-DEMANDED" "the 2^k growth by another door" || exit 9
    quote "4c. The label clauses: the join (2026-09-09) and the skipped dispatch (2026-09-25 / 09-30)" "Opus, pass 10).  **AND THE JOIN ITSELF" "fit the new device.**" || exit 9
}
body > "$H/f2b_body.md" || { echo "ASSEMBLY FAIL: body"; exit 9; }
for seat in ASTRA GROK GLM; do
    tok="${seat}_MTE564F2B_20261018"
    { echo "**Your token: \`$tok\`** -- open your answer with it."; echo; cat "$H/f2b_body.md" "$H/f2b_q.md"; } > "$H/packet_564f2b_$seat.md"
    printf '%-6s %7d bytes  token %s\n' "$seat" "$(wc -c < "$H/packet_564f2b_$seat.md")" "$tok"
done
echo ASSEMBLY_OK
