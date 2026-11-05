PRETABLE_7 erratum -- 2026-11-05, pass 8 (../p8_20261105/codex_codex_pvr_p8.txt).  PRETABLE_7.out is not rewritten: its mtime is
the order proof.

ITS SOURCE INVENTORY.  It says texturedline's body reads "d->reg through THREE spellings: fb_base (:735, read :775); palette_cfg =
d->reg[PVRREG_PALETTE_CFG / 4] & PVR_PALETTE_CFG_MODE_MASK (:760, read :845); d->reg[PVRREG_PALETTE / 4], read directly as the
palette base (:842)", and gives "PALETTE[0] -- none, a palette entry (data): SAMPLED at 0 and 0x10000".  FALSE for the third: :842
forms the palette's address and reads no value, and the loads at :843-844 are indexed by a VRAM byte (:841), computed-index buffer
elements outside the source set (the register ruling's section 1(c)).  TWO spellings, fb_base and palette_cfg.  So its "16 cells"
are 12 FLOOR cells and four PALETTE checks outside the class (PL1t-PL4t); every prediction stands as written.

ITS SCORE (table7/CHECK.txt): 208 hits -- 207 full and 1 partial (Nt_inner_or, on 160 of the 164 rows) -- 0 misses, and 4 variants
wholly unpredicted.
