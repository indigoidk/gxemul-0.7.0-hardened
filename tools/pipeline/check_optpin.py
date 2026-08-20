#!/usr/bin/env python3
"""DOES EVERY DIFFERENTIAL THAT MEASURES A RESOURCE PIN THE OPTIMISATION IT DEPENDS ON?

WHY THIS EXISTS.  `diff_memory_rw.c` asserts "the split is a loop, not recursion" by MEASURING
STACK GROWTH.  gcc 15.2.1 eliminates the tail call at -O2, so the recursion mutant measured
96 bytes and **the row PASSED under the exact defect it existed to catch**.  One flag on that
differential's compile line -- `-fno-optimize-sibling-calls` -- makes it real: loop 0 bytes,
recursion 1,572,768.

That is the `constblind` shape one level down.  Where `constblind` is a row following the
CONSTANT, this is a row following the COMPILER.  The ledger row `optrow` asked for an AUDIT of
"every other row in regress/ that measures stack, allocations or iteration counts".

*** THE AUDIT WAS DONE AND ITS ANSWER IS "memory_rw IS THE ONLY ONE" -- AND THAT ANSWER GOES
STALE. ***  Four other differentials mention "stack" and every mention is PROSE: descriptions
of the SUBJECT's stack use, or of an argument that must not be a stack array.  None measures a
resource.  But there were SEVEN differentials at the last such audit and there are THIRTEEN
now, and tonight a five-seat panel voted to drop a row on the strength of a stale audit
sentence.  An audit is a claim with a shelf life; a check is not.

------------------------------------------------------------------------------------------
*** WHAT IT DETECTS, AND THE BLINDNESS IS THE IMPORTANT HALF. ***

It looks for the STACK-WATERMARK IDIOM specifically -- a file that takes the address of a
local into a static high/low watermark (`sp_lo`/`sp_hi`, `&probe`, a `uintptr_t` pair) -- and
requires that differential's compile line in `gate_offline.sh` to carry an optimisation pin
(`-fno-...`, `-O0` or `-O1`).

It CANNOT detect "measures a resource" in general.  An allocation counter, an iteration count,
or a timing loop would all slip past, and a future row could measure stack by some idiom this
does not know.  **So a green line here means "no UNPINNED file uses the idiom that has actually
bitten", never "no row follows the compiler".**  That distinction is this project's newest
named vacuity class -- a check whose blindness is reported as a green line -- so the blindness
is printed on every run, pass or fail.

The honest alternative -- a human re-audit whenever a differential is added -- is exactly what
went stale.  This catches the one shape that has cost a real false pass, and says plainly that
it catches only that.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEC = os.path.normpath(os.path.join(HERE, "..", ".."))
REG = os.path.join(SEC, "regress")
GATE = os.path.join(REG, "gate_offline.sh")

#  The stack-watermark idiom: a static uintptr_t pair, or an address-of-local probe feeding one.
WATERMARK = re.compile(r"\bsp_lo\b|\bsp_hi\b|uintptr_t\s*\)\s*&\s*\w+|&\s*probe\b")
PIN = re.compile(r"-fno-[a-z-]+|(?<!\w)-O[01](?!\w)")


def compile_line_for(stem, gate_text):
    """Return the gate's compile invocation for diff_<stem>.c, or None."""
    #  Compile lines name the harness file; take the surrounding continued command.
    needle = "diff_%s.c" % stem
    out = []
    for i, line in enumerate(gate_text.split("\n")):
        if needle not in line:
            continue
        #  walk backwards to the start of the command, forwards to its end
        lines = gate_text.split("\n")
        j = i
        while j > 0 and lines[j - 1].rstrip().endswith("\\"):
            j -= 1
        k = i
        while lines[k].rstrip().endswith("\\") and k + 1 < len(lines):
            k += 1
        chunk = " ".join(lines[j:k + 1])
        if "$CC" in chunk or "gcc" in chunk:
            out.append(chunk)
    return out


def main(argv):
    gate = io.open(GATE, encoding="utf-8", newline="").read()
    diffs = sorted(f for f in os.listdir(REG)
                   if f.startswith("diff_") and f.endswith(".c"))

    measured, bad = [], []
    for fn in diffs:
        s = io.open(os.path.join(REG, fn), encoding="utf-8",
                    errors="replace", newline="").read()
        #  Strip block comments so PROSE about stack does not count as a measurement.
        code = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
        if not WATERMARK.search(code):
            continue
        stem = fn[5:-2]
        measured.append(stem)
        chunks = compile_line_for(stem, gate)
        pinned = any(PIN.search(c) for c in chunks)
        #  the selfmutant lane compiles it too, via extra flags
        if not pinned:
            sm = re.search(r"^selfmutant_one\s+%s\s+.*$" % re.escape(fn), gate, re.M)
            if sm and PIN.search(sm.group(0)):
                pinned = True
        if not pinned:
            bad.append(stem)
        print("  %-22s measures stack   pin: %s"
              % (stem, "yes" if pinned else "*** NONE ***"))

    if not measured:
        print("  no differential uses the stack-watermark idiom")

    print()
    print("  %d of %d differentials measure stack by the known idiom" % (len(measured), len(diffs)))
    print("  BLINDNESS, printed every run: this detects the STACK-WATERMARK idiom ONLY.")
    print("  An allocation counter, an iteration count, a timing loop, or a future stack")
    print("  idiom would all slip past.  A green line means 'no UNPINNED file uses the shape")
    print("  that has actually bitten' -- NEVER 'no row follows the compiler'.")

    if bad:
        print()
        print("OPTPIN_FAIL  %s measures a resource with no optimisation pinned" % ", ".join(bad))
        return 1
    print("OPTPIN_PASS  every resource-measuring differential pins its optimisation")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
