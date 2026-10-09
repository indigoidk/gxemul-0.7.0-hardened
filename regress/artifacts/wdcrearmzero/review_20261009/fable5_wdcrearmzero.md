SEAT_ALIVE_20261009_WDC473
# CHECKPOINT -- 2026-10-07 11:3x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)
VERDICT: RATIFY WITH CHANGES (3) -- the fix is right and the held question is CLOSED (the ring is empty at every re-arm at HEAD; at `1f1a02b` it was not, which this seat and Opus found on #473's own pass 2 and #495 fixed); but the SHIPPED detector lets a one-token move of EITHER clamp's bound sweep 128/128 clean (MEASURED, four mutants), the rung-3 witness is blind to it by construction, and the held marker's premise is a wrong record.

Seat: fable5 (Fable 5.1), late REVIEW on `#473` / `wdcrearmzero` + `wdcringambig`, 2026-10-09.
Tree read: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\src\devices\dev_wdc.c` at HEAD `ef577140` (md5 `714071619d8f98e85fe48ae566139345`), plus `git show 1f1a02b:src/devices/dev_wdc.c` for the as-shipped form.  Line numbers below are HEAD's unless marked `[473]`.
RAN / READ are separated in section F.  Nothing under any project tree was written; no index-writing git command; no gate.

---------------------------------------------------------------------------------------------------
## A. THE HELD QUESTION -- can a guest access put bytes in the ring between consumption and the re-arm?

### A1. There is no "between".  (READ)
The re-arm is the TAIL of the read that consumes the last chunk bytes, inside one handler invocation:
`atapi_len -= consumed; atapi_received += consumed;` (:1293-1294) then `if (atapi_len == 0 ...)` (:1312-1319) then the
re-arm (:1359-1466), then the common tail.  The model is single-threaded; no guest access can interleave inside one
`dev_wdc_access()` call.  So the question reduces to: **can ring occupancy differ from `atapi_len` at the START of the
consuming read?** -- i.e. is there a producer or consumer of ring bytes that runs while `atapi_cmd_in_progress == 1 &&
atapi_phase == PHASE_DATAIN` and does not move `atapi_len` in step?

### A2. Every ring producer and consumer at HEAD, derived by grep, not from memory.  (READ)
Deriver: `grep -n 'inbuf_head\|inbuf_tail\|wdc_addtoinbuf\|wdc_get_inbuf' GXEMUL-SEC/src/devices/dev_wdc.c`.

| site | moves | reachable with flag=1 && phase=DATAIN? |
|---|---|---|
| P1 DATAIN arms push (:1460-1462 re-arm, :1797-1798 initial) | head, and `atapi_len` by the same count | yes -- the counted producer |
| P2 data-port WRITE pushes (:1579-1647) | head only | **NO**: `#495` refuses the push when `atapi_cmd_in_progress && atapi_phase != PHASE_CMDOUT` (:1576-1578) |
| P3 IDENTIFY pushes (:1017-1020) | head | NO: only via `wdc_command()`, whose first act is `wdc_new_command_reset()` (:938) -> flag=0, phase=0, head=tail=0 (:915-924) |
| P4 `wdc__read()` direct head advance (:530-541) | head | NO: same route, same reset first (:973) |
| C1 ATAPI read-arm pops (:1198-1214) | tail, and `consumed` | yes -- pops == `consumed` by construction (1/2/4 for len 1/2/4; 3- and 8-byte widths pop 2 and count 2); `#475`'s clamp of `consumed` to `atapi_len` (:1290-1291) matches exactly the pops that fail on an empty ring, GIVEN occupancy == atapi_len |
| C2 sector drain (:1846-1880) | tail | NO: needs `write_in_progress`, which the reset zeroes on EVERY command including `ATAPI_PKT_CMD` |
| C3 CDB dispatch drain (:1739-1742) | tail | only in CMDOUT, and it drains exactly the 12 bytes the `== 12` guard admitted (:1716-1717), so the initial arm always pushes into an EMPTY ring |
| C4 `wdc_new_command_reset()` (:915-924) and the ALT-CTRL SRST arm (:832-835) | head=tail=0 | together with flag=0 -- the re-arm is then unreachable until the next `ATAPI_PKT_CMD`, which resets again |

Everything else a guest can reach mid-DATAIN touches neither the ring nor the ATAPI fields: ERROR/PRECOMP, SECCNT, SECTOR,
CYL_LO/HI, SDH (:1933-2022; a drive-select write changes `d->drive`, the DATAIN state is per controller), STATUS read
(deasserts the IRQ only, :2025-2031), ALT-STATUS read (`status_byte()` only), Drive Address read/write (declined, `#525`/`#494`),
`io_enabled = 0` (`goto ret` before the switch, :1176-1177).  **DMA: none** -- `grep -i dma dev_wdc.c` hits only the
IDENTIFY word-49 comment and a `debug()` string; `bus_pci.c`'s PIIX/VT82C586 IDE wrappers call only `wdc_set_io_enabled()`
(:787-790, :986-989).  Phase lattice: flag=1 implies phase in {CMDOUT, DATAIN, COMPLETED, DATAOUT}, because the reset writes
flag=0 and phase=0 in the same three lines and `ATAPI_PKT_CMD` writes flag=1 and phase=CMDOUT together (:1046-1047); the
re-arm additionally needs phase != CMDOUT (`#477`, :1318-1319), so CMDOUT leftovers cannot reach a DATAIN re-arm -- the only
exits from CMDOUT are the dispatch (drains all 12) and a reset (zeroes).

> **Invariant at HEAD: throughout DATAIN, ring occupancy == `atapi_len`.**  P1 is the only producer and C1 the only consumer
> that can run in that state, and they move in lockstep.  Therefore `atapi_len == 0` at the re-arm means the ring is EMPTY,
> and the refill of min(remaining, 32768) bytes into a 262655-slot ring is never refused.  **Answer at HEAD: NO.**

Two side paths checked because the question named them: `res == 0` (:1765-1777) `break`s out of the `wd_data` arm with the ring
already drained; `res == 2` DATAOUT sets `atapi_len = received = 0`, and a DATA read then completes the command because the
SCSI layer sets `data_out_len`, not `data_in_len`, for those commands (`diskimage_scsicmd.c:891`, `:1287`) -- pre-existing and
not `#473`'s.

### A3. At `1f1a02b` as shipped the answer was YES, through P2 -- and the round's own pass 2 found it.  (READ)
`[473]` :813-873: the write arm pushed unconditionally, and its only diagnostic required `!atapi_cmd_in_progress`.  One 2-byte
DATA store mid-DATAIN grew head without `atapi_len`; the next re-arm refilled behind it and the guest's whole next chunk arrived
shifted.  This is recorded, measured and closed:
* found on `#473`'s pass 2 by the **Fable and grok seats**, measured end to end by **Opus** -- `d894e35d`'s message:
  *"broken independently by the Fable and grok seats ... Opus then MEASURED it end to end: one 2-byte guest store, 65536-byte
  transfer -- committed build 32768 of 32768 bytes wrong"*; the `#473 L4` comment landed in `dev_wdc.c` the same day (:1373-1381);
* rung-3 witnessed 2026-08-30 (`regress/artifacts/wdcaddtoinbufbound/rung3_20260830/`, 20/20 both legs);
* **closed by `#495` (`67120fd6`)**, the phase-keyed refusal at :1576-1578, with the detector's `re-arm: refills a NON-EMPTY ring
  too` row pinning the refill's behaviour on a dirty ring (it killed `Md_emptyguard`).

So the sentence `#473` shipped in its comment ("the ring is empty") was an overclaim, the FIX never depended on it (the refill is
correct on a clean ring and on a dirty one; the dirty ring was a separate write-arm defect), and no line of `#473`'s diff needs
changing.  glm's residual -- "a reset that zeroes `atapi_len` but leaves head/tail" -- does not exist: the only reset helper
zeroes head/tail WITH the flag (:917-923) and never touches `atapi_len`.

### A4. Why a closed question stayed held for three weeks: a wrong record, L4.  (READ)
The ledger marker (`wdcrearmzero`, fable5, 2026-09-18) and this brief both say *"the two Agent seats (opus5, fable5) were never
fired"*, derived from `SEATS.txt`, which counts the eight SCRIPTABLE transports only.  The Agent seats leave no file -- the
carrier's own two-seat counting trap.  Both seats' pass-2 entries sit on the SIBLING row `wdcringambig`, dated 2026-08-27:
opus5 *"PASS 2 -- DO NOT RATIFY AS SHIPPED, the CODE is correct, the DETECTOR is not"* and fable5 *"PASS 2 -- HOLD ... REFUTED
THE BRIEF'S OWN PREMISE"*; `d894e35d` says *"#473 pass 2: 8 of 9 answered"* (kimi lost on both transports).  The panel's brief
names BOTH rows as its subject.  **Correct the marker in place and discharge it with this answer; cross-reference the two
2026-08-27 Agent entries onto `wdcrearmzero`.  Do not copy the brief's premise into the ledger entry written from this file.**

---------------------------------------------------------------------------------------------------
## B. THE ORIGINAL PASS-2 QUESTIONS, answered by the seat the record says never answered

**Q1 -- is the ring empty at the re-arm?**  At `1f1a02b`: NO (A3, interleaved data-port write; fixed by `#495`).  At HEAD: YES, by
the lockstep invariant in A2.  READ (HEAD trace) + the `#495` witness RAN by Opus on 2026-08-30 (cited, not re-run).

**Q2 -- a fifth clause-(d) mutant.**  The round itself reached six (`Md_emptyguard`, `Md5_chunkconst`).  I built FOUR more that
keep the guard and move its BOUND or its OPERAND, and **all four sweep the shipped detector clean** -- section C.  MEASURED.

**Q3 -- `atapi_received += consumed` runs BEFORE the re-arm.**  Verified: :1294 precedes :1424-1426, where the remainder is
`data_in_len - atapi_received` with the updated value, and the refill indexes `data_in[atapi_received + j]` (:1462).  The
detector's `0x3c` marker row (131070 + 2 -> 131072) is live: my control mutant reds its siblings in the same run.  READ + RAN.

**Q4 -- filing the unbounded primitive.**  Right at the time; OVERTAKEN the same day by `#484`, which bounded it (drop-newest,
latched, one slot sacrificed, :245-252), and the contract block already carries that correction (`diff_wdc_identify.c:936-953`).
READ.

**Q5 -- one round, two defects.**  Ship together: yes.  `d894e35d` already corrected "inseparable" to "a two-stage ordering
exists", and the ordering is specific: stage 1 = clamp-only at the re-arm (`= 0` -> `= 32768`, NO refill, the whole transfer
still in the ring from the unbounded initial push, sound up to the ring's 262655); stage 2 = bound the push AND add the refill
together.  Re-arm-first WITH the refill is NOT a safe stage -- it double-pushes chunk 2 onto a ring that already holds it.
REASONED from the two arms; not measured.

---------------------------------------------------------------------------------------------------
## C. WHAT I FOUND ELSE -- the shipped detector does not pin WHERE either clamp's bound is.  (MEASURED)

### C1. The inventory that predicted it.  (READ)
Remainders the shipped rows place at the RE-ARM clamp: 4998 (`q2`), 7232 (`chunk edge`, the only row at the transfer's first
re-arm), 68930 (`rearm_zero` and the dirty-ring row, both at received 131072 = the END OF CHUNK 4 by the row's own comment,
:727-728).  Transfer sizes at the ARM clamp: 10, 12, 64, 512 and 263168 (`stub_datain_len` sites).  **No row approaches 32768
from either side.**  Any bound moved inside (7232, 68930) at the re-arm, or (512, 263168) at the arm, agrees with every row.
The carrier's accept-row lesson, on a relational clamp: one row far past a bound proves a clamp EXISTS, not WHERE it is --
*"if this window got smaller, which row reds?"*  Here: none.

### C2. The table, against the shipped detector (`diff_wdc_identify.c` at HEAD, 128 rows) and HEAD `dev_wdc.c`.
Built in my own WSL scratch `/tmp/fable473` (sources `cmp`/md5-identical to GXEMUL-SEC; gate 2's exact compile line:
`-O2 -std=c99 -I src/include -I src/include/thirdparty -ffunction-sections -fdata-sections -Wl,--gc-sections`).  Each mutant is a
regex that must match EXACTLY ONE site or the run is scored FAULT; the binary is checked `-nt` its source.  Baseline: `128 rows,
0 failures`, `WDC_IDENTIFY_PASS` (the 22 `FAIL @@SELFCHECK@@` lines are `#551`'s covered-failure self-check and are excluded by
label; the gate reads the summary and the token, both green).  Logs: `scratchpad\fableq\measured_20261009\ship.txt`,
`ship_<mutant>.log`.

```
  mutant                 edit (one token, one site)                         shipped detector
  ctrl_rearm32767        re-arm  `atapi_len = 32768;` -> `32767;`           KILLED   3 red / 128   (positive control)
  M1_opswap_received     re-arm  `atapi_len > 32768` -> `atapi_received > 65536`   ESCAPED  0 red / 128
  M2_rearm_relax65536    re-arm  `atapi_len > 32768` -> `atapi_len > 65536`        ESCAPED  0 red / 128
  M2b_arm_relax65536     ARM     `atapi_len > 32768` -> `atapi_len > 65536`        ESCAPED  0 red / 128
  M3_rearm_lower16384    re-arm  `atapi_len > 32768` -> `atapi_len > 16384`        ESCAPED  0 red / 128
```

### C3. Guest-visible consequence.  (READ -- traced through the register read path; the emulator was not run)
Under `M2`, every transfer above 65536 bytes meets a re-arm whose remainder lies in (32768, 65536]: the whole remainder is
pushed, `atapi_len` = that remainder, and the byte-count registers report **32768** because the READ path clamps
(`if (x > 32768) x = 32768;`, :1974-1976, :1994-1996).  The guest drains 32768, `atapi_len` stays > 0, and there is no re-arm
and **no interrupt** for the rest of the chunk.  An interrupt-driven driver (NetBSD's `atapi_wdc` PIO path waits for INTRQ per
DRQ block) times out -- `wdcrearmzero`'s own stall, restored across the band the round fixed, by one digit.  `M2b` is the same
symptom for transfers in (32768, 65536] at the initial arm.  `M3` clamps a (16384, 32768) remainder UP to 32768 and the refill
reads past `data_in` -- `Md5_chunkconst`'s heap-over-read class.  `M1` misbehaves only at the transfer's FIRST re-arm (received
<= 65536), which is the one every real transfer in (32768, 65536+32768] takes.

**The rung-3 witness cannot see any of them, by construction.**  Its observable is CYL_HI after the first re-arm of a 192-block
transfer, i.e. `(min(atapi_len, 32768) >> 8) & 255` (`wdcrearmzero_rung3_probe.py:11`, `:227`; `RESULT.md`): remainder 65536,
under `M2` unclamped, CYL_HI reads **0x80 exactly as on the fix**.  It discriminates 0 from non-zero and nothing else.  And it is
wired into no gate (`grep wdcrearmzero regress/*.sh`: nothing), so today nothing in the battery defends the bound at all.

### C4. The repair, MEASURED in a scratch COPY of the detector (never the repo).
Four rows, one on each side of each clamp, adjacent to it: re-arm remainder 32769 (expect `atapi_len` 32768, occupancy 32768),
re-arm remainder 32767 (expect 32767 / 32767), arm transfer 32769 (occupancy 32768), arm transfer 32767 (occupancy 32767).
`{32767, 32769}` pins a bound as tightly as it is observable (`> 32767`, `>= 32768` and `> 32768` are the same clamp).
Identity count 128 -> 134.  File: `measured_20261009\diff_wdc_identify.fb2.c` (the `fb:` labels are scratch names; all under
the 38-column width).

```
                         shipped (128)   +just-past rows (131)   +just-below rows (134)
  ctrl_rearm32767        KILLED 3        KILLED 5                KILLED 5
  M1_opswap_received     ESCAPED         KILLED 2                (not re-run; killed at 131)
  M2_rearm_relax65536    ESCAPED         KILLED 2                KILLED 2
  M2b_arm_relax65536     ESCAPED         KILLED 1                KILLED 1
  M3_rearm_lower16384    ESCAPED         ESCAPED 0 / 131         KILLED 2
```
The middle column is the measurement that matters for the design: a just-PAST row alone cannot see a LOWERED bound, because
32769 clamps correctly under any lowered bound.  Both sides are owed.  Logs: `fb.txt`, `fb2.txt`, `fb_<m>.log`, `fb2_<m>.log`.

### C5. Grading, and the one point I hand to the adjudicator.
"A bound relaxed" is clause (d)'s own worked example, applied to the predicate the fix DEPENDS ON (the clamp whose repair `#473`
changed from `= 0` to `= 32768`), and four such mutants sweep the SHIPPED detector clean.  **That is a clause-(d) floor breach of
shipped material -> L2 -> a follow-up commit under the late-dissent rule's disposition 2, not under `#473`'s number.**  The
tension to rule on: the 2026-09-25 three-region reading (below / at / past) would say the "past" region is discharged by one row
at 68930.  The measured sweep says the region's POSITION is what matters and one far row does not pin it; the carrier's own
accept-row rule says the same.  I recommend L2 and the four rows; if the adjudicator reads it as clause-(e) debt, it is still a
filed row with a measured kill table ready.

---------------------------------------------------------------------------------------------------
## D. RECORDS -- corrections in place (L4), each with its warrant
1. `ledger.json` `wdcrearmzero` fable5 2026-09-18 marker: *"never fired"* is false (A4).  Discharge; cross-reference the two
   2026-08-27 Agent entries from `wdcringambig`.
2. Contract block `diff_wdc_identify.c:959-960` and `CHANGELOG.md:17256` -- *"the rows pin the FIRST re-arm"*: the shipped re-arm
   rows sit at the END OF CHUNK 4 (received 131072, by the row's own comment at :727-728) and at a synthetic 35002; the transfer's
   first re-arm is held only by `chunk edge` with a sub-clamp remainder of 7232.  Say "one re-arm per row, at the fourth chunk
   boundary"; the ambiguity is exactly what let the bound go unpinned.
3. `regress/artifacts/wdcrearmzero/rung3_20260913/RESULT.md`: disclose that the oracle is the READ-clamped byte count and
   therefore cannot see an over-push (`atapi_len > 32768`) at the re-arm (C3).
4. `wdcrearmwalk` (open, no commits) is the multi-re-arm WALK; the bound-position gap in C is a different class and should not be
   folded into it.

---------------------------------------------------------------------------------------------------
## E. THE PREMISE AUDIT the brief asked for
`WDC_MAX_SECTORS 512`, `WDC_INBUF_SIZE (512*(WDC_MAX_SECTORS+1))` at `dev_wdc.c:47-48` = 262656 = exactly 513 blocks: holds
(READ).  minimax's objection stands as method -- the constant was asserted, not inlined, in a packet-fed brief.

---------------------------------------------------------------------------------------------------
## F. RAN versus READ, and limits
RAN: the shipped detector against HEAD `dev_wdc.c`, 5 mutants x 3 detector variants, 16 builds and runs in `/tmp/fable473`;
every log, the scratch detector copies and the baseline md5 copied to `scratchpad\fableq\measured_20261009\` (durable).  Scripts:
`setup473.sh`, `mut473.py`, `run473.sh`, `addrows473.py`, `addrows473c.py`, `drive473*.sh` beside this file.
READ: the HEAD and `1f1a02b` handlers end to end (every exit path, the `ret:` tail at :2050-2069), `#474`, `#495`, the ledger
rows, `d894e35d`'s message, the kill-table artifacts, the witness probe and its RESULT.md.
NOT RUN: the emulator.  C3's consequences are traced through the register read path, not observed on a guest; the witness's
blindness is derived from its own stated oracle.
LIMIT: A2's invariant is a reading over the producers and consumers the grep deriver finds; a producer it does not name would
break the argument at that site.  `M1` is the DEPENDS-ON operand-swap form, not a likely maintainer edit; `M2`/`M2b`/`M3` are the
canonical bound moves and are one digit each.
Apparatus note for the record: my first scratch-row insertion put real newlines into C `printf` strings because `re.sub`
processes backslashes in the REPLACEMENT -- the carrier's one-backslash-level trap by a path it does not list; fixed with
`str.replace` and the build error was the tell, not a wrong number.
