#!/usr/bin/env python3
#  #522 ppcrldiclzero mutator.  One named literal find/replace per mutant.
#  MUTANT-TEXT-NOT-FOUND is exit 9, a HARD FAILURE, so every mutant doubles as a PRESENCE
#  PIN on the fix's own text.  That pin has now earned its keep FOUR times in two rounds:
#  an ambiguous anchor matching two sites, an M_NULL that replaced a statement with a
#  COMMENT so the following `goto' became the if-body, a driver calling the PREVIOUS
#  round's mutator, and a backslash level eaten on the bash->heredoc->python path that
#  turned every "\n" in this file into a real newline.
#
#  *** THAT LAST ONE IS WHY THIS FILE IS WRITTEN DIRECTLY RATHER THAN GENERATED. ***  The
#  carrier's rule is that one backslash level is consumed in BOTH directions on that path,
#  and the remedy is to write the file with an editor, not to reason about the level count.
#
#  Usage: mutate.py <path-to-clone-cpu_ppc_instr.c> <mutant>
import io, sys, subprocess

P, m = sys.argv[1], sys.argv[2]
T = '\t'
NL = chr(10)

FIXED   = T*2 + "tmp2 |= ((uint64_t)1 << (63-mb));" + NL
ASSIGN  = T + "cpu->cd.ppc.gpr[ra] = tmp & tmp2;" + NL

#  The four decode/CR0 literals come from PASS 2, which built its own independent table and
#  found TWO TOTAL ESCAPES of the 19-row instrument.  Reused verbatim from the measuring
#  seat's mutator so the legs are comparable across the two tables.
SHMB_OLD = (T + "int sh = ((ic->arg[0] >> 11) & 31) | ((ic->arg[0] & 2) << 4);" + NL
            + T + "int mb = ((ic->arg[0] >> 6) & 31) | (ic->arg[0] & 0x20);" + NL)
SH5_NEW  = (T + "int sh = ((ic->arg[0] >> 11) & 31);" + NL
            + T + "int mb = ((ic->arg[0] >> 6) & 31) | (ic->arg[0] & 0x20);" + NL)
MB5_NEW  = (T + "int sh = ((ic->arg[0] >> 11) & 31) | ((ic->arg[0] & 2) << 4);" + NL
            + T + "int mb = ((ic->arg[0] >> 6) & 31);" + NL)
CR0_OLD  = (T + "cpu->cd.ppc.gpr[ra] = tmp & tmp2;" + NL + T + "if (rc)" + NL
            + T*2 + "update_cr0(cpu, cpu->cd.ppc.gpr[ra]);" + NL)
CR0_NEW  = (T + "cpu->cd.ppc.gpr[ra] = tmp & tmp2;" + NL + T + "if (rc)" + NL
            + T*2 + "update_cr0(cpu, tmp);" + NL)

M = {
    'BASE': None,

    #  M_ORIG -- THE DEFECT VERBATIM.  Floor clause (b), and unlike #521 it is satisfiable
    #  literally here: this diff changes a STATEMENT rather than making one unreachable,
    #  so putting it back restores exactly what shipped.
    'M_ORIG': (FIXED, T*2 + "tmp |= ((uint64_t)1 << (63-mb));" + NL),

    #  M_NAIVE -- `&' becomes `|'.  The product comment warns against this shape, and a
    #  warning no mutant tests is a claim nobody has checked.  It ships an OR where the
    #  architecture says AND: 126 of 190 cells wrong, measured.
    'M_NAIVE': (ASSIGN, T + "cpu->cd.ppc.gpr[ra] = tmp | tmp2;" + NL),

    #  M_MASKEND -- THE NULLED REPAIR, floor clause (d).  The corrected `tmp2 |=' is KEPT
    #  and its EFFECT weakened, so the mask is built into the right variable and is the
    #  wrong mask.  A detector that only checks "not zero any more" passes this.
    #
    #  *** RECORDED RATHER THAN REBUILT: this mutant is ITSELF UNDEFINED.  At mb == 63 it
    #  evaluates 1 << -1.  Pass 2 measured the consequence -- `zx32' returned
    #  0x800000004afef00d with bit 63 WRAPPED IN, and every MB=0 cell comes out CORRECT,
    #  which is why `census wrong' is 126 rather than 190.  The clause is discharged either
    #  way, but the clean form was `mb <= 62' -- weaken the LOOP BOUND, not the shift
    #  count.  Kept as-run so the two tables stay comparable. ***
    'M_MASKEND': (FIXED, T*2 + "tmp2 |= ((uint64_t)1 << (62-mb));" + NL),

    #  M_NOAND -- discard the rotated data and keep only the mask.  Separates "the mask is
    #  built correctly" from "the mask is APPLIED to the rotated value".
    'M_NOAND': (ASSIGN, T + "cpu->cd.ppc.gpr[ra] = tmp2;" + NL),

    #  M_SH5 -- drop the sh5 bit from the SH decode.  *** ESCAPED THE 19-ROW INSTRUMENT
    #  19/19. ***  Every rldicl with SH >= 32 then rotates by SH-32, and the manual's
    #  simplified mnemonics make `srdi rA,rS,n' EQUAL to `rldicl rA,rS,64-n,n' -- so EVERY
    #  logical right shift by 1..32 has SH >= 32.  The old rows drove SH 0 and 8 only, both
    #  below 32, so the sh5 bit was never load-bearing anywhere in the instrument.
    'M_SH5': (SHMB_OLD, SH5_NEW),

    #  M_MB5 -- the IDENTICAL edit on the SAME line, dropping mb5 instead.  KILLED 16/19.
    #  Carried as the control that makes M_SH5 a result rather than an anecdote: same
    #  anchor, same kind of mutant, one field covered and the other invisible.
    'M_MB5': (SHMB_OLD, MB5_NEW),

    #  M_CR0 -- feed update_cr0 the UNMASKED rotated value.  *** ESCAPED 19/19, AND IT IS
    #  NOT AN INVENTED MUTANT: this is the token X(rldicr) ships, CORRECTLY, ten lines below
    #  -- there `tmp' IS the destination.  A future editor harmonising the two handlers
    #  writes exactly this. ***  The old instrument emitted rc=0 on every encoding, so the
    #  whole record-form path was unexecuted.
    'M_CR0': (CR0_OLD, CR0_NEW),

    #  M_NOMASK -- delete the `& tmp2' on the FIXED code, which ships ROTL64 ALONE with the
    #  mask ignored.  Distinct from M_NAIVE: before the fix that edit would have shipped the
    #  OR, because the mask was in `tmp'.  Pass 2 measured it at 16/19.
    'M_NOMASK': (ASSIGN, T + "cpu->cd.ppc.gpr[ra] = tmp;" + NL),

    'HEAD': ('WHOLE-FILE', None),
}

if m not in M:
    print('unknown mutant', m); sys.exit(9)

spec = M[m]
if spec is None:
    print('MUTATE BASE: baseline installed unmutated'); sys.exit(0)

if spec[0] == 'WHOLE-FILE':
    r = subprocess.run(['git', '-C', '/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC',
                        'show', 'HEAD:src/cpus/cpu_ppc_instr.c'], stdout=subprocess.PIPE)
    if r.returncode != 0 or not r.stdout:
        print('HEAD checkout FAILED'); sys.exit(9)
    io.open(P, 'wb').write(r.stdout)
    print('MUTATE HEAD: committed pre-fix file installed (whole-file null medium)')
    sys.exit(0)

old, new = spec
s = io.open(P, encoding='utf-8', newline='').read()
c = s.count(old)
if c != 1:
    print('MUTANT-TEXT-NOT-FOUND: %s matched %d times' % (m, c)); sys.exit(9)
io.open(P, 'w', encoding='utf-8', newline='').write(s.replace(old, new))
print('MUTATE %s: applied' % m)
