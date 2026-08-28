import sys
BS = chr(92); NL = BS + 'n'
which, src = sys.argv[1], sys.argv[2]
s = open(src).read()
def sub(old, new, tag):
    global s
    n = s.count(old); assert n == 1, "%s anchor %d" % (tag, n)
    s = s.replace(old, new, 1)

if which == "M1ret":
    # Site B: break -> return.  The sketch-rule mutant: four readers proposed it.
    sub('\t\t\t    " 0x%02x -- declined.  (once) ]' + NL + '", d->cmd[0]);\n\t\t}\n\t\tbreak;\n\t}\n',
        '\t\t\t    " 0x%02x -- declined.  (once) ]' + NL + '", d->cmd[0]);\n\t\t}\n\t\treturn;\n\t}\n', "M1")
elif which == "M2nolatch":
    # Site B: latch tested but never SET -- the #460 vacuity shape
    sub('\t\t\td->warned |= GDROM_W_UNKCMD;\n', '', "M2")
elif which == "M3shared":
    # Site A reuses site B's bit: one latch for two sites
    sub('if (!(d->warned & GDROM_W_FMT)) {\n\t\t\t\td->warned |= GDROM_W_FMT;',
        'if (!(d->warned & GDROM_W_UNKCMD)) {\n\t\t\t\td->warned |= GDROM_W_UNKCMD;', "M3")
elif which == "M4nobreakA":
    # Site A: decline announced but NOT taken -- falls through to sector_nr with a bad format
    sub('\t\t\t}\n\t\t\tbreak;\n\t\t}\n\t\tsector_nr =', '\t\t\t}\n\t\t}\n\t\tsector_nr =', "M4")
elif which == "M5outerA":
    # Site A: break hoisted OUT of the else-if -- 0x20 (the ACCEPT path) now breaks too
    sub('\t\t\t}\n\t\t\tbreak;\n\t\t}\n\t\tsector_nr =', '\t\t\t}\n\t\t}\n\t\tbreak;\n\t\tsector_nr =', "M5")
elif which == "M6cond":
    # clause-(d): keep the guard, null its repair -- tail tests data_len instead of data
    sub('\tif (d->data != NULL) {\n', '\tif (d->data_len != 0) {\n', "M6")
else:
    raise SystemExit("unknown mutant " + which)
open(src, 'w').write(s)
print("MUTANT %s APPLIED" % which)
