#!/usr/bin/env python3
"""listcmd_witness.py <gxemul> -- a sibling of pvrrenderexit found while reading pvr_render() for the detector: the command loop's
`default: fatal("pvr_render: unimplemented list cmd %i\n", cmd); exit(1);`.  One cold -E dreamcast session per command type 2, 3, 5, 6:
FB_RENDER_CFG = 1, one 8-word command whose word 0 carries that type in bits 31-29, then STARTRENDER, each store a real guest mov.l
(the witness probe's store() shape).  Reports exit status and whether the fatal text printed.  Read-only research."""
import os
import subprocess
import sys
import tempfile

BIN = sys.argv[1]
tmp = tempfile.mkdtemp(prefix="listcmd_")
DUMMY = os.path.join(tmp, "dummy.bin")
open(DUMMY, "wb").write(bytes(4))
CODE, W_STORE = 0x8c010000, 0x00092782
FB_RENDER_CFG, STARTRENDER, TA = 0xa05f8048, 0xa05f8014, 0xb0000000


def store(addr, val):
    return ["r7=0x%x" % addr, "r8=0x%x" % val, "pc=0x%x" % CODE, "step 1"]


for cmd in (2, 3, 5, 6):
    body = ["put w 0x%x, 0x%08x" % (CODE, W_STORE)] + store(FB_RENDER_CFG, 1)
    for k, w in enumerate([cmd << 29, 0, 0, 0, 0, 0, 0, 0]):
        body += store(TA + 4 * k, w)
    body += store(STARTRENDER, 0) + ["reg", "quit"]
    p = subprocess.run([BIN, "-V", "-x", "-E", "dreamcast", "0x%x:%s" % (CODE, DUMMY)], input=("\n".join(body) + "\n").encode(),
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
    t = p.stdout.decode("latin-1", "replace")
    print("cmd %d: exit%d  fatal=%s  prompt=%s" % (cmd, p.returncode, "unimplemented list cmd %d" % cmd in t, "GXemul> reg" in t))
print("LISTCMD_WITNESS_DONE")
