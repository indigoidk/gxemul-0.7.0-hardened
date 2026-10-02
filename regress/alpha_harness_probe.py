#!/usr/bin/env python3
#  alpha_harness_probe.py -- THE ALPHA RUNG-3 HARNESS.
#
#  There has never been an Alpha probe in this tree, and three open HIGH rows need one
#  (`alphaswpctxptbr', `alphapfnoffset', and the swpctx return-register defect).  This file is
#  the FOUNDATION: an encoder, a pty session, and the two controls the witness ladder demands
#  of any rung-3 access witness.  It deliberately ships the controls FIRST and asserts nothing
#  about any defect, because a harness whose controls have never been green cannot be trusted
#  to say anything about a defect afterwards.
#
#  *** WHAT IS ESTABLISHED BEFORE THIS FILE RUNS, all read out of the fork rather than assumed:
#
#  1. THE MACHINES EXIST AND THREE OF FOUR RUN.  Measured 2026-09-07: `-H' advertises
#     alphabook1 (21066), alphaserver4100 (21164A-2), 3000/300 and eb164 (21164PC); the first,
#     second and fourth construct and reach the debugger prompt, and `3000/300' ABORTS the host
#     during construction at interrupt_handler_lookup("0") -- a separate filed defect.
#
#  2. `call_pal' IS OPCODE 0 WITH THE PAL NUMBER IN BITS 25..0, and cpu_alpha_instr.c dispatches
#     it STRAIGHT to alpha_palcode():
#         case 0x00:  ic->f = instr(call_pal);  ic->arg[0] = iword & 0x3ffffff;
#     so `call_pal 0x30' is literally the instruction word 0x00000030.
#
#     *** BUT "NO GATING OF ANY KIND" WAS MY CLAIM AND IT IS WRONG.  A seat corrected it, and
#     the correction is the difference between a working probe and one that mysteriously
#     halts. ***  Dispatch INTO alpha_palcode() carries no privilege check -- but the function
#     GATES ITS OWN SWITCH, at cpu_alpha_palcode.c:183:
#
#         uint64_t userMode = cpu->cd.alpha.ps & ALPHA_PSL_USERMODE;   /* 0x0008 */
#         if (userMode && !(palcode == 0x80 || 0x81 || 0x83 || 0xae ||
#                           0xaa || 0x86 || 0x9e || 0x92 || 0x9f)) {
#                 fatal("[ Privileged Alpha PALcode called from user mode: TODO ]");
#                 cpu->running = 0;          <-- THE MACHINE STOPS
#                 return;
#         }
#
#     0x30 is NOT on that whitelist.  So in user mode `call_pal 0x30' does not reach swpctx --
#     it HALTS THE CPU.  **That failure would present as a probe whose step never completes,
#     i.e. as a broken harness rather than as a mode problem**, which is exactly why it gets a
#     control row of its own below rather than a comment.
#
#     `cpu->cd.alpha.ps' has no explicit initialiser anywhere in src/, so it is zero from the
#     zeroed cpu struct and USERMODE is clear -- kernel mode.  **That is a DERIVATION, not a
#     measurement**, and the `palgate' row is what turns it into one.
#
#  3. THE MEMORY-FORMAT ENCODING is opcode<<26 | ra<<21 | rb<<16 | disp16, and the opcodes are
#     read off cpu_alpha_instr.c's own decoder rather than from a manual: LDA 0x08, LDAH 0x09,
#     LDQ 0x29, STQ 0x2d, LDL 0x28, STL 0x2c.
#
#  4. REGISTER NUMBERS AND DEBUGGER NAMES come from cpu_alpha.h's ALPHA_REG_NAMES:
#     r0 v0, r1 t0, r2 t1, r3 t2, ... r16 a0, ... r30 sp, r31 zero.
#
#  *** WHAT IS NOT ESTABLISHED, and is exactly what the controls are for: WHICH ADDRESSES ARE
#  WRITABLE RAM.  The machine loads a file at 0x20000000 and `alphaserver4100'/`eb164' report
#  "cpu0: starting at 0x0000000020000000", but -M 64 is 64 MB and 0x20000000 is 512 MB, so the
#  two facts do not obviously agree.  THIS FILE DOES NOT GUESS: the liveness control writes a
#  known value through a real guest store and reads it back through a real guest load, and if
#  the address is wrong that row goes RED and says so.  A harness that assumed an address and
#  then reported a defect would be measuring its own mistake. ***

import os, sys, re, pty, time, select

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
MACH  = sys.argv[3] if len(sys.argv) > 3 else "alphabook1"

rows = []

def row(name, got, want, note="", negate=False):
    ok = (got != want) if negate else (got == want)
    rows.append((name, ok))
    print("%-18s %-20s %-20s %-40s %s" % (name, str(got), ("NOT " if negate else "") + str(want),
                                          note, "ok" if ok else "FAIL"))
    return ok

# ---------------------------------------------------------------- the encoder
#  Memory format.  `disp' is a SIGNED 16-bit displacement, so it is masked here and the caller
#  is responsible for keeping values in range -- an out-of-range displacement silently truncating
#  would be a wrong instruction that still assembles, which is the hand-assembled-encoding trap
#  this project has paid for four times.  Hence the assert.
def mem(op, ra, rb, disp):
    assert -0x8000 <= disp <= 0xffff, "displacement %r out of 16-bit range" % disp
    return ((op & 0x3f) << 26) | ((ra & 31) << 21) | ((rb & 31) << 16) | (disp & 0xffff)

ZERO = 31
def LDA (ra, disp, rb=ZERO): return mem(0x08, ra, rb, disp)
def LDAH(ra, disp, rb=ZERO): return mem(0x09, ra, rb, disp)
def LDQ (ra, disp, rb):      return mem(0x29, ra, rb, disp)
def STQ (ra, disp, rb):      return mem(0x2d, ra, rb, disp)
def LDL (ra, disp, rb):      return mem(0x28, ra, rb, disp)
def STL (ra, disp, rb):      return mem(0x2c, ra, rb, disp)
def CALL_PAL(n):             return n & 0x3ffffff        # opcode 0; see note 2 above
NOP = LDA(ZERO, 0, ZERO)     # lda zero,0(zero) -- the decoder turns ra==zero into instr(nop)

#  *** BUILDING A 32-BIT CONSTANT NEEDS TWO INSTRUCTIONS AND ONE CORRECTION FOR SIGN. ***
#  LDAH adds (disp << 16) and LDA adds a SIGN-EXTENDED disp.  So for a low half with bit 15 set,
#  the LDA subtracts 0x10000 and the high half must be pre-incremented to compensate.  Getting
#  this wrong yields an address off by 65536, which would look like a memory-map problem rather
#  than an encoding bug -- so it is done here once, with a self-test below.
def load_const(reg, val):
    hi, lo = (val >> 16) & 0xffff, val & 0xffff
    if lo & 0x8000:
        hi = (hi + 1) & 0xffff
    return [LDAH(reg, hi, ZERO), LDA(reg, lo - 0x10000 if lo & 0x8000 else lo, reg)]

def _selftest_load_const():
    #  A NEGATIVE CONTROL ON THE ENCODER ITSELF, run every time.  It costs microseconds and it
    #  checks the one piece of arithmetic in this file that is easy to get silently wrong.
    for v in (0x00000000, 0x00001000, 0x00008000, 0x0000ffff, 0x20000000,
              0x5a5a5a5a, 0x20018000, 0xdeadbeef, 0x0001ffff):
        hi, lo = (v >> 16) & 0xffff, v & 0xffff
        eff_hi = (hi + 1) & 0xffff if lo & 0x8000 else hi
        eff_lo = lo - 0x10000 if lo & 0x8000 else lo
        got = ((eff_hi << 16) + eff_lo) & 0xffffffff
        if got != v:
            print("ENCODER SELFTEST FAILED for 0x%08x -> 0x%08x" % (v, got))
            return False
    return True

# ---------------------------------------------------------------- the session
def session(cmds, settle=1.6, spin=1.8):
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
        if not rd(spin if i == len(cmds) - 1 else 0.25):
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

def printed(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return "absent" if not m else "0x%x" % int(m.group(1), 16)

def run_ops(ops, at=0x01010000):
    put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]

# ---------------------------------------------------------------- go
DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alpha_dummy.bin")
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\x00" * 8)

print("alpha_harness_probe -- binary=%s label=%s machine=%s" % (BIN, LABEL, MACH))
print("%-18s %-20s %-20s %-40s %s" % ("row", "got", "want", "note", ""))

row("encoder", "ok" if _selftest_load_const() else "FAILED", "ok",
    "load_const's sign correction, 9 vectors, offline")

#  CONTROL 1 -- LIVENESS.  A known value through a REAL guest store and a REAL guest load.
#  If the scratch address is not writable RAM this row is RED, which is the point: it tells us
#  the address is wrong rather than letting a later row blame the emulator.
#  REGISTER NUMBERS, with their DEBUGGER NAMES beside them.  The two are offset by one and
#  that offset has already produced one wrong row in this file: register 1 prints as "t0",
#  register 2 as "t1", register 3 as "t2" (ALPHA_REG_NAMES, cpu_alpha.h).
T0, T1, T2, T3, T4 = 1, 2, 3, 4, 5   # debugger names: "t0".."t4"
SCRATCH, LIVE_VAL = 0x01020000, 0x5a5a5a5a
ops = load_const(T0, SCRATCH) + load_const(T1, LIVE_VAL) + [STQ(T1, 0, T0), LDQ(T2, 0, T0)]
#  PRINT THE REGISTER THE LOAD ACTUALLY TARGETS.  T2 is register NUMBER 3, and
#  ALPHA_REG_NAMES calls register 3 "t2" -- an earlier draft printed "t1" (register 2), which
#  the load never writes, so the row would have been reading an untouched register.  That is
#  the hand-assembled-encoding trap in its purest form: a wrong register field yields a value
#  no oracle here would have questioned.
t, alive = session(run_ops(ops) + ["print t2"])
row("live", printed(t, "t2") if alive else "died", "0x%x" % LIVE_VAL,
    "LIVENESS: guest store then load, through RAM")

#  CONTROL 2 -- did the CPU execute at all?  A register written by a guest instruction and
#  nothing else.  It separates "the store/load path is wrong" from "no instruction ran", which
#  the liveness row alone cannot distinguish -- both present as a wrong value.
t, alive = session(run_ops(load_const(T2, 0x1234)) + ["print t2"])
row("exec", printed(t, "t2") if alive else "died", "0x1234",
    "a guest LDAH/LDA pair reached a register")

#  CONTROL 3 -- THE PALCODE MODE GATE.  `call_pal 0x30' is privileged: in user mode
#  alpha_palcode() prints "Privileged Alpha PALcode called from user mode" and sets
#  cpu->running = 0 BEFORE its switch, so the handler never runs.  This row proves we are on the
#  kernel-mode side of that gate, by asserting the diagnostic is ABSENT and the machine is still
#  alive after issuing the call.
#
#  *** IT IS A CONTROL ON A PREMISE THAT WAS ALREADY WRONG ONCE. ***  I wrote in this file's own
#  header that dispatch has "no gating of any kind"; a seat read alpha_palcode() and corrected
#  it.  A harness that assumed kernel mode and hit the gate would report a dead machine and look
#  like a pty or encoding fault -- so the assumption is measured here instead of trusted.
t, alive = session(run_ops([CALL_PAL(0x30)]) + ["print v0"])
gated = "gated" if "user mode" in t else "not gated"
row("palgate", gated, "not gated",
    "call_pal 0x30 is privileged; we must be in kernel mode")
#  *** `palalive' IS VACUOUS AND IS KEPT ONLY AS A LABELLED NON-ORACLE. ***  `alive' means the pty
#  is still readable.  `alpha_palcode's default arm sets `cpu->running = 0' and STAYS IN THE
#  DEBUGGER, because -V single-steps -- the emulator does not exit.  So this row cannot distinguish
#  a served call from a refused one and would stay green either way.  The mode question is answered
#  by `palgate', which greps for the diagnostic text instead.
row("palalive", "alive" if alive else "died", "alive",
    "NON-ORACLE: -V keeps the debugger alive either way; see palgate")

# ---------------------------------------------------------------- the swpctx witness
#  *** THE FIRST DESIGN WAS SELF-DEFEATING AND A SEAT REFUTED IT.  The defect DESTROYS THE PATH
#  THE WITNESS NEEDS TO OBSERVE IT, and that is why everything below lives in K0SEG. ***
#
#  The naive design -- put both PCBs in ordinary RAM, swpctx twice, read ctx_A+16 -- fails because
#  `alpha_translate_v2p' only identity-maps while `base == 0':
#
#      if (!userMode && (vaddr >= ALPHA_K0SEG_BASE && vaddr <= ALPHA_K0SEG_END)) {
#              *return_paddr = vaddr & 0x000003ffffffffffULL;   /* checked FIRST */
#              return 2; }
#      ...
#      if (!userMode && base == 0) { *return_paddr = vaddr & ...; ... }   /* the "UGLY hack" */
#
#  The moment the buggy line makes `apcb_ptbr' nonzero, `base != 0', the hack stops applying, and
#  every later access -- INCLUDING INSTRUCTION FETCH -- falls into a page-table walk over garbage.
#  One vaddr in that path even has an `exit(1)'.  So the second `call_pal' never lands and the save
#  that is supposed to publish the defect never happens.
#
#  AND THE OBVIOUS FALLBACK FAILS TOO, by symmetry: putting the marker in `ptbr' instead of `flags'
#  makes the identity map die on the FIXED build rather than on the defective one.  **No nonzero
#  value anywhere in that field survives either polarity**, so K0SEG is not the better option -- it
#  is the only one.
#
#  K0SEG is checked BEFORE `base' is read, so a K0SEG access is immune to whatever `apcb_ptbr'
#  holds.  Code, both PCBs and the pointer vector therefore all live there.
#
#  *** THE BOOTSTRAP, because lda/ldah build 32-bit constants and K0SEG needs bit 63..42: ***
#  the 64-bit pointers are written into memory with the debugger's `put d' (64-bit; note `put q' is
#  128-bit in this debugger) and the guest loads them with ONE identity-mapped `ldq' issued while
#  `ptbr' is still zero.  After that every address the guest uses is a K0SEG value held in a
#  register, and nothing depends on translation state again.
K0SEG      = 0xfffffc0000000000
def k0(p):  return K0SEG | p

#  *** EVERY ADDRESS HERE WAS OUTSIDE RAM UNTIL A CODE REVIEW SAID SO, AND THE FAILURE WOULD
#  HAVE BEEN SILENT AND GREEN. ***  The machine is built with `-M 64' = 64 MB, and these were
#  at 0x200xxxxx (512 MB+).  K0SEG translation is `vaddr & 0x3ffffffffff', so the K0SEG idea
#  survives contact with alpha_translate_v2p -- but the PHYSICAL BACKING does not.
#
#  `memory_warn_about_unimplemented_addr' only halts when `halt_on_nonexistant_memaccess' is
#  set, i.e. under `-T'.  WITHOUT IT: writes succeed and are DISCARDED, and reads RETURN
#  ZEROS.  An instruction fetch of zeros is a real instruction -- `call_pal 0'.
#
#  So with the old plan the guest wrote nothing, read zeros, and the defect row -- which
#  wanted ZERO for the correct case -- would have gone GREEN while measuring "unmapped reads
#  return 0".  Three rows were exposed to that.
P_CODE, P_PTRV, P_PCB_A, P_PCB_B = 0x01040000, 0x01020000, 0x01030000, 0x01031000
assert max(P_CODE, P_PTRV, P_PCB_A, P_PCB_B) < 64*1024*1024, \
    'address outside the 64 MB the machine is built with -- reads would return 0 silently'
#  *** TWO DISTINCTIVE VALUES, AND NEITHER IS ZERO.  THIS IS THE POINT. ***
#  The first design put 0 in A.ptbr so the CORRECT case read back 0 -- and 0 is also what an
#  unmapped read returns, so a broken setup was indistinguishable from a correct handler.
#  K0SEG is what makes the repair possible: translation never consults `apcb_ptbr' for a
#  K0SEG address, so `apcb_ptbr' may hold anything without breaking the probe.
#
#      correct handler  -> PCB_A+16 == PTBR_VAL   (apcb_ptbr keeps A's ptbr)
#      the defect       -> PCB_A+16 == FLAGS_VAL  (apcb_ptbr took A's flags)
#      anything broken  -> 0, which is NEITHER, so BOTH rows red
PTBR_VAL  = 0x00000000aaaa1111     # A.ptbr
FLAGS_VAL = 0x00000000bbbb2222     # A.flags
MARKER = FLAGS_VAL                  # kept for the row text below

#  PCB field offsets, read off the save block in cpu_alpha_palcode.c:
#      +0 ksp  +8 usp  +16 ptbr  +24 cpc(32)  +28 asn(32)  +32 unique  +40 flags  +48/56 decrsv
def pcb(base, ptbr, flags):
    return ["put d 0x%x, 0x%x" % (base + 0,  0),
            "put d 0x%x, 0x%x" % (base + 8,  0),
            "put d 0x%x, 0x%x" % (base + 16, ptbr),
            "put d 0x%x, 0x%x" % (base + 32, 0),
            "put d 0x%x, 0x%x" % (base + 40, flags),
            "put d 0x%x, 0x%x" % (base + 48, 0),
            "put d 0x%x, 0x%x" % (base + 56, 0)]

#  A.ptbr = 0 so the CORRECT build leaves apcb_ptbr zero; A.flags = MARKER so the DEFECTIVE build
#  copies MARKER into apcb_ptbr.  The second swpctx then saves apcb_ptbr into A+16, and that word
#  is the oracle: 0 if correct, MARKER if the defect is present.
#  [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] PTBR_VAL is
#  0x00000000aaaa1111 and the ptbr row expects it. apcb_flags is loaded from new_flags, and the flags row expects
#  0x00000000bbbb2222.  (regress23:F9: regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
setup = pcb(P_PCB_A, PTBR_VAL, FLAGS_VAL) + pcb(P_PCB_B, 0, 0)
setup += ["put d 0x%x, 0x%x" % (P_PTRV + 0,  k0(P_PCB_A)),
          "put d 0x%x, 0x%x" % (P_PTRV + 8,  k0(P_PCB_B)),
          "put d 0x%x, 0x%x" % (P_PTRV + 16, k0(P_PTRV))]

A0 = 16
prog = (load_const(T0, P_PTRV)          # identity-mapped, while ptbr is still 0
        + [LDQ(T0, 16, T0),             # t0 = K0SEG alias of the pointer vector
           LDQ(A0, 0, T0),              # a0 = &PCB_A  (K0SEG)
           LDQ(T3, 0, T0),              # t3 = &PCB_A  kept for the readback
           CALL_PAL(0x30),              # swpctx -> loads A; the defect sets apcb_ptbr = MARKER
           LDQ(A0, 8, T0),              # a0 = &PCB_B  -- t0 is K0SEG, so this survives
           CALL_PAL(0x30),              # swpctx -> SAVES apcb_ptbr into PCB_A+16
           LDQ(T2, 16, T3),             # t2 = that saved word
           LDQ(T4, 40, T3)])            # t4 = the saved FLAGS word (`swpctx flags')

code_cmds = ["put w 0x%x, 0x%08x" % (k0(P_CODE) + 4 * i, op) for i, op in enumerate(prog)]
t, alive = session(setup + code_cmds + ["pc=0x%x" % k0(P_CODE), "step %d" % len(prog),
                                        "print t2", "print t4"])
got = printed(t, "t2") if alive else "died"

row("swpctx alive", "alive" if alive else "died", "alive",
    "the guest survives two swpctx calls in K0SEG")

#  THE DEFECT ROW.  RED on the committed build (it reads MARKER), GREEN once :282 assigns
#  apcb_flags instead of apcb_ptbr.
row("swpctx ptbr", got, "0x%x" % PTBR_VAL,
    "PCB_A+16 must hold A.ptbr, not A.flags")

#  CLAUSE (b): pins the SPECIFIC wrong value, so a reinstatement of the defect is distinguishable
#  from any other way of getting the word wrong.
#  *** AN INEQUALITY PASSES ON EVERY NON-OBSERVATION.  Repaired 2026-09-07 after a probe-helper
#  audit found this row, and four siblings across three probes, green on "absent"/"died"/0x0 --
#  states in which nothing was measured at all.  `swpctx ptbr' reds on those, so the DETECTOR
#  never escaped; what was wrong was this row's own note, which claims a control it did not have.
#  Stated positively, a non-observation lands in the `got' column instead of scoring green. ***
obs = got.startswith("0x") and got != "0x0"
notflags = obs and got != ("0x%x" % FLAGS_VAL)
row("swpctx notflags", "yes" if notflags else got, "yes",
    "an OBSERVED word that is not A.flags -- absent/died/0x0 are setup failures, not passes")

#  AND NOT ZERO EITHER.  Zero is what an unmapped read returns, so it is the signature of a BROKEN
#  SETUP rather than of either code state.  Without this row a probe whose addresses drifted back
#  outside RAM would fail `swpctx ptbr' and pass `swpctx notflags', which reads like a real defect.
#  *** THE SECOND CONSEQUENCE, and this witness was BLIND to it until 2026-09-07. ***
#  `:282' assigns new_flags to apcb_ptbr, so apcb_flags is NEVER LOADED -- and the next SAVE then
#  publishes that never-loaded word into the outgoing PCB, wiping the flags the guest planted.
#
#  A fix review put it plainly: both rows above read the SAME cell (A+16), so a build that merely
#  stops clobbering PTBR -- delete `:282', or send new_flags to any other field -- scores a clean
#  sweep.  This row reads A+40, on the page `swpctx mapped' already proved is backed: 0 on HEAD (a
#  save of a field that was never loaded), FLAGS_VAL once the load is correct.
row("swpctx flags", printed(t, "t4"), "0x%x" % FLAGS_VAL,
    "PCB_A+40 must hold A.flags -- apcb_flags is never loaded on HEAD")

row("swpctx mapped", "yes" if obs else got, "yes",
    "a real nonzero readback -- 0x0/absent/died all mean the memory was never there")

ok = sum(1 for _, o in rows if o)
print("")
print("ALPHAHARNESS_RESULT=%d/%d" % (ok, len(rows)))
print("ALPHAHARNESS_DONE")
sys.exit(0 if ok == len(rows) else 1)
