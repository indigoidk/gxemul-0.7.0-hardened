import ast, sys
src, rep, out = sys.argv[1], sys.argv[2], sys.argv[3]
L = open(src, encoding="utf-8").read().split("\n")
assert L[235].startswith("is the INTERSECTION.  Over the 46 ACCEPTS entries:"), L[235][:60]
assert L[261] == "    46  = the ACCEPTS entry count (46 ENTRIES, six KINDS).", L[261]
R = open(rep, encoding="utf-8").read().rstrip("\n").split("\n")
new = "\n".join(L[:235] + R + L[262:])
open(out, "w", encoding="utf-8", newline="\n").write(new)
def code(t):
    m = ast.parse(t)
    return ast.dump(ast.Module(body=m.body[1:], type_ignores=[]))
a, b = ast.parse(open(src, encoding="utf-8").read()), ast.parse(new)
print("parses OK; code (AST minus docstring) identical:", code(open(src, encoding="utf-8").read()) == code(new))
print("docstring lines before/after: %d / %d" % (a.body[0].value.value.count("\n"), b.body[0].value.value.count("\n")))
print("SPLICE46_DONE")
