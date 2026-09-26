#!/usr/bin/env python3
"""Does MK_b9_31 restore the host kill?  PORT=5, then 0x200 (sw) to PORT, then ONE DATA read.  0x200's only bit >= 3 is
bit 9, so under MK_b9_31 it is ACCEPTED (current_port = 512) and the DATA arm's kept range check ends the process.
Uses the shipped v5 probe's own session() (frozen copy in argv[2]).  usage: mask_witness.py <gxemul> <frozen probe>"""
import importlib.util
import os
import sys

BIN, PROBE = sys.argv[1], sys.argv[2]
sys.argv = [PROBE, BIN]
spec = importlib.util.spec_from_file_location("fbp", PROBE)
fbp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fbp)
stub = fbp.stub_path()
S = fbp.session("MW", [("sw", "a0", 0, None), ("sw", "t1", 0, None), ("lw", "s0", 16, None)],
                [("t0", fbp.FBCTRL), ("a0", 5), ("t1", 0x200), ("s0", 0xdead)], ["s0"], stub)
os.unlink(stub)
print("MW status=%s steps=%d/%d exit=%s DATA read=%s" % (S["status"], S["steps"], S["n"], S["exit"],
                                                          fbp.hx(S["vals"].get("s0"))))
print("MW_DONE")
