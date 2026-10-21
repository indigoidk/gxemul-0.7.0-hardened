#!/usr/bin/env python3
"""mk_legs568.py -- kill table 1 for #568 (vmedefaultkill): generate every leg's source by ONE exact find/replace.

usage (WSL python3):  python3 -I -B mk_legs568.py <dev_vme.fix568.c> <machine_mvme88k.head.c> <outdir>

Writes <outdir>/legs/src/<LEG>.dev_vme.c (NULL: <LEG>.machine_mvme88k.c), <outdir>/legs/<LEG>.diff (unified diff
against the input it was made from) and <outdir>/legs/MANIFEST.txt.  EVERY find text must occur EXACTLY ONCE in its
input; if any leg's does not, NOTHING is written and the exit status is 5 (a mutant whose edit did not land is a
false result).  Inputs are md5-checked; CR anywhere refuses.  LF in, LF out (newline="" both ways).

The legs are PRETABLE.out section 5 / PRETABLE_ADDENDUM_v2.out section 4, each translated here into an exact edit.
`pretable' quotes the addendum's prediction text for the leg verbatim.  M_LATCHCLRW_POST is NOT a PRETABLE leg: it
is the second translation of M_LATCHCLRW, because PRETABLE.out section 5 ("the write clears; later reads") and the
addendum ("each read-first register re-announces on its write") describe two different edits -- a write clearing the
latch AFTER the check (POST) or BEFORE it (M_LATCHCLRW as built here).  Both are built so neither description is
silently chosen over the other.
"""
import difflib
import hashlib
import io
import os
import sys

FIXMD5 = "4e3e7fc220062b429f7d9d6e140fec9e"
MACHMD5 = "c1edc233de21c6fbd7494f34c05be759"

#  Recurring anchors, each checked to occur exactly once in the fix by the generic count below.
LATCH_TEST = "\t\tif (!(d->warned_unimpl & (1ULL << (relative_addr >> 2)))) {\n"
LATCH_SET = "\t\t\td->warned_unimpl |= 1ULL << (relative_addr >> 2);\n"
ARM_END = "\t\t}\n\t\tbreak;\n\n\tdefault:"          # the decline arm's closing brace + break, then default:
DEF_RET = "\t\treturn 0;\n\t}\n"                       # default:'s refusal and the switch's closing brace
CLR_W = ("\t\tif (writeflag == MEM_WRITE)\n"
         "\t\t\td->warned_unimpl &= ~(1ULL << (relative_addr >> 2));\n")

# (LEG, target, one-line edit, PRETABLE addendum section 4 text, find, replace)
LEGS = [
    ("M_EXIT", "dev_vme.c", "default: `return 0;' -> `exit(1);' (the removed defect, verbatim, at the fixed site)",
     "p1 fault lo/hi/mid/wr, p1 census, p1 widths, p1 p2 edge, p3 interim, p2 int byte/half die",
     DEF_RET, "\t\texit(1);\n\t}\n"),
    ("M_DROPMCTL", "dev_vme.c", "drop the label `case VME2_MASTERCTL:' (0x28)",
     "p2 rd census, p2 wr census, p2 ann rd, p2 ann wr (+ their 2nd passes not completed)",
     "\tcase VME2_MASTERCTL:\n", ""),
    ("M_DROPMISC", "dev_vme.c", "drop the label `case VME2_MISC:' (0x8c, the last member)",
     "p2 rd census, p2 wr census, p2 ann rd/wr, p1 p2 edge",
     "\tcase VME2_MISC:\n", ""),
    ("M_ADD94", "dev_vme.c", "add the label `case 0x94:' to the decline arm (after `case VME2_MISC:')",
     "p1 census (987/988), p1 fault mid",
     "\tcase VME2_MISC:\n", "\tcase VME2_MISC:\n\tcase 0x94:\n"),
    ("M_LATCHONE", "dev_vme.c", "latch keyed by a constant: test AND set use `1ULL << 0' (one shared latch)",
     "p2 ann rd, p2 ann wr (1 line each)",
     LATCH_TEST + LATCH_SET,
     "\t\tif (!(d->warned_unimpl & (1ULL << 0))) {\n\t\t\td->warned_unimpl |= 1ULL << 0;\n"),
    ("M_LATCHNOSET", "dev_vme.c", "delete the latch set `d->warned_unimpl |= ...;' (the latch is never set)",
     "p2 ann rd, p2 ann wr (52 lines), p2 ann rd 2, p2 ann wr 2",
     LATCH_SET, ""),
    ("M_LATCHRDSET", "dev_vme.c", "the latch set guarded by `if (writeflag == MEM_READ)' (set only on reads)",
     "p2 ann wr (each write-first register re-announces on its read)",
     LATCH_SET, "\t\t\tif (writeflag == MEM_READ)\n\t" + LATCH_SET),
    ("M_LATCHCLRW", "dev_vme.c",
     "a write CLEARS its latch bit BEFORE the check (`if (writeflag == MEM_WRITE) d->warned_unimpl &= ~bit;')",
     "p2 ann rd (each read-first register re-announces on its write)",
     LATCH_TEST, CLR_W + LATCH_TEST),
    ("M_LATCHCLRW_POST", "dev_vme.c",
     "[translation variant, not a PRETABLE leg] a write clears its latch bit AFTER the check/announce",
     "p2 ann rd (each read-first register re-announces on its write)",
     ARM_END, "\t\t}\n" + CLR_W + "\t\tbreak;\n\n\tdefault:"),
    ("M_WDEBUG", "dev_vme.c", "the write-branch announce `fatal(' -> `debug('",
     "p2 ann wr, p2 nw wr",
     "\t\t\t\tfatal(\"[ vme: unimplemented write to register \"\n",
     "\t\t\t\tdebug(\"[ vme: unimplemented write to register \"\n"),
    ("M_RDEBUG", "dev_vme.c", "the read-branch announce `fatal(' -> `debug('",
     "p2 ann rd, p2 nw rd",
     "\t\t\t\tfatal(\"[ vme: unimplemented read from register \"\n",
     "\t\t\t\tdebug(\"[ vme: unimplemented read from register \"\n"),
    ("M_ANNLEN4", "dev_vme.c", "the announce (and its latch) only for 4-byte accesses: `if (len == 4 && !(...))'",
     "p2 nw rd, p2 nw wr",
     LATCH_TEST, "\t\tif (len == 4 && !(d->warned_unimpl & (1ULL << (relative_addr >> 2)))) {\n"),
    ("M_TRUNC", "dev_vme.c", "the write announce prints a 32-bit value: `(unsigned long long) (uint32_t) idata'",
     "p2 nw wr",
     "(unsigned long long) idata);", "(unsigned long long) (uint32_t) idata);"),
    ("M_WRFAULT", "dev_vme.c", "the decline arm returns 0 for writes: `if (writeflag == MEM_WRITE) return 0;' before its break",
     "p2 wr census, p2 st widths, p2 ann wr, p2 nw wr",
     ARM_END, "\t\t}\n\t\tif (writeflag == MEM_WRITE)\n\t\t\treturn 0;\n\t\tbreak;\n\n\tdefault:"),
    ("M_LENFAULT", "dev_vme.c", "the decline conditioned on len: `if (len != 4) return 0;' before the arm's break",
     "p2 ld widths, p2 st widths, p2 nw rd, p2 nw wr",
     ARM_END, "\t\t}\n\t\tif (len != 4)\n\t\t\treturn 0;\n\t\tbreak;\n\n\tdefault:"),
    ("M_STORE", "dev_vme.c", "the decline arm STORES writes: `if (writeflag == MEM_WRITE) d->reg[w] = idata;' before its break",
     "p2 wr census",
     ARM_END, "\t\t}\n\t\tif (writeflag == MEM_WRITE)\n"
              "\t\t\td->reg[relative_addr / sizeof(uint32_t)] = idata;\n\t\tbreak;\n\n\tdefault:"),
    ("M_ODATA0", "dev_vme.c", "`odata = 0;' at the top of the decline arm (reads forced to 0)",
     "predicted SURVIVOR (equivalent today)",
     LATCH_TEST, "\t\todata = 0;\n" + LATCH_TEST),
    ("M_SERVED0", "dev_vme.c", "the read announce prints a literal 0: `(unsigned) odata' -> `(unsigned) 0'",
     "predicted SURVIVOR (equivalent today -- section 2 (i))",
     "(unsigned) odata);", "(unsigned) 0);"),
    ("M_FLTBREAK", "dev_vme.c", "default: `return 0;' -> `break;' (the refusal served instead)",
     "p1 fault lo/hi/mid/wr, p1 census, p1 widths, p1 p2 edge, p3 interim, p2 int byte/half",
     DEF_RET, "\t\tbreak;\n\t}\n"),
    ("M_FLTLEN", "dev_vme.c", "default: `if (len != 4) break;' before `return 0;' (refusal narrowed to word accesses)",
     "p1 widths, p3 interim, p2 int byte, p2 int half",
     DEF_RET, "\t\tif (len != 4)\n\t\t\tbreak;\n" + DEF_RET),
    ("M_FLTWR", "dev_vme.c", "default: `if (writeflag == MEM_WRITE) break;' before `return 0;' (writes no longer refused)",
     "p1 fault wr, p1 widths",
     DEF_RET, "\t\tif (writeflag == MEM_WRITE)\n\t\t\tbreak;\n" + DEF_RET),
    ("M_NOONCE", "dev_vme.c", "`(once)' dropped from the read announce's tail",
     "p2 ann rd (tail literal)",
     "-- served 0x%x.  (once) ]", "-- served 0x%x.  ]"),
    ("M_DROPTCTL", "dev_vme.c", "drop the cased label `case VME2_TCTL:' (0x60)",
     "cased census, tctl rt",
     "\tcase VME2_TCTL:\n", ""),
    ("M_CAPNARROW", "dev_vme.c", "narrow the latch: `uint64_t warned_unimpl' -> `uint32_t' (the typedef must refuse the build)",
     "BUILD FAILS (the typedef) -- killed by construction",
     "\tuint64_t\twarned_unimpl;\n", "\tuint32_t\twarned_unimpl;\n"),
    ("NULL", "machine_mvme88k.c", "[null medium, not a dev_vme.c leg] the vme device_add removed from machine_mvme88k.c "
     "(dev_vme.c = fix568)",
     "5/34, CONTROL=FAIL (measured)",
     "\t\tsnprintf(tmpstr, sizeof(tmpstr), \"vme addr=0x%x\", VME2_BASE);\n\t\tdevice_add(machine, tmpstr);\n",
     "\t\tsnprintf(tmpstr, sizeof(tmpstr), \"vme addr=0x%x\", VME2_BASE);\n"),
]


def rd(p):
    with io.open(p, "r", encoding="latin-1", newline="") as f:
        return f.read()


def wr(p, s):
    with io.open(p, "w", encoding="latin-1", newline="") as f:
        f.write(s)


def md5s(s):
    return hashlib.md5(s.encode("latin-1")).hexdigest()


def main():
    if len(sys.argv) != 4:
        sys.stderr.write("usage: mk_legs568.py <dev_vme.fix568.c> <machine_mvme88k.head.c> <outdir>\n")
        return 2
    fix, mach, out = rd(sys.argv[1]), rd(sys.argv[2]), sys.argv[3]
    bad = []
    if md5s(fix) != FIXMD5:
        bad.append("fix md5 %s != %s" % (md5s(fix), FIXMD5))
    if md5s(mach) != MACHMD5:
        bad.append("machine md5 %s != %s" % (md5s(mach), MACHMD5))
    if "\r" in fix or "\r" in mach:
        bad.append("CR in an input")
    names = [l[0] for l in LEGS]
    if len(set(names)) != len(names):
        bad.append("duplicate leg name")
    made = []
    for name, target, what, pre, find, repl in LEGS:
        src = fix if target == "dev_vme.c" else mach
        n = src.count(find)
        if n != 1:
            bad.append("%s: find text occurs %d times (want exactly 1): %r" % (name, n, find))
            continue
        res = src.replace(find, repl, 1)
        if res == src:
            bad.append("%s: edit is a no-op" % name)
            continue
        if "\r" in res:
            bad.append("%s: CR in output" % name)
            continue
        made.append((name, target, what, pre, src, res))
    if bad:
        for b in bad:
            sys.stderr.write("REFUSED: %s\n" % b)
        sys.stderr.write("NOTHING WRITTEN\n")
        return 5
    os.makedirs(os.path.join(out, "legs", "src"), exist_ok=True)
    man = ["# mk_legs568.py manifest: LEG target md5 +lines -lines | edit | PRETABLE addendum section 4 prediction",
           "# input fix %s md5 %s ; machine %s md5 %s" % (sys.argv[1], FIXMD5, sys.argv[2], MACHMD5)]
    for name, target, what, pre, src, res in made:
        fn = "%s.%s" % (name, target)
        wr(os.path.join(out, "legs", "src", fn), res)
        base = "dev_vme.fix568.c" if target == "dev_vme.c" else "machine_mvme88k.head.c (1a59a47e)"
        dl = list(difflib.unified_diff(src.splitlines(True), res.splitlines(True),
                                       fromfile=base, tofile="%s/%s" % (name, target), n=3))
        wr(os.path.join(out, "legs", "%s.diff" % name), "".join(dl))
        plus = sum(1 for l in dl if l.startswith("+") and not l.startswith("+++"))
        minus = sum(1 for l in dl if l.startswith("-") and not l.startswith("---"))
        man.append("%-17s %-18s %s +%d -%d | %s | %s" % (name, target, md5s(res), plus, minus, what, pre))
    wr(os.path.join(out, "legs", "MANIFEST.txt"), "\n".join(man) + "\n")
    print("\n".join(man))
    print("MK_LEGS568_DONE %d legs" % len(made))
    return 0


if __name__ == "__main__":
    sys.exit(main())
