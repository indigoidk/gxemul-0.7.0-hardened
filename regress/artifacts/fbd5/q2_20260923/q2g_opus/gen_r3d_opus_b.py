#!/usr/bin/env python3
"""Opus seat, q2g ADDENDUM (written after the main table, before these two were built): two more CALLER-context members
that the scratch real-caller row W5 does not set -- to measure whether a ROW can close the class or only a disclosure can.
Same anchors and prediction classes as gen_r3d_opus.py."""
import io, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_r3d_opus as g  # noqa: E402
FROZEN = g.FROZEN
g.V[:] = []
g.dir_("CX09", "CX", "A1", "writeflag == MEM_READ && !cpu->pc", "GREEN-REAL",
       note="12 characters: every real IRQ_RAW_STATUS read declined (a real access has the accessing instruction's PC; "
            "the harness cpu's is 0).  PREDICTED GREEN ON THE 872-ROW EXTENSION TOO: W5 does not set pc")
g.clr_("CX10", "CX", 1, "\t\t\tif ((d->irq_status & d->irq_enable) && !cpu->cd.arm.cpsr)", "GREEN-REAL",
       note="a Clear never asserts once the CPU has a mode in CPSR (always, on a real ARM).  PREDICTED GREEN ON THE "
            "EXTENSION TOO: W5 does not set cpsr")
def variants():
    return g.V
def check_anchors(allv):
    return g.check_anchors(allv)
if __name__ == "__main__":
    allv = variants()
    print("variants:", len(allv), " anchor errors:", check_anchors(allv))
    if len(sys.argv) > 1 and sys.argv[1] == "pred":
        for v in allv:
            print("%-6s %-4s %-4s %-10s %s   [%s]" % (v["vid"], v["family"], v["arm"], v["pred"], v["text"], v["note"]))
