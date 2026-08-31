#!/usr/bin/env python3
#  #497 kill table -- apply ONE named mutant to a fresh copy of the FIXED source.
#  Always starts from /tmp/gx497_fix_src.c so mutants never compose.
#  A mutant whose find-text is absent is a HARD FAIL (presence pin).
import sys

BS = chr(92)
NL = BS + "n"

name = sys.argv[1]
dst  = sys.argv[2]
s    = open("/tmp/gx497_fix_src.c").read()

SITES = [
    ("CRIME_RE_TLB_A",    "SGIRE_W_TLBA_LEN", "tlba"),
    ("CRIME_RE_TLB_B",    "SGIRE_W_TLBB_LEN", "tlbb"),
    ("CRIME_RE_TLB_C",    "SGIRE_W_TLBC_LEN", "tlbc"),
    ("CRIME_RE_TEX",      "SGIRE_W_TEX_LEN",  "tex"),
    ("CRIME_RE_LINEAR_A", "SGIRE_W_LINA_LEN", "lina"),
    ("CRIME_RE_LINEAR_B", "SGIRE_W_LINB_LEN", "linb"),
]

HEAD = "\t\tif (len != 8) {\n"
TAIL = "\t\t} else if (writeflag == MEM_WRITE) {\n"

def block(text, sym):
    """(start, end) of one site's whole width-guard block in the FIXED source."""
    k = text.index('"' + sym + ' -- declined.')
    st = text.rindex(HEAD, 0, k)
    en = text.index(TAIL, k) + len(TAIL)
    return st, en

def orig_block(sym):
    return (HEAD +
            '\t\t\tfatal("TODO: unimplemented len=%i for ' + sym + NL + '", len);\n'
            "\t\t\texit(1);\n"
            "\t\t}\n"
            "\n"
            "\t\tif (writeflag == MEM_WRITE) {\n")

def sub(text, old, new, want):
    got = text.count(old)
    assert got == want, "MUTANT_TEXT_NOT_FOUND: %r wanted %d got %d" % (old[:60], want, got)
    return text.replace(old, new)

def reinstate(text, syms):
    for sym in syms:
        st, en = block(text, sym)
        text = text[:st] + orig_block(sym) + text[en:]
    return text

# ---------------------------------------------------------------- clause (b)
if name == "b_all":
    s = reinstate(s, [x[0] for x in SITES])
elif name.startswith("b_"):
    tag = name[2:]
    sym = [x[0] for x in SITES if x[2] == tag]
    assert sym, "unknown site tag %s" % tag
    s = reinstate(s, sym)

# ---------------------------------------------------------------- clause (d)
elif name == "d_andwrite":
    # if (X) -> if (X && Y) on the DOMINATING predicate.  The canonical form.
    s = sub(s, HEAD, "\t\tif (len != 8 && writeflag == MEM_WRITE) {\n", 6)

elif name == "d_growth":
    # guard-only growth: swallows LEGAL 8-byte accesses at offsets with bit 3 set.
    s = sub(s, HEAD, "\t\tif (len != 8 || (relative_addr & 8)) {\n", 6)

elif name == "d_ifnotelse":
    # keep the decline, NULL its repair: a declined access falls through into
    # the store/read arms again.  This is the else-if splice itself removed.
    s = sub(s, TAIL, "\t\t}\n\n\t\tif (writeflag == MEM_WRITE) {\n", 6)

elif name == "d_returnzero":
    # the edit the block comment says would be wrong: decline by returning 0.
    s = sub(s, TAIL, "\t\t\treturn 0;\n" + TAIL, 6)

elif name == "d_nolatch":
    # M3: delete the latch entirely, keep the message.  Substring-presence rows
    # pass this; only a COUNT reds.
    for sym, bit, _t in SITES:
        s = sub(s,
                "\t\t\tif (!(d->warned & " + bit + ")) {\n"
                "\t\t\t\td->warned |= " + bit + ";\n"
                '\t\t\t\tfatal("[ sgi_re: unimplemented len=%i for "\n'
                '\t\t\t\t    "' + sym + ' -- declined.  (once) ]' + NL + '",\n'
                "\t\t\t\t    (int) len);\n"
                "\t\t\t}\n",
                '\t\t\tfatal("[ sgi_re: unimplemented len=%i for "\n'
                '\t\t\t    "' + sym + ' -- declined.  (once) ]' + NL + '",\n'
                "\t\t\t    (int) len);\n", 1)

elif name == "d_noset":
    # keep the test, drop the SET: the latch never latches.
    for _sym, bit, _t in SITES:
        s = sub(s, "\t\t\t\td->warned |= " + bit + ";\n", "", 1)

elif name == "d_sharedbit":
    # M2 in its blunt form: all six sites share ONE bit.
    for _sym, bit, _t in SITES[1:]:
        s = sub(s, bit + ")", "SGIRE_W_TLBA_LEN)", 1)
        s = sub(s, bit + ";", "SGIRE_W_TLBA_LEN;", 1)

elif name == "d_bitcollide":
    # M2 in its subtle form: ONE enumerator duplicated -- a copy-paste slip.
    s = sub(s, "SGIRE_W_TLBB_LEN  = 1 << 1,", "SGIRE_W_TLBB_LEN  = 1 << 0,", 1)

elif name == "e_wrongsite":
    # attribution: TLB_B announces itself as TLB_A.
    s = sub(s, '\t\t\t\t    "CRIME_RE_TLB_B -- declined.  (once) ]' + NL + '",\n',
               '\t\t\t\t    "CRIME_RE_TLB_A -- declined.  (once) ]' + NL + '",\n', 1)

else:
    sys.exit("unknown mutant %s" % name)

open(dst, "w").write(s)
print("MUTANT_APPLIED=%s" % name)
