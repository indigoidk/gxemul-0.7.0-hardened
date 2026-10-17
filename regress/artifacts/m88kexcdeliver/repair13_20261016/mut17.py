"""mut17.py <tag> -- apply ONE table-17 mutant to src/cpus/cpu_m88k.c in the current directory (the scratch clone).
Exits nonzero, leaving the file untouched, unless the find-text matches exactly once; the driver then verifies the file
DIFFERS from HEAD's before it builds.  No backslash escapes anywhere: tabs and newlines are chr(9) and chr(10), because a
Bash -> heredoc -> Python path consumes one backslash level (the first draft of this driver lost it, which would have
measured the unmutated binary and reported it as an escape)."""
import io, sys

T, N = chr(9), chr(10)
RR_OLD = T + T + "if (!is_trap) {" + N + T + T + T + "vector = M88K_EXCEPTION_ERROR;"
FB_OLD = T + "if (vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented) {"
MUT = {
    "M_RRNTDS": (RR_OLD, T + T + "if (!is_trap && !cpu->delay_slot) {" + N + T + T + T + "vector = M88K_EXCEPTION_ERROR;"),
    "M_RRTDS": (RR_OLD, T + T + "if (!is_trap || cpu->delay_slot) {" + N + T + T + T + "vector = M88K_EXCEPTION_ERROR;"),
    "M_FBDS": (FB_OLD, T + "if (vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented && !cpu->delay_slot) {"),
}
tag = sys.argv[1]
old, new = MUT[tag]
p = "src/cpus/cpu_m88k.c"
t = io.open(p, encoding="utf-8", newline="").read()
n = t.count(old)
if n != 1:
    print("MUT17_FAIL %s: find-text matched %d times -- file untouched" % (tag, n))
    sys.exit(3)
io.open(p, "w", encoding="utf-8", newline="").write(t.replace(old, new))
print("MUT17_OK %s: %s" % (tag, new.strip().split(N)[0]))
