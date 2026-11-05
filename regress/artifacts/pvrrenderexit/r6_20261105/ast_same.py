#!/usr/bin/env python3
"""ast_same.py -- do two versions of a Python script have the same AST once the module docstring is removed?  (Comments are not in
the AST.)  Prints SAME or DIFFERENT with the dump sizes.  usage: ast_same.py <a.py> <b.py>"""
import ast
import io
import sys


def body_dump(path):
    tree = ast.parse(io.open(path, encoding="latin-1").read())
    b = tree.body
    if b and isinstance(b[0], ast.Expr) and isinstance(getattr(b[0], "value", None), ast.Constant) and isinstance(b[0].value.value, str):
        b = b[1:]
    return ast.dump(ast.Module(body=b, type_ignores=[]), include_attributes=False)


a, b = body_dump(sys.argv[1]), body_dump(sys.argv[2])
print("%s (AST without the docstring: %d vs %d chars)" % ("SAME" if a == b else "DIFFERENT", len(a), len(b)))
