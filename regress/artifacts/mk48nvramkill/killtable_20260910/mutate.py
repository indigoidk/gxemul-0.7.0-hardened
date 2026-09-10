#!/usr/bin/env python3
#  #521 mk48nvramkill mutator.  One named literal find/replace per mutant.
#  MUTANT-TEXT-NOT-FOUND is exit 9, a HARD FAILURE -- so every mutant doubles as a
#  PRESENCE PIN on the fix's own text: if the fix is edited away, the table cannot
#  silently score a build that no longer contains it.
#  Usage: mutate.py <path-to-clone-dev_mk48txx.c> <mutant>
import io, sys

P, m = sys.argv[1], sys.argv[2]
T = '\t'

FIXED_LOW = T + "if (relative_addr < MK48T08_CLKOFF + MK48TXX_ICSR ||\n"
UPPER     = T + "    relative_addr >= MK48T08_CLKOFF + MK48TXX_ISEC) {\n"
#  THE STORE LINE APPEARS TWICE -- once in the accept block and once in the ICSR case
#  arm -- so the accept-block one is anchored by the `goto ret;' that follows it.  The
#  exactly-one-match rule CAUGHT this before the table ran, which is the presence pin
#  doing its job rather than a near miss.
STORE     = T*3 + "d->reg[relative_addr] = idata;\n" + T*2 + "goto ret;\n"

M = {
    #  BASE: the fix, unmutated.  Present so the base score comes from the same driver
    #  and the same frozen probe as every other leg.
    'BASE': None,

    #  M_OLD -- RESTORE THE OLD DISPATCH.  This is the round's stand-in for floor clause
    #  (b): the diff removes no kill statement, it makes one UNREACHABLE, so a verbatim
    #  reinstatement of the `default:' arm is a no-op or dead code and no channel can see
    #  it.  Putting the LOWER BOUND back is the distinguishable form, and it restores the
    #  defect exactly.
    'M_OLD': (FIXED_LOW, T + "if (relative_addr < MK48T08_CLKOFF ||\n"),

    #  M_HALF -- a PARTIAL boundary move.  The repair's own predicate, weakened to the
    #  least-restrictive form that still reads like the same check.  Offsets 0x1ff4..7
    #  remain fatal.  A detector that passes this has pinned the bound's existence and
    #  not its VALUE.
    'M_HALF': (FIXED_LOW, T + "if (relative_addr < MK48T08_CLKOFF + 4 ||\n"),

    #  M_ICSR -- move the UPPER bound instead, so the window is empty and the implemented
    #  control case is never reached.  The near/far-bound lesson: a bound is pinned only
    #  by a row that sits on it.
    'M_ICSR': (UPPER, T + "    relative_addr >= MK48T08_CLKOFF + MK48TXX_ICSR) {\n"),

    #  M_NULL -- THE NULLED REPAIR, floor clause (d).  The corrected guard is KEPT and its
    #  effect removed: accesses still take the accept path, but a write stores nothing.
    #  A survival oracle cannot see this -- both forms survive -- which is why the round
    #  needs a round-trip row rather than a "the host is still alive" row.
    #  *** REBUILT 2026-09-10 AFTER THE PASS-2 PANEL CAUGHT IT, and the first form was not
    #  the mutant this table said it was.  It replaced the store with a COMMENT, and a
    #  comment is WHITESPACE -- so `goto ret;' became the if-body, READS stopped taking the
    #  accept path and fell into the switch, and the leg measured "reads are fatal
    #  everywhere" while the record claimed clause (d) had been satisfied.  The write-side
    #  rows never saw a missing store at all.  The replacement is now a real BRACED
    #  statement, so the `if' has a body and control flow is unchanged. ***
    'M_NULL': (STORE, T*2 + "{ /*  M_NULL: backing store removed  */ }\n" + T*2 + "goto ret;\n"),

    #  HEAD -- whole-file null medium: the committed pre-fix source.
    'HEAD': ('WHOLE-FILE', None),
}

if m not in M:
    print('unknown mutant', m); sys.exit(9)

spec = M[m]
if spec is None:
    print('MUTATE BASE: baseline installed unmutated'); sys.exit(0)

if spec[0] == 'WHOLE-FILE':
    import subprocess
    r = subprocess.run(['git', '-C', '/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC',
                        'show', 'HEAD:src/devices/dev_mk48txx.c'],
                       stdout=subprocess.PIPE)
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
