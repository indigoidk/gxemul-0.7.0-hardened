# fbfiqsilent -- FIQEnable answers silently while its IRQ twin ends the host

## 0. SCOPE

Read `GXEMUL-SEC/src/devices/dev_footbridge.c` -- the FIQ and IRQ register arms -- and
**`_scratchpad/dc21285.txt`**, the extracted Intel DC21285 datasheet, which IS present in this tree.
Please avoid `regress/artifacts/` and `tools/pipeline/ledger.json`.

Tree: `GXEMUL-SEC/src/`. Ignore the pristine 2021 `src/` at the project root.

*** NO MUTANT, NO EVASION, NO GUEST SEQUENCE IS WANTED. *** Source review plus a datasheet reading.

## 1. WHY THIS ROW IS WORTH YOUR TIME

**Three rows in this queue are blocked because the architecture manual is not in the tree** --
`armbfcdecode` needs DDI 0406, and two Alpha rows need an Alpha ARM. **This one is not blocked:**
`_scratchpad/` holds `dc21285.pdf` and `dc21285.txt`, and that datasheet has already settled a
footbridge question in this project -- `+0x188` turned out to be **IRQEnable, a documented read-only
register** whose value the model computes correctly and then discarded, which changed the
disposition from "decline" to "accept".

**So please cite the datasheet by section or table, and quote it.** This project has shipped page
citations that came from model output rather than a local document and is trying not to again -- if
the datasheet does not cover something, say so rather than filling the gap.

## 2. THE FILED CLAIM -- a claim, not a premise

> *"`dev_footbridge.c` answers FIQEnable reads with a silent constant 0 while its IRQ twin ends the
> host."*

**Unverified by me.**

**Please do not simply ratify.** You have refuted premises of mine on six briefs tonight.

## 3. QUESTIONS -- VERDICT LINE FIRST

**Q1. Is the asymmetry real?** Quote both arms. Does one really terminate while its twin returns a
constant? Give the register offsets and the exact behaviour of each.

**Q2. WHAT DOES THE DATASHEET SAY THESE REGISTERS ARE?** This is the question the local manual can
actually answer, and it is why this row is unblocked. Are FIQEnable / FIQStatus read-only,
write-1-to-set, or something else? **If the model's constant 0 is the architecturally correct answer
for an unconfigured device, the "silent" half is not a defect at all** -- which would be the
`+0x188` outcome again, and I would rather learn that than ship a fix.

**Q3. Which disposition for the terminating twin?**
**1 DELETE · 2 DECLINE (silent) · 3 DECLINE + LATCHED ANNOUNCE · 4 ACCEPT · 5 FAULT · 6 BACKED
ACCEPT · 7 IMPLEMENT.** Note that footbridge is an **ARM** machine, so unlike the Alpha rows this
session has been working, **member 5 FAULT may genuinely be available here** -- `memory_rw`'s
device-failure path has an ARM arm. Say whether it is, and whether it is right.

**Q4. Is the SILENT half also wrong, independently?** A silent constant where the hardware would
report real state is a fidelity gap even when it does not terminate. If the datasheet says the value
should reflect something the model tracks, this is member 4 ACCEPT territory -- the model computing
the right answer and discarding it, exactly as `+0x188` did.

**Q5. One round or two?** The terminating arm and the silent arm are different defects with
different fixes. The project's rule: more findings create more candidate ROUNDS, never bigger
rounds. Argue it.

**Q6. What observable distinguishes fixed from unfixed, for each half?** Name the channel. If the
honest answer is that no in-tree probe drives footbridge FIQ, say so -- that caps the severity and
makes it a documented candidate.
