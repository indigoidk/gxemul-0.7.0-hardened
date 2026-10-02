ASTRA CONFIRMATION of a grok-seat adjudication -- `3f`

Open with the token `ASTRACONFIRM_3F_ALIVE` on its own line, then ONE verdict line:
`VERDICT: <w> of <n> dispositions wrong (<m> more need a change of wording or severity)`

**Context.**  GPT-6 Astra reviewed parts of this GXemul fork read-only (the "answers" below).  The grok seat (grok-4.7, xhigh -- a different model family from the review) then
ADJUDICATED every finding in those answers against the source: CONFIRMED-FILED (already in the queue), CONFIRMED-NEW
(a new queue row, with a severity), RECORD-L4 (a false comment or record, with replacement text), TEST-GAP-FILE,
REFUTED, UNSETTLED or DUPLICATE.  The project owner ruled on 2026-10-02 that the working seats are GPT-6 Astra, agy and grok (the Fable
seat was deliberately not fired on this batch): GPT-6 Astra confirms or overturns the grok seat's dispositions before
anything is filed or corrected.  Nothing is fixed here; this decides what the queue says.

**Please do not simply ratify.**  The question is: **WHICH OF THE GROK SEAT'S DISPOSITIONS IS WRONG?**  Check each against the
committed tree (`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show HEAD:<path>`; the working tree carries uncommitted
work that is not under review; ignore every other `src/` under the project root).  In particular:
- a REFUTED finding whose refutation is itself wrong is the most expensive error here -- it hides a live defect;
- a CONFIRMED-FILED whose id does not exist in `OUTSTANDING_BUGS.md` at HEAD, or names a different defect;
- a RECORD-L4 whose replacement text is itself false of the code;
- a severity that is too low (a guest can end the emulator process, touch memory outside a buffer, or hang it = HIGH);
- a CONFIRMED-NEW that duplicates an existing row, in `OUTSTANDING_BUGS.md` or in
  `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\DISPOSITIONS.md` (this campaign's earlier rulings: twelve batches).
You wrote the findings and a sibling of yours wrote the draft the grok seat had in view, so be hardest where the
ruling AGREES with that draft, and say so where the grok seat changed it and was wrong to.

**The adjudication:** ``C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\adjudication\grok_20261002\grok_rule3f.txt``
**The answers it adjudicated:** `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\devne2000\codex_devne2000.txt`, `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\netip\codex_netip.txt`, `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\net\codex_net.txt`, `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\bundle_net\codex_bundle_net.txt`, `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\devjazz\codex_devjazz.txt`

**For each disposition you overturn or amend, one block:**
`<job>:F<n> | grok said <X> | should be <Y> | the evidence (path:line at HEAD, or the queue line) | confidence`

Then list the dispositions you checked and found right (ids only is fine), and end with
`DENOMINATOR: checked <c> of <n> dispositions against the source`.

Read-only: write nothing, build nothing, run nothing that changes a file.
