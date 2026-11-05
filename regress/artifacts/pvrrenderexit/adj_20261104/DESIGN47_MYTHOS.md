# Cloud routine answer, banked VERBATIM by extract_teleport.py at 2026-11-05 00:20:49Z

* source: the local transcript of `claude --teleport` -- `C:/Users/User00/.claude/projects/C--Users-User00-AppData-Local-Temp-claude-d0d925bc6bb158fc-ccd8e376-b626-4ae7-b60a-ecf2767f320e-scratchpad-tpmythpvr/3ec00595-6caa-47d6-a274-4742d3ab025a.jsonl`
* session: `https://claude.ai/code/session_015fEQzK93QApTMZmCRC1rYy`   trigger: `trig_011VFvYFpC8GaEzdL4CgYw1S`   packet: `_scratchpad/w_pvr/PVRDET_mythos.md`
* the answer's message: timestamp 2026-11-05T00:17:02.637Z, model field `claude-mythos-5-1` (all assistant models in the transcript: ['claude-haiku-5-5', 'claude-mythos-5-1'])
* delivery token `MYTHOSPVRDET`: present; 9046 characters; PART markers N = 0, present 0, MISSING none; `END OF PARTS`: NO
* safety-classifier notices in the transcript: none
* the run's final line: MYTHOSPVRDET: 6 RULINGS 0 WRONG 1 GAPS VERDICT:CHANGE-FIRST

---
MYTHOSPVRDET
model: claude-mythos-5-1 (configured identifier; the serving model may differ)
VERDICT: CHANGE-FIRST. All six added sessions are owed. All 26 predictions re-derive as written (zero wrong). One in-bound edit no row notices: the equal edge of the depth compare (`<=` to `<`) in each rasterizer. One detector row (`texon session`) is survive-only and must be flagged a control. Four in-bound variants are missing from the list but are caught. Land these before the table.

## 1. The added sessions

- **R6 `behind`: OWED**, by the joint-cell rule (PRETABLE section 3, cell {zwrite 1, depth fail} in simpleline) and by the claim rule (comment "depth test kept"). It is the only catcher of M13. Without it, "Z-write disable" misread as "Z-test disable" is a floor gap. R2 only exercises the pass side of a Z-off polygon.
- **R7 `texbeh`: OWED**, by sibling parity and the same joint cell in texturedline. Only catcher of M14.
- **R7 `texon`: OWED**, by joint-cell exhaustion, cell {zwrite 0, depth fail} in texturedline. Its catch set for the listed 26 is a strict subset of texbeh's, so on the listed variants alone it would be excess. But one in-bound weakening makes it unique: `d->vram_z[ofs] <= z || !d->zwrite_disabled` in texturedline (Z-on polygons skip the depth test). texbeh's T2 is Z-off, so the test still applies there and texbeh stays green. texon overlap goes green and is the only red. Keep it, and add that variant (M27 below) so the row has a reason in the table.
- **R8 `sticky`: OWED**, by the guard-field vs body-field rule (section 3: the field set by one header and a later Z-on header in the same render). Only catcher of M8. `two` cannot catch it because render 2 goes through the entry reset.
- **R9 `edges` and `texedges`: OWED**, by D2. `if (x > 0 && x < d->xsize)` dominates both edited stores, so DEPENDS-ON clause (1) enumerates it, and no earlier session drew within 10 pixels of either edge. Two rows per compare, four per rasterizer, eight total: within D2's cap. Z-on headers are right for these sessions: under Z-on the edited store itself is what lands at the wrapped offset. Note these rows do not discriminate HEAD from the fix (HEAD has the same bound); that is proper for floor rows.

## 2. The predictions, re-derived

Geometry check first. T1 at y = 180 spans x 140..260, T2 spans 165..335, so (220,180) is in both, (320,180) is T2 only, (120,120) is T1 only (T2 starts at y = 150). Depth: the larger z wins, T1 = 2.0 near, T2 = 1.0 far, background below both.

- **B1_exit**: Z-off sessions die inside the STARTRENDER store, so every pixel reads none and `how` = exit1. Red: zoff session, zoff prompt (2), ovoff (5), behind (4), texoff (4), texbeh (4), two (4), sticky (3) = 26 red. 13/39, 21/47 since edges and texedges carry no Z-off header. `zoff rendered` stays green because the entry debug line precedes the loop and exit(1) flushes stdio. Correct.
- **M3 simple_inv**: ovoff: T1 Z-off stores 2.0, T2 fails, overlap 0xf800. ovon: T1 never stores, T2 passes, 0x07e0. behind: T1 never stores, T2 Z-off passes and stores, 0x07e0. two: render 2 flag 0, T1 never stores, 0x07e0. sticky: flag 0 after the Z-on header, T1 never stores, 0x001f. texoff: T1 is texturedline (correct guard), T2 simpleline Z-on draws without storing, overlap green, OK. Five red, 42/47. Correct.
- **M4 tex_inv**: texoff: T1 textured Z-off stores 2.0, T2 untextured fails, 0xf800. texbeh: T1 no store, T2 Z-off passes and draws green. texon: T1 no store, T2 green. texedges: drawn, no store, fine. Three red, 44/47. Correct.
- **M6 assign1**: ovoff and texoff stay green (nothing stores, T2 passes). ovon, behind, texbeh, texon red (T1 never stores). sticky red (T1 under flag 1). two green (render 2 has no header, reset to 0). Five red, 42/47. Correct.
- **M7 assign_inv**: adds ovoff and texoff (Z-off now stores, Z-on T2 fails) to M6's five. Seven red, 40/47. Correct.
- **M8 sticky**: only sticky overlap: flag stays 1 through the Z-on header, T1 never stores, T2 blue draws over, 0x001f. two is saved by the entry reset. 46/47. Correct.
- **M9 / M10**: only two overlap (render 2 inherits 1, T1 does not store, T2 green). Section 7 settles M10 the same way. Correct.
- **M11 decline**: ovoff t1 only, behind t2 only, texoff t1 only, texbeh t2 only all 0x0000. The overlap rows stay right. Four red, 43/47. Correct.
- **M12 hoist_simple**: ovoff t1 only and behind t2 only black (texoff's T1 is texturedline). Two red, 45/47. Correct.
- **M13 / M14**: behind overlap and texbeh overlap respectively: the far Z-off T2 bypasses the test and draws green. One red each. Correct.
- **M15 / M16**: simpleline never stores: ovon, behind, two, sticky overlap (ovoff and texoff stay green). texturedline never stores: texbeh, texon. Correct.
- **M17**: equivalent as argued, provided the two rasterizers are only ever reached from pvr_render and the field's only non-zero writer is inside the loop. 47/47 is the right label.
- **M18-M25**: `x >= 0` draws (0,230) from LEFT's row 230. `x > 1` blanks (1,230). `x <= xsize` admits x = 640 on row 330, offset 331*640, pixel (0,331), and admits nothing else (641..670 stay excluded). `x < xsize - 1` blanks (639,330). Exactly one red each, 46/47. Correct. Deleting a bound also reds l out or r out, so the deletions are covered.

No wrong predictions.

## 3. The controls

None of the 13 declared controls is the only catcher of any of the 26. I checked the one in-bound edit that moves "controls", the inverted compare `>= z`: it blanks T1 over the background, so ovon t1 only moves, but ovoff t1 only and ovon overlap (black instead of red) move too.

One detector row is unmovable: **`texon session`**. Both headers in that session are Z-on, so B1 cannot kill it, and no other variant touches an exit. It is survive-only, which section 4 says no detector row may be. Flag it `control=True` (or drop it, matching `ovon`, `edges` and `texedges`, which have no session row). Measurement: the table's per-variant red sets will never contain it.

## 4. Missing in-bound variants

Each is one exact edit.

- **M26_simple_ztest_deleted**: simpleline `if (d->vram_z[ofs] <= z)` to `if (1)`. Red: ovon, behind, two, sticky overlap. 43/47. (texturedline twin: texbeh, texon overlap, 45/47.)
- **M27_tex_zon_bypass**: texturedline `<= z` to `<= z || !d->zwrite_disabled`. Red: texon overlap only. 46/47. This is the variant that earns texon its place. (simpleline twin: ovon, two, sticky overlap.)
- **M28_hoist_tex**: texturedline `if (d->vram_z[ofs] <= z && !d->zwrite_disabled)`. Red: texoff t1 only, texbeh t2 only. 45/47. The list has M12 for simpleline only, breaking the sibling parity the list otherwise keeps.
- **M29_simple_lt / M30_tex_lt**: `<=` to `<` in each rasterizer. **Red: none. This is the gap.** PRETABLE declines it because D2 is "a constant bound" rule, but the ruling's own D2 wording carries no such limit, and the table already treats tightenings of a two-variable-free compare as in-bound (M19, M21). Coplanar polygons drawn twice are ordinary Dreamcast decal practice, so the edge is reachable in real guests.
  Fix: one session `equal` (and `texequal` for parity): Z-on header, T1 red at z = 2.0, T2 green at z = 2.0, read overlap and t2 only. Want overlap 0x07e0 (ties go to the later polygon under `<=`); under `<` it reads 0xf800. Settling measurement: run `equal` on the fixed build first. If overlap is 0x07e0 the edge is exact and the row stands. If it reads 0xf800, per-pixel interpolation drifted below 2.0 and the edge is unreachable on this tree; record the row void like R5's clause rather than rewriting it.

Also in-bound but caught, worth listing for completeness: wrong bit (`>> 25`) reds ovoff and texoff overlap; entry reset changed to `= 1` reds two overlap; reset moved inside the per-command loop reds ovoff and texoff overlap.

## 5. Everything else, by severity

1. **Equal-edge gap** (section 4, M29/M30). Settled by running `equal` on the fixed build, then on M29.
2. **`texon session` flagged as detector while survive-only.** Settled by the table: it is green in all 26 columns. Change the flag before the table since the probe does not change during it.
3. **Four missing variants** (M26, M27, M28 and twins). Not gaps, but M27 is what justifies keeping texon, so the table should carry it. Settled by their predicted single-row reds appearing in SCORES.txt.
4. **M17 equivalence** rests on simpleline and texturedline having no caller outside pvr_render. A grep for their call sites settles it; if one exists, M17 is a real variant and needs a row.
5. **Low**: `zoff rendered` on the B1 and HEAD legs depends on the entry debug line being flushed by exit(1). It is, since exit() flushes stdio; only an `_exit` would break it. The HEAD leg's own run settles it.

Recommended pre-table change set: add the `equal` and `texequal` sessions (4 rows, 51 total), set `texon session` to control, add M26-M30 with twins to the variant list, and restate denominators to /51.

MYTHOSPVRDET: 6 RULINGS 0 WRONG 1 GAPS VERDICT:CHANGE-FIRST
