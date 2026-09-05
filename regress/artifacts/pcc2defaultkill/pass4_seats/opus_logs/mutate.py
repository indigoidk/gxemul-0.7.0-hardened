#!/usr/bin/env python3
#  #501 pass-4 Opus seat: apply ONE mutant to the clone's dev_pcc2.c, by unique-anchor replace.
#  Refuses if the anchor is absent or non-unique.  Prints the diff line count.
import sys, subprocess
SEC = "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_pcc2.c"
TGT = "/tmp/gxopus501p4/src/devices/dev_pcc2.c"

MUT = {
  # read announce: print data[len>>2] -- data[0] at len 1 and len 2, data[1] at len 4.
  # The M_LASTBYTE class narrowed to len 4, where the only row reads four zero bytes.
  "MO1_RDWIDEBYTE": (
     '\t\t\t\t    (int) relative_addr, (int) len, data[0]);',
     '\t\t\t\t    (int) relative_addr, (int) len, data[len>>2]);'),
  # the WRITE arm's announce suppressed at len 2 (the len-2 write takes the read text).
  "MO2_WRHALFSILENT": (
     '\t\t\td->warned_unimpl |= 1ULL << relative_addr;\n\t\t\tif (writeflag == MEM_WRITE)',
     '\t\t\td->warned_unimpl |= 1ULL << relative_addr;\n\t\t\tif (writeflag == MEM_WRITE && len != 2)'),
  # read announce: the OFFSET label zeroed for relative_addr >= 0x14 (31 of the 43 offsets).
  "MO3_RDOFFLABEL": (
     '\t\t\t\t    (int) relative_addr, (int) len, data[0]);',
     '\t\t\t\t    (int) (relative_addr < 0x14 ? relative_addr : 0), (int) len, data[0]);'),
  # CONTROL: the pass-3 escape the repair claims to close (table 4 says 45/46, srvd half text).
  "CTL_LASTBYTE": (
     '\t\t\t\t    (int) relative_addr, (int) len, data[0]);',
     '\t\t\t\t    (int) relative_addr, (int) len, data[len-1]);'),
  # the WRITE announce's VALUE zeroed at len 2 only (weaker form of MO2, same cell).
  "MO4_WRHALFVAL": (
     '\t\t\t\t    (int) relative_addr, (int) len, (int) idata);',
     '\t\t\t\t    (int) relative_addr, (int) len, (int) (len == 2 ? 0 : idata));'),
}

name = sys.argv[1]
if name == "RESTORE":
    open(TGT, "w", newline="").write(open(SEC, newline="").read())
    print("RESTORED")
    sys.exit(0)
old, new = MUT[name]
src = open(SEC, newline="").read()
n = src.count(old)
if n != 1:
    print("ANCHOR_FAIL %s occurrences=%d" % (name, n)); sys.exit(9)
open(TGT, "w", newline="").write(src.replace(old, new))
d = subprocess.run(["diff", SEC, TGT], capture_output=True, text=True).stdout
print("MUTANT %s applied; diff lines: %d" % (name, len([l for l in d.splitlines() if l[:1] in "<>"])))
print(d)
