#!/bin/bash
# Build the gated harness on the FROZEN device; it must reproduce the frozen output byte for byte with
# FBSKIP unset, and each gate must remove exactly the rows its loops define.
set -u
X=/tmp/opusq2c
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2c/opus
F=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2c/frozen
cmp "$X/src/devices/dev_footbridge.c" "$F/dev_footbridge.c" && echo "scratch device == frozen"
python3 "$O/mkgated.py" "$F/diff_footbridge.c" "$X/regress/diff_gated.c" || exit 9
cp "$X/regress/diff_gated.c" "$O/diff_gated.c"
md5sum "$X/regress/diff_gated.c"
cd "$X/regress" || exit 9
gcc -O2 -std=c99 -Wall -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections -Wl,--gc-sections -I"$X/src" -I"$X/src/include" -I"$X/src/include/thirdparty" -o g diff_gated.c -lm
echo "gcc rc=$?"
./g > /tmp/opusq2c/g_unset.log 2>&1
cmp /tmp/opusq2c/g_unset.log "$O/baseline.log" && echo "GATED, FBSKIP unset == frozen baseline output (byte-identical)"
FBSKIP= ./g > /tmp/opusq2c/g_empty.log 2>&1
cmp /tmp/opusq2c/g_empty.log "$O/baseline.log" && echo "GATED, FBSKIP empty == frozen baseline output (byte-identical)"
names() { grep -E '^  (ok|FAIL) +' "$1" | grep -v '@@SELFCHECK@@' | sed -E 's/^  (ok|FAIL) +//; s/[[:space:]]+[0-9]+$//; s/[[:space:]]+$//' | sort -u; }
names "$O/baseline.log" > /tmp/opusq2c/base_names.txt
echo "baseline distinct row names (excl selfcheck probes): $(wc -l < /tmp/opusq2c/base_names.txt)"
for gate in P X1 X2 X3 X4 X5 X6 X6R X6W X6P X7 X7W X7R X8 X9 X9R X9W X10 X10R X10W X11 X12 SEEDED ZERO WIDE ONES "X9,X12" "X7,X10" "P,X1,X2,X3,X4,X5" "X6,X7,X9,X10,X11,X12"; do
	FBSKIP="$gate" ./g > /tmp/opusq2c/g_gate.log 2>&1
	rows=$(grep -oE '^[0-9]+ rows' /tmp/opusq2c/g_gate.log | grep -oE '^[0-9]+')
	nf=$(grep '^  FAIL' /tmp/opusq2c/g_gate.log | grep -v '@@SELFCHECK@@' | grep -vc 'IDENTITY')
	idf=$(grep '^  FAIL' /tmp/opusq2c/g_gate.log | grep -c 'IDENTITY')
	gone=$(( 707 - rows ))
	names /tmp/opusq2c/g_gate.log > /tmp/opusq2c/gate_names.txt
	# the removed row names, grouped by their first token (the family prefix)
	missing=$(comm -23 /tmp/opusq2c/base_names.txt /tmp/opusq2c/gate_names.txt | awk '{print $1}' | sort | uniq -c \
	          | awk '{printf "%s:%s ", $2, $1}')
	nmiss=$(comm -23 /tmp/opusq2c/base_names.txt /tmp/opusq2c/gate_names.txt | wc -l)
	printf '%-24s rows=%-4s removed=%-4s names-removed=%-4s non-IDENTITY FAILs=%s IDENTITY FAIL=%s  by prefix: %s\n' \
	    "$gate" "$rows" "$gone" "$nmiss" "$nf" "$idf" "$missing"
done
echo GATED_CHECK_DONE
