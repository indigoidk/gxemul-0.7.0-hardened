#!/bin/bash
# fable5 adj B -- the full argument-shape closure (pinned_shape) on BASE and the four paren-drop media, plus the
# D1 companion: ASAN (pinned) vs the sizeof form on the pointer media, already in RESULTS.txt.
set -u
P=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/adjB
W=/tmp/gxfable_adjB
O=$W/out
python3 -I "$P/mk_variant2.py" "$W"
python3 -c "import ast; ast.parse(open('/tmp/gxfable_adjB/variants/pinned_shape/sysasic_range_check.py').read()); print('pinned_shape driver parses')"
echo "  pinned_shape driver md5 $(md5sum < $W/variants/pinned_shape/sysasic_range_check.py | cut -c1-12) cases md5 $(md5sum < $W/variants/pinned_shape/sysasic_range_cases.c | cut -c1-12)"
diff "$W/variants/pinned/sysasic_range_cases.c" "$W/variants/pinned_shape/sysasic_range_cases.c" > "$W/shape_cases.diff"
diff "$W/variants/pinned/sysasic_range_check.py" "$W/variants/pinned_shape/sysasic_range_check.py" > "$W/shape_driver.diff"
echo "shape cases diff lines: $(grep -c '^[<>]' $W/shape_cases.diff); shape driver diff lines: $(grep -c '^[<>]' $W/shape_driver.diff)"
echo "SHAPE start $(date '+%Y-%m-%d %H:%M:%S')"
one() {
  local v=$1 m=$2
  local h=$W/media/$m/thirdparty/dreamcast_sysasicvar.h
  python3 -I "$W/variants/$v/sysasic_range_check.py" --cc cc --header "$h" --memory-h "$W/memory.h" \
      --keep "$W/rowlogs/$v/$m" > "$O/${v}__$m.out" 2>&1
  local rc=$?
  local red; red=$(grep -E '^  FAIL ' "$O/${v}__$m.out" | awk '{print $2"."$3}' | tr '\n' ',' | sed 's/,$//')
  printf '%-18s %-16s exit=%d %s red=[%s]\n' "$v" "$m" "$rc" "$(tail -1 "$O/${v}__$m.out")" "$red"
}
export -f one; export W O
for m in BASE HEADH cand_buf4 ptr4 ptr8 e1noparen e2noparen A_enoparen B_enoparen; do echo "pinned_shape $m"; done | \
  xargs -P 6 -n 2 bash -c 'one "$0" "$1"' | sort | tee "$W/RESULTS_shape.txt"
echo "--- detail lines on the five shape media (SWEEP, TSWEEP, TVAL)"
for m in BASE e1noparen e2noparen A_enoparen B_enoparen; do
  grep -E '^  (ok|FAIL) +(PROD|POL) +(SWEEP|TSWEEP|TVAL) ' "$O/pinned_shape__$m.out" | sed "s/^/  $m: /" | cut -c1-230
done
echo "--- the TX record lines on BASE / A_enoparen / B_enoparen"
for m in BASE A_enoparen B_enoparen; do grep '^TX ' "$W/rowlogs/pinned_shape/$m/PROD_TVAL.run" | sed "s/^/  $m: /" | cut -c1-160; done
echo "SHAPE end $(date '+%Y-%m-%d %H:%M:%S')"
echo SHAPE_DONE
