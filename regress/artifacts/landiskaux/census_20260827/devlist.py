#!/usr/bin/env python3
"""devlist.py -- dump the landisk machine's mapped-device table.

Q4: does anything else in the tree already claim 0x1400002c?  Static grep answers
"nothing in the source"; this answers it for the CONSTRUCTED machine, which is the
form that matters -- a device can be added by a bus/PROM layer without the machine
file naming an address.
"""
import sys, time
sys.path.insert(0, "/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad")
import gxprobe

BIN = sys.argv[1] if len(sys.argv) > 1 else "/tmp/gxcensusA/gxemul"
IMG = "/mnt/c/DocumentNoSnc/CC/GXEMUL/_images"


class SH4Emu(gxprobe.Emu):
    def install_stubs(self):
        pass


e = SH4Emu(BIN, ["-V", "-E", "landisk", "-M", "64",
                 "-d", "iR:%s/wdc-scratch-64m.img" % IMG,
                 "%s/openbsd76-landisk-bsd.rd" % IMG], boot_wait=6.0)
e.send("device list", wait=3.0)
e.send("watchpoint add 0xb400002c, 1", wait=1.5)
e.send("watchpoint show", wait=1.5)
txt = e.raw_text
e.close()
open("/tmp/census_devlist.log", "w").write(txt)
start = txt.find("device list")
print(txt[start:] if start >= 0 else txt[-4000:])
