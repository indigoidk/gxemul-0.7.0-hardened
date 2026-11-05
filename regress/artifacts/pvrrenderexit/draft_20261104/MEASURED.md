# pvrrenderexit -- the PIXEL CHANNEL and the fix DRAFT, measured 2026-11-04 02:2x by the main loop (Opus 5.5)

Measured after the Opus measuring seat for this question (`_scratchpad/opus_20261104/m_pvr/answer.md`) stopped on a safety-classifier
refusal having only read source; its one READ fact -- the linear VRAM read window at P2 0xa5000000, a plain `memcpy` from `d->vram` --
is what this channel uses.  NO RULING: the design is Fable's and is HELD.  The draft is the pass-1 fix draft
(`_scratchpad/cloud_fable_20261103/pvrrenderexit/11_packet_fixdraft.md`), applied to a SCRATCH CLONE only (`/tmp/gxmain_pvr`, a `cp -a` of
`build/` whose `dev_pvr.c` was checked CLEAN against SEC; removed afterwards); `draft.diff` is that edit.

**The channel** (`main_pixels.py`): one cold `-E dreamcast` session, every access a real SH-4 `mov.l`; one Tile Accelerator list with a
NEAR red triangle T1 (z = 2.0; the renderer keeps the larger z, `if (d->vram_z[ofs] <= z)`) and then a FAR green triangle T2 (z = 1.0)
overlapping it; STARTRENDER; four pixels read back through 0xa5000000 + (y*640 + x)*2 (RGB565).

| binary | T1 Z-write | exit | overlap (220,180) | T2 only (320,180) | T1 only (120,120) | background | file |
|---|---|---|---|---|---|---|---|
| build/gxemul (dev_pvr.c == HEAD) | on | 0 | 0xf800 RED | 0x07e0 GREEN | 0xf800 RED | 0x0000 | `pix_head_on.out` |
| build/gxemul | OFF | **1** (`pvr: no zwrite? not implemented yet.`) | -- | -- | -- | -- | `pix_head_off.out` |
| the draft | on | 0 | 0xf800 RED | 0x07e0 GREEN | 0xf800 RED | 0x0000 | `pix_draft_on.out` |
| the draft | OFF | 0 | **0x07e0 GREEN** | 0x07e0 GREEN | 0xf800 RED | 0x0000 | `pix_draft_off.out` |

**What it shows.**  (1) The depth test is observable by a guest: with Z-write on, the farther triangle drawn second does NOT overwrite the
nearer one (overlap RED).  (2) The draft leaves the Z-write-on render pixel-identical to HEAD.  (3) With Z-write disabled on T1 the draft
keeps the process alive, still DRAWS T1 (its own pixel RED -- not declined), and stores no depth for it, so T2 draws over T1 in the
overlap (GREEN) -- the meaning of Z-write disable (depth-tested and drawn, no depth store).  (4) The witness probe on the draft:
`probe_draft.out` 9/9, CONTROL=OK, SYMPTOM=ABSENT (the same script was 7/9 SYMPTOM=PRESENT on HEAD, `witness_20261104/`).

**The rows this channel offers a detector** (for the ruling to adopt or not): the overlap pixel separates IMPLEMENT (GREEN) from DECLINE
(T1 skipped: overlap GREEN too, but T1-only black) and from a draft whose depth store is not guarded (overlap RED); the T1-only pixel
separates IMPLEMENT/accept from DECLINE.  Not measured: a textured polygon (the second rasterizer's guarded store), more than one render,
a Z-write-disabled polygon followed by vertices with no new header.

**What "the draft" means here.**  `apply_draft.py` writes the draft's INTENT as its AFTER image shows it (the two fields, the guarded depth store in BOTH rasterizers, `d->zwrite_disabled = !zwrite;` and the once-latched announce in place of the exit), not the packet's literal hunks: an Opus reading seat (`_scratchpad/cloud_fable_20261103/pvrrenderexit/26_answer_bugreview_fixdraft_opus_b.txt`) found the literal diff malformed -- its third hunk deletes `double z = z1, u = u1, v = v1;` in `texturedline`, so it would not compile -- and the AFTER image is the design.  The same seat found the flag survives from one STARTRENDER to the next (a per-render reset is owed); this channel renders once per session and does not observe that.
