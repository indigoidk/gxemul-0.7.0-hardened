import io
p = 'arm_msrmode_probe.py'
s = io.open(p, newline='').read()
grid = io.open('grid_block.py', newline='').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)


rep('''row("row count", len(rows) + 1, 43,''', grid + '''row("row count", len(rows) + 1, 47,''')
rep('''for p in ("dpi", "pop")) + ",msr lbl,tbit,encl2,msr wide")''',
    '''for p in ("dpi", "pop")) + ",msr lbl,tbit,encl2,msr wide,grid msr,grid dpi,grid pop")''')
# session counter
rep('''def session(cmds, settle=1.6, spin=1.6):''', '''NSESS = [0]


def session(cmds, settle=1.6, spin=1.6):''')
rep('''    pid, fd = pty.fork()''', '''    NSESS[0] += 1
    pid, fd = pty.fork()''')
rep('''print("ARMMSRMODE_RESULT=%d/%d" % (n, len(rows)))''',
    '''print("ARMMSRMODE_RESULT=%d/%d" % (n, len(rows)))
print("ARMMSRMODE_SESSIONS=%d" % NSESS[0])''')
# stale inline src-row comment
i = s.index("#  through `ldmia r6!,{pc}^' over a table of block addresses.")
j = s.index("\n", s.index("= c00000c0|label", i))
s = s[:i] + '''#  through `ldmia r6!,{pc}^' over a table of block addresses.  Want R1 = R4 = ffffffdf and R2 = R3
#  = ffffffc0|label (mode kept, every other bit from the SPSR 0xffffffcf; `msr cpsr_fsx,#0' and the
#  label re-entry before each decline leave the old CPSR 0x0000000m), and EXACTLY ONE announce.''' + s[j:]

# ------------------------------------------------------------------ header
a0 = s.index("CLASS CLOSURE (repair 4)")
a1 = s.index("CONTRACT (floor clause (e))")
s = s[:a0] + '''THE GENERATED GRID (repair 5; owner ruling 2026-10-08).  The restore/MSR coverage is GENERATED
from tables (grid_obs(): labels, MODELLED, UNMODELLED, complementary value pairs), not written row
by row: `grid msr', `grid dpi', `grid pop' run every generated observation and compare the WHOLE
CPSR word; `grid cov' re-derives the coverage table from the same generator and reds on any gap.
  G1 every (path, outcome, bit 0..31, polarity) cell has an observation whose result bit must
     equal the SPSR / operand value while the OLD CPSR's bit differs (complementary pairs:
     OLD 0 / NEW all-ones-with-T, and OLD all-ones / NEW 0), so keep-old, force-0 and force-1 all
     change the word.  This is a UNION across observations, not a property of every decline.
     Named equivalents: bit 4 polarity 0 (every modelled mode and label has bit 4 set) and T
     polarity 0 against OLD T = 1 (the guest runs ARM code, so OLD T is always 0; keep-old T is
     caught at polarity 1).  The latch is SET for every decline after a session's first.
  G2 every msr_imm label (FIQ IRQ SVC ABT UND SYS) declines label ^ 0x1f, which differs in all
     five mode bits; the restore labels decline the same value as the SPSR.
  G3 all 25 unmodelled values are declined and all 7 modelled modes accepted on EACH path.
  G4 arm_pop's enclosing cells {S, non-S} x {PC, no PC}, all four, in grid pop.
  The hand-written rows below remain (G5): label x latch x outcome (src), tbit (T with the latch
  clear, by `print cpsr'), encl / encl2 (the DPI enclosing cells), msr wide, msr lbl.  Sessions:
  the probe prints ARMMSRMODE_SESSIONS.

''' + s[a1:]
rep('''  * the helper answering 1 always (kill 14/15/1e), admitting 0x1c-0x1e (kill 1e), dropping its
    `& ARM_FLAG_MODE' projection (src rows), or WIDENING it by ANY bit 31:5 (closure rule (1):
    src rows, tbit, msr wide, msr lbl);''',
    '''  * the helper answering 1 always (kill 14/15/1e), wrong on ANY of the 32 mode values on ANY path
    -- narrowed (e.g. `& 0x17' admits 0x18-0x1a), widened by any bit 31:5, or dropped (grid *:
    G3 drives all 25 unmodelled and all 7 modelled values through each path; src rows, tbit,
    msr wide);''')
rep('''  * the msr_imm decline clearing fewer than all five mode bits, at any label (`& ~0x0f': kill 03
    at SVC, encl2 at FIQ), or clearing MORE (`& ~0x3f', T lost: tbit); the restore keep-mode mask
    clearing fewer than bits 0-3 (src rows, per the bit/label table above);''',
    '''  * the msr_imm decline clearing fewer than all five mode bits at ANY label (grid msr: G2
    declines label ^ 0x1f at all six labels; kill 03, encl2), or clearing MORE (`& ~0x3f', T lost:
    tbit, grid msr); the restore keep-mode mask letting any SPSR mode bit through (grid dpi/pop:
    G2; src rows);''')
rep('''  * a decline taking ANY bit 31:5 from the old CPSR (or forcing it) instead of the SPSR / operand
    (closure rule (2): src rows R2/R3, tbit, msr wide) -- this replaces the repair-3 sentence
    "the declined SPSR has N Z I F SET while the CPSR it replaces has them CLEAR", which was FALSE
    for N and Z (the replaced CPSR then was c00000xx);''',
    '''  * a decline OR accept taking ANY bit 31:5 from the old CPSR, or forcing it to 0 or to 1,
    with the latch clear or set (grid *: G1 complementary pairs; src R2/R3; tbit; msr wide) --
    this replaces the repair-3 sentence "the declined SPSR has N Z I F SET while the CPSR it
    replaces has them CLEAR" (FALSE for N and Z) and repair 4's "at EVERY decline, every restored
    bit differs" (FALSE for T at src R2/R3 and msr wide: it held only as a UNION);''')
rep('''  * the enclosing predicates widened in ANY of their cells (see the closure paragraph): arm_pop's
    `if (return_flag)' (encl: non-S LDM with pc; encl2: S-LDM without pc),''',
    '''  * the enclosing predicates widened in ANY of their cells: arm_pop's `if (return_flag)' (grid
    pop: all four {S, non-S} x {PC, no PC}; also encl, encl2),''')
a0 = s.index("NOT CLAIMED, disclosed:")
a1 = s.index("NAMED-RED tally")
s = s[:a0] + '''NOT CLAIMED, disclosed: DPI opcode instances other than MOV and SUB (graded (e): the opcode
flows into nothing the repair reads).  The msr_imm comment's "only the LOCAL mask changes:
ic->arg[] is a cached translation" -- every grid observation re-executes the SAME translated
`msr cpsr_fsxc,r1' with a different r1, which pins the register form; the IMMEDIATE form's
re-execution is not rowed.  Per-CPU latch isolation (one CPU only); exception entry as a
Save-backstop route (no row); T-bit / execution-state coherence after a T-set restore beyond the
CPSR word itself; the USR/SYS `LDM {pc}^' and `MSR SPSR' paths that stop the CPU (filed
separately).  The grid, tbit and `print cpsr' readbacks are rung-3 debugger observations.  The
`msr wide' accept 0xffffffd1 sets operand bits 31:6, 4 and 0 only (bits 3:1 are clear: the grid's
accepts and c_17 / c_1b / c_1f carry them) -- repair 4's header said "bits 31:6, 4:0".

''' + s[a1:]
a0 = s.index("NAMED-RED tally")
a1 = s.index("Stay on `step', never `continue'")
s = s[:a0] + '''NAMED-RED tally: HEAD = 18/47, RED exactly the 29 rows kill 14, kill 15, save 2s, kill 1e,
kill 03, rst movs, rst ldm, zero spsr, dbg save, dbg both, latch ind, latch rpt, the ten src *
rows, msr lbl, tbit, encl2, msr wide, grid msr, grid dpi, grid pop, CONTROL=OK.  `encl' drives no
unmodelled mode and `grid cov' is static, so both are GREEN on HEAD.  `save 2s' on HEAD is the
SAME Load death as `kill 14' (EOF on the first MSR) -- it is not an independent HEAD reproduction
of Save; nor is `dbg both' a HEAD reproduction of Load (HEAD dies in Save first).  47/47 on HEAD
is a broken vehicle, not success.

''' + s[a1:]
rep('''dpi/src pop x {fiq irq abt und svc}, msr lbl, encl, tbit, encl2, msr wide, the `if=' (I/F) pin on''',
    '''dpi/src pop x {fiq irq abt und svc}, msr lbl, encl, tbit, encl2, msr wide, grid msr, grid dpi,
grid pop, grid cov, the `if=' (I/F) pin on''')
io.open(p, 'w', newline='').write(s)
print("EDITED")
