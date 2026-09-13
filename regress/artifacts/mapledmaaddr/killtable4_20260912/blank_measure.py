#!/usr/bin/env python3
"""Measure blank lines / bare CRs in clean maple read sessions, using the probe's own apparatus (exec'd up to rows)."""
import sys, collections
SRC = "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/maple_dmaaddr_probe.py"
BIN = sys.argv[1]
src = open(SRC).read()
cut = src.index('print("MAPLE_DMAADDR DETECTOR')
sys.argv = ["x", BIN]
g = {"__name__": "m"}
exec(compile(src[:cut], SRC, "exec"), g)
sess = {
 "val_a": g["store32"](g["MAPLE_DMAADDR"], g["VAL_A"], g["CODE"]) + g["load32"](g["MAPLE_DMAADDR"], g["CODE"] + 0x20),
 "initial": g["load32"](g["MAPLE_DMAADDR"], g["CODE"]),
 "triple": g["store32"](g["MAPLE_DMAADDR"], g["VAL_A"], g["CODE"]) + g["load32"](g["MAPLE_DMAADDR"], g["CODE"] + 0x20, dest=2)
           + g["load32"](g["MAPLE_DMAADDR"], g["CODE"] + 0x40, dest=3) + g["load32"](g["MAPLE_DMAADDR"], g["CODE"] + 0x60, dest=4),
}
for rep in range(3):
    for name, cmds in sess.items():
        t, how = g["session"](cmds)
        i = t.find("GXemul> ")
        body = t[i:]
        lines = body.replace("\r", "").split("\n")
        blanks = sum(1 for ln in lines if ln == "")
        ncr, nlf = body.count("\r"), body.count("\n")
        crlf = body.count("\r\n")
        print("%s rep%d how=%s blanks=%d CR=%d LF=%d CRLF=%d bareCR=%d lines=%d noise=%r" % (
            name, rep, how, blanks, ncr, nlf, crlf, ncr - crlf, len(lines), g["noise"](t, cmds)))
        if rep == 0 and name == "val_a":
            print(repr(body[-400:]))
print("BLANK_MEASURE_DONE")
