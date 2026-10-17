#!/bin/bash
# fable5 adj B -- the measurement matrix.  Every run: a driver variant x a header medium, the frozen driver's own
# flags (mirror) unless the variant adds ASAN itself; memory.h = HEAD's.  Row logs kept under $W/rowlogs/<tag>/<m>.
set -u
W=/tmp/gxfable_adjB
O=$W/out; rm -rf "$O" "$W/rowlogs"; mkdir -p "$O" "$W/rowlogs"
echo "MATRIX start $(date '+%Y-%m-%d %H:%M:%S')"
one() {   # one <variant> <medium> <cc>
  local v=$1 m=$2 ccarg=$3
  local tag=$v; [ "$ccarg" != cc ] && tag="${v}@noasan"
  local h=$W/media/$m/thirdparty/dreamcast_sysasicvar.h
  python3 -I "$W/variants/$v/sysasic_range_check.py" --cc "$ccarg" --header "$h" --memory-h "$W/memory.h" \
      --keep "$W/rowlogs/$tag/$m" > "$O/${tag}__$m.out" 2>&1
  local rc=$?
  local red; red=$(grep -E '^  FAIL ' "$O/${tag}__$m.out" | awk '{print $2"."$3}' | tr '\n' ',' | sed 's/,$//')
  local void; void=$(grep -m1 '^VOID: ' "$O/${tag}__$m.out" | cut -c1-120)
  printf '%-18s %-16s exit=%d %s red=[%s] %s\n' "$tag" "$m" "$rc" "$(tail -1 "$O/${tag}__$m.out")" "$red" "$void"
}
export -f one; export W O
ALL="BASE HEADH cand_buf4 cand_buf16 ptr8 ptr4 u64obj cast_uc cast_u8 plus0 sz8 cand_rwlen_hex static8 e1noparen e2noparen A_enoparen B_enoparen T54_MEM_WRITE_2"
{
  for m in $ALL; do echo "orig $m cc"; echo "pinned $m cc"; done
  for m in BASE HEADH e1noparen e2noparen A_enoparen B_enoparen; do echo "pinned_sample $m cc"; done
  for m in BASE cand_buf4 cand_buf16 ptr8 ptr4 u64obj cast_uc plus0 cand_rwlen_hex; do echo "sizeof_both $m cc"; done
  for m in BASE T54_MEM_WRITE_2; do echo "pinned_mw2 $m cc"; done
  echo "pinned BASE $W/cc_noasan.sh"
  echo "pinned_preflight BASE $W/cc_noasan.sh"
  echo "pinned_preflight BASE cc"
  echo "pinned_preflight cand_buf4 cc"
} > "$W/JOBS.txt"
echo "jobs: $(wc -l < $W/JOBS.txt)"
xargs -P 6 -n 3 bash -c 'one "$0" "$1" "$2"' < "$W/JOBS.txt" | sort > "$W/RESULTS.txt"
cat "$W/RESULTS.txt"
echo "--- ASAN evidence lines (the run logs' first sanitizer line) for the extent media:"
for t in pinned/cand_buf4 pinned/ptr4 pinned/ptr8 pinned/cast_uc pinned/plus0 pinned/u64obj pinned/static8 pinned/cand_buf16 pinned_preflight/cand_buf4; do
  for r in ID TVAL; do
    f=$W/rowlogs/$t/PROD_$r.run
    if [ -f "$f" ]; then echo "  $t $r: $(head -1 "$f") | $(grep -m1 -E 'ERROR: AddressSanitizer|SUMMARY: AddressSanitizer' "$f" | cut -c1-120)"; else echo "  $t $r: (no run log)"; fi
  done
done
echo "--- the link-failure simulation: PROD_ID.err under pinned@noasan"
head -4 "$W/rowlogs/pinned@noasan/BASE/PROD_ID.err"
echo "--- the preflight line under both compilers"
grep -h '^sysasic_range_check: asan' "$O/pinned_preflight@noasan__BASE.out" "$O/pinned_preflight__BASE.out"
echo "--- the sample form: SWEEP/TSWEEP detail lines on BASE, e1noparen, e2noparen, A_enoparen, B_enoparen"
for m in BASE e1noparen e2noparen A_enoparen B_enoparen; do grep -E '^  (ok|FAIL) +(PROD|POL) +T?SWEEP ' "$O/pinned_sample__$m.out" | sed "s/^/  $m: /" | cut -c1-200; done
echo "MATRIX end $(date '+%Y-%m-%d %H:%M:%S')"
echo MATRIX_DONE
