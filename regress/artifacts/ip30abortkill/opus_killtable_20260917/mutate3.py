import sys
F = "/tmp/gxo498/src/devices/dev_sgi_re.c"
ORIG = "/tmp/gxo498_orig_dev_sgi_re.c"
which = sys.argv[1]
src = open(ORIG, encoding="utf-8").read()
T = chr(9); NL = chr(10); BS = chr(92)
LATCH = (T+T+"if (!(d->warned & SGIRE_W_DE_LEN)) {"+NL
       + T+T+T+"d->warned |= SGIRE_W_DE_LEN;"+NL
       + T+T+T+'fatal("[ sgi_de: unimplemented len=%i -- declined."'+NL
       + T+T+T+'    "  (once) ]'+BS+'n", (int) len);'+NL
       + T+T+"}"+NL
       + T+T+"goto de_declined;"+NL)
TAIL = (" de_declined:"+NL
      + T+"/*  #498: a declined access jumps here, skipping BOTH the register"+NL
      + T+"    switch and draw_primitive(), and is still answered.  */"+NL
      + T+"if (writeflag == MEM_READ)"+NL
      + T+T+"memory_writemax64(cpu, data, len, odata);"+NL)
M = {
 "bracegoto": (LATCH,
    T+T+"if (!(d->warned & SGIRE_W_DE_LEN)) {"+NL
  + T+T+T+"d->warned |= SGIRE_W_DE_LEN;"+NL
  + T+T+T+'fatal("[ sgi_de: unimplemented len=%i -- declined."'+NL
  + T+T+T+'    "  (once) ]'+BS+'n", (int) len);'+NL
  + T+T+T+"goto de_declined;"+NL
  + T+T+"}"+NL),
 "bit5collide": (T+"SGIRE_W_DE_LEN    = 1 << 6,"+NL,
                 T+"SGIRE_W_DE_LEN    = 1 << 5,"+NL),
 "skipans": (TAIL,
      " de_declined:"+NL
    + T+"if (writeflag == MEM_READ && len >= 4)"+NL
    + T+T+"memory_writemax64(cpu, data, len, odata);"+NL),
}
if which == "base":
    open(F,"w",encoding="utf-8",newline="").write(src); print("BASELINE RESTORED"); sys.exit(0)
find, repl = M[which]
n = src.count(find)
if n != 1:
    print("MUTANT-TEXT-NOT-UNIQUE %s count=%d -- FAIL" % (which, n)); sys.exit(9)
open(F,"w",encoding="utf-8",newline="").write(src.replace(find, repl))
print("MUTANT APPLIED: %s" % which)
