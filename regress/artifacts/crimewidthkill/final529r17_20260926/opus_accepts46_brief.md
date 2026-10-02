OPUS_SEAT_ALIVE_20260926_529acc -- open your answer with that token and the first line of
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\CHECKPOINT.md`, verbatim.

You are the measuring seat for #529 (crimewidthkill) in the GXemul hardened fork, a C hardware emulator.  The tree is
`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`; ignore any other `src/`.  **Read-only on every project tree**; you may build
and run only in a WSL scratch clone under `/tmp` (never under C:\DocumentNoSnc\cc\GXEMUL), and you owe nothing that
needs one unless you choose to measure.  Write your answer to
`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\final529r17_20260926\opus_accepts46.md`
(the only project-tree file you may write) and return its content.

THE QUESTION.  The detector's contract (`final529r17_20260926\crime_width_probe.r17.py`, the module docstring) carries
repair 13's bucket partition of the 46 ACCEPTS entries (docstring lines ~236-262): 23 rowed post-latch, 8 already
pinned post-latch, 10 EQUIVALENT at the guest, 5 HOST-DIAGNOSTIC ONLY.  Its own text says the partition is incomplete:
3 of the 5 host-diagnostic members are named and 2 are not; 4 of the 10 equivalent members are named and 6 are not --
"a bucket whose members cannot be listed cannot be audited", with an OWED line.  Both adjudicators have ruled on it:
the flagship seat said FILE it; the second adjudicator said it needs "an L4 enumeration correction and justified
dispositions, not blanket filing as coverage debt".

Produce the enumeration, AS OF THE CURRENT PROBE (r17 = repair 16's rows; repairs 14-16 rowed several of the cells
the buckets were written about, so the partition may have moved):

1. A table of all 46 ACCEPTS entries (the `ACCEPTS` tuple in the probe; `repair14_20260916\BUCKETS8_rerun.out` lists
   them with their pre- and post-latch sessions): for each, its disposition NOW, one of
   ROWED (name the row(s) and the latch state(s) they observe it in), EQUIVALENT (the derivation, from
   `src\devices\dev_sgi_ip32.c`'s `DEVICE_ACCESS(crime)`: why no guest channel can separate it from a decline), or
   HOST-DIAGNOSTIC ONLY (the host text it produces and why nothing guest-visible differs).
2. From that, the members of repair 13's two unlisted buckets -- or, if the table shows repair 13's counts no longer
   describe the tree, say so and give the current counts instead.  Every EQUIVALENT claim must carry its derivation;
   a claim you could only settle by running, mark as such (or measure it in your clone and say what you ran).
3. The exact replacement text for the docstring's bucket block (lines ~236-262), keeping its history visible (the
   file's style quotes the sentence it corrects), and naming your table as the artifact.

State what is a reading and what is a measurement.  Neutral engineering review: this is about which test rows cover
which device register accesses.
