Erratum to ADJ_MYTHOS_local.md (the pass-6 ruling) -- repair 7, 2026-11-05, on the REGRESS-stage adjudication
(../adj_reg_20261105/ADJ_MYTHOS_local.md, section 1(e)), as corrected by pass 8.  The ruling file is not rewritten.

Its line 5 ("Zero floor breaches survive adjudication") and line 53 ("0 FLOOR") are NARROWED: both hold for the denominator of its
section 2, the edit shapes of the two exchange bodies (dev_pvr.c:664-668, :737-740), which is what pass 6 enumerated -- not for the
guards.  The guards' constant 0 swapped for the d->reg values the guarded bodies read (fb_base, palette_cfg) are 12 FLOOR cells,
rowed by repair 7 (../r7_20261105/PRETABLE_7.out, table7/; ../r3_20261105/CLOSURE3.errata.md).

(Corrected 2026-11-05, pass 8 -- codex, ../p8_20261105/codex_codex_pvr_p8.txt: this said "(fb_base, palette_cfg, the first PALETTE
register) are 16 FLOOR cells".  The body reads the first PALETTE register only as palette elements indexed by a VRAM byte
(dev_pvr.c:841-844), buffer elements outside the class.)
