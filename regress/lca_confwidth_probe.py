#!/usr/bin/env python3
#
#  lcaconfwidth -- RUNG-3 WITNESS: the LCA IOC_CONF kill diagnostic names a value the guard ACCEPTS.
#
#  THE DEFECT, dev_lca.c, `case LCA_IOC_CONF:'
#
#      d->ioc_conf = idata;                     /* the FULL 64-bit value is stored   */
#      if (idata & ~1) {                        /* the guard sees all 64 bits        */
#              fatal("TODO: Write to unimplemented bit of"
#                  " IOC_CONF: 0x%x\n", (int)idata);   /* the message sees 32        */
#              exit(1);
#      }
#
#  A guest `stq' of 0x100000000 sets bit 32.  `idata & ~1' is true, so the process dies -- and
#  `(int)idata' is 0, which is a value this guard ACCEPTS.  The kill message names an acceptable
#  value while killing on an unacceptable one.  That is the whole defect, and it is observable.
#
#  *** WHAT THIS PROBE IS AND IS NOT.  It is a WITNESS (rung 3): it shows the symptom on the
#  COMMITTED build, which is what licenses a fix.  It is not a detector and must not be gated --
#  a witness stays red until the fix lands. ***
#
#  ---------------------------------------------------------------------------------------------
#  FOUR THINGS THE DESIGN REVIEW (grok, 2026-09-07) KILLED BEFORE THIS WAS WRITTEN.  Each would
#  have produced a green or an unreadable run, and none is obvious from the source alone:
#
#  1. `load_const' CANNOT BUILD EITHER OPERAND.  LDA/LDAH make 32-bit sign-extended constants.
#     The K0SEG address needs bits 63..42 and the test value needs bit 32.  So both 64-bit words
#     are planted in RAM with debugger `put d' and loaded with `ldq' while `ptbr' is still 0 --
#     the same bootstrap alpha_harness_probe.py uses, and the only one that works.
#
#  2. DEBUGGER `dump' CANNOT BE THE READ-BACK.  `dump' calls memory_rw with NO_EXCEPTIONS, and
#     LCA registers DM_DEFAULT rather than DM_READS_HAVE_NO_SIDE_EFFECTS, so the handler is
#     SKIPPED and the caller gets the pre-zeroed buffer.  That is the UNMAPPED SIGNATURE PRODUCED
#     BY A HIT -- a false negative that looks exactly like a miss.  The read-back is a guest `ldq'.
#
#  3. `put d' OF THE KILLING VALUE IS NOT RUNG-3.  store_64bit_word goes through memory_rw with
#     CACHE_DATA and no NO_EXCEPTIONS, so it DOES enter the handler and exit(1)s -- a real kill,
#     caused by no guest instruction.  The killing store must be a guest `stq'.
#
#  4. A MISS IS NOT ONLY "UNMAPPED -> NOTHING".  Offset 0 of the window is LCA_IOC_BASE (HAE),
#     which `break's with no kill.  A store to k0(0x180000000) is SILENT WHILE INSIDE the LCA
#     window.  Unmapped and HAE both read back 0, so the control has to tell them apart -- which
#     is what `ioc rt' does: only the real IOC_CONF arm stores AND returns the value.
#
#  ---------------------------------------------------------------------------------------------
#  HONEST LIMIT, stated because the row must not claim a language guarantee: `(int)0x100000000 == 0'
#  is IMPLEMENTATION-DEFINED, not C99.  GCC and Clang truncate to the low 32 bits, which is what
#  this tree is built with, so the witness holds on this build and is not a statement about C.
#
#  Usage:  lca_confwidth_probe.py <gxemul-binary> [label]
import os, sys, pty, select, time, re, struct

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
MACH  = "alphabook1"          #  device_add(machine, "lca") is ST_ALPHABOOK1 ONLY

rows = []
def row(name, got, want, note="", negate=False):
    ok = (got != want) if negate else (got == want)
    rows.append((name, ok))
    shown = ("NOT " + str(want)) if negate else str(want)
    print("%-16s %-22s %-24s %-46s %s" % (name, str(got), shown, note, "ok" if ok else "FAIL"))
    return ok

# ---------------------------------------------------------------- encoder (memory format only)
ZERO, T0, T1, T2, T3 = 31, 1, 2, 3, 4

def mem(op, ra, rb, disp):
    assert -32768 <= disp <= 32767, "displacement %d out of range" % disp
    return (op << 26) | (ra << 21) | (rb << 16) | (disp & 0xffff)

def LDA (ra, disp, rb=ZERO): return mem(0x08, ra, rb, disp)
def LDAH(ra, disp, rb=ZERO): return mem(0x09, ra, rb, disp)
def LDQ (ra, disp, rb):      return mem(0x29, ra, rb, disp)
def STQ (ra, disp, rb):      return mem(0x2d, ra, rb, disp)

def load_const(reg, val):
    #  32-bit only, and deliberately so: this builds the SCRATCH pointer, never a 64-bit operand.
    lo = val & 0xffff
    hi = (val >> 16) & 0xffff
    if lo & 0x8000:                      # LDA sign-extends its displacement
        hi = (hi + 1) & 0xffff
    ops = [LDAH(reg, hi if hi < 0x8000 else hi - 0x10000)]
    ops.append(LDA(reg, lo if lo < 0x8000 else lo - 0x10000, reg))
    return ops

# ---------------------------------------------------------------- addresses (ALL RAM < 64 MB)
K0SEG       = 0xfffffc0000000000
def k0(p):  return K0SEG | p

LCA_IOC_BASE = 0x180000000
LCA_IOC_CONF = LCA_IOC_BASE + 0x020          # alpha_lcareg.h
SCRATCH      = 0x01020000                    # the three 64-bit words live here
CODE         = 0x01040000
LEGAL        = 0x1                           # 1 & ~1 == 0 -> accepted, no kill
KILLER       = 0x100000000                   # bit 32 -> guard fires; (int) of it is 0

#  The same guard the Alpha harness needed: an address past physical_max is written to nothing and
#  read back as zero, SILENTLY.  -M 64 gives 64 MB.
assert max(SCRATCH, CODE) < 64 * 1024 * 1024, "scratch/code must be inside RAM"

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
        if not rd(spin if i == len(cmds) - 1 else 0.3):
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

print("lca_confwidth_probe -- binary=%s label=%s machine=%s" % (BIN, LABEL, MACH))
print("%-16s %-22s %-24s %-46s %s" % ("row", "got", "want", "note", ""))

# ---------------------------------------------------------------- SESSION 1: liveness + control
#  Everything up to and including the legal round-trip, WITHOUT the killing store, so these rows
#  are readable on a build where the killing store would end the process.
setup = ["put d 0x%x, 0x%x" % (SCRATCH + 0,  k0(LCA_IOC_CONF)),
         "put d 0x%x, 0x%x" % (SCRATCH + 8,  LEGAL),
         "put d 0x%x, 0x%x" % (SCRATCH + 16, KILLER)]

prog_ctl = (load_const(T0, SCRATCH) +
            [LDQ(T1, 0, T0),        # t1 = k0(LCA_IOC_CONF)
             LDQ(T2, 8, T0),        # t2 = 0x1
             STQ(T2, 0, T1),        # LEGAL store into the device
             LDQ(T3, 0, T1)])       # guest read-back through the SAME decode
cmds = setup + ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog_ctl)]
cmds += ["pc=0x%x" % k0(CODE), "step %d" % len(prog_ctl), "print t3"]
t1txt, alive1 = session(cmds)

row("live", "alive" if alive1 else "dead", "alive",
    "the control session survives the legal write")
row("ioc rt", printed(t1txt, "t3"), "0x1",
    "guest stq 0x1 then guest ldq through the SAME decode")

# ---------------------------------------------------------------- SESSION 2: the killing store
#  The killing store is LAST because nothing runs after it.
prog_kill = (load_const(T0, SCRATCH) +
             [LDQ(T1, 0, T0),       # t1 = k0(LCA_IOC_CONF)
              LDQ(T2, 16, T0),      # t2 = 0x100000000
              STQ(T2, 0, T1)])      # THE KILLING STORE
cmds = setup + ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog_kill)]
cmds += ["pc=0x%x" % k0(CODE), "step %d" % len(prog_kill)]
t2txt, alive2 = session(cmds)

#  *** PARSE THE VALUE; DO NOT SUBSTRING-MATCH IT. ***
#  These rows used `"IOC_CONF: 0x100000000" in text'.  A message of 0x1000000000 -- one extra
#  literal zero, a plausible edit at this very site -- CONTAINS that string, so the row went
#  GREEN on a wrong diagnostic, and the displayed `got' was manufactured from the boolean rather
#  than read from the output.  `zero' had the mirror flaw (0x0abc contains 0x0).
#  Found by a pass-2 review of this round, not by the round itself.
m_ioc = re.search(r"IOC_CONF: (0x[0-9a-fA-F]+)", t2txt)
hit   = m_ioc is not None
ioc   = int(m_ioc.group(1), 16) if m_ioc else None
shown = ("0x%x" % ioc) if m_ioc else "absent"
zero  = (ioc == 0)
full  = (ioc == KILLER)

#  *** ORACLE POLARITY.  The ladder requires a witness to show the symptom on the PRE-FIX build and
#  go GREEN post-fix WITH THE SAME SCRIPT.  So these rows assert the CORRECT behaviour and are
#  expected to FAIL here.  The first draft of this probe asserted the DEFECT as the passing state
#  and scored 6/6 on the committed build -- which reads as success and would have gone RED the
#  moment the bug was fixed.  That is a detector-of-the-defect wearing a witness's clothes, and it
#  is the opposite of what clause (i) asks for. ***
row("kill fired", "yes" if hit else "no", "yes",
    "CONTROL: the IOC_CONF guard announced -- not HAE, not unmapped, not a skipped handler")
row("kill width", shown, "0x%x" % KILLER,
    "the message must name the value that ACTUALLY killed")
#  *** AN INEQUALITY PASSES ON EVERY NON-OBSERVATION.  Repaired 2026-09-07 -- see the same note
#  in alpha_harness_probe.py.  With the diagnostic REMOVED but the terminating call kept, `shown'
#  is "absent", which is != "0x0" and scored GREEN.  `kill fired' reds on that, so the detector
#  did not escape; this row's note claimed a control it did not have. ***
notzero = hit and ioc != 0
row("kill notzero", "yes" if notzero else shown, "yes",
    "the diagnostic must NAME a nonzero value -- 0x0 is a value this guard ACCEPTS, and 'absent' is no diagnostic at all")
row("died", "died" if not alive2 else "alive", "died",
    "CONTROL: exit(1) really ran -- distinguishes a kill from a silent decline")

ok = sum(1 for _, o in rows if o)
print()
print("LCACONF_RESULT=%d/%d" % (ok, len(rows)))
print("LCACONF_DONE")
sys.exit(0 if ok == len(rows) else 1)
