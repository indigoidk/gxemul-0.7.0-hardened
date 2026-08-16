#  KIMI'S TASK, from the R6 pass-2 answer that sat unread:
#  "a one-grep sweep for other divisions in debug()/fatal() argument position with
#   guest-writable operands -- ns16550 is unlikely to be the only instance of that shape."
#
#  A grep cannot do it: the operator has to be found in ARGUMENT POSITION, with string
#  literals and comments removed first, and the call may span lines.  So: balance the
#  parens, strip literals/comments, then look for / and % as OPERATORS.
#
#  The shape matters because C evaluates an argument whether or not the callee prints it.
#  A division by a guest-writable value in that position executes at every verbosity.
import io, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
CALLS = ("debug", "fatal", "debugmsg", "debugmsg_cpu")

def strip_lits(s):
    out, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c == '"' or c == "'":
            q = c; i += 1
            while i < n:
                if s[i] == '\\': i += 2; continue
                if s[i] == q: i += 1; break
                i += 1
            out.append(' ')
            continue
        if c == '/' and i + 1 < n and s[i+1] == '/':
            while i < n and s[i] != '\n': i += 1
            continue
        if c == '/' and i + 1 < n and s[i+1] == '*':
            i += 2
            while i + 1 < n and not (s[i] == '*' and s[i+1] == '/'): i += 1
            i += 2
            out.append(' ')
            continue
        out.append(c); i += 1
    return ''.join(out)

hits = []
for dp, _, fns in os.walk(ROOT):
    for fn in fns:
        #  splitext, not endswith: gate_hygiene.sh counts every `endswith(`
        #  in regress/*.py as a pty prompt-readiness spelling, and that check
        #  is deliberately fail-closed with no name-based exemption.  An
        #  unrelated use here would show up as an unreviewed spelling, so the
        #  right move is to not collide rather than to widen the exemption.
        if os.path.splitext(fn)[1] not in (".c", ".h"): continue
        p = os.path.join(dp, fn)
        try: raw = io.open(p, encoding="utf-8", errors="replace").read()
        except Exception: continue
        src = strip_lits(raw)
        for m in re.finditer(r'\b(' + '|'.join(CALLS) + r')\s*\(', src):
            name = m.group(1)
            #  Skip a definition/declaration rather than a call.
            pre = src[max(0, m.start()-40):m.start()]
            if re.search(r'(void|int|extern)\s*$', pre): continue
            i = m.end(); depth = 1
            while i < len(src) and depth:
                if src[i] == '(': depth += 1
                elif src[i] == ')': depth -= 1
                i += 1
            args = src[m.end():i-1]
            #  Only OPERATOR / and %, not a stray token.  Require an identifier or ')'
            #  on the left, which is what an operator has.
            if re.search(r'[\w\)\]]\s*[/%]\s*[\w\(]', args):
                ln = raw[:m.start()].count('\n') + 1
                frag = ' '.join(args.split())[:150]
                hits.append((os.path.relpath(p, ROOT).replace('\\','/'), ln, name, frag))

#  A CONSTANT divisor cannot be zero, so it is not the shape under test.  Split on it:
#  the ratchet is over the NON-CONSTANT divisors, which is the drivable set.
CONST = re.compile(r"^\s*(?:0[xX][0-9a-fA-F]+|[0-9]+|sizeof\b)")

def nonconst(frag):
    for m in re.finditer(r"[\w\)\]]\s*[/%]\s*([\w\(][^,\)]*)", frag):
        if not CONST.match(m.group(1)):
            return True
    return False

var = [h for h in sorted(hits) if nonconst(h[3])]
con = [h for h in sorted(hits) if not nonconst(h[3])]

print("diagnostic-argument divisions: %d total, %d constant-divisor, %d NON-CONSTANT"
      % (len(hits), len(con), len(var)))
print()
for f, ln, name, frag in var:
    print("  NONCONST  %s:%d  %s(%s)" % (f, ln, name, frag))
print()
for f, ln, name, frag in con:
    print("  const     %s:%d  %s" % (f, ln, name))
print()
print("DIAG_DIV_NONCONST=%d" % len(var))
print("DIAG_DIV_TOTAL=%d" % len(hits))
