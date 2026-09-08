#!/usr/bin/env python3
#
#  lcaconfbus1kill -- RUNG-3 WITNESS: an ACCEPTED write to LCA_IOC_CONF arms a host kill in a
#  DIFFERENT handler, reached by an ordinary guest load with no rejected value anywhere on the path.
#
#  THE DEFECT, two handlers in `dev_lca.c':
#
#      DEVICE_ACCESS(lca_ioc), case LCA_IOC_CONF:
#              d->ioc_conf = idata;
#              /*  Only bit 0 is implemented so far, the PCI bus 0 vs bus non-0 selection bit.  */
#              if (idata & ~1) { fatal(...); exit(1); }     <-- 0x1 PASSES.  Accepted and stored.
#
#      DEVICE_ACCESS(lca_pci_conf):
#              bus = d->ioc_conf & 1;
#              if (bus == 0) { ...dev scan, already de-fatalised... }
#              else { fatal("TODO. Non-zero bus.\n"); exit(1); }
#
#  So: guest stores 0x1 to IOC_CONF (accepted), then ANY access in the PCI config window ends the
#  host.  Two ordinary accesses; nothing is refused.
#
#  *** WHY THIS IS A SEPARATE FILE AND NOT A SESSION IN lca_confwidth_probe.py. ***  That probe is a
#  SHIPPED witness with its own contract (HEAD 4/6, fix 6/6) recorded in the wiring manifest.  Adding
#  rows to a shipped detector perturbs its RESULT line and its recorded scores, and this defect is a
#  separate queue row with a separate disposition.  The ENCODERS and the session driver are copied
#  deliberately -- probes in this tree are standalone by design.
#
#  ---------------------------------------------------------------------------------------------
#  DESIGN REVIEWED BY THE grok SEAT, 2026-09-07, AFTER codex REFUSED THE BRIEF ON A CONTENT FILTER
#  (regress/artifacts/lcaconfbus1kill/grok_witness_20260907.txt).  VERDICT: SOUND.  Four corrections
#  from that review are built in here and are NOT optional:
#
#    1.  ONE PROCESS, NOT TWO SESSIONS.  The control read and the armed read happen in the SAME
#        emulator run, so ONLY `ioc_conf' differs between them.  Two separate sessions would leave a
#        residual that something else differed before the debugger prompt.
#    2.  S2 IS A READ, NOT A WRITE.  Both reach the kill.  But an empty-slot WRITE makes
#        `bus_pci_data_access' print "[ ... write to non-existant device ... ]", so the CONTROL
#        would carry a second fatal() on stderr.  An empty-slot READ of reg 0 is the architectural
#        ID probe and is silent.
#    3.  LIVENESS IS NOT `ioc rt'.  That row (in the sibling probe) proves the WRITER round-trips;
#        it says nothing about THIS window.  Liveness here is the control read SURVIVING and
#        returning the empty-slot signature.
#    4.  STAY ON `step'.  `continue' would make `lca_interrupt_assert'/`_deassert' -- bare
#        fatal()+exit(1) stubs with no guard -- a confounder.
#
#  THREE TRAPS THE SIBLING PROBE ALREADY PAID FOR, and none recurs here:
#    *  debugger `dump' skips DM_DEFAULT handlers and would return the #95 pre-zero, making both
#       reads look unmapped.  Every access below is a guest instruction.
#    *  a debugger `put d' of a killing value IS a host kill but is NOT a guest instruction, so it
#       witnesses nothing.  The arming store is a guest `stq'.
#    *  HAE at window offset 0 silently succeeds -- but that is `LCA_IOC_BASE+0' in `lca_ioc'.
#       `lca_pci_conf' has NO per-offset special case, so `LCA_PCI_CONF+0' is a clean control.
#
#  *** CONTRACT -- WHAT THIS WITNESSES AND WHAT IT DOES NOT. ***
#  It establishes: on unmodified `alphabook1', an ACCEPTED `stq 0x1' to CONF followed by ANY access
#  in the PCI config window produces a host exit(1) whose diagnostic is this arm, with no rejected
#  value on the path.  It does NOT establish that any shipped guest does this, and it is NOT a
#  detector of the repair: "host survives" greens equally for a silent return, for a latched
#  announce, and for falling through into bus_pci with cur_bus=1 (empty type-1 also survives).  A
#  fix round owes a row that discriminates those.  Do not read a green here as "type-1 is modelled".
#
#  Usage:  lca_confbus_probe.py <gxemul-binary> [label]
import os, sys, pty, select, time, re

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
MACH  = "alphabook1"          #  device_add(machine, "lca") is ST_ALPHABOOK1 ONLY

rows = []
def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-14s %-24s %-24s %-52s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
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
    if lo >= 0x8000:
        hi = (hi + 1) & 0xffff
    ops = [LDAH(reg, hi if hi < 0x8000 else hi - 0x10000)]
    if lo:
        ops.append(LDA(reg, lo if lo < 0x8000 else lo - 0x10000, reg))
    return ops

# ---------------------------------------------------------------- addresses (ALL RAM < 64 MB)
K0SEG        = 0xfffffc0000000000
def k0(p):   return K0SEG | p

LCA_IOC_BASE = 0x180000000
LCA_IOC_CONF = LCA_IOC_BASE + 0x020      # alpha_lcareg.h
LCA_PCI_CONF = 0x1e0000000               # alpha_lcareg.h; DEVINIT maps 0x20000000 bytes here
SCRATCH      = 0x01020000
CODE         = 0x01040000
LEGAL        = 0x1                       # `idata & ~1' == 0 -> ACCEPTED by the CONF guard

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

def printed(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return "absent" if not m else "0x%x" % int(m.group(1), 16)

print("lca_confbus_probe -- binary=%s label=%s machine=%s" % (BIN, LABEL, MACH))
print("%-14s %-24s %-24s %-52s %s" % ("row", "got", "want", "note", ""))

# ---------------------------------------------------------------- the single session
#  Register discipline: T0 holds the SCRATCH base and is CLOBBERED last, after both pointers are
#  loaded, so only four temporaries are needed.
setup = ["put d 0x%x, 0x%x" % (SCRATCH + 0,  k0(LCA_IOC_CONF)),
         "put d 0x%x, 0x%x" % (SCRATCH + 8,  LEGAL),
         "put d 0x%x, 0x%x" % (SCRATCH + 16, k0(LCA_PCI_CONF))]

lc      = load_const(T0, SCRATCH)
prologue = lc + [LDQ(T1, 16, T0),   # t1 = k0(LCA_PCI_CONF)
                 LDQ(T3, 0,  T0),   # t3 = k0(LCA_IOC_CONF)
                 LDQ(T0, 8,  T0),   # t0 = 0x1   (base clobbered LAST -- both pointers are loaded)
                 LDQ(T2, 0,  T1)]   # [A] CONTROL read of PCI config, with ioc_conf == 0
armed    = [STQ(T0, 0, T3),         # [B] the ACCEPTED store: ioc_conf = 1
            LDQ(T2, 0, T1)]         # [C] the SAME read again -- now bus == 1

prog = prologue + armed
cmds = setup + ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog)]
cmds += ["pc=0x%x" % k0(CODE),
         "step %d" % len(prologue),    # run up to and including the CONTROL read
         "print t2",                   # its value, while the host is certainly still alive
         "step %d" % len(armed)]       # the accepted store, then the armed read
txt, alive = session(cmds)

ctl = printed(txt, "t2")

#  ---- CONTROL 1: the same access, same address, same width, SURVIVES with ioc_conf == 0 --------
#  This is what attributes any later death to the VALUE and not to the address, the width, or the
#  fact that the window was touched at all.
row("bus ctl", "yes" if ctl != "absent" else "absent", "yes",
    "CONTROL: identical read at ioc_conf==0 completed and printed")

#  ---- CONTROL 2: DEVICE SIGNATURE on the control -----------------------------------------------
#  grok: an empty-slot read returns 0xffffffffffffffff via memory_writemax64; UNMAPPED returns 0.
#  So this distinguishes "reached lca_pci_conf and probed an absent device" from "missed the device".
row("bus ctlsig", ctl, "0xffffffffffffffff",
    "DEVICE SIGNATURE: empty-slot ID probe; unmapped would read 0")

#  ---- THE DEFECT ROW ---------------------------------------------------------------------------
#  ORACLE POLARITY: the ladder requires the witness to show the symptom on the PRE-FIX build and go
#  GREEN post-fix with the SAME script, so this asserts the CORRECT behaviour.
#  PRE-FIX  -> "dead"  -> RED.        POST-FIX -> "alive" -> GREEN.
row("bus kill", "alive" if alive else "dead", "alive",
    "an ACCEPTED stq 0x1 then an ordinary ldq must NOT end the host")

#  ---- ATTRIBUTION: if it died, it died HERE ----------------------------------------------------
#  Green in BOTH directions by construction, and RED only if the host dies WITHOUT this arm's
#  diagnostic -- i.e. if something else killed it.  The literal is unique in src/ (one site).
sig = ("TODO. Non-zero bus." in txt)
row("bus attrib", "yes" if (alive or sig) else "died-elsewhere", "yes",
    "ATTRIBUTION: a death here must carry THIS arm's unique diagnostic")

#  *** ECHO THE EVIDENCE INTO THIS LOG. ***  The first run of this probe passed `bus attrib' by
#  testing the PTY buffer and printing nothing, so the PRESERVED artifact carried no trace of the
#  diagnostic the row rests on -- a green row whose evidence a later reader cannot check.  The
#  literal is unique in src/ (one site, dev_lca.c:133; a second grep hit is the .o).
for _l in txt.split(chr(10)):
    if "Non-zero bus" in _l or "lca_ioc: unimplemented" in _l:
        print("  EVIDENCE: %s" % _l.strip())

ok = sum(1 for _, o in rows if o)
print("")
print("LCACONFBUS_RESULT=%d/%d" % (ok, len(rows)))
print("LCACONFBUS_WITNESS=%s" % ("PASS" if ok == len(rows) else "FAIL"))
print("LCACONFBUS_DONE")
