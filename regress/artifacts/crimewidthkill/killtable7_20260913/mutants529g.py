#!/usr/bin/env python3
"""mutants529g.py NAME SRC DST -- #529 kill table 7: the THIRD closing pass's undetected changes (repair 8).

Imports table 6's mutator (every earlier mutant by name) and adds this pass's.  The Opus third-closing seat's mutator is
exec'd verbatim when present (prefix `r_').  Every find-text must occur EXACTLY ONCE -- a presence pin.
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
for t in ("killtable6_20260913", "killtable5_20260913", "killtable4_20260913", "killtable3_20260913",
          "killtable2_20260913"):
    sys.path.insert(0, os.path.join(HERE, "..", t))
import mutants529f as F                                    # noqa: E402

E = F.E
GOTO, g = E.GOTO, E.g
B = E.D.C.B
DEFINE = E.DEFINE
DOGBR, REVIF = E.DOGBR, E.REVIF
ISTAT = "\tcase CRIME_INTSTAT:\t/*  0x010, Current interrupt status  */\n"
TXTEND = "\t\t\t\t    \"control 0x%016llx ]\\n\", (long long)idata);\n"

M = dict(F.M)
_p = os.path.join(HERE, "mutants_close3_opus.py")
if os.path.exists(_p):
    _ns = {}
    _src = io.open(_p, encoding="utf-8").read()
    _cut = "if __name__" if "if __name__" in _src else "name, path = sys.argv"   # the seat's CLI, not its mutants
    exec(_src.split(_cut)[0], _ns)
    M.update({"r_" + k: v for k, v in _ns["M"].items() if k != "base"})
M.update({
    # codex: the latch bit keyed on address bit 7 / bit 8
    "c3_lat_b7":   [(DEFINE, "#define\tCRIME_W_LEN\t\t(1 << !!(relative_addr & 0x80))")],
    "c3_lat_b8":   [(DEFINE, "#define\tCRIME_W_LEN\t\t(1 << !!(relative_addr & 0x100))")],
    # codex: the notice suppressed when address bit 1 is clear; mine: suppressed at one label
    "c3_quiet_b1":    [(B.LATCH_TEST, "\t\tif (!(d->warned & CRIME_W_LEN) && (relative_addr & 2)) {")],
    "c3_quiet_imask": [(B.LATCH_TEST, "\t\tif (!(d->warned & CRIME_W_LEN) && relative_addr != CRIME_INTMASK) {")],
    # codex, grok, kimi: a pre-set inside a branch reached only after a session's first refusal
    "c3_pre_dog":   [(DOGBR, DOGBR + "\t\t\t\td->warned |= CRIME_W_LEN;\n")],
    "c3_pre_revbr": [(REVIF, REVIF + "\t\t\td->warned |= CRIME_W_LEN;\n")],
    "c3_pre_istat": [(ISTAT, ISTAT + "\t\td->warned |= CRIME_W_LEN;\n")],
    # codex: a far-block store that CLEARS
    "c3_far_and":  [(GOTO, g("if (writeflag == MEM_WRITE && (relative_addr & 0x200)) d->reg[relative_addr / 8] &= idata; "
                             "goto crime_declined;"))],
    # glm: the 4-byte path's half as the answer
    "c3_half_istat": [(GOTO, g("if (writeflag == MEM_READ && relative_addr == CRIME_INTSTAT) "
                               "odata = d->reg[relative_addr / 8] >> 32; goto crime_declined;"))],
    "c3_half_imask": [(GOTO, g("if (writeflag == MEM_READ && relative_addr == CRIME_INTMASK) "
                               "odata = d->reg[relative_addr / 8] >> 32; goto crime_declined;"))],
    # the Opus third-closing seat named these by reading and did not build them: a pre-set on the zero-leftover side,
    # and on the DOG-clear side (the second one reopened by repair 8's prologue swap of 0x01 for 0x0201)
    # (the else goes after the WHOLE fatal() statement -- table 7's first launch inserted it after the call's first
    #  line, which did not compile; the build failure is recorded in POSTTABLE 7)
    "c3_pre_ctl0":   [(TXTEND, TXTEND + "\t\t\telse\n\t\t\t\td->warned |= CRIME_W_LEN;\n")],
    "c3_pre_dogclr": [(DOGBR, DOGBR.replace("\t\t\tif (idata & CRIME_CONTROL_DOG_ENABLE) {\n",
                                            "\t\t\tif (!(idata & CRIME_CONTROL_DOG_ENABLE))\n\t\t\t\td->warned |= CRIME_W_LEN;\n"
                                            "\t\t\tif (idata & CRIME_CONTROL_DOG_ENABLE) {\n"))],
    # deepseek: a landing at CRIME_SOFTINT -- PREDICTED SURVIVOR (the one-unnamed-offset class, disclosed)
    "c3_soft_land": [(GOTO, g("if (writeflag == MEM_WRITE && relative_addr == CRIME_SOFTINT) "
                              "d->reg[CRIME_SOFTINT / 8] |= idata; goto crime_declined;"))],
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
