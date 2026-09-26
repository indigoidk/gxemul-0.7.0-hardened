#!/bin/bash
#  #551 pass 1, opus seat: build a /tmp copy of HEAD's harness + dev_wdc.c and its dev_wdc.c mutants.
#  READ-ONLY toward C:\DocumentNoSnc\cc\GXEMUL\ -- everything is written under $W.
set -eu
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus551p1
REPO=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
W=/tmp/opus551p1
rm -rf "$W"; mkdir -p "$W/sec"
tar -x -C "$W/sec" -f "$SP/sec_head.tar"
cp "$REPO/config.h" "$W/sec/config.h"          # generated, ignored by git; misc.h needs ../../config.h
echo "HEAD copy vs working tree (both files are clean vs HEAD):"
md5sum "$W/sec/regress/diff_wdc_identify.c" "$REPO/regress/diff_wdc_identify.c" \
       "$W/sec/src/devices/dev_wdc.c" "$REPO/src/devices/dev_wdc.c" | awk '{print "  " $1 "  " $2}'

python3 - "$W" <<'PYEOF'
import io, os, sys
W = sys.argv[1]
src = io.open(W + "/sec/src/devices/dev_wdc.c", encoding="utf-8", newline="").read()
def need1(s, frag):
    n = s.count(frag)
    if n != 1:
        raise SystemExit("anchor count %d for %r" % (n, frag[:60]))
muts = {}
muts["pristine"] = src
sm_old = io.open(W + "/sec/regress/selfmutants/wdc_identify.old", encoding="utf-8", newline="").read()
sm_new = io.open(W + "/sec/regress/selfmutants/wdc_identify.new", encoding="utf-8", newline="").read()
need1(src, sm_old); muts["selfmut"] = src.replace(sm_old, sm_new, 1)
# the true pre-#405 text: the six SHIFTED capacity lines back to `% 255`
s = src
for w in ("58", "61"):
    for sh in ("24", "16"):
        a = "d->identify_struct[2 * %s + %s] = ((total_size / 512) >> %s) & 255;" % (w, "0" if sh == "24" else "1", sh)
        need1(s, a); s = s.replace(a, a.replace("& 255", "% 255"))
for w in ("57", "60"):
    a = "d->identify_struct[2 * %s + 0] = ((total_size / 512) >> 8) & 255;" % w
    need1(s, a); s = s.replace(a, a.replace("& 255", "% 255"))
muts["rev255"] = s
# a 13-bit cylinder truncation: first self-contradiction at c = 8192, so ONLY the
# spec-free oracle (row_selfconsistent) can see it -- row_wide_geometry uses c = 4096.
a = "d->identify_struct[2 * 1 + 0] = d->cyls[d->drive] >> 8;"
need1(src, a); muts["cyl13"] = src.replace(a, "d->identify_struct[2 * 1 + 0] = (d->cyls[d->drive] >> 8) & 0x1f;")
# the pre-#481 reset bit: kills only SRST rows, all of which run before row 125
a = "if (idata & WDCTL_RST) {"
need1(src, a); muts["srstbit"] = src.replace(a, "if (idata & WDCTL_4BIT) {")
for k, v in muts.items():
    d = "%s/dev/%s/src/devices" % (W, k); os.makedirs(d, exist_ok=True)
    os.makedirs("%s/dev/%s/regress" % (W, k), exist_ok=True)
    io.open(d + "/dev_wdc.c", "w", encoding="utf-8", newline="").write(v)
    print("  dev variant %-9s %s" % (k, "pristine" if v == src else "%d chars differ" % sum(1 for x, y in zip(v, src) if x != y)))
PYEOF
#  the harness's quoted include "../src/devices/dev_wdc.c" resolves per dev tree, and the
#  headers' "../../config.h" resolves against $W/sec -- link config.h next to each tree too.
for d in "$W"/dev/*; do ln -s "$W/sec/config.h" "$d/config.h"; done
python3 "$SP/xform.py" census "$W/sec/regress/diff_wdc_identify.c"
echo SETUP_DONE
