#!/usr/bin/env python3
"""mutants_r14.py <name> <src> <dst> -- #529 repair 14: the mutants repair 14's OWN rows must kill.

Every other mutant table 12 needs already exists and is built (mutants8.py, mutants8b.py, the repair-14
seat's mutants14.py).  THIS FILE SUPPLIES THE ONE THAT DID NOT: the (d) DEPENDS-ON mutant for ACCEPTS
entry 14.

*** WHY IT HAD TO BE WRITTEN AT ALL: the CHANNEL rule says a row names the mutant it kills.  Entry 14's
repair moves `p acc ctl msg' from 3 to 4 -- and no mutant in the campaign declines the EIGHT-byte CONTROL
write, because the whole point of entry 14 is that the width axis was never covered there.  A row shipped
with no mutant is a row nobody has shown can fail. ***

    W_ctl8w   decline an EIGHT-byte CONTROL WRITE, post-latch only.  This is the width-axis (d) form: the
              guard keeps the 4-byte arm intact, so `p acc ctl msg' loses its two `sd' messages while the
              `sw' pair still print.  Keyed post-latch so the CLEAR twin's `acc ctl sd' is untouched, which
              makes the prediction a SHARP one rather than a sweep.

PREDICTED RED SET, traced through the sessions rather than guessed -- TWO rows, not one:
    p acc ctl msg   the POST session issues `sd 0x01' AND `sd 0x0201', both 8-byte CONTROL writes, so the
                    count falls 4 -> 2.
    rst 8w          rst_session("sd") writes 0x800 at CONTROL post-latch; declined, the CPUs do NOT stop,
                    the round trip after it RUNS, and v1 holds LIVE_VAL instead of the SENTINEL.
NOT red, and each is a check on the mutant rather than on the probe:
    p acc ctl ld / p acc ctl4r / p acc ctl0c   the guard carries `writeflag == MEM_WRITE', so reads are
                    untouched -- if any of these moves, the mutant is wider than intended.
    acc ctl sd      the CLEAR twin, untouched because the guard carries the latch term.
    rst 4w          the FOUR-byte halt still works, which is what makes this a WIDTH mutant and not a
                    CONTROL-write mutant.

Sentinel: APPLIED_R14 <name> <n edits>."""
import io
import sys

LEN8 = "\tif (len == 8) {\n"
L = "(d->warned & CRIME_W_LEN)"

M = {
    "base": [],
    "W_ctl8w": [(LEN8,
                 "\tif (len == 8 && relative_addr == CRIME_CONTROL &&\n"
                 "\t    writeflag == MEM_WRITE && %s)\n"
                 "\t\tgoto crime_declined;\n\n" % L + LEN8,
                 1)],
}

if len(sys.argv) == 2 and sys.argv[1] == "list":
    print(" ".join(sorted(M)))
    sys.exit(0)

if len(sys.argv) != 4:
    print(__doc__)
    sys.exit(2)

name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
if name not in M:
    print("unknown mutant %r; known: %s" % (name, " ".join(sorted(M))))
    sys.exit(2)

txt = io.open(src, encoding='utf-8', newline='').read()
n = 0
for find, repl, want in M[name]:
    got = txt.count(find)
    if got != want:
        #  A find-text that does not match EXACTLY as expected is a FAIL, never a silent skip: that turns
        #  every anchor into a PRESENCE PIN on the feature it edits.
        print("ANCHOR MISMATCH in %s: expected %d occurrence(s), found %d" % (name, want, got))
        sys.exit(1)
    txt = txt.replace(find, repl, want)
    n += want

#  newline='' IS LOAD-BEARING: without it, Windows Python translates every LF to CRLF and the mutant
#  differs from its source in EVERY LINE -- which makes the diff unreadable and would defeat a
#  hunk-for-hunk cross-check against a preserved diff.  It behaves under WSL by luck, not by design.
io.open(dst, "w", encoding='utf-8', newline='').write(txt)
print("APPLIED_R14 %s (%d edit(s))" % (name, n))
