#!/bin/bash
# m1_argv.sh -- under GIT-BASH: which of the strings the deriver hands a Windows python does MSYS rewrite?
# Each string goes through `command python - ARG <<'PY'` exactly as pywrite/astcall pass them; python writes back
# repr(argv) to a utf-8 file; compare with what was sent.
set -u
O=/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_c6/out/M1.txt; : > "$O"
. /c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_c6/lib6.sh
NEED=" EXPECT_WHOLE_FULL(3->5) WHOLE_FULL_FILES([arm_bdt_probe.py:1 arm_flags_probe.py:2]->[arm_bdt_probe.py:1 arm_flags_probe.py:2 newsub/zz_sub_probe.py:2])"
i=0
for s in "$R1" "$R2" "$R3" "$R4" "$R5" "$R6" \
         "arm_bdt_probe.py:1 arm_flags_probe.py:2 newsub/zz_sub_probe.py:2" "newsub/a.py:1" "$NEED" \
         "newsub/zz_probe.py" "grandfather" "zz-legit_probe.py" "5" "" \
         "2026-09-23: x=/usr/bin and y=/tmp sixteen letters" "2026-09-23: see /tmp/a:/tmp/b sixteen letters" \
         "/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gate_hygiene.sh"; do
  i=$((i+1)); T=$(mktemp)
  command python - "$T" "$s" <<'PY'
import io, sys
io.open(sys.argv[1], "w", encoding="utf-8", newline="\n").write(sys.argv[2])
PY
  got=$(cat "$T"); rm -f "$T"
  if [ "$got" = "$s" ]; then echo "M1.$i verbatim   [$s]" >> "$O"; else echo "M1.$i CONVERTED [$s] -> [$got]" >> "$O"; fi
done
echo M1_DONE >> "$O"; cat "$O"
