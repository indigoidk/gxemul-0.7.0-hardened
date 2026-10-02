#!/usr/bin/env python3
"""mutants529e.py NAME SRC DST -- #529 kill table 5: the SECOND closing pass's undetected changes of the 111-row test.

Imports table 4's mutator (so every earlier mutant stays available by name, including the Opus closing seat's `o_*')
and adds this pass's.  The Opus second-closing seat's own mutator is exec'd verbatim when present (prefix `p_').
Every find-text must occur EXACTLY ONCE -- a presence pin.
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "killtable4_20260913"))
sys.path.insert(0, os.path.join(HERE, "..", "killtable3_20260913"))
sys.path.insert(0, os.path.join(HERE, "..", "killtable2_20260913"))
import mutants529d as D                                    # noqa: E402

GOTO, g = D.GOTO, D.g
B = D.C.B
DEFINE = "#define\tCRIME_W_LEN\t\t(1 << 0)"
REVIF = "\t\tif (((uint32_t)cpu->pc & 0xffffff00) == (uint32_t)0xbfc05100) {\n"
DOGBR = "\t\t\tif (idata & CRIME_CONTROL_DOG_ENABLE) {\n\t\t\t\tidata &= ~CRIME_CONTROL_DOG_ENABLE;\n"
TXTBR = "\t\t\tif (idata != 0)\n\t\t\t\tfatal(\"[ CRIME_CONTROL: unimplemented \"\n"
IRQARM = "\tcase CRIME_INTMASK:\t/*  0x018, Current interrupt mask  */\n\t\tcrime_interrupt_reassert(d);\n"
ARM8 = D.C.ARM8_BODY

M = dict(D.M)
_p = os.path.join(HERE, "mutants_close2_opus.py")
if os.path.exists(_p):
    _ns = {}
    exec(io.open(_p, encoding="utf-8").read().split("name, path = sys.argv")[0], _ns)
    M.update({"p_" + k: v for k, v in _ns["M"].items() if k != "base"})
M.update({
    # codex: the latch bit keyed on ONE label (the define is used by both the test and the set)
    "c2_lbl_imask": [(DEFINE, "#define\tCRIME_W_LEN\t\t(1 << (relative_addr == CRIME_INTMASK))")],
    "c2_lbl_istat": [(DEFINE, "#define\tCRIME_W_LEN\t\t(1 << (relative_addr == CRIME_INTSTAT))")],
    "c2_lbl_ctl":   [(DEFINE, "#define\tCRIME_W_LEN\t\t(1 << (relative_addr == CRIME_CONTROL))")],
    # codex: a halfword-only nonzero answer at DOG; kimi CLI: a decline answering THE REGISTER at a label
    "c2_dog100":    [(GOTO, g("if (relative_addr == CRIME_DOG) odata = 0x100; goto crime_declined;"))],
    "c2_reg_imask": [(GOTO, g("if (relative_addr == CRIME_INTMASK) odata = d->reg[relative_addr / 8]; goto crime_declined;"))],
    "c2_reg_istat": [(GOTO, g("if (relative_addr == CRIME_INTSTAT) odata = d->reg[relative_addr / 8]; goto crime_declined;"))],
    "c2_reg_dog":   [(GOTO, g("if (relative_addr == CRIME_DOG) odata = d->reg[relative_addr / 8]; goto crime_declined;"))],
    # kimi CLI: a landing that ORs into INTMASK
    "c2_land_or":   [(GOTO, g("if (writeflag == MEM_WRITE && relative_addr == CRIME_INTMASK) "
                              "d->reg[CRIME_INTMASK / 8] |= idata; goto crime_declined;"))],
    # codex: re-arm inside CONTROL's DOG_ENABLE branch; and the same inside the other branches an accepted access takes
    "c2_rearm_dog": [(DOGBR, DOGBR + "\t\t\t\td->warned = 0;\n")],
    "c2_rearm_txt": [(TXTBR, "\t\t\tif (idata != 0 && ((d->warned = 0) == 0))\n\t\t\t\tfatal(\"[ CRIME_CONTROL: unimplemented \"\n")],
    "c2_rearm_rev": [(REVIF, REVIF + "\t\t\td->warned = 0;\n")],
    # glm: a pre-set in a switch arm -- the INTMASK/INTSTAT arm (PREDICTED DETECTED) and the REV arm (the open member)
    "c2_pre_irq":   [(IRQARM, IRQARM.replace("\t\tcrime_interrupt_reassert(d);\n",
                                             "\t\td->warned |= CRIME_W_LEN;\n\t\tcrime_interrupt_reassert(d);\n"))],
    "c2_pre_rev":   [(REVIF, "\t\td->warned |= CRIME_W_LEN;\n" + REVIF)],
    # kimi-k3:cloud: decline effects keyed on an ADDRESS BIT no refusal carried (bit 7, bit 8)
    "c2_bit7_ans":  [(GOTO, g("odata = relative_addr & 0x80; goto crime_declined;"))],
    "c2_bit8_land": [(GOTO, g("if (writeflag == MEM_WRITE && (relative_addr & 0x100)) d->reg[relative_addr / 8] = idata; "
                              "goto crime_declined;"))],
    "c2_bit7_quiet": [(B.LATCH_TEST, "\t\tif (!(d->warned & CRIME_W_LEN) && !(relative_addr & 0x80)) {")],
    "c2_bit8_ft":   [(GOTO, g("if (!(relative_addr & 0x100)) goto crime_declined;"))],
    "c2_bit8_rearm": [(ARM8, ARM8.replace("\tif (len == 8) {\n", "\tif (len == 8) {\n\t\tif (relative_addr & 0x100) d->warned = 0;\n", 1))],
    "c2_bit8_latch": [(B.LATCH_SET, "\t\t\td->warned |= (relative_addr & 0x100) ? 0 : CRIME_W_LEN;\n")],
})

if __name__ == "__main__":
    if sys.argv[1:2] == ["list"]:
        print(" ".join(M))
        sys.exit(0)
    name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    s = io.open(src, newline="").read()
    for find, repl in M[name]:
        n = s.count(find)
        if n != 1:
            sys.stderr.write("MUTANT %s: find-text occurs %d times (want 1)\n" % (name, n))
            sys.exit(2)
        s = s.replace(find, repl, 1)
    io.open(dst, "w", newline="").write(s)
    print("APPLIED %s (%d edit(s))" % (name, len(M[name])))
