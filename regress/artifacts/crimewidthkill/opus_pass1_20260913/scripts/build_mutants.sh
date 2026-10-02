#!/bin/bash
# build_mutants.sh -- second batch in the same scratch clone: mutants of the `decline' candidate.
set -u
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopuscrime
B=/tmp/gxopuscrime_bins
F=src/devices/dev_sgi_ip32.c
cd "$C" || exit 1
[ -e .MUTANT ] && { echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; }
if cmp -s "$F" "$SEC/$F"; then echo "BASELINE_CMP CLEAN $F"; else echo "BASELINE_CMP DIFFERS -- abort"; exit 1; fi
echo "$F crimewidthkill decline-mutants (opus pass1)" > .MUTANT
build() {
    rm -f src/devices/dev_sgi_ip32.o
    make -j4 > "$B/build_$1.log" 2>&1
    rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt "$F" ] && [ src/devices/dev_sgi_ip32.o -nt "$F" ]; then
        cp gxemul "$B/$1"; echo "BUILD_OK $1 rc=$rc fresh=yes"
    else
        echo "BUILD_FAIL $1 rc=$rc"; tail -20 "$B/build_$1.log"; return 1
    fi
}
for v in return1 fallsw nolatch len1only readonly; do
    python3 "$SP/apply_variant.py" "$v" "$SEC/$F" "$F" || { echo "APPLY FAILED $v"; exit 1; }
    diff -u "$SEC/$F" "$F" > "$B/$v.diff"
    build "$v" || exit 1
done
cp "$SEC/$F" "$F"
build restored2 || exit 1
if cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ]; then rm -f .MUTANT; echo "CLONE RESTORED cmp=clean binary-nt-source=yes"; else echo "CLONE RESTORE INCOMPLETE -- sentinel kept"; fi
cmp -s "$B/base" "$B/restored2" && echo "restored2 == base (byte-identical)" || echo "restored2 differs from base"
for v in fault decline delete return1 fallsw nolatch len1only readonly; do cmp -s "$B/base" "$B/$v" && echo "WARNING $v IDENTICAL TO base" || echo "$v differs from base"; done
grep -iE "warning|error" "$B"/build_*.log | grep -i sgi_ip32 || echo "no dev_sgi_ip32 warnings/errors in build logs"
echo BUILD_MUTANTS_DONE
