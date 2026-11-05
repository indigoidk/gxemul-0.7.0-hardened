# pvrrenderexit -- the main loop's CHECKS of the rulings' open source questions (2026-11-04 17:14Z, Opus 5.5; reads, no edit)

Each is a read of GXEMUL-SEC/src/devices/dev_pvr.c at HEAD ebe5af82 (the file is unmodified in the working tree).

1. Fable U2 / Mythos part 15 -- `vertex_index` is INITIALISED at render entry: `int vertex_index = 0;` (:1122), re-zeroed by each polygon header (:1193).  A header-less vertex at the start of a render writes index 0.
2. Mythos part 14 -- the object buffer is PER RENDER: pvr_render ends with `pvr_clear_ta_commands(d);` (:1423, which sets `d->n_ta_commands = 0` at :1065); the only other resets are pvr_reset_ta (:1438) and the buffer-full guard (:1531).  So render 2 of the two-render session reports 7 Tile Accelerator commands (X 3 + header 1 + Y 3), and X is genuinely header-less: the confound (N = 11) does not arise and no TA_LIST_INIT store is needed.
3. Header-less vertices parse with the per-render locals initialised at :1089-1121 (listtype 0, color_type 0, texture 0); with color_type 0 the vertex writes wf_r/wf_g/wf_b from list[6] (:1335-1338) before the untextured rasterizer reads them (:1392-1395).
4. Not a finding, recorded so it is not re-derived: `int wf_r[4], wf_g[4], wf_b[4];` (:1127) has no initialiser; the textured path never writes them (:1329-1333) and passes texture parameters, not them, to pvr_render_triangle_textured (:1385); a new header resets vertex_index, so every untextured triangle's three colours are written before use.  The strip shift at :1407/:1411 copies indeterminate values only within a textured strip, where they are never read.

Consequence: the two-render row (Fable ROW 3 = Mythos 'pvr_zwrite_tworender') is buildable as designed; its remaining prerequisite is the session's time budget (Mythos part 8: ~0.68 s per step-per-store; 93 steps).
