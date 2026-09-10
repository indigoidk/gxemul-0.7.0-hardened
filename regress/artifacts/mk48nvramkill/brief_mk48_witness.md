# `mk48nvramkill` -- BUILD THE RUNG-3 WITNESS, or report honestly that you cannot

Open your answer with `VERDICT:` on its own first line, then the liveness token
`OPUS_MK48_WITNESS_20260910`, then a VERBATIM quote of the **third** line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`.

This is ordinary robustness testing of a device model in an emulator written in C99. **The tree under
review is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`** -- three unrelated 2021-vintage copies of this
project sit elsewhere under the project root, so line numbers off by hundreds mean you are reading one of
those.

## THE DEFECT, stated so you can refute it

`src/devices/dev_mk48txx.c` models the MK48T08 clock/NVRAM chip. Grep anchor for the site:
`default:if (writeflag == MEM_READ)`.

The device is registered for `MK48TXX_LEN` = `MK48T08_CLKSZ` = **8192** bytes, so `relative_addr` spans
`[0, 0x2000)`. An early accept block passes everything OUTSIDE
`[MK48T08_CLKOFF, MK48T08_CLKOFF + MK48TXX_ISEC)` straight to the RAM path with a `goto ret`. With
`MK48T08_CLKOFF` = `0x1ff0` and `MK48TXX_ISEC` = `9`, the `switch` is reached for exactly the nine offsets
`0x1ff0..0x1ff8` -- and it holds exactly ONE case, `MK48T08_CLKOFF + MK48TXX_ICSR` = `0x1ff8`.

**So the eight offsets `0x1ff0` through `0x1ff7` fall to `default:` and call `exit(1)`.**

`src/machines/machine_mvme88k.c` attaches the device unconditionally at **`0xfffc0000`**, in the same
block that attaches the PCC2 SCSI controller. So the eight fatal offsets should be at guest physical
`0xfffc1ff0` .. `0xfffc1ff7`.

**Please do not simply ratify this.** Check the constants, the registration length and the attach address
yourself; if any of them is different from what I have written, the whole round changes.

## WHAT I AM ASKING FOR

**A RUNG-3 WITNESS: a real guest access through real address decode and real `memory_rw`, on an
UNMODIFIED in-tree machine description.** This project's ladder is explicit that a `#include`/direct-call
harness is NOT a reproduction, and that adding a machine or a `device_add` in order to reach the site is
laundering rather than witnessing. `mvme88k` already attaches this device, so no such addition is needed.

`regress/` holds many existing pty-driven probes you can copy the shape of -- `_scratchpad/gxprobe.py` is
the validated harness and the project's own rule is *don't hand-roll pty plumbing*. Several probes drive
the debugger with `step`; look at one and follow it.

**A VALID witness needs all of these, and this project has been burned by each:**
1. **It shows the symptom on the COMMITTED build.** `C:\DocumentNoSnc\CC\GXEMUL\build\gxemul` is current
   and clean (source `cmp`s CLEAN against the repo, binary is newer than the source). There is no fix
   yet, so a green run means the witness is wrong, not that the defect is absent.
2. **A LIVENESS control** -- a known value returns through the SAME decode. Offset `0x1ff9` and anything
   below `0x1ff0` take the RAM path, so a write-then-read round trip there should work and proves the
   device is mapped, responding, and reached at the address you think.
3. **A DEVICE-SIGNATURE control** -- something proving the value came from THIS DEVICE rather than from
   RAM or a fallback. *The project's footbridge probe once returned `0x0` everywhere with its RAM control
   green, so one control is not enough.* The clock registers at `0x1ff9..0x1fff` are filled by
   `mk48txx_update_regs()` from the host clock and are a candidate signature; find your own if that does
   not work.
4. **The machine description and dispatch UNMODIFIED.**

## THE THING THAT MAKES THIS ORACLE UNUSUAL, and I want your judgement on it

**The symptom is PROCESS DEATH, not a wrong value.** `exit(1)` ends the emulator, so the observable is
that the child terminates and prints `[ mk48txx: unimplemented READ from offset 0x1ff0 ]`. That is easy
to see and easy to get WRONG:
* a probe that merely times out cannot distinguish a kill from a hang;
* a probe that greps for the message does not establish that the process DIED, only that it complained --
  and this fork has many `fatal()` calls that RETURN (`fatal()` has no early-out and does not exit);
* the emulator can exit for unrelated reasons, so the run needs to show the death is ATTRIBUTABLE to
  this access -- the natural control being an otherwise identical session that reads `0x1ff9` instead and
  runs to completion.

**Please design the oracle to separate those, and say in your answer which discriminator you used.**

## QUESTIONS

1. **Build it and run it against `build/gxemul`.** Report the actual transcript, the row results, and the
   exact command line. If a step does not work, say what you tried and what happened -- a negative result
   with its warrant is a real answer here.
2. **If you CANNOT build a rung-3 witness, say so plainly and stop.** That is a genuine answer and the
   round proceeds as documented-only with the attempt recorded. Do not invent a lower-rung substitute and
   present it as a witness; do not modify a machine description to reach the site.
3. **How many of the eight offsets should the witness drive?** One is enough to license a fix; eight is
   the honest census. Say which you did and why.
4. **Anything else you noticed** -- especially if the boundary is wrong in some way I have not described,
   or if some other part of this device's decode is also unreachable or fatal.

## HOUSE RULES FOR THIS JOB

* **Copy the tree if you need to build; NEVER write into `GXEMUL-SEC`.** You should not need to build at
  all -- `build/gxemul` is current -- but if you do, work in your own `/tmp` copy and say so.
* Put any probe you write in the session scratchpad, not in the repo; I will place it if it lands.
* Builds go through `wsl -d Gentoo` (the default distro has no `make`), and a Windows path handed to
  `wsl -- bash` fails while `wsl` itself exits 0, so use the `/mnt/c/...` form.
* Long runs: check the log's completion sentinel, not its size.
