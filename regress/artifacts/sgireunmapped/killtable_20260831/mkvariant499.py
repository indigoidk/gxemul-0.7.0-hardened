#!/usr/bin/env python3
"""mkvariant499.py <variant> <pristine_src> <out_src>

Round #499 variant generator.  Derived from the #498-era
opus_witness_20260830/mkvariant.py, with THREE changes, each recorded:

  1. THE ENUM BIT MOVED.  The original inserted SGIRE_W_UNMAP_WR = 1 << 6.
     HEAD (cb28a6f, #498) ADDED `SGIRE_W_DE_LEN = 1 << 6' to the same enum
     and the same `d->warned' word, which DEVICE_ACCESS(sgi_de) shares
     (it casts the same `struct sgi_re_data *').  Re-running the original
     generator against today's HEAD therefore emits a DUPLICATE enumerator
     value -- legal C, silent, and a live latch collision.  This generator
     uses 1 << 7 / 1 << 8 and HARD-FAILS on any duplicate.
     Variant `fix6' reproduces the naive form deliberately, to measure
     whether the shipped detector can see the collision at all.

  2. Four new mutants: m1_tlba, m2_tlbb, m3_tlbc (far-bound shrinks) and
     m4_bitcollide (SGIRE_W_TLBA_LEN 1<<0 -> 1<<1).

  3. Every find-text is asserted UNIQUE before replacement (presence pin +
     uniqueness pin).  M2's `< CRIME_RE_TLB_C' appears in two arms; the
     anchor used is the whole TLB_B conditional, which is unique.

Backslash discipline: every backslash that must survive into the C file is
chr(92) (Bash -> heredoc -> Python eats one level in both directions)."""
import re, sys

BS = chr(92)
NL = BS + "n"
Q  = '"'

variant, src_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src_path).read()

def die(msg):
    sys.stderr.write("MKVARIANT FAIL: " + msg + "\n"); sys.exit(9)

def sub1(text, old, new, tag):
    """replace exactly one occurrence; absent or non-unique is a HARD FAIL."""
    n = text.count(old)
    if n != 1:
        die("%s: anchor count %d (want 1) for %r" % (tag, n, old[:70]))
    return text.replace(old, new)

# ---- EXTRACT the committed catch-all rather than transcribing it -----------
A = "\t} else {\n\t\tif (writeflag == MEM_WRITE)\n\t\t\tfatal(" + Q + "[ sgi_re: unimplemented write to "
if A not in s:
    die("ANCHOR A NOT FOUND")
start = s.index(A)
endmark = "\t\texit(1);\n\t}\n"
end = s.index(endmark, start)
OLD = s[start:end + len(endmark)]
if s.count(OLD) != 1:
    die("CATCH-ALL BLOCK IS NOT UNIQUE (%d matches)" % s.count(OLD))

ENUM_OLD = "\tSGIRE_W_LINB_LEN  = 1 << 5,\n"
if s.count(ENUM_OLD) != 1:
    die("ENUM TEXT NOT FOUND/UNIQUE")

def enum_new(wr_bit, rd_bit):
    return (ENUM_OLD
            + "\tSGIRE_W_UNMAP_WR  = 1 << %d,\n" % wr_bit
            + "\tSGIRE_W_UNMAP_RD  = 1 << %d,\n" % rd_bit)

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

def apply_fix(text, wr_bit=7, rd_bit=8):
    text = sub1(text, ENUM_OLD, enum_new(wr_bit, rd_bit), "enum")
    text = sub1(text, OLD, announce("SGIRE_W_UNMAP_WR", "SGIRE_W_UNMAP_RD", ""), "catchall")
    return text

# ---- the three window conditionals, each asserted unique ------------------
C_TLBA = "relative_addr >= CRIME_RE_TLB_A && relative_addr < CRIME_RE_TLB_B"
C_TLBB = "relative_addr >= CRIME_RE_TLB_B && relative_addr < CRIME_RE_TLB_C"
C_TLBC = "relative_addr >= CRIME_RE_TLB_C && relative_addr < CRIME_RE_TLB_C + 0x200"
E_TLBA = "\tSGIRE_W_TLBA_LEN  = 1 << 0,\n"

if variant == "base":
    pass
elif variant == "fix":
    s = apply_fix(s)
elif variant == "fix6":
    # the naive port of the #498-era generator: UNMAP_WR collides with
    # SGIRE_W_DE_LEN (both 1 << 6).  Duplicate check is bypassed ON PURPOSE.
    s = apply_fix(s, 6, 7)
elif variant == "m1_tlba":
    s = apply_fix(s)
    s = sub1(s, C_TLBA, C_TLBA.replace("< CRIME_RE_TLB_B", "< CRIME_RE_TLB_B - 0x100"), "m1")
elif variant == "m2_tlbb":
    s = apply_fix(s)
    s = sub1(s, C_TLBB, C_TLBB.replace("< CRIME_RE_TLB_C", "< CRIME_RE_TLB_C - 0x100"), "m2")
elif variant == "m3_tlbc":
    s = apply_fix(s)
    s = sub1(s, C_TLBC, C_TLBC.replace("+ 0x200", "+ 0x100"), "m3")
elif variant == "m5_lina_near":
    # NEAR-bound growth, the mirror of M1-M3.  [0x1700,0x1740) is pushed out
    # of LIN_A and falls to the catch-all; the accept row at the TOP slot
    # (0x1778) is still inside the window and cannot see it.
    s = apply_fix(s)
    C_LINA = "relative_addr >= CRIME_RE_LINEAR_A && relative_addr < CRIME_RE_LINEAR_A + 0x80"
    s = sub1(s, C_LINA,
             C_LINA.replace(">= CRIME_RE_LINEAR_A", ">= CRIME_RE_LINEAR_A + 0x40"), "m5")
elif variant == "m4_bitcollide":
    s = apply_fix(s)
    s = sub1(s, E_TLBA, "\tSGIRE_W_TLBA_LEN  = 1 << 1,\n", "m4")
else:
    die("unknown variant " + variant)

# ---- duplicate-enumerator check (skipped for the deliberate fix6) ---------
if variant != "fix6":
    body = s[s.index("enum {"):s.index("};", s.index("enum {"))]
    vals = re.findall(r"(SGIRE_W_[A-Z_]+)\s*=\s*1 << (\d+)", body)
    seen = {}
    for nm, sh in vals:
        if variant == "m4_bitcollide" and nm == "SGIRE_W_TLBA_LEN":
            continue          # the mutant IS the collision
        if sh in seen:
            die("DUPLICATE ENUMERATOR VALUE 1<<%s: %s and %s" % (sh, seen[sh], nm))
        seen[sh] = nm

open(out_path, "w").write(s)
sys.stderr.write("variant %s written (%d bytes)\n" % (variant, len(s)))
