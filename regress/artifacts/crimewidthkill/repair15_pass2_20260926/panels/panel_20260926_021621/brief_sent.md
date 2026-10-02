# #529 crimewidthkill -- REPAIR 15, PASS 2 (closing pass on the repair diff; the floor question on the composite)

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`** (the uncommitted #529 working set) **and the
frozen probe `GXEMUL-SEC/regress/artifacts/crimewidthkill/table14_20260926/crime_width_probe.table14.py`.**
There are THREE pristine-2021-upstream copies of GXemul under the project root (`./src/` and two
under `_archive/audit-results-*/builds/`).  They are NOT this fork.  If your line numbers disagree
with mine by hundreds you are reading one of them -- say so rather than reconciling.

**If you cannot read files that is expected** -- every fact you need is inlined below.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim -- an index range, an offset, a count of
reachable addresses -- ENUMERATE it rather than reasoning about it.**  Walk the values.
A derivation that skips one masking line reads exactly like a correct one.

**And ENUMERATE THE RIGHT DOMAIN -- a domain is itself a premise.**  Ask what the PRODUCER of
these values can actually emit before you walk them.

**VERDICT LINE FIRST**, so your answer survives truncation.  Then one line per question below,
then your reasons.  Language: this is ordinary bounds-and-error-handling review of an emulator's
device model; "declined" means an access the model refuses and answers with 0.

## 1. STATUS -- WHAT HAS AND HAS NOT SHIPPED (checked when this brief was written)

* **#529 is NOT committed.**  HEAD is `f4f601c4` (#548).  #529's working set is uncommitted and
  will not commit before #549 does, nor before the GPT-6 Astra adjudicator confirms.
* The working probe `regress/crime_width_probe.py` is still the 204-row `a0af7c92`.  Repair 15 exists
  ONLY as the frozen 218-row copy under review (`f5e915f6`), built by a script from `a0af7c92`.
* The gate pin in `regress/gate_arm.sh` still reads 204; moving it to 218 is OWED after this pass,
  citing table 14's base leg.

**WHAT #529 IS.**  One guest `lb/lbu/lh/lhu/sb/sh` anywhere in the SGI O2's CRIME register window used
to END THE PROCESS.  #529 declines the narrow width instead: announced once per device (a latched
`fatal()`, which prints and returns), a read answered 0 through the common tail, a write dropped --
and the register switch SKIPPED, because falling through it would let a declined halfword stop every
CPU (CONTROL), redirect the PC (REV), reassert the interrupt line (INTSTAT/INTMASK) or advance the
clock (TIME).  The detector is a 204-row probe, reviewed across fourteen repairs.

## 2. WHY REPAIR 15 EXISTS

The flagship adjudicator's first-hand re-ruling (2026-09-25) set the floor for the
DECLINE-SUPPRESSION class -- a `goto crime_declined` that is skipped for one label once the width latch
is already SET -- as **{observable skipped label} x {latch SET}**.  Table 12 had measured the class:

    M3_timelatch  (TIME exempted once the latch is set)   204/204  -- NOTHING SAW IT
    M5_revlatch   (REV  exempted once the latch is set)   204/204  -- NOTHING SAW IT
    M4_timeplain  (TIME exempted in EITHER latch state)   200/204  killed by the `time' rows
    M6_istlatch   (INTSTAT exempted once the latch set)   201/204  killed by the `istat' rows

and table 13a measured the two labels that were only DERIVED covered:

    M7_intmasklatch  201/204  killed (imask sb/lh/sh)      M8_ctllatch  201/204  killed (sb08 msg, sh08b run, gate run)

M3/M5 escaped because every session that refused at TIME or REV did so as that session's FIRST
refusal (latch CLEAR), and the one session that refuses there with the latch SET (`latch x5`) does it
from ordinary code (REV's redirect needs the PROM window) with no TIME sample afterwards.  **Repair 15
adds, per label, sessions whose FIRST refusal is at +0x07 (sets the latch) and whose SECOND is at the
label**, all four narrow ops each, reading the arm's own side effect.  It also adds the pair the
adjudicator's repair-14 ruling made conditional for ACCEPTS entries 13/17 (CONTROL's DOG_ENABLE-only
writes) -- see section 6.

## 3. PREMISES ALREADY SETTLED, RE-INLINED SO NOBODY SPENDS AN ANSWER RE-DERIVING THEM

Each was RE-READ in this scope while this brief was written (citations are to the working tree):

* **`fatal()` prints and returns; it never ends the process.**  `src/core/debugmsg.c`, the whole body:
  `va_list argp; va_start(argp, fmt); va_debug(argp, fmt); va_end(argp);`
* **Every probe session is a FRESH emulator** (`session()` below: `pty.fork()` + `os.execv(BIN, [...
  "-E", "sgi", "-e", "ip32" ...])`), so the width latch starts CLEAR in every session.  Adding a
  session cannot change another session's rows.
* **Exactly ONE CRIME tick per probe session, at its first step.**  `src/machines/machine.c`: a tick
  function starts with `ticks_till_next[n] = 0` and `ticks_reset_value[n] = 1 << tickshift`; each pass
  of the loop does `ticks_till_next[te] -= single_step ? 1 : N_SAFE_DYNTRANS_LIMIT;` and fires while
  `<= 0`.  CRIME registers with `CRIME_TICKSHIFT` = 14, so the next tick is 16384 single steps away,
  and a probe session steps a few dozen instructions.
* **The CRIME access function, verbatim** (`src/devices/dev_sgi_ip32.c`, md5 8c1d1545):

```c
DEVICE_ACCESS(crime)
{
	/*
	 *  The CRIME is memory mapped as 0x80 bytes, starting at
	 *  physical 0x14000000.
	 *
	 *  On my real O2:
	 *
	 *  0x14000080..0x140000ff is the same as 0x14000000..0x1400007f.
	 *  0x14000100..0x1400017f is the same as 0x14000000..0x1400007f.
	 *  0x14000180..0x140001ff is the same as 0x14000000..0x1400007f.
	 *
	 *  (I assume that real code will never access the above "mirrors",
	 *  but it would be trivial to add redirection so that such code
	 *  would work too.)
	 *
	 *  Memory control then starts at 0x14000200.
	 */
	struct crime_data *d = (struct crime_data *) extra;
	uint64_t idata = 0, odata = 0;
	uint64_t preserved_CRIME_HARDINT = d->reg[CRIME_HARDINT / sizeof(uint64_t)];
	size_t i;

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len);

	/*
	 *  Set crime version/revision:
	 *
	 *  This might not be the most elegant or correct solution, but it
	 *  seems that the IP32 PROM likes 0x11 for machines without graphics,
	 *  and 0xa1 for machines with graphics.
	 *
	 *  NetBSD 2.0 complains about "unknown" crime for 0x11, but I guess
	 *  that's something one has to live with.  (TODO?)
	 */
	d->reg[CRIME_REV / sizeof(uint64_t)] = d->use_fb? 0xa1 : 0x11;

	d->reg[CRIME_CONTROL / sizeof(uint64_t)] = CRIME_CONTROL_ENDIANESS;

	d->reg[CRIME_INTSTAT / sizeof(uint64_t)] =
		(d->reg[CRIME_SOFTINT / sizeof(uint64_t)] |
		d->reg[CRIME_HARDINT / sizeof(uint64_t)]);

	/*
	 *  Amount of memory.  Bit 8 of bank control set ==> 128MB instead
	 *  of 32MB per bank (?)
	 *
	 *  According to OpenBSD, "Empty banks are reported as duplicates of
	 *  bank #0."
	 */
	if (cpu->machine->physical_ram_in_mb > 1024) {
		fatal("[ sgi_crime: SGI O2 can not have more than 1024 MB RAM ]\n");
		exit(1);
	}

	int mb_per_bank;
	if (cpu->machine->physical_ram_in_mb <= 256)
		mb_per_bank = 32;
	else
		mb_per_bank = 128;

	if (cpu->machine->physical_ram_in_mb % mb_per_bank) {
		fatal("[ sgi_crime: for up to 256 MB RAM, RAM size needs to be divisible "
			"by 32 MB. for larger RAM sizes (up to 1024 MB), it needs to be "
			"divisible by 128 MB. ]\n");
		exit(1);
	}

	int flag_for_128MB = mb_per_bank == 128 ? 0x100 : 0x000;
	size_t total_mb = 0;
	for (int bank = 0; bank < 8; ++bank) {
		int b = mb_per_bank == 128 ? (bank << 2) : bank;
		if (total_mb >= cpu->machine->physical_ram_in_mb)
			d->reg[CRIME_MEM_BANK_CTRL0 / sizeof(uint64_t) + bank] =
				d->reg[CRIME_MEM_BANK_CTRL0 / sizeof(uint64_t) + 0];
		else
			d->reg[CRIME_MEM_BANK_CTRL0 / sizeof(uint64_t) + bank] = flag_for_128MB | b;

		total_mb += mb_per_bank;
	}
	
	if (len == 8) {
		if (writeflag == MEM_WRITE)
			d->reg[relative_addr / 8] = idata;
		else
			odata = d->reg[relative_addr / 8];
	} else if (len == 4) {
		if (writeflag == MEM_WRITE) {
			if (relative_addr & 4) {
				d->reg[relative_addr / 8] &= ~0xffffffffULL;
				d->reg[relative_addr / 8] |= (uint32_t)idata;
			} else {
				d->reg[relative_addr / 8] &= 0xffffffffULL;
				d->reg[relative_addr / 8] |= (uint64_t)(idata << 32ULL);
			}
		} else {
			odata = d->reg[relative_addr / 8];
			if (relative_addr & 4)
				odata = (int32_t)odata;
			else
				odata = (int32_t)(odata >> 32);
		}
	} else {
		/*
		 *  #529: THIS USED TO END THE PROCESS.  One guest lb, lbu, lh,
		 *  lhu, sb or sh anywhere in CRIME did it (witnessed at rung 3
		 *  on an unmodified -E sgi -e ip32, 6/6).  The width is now
		 *  DECLINED and announced once, the #498 sgi_de shape: a read
		 *  is answered 0 through the common tail, a write is dropped.
		 *
		 *  The goto skips the register switch below, and that is the
		 *  point of it: falling through would let a halfword 0x0800
		 *  written at CRIME_CONTROL stop every CPU, a narrow access to
		 *  CRIME_REV from the PROM probe loop redirect the PC, one at
		 *  INTSTAT or INTMASK reassert the interrupt line, and one at
		 *  CRIME_TIME advance the clock -- all measured.  It is not
		 *  `return 0' either: that raises a guest bus error
		 *  (EXCEPTION_DBE, cpus/memory_rw.c), and what real CRIME does
		 *  on a narrow cycle is not documented here.
		 */
		if (!(d->warned & CRIME_W_LEN)) {
			d->warned |= CRIME_W_LEN;
			fatal("[ crime: unimplemented len=%i at 0x%x -- declined."
			    "  (once) ]\n", (int) len, (int) relative_addr);
		}
		goto crime_declined;
	}

	switch (relative_addr) {

	case CRIME_REV:		/*  0x000  */
		/*
		 *  A contender for winning a prize for the worst hack
		 *  in history:  the IP32 PROM probes the CPU caches during
		 *  bootup, but they are not really emulated, so it fails.
		 *  During the probe, the CRIME_REV is read a lot. By
		 *  "returning" from the probe function, i.e. jumping to ra,
		 *  when this register is read the second time, the probe
		 *  can be skipped, and the PROM thus runs further.
		 *
		 *  The address where this happens is:
		 *	0xbfc0517c	PROM v2.3
		 *	0xbfc051ac	PROM v4.13
		 *
		 *  4.18 works too.
		 *
		 *  By extrapolating a bit (allowing for variations for other
		 *  versions of the PROM), let's return if the read of the
		 *  CRIME_REV register occurs anywhere near 0xbfc051XX.
		 */
		if (((uint32_t)cpu->pc & 0xffffff00) == (uint32_t)0xbfc05100) {
			cpu->pc = cpu->cd.mips.gpr[MIPS_GPR_RA];
			if (cpu->is_32bit)
				mips32_pc_to_pointers(cpu);
			else
				mips_pc_to_pointers(cpu);
		}
		break;

	case CRIME_CONTROL:	/*  0x008  */
		/*  TODO: 64-bit write to CRIME_CONTROL, but some things
		    (such as NetBSD 1.6.2) write to 0x00c!  */
		if (writeflag == MEM_WRITE) {
			/*
			 *  0x200 = watchdog timer (according to NetBSD)
			 *  0x800 = "reboot" used by the IP32 PROM
			 */
			if (idata & CRIME_CONTROL_DOG_ENABLE) {
				idata &= ~CRIME_CONTROL_DOG_ENABLE;
			}
			if (idata & CRIME_CONTROL_HARD_RESET) {
				int j;

				/*  This is used by the IP32 PROM's
				    "reboot" command:  */
				for (j=0; j<cpu->machine->ncpus; j++)
					cpu->machine->cpus[j]->running = 0;

				idata &= ~CRIME_CONTROL_HARD_RESET;
			}

			idata &= ~CRIME_CONTROL_ENDIANESS;

			if (idata != 0)
				fatal("[ CRIME_CONTROL: unimplemented "
				    "control 0x%016llx ]\n", (long long)idata);
		}
		break;

	case CRIME_INTSTAT:	/*  0x010, Current interrupt status  */
	case CRIME_INTMASK:	/*  0x018, Current interrupt mask  */
		crime_interrupt_reassert(d);
		break;

	case CRIME_DOG:		/*  0x030  */
		// No warning.
		break;

	case CRIME_TIME:	/*  0x038  */
		crime_update_crime_time(d);
		break;

	default:
		if (writeflag==MEM_READ) {
			debug("[ crime: read from 0x%x, len=%i:",
			    (int)relative_addr, len);
			for (i=0; i<len; i++)
				debug(" %02x", data[i]);
			debug(" ]\n");
		} else {
			debug("[ crime: write to 0x%x:", (int)relative_addr);
			for (i=0; i<len; i++)
				debug(" %02x", data[i]);
			debug(" (len=%i) ]\n", len);
		}
	}

 crime_declined:
	/*  #529: a declined access jumps here, skipping the register switch,
	    and is still answered.  */
	d->reg[CRIME_HARDINT / sizeof(uint64_t)] = preserved_CRIME_HARDINT;
	d->reg[CRIME_INTSTAT / sizeof(uint64_t)] =
		(d->reg[CRIME_SOFTINT / sizeof(uint64_t)] |
		d->reg[CRIME_HARDINT / sizeof(uint64_t)]);

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}
```

* **The TIME update and the tick, verbatim:**

```c
void crime_update_crime_time(struct crime_data* d)
{
	struct timeval tv;
	
	gettimeofday(&tv, NULL);

	uint64_t microseconds = tv.tv_sec * 1000000 + tv.tv_usec;
	if (d->last_microseconds == 0)
		d->last_microseconds = microseconds;

	int64_t delta = microseconds - d->last_microseconds;

	if (delta < 0) {
		fatal("[ crime_update_crime_time: host system time went backwards? ]\n");
		d->last_microseconds = microseconds;
		delta = 0;
	}

	// The delta to add is 66 per microsecond.
	int64_t to_add = delta * 66;

	if (to_add >= 1) {
		// NetBSD says CRIME_TIME_MASK = 0x0000ffffffffffffULL
		// but my O2 seems to use only the lower 32 bits as an
		// _unsigned_ value. (TODO: Double-check this again.)
		d->reg[CRIME_TIME / sizeof(uint64_t)] =
			(uint32_t)(d->reg[CRIME_TIME / sizeof(uint64_t)] + to_add);

		d->last_microseconds = microseconds;
	}
}


/*
 *  dev_crime_tick():
 *
 *  Updates CRIME_TIME (at 66 MHz) and reassert CRIME interrupts.
 */
DEVICE_TICK(crime)
{
	struct crime_data *d = (struct crime_data *) extra;

	crime_update_crime_time(d);
	crime_interrupt_reassert(d);
}
```

## 4. THE PROBE'S HELPERS, VERBATIM (from the frozen table-14 probe)

```python
CODE = 0x80001000
SCRATCH_RAM = 0xa0001800
LIVE_VAL = 0x12345678
CRIME = 0xb4000000
SENT = 0xdeadbeef
RA = 0x80004000
PROBE_PC = 0xbfc05180           # inside the CRIME_REV hack's window, (pc & 0xffffff00) == 0xbfc05100

def session(cmds, settle=1.5, spin=1.2):
    """one emulator, read to the pty's EOF after `quit'.  Returns (text, clean): clean = EOF reached AND exit 0."""
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "sgi", "-e", "ip32", "-M", "64", "0x80001000:" + DUMMY])
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
            except OSError:
                return False
            if not d:
                return False
            buf += d.decode("latin-1", "replace")
        return True

    rd(settle)
    for i, c in enumerate(cmds):
        try:
            if c == "<RUN>":        # free-run: `continue', let the guest run, then break back in with CTRL-C
                os.write(fd, b"continue\n")
                ok = rd(2.0)
                os.write(fd, b"\x03")
                ok = ok and rd(1.5)
            else:
                os.write(fd, (c + "\n").encode("latin-1"))
                ok = rd(spin if i == len(cmds) - 1 else 0.25)
        except OSError:
            break
        if not ok:
            break
    eof = True                      # a process already gone before `quit' has closed the pty; its status says how
    try:
        os.write(fd, b"quit\n")
        eof = not rd(10.0)          # to EOF, so anything printed on the way out is in the transcript
    except OSError:
        pass
    if not eof:
        try:
            os.kill(pid, signal.SIGKILL)    # a session that never reached EOF is ended, never waited on forever
        except OSError:
            pass
    try:
        os.close(fd)
    except OSError:
        pass
    how = "nostatus"
    try:
        _, stat = os.waitpid(pid, 0)
        how = ("sig%d" % os.WTERMSIG(stat)) if os.WIFSIGNALED(stat) else ("exit%d" % os.WEXITSTATUS(stat))
    except OSError:
        pass
    return buf.replace("\r", ""), (eof and how == "exit0")


def pr(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return ("0x%x" % int(m.group(1), 16)) if m else "absent"


def exc(t):
    c = pr(t, "cause")
    return ("%d" % ((int(c, 16) >> 2) & 0x1f)) if c != "absent" else "absent"


def count(t, s, clean):
    """a text count is evidence only from a whole transcript: an unclean session reads `unclean', never a number"""
    return t.count(s) if clean else "unclean"


class Addr(object):
    def __init__(self, base):
        self.a = base

    def take(self, n):
        got = self.a
        self.a += 4 * (n + 2) + 0x20
        return got


def run_ops(ops, at):
    put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
    put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
            "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, OP_NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]


def ld(A, op, addr, rt, at=None):
    """one load `op rt, 0(at)', rt seeded with SENT; returns (cmds, code address)"""
    here = A.take(1) if at is None else at
    return ["at=0x%x" % addr, "%s=0x%x" % (rt, SENT)] + run_ops([enc(op, "at", rt)], here), here


def st(A, op, addr, val, at=None):
    here = A.take(1) if at is None else at
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([enc(op, "a3", "t0")], here), here


AFTER = ["print pc", "print cause"]


def roundtrip(A):
    """a RAM round trip printed in v1: absent if the host died, the sentinel if the CPU was stopped"""
    c1, _ = st(A, "sw", SCRATCH_RAM, LIVE_VAL)
    c2, _ = ld(A, "lw", SCRATCH_RAM, "v1")
    return c1 + c2 + ["print v1"]



def nth(t, reg, n):
    ms = re.findall(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return int(ms[n], 16) if len(ms) > n else None



SMALL = 66 * 100000


def mag(v):
    return "absent" if v is None else ("small" if v < SMALL else "large")


```

The PRE-EXISTING rows that refuse at TIME and REV (latch CLEAR at the refusal), and the `latch x5`
session's later refusals at +0x00 and +0x38 (latch SET, from CODE, no TIME sample after):

```python
for op in ("lb", "sb", "lh", "sh"):
    A = Addr(CODE)
    c = []
    x, _ = ld(A, "ld", CRIME + 0x38, "s0"); c += x
    if op in ("lb", "lh"):
        x, _ = ld(A, op, CRIME + 0x38, "v0"); c += x
    else:
        x, _ = st(A, op, CRIME + 0x38, 0xff if op == "sb" else 0xffff); c += x
    x, _ = ld(A, "ld", CRIME + 0x38, "s1"); c += x
    x, _ = ld(A, "ld", CRIME + 0x38, "s2"); c += x
    if op == "lb":                                  # a second refusal: the TIME-first latch cell
        x, _ = ld(A, "lb", CRIME + 0x07, "v1"); c += x
    t, clean = session(c + ["print s1", "print s2", "print v0"])
    s1, s2 = nth(t, "s1", 0), nth(t, "s2", 0)
    row("time %s" % op, mag(s1), "small", "after refused %s +0x38 (raw %s)" % (op, s1))
    row("time %s ctl" % op, mag(s2), "large", "CONTROL: accepted ld moved TIME (raw %s)" % s2)
    if op in ("lb", "lh"):
        row("time %s v0" % op, pr(t, "v0"), "0x0", "refused %s +0x38 answers 0" % op)
    if op == "lb":
        row("time once", count(t, "-- declined.", clean), 1, "first refusal at CRIME_TIME, then +0x07: one notice")
        row("time said", said(t, 1, 0x38, clean), 1, "lb +0x38 (first refusal): its own announce")

for op in ("lb", "lh"):
    A = Addr(CODE)
    x, _ = ld(A, op, CRIME + 0, "v0", at=PROBE_PC)
    more = ld(A, "lb", CRIME + 0x07, "v1")[0] if op == "lb" else []     # a second refusal: the REV-first latch cell
    t, clean = session(["ra=0x%x" % RA] + x + AFTER + ["print v0"] + more)
    row("%s rev pc" % op, pr(t, "pc"), "0x%x" % (PROBE_PC + 4), "%dR at CRIME_REV from 0xbfc05180: pc NOT ra"
        % (1 if op == "lb" else 2))
    row("%s rev v0" % op, pr(t, "v0"), "0x0", "refused %s at CRIME_REV answers 0" % op)
    if op == "lb":
        row("rev once", count(t, "-- declined.", clean), 1, "first refusal at CRIME_REV, then +0x07: one notice")
        row("rev said", said(t, 1, 0x0, clean), 1, "lb +0x00 (first refusal, every address bit clear): its own announce")

#  the CRIME_REV arm's PROM-probe hack does not test writeflag, so the WRITE cells at +0 are side-effect cells too
for op, val in (("sb", 0xa5), ("sh", 0xa5a5)):
    A = Addr(CODE)
    x, _ = st(A, op, CRIME + 0, val, at=PROBE_PC)
    t, clean = session(["ra=0x%x" % RA] + x + AFTER)
    row("%s rev pc" % op, pr(t, "pc"), "0x%x" % (PROBE_PC + 4), "%dW at CRIME_REV from 0xbfc05180: pc NOT ra"
        % (1 if op == "sb" else 2))

...
for op, off in (("lh", 6), ("lb", 7), ("lbu", 0x3f)):
    x, _ = ld(A, op, CRIME + off, "v0"); c += x
for op, off, val in (("sb", 0x37, 0xab), ("sh", 0x36, 0xabcd)):
    x, _ = st(A, op, CRIME + off, val); c += x
#  and refusals at CRIME_REV and CRIME_TIME AFTER the latch is set (the Opus third-closing seat, measured: a latch TEST
#  that lets one label through -- `|| relative_addr == CRIME_REV' -- passed, because REV and TIME were each refused only
#  once per session, first; every other label is refused again after the latch is set somewhere)
for off in (0x00, 0x38):
    x, _ = ld(A, "lb", CRIME + off, "v0"); c += x
t, clean = session(c + roundtrip(A))
row("latch x5", count(t, "-- declined.", clean), 1, "5 refused accesses, then +0x00, +0x38 -> one (once)")
row("latch surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives all five")
```

## 5. THE DIFF UNDER REVIEW -- `regress/crime_width_probe.py` a0af7c92 -> f5e915f6, WHOLE

```diff
--- crime_width_probe.py	2026-09-23 15:25:36.426365700 -0500
+++ artifacts/crimewidthkill/table14_20260926/crime_width_probe.table14.py	2026-09-26 00:27:18.403660000 -0500
@@ -331,11 +331,26 @@
       M5_revlatch    the same at CRIME_REV                                        -- 188/188  [188-row]
   with M4_timeplain (the same edit WITHOUT the latch conjunct) killed at 184/188 and M6_istlatch (the same  [188-row]
   edit at INTSTAT) killed at 185/188 -- the controls that make those two escapes mean `no row looked'.  [188-row]
-  *** OF THE FIVE GUEST-OBSERVABLE LABELS ON THAT FACE, THREE HAVE BEEN SWEPT (INTSTAT killed, TIME and REV
-  escaping) AND **INTMASK AND CONTROL-WRITE ARE COVERED ONLY BY READING, NEVER MEASURED**.  Deriving them
-  covered is the same move that M5_revlatch was built to punish: REV was DERIVED open and then MEASURED
-  open. ***  Carriers for TIME and REV, and label-swap mutants for INTMASK and CONTROL-write, are OWED and
-  are not in this file yet.
+  *** REPAIR 15 (2026-09-26) ROWS THE OPEN CELLS.  The floor, by the flagship's first-hand re-ruling
+  (artifacts/crimewidthkill/rerule_20260925/fable5_rerule_529_20260925.md), is {observable skipped label} x
+  {latch SET}.  M3/M5 escaped because no refusal at TIME or REV with the latch already SET had a channel: the
+  `time' and `rev' sessions refuse there FIRST, and the `latch x5' session's later refusals at +0x00 and +0x38
+  run from CODE (REV's redirect needs the PROM window) with no TIME sample after them.  The `tl' and `rl' rows
+  refuse at +0x07 FIRST, then at the label.  The five guest-observable labels, the label-swap built for each,
+  and the table that measures it (scores are in those tables' logs, never here):
+      INTSTAT  M6_istlatch      istat sb/lh/sh                  repair14_20260916/ (table 12)
+      INTMASK  M7_intmasklatch  imask sb/lh/sh                  table13a_20260925/
+      CONTROL  M8_ctllatch      sb08 msg, sh08b run, gate run   table13a_20260925/
+      TIME     M3_timelatch     tl lb/sb/lh/sh                  table14_20260926/
+      REV      M5_revlatch      rl lb/lh/sb/sh pc               table14_20260926/
+  DOG (a bare `break;') and default (host log only -- and `mid nodflt' already reads it after a latch-
+  setting refusal: M1_gotolatch reddened it in table 12) have no guest-observable arm: clause (e).
+  ENTRIES 13/17 of ACCEPTS (`sw'/`sd +0x08 = 0x0200', CONTROL's DOG mask): the arm clears DOG and nothing
+  prints, and the prelude re-forces the register at every access, so the CONTROL text COUNT is the cell's one
+  observable -- and no row read it in a session holding that write.  `ctldog sw msg'/`ctldog sd msg' are the pair
+  (D_nodogclear, the DOG branch's clear deleted; table14_20260926/).  A SILENT decline of the DOG-only write
+  changes nothing any access can see: EQUIVALENT, disclosed.  The latch x DOG joint is clause (e): the CONTROL
+  arm reads no latch. ***
 
 DISCLOSED, not rowed:
   * `goto crime_declined' -> `return 1' is EQUIVALENT on every channel: memory_rw pre-zeroes a device read buffer
@@ -869,6 +884,62 @@
         row("time once", count(t, "-- declined.", clean), 1, "first refusal at CRIME_TIME, then +0x07: one notice")
         row("time said", said(t, 1, 0x38, clean), 1, "lb +0x38 (first refusal): its own announce")
 
+# ---- #529 REPAIR 15: THE DECLINE HOLDS WITH THE LATCH ALREADY SET, at the two labels whose leak no row saw ----
+#  The `time' and `rev' sessions above refuse at TIME/REV FIRST, so the width latch is still CLEAR there -- and a
+#  `goto' conditioned on the SET latch plus the label (M3_timelatch, M5_revlatch; repair14_20260916/, table 12)
+#  never leaks in them.  (The `latch x5' session below refuses at +0x00 and +0x38 with the latch SET, but from CODE
+#  -- REV's redirect needs the PROM window -- and with no TIME sample after, so neither leak had a channel there.)
+#  Here the FIRST refusal is at +0x07 (the default arm; it sets the latch), and only THEN the refusal at the label.
+#  CHANNELS: TIME -- crime_update_crime_time() at the refused access moves the next sample by the wall-clock since
+#  the last update (large vs SMALL: the `time' rows' channel, and their disclosed tick assumption; the extra +0x07
+#  access adds debugger steps, never a TIME update, on a fix build); REV -- the arm's PROM-window hack redirects the
+#  pc to ra (the `rev pc' rows' channel).  All four narrow ops at each label, as repair 14's ruling said: the
+#  decline block tests neither width nor direction, and the four are the width x direction cells a leak keyed on
+#  either could use.
+for op in ("lb", "sb", "lh", "sh"):
+    A = Addr(CODE)
+    c = []
+    x, _ = ld(A, "ld", CRIME + 0x38, "s0"); c += x
+    x, _ = ld(A, "lb", CRIME + 0x07, "v1"); c += x          # the FIRST refusal: sets the latch
+    if op in ("lb", "lh"):
+        x, _ = ld(A, op, CRIME + 0x38, "v0"); c += x
+    else:
+        x, _ = st(A, op, CRIME + 0x38, 0xff if op == "sb" else 0xffff); c += x
+    x, _ = ld(A, "ld", CRIME + 0x38, "s1"); c += x
+    x, _ = ld(A, "ld", CRIME + 0x38, "s2"); c += x
+    t, clean = session(c + ["print s1", "print s2"])
+    s1, s2 = nth(t, "s1", 0), nth(t, "s2", 0)
+    row("tl %s" % op, mag(s1), "small", "latch SET, refused %s +0x38: no clock step (raw %s)" % (op, s1))
+    row("tl %s ctl" % op, mag(s2), "large", "CONTROL: accepted ld moved TIME (raw %s)" % s2)
+
+for op in ("lb", "lh", "sb", "sh"):
+    A = Addr(CODE)
+    y, _ = ld(A, "lb", CRIME + 0x07, "v1")                 # the FIRST refusal, from CODE: sets the latch
+    if op in ("lb", "lh"):
+        x, _ = ld(A, op, CRIME + 0, "v0", at=PROBE_PC)
+    else:
+        x, _ = st(A, op, CRIME + 0, 0xa5 if op == "sb" else 0xa5a5, at=PROBE_PC)
+    t, clean = session(["ra=0x%x" % RA] + y + x + AFTER)
+    row("rl %s pc" % op, pr(t, "pc"), "0x%x" % (PROBE_PC + 4),
+        "latch SET, refused %s at CRIME_REV from 0xbfc05180: pc NOT ra" % op)
+
+# ---- #529 REPAIR 15: ACCEPTS entries 13/17, CONTROL's DOG-only writes (FABLE_RULING_20260917.md B) ----
+#  `sw'/`sd +0x08 = 0x0200': the arm clears DOG, the residue is 0 and nothing prints, and the prelude re-forces
+#  CONTROL at every access -- so the CONTROL text COUNT is the cell's one observable, and no session holding a
+#  0x0200 write read it (the ACCEPTS sessions count `-- declined.'; `p acc ctl msg' writes 0x01, 0x0001 and
+#  0x0201).  MUTANT: D_nodogclear, the DOG branch's `idata &= ~CRIME_CONTROL_DOG_ENABLE;' deleted -- the arm's own
+#  tested bit with its repair nulled -- prints for 0x0200.  Each width is one session: the 0x0200 write, then its
+#  0x0201 twin, the in-session LIVENESS half of the pair (a bare count of 0 is green under a dead channel or a
+#  declined write).  CHANNEL: fix ONE text, the twin's; D_nodogclear TWO.  A silent decline of the 0x0200 write
+#  still reads ONE -- EQUIVALENT, since no access can see the cell (disclosed in the contract).
+for op in ("sw", "sd"):
+    A = Addr(CODE)
+    x, _ = st(A, op, CRIME + 0x08, 0x0200)
+    y, _ = st(A, op, CRIME + 0x08, 0x0201)
+    t, clean = session(x + y)
+    row("ctldog %s msg" % op, count(t, "CRIME_CONTROL: unimplemented", clean), 1,
+        "%s 0x0200 then 0x0201 +0x08: ONE CONTROL text, the twin's" % op)
+
 # ---- a refused store leaves the register it names untouched (CRIME_DOG seeded by an accepted sd) ----
 A = Addr(CODE)
 c = []
@@ -1589,7 +1660,8 @@
 control = all(st_.get(n, False) for n in ("live", "devsig", "devsig hi", "dflt ctl", "rev pc ctl", "sw08 halts",
                                           "gate hardint", "gate line",
                                           "sw08 msg ctl", "imask pre", "imask ctl", "istat pre", "istat ctl",
-                                          "time lb ctl", "time sb ctl", "time lh ctl", "time sh ctl"))
+                                          "time lb ctl", "time sb ctl", "time lh ctl", "time sh ctl",
+                                          "tl lb ctl", "tl sb ctl", "tl lh ctl", "tl sh ctl"))
 print("")
 print("FAILING: " + ", ".join(n for n, ok in rows if not ok))
 print("CRIMEP_RESULT=%d/%d" % (npass, len(rows)))
```

## 6. THE ENTRIES-13/17 CHANNEL CHECK (the repair-14 ruling's conditional, run for this repair)

The ruling's words: *"name the mutant each kills and the observable that differs ... If a
body-tested-partition mutant escapes -> L2, IN as the pair; if the count cannot vary under any such
mutant -> clause (e), disclosed."*  ACCEPTS entries 13/17 are accepted `sw`/`sd +0x08 = 0x0200`
(DOG_ENABLE alone).  The prelude re-forces CONTROL = ENDIANESS at every access, so the stored value is
visible to nothing; the arm clears DOG, the residue is 0, nothing prints and nothing stops.  The
mutant that moves the cell: **D_nodogclear**, the DOG branch's `idata &= ~CRIME_CONTROL_DOG_ENABLE;`
deleted, which makes the arm print for 0x0200.  Before repair 15 five rows counted
`CRIME_CONTROL: unimplemented` -- `sw08 msg ctl` (session writes sw 0x01), `sb08 msg` and `sh08b msg`
(REFUSED narrow writes, declined before the arm), `acc ctl sd` (sd 0x01), `p acc ctl msg` (sd 0x01,
sw 0x0001, sw 0x0201, sd 0x0201) -- and NONE of their sessions writes 0x0200; the ACCEPTS sessions
that do write it count only `-- declined.`.  So repair 15 adds `ctldog sw msg` / `ctldog sd msg`: one
session per width, the 0x0200 write then its 0x0201 twin (the in-session liveness half), expecting ONE
text.  A silent decline of the 0x0200 write still reads one -- disclosed as EQUIVALENT.

## 7. THE MUTANTS, VERBATIM HUNKS (each applied to dev_sgi_ip32.c 8c1d1545; every re-derived edit was
checked byte-identical to the diff its earlier table preserved)

**M1_gotolatch**

```
+			goto crime_declined;
-		goto crime_declined;
```

**M3_timelatch**

```
+			goto crime_declined;
-		goto crime_declined;
+		if (relative_addr != CRIME_TIME)
+			goto crime_declined;
```

**M4_timeplain**

```
-		goto crime_declined;
+		if (relative_addr != CRIME_TIME)
+			goto crime_declined;
```

**M5_revlatch**

```
+			goto crime_declined;
-		goto crime_declined;
+		if (relative_addr != CRIME_REV)
+			goto crime_declined;
```

**M6_istlatch**

```
+			goto crime_declined;
-		goto crime_declined;
+		if (relative_addr != CRIME_INTSTAT)
+			goto crime_declined;
```

**M7_intmasklatch**

```
+			goto crime_declined;
-		goto crime_declined;
+		if (relative_addr != CRIME_INTMASK)
+			goto crime_declined;
```

**M8_ctllatch**

```
+			goto crime_declined;
-		goto crime_declined;
+		if (relative_addr != CRIME_CONTROL)
+			goto crime_declined;
```

**G_glm_tim4clear**

```
+	if (len == 4 && relative_addr == CRIME_TIME && !(d->warned & CRIME_W_LEN))
+		goto crime_declined;
```

**G_clr_ist4r**

```
+	if (len == 4 && writeflag == MEM_READ && relative_addr == CRIME_INTSTAT && !(d->warned & CRIME_W_LEN))
+		goto crime_declined;
```

**G_clr_ctl4r**

```
+	if (len == 4 && writeflag == MEM_READ && relative_addr == CRIME_CONTROL && !(d->warned & CRIME_W_LEN))
+		goto crime_declined;
```

**G_clr_imk4r**

```
+	if (len == 4 && writeflag == MEM_READ && relative_addr == CRIME_INTMASK && !(d->warned & CRIME_W_LEN))
+		goto crime_declined;
```

**G_lane_ctl**

```
-			if (relative_addr & 4)
+			if ((relative_addr & 4) || (relative_addr == CRIME_CONTROL && (d->warned & CRIME_W_LEN)))
```

**K_ctl4w_reset_post**

```
-	} else if (len == 4) {
+	} else if (len == 4 && !(writeflag == MEM_WRITE && relative_addr == CRIME_CONTROL && (idata & CRIME_CONTROL_HARD_RESET) &&
+	    (d->warned & CRIME_W_LEN))) {
```

**K_ctl8w_reset_post**

```
-	if (len == 8) {
+	if (len == 8 && !(writeflag == MEM_WRITE && relative_addr == CRIME_CONTROL && (idata & CRIME_CONTROL_HARD_RESET) &&
+	    (d->warned & CRIME_W_LEN))) {
```

**M2_ld278clr**

```
+	if (relative_addr == 0x278 && len == 8 && writeflag == MEM_READ
+	    && !(d->warned & CRIME_W_LEN))
+		goto crime_declined;
```

**W_ctl8w**

```
+	if (len == 8 && relative_addr == CRIME_CONTROL &&
+	    writeflag == MEM_WRITE && (d->warned & CRIME_W_LEN))
+		goto crime_declined;
```

**D_nodogclear**

```
-				idata &= ~CRIME_CONTROL_DOG_ENABLE;
```

## 8. MEASUREMENTS

**Table 12** (repair 14, 204 rows; `repair14_20260916/logs/lane*.out`, verbatim):

```
base CRIMEP_RESULT=204/204 CRIMEP_CONTROL=OK done=1 FAILING: 
G_clr_imk4r CRIMEP_RESULT=203/204 CRIMEP_CONTROL=FAIL done=1 FAILING: gate line
M1_gotolatch CRIMEP_RESULT=194/204 CRIMEP_CONTROL=OK done=1 FAILING: sb08 msg, sh08b run, imask sb, imask lh, imask sh, istat sb, istat lh, istat sh, gate run, mid nodflt
M5_revlatch CRIMEP_RESULT=204/204 CRIMEP_CONTROL=OK done=1 FAILING: 
G_glm_tim4clear CRIMEP_RESULT=202/204 CRIMEP_CONTROL=OK done=1 FAILING: c t4w gap, c t4r gap
G_lane_ctl CRIMEP_RESULT=203/204 CRIMEP_CONTROL=OK done=1 FAILING: p acc ctl4r
M2_ld278clr CRIMEP_RESULT=203/204 CRIMEP_CONTROL=OK done=1 FAILING: top8 clear
M6_istlatch CRIMEP_RESULT=201/204 CRIMEP_CONTROL=OK done=1 FAILING: istat sb, istat lh, istat sh
G_clr_ist4r CRIMEP_RESULT=203/204 CRIMEP_CONTROL=OK done=1 FAILING: acc istat lw
K_ctl4w_reset_post CRIMEP_RESULT=203/204 CRIMEP_CONTROL=OK done=1 FAILING: rst 4w
M3_timelatch CRIMEP_RESULT=204/204 CRIMEP_CONTROL=OK done=1 FAILING: 
W_ctl8w CRIMEP_RESULT=202/204 CRIMEP_CONTROL=OK done=1 FAILING: p acc ctl msg, rst 8w
G_clr_ctl4r CRIMEP_RESULT=204/204 CRIMEP_CONTROL=OK done=1 FAILING: 
K_ctl8w_reset_post CRIMEP_RESULT=203/204 CRIMEP_CONTROL=OK done=1 FAILING: rst 8w
M4_timeplain CRIMEP_RESULT=200/204 CRIMEP_CONTROL=OK done=1 FAILING: time lb, time sb, time lh, time sh
```

**Table 13a** (the INTMASK/CONTROL swaps and a base leg on probe a0af7c92, 204 rows; verbatim):

```
base CRIMEP_RESULT=204/204 CRIMEP_CONTROL=OK done=1 FAILING: 
M7_intmasklatch CRIMEP_RESULT=201/204 CRIMEP_CONTROL=OK done=1 FAILING: imask sb, imask lh, imask sh
M8_ctllatch CRIMEP_RESULT=201/204 CRIMEP_CONTROL=OK done=1 FAILING: sb08 msg, sh08b run, gate run
```

**Table 14 PREDICTIONS**, written in `PRETABLE14.out` BEFORE any build (its mtime proves the order), verbatim:

```
PREDICTIONS -- exact red sets, score over 218, CRIMEP_CONTROL:
  base                none                                                                  218/218  OK
  G_clr_ctl4r         none (the equivalent 4R cell; ctl0c_discharge_20260917/VERDICT.md)    218/218  OK
  G_clr_imk4r         gate line                                                             217/218  FAIL (gate line
                                                                                                     is a control)
  G_clr_ist4r         acc istat lw                                                          217/218  OK
  G_glm_tim4clear     c t4w gap, c t4r gap                                                  216/218  OK
  G_lane_ctl          p acc ctl4r                                                           217/218  OK
  K_ctl4w_reset_post  rst 4w                                                                217/218  OK
  K_ctl8w_reset_post  rst 8w                                                                217/218  OK
  M1_gotolatch        table 12's ten -- sb08 msg, sh08b run, imask sb, imask lh, imask sh, istat sb, istat lh,
                      istat sh, gate run, mid nodflt -- plus tl lb, tl sb, tl lh, tl sh, rl lb pc, rl lh pc,
                      rl sb pc, rl sh pc                                                    200/218  OK
  M2_ld278clr         top8 clear                                                            217/218  OK
  M3_timelatch        tl lb, tl sb, tl lh, tl sh                                            214/218  OK
  M4_timeplain        time lb, time sb, time lh, time sh, tl lb, tl sb, tl lh, tl sh        210/218  OK
  M5_revlatch         rl lb pc, rl lh pc, rl sb pc, rl sh pc                                214/218  OK
  M6_istlatch         istat sb, istat lh, istat sh                                          215/218  OK
  W_ctl8w             p acc ctl msg, rst 8w                                                 216/218  OK
  M7_intmasklatch     imask sb, imask lh, imask sh                                          215/218  OK
  M8_ctllatch         sb08 msg, sh08b run, gate run                                         215/218  OK
  D_nodogclear        ctldog sw msg, ctldog sd msg                                          216/218  OK

```

**Table 14 RESULTS** (218 rows; four lanes; `table14_20260926/logs/lane*.out` and `check14.out`, verbatim):

```
base CRIMEP_RESULT=218/218 CRIMEP_CONTROL=OK done=1 FAILING:  00:54:13
G_clr_imk4r CRIMEP_RESULT=217/218 CRIMEP_CONTROL=FAIL done=1 FAILING: gate line 01:14:19
M1_gotolatch CRIMEP_RESULT=200/218 CRIMEP_CONTROL=OK done=1 FAILING: sb08 msg, sh08b run, imask sb, imask lh, imask sh, istat sb, istat lh, istat sh, gate run, tl lb, tl sb, tl lh, tl sh, rl lb pc, rl lh pc, rl sb pc, rl sh pc, mid nodflt 01:34:27
M5_revlatch CRIMEP_RESULT=214/218 CRIMEP_CONTROL=OK done=1 FAILING: rl lb pc, rl lh pc, rl sb pc, rl sh pc 01:54:33
M8_ctllatch CRIMEP_RESULT=215/218 CRIMEP_CONTROL=OK done=1 FAILING: sb08 msg, sh08b run, gate run 02:14:41
G_glm_tim4clear CRIMEP_RESULT=216/218 CRIMEP_CONTROL=OK done=1 FAILING: c t4w gap, c t4r gap 00:54:13
G_lane_ctl CRIMEP_RESULT=217/218 CRIMEP_CONTROL=OK done=1 FAILING: p acc ctl4r 01:14:19
M2_ld278clr CRIMEP_RESULT=217/218 CRIMEP_CONTROL=OK done=1 FAILING: top8 clear 01:34:27
M6_istlatch CRIMEP_RESULT=215/218 CRIMEP_CONTROL=OK done=1 FAILING: istat sb, istat lh, istat sh 01:54:33
D_nodogclear CRIMEP_RESULT=216/218 CRIMEP_CONTROL=OK done=1 FAILING: ctldog sw msg, ctldog sd msg 02:14:41
G_clr_ist4r CRIMEP_RESULT=217/218 CRIMEP_CONTROL=OK done=1 FAILING: acc istat lw 00:54:13
K_ctl4w_reset_post CRIMEP_RESULT=217/218 CRIMEP_CONTROL=OK done=1 FAILING: rst 4w 01:14:19
M3_timelatch CRIMEP_RESULT=214/218 CRIMEP_CONTROL=OK done=1 FAILING: tl lb, tl sb, tl lh, tl sh 01:34:27
W_ctl8w CRIMEP_RESULT=216/218 CRIMEP_CONTROL=OK done=1 FAILING: p acc ctl msg, rst 8w 01:54:33
G_clr_ctl4r CRIMEP_RESULT=218/218 CRIMEP_CONTROL=OK done=1 FAILING:  00:54:13
K_ctl8w_reset_post CRIMEP_RESULT=217/218 CRIMEP_CONTROL=OK done=1 FAILING: rst 8w 01:14:19
M4_timeplain CRIMEP_RESULT=210/218 CRIMEP_CONTROL=OK done=1 FAILING: time lb, time sb, time lh, time sh, tl lb, tl sb, tl lh, tl sh 01:34:27
M7_intmasklatch CRIMEP_RESULT=215/218 CRIMEP_CONTROL=OK done=1 FAILING: imask sb, imask lh, imask sh 01:54:33

leg                  score      reds  control  verdict
base                 218/218       0  OK       exact
G_glm_tim4clear      216/218       2  OK       exact
G_clr_ist4r          217/218       1  OK       exact
G_clr_ctl4r          218/218       0  OK       exact
G_clr_imk4r          217/218       1  FAIL     exact
G_lane_ctl           217/218       1  OK       exact
K_ctl4w_reset_post   217/218       1  OK       exact
K_ctl8w_reset_post   217/218       1  OK       exact
M1_gotolatch         200/218      18  OK       exact
M2_ld278clr          217/218       1  OK       exact
M3_timelatch         214/218       4  OK       exact
M4_timeplain         210/218       8  OK       exact
M5_revlatch          214/218       4  OK       exact
M6_istlatch          215/218       3  OK       exact
W_ctl8w              216/218       2  OK       exact
M7_intmasklatch      215/218       3  OK       exact
M8_ctllatch          215/218       3  OK       exact
D_nodogclear         216/218       2  OK       exact

CHECK14_PASS
```

## 9. WHAT THIS PACKET SHOWS OF #529's FILES

    regress/crime_width_probe.py      repair 15's diff: INLINED whole (section 5)
    src/devices/dev_sgi_ip32.c        UNCHANGED by repair 15; the whole access function INLINED as context
    regress/gate_arm.sh               UNCHANGED by repair 15; the 204 -> 218 pin is OWED after this pass
    records (CHANGELOG, ledger, MANIFEST, carrier)   NOT SHOWN -- not written yet; they follow this pass

## 10. QUESTIONS (verdict line first; then one line per question; then reasons)

**Q1. PREMISE AUDIT -- each stated as a question.  Check the ones you can; name the ones you cannot.**
  (a) Is it true that a session's rows cannot be moved by adding OTHER sessions (fresh emulator per
      session)?  Is there any state that crosses sessions -- a file, the dummy RAM image, the host clock?
  (b) Is it true that the `tl` rows' s1 stays SMALL on the fixed build?  Walk the updates to
      `d->reg[TIME]` in a `tl` session step by step: the s0 load, the tick, the +0x07 refusal, the
      refusal at 0x38, the s1 load.  Where exactly can an update happen, and is the fixed build's s1
      the value left by the tick?
  (c) Is it true that the REV arm's redirect fires for all four narrow ops once the goto is skipped --
      including the WRITES, and including `lh` (a 2-byte access at +0x00)?
  (d) Is it true that D_nodogclear is the ONLY mutant of the CONTROL arm's DOG partition that no row
      saw before repair 15?  (Think of DOG treated as a stop bit; DOG suppressing the residue print; a
      re-arm inside the DOG branch.)
  (e) Is the five-label enumeration complete?  The switch's labels are REV, CONTROL, INTSTAT, INTMASK,
      DOG, TIME and `default:` -- which of them has a guest-observable effect that a suppressed decline
      would expose, and is any offset outside those labels observable some other way?

**Q2. THE FLOOR QUESTION, ON THE COMPOSITE.**  After repair 15, does any mutant exist in the
decline-suppression class {observable label} x {latch SET} -- or in the enumeration the contract claims
(section 5's contract block) -- that the 218 rows do not see?  Name the label, the latch state and the
row you expect to stay green.  **The closing condition is zero breaches WITH THE DENOMINATOR: say which
cells and shapes you swept.**  A bare "none found" does not close.

**Q3. THE 13/17 DISPOSITION.**  The ruling offered two dispositions (L2 pair, or clause-(e) disclosure).
Is the pair the right member, and is there a member neither the ruling nor this brief named?  Is the
pair's channel sound -- can `ctldog <w> msg` read ONE on a build where the 0x0200 write DID print?

**Q4. TABLE 14 AGAINST ITS PREDICTIONS.**  Section 8 shows the pre-registered red sets and the results.
Does any leg's result differ from its prediction, and if so which of the three explanations fits
(mis-built mutant, dead target, mis-cut row)?  Does any row red on a leg where no hunk reaches it?

If, while verifying a claim, you found something ELSE -- say so.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
