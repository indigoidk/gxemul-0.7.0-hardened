# pvrrenderexit repair 3 -- THE CLASS CLOSURE (2026-11-05)

Pass 2 and pass 3 found breaches of one class -- cells of the predicates that dominate the guarded depth store, left empty -- so this
repair owes the class closure in one diff (carrier: "when two consecutive passes find breaches of one class ... enumerate the full
space from the function's own inputs, close every cell in ONE diff, and write into the CONTRACT which cells are covered and which are
deliberately not").  This file is that enumeration.  The probe header's REPAIR 3 CONTRACT is its summary.

## 1. What is enumerated, and by which rule

The fix guards one store per rasterizer: `if (!d->zwrite_disabled) d->vram_z[ofs] = z;` (simpleline, texturedline), fed by the case-4
decode `zwrite = ! ((list[1] >> 26) & 1); d->zwrite_disabled = !zwrite;`.  The predicates that DOMINATE each store, walked up to the
function boundary (the DEPENDS-ON bound, clause 1), are, per rasterizer:

| id | predicate (simpleline 654-723 / texturedline 725-904) | the store is reached when |
|---|---|---|
| P1 | `y < 0`, `y >= d->ysize` (early return) | 0 <= y <= 479 |
| P2 | `(x1 < 0 && x2 < 0)` (early return) | not both ends left of column 0 |
| P3 | `(x1 >= d->xsize && x2 >= d->xsize)` (early return) | not both ends at or right of 640 |
| P4 | `if (x1 > x2) { exchange x, z, r, g, b }` (texturedline: x, z, u, v) | always; it orders the span and its attributes |
| P5 | `int x = x1` (the loop's start) | x from (int)x1 |
| P6 | `x <= x2` (the loop's end) | through floor(x2) (texturedline: x2, an int) |
| P7 | `x > 0 && x < d->xsize` (inner bound) | columns 1..639 |
| P8 | `d->vram_z[ofs] <= z` (depth test), crossed with the guard `!d->zwrite_disabled` | stored depth not above the incoming one |
| P9 | the case-4 decode (shared by both rasterizers) | header word 1 bit 26 set => Z-write disabled |

The rules applied, each as the brief stated it:
* **each compare's two edges** (rule D2: a region is pinned at its edge, by the LEAST-observable NON-EQUIVALENT move of its bound; at
  most two rows per compare);
* **operand swaps drawn only from fields the body reads**: the int fields the rasterizer body reads are d->xsize, d->ysize,
  d->zwrite_disabled and d->bytes_per_pixel (2); every int operand of P1-P3 and P7 -- the fields and the constant 0 -- is swapped
  with each of them; P4's endpoints are copied for each other (codex's D, E); and the swap body's attribute exchanges, which the body
  reads after the swap (both Gemini readings, via the coordinator), are deleted one at a time;
* **the joint cells the body itself distinguishes**: P8's relation {<, ==, >} crossed with Z-write {on, off};
* **the decode's single-edit forms**: operator, mask widened by any single bit k, shift moved, operand word changed.

## 2. The denominator: 173 INPUT CELLS (deriver: `closure_cells.py`, output `closure_cells.out`)

Two units, kept apart because a count that names neither cannot be checked:
* **INPUT CELLS** -- codex's unit: a region of a predicate's inputs that a row can place a span or a header in.  This is the
  denominator, and `closure_cells.py` lists every one with its disposition and row.
* **EDIT FORMS** -- the edits that reach those cells.  They are tabulated by family in section 4 (every operator, every operand swap,
  every bound move named there) and section 8 (the multi-token Z-off family); test-variant table 3 builds 128 of them (62 from table
  2, 66 new), each with an exact prediction or NOT PREDICTED (PRETABLE_3.out).

The 173 input cells:
* **codex's 84** (pass 3): per rasterizer 33 -- P1 4 (rows -1, 0, 479, 480), P2 4 truth pairs, P3 4 truth pairs, P4 5, P5 3, P6 3, P7
  4, P8 6 -- plus simpleline's two fractional span-end cells, plus 16 decode patterns of word 1 bits 25-28.  Its P1-P7 cells are the
  Z-ON halves (every geometry row before the twins drew a Z-on polygon); P8 already crosses the depth relation with Z-write;
* **added, 18**: A1 the swap body -- a reversed span whose ends differ in z, r, g or b (simpleline) or in z, u or v (texturedline), 7;
  A2 the right clause's two compares at their edge, per rasterizer, 4; A3 the left clause's two compares at their edge, per rasterizer,
  4; A7 a Z-on header with word 1 bit 29, 30 or 31 set, 3.  (A5, A6 and A8 are edit forms on cells already counted.)
* **the Z-off twins, 71** (section 8; the coordinator's ruling on the 09-04 floor): every P1-P7 cell, the fractional pair, A1, A2 and A3
  crossed with Z-write OFF.  (The 91-row version's "A4" -- a Z-off polygon at row 0 and at column 1 -- is two of these and is no longer
  counted on its own.)

**Tally (closure_cells.out): OLD 50 (an existing row), NEW 91 (a repair-3 row), EQUIV 12, DOM 6, UB 4, NN 10.**  OLD + NEW = 141 cells
rowed; EQUIV and DOM carry their derivations below (a twin keeps its Z-on cell's reason: Z-write changes only the depth store, never
which pixels are drawn); UB = row -1 in both rasterizers, Z-on and Z-off, whose only reaching edits read outside vram_z; NN = ten
decode patterns no single edit of the decode separates from the six rowed headers.  No input cell that an edit reaches on a defined
path is left without a row or a named clause-(e) disclosure.  (Corrected 2026-11-05, repair 4 -- codex pass 4, F1, as the pass-4
ruling scoped it, ../adj_p4_20261105/ADJ_MYTHOS_local.md section 3: this said "...left without a row", which was false for eleven
single edits pass 4 found -- B1, B2, B4-B10, B13, B14, measured surviving the 128-row probe in ../r4_20261105/meas_B/ -- and the
cell list was short by eight half-pixel cells, four simpleline position compares crossed with Z-write.  Repair 4 rows all eleven,
counts 181 cells, and discloses the moves below half a pixel as SAMPLED (rule D2-F): ../r4_20261105/PVR4_NOTE.md.)

## 3. codex's 84, cell by cell (s = simpleline, t = texturedline; each row exists in both rasterizers unless marked)

| cell | s | t | row / disposition |
|---|---|---|---|
| P1 row -1 | x | x | NOT COVERED: `y < -1` (Y2) admits row -1, whose depth read is vram_z[x - 640] -- undefined behaviour (table 2: Y2 measured red, NOT PREDICTED) |
| P1 row 0 | x | x | `yedges t in` / `texyedges t in` (Y1 `y < 1`) |
| P1 row 479 | x | x | `yedges b in` / `texyedges b in` (Y3 `y >= ysize - 1`) |
| P1 row 480 | x | x | `yedges b out` / `texyedges b out`: the fix's want is deterministic; the edit that admits it (Y4 `y > ysize`) reads past vram_z -- NOT PREDICTED |
| P2 (no, no) | x | x | every inner row |
| P2 (yes, no) | x | x | `edges l in` / `texedges l in` (O1; codex's other operand copy, `x1 < 0 && x1 < 0`) |
| P2 (no, yes) | x | x | **`edges2 l rev` / `texedges2 l rev`** [new] (codex D: LREV row 230 arrives 30.0 / -30.0) |
| P2 (yes, yes) | x | x | EQUIVALENT: a span wholly left of column 0 draws nothing with or without the return (the inner `x > 0` rejects every column, and truncation toward zero puts its first column at <= 0) |
| P3 (no, no) | x | x | every inner row |
| P3 (no, yes) | x | x | `edges r in`, `edges rspan` (+ tex) (O2; codex's other copy `x2 >= && x2 >=`) |
| P3 (yes, no) | x | x | **`edges2 r rev` / `texedges2 r rev`** [new] (codex E: RREV row 400 arrives 700.0 / 639.0) |
| P3 (yes, yes) | x | x | EQUIVALENT: a span wholly at or right of 640 draws nothing either way (the inner `x < 640`) |
| P4 forward | x | x | every forward row |
| P4 equal ends, equal attributes | x | x | EQUIVALENT: exchanging equal values is the identity |
| P4 equal ends, unequal attributes | x | x | **`swap vert` / `texswap vert`** [new] (codex C; codex proposed unequal depths read back through a polygon at 1.5 -- unequal COLOUR (simpleline) and u (texturedline) need no second polygon) |
| P4 reversed by 1 | x | x | **`swap s tip` / `texswap s tip`** [new] (codex B: SWAP row 249, 400.5 / 399.5 -- codex's own row) |
| P4 reversed by > 1 | x | x | `yedges swap` / `texyedges swap` (S1) |
| P5 before | x | x | **`swap s before` / `texswap s before`** [new] (codex A: (364,180), codex's own row -- moved into a new session, see section 5) |
| P5 at | x | x | `edges rspan` (X1 `x1 + 1`); also `edges2 r rev` (RREV's swapped start 639.0) |
| P5 after | x | x | DOMINATED: every single edit of the initializer that drops the column after the start (`x1 + k`, k >= 2) drops the start too, which `rspan` sees |
| P6 before | x | x | every inner row (the column before an end is interior) |
| P6 at | x | x | `yedges s end` (+ tex) (E1 `x < x2`) |
| P6 after | x | x | `yedges s past` (+ tex) (E2 `x <= x2 + 1`) |
| P7 column 0 | x | x | `edges l out` (+ tex) (M18, M22) |
| P7 column 1 | x | x | `edges l in` (+ tex) (M19, M23) |
| P7 column 639 | x | x | `edges r in` (+ tex) (M21, M25) |
| P7 column 640 | x | x | `edges r out` (+ tex) (M20, M24: x = 640 of row 330 lands at (0,331)) |
| P8 (<, on) | x | x | `ovon t1 only` / `texbeh t1 only` |
| P8 (<, off) | x | x | `ovoff t1 only` / `texoff t1 only` (M11, M12, M28) |
| P8 (==, on) | x | x | `equal overlap` / `texequal overlap` (M29, M30) |
| P8 (==, off) | x | x | **`zeq overlap` / `texzeq overlap`** [new] (codex F; codex's own row) |
| P8 (>, on) | x | x | `ovon overlap` / `texon overlap` (M27b, M27) |
| P8 (>, off) | x | x | `behind overlap` / `texbeh overlap` (M13, M14) |
| simpleline fractional end, floor(x2) | x | -- | DOMINATED by `yedges s end`: a single edit of `x <= x2` that drops floor(x2) at a fractional end n + f (`x <= x2 - k`, `x < x2 - k`, k >= 1) gives a last column <= n - 1, and at the integral end 435.0 a last column <= 434 -- `s end` reds.  `x < x2` keeps floor(x2) (n < n + f) |
| simpleline fractional end, ceil(x2) | x | -- | **`swap frac past`** [new] (codex I: FRAC row 101 ends 150.5; `x < x2 + 1` draws 151).  texturedline's ends are ints: `x < x2 + 1` is `x <= x2` there -- EQUIVALENT (It, measured green) |

The 16 decode patterns (word 1 bits 25-28), and the single-edit forms they serve (P9, section 4):

| pattern | row |
|---|---|
| 0x00000000 | ovon, texon, equal, edges, ... (every Z-on header) |
| 0x02000000 | `mask25 overlap` (K2) |
| 0x04000000 | `ovoff overlap` and every Z-off header |
| 0x08000000 | `mask overlap` (K1) |
| 0x0c000000 | **`maskoff overlap`** [new] (codex G, `== 1`; codex proposed 0x14000000, culling mode 2 -- 0x0c000000 is culling mode 1, which culls nothing, so no cross-product sign enters the row) |
| 0x10000000 | **`maskhi overlap`** [new] (codex H, `& 5`; the header is 0xf0000000, which also carries bits 29-31 for `& 9`, `& 17`, `& 33`) |
| 0x06, 0x0a, 0x0e, 0x12, 0x14, 0x16, 0x18, 0x1a, 0x1c, 0x1e (x 0x01000000) | NOT NEEDED, 10: every single-edit form of the decode is separated from the fix by one of the six rows above (section 4, P9) -- a pattern that separates no single edit owes no row |

## 4. The added cells (A1-A3, A7) and the edit-form families (A4-A8, P9)

**A1 -- the swap body (Gemini x2).**  MEASURED on the 68-row probe (PVR3_NOTE.md): Zs, Rs, Gs, Bs, Zt, Ut, Vt survived; Xs, Xt red.

| cell | row |
|---|---|
| simpleline x exchange deleted (`double tmpf = x1;` kept) | `yedges swap`, `yedges s end` (measured), and `swap s tip`, `ramp l end`, `edges2 l rev`, `edges2 r rev`, `edges2 l tip` (predicted) |
| simpleline z / r / g / b exchange deleted | **`ramp l end`** [new]: RAMP row 60 arrives 520.0 (v1: z 1.0, magenta 0xff00ff) then 440.0 (v2: z 2.0, green); the fix moves v2's z and colour to column 440, so (440,60) is green at z 2.0 and COVER (z 1.5, blue, drawn after) fails there.  No z exchange: column 440 has z 1.0, COVER passes, blue.  No r / g / b exchange: that channel from v1 -- 0xffe0 / 0x0000 / 0x07ff |
| texturedline x exchange deleted (`int tmp = x1; (void) tmp;`) | `texyedges swap`, `texyedges s end` (measured), and the textured twins of the rows above (predicted) |
| texturedline z / u / v exchange deleted | **`texramp l end`** [new]: v2's (u, v) = (0, 0.125) is texel (0,1), linear 0x100008, stored blue; no z exchange: COVER's texel (0,0), red; no u exchange: texel (4,1), linear 0x10000c, never stored (VRAM is zeroed_alloc'd), 0x0000; no v exchange: texel (0,0), red |

**A2 -- the right clause's compares at their edge (bound - 1; + k is EQUIVALENT: columns >= 640 are never drawn).**  x1 alone
(`x1 >= d->xsize - 1`, R1a): `edges rspan` (RSPAN's rows start at 639.0) + tex.  x2 alone (`x2 >= d->xsize - 1`, R2): **`edges2 r rev`**
[new] (RREV row 400: x1 700.0, x2 639.0) + tex.  Both (R1, table 2): `rspan`, now also `r rev`.

**A3 -- the left clause's compares at their edge.**  A move DOWN is EQUIVALENT (a span with both ends below 0 draws nothing).  A move UP
BY ONE is EQUIVALENT too -- it changes only spans whose moved end lies in [0, 1), which draw at most column 0, and column 0 is never
drawn (L1, measured green in table 2).  **So D2's least-observable NON-equivalent INTEGER move is UP BY TWO, and the edge rows are spans
with an end in [1, 2):**  (Corrected 2026-11-05, repair 4 -- codex pass 4, F1: this said "least-observable NON-equivalent move" with no
INTEGER; the reasoning covered integer moves only, and simpleline's ends are doubles.  The half-pixel moves, settled by the pass-4
ruling's rule D2-F: a position compare is pinned at the pixel and at the half pixel, the only other discretization of a position
being round-to-nearest.  Here they need no new row: `x1 < 0.5` / `x2 < 0.5` are EQUIVALENT -- the span they newly refuse draws at most
column 0, which is never drawn -- and `x1 < 1.5` / `x2 < 1.5` are caught by the same rows, `edges2 l tip` and `edges2 x2 tip`, whose
ends at 1.0 fall below 1.5 (all four built and measured exactly as predicted on the 140-row probe: ../r4_20261105/meas_L/).  Below
half a pixel the family is SAMPLED: ../r4_20261105/PVR4_NOTE.md.)
* x1 compare (`x1 < 2`, or `x1 < d->bytes_per_pixel`, W3): **`edges2 l tip`** [new] -- LREV row 259 arrives 1.0 then -1.0 (reversed,
  x2 < 0); the fix swaps it and draws columns -1..1, so column 1; W3 returns early.  + tex (ints 1 / -1).
* x2 compare (`x2 < 2`, W4): **`edges2 x2 tip`** [new] -- LEFT3 row 159 spans -1.0..1.0 (forward, x1 < 0); W4 returns early.  + tex;
  its Z-off twin is `zleft tip`.
* A move by k > 2 is DOMINATED by the move by 2 (the [1, 2) span returns under every k >= 2).

**A4 -- operand swaps from the body's int fields** (xsize 640, ysize 480, zwrite_disabled 0 or 1, bytes_per_pixel 2).  Per
rasterizer; "caught" names the row that reds:

| operand | -> d->xsize | -> d->ysize | -> d->zwrite_disabled | -> d->bytes_per_pixel |
|---|---|---|---|---|
| `y < 0` | every row returns: caught by every drawn pixel (e.g. ovon t1 only) | the same | Z-off polygons lose row 0: **`zyedges t in`** [new, Z-off twin] (W2) | `t in` |
| `x1 < 0` (P2) | returns reversed spans with x2 < 0: `edges2 l rev` | the same | EQUIVALENT (an up-move by one) | `edges2 l tip` (W3) |
| `x2 < 0` (P2) | returns forward spans with x1 < 0: `edges l in` | the same | EQUIVALENT | `edges2 x2 tip` (W4) |
| `x > 0` (P7) | nothing drawn: caught | columns <= 480 lost: `edges l in` | Z-off polygons lose column 1: **`zedges l in`** [new, Z-off twin] (W1) | column 1 lost: `edges l in` |
| `y >= d->ysize` (P1) | NOT COVERED: rows 480-639 admitted, the depth read leaves vram_z (undefined behaviour) | -- | every row >= 0 / >= 1 returns: caught | every row >= 2 returns: caught |
| `x1 >= d->xsize` (P3) | -- | `edges r in`, `rspan` (Q1) | `edges r in` (x1 >= 0 or 1 with x2 >= 640 returns RIGHT row 330) | `edges r in` |
| `x2 >= d->xsize` (P3) | -- | `edges2 r rev` (Q2) | `edges2 r rev` (RREV: x1 >= 640, x2 >= 0) | `edges2 r rev` |
| `x < d->xsize` (P7) | -- | `edges r in`, `rspan`, `edges2 r rev` (Q3) | nothing drawn: caught | only column 1: `edges r in` |

The two Z-off-only swaps (W1, W2) are the only single-token edits in this enumeration that tie a geometry predicate to Z-write: for
Z-on polygons each IS the fix, and every row-0 and column-1 pixel the 68-row probe read was drawn Z-on.  The Z-off twins (section 8)
read row 0 and column 1 for Z-off polygons (`zyedges t in`, `zedges l in`); the 91-row version's `zleft row 0` (a Z-off polygon at
(1,0)) did the same and was dropped for them.  MEASURED survivors of the 68-row probe: W1s/t, W2s/t, W3s/t, W4s/t (PVR3_NOTE.md, step 2c).

**A5 -- the inner bound's `&&` made `||`** (Ns, Nt): every column of every span is drawn: `edges l out` ((0,230) red) and `edges r out`
(x = 640 of row 330 lands at (0,331)) + tex.  No probed span has a negative column on row 0 or reaches past (639, 479), so the
dropped bound still writes inside vram_z -- the repair-3 geometry was chosen so (a first design, LEFT moved to rows -30..29, would
have put columns -30..-1 of row 0 at vram_z[-30..-1] under this edit, and was replaced: LEFT3 sits at rows 100-159).

**A6 -- the depth test's bound moved.**  +1 (`<= z + 1`, Ps / Pt): T1 and T2 differ by exactly 1.0, so `ovon overlap`, `behind overlap`,
`two overlap`, `sticky overlap`, `mask overlap`, `mask25 overlap`, `maskhi overlap`, `ramp l end` (COVER 1.5 vs 2.0) red; texturedline:
`texbeh overlap`, `texon overlap`, `texramp l end`.  -1 (`<= z - 1`, Pms): `equal overlap`, `zeq overlap`.

**A7 / P9 -- the decode's single-edit forms**, with s = list[1] >> 26 (the rowed headers give s = 0, 0 (bit 25 only), 1, 2, 3, 60):

| form | separated by |
|---|---|
| `&` -> `==` (G) | `maskoff overlap` (s = 3: 3 & 1 = 1, 3 == 1 false) [new] |
| `&` -> `!=`, `<`, `<=`, `\|`, `^`, `\|\|`, `+`, `-` (unsigned: 0 - 1 wraps) | `ovon overlap` (s = 0 becomes Z-off) |
| `&` -> `>`, `%`, `>>` | `ovoff overlap` (s = 1 becomes Z-on) |
| `&` -> `>=`, `&&`, `*`, `/`, `<<` | `mask overlap` (s = 2 becomes Z-off) |
| mask 1 -> m, bit 0 clear | `ovoff overlap` |
| mask 1 -> m, bits 0 and 1 set (K1 `& 3`, ...) | `mask overlap` |
| mask 1 -> m, bit 0 set, bit 1 clear, any of bits 2-5 set (H `& 5`, `& 9`, `& 17`, `& 33`) | **`maskhi overlap`** [new] (s = 60 = bits 2-5) |
| mask 1 -> m, bit 0 set, only bits >= 6 besides (`& 65`, ...) | EQUIVALENT: s <= 63 (H65 in table 3, predicted green) |
| shift 26 -> any other (M31 `>> 25`, `>> 27`, ...) | `ovoff overlap` (bit 26 is read nowhere else); `>> 25` with the mask widened (K2) needs bit 25: `mask25 overlap` |
| `>>` -> `<<` | `ovoff overlap` (the result is 0) |
| list[1] -> list[0] / list[2] / list[3] / list[4..7] | `ovoff overlap` (none of those words has bit 26 in an untextured header); list[3] also reds texbeh / texon / texramp (a textured header's word 3 has bit 26 set) |
| the `!` dropped | `ovon overlap` and `ovoff overlap` (the assignment inverted, M7's twin) |

Widening DOWN to bits 0-24 takes a shift move AND a mask change, two edits (K2 is the bit-25 one, rowed).

**A8 -- the early return's `||` made `&&`.**  First (`y < 0 && y >= ysize`): no y bound at all -- rows above and below the frame are
admitted; NOT COVERED (undefined behaviour).  Second (`y >= ysize && (left clause)`): rows >= 480 admitted unless left of the frame;
NOT COVERED (undefined behaviour, BOTTOM reaches row 509).  Third (`(left) && (right)`): no span is off both edges, so both x clauses
vanish -- EQUIVALENT (the inner bound does their work).

## 5. The rows (60 new, 128 in all) and why each is shaped so

Every want is DERIVED from the sweep (pvr_render_triangle{,_textured}: vertices sorted by y, a tie keeping the listed order; for a flat
top the start edge is v1 -> v3 and the stop edge v2 -> v3, the first row carrying both vertices' values exactly; row y3 never drawn;
texturedline receives the ends truncated toward zero) and from the depth rule (`vram_z <= z` passes; Z-off skips only the store).
Base run 128/128 on build/gxemul (base128/, 3.1 s, no session timed out); pre-fix 60/128 (head128/).  22 repair-3 render sessions,
38 in all; the largest sends 4066 bytes (ztyedges), under STDIN_CAP 4096.

| session (stdin bytes) | rows | catches |
|---|---|---|
| swap (3972) | swap s before, s tip, vert, frac past | A, B, C, I |
| texswap (2909) | texswap s before, s tip, vert | A, B, C (texturedline) |
| ramp (2738) | ramp l end | the swap body z, r, g, b |
| texramp (2837) | texramp l end | the swap body z, u, v |
| edges2 (3962) | edges2 l rev, r rev, l tip, x2 tip | D, E, R2, W3, W4 |
| texedges2 (3968) | texedges2 l rev, r rev, l tip, x2 tip | the same |
| zeq (3100), texzeq (3177) | zeq / texzeq overlap | F |
| maskoff (3100) | maskoff overlap | G |
| maskhi (3101) | maskhi overlap | H, `& 9`, `& 17`, `& 33` |
| zedges (4014), ztedges (4020) | the five edges rows, Z-off | the Z-off twins (section 8) |
| zyedges (4060), ztyedges (4066) | the six yedges rows, Z-off | the same |
| zswap (3978), ztswap (2915) | the swap rows, Z-off | the same |
| zedges2 (2829), ztedges2 (2850) | edges2's l rev, r rev, l tip, Z-off | the same |
| zleft (1644), texzleft (1680) | zleft tip: edges2 x2 tip, Z-off | the same |
| zramp (3092), ztramp (3197) | the swap body for a Z-off span (COVER stored first) | the same |

Departures from codex's proposed rows, each with its reason:
* A, B, C, E, F, G and I keep codex's pixel or channel except: **C** reads unequal colour (simpleline) / u (texturedline) at one pixel
  instead of unequal depth through a second polygon -- one triangle, and a channel the base run validates (the fix reads green from
  the start end; C reads the stop end's red); **E** reads RREV's FIRST row (400: both ends exact) instead of row 430 (whose start
  669.5 accumulates -61/60 thirty times), and the same row pins R2; **G** uses header 0x0c000000 (culling mode 1) instead of 0x14000000
  (culling mode 2, which makes the row depend on T1's cross product); **H** uses 0xf0000000 so one row serves `& 5`, `& 9`, `& 17` and
  `& 33`.
* **A and B are not added to yedges**, where codex put them: yedges already sends 4054 bytes and two more pixel reads (39 bytes each)
  would pass the 4100-byte STDIN CAP (PVR3_NOTE.md) -- the reads would be swallowed and the rows would read `none`.  They live in the
  new swap sessions, on a second copy of SWAP.
* **D** reads LREV at row 230 as codex proposed; edges2 additionally reads LREV's last row (259) and LEFT3's (159) for A3.
* The 91-row version's `zleft row 0` / `texzleft row 0` (a Z-off polygon at (1,0), for W1/W2) are dropped: the Z-off twins of
  `yedges t in` and `edges l in` hold both cells, and every variant that redded them reds a twin.

## 6. Deliberately NOT covered -- the contract's list, with reasons

* rows above and below the frame: `y < -1` (Y2), `y > ysize` (Y4), `y >= d->xsize`, A8's first and second `&&`: undefined behaviour;
* EQUIVALENT: P2/P3 all-off-screen cells; the left clause moved down or up by one; the right clause loosened; A8's third `&&`; equal
  ends with equal attributes; texturedline's `x < x2 + 1` (It); the mask widened past bit 31 (H65);
* DOMINATED: the column after the start; simpleline's floor(x2) at a fractional end;
* a FRACTIONAL move of the swap bound in simpleline (`x1 > x2 + 0.5`): every probed reversed span differs by a whole number (SWAP's
  ends step by +-0.5 each row).  texturedline's ends are ints, so there it is EQUIVALENT;
  [WITHDRAWN 2026-11-05 by the pass-4 ruling (rule D2-F): the simpleline half of this item is a floor breach, not a disclosure --
  codex pass 4's B1, measured surviving the 128-row probe (../r4_20261105/meas_B/) and rowed by repair 4's `half swap`; the
  texturedline half stays EQUIVALENT.  The item is kept, struck, so the record shows what was disclosed.]
* the per-span interpolation (dz12, dr12, dg12, db12, du12, dv12) and the per-pixel steps: data flow into the stored and drawn values,
  not a predicate dominating the store (the DEPENDS-ON bound forbids transitive data-flow chasing); the ramp rows read only a span's
  first pixel;  [CORRECTED 2026-11-05, repair 4: the ramp rows' first-pixel reading left the swap body's `a2 = tmpf` half unpinned
  -- codex pass 4's B4-B10, measured surviving in ../r4_20261105/meas_B/; repair 4's ramp8 rows read the reversed span's far end.
  The interpolation between the two ends stays data flow.]
* the decode widened DOWN past bit 25 (two edits);
* (the geometry x Z-write question this file once left open is SETTLED by the coordinator's ruling: the Z-off twins, section 8.)

## 7. The CONTRACT text (as it stands in the probe header)

See `regress/pvr_zwrite_probe.py`, docstring, "REPAIR 3 CONTRACT" through "NOT COVERED, by name" -- the COVERED list maps one-to-one
onto sections 3 and 4 above, and the NOT COVERED list onto section 6.

## 8. THE Z-OFF TWINS (the coordinator's ruling, 2026-11-05)

**The ruling.**  "By the letter of the 09-04 floor ruling the cells a row is owed for are the cross-product of the guard's dominating
predicates (every geometry predicate that dominates the guarded depth store, and the depth test) with the device state the repair
path reads (zwrite_disabled), and the two are jointly reachable (any polygon can be Z-off with any geometry).  So every geometry cell's
Z-off twin is a floor cell ... Rows that pin each geometry edge for a Z-off polygon also catch every multi-token form at that edge."

**The rows.**  Each single-layer geometry session -- edges, yedges, swap, edges2 and their textured twins -- is repeated with its header
made Z-off (zedges, zyedges, zswap, zedges2; ztedges, ztyedges, ztswap, ztedges2), and edges2 gained LEFT3's row 159 (`x2 tip`, Z-on)
so that zleft's Z-off LEFT3 is its twin.  **Every want is the Z-on twin's, derived the same way:** a Z-off polygon goes through the same
y and x clauses, swap, span bounds and depth test, and draws the same colour -- `if (!d->zwrite_disabled)` skips only the store -- and
over the cleared frame its depth test passes as the Z-on one's does.  The swap body cannot be twinned that way (its z channel needs a
stored depth), so zramp / ztramp draw COVER (Z-on, z 1.5) FIRST and the RAMP Z-off over it: v2's z 2.0 passes `1.5 <= 2.0` and draws;
without the z exchange z 1.0 fails and COVER's colour stays; without the r, g, b (u, v) exchanges the colour changes as in ramp.

**The prediction rule (pvr_variants_3.py `twins()`).**  For a variant that does not treat Z-off geometry differently, a twin reds exactly
when its Z-on row reds (same pixels, same depth outcome).  The variants that DO treat it differently are derived one by one:
* B1 (the exit reinstated) and the pre-fix HEAD: every Z-off session ends the process, so all 37 twin rows red (pixels read `none`) --
  the HEAD leg MEASURED this already (head128/: 60/128, exactly the predicted red set);
* M11 (Z-off triangles declined), M12 (simpleline's hoist: Z-off draws nothing), M28 (texturedline's): every twin that wants a colour
  reds; the ones that want black stay black;
* W1 (`x > d->zwrite_disabled`): the Z-off column-1 twins (zedges l in, zedges2 l rev, l tip, zleft tip); W2 (`y <
  d->zwrite_disabled`): zyedges t in;
* zramp / ztramp under the non-Z-specific variants: red under A (x1 - 1: column 440 takes the second step's colour or texel), X1 (x1 +
  1: RAMP misses 440, COVER shows), S1 and the x-exchange deletion (RAMP not drawn), the z / r / g / b (z / u / v) exchange deletions,
  and Pms (`<= z - 1`: 1.5 <= 1.0 fails -- the one place the Z-off ramp differs from the Z-on one, whose RAMP is drawn over the
  background).

**The multi-token family (the coordinator: one representative per geometry predicate).**  One edit per predicate per rasterizer moves a
bound by 2 * d->zwrite_disabled, so Z-on polygons see the fix and Z-off ones a moved edge; each is predicted to red only Z-off twins
(and zleft tip), and each would have survived the 68-row probe (table 3 measured every V variant red on repair-3 rows only).
(Corrected 2026-11-05, repair 4 -- codex pass 4, F3, with the pass-4 ruling's correction to codex: this said each "would have
SURVIVED the 91-row probe (no row drew Z-off geometry there but zleft's one triangle)".  That probe's zleft session drew ONE Z-off
triangle, LEFT2 (base91_v1/probe91_run.py), not "ZCORNER and LEFT3" as codex read it, and by derivation FOUR of the fourteen would
have been red there, not five: V1s (zleft row 0), V6s (zleft tip), V2t (texzleft tip) and V7t (texzleft row 0 and tip); V5t (`x1 +
2`) still draws column 1 and survives.)

| predicate | simpleline (V..s) | red | texturedline (V..t) | red |
|---|---|---|---|---|
| P1 y | `y < 2zw` | zyedges t in | `y >= ysize - 2zw` | ztyedges b in |
| P2 left | `x1 < 2zw && ...` | zedges2 l tip | `... && x2 < 2zw` | texzleft tip |
| P3 right | `x1 >= xsize - 2zw && ...` | zedges rspan | `... && x2 >= xsize - 2zw` | ztedges2 r rev |
| P4 swap | `x1 > x2 + 2zw` | zswap s tip, zedges2 l tip | `x1 > x2 - 2zw` | ztswap vert |
| P5 start | `int x = x1 - 2zw` | zswap s before, zramp l end | `int x = x1 + 2zw` | ztedges rspan, ztswap s tip, vert, ztedges2 r rev, ztramp |
| P6 end | `x <= x2 - 2zw` | zyedges s end, zswap s tip, vert, zedges2 l tip, zleft tip | `x <= x2 + 2zw` | ztyedges s past |
| P7 inner | `x < xsize - 2zw` | zedges r in, rspan, zedges2 r rev | `x > 2zw && ...` | ztedges l in, ztedges2 l rev, l tip, texzleft tip |

(2zw = `2 * d->zwrite_disabled`.)  Each red comes from the same edge its Z-on row pins, moved for the Z-off polygon the twin draws.  All
66 new variants, the V family included, pass `cc -fsyntax-only` with build/'s flags (`syntax_check_V.sh`).

