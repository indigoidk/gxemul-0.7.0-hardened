#!/bin/bash
#  PASS 5 Fable seat, second mutant: the FAULT member (`break' -> `return 0') at an
#  OPERATOR-ONLY block (VECBASE).  Part 4 measured it only at GENCTL, where a GUEST st.h
#  faults.  Prediction: 101/101 TOTAL ESCAPE (no guest wide access reaches an odd offset;
#  the debugger put merely prints FAILED!, which no row counts).  Same restored clone.
set -u
G=/mnt/c/DocumentNoSnc/CC/GXEMUL; SEC=$G/GXEMUL-SEC; T=/tmp/gxfable_p5; F=src/devices/dev_pcc2.c
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p5_fable
say() { echo "[$(date +%H:%M:%S)] $*"; }
die() { echo "*** ABORT: $*"; exit 9; }
[ -d "$T" ] || die "clone missing"
[ -e "$T/.MUTANT" ] && die "clone carries a sentinel -- not starting"
cmp -s "$T/$F" "$SEC/$F" || die "clone not clean vs SEC before start"
build() { cd "$T" || die cd; rm -f src/devices/dev_pcc2.o; make -j4 > "$OUT/build_$1.log" 2>&1; [ "$T/gxemul" -nt "$T/$F" ] || die "$1: binary not newer than source"; }
score() {
    cd "$SEC/regress" || die cd
    python3 -u "$OUT/frozen_probe.py" "$T/gxemul" "$1" > "$OUT/$1.out" 2>&1
    grep -q PCC2W_PROBE_DONE "$OUT/$1.out" || die "$1: NO COMPLETION SENTINEL"
    say "  $1 [$2]: $(grep -m1 PCC2W_RESULT "$OUT/$1.out")"
    grep -m1 PCC2W_RED "$OUT/$1.out" | sed 's/PCC2W_RED=/      RED: /' || true
}
echo "$F  mutant M_RET0_VECBASE" > "$T/.MUTANT"; cp "$SEC/$F" "$T/$F"
python3 - "$T/$F" <<'PYEOF'
import io, sys
p = sys.argv[1]; s = io.open(p, encoding='utf-8').read()
a = '\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_VECBASE_LEN, "PCCTWO_VECBASE", len);\n\t\t\tbreak;\n\t\t}\n'
assert s.count(a) == 1, "VECBASE guard anchor count=%d" % s.count(a)
s = s.replace(a, a.replace('\t\t\tbreak;\n', '\t\t\treturn 0;\n'))
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
PYEOF
cmp -s "$T/$F" "$SEC/$F" && die "M_RET0_VECBASE: file UNCHANGED"
say "    [M_RET0_VECBASE] mutant text: $(grep -c 'return 0;' "$T/$F") ret0 (fix has 0)"
build M_RET0_VECBASE
say "    [M_RET0_VECBASE] binary $(date -r "$T/gxemul" +%H:%M:%S)  source $(date -r "$T/$F" +%H:%M:%S)"
score M_RET0_VECBASE "predict 101/101 ESCAPE"
say "    FAILED! lines in the op vecbase session are the only varying observable; count in the whole log: $(grep -c 'FAILED!' "$OUT/M_RET0_VECBASE.out")"
cp "$SEC/$F" "$T/$F"; cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED -- sentinel KEPT"
build restore2; rm -f "$T/.MUTANT"; say "  restored + REBUILT + verified, sentinel cleared"
say "KILL_P5_FABLE_RET0_DONE"
