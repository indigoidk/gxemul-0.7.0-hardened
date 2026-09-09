# A survival oracle used across several regression probes — is it vacuous, and where?

**Answer in prose. Do not propose a code change, do not write a test, and do not construct any input
sequence.** I want the census and the analysis; I will decide the repair.

## Read only these files

    regress/gdrom_decline_probe.py       regress/pcc2_width_probe.py
    regress/gdrom_default_probe.py       regress/pcc2_width_witness.py
    regress/gdrom_toclen_probe.py        regress/sgi_de_primop_probe.py
    regress/sgi_de_width_probe.py        regress/sgi_re_unmapped_probe.py
    regress/sgi_re_width_probe.py

*** THOSE NINE ARE THE WHOLE POPULATION AND THE LIST IS DERIVED, NOT GUESSED: ***

    grep -c 'row(.*"exit0"' regress/*.py   ->  43 rows across exactly these 9 files

**A previous firing of this brief was CUT SHORT after ~700 KB because the file scope was written as
a PREDICATE ("only files containing row( and exit0") -- which cannot be evaluated without reading
everything.  The list above is the same scope stated extensionally, and it is a fraction of the
reading.**  Do not read any other probe.

Do not read `CHANGELOG.md`, `tools/pipeline/ledger.json`, `OUTSTANDING_BUGS.md`, or anything under
`_scratchpad/`.

## Please do not simply ratify

**Where I claim a COUNT, derive it and report the number you get, plus the per-file breakdown.**
This project has been bitten repeatedly by censuses that keyed on a NAME when the thing that defines
the class is a PROPERTY — so before counting, say what you think makes a row a member, and check
that your pattern tests that property rather than a correlate of it.

**VERDICT LINE FIRST.**

## The concern, stated so you can refute it

Several probes assert that the emulator SURVIVED an access by expecting a token spelled `exit0`.
The worry is that this oracle cannot distinguish:

* the guarded code declining cleanly and the process exiting 0 (what the row means), from
* the code announcing a problem and *then* exiting 0 (which the row would also accept).

If that is right, a mutant that keeps the diagnostic and drops only the refusal would satisfy every
such row — a check that cannot fail, in the place where the project most relies on it.

## The questions

**Q1. Census the population.** How many `row(...)` calls use an `exit0` want, in how many files?
Give the per-file breakdown. Then say what each of those rows is actually asserting — I expect them
to differ more than the shared token suggests.

**Q2 IS ALREADY ANSWERED -- DO NOT SPEND BUDGET RE-DERIVING IT.**  A previous firing established
that the helpers return three separate observations (captured output, whether a PTY failure was
seen, and the child's exit status) and that **`exit0` comes from the exit status alone**.  Confirm
in one sentence if you disagree; otherwise take it as given and spend the effort on Q1 and Q4, which
that firing did not reach.

**Q3. Can a probe distinguish "declined cleanly" from "announced and then exited 0"?** If the
producer only observes the exit status, the answer is no and the concern holds. If it also captures
output, say what would have to be asserted to make the distinction, in words.

**Q4. Which of the census rows are ALREADY safe?** I expect some pair the `exit0` want with a
second row on the same access — a value read back, a diagnostic matched, a count. Name those, because
they are the ones needing nothing. **I want the population split into "vacuous alone" and "already
paired", not a single number.**

**Q5. Is there a probe in this tree that does this WELL?** Name the file and describe its idiom. An
in-tree precedent is worth far more than a general principle, and if one exists the repair is to
copy it rather than invent something.
