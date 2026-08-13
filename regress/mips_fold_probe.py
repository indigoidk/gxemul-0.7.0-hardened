#!/usr/bin/env python3
r"""#388 phase-B instrument: the MIPS fold-witness counters, on real guest loops.

Each row seeds a tiny loop at the debugger of a FRESH emulator, sets ONE
breakpoint on a non-arming instruction (a lui; lui never sets
combination_check) placed after the measured sequence, free-runs to it, and
reads the counters back with tlbdump. Stepping is forbidden here: the
cpu_dyntrans.c:1888 combination gate skips single_step, so a step-driven row
would measure an emulator in which folds cannot install at all. A breakpoint
instead disables only translation READ-AHEAD (cpu_dyntrans.c:1938 requires
breakpoints.n == 0); the :1888 gate tests neither breakpoints.n nor the plain
delay_slot flag (only in_crosspage_delayslot) -- though it DOES test
single_step_breakpoint, which a breakpoint HIT sets transiently (#388 pass-2:
an ignore-count breakpoint form would set it on every ignored hit and silently
disable combining; these rows hit their anchor exactly once, at the end), so
combining stays live and
translation becomes lazy -- each instruction translates when first reached,
including the arming instruction inside pass 1's delay-slot dispatch.

That lazy order fixes the arithmetic: pass 1 runs the original sequence and
performs the install mid-pass (the arming instruction's translation rewrites
an EARLIER ic slot); passes 2..P dispatch the fold handler. Hence for a
P-pass loop, install=1 and fire=P-1 for the branch/lui/multi folds (their
handlers bump fire once per dispatch, after the delay-slot guard, taken or
untaken), while memset fires once per handler COMPLETION, not per pass.

Rows (P=5 passes; every expectation derived, not observed):
  bne_nop_3max   bne_samepage_nop, 3max R3000 MODE32 LE.  addiu t0,t0,1 /
                 bne t0,t1,loop / nop(0x00000000) / lui[bp].  t0=0,t1=5: the
                 bne executes 5x (4 taken + 1 final untaken).  Pass 1 = plain
                 bne_samepage; translating its delay-slot nop runs
                 COMBINE(nop), whose bne arm (4th of 5 in MODE32, 2nd of 3 in
                 MODE64 -- the beq arm is last) rewrites the bne slot
                 (install=1); executions 2..5 dispatch the fold -> fire=4.
  bne_nop_tm64   same loop on testmips 5KE 64-bit BE: install=1 fire=4.
  lui_ori_3max   lui t2 / ori t2,t2 / addiu t0,t0,1 / bne t0,t1,loop /
                 or t3,t3,t3 / lui[bp].  COMBINE(ori) fires at the ori's
                 translation (ic[-1]==instr(set)) and rewrites the LUI slot
                 (install=1); passes 2..5 dispatch lui_ori -> fire=4.  The
                 delay-slot filler is or t3,t3,t3 (rd!=0), NOT a nop: 'or'
                 sets no combination_check, so the bne stays un-folded and
                 the row witnesses lui_ori alone.
  mlw2_le_3max   lui t2,0xdead / lui t3,0xdead / lw t2,0(t0) / lw t3,4(t0) /
                 addiu t1,t1,1 / bne t1,t4,loop / or t5,t5,t5 / lui[bp].
                 COMBINE(lw)'s _2 arm at lw#2's translation (same handler,
                 same base ptr, dest#1 != base) rewrites the lw#1 slot
                 (install=1).  The data page is warm before execution -- the
                 seeding `put w` itself installs host_load AND host_store
                 (#388 pass-2 correction: pass 1's loads warm nothing that
                 put w has not already warmed) -- so the generated body's
                 single bail never triggers on passes 2..5 -> fire=4.
                 The in-loop POISONS (lui t2/t3,0xdead) make the value checks
                 load-bearing: every pass clobbers t2/t3 before the loads, so
                 the final values can only come from the LAST dispatch -- the
                 folded body -- never survive from pass 1's real loads (#388
                 pass-2: without them, a fold body that wrote nothing kept
                 pass 1's correct values and the value rows stayed green).
                 multi_lw_2_le (pmax LE), value rows on this row too.
  mlw2_be_tm64   same on testmips 5KE BE -> multi_lw_2_be, install=1 fire=4.
                 PLUS two value checks read via `print` (never dump on BE):
                 the final pass's loads went through the _be BODY, so
                 t2==0x0badcafe and t3==0xffffffffdeadbeef witness the BE32
                 byte-swap AND the (MODE_int_t)(int32_t) sign-extension.
  mlw2_be_tm32   same on testmips -C R3000 (MODE32 BE cell): install=1 fire=4.
  memset_3max    s: addiu t0,t0,4 / bne t1,t0,s / sw zr,-4(t0) / lui[bp],
                 t0=DATA (page-aligned), t1=DATA+0x100, single page.  Pass 1
                 runs the real triple; translating the delay-slot sw runs
                 COMBINE(sw)'s memset arm (addiu rX,rX,4; bne with rX and
                 target &addiu; sw zr,-4(rX)) which rewrites the ADDIU slot
                 (install=1), and the real sw warms host_store.  Pass 2
                 dispatches the fold: rX=DATA+4, rY-rX=0xfc, (rX&0xfff)+0xfc
                 <= 0x1000 -> ONE un-clamped completion -> fire=1, then
                 next_ic=&ic[3] leaves the loop; the branch never re-runs.
                 fire counts completions: (1,1), NOT passes-1.

Measurement facts (each placement is load-bearing):
* Code sits at page offset 0x20 (ic slot 8): COMBINE(nop) bails below
  n_back 8, COMBINE(sw)/(lw) below 4 -- every arming instruction here clears
  its gate.  The loop never stores to its own code page; data lives on the
  next page.  nops are encoded 0x00000000 ONLY: arming rides the SPECIAL_SLL
  decode path (cpu_mips_instr.c:4470), so an or-encoded pseudo-nop (rd==0)
  becomes instr(nop) yet never arms and the fold would silently not install.
  Fillers use or rd,rs,rt with rd!=0, which neither arms nor turns into nop.
* The breakpoint address is checked in the TO_BE_TRANSLATED head, and stops
  BEFORE the anchor executes ("The instruction has not yet executed"), so the
  anchor lui clobbers nothing and never arms.
* 3max is constructed exactly as the committed mips_fixedmode_probe.py does:
  -V -e 3max -M 64 <pmax kernel file>, driven at the debugger, never booted.
  testmips constructs from a 4-byte /tmp stub raw-loaded at kseg0 (the
  phase-A smoke pattern); file_raw.c parses the 0x-prefixed address with
  strtoull and sign-extends for MIPS.
* Debugger register names are the fixed ABI table from cpu_mips.h
  (zr,at,v0..ra) -- the settings tree registers ONLY those, so numeric rN
  forms do not resolve on MIPS; encodings below carry the numeric fields.
* `print <reg>` answers a BARE `0x%x` line with NO name echo (MEASURED on
  testmips during #388 phase B; the "<reg> = 0x%x" form is the ASSIGNMENT echo,
  not print's). Parsed as the ARM probes do: `(?m)^0x([0-9a-fA-F]+)\s*$` from
  the command's mark; values compared as integers.
* Counter parse is bound to ^cpu\\d+: MFOLD...; START must declare n=34, END
  must match the counted rows, and duplicate/unknown/malformed rows fail the
  parse (BAD).  An absent or unterminated block is DEAD, never zero.
* The task sheet's per-fold sanity "install >= fire" is unsatisfiable
  against its own arithmetic (a 5-pass loop is install=1 fire=4 by design);
  the invariant that IS true -- a handler can only be dispatched from a slot
  an install rewrote -- is checked instead: fire>0 with install==0 is BAD.
* Instruction words are helper-built AND asserted against pinned constants
  (four prior incidents of a wrong register field yielding an accidental 0).

Output: one line per check, %-24s name then values then ok/FAIL, then
MFOLDPROBE_CONTROL=OK|FAIL (liveness pin: every parsed block had START+END
and at least one row's target counters were nonzero), MFOLDPROBE_RESULT=n/t.
Usage: mips_fold_probe.py <gxemul-binary> <pmax-kernel> [row-name|all]
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
PMAX_KERNEL = sys.argv[2]
ONLY = sys.argv[3] if len(sys.argv) > 3 else "all"

PASSES = 5

#  Code at page offset 0x20 == ic slot 8 (n_back gates); data on the NEXT page.
CODE3MAX = 0xffffffff80020020
DATA3MAX = 0xffffffff80021000
CODETEST = 0xffffffff80100020
DATATEST = 0xffffffff80101000
STUBADDR = 0xffffffff80100000


def itype(op, rs, rt, imm):
    return (op << 26) | (rs << 21) | (rt << 16) | (imm & 0xffff)


def orsame(r):                       # or rN,rN,rN -- rd!=0: NOT a nop, arms nothing
    return (r << 21) | (r << 16) | (r << 11) | 0x25


ADDIU_T0_1 = itype(0x09, 8, 8, 1)          # addiu t0,t0,1
ADDIU_T0_4 = itype(0x09, 8, 8, 4)          # addiu t0,t0,4
ADDIU_T1_1 = itype(0x09, 9, 9, 1)          # addiu t1,t1,1
BNE_T0_T1_M2 = itype(0x05, 8, 9, -2)       # bne t0,t1,-2  (target: this-4)
BNE_T0_T1_M4 = itype(0x05, 8, 9, -4)       # bne t0,t1,-4  (target: this-12)
BNE_T1_T4_M4 = itype(0x05, 9, 12, -4)      # bne t1,t4,-4
BNE_T1_T0_M2 = itype(0x05, 9, 8, -2)       # bne t1,t0,-2  (memset: rY=t1 rX=t0)
LUI_T2 = itype(0x0f, 0, 10, 0x1234)        # lui t2,0x1234
ORI_T2 = itype(0x0d, 10, 10, 0x5678)       # ori t2,t2,0x5678
LW_T2_0_T0 = itype(0x23, 8, 10, 0)         # lw t2,0(t0)
LW_T3_4_T0 = itype(0x23, 8, 11, 4)         # lw t3,4(t0)
SW_ZR_M4_T0 = itype(0x2b, 8, 0, -4)        # sw zr,-4(t0)
NOP = 0x00000000
ANCHOR = itype(0x0f, 0, 15, 0)             # lui t7,0 -- the breakpoint anchor
#  #388 pass-2: in-loop poisons (lui is non-arming) so the value checks can
#  only be satisfied by the LAST dispatch's writes, and a longer backward
#  branch for the grown loop.
LUI_T2_P = itype(0x0f, 0, 10, 0xdead)      # lui t2,0xdead
LUI_T3_P = itype(0x0f, 0, 11, 0xdead)      # lui t3,0xdead
BNE_T1_T4_M6 = itype(0x05, 9, 12, -6)      # bne t1,t4,-6 (poisoned mlw2 loop)
#  #388 pass-2: the bail-detector row's base -- the kseg1 view of the test
#  machines' console device (DEV_CONS_ADDRESS 0x10000000). Device pages are
#  NEVER inserted into host_load, so the generated fold bails on EVERY
#  dispatch: (install, fire) == (1, 0). A fire bump hoisted above the bail
#  reads (1, 4) and reddens the row.
DEVBASE = 0xffffffffb0000000

#  A drifting helper otherwise tests a different instruction silently.
assert ADDIU_T0_1 == 0x25080001 and ADDIU_T0_4 == 0x25080004
assert ADDIU_T1_1 == 0x25290001
assert BNE_T0_T1_M2 == 0x1509fffe and BNE_T0_T1_M4 == 0x1509fffc
assert BNE_T1_T4_M4 == 0x152cfffc and BNE_T1_T0_M2 == 0x1528fffe
assert LUI_T2 == 0x3c0a1234 and ORI_T2 == 0x354a5678
assert LW_T2_0_T0 == 0x8d0a0000 and LW_T3_4_T0 == 0x8d0b0004
assert SW_ZR_M4_T0 == 0xad00fffc and ANCHOR == 0x3c0f0000
assert orsame(11) == 0x016b5825 and orsame(13) == 0x01ad6825
assert LUI_T2_P == 0x3c0adead and LUI_T3_P == 0x3c0bdead
assert BNE_T1_T4_M6 == 0x152cfffa

#  Name tables mirrored from cpu_mips.c (order irrelevant here; membership only).
FOLD_NAMES = frozenset((
    "multi_sw_2_le", "multi_sw_3_le", "multi_sw_4_le", "multi_sw_5_le",
    "multi_sw_2_be", "multi_sw_3_be", "multi_sw_4_be", "multi_sw_5_be",
    "multi_lw_2_le", "multi_lw_3_le", "multi_lw_4_le", "multi_lw_5_le",
    "multi_lw_2_be", "multi_lw_3_be", "multi_lw_4_be", "multi_lw_5_be",
    "memset_addiu_bne_sw", "netbsd_r3k_picache_do_inv", "linux_pmax_idle",
    "netbsd_pmax_idle", "strlen_lb_addiu_bne_nop", "bne_samepage_nop",
    "beq_samepage_nop", "xor_andi_sll", "andi_sll", "lui_ori", "multi_addu_3",
    "addiu_bne_samepage_addiu", "lui_addiu", "b_samepage_addiu",
    "beq_samepage_addiu", "bne_samepage_addiu", "jr_ra_addiu",
    "b_samepage_daddiu"))
N_FOLDS = 34
assert len(FOLD_NAMES) == N_FOLDS
CSITE_NAMES = frozenset(("sw", "lw", "r3k_cache_inv", "nop", "sll", "ori",
                         "addu", "addiu", "b_daddiu"))
IDLE_NAMES = frozenset(("linux", "netbsd"))

RE_START = re.compile(r"^cpu(\d+): MFOLD_START version=1 n=(\d+)$")
RE_ROW = re.compile(r"^cpu(\d+): MFOLD (\S+) install=(\d+) fire=(\d+)$")
RE_ARM = re.compile(r"^cpu(\d+): MFOLD_ARM (\S+) count=(\d+)$")
RE_IDLE = re.compile(r"^cpu(\d+): MFOLD_IDLE (\S+) entered=(\d+)$")
RE_END = re.compile(r"^cpu(\d+): MFOLD_END n=(\d+) nonzero=(\d+)$")
RE_ANY = re.compile(r"^cpu\d+: MFOLD")


def parse_mfold(text):
    """-> ("OK", cpu0 fold dict) | ("DEAD", None) | ("BAD", None).

    DEAD = no block, or START without END (emulator died / pre-#388 build);
    BAD = the block exists but lies (wrong n, unknown/duplicate/malformed
    row, counts that disagree, or fire without install)."""
    blocks = {}
    cur = None          # [cpu, folds, arms, idles, rowcount]
    for raw in text.splitlines():
        s = raw.strip("\r")
        if not RE_ANY.match(s):
            continue
        m = RE_START.match(s)
        if m:
            if cur is not None or int(m.group(1)) in blocks:
                return "BAD", None
            if int(m.group(2)) != N_FOLDS:
                return "BAD", None
            cur = [int(m.group(1)), {}, {}, {}, 0]
            continue
        m = RE_END.match(s)
        if m:
            if cur is None or int(m.group(1)) != cur[0]:
                return "BAD", None
            if int(m.group(2)) != cur[4] or int(m.group(3)) != len(cur[1]):
                return "BAD", None
            blocks[cur[0]] = cur[1]
            cur = None
            continue
        m = RE_ROW.match(s)
        if m:
            name = m.group(2)
            if cur is None or int(m.group(1)) != cur[0]:
                return "BAD", None
            if name not in FOLD_NAMES or name in cur[1]:
                return "BAD", None
            inst, fire = int(m.group(3)), int(m.group(4))
            if fire > 0 and inst == 0:
                #  A handler can only be dispatched from a slot an install
                #  rewrote; fire without install is a lying counter.  (The
                #  task sheet's "install >= fire" is the impossible
                #  direction: loops fire passes-1 times per single install.)
                return "BAD", None
            cur[1][name] = (inst, fire)
            cur[4] += 1
            continue
        m = RE_ARM.match(s)
        if m:
            if cur is None or int(m.group(1)) != cur[0]:
                return "BAD", None
            if m.group(2) not in CSITE_NAMES or m.group(2) in cur[2]:
                return "BAD", None
            cur[2][m.group(2)] = int(m.group(3))
            cur[4] += 1
            continue
        m = RE_IDLE.match(s)
        if m:
            if cur is None or int(m.group(1)) != cur[0]:
                return "BAD", None
            if m.group(2) not in IDLE_NAMES or m.group(2) in cur[3]:
                return "BAD", None
            cur[3][m.group(2)] = int(m.group(3))
            cur[4] += 1
            continue
        return "BAD", None      # ^cpuN: MFOLD... that fits no known shape
    if cur is not None:
        return "DEAD", None     # START without END
    if 0 not in blocks:
        return "DEAD", None     # counters absent entirely
    return "OK", blocks[0]


def run_row(machine_argv, first_wait, code, words, bp_off, puts, regs, reads):
    """One fresh emulator: seed, breakpoint, continue, tlbdump, reg prints."""
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V"] + machine_argv)
        os._exit(127)
    buf = ""

    def rd(t=0.4):
        nonlocal buf
        r, _, _ = select.select([fd], [], [], t)
        if fd not in r:
            return True
        try:
            d = os.read(fd, 65536)
        except OSError:
            return False
        if not d:
            return False
        buf += d.decode("latin1", "replace")
        return True

    def wait_from(mark, timeout=30):
        t = time.time()
        while time.time() - t < timeout:
            if not rd():
                return False
            if len(buf) > mark and buf[mark:].rstrip().endswith("GXemul>"):
                return True
        return False

    def send(sx, timeout=30):
        mark = len(buf)
        b = (sx + "\n").encode("latin1")
        n = 0
        while n < len(b):
            n += os.write(fd, b[n:])
        wait_from(mark, timeout)
        return mark

    def finish(status, folds=None, vals=None):
        try:
            os.write(fd, b"quit\n")
            time.sleep(0.3)
            os.kill(pid, 9)
            os.waitpid(pid, 0)
        except Exception:
            pass
        return status, folds, (vals if vals is not None else {})

    if not wait_from(0, first_wait):
        return finish("DEAD")

    for i, w in enumerate(words):
        send("put w 0x%x, 0x%08x" % (code + 4 * i, w))
    for a, w in puts:
        send("put w 0x%x, 0x%08x" % (a, w))
    for name, val in regs:
        send("%s=0x%x" % (name, val))
    send("breakpoint add 0x%x" % (code + bp_off))
    send("pc=0x%x" % code)

    mark = len(buf)
    b = b"continue\n"
    n = 0
    while n < len(b):
        n += os.write(fd, b[n:])
    if not wait_from(mark, 60):
        #  No breakpoint hit: drop to the debugger anyway so the counters
        #  (and the row's inevitable FAIL) are still diagnosable.
        os.write(fd, b"\x03")
        wait_from(len(buf), 15)

    mark = send("tlbdump", 45)
    status, folds = parse_mfold(buf[mark:])

    vals = {}
    for name in reads:
        got = None
        for _ in range(2):
            mark = send("print %s" % name)
            #  #388: `print <reg>` answers a BARE `0x%x` line, no name echo
            #  (MEASURED on testmips; the docstring's "name = 0x%x" form is the
            #  assignment echo, not print's). Match the bare-hex-line idiom the
            #  ARM probes use, anchored to this command's mark.
            m = re.search(r"(?m)^0x([0-9a-fA-F]+)\s*$", buf[mark:])
            if m:
                got = int(m.group(1), 16)
                break
            time.sleep(1.0)
            rd(1.0)
        vals[name] = got
    return finish(status, folds, vals)


def stub_path():
    p = "/tmp/gx_mfold_%d.bin" % os.getpid()
    with open(p, "wb") as f:
        f.write(b"\x00\x00\x00\x00")
    return p


#  Loop bodies (memory order; [bp] = breakpoint anchor, never executes):
W_BNE_NOP = [ADDIU_T0_1, BNE_T0_T1_M2, NOP, ANCHOR]
W_LUI_ORI = [LUI_T2, ORI_T2, ADDIU_T0_1, BNE_T0_T1_M4, orsame(11), ANCHOR]
W_MLW2 = [LUI_T2_P, LUI_T3_P, LW_T2_0_T0, LW_T3_4_T0, ADDIU_T1_1,
          BNE_T1_T4_M6, orsame(13), ANCHOR]
W_MEMSET = [ADDIU_T0_4, BNE_T1_T0_M2, SW_ZR_M4_T0, ANCHOR]

M3MAX = ["-e", "3max", "-M", "64", PMAX_KERNEL]     # the committed 3max form


def rows(stub):
    tm64 = ["-E", "testmips", "-M", "64", "0x%x:%s" % (STUBADDR, stub)]
    tm32 = ["-E", "testmips", "-C", "R3000", "-M", "64",
            "0x%x:%s" % (STUBADDR, stub)]
    lw_regs3 = [("t0", DATA3MAX), ("t1", 0), ("t4", PASSES)]
    lw_regst = [("t0", DATATEST), ("t1", 0), ("t4", PASSES)]
    lw_data3 = [(DATA3MAX, 0x0badcafe), (DATA3MAX + 4, 0xdeadbeef)]
    lw_datat = [(DATATEST, 0x0badcafe), (DATATEST + 4, 0xdeadbeef)]
    cnt_regs = [("t0", 0), ("t1", PASSES)]
    #  name, argv, 1st-prompt wait, code base, words, bp off, data puts,
    #  regs, fold, (want install, want fire), reg reads
    return [
        ("bne_nop_3max", M3MAX, 150, CODE3MAX, W_BNE_NOP, 0x0c, [],
         cnt_regs, "bne_samepage_nop", (1, PASSES - 1), []),
        ("bne_nop_tm64", tm64, 90, CODETEST, W_BNE_NOP, 0x0c, [],
         cnt_regs, "bne_samepage_nop", (1, PASSES - 1), []),
        ("lui_ori_3max", M3MAX, 150, CODE3MAX, W_LUI_ORI, 0x14, [],
         cnt_regs, "lui_ori", (1, PASSES - 1), []),
        ("mlw2_le_3max", M3MAX, 150, CODE3MAX, W_MLW2, 0x1c, lw_data3,
         lw_regs3, "multi_lw_2_le", (1, PASSES - 1), ["t2", "t3"]),
        ("mlw2_be_tm64", tm64, 90, CODETEST, W_MLW2, 0x1c, lw_datat,
         lw_regst, "multi_lw_2_be", (1, PASSES - 1), ["t2", "t3"]),
        ("mlw2_be_tm32", tm32, 90, CODETEST, W_MLW2, 0x1c, lw_datat,
         lw_regst, "multi_lw_2_be", (1, PASSES - 1), ["t2", "t3"]),
        #  #388 pass-2, the bail-detector: base = a DEVICE page (never enters
        #  host_load), so the generated body bails on EVERY dispatch. The one
        #  row whose fire expectation is 0 -- it is what notices a fire bump
        #  hoisted above the bail (which would read (1,4) here).
        ("mlw2_dev_tm64", tm64, 90, CODETEST, W_MLW2, 0x1c, [],
         [("t0", DEVBASE), ("t1", 0), ("t4", PASSES)],
         "multi_lw_2_be", (1, 0), []),
        #  memset: fire counts handler COMPLETIONS -- one un-clamped chunk.
        ("memset_3max", M3MAX, 150, CODE3MAX, W_MEMSET, 0x0c, [],
         [("t0", DATA3MAX), ("t1", DATA3MAX + 0x100)],
         "memset_addiu_bne_sw", (1, 1), []),
    ]


#  Register-value checks; the in-loop poisons make these witness the LAST
#  dispatch's writes. The 0x8000_0000-bit expectation is BUILD-dependent,
#  MEASURED (#388 pass-2): the 64-bit build prints the sign-extended register
#  (0xffffffffdeadbeef); the MODE32 builds print the 32-bit value
#  (0xdeadbeef). Both witness the (MODE_int_t)(int32_t) assembly equally.
VALS = {
    "mlw2_le_3max": [("mlw2v0_le_3max", "t2", 0x0badcafe),
                     ("mlw2v1_le_3max", "t3", 0xdeadbeef)],
    "mlw2_be_tm64": [("mlw2v0_be_tm64", "t2", 0x0badcafe),
                     ("mlw2v1_be_tm64", "t3", 0xffffffffdeadbeef)],
    "mlw2_be_tm32": [("mlw2v0_be_tm32", "t2", 0x0badcafe),
                     ("mlw2v1_be_tm32", "t3", 0xdeadbeef)],
}

_names = [r[0] for r in rows("x")] + [v[0] for vl in VALS.values() for v in vl]
for _a in _names:                    # the padded-column trap, statically dead
    assert len(_a) <= 22
    for _b in _names:
        assert _a == _b or not _b.startswith(_a)

stub = stub_path()
passed = total = 0
control_ok = True
any_nonzero = False
for (name, argv, fwait, code, words, bp, puts, regs, fold, want,
     reads) in rows(stub):
    if ONLY != "all" and ONLY != name:
        continue
    total += 1
    status, folds, vals = run_row(argv, fwait, code, words, bp, puts, regs,
                                  reads)
    if status != "OK":
        control_ok = False
        got_i = got_f = status         # DEAD or BAD, never zero
        ok = False
    else:
        got_i, got_f = folds.get(fold, (0, 0))
        if got_i or got_f:
            any_nonzero = True
        ok = (got_i, got_f) == want
    passed += ok
    print("%-24s install=%s/%d fire=%s/%d %s" % (
        name, got_i, want[0], got_f, want[1], "ok" if ok else "FAIL"))
    if name in VALS:
        for vname, reg_, vwant in VALS[name]:
            total += 1
            got = vals.get(reg_)
            vok = (got == vwant)
            passed += vok
            print("%-24s got=%s want=0x%x %s" % (
                vname, ("0x%x" % got) if got is not None else "None",
                vwant, "ok" if vok else "FAIL"))

if not any_nonzero:
    control_ok = False
print("MFOLDPROBE_CONTROL=%s" % ("OK" if control_ok else "FAIL"))
print("MFOLDPROBE_RESULT=%d/%d" % (passed, total))
