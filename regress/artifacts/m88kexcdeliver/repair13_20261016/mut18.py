"""mut18.py <tag> -- apply ONE table-18 mutant to src/cpus/cpu_m88k.c in the current directory (the scratch clone).
Exits nonzero, leaving the file untouched, unless the find-text matches exactly once.  Tabs/newlines are chr(9)/chr(10):
no backslash escapes, because the Bash -> heredoc -> Python path consumes one level (see mut17.py)."""
import io, sys

T, N = chr(9), chr(10)
RR_OLD = T + T + "if (!is_trap) {" + N + T + T + T + "vector = M88K_EXCEPTION_ERROR;"
FB_OLD = T + "if (vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented) {"
SITE = {
    "M_RRNTDS": (RR_OLD, T + T + "if (!is_trap && !cpu->delay_slot) {" + N + T + T + T + "vector = M88K_EXCEPTION_ERROR;"),
    "M_RRTDS": (RR_OLD, T + T + "if (!is_trap || cpu->delay_slot) {" + N + T + T + T + "vector = M88K_EXCEPTION_ERROR;"),
    "M_FBDS": (FB_OLD, T + "if (vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented && !cpu->delay_slot) {"),
}
ARMS = {"M_DSNOT_" + a: a for a in ("MISALIGNED_ACCESS", "UNIMPLEMENTED_OPCODE", "PRIVILEGE_VIOLATION", "INTEGER_OVERFLOW",
                                    "ILLEGAL_INTEGER_DIVIDE", "BOUNDS_CHECK_VIOLATION", "ERROR")}
tag = sys.argv[1]
p = "src/cpus/cpu_m88k.c"
t = io.open(p, encoding="utf-8", newline="").read()
if tag in SITE:
    old, new = SITE[tag]
    n = t.count(old)
    if n != 1:
        print("MUT18_FAIL %s: find-text matched %d times -- file untouched" % (tag, n)); sys.exit(3)
    t = t.replace(old, new)
    shown = new.strip().split(N)[0]
elif tag in ARMS:
    lines = t.split(N)
    hits = [k for k, l in enumerate(lines) if l.strip() == "case M88K_EXCEPTION_%s:" % ARMS[tag]]
    if len(hits) < 1:
        print("MUT18_FAIL %s: case label not found" % tag); sys.exit(3)
    i = hits[0]                       # switch 1 is the first switch in the file's exception function
    js = [k for k in range(i, i + 6) if "implemented = true;" in lines[k]]
    if len(js) != 1:
        print("MUT18_FAIL %s: implemented line not found under the label" % tag); sys.exit(3)
    lines[js[0]] = lines[js[0]].replace("implemented = true;", "implemented = !cpu->delay_slot;")
    t = N.join(lines)
    shown = "line %d: %s" % (js[0] + 1, lines[js[0]].strip())
else:
    print("MUT18_FAIL unknown tag %s" % tag); sys.exit(3)
io.open(p, "w", encoding="utf-8", newline="").write(t)
print("MUT18_OK %s: %s" % (tag, shown))
