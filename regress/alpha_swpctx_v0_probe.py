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
        os.execv(BIN, [BIN, "-V", "-x", "-E", "alpha", "-e", MACH, "-M", "64",
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
RESP = r"^GXemul> print +%s *\n *(0x[0-9a-f]+) *$"

def responses(t, reg):
    """Every genuine `print <reg>' response, in order.  Anchored, so a trace line or a
       lookalike command cannot supply one."""
    return re.findall(RESP % reg, t, re.M)

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
v0_final = ("0x%x" % int(allv0[1], 16)) if V0_RESPONSES == 2 else \
           ("%d v0 RESPONSE(S), WANTED EXACTLY 2" % V0_RESPONSES)

#  ---- CONTROL 1: LIVENESS -- the guest ran and the debugger answered ---------------------
row("live", "alive" if alive else "died", "alive",
    "CONTROL: the session survives the whole sequence")
row("v0 read", "yes" if v0_after1 != "absent" else "absent", "yes",
    "CONTROL: v0 is readable at all through `print' after call 1")

#  ---- CONTROL 1b: APPARATUS -- the second observation actually arrived --------------------
#  Without this, a missed second response silently reuses the first and can GREEN a broken build.
row("v0 pair", "%d of 2" % V0_RESPONSES, "2 of 2",
    "APPARATUS: EXACTLY two `print v0' responses, so v0_final is positionally call 2's")

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
