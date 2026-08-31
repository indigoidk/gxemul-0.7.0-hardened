#!/usr/bin/env python3
"""mk500.py <variant> <pristine_src> <out_src>

Variants for the #499 re-pin measurement:

  base    pristine HEAD, byte-for-byte (a copy, so the driver's cmp is meaningful)
  fix     #499's fix WITH THE CORRECTED ENUM PLACEMENT -- both new enumerators
          AFTER SGIRE_W_DE_LEN, so the enum ends at the highest bit and a
          maintainer scanning for the next free bit does not land on 1 << 7.
  mexit0  fix + `exit(0);' at the end of the catch-all else block.  This is the
          mutant the round owes: it reinstates the death with a status that an
          exit-status oracle cannot distinguish from `declined, then quit'.

Every anchor is asserted UNIQUE before replacement -- absent or non-unique is a
hard failure, never a silent no-op.  Backslashes that must survive into the C
file are chr(92): the Bash -> heredoc -> Python path eats one level.
"""
import sys

BS = chr(92)
NL = BS + "n"
Q = '"'

variant, src_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src_path).read()


def die(msg):
    sys.stderr.write("MK500 FAIL: " + msg + "\n")
    sys.exit(9)


def sub1(text, old, new, tag):
    n = text.count(old)
    if n != 1:
        die("%s: anchor count %d (want 1) for %r" % (tag, n, old[:80]))
    return text.replace(old, new)


# ---- EXTRACT the committed catch-all rather than transcribing it ------------
A = ("\t} else {\n\t\tif (writeflag == MEM_WRITE)\n\t\t\tfatal(" + Q
     + "[ sgi_re: unimplemented write to ")
if A not in s:
    die("ANCHOR A (catch-all head) NOT FOUND")
start = s.index(A)
endmark = "\t\texit(1);\n\t}\n"
end = s.index(endmark, start)
OLD_CATCHALL = s[start:end + len(endmark)]
if s.count(OLD_CATCHALL) != 1:
    die("CATCH-ALL BLOCK NOT UNIQUE (%d)" % s.count(OLD_CATCHALL))

# ---- the enum anchor: AFTER SGIRE_W_DE_LEN, not after LINB ------------------
ENUM_ANCHOR = "\tSGIRE_W_DE_LEN    = 1 << 6,\n};\n"
if s.count(ENUM_ANCHOR) != 1:
    die("ENUM ANCHOR NOT FOUND/UNIQUE (%d)" % s.count(ENUM_ANCHOR))

ENUM_NEW = (
    "\tSGIRE_W_DE_LEN    = 1 << 6,\n"
    "\n"
    "\t/*  #499: the unmatched-address catch-all.  TWO bits, one per DIRECTION:\n"
    "\t    a driver probing an unmapped window commonly reads and writes it in\n"
    "\t    one pass, and one bit would announce the first and silence the other.\n"
    "\n"
    "\t    PLACED AFTER SGIRE_W_DE_LEN ON PURPOSE.  An earlier draft inserted\n"
    "\t    these two after SGIRE_W_LINB_LEN (1 << 5), which left the enum ending\n"
    "\t    at 1 << 6 -- so a maintainer scanning to the LAST enumerator for the\n"
    "\t    next free bit would take 1 << 7, which is already used.  A duplicate\n"
    "\t    enumerator is legal C and silent, and both devices share this word.  */\n"
    "\tSGIRE_W_UNMAP_WR  = 1 << 7,\n"
    "\tSGIRE_W_UNMAP_RD  = 1 << 8,\n"
    "};\n")

NEW_CATCHALL = (
    "\t} else {\n"
    "\t\tif (writeflag == MEM_WRITE) {\n"
    "\t\t\tif (!(d->warned & SGIRE_W_UNMAP_WR)) {\n"
    "\t\t\t\td->warned |= SGIRE_W_UNMAP_WR;\n"
    "\t\t\t\tfatal(" + Q + "[ sgi_re: unimplemented write to " + Q + "\n"
    "\t\t\t\t    " + Q + "address 0x%llx, data=0x%016llx -- " + Q + "\n"
    "\t\t\t\t    " + Q + "declined.  (once) ]" + NL + Q + ",\n"
    "\t\t\t\t    (long long)relative_addr, (long long)idata);\n"
    "\t\t\t}\n"
    "\t\t} else {\n"
    "\t\t\tif (!(d->warned & SGIRE_W_UNMAP_RD)) {\n"
    "\t\t\t\td->warned |= SGIRE_W_UNMAP_RD;\n"
    "\t\t\t\tfatal(" + Q + "[ sgi_re: unimplemented read from address" + Q + "\n"
    "\t\t\t\t    " + Q + " 0x%llx -- declined.  (once) ]" + NL + Q + ",\n"
    "\t\t\t\t    (long long)relative_addr);\n"
    "\t\t\t}\n"
    "\t\t}\n"
    "\t}\n")

if variant == "base":
    out = s

elif variant in ("fix", "mexit0", "mret0", "mrdexit0"):
    out = sub1(s, ENUM_ANCHOR, ENUM_NEW, "enum")
    out = sub1(out, OLD_CATCHALL, NEW_CATCHALL, "catchall")
    TAIL = "\t\t\t}\n\t\t}\n\t}\n"
    if variant == "mexit0":
        #  Reinstate the death with status 0, at the end of the else block.
        out = sub1(out, TAIL, "\t\t\t}\n\t\t}\n\t\texit(0);\n\t}\n", "exit0")
    elif variant == "mret0":
        #  Decline by RETURNING 0 instead of falling to the common tail.
        #  memory_rw coerces 0 to -1 and raises EXCEPTION_DBE, so the refusal
        #  becomes a guest bus error and a declined READ never lands a value.
        out = sub1(out, TAIL, "\t\t\t}\n\t\t}\n\t\treturn 0;\n\t}\n", "ret0")
    elif variant == "mrdexit0":
        #  exit(0) in the READ branch ONLY.  The write direction is untouched,
        #  so a write-only oracle stays GREEN while every read kills the host.
        RD = "\t\t\t\t    (long long)relative_addr);\n\t\t\t}\n\t\t}\n\t}\n"
        out = sub1(out, RD, "\t\t\t\t    (long long)relative_addr);\n\t\t\t}\n\t\t\texit(0);\n\t\t}\n\t}\n", "rdexit0")

else:
    die("unknown variant " + variant)

#  Duplicate-enumerator guard: no two enumerators of this enum may share a value.
if variant != "base":
    import re
    blk = out[out.index("enum {"):out.index("};", out.index("enum {"))]
    vals = re.findall(r"(SGIRE_W_[A-Z_]+)\s*=\s*1 << (\d+)", blk)
    seen = {}
    for name, bit in vals:
        if bit in seen:
            die("DUPLICATE ENUMERATOR BIT %s: %s and %s" % (bit, seen[bit], name))
        seen[bit] = name
    #  and the last enumerator must be the highest bit, which is the whole
    #  point of the placement correction.
    if vals[-1][1] != max(int(b) for _n, b in vals).__str__():
        die("LAST ENUMERATOR IS NOT THE HIGHEST BIT (%s = 1 << %s)" % vals[-1])
    sys.stderr.write("  enum ok: %d enumerators, last = %s = 1 << %s\n"
                     % (len(vals), vals[-1][0], vals[-1][1]))

open(out_path, "w").write(out)
print("MK500 %s -> %s (%d bytes)" % (variant, out_path, len(out)))
