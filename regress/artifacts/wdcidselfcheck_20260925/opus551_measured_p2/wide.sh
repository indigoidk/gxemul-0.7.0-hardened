#!/bin/bash
#  serial builds only (a kill table is running)
set -u
P2=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus551p1/p2
W=/tmp/opus551p2
python3 "$P2/wide.py" "$W" || exit 1
FLAGS="-std=c99 -I$W/sec/src/include -I$W/sec/src/include/thirdparty -ffunction-sections -fdata-sections -Wl,--gc-sections"
run() { local h=$1 dev=$2 d=$W/dev/$2/regress; cp "$W/h/$h.c" "$d/"; rm -f "$d/$h.bin"
  if cc -O2 $FLAGS -o "$d/$h.bin" "$d/$h.c" > "$d/$h.cc" 2>&1 && [ "$d/$h.bin" -nt "$d/$h.c" ]; then
    timeout 300 "$d/$h.bin" > "$d/$h.log" 2>&1; echo $? > "$d/$h.rc"; else echo BUILD_FAIL > "$d/$h.rc"; fi; }
for dev in pristine selfmut rev255 cyl13 srstbit drqring w57hi w58lo; do run F_wide $dev; done
run F_wide_u16 pristine; run F_wide_sect4 pristine
python3 - "$W" <<'PYEOF'
import io, sys
W = sys.argv[1]
def rd(dev, h, e):
    return io.open("%s/dev/%s/regress/%s.%s" % (W, dev, h, e), encoding="utf-8", errors="replace").read()
def strip(t): return [l for l in t.split("\n") if "SELFCHECK" not in l]
for dev in ("pristine", "selfmut", "rev255", "cyl13", "srstbit", "drqring", "w57hi", "w58lo"):
    a, b = rd(dev, "F", "log"), rd(dev, "F_wide", "log")
    print("  F_wide vs F  %-8s %s rc %s/%s" % (dev, "IDENTICAL except SELFCHECK lines" if strip(a) == strip(b) else "DIFFER",
          rd(dev, "F", "rc").strip(), rd(dev, "F_wide", "rc").strip()))
for h in ("F_wide", "F_wide_u16", "F_wide_sect4"):
    t = rd("pristine", h, "log")
    print("  %-13s pristine: %s | %s" % (h, " | ".join(l.strip() for l in t.split("\n") if "SELFCHECK" in l and "@@" not in l),
          [l for l in t.split("\n") if l.startswith("WDC_")]))
t = rd("pristine", "F", "log")
print("  grep -c 'high byte' semantics (LINES) on F pristine:", sum(1 for l in t.split("\n") if "high byte" in l))
PYEOF
echo WIDE_DONE
