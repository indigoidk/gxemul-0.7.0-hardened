#!/bin/bash
#  #501 pcc2defaultkill KILL TABLE 3 -- the REPAIRED default: arm and the 36-row detector (pass-2 repair), twelve
#  mutants.  The six pass-2 mutants are scored by BOTH instruments: the 23-row one that shipped at pass 2 (frozen
#  in killtable_20260905/, md5 a96b8bcf) must stay 23/23 on them -- the measured breach -- and the 36-row one must
#  red them.  BASE owes 36/36 AND 23/23 (the old anchors survive the `(len N)' announce).
#    M_EXIT (b) verbatim exit(1) | M_UNLATCH | M_ONELATCH | M_BACKED member 6 | M_RDKILL | M_DIRSWAP   (pass 1)
#    M_WRLATCH  latch SET only on writes (grok A)        M_WIDEKILL  `len != 1' re-kill (grok B)
#    M_OFFKILL  re-kill at unsampled 0x06 (Fable)        M_SRVD0     read announce prints 0 (Opus M_O1, measured)
#    M_BACKED2  member 6 on the latched path (Opus M_O2, measured)    M_ABA  `|=' -> `=' (codex)
set -u
G=/mnt/c/DocumentNoSnc/CC/GXEMUL; SEC=$G/GXEMUL-SEC; F=src/devices/dev_pcc2.c; T=/tmp/gxdk501b
OUT=/tmp/killdk501b; PROBE=pcc2_default_probe.py
OLDK=$SEC/regress/artifacts/pcc2defaultkill/killtable_20260905
say() { echo "[$(date +%H:%M:%S)] $*"; }
die() { echo "*** ABORT: $*"; exit 9; }
rm -rf "$T" "$OUT"; mkdir -p "$OUT/old23"
cp -a "$G/build" "$T" || die "clone failed"
cmp -s "$T/$F" "$SEC/$F" || { cp "$SEC/$F" "$T/$F"; say "  clone's $F refreshed from SEC (the repair; BASE rebuilds it)"; }
grep -q "(len %d)" "$T/$F" || die "the clone's $F lacks the repair"
cp "$SEC/regress/$PROBE" "$OUT/frozen_probe.py" || die "cannot freeze probe"
cp "$SEC/regress/pcc2_width_probe.py" "$OUT/pcc2_width_probe.py" || die "cannot freeze the session helper source"
cp "$OLDK/frozen_probe.py" "$OUT/old23/frozen_probe.py" || die "cannot copy the pass-2 instrument"
cp "$OLDK/pcc2_width_probe.py" "$OUT/old23/pcc2_width_probe.py" || die "cannot copy the pass-2 helper"
[ "$(md5sum "$OUT/old23/frozen_probe.py" | cut -c1-8)" = "a96b8bcf" ] || die "the pass-2 instrument is not a96b8bcf"
say "  instruments frozen: new $(md5sum "$OUT/frozen_probe.py" | cut -c1-8) ($(grep -c '^row(' "$OUT/frozen_probe.py") rows)  old23 a96b8bcf"
build() { cd "$T" || die cd; rm -f src/devices/dev_pcc2.o; make -j4 > "$OUT/build_$1.log" 2>&1; [ "$T/gxemul" -nt "$T/$F" ] || die "$1: binary not newer than source"; }
score() {   # name expect instrument-dir tag
    cd "$SEC/regress" || die cd
    python3 -u "$3/frozen_probe.py" "$T/gxemul" "$1" > "$OUT/$1$4.out" 2>&1
    grep -q PCC2D_PROBE_DONE "$OUT/$1$4.out" || die "$1$4: NO COMPLETION SENTINEL"
    say "  $1$4 [$2]: $(grep -m1 PCC2D_RESULT "$OUT/$1$4.out")"
    grep -m1 PCC2D_RED "$OUT/$1$4.out" | sed 's/PCC2D_RED=/      RED: /' || true
}
mut() {   # name expect body both|new
    echo "$F  mutant $1" > "$T/.MUTANT"; cp "$SEC/$F" "$T/$F"
    python3 - "$T/$F" "$3" <<'PYEOF'
import io, sys
p, body = sys.argv[1], sys.argv[2]; s = io.open(p, encoding='utf-8').read()
ns = {'s': s}; exec(body, ns); io.open(p, 'w', encoding='utf-8', newline='\n').write(ns['s'])
PYEOF
    [ $? -eq 0 ] || die "$1: mutator failed"
    cmp -s "$T/$F" "$SEC/$F" && die "$1: file UNCHANGED after mutation"
    MD=$(diff "$SEC/$F" "$T/$F" | grep -c "^[<>]"); say "    [$1] mutant diff vs SEC: $MD lines; first added: $(diff "$SEC/$F" "$T/$F" | grep "^>" | head -1 | cut -c1-100)"; [ "$MD" -gt 0 ] || die "$1: MUTATION NOT APPLIED"
    build "$1"
    say "    [$1] binary $(date -r "$T/gxemul" +%H:%M:%S)  source $(date -r "$T/$F" +%H:%M:%S)"
    score "$1" "$2" "$OUT" ""
    [ "$4" = both ] && score "$1" "pass-2 instrument: 23/23 owed = the measured breach" "$OUT/old23" ".old23"
}
say "BASE -- 36/36 owed on the repaired instrument, 23/23 on the pass-2 one"; build BASE
score BASE CONTROL "$OUT" ""; score BASE "CONTROL, pass-2 instrument" "$OUT/old23" ".old23"
[ "$(grep -m1 PCC2D_RESULT "$OUT/BASE.out" | cut -d= -f2)" = "36/36" ] || die "BASE IS NOT FULL: $(grep -m1 PCC2D_RED "$OUT/BASE.out") -- a table on a broken instrument measures nothing"
[ "$(grep -m1 PCC2D_RESULT "$OUT/BASE.old23.out" | cut -d= -f2)" = "23/23" ] || die "the pass-2 instrument is NOT full on the repaired product: $(grep -m1 PCC2D_RED "$OUT/BASE.old23.out") -- an old anchor broke"
DKN='\t\tif (!(d->warned_unimpl & (1ULL << relative_addr))) {\n\t\t\td->warned_unimpl |= 1ULL << relative_addr;\n\t\t\tif (writeflag == MEM_WRITE)\n\t\t\t\tfatal("[ pcc2: unimplemented write to offset "\n\t\t\t\t    "0x%x (len %d): 0x%x -- declined.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, (int) idata);\n\t\t\telse\n\t\t\t\t/*  data[0] is the byte actually SERVED; a reload of the\n\t\t\t\t    array here could differ (the tick rewrites the\n\t\t\t\t    counter interiors), and a wide read is labelled.  */\n\t\t\t\tfatal("[ pcc2: unimplemented read from offset "\n\t\t\t\t    "0x%x (len %d) -- served 0x%02x.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, data[0]);\n\t\t}\n\t\tbreak;\n'
DKO='\t\tdebug("[ pcc2: unimplemented %s offset 0x%x",\n\t\t    writeflag == MEM_WRITE? "write to" : "read from",\n\t\t    (int) relative_addr);\n\t\tif (writeflag == MEM_WRITE)\n\t\t\tdebug(": 0x%x", (int)idata);\n\t\tdebug(" ]\\n");\n\t\texit(1);\n'
DKU='\t\tif (1) {\n\t\t\td->warned_unimpl |= 1ULL << relative_addr;\n\t\t\tif (writeflag == MEM_WRITE)\n\t\t\t\tfatal("[ pcc2: unimplemented write to offset "\n\t\t\t\t    "0x%x (len %d): 0x%x -- declined.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, (int) idata);\n\t\t\telse\n\t\t\t\t/*  data[0] is the byte actually SERVED; a reload of the\n\t\t\t\t    array here could differ (the tick rewrites the\n\t\t\t\t    counter interiors), and a wide read is labelled.  */\n\t\t\t\tfatal("[ pcc2: unimplemented read from offset "\n\t\t\t\t    "0x%x (len %d) -- served 0x%02x.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, data[0]);\n\t\t}\n\t\tbreak;\n'
DK1='\t\tif (!(d->warned_unimpl & 1ULL)) {\n\t\t\td->warned_unimpl |= 1ULL;\n\t\t\tif (writeflag == MEM_WRITE)\n\t\t\t\tfatal("[ pcc2: unimplemented write to offset "\n\t\t\t\t    "0x%x (len %d): 0x%x -- declined.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, (int) idata);\n\t\t\telse\n\t\t\t\t/*  data[0] is the byte actually SERVED; a reload of the\n\t\t\t\t    array here could differ (the tick rewrites the\n\t\t\t\t    counter interiors), and a wide read is labelled.  */\n\t\t\t\tfatal("[ pcc2: unimplemented read from offset "\n\t\t\t\t    "0x%x (len %d) -- served 0x%02x.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, data[0]);\n\t\t}\n\t\tbreak;\n'
DKB='\t\tif (writeflag == MEM_WRITE && relative_addr + len <= PCC2_SIZE)\n\t\t\tmemcpy(d->pcctwo_reg + relative_addr, data, len);\n\t\tif (!(d->warned_unimpl & (1ULL << relative_addr))) {\n\t\t\td->warned_unimpl |= 1ULL << relative_addr;\n\t\t\tif (writeflag == MEM_WRITE)\n\t\t\t\tfatal("[ pcc2: unimplemented write to offset "\n\t\t\t\t    "0x%x (len %d): 0x%x -- declined.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, (int) idata);\n\t\t\telse\n\t\t\t\t/*  data[0] is the byte actually SERVED; a reload of the\n\t\t\t\t    array here could differ (the tick rewrites the\n\t\t\t\t    counter interiors), and a wide read is labelled.  */\n\t\t\t\tfatal("[ pcc2: unimplemented read from offset "\n\t\t\t\t    "0x%x (len %d) -- served 0x%02x.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, data[0]);\n\t\t}\n\t\tbreak;\n'
DKR='\t\tif (writeflag == MEM_READ)\n\t\t\texit(1);\n\t\tif (!(d->warned_unimpl & (1ULL << relative_addr))) {\n\t\t\td->warned_unimpl |= 1ULL << relative_addr;\n\t\t\tif (writeflag == MEM_WRITE)\n\t\t\t\tfatal("[ pcc2: unimplemented write to offset "\n\t\t\t\t    "0x%x (len %d): 0x%x -- declined.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, (int) idata);\n\t\t\telse\n\t\t\t\t/*  data[0] is the byte actually SERVED; a reload of the\n\t\t\t\t    array here could differ (the tick rewrites the\n\t\t\t\t    counter interiors), and a wide read is labelled.  */\n\t\t\t\tfatal("[ pcc2: unimplemented read from offset "\n\t\t\t\t    "0x%x (len %d) -- served 0x%02x.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, data[0]);\n\t\t}\n\t\tbreak;\n'
DKS='\t\tif (!(d->warned_unimpl & (1ULL << relative_addr))) {\n\t\t\td->warned_unimpl |= 1ULL << relative_addr;\n\t\t\tif (writeflag != MEM_WRITE)\n\t\t\t\tfatal("[ pcc2: unimplemented write to offset "\n\t\t\t\t    "0x%x (len %d): 0x%x -- declined.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, (int) idata);\n\t\t\telse\n\t\t\t\t/*  data[0] is the byte actually SERVED; a reload of the\n\t\t\t\t    array here could differ (the tick rewrites the\n\t\t\t\t    counter interiors), and a wide read is labelled.  */\n\t\t\t\tfatal("[ pcc2: unimplemented read from offset "\n\t\t\t\t    "0x%x (len %d) -- served 0x%02x.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, data[0]);\n\t\t}\n\t\tbreak;\n'
DKA='\t\tif (!(d->warned_unimpl & (1ULL << relative_addr))) {\n\t\t\tif (writeflag == MEM_WRITE)\n\t\t\t\td->warned_unimpl |= 1ULL << relative_addr;\n\t\t\tif (writeflag == MEM_WRITE)\n\t\t\t\tfatal("[ pcc2: unimplemented write to offset "\n\t\t\t\t    "0x%x (len %d): 0x%x -- declined.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, (int) idata);\n\t\t\telse\n\t\t\t\t/*  data[0] is the byte actually SERVED; a reload of the\n\t\t\t\t    array here could differ (the tick rewrites the\n\t\t\t\t    counter interiors), and a wide read is labelled.  */\n\t\t\t\tfatal("[ pcc2: unimplemented read from offset "\n\t\t\t\t    "0x%x (len %d) -- served 0x%02x.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, data[0]);\n\t\t}\n\t\tbreak;\n'
DKW='\t\tif (len != 1)\n\t\t\texit(1);\n\t\tif (!(d->warned_unimpl & (1ULL << relative_addr))) {\n\t\t\td->warned_unimpl |= 1ULL << relative_addr;\n\t\t\tif (writeflag == MEM_WRITE)\n\t\t\t\tfatal("[ pcc2: unimplemented write to offset "\n\t\t\t\t    "0x%x (len %d): 0x%x -- declined.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, (int) idata);\n\t\t\telse\n\t\t\t\t/*  data[0] is the byte actually SERVED; a reload of the\n\t\t\t\t    array here could differ (the tick rewrites the\n\t\t\t\t    counter interiors), and a wide read is labelled.  */\n\t\t\t\tfatal("[ pcc2: unimplemented read from offset "\n\t\t\t\t    "0x%x (len %d) -- served 0x%02x.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, data[0]);\n\t\t}\n\t\tbreak;\n'
DKF='\t\tif (relative_addr == 0x06)\n\t\t\texit(1);\n\t\tif (!(d->warned_unimpl & (1ULL << relative_addr))) {\n\t\t\td->warned_unimpl |= 1ULL << relative_addr;\n\t\t\tif (writeflag == MEM_WRITE)\n\t\t\t\tfatal("[ pcc2: unimplemented write to offset "\n\t\t\t\t    "0x%x (len %d): 0x%x -- declined.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, (int) idata);\n\t\t\telse\n\t\t\t\t/*  data[0] is the byte actually SERVED; a reload of the\n\t\t\t\t    array here could differ (the tick rewrites the\n\t\t\t\t    counter interiors), and a wide read is labelled.  */\n\t\t\t\tfatal("[ pcc2: unimplemented read from offset "\n\t\t\t\t    "0x%x (len %d) -- served 0x%02x.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, data[0]);\n\t\t}\n\t\tbreak;\n'
DKZ='\t\tif (!(d->warned_unimpl & (1ULL << relative_addr))) {\n\t\t\td->warned_unimpl |= 1ULL << relative_addr;\n\t\t\tif (writeflag == MEM_WRITE)\n\t\t\t\tfatal("[ pcc2: unimplemented write to offset "\n\t\t\t\t    "0x%x (len %d): 0x%x -- declined.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, (int) idata);\n\t\t\telse\n\t\t\t\t/*  data[0] is the byte actually SERVED; a reload of the\n\t\t\t\t    array here could differ (the tick rewrites the\n\t\t\t\t    counter interiors), and a wide read is labelled.  */\n\t\t\t\tfatal("[ pcc2: unimplemented read from offset "\n\t\t\t\t    "0x%x (len %d) -- served 0x%02x.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, 0);\n\t\t}\n\t\tbreak;\n'
DK2='\t\tif (!(d->warned_unimpl & (1ULL << relative_addr))) {\n\t\t\td->warned_unimpl |= 1ULL << relative_addr;\n\t\t\tif (writeflag == MEM_WRITE)\n\t\t\t\tfatal("[ pcc2: unimplemented write to offset "\n\t\t\t\t    "0x%x (len %d): 0x%x -- declined.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, (int) idata);\n\t\t\telse\n\t\t\t\t/*  data[0] is the byte actually SERVED; a reload of the\n\t\t\t\t    array here could differ (the tick rewrites the\n\t\t\t\t    counter interiors), and a wide read is labelled.  */\n\t\t\t\tfatal("[ pcc2: unimplemented read from offset "\n\t\t\t\t    "0x%x (len %d) -- served 0x%02x.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, data[0]);\n\t\t} else if (writeflag == MEM_WRITE)\n\t\t\td->pcctwo_reg[relative_addr] = idata;\n\t\tbreak;\n'
DKE='\t\tif (!(d->warned_unimpl & (1ULL << relative_addr))) {\n\t\t\td->warned_unimpl = 1ULL << relative_addr;\n\t\t\tif (writeflag == MEM_WRITE)\n\t\t\t\tfatal("[ pcc2: unimplemented write to offset "\n\t\t\t\t    "0x%x (len %d): 0x%x -- declined.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, (int) idata);\n\t\t\telse\n\t\t\t\t/*  data[0] is the byte actually SERVED; a reload of the\n\t\t\t\t    array here could differ (the tick rewrites the\n\t\t\t\t    counter interiors), and a wide read is labelled.  */\n\t\t\t\tfatal("[ pcc2: unimplemented read from offset "\n\t\t\t\t    "0x%x (len %d) -- served 0x%02x.  (once) ]\\n",\n\t\t\t\t    (int) relative_addr, (int) len, data[0]);\n\t\t}\n\t\tbreak;\n'
mut M_WRLATCH 'latch rd rd 2, latch rd wr 2 -- the latch SET conditioned on writes (grok A)' "a='$DKN'; assert s.count(a)==1; s=s.replace(a,'$DKA')" both
mut M_WIDEKILL 'wide wr, wide wr msg (n/a), wide rd, wide rd srvd (n/a): host exit1 -- the len-not-1 re-kill (grok B)' "a='$DKN'; assert s.count(a)==1; s=s.replace(a,'$DKW')" both
mut M_OFFKILL 'inword wr, inword rd: host exit1 at 0x06 -- a re-kill at an offset the 23 rows never drove (Fable)' "a='$DKN'; assert s.count(a)==1; s=s.replace(a,'$DKF')" both
mut M_SRVD0 'srvd val text 0 -- the read announce prints 0 (Opus M_O1)' "a='$DKN'; assert s.count(a)==1; s=s.replace(a,'$DKZ')" both
mut M_BACKED2 'sameoff val 0x5a -- member 6 exempting the first write per offset (Opus M_O2)' "a='$DKN'; assert s.count(a)==1; s=s.replace(a,'$DK2')" both
mut M_ABA 'latch aba 3 -- the or-assign made a plain assign forgets earlier bits (codex)' "a='$DKN'; assert s.count(a)==1; s=s.replace(a,'$DKE')" both
mut M_EXIT '29 red: the 16 of pass 2 + the 13 new rows -- every survival/count/value row; live, devsig, sccerr rdawr, genctl, t1cmp, put b x2 stay' "a='$DKN'; assert s.count(a)==1; s=s.replace(a,'$DKO')" new
mut M_UNLATCH 'latch sameoff 2, latch rw one 2, latch rd rd 2, latch rd wr 2, latch aba 3, wide wr msg 2' "a='$DKN'; assert s.count(a)==1; s=s.replace(a,'$DKU')" new
mut M_ONELATCH 'named wr msg 1, named rd msg 1, named rd srvd 1, latch twooff 1, latch aba 1' "a='$DKN'; assert s.count(a)==1; s=s.replace(a,'$DK1')" new
mut M_BACKED 'ieicr rdawr 0x5a, ieerr rdawr 0x5a, sameoff val 0x5a, wide wr 0x5a5a5a5a; sccerr rdawr stays 0x0' "a='$DKN'; assert s.count(a)==1; s=s.replace(a,'$DKB')" new
mut M_RDKILL 'the seven of pass 2 + latch sameoff (its session now reads), sameoff val, latch rd rd, latch rd wr, srvd val x2, wide wr x2, wide rd x2, inword rd, unnamed rd -- nineteen' "a='$DKN'; assert s.count(a)==1; s=s.replace(a,'$DKR')" new
mut M_DIRSWAP 'dir wr text 0, dir rd text 0, named rd srvd 0, srvd val text 0, wide rd srvd 0, wr declined 0' "a='$DKN'; assert s.count(a)==1; s=s.replace(a,'$DKS')" new
say "RESTORE from SEC + REBUILD + verify, THEN clear the sentinel"
cp "$SEC/$F" "$T/$F"; cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED -- sentinel KEPT"
build restore; rm -f "$T/.MUTANT"; say "  restored + REBUILT + verified, sentinel cleared"
say "KILLDK501B_DONE"
