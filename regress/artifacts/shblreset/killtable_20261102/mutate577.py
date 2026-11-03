#!/usr/bin/env python3
"""mutate577.py <mutant> <path-to-cpu_sh.c> -- one #577 kill-table mutant applied to the FIXED block (scratch clone only).
Find-texts must occur exactly once (a presence pin).  The fixed block is:
    if (expevt != EXPEVT_RESET_TLB_MULTI_HIT)
        expevt = EXPEVT_RESET_MANUAL;
"""
import io, sys
m, p = sys.argv[1], sys.argv[2]
s = io.open(p, encoding="utf-8").read()
FIX = "\t\tif (expevt != EXPEVT_RESET_TLB_MULTI_HIT)\n\t\t\texpevt = EXPEVT_RESET_MANUAL;\n"
assert s.count(FIX) == 1, s.count(FIX)
if m == "M_b":        # (b) the removed behaviour verbatim: every code -> power-on
    s = s.replace(FIX, "\t\texpevt = EXPEVT_RESET_POWER;\n")
elif m == "M_c":      # (c) identity for a predicate round: no rewrite at all
    s = s.replace(FIX, "\t\t;\n")
elif m == "M_noex":   # (d) exemption removed: the multiple hit is rewritten too
    s = s.replace(FIX, "\t\texpevt = EXPEVT_RESET_MANUAL;\n")
elif m == "M_wrongex":  # (d) the exemption on the wrong code
    s = s.replace(FIX, "\t\tif (expevt != EXPEVT_TRAPA)\n\t\t\texpevt = EXPEVT_RESET_MANUAL;\n")
elif m == "M_lt100":  # (d) exemption widened to every code below 0x100 (a failing form: 0x140 is not below 0x100)
    s = s.replace(FIX, "\t\tif (expevt >= 0x100)\n\t\t\texpevt = EXPEVT_RESET_MANUAL;\n")
elif m == "M_trapaonly":  # (e) the rewrite keyed to the one general code a narrow table would drive
    s = s.replace(FIX, "\t\tif (expevt == EXPEVT_TRAPA)\n\t\t\texpevt = EXPEVT_RESET_MANUAL;\n")
elif m == "M_power":  # (d) exemption kept, constant wrong
    s = s.replace(FIX, "\t\tif (expevt != EXPEVT_RESET_TLB_MULTI_HIT)\n\t\t\texpevt = EXPEVT_RESET_POWER;\n")
elif m == "M_guard":  # (d) the GUARD weakened: fires on MD as well as BL (Fable pass 2, change 1); cpu_sh.c:910 at HEAD
    G = "\tif (cpu->cd.sh.sr & SH_SR_BL) {\n"
    assert s.count(G) == 1, s.count(G)
    s = s.replace(G, "\tif (cpu->cd.sh.sr & (SH_SR_BL | SH_SR_MD)) {\n")
elif m == "M_resinst":  # (e) an exemption ADDED at a code the table does not drive (pass 2: Fable ADDR_ERR_ST, Grok RES_INST, Argon TLB_MISS)
    s = s.replace(FIX, "\t\tif (expevt != EXPEVT_RESET_TLB_MULTI_HIT && expevt != EXPEVT_RES_INST)\n\t\t\texpevt = EXPEVT_RESET_MANUAL;\n")
else:
    sys.exit("unknown mutant " + m)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("applied", m)
