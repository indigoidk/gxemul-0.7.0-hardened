# SGI "RE" drawing engine — an analysis question about two colour-mode switches

**Answer in prose. Do not propose a code change, do not write a test, and do not construct any
input or instruction sequence.** I want the analysis only; I will decide what to do with it.

## Read only these files

    src/devices/dev_sgi_re.c
    src/include/thirdparty/crmfbreg.h
    src/machines/machine_sgi.c

Do not read `CHANGELOG.md`, `tools/pipeline/ledger.json`, `OUTSTANDING_BUGS.md`, or anything under
`_scratchpad/` — those are project records, not the code under review.

## Please do not simply ratify

Check the premises below rather than reasoning from them. **Where I make a claim about a COUNT or a
SET of values, enumerate it — walk the values and report the number.** Ask what the PRODUCER of
those values can emit before walking them. A derivation that misses one masking line reads exactly
like a correct one.

**VERDICT LINE FIRST.**

## What I believe, stated so you can refute it

There are two `switch` statements on a colour-format field — one on the write side and one on the
read side. Each implements four cases. `crmfbreg.h` defines a fifth format constant that neither
switch has a case for, so that value reaches a `default:` arm in both.

## The questions

**Q1. Confirm or refute the shape.** How many switches, how many cases each, and are the two case
sets identical? If they differ, say how. Sibling asymmetry inside one file usually means one arm was
written against a driver that exercised it and the other was not.

**Q2. Enumerate the colour-format constants `crmfbreg.h` defines and say exactly which are handled.**
Give the constant's value as well as its name. Then say how the field is extracted from the register
— the mask and shift — and therefore **what the full set of values the field can hold actually is.**
That last part is the one I care most about: the number of *unhandled* values is not necessarily one.

**Q3. Describe what each `default:` arm does, precisely.** For the write side I believe it fills a
four-byte buffer with unspecified values and then continues into the normal path; for the read side
I believe it assembles a value from that buffer. Say where those bytes end up — specifically whether
they reach guest-visible memory or a framebuffer, and by what call.

**Q4. Is the fifth format DOCUMENTED?** `crmfbreg.h` is a third-party register header; say whether
it carries any comment or context about that format, and whether anything else in the tree refers to
it. I am trying to establish whether this is an unimplemented-but-real feature or a constant nobody
uses.

**Q5. What has this file already done elsewhere with an unhandled case?** Describe the file's own
existing idioms for a value it does not implement — I want the in-file precedent, because a repair
matching an existing idiom is worth far more than one argued from first principles. Name each
precedent and where it is.

**Q6. Is either `default:` arm reachable at all?** Consider what writes the colour-mode register and
whether any code path constrains the field before the switch sees it. If you conclude a `default:`
is unreachable, say so plainly and give the constraint that makes it so — that answer is just as
useful to me as the opposite.
