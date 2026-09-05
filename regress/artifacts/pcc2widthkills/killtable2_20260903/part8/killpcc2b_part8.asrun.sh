#!/bin/bash
#  PART 2, reduced: M_ALIAS_SCCTX / M_LENGT2_MASK / M_FALL_MASK are the builder's M1 / M2 / M6,
#  which its own pass-3 table measures against the SAME instrument (md5 d9239db6).  Only the
#  pre-table block's yield, M_IDATA_GENCTL, is measured here.
#  The four M_FALL_* (odd-arm announce-then-land) are measured by the builder's pass 3b (78-row,
#  the breach) and 3c (82-row md5 cd22f951, the repair) on the SAME instrument; not repeated here.
#  pcc2widthkills pass-2 repair table -- the IPL/MASK rows.  Runs after the panels clear.
#    BASE          190/190 owed
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
G=/mnt/c/DocumentNoSnc/CC/GXEMUL; SEC=$G/GXEMUL-SEC; T=/tmp/gxpcc2b8; F=src/devices/dev_pcc2.c
OUT=/tmp/killpcc2b8; PROBE=pcc2_width_probe.py
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
    MD=$(diff "$SEC/$F" "$T/$F" | grep -c "^[<>]"); say "    [$1] mutant diff vs SEC: $MD lines; first added: $(diff "$SEC/$F" "$T/$F" | grep "^>" | head -1 | cut -c1-100)"; [ "$MD" -gt 0 ] || die "$1: MUTATION NOT APPLIED (source identical to SEC)"
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
say "BASE -- 190/190 owed"; build BASE; score BASE CONTROL
BASE_RES=$(grep -m1 PCC2W_RESULT "$OUT/BASE.out" | cut -d= -f2)
[ "$BASE_RES" = "190/190" ] || die "BASE IS NOT FULL ($BASE_RES): $(grep -m1 PCC2W_RED "$OUT/BASE.out") -- a table on a broken instrument measures nothing (tablebasenotfull)"
X5='pcc2_width_decline(d, PCC2_W_SCCTX_LEN, "PCCTWO_SCCTX", len);'
FN2='DEVICE_ACCESS(pcc2)\n{\n'
FNN2='DEVICE_ACCESS(pcc2)\n{\n\tstatic int ipl_wr = 0;\t/* MUTANT: the IPL read-branch latch hoisted so the guard can read it */\n'
RDECL='\t\t\t\tstatic int w = 0;\t/* #119: was exit(1) */\n\t\t\t\tif (!w) { fatal("[ pcc2: IPL == 0 on read ]\\n");\n\t\t\t\t    w = 1; }\n'
RDECLN='\t\t\t\tif (!ipl_wr) { fatal("[ pcc2: IPL == 0 on read ]\\n");\n\t\t\t\t    ipl_wr = 1; }\n'
IG2='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_IPL_LEN,'
IGN2='\t\tif (len != 1 && writeflag == MEM_WRITE && !ipl_wr) {\n\t\t\tpcc2_width_decline(d, PCC2_W_IPL_LEN,'
TGC='\t\tif (len != 1 && writeflag == MEM_WRITE && !(d->pcctwo_reg[relative_addr] & PCC2_TCTL_COVF)) {\n\t\t\tpcc2_width_decline(d, PCC2_W_TXCTL_LEN,'
TI4='\t\tif (len != 1 && writeflag == MEM_WRITE && !(d->pcctwo_reg[relative_addr] & 0x04)) {\n\t\t\tpcc2_width_decline(d, PCC2_W_TXICR_LEN,'
GX='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_GENCTL_LEN,'
GXN='\t\tif (len != 1 && writeflag == MEM_WRITE && !(d->warned & (1u << PCC2_W_MASK_LEN))) {\n\t\t\tpcc2_width_decline(d, PCC2_W_GENCTL_LEN,'
TGH='\t\tif (len != 1 && writeflag == MEM_WRITE && !(d->pcctwo_reg[relative_addr] & 0xe0)) {\n\t\t\tpcc2_width_decline(d, PCC2_W_TXCTL_LEN,'
TIL='\t\tif (len != 1 && writeflag == MEM_WRITE && d->pending_timer2_interrupts < 2) {\n\t\t\tpcc2_width_decline(d, PCC2_W_TXICR_LEN,'
IG='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_IPL_LEN,'
IGN='\t\tif (len != 1 && writeflag == MEM_WRITE && !ipl_w) {\n\t\t\tpcc2_width_decline(d, PCC2_W_IPL_LEN,'
WDECL='\t\t\tstatic int w = 0;\t/* #119: was exit(1) (IPL is read-only) */\n\t\t\tif (!w) { fatal("[ pcc2: write to read-only PCCTWO_IPL; "\n\t\t\t    "ignored ]\\n"); w = 1; }\n'
WDECLN='\t\t\tif (!ipl_w) { fatal("[ pcc2: write to read-only PCCTWO_IPL; "\n\t\t\t    "ignored ]\\n"); ipl_w = 1; }\n'
FN='DEVICE_ACCESS(pcc2)\n{\n'
FNN='DEVICE_ACCESS(pcc2)\n{\n\tstatic int ipl_w = 0;\t/* MUTANT: the IPL body latch hoisted so the guard can read it */\n'
TG='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_TXCTL_LEN,'
TGN='\t\tif (len != 1 && writeflag == MEM_WRITE && !(d->pcctwo_reg[relative_addr] & PCC2_TCTL_OVF)) {\n\t\t\tpcc2_width_decline(d, PCC2_W_TXCTL_LEN,'
TB='\t\t\tpcc2_width_decline(d, PCC2_W_TXCTL_LEN, "PCCTWO_TxCTL", len);\n\t\t\tbreak;\n'
TBN='\t\t\tpcc2_width_decline(d, PCC2_W_TXCTL_LEN, "PCCTWO_TxCTL", len);\n\t\t\tif (len < 4 || relative_addr == PCCTWO_T2CTL) break;\n'
IB='\t\t\tpcc2_width_decline(d, PCC2_W_TXICR_LEN, "PCCTWO_TxICR", len);\n\t\t\tbreak;\n'
IBN='\t\t\tpcc2_width_decline(d, PCC2_W_TXICR_LEN, "PCCTWO_TxICR", len);\n\t\t\tif (len < 4 || relative_addr == PCCTWO_T2ICR) break;\n'
VB='\t\tif (writeflag == MEM_WRITE) {\n\t\t\td->pcctwo_reg[relative_addr] = idata & 0xf0;\n\t\t\tif (idata & ~0xf0)\n\t\t\t\tfatal("[ pcc2: HUH? write to PCCTWO_VECBASE"\n\t\t\t\t    " with value 0x%02x. ]\\n", (int) idata);\n\t\t}\n'
VBN='\t\td->pcctwo_reg[relative_addr] = idata & 0xf0;\n\t\tif (idata & ~0xf0)\n\t\t\tfatal("[ pcc2: HUH? write to PCCTWO_VECBASE"\n\t\t\t    " with value 0x%02x. ]\\n", (int) idata);\n'
TI='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_TXICR_LEN,'
TI1='\t\tif (len != 1 && writeflag == MEM_WRITE && d->pending_timer1_interrupts == 0) {\n\t\t\tpcc2_width_decline(d, PCC2_W_TXICR_LEN,'
TI2='\t\tif (len != 1 && writeflag == MEM_WRITE && !d->pending_timer2_interrupts) {\n\t\t\tpcc2_width_decline(d, PCC2_W_TXICR_LEN,'
GB='\t\tif (writeflag == MEM_WRITE) {\n\t\t\td->pcctwo_reg[relative_addr] = idata;\n\t\t\treassert_interrupts(d);\n\t\t}\n'
GBN='\t\td->pcctwo_reg[relative_addr] = idata;\n\t\treassert_interrupts(d);\n'
X10='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_VECBASE_LEN, "PCCTWO_VECBASE", len);\n\t\t\tbreak;\n\t\t}\n'
X11='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_PSCALEADJ_LEN, "PCCTWO_PSCALEADJ", len);\n\t\t\tbreak;\n\t\t}\n'
X6='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_SCCICR_LEN, "PCCTWO_SCCICR", len);\n\t\t\tbreak;\n\t\t}\n'
X7='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_SCCRX_LEN, "PCCTWO_SCCRX", len);\n\t\t\tbreak;\n\t\t}\n'
X8='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_SCSIICR_LEN, "PCCTWO_SCSIICR", len);\n\t\t\tbreak;\n\t\t}\n'
X9='\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_PSCALEADJ_LEN, "PCCTWO_PSCALEADJ", len);\n\t\t\tbreak;\n\t\t}\n'
say "RESTORE from SEC + REBUILD + verify, THEN clear the sentinel"
mut M_TXCTL_OVFHI 'ovfhi2 decl 0, ovfhi2 rb 0x80, ovfhi1 decl 0, ovfhi1 rb 0x80' "a='$TG'; assert s.count(a)==1; s=s.replace(a,'$TGH')"
mut M_PEND2_LT2 'pendn2 decl 0, pendn2 rb 0x20' "a='$TI'; assert s.count(a)==1; s=s.replace(a,'$TIL')"
mut M_IDATA_NE0_QUAL 'latch all zero 0, wwr sccerr dcl 0, pend1 decl 0, pend1 rb 0x20' "import re; a=re.compile(r'if \(len != 1 && writeflag == MEM_WRITE\) \{'); assert len(a.findall(s))==12; s=a.sub('if (len != 1 && idata != 0 && writeflag == MEM_WRITE) {', s)"
mut M_W4FALL_ALL '26 red: rb4 x11, rb8 x11 (genctl BY VALUE 0xd9/0x40), noig4/8 x4' "import re; a=re.compile(r'(pcc2_width_decline\(d, PCC2_W_[A-Z0-9_]+, .PCCTWO_[A-Za-z]+., len\);\n\t\t\t)break;'); assert len(a.findall(s))==12; s=a.sub(r'\1if (len < 4) break;', s)"
mut M_TXICR_IL4 'rb t2icr il4 0x10, rb t1icr il4 0x10' "a='$TI'; assert s.count(a)==1; s=s.replace(a,'$TI4')"
mut M_WARNX_GENCTL 'latch all rev 11' "a='$GX'; assert s.count(a)==1; s=s.replace(a,'$GXN')"
mut M_IPLR 'ipl rset 0' "a='$FN2'; assert s.count(a)==1; s=s.replace(a,'$FNN2'); a='$RDECL'; assert s.count(a)==1; s=s.replace(a,'$RDECLN'); a='$IG2'; assert s.count(a)==1; s=s.replace(a,'$IGN2')"
mut M_TXCTL_COVF 'rb t2ctl b27 0xff, rb t1ctl b27 0xff' "a='$TG'; assert s.count(a)==1; s=s.replace(a,'$TGC')"
cp "$SEC/$F" "$T/$F"; cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED -- sentinel KEPT"
build restore; rm -f "$T/.MUTANT"; say "  restored + REBUILT + verified, sentinel cleared"
say "KILLPCC2B_PART8_DONE"
