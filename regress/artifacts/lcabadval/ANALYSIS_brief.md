# `dev_lca.c` `lca_ioc` — an analysis question about its `default:` arms

Please answer by reading the source. **Answer in prose. Do not propose a code change, do not write
a test, and do not construct any input sequence.** I want the analysis only; I will decide the
disposition myself.

## Read only these files

    src/devices/dev_lca.c
    src/include/thirdparty/alpha_lcareg.h
    src/devices/bus_pci.c            (only for how a PCI config access is serviced)

Do not read `CHANGELOG.md`, `tools/pipeline/ledger.json`, `OUTSTANDING_BUGS.md` or anything under
`_scratchpad/` — those are project records, not the code under review.

## Please do not simply ratify

Where I state something as fact below, check whether it is true. A recent review had seven of nine
readers confirm a premise stated wrongly. **Where I make an arithmetic claim — a value range, a
mask, a count of reachable values — enumerate it rather than reasoning about it.** Walk the values,
and ask what the PRODUCER of those values can actually emit before you walk them.

**VERDICT LINE FIRST.**

## What I believe, stated so you can refute it

`DEVICE_ACCESS(lca_ioc)` handles a small number of register offsets and has `default:` arms for
both reads and writes that call `fatal()` and then `exit(1)`. Separately, its `LCA_IOC_CONF` case
rejects values with bits outside a narrow mask by the same means.

## The questions

**Q1. Enumerate the offsets `lca_ioc` implements, and the exact width of the region the device is
registered for.** How many distinct offsets in that region reach a `default:` arm? Give the count
and how you derived it. Note carefully whether `relative_addr` can be unaligned, and whether the
region is scaled or shifted before the switch sees it — a derivation that misses a shift or a mask
reads exactly like a correct one.

**Q2. For each `exit(1)` in this file, say what it takes to reach it**: which register, which value
or address, and whether reaching it requires anything unusual or merely an ordinary access. Please
distinguish clearly between arms reachable by any access and arms that need a specific value.

**Q3. Which of those arms have a documented meaning in the 21066 hardware manual?** The manual is
at `_scratchpad/21066_66a_hrm.txt` (plain text, 13,876 lines) — you may read that one file too.
I am asking whether the model is refusing something the hardware *documents*, in which case the
right answer is to implement it, or something genuinely undefined.

**Q4. Are the read `default:` and the write `default:` symmetric?** If one is broader than the
other, say which and by how much. Sibling asymmetry inside one handler is usually a sign that one
arm was written against a driver that happened to exercise it and the other was not.

**Q5. What in this file has already been given a non-terminating disposition, and what shape did
that take?** I want the file's own precedents described, because a repair that matches an existing
in-file idiom is worth more than one argued from first principles.
