#!/usr/bin/env python3
"""Does LB_unset16 reinstate the DATA-arm exit on a reachable guest write?  A FRESH device (latch unset): write 16 to
PORT as the very first access, then one DATA read.  Under `idata==0x10 && !warned_port` -> accept, current_port=16,
DATA read -> range check -> exit(1).  On the fix -> refused, survives.  Also tries 2^5 and 2^6 (sh/sw) as first writes.
Uses the frozen v6 probe's own session().  usage: unset_witness.py <gxemul> <frozen probe>"""
import importlib.util
import os
import sys

BIN, PROBE = sys.argv[1], sys.argv[2]
sys.argv = [PROBE, BIN]
spec = importlib.util.spec_from_file_location("fbp", PROBE)
fbp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fbp)
stub = fbp.stub_path()
for lab, w, val in (("16(sb,first)", "sb", 0x10), ("32(sh,first)", "sh", 0x20), ("64(sw,first)", "sw", 0x40)):
    S = fbp.session("U_" + lab, [(w, "t1", 0, None), ("lw", "s0", 16, None)],
                    [("t0", fbp.FBCTRL), ("t1", val), ("s0", 0xdead)], ["s0"], stub)
    print("U %-14s status=%s steps=%d/%d exit=%s DATA=%s" % (lab, S["status"], S["steps"], S["n"], S["exit"],
                                                             fbp.hx(S["vals"].get("s0"))))
os.unlink(stub)
print("U_DONE")
