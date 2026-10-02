#!/usr/bin/env python3
"""Definition-before-use check for the repair-14 edits.

ast.parse() proves the file is SYNTACTICALLY valid.  It does not prove that a name used at line N was
bound before line N -- and crime_width_probe.py is a TOP-LEVEL SCRIPT that executes as it reads, so a
name used too early is a NameError that surfaces only when the table runs.  That would cost a table.

This checks every name the repair-14 additions use against the line where it is first bound.
"""
import ast, io, sys

P = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\crime_width_probe.py"
src = io.open(P, encoding="utf-8").read()
tree = ast.parse(src)

#  first binding line for every top-level name
bound = {}
for node in tree.body:
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        bound.setdefault(node.name, node.lineno)
    elif isinstance(node, ast.Assign):
        for t in node.targets:
            for n in ast.walk(t):
                if isinstance(n, ast.Name):
                    bound.setdefault(n.id, node.lineno)
    elif isinstance(node, (ast.For, ast.While, ast.If)):
        for n in ast.walk(node):
            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
                bound.setdefault(n.id, node.lineno)

#  the names the repair-14 additions depend on, and where each addition sits
CHECKS = [
    ("rst_session body", "roundtrip"), ("rst_session body", "LIVE_VAL"), ("rst_session body", "SENT"),
    ("rst_session body", "pr"), ("rst_session body", "Addr"), ("rst_session body", "CODE"),
    ("rst_session body", "CRIME"), ("rst_session body", "ld"), ("rst_session body", "st"),
    ("rst_session body", "session"), ("rst_session body", "row"),
    ("gapped_clear body", "enc"), ("gapped_clear body", "OP_B_SELF"), ("gapped_clear body", "OP_NOP"),
    ("gapped_clear body", "nth"), ("gapped_clear body", "mag"),
    ("entry 21 rows", "BIT"), ("entry 46 row", "count"),
]

#  where the new code starts: the first repair-14 marker
marker = "#529 repair 14"
first_use = src[:src.find(marker)].count(chr(10)) + 1 if marker in src else None

bad = 0
print("name                 bound at   first repair-14 use at ~%s" % first_use)
for where, name in CHECKS:
    ln = bound.get(name)
    if ln is None:
        print("  %-18s *** NOT BOUND AT TOP LEVEL ***   (%s)" % (name, where))
        bad += 1
    else:
        ok = "OK" if first_use is None or ln < first_use else "*** DEFINED AFTER FIRST USE ***"
        print("  %-18s %-10d %s   (%s)" % (name, ln, ok, where))
        if not (first_use is None or ln < first_use):
            bad += 1

#  and the three new helpers must themselves be defined before the loops that call them
for helper, caller in (("gapped_clear", "_clearnote"), ("rst_session", "_rv")):
    h = bound.get(helper)
    c = bound.get(caller)
    if h is None or c is None:
        print("  %-18s *** helper or caller not found (%s/%s) ***" % (helper, h, c)); bad += 1
    elif h < c:
        print("  %-18s def %-6d < first call %-6d  OK" % (helper, h, c))
    else:
        print("  %-18s *** def %d AFTER its caller %d ***" % (helper, h, c)); bad += 1

print("")
print("FAILURES: %d" % bad)
print("NAMEORDER_%s" % ("PASS" if bad == 0 else "FAIL"))
sys.exit(1 if bad else 0)
