# `dev_pcc2.c` — an analysis question about a terminating arm reached from a legal register write

**Answer in prose. Do not propose a code change, do not write a test, and do not construct any input
or instruction sequence.** I want the analysis; I will design the repair.

## Read only these files

    src/devices/dev_pcc2.c
    src/include/thirdparty/mvme_pcctwo.h     (or whatever header defines the PCC2 register names)
    src/machines/machine_mvme88k.c           (only to answer which machines instantiate it)

Do not read `CHANGELOG.md`, `tools/pipeline/ledger.json`, `OUTSTANDING_BUGS.md`, or anything under
`_scratchpad/`.

## Please do not simply ratify

**Where I claim a COUNT, a REACHABILITY, or a VALUE RANGE, enumerate it and report what you get.**
Ask what the PRODUCER can emit before walking it.

**VERDICT LINE FIRST.**

## What I believe, stated so you can refute it

A byte write to the GENCTL register with a particular bit set (the one the header calls the C040
bit) is a LEGAL write — the register's own guard accepts it — and it subsequently ends the host
inside `reassert_interrupts()`. A previous round de-fatalised a set of WIDTH guards in this file;
this arm was deliberately left, and the width detector's own test values were chosen to stay off it.

## The questions

**Q1. Trace the path from the guest write to the termination, naming each function.** Where exactly
does the process end, what is the guard, and what does its diagnostic say? I want the call chain,
because I do not yet know whether the kill is in the write handler or in something it calls.

**Q2. Is the write actually LEGAL?** Show the register's guard and enumerate which byte values it
accepts. If some accepted values reach the termination and others do not, give both sets. This is
the claim I am least sure of.

**Q3. What does the C040 bit MEAN?** Name it from the header and say what the model does with it
elsewhere — is it read anywhere, does anything depend on it, or is it accepted and discarded? I want
to know whether the right repair implements it or refuses it.

**Q4. Enumerate every other `exit(1)` in this file**, with its guard and what reaching it takes. I
want to know how many siblings there are and whether they are one class or several, because that
decides whether this is one round or several.

**Q5. What non-terminating idioms does this file ALREADY use** for values it does not implement?
Name each and where it is. An in-file precedent is worth far more than a general principle — and if
a previous round already de-fatalised guards here, its chosen shape is the one a new repair should
match unless there is a reason not to.

**Q6. Is `reassert_interrupts()` called from anywhere else?** If so, list the callers and say
whether any of them can reach the same termination by another route. A repair aimed only at the
GENCTL path would miss those.
