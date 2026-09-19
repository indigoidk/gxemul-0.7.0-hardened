# J4 -- `exemptcliff`: eleven probe-wiring exemptions fall due together on 2026-09-28.  What does each need?

## READING SCOPE AND FORM

The tree under review is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` (git HEAD cdbe7d7).  Pristine 2021 copies of GXemul
under the project root (`./src/`, `_archive/`) are NOT this fork.  Do not read `regress/artifacts/` EXCEPT the one
probe named below that lives there, the ledger, the CHANGELOG or OUTSTANDING_BUGS.  Read-only: no edits, builds or
runs.  VERDICT LINE FIRST.  Mark claims READ (file:line), REASONED or NOT CHECKED; counts carry denominators.

## THE SITUATION

`tools/pipeline/check_probe_wiring.py` requires every DETECTOR-class probe under `regress/` to be executed by a
gate script (the GATES array in that file names them; the battery is `regress/run.sh`).  Eleven detectors are
exempt until 2026-09-27 and the checker hard-fails every commit from 2026-09-28 (`d < today`).  Two others were
wired on 2026-09-18 (`mk48_nvram_probe.py` and `hpcmips_ctor_probe.py`, into `regress/gate_arm.sh` -- read those
two sections as the wiring template: a `python3 -u <probe> "$BIN" gate > $LOG` invocation, a completion sentinel,
per-row `check` greps on the log, totals).  The eleven and their recorded reasons:

    fbpending_drain_probe.py       REPORT-ONLY by default: EXPECT_CAP must be set before a gate row can mean anything
    wdc_altoffset_probe.py         two-leg differential; wants a single-leg mode before gate 10 can assert anything
    wdc_altoffset_sig_probe.py     two-leg differential AND needs a ciR: CD-ROM rig the battery does not build today
    wdc_altoffset_4bit_probe.py    two-leg differential; shares the single-leg-mode debt with its two siblings
    wdc_addtoinbuf_probe.py        two-leg differential AND needs a poisoned CD image the battery does not build
    ppc_rldicl_probe.py            gate_ppc.sh now executes -M 64; this probe lacks the RESULT/CONTROL protocol a gate parses
    alpha_tbi_probe.py             no gate runs an Alpha machine; gate_crossfamily.sh is the named home
    lca_badval_probe.py            no gate runs an Alpha machine; gate_crossfamily.sh is the named home
    lca_widewrite_probe.py         no gate runs an Alpha machine
    lca_isalane_probe.py           no gate runs an Alpha machine
    artifacts/ip30abortkill/ip30_abort_probe.py   no gate runs an SGI IP30 guest session (gate_asan_sweep.sh constructs only)

A "two-leg differential" here means the probe runs TWO emulator binaries (a pristine and a mutated one) and compares
them; a gate has ONE binary.

## QUESTIONS

1. **Per probe, a factual card (11 cards):** the machine/binary it needs (`-E ... -e ...`), any image or rig file
   it opens, its argv contract, the verdict/RESULT line it prints and its exit status on a red row, its
   completion sentinel, approximate runtime if the file states one, and whether the recorded reason is STILL TRUE
   at HEAD (e.g. does `gate_ppc.sh` or `gate_crossfamily.sh` now run something this probe could ride on?  does
   `fbpending_drain_probe.py` still default to report-only?).  Cite lines.
2. **Classify the eleven** into: (W) wireable now with a gate section of the mk48/hpcmips shape and no probe
   change; (P) needs a probe-side change first (say which: single-leg mode, RESULT protocol, EXPECT_CAP); (R)
   needs a rig/image the battery does not build; (G) needs a gate that runs a machine family no gate runs today
   (say which gate and what a minimal section would execute).  Counts must sum to 11.
3. **The Alpha four.**  `gate_crossfamily.sh` is the named home for alpha_tbi/lca_badval/lca_widewrite/lca_isalane.
   Read that gate: what does it run today, and what is the smallest section that would run ONE Alpha probe (which
   machine, which binary, how long)?  Do the four share a machine so one section could run all four?
4. **The single-leg question for the wdc four.**  Read `wdc_altoffset_probe.py`: what does its second leg
   compare against, and could a single-leg mode assert the same rows against expected constants instead?  If yes,
   name the rows whose expectations are already literal; if no, name the rows that only make sense as a diff.
5. **Recommend an order** for the nine days: which to wire, which to re-date with a NAMED prerequisite (a filed
   row id or a gate change), which to reclassify (a probe that is really a WITNESS or RESEARCH artefact is not a
   detector and does not owe a gate -- say if any of the eleven is mis-classed).
6. **Standing licence:** anything else found.
