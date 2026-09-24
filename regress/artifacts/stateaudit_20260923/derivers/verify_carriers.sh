#!/bin/bash
S=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
P=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad
D=$S/regress/artifacts/stateaudit_20260923/peer_carriers
bad=0; tot=0; skipped=0
while read -r md5 sz d t src arrow dst rest; do
  case "$md5" in \#*) continue;; esac
  if [ "$arrow" != "->" ]; then skipped=$((skipped+1)); continue; fi
  tot=$((tot+1))
  case "$src" in _scratchpad/*) s="$P/${src#_scratchpad/}";; *) s="$src";; esac
  if ! cmp -s "$s" "$D/$dst"; then bad=$((bad+1)); echo "MISMATCH $src"; fi
  [ "$(md5sum "$D/$dst" | cut -c1-32)" = "$md5" ] || { bad=$((bad+1)); echo "MD5 MISMATCH $dst"; }
done < "$D/MANIFEST.txt"
echo "verified: $tot copies, mismatches: $bad, non-copy lines skipped: $skipped (the two binary md5 records)"
echo "copies on disk: $(find $D -type f ! -name MANIFEST.txt | wc -l)"
