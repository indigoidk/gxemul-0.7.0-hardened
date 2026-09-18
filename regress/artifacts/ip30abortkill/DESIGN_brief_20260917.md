# `ip30abortkill` -- **FIX DESIGN, PASS 1.**  Four `abort()` in one file, three different shapes.
## VERDICT LINE FIRST.  TREE: `GXEMUL-SEC/` under `C:/DocumentNoSnc/CC/GXEMUL`.
## There are THREE pristine-2021 `src/` copies elsewhere under the project root -- ignore them.

## *** DO NOT RATIFY.  Check the premises, not just the derivations. ***

A recent panel here had seven of nine seats confirm a premise a brief stated wrongly.  Every
load-bearing claim below was re-derived locally before this brief was written, but state
plainly any you cannot settle, and attack the ones you can.

## S1 -- THE DEFECT, MEASURED BY READING (not yet by running)

`src/devices/dev_sgi_ip30.c` carries **four** `abort()` calls.  `abort()` contains no `exit(`,
which is why three sweeps of this queue walked past all of them.

    :78   DEVICE_TICK(sgi_ip30)   if (d->imask0 & ((int64_t)1<<50)) { fatal(...); abort(); }
    :127  case 0x10020  Set ISR    d->isr = idata;  fatal(...); abort();
    :135  case 0x10028  Clear ISR  d->isr &= ~idata; fatal(...); abort();
    :145  case 0x10030  ISR write arm             fatal(...); abort();

Reachability facts, all verified locally:

  * `DEV_SGI_IP30_LENGTH` is `0x80000` (`:44`), registered at `:387` with **`DM_DEFAULT`** --
    so the debugger `dump` BYPASSES the handler and only a guest instruction reaches it.
  * `machine_sgi.c:417` adds the device at `sgi_ip30 addr=0x0ff00000`.
  * `machine_sgi.c:744` -- `machine_entry_add_subtype(me, "IP30", 30, "ip30", "octane", NULL)`.
    The subtype is ADVERTISED.
  * `machine_add_tickfunction` at `:402`, so the tick path is live.
  * `0x10020`, `0x10028`, `0x10030` are all inside the window.
  * **NOT IP22:** `dev_sgi_ip22.c:315`/`:339` are the same shape but `machine_sgi.c` aborts
    BEFORE `dev_sgi_ip22_init`, so those are construction (`ctorabortclass`), not a guest path.

## S2 -- TWO FACTS I FOUND BY READING THE ARM, AND THEY CHANGE THE FIX

**(A) `case 0x10020` HAS NO `writeflag` TEST AND RUNS `d->isr = idata;` FIRST.**  `idata` is
initialised to 0 at `:87` and assigned ONLY under `if (writeflag == MEM_WRITE)` at `:89-90`.

> So a guest **LOAD** at `0x0ff10020` **ZEROES THE INTERRUPT STATUS REGISTER** and *then*
> aborts.  Guest-state corruption AND host death in one arm, on a path the `Set ISR` comment
> invites a reader to treat as write-only.

`case 0x10028` shares the missing test (`d->isr &= ~idata` is a no-op at `idata == 0`, then
aborts).  **`case 0x10030` IS writeflag-tested** and its reads return `d->isr` correctly.
**The three arms are NOT uniform.**

**(B) THE TICK ABORT IS ARMED BY A LEGAL WRITE TO AN IMPLEMENTED REGISTER.**  `case 0x10000`
(`:99-105`) implements `imask0` and ACCEPTS the write; `:74-78` then aborts whenever
`d->imask0 & (1<<50)`.  The announcing access SUCCEEDS and the host dies LATER, out of band,
from `DEVICE_TICK`, with no access in flight.

## S3 -- THE OPTION SET (seven members), and what I believe -- ATTACK IT

**1 DELETE · 2 DECLINE silent · 3 DECLINE + LATCHED ANNOUNCE · 4 ACCEPT · 5 FAULT ·
6 BACKED ACCEPT · 7 IMPLEMENT**

My reading is **member 7 IMPLEMENT**, because every one of the four sites carries its intended
model beside it as a commented-out `cpu_interrupt(...)` call -- i.e. a STUBBED PATH with no
predicate refusing anything, which is the tell member 7 was minted for.  Fallback is **member
3** if the interrupt rewrite is out of scope.

**Questions, and I expect to be wrong on at least one:**

**Q1.**  Is member 7 actually available here, or does re-enabling `cpu_interrupt(cpu, 8)` on
IP30 require interrupt plumbing that does not exist?  **Check what `cpu_interrupt` does on this
machine and whether the IP30 interrupt model is wired at all.**  The carrier's own rule is that
a member must be checked for AVAILABILITY on this CPU before it is chosen -- member 5 FAULT was
found unavailable on Alpha exactly that way.

**Q2.**  Member 5 FAULT: MIPS *does* dispatch an exception on a failed device access, so FAULT
is architecturally available -- **but `abort()` fires before any `return 0`, so it is inert as
the code stands.**  Is that a reason to reject it, or a reason it is the cheapest fix?

**Q3 -- THE ONE I THINK MATTERS MOST.**  **Is the missing `writeflag` test a SEPARATE defect
from the abort, owing its own fix and its own row?**  De-fatalising `0x10020` without adding
the test leaves a guest LOAD still zeroing the ISR -- silently, with the host now alive to
carry on with corrupted state.  **That is the `asicindexcase` shape: removing the kill converts
a loud death into a quiet corruption.**  Say whether the fix MUST carry both.

**Q4 -- HOW DO YOU DECLINE A TICK?**  Members 1-7 all presume an ACCESS with a value to refuse.
The `:78` abort is in a tick function with no access in flight.  **What is the right disposition
for a periodic callback that aborts on a state the guest legally set?**  Name it; if the option
set has no member that fits, say so plainly -- the set has been grown three times by seats that
went looking in the tree rather than reasoning.

**Q5 -- THE DE-ESCALATION CLAUSE.**  A fatal->survive fix DELETES the accidental tripwire.  What
ACCEPT-SIDE rows does a detector shipping with this fix owe -- per predicate that used to gate
death?  Note `0x10000` (imask0) is already implemented and accepted, so it may already be an
accept row rather than a new one.

**Q6.**  Grep the fork for the SIBLING disposition: how do the other `dev_sgi_*.c` files handle
an unimplemented interrupt-controller register?  The option-set rule's own advice is that the
tree's precedents are part of the design space, and members 4, 5 and 6 were ALL found that way
and none by argument.

## S4 -- WITNESS, and it is not yet built

Reachability is CONFIRMED BY READING and **NOT MEASURED**.  I am attempting a rung-3 probe in
parallel with this brief -- one guest `lw`/`sw` at `0xffffffffaff10020` on unmodified
`-E sgi -e ip30` (KSEG1: `0xa0000000 | 0x0ff10020`; the file's own `:113` comment quotes the
PROM complaining at `0xffffffffaff10018`, which is how I derived the mapping).

**If you can see a reason that probe will NOT reach the arm -- no boot image, the PROM never
getting that far, a CPU that will not start without one -- say so, because that changes the
round from "fix it" to "document it".**

## S5 -- HONESTY CLAUSE

**"Member N, here is why, and the writeflag test is/is not separate" is the answer.**  If you
cannot settle availability from the files, say which file you would need.  An honest "I cannot
tell whether the interrupt model is wired" is worth more than a confident member choice that
owes plumbing nobody has costed.
