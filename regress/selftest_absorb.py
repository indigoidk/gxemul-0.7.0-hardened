#!/usr/bin/env python3
"""Pure-function selftest for drive_guest.split_stream() -- the pty record parser.

WHY THIS FILE EXISTS. Gate 5 can only observe drive_guest.py's OUTPUT: the markers it found,
the values it read, the reason it stopped. It therefore CANNOT REACH the parser at all, and a
measure seat quantified the consequence -- 13 of 18 driver mutants survive every gate row.
Canned streams through the real function kill most of them, in milliseconds, with no boot.

IT CALLS THE SHIPPED FUNCTION. A re-implementation here would test the copy and leave the
real code unguarded, which is the "a row guards a different instance than it appears to" trap
that has already cost this harness two rounds.

WHAT THE PARSER MUST DO, and every one of these was a real defect or a real near-miss:
  * a record spliced MID-TOKEN must rejoin the guest's line, because the record carries no
    leading newline and lands at the cursor. Anchoring the strip yields `SH77` for
    `HITACHI SH7751R` -- a WRONG ANSWER that reads as an SH4 emulation defect, not a miss;
  * a record SPLIT ACROSS TWO READS must not corrupt anything, at any offset;
  * a bracket-complete but UNTERMINATED record must be held, not consumed -- consuming it
    was the shipped defect, reachable at 1 of 138 LF offsets and 2 of 81 CRLF;
  * a guest line containing a bare '[' must never be swallowed or held forever.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drive_guest import split_stream, REC, HOLD_MAX   # the SHIPPED objects

FAILS = 0
ROWS = 0


def check(name, got, want):
    global FAILS, ROWS
    ROWS += 1
    if got == want:
        print("  ok    %-58s" % name)
    else:
        FAILS += 1
        print("  FAIL  %-58s\n          got  %r\n          want %r" % (name, got, want))


def feed(chunks):
    """Run chunks through the real parser; return (console_text, final_tail, last_count)."""
    tail, out, n = "", [], None
    for c in chunks:
        chunk, tail, got = split_stream(tail, c)
        out.append(chunk)
        if got is not None:
            n = got
    return "".join(out), tail, n


REC_LF = ("[ 33554432 instrs; i/s=63000000 avg=63000000; "
          "pc=0x8c0011f4 <sched_idle+0x8c>]\n")
REC_CRLF = REC_LF[:-1] + "\r\n"

print("--- A. a record spliced mid-token must rejoin the guest's line ---")
for label, rec in (("LF", REC_LF), ("CRLF", REC_CRLF)):
    text = "shpcic0 at mainbus0: HITACHI SH77" + rec + "51R, rev 1\n"
    body, tail, n = feed([text])
    check("%s: whole read, line rejoined" % label, body + tail,
          "shpcic0 at mainbus0: HITACHI SH7751R, rev 1\n")
    check("%s: count parsed" % label, n, 33554432)

print("--- B. SPLIT AT EVERY OFFSET -- the case no regex alone survives ---")
for label, rec in (("LF", REC_LF), ("CRLF", REC_CRLF)):
    text = "shpcic0 at mainbus0: HITACHI SH77" + rec + "51R, rev 1\n"
    ideal = "shpcic0 at mainbus0: HITACHI SH7751R, rev 1\n"
    bad = []
    for cut in range(1, len(text)):
        body, tail, _ = feed([text[:cut], text[cut:]])
        if body + tail != ideal:
            bad.append(cut)
    check("%s: no split offset corrupts the line (of %d)" % (label, len(text) - 1), bad, [])

print("--- C. byte-at-a-time, the most hostile chunking there is ---")
text = "cpu0: HITACHI SH77" + REC_LF + "51R\n"
body, tail, n = feed(list(text))
check("byte-at-a-time: line intact", body + tail, "cpu0: HITACHI SH7751R\n")
check("byte-at-a-time: count parsed", n, 33554432)

print("--- D. an unterminated record must be HELD, never consumed ---")
# This is the shipped defect: with an optional terminator the record matched the instant ']'
# arrived, the hold emptied, and the newline arrived next read as console text.
body, tail, n = feed(["cpu0: HITACHI SH77[ 33554432 instrs; x]"])
check("bracket-complete, no newline: nothing leaked to console", body, "cpu0: HITACHI SH77")
check("bracket-complete, no newline: held for the next read", tail, "[ 33554432 instrs; x]")
body2, tail2, n2 = feed(["cpu0: HITACHI SH77[ 33554432 instrs; x]", "\n51R\n"])
check("...and resolves correctly when the newline arrives",
      body2 + tail2, "cpu0: HITACHI SH7751R\n")
check("...with the count picked up", n2, 33554432)

print("--- E. guest text containing '[' must survive untouched ---")
for name, s in (("bracketed word", "mem [avail] 64MB\n"),
                ("bare '[' then newline", "weird [ thing\nnext\n"),
                ("gxemul's OTHER bracketed messages",
                 "[ using 516580 bytes of bsd ELF symbol table ]\n")):
    body, tail, n = feed([s])
    check("preserved: %s" % name, body + tail, s)
    check("...and no count invented: %s" % name, n, None)

print("--- F. the hold is BOUNDED -- a '[' must not stall the buffer forever ---")
# *** THE LENGTH IS A LITERAL, DELIBERATELY. *** This row first read
# "[" + "x" * (HOLD_MAX + 10), building its fixture from the very constant it was pinning --
# so raising HOLD_MAX to 1e9 grew the fixture too and the mutant survived. A fixture derived
# from the thing under test moves with it and pins nothing. 400 > the shipped 256 and is far
# beyond the longest record ever observed (106 chars).
body, tail, _ = feed(["[" + "x" * 400])
check("a 400-char '[' run is released, not held (HOLD_MAX must stay sane)", tail, "")
check("HOLD_MAX is within the range the measurements justify",
      106 < HOLD_MAX <= 400, True)
body, tail, _ = feed(["[ 33554432 inst", "rs; y]\n"])
check("a genuine record split mid-word still parses", body + tail, "")

print("--- I. the hold must start at the LAST '[', not the first ---")
# `rfind` -> `find` survived every other row: with `find`, an earlier bracket that already has
# its newline suppresses the hold, and the REAL partial record behind it leaks to the console.
body, tail, _ = feed(["mem [avail] 64MB\ncpu0: SH[ 33554432 inst", "rs; z]\n7751R\n"])
check("an earlier resolved '[' does not suppress the hold",
      body + tail, "mem [avail] 64MB\ncpu0: SH7751R\n")

print("--- J. a record body must not span past its own ']' ---")
# `[^\]]*` -> `.*` survived everything: a greedy body eats from the first '[' to the LAST ']'
# on the line, swallowing whatever guest text sits between two records.
two = "cpu0: A[ 100 instrs; p]\nMIDDLE[ 200 instrs; q]\nB\n"
# NOTE the expected value, which this row got wrong first time: each record takes its own
# trailing newline with it -- that is the whole point of the strip, since eating the newline
# is what rejoins a line the record split. So both newlines vanish along with their records.
body, tail, n = feed([two])
check("two records keep the guest text between them",
      body + tail, "cpu0: AMIDDLEB\n")
same_line = "X[ 100 instrs; p]\nKEEP[ 200 instrs; q]\n"
body, tail, _ = feed([same_line])
check("greedy body would swallow KEEP; it must not", body + tail, "XKEEP")

print("--- G. records back to back, and the LAST count is the one kept ---")
body, tail, n = feed(["a" + REC_LF.replace("33554432", "100") +
                      "b" + REC_LF.replace("33554432", "200") + "c\n"])
check("both records stripped", body + tail, "abc\n")
check("last count wins", n, 200)

print("--- H. the shipped regex must REQUIRE the terminator ---")
# Guards the exact character whose absence was the defect. If REC ever matches a record with
# no trailing newline again, this row goes red without needing a stream at all.
check("REC does not match an unterminated record",
      bool(REC.search("[ 33554432 instrs; q]")), False)
check("REC matches a terminated one", bool(REC.search("[ 33554432 instrs; q]\n")), True)
# A GREEDY body (`.*` for `[^\]]*`) survived every stream row, because `.` does not cross
# newlines -- so two records on SEPARATE lines behave identically under both. The only
# discriminating input is two records on ONE line: a greedy body runs from the first '[' to
# the LAST ']' and reports the FIRST count for the whole span.
m = REC.search("[ 100 instrs; p][ 200 instrs; q]\n")
check("REC body stops at its own ']' rather than the line's last",
      m.group(1) if m else None, "200")

print("\n%d rows, %d failures" % (ROWS, FAILS))
print("SELFTEST_ABSORB_%s" % ("PASS" if FAILS == 0 else "FAIL"))
sys.exit(1 if FAILS else 0)
