#!/usr/bin/env python3
"""#549 closing pass (Opus measuring seat): edits of the FINAL dev_fbctrl.c (md5 129694b8) that are NOT among table 3's
62, each ONE text transformation with exactly one match (REFUSED otherwise).

  Q1  DEPENDS-ON: the three predicates dominating the fixed arm -- the PORT case's `writeflag == MEM_READ`,
      `idata >= DEV_FBCTRL_NPORTS`, `!d->warned_port` -- each QUALIFIED with one conjunct over the access width (len) or
      a field the brief lists as body-read (current_port, port[COMMAND]), or with an operand swapped for one.
      E_* are predicted to escape; C_* are CONTROLS on the same axis, predicted red (they show the axis is observable,
      so an escape is about which CELL is rowed, not about a blind channel).
  B   the contract's re-announce boundary: period 11 (claimed caught) and 12 (disclosed).
  Q2  the R session's "refuse 9 after the NOP, PORT keeps 5" row: a single-site edit aimed at R's second refusal, and a
      two-part edit whose parts are each built ALONE first (licensed composite shape (ii)).
usage: gen_close.py <fix.c> <outdir>"""
import io
import os
import sys

RD = "\t\tif (writeflag == MEM_READ)\n\t\t\todata = d->current_port;\n"
PRED = "else if (idata >= DEV_FBCTRL_NPORTS) {"
LATCH = "if (!d->warned_port) {"
LATCH_END = "\t\t\t\td->warned_port = 1;\n\t\t\t}\n"
CMD_ENTRY = "\tint x1, y1, i;\n"
CMDC = "d->port[DEV_FBCTRL_PORT_COMMAND]"


def rd(cond):
    return [(RD, "\t\tif (%s)\n\t\t\todata = d->current_port;\n" % cond)]


def pred(cond):
    return [(PRED, "else if (%s) {" % cond)]


def latch(cond):
    return [(LATCH, "if (%s) {" % cond)]


EDITS = [
    # ---- Q1, predicted ESCAPES
    ("E_rd_w4", "Q1 read x width: a 1/2-byte PORT read falls into the write path (selects 0, reads 0)",
     rd("writeflag == MEM_READ && len >= 4")),
    ("E_rd_cmd", "Q1 read x COMMAND: a PORT read while COMMAND != 0 falls into the write path",
     rd("writeflag == MEM_READ && !" + CMDC)),
    ("E_ref_p1", "Q1 refuse x previous selector 1: the value is STORED when the previous selector is 1",
     pred("idata >= DEV_FBCTRL_NPORTS && d->current_port != 1")),
    ("E_ref_p2", "Q1 refuse x previous selector 2", pred("idata >= DEV_FBCTRL_NPORTS && d->current_port != 2")),
    ("E_ref_p3", "Q1 refuse x previous selector 3", pred("idata >= DEV_FBCTRL_NPORTS && d->current_port != 3")),
    ("E_ref_p4", "Q1 refuse x previous selector 4", pred("idata >= DEV_FBCTRL_NPORTS && d->current_port != 4")),
    ("E_ref_cmd", "Q1 refuse x COMMAND: the value is STORED while COMMAND != 0 (e.g. after GET_RESOLUTION)",
     pred("idata >= DEV_FBCTRL_NPORTS && !" + CMDC)),
    ("E_ann_w4", "Q1 announce x width: only a 4-byte refusal announces (and sets the latch)",
     latch("!d->warned_port && len == 4")),
    ("E_ann_p1", "Q1 announce x previous selector 1: no announce (latch unset) when the previous selector is 1",
     latch("!d->warned_port && d->current_port != 1")),
    ("E_ann_cmd", "Q1 announce x COMMAND: no announce (latch unset) while COMMAND != 0",
     latch("!d->warned_port && !" + CMDC)),
    # ---- Q1 CONTROLS on the same axes, predicted RED
    ("C_rd_w4only", "control: only a 4-byte PORT read is a read (the ld falls through)",
     rd("writeflag == MEM_READ && len == 4")),
    ("C_ref_p0", "control: refusal skipped when the previous selector is 0",
     pred("idata >= DEV_FBCTRL_NPORTS && d->current_port != 0")),
    ("C_ref_p7", "control: refusal skipped when the previous selector is 7",
     pred("idata >= DEV_FBCTRL_NPORTS && d->current_port != 7")),
    ("C_ann_nw4", "control: a 4-byte refusal never announces", latch("!d->warned_port && len != 4")),
    ("C_ann_p5", "control: no announce when the previous selector is 5",
     latch("!d->warned_port && d->current_port != 5")),
    ("S_ref_wp", "swap: the bound raised by the latch (8 accepted once latched)",
     pred("idata >= DEV_FBCTRL_NPORTS + d->warned_port")),
    ("S_rd_idata", "swap: a write of 0 is taken as a read (ignored)", rd("writeflag == MEM_READ || idata == 0")),
    ("S_ann_cp", "swap: announce only when the previous selector is non-zero",
     latch("!d->warned_port && d->current_port")),
    # ---- B: the contract's period boundary
    ("B_mod11", "boundary: the latch counts modulo 11 (re-announces on the 12th refusal) -- claimed caught",
     latch("!(d->warned_port++ % 11)")),
    ("B_mod12", "boundary: the latch counts modulo 12 (re-announces on the 13th) -- disclosed",
     latch("!(d->warned_port++ % 12)")),
    # ---- Q2: the R session's keeps-5 row
    ("R_state1", "R: the refusal stores 9 in R's second-refusal STATE (latched, port 5 = 0x2a) -- also P's 2nd refusal",
     [(LATCH_END, LATCH_END + "\t\t\tif (d->warned_port && d->port[DEV_FBCTRL_PORT_COLOR_R] == 0x2a && idata == 9)\n"
       "\t\t\t\td->current_port = (int) idata;\n")]),
    ("R_partA", "R composite part A ALONE: a command sets latch bit 1 (warned_port |= 2)",
     [(CMD_ENTRY, CMD_ENTRY + "\n\td->warned_port |= 2;\n")]),
    ("R_partB", "R composite part B ALONE: the refusal stores when warned_port == 3",
     [(LATCH_END, LATCH_END + "\t\t\tif (d->warned_port == 3)\n\t\t\t\td->current_port = (int) idata;\n")]),
    ("R_partAB", "R composite A+B: a refusal after a command, once latched, stores the value",
     [(CMD_ENTRY, CMD_ENTRY + "\n\td->warned_port |= 2;\n"),
      (LATCH_END, LATCH_END + "\t\t\tif (d->warned_port == 3)\n\t\t\t\td->current_port = (int) idata;\n")]),
    ("E_cmdset", "extra (dual of table 3's T_D4b): the latch SET on entry to fbctrl_command()",
     [(CMD_ENTRY, CMD_ENTRY + "\n\td->warned_port = 1;\n")]),
]


def main():
    fixp, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    base = io.open(fixp, encoding="utf-8", newline="").read()
    assert "\r" not in base
    for name, cls, edits in EDITS:
        s = base
        for old, new in edits:
            n = s.count(old)
            if n != 1:
                sys.exit("REFUSED %s: %d matches for %r" % (name, n, old[:60]))
            s = s.replace(old, new)
        if s == base:
            sys.exit("REFUSED %s: no change" % name)
        io.open(os.path.join(out, name + ".c"), "w", encoding="utf-8", newline="").write(s)
        print("%-12s %s" % (name, cls))
    print("EDITS_WRITTEN=%d" % len(EDITS))


if __name__ == "__main__":
    main()
