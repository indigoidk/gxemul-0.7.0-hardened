#!/usr/bin/env python3
#
#  sgi_re_width_witness.py -- RUNG-3 WITNESS FOR ACCESS-WIDTH HOST KILL (#dev_sgi_re.c)
#
#  Defect class: A guest choosing an access width ends the host emulator process.
#  Target site: src/devices/dev_sgi_re.c len != 8 guard at CRIME_RE_TLB_A (0x15001000).
#
#  Rung 3: Real MIPS instructions (sd, sw, sh, sb, lw) executed by CPU through
#  real address decode and real memory_rw on UNMODIFIED in-tree -E sgi -e ip32.
#
#  Sentinel: SGIRE_WIDTH_WITNESS_DONE

import os, pty, re, select, sys, time

if len(sys.argv) < 2:
    sys.stderr.write('usage: sgi_re_width_witness.py <gxemul>\n')
    sys.exit(2)

BIN = sys.argv[1]
DUMMY = '/tmp/sgi_dummy.bin'
open(DUMMY, 'wb').write(b'\x00\x00\x00\x00')

CODE = 0xffffffff80001000
RAM_SCRATCH = 0xffffffff80004000
SGI_RE_TLBA = 0xffffffffb5001000
SGI_DE_STATUS = 0xffffffffb5004000

LIVE_VAL = 0x12345678
DEVSIG_STATUS_VAL = 0x1e000000

rows = []

def row(name, got, want, note=''):
    ok = (got == want)
    rows.append((name, ok))
    print('%-14s %-12s %-12s %-46s %s' % (name, got, want, note, 'ok' if ok else 'FAIL'))
    return ok

def session(cmds, settle=0.5, spin=0.2):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, '-V', '-x', '-E', 'sgi', '-e', 'ip32', '0x80001000:' + DUMMY])
        os._exit(127)
    buf = ''
    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.05)
            if not r: continue
            try:
                d = os.read(fd, 65536)
                if not d: return False
                buf += d.decode('latin-1', 'replace')
            except OSError:
                return False
        return True

    alive = rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + '\n').encode('latin-1'))
        except OSError:
            alive = False
            break
        if not rd(spin if i == len(cmds) - 1 else 0.05):
            alive = False
            break
    try:
        os.write(fd, b'quit\n')
        rd(0.2)
    except OSError:
        pass

    how = 'nostatus'
    try:
        p, stat = os.waitpid(pid, os.WNOHANG)
        if p == 0:
            time.sleep(0.05)
            p, stat = os.waitpid(pid, os.WNOHANG)
        if p != 0:
            if os.WIFSIGNALED(stat):
                how = 'sig%d' % os.WTERMSIG(stat)
            elif os.WIFEXITED(stat):
                how = 'exit%d' % os.WEXITSTATUS(stat)
    except OSError:
        pass

    try:
        os.close(fd)
    except OSError:
        pass

    if how == 'nostatus':
        try:
            _, stat = os.waitpid(pid, 0)
            if os.WIFSIGNALED(stat):
                how = 'sig%d' % os.WTERMSIG(stat)
            elif os.WIFEXITED(stat):
                how = 'exit%d' % os.WEXITSTATUS(stat)
        except OSError:
            pass

    return buf, alive, how

def printed(t, reg):
    m = re.findall(r'print\s+%s\s*\r?\n\s*(0x[0-9a-fA-F]+)' % reg, t)
    return m[-1] if m else 'absent'

class Addr(object):
    def __init__(self, base):
        self.a = base
    def take(self, n_ops):
        got = self.a
        self.a += 4 * (n_ops + 2) + 0x20
        return got

def run(ops, at):
    put = ['put w 0x%x, 0x%08x' % (at + 4 * i, op) for i, op in enumerate(ops)]
    put += ['put w 0x%x, 0x10000000' % (at + 4 * len(ops)), # b .
            'put w 0x%x, 0x00000000' % (at + 4 * len(ops) + 4)] # nop
    return put + ['pc=0x%x' % at, 'step %d' % len(ops)]

# MIPS instructions:
def SW(rs, rt): return 0xac000000 | (rs << 21) | (rt << 16)
def SD(rs, rt): return 0xfc000000 | (rs << 21) | (rt << 16)
def SH(rs, rt): return 0xa4000000 | (rs << 21) | (rt << 16)
def SB(rs, rt): return 0xa0000000 | (rs << 21) | (rt << 16)
def LW(rs, rt): return 0x8c000000 | (rs << 21) | (rt << 16)

REG_V0 = 2 # v0
REG_V1 = 3 # v1
REG_A0 = 4 # a0

print('# WIDTH-KILL RUNG-3 WITNESS -- dev_sgi_re.c len!=8 guard')
print('binary: %s' % BIN)
print('')
print('%-14s %-12s %-12s %-46s %s' % ('row', 'got', 'want', 'note', ''))

# ------------------------------------------------------------------ MANDATORY CONTROLS
# LIVENESS control: store then load through RAM
A = Addr(CODE)
t, alive, how = session(['v0=0x%x' % RAM_SCRATCH, 'a0=0x%x' % LIVE_VAL, 'v1=0']
                        + run([SW(REG_V0, REG_A0), LW(REG_V0, REG_V1)], A.take(2))
                        + ['print v1'])
g = printed(t, 'v1')
row('live', g if alive else 'died', '0x%x' % LIVE_VAL,
    'LIVENESS: guest store then guest load, through RAM')

# DEVICE-SIGNATURE control: CRIME_DE_STATUS reads 0x1e000000 on fresh device; RAM reads 0
A = Addr(CODE)
t, alive, how = session(['v0=0x%x' % SGI_DE_STATUS, 'v1=0']
                        + run([LW(REG_V0, REG_V1)], A.take(1))
                        + ['print v1'])
g = printed(t, 'v1')
row('devsig st', g if alive else 'died', '0x%x' % DEVSIG_STATUS_VAL,
    'DEVSIG: fresh CRIME_DE_STATUS = 0x1e000000; RAM = 0')

print('SGIRE_CONTROL=%s' % ('OK' if all(o for _, o in rows) else 'DEAD'))
print('')

# ------------------------------------------------------------------ ACCEPT CONTROL
# Legal width: 8-byte write (sd) survives with exit0
A = Addr(CODE)
t, alive, how = session(['v0=0x%x' % SGI_RE_TLBA, 'a0=0x%x' % LIVE_VAL]
                        + run([SD(REG_V0, REG_A0)], A.take(1)))
row('width8 ok', how, 'exit0',
    'ACCEPT: legal 8-byte store (sd) survives')

# ------------------------------------------------------------------ WRONG-WIDTH KILLS
# 4-byte store (sw) -> fatal() -> exit(1)
A = Addr(CODE)
t, alive, how = session(['v0=0x%x' % SGI_RE_TLBA, 'a0=0x%x' % LIVE_VAL]
                        + run([SW(REG_V0, REG_A0)], A.take(1)))
row('width4 kill', how, 'exit1',
    'ONE 4-byte guest store (sw) -- host process ends')
row('width4 says', '1' if 'TODO: unimplemented len=4 for CRIME_RE_TLB_A' in t else '0', '1',
    'ATTRIBUTION: died with unimplemented len=4')

# 2-byte store (sh) -> fatal() -> exit(1)
A = Addr(CODE)
t, alive, how = session(['v0=0x%x' % SGI_RE_TLBA, 'a0=0x%x' % LIVE_VAL]
                        + run([SH(REG_V0, REG_A0)], A.take(1)))
row('width2 kill', how, 'exit1',
    'ONE 2-byte guest store (sh) -- host process ends')
row('width2 says', '1' if 'TODO: unimplemented len=2 for CRIME_RE_TLB_A' in t else '0', '1',
    'ATTRIBUTION: died with unimplemented len=2')

# 1-byte store (sb) -> fatal() -> exit(1)
A = Addr(CODE)
t, alive, how = session(['v0=0x%x' % SGI_RE_TLBA, 'a0=0x%x' % LIVE_VAL]
                        + run([SB(REG_V0, REG_A0)], A.take(1)))
row('width1 kill', how, 'exit1',
    'ONE 1-byte guest store (sb) -- host process ends')
row('width1 says', '1' if 'TODO: unimplemented len=1 for CRIME_RE_TLB_A' in t else '0', '1',
    'ATTRIBUTION: died with unimplemented len=1')

ok = sum(1 for _, o in rows if o)
print('')
print('SGIRE_WIDTH_WITNESS_RESULT=%d/%d' % (ok, len(rows)))
print('SGIRE_WIDTH_WITNESS_DONE')
