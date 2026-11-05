# pvrrenderexit REPAIR 3 -- implementer's note (Opus 5.5 subagent, 2026-11-05 ~08:45-10:10Z)

Brief: measure codex pass 3's A-I first, close the class, add the fewest rows, correct records a-e, run the base and pre-fix legs,
write the gate block as a file, prepare (not run) table 3.  The coordinator added, mid-task: Gemini's swap-body cells (measure the z
deletions first); then, after the first report, a RULING -- add the Z-off twins of every single-layer geometry cell (the 09-04 floor's
cross-product of the dominating predicates with zwrite_disabled), re-run base and pre-fix, re-prepare table 3 with one multi-token
representative per geometry predicate, update the gate block.  Nothing was committed; no git command was run; gate_arm.sh, src/ and
build/ were not edited; no CHANGELOG or ledger entry was written.

## Results

* **Measured first (PVR3_NOTE.md), each on the CURRENT 68-row probe in a WSL scratch clone:** codex's A-I -- **all 15 SURVIVED (68/68)**,
  none refuted; It (texturedline `x < x2 + 1`, codex: EQUIVALENT) green.  The swap body -- **7 of 9 SURVIVED** (z, r, g, b in simpleline;
  z, u, v in texturedline); the x-exchange deletions red `swap` + `s end`.  The closure's own cells W1-W4 per rasterizer -- **all 8
  SURVIVED**.  No red came from a timed-out session or a `none` read.
* **THE STDIN CAP (new finding; wrong record "f").**  A session's debugger input past byte 4100 is swallowed by the Dreamcast maple
  keyboard's first tick (stdin_cap_test{,2}.out; console.c / machine.c / dev_dreamcast_maple.c).  texyedges (repair 2) sent 4104 bytes,
  so every 68-row run since repair 2 took ~90 s (table 1: 0.4 s) while the gate said "about half a second"; its reads precede the cut,
  so table 2's scores stand.  base68's mask timeout was the same cap, so "about 8 TA commands" names the wrong limit.  Repair:
  texyedges stores only the texel it samples; `session()` refuses an input over STDIN_CAP = 4096.  Largest session now 4066 bytes.
* **The closure (CLOSURE3.md; deriver closure_cells.py): 173 input cells** -- codex's 84, 18 added (swap body, both clauses' compare edges,
  decode bits 29-31) and **71 Z-off twins**.  OLD 50, NEW 91, EQUIV 12, DOM 6, UB 4 (row -1, Z-on and Z-off), NN 10.  Beyond codex and
  Gemini: the left clause's compares are equivalent under a move by one but not by two (W3/W4); `x > d->zwrite_disabled` and `y <
  d->zwrite_disabled` drop column 1 / row 0 for Z-off polygons only (W1/W2); the pass-2 rulings' inner-`||` variants, never built.
* **Rows: 60 new, 128 in all; 22 new render sessions, 38 in all.**  The Z-off twins (zedges, zyedges, zswap, zedges2, zleft, zramp and
  their textured twins: 39 rows) repeat each single-layer geometry session with a Z-off header -- every want is its Z-on twin's, since a
  Z-off polygon draws the same pixels and skips only the store -- and zramp / ztramp test a Z-off swap-body span against a depth COVER
  stored first.  The 91-row version's `zleft row 0` pair was dropped (the twins of `t in` and `l in` hold its cells).
* **Base run on build/gxemul: 128/128, CONTROL=OK, SYMPTOM=ABSENT, 3.1 s, no session timed out** (base128/; CLEARANCE.txt: cmp clean +
  binary fresh, re-checked before every base run).  **Pre-fix (det_20261104/dev_pvr.c.HEAD in clone /tmp/gxpvr3f): 60/128,
  SYMPTOM=PRESENT, CONTROL=OK** -- table 2's 26 red rows plus every new row whose session carries a Z-off header (42), exactly the
  predicted set (`pvr_variants_3.py check` on the measured legs: 3 hits of 3).
* **Departures from codex's rows (CLOSURE3.md section 5):** A and B in a new `swap` session (yedges would pass the cap); C through colour
  / u at one pixel; E at RREV's exact first row; G's header 0x0c000000 (culling mode 1); H's header 0xf0000000 (one row for bits 28-31).

## Records corrected

* Probe docstring, in place and quoting what each corrects: codex **a** (55 red on their rows + 3 EQUIVALENT + 4 NOT PREDICTED, 58
  predicted), **c** (PRETABLE order: driver and results only), **d** (texturedline vs pvr_render); "CONTROLS (13)" -> 14; the mask
  split's cause.  The REPAIR 3 CONTRACT lists covered cells (each Z-on and, via its twin, Z-off) and NOT COVERED cells by name; the
  multi-token geometry-x-Z-write disclosure is gone (the twins cover it).
* `../r2_20261105/PRETABLE_2.errata.md` (c; e: Y2's "< 1280" is overbroad) and `../r2_20261105/table2/VERDICT.errata.md` (the cap: the
  texyedges TIMEOUT on every table-2 gxemul leg except Y2t's SIGSEGV; the scores stand).
* codex **b** ("fifteen render sessions" -> 38 now; my own first draft said "twenty-six", also wrong -- it was 28) and **f** ("about half a
  second" -> ~3 s) in `gate_pvr_block.new`.

## For the main loop

1. **gate_pvr_block.new** replaces gate_arm.sh's whole pvrrenderexit block (header comment through its `fi` and the two blank lines; at
   2120-2151 at ~09:50Z, byte-identical to `gate_pvr_block.pre_r3`).  Changed: the comment, the four pins 68 -> 128, the names list
   (ONE line, 128 names in base-run order).  `gate_block_sim.sh` replays its checks: base128 137/137, head128 72 fail.  `bash -n` passes.
2. **Table 3 (prepared, NOT run):** `cp table3_pvr.sh table3_pvr.run.sh`, run from `run_in_background` under WSL (command in its header);
   clone /tmp/gxpvr4 (absent), clone-local .MUTANT first; refuses without PRETABLE_3.out, the frozen instrument
   table3/probe128_frozen.py, or a matching INSTRUMENT_MD5.  **128 variants**: table 2's 62 by copy; 66 new, each one exact edit of
   dev_pvr.c.fix3 whose text occurs once in its function -- A-I, swap body, W1-W4 (byte-identical to the measured files), 19 closure
   representatives, and **14 multi-token V variants** (a P1-P7 bound moved by 2 * d->zwrite_disabled, one per predicate per
   rasterizer).  All 66 pass `cc -fsyntax-only` with build/'s flags (syntax_check_V.sh).  PRETABLE_3.out (rewritten after the frozen
   probe, before any table output; the 91-row version kept in superseded_91/): **124 predicted EXACTLY (119 red, 5 EQUIVALENT green:
   M17, L1s, L1t, It, H65), 4 NOT PREDICTED (Y2s, Y2t, Y4s, Y4t)**; legs base 128/128, HEAD 60/128 (measured), null media 9/0/1.  The
   driver ends with `pvr_variants_3.py check` (CHECK.txt: PRED=MISS lines and a tally; tested under WSL python3).
3. Propagation: only regress/pvr_zwrite_probe.py changed in the tree (est/ owes the copy at landing).

## Intermediate artifacts (kept, not cited as the record)

base85/, head85/ (85 rows, before W1-W4); base91_v1/, head91_v1/ (a zleft design that put row-0 columns at negative x -- the inner-`||`
variant would have read vram_z[-30..-1]; replaced); base91/, head91/ (the 91-row version, with earlier/ subdirs for unfinished
docstrings); base128/earlier/, head128/earlier/ (the final code with the legs sentence still pending; AST-equal to the final file).

## Clones

/tmp/gxpvr3 (A-I), 3b (swap body), 3c (HEAD 85), 3d (W1-W4), 3e (HEAD 91), 3f (HEAD 128): each restored by its driver (cp from
GXEMUL-SEC, cmp clean, rebuilt, `[ gxemul -nt source ]`, sentinel cleared), re-checked (clones_status.sh), then removed
(clones_cleanup.out, clone_rm_3f.sh).  build/ was only read.
