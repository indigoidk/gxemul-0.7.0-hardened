#!/bin/bash
#  Negative controls for gate_ppc.sh's rlwimi/rldimi section (#527).  The section is EXTRACTED from the gate
#  itself (between its `# ---- ppcrlwimiwidth' header and the NetBSD need_file), its two probe invocations are
#  replaced by copies of a fixture log, and it runs under stub check/note functions that count failures.
#  Fixtures are derived from kill table 3's real BASE logs.  Every doctored case must produce >= 1 FAIL and the
#  untouched case must produce 0 -- otherwise the section's parse-before-score guard is not doing its job.
cd "$(dirname "$0")/../.." || exit 9          # regress/
G=gate_ppc.sh
K=artifacts/ppcrlwimiwidth/killtable3_20260912
T=$(mktemp -d)
awk '/^# ---- ppcrlwimiwidth:/{on=1} on&&/^need_file "\$IMAGES\/netbsd401-macppc-GENERIC"/{exit} on{print}' "$G" > "$T/section.sh"
n=$(grep -c 'python3 ppc_rl[wd]imi_probe.py' "$T/section.sh")
[ "$n" = 2 ] || { echo "EXTRACT FAILED: $n probe invocations found (want 2)"; exit 9; }
sed -i 's#^python3 ppc_rlwimi_probe.py .*#cp "$FIX_W" "$RLWLOG"#; s#^python3 ppc_rldimi_probe.py .*#cp "$FIX_D" "$RLDLOG"#' "$T/section.sh"
cat > "$T/stubs.sh" <<'EOF'
FAILS=0
check() { if [ "$2" = "$3" ]; then :; else FAILS=$((FAILS+1)); echo "      FAIL $1 got=$2 want=$3"; fi; }
note() { :; }
EOF
run() {   # $1 label, $2 rlwimi fixture, $3 rldimi fixture, $4 expect (PASS|FAIL)
    ( LOGDIR="$T/logs_$1"; mkdir -p "$LOGDIR"; FIX_W="$2"; FIX_D="$3"
      . "$T/stubs.sh"; . "$T/section.sh" > "$T/out_$1" 2>&1
      got=PASS; [ "$FAILS" -gt 0 ] && got=FAIL
      verdict=WRONG; [ "$got" = "$4" ] && verdict=ok
      printf '%-28s fails=%-3s got=%-4s want=%-4s %s\n' "$1" "$FAILS" "$got" "$4" "$verdict"
      grep ' FAIL ' "$T/out_$1" | head -3 )
}
W=$K/probe_rlwimi_BASE.raw; D=$K/probe_rldimi_BASE.raw
mk() { sed "$2" "$1" > "$T/$3"; echo "$T/$3"; }
run GOOD                   "$W" "$D" PASS
run W_SHRUNK_27of27        "$(mk "$W" 's#^PPC_RLWIMI_RESULT=.*#PPC_RLWIMI_RESULT=27/27#' w1)" "$D" FAIL
run D_SHRUNK_28of28        "$W" "$(mk "$D" 's#^PPC_RLDIMI_RESULT=.*#PPC_RLDIMI_RESULT=28/28#' d1)" FAIL
run W_ONE_RED_27of28       "$(mk "$W" 's#^PPC_RLWIMI_RESULT=.*#PPC_RLWIMI_RESULT=27/28#' w2)" "$D" FAIL
run W_DUPLICATE_RESULT     "$(mk "$W" '/^PPC_RLWIMI_RESULT=/p' w3)" "$D" FAIL
run D_MALFORMED_EXTRA      "$W" "$(mk "$D" '/^PPC_RLDIMI_RESULT=/a PPC_RLDIMI_RESULT=29/29x' d2)" FAIL
run W_MISSING_DONE         "$(mk "$W" '/^PPC_RLWIMI_PROBE_DONE/d' w4)" "$D" FAIL
run D_MISSING_RESULT       "$W" "$(mk "$D" '/^PPC_RLDIMI_RESULT=/d' d3)" FAIL
run W_CONTROL_FAIL         "$(mk "$W" 's#^PPC_RLWIMI_CONTROL=OK#PPC_RLWIMI_CONTROL=FAIL#' w5)" "$D" FAIL
run D_DUPLICATE_CONTROL    "$W" "$(mk "$D" '/^PPC_RLDIMI_CONTROL=/p' d4)" FAIL
run D_EMPTY_LOG            "$W" /dev/null FAIL
rm -rf "$T"
echo NEGCTL_DONE
