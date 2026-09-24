OPUS_SEAT_ALIVE_20260919_FBD5P2
CHECKPOINT.md line 1: `# CHECKPOINT -- 2026-09-19 10:3x   HEAD: f685d75 (peer records) > 9c28ca5 #539 receipt (7836071 = #539 n6, the footbridge IRQEnable read ACCEPTED)`

**VERDICT: DO NOT SHIP AS-IS. FLOOR BREACH (L2), MEASURED.** Seven single-edit product mutants sweep the shipped composite detector clean (sites probe 36/36 AND diff_footbridge 111/111), and an eighth (A4) passes all 111 differential rows in a compile-only run. Six of the eight are the clause-(d) form `if (X)` -> `if (X && Y)` applied to the fix's own guards:
* a `len == 4` conjunct at the four sites P9 does not cover (A1-A4);
* `&& len == 4` on the DOMINATING `writeflag == MEM_READ` (G1, G2).

The other two sweeps (B1, B2) come from a legal read re-arming a latch. B3, in the same class, passes all 111 differential rows too. The fix code itself is right. The repair is 23 offline rows, measured to kill all ten escapes (A1-A4, B1-B3, G1, G2 and M11) while the FIX stays green (IDENTITY 111 -> 134).

Two of the requested mutants are KILLED: (c) a store into the other family's status, and (d) a dropped `(once)`. M13 (teardown before the observation) is GREEN, as PRETABLE predicted. With the quit also removed it is KILLED, but only by H2's `exit == 0` clause. The probe header's sentence "move the teardown ahead of the observation -> H2 must red" is therefore a WRONG RECORD (L4).

## Method
* **Clone:** scratch clone `/tmp/gxopusfbd5p2` = `cp -a build/`.
* **Baseline:** `git show HEAD:src/devices/dev_footbridge.c` + `patch_fbd5.py`. It `cmp`s equal to GXEMUL-SEC's working copy.
* **Instruments:** GXEMUL-SEC's patched `regress/` files, frozen into the clone (md5: sites 0d6a0adf, diff 44f97470).
* **Sentinel:** clone-local `.MUTANT` dropped before mutant 1.
* **Builds:** every build ran `rm dev_footbridge.o gxemul` then `make -j4`, and all 14 checked `[ gxemul -nt dev_footbridge.c ]` FRESH.
* **FIX control:** build md5 d19184ee, which equals the round's FIX binary and build/. Sites 36/36 PASS, diff 111/111 PASS.
* **Files:** driver `run_p2.run-115954.sh` (frozen copy of `run_p2.sh`), generator `mkmut_p2.py`, harness mutants `hmut_p2.py`. Top log `TABLE_OPUS_P2.log`; per-run logs and each mutant's `diff` are under `logs/`.

## Results (sites probe 36 rows / offline differential 111 rows)

| id | edit (one, on the FIXED file) | sites | differential | disposition |
|---|---|---|---|---|
| A1 (a) | `else if (len == 4 && !d->warned_fiq_raw_w)` | 36/36 | 111/111 | **ESCAPED** |
| A2 (a) | `} else if (len == 4 && !d->warned_irq_clear_r)` (the READ site) | 36/36 | 111/111 | **ESCAPED** |
| A3 (a) | `else if (len == 4 && !d->warned_irq_raw_w)` | 36/36 | 111/111 | **ESCAPED** |
| A4 (a) | same at FIQ_STATUS (compile-only ext run) | not built | all 111 shipped rows green; only the new X1 rows red | **ESCAPED** |
| B1 (b) | a legal IRQ_STATUS READ clears `warned_irq_status_w` | 36/36 | 111/111 | **ESCAPED** |
| B2 (b) | a legal IRQEnable (+0x188) read clears `warned_irq_raw_w` | 36/36 | 111/111 | **ESCAPED** |
| B3 (b) | a legal FIQ_RAW_STATUS read clears `warned_fiq_status_w` | 36/36 | 111/111 | **ESCAPED** |
| C1 (c) | the IRQ_STATUS decline also does `d->fiq_status = idata` | 34/36: S5, SF2 | 11 red (fiq_status preserved) | KILLED |
| C2 (c) | the FIQ_RAW_STATUS decline also does `d->irq_status \|= idata` | 35/36: SF1 | 3 red (P5 preserved, P7) | KILLED |
| D1 (d) | the IRQ_RAW_STATUS announce drops `(once)` | 34/36: N2, N0 | 111/111 (blind: fatal() is counted) | KILLED (guest rows only) |
| D2 (d) | the ENABLE CLEAR announce drops `(once)` (wrapped literal) | 34/36: N3, N0 | 111/111 | KILLED (guest rows only) |
| G1 extra | IRQ_STATUS `if (writeflag == MEM_READ && len == 4)` | 36/36 | 111/111 | **ESCAPED** |
| G2 extra | same at FIQ_RAW_STATUS | 36/36 | 111/111 | **ESCAPED** |
| M13 (e) | sites H2: `os.close(fd)` moved ahead of the `next_rc` send, plus an inert select() hardening (R0: measured green alone, 36/36) | 36/36; H2 `prologue=True next=False dead=True exit=0 ok` | -- | GREEN, as PRETABLE predicted |
| M13q (e) | M13 plus no `quit` | 35/36: H2 (`exit=None`, signal 1 = SIGHUP) | -- | KILLED, by the exit==0 clause alone |

Under G1, a byte or halfword LEGAL read of IRQ_STATUS falls into the decline arm. It returns 0, announces a "write" that never happened, and consumes the latch, so a later real write goes silent. G2 does the same at FIQ_RAW_STATUS.

## Why each escape is structural, not bad luck

**A (width guard on a decline).**
* Arm S only issues WORD accesses.
* In the P-row loop, the first access to each site is len 4. It latches the site before the byte and halfword accesses run, so a len guard is invisible there. This is the M11 blindness, and it applies at every site.
* P9 (byte-first access on a fresh instance) exists **only for IRQ_STATUS**. The repair landed at exactly the address the M11 mutant used and left the four symmetric cells open, which is the `#499` shape.
* `if (X)` -> `if (X && len == 4)` on the predicate the fix ADDED is the canonical clause-(d) form. **Grade: L2.**

**G (narrowed dominating predicate).**
* No row, guest or offline, does a LEGAL byte or halfword read of any status register. On the guest side the status is 0 anyway.
* `writeflag == MEM_READ` dominates every edited line (DEPENDS-ON clause 1).
* The narrowing sends legal accesses INTO the new decline arm. The effects are a wrong value, a false announce, and a consumed latch.
* Width is a floor axis here by the `#499` precedent (width x component x direction). **Grade: L2.**

**B (a legal read re-arms a latch).**
* Arm S reads legally between a site's two declines only in five fixed pairings: (S2, N1), (S1, N2), (S3, N3), (S4, N4), (S5, N5). Each pairing uses a neighbouring register, not the declining site's own read.
* A read that re-arms a DIFFERENT site's latch, or that is the site's own register read, therefore comes after that site's last decline, and nothing observes it.
* Offline, P0's legal reads all come before the first decline, and P7's come after the last.
* These mutants are new WRITERS of the guard field. That is the carrier's "who else writes this field" question. PRETABLE answered it by grepping the product (5 writers), but no row defends it.
* **Grade: arguable.** A new writer in a sibling case is not obviously inside the diff-closed (d) enumeration. B1 is inside the edited case's own read branch, so it is the strongest L2 candidate. The repair is cheap either way (below).

## The repair, MEASURED
This was compile-only. It ran in a separate tree under the clone's `ext/`, and the clone's `src/` was never mutated for it. `ext_block.c` was inserted before IDENTITY in a copy of the shipped `diff_footbridge.c`, adding 23 rows:
* **X1 (10 rows):** for EACH of the five sites and len in {1, 2}, a fresh seeded instance whose FIRST access has that width. It must announce exactly once. This generalises P9 to the full site x width grid.
* **X2 (11 rows):** on a seeded instance, legal len-1 and len-2 reads of IRQ_STATUS, IRQ_RAW_STATUS, FIQ_STATUS, FIQ_RAW_STATUS and IRQ_ENABLE_SET. They must return the low lanes of 0x10 / 0x18 / 0x40 / 0x50 / 0x30 and announce nothing.
* **X3 (2 rows):** latch all five sites, then do legal reads of all five readable registers at widths 1, 2 and 4, then issue all five declines again. There must be 0 new announces.

Results (`EXT_OPUS_P2.log`; per-run logs in `ext_logs/`):

| run | red rows |
|---|---|
| FIX | only IDENTITY (111 vs 134, expected) |
| A1, A2, A3, A4 | each: its two X1 rows |
| M11 | P9 + its two X1 rows |
| B1, B2, B3 | X3 |
| G1, G2 | each: its two X2 rows + "legal narrow reads announce nothing" |

**All ten escapes are killed and the fix gains no new red row.** The block is scratch-only and was not written to any tree. If it is adopted, X1 subsumes P9, and IDENTITY becomes 134 (or 133 if P9 is folded into X1).

## Other findings
* **What M13 actually shows.** With the teardown first, `next=False` and `dead=True` are satisfied by the closed fd whatever the child is doing, so those two clauses do not validate themselves. The leg still reds under M13q because closing the pty sends SIGHUP to a live child (exit None, signal 1). **`exit == 0` is the load-bearing clause** that tells "quit worked" apart from "we closed it."
* **Wrong record (L4) in the header.** In `footbridge_sites_probe.py`'s header, the negative-controls paragraph (around lines 69-70) says "move the teardown ahead of the observation -> H2 must red". That is FALSE: it was measured green. Suggested wording: "...H2 stays green (the closed fd reports dead); only exit == 0 then separates a quit from a HUP -- measured, M13/M13q."
* The differential prints two `@@SELFCHECK@@` lines that match `^  FAIL ` on every run, including FIX; they are its own self-test. A driver grepping for `FAIL` must exclude them. The round's driver does, via `[^@]`; mine initially did not. Harmless.
* D1 and D2 are killed by the guest rows only, because the offline differential counts fatal() calls rather than reading them. That matches M9 and the stated contract split.

## Clone final state
* **Restored:** HEAD + `patch_fbd5.py`.
* **Source check:** `cmp` against GXEMUL-SEC's working `dev_footbridge.c` is CLEAN.
* **Binary check:** `gxemul -nt source` is FRESH, md5 d19184ee.
* **Sentinel:** `.MUTANT` was cleared by the driver only after both checks passed; re-verified afterwards by hand.
* **Extra contents:** `/tmp/gxopusfbd5p2/ext/` holds the compile-only repair-row trees. No build uses any product source there.
* **Nothing else touched:** nothing was written to GXEMUL-SEC, est/, build/, build-asan/ or /tmp/gxsec-build, and no gate_*.sh was run.

## Seat record
* **Model:** Claude Opus 5 (claude-opus-5[1m]), Agent seat.
* **Files read:**
  * `_scratchpad/CHECKPOINT.md` (line 1)
  * `p2/brief_fbd5_p2.md` (sections 1-6)
  * `impl/mkmut_fbd5.py`, `impl/run_table_fbd5.run2-085734.sh`, `impl/hmut_fbd5.py`, `impl/TABLE2.log`, `impl/patch_fbd5.py` (head)
  * GXEMUL-SEC `src/devices/dev_footbridge.c` (:560-650)
  * GXEMUL-SEC `regress/footbridge_sites_probe.py` (whole file)
  * GXEMUL-SEC `regress/diff_footbridge.c` (helpers, includes, IDENTITY)
* **What I ran:** two WSL driver scripts from frozen copies, about 3 minutes of wall time in total:
  * 14 fresh builds
  * 15 sites-probe runs
  * 13 differential runs
  * 11 compile-only extended-differential runs
