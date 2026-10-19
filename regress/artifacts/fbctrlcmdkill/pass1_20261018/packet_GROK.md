**Your token: `GROK_FBCMD_P1_20261018`** -- open your answer with it.

# `fbctrlcmdkill` (HIGH) -- pass 1, the design brief: `dev_fbctrl.c` ends the emulator on any framebuffer-controller command other than 0-2

**Please do not simply ratify** -- a recent panel had seven of nine seats confirm a premise its brief stated wrongly.
Check the premises, not just the derivations.  **The tree under review is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`
(`src/devices/dev_fbctrl.c`, `src/include/testmachine/dev_fb.h`); ignore any other `src/` under the project root**
(pristine 2021 upstream copies).  READ-ONLY.

## The defect, MEASURED test-first (rung 3, unmodified `-E testmips`)

`fbctrl_command()`'s `default:` calls `fatal()` then `exit(1)` for every command other than NOP (0), SET_RESOLUTION (1)
and GET_RESOLUTION (2).  A guest reaches it with ONE DATA write while the COMMAND port (0) is selected -- port 0 is the
power-on selector.  `machine_test.c` installs `fbctrl addr=0x12f00000` on every test machine.  The witness
(`fbctrl_cmd_witness.py.txt`, run on HEAD's binary, both build-clearance parts checked):

```
fbctrl_cmd_witness -- binary=/tmp/gx566/gxemul machine=testmips
  session C   SURVIVED  steps=9/9 exit=0 unimpl_msgs=0
  live           got=0x2a         want=0x2a         ok  a known value returns through PORT/DATA
  devsig         got=0x0          want=0x0          ok  GET_RESOLUTION zeroed X1 (RAM would keep 123)
  session K3  DIED      steps=1/3 exit=1 unimpl_msgs=1
  cmd 3          got=DIED         want=SURVIVED     FAIL  DATA write of 0x3 at COMMAND (sw)
  cmd 3 exit     got=1            want=0            FAIL  the child's exit status after quit
  session K4  DIED      steps=1/3 exit=1 unimpl_msgs=1
  cmd 4          got=DIED         want=SURVIVED     FAIL  DATA write of 0x4 at COMMAND (sw)
  cmd 4 exit     got=1            want=0            FAIL  the child's exit status after quit
  session K5  DIED      steps=1/3 exit=1 unimpl_msgs=1
  cmd 5          got=DIED         want=SURVIVED     FAIL  DATA write of 0x5 at COMMAND (sw)
  cmd 5 exit     got=1            want=0            FAIL  the child's exit status after quit
  session K-1 DIED      steps=1/3 exit=1 unimpl_msgs=1
  cmd -1         got=DIED         want=SURVIVED     FAIL  DATA write of 0xffffffff at COMMAND (sw)
  cmd -1 exit    got=1            want=0            FAIL  the child's exit status after quit
  session K2^32+3 DIED      steps=1/3 exit=1 unimpl_msgs=1
  cmd 2^32+3     got=DIED         want=SURVIVED     FAIL  DATA write of 0x100000003 at COMMAND (sd)
  cmd 2^32+3 exit got=1            want=0            FAIL  the child's exit status after quit
FBCMDW_CONTROL=OK
FBCMDW_RESULT=2/12
FBCMDW_DONE
```

The last session is the width path: `d->port[]` is `int`, so `sd 0x100000003` stores 3 and dispatches FILL.  By the same
truncation `0x100000001` would run SET_RESOLUTION -- a wide write executes a command the guest did not write.

## The enclosing code, in full (`src/devices/dev_fbctrl.c` at HEAD; every exit path and the common tail)

```c
struct fbctrl_data {
	struct vfb_data *vfb_data;
	int		current_port;
	int		port[DEV_FBCTRL_NPORTS];
	int		warned_port;	/* #549: the refused-selector announce */
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
		else {
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

`src/include/testmachine/dev_fb.h`, the command block:

```c


/*
 *  Controller commands:
 */

/*  Do nothing.  */
#define	DEV_FBCTRL_COMMAND_NOP				0

/*  Set resolution to X1 x Y1.  */
#define	DEV_FBCTRL_COMMAND_SET_RESOLUTION		1

/*  Get current resolution into X1, Y1.  */
#define	DEV_FBCTRL_COMMAND_GET_RESOLUTION		2

/*  TODO:  */
#define	DEV_FBCTRL_COMMAND_FILL				3
#define	DEV_FBCTRL_COMMAND_COPY				4


#define	DEV_FBCTRL_MAXY(x)	(((DEV_FBCTRL_ADDRESS-DEV_FB_ADDRESS) / 3) / x)

#endif	/*  TESTMACHINE_FB_H  */
```

## SETTLED PREMISES (recorded resolutions; each a seat can build an if-then on)

* `fatal()` prints and RETURNS -- `src/core/debugmsg.c`'s `fatal()` has no early-out and no exit; `#549`'s 117-row
  detector rests every refusal row on it.
* The house warn-once idiom is ONE latch bit per device instance and per distinct MESSAGE, with a `(once)` marker in the
  message (`#549`'s `warned_port` is this device's existing one, for the refused-selector message).
* `#549` (8ea26abb) refused an out-of-range PORT selector, kept the previous one, and announced once per device, comparing
  all 64 bits of `idata` -- `regress/fbctrl_port_probe.py`, 117 rows, gated.

## Premises I am NOT sure of -- check them

* The bug file says `dev_fb.h` "DOCUMENTS" FILL (3) and COPY (4).  As quoted above it defines two constants under a bare
  `TODO:` and gives them no port semantics.  Is there any semantics anywhere in the tree (or in a test program) that would
  let FILL/COPY be implemented rather than declined?
* I believe no guest in the tree's test programs issues command 3 or 4 -- check.

## Options (the member set; name a member it lacks)

1 DELETE (the kill only, falling through silently) · 2 DECLINE (silent) · 3 DECLINE + LATCHED ANNOUNCE (a new
`warned_cmd` bit, `(once)`) · 4 ACCEPT (n/a: no value computed) · 5 FAULT (n/a on MIPS for an accepted store?) ·
7 IMPLEMENT FILL/COPY (a feature: the owner's scope is fixes).  **My draft: 3** -- unknown commands, FILL and COPY
declined and announced once per device; NOP, SET_RESOLUTION and GET_RESOLUTION unchanged.

## Questions (answer each)

1. **Which member, and why?**  Is one announce for all refused commands right, or do FILL/COPY ("unimplemented") and an
   unknown value ("not a command") need distinct messages -- and therefore distinct latch bits?
2. **The width path.**  Should the dispatch decide on the FULL `idata` (refusing `0x100000003`, as `#549` refused wide
   selectors), or on the stored `int`?  And what should port 0 hold after a refused command -- the refused value
   (truncated), the previous command, or nothing changed?  What does a guest READ of COMMAND then return?
3. **The detector.**  Rows owed by the floor and the de-escalation clause: survival rows per refused class (3, 4, an
   unknown positive, a negative, a wide value), the announce count (two refusals, one announce), and ACCEPT rows for 0, 1
   and 2 -- the old `exit(1)` made a guard that grew (say `cmd > 2` -> `cmd > 1`) self-announcing; after the fix it would
   silently decline GET_RESOLUTION.  Extend `regress/fbctrl_port_probe.py` (gated, 117 rows -- its contract then grows)
   or ship a new probe?  Which channel distinguishes each row's mutant?
4. **Scope.**  `fbctrloffkill` (MED) is the same file's `DEVICE_ACCESS` `default:` -- `exit(1)` on any offset other than
   0x00/0x10.  Same device, same class: does it join this round under the reopening rule (same detector, no new
   oracle), or stay its own?
5. **Which of my premises or my draft is wrong?**

Answer format: open with your token, then ONE line `VERDICT: <member> -- <one line>`, then `FLAG:` lines for any false
premise (with `file:line` evidence), then short answers to 1-5.
