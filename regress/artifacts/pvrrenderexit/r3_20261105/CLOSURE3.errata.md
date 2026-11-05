CLOSURE3 erratum -- repair 7, 2026-11-05, on the REGRESS-stage adjudication (../adj_reg_20261105/ADJ_MYTHOS_local.md, reading (i)),
as corrected by pass 8 (../p8_20261105/codex_codex_pvr_p8.txt).  CLOSURE3.md is not rewritten.

CLOSURE3.md:29-30 reads: "the int fields the rasterizer body reads are d->xsize, d->ysize, d->zwrite_disabled and
d->bytes_per_pixel (2)".  FALSE BY OMISSION: the guarded bodies also read d->reg -- simpleline through fb_base =
REG(PVRREG_FB_RENDER_ADDR1) (dev_pvr.c:662, read at :715); texturedline through fb_base (:735, read at :775) and palette_cfg =
d->reg[PVRREG_PALETTE_CFG / 4] & PVR_PALETTE_CFG_MODE_MASK (:760, read at :845).  So A4 (:149-161) left out two swap sources for the
constant 0 of `y < 0`, `x1 < 0`, `x2 < 0` and `x > 0`: 12 FLOOR cells (simpleline 4 x 1, texturedline 4 x 2).  Every session of
the 148-row probe leaves those registers at their reset 0, equal to the constant, and all 12 swaps survived it, as did four swaps to
the first PALETTE register built beside them (MEASURED: five in ../r7_20261105/meas7/, eleven in ../r7_20261105/meas7b/).  Repair 7
rows them: fbhi, fbedge, fbtedge and palcfg, each with its Z-off twin, 16 rows (../r7_20261105/PRETABLE_7.out, table7/); the palcfg
rows also red the four PALETTE swaps, checks outside the class.

(Corrected 2026-11-05, pass 8 -- codex: this erratum listed "and d->reg[PVRREG_PALETTE / 4] (:842)" among the body's reads and
counted "three swap sources ... 16 FLOOR cells (simpleline 4 x 1, texturedline 4 x 3)".  :842 is `char* base =
(char*)&d->reg[PVRREG_PALETTE / sizeof(uint32_t)];`, an address, and the palette loads at :843-844 are indexed by a VRAM byte read
at :841 -- computed-index buffer elements, which the ruling's section 1(c) excludes.)
