#!/bin/bash
#  Does the new disjointness assert emit any object code?
#
#  The file's EXISTING assert documents this check and its method: compare the
#  objects "with the filename held constant", because __LINE__ immediates shift
#  when a comment block is inserted.  So: build the live file, then build a copy
#  with ONLY the typedef removed (comment left in place, so no lines move), and
#  diff the objects.  Same filename both times.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
BLD=/mnt/c/DocumentNoSnc/CC/GXEMUL/build
T=/tmp/gdromobj
rm -rf "$T"; mkdir -p "$T"
INC="-I $BLD -I $SEC/src/include -I $SEC/src/include/thirdparty"

#  A: the live file.
cp "$SEC/src/devices/dev_dreamcast_gdrom.c" "$T/same.c"
gcc -O2 -std=gnu99 -c "$T/same.c" -o "$T/with.o" $INC 2>"$T/ea" || { echo "  A FAILED"; head -3 "$T/ea"; exit 1; }

#  B: same file, the typedef's three lines blanked so NO line numbers move.
python3 - "$T/same.c" <<'PYEOF'
import io, sys
p = sys.argv[1]
lines = io.open(p, encoding="utf-8").read().split(chr(10))
hit = [i for i, L in enumerate(lines) if L.startswith("typedef char gdrom_w_masks_disjoint[")]
assert len(hit) == 1, "want one typedef, got %d" % len(hit)
i = hit[0]
#  blank the declaration's four lines in place -- line COUNT preserved
for k in range(i, i + 4):
    lines[k] = ""
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(lines))
print("  (typedef blanked in place; line count preserved)")
PYEOF
gcc -O2 -std=gnu99 -c "$T/same.c" -o "$T/without.o" $INC 2>"$T/eb" || { echo "  B FAILED"; head -3 "$T/eb"; exit 1; }

echo
echo "=== object comparison, same filename, same line numbering ==="
echo "  with assert    : $(stat -c%s "$T/with.o") b   md5 $(md5sum "$T/with.o" | cut -c1-12)"
echo "  without assert : $(stat -c%s "$T/without.o") b   md5 $(md5sum "$T/without.o" | cut -c1-12)"
if cmp -s "$T/with.o" "$T/without.o"; then
  echo "  ==> BYTE-IDENTICAL.  The assert emits NO object code."
else
  echo "  ==> DIFFER in $(cmp -l "$T/with.o" "$T/without.o" 2>/dev/null | wc -l) bytes"
fi
echo
echo "OBJCHECK_DONE"
