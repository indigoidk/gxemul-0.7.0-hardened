SEAT_ALIVE_20261009_WDC473
# CHECKPOINT -- 2026-10-07 11:3x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)
VERDICT: RATIFY WITH CHANGES (7) -- #473's product edits are right and the refill premise HOLDS AT HEAD (0 dirty re-arms in 26,315, MEASURED), but it was FALSE AS SHIPPED at 1f1a02b (4 routes reproduced; codex and grok said so on 2026-08-27 and the round acted); separately a 4-mutant refill/arm CONTENT family escapes the detector at every revision including HEAD (128/0), #495's write guard has no gated detector, and five record groups are wrong -- one of them MEASURED wrong ("no regression" is false in the (32K, 64K] band).

Seat: opus5 (this agent is Claude Opus 5.5, `claude-opus-5-5`).  Late REVIEW seat on `#473` (`1f1a02b`), held question `wdcrearmzero`.

---

## 0. What I RAN and what I only READ

**RAN (all in a private WSL scratch, `/tmp/gxopuswdc`; nothing written to any project tree; no gate; no git command that writes):**

* Trees exported read-only with `git archive` at `1f1a02b` (as shipped), `d894e35d` (#473's pass-2 corrections), `HEAD` = `ef577140`, and the pre-fix parent `00d546de`.  `config.h` copied from `GXEMUL-SEC/`.  Baselines rebuilt in the clone: `1f1a02b` 23 rows / 0 failures, `d894e35d` 26/0, HEAD 128/0.  Baseline `dev_wdc.c` files `cmp`-clean against their archives after every table.
* **A mutant table** against the SHIPPED offline detector (`regress/diff_wdc_identify.c`, unmodified) at all three revisions -- 7 mutants x 3 revisions, each in its own fresh copy, each a one-line edit verified by `diff`.
* **A rung-1 invariant search** (`opus_rearm_fuzz.c`, mine): drives the REAL `dev_wdc_access()` / `dev_wdc_altstatus_access()` of an instrumented COPY of `dev_wdc.c` whose only change is one inserted call, `OPUS_REARM_PRE(d)`, at the head of the re-arm branch, which only READS head/tail.  Three measures: occupancy at re-arm entry (THE QUESTION); the invariant `flag && phase != CMDOUT  =>  occupancy == atapi_len` after every access; and every byte a DATA read pops compared against `data_in[received + k]`.  Plus a **guest-eye** check on the directed sequences (the guest's own lane count vs the transfer), which is what sees a full ring that reads as empty.
* **Separability** (pre-fix parent + only `= 0 -> = 32768`), **`#495` removed at HEAD** (both detectors), and **three proposed detector rows** in a scratch copy of the HEAD detector.

**RUNG 1, SAID PLAINLY.**  Every number below is a direct-call harness through the real access path with the disk/SCSI layers stubbed.  It is a state-machine measurement, never a witness.  Every access it issues is an ordinary register access a guest can make on `evbmips -e malta` (data port at widths 1/2/4; 3/8 only from a 64-bit MIPS guest, per `#337`'s comment).  I did NOT run the 2026-09-13 rung-3 probe or `#495`'s rung-3 witness.

**READ:** `dev_wdc.c` at `1f1a02b` (whole file, every exit path and the `ret:` tail) and at HEAD (the ring primitives, reset helper, `wdc_command()`, the whole `wd_data` read and write arms, the dispatch); the HEAD detector's re-arm, arm, multi-chunk and contract blocks; the panel dir `panel_20260827_050852` (all seven answer files); the ledger rows `wdcrearmzero`, `wdcringambig`, `wdcaddtoinbufbound`, `wdcrearmwalk`; CHANGELOG `Round 473 pass 2`, `Round 474 pass 2`, `Round 475`, `Round 495`; `OUTSTANDING_BUGS.md`'s `#473` residuals.

**Settled premise, re-derived:** `GXEMUL-SEC/src/devices/dev_wdc.c:47-48` (HEAD and `1f1a02b` identical): `WDC_MAX_SECTORS 512`, `WDC_INBUF_SIZE (512*(WDC_MAX_SECTORS+1))` = 262656 = 513 x 512.  minimax's premise audit resolves in the brief's favour.

**THE TREE MOVED DURING THIS REVIEW, AND THE CITATIONS ARE KEYED TO A COMMIT FOR THAT REASON.**
* `04f3e7c0` landed at 13:22 (probe-wiring re-date).  It touches `CHANGELOG.md` (+13 lines), `check_probe_wiring.py` and artifacts -- **none of the files measured here** -- so every "HEAD" result below holds for both `ef577140` and `04f3e7c0`.
* The working copies of `CHANGELOG.md`, `OUTSTANDING_BUGS.md` and `ledger.json` were mid-edit by the peer session.  I first read a working-tree CHANGELOG **163 lines longer than HEAD**.
* So `CHANGELOG.md` / `OUTSTANDING_BUGS.md` / ledger line numbers below are those of **`git show 04f3e7c0:<file>`**.  Grep the quoted text rather than trusting a number.  The `src/` and `regress/` line numbers are unchanged between `ef577140` and `04f3e7c0`.

---

## 1. THE QUESTION -- can the re-arm run with a NON-EMPTY ring?

### 1a. A framing correction first (READ)

There is no window "between a chunk being consumed and the ATAPI re-arm".  The re-arm runs at the bottom of the SAME data-port read whose pops drained the chunk (`1f1a02b` `dev_wdc.c:701-789`; HEAD `:1197-1477`).  So the real question is whether anything can put bytes in the ring that `atapi_len` does not count, while a chunk is being read.  That is what was measured.

### 1b. At `1f1a02b`, as shipped: YES.  MEASURED, four routes

192-block READ(10) (393216 B), so a re-arm follows chunk 1; "guest-eye wrong" = lanes the guest read that differ from the transfer at its own stream position.

| route (one guest action mid-chunk) | occupancy at re-arm entry | guest-eye result |
|---|---|---|
| **D1** one 2-byte store to the DATA port | **2** | chunk 2 shifted: **32655 of 65536** lanes wrong from lane 32768 |
| **D2** `0xA1` ATAPI IDENTIFY, then a bare `0xA0` PACKET, then the guest drains the stale remainder | **512** (the IDENTIFY block) | the guest gets IDENTIFY bytes as the first 512 bytes of chunk 2 |
| **D3** Device Control SRST (`0x04`, released), then D2 | **512** | same -- at `1f1a02b` SRST did nothing at all (`:495-496` tested `WDCTL_4BIT`) |
| **D4** codex's full ring: 229888 one-byte stores | reads **0**: full looks empty | **all of chunk 1 lost** (32641 of 32776 lanes are over-read sentinels); the refill then overwrites the unread chunk |

D4 is invisible to an occupancy reading by construction (`head == tail` is both empty and full), which is why the guest-eye check exists.  Random search, 1000 sessions (seed 3): **447 of 1254 re-arms dirty**.

**Why, READ:** the write arm pushed with no phase guard and its warn latch was off while the flag was set (`:804-873`).  `wdc_command()` cleared only the flag and the error (`:513-515`), so ring residue and the stale `atapi_len`/`atapi_received`/`atapi_st` survived into a new PACKET.  The read arm re-armed on the flag alone, with no phase test (`:732`).  And the ring could not tell full from empty.

**This is NOT a new finding, and the record says so.**  codex (verdict *"CHANGES REQUIRED -- ... the refill's ring-empty premise is false under the actual access handler"*) and grok (*"Q1's safety argument is a drain-path property, not an invariant"*) answered this exact question on 2026-08-27.  Between them they named routes D1, D2, D3 and D4.  The round acted the same morning: `CHANGELOG.md:16961`, *"L4: 'the ring is empty at the re-arm' IS AN OVERCLAIM.  Two seats broke it independently"* (`d894e35d`, 05:33).  So the brief's *"the seats that answered all ratified"* is false: **two of six answering seats dissented on exactly this premise.**

### 1c. At HEAD (`ef577140`): NO.  MEASURED

| run | sessions | data reads | re-arms | **dirty** | **invariant violations** | **content mismatches** |
|---|---|---|---|---|---|---|
| default seed | 200 | 18,518,878 | 309 | **0** | **0** | **0** |
| seed 1 | 10,000 | 860,357,172 | 13,329 | **0** | **0** | **0** |
| seed 2, heavy (up to 8 events over 4 chunks) | 10,000 | 1,174,226,888 | 12,677 | **0** | **0** | **0** |

**Denominator:** 26,315 re-arms.  Events placed at random offsets and at chunk ends -12/-4/-2/-1 were: data-port writes at widths 1/2/4/3; PACKET with no CDB; ATAPI IDENTIFY; ATA READ; ATAPI SOFT RESET; RECAL; a random opcode; Device Control `0x04`/`0x08`/`0x0e`; an alt offset-1 write; alt-status and status reads; random register reads and writes; SDH; partial CDBs; a new transfer; 1- and 8-byte reads.  A "bare PACKET" or "new READ(10)" follow-up was added after half the command and reset events.  Both byte orders and five read-width policies were used.

D1-D4 at HEAD: the store is refused; there is no re-arm in CMDOUT (D2 and D3 read an abandoned transfer, which is correct); the ring is never ambiguous.

**DMA / external paths, READ:** none.  `dev_wdc.c` has no DMA (IDENTIFY word 49 advertises none; `WDSF_SET_MODE` is a debug-only no-op).  The only outside entry point is `wdc_set_io_enabled()` (`bus_pci.c:788,790,987,989,1087,1089`), which gates accesses and touches no state.

**WHY it holds at HEAD (READ, and this is the part a maintainer needs).**  It is an inductive invariant: **while `atapi_cmd_in_progress && phase != PHASE_CMDOUT`, ring occupancy == `atapi_len`.**

* **Established at dispatch.**  The 12-byte gather fires only at exact occupancy 12 and drains all of it (`:1716-1717`, `:1739-1742`).  "Exact" depends on `#484`'s sacrificed slot (`:245-252`).
* **Preserved by reads.**  The pops are `min(calls, occupancy)` and `consumed` is `min(calls, atapi_len)` (`#475`, `:1290-1291`), so the two stay equal.
* **No producer can run in that state:**
  * data-port stores are refused (`#495`, `:1576-1578`);
  * every command entry and every SRST flushes the ring and drops the flag (`#479` helper `:915-924`, called at `:938`; `#481` at `:832-835`);
  * the flag is set only together with CMDOUT (`:1046-1047`);
  * no re-arm in CMDOUT and no dispatch outside it (`#477`, `:1318-1319`, `:1716-1717`).

**The invariant rests on FIVE later commits in four places.**  `#475` 07:03, `#477` 08:55, `#479` 12:18, `#481` 15:05 and `#484` 17:59, all on 2026-08-27, plus `#495` on 2026-08-30.  None of them is at the re-arm, so the refill is correct at HEAD for reasons the re-arm's own comment does not name (see 3c).

### 1d. Does the shipped detector see it?

* **At `1f1a02b`: no.**  The dirty-ring row added by `d894e35d` builds the dirty state with direct `wdc_addtoinbuf()` calls.  It kills grok's `head == tail` guard mutant but cannot detect any ROUTE.
* **At HEAD: there is nothing to see unless a support regresses.**  The support most likely to regress has no gated detector.  **MEASURED, HEAD with `#495`'s guard nulled:**
  * the shipped 128-row detector: **128 rows, 0 failures, PASS** (as `#495`'s own record says);
  * my rung-1 D1 sequence: **dirty re-arm, 32655 of 65536 lanes wrong**.
* The rung-3 witness that `#495` says "ships AS a detector" (`regress/wdc_addtoinbuf_probe.py`) is **executed by no gate**.  It appears only in `gate_hygiene.sh`'s `GRANDFATHERED_PROMPTLESS` census.  That debt is already filed as `wdcsingleleg` under a dated `wiringcliff` exemption.  The new part is that **an offline row closes the gap today**: proposed row P3, section 2 / Q2, measured.

---

## 2. The original pass-2 brief's own five questions

**Q1, refill safety.**  See section 1: FALSE at `1f1a02b`, TRUE at HEAD.

**Q2, a fifth null-repair mutant.  MEASURED: four escape at EVERY revision.**  Each was built in its own copy and verified as a one-line `diff`.

| mutant (one token) | `1f1a02b` (23 rows) | `d894e35d` (26) | HEAD (128) |
|---|---|---|---|
| `Md_frozenj` `data_in[received + j]` -> `data_in[received]` (**codex's, named 2026-08-27, never built until now**) | **ESCAPED 23/0** | **ESCAPED 26/0** | **ESCAPED 128/0** |
| `Md_revwalk` -> `data_in[received - j]` (glm's) | **ESCAPED** | **ESCAPED** | **ESCAPED** |
| `Md_halfj` -> `data_in[received + j/2]` | **ESCAPED** | **ESCAPED** | **ESCAPED** |
| `Md_armfrozen` initial arm `data_in[j]` -> `data_in[0]` | **ESCAPED** | **ESCAPED** | **ESCAPED** |
| control `Md_wrongoff` -> `data_in[j]` (in contract) | killed 1 | killed 1 | killed 2 |
| control `Md_order` -> `data_in[received - consumed + j]` | killed 1 | killed 1 | killed 2 |

**Mechanism.**  Each content oracle reads ONE byte -- the first of the chunk.  At the re-arm that is `0x3c` (and `0xa1` on the chunk-edge row); at the arm it is `0x5a`.  So any source-index edit that keeps byte 0 correct passes, while 32767 of 32768 bytes are wrong.  The row comment claims the class, though: *"MARKERS, so the refill can be caught taking bytes from the WRONG place"*.

**The repair, MEASURED in a scratch copy of the HEAD detector** (`proposed_opus/PROPOSED.diff`):

* **P1:** fill `row_rearm_zero`'s payload with a position pattern before its markers, then compare the WHOLE 32768-byte refilled chunk against `payload[131072..]`.
* **P2:** in `row_arm_overrun`, check bytes 1 and 32767 equal the stub's `0xc3`.
* **P3:** the `#495` write route offline.  Arm through the real dispatch, drain chunk 1 to 2 bytes, store 2 bytes, drain them, then require occupancy 32768 and `data_in[32768]` first.

| tree | result with P1-P3 (identity 128 -> 131) |
|---|---|
| HEAD | **131 rows, 0 failures, PASS** |
| `Md_frozenj` / `Md_revwalk` / `Md_halfj` | KILLED by P1 |
| `Md_armfrozen` | KILLED by P2 |
| HEAD minus `#495` | KILLED by P3 |
| `Md_wrongoff` / `Md_order` | still killed (now 4 and 3 rows) |

**P3's scope, REASONED, not measured:** it pins `#495`'s clauses (a) and (b) only, using one 2-byte store in DATAIN.  `#495`'s own `M5` (`== PHASE_DATAIN`) and `M6` (`&& len == 2`) would pass it.  The full `#495` contract still needs the rung-3 witness wired (`wdcsingleleg`).

**Q3, `received += consumed` before the re-arm.**
* READ: `1f1a02b` `:749-751`; HEAD `:1293-1294`, then the `== 0` tests.
* MEASURED: the order-reversed form (`Md_order`) is killed at all three revisions.  So the brief's fear that *"every row ... would still be green"* is false of the shipped detector; grok's reading was right.

**Q4, leaving the primitive unbounded.**  Filing it was the right call, but the stated reason ("correct and complete for every caller in the tree today") was false at the time.  The data-port write arm was an unbounded, unguarded caller during DATAIN, and D4 shows the refill pushing onto a full ring that reads as empty.  It became moot within 13 hours: `#484` (`cf300c07`, 17:59 the same day) bounded the primitive with refuse-before-store.  At HEAD the primitive IS bounded.

**Q5, one round for two defects.**  Shipping them together was a legitimate choice; "inseparable" was wrong.  **MEASURED:** the pre-fix parent with ONLY the re-arm `0 -> 32768` change (no clamp move, no refill) completes:
* 96 blocks: 5 re-arms, 0 of 196608 lanes wrong;
* 128 blocks: 7 re-arms, 0 of 262144 wrong;
* only 129 blocks (264192 > ring) still wraps.

The unmodified parent stalls in DATAIN.  So the re-arm-first ordering is a complete stall fix for every transfer that fits.  The round's own record already says this (`CHANGELOG.md:17043`, from codex).  The 2026-09-18 ledger note re-minted the refuted word (3e).

---

## 3. Something ELSE -- the records

**(a) The held question and the brief rest on a misreading of the record.**  The ledger codex entry on `wdcrearmzero` says *"NOBODY HAS RE-READ codex's answer per-row ... It is not a claim that codex addressed this row specifically"*.  I opened it.
* Its verdict line IS the dissent on this row.
* Its other findings appear point by point in the `Round 473 pass 2` block (`CHANGELOG.md:16951`): the L4, the 22-vs-23 archive, the four ledger rows that were missing, and the two-stage ordering.
* The only item that was never acted on is `Md_frozenj` -- which escapes (section 2, Q2).

So the hold question (2026-09-18) asked something answered and corrected on 08-27 and fixed by `#495` on 08-30.  **L4 on `wdcrearmzero`'s `hold_question`, the codex entry, and this brief's "all ratified".**

**(b) MEASURED FALSE: "a regression needs a case that WORKED before ... and there is none".**  This sits at `CHANGELOG.md:16710` (Round 474 pass 2, *"Two records of mine measured FALSE"*, item (a)) and is repeated in HEAD's re-arm comment.

At 32 blocks (65536 B -- the band the ledger's own Correction 2 calls *"precisely the MAXPHYS-sized band real drivers use"*), with one mid-chunk data-port store:

| build | guest-eye wrong | end state |
|---|---|---|
| pre-fix parent `00d546de` | **0 of 65536** | completes, 2 stray bytes left |
| `1f1a02b` | **32626 of 65536**, from lane 32768 | chunk 2 shifted |
| HEAD | 0 | the store is refused |

The "second seat" measured a transfer above 64 KB, where the pre-fix build never delivers chunk 2 at all, and the conclusion was then written for every size.  It is the dropped-qualifier class.  The first draft's "REGRESSION" was right for (32 KB, 64 KB].  **No live defect** (`#495` closed it); L4 in both places.

**(c) HEAD's re-arm comment is stale in present tense, and one sentence is cut in half.**
* *"the data-port WRITE arm above pushes guest bytes with no phase guard and no capacity check ... those bytes are still queued when the refill runs"* -- false since `#495` (guard) and `#484` (capacity).  It now UNDER-states safety and names none of the five supports in 1c.
* "above" is wrong: the write arm is below the read arm.
* *"An adversarial interleaved write DESYNCHRONISES that guest's own"* ends mid-sentence.  `d64a1fc3` (`#475`, 07:03) rewrote that paragraph and dropped the word "transfer.".  `CHANGELOG.md`'s pass-2 block carries the same splice: an orphaned lowercase *"adversarial interleaved write..."* line at `:16978`, and *"was false**, and closure is no shield for false prose."* at `:16990`.
* The 229889-vs-262657 "route" arithmetic describes routes that no longer exist.
* **Suggested replacement:** state the 1c invariant and its supports.  These are `src/` comments, so they batch with the held class.

**(d) Detector records at HEAD.**
* `diff_wdc_identify.c`: the dirty-ring row's rationale (*"exactly what an interleaved data-port write leaves in the ring"*) and the contract bullet *"THE PREMISE ITSELF ... the data-port WRITE arm pushes with no phase guard"* are false since `#495`.  The row's state is now unreachable by any guest (1c).  It is still worth keeping as a tripwire if a producer is ever reopened.
* `kill473_table.txt` is cited at `diff_wdc_identify.c:916` and `gate_offline.sh:1741` (*"ALL EIGHT mutants"*).  **No such file exists** (`git ls-files`).  codex and grok both flagged the name on 08-27.  The table is `regress/artifacts/wdcchunking/killtable_20260827/TABLE.txt` and holds 10 entries.

**(e) Ledger and open list.**
* The agy entry (2026-09-18) records *"THE TWO DEFECTS WERE NOT SEPARABLE AND SHIPPING THEM TOGETHER WAS MANDATORY ... a warrant the round should keep"*.  That is refuted by `CHANGELOG.md:17043` and by the Q5 measurement.
* `wdcaddtoinbufbound`:
  * it is still `in work` with `commits: ae68e29` (the witness only); `#495`'s fix `67120fd6` is recorded under `propagatecpsilent`;
  * its `hold_question` asks where the fix belongs, which `#495` answered;
  * it predicts *"any fix will turn ... `re-arm: refills a NON-EMPTY ring too` RED"* -- MEASURED false: HEAD runs that row green (`32773`).
* `OUTSTANDING_BUGS.md:11645-11660`:
  * *"The row is still LIVE ... the data-port WRITE arm pushes with no phase guard"* -- false since `#495`;
  * an un-struck tail of the struck sentence still reads *"...no row in the shipped detector would see it"*, directly after "All three clauses are now false";
  * *"Both ledger rows close with `witness: none`"* -- false: there is a rung-3 probe witness dated 2026-09-13, and `wdcringambig` closed with a probe.

**(f) Recorded behaviour, quantified rather than new.**  This is not a finding: `#475` chose it deliberately (*"served as ring-empty 0xff"*, `CHANGELOG.md:16837`), and `row_odd_multichunk` pins it.  A mixed-width guest whose access straddles the 32768 boundary gets 0xFF in the lanes past it, and every later lane arrives one access late.  Measured: **32651 of 65533** lanes.  This is out of protocol (32768 is a multiple of every legal width), so no action is asked.

**(g) `wdcrearmwalk`, evidence only.**  D7 walks 96-, 128- and 129-block transfers end to end at HEAD: 5, 7 and 8 re-arms, 0 lanes wrong.  P1 extended with a loop is the "loop-to-exhaustion" row that item asks for.

---

## 4. Dispositions under the late-dissent rule

| # | item | class | disposition |
|---|---|---|---|
| 1 | THE QUESTION | answered, no breach | close the held stage: FALSE at `1f1a02b` (already corrected in `d894e35d`), TRUE at HEAD (measured) |
| 2 | content family escapes at all revisions | the row comment's CLASS claim is measured false: **L4 at least** | **file a small detector round adding P1 and P2** (measured).  **Adjudicator question:** the round classed `Md_wrongoff`, a source-index mutant, as clause (d) and closed its escape as a floor breach.  Does that make `Md_frozenj` L2?  The carrier's bounded DEPENDS-ON (predicates and guard-operand swaps) says no; I lean FILE. |
| 3 | `#495`'s guard has no gated detector; "the only way clause (a) could be met" | measured false | L4 on `#495`'s record, and FILE P3 (or fold it into `wdcsingleleg`) |
| 4 | "there is none" (regression) | measured false | L4, `CHANGELOG.md:16710` and the HEAD re-arm comment |
| 5 | ledger hold question, codex entry, agy "NOT SEPARABLE" | wrong record | L4 |
| 6 | stale HEAD comments, the splice, the ghost `kill473_table.txt` | wrong record | L4, `src/` batch |
| 7 | `OUTSTANDING_BUGS` residuals, `wdcaddtoinbufbound` row | wrong record | L4 |

**No product-code change is asked for.**  `#473`'s three edits are correct, and their remaining safety argument is now carried by five later commits (1c).

---

## 5. Artifacts (session scratchpad -- VOLATILE; copy before any record cites a number)

Base folder: `C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\opuswdc\`

* `killtable_opus\TABLE.txt` -- the 21-cell mutant table, the baseline `cmp` lines, sentinel `KILLTABLE_DONE`, and per-mutant `.out`.
* `fuzz_opus\` -- the search runs (`HEAD.out`, `HEAD.s1normal.out`, `HEAD.s2heavy.out`, `1f1a02b.out`, `1f1a02b.s3heavy.out`, `pre473.out`), the directed runs (`*.directed.out`), the instrumentation diffs (`*.build`), and `no495.a.out` / `no495.b.out`.
* `proposed_opus\TABLE.txt`, `PROPOSED.diff`, `diff_wdc_identify.PROPOSED.c`.
* Harness `opus_rearm_fuzz.c`.  Drivers `setup_base.sh`, `killtable.sh`, `run_fuzz.sh`, `run_scale.sh`, `run_sep.sh`, `run_no495.sh`, `run_proposed.sh`.  Mutators `mutate.py`, `rearm_only.py`, `no495.py`, `propose_rows.py`.  Every mutator refuses unless its anchor matches exactly once.

Suggested durable home: `regress/artifacts/wdcrearmzero/opus5_review_20261009/`.

**Not run, and why.**  I did not run the rung-3 guest at HEAD, because HEAD's "no route" answer rests on the read invariant and 26,315 measured re-arms; one more rung-3 route would add little.  If one is wanted, the cheap one is `#495`'s own witness, which needs the poisoned image noted in `wdcsingleleg`.
