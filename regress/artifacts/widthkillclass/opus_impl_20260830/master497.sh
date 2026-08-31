#!/bin/bash
#  #497 DEFINITIVE RUN -- 35-row instrument, frozen once, used for every row.
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/gx497
OUT=/tmp/gx497tab
T=/tmp/gx497impl
SRC=$T/src/devices/dev_sgi_re.c
rm -rf "$OUT"; mkdir -p "$OUT"

echo "########## 0. FREEZE THE INSTRUMENT (one probe for the whole comparison)"
cp "$SP/sgi_re_width_probe.py" /tmp/gx497_probe_frozen.py
cp "$SP/table497.sh"           /tmp/gx497_table_frozen.sh
md5sum /tmp/gx497_probe_frozen.py

echo "########## 0b. tree must be at the FIXED source before we start"
cp /tmp/gx497_fix_src.c "$SRC"
rm -f "$T/src/devices/dev_sgi_re.o"
( cd "$T" && make -j8 ) > "$OUT/build_fix.log" 2>&1
echo "MAKE_RC=$?"
if [ "$T/gxemul" -nt "$SRC" ]; then echo "FRESH=YES"; else echo "FRESH=NO *** STOP ***"; exit 1; fi
cp "$T/gxemul" /tmp/gx497_fix_gxemul

echo ""
echo "########## 1. THE FIX ITSELF (must be clean)"
python3 -u /tmp/gx497_probe_frozen.py /tmp/gx497_fix_gxemul FIX > "$OUT/probe_fix.out" 2>&1
grep -h "OPUS497T_CONTROL\|OPUS497T_RESULT" "$OUT/probe_fix.out"
grep "FAIL" "$OUT/probe_fix.out" | sed "s/^/    /"

echo ""
echo "########## 2. FLOOR (a) -- PRE-FIX build must FAIL"
python3 -u /tmp/gx497_probe_frozen.py /tmp/gx497_base_gxemul PREFIX > "$OUT/probe_a_prefix.out" 2>&1
grep -h "OPUS497T_CONTROL\|OPUS497T_RESULT" "$OUT/probe_a_prefix.out"

echo ""
echo "########## 3. FLOOR (c) -- NULL MEDIUM"
python3 -u /tmp/gx497_probe_frozen.py /bin/true NULLMEDIUM > "$OUT/probe_c_null.out" 2>&1
grep -h "OPUS497T_CONTROL\|OPUS497T_RESULT" "$OUT/probe_c_null.out"

echo ""
echo "########## 4. THE MUTANT TABLE"
bash /tmp/gx497_table_frozen.sh \
    b_all b_tlba b_tlbb b_tlbc b_tex b_lina b_linb \
    d_andwrite d_growth d_ifnotelse d_returnzero \
    d_nolatch d_noset d_sharedbit d_bitcollide e_wrongsite

echo ""
echo "########## 5. SUMMARY"
for f in "$OUT"/probe_*.out; do
    lab=$(grep -h "OPUS497T_LABEL=" "$f" | sed "s/OPUS497T_LABEL=//")
    res=$(grep -h "OPUS497T_RESULT=" "$f" | sed "s/OPUS497T_RESULT=//")
    ctl=$(grep -h "OPUS497T_CONTROL=" "$f" | sed "s/OPUS497T_CONTROL=//")
    printf "  %-14s %-10s CONTROL=%s\n" "$lab" "$res" "$ctl"
done
echo "MASTER497_DONE"
