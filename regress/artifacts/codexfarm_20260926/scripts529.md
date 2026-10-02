You are a reviewer of release scripts for a C hardware emulator project (the GXemul hardened fork; tree
`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`).  Read-only: change no file and run nothing that writes.

These scripts will assemble and commit change #529 (all in
`C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\`):
`records\prep529.py`, `records\commit529.sh`, `records\ledger_529.py`, `p529\r17\mk_r17.py`, `p529\r17\mk_gate529.py`,
`p529\r17\manifest529.py`.  The working tree is shared with another session's uncommitted work; the scripts must commit
#529's content only, stage by name, never lose a working-tree change, and undo everything if the pre-commit hook fails.

FIRST LINE: `VERDICT: <N> defects`.  Then each defect: the file and line, the input or tree state that triggers it, and
what goes wrong (a wrong file staged, a working change lost, a refusal that cannot fire, a check that passes on the
wrong thing, an undo that does not restore).  Check in particular: the five parked MANIFEST entries removed from and
re-inserted into the checker; the artifacts directory staged without `ctl0c_discharge_20260917/bin/`; the ledger
rebuilt from the backup; the placeholder refusals; what happens if HEAD moves between prep and commit.
