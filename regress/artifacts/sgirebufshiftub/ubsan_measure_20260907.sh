#!/bin/bash
#  THE REAL RUN, TAKE 3.  Two apparatus failures preceded this and both were caught by controls
#  rather than by luck, which is the only reason no false negative was recorded:
#
#    take 1  captured the PROBE's streams; the emulator runs in a PTY, so UBSan's output was never
#            in them.  Result: a meaningless 0 that looked like a measurement.
#    take 2  used UBSAN_OPTIONS/ASAN_OPTIONS log_path.  The IN-BAND CONTROL refused the run:
#            GCC's libubsan IGNORES log_path -- measured, H2 and H3 both produced ZERO files while
#            the diagnostic still went to stderr.
#
#  THE PLUMBING THAT ACTUALLY WORKS, from the same diagnosis: the diagnostic goes to stderr and
#  survives redirection (H5).  So WRAP the binary.  The probe takes the emulator path as an
#  argument, so a wrapper that execs the real binary with stderr appended to a file needs no change
#  to the probe at all -- and the probe cannot know the difference.
set -u
ASAN=/mnt/c/DocumentNoSnc/CC/GXEMUL/build-asan
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
W=/tmp/gxub5; rm -rf $W; mkdir -p $W; cd $W
CAP=$W/ubsan_capture.txt
: > $CAP

echo "=== clearance on the ASAN tree ==="
[ $ASAN/gxemul -nt $ASAN/src/devices/dev_sgi_re.c ] && echo "  part2 FRESH" || { echo "  *** STALE"; exit 9; }
cmp -s $ASAN/src/devices/dev_sgi_re.c $SEC/src/devices/dev_sgi_re.c && echo "  part1 CLEAN" || { echo "  *** DIVERGENT"; exit 9; }

#  The wrapper.  `exec' so signals and the pty behave exactly as with the real binary.
cat > $W/gxwrap <<WEOF
#!/bin/bash
exec $ASAN/gxemul "\$@" 2>> $CAP
WEOF
chmod +x $W/gxwrap

echo
echo "=== IN-BAND CONTROL: does the WRAPPER shape actually capture a known UB? ==="
FLAGS=$(grep -m1 '^COPTIM' $ASAN/src/devices/Makefile | sed 's/^COPTIM=//')
cat > $W/ctl.c <<'CEOF'
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
int main(int argc, char **argv)
{
	uint8_t buf[8]; uint32_t color; int i;
	for (i = 0; i < 8; i++) buf[i] = (uint8_t) strtoul(argv[1], NULL, 0) + i;
	color = (buf[0] << 24) + (buf[1] << 16) + (buf[2] << 8);
	printf("CONTROL color=0x%08x\n", color);
	return 0;
}
CEOF
gcc $FLAGS -o $W/ctl $W/ctl.c || { echo "  *** control build failed"; exit 9; }
CTLCAP=$W/ctl_capture.txt; : > $CTLCAP
cat > $W/ctlwrap <<WEOF
#!/bin/bash
exec $W/ctl "\$@" 2>> $CTLCAP
WEOF
chmod +x $W/ctlwrap
$W/ctlwrap 0xaa > /dev/null
N=$(grep -ic 'runtime error' $CTLCAP)
echo "  control capture lines: $N"
sed 's/^/    /' $CTLCAP | head -2
if [ "$N" -eq 0 ]; then
    echo "  *** THE WRAPPER SHAPE DOES NOT CAPTURE.  Emulator silence would be uninterpretable.  STOPPING."
    exit 9
fi
#  And the NEGATIVE direction, so the capture is discriminating rather than merely non-empty.
: > $CTLCAP; $W/ctlwrap 0x02 > /dev/null
M=$(grep -ic 'runtime error' $CTLCAP)
echo "  control with a LOW byte (must be 0): $M"
[ "$M" -ne 0 ] && { echo "  *** capture is not discriminating -- STOPPING"; exit 9; }
echo "  -> the wrapper captures, and only when UB occurs.  A zero below is now MEANINGFUL."

echo
echo "=== RUN: the shipped 10-row #505 probe, driving the WRAPPER ==="
cp $SEC/regress/sgi_re_rgb_probe.py $W/probe.py
timeout 900 python3 -u $W/probe.py $W/gxwrap asanrun > $W/probe.out 2> $W/probe.err
echo "  probe rc=$?"
echo "  result: $(tr -d '\0' < $W/probe.out | grep -o 'SGIRGB_RESULT=[0-9]*/[0-9]*' | tail -1)"
echo "  capture file: $(wc -c < $CAP) bytes"

echo
echo "=== UBSan diagnostics from the EMULATOR ==="
TOT=$(grep -ic 'runtime error' $CAP)
echo "  'runtime error' lines: $TOT"
echo
echo "  --- by kind ---"
grep -i 'runtime error' $CAP | sed 's/.*runtime error: //' | sort | uniq -c | sort -rn | head -25
echo
echo "  --- by source location ---"
grep -o '[a-zA-Z_0-9]*\.c:[0-9]*:[0-9]*' $CAP | sort | uniq -c | sort -rn | head -25
echo
echo "  --- LEFT SHIFT specifically (the class under test) ---"
echo "  left-shift lines: $(grep -ic 'left shift of' $CAP)"
grep -i 'left shift of' $CAP | sort | uniq -c | sort -rn | head -8 | sed 's/^/    /'

mkdir -p $SEC/regress/artifacts/sgirebufshiftub
cp $CAP $SEC/regress/artifacts/sgirebufshiftub/ubsan_emulator_20260907.txt
echo
echo "  preserved: regress/artifacts/sgirebufshiftub/ubsan_emulator_20260907.txt"
echo "UBREAL3_DONE"
