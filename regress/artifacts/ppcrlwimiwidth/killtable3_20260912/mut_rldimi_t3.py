#!/usr/bin/env python3
"""ppcrldimimask table-3 mutator for the two pass-2 legs.  usage: mut_rldimi_t3.py <SEC cpu_ppc_instr.c> <out> <LEG>

  D_SKIP_FULL_ROT  the rotate is skipped exactly when the mask is full width (codex, pass 2):
                   `while (n-- != 0)' -> `while (n-- != 0 && mb != ((64 - sh) & 63))'
  D_ALIAS_REREAD   the merge re-reads rS AFTER rA was cleared and rotates that, instead of using the
                   snapshot `s' (glm, pass 2 -- its "equivalently" form).  glm's literal one-line form,
                   `gpr[ra] |= (tmp & cpu->cd.ppc.gpr[rs])', reads the UNROTATED source, so it is wrong
                   for every SH != 0 whatever the aliasing and is not the aliasing mutant (simulated
                   2026-09-12, _scratchpad sim_rldimi_t3.py).  This form differs from the fix ONLY when rA == rS.

Each find-text must occur EXACTLY ONCE or the leg is refused, so a find-text doubles as a presence pin.
"""
import io, sys

LEGS = {
    "D_SKIP_FULL_ROT": ("\twhile (n-- != 0) {\n",
                        "\twhile (n-- != 0 && mb != ((64 - sh) & 63)) {\n"),
    "D_ALIAS_REREAD": ("\tcpu->cd.ppc.gpr[ra] |= (tmp & s);\n",
                       "\t{ uint64_t s2 = cpu->cd.ppc.gpr[rs]; int k = sh;\n"
                       "\t  while (k-- != 0) s2 = (s2 << 1) | (s2 >> 63);\n"
                       "\t  cpu->cd.ppc.gpr[ra] |= (tmp & s2); }\n"),
}

src, dst, leg = sys.argv[1:4]
t = io.open(src, encoding="utf-8").read()
if leg not in LEGS:
    sys.exit("unknown leg %s -- REFUSING" % leg)
old, new = LEGS[leg]
if t.count(old) != 1:
    sys.stderr.write("find-text for %s occurs %d times -- REFUSING\n" % (leg, t.count(old)))
    sys.exit(3)
io.open(dst, "w", encoding="utf-8", newline="\n").write(t.replace(old, new))
print("MUTATED %s" % leg)
