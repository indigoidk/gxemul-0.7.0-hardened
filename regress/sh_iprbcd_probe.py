#!/usr/bin/env python3
"""Witness for sh4iprbcd (IPRB/IPRC/IPRD never read) + sh4prioraise (no rescan).

Route: SCIF TXI (INTEVT 0x760) on landisk.  It is the ONE Table 19.6 source in
this tree that a device asserts SYNCHRONOUSLY inside a guest store --
dev_sh4.c:2535+, `case SH4_SCIF_BASE + SCIF_SSR:` writes scif_ssr and calls
scif_reassert_interrupts(), which INTERRUPT_ASSERTs scif_tx_irq when
SCSCR2.TIE && SCSSR2.(TDFE|TEND).  So the assert can be produced under `step`,
where debugger.c:800 has stopped the host timers.

Delivery itself must be observed FREE-RUNNING: cpu_dyntrans.c:204-206 refuses to
deliver interrupts while single-stepping.  Discriminator = a breakpoint at
VBR+0x600.  Delivered -> the vector is reached, the breakpoint stops the guest,
the debugger answers `print 0x1234`.  Refused -> the guest spins in `bra .`
forever and never returns to a prompt.

Rows are IMASK-BRACKETED in both directions on purpose.  cpu_dyntrans.c:247-249
delivers only when `IMASK < int_level`, so a pair of rows at IMASK=k pins the
level to a range rather than to "nonzero".  A single "did something deliver" row
is passed by any nonzero priority, which is exactly the escape this file exists
to close: PRE-FIX, SCIF sits at 3 unconditionally, from
`(intc_intpri08 >> 16) & 0xf` with intpri08 initialised to 0x33333333.
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
KERNEL = sys.argv[2]

LANDISK_CODE = 0x8c010000
SCRATCH = 0x8c010200
VBR = 0x8c020000
HANDLER = VBR + 0x600
LIVE = 0x12345678

SH4_IPRA = 0xffd00004
SH4_IPRC = 0xffd0000c
SH4_IPRD = 0xffd00010          # reset value 0xda74 -- the device signature
SCSCR2 = 0xffe80008            # TIE = 0x0080
SCSSR2 = 0xffe80010            # TDFE|TEND = 0x0060
#  MEASURED, not assumed: `mov.w @Rn,R0` SIGN-EXTENDS, so the 0xda74 the device
#  answers arrives in R0 as 0xffffda74.  Asymmetric under byte swap either way,
#  which is what the control needs.
IPRD_RESET = 0xffffda74

MOV_W_R2_AT_R1 = 0x2121
MOV_W_R4_AT_R3 = 0x2341
MOV_W_R6_AT_R5 = 0x2561
MOV_W_R8_AT_R7 = 0x2781
MOV_L_R0_AT_R1 = 0x2102
MOV_W_AT_R1_R0 = 0x6011        # mov.w @r1,r0  (sign-extending 16-bit load)
MOV_L_R0_AT_R2 = 0x2202
BRA_SELF = 0xaffe
NOP = 0x0009


def session(cmds, settle=8.0, spin=6.0, verify=True, machine="landisk"):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-E", machine, "-M", "64", KERNEL])
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
        if not rd(spin if i == len(cmds) - 1 else 0.9):
            alive = False
            break
    if alive and verify:
        mark = len(buf)
        try:
            os.write(fd, b"print 0x1234\n")
            rd(1.5)
            alive = "0x1234" in buf[mark:] or "4660" in buf[mark:]
        except OSError:
            alive = False
    try:
        os.write(fd, b"quit\n")
        time.sleep(0.2)
        os.kill(pid, 9)
        os.waitpid(pid, 0)
    except Exception:
        pass
    return buf, alive


def handler_stub():
    return ["put h 0x%x, 0x%04x" % (HANDLER, NOP),
            "put h 0x%x, 0x%04x" % (HANDLER + 2, BRA_SELF),
            "put h 0x%x, 0x%04x" % (HANDLER + 4, NOP)]


def scif_assert_code(iprc, at=LANDISK_CODE):
    """Three synchronous stores: IPRC, then SCSCR2.TIE, then SCSSR2.TDFE|TEND."""
    return (["r1=0x%x" % SH4_IPRC, "r2=0x%08x" % iprc,
             "r3=0x%x" % SCSCR2, "r4=0x00000080",
             "r5=0x%x" % SCSSR2, "r6=0x00000060",
             "put h 0x%x, 0x%04x" % (at, MOV_W_R2_AT_R1),
             "put h 0x%x, 0x%04x" % (at + 2, MOV_W_R4_AT_R3),
             "put h 0x%x, 0x%04x" % (at + 4, MOV_W_R6_AT_R5),
             "put h 0x%x, 0x%04x" % (at + 6, BRA_SELF),
             "put h 0x%x, 0x%04x" % (at + 8, NOP),
             "pc=0x%x" % at, "step 3"])


def run_deliver(iprc, imask, extra_after=None):
    """Assert SCIF TX with IPRC=<iprc>, then free-run at SR.IMASK=<imask>."""
    c = handler_stub() + scif_assert_code(iprc)
    if extra_after:
        c += extra_after
    c += ["sr=0x%08x" % (0x40000000 | (imask << 4)),
          "vbr=0x%x" % VBR,
          "breakpoint add 0x%x" % HANDLER,
          "continue"]
    _, alive = session(c)
    return "delivered" if alive else "refused"


def raise_iprc(new, at=LANDISK_CODE + 0x40):
    """A SECOND, LATER guest store to IPRC -- after the line is already asserted."""
    return ["r7=0x%x" % SH4_IPRC, "r8=0x%08x" % new,
            "put h 0x%x, 0x%04x" % (at, MOV_W_R8_AT_R7),
            "put h 0x%x, 0x%04x" % (at + 2, BRA_SELF),
            "put h 0x%x, 0x%04x" % (at + 4, NOP),
            "pc=0x%x" % at, "step 1",
            "pc=0x%x" % (LANDISK_CODE + 6)]     # park back in the bra . self-loop


def prewrite_iprc(v, at=LANDISK_CODE + 0x60):
    """A guest store to IPRC BEFORE the asserting sequence runs."""
    return ["r7=0x%x" % SH4_IPRC, "r8=0x%08x" % v,
            "put h 0x%x, 0x%04x" % (at, MOV_W_R8_AT_R7),
            "put h 0x%x, 0x%04x" % (at + 2, BRA_SELF),
            "put h 0x%x, 0x%04x" % (at + 4, NOP),
            "pc=0x%x" % at, "step 1"]


def deassert_scif(at=LANDISK_CODE + 0x80):
    """Clear SCSSR2 -- scif_reassert_interrupts() then INTERRUPT_DEASSERTs."""
    return ["r7=0x%x" % SCSSR2, "r8=0x00000000",
            "put h 0x%x, 0x%04x" % (at, MOV_W_R8_AT_R7),
            "put h 0x%x, 0x%04x" % (at + 2, BRA_SELF),
            "put h 0x%x, 0x%04x" % (at + 4, NOP),
            "pc=0x%x" % at, "step 1",
            "pc=0x%x" % (LANDISK_CODE + 6)]


def run_deliver2(pre, iprc, imask, extra_after=None):
    """Same as run_deliver but with an optional IPRC store BEFORE the assert."""
    c = handler_stub() + (prewrite_iprc(pre) if pre is not None else [])
    c += scif_assert_code(iprc)
    if extra_after:
        c += extra_after
    c += ["sr=0x%08x" % (0x40000000 | (imask << 4)),
          "vbr=0x%x" % VBR,
          "breakpoint add 0x%x" % HANDLER,
          "continue"]
    _, alive = session(c)
    return "delivered" if alive else "refused"


rows = []


def row(name, got, want, note=""):
    """*** THE VERDICT MUST BE THE LAST FIELD ON THE LINE. ***

    Measured, not assumed: an earlier draft of this file printed the note AFTER
    `ok`/`FAIL`, and `gate_sh_rounding.sh`'s established idiom is
    `grep -E " ok$| FAIL$"` plus `count "$LOG" "^$v  .*ok$"`.  Against the
    note-last format BOTH match ZERO lines, so every row would have been reported
    as absent while the probe itself printed a correct 6/10 and 10/10.  A gate
    that greps nothing scores the same as a gate whose rows all pass.
    """
    ok = (got == want)
    rows.append((name, ok))
    print("%-14s %-12s %-12s %-34s %s" % (name, got, want, note,
                                          "ok" if ok else "FAIL"))


def dumped(transcript, alive):
    if not alive:
        return "died"
    m = re.search(r"0x0*[0-9a-f]+\s+([0-9a-f]{8})", transcript.split("dump")[-1])
    if not m:
        return "nodump"
    return "0x%08x" % int.from_bytes(bytes.fromhex(m.group(1)), "little")


#  ---- control ---------------------------------------------------------------
_, ctl_alive = session([], spin=1.0)
print("IPRBCD_CONTROL=%s" % ("OK" if ctl_alive else "DEAD"))
if not ctl_alive:
    print("IPRBCD_RESULT=0/0")
    sys.exit(0)

#  ---- R1: LIVENESS control (a known value through the same decode) -----------
t, a = session(["r0=0x%08x" % LIVE, "r1=0x%x" % SCRATCH,
                "put w 0x%x, 0xdeadbeef" % SCRATCH,
                "put h 0x%x, 0x%04x" % (LANDISK_CODE, MOV_L_R0_AT_R1),
                "pc=0x%x" % LANDISK_CODE, "step 1",
                "dump 0x%x 0x%x" % (SCRATCH, SCRATCH + 4)], spin=1.5)
row("live", dumped(t, a), "0x%08x" % LIVE, "RAM through a guest store")

#  ---- R2: DEVICE-SIGNATURE control ------------------------------------------
#  A guest 16-bit load of IPRD returns cpu_sh.c's reset value 0xda74, which RAM
#  at that address could not produce and which only the INTC case in dev_sh4.c
#  can answer.  This proves the P4 INTC decode path -- the very path the rows
#  below drive -- is live, independently of any interrupt being delivered.
t, a = session(["r1=0x%x" % SH4_IPRD, "r2=0x%x" % SCRATCH,
                "put w 0x%x, 0xdeadbeef" % SCRATCH,
                "put h 0x%x, 0x%04x" % (LANDISK_CODE, MOV_W_AT_R1_R0),
                "put h 0x%x, 0x%04x" % (LANDISK_CODE + 2, MOV_L_R0_AT_R2),
                "pc=0x%x" % LANDISK_CODE, "step 2",
                "dump 0x%x 0x%x" % (SCRATCH, SCRATCH + 4)], spin=1.5)
row("devsig", dumped(t, a), "0x%08x" % IPRD_RESET, "IPRD reset value via P4")

#  ---- THE NAIVE WITNESS, kept as a row so its weakness is visible ------------
#  "Write one IPR and expect delivery."  Question 4 of the brief.  Recorded here
#  so the kill matrix shows, in one column, every mutant it lets through.
row("naive", run_deliver(0x00f0, 0), "delivered", "ONE IPR write, IMASK=0")

#  ---- sh4iprbcd: SCIF's priority must come from IPRC[7:4] --------------------
#  HI: IPRC says 15, IMASK 3.  Pre-fix SCIF is 3 -> 3 < 3 is false -> refused.
row("iprc_hi", run_deliver(0x00f0, 3), "delivered", "IPRC[7:4]=15, IMASK=3")
#  LO: IPRC says 1, IMASK 1.  Pre-fix SCIF is 3 -> 1 < 3 -> delivered.
row("iprc_lo", run_deliver(0x0010, 1), "refused", "IPRC[7:4]=1, IMASK=1")
#  A third point, so the pair cannot be satisfied by a constant that happens to
#  bracket: IPRC says 1, IMASK 0 -> level 1 is admitted, so it MUST deliver.
row("iprc_lo1", run_deliver(0x0010, 0), "delivered", "IPRC[7:4]=1, IMASK=0")

#  ---- sh4prioraise: a raised priority must deliver a STANDING request --------
#  IPRC=0 at assert time, so post-fix the line is masked and int_to_assert is
#  never set (cpu_sh.c:350 `if (prio == 0) return;`).  A LATER store raises it.
row("raise", run_deliver(0x0000, 3, raise_iprc(0x00f0)), "delivered",
    "assert masked, then IPRC[7:4]:=15")
#  The companion: the rescan must use the NEW value, not merely fire.
row("raise_lo", run_deliver(0x0000, 3, raise_iprc(0x0010)), "refused",
    "assert masked, then IPRC[7:4]:=1, IMASK=3")

#  ---- the nibble must be CLEARED, not merely OR-ed -------------------------
#  A priority that only ever RISES passes every row above, because IPRC resets to
#  0x0000 so within one session `|=` and `=` agree.  This row writes 15 first and
#  1 second: an OR-only update leaves 15 and delivers at IMASK=1.
row("lower", run_deliver2(0x00f0, 0x0010, 1), "refused",
    "IPRC[7:4]:=15 then :=1, IMASK=1")

#  ---- the rescan must ZERO int_to_assert/int_level before scanning -----------
#  Dropping those two zeroings passes every raise row (the scan can only climb),
#  but breaks DEASSERT: the stale winner survives and a cleared source is still
#  delivered.  Assert, then clear SCSSR2 (dev_sh4.c:2528-2535 deasserts), then
#  free-run at IMASK=0 -- nothing may be delivered.
row("deassert", run_deliver(0x00f0, 0, deassert_scif()), "refused",
    "assert at 15 then clear SCSSR2, IMASK=0")

#  ---- the two rows NO BEHAVIOURAL TEST CAN REPLACE ---------------------------
#  *** MEASURED: dropping the IPRB/IPRC blocks, and dropping the three RTC lines,
#  each score a CLEAN 10/10 against every row above. ***  Not because those rows
#  are weak -- because WDT, REF, SCI, GPIO, DMAC, H-UDI and RTC have no
#  INTERRUPT_ASSERT anywhere in this tree.  Nothing a guest can DO depends on
#  their priorities, so no behavioural row can ever tell the difference.
#
#  #458 exposes int_prio_and_pending[] through the settings interface precisely
#  so a row can ask what a source's priority WOULD be, without needing anything
#  to raise it.  These two rows are the reason that exposure exists; without them
#  it is an unused convenience, and with them the escape class is closed.
SH4_IPRB = 0xffd00008


def write_ipr_then_read(reg, value, slot, at=LANDISK_CODE + 0xa0, slots=None):
    """One guest store to an IPR, then read the resulting priority nibble(s).

    `slots` reads several in ONE session, which is how the IPRD pair below
    shares a boot: the row and its control must see the SAME store.
    """
    return (["r7=0x%x" % reg, "r8=0x%08x" % value,
             "put h 0x%x, 0x%04x" % (at, MOV_W_R8_AT_R7),
             "put h 0x%x, 0x%04x" % (at + 2, BRA_SELF),
             "put h 0x%x, 0x%04x" % (at + 4, NOP),
             "pc=0x%x" % at, "step 1"]
            + ["print iprio_%x" % x for x in (slots or (slot,))])


def prio_of(t, slot):
    m = re.search(r"print\s+iprio_%x\s*\r?\n\s*0x([0-9a-f]+)" % slot, t)
    return ("0x%x" % (int(m.group(1), 16) & 0xf)) if m else "absent"


#  WDT lives in IPRB[15:12].  Nothing asserts it, so this is unobservable any
#  other way -- and it is the sole killer of the drop-the-IPRB/IPRC mutant.
t_b, alive_b = session(write_ipr_then_read(SH4_IPRB, 0xa000, 0x560), spin=1.0)
row("iprb wdt", prio_of(t_b, 0x560) if alive_b else "died", "0xa",
    "IPRB[15:12]=10 -> WDT slot 0x560")

#  RTC lives in IPRA[3:0] -- a nibble of a register the function ALREADY read,
#  and the sole killer of the drop-the-RTC-lines mutant.
t_a, alive_a = session(write_ipr_then_read(SH4_IPRA, 0x000c, 0x480), spin=1.0)
row("ipra rtc", prio_of(t_a, 0x480) if alive_a else "died", "0xc",
    "IPRA[3:0]=12 -> RTC ATI slot 0x480")

#  *** THE ROW THAT DEFENDS THE ROUND'S CENTRAL DECISION. ***
#
#  #458 declines to read IPRD, and a pass-2 seat pointed out that the decision
#  lived ONLY IN A COMMENT: it predicted that `m_iprdread` -- the obvious "read
#  all four registers per Table 19.6" completion -- escapes every other row here
#  while masking four PCIC lines on landisk.  MEASURED and confirmed: with this
#  pair present `m_iprdread` scores 13/14, red on `iprd hold` alone.
#
#  The kill is cheap because the settings channel is already paid for.  IPRD's
#  four nibbles alias IRL0-3 = 0x240/0x2a0/0x300/0x360, which are ALSO
#  IRQ2/5/8/11 (sh4_exception.h:137-140 vs :144-154), owned by the hardwired
#  15..1 ramp.  So a guest `IPRD := 0` -- the exact store OpenBSD/landisk 7.6
#  makes at boot -- must leave slot 0x240 at 0xd.
#
#  `iprd ctl` is the discriminator, not decoration: IRQ10 (the wdc) is NOT one
#  of IPRD's four slots, so it stays 0x5 under both the fix and the mutant.  A
#  red `iprd hold` with a green `iprd ctl` says IPRD specifically, rather than
#  "the session broke".
t_d, alive_d = session(
    write_ipr_then_read(SH4_IPRD, 0x0000, 0x240, slots=(0x240, 0x340)),
    spin=1.0)
row("iprd hold", prio_of(t_d, 0x240) if alive_d else "died", "0xd",
    "IPRD:=0 must NOT move IRQ2/IRL0 slot 0x240")
row("iprd ctl", prio_of(t_d, 0x340) if alive_d else "died", "0x5",
    "control: IRQ10/wdc is outside IPRD, unmoved")

#  *** THE ONE ESCAPE THAT WAS NOT COVERAGE DEBT. ***
#
#  A pass-2 measuring seat built `m_sciftxonly` -- narrow the IPRC SCIF loop to
#  `for (i = SH4_INTEVT_SCIF_TXI; i <= SH4_INTEVT_SCIF_TXI; ...)`, one identifier
#  -- and MEASURED it at 14/14.  Every other escape found this round reaches a
#  slot nothing in the tree asserts; this one does not.
#
#  SCIF RXI (0x720) IS LIVE.  dev_sh4.c:250-256 asserts scif_rx_irq whenever
#  SCSCR2.RIE && SCSSR2.DR, connected at :1912.  That is CONSOLE INPUT on
#  landisk, the only SH machine this project boots.  Measured on both builds at
#  IPRC=0x00f0, SCSCR2=0x40, SCSSR2=0x01, IMASK=3:
#
#      fix            iprio_720 = 0x1f (asserted, prio 15)   RX delivered
#      m_sciftxonly   iprio_720 = 0x10 (asserted, prio  0)   RX refused
#
#  So the mutant silently deletes console input and the detector stays green.
#  The ten behavioural rows all drive TXI (0x760) -- scif_assert_code() writes
#  SCSCR2.TIE + SCSSR2.TDFE|TEND, the TX arm -- so nothing touched the RX side.
#
#  These four rows pin the WHOLE membership of the loop in one session, which
#  kills every narrowing of it rather than just the measured one.  This is the
#  de-escalation clause's own shape: the round was pinning the accept side of a
#  four-member loop at exactly one member.
t_c, alive_c = session(
    write_ipr_then_read(SH4_IPRC, 0x00f0, 0x700,
                        slots=(0x700, 0x720, 0x740, 0x760)),
    spin=1.0)
for _slot, _nm in ((0x700, "eri"), (0x720, "rxi"), (0x740, "bri"), (0x760, "txi")):
    row("scif %s" % _nm, prio_of(t_c, _slot) if alive_c else "died", "0xf",
        "IPRC[7:4]=15 -> SCIF slot 0x%x" % _slot)

n = sum(1 for _, ok in rows if ok)
print("IPRBCD_RESULT=%d/%d" % (n, len(rows)))
print("IPRBCD_VECTOR=" + ",".join(("1" if ok else "0") for _, ok in rows))
