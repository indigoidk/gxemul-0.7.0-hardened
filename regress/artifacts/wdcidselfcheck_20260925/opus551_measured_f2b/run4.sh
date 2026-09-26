#!/bin/bash
#  #551 F2 on pass 2, opus seat.  WSL /tmp only; SERIAL builds (a kill table is running).
#  Device variants are pass 2's (/tmp/opus551p2, built from HEAD's dev_wdc.c); harness = MINE_b.c.
set -u
F2B=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus551p1/f2b
MINE=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/wdc551/MINE_b.c
REPO=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
W=/tmp/opus551f2b
rm -rf "$W"; mkdir -p "$W/h"
cp -a /tmp/opus551p2/sec /tmp/opus551p2/dev "$W/"
cp "$MINE" "$W/final.c"
echo "MINE_b md5 (want d0339493): $(md5sum < "$W/final.c" | cut -c1-8); dev_wdc.c in the device trees: $(md5sum < "$W/dev/pristine/src/devices/dev_wdc.c" | cut -c1-8) (HEAD $(git -C "$REPO" show HEAD:src/devices/dev_wdc.c 2>/dev/null | md5sum | cut -c1-8))"
awk '/check     "wdc IDENTIFY: row failures"/{s=1} s && /^fi$/ {exit} s' "$REPO/regress/gate_offline.sh" > "$W/gatewdc.inc"
echo "gate-2 wdc checks extracted: $(grep -c '^ *check' "$W/gatewdc.inc")"
python3 "$F2B/xform4.py" "$W/final.c" "$W/h" || exit 1
for d in "$W"/dev/*/; do rm -f "$d"/regress/*; cp "$W"/h/*.c "$d/regress/"; done
FLAGS="-std=c99 -I$W/sec/src/include -I$W/sec/src/include/thirdparty -ffunction-sections -fdata-sections -Wl,--gc-sections"
one() {
    local h=$1 dev=$2 d=$W/dev/$2/regress
    if cc -O2 $FLAGS -o "$d/$h.bin" "$d/$h.c" > "$d/$h.cc" 2>&1 && [ "$d/$h.bin" -nt "$d/$h.c" ]; then
        timeout 300 "$d/$h.bin" > "$d/$h.log" 2>&1; echo $? > "$d/$h.rc"
    else
        echo BUILD_FAIL > "$d/$h.rc"
    fi
}
{
    for dev in pristine selfmut dropold drqring w57hi w58lo dropold_sm drqring_sm w57hi_sm w58lo_sm rev255 cyl13 srstbit; do echo "B $dev"; done
    for dev in pristine selfmut dropold dropold_sm; do echo "B_want165 $dev"; done
    for dev in pristine selfmut w57hi w57hi_sm; do echo "B_sect4 $dev"; echo "B_wrap $dev"; done
    for dev in pristine selfmut w58lo w58lo_sm; do echo "B_u16 $dev"; done
    for dev in pristine selfmut drqring drqring_sm; do echo "B_postinc $dev"; echo "B_name $dev"; done
    for dev in pristine selfmut; do echo "B_scnoforce_chkstub $dev"; echo "B_andsect $dev"; done
    for dev in pristine selfmut dropold dropold_sm drqring drqring_sm w57hi w57hi_sm; do echo "B_tally $dev"; done
    for dev in pristine selfmut; do echo "B_nosc_full $dev"; echo "B_nosc_keepdecl $dev"; echo "B_nosc_nodecl $dev"; done
} > "$W/jobs.txt"
echo "jobs: $(wc -l < "$W/jobs.txt") (serial)"
t0=$(date +%s)
while read -r h dev; do one "$h" "$dev"; done < "$W/jobs.txt"
echo "built+ran serially in $(( $(date +%s) - t0 )) s; build failures: $(grep -l BUILD_FAIL "$W"/dev/*/regress/*.rc | sed "s|$W/dev/||" | tr '\n' ' ')"
echo RUN4_DONE
