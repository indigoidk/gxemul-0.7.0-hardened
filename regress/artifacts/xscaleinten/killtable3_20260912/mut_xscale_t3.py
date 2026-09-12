#!/usr/bin/env python3
"""xscaleinten kill table 2 mutator.  usage: mut_xscale_t2.py <SEC cpu_arm_coproc.c> <out> <LEG>

Baseline = the CURRENT SEC cpu_arm_coproc.c.  Every leg replaces ONE block that must occur exactly once
(a miss is a HARD FAIL, exit 3 -- never an unmutated leg).  The first five mutants are table 1's
(killtable_20260911/mutate_xscale.py), rebased onto the current source; the last three are the
cells the promotion added rows for:

  M_OP1        the kill reinstated only for opcode1 != 0  -- codex pass 2: escaped the 26-row witness 26/26
               because every inten access had opcode1 == 0.  Target row: D_OP1.
  M_ISTEER_WR  an inten WRITE also writes isteer            -- target row: INTEN_WRITE_PRESERVES_ISTEER
  M_CRM        crm=1/crn=0 (tmr0) reads inten instead       -- codex: "D_TRR0 does not isolate crm".
               Target row: D_CRM1_TMR0.
"""
import io, sys

T = "\t"
FIX = (T*2 + "case 0:" + T + "if (l_bit) {\n" + T*4 + "cpu->cd.arm.r[rd] = cpu->cd.arm.i80321_inten;\n"
       + T*3 + "} else\n" + T*4 + "cpu->cd.arm.i80321_inten = cpu->cd.arm.r[rd];\n" + T*3 + "break;")
TMR0 = T*2 + "case 0:" + T + "/*  tmr0:  */\n" + T*3 + "if (l_bit)\n" + T*4 + "cpu->cd.arm.r[rd] = cpu->cd.arm.tmr0;\n"

def blk(read_extra_pre="", read_line="cpu->cd.arm.r[rd] = cpu->cd.arm.i80321_inten;", read_extra_post="",
        head="", write_line="cpu->cd.arm.i80321_inten = cpu->cd.arm.r[rd];"):
    return (T*2 + "case 0:" + T + head + "if (l_bit) {\n" + read_extra_pre + T*4 + read_line + "\n" + read_extra_post
            + T*3 + "} else\n" + T*4 + write_line + "\n" + T*3 + "break;")

LEGS = {
 "M1": (FIX, blk(read_extra_post=T*4 + "if (cpu->cd.arm.i80321_isrc != 0) {\n" + T*5
                 + "fatal(\"TODO: XScale read from inten with isrc!=0\\n\");\n" + T*5 + "exit(1);\n" + T*4 + "}\n")),
 "M5": (FIX, blk(read_line="cpu->cd.arm.r[rd] = cpu->cd.arm.i80321_isteer;",
                 write_line="cpu->cd.arm.i80321_isteer = cpu->cd.arm.r[rd];")),
 "M_OPCODE2": (FIX, blk(head="if (opcode2 != 0) {\n" + T*4 + "fatal(\"TODO: XScale inten bad opcode2\\n\");\n"
                        + T*4 + "exit(1);\n" + T*3 + "}\n" + T*3)),
 "M_RD15": (FIX, blk(read_extra_pre=T*4 + "if (rd == 15) {\n" + T*5 + "fatal(\"TODO: XScale inten to r15 refused\\n\");\n"
                     + T*5 + "exit(1);\n" + T*4 + "}\n")),
 "M_NREAD": (FIX, blk(read_extra_pre=T*4 + "static int nread = 0;\n" + T*4 + "if (++nread > 4) {\n" + T*5
                      + "fatal(\"TODO: XScale inten nread > 4\\n\");\n" + T*5 + "exit(1);\n" + T*4 + "}\n")),
 "M_OP1": (FIX, blk(read_extra_post=T*4 + "if (opcode1 != 0) {\n" + T*5 + "fatal(\"TODO: XScale read from inten?\\n\");\n"
                    + T*5 + "exit(1);\n" + T*4 + "}\n")),
 "M_ISTEER_WR": (FIX, blk(write_line="{ cpu->cd.arm.i80321_inten = cpu->cd.arm.r[rd]; "
                          "cpu->cd.arm.i80321_isteer = cpu->cd.arm.r[rd]; }")),
 #  TABLE 3 (pass 2, 2026-09-12): the two exits the 29-row instrument could not see.  M_MAGICBIT uses
 #  bit 22, the Opus seat's choice (opus_pass2_20260912/mutant_XM_MAGICBIT.txt).  Target row RD0_ALLONES.
 "M_RD0": (FIX, blk(read_extra_post=T*4 + "if (rd == 0) {\n" + T*5 + "fatal(\"TODO: XScale read from inten?\\n\");\n"
                    + T*5 + "exit(1);\n" + T*4 + "}\n")),
 "M_MAGICBIT": (FIX, blk(read_extra_post=T*4 + "if (cpu->cd.arm.i80321_inten & 0x00400000) {\n" + T*5
                         + "fatal(\"TODO: XScale read from inten?\\n\");\n" + T*5 + "exit(1);\n" + T*4 + "}\n")),
 "M_CRM": (TMR0, TMR0.replace("cpu->cd.arm.r[rd] = cpu->cd.arm.tmr0;", "cpu->cd.arm.r[rd] = cpu->cd.arm.i80321_inten;")),
}

src, dst, leg = sys.argv[1:4]
t = io.open(src, encoding="utf-8").read()
if leg != "BASE":
    if leg not in LEGS:
        sys.exit("unknown leg %s" % leg)
    old, new = LEGS[leg]
    n = t.count(old)
    if n != 1 or old == new:
        sys.stderr.write("FIND-TEXT for %s occurs %d times (or no-op) -- REFUSING\n" % (leg, n))
        sys.exit(3)
    t = t.replace(old, new)
io.open(dst, "w", encoding="utf-8", newline="\n").write(t)
print("MUTATED %s" % leg)
