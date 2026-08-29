import sys
BS = chr(92)
NL = BS + 'n'
src, tag = sys.argv[1], sys.argv[2]
s = open(src).read()

def sub(s, old, new, name):
    n = s.count(old)
    assert n == 1, "MUTANT TEXT NOT FOUND (or ambiguous): %s count=%d" % (name, n)
    return s.replace(old, new, 1)

#  The POST-FIX Site A decline block, verbatim from mkfix.py's `new`.
SITEA = ('\t\t\tif (!(d->warned & GDROM_W_FMT)) {\n'
         '\t\t\t\td->warned |= GDROM_W_FMT;\n')
SITEB = ('\tdefault:if (!(d->warned & GDROM_W_UNKCMD)) {\n'
         '\t\t\td->warned |= GDROM_W_UNKCMD;\n')

if tag == "M_retA":
    #  Site A declines and RETURNS instead of BREAKING -- the M1ret defect at
    #  the OTHER de-fatalised arm.  Anchor on the decline's closing brace + break.
    old = ('\t\t\t\t    d->cmd[1]);\n'
           '\t\t\t}\n'
           '\t\t\tbreak;\n')
    new = ('\t\t\t\t    d->cmd[1]);\n'
           '\t\t\t}\n'
           '\t\t\treturn;\n')
    s = sub(s, old, new, tag)

elif tag == "Ma_toclen":
    #  Site A's latch bit COLLIDES with #489's GDROM_W_TOCLEN.
    new = ('\t\t\tif (!(d->warned & GDROM_W_TOCLEN)) {\n'
           '\t\t\t\td->warned |= GDROM_W_TOCLEN;\n')
    s = sub(s, SITEA, new, tag)

elif tag == "Mb_toclen":
    new = ('\tdefault:if (!(d->warned & GDROM_W_TOCLEN)) {\n'
           '\t\t\td->warned |= GDROM_W_TOCLEN;\n')
    s = sub(s, SITEB, new, tag)

elif tag == "M_growA":
    #  ACCEPT-SIDE GROWTH at Site A: the format predicate's accepted constant
    #  moves by one, so the legal 0x20 is newly declined.  The diagnostic's
    #  operand is `d->cmd[1]`, a variable the guard cannot mask, so guard-only
    #  is non-equivalent AND is the least-observable form (#451's discriminator).
    s = sub(s, "d->cmd[1] != 0x20", "d->cmd[1] != 0x21", tag)

elif tag == "M_a24fold":
    #  "Simplify": route every unimplemented format through the upstream
    #  warn-and-continue arm.  The decline disappears; the bare regex
    #  `unimplemented data format` still matches once.
    s = sub(s, "if (d->cmd[1] == 0x24) {", "if (d->cmd[1] != 0x20) {", tag)

elif tag == "M_growB":
    #  ACCEPT-SIDE GROWTH at Site B: Mount is newly unhandled.
    s = sub(s, "\tcase 0x70:\n", "\tcase 0x71:\n", tag)

else:
    raise SystemExit("unknown mutant tag %s" % tag)

open(src, 'w').write(s)
print("MUTANT %s APPLIED OK" % tag)
