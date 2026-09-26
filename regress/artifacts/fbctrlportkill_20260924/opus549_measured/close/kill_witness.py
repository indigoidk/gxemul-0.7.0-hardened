#!/usr/bin/env python3
"""Does E_ref_cmd reinstate the host kill?  GET_RESOLUTION, PORT=5, refuse 9, then ONE DATA read.  Uses the shipped
probe's session() (frozen copy in argv[2]).  usage: kill_witness.py <gxemul> <frozen probe>"""
import importlib.util
import sys
BIN, PROBE = sys.argv[1], sys.argv[2]
sys.argv = [PROBE, BIN]
spec = importlib.util.spec_from_file_location("fbp", PROBE)
fbp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fbp)
stub = fbp.stub_path()
S = fbp.session("KW", [("sw", "zr", 0, None), ("sw", "a1", 16, None), ("sw", "a0", 0, None), ("sw", "t1", 0, None),
                       ("lw", "s0", 16, None)],
                [("t0", fbp.FBCTRL), ("a0", 5), ("a1", 2), ("t1", 9), ("s0", 0xdead)], ["s0"], stub)
import os
os.unlink(stub)
print("KW status=%s steps=%d/%d exit=%s DATA read=%s" % (S["status"], S["steps"], S["n"], S["exit"], fbp.hx(S["vals"].get("s0"))))
print("KW_DONE")
