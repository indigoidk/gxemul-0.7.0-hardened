#!/bin/bash
# bash -n on the frozen gate scripts, and gate_offline's three SM-manifest assertions evaluated
# (grep/loop logic only) against the FROZEN file and the working-tree diff_*.c set.
set -u
F=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/p2_536_537/frozen
HERE=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress
bash -n "$F/gate_offline.sh" && echo "bash -n gate_offline.sh: OK"
bash -n "$F/gate_arm.staged.sh" && echo "bash -n gate_arm.staged.sh: OK"
eval "$(grep -E '^SM_COVERED=|^SM_EXEMPT=' "$F/gate_offline.sh")"
sm_missing=""
for f in "$HERE"/diff_*.c; do stem=$(basename "$f" .c); stem=${stem#diff_}; _found=no
  for _c in $SM_COVERED; do [ "$_c" = "$stem" ] && _found=yes; done
  for _e in $SM_EXEMPT; do [ "${_e%%:*}" = "$stem" ] && _found=yes; done
  [ "$_found" = yes ] || sm_missing="$sm_missing $stem"; done
echo "every differential covered or exempt: ${sm_missing:-none}"
sm_unbacked=""
for _stem in $SM_COVERED; do grep -qE "^selfmutant_one +[^ ]+ +[^ ]+ +$_stem +" "$F/gate_offline.sh" || sm_unbacked="$sm_unbacked $_stem"; done
echo "every COVERED stem has a selfmutant_one call: ${sm_unbacked:-none}"
echo "SM_EXEMPT now: $SM_EXEMPT"
echo "the stray line is gone: $(grep -c "^' ' ')" "$F/gate_offline.sh")"
