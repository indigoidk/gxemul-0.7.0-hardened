#!/usr/bin/env python3
"""r6_20261105 -- prove the records-6 probe edit is TEXT ONLY.

Usage: python3 -I textonly_check.py <edited probe> <frozen probe>

Check 1 (the one the round asks for): ast.dump() of each file with the module docstring dropped and EVERY string constant replaced
by the placeholder "S" must be equal.  Anything that is not a docstring, a comment or a string literal -- a row's instruction word,
seed, want, register list, control flag, the sentinel logic -- survives the placeholdering and would make the dumps differ.

Check 2 (supplementary, because row NAMES and notice FRAGMENTS are string literals too and are logic, not text): the string
constants are listed in source order for both files and paired up; every pair that differs is printed.  Each must be a `note`
argument (the fourth positional argument of a row() call) or a comment-like string; a differing row name, `has()` fragment,
format string or sentinel would show here.  Same count of constants on both sides is required.
"""
import ast
import sys


def load(path):
    with open(path, encoding="latin-1") as f:
        return ast.parse(f.read(), path)


def placeholdered(tree):
    body = tree.body
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
        body = body[1:]
    mod = ast.Module(body=body, type_ignores=[])
    for n in ast.walk(mod):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            n.value = "S"
    return ast.dump(mod)


def strings(tree):
    body = tree.body
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
        body = body[1:]
    mod = ast.Module(body=body, type_ignores=[])
    out = []
    for n in ast.walk(mod):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            out.append((n.lineno, n.col_offset, n.value))
    out.sort()
    return out


def note_positions(tree):
    """(lineno, col) of every string that is a note: the 4th positional argument of a row() call, or the element bound to the
    loop variable `note` in a `for ..., note in ((...), ...)` loop (the witness rows pass that variable on as the row's note)."""
    pos = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "row" and len(n.args) >= 4:
            for s in ast.walk(n.args[3]):
                if isinstance(s, ast.Constant) and isinstance(s.value, str):
                    pos.add((s.lineno, s.col_offset))
        if isinstance(n, ast.For) and isinstance(n.target, ast.Tuple) and isinstance(n.iter, ast.Tuple):
            names = [t.id if isinstance(t, ast.Name) else None for t in n.target.elts]
            if "note" in names:
                k = names.index("note")
                for row_tuple in n.iter.elts:
                    if isinstance(row_tuple, ast.Tuple) and len(row_tuple.elts) == len(names):
                        s = row_tuple.elts[k]
                        if isinstance(s, ast.Constant) and isinstance(s.value, str):
                            pos.add((s.lineno, s.col_offset))
    return pos


#  placeholdered() rewrites the constants IN PLACE, so check 2 parses its own trees (the first version of this script listed
#  the already-placeholdered constants and reported 0 differences -- a false pass, caught because three notes were known to differ).
d1, d2 = placeholdered(load(sys.argv[1])), placeholdered(load(sys.argv[2]))
print("check 1 (ast.dump, module docstring dropped, every string constant -> 'S'):", "EQUAL" if d1 == d2 else "DIFFERENT")
print("   dump length edited=%d frozen=%d" % (len(d1), len(d2)))

edited, frozen = load(sys.argv[1]), load(sys.argv[2])
s1, s2 = strings(edited), strings(frozen)
print("check 2 (string constants in source order): edited=%d frozen=%d" % (len(s1), len(s2)))
notes = note_positions(edited)
rc = 0 if d1 == d2 else 1
if len(s1) != len(s2):
    print("   COUNT DIFFERS")
    rc = 1
else:
    n_diff = 0
    for (l1, c1, v1), (l2, c2, v2) in zip(s1, s2):
        if v1 != v2:
            n_diff += 1
            kind = "note" if (l1, c1) in notes else "NOT A NOTE"
            if kind != "note":
                rc = 1
            print("   differs: edited :%d (%s) %r <- frozen :%d %r" % (l1, kind, v1, l2, v2))
    print("   %d string constants differ; all notes: %s" % (n_diff, "yes" if rc == 0 else "NO"))
print("TEXTONLY_CHECK=%s" % ("PASS" if rc == 0 else "FAIL"))
sys.exit(rc)
