#!/bin/bash
# Q1(d): build the FROZEN pre-repair harness (333 rows) against the FROZEN device and compare its row
# names with the repaired harness's 491: every pre-repair row except IDENTITY must reappear, green.
X=/tmp/opusq2r
F=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2r/frozen
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2r/opus
cmp "$X/src/devices/dev_footbridge.c" "$F/dev_footbridge.c" || { echo "scratch device is not the frozen copy"; exit 9; }
cp "$F/diff_footbridge.prerepair.c" "$X/regress/diff_pre.c"
cd "$X/regress" || exit 9
gcc -O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections -Wl,--gc-sections -I"$X/src" -I"$X/src/include" -I"$X/src/include/thirdparty" -o dpre diff_pre.c -lm || exit 9
./dpre > "$O/prerepair.log" 2>&1
tail -2 "$O/prerepair.log"
python3 - "$O/prerepair.log" "$O/baseline.log" <<'PYEOF'
import re, sys
def names(p):
    ok, bad = [], []
    for ln in open(p, encoding="utf-8"):
        m = re.match(r"^  ok    (.*?)\s+\S+$", ln.rstrip("\n"))
        if m and "SELFCHECK" not in ln:
            ok.append(m.group(1).rstrip())
        elif ln.startswith("  FAIL  ") and "@@SELFCHECK@@" not in ln:
            bad.append(ln[8:].rstrip())
    return ok, bad
pre_ok, pre_bad = names(sys.argv[1])
new_ok, new_bad = names(sys.argv[2])
print("pre-repair: %d green names (%d distinct), %d red" % (len(pre_ok), len(set(pre_ok)), len(pre_bad)))
print("repaired  : %d green names (%d distinct), %d red" % (len(new_ok), len(set(new_ok)), len(new_bad)))
missing = [n for n in pre_ok if n not in set(new_ok)]
print("pre-repair green names absent from the repaired run:", missing)
added = sorted(set(new_ok) - set(pre_ok))
fam = {}
for n in added:
    fam[n.split()[0]] = fam.get(n.split()[0], 0) + 1
print("names added by the repair, by prefix:", fam)
print("added X6 names not containing 'wide':", [n for n in added if n.startswith("X6") and "wide" not in n])
print("added X7 names not containing 'wide':", [n for n in added if n.startswith("X7") and "wide" not in n])
PYEOF
rm -f "$X/regress/dpre" "$X/regress/diff_pre.c"
echo PRE_DONE
