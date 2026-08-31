#!/usr/bin/env python3
"""mkvariant.py <variant> <pristine_src> <out_src>

Generates one variant of dev_sgi_re.c from the COMMITTED source.

TWO HAZARDS DESIGNED OUT, both from the carrier:
  * the OLD text is EXTRACTED from the source between anchors, never
    transcribed -- a hand-copied block already failed this script's own
    presence pin once;
  * every backslash that must survive into the C file is chr(92).  Writing
    a literal backslash through Bash -> heredoc -> Python loses one level,
    which silently turned an escaped \n into a real newline and split a C
    string literal.
A find-text that is absent is a HARD FAIL (presence pin)."""
import sys

BS = chr(92)
NL = BS + "n"          # the two characters a C string needs
Q  = '"'

variant, src_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src_path).read()

def die(msg):
    sys.stderr.write(msg + "\n"); sys.exit(9)

# ---- EXTRACT the committed catch-all rather than transcribing it -----------
A = "\t} else {\n\t\tif (writeflag == MEM_WRITE)\n\t\t\tfatal(" + Q + "[ sgi_re: unimplemented write to "
if A not in s:
    die("ANCHOR A NOT FOUND")
start = s.index(A)
endmark = "\t\texit(1);\n\t}\n"
end = s.index(endmark, start)
if end < 0:
    die("ANCHOR B NOT FOUND")
OLD = s[start:end + len(endmark)]
if s.count(OLD) != 1:
    die("CATCH-ALL BLOCK IS NOT UNIQUE (%d matches)" % s.count(OLD))

ENUM_OLD = "\tSGIRE_W_LINB_LEN  = 1 << 5,\n"
if ENUM_OLD not in s:
    die("ENUM TEXT NOT FOUND")
ENUM_NEW = ENUM_OLD + "\tSGIRE_W_UNMAP_WR  = 1 << 6,\n\tSGIRE_W_UNMAP_RD  = 1 << 7,\n"

def announce(bit_w, bit_r, tail):
    L = []
    L.append("\t} else {\n")
    L.append("\t\tif (writeflag == MEM_WRITE) {\n")
    L.append("\t\t\tif (!(d->warned & " + bit_w + ")) {\n")
    L.append("\t\t\t\td->warned |= " + bit_w + ";\n")
    L.append("\t\t\t\tfatal(" + Q + "[ sgi_re: unimplemented write to " + Q + "\n")
    L.append("\t\t\t\t    " + Q + "address 0x%llx, data=0x%016llx -- " + Q + "\n")
    L.append("\t\t\t\t    " + Q + "declined.  (once) ]" + NL + Q + ",\n")
    L.append("\t\t\t\t    (long long)relative_addr, (long long)idata);\n")
    L.append("\t\t\t}\n")
    L.append("\t\t} else {\n")
    L.append("\t\t\tif (!(d->warned & " + bit_r + ")) {\n")
    L.append("\t\t\t\td->warned |= " + bit_r + ";\n")
    L.append("\t\t\t\tfatal(" + Q + "[ sgi_re: unimplemented read from address" + Q + "\n")
    L.append("\t\t\t\t    " + Q + " 0x%llx -- declined.  (once) ]" + NL + Q + ",\n")
    L.append("\t\t\t\t    (long long)relative_addr);\n")
    L.append("\t\t\t}\n")
    L.append("\t\t}\n")
    L.append(tail)
    L.append("\t}\n")
    return "".join(L)

if variant == "base":
    pass
elif variant == "fix":
    s = s.replace(ENUM_OLD, ENUM_NEW).replace(OLD, announce("SGIRE_W_UNMAP_WR", "SGIRE_W_UNMAP_RD", ""))
elif variant == "mret0":
    s = s.replace(ENUM_OLD, ENUM_NEW).replace(OLD, announce("SGIRE_W_UNMAP_WR", "SGIRE_W_UNMAP_RD", "\t\treturn 0;\n"))
elif variant == "mlatch":
    s = s.replace(OLD, announce("SGIRE_W_TEX_LEN", "SGIRE_W_TEX_LEN", ""))
elif variant == "mwonly":
    L = []
    L.append("\t} else {\n")
    L.append("\t\tif (writeflag == MEM_WRITE) {\n")
    L.append("\t\t\tif (!(d->warned & SGIRE_W_UNMAP_WR)) {\n")
    L.append("\t\t\t\td->warned |= SGIRE_W_UNMAP_WR;\n")
    L.append("\t\t\t\tfatal(" + Q + "[ sgi_re: unimplemented write to " + Q + "\n")
    L.append("\t\t\t\t    " + Q + "address 0x%llx, data=0x%016llx -- " + Q + "\n")
    L.append("\t\t\t\t    " + Q + "declined.  (once) ]" + NL + Q + ",\n")
    L.append("\t\t\t\t    (long long)relative_addr, (long long)idata);\n")
    L.append("\t\t\t}\n")
    L.append("\t\t} else {\n")
    L.append("\t\t\tfatal(" + Q + "[ sgi_re: unimplemented read from address" + Q + "\n")
    L.append("\t\t\t    " + Q + " 0x%llx ]" + NL + Q + ", (long long)relative_addr);\n")
    L.append("\t\t\texit(1);\n")
    L.append("\t\t}\n")
    L.append("\t}\n")
    s = s.replace(ENUM_OLD, ENUM_NEW).replace(OLD, "".join(L))
elif variant == "mshrink":
    s = s.replace(ENUM_OLD, ENUM_NEW).replace(OLD, announce("SGIRE_W_UNMAP_WR", "SGIRE_W_UNMAP_RD", ""))
    A_OLD = "relative_addr >= CRIME_RE_LINEAR_A && relative_addr < CRIME_RE_LINEAR_A + 0x80"
    if A_OLD not in s:
        die("SHRINK TEXT NOT FOUND")
    s = s.replace(A_OLD, A_OLD.replace("+ 0x80", "+ 0x40"))
elif variant == "mshrinkb":
    s = s.replace(ENUM_OLD, ENUM_NEW).replace(OLD, announce("SGIRE_W_UNMAP_WR", "SGIRE_W_UNMAP_RD", ""))
    B_OLD = "relative_addr >= CRIME_RE_LINEAR_B && relative_addr < CRIME_RE_LINEAR_B + 0x80"
    if B_OLD not in s:
        die("SHRINKB TEXT NOT FOUND")
    s = s.replace(B_OLD, B_OLD.replace("+ 0x80", "+ 0x40"))
elif variant == "mtexshrink":
    s = s.replace(ENUM_OLD, ENUM_NEW).replace(OLD, announce("SGIRE_W_UNMAP_WR", "SGIRE_W_UNMAP_RD", ""))
    T_OLD = "relative_addr >= CRIME_RE_TEX && relative_addr < CRIME_RE_TEX + 0xe0"
    if T_OLD not in s:
        die("TEXSHRINK TEXT NOT FOUND")
    s = s.replace(T_OLD, T_OLD.replace("+ 0xe0", "+ 0x60"))
elif variant == "mnolatch":
    # clause (d): keep the guard, NULL its repair -- announce but never set the
    # bit, so the decline floods instead of latching.
    s = s.replace(ENUM_OLD, ENUM_NEW)
    a = announce("SGIRE_W_UNMAP_WR", "SGIRE_W_UNMAP_RD", "")
    TAB4 = chr(9) * 4
    LF = chr(10)
    a = a.replace(TAB4 + "d->warned |= SGIRE_W_UNMAP_WR;" + LF, "")
    a = a.replace(TAB4 + "d->warned |= SGIRE_W_UNMAP_RD;" + LF, "")
    s = s.replace(OLD, a)
else:
    die("unknown variant " + variant)

open(out_path, "w").write(s)
sys.stderr.write("variant %s written\n" % variant)
