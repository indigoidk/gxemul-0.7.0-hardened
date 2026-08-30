import re, sys
BS = chr(92)
NL = BS + "n"          # the two characters that end a C string literal
p = "/tmp/gxopus_497/src/devices/dev_sgi_re.c"
s = open(p).read()

SITES = [("CRIME_RE_TLB_A","SGIRE_W_TLBA_LEN"),
         ("CRIME_RE_TLB_B","SGIRE_W_TLBB_LEN"),
         ("CRIME_RE_TLB_C","SGIRE_W_TLBC_LEN"),
         ("CRIME_RE_TEX","SGIRE_W_TEX_LEN"),
         ("CRIME_RE_LINEAR_A","SGIRE_W_LINA_LEN"),
         ("CRIME_RE_LINEAR_B","SGIRE_W_LINB_LEN")]

anchor = "struct sgi_re_data {"
assert s.count(anchor) == 1
bits = "\n".join("\t%s\t= 1 << %d," % (b, i) for i, (_, b) in enumerate(SITES))
s = s.replace(anchor,
  "/*  #497: one latch bit per WIDTH-guard site.  Six, not one: the six\n"
  "    windows are DIFFERENT address ranges a driver walks in ONE session,\n"
  "    so they are NOT mutually exclusive at runtime -- which is exactly\n"
  "    the discriminator dev_wdc.c records for #337's shared warned_badlen.  */\n"
  "enum {\n" + bits + "\n};\n\n" + anchor + "\n\tuint32_t\twarned;\n", 1)

n = 0
for sym, bit in SITES:
    old = ("\t\tif (len != 8) {\n"
           '\t\t\tfatal("TODO: unimplemented len=%i for ' + sym + NL + '", len);\n'
           "\t\t\texit(1);\n"
           "\t\t}\n"
           "\n"
           "\t\tif (writeflag == MEM_WRITE) {\n")
    new = ("\t\tif (len != 8) {\n"
           "\t\t\t/*  #497: a GUEST choosing an access width used to end\n"
           "\t\t\t    the host process here.  Decline instead; the common\n"
           "\t\t\t    tail still answers a READ with odata (0).  else-if,\n"
           "\t\t\t    NOT an early return: a return here would skip that\n"
           "\t\t\t    tail, and 'return 0' would raise EXCEPTION_DBE in\n"
           "\t\t\t    the guest (see cpus/memory_rw.c res<=0 arm).  */\n"
           "\t\t\tif (!(d->warned & " + bit + ")) {\n"
           "\t\t\t\td->warned |= " + bit + ";\n"
           '\t\t\t\tfatal("[ sgi_re: unimplemented len=%i for "\n'
           '\t\t\t\t    "' + sym + ' -- declined.  (once) ]' + NL + '",\n'
           "\t\t\t\t    (int)len);\n"
           "\t\t\t}\n"
           "\t\t} else if (writeflag == MEM_WRITE) {\n")
    assert s.count(old) == 1, "site %s: count=%d" % (sym, s.count(old))
    s = s.replace(old, new, 1)
    n += 1

assert n == 6
open(p, "w").write(s)
print("APPLIED_SITES=%d" % n)
print("exit1_remaining_in_file=%d" % len(re.findall(r"^\s+exit\(1\);", s, re.M)))
