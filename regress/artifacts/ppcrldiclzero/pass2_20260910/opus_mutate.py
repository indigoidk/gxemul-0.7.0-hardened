#!/usr/bin/env python3
#  Opus pass-2 seat, #522 ppcrldiclzero.  INDEPENDENT mutator (not the round's).
#  Literal find/replace; MUTANT-TEXT-NOT-FOUND = exit 9, so every leg doubles as a
#  presence pin.  Operates ONLY on the path given, which is always the /tmp clone.
import io, sys

P, m = sys.argv[1], sys.argv[2]
T = '\t'

FIXED = T*2 + "tmp2 |= ((uint64_t)1 << (63-mb));\n"

#  two-line anchor: the bare `int sh = ...' line appears TWICE (rldicl and rldicr),
#  so the following `int mb =' line is what makes it unique to X(rldicl).
SHMB_OLD = (T + "int sh = ((ic->arg[0] >> 11) & 31) | ((ic->arg[0] & 2) << 4);\n"
            + T + "int mb = ((ic->arg[0] >> 6) & 31) | (ic->arg[0] & 0x20);\n")
SH5_NEW  = (T + "int sh = ((ic->arg[0] >> 11) & 31);\n"
            + T + "int mb = ((ic->arg[0] >> 6) & 31) | (ic->arg[0] & 0x20);\n")
MB5_NEW  = (T + "int sh = ((ic->arg[0] >> 11) & 31) | ((ic->arg[0] & 2) << 4);\n"
            + T + "int mb = ((ic->arg[0] >> 6) & 31);\n")

ROT_OLD = (T + "while (sh-- != 0) {\n" + T*2 + "int b = (tmp >> 63) & 1;\n"
           + T*2 + "tmp = (tmp << 1) | b;\n" + T + "}\n" + T + "tmp2 = 0;\n")
ROT_NEW = (T + "while (sh-- > 1) {\n" + T*2 + "int b = (tmp >> 63) & 1;\n"
           + T*2 + "tmp = (tmp << 1) | b;\n" + T + "}\n" + T + "tmp2 = 0;\n")

CR0_OLD = (T + "cpu->cd.ppc.gpr[ra] = tmp & tmp2;\n" + T + "if (rc)\n"
           + T*2 + "update_cr0(cpu, cpu->cd.ppc.gpr[ra]);\n")
CR0_NEW = (T + "cpu->cd.ppc.gpr[ra] = tmp & tmp2;\n" + T + "if (rc)\n"
           + T*2 + "update_cr0(cpu, tmp);\n")

M = {
    'BASE': None,
    #  HARNESS CONTROL: reproduce the round's own M_ORIG number (expect 14/19).
    #  If my clone/build/probe pipeline disagrees with the round's table here, no
    #  other number below is worth anything.
    'M_ORIG':   (FIXED, T*2 + "tmp |= ((uint64_t)1 << (63-mb));\n"),
    #  CANDIDATE ESCAPE 1 -- drop the sh5 bit.  Every SH >= 32 then rotates by SH-32.
    #  `srdi rX,rY,n' IS `rldicl rX,rY,64-n,n', so this breaks every logical right
    #  shift by 1..32.  Predicted 19/19: the census is rotate-AMOUNT-blind (rS is
    #  all-ones, and ROTL64(all-ones,n) is all-ones for every n) and the only
    #  rotate-sensitive rldicl rows use SH=0 and SH=8, both below 32.
    'M_SH5':    (SHMB_OLD, SH5_NEW),
    #  POSITIVE CONTROL on the SAME decode line -- drop the mb5 bit instead.  MB=32
    #  is rowed by `zx32 rldicl', so this MUST die.  It proves the two-line anchor
    #  lands inside X(rldicl) and that a decode-field mutant is reachable at all.
    'M_MB5':    (SHMB_OLD, MB5_NEW),
    #  rotate by ONE TOO FEW.  Isolates the rotate AMOUNT axis: predicted to redden
    #  `rot8 rldicl' ALONE (18/19), showing that axis rests on one row at one value.
    'M_ROTAMT': (ROT_OLD, ROT_NEW),
    #  CANDIDATE ESCAPE 2 -- feed CR0 the UNMASKED rotated value.  That is exactly
    #  the shape the CORRECT sibling X(rldicr) uses ten lines below
    #  (`update_cr0(cpu, tmp)'), so a future harmonising edit writes this.  The probe
    #  emits no Rc=1 encoding anywhere, so predicted 19/19.
    'M_CR0':    (CR0_OLD, CR0_NEW),
}

if m not in M:
    print('unknown mutant', m); sys.exit(9)
spec = M[m]
if spec is None:
    print('MUTATE BASE: baseline installed unmutated'); sys.exit(0)
old, new = spec
s = io.open(P, encoding='utf-8', newline='').read()
c = s.count(old)
if c != 1:
    print('MUTANT-TEXT-NOT-FOUND: %s matched %d times' % (m, c)); sys.exit(9)
io.open(P, 'w', encoding='utf-8', newline='').write(s.replace(old, new))
print('MUTATE %s: applied' % m)
