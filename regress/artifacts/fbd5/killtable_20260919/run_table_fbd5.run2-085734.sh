#!/bin/bash
# fbdeclinefive (#545) -- witness, fix, kill table and restore, ALL in a scratch clone of build/ (never a project tree).
#   MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/fbd5/impl/run_table_fbd5.sh
# Order (PRETABLE.out already written -- its mtime precedes this run's logs):
#   1 clone build/ -> /tmp/gxfbd5; name the baseline; cmp the file-to-be-mutated against SEC HEAD; sentinel
#   2 HEAD build -> the PRE-FIX RED: patched probes (sites S arm dies; drain/witness H legs green but their device rows
#     unaffected) and the patched differential dying at P1
#   3 apply the fix; FIX build -> everything green (the post-fix witness)
#   4 M1..M11 product mutants: one edit each on the FIXED source, rebuild, sites probe + differential
#   5 M12/M14 harness mutants on the FIX binary (probe copies edited)
#   6 restore from SEC HEAD, rebuild, two-part clearance, clear sentinel
set -u
ROOT=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$ROOT/GXEMUL-SEC
IMPL=$ROOT/_scratchpad/fbd5/impl
CLONE=/tmp/gxfbd5
OUT=$CLONE/out
STAMP=$(date +%Y%m%d_%H%M%S)
echo "FBD5_TABLE_START $STAMP"

# ---------------------------------------------------------------- 1 clone + baseline
rm -rf "$CLONE"
cp -a "$ROOT/build" "$CLONE" || { echo "CLONE FAILED"; exit 2; }
mkdir -p "$OUT" "$CLONE/probes"
cd "$CLONE" || exit 2
git -C "$SEC" show HEAD:src/devices/dev_footbridge.c > "$OUT/dev_footbridge.HEAD.c"
if cmp -s src/devices/dev_footbridge.c "$OUT/dev_footbridge.HEAD.c"; then echo "BASELINE dev_footbridge.c == SEC HEAD ($(git -C "$SEC" rev-parse --short HEAD))"; else echo "BASELINE MISMATCH: build/ dev_footbridge.c != SEC HEAD -- STOP"; exit 3; fi
for f in footbridge_sites_probe.py fbpending_drain_probe.py fbpending_witness.py diff_footbridge.c; do
    git -C "$SEC" show HEAD:regress/$f > "$CLONE/probes/$f"
done
cp "$CLONE/probes/"* "$CLONE/regress/" 2>/dev/null
mkdir -p "$CLONE/regress"; for f in footbridge_sites_probe.py fbpending_drain_probe.py fbpending_witness.py diff_footbridge.c; do cp "$CLONE/probes/$f" "$CLONE/regress/$f"; done
python3 "$IMPL/patch_sites_fbd5.py" "$CLONE"   > "$OUT/patch_probes.log" 2>&1 || { echo "sites patch FAILED"; cat "$OUT/patch_probes.log"; exit 3; }
python3 "$IMPL/patch_pending_fbd5.py" "$CLONE" >> "$OUT/patch_probes.log" 2>&1 || { echo "pending patch FAILED"; cat "$OUT/patch_probes.log"; exit 3; }
python3 "$IMPL/patch_diff_fbd5.py" "$CLONE"    >> "$OUT/patch_probes.log" 2>&1 || { echo "diff patch FAILED"; cat "$OUT/patch_probes.log"; exit 3; }
mkdir -p "$CLONE/frozen"; cp "$CLONE/regress/footbridge_sites_probe.py" "$CLONE/regress/fbpending_drain_probe.py" \
      "$CLONE/regress/fbpending_witness.py" "$CLONE/regress/diff_footbridge.c" "$CLONE/frozen/"   # FROZEN instruments
printf '\0\0\0\0' > "$OUT/stub.bin"
echo "fbd5 table $STAMP -- dev_footbridge.c mutated; restore from SEC HEAD, rebuild, cmp" > "$CLONE/.MUTANT"

build() {   # build <tag> -> out/gxemul_<tag>; prints BUILD_<tag> rc and freshness
    rm -f src/devices/dev_footbridge.o gxemul
    make -j4 > "$OUT/build_$1.log" 2>&1; rc=$?
    if [ -x gxemul ] && [ gxemul -nt src/devices/dev_footbridge.c ]; then fresh=FRESH; else fresh=STALE; fi
    cp gxemul "$OUT/gxemul_$1" 2>/dev/null
    echo "BUILD_$1 rc=$rc $fresh $(md5sum gxemul | cut -c1-8)"
    [ "$fresh" = FRESH ] || { echo "BUILD $1 NOT FRESH -- STOP"; exit 4; }
}
runsites() {  # runsites <tag> <binary>
    python3 -u "$CLONE/frozen/footbridge_sites_probe.py" "$2" "$OUT/stub.bin" > "$OUT/sites_$1.log" 2>&1
    echo "SITES_$1 $(grep -E '^ROWS=|^FOOTBRIDGE_SITES_(PASS|FAIL)|^FOOTBRIDGE_SITES_CONTROL' "$OUT/sites_$1.log" | tr '\n' ' ')  red: $(grep -E ' FAIL$' "$OUT/sites_$1.log" | awk '{print $1}' | tr '\n' ',')"
}
rundiff() {   # rundiff <tag>  (compiles the frozen differential against THIS clone's device source)
    ( cd "$CLONE/frozen" && gcc -O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections -Wl,--gc-sections \
        -I"$CLONE/src" -I"$CLONE/src/include" -I"$CLONE/src/include/thirdparty" -I"$CLONE/regress" \
        -o "$OUT/diff_$1" ./diff_footbridge.c -lm > "$OUT/diffc_$1.log" 2>&1 ) ; crc=$?
    if [ $crc -ne 0 ]; then echo "DIFF_$1 COMPILE rc=$crc"; return; fi
    "$OUT/diff_$1" > "$OUT/diff_$1.log" 2>&1; rrc=$?
    echo "DIFF_$1 rc=$rrc $(grep -E 'rows, |DIFF_FOOTBRIDGE_' "$OUT/diff_$1.log" | tr '\n' ' ') red: $(grep -E '^  FAIL  [^@]' "$OUT/diff_$1.log" | cut -c9-60 | tr '\n' '|' | cut -c1-200)"
}

# ---------------------------------------------------------------- 2 HEAD: the pre-fix red
build HEAD
runsites HEAD "$OUT/gxemul_HEAD"
rundiff HEAD
python3 -u "$CLONE/frozen/fbpending_witness.py" "$OUT/gxemul_HEAD" "$OUT/stub.bin" > "$OUT/witness_HEAD.log" 2>&1; echo "WITNESS_HEAD rc=$? $(grep -E '^  (ok|FAIL) +(H1|H2|R0)' "$OUT/witness_HEAD.log" | awk '{print $1":"$2}' | tr '\n' ' ') $(grep -E 'VERDICT' "$OUT/witness_HEAD.log" | tail -1)"

# ---------------------------------------------------------------- 3 FIX
python3 "$IMPL/patch_fbd5.py" "$CLONE" > "$OUT/patch_fix.log" 2>&1 || { echo "FIX PATCH FAILED"; cat "$OUT/patch_fix.log"; exit 5; }
cp src/devices/dev_footbridge.c "$OUT/dev_footbridge.FIX.c"
build FIX
runsites FIX "$OUT/gxemul_FIX"
rundiff FIX
python3 -u "$CLONE/frozen/fbpending_witness.py" "$OUT/gxemul_FIX" "$OUT/stub.bin" > "$OUT/witness_FIX.log" 2>&1; echo "WITNESS_FIX rc=$? $(grep -E '^  (ok|FAIL) +(H1|H2|R0)' "$OUT/witness_FIX.log" | awk '{print $1":"$2}' | tr '\n' ' ') $(grep -E 'VERDICT' "$OUT/witness_FIX.log" | tail -1)"
python3 -u "$CLONE/frozen/fbpending_drain_probe.py" "$OUT/gxemul_FIX" "$OUT/stub.bin" > "$OUT/drain_FIX.log" 2>&1; echo "DRAIN_FIX rc=$? $(grep -E '^  (ok|FAIL) +(H1|H2|R0)' "$OUT/drain_FIX.log" | awk '{print $1":"$2}' | tr '\n' ' ') $(grep -E 'FBDRAIN_VERDICT' "$OUT/drain_FIX.log" | tail -1)"

# ---------------------------------------------------------------- 4 product mutants
for M in M1 M2 M3 M4 M5 M6 M7 M8 M9 M10 M11; do
    cp "$OUT/dev_footbridge.FIX.c" src/devices/dev_footbridge.c
    python3 "$IMPL/mkmut_fbd5.py" "$CLONE" $M > "$OUT/mut_$M.log" 2>&1 || { echo "$M DID NOT APPLY"; cat "$OUT/mut_$M.log"; continue; }
    build $M
    runsites $M "$OUT/gxemul_$M"
    rundiff $M
done

# ---------------------------------------------------------------- 5 harness mutants on the FIX binary
cp "$OUT/dev_footbridge.FIX.c" src/devices/dev_footbridge.c
python3 "$IMPL/hmut_fbd5.py" "$CLONE/frozen/footbridge_sites_probe.py" "$OUT/sites_M12.py" M12
python3 -u "$OUT/sites_M12.py" "$OUT/gxemul_FIX" "$OUT/stub.bin" > "$OUT/sites_M12.log" 2>&1
echo "SITES_M12(quitless) $(grep -E '^ROWS=|^FOOTBRIDGE_SITES_(PASS|FAIL)' "$OUT/sites_M12.log" | tr '
' ' ') red: $(grep -E ' FAIL$' "$OUT/sites_M12.log" | awk '{print $1}' | tr '
' ',')"
python3 "$IMPL/hmut_fbd5.py" "$CLONE/frozen/footbridge_sites_probe.py" "$OUT/sites_M14.py" M14
python3 -u "$OUT/sites_M14.py" "$OUT/gxemul_FIX" "$OUT/stub.bin" > "$OUT/sites_M14.log" 2>&1
echo "SITES_M14(anyexit, -M notanumber) H1: $(grep -E '^H1 ' "$OUT/sites_M14.log")"
python3 "$IMPL/hmut_fbd5.py" "$CLONE/frozen/footbridge_sites_probe.py" "$OUT/sites_M14ctl.py" M14ctl
python3 -u "$OUT/sites_M14ctl.py" "$OUT/gxemul_FIX" "$OUT/stub.bin" > "$OUT/sites_M14ctl.log" 2>&1
echo "SITES_M14ctl(shipped predicate, -M notanumber) H1: $(grep -E '^H1 ' "$OUT/sites_M14ctl.log")"

# ---------------------------------------------------------------- 6 restore + clearance
cp "$OUT/dev_footbridge.HEAD.c" src/devices/dev_footbridge.c
build RESTORED
if cmp -s src/devices/dev_footbridge.c "$OUT/dev_footbridge.HEAD.c" && [ gxemul -nt src/devices/dev_footbridge.c ]; then
    rm -f "$CLONE/.MUTANT"; echo "RESTORE OK: source == SEC HEAD, binary fresh, sentinel cleared"
else
    echo "RESTORE INCOMPLETE -- sentinel LEFT IN PLACE"
fi
echo "FBD5_TABLE_DONE $(date +%Y%m%d_%H%M%S)"
