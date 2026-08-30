# AGY JOB 2 — build a RUNG-3 WITNESS for a host-kill class nobody has witnessed

You have build and execute capability. **This task is a measurement, not an analysis.**

## HOUSEKEEPING — not optional

* **COPY THE TREE. NEVER WRITE TO `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC`.** Work in
  `/tmp/gxagy_wk`. Verify at the end with `git -C ... status --porcelain` and report it.
* Build inside `wsl -d Gentoo` (default distro has no `make`). `rm` the `.o` first.
* `MAKE_RC` can report 0 on a failed build — check `[ binary -nt source ]` explicitly.

## THE DEFECT CLASS

**A GUEST CHOOSING AN ACCESS WIDTH ends the host emulator process.** This fork fixed the
class in `dev_wdc.c` (its own comment: *"a 3- or 8-byte access to the data port used to call
exit(1) — a GUEST choosing an access width killed the host process"*) and never swept for the
rest. Sixteen sites survive in two other devices:

* `src/devices/dev_sgi_re.c` — 6 sites of the form
  `if (len != 8) { fatal("TODO: unimplemented len=%i ..."); exit(1); }`
* `src/devices/dev_pcc2.c` — 10 sites, diagnostics like *"TODO: pcc2: non-byte reads and
  writes of ..."*

**Reachability for sgi_re is established BY CONSTRUCTION** — `machine_sgi.c` calls
`dev_sgi_re_init(machine, mem, 0x15000000)` and the device registers at `baseaddr + 0x1000`.
Find these with grep rather than trusting my line numbers.

## WHAT I NEED

**A rung-3 witness on ONE site.** Rung 3 means: a real guest instruction, through real
address decode and real `memory_rw`, on an **UNMODIFIED in-tree machine description**. A
`#include`-and-call harness is explicitly NOT a witness here and will be rejected.

1. Pick the cheapest reachable site — I suggest the `dev_sgi_re.c` `len != 8` guard, but if
   `dev_pcc2.c` turns out easier to reach, take that and say why.
2. Work out which `-E <machine>` instantiates it and at what guest address the register
   window lands. **Check this; do not assume it.**
3. Write a probe that plants a guest instruction performing an access of the WRONG WIDTH at
   that address, runs it, and observes the outcome via `waitpid` — distinguishing
   `exit1` (the defect) from `exit0` (survived) from `sigN` (a crash that is NOT this defect).
4. **Carry the two mandatory controls:** a LIVENESS control (a known value returns through
   the same decode) and a DEVICE-SIGNATURE control (the observed value could only have come
   from the device — RAM would answer differently). One control is not enough: a sibling
   probe once returned 0x0 everywhere with its RAM control green.
5. Run it on the **committed, unmodified** build and report whether the host dies.

There is a working example of exactly this shape to copy from:
`GXEMUL-SEC/regress/artifacts/gdromcondlies/witness_20260830/gdrom_cond_witness.py`
(SH4/dreamcast). Read it for the pty/debugger machinery — `put h`, `pc=`, `step N`, a
`bra .` self-loop, `print rN` — and re-aim it. **The instruction encodings will be different
for MIPS/m88k; derive them, and include at least one row expecting a small NONZERO value,
because a wrong register field yields 0 and every sentinel row accepts 0 by accident.**

## REPORT

Verdict line first: **did you get a rung-3 witness, yes or no?** Then the probe, the row
table, and the raw outcome. **If you cannot build one, say so plainly and say what stopped
you** — that is a genuine and useful answer, and the round proceeds as documented-only. Do
not invent a result.
