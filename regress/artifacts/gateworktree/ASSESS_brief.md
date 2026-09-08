# gateworktree -- does the pre-commit gate check what actually gets committed?

## 0. SCOPE

Read `GXEMUL-SEC/tools/precommit_check.sh` and whatever it invokes under `tools/pipeline/`.
Please avoid `regress/artifacts/` and `tools/pipeline/ledger.json`.

Tree: `GXEMUL-SEC/`. Ignore the pristine 2021 `src/` at the project root.

*** NO MUTANT, NO EVASION, NO GUEST SEQUENCE IS WANTED. *** Harness source review.

## 1. WHY NOW, AND WHY THIS IS NOT HYPOTHETICAL

The filed claim is:

> *"`precommit_check.sh` validates the WORKING TREE, not the staged content, so it cannot see [a
> divergence between them]."*

**I am about to make exactly the commit that would expose this.** The working tree currently has
ten modified tracked files, and the commit will stage **nine** of them -- `regress/sgi_de_primop_probe.py`
is deliberately excluded by a standing project rule, along with several untracked paths. So the
working tree and the staged content **will differ**, by construction, in the very commit this gate
is about to approve.

**If the claim holds, the gate is checking a state that is never committed.**

## 2. QUESTIONS -- VERDICT LINE FIRST

**Please do not simply ratify.** You have refuted premises of mine on seven briefs tonight,
including one an hour ago where I asserted an ARM exception arm that does not exist.

**Q1. Is the claim true?** Quote the lines that read files. Does the script read from the filesystem,
from `git show :<path>`, from `git diff --cached`, or a mixture? **A mixture would be the worst
case** -- some checks staged, some not, with nothing saying which.

**Q2. Which specific checks are affected, and how badly?** The script has lettered sections. For
each that reads a file: would it pass on a working tree that is correct while the STAGED content is
wrong, or vice versa? I care most about the ones that would give a FALSE GREEN, not the ones that
would false-red -- a false red is loud.

**Q3. Is section J affected?** That section hard-fails on byte-divergence between the root
`CLAUDE.md` and its tracked copy at `tools/CLAUDE.md`. **If it compares working-tree bytes, then
staging one and not the other passes the gate and commits a divergence** -- which is precisely the
failure J exists to prevent.

**Q4. What is the smallest correct fix?** `git show :<path>` reads staged content; `git diff --cached`
lists it. **Does converting the script cost anything?** In particular: would it break the common case
where a developer runs the gate BEFORE staging anything, with an empty index? That case must keep
working, or the gate gets run less often, which is worse than the defect.

**Q5. Is there a cheaper mitigation than converting the script?** For instance, a single check that
the working tree and the index AGREE for the files the gate reads, failing loudly when they do not.
That is one command and it converts a silent blind spot into a loud refusal. **Argue whether that is
sufficient or merely comforting** -- this project has a recorded class of "checks that cannot fail",
and a mitigation that passes whenever the developer stages everything would be one.

**Q6. Severity.** Has this ever actually mattered, on the evidence in the script itself? A defect
that requires an unusual staging pattern to trigger ranks differently from one that fires whenever
anyone stages a subset. **Say which this is.**
