#!/bin/bash
#  #500 sgideprimop -- corrected witness.  The FIRST attempt was CONFOUNDED: a
#  START-aliased WRITE also writes the register, so the trigger value BECOMES op.
#  Attempt A appeared to test the reset value and actually tested op = 1; attempt C
#  programmed TRIANGLE and then CLOBBERED it with the trigger write.
cd /mnt/c/DocumentNoSnc/cc/GXEMUL
printf '\0\0\0\0' > /tmp/d500.bin
G="./build/gxemul -V -E sgi -e ip32 -M 64 0x80001000:/tmp/d500.bin"

echo "=== A2: the TRUE reset-value test -- a START-aliased READ, nothing ever written ==="
echo "    (a READ cannot carry a value, so op MUST be whatever init left there)"
printf 'put w 0xffffffffb5002860, 0x0\nquit\n' > /dev/null   # not used; read below
printf 'x 0xffffffffb5002860\nquit\n' | timeout 60 $G 2>&1 \
  | grep -iE 'UNIMPLEMENTED drawing op' | head -2
echo "  emulator exit status: ${PIPESTATUS[1]}"

echo
echo "=== B2: TRIANGLE -- the encoding must go in the TRIGGER write, not a prior one ==="
printf 'put w 0xffffffffb5002860, 0x02000000\nquit\n' | timeout 60 $G 2>&1 \
  | grep -iE 'UNIMPLEMENTED drawing op' | head -2
echo "  emulator exit status: ${PIPESTATUS[1]}"

echo
echo "=== C2: POINT explicitly -- 0x00000000 in the trigger write ==="
printf 'put w 0xffffffffb5002860, 0x00000000\nquit\n' | timeout 60 $G 2>&1 \
  | grep -iE 'UNIMPLEMENTED drawing op' | head -2
echo "  emulator exit status: ${PIPESTATUS[1]}"

echo
echo "=== D2: CONTROL -- a LEGAL primitive (RECTANGLE 0x03000000) must NOT die ==="
printf 'put w 0xffffffffb5002860, 0x03000000\nquit\n' | timeout 60 $G 2>&1 \
  | grep -ciE 'UNIMPLEMENTED drawing op' | sed 's/^/  draw-kill messages: /'
echo "  emulator exit status: ${PIPESTATUS[1]}"
echo WIT500B_DONE
