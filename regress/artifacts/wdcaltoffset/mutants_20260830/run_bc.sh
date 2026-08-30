#!/bin/bash
#
#  wdcaltoffset -- TABLE B (the read side) and TABLE C (is m3's escape a real defect?).
#  Both reuse the binaries run_mutants.sh already built and verified; nothing is
#  rebuilt here, so this script measures and never mutates.
#
#    MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash \
#      /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/wdcaltoffset/mutants_20260830/run_bc.sh
#
set -u
SEC=${GXSEC:-/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC}
ART="$SEC/regress/artifacts/wdcaltoffset/mutants_20260830"
O=${OUT:-/tmp/gxaltoff2}
IMG="$O/altoff-scratch.img"
CDIMG="$O/altoff-cd.img"

#  THE BINARIES MUST BE THE ONES TABLE A MEASURED.  A table that silently rebuilt, or
#  that measured a leftover from an earlier round, is the stale-binary trap.
echo "---- the binaries this table will measure ----"
MISS=0
for l in base fix m1 m2 m3 m4; do
    if [ -x "$O/$l/gxemul" ]; then
        echo "  $l  $(stat -c '%s bytes  %y' "$O/$l/gxemul")"
    else
        echo "  *** $l/gxemul MISSING -- run run_mutants.sh first"; MISS=1
    fi
done
[ "$MISS" = 0 ] || { echo "TABLES_BC_ABORTED"; exit 1; }
echo

mkdir -p "$O/runbc"
[ -f "$CDIMG" ] || dd if=/dev/zero of="$CDIMG" bs=1M count=8 status=none

#  ---- TABLE B: the read side.  The read path is identical on every leg by
#  construction, so running all six is itself a control on that claim.
python3 -u "$ART/table_b.py" "$O/runbc" "$IMG" \
    base="$O/base/gxemul" fix="$O/fix/gxemul" m1="$O/m1/gxemul" \
    m2="$O/m2/gxemul" m3="$O/m3/gxemul" m4="$O/m4/gxemul" \
    2>&1 | tee "$O/runbc/console_b.log"

echo
#  ---- TABLE C: only the three legs that can differ on the signature channel.
python3 -u "$ART/table_c.py" "$O/runbc" "$CDIMG" \
    base="$O/base/gxemul" fix="$O/fix/gxemul" m3="$O/m3/gxemul" \
    2>&1 | tee "$O/runbc/console_c.log"

#  ---- preserve, VERIFIED BY THE COMPLETION SENTINEL, never by existence ----
for f in "$O/runbc/TABLE_B.txt:TABLE_B_DONE" "$O/runbc/TABLE_C.txt:TABLE_C_DONE"; do
    p=${f%:*}; want=${f#*:}
    if [ ! -f "$p" ]; then echo "  *** $p never written -- NOT preserved"
    elif [ "$(tail -1 "$p")" != "$want" ]; then
        echo "  *** $p does not end in $want -- truncated, NOT preserved"
    else cp "$p" "$ART/$(basename "$p")"
         echo "  preserved $(basename "$p") ($(stat -c %s "$p") bytes, sentinel ok)"; fi
done
for t in base fix m3; do
    cp "$O/runbc/transcript_sig_$t.log" "$ART/transcript_sig_$t.log" 2>/dev/null
done
echo "TABLES_BC_DONE"
