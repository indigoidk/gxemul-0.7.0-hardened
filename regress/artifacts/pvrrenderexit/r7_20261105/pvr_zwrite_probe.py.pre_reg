#!/usr/bin/env python3
"""pvrrenderexit -- DETECTOR (built on its rung-3 witness) for the Dreamcast PVR renderer's Z-write-disable exit, dev_pvr.c.

DEFECT (filed 2026-10-02).  src/devices/dev_pvr.c, pvr_render(): a STARTRENDER write renders the Tile Accelerator commands the
guest submitted; for a polygon header whose list word 1 has bit 26 set (Z-write DISABLED, `zwrite = !((list[1] >> 26) & 1)`)
the renderer printed "pvr: no zwrite? not implemented yet." and called exit(1) -- the emulator process ended.

THE FIX (#NNN).  Such a polygon goes through the same depth test and rasterization as any other polygon, and only its depth store
is skipped: both rasterizers (simpleline, texturedline) check d->zwrite_disabled at their vram_z stores, case 4 assigns it from
the header's bit, and every pvr_render clears it first, so a list with no header does not inherit the previous render's value.

WHAT THE ROWS MEASURE (`-E dreamcast`, an UNMODIFIED in-tree machine; one cold debugger session per case).  Every device access is a
REAL guest instruction through the SH-4 decoder and memory_rw: `mov.l r8,@r7` and `mov.l @r7,r8` placed at 0x8c010000.  A render
session writes FB_RENDER_CFG = 1 (RGB565), polygon headers and vertices to the TA (the store at offset 0x1c submits a command), then
STARTRENDER, which renders synchronously inside that store; pixels are read back through the linear VRAM window, one 32-bit guest
load per pixel.  T1 is drawn first at z = 2.0 and T2 second at z = 1.0 over it; the renderer keeps the larger z (vram_z <= z).
  CONTROLS (14): the PVR ID register reads 0x17fd11db through a guest load (RAM would not); a Z-write-enabled render runs to the
end and survives to the prompt; a bogus machine runs nothing; the Z-off render was reached (`zoff rendered`); and the pixels no
enumerated variant moves -- ovon's T2-only, T1-only and background pixels, and the T2-only pixels of texon, equal, texequal and
mask.  (Corrected 2026-11-05, repair 3: this said "CONTROLS (13)" and stopped at texequal; repair 2 added `mask t2 only` as a
control and did not count it.)
  zoff (R1): one Z-off header survives to the prompt.  ovoff (R2): a Z-off T1, then T2 -- T1 stored no depth, so T2 draws over
it.  ovon (R3): both Z-on -- T1's depth hides T2.  behind (R6): a Z-off T2 behind a Z-on T1 still fails the depth test.  texoff
(R4), texbeh and texon (R7): the same cells through texturedline, from red and green texels.  two (R5): a Z-off render, then a
second render of bare vertices -- no header, so Z-write is on (the per-render reset).  sticky (R8): a Z-off header, then a Z-on one
in the same render.  edges and texedges (R9): triangles across the left and right screen edges pin the x-range bound above both
stores at its edges.  equal and texequal (R10): two Z-on polygons at the SAME z -- the later one wins under `<=`.  Repair 2:
yedges and texyedges (the y range at rows 0, 479 and 480; the x1 > x2 swap; the span end at an exact integer), mask and mask25
(word 1 bits 27 and 25 must not disable the depth store).  Repair 3 (the CONTRACT below): swap and texswap (the column before an
exact span start; a reversed span exactly one wide; equal span ends whose attributes differ; simpleline's fractional span end),
ramp and texramp (a reversed span whose two ends differ in depth and in colour or texture coordinates, read at its left end under
a later polygon at an in-between depth), edges2 and texedges2 (reversed spans across the left and right screen edges, and the left
clause's two compares at their edge), zeq and texzeq (a Z-off polygon at the SAME z as a stored depth: it passes `<=` and draws),
maskoff (bits 26 and 27: `& 1`, not `== 1`) and maskhi (bits 28-31 without bit 26: no wider mask); and the Z-OFF TWINS -- zedges,
zyedges, zswap, zedges2, zleft, zramp and their textured zt* / texzleft twins -- every single-layer geometry session above drawn by a
Z-off polygon, and the swap-body session with a Z-off span tested against a stored depth.  Repair 4 (the D2-F paragraph in the
CONTRACT): swap and zswap gain `s start` (a span start at x.5); half and zhalf put each simpleline position compare at the HALF
pixel (a span reversed by 0.5; x1, then x2, at 639.5); ramp8, zramp8, texramp8 and ztramp8 read the swap body at a reversed span's
FAR end, eight columns from its swapped start.  Repair 5: ramp8hi and zramp8hi read both ends of RAMP8 from ABOVE, under a cover at
z 4.0; negx, znegx, texnegx and ztnegx read a span whose start is NEGATIVE.

STDIN CAP (measured 2026-11-05, r3_20261105/stdin_cap_test{,2}.out).  A session loses every byte of its debugger input past byte
4100: in a render session the first `step 1` comes at byte 100, the debugger's console FIFO (CONSOLE_FIFO_LEN 4096, refilled 100
bytes at a time while 101 are free) has then read 4100 bytes, and that step runs the maple keyboard's tick for the first time
(machine.c starts every tick at ticks_till_next 0), which reads whatever stdin is left into its own console handle as key presses.
(Corrected 2026-11-05, repair 4 -- codex pass 4, F4: this said the first step comes at byte 100 in every session.  id and neg
write no r8= line, so theirs ends at byte 93, and their whole input is about 100 bytes.)  A session past the cap
loses its `quit` and waits out the 90 s timeout.  texyedges sent 4104 bytes from repair 2 until repair 3: its `quit` arrived as
`q`, every run of the 68-row probe took about 90 s (table 2: ~90.5 s on every gxemul leg but Y2t's, whose texyedges session
crashed first; table 1's 51-row probe: 0.4 s), and its six pixel reads all came before the cut, so its rows measured what they say.  It now stores only the red texel it samples.  The
"16-command" mask session that base68's first run lost was this cap too (6088 bytes), not a slow session.  session() refuses an
input longer than STDIN_CAP before running anything.

CLAUSE (e) -- catches (test-variant table 2, artifacts/pvrrenderexit/r2_20261105/table2/SCORES.txt and VERDICT.md; PRETABLE_2.out
was written before the driver ran -- every table-2 result is newer, only the frozen probe, copied first, is older; 62 variants on
the then 68-row probe, 58 of them with a prediction: 55 red on their predicted rows, 3 green as predicted EQUIVALENT (M17, L1s,
L1t), and 4 red that were NOT PREDICTED (Y2s, Y2t, Y4s, Y4t: undefined behaviour).  Corrected 2026-11-05, repair 3 (codex pass 3,
records a and c): this said "PRETABLE_2.out written before it; 62 variants on this 68-row probe: 59 red, every one on its predicted
rows".  Table 1's 36 on the then 51-row probe are det_20261104/table1/): the removed exit reinstated verbatim (B1); either
rasterizer's store left unguarded, its guard inverted, or its store never made (M1-M4, M15, M16); case 4's assignment forced to 0
or to 1, inverted, or made set-only (M5-M8); the per-render reset deleted, moved into pvr_reset_ta(), set to 1, or moved into the
command loop (M9, M10, M32, M33); Z-off polygons declined, or the guard folded into the depth test (M11, M12, M28); the depth test
bypassed for Z-off or for Z-on polygons, or deleted (M13, M14, M26, M26b, M27, M27b); its equal edge tightened (M29, M30); either
x-range bound moved by one (M18-M25); the wrong header bit (M31); the y range of either rasterizer's early return tightened (Y1:
`t in`; Y3: `b in`); its x clauses' `&&` made `||` (O1: `l in`; O2: `r in`, `rspan`); the right clause tightened to xsize - 1 or
the span start moved to x1 + 1 (R1, X1: `rspan`); the span end tightened or widened (E1: `s end`; E2: `s past`); the swap deleted
(S1: `swap`, `s end`); the bit-26 decode widened to bits 26-27 or to bits 25-26 (K1: `mask overlap`; K2: `mask25 overlap`) -- each
per rasterizer where it has two.
  REPAIR 3 CONTRACT (the class closure: artifacts/pvrrenderexit/r3_20261105/CLOSURE3.md).  Designed to catch, per rasterizer, every
cell of the predicates that dominate the guarded depth store, and the decode's single-edit forms.  Every cell marked [r3] is new in
repair 3: its single-site variants were MEASURED SURVIVORS of the 68-row probe (r3_20261105/PVR3_NOTE.md: codex's A-I, both Gemini
readings' swap body, the closure's W1-W4); the Z-off twins' multi-token representatives (V1s-V7t: a bound moved by 2 *
d->zwrite_disabled) are DERIVED survivors, since before the twins no row drew Z-off geometry but zleft's one triangle.  Every kill
is owed to test-variant table 3 (r3_20261105/PRETABLE_3.out, table3_pvr.sh), which RAN on 2026-11-05, 04:10:23-04:19:18 local
(r3_20261105/table3/TABLE.log): 129 of its 130 predictions hit, and the one miss, Vt_swap_nov, reddened ztramp's row as well as
texramp's, where only texramp's was predicted (r3_20261105/PRETABLE_3.errata.md).  (Corrected 2026-11-05, repair 4 -- codex pass 4,
F2: this said "prepared, NOT YET RUN".)  REPAIR 4 (pass 4, rule D2-F, ruled in artifacts/pvrrenderexit/adj_p4_20261105/
ADJ_MYTHOS_local.md) adds the twelve rows marked [r4]: their single-site variants, codex pass 4's B1, B2, B4-B10, B13 and B14, were
MEASURED SURVIVORS of the 128-row probe (r4_20261105/meas_B/SCORES.txt), and every kill is owed to test-variant table 4
(r4_20261105/PRETABLE_4.out, table4/), which RAN on 2026-11-05, 05:27:20-05:36:16 local, on the 140-row probe: all 148 of its
predictions hit -- its six legs, 130 variants red, each on exactly its predicted rows, and 12 green as predicted (EQUIVALENT or
clause-(e) DEBT, each named) -- and the four undefined-behaviour variants were not predicted (table4/CHECK.txt, VERDICT.md).
REPAIR 5 (pass 5, ruled in artifacts/pvrrenderexit/adj_p5_20261105/ADJ_MYTHOS_local.md) adds the eight rows marked [r5]: six owed,
and two optional (`ramp8hi l end`, `zramp8hi l end`) kept because they measured red on two compound substitutions, `z1 += z2` and
`z1 *= z2` (r5_20261105/meas_cand/SCORES.txt).  The single-site variants of its three FLOOR cells -- simpleline's `tmpf = z1;`
deleted, N1s (`int x = x1 + 0.25`) and B2t (texturedline's `int x = x1 + 0.5`) -- were MEASURED SURVIVORS of the 140-row probe
(r5_20261105/meas140/SCORES.txt), and every kill is owed to test-variant table 5 (r5_20261105/PRETABLE_5.out, table5/), which
RAN on 2026-11-05, 06:29:53-06:40:24 local, on this probe's 148 rows: all 192 of its predictions hit -- its six legs, 156 variants
red, each on exactly its predicted rows, and 30 green as predicted (EQUIVALENT or clause-(e) DEBT, each named) -- the four
undefined-behaviour variants were not predicted, and the thirteen non-finite compound forms were excluded and named
(table5/CHECK.txt, VERDICT.md).
COVERED -- each cell below for a Z-ON polygon by the row named, and for a Z-OFF polygon by that row's Z-off twin (z..., zt...; `x2
tip`'s twin is `zleft tip`), the cross-product of every predicate dominating the guarded store with Z-write [r3]:
  the y range: rows 0 and 479 drawn, row 480 not (t in, b in, b out);
  the left x clause by its truth cells (x1 < 0, x2 < 0): (yes, no) `l in`, (no, yes) `edges2 l rev` [r3], (no, no) every inner row;
its x1 and x2 compares at their edge, which is an INTEGER move by TWO (one only changes column 0): a reversed span 1.0..-1.0
(`edges2 l tip`) and a forward span -1.0..1.0 (`edges2 x2 tip`) each drawing column 1 [r3]; at the half pixel the same two rows
red `x1 < 1.5` and `x2 < 1.5`, and `< 0.5` is EQUIVALENT (column 0 is never drawn) -- all four measured as predicted,
r4_20261105/meas_L/ [r4] (corrected 2026-11-05, repair 4 -- codex pass 4, F1: this said "a move by TWO", true of integer moves
only);
  the right x clause: (no, yes) `r in`, `rspan`; (yes, no) `edges2 r rev` [r3]; its x1 compare's edge (`rspan`, a span starting at
639.0) and its x2 compare's edge (`edges2 r rev`, a reversed span ending at 639.0) [r3]; each compare at the half pixel, an end at
639.5 (`half r x1`, `half r x2`) [r4];
  the operand swaps from the fields the body reads (d->xsize, d->ysize, d->zwrite_disabled, d->bytes_per_pixel) into every bound:
all land on the rows above -- `y < d->zwrite_disabled` and `x > d->zwrite_disabled`, which drop row 0 or column 1 for Z-off polygons
only, on the Z-off twins (`zyedges t in`, `zedges l in`) [r3];
  the x1 > x2 swap: reversed by more than one (`yedges swap`), by exactly one (`swap s tip`) [r3], by half a pixel (`half swap`)
[r4], equal ends whose attributes differ (`swap vert`) [r3]; its body's exchanges of z, r, g and b (`ramp l end`; Z-off: `zramp l
end`) [r3] and of z, u and v (`texramp l end`; Z-off: `ztramp l end`) [r3], each at the reversed span's right end too (`ramp8 r
end`, `texramp8 r end`; Z-off: `zramp8 r end`, `ztramp8 r end`) [r4], and simpleline's at both ends from above, under a cover at z
4.0 (`ramp8hi r end`, `ramp8hi l end`; Z-off: `zramp8hi r end`, `zramp8hi l end`) [r5];
  the span start: the column before an exact start (`swap s before`) [r3], a start at x.5 (`swap s start`) [r4], a NEGATIVE start
(`negx n start`, `texnegx n start`; Z-off: `znegx n start`, `ztnegx n start`) [r5], and the start column (`rspan`);
  the span end: an exact end and the column past it (`s end`, `s past`); simpleline's fractional end, the column past floor(x2)
(`swap frac past`) [r3];
  the inner x bounds: columns 0, 1, 639 and 640 (`l out`, `l in`, `r in`, `r out`), and its `&&` made `||` (`l out`, `r out`);
  the depth test crossed with Z-write: stored depth below, equal to and above the incoming one, each with Z-write on and off --
ovon t1 only / texbeh t1 only, ovoff t1 only / texoff t1 only, equal / texequal, zeq / texzeq [r3], ovon / texon overlap, behind /
texbeh overlap; its bound moved by +1 (`ovon overlap`: T1 and T2 differ by exactly 1.0) or by -1 (`equal overlap`);
  the decode: bit 26 clear and set (ovon, ovoff); `== 1` for `& 1` (`maskoff overlap`, bits 26 and 27) [r3]; the mask widened to
bit 27 (`mask overlap`) or to any of bits 28-31 (`maskhi overlap`) [r3]; a shift move to bit 25 with the mask widened (`mask25
overlap`); any other shift move or operand change (ovoff overlap).
  THE SWAP BODY'S STATEMENT DELETIONS [r5] (pass-5 ruling, section 1): the two exchange bodies hold 27 statements, simpleline's
five exchanges at dev_pvr.c:664-668 and texturedline's four at :737-740.  Three are declarations whose temporary the line uses
again, so deleting one alone does not compile -- `double tmpf = x1;` (:664), `int tmp = x1;` (:737), `double tmpf = z1;` (:738),
each refused by the compiler (r5_20261105/syntax_check_5.out) -- and are named, not cells.  The other 24 are deletion cells, each
held by the row named and by its Z-off twin (measured: r4_20261105/table4/, r5_20261105/meas140/, meas_cand/): the `tmp = a1`
halves -- simpleline `tmpf = z1;` `ramp8hi r end` [r5]; `tmpf = r1;`, `tmpf = g1;`, `tmpf = b1;` `ramp8 r end`; texturedline `tmpf =
u1;`, `tmpf = v1;` `texramp8 r end`; the `a1 = a2` halves -- simpleline z, r, g, b `ramp l end`; texturedline z, u, v `texramp l
end`; the `a2 = tmp` halves -- simpleline z, r, g, b `ramp8 r end`; texturedline z, u, v `texramp8 r end` [r4]; the x halves --
simpleline `x1 = x2;` `yedges swap`, `x2 = tmpf;` `yedges swap` and `yedges s end`; texturedline `x1 = x2;` `texyedges swap`, `x2 =
tmp;` `texyedges swap` and `texyedges s end`.
  NOT COVERED, by name: rows above the frame, y <= -1 (`y < -1`, Y2; the early return's first `||` made `&&`), and rows below it,
y >= 480 (`y > ysize`, Y4; `y >= d->xsize`; the first or second `||` made `&&`): undefined behaviour, the depth read lands outside
vram_z; the left clause's compares moved by one, its
compares moved down, and both clauses' all-off-screen cells (EQUIVALENT: column 0 and columns 640 and up are never drawn); the right
clause loosened (EQUIVALENT, the same reason); the third `||` made `&&` (EQUIVALENT: no span is off both edges); equal span ends
with equal attributes (EQUIVALENT: an exchange of equal values); texturedline's `x < x2 + 1` (EQUIVALENT: its span ends are
integers); simpleline's fractional span end at floor(x2) (every narrowing that drops it also drops `s end`); the per-span
interpolation (dz12, dr12, du12, ... and the per-pixel steps: data flow into the stored and drawn values, not a predicate); the mask
widened past bit 31 (EQUIVALENT: the shifted word is below 64); widening to bits 0-24 (a shift move and a mask change, two edits).
(Corrected 2026-11-05, repair 4: this list disclosed "a fractional move of the swap bound in simpleline (`x1 > x2 + 0.5`: no probed
span is reversed by less than one)", which the pass-4 ruling withdrew -- that edit is a floor breach, rowed now by `half swap` --
and said the ramp rows read "only a span's first pixel", which the ramp8 rows no longer leave true.)
  FRACTIONAL MOVES (rule D2-F, pass 4, as the pass-5 ruling corrected it): every simpleline position compare and the span start
are pinned at the pixel and at the half pixel (swap: `half swap`; start: `swap s start`; end: `swap frac past`; right clause: `half
r x1`, `half r x2`; Z-off twins likewise). The span START is a truncation toward zero, not a compare. At the -1.0 start the
`negx` rows draw (NEGX, the negx sessions), `int x = x1 + c` begins at 0 for every c in (2^-54, 1]: the sum rounds to -1 + 2^-53,
the next double toward zero, or nearer zero, and truncates to 0, one column late with every attribute one step behind, a
whole-pixel move that one row pins (texturedline likewise: `texnegx n start`). At c = 2^-54 the tie rounds to the even -1.0 and
below it the sum is -1.0 again, so the start family is EXHAUSTED over the sign cells the early return tests only down to the
start's own double resolution. Below it: c = 2^-54 is the family's one surviving member in simpleline, SAMPLED and disclosed: it
changes the start only at x1 = 1 - 2^-53, the double below 1.0, which the tie rounds up (codex pass 6, B; its witness is
[(0,50),(3,50),(3,80)], green, red, green at z 2.0: row 60 arrives x1 = ten additions of 0.1 = 1 - 2^-53, x2 = 3, so the fix starts
at 0 and draws (85,170,0) = 0x5540 at (1,60) while the variant starts at 1 and draws vertex 1's green 0x07e0, both Z-states; DERIVED,
not measured); every c < 2^-54 is EQUIVALENT (DERIVED: the sum truncates to the same integer as x1). In
texturedline every c <= 2^-54 is EQUIVALENT (an int start plus 2^-54 rounds back to the int, or at 0 truncates to it). In
texturedline every fractional move of a position COMPARE is EQUIVALENT for every integer
end, negative included (both operands are ints: `x1 > x2 + c` is `x1 > x2`, `x1 >= xsize - c` is `x1 >= xsize`, `x <= x2 + c` is
`x <= x2`); its start truncation is the one non-equivalent fractional move there (B2t: measured green on 140 rows, a floor breach,
rowed by `texnegx n start`). Below half a pixel the simpleline COMPARES (`x1 > x2 + c`, `x <= x2 + c`, `x1 >= xsize - c`, 0 < c <
0.5) remain SAMPLED: a row at fraction f reds every move >= f and none below. The depth test's constant offsets: `<= z - c` is held
by the equal rows for every c > 0; `<= z + c` is SAMPLED at 1.0 (both Z-states) and 0.5 (Z-on, the ramp rows) and claimed nowhere
finer, the body having no unit for z. The swap body is pinned at BOTH ends of a reversed span (`l end`: the `a1 = a2` half; `r
end`: the `a2 = tmp` half); the interpolation between them remains data flow, not a predicate.  (Corrected 2026-11-05, repair 5 --
codex pass 5's R1 and the pass-5 ruling's R3: this said "Below half a pixel (`x1 > x2 + c`, `int x = x1 + c`, `x <= x2 + c`, `x1 >=
xsize - c`, 0 < c < 0.5) the moves are SAMPLED, not claimed: ... so the family has no least member and no finite row set pins it.
In texturedline every such move is EQUIVALENT (integer ends; built and measured green)" -- false for the START, which truncates
toward zero: B2t is not EQUIVALENT at a negative start, and one row pins every `int x = x1 + c`, 0 < c <= 1 [repair 6: for
2^-54 < c <= 1 only].)  (Corrected 2026-11-05, repair 6 -- codex pass 6 and the pass-6 ruling's R3, ../artifacts/pvrrenderexit/
adj_p6_20261105/ADJ_MYTHOS_local.md section 3: the start sentence said "for a negative integer start every `int x = x1 + c`, 0 < c
<= 1, begins at x1 + 1 and carries every attribute one step behind, a whole-pixel move that one row pins, so the start family is not
SAMPLED but EXHAUSTED over the sign cells the early return itself tests" -- false below the start's double resolution, where -1 +
2^-54 rounds back to -1.0.)
  EDIT SHAPES ON THE TWO EXCHANGE BODIES (pass-6 ruling, section 2 -- each count and derivation is there; DERIVED unless marked
MEASURED), NOT COVERED except (a): the 27 statements at dev_pvr.c:664-668 and :737-740 (24 assignments, 3 declarations); the guard
`if (x1 > x2)` is P4, closed in CLOSURE3.  X, Y, W, B = d->xsize 640, d->ysize 480, d->zwrite_disabled 0 or 1, d->bytes_per_pixel 2.
 (a) deletion: FLOOR, closed -- 24 cells, each red on its named row and twin (MEASURED, table 5); the 3 declarations do not compile.
 (b) compound operator: DEBT -- 108 forms (96 `+=` `-=` `*=` `/=`; 12 int-only on texturedline's two x statements, `%=` `&=` `|=`
`^=` and `<<=` `>>=`): of the 80 codex pass 5 screened, 26 survived the 140 rows (MEASURED), 13 non-finite (excluded, named in
PRETABLE_5), 41 caught; the 16 x forms and the 8 `%=` `&=` `|=` `^=` caught; the 4 shifts undefined.  Simpleline's 7 depth survivors
now red on the ramp8hi rows, and 19 survive the 148 rows (both MEASURED, table 5): texturedline `z1 += z2`, `z1 *= z2`, `z2 +=
tmpf`, `z2 *= tmpf`; simpleline `tmpf += r1`, `tmpf *= r1`, `r2 += tmpf`, `tmpf *= g1`, `g1 += g2`, `g2 *= tmpf`, `tmpf += b1`,
`b1 *= b2`, `b2 += tmpf`; texturedline `u1 *= u2`, `u2 += tmpf`, `u2 -= tmpf`, `tmpf *= v1`, `v1 += v2`, `v2 *= tmpf`.  Remedy: the
sets below.
 (c) right-hand side to a body-read field: DEBT (ruling section 1) -- 108 cells (each statement x X, Y, W, B): 79 caught, 21 survive
-- simpleline `tmpf = z1`, `z1 = z2`, `z2 = tmpf` -> B; texturedline `double tmpf = z1`, `z1 = z2`, `z2 = tmpf` -> X, Y, B;
`tmpf = r1`, `r2 = tmpf` -> X, Y; `tmpf = g1`, `g2 = tmpf` -> W; `b1 = b2` -> W, B; `u1 = u2` -> Y (codex pass 6, A) -- and 8
UNDETERMINED, FP-sensitive on SWAP's recurrence: `u1 = u2` -> X, B; `tmpf = v1`, `v2 = tmpf` -> X, Y, B.  Remedy: the sets below.
 (d) right-hand side to another local or parameter: DEBT, an open family (about 400 forms), not enumerated -- a self or partner
operand equals a deletion, held by (a); `b1 = z2` and `b1 = z1` survive.  Remedy: the sets below.
 (e) right-hand side to a constant: DEBT, infinite -- survives in bands: z2 in (1.5, 4.0), r2 in [251.5, 256), 0 <= g2 < 2, 0 <=
b1 < 8.  Remedy: the depth and RGB sets.
 (f) sign (right-hand side negated): DEBT -- 27 forms, 19 caught, 8 survive: `b1 = -b2`, `tmpf = -g1`, `g2 = -tmpf`, `u1 = -u2`,
`tmpf = -v1`, `v2 = -tmpf`, `tmpf = -u1`, `u2 = -tmpf`.  Remedy: the RGB set and the amended UV set.
 (g) one statement moved: no cell owed; texturedline `x2 = tmp` moved after its z exchange is EQUIVALENT.
 (h) left-hand side changed: held by (a) -- the original target is left unassigned.
 (i) type change, duplication, insertion, guard: `int tmpf` at :664 SURVIVES (remedy: RAMP8 depths (1.75, 1, 1.75) under COVER8,
both Z-states); `int tmpf` at :738 caught by `texramp8 r end`; `float tmpf` (:664, :738) and `double tmp` (:737) EQUIVALENT on the
probe's values; adjacent duplication of an assignment is EQUIVALENT; duplicating a declaration does not compile; insertion an open
family, disclosed; guard edits P4, closed.
 (j) other right-hand-side expression changes, casts included -- an open family, DEBT, not enumerated.
 REMEDY SETS, filed, not owed (both Z-states; the depth sets in both rasterizers): DEPTH -- RAMP8 depths (3, 2, 3) under a cover at
4.0, and RAMP8 depths (1, 1, 1) under COVERHI at 1.5, each read at both ends; RGB -- RAMP8 colours (63,96,128) / (32,48,80), 0x3b10
at 448 and 0x218a at 440; UV -- uvs (0.375, 0.25) / (0.25, 0.375) with only texels (3,2) and (2,3) stored, read at both ends.
PROBE-DESIGN NOTE: the probe's standard depth 2.0 equals d->bytes_per_pixel, so every constant write of B is invisible at depth 2.0.
 (Replaces, 2026-11-05, repair 6: repair 5's COMPOUND ASSIGNMENTS paragraph, which counted 80 compound forms ("screened 80 by
derivation on the 140 rows: 41 caught, 13 undefined ..., 26 survive"), named no other edit shape, and gave the UV set as "uvs
(0.5,0.25) / (0.25,0.375)", which leaves `tmpf = -u1` green; in (e) the ruling's bands "any r2 in [248, 256)" and "any g2 ... below
the quantum" are narrowed, `half swap` doubling the slope at column 101 (r2 248 reads 241 there, g2 2 reads 4) -- full text:
r6_20261105/pvr_zwrite_probe.py.pre_r6; corrections: r6_20261105/RECORDS6_NOTE.md.)
  discloses, not claimed: M17 (the reset moved to the end of pvr_render) is EQUIVALENT -- the one early exit after the reset's
old position, the frame-outside-VRAM `return` (dev_pvr.c:1166; the RGB565 check's exit at :1090 precedes the reset, the list-command
exit at :1432 ends the process), comes before every header of its render, the field's only non-zero writer is the header case in
the render loop, and the field is zero there, from DEVINIT or the previous render's end -- so no row can see it (corrected
2026-11-05, repair 4 -- codex pass 4, F8, with the ruling's correction: this said the render loop has no early exit after the
reset's old position); the three sibling exits (an unimplemented texture pixel format, in texturedline(); a non-RGB565 render mode and an unimplemented
list command, in pvr_render()) keep their own disposition (the list-command exit is witnessed at
artifacts/pvrrenderexit/sibling_listcmd_20261104/) -- corrected 2026-11-05 (codex pass 3, record d): this said "the three sibling
exits in the same function"; the equal-depth rows rely on z staying exactly 2.0 across a flat triangle (every slope is 0.0 in
pvr_render_triangle and in both rasterizers; measured green on the fix); fog, translucency and the other list types; L1 (the left
x clause tightened to 1) is EQUIVALENT, measured green -- no probed span has both ends in [0, 1), and `x > 0` never draws column 0;
Y2 (`y < -1`) and Y4 (`y > ysize`) are NOT PREDICTED and not claimed -- they admit row -1, whose colour store lands before the
frame (FB_RENDER_ADDR1 is 0 here, so before VRAM itself) and whose depth read lands before vram_z, and row 480, whose depth read
lands past the frame-exact vram_z (malloc of xsize*ysize doubles): undefined behaviour (on table 2's build Y2 reddened the whole
y-edges session and Y4 only `b out`).  The `mask25` row went BEYOND the pass-2 rulings: their premise that the textured sessions
already catch K2 was false -- no probe header sets word 1 bit 25 (texturing comes from word 0 bit 3; texture1 is decoded and
ignored).  The two mask headers run in two sessions because one session sending both (6088 bytes) passed the STDIN CAP above
(r2_20261105/base68/SPLIT_NOTE.md) -- corrected 2026-11-05: this said such a session "outran the 90 s session limit".  On the
68-row probe the pre-fix build scored 42 of the 68 rows with the symptom PRESENT, and three null media -- /bin/true 9/68, an absent
binary 0/68, /bin/false 1/68 -- each CONTROL=FAIL (r2_20261105/table2/SCORES.txt).  The 128-row probe (repair 3): the fix 128/128
in ~3 s with no session timed out, the pre-fix build 60/128 with the symptom PRESENT (r3_20261105/base128/, head128/: table 2's 26
red rows plus every repair-3 row whose session carries a Z-off header, 42), and its null media 9/128, 0/128 and 1/128
(r3_20261105/table3/SCORES.txt).  The 140-row probe (repair 4): the fix 140/140 in ~2 s with no session timed out (48 sessions),
and the pre-fix build 66/140 with the symptom PRESENT (r4_20261105/base140/, head140/: the 128-row probe's 68 red rows plus the six
repair-4 rows whose session carries a Z-off header -- `zswap s start`, zhalf's three, `zramp8 r end`, `ztramp8 r end`), and its
null media 9/140, 0/140 and 1/140 (r4_20261105/table4/SCORES.txt).  This 148-row probe (repair 5): the fix 148/148 in ~2 s with
no session timed out (54 sessions), and the pre-fix build 70/148 with the symptom PRESENT (r5_20261105/base148/, head148/: the
140-row probe's 74 red rows plus the four repair-5 rows whose session carries a Z-off header -- `zramp8hi r end`, `zramp8hi l end`,
`znegx n start`, `ztnegx n start`); its null media are predicted in r5_20261105/PRETABLE_5.out.

Sentinel: PVR_ZWRITE_PROBE_DONE (plus PVR_ZWRITE_RESULT=n/N, _CONTROL=OK|FAIL, _SYMPTOM=PRESENT|ABSENT, _RED=none|<names>).
Session transcripts go to the optional [workdir].
"""

import os
import re
import struct
import subprocess
import sys
import tempfile
import time

if len(sys.argv) < 2:
    sys.stderr.write("usage: pvr_zwrite_probe.py <gxemul> [label] [workdir]\n")
    sys.exit(2)

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
WORK = sys.argv[3] if len(sys.argv) > 3 else None
if WORK:
    os.makedirs(WORK, exist_ok=True)
_TMPDIR = tempfile.mkdtemp(prefix="pvr_zwrite_")
DUMMY = os.path.join(_TMPDIR, "dummy.bin")
open(DUMMY, "wb").write(bytes(4))

CODE = 0x8c010000            # P1 RAM
W_STORE = 0x00092782          # mov.l r8,@r7 ; nop  (little-endian halfwords)
W_LOAD = 0x00096872           # mov.l @r7,r8 ; nop
PVR_ID = 0xa05f8000           # PVRREG_REGSTART + PVRREG_ID (P2)
FB_RENDER_CFG = 0xa05f8048
STARTRENDER = 0xa05f8014
TA = 0xb0000000               # the Tile Accelerator window (P2 of 0x10000000)
POLY0 = 0x80000000            # list word 0: cmd 4 (polygon), list type 0, untextured
ZW_OFF = 0x04000000           # list word 1, bit 26: Z-write DISABLED
FATAL = "no zwrite?"
RENDERED = ", 1 Tile Accelerator commands"   # anchored: ", 11 Tile ..." must not match
VRAM = 0xa5000000             # the linear VRAM window (P2 of 0x05000000): a plain memcpy to and from d->vram
FOG2 = 0x00800000             # list word 2 bits 23-22 = 2, the one fog type the renderer does not warn about
VTX, VTX_EOS = 0xE0000000, 0xF0000000      # list word 0 of a vertex: cmd 7; bit 28 = end of strip
RED, GREEN, BLUE, BLACK = 0xf800, 0x07e0, 0x001f, 0x0000   # RGB565 pixels of packed colours 0xff0000, 0x00ff00, 0x0000ff, background
MAGENTA = 0xff00ff            # a packed colour unlike GREEN in all three channels (the ramp rows)
TEX_RED, TEX_GREEN = 0x200000, 0x200008    # texture addresses; u = v = 0 samples texel (0,0), which the renderer's
TEXEL_LINEAR = {TEX_RED: 0x100000, TEX_GREEN: 0x100004}   # 64-bit-area mapping reads at these linear VRAM offsets
#  The textures are 8 x 8 RGB565, not twiddled, 2 bytes a texel: texel (tx, ty) of TEX_RED is texture address 0x200000 + 2 * (tx +
#  8 * ty), read at linear ((a & 4) << 20) | (a & 3) | ((a & 0x7ffff8) >> 1) (texturedline).  So u = 0.5 (tx 4) is 0x200008 =
#  TEX_GREEN's texel (green), and v = 0.125 (ty 1) is 0x200010, linear 0x100008 (TEXEL01, stored blue by the texramp session).
#  Texel (4, 1) (0x200018, linear 0x10000c) is never stored: VRAM is zeroed_alloc'd, so it reads 0x0000.
TEXEL01 = 0x100008
T1 = [(100.0, 100.0), (300.0, 100.0), (200.0, 300.0)]      # drawn first, z = 2.0 (the renderer keeps the larger z: vram_z <= z)
T2 = [(150.0, 150.0), (350.0, 150.0), (250.0, 350.0)]      # drawn second, z = 1.0, overlapping T1
AWAY = [(500.0, 400.0), (620.0, 400.0), (560.0, 470.0)]    # clear of every probed pixel
LEFT = [(-60.0, 200.0), (60.0, 200.0), (0.0, 260.0)]       # spans the left edge: its row 230 runs from x = -30 to 30
RIGHT = [(580.0, 300.0), (700.0, 300.0), (640.0, 360.0)]   # spans the right edge: its row 330 runs from x = 610 to 670
RSPAN = [(639.0, 400.0), (700.0, 400.0), (639.0, 460.0)]   # vertical left edge at x = 639.0: row 430 spans 639.0..669.5
TOP = [(250.0, -30.0), (350.0, -30.0), (300.0, 30.0)]      # reaches row 0 (row 0 spans 275..325)
BOTTOM = [(300.0, 450.0), (350.0, 510.0), (250.0, 510.0)]  # reaches row 479 and, past the frame, row 480
SWAP = [(450.0, 150.0), (350.0, 150.0), (400.0, 250.0)]    # right-then-left: every span arrives x1 > x2; row 180 is 435.0..365.0
#  Repair 3.  Each sweep is pvr_render_triangle{,_textured}: vertices sorted by y (a tie keeps the listed order), then for a flat top
#  the start edge is vertex 1 -> 3 and the stop edge vertex 2 -> 3, the first row carrying both vertices' values exactly; the last
#  row (y3) is never drawn; texturedline receives the two ends truncated to int.
VERT = [(300.0, 100.0), (300.0, 150.0), (300.0, 200.0)]    # all at x = 300: every row arrives x1 == x2 == 300.0; at row 150 the
#                                                            start end carries vertex 1's values (1 -> 3 is constant) and the stop
#                                                            end vertex 2's, so their attributes differ there
FRAC = [(100.0, 100.0), (201.0, 100.0), (100.0, 102.0)]    # row 101 spans 100.0..150.5 (dx23 = -50.5): its last column is 150
LREV = [(60.0, 200.0), (-60.0, 200.0), (0.0, 260.0)]       # LEFT reversed: row 230 arrives 30.0 then -30.0 (dx = -1.0 and +1.0)
RREV = [(700.0, 400.0), (639.0, 400.0), (639.0, 460.0)]    # RSPAN reversed: row 400, its first, arrives 700.0 then 639.0 exactly
RAMP = [(520.0, 60.0), (440.0, 60.0), (480.0, 100.0)]      # flat top right then left: row 60 arrives 520.0 (vertex 1) then 440.0
#                                                            (vertex 2), so the swap moves vertex 2's z and colour to column 440
COVER = [(430.0, 50.0), (450.0, 50.0), (440.0, 70.0)]      # z 1.5, drawn after RAMP: its row 60 spans 435..445, over (440,60)
#                                                            (zramp draws it BEFORE a Z-off RAMP, as the depth RAMP is tested against)
LEFT3 = [(-60.0, 100.0), (60.0, 100.0), (0.0, 160.0)]      # LEFT moved to rows 100-159: row 159, its last, spans -1.0..1.0 (dx =
#                                                            +-1.0, exact); no negative column on row 0
MASK27, MASK25 = 0x08000000, 0x02000000   # list word 1 bit 27 (culling mode 1: culls nothing) and bit 25 (texture1: ignored)
ZOFF27 = 0x0c000000           # word 1 bits 26 and 27: Z-write disabled, culling mode 1 (culls nothing); (word >> 26) is 3
MASKHI = 0xf0000000           # word 1 bits 28-31, bit 26 clear: culling mode 2 (T1's cross product is +40000, not culled) and depth
#                               mode 7 (decoded, used only by ta_debug output); (word >> 26) is 60
#  Repair 4 (pass 4, rule D2-F): the half-pixel edges of simpleline's position compares, and the swap body's far end.  Every end
#  below is exact in binary (integer vertices, slopes of 0.25, 0.5, 1 and 30).
HALF = [(102.0, 100.0), (100.0, 100.0), (101.0, 104.0)]     # row 103 arrives 101.25 then 100.75 (dx = -0.25, +0.25): reversed by
#                                                            HALF a pixel; swapped, it draws columns 100 and 101
HALFR1 = [(639.0, 400.0), (700.0, 400.0), (640.0, 402.0)]   # row 401 arrives 639.5 then 670.0: x1 is half a pixel below xsize
HALFR2 = [(700.0, 410.0), (639.0, 410.0), (640.0, 412.0)]   # the same with the top vertices exchanged: row 411 arrives 670.0 then
#                                                            639.5, so x2 is the end half a pixel below xsize (and on other rows)
RAMP8 = [(448.0, 60.0), (440.0, 60.0), (444.0, 64.0)]       # flat top right then left: row 60 arrives 448.0 (vertex 1) then 440.0
#                                                            (vertex 2) and is swapped; column 448, the span's RIGHT end after the
#                                                            swap, is eight exact steps from 440 and carries vertex 1's values
COVER8 = [(438.0, 50.0), (458.0, 50.0), (448.0, 70.0)]      # z 1.5: its row 60 spans 443..453, over (448,60)
TEX_01 = 0x200010             # a texture whose texel (0,0) is TEX_RED's texel (0,1): linear 0x100008 (TEXEL01, stored blue)
#  Repair 5 (pass 5): the swap body's right end read from above, and a NEGATIVE span start.
COVERHI = [(430.0, 50.0), (470.0, 50.0), (450.0, 70.0)]    # z 4.0: its row 60 spans 440..460 (dx13 = +1, dx23 = -1), over 440 and 448
NEGX = [(-1.0, 60.0), (1.0, 60.0), (0.0, 62.0)]            # flat top: row 60 arrives -1.0 then 1.0, forward; columns -1 and 0 are
#                                                            clipped but still advance the attributes, so column 1 is the third step
PIX = {"overlap": (220, 180), "t2 only": (320, 180), "t1 only": (120, 120), "bg": (10, 10),
       "l in": (1, 230), "l out": (0, 230), "r in": (639, 330), "r out": (0, 331)}   # r out: where x = 640 of row 330 would land
PIX.update({"t in": (300, 0), "b in": (300, 479), "b out": (300, 480), "swap": (400, 180), "s end": (435, 180),
            "s past": (436, 180), "rspan": (639, 430)})
PIX.update({"s before": (364, 180), "s tip": (400, 249), "vert": (300, 150), "frac past": (151, 101), "l rev": (1, 230),
            "r rev": (639, 400), "l end": (440, 60), "l tip": (1, 259), "tip": (1, 159)})
PIX.update({"s start": (399, 249), "half": (101, 103), "half r1": (639, 401), "half r2": (639, 411), "r end": (448, 60)})
PIX.update({"n start": (1, 60)})
#  STDIN CAP (docstring): the first `step 1` of every RENDER session ends at byte 100 of its input (the two `put w` lines, then the
#  first store's r7=, r8=, pc= and step lines), and by then the console FIFO has read 4000 + 100 bytes; the maple tick that step runs
#  swallows the rest.  4096 keeps a margin under the derived 4100.  (Corrected 2026-11-05, repair 4 -- codex pass 4, F4: this said
#  "every session"; id and neg write no r8= line, so their first step ends at byte 93, in inputs of about 100 bytes.)
STDIN_CAP = 4096

rows = []
controls = []
symptom_hits = 0


def row(name, got, want, note="", control=False):
    assert name not in [n for n, _ in rows], "DUPLICATE ROW NAME %r" % name
    assert len(name) <= 16, name
    ok = (got == want)
    rows.append((name, ok))
    if control:
        controls.append((name, ok))
    print("%-18s %-20s %-20s %-46s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    return ok


def store(addr, val):
    return ["r7=0x%x" % addr, "r8=0x%x" % val, "pc=0x%x" % CODE, "step 1"]


def session(name, body, machine="dreamcast", timeout=90):
    """One cold run: the two words placed, then `body`, then `reg`.  Returns (regs, text, how)."""
    global symptom_hits
    cmds = ["put w 0x%x, 0x%08x" % (CODE, W_STORE), "put w 0x%x, 0x%08x" % (CODE + 4, W_LOAD)] + list(body) + ["reg", "quit"]
    argv = [BIN, "-V", "-x", "-E", machine, "0x%x:%s" % (CODE, DUMMY)]
    inp = ("\n".join(cmds) + "\n").encode("latin-1")
    #  STDIN CAP: input past the cap is swallowed by the maple keyboard's first tick (docstring); refuse it before running anything
    assert len(inp) <= STDIN_CAP, "SESSION %r SENDS %d BYTES, PAST STDIN_CAP %d" % (name, len(inp), STDIN_CAP)
    try:
        p = subprocess.run(argv, input=inp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        t = p.stdout.decode("latin-1", "replace").replace("\r", "")
        rc = p.returncode
        how = ("sig%d" % -rc) if rc < 0 else ("exit%d" % rc)
    except subprocess.TimeoutExpired as e:
        t = (e.output or b"").decode("latin-1", "replace").replace("\r", "")
        how = "TIMEOUT"
    except OSError as e:            # an ABSENT binary is a null medium: every row fails, the sentinel still prints
        t = ""
        how = "NOBIN(%s)" % e.__class__.__name__
    if WORK:
        open(os.path.join(WORK, name.replace(" ", "_") + ".txt"), "w", encoding="latin-1").write(
            "$ " + " ".join(argv) + "\n--- stdin ---\n" + "\n".join(cmds) + "\n--- transcript (%s) ---\n" % how + t)
    if how != "exit0" and FATAL in t:
        symptom_hits += 1
    regs = {}
    i = t.rfind("GXemul> reg")
    if i >= 0:
        m = re.search(r"\br8\s*=\s*(0x[0-9a-fA-F]+)", t[i:])
        if m:
            regs["r8"] = int(m.group(1), 16)
    return regs, t, how


def prompt(t):
    i = t.rfind("GXemul> reg")
    return "yes" if (i >= 0 and "cpu0:" in t[i:]) else "no"


def render(word1):
    body = store(FB_RENDER_CFG, 1)
    for k, w in enumerate([POLY0, word1, 0, 0, 0, 0, 0, 0]):
        body += store(TA + 4 * k, w)
    return body + store(STARTRENDER, 0)


def f32(v):
    return struct.unpack(">I", struct.pack(">f", v))[0]


def ta(words):
    """One 8-word TA command; the store at offset 0x1c submits it."""
    out = []
    for k, w in enumerate(words):
        out += store(TA + 4 * k, w)
    return out


def header(zoff, tex=None):
    """A polygon header, list type 0: packed colour, or textured (word 0 bit 3) with word 3 = RGB565 (pixel format 1),
    not twiddled (bit 26), texture address tex >> 3; 8 x 8 texels.  zoff sets word 1 bit 26 (Z-write disabled)."""
    w0 = POLY0 | (8 if tex is not None else 0)
    w3 = (0x0c000000 | (tex >> 3)) if tex is not None else 0
    return ta([w0, ZW_OFF if zoff else 0, FOG2, w3, 0, 0, 0, 0])


def tri(pts, z, rgb=0):
    """Three vertices, end of strip on the last; rgb is the packed colour (word 6), u = v = 0 for a textured header."""
    out = []
    for i, (x, y) in enumerate(pts):
        out += ta([VTX_EOS if i == 2 else VTX, f32(x), f32(y), f32(z), 0, 0, rgb, 0])
    return out


def tri_pv(pts, zs, rgbs=(0, 0, 0), uvs=((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))):
    """tri() with PER-VERTEX depth, packed colour (word 6) and texture coordinates (words 4 and 5, read for a textured header)."""
    out = []
    for i, (x, y) in enumerate(pts):
        out += ta([VTX_EOS if i == 2 else VTX, f32(x), f32(y), f32(zs[i]), f32(uvs[i][0]), f32(uvs[i][1]), rgbs[i], 0])
    return out


def texels():
    return store(VRAM + TEXEL_LINEAR[TEX_RED], RED) + store(VRAM + TEXEL_LINEAR[TEX_GREEN], GREEN)


def texel(lin, val):
    return store(VRAM + lin, val)


def psession(name, body, pixels):
    """A render session that reads `pixels` back through the linear VRAM window, one 32-bit guest load each, in order.  Returns
    ({pixel: value or None}, text, how).  Only register-dump lines count: the debugger also echoes each r8=... command."""
    for p in pixels:
        x, y = PIX[p]
        body = body + ["r7=0x%x" % (VRAM + ((y * 640 + x) & ~1) * 2), "pc=0x%x" % (CODE + 4), "step 1", "reg"]
    _, t, how = session(name, body)
    vals = [int(m.group(1), 16) for m in re.finditer(r"^cpu0: .*?\br8 +=\s*(0x[0-9a-fA-F]+)", t, re.M)]
    #  a 32-bit load at an even pixel: little-endian, so an odd pixel is the high half
    half = lambda v, x: ((v >> 16) if x & 1 else v) & 0xffff
    return {p: (half(vals[i], PIX[p][0]) if i < len(vals) else None) for i, p in enumerate(pixels)}, t, how


def px(v):
    return "none" if v is None else "0x%04x" % v


print("pvrrenderexit RUNG-3 WITNESS -- binary=%s label=%s" % (BIN, LABEL))
print("machine: -E dreamcast (UNMODIFIED in-tree); guest mov.l stores at 0x%x" % CODE)
print("%-18s %-20s %-20s %-46s %s" % ("row", "got", "want", "note", ""))
t0 = time.time()

nr, _, nhow = session("neg", ["r7=0x%x" % PVR_ID, "pc=0x%x" % (CODE + 4), "step 1"], machine="nosuchmachine", timeout=30)
row("neg apparatus", "%s/%s" % (nhow, hex(nr["r8"]) if "r8" in nr else "none"), "exit1/none", "a bogus machine runs no guest", control=True)
r, T, how = session("id", ["r7=0x%x" % PVR_ID, "pc=0x%x" % (CODE + 4), "step 1"])
row("id session", how, "exit0", "mov.l @r7,r8 from the PVR ID register", control=True)
row("id r8", hex(r["r8"]) if "r8" in r else "none", hex(0x17fd11db), "the device answers (RAM would not)", control=True)
r, T, how = session("zon", render(0))
row("zon session", how, "exit0", "Z-write ENABLED render: survives", control=True)
row("zon rendered", "yes" if RENDERED in T else "no", "yes", "the renderer saw the one TA command", control=True)
row("zon prompt", prompt(T), "yes", "the debugger ran `reg` afterwards", control=True)
r, T, how = session("zoff", render(ZW_OFF))
row("zoff rendered", "yes" if RENDERED in T else "no", "yes", "the render was reached (both builds)", control=True)
row("zoff session", how, "exit0", "Z-write DISABLED render: survives")
row("zoff prompt", prompt(T), "yes", "the debugger ran `reg` afterwards")

# ---- THE DEPTH-TEST CHANNEL (cloud Fable 5.1's ruling, rows R2-R5; R6-R8 from PRETABLE.out's joint cells; R9 and R10 from its addenda 6 and 7).  One cold
# ---- session each: FB_RENDER_CFG = 1, the polygon headers and vertices as real guest stores, STARTRENDER, then pixels read back.
CFG = store(FB_RENDER_CFG, 1)
GO = store(STARTRENDER, 0)
P, T, how = psession("ovoff", CFG + header(True) + tri(T1, 2.0, 0xff0000) + header(False) + tri(T2, 1.0, 0x00ff00) + GO,
                     ["overlap", "t2 only", "t1 only", "bg"])
row("ovoff session", how, "exit0", "R2: T1 Z-off red, T2 green behind it")
row("ovoff overlap", px(P["overlap"]), px(GREEN), "T1 stored no depth, so T2 draws over it")
row("ovoff t2 only", px(P["t2 only"]), px(GREEN), "T2 drawn")
row("ovoff t1 only", px(P["t1 only"]), px(RED), "T1 drawn (not declined)")
row("ovoff bg", px(P["bg"]), px(BLACK), "the frame was cleared")
P, T, how = psession("ovon", CFG + header(False) + tri(T1, 2.0, 0xff0000) + header(False) + tri(T2, 1.0, 0x00ff00) + GO,
                     ["overlap", "t2 only", "t1 only", "bg"])
row("ovon overlap", px(P["overlap"]), px(RED), "R3: both Z-on: T1's depth hides T2")
row("ovon t2 only", px(P["t2 only"]), px(GREEN), "T2 drawn", control=True)
row("ovon t1 only", px(P["t1 only"]), px(RED), "T1 drawn", control=True)
row("ovon bg", px(P["bg"]), px(BLACK), "the frame was cleared", control=True)
P, T, how = psession("behind", CFG + header(False) + tri(T1, 2.0, 0xff0000) + header(True) + tri(T2, 1.0, 0x00ff00) + GO,
                     ["overlap", "t2 only", "t1 only"])
row("behind session", how, "exit0", "R6: T1 Z-on red, T2 Z-off green behind")
row("behind overlap", px(P["overlap"]), px(RED), "a Z-off T2 still fails the depth test")
row("behind t2 only", px(P["t2 only"]), px(GREEN), "T2 drawn where it passes")
row("behind t1 only", px(P["t1 only"]), px(RED), "T1 drawn")
P, T, how = psession("texoff", CFG + texels() + header(True, TEX_RED) + tri(T1, 2.0) + header(False) + tri(T2, 1.0, 0x00ff00) + GO,
                     ["overlap", "t1 only", "t2 only"])
row("texoff session", how, "exit0", "R4: T1 textured Z-off (red texel)")
row("texoff overlap", px(P["overlap"]), px(GREEN), "texturedline stored no depth for T1")
row("texoff t1 only", px(P["t1 only"]), px(RED), "T1 drawn from its texel")
row("texoff t2 only", px(P["t2 only"]), px(GREEN), "T2 drawn")
P, T, how = psession("texbeh", CFG + texels() + header(False, TEX_RED) + tri(T1, 2.0) + header(True, TEX_GREEN) + tri(T2, 1.0) + GO,
                     ["overlap", "t2 only", "t1 only"])
row("texbeh session", how, "exit0", "R7: textured T1 Z-on, textured T2 Z-off")
row("texbeh overlap", px(P["overlap"]), px(RED), "textured Z-off T2 fails the depth test")
row("texbeh t2 only", px(P["t2 only"]), px(GREEN), "T2 drawn from its texel")
row("texbeh t1 only", px(P["t1 only"]), px(RED), "T1 drawn from its texel")
P, T, how = psession("texon", CFG + texels() + header(False, TEX_RED) + tri(T1, 2.0) + header(False, TEX_GREEN) + tri(T2, 1.0) + GO,
                     ["overlap", "t2 only"])
row("texon overlap", px(P["overlap"]), px(RED), "R7: both textured Z-on: T1 hides T2")
row("texon t2 only", px(P["t2 only"]), px(GREEN), "T2 drawn from its texel", control=True)
P, T, how = psession("two", CFG + header(True) + tri(AWAY, 2.0, 0xff0000) + GO + tri(T1, 2.0, 0xff0000) + tri(T2, 1.0, 0x00ff00) + GO,
                     ["overlap", "t1 only", "t2 only"])
row("two session", how, "exit0", "R5: a Z-off render, then bare vertices")
row("two overlap", px(P["overlap"]), px(RED), "render 2 has no header: Z-write is on")
row("two t1 only", px(P["t1 only"]), px(RED), "headerless vertices draw")
row("two t2 only", px(P["t2 only"]), px(GREEN), "T2 drawn")
P, T, how = psession("sticky", CFG + header(True) + header(False) + tri(T1, 2.0, 0x00ff00) + tri(T2, 1.0, 0x0000ff) + GO,
                     ["overlap", "t2 only"])
row("sticky session", how, "exit0", "R8: a Z-off header, then a Z-on one")
row("sticky overlap", px(P["overlap"]), px(GREEN), "the Z-on header re-enabled the store")
row("sticky t2 only", px(P["t2 only"]), px(BLUE), "the blue triangle drawn")
P, T, how = psession("edges", CFG + header(False) + tri(LEFT, 2.0, 0xff0000) + tri(RIGHT, 2.0, 0xff0000)
                     + tri(RSPAN, 2.0, 0xff0000) + GO, ["l in", "l out", "r in", "r out", "rspan"])
row("edges l in", px(P["l in"]), px(RED), "R9: column 1 drawn (pins x > 0 from above)")
row("edges l out", px(P["l out"]), px(BLACK), "column 0 not drawn (x > 0 from below)")
row("edges r in", px(P["r in"]), px(RED), "column 639 drawn (x < xsize from below)")
row("edges r out", px(P["r out"]), px(BLACK), "x = 640 not wrapped onto row 331")
row("edges rspan", px(P["rspan"]), px(RED), "a span from x = 639.0 draws column 639")
P, T, how = psession("texedges", CFG + texels() + header(False, TEX_RED) + tri(LEFT, 2.0) + tri(RIGHT, 2.0) + tri(RSPAN, 2.0) + GO,
                     ["l in", "l out", "r in", "r out", "rspan"])
row("texedges l in", px(P["l in"]), px(RED), "R9 textured: column 1 drawn")
row("texedges l out", px(P["l out"]), px(BLACK), "column 0 not drawn")
row("texedges r in", px(P["r in"]), px(RED), "column 639 drawn")
row("texedges r out", px(P["r out"]), px(BLACK), "x = 640 not wrapped onto row 331")
row("texedges rspan", px(P["rspan"]), px(RED), "textured: column 639 from x = 639")
# ---- R10 (addendum 7): the depth compare's EQUAL edge.  Z-on T1 then Z-on T2 at the SAME z: under `<=` the later polygon wins.
P, T, how = psession("equal", CFG + header(False) + tri(T1, 2.0, 0xff0000) + header(False) + tri(T2, 2.0, 0x00ff00) + GO,
                     ["overlap", "t2 only"])
row("equal overlap", px(P["overlap"]), px(GREEN), "R10: equal z, the later polygon wins (<=)")
row("equal t2 only", px(P["t2 only"]), px(GREEN), "T2 drawn", control=True)
P, T, how = psession("texequal", CFG + texels() + header(False, TEX_RED) + tri(T1, 2.0) + header(False, TEX_GREEN) + tri(T2, 2.0) + GO,
                     ["overlap", "t2 only"])
row("texequal overlap", px(P["overlap"]), px(GREEN), "R10 textured: equal z, the later wins")
row("texequal t2 only", px(P["t2 only"]), px(GREEN), "T2 drawn from its texel", control=True)
# ---- the class closure (repair 2; the pass-2 adjudication).  Both rasterizers' y early return (TOP reaches row 0; BOTTOM row 479
# and, past the frame, row 480), the x1 > x2 swap (SWAP arrives reversed) and the span end at an EXACT integer (SWAP's slopes are
# +-0.5, so its row-180 span is exactly 365.0..435.0: `x < x2` drops pixel 435, `x <= x2 + 1` adds 436).
GEO = ["t in", "b in", "b out", "swap", "s end", "s past"]
P, T, how = psession("yedges", CFG + header(False) + tri(TOP, 2.0, 0xff0000) + tri(BOTTOM, 2.0, 0xff0000)
                     + tri(SWAP, 2.0, 0xff0000) + GO, GEO)
row("yedges t in", px(P["t in"]), px(RED), "row 0 drawn (y < 0 from above)")
row("yedges b in", px(P["b in"]), px(RED), "row 479 drawn (y >= ysize from below)")
row("yedges b out", px(P["b out"]), px(BLACK), "row 480 not drawn (past the frame)")
row("yedges swap", px(P["swap"]), px(RED), "a reversed span is swapped and drawn")
row("yedges s end", px(P["s end"]), px(RED), "span end x2 = 435.0 drawn (x <= x2)")
row("yedges s past", px(P["s past"]), px(BLACK), "x2 + 1 not drawn")
#  Repair 3: only the red texel is stored -- every texyedges vertex has u = v = 0 -- because with both texels this session sent 4104
#  bytes, past the STDIN CAP (docstring), and its `quit` was lost.
P, T, how = psession("texyedges", CFG + texel(TEXEL_LINEAR[TEX_RED], RED) + header(False, TEX_RED) + tri(TOP, 2.0) + tri(BOTTOM, 2.0)
                     + tri(SWAP, 2.0) + GO, GEO)
row("texyedges t in", px(P["t in"]), px(RED), "textured: row 0 drawn")
row("texyedges b in", px(P["b in"]), px(RED), "textured: row 479 drawn")
row("texyedges b out", px(P["b out"]), px(BLACK), "textured: row 480 not drawn")
row("texyedges swap", px(P["swap"]), px(RED), "textured: a reversed span drawn")
row("texyedges s end", px(P["s end"]), px(RED), "textured: span end 435 drawn")
row("texyedges s past", px(P["s past"]), px(BLACK), "textured: x2 + 1 not drawn")
# ---- the decode mask's two edges (repair 2): word 1 bit 26 is Z-write disable.  A header with bit 27 set (culling mode 1, which
# culls nothing) and one with bit 25 set (texture1, which the renderer decodes and ignores) must both still store depth: T2 (green,
# z 1.0) lies behind T1 (red, z 2.0).  One header per session: a session sending both (6088 bytes) passed the STDIN CAP (docstring)
# and lost its tail -- corrected 2026-11-05: this said such a session "outran the 90 s session limit".
P, T, how = psession("mask", CFG + ta([POLY0, MASK27, FOG2, 0, 0, 0, 0, 0]) + tri(T1, 2.0, 0xff0000) + header(False)
                     + tri(T2, 1.0, 0x00ff00) + GO, ["overlap", "t2 only"])
row("mask overlap", px(P["overlap"]), px(RED), "a bit-27 header still stores depth")
row("mask t2 only", px(P["t2 only"]), px(GREEN), "T2 drawn", control=True)
P, T, how = psession("mask25", CFG + ta([POLY0, MASK25, FOG2, 0, 0, 0, 0, 0]) + tri(T1, 2.0, 0xff0000) + header(False)
                     + tri(T2, 1.0, 0x00ff00) + GO, ["overlap"])
row("mask25 overlap", px(P["overlap"]), px(RED), "a bit-25 header still stores depth")
# ---- repair 3: the class closure, completed (r3_20261105/CLOSURE3.md; the CONTRACT in the docstring).  Each row names the variant it
# ---- catches and the pixel that differs; every want is derived from the sweep and the depth rule, and each variant was MEASURED to
# ---- survive the 68 rows before them (r3_20261105/PVR3_NOTE.md).
#  swap (simpleline).  SWAP row 180 arrives 435.0 then 365.0 and is swapped: its first column is 365, so column 364 stays black --
#  `int x = x1 - 1` (A) draws it red.  SWAP row 249, its last, arrives 400.5 then 399.5 (99 steps of -0.5 and +0.5, exact): swapped,
#  it draws 399 and 400 -- `x1 > x2 + 1` (B) leaves it reversed and draws nothing.  VERT row 150 arrives 300.0 and 300.0: unswapped,
#  its one pixel takes the start end's colour, vertex 1's green -- `x1 >= x2` (C) swaps in vertex 2's red.  FRAC row 101 ends at
#  150.5: `x <= x2` stops at 150 -- `x < x2 + 1` (I) draws 151 red.  Repair 4 (D2-F): swapped, row 249 STARTS at 399.5, which `int
#  x = x1` truncates to 399 -- `int x = x1 + 0.5` (B2, round to nearest) starts at 400 and leaves column 399 black.
P, T, how = psession("swap", CFG + header(False) + tri(SWAP, 2.0, 0xff0000) + tri_pv(VERT, (2.0, 2.0, 2.0), rgbs=(0x00ff00, 0xff0000, 0x00ff00))
                     + tri(FRAC, 2.0, 0xff0000) + GO, ["s before", "s tip", "vert", "frac past", "s start"])
row("swap s before", px(P["s before"]), px(BLACK), "A: the column before the start 365")
row("swap s tip", px(P["s tip"]), px(RED), "B: a span reversed by 1.0 is swapped")
row("swap vert", px(P["vert"]), px(GREEN), "C: equal ends not swapped (v1's green)")
row("swap frac past", px(P["frac past"]), px(BLACK), "I: past the end 150.5 (`x <= x2`)")
row("swap s start", px(P["s start"]), px(RED), "B2: the start 399.5 truncates to 399")
#  texswap (texturedline: the ends arrive as ints).  SWAP row 180: 435 and 365 -- column 364 black, red under A.  Row 249: 400 and
#  399, swapped to draw 399 and 400 -- nothing under B.  VERT row 150: 300 and 300, u 0.5 at the start end (vertex 1 -> 3) and 0.0
#  at the stop end (vertex 2): unswapped it samples u 0.5, texel (4,0), green -- under C it samples u 0.0, texel (0,0), red.
#  texturedline's `x < x2 + 1` is EQUIVALENT (integer ends), so there is no textured `frac past`.
P, T, how = psession("texswap", CFG + texels() + header(False, TEX_RED) + tri(SWAP, 2.0)
                     + tri_pv(VERT, (2.0, 2.0, 2.0), uvs=((0.5, 0.0), (0.0, 0.0), (0.5, 0.0))) + GO, ["s before", "s tip", "vert"])
row("texswap s before", px(P["s before"]), px(BLACK), "A textured: column 364 not drawn")
row("texswap s tip", px(P["s tip"]), px(RED), "B textured: 400 then 399 is swapped")
row("texswap vert", px(P["vert"]), px(GREEN), "C textured: unswapped u 0.5 (green)")
#  ramp (the swap BODY, simpleline).  RAMP row 60 arrives 520.0 (vertex 1: z 1.0, magenta) then 440.0 (vertex 2: z 2.0, green); the
#  swap moves vertex 2's z and colour to column 440, its first.  So (440,60) is green at z 2.0, and COVER (z 1.5, blue, drawn
#  after) fails `2.0 <= 1.5` there.  Delete the z exchange and column 440 gets z 1.0: COVER passes and draws blue.  Delete the r, g
#  or b exchange and that channel comes from vertex 1: yellow 0xffe0, black 0x0000, cyan 0x07ff.  (A span-start or swap edit that
#  moves or drops RAMP's first column shows here too: CLOSURE3.md.)
P, T, how = psession("ramp", CFG + header(False) + tri_pv(RAMP, (1.0, 2.0, 1.0), rgbs=(MAGENTA, 0x00ff00, MAGENTA))
                     + tri(COVER, 1.5, 0x0000ff) + GO, ["l end"])
row("ramp l end", px(P["l end"]), px(GREEN), "swap body: v2's z 2.0 and green at 440")
#  texramp (texturedline).  RAMP row 60: vertex 1 has z 1.0 and (u,v) (0.5, 0); vertex 2 has z 2.0 and (0, 0.125).  Swapped,
#  column 440 samples (0, 0.125), texel (0,1) = TEXEL01, stored blue, at z 2.0; COVER (z 1.5, u = v = 0, texel (0,0) red) fails
#  there.  Without the z exchange COVER passes (red); without the u exchange it samples texel (4,1), never stored (0x0000);
#  without the v exchange texel (0,0) (red).
P, T, how = psession("texramp", CFG + texel(TEXEL_LINEAR[TEX_RED], RED) + texel(TEXEL01, BLUE) + header(False, TEX_RED)
                     + tri_pv(RAMP, (1.0, 2.0, 1.0), uvs=((0.5, 0.0), (0.0, 0.125), (0.5, 0.0))) + tri(COVER, 1.5) + GO, ["l end"])
row("texramp l end", px(P["l end"]), px(BLUE), "swap body: v2's z and (u,v) at 440")
#  edges2 / texedges2: the x clauses' other truth cells.  LREV row 230 arrives 30.0 then -30.0 (x1 >= 0, x2 < 0): no clause holds,
#  so it is swapped and columns 1..30 drawn -- `(x2 < 0 && x2 < 0)` (D) returns early.  RREV row 400 arrives 700.0 then 639.0
#  (x1 >= xsize, x2 < xsize): swapped, column 639 drawn -- `(x1 >= xsize && x1 >= xsize)` (E) returns early, and so does the x2
#  compare tightened alone, `x2 >= d->xsize - 1` (639 >= 639).  LREV row 259, its last, arrives 1.0 then -1.0: swapped, it draws
#  columns -1..1, so column 1 -- the left clause's x1 compare moved up by TWO, `x1 < 2` (or `x1 < d->bytes_per_pixel`), returns early
#  there.  A move by one is EQUIVALENT (only column 0 changes, and column 0 is never drawn), so two is the compare's edge.  LEFT3 row
#  159 spans -1.0..1.0 (forward, x1 < 0): column 1 is drawn -- the x2 compare moved up by two, `x2 < 2` (or `x2 < d->bytes_per_pixel`),
#  returns early there (`x2 tip`; one is EQUIVALENT, as for x1).
P, T, how = psession("edges2", CFG + header(False) + tri(LREV, 2.0, 0xff0000) + tri(RREV, 2.0, 0xff0000) + tri(LEFT3, 2.0, 0xff0000)
                     + GO, ["l rev", "r rev", "l tip", "tip"])
row("edges2 l rev", px(P["l rev"]), px(RED), "D: 30 then -30, swapped: column 1 drawn")
row("edges2 r rev", px(P["r rev"]), px(RED), "E: 700 then 639, swapped: 639 drawn")
row("edges2 l tip", px(P["l tip"]), px(RED), "x1 < 2: 1.0 then -1.0 draws column 1")
row("edges2 x2 tip", px(P["tip"]), px(RED), "x2 < 2: -1.0..1.0 draws column 1")
P, T, how = psession("texedges2", CFG + texel(TEXEL_LINEAR[TEX_RED], RED) + header(False, TEX_RED) + tri(LREV, 2.0) + tri(RREV, 2.0)
                     + tri(LEFT3, 2.0) + GO, ["l rev", "r rev", "l tip", "tip"])
row("texedges2 l rev", px(P["l rev"]), px(RED), "D textured: column 1 drawn")
row("texedges2 r rev", px(P["r rev"]), px(RED), "E textured: column 639 drawn")
row("texedges2 l tip", px(P["l tip"]), px(RED), "x1 < 2 textured: 1 then -1 draws col 1")
row("texedges2 x2 tip", px(P["tip"]), px(RED), "x2 < 2 textured: -1..1 draws column 1")
#  zleft / texzleft: LEFT3 drawn by a Z-OFF polygon -- the Z-off twin of `x2 tip` (the Z-off twins of every other single-layer row
#  follow at the end).
P, T, how = psession("zleft", CFG + header(True) + tri(LEFT3, 2.0, 0xff0000) + GO, ["tip"])
row("zleft tip", px(P["tip"]), px(RED), "Z-off twin of edges2 x2 tip")
P, T, how = psession("texzleft", CFG + texel(TEXEL_LINEAR[TEX_RED], RED) + header(True, TEX_RED) + tri(LEFT3, 2.0) + GO, ["tip"])
row("texzleft tip", px(P["tip"]), px(RED), "Z-off twin of texedges2 x2 tip")
#  zeq / texzeq: the depth test's (equal, Z-off) cell.  Z-on T1 stores 2.0; Z-off T2 at the SAME 2.0 passes `2.0 <= 2.0` and draws
#  green (storing nothing) -- `vram_z < z || (!zwrite_disabled && vram_z == z)` (F) refuses it, leaving red.
P, T, how = psession("zeq", CFG + header(False) + tri(T1, 2.0, 0xff0000) + header(True) + tri(T2, 2.0, 0x00ff00) + GO, ["overlap"])
row("zeq overlap", px(P["overlap"]), px(GREEN), "F: a Z-off T2 at equal z still draws")
P, T, how = psession("texzeq", CFG + texels() + header(False, TEX_RED) + tri(T1, 2.0) + header(True, TEX_GREEN) + tri(T2, 2.0) + GO,
                     ["overlap"])
row("texzeq overlap", px(P["overlap"]), px(GREEN), "F textured: Z-off T2 at equal z draws")
#  maskoff: word 1 = bits 26 and 27 (word >> 26 = 3): `& 1` gives 1, Z-write disabled, so T1 stores no depth and T2 (z 1.0) draws over
#  it -- `== 1` (G) gives 0, T1 stores 2.0 and T2 fails.  maskhi: bits 28-31 with bit 26 clear (word >> 26 = 60): `& 1` gives 0, T1
#  stores depth and hides T2 -- the mask widened to bit 28, 29, 30 or 31 (`& 5`, `& 9`, `& 17`, `& 33`; H is `& 5`) disables T1's
#  store, and T2 draws green.
P, T, how = psession("maskoff", CFG + ta([POLY0, ZOFF27, FOG2, 0, 0, 0, 0, 0]) + tri(T1, 2.0, 0xff0000) + header(False)
                     + tri(T2, 1.0, 0x00ff00) + GO, ["overlap"])
row("maskoff overlap", px(P["overlap"]), px(GREEN), "G: bits 26+27 disable the store (& 1)")
P, T, how = psession("maskhi", CFG + ta([POLY0, MASKHI, FOG2, 0, 0, 0, 0, 0]) + tri(T1, 2.0, 0xff0000) + header(False)
                     + tri(T2, 1.0, 0x00ff00) + GO, ["overlap"])
row("maskhi overlap", px(P["overlap"]), px(RED), "H: bits 28-31 still store depth")
# ---- repair 3, the Z-OFF TWINS (the coordinator's ruling on the 09-04 floor: the cells a row is owed for are the cross-product of
# ---- every predicate dominating the guarded store with the state the repair path reads, zwrite_disabled).  Each session below is
# ---- a single-layer geometry session above with its header made Z-off.  A Z-off polygon goes through the same depth test and
# ---- rasterization and draws the same colour, and only its depth store is skipped; over the cleared frame the depth test passes
# ---- either way -- so each want is its Z-on twin's, derived the same way.  A row here reds when an edit treats Z-off geometry
# ---- differently from Z-on geometry at that edge, however many tokens the edit takes.  ztedges and ztyedges store only the red
# ---- texel they sample (the STDIN CAP).  (zleft above is `x2 tip`'s twin.)
P, T, how = psession("zedges", CFG + header(True) + tri(LEFT, 2.0, 0xff0000) + tri(RIGHT, 2.0, 0xff0000) + tri(RSPAN, 2.0, 0xff0000)
                     + GO, ["l in", "l out", "r in", "r out", "rspan"])
row("zedges l in", px(P["l in"]), px(RED), "Z-off twin: column 1 drawn")
row("zedges l out", px(P["l out"]), px(BLACK), "Z-off twin: column 0 not drawn")
row("zedges r in", px(P["r in"]), px(RED), "Z-off twin: column 639 drawn")
row("zedges r out", px(P["r out"]), px(BLACK), "Z-off twin: x = 640 not wrapped")
row("zedges rspan", px(P["rspan"]), px(RED), "Z-off twin: a span from 639.0")
P, T, how = psession("zyedges", CFG + header(True) + tri(TOP, 2.0, 0xff0000) + tri(BOTTOM, 2.0, 0xff0000) + tri(SWAP, 2.0, 0xff0000)
                     + GO, GEO)
row("zyedges t in", px(P["t in"]), px(RED), "Z-off twin: row 0 drawn")
row("zyedges b in", px(P["b in"]), px(RED), "Z-off twin: row 479 drawn")
row("zyedges b out", px(P["b out"]), px(BLACK), "Z-off twin: row 480 not drawn")
row("zyedges swap", px(P["swap"]), px(RED), "Z-off twin: reversed span drawn")
row("zyedges s end", px(P["s end"]), px(RED), "Z-off twin: span end 435.0 drawn")
row("zyedges s past", px(P["s past"]), px(BLACK), "Z-off twin: x2 + 1 not drawn")
P, T, how = psession("zswap", CFG + header(True) + tri(SWAP, 2.0, 0xff0000) + tri_pv(VERT, (2.0, 2.0, 2.0), rgbs=(0x00ff00, 0xff0000, 0x00ff00))
                     + tri(FRAC, 2.0, 0xff0000) + GO, ["s before", "s tip", "vert", "frac past", "s start"])
row("zswap s before", px(P["s before"]), px(BLACK), "Z-off twin: column 364 not drawn")
row("zswap s tip", px(P["s tip"]), px(RED), "Z-off twin: reversed by 1.0, swapped")
row("zswap vert", px(P["vert"]), px(GREEN), "Z-off twin: equal ends not swapped")
row("zswap frac past", px(P["frac past"]), px(BLACK), "Z-off twin: past the end 150.5")
row("zswap s start", px(P["s start"]), px(RED), "Z-off twin: the start 399.5 -> 399")
P, T, how = psession("zedges2", CFG + header(True) + tri(LREV, 2.0, 0xff0000) + tri(RREV, 2.0, 0xff0000) + GO,
                     ["l rev", "r rev", "l tip"])
row("zedges2 l rev", px(P["l rev"]), px(RED), "Z-off twin: 30 then -30 draws column 1")
row("zedges2 r rev", px(P["r rev"]), px(RED), "Z-off twin: 700 then 639 draws 639")
row("zedges2 l tip", px(P["l tip"]), px(RED), "Z-off twin: 1.0 then -1.0 draws col 1")
#  zramp: the swap body for a Z-OFF span.  COVER (Z-on, z 1.5, blue) is drawn FIRST and stores 1.5 at (440,60); then RAMP, Z-off:
#  swapped, column 440 carries vertex 2's z 2.0 and green, passes `1.5 <= 2.0`, and draws green (storing nothing).  Without the z
#  exchange column 440 has z 1.0, fails, and stays blue; without the r, g or b exchange: 0xffe0, 0x0000, 0x07ff.
P, T, how = psession("zramp", CFG + header(False) + tri(COVER, 1.5, 0x0000ff) + header(True)
                     + tri_pv(RAMP, (1.0, 2.0, 1.0), rgbs=(MAGENTA, 0x00ff00, MAGENTA)) + GO, ["l end"])
row("zramp l end", px(P["l end"]), px(GREEN), "Z-off swap body over a stored 1.5")
P, T, how = psession("ztedges", CFG + texel(TEXEL_LINEAR[TEX_RED], RED) + header(True, TEX_RED) + tri(LEFT, 2.0) + tri(RIGHT, 2.0)
                     + tri(RSPAN, 2.0) + GO, ["l in", "l out", "r in", "r out", "rspan"])
row("ztedges l in", px(P["l in"]), px(RED), "textured Z-off twin: column 1 drawn")
row("ztedges l out", px(P["l out"]), px(BLACK), "textured Z-off twin: column 0 not")
row("ztedges r in", px(P["r in"]), px(RED), "textured Z-off twin: column 639 drawn")
row("ztedges r out", px(P["r out"]), px(BLACK), "textured Z-off twin: 640 not wrapped")
row("ztedges rspan", px(P["rspan"]), px(RED), "textured Z-off twin: span from 639")
P, T, how = psession("ztyedges", CFG + texel(TEXEL_LINEAR[TEX_RED], RED) + header(True, TEX_RED) + tri(TOP, 2.0) + tri(BOTTOM, 2.0)
                     + tri(SWAP, 2.0) + GO, GEO)
row("ztyedges t in", px(P["t in"]), px(RED), "textured Z-off twin: row 0 drawn")
row("ztyedges b in", px(P["b in"]), px(RED), "textured Z-off twin: row 479 drawn")
row("ztyedges b out", px(P["b out"]), px(BLACK), "textured Z-off twin: row 480 not")
row("ztyedges swap", px(P["swap"]), px(RED), "textured Z-off twin: reversed span")
row("ztyedges s end", px(P["s end"]), px(RED), "textured Z-off twin: span end 435")
row("ztyedges s past", px(P["s past"]), px(BLACK), "textured Z-off twin: x2 + 1 not drawn")
P, T, how = psession("ztswap", CFG + texels() + header(True, TEX_RED) + tri(SWAP, 2.0)
                     + tri_pv(VERT, (2.0, 2.0, 2.0), uvs=((0.5, 0.0), (0.0, 0.0), (0.5, 0.0))) + GO, ["s before", "s tip", "vert"])
row("ztswap s before", px(P["s before"]), px(BLACK), "textured Z-off twin: 364 not drawn")
row("ztswap s tip", px(P["s tip"]), px(RED), "textured Z-off twin: 400 then 399")
row("ztswap vert", px(P["vert"]), px(GREEN), "textured Z-off twin: u 0.5 (green)")
P, T, how = psession("ztedges2", CFG + texel(TEXEL_LINEAR[TEX_RED], RED) + header(True, TEX_RED) + tri(LREV, 2.0) + tri(RREV, 2.0) + GO,
                     ["l rev", "r rev", "l tip"])
row("ztedges2 l rev", px(P["l rev"]), px(RED), "textured Z-off twin: column 1 drawn")
row("ztedges2 r rev", px(P["r rev"]), px(RED), "textured Z-off twin: column 639 drawn")
row("ztedges2 l tip", px(P["l tip"]), px(RED), "textured Z-off twin: 1 then -1, col 1")
#  ztramp: COVER textured (Z-on, z 1.5, texel (0,0) red) first, then RAMP textured and Z-off: column 440 samples (0, 0.125), texel
#  (0,1), blue, at z 2.0 and passes.  No z exchange: z 1.0 fails, red stays; no u exchange: texel (4,1), 0x0000; no v: texel (0,0).
P, T, how = psession("ztramp", CFG + texel(TEXEL_LINEAR[TEX_RED], RED) + texel(TEXEL01, BLUE) + header(False, TEX_RED) + tri(COVER, 1.5)
                     + header(True, TEX_RED) + tri_pv(RAMP, (1.0, 2.0, 1.0), uvs=((0.5, 0.0), (0.0, 0.125), (0.5, 0.0))) + GO, ["l end"])
row("ztramp l end", px(P["l end"]), px(BLUE), "textured Z-off swap body over 1.5")

# ---- REPAIR 4 (pass 4; ruling ../artifacts/pvrrenderexit/adj_p4_20261105/ADJ_MYTHOS_local.md, rule D2-F): each simpleline position
# ---- compare pinned at the HALF PIXEL as well as at the pixel, and the swap body at a reversed span's FAR end.  Each variant named
# ---- was MEASURED to survive the 128 rows before these (r4_20261105/meas_B/SCORES.txt).
#  half (simpleline).  HALF row 103 arrives 101.25 then 100.75, reversed by half a pixel: swapped, it draws 100 and 101 -- `x1 > x2
#  + 0.5` (B1) leaves it reversed and draws nothing, so column 101 is black.  HALFR1 row 401 arrives 639.5 then 670.0: 639.5 is
#  below xsize, so the row is drawn from (int) 639.5 = 639 -- `x1 >= d->xsize - 0.5` (B13) returns early.  HALFR2 row 411 arrives
#  670.0 then 639.5: `x2 >= d->xsize - 0.5` (B14) returns early; the fix swaps it and draws 639.  (`int x = x1 + 0.5`, B2, starts
#  both right-edge rows at 640: nothing drawn.)  The two right-edge pixels sit on different rows, so neither triangle masks the other.
HALFS = tri(HALF, 2.0, 0xff0000) + tri(HALFR1, 2.0, 0xff0000) + tri(HALFR2, 2.0, 0xff0000)
P, T, how = psession("half", CFG + header(False) + HALFS + GO, ["half", "half r1", "half r2"])
row("half swap", px(P["half"]), px(RED), "B1: a span reversed by 0.5 is swapped")
row("half r x1", px(P["half r1"]), px(RED), "B13: x1 = 639.5 is not past the edge")
row("half r x2", px(P["half r2"]), px(RED), "B14: x2 = 639.5 is not past the edge")
P, T, how = psession("zhalf", CFG + header(True) + HALFS + GO, ["half", "half r1", "half r2"])
row("zhalf swap", px(P["half"]), px(RED), "Z-off twin: reversed by 0.5, swapped")
row("zhalf r x1", px(P["half r1"]), px(RED), "Z-off twin: x1 = 639.5 drawn at 639")
row("zhalf r x2", px(P["half r2"]), px(RED), "Z-off twin: x2 = 639.5 drawn at 639")
#  ramp8: the swap body's RIGHT end.  RAMP8 (depths 2, 1, 2; magenta, green, magenta) row 60 arrives 448.0 (vertex 1) then 440.0
#  (vertex 2): swapped, column 448 is eight exact steps (dz 0.125, dr 31.875) from 440 and carries vertex 1's z 2.0 and magenta;
#  COVER8 (Z-on, z 1.5, blue) drawn after it fails there.  Deleting only `z2 = tmpf` leaves z flat at 1.0, so COVER8 draws blue;
#  only `r2 = tmpf`, `g2 = tmpf` or `b2 = tmpf`: 0x001f, 0xffff, 0xf800.  The `l end` rows read column 440, which `z1 = z2` (and
#  r1, g1, b1) still supplies.  zramp8: COVER8 (Z-on) FIRST, then RAMP8 Z-off: 2.0 passes over the stored 1.5 and draws magenta.
RAMP8S = tri_pv(RAMP8, (2.0, 1.0, 2.0), rgbs=(MAGENTA, 0x00ff00, MAGENTA))
P, T, how = psession("ramp8", CFG + header(False) + RAMP8S + tri(COVER8, 1.5, 0x0000ff) + GO, ["r end"])
row("ramp8 r end", px(P["r end"]), px(0xf81f), "B4-B7: the swap body at the right end")
P, T, how = psession("zramp8", CFG + header(False) + tri(COVER8, 1.5, 0x0000ff) + header(True) + RAMP8S + GO, ["r end"])
row("zramp8 r end", px(P["r end"]), px(0xf81f), "Z-off twin: 2.0 passes over 1.5")
#  texramp8: RAMP8 textured, (u,v) (0.5,0) (0,0.125) (0.5,0): column 448 samples (0.5, 0), texel (4,0), green, at z 2.0; COVER8
#  textured through TEX_01 (its texel (0,0) is TEXEL01, stored blue) fails there.  Deleting only `z2 = tmpf`: z 1.0, COVER8's blue;
#  only `u2 = tmpf`: texel (0,0), red; only `v2 = tmpf`: texel (4,1), never stored, 0x0000.  (Blue keeps the z2, u2 and v2
#  signatures distinct; a red COVER8 would merge the first two without hiding either.  Corrected 2026-11-05, repair 5 -- codex pass
#  5, R2: this said a red COVER8 "would hide the u2 case".)
TRAMP8S = tri_pv(RAMP8, (2.0, 1.0, 2.0), uvs=((0.5, 0.0), (0.0, 0.125), (0.5, 0.0)))
TEX8 = CFG + texels() + texel(TEXEL01, BLUE)
P, T, how = psession("texramp8", TEX8 + header(False, TEX_RED) + TRAMP8S + header(False, TEX_01) + tri(COVER8, 1.5) + GO, ["r end"])
row("texramp8 r end", px(P["r end"]), px(GREEN), "B8-B10: textured swap body, right end")
P, T, how = psession("ztramp8", TEX8 + header(False, TEX_01) + tri(COVER8, 1.5) + header(True, TEX_RED) + TRAMP8S + GO, ["r end"])
row("ztramp8 r end", px(P["r end"]), px(GREEN), "textured Z-off twin over 1.5")

# ---- REPAIR 5 (pass 5; ruling ../artifacts/pvrrenderexit/adj_p5_20261105/ADJ_MYTHOS_local.md): the swap body's `tmpf = z1` read at
# ---- the right end from ABOVE, and the span start at a NEGATIVE x1.  Each variant named was MEASURED to survive the 140 rows before
# ---- these (r5_20261105/meas140/SCORES.txt).
#  ramp8hi.  RAMP8 with depths (3, 2, 3) (magenta, green, magenta) stores 3.0 at column 448 and 2.0 at 440; COVERHI (Z-on, z 4.0,
#  blue) drawn after it passes over both, so both are blue.  Deleting only `tmpf = z1` leaves tmpf holding the original x1, so z2 =
#  448.0 and COVERHI fails at 448: magenta.  zramp8hi: COVERHI (Z-on) FIRST, then RAMP8 Z-off: 3.0 fails against the stored 4.0 and
#  (448,60) stays blue; the deletion's 448.0 passes and draws magenta.  The two optional rows read (440,60): `z1 += z2` and `z1 *=
#  z2` put 5.0 and 6.0 there, so COVERHI fails (Z-on) or RAMP8 passes (Z-off) and green shows -- measured, r5_20261105/meas_cand/.
RAMP8HI = tri_pv(RAMP8, (3.0, 2.0, 3.0), rgbs=(MAGENTA, 0x00ff00, MAGENTA))
P, T, how = psession("ramp8hi", CFG + header(False) + RAMP8HI + tri(COVERHI, 4.0, 0x0000ff) + GO, ["r end", "l end"])
row("ramp8hi r end", px(P["r end"]), px(BLUE), "`tmpf = z1` at the right end, from above")
row("ramp8hi l end", px(P["l end"]), px(BLUE), "the left end from above (stored 2.0)")
P, T, how = psession("zramp8hi", CFG + header(False) + tri(COVERHI, 4.0, 0x0000ff) + header(True) + RAMP8HI + GO, ["r end", "l end"])
row("zramp8hi r end", px(P["r end"]), px(BLUE), "Z-off twin: 3.0 fails against 4.0")
row("zramp8hi l end", px(P["l end"]), px(BLUE), "Z-off twin: 2.0 fails against 4.0")
#  negx (simpleline).  NEGX (green, red, green; z 2.0) row 60 arrives -1.0 then 1.0: `int x = x1` starts at -1, so column 1 is the
#  third step (dr12 127.5) and carries vertex 2's exact red.  `int x = x1 + 0.25` (N1s) truncates -0.75 toward zero: it starts at
#  0 and puts the midpoint, 0x7be0, at column 1.  texnegx: NEGX textured, u 0 -> 0.5 (du12 0.25): column 1 samples u 0.5, texel
#  (4,0), green; `int x = x1 + 0.5` (B2t) starts at 0 and samples u 0.25, texel (2,0) (linear 0x500000, never stored): 0x0000.
NEGXS = tri_pv(NEGX, (2.0, 2.0, 2.0), rgbs=(0x00ff00, 0xff0000, 0x00ff00))
TNEGXS = tri_pv(NEGX, (2.0, 2.0, 2.0), uvs=((0.0, 0.0), (0.5, 0.0), (0.0, 0.0)))
P, T, how = psession("negx", CFG + header(False) + NEGXS + GO, ["n start"])
row("negx n start", px(P["n start"]), px(RED), "N1s: the start -1.0 at its exact value")
P, T, how = psession("znegx", CFG + header(True) + NEGXS + GO, ["n start"])
row("znegx n start", px(P["n start"]), px(RED), "Z-off twin: column 1 the third step")
P, T, how = psession("texnegx", CFG + texels() + header(False, TEX_RED) + TNEGXS + GO, ["n start"])
row("texnegx n start", px(P["n start"]), px(GREEN), "B2t: the int start -1, u 0.5 at column 1")
P, T, how = psession("ztnegx", CFG + texels() + header(True, TEX_RED) + TNEGXS + GO, ["n start"])
row("ztnegx n start", px(P["n start"]), px(GREEN), "textured Z-off twin: u 0.5 at column 1")

n_ok = sum(1 for _, ok in rows if ok)
red = [n for n, ok in rows if not ok]
print("elapsed %.1fs" % (time.time() - t0))
print("PVR_ZWRITE_RESULT=%d/%d" % (n_ok, len(rows)))
print("PVR_ZWRITE_CONTROL=%s" % ("OK" if all(ok for _, ok in controls) else "FAIL"))
print("PVR_ZWRITE_SYMPTOM=%s" % ("PRESENT" if symptom_hits else "ABSENT"))
print("PVR_ZWRITE_RED=%s" % (",".join(n.replace(" ", "_") for n in red) if red else "none"))
print("PVR_ZWRITE_PROBE_DONE")
