#!/usr/bin/env python3
"""#549 closing pass: ROW PROTOTYPES for the cells the 73-row probe does not row (each measured escaping it).
Imports the SHIPPED probe (a frozen copy, path in argv[2]) and reuses its own session() -- same launcher, same stepping,
same disassembly check -- adding only the lb/lh encodings.  Each cell is its own fresh-emulator session.
usage: close_rows_proto.py <gxemul> <frozen shipped probe .py>"""
import importlib.util
import sys

BIN, PROBE = sys.argv[1], sys.argv[2]
sys.argv = [PROBE, BIN]                                   # the probe reads BIN from argv[1] at import
spec = importlib.util.spec_from_file_location("fbp", PROBE)
fbp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fbp)
fbp.OPS["lb"] = 0x20
fbp.OPS["lh"] = 0x21
assert fbp.ins("lb", "s0", 0) == 0x81100000 and fbp.ins("lh", "s1", 0) == 0x85110000
F = fbp.FBCTRL
RES = []


def row(name, got, want):
    ok = got == want
    RES.append(ok)
    print("  %-4s %-58s got=%-10s want=%s" % ("ok" if ok else "FAIL", name, got, want))


hx = fbp.hx
stub = fbp.stub_path()
try:
    # X1 read x width: a byte and a halfword read of PORT with selector 5, then PORT read by lw
    S = fbp.session("X1", [("sw", "a0", 0, None), ("lb", "s0", 0, None), ("lh", "s1", 0, None), ("lw", "s2", 0, None)],
                    [("t0", F), ("a0", 5), ("s0", 0xdead), ("s1", 0xdead), ("s2", 0xdead)], ["s0", "s1", "s2"], stub)
    row("X1 lb of PORT reads 5", hx(S["vals"].get("s0")), "0x5")
    row("X1 lh of PORT reads 5", hx(S["vals"].get("s1")), "0x5")
    row("X1 PORT still 5 after the narrow reads", hx(S["vals"].get("s2")), "0x5")
    # X2 refuse x previous selectors 1..4
    prog, regs, rds = [], [("t0", F), ("t1", 9), ("a0", 1), ("a1", 2), ("a2", 3), ("a3", 4)], []
    for p, r, rb in ((1, "a0", "s0"), (2, "a1", "s1"), (3, "a2", "s2"), (4, "a3", "s3")):
        prog += [("sw", r, 0, None), ("sw", "t1", 0, None), ("lw", rb, 0, None)]
        regs.append((rb, 0xdead))
        rds.append(rb)
    S = fbp.session("X2", prog, regs, rds, stub)
    for p, rb in ((1, "s0"), (2, "s1"), (3, "s2"), (4, "s3")):
        row("X2 refuse 9 after PORT=%d, PORT keeps %d" % (p, p), hx(S["vals"].get(rb)), "0x%x" % p)
    # X3 COMMAND != 0: GET_RESOLUTION, PORT=5, lw PORT; the session's FIRST refusal; lw PORT
    S = fbp.session("X3", [("sw", "zr", 0, None), ("sw", "a1", 16, None), ("sw", "a0", 0, None), ("lw", "s0", 0, None),
                           ("sw", "t1", 0, "c1"), ("lw", "s1", 0, None)],
                    [("t0", F), ("a0", 5), ("a1", 2), ("t1", 9), ("s0", 0xdead), ("s1", 0xdead)], ["s0", "s1"], stub)
    row("X3 PORT read after GET_RESOLUTION reads 5", hx(S["vals"].get("s0")), "0x5")
    row("X3 first refusal after GET_RESOLUTION announces (count 1)", S["once_after"].get("c1"), 1)
    row("X3 refuse 9 after GET_RESOLUTION, PORT keeps 5", hx(S["vals"].get("s1")), "0x5")
    # X4 the FIRST refusal of a fresh device at widths 1, 2 and 8 announces
    for w, reg, val in (("sb", "t4", 8), ("sh", "t4", 8), ("sd", "t4", 8)):
        S = fbp.session("X4" + w, [("sw", "a0", 0, None), (w, reg, 0, "f1")], [("t0", F), ("a0", 5), (reg, val)], [],
                        stub)
        row("X4 first refusal by %s announces (count 1)" % w, S["once_after"].get("f1"), 1)
    # X5 the FIRST refusal after PORT=1 announces
    S = fbp.session("X5", [("sw", "a0", 0, None), ("sw", "t1", 0, "f1")], [("t0", F), ("a0", 1), ("t1", 9)], [], stub)
    row("X5 first refusal after PORT=1 announces (count 1)", S["once_after"].get("f1"), 1)
finally:
    import os
    try:
        os.unlink(stub)
    except OSError:
        pass
print("XROWS_RESULT=%d/%d" % (sum(RES), len(RES)))
print("XROWS_DONE")
sys.exit(0 if all(RES) else 1)
