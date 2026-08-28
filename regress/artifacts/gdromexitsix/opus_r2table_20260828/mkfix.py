import sys
BS = chr(92)
NL = BS + 'n'          # the two characters backslash-n, as they appear in C source
src = sys.argv[1]
s = open(src).read()

def sub(s, old, new, tag):
    n = s.count(old)
    assert n == 1, "%s anchor count %d" % (tag, n)
    return s.replace(old, new, 1)

# 1) two new warn bits
old = "\tGDROM_W_TOCLEN_B,\t/*  #489: the SEVENTH, and the bit the trigger was set for  */\n\tGDROM_W_NBITS\n"
new = ("\tGDROM_W_TOCLEN_B,\t/*  #489: the SEVENTH, and the bit the trigger was set for  */\n"
       "\tGDROM_W_FMT_B,\n\tGDROM_W_UNKCMD_B,\n\tGDROM_W_NBITS\n")
s = sub(s, old, new, "enum")

old = "#define\tGDROM_W_TOCLEN\t(1u << GDROM_W_TOCLEN_B)\n"
new = old + "#define\tGDROM_W_FMT\t(1u << GDROM_W_FMT_B)\n#define\tGDROM_W_UNKCMD\t(1u << GDROM_W_UNKCMD_B)\n"
s = sub(s, old, new, "masks")

# 2) SITE A
old = ('\t\t} else if (d->cmd[1] != 0x20) {\n'
       '\t\t\tfatal("GDROM unimplemented data format 0x%02x' + NL + '",\n'
       '\t\t\t    d->cmd[1]);\n'
       '\t\t\texit(1);\n'
       '\t\t}\n')
new = ('\t\t} else if (d->cmd[1] != 0x20) {\n'
       '\t\t\tif (!(d->warned & GDROM_W_FMT)) {\n'
       '\t\t\t\td->warned |= GDROM_W_FMT;\n'
       '\t\t\t\tfatal("[ dreamcast_gdrom: unimplemented data"\n'
       '\t\t\t\t    " format 0x%02x -- declined.  (once) ]' + NL + '",\n'
       '\t\t\t\t    d->cmd[1]);\n'
       '\t\t\t}\n'
       '\t\t\tbreak;\n'
       '\t\t}\n')
s = sub(s, old, new, "siteA")

# 3) SITE B
old = ('\tdefault:fatal("GDROM handle_command: unimplemented command 0x%02x"\n'
       '\t\t    "' + NL + '", d->cmd[0]);\n'
       '\t\texit(1);\n'
       '\t}\n')
new = ('\tdefault:if (!(d->warned & GDROM_W_UNKCMD)) {\n'
       '\t\t\td->warned |= GDROM_W_UNKCMD;\n'
       '\t\t\tfatal("[ dreamcast_gdrom: unimplemented command"\n'
       '\t\t\t    " 0x%02x -- declined.  (once) ]' + NL + '", d->cmd[0]);\n'
       '\t\t}\n'
       '\t\tbreak;\n'
       '\t}\n')
s = sub(s, old, new, "siteB")

open(src, 'w').write(s)
print("FIX APPLIED OK")
