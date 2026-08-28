"""Mutant applier for #489 table 5.  NO SHELL ESCAPING ANYWHERE.

The three mutants this replaces (M8/M9/M10) all failed with "MUTANT TEXT NOT FOUND"
in table 4, because their anchors were written through a
  bash -> heredoc -> python -> heredoc -> python
chain and one backslash level was consumed: `cat -A` showed real TABs and a real
newline inside a Python string literal, which is a SyntaxError.

The carrier's rule is not "count the levels more carefully", it is: build any
backslash that must survive with chr(92), or avoid the chain.  This file avoids the
chain -- it is a real file, read by python directly, with no shell in between.

TAB = chr(9) is spelled explicitly for the same reason: a literal tab in source is
invisible and survives copy-paste badly.
"""
import sys

TAB = chr(9)
NL = chr(10)

GUARD = (TAB + TAB + "if (d->cnt != 408) {" + NL +
         TAB + TAB + TAB + "if (!(d->warned & GDROM_W_TOCLEN)) {")


def apply(path, new_guard_line):
    src = open(path).read()
    if src.count(GUARD) != 1:
        sys.stderr.write("ANCHOR NOT UNIQUE: %d occurrences\n" % src.count(GUARD))
        return 1
    new = (TAB + TAB + new_guard_line + NL +
           TAB + TAB + TAB + "if (!(d->warned & GDROM_W_TOCLEN)) {")
    open(path, 'w').write(src.replace(GUARD, new, 1))
    return 0


if __name__ == "__main__":
    which = sys.argv[1]
    target = sys.argv[2]
    forms = {
        #  exempt-zero: cnt==0 is ACCEPTED -> alloc_data(0) -> malloc(0) and the
        #  writer stores through byte 407.  Re-opens the round's own heap overflow.
        "M8": "if (d->cnt != 408 && d->cnt != 0) {",
        #  lower-bound: cnt >= 409 is ACCEPTED.  No overflow, but the guard now
        #  admits lengths it must refuse -- 65,527 of 65,536 inputs change meaning.
        "M9": "if (d->cnt < 408) {",
        #  latch-state collapse: the latch bit gates the GUARD, not just the message.
        #  First bad TOC declines; every one after it reaches alloc_data().
        "M10": "if (d->cnt != 408 && !(d->warned & GDROM_W_TOCLEN)) {",
    }
    sys.exit(apply(target, forms[which]))
