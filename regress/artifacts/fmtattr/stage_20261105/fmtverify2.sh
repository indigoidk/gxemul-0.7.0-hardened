#!/bin/bash
# fmtverify2.sh -- HEAD's sources + ALL staged files (fmtfix/stage/src, misc.h's permanent GX_PRINTF attributes included), built
# in a scratch dir exactly as a user would build them; counts every compiler warning (gate 1 requires 0).  Usage: <head_tar>
set -u
D=/tmp/gxfmtv2_$$; O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/codescan/fmtfix; TAR=${1:?head tar}
{
echo "# $(date -u +%FT%TZ) fmtverify2: $TAR + fmtfix/stage (permanent attributes), scratch build in $D"
mkdir -p "$D" && tar -xf "$TAR" -C "$D" || { echo "EXTRACT FAILED"; exit 1; }
n=0; for f in $(cd "$O/stage" && find src -type f); do cp "$O/stage/$f" "$D/$f" && n=$((n+1)); done; echo "staged files overlaid: $n"
echo "misc.h GX_PRINTF uses (want 5: the definition's #else line excluded, 4 declarations + 1 #define with args): $(grep -c 'GX_PRINTF(' "$D/src/include/misc.h")"
( cd "$D" && ./configure > "$O/v2_configure.log" 2>&1 ); echo "configure rc=$?"
( cd "$D" && make -k -j4 > "$O/v2_make.log" 2>&1 ); echo "make rc=$?"
[ -x "$D/gxemul" ] && echo "binary built: yes" || echo "binary built: NO"
echo "ALL warnings: $(grep -c 'warning:' "$O/v2_make.log")   errors: $(grep -c ': error:' "$O/v2_make.log")"
# negative controls: one seeded mismatch per function must warn (proves each attribute is present and effective)
cat > "$D/fmtctl.c" <<'EOF'
#include <stdio.h>
#include <stdint.h>
struct cpu;
#include "misc.h"
void fmtctl(struct cpu *c) {
	debug("%i", (int64_t)1);
	fatal("%i", (int64_t)1);
	debugmsg(0, "x", 0, "%i", (int64_t)1);
	debugmsg_cpu(c, 0, "x", 0, "%i", (int64_t)1);
}
EOF
( cd "$D" && gcc -Wall -fsyntax-only -Isrc/include fmtctl.c > "$O/v2_ctl.log" 2>&1 ); echo "control compile rc=$?"
for fn in debug fatal debugmsg debugmsg_cpu; do
  printf 'control %-13s %s\n' "$fn" "$(grep -A1 -E "In function|fmtctl.c:[0-9]+" "$O/v2_ctl.log" | grep -c -E "fmtctl.c:[0-9]+:[0-9]+: warning: format .* \[-Wformat=\]" )"; done | head -1
echo "control warnings (want 4): $(grep -c -E 'fmtctl.c:[0-9]+:[0-9]+: warning: format .*\[-Wformat=\]' "$O/v2_ctl.log")"
echo "FMTVERIFY2_DONE"
rm -rf "$D"; [ -d "$D" ] && echo "SCRATCH NOT REMOVED" || echo "scratch removed"
} > "$O/fmtverify2.out" 2>&1
cat "$O/fmtverify2.out"
