#!/usr/bin/env python3
"""vme_default_probe.py -- rung-3 DETECTOR for dev_vme.c's `default:' arm (vmedefaultkill, #568).

REVISION 2 (2026-10-20), against the FINAL fix `vme/fix/dev_vme.fix568.c' (md5 4e3e7fc2...) and the pass-1
adjudication's consolidated detector (ADJUDICATION_p1.md) with the coordinator's two refinements.  Revision 1
(vme_default_probe.v1.py, 21 rows) was drafted against the section-5 SKETCH.  Its rows are kept here with three
changes: `p2 announce' / `p2 once' / `p2 wr announce' are REPLACED by the two two-pass announce sessions; `p2 width'
is renamed `p2 ld widths'; and `cased census' reads each cased offset once (T1COUNT's +100 moved to `t1count inc').

DEFECT (HEAD 1a59a47e = 5dbc000e's src tree; dev_vme.c byte-identical to the 0.7.0 import).  DEVICE_ACCESS(vme)
names TEN offsets (0x00, GCSRCTL 0x2c, TCR 0x4c, T1CMP 0x50, T1COUNT 0x54, TCTL 0x60, IRQEN 0x6c, IRQL3 0x80,
IRQL4 0x84, VBR 0x88); every other offset reaches `default:', which prints with debug() and calls exit(1).

THE FIX (#568):
  population 2 -- the 26 header-named register WORD STARTS with no case (the header's 36 contiguous words
      0x00..0x8c minus the ten): exact labels, DECLINE + ANNOUNCE ONCE.  A read is served d->reg[w] (0: nothing
      writes those words); a write is dropped; one latched fatal() per register per instance, the first access's
      direction deciding the wording:
        [ vme: unimplemented read from register 0x%x (len %d) -- served 0x%x.  (once) ]
        [ vme: unimplemented write to register 0x%x (len %d): 0x%llx -- declined.  (once) ]
  population 1 -- every offset that is not one of the 36 exact labels (the 988 unnamed word starts 0x90..0xffc
      and every sub-word start): FAULT.  `default:' keeps its two debug() lines and returns 0; memory_rw.c raises
      the m88k data-access exception (vector 3; VBR 0 at reset -> PC 0x18) with DMT0/DMD0/DMA0 recorded.

RUNG 3: real MC88100 instructions through real address decode and real memory_rw on the UNMODIFIED in-tree
`-E mvme88k -e mvme187' (machine_mvme88k.c attaches "vme addr=0x%x", VME2_BASE = 0xfff40000).  STEPPED sessions
feed the debugger on stdin (mk48_nvram_probe.py's shape); FREE-RUNNING sessions drive it through a pty one command
at a time and send nothing while the guest runs -- the debugger reads MAIN_CONSOLE, which is also the guest
console's input (pcc2_width_probe.py's shape).  Only a free-running session can tell fatal() from debug():
stepping makes both print; `free neg ctl' proves each run really was free.

MECHANICS (src/cpus/cpu_m88k.c, cpu_m88k_instr_loadstore.c):
  * a data-access exception sets PSR.SFRZ and a second one while it is set becomes ERROR, so every STEPPED fault
    row has a session of its own; the FREE-RUNNING fault rows install `addu r1,r1,1 ; rte' at the vector (rte
    restores PSR from EPSR and resumes at SNIP = fault + 4) and COUNT the faults;
  * a faulting load writes no register -- destinations are seeded with a sentinel that must survive;
  * every other session puts `br' to itself at the vector (a zero word there is `goto bad': "UNIMPLEMENTED
    instruction at 0x18", "All machines stopped" -- explore2_FIX.out (a)), and free-running ones put a
    breakpoint on it, so a fault stops the run instead of hanging it;
  * DMA0 is the WORD address (`dma[0] = addr & ~3'); DMT0 = VALID | DAS 0x4000 | byte enables << 2, plus
    DREG << 7 on a load or WRITE 0x2 on a store.  The eight DMT0 wants were PREDICTED from that code before the
    first run (dmt0_predictions.txt) and that run (trial2_FIX568.out) MEASURED all eight as predicted -- the
    seat's 0x4000 | (dreg << 7) | 0x3d for a word load (0x423d r4, 0x433d r6), 0x403f for a word store, 0x4211
    for a byte at addr & 3 == 1, 0x420d for a halfword at addr & 2 == 2.

ENCODINGS are hand-assembled (decoder op26: ld.hu 0x02, ld.bu 0x03, ld.d 0x04, ld 0x05, st.d 0x08, st 0x09,
st.h 0x0a, st.b 0x0b, or 0x16, addu 0x18, br 0x30 with d26 = 0, rte 0xf400fc00).  EVERY placed word is re-read
with `unassemble' and compared word / mnemonic / operands against an independent expectation (row `unasm',
count pinned by a LITERAL).  Every session that touches the device opens with `ld r30,r3,0x88' and its rows
report `nodev ... (FAILED FOR SOME OTHER REASON)' unless r30 is DEVINIT's VBR seed 0x67000000: a wrong
base-register field would read RAM zeros, which the zero-expecting rows would otherwise accept.

ROWS, each with the mutant it is DESIGNED to catch and the channel that differs under it.
*** NO KILL TABLE EXISTS FOR THIS REVISION.  Every mutant outcome below is PREDICTED by reading fix568; only
HEAD, fix568 and the null medium were measured (run2_HEAD.out / run2_FIX568.out / run2_NULL.out). ***
  apparatus (CONTROL)
    neg apparatus  a bogus subtype: the liveness oracle MUST go red (it is failable)
    session / live the control session runs to `quit'; an or-immediate reads back
    vbr reset      DEVICE SIGNATURE: DEVINIT's VBR seed (RAM or a device-less build answers 0)
    t1cmp rt       cased T1CMP stores and reads back (and is the null medium's second discriminator)
    cased census   one ld at each of the ten cased offsets, ONE session, sentinel-seeded, PC + liveness after:
                   a cased label dropped FAULTs that offset and every later load keeps its sentinel
    free ctl       FREE-RUNNING T1CMP round trip to a breakpoint
    free quiet     ...that run prints NO vme text at all (a cased access never announces)
    free neg ctl   GCSRCTL's debug() line: PRESENT in the stepped cased census, ABSENT in the free run -- the
                   run was free at verbose 0, so the fatal-vs-debug channel of the announce rows can vary
    unasm          every placed word re-read by the disassembler
  cased accept side -- the write paths the de-escalation clause owes (not CONTROL: they detect mutants)
    tctl rt        TCTL stores a word and reads it back
    vbr rt         VBR stores a word and reads it back, then is restored to the seed and read back again
    t1count inc    T1COUNT stores a word; two reads give it and it + 100 (the read arm's `+= 100')
    cased wr       a word store to each of the six NON-storing cased arms (0x00, GCSRCTL, TCR, IRQEN, IRQL3,
                   IRQL4): no fault, PC + liveness after
  population 2 (decline)
    p2 rd census   26 ld: all 0, no fault, PC + liveness after; a label dropped FAULTs (HEAD: the host dies)
    p2 wr census   26 st of 0xa5a5a5a5, a liveness or (checked: a FAULTING store stops it), then the 26 ld:
                   all 0.  A decline that STORES reads back non-zero -- visible because fix568 does NOT force
                   odata = 0; a decline conditioned on direction FAULTs
    p2 ld widths   ld.bu + ld.hu at 0x28, ld.d at 0x08 (BOTH r6 and r7): 0, no fault -- a decline conditioned
                   on len FAULTs one of them
    p2 st widths   st.b + st.h at 0x28, st.d at 0x08, a liveness or, then read 0x28, 0x08, 0x0c back: all 0
  announce (FREE-RUNNING; full tail literals; every offset exactly once)
    p2 ann rd      each of the 26 READ then immediately WRITTEN: exactly 26 read-form lines, 0 write-form
    p2 ann rd 2    the same pairs again in the same session: 0 lines, PC at the breakpoint, liveness proof
    p2 ann wr      each WRITTEN then immediately READ: exactly 26 write-form lines `(len 4): 0xa5a5a5a5'
    p2 ann wr 2    the same pairs again: 0 lines, PC at the breakpoint, liveness proof
                   -- together 26 labels x {read, write} x {latch clear, set}: read- or write-branch
                   fatal -> debug (0 lines), a shared latch (1), a never-set latch (52), a per-direction latch
                   (52), a latch cleared by a write (pass 2 re-announces), a latch set at one constant bit
                   (51), a dropped `(once)' or changed tail (no exact match)
    p2 nw rd       FIRST access to three untouched registers by ld.bu / ld.hu / ld.d: `(len 1)', `(len 2)',
                   `(len 8) -- served 0x0.' -- an announce that fires only for 4-byte accesses gives 0
    p2 nw wr       FIRST access by st.b / st.h / st.d: `(len 1): 0xd4', `(len 2): 0xc3d4',
                   `(len 8): 0x1122334455667788' -- a 32-bit truncation of the 64-bit value fails the match
  population 1 (fault)
    p1 fault lo / hi / mid   ld at 0x90 / 0xffc / 0x94: PC 0x18, DMA0, DMT0 (word load into r4), host alive;
                   `return 0' -> `break' serves the read (PC advances); exit(1) reinstated kills the host
    p1 fault wr    st at 0x90: PC 0x18, DMA0, DMT0 (the word-store form)
    p1 p2 edge     ld 0x8c declines (0), then ld 0x90 faults: the label set's last member dropped faults at
                   0x8c instead; a label added AT 0x90 declines it
    p1 census      FREE-RUNNING: all 988 population-1 word starts, faults counted: a label added at ANY of them
                   gives 987; `return 0' -> `break' gives 0
    p1 widths      FREE-RUNNING: ld.bu 0x93, ld.hu 0x96, ld.d 0x98, st.b 0x9d, st.h 0xa2, st.d 0xa8 -- six
                   faults: a FAULT narrowed to word accesses (or to one direction) declines some of them
  interims -- NAMED channels of `vmewidthlanes': that round reds these and re-derives them
    p3 interim     ld.bu 0x51 (inside cased T1CMP): fault, DMA0 0xfff40050 -- also `if (len != 4) break;' in
                   `default:' (Fable) declines it
    p2 int byte    ld.bu 0x29 (inside population-2 MASTERCTL): fault, DMA0 0xfff40028
    p2 int half    ld.hu 0x2a (inside MASTERCTL): fault, DMA0 0xfff40028

CONTRACT (clause e).  DESIGNED to catch: the mutants named above, by the channels named above -- a design claim
until a kill table measures it.  NOT CLAIMED, so a later escape is outside the contract rather than an argument:
  * populations 3 and 4 and population-2 sub-word starts beyond the three interim pins (one byte at 0x51, one
    byte at 0x29, one halfword at 0x2a);
  * ld.d / st.d at the cased bases 0x00, 0x60 and 0x88, whose second word is a population-2 register (0x04,
    0x64, 0x8c): the device sees ONE access to the cased label;
  * cased-word ld.d / st.d lane placement (population 4: a 32-bit register served into, or stored from, the
    wrong half of an 8-byte access);
  * NO_EXCEPTIONS callers -- the debugger's put/dump/unassemble never reach the handler (silent zero fill);
  * instruction fetch from the window (a population-1 fetch takes vector 2 and halts; a population-2 fetch
    declines);
  * xmem (declines twice at population 2 -- the store silently; its load faults at population 1);
  * per-instance latch isolation: mvme187 attaches ONE vme device per process;
  * the guest's abort-handler consequence (IRQSTAT served 0: OpenBSD's vme2abort() returns "irq not set");
  * population-1 accesses other than the 988 word loads, the four stepped faults and the six width faults;
  * a served value other than 0 in the read announce (no population-2 word is ever non-zero);
  * anything about the real VMEchip2 (its register chapter is not on disk).

TEST-FIRST SHAPE: on the committed HEAD every session touching population 1 or 2 ends the host (exit 1); the
controls and the cased accept rows stay green.

Sentinel: VME_DEFAULT_PROBE_DONE (plus VME_DEFAULT_RESULT=n/N, VME_DEFAULT_CONTROL=OK|FAIL)
"""

import os
import pty
import re
import select
import shutil
import subprocess
import sys
import tempfile
import time

if len(sys.argv) < 2:
    sys.stderr.write("usage: vme_default_probe.py <gxemul> [label]\n")
    sys.exit(2)

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
#  A private dummy file: a shared /tmp path once let two concurrent runs race on it.
_TMPDIR = tempfile.mkdtemp(prefix="vme_default_")
DUMMY = os.path.join(_TMPDIR, "dummy.bin")
with open(DUMMY, "wb") as _f:
    _f.write(b"\x00\x00\x00\x00")

VME = 0xfff40000            # VME2_BASE (mvme88k_vme.h)
CODE = 0x00010000
CODE2 = 0x00010200          # the second pass of a two-pass free-running session
CENSUS = 0x00020000         # the population-1 census program
VEC_DACC = 0x18             # VBR 0 + 8 * M88K_EXCEPTION_DATA_ACCESS (3)
VEC_MISAL = 0x20            # VBR 0 + 8 * M88K_EXCEPTION_MISALIGNED_ACCESS (4)
SENT = 0xdeadbeef
WVAL = 0xa5a5a5a5
T1VAL = 0x12345678
TCTLVAL = 0x13572468
VBRVAL = 0x89abcdef
T1CVAL = 0x00001000
NARROW = 0xa1b2c3d4         # st.b / st.h source: distinct bytes, so a lane mix-up is visible
DHI, DLO = 0x11223344, 0x55667788   # st.d source pair: HIGH word != low word, so a 32-bit truncation shows
VBR_SEED = 0x67000000       # DEVINIT: VME2_SET_VBR0(6) + VME2_SET_VBR1(7) = 6 << 28 | 7 << 24
LIVE = 0x1234
LIVE2 = 0x5678              # the second-pass liveness proof
STLIVE = 0x5a5a             # the after-the-stores liveness proof
T1COUNT_STEP = 100          # the T1COUNT read arm's `+= 100' (after the preload has served)

CASED = (0x00, 0x2c, 0x4c, 0x50, 0x54, 0x60, 0x6c, 0x80, 0x84, 0x88)
POP2 = ((0x04, "SADDR2"), (0x08, "SLAVELMOD1"), (0x0c, "SLAVELMOD2"), (0x10, "SLAVECTL"),
        (0x14, "MASTER1"), (0x18, "MASTER2"), (0x1c, "MASTER3"), (0x20, "MASTER4"),
        (0x24, "MASTER4MOD"), (0x28, "MASTERCTL"), (0x30, "DMACTL"), (0x34, "DMAMODE"),
        (0x38, "DMALADDR"), (0x3c, "DMAVMEADDR"), (0x40, "DMACOUNT"), (0x44, "DMATABLE"),
        (0x48, "DMASTAT"), (0x58, "T2CMP"), (0x5c, "T2COUNT"), (0x64, "PRESCALE"),
        (0x68, "IRQSTAT"), (0x70, "SETSOFTIRQ"), (0x74, "IRQCLR"), (0x78, "IRQL1"),
        (0x7c, "IRQL2"), (0x8c, "MISC"))
POP2_OFFS = tuple(o for o, _ in POP2)
POP1 = tuple(range(0x90, 0x1000, 4))
#  The header's register block is 36 CONTIGUOUS words, 0x00..0x8c: cased + population 2 must tile it exactly.
assert len(CASED) == 10 and len(POP2) == 26 and len(POP1) == 988
assert sorted(CASED + POP2_OFFS) == list(range(0, 0x90, 4))

#  DMT0 PREDICTIONS (written before the first run, from cpu_m88k_instr_loadstore.c: VALID 0x1, DAS 0x4000,
#  byte enables << 2 -- word 0xf, byte 1 << (3 - (addr & 3)), half 3 << (2 - (addr & 2)) -- and DREG << 7 on a
#  load or WRITE 0x2 on a store).  The rows pin what the measurement says.
def dmt_load(dreg, en):
    return 0x1 | 0x4000 | (dreg << 7) | (en << 2)


DMT_ST_WORD = 0x1 | 0x2 | 0x4000 | (0xf << 2)          # 0x403f
DMT_LD_WORD_R4 = dmt_load(4, 0xf)                      # 0x423d
DMT_LD_WORD_R6 = dmt_load(6, 0xf)                      # 0x433d
DMT_LD_BYTE1_R4 = dmt_load(4, 1 << (3 - 1))            # 0x4211  (a byte at addr & 3 == 1)
DMT_LD_HALF2_R4 = dmt_load(4, 3 << (2 - 2))            # 0x420d  (a halfword at addr & 2 == 2)

PROMPT = "GXemul> "
RD_LINE = "[ vme: unimplemented read from register 0x%x (len %d) -- served 0x%x.  (once) ]"
WR_LINE = "[ vme: unimplemented write to register 0x%x (len %d): 0x%x -- declined.  (once) ]"
GCS_LINE = "[ vme: unimplemented GCSRCTL ]"
VMETXT = "[ vme:"


# ------------------------------------------------------------------- encodings
class Ins(object):
    __slots__ = ("word", "mnem", "ops")

    def __init__(self, word, mnem, ops):
        self.word, self.mnem, self.ops = word, mnem, ops


def enc(op26, rd, rs1, imm):
    assert 0 <= op26 < 64 and 0 <= rd < 32 and 0 <= rs1 < 32 and 0 <= imm <= 0xffff
    return (op26 << 26) | (rd << 21) | (rs1 << 16) | imm


def _mem(op26, mnem, rd, off, rs1=3):
    return Ins(enc(op26, rd, rs1, off), mnem, "r%d,r%d,0x%x" % (rd, rs1, off))


def LD(rd, off):
    return _mem(0x05, "ld", rd, off)


def LD_BU(rd, off):
    return _mem(0x03, "ld.bu", rd, off)


def LD_HU(rd, off):
    return _mem(0x02, "ld.hu", rd, off)


def LD_D(rd, off):
    assert rd != 31 and off % 8 == 0
    return _mem(0x04, "ld.d", rd, off)


def ST(rs, off):
    return _mem(0x09, "st", rs, off)


def ST_B(rs, off):
    return _mem(0x0b, "st.b", rs, off)


def ST_H(rs, off):
    assert off % 2 == 0
    return _mem(0x0a, "st.h", rs, off)


def ST_D(rs, off):
    assert rs != 31 and off % 8 == 0
    return _mem(0x08, "st.d", rs, off)


def OR_I(rd, rs1, imm):
    assert rd != 0
    return Ins(enc(0x16, rd, rs1, imm), "or", "r%d,r%d,0x%x" % (rd, rs1, imm))


def ADDU_I(rd, rs1, imm):
    #  the disassembler prints this immediate in DECIMAL (cpu_m88k.c: "%s\tr%i,r%i,%i")
    return Ins(enc(0x18, rd, rs1, imm), "addu", "r%d,r%d,%d" % (rd, rs1, imm))


def RTE():
    return Ins(0xf400fc00, "rte", "")


def BR_SELF():
    #  op26 0x30, d26 = 0: the target is the branch itself; the operand is filled in on placement
    return Ins(0xc0000000, "br", None)


def VSIG():
    return LD(30, 0x88)          # every device session's opening VBR read


GUARD = (VEC_DACC, [BR_SELF()])
HANDLER = (VEC_DACC, [ADDU_I(1, 1, 1), RTE()])


# ------------------------------------------------------------------- sessions
def hx(v):
    return "absent" if v is None else "0x%x" % v


def argv_for(subtype):
    return [BIN, "-V", "-x", "-E", "mvme88k", "-e", subtype, "-M", "64",
            "0x%x:%s" % (CODE, DUMMY)]


def seeds(pairs):
    return ["r%d=0x%x" % (r, v) for r, v in pairs]


def place(blocks):
    """blocks: [(addr, [Ins])] -> (debugger commands, [(addr, Ins)]).  Every block is re-read with
       `unassemble' (end-exclusive) right after it is written."""
    cmds, placed = [], []
    for at, insns in blocks:
        for i, ins in enumerate(insns):
            a = at + 4 * i
            if ins.ops is None:
                ins = Ins(ins.word, ins.mnem, "0x%08x" % a)
            cmds.append("put w 0x%x, 0x%08x" % (a, ins.word))
            placed.append((a, ins))
        cmds.append("unassemble 0x%x 0x%x" % (at, at + 4 * len(insns)))
    return cmds, placed


def run_piped(cmds, subtype="mvme187", timeout=90):
    inp = ("\n".join(list(cmds) + ["quit"]) + "\n").encode("latin-1")
    try:
        p = subprocess.run(argv_for(subtype), input=inp, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        return (e.output or b"").decode("latin-1", "replace").replace("\r", ""), "TIMEOUT"
    rc = p.returncode
    return (p.stdout.decode("latin-1", "replace").replace("\r", ""),
            ("sig%d" % -rc) if rc < 0 else ("exit%d" % rc))


def run_pty(cmds, t_cmd=10.0, t_run=30.0):
    """One command at a time through a pty.  An ordinary command waits for the next prompt; `continue' waits
       for BREAKPOINT and then a prompt after it, and nothing is sent while the guest runs.  -> (transcript,
       how); how is exitN / sigN, or no-prompt / no-breakpoint (the child is then killed: a guest still running
       would never read `quit')."""
    pid, fd = pty.fork()
    if pid == 0:
        try:
            os.execv(BIN, argv_for("mvme187"))
        finally:
            os._exit(127)
    buf = [""]

    def pump(deadline, pred):
        while True:
            if pred():
                return "ok"
            left = deadline - time.time()
            if left <= 0:
                return "timeout"
            r, _, _ = select.select([fd], [], [], min(left, 0.05))
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
            except OSError:
                return "eof"
            if not d:
                return "eof"
            buf[0] += d.decode("latin-1", "replace")

    state = pump(time.time() + 20.0, lambda: PROMPT in buf[0])
    failed = None if state == "ok" else ("no-prompt" if state == "timeout" else None)
    if state == "ok":
        for c in cmds:
            start = len(buf[0])
            try:
                os.write(fd, (c + "\n").encode("latin-1"))
            except OSError:
                state = "eof"
                break
            if c == "continue":
                def pred(start=start):
                    b = buf[0].find("BREAKPOINT", start)
                    return b >= 0 and buf[0].find(PROMPT, b) >= 0
                state = pump(time.time() + t_run, pred)
                if state == "timeout":
                    failed = "no-breakpoint"
            else:
                state = pump(time.time() + t_cmd,
                             lambda start=start: buf[0].find(PROMPT, start) >= 0)
                if state == "timeout":
                    failed = "no-prompt"
            if state != "ok":
                break
    if state == "ok":
        try:
            os.write(fd, b"quit\n")
        except OSError:
            pass
        pump(time.time() + 5.0, lambda: False)
    try:
        os.close(fd)
    except OSError:
        pass
    stat, reaped = None, False
    for attempt in range(2):
        for _ in range(40):
            try:
                p, s = os.waitpid(pid, os.WNOHANG)
            except OSError:
                p, s = pid, None
            if p:
                stat, reaped = s, True
                break
            time.sleep(0.05)
        if reaped:
            break
        try:
            os.kill(pid, 9)
        except OSError:
            pass
        failed = failed or "killed"
    if failed:
        how = failed
    elif stat is None:
        how = "unreaped"
    elif os.WIFSIGNALED(stat):
        how = "sig%d" % os.WTERMSIG(stat)
    else:
        how = "exit%d" % os.WEXITSTATUS(stat)
    return buf[0].replace("\r", ""), how


DIS_RE = re.compile(r"^[su]([0-9a-f]{8}): ([0-9a-f]{8})\s+(?:<-\s+)?(\S+)(?:\t(\S+))?[ \t]*$", re.M)
GPR_RE = re.compile(r"\br(\d+)\s*=\s*(0x[0-9a-fA-F]+)")
PC_RE = re.compile(r"cpu\d+:\s+pc\s+=\s+(0x[0-9a-fA-F]+)")
CR_RE = re.compile(r"\b([A-Z][A-Z0-9]*)=(0x[0-9a-fA-F]+)")


class Res(object):
    pass


def analyse(text, how, placed):
    """Split the transcript at the prompts; parse every unassemble, every reg dump (in order), the last
       `reg 0,0', and the text of every `continue'."""
    r = Res()
    r.how, r.text, r.placed = how, text, placed
    r.dis, r.dumps, r.cr, r.conts = {}, [], None, []
    for part in text.split(PROMPT)[1:]:
        cmd, _, out = part.partition("\n")
        cmd = cmd.strip()
        if cmd.startswith("unassemble"):
            for m in DIS_RE.finditer(out):
                r.dis[int(m.group(1), 16)] = (int(m.group(2), 16), m.group(3), m.group(4) or "")
        elif cmd == "reg":
            m = PC_RE.search(out)
            if m:
                r.dumps.append(({int(g.group(1)): int(g.group(2), 16)
                                 for g in GPR_RE.finditer(out)}, int(m.group(1), 16)))
        elif cmd == "reg 0,0":
            cr = {g.group(1): int(g.group(2), 16) for g in CR_RE.finditer(out)}
            if cr:
                r.cr = cr
        elif cmd == "continue":
            r.conts.append(out)
    r.regs, r.pc = r.dumps[-1] if r.dumps else (None, None)
    return r


UNASM = {"ok": 0, "n": 0, "bad": []}


def check_unasm(r, scored=True):
    ok = n = 0
    for a, ins in r.placed:
        n += 1
        d = r.dis.get(a)
        if d is not None and d == (ins.word, ins.mnem, ins.ops):
            ok += 1
        elif scored:
            UNASM["bad"].append("0x%x:%08x %s %s -> %r" % (a, ins.word, ins.mnem, ins.ops, d))
    if scored:
        UNASM["ok"] += ok
        UNASM["n"] += n
    return ok, n


def stepped(blocks, regs, nsteps, cr=False, scored=True):
    cmds, placed = place(blocks)
    cmds = seeds([(3, VME)] + regs) + cmds + ["pc=0x%x" % CODE, "step %d" % nsteps, "reg"]
    if cr:
        cmds.append("reg 0,0")
    t, how = run_piped(cmds)
    r = analyse(t, how, placed)
    check_unasm(r, scored)
    return r


def freerun(blocks, regs, bps, runs):
    """runs: [start pc] -- each is `pc=<start>', `continue', `reg'.  All code, every unassemble and every
       breakpoint go in BEFORE the first `continue', so the disassembly cross-check never depends on surviving
       a run."""
    cmds, placed = place(blocks)
    cmds = seeds([(3, VME)] + regs) + cmds + ["breakpoint add 0x%x" % b for b in bps]
    for start in runs:
        cmds += ["pc=0x%x" % start, "continue", "reg"]
    t, how = run_pty(cmds)
    r = analyse(t, how, placed)
    check_unasm(r)
    return r


def died(r):
    return "died:%s" % r.how


def reg(r, n):
    if r.regs is None:
        return died(r) if r.how != "exit0" else "absent"
    return hx(r.regs.get(n))


def devsig_bad(r):
    """None when the session's opening VBR read saw the device; else the reason."""
    if r.regs is None:
        return died(r)
    if r.regs.get(30) != VBR_SEED:
        return "nodev r30=%s (FAILED FOR SOME OTHER REASON)" % hx(r.regs.get(30))
    return None


def end_of(prog, at=CODE):
    return at + 4 * (len(prog) - 1)


def tail(r, pc_want, live_reg=31, live_want=LIVE):
    """'' when the stepped run ended at the program's br with its liveness register set; else a suffix."""
    s = ""
    if r.pc != pc_want:
        s += " pc=%s" % hx(r.pc)
    if r.regs.get(live_reg) != live_want:
        s += " r%d=%s" % (live_reg, hx(r.regs.get(live_reg)))
    return s


def lines(seg):
    return [ln.rstrip() for ln in seg.split("\n")]


rows = []


def row(name, got, want, note=""):
    assert name not in [n for n, _ in rows], "DUPLICATE ROW NAME %r" % name
    assert len(name) <= 15, name     # `%-16s ' keeps a gate's `^$v  .*ok$' satisfiable
    ok = (got == want)
    rows.append((name, ok))
    print("%-16s %-34s %-34s %-60s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    sys.stdout.flush()
    return ok


print("vmedefaultkill RUNG-3 DETECTOR (revision 2, fix568) -- binary=%s label=%s" % (BIN, LABEL))
print("machine: -E mvme88k -e mvme187 -M 64 (UNMODIFIED); vme at 0x%08x" % VME)
t0 = time.time()

# ================================================================ INFO (unscored)
#  Measured so the panel has the number; NOT a row -- no want, no score, no pin.  (LD_D refuses a 4-mod-8
#  offset, so this one word is built by hand.)
cmds, placed = place([(VEC_MISAL, [BR_SELF()]), (CODE, [VSIG(), Ins(enc(0x04, 4, 3, 0x0c), "ld.d", "r4,r3,0xc"),
                                                        OR_I(6, 0, LIVE), BR_SELF()])])
t, how = run_piped(seeds([(3, VME), (4, SENT), (5, SENT), (6, SENT), (30, SENT)]) + cmds
                   + ["pc=0x%x" % CODE, "step 3", "reg"])
ri = analyse(t, how, placed)
print("INFO ld.d 4mod8  ld.d at 0x0c (4 mod 8): how=%s pc=%s r4=%s r5=%s r6=%s vme-text=%d unasm=%d/%d"
      % (ri.how, hx(ri.pc), reg(ri, 4), reg(ri, 5), reg(ri, 6), ri.text.count(VMETXT),
         *check_unasm(ri, scored=False)))

print("%-16s %-34s %-34s %-60s %s" % ("row", "got", "want", "note", ""))

# ================================================================ apparatus
#  APPARATUS NEGATIVE CONTROL: the liveness oracle must be able to go red.
cmds, _ = place([(CODE, [OR_I(4, 0, LIVE), BR_SELF()])])
t, how = run_piped(seeds([(4, SENT)]) + cmds + ["pc=0x%x" % CODE, "step 1", "reg"], subtype="187")
rn = analyse(t, how, [])
row("neg apparatus", "%s/%s" % (how, hx(rn.regs.get(4)) if rn.regs else "absent"), "exit1/absent",
    "bogus subtype `187' -> no machine -> `live' MUST fail")

prog = [OR_I(4, 0, LIVE), LD(5, 0x88), ST(2, 0x50), LD(6, 0x50), BR_SELF()]
r = stepped([GUARD, (CODE, prog)], [(2, T1VAL), (4, SENT), (5, SENT), (6, SENT)], 4)
row("session", r.how, "exit0", "the control session ran to `quit'")
row("live", reg(r, 4), hx(LIVE), "or r4,r0,0x1234 -- the guest executes, readback works")
row("vbr reset", reg(r, 5), hx(VBR_SEED), "DEVICE SIGNATURE: DEVINIT's VBR seed; RAM or no device reads 0")
row("t1cmp rt", reg(r, 6), hx(T1VAL), "a word stored to CASED T1CMP reads back")

#  CASED CENSUS: one load per cased offset, ONE session, sentinel-seeded, then liveness.  Stepped, so the GCSRCTL
#  load's debug() line PRINTS here -- the positive half of `free neg ctl'.
CC = [(4, 0x00), (5, 0x2c), (6, 0x4c), (7, 0x50), (8, 0x54), (9, 0x60), (10, 0x6c), (11, 0x80), (12, 0x84),
      (13, 0x88)]
CC_WANT = {4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: VBR_SEED, 15: LIVE}
prog = [LD(rr, o) for rr, o in CC] + [OR_I(15, 0, LIVE), BR_SELF()]
r = stepped([GUARD, (CODE, prog)], [(rr, SENT) for rr in CC_WANT], len(prog) - 1)
gcs_stepped = lines(r.text).count(GCS_LINE)
if r.regs is None:
    got = died(r)
else:
    got = "%d/%d" % (sum(1 for rr, v in CC_WANT.items() if r.regs.get(rr) == v), len(CC_WANT))
    if r.pc != end_of(prog):
        got += " pc=%s" % hx(r.pc)
row("cased census", got, "11/11", "ten cased offsets read (VBR 0x67000000, the rest 0) + liveness")

#  FREE-RUNNING SHAPE CONTROL: T1CMP round trip and a GCSRCTL read, to a breakpoint.
prog = [VSIG(), ST(2, 0x50), LD(5, 0x50), LD(8, 0x2c), OR_I(7, 0, LIVE), BR_SELF()]
bp = end_of(prog)
r = freerun([GUARD, (CODE, prog)], [(2, T1VAL), (5, SENT), (7, SENT), (8, SENT), (30, SENT)],
            [bp, VEC_DACC], [CODE])
if r.regs is None or not r.conts:
    got_c = got_q = got_n = died(r)
elif r.pc != bp:
    got_c = got_q = got_n = "stopped pc=%s (FAILED FOR SOME OTHER REASON)" % hx(r.pc)
else:
    got_c = "%s/%s/%s" % (hx(r.regs.get(5)), hx(r.regs.get(30)), hx(r.regs.get(7)))
    got_q = r.conts[0].count(VMETXT)
    got_n = "%d/%d" % (gcs_stepped, lines(r.conts[0]).count(GCS_LINE))
row("free ctl", got_c, "%s/%s/%s" % (hx(T1VAL), hx(VBR_SEED), hx(LIVE)),
    "FREE-RUNNING to a breakpoint: T1CMP round trip, VBR, liveness")
row("free quiet", got_q, 0, "...and that run prints NO vme text at all")
row("free neg ctl", got_n, "1/0", "GCSRCTL's debug() line: 1 stepped (cased census), 0 free-running")

# ================================================================ cased accept side (write paths)
prog = [VSIG(), ST(2, 0x60), LD(4, 0x60), ST(7, 0x88), LD(5, 0x88), ST(11, 0x88), LD(12, 0x88),
        ST(8, 0x54), LD(9, 0x54), LD(10, 0x54), OR_I(31, 0, LIVE), BR_SELF()]
r = stepped([GUARD, (CODE, prog)],
            [(2, TCTLVAL), (7, VBRVAL), (8, T1CVAL), (11, VBR_SEED), (4, SENT), (5, SENT), (9, SENT),
             (10, SENT), (12, SENT), (30, SENT), (31, SENT)], len(prog) - 1)
bad = devsig_bad(r)
if bad:
    g_t = g_v = g_c = bad
else:
    sfx = tail(r, end_of(prog))
    g_t = hx(r.regs.get(4)) + sfx
    g_v = "%s/%s" % (hx(r.regs.get(5)), hx(r.regs.get(12))) + sfx
    g_c = "%s/%s" % (hx(r.regs.get(9)), hx(r.regs.get(10))) + sfx
row("tctl rt", g_t, hx(TCTLVAL), "TCTL stores a word and reads it back")
row("vbr rt", g_v, "%s/%s" % (hx(VBRVAL), hx(VBR_SEED)), "VBR stores, reads back; restored to the seed, reads back")
row("t1count inc", g_c, "%s/%s" % (hx(T1CVAL), hx(T1CVAL + T1COUNT_STEP)),
    "T1COUNT stores; two reads give it, then it + 100")

prog = [VSIG()] + [ST(2, o) for o in (0x00, 0x2c, 0x4c, 0x6c, 0x80, 0x84)] + [OR_I(31, 0, LIVE), BR_SELF()]
r = stepped([GUARD, (CODE, prog)], [(2, WVAL), (30, SENT), (31, SENT)], len(prog) - 1)
bad = devsig_bad(r)
row("cased wr", bad if bad else "%s/%s" % (hx(r.pc), hx(r.regs.get(31))),
    "%s/%s" % (hx(end_of(prog)), hx(LIVE)), "a word store to 0x00/GCSRCTL/TCR/IRQEN/IRQL3/IRQL4: no fault")

# ================================================================ population 2 (decline)
REGS26 = list(range(4, 30))
prog = [VSIG()] + [LD(rr, o) for rr, o in zip(REGS26, POP2_OFFS)] + [OR_I(31, 0, LIVE), BR_SELF()]
r = stepped([GUARD, (CODE, prog)], [(30, SENT), (31, SENT)] + [(rr, SENT) for rr in REGS26], len(prog) - 1)
bad = devsig_bad(r)
row("p2 rd census", bad if bad else "%d/26" % sum(1 for rr in REGS26 if r.regs.get(rr) == 0) + tail(r, end_of(prog)),
    "26/26", "26 ld, one per population-2 register: all 0, no fault, runs on")

prog = ([VSIG()] + [ST(2, o) for o in POP2_OFFS] + [OR_I(1, 0, STLIVE)]
        + [LD(rr, o) for rr, o in zip(REGS26, POP2_OFFS)] + [OR_I(31, 0, LIVE), BR_SELF()])
r = stepped([GUARD, (CODE, prog)], [(2, WVAL), (1, SENT), (30, SENT), (31, SENT)] + [(rr, SENT) for rr in REGS26],
            len(prog) - 1)
bad = devsig_bad(r)
if bad:
    got = bad
else:
    got = "%d/26" % sum(1 for rr in REGS26 if r.regs.get(rr) == 0) + tail(r, end_of(prog))
    if r.regs.get(1) != STLIVE:
        got += " after-st r1=%s" % hx(r.regs.get(1))
row("p2 wr census", got, "26/26", "26 st 0xa5a5a5a5, liveness AFTER the stores, 26 ld: all 0")

prog = [VSIG(), LD_BU(4, 0x28), LD_HU(5, 0x28), LD_D(6, 0x08), OR_I(31, 0, LIVE), BR_SELF()]
r = stepped([GUARD, (CODE, prog)], [(4, SENT), (5, SENT), (6, SENT), (7, SENT), (30, SENT), (31, SENT)],
            len(prog) - 1)
bad = devsig_bad(r)
row("p2 ld widths", bad if bad else "%d/4" % sum(1 for rr in (4, 5, 6, 7) if r.regs.get(rr) == 0)
    + tail(r, end_of(prog)), "4/4", "ld.bu + ld.hu at 0x28, ld.d at 0x08 (r6 AND r7): 0, no fault")

prog = [VSIG(), ST_B(12, 0x28), ST_H(12, 0x28), ST_D(10, 0x08), OR_I(1, 0, STLIVE),
        LD(4, 0x28), LD(5, 0x08), LD(6, 0x0c), OR_I(31, 0, LIVE), BR_SELF()]
r = stepped([GUARD, (CODE, prog)], [(12, NARROW), (10, DHI), (11, DLO), (1, SENT), (4, SENT), (5, SENT),
                                    (6, SENT), (30, SENT), (31, SENT)], len(prog) - 1)
bad = devsig_bad(r)
if bad:
    got = bad
else:
    got = "%d/3" % sum(1 for rr in (4, 5, 6) if r.regs.get(rr) == 0) + tail(r, end_of(prog))
    if r.regs.get(1) != STLIVE:
        got += " after-st r1=%s" % hx(r.regs.get(1))
row("p2 st widths", got, "3/3", "st.b + st.h at 0x28, st.d at 0x08: no fault; 0x28/0x08/0x0c read back 0")


# ================================================================ announce (free-running)
def announce_pair(rows_names, first, second, want_line, want_form):
    """Two passes in ONE free-running session.  Pass 1 and pass 2 each access every population-2 register twice
       in a row, `first' then `second'.  Pass 1 must print exactly the 26 `want_line' lines (one per offset, full
       literal) and no other vme text; pass 2 must print nothing, end at its breakpoint, and set its liveness."""
    def pairs():
        out = []
        for o in POP2_OFFS:
            out += [first(o), second(o)]
        return out
    pass1 = [VSIG()] + pairs() + [BR_SELF()]
    pass2 = pairs() + [OR_I(31, 0, LIVE2), BR_SELF()]
    bp1, bp2 = end_of(pass1), end_of(pass2, CODE2)
    r = freerun([GUARD, (CODE, pass1), (CODE2, pass2)], [(2, WVAL), (4, SENT), (30, SENT), (31, SENT)],
                [bp1, bp2, VEC_DACC], [CODE, CODE2])
    pcs = [pc for _, pc in r.dumps]
    n1, n2 = rows_names
    note1 = "pass 1: vme lines / exact %s lines / offsets exactly once" % want_form
    note2 = "pass 2, same pairs again: no vme text; breakpoint + r31=0x5678"
    if not pcs or not r.conts:
        row(n1, died(r), "26/26/26", note1)
        row(n2, "pass 1 not completed (FAILED FOR SOME OTHER REASON)", 0, note2)
        return
    bad = None
    if r.dumps[0][0].get(30) != VBR_SEED:
        bad = "nodev r30=%s (FAILED FOR SOME OTHER REASON)" % hx(r.dumps[0][0].get(30))
    l1 = lines(r.conts[0])
    exact = [o for o in POP2_OFFS if l1.count(want_line(o)) == 1]
    nvme = r.conts[0].count(VMETXT)
    g1 = bad if bad else "%d/%d/%d" % (nvme, sum(l1.count(want_line(o)) for o in POP2_OFFS), len(exact))
    if pcs[0] != bp1 and not bad:
        g1 += " stopped pc=%s" % hx(pcs[0])
    row(n1, g1, "26/26/26", note1)
    if bad or pcs[0] != bp1:
        g2 = "pass 1 not completed (FAILED FOR SOME OTHER REASON)"
    elif nvme == 0:
        g2 = "pass 1 silent (FAILED FOR SOME OTHER REASON)"
    elif len(pcs) < 2 or len(r.conts) < 2:
        g2 = "pass 2 %s" % died(r)
    elif pcs[1] != bp2 or r.dumps[1][0].get(31) != LIVE2:
        g2 = "%d stopped pc=%s r31=%s" % (r.conts[1].count(VMETXT), hx(pcs[1]), hx(r.dumps[1][0].get(31)))
    else:
        g2 = r.conts[1].count(VMETXT)
    row(n2, g2, 0, note2)


announce_pair(("p2 ann rd", "p2 ann rd 2"), lambda o: LD(4, o), lambda o: ST(2, o),
              lambda o: RD_LINE % (o, 4, 0), "read-form")
announce_pair(("p2 ann wr", "p2 ann wr 2"), lambda o: ST(2, o), lambda o: LD(4, o),
              lambda o: WR_LINE % (o, 4, WVAL), "write-form")

#  NON-WORD FIRST ACCESSES, free-running: each of six untouched registers is reached first at its own width.
NW_RD = [(LD_BU(4, 0x04), RD_LINE % (0x04, 1, 0)), (LD_HU(5, 0x0c), RD_LINE % (0x0c, 2, 0)),
         (LD_D(6, 0x10), RD_LINE % (0x10, 8, 0))]
NW_WR = [(ST_B(12, 0x14), WR_LINE % (0x14, 1, NARROW & 0xff)),
         (ST_H(12, 0x1c), WR_LINE % (0x1c, 2, NARROW & 0xffff)),
         (ST_D(10, 0x20), WR_LINE % (0x20, 8, (DHI << 32) | DLO))]
prog = [VSIG()] + [i for i, _ in NW_RD + NW_WR] + [OR_I(31, 0, LIVE), BR_SELF()]
bp = end_of(prog)
r = freerun([GUARD, (CODE, prog)], [(12, NARROW), (10, DHI), (11, DLO), (4, SENT), (5, SENT), (6, SENT),
                                    (7, SENT), (30, SENT), (31, SENT)], [bp, VEC_DACC], [CODE])
bad = devsig_bad(r)
if not bad and (r.pc != bp or not r.conts):
    bad = "stopped pc=%s (FAILED FOR SOME OTHER REASON)" % hx(r.pc)
if bad:
    g_r = g_w = bad
else:
    l = lines(r.conts[0])
    nrd = sum(1 for x in l if x.startswith("[ vme: unimplemented read from register"))
    nwr = sum(1 for x in l if x.startswith("[ vme: unimplemented write to register"))
    g_r = "%d/%d" % (sum(1 for _, w in NW_RD if l.count(w) == 1), nrd)
    g_w = "%d/%d" % (sum(1 for _, w in NW_WR if l.count(w) == 1), nwr)
    if r.regs.get(31) != LIVE:
        g_r += " r31=%s" % hx(r.regs.get(31))
        g_w += " r31=%s" % hx(r.regs.get(31))
row("p2 nw rd", g_r, "3/3", "FREE: first ld.bu/ld.hu/ld.d -> (len 1)/(len 2)/(len 8) served 0x0")
row("p2 nw wr", g_w, "3/3", "FREE: first st.b/st.h/st.d -> 0xd4/0xc3d4/0x1122334455667788")


# ================================================================ population 1 (fault) + interims
def fault_row(name, access, extra_seeds, dma_want, dmt_want, note):
    """Stepped, ONE fault per session: VSIG, the access, an or, br; three steps put PC on the vector's br."""
    prog = [VSIG(), access, OR_I(5, 0, LIVE), BR_SELF()]
    r = stepped([GUARD, (CODE, prog)], [(4, SENT), (5, SENT), (30, SENT)] + extra_seeds, 3, cr=True)
    bad = devsig_bad(r)
    if bad:
        got = bad
    else:
        cr = r.cr or {}
        got = "%s/%s/%s/%s" % (r.how, hx(r.pc), hx(cr.get("DMA0")), hx(cr.get("DMT0")))
        for rr in (4, 5):        # a faulting load writes no register; the instruction after it never runs
            if r.regs.get(rr) != SENT:
                got += " r%d=%s" % (rr, hx(r.regs.get(rr)))
    row(name, got, "exit0/0x18/%s/%s" % (hx(VME + dma_want), hx(dmt_want)), note)


fault_row("p1 fault lo", LD(4, 0x90), [], 0x90, DMT_LD_WORD_R4, "ld r4 at 0x90: PC 0x18, DMA0, DMT0, host alive")
fault_row("p1 fault hi", LD(4, 0xffc), [], 0xffc, DMT_LD_WORD_R4, "ld r4 at 0xffc (the last word)")
fault_row("p1 fault mid", LD(4, 0x94), [], 0x94, DMT_LD_WORD_R4, "ld r4 at 0x94 (an interior sample)")
fault_row("p1 fault wr", ST(2, 0x90), [(2, WVAL)], 0x90, DMT_ST_WORD, "st at 0x90: the word-store DMT0")

prog = [VSIG(), LD(4, 0x8c), LD(6, 0x90), OR_I(5, 0, LIVE), BR_SELF()]
r = stepped([GUARD, (CODE, prog)], [(4, SENT), (5, SENT), (6, SENT), (30, SENT)], 4, cr=True)
bad = devsig_bad(r)
if bad:
    got = bad
else:
    cr = r.cr or {}
    got = "%s/%s/%s/%s" % (hx(r.regs.get(4)), hx(r.pc), hx(cr.get("DMA0")), hx(cr.get("DMT0")))
    for rr in (5, 6):
        if r.regs.get(rr) != SENT:
            got += " r%d=%s" % (rr, hx(r.regs.get(rr)))
row("p1 p2 edge", got, "0x0/0x18/%s/%s" % (hx(VME + 0x90), hx(DMT_LD_WORD_R6)),
    "ld 0x8c declines (0), then ld r6 at 0x90 faults")

fault_row("p3 interim", LD_BU(4, 0x51), [], 0x50, DMT_LD_BYTE1_R4,
          "ld.bu 0x51 inside cased T1CMP faults; DMA0 = the WORD address")
fault_row("p2 int byte", LD_BU(4, 0x29), [], 0x28, DMT_LD_BYTE1_R4, "ld.bu 0x29 inside population-2 MASTERCTL faults")
fault_row("p2 int half", LD_HU(4, 0x2a), [], 0x28, DMT_LD_HALF2_R4, "ld.hu 0x2a inside MASTERCTL faults")

#  POPULATION-1 CENSUS: every word start 0x90..0xffc, free-running, each fault counted by the handler.
cprog = [VSIG()] + [LD(4, o) for o in POP1] + [BR_SELF()]
cbp = end_of(cprog, CENSUS)
r = freerun([HANDLER, (CENSUS, cprog)], [(1, 0), (4, SENT), (30, SENT)], [cbp], [CENSUS])
bad = devsig_bad(r)
if bad:
    got = bad
elif r.pc != cbp:
    got = "stopped pc=%s (FAILED FOR SOME OTHER REASON)" % hx(r.pc)
else:
    got = "%d/%d" % (r.regs.get(1, -1), len(POP1))
    if r.regs.get(4) != SENT:
        got += " r4=%s" % hx(r.regs.get(4))
row("p1 census", got, "988/988", "FREE-RUNNING: all 988 population-1 word starts fault")

#  POPULATION-1 WIDTHS: six non-word accesses, free-running, faults counted; every load destination keeps its
#  sentinel and the closing or runs.
prog = [VSIG(), LD_BU(4, 0x93), LD_HU(5, 0x96), LD_D(6, 0x98), ST_B(12, 0x9d), ST_H(12, 0xa2), ST_D(10, 0xa8),
        OR_I(31, 0, LIVE), BR_SELF()]
bp = end_of(prog)
r = freerun([HANDLER, (CODE, prog)], [(1, 0), (12, NARROW), (10, DHI), (11, DLO), (4, SENT), (5, SENT), (6, SENT),
                                      (7, SENT), (30, SENT), (31, SENT)], [bp], [CODE])
bad = devsig_bad(r)
if bad:
    got = bad
elif r.pc != bp:
    got = "stopped pc=%s (FAILED FOR SOME OTHER REASON)" % hx(r.pc)
else:
    got = "%d/6" % r.regs.get(1, -1)
    for rr in (4, 5, 6, 7):
        if r.regs.get(rr) != SENT:
            got += " r%d=%s" % (rr, hx(r.regs.get(rr)))
    if r.regs.get(31) != LIVE:
        got += " r31=%s" % hx(r.regs.get(31))
row("p1 widths", got, "6/6", "FREE: ld.bu/ld.hu/ld.d/st.b/st.h/st.d at population 1: six faults")

# ================================================================ disassembly cross-check
#  LITERAL want, derived by hand per session BEFORE the first run: ctl 6, cased 13, rt 13, cased wr 10, free ctl
#  7, p2 rd 30, p2 wr 57, p2 ld widths 7, p2 st widths 11, ann rd 109, ann wr 109, nonword 10, four p1 fault
#  rows 5 each, edge 6, three interim rows 5 each, census 992 (handler 2 + VSIG + 988 + br), p1 widths 11 = 1426.
#  Computing it from the session lists would let a shrunk list pass its own count.
row("unasm", "%d/%d" % (UNASM["ok"], UNASM["n"]), "1426/1426", "every placed word re-read by the disassembler")
for b in UNASM["bad"][:8]:
    print("  unasm mismatch: %s" % b)

# ================================================================ score + done
npass = sum(1 for _, ok in rows if ok)
print("SCORE %d/%d" % (npass, len(rows)))
CONTROL_ROWS = ("session", "live", "unasm", "neg apparatus", "vbr reset", "t1cmp rt", "cased census",
                "free ctl", "free quiet", "free neg ctl")
_status = dict(rows)
control_ok = all(_status.get(n, False) for n in CONTROL_ROWS)    # a renamed control fails loudly
print("VME_DEFAULT_RESULT=%d/%d" % (npass, len(rows)))
print("VME_DEFAULT_CONTROL=%s" % ("OK" if control_ok else "FAIL"))
print("VME_DEFAULT_LABEL=%s" % LABEL)
print("VME_DEFAULT_ELAPSED=%.1fs" % (time.time() - t0))
red = [n for n, ok in rows if not ok]
if red:
    print("VME_DEFAULT_RED=%s" % ",".join(red))
shutil.rmtree(_TMPDIR, ignore_errors=True)
print("VME_DEFAULT_PROBE_DONE")
sys.stdout.flush()
sys.exit(0 if control_ok and npass == len(rows) else 1)
