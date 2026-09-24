#!/bin/bash
# COPY-ONLY backup of the peer session's work that no snapshot holds (Fable 5.1 audit ruling Q3 rank 1(a)):
# the two WSL /tmp clones' differing sources and the peer's _scratchpad generators.  Nothing is edited or removed.
set -u
S=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
P=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad
D=$S/regress/artifacts/stateaudit_20260923/peer_carriers
mkdir -p "$D/clones" "$D/scratch"
M="$D/MANIFEST.txt"
{
echo "# BACKUP COPIES taken by session GXEMUL [087a90] on $(date '+%F %T'), COPY-ONLY."
echo "# Owner of the work: session GXEMUL (2) [e8a2bc] (#540 lcaisaphys, #541 alphavmkill, #542 alphaifetchkill, #544 cxseatcheck)."
echo "# The LIVE copies are where the 'source' column says.  Do not edit these; do not commit them unless their owner decides."
echo "# A clone file 'DIFFERS' from the GXEMUL-SEC working tree either because it carries the owner's fix OR because the"
echo "# clone was cut from an older baseline (e.g. dev_footbridge.c before #545) or is a divergence-set path -- which is"
echo "# which is the OWNER's call; nothing here asserts it."
echo "# columns: md5  bytes  mtime  source -> copy"
} > "$M"
for C in /tmp/gx541 /tmp/gx542; do
  n=$(basename "$C")
  for f in $(cd "$C" && find src -type f \( -name '*.c' -o -name '*.h' \) | sort); do
    [ -f "$S/$f" ] && cmp -s "$C/$f" "$S/$f" && continue
    mkdir -p "$D/clones/$n/$(dirname "$f")"
    cp -p "$C/$f" "$D/clones/$n/$f"
    echo "$(md5sum "$C/$f" | cut -c1-32)  $(stat -c %s "$C/$f")  $(stat -c %y "$C/$f" | cut -c1-19)  $C/$f -> clones/$n/$f" >> "$M"
  done
  echo "$(md5sum "$C/gxemul" | cut -c1-32)  $(stat -c %s "$C/gxemul")  $(stat -c %y "$C/gxemul" | cut -c1-19)  $C/gxemul  (binary NOT copied; md5 recorded only)" >> "$M"
done
for w in w541 w540 waifk; do
  (cd "$P" && find "$w" -type f ! -name '*.raw' ! -name '*.pyc' ! -path '*/__pycache__/*' -print0) | while IFS= read -r -d '' f; do
    mkdir -p "$D/scratch/$(dirname "$f")"
    cp -p "$P/$f" "$D/scratch/$f"
    echo "$(md5sum "$P/$f" | cut -c1-32)  $(stat -c %s "$P/$f")  $(stat -c %y "$P/$f" | cut -c1-19)  _scratchpad/$f -> scratch/$f" >> "$M"
  done
done
(cd "$P" && find w544 -maxdepth 1 -type f ! -name '*.pyc' -print0) | while IFS= read -r -d '' f; do
  mkdir -p "$D/scratch/w544"
  cp -p "$P/$f" "$D/scratch/$f"
  echo "$(md5sum "$P/$f" | cut -c1-32)  $(stat -c %s "$P/$f")  $(stat -c %y "$P/$f" | cut -c1-19)  _scratchpad/$f -> scratch/$f  (w544 top level only; its subdirs are sweep copies, 133 MB)" >> "$M"
done
# verify every copy byte-for-byte against its source
bad=0; tot=0
while read -r md5 sz mt src arrow dst rest; do
  case "$md5" in \#*) continue;; esac
  [ "$arrow" = "->" ] || continue
  tot=$((tot+1))
  case "$src" in _scratchpad/*) s="$P/${src#_scratchpad/}";; *) s="$src";; esac
  cmp -s "$s" "$D/$dst" || { bad=$((bad+1)); echo "MISMATCH $src"; }
done < "$M"
echo "copied and verified: $tot files, mismatches: $bad"
du -sh "$D" | cut -f1
