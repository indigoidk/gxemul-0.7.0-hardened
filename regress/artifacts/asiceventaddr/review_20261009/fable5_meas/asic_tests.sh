#!/bin/bash
# fable5 late-review seat, asiceventaddr (#466 / #468 / #469).  SCRATCH ONLY.
# Includes the REAL header read-only; writes nothing outside $SD.
set -u
SD=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fableq/asictest
HDIR=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/include/thirdparty
HDR=$HDIR/dreamcast_sysasicvar.h
mkdir -p "$SD" && cd "$SD" || exit 9
OUT=$SD/asic_tests.out
: > "$OUT"
say() { echo "$@" | tee -a "$OUT"; }

say "gcc: $(gcc --version | head -1)"
say "g++: $(g++ --version 2>/dev/null | head -1 || echo none)"
say "header md5: $(md5sum "$HDR" | cut -c1-12)  $(wc -l < "$HDR") lines"
say "default __STDC_VERSION__: $(echo __STDC_VERSION__ | gcc -E -P - | tail -1)"

say "--- T0 event census, derived from the header (object-like SYSASIC_EVENT_* with a numeric value) ---"
grep -E '^#define[[:space:]]+SYSASIC_EVENT_[A-Z0-9_]+[[:space:]]+(0x[0-9a-fA-F]+|[0-9]+)' "$HDR" \
  | awk '{printf "%s=%s ", $2, $3} END {print ""}' | tee -a "$OUT"
say "count=$(grep -cE '^#define[[:space:]]+SYSASIC_EVENT_[A-Z0-9_]+[[:space:]]+(0x[0-9a-fA-F]+|[0-9]+)' "$HDR")"
say "values with (e & 31) == 31: $(grep -E '^#define[[:space:]]+SYSASIC_EVENT_[A-Z0-9_]+[[:space:]]+[0-9]+' "$HDR" | awk '($3 % 32) == 31 {print $2"="$3}' | tr '\n' ' ')(end)"
say "max value: $(grep -E '^#define[[:space:]]+SYSASIC_EVENT_[A-Z0-9_]+[[:space:]]+[0-9]+' "$HDR" | awk '{if ($3+0 > m) m=$3+0} END {print m}')"

# ---------- sources ----------
cat > t_ok.c <<'EOF'
#include <stdio.h>
#include <stdint.h>
#include "dreamcast_sysasicvar.h"
#define UNGUARDED_ADDR(e) (SYSASIC_BASE + 4*((e)>>5))
#define EV(n) printf("%-28s %3d addr=0x%06x unguarded=0x%06x same=%d mask=0x%08x\n", #n, (int)(n), \
    (unsigned)SYSASIC_EVENT_TO_ADDR(n), (unsigned)UNGUARDED_ADDR(n), \
    (int)(SYSASIC_EVENT_TO_ADDR(n) == UNGUARDED_ADDR(n)), (unsigned)SYSASIC_EVENT_TO_BITMASK(n))
int main(void) {
  EV(SYSASIC_EVENT_RENDERDONE); EV(SYSASIC_EVENT_PVR_SCANINT1); EV(SYSASIC_EVENT_PVR_SCANINT2);
  EV(SYSASIC_EVENT_VBLINT); EV(SYSASIC_EVENT_OPAQUEDONE); EV(SYSASIC_EVENT_OPAQUEMODDONE);
  EV(SYSASIC_EVENT_TRANSDONE); EV(SYSASIC_EVENT_TRANSMODDONE); EV(SYSASIC_EVENT_MAPLE_DMADONE);
  EV(SYSASIC_EVENT_MAPLE_ERROR); EV(SYSASIC_EVENT_GDROM_DMA); EV(SYSASIC_EVENT_SPU_DMA);
  EV(SYSASIC_EVENT_SPU_IRQ); EV(SYSASIC_EVENT_PVR_DMA); EV(SYSASIC_EVENT_PVR_PTDONE);
  EV(SYSASIC_EVENT_GDROM); EV(SYSASIC_EVENT_AICA); EV(SYSASIC_EVENT_8BIT); EV(SYSASIC_EVENT_EXT);
  EV(SYSASIC_EVENT_PRIMOUTOFMEM); EV(SYSASIC_EVENT_MATOUTOFMEM);
  { uint64_t a = SYSASIC_EVENT_TO_ADDR(0), b = SYSASIC_EVENT_TO_ADDR(95);
    printf("domain ends: e=0 -> 0x%llx   e=95 -> 0x%llx\n", (unsigned long long)a, (unsigned long long)b); }
  return 0;
}
EOF

cat > t_c89.c <<'EOF'
#include "dreamcast_sysasicvar.h"
int main(void) { int a = SYSASIC_EVENT_TO_ADDR(95); int b = SYSASIC_EVENT_TO_ADDR(0);
  return (a == 0x5f6908 && b == 0x5f6900) ? 0 : 1; }
EOF

cat > t_96.c <<'EOF'
#include "dreamcast_sysasicvar.h"
#define SYSASIC_EVENT_FOO 96
int main(void) { int a = SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_FOO); return a; }
EOF

cat > t_neg1.c <<'EOF'
#include "dreamcast_sysasicvar.h"
int main(void) { int a = SYSASIC_EVENT_TO_ADDR(-1); return a; }
EOF

cat > t_runtime.c <<'EOF'
#include "dreamcast_sysasicvar.h"
int main(int argc, char **argv) { int e = argc; (void)argv; int a = SYSASIC_EVENT_TO_ADDR(e); return a; }
EOF

cat > t_constint.c <<'EOF'
#include "dreamcast_sysasicvar.h"
int main(void) { const int e = 95; int a = SYSASIC_EVENT_TO_ADDR(e); return a; }
EOF

cat > t_enum_ok.c <<'EOF'
#include "dreamcast_sysasicvar.h"
enum { EV_LAST_LEGAL = 95 };
int main(void) { int a = SYSASIC_EVENT_TO_ADDR(EV_LAST_LEGAL); return a == 0x5f6908 ? 0 : 1; }
EOF

cat > t_enum_bad.c <<'EOF'
#include "dreamcast_sysasicvar.h"
enum { EV_FIRST_ILLEGAL = 96 };
int main(void) { int a = SYSASIC_EVENT_TO_ADDR(EV_FIRST_ILLEGAL); return a; }
EOF

# the ledger's 2026-09-17 remedy: give BITMASK the same + RANGE_OK(e)
cat > t_remedy31.c <<'EOF'
#include <stdint.h>
#include "dreamcast_sysasicvar.h"
#define BITMASK_WITH_RANGE_OK(e) ((1 << ((e) & 31)) + SYSASIC_EVENT_RANGE_OK(e))
int main(void) { uint64_t t = BITMASK_WITH_RANGE_OK(31); return (int)(t & 1); }
EOF
cat > t_remedy96.c <<'EOF'
#include <stdint.h>
#include "dreamcast_sysasicvar.h"
#define BITMASK_WITH_RANGE_OK(e) ((1 << ((e) & 31)) + SYSASIC_EVENT_RANGE_OK(e))
int main(void) { uint64_t t = BITMASK_WITH_RANGE_OK(96); return (int)(t & 1); }
EOF

# UB probe: the shipped BITMASK at e == 31 (in-domain), signed vs unsigned, constant and non-constant
cat > t_ub.c <<'EOF'
#include <stdio.h>
#include <stdint.h>
#include "dreamcast_sysasicvar.h"
int main(int argc, char **argv) {
  volatile int k = 31; (void)argv; if (argc > 5) k = 0;
  uint64_t c = SYSASIC_EVENT_TO_BITMASK(31);            /* constant e, the shipped macro */
  uint64_t v = (1 << ((k) & 31));                       /* same expression, non-constant e */
  uint64_t u = (1U << ((k) & 31));                      /* the one-token repair */
  c |= 0x100000000ULL; v |= 0x100000000ULL; u |= 0x100000000ULL;
  printf("tmp2 shipped(const 31)=0x%016llx  shipped(volatile 31)=0x%016llx  1U-form=0x%016llx  low32: 0x%08x 0x%08x 0x%08x\n",
    (unsigned long long)c, (unsigned long long)v, (unsigned long long)u, (unsigned)c, (unsigned)v, (unsigned)u);
  return 0;
}
EOF

cat > t_cxx.cc <<'EOF'
#include <stdint.h>
#include "dreamcast_sysasicvar.h"
int main() { uint64_t a = SYSASIC_EVENT_TO_ADDR(95); return (int)(a & 1); }
EOF

# ---------- runner ----------
try() { # name expect(ok|err) file flags...
  local name=$1 expect=$2 file=$3; shift 3
  local rc
  if gcc "$@" -I"$HDIR" "$file" -o "$name.bin" > "$name.log" 2>&1; then rc=ok; else rc=err; fi
  local mark=PASS; [ "$rc" = "$expect" ] || mark='*** UNEXPECTED ***'
  say "T[$name] expect=$expect got=$rc $mark   flags: $*"
  if [ -s "$name.log" ]; then grep -m3 -E 'error|warning' "$name.log" | sed 's/^/      /' | tee -a "$OUT"; fi
}

say "--- T1 legal domain compiles, all 21 events byte-identical with/without the guard ---"
try ok_default ok t_ok.c -Wall -Wextra -O0
./ok_default.bin | tee -a "$OUT"
try ok_c99pe ok t_ok.c -std=c99 -pedantic-errors -Wall -Wextra -O0
try c89pe ok t_c89.c -std=c89 -pedantic-errors -Wall -Wextra -O0
./c89pe.bin; say "c89 binary rc=$? (0 = both domain ends give the expected addresses)"
try enum_ok ok t_enum_ok.c -std=c99 -pedantic-errors -Wall -Wextra -O0
./enum_ok.bin; say "enum_ok rc=$?"

say "--- T2/T3 both ends refuse: 96 and -1 ---"
try e96 err t_96.c -Wall -Wextra -O0
try e96_c99 err t_96.c -std=c99 -pedantic-errors -Wall -Wextra -O0
try neg1 err t_neg1.c -Wall -Wextra -O0
try enum_bad err t_enum_bad.c -std=c99 -pedantic-errors -Wall -Wextra -O0

say "--- T4 a non-constant e is a HARD ERROR, not a silent runtime degrade ---"
try runtime err t_runtime.c -Wall -Wextra -O0
try constint err t_constint.c -std=c99 -pedantic-errors -Wall -Wextra -O0

say "--- T5 the ledger's remedy (+ RANGE_OK on BITMASK): inert at e=31 (in-domain), refuses 96 (already refused by ADDR at every call site) ---"
try remedy31 ok t_remedy31.c -std=c99 -pedantic-errors -Wall -Wextra -O0
try remedy96 err t_remedy96.c -std=c99 -pedantic-errors -Wall -Wextra -O0

say "--- T6 the in-domain 1 << 31 in BITMASK: diagnostics and UBSan ---"
try ub_warn ok t_ub.c -std=c99 -Wall -Wextra -Wshift-overflow=2 -O0
try ub_pedantic ok t_ub.c -std=c99 -pedantic -Wall -Wextra -O0
try ub_san ok t_ub.c -std=c99 -O0 -g -fsanitize=undefined
say "ub_san run:"; ./ub_san.bin 2>&1 | tee -a "$OUT"; say "ub_san rc=${PIPESTATUS[0]}"
try ub_asanflags ok t_ub.c -O1 -g -fno-omit-frame-pointer -fsanitize=address,undefined
say "ub_asanflags run (the build-asan CFLAGS):"; ./ub_asanflags.bin 2>&1 | tee -a "$OUT"; say "rc=${PIPESTATUS[0]}"

say "--- T7 C++ (informational: no C++ includer exists in the tree) ---"
if command -v g++ >/dev/null 2>&1; then
  if g++ -I"$HDIR" t_cxx.cc -o cxx.bin > cxx.log 2>&1; then say "T[cxx] compiles under g++"; else say "T[cxx] g++ REFUSES:"; grep -m2 error cxx.log | sed 's/^/      /' | tee -a "$OUT"; fi
else say "T[cxx] no g++ on this box"; fi

say "ASIC_TESTS_DONE"
