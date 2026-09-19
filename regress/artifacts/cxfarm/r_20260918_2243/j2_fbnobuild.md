# J2 -- `fbnobuild`: gate 2's two fbpending_bound lanes on a host with no build/ objects -- check the repair design

## READING SCOPE AND FORM

The tree under review is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` (git HEAD cdbe7d7).  Pristine 2021 copies of GXemul
under the project root (`./src/`, `_archive/`) are NOT this fork.  Do not read `regress/artifacts/`, the ledger, the
CHANGELOG or OUTSTANDING_BUGS; the facts you need are here.  Read-only: no edits, builds or runs.
VERDICT LINE FIRST.  Mark claims READ (file:line), REASONED or NOT CHECKED; counts carry denominators; check the
premises rather than ratifying them.

## THE SITUATION (measured 2026-09-18 by a measuring seat, with lib.sh)

`regress/diff_fbpending_bound.c` is the one offline differential that LINKS ~221 objects from `build/` (the
in-place build tree, a sibling of GXEMUL-SEC) instead of compiling standalone.  Gate 2 (`regress/gate_offline.sh`)
runs it twice: the `#442` main lane (grep `fbpending bound:` rows) and, since `#537`, a self-mutant lane
(`selfmutant_one diff_fbpending_bound.c ...`, a `find "$SEC/../build/src" -name '*.o'` in its flags).

When `build/` has NO objects:
  * the main lane hits a `note` (lib.sh: `note()` touches neither `_fails` nor `_degraded`; `gate_end` then returns
    PASS, rc 0) -- so the gate is green with the detector never run;
  * the new self-mutant lane reports SETUP (undefined references from `reload_timer_value`), under the row name
    "selfmutant fbpending_bound: the detector still detects, via its named row" -- a red on a row named for
    something else;
  * the SELFCHECK row "every COVERED detector ran its sentinel" reads `$LOGDIR/diff_fbpending_bound.log`, which
    gate 2 never deletes, so a RETAINED log from an earlier run satisfies it (`$LOGDIR` defaults to
    /tmp/gxregress; a reboot clears it, and then that row reds too).

Reachability: `regress/run.sh` runs every gate whatever the previous rc, so a battery whose gate 1
(`gate_build.sh`, which rebuilds build/ from est/ and asserts 223 objects) failed or was skipped reaches this;
so does any standalone gate 2 run on a bare host.

Proposed repair (filed, not built): `degrade()` (SKIP, rc 77) in BOTH lanes' no-objects path; truncate
`$LOGDIR/diff_fbpending_bound.log` before the main lane; two negative controls (no objects -> SKIP not PASS; a
stale log -> red).  Also to carry: a stray `regress/dev_footbridge.c` would be compiled SILENTLY by the main lane
(the harness's `#include "dev_footbridge.c"` searches the including file's directory first) while the self-mutant
lane, which compiles in a mirrored tree, never reaches it -- the two lanes would test different code.

## QUESTIONS

1. **Check the measurements against the code.**  In `regress/lib.sh`: cite `note()`, `degrade()`, `gate_end` and
   the SKIP exit code.  In `gate_offline.sh`: cite the main lane's no-objects branch, the self-mutant call, and the
   SELFCHECK ran-its-sentinel row and what file it reads.  Is anything above wrong?
2. **Precedent.**  Which other gate sections already use `degrade()` for a missing prerequisite (grep the regress
   gates)?  Is there one whose shape this repair should copy, and does any of them ALSO truncate a log?
3. **The truncation.**  If the main lane's log is truncated before the lane runs, can a HEALTHY run ever red the
   ran-its-sentinel row (ordering of the lane vs that row; any other reader of that log)?  Cite lines.
4. **The two lanes' include paths.**  Read the harness's `#include` of `dev_footbridge.c` and both lanes' `-I`
   flags: confirm or refute that a stray `regress/dev_footbridge.c` reaches the main lane and not the self-mutant
   lane.  Is there a cheap presence check (a row) that would make the two lanes' inputs demonstrably the same file?
5. **Disposition.**  Is the filed repair the right one, too much, or too little?  What are its two negative
   controls exactly (input, expected token), and is anything else in gate 2 in the same "note-skip reads as PASS"
   class (grep for `note` calls guarding a missing input)?  Count them.
6. **Standing licence:** anything else found while verifying.
