#!/usr/bin/env python3
#  #497: strengthen the LINEAR alignment warrant AFTER table 1, before table 2.
#  Comment-only.  It cites the SECOND guest route (ldl/ldr/sdl/sdr), which is the
#  one a reader would actually worry about and which the first draft did not
#  cover, and it records the ONE non-guest exception plus the laundering trap
#  that exception creates.
import sys

Q = chr(34)          # a literal double quote, built rather than escaped
AP = chr(39)         # a literal apostrophe

p = sys.argv[1] if len(sys.argv) > 1 else "/tmp/gx497_fix_src.c"
s = open(p).read()

old = ("\t\t\t *  ((relative_addr & 0x7f) >> 2) & 0x1f, so it reaches 31 and\n"
       "\t\t\t *  [tlbi+1] indexes 32 of a [32] array.  Only 8-byte ALIGNMENT\n"
       "\t\t\t *  keeps tlbi even and thus <= 30, and MIPS supplies that\n"
       "\t\t\t *  alignment (cpus/cpu_mips_instr_loadstore.c raises ADES/ADEL\n"
       "\t\t\t *  before the device is reached), so len == 8 implies it.\n")

new = "".join([
    "\t\t\t *  ((relative_addr & 0x7f) >> 2) & 0x1f, so it reaches 31 and\n",
    "\t\t\t *  [tlbi+1] indexes 32 of a [32] array.  Only 8-byte ALIGNMENT\n",
    "\t\t\t *  keeps tlbi even and thus <= 30.  On the GUEST paths that\n",
    "\t\t\t *  alignment is supplied by two independent mechanisms, and both\n",
    "\t\t\t *  were checked rather than assumed:\n",
    "\t\t\t *    - an ordinary ld/sd tests addr & (LS_SIZE-1) and raises\n",
    "\t\t\t *      ADES/ADEL WITHOUT calling memory_rw at all\n",
    "\t\t\t *      (cpus/cpu_mips_instr_loadstore.c);\n",
    "\t\t\t *    - the unaligned ldl/ldr/sdl/sdr helper masks the address\n",
    "\t\t\t *      itself -- cpus/cpu_mips_instr_unaligned.c computes\n",
    "\t\t\t *      aligned_addr = addr & ~(wlen-1) and passes THAT to all\n",
    "\t\t\t *      three of its memory_rw calls, so it cannot deliver an\n",
    "\t\t\t *      unaligned len == 8 either.\n",
    "\t\t\t *  Narrower accesses carry len != 8 and are declined above, and\n",
    "\t\t\t *  dev_sgi_re_init is called only from machines/machine_sgi.c,\n",
    "\t\t\t *  so no other CPU family reaches this handler.\n",
    "\t\t\t *\n",
    "\t\t\t *  ONE EXCEPTION, AND IT IS NOT A GUEST PATH: the host debugger" + AP + "s\n",
    "\t\t\t *  `put d" + AP + " prints " + Q + "WARNING: address isn" + AP + "t aligned" + Q + " and then\n",
    "\t\t\t *  PROCEEDS -- the warning is a printf, not a guard -- so it can\n",
    "\t\t\t *  hand an unaligned len == 8 straight to memory_rw.  That is why\n",
    "\t\t\t *  the invariant above is stated for GUEST paths only.  It also\n",
    "\t\t\t *  means `put d" + AP + " must NOT be used to " + Q + "witness" + Q + " the over-run:\n",
    "\t\t\t *  it bypasses the guest instruction path, so a reproduction\n",
    "\t\t\t *  built on it would be laundering rather than witnessing.\n",
    "\t\t\t *  The over-run itself stays filed as sgilinearoob, and it is\n",
    "\t\t\t *  NOT guest-reachable while this guard stands.\n",
])

n = s.count(old)
assert n == 2, "expected the note at BOTH LINEAR sites, found %d" % n
s = s.replace(old, new)
open(p, "w").write(s)
print("STRENGTHENED_SITES=%d" % n)
