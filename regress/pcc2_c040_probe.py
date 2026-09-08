#!/usr/bin/env python3
#
#  pcc2c040kill -- RUNG-3 WITNESS: ONE legal guest byte store ends the host.
#
#  THE DEFECT.  `dev_pcc2.c', in `reassert_interrupts()':
#
#      fatal("pcc2: C040 interrupt assertions... TODO\n");        (:275)
#      exit(1);
#
#  The C040 test is the FIRST thing in that helper.  `PCCTWO_GENCTL' is offset 0x02, `PCC2_C040'
#  is 0x04, `pcctwo_reg[]' is `uint8_t[]', and the register resets to 0x00.  **The GENCTL byte-write
#  arm stores `idata' UNMASKED and then calls the helper in the same access** -- so a single legal
#  `st.b' of 0x04 terminates the emulator on the spot.  No second access, no driver, no interrupt.
#
#  *** THAT ONE-ACCESS READING IS A CORRECTION, NOT THE ORIGINAL FINDING. ***  This row was filed
#  around a longer road -- an SCCRXIACK load running the same helper, reachable from OpenBSD's `cl.c'
#  console driver -- and a codex pass-1 audit found the short one: *"the GENCTL write itself
#  immediately calls the terminating helper.  Arming and termination occur within that access;
#  subsequent SCC traffic is unnecessary."*  The long road is real and SUPERFLUOUS; nobody had
#  noticed the short one because the long one was interesting.
#
#  ---------------------------------------------------------------------------------------------
#  DESIGN REVIEWED BY grok (regress/artifacts/pcc2c040kill/grok_witness_20260907.txt), which
#  REFUSED the first proposal: *"A guest `st.b' of 0x04 at GENCTL is a sound CORE of a rung-3
#  witness of this kill.  Survival-only, in `pcc2_width_probe.py', with no same-decode preset and no
#  site-attribution, is not.  That is the same class as the design you asked me to assume: the
#  observation is either destroyed by the defect, or it reports success while measuring nothing."*
#
#  All three of its requirements are built in:
#
#    1.  A SAME-DECODE PRESET that must SURVIVE.  grok supplied it: *"`acc all' already writes 0x10
#        to GENCTL and survives.  That is the negative control.  It is not the witness."*  So the
#        control writes 0x10 through the identical instruction, register and width.
#    2.  SITE ATTRIBUTION.  The kill text is unique in the tree, so a death here cannot be confused
#        with a death anywhere else.
#    3.  NOT bolted into `pcc2_width_probe.py'.  That is a 113 KB SHIPPED detector whose scores are
#        recorded; adding rows perturbs them.  Separate file, scaffolding COPIED.
#
#  *** THE session() BELOW IS COPIED VERBATIM AND MUST NOT BE REIMPLEMENTED. ***  grok's pitfall #8,
#  measured on this exact machine: *"Hand-rolled prompt wait -- death reads as SURVIVED."*  The
#  copied version reaps the child and reports `how' (exit1 / sigN), which is what makes "died" a
#  measurement rather than a timeout.
#
#  OTHER PITFALLS IT ENUMERATED, all avoided here:
#    *  a debugger `put b' does NOT reproduce this -- the store must be a GUEST `st.b' (S2);
#    *  `-e 187' is not the subtype: everything dies and survival-only would score the defect on a
#       machine that never constructed.  The subtype is `mvme187';
#    *  CHIPREV (0x01) and VECBASE (0x03) have no C040 path, so an off-by-one in the offset silently
#       tests nothing;
#    *  a post-fix GENCTL readback of 0 proves nothing: unmapped reads are also 0.
#
#  *** CONTRACT. ***  This witnesses THIS `exit(1)' and is NOT a detector of the repair: the
#  adjudicated disposition is DECLINE + LATCHED ANNOUNCE, and "host survives" would green for a
#  silent decline, a latched one, and a real C040 implementation alike.  A fix round owes a row that
#  discriminates them -- for the latched form, the announce text and its once-only property are the
#  available channel.
#
#  Usage:  pcc2_c040_probe.py <gxemul-binary> [label]
import os, pty, re, select, sys, time
BIN = sys.argv[1] if len(sys.argv) > 1 else "build/gxemul"
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
DUMMY = "/tmp/pcc2_c040_dummy.bin"      #  own name: never share a scratch path with the
open(DUMMY, "wb").write(bytes(4))       #  shipped width probe.  bytes(4), not an
                                        #  escape: this line cooked once already.

CODE = 0x00010000
SCRATCH = 0x00020000
PCC2 = 0xfff42000
GENCTL, T2CTL, T2ICR, SCCERR, SCCTX = 0x02, 0x16, 0x1a, 0x1c, 0x1e
def enc(op26, rd, rs1, imm):
    return (op26 << 26) | (rd << 21) | (rs1 << 16) | (imm & 0xffff)


#  r2 = PCC2 base, r3 = scratch, r4 = load target, r5 = store source, r6 = second source
#  ld.b / ld.h (0x07 / 0x06) SIGN-EXTEND: 0x82 would print as 0xffffff82.  Every row that
#  asserts a VALUE uses the unsigned forms ld.bu / ld.hu (0x03 / 0x02); the survival rows
#  only check exit status and keep the signed forms.
def LD_B(rd, off): return enc(0x07, rd, 2, off)
def LD_H(rd, off): return enc(0x06, rd, 2, off)
def LD_BU(rd, off): return enc(0x03, rd, 2, off)
def LD_HU(rd, off): return enc(0x02, rd, 2, off)
def LD_W(rd, off): return enc(0x05, rd, 2, off)
def ST_B(rs, off): return enc(0x0b, rs, 2, off)
def ST_H(rs, off): return enc(0x0a, rs, 2, off)
def ST_W(rs, off): return enc(0x09, rs, 2, off)
I_ST_SCR = enc(0x09, 5, 3, 0)          # st  r5,r3,0   scratch word
I_LD_SCR = enc(0x05, 4, 3, 0)          # ld  r4,r3,0
I_BR_SELF = 0xc0000000
SENTINEL = 0xdeadbeef
rows = []

def row(name, got, want, note=""):
    assert name not in [n for n, _ in rows], "DUPLICATE ROW NAME %r" % name
    assert len(name) <= 15, name    # load-bearing for gate_arm.sh: `%-16s' plus a literal space keep its `^$v  .*ok$' pattern satisfiable (pass 9, Opus)
    ok = (got == want)
    rows.append((name, ok))
    print("%-16s %-12s %-12s %-46s %s" % (name, str(got), str(want), note,
                                          "ok" if ok else "FAIL"))
    return ok

def session(cmds, settle=1.5, spin=1.2):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "mvme88k", "-e", "mvme187", "-M", "64",
                       "0x10000:" + DUMMY])
        os._exit(127)
    buf = ""

    def rd(t, until=None):
        #  drain the pty for t seconds; with `until', return as soon as that text has
        #  arrived (pass 7: a fixed drain after `continue' could send the next command to a
        #  guest that had not reached its breakpoint yet).
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            if until is not None and until in buf:
                return True
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
        if until is not None and until in buf:    # pass 9 (codex): the token may land in the last read
            return True
        return "timeout" if until is not None else True

    alive = rd(settle)
    how = "nostatus"
    for i, c in enumerate(cmds):
        w = spin if i == len(cmds) - 1 else 0.25
        until = None
        if isinstance(c, tuple):    # (cmd, wait[, until]): `continue' waits for its breakpoint
            until = c[2] if len(c) > 2 else None    # read the tuple BEFORE unpacking it
            c, w = c[0], c[1]
        try:
            #  the one unbounded call left (pass 9, Opus): it blocks only if the pty input buffer fills
            #  while the guest free-runs -- tens of bytes per command against a kilobyte buffer.
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            alive = False
            break
        r = rd(w, until)
        if r is False:
            alive = False
            break
        if r == "timeout":
            #  pass 8 (codex, grok): the guest never reached its breakpoint -- send it nothing
            #  more, and let every row of this session say so through cval().
            how = "no-breakpoint"
            break
    try:
        os.write(fd, b"quit\n")
        rd(0.4)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    how = how if how == "no-breakpoint" else "nostatus"
    #  pass 7: a guest still running (no breakpoint reached) would block waitpid forever;
    #  give it a moment after the pty closed, then kill it -- the row says so, the gate
    #  does not hang.
    stat = None
    reaped = False
    for _ in range(30):
        try:
            p, stat = os.waitpid(pid, os.WNOHANG)
        except OSError:
            p, stat = pid, None
        if p:
            reaped = True
            break
        time.sleep(0.1)
    if not reaped:
        try:
            os.kill(pid, 9)
        except OSError:
            pass
        how = how if how == "no-breakpoint" else "killed"
        for _ in range(30):    # pass 8 (Opus F2): reap the killed child, bounded
            try:
                p, stat = os.waitpid(pid, os.WNOHANG)
            except OSError:
                p, stat = pid, None
            if p:
                reaped = True
                break
            time.sleep(0.1)
        if not reaped:
            how = how if how == "no-breakpoint" else "unreaped"
    try:
        if stat is None or not reaped or how in ("no-breakpoint", "unreaped", "killed"):
            pass
        elif os.WIFSIGNALED(stat):
            how = "sig%d" % os.WTERMSIG(stat)
        elif os.WIFEXITED(stat):
            how = "exit%d" % os.WEXITSTATUS(stat)
    except OSError:
        pass
    return buf.replace("\r", ""), alive, how
def program(insns, at=CODE):
    #  `at' lets a session run TWO programs: a second sequence at the SAME address finds
    #  pc already there and the assignment is skipped (the Addr hazard, designed out in
    #  the sgi probes with Addr.take()).  Callers needing two pass at=CODE + 0x100.
    words = list(insns) + [I_BR_SELF, 0]
    cmds = ["put w 0x%x, 0x%08x" % (at + 4 * i, w) for i, w in enumerate(words)]
    return cmds + ["pc=0x%x" % at, "step %d" % len(insns)]


def setup(r5="0x5a5a5a5a", r6="0x0"):
    return ["r2=0x%x" % PCC2, "r3=0x%x" % SCRATCH, "r5=%s" % r5, "r6=%s" % r6,
            "r4=0x%x" % SENTINEL]

print("pcc2_c040_probe -- binary=%s label=%s machine=mvme88k/mvme187" % (BIN, LABEL))
print("%-14s %-22s %-22s %-50s %s" % ("row", "got", "want", "note", ""))

C040 = 0x04            #  PCC2_C040
BENIGN = 0x10          #  grok: `acc all' already writes this to GENCTL and survives

#  ---- CONTROL: the identical instruction, register and width, with a benign value ---------------
t, alive, how = session(setup(r5="0x%x" % BENIGN) + program([ST_B(5, GENCTL)]))
row("genctl ctl", "alive" if alive else "died(%s)" % how, "alive",
    "CONTROL: same st.b, same GENCTL, benign value -- must survive")

ctl_saw_c040 = ("C040 interrupt assertions" in t)
row("genctl ctlq", "no" if not ctl_saw_c040 else "yes", "no",
    "CONTROL: the benign write must NOT reach the C040 arm")

#  ---- THE DEFECT ROW ---------------------------------------------------------------------------
#  ORACLE POLARITY is the ladder's: assert the CORRECT behaviour, so this is RED pre-fix and GREEN
#  post-fix with the SAME script.
t2, alive2, how2 = session(setup(r5="0x%x" % C040) + program([ST_B(5, GENCTL)]))
row("c040 kill", "alive" if alive2 else "died(%s)" % how2, "alive",
    "one legal guest st.b of 0x04 to GENCTL must NOT end the host")

#  ---- ATTRIBUTION: if it died, it died HERE ----------------------------------------------------
#  Green in both directions by construction; RED only if the host dies WITHOUT this arm's text.
sig = ("C040 interrupt assertions" in t2)
row("c040 attrib", "yes" if (alive2 or sig) else "died-elsewhere", "yes",
    "ATTRIBUTION: a death here must carry the C040 arm's unique diagnostic")

for _l in t2.split(chr(10)):
    if "C040" in _l:
        print("  EVIDENCE: %s" % _l.strip())

#  ================================================================================================
#  #512 DISCRIMINATING ROWS.  The four rows above are the WITNESS and their oracle is `alive' --
#  which, as this file's own contract says, greens for a silent decline, a latched decline and a
#  real C040 implementation alike.  The pass-1 panel named the two mutants that survive it:
#
#    deepseek  "a text-matching row that only checks for the announce after a SINGLE C040 write is
#               insufficient ... the once-only check is essential; presence alone is not enough."
#    minimax   the NON-SUPPRESSING mutant -- announce correctly, then forget `assert = 0'.
#
#  The four rows above are LEFT BYTE-FOR-BYTE ALONE.  They were measured 3/4 RED on the committed
#  build and 4/4 GREEN on the fix with the SAME script (artifacts witness_HEAD_ and witness_FIX512_),
#  which is witness clause (i); re-keying them onto the new text would destroy that evidence.
#  ================================================================================================

#  The announce's own distinctive substring.  Deliberately NOT the whole sentence: a row that
#  matches the full text also fails on a harmless rewording, which makes it a spelling test.
SAYS = "C040 (MC68040 EIPL)"

#  ---- kills: SILENT DECLINE (delete the announce, keep `assert = 0').  channel: the text --------
row("c040 says", "yes" if SAYS in t2 else "no", "yes",
    "the decline must ANNOUNCE -- a silent decline is a different disposition")

#  ---- kills: NON-LATCHING (drop the `warned' test, or clear the bit).  channel: the COUNT -------
#  Two C040 writes in ONE session.  The house idiom is N=1 PER DEVICE INSTANCE, so the second write
#  must be silent.  A mutant that announces every call scores 2 here and is invisible to `c040 says'.
t3, alive3, how3 = session(setup(r5="0x%x" % C040)
                           + program([ST_B(5, GENCTL), ST_B(5, GENCTL)]))
n_says = t3.count(SAYS)
row("c040 once", ("%d" % n_says) if alive3 else "died(%s)" % how3, "1",
    "TWO C040 writes must announce EXACTLY ONCE -- the (once) latch, not just presence")

#  ---- kills: LATCH-BIT COLLISION.  channel: the text SURVIVING earlier warn traffic -------------
#  `d->warned' is shared: PCC2_W_C040 is one bit of a field whose other bits are set by ordinary
#  guest register traffic.  A mutant using a bit some other arm already sets would be SILENCED by
#  benign traffic and would still pass `c040 says' on a fresh instance.  So dirty a DIFFERENT bit
#  first (a wide store to GENCTL trips the width decline, PCC2_W_GENCTL_LEN) and require the
#  announce anyway.  #490 measured exactly this collision shape in this file.
#  *** ST_H, NOT ST_W.  MEASURED: a WORD store to GENCTL (offset 0x02) is misaligned and the m88k
#  core raises `exception MISALIGNED_ACCESS' BEFORE memory_rw, so the pre-dirty never reaches the
#  device and this row reddened on a correct fix.  A HALFWORD store at an even offset is aligned,
#  reaches the handler, and trips the width decline because len != 1.  ***
t4, alive4, how4 = session(setup(r5="0x%x" % C040)
                           + program([ST_H(5, GENCTL), ST_B(5, GENCTL)]))
row("c040 predirty", ("yes" if SAYS in t4 else "no") if alive4 else "died(%s)" % how4, "yes",
    "a DIFFERENT warned bit set first must not silence the C040 announce (bit-collision mutant)")

#  ---- OWED, NOT SHIPPED -- and named so the gap does not read as coverage ------------------------
#  minimax's NON-SUPPRESSING mutant (announce correctly, then forget `assert = 0') is NOT covered
#  by any row here.
#
#  *** DO NOT USE THE `IPL ... => ASSERT' debug LINE AS THE ORACLE.  It is the obvious candidate and
#  it is WRONG, for a reason that has nothing to do with visibility. ***
#
#  `debug("[ pcc2: IPL = %i, MASK = %i => %s ]")' sits at the FOOT of reassert_interrupts() but
#  EXECUTES BEFORE BOTH SUPPRESSIONS -- the MIEN test and the C040 test are BELOW it, and only the
#  INTERRUPT_ASSERT/DEASSERT pair after them reflects the real line state.  Verified by line order.
#  So the message reports the PRE-SUPPRESSION value of `assert' and is green under the very mutant it
#  would be chosen to catch.  *Named by the codex seat on pass 1: "do not use the existing
#  `IPL ... => ASSERT' debug message as the line-state oracle: it executes before MIEN suppression
#  and before the proposed C040 suppression.  Observe the interrupt callback/state."*
#
#  (Two earlier drafts of this paragraph were wrong in two different ways.  The first said the line
#  was ABSENT at default verbosity -- false; it prints while single-stepping, and the "0 occurrences"
#  came from grepping the probe's own STDOUT ARTIFACT instead of the captured pty text.  The second
#  then proposed it as the oracle.  **Visibility was never the question; POSITION was.**)
#
#  *** WHAT ACTUALLY BLOCKS THE ROW IS THAT ITS CHANNEL CANNOT VARY, AND THAT IS A SOURCE FACT. ***
#  For the tail to print ASSERT at all, some interrupt must be pending above the mask -- i.e. an
#  INT bit set in one of the ICRs.  MEASURED by reading every guest-writable arm: TxICR keeps only
#  `idata & 0x17' and SCCICR only `idata & 0x1f', so PCC2_IRQ_INT (0x20) is MASKED OUT OF EVERY
#  WRITABLE ARM.  The bit's only producer is reassert_interrupts() itself, from
#  pending_timerN_interrupts, which are incremented by the TIMER TICK -- and a stepped probe cannot
#  run one, because the debugger stops host-timer callbacks for the duration of `step'.
#
#  So this is the accept-row failability rule one level up: a NEVER-SET-BY-GUEST bit cannot carry
#  the row, and no amount of verbosity changes that.  The row needs a FREE-RUNNING probe shape.
#
#  *** AND IT IS A MEASURED ESCAPE, NOT A PREDICTED ONE.  KILL TABLE, 2026-09-08, artifacts in
#  regress/artifacts/pcc2c040kill/killtable_20260907/: ***
#
#      BASE                                   7/7
#      M_b_reinstate   the verbatim exit(1)   3/7   floor (b) -- KILLED
#      M_d2_silent     announce deleted       4/7   floor (d) -- KILLED
#      M_d3_nolatch    announce every call    6/7   floor (d) -- KILLED (c040 once, scores 2)
#      M_d4_collide    latch bit reused       6/7   floor (d) -- KILLED (c040 predirty)
#      M_d1_noassert   `assert = 0' removed   7/7   *** ESCAPES -- CLEAN SWEEP ***
#
#  *** THIS IS A FLOOR BREACH UNDER CLAUSE (d), AND THIS FILE DOES NOT PRETEND OTHERWISE. ***
#  `assert = 0' IS the repair's effect, so removing it is (d)'s canonical "keep the guard, null the
#  repair" -- inside the DEPENDS-ON closure, not outside it.  Calling it clause-(e) contract debt
#  would be using the contract as an escape hatch, which is the one thing clause (e) must not become.
#
#  THE CONTRACT, stated honestly: this detector catches REINSTATEMENT of the host kill, a SILENT
#  decline, a NON-LATCHING announce and a COLLIDING latch bit -- all four MEASURED.  It does NOT
#  catch a fix that announces correctly and fails to suppress the assertion.  The repair for that is
#  a free-running probe (breakpoint + `continue', so host-timer callbacks run and a timer interrupt
#  can go pending), which is a different probe shape rather than another row here.

#  ================================================================================================
#  #512 L2 REPAIR -- the non-suppressing mutant, which the seven rows above CANNOT see.
#
#  MEASURED: removing `assert = 0' scores 7/7 (killtable_20260907/M_d1_noassert.raw), and a pass-2
#  seat named a ONE-TOKEN variant, `assert = 0;' -> `return;', that also scores 7/7.
#
#  *** THE DESIGN BELOW IS A REVISION.  MY FIRST ONE WOULD HAVE PASSED THE `return' MUTANT. ***
#  The codex design review (artifacts/pcc2c040kill/codex_assertrow_20260908.txt) found why:
#
#      GENCTL resets to ZERO, so MIEN is clear through the setup and every recalculation DEASSERTS
#      the CPU line.  At the final write the repair deasserts (no interrupt), deleting `assert = 0'
#      asserts (caught) -- but `return' LEAVES THE ALREADY-DEASSERTED LINE UNCHANGED, so it also
#      shows no interrupt and PASSES.  *"Deleting the assignment permits assertion; returning
#      preserves the incoming line state."*
#
#  THE FIX IS A PRECONDITION, NOT AN ORACLE: both rows write MIEN-ONLY GENCTL FIRST, so the line is
#  ALREADY ASSERTED before the operation under test.  Then `return' leaves it asserted and reddens.
#
#  AND THE OBVIOUS ORACLE IS A CHECK THAT CANNOT FAIL: rd() tests `until in buf' against the WHOLE
#  accumulated transcript, and the settle drain has already buffered a `GXemul>' prompt -- so
#  ("continue", grace, "GXemul>") returns True with ZERO READS.  `how == "no-breakpoint"' is no
#  better: it proves a MISSING TOKEN, not execution-without-delivery, and a hang satisfies it.
#  So BOTH rows stop at a breakpoint and the discriminator is WHICH PC, never a timeout.
#  ================================================================================================

IRQ_ENTRY = 0x8        #  m88k EXCEPTION_INTERRUPT is vector 1; entry = VBR + 8*vector, and VBR is
                       #  0 because mvmeprom.c EXPLICITLY sets it -- not an assumed reset value.
STCR_R5_CR1 = 0x80058025   #  stcr r5,cr1 -- copied from m88k_exc_probe.py and decoder-checked by
                           #  the review, NOT hand-assembled (the encoding trap this project records)
PSR_INDCLR = 0x80000000    #  MODE only, IND CLEAR: dispatch needs `irq_asserted && !(PSR & IND)'
CLMPCC = 0xfff45000
CLMPCC_IER = 0x11
SCCTX_ARM = 0x13       #  PCC2_IRQ_IEN | level 3.  The device ORs in INT (0x20) -> 0x33; MASK
                       #  resets to 0, so IPL 3 wins the comparison.
IER_ON = 0x03          #  clmpcc asserts SCC TX when (IER & 3) != 0


def ST_B7(rs, off):    #  store via r7 (the clmpcc base); ST_B is hardwired to r2 (PCC2)
    return enc(0x0b, rs, 7, off)


def assert_row(label, final_genctl, repeat=1, then_genctl=None):
    #  Setup runs under `step' -- dispatch is suppressed while single-stepping BY DESIGN, so the
    #  line can be armed without the interrupt being taken early.
    insns = [
        STCR_R5_CR1,               # 0  PSR: interrupts enabled
        ST_B(6, SCCTX),            # 1  SCCTX = 0x13   (IEN | level 3)
        ST_B7(8, CLMPCC_IER),      # 2  clmpcc IER -> INTERRUPT_ASSERT(irq_scc_tx), synchronous
        LD_BU(11, SCCTX),          # 3  read back: must be 0x33, proving INT arrived
        ST_B(9, GENCTL),           # 4  MIEN only -- THE PRECONDITION: the line is now ASSERTED
    ] + [ST_B(10, GENCTL)] * repeat  # 5..  the operation under test, ONCE or TWICE
    if then_genctl is not None:      # ..  and optionally a FOLLOWING write (the recovery cell)
        insns = insns + [ST_B(13, GENCTL)]
    #  COLLATERAL-STATE readback, costing NO extra session: three seats independently named
    #  suppression-by-clobbering (codex "collateral state changes"; grok `GENCTL &= ~PCC2_MIEN';
    #  deepseek "replace `assert = 0' with `MIEN = 0' -- the rows check only that no interrupt is
    #  delivered, they do not check that MIEN remains set").  Read GENCTL back so a fix that
    #  suppresses by disabling ALL interrupts is visible.
    insns = insns + [LD_BU(14, GENCTL)]

    #  6 is a harmless RAM store (I_ST_SCR = st r5,r3,0, already defined by the scaffolding) purely
    #  so the COMPLETION breakpoint at 7 is an address the guest ARRIVES AT rather than one it is
    #  already sitting on after `step'.  Do NOT hand-assemble an instruction here: `enc()' builds
    #  the IMMEDIATE form, and a triadic register op needs a different encoder.
    words = insns + [I_ST_SCR, I_BR_SELF, 0]     # harmless, then br . = COMPLETION
    #  DERIVED, never hardcoded: `repeat' changes the instruction count, and a stale literal here
    #  would put the completion breakpoint on the wrong word and make the row unfalsifiable.
    completion = CODE + 4 * (len(insns) + 1)
    cmds = ["put w 0x%x, 0x%08x" % (CODE + 4 * i, w) for i, w in enumerate(words)]
    cmds += ["put w 0x%x, 0x%08x" % (IRQ_ENTRY, I_BR_SELF)]     # the vector spins, not zeros
    cmds += ["r2=0x%x" % PCC2, "r5=0x%x" % PSR_INDCLR, "r6=0x%x" % SCCTX_ARM,
             "r7=0x%x" % CLMPCC, "r8=0x%x" % IER_ON, "r9=0x02",
             "r10=0x%x" % final_genctl, "r11=0x0", "r12=0x0",
             "r13=0x%x" % (then_genctl if then_genctl is not None else 0)]
    cmds += ["breakpoint add 0x%x" % IRQ_ENTRY,
             "breakpoint add 0x%x" % completion]
    cmds += ["pc=0x%x" % CODE, "step %d" % len(insns),
             ("continue", 6.0), "reg"]
    t, alive, how = session(cmds, spin=2.0)
    pcs = re.findall(r"pc\s*=\s*0x([0-9a-f]{8})", t)
    r11 = re.findall(r"r11\s*=\s*0x([0-9a-f]+)", t)
    r14 = re.findall(r"r14\s*=\s*0x([0-9a-f]+)", t)
    return (t, alive, how, (int(pcs[-1], 16) if pcs else None),
            (int(r11[-1], 16) if r11 else None), completion,
            (int(r14[-1], 16) if r14 else None))

#  ---- LIVENESS + POSITIVE CONTROL: with C040 CLEAR the interrupt MUST be delivered -------------
tc, alivec, howc, pcc, r11c, compc, gc = assert_row("live", 0x02)

row("irq pending", ("0x%02x" % r11c) if r11c is not None else "no-readback", "0x33",
    "LIVENESS: the clmpcc IER store must set SCCTX's INT bit -- without this the pair is vacuous")

row("irq live", ("0x%x" % pcc) if pcc is not None else "no-pc(%s)" % howc, "0x%x" % IRQ_ENTRY,
    "POSITIVE CONTROL: C040 CLEAR, line asserted -- the interrupt vector MUST be reached")

#  ---- THE DEFECT ROW: same sequence, C040 SET -- delivery must be suppressed --------------------
#  Affirmative negative evidence: it must REACH THE COMPLETION BREAKPOINT, not merely fail to
#  reach the vector.  A timeout, an unexpected stop or a death is a FAILURE, never the answer.
td, alived, howd, pcd, r11d, compd, gd = assert_row("c040", 0x06)

row("c040 noassert", ("0x%x" % pcd) if pcd is not None else "no-pc(%s)" % howd,
    "0x%x" % compd,
    "C040 SET on an ALREADY-ASSERTED line: must reach completion, NOT the interrupt vector")

#  ---- THE SECOND ENCOUNTER.  This closes the ENCOUNTER axis rather than chasing one mutant. -----
#  MEASURED: with only the row above, `assert = 0' moved INSIDE the latch scores 10/10
#  (killtable_20260908/M_latchinside.raw).  It suppresses correctly on the FIRST C040 encounter --
#  the latch is unset, so the body runs -- and skips the suppression on EVERY LATER ONE.  The codex
#  pass-1 seat predicted exactly this: *"The first encounter suppresses correctly; later encounters
#  can assert the CPU line.  The announcement count remains exactly one."*
#
#  The axis has two cells, FIRST and LATER, and the rows above held only the first.  A second
#  identical C040 write closes it: under the shipped fix `assert = 0' is outside the latch and runs
#  both times; under the mutant the second call leaves the line asserted and the interrupt lands.
t2, alive2b, how2b, pc2b, r112b, comp2b, g2b = assert_row("c040x2", 0x06, repeat=2)

row("c040 noassert2", ("0x%x" % pc2b) if pc2b is not None else "no-pc(%s)" % how2b,
    "0x%x" % comp2b,
    "the SECOND C040 encounter, latch already set, must ALSO suppress -- the encounter axis")

#  ---- THE FOURTH CELL: RECOVERY.  C040 CLEARED after the latch has fired. -----------------------
#  *** THE THREE ROWS ABOVE DO NOT CLOSE THE AXIS, and calling it closed was this round's SECOND
#  attempt to grade a floor-shaped hole as contract debt. ***  The C040 block reads TWO device-state
#  lvalues -- `GENCTL & PCC2_C040' and `warned & (1u << PCC2_W_C040)' -- so their product is FOUR
#  cells, not two (grok, pass 2 on the L2 repair):
#
#                    warned = 0            warned = 1
#      C040 clear    `irq live'            *** THIS ROW ***
#      C040 set      `c040 noassert'       `c040 noassert2'
#
#  `irq live' does NOT hold the empty cell: it runs on a FRESH machine, so `warned' is 0.  It is the
#  accept row for C040-clear, not for C040-clear-AFTER-C040-set.
#
#  THE MUTANT IT KILLS, named by the same seat -- STICKY SUPPRESSION, one line:
#      if ((GENCTL & PCC2_C040) || (d->warned & (1u << PCC2_W_C040))) {
#  After the first C040 write `warned' is set, so every later call zeros `assert' even with C040
#  CLEAR.  Predicted to score 11/11 against the rows above -- a clean sweep -- because every one of
#  them either runs fresh or keeps C040 set.
t3, alive3b, how3b, pc3b, r113b, comp3b, g3b = assert_row("c040rec", 0x06, then_genctl=0x02)

row("c040 recover", ("0x%x" % pc3b) if pc3b is not None else "no-pc(%s)" % how3b,
    "0x%x" % IRQ_ENTRY,
    "C040 CLEARED after the latch fired: assertion must RESUME -- the fourth product cell")

#  ---- COLLATERAL STATE: suppression must not be achieved by CLOBBERING. -------------------------
#  THREE SEATS named this independently on pass 2 and no row saw it: codex called it "collateral
#  state changes"; grok named `assert = 0;' plus `GENCTL &= ~PCC2_MIEN'; deepseek put it as
#  *"replace `assert = 0' with `MIEN = 0' -- the rows check only that no interrupt is DELIVERED,
#  they do not check that MIEN remains SET.  Suppression by masking passes every row."*
#
#  Costs NO extra session: the readback rides on the sessions already run.  GENCTL must still read
#  back what the guest wrote -- MIEN set, C040 set -- after the suppression has happened.
row("c040 genctl", ("0x%02x" % gd) if gd is not None else "no-readback", "0x06",
    "GENCTL must read back MIEN|C040: suppression by clobbering MIEN would pass every other row")

#  ---- THE LIVENESS CONTROL WAS ONLY APPLIED TO ONE SESSION OF FOUR. ----------------------------
#  Named by the kimi-k3:cloud seat on pass 2: *"assert_row() returns r11d and r112b, and no row
#  checks them.  Disposition 3 is correct but INCOMPLETELY APPLIED.  Its own rationale -- 'no
#  interrupt' must be distinguishable from 'no request was ever created' -- applies with equal force
#  to the two C040 sessions, yet the request check exists only for the live session."*
#
#  It is exactly right, and it is the vacuity shape: `c040 noassert' reaching COMPLETION is
#  consistent with "the fix suppressed correctly" AND with "no interrupt was ever pending in that
#  session".  Only the SCCTX readback separates them.  Free -- the sessions already ran.
for _lbl, _v in (("c040 pending", r11d), ("c040x2 pending", r112b), ("c040rec pending", r113b)):
    row(_lbl, ("0x%02x" % _v) if _v is not None else "no-readback", "0x33",
        "LIVENESS for THIS session: without it, `completion' cannot be told from `never asked'")

ok = sum(1 for _, o in rows if o)
print("")
print("PCC2C040_RESULT=%d/%d" % (ok, len(rows)))
print("PCC2C040_WITNESS=%s" % ("PASS" if ok == len(rows) else "FAIL"))
print("PCC2C040_DONE")
