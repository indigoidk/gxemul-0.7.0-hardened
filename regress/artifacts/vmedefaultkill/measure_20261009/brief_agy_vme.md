# Measuring job: what the OpenBSD/mvme88k guest's seven VME2 register accesses do today, and under two sketch dispositions

Open your answer with `VERDICT: MEASURED / APPARATUS FAILED`, then the tables below, then the paths, then `FLAG:` lines.

## Why

GXemul (the hardened fork at `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`, git HEAD `200671b6`; ignore any other `src/`
under `C:\DocumentNoSnc\cc\GXEMUL\`) models the MVME187's VME2 chip in `src/devices/dev_vme.c`.  Its `default:` arm --
every offset with no `case` -- prints with `debug()` (invisible at default verbosity) and then calls `exit(1)`, ending
the emulator.  The in-tree guest source `_guest-src-openbsd22/sys/arch/mvme88k/dev/vme.c` makes these accesses to
offsets that have no `case` (VME2 base `0xfff40000`; offsets from `src/include/thirdparty/mvme88k_vme.h`):

| site | guest code | access | offset |
|---|---|---|---|
| A1 | `vme2chip_init`: `ctl = vme2->vme2_masterctl` | 32-bit read | MASTERCTL 0x28 |
| A2 | `vme2->vme2_master3 = ...` | 32-bit write | MASTER3 0x1c |
| A3 | `vme2->vme2_master4 = ...` | 32-bit write | MASTER4 0x20 |
| A4 | `vme2->vme2_master4mod = ...` | 32-bit write | MASTER4MOD 0x24 |
| A5 | `vme2->vme2_masterctl = ctl` | 32-bit write | MASTERCTL 0x28 |
| H1 | `vme2abort`: `if (!(vme2->vme2_irqstat & VME2_IRQ_AB))` | 32-bit read | IRQSTAT 0x68 |
| H2 | `vme2->vme2_irqclr = VME2_IRQ_AB` (only when the AB bit is set) | 32-bit write | IRQCLR 0x74 |

The project owner asked for a MEASUREMENT before choosing what these accesses should do.  Your job is to measure three
binaries -- nothing is being fixed here, and two of the binaries are deliberately throwaway sketches.

## Hard rules

* READ-ONLY on the project: never create, change, move or delete anything under `C:\DocumentNoSnc\cc\GXEMUL`.  Your only
  writable directory is the work directory named in the prompt.
* Do NOT build anything.  Three prebuilt binaries, all in WSL distro `Gentoo`:
  * `HEAD`    `/tmp/gxppcwit/gxemul`    -- committed source (`git archive 200671b6`).
  * `FAULT`   `/tmp/gxvme_fault/gxemul`   -- same, with the `default:` arm's `exit(1);` replaced by `return 0;`, so
    `memory_rw` raises the m88k data-access exception (`src/cpus/memory_rw.c`, the `#ifdef MEM_M88K` arm).
  * `DECLINE` `/tmp/gxvme_decline/gxemul` -- same, with `exit(1);` replaced by `odata = 0; break;`, so a read returns 0
    and a write is dropped.
  `diff` each tree's `src/devices/dev_vme.c` against `/tmp/gxppcwit/src/devices/dev_vme.c` first and report it.
* Everything in the FOREGROUND; wait for each command; do not finish before your probe printed its last line.

## How to build the probe (copy, do not import, and do not edit any committed file)

Copy the cold-debugger harness from the committed `GXEMUL-SEC\regress\mk48_nvram_probe.py` (its `session()` runs
`-E mvme88k -e mvme187 -M 64` -- the UNMODIFIED in-tree machine -- feeds debugger commands, and parses the register
dump; read how it places instructions and seeds registers) into a NEW file in your work directory,
`vme_sites_probe.py`, and run it from WSL with `MSYS_NO_PATHCONV=1 wsl -d Gentoo -- python3 -u <work dir in /mnt/c
form>/vme_sites_probe.py <binary> <label>` once per binary.  Keep each run's complete output as
`run_<label>.out` in the work directory; the last line of each must be `VME_SITES_DONE`.

For EACH of the seven sites, ONE session per binary: seed `r3` = the register's address (`0xfff40000 + offset`), for
a write seed `r2` = a distinctive value (`0x5a5a1234`), for a read seed `r2` = a sentinel (`0xdeadbeef`); place the
32-bit `ld r2,r3,0` or `st r2,r3,0`, then `or r4,r0,0x1234` (liveness); step 2; dump registers.  Record:
1. did the emulator process survive (exit status / whether the `reg` dump arrived)?
2. the PC after the step -- did it continue to the liveness instruction, or vector?  (m88k vectors are at
   VBR + 8 * vector; the data-access exception is vector 3.  Read VBR and say what it was.)
3. for a read: `r2` after the step; for every site: `r4` (liveness).
4. under FAULT only: whatever the model records about the fault -- the 88100 data-unit fault registers if the
   register dump shows them (DMT0 / DMD0 / DMA0), and the data CMMU's fault status and fault address as a GUEST LOAD
   would read them (find the CMMU's address in `src/machines/machine_mvme88k.c` and the PFSR / PFAR offsets in the
   tree's m8820x headers; read them with a guest `ld` in a second session after the fault, not with the debugger's
   `dump`).  The guest's own handler reads that status (`_guest-src-openbsd22/sys/arch/mvme88k/mvme88k/eh.S` near
   line 1009) and `trap.c` decides from it whether to recover or `panictrap()` (near line 292 and 368).  Say what the
   handler would see; do not guess what it then does beyond what the source says.

**Controls, in every binary:** (a) a CASED register round-trip -- `st` `0x12345678` to T1CMP (offset 0x50) and `ld` it
back: it must read `0x12345678` in all three binaries (proves the device decode reaches `dev_vme.c`); (b) the
liveness `or` in every session; (c) the tree's own `unassemble` of each placed word must show the intended `ld` /
`st` with `r2,r3,0` -- the hand-assembled-encoding trap is real here, and a wrong register field reads 0.

## What to report

1. A table, one row per site x binary: survived?, PC after, r2 (reads), r4, and the FAULT-only fault record.
2. The controls' results, per binary.  If any control fails, the verdict is APPARATUS FAILED.
3. Separately for ATTACH (A1-A5) and for the ABORT HANDLER (H1-H2), in plain words: what the guest would experience
   under each binary, citing only what you measured plus the guest source lines it rests on.  Under DECLINE, say what
   value IRQSTAT reads and what `vme2abort` therefore does next, quoting its source.
4. Exact paths of `vme_sites_probe.py` and the three `run_*.out`, and the md5 of each tree's `dev_vme.c`.
5. Anything that surprised you, each as its own line starting `FLAG:`.
