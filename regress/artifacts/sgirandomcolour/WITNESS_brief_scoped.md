# SGI "RE" drawing-engine colour-mode dispatch — can a guest reach the unimplemented `default:` arm?

**Scope: ordinary emulator correctness work.** A `switch` on a documented pixel-format field
implements four of the five values the header defines. The fifth falls to a `default:` arm that
fills the pixel buffer with unspecified values rather than a formatted pixel. I want to know
whether an ordinary guest instruction sequence can reach that arm on an unmodified in-tree machine,
and if so, to have a small reproducible test that shows it.

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise its author stated wrongly. **Check the
premises, not just the derivations.** Where I state something as fact, ask whether it is true. A
seat that re-derives a premise from something this brief did NOT give it is worth more than a seat
that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** There are THREE pristine-2021-upstream copies of
GXemul under the project root (`./src/` and two under `_archive/audit-results-*/builds/`). They are
NOT this fork. If your line numbers disagree with mine by hundreds you are reading one of them.

**Where this brief states an ARITHMETIC claim — a field width, a mask, a set of reachable values —
ENUMERATE it rather than reasoning about it.** Walk the values. **And ENUMERATE THE RIGHT DOMAIN:**
ask what the PRODUCER of these values can actually emit before you walk them. A derivation that
skips one masking line reads exactly like a correct one.

**VERDICT LINE FIRST**, so your answer survives truncation.

## §B0 — *** READ ONLY THESE FILES.  THIS BOUND IS PART OF THE TASK. ***

    src/devices/dev_sgi_re.c
    src/include/thirdparty/crmfbreg.h
    src/machines/machine_sgi.c          (only to answer Q1: which machine instantiates the device)
    regress/gxprobe.py                  (only if you need the existing probe harness idiom)

**Do NOT search or read `CHANGELOG.md`, `tools/pipeline/ledger.json`, `OUTSTANDING_BUGS.md`, or
anything under `_scratchpad/`.** Those are this project's own engineering RECORDS, not the code
under review. They are long, they are written in shorthand, and reading them will not help you
answer any question below — every fact you need about them is already summarised in §C.

If you find yourself wanting a fact that is only in those files, say so and stop rather than going
to get it.

## §C — SETTLED PREMISES (verified locally for this brief)

**P1.** `src/devices/dev_sgi_re.c` implements a colour-mode `switch` with exactly four cases —
`DE_MODE_TYPE_CI`, `_RGB`, `_RGBA`, `_ABGR` — and a `default:` arm whose body begins
`buf[0] = random();` (four such calls).
Anchor: `grep -n 'buf\[0\] = random();' src/devices/dev_sgi_re.c`

**P2.** `src/include/thirdparty/crmfbreg.h` documents **FIVE** colour types. The fifth is
`DE_MODE_TYPE_YCRCB  0x000000f0`.

**P3.** `grep -c YCRCB src/devices/dev_sgi_re.c` = **0**. The documented fifth mode is not handled
anywhere in the device, so it reaches the `default:` arm.

**P4 — a related round already shipped and is the model to follow, NOT to copy.** A sibling arm in
the same file (`horrible_getputpixel()`) had a single `random()` call; it was replaced under round
`sgirandompixel`. That round's disposition was *decline the operation and announce once*. **The arm
in this brief differs in an important way: it fills a BUFFER rather than one caller variable, so
what a declined fill should leave in that buffer is its own question.**

## §D — WHAT I AM ASKING FOR

This project's test ladder ranks evidence by how the code path was reached:

* **rung 4 — boot:** a real guest driver reaches the path unaided.
* **rung 3 — cold-debugger probe:** a real guest instruction through real address decode and real
  `memory_rw`, on an **UNMODIFIED in-tree machine description**. This is EQUAL to a boot in
  admissibility and is what I am asking you to try for.
* **rung 2 — machine construction:** only valid for defects in construction itself.
* **rung 1 — an `#include`/direct-call harness:** **NEVER acceptable as a reproduction here.** If it
  still compiles and still shows the behaviour after the machine description and device dispatch
  are removed, it was never a reproduction.

A rung-3 probe must additionally carry **two controls**: a **LIVENESS** control (a known value
returns through the same decode, proving the probe reached the device at all) and a
**DEVICE-SIGNATURE** control (the observed value could only have come from this device — RAM would
answer differently). One control is not enough: a probe for a different device once returned zeroes
everywhere with its RAM control green.

**And a machine or `device_add` introduced IN ORDER TO reach the site is laundering, not
witnessing.** The machine description must be one already committed in the tree.

## §E — THE QUESTIONS

**Q1. Which in-tree machine instantiates this device, and is the register window guest-addressable
on it?** Name the machine by the `-e` name the emulator accepts, and give the physical address of
the register that selects the colour mode. If more than one machine qualifies, say which is the
least ceremonious to drive.

**Q2. What is the exact guest instruction sequence that sets the mode field to the fifth value and
then triggers one pixel operation?** Please give it as concrete stores with addresses and values,
not as prose. State the CPU architecture and whether the sequence needs any prior initialisation
(a mode register, an enable bit, a destination pointer) — and if it does, say what and why.

**Q3. What is the OBSERVABLE?** The arm fills a buffer with unspecified values, so an oracle that
just reads the buffer back is not stable across runs and cannot be a test expectation. I need a
channel that differs deterministically between the current code and a corrected version. Candidates
I can think of, please assess and add to: (a) the values are non-deterministic across two runs with
identical input, which is itself a stable *property* to assert; (b) some downstream register or
debug line reports what was written; (c) the operation's effect on a framebuffer region readable by
a second guest load. **Say plainly if you think no deterministic channel exists** — that is a real
answer and it changes the round's disposition rather than blocking it.

**Q4. If you conclude no rung-3 probe is constructible, say so and say WHY**, naming what is
missing. That is a genuine answer: the round then proceeds as documented-only with the attempt
recorded. What it must never mean is that nobody thought to ask.

**Q5. What disposition would you choose for the arm itself?** The option set used here has seven
members: (1) delete the operation, (2) decline silently, (3) decline plus a bounded/latched
announce, (4) accept — where the model already computes the right answer and discards it,
(5) fault — deliver the architectural bus error, (6) backed accept — invent storage and accept,
(7) implement the missing mode. **Before choosing, grep this tree for an existing idiom** — the
tree's own precedents are part of the design space, and members 4, 5 and 6 were all found that way
in earlier rounds rather than by argument. Also grep the SIBLING arms in this same file: their
disposition is a stronger warrant than any general principle.
