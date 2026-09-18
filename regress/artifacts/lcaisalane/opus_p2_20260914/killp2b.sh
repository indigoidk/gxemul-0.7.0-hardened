#!/bin/bash
# killp2b.sh -- #530 pass-2 measuring seat (Opus 5), leg B.  Builds `head' (HEAD's dev_lca.c verbatim) and
# `p_andmask' (table 1's m_andmask edit, re-built here) in the clone /tmp/gxopus530, then runs split_probe.py
# (unaligned K0SEG accesses crossing a 1 KB boundary at the UART scratch port) on base, head, p_andmask, and
# the 37-row probe on p_andmask.  Launched from a frozen copy.
set -u
K=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/lcaisalane/opus_p2_20260914
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus530
B=/tmp/gxopus530_bins
F=src/devices/dev_lca.c
SPL=$K/split_probe.frozen.py
DSC=$K/disc_probe.frozen.py
cp "$K/split_probe.py" "$SPL"
cp "$K/disc_probe.py" "$DSC"
md5sum "$SPL" "$DSC" "$SEC/$F" | tee "$K/logs/INSTRUMENT_b.md5"
cd "$C" || exit 1
[ -e .MUTANT ] && { echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; }
cmp -s "$F" "$SEC/$F" && echo "BASELINE_CMP CLEAN" || { echo "BASELINE_CMP DIFFERS -- abort"; exit 1; }
echo "$F #530 pass-2 opus seat leg B -- restore from GXEMUL-SEC" > .MUTANT
build() {
    rm -f src/devices/dev_lca.o
    make -j2 > "$K/builds/build_$1.log" 2>&1
    rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt "$F" ] && [ src/devices/dev_lca.o -nt "$F" ]; then
        cp gxemul "$B/$1"; echo "BUILD_OK $1"
    else
        echo "BUILD_FAIL $1 rc=$rc"; tail -20 "$K/builds/build_$1.log"; return 1
    fi
}
( cd "$SEC" && git show HEAD:$F ) > "$F"; diff -u "$SEC/$F" "$F" > "$K/logs/head.diff"; sleep 1
build head
python3 - "$SEC/$F" "$F" <<'PYEOF'
import io, sys
s = io.open(sys.argv[1], newline="").read()
a = "\tofs = (relative_addr & 3) % len;\n"
assert s.count(a) == 1
io.open(sys.argv[2], "w", newline="").write(s.replace(a, "\tofs = (relative_addr & 3) & (len - 1);\n"))
print("APPLIED p_andmask")
PYEOF
diff -u "$SEC/$F" "$F" > "$K/logs/p_andmask.diff"; sleep 1
build p_andmask
cp "$SEC/$F" "$F"; sleep 1
build restored2
if cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ]; then rm -f .MUTANT; echo "CLONE RESTORED cmp=clean binary-nt-source=yes"; else echo "CLONE RESTORE INCOMPLETE -- sentinel kept"; fi
cmp -s "$B/base" "$B/restored2" && echo "restored2 == base (byte-identical)" || echo "restored2 differs from base"
cd "$K"
for m in base head p_andmask p_nozero; do
    python3 -u "$SPL" "$B/$m" "$m" > "$K/logs/split_$m.out" 2>&1
    echo "== split $m"; cat "$K/logs/split_$m.out"
done
for m in base p_wbit1 p_wnarrow p_wdrop4 p_waddr4 p_lane0decl p_nozero p_rep4 p_q8lane p_port10 p_andmask; do
    python3 -u "$DSC" "$B/$m" "$m" > "$K/logs/disc_$m.out" 2>&1
    echo "== disc $m"; cat "$K/logs/disc_$m.out"
done
python3 -u "$K/lca_isalane_probe.opusp2.py" "$B/p_andmask" p_andmask > "$K/logs/probe_p_andmask.raw" 2>&1
echo "p_andmask $(grep '^LCAISALANE_RESULT=' "$K/logs/probe_p_andmask.raw") done=$(grep -c '^LCAISALANE_DONE' "$K/logs/probe_p_andmask.raw")"
echo KILLP2B_DONE
