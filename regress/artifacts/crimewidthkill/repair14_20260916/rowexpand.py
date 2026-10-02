#!/usr/bin/env python3
"""rowexpand.py -- statically expand every row() NAME in crime_width_probe.py and look for COLLISIONS.

*** WHY THIS IS NOT REDUNDANT WITH THE DUPLICATE CHECK ALREADY RUN. ***  That one compared LITERAL row
names.  154 row() call sites produce 204 rows, so the difference is made by names built from FORMAT
TEMPLATES inside loops -- `row("%s pc" % op, ...)' -- and a literal-only check cannot see those at all.
Two loops in this probe emit five textually IDENTICAL templates; whether they collide depends entirely on
whether their loop domains overlap, which is not visible at the call site.

A collision does not crash.  Two rows with one name silently merge, the table reports fewer rows than the
probe defines, and table 12's base leg does not read 204/204 -- after a full build and run.

METHOD, and its limits are stated rather than implied:
  * parse with ast, never regex;
  * a row() whose first argument is a plain string -> that literal;
  * a row() whose first argument is `"<tmpl>" % <name>' or `"<tmpl>" % (<names>)' -> look OUTWARD through
    enclosing ast.For nodes for one binding that name, and expand over the loop's literal domain;
  * anything else -> reported UNRESOLVED and counted separately.  An unresolved name is NOT scored as
    unique; saying "0 duplicates" while silently dropping names is the check-that-cannot-fail shape.
"""
import ast, io, sys
from collections import Counter

P = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\crime_width_probe.py"
tree = ast.parse(io.open(P, encoding="utf-8").read())

#  parent links, so a row() call can look outward for its enclosing loops
parent = {}
for node in ast.walk(tree):
    for ch in ast.iter_child_nodes(node):
        parent[ch] = node

def enclosing_fors(node):
    out, cur = [], parent.get(node)
    while cur is not None:
        if isinstance(cur, ast.For):
            out.append(cur)
        cur = parent.get(cur)
    return out

def target_names(tgt):
    if isinstance(tgt, ast.Name):
        return [tgt.id]
    if isinstance(tgt, (ast.Tuple, ast.List)):
        return [e.id for e in tgt.elts if isinstance(e, ast.Name)]
    return []

def domain_for(var, fors):
    """values `var' takes, from the nearest enclosing for whose target binds it"""
    for f in fors:
        names = target_names(f.target)
        if var not in names:
            continue
        idx = names.index(var)
        try:
            it = ast.literal_eval(f.iter)
        except Exception:
            return None
        vals = []
        for item in it:
            if len(names) == 1:
                vals.append(item)
            else:
                if not isinstance(item, (tuple, list)) or idx >= len(item):
                    return None
                vals.append(item[idx])
        return vals
    return None

names, unresolved = [], []
sites = 0
for node in ast.walk(tree):
    if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id == "row" and node.args):
        continue
    sites += 1
    a = node.args[0]
    ln = getattr(node, "lineno", -1)

    if isinstance(a, ast.Constant) and isinstance(a.value, str):
        names.append((a.value, ln)); continue

    #  "<tmpl>" % <expr>
    if (isinstance(a, ast.BinOp) and isinstance(a.op, ast.Mod)
            and isinstance(a.left, ast.Constant) and isinstance(a.left.value, str)):
        tmpl = a.left.value
        rhs = a.right
        vars_ = [rhs.id] if isinstance(rhs, ast.Name) else \
                ([e.id for e in rhs.elts if isinstance(e, ast.Name)]
                 if isinstance(rhs, ast.Tuple) and all(isinstance(e, ast.Name) for e in rhs.elts)
                 else None)
        if vars_:
            fors = enclosing_fors(node)
            doms = [domain_for(v, fors) for v in vars_]
            if all(d is not None for d in doms):
                if len(doms) == 1:
                    for v in doms[0]:
                        names.append((tmpl % v, ln))
                else:
                    import itertools
                    for combo in itertools.product(*doms):
                        names.append((tmpl % combo, ln))
                continue
        unresolved.append((ast.dump(a)[:70], ln)); continue

    unresolved.append((ast.dump(a)[:70], ln))

print("row() call sites          : %d" % sites)
print("names RESOLVED statically : %d" % len(names))
print("names UNRESOLVED          : %d   (NOT scored as unique -- see below)" % len(unresolved))
print("")
c = Counter(n for n, _ in names)
dups = {n: k for n, k in c.items() if k > 1}
print("DISTINCT resolved names   : %d" % len(c))
print("COLLISIONS                : %d" % len(dups))
for n, k in sorted(dups.items()):
    where = sorted({l for nm, l in names if nm == n})
    print("   *** %-22r x%d   at lines %s" % (n, k, where))
if unresolved:
    print("")
    print("UNRESOLVED (each could hide a collision; listed so the count is honest):")
    for d, l in unresolved[:25]:
        print("   line %4d  %s" % (l, d))
print("")
print("ROWEXPAND_%s" % ("CLEAN" if not dups else "COLLISION"))
sys.exit(1 if dups else 0)
