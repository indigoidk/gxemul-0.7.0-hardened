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
       "\t\t    reset: sh7750_hardware.txt 5.5.3 (:12302-12304) and 5.6.1\n"
       "\t\t    (2) Manual Reset, :12376 and :12383-12384 -- \"Exception code\n"
       "\t\t    H'020 is set in EXPEVT\" -- not a power-on reset (H'000),\n"
       "\t\t    which is what stood here.  The two TLB multiple-hit\n"
       "\t\t    exceptions are reset-category in their own right (Table\n"
       "\t\t    5.2, :12006 and :12010; code H'140, :12461) and keep their\n"
       "\t\t    code.  A user break under BL is suppressed at the UBC\n"
       "\t\t    (:41448-41452) and never reaches here; EXPEVT_BREAK has no\n"
       "\t\t    raiser in this tree.  An interrupt cannot latch a code here\n"
       "\t\t    either: cpu_dyntrans.c delivers none while BL is set, and\n"
       "\t\t    the intevt path below discards expevt before storing it.  */\n"
       "\t\tif (expevt != EXPEVT_RESET_TLB_MULTI_HIT)\n"
       "\t\t\texpevt = EXPEVT_RESET_MANUAL;\n"
       "\t}\n")
assert s.count(old) == 1, s.count(old)
io.open(p, "w", encoding="utf-8", newline="\n").write(s.replace(old, new))
print("fix #577 applied")
