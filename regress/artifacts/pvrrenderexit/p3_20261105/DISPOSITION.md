# pvrrenderexit PASS 3 -- disposition (main loop, 2026-11-05)

Seats: codex GPT-6 Astra at `ultra` ANSWERED (codex_codex_pvr_p3.txt; `CODEXP3PVR: 84 CELLS SWEPT 15 BREACHES 5 FALSE RECORDS
VERDICT:REPAIR`; it read both rasterizers, both triangle sweeps, the decode, culling, texture selection, the depth allocation and the
probe; it built and ran nothing).  Gemini 4 Argon x2 (jobs p3_pvr, p3_pvr_r2): being sent at the time of writing -- folded in when they
land.  glm-5.3 SEAT DOWN (Ollama monthly limit); grok-4.7 SEAT FAILURE (402 billing wall).

## codex's findings (DERIVED from the source, not measured; each "two breaches" = one per rasterizer)

* A -- span start widened, `int x = x1` -> `x1 - 1` (2): no row reads the column before the span start; row: `s before` (364,180).
* B -- swap threshold `x1 > x2` -> `x1 > x2 + 1` (2); C -- `x1 > x2` -> `x1 >= x2` (2): the two edges of the swap compare, unrowed
  (repair 2 rowed only the swap DELETED).  C needs equal endpoints with UNEQUAL depths, which no flat-depth probe triangle has.
* D -- the left clause's first operand copied, `(x2 < 0 && x2 < 0)` (2); E -- the right clause's second operand copied (2): every rowed
  span arrives forward-oriented; rows: reversed LEFT and reversed RSPAN.
* F -- the depth test made `vram_z[ofs] < z || (!zwrite_disabled && vram_z[ofs] == z)` (2): the (Z-off, equal depth) joint cell is
  unrowed (equal/texequal are Z-on).
* G -- the decode `(list[1] >> 26) & 1` -> `== 1` (1); H -- `& 1` -> `& 5` (1): no header sets bit 26 together with a higher bit, or
  bit 28 alone.
* I -- simpleline's span end `x <= x2` -> `x < x2 + 1` (1): repair 2's exact-integer end cannot separate them; a fractional end can.
* a-e (records): "59 red, every one on its predicted rows" (4 of the 59 were NOT PREDICTED); the gate's "fifteen render sessions"
  (sixteen); a PRETABLE-order claim not restricted to the driver and results; "the three sibling exits in the same function" (the
  texture-format exit is in texturedline(), the other two in pvr_render()); Y2's "negative VRAM offset when FB_RENDER_ADDR1 < 1280"
  (overbroad: the colour offset at fb_base 1000 is positive).

## Disposition (standing rules; no new ruling is needed for the gradings)

* The pass-2 ruling put the predicates dominating the guarded depth store in BOTH rasterizers, and the decode, inside the floor, and
  repair 2 closed one member per predicate.  A-I are further members of exactly those predicates: the compares' other edges (rule D2:
  a region is pinned at its edge, two rows per compare at most), operand swaps drawn from fields the body reads (DEPENDS-ON clause 2),
  the guard x depth-relation joint cell (the 09-04 floor: guard predicates x the state the repair path reads), and the decode's further
  single-edit forms.  If measured (repair 3 measures them FIRST), they are floor breaches, L2, repaired in-round.
* Pass 2 and pass 3 found breaches of the same class, so repair 3 owes the CLASS CLOSURE in one diff: enumerate the space from the
  rasterizers' own inputs (codex's 84-cell denominator is the starting point), close every floor cell, and write into the probe
  CONTRACT which cells are covered and which are deliberately not -- so the next pass verifies an enumeration instead of hunting cells.
* a-e are wrong records (L4): corrected in place in the probe docstring and the gate comment, and as dated errata beside the table-2
  files (never rewriting a measurement record).
* Repair 3 goes to an implementer (Opus 5.5 subagent).  It writes gate_arm.sh's pvr block as a file for the main loop to apply, because
  the fbsdram implementer is editing a different block of gate_arm.sh in the same window.

## ADDENDUM -- Gemini's first reading

`p3_pvr` (gweb/jobs_20261105_rounds/p3_pvr/gemini_web.out; no verdict line -- exit 1 -- read in full): REPAIR, one breach = codex's B
(the swap threshold `x1 > x2 + 1`, needing a reversed span narrower than 1 pixel), and one false record = codex's b ("fifteen render
sessions": sixteen).  It confirms the mask25 row is rightly added (no probe header set bit 25).  Nothing beyond codex; `p3_pvr_r2`
pending.

## CORRECTION + ADDENDUM -- the first answer's file was overwritten; both Gemini readings now in

The addendum above cites `p3_pvr/gemini_web.out` (2,344 bytes, no verdict line: the swap threshold `x1 > x2 + 1` and "fifteen" render
sessions).  The sender RE-SENT that job at 02:51:31 local and overwrote the file, so that first answer survives only as quoted above.
The resend (`gemini_p3_pvr.md`, 2,890 bytes, `GWEBP3PVR: 4 ATTACKS 2 BROKEN 2 HOLDS`) and the replication (`gemini_p3_pvr_r2.md`, 2,523
bytes, `GWEBP3PVRR: 4 ATTACKS 2 BROKEN 2 HOLDS`), both banked beside this file, INDEPENDENTLY found one cell beyond codex: deleting only
the z1/z2 swap (or the r/g/b, or the texture-coordinate swaps) inside the `x1 > x2` block keeps all 68 rows green, because the SWAP
triangle is flat (z 2.0 and one colour at every vertex).  Same class as codex's C (DEPENDS-ON clause 2: the body reads those values
after the swap); handed to the repair-3 implementer to measure first.  Both also repeat codex's b (sixteen sessions, not fifteen).

*Corrected 2026-11-05 (main loop): this file's time-of-day stamps (removed: ~10:1xZ, ~10:3xZ, ~11:1xZ) were GUESSES that ran up to 3.5 hours AHEAD of the clock; the qhs landing-kit agent found them by checking against the files' own timestamps.  The file's own timestamps are the record: created 08:35Z, last written 08:54Z before this note (UTC).*
