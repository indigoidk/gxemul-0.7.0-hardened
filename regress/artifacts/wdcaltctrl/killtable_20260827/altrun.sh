#!/bin/bash
#  *** SUPERSEDED.  KEPT AS HISTORY, DO NOT RE-RUN.  Two defects, both of which this
#      round paid for once each:
#
#      1. IT REUSES ITS OUTPUT NAME.  Running it after the fix OVERWROTE the pre-fix
#         log, so the artifact preserved under that name showed the POST-fix result
#         wearing the pre-fix label.  Re-derived with prefixrun.sh, which writes to a
#         name no post-fix run uses.
#      2. ITS GREP NAMES A ROW THAT NO LONGER EXISTS.  `still signs` was renamed in
#         the re-cut, and a grep that matches nothing PRINTS NOTHING -- a re-runner
#         sees one fewer row with no error, no warning and no zero count.  That is the
#         pattern-matched-nothing class, inside a script preserved as evidence.
#
#      Use prefixrun.sh (pre-fix measurement) and killalt.sh (the table) instead.
#      The row name below is corrected so a reader who runs it anyway sees all of
#      them, but the reused output path is left AS IT WAS -- fixing it would erase
#      the evidence of what went wrong. ***
S=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
A=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/alt
O=/tmp/gxalt; mkdir -p "$O"
gcc -O2 -std=c99 -I"$S/src/include" -I"$S/src/include/thirdparty" \
    -ffunction-sections -fdata-sections -Wl,--gc-sections \
    -o "$O/alt" "$A/regress/diff_wdc_identify.c" 2> "$O/alt.cc"
if [ $? -ne 0 ]; then echo COMPILEFAIL; head -8 "$O/alt.cc"; exit 1; fi
"$O/alt" > "$O/alt.out" 2>&1
echo "--- the seven new rows on the COMMITTED device ---"
grep -E 'SRST \(0x06\)|routine 0x08 preserves|nIEN write is not|SRST aborts|still signs|does not sign|reset signature works' "$O/alt.out"
echo "--- totals ---"
tail -2 "$O/alt.out"
