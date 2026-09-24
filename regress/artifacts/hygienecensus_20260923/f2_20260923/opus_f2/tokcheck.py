#!/usr/bin/env python3
"""opus seat, F2 pass: would a TOKEN-level classifier (python's own tokenize: COMMENT and STRING tokens are not code)
see what the gate's line-level `grep -v '^[[:space:]]*#' | grep 'endswith('` misses?  Read-only over a copy.

For each copy dir given: the pty population the gate uses (raw text contains the regex pty.fork), classified two ways:
  gate   -- the gate's rule: a non-full-line-comment line contains the text `endswith(`
  token  -- a NAME token `endswith` immediately followed by the OP `(` (comments, strings, docstrings are not code)
and the whole-buffer census counted two ways over the pty-driving population: LINES (the gate) vs OCCURRENCES.
"""
import io, os, re, sys, tokenize

GF_RE = re.compile(r'^GRANDFATHERED_PROMPTLESS="(.*?)"', re.S | re.M)
WHOLE = re.compile(r'buf.rstrip\(\).endswith\(["\']GXemul>["\']\)')
PTYD = re.compile(r'pty\.fork|forkpty|pty\.spawn|^[ \t]*(import|from) drive_guest', re.M)

def token_has_endswith_call(src):
    toks = [t for t in tokenize.generate_tokens(io.StringIO(src).readline)
            if t.type not in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT)]
    for a, b in zip(toks, toks[1:]):
        if a.type == tokenize.NAME and a.string == "endswith" and b.type == tokenize.OP and b.string == "(":
            return True
    return False

def gate_has(src):
    return any("endswith(" in l for l in src.split("\n") if not re.match(r"^[ \t]*#", l))

for d in sys.argv[1:]:
    files = []
    for root, dirs, fs in os.walk(d):
        dirs[:] = [x for x in dirs if not (root == d and x == "artifacts")]
        files += [os.path.join(root, f) for f in fs if f.endswith(".py")]
    pty = [f for f in files if re.search(r"pty.fork", io.open(f, encoding="utf-8", errors="replace").read())]
    gate_pl, tok_pl, tok_err = set(), set(), []
    for f in pty:
        s = io.open(f, encoding="utf-8", errors="replace").read()
        rel = os.path.relpath(f, d)
        if not gate_has(s): gate_pl.add(rel)
        try:
            if not token_has_endswith_call(s): tok_pl.add(rel)
        except (tokenize.TokenError, SyntaxError, IndentationError) as e:
            tok_err.append("%s (%s)" % (rel, type(e).__name__)); tok_pl.add(rel)   # unreadable -> fail-closed
    g = GF_RE.search(io.open(os.path.join(d, "gate_hygiene.sh"), encoding="utf-8").read())
    gf = set(g.group(1).split()) if g else set()
    lines = occ = 0
    for f in files:
        s = io.open(f, encoding="utf-8", errors="replace").read()
        if not PTYD.search(s): continue
        for l in s.split("\n"):
            if re.match(r"^[ \t]*#", l): continue
            n = len(WHOLE.findall(l)); occ += n; lines += 1 if n else 0
    print("== %s" % d)
    print("   pty population %d | promptless: gate-rule %d, token-rule %d | grandfathered %d" % (len(pty), len(gate_pl), len(tok_pl), len(gf)))
    print("   token-rule promptless NOT grandfathered (what a token classifier would NAME): %s" % (sorted(tok_pl - gf) or "none"))
    print("   gate-rule  promptless NOT grandfathered: %s" % (sorted(gate_pl - gf) or "none"))
    print("   classified differently by the two rules: %s" % (sorted(gate_pl ^ tok_pl) or "none"))
    if tok_err: print("   tokenize errors (listed promptless, fail-closed): %s" % tok_err)
    print("   whole-buffer sites over pty-driving code lines: LINES %d, OCCURRENCES %d" % (lines, occ))
