#!/usr/bin/env python3
"""Opus seat, #545 repair-3d pass (q2g): NEW one-line shapes, scored on the frozen 864-row 3d instrument (6c92d7e5).

Each carries a PREDICTION written before any run:
  RED         -- a row goes red (target = the row(s) expected; these are CONTROLS: they prove a channel IS read)
  GREEN-DISC  -- green, a real change that the 3d contract's NOT COVERED list names (quoted in `note`)
  GREEN-REAL  -- green, a real change NOT named there -- a finding if measured so
Every `old` must occur exactly once in the frozen device (check_anchors()); none of these shapes is among the 739
the main loop carried (existing_edits.txt, catalogued from /tmp/fbd5r3d_var).
"""
import io, sys

FROZEN = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2g/frozen/dev_footbridge.c"
T, NL = "\t", "\n"

# ---- anchors (each unique in the frozen device; checked) ----
RD = {  # the four status-read lines, with enough context to be unique
    "A0": T * 3 + "odata = d->irq_status & d->irq_enable;",
    "A1": T * 3 + "odata = d->irq_status;" + NL + T * 2 + "else if (!d->warned_irq_raw_w) {",
    "A3": T * 3 + "odata = d->fiq_status & d->fiq_enable;",
    "A4": T * 3 + "odata = d->fiq_status;" + NL + T * 2 + "else if (!d->warned_fiq_raw_w) {",
}
BODY = {"A0": "d->warned_irq_status_w = 1;", "A1": "d->warned_irq_raw_w = 1;", "A2": "d->warned_irq_clear_r = 1;",
        "A3": "d->warned_fiq_status_w = 1;", "A4": "d->warned_fiq_raw_w = 1;"}
DIR = {  # direction test + its first body line
    "A0": T * 2 + "if (writeflag == MEM_READ)" + NL + T * 3 + "odata = d->irq_status & d->irq_enable;",
    "A1": T * 2 + "if (writeflag == MEM_READ)" + NL + T * 3 + "odata = d->irq_status;",
    "A2": T * 2 + "if (writeflag == MEM_WRITE) {" + NL + T * 3 + "d->irq_enable &= ~idata;",
    "A3": T * 2 + "if (writeflag == MEM_READ)" + NL + T * 3 + "odata = d->fiq_status & d->fiq_enable;",
}
LATCH = {"A3": T * 2 + "else if (!d->warned_fiq_status_w) {"}
CLR = [T * 3 + "d->irq_enable &= ~idata;", T * 3 + "if (d->irq_status & d->irq_enable)",
       T * 4 + "INTERRUPT_ASSERT(d->irq);", T * 3 + "else", T * 4 + "INTERRUPT_DEASSERT(d->irq);"]
CLR_TAIL = NL + T * 2 + "} else if (!d->warned_irq_clear_r) {"
CLR_OLD = NL.join(CLR) + CLR_TAIL
IDL = T + "if (writeflag == MEM_WRITE)" + NL + T * 2 + "idata = memory_readmax64(cpu, data, len);" + NL + NL \
    + T + "if (relative_addr >= TIMER_1_LOAD"
FOLD = T + "if (relative_addr >= TIMER_1_LOAD && relative_addr <= TIMER_4_CLEAR) {"
TXT0 = T * 3 + "fatal(\"[ WARNING: footbridge write to irq status? \""

V = []


def add(vid, fam, arm, old, new, text, pred, target="", note=""):
    V.append(dict(vid=vid, family=fam, arm=arm, old=old, new=new, text=text, pred=pred, target=target, note=note))


def read_(vid, fam, arm, stmt, pred, target="", note=""):
    old = RD[arm]
    first = old.split(NL)[0]
    add(vid, fam, arm, old, old.replace(first, T * 3 + stmt, 1), stmt, pred, target, note)


def body_(vid, fam, arm, stmt, pred, target="", note=""):
    add(vid, fam, arm, T * 3 + BODY[arm], T * 3 + stmt, stmt, pred, target, note)


def dir_(vid, fam, arm, expr, pred, target="", note=""):
    old = DIR[arm]
    first = old.split(NL)[0]
    tail = " {" if first.endswith("{") else ""
    add(vid, fam, arm, old, old.replace(first, T * 2 + "if (" + expr + ")" + tail, 1), "if (" + expr + ")" + tail,
        pred, target, note)


def latch_(vid, fam, arm, expr, pred, target="", note=""):
    add(vid, fam, arm, LATCH[arm], T * 2 + "else if (" + expr + ") {", "else if (" + expr + ") {", pred, target, note)


def clr_(vid, fam, idx, line, pred, target="", note=""):
    L = list(CLR)
    L[idx] = line
    add(vid, fam, "A2", CLR_OLD, NL.join(L) + CLR_TAIL, line.strip(), pred, target, note)


def fetch_line(vid, fam, stmt, pred, target="", note=""):
    add(vid, fam, "head", IDL, IDL.replace(T * 2 + "idata = memory_readmax64(cpu, data, len);", T * 2 + stmt, 1),
        stmt, pred, target, note)


def fetch_test(vid, fam, expr, pred, target="", note=""):
    add(vid, fam, "head", IDL, IDL.replace(T + "if (writeflag == MEM_WRITE)", T + "if (" + expr + ")", 1),
        "if (" + expr + ") idata = ...", pred, target, note)


ASRT = "d->irq_asserted && !(d->irq_status & d->irq_enable)"     # the asserted Clear that DEASSERTS (X14 k = 0)

# ==== AS: the channels 3d added -- are they complete at the OTHER asserted / DEVINIT-asserting accesses? ====
read_("AS01", "AS", "A0", "odata = d->irq_status & d->irq_enable, d->warned_irq_raw_w |= d->irq_asserted;", "GREEN-REAL",
      note="the asserted IRQ_STATUS read (X14's cell) consumes +0x184's latch: its first declined write is never "
           "announced.  Host log only.  The row reads the five fields, not the latches, and no decline follows it")
clr_("AS02", "AS", 0, T * 3 + "d->irq_enable &= ~idata, d->warned_irq_status_w |= d->irq_asserted;", "GREEN-REAL",
     note="the asserted Clear (X14's cell, both ways) consumes +0x180's latch.  Host log only.  No decline follows "
          "rows k=0/k=1; the re-arm row's Clear comes after all five latched")
clr_("AS03", "AS", 0, T * 3 + "d->irq_enable &= ~idata, d->fiq_enable |= " + ASRT + ";", "GREEN-REAL",
     note="fiq_enable bit 0 set by the asserted DEASSERTING Clear.  Guest-invisible (fiq_status has no writer, so "
          "FIQ_STATUS = fiq_status & fiq_enable stays 0)")
clr_("AS04", "AS", 0, T * 3 + "d->irq_enable &= ~idata, d->fiq_status |= " + ASRT + ";", "GREEN-REAL",
     note="fiq_status bit 0 set by the asserted DEASSERTING Clear -- GUEST-VISIBLE: FIQ_RAW_STATUS (+0x284) reads 1 "
          "after an ISR masks the line it is servicing.  Row k=0 reads enable/raw status/CPU line, not the FIQ fields")
clr_("AS04b", "AS", 0, T * 3 + "d->irq_enable &= ~idata, d->fiq_status |= d->irq_asserted && "
     "(d->irq_status & d->irq_enable) != 0;", "RED",
     "X14 re-arm row ONLY (its Clear 0x400 is the asserted ASSERTING Clear; E4 reads fiq_status at its end)",
     note="control: the asserting polarity of AS04")
read_("AS05", "AS", "A0", "odata = d->irq_status & d->irq_enable, d->fiq_status |= d->irq_asserted;", "RED",
      "X14 IRQ_STATUS-read row (E2) and the re-arm row (+0x284 read, and its end)", note="control for E2")
body_("AS06", "AS", "A0", "d->warned_irq_status_w = 1; d->fiq_status |= d->irq_asserted;", "RED",
      "X14 re-arm row ONLY (+0x284 read after the decline, and E4 at its end)", note="control for E4")
read_("AS07", "AS", "A1", "odata = d->irq_status, d->warned_irq_status_w |= d->irq_asserted;", "GREEN-DISC",
      note="the asserted +0x184 read consumes +0x180's latch -- only rowed with the latches SET (re-arm row).  "
           "NOT COVERED: 'irq_asserted = 1 at the other legal accesses and widths'")
clr_("AS08", "AS", 0, T * 3 + "d->irq_enable &= ~idata, d->fiq_status |= d->timer_control[0] && "
     "(d->irq_status & d->irq_enable) != 0;", "GREEN-REAL",
     note="fiq_status bit 0 set by an ASSERTING Clear at DEVINIT timer values (E1's cell) -- GUEST-VISIBLE via "
          "+0x284 on every real cats/netwinder (timer_control reset is PERIODIC).  The E1 rows read the enable, the "
          "raw status and the CPU line; the deasserting DEVINIT Clear's instance is read by the declines row")
clr_("AS09", "AS", 0, T * 3 + "d->irq_enable &= ~idata, d->irq_status |= (d->timer_control[0] && "
     "(d->irq_status & d->irq_enable)) ? 0x100u : 0u;", "RED", "X14 DEVINIT Clear 0x20 rows x2 (E1)",
     note="control for E1: the raw status changed (not zeroed, unlike CXC1)")

# ==== SR: a STORE, from the five arms or the Clear, to state no row reads after the access ====
body_("SR01", "SR", "A0", "d->warned_irq_status_w = 1; d->timer_control[0] = 0;", "GREEN-REAL",
      note="a declined IRQ_STATUS write disables timer 1 -- GUEST-VISIBLE (TIMER_1_CONTROL reads 0; the clock stops). "
           "X6/X14 read the four interrupt fields only")
read_("SR02", "SR", "A0", "odata = d->irq_status & d->irq_enable, d->pending_timer_interrupts[0] = 0;", "GREEN-REAL",
      note="every IRQ_STATUS read drops timer 1's pending ticks -- GUEST-VISIBLE (a backlog is lost: #474's lost-"
           "interrupt class, at the register an ISR reads first).  X14's 'tick pending' reads count interrupt calls, "
           "not the pending count")
clr_("SR03", "SR", 0, T * 3 + "d->irq_enable &= ~idata, d->timer_control[0] &= ~TIMER_ENABLE;", "GREEN-REAL",
     note="every legal Clear write disables timer 1 -- GUEST-VISIBLE")
read_("SR04", "SR", "A1", "odata = d->irq_status, d->timer_value[0] = 0;", "GREEN-REAL",
      note="IRQ_RAW_STATUS read zeroes TIMER_1_VALUE -- GUEST-VISIBLE")
body_("SR05", "SR", "A2", "d->warned_irq_clear_r = 1; d->timer_load[0] = 0;", "GREEN-REAL",
      note="the declined +0x18c read zeroes TIMER_1_LOAD -- GUEST-VISIBLE")
body_("SR06", "SR", "A4", "d->warned_fiq_raw_w = 1; reload_timer_value(cpu, d, 0);", "GREEN-REAL",
      note="the declined +0x284 write reloads timer 1 -- GUEST-VISIBLE (TIMER_1_VALUE jumps to the load)")
body_("SR07", "SR", "A3", "d->warned_fiq_status_w = 1; d->pending_bound[0] = 0;", "GREEN-REAL",
      note="the declined +0x280 write zeroes timer 1's pending bound (backlog coalesced to 1)")
clr_("SR08", "SR", 0, T * 3 + "d->irq_enable &= ~idata, d->pending_timer_interrupts[0] = 0;", "GREEN-REAL",
     note="every legal Clear write drops timer 1's pending ticks -- GUEST-VISIBLE")
read_("SR09", "SR", "A3", "odata = d->fiq_status & d->fiq_enable, d->timer_control[1] = 0;", "GREEN-REAL",
      note="FIQ_STATUS read disables timer 2 -- GUEST-VISIBLE")
fetch_line("SR10", "SR", "idata = memory_readmax64(cpu, data, len), d->pending_timer_interrupts[0] = 0;", "RED",
           "the fbclearread/timer rows at the top of the file (a TIMER_1_CLEAR write with pending 2 wants 1)",
           note="control: the same store in the SHARED head is seen by the timer rows")
body_("SR11", "SR", "A1", "d->warned_irq_raw_w = 1; d->timer[0] = NULL;", "GREEN-REAL",
      note="the declined +0x184 write forgets timer 1's host timer: the next reload adds a SECOND one (double rate)")

# ==== CX: the CALLER context beyond `mem` and the machine type (NOT COVERED names only those two) ====
dir_("CX01", "CX", "A1", "writeflag == MEM_READ && !cpu->running", "GREEN-REAL",
     note="every real IRQ_RAW_STATUS read declined (returns 0; the first announces) -- GUEST-VISIBLE in 2 steps.  "
          "The harness cpu is calloc'd: running false; emul.c sets it true")
dir_("CX02", "CX", "A0", "writeflag == MEM_READ && cpu->byte_order != EMUL_LITTLE_ENDIAN", "GREEN-REAL",
     note="every IRQ_STATUS read on a little-endian ARM declined -- GUEST-VISIBLE.  cpu_arm.c sets byte_order LE; the "
          "harness leaves 0 (EMUL_UNDEFINED_ENDIAN)")
clr_("CX03", "CX", 1, T * 3 + "if ((d->irq_status & d->irq_enable) && !cpu->is_32bit)", "GREEN-REAL",
     note="on a 32-bit CPU a Clear never asserts: a Clear leaving a line pending DROPS the CPU line -- GUEST-VISIBLE "
          "(lost interrupt).  X14 counts the CPU line, but its cpu has is_32bit 0")
latch_("CX04", "CX", "A3", "!d->warned_fiq_status_w && !cpu->running", "GREEN-REAL",
       note="in a real run the declined FIQ_STATUS write is never announced (host log only; like MC05)")
fetch_test("CX05", "CX", "writeflag == MEM_WRITE && !cpu->running", "GREEN-REAL",
           note="in a real run EVERY write fetches 0 -- GUEST-VISIBLE (a Clear clears nothing; every register write "
                "is 0).  A head test.  The top-of-file timer rows run with the same calloc'd cpu")
dir_("CX06", "CX", "A2", "writeflag == MEM_WRITE && !cpu->ninstrs", "GREEN-REAL",
     note="after the first instruction every Clear write goes to the +0x18c decline -- GUEST-VISIBLE")
add("CX07", "CX", "head", FOLD, T + "if (relative_addr >= TIMER_1_LOAD && relative_addr <= TIMER_4_CLEAR && "
    "!cpu->running) {", "fold: ... && !cpu->running", "GREEN-REAL",
    note="in a real run timers 2-4 never fold: their registers fall to default -- GUEST-VISIBLE.  A head test")
dir_("CX08", "CX", "A0", "writeflag == MEM_READ && !cpu->machine->ncpus", "GREEN-REAL",
     note="machine->ncpus is 1 in a real run, 0 in the harness")

# ==== RS: the raw status at an asserted Clear, in states X14 does not build (E3 reads 0x10 at k = 0 and k = 1) ====
clr_("RS01", "RS", 0, T * 3 + "d->irq_enable &= ~idata, d->irq_status &= d->irq_asserted ? (d->irq_enable | "
     "(uint32_t) idata) : ~0u;", "GREEN-DISC",
     note="FS01 minus the lines this Clear masks: a line ALREADY masked and pending is dropped from the raw status -- "
          "guest-visible (lost interrupt when re-enabled).  Needs status to hold a masked line while asserted; the "
          "line-4 instance holds status == enable.  NOT COVERED: 'JOINT conditions beyond the rowed combinations'")
clr_("RS02", "RS", 0, T * 3 + "d->irq_enable &= ~idata, d->irq_status &= (d->irq_asserted && (idata & "
     "~d->irq_status)) ? d->irq_enable : ~0u;", "GREEN-DISC",
     note="FS01 only when the Clear also masks a line that is not pending: k=0's 0x10 is pending, k=1's store is a "
          "no-op (status == enable).  JOINT, as RS01")

# ==== IAS: irq_asserted SET where it was 0 ====
body_("IAS01", "IAS", "A0", "d->warned_irq_status_w = 1; d->irq_asserted = 1;", "GREEN-DISC",
      note="visible only through the producer's deassert, which nothing here calls.  NOT COVERED: the producer "
           "pair and the LEVEL line")
clr_("IAS02", "IAS", 2, T * 4 + "d->irq_asserted = 1, INTERRUPT_ASSERT(d->irq);", "GREEN-DISC",
     note="the asserting Clear records irq_asserted -- half of fbirqstuck's F13 fix; 3d leaves it unpinned on purpose")

# ==== FMT: the announce TEXT, where the text is a FORMAT (the real fatal() is vsnprintf(buf, fmt, argp)) ====
add("FMT01", "FMT", "A0", TXT0, T * 3 + "fatal(\"[ WARNING: footbridge write to irq status? %s \"",
    "the +0x180 announce gains a %s with no argument", "GREEN-DISC",
    note="NOT COVERED: 'the announce TEXT' (TX01) -- but this text is a vsnprintf FORMAT: undefined behaviour in the "
         "product (a read of a missing vararg), in the one access #545 made survivable.  fatal() is stubbed here and "
         "has no format attribute, so no compiler sees it either")

# ==== FW: E5's fill -- does a fetch past len reach every narrow Clear? ====
fetch_line("FW01", "FW", "idata = memory_readmax64(cpu, data, relative_addr == IRQ_ENABLE_CLEAR ? 4 : len);", "RED",
           "X12/X13 narrow Clears in wide and ones (16, as R3D_FW1)", note="control: FW1 aimed at the Clear only")
fetch_line("FW02", "FW", "idata = memory_readmax64(cpu, data, len) | (len == 1 ? (uint64_t) data[1] << 8 : 0);",
           "RED", "X12/X13 len-1 Clears in the ONES state (4); wide holds no enable bit 8-15",
           note="a one-byte over-read that lands in byte 1 -- only the ones state has enable bits there")
fetch_line("FW03", "FW", "idata = memory_readmax64(cpu, data, len == 4 ? 8 : len);", "EQ",
           note="EQUIVALENT for the Clear: irq_enable is 32 bits, so bytes 4-7 of an 8-byte fetch are truncated by "
                "`&= ~idata`.  (Set/FIQ/timer arms at len 4: the same truncation, 32-bit fields.)")


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
            print("%-6s %-4s %-4s %-10s %s   [%s%s]" % (v["vid"], v["family"], v["arm"], v["pred"], v["text"],
                                                      ("target: " + v["target"] + "; ") if v["target"] else "",
                                                      v["note"]))
