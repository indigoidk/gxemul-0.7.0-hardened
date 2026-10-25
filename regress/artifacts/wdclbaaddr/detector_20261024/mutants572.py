#  #572 wdclbaaddr -- kill-table mutant applicator.  CLASS_TOOL.
#
#  Each mutant is a textual edit to the FIXED src/devices/dev_wdc.c (clause-(b)
#  reinstatements of the removed defect, clause-(d) conditioned-arm variants, and the
#  clause-(f) ANCHOR translations).  Every old text must occur EXACTLY ONCE at the
#  moment it is applied, so a find-text that no longer matches is a loud failure, and a
#  mutant additionally pins the presence of the text it edits.
#
#  Usage:  python3 mutants572.py --list
#          python3 mutants572.py --check <path-to-dev_wdc.c>
#          python3 mutants572.py <name> <path-to-dev_wdc.c>   (edits in place)
#
#  The READ-site and WRITE-site LBA arms are textually identical, so each is captured
#  with its DISTINCT following statement (`while (count` for read, `d->write_in_progress`
#  for write) to disambiguate.
#
#  TABLE 1 ran the first 18 entries (V1 .. V18 and V20); TABLE 2 (V5r, V6r, V8w, V11w,
#  V9r8, V10r, V10w, T_m1, T_p1) was ADDED AFTER TABLE 1 RAN, to back the probe header's CATCHES and
#  ANCHOR text.  Table 1's applicator is preserved byte-for-byte beside this file as
#  mutants572_table1.py.txt; the 18 table-1 entries below are unchanged from it.
#  V12 and V7 (two single builds, SCORES_V12_V7.txt) were added after table 2 ran; table
#  2's applicator is preserved as mutants572_table2.py.txt and its 27 entries are unchanged.
import io
import sys

#  --- the four fixed-source blocks the mutants edit --------------------------------
DECODE = "\t\t\td->lba   = (idata >> 6) & 1;"
RB = ("\t\t\todata = d->sdh_resv | (d->lba << 6) | (d->drive << 4) |\n"
      "\t\t\t    d->head;")
READ_ARM = ("\tif (d->lba)\n"
            "\t\toffset = 512 * (int64_t)(((d->head & 0xf) << 24) +\n"
            "\t\t    (cyl << 8) + d->sector);\n"
            "\n"
            "\twhile (count > 0) {")
WRITE_ARM = ("\tif (d->lba)\n"
             "\t\toffset = 512 * (int64_t)(((d->head & 0xf) << 24) +\n"
             "\t\t    (cyl << 8) + d->sector);\n"
             "\n"
             "\td->write_in_progress = d->cur_command;")
FORMULA = "((d->head & 0xf) << 24) +\n\t\t    (cyl << 8) + d->sector"
TAIL = "(cyl << 8) + d->sector);"


def read_new(expr):
    return READ_ARM.replace("\tif (d->lba)\n\t\toffset", expr + "\n\t\toffset", 1)


def write_new(expr):
    return WRITE_ARM.replace("\tif (d->lba)\n\t\toffset", expr + "\n\t\toffset", 1)


MUTANTS = {
    #  ---------------------------------------------------------------- TABLE 1
    #  decode (site 1)
    "V1":  (DECODE, "\t\t\td->lba   = (idata >> 5) & 1;"),              # (b) back on bit 5
    "V2":  (DECODE, "\t\t\td->lba   = (idata >> 7) & 1;"),             # decode on bit 7
    "V3":  (DECODE, "\t\t\td->lba   = ((idata >> 6) & (idata >> 5)) & 1;"),  # bit 6 AND bit 5

    #  read-site arm
    "V4r": (READ_ARM, read_new("\tif (d->lba && d->head == 0)")),     # (d) head-conditioned
    "V8":  (READ_ARM, READ_ARM.replace(FORMULA, "(cyl << 8) + d->sector", 1)),  # no head term
    "V11": (READ_ARM, READ_ARM.replace(TAIL, "(cyl << 8) + d->sector - 1);", 1)),  # sector - 1
    "V13r": (READ_ARM, read_new("\tif (1)")),                         # unconditional LBA (read)
    "V14w": (READ_ARM, read_new("\tif (0)")),                         # read arm left disabled
    "V15": (READ_ARM, READ_ARM.replace("512 * (int64_t)(((d->head",
                                       "512 * (((d->head", 1)),       # unwidened 32-bit product

    #  write-site arm
    "V4w": (WRITE_ARM, write_new("\tif (d->lba && d->head == 0)")),
    "V5w": (WRITE_ARM, write_new("\tif (d->lba && cyl == 0)")),
    "V6w": (WRITE_ARM, write_new("\tif (d->lba && d->sector != 0)")),
    "V13w": (WRITE_ARM, write_new("\tif (1)")),
    "V14r": (WRITE_ARM, write_new("\tif (0)")),                       # write arm left disabled

    #  read-back composition (site 4)
    "V16": (RB, RB.replace("d->sdh_resv |", "(d->sdh_resv | 0xa0) |", 1)),   # force bits 7,5 to 1
    "V17": (RB, RB.replace("d->sdh_resv |", "(d->sdh_resv & 0x80) |", 1)),   # drop reserved bit 5
    "V18": (RB, RB.replace("(d->lba << 6)", "(0)", 1)),                      # drop bit 6 reflection

    #  write_offset captured BEFORE the LBA arm runs (statement order in wdc__write)
    "V20": (("\tif (d->lba)\n"
             "\t\toffset = 512 * (int64_t)(((d->head & 0xf) << 24) +\n"
             "\t\t    (cyl << 8) + d->sector);\n"
             "\n"
             "\td->write_in_progress = d->cur_command;\n"
             "\td->write_count = count;\n"
             "\td->write_offset = offset;"),
            ("\td->write_in_progress = d->cur_command;\n"
             "\td->write_count = count;\n"
             "\td->write_offset = offset;\n"
             "\tif (d->lba)\n"
             "\t\toffset = 512 * (int64_t)(((d->head & 0xf) << 24) +\n"
             "\t\t    (cyl << 8) + d->sector);")),

    #  ---------------------------------------------------------------- TABLE 2
    "V5r": (READ_ARM, read_new("\tif (d->lba && cyl == 0)")),         # read, cyl-conditioned
    "V6r": (READ_ARM, read_new("\tif (d->lba && d->sector != 0)")),   # read, sector-conditioned
    "V8w": (WRITE_ARM, WRITE_ARM.replace(FORMULA, "(cyl << 8) + d->sector", 1)),  # write, no head
    "V11w": (WRITE_ARM, WRITE_ARM.replace(TAIL, "(cyl << 8) + d->sector - 1);", 1)),  # write, s-1
    "V9r8": (READ_ARM, READ_ARM.replace("<< 24) +", "<< 8) +", 1)),    # read, head shift k = 8
    "V10r": (READ_ARM, READ_ARM.replace("(cyl << 8)", "(d->cyl_lo << 8)", 1)),    # read, cyl_hi dropped
    "V10w": (WRITE_ARM, WRITE_ARM.replace("(cyl << 8)", "(d->cyl_lo << 8)", 1)),  # write, cyl_hi dropped
    #  The ANCHOR translations: every LBA moved by one sector at BOTH sites (the formula is
    #  duplicated in two local arms, so a device-wide shift is one conceptual edit at two
    #  textual sites) -- a LIST of (old, new) pairs, each matched exactly once in turn.
    "T_m1": [(READ_ARM, READ_ARM.replace(TAIL, "(cyl << 8) + d->sector - 1);", 1)),
             (WRITE_ARM, WRITE_ARM.replace(TAIL, "(cyl << 8) + d->sector - 1);", 1))],
    "T_p1": [(READ_ARM, READ_ARM.replace(TAIL, "(cyl << 8) + d->sector + 1);", 1)),
             (WRITE_ARM, WRITE_ARM.replace(TAIL, "(cyl << 8) + d->sector + 1);", 1))],

    #  ---------------------------------------------------------------- V12 / V7
    #  Two single builds run after table 2, recorded by their expected DISPOSITIONS and
    #  never as escapes: V12 is EQUIVALENT (the only writer of d->head is the SDH arm's
    #  `idata & 0xf`, so the mask in the formula is redundant in every reachable state);
    #  V7 is the disclosed BLIND cell (both the CHS and the LBA reading of a cyl_hi >= 1
    #  request fall past a 4096-sector image).  Each conditions BOTH sites in one build.
    "V12": [(READ_ARM, READ_ARM.replace("((d->head & 0xf) << 24)", "(d->head << 24)", 1)),
            (WRITE_ARM, WRITE_ARM.replace("((d->head & 0xf) << 24)", "(d->head << 24)", 1))],
    "V7": [(READ_ARM, read_new("\tif (d->lba && d->cyl_hi == 0)")),
           (WRITE_ARM, write_new("\tif (d->lba && d->cyl_hi == 0)"))],
}


def pairs(name):
    v = MUTANTS[name]
    return v if isinstance(v, list) else [v]


def apply(name, path):
    s = io.open(path, "r", newline="").read()
    for old, new in pairs(name):
        n = s.count(old)
        if n != 1:
            sys.stderr.write("MUTANT %s: old text occurs %d times (want 1)\n" % (name, n))
            sys.exit(3)
        if new == old:
            sys.stderr.write("MUTANT %s: new text equals old\n" % name)
            sys.exit(4)
        s = s.replace(old, new, 1)
    io.open(path, "w", newline="").write(s)
    print("MUTANT %s applied to %s" % (name, path))


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        for k in MUTANTS:
            print(k)
        return
    if len(sys.argv) == 3 and sys.argv[1] == "--check":
        #  every mutant's old text(s) must occur exactly once, applied in turn
        s = io.open(sys.argv[2], "r", newline="").read()
        bad = 0
        for k in MUTANTS:
            t = s
            ok = True
            occs = []
            for old, new in pairs(k):
                c = t.count(old)
                occs.append(c)
                ok = ok and c == 1 and new != old
                if c == 1:
                    t = t.replace(old, new, 1)
            print("%-5s occ=%s %s" % (k, occs, "OK" if ok else "*** BAD"))
            bad += (not ok)
        sys.exit(1 if bad else 0)
    if len(sys.argv) != 3:
        sys.stderr.write("usage: mutants572.py <name|--list|--check> <path>\n")
        sys.exit(2)
    apply(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
