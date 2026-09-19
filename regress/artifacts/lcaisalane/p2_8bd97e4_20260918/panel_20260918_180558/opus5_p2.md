OPUS_SEAT_530P2_LIVE
VERDICT: CLOSES -- zero floor breaches across 13 binaries × 10 cells (102 legs). Each of the 9 variants that escape the width row is killed by the same shipped GETENV instrument at another reachable cell, so they are clause-(e) debt. But "the width cell is COVERED" is measured FALSE: the row covers 1 of 12 cells, and three L4 corrections are owed.

**Method.** I worked in a scratch clone `/tmp/gxopus530p2`. Its `dev_lca.c` `cmp`'d clean against SEC and against the `8bd97e4` blob (md5 `8084ff07`). The other path files also matched `8bd97e4`, except `cpu_alpha_palcode.c`, which differs only by a comment. I rebuilt base in the clone first, and base scored full marks on every cell, so the probe construction is sound. Predictions went on file before any leg. The file's Birth time is 18:25:33 and the first leg ran at 18:26:09. I appended to it three times, so its mtime does not prove the order; each addendum states what had already run when it was written. Every leg ended in its sentinel, none retried, and every value matched its prediction. Only `getenv` rows ever went red; every alive and control row was green on all 13 binaries.

**Q1 — every entry MEASURED** (`logs/<cell>__<bin>.log`). The frozen row is the shipped `lca_widewrite_probe.py`.

| id | edit | frozen row | first differing input | killing cell (base → variant) |
|---|---|---|---|---|
| (a) va | write arm `&& len <= 16` | 3/3, not distinguished | C=64 | l0w64 MCR 0x41→0x03; l2w64, kbc256, kbc1024 also kill it |
| (b) vb | guard `len > 16` | 3/3 | C=64 | l0w64 0x41→0x03; kbc1024 0x41→0x04 |
| (c) vc | `len<=8 \|\| lane==3` | 3/3 | C=16, lane 0/1/2 | l0w16 0x41→0x03; low16 IMR 0x42→0xff; mc2 MSR; kbc16/256/1024 |
| (d) vd | `% (len>8?8:len)` | 3/3 | none: EQUIVALENT | equals base at 5 cells |
| (e) ve | `len>8 && port<0x200` | 3/3 | C=16, port < 0x200 | low16 0x42→0xff; kbc16 0x41→0x04 |
| (f) vf | `data[len>8?0:ofs]` | 2/3, DISTINGUISHED (0x41 vs 0x44) | C=16, lane ≠ 0 | also k16 2/3, mc2 3/5 |
| (g) vg | before the shift: `len>8 && (A & 0x10)` | 3/3 | C=16, k=16 | k16 SCR 0x44→0x5a; mc2 MSR 0xf3→0xb0 |
| (h) vh | read loop `i<8` | 3/3 | none: EQUIVALENT | equals base at 5 cells |
| T1 vt1 | "aligned only": `len>8 && (A & 0x1f)` | 3/3 | C=16, k=16 | same cells as (g); same function as (g) on everything store_buf can produce |
| T2 vt2 | static check: refuse a wide chunk that continues the previous access | 3/3 | 2nd chunk of a multi-chunk write | mc2 SCR 0x54→0x5a |
| ladder | `len <= 64` / `len <= 256` | 3/3 each | C=256 / C=1024 | kbc256 (≤64 variant red), kbc1024 (both red) |

- **Brief's predictions:** all eight of the brief's Q1 predictions are correct. For (h), only the first half of its reason is needed: the #95 pre-zero plus ofs ≤ 3 < 8 makes it equivalent even for a wide read.
- **Parent probe:** every variant scores 352/352 by construction (DERIVED, not run). Each added predicate is gated on `len > 8`, T2's static is read only by that decline, and the parent has no non-comment CALL_PAL, GETENV or `-o`.
- **Other readings of "aligned" (DERIVED):**
  - Alignment to 16 or less, or to the chunk's own length: EQUIVALENT, because store_buf chunks are always aligned to their size.
  - Alignment to 32: escapes the row (this is the vt1 I built).
  - Alignment to 64 or more, or lane-0-only: the row catches it, because `0x5fe0` is 32-aligned but not 64-aligned, and the row is lane 3.
- **Ladder:** it measures that chunks of 16, exactly 64, exactly 256 and more than 256 bytes reach the handler whole (no more than 1024, by the 1 KB split).

**Q2 — ruling: no L2, three L4s.**
- **Which rule sets the floor:** the joint-cells letter. The write arm tests `len` only against 0, and `% len` separates only 1, 2, 3 and ≥4. So every width ≥ 4 is one class, and any threshold at 8, 16, 64 or 256 splits it at a point the body never tests.
- **How I read pass 6:** by its own stated reason, "(uncatchable, so it cannot be discharged that way)". That makes it a condition on clause (e): a contract line can only discharge a variant that some shipped instrument can reach.
  - That condition is what made `len <= 8` an L2: no instruction can reach len > 8.
  - It is now met, measured: every escape is killed by the GETENV instrument at another cell.
- **Why not the literal "probed width set" wording:** read as a floor rule, it singles out the width axis for no reason the body supplies. Width was only ever special because of the STQ = 8 instrument boundary. The same reading applied to ports or to the discarded a<4:0> bits would contradict the parent's flagship-ruled class disclosures (p_port10, lcaisasize/H1b).
- **The three L4s:**
  1. The row's "DESIGNED TO CATCH any guard that declines a len > 8 WRITE … guard or conjunct form" is refuted by (a), (b), (c), (e), (g), T1 and T2. Each is such a guard and each scores 3/3.
  2. Clause (iii)'s warrant, "the others share the same `len > 8` predicate", is refuted by (a), (b) and the ladder.
  3. The parent header's "COVERED, not merely disclosed" is false: 1 of 12 cells is rowed.
- **The brief's 12-cell enumeration:** I walked it and it is exact for (C, k, lane) writes: 8 + 2 + 1 + 1. It omits axes the body never tests but the producer does vary: the chunk's position in a multi-chunk write (T2 lives there), the port value beyond its lane (e), and the byte value. The forwarded byte of a wide chunk can never be NUL.
- **If the adjudicator follows pass 6's wording instead:** (a) and (b) become L2, and one diff should close these cells:
  - Row the 8 (C, lane) write cells: C16 × lanes 0–3, C64 × lanes 0 and 2, C256 × lane 0, C1024 × lane 0.
  - Add one k=16 cell and one two-chunk write.
  - Disclose, with warrant: the rest of the k axis, port values, chunk index beyond 2, and the READ side.

**Q3.**
- **`wide alive`** is survive-only. No variant turns it red on its own, because a host death also leaves t4 unprinted and reds `wide getenv` with it. DERIVED; green everywhere, MEASURED.
- **`wide live`** is a valid control. RAM cannot sit at that address, a missing device reads 0 or leaves the sentinel, and the scratch register resets to 0, so 0x5a proves the store landed. It does not prove the register is specifically the scratch register, which does not matter for the row's claim. DERIVED.
- **`RET`** is correct. Every red leg printed the preset, which only phase 4's load can produce, so each red is a detection and not a construction failure. MEASURED.
- **New construction gap (DERIVED):** nothing asserts the GETENV length is over 8. Changing `load_const(A3, 16)` to 4 turns the row into a len-4 row that base and both pass-6 mutants pass silently.
- **Other producers (DERIVED, grep census at `8bd97e4`):** GETENV/store_buf is the only way len > 8 reaches this window on alphabook1.
  - The only PHYSICAL user present on alphabook1 is pccmos: 1-byte accesses at a fixed internal address.
  - File loaders use NO_EXCEPTIONS, which never calls a DM_DEFAULT handler such as lca_isa.
  - Instruction fetch reads 4 bytes and PUTS reads 1; there is no bus master.
  - So there is no PHYSICAL producer and no wide READ producer.
  - Widths above 16 need a host string of at least C−1 characters. The kernel name `alpha_dummy.bin` alone yields a 16-byte chunk.

**Q4.**
- **Precedent:** no other regress row drives store_buf; there is no in-tree precedent.
- **Options the brief did not name:**
  - (5) A minimal kill subset chosen by measured coverage: the pair {mc2, kbc1024} reds all nine escapes plus (f), and both fit in one session with a 1024-character `-o`.
  - (6) Remove the producer. This is a shared-code change to store_buf and needs its own warrant.
  - (7) Fold the closure into the reopened `lcawidefold` fix. Once the handler forwards every byte, the body tests `len` and the width rows become floor under the plain letter.
- **My choice:** under my ruling this is optional debt, but I would take (5) now. It is cheaper and more honest than an 11-cell disclosure.

**Q5.**
- The fall-through variants (a) and (c) write into the emulator's own heap copy of the `-o` string: store_buf passes a const-cast pointer to it as `data`. A second GETENV into RAM would therefore detect fall-throughs at any port, including unmapped ones. It cannot see declines that simply return 0. DERIVED, not run.
- (d) produces a different binary from base but behaves identically at every cell measured.

**Restore.** The clone's `dev_lca.c` was restored from SEC and `cmp`'d clean. The rebuilt binary is fresh and md5-identical to the measured base (`c6bcdbdf`), and the sentinel is removed. Nothing else under GXEMUL-SEC, `build/`, `est/`, `build-asan/` or `/tmp/gxsec-build` was written. Builds used `make -j2`. Probe legs ran four at a time with the emulators idle at the debugger prompt.

Files are in `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\lcalenzerodrop\opus_p2_20260918\` (untracked; 260 files, no `.bin`):
- `README.md`
- `PREDICTIONS.txt`
- `PREDICTIONS.stat.txt`
- `RESULTS.txt`
- `lca_widecell_probe.py`
- `variants/*.diff`
- `scripts/`
- `logs/`