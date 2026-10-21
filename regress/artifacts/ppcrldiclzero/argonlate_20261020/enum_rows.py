#!/usr/bin/env python3
"""Static (AST-only) enumeration of every row() call in a ppc_rldicl_probe.py revision.
Never imports or executes the probe.  Usage: enum_rows.py <probe.py>"""
import ast
import io
import sys

src = io.open(sys.argv[1], encoding="utf-8", newline="").read()
tree = ast.parse(src)
lines = src.split("\n")

# ---- every call site of every helper, by enclosing top-level statement line
HELPERS = ["rotl64", "mask_b_63", "mask_0_e", "mask_range", "want_rldicl",
           "want_rldicr", "want_rldimi", "rotl32", "mask32", "want_rlwinm",
           "want_rlwimi", "RLDICL", "RLDICR", "RLDIMI", "RLWINM", "RLWIMI",
           "enc_md", "enc_m", "LI", "ORI"]
calls = {h: [] for h in HELPERS}
for node in ast.walk(tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
            and node.func.id in calls:
        calls[node.func.id].append(node.lineno)
print("=== helper call sites (line numbers of the Call node)")
for h in HELPERS:
    print("  %-12s %3d  %s" % (h, len(calls[h]), sorted(calls[h])))

# ---- names referenced by each module-level assignment, to resolve a want/got
#      expression that goes through a variable (e.g. census_fail, _naive)
def names_in(n):
    out = set()
    for x in ast.walk(n):
        if isinstance(x, ast.Name):
            out.add(x.id)
        if isinstance(x, ast.Call) and isinstance(x.func, ast.Name):
            out.add(x.func.id + "()")
    return out

print()
print("=== row() calls: line | name | WANT expression | names/calls in WANT | names/calls in GOT")
n = 0
for node in ast.walk(tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
            and node.func.id == "row":
        n += 1
        name = node.args[0].value if isinstance(node.args[0], ast.Constant) else "?"
        got = node.args[1]
        want = node.args[2]
        wsrc = ast.get_source_segment(src, want)
        print("%3d | %-16s | %-44s | %-38s | %s" % (
            node.lineno, name, wsrc.replace("\n", " ")[:44],
            ",".join(sorted(names_in(want))) or "-",
            ",".join(sorted(names_in(got)))[:70]))
print("ROW CALLS: %d" % n)
