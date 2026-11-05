#!/usr/bin/env python3
"""pvr_variants.py -- writes the table-1 test variants of the pvrrenderexit fix (dev_pvr.c.fix) into variants/<name>.c.  Each is ONE
exact-text edit (asserted to match the expected number of times); TAB, NL and the backslash are built with chr() so no shell or heredoc
layer can eat them.  Names and intent are listed in PRETABLE.out, written before table 1 runs."""
import io
import os

TAB, NL, BS = chr(9), chr(10), chr(92)
HERE = os.path.dirname(os.path.abspath(__file__))
FIX = io.open(os.path.join(HERE, "dev_pvr.c.fix"), encoding="latin-1", newline="").read()
GUARD = TAB * 4 + "if (!d->zwrite_disabled)" + TAB + "/*  #NNN: depth test kept, store skipped  */" + NL
STORE = TAB * 5 + "d->vram_z[ofs] = z;" + NL
ZTEST = TAB * 3 + "if (d->vram_z[ofs] <= z) {" + NL
ASSIGN = TAB * 3 + "d->zwrite_disabled = !zwrite;" + NL
RESET = TAB + "d->zwrite_disabled = 0;" + TAB + "/*  #NNN: per render.  A type-4 header in this"
CULL = TAB * 4 + "if (!culled) {" + NL
END = TAB + "pvr_clear_ta_commands(d);" + NL + TAB + NL + TAB + "// TODO: RENDERDONE"
RESETTA = TAB + "REG(PVRREG_DIWCONF) = DIWCONF_MAGIC;" + NL
XR = TAB * 2 + "if (x > 0 && x < d->xsize) {" + NL   # the x-range check above both guarded stores (D2 edges)
ZBIT = TAB * 3 + "zwrite = ! ((list[1] >> 26) & 1);" + NL   # the bit case 4 reads (M31)
LOOP = TAB + "for (size_t index = 0; index < d->n_ta_commands; ++index) {" + NL   # the per-command loop (M33)


def nth(s, old, new, n, count):
    """Replace the n-th (0-based) of exactly `count` occurrences of old."""
    assert s.count(old) == count, (old[:60], s.count(old), count)
    i = -1
    for _ in range(n + 1):
        i = s.index(old, i + 1)
    return s[:i] + new + s[i + len(old):]


def one(s, old, new):
    return nth(s, old, new, 0, 1)


B1 = (TAB * 3 + "if (!zwrite) {" + NL + TAB * 4 + 'fatal("pvr: no zwrite? not implemented yet.' + BS + 'n");' + NL +
      TAB * 4 + "exit(1);" + NL + TAB * 3 + "}" + NL)
V = {
    "B1_exit": one(FIX, ASSIGN, B1 + ASSIGN),                                                  # the removed block, verbatim, back
    "M1_simple_unguarded": nth(FIX, GUARD + STORE, TAB * 4 + "d->vram_z[ofs] = z;" + NL, 0, 2),
    "M2_tex_unguarded": nth(FIX, GUARD + STORE, TAB * 4 + "d->vram_z[ofs] = z;" + NL, 1, 2),
    "M3_simple_inv": nth(FIX, GUARD, GUARD.replace("(!d->", "(d->"), 0, 2),
    "M4_tex_inv": nth(FIX, GUARD, GUARD.replace("(!d->", "(d->"), 1, 2),
    "M5_assign0": one(FIX, ASSIGN, TAB * 3 + "d->zwrite_disabled = 0;" + NL),
    "M6_assign1": one(FIX, ASSIGN, TAB * 3 + "d->zwrite_disabled = 1;" + NL),
    "M7_assign_inv": one(FIX, ASSIGN, TAB * 3 + "d->zwrite_disabled = zwrite;" + NL),
    "M8_sticky": one(FIX, ASSIGN, TAB * 3 + "if (!zwrite) d->zwrite_disabled = 1;" + NL),
    "M9_noreset": one(FIX, RESET, TAB + "/* d->zwrite_disabled = 0; */" + TAB + "/*  #NNN: per render.  A type-4 header in this"),
    "M10_reset_in_resetta": one(one(FIX, RESET, TAB + "/* moved */" + TAB + "/*  #NNN: per render.  A type-4 header in this"),
                                RESETTA, RESETTA + TAB + "d->zwrite_disabled = 0;" + NL),
    "M11_decline": one(FIX, CULL, TAB * 4 + "if (!culled && !d->zwrite_disabled) {" + NL),
    "M12_hoist_simple": nth(FIX, ZTEST + GUARD + STORE, ZTEST.replace("if (d->", "if (!d->zwrite_disabled && d->") +
                                TAB * 4 + "d->vram_z[ofs] = z;" + NL, 0, 2),
    "M13_ztest_bypass_simple": nth(FIX, ZTEST, ZTEST.replace("<= z)", "<= z || d->zwrite_disabled)"), 0, 2),
    "M14_ztest_bypass_tex": nth(FIX, ZTEST, ZTEST.replace("<= z)", "<= z || d->zwrite_disabled)"), 1, 2),
    "M15_simple_never_store": nth(FIX, GUARD, GUARD.replace("(!d->zwrite_disabled)", "(!d->zwrite_disabled && 0)"), 0, 2),
    "M16_tex_never_store": nth(FIX, GUARD, GUARD.replace("(!d->zwrite_disabled)", "(!d->zwrite_disabled && 0)"), 1, 2),
    "M17_reset_at_end": one(one(FIX, RESET, TAB + "/* moved */" + TAB + "/*  #NNN: per render.  A type-4 header in this"),
                            END, TAB + "d->zwrite_disabled = 0;" + NL + END),
    "M18_simple_lo_ge": nth(FIX, XR, XR.replace("x > 0", "x >= 0"), 0, 2),
    "M19_simple_lo_gt1": nth(FIX, XR, XR.replace("x > 0", "x > 1"), 0, 2),
    "M20_simple_hi_le": nth(FIX, XR, XR.replace("x < d->xsize", "x <= d->xsize"), 0, 2),
    "M21_simple_hi_lt1": nth(FIX, XR, XR.replace("x < d->xsize", "x < d->xsize - 1"), 0, 2),
    "M22_tex_lo_ge": nth(FIX, XR, XR.replace("x > 0", "x >= 0"), 1, 2),
    "M23_tex_lo_gt1": nth(FIX, XR, XR.replace("x > 0", "x > 1"), 1, 2),
    "M24_tex_hi_le": nth(FIX, XR, XR.replace("x < d->xsize", "x <= d->xsize"), 1, 2),
    "M25_tex_hi_lt1": nth(FIX, XR, XR.replace("x < d->xsize", "x < d->xsize - 1"), 1, 2),
    # addendum 7 (the design ruling on the 47-row draft: Mythos 5.1 adjudicating, Opus 5.5 confirming)
    "M26_simple_ztest_del": nth(FIX, ZTEST, ZTEST.replace("(d->vram_z[ofs] <= z)", "(1)"), 0, 2),
    "M26b_tex_ztest_del": nth(FIX, ZTEST, ZTEST.replace("(d->vram_z[ofs] <= z)", "(1)"), 1, 2),
    "M27_tex_zon_bypass": nth(FIX, ZTEST, ZTEST.replace("<= z)", "<= z || !d->zwrite_disabled)"), 1, 2),
    "M27b_simple_zon_bypass": nth(FIX, ZTEST, ZTEST.replace("<= z)", "<= z || !d->zwrite_disabled)"), 0, 2),
    "M28_hoist_tex": nth(FIX, ZTEST + GUARD + STORE, ZTEST.replace("if (d->", "if (!d->zwrite_disabled && d->") +
                         TAB * 4 + "d->vram_z[ofs] = z;" + NL, 1, 2),
    "M29_simple_lt": nth(FIX, ZTEST, ZTEST.replace("<= z)", "< z)"), 0, 2),
    "M30_tex_lt": nth(FIX, ZTEST, ZTEST.replace("<= z)", "< z)"), 1, 2),
    "M31_bit25": one(FIX, ZBIT, ZBIT.replace(">> 26)", ">> 25)")),
    "M32_reset1": one(FIX, RESET, RESET.replace("= 0;", "= 1;")),
    "M33_reset_in_loop": one(one(FIX, RESET, TAB + "/* moved */" + TAB + "/*  #NNN: per render.  A type-4 header in this"),
                             LOOP, LOOP + TAB * 2 + "d->zwrite_disabled = 0;" + NL),
}
os.makedirs(os.path.join(HERE, "variants"), exist_ok=True)
for name, text in V.items():
    assert text != FIX, name
    io.open(os.path.join(HERE, "variants", name + ".c"), "w", encoding="latin-1", newline="").write(text)
print("%d variants written" % len(V))
