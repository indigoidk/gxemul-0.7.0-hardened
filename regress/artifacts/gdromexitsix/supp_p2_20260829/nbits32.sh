#!/bin/bash
#  THE SEAM BETWEEN THE TWO ASSERTS, at exactly GDROM_W_NBITS == 32.
#
#    gdrom_w_fits_its_carriers  admits 32  (32 <= 8*sizeof(uint32_t) and 32 <= 8*sizeof(1u))
#    gdrom_w_masks_disjoint     evaluates (1u << 32), which is UNDEFINED
#
#  So the capacity guard says "fits" at the exact width where the disjointness
#  guard's own right-hand side stops being defined.  What does the compiler do?
set -u
T=/tmp/gdromseam; rm -rf "$T"; mkdir -p "$T"

gen () {  # $1 outfile, $2 NBITS
python3 - "$1" "$2" <<'PYEOF'
import io, sys
p, n = sys.argv[1], int(sys.argv[2])
L = ["#include <stdint.h>", "enum {"]
for i in range(n):
    L.append("\tB%d," % i)
L.append("\tGDROM_W_NBITS")
L.append("};")
L.append("struct dreamcast_gdrom_data { uint32_t warned; };")
L.append("typedef char gdrom_w_fits_its_carriers[")
L.append("    (GDROM_W_NBITS <= 8 * sizeof(((struct dreamcast_gdrom_data *)0)->warned) &&")
L.append("     GDROM_W_NBITS <= 8 * sizeof(1u)) ? 1 : -1];")
ors = " | ".join("(1u << B%d)" % i for i in range(n))
L.append("typedef char gdrom_w_masks_disjoint[")
L.append("    ((%s) == ((1u << GDROM_W_NBITS) - 1u)) ? 1 : -1];" % ors)
L.append("int main(void) { return 0; }")
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(L))
PYEOF
}

for n in 9 31 32 33; do
  gen "$T/t.c" "$n"
  out=$(gcc -std=gnu99 -pedantic-errors -Wall -Wextra -c "$T/t.c" -o "$T/t.o" 2>&1)
  if [ -z "$out" ]; then st="CLEAN"; else
    if echo "$out" | grep -q "error:"; then st="ERROR"; else st="WARN-ONLY"; fi
  fi
  printf '  NBITS=%-3s  %-10s  %s\n' "$n" "$st" \
     "$(echo "$out" | grep -m2 -oE "(error|warning): .*" | tr '\n' ' ' | cut -c1-110)"
done
echo "SEAM_DONE"
