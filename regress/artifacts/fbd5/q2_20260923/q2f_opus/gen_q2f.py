#!/usr/bin/env python3
"""Opus seat, #545 repair-3c pass (q2f): NEW one-line shapes, scored on the frozen 864-row instrument.

Each carries a PREDICTION written before any run: RED; EQ (green, equivalent); GREEN-DISC (green, a real change the
864-row contract's NOT COVERED list names); GREEN-REAL (green, a real change NOT named there -- a finding if measured so).
`target` names the row(s) a RED is predicted on, where that is the point of the shape.
Every `old` must occur exactly once in the frozen device (check_anchors()).
"""
import io, sys

FROZEN = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2f/frozen/dev_footbridge.c"
T, NL = "\t", "\n"

ARMS = {
    "A0": dict(dir_old=T * 2 + "if (writeflag == MEM_READ)" + NL + T * 3 + "odata = d->irq_status & d->irq_enable;",
               flag_old=T * 2 + "else if (!d->warned_irq_status_w) {", body_old=T * 3 + "d->warned_irq_status_w = 1;",
               read_old=T * 3 + "odata = d->irq_status & d->irq_enable;"),
    "A1": dict(dir_old=T * 2 + "if (writeflag == MEM_READ)" + NL + T * 3 + "odata = d->irq_status;",
               flag_old=T * 2 + "else if (!d->warned_irq_raw_w) {", body_old=T * 3 + "d->warned_irq_raw_w = 1;",
               read_old=T * 3 + "odata = d->irq_status;" + NL + T * 2 + "else if (!d->warned_irq_raw_w) {"),
    "A2": dict(dir_old=T * 2 + "if (writeflag == MEM_WRITE) {" + NL + T * 3 + "d->irq_enable &= ~idata;",
               flag_old=T * 2 + "} else if (!d->warned_irq_clear_r) {", body_old=T * 3 + "d->warned_irq_clear_r = 1;"),
    "A3": dict(dir_old=T * 2 + "if (writeflag == MEM_READ)" + NL + T * 3 + "odata = d->fiq_status & d->fiq_enable;",
               flag_old=T * 2 + "else if (!d->warned_fiq_status_w) {", body_old=T * 3 + "d->warned_fiq_status_w = 1;",
               read_old=T * 3 + "odata = d->fiq_status & d->fiq_enable;"),
    "A4": dict(dir_old=T * 2 + "if (writeflag == MEM_READ)" + NL + T * 3 + "odata = d->fiq_status;",
               flag_old=T * 2 + "else if (!d->warned_fiq_raw_w) {", body_old=T * 3 + "d->warned_fiq_raw_w = 1;",
               read_old=T * 3 + "odata = d->fiq_status;" + NL + T * 2 + "else if (!d->warned_fiq_raw_w) {"),
}
CLR = [T * 3 + "d->irq_enable &= ~idata;", T * 3 + "if (d->irq_status & d->irq_enable)",
       T * 4 + "INTERRUPT_ASSERT(d->irq);", T * 3 + "else", T * 4 + "INTERRUPT_DEASSERT(d->irq);"]
CLR_TAIL = NL + T * 2 + "} else if (!d->warned_irq_clear_r) {"
CLR_OLD = NL.join(CLR) + CLR_TAIL
IDL = T + "if (writeflag == MEM_WRITE)" + NL + T * 2 + "idata = memory_readmax64(cpu, data, len);" + NL + NL \
    + T + "if (relative_addr >= TIMER_1_LOAD"
FOLD = T + "if (relative_addr >= TIMER_1_LOAD && relative_addr <= TIMER_4_CLEAR) {"
PA_OR = T + "d->irq_status |= interrupt->line;"
PA_IF = T + "if ((d->irq_status & d->irq_enable) /* && !d->irq_asserted */) {"
PA_BODY = T * 2 + "d->irq_asserted = 1;" + NL + T * 2 + "INTERRUPT_ASSERT(d->irq);"
PD_AND = T + "d->irq_status &= ~interrupt->line;"
PD_IF = T + "if (!(d->irq_status & d->irq_enable) && d->irq_asserted) {"
PD_BODY = T * 2 + "d->irq_asserted = 0;" + NL + T * 2 + "INTERRUPT_DEASSERT(d->irq);"

V = []


def add(vid, fam, arm, old, new, text, pred, target="", note=""):
    V.append(dict(vid=vid, family=fam, arm=arm, old=old, new=new, text=text, pred=pred, target=target, note=note))


def first_line(s):
    return s.split(NL)[0]


def dir_(vid, fam, arm, expr, pred, target="", note=""):
    a = ARMS[arm]
    fl = first_line(a["dir_old"])
    tail = " {" if fl.endswith("{") else ""
    add(vid, fam, arm, a["dir_old"], a["dir_old"].replace(fl, T * 2 + "if (" + expr + ")" + tail, 1),
        "if (" + expr + ")" + tail, pred, target, note)


def flag_(vid, fam, arm, expr, pred, target="", note=""):
    a = ARMS[arm]
    nl = T * 2 + ("} else if (" if arm == "A2" else "else if (") + expr + ") {"
    add(vid, fam, arm, a["flag_old"], nl, nl.strip(), pred, target, note)


def body_(vid, fam, arm, stmt, pred, target="", note=""):
    add(vid, fam, arm, ARMS[arm]["body_old"], T * 3 + stmt, stmt, pred, target, note)


def read_(vid, fam, arm, stmt, pred, target="", note=""):
    old = ARMS[arm]["read_old"]
    add(vid, fam, arm, old, old.replace(first_line(old), T * 3 + stmt, 1), stmt, pred, target, note)


def clr_(vid, fam, idx, line, pred, target="", note=""):
    L = list(CLR)
    L[idx] = line
    add(vid, fam, "A2", CLR_OLD, NL.join(L) + CLR_TAIL, line.strip(), pred, target, note)


def clr_after(vid, fam, line, pred, target="", note=""):
    """insert ONE line after the Clear write's drive (after `INTERRUPT_DEASSERT(d->irq);`)"""
    add(vid, fam, "A2", CLR_OLD, NL.join(CLR) + NL + line + CLR_TAIL, line.strip(), pred, target, note)


def fetch_(vid, fam, expr, pred, target="", note=""):
    add(vid, fam, "head", IDL, IDL.replace(T + "if (writeflag == MEM_WRITE)", T + "if (" + expr + ")", 1),
        "if (" + expr + ") idata = memory_readmax64(...)", pred, target, note)




# ---- P: Q1(a) -- each CHANGED or NEW X14 row red on its own, through the channel 3c gave it; and the four X14 rows
#      that no one of the 711 reddens alone
clr_("P_DJ", "P_sole", 1, T * 3 + "if (d->timer_control[0] ? (d->irq_status & d->irq_enable) : (d->irq_status && d->irq_enable))",
     "RED", "X14 disjoint row ONLY (the `&&` cell, calloc instance only)")
clr_("P_SC0", "P_sole", 1, T * 3 + "if ((d->irq_status & d->irq_enable) || (d->timer_control[0] && !d->pending_timer_interrupts[0]))",
     "RED", "X14 DEVINIT Set/Clear row ONLY (ZCPU(1,1))")
clr_("P_K0", "P_sole", 1, T * 3 + "if ((d->irq_status & d->irq_enable) && !(d->timer_control[0] && !d->pending_timer_interrupts[0]))",
     "RED", "X14 DEVINIT keeps row ONLY (new row)")
clr_("P_A4", "P_sole", 1, T * 3 + "if ((d->irq_status & d->irq_enable) && !(d->irq_asserted && !d->warned_irq_status_w))",
     "RED", "X14 asserted Clear 0x400 row ONLY")
read_("P_RD0c", "P_chan", "A0", "odata = d->irq_status & d->irq_enable, (d->timer_control[0] && "
      "!d->pending_timer_interrupts[0]) ? INTERRUPT_DEASSERT(d->irq) : (void) 0;", "RED",
      "X14 DEVINIT reads row AND its Set/Clear row: the counters run on from the reads (the reads' no-call check holds "
      "nothing alone)")
body_("P_DD0c", "P_chan", "A0", "d->warned_irq_status_w = 1; if (d->timer_control[0] && !d->pending_timer_interrupts[0]) "
      "INTERRUPT_DEASSERT(d->irq);", "RED", "X14 DEVINIT declines row ONLY (the no-call channel)")
body_("P_DD1c", "P_chan", "A0", "d->warned_irq_status_w = 1; if (d->pending_timer_interrupts[0]) INTERRUPT_DEASSERT(d->irq);",
      "RED", "X14 tick declines row ONLY (the no-call channel)")
read_("P_ISf", "P_chan", "A0", "odata = d->irq_status & d->irq_enable, d->irq_status &= (d->irq_asserted && "
      "!d->warned_irq_status_w) ? ~d->irq_enable : ~0u;", "RED", "X14 asserted IRQ_STATUS read ONLY (the fields channel)")
read_("P_ISc", "P_chan", "A0", "odata = d->irq_status & d->irq_enable, (d->irq_asserted && !d->warned_irq_status_w) ? "
      "INTERRUPT_DEASSERT(d->irq) : (void) 0;", "RED", "X14 asserted IRQ_STATUS read ONLY (the no-call channel)")
clr_("P_RAf", "P_chan", 0, T * 3 + "d->irq_enable &= ~idata, d->irq_status &= (d->irq_asserted && d->warned_irq_clear_r) ? "
     "~0x10u : ~0u;", "RED", "X14 re-arm row ONLY (its final fields / one assert)")
read_("P_RAv", "P_chan", "A1", "odata = (d->irq_asserted && d->warned_irq_raw_w) ? (d->irq_status & ~0x10u) : d->irq_status;",
      "RED", "X14 re-arm row ONLY (the read values)")
# ---- FS: field stores at X14's asserted Clear cells, on channels those rows do not name
clr_("FS01", "FS", 0, T * 3 + "d->irq_enable &= ~idata, d->irq_status &= d->irq_asserted ? d->irq_enable : ~0u;",
     "GREEN-REAL", note="the ISR's Clear drops the masked line from the RAW status; the asserted Clear rows read no status")
clr_("FS02", "FS", 0, T * 3 + "d->irq_enable &= ~idata, d->irq_asserted &= (d->irq_status & d->irq_enable) != 0;",
     "GREEN-DISC", note="only a later device-lowered line shows it (a line left high): the producer pair / LEVEL lines")
clr_("FS04", "FS", 0, T * 3 + "d->irq_enable &= ~idata, d->irq_status &= d->timer_control[0] ? ~idata : ~0u;", "RED",
     "X14 DEVINIT declines rows (their final field check, same instance)")
clr_("FS05", "FS", 0, T * 3 + "d->irq_enable &= ~idata, d->irq_status &= d->pending_timer_interrupts[0] ? ~idata : ~0u;",
     "RED", "X14 tick declines row")
# ---- MC: the CALLER context -- the harness calls with mem = NULL and a cpu whose machine type is MACHINE_NONE (0);
#      every real caller passes the memory object and runs as MACHINE_CATS (5002) or MACHINE_NETWINDER (5004)
dir_("MC01", "MC", "A0", "writeflag == MEM_READ && cpu->machine->machine_type != MACHINE_NETWINDER", "GREEN-REAL",
     note="netwinder: IRQ_STATUS reads declined, return 0")
clr_("MC02", "MC", 1, T * 3 + "if ((d->irq_status & d->irq_enable) && cpu->machine->machine_type != MACHINE_CATS)",
     "GREEN-REAL", note="cats: a Clear never asserts")
dir_("MC03", "MC", "A1", "writeflag == MEM_READ && !mem", "GREEN-REAL", note="every real caller: IRQ_RAW_STATUS reads declined")
fetch_("MC04", "MC", "writeflag == MEM_WRITE && !mem", "GREEN-REAL", note="every real caller: every write fetches 0")
flag_("MC05", "MC", "A0", "!d->warned_irq_status_w && cpu->machine->machine_type != MACHINE_CATS", "GREEN-REAL",
      note="cats: declined IRQ_STATUS writes never announced")
clr_("MC07", "MC", 0, T * 3 + "d->irq_enable &= cpu->machine->machine_type == MACHINE_NETWINDER ? ~(idata & 0xff) : ~idata;",
     "GREEN-REAL", note="netwinder: a Clear cannot mask ISA line 11 (bit 11 is in byte 1)")
# ---- TX: the announce TEXT (the rows count fatal() calls)
add("TX01", "TX", "A0", T * 3 + "fatal(\"[ WARNING: footbridge write to irq status? \"",
    T * 3 + "fatal(\"[ WARNING: footbridge write to irq raw status? \"", "the +0x180 announce names +0x184", "GREEN-REAL",
    note="NOT COVERED does not name the text; the P-rows header gives it to the guest rows")


def variants():
    ids = [v["vid"] for v in V]
    assert len(ids) == len(set(ids)), "duplicate ids"
    return V


def check_anchors(allv):
    fz = io.open(FROZEN, encoding="utf-8", newline="").read()
    return [(v["vid"], fz.count(v["old"])) for v in allv if fz.count(v["old"]) != 1 or v["old"] == v["new"]]


if __name__ == "__main__":
    allv = variants()
    print("variants:", len(allv), " anchor errors:", check_anchors(allv))
    if len(sys.argv) > 1 and sys.argv[1] == "pred":
        for v in allv:
            print("%-6s %-6s %-4s %-10s %s   [%s%s]" % (v["vid"], v["family"], v["arm"], v["pred"], v["text"],
                                                        ("target: " + v["target"] + "; ") if v["target"] else "", v["note"]))
