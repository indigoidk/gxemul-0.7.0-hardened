#!/usr/bin/env python3
"""apply_fix577.py <path-to-cpu_sh.c> -- the #577 shblreset edit: a general exception taken with SR.BL set is a MANUAL reset
(EXPEVT H'020), and the two TLB multiple-hit codes (H'140) keep their own code.  The find-text must occur exactly once."""
import io, sys
p = sys.argv[1]
s = io.open(p, encoding="utf-8").read()
old = ("\tif (cpu->cd.sh.sr & SH_SR_BL) {\n"
       "\t\tfatal(\"[ sh_exception(): BL bit already set. ]\\n\");\n"
       "\n"
       "\t\t/*  This is actually OK in two cases: a User Break,\n"
       "\t\t    or on NMI interrupts if a special flag is set?  */\n"
       "\t\t/*  TODO  */\n"
       "\n"
       "\t\texpevt = EXPEVT_RESET_POWER;\n"
       "\t}\n")
new = ("\tif (cpu->cd.sh.sr & SH_SR_BL) {\n"
       "\t\tfatal(\"[ sh_exception(): BL bit already set. ]\\n\");\n"
       "\n"
       "\t\t/*  #577: a general exception taken with BL set is a MANUAL\n"
       "\t\t    reset -- sh7750_hardware.txt 5.5.3 (:12302-12304), EXPEVT\n"
       "\t\t    H'020 (:678-681) -- not a power-on reset (H'000), which is\n"
       "\t\t    what stood here.  The two TLB multiple-hit exceptions are\n"
       "\t\t    reset-category in their own right (Table 5.2, :12006 and\n"
       "\t\t    :12010; code H'140, :12461) and keep their code.  A user\n"
       "\t\t    break would be the other exemption; EXPEVT_BREAK is never\n"
       "\t\t    raised in this tree.  Interrupts do not reach this path:\n"
       "\t\t    cpu_dyntrans.c gates their delivery on BL.  */\n"
       "\t\tif (expevt != EXPEVT_RESET_TLB_MULTI_HIT)\n"
       "\t\t\texpevt = EXPEVT_RESET_MANUAL;\n"
       "\t}\n")
assert s.count(old) == 1, s.count(old)
io.open(p, "w", encoding="utf-8", newline="\n").write(s.replace(old, new))
print("fix #577 applied")
