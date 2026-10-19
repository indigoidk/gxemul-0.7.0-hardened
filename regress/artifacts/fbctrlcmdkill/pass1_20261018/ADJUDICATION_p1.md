# fbctrlcmdkill -- pass 1 adjudication (2026-10-18, main loop, Opus 5.5; Fable 5.1 walled and is HELD)

Seats: GPT-6 Astra (`codex_fbcmdp1.txt`), Grok 4.7 (`grok_p1.txt`), GLM 5.3 packet-fed (`glm_p1.txt`); Fable 5.1 tried once
and walled (`fable5_p1_WALL.txt`, HTTP 429).  Opus 5.5, agy, kimi, deepseek and minimax deliberately not fired (the owner's
2026-10-17 roster).  Witness: `WITNESS_headbin.out` (2/12 on HEAD's binary, controls OK).

## The design -- unanimous, 3 of 3

**Member 3, DECLINE + LATCHED ANNOUNCE, decided in the DATA arm BEFORE the store, on the full 64-bit `idata`.**  When the
selected port is COMMAND, accept exactly `idata` == 0, 1 or 2; for anything else skip BOTH the store into `d->port[0]` and
`fbctrl_command()`, leave COMMAND (and every other cell, the selector and the framebuffer) as it was, announce once per
device through a NEW `warned_cmd` bit (independent of #549's `warned_port`) with one message naming the full value in hex
and saying the command port is unchanged, with `(once)`, and take the existing common tail (`return 1`; a read path is not
involved).  The `default:` arm's `exit(1)` then has no reachable caller; what happens to it is a pass-2 question (keep a
tripwire as #549 kept the DATA-arm one, or delete).

Why the site matters (GLM, Grok, Astra independently): `fbctrl_command()` reads the already-truncated `int`, so a latch in
`default:` still lets `sd 0x100000001` run SET_RESOLUTION and `sd 0x100000000` run NOP -- a wide write executing a command
the guest did not write.  The gate must compare the full `uint64_t`, as #549's selector refusal does.

## Disputed: `fbctrloffkill` (the offset `default:`) -- stays its own row, 2-1

Astra and Grok: the reopening rule admits a second site only when the same detector needs no new oracle, and an offset
decline needs one (a read's returned value, or a bus error -- FAULT is available on testmips); GLM: join it, its own latch
bit.  Ruled for the two: the command rows use only PORT and DATA, and the offset arm's read semantics are a separate design.

## Flags on my brief -- all TAKEN

* "dev_fb.h DOCUMENTS FILL and COPY" was false (3 of 3): two TODO constants, no port semantics; HISTORY calls them future
  work; `framebuffer_blockcopyfill()` (dev_fb.c) is an internal helper of other devices, not this controller's protocol;
  no guest in `demos/` or `test/` issues 3 or 4 -- the only writer, `demos/rectangles/rectangles.c`, sends SET_RESOLUTION.
* "FAULT n/a on MIPS" was false (Astra, Grok): a device access returning 0 becomes `EXCEPTION_DBE` (memory_rw.c); FAULT is
  available and is the wrong member for a store to a mapped register (a policy choice, recorded as such).
* The witness's `sd 0x100000003` does NOT measure the width hole (3 of 3): it truncates to 3, which dies in `default:`
  either way.  The width pin is a wide value congruent to an ACCEPTED command: `0x100000001` (no resize), `0x100000002`
  (X1/Y1 not zeroed), `0x100000000` (COMMAND unchanged).
* "dispatches FILL" was loose: 3 has no case arm; it falls to `default:`.

## The detector -- a NEW gated probe (3 of 3 prefer it; `fbctrl_port_probe.py` stays at 117, pinned by gate_mips_folds.sh)

Per refused class (3, 4, 5, `sw 0xffffffff`, `sd 0x100000003`, and the wide aliases `sd 0x100000000/1/2`), each on a fresh
device seeded so COMMAND is 2 and X1/Y1 are nonzero: survival past the store (a later access completes, exit 0), COMMAND
reads back 2, X1/Y1 unchanged, no resize line, and exactly one announce naming the full value.  A session refusing twice
(different classes, and across a selector refusal in both orders) keeps ONE command announce -- the shared-latch and flood
pins -- plus one free-running announce check (a demotion to `debug()` goes silent there).  ACCEPT rows with their side
effects, before and after the latch is set: NOP after COMMAND 2 reads back 0 and leaves X1; SET_RESOLUTION executes
(Grok: X1 = Y1 = 0 makes `dev_fb_resize()` print its `size too small` line, a `fatal()` that returns -- the latch must not
swallow it; Astra: a real 32x32 resize moves the byte at framebuffer offset 1920 to offset 96 through the row-copy loop);
GET_RESOLUTION zeroes nonzero X1 and Y1 and reads back 2.  Misplacement rows: a read of COMMAND does not re-execute it; a
DATA write of 3 to a non-COMMAND port is ordinary storage.  Floor: (a) the pre-fix build, (b) the kill re-inserted
verbatim, (c) a null medium, (d) DEPENDS-ON mutants on the new compare (narrowed to 32 bits, `> 2` -> `> 1`, the latch
shared with `warned_port`), each predicted before its table.

## Next (after the 2026-10-18 weekly battery, ~22:15)

Implement in GXEMUL-SEC, est/, build/, build-asan/ and /tmp/gxsec-build (dev_fbctrl.c is a shared file); write the probe;
pre-fix vs post-fix on one instrument; kill table with a PRETABLE.out first; pass 2 on the diff, F2, Astra confirm; gate.
