# grok seat -- three of YOUR tie-break rulings, disputed by the confirming seat: concede or hold

READ-ONLY.  Write nothing, build nothing, run nothing that changes a file.  The tree under review is
`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC` at commit `7440e129` -- read committed files only
(`git -C C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC show 7440e129:<path>`; never `git status` or `git diff`), and ignore any
other `src/` under the project root.

Open your answer with the token `GROK_HOPEN3_ALIVE_1002` followed, on the same line, by the first line of
`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\HARNESS_DISPOSITIONS.md` quoted
verbatim.  The NEXT line is your verdict line, exactly in this form:

`VERDICT: <n> conceded, <m> held, of 3 open findings`

## What is open

In the review of this project's regression harness you ruled 21 rows where two verifications differed
(`...\astraretro_harness_20260926\adjudication\grok_20261002\grok_htiebreak.txt`).  GPT-6 Astra then confirmed the
draft dispositions group by group.  On three findings your tie-break and Astra's confirmation give different KINDS, so
neither is filed.  Both lines of each are quoted, verbatim, at the end of `HARNESS_DISPOSITIONS.md` under the heading
"OPEN BETWEEN TWO SEATS"; read them there.  (A fourth pair under that heading, `hgatehygiene:F5`, differs only in grade
and is settled: both make it NEW, so your MED governs.)

1. `hbundle_regress28:F1` -- you: NEW MED `pcc2fatestatus` ("PCC2 survival row ignores forced termination").
   Astra: FILED `ptywaitstatus`.
2. `hgdromcondprobe:F3` -- you: NEW HIGH `gdromcondhow` ("R1b and R2b accept the diagnostic and ignore child
   termination").  Astra: FILED `ptywaitstatus`, adding these consumer sites to its evidence.
3. `hdiffdiskimageio:F2` -- you: NEW LOW `diskionegwriteproof`.  Astra: RECORD -- the row's comment is corrected to say
   that on the normal fseeko path the negative-offset WRITE does not independently prove the explicit guard.

## The fact that decides 1 and 2

`ptywaitstatus` is an EXISTING queue row (`git show 7440e129:OUTSTANDING_BUGS.md`, the heading at about line 21937):
"regress/*.py pty probes: the emulator child's WAIT STATUS does not reach the liveness verdict in 56 of 73 pty probes
-- a host death AFTER the final observation passes, and a dead attempt whose last print is missing can still qualify
for a retry".  It is a CLASS row with a census.  The question for 1 and 2 is plain and checkable: **is the defect you
ruled NEW the same defect that class row already records for that probe, or a different one?**  Please check, for
`regress/pcc2_default_probe.py` and `regress/gdrom_cond_probe.py`:
 (a) is the probe one of the 56 the row's census counts (the census is in the ledger note of that row and in the queue
     text around that heading)?  If you cannot find the census list, say so;
 (b) is what you found "the wait status does not reach the verdict" -- the class -- or something the class does not
     cover (for example: the row accepts a DIAGNOSTIC as its pass condition whatever the child's fate, which would stay
     wrong even if the wait status were plumbed through)?  Cite the probe lines.
A finding that is the class, in a probe the class counts, is FILED under it; a finding the class does not cover is its
own row.  Do not defend your ruling and do not defer: say which it is, with lines.

## For 3

Is the defect a wrong COMMENT (then RECORD is right: the fix is the sentence) or a CHECK THAT CANNOT FAIL (then it is a
row: the fix is a test)?  Cite `regress/diff_diskimage_io.c` and `src/disk/diskimage.c` lines.

## Answer format

For each of the three: `<n> | CONCEDE: <the kind you now give> | HOLD: <your kind>` -- then one line naming what you
opened (`path:line` at `7440e129`) and what it showed.  Mark what a reading cannot settle as UNSETTLED and name the
measurement.  Last line: `DENOMINATOR: opened <n> of the <m> locations this brief and the two lines name`.
