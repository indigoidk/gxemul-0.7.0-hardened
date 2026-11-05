# pvrrenderexit -- the rung-3 witness, measured 2026-11-04 01:26 (before any edit)

No fix exists: the design ruling for the Z-write site (ONE exit only; the siblings keep their own disposition) is Fable's and is HELD
(owner 2026-11-04 ~00:4x "hold fable"; ~01:0x "keep going ... on the 5 oldest bugs").  Measured by the main loop (Opus 5.5).

**Instrument.**  `regress/pvr_zwrite_probe.py`, run as the frozen copy `probe_frozen.py` (md5 a2a7496922d2, equal to the source at run
time; `RUN.log` 01:26:08).  Machine: `-E dreamcast`, UNMODIFIED in-tree.  Every device access is a real SH-4 `mov.l` through the decoder
and memory_rw (placed at 0x8c010000 with `put w`; each store is r7 = address, r8 = value, PC = 0x8c010000, one `step`): FB_RENDER_CFG = 1
(0xa05f8048), the eight words of one polygon header to the Tile Accelerator (0xb0000000..0xb000001c; the write at offset 0x1c submits it),
then STARTRENDER (0xa05f8014), which renders synchronously inside that store.

| run | binary | RESULT | CONTROL | SYMPTOM | red rows |
|---|---|---|---|---|---|
| `prefix_head.out` | the scratch clone /tmp/gx579 rebuilt (src/cpus and src/devices) with HEAD `ebe5af82`'s copy of every product file the tree has uncommitted (`cpu_alpha_palcode.c`, `cpu_ppc_instr.c`, `dev_lca.c`, `dev_pcc2.c`, `dev_sh4.c`, `mvme_pcctworeg.h`), each checked `== HEAD`, plus `dev_pvr.c` and `machine_dreamcast.c` (`RUN.log`) | 7/9 | OK | PRESENT | `zoff session`, `zoff prompt` |
| `prefix_build.out` | `build/gxemul` (its `dev_sh4.c` is the tree's UNCOMMITTED copy, not this round's; the PVR, SH-4 core and dreamcast files are HEAD's) | 7/9 | OK | PRESENT | the same two |
| `null.out` | `/bin/true` | 3/9 | FAIL | ABSENT | -- |
| `nobin.out` | a missing path | 0/9 | FAIL | ABSENT | -- |

Controls: a guest `mov.l @r7,r8` from the PVR ID register reads 0x17fd11db (RAM would not); the same render with Z-write ENABLED (list word
1 = 0) runs to the end -- the device prints `[ pvr_render: rendering to FB offset 0x0, 1 Tile Accelerator commands ]` -- and the process
survives with the prompt back.  Witness: with list word 1 = 0x04000000 (bit 26, Z-write DISABLED) the same session prints
`[ pvr: STARTRENDER ]`, `[ pvr_render: rendering to FB offset 0x0, 1 Tile Accelerator commands ]`, `pvr: no zwrite? not implemented yet.`
and exits with status 1 (`prefix_head_sessions/zoff.txt`).  The `zoff rendered` row is green on both builds by design: it proves the render
was reached before the exit.

**Owed when the design is ruled:** what a Z-write-disabled polygon draws (the depth-test channel: vertices plus a pixel read-back -- the
witness-brief answer's seventeen-command design), whether a once-latched announce prints, the three sibling exits (texture pixel format,
a non-RGB565 render mode, an unimplemented list command -- each its own row), more than one command per render, the gate wiring and the
kill table.
