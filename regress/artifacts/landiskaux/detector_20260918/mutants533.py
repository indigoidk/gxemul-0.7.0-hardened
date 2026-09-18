#!/usr/bin/env python3
"""landiskaux kill-table mutants.  Usage: mutants533.py <name> <src dev_wdc.c> <dst dev_wdc.c>
Each find-text must occur EXACTLY ONCE, or the mutant refuses -- so a find-text that stops
matching reads as a FAIL, never as a silently-unmutated green."""
import io, sys

CASE = ("\tcase MACHINE_LANDISK:\n")
FIX = "\t\talt_status_addr = devinit->addr + 0x2c;\n"
IQ = "\tcase MACHINE_IQ80321:\n\t\talt_status_addr = devinit->addr + 0x402;\n\t\tbreak;\n"
REG = ("\tmemory_device_register(devinit->machine->memory, \"wdc_altstatus\",\n"
       "\t    alt_status_addr, 2, dev_wdc_altstatus_access, d, DM_DEFAULT, NULL);\n")


def landisk_block(s):
    """The whole appended case, comment included, up to and including its break."""
    i = s.index(CASE)
    j = s.index("\t\tbreak;\n", i) + len("\t\tbreak;\n")
    return s[i:j]


def m_head(s):
    return s.replace(landisk_block(s), "", 1)


def m_0x16(s):
    return s.replace(FIX, "\t\talt_status_addr = devinit->addr + 0x16;\n", 1)


def m_0x2d(s):
    return s.replace(FIX, "\t\talt_status_addr = devinit->addr + 0x2d;\n", 1)


def m_both(s):
    extra = ("\tif (devinit->machine->machine_type == MACHINE_LANDISK)\n"
             "\t\tmemory_device_register(devinit->machine->memory, \"wdc_altstatus_old\",\n"
             "\t\t    devinit->addr + 0x206, 2, dev_wdc_altstatus_access, d, DM_DEFAULT, NULL);\n")
    return s.replace(REG, REG + extra, 1)


def m_above(s):
    blk = landisk_block(s)
    nobreak = blk[: blk.rindex("\t\tbreak;\n")]
    s = s.replace(blk, "", 1)
    return s.replace(IQ, nobreak + IQ, 1)


M = {"M_head": (m_head, [CASE]), "M_0x16": (m_0x16, [FIX]), "M_0x2d": (m_0x2d, [FIX]),
     "M_both": (m_both, [REG]), "M_above": (m_above, [CASE, IQ])}

if __name__ == "__main__":
    if sys.argv[1:2] == ["list"]:
        print(" ".join(M)); sys.exit(0)
    name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    s = io.open(src, newline="").read()
    fn, finds = M[name]
    for f in finds:
        if s.count(f) != 1:
            sys.stderr.write("MUTANT %s: find-text occurs %d times (want 1)\n" % (name, s.count(f)))
            sys.exit(2)
    out = fn(s)
    if out == s:
        sys.stderr.write("MUTANT %s: produced NO change\n" % name); sys.exit(3)
    io.open(dst, "w", newline="").write(out)
