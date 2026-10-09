#!/usr/bin/env python3
"""armmsrmodekill -- RUNG-3 WITNESS.  One privileged MSR ends the PROCESS on `-E testarm'.

BUILT FROM regress/artifacts/armmsrmodekill/WITNESSSPEC_REWRITE_grok_20260917.txt, which is a
REWRITE and not the original 16-row spec plus eight sticky notes.  That spec's amendments file
carries a SUPERSEDED banner; do not build from it.

REPAIRED after regress/artifacts/armmsrmodekill/PROBEATTACK_grok_20260917.txt (the attack on the
never-run first draft) -- see the `REPAIR' notes inline.  Summary of the repairs:
  R1  dump parsing: aligned base + little-endian assembly (read_mem32() in arm_bdt_probe.py,
      sw() in arm_flags_probe.py).  The first draft already carried both; kept.
  R2  EARLY/LATE SPLIT.  Every MSR session dumps the 0x9000 line TWICE (the arming dump of DEST
      before the stimulus, the result dump after it).  A first-match parse returns the EARLY
      line, where every post-MSR slot is still POISON -- so a correct fix would have read
      `nofire' on every kill row.  An `@MARK' pseudo-command becomes `print 0x5eed5eed' and
      the transcript is split at that token; arming is parsed only from before it, results
      only from after it.
  R3  `save 2s' plant and classifier agree, on the spec's own slots: return CPSR at DEST+8,
      SP at DEST+12, both inside the one dumped line.  The first draft planted SP at DEST+16
      and never dumped 0x9010, so ` sp' could never appear -- the row was ALWAYS red.  `rt'
      requires mode == 0x13 at the return slot, not mere existence.
  R4  the plant-dump of the MSR slot is SCORED: every MSR session dumps its whole planted
      stream before the stimulus and checks each word against WORDS, plus DEST == 0xd3 (the
      spec's "every later session repeats DEST==0xd3 + plant-dump").  A failure renders the
      row `unarmed', never `dead'.  This is what separates "died at the MSR" from "the MSR was
      never the instruction that ran".
  R5  CONTROL=DEAD stops the probe: `enc ok' red stops before any guest session; `live' or
      `pc adv' red stops before `armed'; `armed' red stops before any kill row.
  R6  `enc ok' note quoted the removed (w & 0x0FB0F000) mask; it now states the field-nibble
      test the code performs.  f_14 additionally checks rot == 0.
  R7  liveness: EOF on the pty is recorded; on EOF the child is reaped with a long deadline,
      without EOF with a short one (a live emulator never exits, and every live session used to
      burn the full 12 s).  The SIGKILL tail now READS THE STATUS: if waitpid shows the child
      exited on its own (not by our SIGKILL), alive is False.
  R8  canary accept rows also check arrival SP == 0 (spec: "arrive m=XX SP=0"), and `acc usr'
      now passes sp_at so a Load-skip (SP still BOOT_SP in USR32) reds it.

THE DEFECT, verified by reading cpu_arm.c at HEAD ef577140 -- PRE-#562; #562 replaced both exits
with latched backstops, so these lines describe the unfixed tree only:

    cpu_arm.c:606-608   arm_load_register_bank: default: fatal("...unimplemented mode %i"); exit(1);
    cpu_arm.c:559-561   arm_save_register_bank: default: same

`0xE321F014' is `MSR CPSR_c, #0x14' -- mode 0x14 is a RESERVED ARM mode, so the Load arm's
`default:' is reached and the process dies.  `%i' prints DECIMAL: `unimplemented mode 20'.

*** POLARITY: WANT IS POST-FIX CORRECT.  A PRE FAIL ON A DEFECT ROW *IS* THE REPRODUCTION. ***
*** ORACLE: EOF ALONE => DEAD.  THE TEXT IS DIAGNOSIS, NEVER HALF THE TRIGGER. ***

#562 THE FIX AND WHAT THIS PROBE NOW DETECTS.  Three guest writers can put an unmodelled mode
(anything but 10 11 12 13 17 1b 1f) into CPSR, and each now DECLINES THE MODE FIELD ONLY, with a
`(once)' announce naming its site: msr_imm (`MSR CPSR_c'), arm_pop's `LDM {..pc}^' SPSR restore,
and the DPI `MOVS pc,..' SPSR restore.  The restores keep the CURRENT mode in M[4:0] and assign
every other bit from the SPSR (DPI later forces T for an odd destination PC; not driven here).
The Save/Load `default:' arms are BACKSTOPS (latched announce, return, no exit(1)), reached only
once an unmodelled mode is ALREADY in CPSR, which no guest instruction can now install -- only a
debugger `cpsr=' assignment.  After such a plant Save's default: is reached by a guest `MSR
CPSR_c' to a modelled mode (dbg save), a DPI S-to-PC (dbg both, latch rpt) or exception entry;
Load's default: ONLY by a DPI S-to-PC executed in the planted mode (dbg both, latch rpt).  An
`LDM {..pc}^' from a planted mode stops the CPU at arm_pop's selector default: first
(pre-existing; not this fix).  POST-FIX the guest is in SVC32 with the I/F bits the write set --
`#0x14' clears I and F -- NOT in a reserved mode.  Rows added by #562: kill 1e, kill 03, rst movs,
rst ldm, zero spsr, acc movs, acc ldm, dbg save, dbg both, latch ind, latch rpt, src dpi/src pop x
{fiq irq abt und svc}, msr lbl, encl, the `if=' (I/F) pin on kill 14 / kill 15, and ` sp0' (an
actual zero SP readback) on the rows whose SP is a never-loaded bank.

MODES 0x00-0x0F ARE NOW CLAIMED.  This header used to BAN `MSR CPSR_c, #0' as "the 26-bit hole,
a different defect".  The helper declines 0x00-0x0F like any other unmodelled value, and
`zero spsr' drives exactly mode 0x00 (an SPSR never written is zero: cpu_new zero-fills).

CLASS CLOSURE (repair 3).  Enumerated from the restore repair's own inputs: the current-mode LABEL
(selects spsr_*), the LATCH it reads, the OUTCOME (declined / accepted), and the SPSR bits it
MASKS.  Each `src <path> <label>' session enters its label WITH I AND F SET (msr cpsr_c,#0xdX),
re-enters it with I and F CLEAR before the declines, and runs four restores in ONE process: ACCEPT 0xc00000df (latch clear), DECLINE 0xc00000cf (latch
clear -> set), DECLINE again (latch set), ACCEPT (latch set); each CPSR word is read back and the
site's announce count must be exactly 1.  So {FIQ IRQ ABT UND SVC} x {clear, set} x {declined,
accepted} x {DPI, POP} = 40 cells, all rowed.  Masked bits: the declined SPSR sets mode bits 0-3,
and every bit has a label whose own bit is CLEAR (bit0 IRQ; bit1 FIQ; bit2 FIQ IRQ UND SVC; bit3
FIQ IRQ ABT SVC) on BOTH paths, so a keep-mode mask that lets any of bits 0-3 through changes the
readback.  Bit 4 is EQUIVALENT (set in every modelled mode).  The helper's operand is driven with
bits 7:5 set (the 0xdX entries, 0xcf / 0xdf) and clear (every c_XX row), and bits 31:30 set (N|Z).

CONTRACT (floor clause (e)) -- the edits this detector is DESIGNED to catch:
  * exit(1) reinstated at Save's default: (dbg save, dbg both, latch rpt) or Load's (dbg both,
    latch rpt);
  * the helper answering 1 always (kill 14/15/1e), admitting 0x1c-0x1e (kill 1e), dropping its
    `& ARM_FLAG_MODE' projection (src rows: N|Z set) or WIDENING it, e.g. `& 0xff' (src rows and
    msr lbl: I|F set in the operand);
  * the guard dropped at msr_imm (kill rows), arm_pop (rst ldm, src pop x FIQ IRQ ABT UND SVC) or
    DPI (rst movs, zero spsr, src dpi x FIQ IRQ ABT UND SVC), or restricted to ONE label, or to
    one unmodelled value such as 0x14 (src rows decline 0x0f);
  * the msr_imm guard skipped at one current-mode label (msr lbl: a decline from each of FIQ IRQ
    ABT UND SYS);
  * the msr_imm decline clearing fewer than all five mode bits, e.g. `& ~0x0f' (kill 03: the
    only driven mode value with bit 4 CLEAR); the restore keep-mode mask clearing fewer than bits
    0-3 (src rows, per the bit/label table above);
  * a restore guard made unconditional, or unconditional for one label, or skipped / forced for one
    label x latch-state cell (src rows: all 40 cells; acc movs, acc ldm);
  * a WHOLE-OPERATION decline in msr_imm instead of field-only (the `if=' pin on kill rows);
  * the restore not taking N, Z, I or F from the SPSR -- forced clear, or kept from the old CPSR
    (src rows: the whole CPSR word; the declined SPSR has N Z I F SET while the CPSR it replaces
    has them CLEAR);
  * any two of the five latch sites sharing a bit (latch rpt: all five in one process; also
    dbg both, latch ind);
  * a latch that never SUPPRESSES (`|=' -> `&=', or the `|=' line deleted), or a repair applied
    only while its latch is clear (latch rpt: every site visited TWICE; src rows per label);
  * the enclosing predicates of both restores made unconditional: arm_pop's `if (return_flag)',
    the DPI template's `rd == PC' compare, and the restore's `#ifdef A__S' (encl: a plain
    `ldmia r5,{pc}', a non-S `add pc,r6,#0' and `add r0,pc,#0' -- NOT `mov pc,lr', which the
    decoder turns into `ret' and so never reaches the DPI template).
NOT CLAIMED, disclosed: unmodelled values a helper could get wrong unseen -- those never driven
through ANY path: 0x01, 0x02, 0x04-0x0e, 0x16, 0x18-0x1a, 0x1c, 0x1d.  Per path: msr_imm drives
0x03 0x14 0x15 0x1e; DPI drives 0x00 (SVC only), 0x0f, 0x14 (SVC only); arm_pop drives 0x0f,
0x14 (SVC only).  The msr_imm comment's "only the LOCAL mask changes: ic->arg[] is a cached translation"
-- no row re-executes ONE translated MSR, so a guard that wrote ic->arg[] would go unseen;
per-CPU latch isolation (one CPU only); exception entry as a Save-backstop route (no row);
T-bit / execution-state coherence on restore; the USR/SYS `LDM {pc}^' and `MSR SPSR' paths that
stop the CPU (filed separately).

NAMED-RED tally: HEAD = 17/40, RED exactly the 23 rows kill 14, kill 15, save 2s, kill 1e,
kill 03, rst movs, rst ldm, zero spsr, dbg save, dbg both, latch ind, latch rpt, the ten src *
rows and msr lbl, CONTROL=OK.  `encl' drives no unmodelled mode and is GREEN on HEAD.  `save 2s'
on HEAD is the SAME Load death as `kill 14' (EOF on the first MSR) -- it is not an independent
HEAD reproduction of Save; nor is `dbg both' a HEAD reproduction of Load (HEAD dies in Save
first).  40/40 on HEAD is a broken vehicle, not success.

Stay on `step', never `continue' (IRQ dispatch is inside `if (!single_step)').
"""
import os
import pty
import re
import select
import signal
import sys
import time

BIN = sys.argv[1] if len(sys.argv) > 1 else "../build/gxemul"
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"

STUB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "arm_bfx_stub.bin")
if not os.path.exists(STUB):
    with open(STUB, "wb") as f:
        f.write(b"\0" * 16)

CODE = 0x8000
DEST = 0x9000
BOOT_SP = 0x03FFF000
BOOT_CPSR = 0xD3
POISON = 0xDEADBEEF
MARK = "@MARK"

#  *** ONE WORDS DICT.  Every `put w' is drawn from here and every MSR session dumps its whole
#  planted stream against these entries before the stimulus (R4). ***
WORDS = {
    "mrs_r3":   0xE10F3000,              # mrs  r3, cpsr
    "str_r3":   0xE5843000,              # str  r3, [r4]
    "str_r3_4": 0xE5843004,              # str  r3, [r4,#4]
    "str_r3_8": 0xE5843008,              # str  r3, [r4,#8]
    "str_r3_c": 0xE584300C,              # str  r3, [r4,#12]
    "str_sp_8": 0xE584D008,              # str  r13,[r4,#8]
    "str_sp_c": 0xE584D00C,              # str  r13,[r4,#12]
    "str_sp_10": 0xE584D010,             # str  r13,[r4,#16]
    "mov_r0_2a": 0xE3A0002A,             # mov  r0, #0x2a
    "str_r0":   0xE5840000,              # str  r0, [r4]
    "b_self":   0xEAFFFFFE,              # b    .
}
for m in (0x03, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x17, 0x1B, 0x1E, 0x1F):
    WORDS["c_%02x" % m] = 0xE321F000 | m     # msr cpsr_c, #m
WORDS["f_14"] = 0xE328F014                   # msr cpsr_f, #0x14
#  #562: SPSR poisoning and the two restore paths.
for m in (0x14, 0x1F):
    WORDS["s_%02x" % m] = 0xE361F000 | m     # msr spsr_c, #m
WORDS["movs_pc_lr"] = 0xE1B0F00E             # movs pc, lr       (DPI S-to-PC restore)
WORDS["ldm_r5_pc_s"] = 0xE8D58000            # ldmia r5, {pc}^   (arm_pop restore)

TGT = 0x8100                                 # restore target: lr, and the word at LDMW
LDMW = 0x9100                                # where `ldm_r5_pc_s' loads pc from
TGT_OPS = ["mrs_r3", "str_r3_4", "str_sp_8"]
TGT2 = 0x8140                                # `latch ind': readback after the chained MOVS
#  #562 pass 2: words for `latch rpt' and the `src *' rows.
WORDS["ldm_r6_pc_s"] = 0xE8D68000            # ldmia r6, {pc}^
WORDS["mov_lr_8100"] = 0xE3A0EC81            # mov  lr, #0x8100  (0x81 ror 24)
WORDS["add_lr_40"] = 0xE28EE040              # add  lr, lr, #0x40
WORDS["sf_c0"] = 0xE368F103                  # msr  spsr_f, #0xc0000000  (N and Z; 0x03 ror 2)
NZ = 0xC0000000
#  #562 repair 3: label entry WITH I and F set, the class-closure SPSR values, the chained-restore
#  operands, and the enclosing-predicate controls.
for m in (0xD1, 0xD2, 0xD3, 0xD7, 0xDB, 0xDF):
    WORDS["c_%02x" % m] = 0xE321F000 | m     # msr cpsr_c, #m  (I|F|mode)
for m in (0xCF, 0xDF):
    WORDS["s_%02x" % m] = 0xE361F000 | m     # msr spsr_c, #m
WORDS["movs_pc_r5"] = 0xE1B0F005             # movs pc, r5        (DPI S-to-PC; r5 is not banked)
WORDS["add_r5_40"] = 0xE2855040              # add  r5, r5, #0x40
WORDS["ldm_r6w_pc_s"] = 0xE8F68000           # ldmia r6!, {pc}^   (arm_pop restore, chained)
WORDS["ldm_r5_pc"] = 0xE8958000              # ldmia r5, {pc}     (NO ^: return_flag stays 0)
WORDS["add_pc_r6_0"] = 0xE286F000            # add  pc, r6, #0    (non-S DPI to PC; not `ret')
WORDS["add_r0_pc_0"] = 0xE28F0000            # add  r0, pc, #0    (Rn = PC, Rd != PC)
WORDS["str_r0_c"] = 0xE584000C               # str  r0, [r4,#12]
WORDS["str_r3_10"] = 0xE5843010              # str  r3, [r4,#16]
WORDS["str_r3_14"] = 0xE5843014              # str  r3, [r4,#20]
#  OPUS CLOSURE words
WORDS["adds_r0_pc_0"] = 0xE29F0000           # adds r0, pc, #0
WORDS["ldm_r5_r0_s"] = 0xE8D50001            # ldmia r5, {r0}^
WORDS["subs_pc_lr_0"] = 0xE25EF000           # subs pc, lr, #0
WORDS["sf_ff"] = 0xE368F4FF                  # msr spsr_f, #0xff000000
WORDS["ss_ff"] = 0xE364F8FF                  # msr spsr_s, #0x00ff0000
WORDS["sx_ff"] = 0xE362FCFF                  # msr spsr_x, #0x0000ff00
WORDS["cf_0"] = 0xE32EF000                   # msr cpsr_fsx, #0
for m in (0x3F, 0x34):
    WORDS["c_%02x" % m] = 0xE321F000 | m
    WORDS["s_%02x" % m] = 0xE361F000 | m

rows = []
diagnosis = []


def row(name, got, want, note=""):
    rows.append((name, str(got), str(want), note))


def session(cmds, settle=1.6, spin=1.6):
    """ONE FRESH PROCESS per scored row that executes a guest instruction.  Returns (t, alive);
    _session_split() turns the `@MARK' pseudo-command into the early/late split (R2)."""
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-A", "-E", "testarm", "-M", "64",
                       "0x%x:%s" % (CODE, STUB)])
        os._exit(127)
    buf = ""
    eof = False

    def rd(t):
        nonlocal buf, eof
        end = time.time() + t
        while time.time() < end:
            try:
                r, _, _ = select.select([fd], [], [], 0.1)
            except OSError:
                eof = True
                return
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
            except OSError:
                eof = True
                return
            if not d:
                eof = True
                return
            buf += d.decode("utf-8", "replace")

    rd(settle)
    for c in cmds:
        if eof:
            break
        try:
            os.write(fd, (c + "\n").encode())
        except OSError:
            eof = True
            break
        rd(0.3)
    rd(spin)

    #  *** POLL, NEVER SAMPLE ONCE. ***  rd() returns immediately on EOF, so a dying child must
    #  be given time to die.  On EOF reap with a long deadline; without EOF a short one (R7).
    alive = True
    deadline = time.time() + (12.0 if eof else 3.0)
    while time.time() < deadline:
        try:
            wpid, _st = os.waitpid(pid, os.WNOHANG)
        except ChildProcessError:
            alive = False
            break
        if wpid == pid:
            alive = False
            break
        time.sleep(0.05)
    if alive:
        try:
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass
        try:
            _w, st = os.waitpid(pid, 0)
            #  R7: if the child exited on its own between the last poll and our kill, the
            #  status says so -- do not leave alive=True for a process that died by itself.
            if os.WIFEXITED(st) or (os.WIFSIGNALED(st) and os.WTERMSIG(st) != signal.SIGKILL):
                alive = False
        except ChildProcessError:
            pass
    try:
        os.close(fd)
    except OSError:
        pass
    return buf.replace("\r", ""), alive


def _session_split(cmds):
    #  Insert a unique, harmless marker command at MARK so the split survives \r stripping:
    #  `print 0x5eed5eed' is answered by the debugger (sh_intprio_probe.py measured `print
    #  0x1234'), and even if it were not, its echo carries the token.
    real = []
    for c in cmds:
        real.append("print 0x5eed5eed" if c == MARK else c)
    t, alive = session(real)
    i = t.find("5eed5eed")
    if i < 0:
        return t, "", alive, False
    #  late = everything after the marker's answer line (skip echo + answer)
    j = t.rfind("5eed5eed")
    nl = t.find("\n", j)
    late = t[nl + 1:] if nl >= 0 else ""
    return t[:i], late, alive, True


def printed(t, reg):
    #  COPIED VERBATIM from regress/lca_isalane_probe.py.  `print <reg>' emits a BARE `0x...'.
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return None if not m else int(m.group(1), 16)


def dumpcmd(addr, end=None):
    """*** ALWAYS DUMP FROM THE 16-BYTE-ALIGNED BASE. ***  debugger_cmd_dump does
    `addr = addr_start & ~0xf' and blank-pads groups before addr_start (arm_bdt_probe.py
    read_mem32(), measured 2026-09-11)."""
    base = addr & ~0xF
    top = ((end if end is not None else addr) + 16) & ~0xF
    if top <= base:
        top = base + 16
    return "dump 0x%x 0x%x" % (base, top)


def dumped(t, addr):
    """The word stored at `addr', from the LAST aligned dump line in `t' (R2: callers pass the
    early or the late half, never the whole transcript).  Memory-order bytes, little-endian
    guest: assemble like sw() in arm_flags_probe.py."""
    label = "0x%08x" % (addr & ~0xF)
    idx = (addr & 0xF) // 4
    val = None
    for line in t.splitlines():
        if line.startswith(label):
            parts = line[12:48].split()
            if len(parts) == 4 and len(parts[idx]) == 8:
                val = int.from_bytes(bytes.fromhex(parts[idx]), "little")
    return val


def plant(ops, at=CODE):
    out = []
    for i, k in enumerate(ops):
        out.append("put w 0x%x, 0x%08x" % (at + 4 * i, WORDS[k]))
    out.append("put w 0x%x, 0x%08x" % (at + 4 * len(ops), WORDS["b_self"]))
    return out


def prologue():
    """POISON DEST..DEST+16 (the post-MSR stores must overwrite them) and point r4 at DEST."""
    return ["put w 0x%x, 0x%08x" % (DEST + o, POISON) for o in (0, 4, 8, 12, 16)] \
        + ["r4=0x%x" % DEST]


PREFIX = ["mrs_r3", "str_r3"]


def msr_cmds(ops, steps_after, late_end=DEST + 12, restore=False, regs=(), poke=(),
             chain=False):
    """Standard MSR session: prefix MRS/STR to DEST, arming dumps (DEST and the whole planted
    stream), MARK, the stimulus steps, then the result dump.
    #562: restore=True also plants TGT_OPS at TGT, sets lr=TGT and the LDMW word to TGT, and
    arms all three (a fall-through past the restore lands on b_self and reads `nofire').
    `regs' are debugger assignments made BEFORE the prefix; `poke' ones AFTER the arming dumps
    (a `cpsr=' poke must follow the prefix, whose MRS arms DEST == 0xd3).
    chain=True (with restore): TGT holds `movs pc,lr' and the readback TGT_OPS move to TGT2,
    where lr points -- so one session can run an LDM^ restore and then a MOVS restore."""
    full = PREFIX + ops
    cmds = prologue() + plant(full)
    extra = {}
    rb = TGT2 if chain else TGT
    if restore:
        cmds += plant(TGT_OPS, at=rb) + ["put w 0x%x, 0x%08x" % (LDMW, TGT),
                                         "lr=0x%x" % rb, "r5=0x%x" % LDMW]
        for i, k in enumerate(TGT_OPS + ["b_self"]):
            extra[rb + 4 * i] = WORDS[k]
        extra[LDMW] = TGT
        if chain:
            cmds += plant(["movs_pc_lr"], at=TGT)
            extra[TGT] = WORDS["movs_pc_lr"]
            extra[TGT + 4] = WORDS["b_self"]
    cmds += list(regs) + ["pc=0x%x" % CODE, "step 2", dumpcmd(DEST),
                          dumpcmd(CODE, CODE + 4 * len(full))]
    if restore:
        cmds += [dumpcmd(TGT, TGT + 4 * len(TGT_OPS)), dumpcmd(LDMW)]
        if chain:
            cmds += [dumpcmd(TGT2, TGT2 + 4 * len(TGT_OPS))]
    cmds += [MARK] + list(poke) + ["step %d" % s for s in steps_after] \
        + [dumpcmd(DEST, late_end)]
    return cmds, (full, extra)


def arming(early, full):
    """R4: DEST == 0xd3 after the prefix, and every planted word reads back as its WORDS entry.
    #562: `full' may be (ops, {addr: word}) -- the extra plants (restore target, LDM word)."""
    extra = {}
    if isinstance(full, tuple):
        full, extra = full
    if dumped(early, DEST) != BOOT_CPSR:
        return False
    for i, k in enumerate(full):
        if dumped(early, CODE + 4 * i) != WORDS[k]:
            return False
    for a, w in extra.items():
        if dumped(early, a) != w:
            return False
    return True


def prog_session(code_ops, blocks=(), data=None, regs=(), segments=((), ()), late_end=DEST + 12):
    """#562 pass 2: a multi-block program.  code_ops at CODE (after PREFIX), each (addr, ops) block
    at addr, each {addr: word} data word planted; every block and data word is ARMED (dumped and
    checked before MARK).  `segments' = ((pokes, steps), ...) after MARK: debugger assignments,
    then `step N'."""
    data = data or {}
    full = PREFIX + list(code_ops)
    cmds = prologue() + plant(full)
    extra = {}
    for a, ops in blocks:
        cmds += plant(ops, at=a)
        for i, k in enumerate(list(ops) + ["b_self"]):
            extra[a + 4 * i] = WORDS[k]
    for a, w in data.items():
        cmds.append("put w 0x%x, 0x%08x" % (a, w))
        extra[a] = w
    cmds += list(regs) + ["pc=0x%x" % CODE, "step 2", dumpcmd(DEST),
                          dumpcmd(CODE, CODE + 4 * len(full))]
    for a, ops in blocks:
        cmds.append(dumpcmd(a, a + 4 * len(ops)))
    for a in data:
        cmds.append(dumpcmd(a))
    cmds.append(MARK)
    for pokes, steps in segments:
        cmds += list(pokes) + (["step %d" % steps] if steps else [])
    cmds.append(dumpcmd(DEST, late_end))
    early, late, alive, marked = _session_split(cmds)
    return early, late, alive, marked, (full, extra)


def announces(t, key):
    """#562 pass 2: how MANY `(once)' lines the named site printed -- a latch that never
    suppresses prints twice when its site is visited twice; any() could not see that."""
    return sum(1 for ln in t.splitlines() if key in ln and "(once)" in ln)


def diag_unimpl(nm, t):
    """#562: which register-bank `unimplemented mode' text a session printed (HEAD: the
    function that exit(1)ed -- the reason under test; fixed: the backstop that announced)."""
    hits = sorted(set(re.findall(r"arm_(save|load)_register_bank: unimplemented mode (\d+)", t)))
    diagnosis.append("%s: %s" % (nm, ", ".join("%s mode %s" % h for h in hits) if hits
                                 else "no bank text"))


def announced(t, key):
    """#562: a `(once)' announce from the NAMED site -- the five sites share the token, so a
    bare `(once)' cannot tell a decline from a backstop, or Save's backstop from Load's."""
    return any(key in ln and "(once)" in ln for ln in t.splitlines())


def classify(early, late, alive, marked, full, cpsr_at=DEST + 4, sp_at=None, rt_at=None,
             once_key=None, pin_if=False, backstops=False, declines=False):
    """The got string.  EOF ALONE => dead.  Arming is checked first, from the EARLY half.
    #562: once_key names the announcing site; pin_if adds the CPSR I/F pair (field-only vs
    whole-operation decline); backstops adds ` save' / ` load' per Save/Load announce."""
    if not marked or not arming(early, full):
        return "unarmed"
    if not alive:
        return "dead"
    cpsr = dumped(late, cpsr_at)
    if cpsr is None or cpsr == POISON:
        return "nofire"
    got = "m=%02x" % (cpsr & 0x1F)
    if pin_if:
        got += " if=%d" % ((cpsr >> 6) & 3)
    if sp_at is not None:
        v = dumped(late, sp_at)
        #  #562 pass 2: ` sp0' is an ACTUAL zero readback (a never-loaded bank), not merely
        #  "not BOOT_SP" -- a missing or POISON slot now renders neither token.
        if v == BOOT_SP:
            got += " sp"
        elif v == 0:
            got += " sp0"
    t = early + late
    if (announced(t, once_key) if once_key else "(once)" in t):
        got += " once"
    if declines:
        for key, tag in (("msr_imm", "msr"), ("arm_pop", "pop"), ("dpi S-to-pc", "dpi")):
            if announced(t, key):
                got += " " + tag
    if backstops:
        if announced(t, "arm_save_register_bank"):
            got += " save"
        if announced(t, "arm_load_register_bank"):
            got += " load"
    if rt_at is not None:
        v = dumped(late, rt_at)
        if v not in (None, POISON) and (v & 0x1F) == 0x13:
            got += " rt"
    return got


def report_dead(why):
    print("arm_msrmode_probe -- binary=%s label=%s machine=testarm" % (BIN, LABEL))
    print("ARMMSRMODE_CONTROL=DEAD")
    print("ARMMSRMODE_RESULT=0/0")
    print("  *** SETUP FAILED (%s) -- the vehicle is not the vehicle.  NOT 'no defect'. ***" % why)
    for nm, got, want, note in rows:
        print("  %-11s got=%-16s want=%-16s %s" % (nm, got, want, note[:56]))
    print("ARMMSRMODE_DONE")
    raise SystemExit(0)


# ---------------------------------------------------------------- enc ok  (no guest)
#  MSR immediate:  cond 00110 R 10 field(19:16) 1111 rot(11:8) imm8.  The field nibble is
#  bits 19:16 and a mask cannot substitute for it (0x0FB0F000 kills bit 0x08 and cannot tell
#  the c-form from the f-form).
bad = []
for k, w in WORDS.items():
    if k.startswith("c_"):
        if ((w >> 16) & 0xF) != 0b0001 or (w & 0xFF) != int(k[2:], 16) \
                or ((w >> 8) & 0xF) != 0 or (w & 0x00400000) or (w & 0x0FB0F000) != 0x0320F000:
            bad.append(k)
    if k == "f_14":
        if ((w >> 16) & 0xF) != 0b1000 or (w & 0xFF) != 0x14 or ((w >> 8) & 0xF) != 0 \
                or (w & 0x00400000) or (w & 0x0FB0F000) != 0x0320F000:
            bad.append(k)
    if k.startswith("s_"):
        #  #562: the SPSR form -- same frame, field nibble 0001, bit 22 (R) SET.
        if ((w >> 16) & 0xF) != 0b0001 or (w & 0xFF) != int(k[2:], 16) \
                or ((w >> 8) & 0xF) != 0 or not (w & 0x00400000) \
                or (w & 0x0FB0F000) != 0x0320F000:
            bad.append(k)
    if k == "movs_pc_lr":
        #  data-processing MOV (opcode 1101), S set, Rd = 15, Rm = 14, no shift
        if (w >> 21) & 0xF != 0xD or not (w >> 20) & 1 or (w >> 12) & 0xF != 15 \
                or w & 0xFFF != 14 or (w >> 25) & 7 != 0:
            bad.append(k)
    if k in ("ldm_r6_pc_s", "mov_lr_8100", "add_lr_40", "sf_c0"):
        #  #562 pass 2: whole-word field decode against the intended operation.
        ok = {"ldm_r6_pc_s": (w >> 25) & 7 == 0b100 and (w >> 20) & 1 and (w >> 22) & 1
              and not (w >> 21) & 1 and (w >> 16) & 0xF == 6 and w & 0xFFFF == 0x8000,
              "mov_lr_8100": (w >> 25) & 7 == 1 and (w >> 21) & 0xF == 0xD
              and not (w >> 20) & 1 and (w >> 12) & 0xF == 14
              and (((w & 0xFF) >> (2 * ((w >> 8) & 0xF))) | ((w & 0xFF)
                   << (32 - 2 * ((w >> 8) & 0xF)))) & 0xFFFFFFFF == TGT,
              "add_lr_40": (w >> 25) & 7 == 1 and (w >> 21) & 0xF == 0x4
              and not (w >> 20) & 1 and (w >> 16) & 0xF == 14 and (w >> 12) & 0xF == 14
              and w & 0xFFF == 0x40,
              "sf_c0": (w & 0x0FB0F000) == 0x0320F000 and (w & 0x00400000)
              and ((w >> 16) & 0xF) == 0b1000 and ((w >> 8) & 0xF) == 1 and (w & 0xFF) == 3,
              }[k]
        if not ok:
            bad.append(k)
    if k in ("movs_pc_r5", "add_r5_40", "ldm_r6w_pc_s", "ldm_r5_pc", "add_pc_r6_0", "add_r0_pc_0",
             "str_r0_c", "str_r3_10", "str_r3_14"):
        #  #562 repair 3: cond, class, opcode, S/W/L, Rn, Rd and operand, field by field.
        f = ((w >> 28), (w >> 25) & 7, (w >> 21) & 0xF, (w >> 20) & 1, (w >> 16) & 0xF,
             (w >> 12) & 0xF, w & 0xFFF)
        want = {"movs_pc_r5": (0xE, 0, 0xD, 1, 0, 15, 5),
                "add_r5_40": (0xE, 1, 0x4, 0, 5, 5, 0x40),
                "add_pc_r6_0": (0xE, 1, 0x4, 0, 6, 15, 0),
                "add_r0_pc_0": (0xE, 1, 0x4, 0, 15, 0, 0),
                "str_r0_c": (0xE, 2, 0xC, 0, 4, 0, 0xC),
                "str_r3_10": (0xE, 2, 0xC, 0, 4, 3, 0x10),
                "str_r3_14": (0xE, 2, 0xC, 0, 4, 3, 0x14)}.get(k)
        if k == "ldm_r6w_pc_s":
            ok = (w >> 25) & 7 == 4 and (w >> 20) & 1 and (w >> 22) & 1 and (w >> 21) & 1 \
                and (w >> 23) & 1 and not (w >> 24) & 1 and (w >> 16) & 0xF == 6 \
                and w & 0xFFFF == 0x8000
        elif k == "ldm_r5_pc":
            ok = (w >> 25) & 7 == 4 and (w >> 20) & 1 and not (w >> 22) & 1 \
                and not (w >> 21) & 1 and (w >> 23) & 1 and not (w >> 24) & 1 \
                and (w >> 16) & 0xF == 5 and w & 0xFFFF == 0x8000
        else:
            ok = f == want
        if not ok:
            bad.append(k)
    if k == "ldm_r5_pc_s":
        #  LDM: bits 27:25 = 100, L set, S (bit 22) set, W clear, Rn = 5, list = {pc} only
        if (w >> 25) & 7 != 0b100 or not (w >> 20) & 1 or not (w >> 22) & 1 \
                or (w >> 21) & 1 or (w >> 16) & 0xF != 5 or w & 0xFFFF != 0x8000:
            bad.append(k)
row("enc ok", "clean" if not bad else ",".join(bad), "clean",
    "CONTROL=DEAD. Decoder match on the PLANTED literals: MSR-imm frame (w & 0x0FB0F000) == "
    "0x0320F000, field nibble (w>>16)&0xF = 0001 c-form / 1000 f-form, rot 0, bit 22 clear, imm8 "
    "== the key's mode.")
if bad:
    report_dead("enc ok")

# ---------------------------------------------------------------- S1: live / pc adv
early, late, alive, marked = _session_split(
    prologue() + plant(["mov_r0_2a", "str_r0"])
    + ["pc=0x%x" % CODE, "step 2", dumpcmd(DEST), "print pc"])
row("live", "0x%x" % (dumped(early, DEST) or 0) if alive else "dead", "0x2a",
    "CONTROL=DEAD. Plant, step and dump executed at all.")
row("pc adv", "0x%x" % (printed(early, "pc") or 0) if alive else "dead", "0x%x" % (CODE + 8),
    "CONTROL=DEAD. The words were translated as 4-byte ARM instructions.")
if rows[-2][1] != rows[-2][2] or rows[-1][1] != rows[-1][2]:
    report_dead("live/pc adv")

# ---------------------------------------------------------------- S1b: armed
early, late, alive, marked = _session_split(
    prologue() + plant(["mrs_r3", "str_r3_4", "str_sp_8"])
    + ["pc=0x%x" % CODE, "step 3", dumpcmd(DEST, DEST + 8)])
a4, a8 = dumped(early, DEST + 4), dumped(early, DEST + 8)
armed = "%s/%s" % (("0x%x" % a4) if (alive and a4 is not None) else "?",
                   ("0x%x" % a8) if (alive and a8 is not None) else "?")
row("armed", armed, "0x%x/0x%x" % (BOOT_CPSR, BOOT_SP),
    "CONTROL=DEAD. SVC32 privileged testarm -- not USR32, not barearm, and not a debugger cpsr "
    "write. If this reds NO kill row may be scored.")
if armed != rows[-1][2]:
    report_dead("armed")

# ---------------------------------------------------------------- S2: no cbit
cmds, full = msr_cmds(["f_14", "mrs_r3", "str_r3_4", "str_sp_8"], [4])
early, late, alive, marked = _session_split(cmds)
row("no cbit", classify(early, late, alive, marked, full, sp_at=DEST + 8), "m=13 sp",
    "MSR CPSR_f writes the FLAGS byte, so the mode field is untouched and the host must live. "
    "NOT CONTROL=DEAD: a red here is a decoder finding, not a reproduction.")

# ---------------------------------------------------------------- S3/S4: the kill rows
for nm, key, dec in (("kill 14", "c_14", 20), ("kill 15", "c_15", 21)):
    cmds, full = msr_cmds([key, "mrs_r3", "str_r3_4", "str_sp_8"], [1, 3])
    early, late, alive, marked = _session_split(cmds)
    row(nm, classify(early, late, alive, marked, full, sp_at=DEST + 8, once_key="msr_imm",
                     pin_if=True), "m=13 if=0 sp once",
        "MSR CPSR_c, #0x%02x into a RESERVED mode reaches arm_load_register_bank's default: and "
        "exit(1)s. PRE is `dead' -- EOF ALONE -- and that FAIL is the reproduction. #562: "
        "if=0 pins FIELD-ONLY (the write clears I/F; a whole-op decline keeps if=3)."
        % int(key[2:], 16))
    t = early + late
    diagnosis.append("%s: %s" % (nm, "load mode %d seen" % dec
                                 if ("arm_load_register_bank: unimplemented mode %d" % dec) in t
                                 else "NO LOAD TEXT"))

# ---------------------------------------------------------------- S5: save 2s
#  R3: the spec's slots -- post-MSR1 CPSR at DEST+4, return CPSR at DEST+8, SP at DEST+12.
cmds, full = msr_cmds(["c_14", "mrs_r3", "str_r3_4", "c_13", "mrs_r3", "str_r3_8", "str_sp_c"],
                      [1, 2, 1, 3])
early, late, alive, marked = _session_split(cmds)
row("save 2s", classify(early, late, alive, marked, full, sp_at=DEST + 12, rt_at=DEST + 8),
    "m=13 sp once rt",
    "#0x14 then #0x13 in one process. On HEAD it dies on the FIRST MSR (the same Load death as "
    "kill 14). A Load-only fix still dies on the SECOND (Save of the reserved mode). Keep kill 15.")
t = early + late
diagnosis.append("save 2s: load=%s save=%s" % (
    "yes" if "arm_load_register_bank: unimplemented mode 20" in t else "no",
    "yes" if "arm_save_register_bank: unimplemented mode 20" in t else "no"))

# ---------------------------------------------------------------- S6..S13: accept side
cmds, full = msr_cmds(["c_10", "mrs_r3", "str_r3_4", "str_sp_8"], [4])
early, late, alive, marked = _session_split(cmds)
row("acc usr", classify(early, late, alive, marked, full, sp_at=DEST + 8), "m=10 sp0",
    "USR32 is ONE-WAY (the USR mask strips the c-byte). SP is the USR bank's (0), so ` sp' in "
    "the got means the bank Load did not happen.")

for nm, key, want_m in (("acc fiq", "c_11", 0x11), ("acc irq", "c_12", 0x12),
                        ("acc abt", "c_17", 0x17), ("acc und", "c_1b", 0x1B),
                        ("acc sys", "c_1f", 0x1F)):
    cmds, full = msr_cmds([key, "mrs_r3", "str_r3_4", "str_sp_8",
                           "c_13", "mrs_r3", "str_r3_c", "str_sp_10"], [8],
                          late_end=DEST + 16)
    early, late, alive, marked = _session_split(cmds)
    if not marked or not arming(early, full):
        got = "unarmed"
    elif not alive:
        got = "dead"
    else:
        arrive, sp_arr = dumped(late, DEST + 4), dumped(late, DEST + 8)
        back, sp_back = dumped(late, DEST + 12), dumped(late, DEST + 16)
        got = "%s/%s/%s/%s" % (
            "m=%02x" % (arrive & 0x1F) if arrive not in (None, POISON) else "nofire",
            "0" if sp_arr == 0 else "x",
            "m=%02x" % (back & 0x1F) if back not in (None, POISON) else "nofire",
            "sp" if sp_back == BOOT_SP else "nosp")
    row(nm, got, "m=%02x/0/m=13/sp" % want_m,
        "ACCEPT + CANARY in one row: arrive mode/SP==0 (banked, BSS-zero), return mode 0x13 with "
        "SP==BOOT_SP. A Save no-op returns SP=0; a Load no-op arrives with SP=BOOT_SP.")

cmds, full = msr_cmds(["c_13", "mrs_r3", "str_r3_4", "str_sp_8"], [4])
early, late, alive, marked = _session_split(cmds)
row("same svc", classify(early, late, alive, marked, full, sp_at=DEST + 8), "m=13 sp",
    "SAME-MODE: Load is not called, so SP-UNCHANGED *IS* the preservation check. Not 0xd3 -- "
    "#0x13 clears I|F.")

cmds, full = msr_cmds(["c_10", "c_14", "mrs_r3", "str_r3_4"], [4])
early, late, alive, marked = _session_split(cmds)
row("usr mask", classify(early, late, alive, marked, full), "m=10",
    "In USR32 the c-byte is STRIPPED, so the following #0x14 must NOT reach the mode field. "
    "The host lives and the mode stays 0x10.")

# ---------------------------------------------------------------- #562 rows
#  kill 1e: pins the helper's DOMAIN past the two driven reserved values -- a range form
#  admitting 0x1c-0x1e sends 0x1e to Load's backstop and reads m=1e.
cmds, full = msr_cmds(["c_1e", "mrs_r3", "str_r3_4", "str_sp_8"], [1, 3])
early, late, alive, marked = _session_split(cmds)
row("kill 1e", classify(early, late, alive, marked, full, sp_at=DEST + 8, once_key="msr_imm",
                        pin_if=True), "m=13 if=0 sp once",
    "MSR CPSR_c, #0x1e: unmodelled, like 0x14/0x15. Kills a helper widened by RANGE to 0x1e.")
diag_unimpl("kill 1e", early + late)

#  kill 03: the only driven mode value with bit 4 CLEAR.  Every other MSR value here has bit 4
#  set, so a decline that cleared only M[3:0] from the mask (`& ~0x0f') still wrote bit 4 = 0 from
#  this value and reached Load's backstop with mode 0x03; the rows before this one could not see it.
cmds, full = msr_cmds(["c_03", "mrs_r3", "str_r3_4", "str_sp_8"], [1, 3])
early, late, alive, marked = _session_split(cmds)
row("kill 03", classify(early, late, alive, marked, full, sp_at=DEST + 8, once_key="msr_imm",
                        pin_if=True), "m=13 if=0 sp once",
    "MSR CPSR_c, #0x03 (bit 4 clear): declined, mode unchanged. Pins the full 5-bit mode mask.")
diag_unimpl("kill 03", early + late)

#  The two SPSR restores.  `MSR SPSR_c, #0x14' poisons spsr_svc (I=F=0, mode 0x14); the restore
#  must land at TGT (else `nofire') in SVC32 -- current mode kept -- with I/F FROM THE SPSR
#  (if=0; a restore that skipped the CPSR write keeps the boot if=3) and the SVC SP.
for nm, op, site in (("rst movs", "movs_pc_lr", "dpi S-to-pc"),
                     ("rst ldm", "ldm_r5_pc_s", "arm_pop")):
    cmds, full = msr_cmds(["s_14", op], [6], restore=True)
    early, late, alive, marked = _session_split(cmds)
    row(nm, classify(early, late, alive, marked, full, sp_at=DEST + 8, once_key=site,
                     pin_if=True), "m=13 if=0 sp once",
        "MSR SPSR_c,#0x14 then %s: the restore reaches Load's default: (HEAD dead). Post-fix: "
        "at TGT, mode kept, I/F from the SPSR, `%s' announce." % (op, site))
    diag_unimpl(nm, early + late)

#  zero spsr: NO MSR at all -- spsr_svc is never written on testarm (cpu_new zero-fills), so
#  `MOVS pc,lr' from boot SVC32 restores mode 0x00.
cmds, full = msr_cmds(["movs_pc_lr"], [4], restore=True)
early, late, alive, marked = _session_split(cmds)
row("zero spsr", classify(early, late, alive, marked, full, sp_at=DEST + 8,
                          once_key="dpi S-to-pc", pin_if=True), "m=13 if=0 sp once",
    "MOVS pc,lr from boot SVC32 with spsr_svc never written (mode 0x00). HEAD dead.")
diag_unimpl("zero spsr", early + late)

#  The restores' ACCEPT side: a modelled SPSR mode must be APPLIED.  A guard made unconditional
#  (always keep the current mode) reads m=13 here.  SYS32 SP is the usr/sys bank's (0).
for nm, op in (("acc movs", "movs_pc_lr"), ("acc ldm", "ldm_r5_pc_s")):
    cmds, full = msr_cmds(["s_1f", op], [6], restore=True)
    early, late, alive, marked = _session_split(cmds)
    row(nm, classify(early, late, alive, marked, full, sp_at=DEST + 8, pin_if=True),
        "m=1f if=0 sp0",
        "MSR SPSR_c,#0x1f then %s: SYS32 restored, SP from the usr/sys bank (0), no announce."
        % op)

#  The BACKSTOPS: reached only with an unmodelled mode already in CPSR, which only the debugger
#  `cpsr=' ASSIGNMENT can now install (no bank switch, no flags
#  sync).  NOT `put', which writes MEMORY.  The poke follows the arming dumps.  once_key names
#  a DECLINE site that must NOT announce: a plant is not a guest decline (dbg both: the DPI
#  guard runs only when an SPSR was copied, and mode 0x14 has none).
cmds, full = msr_cmds(["c_13", "mrs_r3", "str_r3_4", "str_sp_8"], [4], poke=["cpsr=0xd4"])
early, late, alive, marked = _session_split(cmds)
row("dbg save", classify(early, late, alive, marked, full, sp_at=DEST + 8, backstops=True,
                         once_key="msr_imm"),
    "m=13 sp0 save",
    "cpsr=0xd4 then MSR CPSR_c,#0x13: Save's default: (HEAD exit(1)) announces and returns; "
    "Load(SVC) gives the never-saved svc SP: an actual 0, ` sp0'.")
diag_unimpl("dbg save", early + late)

cmds, full = msr_cmds(["movs_pc_lr"], [4], restore=True, poke=["cpsr=0xd4"])
early, late, alive, marked = _session_split(cmds)
row("dbg both", classify(early, late, alive, marked, full, sp_at=DEST + 8, backstops=True,
                         once_key="dpi S-to-pc"),
    "m=14 sp save load",
    "cpsr=0xd4 then MOVS pc,lr: no SPSR for 0x14, so BOTH Save's and Load's default: run in ONE "
    "instruction (Load's backstop and the distinct bits are ALSO carried by latch rpt).")
diag_unimpl("dbg both", early + late)

#  latch ind: ALL THREE guest declines in ONE process -- MSR CPSR_c,#0x14, then MSR SPSR_c,#0x14
#  and LDM {pc}^ (arm_pop) to TGT, whose MOVS pc,lr (DPI) restores the same poisoned spsr_svc to
#  TGT2.  Each site has its own mode_warned bit, so all three texts must appear; any two sharing a
#  bit print only the first.  (The other rows are each a fresh process and cannot see sharing.)
cmds, full = msr_cmds(["c_14", "s_14", "ldm_r5_pc_s"], [8], restore=True, chain=True)
early, late, alive, marked = _session_split(cmds)
#  once_key="register_bank": the generic ` once' token would be set by ANY of the three texts and
#  so carries nothing here; keyed on the backstops it pins their ABSENCE instead (no guest
#  decline may fall through to Save/Load).  The per-site ` msr pop dpi' tags are the channel.
row("latch ind", classify(early, late, alive, marked, full, sp_at=DEST + 8, pin_if=True,
                          once_key="register_bank", declines=True), "m=13 if=0 sp msr pop dpi",
    "MSR, LDM^ and MOVS declines in ONE session: three distinct latch bits, three texts.")
diag_unimpl("latch ind", early + late)

# ---------------------------------------------------------------- #562 pass 2: latch rpt
#  EVERY one of the five latch sites visited TWICE in ONE process.  Wants EXACTLY ONE announce per
#  site (a latch that never suppresses prints two; two sites sharing a bit print one between
#  them) AND the repair still applied on the second visit: the declines leave SVC32 (a=13/..),
#  the backstops leave the planted 0x14 alive (b=14/..).
#    CODE  c_14 c_15 (msr x2)  s_14  ldm r5 -> T1      T1  ldm r6 -> T2  (pop x2)
#    T2    movs pc,lr -> T3                            T3  add lr,#0x40 ; movs -> T4  (dpi x2)
#    T4    mrs ; str [r4,#4] ; str sp,[r4,#8]
#  then cpsr=0xd4, pc=T5, lr=T6:
#    T5    movs pc,lr -> T6  (save+load)   T6  add lr,#0x40 ; movs -> T7  (save+load again)
#    T7    mrs ; str [r4,#12] ; str sp,[r4,#16]
LR1, LR2, LR3, LR4, LR5, LR6, LR7 = 0x8100, 0x8140, 0x8180, 0x81C0, 0x8200, 0x8240, 0x8280
early, late, alive, marked, full = prog_session(
    ["c_14", "c_15", "s_14", "ldm_r5_pc_s"],
    blocks=[(LR1, ["ldm_r6_pc_s"]), (LR2, ["movs_pc_lr"]), (LR3, ["add_lr_40", "movs_pc_lr"]),
            (LR4, ["mrs_r3", "str_r3_4", "str_sp_8"]), (LR5, ["movs_pc_lr"]),
            (LR6, ["add_lr_40", "movs_pc_lr"]), (LR7, ["mrs_r3", "str_r3_c", "str_sp_10"])],
    data={LDMW: LR1, LDMW + 4: LR2},
    regs=["r5=0x%x" % LDMW, "r6=0x%x" % (LDMW + 4), "lr=0x%x" % LR3],
    segments=(((), 11), (["cpsr=0xd4", "pc=0x%x" % LR5, "lr=0x%x" % LR6], 6)),
    late_end=DEST + 16)
if not marked or not arming(early, full):
    got = "unarmed"
elif not alive:
    got = "dead"
else:
    def _half(ca, sa):
        c, v = dumped(late, ca), dumped(late, sa)
        if c in (None, POISON):
            return "nofire"
        return "%02x/%d/%s" % (c & 0x1F, (c >> 6) & 3,
                               "sp" if v == BOOT_SP else ("0" if v == 0 else "x"))
    t = early + late
    got = "a=%s b=%s msr%d pop%d dpi%d save%d load%d" % (
        _half(DEST + 4, DEST + 8), _half(DEST + 12, DEST + 16),
        announces(t, "msr_imm"), announces(t, "arm_pop"), announces(t, "dpi S-to-pc"),
        announces(t, "arm_save_register_bank"), announces(t, "arm_load_register_bank"))
row("latch rpt", got, "a=13/0/sp b=14/3/sp msr1 pop1 dpi1 save1 load1",
    "Five latch sites x2 in ONE process: exactly one announce each, repair kept on visit 2.")
diag_unimpl("latch rpt", early + late)

# ---------------------------------------------------------------- #562 repair 3: src dpi / src pop
#  CLASS CLOSURE of label x latch x outcome x masked bits (see the header).  Per label and path,
#  ONE process, four chained restores, each read back:
#    enter the label with I|F set; SPSR := N|Z|0xdf; restore     -> ACCEPT, latch clear  (R1)
#    re-enter it with I|F CLEAR;  SPSR_c := 0xcf;   restore     -> DECLINE, latch clear (R2)
#                                                    restore     -> DECLINE, latch SET   (R3)
#                                 SPSR_c := 0xdf;   restore     -> ACCEPT, latch set    (R4)
#  DPI chains through `movs pc,r5' (lr is banked; r5 is not) with r5 += 0x40 per block; POP chains
#  through `ldmia r6!,{pc}^' over a table of block addresses.  Want R1 = R4 = c00000df and R2 = R3
#  = c00000c0|label (mode kept, N Z I F from the SPSR), and EXACTLY ONE announce from the site.
BLK = [TGT + 0x40 * i for i in range(4)]     # 0x8100 0x8140 0x8180 0x81c0
for lab, mode in (("fiq", 0x11), ("irq", 0x12), ("abt", 0x17), ("und", 0x1B), ("svc", 0x13)):
    ck = "c_%02x" % (0xC0 | mode)            # first entry: I|F SET (helper operand bits 7:6)
    cc = "c_%02x" % mode                     # re-entry: I|F CLEAR, so the declines' I/F (set in
                                             # the SPSR) can only have come from the SPSR
    for path in ("dpi", "pop"):
        if path == "dpi":
            early, late, alive, marked, full = prog_session(
                [ck, "sf_ff", "ss_ff", "sx_ff", "s_df", "movs_pc_r5"],
                blocks=[(BLK[0], ["mrs_r3", "str_r3_4", "add_r5_40", "cf_0", cc, "s_cf",
                                  "movs_pc_r5"]),
                        (BLK[1], ["mrs_r3", "str_r3_8", "add_r5_40", "cf_0", cc, "movs_pc_r5"]),
                        (BLK[2], ["mrs_r3", "str_r3_c", "add_r5_40", "s_df", "movs_pc_r5"]),
                        (BLK[3], ["mrs_r3", "str_r3_10"])],
                regs=["r5=0x%x" % BLK[0]],
                segments=(((), 26),), late_end=DEST + 0x14)
            key = "dpi S-to-pc"
        else:
            early, late, alive, marked, full = prog_session(
                [ck, "sf_ff", "ss_ff", "sx_ff", "s_df", "ldm_r6w_pc_s"],
                blocks=[(BLK[0], ["mrs_r3", "str_r3_4", "cf_0", cc, "s_cf", "ldm_r6w_pc_s"]),
                        (BLK[1], ["mrs_r3", "str_r3_8", "cf_0", cc, "ldm_r6w_pc_s"]),
                        (BLK[2], ["mrs_r3", "str_r3_c", "s_df", "ldm_r6w_pc_s"]),
                        (BLK[3], ["mrs_r3", "str_r3_10"])],
                data={LDMW + 4 * i: BLK[i] for i in range(4)},
                regs=["r6=0x%x" % LDMW],
                segments=(((), 23),), late_end=DEST + 0x14)
            key = "arm_pop"
        if not marked or not arming(early, full):
            got = "unarmed"
        elif not alive:
            got = "dead"
        else:
            vals = [dumped(late, DEST + o) for o in (4, 8, 12, 16)]
            got = " ".join("nofire" if v in (None, POISON) else "%08x" % v for v in vals) \
                + " n=%d" % announces(early + late, key)
        acc, dec = 0xFFFFFFDF, 0xFFFFFFC0 | mode
        row("src %s %s" % (path, lab), got, "%08x %08x %08x %08x n=1" % (acc, dec, dec, acc),
            "%s from %s: accept, decline, decline (latch set), accept; one announce."
            % (path.upper(), lab.upper()))
        diag_unimpl("src %s %s" % (path, lab), early + late)

# ---------------------------------------------------------------- #562 repair 3: msr lbl
#  The msr_imm guard at every current-mode label it can run in (USR strips the c-byte): enter
#  FIQ, IRQ, ABT, UND, SYS in turn WITH I|F set, and in each write #0x14.  Each decline keeps the
#  label and clears I/F (the c-byte 0x14 has them clear).  One announce in total.
seq, blocks = [], []
for i, m in enumerate((0x11, 0x12, 0x17, 0x1B, 0x1F)):
    seq += ["c_%02x" % (0xC0 | m), "c_14", "mrs_r3", ("str_r3_4", "str_r3_8", "str_r3_c",
                                                      "str_r3_10", "str_r3_14")[i]]
early, late, alive, marked, full = prog_session(seq, segments=(((), 20),), late_end=DEST + 0x14)
if not marked or not arming(early, full):
    got = "unarmed"
elif not alive:
    got = "dead"
else:
    vals = [dumped(late, DEST + o) for o in (4, 8, 12, 16, 20)]
    got = " ".join("nofire" if v in (None, POISON) else "%02x" % v for v in vals) \
        + " n=%d" % announces(early + late, "msr_imm")
row("msr lbl", got, "11 12 17 1b 1f n=1",
    "MSR CPSR_c,#0x14 from FIQ IRQ ABT UND SYS: declined at every label, one announce.")
diag_unimpl("msr lbl", early + late)

# ---------------------------------------------------------------- #562 repair 3: encl
#  The restores' ENCLOSING predicates.  SVC with spsr_svc = 0x1f (a VALID, different mode), then
#  three PC writes that must NOT restore it: a plain `ldmia r5,{pc}' (return_flag 0), a non-S
#  `add pc,r6,#0' (the A__PC template instance, not the `ret' shortcut that `mov pc,lr' decodes
#  to), and `add r0,pc,#0' (Rn = PC, Rd != PC: no PC write at all).  Wants m=13 after each and
#  r0 = its own address + 8.
E1, E2 = TGT, TGT + 0x40
early, late, alive, marked, full = prog_session(
    ["s_1f", "ldm_r5_pc"],
    blocks=[(E1, ["mrs_r3", "str_r3_4", "add_pc_r6_0"]),
            (E2, ["add_r0_pc_0", "str_r0_c", "mrs_r3", "str_r3_8"])],
    data={LDMW: E1}, regs=["r5=0x%x" % LDMW, "r6=0x%x" % E2],
    segments=(((), 9),), late_end=DEST + 0x10)
if not marked or not arming(early, full):
    got = "unarmed"
elif not alive:
    got = "dead"
else:
    m1, m2, r0 = dumped(late, DEST + 4), dumped(late, DEST + 8), dumped(late, DEST + 12)
    got = " ".join("nofire" if v in (None, POISON) else f(v)
                   for v, f in ((m1, lambda x: "%02x" % (x & 0x1F)),
                                (m2, lambda x: "%02x" % (x & 0x1F)), (r0, lambda x: "%x" % x)))
row("encl", got, "13 13 %x" % (E2 + 8),
    "Plain LDM {pc}, non-S ADD pc, ADD r0,pc with spsr_svc = 0x1f: none may restore the SPSR.")

T2, T3, T4, T5 = 0x8200, 0x8300, 0x8340, 0x8380
T6 = 0x83C0
early, late, alive, marked, full = prog_session(
    ["s_3f", "ldm_r5_pc_s"],
    blocks=[(TGT, []), (T2, ["s_3f", "movs_pc_lr"]), (T3, ["c_3f"]), (T4, ["c_34"]),
            (T5, ["s_34", "ldm_r5_pc_s"]), (T6, ["s_34", "movs_pc_lr"])],
    data={LDMW: TGT}, regs=["r5=0x%x" % LDMW, "lr=0x%x" % TGT],
    segments=(((), 2), (["print cpsr", "cpsr=0xd3", "pc=0x%x" % T2, "lr=0x%x" % TGT], 2),
              (["print cpsr", "cpsr=0xd3", "pc=0x%x" % T3], 1),
              (["print cpsr", "cpsr=0xd3", "pc=0x%x" % T4], 1),
              (["print cpsr", "cpsr=0xd3", "pc=0x%x" % T5], 2),
              (["print cpsr", "cpsr=0xd3", "pc=0x%x" % T6, "lr=0x%x" % TGT], 2),
              (["print cpsr"], 0)))
if not marked or not arming(early, full):
    got = "unarmed"
elif not alive:
    got = "dead"
else:
    vals = re.findall(r"print\s+cpsr\s*\n\s*(0x[0-9a-f]+)", late)
    t = early + late
    got = " ".join("%02x" % (int(v, 16) & 0xff) for v in vals) + " n=%d" % (
        announces(t, "msr_imm") + announces(t, "arm_pop") + announces(t, "dpi S-to-pc"))
row("tbit", got, "3f 3f 3f 33 33 33 n=3",
    "T-set accept via pop/DPI/msr (0x3f), T-set decline via msr/pop/DPI (0x34): T from the operand.")
T7 = 0x8400
early, late, alive, marked, full = prog_session(
    ["s_1f", "adds_r0_pc_0", "mov_r0_2a", "mrs_r3", "str_r3_4", "ldm_r5_r0_s", "mrs_r3",
     "str_r3_8", "s_14", "subs_pc_lr_0"],
    blocks=[(T7, ["mrs_r3", "str_r3_c", "c_11", "c_03", "mrs_r3", "str_r3_10"])],
    data={LDMW: 0x12345678}, regs=["r5=0x%x" % LDMW, "lr=0x%x" % T7],
    segments=(((), 16),), late_end=DEST + 0x14)
if not marked or not arming(early, full):
    got = "unarmed"
elif not alive:
    got = "dead"
else:
    vals = [dumped(late, DEST + o) for o in (4, 8, 12, 16)]
    got = " ".join("nofire" if v in (None, POISON) else "%02x" % (v & 0x1f) for v in vals)
row("encl2", got, "13 13 13 11",
    "adds r0,pc / ldm {r0}^ must not restore; subs pc,lr declines 0x14; msr #0x03 at FIQ declined.")
row("row count", len(rows) + 1, 42, "identity row (floor clause (c)): the row set is complete.")

# ---------------------------------------------------------------- report
print("arm_msrmode_probe -- binary=%s label=%s machine=testarm" % (BIN, LABEL))
print("ARMMSRMODE_CONTROL=OK")
n = 0
reds = []
for nm, got, want, note in rows:
    ok = (got == want)
    n += 1 if ok else 0
    if not ok:
        reds.append(nm)
    print("  %-11s got=%-18s want=%-18s %-4s %s" % (nm, got, want, "ok" if ok else "FAIL", note[:64]))
print("ARMMSRMODE_RESULT=%d/%d" % (n, len(rows)))
print("ARMMSRMODE_REDS=%s" % (",".join(reds) if reds else "none"))
for d in diagnosis:
    print("  diag  %s" % d)
EXPECT = ("kill 14,kill 15,save 2s,kill 1e,kill 03,rst movs,rst ldm,zero spsr,dbg save,dbg both,"
          "latch ind,latch rpt," + ",".join("src %s %s" % (p, m) for m in
                                          ("fiq", "irq", "abt", "und", "svc")
                                          for p in ("dpi", "pop")) + ",msr lbl")
print("ARMMSRMODE_EXPECT_HEAD_REDS=%s" % EXPECT)
print("ARMMSRMODE_TALLY_MATCHES_HEAD_EXPECT=%s" % ("yes" if ",".join(reds) == EXPECT else "no"))
print("ARMMSRMODE_DONE")
