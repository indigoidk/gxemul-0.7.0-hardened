#!/usr/bin/env python3
"""#549 verifying pass (Opus, re-issue): the floor shape the first answer's denominator omitted -- the compare
`idata >= DEV_FBCTRL_NPORTS` NARROWED to ignore one bit range.  A refused value whose only bits >= 3 lie in the ignored
range is then ACCEPTED (stored as an out-of-range int).  Predicted by arithmetic: no v5 refusal has its bits >= 3 confined
to 5-7, 9-31 or 34-62, so those three score the total; bit 8 alone IS refused by v5 (0x100), so its narrowing is a
CONTROL, predicted red.  usage: gen_mask.py <fix.c> <outdir>"""
import io
import os
import sys

PRED = "else if (idata >= DEV_FBCTRL_NPORTS) {"
EDITS = [
    ("MK_b9_31", "ignore bits 9-31", "(idata & ~0xfffffe00ULL) >= DEV_FBCTRL_NPORTS"),
    ("MK_b5_7", "ignore bits 5-7", "(idata & ~0xe0ULL) >= DEV_FBCTRL_NPORTS"),
    ("MK_b34_62", "ignore bits 34-62", "(idata & ~0x7ffffffc00000000ULL) >= DEV_FBCTRL_NPORTS"),
    ("MK_b8_ctl", "CONTROL: ignore bit 8 alone (v5 refuses 0x100)", "(idata & ~0x100ULL) >= DEV_FBCTRL_NPORTS"),
]


def main():
    fixp, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    base = io.open(fixp, encoding="utf-8", newline="").read()
    assert base.count(PRED) == 1
    for name, cls, expr in EDITS:
        io.open(os.path.join(out, name + ".c"), "w", encoding="utf-8", newline="").write(
            base.replace(PRED, "else if (%s) {" % expr))
        print("%-10s %s" % (name, cls))


if __name__ == "__main__":
    main()
