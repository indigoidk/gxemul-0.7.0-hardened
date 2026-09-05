#!/bin/bash
#  PART 2, reduced: M_ALIAS_SCCTX / M_LENGT2_MASK / M_FALL_MASK are the builder's M1 / M2 / M6,
#  which its own pass-3 table measures against the SAME instrument (md5 d9239db6).  Only the
#  pre-table block's yield, M_IDATA_GENCTL, is measured here.
#  The four M_FALL_* (odd-arm announce-then-land) are measured by the builder's pass 3b (78-row,
#  the breach) and 3c (82-row md5 cd22f951, the repair) on the SAME instrument; not repeated here.
#  pcc2widthkills pass-2 repair table -- the IPL/MASK rows.  Runs after the panels clear.
#    BASE          101/101 owed
#    M_DELETE_MASK MASK guard removed        -> rb mask reads 0xbb (the twin of M_DELETE)   was a 60/60 sweep
#    M_KILL_IPL    IPL width kill reinstated -> hrd ipl exit1 (GUEST-reachable, even)       was a 60/60 sweep
#    M_KILL_MASK   MASK width kill reinstated-> op mask exit1 (operator)                   was a 60/60 sweep
#    M_DELETE      (control) still reds rb genctl -- the repair perturbed nothing
#  PER-ARM (pass 2, grok): only GENCTL had a readback, so a guard edited at ONE arm escaped.
#    M_DELETE_TXICR  TXICR guard removed      -> rb t2icr 0x10 (halfword lands: 0xaab8 & 0x17)
#    M_LENGT2_TXICR  `len != 1' -> `len > 2'  -> rb t2icr 0x10, rb t2icr dcl 0
#    M_LENGT2_TXCTL  same at TXCTL            -> rb t2ctl 0x0  (0xaab8 & 3)
#    M_LENGT2_SCCTX  same at SCCTX            -> rb scctx 0x18 (0xaab8 & 0x1f)
#    M_LENGT2_SCCERR same at SCCERR           -> hwr sccerr dcl 0 (value-identical arm: message only)
#  THE BUILDER'S SWEEPS not already above (Opus, pass 2, table of 11):
#    M_ALIAS_SCCTX   SCCTX declines on SCCRX's bit (ONE char) -> latch all 11 (a collision drops the count)
#    M_LENGT2_MASK   MASK `len != 1' -> `len > 2'        -> rb mask 0xbb (halfword lands)
#    M_FALL_MASK     MASK announces then falls through   -> rb mask 0xbb
#    M_IDATA_GENCTL guard operand len -> idata > 0xff (PRE-TABLE yield) -> rb genctl lo 0x22, latch all 11
set -u
G=/mnt/c/DocumentNoSnc/CC/GXEMUL; SEC=$G/GXEMUL-SEC; T=/tmp/gxpcc2b4; F=src/devices/dev_pcc2.c
OUT=/tmp/killpcc2b4; PROBE=pcc2_width_probe.py
say() { echo "[$(date +%H:%M:%S)] $*"; }
die() { echo "*** ABORT: $*"; exit 9; }
rm -rf "$T" "$OUT"; mkdir -p "$OUT"
cp -a "$G/build" "$T" || die "clone failed"
cmp -s "$T/$F" "$SEC/$F" || { cp "$SEC/$F" "$T/$F"; say "  clone's $F refreshed from SEC (comment-only change since build/ was built)"; }
cp "$SEC/regress/$PROBE" "$OUT/frozen_probe.py" || die "cannot freeze probe"
say "  instrument frozen: $(wc -c < "$OUT/frozen_probe.py") bytes"
build() { cd "$T" || die cd; rm -f src/devices/dev_pcc2.o; make -j4 > "$OUT/build_$1.log" 2>&1; [ "$T/gxemul" -nt "$T/$F" ] || die "$1: binary not newer than source"; }
score() {
    cd "$SEC/regress" || die cd
    python3 -u "$OUT/frozen_probe.py" "$T/gxemul" "$1" > "$OUT/$1.out" 2>&1
    grep -q PCC2W_PROBE_DONE "$OUT/$1.out" || die "$1: NO COMPLETION SENTINEL"
    say "  $1 [$2]: $(grep -m1 PCC2W_RESULT "$OUT/$1.out")"
    grep -m1 PCC2W_RED "$OUT/$1.out" | sed 's/PCC2W_RED=/      RED: /' || true
}
mut() {
    echo "$F  mutant $1" > "$T/.MUTANT"; cp "$SEC/$F" "$T/$F"
    python3 - "$T/$F" "$3" <<'PYEOF'
import io, sys
p, body = sys.argv[1], sys.argv[2]; s = io.open(p, encoding='utf-8').read()
ns = {'s': s}; exec(body, ns); io.open(p, 'w', encoding='utf-8', newline='\n').write(ns['s'])
PYEOF
    [ $? -eq 0 ] || die "$1: mutator failed"
    cmp -s "$T/$F" "$SEC/$F" && die "$1: file UNCHANGED after mutation"
    say "    [$1] mutant text: $(grep -c 'len != 0' "$T/$F") len!=0, $(grep -c 'len & 6' "$T/$F") len&6, $(grep -c 'warned = (1u' "$T/$F") assign, $(grep -c 'warned |= 1;' "$T/$F") bit0, $(grep -c 'return 0;' "$T/$F") ret0"
    build "$1"
    say "    [$1] binary $(date -r "$T/gxemul" +%H:%M:%S)  source $(date -r "$T/$F" +%H:%M:%S)"
    score "$1" "$2"
}
G1='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_GENCTL_LEN, "PCCTWO_GENCTL", len);\n\t\t\tbreak;\n\t\t}\n'
M1='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_MASK_LEN, "PCCTWO_MASK", len);\n\t\t\tbreak;\n\t\t}\n'
I1='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_IPL_LEN, "PCCTWO_IPL", len);\n\t\t\tbreak;\n\t\t}\n'
X1='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_TXICR_LEN, "PCCTWO_TxICR", len);\n\t\t\tbreak;\n\t\t}\n'
X2='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_TXCTL_LEN, "PCCTWO_TxCTL", len);\n\t\t\tbreak;\n\t\t}\n'
X3='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_SCCTX_LEN, "PCCTWO_SCCTX", len);\n\t\t\tbreak;\n\t\t}\n'
X4='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_SCCERR_LEN, "PCCTWO_SCCERR", len);\n\t\t\tbreak;\n\t\t}\n'
say "BASE -- 101/101 owed"; build BASE; score BASE CONTROL
BASE_RES=$(grep -m1 PCC2W_RESULT "$OUT/BASE.out" | cut -d= -f2)
[ "$BASE_RES" = "101/101" ] || say "*** BASE IS NOT FULL ($BASE_RES): $(grep -m1 PCC2W_RED "$OUT/BASE.out") -- CONTINUING; read every cell with those rows SUBTRACTED ***"
X5='pcc2_width_decline(d, PCC2_W_SCCTX_LEN, "PCCTWO_SCCTX", len);'
X10='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_VECBASE_LEN, "PCCTWO_VECBASE", len);\n\t\t\tbreak;\n\t\t}\n'
X11='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_PSCALEADJ_LEN, "PCCTWO_PSCALEADJ", len);\n\t\t\tbreak;\n\t\t}\n'
X6='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_SCCICR_LEN, "PCCTWO_SCCICR", len);\n\t\t\tbreak;\n\t\t}\n'
X7='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_SCCRX_LEN, "PCCTWO_SCCRX", len);\n\t\t\tbreak;\n\t\t}\n'
X8='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_SCSIICR_LEN, "PCCTWO_SCSIICR", len);\n\t\t\tbreak;\n\t\t}\n'
X9='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_PSCALEADJ_LEN, "PCCTWO_PSCALEADJ", len);\n\t\t\tbreak;\n\t\t}\n'
say "RESTORE from SEC + REBUILD + verify, THEN clear the sentinel"
mut M_LEN8_VECBASE 'latch all d 11' "a='$X10'; assert s.count(a)==1; s=s.replace(a,a.replace('len != 1','len & 6'))"
mut M_LATCH_ASSIGN 'latch aba 3' "a='d->warned |= (1u << bit);'; assert s.count(a)==1; s=s.replace(a,'d->warned = (1u << bit);')"
mut M_LATCH_BIT0 'latch same2 2' "a='d->warned |= (1u << bit);'; assert s.count(a)==1; s=s.replace(a,'d->warned |= 1;')"
mut M_GROW_IPL 'acc ipl ro 0, acc all 1' "a='$I1'; assert s.count(a)==1; s=s.replace(a,a.replace('len != 1','len != 0'))"
mut M_RET0_GENCTL 'hwr genctl lv died' "a='$G1'; assert s.count(a)==1; s=s.replace(a,a.replace('\t\t\tbreak;\n','\t\t\treturn 0;\n'))"
cp "$SEC/$F" "$T/$F"; cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED -- sentinel KEPT"
build restore; rm -f "$T/.MUTANT"; say "  restored + REBUILT + verified, sentinel cleared"
say "KILLPCC2B_PART4_DONE"
