THE 40 CLOSURES -- a read-only check by the agy seat that each "already fixed" really is

Open your answer with the token AGY_CLOSURES_ALIVE_1002 on its own line.  SECOND line, exactly in this form:
VERDICT: <r> closures right, <w> wrong (the defect is still in the source), <u> not settled by reading, of 40 closures

You are one seat of a review panel for a C emulator fork (GXemul, hardened).  READ-ONLY, always: write no file, run
nothing, build nothing, change nothing anywhere.  Your only output is the text you print.

CONTEXT.  The project's queue file, OUTSTANDING_BUGS.md, carries some entries in prose with no short id.  Three seats
went through them; the result is
C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\idless_20261002\IDLESS_DISPOSITIONS.md
Near its end, under the heading "THE CLOSE-RECORD ENTRIES (40)", it lists 40 entries where the ruling is: the queue
text still says OPEN, but the committed source shows the defect is GONE, so the text is to be replaced.  A closure is
the costly direction -- a WRONG closure hides a defect that is still there -- so each one gets an independent check,
and that is your job.  Your agreement carries no weight; a file and line that contradicts a closure does.

THE TREE.  C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC (git).  The queue line numbers in that list are those of commit
db8b1a33: read the queue text with
  git -C C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC show db8b1a33:OUTSTANDING_BUGS.md
and the source at the same commit (git ... show db8b1a33:<path>, with grep -n or awk for line numbers).  Never read
C:\DocumentNoSnc\cc\GXEMUL\src, est, build, build-asan or _archive: they are other copies and their line numbers differ
by hundreds.  Never run git status or git diff.

FOR EACH OF THE 40 ENTRIES (each line of the list gives: slice | queue lines | whose line governs | the governing line):
 1. read the queue lines it names: what defect or owed work does the entry record?
 2. read the source lines the governing line cites as the fix, and the place the defect lived: is the defect GONE
    from the committed source, or STILL THERE (in whole or in part)?
 3. is the replacement sentence the governing line proposes TRUE of the source -- no claim the code does not support?
One block per entry:
<slice> <queue lines> | GONE / STILL THERE: <what remains> / PARTLY: <what remains> / UNSETTLED: <what would settle it> | replacement sentence TRUE / FALSE: <why> / none given | <the lines you read, path:line>
Do not guess: an honest UNSETTLED is worth more than a confident wrong answer.  Be hardest on the entries where the
governing line cites no source line at all, and on the ones that say a row or a test "exists" -- open the file and
find it.

Then, on separate lines: (a) any closure whose fix lives only in the working tree's later commits and not at db8b1a33
(say which commit shows it, if you can tell); (b) two list lines that are the same queue entry.

LAST LINE: DENOMINATOR: opened the source for <n> of 40 closures
