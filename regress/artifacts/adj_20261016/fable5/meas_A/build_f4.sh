#!/bin/bash
set -u
R=/tmp/gxf5adjA
B=$R/base
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/adjA
MUT=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/wdc473floor/r3pass_20261013/opus5/mutants
CC=$(command -v cc || command -v gcc)
INC="-I$B/src/include -I$B/src/include/thirdparty"
run_one () {
    name="$1"; wdcsrc="$2"
    D=$R/f4_$name
    rm -rf "$D"; mkdir -p "$D/src/devices" "$D/regress"
    cp "$wdcsrc" "$D/src/devices/dev_wdc.c"
    cp "$S/scratch_f4.c" "$D/regress/scratch_f4.c"
    if $CC -O2 -std=c99 $INC -ffunction-sections -fdata-sections -Wl,--gc-sections -o "$D/scratch_f4" "$D/regress/scratch_f4.c" > "$D/build.log" 2>&1; then
        if [ ! "$D/scratch_f4" -nt "$D/src/devices/dev_wdc.c" ]; then echo "$name BUILD_STALE"; return; fi
        md=$(md5sum "$D/src/devices/dev_wdc.c" | cut -c1-8)
        echo "---- $name (dev_wdc.c md5 $md) ----"
        "$D/scratch_f4"
    else
        echo "$name BUILD_FAIL"; tail -5 "$D/build.log"
    fi
}
run_one HEAD      "$B/src/devices/dev_wdc.c"
run_one D2_st     "$MUT/D2_st.c"
run_one D2_or_st  "$MUT/D2_or_st.c"
run_one D2_and_st "$MUT/D2_and_st.c"
run_one D2_phase  "$MUT/D2_phase.c"
echo "F4_DONE"
