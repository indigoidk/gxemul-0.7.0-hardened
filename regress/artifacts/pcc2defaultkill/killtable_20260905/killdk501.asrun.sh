#!/bin/bash
#  #501 pcc2defaultkill KILL TABLE -- the new default: arm of DEVICE_ACCESS(pcc2), six mutants, the 23-row
#  detector regress/pcc2_default_probe.py (frozen with the width probe it borrows session() from).
#    BASE       23/23 owed (the fix)
#    M_EXIT     (b) verbatim exit(1) reinstated
#    M_UNLATCH  (d) announce unlatched
#    M_ONELATCH (d) one whole-arm latch bit
#    M_BACKED   member 6 (a store into pcctwo_reg[]) substituted
#    M_RDKILL   (d) reads re-killed
#    M_DIRSWAP  (d) the announce's direction test inverted
set -u
G=/mnt/c/DocumentNoSnc/CC/GXEMUL; SEC=$G/GXEMUL-SEC; T=/tmp/gxdk501; F=src/devices/dev_pcc2.c
OUT=/tmp/killdk501; PROBE=pcc2_default_probe.py
say() { echo "[$(date +%H:%M:%S)] $*"; }
die() { echo "*** ABORT: $*"; exit 9; }
rm -rf "$T" "$OUT"; mkdir -p "$OUT"
cp -a "$G/build" "$T" || die "clone failed"
cmp -s "$T/$F" "$SEC/$F" || { cp "$SEC/$F" "$T/$F"; say "  clone's $F refreshed from SEC (comment-only change since build/ was built)"; }
cp "$SEC/regress/$PROBE" "$OUT/frozen_probe.py" || die "cannot freeze probe"
cp "$SEC/regress/pcc2_width_probe.py" "$OUT/pcc2_width_probe.py" || die "cannot freeze the session helper source"
say "  instrument frozen: $(wc -c < "$OUT/frozen_probe.py") bytes"
build() { cd "$T" || die cd; rm -f src/devices/dev_pcc2.o; make -j4 > "$OUT/build_$1.log" 2>&1; [ "$T/gxemul" -nt "$T/$F" ] || die "$1: binary not newer than source"; }
score() {
    cd "$SEC/regress" || die cd
    python3 -u "$OUT/frozen_probe.py" "$T/gxemul" "$1" > "$OUT/$1.out" 2>&1
    grep -q PCC2D_PROBE_DONE "$OUT/$1.out" || die "$1: NO COMPLETION SENTINEL"
    say "  $1 [$2]: $(grep -m1 PCC2D_RESULT "$OUT/$1.out")"
    grep -m1 PCC2D_RED "$OUT/$1.out" | sed 's/PCC2D_RED=/      RED: /' || true
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
say "BASE -- 23/23 owed"; build BASE; score BASE CONTROL
BASE_RES=$(grep -m1 PCC2D_RESULT "$OUT/BASE.out" | cut -d= -f2)
[ "$BASE_RES" = "23/23" ] || die "BASE IS NOT FULL ($BASE_RES): $(grep -m1 PCC2D_RED "$OUT/BASE.out") -- a table on a broken instrument measures nothing (tablebasenotfull)"
say "RESTORE from SEC + REBUILD + verify, THEN clear the sentinel"
DKN='\t\tif (!(d->warned_unimpl & (1ULL << relative_addr))) {\n\t\t\td->warned_unimpl |= 1ULL << relative_addr;\n\t\t\tif (writeflag == MEM_WRITE)\n\t\t\t\tfatal("[ pcc2: unimplemented write to offset "\n\t\t\t\t    "0x%x: 0x%x -- declined.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) idata);\n\t\t\telse\n\t\t\t\tfatal("[ pcc2: unimplemented read from offset "\n\t\t\t\t    "0x%x -- served 0x%02x.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr,\n\t\t\t\t    d->pcctwo_reg[relative_addr]);\n\t\t}\n\t\tbreak;\n'
DKO='\t\tdebug("[ pcc2: unimplemented %s offset 0x%x",\n\t\t    writeflag == MEM_WRITE? "write to" : "read from",\n\t\t    (int) relative_addr);\n\t\tif (writeflag == MEM_WRITE)\n\t\t\tdebug(": 0x%x", (int)idata);\n\t\tdebug(" ]\\n");\n\t\texit(1);\n'
DKU='\t\tif (1) {\n\t\t\td->warned_unimpl |= 1ULL << relative_addr;\n\t\t\tif (writeflag == MEM_WRITE)\n\t\t\t\tfatal("[ pcc2: unimplemented write to offset "\n\t\t\t\t    "0x%x: 0x%x -- declined.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) idata);\n\t\t\telse\n\t\t\t\tfatal("[ pcc2: unimplemented read from offset "\n\t\t\t\t    "0x%x -- served 0x%02x.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr,\n\t\t\t\t    d->pcctwo_reg[relative_addr]);\n\t\t}\n\t\tbreak;\n'
DK1='\t\tif (!(d->warned_unimpl & 1ULL)) {\n\t\t\td->warned_unimpl |= 1ULL;\n\t\t\tif (writeflag == MEM_WRITE)\n\t\t\t\tfatal("[ pcc2: unimplemented write to offset "\n\t\t\t\t    "0x%x: 0x%x -- declined.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) idata);\n\t\t\telse\n\t\t\t\tfatal("[ pcc2: unimplemented read from offset "\n\t\t\t\t    "0x%x -- served 0x%02x.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr,\n\t\t\t\t    d->pcctwo_reg[relative_addr]);\n\t\t}\n\t\tbreak;\n'
DKB='\t\tif (writeflag == MEM_WRITE && relative_addr + len <= PCC2_SIZE)\n\t\t\tmemcpy(d->pcctwo_reg + relative_addr, data, len);\n\t\tif (!(d->warned_unimpl & (1ULL << relative_addr))) {\n\t\t\td->warned_unimpl |= 1ULL << relative_addr;\n\t\t\tif (writeflag == MEM_WRITE)\n\t\t\t\tfatal("[ pcc2: unimplemented write to offset "\n\t\t\t\t    "0x%x: 0x%x -- declined.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) idata);\n\t\t\telse\n\t\t\t\tfatal("[ pcc2: unimplemented read from offset "\n\t\t\t\t    "0x%x -- served 0x%02x.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr,\n\t\t\t\t    d->pcctwo_reg[relative_addr]);\n\t\t}\n\t\tbreak;\n'
DKR='\t\tif (writeflag == MEM_READ)\n\t\t\texit(1);\n\t\tif (!(d->warned_unimpl & (1ULL << relative_addr))) {\n\t\t\td->warned_unimpl |= 1ULL << relative_addr;\n\t\t\tif (writeflag == MEM_WRITE)\n\t\t\t\tfatal("[ pcc2: unimplemented write to offset "\n\t\t\t\t    "0x%x: 0x%x -- declined.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) idata);\n\t\t\telse\n\t\t\t\tfatal("[ pcc2: unimplemented read from offset "\n\t\t\t\t    "0x%x -- served 0x%02x.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr,\n\t\t\t\t    d->pcctwo_reg[relative_addr]);\n\t\t}\n\t\tbreak;\n'
DKS='\t\tif (!(d->warned_unimpl & (1ULL << relative_addr))) {\n\t\t\td->warned_unimpl |= 1ULL << relative_addr;\n\t\t\tif (writeflag != MEM_WRITE)\n\t\t\t\tfatal("[ pcc2: unimplemented write to offset "\n\t\t\t\t    "0x%x: 0x%x -- declined.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) idata);\n\t\t\telse\n\t\t\t\tfatal("[ pcc2: unimplemented read from offset "\n\t\t\t\t    "0x%x -- served 0x%02x.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr,\n\t\t\t\t    d->pcctwo_reg[relative_addr]);\n\t\t}\n\t\tbreak;\n'
mut M_EXIT 'every survival row red (host exit1): named wr/rd, inword wr, unnamed wr, alias 0x6a, both rdawr rows; genctl/t1cmp/put b/live/devsig stay -- (b) verbatim reinstatement' "a='$DKN'; assert s.count(a)==1; s=s.replace(a,'$DKO')"
mut M_UNLATCH 'latch sameoff 2, latch rw one 2 -- the announce fires on every access' "a='$DKN'; assert s.count(a)==1; s=s.replace(a,'$DKU')"
mut M_ONELATCH 'named wr msg 1, named rd msg 1, named rd srvd 1, latch twooff 1 -- a single whole-arm latch bit' "a='$DKN'; assert s.count(a)==1; s=s.replace(a,'$DK1')"
mut M_BACKED 'ieicr rdawr 0x5a, ieerr rdawr 0x5a; sccerr rdawr stays 0x0 (the control) -- member 6 substituted for member 3' "a='$DKN'; assert s.count(a)==1; s=s.replace(a,'$DKB')"
mut M_RDKILL 'named rd host exit1 (+ rd msg/srvd n/a), dir rd text n/a -- a writeflag guard that re-kills READS' "a='$DKN'; assert s.count(a)==1; s=s.replace(a,'$DKR')"
mut M_DIRSWAP 'dir wr text 0, dir rd text 0, named rd srvd 0 -- the direction test inverted in the announce' "a='$DKN'; assert s.count(a)==1; s=s.replace(a,'$DKS')"
cp "$SEC/$F" "$T/$F"; cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED -- sentinel KEPT"
build restore; rm -f "$T/.MUTANT"; say "  restored + REBUILT + verified, sentinel cleared"
say "KILLDK501_DONE"
