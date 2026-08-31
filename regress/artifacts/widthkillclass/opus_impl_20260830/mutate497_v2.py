#!/usr/bin/env python3
#  #497 kill table, MUTATOR v2 -- apply ONE named mutant to a fresh copy of the
#  FIXED source.  Always starts from /tmp/gx497_fix_src.c so mutants never
#  compose.  A mutant whose find-text is absent is a HARD FAIL (presence pin).
#
#  v2 adds e_swapsite; see its comment for why xsite order needed it.
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

def msgline(sym):
    """The second physical line of one site's decline fatal()."""
    return '\t\t\t\t    "' + sym + ' -- declined.  (once) ]' + NL + '",\n'

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
    s = sub(s, HEAD, "\t\tif (len != 8 && writeflag == MEM_WRITE) {\n", 6)

elif name == "d_accept4":
    #  THE DE-ESCALATION GROWTH IN THE OTHER DIRECTION: widen the ACCEPT set
    #  rather than the refuse set -- a plausible "let us also support 32-bit
    #  access" edit.  It is the mutant that REOPENS THE LINEAR OVER-RUN, because
    #  a len=4 write then falls into the fixed-arity store.
    #  Predicted: `sw surv' stays GREEN (a short store still survives), so it is
    #  caught only by `sw lat1' (no message) and `lw surv' (read kill).
    s = sub(s, HEAD, "\t\tif (len != 8 && len != 4) {\n", 6)

elif name == "d_lessthan":
    #  EQUIVALENCE PROBE, expected NOT to die: over the reachable guest domain
    #  len is one of {1,2,4,8}, so `len < 8' and `len != 8' select the same set.
    #  A mutant that will not die is a RESULT -- here it documents that the
    #  guard's exact FORM is immaterial and only its accept SET matters.
    s = sub(s, HEAD, "\t\tif (len < 8) {\n", 6)

elif name == "d_growth":
    s = sub(s, HEAD, "\t\tif (len != 8 || (relative_addr & 8)) {\n", 6)

elif name == "d_ifnotelse":
    s = sub(s, TAIL, "\t\t}\n\n\t\tif (writeflag == MEM_WRITE) {\n", 6)

elif name == "d_returnzero":
    s = sub(s, TAIL, "\t\t\treturn 0;\n" + TAIL, 6)

elif name == "d_nolatch":
    for sym, bit, _t in SITES:
        s = sub(s,
                "\t\t\tif (!(d->warned & " + bit + ")) {\n"
                "\t\t\t\td->warned |= " + bit + ";\n"
                '\t\t\t\tfatal("[ sgi_re: unimplemented len=%i for "\n'
                + msgline(sym) +
                "\t\t\t\t    (int) len);\n"
                "\t\t\t}\n",
                '\t\t\tfatal("[ sgi_re: unimplemented len=%i for "\n'
                '\t\t\t    "' + sym + ' -- declined.  (once) ]' + NL + '",\n'
                "\t\t\t    (int) len);\n", 1)

elif name == "d_noset":
    for _sym, bit, _t in SITES:
        s = sub(s, "\t\t\t\td->warned |= " + bit + ";\n", "", 1)

elif name == "d_sharedbit":
    for _sym, bit, _t in SITES[1:]:
        s = sub(s, bit + ")", "SGIRE_W_TLBA_LEN)", 1)
        s = sub(s, bit + ";", "SGIRE_W_TLBA_LEN;", 1)

elif name == "d_bitcollide":
    s = sub(s, "SGIRE_W_TLBB_LEN  = 1 << 1,", "SGIRE_W_TLBB_LEN  = 1 << 0,", 1)

elif name == "e_wrongsite":
    #  TLB_B announces itself as TLB_A: one symbol VANISHES from the transcript.
    s = sub(s, msgline("CRIME_RE_TLB_B"), msgline("CRIME_RE_TLB_A"), 1)

elif name == "e_swapsite":
    #  ISOLATES `xsite order' FROM `xsite 6msg'.
    #  e_wrongsite makes a symbol VANISH, so it reds BOTH cross-site rows and
    #  cannot show that the order row carries weight of its own.  A SWAP keeps
    #  all six literals present exactly once -- so `xsite 6msg' stays GREEN --
    #  while putting two of them at the wrong POSITIONS, which only `xsite
    #  order' observes.  Without this mutant that row has no kill of its own and
    #  is, by the CHANNEL rule, vacuous by construction.
    s = sub(s, msgline("CRIME_RE_TLB_B"), msgline("@@SWAP@@"), 1)
    s = sub(s, msgline("CRIME_RE_TLB_C"), msgline("CRIME_RE_TLB_B"), 1)
    s = sub(s, msgline("@@SWAP@@"),       msgline("CRIME_RE_TLB_C"), 1)

else:
    sys.exit("unknown mutant %s" % name)

open(dst, "w").write(s)
print("MUTANT_APPLIED=%s" % name)
