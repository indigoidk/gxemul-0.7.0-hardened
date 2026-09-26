#!/bin/bash
set -u
F2B=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus551p1/f2b
W=/tmp/opus551f2b
python3 "$F2B/cnt.py" "$W" || exit 1
FLAGS="-std=c99 -I$W/sec/src/include -I$W/sec/src/include/thirdparty -ffunction-sections -fdata-sections -Wl,--gc-sections"
run() { local h=$1 dev=$2 d=$W/dev/$2/regress; cp "$W/h/$h.c" "$d/"
  if cc -O2 $FLAGS -o "$d/$h.bin" "$d/$h.c" > "$d/$h.cc" 2>&1 && [ "$d/$h.bin" -nt "$d/$h.c" ]; then
    timeout 300 "$d/$h.bin" > "$d/$h.log" 2>&1; echo $? > "$d/$h.rc"; else echo BUILD_FAIL > "$d/$h.rc"; fi; }
for dev in pristine selfmut rev255 cyl13 srstbit drqring w57hi dropold w58lo; do run B_cnt $dev; done
for dev in dropold drqring w57hi; do run B_cnt_tally $dev; done
python3 - "$W" <<'PYEOF'
import io, re, sys
W = sys.argv[1]
def rd(dev, h, e): return io.open("%s/dev/%s/regress/%s.%s" % (W, dev, h, e), encoding="utf-8", errors="replace").read()
for dev in ("pristine", "selfmut", "rev255", "cyl13", "srstbit", "drqring", "w57hi", "dropold", "w58lo"):
    a, b = rd(dev, "B", "log"), rd(dev, "B_cnt", "log")
    print("  B_cnt vs B %-8s %s rc %s/%s" % (dev, "IDENTICAL (whole log)" if a == b else "DIFFER",
          rd(dev, "B", "rc").strip(), rd(dev, "B_cnt", "rc").strip()))
for dev in ("dropold", "drqring", "w57hi"):
    t = rd(dev, "B_cnt_tally", "log")
    m = re.search(r"^(\d+) rows, (\d+) failures", t, re.M)
    print("  B_cnt_tally %-8s trailer '%s' token %s rc %s" % (dev, m.group(0) if m else "?",
          re.search(r"WDC_IDENTIFY_(PASS|FAIL)", t).group(0), rd(dev, "B_cnt_tally", "rc").strip()))
PYEOF
echo CNT_DONE
