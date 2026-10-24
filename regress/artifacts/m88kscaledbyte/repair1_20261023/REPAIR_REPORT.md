# `#569` repair pass (R1-R5 + F25) -- the builder's report (2026-10-23; HEAD `5986c137`, unchanged throughout)

Spec: `pass2_20261023/f2/REPAIR_SPEC.md`, with its header amendments applied over section 1; the edits as amended in
`f2/repair_proposal.md`; the ruling is `f2/codex_t1f2.txt` (GPT-6 Astra: SHIP WITH THE NAMED REPAIRS).  Same sandbox
as BUILD_SPEC section 0: no git write, nothing under `tools/`, no peer file, `diff_wdc_identify.c` untouched.  Every
number below names the file that holds it.  The scoped pass on this repair diff (spec section 3) is the main loop's.

## 1. What was done, in order (2026-10-23)
| time | step | receipt |
|---|---|---|
| 11:44 | pre-check: the four round files equal pass 2's (same md5s), HEAD `5986c137`, nothing running | -- |
| 11:45 | the consumers read and enumerated BEFORE the wording was chosen | `R3_SOURCE_READING.out` |
| 11:45 | **R3**: the generator's `#569` consumer sentence reworded (comment only) | `generator_r3.diff` |
| 11:46 | the repaired generator compiled and run in `/tmp/gxt1/repair`: its output == the committed table | `TABLE_UNCHANGED.out` |
| 11:47 | **R2, R4, F25** in the driver | `driver_r1.diff` |
| 11:47 | **R1**: the block moved in the working-tree file; the new staged copy built from a fresh HEAD read | `staged/` |
| 11:48 | **M1**: the driver on the repo defaults; R2's compiler selection measured | `M1.out`, `fixed_r1.out`, `M1_cc_cases.out`, `cc_*.out` |
| 11:51-11:54 | **M2 (= R5)**: GATE 2 with the staged gate swapped in, then restored | `GATE2_committedform_tail.out`, `wt_gate_offline.sh.bak` |
| 11:55-11:58 | **M3**: GATE 2 on the working tree | `GATE2_wt_tail.out` |
| 11:58-12:02 | **M4**: propagation; `build/`, `build-asan/`, `/tmp/gxsec-build` rebuilt one at a time; clearance re-run | `CLEARANCE_r1.out` |
| 12:03 | F25's disclosure measured, supplementary | `F25.out` |

## 2. Diff stat (plain `diff` against `git show HEAD:<file>`; all LF)
| file | HEAD -> now | the repair's own delta (pass 2 -> now) |
|---|---|---|
| `src/cpus/generate_m88k_loadstore.c` | +10 -4 (working tree) | +5 -3 (R3, a comment) |
| `src/cpus/tmp_m88k_loadstore.c` | +24 -24 (working tree) | none (`TABLE_UNCHANGED.out`) |
| `regress/diff_m88k_loadstore_gen.sh` (new) | +280 -0 (working tree) | +10 -6 (R2, R4, F25) |
| `regress/gate_offline.sh` | +48 -0 (HEAD -> `repair1_20261023/staged/gate_offline.sh`) | +48 -45 (the move; `staged/move_staged.diff`, `staged/move_WT.diff`) |

`diff HEAD-blob staged` is ONE hunk, `185a186,233` (unified: `@@ -183,6 +183,54 @@`): **N = 48**, at `:185/186`
(`staged/insert_HEAD.diff`).  The working-tree insertion (`staged/insert_WT.diff`, against the pre-#569 working tree)
is the same 48 lines at the same place, compared byte for byte; the foreign hunks are unchanged apart from the shift.
`#569` occurs exactly once in each file.  md5: generator `699b7309...`, table `d222e737...` (unchanged), driver
`7c888857...`, working-tree gate `2af22d40...`, staged gate `faebdd85...`.

## 3. The repairs
* **R1** -- the block is now between `CC=$(command -v cc || command -v gcc)` and `need_file "$HERE/diff_ieee_store.c"`.
  It is invoked as `GEN= TABLE= CC="$CC" "$HERE/diff_m88k_loadstore_gen.sh" > "$MLSLOG" 2>&1`.  Its comment gains the
  proposal's placement sentence.  Its consumer sentence is UNCHANGED, as the header amendment requires (F9/F16/F23).
  The old `table1_20261022/staged/` copy is left as pass 2's record.
* **R2** -- `CC=${CC:-$(command -v cc >/dev/null 2>&1 && echo cc || echo gcc)}`; the header's override line now reads
  `CC=<compiler> (default cc, else gcc; gate 2 passes its own)`.
* **R3** -- the generator comment now says: the register-form ld/st decoder installs twelve of the slots as ic->f and
  xmem_slow() calls four; the other eight have no caller today and are repaired with them.  It is verified by READING
  the consumers (`R3_SOURCE_READING.out`: `cpu_m88k_instr.c` `:2377`, `:2411`, `:3606`/`:3611`, `:3622`, with
  `:2359`, `:2368-2373`, `:3043`, `:3087`, `:3599-3600`, `:3655`).  The enumeration of the index expressions gives
  decoder 12 (160 164 168 176 180 184 224 228 232 240 244 248), xmem_slow 4 (416 420 432 436), immediate form 0, no
  caller 8 (424 440 480 484 488 496 500 504), no overlap: MATCHES.  All 24 stay pinned.  The table is byte-unchanged.
  The comment is propagated to `est/` and the three build trees.
* **R4** -- the weighted formula is REPLACED, not annotated: `index = no_pc_sync + registeroffset + usr + scaledness +
  endianness + signedness + store + size`, "a SUM of the generator's flag-VALUED loop variables, each 0 or its flag
  (256, 128, 64, 32, 16, 8, 4), size 0..3".  It agrees with the existing indices (160 = 128 + 32; 504 = 256 + 128 + 64
  + 32 + 16 + 8).  No row or expected name changed (M1).
* **F25** -- one disclosure in the NOT-OBSERVED paragraph: "A name swap among UNPINNED cells (e.g. the scaled
  word/halfword cells not in the accept set, 185/186), made in both artifacts, keeps every row green: outside the
  contract."  The qualifier is D-1 below, measured in `F25.out`.
* **R5** = M2.

## 4. Measurements
* **M1** (`M1.out`, `fixed_r1.out`): `ROWS=123 FAIL=0`, sentinel; **byte-identical to `table1_20261022/fixed.out`**.
  The driver prints no version or CC line; its only note lines are GEN and TABLE.  Supplementary (`M1_cc_cases.out`,
  one `cc_<case>.out` each):
  * cc present: green.
  * gcc only (no cc on PATH): green, byte-identical output.
  * neither compiler: red at `gen_compiles` (64/123), the explicit row, never a skip.
  * `CC=gcc`: green.
  * `CC=/bin/false`: red at `gen_compiles`, which shows the override is honoured.
* **M2** (`GATE2_committedform_tail.out`): `offline-differential: PASS (485 checks)`, `REGRESS_PASS`, rc 0, 179 s.
  The block's 126 checks are all ok, with 0 gate-level FAIL rows.  The working-tree file was backed up
  (`wt_gate_offline.sh.bak`, md5 `2af22d40...`), the staged copy swapped in (`faebdd85...`), and the file restored
  afterwards; `cmp` against the backup is CLEAN.  **This is NOT a clean committed-tree run.**  21 of 702 tracked
  `src/`, top-level `regress/` and `tools/` files differ from HEAD (listed in the receipt), among them the foreign
  `regress/diff_wdc_identify.c` and the peer's five `src/` files.  The receipt also lists the untracked files.  485
  equals the derived 359 + 126.  The 502 receipt from pass 2 and GATE 11's recorded limitations stand as written.
* **M3** (`GATE2_wt_tail.out`): `PASS (502 checks)`, `REGRESS_PASS`, rc 0, 171 s; 126/126.  502 = 485 + the 17 checks
  the foreign hunks add, the same count as pass 2's working-tree run.
* **M4** (`CLEARANCE_r1.out`, run 12:02:05):

  | tree | part 1, generator / table | part 2 (`gxemul -nt` each file) |
  |---|---|---|
  | `est/` | CLEAN / CLEAN | N/A (source tree, no binary) |
  | `build/` | CLEAN / CLEAN | yes / yes (11:59:20) |
  | `build-asan/` | CLEAN / CLEAN | yes / yes (12:01:18) |
  | `/tmp/gxsec-build` | CLEAN / CLEAN | yes / yes (12:01:52) |

  In each build tree make itself re-ran the generator rule once (log lines 113/113/111), and the in-tree table compares
  CLEAN against GXEMUL-SEC.  The **driver was not propagated: no tree has a `regress/` directory, `est/` included**
  (measured; listed in the receipt).  GATE 11 was not re-run, as specified.

## 5. What disagreed with the spec or a ruling (by id), and notes
* **D-1 (F25's wording).**  "made in both artifacts" was added.  A swap in one artifact alone reds the fresh ==
  committed row: `F25.out`, F25a 1/123 (table only) against F25b 0/123 (both).  The variants exist as files only
  (`F25_table.diff`, `F25_generator.diff`).
* **D-2 (M4's parenthetical).**  The spec says "the driver only exists in GXEMUL-SEC/est"; `est/` has no `regress/`
  either, so the driver exists only in GXEMUL-SEC.
* **D-3 (section 1 R3 vs the header).**  Section 1 says "the gate block's comment likewise"; the header amendment says
  the generator only.  The header was followed.
* **D-4 (R3's words).**  The proposal's original R3 text does not carry the twelve/four/eight counts that section 1's
  parenthetical asks for.  I used the proposal's AMENDED sentence (written for the gate comment), moved into the
  generator.  The exact words are in `generator_r3.diff`, for pass 3.
* **D-5 (landing, new).**  `.gitignore:33` `regress/diff_*` (re-included only for `!regress/diff_*.c`) matches the new
  driver, so `git ls-files --others --exclude-standard` does not list it and a plain `git add` refuses it.  Land it
  with `git add -f` AND mode 100755, then check `git ls-files -s` (F4/F26).  The tracked `regress/diff_autodev_gen.sh`
  (100755) sits under the same rule.
* **D-6.**  `wt_gate_offline.sh.bak` (kept as M2 requires) contains another session's uncommitted `gate_offline.sh`
  hunks.  Committing it would publish that work; that is the coordinator's call.
* **D-7.**  `make -j8`, one make job, as in the build.
* **Supplementary measurements, beyond the spec:** M1's five compiler cases and `F25.out`.
* **F28.**  The "18 outputs" are the 16 v3 outputs plus v1's PRE/FIX.  The root `table1_20261022/RUNS.log` holds only
  the 16 v3 runs.  v1's PRE/FIX are recorded in `driver_v1/prefix_HEAD.meta` and `driver_v1/fixed.meta`, and v1's ten
  legs in `driver_v1/RUNS.log`.
* **Not done here (records / landing, the main loop's):**
  * the stale `pass1_20261022/MANIFEST.md5` (F15);
  * the landing records (F7, F21, F26);
  * the filings (F13, F19, F24, C1/C2);
  * the scoped pass (spec section 3).  Its diff to inline is `generator_r3.diff`, `driver_r1.diff`,
    `staged/insert_HEAD.diff` and `staged/move_staged.diff`.

REPAIR_REPORT_DONE


**Landing note (main loop, 2026-10-23 ~12:20):** `wt_gate_offline.sh.bak` (md5 `2af22d40...`, the working-tree gate backed up before the M2 swap) was MOVED OUT of this directory before the commit, because it carries another session's uncommitted `gate_offline.sh` hunks that must not land under `#569`; it is kept in the session scratchpad (`t1/landing/wt_gate_offline.sh.bak_peerhunks`).  The restore it witnessed is also recorded by the `cmp` line above.

**Timeline correction (main loop, 2026-10-23 ~12:25; found by GLM 5.3 on pass 3, `pass3_20261023/ollama_glm_t1p3.txt:11`):** the section-1 row "| 11:48 | **M1** ..." names receipts whose files on disk are stamped 12:02:54-12:02:56 (`M1.out`, `fixed_r1.out`, `M1_cc_cases.out`), i.e. AFTER M4's rebuilds (11:58-12:02).  The receipts are the 12:02 ones: either M1 was re-run after M4 and the earlier files overwritten (same driver md5 `7c888857...`, same result, ROWS=123 FAIL=0, byte-identical to `table1_20261022/fixed.out`), or the 11:48 row is a timeline error.  The measurement stands; the stamp is corrected here rather than in the table.
