# qhslowifetch -- third reading, the proviso (main loop, 2026-11-05)

GPT-6 Astra (codex, `ultra`) ANSWERED (codex_codex_qhs_rec12.txt; `CODEXREC12QHS: 0 ACCEPTED 2 TO FIX VERDICT:FIX`).  The rec11
proviso still left a hole, and codex supplied a source-derived counterexample: `if (addr == 0xfec00008) pc ^= 0x1000`.  The second
visit happens and the toggled state is unchanged, but the prologue recomputes addr from the moved pc, so the condition is false the
second time; the toggle fires once and does not cancel.  It is a records defect, not a detector escape.

THE PATTERN IS memc's, and so is the remedy.  Two qualifications of one derived sentence, each defeated by a new counterexample:
the sentence made a claim about the SECOND visit, and every fix tried to bound what can happen there.  It is REPLACED by its
first-visit core, which says nothing about the second visit.  A toggle inserted before arm (a) whose condition reads only the
pair's shared entry state executes on the partner's one visit exactly when it executes on the two-entry session's first visit.
So one that executes on both visits and cancels there executes once on the partner (DERIVED).  "This says nothing about the
second visit, which a toggle can remove or whose condition it can change (codex rec11, rec12)."  The partner-loop comment is
changed the same way.  Diff: r7_20261105/ppc_ifetch_probe.py.rec12.diff (copy .pre_rec12).  Proof: r7_20261105/rec12_proof.out --
all six EQUAL, the negative control DIFFERENT, max width 131.  A fourth reading, scoped to the replacement, is fired
(rec13_20261105/).

*Corrected 2026-11-05 (main loop): this file's time-of-day stamps (removed: ~15:3xZ) were GUESSES that ran up to 3.5 hours AHEAD of the clock; the qhs landing-kit agent found them by checking against the files' own timestamps.  The file's own timestamps are the record: created 12:19Z, last written 12:19Z before this note (UTC).*
