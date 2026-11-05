# Cloud routine answer, banked VERBATIM by extract_teleport.py at 2026-11-05 02:13:02Z

* source: the local transcript of `claude --teleport` -- `C:/Users/User00/.claude/projects/C--Users-User00-AppData-Local-Temp-claude-d0d925bc6bb158fc-ccd8e376-b626-4ae7-b60a-ecf2767f320e-scratchpad-tppvrp2o/eba83adf-f205-41c8-a926-17e9437a210c.jsonl`
* session: `https://claude.ai/code/session_015fEQzGpwArRsBG9K3s1RFk`   trigger: `trig_019r5aF39CNmuRXm6iVRaNXa`   packet: `C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/w_pvr/P2_PVR_cloud.md`
* the answer's message: timestamp 2026-11-05T02:10:51.894Z, model field `claude-opus-5-5` (all assistant models in the transcript: ['claude-haiku-5-5', 'claude-opus-5-5'])
* delivery token `CLOUDP2PVR`: present; 9779 characters; PART markers N = 0, present 0, MISSING none; `END OF PARTS`: NO
* safety-classifier notices in the transcript: none
* the run's final line: CLOUDP2PVR: 3 CHECKED 2 FALSE 4 FLOOR-GAPS VERDICT:REPAIR-NEEDED

---
CLOUDP2PVR
model: claude-opus-5-5 (Opus 5.5)
VERDICT: REPAIR-NEEDED. The fix itself is correct and matches the ruling. The detector needs more rows: it has four in-bound floor gaps of the same kind addendum 6 found and fixed for the x-range.

**1. The fix**

**Against the ruling, change for change:**
- **C1 (the struct field):** matches. Only the comment's line wrapping and indentation differ.
- **C2 and C3 (the two rasterizers):** one guard on each `vram_z` store, at simpleline 687 and texturedline 772. The old line 761 is now line 766, `double z = z1, u = u1, v = v1;`, and it is kept. I cannot check "r1 as written" word for word because r1's hunks are not in the brief.
- **C4 (the per-render reset):** deviates in position only, and the deviation is harmless. The ruling places the reset "in the settings block at 1087-1089" (HEAD numbering, which is now about 1093-1095). The diff puts it just after the settings block, at 1137. Lines 1093-1135 contain only declarations, nothing between the two spots reads the field or leaves the function, and both spots come before the 1166 return and before the command loop. The ruling's stated reason ("precedes the command loop") is satisfied.
- **C5 (the exit replaced):** matches. The comment is the same and the assignment is `= !zwrite`.
- **C6 (no announce):** matches. There is no announce, latch or `warned_nozwrite`.
- **C7 (diff hygiene):** matches. There is no fogv comment and no new zwrite/texture1 prints, and both word-2 TODOs are kept.

**P1 (all headers have bit 26 clear) — true.**
- The field is set to 0 at line 1137.
- Every type-4 header then assigns `!zwrite`, which is `!(!0)`, so 0.
- No other code writes the field. So the guard always passes, every store runs as on HEAD, and every pixel and every `vram_z` value is the same.
- The struct gains a field in the middle, which shifts the offsets of later fields. Nothing shown depends on those offsets.

**P2 (modifier-volume headers) — true as worded, but the meaning is unresolved.**
- Case 4 handles both polygon and modifier-volume headers, and it reads bit 26 the same way for both.
- From memory of the CLX2 documentation, a modifier volume's ISP word carries only the volume instruction (bits 31-29) and the culling mode (bits 28-27). The lower bits, bit 26 included, are reserved. I have not checked this against a source, so the fix may be treating a reserved bit as "Z-write disable".
- On HEAD, that bit already ended the emulator. On the fix, it sets a field that the next header overwrites. Low risk.

**P3 (M17, the reset moved to the end, is equivalent) — true.** The equivalence rests on the field being 0 between renders:
- It relies on DEVINIT zeroing the struct, which is not shown here.
- Every path that reaches the loop also reaches the end of pvr_render, because the only other ways out are `exit()` calls.
- On the 1166 early return the field is already 0. Under the current code it is 0 because the reset at 1137 comes before that return. Under M17 it is 0 because it was never set.
- simpleline and texturedline are only reached through pvr_render (addendum 7f).

**The field's lifetime and every exit path:**
- A header's value lasts across all strips until the next header or the end of the render. That matches TA header semantics, and other header state (texture, culling mode) already persists the same way.
- `END_OF_LIST` does not clear the field. This is consistent with the other header state.
- The early returns (simpleline 660, texturedline 733, pvr_render 1166) all leave the field as it was.
- The `exit()` calls at 874, 1090 and 1432 are older sibling exits and are not affected.

The fix is correct.

**2. The floor: four gaps, none of which any row catches**

Addendum 6 applied this rule: a predicate that dominates the guarded stores is in bound, and each relational compare is pinned at its edges. By that same rule, two more predicates in each rasterizer are in bound but have no row:

**(a) The y-range early return**, simpleline 658 and texturedline 731. These are four edits per rasterizer:
- `y < 0` changed to `y < 1`
- `y >= d->ysize` changed to `y >= d->ysize - 1`
- `y < 0` changed to `y < -1`
- `y >= d->ysize` changed to `y > d->ysize`

Expected red: none. No session draws a pixel on row 0 or row 479. The lowest drawn y is 100 and the highest is 470, from AWAY. The two widenings write `vram_z` outside its buffer (`vram_z[x-640]`, or row 480), so a regression here is memory-unsafe.

**(b) The span-end loop condition**, simpleline 683 and texturedline 768. The edits are `x <= x2` changed to `x < x2` or to `x <= x2 + 1`. Expected red: none. No probed pixel is within one column of a span end:
- At y=180, T1 spans 140-260 and T2 spans 165-335. The probed pixels are 220 and 320.
- At y=120, T1 spans 110-290. The probed pixel is 120.
- The edge rows test the x-range bound, not the span end.

That gives four gap sites: (a) in each rasterizer and (b) in each rasterizer. Proposed rows: one pixel each on rows 0 and 479, and one pixel at a known span end, in both an untextured and a textured session.

**What I swept:**
- The 36 enumerated variants. The table reproduces every predicted red set.
- `&&` changed to `||` in each early-return clause and in `x > 0 && x < xsize`. I predict the edge rows red these, but none of them was run.
- The swap at `x1 > x2`. Whether deleting it changes anything depends on how pvr_render_triangle orders x1 and x2, which the brief does not show. A variant run would settle it.
- The command loop bound `index < n_ta_commands`. Tightening it drops the last vertex, which the "t2 only" rows catch. Using `<=` reads a cleared command, which is effectively equivalent.
- The case-4 bit: M31 covers it.
- The RGB565 check at 1088 and the fb_base bound at 1158. Both dominate the reset or the loop. Under a strict reading they are in bound, and no row here moves for them. They belong to sibling and #119 dispositions; running them against the full gate would settle whether those blocks cover them.

**3. The channel check**

- **Rows that catch Z-off behaviour:** every session row and both zoff rows red under B1, where the process exits and no prompt appears.
- **Overlap rows:** each one is moved by the variants listed in table 1, and its pixel changes as section 4 of PRETABLE describes:
  - ovoff, ovon, behind, texoff, texbeh, texon: 0xf800 versus 0x07e0.
  - sticky: 0x001f versus 0x07e0.
  - two: 0x07e0 versus 0xf800.
- **"t1 only" and "t2 only" rows in Z-off sessions:** these catch M11, M12 and M28 (drawn versus 0x0000).
- **Edge rows:** these catch M18-M25.
- **R10 rows (equal and texequal overlap):** these catch M29 and M30.

None of the rows is vacuous. Two rows behave like controls without being flagged as controls:
- **Eight pixel rows move only under B1:** ovoff t2 only, ovoff bg, behind t1 only, texoff t2 only, texbeh t1 only, two t1 only, two t2 only and sticky t2 only. Under B1 they only read "none" because the process died, which the session row of the same session already reports. Addendum 7d is right that they are not controls. They are also not independent detectors, so the 51-row count overstates how many separate things are being checked.
- **The nine session rows pass on /bin/true:** they only mean something together with the pixel and prompt rows in the same session.

The thirteen controls held CONTROL=OK on the HEAD leg, under B1 and under every M-variant. They are unmoved, as far as the enumerated variants go.

**4. False records: two**

- **The probe's printed banner** reads `pvrrenderexit RUNG-3 WITNESS`. The docstring and the gate comment both say this file is the detector and that the witness is not run.
- **PRETABLE section 3, the joint cells**, lists "texturedline (0,pass) texbeh and texon t1". There is no texon t1 row; the texon session only emits "overlap" and "t2 only".

Imprecise but not counted:
- The field comment says "of the polygon being rendered". It actually holds the bit of the most recent type-4 header, which can be a modifier-volume header, and it is 0 in a render with no header.
- VERDICT.md says "M1-M33 … each reddened exactly the rows PRETABLE named". That includes M17, which reddened no rows and is only true in the sense that it matched its empty prediction.

**5. Other findings, most severe first**

1. **The floor gaps in section 2.** To settle: run the eight y-bound edits and the four span-end edits against the probe and confirm 51/51, then add the rows.
2. **The two "l out" rows (edges and texedges) lock in the existing column-0 behaviour.** They require column 0 to stay BLACK, but `x > 0` looks like an existing off-by-one in HEAD. If someone later corrects it to `x >= 0`, the gate goes red. To settle: compare a render covering column 0 with reference hardware or another renderer. If column 0 should be drawn, re-note these rows as pinning HEAD's behaviour, not correct behaviour.
3. **There is no proof that what was measured is what is in the tree.** The table ran on `dev_pvr.c.fix` (md5 481755b4f10f) and `probe51_draft_frozen.py` (md5 5da28a4dfcf7). To settle: compare the md5 of the in-tree `src/devices/dev_pvr.c` and `regress/pvr_zwrite_probe.py` against those. Gate 14 is still running, and the ship decision should wait for its result.
4. **M17's equivalence assumes DEVINIT zeroes the struct**, which is not shown. To settle: read DEVINIT(pvr) for `memset(d, 0, sizeof(*d))`.
5. **P2's semantics.** To settle: a session with a list-type-1 header with bit 26 set, followed by a Z-on polygon list, compared against expected pixels.
6. **The ruling's own placement for the C4 reset is unmet** (cosmetic). Either record the deviation beside the ruling or move the reset to 1093-1095.

CLOUDP2PVR: 3 CHECKED 2 FALSE 4 FLOOR-GAPS VERDICT:REPAIR-NEEDED
