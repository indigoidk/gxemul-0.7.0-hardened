#!/usr/bin/env python3
"""
maple_dmaaddr_probe.py -- regression detector for `mapledmaaddr' (#528) on UNMODIFIED `-E dreamcast'.

src/devices/dev_dreamcast_maple.c, case 0x04 (MAPLE_DMAADDR), read arm: it computed `odata = d->dmaaddr' and then
called fatal() and exit(1), so an ordinary guest read ended the emulator.  #528 is ACCEPT: the read now returns the
field, quietly, like MAPLE_ENABLE's.  Promoted from the rung-3 witness
regress/artifacts/mapledmaaddr/agy_maple_witness_20260912.py (committed 4/12, fix 12/12), with the rows the pass-1
panel and Fable's ruling (artifacts/mapledmaaddr/fable_pass1_20260912.md) owed.

Every register access is a real SH4 guest instruction (`mov.l', or `mov.b' / `mov.w' where the row says so) stepped
through the cold debugger: the maple device is registered DM_DEFAULT, so the debugger's own dump/put never reach its
handler.  Every load destination is seeded with a POISON value distinct from every want, so a fix that silently skips
the load cannot pass a value row.

CONTRACT (vacuity-floor clause e).  Designed to catch, and each MEASURED in a kill table under
artifacts/mapledmaaddr/ (killtable2_20260912/, killtable3_20260912/, killtable4_20260912/): the removed
fatal()+exit(1) reinstated (HEAD); a diagnostic alone -- verbatim, reworded WITH or WITHOUT the device name, latched,
or printing only a bare hex value, a blank line, a bare carriage return or a prompt-shaped line -- because the silence
row counts, in the twelve read sessions, any transcript line outside the debugger's quiet grammar AND any line class
(hex / put / disassembly / prompt) whose count differs from what the session's commands owe, any interior blank line
and any CR that is not the pty's CRLF (never a device name); exit(1) alone;
the FAULT idiom `return 0' (a silent load-skip on SH4, where memory_rw.c raises no exception); DECLINE, unconditional
or keyed on the consumer's partitions -- `read aligned' (a 32-byte-aligned value), `read enabled' (after
MAPLE_ENABLE = 1) and their joint cell `read joint'; an exit keyed on either partition; the read hoisted out of its
`relative_addr == 0x04' guard; 0x04 widened onto another case label (a read at EVERY other label, `other 0x..'), onto
a single-bit alias in the default arm (`alias 0x0c/24/44/84', and through the low bits by the SUB-WORD accesses that
reach them, `alias 0x05' mov.b and `alias 0x06' mov.w), or onto 0x00 (`alias 0x00'); a read arm that also writes
MAPLE_ENABLE or the timeout (`other pre read' then `other 0x14' / `other 0x80'); a read that clears the field (`double
read 2'); an effect that starts on the third read (`reread 3'); masking of the low five bits; an exit keyed on the
value 0, 4, bit 30, or a 16- or 8-bit access (`read width16', `read width8').
NOT COVERED, each clause (e) -- the arm copies the field and tests no partition of it, and DEPENDS-ON's bound stops
at the enclosing function: an effect keyed on another exact value, or on a bit pattern all-ones does not set; any
single SET bit is pinned by all-ones by construction but only bit 30 was measured; masking of HIGH bits is covered by
the values but was not separately measured; an effect starting after the third read in one process (counter > 3);
side effects on sibling state the rows never read back (MAPLE_STATE reads a constant 0; the port devices; anything
read only by maple_do_dma_xfer()); effects keyed on the environment (time, verbosity, the host); 64-bit reads (no
reachable 8-byte callback on this SH4); a `writeflag' that is neither MEM_READ nor MEM_WRITE (no caller passes one --
EQUIVALENT); moving the assignment out of the `else' (the tail ignores odata on a write -- EQUIVALENT); a diagnostic
that prints no byte (`fatal("")' -- EQUIVALENT: nothing reaches the guest or the operator).  The
consumer-keyed forms (`enable', the alignment bits, the read count) are outside the BOUND, not merely value cells:
`d->enable' is read by maple_do_dma_xfer(), never by the guarded body.  Their rows are L1 -- licensed because cheap,
never graded floor because cheap.
NO ROW asserts what a read returns AFTER a DMA transfer.  Whether the transfer's cursor update (`d->dmaaddr = addr'
at the end of maple_do_dma_xfer) is architectural is the separate row `mapledmaadvance', whose detector will observe
it through this read arm using the refusal message's printed field as its oracle -- never a computed `P + 12'.

Sentinel: MAPLE_DMAADDR_PROBE_DONE (plus MAPLE_DMAADDR_RESULT=n/N and MAPLE_DMAADDR_CONTROL=OK|FAIL).
"""

import os
import pty
import re
import select
import sys
import time

if len(sys.argv) < 2:
    sys.stderr.write("usage: maple_dmaaddr_probe.py <gxemul> [kernel] [label]\n")
    sys.exit(2)

BIN = sys.argv[1]
KERNEL = sys.argv[2] if len(sys.argv) > 2 else "/mnt/c/DocumentNoSnc/CC/GXEMUL/_images/openbsd76-landisk-bsd.rd"
LABEL = sys.argv[3] if len(sys.argv) > 3 else ""

MAPLE_DMAADDR = 0xa05f6c04
MAPLE_RESET2 = 0xa05f6c10
MAPLE_SPEED = 0xa05f6c80

CODE = 0x8c001000
MARKER = 0x8c001f04
POISON = 0xa5a55a5a            # seeded into every load destination; differs from every want below

BRA_SELF = 0xaffe
NOP = 0x0009

VAL_A = 0x8c012345             # nonzero high bits and nonzero low five bits
VAL_B = 0x0c00001f             # all five low bits set
VAL_4 = 0x00000004             # the value 4 (codex's `d->dmaaddr == 0x04' swap) -- clause (e), L1
VAL_ONES = 0xffffffff          # every bit set: pins any single-bit-SET exit -- clause (e), L1
VAL_R = 0x13579bdf             # the replacing write
VAL_ALIGN = 0x0c0f0000         # 32-byte aligned and nonzero: the only class maple_do_dma_xfer() accepts
MAPLE_ENABLE = 0xa05f6c14


def run(ops, at):
    put = ["put h 0x%x, 0x%04x" % (at + 2 * i, op) for i, op in enumerate(ops)]
    put += ["put h 0x%x, 0x%04x" % (at + 2 * len(ops), BRA_SELF),
            "put h 0x%x, 0x%04x" % (at + 2 * len(ops) + 2, NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]


LD_B, LD_W, LD_L = 0x6000, 0x6001, 0x6002     # mov.b / mov.w / mov.l @Rm, Rn (sign-extending)


def load32(addr, at, dest=2, op=LD_L):
    """mov.l @r1, r<dest> (or the .b / .w form), with r<dest> POISONED first."""
    return ["r1=0x%x" % addr, "r%d=0x%x" % (dest, POISON)] + \
        run([op | (1 << 4) | (dest << 8)], at) + ["print r%d" % dest]


def store32(addr, val, at):
    """mov.l r2, @r1"""
    return ["r1=0x%x" % addr, "r2=0x%08x" % val] + run([0x2122], at)


def session(cmds, settle=2.5, spin=1.2):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "dreamcast", "-M", "64", KERNEL])
        os._exit(127)
    buf = ""

    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.20)
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
            except OSError:
                return False
            if not d:
                return False
            buf += d.decode("latin-1", "replace")
        return True

    rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            break
        if not rd(spin if i == len(cmds) - 1 else 0.20):
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
    how = "nostatus"
    try:
        _, stat = os.waitpid(pid, 0)
        if os.WIFSIGNALED(stat):
            how = "sig%d" % os.WTERMSIG(stat)
        elif os.WIFEXITED(stat):
            how = "exit%d" % os.WEXITSTATUS(stat)
    except OSError:
        pass
    return buf, how


#  THE SILENCE CHANNEL (pass 2, 2026-09-12).  The first version counted sessions whose transcript contained the text
#  `dreamcast_maple' -- which IS one literal, and a token-free `fatal("[ maple: DMAADDR read ]")' passed it (codex, glm,
#  kimi).  A clean session prints only this grammar after the first prompt -- measured on the fixed build: the
#  `GXemul> ' command echo, a bare hex value (`r1=' / `print'), a `put' confirmation `0x...: hhhh', and the stepped
#  instruction's disassembly `8c001000:  2122  mov.l ...'.  ANY other line is the emulator speaking, whatever it says.
_QUIET = (re.compile(r"^$"), re.compile(r"^GXemul> "), re.compile(r"^0x[0-9a-f]+$"),
          re.compile(r"^0x[0-9a-f]+: [0-9a-f]+$"), re.compile(r"^[0-9a-f]{8}:\s+[0-9a-f]{4}\s"))


def noise(t, cmds=None):
    """Lines after the first debugger prompt that are not in the quiet grammar -- AND, when the session's commands are
    given, any surplus in a line CLASS.  The §F2 pass (codex) showed a grammar alone is a whitelist of SHAPES: a
    diagnostic that prints a bare hex line (`fatal("0x%08x\\n", ...)') fits the shape of a `print' answer.  So each
    command is owed exactly its expected output: one hex line per `rN=' / `pc=' / `print', one `put' confirmation per
    `put', one disassembly line per stepped instruction, one prompt line per command.  A count that differs is the
    emulator speaking.  And the grammar's two shape-free members are closed the same way (§F2, grok: `fatal("\\n")'
    prints only a BLANK line): a clean session's only empty line is the one after its final newline, and every CR is
    the pty's CRLF -- measured on the fixed build, 3 x 3 sessions (blank_measure: blanks=1, bare CR 0)."""
    i = t.find("GXemul> ")
    raw = t[i:] if i >= 0 else t
    body = raw.replace("\r", "").split("\n")
    bad = [ln for ln in body if not any(p.match(ln) for p in _QUIET)]
    if cmds is not None:
        want_hex = sum(1 for c in cmds if re.match(r"^(r\d+=|pc=|print )", c))
        want_put = sum(1 for c in cmds if c.startswith("put "))
        want_dis = sum(int(c.split()[1]) for c in cmds if c.startswith("step "))
        got_hex = sum(1 for ln in body if _QUIET[2].match(ln))
        got_put = sum(1 for ln in body if _QUIET[3].match(ln))
        got_dis = sum(1 for ln in body if _QUIET[4].match(ln))
        #  the `quit' echo is not counted: it is typed after the last command and may miss the read window on a
        #  loaded host, which must not red a clean session
        got_prm = sum(1 for ln in body if ln.startswith("GXemul> ") and ln != "GXemul> quit")
        blanks = sum(1 for ln in body[:-1] if ln == "")
        bare_cr = raw.count("\r") - raw.count("\r\n")
        for name, g, w in (("hex", got_hex, want_hex), ("put", got_put, want_put), ("disasm", got_dis, want_dis),
                           ("prompt", got_prm, len(cmds)), ("interior blank", blanks, 0), ("bare CR", bare_cr, 0)):
            if g != w:
                bad.append("%s lines %d, commands owe %d" % (name, g, w))
    return bad


def printed(t, reg, nth=-1):
    m = re.findall(r"print\s+%s\s*\r?\n\s*(0x[0-9a-f]+)" % reg, t)
    return m[nth] if len(m) >= (nth + 1 if nth >= 0 else 1) else "absent"


def hx(v):
    if isinstance(v, int):
        return "0x%x" % v
    if isinstance(v, str) and v.startswith("0x"):
        try:
            return "0x%x" % int(v, 16)
        except ValueError:
            return v
    return str(v)


rows = []


def row(name, got, want, note=""):
    g, w = hx(got), hx(want)
    ok = (g == w)
    rows.append((name, ok))
    print("%-18s %-14s %-14s %-44s %s" % (name, g, w, note, "ok" if ok else "FAIL"))
    sys.stdout.flush()


#  The READ sessions: every one of them must be silent -- noise() finds no line outside the quiet grammar and no
#  surplus in any line class.  A write to MAPLE_DMAADDR or MAPLE_ENABLE prints nothing (the former's debug() is
#  commented out) and every other register read in these sessions is a quiet arm, so ANY extra output is the read
#  speaking.  Keyed on the channel, never on one literal string (Fable pass 1: the literal form is vacuous by
#  construction against a reworded or latched announce; §F2, codex: nor on a line SHAPE alone).
READS = []


def rsession(cmds):
    t, how = session(cmds)
    READS.append((t, how, cmds))
    return t, how


print("MAPLE_DMAADDR DETECTOR -- rung 3, unmodified -E dreamcast   binary=%s  label=%s" % (BIN, LABEL))
print("%-18s %-14s %-14s %-44s %s" % ("row", "got", "want", "note", ""))

# -- controls ------------------------------------------------------------------------------------------------------
t, how = session(["put w 0x8c001800, 0x12345678"] + load32(0x8c001800, CODE))
row("ctrl live", printed(t, "r2"), 0x12345678, "RAM round trip through the same apparatus")
t, how = session(load32(0xffd00010, CODE))
g = printed(t, "r2")
row("ctrl devsig sh4", ("0x%x" % (int(g, 16) & 0xffff)) if g.startswith("0x") else g, 0xda74,
    "SH4 IPRD reset value: a device, not RAM")
t, how = session(store32(MAPLE_SPEED, 0x12345678, CODE) + load32(MAPLE_SPEED, CODE + 0x20))
row("ctrl devsig maple", printed(t, "r2"), 0x12340000, "MAPLE_SPEED shifts/masks: this device decodes")

# -- the accept cell, FLOOR: poisoned destination, high and low-five bits ------------------------------------------
t, how = rsession(store32(MAPLE_DMAADDR, VAL_A, CODE) + load32(MAPLE_DMAADDR, CODE + 0x20))
row("read val_a", printed(t, "r2"), VAL_A, "high + low bits; destination poisoned")
t, how = rsession(store32(MAPLE_DMAADDR, VAL_B, CODE) + load32(MAPLE_DMAADDR, CODE + 0x20))
row("read val_b", printed(t, "r2"), VAL_B, "low five bits all set")

# -- the dominating-predicate complement, FLOOR.  `switch (relative_addr)' partitions the offsets by CASE LABEL, so the
#  complement of `relative_addr == 0x04' is every other label: with the field nonzero, each must answer its OWN value
#  (all 0 on a fresh device), never the field.  Kills the hoist and a label widened onto 0x04 (`case 0x04: case 0x18:').
#  Pass 1 rowed RESET2 alone; pass 2 (kimi's `case 0x04: case 0x18:', grok's `relative_addr & 4') showed one label
#  pins only itself.  All six reads are quiet arms, so this is a silence session too.  The DMAADDR read FIRST (§F2,
#  kimi): a read arm that also writes a sibling field (`d->enable = 1;', `d->timeout = ...') would show at `other 0x14'
#  / `other 0x80' -- but only if the read happens before them.  L1: sibling-state side effects are clause (e).
OTHER = ((0x10, "RESET2"), (0x14, "ENABLE"), (0x18, "STATE"), (0x80, "SPEED"), (0x8c, "RESET"), (0xe8, "0xe8"))
cmds = store32(MAPLE_DMAADDR, VAL_A, CODE) + load32(MAPLE_DMAADDR, CODE + 0x20, dest=9)
for i, (off, _) in enumerate(OTHER):
    cmds += load32(0xa05f6c00 + off, CODE + 0x20 * (i + 2), dest=2 + i)
t, how = rsession(cmds)
row("other pre read", printed(t, "r9"), VAL_A, "the DMAADDR read before the six below")
for i, (off, name) in enumerate(OTHER):
    row("other 0x%02x" % off, printed(t, "r%d" % (2 + i)), 0x0, "%s reads 0 with the field nonzero" % name)

# -- single-bit ALIASES of 0x04, FLOOR: `switch (relative_addr & ~bit)' folds 0x04|bit onto DMAADDR (codex: & ~0x08,
#  & ~0x20, & ~0x40).  The aligned ones not already a case label are DEFAULT-arm offsets, which print their own
#  `UNIMPLEMENTED read' diagnostic by design -- so this session is NOT a silence session; the channel is the VALUE: the
#  default arm answers 0, an alias would answer the field.  0x14 is already `other 0x14'.  The low bits (§F2, kimi):
#  0x05 and 0x06 are misaligned for mov.l but NOT for mov.b / mov.w, which reach the device with relative_addr 5 / 6 --
#  so `& ~0x01' and `& ~0x02' fold them onto DMAADDR and answer the field's low byte 0x45 / half 0x2345.  And 0x00
#  (§F2, codex): a `case 0x00:' stacked on the DMAADDR label.
ALIAS = ((0x0c, LD_L), (0x24, LD_L), (0x44, LD_L), (0x84, LD_L), (0x00, LD_L), (0x05, LD_B), (0x06, LD_W))
cmds = store32(MAPLE_DMAADDR, VAL_A, CODE)
for i, (off, op) in enumerate(ALIAS):
    cmds += load32(0xa05f6c00 + off, CODE + 0x20 * (i + 1), dest=2 + i, op=op)
t, how = session(cmds)
for i, (off, op) in enumerate(ALIAS):
    row("alias 0x%02x" % off, printed(t, "r%d" % (2 + i)), 0x0,
        "default arm answers 0, not the field (mov.%s)" % {LD_B: "b", LD_W: "w", LD_L: "l"}[op])

# -- width, L1 (clause (e): `len' is read by the common tail, not the guarded body): a 16-bit read.  mov.w sign-extends;
#  VAL_A's low half 0x2345 is positive.  Kills an exit or diagnostic keyed on `len != 4' (glm, kimi).
#  And an 8-bit read (§F2, kimi: `len == 1'): mov.b, VAL_A's low byte 0x45, also positive.
t, how = rsession(store32(MAPLE_DMAADDR, VAL_A, CODE) + load32(MAPLE_DMAADDR, CODE + 0x20, dest=2, op=LD_W)
                  + load32(MAPLE_DMAADDR, CODE + 0x40, dest=3, op=LD_B))
row("read width16", printed(t, "r2"), 0x2345, "mov.w: low half, 16-bit access")
row("read width8", printed(t, "r3"), 0x45, "mov.b: low byte, 8-bit access")

# -- survival + exit status, FLOOR: the exit(1) half -----------------------------------------------------------------
cmds = ["put w 0x%x, 0x0" % MARKER, "r1=0x%x" % MAPLE_DMAADDR, "r2=0x%x" % POISON,
        "r3=0x55aa55aa", "r4=0x%x" % MARKER] + run([0x6212, 0x2432], CODE) + load32(MARKER, CODE + 0x20, dest=5)
t, how = rsession(cmds)
row("marker survive", printed(t, "r5"), 0x55aa55aa, "the store after the read executes")
row("exit status", how, "exit0", "the session ends by `quit'")

# -- clause (e) cells, L1 (cheap, disclosed by class) ----------------------------------------------------------------
t, how = rsession(load32(MAPLE_DMAADDR, CODE))
row("initial zero", printed(t, "r2"), 0x0, "fresh device: field is zero")
t, how = rsession(store32(MAPLE_DMAADDR, VAL_4, CODE) + load32(MAPLE_DMAADDR, CODE + 0x20))
row("read four", printed(t, "r2"), VAL_4, "the value 4")
t, how = rsession(store32(MAPLE_DMAADDR, VAL_ONES, CODE) + load32(MAPLE_DMAADDR, CODE + 0x20))
row("read all ones", printed(t, "r2"), VAL_ONES, "every bit set")
#  The CONSUMER's partitions (Opus pass 2, measured): maple_do_dma_xfer() tests `!d->enable' and `addr & 0x1f', and
#  every other row writes a value with nonzero low five bits on a device never enabled -- so a read DECLINED or KILLED
#  only for a 32-byte-aligned value, or only once enabled, scored 16/16.  An aligned nonzero value is exactly what a
#  working driver writes.  Clause (e) by the pass-1 rule (field & bit; enable is not a field the body reads), taken
#  as L1 because two rows kill all four measured forms.
t, how = rsession(store32(MAPLE_DMAADDR, VAL_ALIGN, CODE) + load32(MAPLE_DMAADDR, CODE + 0x20))
row("read aligned", printed(t, "r2"), VAL_ALIGN, "32-byte-aligned nonzero, as a driver writes")
#  And the JOINT cell (§F2, codex): a decline keyed on `enable && aligned' passes both rows above, each of which holds
#  only one half.  Same session: enabled, then an aligned value written and read.
t, how = rsession(store32(MAPLE_ENABLE, 1, CODE) + store32(MAPLE_DMAADDR, VAL_A, CODE + 0x20)
                  + load32(MAPLE_DMAADDR, CODE + 0x40, dest=2) + store32(MAPLE_DMAADDR, VAL_ALIGN, CODE + 0x60)
                  + load32(MAPLE_DMAADDR, CODE + 0x80, dest=3))
row("read enabled", printed(t, "r2"), VAL_A, "after MAPLE_ENABLE = 1 (no transfer started)")
row("read joint", printed(t, "r3"), VAL_ALIGN, "enabled AND 32-byte aligned: both consumer partitions")
t, how = rsession(store32(MAPLE_DMAADDR, VAL_A, CODE) + load32(MAPLE_DMAADDR, CODE + 0x20, dest=2)
                  + load32(MAPLE_DMAADDR, CODE + 0x40, dest=3) + load32(MAPLE_DMAADDR, CODE + 0x60, dest=4))
row("double read 1", printed(t, "r2"), VAL_A, "first of three reads, no write between")
row("double read 2", printed(t, "r3"), VAL_A, "second read: the first did not clear it")
row("reread 3", printed(t, "r4"), VAL_A, "third read (a per-process read count)")
t, how = rsession(store32(MAPLE_DMAADDR, VAL_A, CODE) + store32(MAPLE_DMAADDR, VAL_R, CODE + 0x20)
                  + load32(MAPLE_DMAADDR, CODE + 0x40))
row("write replace", printed(t, "r2"), VAL_R, "a second write replaces what the read reports")

# -- silence over every read session, FLOOR ---------------------------------------------------------------------------
noisy = [n for n in (noise(t, c) for t, _, c in READS) if n]
row("read silent", "%d/%d" % (len(noisy), len(READS)), "0/%d" % 12, "read sessions with ANY off-grammar line")
for n in noisy[:3]:
    print("    noise: %r" % n[:2])

t, how = session(["put w 0x8c001800, 0xdeadbeef"] + load32(0x8c001800, CODE))
row("ctrl zlive", printed(t, "r2"), 0xdeadbeef, "trailing RAM round trip: the apparatus lived")

npass = sum(1 for _, ok in rows if ok)
CONTROL_ROWS = ("ctrl live", "ctrl devsig sh4", "ctrl devsig maple", "ctrl zlive")
st = dict(rows)
control_ok = all(st.get(n, False) for n in CONTROL_ROWS)
print("")
print("SCORE %d/%d  label=%s" % (npass, len(rows), LABEL))
print("FAILING: " + ", ".join(n for n, ok in rows if not ok))
print("MAPLE_DMAADDR_RESULT=%d/%d" % (npass, len(rows)))
print("MAPLE_DMAADDR_CONTROL=%s" % ("OK" if control_ok else "FAIL"))
print("MAPLE_DMAADDR_PROBE_DONE")
sys.stdout.flush()
sys.exit(0 if control_ok and npass == len(rows) else 1)
