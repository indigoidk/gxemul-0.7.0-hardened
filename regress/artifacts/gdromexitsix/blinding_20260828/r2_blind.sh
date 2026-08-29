#!/bin/bash
#  THE PREDICTION, committed in writing before this ran:
#  pre-fix the mis-assembled packets scored 55/58, CAUGHT via the host DYING.
#  post-fix the host survives, so the nodata-stale triple must go GREEN and both must
#  read 58/58 -- the probe blinded to a mis-assembled packet.  That blinding is the
#  entire justification for the 19-row replacement detector.
R=/mnt/c/DocumentNoSnc/cc/GXEMUL
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/40fd4ccc-4c3b-4ad6-91dc-122d039ab5a2/scratchpad
P=$R/GXEMUL-SEC/regress/gdrom_default_probe.py
for pkt in 0x2031 0x2130; do
  cp "$P" $S/p_blind.py
  python3 - "$S/p_blind.py" "$pkt" <<'PY'
import io, sys
p, pkt = sys.argv[1], sys.argv[2]
t = io.open(p, encoding='utf-8', newline='').read()
a = '"r8=0x2030"'
assert t.count(a) == 1, "anchor count %d -- refusing" % t.count(a)
io.open(p,'w',encoding='utf-8',newline='').write(t.replace(a, '"r8=%s"' % pkt, 1))
PY
  [ $? -eq 0 ] || { echo "PATCH FAILED for $pkt"; continue; }
  echo "=== post-fix, packet $pkt ==="
  python3 -u $S/p_blind.py $R/build/gxemul $R/_images/openbsd76-landisk-bsd.rd 2>&1 \
    | grep -E "GDROM_DEF_RESULT|^(nodata stale|stale says|stale idle)"
done
echo R2_BLIND_DONE
