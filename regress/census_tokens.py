#!/usr/bin/env python3
"""census_tokens.py -- the TOKEN-level half of gate_hygiene.sh's readiness census (hygienecensus, 2026-09-23).

Why tokens.  The census's POSITIVE classifications -- "this probe has a prompt-readiness check", "this file holds N
whole-buffer sites" -- were line-level greps, and text on a code line that is not code counted as code: a trailing
comment, a string, a docstring.  Measured on the census round's F2 pass (the Opus seat): a probe whose only call of
the ends-with method was a trailing comment or a docstring was counted as prompt-detecting, and two whole-buffer sites
on ONE line counted as one.  Python's tokenizer separates COMMENT and STRING tokens from code, and every occurrence is
a separate match, so neither can happen here.  (A probe in a subdirectory judged by a same-named top-level file was
the third defect that pass measured; the GATE fixed that, by passing paths relative to regress/.)

Statement boundaries are KEPT.  The first version dropped NEWLINE tokens with the other layout tokens, so a method
REFERENCE on one statement and a parenthesised string on the next -- `x = buf.rstrip().endswith` / `("GXemul>")` --
read as one whole-buffer call, and a probe whose readiness test had been turned into that passed every row (measured by
the census closing pass, controls_c2/t_nljoin).  NL, the newline INSIDE brackets, is still layout.  And a call is
counted only where the name follows a "." -- a function DEFINITION under that name calls nothing, and the first
version credited one (codex, the same pass).  Tokens are not a parse: a class PATTERN of the same shape in a `match`
statement (`case K.<name>(...)`) is still counted, and a call through an alias with no "." before the name is not
(the F3 pass, codex).  The second fails closed -- the probe is listed promptless, if no other call of it is counted.
The first fails OPEN: a grandfathered probe that gains such a pattern reads as no longer promptless, and --release
then took it off the list with every row green (measured, the census F4 pass, the Opus seat; filed).  Since F6b the
deriver re-checks that decision with Python's own parser and refuses it.

The CLOSED-WORLD counts (a bare prompt-suffix test, an unrecognised spelling of the ends-with call) are NOT done here
and must not be: they count TEXT on code lines, in the gate itself, so a comment or a string that spells the method
is counted -- the safe direction.  They see only the literal spelling with no space before the parenthesis (a space
passes them: hygienecensusholes e9).  THIS FILE IS SCANNED BY THOSE COUNTS TOO (it is a top-level regress/*.py),
which is why the method's name never appears here followed directly by an opening parenthesis -- not in code, not in
this docstring.

Usage (paths are read one per line from stdin, relative to the directory given):
    census_tokens.py promptless DIR   print each path with no method call of the ends-with method: the OP token ".",
                                      a NAME token spelled ENDS_WITH, the OP token "(", in one statement.  A file that
                                      cannot be read or tokenized is PRINTED (listed promptless: it cannot be read, so it
                                      is not trusted).  Tokens are not a parse: a file that tokenizes but would not
                                      compile is graded like any other.
    census_tokens.py whole DIR        print "path:N" for each path with N > 0 code-level whole-buffer sites: a NAME
                                      whose last three letters are "buf", then ".", "rstrip", "(", ")", ".", ENDS_WITH,
                                      "(", a STRING whose value is exactly "GXemul>", ")", in one statement.  Counted
                                      per OCCURRENCE, either quote, any spacing between the tokens.  An unreadable file
                                      prints NOTHING here (it has no count); the promptless mode is what names it.
Exit status 2 on a usage error; otherwise 0 -- an unreadable path is an output (promptless) or a missing count (whole),
never an exception.  On Python 3.12 and later an f-string's replacement fields are tokenized as code, so a call inside
one counts; on earlier versions it is one STRING token and does not (no probe relies on either).
"""
import ast, io, os, sys, tokenize

ENDS_WITH = "ends" + "with"          # spelled in two halves: see the docstring's CLOSED-WORLD paragraph
SKIP = (tokenize.NL, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT, tokenize.ENCODING)   # NEWLINE is KEPT


def code_tokens(path):
    src = io.open(path, encoding="utf-8", errors="strict").read()
    return [t for t in tokenize.generate_tokens(io.StringIO(src).readline) if t.type not in SKIP]


def has_ends_with_call(toks):
    return any(d.type == tokenize.OP and d.string == "." and a.type == tokenize.NAME and a.string == ENDS_WITH
               and b.type == tokenize.OP and b.string == "("
               for d, a, b in zip(toks, toks[1:], toks[2:]))


def is_prompt_string(t):
    if t.type != tokenize.STRING:
        return False
    try:
        return ast.literal_eval(t.string) == "GXemul>"
    except (ValueError, SyntaxError):
        return False


SHAPE = [(tokenize.OP, "."), (tokenize.NAME, "rstrip"), (tokenize.OP, "("), (tokenize.OP, ")"), (tokenize.OP, "."),
         (tokenize.NAME, ENDS_WITH), (tokenize.OP, "("), (tokenize.STRING, None), (tokenize.OP, ")")]


def whole_sites(toks):
    n = 0
    for i in range(len(toks) - len(SHAPE)):
        head = toks[i]
        if head.type != tokenize.NAME or head.string[-3:] != "buf":
            continue
        rest = toks[i + 1:i + 1 + len(SHAPE)]
        if all(t.type == kind and (text is None or t.string == text) for (kind, text), t in zip(SHAPE, rest)) \
                and is_prompt_string(rest[7]):
            n += 1
    return n


def main(argv):
    if len(argv) != 3 or argv[1] not in ("promptless", "whole"):
        sys.stderr.write(__doc__)
        return 2
    mode, base = argv[1], argv[2]
    for line in sys.stdin.read().split("\n"):
        rel = line.strip("\r")
        if not rel:
            continue
        try:
            toks = code_tokens(os.path.join(base, rel))
        except (OSError, ValueError, UnicodeDecodeError, tokenize.TokenError, SyntaxError, IndentationError):
            if mode == "promptless":
                print(rel)
            continue
        if mode == "promptless":
            if not has_ends_with_call(toks):
                print(rel)
        else:
            n = whole_sites(toks)
            if n:
                print("%s:%d" % (rel, n))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
