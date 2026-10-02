#!/bin/bash
# compare.sh -- every candidate/mutant's rows diffed against the `decline' candidate's rows (label line dropped)
O=/tmp/gxopuscrime_out
for v in "$@"; do
    [ -f "$O/rows_$v.out" ] || { echo "== $v: NO OUTPUT"; continue; }
    tail -1 "$O/rows_$v.out" | grep -q CRIMEO_DONE || echo "== $v: SENTINEL MISSING"
    n=$(diff <(tail -n +2 "$O/rows_decline.out") <(tail -n +2 "$O/rows_$v.out") | grep -c '^>')
    m=$(diff <(tail -n +2 "$O/rows_decline.out") <(tail -n +2 "$O/rows_$v.out") | grep -c '^<')
    echo "== $v vs decline: $n lines only in $v, $m lines only in decline (decline has $(tail -n +2 "$O/rows_decline.out" | wc -l), $v has $(tail -n +2 "$O/rows_$v.out" | wc -l))"
    diff <(tail -n +2 "$O/rows_decline.out") <(tail -n +2 "$O/rows_$v.out") | grep '^>' | cut -c1-200
done
