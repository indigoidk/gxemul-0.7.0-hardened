#!/bin/bash
#  opus5 measurement driver for the asiceventaddr late review.
#  READ-ONLY on every project tree: the SEC header is only ever passed via -I
#  (or copied OUT of SEC into this directory); every mutant is a copy here.
set -u
M=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fableq/opus5_meas
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
HDR=$SEC/src/include/thirdparty/dreamcast_sysasicvar.h
INC="-I$SEC/src/include"
#  the build's own flags, from build/src/devices/Makefile CWARNINGS + COPTIM
BF="-Wshadow -Wcast-align -Wstrict-aliasing -Wall -Wextra -Wno-unused-parameter -Wno-cast-align -fstrict-aliasing -fomit-frame-pointer -fpeephole -fgnu89-inline -O3 -DNDEBUG"
BF0="${BF/-O3/-O0}"
OUT=$M/out
rm -rf "$OUT"; mkdir -p "$OUT"
cd "$M" || { echo "cannot cd $M"; exit 1; }

diag() {  # first error, else first warning, else "-"
	local f=$1 l
	l=$(grep -m1 -E 'error:' "$f" || grep -m1 -E 'warning:' "$f" || echo "-")
	echo "$l" | sed -e 's#^.*/##' | cut -c1-150
}

echo "== A0 toolchain + header identity"
cc --version | head -1
cc -dM -E -x c /dev/null | grep __STDC_VERSION__
md5sum "$HDR" | sed 's#  .*/#  #'

echo; echo "== A1 POSITIVE: 21 real events, build flags (default dialect)"
if cc $BF $INC t_pos.c -o "$OUT/t_pos" 2> "$OUT/t_pos.err"; then
	echo "compile rc=0 warnings=$(grep -c 'warning:' "$OUT/t_pos.err")"
	"$OUT/t_pos"; echo "run rc=$?"
else echo "compile FAILED: $(diag "$OUT/t_pos.err")"; fi
echo "-- same TU under -std=c99 -pedantic-errors -Wall -Wextra:"
cc -std=c99 -pedantic-errors -Wall -Wextra $INC -c t_pos.c -o "$OUT/t_pos99.o" 2> "$OUT/t_pos99.err"
echo "   rc=$? diag: $(diag "$OUT/t_pos99.err")"

echo; echo "== A2 C89 CLAIM: ADDR over all 21 events, -pedantic-errors -Wall -Wextra per dialect"
for s in c89 gnu89 c99 c11 c17 c23 gnu23; do
	cc -std=$s -pedantic-errors -Wall -Wextra $INC -c t_c89.c -o "$OUT/c89_$s.o" 2> "$OUT/c89_$s.err"
	printf '   %-6s rc=%s diag: %s\n' "$s" "$?" "$(diag "$OUT/c89_$s.err")"
done

echo; echo "== B DOMAIN: one argument per compile (build flags | -std=c99 -pedantic-errors)"
EVS=( "" "0" "95" "96" "127" "128" "159" "479" "2048" "6144" "(-1)" "(-32)" "(-2147483647-1)" "2147483647" "96u" "4294967295u" "0x100000000LL" "((unsigned char)200)" "'A'" "(0, 50)" "(0, 100)" "31" "63" "-1 (bare)" "0x5f" )
for c in $(seq 1 24); do
	cc $BF $INC -DCASE=$c -c t_neg.c -o "$OUT/neg_$c.o" 2> "$OUT/neg_$c.err"; r1=$?
	cc -std=c99 -pedantic-errors -Wall -Wextra $INC -DCASE=$c -c t_neg.c -o "$OUT/negp_$c.o" 2> "$OUT/negp_$c.err"; r2=$?
	printf '   CASE %2d EV=%-22s build rc=%s | c99-pedantic rc=%s | %s\n' "$c" "${EVS[$c]}" "$r1" "$r2" "$(diag "$OUT/neg_$c.err")"
done

echo; echo "== C CONSTANCY: runtime / const / enum / constexpr / side effect (-O3 | -O0)"
RTN=( "" "runtime int e" "static const int 5" "static const int 100" "enum 50" "enum 100" "V2 neg-ARRAY, runtime e" "constexpr 5" "constexpr 100" "g++ (side effect)" )
for c in $(seq 1 9); do
	cc $BF $INC -DCASE=$c -c t_rt.c -o "$OUT/rt_$c.o" 2> "$OUT/rt_$c.err"; r1=$?
	cc $BF0 $INC -DCASE=$c -c t_rt.c -o "$OUT/rt0_$c.o" 2> "$OUT/rt0_$c.err"; r2=$?
	printf '   CASE %d %-24s -O3 rc=%s -O0 rc=%s | %s\n' "$c" "${RTN[$c]}" "$r1" "$r2" "$(diag "$OUT/rt_$c.err")"
done
echo "-- V2 again with -Wvla, to show what would have to be enabled to see the VLA:"
cc $BF -Wvla $INC -DCASE=6 -c t_rt.c -o "$OUT/rt6v.o" 2> "$OUT/rt6v.err"; echo "   rc=$? $(diag "$OUT/rt6v.err")"

echo; echo "== D BITMASK: shipped value, UBSan, the ledger's one-token remedy, the 1u form"
cc $BF -Wshift-overflow=2 $INC t_shift.c -o "$OUT/t_shift" 2> "$OUT/t_shift.err"
echo "compile rc=$? ; -Wshift-overflow=2 warnings: $(grep -c 'warning:' "$OUT/t_shift.err")"
grep -E 'warning:' "$OUT/t_shift.err" | sed -e 's#^.*/##' | cut -c1-170 | sed 's/^/   /'
"$OUT/t_shift" | sed 's/^/   /'
for s in c99 gnu23; do
	cc -std=$s -O0 -fsanitize=undefined $INC t_shift.c -o "$OUT/t_shift_ubsan_$s" 2> /dev/null
	echo "-- UBSan build -std=$s rc=$?; runtime diagnostics:"
	"$OUT/t_shift_ubsan_$s" > "$OUT/ubsan_$s.out" 2> "$OUT/ubsan_$s.err"
	grep -c 'runtime error' "$OUT/ubsan_$s.err" | sed 's/^/   runtime-error lines: /'
	grep 'runtime error' "$OUT/ubsan_$s.err" | sed -e 's#^.*t_shift.c#t_shift.c#' | sort | uniq -c | sed 's/^/   /'
done

echo; echo "== E ENUMERATION of the unguarded formula over e in [0,8192)"
cc -O2 -Wall -Wextra $INC t_enum.c -o "$OUT/t_enum" 2> "$OUT/t_enum.err" && "$OUT/t_enum"

echo; echo "== F GUARD MUTANTS (copies of the header in this directory; SEC untouched)"
mk() {  # name sed-expr
	mkdir -p "$M/mut_$1/thirdparty"
	cp "$HDR" "$M/mut_$1/thirdparty/dreamcast_sysasicvar.h"
	sed -i -e "$2" "$M/mut_$1/thirdparty/dreamcast_sysasicvar.h"
	local nd
	nd=$(diff "$HDR" "$M/mut_$1/thirdparty/dreamcast_sysasicvar.h" | grep -c '^[<>]')
	printf '   mutant %-8s changed-line-pairs=%s (want 2)  ' "$1" "$nd"
	diff "$HDR" "$M/mut_$1/thirdparty/dreamcast_sysasicvar.h" | grep '^>' | cut -c1-90
}
mk null    's/(e) < 96) ? 1 : -1; })/(e) < 96) ? 1 : 1; })/'
mk upper   's/((e) >= 0 [&][&] (e) < 96)/((e) < 96)/'
mk wide    's/(e) < 96) ? 1 : -1; })/(e) < 128) ? 1 : -1; })/'
mk noguard 's/ + SYSASIC_EVENT_RANGE_OK(e))$/)/'
for m in null upper wide noguard; do
	MI="-I$M/mut_$m"
	cc $BF $MI t_pos.c -o "$OUT/pos_$m" 2> /dev/null && r=$("$OUT/pos_$m" | tail -1) || r="COMPILE FAIL"
	esc=""
	for c in 3 4 5 10 23; do
		cc $BF $MI -DCASE=$c -c t_neg.c -o "$OUT/m_${m}_$c.o" 2> /dev/null
		[ $? -eq 0 ] && esc="$esc ${EVS[$c]}:COMPILES" || esc="$esc ${EVS[$c]}:refused"
	done
	printf '   %-8s in-tree 21 events -> %s |%s\n' "$m" "$r" "$esc"
done
echo "-- and the SHIPPED header on the same five, for contrast:"
esc=""
for c in 3 4 5 10 23; do
	cc $BF $INC -DCASE=$c -c t_neg.c -o "$OUT/s_$c.o" 2> /dev/null
	[ $? -eq 0 ] && esc="$esc ${EVS[$c]}:COMPILES" || esc="$esc ${EVS[$c]}:refused"
done
echo "   shipped |$esc"

echo; echo "== G SEC header unchanged by this run"
md5sum "$HDR" | sed 's#  .*/#  #'
echo OPUS5_MEAS_DONE
