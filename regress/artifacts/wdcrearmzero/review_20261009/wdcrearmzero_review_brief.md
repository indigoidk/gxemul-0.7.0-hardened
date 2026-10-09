# Late REVIEW seat on `#473` (`1f1a02b`): `wdcrearmzero` + `wdcringambig` -- one held question

**Liveness, first two lines of your answer:** (1) the token `SEAT_ALIVE_20261009_WDC473`; (2) the FIRST LINE of
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\CHECKPOINT.md`, quoted verbatim.  Then
`VERDICT: RATIFY / RATIFY WITH CHANGES (<n>) / DO NOT RATIFY -- <one line>`.

Tree under review: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\src\` only.  The project root holds pristine April-2021
upstream copies; if your line numbers disagree with the tree by hundreds you are reading the wrong copy.
**READ-ONLY on every project tree** (`GXEMUL-SEC`, `est`, `build`, `build-asan`, WSL `/tmp/gxsec-build`): no edits,
no `git add/commit/stash/checkout/reset`, no plain `git status` (a commit precheck holds staged files; use
`git --no-optional-locks status`, `git show`, `git log`), and no gates.  You MAY build and run in your OWN WSL scratch
clone if the question needs a measurement (`MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash -c '...'`; `rm src/cpus/*.o`
first; check `[ gxemul -nt src/devices/dev_wdc.c ]` after) -- say plainly what you ran and what you only read.

## Why you are being asked now

`#473` shipped as `1f1a02b` on 2026-08-27.  Its pass-2 panel (`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\panel_20260827_050852\`,
brief `brief_sent.md`) ran the scriptable seats only; the two Agent seats were never fired, so the REVIEW stage of
`wdcrearmzero` is held for you.  The round is closed, so the late-dissent rule governs your answer: a wrong record is
corrected in place (L4); a MEASURED false pass against the shipped detector gets a follow-up commit; anything else is
filed as a new queue item, carried verbatim.  **Do not simply ratify** -- the seats that answered all ratified, and
unanimity on a brief-supplied fact is worth nothing.

## Settled premise (checked by grep 2026-10-09 -- re-derive it if you doubt it)

`WDC_MAX_SECTORS` is `512` and `WDC_INBUF_SIZE` is `(512*(WDC_MAX_SECTORS+1))`, at
`GXEMUL-SEC/src/devices/dev_wdc.c:47-48`.  The 2026-09-18 minimax answer flagged that the 513-block figure in the
pass-2 brief assumed this constant without stating it; the constant holds.

## THE QUESTION (held since 2026-09-18)

glm's pass-2 answer named a risk -- **interleaved guest register access mid-chunk** -- that deepseek could not close
from the packet.  **Can any guest-reachable access (a register read or write, a status poll, a new command, a
reset, an alt-status read, a DMA path) happen between a chunk being consumed and the ATAPI re-arm such that the
re-arm runs with a NON-EMPTY data ring?**  If it can, the refill-safety premise `#473`'s fix rests on is wrong, and
the shipped detector (`regress/diff_wdc_identify.c` and the rows `#473` added) may not see it.

Read the enclosing functions in `dev_wdc.c` (every exit path and the common tail), and the fix itself:
`git -C C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC show --format= 1f1a02b -- src/devices/dev_wdc.c`
(use `--format=`; a line-count cut on `git show` inlines the commit message instead of the diff).
The row's reproduction recipe is in its 2026-09-13 research entry: `evbmips -e malta`, PACKET + READ(10) of 192
blocks (a remainder above 32768 after the first chunk).

Then, as the seat that never answered, **answer the original pass-2 brief's own questions**
(`panel_20260827_050852\brief_sent.md`).  Separate READ from RAN.  **If you found something ELSE -- say so.**

Write your FULL answer to `C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\fableq\<seat>_wdcrearmzero.md`
(`<seat>` = `fable5` or `opus5`) and return it as your final message.
