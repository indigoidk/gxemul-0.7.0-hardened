#!/bin/bash
# opus5 late seat (wdcrearmzero), 2026-10-09.  Mutant table against the SHIPPED offline
# detector regress/diff_wdc_identify.c at three revisions:
#   1f1a02b  -- #473 as shipped (23 rows)
#   d894e35d -- #473's pass-2 corrections (dirty-ring row etc.)
#   HEAD     -- ef577140 (128 rows)
# Each mutant is built in its OWN fresh copy under /tmp/gxopuswdc/m_<rev>_<mut>; the
# baseline trees t_<rev> are never written, and are cmp-verified against their archives
# at the end.  Nothing is written under any project tree.  Outputs go to the scratchpad.
set -u
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opuswdc
OUT=$S/killtable_opus
mkdir -p "$OUT"
command -v python3 >/dev/null || { echo "NO python3 in WSL"; exit 7; }
T=/tmp/gxopuswdc
TABLE=$OUT/TABLE.txt
: > "$TABLE"

REFILL='data_in[d->atapi_received + j]'
ARM='wdc_addtoinbuf(d, d->atapi_st->data_in[j]);'

# name | old | new   (one per line, fields separated by '|')
MUTS="M0_identity|$REFILL|$REFILL
Md_wrongoff|$REFILL|data_in[j]
Md_frozenj|$REFILL|data_in[d->atapi_received]
Md_revwalk|$REFILL|data_in[d->atapi_received - j]
Md_halfj|$REFILL|data_in[d->atapi_received + j/2]
Md_order|$REFILL|data_in[d->atapi_received - consumed + j]
Md_armfrozen|$ARM|wdc_addtoinbuf(d, d->atapi_st->data_in[0]);"

printf '%-10s %-14s %-9s %s\n' REV MUTANT VERDICT DETAIL >> "$TABLE"
for rev in 1f1a02b d894e35d HEAD; do
  echo "$MUTS" | while IFS='|' read -r name old new; do
    D=$T/m_${rev}_${name}
    rm -rf "$D"; mkdir -p "$D"
    cp -a "$T/t_$rev/src" "$T/t_$rev/regress" "$T/t_$rev/config.h" "$D/"
    log=$OUT/${rev}_${name}.out
    : > "$log"
    if ! python3 "$S/mutate.py" "$D/src/devices/dev_wdc.c" "$old" "$new" >> "$log" 2>&1; then
      printf '%-10s %-14s %-9s %s\n' "$rev" "$name" "NOAPPLY" "find-text not unique/absent" >> "$TABLE"
      continue
    fi
    ( cd "$D/regress" && gcc -O2 -std=c99 -I../src/include -I../src/include/thirdparty \
        -ffunction-sections -fdata-sections -Wl,--gc-sections \
        -o mut diff_wdc_identify.c ) >> "$log" 2>&1
    if [ ! -x "$D/regress/mut" ] || [ ! "$D/regress/mut" -nt "$D/src/devices/dev_wdc.c" ]; then
      printf '%-10s %-14s %-9s %s\n' "$rev" "$name" "NOBUILD" "compile failed" >> "$TABLE"
      continue
    fi
    ( cd "$D/regress" && ./mut ) > "$D/run.out" 2> "$D/run.err"
    rc=$?
    cat "$D/run.out" >> "$log"
    summ=$(grep -E '^[0-9]+ rows, [0-9]+ failures' "$D/run.out")
    pass=$(grep -c 'WDC_IDENTIFY_PASS' "$D/run.out")
    fl=$(grep -E '^  FAIL' "$D/run.out" | sed -E 's/^  FAIL //' | cut -c1-40 | tr '\n' ';')
    if [ "$rc" -ne 0 ] && [ -z "$summ" ]; then
      v="CRASH"; summ="rc=$rc (no summary line)"
    elif [ "$pass" = "1" ]; then
      v="ESCAPED"
    else
      v="KILLED"
    fi
    printf '%-10s %-14s %-9s %s rc=%s %s\n' "$rev" "$name" "$v" "$summ" "$rc" "$fl" >> "$TABLE"
  done
done

echo "--- baseline integrity: t_<rev> dev_wdc.c vs its archive" >> "$TABLE"
for rev in 1f1a02b d894e35d HEAD; do
  mkdir -p "$T/chk_$rev" && tar -xf "$S/t_$rev.tar" -C "$T/chk_$rev"
  if cmp -s "$T/chk_$rev/t_$rev/src/devices/dev_wdc.c" "$T/t_$rev/src/devices/dev_wdc.c"; then
    echo "  $rev baseline dev_wdc.c UNMUTATED (cmp clean)" >> "$TABLE"
  else
    echo "  $rev baseline dev_wdc.c DIFFERS -- the table is void" >> "$TABLE"
  fi
done
echo KILLTABLE_DONE >> "$TABLE"
cat "$TABLE"
