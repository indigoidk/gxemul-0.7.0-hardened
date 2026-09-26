#!/usr/bin/env python3
"""#549 F2 measuring seat: write every variant of the FIXED dev_fbctrl.c as a full file.

  T_*  the D-row TARGET device edits (the edit each proposed row is meant to catch), plus two extras the seats named
       (T_X_ann6: an announce on an ACCEPTED selector outside C's set -- Astra's A-silence finding; T_X_w8: a
       width-gated accept of the boundary 8 -- grok F2 finding 7).
  M_*  table 2's 25 edits, regenerated with table2/mutants549.py.txt's own transformation list (imported, not copied).
  N_*  pass 2's 14 edits, copied from the p2 seat's /tmp/gxopus549p2_var and checked against p2/variants.diff.

Each T_ edit is one text transformation with EXACTLY one match (a find-text matching nothing is REFUSED).
usage: gen_variants_f2.py <fix.c> <HEAD dev_fbctrl.c> <table2 mutants549.py> <p2 var dir> <outdir>"""
import importlib.util
import io
import os
import sys

BS = chr(92)
NL = BS + "n"      # backslash-n inside a C string literal

PRED = "else if (idata >= DEV_FBCTRL_NPORTS) {"
REFUSE_OPEN = PRED + "\n"
LATCH_TEST = "if (!d->warned_port) {"
LATCH_BLOCK_END = "\t\t\t\td->warned_port = 1;\n\t\t\t}\n"
ACCEPT = "\t\t} else\n\t\t\td->current_port = idata;\n"
ANNOUNCE_ARG = "(unsigned long long) idata);"
READ_PORT = "\t\t\todata = d->current_port;\n"
GETRES_Y1 = "\t\t\td->port[DEV_FBCTRL_PORT_Y1] = 0;\n"
CMD_ENTRY = "\tint x1, y1, i;\n"
MEMSET = "\tmemset(d, 0, sizeof(struct fbctrl_data));\n"

ANN6 = ("\t\t} else {\n"
        "\t\t\tif (idata == 6 && !d->warned_port) {\n"
        "\t\t\t\tfatal(\"[ fbctrl: port number 0x%llx is out of range; \"\n"
        "\t\t\t\t    \"the selector is unchanged (once) ]" + NL + "\",\n"
        "\t\t\t\t    (unsigned long long) idata);\n"
        "\t\t\t\td->warned_port = 1;\n"
        "\t\t\t}\n"
        "\t\t\td->current_port = idata;\n"
        "\t\t}\n")

TARGETS = [
    ("T_D2_mask63", "D2: bit 63 masked before the compare",
     [(PRED, "else if ((idata & ~(1ULL << 63)) >= DEV_FBCTRL_NPORTS) {")]),
    ("T_D3_pwron", "D3: a refusal stores the value when the previous selector is 0 (power-on)",
     [(LATCH_BLOCK_END, LATCH_BLOCK_END + "\t\t\tif (!d->current_port)\n\t\t\t\td->current_port = (int) idata;\n")]),
    ("T_D3_ctor1", "D3 extra (grok): the constructor selects port 1 at power-on",
     [(MEMSET, MEMSET + "\td->current_port = 1;\n")]),
    ("T_D4b_cmdrearm", "D4: the latch cleared on entry to fbctrl_command()",
     [(CMD_ENTRY, CMD_ENTRY + "\n\td->warned_port = 0;\n")]),
    ("T_D6_rdbit32", "D6: the PORT read ORs bit 32",
     [(READ_PORT, "\t\t\todata = (uint64_t) d->current_port | (1ULL << 32);\n")]),
    ("T_D7a_sub4zero", "D7: selector 0 refused for sb/sh (len < 4)",
     [(PRED, "else if (idata >= DEV_FBCTRL_NPORTS || (len < 4 && idata == 0)) {")]),
    ("T_D7b_sdzero", "D7: selector 0 refused for sd (len == 8)",
     [(PRED, "else if (idata >= DEV_FBCTRL_NPORTS || (!idata && len == 8)) {")]),
    ("T_D7c_shzero", "D7 extra: selector 0 refused for sh only (len == 2)",
     [(PRED, "else if (idata >= DEV_FBCTRL_NPORTS || (!idata && len == 2)) {")]),
    ("T_D8_or1", "D8: the refusal ORs 1 into the previous selector",
     [(REFUSE_OPEN, REFUSE_OPEN + "\t\t\td->current_port |= 1;\n")]),
    ("T_D9a_only9", "D9: announce only for the value 9",
     [(LATCH_TEST, "if (!d->warned_port && idata == 9) {")]),
    ("T_D9b_mod10", "D9: the latch counts modulo 10 (re-announces on the 11th refusal)",
     [(LATCH_TEST, "if (!(d->warned_port++ % 10)) {")]),
    ("T_D9c_serial1", "D9: announce only on the machine with serial_nr 1",
     [(LATCH_TEST, "if (!d->warned_port && cpu->machine->serial_nr == 1) {")]),
    ("T_D10_print0", "D10: the diagnostic prints 0, not the refused value",
     [(ANNOUNCE_ARG, "(unsigned long long) 0);")]),
    ("T_D11a_y1one", "D11: GET_RESOLUTION (no X11) sets Y1 to 1",
     [(GETRES_Y1, "\t\t\td->port[DEV_FBCTRL_PORT_Y1] = 1;\n")]),
    ("T_D11b_y1keep", "D11 extra: GET_RESOLUTION (no X11) leaves Y1 untouched",
     [(GETRES_Y1, "")]),
    ("T_X_ann6", "extra (Astra A-silence): an ACCEPTED selector 6 announces (once)",
     [(ACCEPT, ANN6)]),
    ("T_X_w8", "extra (grok F2 #7): the boundary 8 refused only for 4-byte writes",
     [(PRED, "else if (idata > DEV_FBCTRL_NPORTS || (idata == DEV_FBCTRL_NPORTS && len == 4)) {")]),
]


def apply(base, edits, name):
    s = base
    for old, new in edits:
        n = s.count(old)
        if n != 1:
            sys.exit("REFUSED %s: %d matches for %r" % (name, n, old[:60]))
        s = s.replace(old, new)
    return s


def main():
    fixp, headp, mutp, p2dir, out = sys.argv[1:6]
    os.makedirs(out, exist_ok=True)
    base = io.open(fixp, encoding="utf-8", newline="").read()
    head = io.open(headp, encoding="utf-8", newline="").read()
    assert "\r" not in base and "\r" not in head
    wrote = []
    for name, cls, edits in TARGETS:
        io.open(os.path.join(out, name + ".c"), "w", encoding="utf-8", newline="").write(apply(base, edits, name))
        wrote.append(name)
        print("%-16s %s" % (name, cls))
    spec = importlib.util.spec_from_loader("mutants549", loader=None)
    mod = importlib.util.module_from_spec(spec)
    exec(io.open(mutp, encoding="utf-8").read().replace('if __name__ == "__main__":', "if False:"), mod.__dict__)
    for name, cls, edits in mod.MUTANTS:
        s = head if edits is None else apply(base, edits, name)
        io.open(os.path.join(out, name + ".c"), "w", encoding="utf-8", newline="").write(s)
        wrote.append(name)
        print("%-16s %s" % (name, cls))
    for fn in sorted(os.listdir(p2dir)):
        if fn.startswith("N_") and fn.endswith(".c"):
            s = io.open(os.path.join(p2dir, fn), encoding="utf-8", newline="").read()
            io.open(os.path.join(out, fn), "w", encoding="utf-8", newline="").write(s)
            wrote.append(fn[:-2])
            print("%-16s (p2 variant, copied)" % fn[:-2])
    print("VARIANTS_WRITTEN=%d" % len(wrote))


if __name__ == "__main__":
    main()
