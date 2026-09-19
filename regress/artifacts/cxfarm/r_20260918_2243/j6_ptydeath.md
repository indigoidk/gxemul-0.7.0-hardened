# J6 -- pty-driven probes that never look at the child's exit status: for each, is a late host death VISIBLE through some other channel?

## READING SCOPE AND FORM

The tree under review is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` (git HEAD cdbe7d7); read only `regress/*.py`
(top level).  Do not read `regress/artifacts/`, the ledger, the CHANGELOG or OUTSTANDING_BUGS.  Read-only.
VERDICT LINE FIRST.  Mark claims READ (file:line), REASONED or NOT CHECKED; counts carry denominators.

## THE SITUATION

Most probes under `regress/` drive the emulator through `pty.fork()`, send debugger commands, read rows back, then
`quit`, close the master and reap the child.  A measured defect (2026-09-18, with a mock): a probe whose
`session()` calls `os.waitpid` and DISCARDS the status reports GREEN when the emulator dies AFTER the probe's last
observation -- e.g. an `exit(1)` on the way out -- because nothing reads the status and the pty EOF looks like a
normal quit.  The fix shape that measured correctly: drain the pty to EOF after `quit`, THEN close and reap, and
require `WIFEXITED` with status 0 (closing the master before the child exits SIGHUPs it and would score a clean run
as a death; a clean run gave status 0, a deliberate `exit(1)` gave 256).

A census by a peer, keyed on whether the file references W{IFEXITED,EXITSTATUS,IFSIGNALED,TERMSIG} or
`waitstatus_to_exitcode`: of the `regress/*.py` files that call `pty.fork`, 17 USE the status, 1 binds it unused,
39 call `os.waitpid` bare (status discarded), 16 never reap at all.  That key is a CORRELATE: a discarded status is
a defect only where NO OTHER CHANNEL observes the death.

## THE QUESTION -- one table, one row per file

Derive the population yourself first: list every top-level `regress/*.py` that calls `pty.fork` (count it), and
classify each as USED / BOUND-UNUSED / BARE / NO-WAITPID by reading its reap code (cite the line).  Then, for
EVERY file NOT in USED, answer:

  (a) does any row or final check observe the child's death through another channel -- an `OSError`/EOF on read
      that is turned into a `HOST-DIED` token, a `quit` echo that must arrive, a row that reads a value AFTER the
      last guest action, a sentinel the emulator prints on clean exit?  Cite the line.
  (b) what is the LAST observation the probe makes before `quit`, and would a death immediately after it change
      the verdict (yes / no / only if the death precedes X)?
  (c) does the probe have any row whose EXPECTED result is a death (a kill arm)?  If so, how is death detected
      there, and would an exit status OTHER than 1 (a SIGSEGV, a SIGABRT) score the same?
  (d) your classification: EXPOSED (a late death is invisible), COVERED-BY-CHANNEL (name it), or N/A (the probe's
      rows never depend on the host surviving).

End with counts: N files, USED / BOUND-UNUSED / BARE / NO-WAITPID, and among the last three how many EXPOSED,
COVERED, N/A.  Then name the three or four files where the fix matters MOST (a gated detector, a kill arm that
cannot tell a signal from exit 1, a witness whose whole point is host survival) and say why.

Two files have already been measured EXPOSED by others and need no re-derivation beyond confirming the reap line:
`fbpending_drain_probe.py` (close routine ~line 403) and `fbpending_witness.py` (~line 342); `lca_widewrite_probe.py`
was the mock's subject.

**Standing licence:** anything else found -- e.g. a probe whose `quit` is never sent, or a reap that can hang.
