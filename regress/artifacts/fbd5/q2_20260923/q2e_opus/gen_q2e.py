#!/usr/bin/env python3
"""Opus seat, #545 repair-3 pass (q2e): NEW one-line shapes, scored on the frozen 862-row instrument.

Each carries a PREDICTION written before any run: RED; EQ (green, equivalent); GREEN-DISC (green, a real change the
862-row contract's NOT COVERED list names); GREEN-REAL (green, a real change NOT named there -- a finding if measured so).
`target` names the row(s) a RED is predicted on, where that is the point of the shape.
Every `old` must occur exactly once in the frozen device (check_anchors()).
"""
import io, sys

FROZEN = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2e/frozen/dev_footbridge.c"
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


# ---- B: Q1(b) -- a one-line variant for each of the 8 X14 rows that no one of the 652 reddens ALONE
clr_("B_NS", "B_sole", 1, T * 3 + "if ((d->irq_status & d->irq_enable) || (!d->irq_status && d->irq_enable))", "RED",
     "X14 no-status row ONLY")
clr_("B_L4", "B_sole", 1, T * 3 + "if (d->irq_status & d->irq_enable & ~((d->irq_status == d->irq_enable && "
     "!d->irq_asserted) ? 0x10u : 0u))", "RED", "X14 line-4 row ONLY")
read_("B_DR", "B_sole", "A1", "odata = (d->timer_control[0] && !d->pending_timer_interrupts[0]) ? 0 : d->irq_status;",
      "RED", "X14 DEVINIT reads row ONLY")
read_("B_TR", "B_sole", "A1", "odata = d->pending_timer_interrupts[0] ? 0 : d->irq_status;", "RED",
      "X14 tick-pending reads row ONLY")
clr_after("B_DS", "B_sole", T * 3 + "if (d->timer_control[0] && !d->pending_timer_interrupts[0]) return 0;", "RED",
          "X14 DEVINIT Set/Clear row ONLY")
clr_after("B_TS", "B_sole", T * 3 + "if (d->pending_timer_interrupts[0]) return 0;", "RED",
          "X14 tick-pending Set/Clear row ONLY")
body_("B_DD", "B_sole", "A2", "d->warned_irq_clear_r = 1; odata = d->timer_control[0] && !d->pending_timer_interrupts[0];",
      "RED", "X14 DEVINIT declines row ONLY")
body_("B_TD", "B_sole", "A2", "d->warned_irq_clear_r = 1; odata = d->pending_timer_interrupts[0] != 0;", "RED",
      "X14 tick-pending declines row ONLY")
# ---- IA: irq_asserted = 1 at the other legal accesses and widths, and at X14's own cells on channels it does not read
dir_("IA01", "IA", "A1", "writeflag == MEM_READ && !d->irq_asserted", "GREEN-DISC", note="IRQ_RAW_STATUS in the ISR reads 0")
dir_("IA02", "IA", "A3", "writeflag == MEM_READ && !d->irq_asserted", "GREEN-DISC", note="host only: fiq_status is 0")
dir_("IA03", "IA", "A4", "writeflag == MEM_READ && !d->irq_asserted", "GREEN-DISC", note="host only")
dir_("IA04", "IA", "A0", "writeflag == MEM_READ && (len == 4 || !d->irq_asserted)", "GREEN-DISC",
     note="byte/half/8-byte status read in the ISR")
dir_("IA05", "IA", "A2", "writeflag == MEM_WRITE && (len == 4 || !d->irq_asserted)", "GREEN-DISC",
     note="narrow Clear in the ISR declined")
fetch_("IA06", "IA", "writeflag == MEM_WRITE && (len == 4 || !d->irq_asserted)", "GREEN-DISC",
       note="narrow writes in the ISR fetch 0")
clr_("IA07", "IA", 1, T * 3 + "if ((d->irq_status & d->irq_enable) && (len == 4 || !d->irq_asserted))", "GREEN-DISC",
     note="narrow Clear in the ISR never asserts")
flag_("IA08", "IA", "A0", "!d->warned_irq_status_w && !d->irq_asserted", "RED", "X14 re-arm row")
read_("IA09", "IA", "A1", "odata = d->irq_status, d->warned_irq_status_w &= !d->irq_asserted;", "RED", "X14 re-arm row")
clr_("IA10", "IA", 0, T * 3 + "d->irq_enable &= ~idata, d->warned_fiq_raw_w &= !d->irq_asserted;", "RED", "X14 re-arm row")
read_("IA11", "IA", "A0", "odata = d->irq_status & d->irq_enable, d->warned_irq_raw_w &= !(d->irq_asserted && len == 2);",
      "GREEN-DISC", note="host: a latch clearer at another width")
read_("IA12", "IA", "A0", "odata = d->irq_status & d->irq_enable, d->irq_status &= d->irq_asserted ? ~d->irq_enable : ~0u;",
      "GREEN-REAL", note="X14's asserted IRQ_STATUS read checks no field after the read")
read_("IA13", "IA", "A0", "odata = d->irq_status & d->irq_enable, d->irq_asserted ? INTERRUPT_DEASSERT(d->irq) : (void) 0;",
      "GREEN-REAL", note="X14's asserted IRQ_STATUS read checks no interrupt call after the read")
body_("IA14", "IA", "A0", "d->warned_irq_status_w = 1; if (d->irq_asserted) INTERRUPT_DEASSERT(d->irq);", "GREEN-REAL",
      note="X14's re-arm row checks no interrupt call at its declines")
read_("IA15", "IA", "A1", "odata = (d->irq_asserted && d->warned_irq_raw_w) ? 0 : d->irq_status;", "GREEN-DISC",
      note="joint irq_asserted x latch at another legal access")
read_("IA16", "IA", "A0", "odata = (d->irq_asserted && d->warned_irq_status_w) ? 0 : d->irq_status & d->irq_enable;",
      "GREEN-REAL", note="X14's re-arm row makes this read and checks only its return value")
# ---- TD: DEVINIT's timer values / a tick pending, at X14's own cells, on the channels those rows do not read
clr_("TD01", "TD", 1, T * 3 + "if ((d->irq_status & d->irq_enable) && !d->timer_control[0])", "GREEN-REAL",
     note="the DEVINIT Set/Clear row checks no interrupt call")
clr_("TD02", "TD", 1, T * 3 + "if ((d->irq_status & d->irq_enable) && !d->pending_timer_interrupts[0])", "GREEN-REAL",
     note="timer 0's tick is X14's cell; its Set/Clear row checks no call")
clr_("TD03", "TD", 1, T * 3 + "if ((d->irq_status & d->irq_enable) || d->timer_control[0])", "GREEN-REAL",
     note="from reset a Clear always asserts")
body_("TD04", "TD", "A0", "d->warned_irq_status_w = 1; if (d->timer_control[0]) INTERRUPT_DEASSERT(d->irq);", "GREEN-REAL",
      note="the DEVINIT declines row checks no interrupt call")
body_("TD05", "TD", "A2", "d->warned_irq_clear_r = 1; odata = d->timer_control[0] ? d->irq_enable : 0;", "RED",
      "X14 DEVINIT declines rows (declined read value)")
dir_("TD06", "TD", "A0", "writeflag == MEM_READ && (len != 1 || !d->timer_control[0])", "GREEN-DISC",
     note="a byte status read from reset declined")
fetch_("TD07", "TD", "writeflag == MEM_WRITE && (len != 2 || !d->pending_timer_interrupts[0])", "GREEN-DISC",
       note="timer 0 tick at another width: named only by the catch-all's head")
dir_("TD08", "TD", "A1", "writeflag == MEM_READ && !d->pending_timer_interrupts[1]", "GREEN-DISC", note="another timer")
dir_("TD09", "TD", "A2", "writeflag == MEM_WRITE && !(d->timer_control[0] & TIMER_ENABLE)", "GREEN-DISC",
     note="timer 1 enabled: every Clear declined")
flag_("TD10", "TD", "A3", "!d->warned_fiq_status_w && d->timer_load[0] != TIMER_MAX_VAL", "RED", "X14 DEVINIT declines rows")
dir_("TD11", "TD", "A4", "writeflag == MEM_READ || d->pending_timer_interrupts[0]", "RED", "X14 tick declines row")
clr_("TD12", "TD", 1, T * 3 + "if ((d->irq_status & d->irq_enable) || d->pending_timer_interrupts[0])", "GREEN-REAL",
     note="a Clear with a tick pending always asserts")
clr_("TD13", "TD", 0, T * 3 + "d->irq_enable &= d->timer_control[0] ? ~(idata & 0xffff) : ~idata;", "GREEN-DISC",
     note="from reset a Clear ignores enable bits 16-31 (PCI line 18); X14's DEVINIT Clear writes 0x10")
# ---- PR: the producer pair (Q2's edit space names it); x14_line raises line 4 once from an empty status, never lowers
add("PR01", "PR", "prod", PA_OR, T + "d->irq_status = interrupt->line;", "d->irq_status = interrupt->line;  (assert)",
    "GREEN-REAL", note="a second raised line wipes the first")
add("PR02", "PR", "prod", PA_IF, T + "if ((d->irq_status & d->irq_enable) && !d->irq_asserted) {",
    "if ((d->irq_status & d->irq_enable) && !d->irq_asserted) {  (assert: the commented-out NetBSD form)", "GREEN-REAL",
    note="stale irq_asserted after a Clear: a later enabled line is never delivered")
add("PR03", "PR", "prod", PA_IF, T + "if (d->irq_enable) {", "if (d->irq_enable) {  (assert)", "GREEN-REAL",
    note="a line that is not enabled raises the CPU line")
add("PR04", "PR", "prod", PD_AND, T + "d->irq_status &= interrupt->line;", "d->irq_status &= interrupt->line;  (deassert)",
    "GREEN-REAL", note="lowering one line clears every OTHER pending line and keeps its own")
add("PR05", "PR", "prod", PD_IF, T + "if (!(d->irq_status & d->irq_enable)) {", "if (!(d->irq_status & d->irq_enable)) {  (deassert)",
    "GREEN-DISC", note="differs only where an enable arm left the CPU line high with irq_asserted 0: fbirqstuck's level")
add("PR06", "PR", "prod", PD_BODY, T * 2 + ";" + NL + T * 2 + "INTERRUPT_DEASSERT(d->irq);",
    "d->irq_asserted = 0; deleted  (deassert)", "GREEN-DISC", note="differs only in fbirqstuck's state (the level)")
add("PR07", "PR", "prod", PD_BODY, T * 2 + "d->irq_asserted = 0;" + NL + T * 2 + ";", "INTERRUPT_DEASSERT(d->irq); deleted  (deassert)",
    "GREEN-REAL", note="a device lowering its line leaves the CPU line high")
add("PR08", "PR", "prod", PA_BODY, T * 2 + "d->irq_asserted = 1;" + NL + T * 2 + "INTERRUPT_ASSERT(d->timer_irq[0]);",
    "INTERRUPT_ASSERT(d->timer_irq[0]);  (assert)", "RED", "X14 IRQ_STATUS-read row (the raise's CPU check)")
add("PR09", "PR", "prod", PA_BODY, T * 2 + "d->irq_asserted = 0;" + NL + T * 2 + "INTERRUPT_ASSERT(d->irq);",
    "d->irq_asserted = 0;  (assert)", "RED", "X14 irq_asserted rows")
# ---- J: the drive test's disjoint / status-zero cells with a latch SET (X14 rows them with every latch clear)
clr_("J01", "J", 1, T * 3 + "if ((d->irq_status & d->irq_enable) || (d->warned_irq_clear_r && d->irq_enable))", "GREEN-DISC",
     note="joint drive x latch: named only by the joints line's head")
clr_("J02", "J", 1, T * 3 + "if (d->warned_irq_clear_r ? (d->irq_status && d->irq_enable) : (d->irq_status & d->irq_enable))",
     "GREEN-DISC", note="`&&` once +0x18c's latch is set")
# ---- W: other instance fields, the 8-byte upper word, the fold under irq_asserted
read_("W01", "W", "A0", "odata = (d->irq_status & d->irq_enable) | (len == 8 ? (uint64_t) d->irq_status << 32 : 0);", "RED",
      "X9/X10 len-8 IRQ_STATUS rows (they PIN the upper word to 0)")
dir_("W02", "W", "A0", "writeflag == MEM_READ && !d->timer[0]", "GREEN-DISC", note="timer 1 enabled: the host timer handle")
clr_("W03", "W", 1, T * 3 + "if ((d->irq_status & d->irq_enable) && d->irq.extra == NULL)", "GREEN-REAL",
     note="DEVINIT connects d->irq (extra = the cpu); every row's d->irq.extra is NULL")
dir_("W04", "W", "A1", "writeflag == MEM_READ && !d->pcibus", "GREEN-REAL", note="DEVINIT sets pcibus; every row's is NULL")
flag_("W05", "W", "A0", "!d->warned_irq_status_w && !d->console_handle", "GREEN-DISC", note="a latch guard: named")
add("W06", "W", "head", FOLD, T + "if (relative_addr >= TIMER_1_LOAD && relative_addr <= TIMER_4_CLEAR && !d->irq_asserted) {",
    "fold only when !d->irq_asserted", "GREEN-DISC", note="other registers only")


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
            print("%-5s %-6s %-4s %-10s %s   [%s%s]" % (v["vid"], v["family"], v["arm"], v["pred"], v["text"],
                                                       ("target: " + v["target"] + "; ") if v["target"] else "", v["note"]))
