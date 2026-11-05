# pvrrenderexit pass 2 -- checks run by the main loop, 2026-11-05 02:1xZ (each settles a seat's claim by reading or measuring)

1. GLM F1 ("W_LOAD 0x00096872 decodes as mov.l @r8,r7") -- REFUTED.  _scratchpad/sh4_programming.txt:13674 reads
   `MOV.L @Rm,Rn  (Rm) -> Rn  0110nnnnmmmm0010`, so halfword 0x6872 has nnnn = 8 (Rn = r8) and mmmm = 7 (Rm = r7): mov.l @r7,r8, as
   the probe comments.  Measured corroboration: the base leg's `id r8` reads 0x17fd11db, the PVR ID, through that very load
   (legs51/LEGS.log, base 51/51).  W_STORE 0x2782 = mov.l r8,@r7 by :13668 (0010nnnnmmmm0010).
2. GLM custody (is the landed probe the measured instrument?) -- regress/pvr_zwrite_probe.py md5 31a20cd0aad5 is NOT byte-identical to
   det_20261104/probe51_draft_frozen.py (md5 5da28a4dfcf7, the instrument of legs51 and table 1); the two are AST-equal once the
   module docstring is removed (python ast.dump comparison).  The docstring was rewritten after table 1 (make_final_probe.py).  So every
   row, want and session is the measured one; the record should say so.
3. GLM 33 (vram_z writers) -- three, as PRETABLE section 3 says: `grep -n 'vram_z\[' src/devices/dev_pvr.c` gives the two guarded stores
   (688 simpleline, 773 texturedline), their two depth tests (686, 771) and the render-entry clear (1181).
4. Argon's pvr answer was banked by hand (gweb jobs_20261103_adj/pvrrenderexit_p2/BANKED_BY_HAND.txt): the packet carried two
   final-line formats, the author's apparatus defect.
5. The table-1 VERDICT.md said "Run 2026-11-05 19:04-19:06 local"; 19:04 local was 2026-11-04 (01:04Z on 11-05).  Corrected in place
   before the cloud copies went out; grok, GLM and Argon received the earlier wording.
6. Opus custody point -- src/devices/dev_pvr.c is byte-identical to det_20261104/dev_pvr.c.fix (md5 481755b4f10f), the table-1 baseline (cmp, 02:1xZ).  Fable's P3 dependency: DEVINIT(pvr) memsets the struct (dev_pvr.c:2686, memset(d, 0, sizeof(struct pvr_data))).
7. Argon's ADJUDICATION answer (gweb pvrrenderexit_adjp2, 02:42Z local 20:42, after the cloud Fable packet went out) -- its three
   substantive overturns, checked by reading:
   a. P4 "bit 25 enables texture1 and routes the polygon to texturedline" -- REFUTED: texture1 is assigned at dev_pvr.c:1236, printed
      under ta_debug at :1246, and otherwise ignored (":1261 For now, trust texture and ignore texture1."); the draw dispatch keys on word
      0's `texture` (:1342, :1397).  A word-1 bit 25 changes no rasterizer.
   b. P1 "row 480 is outside the frame and has NO pixel channel" -- REFUTED: the probe reads pixels through the linear VRAM window
      (VRAM + ((y*640 + x) & ~1)*2); row 480 col 300 is VRAM offset 615,000, inside the 8 MB VRAM (`#define VRAM_SIZE (8*1048576)`,
      :83), past the 614,400-byte frame the render clears, and zero from zeroed_alloc (:2698).
   c. "missed by all seats": pvr_render_triangle's reject (`if (y3 < 0 || y1 >= d->ysize)`) and its y sweep loops -- OUTSIDE the bound:
      they are in the CALLER, and DEPENDS-ON stops at the enclosing function (simpleline / texturedline); grok said the same in pass 2.
   Its P3 point (the swap depends on shape, not listing order) is a wording correction, not an overturn: for these flat-topped
   triangles the listing order decides which top vertex is v2 and so which side of the long edge it lies.
