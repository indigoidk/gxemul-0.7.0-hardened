#!/bin/bash
set -u
C5=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus551p1/c
W=/tmp/opus551c
python3 "$C5/pin.py" "$W" || exit 1
FLAGS="-std=c99 -I$W/sec/src/include -I$W/sec/src/include/thirdparty -ffunction-sections -fdata-sections -Wl,--gc-sections"
run() { local h=$1 dev=$2 d=$W/dev/$2/regress; cp "$W/h/$h.c" "$d/"
  if cc -O2 $FLAGS -o "$d/$h.bin" "$d/$h.c" > "$d/$h.cc" 2>&1 && [ "$d/$h.bin" -nt "$d/$h.c" ]; then
    timeout 300 "$d/$h.bin" > "$d/$h.log" 2>&1; echo $? > "$d/$h.rc"; else echo BUILD_FAIL > "$d/$h.rc"; fi; }
for dev in pristine selfmut dropold drqring w57hi; do run Cpin $dev; done
for dev in pristine dropold; do run Cpin_nocmpinc_reset1 $dev; done
for dev in pristine selfmut dropold drqring w57hi; do
  printf "  Cpin vs Cfix %-8s %s\n" $dev "$(cmp -s $W/dev/$dev/regress/Cpin.log $W/dev/$dev/regress/Cfix.log && echo WHOLE-LOG-IDENTICAL || echo DIFFER)"; done
for dev in pristine dropold; do
  printf "  Cpin_nocmpinc_reset1 %-8s %s | %s\n" $dev "$(grep -E '^[0-9]+ rows|WDC_IDENTIFY' $W/dev/$dev/regress/Cpin_nocmpinc_reset1.log | tr '\n' ' ')" \
    "$(grep 'SELFCHECK(' $W/dev/$dev/regress/Cpin_nocmpinc_reset1.log | tr -s ' ' | tr '\n' ' ')"; done
echo PIN_DONE
