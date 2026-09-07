#!/bin/bash
#  DOES THE SIGNED-SHIFT UB ACTUALLY FIRE?  Owner decision 2026-09-07: measure before proposing.
#
#  *** THE POSITIVE CONTROL IS THE WHOLE POINT AND IT RUNS FIRST. ***
#  If the real run reports nothing, that is ambiguous between "the code does not do this" and
#  "this toolchain's UBSan does not check this" -- the pattern-that-matches-nothing shape.  So a
#  minimal reproducer, compiled with build-asan's OWN flags, must be shown to REPORT before any
#  silence from the real binary is worth anything.
#
#  The control takes its byte from argv so -O3 cannot constant-fold the shift away.
set -u
W=/tmp/gxub
rm -rf $W; mkdir -p $W; cd $W
ASAN=/mnt/c/DocumentNoSnc/CC/GXEMUL/build-asan

echo "=== build-asan's real flags, read from its own generated Makefile ==="
grep -m1 '^COPTIM' $ASAN/src/devices/Makefile
FLAGS=$(grep -m1 '^COPTIM' $ASAN/src/devices/Makefile | sed 's/^COPTIM=//')
echo

cat > ctl.c <<'CEOF'
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
/*  The exact idiom under test, as dev_sgi_re.c writes it: a uint8_t element of an array,
    promoted to int, shifted 24.  0xaa << 24 = 2852126720 > INT_MAX -> UB.  */
int main(int argc, char **argv)
{
	uint8_t buf[8];
	uint32_t color;
	int i;
	for (i = 0; i < 8; i++)
		buf[i] = (uint8_t) strtoul(argv[1], NULL, 0) + i;
	color = (buf[0] << 24) + (buf[1] << 16) + (buf[2] << 8);
	printf("CONTROL color=0x%08x from buf[0]=0x%02x\n", color, buf[0]);
	return 0;
}
CEOF

echo "=== POSITIVE CONTROL: compile the idiom with build-asan's flags ==="
gcc $FLAGS -o ctl ctl.c 2> ctl_build.err
rc=$?
echo "  gcc rc=$rc"; [ -s ctl_build.err ] && head -5 ctl_build.err
[ $rc -ne 0 ] && { echo "*** control did not build -- cannot interpret anything below"; exit 9; }

echo
echo "--- run with a byte >= 0x80 (0xaa): UB EXPECTED ---"
./ctl 0xaa > ctl_hi.out 2> ctl_hi.err
echo "  stdout: $(cat ctl_hi.out)"
echo "  stderr: $(wc -l < ctl_hi.err) lines"
grep -i 'runtime error' ctl_hi.err | head -3 | sed 's/^/    /'

echo
echo "--- run with a byte < 0x80 (0x02): NO UB EXPECTED (the negative control) ---"
./ctl 0x02 > ctl_lo.out 2> ctl_lo.err
echo "  stdout: $(cat ctl_lo.out)"
echo "  stderr: $(wc -l < ctl_lo.err) lines"
grep -i 'runtime error' ctl_lo.err | head -3 | sed 's/^/    /'

HI=$(grep -ic 'runtime error' ctl_hi.err)
LO=$(grep -ic 'runtime error' ctl_lo.err)
echo
echo "=== CONTROL VERDICT ==="
if [ "$HI" -gt 0 ] && [ "$LO" -eq 0 ]; then
    echo "  DISCRIMINATING: UBSan reports the high byte and not the low one."
    echo "  A silent real run therefore MEANS the path did not execute the UB."
elif [ "$HI" -eq 0 ]; then
    echo "  *** NOT DISCRIMINATING: UBSan did NOT report the known-UB case. ***"
    echo "  This toolchain's -fsanitize=undefined does not include the shift-base check here,"
    echo "  so ANY silence from the real binary is uninterpretable.  STOP -- do not read the"
    echo "  real run as evidence of anything."
else
    echo "  *** NOT DISCRIMINATING: the low byte reported too -- the control is wrong. ***"
fi
echo "UBCTL_DONE"
