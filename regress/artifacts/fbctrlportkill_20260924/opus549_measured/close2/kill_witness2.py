#!/usr/bin/env python3
"""Does F_ref_c7 reinstate the host kill?  PORT=7, DATA=0x77 (COLOR_B), PORT=5, PORT=9, then ONE DATA read.
Uses the shipped probe's own session() (frozen copy in argv[2]).  usage: kill_witness2.py <gxemul> <frozen probe>"""
import importlib.util
import os
import sys
BIN, PROBE = sys.argv[1], sys.argv[2]
sys.argv = [PROBE, BIN]
spec = importlib.util.spec_from_file_location("fbp", PROBE)
fbp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fbp)
stub = fbp.stub_path()
S = fbp.session("KW2", [("sw", "a2", 0, None), ("sw", "a3", 16, None), ("sw", "a0", 0, None), ("sw", "t1", 0, None),
                        ("lw", "s0", 16, None)],
                [("t0", fbp.FBCTRL), ("a0", 5), ("a2", 7), ("a3", 0x77), ("t1", 9), ("s0", 0xdead)], ["s0"], stub)
os.unlink(stub)
print("KW2 status=%s steps=%d/%d exit=%s DATA read=%s" % (S["status"], S["steps"], S["n"], S["exit"], fbp.hx(S["vals"].get("s0"))))
print("KW2_DONE")
