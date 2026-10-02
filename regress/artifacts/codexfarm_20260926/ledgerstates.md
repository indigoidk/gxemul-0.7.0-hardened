You are an auditor for a C hardware emulator project's records (the GXemul hardened fork).  The tree is
`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`.  Read-only: change no file.

The ledger `tools\pipeline\ledger.json` holds ~440 rows not closed.  Some of them are finished work whose state was
never updated (example: `ip30abortkill` reads "in work", while `OUTSTANDING_BUGS.md` says "FIXED AS `#531`, 2026-09-17",
and `untrackeddetectors` names a probe change #529 is about to commit).  Find the rest -- for the rows of severity HIGH,
MED-HIGH and MED (any case) whose state is `open`, `held` or `in work`:

FIRST LINE: `VERDICT: <N> rows whose state disagrees with the record`.  Then a table, one line each: row id, its ledger
state, the evidence that the work shipped or was superseded (a commit subject from `git -C <tree> log --oneline`
naming the row or its round number, a CHANGELOG block, an OUTSTANDING_BUGS "CLOSED/FIXED" line -- file:line), and the
state the evidence supports.  Only rows with such evidence; do not guess.  Then list the rows where the evidence
CONFLICTS (the record says fixed, a later record says reopened).  Say which you checked by git and which by text.
