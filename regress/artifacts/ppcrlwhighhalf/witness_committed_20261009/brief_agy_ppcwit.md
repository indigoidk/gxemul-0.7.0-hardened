# Measuring job: a rung-3 witness for `rlwinm` / `rlwnm` on committed HEAD (row `ppcrlwhighhalf`)

Open your answer with `VERDICT: WITNESSED / NOT WITNESSED / APPARATUS FAILED`, then the table below, then the paths.

## What this is

GXemul is a C emulator; the hardened fork lives at `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\` (git HEAD `200671b6`).
Ignore any other `src/` under `C:\DocumentNoSnc\cc\GXEMUL\` -- those are pristine 2021 upstream copies.

The PowerPC handlers for `rlwinm` and `rlwnm` (`src/cpus/cpu_ppc_instr.c`, search for `X(rlwinm)` and `X(rlwnm)`) compute
the rotated-and-masked value as a `uint32_t` and store it into the 64-bit register.  PowerPC Book I v2.01 (`:4125-4137`)
defines `r <- ROTL32((RS)[32:63], n); m <- MASK(MB+32, ME+32); RA <- r & m` at 64 bits, where ROTL32 duplicates the
rotated word into BOTH halves and MASK wraps when MB > ME.  So a WRAPPING mask should keep high-half bits that the
32-bit computation drops.  The job is to MEASURE what committed HEAD does, before anyone changes the handler.

## Hard rules

* READ-ONLY on the project: never create, change, move or delete anything under `C:\DocumentNoSnc\cc\GXEMUL`.  Your only
  writable directory is the work directory named in the prompt.
* Do NOT build the emulator.  The binary is prebuilt from committed HEAD `200671b6` (a `git archive`, so no uncommitted
  working-tree content): WSL path `/tmp/gxppcwit/gxemul`, built in WSL distro `Gentoo`;
  `src/cpus/cpu_ppc_instr.c` there has md5 prefix `87a766e0`, the same as `git show HEAD:src/cpus/cpu_ppc_instr.c`.
  Re-check both before running: `MSYS_NO_PATHCONV=1 wsl -d Gentoo -- md5sum /tmp/gxppcwit/src/cpus/cpu_ppc_instr.c`.
* Everything in the FOREGROUND; wait for each command to finish; do not end before your probe printed its sentinel.

## How to build the probe (copy, do not import, and do not edit the committed file)

Copy the harness from the committed `GXEMUL-SEC\regress\ppc_rlwimi_probe.py` into a NEW file in your work directory,
`ppc_rlwhigh_witness.py`: its `session()` function (cold debugger: `put w`, `unassemble`, `pc=`, `step N`, `reg`), the
`DUMMY` stub, `CODE = 0x10000`, the `row()` printer, the encoders `enc_m`/`RLWINM`/`LI`/`ORI`, and the architecture
helpers `rotl32`/`mask_range`/`mask32`/`want_rlwinm`.  Add an `RLWNM(ra, rs, rb, mb, me, rc=0)` encoder: opcode 23,
format M with RB in the SH field.  Machine: `-E bareppc -M 64`, unmodified (default CPU PPC970, 64-bit, MSR[SF]=1 as the
committed probe's header records).  Run it from WSL:
`MSYS_NO_PATHCONV=1 wsl -d Gentoo -- python3 -u <work dir in /mnt/c form>/ppc_rlwhigh_witness.py /tmp/gxppcwit/gxemul`
and keep the complete output as `witness.out` in the work directory.  Print `PPCRLWHIGH_WITNESS_DONE` as the last line.

## Rows (one session per row is fine; seed r4 with the sentinel `0x5A5A5A5A5A5A5A5A` unless stated)

| row | instruction(s) | setup | want (Book I) | predicted HEAD |
|---|---|---|---|---|
| `pvr` | `mfspr r6, 287` | -- | `0x00390000` (PPC970, `src/include/cpu_ppc.h`) | same |
| `live` | `li r9, 0x1234` placed AFTER the target in the `target.` session | r9 = sentinel | `0x1234` | same |
| `disasm` | the tree's own `unassemble` of the `target.` word | -- | mnemonic `rlwinm.`, operands `r4,r3,1,31,0` | same |
| `nowrap` | `rlwinm r4,r3,1,0,31` | r3 = 1 | `0x2` (small nonzero: proves the register fields) | `0x2` |
| `target.` | `rlwinm. r4,r3,1,31,0` (Rc=1; word should be `0x54640fc1` -- check it against your encoder) | r3 = 1, XER = 0 | r4 = `0x0000000200000000`, CR0 nibble `4` (GT) | r4 = `0x0`, CR0 `2` (EQ) |
| `target` | `rlwinm r4,r3,1,31,0` (Rc=0) | r3 = 1 | `0x0000000200000000` | `0x0` |
| `rlwnm1` | `rlwnm r4,r3,r5,31,0` | r3 = 1, r5 = 1 | `0x0000000200000000` | `0x0` |
| `rlwnm33` | `rlwnm r4,r3,r5,31,0` | r3 = 1, r5 = 33 (only RB's low 5 bits count) | `0x0000000200000000` | `0x0` |

Score every row against the Book I column using the copied `want_rlwinm` (it already implements the 64-bit wrapping
mask), and ALSO print the predicted-HEAD column beside it.  Print the CR value from `reg` and the CR0 nibble (its top four
bits).  If the `reg` dump does not show `cr`, say so rather than inventing a value.

## What to report

1. The table: row, got, Book I want, predicted HEAD, and whether got matches Book I.  Which rows show the high half lost?
2. The controls: did `pvr`, `live`, `disasm` and `nowrap` all come out right?  If any control failed, the verdict is
   APPARATUS FAILED, whatever the target rows say.
3. Exact paths of `ppc_rlwhigh_witness.py` and `witness.out`, and the md5 you measured for the binary's
   `cpu_ppc_instr.c`.
4. Anything that surprised you, as a line of its own starting `FLAG:`.
