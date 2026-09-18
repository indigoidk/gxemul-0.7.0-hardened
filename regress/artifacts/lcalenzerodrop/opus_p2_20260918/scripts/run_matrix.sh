#!/bin/bash
#  run_matrix.sh <parallelism> <binlist> <celllist>   e.g.  run_matrix.sh 4 "base va" "frozen k16"
#  Runs each (cell, binary) leg from FROZEN probe copies in /tmp/gxopus530p2_probe; one log per leg.
set -u
P=$1; BLIST=$2; CLIST=$3
WIN=/mnt/c/Users/User00/AppData/Local/Temp/opus530p2
export PR=/tmp/gxopus530p2_probe
export BINS=/tmp/gxopus530p2_bins
export LOGS=/tmp/gxopus530p2_logs
mkdir -p "$LOGS"
#  freeze the instrument for this run: the copy is what runs, the Windows original may be edited meanwhile
if [ ! -f "$PR/lca_widecell_probe.py" ] || ! cmp -s "$WIN/lca_widecell_probe.py" "$PR/lca_widecell_probe.py"; then
    cp "$WIN/lca_widecell_probe.py" "$PR/lca_widecell_probe.py"
fi
md5sum "$PR/lca_widewrite_probe.py" "$PR/lca_widecell_probe.py" "$PR/alpha_dummy.bin"
run1() {
    c=$1; b=$2
    if [ "$c" = frozen ]; then
        WIDEWRITE_RAW="$LOGS/raw_frozen__$b.txt" timeout 600 python3 -u "$PR/lca_widewrite_probe.py" "$BINS/$b" "$b" \
            > "$LOGS/frozen__$b.log" 2>&1
    else
        WIDECELL_RAW="$LOGS/raw_${c}__$b.txt" timeout 600 python3 -u "$PR/lca_widecell_probe.py" "$BINS/$b" "$b" "$c" \
            > "$LOGS/${c}__$b.log" 2>&1
    fi
    echo "$(date '+%T') done $c $b rc=$? :: $(grep -E 'RESULT=' "$LOGS/"*"${c}__$b.log" | tail -1) :: $(tail -1 "$LOGS/"*"${c}__$b.log")"
}
export -f run1
for c in $CLIST; do for b in $BLIST; do echo "$c $b"; done; done > "$LOGS/jobs_$$.txt"
echo "== $(date '+%F %T') $(wc -l < "$LOGS/jobs_$$.txt") legs, parallelism $P"
xargs -P "$P" -L 1 bash -c 'run1 "$0" "$1"' < "$LOGS/jobs_$$.txt"
echo "RUN_MATRIX_DONE $(date '+%F %T')"
