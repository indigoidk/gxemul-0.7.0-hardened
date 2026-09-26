#!/bin/bash
#  #551 PASS 2, opus seat.  WSL /tmp only; builds SINGLE-THREADED (a kill table is running).
#  Reads the repo (never writes it): the FINAL harness from the working tree, dev_wdc.c from HEAD.
set -u
P2=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus551p1/p2
TAR=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus551p1/sec_head.tar
REPO=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
W=/tmp/opus551p2
rm -rf "$W"; mkdir -p "$W/sec" "$W/h"
tar -x -C "$W/sec" -f "$TAR"
cp "$REPO/config.h" "$W/sec/config.h"
cp "$REPO/regress/diff_wdc_identify.c" "$W/final.c"
echo "final harness md5 (want ef662cb5...): $(md5sum < "$W/final.c" | cut -c1-32)"
echo "dev_wdc.c HEAD copy vs working tree:  $(md5sum < "$W/sec/src/devices/dev_wdc.c" | cut -c1-8) $(md5sum < "$REPO/src/devices/dev_wdc.c" | cut -c1-8)"
#  gate 2's wdc check block, located by pattern in the WORKING-TREE gate (it carries #550+#551)
awk '/check     "wdc IDENTIFY: row failures"/{s=1} s && /^fi$/ {exit} s' "$REPO/regress/gate_offline.sh" > "$W/gatewdc.inc"
echo "gate-2 wdc checks extracted: $(grep -c '^ *check' "$W/gatewdc.inc")"
grep -q "grep -q 'SELFCHECK the comparator can still fail'" "$REPO/regress/gate_offline.sh" && echo "G row present in gate_offline.sh"
grep -q '^SC_COVERED=.*wdc_identify' "$REPO/regress/gate_offline.sh" && echo "wdc_identify is in SC_COVERED"

python3 - "$W" <<'PYEOF'
import io, os, sys
W = sys.argv[1]
src = io.open(W + "/sec/src/devices/dev_wdc.c", encoding="utf-8", newline="").read()
def need1(s, frag):
    if s.count(frag) != 1:
        raise SystemExit("anchor count %d for %r" % (s.count(frag), frag[:60]))
sm_old = io.open(W + "/sec/regress/selfmutants/wdc_identify.old", encoding="utf-8", newline="").read()
sm_new = io.open(W + "/sec/regress/selfmutants/wdc_identify.new", encoding="utf-8", newline="").read()
def sm(s):
    need1(s, sm_old); return s.replace(sm_old, sm_new, 1)
def rep(s, a, b):
    need1(s, a); return s.replace(a, b)
M = {"pristine": src, "selfmut": sm(src)}
s = src
for w_, sh, b in (("58", "24", "0"), ("58", "16", "1"), ("61", "24", "0"), ("61", "16", "1"), ("57", "8", "0"), ("60", "8", "0")):
    a = "d->identify_struct[2 * %s + %s] = ((total_size / 512) >> %s) & 255;" % (w_, b, sh)
    s = rep(s, a, a.replace("& 255", "% 255"))
M["rev255"] = s
M["cyl13"] = rep(src, "d->identify_struct[2 * 1 + 0] = d->cyls[d->drive] >> 8;",
                 "d->identify_struct[2 * 1 + 0] = (d->cyls[d->drive] >> 8) & 0x1f;")
M["srstbit"] = rep(src, "if (idata & WDCTL_RST) {", "if (idata & WDCTL_4BIT) {")
M["drqring"] = rep(src, "\tif (d->inbuf_head != d->inbuf_tail)\n\t\todata |= WDCS_DRQ;\n", "")
M["w57hi"] = rep(src, "d->identify_struct[2 * 57 + 0] = ((total_size / 512) >> 8) & 255;",
                 "d->identify_struct[2 * 57 + 0] = 0;")
#  word 58's low byte (bits 16-23 of "current capacity"); nothing but row() reads 57-58
M["w58lo"] = rep(src, "d->identify_struct[2 * 58 + 1] = ((total_size / 512) >> 16) & 255;",
                 "d->identify_struct[2 * 58 + 1] = 0;")
#  #484's own named mutant: a full ring drops its OLDEST byte instead of refusing the newest.
#  Occupancy and DRQ stay sound; only the anchored rows can see it.
M["dropold"] = rep(src, "\t\treturn;\n\t}\n\n\td->inbuf[d->inbuf_head] = c;",
                   "\t\td->inbuf_tail = (d->inbuf_tail + 1) % WDC_INBUF_SIZE;\n\t}\n\n\td->inbuf[d->inbuf_head] = c;")
for base in ("drqring", "w57hi", "w58lo", "dropold"):
    M[base + "_sm"] = sm(M[base])
for k, v in M.items():
    os.makedirs("%s/dev/%s/src/devices" % (W, k), exist_ok=True)
    os.makedirs("%s/dev/%s/regress" % (W, k), exist_ok=True)
    io.open("%s/dev/%s/src/devices/dev_wdc.c" % (W, k), "w", encoding="utf-8", newline="").write(v)
print("dev variants:", " ".join(sorted(M)))
PYEOF
python3 "$P2/xform3.py" "$W/final.c" "$W/h" || exit 1
for d in "$W"/dev/*/; do cp "$W"/h/*.c "$d/regress/"; done

FLAGS="-std=c99 -I$W/sec/src/include -I$W/sec/src/include/thirdparty -ffunction-sections -fdata-sections -Wl,--gc-sections"
one() {   # harness dev -- gate 2's own compile line (-O2), then run as gate 2 does (2>&1)
    local h=$1 dev=$2 d=$W/dev/$2/regress
    rm -f "$d/$h.bin" "$d/$h.log" "$d/$h.rc"
    if cc -O2 $FLAGS -o "$d/$h.bin" "$d/$h.c" > "$d/$h.cc" 2>&1 && [ "$d/$h.bin" -nt "$d/$h.c" ]; then
        timeout 300 "$d/$h.bin" > "$d/$h.log" 2>&1; echo $? > "$d/$h.rc"
    else
        echo BUILD_FAIL > "$d/$h.rc"
    fi
}
{
    for dev in pristine selfmut rev255 cyl13 srstbit drqring w57hi w58lo dropold drqring_sm w57hi_sm w58lo_sm dropold_sm; do echo "F $dev"; done
    for dev in pristine selfmut rev255 cyl13 srstbit drqring w57hi; do echo "F_fc $dev"; done
    for dev in pristine selfmut dropold dropold_sm; do echo "F_want165 $dev"; done
    for dev in pristine selfmut w57hi w57hi_sm; do echo "F_sect4 $dev"; echo "F_wrap $dev"; done
    for dev in pristine selfmut w58lo w58lo_sm; do echo "F_u16 $dev"; done
    for dev in pristine selfmut drqring drqring_sm; do echo "F_postinc $dev"; echo "F_name $dev"; done
    for dev in pristine selfmut; do echo "F_scnoforce_chkstub $dev"; echo "F_fc_scnoforce_chkstub $dev"; done
} > "$W/jobs.txt"
echo "jobs: $(wc -l < "$W/jobs.txt") (serial)"
t0=$(date +%s)
while read -r h dev; do one "$h" "$dev"; done < "$W/jobs.txt"
echo "built+ran serially in $(( $(date +%s) - t0 )) s; build failures: $(grep -l BUILD_FAIL "$W"/dev/*/regress/*.rc 2>/dev/null | wc -l)"
echo RUN3_DONE
