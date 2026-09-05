#!/usr/bin/env python3
"""wdcflood: six unlatched fatal() in dev_wdc.c, each guest-drivable without bound.

SITE NUMBERS IN THIS FILE ARE PRE-FIX LINE NUMBERS, USED AS STABLE NAMES.  The fix
adds ~97 lines, so every one of them resolves to the WRONG LINE in the shipped
file -- `:145` reads as DEVICE_TICK(wdc).  They are kept because the ledger, the
round block and all five kill tables name the sites this way, and renumbering
here would break that correspondence silently.

THE POST-FIX COLUMN IS DELIBERATELY NOT A NUMBER.  One was written here and went
stale ONE EDIT LATER -- a six-line comment added to dev_wdc.c in the same session
moved all six by four.  The durable key is the flag name, so that is what is
given; `grep -n 'd->FLAG = 1;' ../src/devices/dev_wdc.c` resolves it at any commit.

    pre     grep key                        site
    :145    d->warned_inbuf_overrun = 1;    wdc_addtoinbuf ring overrun
    :160    d->warned_inbuf_overread = 1;   wdc_get_inbuf over-read
    :583    d->warned_unimpl_cmd = 1;       unimplemented command
    :607    d->warned_nonbyte_write = 1;    non-8-bit access on WRITE
    :704    d->warned_data_unexpected = 1;  write to DATA when not expected
    :1025   d->warned_nonbyte_read = 1;     non-8-bit access on READ

The map was derived from the diff, not assumed: the two width messages are
byte-identical apart from WRITE!/READ!, so a truncated text search returns the
wrong site -- it did, on the first attempt.

WHAT THIS DETECTS, AND WHAT IT DOES NOT (floor clause (e), the CONTRACT).

  DESIGNED TO CATCH
    * removal of any of the six per-instance latch guards this round adds.  An
      earlier version of this line claimed "any of the six" while the contract
      below excluded `:145`, so it CONTRADICTED ITSELF and the file really covered
      FIVE unique sites.  Two file-reading seats caught it independently, and it
      was an L2 floor breach under clause (b), not a wording slip.  `:145` now has
      its own row (`overrun x2`), so the claim is true again -- and it is stated
      here as a thing a ROW MEASURES, not a thing believed;
    * a latch whose operand a guest can CLEAR between fires (`w16 reset`), and any
      latch with period N > 1 rather than 1 (`fire3`);
    * a latch reset on a NORMAL device operation (`interleave`) -- the class every
      back-to-back row is blind to by construction;
    * a latch whose repair is NULLED -- guard kept, flag never set (clause (d));
    * a latch made PER-DEVICE-LAST-VALUE rather than per-site, under which a guest
      alternating two stimuli floods forever ("last-warned-opcode");
    * a latch operand swapped for a GUEST-RESETTABLE field (d->seccnt and friends);
    * a guard that swallows a guest-visible side effect -- the ABRT status at :583
      and the -1 return at :160 -- which a line-count oracle alone cannot see.

  NOT CLAIMED
    * ring-buffer HEALTH.  `:145`/`:160` sit on a ring that uses head==tail for BOTH
      empty and full with no disambiguator, and whose two BULK paths never compare
      the pointers at all.  Filed as `wdcringambig`.  THE LATCH BOUNDS THE
      ANNOUNCEMENT; THE RING INVARIANT IS UNTOUCHED, and no row here says otherwise.
    * per-opcode uniqueness at `:583`.  The shipped spec is ONE line per device, not
      one per opcode.  An alternating-opcode observation is OUTSIDE this contract,
      not a floor breach.  (deepseek argued for a per-opcode set; FILED, not shipped.)
    * *** PER-INSTANCE STORAGE.  A PROCESS-GLOBAL `static` latch would pass every
      row here, because every row starts a FRESH emulator. ***  Measuring it needs
      ONE session driving TWO controller instances.  The landisk rig has one --
      but `dev_pcic.c:234-242` adds TWO wdc instances unconditionally (0x14000180
      and 0x140001f0), reached from every hpcmips subtype, so the FORK does have a
      rig for it and this is coverage debt rather than an impossibility.
      *** AN EARLIER VERSION OF THIS BULLET BUNDLED FLAG PAIRING IN WITH THAT AND
      WARRANTED BOTH ON "the rig does not have two instances".  THAT IS A
      NON-SEQUITUR, AND IT HID A MEASURABLE CLAIM BEHIND AN UNMEASURABLE ONE. ***
      Pairing survived for an entirely different reason: NO ROW FIRED TWO SITES IN
      ONE SESSION.  That is a property of the ROW SET, and `wr indep` below now
      fixes it in three lines.  The ring pair (:145/:160) is still unpinned --
      same shape, one more runloop, FILED.
    * A latch RESET ON A NORMAL OPERATION -- and the honest scope is NARROWER than an
      earlier version of this bullet claimed.  Pinned at :607/:1025 (`w16 reset`,
      `r16 reset`) for a reset arriving THROUGH `dev_wdc_access`.  At :583 pinned by
      `interleave` for **ONE valid opcode of nineteen** -- `interleave`'s only valid
      command is 0xEC, so a reset hidden in `WDCC_RECAL`, `SET_FEATURES`,
      `WDCC_DIAGNOSE` or any of the other cases is unpinned.  NOT pinned at all at
      :160, :704 or :145.  **AND NOT PINNED ANYWHERE for a reset arriving through the
      SIBLING HANDLER**: `dev_wdc_altstatus_access` shares the same `d`, and no row in
      this file touches its address -- which is where a real driver's reset goes.
      All three gaps FILED (`wdcflagindep`).
    * A LAST-VALUE latch keyed on the stimulus rather than on a boolean -- pinned at
      :583 (`unimpl 2op`, two opcodes) and at :607/:1025 (`w mixed`, `r mixed`, two
      WIDTHS).  **NOT pinned at :704**, where `datawr x2` writes an identical `len`
      and an identical `idata` twice, so keying that latch on either sweeps clean.
    * A latch OPERAND SWAPPED FOR A GUEST-RESETTABLE FIELD -- pinned at :607
      (`w16 reset`).  **NOT pinned anywhere else, and :583 is known reachable:**
      its guard reads `warned_unimpl_cmd` while its BODY reads `d->seccnt`, which
      a guest writes directly, so `if (!d->seccnt)` there scores a clean sweep.
      FILED.  *Both of these bullets were UNSCOPED in an earlier version -- listed
      under DESIGNED TO CATCH while each was measured at exactly one site of six.
      A capability claimed generally and measured once is the overclaim this
      contract exists to prevent.*
    * A `return` inserted after a latched `fatal()` at the four NON-width sites.
      The two width rows carry VALUE oracles that check BOTH fires, which is what
      that edit needs (it corrupts the FIRST access, not the second); the other
      four sites are count-only.
    * *** A CHANNEL DOWNGRADE. `fatal(` -> `debug(` at any site scores a CLEAN
      SWEEP HERE AND IS A REAL ESCAPE. ***  Every row single-steps (true until #486:
      `runloop` free-runs, and its docstring narrows this sentence), and `debug()`
      always prints under stepping (`core/debugmsg.c:375` early-outs on `v < 0`,
      which free-running at verbose 0 gives and stepping does not).  So a
      production guest would get SILENCE while every row stays green -- quietly
      reversing this round's own warrant for keeping `fatal()`.  Named by a
      file-reading seat.  **A step-based probe cannot see channel semantics at
      all**; the guard against it is a source-grep for `fatal(` at the six sites,
      in the gate rather than here.
    * That the ring is HEALTHY at the two ring sites -- see `wdcringambig`.  The
      `overrun x2` row's 1026 x 512 arithmetic WAS the BROKEN ring's exact-fit
      geometry.

      *** THIS BULLET SAID THE ROW WAS "marked for RE-PIN when that row lands",
      MEANING A FUTURE RING FIX.  THE RE-PIN TRIGGER FIRED ON THE WRONG ROUND. ***
      #484's ring repair changes how many overrun EVENTS occur, not the LATCHED
      count this row asserts, so it would not have moved the answer.  What killed
      the row was #479 -- an unconditional `wdc_new_command_reset()` in
      `wdc_command()`, capping per-command occupancy at 512 so the stimulus can no
      longer lap the ring at all.  MEASURED by a single-variable control that
      reverts only that reset: OVERRUN goes 0 -> 1.

      Re-aimed by #486 at the guest data port.  Two killers, different clauses, and
      naming only the ring repair would have repeated the wrong-cause shape one
      generation on.

CLAUSE (b) -- FAILS ON A VERBATIM REINSTATEMENT AT **EVERY** FIXED SITE -- BY TWO ROUTES,
AND THE PER-SITE MAPPING IS WRITTEN OUT HERE BECAUSE NOBODY HAD WRITTEN IT ANYWHERE.

  :160  overread x2   pre-fix HEAD (prefix_HEAD.raw)   reads 2, wants 1
  :583  unimpl x2     pre-fix HEAD                     reads 2, wants 1
  :607  w16 x2        pre-fix HEAD                     reads 2, wants 1
  :704  datawr x2     pre-fix HEAD                     reads 2, wants 1
  :1025 r16 x2        pre-fix HEAD                     reads 2, wants 1
  :145  overrun x2    mutant Mb2 (table2_22rows)       reads 2, wants 1

The first five need no mutant: **the pre-fix committed build IS the verbatim unlatched
form at those sites**, so the test-first run already is their reinstatement measurement.
`:145` needed `Mb2` because its row did not exist when the pre-fix run was taken -- and
that absence was an L2 FLOOR BREACH, found by a file-reading seat on pass 2 and closed
in-round. Until `overrun x2` existed, removing the `:145` guard scored a CLEAN SWEEP.

THE ORACLE IS "EXACTLY ONE, THEN ZERO", AND THE SECOND HALF IS THE POINT.

Every site row fires its site TWICE in one session and asserts the line count is
EXACTLY 1.  A one-off row is colourless: it prints one line before the fix and one
line after, so it cannot tell a working latch from no latch at all.  And a "<= 1"
oracle is worse than useless -- it passes a mutant that prints ZERO, i.e. a latch
that sets its flag BEFORE the test and never announces anything.  One, then zero, is
the pair a latch actually promises.

    pre-fix   2 lines  (RED)      post-fix  1 line  (green)
    nulled    2 lines  (RED)      set-first 0 lines (RED)

CONTROLS.  Two, because one is not enough -- a probe in this tree once returned 0x0
everywhere with its RAM control green:
    live    a known value round-trips through the same decode
    devsig  a value only the DEVICE can produce; RAM answers differently

Usage:  wdc_flood_probe.py [gxemul-binary] [kernel] [disk-image]
Prints WDC_FLOOD_RESULT=<correct>/<total> as its last line.
"""

import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1] if len(sys.argv) > 1 else "../../build/gxemul"
KERNEL = sys.argv[2] if len(sys.argv) > 2 else "../../_images/openbsd76-landisk-bsd.rd"
DISK = sys.argv[3] if len(sys.argv) > 3 else "../../_images/wdc-scratch-64m.img"

#  landisk: `wdc addr_mult=2 addr=0x14000000` (machine_landisk.c:87-89), and
#  dev_wdc.c:674 divides relative_addr by addr_mult -- so register N is at
#  0x14000000 + 2N.  P2 (0xb...) is the uncached window, which is what a device
#  access must use; a P1 address would be served from the cache.
WDC = 0xb4000000
WD_DATA = WDC + 0                  # reg 0
WD_SECCNT = WDC + 4                # reg 2 -- a NON-data register, for the len!=1 arms
WD_CMD = WDC + 14                  # reg 7: command on write, status on read
#  *** WD_CMD IS AT OFFSET 0x0e, SO A 32-BIT ACCESS IS UNALIGNED AND FAULTS. ***
#  Measured: `mov.l r8,@r7` to 0xb400000e produced ZERO device lines -- the SH4
#  alignment check (amask 3) raises an address error and the store never reaches
#  dev_wdc.c at all.  A row built on it is not a weak row, it is a row testing
#  nothing, and it read GREEN-on-a-count-of-zero in the pre-fix run that found it.
#  Byte access is what a real driver uses for the command register; 16-bit is also
#  legal here (0x0e is even), which is what the :1025 row relies on.

#  RAM is at 0x0c000000 on landisk (machine_landisk.c:84); 0x8c... is its P1 alias.
CODE = 0x8c001000
SCRATCH = 0x8c001800
LIVE = 0x5eed

NOP = 0x0009
BRA_SELF = 0xaffe
MOV_L_R8_AT_R7 = 0x2782            # mov.l r8,@r7
MOV_L_AT_R1_R2 = 0x6212            # mov.l @r1,r2
MOV_W_R8_AT_R7 = 0x2781            # mov.w r8,@r7
MOV_W_AT_R1_R2 = 0x6211            # mov.w @r1,r2
MOV_B_R8_AT_R7 = 0x2780            # mov.b r8,@r7
MOV_B_AT_R1_R2 = 0x6210            # mov.b @r1,r2
DT_R3 = 0x4310                     # dt r3   (0100nnnn00010000, n=3)


def BF_BACK(n):
    #  bf disp8: target == (bf_addr + 4) + disp*2.  The bf sits at word index n+1
    #  and the loop head at 0, so disp == -(n + 3).
    return 0x8b00 | ((-(n + 3)) & 0xff)

#  One pattern per SITE.  They must not overlap: a pattern that matches two sites
#  turns a per-site count into a device-wide count and every row silently changes
#  meaning.  Checked below by the `disjoint` row.
P_UNIMPL = re.compile(r"wdc: WARNING! Unimplemented command")
P_OVERREAD = re.compile(r"wdc: WARNING! someone is reading too much")
P_W8 = re.compile(r"wdc: WARNING! non-8-bit access on WRITE")
P_R8 = re.compile(r"wdc: WARNING! non-8-bit access on READ")
P_DATA = re.compile(r"wdc: write to DATA, but not")
P_OVERRUN = re.compile(r"wdc_addtoinbuf\(\): WARNING! wdc inbuf overrun")

rows = []


def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-14s %-12s %-12s %-40s %s" % (name, got, want, note,
                                          "ok" if ok else "FAIL"))
    return ok


def session(cmds, settle=8.0, spin=2.0, disk=True):
    argv = [BIN, "-V", "-x", "-E", "landisk", "-M", "64"]
    if disk and os.path.exists(DISK):
        #  `iR:` -- ALL prefix chars come before a SINGLE colon.  diskimage.c:1652
        #  takes `strchr(fname, ':')`, the FIRST colon, and the loop at :1654 runs
        #  `while (fname <= cp)` -- so in `i:R:path` only `i` is ever read as a
        #  prefix and `R:path` becomes the FILENAME.  (An earlier draft said `i:R:`
        #  hits the invalid-prefix arm at :1752; it does NOT -- it never reaches it.
        #  Same conclusion, wrong mechanism, and a wrong reason gets reused.)
        #  R: discards guest writes into a pid-unique overlay, so repeated runs
        #  cannot inherit state.
        argv += ["-d", "iR:" + DISK]
    argv.append(KERNEL)
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, argv)
        os._exit(127)
    buf = ""

    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.25)
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

    alive = rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            alive = False
            break
        if not rd(spin if i == len(cmds) - 1 else 0.35):
            alive = False
            break
    try:
        os.write(fd, b"quit\n")
        rd(0.6)
    except OSError:
        pass
    for fn in (lambda: os.close(fd), lambda: os.waitpid(pid, 0)):
        try:
            fn()
        except OSError:
            pass
    return buf, alive


def printed(t, reg):
    m = re.search(r"print\s+%s\s*\r?\n\s*(0x[0-9a-f]+)" % reg, t)
    return m.group(1) if m else "absent"


def printed_all(t, reg):
    """Every value the debugger echoed for `reg`, in order.

    *** THE ROWS BELOW NEED THIS BECAUSE A ONE-VALUE ORACLE CHECKED THE WRONG FIRE. ***
    The escape these value rows exist for -- a `return` inserted after a latched
    `fatal()` -- corrupts the FIRST access: the flag is not yet set, so the guard IS
    entered, and the inserted return skips the repair.  The SECOND access finds the
    flag set, skips the guard entirely, and repairs normally.  A row that reads the
    value once, after both fires, therefore sees a perfectly good value and passes.
    Checking BOTH fires is the whole point.
    """
    return re.findall(r"print\s+%s\s*\r?\n\s*(0x[0-9a-f]+)" % reg, t) or ["absent"]


def lowbyte(v):
    """Low 8 bits as hex, or the sentinel through.

    The width repair sets only `data[0]`, so the upper bytes of a wide read are
    unspecified; masking is what makes the oracle about the REPAIR rather than
    about whatever happened to be in the register's other half.
    """
    return v if not v.startswith("0x") else "0x%02x" % (int(v, 16) & 0xff)


def run(steps, at=CODE):
    put = ["put h 0x%x, 0x%04x" % (at + 2 * i, op) for i, op in enumerate(steps)]
    put += ["put h 0x%x, 0x%04x" % (at + 2 * len(steps), BRA_SELF),
            "put h 0x%x, 0x%04x" % (at + 2 * len(steps) + 2, NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(steps)]


def ld(reg):
    return ["r1=0x%x" % reg, "r2=0"]


def st(reg, val):
    return ["r7=0x%x" % reg, "r8=0x%08x" % val]


def runloop(body, count, at=CODE):
    """Emit `body` in a hardware loop of `count` iterations and FREE-RUN it.

        loop:  <body>
               dt   r3        decrement r3, T = (r3 == 0)
               bf   loop      disp from BF_BACK
        end:   bra  end       breakpoint here

    *** CONVERTED FROM `step N` TO breakpoint+continue BY #486, AND THE REASON IS NOT
    THE ONE YOU WOULD GUESS. ***  The old form stepped `len(ops) * count + 2`
    instructions.  At the counts this probe now needs that is ~394,000 steps -- but
    raw step count was never the obstacle.  `dev_wdc.c` sets `d->data_debug = 1` at
    attach, so EVERY data-port write calls `debug()`; `debug()` PRINTS under stepping
    (single-stepping raises its verbosity above the threshold) and returns silently
    when free-running at verbose 0.  MEASURED, full size:

        step  mov.w x131400   30.684 s   131400 debug lines   20,369,040 bytes of pty
        fast  mov.w x131400    0.005 s        0 debug lines

    So the stepped form WORKS and costs 30 s and 20 MB of pty traffic per row.  Say
    that rather than "394,200 steps is too slow", which is the wrong reason and a
    future reader would act on it.

    *** FREE-RUNNING IS ALSO A CAPABILITY GAIN, NOT ONLY A SPEED ONE. ***  Because
    `debug()` goes quiet at verbose 0, a `fatal(` -> `debug(` channel downgrade at a
    site this probe watches now REDS here.  Measured: that mutant is killed at all
    three counts.  A stepped row could not see it -- the contract said as much, and
    that sentence is narrowed by this change.

    NOT ADDED AS A VARIANT.  `runloop` has exactly ONE caller in the tree, so a
    `runloop_fast` beside it would leave a dead helper -- and this fork licenses
    additions by measured deltas or a transferred warrant, never by "it cannot hurt".

    *** THE `print r3` IS A COMPLETION CONTROL AND IS NOT OPTIONAL. ***  (STATED, NOT
    ENFORCED: no row parses the printed r3 -- filed as wdcfloodprobe, 2026-09-05.)  `session()`'s
    reader returns True on a plain timeout, so a `continue` that never reaches the
    breakpoint would leave the guest spinning in `bra .` with the process alive, and
    the row would score whatever happened to be in the buffer.  Pinning r3 to 0 is
    what makes "the loop ran" a measurement instead of an assumption.
    """
    ops = list(body) + [DT_R3, BF_BACK(len(body))]
    end = at + 2 * len(ops)
    put = ["r3=%d" % count]
    put += ["put h 0x%x, 0x%04x" % (at + 2 * i, op) for i, op in enumerate(ops)]
    put += ["put h 0x%x, 0x%04x" % (end, BRA_SELF),
            "put h 0x%x, 0x%04x" % (end + 2, NOP)]
    return put + ["breakpoint add 0x%x" % end, "pc=0x%x" % at, "continue",
                  "print r3"]


def n(pat, t, alive):
    return ("%d" % len(pat.findall(t))) if alive else "died"


#  ------------------------------------------------------------------ controls
t, alive = session(st(SCRATCH, LIVE) + ld(SCRATCH)
                   + run([MOV_L_R8_AT_R7, MOV_L_AT_R1_R2]) + ["print r2"])
row("live", printed(t, "r2") if alive else "died", "0x5eed",
    "a known value round-trips through the decode")

#  DEVICE SIGNATURE.  A byte read of the STATUS register returns a value the device
#  computes from its own state.  RAM at this address would answer 0x0, and an
#  unmapped address answers 0x0 too -- so a NON-ZERO status is the discriminator.
t, alive = session(ld(WD_CMD) + run([MOV_B_AT_R1_R2]) + ["print r2"])
STATUS = printed(t, "r2") if alive else "died"
row("devsig", "nonzero" if (STATUS not in ("died", "absent", "0x0")) else STATUS,
    "nonzero", "status reg answers from device state, not RAM")

#  ------------------------------------------------ the six sites, fired TWICE each
#
#  Each row's `want` is 1: ONE announcement, then silence.  On the committed
#  pre-fix build every one of these reads 2, which is the test-first red.

t, alive = session(st(WD_CMD, 0xaa)
                   + run([MOV_B_R8_AT_R7, MOV_B_R8_AT_R7]))
row("unimpl x2", n(P_UNIMPL, t, alive), "1",
    ":583 same unknown opcode twice -> ONE line")

#  THE PER-DEVICE SPEC, PINNED.  Two DIFFERENT unknown opcodes must still yield ONE
#  line.  This is the row that kills a "last-warned-opcode" latch, under which an
#  alternating guest floods forever -- and it simultaneously pins that the shipped
#  spec is per-device, so a later per-opcode change is a visible spec change and not
#  a silent one.
t, alive = session(st(WD_CMD, 0xaa) + run([MOV_B_R8_AT_R7])
                   + st(WD_CMD, 0x5a) + run([MOV_B_R8_AT_R7]))
row("unimpl 2op", n(P_UNIMPL, t, alive), "1",
    ":583 TWO different opcodes -> still ONE line")

#  THE GUEST-VISIBLE SIDE EFFECT, WHICH A LINE COUNT CANNOT SEE.  `d->error |=
#  WDCE_ABRT` must stay OUTSIDE the latch guard.  Nested inside it, the SECOND
#  unknown command produces neither a line nor an ABRT -- it silently SUCCEEDS.
#  wdc_command() re-clears d->error per command, so reading status after the second
#  command is the discriminator.  WDCE_ABRT is bit 2 (0x04) in the error register;
#  the status register's ERROR bit is 0x01.
t, alive = session(st(WD_CMD, 0xaa) + run([MOV_B_R8_AT_R7])
                   + st(WD_CMD, 0x5a) + run([MOV_B_R8_AT_R7])
                   + ld(WD_CMD) + run([MOV_B_AT_R1_R2]) + ["print r2"])
S2 = printed(t, "r2") if alive else "died"
row("abrt 2nd", "err" if (S2 not in ("died", "absent")
                          and (int(S2, 16) & 0x01)) else S2,
    "err", ":583 the SECOND command still reports ERROR")

t, alive = session(ld(WD_DATA)
                   + run([MOV_B_AT_R1_R2, MOV_B_AT_R1_R2]))
row("overread x2", n(P_OVERREAD, t, alive), "1",
    ":160 two empty-ring byte reads -> ONE line")

#  THE OTHER GUEST-VISIBLE SIDE EFFECT.  `return (uint64_t) -1;` must stay OUTSIDE
#  the guard at :160.  Nested inside it, the SECOND over-read falls through to
#  `d->inbuf_tail = (d->inbuf_tail + 1) % WDC_INBUF_SIZE` and CORRUPTS THE RING
#  POINTER -- a fix strictly worse than the flood it removes.  A byte read of an
#  empty ring must return 0xff.
t, alive = session(ld(WD_DATA)
                   + run([MOV_B_AT_R1_R2, MOV_B_AT_R1_R2]) + ["print r2"])
row("overread -1", printed(t, "r2") if alive else "died", "0xffffffff",
    ":160 the SECOND empty read still returns -1 (mov.b SIGN-EXTENDS)")

t, alive = session(st(WD_SECCNT, 0x1234)
                   + run([MOV_W_R8_AT_R7, MOV_W_R8_AT_R7]))
row("w16 x2", n(P_W8, t, alive), "1",
    ":607 two 16-bit non-DATA writes -> ONE line")

t, alive = session(ld(WD_CMD)
                   + run([MOV_W_AT_R1_R2, MOV_W_AT_R1_R2]))
row("r16 x2", n(P_R8, t, alive), "1",
    ":1025 two 16-bit non-DATA reads -> ONE line")

t, alive = session(st(WD_DATA, 0x1234)
                   + run([MOV_L_R8_AT_R7, MOV_L_R8_AT_R7]))
row("datawr x2", n(P_DATA, t, alive), "1",
    ":704 two unexpected DATA writes -> ONE line")

#  *** FIRE THREE TIMES, NOT TWO.  A TWO-FIRE ORACLE CANNOT SEE A PERIOD-2 LATCH. ***
#  A seat proposed `d->warned_X = !d->warned_X;` so that fires 1 and 3 announce while a
#  two-fire row stays green.  Reading says that particular edit cannot work -- the
#  assignment sits INSIDE the guard, so fire 2 never reaches it -- but the CLASS is real
#  and this row closes periods 2 and 3: three fires expose a latch that re-arms every 2nd or
#  3rd fire; a period-4 latch fires at 1 and 5 and shows ONE line (this comment said "any
#  period N > 1" until the 2026-09-05 retrospective review -- wdcfloodprobe).
t, alive = session(st(WD_CMD, 0xaa)
                   + run([MOV_B_R8_AT_R7, MOV_B_R8_AT_R7, MOV_B_R8_AT_R7]))
row("fire3", n(P_UNIMPL, t, alive), "1",
    ":583 THREE fires -> still ONE line (kills period-N)")

#  *** THE ROWS ABOVE FIRE BACK-TO-BACK, SO THEY ARE BLIND TO ANY EDIT THAT ONLY
#  CHANGES WHAT HAPPENS BETWEEN THE FIRES. ***  ONE line inside an existing valid
#  command's case -- `d->warned_unimpl_cmd = 0;` -- reuses the existing flag, guard and
#  branch, passes every back-to-back row, and lets a guest that alternates
#  probe/IDENTIFY/probe flood forever.  Named by a packet-fed seat reasoning about what
#  the rows do NOT do, which is the same shape as #463's distinctness blindness.
t, alive = session(st(WD_CMD, 0xaa) + run([MOV_B_R8_AT_R7])
                   + st(WD_CMD, 0xec) + run([MOV_B_R8_AT_R7])
                   + st(WD_CMD, 0xaa) + run([MOV_B_R8_AT_R7]))
row("interleave", n(P_UNIMPL, t, alive), "1",
    ":583 fire, VALID cmd, fire -> ONE line")

#  *** THE M6 ESCAPE, MEASURED 14/14 AGAINST THE 14-ROW DETECTOR. ***  A seat predicted
#  it and the kill table confirmed it: swap the latch operand for a GUEST-RESETTABLE
#  struct field -- `if (len != 1 && !d->seccnt) { d->seccnt = 1; fatal(...); }` -- and
#  every back-to-back row stays green, because nothing between the two fires ever puts
#  the operand back.  A guest that writes seccnt = 0 between wide writes gets unlimited
#  lines.  This row clears the operand BY AN ORDINARY GUEST WRITE between the fires.
t, alive = session(st(WD_SECCNT, 0x1234) + run([MOV_W_R8_AT_R7])
                   + st(WD_SECCNT, 0x0000) + run([MOV_B_R8_AT_R7])
                   + st(WD_SECCNT, 0x1234) + run([MOV_W_R8_AT_R7]))
row("w16 reset", n(P_W8, t, alive), "1",
    ":607 wide, CLEAR seccnt, wide -> ONE line")

#  *** SIX FLAGS, NOT FEWER -- AND THIS ROW MOVES THAT FROM A READING TO A MEASUREMENT. ***
#  The contract used to say flag independence was unmeasurable here because every row
#  starts a fresh emulator and the rig has one controller.  **That warrant explains the
#  PROCESS-GLOBAL case only.**  Pairing survives for a different reason entirely: NO ROW
#  FIRES TWO DIFFERENT SITES IN ONE SESSION -- a property of the ROW SET, not of the rig,
#  and therefore fixable in three lines.  (Checked across all 22 rows: `datawr x2` writes
#  wd_data so the width check is never reached;
#  both value rows seed and read 8-bit.
#
#  *** TWO CLAIMS IN THIS PARAGRAPH WERE MADE FALSE BY #486, IN THE SAME DIFF THAT
#  RE-AIMED THE ROW, AND BOTH ARE CORRECTED RATHER THAN LEFT TO BE FOUND. ***  It said
#  `overrun x2` "uses legal 8-bit writes" and that "Zero rows fire two sites".  The
#  re-aimed row writes SIXTEEN-bit to wd_data and fires BOTH `:704` and `:145` in one
#  session -- measured DATA=1 OVERRUN=1.
#
#  That is deliberate, not incidental: firing both sites is what kills the flag-pairing
#  mutant, and it is why that row's oracle carries a THIRD value asserting that no single
#  line is matched by both patterns.)
#
#  This fires :607 and :1025 in ONE session.  A paired flag lets the first fire silence
#  the second, giving "1,0".  Named by the compile-and-measure seat reading the final
#  diff -- the round's HEADLINE design decision, unmeasured until now.
t, alive = session(st(WD_SECCNT, 0x1234) + run([MOV_W_R8_AT_R7])
                   + ld(WD_SECCNT) + run([MOV_W_AT_R1_R2]))
row("wr indep", "%s,%s" % (n(P_W8, t, alive), n(P_R8, t, alive)), "1,1",
    ":607 and :1025 in ONE session -> ONE line EACH")

#  *** SIBLING PARITY, ONE LEVEL DOWN -- AND THIS PAIR IS WHAT THE ROUND'S ONE PERMITTED
#  ASK-AGAIN BOUGHT. ***  `:583` has a TWO-STIMULI row (`unimpl 2op`, two different
#  opcodes).  The width sites had none: `w16 x2` fires (2,2) and `w32 x2` fires (4,4), in
#  SEPARATE sessions.  So a LAST-WARNED-WIDTH latch --
#
#      if (len != 1 && d->warned_nonbyte_write != (int) len) {
#              d->warned_nonbyte_write = (int) len;
#
#  -- scored a CLEAN SWEEP on all 24 rows while a guest alternating mov.w / mov.l floods
#  at one host line per store, forever.  It is the SAME CLASS this round already declared
#  a defect at :583 (`warned_unimpl_cmd != cur_command`, killed by `unimpl 2op`),
#  transposed to a site where nothing could observe it.  The reset rows below do not help:
#  they interpose a `len == 1` access, which `len != 1` rejects before the flag operand is
#  ever consulted.
#
#  THE GENERAL QUESTION, worth more than the two rows: the contract already asks "do two
#  SITES share a session?" (`wr indep`).  Its DUAL was missing --
#      *** for each site, does any ONE session present two DIFFERENT stimuli that both
#          reach that site's guard? ***
#  :583 yes; :607, :1025, :704, :160 and :145 all repeated an identical stimulus.  That is
#  one grep of the row list, and it is why the whole last-value-latch family sat unpinned
#  at five sites of six.
t, alive = session(st(WD_SECCNT, 0x1234) + run([MOV_W_R8_AT_R7])
                   + st(WD_SECCNT, 0x12345678) + run([MOV_L_R8_AT_R7]))
row("w mixed", n(P_W8, t, alive), "1",
    ":607 a 16-bit THEN a 32-bit write -> ONE line")

t, alive = session(ld(WD_SECCNT) + run([MOV_W_AT_R1_R2])
                   + run([MOV_L_AT_R1_R2]))
row("r mixed", n(P_R8, t, alive), "1",
    ":1025 a 16-bit THEN a 32-bit read -> ONE line")

#  WD_SECCNT for both: WD_CMD sits at offset 0x0e and a 32-bit access there is unaligned
#  and faults -- see the trap recorded at the top of this file.

#  *** SIBLING PARITY: :607 HAS A CLEAR-BETWEEN ROW AND :1025 DID NOT -- BY ACCIDENT. ***
#  `w16 reset` happens to place a legal 8-bit write between its two wide writes, so it
#  covers a reset-on-normal-operation edit at :607.  Nothing covered the mirror at :1025:
#  `r16 x2`/`r32 x2` fire back-to-back, `r16 value` seeds with a WRITE and checks values
#  not counts, and `accept r8` is a separate session.  So
#  `d->warned_nonbyte_read = 0;` on a legal 8-bit read scored 22/22.
#  Same predicate, same message modulo WRITE/READ, added in the same hunk pair -- the
#  carrier's pre-table check calls that asymmetry "a row you owe or a sentence you owe".
t, alive = session(ld(WD_CMD) + run([MOV_W_AT_R1_R2])
                   + run([MOV_B_AT_R1_R2])
                   + run([MOV_W_AT_R1_R2]))
row("r16 reset", n(P_R8, t, alive), "1",
    ":1025 wide, LEGAL 8-bit read, wide -> ONE line")

#  WIDTH.  The two `x2` rows above probe 16-bit ONLY, so a guard narrowed from
#  `len != 1` to `len == 2` escaped them.  WD_SECCNT is at offset 4 and IS 4-byte
#  aligned, so a 32-bit access reaches the device instead of faulting.
t, alive = session(st(WD_SECCNT, 0x12345678)
                   + run([MOV_L_R8_AT_R7, MOV_L_R8_AT_R7]))
row("w32 x2", n(P_W8, t, alive), "1",
    ":607 two 32-bit non-DATA writes -> ONE line")

t, alive = session(ld(WD_SECCNT)
                   + run([MOV_L_AT_R1_R2, MOV_L_AT_R1_R2]))
row("r32 x2", n(P_R8, t, alive), "1",
    ":1025 two 32-bit non-DATA reads -> ONE line")

#  *** VALUE ORACLES AT THE TWO WIDTH SITES, CHECKING **BOTH** FIRES. ***  A count-only
#  row cannot see a `return` inserted after a latched `fatal()` -- and neither can a
#  value row that reads only ONCE, because that edit corrupts the FIRST access (flag
#  unset, guard entered, return skips the repair) while the SECOND finds the flag set,
#  skips the guard and repairs normally.
#
#  *** AN EARLIER VERSION OF `r16 value` WAS MEASURED VACUOUS AND IS REPLACED. ***  Its
#  oracle was `printed(...) != "absent"` against a wanted "read", so it passed whenever
#  the debugger echoed ANY hex value -- structurally incapable of failing while the
#  emulator lived, and green under every one of table 2's ten mutants.  (It did
#  not exist for table 1, which measured a 14-row detector; an earlier version of
#  this note said "both tables", which is false -- checked, 0 occurrences in
#  table1_14rows.  A vacuity claim is not improved by overstating its evidence.)
#  The `live` control
#  already covers session death, so it measured nothing at all.  This is the vacuity
#  floor's own shape (a row that cannot go red is not a row) caught pre-ship, L1.
#
#  Seed with a LEGAL 8-bit write so the register holds a known value, then fire twice
#  and check the low byte after EACH.  The mask is deliberate: the repair sets only
#  `data[0]`, so a wide read's upper byte is unspecified and asserting it would make the
#  row about the wrong thing.  `:1025` sits inside the common `ret:` tail, so
#  `data[0] = odata` must run on BOTH reads.
t, alive = session(st(WD_SECCNT, 0x37) + run([MOV_B_R8_AT_R7])
                   + ld(WD_SECCNT) + run([MOV_W_AT_R1_R2]) + ["print r2"]
                   + run([MOV_W_AT_R1_R2]) + ["print r2"])
_v = [lowbyte(x) for x in printed_all(t, "r2")]
row("r16 value", (",".join(_v[:2]) if alive else "died"), "0x37,0x37",
    ":1025 BOTH wide reads fill the buffer")

#  The write-width site's repair is `idata = data[0]`, a FOURTH guest-visible side
#  effect the round's own review list omitted.  Both wide writes must deliver their low
#  byte -- the first with the latch unset, the second with it set -- so this row writes
#  a DIFFERENT value each time and reads back after each.
t, alive = session(st(WD_SECCNT, 0x0041) + run([MOV_W_R8_AT_R7])
                   + ld(WD_SECCNT) + run([MOV_B_AT_R1_R2]) + ["print r2"]
                   + st(WD_SECCNT, 0x0042) + run([MOV_W_R8_AT_R7])
                   + ld(WD_SECCNT) + run([MOV_B_AT_R1_R2]) + ["print r2"])
_w = [lowbyte(x) for x in printed_all(t, "r2")]
row("w16 value", (",".join(_w[:2]) if alive else "died"), "0x41,0x42",
    ":607 BOTH wide writes land data[0]")

#  *** `:145`, AND IT CLOSES AN L2 FLOOR BREACH -- WHICH #486 FOUND RE-OPENED. ***
#
#  THE ROW WAS DEAD, AND NOT MERELY RED.  It used to drive 1026 undrained IDENTIFY
#  commands.  `#479` made `wdc_command()` call `wdc_new_command_reset()`
#  UNCONDITIONALLY, which zeroes both ring pointers, so occupancy after any command is
#  at most 512 and 1026 commands cannot lap a 262,656-byte ring.  MEASURED, by a
#  single-variable control that reverts ONLY that reset and keeps #484's ring:
#
#      shipped build            OVERRUN = 0
#      #479's reset reverted    OVERRUN = 1
#
#  *** AND IT WAS NON-DISCRIMINATING, WHICH IS WORSE THAN RED. ***  Measured on the
#  committed binary: the old stimulus reads OVERRUN = 0 on the shipped latch AND 0 on a
#  build with the latch DELETED.  Clause (b) was open at the ring producer with nothing
#  saying so.
#
#  RE-AIMED at the guest DATA PORT, which takes no `wdc_command()` and therefore no
#  reset -- the only surviving route that laps the ring.
#
#  *** THE COUNT IS 131400 AND IT SITS 72 STORES ABOVE A CLIFF.  DO NOT "TIDY" IT. ***
#  Post-#484 the producer refuses at head == 262,655, so push 262,656 is the first
#  refusal -- the SECOND push of store 131,328.  Measured, want == 1:
#
#      n            131328      131329      131400
#      shipped         1 ok        1 ok        1 ok
#      latch DELETED   1 VACUOUS   3 red     145 red
#
#  At the exact fill point the unlatched mutant is GREEN.  Shrinking 131400 to 131328
#  reads like tightening a hand-waved number to what the arithmetic says, makes the
#  comment MORE precise, and silently re-opens the L2 breach.  The margin is a
#  load-bearing product of this row.
#
#  ORACLE IS THREE VALUES, and the third is the anti-fake control.  The smallest way to
#  fake this row is to re-anchor P_OVERRUN onto the `:704` DATA text -- then every build
#  reads 1 and `disjoint` cannot catch it, because its own stimulus fires neither
#  pattern.  So this row counts BOTH sites and asserts that NO SINGLE LINE is matched by
#  both.  Asserting "1,1" alone does not close it; a P_OVERRUN aimed at the DATA line
#  still gives 1,1.
#
#  It fires `:704` and `:145` in ONE session, which additionally kills a flag-pairing
#  mutant (the `:704` site's guard and assignment switched to `warned_inbuf_overrun`):
#  measured DATA=1 OVERRUN=0 -> red, while the OLD row was blind to it either way.
#
#  `spin` is back to the default: free-running finishes in ~0.02 s, so the old 25 s wait
#  was dead weight in every battery run.
t, alive = session(st(WD_DATA, 0x1234) + runloop([MOV_W_R8_AT_R7], 131400),
                   settle=10.0)
_both = sum(1 for _l in t.splitlines()
            if P_DATA.search(_l) and P_OVERRUN.search(_l))
row("overrun x2",
    ("%s,%s,%d" % (n(P_DATA, t, alive), n(P_OVERRUN, t, alive), _both)
     if alive else "died"),
    "1,1,0",
    ":704 + :145 in one session, and NO line matched by both")


#  ------------------------------------------------------------ the accept side
#
#  *** THESE ARE LEGAL-PATH QUIET PINS.  THEY ARE **NOT** DE-ESCALATION ACCEPT ROWS,
#  AND AN EARLIER COMMENT HERE CLAIMED THEY WERE -- WRONG TWICE OVER. ***
#
#  Wrong clause: the de-escalation clause governs a fix that removes a HOST-FATAL
#  guard.  This fix removes none.  `fatal()` never exited -- measured, 100 stores and
#  100 lines with the process continuing -- so no predicate here ever gated death, and
#  nothing accepted before is refused now: every guest-visible side effect is
#  unconditional and the first occurrence still announces on a channel `-q` cannot
#  silence.  A latch that PRESERVES the announcement is the opposite of the clause's
#  silent-refusal hazard.
#
#  Wrong verb: these rows prove a legal access does not ANNOUNCE.  They do not prove
#  it is not REFUSED -- none of them reads a value back, so a silent refusal would
#  pass all three.  Calling them accept rows would convert three voluntary quiet pins
#  into obligation-carriers with no measured kill behind them, which is precisely the
#  vacuity the floor exists to refuse.
#
#  What they ARE worth: they are the only automation watching these lines at all,
#  since gate_hygiene carries no wdc patterns.  Kept as quiet pins, claimed as
#  nothing more.  Their staying green under CODE mutants is expected, not a defect.
#
#  *** BUT THEY ARE NOT UNFAILABLE, AND AN EARLIER VERSION OF THIS NOTE IMPLIED THEY
#  WERE. ***  All three redden against a NULL MEDIUM (0/22 on an absent binary and on
#  a real non-emulator), because `n()` returns "died" rather than "0" when the run
#  produced nothing.  A naive "expect 0 diagnostics" row would PASS against silence --
#  zero is exactly what silence produces.  That one line is what stops every
#  absence-shaped oracle in this file from being vacuous under clause (c), and it was
#  not written for that reason.
#
#  KNOWN GAP, FILED: an EXPECTED DATA write (`write_in_progress` set) has no quiet
#  pin, so dropping `!d->write_in_progress` from that predicate would warn-and-latch
#  on legal I/O with every row here still green.  Building it needs a WRITE-command
#  staging sequence this probe does not have.

t, alive = session(st(WD_CMD, 0xec) + run([MOV_B_R8_AT_R7]))
row("accept ec", n(P_UNIMPL, t, alive), "0",
    "0xEC IDENTIFY is implemented -- must say NOTHING")

t, alive = session(st(WD_SECCNT, 0x01) + run([MOV_B_R8_AT_R7]))
row("accept w8", n(P_W8, t, alive), "0",
    "an 8-bit non-DATA write is legal -- must say NOTHING")

t, alive = session(ld(WD_CMD) + run([MOV_B_AT_R1_R2]))
row("accept r8", n(P_R8, t, alive), "0",
    "an 8-bit status read is legal -- must say NOTHING")

#  ------------------------------------------------------------------ hygiene
#
#  A pattern that matches two sites turns every per-site count into a device-wide
#  count and silently changes what every row above means.  Cheap to check, and this
#  project has shipped an unanchored pattern that matched a row's own DESCRIPTION.
t, alive = session(st(WD_CMD, 0xaa) + run([MOV_B_R8_AT_R7]))
hits = sum(1 for p in (P_UNIMPL, P_OVERREAD, P_W8, P_R8, P_DATA, P_OVERRUN)
           if p.search(t))
row("disjoint", "%d" % hits, "1",
    "one stimulus matches exactly ONE site pattern")

ok = sum(1 for _, v in rows if v)
print()
print("WDC_FLOOD_RESULT=%d/%d" % (ok, len(rows)))
