# -*- coding: utf-8 -*-
#  #489 M0: BARE DELETION of the cnt!=408 guard, for an ASAN run.
#
#  Written as a REAL FILE, not through a nested heredoc.  The first attempt embedded the
#  anchor in `python3 - <<'PY'` inside `cat <<'EOF'`, and the C string's `\n` was eaten by
#  the chain -- the applier refused with count=0, which is the correct failure but cost a
#  build.  The carrier's rule is exactly this: use chr(92) for any backslash that must
#  survive, and do not reason about how many levels consume it.
import io, sys

BS = chr(92)

OLD = (
    '\t\tif (d->cnt != 408) {\n'
    '\t\t\tif (!(d->warned & GDROM_W_TOCLEN)) {\n'
    '\t\t\t\td->warned |= GDROM_W_TOCLEN;\n'
    '\t\t\t\tfatal("[ dreamcast_gdrom: Read TOC with"\n'
    '\t\t\t\t    " cnt=%i, not 408 -- declined.  (once) ]' + BS + 'n",\n'
    '\t\t\t\t    (int) d->cnt);\n'
    '\t\t\t}\n'
    '\t\t\tbreak;\n'
    '\t\t}\n'
)

p = sys.argv[1]
t = io.open(p, encoding='utf-8', newline='').read()
n = t.count(OLD)
if n != 1:
    sys.stderr.write("MUTANT TEXT NOT FOUND (count=%d) -- refusing\n" % n)
    sys.exit(1)
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(OLD, '', 1))

# verify the guard is gone and alloc_data is now unconditional on this path
v = io.open(p, encoding='utf-8', newline='').read()
assert 'if (d->cnt != 408) {' not in v, "guard still present after edit"
print("M0 applied: cnt!=408 guard deleted, alloc_data now reached for ANY cnt")
