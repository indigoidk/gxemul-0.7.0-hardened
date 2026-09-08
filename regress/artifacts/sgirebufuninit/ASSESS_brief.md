# sgirebufuninit -- an uninitialised buffer whose length the guest chooses

## 0. SCOPE, and what this brief does NOT ask for

Read `GXEMUL-SEC/src/devices/dev_sgi_re.c` -- `horrible_getputpixel()` and its callers. Please avoid
`regress/artifacts/` and `tools/pipeline/ledger.json`.

Tree: `GXEMUL-SEC/src/`. Ignore the pristine 2021 `src/` at the project root.

*** NO MUTANT, NO EVASION, NO GUEST SEQUENCE IS WANTED. *** This is a source-analysis and
disposition question about code that exists. (You refused a brief of mine earlier tonight that asked
for an edit which defeats a detector; nothing here does.)

## 1. THE FILED CLAIM -- a claim, not a premise

> *"`horrible_getputpixel()`: `uint8_t buf[8]` is never initialised and the guest picks how many of
> its bytes are used -- uninitialised host stack reaches guest-visible memory on PUT and `*color`
> on GET."*

**Please do not simply ratify.** You have refuted premises of mine on five briefs tonight, which is
the behaviour I want.

## 2. SETTLED PREMISES -- verified by me this session; challenge any that look wrong

* `uint8_t buf[8];` is declared with no initialiser inside the function.
* `int bufdepth = 1 << ((mode >> 8) & 3);` so **the guest chooses 1, 2, 4 or 8** via a register it
  writes.
* the PUT switch fills `buf[0]` only for `DE_MODE_TYPE_CI`, and `buf[0..3]` for RGB, RGBA and ABGR.
  **No arm writes `buf[4..7]`.**
* the transfer is `cpu->memory_rw(cpu, cpu->mem, tileptr + ofs, buf, bufdepth, MEM_WRITE, ...)`.
* on the GET side the same `buf` is filled by a `MEM_READ` of `bufdepth` bytes and then recombined;
  the `default:` arm builds a 32-bit value from `buf[0..3]`.
* **there is NO validation of the mode register** -- `DEVICE_ACCESS(sgi_de)` stores it raw, its own
  comment saying *"Treat all registers as read/write, by default"*, and `draw_primitive` reads it
  straight back.

## 3. QUESTIONS -- VERDICT LINE FIRST

**Q1. Which (mode, bufdepth) combinations actually send uninitialised bytes to guest memory?**
Enumerate rather than assert: for each colour type and each of the four bufdepths, how many of the
`bufdepth` bytes were written by the switch. I want the count of reachable combinations that leak,
derived from the code.

**Q2. Same question on the GET side.** The read fills `bufdepth` bytes, but the recombination reads
`buf[0..3]` in several arms. **If `bufdepth < 4`, are `buf[2]`/`buf[3]` stale from a previous call
or uninitialised on the first?** Say which, and whether the value reaches `*color` and thence the
caller.

**Q3. What is ACTUALLY exposed?** This is a device model in a userland emulator: the bytes are this
process's own stack, not another process's memory. **Say plainly whether this is (a) a
guest-visible NONDETERMINISM defect, (b) an information-exposure defect, or (c) both** -- and do not
inflate it. The project ranks by measurable consequence, and "uninitialised" alone is not a severity.

**Q4. What is the smallest correct fix, and does it cost anything?** A `memset` at declaration is
the obvious candidate. **Does it change behaviour for any combination that currently works
correctly?** That question matters more than the fix -- a repair that alters a correct path is a
behavioural change wearing a UB-fix's clothes.

**Q5. Is this ONE round with `sgirandomcolour`?** That row is the same switch's `default:` arm
filling `buf` with `random()`. A five-seat panel ruled them **two rounds**, on the ground that one
oracle cannot distinguish a CI/depth-8 regression from a YCRCB regression. **Do you agree?** And
note the trap that panel named: **zero-initialising `buf` at its declaration would silently fix half
of `sgirandomcolour` too**, which is how one round quietly becomes two.

**Q6. What observable distinguishes fixed from unfixed?** Not a guest sequence -- name the channel.
If the honest answer is that uninitialised stack often happens to be zero, so a single run cannot
tell, say so; that shapes the detector and is worth more than a confident oracle that cannot fail.
