# THESE CONTROLS TEST A DECLARATION THE FILE NO LONGER CONTAINS.

**They vary only the `#define` block and they test the `|` (OR) form.  The shipped
declaration is the `+` (SUM) form.**  Read them as a record of the SUPERSEDED
state, never as evidence for what `dev_dreamcast_gdrom.c` ships today.

    controls.sh   five states, `|` only, synthetic TU     <- SUPERSEDED
    tucheck.sh    the real file's own translation unit
    objcheck.sh   byte-identical objects (assert emits no code)
    ordelta.sh    the `|` -> `+` delta on the E1 shape
    triple.sh     kimi's unmeasured TRIPLE alias, both forms

## Why this file exists

The product comment cited this directory for a claim of **"MEASURED IN FIVE
STATES"** while the file shipped `+`.  That is an L4 wrong record: the cited
controls backed a declaration that had been replaced.  Corrected 2026-08-29
after the opus5 supplementary seat opened `controls.sh` and compared its
operator against the source.

**The failure is not that the controls were wrong.**  Every result in them is
true of the form they test.  The failure is that they were *cited for a
different form*, and nothing in the directory said which form that was — so a
reader following the citation would have found five green rows and concluded
the shipped declaration had been measured.

## What supersedes it

`../supp_p2_20260829/bothstates_20260829.out` — **eight states x BOTH operator
forms, generated from the real file, with md5s for the PRE and POST sources.**
It is strictly stronger in two ways this set could not be:

* it varies the **enum** block, not just the `#define` block.  Three states that
  compile clean under `|` are only reachable that way, and this directory's
  controls cannot express them at all;
* it carries both forms side by side, so the delta is visible in one artifact
  instead of inferred across two runs.

`ordelta.sh` and `triple.sh` remain valid and are not superseded — both test
`|` against `+` explicitly and say so in their own output.

## The general lesson, which cost nothing here only because a seat looked

An artifact directory is named for the DAY it was written, not for the code
state it measured.  When the code moves, the directory keeps its name and its
green rows, and a citation to it silently becomes a claim about the wrong thing.
**Name the state in the artifact, not only the date** — the seat that found this
hit the same hazard in its own work an hour later, captured a post-fix tree
under a pre-fix caption, and renamed the file `_POSTFIX_TREE.out` rather than
leaving it to be read as an absence of the escape.
