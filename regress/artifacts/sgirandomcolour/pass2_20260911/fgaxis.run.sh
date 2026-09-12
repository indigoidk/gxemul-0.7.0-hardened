#!/bin/bash
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
OUT=$SEC/regress/artifacts/sgirandomcolour/pass2_20260911
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/p2
CLONE=/tmp/gxop519p2
SRC=$CLONE/src/devices/dev_sgi_re.c
BL=$OUT/BASELINE_FIX519_P2.c
cp "$SP/ctrl519p2_fg.py" "$OUT/ctrl519p2_fg.P2FROZEN.py"
exec > >(tee -a "$OUT/FGAXIS.out") 2>&1
echo "=== M37 discriminating run $(date) ==="
printf '%s\n' "src/devices/dev_sgi_re.c -- #519 PASS-2 fg-axis discriminator (Opus)" \
  "RESTORE FROM: $BL" "written $(date)" > "$CLONE/.MUTANT"
build () {
    rm -f "$CLONE/src/devices/dev_sgi_re.o" "$CLONE/gxemul"
    ( cd "$CLONE" && make -j4 ) > "$OUT/build_fg_$1.log" 2>&1
    if [ -x "$CLONE/gxemul" ] && [ "$CLONE/gxemul" -nt "$SRC" ]; then echo "  build $1: FRESH"; return 0; fi
    echo "  build $1: *** STALE/FAILED ***"; return 1
}
echo "--- leg BASE (the fix) ---"
cp "$BL" "$SRC"
build BASE && python3 -u "$OUT/ctrl519p2_fg.P2FROZEN.py" "$CLONE/gxemul" BASE > "$OUT/BASE.fgctrl" 2>&1
tail -8 "$OUT/BASE.fgctrl"
echo "--- leg M37_fgvalue ---"
cp "$BL" "$SRC"
python3 "$OUT/mut519p2b.P2FROZEN.py" "$SRC" M37_fgvalue || { echo "MUTATE FAILED"; exit 1; }
build M37 && python3 -u "$OUT/ctrl519p2_fg.P2FROZEN.py" "$CLONE/gxemul" M37_fgvalue > "$OUT/M37_fgvalue.fgctrl" 2>&1
tail -8 "$OUT/M37_fgvalue.fgctrl"
echo "=== RESTORE + two-part clearance ==="
cp "$BL" "$SRC"
rm -f "$CLONE/src/devices/dev_sgi_re.o" "$CLONE/gxemul"
( cd "$CLONE" && make -j4 ) > "$OUT/build_fg_RESTORE.log" 2>&1
if cmp -s "$SRC" "$SEC/src/devices/dev_sgi_re.c"; then P1=CLEAN; else P1="*** DIFFERS ***"; fi
if [ -x "$CLONE/gxemul" ] && [ "$CLONE/gxemul" -nt "$SRC" ]; then P2=FRESH; else P2="*** STALE ***"; fi
echo "PART1 clone source vs SEC:        $P1"
echo "PART2 [ gxemul -nt dev_sgi_re.c ]: $P2"
if [ "$P1" = "CLEAN" ] && [ "$P2" = "FRESH" ]; then rm -f "$CLONE/.MUTANT"; echo "sentinel CLEARED"; else echo "*** SENTINEL LEFT IN PLACE ***"; fi
echo "sentinels: $(tail -1 "$OUT/BASE.fgctrl") / $(tail -1 "$OUT/M37_fgvalue.fgctrl")"
echo "FGAXIS_DONE"
