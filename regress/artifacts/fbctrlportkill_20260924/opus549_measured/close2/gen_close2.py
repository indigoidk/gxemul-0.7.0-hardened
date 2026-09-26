#!/usr/bin/env python3
"""#549 closing F2 pass (Opus measuring seat): edits of the FINAL dev_fbctrl.c (md5 129694b8) NOT among table 4's 101,
each ONE text transformation per find-text with exactly one match (REFUSED otherwise).

  F_*  predicted 94/94: a dominating predicate qualified by ONE value (or the zero/non-zero class) of ONE field the body
       reads (port[] cells other than COMMAND; COMMAND's value 1; idata's bit-63 class), or an effect the header's
       ENUMERATION claims to hold (effect 4, "a refusal leaves every cell alone") violated on ONE axis value.
  K_*  CONTROLS on the same axes, predicted red.
  J_*  the joint cell C19's KEEP rests on (COMMAND != 0 AND latched), predicted red on R's keeps row alone.
  W_*  a weakened predicate.
usage: gen_close2.py <fix.c> <outdir>"""
import io
import os
import sys

RD = "\t\tif (writeflag == MEM_READ)\n\t\t\todata = d->current_port;\n"
PRED = "else if (idata >= DEV_FBCTRL_NPORTS) {"
LATCH = "if (!d->warned_port) {"
LATCH_END = "\t\t\t\td->warned_port = 1;\n\t\t\t}\n"
CMDC = "d->port[DEV_FBCTRL_PORT_COMMAND]"
C7 = "d->port[DEV_FBCTRL_PORT_COLOR_B]"


def rd(cond):
    return [(RD, "\t\tif (%s)\n\t\t\todata = d->current_port;\n" % cond)]


def pred(cond):
    return [(PRED, "else if (%s) {" % cond)]


def latch(cond):
    return [(LATCH, "if (%s) {" % cond)]


def clob(cond):
    return [(LATCH_END, LATCH_END + "\t\t\tif (%s)\n\t\t\t\td->port[idata & 7] = idata;\n" % cond)]


EDITS = [
    # -- one predicate x one value of one body-read field: predicted ESCAPES
    ("F_ref_c7", "refusal skipped (value STORED) while COLOR_B (port 7) is non-zero", pred("idata >= DEV_FBCTRL_NPORTS && !" + C7)),
    ("F_ref_y1", "refusal skipped while Y1 (port 2) is non-zero", pred("idata >= DEV_FBCTRL_NPORTS && !d->port[DEV_FBCTRL_PORT_Y1]")),
    ("F_ref_r55", "refusal skipped while COLOR_R (port 5) holds 0x55", pred("idata >= DEV_FBCTRL_NPORTS && d->port[DEV_FBCTRL_PORT_COLOR_R] != 0x55")),
    ("F_ref_cmd1", "refusal skipped while COMMAND holds 1 (SET_RESOLUTION)", pred("idata >= DEV_FBCTRL_NPORTS && " + CMDC + " != 1")),
    ("F_rd_c7", "a PORT read while COLOR_B is non-zero falls into the write path", rd("writeflag == MEM_READ && !" + C7)),
    ("F_rd_cmd1", "a PORT read while COMMAND holds 1 falls into the write path", rd("writeflag == MEM_READ && " + CMDC + " != 1")),
    ("F_ann_sign", "no announce (latch unset) for a refused value with bit 63 set", latch("!d->warned_port && (int64_t) idata >= 0")),
    ("F_ann_cmd1", "no announce (latch unset) while COMMAND holds 1", latch("!d->warned_port && " + CMDC + " != 1")),
    # -- effect 4 ("a refusal leaves every cell alone") violated on ONE axis value the enumeration claims to hold
    ("F_cell_sh", "effect 4 x width sh: a refusal by sh writes port[idata & 7]", clob("len == 2")),
    ("F_cell_p5", "effect 4 x previous selector 5: the refusal writes port[idata & 7]", clob("d->current_port == 5")),
    ("F_cell_cmd0", "effect 4 x COMMAND 0: the refusal writes port[idata & 7]", clob("!" + CMDC)),
    # -- CONTROLS, predicted red
    ("K_ref_x1", "control: refusal skipped while X1 (port 1) is non-zero (V's first refusal holds X1=123)",
     pred("idata >= DEV_FBCTRL_NPORTS && !d->port[DEV_FBCTRL_PORT_X1]")),
    ("K_ref_r", "control: refusal skipped while COLOR_R is non-zero (P holds 0x2a)",
     pred("idata >= DEV_FBCTRL_NPORTS && !d->port[DEV_FBCTRL_PORT_COLOR_R]")),
    ("K_cell_sb", "control: effect 4 x width sb (V refuses 0xff by sb)", clob("len == 1")),
    ("K_cell_p7", "control: effect 4 x previous selector 7 (V's five later refusals)", clob("d->current_port == 7")),
    # -- the joint cell C19 rests on
    ("J_ref_cmdlatch", "joint: refusal skipped while COMMAND != 0 AND latched (R's second refusal)",
     pred("idata >= DEV_FBCTRL_NPORTS && !(d->warned_port && " + CMDC + ")")),
    # -- a weakened predicate
    ("W_pred_ge7", "weakened bound: 7 refused too", pred("idata >= DEV_FBCTRL_NPORTS - 1")),
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
