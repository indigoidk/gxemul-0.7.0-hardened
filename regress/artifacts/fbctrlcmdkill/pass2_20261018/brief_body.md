# `fbctrlcmdkill` (HIGH) -- pass 2 on the real diff: `#567` refuses every framebuffer-controller command but 0-2 before the store

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise its brief's author stated wrongly.  **Check the premises, not
just the derivations.**  Where I state something as fact, ask whether it is true.  A seat that re-derives a premise from
something this brief did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`, its WORKING TREE (the diff below is uncommitted).**
Ignore every other `src/` under the project root (pristine 2021 upstream copies).  The working tree also carries
UNRELATED uncommitted edits to other files (`dev_lca.c`, `dev_pcc2.c`, `dev_sh4.c`, `cpu_alpha_palcode.c`,
`regress/diff_wdc_identify.c`, `regress/gate_offline.sh` and others) -- they are not this round; ignore them.  Frozen
copies of this round's files are in `regress/artifacts/fbctrlcmdkill/pass2_20261018/frozen/` -- cite those.

**If you cannot read files that is expected** -- every fact you need is inlined.  Name any premise you cannot settle from
this packet rather than guessing at it.  **Where this brief states an arithmetic claim -- a value range, a count of rows
-- ENUMERATE it rather than reasoning about it**, and enumerate the right domain: ask what the producer of a value can
actually emit before walking it.

**VERDICT LINE FIRST**, so your answer survives truncation.  READ-ONLY: write nothing to any project tree.

## What this pass reviews -- `git diff --numstat`, each file with its disclosure

```
22   1  src/devices/dev_fbctrl.c               INLINED -- the whole diff, and the post-fix functions in full (section 1)
378  0  regress/fbctrl_cmd_probe.py (NEW)      INLINED IN FULL (section 2)
47   0  regress/gate_mips_folds.sh             INLINED -- the whole added block (section 3)
13   6  regress/gate_hygiene.sh                INLINED -- the whole diff (section 5)
3    1  tools/precommit_check.sh               INLINED (section 5)
1    0  tools/pipeline/check_probe_wiring.py   INLINED (section 5); the working file carries 15 MORE uncommitted lines
                                               from other work -- not this round, not shown, not to be staged
```

`est/src/devices/dev_fbctrl.c` (the non-git twin tree) is byte-identical to SEC's (md5 490b57d8...).  The records
(CHANGELOG block, bug-file entry, ledger) are not written yet; they follow this pass.

## SETTLED PREMISES -- recorded resolutions, re-inlined so nobody spends an answer re-deriving them

* **`fatal()` prints and RETURNS** -- `src/core/debugmsg.c`'s `fatal()` has no early-out and no exit.  Every refusal row
  rests on it (as `#549`'s 117-row detector does).
* **Pass 1 (2026-10-18, `pass1_20261018/ADJUDICATION_p1.md`)**: GPT-6 Astra, Grok 4.7 and GLM 5.3 each chose option
  member 3 -- REFUSE every 64-bit DATA value other than 0, 1 and 2 at COMMAND **before the store**, leave COMMAND
  unchanged, one new `warned_cmd` latch and one `(once)` announce naming the full value, a new gated probe.  FILL (3) and
  COPY (4) have no port semantics anywhere (a `TODO:` over two bare constants), so implementing them is a feature, not a
  fix.  `fbctrloffkill` (the same file's offset `default:`) stays its own row, 2-1.  The Fable seat walled (held).
* **The test-first witness (rung 3, unmodified `-E testmips`, HEAD's binary): 2/12** -- DATA writes of 3, 4, 5, -1 at
  COMMAND, and `sd 0x100000003`, each end the host with exit 1 (`pass1_20261018/WITNESS_headbin.out`); 12/12 on the fix.
* **The house latch idiom** is one latch per device instance and per message, with a `(once)` marker; `#549`'s
  `warned_port` is this device's existing one.
* **Floor clause (c)** is recorded in one of two forms -- `(c): measured at <artifact>` or `(c): by construction via
  <row/pin>, leg not run` -- and the null medium for a runtime probe is an absent or non-emulator binary.
* **Rule D2**: a compare against a constant bound B that a fix depends on is pinned by rows at B+1 (past the bound) and
  B-1 (below it); a far row proves the branch exists and never pins the bound.

## 1. The fix -- the diff, then the post-fix code in full (every exit path and the common tail)

```diff
diff --git a/src/devices/dev_fbctrl.c b/src/devices/dev_fbctrl.c
index eab10df8..2013d66e 100644
--- a/src/devices/dev_fbctrl.c
+++ b/src/devices/dev_fbctrl.c
@@ -50,6 +50,7 @@ struct fbctrl_data {
 	int		current_port;
 	int		port[DEV_FBCTRL_NPORTS];
 	int		warned_port;	/* #549: the refused-selector announce */
+	int		warned_cmd;	/* #567: the refused-command announce */
 };
 
 
@@ -98,6 +99,9 @@ static void fbctrl_command(struct cpu *cpu, struct fbctrl_data *d)
 
 	/*  TODO: Block copy and fill.  */
 
+	/*  #567: unreachable while the DATA arm refuses every command
+	    other than these three; kept as a tripwire for a later edit
+	    that lets one in, as #549 kept the selector's.  */
 	default:fatal("fbctrl_command: Unimplemented command %i.\n", cmd);
 		exit(1);
 	}
@@ -146,7 +150,24 @@ DEVICE_ACCESS(fbctrl)
 
 		if (writeflag == MEM_READ)
 			odata = d->port[d->current_port];
-		else {
+		else if (d->current_port == DEV_FBCTRL_PORT_COMMAND &&
+		    idata > DEV_FBCTRL_COMMAND_GET_RESOLUTION) {
+			/*  #567: a command other than NOP, SET_RESOLUTION and
+			    GET_RESOLUTION is REFUSED before it is stored: COMMAND
+			    keeps its previous value and nothing executes.  It used
+			    to reach fbctrl_command()'s default: and end the
+			    emulator, FILL (3) and COPY (4) included -- the header
+			    names them under a TODO and gives them no ports.  The
+			    compare is on all 64 bits: the cell is an int, so a
+			    wide 0x100000001 used to be stored as 1 and run
+			    SET_RESOLUTION.  Announced once per device.  */
+			if (!d->warned_cmd) {
+				fatal("[ fbctrl: command 0x%llx is not supported; "
+				    "the command port is unchanged (once) ]\n",
+				    (unsigned long long) idata);
+				d->warned_cmd = 1;
+			}
+		} else {
 			d->port[d->current_port] = idata;
 			if (d->current_port == DEV_FBCTRL_PORT_COMMAND)
 				fbctrl_command(cpu, d);
```

The post-fix struct, `fbctrl_command()` and `DEVICE_ACCESS(fbctrl)`, verbatim from the frozen copy:

```c
struct fbctrl_data {
	struct vfb_data *vfb_data;
	int		current_port;
	int		port[DEV_FBCTRL_NPORTS];
	int		warned_port;	/* #549: the refused-selector announce */
	int		warned_cmd;	/* #567: the refused-command announce */
};


/*
 *  fbctrl_command():
 *
 *  Execute a framebuffer control command.
 */
static void fbctrl_command(struct cpu *cpu, struct fbctrl_data *d)
{
	int cmd = d->port[DEV_FBCTRL_PORT_COMMAND];
	int x1, y1, i;

	switch (cmd) {

	case DEV_FBCTRL_COMMAND_NOP:
		break;

	case DEV_FBCTRL_COMMAND_SET_RESOLUTION:
		/*
		 *  Change the framebuffer resolution to X1 x Y1 pixels.
		 */
		x1 = d->port[DEV_FBCTRL_PORT_X1];
		y1 = d->port[DEV_FBCTRL_PORT_Y1];
		debug("[ dev_fbctrl: changing resolution to %i,%i ]\n", x1, y1);

		dev_fb_resize(d->vfb_data, x1, y1);

		/*  Remember to invalidate all translations for anyone
		    who might have used the old framebuffer:  */
		for (i = 0; i < cpu->machine->ncpus; i++)
			cpu->machine->cpus[i]->invalidate_translation_caches(
			    cpu->machine->cpus[i], 0, INVALIDATE_ALL);
		break;

	case DEV_FBCTRL_COMMAND_GET_RESOLUTION:
		if (cpu->machine->x11_md.in_use) {
			d->port[DEV_FBCTRL_PORT_X1] = d->vfb_data->xsize;
			d->port[DEV_FBCTRL_PORT_Y1] = d->vfb_data->ysize;
		} else {
			// When not using X11 output, return 0x0 size.
			d->port[DEV_FBCTRL_PORT_X1] = 0;
			d->port[DEV_FBCTRL_PORT_Y1] = 0;
		}
		break;

	/*  TODO: Block copy and fill.  */

	/*  #567: unreachable while the DATA arm refuses every command
	    other than these three; kept as a tripwire for a later edit
	    that lets one in, as #549 kept the selector's.  */
	default:fatal("fbctrl_command: Unimplemented command %i.\n", cmd);
		exit(1);
	}
}


DEVICE_ACCESS(fbctrl)
{
	struct fbctrl_data *d = (struct fbctrl_data *) extra;
	uint64_t idata = 0, odata = 0;

	if (writeflag == MEM_WRITE)
	        idata = memory_readmax64(cpu, data, len);

	switch (relative_addr) {

	case DEV_FBCTRL_PORT:
		if (writeflag == MEM_READ)
			odata = d->current_port;
		else if (idata >= DEV_FBCTRL_NPORTS) {
			/*  #549: an out-of-range selector is REFUSED, and
			    current_port keeps its previous, always-valid value.
			    It used to be stored as an int with only a warning:
			    9 made the next DATA access end the emulator in the
			    range check below, and a wide value was truncated
			    onto a legal port (0x100000003 selected port 3).
			    Announced once per device.  */
			if (!d->warned_port) {
				fatal("[ fbctrl: port number 0x%llx is out of range; "
				    "the selector is unchanged (once) ]\n",
				    (unsigned long long) idata);
				d->warned_port = 1;
			}
		} else
			d->current_port = idata;
		break;

	case DEV_FBCTRL_DATA:
		/*  #549: unreachable while the PORT arm refuses; kept as a
		    tripwire for a later edit that lets a bad selector in.  */
		if (d->current_port < 0 || d->current_port
		    >= DEV_FBCTRL_NPORTS) {
			fatal("[ fbctrl port number is out of range! ]\n");
			exit(1);
		}

		if (writeflag == MEM_READ)
			odata = d->port[d->current_port];
		else if (d->current_port == DEV_FBCTRL_PORT_COMMAND &&
		    idata > DEV_FBCTRL_COMMAND_GET_RESOLUTION) {
			/*  #567: a command other than NOP, SET_RESOLUTION and
			    GET_RESOLUTION is REFUSED before it is stored: COMMAND
			    keeps its previous value and nothing executes.  It used
			    to reach fbctrl_command()'s default: and end the
			    emulator, FILL (3) and COPY (4) included -- the header
			    names them under a TODO and gives them no ports.  The
			    compare is on all 64 bits: the cell is an int, so a
			    wide 0x100000001 used to be stored as 1 and run
			    SET_RESOLUTION.  Announced once per device.  */
			if (!d->warned_cmd) {
				fatal("[ fbctrl: command 0x%llx is not supported; "
				    "the command port is unchanged (once) ]\n",
				    (unsigned long long) idata);
				d->warned_cmd = 1;
			}
		} else {
			d->port[d->current_port] = idata;
			if (d->current_port == DEV_FBCTRL_PORT_COMMAND)
				fbctrl_command(cpu, d);
		}

		break;

	default:
		fatal("[ dev_fbctrl: unimplemented relative addr 0x%x ]\n",
		    (int)relative_addr);
		exit(1);
	}

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}
```

## 2. The detector -- `regress/fbctrl_cmd_probe.py`, in full (its header carries the CONTRACT)

```python
#!/usr/bin/env python3
"""#567 fbctrlcmdkill -- the DETECTOR for dev_fbctrl.c's command port, on an UNMODIFIED `-E testmips`.

machine_test.c installs `fbctrl addr=0x12f00000` in testmips's own setup.  t0 = 0xffffffffb2f00000, kseg1 of
DEV_FBCTRL_ADDRESS; PORT is +0x00, DATA +0x10.  Port 0 is COMMAND; a DATA write there executes the command.  Pre-#567
any command other than NOP (0), SET_RESOLUTION (1) and GET_RESOLUTION (2) reached fbctrl_command()'s default: and
ended the emulator, and a WIDE value was stored truncated into the int cell and dispatched as its low word.  #567
refuses every 64-bit value other than 0, 1 and 2 in the DATA arm BEFORE the store: COMMAND keeps its value, nothing
executes, and one announce per device names the full value -- `[ fbctrl: command 0x... is not supported; the command
port is unchanged (once) ]`.

SESSIONS (each on a fresh emulator, every word stepped and compared with the emulator's own step line, unless F):
  C    controls: PORT=5, DATA=0x2a, read back (LIVENESS); PORT=1, DATA=123, PORT=0, DATA=2 (GET_RESOLUTION, headless:
       zeroes X1/Y1), PORT=1, read (DEVICE-SIGNATURE: 0 where RAM would keep 123).
  R:v  one REFUSAL per class, on a device seeded with COMMAND = 2 (by a GET), X1 = 123, Y1 = 77: PORT=0, DATA=v, then
       read COMMAND, X1, Y1.  Classes: 3, 4, 5 and 0xffffffff by sw; 3 by sb and 4 by sh (the gate never tests len,
       so `&& len >= 4' would let a byte or halfword command through --
       regress/artifacts/fbctrlcmdkill/draft_20261018/PRETABLE.out, section 1); 0x100000003, 0x100000000, 0x100000001,
       0x100000002 and 0xffffffffffffffff by sd.  The wide aliases of ACCEPTED commands are the width pin: a compare on
       the stored int would run NOP (COMMAND reads 0), SET_RESOLUTION (COMMAND reads 1) or GET_RESOLUTION (X1/Y1 read 0).
  A:n  ACCEPT, latch clear: NOP after COMMAND 2 (COMMAND reads 0, X1 keeps 123); SET_RESOLUTION with X1 = Y1 = 0
       (dev_fb_resize() prints `size too small (0 x 0); ignored.` -- a fatal() that returns; COMMAND reads 1);
       GET_RESOLUTION after X1 = 123, Y1 = 77 (both read 0; COMMAND reads 2).  No command announce in any of them.
  L    ACCEPT with the latch SET: refuse 3 first, then GET (X1 123 -> 0), NOP (COMMAND 0), SET at 0 x 0 (the resize line
       once, COMMAND 1) -- one command announce in the whole session.
  M1   a READ of COMMAND does not execute it: COMMAND = 2 by a GET, X1 = 123, PORT=0, read DATA (2), PORT=1, read X1
       (still 123: a re-executed GET would zero it).
  M2   a DATA write of 3 to a NON-COMMAND port (PORT=3, X2) is ordinary storage: reads back 3, no announce.
  T2   two refusals, 3 then 5: ONE command announce, naming 0x3; COMMAND keeps its power-on 0.
  P1   selector refused first (PORT=9, #549's announce), then command 4 refused: one announce of each kind.
  P2   the reverse order: command 4, then selector 9: one of each.
  F    FREE-RUNNING: PORT=0, DATA=3, then continue to a breakpoint -- the announce must print: under free-running
       debug() returns at default verbosity while fatal() prints, so this is the one row that sees a demotion.
Every refusal row rests on `fatal()` printing and RETURNING (src/core/debugmsg.c's fatal(): no early-out, no exit).

CONTRACT (clause e) -- AN ENUMERATION.
THE FLOOR.  The fixed DATA arm's refusal branch tests the access direction, the port (`current_port == COMMAND`), the
written value (`idata > DEV_FBCTRL_COMMAND_GET_RESOLUTION`, on all 64 bits) and the latch (`!warned_cmd`); the accept
branch stores the value and, at COMMAND, dispatches it.  Every cell of those is held:
  the value  at the bound, 2 (A:get, and every seed); below it, 1 (A:set) and 0 (A:nop); past it, 3 (R:3, R:sb3, L,
             T2, F -- rule D2's B+1 edge), 4 (R:4, R:sh4, P1, P2), 5 (R:5, T2), 0xffffffff (R:m1w) and all-ones (R:m1d)
  its width  sb (R:sb3), sh (R:sh4), sw (R:3, R:4, R:5, R:m1w), sd (R:w3, R:w0, R:w1, R:w2, R:m1d) -- the four wide
             values whose low word is 0..3 are the width pin: a compare on the low word accepts w0-w2
  the port   COMMAND (every R and A session, L, T2, P1, P2, F) and not COMMAND (M2: 3 at X2 is data)
  the latch  clear (the first refusal of every R session, L, T2, P1, P2, F) and set (L's three accepts, T2's second
             refusal); the selector's latch apart from it, in both orders (P1, P2)
  direction  a write (all) and a read (M1: a read of COMMAND returns it and runs nothing)
EFFECTS, each held by the sessions named:
  a refused command keeps COMMAND's previous value -- 2 (every R class), 0 (T2)
  a refused command executes nothing -- X1 and Y1 kept with a GET in COMMAND (every R class); no resize line (nosmall)
  the first refusal announces once, naming the full value -- every R class, T2 (0x3, then 5 silent), P1 and P2 (beside
      #549's selector announce), F (free-running: fatal() prints where debug() would not)
  an accepted command is stored and runs -- NOP (A:nop, L), SET_RESOLUTION (A:set, L: the resize line), GET_RESOLUTION
      (A:get, L, C), with the latch clear (A) and set (L)
Measured: the eleven edits of kill table 1 (regress/artifacts/fbctrlcmdkill/killtable1_20261018/) are all red -- the
gate removed (the pre-#567 arm: 36/95, row for row the pre-fix leg), the compare narrowed to 32 bits, the bound moved
down by one, two and three, the gate qualified by width, the latch shared with the selector's or never set, the
announce demoted to debug(), the refused value stored, and the port test dropped.
On a dead binary 15 rows read green -- the eleven `nosmall' rows and four announce counts, which read 0 on a session
that never started -- so gate 16 requires FBCMD_CONTROL=OK and pins the score by equality (kill table 1's null media).
NOT CLAIMED (disclosed).  (0) A joint cell: the latch SET crossed with a wide alias -- no row refuses w0-w2 after a
first refusal, and the gate does not read the latch.  (1) A refusal that STORES a value aliasing the previous COMMAND:
w2 truncates to 2 and its `cmd' row cannot vary; ten classes and T2 pin the store (table 1, D8).  (2) Values and bits
not listed: the compare is relational, so its generating set is its regions, held at their edges; single-bit coverage
like #549's session B is not claimed.  (3) A second fbctrl instance (#549's fbctrltwoinst, filed): warned_cmd is per
device and the probe drives one.  (4) The device's other offsets (fbctrloffkill, filed).  (5) fbctrl_command()'s
default:, kept as a tripwire: unreachable while the arm refuses, so no row reaches it on the fixed device.
FILL (3) and COPY (4) are refused because nothing implements them (the header lists them under a TODO); a round that
implements one moves its rows from the refusal list to the accept list.

Output: one row per check, then FBCMD_CONTROL=OK|FAILED, FBCMD_RESULT=n/t, FBCMD_DONE.  The exit status is 0 only when
the controls are OK and every row is green.
usage: fbctrl_cmd_probe.py <gxemul-binary>
"""
import os
import pty
import re
import select
import signal
import sys
import time

BIN = sys.argv[1]
STUBADDR = 0xffffffff80100000
CODE = 0xffffffff80100020
FBCTRL = 0xffffffffb2f00000
CMD_RE = re.compile(r"\[ fbctrl: command (0x[0-9a-f]+) is not supported; the command port is unchanged \(once\) \]")
PORT_RE = re.compile(r"\[ fbctrl: port number 0x[0-9a-f]+ is out of range; the selector is unchanged \(once\) \]")
SMALL_RE = re.compile(r"dev_fb_resize\(\): size too small \(0 x 0\); ignored\.")
UNIMPL_RE = re.compile(r"fbctrl_command: Unimplemented command")
REG = dict(zr=0, t0=8, t1=9, t2=10, t3=11, t4=12, t5=13, t6=14, t7=15, s0=16, s1=17, s2=18, s3=19, s4=20, s5=21,
           s6=22, s7=23)
OPS = dict(sb=0x28, sh=0x29, sw=0x2b, sd=0x3f, lw=0x23)


def ins(op, rt, off, base="t0"):
    return (OPS[op] << 26) | (REG[base] << 21) | (REG[rt] << 16) | (off & 0xffff)


def text(op, rt, off, base="t0"):
    return "%s %s,%d(%s)" % (op, rt, off, base)


ANCHOR = (0x0f << 26) | (REG["t7"] << 16)                   # lui t7,0 -- the breakpoint anchor, never executed
assert ins("sw", "t1", 0) == 0xad090000                    # pinned independently of the helper
assert ins("lw", "t2", 0x10) == 0x8d0a0010
assert ins("sd", "t5", 0) == 0xfd0d0000
assert ins("sw", "zr", 0) == 0xad000000
assert ins("sb", "t1", 0x10) == 0xa1090010
assert ins("sh", "t1", 0x10) == 0xa5090010
assert ANCHOR == 0x3c0f0000

#  register plan, the same in every session: s1..s3 = 1..3, s5 = 5, s6 = 9 (a refused selector), t5 = 123, t6 = 77
BASE_REGS = [("t0", FBCTRL), ("s1", 1), ("s2", 2), ("s3", 3), ("s4", 4), ("s5", 5), ("s6", 9), ("t5", 123), ("t6", 77)]


def stub_path():
    p = "/tmp/gx_fbcmd567_%d.bin" % os.getpid()
    with open(p, "wb") as f:
        f.write(b"\x00\x00\x00\x00")
    return p


def session(label, prog, regs, reads, stub, free_run=False):
    """prog: list of (op, rt, off).  Steps each (or free-runs to an anchor after the last), then prints reads."""
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-E", "testmips", "-M", "64", "0x%x:%s" % (STUBADDR, stub)])
        os._exit(127)
    buf = ""
    dead = [False]

    def rd(t=0.4):
        nonlocal buf
        r, _, _ = select.select([fd], [], [], t)
        if fd not in r:
            return True
        try:
            d = os.read(fd, 65536)
        except OSError:
            dead[0] = True
            return False
        if not d:
            dead[0] = True
            return False
        buf += d.decode("latin1", "replace")
        return True

    def wait(mark=0, echo=None, timeout=60):
        t = time.time()
        while time.time() - t < timeout:
            if not rd():
                return False
            resp = buf[mark:]
            if echo is not None and echo not in resp:
                continue
            if len(buf) > mark and resp.rstrip().endswith("GXemul>"):
                return True
        return False

    def send(x, timeout=60):
        b = (x + "\n").encode("latin1")
        _mark = len(buf)
        n = 0
        try:
            while n < len(b):
                n += os.write(fd, b[n:])
        except OSError:
            dead[0] = True
            return False
        return wait(mark=_mark, echo=x if x else None, timeout=timeout)

    words = [ins(op, rt, off) for op, rt, off in prog] + [ANCHOR]
    status, badis, vals, steps = "?", [], {}, 0
    if not wait(timeout=120):
        status = "NO-PROMPT"
    else:
        for i, w in enumerate(words):
            send("put w 0x%x, 0x%08x" % (CODE + 4 * i, w))
        for name, val in regs:
            send("%s=0x%x" % (name, val & 0xffffffffffffffff))
        send("pc=0x%x" % CODE)
        status = "SURVIVED"
        if free_run:
            send("breakpoint add 0x%x" % (CODE + 4 * len(prog)))
            mark = len(buf)
            try:
                os.write(fd, b"continue\n")
            except OSError:
                dead[0] = True
            if not wait(mark=mark, timeout=60) or dead[0]:
                status = "DIED" if dead[0] else "NO-BREAK"
            elif ("%016x" % (CODE + 4 * len(prog))) not in buf[mark:] and \
                    ("%08x" % ((CODE + 4 * len(prog)) & 0xffffffff)) not in buf[mark:]:
                status = "NO-BREAK"
            else:
                steps = len(prog)
        else:
            for i, (op, rt, off) in enumerate(prog):
                mark = len(buf)
                if not send("step 1", timeout=30) or dead[0]:
                    status = "DIED"
                    break
                steps += 1
                m = re.search(r"%016x:?\s+%08x\s+([^\r\n<]+)" % (CODE + 4 * i, words[i]), buf[mark:])
                got = re.sub(r"\s+", " ", m.group(1)).strip() if m else "(no step line)"
                if not got.startswith(text(op, rt, off)):
                    badis.append("+0x%02x planted 0x%08x -> %r, expected %r" % (4 * i, words[i], got, text(op, rt, off)))
        if status == "SURVIVED":
            for name in reads:
                got = None
                for _ in range(2):
                    mark = len(buf)
                    if not send("print %s" % name, timeout=30) or dead[0]:
                        break
                    m = re.search(r"(?m)^0x([0-9a-fA-F]+)\s*$", buf[mark:])
                    if m:
                        got = int(m.group(1), 16)
                        break
                vals[name] = got
    try:
        os.write(fd, b"quit\n")
    except OSError:
        pass
    t1 = time.time()
    while time.time() - t1 < 20.0:
        if not rd(0.1):
            break
    try:
        os.close(fd)
    except OSError:
        pass
    rpid, st = 0, None
    t1 = time.time()
    while rpid == 0 and time.time() - t1 < 10.0:
        try:
            rpid, st = os.waitpid(pid, os.WNOHANG)
        except OSError:
            break
        if rpid == 0:
            time.sleep(0.05)
    if rpid == 0:
        try:
            os.kill(pid, signal.SIGKILL)
            _, st = os.waitpid(pid, 0)
        except OSError:
            st = None
    code = os.WEXITSTATUS(st) if st is not None and os.WIFEXITED(st) else None
    cmd = CMD_RE.findall(buf)
    print("  session %-6s %-9s steps=%d/%d exit=%s cmd_once=%d port_once=%d small=%d unimpl=%d" % (
        label, status, steps, len(prog), code, len(cmd), len(PORT_RE.findall(buf)), len(SMALL_RE.findall(buf)),
        len(UNIMPL_RE.findall(buf))))
    for b in badis:
        print("      DISASSEMBLY MISMATCH: %s" % b)
    return {"status": status, "exit": code, "badis": badis, "vals": vals, "cmd": cmd,
            "port": len(PORT_RE.findall(buf)), "small": len(SMALL_RE.findall(buf)), "buf": buf}


RESULTS, CONTROL = [], [True]


def row(name, got, want, note=""):
    ok = got == want
    RESULTS.append(ok)
    print("  %-22s got=%-20s want=%-20s %s  %s" % (name, got, want, "ok" if ok else "FAIL", note))
    return ok


def hx(v):
    return "-" if v is None else "0x%x" % v


def alive(S):
    return "alive" if S["status"] == "SURVIVED" and S["exit"] == 0 else "%s/%s" % (S["status"], S["exit"])


def track(S):
    if S["badis"]:
        CONTROL[0] = False
    return S


#  PORT/DATA program fragments
def sel(reg):
    return ("sw", reg, 0)


def put(reg, op="sw"):
    return (op, reg, 16)


def get(reg):
    return ("lw", reg, 16)


SEED = [sel("zr"), put("s2"),                     # COMMAND = 2: a GET (headless: X1 = Y1 = 0)
        sel("s1"), put("t5"), sel("s2"), put("t6"),   # X1 = 123, Y1 = 77
        sel("zr")]                                # PORT back to COMMAND
READ3 = [get("t2"), sel("s1"), get("t3"), sel("s2"), get("t4")]   # t2 = COMMAND, t3 = X1, t4 = Y1

stub = stub_path()
print("fbctrl_cmd_probe -- binary=%s machine=testmips" % BIN)

C = track(session("C", [sel("s5"), ("sw", "t7", 16), get("t2"), sel("s1"), put("t5"), sel("zr"), put("s2"),
                        sel("s1"), get("t3")], BASE_REGS + [("t7", 0x2a)], ["t2", "t3"], stub))
CONTROL[0] = CONTROL[0] and C["status"] == "SURVIVED" and C["vals"].get("t2") == 0x2a and C["vals"].get("t3") == 0
row("live", hx(C["vals"].get("t2")), "0x2a", "a known value returns through PORT/DATA")
row("devsig", hx(C["vals"].get("t3")), "0x0", "GET_RESOLUTION zeroed X1 (RAM would keep 123)")

REFUSED = [("3", "sw", 3), ("4", "sw", 4), ("sb3", "sb", 3), ("sh4", "sh", 4), ("5", "sw", 5), ("m1w", "sw", 0xffffffff), ("w3", "sd", 0x100000003),
           ("w0", "sd", 0x100000000), ("w1", "sd", 0x100000001), ("w2", "sd", 0x100000002),
           ("m1d", "sd", 0xffffffffffffffff)]
for name, op, v in REFUSED:
    S = track(session("R:" + name, SEED + [put("t1", op)] + READ3, BASE_REGS + [("t1", v)], ["t2", "t3", "t4"], stub))
    shown = v & {"sb": 0xff, "sh": 0xffff, "sw": 0xffffffff, "sd": 0xffffffffffffffff}[op]
    row("ref %s alive" % name, alive(S), "alive", "%s 0x%x at COMMAND" % (op, v))
    row("ref %s cmd" % name, hx(S["vals"].get("t2")), "0x2", "COMMAND keeps 2 (a NOP would read 0, a SET 1)")
    row("ref %s x1" % name, hx(S["vals"].get("t3")), "0x7b", "X1 keeps 123 (a GET would zero it)")
    row("ref %s y1" % name, hx(S["vals"].get("t4")), "0x4d", "Y1 keeps 77")
    row("ref %s once" % name, ",".join(S["cmd"]) or "-", "0x%x" % shown, "one announce, the full value")
    row("ref %s nosmall" % name, S["small"], 0, "no resize attempted")

A0 = track(session("A:nop", SEED + [put("zr")] + READ3, BASE_REGS, ["t2", "t3", "t4"], stub))
row("acc nop cmd", hx(A0["vals"].get("t2")), "0x0", "NOP is stored: COMMAND reads 0")
row("acc nop x1", hx(A0["vals"].get("t3")), "0x7b", "NOP touches nothing else")
row("acc nop quiet", len(A0["cmd"]), 0, "no command announce")
A1 = track(session("A:set", [sel("zr"), put("s1"), get("t2")], BASE_REGS, ["t2"], stub))
row("acc set cmd", hx(A1["vals"].get("t2")), "0x1", "SET_RESOLUTION is stored")
row("acc set ran", A1["small"], 1, "dev_fb_resize() ran: `size too small (0 x 0)` once")
row("acc set quiet", len(A1["cmd"]), 0, "no command announce")
A2 = track(session("A:get", [sel("s1"), put("t5"), sel("s2"), put("t6"), sel("zr"), put("s2")] + READ3,
                   BASE_REGS, ["t2", "t3", "t4"], stub))
row("acc get cmd", hx(A2["vals"].get("t2")), "0x2", "GET_RESOLUTION is stored")
row("acc get x1", hx(A2["vals"].get("t3")), "0x0", "and runs: X1 123 -> 0")
row("acc get y1", hx(A2["vals"].get("t4")), "0x0", "and Y1 77 -> 0")
row("acc get quiet", len(A2["cmd"]), 0, "no command announce")

L = track(session("L", [sel("zr"), put("s3"),                                   # refuse 3: the latch is SET
                        sel("s1"), put("t5"), sel("zr"), put("s2"),             # GET with X1 = 123
                        sel("s1"), get("t3"), sel("zr"), put("zr"), get("t2"),  # X1, then NOP -> COMMAND 0
                        put("s1"), get("t4")],                                  # SET at 0 x 0 -> COMMAND 1
              BASE_REGS, ["t3", "t2", "t4"], stub))
row("latch get x1", hx(L["vals"].get("t3")), "0x0", "GET still runs with the latch set")
row("latch nop cmd", hx(L["vals"].get("t2")), "0x0", "NOP still stored with the latch set")
row("latch set cmd", hx(L["vals"].get("t4")), "0x1", "SET still stored with the latch set")
row("latch set ran", L["small"], 1, "and still runs (the resize line once)")
row("latch once", ",".join(L["cmd"]) or "-", "0x3", "one command announce in the session")

M1 = track(session("M1", [sel("zr"), put("s2"), sel("s1"), put("t5"), sel("zr"), get("t2"), sel("s1"), get("t3")],
                   BASE_REGS, ["t2", "t3"], stub))
row("rdcmd val", hx(M1["vals"].get("t2")), "0x2", "a read of COMMAND returns it")
row("rdcmd noexec", hx(M1["vals"].get("t3")), "0x7b", "and does not execute it (X1 keeps 123)")
M2 = track(session("M2", [sel("s3"), put("s3"), get("t2")], BASE_REGS, ["t2"], stub))
row("x2 three", hx(M2["vals"].get("t2")), "0x3", "3 at X2 is ordinary storage")
row("x2 quiet", len(M2["cmd"]), 0, "no command announce")

T2 = track(session("T2", [sel("zr"), put("s3"), put("s5"), get("t2")], BASE_REGS, ["t2"], stub))
row("two once", ",".join(T2["cmd"]) or "-", "0x3", "two refusals, one announce, the first value")
row("two cmd", hx(T2["vals"].get("t2")), "0x0", "COMMAND keeps its power-on 0")
P1 = track(session("P1", [sel("s6"), put("s4"), get("t2")], BASE_REGS, ["t2"], stub))
row("p1 port", P1["port"], 1, "the refused selector announced once")
row("p1 cmd", ",".join(P1["cmd"]) or "-", "0x4", "and the refused command, on its own latch")
P2 = track(session("P2", [sel("zr"), put("s4"), sel("s6"), get("t2")], BASE_REGS, ["t2"], stub))
row("p2 cmd", ",".join(P2["cmd"]) or "-", "0x4", "command first")
row("p2 port", P2["port"], 1, "then the selector, on its own latch")

F = track(session("F", [sel("zr"), put("s3")], BASE_REGS, [], stub, free_run=True))
row("free alive", F["status"], "SURVIVED", "free-running past the refusal to the anchor")
row("free once", ",".join(F["cmd"]) or "-", "0x3", "fatal() prints while free-running (debug() would not)")

try:
    os.unlink(stub)
except OSError:
    pass
print("FBCMD_CONTROL=%s" % ("OK" if CONTROL[0] else "FAILED"))
print("FBCMD_RESULT=%d/%d" % (sum(RESULTS), len(RESULTS)))
print("FBCMD_DONE")
sys.exit(0 if CONTROL[0] and all(RESULTS) else 1)
```

Its code is the instrument kill table 1 measured (`killtable1_20261018/probe.frozen.py.txt`) with ONE change:
`send()`'s local `mark` renamed `_mark`, the spelling gate 6's fresh-mark census keys on (`#549` made the same rename).
An AST comparison with only that local renamed is equal; the docstring gained the CONTRACT.

## 3. The gate wiring -- the block added to `regress/gate_mips_folds.sh` (gate 16), before its pmax-kernel check

```bash
#  ---------------------------------------------------------------------------------------
#  #567 fbctrlcmdkill: the same device's COMMAND port.  Before #567 a DATA write at COMMAND of any
#  command but NOP (0), SET_RESOLUTION (1) and GET_RESOLUTION (2) -- FILL and COPY among them --
#  reached fbctrl_command()'s default: and ended the emulator, and a wide value was stored into the
#  int cell as its low word, so 0x100000001 ran SET_RESOLUTION.  #567 refuses every other 64-bit
#  value before the store (COMMAND keeps its value, nothing runs) and announces once per device.
#  regress/fbctrl_cmd_probe.py drives real guest sb/sh/sw/sd/lw on an unmodified testmips, like the
#  #549 probe above, so it too runs before the pmax-kernel check.  THE CONTRACT is its header.
#  Kill table 1 (regress/artifacts/fbctrlcmdkill/killtable1_20261018/) built eleven edits, each
#  red, and two null media: on a binary that runs nothing, 15 absence rows read green and the
#  record still parses -- so this block requires CONTROL=OK and pins the score by EQUALITY.
#  `gatedevicesplit` (#498) grows by this second device probe in a CPU gate: recorded, not hidden.
#  The probe prints a row's status AFTER got/want, unlike the #549 probe, so every row count below
#  uses one anchored pattern, FCROW; it counted 95 rows in each of kill table 1's fourteen logs.
FCLOG=$LOGDIR/fbctrl_cmd_probe.log
FCROW='^  [^ ].* got=[^ ]* +want=[^ ]* +'
fcrc=0
python3 -u fbctrl_cmd_probe.py "$PMAX" > "$FCLOG" 2>&1 || fcrc=$?
if [ "$(grep -cx 'FBCMD_DONE' "$FCLOG")" != "1" ] ||
   [ "$(grep -c '^FBCMD_RESULT=' "$FCLOG")" != "1" ] ||
   ! grep -Eq '^FBCMD_RESULT=(0|[1-9][0-9]*)/(0|[1-9][0-9]*)$' "$FCLOG" ||
   [ "$(grep -c '^FBCMD_CONTROL=' "$FCLOG")" != "1" ] ||
   ! grep -Eq '^FBCMD_CONTROL=(OK|FAILED)$' "$FCLOG"; then
    note "fbctrl command probe produced no unique, complete record; last lines follow"
    tail -5 "$FCLOG" | sed 's/^/       /'
    check "fbctrl command probe output parses" "no" "yes"
else
    check "fbctrl command probe output parses" "yes" "yes"
    grep -E "${FCROW}FAIL  " "$FCLOG" | sed 's/^/       /'
    check "fbctrl command probe controls" "$(sed -n 's/^FBCMD_CONTROL=//p' "$FCLOG")" "OK"
    #  As for #549: the probe exits nonzero on a crash OR a red row, a second catcher of a red score.
    check "fbctrl command probe exit 0 (nonzero: a crash or a red row)" "$fcrc" "0"
    fcres=$(sed -n 's/^FBCMD_RESULT=//p' "$FCLOG")
    #  Pinned UNQUOTED under a one-token stem, so check_score_claims.py sees the pin (as #549's).
    check "fbctrl_cmd rows run" "${fcres#*/}" 95
    check "fbctrl_cmd rows correct" "${fcres%/*}" "95"
    check "fbctrl_cmd rows failed" "$(grep -cE "${FCROW}FAIL  " "$FCLOG")" "0"
    #  Reconcile the rows printed with the trailer, and require each row name once (#549 F2).
    check "fbctrl_cmd rows emitted match the trailer total" \
          "$(grep -cE "${FCROW}(ok|FAIL)  " "$FCLOG")" "${fcres#*/}"
    check "fbctrl_cmd ok rows match the trailer count" \
          "$(grep -cE "${FCROW}ok  " "$FCLOG")" "${fcres%/*}"
    check "fbctrl_cmd row names are unique" \
          "$(grep -E "${FCROW}(ok|FAIL)  " "$FCLOG" | sed -E 's/^  (.*[^ ]) +got=.*/\1/' |
             sort | uniq -d | wc -l)" "0"
fi
```

**REPLAYED OFFLINE** (`wiring_20261018/GATE16_REPLAY.out`): the block's own lines (minus the probe launch and its `fcrc=0`
initializer) were sourced with a stub `check()` against every kill-table-1 log, each with its recorded exit status:

```
#567 gate 16 block REPLAYED offline, 2026-10-18 21:55:35: the block's own lines from regress/gate_mips_folds.sh
(g16_extract.sh = FCROW= .. fi, minus the probe launch and its fcrc=0 initializer), sourced with a stub check()
against every kill-table-1 log, fcrc = that leg's recorded exit status; then three hand-made negative controls.
B_gateoff        fcrc=1  checks=9 red=3  fbctrl command probe exit 0 (nonzero: a crash or a red row) got=1 want=0;fbctrl_cmd rows correct got=36 want=95;fbctrl_cmd rows failed got=59 want=0
C_absent         fcrc=1  checks=9 red=4  fbctrl command probe controls got=FAILED want=OK;fbctrl command probe exit 0 (nonzero: a crash or a red row) got=1 want=0;fbctrl_cmd rows correct got=15 want=95;fbctrl_cmd rows failed got=80 want=0
C_bintrue        fcrc=1  checks=9 red=4  fbctrl command probe controls got=FAILED want=OK;fbctrl command probe exit 0 (nonzero: a crash or a red row) got=1 want=0;fbctrl_cmd rows correct got=15 want=95;fbctrl_cmd rows failed got=80 want=0
D10_nolatch      fcrc=1  checks=9 red=3  fbctrl command probe exit 0 (nonzero: a crash or a red row) got=1 want=0;fbctrl_cmd rows correct got=94 want=95;fbctrl_cmd rows failed got=1 want=0
D1_u32           fcrc=1  checks=9 red=3  fbctrl command probe exit 0 (nonzero: a crash or a red row) got=1 want=0;fbctrl_cmd rows correct got=88 want=95;fbctrl_cmd rows failed got=7 want=0
D2_gt1           fcrc=1  checks=9 red=4  fbctrl command probe controls got=FAILED want=OK;fbctrl command probe exit 0 (nonzero: a crash or a red row) got=1 want=0;fbctrl_cmd rows correct got=64 want=95;fbctrl_cmd rows failed got=31 want=0
D3_gt0           fcrc=1  checks=9 red=4  fbctrl command probe controls got=FAILED want=OK;fbctrl command probe exit 0 (nonzero: a crash or a red row) got=1 want=0;fbctrl_cmd rows correct got=60 want=95;fbctrl_cmd rows failed got=35 want=0
D4_ge0           fcrc=1  checks=9 red=4  fbctrl command probe controls got=FAILED want=OK;fbctrl command probe exit 0 (nonzero: a crash or a red row) got=1 want=0;fbctrl_cmd rows correct got=60 want=95;fbctrl_cmd rows failed got=35 want=0
D5_len4          fcrc=1  checks=9 red=3  fbctrl command probe exit 0 (nonzero: a crash or a red row) got=1 want=0;fbctrl_cmd rows correct got=85 want=95;fbctrl_cmd rows failed got=10 want=0
D6_shared        fcrc=1  checks=9 red=3  fbctrl command probe exit 0 (nonzero: a crash or a red row) got=1 want=0;fbctrl_cmd rows correct got=93 want=95;fbctrl_cmd rows failed got=2 want=0
D7_debug         fcrc=1  checks=9 red=3  fbctrl command probe exit 0 (nonzero: a crash or a red row) got=1 want=0;fbctrl_cmd rows correct got=94 want=95;fbctrl_cmd rows failed got=1 want=0
D8_store         fcrc=1  checks=9 red=3  fbctrl command probe exit 0 (nonzero: a crash or a red row) got=1 want=0;fbctrl_cmd rows correct got=84 want=95;fbctrl_cmd rows failed got=11 want=0
D9_anyport       fcrc=1  checks=9 red=4  fbctrl command probe controls got=FAILED want=OK;fbctrl command probe exit 0 (nonzero: a crash or a red row) got=1 want=0;fbctrl_cmd rows correct got=55 want=95;fbctrl_cmd rows failed got=40 want=0
base             fcrc=0  checks=9 red=0  
neg_duprow.log   fcrc=0  checks=9 red=1  fbctrl_cmd row names are unique got=1 want=0
neg_nodone.log   fcrc=0  checks=1 red=1  fbctrl command probe output parses got=no want=yes
neg_rowgone.log  fcrc=0  checks=9 red=2  fbctrl_cmd rows emitted match the trailer total got=94 want=95;fbctrl_cmd ok rows match the trailer count got=94 want=95
neg_nodone.log = base.raw without FBCMD_DONE; neg_rowgone.log = without the 'ref 3 x1' row; neg_duprow.log = 'ref 4 cmd' renamed 'ref 3 cmd'.
GATE16_REPLAY_DONE
```

## 4. The measurements

**The shipped probe's two legs, one instrument** (`pass2_20261018/legs/LEGS.out`, 23:17:48; the probe run is the frozen
copy inlined in section 2, md5 `5d90c732...`; each leg first checked its tree held the named `dev_fbctrl.c`, carried no
sentinel, and had a binary newer than that source):

```
HEAD (/tmp/gx566, HEAD's dev_fbctrl.c; binary md5 25ac428c6592): rc=1 FBCMD_RESULT=36/95 FBCMD_CONTROL=OK last=FBCMD_DONE
FIX  (/tmp/gx567, the fix;            binary md5 004caa290db2): rc=0 FBCMD_RESULT=95/95 FBCMD_CONTROL=OK last=FBCMD_DONE
```

36/95 is the count the PRETABLE predicted for the pre-fix leg, and the draft instrument measured the same before the
`_mark` rename (`draft_20261018/PROBE95_prefix.out`, `PROBE95_postfix.out`).  The witness: 2/12 on HEAD, 12/12 on the fix.

**Kill table 1** (`killtable1_20261018/`, PRETABLE written beforehand at `draft_20261018/PRETABLE.out`, 17:30:58; table
21:34-21:42; the clone restored to the fix, both clearance parts, its sentinel cleared):

```
TABLE1 start 2026-10-18 21:34:44
probe md5 be58950acd681c1d20f4daf0c68a1e9f
base: the draft fix, as built
base         rc=0 FBCMD_RESULT=95/95 FBCMD_CONTROL=OK last=FBCMD_DONE
B_gateoff    rc=1 FBCMD_RESULT=36/95 FBCMD_CONTROL=OK last=FBCMD_DONE
D1_u32       rc=1 FBCMD_RESULT=88/95 FBCMD_CONTROL=OK last=FBCMD_DONE
D2_gt1       rc=1 FBCMD_RESULT=64/95 FBCMD_CONTROL=FAILED last=FBCMD_DONE
D3_gt0       rc=1 FBCMD_RESULT=60/95 FBCMD_CONTROL=FAILED last=FBCMD_DONE
D4_ge0       rc=1 FBCMD_RESULT=60/95 FBCMD_CONTROL=FAILED last=FBCMD_DONE
D5_len4      rc=1 FBCMD_RESULT=85/95 FBCMD_CONTROL=OK last=FBCMD_DONE
D6_shared    rc=1 FBCMD_RESULT=93/95 FBCMD_CONTROL=OK last=FBCMD_DONE
D7_debug     rc=1 FBCMD_RESULT=94/95 FBCMD_CONTROL=OK last=FBCMD_DONE
D8_store     rc=1 FBCMD_RESULT=84/95 FBCMD_CONTROL=OK last=FBCMD_DONE
D9_anyport   rc=1 FBCMD_RESULT=55/95 FBCMD_CONTROL=FAILED last=FBCMD_DONE
D10_nolatch  rc=1 FBCMD_RESULT=94/95 FBCMD_CONTROL=OK last=FBCMD_DONE
null media (c):
C_absent     rc=1 FBCMD_RESULT=15/95 FBCMD_CONTROL=FAILED last=FBCMD_DONE
C_bintrue    rc=1 FBCMD_RESULT=15/95 FBCMD_CONTROL=FAILED last=FBCMD_DONE
--- restore
part 1: src/devices/dev_fbctrl.c == the draft fix
part 2: binary newer than src/devices/dev_fbctrl.c
restored binary md5 004caa290db23c39b01f3c0c086a2545
sentinel cleared
TABLE1 end 2026-10-18 21:42:27
TABLE1_DONE
```

**Its predictions against those scores** (`killtable1_20261018/KILLTABLE1_VS_PRETABLE.out`, verbatim):

```
#567 fbctrlcmdkill -- KILL TABLE 1 against the predictions of ../draft_20261018/PRETABLE.out (mtime 17:30:58; this
table ran 21:34:44 -> 21:42:27, SCORES.txt).  Written 2026-10-18 ~21:5x from the logs in this directory.

INSTRUMENT: probe.frozen.py.txt (md5 be58950a..., the 95-row draft measured in ../draft_20261018/PROBE95_*.out).
BASELINE: the draft fix (../draft_20261018/fix567_draft.diff), in the scratch clone /tmp/gx567: base 95/95 (base.raw).
MUTANTS: mutants/*.diff (each an exact-anchor edit of the fix by mk_mutants567.py.txt; md5s in mutants/MD5.txt).
The frozen driver's name says 2136; the table began at 21:34:44 (the name was chosen before launch, by the clock misread).
RESTORE: part 1 (cmp with the fix) and part 2 (binary newer than the source) both passed; the clone's sentinel cleared.
Row counts were re-derived with an ANCHORED pattern, `^  [^ ].* got=[^ ]* +want=[^ ]* +(ok|FAIL)  `: it counts 95 rows
in every log and its ok count equals FBCMD_RESULT's numerator in all fourteen.

RESULT: ALL ELEVEN MUTANTS RED, and both null media red.  Every KILL prediction held.  Four named-row predictions did not
hold as written.  One failed outright (D4).  One universal claim was wrong for one class (D8).  One null-media
prediction named the wrong gate row.  Several mutants' blast radius was under-predicted.  Each case is below.

mutant        predicted (PRETABLE section 4)                    measured                      verdict
------------  ------------------------------------------------  ----------------------------  -----------------------
B_gateoff     36/95 = the pre-fix leg on the grown instrument   36/95; and row for row        HELD EXACTLY
 (b)                                                            IDENTICAL to PROBE95_prefix.out
                                                                (names, got-values, status, all 95)
C_absent      CONTROL=FAILED, every session NO-PROMPT,          CONTROL=FAILED, 22/22 NO-PROMPT,  RED as predicted;
C_bintrue     "the gate's parse reds"                           15/95 (same 15 for both)          WRONG GATE ROW named
 (c)
D1_u32        w0 cmd (0), w1 cmd (1), w2 x1/y1 (0); w3 refused  88/95: those 4 + w0/w1/w2 once   HELD (+3 once rows)
D2_gt1        acc get cmd/x1/y1, latch get x1                   64/95, CONTROL=FAILED: those 4    HELD on named rows;
                                                                + 27                              blast radius missed
D3_gt0        acc set cmd/ran, latch set cmd/ran + D2's         60/95: D2's 31 + acc set cmd,     HELD (+ acc set quiet)
                                                                acc set ran, acc set quiet,
                                                                latch set cmd
D4_ge0        acc nop cmd, latch nop cmd + D2's/D3's            60/95: THE SAME 35 ROWS AS D3;    NAMED ROWS FAILED
                                                                both NOP rows GREEN               (masked; see below)
D5_len4       ref sb3, ref sh4 die                              85/95: exactly their 10 rows      HELD EXACTLY
D6_shared     p1 cmd, p2 port                                   93/95: exactly those 2            HELD EXACTLY
D7_debug      free once                                         94/95: exactly that 1             HELD EXACTLY
D8_store      ref * cmd (COMMAND reads the truncated value)     84/95: 10 of 11 ref * cmd rows    UNIVERSAL CLAIM WRONG
                                                                + two cmd; `ref w2 cmd' GREEN     FOR ONE CLASS
D9_anyport    x2 three, x2 quiet                                55/95, CONTROL=FAILED: those 2    HELD on named rows;
                                                                + 38                              blast radius missed
D10_nolatch   two once ("0x3,0x5")                              94/95: exactly that, got 0x3,0x5  HELD EXACTLY

THE FOUR THAT DID NOT HOLD AS WRITTEN

1. D4 (`> 2' -> `>= 0': every command refused).  PRETABLE named `acc nop cmd' and `latch nop cmd'.  Both stay GREEN.
   In A:nop and in L the NOP follows a GET that would have put COMMAND at 2 -- and D4 refuses that GET too, so COMMAND
   keeps its power-on 0 and a refused NOP reads exactly like an accepted one (0).  A COMPOUND mutant's second component
   removed the state its first component's rows read.  The rows are not vacuous in general: under a NOP-ONLY refusal
   the GET lands and both rows read 2.  Nothing in table 1 measured that; addendum E2 (../killtable1b_20261018/) does.
   D4 itself is killed by its other 35 rows.

2. D8 (the refused value STORED, execution still skipped).  PRETABLE said `ref * cmd' red.  `ref w2 cmd' stays GREEN:
   w2 = 0x100000002 is stored into the int cell as 2, which IS the previous COMMAND value (the seed's GET).  That one
   row's channel cannot vary under D8 by construction; the class is pinned by the other ten (and by `two cmd', 0x5,
   which the prediction did not name).

3. Null media.  PRETABLE said "the gate's parse reds".  It does not: the probe prints a complete, well-formed record on
   a dead binary (FBCMD_DONE, FBCMD_RESULT=15/95, FBCMD_CONTROL=FAILED), and a parse modelled on gate 16's #549 block
   accepts FAILED as a well-formed value.  The gate reds on its controls row (FAILED, want OK), its exit row (1, want 0)
   and its score rows (15, want 95).  The outcome is as predicted; the gate row named was wrong.
   THE 15 ROWS GREEN ON A DEAD BINARY are absence rows: the eleven `ref * nosmall' (no resize line) and the four
   announce counts `acc nop quiet', `acc set quiet', `acc get quiet', `x2 quiet' (no announce).  Each reads 0 on a
   session that never started, so each depends on the controls row and the score pin to be meaningful -- which is
   why the wiring pins the score by EQUALITY and requires CONTROL=OK (clause (c) by construction, measured here).

4. BLAST RADIUS (D2, D3, D9, and D1's once rows).  Every named row reddened, but D2 and D9 reddened 27 and 38 rows the
   prediction did not name, because the SEED (a GET, X1 = 123, Y1 = 77) and the C controls (0x2a at PORT 5, a GET) go
   through the arm under test.  Under D2 the seed's GET is refused, so every R class reads COMMAND 0 and its first
   announce is 0x2.  Under D9 the X1/Y1 seeds are refused, so every R class reads X1 = Y1 = 0 and its first announce is
   0x7b.  Both also turn CONTROL to FAILED.  Under-predicting a mutant's reach is harmless for a kill; it is recorded
   because a row named for one mutant that is ALSO red under another is shared evidence, not independent evidence.

PRETABLE SECTION 5 -- the channel line's hypothesis, as the carrier asks the first mandated application to CHECK it:
"a row's channel-under-its-mutant is knowable at WRITING time".  Here it HELD for B, D1-D3 and D5-D10: each named row
reddened, except D8's w2, which a writing-time reading could have caught by asking whether the refused value aliases
the previous one.  It FAILED for D4.  D4 refuses three accepted cells at once (NOP, SET, GET), and two of its named
rows sit in sessions whose SETUP issues one of the others (a GET before the NOP).  D3 also refuses two cells (SET, GET)
and held, because its named rows' sessions issue no GET before the SET.  The lesson worth carrying: for a mutant that
changes MORE THAN ONE cell of a partition, read each named row's session for a setup step another changed cell breaks.
```

**Kill table 1b** (`killtable1b_20261018/`, 23:13:18-23:17:48; its addendum `PRETABLE_ADDENDUM_t1b.out` was written at
21:50:25, before the run; same frozen instrument, same baseline; the clone restored to the fix, both clearance parts,
sentinel cleared).  Five mutants, each an exact-anchor edit of the fix, each answering a gap table 1 left:

```
mutant      edit                                                        predicted   measured
E1_gt3      `> GET_RESOLUTION' -> `> GET_RESOLUTION + 1' (FILL accepted) 19 red      76/95 -- the same 19 rows
E2_nopref   the gate also refuses NOP                                    3 red       92/95 -- acc nop cmd 0x2,
                                                                                     acc nop quiet 1, latch nop cmd 0x2
E3_setref   the gate also refuses SET_RESOLUTION                         5 red       90/95 -- the same 5 rows
E4_hoist    the dispatch moved out of the store branch, so a refusal     22 red      73/95 -- ref * x1 and ref * y1,
            re-runs the PREVIOUS command (the seed's GET)                            all 11 classes (0x0)
E5_signed   `(int64_t) idata > GET_RESOLUTION' (negative values pass)    5 red       90/95 -- ref m1d, its 5 rows
```

**Every prediction held, row for row.**  E1 is rule D2's past-the-bound edge in the direction that re-opens the host
kill: `ref 3` and `ref sb3` die, and so do the sessions whose first refusal is 3 (L, T2, F).  E2 and E3 settle table
1's one failed prediction: with only ONE cell refused, the NOP and SET rows that D4 masked are live (the seed's GET now
lands, so a refused NOP leaves COMMAND at 2).  E4 shows the "nothing executes" claim is carried by every R class's
X1/Y1 rows.  E5 shows the sign axis is carried by `m1d` alone -- `m1w` (sw 0xffffffff) arrives zero-extended and is
positive.

**The weekly battery, run on this working tree** (`_scratchpad/nightly/verdict_20261018_231924.txt` and
`battery_20261018_231924.log`; re-triggered by hand after the scheduled 18:00 run died in Modern Standby during gate 3):
`HEAD=6c2840d7`, `TREE_DIRTY=YES` (this round's diff plus other uncommitted work), START 2026-10-18 23:22:00, END
2026-10-19 03:51:19, `RUN_SH_EXIT=0`, **`REGRESS_PASS`, `GATE_COVERAGE=16/16`, passed 16, failed 0, skipped 0.**  Gate 1
rebuilt `build/` from `est/` and `/tmp/gxsec-build` from SEC with the fix in both (18 checks, including the est/SEC
divergence check); gate 6 passed on the re-derived census pins; gate 16 ran this round's block on `build/gxemul`
(CONDENSED from the log, lines 6489-6542: verbatim, except that the 30 fold-probe lines between `fold probe completed`
and the gate's PASS line are omitted):

```
## GATE: gate 16: MIPS fold witness (#388)
  ok   fbctrl probe output parses                           yes
  ok   fbctrl probe controls                                OK
  ok   fbctrl probe exit 0 (nonzero: a crash or a red row)  0
  ok   fbctrl_port rows run                                 117
  ok   fbctrl_port rows correct                             117
  ok   fbctrl_port rows failed                              0
  ok   fbctrl_port rows emitted match the trailer total     117
  ok   fbctrl_port ok rows match the trailer count          117
  ok   fbctrl_port row names are unique                     0
  ok   fbctrl command probe output parses                   yes
  ok   fbctrl command probe controls                        OK
  ok   fbctrl command probe exit 0 (nonzero: a crash or a red row) 0
  ok   fbctrl_cmd rows run                                  95
  ok   fbctrl_cmd rows correct                              95
  ok   fbctrl_cmd rows failed                               0
  ok   fbctrl_cmd rows emitted match the trailer total      95
  ok   fbctrl_cmd ok rows match the trailer count           95
  ok   fbctrl_cmd row names are unique                      0
  ok   fold probe completed (result line present)           yes
gate 16: MIPS fold witness (#388): PASS (35 checks)
```

## 5. The census pins, the score manifest and the wiring manifest

Gate 6 (`gate_hygiene.sh`) pins how many pty probes lie in the tree and how many are PROMPTLESS (send without waiting
for the debugger prompt).  Re-deriving them for `#567`'s probe with `tools/derive_hygiene_pins.sh` showed two moves,
not one: the census read 76 against a pin of 74, and the promptless census 44 against 43.  The second probe is
`regress/sgi_mte_decline_probe.py`, committed by `#564` (`e7fc97e6`) THIS MORNING without moving either pin -- so this
week's battery would have reddened gate 6 whatever `#567` did -- and it is PROMPTLESS (fixed waits: a 1.5 s settle,
0.22 s between commands).  `--write` REFUSES while a promptless probe is neither grandfathered nor prompt-detecting, so
`#567` grandfathered it with the tool (`--grandfather sgi_mte_decline_probe.py`, the 2026-09-19 precedent: twenty
promptless probes grandfathered, "converting a probe's readiness is its own round"), then ran `--write`: 76 and 26.
After it, all eight censuses equal their pins.  Two rows are filed beside it: `ptyprobepins` (a precommit check, so a
commit cannot strand the pins again) and `sgimtereadiness` (the conversion).

```diff
diff --git a/regress/gate_hygiene.sh b/regress/gate_hygiene.sh
index ba588738..f71ba52e 100644
--- a/regress/gate_hygiene.sh
+++ b/regress/gate_hygiene.sh
@@ -385,7 +385,7 @@ check "readiness: no unrecognised endswith spelling" "$unknown" "$EXPECT_UNKNOWN
 #  and reds THREE rows -- this one, the promptless count and the promptless-names row -- because all three are
 #  grandfathered names that exist only in the working tree (measured on a copy with them removed: 70/73, 40/43,
 #  names gone=the three).  Written by `tools/derive_hygiene_pins.sh --write`, never by hand. ***
-EXPECT_PTY_PROBES=74
+EXPECT_PTY_PROBES=76
 #  *** AND THE SAME PROBE BROKE A SECOND CENSUS IN THIS FILE, WHICH pass 11's OWN
 #  REPAIR DID NOT FIX.  Found by the codex seat reviewing that repair. ***
 #
@@ -419,8 +419,9 @@ gdrom_cond_probe.py sgi_re_width_probe.py
 sgi_de_width_probe.py sgi_re_unmapped_probe.py
 alpha_harness_probe.py alpha_pfnoffset_probe.py alpha_swpctx_v0_probe.py alpha_tbi_probe.py arm_bfx_width_probe.py landisk_aux_probe.py lca_badval_probe.py lca_confbus_probe.py lca_confwidth_probe.py lca_irqstub_probe.py lca_irqstub_uart_probe.py lca_isalane_probe.py lca_widewrite_probe.py maple_dmaaddr_probe.py pcc2_c040_probe.py sgi_mte_fill_probe.py sgi_re_colourdefault_probe.py sgi_re_randompixel_probe.py sgi_re_rgb_probe.py wdc_altdigin_probe.py
 arm_msrmode_probe.py lca_isaphys_probe.py
-crime_width_probe.py"
-#  hygienecensus: tools/derive_hygiene_pins.sh --grandfather appended THREE blocks to the list above; they are
+crime_width_probe.py
+sgi_mte_decline_probe.py"
+#  hygienecensus: tools/derive_hygiene_pins.sh --grandfather appended FOUR blocks to the list above; they are
 #  named here by their FIRST NAME, never by position, because the next --grandfather appends another.
 #  The block beginning `alpha_harness_probe.py` (derived 2026-09-19): 20 PROMPTLESS pty probes committed
 #  between 2026-09-05 and 2026-09-18 that moved NO PIN -- they moved the promptless census (20 -> 40) and the
@@ -433,9 +434,16 @@ crime_width_probe.py"
 #  (2026-09-23, OWNER RULING): arm_msrmode_probe.py (armmsrmodekill) and lca_isaphys_probe.py (#540).  The
 #  block beginning `crime_width_probe.py` (2026-09-23, pass 2 of this round, under the same ruling's
 #  principle): crime_width_probe.py (#529), hidden from this census by a comment until pass 2 stopped the
-#  classifier reading full-line comments (it reads tokens since the F2 repair).  All three are UNTRACKED and lying
+#  classifier reading full-line comments (it reads tokens since the F2 repair).  All three were UNTRACKED and lying
 #  in the tree, named so the census passes on
-#  the tree the weekly battery runs.  Re-derive, never hand-edit: `bash tools/derive_hygiene_pins.sh` (report),
+#  the tree the weekly battery runs.  (2026-10-18: crime_width_probe.py was committed by 7440e129 and
+#  arm_msrmode_probe.py by 4f908ad5; lca_isaphys_probe.py still lies untracked.)  The block beginning
+#  `sgi_mte_decline_probe.py` (2026-10-18, #567): #564 (e7fc97e6) committed that promptless probe -- fixed
+#  waits, no readiness read -- and moved neither census, so this gate would have reddened at the next battery;
+#  #567, adding its own pty probe, could not re-derive its pins while it stood, because --write refuses a
+#  promptless probe that is neither grandfathered nor prompt-detecting.  Grandfathered on the 2026-09-19
+#  precedent; converting its readiness is its own round.
+#  Re-derive, never hand-edit: `bash tools/derive_hygiene_pins.sh` (report),
 #  `--grandfather NAME...` / `--release NAME...`, then `--write`.
 
 #  *** THIS WAS THE THIRD POPULATION AND THE F2 EDIT MISSED IT.  Found by the agy seat
@@ -596,7 +604,7 @@ fi
 #  send() spelled the fresh mark `mark=mark`, which the fresh-mark census does not read, so that one said
 #  23 and the three #392 counts DISAGREED at HEAD.  The probe's rename to `_mark` (same change) makes the
 #  three agree; the deriver refuses to write while they disagree, which is why the rename precedes the pin. ***
-EXPECT_CONVERTED=25
+EXPECT_CONVERTED=26
 #  One helper for all three, so they agree on WHAT they look at.  The first draft
 #  used py_code() for the anchored count and a raw grep for the other two, which
 #  meant a comment mentioning the echo guard would have inflated one count and not
```

```diff
diff --git a/tools/precommit_check.sh b/tools/precommit_check.sh
index c157ab43..eb382bf6 100644
--- a/tools/precommit_check.sh
+++ b/tools/precommit_check.sh
@@ -353,7 +353,9 @@ elif out=$(python "$SCORECHK" 2>&1); then
 	#  the stem, and only a docstring at regress/<stem>_probe.py or regress/<stem>.py; no comment line
 	#  names ip30_abort and the probe lives under artifacts/, so for this pin it checks no prose -- only
 	#  the pin is counted.
-	SCORE_CLAIMS_MANIFEST=35
+	#  RAISED 35 -> 36 ON 2026-10-18, DELIBERATELY.  One newly gated probe: fbctrl_cmd_probe.py
+	#  (#567, pinned UNQUOTED in gate_mips_folds.sh at 95 rows).
+	SCORE_CLAIMS_MANIFEST=36
 	_spinned=$(printf '%s\n' "$out" | sed -n 's/^SCORE_CLAIMS_PINNED=//p')
 	if [ -z "$_spinned" ]; then
 		bad "check_score_claims printed no SCORE_CLAIMS_PINNED line -- the count cannot be pinned"
```

`tools/pipeline/check_probe_wiring.py`, this round's one line (beside `#549`'s entry):

```
    "fbctrl_cmd_probe.py":         (CLASS_DETECTOR, "#567 fbctrl COMMAND refusal"),
```

`check_score_claims.py` now reports `SCORE_CLAIMS_PINNED=36` and passes (the manifest moves 35 -> 36 with it).

## 6. Questions -- answer each

1. **The premise audit.**  Each of these is load-bearing; tell me which is false, with evidence.
   * Every DATA value a guest can write at COMMAND reaches the compare as the FULL access value, ZERO-extended
     (`memory_readmax64(cpu, data, len)` for sb/sh/sw/sd), so `idata > 2` on `uint64_t` refuses everything except
     0, 1 and 2 at every width.  Is any access width or path able to present a value the compare misreads?
   * After the fix COMMAND can only ever hold 0, 1 or 2 (power-on 0 from `memset`; nothing else writes
     `port[DEV_FBCTRL_PORT_COMMAND]`; GET_RESOLUTION writes X1/Y1 only), so `fbctrl_command()`'s `default:` is
     unreachable and kept only as a tripwire.  Is there a writer I missed?
   * The read path is unchanged: a read of COMMAND returns the stored int, and a refused write never changes it.
   * `B_gateoff` (the gate removed) is HEAD's DATA arm byte for byte, so it is floor clause (b) -- and its 95 rows are
     row-for-row identical to the pre-fix leg.  Is the mutant really the removed defect, at every fixed site?
2. **The smallest edit that breaks this and still passes** -- name it, and the row you expect to stay green.
3. **Option-set completeness**: pass 1 settled member 3.  Is there evidence in THIS diff that changes that?
4. **The floor's clause (d), DEPENDS-ON.**  My enumeration of the predicates the fix depends on, each with its measured
   mutant: the port test (D9); the compare's width (D1), sign (E5), bound moved down (D2, D3, D4) and up (E1); the latch
   (D6 shared, D10 never set); the announce level (D7); the store order (D8); the dispatch's placement (E4); a width
   qualifier (D5).  Joint cells are disclosed, not rowed -- the latch SET crossed with a wide alias is the contract's
   NOT CLAIMED (0).  **Which predicate, or which cell of one, has no measured mutant?**
5. **CHANNEL.**  Two rows were found unable to vary under a named mutant: D4's NOP rows (masked, because D4 also refuses
   the GET that seeds those sessions -- E2 measures the NOP cell alone) and `ref w2 cmd` under D8 (w2 truncates to the
   previous COMMAND value, 2).  Is there a third?
6. **The gate block.**  Can any of its nine checks pass on a run that should fail?  It counts rows with one anchored
   pattern because this probe prints a row's status AFTER got/want.  (The replay above is my evidence; find its hole.)
7. **The census repair inside `#567`.**  Folding `#564`'s stranded pins into this round's diff, because the deriver will
   not write `#567`'s pins while they stand -- right, or should it be its own commit, landed first?
8. **WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?**  I accepted FIVE: (a) D4's two non-varying NOP rows are not a floor
   breach, because E2 measures that cell alone; (b) `ref w2 cmd` under D8 is not a breach, because ten classes and
   `two cmd` pin the store; (c) the 15 rows green on a dead binary are acceptable because the gate requires CONTROL=OK
   and pins the score by equality -- clause (c) MEASURED at `killtable1_20261018/C_absent.raw` and `C_bintrue.raw`;
   (d) grandfathering `sgi_mte_decline_probe.py` rather than converting it; (e) adding a second device probe to gate 16,
   a CPU gate, compounding the recorded `gatedevicesplit` debt.  Be harder on any of these that you would have argued for.

If, while verifying a claim, you found something ELSE -- say so.

**Answer format:** open with your token, then ONE line `VERDICT: SHIP | SHIP WITH CHANGES | DO NOT SHIP -- <one line>`,
then `FLAG:` lines for any false premise (with evidence: a grep anchor or a construct name), then answers to 1-8.
