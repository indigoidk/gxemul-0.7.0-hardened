Begin your answer with the token MYTHOSREGPVR on its own line, then `model: <your model name>`, then your verdict line.  You may
open files under C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/ READ-ONLY to check a claim; write nothing, build nothing, run no git command
that writes.  The tree under review is GXEMUL-SEC/src/ and GXEMUL-SEC/regress/; ignore any other src/ you find (the project root
holds pristine 2021 upstream copies).  The probe, the gate block and dev_pvr.c below are the STAGED copies the commit will carry (also
at C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/wpvr/landing/staged/).  The working tree's regress/gate_arm.sh still holds pvr's OLD 68-row
block and other rounds' uncommitted blocks, so read the gate block HERE; the working tree's probe differs from the staged one only
in its docstring (block A's caption).

# REGRESS REVIEW (the Fable-only stage) -- round #581 `pvrrenderexit`: the detector as it will ship

**PROJECT FRAMING -- this is a defensive software-robustness project.**  GXemul is a computer-architecture emulator: a developer tool
that runs legacy operating systems in a software sandbox for research and preservation.  This fork is a HARDENING effort -- ordinary
software-correctness engineering on the emulator's own C code, each fix shipped with a regression test that keeps it fixed.  There is
no attack, no target system and no affected third party; the guest is a few instruction words under test INSIDE the emulator, and the
host is the emulator process on the developer's own machine.  This round removes a place where the emulator ended its own process on
ordinary guest input.  **Vocabulary**: a *test variant* is a deliberately broken copy of the fix used to measure whether the
regression test notices it; *detected* / *red* = a row failed; *green* (a variant) = every row passed; a *null medium* is a run with
no working emulator behind the probe (a non-emulator binary, a missing one).

**Your role: the flagship's REGRESS review**, the fable5 slot's step (owner, 2026-11-05: Mythos is that slot, run locally, as for
#575, memc and qhs).  By standing owner directive only the flagship seat reviews the `regress` stage.  THE ROUND:
`src/devices/dev_pvr.c`, pvr_render(): a STARTRENDER write renders the Tile Accelerator commands the guest submitted; for a polygon
header whose list word 1 sets bit 26 (Z-write DISABLED, `zwrite = !((list[1] >> 26) & 1)`), HEAD printed "pvr: no zwrite? not
implemented yet." and called exit(1).  The rung-3 witness (block H2) measured that exit on the committed build.  The fix (block G):
a `zwrite_disabled` field; both rasterizers (simpleline, texturedline) keep the depth TEST and skip only their `vram_z` store when it
is set; case 4 assigns it from the header's bit; every pvr_render clears it first.  The three sibling exits keep their own
disposition.  The detector is regress/pvr_zwrite_probe.py (148 rows, 54 debugger sessions on UNMODIFIED `-E dreamcast`; block A,
whose docstring is the CONTRACT) in gate 14 (block B).  It grew through five numbered test-variant tables on the 51-, 68-, 128-, 140-
and 148-row probes (det_20261104/table1/, r2_20261105/table2/, r3_20261105/table3/, r4_20261105/table4/, r5_20261105/table5/) and
review passes p2..p7 on the diff, with rulings after passes 2, 4, 5 and 6 (block F3).  THE FLOOR CHAIN CLOSED AT PASS 7 (0 breaches
over 272 exchange-body cells) and the records chain at recp7 (7 accepted, 0 to fix) -- block F.  The pass-6 ruling (block F1,
CLOSE-AFTER-RECORDS) enumerated every single-site edit shape on the two exchange bodies of the x1 > x2 swap; the contract's EDIT
SHAPES paragraph restates it with the repair-6 and pass-7 corrections (block F2).  NO SEAT HAS REVIEWED THE DETECTOR AS IT WILL LAND
as one object -- the probe after the pass-7 records, the 148-row gate block, the filings -- and gate 14 last ran the pvr block IN
SITU on the 51-row probe (block H2), so this review is also the first reading of the 148-row block's pins (block H1 replays them over
table 5's banked logs).

Mark each claim CHECKED-IN-PACKET (block + line), CHECKED-IN-TREE (file:line you opened), REASONED, or UNSETTLED (name the one
measurement that settles it -- the main loop runs it).  A finding is fixed in this round only if it is a floor breach (L2), an
undischarged obligation (L3) or a wrong record (L4); everything else is FILED with its warrant.  Rows are owed per enumerated wrong
version of the fix inside the DEPENDS-ON bound (the predicates dominating the edited lines, walked to the enclosing function; operand
swaps only from fields the guarded body reads -- defined on the GUARD's operands, block F1 section 1; joint cells only where the
body's own tests distinguish them; the FLOOR is the guard's dominating predicates crossed with the device-state lvalues the repair
path reads that are jointly reachable -- here `zwrite_disabled`, hence the Z-off twins), never per possible state; a filter may
reject or repair a row, never demand one outside the bound.  Count the arguments, not the seats: an agreement that only restates a
packet's premise is no evidence.

**PREMISES PUT AS QUESTIONS -- please do not simply ratify; on this project seven of nine seats once confirmed a premise a brief
stated wrongly.  Check each against the tree:**
* P1. I believe the floor is the contract's COVERED list: per rasterizer, the y early return, the left and right x clauses (truth
  cells and each compare at its edge), the x1 > x2 swap (by more than one, by one, by half a pixel, equal ends) and its body's 24
  deletion cells, the span start (an exact start, x.5, a NEGATIVE start), the span end, the inner x bounds, the depth test x
  Z-write, and the decode's single-edit forms -- each for a Z-off polygon through its Z-off twin; plus the per-render reset and case
  4's assignment (the M-series).  Is any predicate or body-read lvalue of the shipped simpleline(), texturedline() or pvr_render()
  missing?  And is the pass-6 ruling's reading (i) -- the exchange bodies' non-deletion edits are clause-(e) DEBT -- right?
* P2. I believe none of table 5's 30 green variants (block C: 8 EQUIVALENT; 3 DEBT that D2-F grades SAMPLED -- B3s `x <= x2 +
  0.25`, B11s and B12t `vram_z <= z + 0.25`; 19 compound DEBT) lies inside that floor.  Is there one?
* P3. I believe clause (b) has ONE removed defect, the exit, and B1_exit (the four lines reinstated verbatim after the new
  assignment) reds every row of every session carrying a Z-off header but `zoff rendered` (green by design: the render is reached
  before the exit) -- table 5: 70/148 SYMPTOM=PRESENT, HEAD's red set exactly -- and that the field, the two guarded stores, case
  4's assignment and the reset are ADDITIONS whose nulling is clause (d) (the contract's M-series, in its CLAUSE (e) paragraph).
  Is that the right split?
* P4. I believe clause (c) is discharged by three null media measured on table 5 (/bin/true, an absent binary, /bin/false: 9, 0
  and 1 of 148, each CONTROL=FAIL) -- the carrier's runtime-probe form, "an ABSENT or NON-EMULATOR binary".  Which of the two
  record forms (`(c): measured at <artifact>` / `(c): by construction via <pin>`) is right here, and does the gate's equality pin
  on the row count matter?
* P5. I believe every one of the block's 157 checks can fail (block H1: each failed on at least one replayed leg), and that it
  needs no check of PVR_ZWRITE_RED= or of the sentinel's position.  Can any check not fail, and is either missing check owed?
* P6. I believe the STDIN cap (the probe refuses any session over 4096 bytes; the largest, ztyedges, sends 4066) keeps every
  session's input whole.  Could a session lose input BELOW the cap, i.e. is the 4100-at-the-first-step derivation (contract, STDIN
  CAP) right for every session, including id and neg?
* P7. I believe the contract applies round rule D2-F (the pass-4 ruling, corrected by pass 5's and pass 6's R3) as last corrected:
  position compares pinned at the pixel and the half pixel in simpleline; the span START a truncation, exhausted only down to its
  double resolution; texturedline's compare moves EQUIVALENT; the depth compare unit-less.  Is any D2-F statement in the contract
  false, or stated beyond what was measured?  (Whether D2-F enters the carrier is the OWNER's call, filed as F6 in block D.)

**Write your answer in this order** (it is banked as regress/artifacts/pvrrenderexit/regress_20261105/REG_MYTHOS_local.md):
1. Evidence basis (which blocks and which files you opened).
2. The vacuity floor, clause by clause, each with the artifact that discharges it or the breach: (a) the pre-fix build fails;
   (b) a verbatim reinstatement of the removed defect at EVERY fixed site fails (P3); (c) a null medium fails (P4); (d) null-repair
   over the DEPENDS-ON floor (P1, P2), D2-F included (P7); (e) the contract in the probe header: true as written, and complete for
   what table 5 measured -- the COVERED and NOT COVERED lists, the EDIT SHAPES enumeration (a)-(j) and its remedy sets, the
   discloses; (f) anchors -- which rows pin WHERE a span lands rather than only that something changed (ask: if every pixel moved
   one column, which row reds?  if a span bound moved by a half pixel, which row reds?).
3. Gate 14's pvr block (block B): does every pin red under (i) a dead probe, (ii) a probe that silently loses rows, (iii) a probe that
   adds a row, (iv) a probe whose sentinel prints but whose RESULT line is missing?  Name any pin that cannot fail.  Does block H1
   show what it claims?  Is the block's comment true (counts, timings, the tables' claims)?
4. The tables (block C; r5_20261105/PRETABLE_5.out by path): is any row VACUOUS by construction (its observable cannot vary under
   the variant it is meant to catch)?  Is any detection credited to a different row than the record claims?  Are the 30 green
   variants correctly disclosed -- each EQUIVALENT or DEBT as named, none inside the floor?
5. Records: wrong numbers or claims in the probe header (block A -- including the landing's own docstring edits, the round number
   and thirteen historical scores put in words for section U), the gate comment (block B), VERDICT.md (block C), RECORDS6_NOTE
   (block F2), the dispositions (F3), and the filings list (block D: is any owed filing missing, any listed one wrong?).  One
   sentence to test: the probe header ends "its null media are predicted in r5_20261105/PRETABLE_5.out" -- table 5 has since
   measured them; is that a wrong record or an incomplete true one?
6. The main loop's dispositions: which accepted disposition is wrong?  Counted (block F3): pass 3 -- codex 15 breaches and 5 records,
   all taken into repair 3, Gemini twice; pass 4 -- codex 14 and 8, ruled 11 FLOOR 3 DEBT 8 RECORDS; pass 5 -- codex 27 and 2,
   ruled 3 FLOOR 26 DEBT 2 RECORDS (and the ruler's own R3); pass 6 -- codex 20 and 1, ruled 0 FLOOR 29 DEBT 1 RECORD; pass 7 --
   0 breaches, 7 records, each deleted or narrowed; recp7 -- 7 accepted, 0 to fix.  Is the zero-floor disposition right?
7. Which of your own findings is weakest, and what would overturn it.
Final line: `MYTHOSREGPVR: <n> CHECKS <b> FLOOR-BREACHES <r> RECORD-FINDINGS VERDICT:<REGRESS-CLEAN|REGRESS-WITH-FINDINGS|REGRESS-BREACH>`

Files you may open (READ-ONLY) if a block is not enough, under GXEMUL-SEC/regress/artifacts/pvrrenderexit/: r5_20261105/PRETABLE_5.out (the predictions,
written before the first result), r5_20261105/table5/SCORES.txt, TABLE.log and the 196 probe_*.out logs, r5_20261105/pvr_table5.py
and pvr_variants_5.py (the walker and the variant builder), r5_20261105/PVR5_NOTE.md and CHANNELS5.txt, r4_20261105/PVR4_NOTE.md,
r3_20261105/CLOSURE3.md (the class closure), adj_p4_20261105/ and adj_p5_20261105/ADJ_MYTHOS_local.md (the rulings that minted
D2-F and the deletion closure), p3..p7_20261105/ (each pass's answer and DISPOSITION.md), and regress/pvr_zwrite_probe.py (the
probe's code; identical to the staged copy's outside the docstring).

---

### A. the CONTRACT: the staged probe's docstring (regress/pvr_zwrite_probe.py as it will ship: the working copy with `THE FIX (#NNN).` set to #581 and the history paragraph's thirteen N/M scores of the 68-, 128- and 140-row instruments put in words -- section U reads ten of them as stale claims against the 148-row pin.  PROBE_IDENTITY_pvr.md proves the syntax tree minus the docstring, every string kept, equal to the working copy's and to table 5's frozen instrument)

```
#!/usr/bin/env python3
"""pvrrenderexit -- DETECTOR (built on its rung-3 witness) for the Dreamcast PVR renderer's Z-write-disable exit, dev_pvr.c.

DEFECT (filed 2026-10-02).  src/devices/dev_pvr.c, pvr_render(): a STARTRENDER write renders the Tile Accelerator commands the
guest submitted; for a polygon header whose list word 1 has bit 26 set (Z-write DISABLED, `zwrite = !((list[1] >> 26) & 1)`)
the renderer printed "pvr: no zwrite? not implemented yet." and called exit(1) -- the emulator process ended.

THE FIX (#581).  Such a polygon goes through the same depth test and rasterization as any other polygon, and only its depth store
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
68-row probe the pre-fix build scored 42 of the 68 rows with the symptom PRESENT, and three null media -- /bin/true 9 of 68, an absent
binary 0 of 68, /bin/false 1 of 68 -- each CONTROL=FAIL (r2_20261105/table2/SCORES.txt).  The 128-row probe (repair 3): the fix 128 of 128
in ~3 s with no session timed out, the pre-fix build 60 of 128 with the symptom PRESENT (r3_20261105/base128/, head128/: table 2's 26
red rows plus every repair-3 row whose session carries a Z-off header, 42), and its null media 9 of 128, 0 of 128 and 1 of 128
(r3_20261105/table3/SCORES.txt).  The 140-row probe (repair 4): the fix 140 of 140 in ~2 s with no session timed out (48 sessions),
and the pre-fix build 66 of 140 with the symptom PRESENT (r4_20261105/base140/, head140/: the 128-row probe's 68 red rows plus the six
repair-4 rows whose session carries a Z-off header -- `zswap s start`, zhalf's three, `zramp8 r end`, `ztramp8 r end`), and its
null media 9 of 140, 0 of 140 and 1 of 140 (r4_20261105/table4/SCORES.txt).  This 148-row probe (repair 5): the fix 148/148 in ~2 s with
no session timed out (54 sessions), and the pre-fix build 70/148 with the symptom PRESENT (r5_20261105/base148/, head148/: the
140-row probe's 74 red rows plus the four repair-5 rows whose session carries a Z-off header -- `zramp8hi r end`, `zramp8hi l end`,
`znegx n start`, `ztnegx n start`); its null media are predicted in r5_20261105/PRETABLE_5.out.

Sentinel: PVR_ZWRITE_PROBE_DONE (plus PVR_ZWRITE_RESULT=n/N, _CONTROL=OK|FAIL, _SYMPTOM=PRESENT|ABSENT, _RED=none|<names>).
Session transcripts go to the optional [workdir].
"""
```

### A2. the 148 rows as the probe prints them

```
(name, want, note: table 5's base log, r5_20261105/table5/probe_base.out, every row ok -- its got column equals want; the staged probe prints these strings exactly: PROBE_IDENTITY_pvr.md.  Controls (control=True in row()): neg apparatus, id session, id r8, zon session, zon rendered, zon prompt, zoff rendered, ovon t2 only, ovon t1 only, ovon bg, texon t2 only, equal t2 only, texequal t2 only, mask t2 only.  The session is the row name's first word; its pixel is PIX[the rest] in block A3.)
neg apparatus    exit1/none   a bogus machine runs no guest
id session       exit0        mov.l @r7,r8 from the PVR ID register
id r8            0x17fd11db   the device answers (RAM would not)
zon session      exit0        Z-write ENABLED render: survives
zon rendered     yes          the renderer saw the one TA command
zon prompt       yes          the debugger ran `reg` afterwards
zoff rendered    yes          the render was reached (both builds)
zoff session     exit0        Z-write DISABLED render: survives
zoff prompt      yes          the debugger ran `reg` afterwards
ovoff session    exit0        R2: T1 Z-off red, T2 green behind it
ovoff overlap    0x07e0       T1 stored no depth, so T2 draws over it
ovoff t2 only    0x07e0       T2 drawn
ovoff t1 only    0xf800       T1 drawn (not declined)
ovoff bg         0x0000       the frame was cleared
ovon overlap     0xf800       R3: both Z-on: T1's depth hides T2
ovon t2 only     0x07e0       T2 drawn
ovon t1 only     0xf800       T1 drawn
ovon bg          0x0000       the frame was cleared
behind session   exit0        R6: T1 Z-on red, T2 Z-off green behind
behind overlap   0xf800       a Z-off T2 still fails the depth test
behind t2 only   0x07e0       T2 drawn where it passes
behind t1 only   0xf800       T1 drawn
texoff session   exit0        R4: T1 textured Z-off (red texel)
texoff overlap   0x07e0       texturedline stored no depth for T1
texoff t1 only   0xf800       T1 drawn from its texel
texoff t2 only   0x07e0       T2 drawn
texbeh session   exit0        R7: textured T1 Z-on, textured T2 Z-off
texbeh overlap   0xf800       textured Z-off T2 fails the depth test
texbeh t2 only   0x07e0       T2 drawn from its texel
texbeh t1 only   0xf800       T1 drawn from its texel
texon overlap    0xf800       R7: both textured Z-on: T1 hides T2
texon t2 only    0x07e0       T2 drawn from its texel
two session      exit0        R5: a Z-off render, then bare vertices
two overlap      0xf800       render 2 has no header: Z-write is on
two t1 only      0xf800       headerless vertices draw
two t2 only      0x07e0       T2 drawn
sticky session   exit0        R8: a Z-off header, then a Z-on one
sticky overlap   0x07e0       the Z-on header re-enabled the store
sticky t2 only   0x001f       the blue triangle drawn
edges l in       0xf800       R9: column 1 drawn (pins x > 0 from above)
edges l out      0x0000       column 0 not drawn (x > 0 from below)
edges r in       0xf800       column 639 drawn (x < xsize from below)
edges r out      0x0000       x = 640 not wrapped onto row 331
edges rspan      0xf800       a span from x = 639.0 draws column 639
texedges l in    0xf800       R9 textured: column 1 drawn
texedges l out   0x0000       column 0 not drawn
texedges r in    0xf800       column 639 drawn
texedges r out   0x0000       x = 640 not wrapped onto row 331
texedges rspan   0xf800       textured: column 639 from x = 639
equal overlap    0x07e0       R10: equal z, the later polygon wins (<=)
equal t2 only    0x07e0       T2 drawn
texequal overlap 0x07e0       R10 textured: equal z, the later wins
texequal t2 only 0x07e0       T2 drawn from its texel
yedges t in      0xf800       row 0 drawn (y < 0 from above)
yedges b in      0xf800       row 479 drawn (y >= ysize from below)
yedges b out     0x0000       row 480 not drawn (past the frame)
yedges swap      0xf800       a reversed span is swapped and drawn
yedges s end     0xf800       span end x2 = 435.0 drawn (x <= x2)
yedges s past    0x0000       x2 + 1 not drawn
texyedges t in   0xf800       textured: row 0 drawn
texyedges b in   0xf800       textured: row 479 drawn
texyedges b out  0x0000       textured: row 480 not drawn
texyedges swap   0xf800       textured: a reversed span drawn
texyedges s end  0xf800       textured: span end 435 drawn
texyedges s past 0x0000       textured: x2 + 1 not drawn
mask overlap     0xf800       a bit-27 header still stores depth
mask t2 only     0x07e0       T2 drawn
mask25 overlap   0xf800       a bit-25 header still stores depth
swap s before    0x0000       A: the column before the start 365
swap s tip       0xf800       B: a span reversed by 1.0 is swapped
swap vert        0x07e0       C: equal ends not swapped (v1's green)
swap frac past   0x0000       I: past the end 150.5 (`x <= x2`)
swap s start     0xf800       B2: the start 399.5 truncates to 399
texswap s before 0x0000       A textured: column 364 not drawn
texswap s tip    0xf800       B textured: 400 then 399 is swapped
texswap vert     0x07e0       C textured: unswapped u 0.5 (green)
ramp l end       0x07e0       swap body: v2's z 2.0 and green at 440
texramp l end    0x001f       swap body: v2's z and (u,v) at 440
edges2 l rev     0xf800       D: 30 then -30, swapped: column 1 drawn
edges2 r rev     0xf800       E: 700 then 639, swapped: 639 drawn
edges2 l tip     0xf800       x1 < 2: 1.0 then -1.0 draws column 1
edges2 x2 tip    0xf800       x2 < 2: -1.0..1.0 draws column 1
texedges2 l rev  0xf800       D textured: column 1 drawn
texedges2 r rev  0xf800       E textured: column 639 drawn
texedges2 l tip  0xf800       x1 < 2 textured: 1 then -1 draws col 1
texedges2 x2 tip 0xf800       x2 < 2 textured: -1..1 draws column 1
zleft tip        0xf800       Z-off twin of edges2 x2 tip
texzleft tip     0xf800       Z-off twin of texedges2 x2 tip
zeq overlap      0x07e0       F: a Z-off T2 at equal z still draws
texzeq overlap   0x07e0       F textured: Z-off T2 at equal z draws
maskoff overlap  0x07e0       G: bits 26+27 disable the store (& 1)
maskhi overlap   0xf800       H: bits 28-31 still store depth
zedges l in      0xf800       Z-off twin: column 1 drawn
zedges l out     0x0000       Z-off twin: column 0 not drawn
zedges r in      0xf800       Z-off twin: column 639 drawn
zedges r out     0x0000       Z-off twin: x = 640 not wrapped
zedges rspan     0xf800       Z-off twin: a span from 639.0
zyedges t in     0xf800       Z-off twin: row 0 drawn
zyedges b in     0xf800       Z-off twin: row 479 drawn
zyedges b out    0x0000       Z-off twin: row 480 not drawn
zyedges swap     0xf800       Z-off twin: reversed span drawn
zyedges s end    0xf800       Z-off twin: span end 435.0 drawn
zyedges s past   0x0000       Z-off twin: x2 + 1 not drawn
zswap s before   0x0000       Z-off twin: column 364 not drawn
zswap s tip      0xf800       Z-off twin: reversed by 1.0, swapped
zswap vert       0x07e0       Z-off twin: equal ends not swapped
zswap frac past  0x0000       Z-off twin: past the end 150.5
zswap s start    0xf800       Z-off twin: the start 399.5 -> 399
zedges2 l rev    0xf800       Z-off twin: 30 then -30 draws column 1
zedges2 r rev    0xf800       Z-off twin: 700 then 639 draws 639
zedges2 l tip    0xf800       Z-off twin: 1.0 then -1.0 draws col 1
zramp l end      0x07e0       Z-off swap body over a stored 1.5
ztedges l in     0xf800       textured Z-off twin: column 1 drawn
ztedges l out    0x0000       textured Z-off twin: column 0 not
ztedges r in     0xf800       textured Z-off twin: column 639 drawn
ztedges r out    0x0000       textured Z-off twin: 640 not wrapped
ztedges rspan    0xf800       textured Z-off twin: span from 639
ztyedges t in    0xf800       textured Z-off twin: row 0 drawn
ztyedges b in    0xf800       textured Z-off twin: row 479 drawn
ztyedges b out   0x0000       textured Z-off twin: row 480 not
ztyedges swap    0xf800       textured Z-off twin: reversed span
ztyedges s end   0xf800       textured Z-off twin: span end 435
ztyedges s past  0x0000       textured Z-off twin: x2 + 1 not drawn
ztswap s before  0x0000       textured Z-off twin: 364 not drawn
ztswap s tip     0xf800       textured Z-off twin: 400 then 399
ztswap vert      0x07e0       textured Z-off twin: u 0.5 (green)
ztedges2 l rev   0xf800       textured Z-off twin: column 1 drawn
ztedges2 r rev   0xf800       textured Z-off twin: column 639 drawn
ztedges2 l tip   0xf800       textured Z-off twin: 1 then -1, col 1
ztramp l end     0x001f       textured Z-off swap body over 1.5
half swap        0xf800       B1: a span reversed by 0.5 is swapped
half r x1        0xf800       B13: x1 = 639.5 is not past the edge
half r x2        0xf800       B14: x2 = 639.5 is not past the edge
zhalf swap       0xf800       Z-off twin: reversed by 0.5, swapped
zhalf r x1       0xf800       Z-off twin: x1 = 639.5 drawn at 639
zhalf r x2       0xf800       Z-off twin: x2 = 639.5 drawn at 639
ramp8 r end      0xf81f       B4-B7: the swap body at the right end
zramp8 r end     0xf81f       Z-off twin: 2.0 passes over 1.5
texramp8 r end   0x07e0       B8-B10: textured swap body, right end
ztramp8 r end    0x07e0       textured Z-off twin over 1.5
ramp8hi r end    0x001f       `tmpf = z1` at the right end, from above
ramp8hi l end    0x001f       the left end from above (stored 2.0)
zramp8hi r end   0x001f       Z-off twin: 3.0 fails against 4.0
zramp8hi l end   0x001f       Z-off twin: 2.0 fails against 4.0
negx n start     0xf800       N1s: the start -1.0 at its exact value
znegx n start    0xf800       Z-off twin: column 1 the third step
texnegx n start  0x07e0       B2t: the int start -1, u 0.5 at column 1
ztnegx n start   0x07e0       textured Z-off twin: u 0.5 at column 1
```

### A3. the probe's geometry and pixels (its code from `T1 = [` to `STDIN_CAP`; sessions and wants follow in the file)

```
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
```

### B. gate 14's pvr block (the staged regress/gate_arm.sh: HEAD's file plus exactly this block and two blank lines, directly before the `hpcmipsctor (#444) + #536` block; r5_20261105/gate_pvr_block.new with its header's #NNN set to #581)

```
#  ------------------------------------------------------------ pvrrenderexit (#581)
#  dev_pvr.c's renderer ended the emulator (fatal() + exit(1)) on a polygon header whose list word 1 sets bit 26 (Z-write disable).
#  Now such a polygon goes through the same depth test and rasterization as any other and only its depth store is skipped, in both
#  rasterizers, and every render clears the flag first.  The rung-3 witness (regress/artifacts/pvrrenderexit/witness_20261104/) is
#  NOT run here; this is its detector: 148 rows -- the witness's nine plus fifty render sessions whose pixels are read back
#  through the linear VRAM window (the depth-test cells of both rasterizers, two renders in one session, the x-range bound at both
#  screen edges, the equal-depth edge, repair 2's y range, span end and start, swap and bit-26 decode neighbours, repair 3's class
#  closure -- the swap's other edges and body, reversed spans across both edges, the left clause's compares at their edge, a Z-off
#  polygon at equal depth, the decode's `== 1` and wider masks, and a Z-OFF TWIN of every single-layer geometry session and of the
#  swap-body session -- repair 4's half-pixel edges of simpleline's position compares and the swap body's far end, and repair 5's
#  swap body read from above and span starts at a negative x, each with its Z-off twin).  Needs only the binary: -E dreamcast with
#  a 4-byte dummy image at 0x8c010000, about two seconds (r5_20261105/base148f/: 2.2 s).  (Corrected 2026-11-05, repair 3: this
#  said 'fifteen render sessions' -- repair 2 made sixteen -- and 'about half a second', which held for the 51-row probe; the
#  68-row probe took ~90 s, because one session's input passed the 4100-byte debugger stdin cap and waited out its timeout --
#  r3_20261105/PVR3_NOTE.md.  The probe now refuses such a session before running anything.)  It sits here rather than in
#  gate_sh_rounding.sh with the other dreamcast probes only because that file carried another session's uncommitted work when it
#  landed.  Test-variant tables: regress/artifacts/pvrrenderexit/det_20261104/table1/ (the 51-row probe), r2_20261105/table2/ (the
#  68-row probe), r3_20261105/table3/ (the 128-row probe: 129 of its 130 predictions hit; the miss was a Z-off twin left out of one
#  prediction, r3_20261105/PRETABLE_3.errata.md), r4_20261105/table4/ (the 140-row probe: all 148 of its predictions hit -- B2t's
#  "EQUIVALENT" struck by r4_20261105/PRETABLE_4.errata.md) and r5_20261105/table5/ (this probe: all 192 of PRETABLE_5.out's
#  predictions hit -- 186 variants and six legs; four undefined-behaviour variants unpredicted, thirteen non-finite forms excluded).
#  (Corrected 2026-11-05, repair 4 -- codex pass 4, F2: this said table 3 was 'prepared, not yet run'.)  Like the blocks above, it
#  runs only if none of this gate's earlier skip points fired.
PVRLOG=$LOGDIR/pvr_zwrite.log
python3 -u pvr_zwrite_probe.py "$PMAX" gate > "$PVRLOG" 2>&1 || true
if ! grep -q "PVR_ZWRITE_PROBE_DONE" "$PVRLOG"; then
    check "pvr zwrite probe completed" "no" "yes"
else
    check "pvr zwrite probe completed" "yes" "yes"
    check "pvr zwrite sentinel once" "$(grep -c '^PVR_ZWRITE_PROBE_DONE$' "$PVRLOG")" "1"
    pzres=$(sed -n 's/^PVR_ZWRITE_RESULT=//p' "$PVRLOG")
    check "pvr_zwrite rows run"     "${pzres#*/}" 148
    check "pvr_zwrite rows correct" "${pzres%/*}" "148"
    check "pvr zwrite controls" "$(grep -c '^PVR_ZWRITE_CONTROL=OK$' "$PVRLOG")" "1"
    check "pvr zwrite symptom absent" "$(grep -c '^PVR_ZWRITE_SYMPTOM=ABSENT$' "$PVRLOG")" "1"
    for v in "neg apparatus" "id session" "id r8" "zon session" "zon rendered" "zon prompt" "zoff rendered" "zoff session" "zoff prompt" "ovoff session" "ovoff overlap" "ovoff t2 only" "ovoff t1 only" "ovoff bg" "ovon overlap" "ovon t2 only" "ovon t1 only" "ovon bg" "behind session" "behind overlap" "behind t2 only" "behind t1 only" "texoff session" "texoff overlap" "texoff t1 only" "texoff t2 only" "texbeh session" "texbeh overlap" "texbeh t2 only" "texbeh t1 only" "texon overlap" "texon t2 only" "two session" "two overlap" "two t1 only" "two t2 only" "sticky session" "sticky overlap" "sticky t2 only" "edges l in" "edges l out" "edges r in" "edges r out" "edges rspan" "texedges l in" "texedges l out" "texedges r in" "texedges r out" "texedges rspan" "equal overlap" "equal t2 only" "texequal overlap" "texequal t2 only" "yedges t in" "yedges b in" "yedges b out" "yedges swap" "yedges s end" "yedges s past" "texyedges t in" "texyedges b in" "texyedges b out" "texyedges swap" "texyedges s end" "texyedges s past" "mask overlap" "mask t2 only" "mask25 overlap" "swap s before" "swap s tip" "swap vert" "swap frac past" "swap s start" "texswap s before" "texswap s tip" "texswap vert" "ramp l end" "texramp l end" "edges2 l rev" "edges2 r rev" "edges2 l tip" "edges2 x2 tip" "texedges2 l rev" "texedges2 r rev" "texedges2 l tip" "texedges2 x2 tip" "zleft tip" "texzleft tip" "zeq overlap" "texzeq overlap" "maskoff overlap" "maskhi overlap" "zedges l in" "zedges l out" "zedges r in" "zedges r out" "zedges rspan" "zyedges t in" "zyedges b in" "zyedges b out" "zyedges swap" "zyedges s end" "zyedges s past" "zswap s before" "zswap s tip" "zswap vert" "zswap frac past" "zswap s start" "zedges2 l rev" "zedges2 r rev" "zedges2 l tip" "zramp l end" "ztedges l in" "ztedges l out" "ztedges r in" "ztedges r out" "ztedges rspan" "ztyedges t in" "ztyedges b in" "ztyedges b out" "ztyedges swap" "ztyedges s end" "ztyedges s past" "ztswap s before" "ztswap s tip" "ztswap vert" "ztedges2 l rev" "ztedges2 r rev" "ztedges2 l tip" "ztramp l end" "half swap" "half r x1" "half r x2" "zhalf swap" "zhalf r x1" "zhalf r x2" "ramp8 r end" "zramp8 r end" "texramp8 r end" "ztramp8 r end" "ramp8hi r end" "ramp8hi l end" "zramp8hi r end" "zramp8hi l end" "negx n start" "znegx n start" "texnegx n start" "ztnegx n start"; do
        check "pvr zwrite row: $v" "$(count "$PVRLOG" "^$v  .*ok$")" "1"
    done
    check "pvr zwrite rows emitted" "$(( $(count "$PVRLOG" " ok$") + $(count "$PVRLOG" " FAIL$") ))" "148"
    check "pvr zwrite rows green"   "$(count "$PVRLOG" " ok$")"   "148"
    check "pvr zwrite rows red"     "$(count "$PVRLOG" " FAIL$")" "0"
fi
```

### C. test-variant table 5 (r5_20261105/table5/): VERDICT.md, the verdict of record, unedited; CHECK.txt; the leg scores

# pvrrenderexit -- test-variant TABLE 5 (repair 5: the swap body's statement-deletion closure, its right end from above, a negative span start; 148 rows), 2026-11-05 06:29:53-06:40:24 local (TABLE.log)

Driver `../table5_pvr.run.sh` (frozen copy of table5_pvr.sh), WSL scratch clone /tmp/gxpvr8 under a clone-local .MUTANT; restored,
cmp-clean against GXEMUL-SEC and against `../dev_pvr.c.fix5`, rebuilt fresh, sentinel cleared (TABLE.log).  Instrument
`probe148_frozen.py` (md5 84fe7386d80139de97ec7026bbe23e7f), cmp-identical to the in-tree probe when PRETABLE_5 was written; its md5 is
recorded in `../PRETABLE_5.out` and the driver checked it before the first leg.  Order: the frozen probe 06:28:22, PRETABLE_5.out
06:29:02, the first result (MD5.txt) 06:29:50 -- every prediction predates every result.  Scores: SCORES.txt; the driver's own
prediction check: CHECK.txt.  196 legs (190 variants and six apparatus legs), no build failed, no session timed out in any leg.

* Legs: base 148/148 CONTROL=OK SYMPTOM=ABSENT; HEAD (the pre-fix exit) 70/148 SYMPTOM=PRESENT CONTROL=OK on its predicted red set;
  null media /bin/true 9/148, an absent binary 0/148, /bin/false 1/148 -- each CONTROL=FAIL; restored 148/148.
* `TABLE5_CHECK hits=192 misses=0 not_predicted=4`: all six legs and all 186 predicted variants exactly as PRETABLE_5 recorded them.
  - 156 variants RED, each on exactly its predicted set -- among them the three FLOOR cells on their repair-5 rows and nothing else
    (DTs_z, simpleline's `tmpf = z1;` deleted: `ramp8hi r end` + twin; N1s: `negx n start` + twin; B2t: `texnegx n start` + twin),
    every one of the 24 swap-body deletion cells on its Z-on row AND its Z-off twin, and simpleline's seven depth compounds on the
    ramp8hi rows (five at the right end, `z1 += z2` and `z1 *= z2` at the left).
  - 30 variants GREEN, each predicted green and named: EQUIVALENT M17, L1s, L1t, It, H65, B1t, B13t, B14t; clause-(e) DEBT B3s, B11s,
    B12t; and the 19 compound substitutions that are debt -- texturedline's four depth members (the pass-5 ruling predicted these red
    on ramp8hi, which is untextured; green, as the candidate run had already measured) and the 15 colour and UV members.
  - Derivations PRETABLE_5 added beyond the ruling, all held: X1s also reddens the two left-end rows (COVERHI and RAMP8 both start at
    441, so nothing draws (440,60)); At reddens the negative-start textured rows (u 0.75: texel (6,0), never stored) while As and V5s
    clamp to red on `negx n start`; M13, M26, M3, M15, M6 and M7 red the Z-off ramp8hi rows, Ps only the right end; B2s reddens
    `negx n start` with N1s.
  - NOT PREDICTED (undefined behaviour, as in tables 2-4): Y2s, Y2t red their whole y-edges sessions and the Z-off twins; Y4s, Y4t red
    `b out` in both sessions -- the same sets as before.
  - EXCLUDED, not built: the thirteen compound forms that divide by an operand that is zero on a drawn swapped span (named in
    PRETABLE_5).


#### table5/CHECK.txt

```
PRED=NOTPRED Y2s_simple_ltm1 red=yedges_t_in,yedges_b_in,yedges_b_out,yedges_swap,yedges_s_end,yedges_s_past,zyedges_t_in,zyedges_b_in,zyedges_b_out,zyedges_swap,zyedges_s_end,zyedges_s_past
PRED=NOTPRED Y2t_tex_ltm1 red=texyedges_t_in,texyedges_b_in,texyedges_b_out,texyedges_swap,texyedges_s_end,texyedges_s_past,ztyedges_t_in,ztyedges_b_in,ztyedges_b_out,ztyedges_swap,ztyedges_s_end,ztyedges_s_past
PRED=NOTPRED Y4s_simple_gt red=yedges_b_out,zyedges_b_out
PRED=NOTPRED Y4t_tex_gt red=texyedges_b_out,ztyedges_b_out
TABLE5_CHECK hits=192 misses=0 not_predicted=4
```

#### table5/SCORES.txt, the legs and the verbatim reinstatement (RED lists replaced by their counts)

```
base 148/148 CONTROL=OK SYMPTOM=ABSENT DONE=1 RED=none TIMEOUT_SESSIONS=none
HEAD 70/148 CONTROL=OK SYMPTOM=PRESENT DONE=1 RED=<78 rows> TIMEOUT_SESSIONS=none
null_true 9/148 CONTROL=FAIL SYMPTOM=ABSENT DONE=1 RED=<139 rows> TIMEOUT_SESSIONS=none
null_absent 0/148 CONTROL=FAIL SYMPTOM=ABSENT DONE=1 RED=<148 rows> TIMEOUT_SESSIONS=none
null_false 1/148 CONTROL=FAIL SYMPTOM=ABSENT DONE=1 RED=<147 rows> TIMEOUT_SESSIONS=none
restored 148/148 CONTROL=OK SYMPTOM=ABSENT DONE=1 RED=none TIMEOUT_SESSIONS=none
B1_exit 70/148 CONTROL=OK SYMPTOM=PRESENT DONE=1 RED=<78 rows> TIMEOUT_SESSIONS=none
```

The 190 variants: 160 red (each line in SCORES.txt names its rows), 30 green -- B11s_ztest_q, B12t_ztest_q, B13t_right_x1_half, B14t_right_x2_half, B1t_swap_half, B3s_end_q, CBs_b1mul, CBs_b2add, CBs_tadd, CGs_g1add, CGs_g2mul, CGs_tmul, CRs_r2add, CRs_tadd, CRs_tmul, CUt_u1mul, CUt_u2add, CUt_u2sub, CVt_tmul, CVt_v1add, CVt_v2mul, CZt_z1add, CZt_z1mul, CZt_z2add, CZt_z2mul, H65_decode_and65, It_end_lt_p1, L1s_simple_lt1left, L1t_tex_lt1left, M17_reset_at_end.

### D. the filings the round owes (the landing kit's list; filed at landing as ledger rows and OUTSTANDING_BUGS.md entries)

```
F1  pvrswapdebt  (LOW, coverage debt -- ranked below live defects in dev_pvr.c, per the carrier's floor section)
    The two exchange bodies of the x1 > x2 swap (dev_pvr.c simpleline :664-668, texturedline :737-740; 27 statements) carry
    clause-(e) DEBT that the shipped 148-row detector does not catch.  Grades: adj_p6_20261105/ADJ_MYTHOS_local.md section 2, as the
    probe's EDIT SHAPES paragraph restates them with the repair-6 and pass-7 corrections (r6_20261105/RECORDS6_NOTE.md sections 3 and
    PASS 7).  Escapes:
      MEASURED green on the 148 rows (r5_20261105/table5/SCORES.txt): the 19 compound substitutions -- texturedline `z1 += z2`,
        `z1 *= z2`, `z2 += tmpf`, `z2 *= tmpf`; simpleline `tmpf += r1`, `tmpf *= r1`, `r2 += tmpf`, `tmpf *= g1`, `g1 += g2`,
        `g2 *= tmpf`, `tmpf += b1`, `b1 *= b2`, `b2 += tmpf`; texturedline `u1 *= u2`, `u2 += tmpf`, `u2 -= tmpf`, `tmpf *= v1`,
        `v1 += v2`, `v2 *= tmpf` (table 5: CZt_*, CRs_*, CGs_*, CBs_*, CUt_*, CVt_*); and the three D2-F grades SAMPLED: B3s
        (`x <= x2 + 0.25`, below the half pixel) and B11s, B12t (`vram_z <= z + 0.25`, the unit-less depth compare) --
        adj_p4_20261105 section 2 (ii) and (iii).
      DERIVED (ruling section 2, not measured): 21 right-hand-side-to-body-read-field cells (12 depth, 8 RGB, 1 UV: the probe's (c)
        list, incl. codex pass 6's (A) `u1 = u2` -> d->ysize); 8 sign survivors ((f)); `int tmpf` at :664 ((i)); (B) `int x = x1 +
        0x1p-54` (the start family's sub-resolution member, SAMPLED); the open families (d) other local or parameter (about 400
        forms; `b1 = z2`, `b1 = z1` survive), (e) constants (bands z2 in (1.5, 4.0), r2 in [251.5, 256), 0 <= g2 < 2, 0 <= b1 < 8),
        (i) insertion, (j) other right-hand-side expression changes, casts included.
    Remedy sets, filed not owed (the probe's REMEDY SETS line; pass-7 R7): DEPTH -- RAMP8 depths (3, 2, 3) under a cover at 4.0
    (texturedline too; ramp8hi is untextured) and RAMP8 depths (1, 1, 1) under COVERHI at 1.5, each read at both ends; RGB -- RAMP8
    colours (63,96,128) / (32,48,80), 0x3b10 at 448 and 0x218a at 440; UV -- uvs (0.375, 0.25) / (0.25, 0.375) with only texels
    (3,2) and (2,3) stored, read at both ends; `int tmpf` -- RAMP8 depths (1.75, 1, 1.75) under COVER8.  Both Z-states, both
    rasterizers where the set names a depth.  The ruling's own estimate: one session pair per rasterizer reds every named survivor
    (adj_p6 section 5).  Discriminator for whether it earns a round: it states a measurable consequence (each named survivor is a
    predicted red on the remedy sessions).

F2  pvruvfpundet  (LOW, an UNKNOWN to settle by measurement)
    The 8 UV field-substitution cells the ruling could not grade by derivation: `u1 = u2` -> d->xsize, d->bytes_per_pixel;
    `tmpf = v1`, `v2 = tmpf` -> d->xsize, d->ysize, d->bytes_per_pixel -- FP-sensitive on SWAP's recurrence (35 steps of fl(F/70):
    the texel mask sees 0 or 7 by the sign of the accumulated error; adj_p6 section 2(c)).  The measurement: build each, run the 148
    rows (green or red is the answer), then the amended UV session of F1.  Same batch, from adj_p6 section 4: (A) and (B), predicted
    green on the 148 rows and red on the amended UV session / codex pass 6's (B) witness session (0x07e0 against 0x5540) -- "neither
    is owed before closing"; measuring them turns two derived disclosures into measured ones.

F3  pvrdepth2bpp  (LOW, probe-design note)
    The probe's standard depth 2.0 equals d->bytes_per_pixel (2 in RGB565), so every constant-write variant that writes B into a
    depth is invisible wherever the sampled depth is 2.0 (adj_p6 section 1 (iii); the probe's PROBE-DESIGN NOTE).  A sampled value
    should equal no body-read field constant.  The DEPTH remedy set of F1 moves the depths off 2.0 where it matters; this row
    records the design rule for the next probe of this file (and asks whether other probes sample a value equal to a body-read
    field).

F4  dcstdincap  (MED, a test-apparatus hazard -- harness: witness when rowed)
    The debugger loses every byte of a `-E dreamcast` session's stdin past ~4100 (the console FIFO has read 4000 + 100 bytes by the
    first `step`, and the maple keyboard's first tick reads the rest as key presses: the probe's STDIN CAP paragraph, measured in
    r3_20261105/stdin_cap_test{,2}.out).  A session past the cap loses its `quit` and waits out its timeout; reads after the cut are
    lost.  pvr_zwrite_probe.py refuses such a session before running (STDIN_CAP 4096).  NONE of the other eleven tracked `-E
    dreamcast` scripts mentions a cap (grep for STDIN_CAP/4096/4100, 2026-11-05: 0 matches each): asic_badaddr_probe.py,
    diag_div_sweep.py, gdrom_cond_probe.py, gdrom_data_probe.py, gdrom_decline_probe.py, gdrom_default_probe.py,
    gdrom_toclen_probe.py, maple_dmaaddr_probe.py, sh4_pcic_probe.py, sh4pcic_witness.py, sh_pclock_probe.py.  The check: for each,
    the largest session's stdin size (a dry print of each session's command list, no emulator); any over 4096 is a row measuring
    less than it says.  (gdrom_default_probe.py carries another session's uncommitted edits today -- read only.)

F5  pvrmodvolbit26  (LOW, an UNKNOWN -- FOUND IN PASS 2, NOT IN THE COORDINATOR'S LIST)
    The pass-2 rulings FILEd P20/D3 (p2_20261105/ADJ_MYTHOS.md, _r2, _r3, _r4: "P20 UPHOLD FILE", "D3 FILE upheld"): what bit 26
    of list word 1 means in a MODIFIER-VOLUME header.  Fable and Opus read it as reserved (volume instruction 31-29, culling 28-27,
    26-0 reserved); grok as the depth-write bit with the volume instruction in 29-30; no local manual covers the PowerVR TA format
    (`ls _scratchpad/*.pdf`, 2026-11-05: no PVR/TA manual).  The fix is no worse than HEAD (HEAD exited; now zwrite_disabled holds
    the bit until the next type-4 header, and modifier volumes are not modelled).  Settles with a primary source for the TA
    parameter format.

F6  OWNER ITEM -- FLAG ONLY, DO NOT FILE AS A ROW
    Whether round rule D2-F (adj_p4_20261105/ADJ_MYTHOS_local.md section 2: a rasterizer's position compares pinned at the pixel AND
    the half pixel, sub-half-pixel moves SAMPLED, the depth compare unit-less; as corrected by adj_p5 R3 -- the span START is a
    truncation, not a compare -- and adj_p6 R3 -- exhausted only down to the start's double resolution) goes into the carrier
    (tools/CLAUDE.md, beside rule D2).  The owner's call.
```

### F1. the final ruling (adj_p6_20261105/ADJ_MYTHOS_local.md, whole but for the run's one-line preamble)

MYTHOSADJP6PVR

VERDICT: CLOSE-AFTER-RECORDS. Codex's 20 operand substitutions are clause-(e) DEBT by reading (i), not floor breaches: the carrier defines the operand-swap form as the GUARD's operand swapped for a body-read field (tools/CLAUDE.md:1430-1431, :1448-1451), the exchange bodies entered the bound as P4's effect and hold deletion cells only, and a right-hand side rewritten to a field is a value perturbation in data flow, the compound family's sibling that pass 5 already graded DEBT. (A) is a member of the same family; (B) is the start family's one surviving member below the double's resolution, SAMPLED under D2-F. One false record, mine (R3), upheld and reworded below. Zero floor breaches survive adjudication; the denominator is the edit-shape enumeration in section 2, which pass 7 verifies. 0 FLOOR, 29 DEBT filed with remedies, 1 record upheld, no product change, no rows owed.

Premises I checked myself: the swap bodies at dev_pvr.c:663-669 and :736-741, the guard at :658/:731, the loop starts at :683 (double x1) and :768 (int x1), the attribute initialisers at :682/:766 and the per-pixel advance at :721, the depth test and guarded store at :686-688/:771-773, the colour clamp and RGB565 pack at :707-713, the texel index `int texturex = u * texture_xsize; texturex &= 7` at :778-781, the flat-top sweep at :964-979 and :1042-1058, the vertex decode at :1335-1351; the probe's geometries at pvr_zwrite_probe.py:263-297, its sessions at :573-603, :727-755, :765-785; the carrier at tools/CLAUDE.md:1373-1472, :1545-1566, :2707-2710; CLOSURE3's application of clause (2) at the packet's :600-603; and gate_offline.sh:255-259, which refuses fast-math flags, so the build evaluates in strict IEEE binary64 (x86-64, SSE2).

1. THE 20: DEBT, by reading (i).

Why (i). Clause (2) says "for operand-swap forms, swaps drawn ONLY from fields the guarded BODY reads" (:1450-1451), and the carrier defines that form two paragraphs earlier: "the (d) mutant reroutes an EXISTING guard's repair. For a de-fatalisation: swap the guard's operand for a field the guarded BODY reads" (:1430-1431). The measured case #462 swapped the guard's operand (:1436-1438). CLOSURE3 applied it the same way: "every int operand of P1-P3 and P7 -- the fields and the constant 0 -- is swapped with each of them" (packet :600-602), that is, predicate operands. The exchange bodies entered the bound separately, as the effect of P4 (A1, packet :602-603: the attribute exchanges "are deleted one at a time"), and the shapes admitted there have been deletions: whole exchanges (repair 3), the `a2 = tmp` halves (pass 4), every statement (pass 5). An assignment's right-hand side is not a guard operand. My pass-5 phrase "swaps no operand for a body-read field" (ADJ_MYTHOS_local.md:24) listed the shape without its bound; "a rule's bounds travel with its quotation, or the quotation is a different rule" (:1551-1552). Codex read it without the bound (codex_codex_pvr_p6.txt:11).

Why not (ii). If clause (2) admitted any assignment inside the bound, it would admit `double z = z1` (:682), `int ofs = x + y * d->xsize` (:685), `dz12` (:678) and `fbofs` (:715), which the guarded body reads just as it reads the exchange body: four fields at each, the transitive data-flow chase the bound exists to refuse (:1444-1446). Nothing in the carrier distinguishes the exchange body's assignments from those except that P4 owns them, and P4's admission was for its effect nulled, not rewritten.

Why not (iii). `z2 = B` does not null the exchange half: on ramp8 (RAMP8S depths (2,1,2), :740) it writes the very value the exchange would have written, and the deletion of `z2 = tmpf` is caught there (z 1.0 under COVER8's 1.5) while `z2 = 2.0` is not. The variant is "exchange correctly whenever z1 == 2.0, else write 2.0": a value-specific bug. The body tests z only relationally against the stored depth (:686); it never tests z == 2.0 as a case, so by :1470-1472 the cell is "a value the body never tests as a case", disclosed under clause (e). The same holds for 255 at the clamp (:708) and for 0, 1, 2 under the 565 quantum (:713). Grading by shape also keeps pass 5 consistent: `z2 += tmpf` and `z2 = 2` are the same perturbation of the same value, and reopening the compound grade as "null-plus-something" would reopen a measured decision.

The honest finding under (iii) is a probe-design note, and it goes on record: the probe's standard depth 2.0 (:255, :740, :776) equals d->bytes_per_pixel, so every constant-write mutant that writes B is invisible at depth 2.0. A sampled value should equal no body-read field constant.

Codex's derivations, checked: the twelve depth survivors hold (simpleline's X, Y and W members are caught: 640 and 480 fail under COVERHI's 4.0 on ramp8hi, W's 0 or 1 passes under 1.5 on ramp and ramp8; texturedline's W members are caught on texramp/texramp8, its X, Y, B members sit above 1.5 on the only textured threshold rows, :752-755). The eight RGB survivors hold, including codex's HALF check at :51 (green 2 at column 101 is below the quantum; `g2 = B` gives 4 and is caught). I verified the remainder of the 36 RGB cells: `r1 = r2 -> W` and `-> B` are caught by `yedges swap` (127.5 and 128.5 at column 400, not 255), `g1 = g2 -> X/Y` by the same row (yellow at 400), `g1 = g2 -> W/B` by `ramp l end` (black). Codex's three detecting sets are correct as written for the 20 (the depth set, codex :38; the unsaturated RGB set, :53, values 0x3b10 and 0x218a re-derived: 63>>3=7, 96>>2=24, 128>>3=16; 32>>3=4, 48>>2=12, 80>>3=10). One amendment to the UV set in section 2(f).

2. THE EDIT-SHAPE ENUMERATION, once, for the two exchange bodies (27 statements: simpleline :664-668, five exchanges; texturedline :737-740, four; 24 assignments and three declarations). The guard `if (x1 > x2)` at :663/:736 is P4 and is closed in CLOSURE3 (operator, bound, operand copies); it is not an exchange-body edit.

(a) Statement deletion. FLOOR, closed: 24 cells, each held by the row the contract names and its Z-off twin (packet :299-308; table 5, 0 misses); three declarations undeletable (syntax_check_5.out). Denominator 24.

(b) Compound operator (`=` to `+=`, `-=`, `*=`, `/=`): 24 x 4 = 96 forms, not 80. Pass 5 screened 80 (depth 20, RGB 36, UV 24); the 16 forms on the four x statements were never screened. Derived here on SWAP row 180 (435 then 365, :263): simpleline `x1 += x2` 800, `x1 *= x2` 158775, `x2 -= tmpf` -70, `x2 /= tmpf` 0.84 draw nothing (`yedges swap` red); `x1 -= x2` 70 and `x1 /= x2` 1.19 draw column 364 (`swap s before` red); `x2 += tmpf` 800 and `x2 *= tmpf` draw column 436 (`yedges s past` red); texturedline the same on the textured rows. All 16 caught. Texturedline's int x statements also take `%=`, `&=`, `|=`, `^=` (8 forms: 435 % 365 = 70, 435 & 365 = 289, 435 | 365 = 511, 435 ^ 365 = 222, and 365 % 435 = 365 leaving a one-column span; each red on `texswap s before`, `texyedges swap` or `texyedges s end`) and `<<=`, `>>=` (4 forms, a shift by 365 or 435: undefined behaviour, not predicted). Grade: DEBT (pass-5 section 2 stands); 26 measured survivors on record; remedy the three sets.

(c) Operand to body-read field (RHS to d->xsize, d->ysize, d->zwrite_disabled, d->bytes_per_pixel): 27 x 4 = 108 cells, not codex's 84 (codex omitted UV's 24, :135). x: 24 caught (640 or 480 inverts or extends the span, 0, 1 or 2 collapses it; `yedges swap`, `swap s before`, `yedges s past` and textured twins). Depth: 24, of which 12 survive (codex :15-25). RGB: 36, of which 8 survive (codex :40-49). UV: 24, derived here from :778-781, where every field value times 8 is a multiple of 8 and masks to column or row 0: `tmpf = u1 -> F` and `u2 = tmpf -> F` (8) caught on `texramp8 r end` (column 0, red, not green); `v1 = v2 -> F` (4) caught on `texramp l end` (row 0, red, not blue); `u1 = u2 -> W`, `tmpf = v1 -> W`, `v2 = tmpf -> W` (3) caught only by the Z-off twin `ztyedges swap` (W = 1 puts u or v near 0.5 at column 400: texel column or row 3 or 4, not red); `u1 = u2 -> Y` survives by exact derivation (codex A, :67-69, checked: the eight RAMP8 steps from 480 to 0.5 are dyadic and exact); `u1 = u2 -> X`, `-> B`, `tmpf = v1 -> X/Y/B`, `v2 = tmpf -> X/Y/B` (8) are FP-sensitive on the SWAP recurrence (35 steps of fl(F/70): the mask sees 0 or 7 according to the sign of the accumulated error) and need a measurement. Grade: DEBT by section 1. Caught 24 + 12 + 28 + 15 = 79 by derivation; survivors 12 + 8 + 1 = 21; undetermined 8. Remedy: codex's depth set (RAMP8 depths (1,1,1), COVERHI at 1.5, both ends, both rasterizers, both Z-states: it also pins z2 from above at 1.5 while ramp8 pins it from below at 1.5, so no constant survives the pair), the unsaturated RGB set, and the UV set as amended in (f).

(d) Operand to another local or parameter (RHS to x1, x2, z1, z2, r1 .. b2, u1 .. v2, tmpf, tmp, y, fb_base, the texture parameters): about 400 forms. Three sub-shapes. RHS to the target itself or to its exchange partner's current value is a no-op or equals a statement deletion (`z1 = z1`; `z2 = z1` after `z1 = z2`): held by (a). RHS to a coordinate (365..520, or 1, 30, 639, 700) into z is caught by ramp8hi at either end (fails under 4.0; the optional left-end rows earn their keep), into a colour channel is caught where the channel expects 0 and survives where it expects 255 (`g1 = x1` on ramp, but `yedges swap` catches it at 127.5). RHS to a depth (1..3) or y into a colour channel quantises to 0: `b1 = z2`, `b1 = z1`, `g2 = z1` survive ramp and SWAP; HALF catches `g2 = z1` (green 4 at column 101) but not `b1 = z2`. Grade: DEBT, an open family, the same value-coincidence class, same remedy; not enumerated cell by cell.

(e) Operand to a constant (RHS to a literal): an infinite family. Any z2 in (1.5, 4.0) survives every row (ramp8 pins it from below, ramp8hi from above); any r2 in [248, 256), any g2 or b1 below the quantum survives. `!tmpf` and `!x` yield 0 or 1 and behave as the W column of (c). Grade: DEBT; codex's depth set closes the depth band for simpleline and texturedline (z2 must be above 1.5 on ramp8 and below 1.5 on the new set), the unsaturated RGB set closes the colour bands (r2 in [248,256) and [56,64) at once is empty).

(f) Sign or negation (RHS negated): 27 forms. 19 caught by derivation (a negated coordinate collapses the span; a negated depth passes under every cover; `r1 = -r2` reads 0 at column 400 of SWAP; `g1 = -g2` and `v1 = -v2` black or texel (0,7) at the left end; `tmpf = -r1`, `tmpf = -b1` and their `a2 = -tmpf` twins lose a 255 channel at 448). 8 survive by derivation: `b1 = -b2`, `tmpf = -g1`, `g2 = -tmpf` (the negated original is 0 on every swapped span: green's b, magenta's g, red's g and b); `u1 = -u2`, `tmpf = -v1`, `v2 = -tmpf` (the negated original is 0); `tmpf = -u1`, `u2 = -tmpf` (u2 = -0.5: `(int)(-4.0) & 7` is 4, the same texel as 0.5, :778-779). Grade: DEBT, the compound sibling (`x = -y` is `x = 0 - y`). Remedy: the unsaturated RGB set catches the three colour members; the UV set catches the five only if its right-end u is not symmetric under the mask: codex's (0.5, 0.25) leaves `tmpf = -u1` green. Amend to right end (0.375, 0.25), texel (3,2), left end (0.25, 0.375), texel (2,3), only those two texels stored: -0.375 masks to column 5, -0.25 to row 6; and the six UV compound survivors stay caught (`u2 -= tmpf` gives -0.125, column 7; `u1 *= u2` 0.09375, column 0; `v1 += v2` 0.625, row 5).

(g) Statement reorder (one statement moved): every move is derivably caught. Within an exchange it equals a half-deletion (held by (a)); across exchanges it writes one attribute's value into another: a coordinate into z (ramp8hi), a colour into z (0 passes under 1.5; 255 fails under 4.0), z into a colour (2 reads as 0 where 255 is expected at 448, or green 4 on HALF), u or v into z (below 1.5 on texramp8), z into u or v (column 0, red, or row 4, unstored). Declarations cannot move past their first use. No cell owed; pass 7 may sample.

(h) Swapped targets (LHS changed): each form leaves the original target unassigned, which is one of (a)'s 24 closed cells, plus a stray write that the next statement overwrites or that lands out of band (`tmpf = z1 -> z2 = z1`: tmpf keeps 448.0 and `ramp8hi r end` reds it; `x2 = tmpf -> x1 = tmpf`: a one-column span, `yedges swap`). A renamed declaration does not compile. Held by (a).

(i) Other single-site shapes found. Declaration type change: `int tmpf` at :664 SURVIVES by derivation (every exchanged x, z and colour on every swapped span is integral or truncates to the same drawn column; 400.5 to 400 draws the same columns under `x <= x2`); `int tmpf` at :738 is caught by `texramp8 r end` (u2 = (int)0.5 = 0); `float tmpf` at :664 and :738 and `double tmp` at :737 are EQUIVALENT on the probe's values (all binary32-exact) and a precision loss in general, not claimed. Grade: DEBT; remedy for `int tmpf` a fractional right-end depth across the 1.5 threshold (RAMP8 depths (1.75, 1, 1.75): the fix fails under COVER8, the truncated 1 passes), both Z-states. Statement duplication: EQUIVALENT (idempotent). Statement insertion: an open family outside DEPENDS-ON, disclosed. Guard edits: P4, closed in CLOSURE3.

Denominator for pass 7: 24 deletion cells (FLOOR, held); 108 compound forms (96 arithmetic, 12 int-only; 26 measured survivors, 13 non-finite, 4 undefined, the rest caught); 108 field-substitution cells (21 derived survivors, 8 undetermined, 79 caught); 27 sign forms (8 survivors); 27 reorder-and-target families (held); the type-change cell at :664 (1 survivor); and the three open families (other-local, constant, insertion) disclosed with the band each survives in. DEBT filed: codex's 20, (A), (B), the 8 sign survivors, `int tmpf`: 29 named cells, plus 8 FP-sensitive cells to measure.

3. R3: UPHELD, mine. The corrected wording (replacing the sentence at packet :325-327):

"The span START is a truncation toward zero, not a compare. At the -1.0 start the `negx` rows draw (:297, :776-785), `int x = x1 + c` begins at 0 for every c > 2^-54: the sum rounds to -1 + 2^-53, the next double toward zero, and truncates to 0, one column late with every attribute one step behind, a whole-pixel move that one row pins (texturedline likewise: `texnegx n start`). At c = 2^-54 the tie rounds to the even -1.0 and below it the sum is -1.0 again, so the start family is EXHAUSTED over the sign cells the early return tests only down to the start's own double resolution. Below it: c = 2^-54 is the family's one surviving member in simpleline, SAMPLED and disclosed: it changes the start only at x1 = 1 - 2^-53, the double below 1.0, which the tie rounds up (codex pass 6, B; its witness is [(0,50),(3,50),(3,80)], green, red, green at z 2.0: row 60 arrives x1 = ten additions of 0.1 = 1 - 2^-53, x2 = 3, so the fix starts at 0 and draws (85,170,0) = 0x5540 at (1,60) while the variant starts at 1 and draws vertex 1's green 0x07e0, both Z-states); every c < 2^-54 is EQUIVALENT (the sum rounds back to x1 for |x1| >= 0.5 and cannot reach an integer below it). In texturedline every c <= 2^-54 is EQUIVALENT (an int start plus 2^-54 rounds back to the int)."

Codex's witness value for (B) is wrong: it wrote "midpoint 0x7be0" (:73), which is NEGX's midpoint; this triangle's colour at column 1 is (85,170,0) = 0x5540 (dr12 = 170/2 exactly, since 3 - (1 - 2^-53) rounds to 2.0; the clipped iteration at x = 0 advances once). The mechanism holds.

4. (A) and (B): both DEBT, neither EQUIVALENT-on-this-host; both have a witness on this host and their arithmetic is deterministic here (strict binary64; gate_offline.sh:255-259 refuses the flags that would change it). (A) `u1 = u2 -> u1 = d->ysize` is a (c) cell, DEBT by section 1, surviving by exact derivation; the measurement that settles it: build it, run the 148 rows (predicted green), then the amended UV session read at (440,60) (predicted 0x0000, texel (0,3) unstored, against blue). (B) `int x = x1 + 0x1p-54` is the start family's single sub-resolution member, SAMPLED under D2-F (a move below half a pixel at a non-negative start), DEBT; the measurement: build it, run the 148 rows (predicted green), then the witness session (predicted 0x07e0 against 0x5540). Both measurements turn a derived disclosure into a measured one; neither is owed before closing.

5. VERDICT: CLOSE-AFTER-RECORDS. Zero floor breaches survive adjudication; the diff is delivered (148/148, table 5 192 hits); the zero carries its denominator (section 2). Records owed, no rows, no product: (1) the R3 sentence replaced by section 3's wording, with codex's (B) and its corrected want on record; (2) the contract's COMPOUND ASSIGNMENTS paragraph (packet :339-352) extended to the full enumeration of section 2, with each shape's grade, its survivors by name (codex's 20, A, B, the 8 sign survivors, `int tmpf` at :664, the 8 FP-sensitive UV cells as undetermined), the 16 unscreened x compounds and the 24 UV field cells added to the counts, the value-coincidence note (depth 2.0 equals bytes_per_pixel), and the three remedy sets with the UV set amended to (0.375, 0.25)/(0.25, 0.375); (3) codex's denominator corrected on record: 108 swept omitted the 24 UV field cells, and its (B) want value. Pass 7 verifies section 2 against the code and the rows; if it chooses to measure, the three remedy sets in one session pair per rasterizer would red every named survivor at once, which is the one cheap delta still on the table, but it is filed, not owed.

MYTHOSADJP6PVR: 0 FLOOR 29 DEBT 1 RECORDS UPHELD VERDICT:CLOSE-AFTER-RECORDS

### F2. the records chain after the ruling: r6_20261105/RECORDS6_NOTE.md (repair 6 and the pass-7 fixes, each with the text it replaced), then the disposition of the reading that closed it (recp7_20261105)

# pvrrenderexit repair 6 (2026-11-05) -- records only, after the pass-6 ruling

Ruling: `../adj_p6_20261105/ADJ_MYTHOS_local.md` (`0 FLOOR 29 DEBT 1 RECORDS UPHELD VERDICT:CLOSE-AFTER-RECORDS`), on
`../p6_20261105/codex_codex_pvr_p6.txt`.  Text only: no row, no table, no build (no printed string changed), dev_pvr.c and gate_arm.sh
untouched.  Backup first: `pvr_zwrite_probe.py.pre_r6` (md5 0fa83b8191ee01c03ec64545bb569cbe, the repair-5 probe).

## 1. R3 (the pass-6 ruling's section 3), in the probe's D2-F paragraph

The start sentence is replaced by the ruling's wording; the old one is quoted in a dated note beside it, and the repair-5 note's
"one row pins every `int x = x1 + c`, 0 < c <= 1" gains "[repair 6: for 2^-54 < c <= 1 only]".  Arithmetic re-done in binary64
(`r3_arith.py`, output `r3_arith.out`): -1 + 2^-54 is -1.0 (tie to even); just above 2^-54 the sum is -1 + 2^-53 and truncates to 0;
codex's (B) witness row 60 starts at 0.9999999999999999 = 1 - 2^-53 with x2 - x1 = 2.0, so the fix puts (85, 170, 0) = **0x5540** at
(1,60) and `x1 + 2^-54` starts at 1 with vertex 1's green 0x07e0; among the doubles just below 1, 2, 3, 4 only 1 - 2^-53 moves.
**Four precision fixes to the ruling's sentence, each checked:** (i) "for every c > 2^-54" dropped the family's upper bound
(`int(-1 + 2.0)` is 1, not 0) -- written "c in (2^-54, 1]"; (ii) "the sum rounds to -1 + 2^-53" holds for c just above 2^-54 only --
"or nearer zero" added; (iii) texturedline's "an int start plus 2^-54 rounds back to the int" is not true at 0 (0 + 2^-54 is exact) --
"or at 0 truncates to it" added; (iv) its probe line numbers ":297, :776-785" (same-file, shifting with every edit) became the construct
names NEGX and the negx sessions.  The witness is marked DERIVED, not measured (the ruling's section 4: the measurement is not owed).

## 2. Codex pass 6, corrected on record

* **Denominator.**  "108 CELLS SWEPT" was 24 statement deletions plus 84 field substitutions (24 x, 24 depth, 36 RGB).  It omitted UV's
  24 field cells: the field-substitution shape has **108** cells (the ruling's section 2(c)), so the sweep codex described is 132 cells,
  and the shapes named here are the ruling's nine in section 2 [PASS 7: plus (j); this said "the full enumeration"].
* **(B)'s want.**  Codex wrote "midpoint 0x7be0" -- NEGX's midpoint.  This triangle's colour at column 1 is **0x5540** (section 1 above).

## 3. The enumeration (the probe's EDIT SHAPES paragraph, replacing repair 5's COMPOUND ASSIGNMENTS paragraph)

One entry per shape, (a) to (i), each with its grade, count, survivors by name and remedy set, citing the ruling's section 2 for the
derivation; plus the three remedy sets (the UV set amended to (0.375, 0.25) / (0.25, 0.375)) and the value-coincidence note (depth 2.0 =
d->bytes_per_pixel).  Counts checked: (b) 26 + 13 + 41 + 16 + 8 + 4 = 108; (c) 79 + 21 + 8 = 108, the 21 named = 12 depth + 8 RGB + 1 UV,
the 8 undetermined named; (f) 19 + 8 = 27.  Measured statements are marked MEASURED (table 5: the 24 deletion cells, the 7 depth
compounds red on ramp8hi, the 19 compound survivors); everything else stays DERIVED.  The amended UV values were checked: -0.375 masks to
column 5, -0.25 to row 6; `u2 -= tmpf` gives -0.125 (column 7), `u1 *= u2` 0.09375 (column 0), `v1 += v2` 0.625 (row 5).

**Two ruling claims that do not hold, corrected in the probe (DERIVED):**
* (e) "any r2 in [248, 256), any g2 or b1 below the quantum survives": `half swap`'s row 103 is half a pixel wide (100.75..101.25) and
  its loop starts at 100, so column 101 gets twice the endpoint's change -- r = 2 r2 - 255 (248 reads 241: 30, not 31, in RGB565) and
  g = 2 g2 (2 reads 4).  r2 in [248, 251.5) and g2 in [2, 4) are caught; written "r2 in [251.5, 256), g2 below 2, b1 below 8".  (The
  ruling's own section 1 and codex both note the g2 = 2 case at column 101; section 2(e) did not carry it.)
* The tally "codex's 20, (A), (B), the 8 sign survivors, `int tmpf`: 29 named cells" sums to **31** (20 + 1 + 1 + 8 + 1).  The probe
  names each survivor per shape and writes no total.

## 4. Siblings

The universal "every 0 < c <= 1 ... one row pins the whole family" also stood in `../r4_20261105/PVR4_NOTE.md` and, as "the start family
is not SAMPLED below half a pixel", in `../r4_20261105/PRETABLE_4.errata.md`: each gains a dated repair-6 bracket pointing here.  The
gate block (`../r5_20261105/gate_pvr_block.new`) repeats none of the corrected claims: no patch, and its row count stays 148.

## 5. Proof that the edit is text only -- `AST_PROOF.txt`

The shipped probe against table 5's frozen instrument (`../r5_20261105/table5/probe148_frozen.py`): **AST without the docstring SAME**
(153280 chars each), code tokens SAME (7966 each); control, against the 140-row probe: DIFFERENT.  So table 5's 192 hits stand for the
shipped probe.  The whole edit is `probe_r6.diff` (docstring lines only).  No build was needed; as a sanity check the shipped probe ran
once on build/gxemul, read-only, clearance recorded: 148/148 (`base148r6/`).

## 6. Denominator for pass 7 (the ruling's, with the tally corrected)

24 deletion cells (FLOOR, held); 108 compound forms (96 arithmetic, 12 int-only: 26 measured survivors of 140 rows, 19 of 148, 13
non-finite, 4 undefined, the rest caught); 108 field-substitution cells (21 derived survivors, 8 undetermined, 79 caught); 27 sign forms
(8 survivors); reorder and target changes held by (a); the type change at :664 (1 survivor); three open families [PASS 7: four, with (j)] (other local,
constant, insertion) disclosed with their bands.  Named DEBT cells: 31, plus 8 FP-sensitive cells to measure.

## PASS 7 (2026-11-05) -- seven record items, text only

Codex pass 7 (`../p7_20261105/codex_codex_pvr_p7.txt`, section 3): zero floor breaches over 272 cells; seven items in the
enumeration's prose.  Each was deleted or narrowed in the probe's docstring.  Backup `pvr_zwrite_probe.py.pre_p7rec`, diff
`probe_p7rec.diff` (docstring lines only), proof `AST_PROOF_p7.txt`: the AST without the docstring is the SAME as table 5's frozen
instrument (the control, the 140-row probe, DIFFERENT).
* R1, one line added: "(j) other right-hand-side expression changes, casts included -- an open family, DEBT, not enumerated"; (i)'s
  label "other single-site shapes" narrowed to "type change, duplication, insertion, guard"; "the three sets" became "the sets below";
  this note's "the full enumeration" narrowed above.
* R2, mechanism deleted: "(the sum rounds back to x1 for |x1| >= 0.5 and cannot reach an integer below it)" became "(DERIVED: the sum
  truncates to the same integer as x1)".  At x1 = -0.5, -0.5 + 3 * 2^-56 is -0.49999999999999994 and still truncates to 0
  (`p7_checks.out`, which also samples 20,029 values of x1).
* R3, narrowed: "b1 below 8" became "0 <= b1 < 8" (b1 = -8 reads 0xf801 at (101,103), `p7_checks.out`); "g2 below 2", the same
  unbounded form, became "0 <= g2 < 2".
* R4, deleted: "`!tmpf` and `!x` act as the W column of (c)".
* R5, universal deleted: "every move caught" became "texturedline `x2 = tmp` moved after its z exchange is EQUIVALENT".
* R6, rewritten: "a duplicated statement EQUIVALENT" became "adjacent duplication of an assignment is EQUIVALENT; duplicating a
  declaration does not compile" (`dup_check.out`: `redefinition of 'tmpf'`; the duplicated assignment compiles).
* R7, rewritten: the depth remedy keeps RAMP8 depths (3, 2, 3) under a cover at 4.0 beside (1, 1, 1) under COVERHI at 1.5, both
  rasterizers and Z-states; the all-one set alone leaves texturedline `z1 *= z2` and `z2 *= tmpf` at 1.0.
No row, table, build, git or gate_arm.sh.  The gate block repeats none of these claims.


#### recp7_20261105/DISPOSITION.md (the reading itself, item by item: recp7_20261105/codex_codex_pvr_recp7.txt)

# pvrrenderexit -- reading of the seven pass-7 record fixes (main loop, 2026-11-05)

GPT-6 Astra (codex, `ultra`) ANSWERED (codex_codex_pvr_recp7.txt; `CODEXRECP7PVR: 7 ACCEPTED 0 TO FIX VERDICT:ACCEPT`).  All seven
are TRUE, including the implementer's unrequested 0 <= g2 < 2 bound.  No new false claim was introduced.
THE pvr REVIEW CHAINS ARE CLOSED.  Floor: pass 7, 0 breaches over 272 cells.  Records: this reading.  Under the delete-or-narrow
discipline the records closed in ONE reading, against three rewrite rounds for memc earlier the same day.  pvr goes to its REGRESS
stage and landing kit.

### F3. the passes: every verdict line from pass 2 on, then pass 7's disposition

(each answer's last verdict line, read from the file; the dispositions p3..p7_20261105/DISPOSITION.md carry the main loop's handling and the seat ledger -- glm-5.3 and grok-4.7 walled from pass 3 on, Gemini 4 Argon down from pass 5)

```
p2 ruling (4th run)  p2_20261105/ADJ_MYTHOS_r4.md               MYTHOSADJP2PVR: 26 RULINGS 3 CHANGES 3 FILED VERDICT:APPLY-WITH-CHANGES
p3 codex             p3_20261105/codex_codex_pvr_p3.txt         CODEXP3PVR: 84 CELLS SWEPT 15 BREACHES 5 FALSE RECORDS VERDICT:REPAIR
p3 Gemini            p3_20261105/gemini_p3_pvr.md               GWEBP3PVR: 4 ATTACKS 2 BROKEN 2 HOLDS 0 UNSETTLED DRAFTABLE:NO
p3 Gemini r2         p3_20261105/gemini_p3_pvr_r2.md            GWEBP3PVRR: 4 ATTACKS 2 BROKEN 2 HOLDS 0 UNSETTLED DRAFTABLE:NO
p4 codex             p4_20261105/codex_codex_pvr_p4.txt         CODEXP4PVR: 177 CELLS SWEPT 14 BREACHES 8 FALSE RECORDS VERDICT:REPAIR
p4 Gemini            p4_20261105/gemini_p4_pvr.md               GWEBP4PVR: 10 ATTACKS 0 BROKEN 10 HOLDS 0 UNSETTLED DRAFTABLE:YES
p4 ruling            adj_p4_20261105/ADJ_MYTHOS_local.md        MYTHOSADJP4PVR: 11 FLOOR 3 DEBT 8 RECORDS UPHELD VERDICT:REPAIR-4
p5 codex             p5_20261105/codex_codex_pvr_p5.txt         CODEXP5PVR: 181 CELLS SWEPT 27 BREACHES 2 FALSE RECORDS VERDICT:REPAIR
p5 ruling            adj_p5_20261105/ADJ_MYTHOS_local.md        MYTHOSADJP5PVR: 3 FLOOR 26 DEBT 2 RECORDS UPHELD VERDICT:REPAIR-5
p6 codex             p6_20261105/codex_codex_pvr_p6.txt         CODEXP6PVR: 108 CELLS SWEPT 20 BREACHES 1 FALSE RECORDS VERDICT:REPAIR
p6 ruling            adj_p6_20261105/ADJ_MYTHOS_local.md        MYTHOSADJP6PVR: 0 FLOOR 29 DEBT 1 RECORDS UPHELD VERDICT:CLOSE-AFTER-RECORDS
p7 codex             p7_20261105/codex_codex_pvr_p7.txt         CODEXP7PVR: 272 CELLS SWEPT 0 BREACHES 7 FALSE RECORDS VERDICT:REPAIR
recp7 codex          recp7_20261105/codex_codex_pvr_recp7.txt   CODEXRECP7PVR: 7 ACCEPTED 0 TO FIX VERDICT:ACCEPT
```

#### p7_20261105/DISPOSITION.md (whole)

# pvrrenderexit PASS 7 -- disposition (main loop, 2026-11-05)

Seats: GPT-6 Astra (codex, `ultra`) ANSWERED (codex_codex_pvr_p7.txt; `CODEXP7PVR: 272 CELLS SWEPT 0 BREACHES 7 FALSE RECORDS
VERDICT:REPAIR`).  Gemini 4 Argon: SEAT FAILURE, because the web route is down.  glm-5.3 and grok-4.7 are walled.

THE FLOOR CHAIN CLOSES HERE.  This is a VALID pass: the enumeration and records were delivered, the seat misses are named, and the
zero carries its denominator.  That denominator is 272 finite exchange-body forms: 24 deletions, 108 compounds, 108 field
substitutions, 27 negations and 5 type changes.  The 14 D2-F feature and Z-state observations were checked separately.  No
FLOOR-graded cell is green.  The guard-operand reading of clause (2) is upheld.
SEVEN RECORD ITEMS, all in the enumeration's explanatory prose; none changes a grade at the floor:
* R1: a missing open family, right-hand-side expression and cast changes.
* R2: a false rounding mechanism at x1 = -0.5; the equivalence survives.
* R3: an unrestricted blue band; b1 = -8 is caught.
* R4: `!tmpf` is not the W substitution.
* R5: "every move caught" is false; independent exchanges permit equivalent moves.
* R6: duplicating a declaration does not compile.
* R7: the remedy sets must keep the (3,2,3)-under-4 depth set beside the all-one set.
They went to the implementer (Opus 5.5, resumed), told to DELETE or NARROW rather than explain.  The same lesson came out of memc
and qhs today.  A narrow reading of the fixes follows.  Then come the REGRESS stage and the landing.

### G. the fix: src/devices/dev_pvr.c, HEAD against the staged file

```
(HEAD cbd916d1's file against the STAGED file: the working copy, md5 481755b4f10fc67a8749884a90594ff9 -- the source table 5 measured -- with its six `#NNN` comment tags set to #581; STAGED_DIFFS_pvr.md proves the two differ in comments only.  The four build trees hold the unfilled working copy: TREES_pvr.txt; the landing owes them the staged file.)
--- a/src/devices/dev_pvr.c (HEAD)
+++ b/src/devices/dev_pvr.c (staged)
@@ -142,10 +142,14 @@
     size_t            n_ta_commands;
 
     /*  Video RAM and Z information:  */
     uint8_t            *vram;
     double            *vram_z;
+    int            zwrite_disabled;    /*  #581: ISP/TSP word 1 bit 26 of the
+                                polygon being rendered.  When set, the
+                                rasterizers skip their vram_z stores.
+                                Cleared at every pvr_render entry.  */
 
     /*  DMA registers:  */
     uint32_t        dma_reg[N_PVR_DMA_REGS];
     uint32_t        dma_more_reg[N_PVR_DMA_REGS];
 };
@@ -678,11 +682,12 @@
     double z = z1, r = r1, g = g1, b = b1;
     for (int x = x1; x <= x2; ++x) {
         if (x > 0 && x < d->xsize) {
             int ofs = x + y * d->xsize;
             if (d->vram_z[ofs] <= z) {
-                d->vram_z[ofs] = z;
+                if (!d->zwrite_disabled)    /*  #581: depth test kept, store skipped  */
+                    d->vram_z[ofs] = z;
 
                 // z = 1/w
                 // int v = z * scale_factor;
                 // printf("z=%f v=%i\n", z, v);
                 // if (v < 0) v = 0;
@@ -762,11 +767,12 @@
 
     for (int x = x1; x <= x2; ++x) {
         if (x > 0 && x < d->xsize) {
             int ofs = x + y * d->xsize;
             if (d->vram_z[ofs] <= z) {
-                d->vram_z[ofs] = z;
+                if (!d->zwrite_disabled)    /*  #581: depth test kept, store skipped  */
+                    d->vram_z[ofs] = z;
 
                 int fbofs = fb_base + ofs * d->bytes_per_pixel;
 
                 // Get color from texture:
                 int texturex = u * texture_xsize;
@@ -1126,10 +1132,14 @@
     double wf_z[4] = { 0 }, wf_u[4] = { 0 }, wf_v[4] = { 0 };
     int wf_r[4], wf_g[4], wf_b[4];
 
     double baseRed = 0.0, baseGreen = 0.0, baseBlue = 0.0;
 
+    d->zwrite_disabled = 0;    /*  #581: per render.  A type-4 header in this
+                    call assigns it; a list with no header must
+                    not inherit the previous render's value.  */
+
     debug("[ pvr_render: rendering to FB offset 0x%x, "
         "%i Tile Accelerator commands ]\n", fb_base, d->n_ta_commands);
 
     /*
      *  Clear all pixels first.
@@ -1238,14 +1248,17 @@
                 fatal("shading1 %s, ", shading1 ? "TRUE" : "false");
                 fatal("uv_format1 %s, ", uv_format1 ? "TRUE" : "false");
                 fatal("dcalcexact %s\n", dcalcexact ? "TRUE" : "false");
             }
 
-            if (!zwrite) {
-                fatal("pvr: no zwrite? not implemented yet.\n");
-                exit(1);
-            }
+            /*  #581: ISP/TSP instruction word 1 bit 26 is "Z-write disable".
+                A polygon with the bit set goes through the same depth test
+                and rasterization as any other polygon, but its depth values
+                are not stored.  Both rasterizers check d->zwrite_disabled
+                at their vram_z stores.  Before #581 this bit ended the
+                emulator with fatal() + exit(1).  */
+            d->zwrite_disabled = !zwrite;
 
             // For now, trust texture and ignore texture1.
             // if (texture != texture1) {
             //    fatal("pvr: texture != texture1. what to do?\n");
             //    exit(1);
```

### H1. gate 14's pvr block replayed over table 5's banked logs and synthetic logs (dryrun_pvr.py: the probe call replaced, marked, by a copy of each log; HEAD's regress/lib.sh sourced)

```
Gate 14's pvrrenderexit block, as staged, replayed over table 5's 196 banked logs and 18 synthetic logs, the probe call replaced by each log (`regress/artifacts/pvrrenderexit/landing_20261105/DRYRUN_pvr.out`): base (the fix) green; HEAD red (82 of 157 checks); /bin/true red (143 of 157 checks); an absent binary red (152 of 157 checks); /bin/false red (151 of 157 checks); restored green; the 30 variants the probe scored green green (B11s_ztest_q, B12t_ztest_q, B13t_right_x1_half, B14t_right_x2_half, B1t_swap_half, B3s_end_q, CBs_b1mul, CBs_b2add, CBs_tadd, CGs_g1add, CGs_g2mul, CGs_tmul, CRs_r2add, CRs_tadd, CRs_tmul, CUt_u1mul, CUt_u2add, CUt_u2sub, CVt_tmul, CVt_v1add, CVt_v2mul, CZt_z1add, CZt_z1mul, CZt_z2add, CZt_z2mul, H65_decode_and65, It_end_lt_p1, L1s_simple_lt1left, L1t_tex_lt1left, M17_reset_at_end); the 160 it scored red, red; on every banked log the failing per-row pins are exactly the rows the log's PVR_ZWRITE_RED names; the 17 synthetic logs that should red (a dead probe; the sentinel missing, doubled or not alone; protocol keys missing, doubled or changed; a row lost, added, doubled or flipped; every row removed) each red on the pins they target, and a line after the sentinel stays green (no pin reads the sentinel's position); every one of the block's 157 checks failed on at least one leg.

(the six legs, the synthetic legs and the pin coverage; every banked variant's line: regress/artifacts/pvrrenderexit/landing_20261105/DRYRUN_pvr.out)
--- base                       148/148 CONTROL=OK SYMPTOM=ABSENT        want green got green; failing row pins == the log's RED list (0)
--- HEAD                       70/148 CONTROL=OK SYMPTOM=PRESENT        want red   got red (82 of 157 checks); failing row pins == the log's RED list (78)
      pvr_zwrite rows correct
      pvr zwrite symptom absent
      pvr zwrite rows green
      pvr zwrite rows red
--- null_true                  9/148 CONTROL=FAIL SYMPTOM=ABSENT        want red   got red (143 of 157 checks); failing row pins == the log's RED list (139)
      pvr_zwrite rows correct
      pvr zwrite controls
      pvr zwrite rows green
      pvr zwrite rows red
--- null_absent                0/148 CONTROL=FAIL SYMPTOM=ABSENT        want red   got red (152 of 157 checks); failing row pins == the log's RED list (148)
      pvr_zwrite rows correct
      pvr zwrite controls
      pvr zwrite rows green
      pvr zwrite rows red
--- null_false                 1/148 CONTROL=FAIL SYMPTOM=ABSENT        want red   got red (151 of 157 checks); failing row pins == the log's RED list (147)
      pvr_zwrite rows correct
      pvr zwrite controls
      pvr zwrite rows green
      pvr zwrite rows red
--- restored                   148/148 CONTROL=OK SYMPTOM=ABSENT        want green got green; failing row pins == the log's RED list (0)
--- X1 dead probe (empty log)                          want red on pvr zwrite probe completed; got red (1 of 1 checks)
      pvr zwrite probe completed
--- X2 sentinel missing                                want red on pvr zwrite probe completed; got red (1 of 1 checks)
      pvr zwrite probe completed
--- X3 sentinel printed twice                          want red on pvr zwrite sentinel once; got red (1 of 157 checks)
      pvr zwrite sentinel once
--- X4 sentinel not alone on its line                  want red on pvr zwrite sentinel once; got red (1 of 157 checks)
      pvr zwrite sentinel once
--- X5 RESULT line missing                             want red on pvr_zwrite rows run, pvr_zwrite rows correct; got red (2 of 157 checks)
      pvr_zwrite rows run
      pvr_zwrite rows correct
--- X6 CONTROL line missing                            want red on pvr zwrite controls; got red (1 of 157 checks)
      pvr zwrite controls
--- X7 SYMPTOM line missing                            want red on pvr zwrite symptom absent; got red (1 of 157 checks)
      pvr zwrite symptom absent
--- X8 every protocol key printed twice                want red on pvr_zwrite rows run, pvr_zwrite rows correct, pvr zwrite controls, pvr zwrite symptom absent; got red (4 of 157 checks)
      pvr_zwrite rows run
      pvr_zwrite rows correct
      pvr zwrite controls
      pvr zwrite symptom absent
--- X9 one row lost (ztnegx n start)                   want red on pvr zwrite row: ztnegx n start, pvr zwrite rows emitted, pvr zwrite rows green; got red (3 of 157 checks)
      pvr zwrite row: ztnegx n start
      pvr zwrite rows emitted
      pvr zwrite rows green
--- X10 one row added                                  want red on pvr zwrite rows emitted, pvr zwrite rows green; got red (2 of 157 checks)
      pvr zwrite rows emitted
      pvr zwrite rows green
--- X11 one row printed twice (ztnegx n start)         want red on pvr zwrite row: ztnegx n start, pvr zwrite rows emitted, pvr zwrite rows green; got red (3 of 157 checks)
      pvr zwrite row: ztnegx n start
      pvr zwrite rows emitted
      pvr zwrite rows green
--- X12 one row FAIL, protocol unchanged (ztnegx n start) want red on pvr zwrite row: ztnegx n start, pvr zwrite rows green, pvr zwrite rows red; got red (3 of 157 checks)
      pvr zwrite row: ztnegx n start
      pvr zwrite rows green
      pvr zwrite rows red
--- X13 every row line removed                         want red on pvr zwrite rows emitted, pvr zwrite rows green; got red (150 of 157 checks)
      pvr zwrite row: neg apparatus
      pvr zwrite row: id session
      pvr zwrite row: id r8
      pvr zwrite row: zon session
--- X14 RESULT says 147/148                            want red on pvr_zwrite rows correct; got red (1 of 157 checks)
      pvr_zwrite rows correct
--- X15 RESULT says 149/149 (a probe that grew)        want red on pvr_zwrite rows run, pvr_zwrite rows correct; got red (2 of 157 checks)
      pvr_zwrite rows run
      pvr_zwrite rows correct
--- X16 CONTROL=FAIL, rows unchanged                   want red on pvr zwrite controls; got red (1 of 157 checks)
      pvr zwrite controls
--- X17 SYMPTOM=PRESENT, rows unchanged                want red on pvr zwrite symptom absent; got red (1 of 157 checks)
      pvr zwrite symptom absent
--- X18 a line after the sentinel (informational)      want green; got green
PIN COVERAGE (157 checks the base leg runs; legs on which each failed, over 196 banked + 18 synthetic legs):
    2  pvr zwrite probe completed
    2  pvr zwrite sentinel once
    3  pvr_zwrite rows run
  168  pvr_zwrite rows correct
    6  pvr zwrite controls
    5  pvr zwrite symptom absent
    4  pvr zwrite rows emitted
  169  pvr zwrite rows green
  165  pvr zwrite rows red
  the 148 per-row pins: each failed on 3 to 28 legs; X13 (every row line removed) failed 148 of them
CHECKS THAT FAILED ON NO LEG: none
DRYRUN_PVR_OK
```

### H2. the rung-3 witness (witness_20261104/WITNESS.md, measured 2026-11-04 before any edit) and the last in-situ gate run

# pvrrenderexit -- the rung-3 witness, measured 2026-11-04 01:26 (before any edit)

[the hold note and the instrument paragraph are elided; the file has them]

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


**The last in-situ gate-14 run** (`wiring_20261105/`, `gate14.time`: start=2026-11-05T01:20:46Z; gate rc=0; end=2026-11-05T03:37:54Z; total=1609 memc=84 pvr=60 fail=0 skip=0) ran the 51-row block on the 51-row probe: `gate14_pvr_zwrite.log` ends PVR_ZWRITE_RESULT=51/51, CONTROL=OK, SYMPTOM=ABSENT.  The 148-row block has never run in situ; block H1 replays it over banked logs, and the in-situ run is owed at landing.
