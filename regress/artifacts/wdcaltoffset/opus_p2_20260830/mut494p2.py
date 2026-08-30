"""#494 pass-2 OPUS seat -- mutant applier.

A SEPARATE FILE rather than a heredoc inside the driver, deliberately: one backslash
level is consumed on the Bash -> heredoc -> Python path IN BOTH DIRECTIONS, and this
file has to write a C string literal containing a two-character `\\n`.  BS = chr(92)
and raw concatenation are immune in both directions.

Every mutant asserts its anchor count is EXACTLY 1 before editing.  A pattern that
matches nothing reports zero for everything, and a mutant that was never applied
scores as a KILL -- which is the vacuity this table exists to refuse.

    python3 mut494p2.py <file> <name>
"""
import io
import sys

BS = chr(92)

#  The two-character sequence backslash-n, as it appears INSIDE the C source's own
#  string literal.  Written this way rather than as an escape so no transport layer
#  can cook it into a real newline.
IGN = '\t\t    " ignored ]' + BS + 'n", (int)idata);'

GUARD = "\telse if (relative_addr != 0) {"

STATUS = ('\todata = status_byte(d, cpu);\n'
          '\n'
          '\tif (writeflag==MEM_READ)\n'
          '\t\tdebug("[ wdc: read from ALTSTATUS: 0x%02x ]' + BS + 'n",\n')

MUTANTS = {
    #  ---- CLAUSE-(d) CONDITIONAL NARROWINGS of the dominating predicate.
    #  `if (X)` -> `if (X && Y)` where Y holds in every state either probe builds.
    "n1_4bitguard": (
        GUARD,
        "\telse if (relative_addr != 0 && !(idata & WDCTL_4BIT)) {"),
    "n3_atapiguard": (
        GUARD,
        "\telse if (relative_addr != 0 && !d->atapi_cmd_in_progress) {"),
    "n4_wipguard": (
        GUARD,
        "\telse if (relative_addr != 0 && d->write_in_progress) {"),

    #  ---- POSITIVE CONTROL.  Must RED on both instruments.  Without it every
    #  "ESCAPED" row above could be a broken harness printing green.
    "n5_nulled": (
        GUARD,
        "\telse if (relative_addr > 1) {"),

    #  ---- SCOPE mutant: makes the alt handler symmetric with the main handler,
    #  which does `relative_addr /= d->addr_mult;`.  A NO-OP where addr_mult == 1
    #  (malta, every ISA/PCI wdc) and NOT a no-op on landisk (addr_mult=2) or
    #  macppc (addr_mult=0x10).  Both instruments run only on malta.
    "n2_addrmult": (
        STATUS,
        '\todata = status_byte(d, cpu);\n'
        '\n'
        '\trelative_addr /= d->addr_mult;\n'
        '\n'
        '\tif (writeflag==MEM_READ)\n'
        '\t\tdebug("[ wdc: read from ALTSTATUS: 0x%02x ]' + BS + 'n",\n'),

    #  ---- Q2 MEASUREMENT, not a kill-table row.  Does `return 0` from a
    #  REGISTERED device reach "unassigned-address handling" (the shipped comment's
    #  claim), or does memory_rw treat it as a FAILED device access?
    "n6_ret0": (
        IGN + "\n\t} else {",
        IGN + "\n\t\treturn 0;\n\t} else {"),
}


def main():
    path, name = sys.argv[1], sys.argv[2]
    if name not in MUTANTS:
        sys.stderr.write("unknown mutant %r\n" % name)
        return 3
    old, new = MUTANTS[name]
    t = io.open(path, encoding="utf-8", newline="").read()
    n = t.count(old)
    #  DENOMINATOR: say how many the anchor selected, so "0 of 1" and a silent
    #  no-op cannot look alike.
    sys.stdout.write("    anchor selected %d occurrence(s); want exactly 1\n" % n)
    if n != 1:
        sys.stderr.write("*** anchor count %d for %s -- refusing\n" % (n, name))
        return 4
    t2 = t.replace(old, new, 1)
    if t2 == t:
        sys.stderr.write("*** replacement was a no-op for %s\n" % name)
        return 5
    io.open(path, "w", encoding="utf-8", newline="").write(t2)
    sys.stdout.write("    applied %s\n" % name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
