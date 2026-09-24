#!/bin/bash
# U3: preprocess HEAD's and the working dev_sgi_re.c AT THE SAME PATH with identical flags; compare.
set -u
S=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
T=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/u3_cpp
FL="-I$S -I$S/src/include -D_XOPEN_SOURCE=600 -D_XOPEN_SOURCE_EXTENDED -DHAVE_CONFIG_H"
for v in head work; do
	cp "$T/${v}_dev_sgi_re.c" "$T/x/dev_sgi_re.c"
	gcc -E -P $FL "$T/x/dev_sgi_re.c" > "$T/${v}.i" 2> "$T/${v}.err"; echo "$v cpp rc=$? lines=$(wc -l < "$T/${v}.i")"
	gcc -c -O0 $FL "$T/x/dev_sgi_re.c" -o "$T/${v}.o" 2>> "$T/${v}.err"; echo "$v cc rc=$? bytes=$(wc -c < "$T/${v}.o")"
done
cmp "$T/head.i" "$T/work.i" && echo "PREPROCESSED OUTPUT IDENTICAL"
cmp "$T/head.o" "$T/work.o" && echo "OBJECT FILES IDENTICAL"
grep -c 'delete ' "$T/head_dev_sgi_re.c" "$T/work_dev_sgi_re.c"
