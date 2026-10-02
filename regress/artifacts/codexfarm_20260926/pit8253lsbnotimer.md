You are a researcher for a C hardware emulator project (the GXemul hardened fork).  The tree is
`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`; ignore any other `src/`.  Read-only: change no file and build nothing.

Queue row `pit8253lsbnotimer` (MED-HIGH, open), ledger title: "dev_8253.c one-byte formats: BOTH arms keep the other byte stale against the datasheet, and the LSB arm additionally installs no timer -- wrong host rate on counter 0"
Its full text: `OUTSTANDING_BUGS.md` (search "`pit8253lsbnotimer`" -- read EVERY section naming it, the latest last) and the row's
entries in `tools\pipeline\ledger.json` (id `pit8253lsbnotimer`).  The committed tree is `git -C <tree> show HEAD:<path>`; the
working tree may carry uncommitted work on the same file -- say which one you read.

FIRST LINE: `VERDICT: <the recommended next step for this row, in one phrase>`.  Then:
1. The code path, file:line, from a guest instruction or access to each defect site the row names; re-derive the
   row's count of sites rather than trusting it, and say whether the count still holds at HEAD.
2. What the architecture or the device documentation says the behaviour should be -- grep the manuals in
   `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\*.txt` (list them with `ls`; cite by file:line), or say none covers it.
3. The option set for each site, with the tree's own precedent for each option (file:line of an existing site that does
   it), and which one the evidence supports.
4. Existing probes, gates or rows that touch these sites (grep `regress\`), and what a fix would disturb.
5. The witness: the smallest guest sequence on an UNMODIFIED in-tree machine that reaches one site (describe it; do not
   write a program), with a liveness control and a device-signature control.
6. Anything in the row's text that the tree now contradicts (a site already fixed, a line moved, a claim superseded).
Say what you read (file:line) and what you inferred.
