"""mut20.py <tag> -- apply ONE table-20 mutant to src/cpus/cpu_m88k.c in the current directory (the scratch clone).
Exits nonzero, leaving the file untouched, unless the find-text matches exactly once.  Tabs/newlines are chr(9)/chr(10)."""
import io, sys

T, N = chr(9), chr(10)
LABELS = ("MISALIGNED_ACCESS", "UNIMPLEMENTED_OPCODE", "PRIVILEGE_VIOLATION", "BOUNDS_CHECK_VIOLATION",
          "ILLEGAL_INTEGER_DIVIDE", "INTEGER_OVERFLOW", "ERROR")
L5 = ("MISALIGNED_ACCESS", "UNIMPLEMENTED_OPCODE", "PRIVILEGE_VIOLATION", "ILLEGAL_INTEGER_DIVIDE", "INTEGER_OVERFLOW")
SFRZ = "(cpu->cd.m88k.cr[M88K_CR_PSR] & M88K_PSR_SFRZ)"
RR_OLD = T + T + "if (!is_trap) {" + N + T + T + T + "vector = M88K_EXCEPTION_ERROR;"
FB_OLD = T + "if (vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented) {"
D865_OLD = T + "if (cpu->delay_slot)" + N + T + T + "cpu->delay_slot = EXCEPTION_IN_DELAY_SLOT;"
D840_OLD = T + T + "if (cpu->delay_slot) {" + N + T + T + T + "if (vector == M88K_EXCEPTION_DATA_ACCESS) {"


def rr(cond):
    return (RR_OLD, T + T + "if (" + cond + ") {" + N + T + T + T + "vector = M88K_EXCEPTION_ERROR;")


def fb(extra):
    return (FB_OLD, T + "if (vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented && " + extra + ") {")


SITE = {
    "M_RRNTDS": rr("!is_trap && !cpu->delay_slot"),
    "M_RRTDS": rr("!is_trap || cpu->delay_slot"),
    "M_RRUT": rr("!is_trap || (vector >= M88K_EXCEPTION_USER_TRAPS_START && cpu->delay_slot)"),
    "M_FBDS": fb("!cpu->delay_slot"),
    "M_FBFRZDS": fb("!(cpu->delay_slot && " + SFRZ + ")"),
    "M_DS865": (D865_OLD, T + "if (cpu->delay_slot && update_shadow_regs)" + N + T + T + "cpu->delay_slot = EXCEPTION_IN_DELAY_SLOT;"),
    "M_DS840UT": (D840_OLD, T + T + "if (cpu->delay_slot && vector < M88K_EXCEPTION_USER_TRAPS_START) {" + N + T + T + T +
                  "if (vector == M88K_EXCEPTION_DATA_ACCESS) {"),
}
for L in L5:
    SITE["M_RRDS_" + L] = rr("!is_trap || (vector == M88K_EXCEPTION_" + L + " && cpu->delay_slot)")
ARM = {}
for L in LABELS:
    ARM["M_DSNOT_" + L] = (L, "!cpu->delay_slot")
    ARM["M_DSFRZ_" + L] = (L, "!(cpu->delay_slot && " + SFRZ + ")")
    ARM["M_ARMTS_" + L] = (L, "!(cpu->delay_slot && is_trap)")
for L in L5:
    ARM["M_ARMTSU_" + L] = (L, "!(cpu->delay_slot && is_trap && !" + SFRZ + ")")

tag = sys.argv[1]
p = "src/cpus/cpu_m88k.c"
t = io.open(p, encoding="utf-8", newline="").read()
if tag in SITE:
    old, new = SITE[tag]
    n = t.count(old)
    if n != 1:
        print("MUT20_FAIL %s: find-text matched %d times -- file untouched" % (tag, n)); sys.exit(3)
    t = t.replace(old, new)
    shown = new.strip().split(N)[0]
elif tag in ARM:
    L, expr = ARM[tag]
    lines = t.split(N)
    hits = [k for k, l in enumerate(lines) if l.strip() == "case M88K_EXCEPTION_%s:" % L]
    if not hits:
        print("MUT20_FAIL %s: case label not found" % tag); sys.exit(3)
    js = [k for k in range(hits[0], hits[0] + 6) if "implemented = true;" in lines[k]]
    if len(js) != 1:
        print("MUT20_FAIL %s: implemented line not found under the label" % tag); sys.exit(3)
    lines[js[0]] = lines[js[0]].replace("implemented = true;", "implemented = %s;" % expr)
    t = N.join(lines)
    shown = "line %d: %s" % (js[0] + 1, lines[js[0]].strip())
else:
    print("MUT20_FAIL unknown tag %s" % tag); sys.exit(3)
io.open(p, "w", encoding="utf-8", newline="").write(t)
print("MUT20_OK %s: %s" % (tag, shown))
