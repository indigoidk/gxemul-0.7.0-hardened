#!/usr/bin/env python3
"""apply_fix576.py <path-to-cpu_sh_instr.c> -- the #576 shfcnvsdfpul edit in its FINAL wording (the F2 pass's P8 form).
Deletes the stray FPUL store in X(fcnvsd_fpul_drn) and leaves a comment where it stood.  The find-text must occur exactly once.
The scratch clones measured in the kill table carried the pre-P8 comment ("the FTRC store, mis-copied"); the two builds are
byte-identical in object code (HEAD and M_b, which differ only by a comment, share one md5), so the measurement stands."""
import io, sys
p = sys.argv[1]
s = io.open(p, encoding="utf-8").read()
old = "\tieee_interpret_float_value(cpu->cd.sh.fpul, &op1, IEEE_FMT_S);\n\tcpu->cd.sh.fpul = (int32_t) op1.f;\n"
new = ("\tieee_interpret_float_value(cpu->cd.sh.fpul, &op1, IEEE_FMT_S);\n"
       "\t/*  #576: FCNVSD reads FPUL and writes DRn only (sh4_programming.txt\n"
       "\t    9.29, :10866-10871).  Upstream also stored (int32_t) op1.f into\n"
       "\t    fpul here -- the same store FTRC makes, apparently copied -- so a\n"
       "\t    guest reading FPUL after an FCNVSD saw a truncated integer.\n"
       "\t    Removed; nothing else in this handler changes.  */\n")
assert s.count(old) == 1, s.count(old)
io.open(p, "w", encoding="utf-8", newline="\n").write(s.replace(old, new))
print("fix #576 applied (final wording)")
