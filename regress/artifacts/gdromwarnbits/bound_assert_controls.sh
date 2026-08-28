#!/bin/bash
#  Negative controls for gdrom_w_fits_its_carriers.  SCRATCH ONLY.
#  Layout MIRRORS the real tree because src/include/cpu.h does #include "../../config.h".
R=/mnt/c/DocumentNoSnc/cc/GXEMUL
S=$R/GXEMUL-SEC/src
W=/tmp/gdromassert3
rm -rf $W; mkdir -p $W/src/devices
cp $R/build/config.h $W/config.h
cp -r $S/include $W/src/include
ORIG=$W/orig.c
cp $S/devices/dev_dreamcast_gdrom.c $ORIG
T=$W/src/devices/t.c
CC="cc -std=c99 -Wall -Wextra -Wno-unused-parameter -I$W/src/include"

try () {   # $1 label   $2 want(clean|error)
    if $CC -c -o /dev/null $T 2>$W/err.txt; then got=clean; else got=error; fi
    if [ "$got" = "$2" ]; then r="ok"; else r="*** FAIL ***"; fi
    printf '%-48s got=%-6s want=%-6s %s\n' "$1" "$got" "$2" "$r"
    #  ALWAYS show why on a surprise; the first version of this script only
    #  grepped for the error it EXPECTED, so an unrelated failure read as a pass.
    if [ "$got" != "$2" ]; then head -6 $W/err.txt | sed 's/^/        /'; fi
    if [ "$got" = error ] && [ "$2" = error ]; then
        grep -m1 "gdrom_w_fits" $W/err.txt | sed 's/^/        /'
    fi
}

echo "=== C1  POSITIVE CONTROL: shipped source, 6 bits over uint32_t ==="
cp $ORIG $T
try "shipped: must COMPILE" clean

echo "=== C2  clause 1: 9 bits over uint8_t  (the one-token revert of #484's field) ==="
cp $ORIG $T
sed -i 's/^\tuint32_t\twarned;/\tuint8_t\t\twarned;/' $T
sed -i 's/^\tGDROM_W_NBITS$/\tGDROM_W_X7_B,\n\tGDROM_W_X8_B,\n\tGDROM_W_X9_B,\n\tGDROM_W_NBITS/' $T
grep -q 'uint8_t.*warned' $T || echo "        !! FIELD MUTATION DID NOT APPLY"
grep -q 'GDROM_W_X9_B'    $T || echo "        !! ENUM MUTATION DID NOT APPLY"
try "9 bits over uint8_t: must ERROR" error

echo "=== C3  clause 1 satisfied: 9 bits over the shipped uint32_t ==="
cp $ORIG $T
sed -i 's/^\tGDROM_W_NBITS$/\tGDROM_W_X7_B,\n\tGDROM_W_X8_B,\n\tGDROM_W_X9_B,\n\tGDROM_W_NBITS/' $T
grep -q 'GDROM_W_X9_B' $T || echo "        !! ENUM MUTATION DID NOT APPLY"
try "9 bits over uint32_t: must COMPILE" clean

echo "=== C4  clause 2 ALONE: 40 bits over uint64_t -- the single-clause form PASSES this ==="
cp $ORIG $T
sed -i 's/^\tuint32_t\twarned;/\tuint64_t\twarned;/' $T
python3 - "$T" <<'PY'
import sys
p=sys.argv[1]; s=open(p).read()
extra="".join("\tGDROM_W_P%d_B,\n"%i for i in range(7,41))
assert "\tGDROM_W_NBITS\n" in s
s=s.replace("\tGDROM_W_NBITS\n", extra+"\tGDROM_W_NBITS\n",1)
open(p,'w').write(s)
PY
grep -q 'GDROM_W_P40_B' $T || echo "        !! 40-BIT MUTATION DID NOT APPLY"
grep -q 'uint64_t.*warned' $T || echo "        !! FIELD MUTATION DID NOT APPLY"
try "40 bits over uint64_t: must ERROR (1u shift)" error

echo "=== C5  33 bits over uint32_t: both clauses bite ==="
cp $ORIG $T
python3 - "$T" <<'PY'
import sys
p=sys.argv[1]; s=open(p).read()
extra="".join("\tGDROM_W_Q%d_B,\n"%i for i in range(7,34))
s=s.replace("\tGDROM_W_NBITS\n", extra+"\tGDROM_W_NBITS\n",1)
open(p,'w').write(s)
PY
grep -q 'GDROM_W_Q33_B' $T || echo "        !! 33-BIT MUTATION DID NOT APPLY"
try "33 bits over uint32_t: must ERROR" error
