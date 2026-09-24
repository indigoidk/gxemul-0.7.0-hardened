#!/bin/bash
# Final: the scratch device is the frozen copy, no sentinel, a FRESH baseline build is 491/0, the project
# files this seat was told not to touch still carry their start-of-seat hashes; package logs and diffs.
X=/tmp/opusq2r
P=/mnt/c/DocumentNoSnc/cc/GXEMUL
F=$P/_scratchpad/fbd5/q2r/frozen
O=$P/_scratchpad/fbd5/q2r/opus
cmp "$X/src/devices/dev_footbridge.c" "$F/dev_footbridge.c" && echo "scratch device == frozen (cmp clean)"
cmp "$X/regress/diff_footbridge.c" "$F/diff_footbridge.c" && echo "scratch harness == frozen (cmp clean)"
[ -e "$X/.MUTANT" ] && echo "SENTINEL PRESENT" || echo "no sentinel"
cd "$X/regress" || exit 9
rm -f d
gcc -O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections -Wl,--gc-sections -I"$X/src" -I"$X/src/include" -I"$X/src/include/thirdparty" -o d diff_footbridge.c -lm
[ d -nt ../src/devices/dev_footbridge.c ] && echo "binary newer than source"
./d > "$O/baseline_final.log" 2>&1; echo "run rc=$?"
tail -2 "$O/baseline_final.log"
md5sum d
md5sum "$P/GXEMUL-SEC/src/devices/dev_footbridge.c" "$P/GXEMUL-SEC/regress/diff_footbridge.c" "$P/GXEMUL-SEC/regress/gate_offline.sh"
tar czf "$O/variant_logs_and_diffs.tar.gz" -C "$X" logs diffs
tar tzf "$O/variant_logs_and_diffs.tar.gz" | grep -c '\.log$'
tar tzf "$O/variant_logs_and_diffs.tar.gz" | grep -c '\.diff$'
echo FINAL_DONE
