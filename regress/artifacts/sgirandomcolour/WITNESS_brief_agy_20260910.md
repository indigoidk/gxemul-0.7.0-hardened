# sgirandomcolour -- BUILD THE RUNG-3 WITNESS (agy measuring seat, bounded task)

You are the agy measuring seat on the GXemul hardened fork. Both Anthropic measuring seats are walled
until 03:00 America/Chicago; you are the fallback measuring seat on an independent transport. This is a
bounded task: build ONE probe, run it against the committed binary READ-ONLY, report. If any step cannot
be done, say so plainly and stop -- do not improvise a different measurement.

## HARD RULES
* THE TREE is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` (git root). Ignore any other `src/` under the project
  root (pristine 2021 copies). NEVER write into `GXEMUL-SEC/src`, `est/`, `build/`, `build-asan/`.
* Write ONLY: the new file `GXEMUL-SEC/regress/sgi_re_colourdefault_probe.py`, the directory
  `GXEMUL-SEC/regress/artifacts/sgirandomcolour/witness_20260910/` (your driver script, logs, a frozen
  `.asrun.py` copy of the probe), and a report `GXEMUL-SEC/regress/artifacts/sgirandomcolour/agy_witness_20260910.md`.
* Do NOT build anything. Use `C:\DocumentNoSnc\CC\GXEMUL\build\gxemul` READ-ONLY (WSL path
  `/mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul`). It is the current build of the fork with `dev_sgi_re.c`
  at HEAD (`#518` changed only `dev_lca.c`). A kill table is running in `/tmp/gxopus518*` -- leave those
  directories alone; expect the machine to be loaded, so use generous settle times.
* Run under WSL: `MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/<script>.sh` with a script file (the
  default distro has no `make`/python); never `wsl -c` with `$VARS` inline. Put scripts under
  `C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\`.
* Ordinary bounds-correctness engineering on a device model; describe it as such.

## THE DEFECT (settled by three panels; verify the code by reading)
`src/devices/dev_sgi_re.c`, `horrible_getputpixel()`: the PUT branch switches on the colour-type nibble of
the DE mode word (`color_mode = mode & DE_MODE_TYPE_MASK`, mask 0xf0). Four cases are implemented (CI,
RGB, RGBA, ABGR); the `default:` arm assigns `buf[0..3] = random()` and lets the common tail write those
bytes to guest memory, after a per-pixel `fatal()` that RETURNS (`src/core/debugmsg.c`, no exit). Twelve of
the sixteen nibble values reach it, including the documented `DE_MODE_TYPE_YCRCB` (`crmfbreg.h`). So a
guest that programs a documented colour type and draws one pixel gets four host-PRNG bytes in its
framebuffer/tile memory.

## THE INSTRUMENT TO COPY
`regress/sgi_mte_fill_probe.py` (the `#509` detector, 16 rows, unmodified `-E sgi -e ip32`): reuse its
session wrapper, its `store()`/`load()` builders, its `Addr`/`CODE` conventions, its `row()`/summary/
sentinel shape (`<NAME>_RESULT=n/m`, then `<NAME>_DONE`), and especially its DE/MTE programming idiom --
how it sets a TLB entry, pre-paints the destination with a known pattern, programs the mode register and
fires a transfer, then reads the destination back and scores one byte. Read it FULLY first. Also read
`regress/sgi_re_rgb_probe.py` (`#505`), which drives the DE (not MTE) path through `horrible_getputpixel`
with the RGB type -- that is the path you need, with the type nibble changed.

## ROWS (a witness, not yet a detector)
1. `live` -- the same DE PUT with a SUPPORTED type (RGBA or CI, whichever `sgi_re_rgb_probe.py` already
   drives) lands its known colour in a pre-painted destination: liveness + device signature.
2. `ycrcb put` -- the same PUT with the type nibble `DE_MODE_TYPE_YCRCB` (0xf0 per `crmfbreg.h`; verify the
   value and the shift) into a destination pre-painted with a sentinel pattern. Want: the destination is
   UNCHANGED (the honest post-fix behaviour: a declined PUT skips its store). On HEAD it will be neither
   the sentinel nor any packing of the colour -- RED, the defect. Print the four bytes read back.
3. `ycrcb attrib` -- the transcript carries the arm's own diagnostic text (read the exact `fatal()` string
   in the `default:` arm) so the death of the pattern is attributed to THIS arm.
4. `reserved put` -- one more unsupported nibble (a reserved encoding, e.g. 0x50 if it is not a case) with
   the same want, so the row set covers a documented AND an undocumented value.
5. `determinism` -- run the `ycrcb put` session twice in one probe and report whether the four bytes are
   identical across runs (unseeded `random()` is deterministic per process; say what you observe, do not
   assert what it should be).
Give every row a one-line note. Print the per-row lines, then `SGICOLOUR_RESULT=n/m`, then
`SGICOLOUR_DONE`. Exit 0 iff all rows pass.

## PROCEDURE
1. Read `dev_sgi_re.c`'s `horrible_getputpixel` and the two probes. 2. Write the probe. 3. Run it
against `build/gxemul` twice; save to `witness_20260910/HEAD_run1.out` and `HEAD_run2.out`; check the
sentinel is the last line of each. 4. Freeze a copy as `witness_20260910/sgi_re_colourdefault_probe.asrun.py`.
5. Report: the row table (got/want), the four bytes seen at `ycrcb put`, whether they were the sentinel /
a colour packing / neither, the attribution text seen, and anything unexpected (a death for a DIFFERENT
reason is a failed reproduction and must be labelled so). State what you read versus what you assumed.
