## 5. Questions -- verdict line first, then answer each by number; say plainly what you could not check

1. **Your own findings.**  For each finding of yours in section 2: is my disposition right, and is the FIX right?  A fix can
   answer the finding and still be wrong -- check the header-block awk (F1), the `grep -a` (F15), the tracked-column `$HOME`
   route (F9), and the fake's argument log (F4) against the inlined diff and driver.
2. **The repair as material.**  The repair itself owes a pass: read section 4's diff (v1 -> v2) and the v2 controls.  Is
   there a path where the v2 launcher now misclassifies something v1 classified right -- for example, a real codex header
   block the awk misses (a version line not starting `OpenAI Codex`, a rule of a different length), or a stderr where the
   strip plus `grep -a` creates a column-0 `ERROR:` on an rc-0 answer (it should be ignored there -- check)?
3. **The kill table.**  Every PINNED mutant is killed by the control its line names, and the three UNPINNED ones escape as
   recorded.  Is any pinned control killing its mutant for a reason OTHER than the one named?  Is there a one-edit mutant
   of the v2 launcher, NOT in the table, that passes all 63 controls and breaks a ruled property?
4. **Records.**  The closures (`cxlaunchquotation`, `cxlaunchdaybreak`) with witness `RECEIPT_v2.txt` and their HELD regress
   reviews; the in-place corrections (F10, F19); the filing `cxlaunchunpinned` (F13, F14).  Anything wrong?
5. **Which of my accepted dispositions is wrong?**  Name the count you checked (there are 19 findings above).
