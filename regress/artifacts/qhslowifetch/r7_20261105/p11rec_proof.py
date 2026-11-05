import ast
import io
import sys
import tokenize

# Text-only proof for the pass-11 records: the edited probe against table 12's frozen instrument and the pre-edit backup.
cur, frozen, pre = sys.argv[1], sys.argv[2], sys.argv[3]


def src(p):
    return io.open(p, encoding="utf-8", newline="").read()


def ast_minus_doc(p):
    b = ast.parse(src(p)).body
    if b and isinstance(b[0], ast.Expr) and isinstance(b[0].value, ast.Constant) and isinstance(b[0].value.value, str):
        b = b[1:]
    return ast.dump(ast.Module(body=b, type_ignores=[]))


class Mask(ast.NodeTransformer):
    def visit_Constant(self, n):
        return ast.copy_location(ast.Constant(value="S"), n) if isinstance(n.value, str) else n


def ast_all_strings_masked(p):
    return ast.dump(Mask().visit(ast.parse(src(p))))


def tokens(p):
    out, first = [], True
    for t in tokenize.generate_tokens(io.StringIO(src(p)).readline):
        if t.type in (tokenize.COMMENT, tokenize.NL, tokenize.ENCODING):
            continue
        if first and t.type == tokenize.STRING:      # the module docstring
            first = False
            continue
        first = False
        out.append((t.type, t.string))
    return out


def docstring(p):
    return ast.get_docstring(ast.parse(src(p)), clean=False)


for other, tag in ((frozen, "frozen table12"), (pre, "pre_p11rec")):
    print("vs %-15s AST minus docstring: %s" % (tag, "EQUAL" if ast_minus_doc(cur) == ast_minus_doc(other) else "DIFFERENT"))
    print("vs %-15s AST all strings masked: %s" % (tag, "EQUAL" if ast_all_strings_masked(cur) == ast_all_strings_masked(other)
                                                  else "DIFFERENT"))
    print("vs %-15s tokens minus comments and docstring: %s" % (tag, "EQUAL" if tokens(cur) == tokens(other) else "DIFFERENT"))
# Negative control: the comparison must be able to fail.  Change one printed string in a copy and compare again.
s = src(cur)
k = s.index('"exit0"', s.index('"""', s.index('"""') + 3))
mut = s[:k] + '"exit1"' + s[k + 7:]
mp = sys.argv[4]                                    # a scratchpad path: nothing is written under regress/
io.open(mp, "w", encoding="utf-8", newline="").write(mut)
try:
    print("negative control (one printed string changed): AST minus docstring %s; tokens %s" % (
        "EQUAL" if ast_minus_doc(mp) == ast_minus_doc(cur) else "DIFFERENT",
        "EQUAL" if tokens(mp) == tokens(cur) else "DIFFERENT"))
finally:
    import os
    os.remove(mp)
d = docstring(cur).split("\n")
print("docstring lines %d, max width %d, trailing-space lines %d" % (len(d), max(len(x) for x in d), sum(x != x.rstrip() for x in d)))
