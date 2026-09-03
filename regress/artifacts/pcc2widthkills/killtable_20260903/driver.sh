#!/bin/bash
#  pcc2widthkills KILL TABLE -- runs AFTER the pass-15 table clears (one emulator at a time).
#
#  Sequence, each a checkpoint line:
#    0. PREFIX  -- the pcc2 detector against the COMMITTED build (pre-fix dev_pcc2.c):
#                  floor clause (a).  Predicted: every survival/op row red, controls green.
#    1. propagate SEC's dev_pcc2.c into the clone, rebuild, BASE must be 60/60.
#    2. mutants, each labelled with the row it must red:
#         M_DELETE   GENCTL guard removed outright         -> rb genctl reads 0xbb (lane hazard)
#         M_NOBREAK  decline announced, then falls through -> rb genctl reads 0xbb, rb genctl dcl 1
#         M_ASSIGN   latch never set                       -> latch same 2
#         M_SHARED   every block uses GENCTL's bit         -> latch two 1
#         M_RDKILL   read side killed again at GENCTL      -> hrd genctl exit1
#         M_OPKILL   VECBASE (odd, operator-reachable) killed again -> op vecbase exit1
#         M_COMPOSE  accidental per-lane store on GENCTL   -> rb genctl 0xaa, rb vecbase 0xb0
#    3. restore + rebuild + verify, clear the sentinel.
set -u
G=/mnt/c/DocumentNoSnc/CC/GXEMUL; SEC=$G/GXEMUL-SEC; T=/tmp/gxpcc2; F=src/devices/dev_pcc2.c
OUT=/tmp/killpcc2; PROBE=pcc2_width_probe.py
say() { echo "[$(date +%H:%M:%S)] $*"; }
die() { echo "*** ABORT: $*"; exit 9; }
rm -rf "$T" "$OUT"; mkdir -p "$OUT"
say "clone build/ -> $T (build/ still carries the PRE-fix dev_pcc2.c: that is the PREFIX cell)"
cp -a "$G/build" "$T" || die "clone failed"
cp "$SEC/regress/$PROBE" "$OUT/frozen_probe.py" || die "cannot freeze probe"
say "  instrument frozen: $(wc -c < "$OUT/frozen_probe.py") bytes"
#  build/ carries the FIXED file by the time this runs (it was rebuilt for the gate), so
#  the PREFIX cell installs HEAD's pre-fix copy into the clone explicitly, and says so.
git -C "$SEC" show HEAD:$F > "$OUT/dev_pcc2.PREFIX.c" || die "cannot extract HEAD's $F"
cp "$OUT/dev_pcc2.PREFIX.c" "$T/$F"
cmp -s "$T/$F" "$SEC/$F" && die "PREFIX copy is identical to the fixed file -- HEAD already has the fix?"
say "  PREFIX: HEAD's pre-fix $F installed in the clone (differs from SEC, as it must)"

build() { cd "$T" || die cd; rm -f src/devices/dev_pcc2.o; make -j4 > "$OUT/build_$1.log" 2>&1; [ "$T/gxemul" -nt "$T/$F" ] || die "$1: binary not newer than source"; }
score() {
    cd "$SEC/regress" || die cd
    python3 -u "$OUT/frozen_probe.py" "$T/gxemul" "$1" > "$OUT/$1.out" 2>&1
    grep -q PCC2W_PROBE_DONE "$OUT/$1.out" || die "$1: NO COMPLETION SENTINEL"
    say "  $1 [$2]: $(grep -m1 PCC2W_RESULT "$OUT/$1.out")"
    grep -m1 PCC2W_RED "$OUT/$1.out" | sed 's/PCC2W_RED=/      RED: /' || true
}

say "PREFIX -- floor clause (a), the committed build"
build PREFIX; score PREFIX PREFIX

say "PROPAGATE the fix into the clone, rebuild, BASE"
cp "$SEC/$F" "$T/$F"; cmp -s "$T/$F" "$SEC/$F" || die "propagate failed"
build BASE; score BASE CONTROL
BASE_RES=$(grep -m1 PCC2W_RESULT "$OUT/BASE.out" | cut -d= -f2)
[ "$BASE_RES" = "60/60" ] || say "*** BASE IS NOT FULL ($BASE_RES): $(grep -m1 PCC2W_RED "$OUT/BASE.out") -- CONTINUING; read every cell with those rows SUBTRACTED ***"

mut() {  # $1 name  $2 expectation  $3 python edit body (operates on s)
    echo "$F  mutant $1" > "$T/.MUTANT"; cp "$SEC/$F" "$T/$F"
    python3 - "$T/$F" "$3" <<'PYEOF'
import io, sys
p, body = sys.argv[1], sys.argv[2]
s = io.open(p, encoding='utf-8').read()
ns = {'s': s}
exec(body, ns)
io.open(p, 'w', encoding='utf-8', newline='\n').write(ns['s'])
PYEOF
    [ $? -eq 0 ] || die "$1: mutator failed"
    cmp -s "$T/$F" "$SEC/$F" && die "$1: file UNCHANGED after mutation"
    build "$1"; score "$1" "$2"
}
G1='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_GENCTL_LEN, "PCCTWO_GENCTL", len);\n\t\t\tbreak;\n\t\t}\n'
V1='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_VECBASE_LEN, "PCCTWO_VECBASE", len);\n\t\t\tbreak;\n\t\t}\n'

mut M_DELETE  'rb genctl 0xbb' "a='$G1'; assert s.count(a)==1; s=s.replace(a,'')"
mut M_NOBREAK 'rb genctl 0xbb + dcl 1' "a='$G1'; b=a.replace('\t\t\tbreak;\n',''); assert s.count(a)==1; s=s.replace(a,b)"
mut M_ASSIGN  'latch same 2' "a='\t\td->warned |= (1u << bit);\n'; assert s.count(a)==1; s=s.replace(a,'')"
mut M_SHARED  'latch two 1' "import re; n=len(re.findall(r'pcc2_width_decline\(d, PCC2_W_[A-Z]+_LEN,', s)); assert n==12, n; s=re.sub(r'pcc2_width_decline\(d, PCC2_W_[A-Z]+_LEN,', 'pcc2_width_decline(d, PCC2_W_GENCTL_LEN,', s)"
mut M_RDKILL  'hrd genctl exit1' "a='$G1'; b=a.replace('if (len != 1 && writeflag == MEM_WRITE) {', 'if (len != 1 && writeflag == MEM_READ) { exit(1); }\n\t\tif (len != 1 && writeflag == MEM_WRITE) {'); assert s.count(a)==1; s=s.replace(a,b)"
mut M_OPKILL  'op vecbase exit1' "a='$V1'; b='\t\tif (len != 1) { exit(1); }\n'; assert s.count(a)==1; s=s.replace(a,b)"
mut M_COMPOSE 'rb genctl 0xaa, rb vecbase 0xb0' "a='$G1'; b='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tmemcpy(d->pcctwo_reg + relative_addr, data, len);\n\t\t\td->pcctwo_reg[PCCTWO_VECBASE] &= 0xf0;\n\t\t\tbreak;\n\t\t}\n'; assert s.count(a)==1; s=s.replace(a,b)"

say "RESTORE from SEC + REBUILD + verify, THEN clear the sentinel"
cp "$SEC/$F" "$T/$F"; cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED -- sentinel KEPT"
build restore; rm -f "$T/.MUTANT"
say "  restored + REBUILT + verified, sentinel cleared"
say "KILLPCC2_DONE"
