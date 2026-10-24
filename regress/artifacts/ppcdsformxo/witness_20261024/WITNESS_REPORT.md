# ppcdsformxo -- rung-3 witness, DS-form loads (opcode 58), run once on the baseline binary

Date: 2026-10-24.  Probe: `ppc_dsform_probe.py` (this directory).  Run once, foreground, by
`MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/t2/run_dsform_witness.sh`,
which executed `python3 -u ppc_dsform_probe.py /tmp/gxt2/base/gxemul headbin <this dir>`.

**Result: `PPC_DSFORM_RESULT=5/8`, `PPC_DSFORM_CONTROL=OK`, `PPC_DSFORM_SYMPTOM=PRESENT 3/3`,
`PPC_DSFORM_RED=ldu value,ldu RA after,lwa value`; sentinel `PPC_DSFORM_PROBE_DONE` is the last
line of `WITNESS_headbin.out`; probe exit status 1 (`PROBE_RC=1`, by design on any red row).**

## What the probe did

One piped cold-debugger session on the unmodified in-tree `-E bareppc -M 64` (PPC970, 64-bit; the
`reg` readback shows `msr = 0x0`, so physical addressing and SF = 0):

1. seeded r4-r7, r9, r20-r23 and r30 with the sentinel 0x5a5a5a5a5a5a5a5a;
2. filled DATA = 0x20000 .. 0x200ff with a counting byte pattern by `put b` (byte DATA+k = k), and
   `dump`ed it (the dump in `RAW_headbin_main.txt` shows the pattern intact);
3. placed 13 instruction words at CODE = 0x10000 by `put w`, every word produced by the probe's
   `encode(opcode, RT, RA, DS, XO)` -- no typed-in word constants:
   four `lis`+`ori` pairs setting r20, r21, r22, r23 to 0x20080; `ld r4,-112(r20)` (XO 0);
   `ldu r5,-96(r21)` (XO 1); `lwa r6,8(r22)` (XO 2); `lwz r7,8(r23)` (D-form control);
   `li r9,0x1234` last (liveness);
4. `unassemble`d the 13 words, set `pc=0x10000`, `step 13`, `reg`.

Then the same command stream against the bogus machine type `nosuchmachine` (negative apparatus
control).  No store instruction is placed in the guest; the only memory writes are the debugger's
own `put` commands that build the data area and the program.

## Rows

| row | got | want | status |
|---|---|---|---|
| ld value | 0x1011121314151617 | 0x1011121314151617 | ok |
| ldu value | 0x2122232425262728 | 0x2021222324252627 | RED |
| ldu RA after | 0x20080 | 0x20020 | RED |
| lwa value | 0x8a8b8c8d8e8f9091 | 0xffffffff88898a8b | RED |
| lwz value | 0x88898a8b | 0x88898a8b | ok |
| live | 0x1234 | 0x1234 | ok |
| unasm census | 13/13 | 13/13 | ok |
| neg apparatus | exit1/-0x1 | exit1/-0x1 | ok |

## Per instruction: the offset the loaded value names, and RA

Offsets are from DATA = 0x20000; every base was set by the guest to 0x20080.

| instruction | architectural EA | loaded value names | RA after | RA architectural |
|---|---|---|---|---|
| `ld r4,-112(r20)`, XO 0 | 0x20010 (offset 0x10) | doubleword at offset 0x10 | r20 = 0x20080 | 0x20080 (unchanged) |
| `ldu r5,-96(r21)`, XO 1 | 0x20020 (offset 0x20) | doubleword at offset 0x21 | r21 = 0x20080 | 0x20020 (RA <- EA) |
| `lwa r6,8(r22)`, XO 2 | 0x20088 (offset 0x88) | DOUBLEWORD at offset 0x8a | r22 = 0x20080 | 0x20080 (unchanged) |
| `lwz r7,8(r23)`, D-form | 0x20088 (offset 0x88) | zero-extended word at offset 0x88 | r23 = 0x20080 | 0x20080 (unchanged) |

Other observations from the same run: r30 (seeded, never written) = 0x5a5a5a5a5a5a5a5a, so the
seeding took; pc after `step 13` = 0x10034 = CODE + 4 x 13.

## The reds, and whether each is the decode behaviour under test

All three reds are the decode behaviour under test, and the controls that make them attributable
are green (`PPC_DSFORM_CONTROL=OK`):

- **ldu value** -- the value names offset 0x21 = the architectural EA + 1, which is RA + the raw
  low halfword 0xffa1 (-95): the XO bit is folded into the displacement.  The defect, not the
  apparatus: `ld` at XO 0 with a negative DS from the same base value is green, so the DS sign
  extension is decoded correctly and the difference is the XO bits.
- **ldu RA after** -- r21 still holds 0x20080; EA was not written back.  The committed decode
  treats opcode 58 as a non-update doubleword load whatever XO is.
- **lwa value** -- a full doubleword from offset 0x8a = the architectural EA + 2 (RA + raw low
  halfword 0x000a), not the sign-extended word at offset 0x88.  The `lwz` control reads that same
  word correctly (0x88898a8b), so the pattern and the EA are as intended and only lwa's decode
  differs: wrong address (XO folded in) and wrong width and extension.

Corroboration from a separate code path: the `step 13` trace in `RAW_headbin_main.txt` is the
disassembler's running form, and it prints the same folded addresses and values
(`<0x20021: 0x2122232425262728>`, `<0x2008a: 0x8a8b8c8d8e8f9091>`).  The `unassemble` census is
13/13; for the three opcode-58 words the disassembler prints `ld` with displacements -112, -95 and
10, i.e. the XO bits folded into the displacement (an observation about the disassembler: the
census confirms each word's opcode, RT, RA and raw low halfword, not architecture).

Not measured here: the same script against a repaired build (the test-first expectation is that
the three rows go green; that run belongs to the repair round).

## Not covered (the probe's CONTRACT)

- **The store forms `std` and `stdu` (primary opcode 62) are NOT covered** -- no store
  instruction is placed in the guest; stores are a later step.
- The illegal XO values (opcode 58 XO 3; opcode 62 XO 2 or 3); the invalid update forms (`ldu`
  with RA = 0 or RA = RT); 32-bit CPUs; translation on; 64-bit mode (MSR SF set); EAs with a
  non-zero high half; displacements and bases other than those above; page-crossing EAs; the
  indexed forms `ldx`, `ldux`, `lwax`, `lwaux`.

## Baseline receipts (pointers, not copied)

Scratchpad `C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\t2\`:

- `build_base.out` -- the scratch build `/tmp/gxt2/base` (copy of `build/`, the peer's five
  uncommitted files overlaid with HEAD blobs, `src/cpus/*.o` removed, `make` MAKE_RC=0); FRESH
  (`gxemul -nt src/cpus/cpu_ppc_instr.c`); CMP-SEC-OK for the eleven files it lists as exercised by the probe or touched by the fix;
  binary md5 3cd0501cf7c854e0662797ccee1fce64.
- `baseline_scratch_vs_head.txt` -- the scratch tree against HEAD c8fcb5ff: 498 identical,
  1 differing (`src/machines/.index`, generated), the six declared divergence-set paths listed.
- `baseline_build_vs_head.txt` -- the same check on `build/` before the overlay.
- `cpu_ppc_instr.HEAD.c` -- HEAD's `src/cpus/cpu_ppc_instr.c`, md5 87a766e0a8c1f8bbc41ebea8d9255d27,
  equal to the scratch tree's copy.
- `run_dsform_witness.sh` and `run_dsform_witness.out` -- this run's runner and its console output:
  binary md5 re-checked at run time (3cd0501cf7c854e0662797ccee1fce64), FRESH again, no `.MUTANT`
  sentinel in `/tmp/gxt2/base`, `PROBE_RC=1`.

The probe's `elapsed=0.0s` line is its own one-decimal wall-clock figure for both sessions; the
runner's timestamps put the whole run inside one second (06:05:13).  An offline dry run of the
probe's encoder and wants (no emulator) wrote one 4-byte dummy file into the t2 scratchpad.

## Files

- `ppc_dsform_probe.py` -- the probe (LF).
- `WITNESS_headbin.out` -- its full output, ending with the sentinel.
- `RAW_headbin_main.txt` -- the raw main-session transcript (argv and exit header; no carriage
  returns were present).
- `RAW_headbin_neg.txt` -- the negative-apparatus session transcript.
- `ppc_dsform_dummy.bin` -- the 4-byte boot file the probe passes as `0x10000:<file>`.
- `WITNESS_REPORT.md` -- this file.
- `MANIFEST.md5` -- md5 of every other file in this directory.
