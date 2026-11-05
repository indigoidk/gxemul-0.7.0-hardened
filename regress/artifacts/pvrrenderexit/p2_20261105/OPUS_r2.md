# Cloud routine answer, banked VERBATIM by extract_teleport.py at 2026-11-05 02:27:46Z

* source: the local transcript of `claude --teleport` -- `C:/Users/User00/.claude/projects/C--Users-User00-AppData-Local-Temp-claude-d0d925bc6bb158fc-ccd8e376-b626-4ae7-b60a-ecf2767f320e-scratchpad-tppvro2/112044b5-012a-4cc0-9c7f-b67064edcc70.jsonl`
* session: `https://claude.ai/code/session_015fEQzFJhUBWeHaor3VAyJf`   trigger: `trig_019r5aF39CNmuRXm6iVRaNXa`   packet: `C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/w_pvr/P2_PVR_cloud.md`
* the answer's message: timestamp 2026-11-05T02:17:54.292Z, model field `claude-opus-5-5` (all assistant models in the transcript: ['claude-haiku-5-5', 'claude-opus-5-5'])
* delivery token `CLOUDP2PVR`: present; 11617 characters; PART markers N = 0, present 0, MISSING none; `END OF PARTS`: NO
* safety-classifier notices in the transcript: none
* the run's final line: CLOUDP2PVR: 3 CHECKED 4 FALSE 8 FLOOR-GAPS VERDICT:REPAIR-NEEDED

---
CLOUDP2PVR
model: claude-opus-5-5 (configured ID; the model serving this turn may differ)
VERDICT: REPAIR-NEEDED. The fix is correct and matches the ruling. The repair is owed by the detector, not the fix: it has floor gaps in the y-range and span-end bounds of both rasterizers, and in two pvr_render guards that come before the assignment. Four records misstate small facts. Gate 14 in situ has not reported yet.

1. THE FIX

Change for change, against the ruling:
- C1 (struct field, one field, r2's comment): matches.
- C2 and C3 (one guard per rasterizer, identical comments): match. The ruling's line numbers are HEAD numbering. HEAD 767 is now 772 and HEAD 761 is now 766. Line 761 is kept.
- C5 (comment text and `d->zwrite_disabled = !zwrite;`): matches. There is no announce and no latch, and the ta_debug prints and word-2 TODOs are untouched.
- C6 and C7: `warned_nozwrite` and the "(once)" string are absent, and there are no stray hunks. The hunk offsets (+6, then +10) agree with 4+1+1 and then 4 inserted lines.
- C4 deviates in position only. The ruling says "in the settings block at 1087-1089", which is now 1093-1095, the top of that block. The diff puts the reset after the block's last line (HEAD 1130, now 1137). Section 3 says the block holds declarations only, so the two positions behave the same, and the ruling's stated reason ("precedes the command loop") holds. To settle it, read the current lines 1093-1135 for any initialiser with a side effect.

Is the fix itself right? Yes.

Lifetime of the field:
- Across strips: assigned once per type-4 header. It persists through every strip and vertex until the next header, which is the intended scope.
- Across headers: assigned, not set-only (M8 measures this).
- Across renders: cleared at 1137 on every call that gets past the render-mode check. A call that fails that check exits the process, so the field's value no longer matters.

Exit paths of the three edited functions:
- simpleline: the early return at 660 comes before the guard, then the loop runs to its end. Neither path writes the field.
- texturedline: the early return at 733; exit(1) at 874, which follows the store but ends the process; the normal end.
- pvr_render: exit at 1090, before the reset (process dies); return at 1166, after the reset and before the loop, so the field is 0; exit(1) at 1432 (process dies); the normal end.

None of these paths leaves a stale non-zero field visible to a later render.

P1 CHECKED, TRUE. Suppose every header has bit 26 clear. Then the field is 0 at the reset, and every case-4 assignment writes !1 = 0. Both guards are true, so every store HEAD makes is made, in the same order. The HEAD exit at that site never fires. Pixels and vram_z match byte for byte. The base leg (51/51) and every Z-on row agree with this.

P2 CHECKED, first half TRUE, second half unresolved.
- Case 4 handles parameter type 4, which covers polygons and modifier volumes. Nothing between 1203 and 1259 branches on listtype or `modifier`, so a modifier-volume header assigns the field from the same bit.
- My reading of the Holly ISP/TSP documentation: for modifier volumes, bits 31-29 are the volume instruction, bits 28-27 are the culling mode, and the remaining bits are reserved. If that is right, bit 26 means nothing there.
- Consequence: a modifier-volume header with bit 26 set no longer exits. Its vertices are drawn as polygons and skip depth stores. Drawing modifier volumes as polygons at all is pre-existing behaviour.
- No row covers this. To settle it: check the ISP/TSP word table in the PVR2 documentation, and run a session with a list-type-1 header that has bit 26 set and then clear, reading pixels back.

P3 CHECKED, TRUE, but the stated reason is incomplete.
- "The one early return precedes the loop" is true. It does not precede the reset, though: line 1166 comes after line 1137.
- Equivalence still holds by induction. DEVINIT zeroes the field. Under M17, every completed render zeroes it at the end. The 1166 path writes nothing, so the field is 0 at every entry either way.
- This also needs the field to have no other readers. Addendum 7(f) provides that: the rasterizers are called only from pvr_render.

2. THE FLOOR

Cells swept, with these shapes: relational operator relaxed by one, constant shifted by ±1, clause deleted, predicate replaced by 1 or 0.
- simpleline: the early return at 658-659 (four clauses), the loop at 683, the x range at 684 (M18-21), the depth test at 686, the guard at 687.
- texturedline: 731-732, 768, 769 (M22-25), 771, 772.
- pvr_render: 1088, 1158-1159, 1172, 1184, 1189 (case 4), the decode at 1235 (M31), and the reset's value and position (M9, M10, M17, M32, M33).

Shown equivalent, not gaps:
- Deleting either x-clause of the early return: every x is still filtered by 684/769.
- Weakening 1172 to `if (1)`: a leak only, because 1180 overwrites everything.
- 1184 `<` to `<=`: probably reads a zeroed slot (cmd 0 is a no-op). To settle, read pvr_clear_ta_commands and the size of the ta_commands allocation.

GAPS: eight in-bound variants that no row catches. Each dominates the edited lines by the same DEPENDS-ON rule that added the x-range rows in addendum 6.

G1. simpleline 658: `y >= d->ysize` becomes `y > d->ysize`. Row 480 is drawn at ofs = x + 480*640, outside vram_z and into VRAM past the frame. Expected red: none.
G2. simpleline 658: `y < 0` becomes `y < -1`. Row -1 is drawn at a negative ofs. Expected red: none.
G3, G4. The same two edits in texturedline at 731.
- G1-G4 are real unless pvr_render_triangle clips y. That function is not in the brief, and simpleline's own y test suggests it does not clip.
- To settle: add a session with a triangle across the bottom edge (y about 450 to 530). Read (x, 479), expecting RED, and the linear VRAM word at (480*640 + x)*2, expecting 0.
- For the top edge: set FB_RENDER_ADDR1 to 0x10000, draw across y = 0, and read fb_base - 1280 + 2x, expecting 0. Do both untextured and textured.
G5. simpleline 683: `x <= x2` becomes `x <= x2 + 1`. Every span gains one pixel on the right. No probed pixel sits at a span's x2+1: for example, T1's row 180 ends at x = 260, and the edge rows are clipped by 684. Expected red: none.
G6. The same edit in texturedline at 768.
- To settle G5 and G6: add a triangle with a vertical right edge at x = 300.0. Read (300, y), expecting drawn, and (301, y), expecting background. First confirm the rasterizer's integer x2 on the base build.
- The tightening `x < x2` is also unseen, by the same argument.
G7. pvr_render 1088: `!= 0x1` becomes `0`, or the exit is deleted. This dominates the reset and the whole render. Every session writes FB_RENDER_CFG = 1. Expected red: none. To settle: run a session with FB_RENDER_CFG = 0 and expect exit1 with "only RGB565".
G8. pvr_render 1158-1159: delete `fb_base < 0`, or shift `> VRAM_SIZE - frame_bytes` by one. This dominates the assignment at 1259 and every store. No session writes FB_RENDER_ADDR1. Expected red: none. It may already be covered by #119's own gate rows; check that block. On this detector it is a gap.

G7 and G8 are sibling or other-fix predicates. The panel may rule them out of scope under the "own disposition" disclosure. The bound as written includes them.

3. THE CHANNEL

Each row, with the variants that red it and what differs. "+B1" means the row also reds under B1 because the session dies.

Controls (13): neg apparatus, id session, id r8, zon session/rendered/prompt, zoff rendered, ovon t2 only/t1 only/bg, texon t2 only, equal t2 only, texequal t2 only.
- No enumerated variant moves any of them: CONTROL=OK on all 36 variants and on the HEAD leg. The null media move them, as predicted.
- zoff rendered is a true control only because the debug line at 1141 prints before the exit. The HEAD leg confirms it stays green.

Session and prompt rows: zoff session, zoff prompt, and the session rows of ovoff, behind, texoff, texbeh, two and sticky. Only B1 moves them (exit1, no prompt).

Pixel rows with a semantic catch:
- ovoff overlap: M1, M3, M5, M7, M31, M33, +B1. Reads 0xf800 instead of 0x07e0.
- ovoff t1 only and behind t2 only: M11, M12, +B1. Read 0x0000.
- texoff t1 only and texbeh t2 only: M11, M28, +B1. Read 0x0000.
- ovon overlap: M3, M6, M7, M15, M26, M27b. Reads 0x07e0 instead of 0xf800.
- behind overlap: M3, M6, M7, M13, M15, M26, +B1.
- texoff overlap: M2, M4, M5, M7, M31, M33, +B1.
- texbeh overlap: M4, M6, M7, M14, M16, M26b, +B1.
- texon overlap: M4, M6, M7, M16, M26b, M27. It is the only row that catches M27, so it is owed.
- two overlap: M3, M9, M10, M15, M26, M27b, M32, +B1.
- sticky overlap: M3, M6, M7, M8, M15, M26, M27b, +B1. Reads 0x001f instead of 0x07e0.
- edges l in, l out, r in, r out: M19, M18, M21, M20.
- texedges l in, l out, r in, r out: M23, M22, M25, M24.
- equal overlap: M29. texequal overlap: M30.

No row is vacuous: every non-control row reds under at least one measured variant.

Controls in disguise: eight pixel rows move only under B1, and only because the session dies. They are ovoff t2 only, ovoff bg, behind t1 only, texoff t2 only, texbeh t1 only, two t1 only, two t2 only, and sticky t2 only. Each just repeats its session's `session` row. They are correctly not flagged as controls, but they measure liveness, not the fix's semantics.

4. FALSE RECORDS (4)

F1. The probe prints "pvrrenderexit RUNG-3 WITNESS" as its banner. The file is the detector, and the gate comment says the witness "is NOT run here". The gate log therefore labels itself as the witness.
F2. The probe docstring and VERDICT.md say "the render loop has no early exit after the reset's old position". The loop contains exit(1) at 1432 and, through texturedline, at 874. PRETABLE's own wording, "no return or goto", is the true statement. Those exit(1) calls do not affect the equivalence, because they end the process.
F3. PRETABLE addendum 7(d) says "eight of its thirteen 'controls' sit in Z-off sessions". Nine do: zoff rendered sits in the zoff session. Eight are moved by B1; zoff rendered survives because the debug print comes before the exit.
F4. PRETABLE section 1 says each rasterizer has "the same dominating predicates (x in range; vram_z[ofs] <= z)". That list is incomplete. The y-range early return (658/731) and the loop bound (683/768) also dominate the stores. This omission is the source of G1-G6.

Not false, but imprecise:
- The field comment says "of the polygon being rendered"; modifier-volume headers also write the field (P2).
- The gate comment's "about half a second" has no measurement here; the base log's `elapsed` line would settle it.

5. OTHER FINDINGS, most severe first

a. The gate runs a file that table 1 did not measure. The landed regress/pvr_zwrite_probe.py cites table 1's results in its docstring, so it cannot be byte-identical to probe51_draft_frozen.py (md5 5da28a4dfcf7). To settle: diff the two files and confirm only docstring and comment lines differ. Gate 14 in situ, still running, is the base run of the landed file.
b. Gate 14 in situ has not reported. To settle: its result for this block, which must show 51/51 green.
c. The tree's dev_pvr.c has not been shown to be the dev_pvr.c.fix that was measured. To settle: md5sum src/devices/dev_pvr.c against 481755b4f10f.
d. Modifier volumes (P2) have no row. To settle: the list-type-1 session described under P2.
e. Ruling C4 says "at 1087-1089", but the reset sits at the end of the settings block. To settle: read the current lines 1093-1135. If only declarations are there, record the placement as equivalent.

CLOUDP2PVR: 3 CHECKED 4 FALSE 8 FLOOR-GAPS VERDICT:REPAIR-NEEDED
