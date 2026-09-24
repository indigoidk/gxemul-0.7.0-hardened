#!/usr/bin/env python3
"""Opus seat, #545 repair-3e pass (q2h): NEW one-line shapes aimed at the EDGES of 3e's two closures --
(A) ZSNAP/ZKEPT after each access in X14's multi-access rows; (B) pad_kept() in X6/X9/X10.
Prediction classes as in gen_shapes.py: RED (control, target rows), GREEN-DISC (real, named by NOT COVERED),
GREEN-REAL (real, NOT named -> a finding), EQ (equivalent/no observable).
Every `old` unique in the frozen device (checked)."""
import io, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_shapes as g  # noqa: E402

T, NL = "\t", "\n"
FROZEN = g.FROZEN
g.V[:] = []

# ---- the common tail, anchored uniquely via the default arm above it (footbridge_isa has the same tail lines) ----
TAIL_OLD = (
    T + "default:if (writeflag == MEM_READ) {" + NL
    + T*3 + "fatal(\"[ footbridge: read from 0x%x ]\\n\"," + NL
    + T*3 + "    (int)relative_addr);" + NL
    + T*2 + "} else {" + NL
    + T*3 + "fatal(\"[ footbridge: write to 0x%x: 0x%llx ]\\n\"," + NL
    + T*3 + "    (int)relative_addr, (long long)idata);" + NL
    + T*2 + "}" + NL
    + T + "}" + NL + NL
    + T + "if (writeflag == MEM_READ)" + NL
    + T*2 + "memory_writemax64(cpu, data, len, odata);" + NL + NL
    + T + "return 1;")


def tail(vid, newtail, pred, target="", note=""):
    new = TAIL_OLD.replace(T*2 + "memory_writemax64(cpu, data, len, odata);",
                           T*2 + newtail, 1)
    g.add(vid, "WB", "tail", TAIL_OLD, new, newtail, pred, target, note)


# ==== (B) pad_kept edges: the tail write-back widened, conditioned on a site ====
tail("QWBIE8", "memory_writemax64(cpu, data, relative_addr == IRQ_ENABLE_CLEAR ? 8 : len, odata);",
     "RED", "X6 +0x18c declined reads at len 1/2/4 (pad_kept)",
     note="CONTROL: (B) covers the DECLINED read's write-back too, not just legal reads")
tail("QWBST8", "memory_writemax64(cpu, data, relative_addr == IRQ_STATUS ? 8 : len, odata);",
     "RED", "X9/X10 IRQ_STATUS reads at len 1/2/4 (pad_kept)",
     note="CONTROL: (B) covers the IRQ_STATUS legal read's write-back at a state X6/X9/X10 build")
tail("QWBVEND", "memory_writemax64(cpu, data, relative_addr == VENDOR_ID ? 8 : len, odata);",
     "GREEN-REAL", "",
     note="a write-back past len at the VENDOR_ID read: X7 reads VENDOR_ID but has NO pad_kept and reads no value; "
          "X6/X9/X10 never read VENDOR_ID.  If green, the tail's memory-safety is UNPINNED at the non-decline reads "
          "(VENDOR_ID, TIMER_1_VALUE) -- outside the five-arm floor, but a real narrow VENDOR_ID load overflows")
tail("QWBTMRV", "memory_writemax64(cpu, data, relative_addr == TIMER_1_VALUE ? 8 : len, odata);",
     "GREEN-REAL", "",
     note="as QWBVEND, at TIMER_1_VALUE (read by X7 only, no pad_kept)")
tail("QTAIL0", "memory_writemax64(cpu, data, 0, odata);",
     "RED", "X9/X10/X6 legal+declined reads (read value wrong AND pad_kept trivially true but value != want)",
     note="CONTROL: writing back nothing leaves the 0xa5 fill -> read value != want")

# ==== (A) ZKEPT edges: a kept field changed at a Clear the re-arm row reaches ====
g.clr_("QCLRFS", "WB", 0, T*3 + "d->irq_enable &= ~idata, d->fiq_status |= d->irq_asserted;", "RED",
       "X14 re-arm row (ZKEPT after ZCLR(0x400), irq_asserted==1)",
       note="CONTROL: (A) covers the re-arm row's Clear -- fiq_status changed there is caught by ZKEPT.  "
            "X12/X13/X9/X10/single-access Clears have irq_asserted==0 so no change")
g.clr_("QCLRIS", "WB", 0, T*3 + "d->irq_enable &= ~idata, d->irq_status |= (uint32_t) d->irq_asserted << 24;", "RED",
       "X14 re-arm row (ZKEPT and its end check x->irq_status==0x10)",
       note="CONTROL: (A) covers irq_status kept at the re-arm Clear")

# ==== (A) ZKEPT blind spot: a within-access transient (changed and restored inside ONE access) ====
g.body_("QZKTR", "WB", "A0", "d->warned_irq_status_w = 1; d->irq_status++; d->irq_status--;", "EQ",
        note="a field changed and RESTORED within one declined IRQ_STATUS write: nets zero, so ZKEPT (checked AFTER "
             "the access) cannot see it -- but it is a NO-OP, no guest-visible state differs.  Not a floor breach")

# ==== (A) irq_asserted at a legal read (disclosed) ====
g.read_("QIASRD", "WB", "A0", "odata = d->irq_status & d->irq_enable; d->irq_asserted = 1;", "GREEN-DISC",
        note="irq_asserted=1 on the legal IRQ_STATUS read: X9/X10/X6 do not check irq_asserted; the X14 line-4 read "
             "row has it already 1.  NOT COVERED: 'irq_asserted = 1 at the other legal accesses and widths'")

# ==== field-exact condition on a decline latch (disclosed) ====
g.latch_("QLATCHX", "WB", "A3", "!d->warned_fiq_status_w && d->fiq_enable != 0x777u", "GREEN-DISC",
         note="a latch guarded by an EXACT field value no state holds: latch still fires -> green.  NOT COVERED: "
              "'a condition on one EXACT field or data value'")

# ==== (A) does 3e catch irq_asserted spuriously SET on a declined write in a DEVINIT declines row? ====
# (this is IAS01 in gen_shapes -- predicted GREEN on 3d, expected RED on 3e; re-scored there.  Here a variant that
#  sets it only on the IRQ_RAW write, another ZDECLINE access, to confirm the ZKEPT catch is per-access.)
g.body_("QIASRAW", "WB", "A1", "d->warned_irq_raw_w = 1; d->irq_asserted = 1;", "RED",
        "X14 DEVINIT declines rows x2 (ZKEPT after the IRQ_RAW write, irq_asserted 0->1)",
        note="the SECOND ZDECLINE access (IRQ_RAW write) sets irq_asserted -- ZKEPT after each access catches it on "
             "the DEVINIT declines rows (irq_asserted starts 0); the re-arm row starts it 1 so no change there")


def variants():
    ids = [v["vid"] for v in g.V]
    assert len(ids) == len(set(ids)), "dup ids"
    return g.V


def check_anchors(allv):
    return g.check_anchors(allv)


if __name__ == "__main__":
    allv = variants()
    print("variants:", len(allv), " anchor errors:", check_anchors(allv))
    if len(sys.argv) > 1 and sys.argv[1] == "pred":
        for v in allv:
            print("%-8s %-3s %-4s %-10s %s   [%s%s]" % (v["vid"], v["family"], v["arm"], v["pred"], v["text"],
                  ("target: " + v["target"] + "; ") if v["target"] else "", v["note"]))
