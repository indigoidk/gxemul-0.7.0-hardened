# `#564` sgirekills (MTE half) -- PASS 1 DESIGN BRIEF: five terminating calls in `dev_sgi_re.c`'s `do_mte_transfer()`

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  Where I state something as fact, ask whether it is true.  A seat that re-derives a
premise from something this brief did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/` AT HEAD `2951694f`.**  There are THREE pristine-2021-upstream copies of
GXemul under the project root (`./src/` and two under `_archive/audit-results-*/builds/`).  They are NOT this fork.  If
your line numbers disagree with mine by hundreds you are reading one of them -- say so rather than reconciling.  The
working tree carries another session's uncommitted edits to OTHER files (`dev_lca.c`, `dev_pcc2.c`, `dev_sh4.c`,
`cpu_alpha_palcode.c`); `dev_sgi_re.c` is clean (md5 `60203f67`, identical to HEAD).

**If you cannot read files that is expected** -- every fact you need is inlined below.  Name any premise you cannot
settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim -- a field width, a count of reachable values -- ENUMERATE it rather than
reasoning about it.**  And enumerate the right DOMAIN: ask what the producer of a value can actually emit.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## 1. The round

**Row `sgirekills` (HIGH, open).**  Its first half shipped as `#513` (the RE register read-back arms -- accept / decline,
2026-09-08).  That round's design deliberately EXCLUDED the transfer engine, and what remains of the row is exactly
this: **five guest-reachable terminating calls in `do_mte_transfer()`**, each `fatal(...); exit(1);`.  A sixth
`exit(1)` in the same file sits in `DEVICE_ACCESS(sgi_mte)`'s width chain under `if (len == 4) ... else if (len != 4)
... else { ... }` -- exact complements, so it is unreachable; it is out of scope here and already filed (`sgimtewidth`).

| site | guarding condition (verbatim) | where |
|---|---|---|
| S1 | `if (mode & MTE_MODE_STIPPLE)` | before the destination switch -- any destination |
| S2 | `if (src > MTE_TLB_C)` | before the destination switch -- any destination, fill or copy |
| S3 | `if (mode & MTE_MODE_COPY)` | inside `case MTE_TLB_LIN_A: case MTE_TLB_LIN_B:` only (tiled COPY is implemented) |
| S4 | `if (depth != 8)` | inside the linear cases only |
| S5 | `if (bytemask != 0xffffffff)` | inside the linear cases only, after S3 and S4 |

The census of `exit(` in `dev_sgi_re.c` at HEAD -- comments and string literals stripped, then a whole-word search --
finds six statements, at the five sites above plus the unreachable width arm.  **Check that census against section 3
rather than accepting it.**

## 2. The witness -- MEASURED on the committed build, BEFORE any edit (test-first)

A rung-3 cold-debugger probe on the UNMODIFIED `-E sgi -e ip32` machine: every MTE register is programmed by a REAL
GUEST STORE (`sw`) through real address decode and `memory_rw`, and the transfer is fired the way the device defines
it -- a write whose ADDRESS carries `CRIME_DE_START` (0x800), here `DST1 | START` written last.  One session per site,
because the process ends.  Each site row then performs a RAM store and load AFTER the transfer: `survived` means the
session lived and the later load returned its value.  **The site rows expect the post-fix behaviour, so they are RED
on HEAD.**  The binary is a scratch build of HEAD `2951694f` (`git archive`, configure, make, in WSL
`/tmp/gxsk_2951694f`; `[ gxemul -nt src/devices/dev_sgi_re.c ]` true, its `dev_sgi_re.c` md5 `60203f67` = HEAD's).

Instrument (frozen, for the file-reading seats): `regress/artifacts/sgirekills/witness_20261017/sgi_mte_exit_witness.py`
(md5 `dcbb328d`).  The values each site row writes (MODE field layout from `crmfbreg.h`, section 4):

| row | MODE written | BYTEMASK written | expected HEAD site |
|---|---|---|---|
| `stipple` | `0x600` = depth field 2 (32 bpp), STIPPLE 0x400, dst A, src A | not written | S1 |
| `src tex` | `0x260` = depth 32, src field 3 (`MTE_TLB_TEX`) | not written | S2 |
| `lin copy` | `0x810` = dst field 4 (`LIN_A`), COPY 0x800, depth 8 | `0xffffffff` | S3 |
| `lin depth` | `0x110` = dst LIN_A, depth field 1 (16 bpp) | `0xffffffff` | S4 |
| `bytemask` | `0x010` = dst LIN_A, depth 8 | `0x0000ffff` | S5 |
| `lin fill` (control) | `0x010` | `0xffffffff` | none -- every guarded value legal |

BG is `0x11223344`, DST0 = 0, DST1 = 0 (written with START).

**The run, verbatim** (`regress/artifacts/sgirekills/witness_20261017/witness_HEAD_2951694f.out`):

```
