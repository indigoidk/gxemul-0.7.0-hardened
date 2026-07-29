# Guest images used by the harness

These are not in the repository — they run from 2 MB to 2 GB. Put them in `_images/`.
Gates that cannot find their image report `SKIP`, never `PASS`.

## OpenBSD 7.7 / luna88k — m88k (M88100)

The highest-value image in the set. `cpu_m88k_instr.c` stores `IEEE_FMT_S`, so it uses the
exact `float_emul.c` arm #287 changed, and before this rig existed that arm had **no
non-MIPS execution coverage at all**.

* `liveimage-luna88k-raw-20250518.img` — 2,147,483,648 bytes unpacked (ships gzipped)
* `boot` — 70,820 bytes. This is the LUNA-88K boot **program**, a file that must sit
  beside the image; it is not a gxemul keyword. Getting that wrong looks like a boot
  failure.

```
cd _images
gxemul -e luna-88k -d R:liveimage-luna88k-raw-20250518.img boot
```

**The `R:` prefix is required for any harness use**, and omitting it caused a real
non-deterministic gate failure. Plain `-d` opens the image read/write, so every boot
mutates the shared 2 GB file and later runs inherit the previous run's filesystem state.
`R:` opens the base read-only and discards guest writes into a temporary overlay. See
`README.md`.

Boots to a `login:` prompt in roughly three to four minutes. The root password is not set,
so `root` then Enter gives a shell. `awk` is present, which is what makes the in-guest FP
check possible:

```
awk 'BEGIN{printf "%.6f %.6f", 1.5/3.0, 2.0**0.5}'   ->   0.500000 1.414214
```

**Upstream GXemul 0.7.0 cannot boot this image.** Measured unbuffered over 300 s, it emits
its 699-byte startup banner and no guest output whatsoever, while both fork builds reach
`login:` with identical markers. `gate_ab.sh` asserts that as the expected baseline rather
than flagging it as a failure.

The tempting explanation is wrong, and was checked rather than assumed: the fork's m88k
signed-shift and shift-by-32 UB corrections (#36–40, #46) are *not* the cause. Pristine
rebuilt with `-O2 -fwrapv -fno-strict-overflow -fno-strict-aliasing` compiles clean and
still produces nothing but the banner. Whatever fixed luna88k is a genuine source change
inside the first hardening commit, not a compiler exploiting undefined behaviour.

## OpenBSD 7.6 / landisk — SuperH (SH4)

* `openbsd76-landisk-bsd.rd` — 2,188,323 bytes

```
cd _images
gxemul -E landisk -M 64 openbsd76-landisk-bsd.rd
```

Boots the RAMDISK kernel through a full device probe to:

```
(I)nstall, (U)pgrade, (A)utoinstall or (S)hell?
```

Answering `S` gives a shell — but **the rig deliberately sends no input**, because the
emulated SuperH console loses guest writes non-deterministically. Measured on one boot with
ten commands of increasing length: the 15, 23 and 33 byte lines ran, the 9, 17, 27 and 41
byte ones vanished whole. That is a bug candidate in its own right and is written up in
`OUTSTANDING_BUGS.md`; an intermittent gate would be worse than a narrow one.

So the rig asserts the boot instead, checking a value the guest's own device probe prints:

```
shpcic0 at mainbus0: HITACHI SH7751R
```

That proves the SH4 core executed a full kernel boot through device attachment. Separately,
**no in-guest FP test is possible on this media** even if input were reliable — the install
ramdisk was probed and has no `awk`, `perl`, `bc`, `dc` or `python`.

## NetBSD 4.0.1 / macppc — PowerPC (G4)

* `netbsd401-macppc-GENERIC` — 6,907,904 bytes

```
cd _images
gxemul -E macppc -e g4 netbsd401-macppc-GENERIC
```

**Not yet a working rig.** The kernel loads and reports its entry at
`0x00100000 <kernel_text>` on `g3`, `g4`, `g4plus` and `g5`, then produces no further
output. It is kept here because getting PowerPC to a console would close the last
`float_emul.c` calling family that has no execution coverage, and because the load itself
is a non-trivial exercise of the loader.

`g4plus` is worth noting separately: it is a **fork-added** MPC7455 subtype that upstream
0.7.0 does not recognise. It was the single genuine signal produced by the 97-alias
startup matrix before that matrix was retired.

## Coverage this leaves

`float_emul.c` is called by the alpha, m88k, mips, ppc and sh cores plus `dev_pvr`.

| Family | Executes guest code | Checked FP answer in-guest | Reaches #287's arm |
|--------|---------------------|----------------------------|--------------------|
| MIPS (pmax, arc) | yes | **no** — the rigs run `uname`/`id`, no FP | no |
| m88k (luna88k) | yes | yes — `1.5/3.0`, `sqrt(2)` | no |
| SuperH (landisk) | yes — full kernel boot | no — console input is lossy, and no FP tool on the media | no |
| PowerPC (macppc) | loads only | no | no |
| alpha | no | no | no |

**No rig in this harness reaches the arm #287 changed**, and the middle column is stated
per-harness rather than per-project. Two corrections to earlier drafts of this table:

* MIPS was listed as having a checked FP answer. The OpenBSD 2.2 rig scripts run
  `uname -a`, `id`, `hostname`, `ps` and `ifconfig` — no floating point. A separate
  scratchpad script (`regr_p4e_combo.sh`) has exercised `div.d`/`sqrt.d`/`c.lt.d` in-guest
  on pmax, but it is not one of these gates, so it does not belong in this table.
* The m88k row was described as covering #287. It does not: `1.5/3.0` and `sqrt(2)` are
  far inside the region where old and new provably agree (`|x| < 2^128` and
  `|x| >= 2^-126`). Reverting #287 leaves every rig here green.

#287 is covered by **gate 2**, which compiles and links the real `float_emul.c` and
asserts both a closed-form change-set and absolute answers. That is a stronger instrument
than any of these rigs for a pure function — but it is a different claim from "a guest
computed it", and the two should not be conflated.

Closing the in-guest gap would need a staged binary that computes an overflowing
single-precision value (`1e30f * 1e30f`) and prints its bits, on a rig whose media has a
compiler or can carry a cross-built executable. None of the current images qualify: the
OpenBSD 2.2 rig image has no working `cc`, and the landisk ramdisk has no tooling at all.
