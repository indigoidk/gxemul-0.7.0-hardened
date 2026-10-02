#!/usr/bin/env python3
"""mutants529c.py NAME SRC DST -- #529 kill table 3: the F2 pass's survivors of the 71-row detector.

Imports table 2's mutator (every table-1 and table-2 mutant is still available by name) and adds the F2 findings.
Every find-text must occur EXACTLY ONCE (a presence pin); `list' prints the names.
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "killtable2_20260913"))
import mutants529b as B                                    # noqa: E402

GOTO, g, ARM8, ARM4 = B.GOTO, B.g, B.ARM8, B.ARM4
ARM8_BODY = ("\tif (len == 8) {\n\t\tif (writeflag == MEM_WRITE)\n\t\t\td->reg[relative_addr / 8] = idata;\n"
             "\t\telse\n\t\t\todata = d->reg[relative_addr / 8];\n")
ARM4_W = ("\t\t\tif (relative_addr & 4) {\n\t\t\t\td->reg[relative_addr / 8] &= ~0xffffffffULL;\n"
          "\t\t\t\td->reg[relative_addr / 8] |= (uint32_t)idata;\n\t\t\t} else {\n"
          "\t\t\t\td->reg[relative_addr / 8] &= 0xffffffffULL;\n"
          "\t\t\t\td->reg[relative_addr / 8] |= (uint64_t)(idata << 32ULL);\n\t\t\t}\n")
ARM4_R = "\t\t\todata = d->reg[relative_addr / 8];\n\t\t\tif (relative_addr & 4)\n"
REMAP = "(relative_addr & 0x3f) / 8]"

M = dict(B.M)
M.update({
    # grok, glm: the 2-byte cells at the three reassert/update labels
    "istat2":  [(GOTO, g("if (len != 2 || relative_addr != CRIME_INTSTAT) goto crime_declined;"))],
    "imask2":  [(GOTO, g("if (len != 2 || relative_addr != CRIME_INTMASK) goto crime_declined;"))],
    "time2":   [(GOTO, g("if (len != 2 || relative_addr != CRIME_TIME) goto crime_declined;"))],
    "istatsh": [(GOTO, g("if (!(len == 2 && writeflag == MEM_WRITE && relative_addr == CRIME_INTSTAT)) goto crime_declined;"))],
    # kimi-k3:cloud: the accept arms re-map their register index (a round-trip-invisible re-map)
    "remap":   [(ARM8_BODY, ARM8_BODY.replace("relative_addr / 8]", REMAP)),
                (ARM4_W, ARM4_W.replace("relative_addr / 8]", REMAP)),
                (ARM4_R, ARM4_R.replace("relative_addr / 8]", REMAP))],
    # codex (F2 retry): state carried across calls -- a static odata, and a latch re-armed by an accepted access
    "static_od": [("\tuint64_t idata = 0, odata = 0;\n\tuint64_t preserved_CRIME_HARDINT",
                   "\tstatic uint64_t idata = 0, odata = 0;\n\tuint64_t preserved_CRIME_HARDINT")],
    "rearm":     [(ARM8, ARM8.replace("\tif (len == 8) {\n", "\tif (len == 8) {\n\t\td->warned = 0;\n", 1))],
    # the Opus F2 seat's measured 71/71 survivors (opus_f2_20260913/scripts/mutants_f2.py), verbatim
    "h_imask":  [(GOTO, g("if (len == 1 || relative_addr != CRIME_INTMASK) goto crime_declined;"))],
    "h_lbl":    [(GOTO, g("if (len == 1 || (relative_addr != CRIME_INTSTAT && relative_addr != CRIME_INTMASK"
                          " && relative_addr != CRIME_TIME)) goto crime_declined;"))],
    "lt_len":   [(B.LATCH_SET, "\t\t\td->warned |= len;\n")],
    "lt_addr":  [(B.LATCH_SET, "\t\t\td->warned |= relative_addr;\n")],
    "lt_wset":  [(B.LATCH_SET, "\t\t\td->warned |= CRIME_W_LEN << writeflag;\n")],
    "wst_mc":   [(GOTO, g("if (writeflag == MEM_WRITE && relative_addr >= 0x200) d->reg[relative_addr / 8] = idata;"
                          " goto crime_declined;"))],
    # the Opus F2 seat's generating-set breach at CONTROL, and its mirror (fall through only when RESET is clear)
    "c_dog":    [(GOTO, g("if (relative_addr != CRIME_CONTROL || !(idata & CRIME_CONTROL_DOG_ENABLE)) goto crime_declined;"))],
    "c_hrclr":  [(GOTO, g("if (relative_addr != CRIME_CONTROL || (idata & CRIME_CONTROL_HARD_RESET)) goto crime_declined;"))],
    # PREDICTED SURVIVOR, disclosed: a fall-through only at SOFTINT, an offset the switch does not name
    "sft":      [(GOTO, g("if (relative_addr != CRIME_SOFTINT) goto crime_declined;"))],
    # kimi CLI: one refused store lands, at an offset no row names -- PREDICTED SURVIVOR (clause (e), disclosed)
    "wstore31": [(GOTO, g("if (writeflag == MEM_WRITE && relative_addr == 0x31) d->reg[relative_addr / 8] = idata; "
                          "goto crime_declined;"))],
})

if __name__ == "__main__":
    name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    if name == "list":
        print(" ".join(M))
        sys.exit(0)
    s = io.open(src, newline="").read()
    for find, repl in M[name]:
        n = s.count(find)
        if n != 1:
            sys.stderr.write("MUTANT %s: find-text occurs %d times (want 1)\n" % (name, n))
            sys.exit(2)
        s = s.replace(find, repl, 1)
    io.open(dst, "w", newline="").write(s)
    print("APPLIED %s (%d edit(s))" % (name, len(M[name])))
