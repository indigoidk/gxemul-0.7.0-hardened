ASTRA CONFIRMATION of a Fable adjudication -- `batch1b`

Open with the token `ASTRACONFIRM_BATCH1B_ALIVE` on its own line, then ONE verdict line:
`VERDICT: <w> of <n> dispositions wrong (<m> more need a change of wording or severity)`

**Context.**  GPT-6 Astra reviewed parts of this GXemul fork read-only (the "answers" below).  The Fable seat then
ADJUDICATED every finding in those answers against the source: CONFIRMED-FILED (already in the queue), CONFIRMED-NEW
(a new queue row, with a severity), RECORD-L4 (a false comment or record, with replacement text), TEST-GAP-FILE,
REFUTED, UNSETTLED or DUPLICATE.  The project owner has ruled that GPT-6 Astra confirms or overturns the Fable
seat's dispositions before anything is filed or corrected.  Nothing is fixed here; this decides what the queue says.

**Please do not simply ratify.**  The question is: **WHICH OF FABLE'S DISPOSITIONS IS WRONG?**  Check each against the
committed tree (`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show HEAD:<path>`; the working tree carries uncommitted
work that is not under review; ignore every other `src/` under the project root).  In particular:
- a REFUTED finding whose refutation is itself wrong is the most expensive error here -- it hides a live defect;
- a CONFIRMED-FILED whose id does not exist in `OUTSTANDING_BUGS.md` at HEAD, or names a different defect;
- a RECORD-L4 whose replacement text is itself false of the code;
- a severity that is too low (a guest can end the emulator process, touch memory outside a buffer, or hang it = HIGH);
- a CONFIRMED-NEW that duplicates an existing row.

**The adjudication:** ``C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\adjudication\fable_batch1b.md``
**The answers it adjudicated:** `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\bundle_include1\codex_bundle_include1.txt`, `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\bundle_include2\codex_bundle_include2.txt`

**For each disposition you overturn or amend, one block:**
`<job>:F<n> | Fable said <X> | should be <Y> | the evidence (path:line at HEAD, or the queue line) | confidence`

Then list the dispositions you checked and found right (ids only is fine), and end with
`DENOMINATOR: checked <c> of <n> dispositions against the source`.

Read-only: write nothing, build nothing, run nothing that changes a file.
