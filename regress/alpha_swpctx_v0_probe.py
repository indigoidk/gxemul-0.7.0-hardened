#!/usr/bin/env python3
"""alpha_swpctx_v0_probe.py -- does PAL_OSF1_swpctx return the old context in v0?

    usage:  alpha_swpctx_v0_probe.py <gxemul-binary> [label]

WHAT THIS PINS.  `cpu_alpha_palcode.c' handles `call_pal 0x30' (PAL_OSF1_swpctx).  Its own
comment says "Return old context in v0."; the line under that comment writes ALPHA_A0.  The
third-party ABI wrapper `alpha_pal_swpctx' (alpha_cpu.h) declares `v0 __asm("$0")' as an
OUTPUT and lists a0 as clobbered -- so a correct guest reads the result from v0 and must not
rely on a0.  The model therefore publishes its result into the register the caller is told to
discard, and leaves untouched the one the caller reads.

THE ORACLE NEEDS THREE DISTINGUISHABLE VALUES, and a row asserting only "v0 changed" would
pass an incorrect repair that returned the NEW context instead of the old one:

    C = 0x01000000   the OLD context, established by a first swpctx call
    N = 0x01010000   the NEW context, passed to the second call
    S = 0x00ab0000   a sentinel seeded into v0 immediately before the second call

    v0 == C  ->  correct                     (what this probe asserts)
    v0 == S  ->  the handler never wrote v0  (the shipped defect)
    v0 == N  ->  an incorrect repair returning the new context instead of the old

ORACLE POLARITY, per the witness ladder: the row asserts the CORRECT behaviour, so it is RED
on the pre-fix build and GREEN post-fix with the SAME script.

THE ATTRIBUTION CONTROL is the row that makes this a witness rather than a value check.
`a0 land' reads a0 after the second call.  On the shipped build a0 holds C -- which proves
THE HANDLER RAN AND WROTE THE WRONG REGISTER, and separates that from "the handler never
executed", which would leave a0 holding N and v0 holding S.  One observation, two hypotheses
distinguished.

THE CONTRACT -- what this probe is designed to catch, and what it deliberately is not.

CAUGHT: the shipped defect (v0 never written); any repair that returns the NEW context instead
of the old; and any repair that publishes the OLD context into a0.  NOT CAUGHT, and disclosed
rather than discovered later: this probe does NOT assert that the new context was actually
INSTALLED.  Raised independently by deepseek and kimi on the pass-2 panel; filed as coverage
debt rather than fixed here, because it is a different part of the handler from the fix's own
repair and so is not a clause-(d) breach.  The row that would close it: a THIRD swpctx call,
which should return N as its old context.
[#556, 2026-10-02 -- a records correction; the text above is kept as it was written] a0 obs checks that a0 was read,
so v0=C with a0=C scores 6/6. The line 399 note fires on that permitted pair.  (regress22:F7:
regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
[#556, 2026-10-02 -- a records correction; the text above is kept as it was written] A third swpctx still returns N
when ctx=a0 is kept and the PCB loads are omitted, which is also what correct code returns.  (regress22:F9:
regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)

*** AND THE HOLE AS FIRST WRITTEN WAS OVERSTATED, which kimi caught on the NEXT pass. ***  It
said "an edit breaking the subsequent load-new-context block would score full marks".  That is
FALSE of a WHOLESALE break, because `cpu->cd.alpha.ctx = a0;' is the FIRST statement inside
that block: delete the block and `ctx' never advances, so call 2 publishes the STALE context
and `v0 ctx' REDS.  **Only a PARTIAL break that spares the `ctx = a0' bookkeeping -- killing,
say, the PCB field loads alone -- sweeps clean.**  Source-derived from the block's own layout,
not measured.  *A disclosure that overstates its hole is a wrong record in the direction that
looks humble, which is why it survived a pass.*

ALSO NOT CAUGHT, named by grok on the pass-2 panel: a product edit that HARDCODES the planted
value -- `cpu->cd.alpha.r[ALPHA_V0] = 0x01000000;' -- scores 4/4 here.  Filed rather than chased,
and the reason is the bound: the contract is "the OLD context in v0", the planted C is ONE old
context, and rowing every RHS that happens to equal C for this one pair is the unbounded shape.
The hole is NAMED so a later escape is "outside the contract" rather than a surprise.

*** THE ANCHOR WAS ALSO CHECKED FOR BEING TOO STRICT -- AND MY FIRST CHECK OF THAT WAS AN
OVERCLAIM, REFUTED BY A SEAT WITH A MEASUREMENT. ***  I captured ONE live session
(REGEX_REALSHAPE_20260908.out), found the plain response shape, saw the anchored and loose forms
return the SAME three responses, and wrote that the anchor "rejects nothing genuine that this
debugger emits today".

**That was true of ONE ENVIRONMENT and I stated it universally.**  With CLICOLOR set the prompt is
wrapped in ANSI escapes and the anchor matches NOTHING -- measured at 53 escapes and ZERO parsed
responses, a CORRECT build scoring 1/5.  The seat's phrasing is the one to keep: the artifact
establishes the plain response shape; it does not support the accompanying universal claim.

**Closed by passing `-A` at launch**, which removes the dependence rather than widening the
pattern to chase it.  Whitespace and hex case are widened too, because a parser that fails CLOSED
on a genuine response is still a defect.

WHAT `v0 bound' PROVES IS ORDER, NOT PROVENANCE -- a pass-5 seat's precision and it is worth
keeping.  The rule establishes that a v0-shaped response follows a unique second-step echo and is
the second such response.  It does NOT establish that the line is the debugger's answer to the
second `print v0' rather than a correctly-placed replay.  Both genuine reads in a passing run carry
the same value, so no row here can distinguish those.  **The claim the row is entitled to is
positional, and the note says so.**
[#556, 2026-10-02 -- a records correction; the text above is kept as it was written] The first swpctx returns the
initial context 0x10100. The second returns 0x1000000.  (regress22:F8:
regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)

THIS PROBE DOES NOT SCORE a0's VALUE AT ALL.  `a0 obs' scores only that the observation was
MADE; the value is printed as diagnostic.  Two measured findings forced that: scoring `a0 != C'
passed a MISSING observation, and it also failed a PERMITTED implementation that copies the
result into a0 as well.  The defect is caught by `v0 ctx' alone.

THIS PROBE DOES NOT PIN a0's VALUE ON A CORRECT BUILD.  The architecture marks a0
UNPREDICTABLE after the call; only the negative claim -- a0 does not receive the old context --
is owed.  See `a0 land' below for the measurement that established this.

WHY THE PROGRAM RELOADS ITS SCRATCH POINTER.  T0 is Alpha t0, which the wrapper's own clobber
list names.  Whether this model clobbers it is not the point: the guest program is written to
be correct under the ABI, not under the model's current behaviour.
"""
import os, sys, pty, select, time, re

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
MACH  = "alphabook1"

rows = []
def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-14s %-22s %-22s %-56s %s" % (name, str(got), str(want), note,
                                          "ok" if ok else "FAIL"))
    return ok

# ---------------------------------------------------------------- encoder (memory format only)
ZERO, T0 = 31, 1
A0, V0 = 16, 0

def mem(op, ra, rb, disp):
    assert -32768 <= disp <= 32767, "displacement %d out of range" % disp
    return (op << 26) | (ra << 21) | (rb << 16) | (disp & 0xffff)

def LDA (ra, disp, rb=ZERO): return mem(0x08, ra, rb, disp)
def LDAH(ra, disp, rb=ZERO): return mem(0x09, ra, rb, disp)
def LDQ (ra, disp, rb):      return mem(0x29, ra, rb, disp)
def CALL_PAL(func):          return (0x00 << 26) | (func & 0x3ffffff)

def load_const(reg, val):
    lo, hi = val & 0xffff, (val >> 16) & 0xffff
    if lo >= 0x8000:
        hi = (hi + 1) & 0xffff
    ops = [LDAH(reg, hi if hi < 0x8000 else hi - 0x10000)]
    if lo:
        ops.append(LDA(reg, lo if lo < 0x8000 else lo - 0x10000, reg))
    return ops

# ---------------------------------------------------------------- addresses (ALL RAM < 64 MB)
K0SEG   = 0xfffffc0000000000
def k0(p): return K0SEG | p

SCRATCH = 0x01020000
CODE    = 0x01040000
CTX_C   = 0x01000000          # the OLD context -- a PCB the first call installs
CTX_N   = 0x01010000          # the NEW context
SENT    = 0x00ab0000          # the sentinel seeded into v0; LDAH(0xab) builds it exactly
PAL_SWPCTX = 0x30

assert max(SCRATCH, CODE, CTX_C, CTX_N) < 64 * 1024 * 1024, "everything must be inside RAM"
assert len({CTX_C, CTX_N, SENT}) == 3, "the three oracle values must be distinguishable"

DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alpha_dummy.bin")
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 8)

# ---------------------------------------------------------------- session
def session(cmds, settle=1.6, spin=2.2):
    pid, fd = pty.fork()
    if pid == 0:
        #  *** `-A' IS LOAD-BEARING FOR THE PARSER, AND ITS ABSENCE WAS A MEASURED FALSE
        #  FAIL. ***  `use_colorized_output()' (core/misc.c) gates on isatty(STDIN) &&
        #  isatty(STDOUT), and a pty satisfies BOTH -- so with CLICOLOR set the prompt
        #  arrives wrapped in ANSI escapes and no anchor beginning "^GXemul>" can match.
        #  MEASURED: CLICOLOR=1 without `-A' gives 53 escapes and ZERO parsed responses,
        #  so a CORRECT build scores 1/5; with `-A' it is 0 escapes and 5/5.  `-A' sets
        #  enable_colorized_output = false (core/main.c:317).  Found by a pass-4 seat.
        os.execv(BIN, [BIN, "-V", "-x", "-A", "-E", "alpha", "-e", MACH, "-M", "64",
                       "0x20000000:" + DUMMY])
        os._exit(127)
    buf = ""
    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.1)
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
                if not d:
                    return False
                buf += d.decode("latin-1", "replace")
            except OSError:
                return False
        return True
    alive = rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            alive = False; break
        if not rd(spin if i == len(cmds) - 1 else 0.35):
            alive = False; break
    try:
        os.write(fd, b"quit\n"); rd(0.4)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    return buf.replace("\r", ""), alive

#  *** THE LOOSE FORM OF THIS REGEX PRODUCED THREE MEASURED CLEAN SWEEPS, found by a seat that
#  exercised the scorer against 31 SYNTHETIC TRANSCRIPTS rather than reading it. ***  It was
#  `print\s+REG\s*\n\s*(0x..)' with `re.search', and it accepted all of:
#
#      "trace: print v0\n0x1000000"      a TRACE LINE, not a response -- and it can SUBSTITUTE
#                                        for a genuinely missing one, so the count still says 2
#      "sprint v0\n0x1000000"            `sprint' matched because nothing anchored the word
#      "0x1000000: diagnostic"           a value with trailing text
#
#  Anchoring on the PROMPT and requiring the value to be the whole line rejects all three: a real
#  response is always `GXemul> print <reg>' followed by a line that is exactly a hex number.
#  Whitespace is [ \t] and hex is case-insensitive: two pass-4 seats named those
#  independently as over-tight.  Neither occurs in this debugger today, but a parser
#  that fails CLOSED on a genuine response is still a defect, and widening costs
#  nothing -- the prompt anchor and the whole-line requirement do the real work.
RESP = r"^GXemul>[ \t]+print[ \t]+%s[ \t]*\n[ \t]*(0[xX][0-9a-fA-F]+)[ \t]*$"

def responses(t, reg):
    """Every genuine `print <reg>' response, in order.  Anchored, so a trace line or a
       lookalike command cannot supply one."""
    return re.findall(RESP % reg, t, re.M)


def responses_at(t, reg):
    """(value, offset) for every genuine response -- the offset is what lets a caller bind an
       observation to the STEP it followed."""
    return [(m.group(1), m.start()) for m in re.finditer(RESP % reg, t, re.M)]


#  *** BINDING THE OBSERVATION TO ITS STEP, and it closes the last two escapes a pass-4 seat
#  reported. ***  Anchoring fixed the SHAPE of a response; it cannot fix the ORDER.  Two variants
#  still swept 5/5: a second read moved BEFORE the second step, and the first response REPLAYED as
#  the second.  Both are correctly-formed responses in the wrong place, so no pattern over a single
#  response can reject them -- what distinguishes them is WHERE they sit relative to the second
#  `step'.  This finds that command's own echo and requires the second observation to follow it.
def step_marker(t, nsteps):
    """Every occurrence of the `step <nsteps>' command echo, as (start, end) offsets.
       Whole-token: a plain find() also matches `step 40' and `step 4 extra'."""
    return [(m.start(), m.end())
            for m in re.finditer(r"^GXemul>[ \t]+step[ \t]+%d[ \t]*$" % nsteps, t, re.M)]


def bound_second(t, reg, nsteps):
    """The SECOND genuine <reg> response, required to sit AFTER a UNIQUE `step <nsteps>' echo.

       *** THIS COMPOSES TWO RULES THAT EACH LET THE OTHER'S ESCAPES THROUGH, AND A SEAT MEASURED
       BOTH FAILURES OVER 65 SYNTHETIC TRANSCRIPTS. ***

         POSITIONAL ALONE (`allv0[1]')   -- rejected an out-of-order read, but a first response
                                            REPLAYED as the second passed.
         BINDING ALONE (`first response  -- rejected the replay, but an EARLIER `step 4' echo
         after the marker')                rebinds to call 1 and returns C: measured 6/6 FALSE
                                            PASS on the incoming-context mutant, where the
                                            positional rule had correctly scored 4/5.
                                            *The binding repair LOST coverage the positional rule
                                            had.*

       So the scored observation must satisfy BOTH: it is the second response, AND it follows the
       second step.  The marker must also be UNIQUE -- with two `step 4' echoes there is no fact
       of the matter about which one bounds call 2, and guessing is what produced the false pass.

       Returns (value, why) so the caller can report WHICH condition failed rather than a bare
       absent."""
    marks = step_marker(t, nsteps)
    if len(marks) != 1:
        return None, "%d `step %d' echoes, wanted exactly 1" % (len(marks), nsteps)
    resp = responses_at(t, reg)
    if len(resp) != 2:
        return None, "%d %s responses, wanted exactly 2" % (len(resp), reg)
    val, pos = resp[1]
    if pos <= marks[0][1]:
        return None, "the 2nd %s response precedes the 2nd step" % reg
    return val, "ok"


def printed(t, reg):
    r = responses(t, reg)
    return "absent" if not r else "0x%x" % int(r[0], 16)

print("alpha_swpctx_v0_probe -- binary=%s label=%s machine=%s" % (BIN, LABEL, MACH))
print("%-14s %-22s %-22s %-56s %s" % ("row", "got", "want", "note", ""))

# ---------------------------------------------------------------- the program
#  first call:  a0 = C  ->  ctx = C          (establishes the OLD context)
#  seed:        v0 = S                       (so "untouched" is distinguishable)
#  second call: a0 = N  ->  v0 should be C
first  = load_const(T0, SCRATCH) + [LDQ(A0, 0, T0), CALL_PAL(PAL_SWPCTX)]
second = load_const(T0, SCRATCH) + [LDAH(V0, SENT >> 16),
                                    LDQ(A0, 8, T0), CALL_PAL(PAL_SWPCTX)]
prog = first + second

setup = ["put d 0x%x, 0x%x" % (SCRATCH + 0, CTX_C),
         "put d 0x%x, 0x%x" % (SCRATCH + 8, CTX_N)]
cmds  = setup + ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog)]
cmds += ["pc=0x%x" % k0(CODE),
         "step %d" % len(first),      # up to and including the FIRST swpctx
         "print v0",                  # v0 after call 1 -- the liveness/attribution baseline
         "step %d" % len(second),     # seed the sentinel, then the SECOND swpctx
         "print v0",
         "print a0"]
txt, alive = session(cmds)

v0_after1 = printed(txt, "v0")
allv0 = responses(txt, "v0")
alla0 = responses(txt, "a0")
a0_final = ("0x%x" % int(alla0[-1], 16)) if alla0 else "absent"

#  *** A MEASURED FALSE PASS LIVED HERE UNTIL 2026-09-08, AND A SEAT FOUND IT BY EXERCISING THIS
#  PARSER IN ISOLATION RATHER THAN BY READING IT. ***  This was `allv0[-1] if allv0 else "absent"'.
#  The script issues TWO `print v0' commands; if the SECOND response is missed -- a short pty read,
#  a slow step -- `[-1]' silently returns the FIRST call's value.  Under an incorrect repair that
#  returns the INCOMING context (`v0 = a0'), call 1 is passed C, so that stale first value IS C,
#  and the `v0 ctx' row that wants C GOES GREEN ON A BROKEN BUILD.
#
#  codex fed exactly that synthetic transcript -- one v0 response of C, plus a0 = N -- to this
#  scoring code and it returned 4/4.  Not a product escape: a HARNESS false pass, which the
#  stopping rule says is fixed in-round rather than filed.
#
#  THE FIX IS TO REFUSE, NOT TO GUESS.  Fewer than two responses is an APPARATUS failure and must
#  be loud, because "the apparatus selected nothing" and "the value was wrong" must not render the
#  same.  The `v0 pair' row below states the denominator, which is the discipline this project
#  already requires of any search.
#  *** AND THE FIRST REPAIR RELOCATED THE PROBLEM RATHER THAN REMOVING IT -- deepseek and kimi
#  found that independently on the next pass. ***  `len(allv0) >= 2' plus `allv0[-1]' counts
#  REGEX MATCHES, not the IDENTITY of the two responses this script asks for.  Under three or
#  more matches `[-1]' is not the second response at all, and the guard as first written was
#  satisfied by a count rather than by a position.
#
#  THE POSITIONAL FORM SAYS WHAT IS MEANT: v0_final is THE SECOND RESPONSE, and the row below
#  requires EXACTLY two so a third match is loud rather than silently re-indexing.
V0_RESPONSES = len(allv0)
v0_bound, v0_why = bound_second(txt, "v0", len(second))
v0_final = ("0x%x" % int(v0_bound, 16)) if v0_bound else ("UNBOUND: " + v0_why)

#  ---- CONTROL 1: LIVENESS -- the guest ran and the debugger answered ---------------------
row("live", "alive" if alive else "died", "alive",
    "CONTROL: the session survives the whole sequence")
row("v0 read", "yes" if v0_after1 != "absent" else "absent", "yes",
    "CONTROL: v0 is readable at all through `print' after call 1")

#  ---- CONTROL 1b: APPARATUS -- the second observation actually arrived --------------------
#  Without this, a missed second response silently reuses the first and can GREEN a broken build.
row("v0 pair", "%d of 2" % V0_RESPONSES, "2 of 2",
    "APPARATUS: EXACTLY two `print v0' responses")

#  ---- CONTROL 1c: the observation is BOUND TO ITS STEP -----------------------------------
#  Closes the two ORDER escapes anchoring could not: a read moved before the second step, and
#  the first response replayed as the second.  Both are well-formed responses in the wrong
#  place, so only position relative to `step' can reject them.
row("v0 bound", "yes" if v0_bound else "no", "yes",
    "APPARATUS: the scored v0 is the 2nd response AND follows a UNIQUE 2nd step (%s)" % v0_why)

#  ---- CONTROL 2: ATTRIBUTION -- did the handler publish the old context into a0? ----------
#  *** THIS ROW WANTED `a0 == CTX_N' UNTIL 2026-09-08, AND THAT WAS A MEASURED FALSE FAIL. ***
#  Three pass-2 seats read it as pinning THIS MODEL'S CHOSEN REPAIR rather than the
#  architecture, and a built mutant settled it: a CORRECT implementation that also clobbers a0
#  (`r[ALPHA_V0] = ctx' kept, plus `r[ALPHA_A0] = 0xdeadbeef') scored 3/4, failing HERE while
#  `v0 ctx' stayed green.  Real PALcode does clobber a0, and the fix's own comment invokes a0's
#  UNPREDICTABLE status -- which permits ANY value.  So the old row required what the round
#  itself said was not owed.  (kimi: "the probe pins this model's chosen repair, not the
#  architecture".)
#
#  THE HONEST ASSERTION IS THE NEGATIVE ONE: the handler must not publish the OLD context into
#  a0.  That is exactly the defect, and it leaves a0 otherwise free.  All four states:
#
#      shipped defect   (v0=S, a0=C)      RED here      -- the defect, still caught
#      correct          (v0=C, a0=N)      green
#      correct+clobber  (v0=C, a0=0xdead) green         -- no longer a false fail
#      never executed   (v0=S, a0=N)      green here, but `v0 ctx' REDS
#
#  The never-executed case is covered by `v0 ctx', so nothing is lost by relaxing this row --
#  and the OBSERVED a0 is printed either way, which is where the attribution reading lives.
#  *** AND THE FIRST REPAIR TRADED ONE FALSE FAIL FOR A NARROWER ONE, AND ADDED A REGRESSION.
#  Both MEASURED by a seat over synthetic transcripts. ***
#
#    * `a0 != C' scored a MISSING OBSERVATION as a PASS -- "absent" != "0x1000000" is true -- so
#      deleting the final `print a0', or losing its response, turned an apparatus failure into a
#      green row.  The identical transcript scored 3/4 before the repair and 5/5 after.  I
#      introduced that.
#    * `a0 != C' is ALSO still architecturally wrong: UNPREDICTABLE does not imply `a0 != C'.  An
#      implementation that keeps the correct v0 store and ALSO copies that result into a0 before
#      the load block is PERMITTED -- the manual allows an unpredictable result derived from
#      accessible state, and C is already the required return value -- yet it scored 4/5.
#
#  SO THE SCORED CLAIM IS APPARATUS INTEGRITY, AND THE VALUE IS DIAGNOSTIC.  a0 must be OBSERVED;
#  what it holds is printed for the reading that made this a witness -- pre-fix it is C, which
#  says the handler RAN and published to the wrong register -- but no architecturally permitted
#  value is scored against.  `v0 ctx' is what catches the defect, and it does so alone.
#  *** THE CHANNEL LINE FOR THIS ROW, because a pass-5 seat correctly asked what mutant it now
#  kills. ***  Its ORIGINAL mutant was "the handler publishes the old context into a0", and that
#  is no longer scored -- the architecture permits it, which is why the value became diagnostic.
#  So the row would be VACUOUS BY CONSTRUCTION unless it names a different one.
#
#      MUTANT IT KILLS:  the a0 OBSERVATION IS LOST -- the final `print a0' deleted, its response
#                        missed by a short read, or the register unreadable.
#      OBSERVABLE:       `a0_final' is "absent" rather than a hex value.
#
#  That is not hypothetical: the pass-3 repair scored `a0 != C', and "absent" != "0x1000000" is
#  TRUE, so a lost observation PASSED.  A seat measured the same transcript at 3/4 before that
#  repair and 5/5 after.  This row exists to make that state red, and it is the only row that can
#  -- `v0 ctx' says nothing about a0.
row("a0 obs", "seen" if a0_final != "absent" else "absent", "seen",
    "APPARATUS: a0 was observed.  DIAGNOSTIC, not scored: a0 = %s%s" %
    (a0_final, "  <- the OLD context: the handler ran and published to the wrong register"
               if a0_final == ("0x%x" % CTX_C) else ""))

#  ---- THE DEFECT ROW ---------------------------------------------------------------------
#  Asserts the CORRECT behaviour, so: pre-fix RED, post-fix GREEN, same script.
row("v0 ctx", v0_final, "0x%x" % CTX_C,
    "swpctx must return the OLD context in v0 (S=0xab0000 means it never wrote v0)")

bad = [n for n, ok in rows if not ok]
print("\nSWPCTXV0_RESULT=%d/%d" % (len(rows) - len(bad), len(rows)))
if bad:
    print("FAILING: " + " ".join(bad))
print("SWPCTXV0_DONE")
