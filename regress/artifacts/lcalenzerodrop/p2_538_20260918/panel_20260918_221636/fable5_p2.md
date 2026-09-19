FABLE_SEAT_ALIVE_20260918_538P2
claude-fable-5-1 | "# CHECKPOINT -- 2026-09-18 22:0x   HEAD: cdbe7d7 #537 fbsmlane: #442's harness printed a verdict token its own self-mutant lane could never read -- the lane runs, pinned on R3"
VERDICT: CLOSES -- the lane floor is verified 0/4 open (vc_ne0..3 red exactly their own lane's `getenv`, lane-1 covering escape killed at `low16`); CONTINGENT on the F3 re-run, because F2 and F4 change the instrument and a comparison owes one instrument -- the committed probe must be the measured one before commit.

# #538 pass 2 -- Fable 5 seat, adjudicating the lane-class closure

**How I worked.**  Read-only; this file is the only write.  Read in full: the packet, `brief_sent.md`, `opus5_p2.md`,
`codex_adv538p2.txt`, the working-tree `regress/lca_widewrite_probe.py`, `_scratchpad/w538/waitstatus_patch.py`, and in
`regress/artifacts/lcalenzerodrop/closure538_20260918/`: `INSTRUMENT.md5`, `BUILD_PHASE.out`, `logs/bins.md5`, the
`TABLE.out` block inlined in the brief.  Grepped `codex.txt` and `grok.txt` for their Q3 harness text.  Re-derived the
`store_buf` chunking and lane arithmetic from `src/core/memory.c:837-857` and `dev_lca.c:275-312` myself.  I did not
re-run anything.

## Q1 -- CLOSES (contingent on F3).  The floor, the denominator, the receipt

**The floor as ruled at #530 §F2 is {write arm} x {lane 0,1,2,3} at C=16.**  I re-derived it, since it is my own
prior ruling and #540 made me restate the discriminator: `ofs = (relative_addr & 3) % len` (`dev_lca.c:297`) is a
body-induced partition that flows into `data[ofs]`, the operand of the edited forward (`:300-301`) -- so lane is a
floor axis, exactly the form I gave for #540 Q2.  Consistent across both rounds on this one handler.  Direction is the
dominating predicate; the read arm has no wide producer (`store_buf` only writes), so it is legitimately outside the
floor, not an unrowed cell.  So the floor is four cells.

I checked each cell's arithmetic against the real `store_buf` ladder rather than the probe's replay:

| lane | port | a_sparse | chunks | forwarded byte | want | rowed | red under (lane-isolating) |
|---|---|---|---|---|---|---|---|
| 0 | 0x2fc | 0x5f80 | [16] | s[0]='A' | 0x41 | `l0w16 getenv` | **vc_ne0 12/13** |
| 1 | 0x021 | 0x420  | [16] | s[1]='B' | 0x42 | `low16 getenv` | **vc_ne1 12/13** |
| 2 | 0x2fe | 0x5fc0 | [16] | s[2]='C', \|0xb0 | 0xf3 | `l2w16 getenv` | **vc_ne2 12/13** |
| 3 | 0x2ff | 0x5fe0 | [16] | s[3]='D' | 0x44 | `wide getenv` | **vc_ne3 12/13** |

Each cell forwards one 16-byte chunk (c=16 > 8, so the width pin holds), and each is pinned INDEPENDENTLY: the
one-lane exemption `vc_neL` reds exactly its own lane's row and no other (TABLE.out lines 5-8).  **That is the
strongest closure form -- not "some variant reds each row" but "a variant exempting only this lane reds only this
row."**  The lane-1 escape R6 named by name (`&& (len <= 8 || (P & 3) != 1)`, which the popular covering
{mc2, kbc1024} misses) IS `vc_ne1`, red at `low16`.  **0 of 4 cells open.**

**R6 validity, checked:** diff delivered (Opus md5-matched the fenced block to `git diff`, 6 hunks; `INSTRUMENT.md5`
shows the table ran on 8bd97e4's `dev_lca.c` = `8084ff07…`, so the uncommitted #540 `| PHYSICAL` edit did not
contaminate it, and F10 shows it could not anyway); roster complete (nine CLOSES; codex_adv's DOES NOT CLOSE is an
evidence-limit on its four-file list, and it named no surviving floor mutant -- its P1 "whole-chunk delivery" is
settled OUTSIDE its list by KILLLEN8's `[ writing to device 'lca_isa' addr 00005fe0 failed ]`, the len>8 refusal
firing on the real binary); zero carried with its denominator (0/4).

**Why contingent, and it is not a formality.**  F2 (harness) and F4 (preset) CHANGE the instrument, and F5 adds a
file-create.  The shipped probe must be the measured one (the score-claim-names-its-log rule).  F4 alone shifts the
recorded value in the `l2w16` rows of every preset-kept leg (0xb0 -> 0xb1), and F2 recomputes `alive` for all 17.
Neither can OPEN a floor cell -- F2 only makes `alive` stricter, F4 changes a value not a score, F5 is inert because
`alpha_dummy.bin` already existed for the measured run -- **so the enumeration is closed and no listed change can
reopen it.**  But the RECEIPT is owed: the chain closes when F3's re-run reproduces the table on the final
instrument.  I rule CLOSES because the substantive chain question (is the lane floor covered) is settled and the
re-run is a ship-gate receipt, not a fresh adversarial pass that could find a new breach.

## Q2 -- the harness (be hardest here): the hole is REAL, the fix is RIGHT, filing the parent is RIGHT

**Is a late host death a real hole?  YES, and I verified the mechanism rather than taking codex's mock on trust.**
`session()` sets `alive` from `rd()` during setup and the command loop (`:128-135`).  `rd()` returns True on a
*timeout* (`:113-127` -- it only returns False on EOF/OSError).  So a child that prints all its registers and THEN
dies, or hangs silently, leaves `alive == True` with every value already captured -- the rows score on correct
values and the `alive` row is green.  **A mutant that services the access correctly and then crashes the host is
scored a PASS.**  That is the #540-F14 class (host death read as escape) reached from the harness side, and host
death is the class this fork cares about most.  The F6 `if alive and ...` retry guard does NOT cure it, because
`alive` is computed from read-timing, not the child's status -- codex's sharper point, and it is correct.

**The "one seat against two" framing in the packet is inaccurate, and it matters for the record.**  Opus did not deny
the hole: it listed "record the waitpid status" as hardening (a) and named the exact residual (*"an intermittent
death that went undetected and then passed on retry"*).  grok's "no path I can see" is scoped to THIS file's 17 legs
(true -- all completed cleanly, `retried=none`).  So codex and Opus AGREE the latent hole exists; the split is only
DISPOSITION (fix now vs defer), and the packet's fix-now is right for unshipped L1 material -- deferring a cheap,
correct fix would ship a known vacuity in the deliverable, and F3's re-run has to happen anyway, so folding the
harness fix into it costs nothing.  **Correct the record from "one seat against two" to "codex demonstrated what
Opus independently flagged; I adopt the fix Opus named."**

**Is the fix right?  YES.**  The load-bearing insight is the ORDER: drain the pty to EOF (bounded 10 s) BEFORE
`os.close(fd)`, because closing the master first SIGHUPs the session leader and a status check would score that as a
death.  The patch drains, then closes, reaps, and sets `alive = alive and (WIFEXITED and status==0)`.  A post-`quit`
hang hits the 10 s bound, then close SIGHUPs it, and the reap sees a signal -> `clean = False` -> not-alive: the safe
direction.  **One caveat to record, not a blocker:** the reap is a *blocking* `os.waitpid(pid, 0)`; it terminates
only because gxemul installs no SIGHUP handler (Opus verified by grep -- SIGINT/CONT/ALRM/PIPE only).  Put that
dependency in a comment beside the reap, so a future SIGHUP handler cannot silently turn the reap into a hang.

**Is filing the committed parent's copy the right scope?  YES.**  `lca_isalane_probe.py` is a SHIPPED witness (13/16);
patching its `session()` re-opens its 352-row measurement and owes its own re-run -- that is a separate round, and
"more witnesses create more candidate ROUNDS, never bigger rounds."  The three copies patched here are all UNSHIPPED
(this probe, #540, alphavmkill), so they are L1.  File the parent with the residual named explicitly (late-death /
silent-hang scored as pass), so the filed item is actionable rather than "harden the harness."

## Q3 -- F3 owed in FULL; F8 disclose-and-file, with one strengthening

**F3 -- full 17-leg re-run, not just the movable legs.  AGREE.**  A comparison owes ONE instrument: you cannot diff a
base measured on the old instrument against mutants on the new one.  The packet's reason is the right one and I reject
the tempting shortcut ("stricter liveness only adds kills, so keep the old base"): F4 changes a PRESET, which is not a
liveness tightening, and F2 recomputes `alive` for the base leg too.  Operational note the packet already respects: a
#540 kill table is running now, and the F3 re-run carries wall-clock oracles -- it must run alone, after that table,
never concurrently.

**F8 -- DISCLOSE (xi) + FILE the presence pin as LOW.  AGREE, with a required strengthening.**  Opus's concern is
real and I confirmed it: the width "pin" is the assert `got_chunks == chunks`, which compares the probe's OWN replay
against the probe's OWN declaration -- self-referential, blind to a `memory.c` ladder change.  And the shipped GATE
runs only `base`, whose green rows forward `s[lane]` from any chunk width, so the gate cannot tell a 16-byte chunk
from a 4-byte one.  So a future `store_buf` change could make the gate silently stop testing len>8.  **But making it
a scored source-read row opens the frozen-copy path question (which tree's source does the gate read?), which this
round need not open** -- so file, don't owe.  The strengthening: **(xi) must CITE the measured receipt, not merely
name the gap.**  The width WAS empirically pinned at measurement by the base/KILLLEN8 differential -- KILLLEN8's
`failed` line at `00005fe0` proves a len>8 chunk reached the handler on the real binary.  (xi) should read "width>8
confirmed on the real binary at measurement (KILLLEN8 `failed` at 0x5fe0); future ladder drift is disclosed, not
gated," so the contract records a confirmed-then-disclosed dependency rather than an open hole.  This is the one the
packet was least sure of; disclose-and-file is the right call, and the citation is what makes it honest.

## Q4 -- the ten dispositions: no full reversal; two corrections and the Q1 contingency

I traced each disposition to its source line or artifact.  None is substantively wrong.  Three need sharpening:

* **F1 / Q1** -- "CLOSES" is right about the floor but must be stated as CONTINGENT on the F3 receipt (above).  Not a
  reversal; the packet itself owes F3, but the two must be bound: the commit is authorized only when the re-run
  reproduces the table on the final instrument.
* **F2** -- decision upheld; the "one seat against two" characterization is corrected to "codex demonstrated the hole
  Opus independently flagged" (above).  Add the blocking-`waitpid`/no-SIGHUP-handler comment.
* **F8** -- upheld; (xi) must cite the KILLLEN8 receipt (above).

Checked and upheld as written:
* **F3** -- full re-run, correct reason (one instrument).
* **F4** -- preset 0x01: verified.  The MSR stores `idata` (`dev_ns16550.c:236`) and ORs 0xb0 on every access
  (`:128`), so preset 0x00 reads 0xb0 whatever happened -- vacuous; 0x01 reads 0xb1 != want 0xf3 and round-trips.
  The `getenv` red-capability is unaffected (want stays 0xf3).  Right.
* **F5** -- create `alpha_dummy.bin`: right; a fresh-clone robustness fix, inert on the measured run (the file is in
  the artifacts dir).
* **F6** -- the contract L4s: I spot-checked the load-bearing ones.  **(ii) is a genuine catch**: `P & 1`/`P & 3` ARE
  lane bits, inside the floor and caught, so the old wording mis-disclosed floor cells as debt -- "port bits above
  the lane" is correct.  **(vii) equivalent/unreachable**: right -- the NUL sits at chunk offset >=15 while the lane
  byte is at <=3, and argv carries none, so a zero is never forwarded.  **(ix) MSR blind bits 0xb0** and **(x) inner
  forward width** (an OOB read of the one-byte `byte` if the constant 1 widens -- correct, and correctly clause-(e)
  debt since the forward width is a fixed constant, not a body-induced partition).  None moves a cell into or out of
  the floor.  Accept.
* **F7** -- parent header stale present tense (`:164-169`, `:179`): comment-only L4, part of the parent edit.  Right.
* **F9** -- durable receipts: DONE and verified.  `bins.md5` has 18 hashes; only `w_base == w_restored` (and both ==
  the HEAD build), all 16 variants differ; `BUILD_PHASE.out` carries ORDER_OK, BASELINE_CMP CLEAN, CLONE RESTORED
  cmp=clean, restored==base.  This discharges Opus's "no binary hashes" residual.
* **F10** -- #540 cannot move these scores: right; every session runs ptbr==0 kernel mode, where identity == PHYSICAL
  (my #540 pass 1).  Independent of commit order.

**How I checked for a reversal:** I re-derived the floor and the four cells' `store_buf`/lane arithmetic from source
rather than from the replay, confirmed each `vc_neL` reds exactly its lane in TABLE.out, read the patch against the
SIGHUP/EOF ordering it depends on, and read `bins.md5`/`BUILD_PHASE.out` to confirm F9.  The only places the record
overstates are the F2 framing and the F8 disclosure, both corrected above; the decisions are sound.

## Found something else
* The patch's reap is unbounded (`os.waitpid(pid, 0)`), safe only because gxemul has no SIGHUP handler.  That fact is
  load-bearing and lives in another file -- put it in a comment at the reap, or a later SIGHUP handler turns the reap
  into a silent hang.  (Filed-weight, not blocking.)
* The width-pin `assert got_chunks == chunks` reads as a check but cannot fail on an emulator change -- it compares the
  probe to itself.  It is fine as a WITHIN-cell consistency assert; it is not the width receipt.  The receipt is
  KILLLEN8.  (This is the substance of the F8 strengthening.)
