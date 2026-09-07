# RESEARCH TASK (read-only) — scope an error-handling round in `dev_sgi_re.c`

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Where I state something as fact, ask whether it is
true. A seat that re-derives a premise from something this task did NOT give it is worth more than
one that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** There are three pristine-2021-upstream copies of
GXemul under the project root (`./src/` and two under `_archive/audit-results-*/builds/`). They are
NOT this fork. If your line numbers disagree with mine by hundreds you are reading one of them.

**Where this task states an ARITHMETIC claim — a count, a set of offsets — ENUMERATE it rather than
reasoning about it.**

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## Context

GXemul is a machine emulator. `dev_sgi_re.c` models the SGI CRIME rendering engine. This fork is a
maintenance effort whose standing goal is **robust error handling**: where the model meets a
register value or access width it does not implement, it should report the condition and continue,
rather than calling `exit(1)` and ending the emulator process. Ending the process on unimplemented
input is poor error handling in a device model — a simulated peripheral should degrade gracefully.

Several rounds have already converted such sites in this file (`#497`, `#499`, `#500`, `#504`). This
task scopes the remaining ones **before** a design proposal is written. Nothing is being changed.

## 1. THE COUNT — please re-derive it

The queue entry for this work has carried three different counts and I corrected it twice:

    entry title said           21
    my first correction said   19      (it counted commented-out lines)
    the derived live count     12      grep -cE '^[[:space:]]+exit\(1\);'   vs 19 raw matches

**Q1: re-derive the live count by a method of your choosing and say what you counted.** If you get
something other than 12 I want the method, not just the number — two agreeing greps already misled
me on this file because both counted comment text.

## 2. AN ORDERING CONSTRAINT — the interesting part of this round

`regress/sgi_re_width_probe.py` is a regression test wired into `gate_arm.sh`. It ships **six
`<site> ld kill` rows** whose expectation records CURRENT behaviour — that an 8-byte read at each of
six register windows still ends the process:

    row(nm + " ld kill", how + ("+txt" if ok_txt else "-txt"), "exit1+txt",
        "len=8 READ STILL ENDS THE PROCESS here -- untouched")

So **improving the error handling turns a passing test suite red by succeeding**, six rows' worth.
This project's rule for that case is an ordering discipline: re-pin the six expectations FIRST,
demonstrate the COMMITTED build failing under the new expectations, and only THEN change the model.
Otherwise re-pinning a test cannot be distinguished from fitting the test to the code.

## 3. THE EXPECTATION DESIGN I HAVE PRE-REGISTERED — please attack it

I did not invent this. `#499` re-pinned a neighbouring row **in this same test file** under the same
circumstances, and its comment records that **two obvious expectations were measured USELESS before
a third was adopted**:

* **Termination-only** (`how == "exit1"`) — records THAT the process ended, never WHICH site ended
  it. A message change that left the `exit(1)` in place scored **35/35** against a matched control at
  34/35.
* **`exit0`** — exit status cannot separate *handled the value, then quit* from *ended with status
  0*. A variant scored GREEN on an `exit0+txt` expectation while the process was not alive.

What survived records **three** independent observations:

* `how` — the process is still running;
* `txt` — **one contiguous literal** including the address and data fields. Two separate substring
  tests are weaker: `-- declined.` is emitted by six other sites in this file and by a second device,
  so a bare substring cross-matches;
* `v0` — **the handled read reaches the function's common tail and returns a defined 0.** `v0` is
  preset to a sentinel by the test's `load()` helper, so *returned 0* and *never reached the tail*
  are distinguishable. This is the observation that catches a `return 0` (which `memory_rw` converts
  to −1, raising a bus-error exception) and an `exit(0)` confined to the read branch — **neither of
  which a write-side expectation can observe.** These six sites are read paths, so it is not
  optional here.

**Q2: is that the right expectation set for these six, or does a read path need an observation the
earlier site did not?** Name any channel the three above cannot see.

**Q3: what is the smallest change to the model that would restore the old behaviour at one of these
sites while still satisfying a test built that way?** Name the row you expect to stay green. This is
a test-quality question: a regression test that cannot notice the behaviour returning is not doing
its job.

## 4. THE DISPOSITION QUESTION

When a device model meets input it does not implement, this project recognises seven dispositions:
**1 remove the check entirely · 2 ignore the access silently · 3 ignore it and report once ·
4 accept it (the model already computes the right answer) · 5 signal a bus error to the guest ·
6 accept it into invented storage · 7 implement the missing behaviour.**

**Q4: which disposition does each live site want, and do they all want the SAME one?** A round here
may cover a second site only if one design covers both and one test covers both with no new
observation — so if these twelve split across dispositions, this is several rounds and I would
rather know now.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/` AND `GXEMUL-SEC/regress/*.py`.**  Do not read
`GXEMUL-SEC/regress/artifacts/` or `GXEMUL-SEC/tools/pipeline/ledger.json`: they are this project's
archive of past measurements, they are large, and nothing in them is needed for the questions below.
Everything you need is in the model source and the test file.

**Before answering, GREP THE SOURCE FILE AND ITS NEIGHBOURS FOR THE EXISTING IDIOM.** The tree's own
precedents are part of the design space, and this project has twice found whole dispositions that
way. In particular, `#497`, `#499`, `#500` and `#504` each converted a site in this same file, and
their choices constrain what is consistent.

**And check disposition 5 is even AVAILABLE here before recommending it.** Signalling a bus error
works because `memory_rw.c` dispatches an exception on a failed device access — for MIPS and M88K. A
disposition the target CPU cannot deliver is not an option, however good it looks.

## 5. WHAT I AM NOT ASKING

Do not write the change. Do not write test rows. I want: the count, the classification, whether this
is one round or several, and whether the pre-registered expectation set survives contact.

**If, while verifying a claim, you found something ELSE — say so.** The last two rounds' best
findings arrived that way, including two defects in code everyone had called correct.
