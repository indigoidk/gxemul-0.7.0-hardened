Erratum to ADJ_MYTHOS_local.md (the register ruling, REPAIR-7) -- 2026-11-05, pass 8 (../p8_20261105/codex_codex_pvr_p8.txt: 0
floor breaches, one false-record family).  The ruling file is not rewritten.

THE PREMISE.  Line 21 says texturedline's body has, beside fb_base and palette_cfg, "the body's direct read of
`d->reg[PVRREG_PALETTE/4]` at :842".  FALSE: dev_pvr.c:842 is `char* base = (char*)&d->reg[PVRREG_PALETTE / sizeof(uint32_t)];`,
which forms an address and reads no value, and the palette loads at :843-844 are indexed by `index8bpp`, a VRAM byte read at :841 --
computed-index buffer elements, which this ruling's own section 1(c) excludes from the source set.

THE COUNTS IT CARRIED, each narrowed:
* line 3, "The constant-0 guard operands swapped for `fb_base`, `palette_cfg` and `d->reg[PVRREG_PALETTE/4]` are 16 FLOOR cells, 5 of
  them measured green ..., 11 green by derivation": 12 FLOOR cells, swapped for fb_base and palette_cfg; all 12 MEASURED green on the
  148 rows (five in ../r7_20261105/meas7/, seven in meas7b/).
* line 25, "Cells: simpleline 4 sites x 1 source = 4; texturedline 4 sites x 3 sources = 12; 16 FLOOR cells": texturedline 4 x 2 =
  8; 12 FLOOR cells.
* line 30, "Closes the 8 palette_cfg and PALETTE cells (4 rows)": closes the 4 palette_cfg cells; with PALETTE[0] 0x10000 the same
  four rows also red the four PALETTE swaps (PL1t-PL4t), measured checks outside the class, and the rows stay.
* line 33, "extended with the three register sources": two.
* line 39, "MYTHOSADJREGPVR: 16 FLOOR 1 DEBT": 12 FLOOR 1 DEBT.
The sixteen rows, the DEBT and section 1's reading (i) are unchanged.
