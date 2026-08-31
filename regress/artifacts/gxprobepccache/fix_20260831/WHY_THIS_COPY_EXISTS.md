# A repair to an UNTRACKED file, preserved so git can recover it

`_scratchpad/gxprobe.py` is the probe harness the carrier tells every round to use rather than
hand-rolling pty plumbing.  **It is not in version control** — `git ls-files` matches zero, and
it lives at the project root, outside this repo.

Two defects were found in it on 2026-08-31 and both were repaired:

1. **A detector row that COULD NOT FAIL.**  `Emu` caches register assignments and skips
   redundant ones; `step` advances pc but the cache still held the old value.  A driver calling
   `send("step")` directly — instead of `_exec_at()`, which pops the stale pc — had its NEXT
   `set_reg("pc", a)` silently dropped, so the guest executed NOPs at the addresses the row
   believed it was probing.  A clause-(d) latch mutant swept 14/14 against the row written to
   catch it.  Fixed by moving the invalidation into `send()`.

2. **The first repair had a gap one keystroke wide.**  It matched exact command names, but
   `debugger.c` matches by PREFIX (`matchlen` = leading alphabetic run, then `strncasecmp`), so
   `st`, `ste`, `co` and `cont` all advance the guest and none invalidated the cache.  Found by
   the measuring seat AUDITING the repair rather than trusting it.  Now matched by prefix the
   way the debugger itself does, controlled over all nine accepted spellings plus
   `print`/`reg`/`put`/`stop`.

## Why the copy, and what it is NOT

**This is EVIDENCE, not a second live copy.**  Nothing imports it and nothing runs it.  It
exists because a repair to an untracked file is one `rm -rf _scratchpad` away from being lost,
and the finding that produced it — a vacuous row that eight of nine variants scored plausibly
around — is worth more than the diff.

**It deliberately does NOT settle whether gxprobe should be tracked.**  That is a repo-layout
decision with real consequences (a second copy that can drift, needing a byte-compare gate the
way `tools/CLAUDE.md` does), and it belongs to the owner rather than to a round that happened
to touch the file.  Filed as part of `gxprobepccache`.

Note the question is less urgent than it first looks: **no committed probe imports gxprobe.**
All 14 pty-forking probes in `regress/` roll their own plumbing, and `#498`'s detector follows
that precedent deliberately rather than making a committed file depend on one outside the repo.
