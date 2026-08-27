#!/usr/bin/env python3
"""Apply ONE named mutant to /tmp/gx465p2's gdrom device file.

Every edit asserts its find-text is PRESENT (MUTANT-TEXT-NOT-FOUND is a hard
failure, which turns each find-text into a presence pin) and asserts the file
actually changed.  `restore` copies the pristine file back from GXEMUL-SEC --
never from a backup this script made, per the carrier's restore rule.
"""
import shutil, sys

F = "/tmp/gx465p2/src/devices/dev_dreamcast_gdrom.c"
SEC = "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_dreamcast_gdrom.c"

FREE_LEN   = "\td->data = NULL;\n\td->data_len = 0;\n}\n"
FREE_NOLEN = "\td->data = NULL;\n}\n"
BRK429     = "\t\t\tbreak;\t/* OB-20: was exit(1) */\n"
RET429     = "\t\t\treturn;\t/* OB-20: was exit(1) */\n"
BRK420     = "\t\t\t    (int)sector_count);\n\t\t\tbreak;\n"
RET420     = "\t\t\t    (int)sector_count);\n\t\t\treturn;\n"
TAIL       = "\t} else {\n\t\td->cnt = 0;\n\t\td->cond &= ~COND_DATA_AVAIL;\n\t}\n"
TAIL_LEN   = "\t} else {\n\t\td->cnt = 0;\n\t\td->data_len = 0;\n\t\td->cond &= ~COND_DATA_AVAIL;\n\t}\n"

EDITS = {
    #  clause (b) verbatim reinstatement AND clause (d) "keep the guard, remove
    #  its repair" in one edit: free_data() survives, its data_len release does not.
    "Md_nolen":  [(FREE_LEN, FREE_NOLEN)],
    #  question 3's mutant against the SHIPPED form (== the table's m_helper_ret)
    "Mret429":   [(BRK429, RET429)],
    #  the sibling arm, for completeness
    "Mret420":   [(BRK420, RET420)],
    #  the REJECTED candidate fix: repair moved from the release point to the tail
    "Mtail":     [(FREE_LEN, FREE_NOLEN), (TAIL, TAIL_LEN)],
    #  == the table's m_ret415: the tail form with its tail bypassed
    "Mtailret":  [(FREE_LEN, FREE_NOLEN), (TAIL, TAIL_LEN), (BRK429, RET429)],
}

what = sys.argv[1]
if what == "restore":
    shutil.copyfile(SEC, F)
    print("RESTORED from GXEMUL-SEC")
    sys.exit(0)

shutil.copyfile(SEC, F)          # always start from pristine
src = open(F).read()
for find, repl in EDITS[what]:
    if src.count(find) != 1:
        print("MUTANT-TEXT-NOT-FOUND count=%d for %r" % (src.count(find), find[:40]))
        sys.exit(9)
    src = src.replace(find, repl)
open(F, "w").write(src)
if open(F).read() == open(SEC).read():
    print("MUTANT-NO-CHANGE")
    sys.exit(9)
print("MUTANT %s APPLIED" % what)
