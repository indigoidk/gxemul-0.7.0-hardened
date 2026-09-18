# opus_p2_20260918 -- Opus measuring seat, `#530` closing pass 7 (the width row `lca_widewrite_probe.py`)

Tree measured: GXEMUL-SEC `8bd97e4`.  Scratch clone `/tmp/gxopus530p2` (a `cp -a` of `build/`); its
`src/devices/dev_lca.c` was `cmp`-clean against GXEMUL-SEC and against the `8bd97e4` blob before any variant
(md5 `8084ff07...`, `logs/setup.out`).  Every other file on the path (memory.c, memory_rw.c, the Alpha CPU,
machine_alpha.c, ns16550, 8259, pckbc, pccmos, bus_isa, bus_pci, main.c) is `cmp`-identical to `8bd97e4`
except `cpu_alpha_palcode.c`, which differs by a 23-line insertion INSIDE an existing block comment (identical
to the GXEMUL-SEC working tree) -- no code difference.  Base rebuilt in the clone first (`logs/setup.out`:
`gxemul` and `dev_lca.o` newer than `dev_lca.c`), and base scored full marks on every cell: that is the
construction control.  No `.bin` is stored here; the probes need `regress/alpha_dummy.bin` beside them.

## Order of evidence

`PREDICTIONS.txt` was CREATED at 18:25:33 (`PREDICTIONS.stat.txt`, Birth) -- before the first leg (18:26:09).
It was then APPENDED three times, so its mtime is NOT the order proof; each addendum says what had run when
it was written: ADD1 18:27:21 (after only the four base smoke legs in `logs/smoke/`, before any variant leg at
18:27:53); ADD2 before the vb/vd/vf/vh builds at 18:30:17; ADD3 18:33:46, before any vb/vd/vf/vh leg.
Every leg ends in its completion sentinel (`WIDEWRITE_DONE` / `WIDECELL_DONE`); `summarize.py` checks it.

## Files

* `variants/*.diff` -- the one-edit variants (va..vh from the brief's Q1; vt1/vt2 the teammate shapes;
  vw64/vw256 a width ladder).  `scripts/mkvariants.py` generates them from the `8bd97e4` blob, each edit an
  exact-string replacement that must match exactly once.
* `lca_widecell_probe.py` -- the FROZEN width row generalised to the other wide cells.  Harness, encoder,
  GETENV phase and retry rule copied from `8bd97e4:regress/lca_widewrite_probe.py`; WANT is derived by
  replaying `store_buf()`'s chunking and applying the SHIPPED rule, never typed in.
* `logs/<cell>__<binary>.log` + `raw_*` pty transcripts; `logs/matrix*.out` (run order); `logs/bins.md5`.
* `scripts/` -- setup, build, run, restore, collect.

## Results -- 102 legs, every value matched its prediction, zero retries, all sentinels present

`RESULTS.txt` (from `scripts/summarize.py`): score and getenv value(s) per (cell, binary).  The ONLY rows that
ever went red are `getenv` rows (30 of them); every `alive` and `live` (control) row is green on all 13 binaries.

    cell     base      va        vb        vc        vd        ve        vf        vg        vh        vt1       vt2       vw64   vw256
    frozen   3/3 44    3/3 44    3/3 44    3/3 44    3/3 44    3/3 44    2/3 41    3/3 44    3/3 44    3/3 44    3/3 44    3/3    3/3
    k16      3/3 44    3/3 44    3/3 44    3/3 44    3/3 44    3/3 44    2/3 41    2/3 5a    3/3 44    2/3 5a    3/3 44    3/3    3/3
    l0w16    3/3 41    3/3 41    .         2/3 03    .         3/3 41    .         3/3 41    .         3/3 41    3/3 41    .      .
    l0w64    3/3 41    2/3 03    2/3 03    2/3 03    3/3 41    3/3 41    3/3 41    3/3 41    3/3 41    3/3 41    3/3 41    3/3    3/3
    l2w64    3/3 f3    2/3 b0    .         2/3 b0    .         3/3 f3    .         3/3 f3    .         3/3 f3    3/3 f3    3/3    3/3
    low16    3/3 42    3/3 42    .         2/3 ff    .         2/3 ff    .         3/3 42    .         3/3 42    3/3 42    .      .
    mc2      5/5 54/f3 5/5 54/f3 5/5 54/f3 4/5 54/b0 5/5 54/f3 5/5 54/f3 3/5 51/f1 4/5 54/b0 5/5 54/f3 4/5 54/b0 4/5 5a/f3 .      .
    kbc16    3/3 41    3/3 41    .         2/3 04    .         2/3 04    .         3/3 41    .         3/3 41    3/3 41    .      .
    kbc256   3/3 41    2/3 04    .         2/3 04    .         2/3 04    .         3/3 41    .         3/3 41    3/3 41    2/3    3/3
    kbc1024  3/3 41    2/3 04    2/3 04    2/3 04    3/3 41    2/3 04    3/3 41    3/3 41    3/3 41    3/3 41    3/3 41    2/3    2/3

**What it shows.**
* The shipped width row (`frozen`) distinguishes NONE of va, vb, vc, ve, vg, vt1, vt2 -- 3/3 on all seven.
  It distinguishes vf (2/3, 0x41 = s[0] where s[3] = 0x44 is wanted).  vd and vh are EQUIVALENT at every cell.
* Each undistinguished variant is killed by the SAME GETENV instrument at another reachable cell on unmodified
  alphabook1: va/vb at C = 64 (l0w64, l2w64) and above; vc at C = 16 lanes 0/1/2 (l0w16, low16, mc2's MSR,
  kbc16); ve at a port < 0x200 (low16, kbc16); vg and vt1 at k = 16 (k16, mc2's MSR); vt2 at the second chunk
  of a multi-chunk write (mc2's SCR).
* The ladder MEASURES which widths reach lca_isa whole: 16 (va green at frozen), exactly 64 (va red, vw64 green
  at l0w64), exactly 256 (vw64 red, vw256 green at kbc256), > 256 at kbc1024 (vw256 red; <= 1024 by the 1 KB split).
* Minimal killing set: {mc2, kbc1024} reds every built escape (va vb vc ve vg vt1 vt2) and vf; both fit in ONE
  session with a 1024-character -o string.
* 9 of the brief's 12 (C, k, lane) write cells were driven and observed (C16: L0k0, L1k0, L2k16, L3k0, L3k16;
  C64: L0, L2; C256: L0; C1024: L0).  The other three (C16 L0k16, L1k16, L2k0) use the same registers at the
  same ports with k changed -- derived, not run.

## Restore

`logs/restore.out`: clone `dev_lca.c` restored from GXEMUL-SEC, `cmp` rc 0, rebuilt, `gxemul` and
`dev_lca.o` newer than the source, the rebuilt binary is md5-IDENTICAL to the base binary measured
(`c6bcdbdf...`), sentinel removed.  Nothing under GXEMUL-SEC except this directory was written.

## Cells

| cell | register | C | k | lane | port |
|---|---|---|---|---|---|
| frozen | the shipped row itself, run as shipped | 16 | 0 | 3 | 0x2ff SCR |
| k16 | SCR | 16 | 16 | 3 | 0x2ff |
| l0w16 | MCR | 16 | 0 | 0 | 0x2fc |
| l0w64 | MCR | 64 | 0 | 0 | 0x2fc |
| l2w64 | MSR (reads back OR 0xb0) | 64 | 0 | 2 | 0x2fe |
| low16 | 8259 IMR | 16 | 0 | 1 | 0x21 |
| mc2 | SCR + MSR, one 32-byte GETENV = two 16-byte chunks: 0x2fe k16 lane 2 <- s[2], then 0x2ff k0 lane 3 <- s[19] | 16+16 | 16,0 | 2,3 | 0x2fe, 0x2ff |
| kbc16/256/1024 | 8042 command byte (sequenced through the FLAT mapping; the GETENV is the only lca_isa access) | 16/256/1024 | 0 | 0 | 0x60 |

## This seat's Q2 ruling (recorded here so it survives the relay)

**No L2.  Three L4s.**  The joint-cells letter decides which cells are floor: the write body tests `len` only
against 0 (and `% len` separates 1 / 2 / 3 / >=4), so every width >= 4 is one body class and a threshold at 8,
16, 64 or 256 is a partition the body never tests.  Pass 6's "diverges only OUTSIDE the probed set" is read by
its own stated reason -- "(uncatchable, so it cannot be discharged that way)" -- as a condition on clause (e):
a contract line can discharge only a variant some SHIPPED INSTRUMENT can reach.  That is what made `len <= 8`
L2 (no instruction reaches len > 8) and it is now MET: every escape above is killed by the same GETENV
instrument at another reachable cell (measured).  Read literally as a floor rule instead, "probed width set"
privileges the width axis for no reason the body supplies (the only thing that ever made width special was
the STQ = 8 instrument boundary), and the same reading on ports or on a<4:0> would contradict the parent's
flagship-ruled class disclosures (p_port10, lcaisasize / H1b).

The L4s (prose claiming coverage a measurement refutes):
1. `lca_widewrite_probe.py` DESIGNED TO CATCH "any guard that declines a len > 8 WRITE ... in either the guard
   form or the write-arm-conjunct form" -- refuted by vc, ve, vg, vt1, vt2 (and va/vb), each such a guard,
   each 3/3.
2. Its clause (iii) warrant "the others share the same `len > 8' predicate" -- refuted by va/vb and by the
   ladder (thresholds at 16, 64, 256 are all invisible to the row).
3. The parent header "The width cell is therefore COVERED, not merely disclosed" -- one of twelve write cells
   is rowed.

If the adjudicator instead reads pass 6 by its WORDING, va/vb are L2, the class-closure amendment applies, and
the cell set for one diff is the producer's (C, lane) write cells -- C16 x lanes 0-3, C64 x lanes 0/2, C256 x
lane 0, C1024 x lane 0 (8 rows, registers named in the Cells table) -- plus k = 16 at one lane and one two-chunk
write (kills the vg/vt1 and vt2 shapes); disclosed with warrant: k = 16 at the other lanes (a<4:0>, discarded),
port values and ranges (p_port10: the body never tests the port against a constant), chunk index beyond 2 and
the forwarded byte's value (never NUL for a wide chunk; argv carries no 0 byte), and the READ side (no producer).
