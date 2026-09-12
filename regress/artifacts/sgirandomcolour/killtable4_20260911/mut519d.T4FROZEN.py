#!/usr/bin/env python3
#  #519 kill-table 3 mutator -- RE-KEYED to the CURRENT SEC text (the 04:26 bracket-balance edit
#  broke mut519.py's M1/M12 find-strings, which is the driver's presence-pin working as designed).
#  Usage: mut519c.py <path-to-clone-dev_sgi_re.c> <mutant>    exit 9 = MUTANT-TEXT-NOT-FOUND.
import io, shutil, sys
P, m = sys.argv[1], sys.argv[2]
PRE = ('/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/'
       '8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/dev_sgi_re.pre519.c')
T = '\t'
OK0    = T*3 + "ok = 0;\n"
LATCH  = T*3 + "if (!(d->warned & SGIRE_W_BADCOLOR)) {\n"
SETBIT = T*4 + "d->warned |= SGIRE_W_BADCOLOR;\n"
FATAL3 = (T*4 + "fatal(\"[ put: color mode = 0x%x ] [ sgi_re: unimplemented \"\n"
          + T*4 + "    \"colour type in horrible_getputpixel, x=%i y=%i; store \"\n"
          + T*4 + "    \"declined (once) ]" + chr(92) + "n\", color_mode, x, y);\n")
ARM_NEW = OK0 + LATCH + SETBIT + FATAL3 + T*3 + "}\n"
ARM_OLD = (T*3 + "buf[0] = random();\n"
           + T*3 + "buf[1] = random();\n"
           + T*3 + "buf[2] = random();\n"
           + T*3 + "buf[3] = random();\n"
           + T*3 + "// TODO.\n"
           + T*3 + "fatal(\"[ put: color mode = 0x%x ]" + chr(92) + "n\", color_mode);\n")
GUARD  = T*2 + "if (ok)" + T + "/*  #519: a declined type stores nothing  */\n"
CI_PUT = (T*2 + "case DE_MODE_TYPE_CI:\n" + T*3 + "buf[0] = *color;\n" + T*3 + "break;\n"
          + T*2 + "case DE_MODE_TYPE_RGB:\n" + T*3 + "buf[0] = *color >> 24;\n")
CI_PUT_NEW = (T*2 + "case DE_MODE_TYPE_RGB:\n" + T*3 + "buf[0] = *color >> 24;\n")
RGB_PUT = (T*2 + "case DE_MODE_TYPE_RGB:\n" + T*3 + "buf[0] = *color >> 24;\n"
           + T*3 + "buf[1] = *color >> 16;\n" + T*3 + "buf[2] = *color >> 8;\n"
           + T*3 + "buf[3] = 0;\n" + T*3 + "break;\n")
RGBA_PUT = (T*2 + "case DE_MODE_TYPE_RGBA:\n" + T*3 + "buf[0] = *color >> 24;\n"
            + T*3 + "buf[1] = *color >> 16;\n" + T*3 + "buf[2] = *color >> 8;\n"
            + T*3 + "buf[3] = *color;\n" + T*3 + "break;\n")
ABGR_PUT = (T*2 + "case DE_MODE_TYPE_ABGR:\n" + T*3 + "buf[0] = *color;\n" + T*3 + "buf[1] = *color >> 8;\n"
            + T*3 + "buf[2] = *color >> 16;\n" + T*3 + "buf[3] = *color >> 24;\n" + T*3 + "break;\n")
def cond(expr):
    return (OK0, T*3 + "if (" + expr + ")\n" + T*4 + "ok = 0;\n")
M = {
 #  ---- the mutants table 1 already scored, re-keyed ------------------------------------------
 'M1_reinstate':        (ARM_NEW, ARM_OLD),
 'M2_noguard':          (GUARD, ""),
 'M3_zerofill':         (OK0, T*3 + "buf[0] = buf[1] = buf[2] = buf[3] = 0;\n"),
 'M4_okinlatch':        (OK0 + LATCH + SETBIT, LATCH + T*4 + "ok = 0;\n" + SETBIT),
 'M5_nolatch':          (LATCH, T*3 + "if (1) {\n"),
 'M6_sharedbit':        (LATCH + SETBIT, T*3 + "if (!(d->warned & SGIRE_W_BADMODE)) {\n"
                                             + T*4 + "d->warned |= SGIRE_W_BADMODE;\n"),
 'M7_silent':           (FATAL3, ""),
 'M8_declineall':       (T*2 + "int ok = 1;", T*2 + "int ok = 0;"),
 'M9_dropcase_ci':      (CI_PUT, CI_PUT_NEW),
 'M10_dropcase_abgr':   (ABGR_PUT, ""),
 'M12_prefix_reworded': ("fatal(\"[ put: color mode = 0x%x ] [ sgi_re: unimplemented \"",
                         "fatal(\"[ put: colour mode = 0x%x ] [ sgi_re: unimplemented \""),
 'M16_dropcase_rgb':    (RGB_PUT, ""),
 'M17_dropcase_rgba':   (RGBA_PUT, ""),
 #  ---- the two MEASURED TOTAL ESCAPES this round must now kill ---------------------------------
 'M13_widthdecline':    cond("bufdepth == 4"),
 'M14_lineardecline':   cond("linear"),
 #  ---- the 2-axis JOINT the closure's corner cell exists for ------------------------------------
 'M15_jointwidthlin':   cond("bufdepth == 4 || linear"),
 #  ---- the LABEL axis: one mutant per exempted dispatch label (sgimtedepth4dead, 2026-09-09) ----
 'M20_permit_tlba':     cond("tlb_mode != 0"),
 'M21_permit_tlbb':     cond("tlb_mode != 1"),
 'M22_permit_tlbc':     cond("tlb_mode != 2"),
 'M23_permit_tiled_d4': cond("linear || bufdepth != 4"),
 #  ---- the width axis beyond {1,4}: the disclosed depth debt, MEASURED not asserted ------------
 'M24_permit_d2d8':     cond("bufdepth == 1 || bufdepth == 4"),
 'M25_permit_d8':       cond("bufdepth != 8"),
 'M26_permit_d2':       cond("bufdepth != 2"),
 #  ---- a 3-term joint: the boundary this instrument does NOT claim ------------------------------
 'M27_permit_bc_d2d8':  cond("tlb_mode == 0 || linear || bufdepth == 1 || bufdepth == 4"),
 #  ---- the clause-(e) BOUNDARY: color_mode is the switch SELECTOR and does NOT flow into any
 #  lvalue the guarded body reads, so per the 2026-09-09 dispatch-label ruling it is coverage
 #  debt, not floor.  Two of the twelve reaching nibbles are driven; this exempts those two.
 'M28_permit_othernibbles': cond("color_mode == 0xf0 || color_mode == 0x50"),
 #  ============ #519 PASS-4: the CLASS CLOSURE's own negative controls ============
 #  The SIX mutants MEASURED at 59/59 on the 59-row instrument (pass2_20260911/SCORES_P2.txt),
 #  each writing uninitialised host stack into guest memory.  Each MUST now die, or the
 #  closure has failed on its own motivating case.  (M28_permit_othernibbles above is the
 #  sixth; it keeps its table-3 name so the two tables' scores line up.)
 'M30_tilenrdecline':  cond("tile_nr == 0"),
 'M31_tilenrguard':    (GUARD, T*2 + "if (ok || tile_nr)" + T + "/*  #519: a declined type stores nothing  */\n"),
 'M32_tilenrxdecline': cond("tile_nr_x == 0"),
 'M33_tiledorigin':    cond("linear || y == 0"),
 'M37_fgvalue':        cond("*color == 0xaabbccdd"),
 #  ---- the coordinate mutants the 59-row instrument DID kill (58/59, sole red `ycrcb x4y1'):
 #  they must STILL die, or a row broke.
 'M34_ofsguard':       (GUARD, T*2 + "if (ok || ofs)" + T + "/*  #519: a declined type stores nothing  */\n"),
 'M35_xguard':         (GUARD, T*2 + "if (ok || x)" + T + "/*  #519: a declined type stores nothing  */\n"),
 'M36_yguard':         (GUARD, T*2 + "if (ok || y)" + T + "/*  #519: a declined type stores nothing  */\n"),
 #  ---- the NEW axes the closure claims, as their own discriminators --------------------
 'M39_xofsguard':      cond("xofs == 0"),        # the x=128 hole I nearly shipped
 'M40_tilenrydecline': cond("tile_nr_y == 0"),
 'M41_jointtileY':     cond("tile_nr == 0 || y == 0"),   # the pairwise disjunction
 #  ---- settles whether the three `silent' rows earn their place: an announce added to an
 #  ACCEPTED type should red `silent' and NOT `ann1'.  If it reds neither, they are deletable.
 'M38_acceptannounce': (RGBA_PUT,
                        T*2 + "case DE_MODE_TYPE_RGBA:\n" + T*3 + "buf[0] = *color >> 24;\n"
                        + T*3 + "buf[1] = *color >> 16;\n" + T*3 + "buf[2] = *color >> 8;\n"
                        + T*3 + "buf[3] = *color;\n"
                        + T*3 + "fatal(\"[ sgi_re: unimplemented colour type in horrible_getputpixel, x=%i y=%i; store declined (once) ]\\n\", x, y);\n"
                        + T*3 + "break;\n"),
}
if m == 'M11_null':
    shutil.copy(PRE, P); print('M11_null: pre-fix file copied'); sys.exit(0)
if m not in M:
    print('unknown mutant', m); sys.exit(9)
s = io.open(P, encoding='utf-8', newline='').read()
old, new = M[m]
c = s.count(old)
if c != 1:
    print('MUTANT-TEXT-NOT-FOUND: %s matched %d times' % (m, c)); sys.exit(9)
io.open(P, 'w', encoding='utf-8', newline='').write(s.replace(old, new))
print('applied', m)
