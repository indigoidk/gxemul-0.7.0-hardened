"""Offline unit check of owed()/noise()/unclean() in the table-7 scratch probe.  Builds the transcript owed() predicts,
checks it is silent, and checks the edits the final pass named are not.  No emulator run."""
import sys
SRC = "/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/maple_probe_next7.py"
src = open(SRC, encoding="utf-8").read()
cut = src.index('print("MAPLE_DMAADDR DETECTOR')
sys.argv = ["x", "/bin/true"]
g = {"__name__": "m"}
exec(compile(src[:cut], SRC, "exec"), g)
cmds = g["store32"](g["MAPLE_DMAADDR"], g["VAL_A"], g["CODE"]) + g["load32"](g["MAPLE_DMAADDR"], g["CODE"] + 0x20)
lines = []
for kind, want in g["owed"](cmds + ["quit"]):
    if kind in ("echo", "line"):
        lines.append(want)
    elif kind == "hex":
        lines.append("0x%x" % want)
    elif kind == "put":
        lines.append("0x%x: %04x" % want)
    elif kind == "value":
        lines.append("0x8c012345")
t = "boot junk\r\n" + "\r\n".join(lines) + "\r\n"
print("clean noise:", g["noise"](t, cmds))
for ln in lines:
    if "mov" in ln:
        print("  owed disasm:", repr(ln))
# the MEASURED clean line from blank_measure's val_a transcript (killtable4_20260912/blank_measure.py output):
measured = "8c001020:  6212        mov.l\t@r1,r2\t; r1 = 0xa05f6c04"
print("matches the measured clean line:", measured in lines)
hooked = t.replace("mov.l\t@r1,r2\t; r1 = 0xa05f6c04", "DMAADDR read")
print("disassembler-hook noise:", g["noise"](hooked, cmds))
print("unclean sig6/eof:", g["unclean"]("sig6", True), "| exit0/noeof:", g["unclean"]("exit0", False),
      "| exit0/eof:", g["unclean"]("exit0", True))
