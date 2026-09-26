# #549 -- the §F2 pass, MEASURING seat (fresh start; the earlier seat stopped before measuring anything)

Open with `OPUS549F2_ALIVE`, then `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then numbered findings, each marked
**measured** or **read**, under ~1000 words.

**The work is mutation testing of a C emulator's framebuffer-controller register decode.**  The tree is
`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\` (ignore any other `src/` under the project root).  The fix is UNCOMMITTED in
that working tree: `src/devices/dev_fbctrl.c` and the new detector `regress/fbctrl_port_probe.py` (41 rows).

**READ-ONLY for everything under `C:\DocumentNoSnc\cc\GXEMUL\`**, with one exception: write your logs and any row
prototypes to `GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/f2/` (and nowhere else in the
project).  Build and run ONLY in a WSL `/tmp` clone (`MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/...script`; put
scripts in f2/ and run them from there).  Build traps: `rm src/cpus/*.o` before `make`; after every build check
`[ gxemul -nt src/devices/dev_fbctrl.c ]`, because make has been seen to report 0 on a failed build; `cmp` the clone's
dev_fbctrl.c and probe against the working tree before your first run and say so.  Long runs: foreground only.

## What to read (all under `GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/`)

* `f2_brief.md` -- every pass-2 finding with my disposition on each (records R1-R6, apparatus P1-P3, rows D1-D11).
* `panels/codex_f2astra.txt` -- the Astra adjudication; `panels/grok_dedicated_f2.txt` -- the dedicated grok ruling.
  Both say several of my proposed rows would STAY GREEN on the very device edit they target (D2, D3, D7, D9's
  serial_nr clause, D10) and give corrected forms.
* `opus549_measured/p2/variants.diff` and `probe_N_*.out` -- the variants a previous measuring pass built
  (N_datarearm, N_clobcell, N_clobcmd, N_runcmd, ...), all 41/41 on the shipped probe.

## The questions -- MEASURE, do not argue

1. For each D-row in the CORRECTED form Astra/grok give (D2 `sd 0x8000000000000000` after PORT=5; D3 a guest `lw` of
   PORT inside session F into a poisoned register; D4 a DATA write plus a NOP command between two refusals; D5 a
   fill-then-readback of every port plus X1=123 surviving a refusal; D6 an `ld` of PORT; D7 a NON-ZERO predecessor
   before each zero-selector store via `sb` and `sd`; D8 previous-6 and previous-7; D9 twelve refusals; D10 a broad
   announce counter plus a separate first-value check; D11 the Y1 read): build its TARGET device edit, prototype the
   row in a COPY of the probe, and report **red on the target edit / green on the fix** -- or which form is still
   vacuous.  Then run the p2 variants against your prototype.
2. Is a SECOND fbctrl instance reachable without adding a device -- two unmodified `-E testmips` machines in one
   process via a config file?  Try it.  If it works, does a per-device latch show one announce per instance, and does
   any shipped announce-count row go red on a CORRECT build there (e.g. a count that assumes one instance)?
3. The record-validation finding: `p2/out_row_deleted.txt` (a row deleted, trailer still 41/41).  Confirm whether the
   gate-16 block passes it, and name the smallest reconciliation (emitted row lines vs. the trailer) that reds it
   without redding `out_good.txt`.

Say plainly which findings are readings.  If something cannot be built or run, say so and stop that item.
