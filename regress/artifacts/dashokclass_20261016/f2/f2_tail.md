## 6. Questions -- verdict line first, then answer each by number; say plainly what you could not check

1. **Your own findings.**  For each finding of yours in section 2: is my disposition right, and is the FIX right?
2. **The repair as material.**  Read section 4's diffs (v1 -> v2) and section 5's receipts.  Is there a path where v2
   now does something wrong that v1 did right -- for example a ledger edit a reader would call harmless that Q2 now refuses
   (beyond the note-only correction section 3 names), or an entry the identity key cannot tell apart from another?
3. **The kill table.**  Every mutant is killed by the control its line names.  Is any killed for a reason OTHER than the
   one named?  Is there a one-edit mutant of the v2 checker, renderer or Q2 block, NOT in the table, that passes all 35
   controls and breaks a ruled property?
4. **The note in the key** (section 3, first bullet): keep it, or take it out and accept the refill?  If out, what
   closes the refill instead?
5. **The baseline guard** (section 3, second bullet): md5 pin, `cmp` against HEAD, or a pinned total?
6. **Which of my accepted dispositions is wrong?**  Name the count you checked (there are 20 findings above).
