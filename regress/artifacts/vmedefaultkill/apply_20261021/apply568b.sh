#!/bin/bash
#  apply568b.sh -- #568 REPAIR 1 into the trees: fix568b into all five trees (each must hold fix568 first), probe rev 3
#  into SEC/regress (must hold rev 2 first), gate 14's vme block rewritten for 38 rows with a score-claims pin, the three
#  build trees rebuilt, and the two-part clearance RUN.  NO emulator run here: the mini gate waits for a quiet host.
set -u
P=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$P/GXEMUL-SEC
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/vme
A=$S/apply
FIXB=$S/rev3/dev_vme.fix568b.c
PROBE3=$S/rev3/vme_default_probe.rev3.frozen.py
BLOCK=$A/gate14_block568b.sh
OLDMD5=4e3e7fc220062b429f7d9d6e140fec9e
NEWMD5=beb120eae1be112b682bd528f103191c
P2MD5=19de15b3ea69af28e437cdf92e22c97e
P3MD5=ddcebfe3257d3370f3c16b0bee79a4be
TREES="$SEC $P/est $P/build $P/build-asan /tmp/gxsec-build"
m5() { md5sum < "$1" | cut -c1-32; }
say() { echo "$(date '+%F %T') $*"; }

[ "$(m5 "$FIXB")" = "$NEWMD5" ] || { say "REFUSED: fix568b md5 $(m5 "$FIXB")"; exit 3; }
[ "$(m5 "$PROBE3")" = "$P3MD5" ] || { say "REFUSED: rev 3 md5 $(m5 "$PROBE3")"; exit 3; }
[ "$(m5 "$SEC/regress/vme_default_probe.py")" = "$P2MD5" ] || { say "REFUSED: regress probe is not rev 2"; exit 3; }
for t in $TREES; do
    m=$(m5 "$t/src/devices/dev_vme.c")
    [ "$m" = "$OLDMD5" ] || { say "REFUSED: $t dev_vme.c is $m, not fix568"; exit 3; }
done
grep -q 'check "vme default rows red"' "$SEC/regress/gate_arm.sh" || { say "REFUSED: gate_arm.sh lacks the rev-2 block"; exit 3; }

for t in $TREES; do cp "$FIXB" "$t/src/devices/dev_vme.c"; say "propagated $t -> $(m5 "$t/src/devices/dev_vme.c")"; done
cp "$PROBE3" "$SEC/regress/vme_default_probe.py" && chmod +x "$SEC/regress/vme_default_probe.py"
say "probe rev 3 installed $(m5 "$SEC/regress/vme_default_probe.py")"

python3 - "$SEC/regress/gate_arm.sh" "$BLOCK" <<'PYEOF'
import io, sys
p, b = sys.argv[1], io.open(sys.argv[2], encoding="utf-8").read().rstrip("\n") + "\n"
s = io.open(p, encoding="utf-8", newline="").read()
a = s.index("#  ------------------------------------------------------------ vmedefaultkill (#568)")
end_mark = '    check "vme default rows red"     "$(count "$VMEDLOG" " FAIL$")" "0"\nfi\n'
assert s.count(end_mark) == 1, "rev-2 block end count %d" % s.count(end_mark)
e = s.index(end_mark) + len(end_mark)
assert a < e and s.count("vmedefaultkill (#568)") == 1
s = s[:a] + b + s[e:]
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("gate_arm.sh vme block replaced (rev 3, 38 rows)")
PYEOF
say "gate_arm.sh: bash -n rc=$(bash -n "$SEC/regress/gate_arm.sh"; echo $?); 'vme_default rows run' lines: $(grep -c 'vme_default rows run' "$SEC/regress/gate_arm.sh")"

build() {
    local t=$1 n s rc
    n=$(echo "$t" | tr '/' '_')
    cd "$t" || { say "BUILD $t: no tree"; return; }
    rm -f src/cpus/*.o
    s=$(date +%s)
    make -j4 > "$A/make568b$n.log" 2>&1; rc=$?
    say "BUILD $t make_rc=$rc secs=$(( $(date +%s) - s )) gxemul=$(m5 "$t/gxemul") warnings=$(grep -c 'warning:' "$A/make568b$n.log")"
}
build "$P/build"
build "$P/build-asan"
build /tmp/gxsec-build

say "TWO-PART CLEARANCE (dev_vme.c, the round's only src edit):"
for t in "$P/build" "$P/build-asan" /tmp/gxsec-build "$P/est"; do
    if cmp -s "$t/src/devices/dev_vme.c" "$SEC/src/devices/dev_vme.c"; then p1=CLEAN; else p1=DIFFERS; fi
    if [ "$t" = "$P/est" ]; then p2="N/A (source tree, no binary)"
    elif [ "$t/gxemul" -nt "$t/src/devices/dev_vme.c" ]; then p2="binary NEWER than source"
    else p2="*** binary NOT newer than source ***"; fi
    say "  $t: part 1 $p1; part 2 $p2"
done
say "APPLY568B_DONE"
