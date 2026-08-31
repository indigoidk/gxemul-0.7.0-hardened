#!/bin/bash
#  Reproduce the rung-3 witness for pcc2widthkills on the UNMODIFIED committed tree.
#  Real guest m88k instructions through real decode -- not a debugger poke.
cd /mnt/c/DocumentNoSnc/cc/GXEMUL
printf '\0\0\0\0' > /tmp/dummy88k.bin
echo "=== A: REAL GUEST DECODE -- st r1,(r2) with r2 = 0xfff4201c (SCCERR, word-aligned) ==="
printf 'put w 0x1000, 0x5C40FFF4\nput w 0x1004, 0x5842201C\nput w 0x1008, 0x58200042\nput w 0x100c, 0x24220000\npc=0x1000\nstep 4\nquit\n' \
  | timeout 60 ./build/gxemul -V -E mvme88k -e mvme187 -M 64 0x1000:/tmp/dummy88k.bin 2>&1 \
  | grep -iE 'TODO: pcc2|non-byte|st r1|exit|0xfff4201c' | head -8
echo "  exit status: ${PIPESTATUS[0]}"
echo
echo "=== B: the put b TRAP -- does a BYTE put reach the device at all? ==="
printf 'put b 0xfff42002, 0x1\nquit\n' \
  | timeout 60 ./build/gxemul -V -E mvme88k -e mvme187 -M 64 0x1000:/tmp/dummy88k.bin 2>&1 \
  | grep -icE 'TODO: pcc2|non-byte' | sed 's/^/  device messages from put b: /'
echo
echo "=== C: CONTROL -- put w to the same arm SHOULD kill ==="
printf 'put w 0xfff4201c, 0x11223344\nquit\n' \
  | timeout 60 ./build/gxemul -V -E mvme88k -e mvme187 -M 64 0x1000:/tmp/dummy88k.bin 2>&1 \
  | grep -icE 'TODO: pcc2.*SCCERR' | sed 's/^/  SCCERR kill messages from put w: /'
echo PCC2WIT_DONE
