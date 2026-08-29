#!/bin/bash
#  #491 verification, TAKE 2.
#
#  Take 1 was VACUOUS and its own negative control said so: the pre-fix form
#  produced 0 warnings where it must produce 2.  The cause was that the script
#  never checked whether the COMPILE SUCCEEDED -- it grepped output from a
#  command that may not have run.  Same denominator failure as the phantom
#  absence class: a grep over nothing returns 0 and looks like a measurement.
#
#  This version reports compile status FIRST and refuses to read the warning
#  count unless the compile actually produced an object.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
#  The build's real flags, read from build/Makefile:8 rather than guessed.
W="-Wshadow -Wcast-align -Wstrict-aliasing -Wall -Wextra -Wno-unused-parameter -Wno-cast-align"
INC="-I$SEC/src/include -I$SEC/src/include/machines"

compile () {   # $1 = source, $2 = object, prints "rc=N obj=BYTES warn=N"
	local out rc bytes warn
	out=$(gcc -std=gnu99 $W -O3 -DNDEBUG $INC -c "$1" -o "$2" 2>&1)
	rc=$?
	bytes=0; [ -f "$2" ] && bytes=$(stat -c%s "$2")
	warn=$(printf '%s\n' "$out" | grep -cE 'diskimage\.c:[0-9]+:[0-9]+:.*sign-compare')
	printf 'rc=%s obj=%s warn_signcompare=%s\n' "$rc" "$bytes" "$warn"
	printf '%s\n' "$out" | grep -E 'error:' | head -3 | sed 's/^/      ERR /'
	printf '%s\n' "$out" | grep -E 'sign-compare' | head -4 | sed 's/^/      W   /'
}

echo "=== NEGATIVE CONTROL FIRST -- if this does not warn, everything below is vacuous ==="
mkdir -p /tmp/d491pre
sed 's/lentoread = len > (size_t) remain? remain : (off_t) len;/lentoread = len > remain? remain : len;/' \
    "$SEC/src/disk/diskimage.c" > /tmp/d491pre/diskimage.c
if cmp -s /tmp/d491pre/diskimage.c "$SEC/src/disk/diskimage.c"; then
	echo "  *** SED MATCHED NOTHING -- control is vacuous, STOP ***"
	exit 1
fi
echo -n "  pre-fix form : "
compile /tmp/d491pre/diskimage.c /tmp/d491pre.o

echo
echo "=== POST-FIX: the shipped source ==="
echo -n "  shipped      : "
compile "$SEC/src/disk/diskimage.c" /tmp/d491post.o

rm -rf /tmp/d491pre /tmp/d491pre.o /tmp/d491post.o
echo
echo "VERIFY491B_DONE"
