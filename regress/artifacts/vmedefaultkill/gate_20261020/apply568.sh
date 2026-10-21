#!/bin/bash
#  apply568.sh -- #568 (vmedefaultkill): test-first at GATE level, then propagate, rebuild, clear, and re-gate.
#
#  0. the probe goes into SEC/regress/ (a new file) and the gate block into a block-only mini gate; the mini gate
#     runs against a PRESERVED COPY of build/gxemul as it is now (its dev_vme.c is HEAD's): the vme rows must RED;
#  1. the fix is copied into all five trees (SEC, est, build, build-asan, /tmp/gxsec-build) -- refused unless every
#     tree's dev_vme.c is HEAD's first;
#  2. build/, build-asan/ and /tmp/gxsec-build are rebuilt (rm src/cpus/*.o first, the carrier's precaution);
#  3. the TWO-PART CLEARANCE is RUN and its output recorded (est/: source tree, part 2 N/A);
#  4. the mini gate on the rebuilt build/gxemul must PASS;
#  5. the block is inserted into gate_arm.sh after the mk48 block (python, anchor count == 1);
#  then STOP -- the full gate 14 is run separately, alone.
set -u
P=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$P/GXEMUL-SEC
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/vme
A=$S/apply
FIX=$S/fix/dev_vme.fix568.c
PROBE=$S/killtable1/vme_default_probe.frozen.py
BLOCK=$S/gate/gate14_block568.sh
HEADMD5=2516a82bc777fe780f2dc6ccc00fd6c3
FIXMD5=4e3e7fc220062b429f7d9d6e140fec9e
PROBEMD5=19de15b3ea69af28e437cdf92e22c97e
TREES="$SEC $P/est $P/build $P/build-asan /tmp/gxsec-build"
m5() { md5sum < "$1" | cut -c1-32; }
say() { echo "$(date '+%F %T') $*"; }

[ "$(m5 "$FIX")" = "$FIXMD5" ] || { say "REFUSED: fix md5 $(m5 "$FIX")"; exit 3; }
[ "$(m5 "$PROBE")" = "$PROBEMD5" ] || { say "REFUSED: probe md5 $(m5 "$PROBE")"; exit 3; }
for t in $TREES; do
    m=$(m5 "$t/src/devices/dev_vme.c")
    [ "$m" = "$HEADMD5" ] || { say "REFUSED: $t dev_vme.c is $m, not HEAD's"; exit 3; }
done
[ -e "$SEC/regress/vme_default_probe.py" ] && { say "REFUSED: regress/vme_default_probe.py already exists"; exit 3; }
grep -q 'vme_default_probe' "$SEC/regress/gate_arm.sh" && { say "REFUSED: gate_arm.sh already wired"; exit 3; }

#  ---- 0. the mini gate (block only), and the pre-fix binary preserved
cp "$PROBE" "$SEC/regress/vme_default_probe.py" && chmod +x "$SEC/regress/vme_default_probe.py"
say "probe installed $(m5 "$SEC/regress/vme_default_probe.py")"
MINI=$A/gate14_vme_only.sh
{
    echo '#!/bin/bash'
    echo '#  gate14_vme_only.sh -- gate 14'"'"'s #568 block alone (test-first at gate level).  PMAX and LOGDIR from the env.'
    echo 'set -u'
    echo 'cd /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress'
    echo '. ./lib.sh'
    echo 'gate_begin "gate 14 (#568 vme block only)"'
    echo 'PMAX=${PMAX:?}'
    echo 'need_exec "$PMAX"'
    echo 'note "binary : $PMAX"'
    cat "$BLOCK"
    echo 'gate_end'
} > "$MINI"
chmod +x "$MINI"
cp "$P/build/gxemul" "$A/gxemul.prefix568"
say "pre-fix binary preserved: $(m5 "$A/gxemul.prefix568") (build/gxemul, mtime $(stat -c %y "$P/build/gxemul"))"
mkdir -p /tmp/gx568pre && rm -rf /tmp/gx568pre/*
PMAX=$A/gxemul.prefix568 LOGDIR=/tmp/gx568pre bash "$MINI" > "$A/mini_PREFIX.out" 2>&1
say "MINI PRE-FIX rc=$? (want non-zero): $(grep -cE '^ *FAIL' "$A/mini_PREFIX.out") FAIL lines; tail: $(tail -1 "$A/mini_PREFIX.out")"
cp /tmp/gx568pre/vme_default.log "$A/vme_default_PREFIX.log" 2>/dev/null

#  ---- 1. propagate
for t in $TREES; do cp "$FIX" "$t/src/devices/dev_vme.c"; done
for t in $TREES; do say "propagated $t -> $(m5 "$t/src/devices/dev_vme.c")"; done

#  ---- 2. rebuild the three build trees
build() {
    local t=$1 n s rc
    n=$(echo "$t" | tr '/' '_')
    cd "$t" || { say "BUILD $t: no tree"; return; }
    rm -f src/cpus/*.o
    s=$(date +%s)
    make -j4 > "$A/make$n.log" 2>&1; rc=$?
    say "BUILD $t make_rc=$rc secs=$(( $(date +%s) - s )) gxemul=$(m5 "$t/gxemul") warnings=$(grep -c 'warning:' "$A/make$n.log")"
}
build "$P/build"
build "$P/build-asan"
build /tmp/gxsec-build

#  ---- 3. the two-part clearance, RUN (its output is the record)
say "TWO-PART CLEARANCE (dev_vme.c, the round's only src edit):"
for t in "$P/build" "$P/build-asan" /tmp/gxsec-build "$P/est"; do
    if cmp -s "$t/src/devices/dev_vme.c" "$SEC/src/devices/dev_vme.c"; then p1=CLEAN; else p1=DIFFERS; fi
    if [ "$t" = "$P/est" ]; then p2="N/A (source tree, no binary)"
    elif [ "$t/gxemul" -nt "$t/src/devices/dev_vme.c" ]; then p2="binary NEWER than source"
    else p2="*** binary NOT newer than source ***"; fi
    say "  $t: part 1 $p1; part 2 $p2"
done

#  ---- 4. the mini gate on the rebuilt build/gxemul
mkdir -p /tmp/gx568post && rm -rf /tmp/gx568post/*
PMAX=$P/build/gxemul LOGDIR=/tmp/gx568post bash "$MINI" > "$A/mini_FIX.out" 2>&1
say "MINI FIX rc=$? (want 0): $(grep -cE '^ *FAIL' "$A/mini_FIX.out") FAIL lines; tail: $(tail -1 "$A/mini_FIX.out")"
cp /tmp/gx568post/vme_default.log "$A/vme_default_FIX.log" 2>/dev/null

#  ---- 5. wire the block into gate_arm.sh
python3 - "$SEC/regress/gate_arm.sh" "$BLOCK" <<'PYEOF'
import io, sys
p, b = sys.argv[1], io.open(sys.argv[2], encoding="utf-8").read()
s = io.open(p, encoding="utf-8", newline="").read()
anchor = '    check "mk48 nvram rows red"     "$(count "$MK48LOG" " FAIL$")" "0"\nfi\n'
assert "\r\n" not in s, "CRLF gate file"
assert s.count(anchor) == 1, "anchor count %d" % s.count(anchor)
assert "vme_default_probe.py" not in s
s = s.replace(anchor, anchor + "\n\n" + b.rstrip("\n") + "\n", 1)
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("gate_arm.sh wired")
PYEOF
say "gate_arm.sh: $(grep -c 'vme default' "$SEC/regress/gate_arm.sh") 'vme default' lines; bash -n rc=$(bash -n "$SEC/regress/gate_arm.sh"; echo $?)"
say "APPLY568_DONE"
