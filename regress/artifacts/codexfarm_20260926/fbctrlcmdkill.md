You are a researcher for a C hardware emulator project (the GXemul hardened fork).  The tree is
`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`; ignore any other `src/`.  Read-only: change no file and build nothing.

Queue row `fbctrlcmdkill` (HIGH), `OUTSTANDING_BUGS.md` (search "### `fbctrlcmdkill`"): `src\devices\dev_fbctrl.c`,
`fbctrl_command()`'s `default:` ends the emulator process for any command other than 0-2 -- including the documented but
unimplemented FILL and COPY (`dev_fb.h`) -- reached by a guest DATA write while the COMMAND port is selected, on every
test machine.

FIRST LINE: `VERDICT: <recommended disposition in one phrase>`.  Then:
1. The exact code path (file:line) from a guest store to the `exit(1)`, and every other `exit(`/`abort(` in the file.
2. The option set, each with the tree's own precedent (grep `src\devices\*.c` for the idiom; name file:line): decline +
   latched `(once)` announce; implement FILL/COPY; a guest-visible error; anything else the tree does for an unknown
   command.  For each: what a guest observes, and what it would cost.
3. What change #549's committed probe `regress\fbctrl_port_probe.py` already drives through COMMAND (sessions and rows),
   and which rows a fix here would disturb or need.
4. The witness: the smallest guest sequence on an unmodified `-E testmips` that reaches the exit (describe it; do not
   write a program), and which controls would make it admissible (a liveness value and a device signature).
5. Anything in the row's text that the tree contradicts.
Say what you read (file:line) and what you inferred.
