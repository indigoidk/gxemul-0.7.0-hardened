# fbsdrampair -- implementation note (2026-11-05)

Design implemented as ruled (adj_p1_20261105/): member 3, DECLINE + per-register latched announce on both
SDRAM reads, exit(1) removed, `break` kept, writes untouched.  Declined value **0** on both arms, per
ADJ_MYTHOS.md and RESET_PREMISE_NOTE.md (00FC0000h is only the blank-ROM-programming default,
dc21285.txt:3206-3228 -- re-read for this note: line 3220 marks the EXPANSION-ROM mask "(this is the normal
default)" and the SDRAM line 3225 carries no such remark; 7.3.9/7.3.10 give "Reset value: 0.").

## Files

| file | change |
|---|---|
| src/devices/dev_footbridge.c (SEC == est, md5 ccaf09d4) | +29 -4: two latch fields; both read arms decline with odata 0 and announce once (`#NNN`) |
| regress/footbridge_sites_probe.py (md5 a52267ff) | six arms (M O X W B U), 19 rows, 37 -> 56; run_arm gains `snap_at`/`data` (defaults leave the six older arms' sessions unchanged: the pre-change probe prints the same 37 rows byte for byte, old_vs_new_{FIX,HEAD}.diff) |
| regress/gate_arm.sh, footbridge block only | display regex, ROWS 37 -> 56, six new checks (gate_arm.sh.fbs.diff: three hunks, all inside the block) |

## Ruling row -> probe row

Values the RESET rulings (r2, r3) gave as 0x00FC0000 are re-derived for 0: odata is initialised to 0 and
the read arms never assign it.

| ruling row | probe row(s) | what changed |
|---|---|---|
| ADJ R1 / r2 1 / r3 R1: mask-only, 3 reads | MC, M1, M2, M3 | value read from registers by `reg`, not through the UART; asserted on EACH read (r2); destinations preloaded with 0x12345678 so a 0 proves the load wrote; M3 = the arm's diagnostics are exactly [mask announce] (also kills HEAD's text kept, a misname, an extra line) |
| ADJ R2 / r2 2 / r3 R2: offset-only | OC, O1, O2, O3 | O2 pins zero readback against a nonzero declined value; it does not detect the equivalent early return |
| ADJ R3 / r2 3 / r3 R3: mixed | XC, X1 | two mask reads then two offset reads (ADJ); arrival order mask-then-offset asserted (r3) |
| ADJ R4 / r2 4 / r3 R4: write-only | WC, W1, W2 | W1 = no read announce AND survival (so a dead run cannot pass it); W2 = write announces exactly [mask 0x12345678, offset 0x40000]; 0x8FFC0000 not used (r2); changes legitimately when `fbsdramwrites` lands (ADJ) |
| ADJ R5 / r2 5+6 / r3 R5: write-then-read | BC, B1, B2 | one process, both registers (ADJ, r3); r2's separate offset row is B2's own id; B1/B2 assert value 0 AND one announce each (r3: the write path setting the read latch); B2 does not assert the write announce (r2) |
| ADJ R6 / r2 7 / r3 R6: null medium | existing arm L, row I1 | not duplicated: arm L is the MMU-off preamble, liveness, VENDOR_ID 0x1011, no SDRAM access, survives, no footbridge diagnostic |
| ADJ R7: MMU-on arm unchanged | existing arm T (C3 C4 C5) | unchanged |
| r3 R7: the MMU-on arm "must see no once-line" | NEW arm U: UC, U1 | arm T has no SDRAM access, so the check there would be vacuous; U performs M's reads with the MMU left on (the witness's W3).  r3's optional sentinel form is NOT available: at -M 32, PA 0x02000100 is past the end of RAM (zero-fill slack, witness W3.LOAD) |

## Departures from the rulings, and why

1. **B3 added** (writes after the reads still announce) -- not in any ruling.  The mandated GUARD FIELD vs
   BODY FIELD check: guard operand `writeflag` {READ, WRITE} x the body-read latch {0, 1}.  No ruling row
   held (WRITE, latch set); `writeflag == MEM_READ || latch` would sweep every ruling row clean (derived).
2. **Per-arm control rows taken BEFORE the first SDRAM access** (`snap_at`), so the pre-fix build reds the
   defect rows under GREEN controls rather than reading as a dead probe.
3. **Announce text**: ADJ_MYTHOS's ZERO text verbatim, "...declined, reads 0 (written values are not kept)
   (once)".  r2 wanted no value in the text (its reason was coupling rows to the 0x00FC0000 constant); r3's
   text carried the refuted reset value.
4. **Null medium mapped to the existing I1** rather than a duplicate arm (see table).

## Measured

* witness on the fix (witness_FIX.out): W1/W2 SURVIVED-SITE exit 0, r7 0x5a5ac3c3 -> 0, new announce once;
  W3 unchanged.  Pre-fix: witness_20261105/witness_HEAD.out (both sites ended the process).
* probe_legs.out: FIX (scratch clone) ROWS=56 of 56, CONTROL=OK, PASS.  HEAD (build/gxemul, pre-fix
  source) ROWS=46 of 56, CONTROL=OK, RED = M1 M2 M3 O1 O2 O3 X1 B1 B2 B3 -- exactly the rows derived.

* restore_clone.out: /tmp/gxfbs1's source cmp'd CLEAN against GXEMUL-SEC and its binary was newer, so
  its sentinel was cleared and the clone removed.
* propagate.out (coordinator's request, 09:35-09:36 local): build/, build-asan/, /tmp/gxsec-build each
  pre-fix -> fix, make rc 0, part 1 (cmp vs SEC) CLEAN, part 2 ([ gxemul -nt source ]) HOLDS; est/ part 1
  CLEAN, part 2 N/A (source tree).  build/gxemul md5 03a273de = the scratch clone's fix binary.
* fbblock_check.out: ONLY gate_arm.sh's footbridge block (lines 1081-1194, extracted verbatim, its own
  probe launch included) on build/gxemul: 29 checks, 0 FAIL; ROWS=56 of 56, CONTROL=OK.

## Owed (not done here)

* Test-variant table 1 and pass 2 (coordinator: after propagation; not started).
* `#NNN` -> the round number at landing (dev_footbridge.c x3, footbridge_sites_probe.py, gate_arm.sh).
* tools/pipeline/check_probe_wiring.py MANIFEST line for impl_20261105/fbsdram_witness.py (an unchanged
  copy of the witness, CLASS_WITNESS) if this directory is committed.
* CHANGELOG / ledger: not written here.
