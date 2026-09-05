#!/bin/sh
#  BASE2: the SAME frozen instrument the M_ICLR table used -- NO re-copy.
P=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p11_opus
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
echo "FROZEN_MD5=$(md5sum /tmp/frozen_probe_p11.py | cut -c1-8)   (must be 12c7a97b, the M_ICLR instrument)"
echo "CLONE_BINARY_MD5=$(md5sum /tmp/gxopus_p11/gxemul | cut -c1-12)  (must be 3fb4d342e067, the RESTORED baseline)"
cd $SEC/regress || exit 9
date +'START %H:%M:%S'
python3 -u /tmp/frozen_probe_p11.py /tmp/gxopus_p11/gxemul BASE2 > $P/BASE2.out 2>&1
echo "PROBE_RC=$?"
date +'END   %H:%M:%S'
grep -E '^PCC2W_RESULT|^PCC2W_RED|^PCC2W_PROBE_DONE' $P/BASE2.out
echo "FAILCOUNT=$(grep -c 'FAIL$' $P/BASE2.out)"
