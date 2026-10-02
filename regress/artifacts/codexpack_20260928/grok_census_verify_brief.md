GROK SEAT -- verify 22 "unrecorded, guest-reachable" terminating-call sites named by a codex census (2026-09-28)

Open your answer with the token `GROK_CENSUS_VERIFY_ALIVE_0930`.  Then, FIRST LINE:
`VERDICT: <n> of 22 sites are guest-reachable AND unrecorded at HEAD -- <one clause>`.

The tree is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC` (a hardened fork of the GXemul machine emulator, C99).  Read
COMMITTED files at `db8b1a33` (`git -C C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC show db8b1a33:<path>`); the working
tree carries other people's uncommitted work.  Never read `C:\DocumentNoSnc\CC\GXEMUL\src\` (a pristine 2021 upstream
copy).  Read nothing under `regress/artifacts/` except the file this brief names.  Write nothing; return text.

A codex census (`regress/artifacts/codexpack_20260928/INGEST_20260928.md`, section 5) lists 22 sites where a call
to `exit()` is claimed to be (a) reachable from code running in the GUEST at run time and (b) recorded NOWHERE in
`OUTSTANDING_BUGS.md`.  Both claims were made by grep and by reading; neither has been checked by a second seat.
For EACH of the 22 (the section lists them by path:line), answer on one line:
`<path>:<line> | REACHABLE: yes / no / only with <condition> -- <the guarding condition, quoted> | GUEST LEVEL: user / privileged | RECORDED: <backticked id> / prose OUTSTANDING_BUGS.md:<line range> / NONE | <the search you ran: the function name, the message text, the file name, and what matched>`
Search `git show db8b1a33:OUTSTANDING_BUGS.md` by the function name, the diagnostic text in the `fatal()` beside the
exit, and the file's basename -- the queue records many sites in prose without an id, and one earlier pass was
overturned six times for calling such entries unrecorded.  Also check whether the site is one of the nine HIGH findings
already under review (a design dossier exists for `memory_ppc.c:275`, `cpu_ppc_instr.c:2307/:2333`,
`cpu_arm_coproc.c:177`, `cpu_arm.c` exception recursion, `cpu_arm_instr.c` user-mode LDM, `dev_dreamcast_gdrom.c` DMA
re-entry); say "under review" for those.

Then: **(a)** the sites you would rank first for a correction round, with one sentence each on why an ordinary guest
operating system would meet them; **(b)** anything ELSE you noticed while checking (a site the census missed in the same
files; a comment that is false); **(c)** DENOMINATOR: how many of the 22 you checked in the source versus ruled on
from the census text.
