#!/bin/bash
#  #551c, opus seat.  WSL /tmp only; SERIAL builds (a kill table is running).
set -u
C5=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus551p1/c
MINE=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/wdc551/MINE_c.c
REPO=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
W=/tmp/opus551c
rm -rf "$W"; mkdir -p "$W/h"
cp -a /tmp/opus551p2/sec /tmp/opus551p2/dev "$W/"
cp "$MINE" "$W/final.c"
echo "MINE_c md5 (want 765f71d8): $(md5sum < "$W/final.c" | cut -c1-8); device dev_wdc.c: $(md5sum < "$W/dev/pristine/src/devices/dev_wdc.c" | cut -c1-8) (repo $(md5sum < "$REPO/src/devices/dev_wdc.c" | cut -c1-8))"
awk '/check     "wdc IDENTIFY: row failures"/{s=1} s && /^fi$/ {exit} s' "$REPO/regress/gate_offline.sh" > "$W/gatewdc.inc"
echo "gate-2 wdc checks extracted: $(grep -c '^ *check' "$W/gatewdc.inc")"
python3 "$C5/xform5.py" "$W/final.c" "$W/h" || exit 1
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
ESC="pristine selfmut dropold dropold_sm drqring drqring_sm w57hi w57hi_sm"
{
    for dev in pristine selfmut rev255 cyl13 srstbit drqring w57hi w58lo dropold drqring_sm w57hi_sm dropold_sm; do echo "C $dev"; echo "Cfix $dev"; done
    for h in C_reset1 C_resetcmp C_reset2 C_nocmpinc C_nocmpinc_reset1 C_recon_ge_sub C_recon_sub C_recon_lt \
             C_recon_del C_recon_uncond C_sub_before C_sub_after C_reset1_after C_scg_del \
             Cfix_recon_ge_sub Cfix_sub_after Cfix_reset2; do
        for dev in $ESC; do echo "$h $dev"; done
    done
} > "$W/jobs.txt"
echo "jobs: $(wc -l < "$W/jobs.txt") (serial)"
t0=$(date +%s)
while read -r h dev; do one "$h" "$dev"; done < "$W/jobs.txt"
echo "built+ran serially in $(( $(date +%s) - t0 )) s; build failures: $(grep -l BUILD_FAIL "$W"/dev/*/regress/*.rc | wc -l)"
echo RUN5_DONE
