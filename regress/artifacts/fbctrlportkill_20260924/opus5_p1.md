OPUS549P1_ALIVE
# CHECKPOINT -- 2026-09-24 ~10:30 (087a90 sections rewritten; the peer's sections below are untouched)
VERDICT: PROCEED WITH CHANGES

**Design change I would make (top):** the fix code is correct and its detector is strong — but the fix RELOCATES, not removes, the host-kill for a garbage-writing guest, and the round must disclose that. Keep the DATA arm's `exit(1)` (measured belt-and-braces, below). Add to the contract, or to the detector, the residual the fix's own walk exposes: from reset (`current_port==0==COMMAND`), a refused PORT write followed by a DATA **write** of any value other than command 0/1/2 still ends the process, now via `fbctrl_command()`'s `default: exit(1)`. Section 4 files that call separately, but this round makes it reachable on the two-access path the round is about, so it should be named here rather than left silent.

**1. The witness and the fix — MEASUREMENT.** On base (`gxemul_base`, HEAD f4f601c4) the witness reproduces: arm K `HOST-DIED steps=1 exit=1`, controls OK. Built the sketched fix in `/tmp/gxopus549`; arm K now `SURVIVED steps=2 exit=0`, controls still OK. The fix does what it claims.

**2. Premise `sd 0x0000000100000003` — MEASUREMENT.** On base: after `sd 0x100000003` to PORT (port[3] pre-loaded 0x11223344), DATA reads back `0x11223344` and the guest SURVIVES. The int truncation to 3 is real and `memory_readmax64()` delivers all 8 bytes on `-E testmips`. Premise and Q1(c) confirmed.

**3. Q1(b), the width/offset walk — MEASUREMENT.** Widths 1/2/4/8 × every offset in the 0x20 window, big-endian testmips, each cell "refuse PORT, then op@off, then read@0x10", one fresh emulator per cell:
- **base:** DATA-arm `exit(1)` at +0x00 (all widths) and +0x10 (all widths); the DEVICE_ACCESS `default: exit(1)` at every other offset (52 cells).
- **fix: ZERO reach the DATA arm's `exit(1)`.** The 52 `default:`-arm deaths remain (any offset ≠ 0x00/0x10, e.g. a 1-byte access to +0x03 — out of scope, section 4, but a guest still ends the host through them). And **4 new `fbctrl_command` `default: exit(1)` deaths at +0x10**: the refusal keeps `current_port==0==COMMAND`, so a DATA *write* runs `fbctrl_command()` with a bad command. So Q1(b) answer: no access reaches the DATA arm's kill after the fix, but two OTHER terminating calls stay reachable — the unmapped-offset default (pre-existing) and the command default (which the "keep the previous selector" choice routes an unacked guest into at port 0).

**4. Q1(a),(d) — READING (grep at HEAD).** `current_port` is written only by DEVINIT's `memset` and the PORT arm (line 120); the DATA/command arms only read it. Nothing outside `dev_fbctrl.c` depends on the WARNING text — no gate, probe, or hygiene grep mentions `fbctrl` (`git grep fbctrl regress/` is empty); the only other hit is a ledger note. Replacing the text is safe.

**5. Q2, candidate edits vs the proposed rows — MEASUREMENT** (rows probe, all 8 binaries). Every proposed row is green on `fix`, announce=1. Each behaviour-changing edit is caught, and by a specific row:

| edit | verdict | the ONLY row that reds |
|---|---|---|
| `>=`→`>` (accepts 8) | caught | boundary: PORT=8 refused |
| `(uint32_t)idata` | caught | wide: `sd 0x100000003` (truncates to 3, accepted) |
| `(int)idata` | caught | wide **and** negative (`sw -1` accepted as −1) |
| refusal resets to 0 | caught | refusal/boundary/wide/negative "PORT reads 5" (5 reds) |
| store anyway (`idata&7`) | caught | same 5 (PORT reads 1, not 5) |
| latch never (announce every time) | caught | announce: exactly ONE `(once)` (got 3) |
| set latch before the fatal | **PASSES all rows** | — behaviourally identical (one non-reentrant call); not a defect |

So the smallest edit that passes every row is the latch-order swap, and it is a no-op. Every edit that changes guest-observable behaviour is caught. The boundary PORT=8 row, the wide `sd` row, the negative row, and the announce-count row are each individually load-bearing — dropping any one lets a distinct edit through. This is a well-constructed row set.

**6. Q3/Q4, keep the DATA `exit(1)` — MEASUREMENT + reasoning.** With a broken PORT fix (`>` accepts 8), a guest that sets PORT=8 then touches DATA: **measured** — the DATA arm's belt-and-braces fires, `HOST-DIED exit=1` with its diagnostic. If the DATA arm instead *declined*, `current_port==8` would index `port[8]`, one past the 8-element array — a silent out-of-bounds access (reasoning; I did not build the declining variant). So keep the `exit(1)`: it converts a future broken-PORT edit into a loud death rather than an OOB. This is the same argument the fix comment makes, now measured. The counter-point for Q6: the command-arm and default-arm `exit(1)`s are guest-reachable *today* (measured in the walk), so if this fork's policy is that no guest-drivable `exit(1)` may remain, the DATA arm is not the only one and this round does not achieve it — which is why disclosing the command-arm residual matters.

**7. Something else — MEASUREMENT.** The fix's guest-observable win is narrower than "the device no longer kills the host": after it, a guest still ends the process via (a) any access to an offset other than 0x00/0x10, and (b) a DATA write at the reset port 0 with a non-command value. Both are section-4 items, but (b) is newly reachable *because* the refusal keeps the selector — so the round's own change surfaces it. This argues mildly for taking the `fbctrl_command` and `default:` kills in the same family (Q6): they meet same-device and arguably same-class ("guest-drivable `exit(1)` in dev_fbctrl.c"), though they need new oracles (an unmapped-offset row; a bad-command row), so they are legitimately separable if the round says so explicitly.

**Notes on method / limits.** All builds in `wsl -d Gentoo`, `rm src/cpus/*.o` before each mutant, `[ binary -nt source ]` checked, clone-local `.MUTANT` while mutated, restore verified `cmp`-clean against HEAD and rebuilt to the base md5. Clone lived in WSL `/tmp/gxopus549` (removed). I did not exercise little-endian (`-E testmips` is big-endian by construction; a little-endian test machine would reach `case DEV_FBCTRL_PORT` with the low byte in a different lane, but the refusal predicate is on the assembled `idata`, so the fix is endian-independent — reasoning, not measured). Q5 (probe home / `check_probe_wiring.py` wiring) I did not measure; it is the same wiring question #548 answered and belongs to pass 2.

Logs, mutants, probes and BINARIES.md5 are under `GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/`. The repo source is untouched; the clone is gone; no emulator processes remain.
