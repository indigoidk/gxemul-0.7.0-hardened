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

# ================================================================================================
#  #515: THE DISCRIMINATING ROWS THIS PROBE'S OWN CONTRACT SAYS THE FIX ROUND OWES.
#
#  The contract at the top of this file states the blind spot in its own words: *"host survives"
#  greens equally for a silent return, for a latched announce, and for falling through into bus_pci
#  with cur_bus=1 (empty type-1 also survives).  A fix round owes a row that discriminates those.*
#
#  IT IS RIGHT, AND THE REASON IS EXACT: the chosen repair's refusal arm returns the empty-slot
#  signature ITSELF -- all-ones at register 0, zero elsewhere -- because that is what
#  `bus_pci_data_access' returns from its own `dev == NULL' arm (bus_pci.c, VERIFIED by reading it,
#  not taken from a seat).  So a READ cannot tell a refusal from a forward to an empty bus-1 slot:
#  both produce 0xffff...ffff.
#
#  *** THE DISCRIMINATOR IS A WRITE. ***  An empty-slot WRITE is not silent -- it prints
#
#      [ bus_pci_data_access(): write to non-existant device, bus %i func %i device %i ]
#
#  naming `cur_bus', `cur_func' and `cur_device'.  That ONE channel does three separate jobs:
#
#    *  it proves FORWARDING HAPPENED at all (a refusal prints nothing);
#    *  it names WHERE the decode landed -- so this is an ANCHORED row in the carrier's clause-(f)
#       sense, absolute rather than relative.  "If every address in this device shifted, which row
#       reds?"  THIS one: the printed tuple changes.  A distinctness or survival oracle cannot see
#       a translation at all;
#    *  its ABSENCE at the bus-zero address proves the type-1/bus-0 alias is REFUSED rather than
#       forwarded onto the primary bus -- which is the misrouting the repair exists to prevent, and
#       which no survival oracle can observe because a misroute survives happily.
#
#  ADDRESS DERIVATION, from the handler's own two lines rather than from a table:
#
#      reg = (relative_addr >> 5) & 0xfc          tag = (relative_addr >> 5) & ~0xff
#      type-1:  bus = (tag >> 16) & 0xff   dev = (tag >> 11) & 0x1f   func = (tag >> 8) & 7
#      type-0:  dev = first d with tag & (0x800U << d)
#
#      bus 1, dev 3, func 2, reg 0  ->  tag = 0x11a00  ->  relative_addr = 0x234000
#      bus 0 (the alias)            ->  tag = 0x00000  ->  relative_addr = 0x000000
#      type-0 dev 7 (i82378zb)      ->  tag = 0x40000  ->  relative_addr = 0x800000
#
#  dev/func/bus are deliberately DISTINCT and non-zero (1/3/2) so a swapped field cannot pass by
#  coincidence -- the hand-assembled-encoding trap in its address-decode form.

#  *** THE BYTE-ENABLE BITS ARE PART OF THE ADDRESS A DRIVER FORMS, AND THE FIRST VERSION OF THESE
#  CONSTANTS OMITTED THEM.  Found by the minimax seat on pass 2, checked, and correct. ***
#
#  The handler's own comment gives the driver-side construction in full:
#
#      addr = tag << 5 | (regoffset & ~0x03) << 5 | 0x3 << 3
#
#  -- so for register 0 a real address is `tag << 5 | 0x18', not `tag << 5'.  The handler then
#  discards bits 4..0 with `>> 5', so BOTH forms decode identically and the earlier measurement was
#  not wrong.  But driving the form a driver never emits, and then writing that the printed tuple
#  "confirmed the address", overstated what was confirmed: THE TUPLE CONFIRMS THE TAG DECODE, NOT
#  THE ADDRESS CONSTRUCTION.  Including the bits costs nothing and makes the probe drive what
#  NetBSD's lca_pci.c drives, so the claim and the artifact now agree.
BYTE_ENABLES = 0x3 << 3              # `0x3 << 3' from the handler's own comment; reg 0

T1_ADDR = LCA_PCI_CONF + 0x234000 + BYTE_ENABLES   # type-1 -> bus 1, dev 3, func 2, reg 0
T1_ZERO = LCA_PCI_CONF + 0x000000 + BYTE_ENABLES   # type-1 -> bus 0  == THE ALIAS, must be refused
T0_DEV7 = LCA_PCI_CONF + 0x800000 + BYTE_ENABLES   # type-0 -> dev 7  == the registered i82378zb
T0_EMPTY = LCA_PCI_CONF + 0x200000 + BYTE_ENABLES   # type-0 -> dev 5, an EMPTY bus-0 slot
T1_DEV7  = LCA_PCI_CONF + 0x070000 + BYTE_ENABLES   # type-1 -> bus 0, dev 7 == THE MISROUTING
#  tag = 7 << 11 = 0x3800 -> bus (0x3800>>16)&0xff = 0, dev (0x3800>>11)&0x1f = 7, func 0, reg 0.
#  0:7:0 IS the i82378zb.  This is the ONLY address at which forwarding the alias is OBSERVABLE:
#  at every other bus-0 slot the forward hits an empty slot and returns the same all-ones the
#  refusal synthesises.

#  *** PINNED FROM THE PRE-FIX BUILD, AND THAT IS THE CORRECT POLARITY FOR AN ACCEPT ROW. ***
#  The fix does not intend to change type-0 service at all, so the PRE-FIX build is the authority on
#  what a real device read returns.  Pinning it here is not fitting the oracle to the binary -- it is
#  the accept side of the predicate the fix ADDS, which the de-escalation clause requires, and its
#  kill is a mutant that routes type-0 into the refusal arm.  Measured on /tmp/gxlca (baseline
#  5d3f82c) before the fix was written; see artifacts/lcaconfbus1kill/.
T0_PIN = "0x304848086"   # MEASURED on /tmp/gxlca (baseline 5d3f82c), pre-fix
#  0x0000_0003_0484_8086 -- an 8-byte read spans config registers 0 and 4:
#      reg 0  0x04848086 = PCI_ID_CODE(0x8086 Intel, 0x0484 SIO)  -- the i82378zb
#      reg 4  0x00000003             = command 0x0003, status 0x0000
#  Derived independently from bus_pci.c's PCIINIT(i82378zb) and then MEASURED; the two
#  agree, which is the check the hand-assembled-encoding trap asks for.

# ---- SESSION 2: type-1 forwarding, and the bus-zero alias ---------------------------------------
#  Register discipline as in session 1: the SCRATCH base in T0 is clobbered LAST, after every
#  pointer is loaded, so four temporaries suffice.
setup2 = ["put d 0x%x, 0x%x" % (SCRATCH + 0,  k0(LCA_IOC_CONF)),
          "put d 0x%x, 0x%x" % (SCRATCH + 8,  LEGAL),
          "put d 0x%x, 0x%x" % (SCRATCH + 16, k0(T1_ADDR)),
          "put d 0x%x, 0x%x" % (SCRATCH + 24, k0(T1_ZERO))]

prog2 = load_const(T0, SCRATCH) + [
    LDQ(T1, 16, T0),      # t1 = k0(T1_ADDR)
    LDQ(T2, 24, T0),      # t2 = k0(T1_ZERO)
    LDQ(T3, 0,  T0),      # t3 = k0(LCA_IOC_CONF)
    LDQ(T0, 8,  T0),      # t0 = 1        (base clobbered LAST)
    STQ(T0, 0,  T3),      # ioc_conf = 1  -- ACCEPTED by the CONF guard
    STQ(T0, 0,  T2),      # [E] type-1 write, bus 0  -> must be REFUSED and name nothing
    STQ(T0, 0,  T1)]      # [D] type-1 write, bus 1  -> must FORWARD and name the tuple
#  *** THE ORDER IS LOAD-BEARING: [E] BEFORE [D], SO [D]'s TUPLE IS A POST-ALIAS CHECKPOINT. ***
#  The kimi seat refused to ratify the first binding of `t1 alias' and was right.  Binding the row to
#  `alive2' rules out "the host died before [E]" -- but `alive2' only means THE HOST PROCESS SURVIVED.
#  It does not mean the guest EXECUTED [E].  A wrong `step' count, or a trap before the store, leaves
#  the host alive, prints nothing, and the row passes: the same absence-read-as-a-result shape one
#  level up from the one the earlier repair fixed.
#
#  Running the alias FIRST turns the anchor's own diagnostic into the positive term: `bus 1 func 2
#  device 3' can only be printed by [D], and [D] is AFTER [E], so seeing it proves [E] was executed
#  and produced no output.  Absence is now conditioned on a marker that had to be RETIRED, which is
#  exactly what the seat asked for -- and it costs one line swap and no extra session.

cmds2 = setup2 + ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog2)]
cmds2 += ["pc=0x%x" % k0(CODE), "step %d" % len(prog2)]
txt2, alive2 = session(cmds2)

#  *** TERMINATED MATCH -- A FALSE-GREEN FOUND BY THE codex SEAT ON PASS 2. ***
#  The diagnostic's last field is a bare `%i' followed by " ]":
#
#      fatal("[ bus_pci_data_access(): write to non-existant"
#            " device, bus %i func %i device %i ]" ...)
#
#  `dev' is `(tag >> 11) & 0x1f', so it ranges 0..31 -- and the SUBSTRING "device 3" is contained in
#  "device 30" and "device 31".  A decode mutant yielding either (e.g. `(tag >> 11) | 0x1c') would
#  therefore PASS the anchor while landing at the wrong device.  Enumerated rather than argued:
#  of 0..31, exactly {3, 30, 31} contain the text "device 3".
#
#  Including the closing " ]" makes every match exact at the numeric boundary.  It costs two
#  characters and it removes the whole class, not just the two values that motivated it.
#
#  *** NONE of this round's ten mutants produces 30 or 31, so no measured score moves.  It is a
#  hole in the ORACLE, closed pre-ship. ***  Recorded that way rather than as a score change,
#  because claiming a mutant was rescued when none was would be a wrong record.
FWD = "bus 1 func 2 device 3 ]"
ALIAS = "bus 0 func 0 device 0 ]"

row("t1 alive", "alive" if alive2 else "dead", "alive",
    "a type-1 write to a NON-zero bus must not end the host")

row("t1 anchor", "yes" if FWD in txt2 else "no", "yes",
    "ANCHOR: forwarding happened AND landed at bus 1 dev 3 func 2")

#  *** THIS ROW WAS VACUOUS AS FIRST WRITTEN, AND THE PRE-FIX RUN IS WHAT SAID SO. ***  It read
#  `refused if ALIAS not in txt2', which scored GREEN on the pre-fix build -- where the host had
#  already died at [D] and access [E] NEVER EXECUTED.  An absence-of-text oracle cannot tell "the
#  access ran and was refused" from "the access never ran", which is this project's
#  pattern-that-matched-nothing class in its purest form: a phantom absence read as a result.
#  Binding it to `alive2' makes the two states render differently, per the oldest rule here --
#  an unrun check and a passing one must never look the same.
#  THREE distinguishable outcomes, so no two failure modes render alike:
#     no-checkpoint  the anchor store never printed -> [E] is not proven to have run
#     forwarded      the alias reached bus_pci and named the primary bus  -> the misrouting
#     refused        [E] demonstrably ran (the later checkpoint fired) and named nothing
if not alive2:
    _alias = "died"
elif FWD not in txt2:
    _alias = "no-checkpoint"      # POST-ALIAS CHECKPOINT absent: [E] not proven executed
elif ALIAS in txt2:
    _alias = "forwarded"
else:
    _alias = "refused"
row("t1 alias", _alias, "refused",
    "type-1 with bus 0 must NOT be forwarded (checkpointed by the later anchor store)")

for _l in txt2.split(chr(10)):
    if "non-existant" in _l:
        print("  EVIDENCE(S2): %s" % _l.strip())

# ---- SESSION 2b: the REFUSAL'S RETURN VALUE ------------------------------------------------------
#  *** THIS ROW EXISTS BECAUSE I ENUMERATED THE CLAUSE-(d) CLOSURE AND FOUND MY OWN ANSWER WRONG. ***
#  Writing the pass-2 brief I claimed the (type-1, bus == 0, READ) cell was unobservable, "because it
#  returns the same all-ones value as the control".  That reasoning conflates two different accesses:
#  the control is a TYPE-0 empty-slot read, and this is the REFUSAL arm's own synthesised value.  They
#  agree on the fix and they do NOT agree under a mutant.
#
#  The refusal's repair is one expression -- `odata = reg == 0? (uint64_t) -1 : 0'.  NULL IT
#  (`odata = 0') and every row above still passes: the alias is otherwise exercised only by a WRITE,
#  whose `odata' is never read, and the two control reads take the type-0 path.  So the canonical
#  clause-(d) mutant on the refusal's own repair SWEEPS the detector clean without this row.
#
#  A type-1 READ at the alias is therefore the cell that pins the refusal's VALUE, as distinct from
#  `t1 alias', which pins only that forwarding did not happen.
setup2b = ["put d 0x%x, 0x%x" % (SCRATCH + 0, k0(LCA_IOC_CONF)),
           "put d 0x%x, 0x%x" % (SCRATCH + 8, LEGAL),
           "put d 0x%x, 0x%x" % (SCRATCH + 16, k0(T1_ZERO))]
prog2b = load_const(T0, SCRATCH) + [
    LDQ(T1, 16, T0),      # t1 = k0(T1_ZERO)
    LDQ(T3, 0,  T0),      # t3 = k0(LCA_IOC_CONF)
    LDQ(T0, 8,  T0),      # t0 = 1     (base clobbered LAST)
    STQ(T0, 0,  T3),      # ioc_conf = 1
    LDQ(T2, 0,  T1)]      # [F] type-1 READ at the alias -> the refusal's synthesised value
cmds2b = setup2b + ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog2b)]
cmds2b += ["pc=0x%x" % k0(CODE), "step %d" % len(prog2b), "print t2"]
txt2b, alive2b = session(cmds2b)
t1rd = printed(txt2b, "t2")

row("t1 rdval", t1rd if alive2b else "died", "0xffffffffffffffff",
    "the refusal must synthesise the empty-slot signature at register 0")

# ---- SESSION 2d: THE MISROUTING CELL -- the one the fix's own comment names ----------------------
#  *** A FLOOR BREACH FOUND BY THE grok SEAT ON PASS 2, AND IT CAUGHT AN ERROR IN MY OWN PRE-TABLE
#  CHANNEL LINE -- which is the CHANNEL check catching its own table. ***
#
#  PRETABLE section 4 asserted that `t1 alias' kills `M4_condwrite' via the presence of
#  `bus 0 func 0 device 0'.  grok walked it and that is FALSE, in the mirror polarity:
#
#      if (type1 && bus == 0 && writeflag == MEM_WRITE)
#          t1 alias  is a WRITE at 0:0:0 -> still refused        -> still green
#          t1 rdval  is a READ  at 0:0:0 -> forwarded to an EMPTY slot, all-ones -> still green
#          t1 anchor is bus 1            -> unchanged            -> still green
#      CLEAN SWEEP OF THE ELEVEN-ROW PROBE.
#
#  My own mutant used the OPPOSITE polarity (`== MEM_READ'), which `t1 alias' does kill.  So I had
#  repaired the cell at exactly the address my mutant used and left the symmetric cell open -- the
#  same shape the carrier records from `#499', reproduced inside the table built to prevent it.
#
#  *** THE ROOT CAUSE IS THE ADDRESS, NOT THE POLARITY: EVERY ALIAS ROW USED dev 0, AN EMPTY SLOT.
#  Forwarding to an empty slot returns the SAME all-ones the refusal synthesises, so no dev-0 row can
#  ever observe the misrouting.  The fix's own comment names the right address and no row used it:
#  "would ... hand the access to whichever primary-bus device matched -- `i82378zb' is registered at
#  0:7:0".  At 0:7:0 the two outcomes differ ABSOLUTELY -- refusal gives all-ones, a misroute gives
#  the device's real config data. ***
setup2d = ["put d 0x%x, 0x%x" % (SCRATCH + 0,  k0(LCA_IOC_CONF)),
           "put d 0x%x, 0x%x" % (SCRATCH + 8,  LEGAL),
           "put d 0x%x, 0x%x" % (SCRATCH + 16, k0(T1_DEV7))]
prog2d = load_const(T0, SCRATCH) + [
    LDQ(T1, 16, T0),      # t1 = k0(T1_DEV7)
    LDQ(T3, 0,  T0),      # t3 = k0(LCA_IOC_CONF)
    LDQ(T0, 8,  T0),      # t0 = 1      (base clobbered LAST)
    STQ(T0, 0,  T3),      # ioc_conf = 1
    STQ(T0, 0,  T1),      # [H] type-1 WRITE at 0:7:0 -> must be refused, naming nothing
    LDQ(T2, 0,  T1)]      # [I] type-1 READ  at 0:7:0 -> must NOT return the device's data
cmds2d = setup2d + ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog2d)]
cmds2d += ["pc=0x%x" % k0(CODE), "step %d" % len(prog2d), "print t2"]
txt2d, alive2d = session(cmds2d)
d7 = printed(txt2d, "t2")
#  *** THIS ROW WAS VACUOUS BY CONSTRUCTION AND THE KILL TABLE'S OWN EVIDENCE ECHO CAUGHT IT --
#  not the row, which would have scored GREEN under the mutant it exists to kill. ***
#
#  I first matched the EMPTY-SLOT write diagnostic, `bus %i func %i device %i ]'.  That message comes
#  from `bus_pci_data_access''s `dev == NULL' arm -- and 0:7:0 is precisely the address where a
#  device DOES exist.  So at the one address chosen to make the misrouting observable, the chosen
#  channel CANNOT FIRE, for any mutant, ever.
#
#  That is exactly the vacuity the PRE-TABLE CHANNEL check is meant to catch -- *"a row whose named
#  channel cannot vary under its named mutant is VACUOUS BY CONSTRUCTION, and that is knowable at
#  writing time"* -- and I made the error while writing the row that answers an earlier instance of
#  it.  What actually caught it was the probe's habit of echoing its evidence lines into the log,
#  where the M4a run printed the REAL message a forwarded write produces:
#
#      [ bus_pci: write to PCI DATA: data = 0x00000001 (current value = 0x304848086);
#        NOT YET SUPPORTED. bus 0, device 7, function 0 (i82378zb) register 0x00 ]
#
#  A registered device answers on a DIFFERENT path with a DIFFERENT message, and that message is a
#  strictly better oracle: it names the device BY NAME and quotes the config data the write landed
#  on.  Nothing but a real forward to the real i82378zb can produce it.
D7W = "device 7, function 0 (i82378zb)"

#  THE READ ROW.  Its want is the refusal's signature; its ANTI-want is T0_PIN, the device's real
#  data -- so this row is ANCHORED in clause (f)'s sense: it does not merely assert distinctness,
#  it names WHICH cell was reached, by a value only that one device can produce.
row("t1 dev7rd", d7 if alive2d else "died", "0xffffffffffffffff",
    "MISROUTING: a refused alias must NOT return 0:7:0's real config data")

#  THE WRITE ROW.  Absence again -- but checkpointed, because [I] follows [H] and `print t2' only
#  produces a value if [I] executed.  A missing checkpoint renders differently from a clean refusal.
if not alive2d:
    _d7w = "died"
elif d7 == "absent":
    _d7w = "no-checkpoint"
elif D7W in txt2d:
    _d7w = "forwarded"
else:
    _d7w = "refused"
row("t1 dev7wr", _d7w, "refused",
    "MISROUTING: a refused alias WRITE must not land on the real i82378zb")

for _l in txt2d.split(chr(10)):
    if "non-existant" in _l or "NOT YET SUPPORTED" in _l:
        print("  EVIDENCE(S2d): %s" % _l.strip())

# ---- SESSION 2c: THE TYPE-0 WRITE CELL -----------------------------------------------------------
#  *** THIS ROW WAS PRESCRIBED BY THE deepseek SEAT ON PASS 2, AND IT IS A FLOOR CELL. ***  Its
#  finding: my own Q1 enumeration was incomplete -- I listed the two type-1 READ cells as unrowed and
#  missed that (type-0, WRITE) was unrowed too.
#
#  It is inside the clause-(d) closure rather than outside it, which is what makes it a floor cell
#  and not coverage debt.  The guard's dominating predicates are `type1' and `bus == 0'; the guarded
#  body TESTS `writeflag' in its own code, twice.  So the body-tested cross-product is
#  {type-0, type-1} x {bus 0, bus != 0} x {read, write}, and (type-0, write) is one of its cells.
#
#  THE ESCAPE IT CLOSES, enumerated rather than asserted: a refusal conditioned additionally on the
#  type-0 write path --
#
#      if ((type1 && bus == 0) || (!type1 && writeflag == MEM_WRITE))
#
#  leaves `t1 anchor' green (a type-1 WRITE still forwards and still prints its tuple) and leaves
#  `t0 accept' green (a type-0 READ still returns the real config data).  WITHOUT THIS ROW IT
#  SWEEPS THE TABLE.
#
#  The oracle is the empty-slot write diagnostic again, at a DIFFERENT device number, so the string
#  cannot be confused with either of the other two rows' strings.
setup2c = ["put d 0x%x, 0x%x" % (SCRATCH + 0, k0(T0_EMPTY))]
prog2c = load_const(T0, SCRATCH) + [
    LDQ(T1, 0, T0),       # t1 = k0(T0_EMPTY)
    STQ(T1, 0, T1)]       # [G] type-0 WRITE (ioc_conf at its reset value) -- must FORWARD
cmds2c = setup2c + ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog2c)]
cmds2c += ["pc=0x%x" % k0(CODE), "step %d" % len(prog2c)]
txt2c, alive2c = session(cmds2c)

T0W = "bus 0 func 0 device 5 ]"
row("t0 write", ("yes" if T0W in txt2c else "no") if alive2c else "died", "yes",
    "the type-0 WRITE cell: a write must still reach bus_pci and name its slot")

for _l in txt2c.split(chr(10)):
    if "non-existant" in _l:
        print("  EVIDENCE(S2c): %s" % _l.strip())

# ---- SESSION 3: the ACCEPT side -- type-0 service of a REGISTERED device is unchanged -----------
#  ioc_conf is left at its reset value, so this is the `!type1' arm.  A read, not a write: reading a
#  PRESENT device is silent and returns real config data, so this row additionally carries the
#  small-nonzero discipline -- a wrong field yields 0 or all-ones, both of which this rejects.
setup3 = ["put d 0x%x, 0x%x" % (SCRATCH + 0, k0(T0_DEV7))]
prog3 = load_const(T0, SCRATCH) + [LDQ(T1, 0, T0), LDQ(T2, 0, T1)]
cmds3 = setup3 + ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog3)]
cmds3 += ["pc=0x%x" % k0(CODE), "step %d" % len(prog3), "print t2"]
txt3, alive3 = session(cmds3)
t0val = printed(txt3, "t2")

row("t0 alive", "alive" if alive3 else "dead", "alive",
    "ACCEPT: the type-0 path must still reach a registered device")

row("t0 real", "real" if t0val not in ("absent", "0x0", "0xffffffffffffffff") else t0val, "real",
    "ACCEPT: dev 7 is the i82378zb -- neither empty-slot nor unmapped")

row("t0 accept", t0val, T0_PIN,
    "ACCEPT: the exact value type-0 service returned before the fix")

ok = sum(1 for _, o in rows if o)
print("")
print("LCACONFBUS_T1ANCHOR=%s" % ("yes" if FWD in txt2 else "no"))
print("LCACONFBUS_DEV7RD=%s" % d7)
print("LCACONFBUS_T0WRITE=%s" % ("yes" if T0W in txt2c else "no"))
print("LCACONFBUS_T1READ=%s" % t1rd)
print("LCACONFBUS_T0VAL=%s" % t0val)
print("LCACONFBUS_RESULT=%d/%d" % (ok, len(rows)))
print("LCACONFBUS_WITNESS=%s" % ("PASS" if ok == len(rows) else "FAIL"))
print("LCACONFBUS_DONE")
