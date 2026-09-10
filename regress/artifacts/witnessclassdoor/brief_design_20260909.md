# witnessclassdoor -- DESIGN PRE-READ for a harness round: a witness that has gone post-fix-green IS a detector, and the checker's CLASS field is an undated door for un-gated detectors

Please do not simply ratify. A recent panel had seven of nine seats confirm a premise a brief stated
wrongly. Check the premises, not just the derivations. This is an ANALYSIS request about a checker in
the test harness; prose only -- no patch, no code. VERDICT LINE FIRST.

## THE TREE
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`. Ignore any other `src/` under the project root. Read
`tools/pipeline/check_probe_wiring.py` (its MANIFEST, CLASSES, the dated EXEMPT table, and how an
un-gated entry of each class is rendered), and `regress/gate_*.sh` / `regress/run.sh` as needed to
learn which probes any gate actually runs. `tools/pipeline/check_bugfile_sync.py` is the precedent
for a forward-only dated cutoff (`CUTOFF`).

## SETTLED PREMISES (say if you cannot verify one)
1. In check_probe_wiring.py, an un-gated `CLASS_DETECTOR` entry is either UNWIRED (a failure) or
   carries a dated EXEMPT row naming the round that owes it; an un-gated `CLASS_WITNESS` entry renders
   as `not run (correct)`. So the CLASS field decides whether an un-gated probe's debt is VISIBLE.
2. The checker's own definition of a detector is a probe that has gone post-fix-green (it defends a
   fix). A witness exists BEFORE a fix and shows the defect; it does not have to go green after.
3. The Opus seat reported, from reading the MANIFEST, that at least 8 of the 18 `CLASS_WITNESS`
   entries describe a post-fix-green outcome ("fix N/M", "post-fix green MEASURED"), one entry
   unsettled -- so detector debt escapes through the class field, UNDATED, faster than the dated
   EXEMPT table retires it. An instance was made on 2026-09-09: `lca_irqstub_probe.py` kept
   `CLASS_WITNESS` "because re-classing it would demand a gate home".
4. Every checker change in this project ships with a dated cutoff (forward-only; a rule that
   retro-fails the archive gets switched off) and two negative controls, as its own round.

## THE QUESTIONS -- answer extensionally
**Q1.** Enumerate EVERY `CLASS_WITNESS` entry in MANIFEST. For each: (a) does its note record a
post-fix-green outcome? quote the fragment; (b) does any gate script run it (grep the probe filename
across regress/*.sh; name the script and line); (c) if (a) yes and (b) no, it is an un-gated detector
rendered `not run (correct)`. Give the table and the count WITH ITS DERIVER (the grep you ran).
Premise 3 says >= 8 of 18 with one unsettled: confirm, correct, or narrow it -- and say which.
**Q2.** Propose the ONE rule the checker should enforce, in a sentence, with a dated cutoff. State
exactly what an entry must carry to pass under it: (i) re-classed `CLASS_DETECTOR` with a gate home,
or (ii) a dated EXEMPT row naming the round that owes the wiring, or (iii) a note stating post-fix
green was NEVER measured (a true witness). Say how the rule reads the note -- a marker token, a
regex over "fix N/M", or a new MANIFEST field -- and why that choice cannot silently match nothing.
**Q3.** The negative controls the round owes. Describe (i) a synthetic `CLASS_WITNESS` entry that
says post-fix green and that no gate runs, which the rule must FAIL; (ii) the same entry with a dated
EXEMPT row, which must PASS; (iii) a pre-cutoff entry, which must be REPORTED and not FAILED. For each,
what output line distinguishes the outcome, so an unrun control and a passing one cannot look alike.
**Q4.** Risks and cost. Which existing entries go red on day one under your rule, and for each the
cheapest gate home (name a gate section with the same shape -- e.g. gate_asan_sweep.sh hosts
sgi_eaddr_probe.py on build/gxemul with a per-probe section; say where such a section must sit
relative to any `gate_skip` that exits the gate). What would make a maintainer switch this rule off?

Evidence basis: state what you read versus what you took from this packet.
