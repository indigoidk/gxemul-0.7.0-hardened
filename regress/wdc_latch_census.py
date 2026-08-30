#!/usr/bin/env python3
#
#  CENSUS: the six named `warned_` latches in dev_wdc.c -- per-latch PRESENCE,
#  per-latch BALANCE, and the device's whole latch POPULATION -- counted over
#  comment-stripped code.
#
#  WHY THIS REPLACES A grep -c EQUALITY, and the pin it replaces refuted itself.
#  ---------------------------------------------------------------------------
#  `gate_sh_rounding.sh` pinned `grep -cE 'd->warned_(six|names|...)' == 12` and
#  its comment claimed immunity to growth, calling that THE WHOLE LESSON:
#
#      "it ENUMERATES SIX NAMED LATCHES in its regex instead of counting an open
#       set.  The device carries ELEVEN warned_ latches today; this pin still
#       reads 12 because growth cannot reach it."
#
#  It read 15.  Growth reached it by two routes the sentence did not consider,
#  and the claim survived under four hours:
#
#      05ec21e  14:00 2026-08-27   the immunity comment lands
#      cf300c0  17:59 2026-08-27   #484 adds a SECOND guarded site re-using
#                                  warned_inbuf_overrun            -> +2
#      d819188  19:29 2026-08-27   #485 adds a COMMENT naming
#                                  warned_unimpl_cmd               -> +1
#
#  MEMBERS was closed and correctly so.  OCCURRENCES was open: grep -c counts
#  LINES.  And TEXT-vs-CODE was never considered: prose counted as a guard.
#
#  *** A BARE FLOOR (>= 12) WAS PROPOSED AND MEASURED VACUOUS: deleting one
#  latch's two-line guard pair scores 13 and PASSES, restoring the unbounded
#  flood #464 fixed.  Six per-latch ">= 2" rows were also refuted -- ">= 2" is
#  satisfied by TWO READS AND NO SET. ***
#
#  *** AND THE FIRST VERSION OF *THIS* FILE WAS AN L2 FLOOR BREACH.  Measured on
#  pass 2, five escapes, the smallest ONE TOKEN. ***
#  ---------------------------------------------------------------------------
#  It reported per-latch PRESENCE only: does this latch have >= 1 set and >= 1
#  read?  Every mutant in its kill table happened to target a SINGLE-SITE latch,
#  so the table was clean on a population that structurally could not exhibit
#  the defect.  `warned_inbuf_overrun` has TWO sites -- the producer at :246 and
#  #484's consumer at :515 -- and neutralising EITHER ONE leaves the other to
#  satisfy presence:
#
#      if (!d->warned_inbuf_overrun) {   ->   if (1) {     at :246 only
#      => inbuf_overrun set=2 read=1, and the census still said SET=6 READ=6
#      => the producer flood is unbounded again and the gate is GREEN
#
#  Floor clause (b) demands failure on reinstatement at EVERY fixed site, so
#  that is L2, not coverage debt.  Note the inversion, which is the lesson: the
#  OLD pin counted OCCURRENCES, so a second site moved it -- loud and wrong but
#  alive.  Presence-only counting made losing one of two invisible -- quiet and
#  wrong and silent.
#
#  THE THREE ROWS THIS SHIPS, and why each is the shape it is:
#
#    SET / READ   per-latch PRESENCE.  Equality over the six NAMED members, a
#                 closed set that does not grow.  What broke was an equality
#                 over OCCURRENCES, which none of these count.
#    BALANCED     per-latch set_count == read_count.  RELATIONAL, so growth
#                 increments both sides and it is growth-invariant BY
#                 CONSTRUCTION -- not an equality against a frozen literal
#                 needing hand-bumps.  It is the tree's own house idiom: every
#                 latch is 1:1, and `inbuf_overrun` is 2:2.  Kills E1/E2.
#    DECL         how many warned_ latches the device DECLARES.  Replacing a
#                 decaying equality with a growth-immune one DELETES the
#                 accidental tripwire that announced latch growth -- the
#                 carrier's DE-ESCALATION CLAUSE one level up.  This restores
#                 it deliberately: a twelfth latch reds until someone looks.
#
#  HONEST COST, disclosed rather than discovered later: a latch legitimately
#  read twice and set once reds BALANCED.  That is the safe direction -- loud.
#
#  *** CONTRACT (vacuity floor clause (e)) -- WHAT THIS IS DESIGNED TO CATCH ***
#      IN  : a guard neutralised or deleted at any site of any of the six;
#            a SET or READ removed; a guard redirected to a different named
#            latch; latch text moved into a comment; a new latch declared.
#      OUT : a guard whose PREDICATE IS WIDENED while its text survives, e.g.
#            `!d->warned_X` -> `(!d->warned_X || len > 512)`.  Guard text and
#            set are both still present, so NO textual census can see it.
#            Measured as E4 on pass 2.  A later escape of that shape is
#            OUTSIDE THIS CONTRACT, not a breach of it.
#
#  Adjudicated 2026-08-29: proposed by the opus5 seat, adopted by the fable5
#  adjudicator over its own twelve-row alternative, then corrected by opus5's
#  own pass-2 review of its own design.
#
import io
import os
import re
import sys

LATCHES = ("inbuf_overrun", "inbuf_overread", "unimpl_cmd",
           "nonbyte_write", "nonbyte_read", "data_unexpected")

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = os.path.join(HERE, "..", "src", "devices", "dev_wdc.c")


def _blank(seg):
    """Replace a consumed span with spaces, KEEPING its newlines.

    Eating newlines here is the `divsweeplines` defect -- a stripper whose
    output no longer lines up with the raw file.  All three branches below use
    this, including the `//` one: an earlier version blanked that branch with
    `' ' * n`, which silently turned two lines into one.  A LENGTH check does
    not catch that (a space replaced the newline); only a LINE COUNT does.
    """
    return ''.join(chr(10) if ch == chr(10) else ' ' for ch in seg)


def strip_comments(s):
    """Remove C comments and string literals, preserving length AND lines.

    String-first ordering is deliberate: `/*` inside a string literal and `//`
    inside one must not open a comment.
    """
    out, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c == '"' or c == "'":
            st = i
            q = c
            i += 1
            while i < n:
                if s[i] == chr(92):
                    i += 2
                    continue
                if s[i] == q:
                    i += 1
                    break
                i += 1
            out.append(_blank(s[st:i]))
            continue
        if c == '/' and i + 1 < n and s[i + 1] == '/':
            #  C99 phase 2: a `//` comment ending in a backslash CONTINUES onto
            #  the next physical line.  Stopping at the first newline scored the
            #  continuation as CODE -- measured as E6, where one inserted line
            #  swallowed a real SET and the gate stayed green.
            st = i
            while i < n:
                if s[i] == chr(10):
                    j = i - 1
                    while j >= st and s[j] in ' \t':
                        j -= 1
                    if j >= st and s[j] == chr(92):
                        i += 1
                        continue
                    break
                i += 1
            out.append(_blank(s[st:i]))
            continue
        if c == '/' and i + 1 < n and s[i + 1] == '*':
            st = i
            i += 2
            while i + 1 < n and not (s[i] == '*' and s[i + 1] == '/'):
                i += 1
            i = min(i + 2, n)
            out.append(_blank(s[st:i]))
            continue
        out.append(c)
        i += 1
    return ''.join(out)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    try:
        raw = io.open(path, encoding="utf-8", errors="replace").read()
    except IOError:
        #  MISSING and EMPTY must not render the same -- this project's oldest
        #  rule about blanks.
        print("WDC_LATCH_FILE=MISSING")
        for k in ("SET", "READ", "BALANCED", "DECL"):
            print("WDC_LATCH_%s=0" % k)
        return 1

    code = strip_comments(raw)
    nset = nread = nbal = 0
    for l in LATCHES:
        s_hits = len(re.findall(r"d->warned_%s\s*=\s*1\s*;" % re.escape(l), code))
        #  ANCHORED: a bare substring lets a LONGER name satisfy a member's row
        #  -- `!d->warned_nonbyte_read_hi` scored the `nonbyte_read` READ and
        #  passed (measured as E8 on pass 2).  Require a non-identifier char.
        r_hits = len(re.findall(r"!d->warned_%s(?![A-Za-z0-9_])" % re.escape(l), code))
        nset += 1 if s_hits else 0
        nread += 1 if r_hits else 0
        nbal += 1 if (s_hits and s_hits == r_hits) else 0
        print("  %-18s set=%d read=%d %s"
              % (l, s_hits, r_hits, "balanced" if s_hits and s_hits == r_hits else "*** UNBALANCED ***"))

    decl = len(set(re.findall(r"warned_[A-Za-z0-9_]+", code)))
    print("WDC_LATCH_FILE=OK")
    print("WDC_LATCH_SET=%d" % nset)
    print("WDC_LATCH_READ=%d" % nread)
    print("WDC_LATCH_BALANCED=%d" % nbal)
    print("WDC_LATCH_DECL=%d" % decl)
    return 0


if __name__ == "__main__":
    sys.exit(main())
