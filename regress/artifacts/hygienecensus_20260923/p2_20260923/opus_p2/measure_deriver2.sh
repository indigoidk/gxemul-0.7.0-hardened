#!/bin/bash
# opus measuring seat -- deriver on two gate-level evasions: does --write see what the gate row cannot?
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
W=/tmp/opus_census0923
OUT=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus/runs
SNAP=$W/snap/regress
: > "$OUT/DERIVER2_SUMMARY.txt"
mkroot() { local r=$W/d/$1; rm -rf "$r"; mkdir -p "$r/GXEMUL-SEC/regress" "$r/GXEMUL-SEC/tools" "$r/logs"
  cp -p "$SNAP/"* "$r/GXEMUL-SEC/regress/"; cp -p "$SEC/tools/derive_hygiene_pins.sh" "$r/GXEMUL-SEC/tools/"; printf '%s' "$r"; }
elide() { awk '/^UNTRACKED files/ {skip=1; next} skip && /^  / {n++; next} {skip=0; print} END {if (n) print "  [UNTRACKED block elided: " n " names]"}'; }
derive() { local tag=$1 r=$2; shift 2; local g=$r/GXEMUL-SEC/regress/gate_hygiene.sh
  cp -p "$g" "$r/gate.before.$tag"
  ( GXROOT=$r bash "$r/GXEMUL-SEC/tools/derive_hygiene_pins.sh" "$@" ) > "$OUT/$tag.derive" 2>&1; local rc=$?
  { echo "===== $tag: derive_hygiene_pins.sh $* -> rc=$rc"; elide < "$OUT/$tag.derive" | sed 's/^/   /'
    cmp -s "$r/gate.before.$tag" "$g" && echo "   gate file UNCHANGED" || { echo "   gate file CHANGED:"; diff "$r/gate.before.$tag" "$g" | sed 's/^/      /'; }
  } >> "$OUT/DERIVER2_SUMMARY.txt"; }
# e7 under the deriver: a new promptless pty probe whose FILE NAME holds a space
r=$(mkroot dE7_space_name); cp -p "$r/GXEMUL-SEC/regress/pcc2_width_probe.py" "$r/GXEMUL-SEC/regress/zz opus_newprobe.py"
derive dE7_write "$r" --write
# e14 under the deriver: a grandfathered promptless probe RENAMED
r=$(mkroot dE14_rename); mv "$r/GXEMUL-SEC/regress/gdrom_cond_probe.py" "$r/GXEMUL-SEC/regress/zz_renamed_cond_probe.py"
derive dE14_write "$r" --write
echo MEASURE_DERIVER2_DONE >> "$OUT/DERIVER2_SUMMARY.txt"; echo MEASURE_DERIVER2_DONE
