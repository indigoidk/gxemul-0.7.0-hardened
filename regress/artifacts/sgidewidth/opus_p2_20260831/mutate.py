import sys, shutil
F = "/tmp/gxo498/src/devices/dev_sgi_re.c"
ORIG = "/tmp/gxo498_orig_dev_sgi_re.c"
which = sys.argv[1]
src = open(ORIG, encoding="utf-8").read()

T = chr(9)
NL = chr(10)

LATCH = (T+T+"if (!(d->warned & SGIRE_W_DE_LEN)) {"+NL
       + T+T+T+"d->warned |= SGIRE_W_DE_LEN;"+NL
       + T+T+T+'fatal("[ sgi_de: unimplemented len=%i -- declined."'+NL
       + T+T+T+'    "  (once) ]'+chr(92)+'n", (int) len);'+NL
       + T+T+"}"+NL
       + T+T+"goto de_declined;"+NL)

M = {}
#  M1: the brace slip -- goto moved INSIDE the latch block.
M["bracegoto"] = (LATCH,
    T+T+"if (!(d->warned & SGIRE_W_DE_LEN)) {"+NL
  + T+T+T+"d->warned |= SGIRE_W_DE_LEN;"+NL
  + T+T+T+'fatal("[ sgi_de: unimplemented len=%i -- declined."'+NL
  + T+T+T+'    "  (once) ]'+chr(92)+'n", (int) len);'+NL
  + T+T+T+"goto de_declined;"+NL
  + T+T+"}"+NL)

#  M2: clause-(d) bound relaxation on the predicate the fix depends on.
M["accept2"] = (T+"} else if (len == 4) {"+NL,
                T+"} else if (len == 4 || len == 2) {"+NL)

#  M3: the declined READ is no longer answered by memory_writemax64.
M["skipans"] = (T+"if (writeflag == MEM_READ)"+NL+T+T+"memory_writemax64(cpu, data, len, odata);"+NL,
                T+"if (writeflag == MEM_READ && len >= 4)"+NL+T+T+"memory_writemax64(cpu, data, len, odata);"+NL)

#  M4: latch bit collides with an existing one at the ENUM (not the use site).
M["bit5collide"] = (T+"SGIRE_W_DE_LEN    = 1 << 6,"+NL,
                    T+"SGIRE_W_DE_LEN    = 1 << 5,"+NL)

find, repl = M[which]
n = src.count(find)
if n != 1:
    print("MUTANT-TEXT-NOT-UNIQUE %s count=%d -- FAIL" % (which, n))
    sys.exit(9)
open(F, "w", encoding="utf-8", newline="").write(src.replace(find, repl))
print("MUTANT APPLIED: %s" % which)
