#!/bin/bash
#  Compile the REAL dev_dreamcast_gdrom.c as a single TU, with the assert in it.
#  Read-only against the repo: the source is copied into a scratch dir, and the
#  include paths point at build/ which is not written to.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
BLD=/mnt/c/DocumentNoSnc/CC/GXEMUL/build
T=/tmp/gdromtu
rm -rf "$T"; mkdir -p "$T"

cp "$SEC/src/devices/dev_dreamcast_gdrom.c" "$T/live.c"

echo "=== 1. the REAL file, assert PRESENT -- must COMPILE ==="
if gcc -O2 -std=gnu99 -c "$T/live.c" -o "$T/live.o" \
      -I "$BLD" -I "$SEC/src/include" -I "$SEC/src/include/thirdparty" 2>"$T/e1"; then
  echo "  COMPILES ok   ($(stat -c%s "$T/live.o") b object)"
else
  echo "  *** FAILED ***"; head -6 "$T/e1" | sed 's/^/    /'
fi

echo
echo "=== 2. NEGATIVE CONTROL on the REAL file: alias FMT onto OVERREAD -- must REFUSE ==="
sed 's/^#define\tGDROM_W_FMT\t(1u << GDROM_W_FMT_B)/#define\tGDROM_W_FMT\t(1u << GDROM_W_OVERREAD_B)/' \
    "$T/live.c" > "$T/alias.c"
if ! cmp -s "$T/live.c" "$T/alias.c"; then
  echo "  (the alias edit applied)"
else
  echo "  *** the alias edit did NOT apply -- the test would be vacuous ***"
fi
if gcc -O2 -std=gnu99 -c "$T/alias.c" -o "$T/alias.o" \
      -I "$BLD" -I "$SEC/src/include" -I "$SEC/src/include/thirdparty" 2>"$T/e2"; then
  echo "  *** COMPILED -- THE ASSERT DID NOT FIRE ON THE REAL FILE ***"
else
  echo "  REFUSED ok"
  grep -m1 'gdrom_w_masks_disjoint' "$T/e2" | sed 's/^/    /'
fi

echo
echo "TUCHECK_DONE"
