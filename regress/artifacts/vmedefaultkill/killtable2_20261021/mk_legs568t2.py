#!/usr/bin/env python3
"""mk_legs568t2.py -- #568 kill table 2: every table-1 / table-1b leg REGENERATED on fix568b, plus the seven new legs,
each by ONE exact find/replace.

usage (WSL python3):  python3 -I -B mk_legs568t2.py <dev_vme.fix568b.c> <machine_mvme88k.head.c> <outdir>

Writes <outdir>/legs/src/<LEG>.dev_vme.c (NULL: <LEG>.machine_mvme88k.c), <outdir>/legs/<LEG>.diff and
<outdir>/legs/MANIFEST.txt.  EVERY find text must occur EXACTLY ONCE in its input, or NOTHING is written (exit 5).
Inputs md5-checked; CR anywhere refuses; LF in, LF out.

The table-1/1b legs keep their INTENT and their table-1 edit; only the find-strings on the read announce's format and
cast lines change, because fix568b rewrote those two lines (D1): M_NOONCE and M_SERVED0.  M_RDEBUG anchors on the
read announce's FIRST line, which fix568b did not change.  Every other find text is byte-identical to table 1's.
"""
import difflib
import hashlib
import io
import os
import sys

FIXBMD5 = "beb120eae1be112b682bd528f103191c"
MACHMD5 = "c1edc233de21c6fbd7494f34c05be759"

LATCH_TEST = "\t\tif (!(d->warned_unimpl & (1ULL << (relative_addr >> 2)))) {\n"
LATCH_SET = "\t\t\td->warned_unimpl |= 1ULL << (relative_addr >> 2);\n"
ARM_END = "\t\t}\n\t\tbreak;\n\n\tdefault:"
DEF_RET = "\t\treturn 0;\n\t}\n"
CLR_W = ("\t\tif (writeflag == MEM_WRITE)\n"
         "\t\t\td->warned_unimpl &= ~(1ULL << (relative_addr >> 2));\n")

# (LEG, origin, target, one-line edit, find, replace)
LEGS = [
    ("M_EXIT", "t1", "dev_vme.c", "default: `return 0;' -> `exit(1);'", DEF_RET, "\t\texit(1);\n\t}\n"),
    ("M_DROPMCTL", "t1", "dev_vme.c", "drop `case VME2_MASTERCTL:' (0x28)", "\tcase VME2_MASTERCTL:\n", ""),
    ("M_DROPMISC", "t1", "dev_vme.c", "drop `case VME2_MISC:' (0x8c)", "\tcase VME2_MISC:\n", ""),
    ("M_ADD94", "t1", "dev_vme.c", "add `case 0x94:' after `case VME2_MISC:'",
     "\tcase VME2_MISC:\n", "\tcase VME2_MISC:\n\tcase 0x94:\n"),
    ("M_LATCHONE", "t1", "dev_vme.c", "latch keyed by a constant: test AND set use `1ULL << 0'",
     LATCH_TEST + LATCH_SET,
     "\t\tif (!(d->warned_unimpl & (1ULL << 0))) {\n\t\t\td->warned_unimpl |= 1ULL << 0;\n"),
    ("M_LATCHNOSET", "t1", "dev_vme.c", "delete the latch set", LATCH_SET, ""),
    ("M_LATCHRDSET", "t1", "dev_vme.c", "latch set only on reads", LATCH_SET,
     "\t\t\tif (writeflag == MEM_READ)\n\t" + LATCH_SET),
    ("M_LATCHCLRW", "t1", "dev_vme.c", "a write clears its latch bit BEFORE the check", LATCH_TEST, CLR_W + LATCH_TEST),
    ("M_LATCHCLRW_POST", "t1", "dev_vme.c", "a write clears its latch bit AFTER the check/announce",
     ARM_END, "\t\t}\n" + CLR_W + "\t\tbreak;\n\n\tdefault:"),
    ("M_WDEBUG", "t1", "dev_vme.c", "write announce `fatal(' -> `debug('",
     "\t\t\t\tfatal(\"[ vme: unimplemented write to register \"\n",
     "\t\t\t\tdebug(\"[ vme: unimplemented write to register \"\n"),
    ("M_RDEBUG", "t1", "dev_vme.c", "read announce `fatal(' -> `debug(' (anchor: its unchanged first line)",
     "\t\t\t\tfatal(\"[ vme: unimplemented read from register \"\n",
     "\t\t\t\tdebug(\"[ vme: unimplemented read from register \"\n"),
    ("M_ANNLEN4", "t1", "dev_vme.c", "announce and latch only for len 4", LATCH_TEST,
     "\t\tif (len == 4 && !(d->warned_unimpl & (1ULL << (relative_addr >> 2)))) {\n"),
    ("M_TRUNC", "t1", "dev_vme.c", "write announce prints `(unsigned long long) (uint32_t) idata'",
     "(unsigned long long) idata);", "(unsigned long long) (uint32_t) idata);"),
    ("M_WRFAULT", "t1", "dev_vme.c", "decline arm `if (writeflag == MEM_WRITE) return 0;' before its break",
     ARM_END, "\t\t}\n\t\tif (writeflag == MEM_WRITE)\n\t\t\treturn 0;\n\t\tbreak;\n\n\tdefault:"),
    ("M_LENFAULT", "t1", "dev_vme.c", "decline arm `if (len != 4) return 0;' before its break",
     ARM_END, "\t\t}\n\t\tif (len != 4)\n\t\t\treturn 0;\n\t\tbreak;\n\n\tdefault:"),
    ("M_STORE", "t1", "dev_vme.c", "decline arm stores writes into d->reg[w]",
     ARM_END, "\t\t}\n\t\tif (writeflag == MEM_WRITE)\n"
              "\t\t\td->reg[relative_addr / sizeof(uint32_t)] = idata;\n\t\tbreak;\n\n\tdefault:"),
    ("M_ODATA0", "t1", "dev_vme.c", "`odata = 0;' at the top of the decline arm", LATCH_TEST, "\t\todata = 0;\n" + LATCH_TEST),
    ("M_SERVED0", "t1*", "dev_vme.c", "read announce prints a literal 0 (fix568b: `(unsigned long long) odata' -> `... 0')",
     "(unsigned long long) odata);", "(unsigned long long) 0);"),
    ("M_FLTBREAK", "t1", "dev_vme.c", "default: `return 0;' -> `break;'", DEF_RET, "\t\tbreak;\n\t}\n"),
    ("M_FLTLEN", "t1", "dev_vme.c", "default: `if (len != 4) break;' before `return 0;'",
     DEF_RET, "\t\tif (len != 4)\n\t\t\tbreak;\n" + DEF_RET),
    ("M_FLTWR", "t1", "dev_vme.c", "default: `if (writeflag == MEM_WRITE) break;' before `return 0;'",
     DEF_RET, "\t\tif (writeflag == MEM_WRITE)\n\t\t\tbreak;\n" + DEF_RET),
    ("M_NOONCE", "t1*", "dev_vme.c", "`(once)' dropped from the read announce (fix568b: the `0x%llx' tail)",
     "-- served 0x%llx.  (once) ]", "-- served 0x%llx.  ]"),
    ("M_DROPTCTL", "t1", "dev_vme.c", "drop `case VME2_TCTL:' (0x60)", "\tcase VME2_TCTL:\n", ""),
    ("M_CAPNARROW", "t1", "dev_vme.c", "narrow the latch field to uint32_t (the typedef must refuse the build)",
     "\tuint64_t\twarned_unimpl;\n", "\tuint32_t\twarned_unimpl;\n"),
    ("M_DROPIRQEN", "t1b", "dev_vme.c", "drop `case VME2_IRQEN:' (0x6c)", "\tcase VME2_IRQEN:\n", ""),
    ("M_T1CMPWRDROP", "t1b", "dev_vme.c", "T1CMP arm `MEM_WRITE' -> `MEM_READ' (the store dropped)",
     "\tcase VME2_T1CMP:\n\t\tif (writeflag == MEM_WRITE)\n", "\tcase VME2_T1CMP:\n\t\tif (writeflag == MEM_READ)\n"),
    ("M_ADD90", "t1b", "dev_vme.c", "add `case 0x90:' before `case VME2_SADDR2:'",
     "\tcase VME2_SADDR2:\n", "\tcase 0x90:\n\tcase VME2_SADDR2:\n"),
    # ---- new in table 2 (REV3_SPEC section 4, amendments in section 6)
    ("M_IDATA", "new", "dev_vme.c", "announce direction test `if (writeflag == MEM_WRITE)' -> `if (idata)' (pop-2 arm only)",
     LATCH_SET + "\t\t\tif (writeflag == MEM_WRITE)\n", LATCH_SET + "\t\t\tif (idata)\n"),
    ("M_LATCHLEN4", "new", "dev_vme.c", "`if (len == 4)' before the latch SET (the check untouched)",
     LATCH_SET, "\t\t\tif (len == 4)\n\t" + LATCH_SET),
    ("M_DFATAL", "new", "dev_vme.c", "default:'s READ `debug(' -> `fatal('",
     "\t\t\tdebug(\"[ vme: unimplemented READ from offset 0x%x ]\"\n",
     "\t\t\tfatal(\"[ vme: unimplemented READ from offset 0x%x ]\"\n"),
    ("M_DFATALW", "new", "dev_vme.c", "default:'s WRITE `debug(' -> `fatal('",
     "\t\t\tdebug(\"[ vme: unimplemented WRITE to offset 0x%x: \"\n",
     "\t\t\tfatal(\"[ vme: unimplemented WRITE to offset 0x%x: \"\n"),
    ("M_LANE0H", "new", "dev_vme.c", "default: `if (len == 2 && (relative_addr & 3) == 0) break;' before `return 0;'",
     DEF_RET, "\t\tif (len == 2 && (relative_addr & 3) == 0)\n\t\t\tbreak;\n" + DEF_RET),
    ("M_LANE0B", "new", "dev_vme.c", "default: `if (len == 1 && (relative_addr & 3) == 0) break;' before `return 0;'",
     DEF_RET, "\t\tif (len == 1 && (relative_addr & 3) == 0)\n\t\t\tbreak;\n" + DEF_RET),
    ("M_ONENARROW", "new", "dev_vme.c", "both arm literals `1ULL' -> `1u' (test and set; UB at MISC's shift of 35)",
     LATCH_TEST + LATCH_SET,
     "\t\tif (!(d->warned_unimpl & (1u << (relative_addr >> 2)))) {\n"
     "\t\t\td->warned_unimpl |= 1u << (relative_addr >> 2);\n"),
    # ---- the null medium (a reference, not a dev_vme.c leg)
    ("NULL", "ref", "machine_mvme88k.c", "the vme device_add removed from machine_mvme88k.c (dev_vme.c = fix568b)",
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
        sys.stderr.write("usage: mk_legs568t2.py <dev_vme.fix568b.c> <machine_mvme88k.head.c> <outdir>\n")
        return 2
    fix, mach, out = rd(sys.argv[1]), rd(sys.argv[2]), sys.argv[3]
    bad, made = [], []
    if md5s(fix) != FIXBMD5:
        bad.append("fix568b md5 %s != %s" % (md5s(fix), FIXBMD5))
    if md5s(mach) != MACHMD5:
        bad.append("machine md5 %s != %s" % (md5s(mach), MACHMD5))
    if "\r" in fix or "\r" in mach:
        bad.append("CR in an input")
    names = [l[0] for l in LEGS]
    if len(set(names)) != len(names):
        bad.append("duplicate leg name")
    for name, origin, target, what, find, repl in LEGS:
        src = fix if target == "dev_vme.c" else mach
        n = src.count(find)
        if n != 1:
            bad.append("%s: find text occurs %d times (want exactly 1): %r" % (name, n, find))
            continue
        res = src.replace(find, repl, 1)
        if res == src or "\r" in res:
            bad.append("%s: no-op or CR" % name)
            continue
        made.append((name, origin, target, what, src, res))
    if bad:
        for b in bad:
            sys.stderr.write("REFUSED: %s\n" % b)
        sys.stderr.write("NOTHING WRITTEN\n")
        return 5
    os.makedirs(os.path.join(out, "legs", "src"), exist_ok=True)
    man = ["# mk_legs568t2.py manifest: LEG origin target md5 +lines -lines | edit",
           "# origin: t1 = table-1 leg, find text unchanged; t1* = table-1 leg, find text re-anchored on fix568b's D1 lines;",
           "#         t1b = table-1b leg; new = new in table 2; ref = the null medium",
           "# inputs: fix568b md5 %s ; machine md5 %s" % (FIXBMD5, MACHMD5)]
    for name, origin, target, what, src, res in made:
        wr(os.path.join(out, "legs", "src", "%s.%s" % (name, target)), res)
        base = "dev_vme.fix568b.c" if target == "dev_vme.c" else "machine_mvme88k.head.c (1a59a47e)"
        dl = list(difflib.unified_diff(src.splitlines(True), res.splitlines(True), fromfile=base,
                                       tofile="%s/%s" % (name, target), n=3))
        wr(os.path.join(out, "legs", "%s.diff" % name), "".join(dl))
        plus = sum(1 for l in dl if l.startswith("+") and not l.startswith("+++"))
        minus = sum(1 for l in dl if l.startswith("-") and not l.startswith("---"))
        man.append("%-17s %-4s %-18s %s +%d -%d | %s" % (name, origin, target, md5s(res), plus, minus, what))
    wr(os.path.join(out, "legs", "MANIFEST.txt"), "\n".join(man) + "\n")
    print("\n".join(man))
    print("MK_LEGS568T2_DONE %d legs" % len(made))
    return 0


if __name__ == "__main__":
    sys.exit(main())
