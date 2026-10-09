#!/bin/bash
# opus5 late seat: is the #495 defect visible OFFLINE?  HEAD with the write-arm guard
# nulled, measured two ways:
#   (a) the shipped 128-row offline detector (regress/diff_wdc_identify.c, unmodified)
#   (b) my rung-1 directed sequences (D1 = one mid-chunk data-port write)
set -u
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opuswdc
T=/tmp/gxopuswdc
OUT=$S/fuzz_opus
# (a)
D=$T/m_HEAD_no495
rm -rf "$D"; mkdir -p "$D"
cp -a "$T/t_HEAD/src" "$T/t_HEAD/regress" "$T/t_HEAD/config.h" "$D/"
python3 "$S/no495.py" "$D/src/devices/dev_wdc.c" > "$OUT/no495.a.out" 2>&1 || { cat "$OUT/no495.a.out"; exit 3; }
diff "$T/t_HEAD/src/devices/dev_wdc.c" "$D/src/devices/dev_wdc.c" >> "$OUT/no495.a.out"
( cd "$D/regress" && gcc -O2 -std=c99 -I../src/include -I../src/include/thirdparty \
    -ffunction-sections -fdata-sections -Wl,--gc-sections -o mut diff_wdc_identify.c && ./mut ) \
    > "$D/run.out" 2>&1
echo "(a) shipped offline detector vs HEAD-minus-#495: $(grep -E '^[0-9]+ rows' "$D/run.out") $(grep -cE 'WDC_IDENTIFY_PASS' "$D/run.out") pass" | tee -a "$OUT/no495.a.out"
# (b)
F=$T/f_HEADno495
rm -rf "$F"; mkdir -p "$F/regress"
cp -a "$T/f_HEAD/src" "$T/f_HEAD/config.h" "$F/"
python3 "$S/no495.py" "$F/src/devices/dev_wdc.c" > "$OUT/no495.b.out" 2>&1 || { cat "$OUT/no495.b.out"; exit 3; }
cp "$S/opus_rearm_fuzz.c" "$F/regress/"
( cd "$F/regress" && gcc -O2 -std=c99 -Wall -I../src/include -I../src/include/thirdparty \
    -ffunction-sections -fdata-sections -Wl,--gc-sections -o fuzzd opus_rearm_fuzz.c && ./fuzzd 0 ) \
    >> "$OUT/no495.b.out" 2>&1
echo "(b) rung-1 directed sequences vs HEAD-minus-#495:"
grep -E '^  D1|^  D4' "$OUT/no495.b.out"
echo RUN_NO495_DONE
