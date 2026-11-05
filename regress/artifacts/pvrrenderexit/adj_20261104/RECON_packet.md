Begin your answer with the token CLOUDRECON_PVR on its own line, then `model: <your model name>`, then your verdict line.  Do not
call any tool and do not write files; answer in plain text.

# RECONCILIATION -- `pvrrenderexit`: your two final rulings on the same packet (Claude Code Cloud; Fable 5.1)

**Framing.**  GXemul is a computer-architecture emulator (a developer tool that runs legacy operating systems in a software sandbox); this fork
is a software-correctness hardening effort, and every fix ships with a regression test.  Plain correctness language, please.

**What happened.**  You gave the final design ruling on this bug twice, from the same packet, in two independent Claude Code Cloud runs: r1
(the ruling of record) and r2 (a replication).  Their verdicts agree; their change and row lists differ.  The main loop implements ONE fix and
ONE row list, and it records and does not rule -- so the reconciliation is yours.  Below are sections 2-4 (the ruling, the fix, the rows) of r1 and sections 2-4 (the ruling, the fix, the rows) of r2.  You have no
repository: cite the rulings' own items; mark claims CHECKED-IN-PACKET, REASONED or UNSETTLED.

**Answer, VERDICT LINE FIRST (`VERDICT: R1-STANDS | MERGE | R2-SUPERSEDES`), in this order -- keep it compact; code only where it changes:**
1. Every difference between r1 and r2 (disposition, code, comment sentence, row, filed item), one line each, citing each ruling's item.
2. For each: OWED (r1 is wrong or incomplete without it -- quote the r1 sentence), OPTIONAL (wording, or a row another row already covers --
   name it), or WRONG (quote the line it contradicts).  Where they CONFLICT, both sides in a line and which argument is stronger and why.
3. THE MERGED FIX: the exact final code for every hunk that differs from r1's, every product comment TRUE AS WRITTEN; say "r1 as written"
   for each hunk that does not change.
4. THE MERGED ROWS: the final row list (session, guest action, want, the wrong edit each catches), within "rows per enumerated wrong edit".
5. The weakest of these reconciliation rulings, and what would overturn it.
Final line: `CLOUDRECON_PVR: <d> DIFFERENCES <o> OWED <c> CONFLICTS <r> ROWS VERDICT:<R1-STANDS|MERGE|R2-SUPERSEDES>`

---

## r1 -- the ruling of record (FABLE_FINAL.md)

```
2. RULING R1, the disposition: 7 IMPLEMENT.
Warrant (CHECKED-IN-PACKET): the exit at LIST:1243-1246 ends the emulator process on one guest display-list bit, and C shows it from an unmodified -E dreamcast with real SH-4 stores (7/9, controls OK, status 1). That is the robustness defect. The bit's meaning is already encoded by the source itself: `zwrite = !((list[1] >> 26) & 1)` at LIST:1225 names bit 26 as the Z-write DISABLE bit (REASONED that this matches the PVR2 ISP/TSP word; the source agrees with that reading). A polygon with it set is an ordinary polygon that must not update the depth buffer. The implementation is one guarded store per rasterizer, and D measures it doing exactly that: T1 still RED at its own pixel, overlap GREEN, enabled render pixel-identical to HEAD.

R1 continued: why not the other menu items.
1 DELETE and 2/3 DECLINE would stop drawing the polygon. D shows the draft draws it and the guest can see the difference (T1-only pixel RED vs black), so decline is a visible wrong image for a cheaper diff. 5 FAULT is wrong: the bit is a legal guest input, not an error. 6 BACKED ACCEPT (accept the bit, store depth anyway) is the "unguarded store" column in D: overlap RED, which is the wrong image. 7 is the only disposition whose output matches the hardware meaning, and it is two lines of guard. CHECKED-IN-PACKET via D.

R2, the DISPUTED per-render reset: OWED. Status REASONED (the second render is HELD and separately routed; its measurement would make this CHECKED).
Both sides: GLM says each type-4 header assigns the flag before its triangles consume it, so no reset is needed. Grok's source check says a cmd-7 vertex draws when listtype is 0, 2 or 4, listtype is initialised to 0 per call, and the flag is a struct field that nothing zeroes after device init. If that check is accurate, a later STARTRENDER whose list carries vertices before any type-4 header inherits the previous render's flag, and those vertices silently skip depth stores. The ruling turns on whether a vertex command can draw without a header in the same call; grok's reading of 1089 plus 1307 says yes, GLM offers no line that says no.

R2 continued, the warrant beyond that dispute.
Even if GLM were right about today's command loop, the field is per-polygon state living in per-device storage, and every other per-polygon setting in pvr_render (listtype, texture, cullingmode) is re-initialised per call at RENDER:1089. The flag must follow the same rule or it is the one setting that leaks across renders. A reset at the per-call settings block is correctness by construction, costs one store, and makes the HELD measurement a confirmation rather than a gate. Insertion point: the per-call settings block (next to `listtype = 0`), not pvr_reset, not the depth clear. warned_nozwrite is removed (R3), so nothing else stays latched.

R3, the once-latched announce: DROPPED (Opus (b) side).
Warrant: the announce describes a limitation, and after this fix there is none. The bit is implemented, so a message saying the device is doing something unusual is false as a product statement. Observability of the bit already exists at LIST:1235 under ta_debug (CHECKED-IN-PACKET), which is the right place for "this polygon has Z-write off". Keeping the announce would add a field, a latch, and two owed rows (fires once, never fires when enabled) for no behaviour. If the project has a house rule that every removed exit leaves a once-announce, the User00 session overrides this (see section 7).

R4, the literal diff: REJECTED, the AFTER image is the design.
Warrant: Opus (a) and three share-findings seats read the third hunk as deleting the live `double z = z1, u = u1, v = v1;` at 761 and inserting a duplicate `int textureofs; if (twiddled) {`, which cannot compile. Hunks 2 and 4 re-add text already present (fogv comment at 693, the zwrite/texture1 prints at 1235-1236) and hunk 4 deletes the word-2 TODOs. D was measured on apply_draft.py's AFTER image, not the hunks, so the pixels vouch for the AFTER image only. Status: REASONED from four concordant readings of lines I cannot see; a compile of the literal hunks would make it CHECKED.

R5, the background depth fill at 1171 stays UNCONDITIONAL (grok's "other" note). The fill is the per-render depth clear, not a polygon store; guarding it with the flag would let a Z-write-off polygon from a previous render poison the next frame's clear. REASONED (line 1171 omitted).
R6, the comparator: keep `if (d->vram_z[ofs] <= z)` untouched and the guard INSIDE it. The depth test is unchanged for every polygon; only the store is conditional. CHECKED-IN-PACKET via D (enabled render pixel-identical to HEAD).

3. THE FIX. Seven changes; the diff is regenerated from the AFTER image, not patched on top of the hunks.
C1 struct pvr_data, one field only (warned_nozwrite is not added):
'''
    int            zwrite_disabled;    /*  #NNN: Z-write-disable bit of the
                                           polygon currently being rendered.
                                           Reset at each pvr_render call;
                                           set by each type-4 header.  */
'''
(#NNN is the bug id, to be filled by the User00 session before commit.)

C2 simpleline (the first rasterizer), the guard inside the existing test; nothing else in the function changes, no fogv comment added:
'''
            if (d->vram_z[ofs] <= z) {
                if (!d->zwrite_disabled)    /*  #NNN: depth test kept, store skipped  */
                    d->vram_z[ofs] = z;
'''
C3 texturedline (the second rasterizer): keep line 761 `double z = z1, u = u1, v = v1;` exactly; add no second `int textureofs; if (twiddled) {`; the only edit is the same guard at the store (767), inside `if (d->vram_z[ofs] <= z)`, with the same comment.

C4 pvr_render, the per-call reset, in the "Settings for the current polygon being rendered" block at RENDER:1087-1089, beside the other per-call initialisations:
'''
    // Settings for the current polygon being rendered:
    int listtype = 0;  ...
    d->zwrite_disabled = 0;    /*  #NNN: per render; a type-4 header
                                   in this call may set it  */
'''
Not in pvr_reset, not next to the depth clear at 1171 (either would work for correctness; this placement keeps every per-polygon setting in one block).

C5 pvr_render, the exit replaced. The ta_debug prints at 1232-1241 are NOT touched (no re-added zwrite/texture1 lines). The TODOs at 1255-1256 are kept. The replacement, every sentence true as written:
'''
            /*  #NNN: ISP/TSP instruction word 1 bit 26 is "Z-write disable".
                A polygon with the bit set goes through the same depth test
                and rasterization as any other polygon, but its depth values
                are not stored.  Both rasterizers check d->zwrite_disabled
                at their vram_z stores.  Before #NNN this bit ended the
                emulator with fatal() + exit(1).  */
            d->zwrite_disabled = !zwrite;
'''
No announce, no latch.

C6 remove from the draft: the `warned_nozwrite` field, the `if (!zwrite && !d->warned_nozwrite) { fatal(...) ... }` block, the "(once)" string. If the User00 session keeps the announce (house rule), the string must read `[ pvr: polygon with Z-write disabled; depth test kept, depth store skipped (announced once) ]` and the comment's "Announced once per device" stays; otherwise both go.
C7 the diff hygiene list, consolidated rows 1-4: no fogv comment, no zwrite/texture1 prints, keep both word-2 TODOs, keep line 761. Applying the packet's fenced hunks on top of the AFTER image would reintroduce the broken texturedline edit (grok), so the hunks are discarded, not merged.

4. ROWS OWED. The enumerated wrong edits: (a) exit retained; (b) DECLINE instead of draw; (c) store unguarded; (d) enabled path broken, e.g. guard inverted; (e) only one rasterizer guarded; (f) no per-render reset. Four rows cover them, at most one row per wrong edit beyond the shared channel.
ROW 1 (covers a, b, c). Session: one cold -E dreamcast, the D channel. Guest action: FB_RENDER_CFG=1; header with list word 1 = 0x04000000; NEAR red T1 (z 2.0); header with word 1 = 0; FAR green T2 (z 1.0) overlapping; STARTRENDER; read back four pixels. Want: exit 0; overlap (220,180) 0x07e0; T2-only 0x07e0; T1-only (120,120) 0xf800; background 0x0000. Catches: (a) exit 1; (b) T1-only 0x0000; (c) overlap 0xf800.

ROW 2 (covers d). Same session and triangles, both headers word 1 = 0. Want: overlap 0xf800, T2-only 0x07e0, T1-only 0xf800, exit 0, identical to HEAD's enabled row in D. Catches an inverted guard (`if (d->zwrite_disabled)`), which would turn the overlap GREEN, and any regression of the untouched path.
ROW 3 (covers f, the HELD measurement). Session: one cold session, TWO STARTRENDERs. Render 1: Z-write-off header + T1, as ROW 1. Render 2: cmd-7 vertices only, no type-4 header, NEAR T1 then FAR T2. Want: render 2 overlap 0xf800 (flag reset, T1's depth stored, T2 loses the test). Catches a missing reset (overlap 0x07e0). UNSETTLED prerequisite: that a header-less cmd-7 list draws with a visible colour; if it does not, render 2 instead opens with a Z-write-ON header and the row then only guards the "header re-sets the flag" path, and (f) stays measured by inspection.

ROW 4 (covers e). Session: one cold session. Guest action: a TEXTURED Z-write-off NEAR polygon (texture bit, list word 0 bit 3, with a trivially filled texture in VRAM) then the untextured FAR green T2 over it. Want: overlap 0x07e0 and exit 0. Catches a fix that guards simpleline only (overlap keeps the textured colour). UNSETTLED: the channel does not yet build a textured polygon; the row is owed, and if the texture setup proves too costly this round it is FILED against the fix with the SIB1 texture work, not dropped.
Plus: rerun regress/pvr_zwrite_probe.py (md5 a2a7496922d2) on the committed fix; want 9/9 CONTROL=OK SYMPTOM=ABSENT, as D already shows for the AFTER image.

```

## r2 -- the replication (FABLE_FINAL_r2.md)

```
2. THE RULING. Disposition: 7 IMPLEMENT. Z-write disable is honoured at both vram_z stores; the exit goes; no announce.
Warrant A (REASONED; corroborated by the source's own decode at 1223-1230): ISP/TSP instruction word 1 is depth mode in bits 31-29, culling in 28-27, Z-write DISABLE in bit 26, texture in 25. The source already parses exactly this layout and names the bit zwrite. Bit 26 means: run the depth test, draw where it passes, do not store depth. It is how a guest submits translucent polygons so they do not occlude one another. It is ordinary, legal display-list input, not a fault.

Warrant B (CHECKED-IN-PACKET, D): the implementation is observable and complete with respect to the bit. zon: pixel-identical to HEAD (overlap RED, T2-only GREEN, T1-only RED, background 0). zoff: the process survives, T1 is still drawn (T1-only RED), no depth is stored for it (overlap GREEN). The probe moves from 7/9 PRESENT to 9/9 ABSENT.
Warrant C, the rest of the menu: 1 DELETE (drop the exit, keep the store) is the unguarded store, overlap RED on zoff, wrong occlusion. 2 and 3 DECLINE blank every Z-write-off polygon, which is most translucent geometry, when the correct behaviour costs two guarded stores. 4 and 6 ACCEPT without a guard are DELETE by another name. 5 FAULT punishes a legal bit. Only 7 produces output that matches the bit's meaning.

Ruling on the DISPUTED per-render reset: REQUIRED, placed at pvr_render entry in the "Settings for the current polygon being rendered" block (1087-1089), not in pvr_reset. Warrant: (a) the draft's flag is device state with exactly one writer, the type-4 header case, and nothing zeroes it after the init memset (F; REASONED on cited lines 1447-1450 and 2673). (b) grok's source check: listtype starts at 0 and case 7 draws for listtype 0, 2 or 4, so a later STARTRENDER whose list is bare cmd-7 vertices inherits the previous render's flag and skips depth stores (REASONED, one seat's reading; UNSETTLED until the HELD measurement). (c) Independent of (b): every sibling per-polygon setting (listtype, texture, cullingmode, color_type) is initialised at entry; store-enable is the same kind of state. GLM's "each header re-sets it" holds only for lists that carry a header.

Ruling on the announce: DROP it and delete warned_nozwrite. Warrant: the behaviour is implemented completely with respect to the bit, so nothing partial remains to announce; ta_debug already prints "zwrite false" per header (1235); a stderr line on an ordinary translucent-polygon bit fires in every title that draws one; the latch adds a field and owes two rows (exactly once across two Z-off polygons; zero in zon). Grok's row 6 and Opus (b)'s wording objection become moot. A project convention could override this; see part 31.

Answer to the draft brief's own question (is the flag current at every per-triangle call, and is it reset between frames). Within one render: yes. CHECKED-IN-PACKET for the AFTER image: the header case is the only writer, and every triangle of a strip is rasterized after its header and before the next header. Between renders: no, as drafted. Change 6 below supplies the reset. The HELD second-render measurement (row R5) tests exactly this; the ruling does not wait for it, because the reset is correct whether or not the leak is reachable on this tree.

3. THE FIX. Base: regenerate the diff from the AFTER image (apply_draft.py). The packet's literal hunks are NOT the fix; applying them on top of draft.diff puts the broken texturedline edit back (F). Line numbers are dev_pvr.c at HEAD as cited by E and F.
CHANGE 1 (texturedline): keep line 761
'''
double z = z1, u = u1, v = v1;
'''
and do not insert a second `int textureofs; if (twiddled) {` before the existing pair at 777-778. The only edit in texturedline is the store guard, change 9.

CHANGE 2: no added fogv comment; the one at 693 stays single.
CHANGE 3: no added `fatal("zwrite %s, ", ...)` and `fatal("texture1 %s\n", ...)`; the pair at 1235-1236 inside the ta_debug block stays single.
CHANGE 4: keep lines 1255-1256
'''
// TODO: srcblend (31-29)
// TODO: dstblend (28-26)
'''
Blending is still unimplemented, so both TODOs remain true and stay.

CHANGE 5 (struct pvr_data): add exactly one field; do not add warned_nozwrite.
'''
    int        zwrite_disabled;    /*  #NNN: ISP/TSP word 1 bit 26 of the
                        polygon being rendered.  When set, the
                        rasterizers skip their vram_z stores.
                        Cleared at every pvr_render entry.  */
'''
Every clause is true as written once changes 6 to 9 are in: one writer per header, two readers at the stores, one clear at entry.

CHANGE 6 (pvr_render, in the "Settings for the current polygon being rendered" block at 1087-1089, before the command loop):
'''
    //  #NNN: Z-write enable is per polygon and must not survive from one
    //  render to the next (a list of bare vertex commands carries no
    //  header to set it), so every render starts with depth stores enabled.
    d->zwrite_disabled = 0;
'''
Not in pvr_reset: it is not called between STARTRENDERs. Not beside the depth clear at 1170-1171: entry cannot be bypassed by any path between 1089 and the loop (whether such a path exists is UNSETTLED; entry makes it moot). The field stays in the struct because both rasterizers already receive d; a render-local would add a parameter to two helpers for the same behaviour.

CHANGE 7 (pvr_render, replace lines 1243-1246, the fatal and exit):
'''
    /*  #NNN: ISP/TSP instruction word 1 bit 26 is Z-write DISABLE.  The
        polygon takes the same depth test as any other polygon and, where
        the test passes, is drawn, but it must not update the depth buffer.
        The rasterizers check d->zwrite_disabled at their vram_z stores.
        This used to be fatal() + exit(1) on a guest display-list bit.  */
    d->zwrite_disabled = !zwrite;
'''
True as written: the test is this renderer's single `<=` comparison, the same for every polygon; "where the test passes" is Codex's row-7 correction; the two stores are the only readers. The zwrite local stays because the ta_debug print at 1235 uses it.

CHANGE 8 (simpleline, the store at 683) and CHANGE 9 (texturedline, the store at 767), identical text, inside the existing `if (d->vram_z[ofs] <= z) {`:
'''
                if (!d->zwrite_disabled)    /*  #NNN  */
                    d->vram_z[ofs] = z;
'''
The colour store that follows is untouched, so a Z-write-off polygon is still drawn. The background depth fill at 1171 stays unconditional: it is the render's depth clear, not a polygon store. vram_z has no fourth writer (F).

Fix summary: 9 changes. Changes 1-4 repair the literal diff back to the measured AFTER image. Changes 5-9 are the design: one field, one reset at entry, one assignment with its comment in place of the exit, two guarded stores. Removed from the draft: the announce and its latch field. Removed from HEAD: the fatal and exit at 1243-1246. Nothing else in dev_pvr.c moves. The measured AFTER image differs from this text only by the announce, the latch field and the reset, so D's zon and zoff pixels are expected unchanged; R2 and R3 confirm that on the committed fix.

4. ROWS THE FIX OWES. Bound: one row per enumerated wrong edit; two measured rows cover three wrong edits between them. Channel conventions from C and D: cold -E dreamcast, unmodified in-tree; every access a real SH-4 mov.l; FB_RENDER_CFG = 1 at 0xa05f8048; TA list at 0xb0000000, the write at 0x1c submits a header; STARTRENDER at 0xa05f8014; pixels read at 0xa5000000 + (y*640 + x)*2, RGB565.
ROW R1 (exists: regress/pvr_zwrite_probe.py, md5 a2a7496922d2). Session zoff: one header with word 1 = 0x04000000, one triangle, STARTRENDER. Want: 9/9, CONTROL OK, SYMPTOM ABSENT, exit 0, no "no zwrite" line. Catches: the exit left in place, or any new exit on bit 26.

ROW R2 (measured in D on the AFTER image). Session zoff-overlap: header word 1 = 0x04000000, NEAR red T1 at z = 2.0; FAR green T2 at z = 1.0 overlapping T1; STARTRENDER. Want: exit 0; overlap (220,180) = 0x07e0; T2-only (320,180) = 0x07e0; T1-only (120,120) = 0xf800; background = 0x0000. Catches: the unguarded store (menu 1, overlap 0xf800); DECLINE (T1-only 0x0000); an inverted guard (overlap 0xf800); a guard hoisted outside the depth test (T1-only 0x0000). Whether T2 carries its own header is immaterial to these four pixels, since nothing draws after T2.

ROW R3 (measured in D). Session zon-overlap: the same geometry with word 1 = 0 on the header. Want: exit 0; overlap 0xf800; T2-only 0x07e0; T1-only 0xf800; background 0x0000; pixel-identical to HEAD. Catches: an inverted guard (T1 stores nothing, overlap 0x07e0); any edit that broke the Z-write-on store. R2 and R3 together pin the guard's sense: R2 fails on an unguarded store, R3 fails on an inverted one.

ROW R4 (owed, NOT measured: the texturedline store, change 9). Session zoff-textured: R2's geometry with T1 textured: List Word 0 bit 3 set (texture = list[0] & 8), a texture word pointing at a small solid-red texture written to VRAM in a pixel format the switch at 866 implements (UNSETTLED which: 850-870 is omitted; a format it does not handle hits SIB1 first), word 1 bit 26 set. Want: exit 0; overlap 0x07e0; T1-only the texel colour, 0xf800; background 0x0000. Catches: change 9 missing (only simpleline guarded, overlap 0xf800) and the literal hunk 3 (does not compile). One row, because this is one wrong edit.

ROW R5 (the HELD second-render measurement; owed by change 6). Session two-renders: render 1 = header word 1 = 0x04000000 plus one triangle away from the probe pixels, STARTRENDER; render 2 = bare cmd-7 vertices with no type-4 header: NEAR red T1 at z = 2.0 then FAR green T2 at z = 1.0 overlapping, STARTRENDER; read the four pixels after render 2. Want: overlap 0xf800; T1-only 0xf800; T2-only 0x07e0. Catches: no reset, or a reset in pvr_reset only (render 1's flag leaks into render 2, overlap 0x07e0). Void condition: if T1-only reads 0x0000, headerless vertices do not draw on this tree; the leak is then unreachable, the reset stays as defense, and R5 is recorded as void rather than rewritten, because a render-2 list with a header cannot discriminate.

Rows summary: 5 rows. Two measured (R2, R3), one existing (R1), two to build (R4, R5). Wrong edits enumerated and their catcher: exit kept (R1); unguarded store (R2); DECLINE (R2); inverted or hoisted guard (R2 and R3); second rasterizer unguarded, or hunk 3 applied (R4); no per-render reset (R5). If a later ruling reinstates the announce, it owes two further rows: zoff with two Z-off headers prints the line exactly once; zon prints it zero times.

```

Now write the reconciliation in the order given at the top.
