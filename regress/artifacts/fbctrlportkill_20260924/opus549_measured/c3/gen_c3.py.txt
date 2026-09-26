#!/usr/bin/env python3
"""#549 verifying pass (Opus measuring seat): floor edits of the FINAL dev_fbctrl.c (md5 129694b8) NOT among table 5's
212, each ONE text transformation with exactly one match (REFUSED otherwise).

  EQ_*  one-axis floor edits that CHANGE THE SOURCE but are behaviourally EQUIVALENT on the fix's domain -- predicted
        111/111, to show that "a floor edit scoring the total" is not by itself a breach (it must also change behaviour).
  BR_*  one-axis / joint floor edits that DO change behaviour on a reachable input -- predicted RED; a 111/111 here is a
        genuine floor breach.
  Q2_*  my eleven closing-F2 escapes, rebuilt to be scored against v5 in this clone (they are CF2_O_* in table 5).
usage: gen_c3.py <fix.c> <outdir>"""
import io
import os
import sys

PRED = "else if (idata >= DEV_FBCTRL_NPORTS) {"
LATCH = "if (!d->warned_port) {"
LATCH_END = "\t\t\t\td->warned_port = 1;\n\t\t\t}\n"
ACCEPT = "\t\t} else\n\t\t\td->current_port = idata;\n"
RD = "\t\tif (writeflag == MEM_READ)\n\t\t\todata = d->current_port;\n"
READ_PORT = "\t\t\todata = d->current_port;\n"
CMD = "d->port[DEV_FBCTRL_PORT_COMMAND]"


def pred(e):
    return [(PRED, "else if (%s) {" % e)]


def latch(e):
    return [(LATCH, "if (%s) {" % e)]


def accept(stmt):
    return [(ACCEPT, "\t\t} else\n\t\t\t%s\n" % stmt)]


def rd(cond):
    return [(RD, "\t\tif (%s)\n\t\t\todata = d->current_port;\n" % cond)]


def after_latch(stmt):
    return [(LATCH_END, LATCH_END + "\t\t\t" + stmt + "\n")]


EDITS = [
    # ---- EQUIVALENTS (predicted 111/111, NOT breaches): the bound, the accept store, direction, the latch test
    ("EQ_gt7", "bound: idata > 7", pred("idata > 7")),
    ("EQ_maskhi", "bound: (idata & ~7ULL) nonzero", pred("idata & ~7ULL")),
    ("EQ_ge8lit", "bound: idata >= 8 (literal, not the macro)", pred("idata >= 8")),
    ("EQ_acc_and7", "accept: current_port = idata & 7 (idata is 0..7 here)", accept("d->current_port = idata & 7;")),
    ("EQ_acc_castint", "accept: current_port = (int) idata", accept("d->current_port = (int) idata;")),
    ("EQ_dir_new", "direction: writeflag != MEM_WRITE", rd("writeflag != MEM_WRITE")),
    ("EQ_latch_ne1", "latch: d->warned_port != 1", latch("d->warned_port != 1")),
    ("EQ_ann_idata", "latch: !warned && idata (idata is >=8 here, never 0)", latch("!d->warned_port && idata")),
    # ---- GENUINE behaviour changers on floor axes / joints (predicted RED; a 111/111 is a breach)
    ("BR_ge9", "bound: idata >= 9 (accepts 8) -- expect P/W/V/K/F red", pred("idata >= 9")),
    ("BR_no_hi32", "bound: refuse only idata in [8, 2^32) -- accepts wide values", pred("idata >= DEV_FBCTRL_NPORTS && idata < 0x100000000ULL")),
    ("BR_acc_map0", "accept: 0 stored as 1 -- expect A red", accept("d->current_port = idata ? idata : 1;")),
    ("BR_rd_drop0", "read: odata = current_port & 6 -- expect A red", [(READ_PORT, "\t\t\todata = d->current_port & 6;\n")]),
    ("BR_acc_w8", "joint accept x width: store an out-of-range value written by sd", pred("idata >= DEV_FBCTRL_NPORTS && len != 8")),
    ("BR_ann_gt8", "joint announce x value: announce only for idata > 8 (8 silent)", latch("!d->warned_port && idata > 8")),
    ("BR_refuse_lt", "bound: refuse idata >= 7 (7 refused) -- expect A/W red", pred("idata >= DEV_FBCTRL_NPORTS - 1")),
    # ---- Q2: my eleven closing-F2 escapes, rebuilt (CF2_O_* in table 5)
    ("Q2_ref_colorb", "refusal skipped while COLOR_B != 0 (restores the exit)", pred("idata >= DEV_FBCTRL_NPORTS && !d->port[DEV_FBCTRL_PORT_COLOR_B]")),
    ("Q2_ref_y1", "refusal skipped while Y1 != 0", pred("idata >= DEV_FBCTRL_NPORTS && !d->port[DEV_FBCTRL_PORT_Y1]")),
    ("Q2_ref_colorr", "refusal skipped while COLOR_R != 0x55", pred("idata >= DEV_FBCTRL_NPORTS && d->port[DEV_FBCTRL_PORT_COLOR_R] != 0x55")),
    ("Q2_ref_cmd1", "refusal skipped while COMMAND != 1", pred("idata >= DEV_FBCTRL_NPORTS && %s != 1" % CMD)),
    ("Q2_rd_colorb", "PORT read falls into write path while COLOR_B != 0", rd("writeflag == MEM_READ && !d->port[DEV_FBCTRL_PORT_COLOR_B]")),
    ("Q2_rd_cmd1", "PORT read falls into write path while COMMAND != 1", rd("writeflag == MEM_READ && %s != 1" % CMD)),
    ("Q2_ann_bit63", "announce suppressed for a first value with bit 63 set", latch("!d->warned_port && (int64_t) idata >= 0")),
    ("Q2_ann_cmd1", "announce suppressed while COMMAND != 1", latch("!d->warned_port && %s != 1" % CMD)),
    ("Q2_cl_len2", "effect 4: a refusal by sh writes port[idata & 7]", after_latch("if (len == 2) d->port[idata & 7] = idata;")),
    ("Q2_cl_p5", "effect 4: a refusal at previous 5 writes port[idata & 7]", after_latch("if (d->current_port == 5) d->port[idata & 7] = idata;")),
    ("Q2_cl_c0", "effect 4: a refusal under COMMAND 0 writes port[idata & 7]", after_latch("if (!%s) d->port[idata & 7] = idata;" % CMD)),
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
        print("%-14s %s" % (name, cls))
    print("EDITS_WRITTEN=%d" % len(EDITS))


if __name__ == "__main__":
    main()
