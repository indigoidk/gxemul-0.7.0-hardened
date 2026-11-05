# Cloud routine answer, banked VERBATIM by extract_teleport.py at 2026-11-05 00:05:58Z

* source: the local transcript of `claude --teleport` -- `C:/Users/User00/.claude/projects/C--Users-User00-AppData-Local-Temp-claude-d0d925bc6bb158fc-ccd8e376-b626-4ae7-b60a-ecf2767f320e-scratchpad-tppvrdeto/dfcc1562-3d30-4d96-9f12-0a284fc3c69e.jsonl`
* session: `https://claude.ai/code/session_015fEQzHge81CbKHgEEfrkwg`   trigger: `trig_01UcwBcvFB8y9WmvDcBx5Ntw`   packet: `_scratchpad/w_pvr/PVRDET_cloud.md`
* the answer's message: timestamp 2026-11-05T00:03:18.549Z, model field `claude-opus-5-5` (all assistant models in the transcript: ['claude-haiku-5-5', 'claude-opus-5-5'])
* delivery token `CLOUDPVRDET`: present; 7775 characters; PART markers N = 0, present 0, MISSING none; `END OF PARTS`: NO
* safety-classifier notices in the transcript: none
* the run's final line: CLOUDPVRDET: 6 RULINGS 1 WRONG 2 GAPS VERDICT:CHANGE-FIRST

---
CLOUDPVRDET
model: claude-opus-5-5 (the configured ID; the model actually serving this turn may differ)
VERDICT: CHANGE-FIRST. Before the table runs, add two equal-depth sessions (`eq`, `texeq`) and three variants (M26, M27, M28_hoist_tex). Do not mark the eight Z-off-session "controls" as controls. `texon` is excess. Settle M10 by a grep before the run.

## 1. The added sessions

| Session | Ruling | Rule and reason |
|---|---|---|
| R6 `behind` | **OWED** | It is the joint cell (Z-write off, depth fail) in simpleline. It is the only row that catches M13 (`<= z \|\| zwrite_disabled`), which weakens the depth predicate the store depends on. It also backs the comment "depth test kept". |
| R7 `texbeh` | **OWED** | It is the same cell in texturedline (sibling parity). It is the only row that catches M14, and with `texoff` it is one of two rows for M11 in the textured rasterizer. |
| R7 `texon` | **EXCESS** | Its red set {M4, M6, M7, M16} is entirely inside `texbeh overlap`'s red set, because texbeh's T1 is a Z-write-on textured polygon. No enumerated variant reds texon alone. Under "one row per enumerated wrong edit" it adds nothing, so drop it. In fairness, my R3 (`ovon`) is now also covered by `behind`. I keep R3 only because I ruled it as the "Z-write-on render matches HEAD" check. That is not a rule that makes texon owed. |
| R8 `sticky` | **OWED** | This is the state where the field and the body disagree: one header sets the field, then a later Z-write-on header in the same render should clear it. It is the only row that catches M8 (a set-only assignment). |
| R9 `edges`, `texedges` | **OWED** under D2 as the addendum writes it | `x > 0 && x < d->xsize` dominates both guarded stores, so it is a predicate the edited lines depend on. The rule allows at most two rows per compare. Four rows per rasterizer covers two compares, so it is within the limit. Note that both sessions are Z-write on: they measure code that existed before the fix and read the same on HEAD. That is consistent with the 21/47 HEAD prediction, but it is also why the equal-depth exclusion below cannot stand. |

## 2. Predictions, re-derived (z kept when `vram_z <= z`; T1 at z = 2.0, T2 at z = 1.0, background cleared)

- **B1_exit:** every session with a Z-write-off header dies. Red rows: zoff session and prompt (2); ovoff, 4 pixels plus session (5); behind (4); texoff (4); texbeh (4); two (4, because render 1 carries the Z-off header); sticky (3). Total 26 red. `zoff rendered` stays green because the debug line prints at entry, before case 4 runs. Score 13/39, then **21/47**. ✓
- **M3_simple_inv:**
  - ovoff: T1 stores, so overlap reads red.
  - ovon: T1 stores nothing, so T2 shows green over it.
  - behind: T1 is Z-on, stores nothing, and T2 draws over it.
  - two: render 2 has the flag at 0, so T1 stores nothing, which gives green.
  - sticky: the final flag is 0, so green T1 stores nothing and blue T2 draws over it.
  - texoff overlap stays green: T1 goes through texturedline, and T2 is drawn last.
  - Five red, **42/47**. ✓
- **M7_assign_inv:**
  - ovoff: T1 gets 0 and stores, so red.
  - ovon: both polygons get 1, so green.
  - behind: T1 gets 1 and stores nothing, so T2 draws green.
  - texoff, texbeh and texon follow the same pattern.
  - sticky: the last header gives 1, so T1 stores nothing and blue shows.
  - two: the reset gives 0, so red, as wanted.
  - Seven red, **40/47**. ✓
- **M6_assign1:** ovon, behind, texbeh, texon and sticky go red. ovoff stays green, as wanted. The edge triangles do not overlap, so they stay green. **42/47.** ✓
- **M9_noreset:** render 2 inherits 1, so T1 stores nothing and `two overlap` reads green. Every other session starts cold from DEVINIT's memset. **46/47.** ✓
- **M11_decline:** `ovoff t1` and `texoff t1` read black, and `behind t2` and `texbeh t2` read black. The overlaps keep their wanted colours, because a declined T1 leaves T2 green, and a declined T2 leaves T1 red. **43/47.** ✓
- **M8:** sticky overlap reads 0x001f. ✓
- **M15:** ovon, behind, two and sticky go red. ✓
- **M20 and M24:** the pixel at x = 640 on row 330 is ofs 331·640, which is (0, 331), and reads red. ✓
- **M17** is equivalent, as argued. ✓
- **At risk: M10_reset_in_resetta.** The prediction holds only if `pvr_reset_ta()` is not on the STARTRENDER/render path. The fix scoring `two overlap` as red proves that render 2 did not re-run render 1's Z-off header, so something clears the TA list between renders. If that something is `pvr_reset_ta()`, then M10 resets the flag between renders and is equivalent, so it should be predicted undetected (47/47). How to settle it: grep for callers of `pvr_reset_ta`, and read the second "%i Tile Accelerator commands" line in the `two` transcript (6 means the list was cleared).

## 3. The controls

Eight of the 13 declared controls are in B1's own red set: ovoff t2 only, ovoff bg, behind t1 only, texoff t2 only, texbeh t1 only, two t1 only, two t2 only, sticky t2 only. They all sit in Z-write-off sessions that B1 kills. That breaks section 4's definition of a control ("never movable by an enumerated variant").

Marking them `control=True` before landing has two effects:
- The HEAD leg would report `CONTROL=FAIL` next to `SYMPTOM=PRESENT`, so it could no longer tell "apparatus broken" from "defect present".
- B1 would read as an apparatus failure.

None of them is the only row that catches anything, since the session rows already catch B1. The remaining five are genuine controls: zoff rendered, ovon t1 only, ovon t2 only, ovon bg, texon t2 only. The last one goes if texon is dropped. Settle this by running the HEAD leg with the planned flags; I expect `CONTROL=FAIL`. Every detector row moves under some enumerated variant except `two overlap`, which is in doubt only if M10 turns out equivalent; then M9 alone catches it.

## 4. Missing variants

- **M26_simple_lt:** in simpleline, change `d->vram_z[ofs] <= z` to `d->vram_z[ofs] < z`. Expected red: **none**. No session draws two overlapping triangles at the same z. This is a gap.
- **M27_tex_lt:** the same change in texturedline. Expected red: **none**. Also a gap.
  - PRETABLE §3 excludes this edge because the compare "is between two variables, not a constant bound". But `x < d->xsize` also compares two variables, and the addendum's D2 is not limited to constant bounds. M19 and M21 (tightenings) set the precedent that a tightening is in bound.
  - Rows owed: `eq` (untextured, Z-on red T1 at z = 2.0, then Z-on green T2 at z = 2.0 overlapping; overlap should read 0x07e0, and reads 0xf800 under M26) and `texeq` (the same with red and green texels).
- **M28_hoist_tex:** the texturedline version of M12. It is missing by section 1's own parity rule, but rows already catch it: `texoff t1 only` and `texbeh t2 only`, for **45/47**.

## 5. Other findings, by severity

1. **(High)** The control marking in §3. Measure it with the HEAD leg after flagging.
2. **(Medium)** The M10 prediction may be wrong. Settle it with the grep and the transcript count above. If M10 is equivalent, record it as equivalent, not as a gap.
3. **(Low)** `RENDERED = "1 Tile Accelerator commands"` also matches "11 …" or "21 …" as a substring. It is harmless today because only the single-command sessions test it. Anchor it with `\b1 Tile` or the debug prefix. The measurement is a session that submits 11 commands.
4. **(Low)** The `eq` rows assume z stays exactly constant across a triangle with equal vertex z. The fixed build scoring `eq overlap` as 0x07e0 settles it; if it doesn't, the equal edge can't be reached this way and should be disclosed instead.
5. **(Note)** Argon's gap is closed: R9 catches deleting the bound through `l out` and `r out`.

CLOUDPVRDET: 6 RULINGS 1 WRONG 2 GAPS VERDICT:CHANGE-FIRST
