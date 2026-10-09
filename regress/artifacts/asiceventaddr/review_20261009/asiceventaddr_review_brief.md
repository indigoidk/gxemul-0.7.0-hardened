# Late REVIEW seat on `#466` (`9ca9cca`): `asiceventaddr` -- the pass-2 review stage, held since 2026-09-18

**Liveness, first two lines of your answer:** (1) the token `SEAT_ALIVE_20261009_ASIC466`; (2) the FIRST LINE of
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\CHECKPOINT.md`, quoted verbatim.  Then
`VERDICT: RATIFY / RATIFY WITH CHANGES (<n>) / DO NOT RATIFY -- <one line>`.

Tree under review: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\` only.  The project root holds pristine April-2021
upstream copies; if your line numbers disagree with the tree by hundreds you are reading the wrong copy.
**READ-ONLY on every project tree** (`GXEMUL-SEC`, `est`, `build`, `build-asan`, WSL `/tmp/gxsec-build`): no edits,
no `git add/commit/stash/checkout/reset`, no plain `git status` (a commit precheck holds staged files; use
`git --no-optional-locks status`, `git show`, `git log`), and no gates.  You MAY compile a tiny standalone C99 file
in your OWN scratch dir if a claim about the preprocessor or the compiler needs settling (WSL: `wsl -d Gentoo`) --
say plainly what you ran and what you only read.

## Why you are being asked now

`#466` shipped `9ca9cca` on 2026-08-26: an 18-line COMMENT beside `SYSASIC_EVENT_TO_ADDR` in the vendored header
`src/include/thirdparty/dreamcast_sysasicvar.h` (check the path), stating the macro is correct only for `e` in
`[0,95]`.  Its pass-2 panel (`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\panel_20260826_222557\`, brief `brief_sent.md`,
answers beside it) ran 6/9: codex (then GPT-5.6-SOL), agy, grok, glm, minimax and kimi answered; the Agent seats were
never fired and deepseek's answer was a 142 KB thinking burn with no response (a seat failure).  The ledger row
`asiceventaddr` is still OPEN: the decode defect itself was not fixed.

The round is closed, so the late-dissent rule governs your answer: a wrong record is corrected in place (L4); a
MEASURED false pass gets a follow-up commit; anything else is filed as a new queue item, carried verbatim.
**Do not simply ratify.**

## THE TREE HAS MOVED SINCE `9ca9cca` -- checked 2026-10-09, re-derive it

`git log -S SYSASIC_EVENT_RANGE_OK` names ONE later commit, `29b450ce` (#467 + #468, "the ASIC domain is now
ENFORCED").  It rewrote #466's comment and added `SYSASIC_EVENT_RANGE_OK(e)` -- a bitfield-width compile-time bound,
`(e) >= 0 && (e) < 96` -- inside `SYSASIC_EVENT_TO_ADDR` (header lines ~74-141 today).  The rewritten comment says
#466's two-legged rationale against a check was REFUTED BY MEASUREMENT on #466's own pass 2.  So kimi's and
minimax's dissents appear to have been ACTED ON; `SYSASIC_EVENT_TO_BITMASK(e)` is still `(1 << ((e) & 31))` with no
guard.

## What to answer

1. **The original brief's question**, as the seat that never answered (`panel_20260826_222557\brief_sent.md`) --
   answered about `9ca9cca` as shipped, and then: does anything in it still matter after `29b450ce`?
2. **The three dissents the six answers raised** (their files are in that panel dir; each is summarised in the
   ledger row's 2026-09-17 review entries):
   * codex: *a THIRD partial guard -- `SYSASIC_EVENT_RANGE_OK` protects the ADDR macro and not the BITMASK macro one
     line below it.*  Is that live in today's tree?  Is there any use of `SYSASIC_EVENT_TO_BITMASK` (or of the event
     number) that does NOT also pass through `SYSASIC_EVENT_TO_ADDR` and so escapes the compile-time bound?
   * kimi (the rationale fails on both legs) and minimax (a build-time check would close it): **confirm or refute
     that `29b450ce` discharged them** -- and whether the bitfield bound is sound (does a non-constant `e` really
     hard-error rather than compile; is there any caller with a runtime event number?).
3. **The row `asiceventaddr` is still OPEN.**  Given the compile-time bound, can the row's defect -- high events
   decoding to dropped fourth-word offsets, or to LEGAL mask-register cases that clobber guest state -- still occur
   in today's tree?  If not, say what evidence would close it (a disposition and its witness), and whether the
   BITMASK gap keeps it open.

Separate READ from RAN.  **If you found something ELSE -- say so.**

Write your FULL answer to `C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\fableq\<seat>_asiceventaddr.md`
(`<seat>` = `fable5` or `opus5`) and return it as your final message.
