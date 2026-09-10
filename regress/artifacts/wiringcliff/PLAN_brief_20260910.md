# `wiringcliff` -- THE HARNESS ROUND PLAN: wire the two enforceable probes into their gates, re-date the four that cannot fail, and name the negative controls (read-only)

Nonce: CODEX_WIRINGCLIFF_PLAN_20260910.  Open with `VERDICT: GO | NO-GO (n items)` and echo the nonce.

**Please do not simply ratify the derived record.**  `regress/artifacts/wiringcliff/DERIVED_20260909.txt` was
derived at HEAD `b4d4177`; HEAD is now `1ce8296` and six commits have landed since.  Re-run its derivers before
relying on any of its numbers, and say which still hold.

The tree under review is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`; ignore any other `src/` under the project root.

## What is settled (from the derived record and your own contracts answer, `codex_contracts_20260909.txt`)
* `tools/pipeline/check_probe_wiring.py` carries SIX exemptions dated `2026-09-20` (`grep -n '2026-09-20'`); the
  comparison is `d < today`, so they first red on 2026-09-21 and the pre-commit gate hard-fails from then on.
* Two of the six END IN A MEANINGFUL EXIT STATUS and are therefore wirable now: `regress/fbpending_drain_probe.py`
  (`sys.exit(0 if ok else 1)`) and `regress/hpcmips_ctor_probe.py` (`sys.exit(main())`).  The other four
  (`wdc_altoffset_probe.py`, `wdc_altoffset_sig_probe.py`, `wdc_altoffset_4bit_probe.py`, `wdc_addtoinbuf_probe.py`)
  ALWAYS exit 0 and need an oracle round before a gate can consume them; your contracts answer ranked
  `wdc_altoffset_probe.py` closest to gate-ready and `wdc_altoffset_sig_probe.py` furthest.
* A gate row that cannot fail is worse than none (this project's check-that-cannot-fail class), so every wiring
  in this round owes TWO negative controls: the wired row REDS on a mutant of the thing it guards, and the gate
  still PASSES on HEAD with the row in place.
* The exemption re-date is not free either: a re-dated exemption is a claim that the probe is still tracked; it
  owes a reason and a date tied to a plan, not a bump.

## Files
* `tools/pipeline/check_probe_wiring.py` (the manifest: CLASS_* entries, the `EXEMPT` dates and their comments).
* `regress/gate_asan_sweep.sh` -- where `hpcmips_ctor_probe.py` belongs; the derived record says "before the
  `:99 gate_skip`" (read the gate: what does that skip guard, and why must the new row precede it?).
* `regress/gate_ab.sh` -- where `fbpending_drain_probe.py` belongs (your contracts answer has a section on it).
* `regress/lib.sh` (the `check`/`gate_skip`/`count` idioms every gate uses) and one wired probe's existing gate
  row as the model (for example how `gate_sh_rounding.sh` consumes a probe's `_RESULT=` line).
* The six probes themselves.

## Questions (verdict line first; cite by grep anchor and file; one numbered item per finding)
1. Re-derive the exemption set and the exit-status table at HEAD `1ce8296`.  Anything changed?
2. For `hpcmips_ctor_probe.py` -> `gate_asan_sweep.sh`: write the gate row as a SKETCH (the `check` line(s), what
   it greps, the pinned denominator if the probe prints a `_RESULT=n/m`), where in the script it goes and why,
   what it costs in wall-clock, and the TWO negative controls -- name the exact mutant of the source (grep
   anchor + the edit) that must red the row, and the HEAD run that must stay green.
3. The same for `fbpending_drain_probe.py` -> `gate_ab.sh`.  `gate_ab.sh` carries a load-sensitive guest-work
   accounting (`LUNA_BUDGET`, `LUNA_STALL`, `LUNA_BACKSTOP`): does adding a probe run inside it perturb that
   oracle, and if so where else could the row live?
4. For the four always-exit-0 wdc probes: for each, what is the SMALLEST edit that makes its exit status
   meaningful (a `sys.exit` on an `ok` it already computes? a new oracle?), and which of the four is a
   one-line change versus a design round?  Then propose the re-date: one date per probe, each tied to a
   concrete plan ("after the altoffset oracle round", not "later"), and the comment text the manifest entry
   should carry so the next expiry is a scheduled event rather than a surprise.
5. If, while verifying a claim, you found something ELSE -- say so.

Do not run gates, builds or probes (three kill tables are using the trees); no patches to apply -- sketches.
