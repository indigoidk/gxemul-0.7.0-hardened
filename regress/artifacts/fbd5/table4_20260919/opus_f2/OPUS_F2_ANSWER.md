OPUS_SEAT_ALIVE_20260919_FBD5F2
First line of CHECKPOINT.md: `# CHECKPOINT -- 2026-09-19 10:3x   HEAD: f685d75 (peer records) > 9c28ca5 #539 receipt (7836071 = #539 n6, the footbridge IRQEnable read ACCEPTED)`

VERDICT: DO NOT CLOSE THE REPAIR CHAIN. 11 of 14 one-edit mutants of the FIXED dev_footbridge.c pass the SHIPPED composite (diff_footbridge.c 149/149 AND footbridge_sites_probe.py 37/37). At least three families sit inside the round's own closure (L2): X1 checks only the announce channel at its width cell; X3 pins re-arm only at NONZERO data and values; and a latched NARROW +0x18c read can leak IRQEnable again (the removed value) with no row seeing it.

## Method (measured, scratch trees only)
* Generator: `mkmut_f2.py`. One edit per mutant, with find-exactly-once asserts. Diffs are saved in `guest/mut_*.diff`.
* Offline: `run_off.sh` -> `OFF.log`. /tmp/gxopusf2x = cp -a SEC/src + build/config.h. The frozen SHIPPED regress/diff_footbridge.c (md5 c2bc0732) was compiled exactly as run_table3.sh does. Logs: `off/diff_*.log`.
* Guest: `run_guest.sh` -> `GUEST.log`. /tmp/gxopusf2 = cp -a build/. The frozen SHIPPED footbridge_sites_probe.py (md5 30078460) was run against each mutant. For every mutant: `rm dev_footbridge.o gxemul`, make, then `[ gxemul -nt dev_footbridge.c ]`. Every BUILD line says FRESH, with a distinct md5 per mutant. Logs: `guest/sites_*.log`.
* FIX baseline: OFF 149 rows, 0 failures. SITES 37 of 37 PASS. The binary is 9fa0c1f9, the same as table 3's.
* Two of my first builds were MIS-BUILT and are not reported. F5/F5b inserted a statement after an unbraced `if` arm, which detached the `else if`, so they redded P0 for the wrong reason. Both were rebuilt in comma form. Separately, the heredoc path consumed a backslash level in the F2/F7 find-text; fixed with chr(92).

## Q2 -- the three candidates the brief named, plus the ones I judged more dangerous

| id | one edit | OFFLINE (149) | GUEST (37) | result |
|---|---|---|---|---|
| F1  | IRQ_RAW decline guard `&& !d->timer_control[0]` (a field X4 never seeds) | 149/149 | 34/37 red N2,N0,NO | KILLED (guest N2; arm S has timer 1 armed) |
| F1b | IRQ_STATUS decline guard `&& d->irq_enable` | 149/149 | 37/37 | **ESCAPED** |
| F1c | FIQ_STATUS decline guard `&& d->fiq_enable` | 149/149 | 37/37 | **ESCAPED** |
| F2  | a LATCHED (repeat) IRQ_STATUS write does `else INTERRUPT_DEASSERT(d->irq)` | 149/149 | 37/37 | **ESCAPED** |
| F2b | a NARROW FIRST FIQ_RAW decline does `if (len != 4) INTERRUPT_DEASSERT(d->irq)` | 149/149 | 37/37 | **ESCAPED** |
| F3  | legal EnableSet write: `if (idata) d->warned_irq_clear_r = 0;` | 149/149 | 37/37 | **ESCAPED** |
| F3b | legal EnableClear write: `if (idata) d->warned_irq_status_w = 0;` | 149/149 | 37/37 | **ESCAPED** |
| F4  | narrow FIRST FIQ_STATUS write, in the latch block: `if (len != 4) d->fiq_status = idata;` | 149/149 | 37/37 | **ESCAPED** |
| F4b | narrow FIRST +0x18c read, in the latch block: `if (len != 4) d->irq_enable = 0;` | 149/149 | 37/37 | **ESCAPED** |
| F4c | narrow FIRST IRQ_RAW write, in the latch block: `if (len != 4) d->irq_status = idata;` | 149/149 | 37/37 | **ESCAPED** |
| F5  | a legal IRQ_STATUS read re-arms its OWN latch when it reads ZERO | 149/149 | 37/37 | **ESCAPED** |
| F5b | a legal IRQ_RAW read re-arms the IRQ_STATUS latch when it reads ZERO | 149/149 | 34/37 red N1,N0,NO | KILLED (guest N1) |
| F7  | every LATCHED +0x18c read returns `d->irq_enable` (the removed value) | 149/149 | 36/37 red N3 | KILLED (guest N3 only: r8 = 0x30) |
| F7b | only a latched NARROW +0x18c read returns `d->irq_enable` | 149/149 | 37/37 | **ESCAPED** |

The log lines are verbatim in OFF.log and GUEST.log. Every escape reads `OFF Fx rc=0 149 rows, 0 failures` and `SITES Fx ROWS=37 of 37 FOOTBRIDGE_SITES_PASS`.

### Grading (my proposal; the adjudicator rules)
* **F4/F4b/F4c -- L2. This is the #499 shape inside its own repair.** Pass 2 ruled width x first-access a FLOOR cell (F1/F20, repaired as L2 by X1). X1 rows that cell on the ANNOUNCE channel only. It checks no field preservation, no interrupt-output count and no return value. So the fix's repair ("no register changes") can be nulled at exactly the cell X1 was built for, and nothing reds. F4b is the worst of the three: a narrow +0x18c read clears IRQEnable, which is an interrupt loss the guest can see. The repair is cheap. In X1, after each access, check all four fields (a `P_STATE_OK` equivalent), require an asserts+deasserts delta of 0, and require rv == 1. P9 already does this for a byte write to IRQ_STATUS, which is why that site is missing from the list above.
* **F7b -- L2 (clause (d), pure-deletion shape: the REMOVED value comes back under a different predicate).** Before the fix, the +0x18c read computed `odata = d->irq_enable`. The shipped detector cannot see it return on a narrow access:
  * P3's repeated byte and halfword reads never read `buf`.
  * X1 reads only the FIRST narrow access.
  * The guest issues word reads only. N3 catches the word form (F7), and only there.

  Repair: when `dec[i].wf == MEM_READ`, read `buf` back after the P-loop's byte and halfword accesses and want 0. irq_enable is already nonzero there (0x30).
* **F3/F3b and F5 -- L2 by the round's own disposition, and also a Q3 hit (see below).** Pass 2's F3/F4 ("a legal read or a write re-arms a latch") were repaired by X3. X3 drives legal reads only at NONZERO seeded values, and legal Set/Clear writes only with data 0. A re-arm conditioned on the other half of either partition passes. Repair:
  * Run X3's widened writes at 0x70, on the throwaway instance, then re-decline all five and require a count of 0.
  * Add one X3 pass with irq_status and irq_enable zeroed, so that the legal reads return 0.
* **F2/F2b -- coverage debt, unless the adjudicator reads "interrupt output untouched" as part of the repair.** The P rows count asserts and deasserts for the FIRST word decline only. The X rows count nothing: their callbacks are no-ops and are never read. So a repeated or narrow decline that drops the IRQ line while status says pending passes. The repair is one line: snapshot irq_asserts and irq_deasserts around the whole P-loop body and around each X1/X4 access, and require a delta of 0. I would take it in-round. It is the only channel on which a decline can hurt a guest that has interrupts pending, and the P rows already name the property.
* **F1b/F1c -- the brief's candidate 1.** As written it is outside the DEPENDS-ON bound, because the decline body reads only its latch, so it is clause (e) debt. It is still the most REALISTIC of the escapes: a guest that writes a status register before enabling interrupts (the reset state) would be declined silently. X4 zeroes irq_enable only for the read site. The repair costs nothing: run X4 at the write sites with BOTH enables zeroed (X4 already builds a fresh instance per site). F1 (timer_control) shows that the guest arm does kill some field-conditioned guards, but only because timer 1 happens to be armed.

## Q3 -- can the new rows and pins pass while the thing they name is false?
* **X1 "len N as the FIRST access announces once"**: the name is true. But the round cites X1 as closing the width cell of the DECLINE, and the decline's other properties at that cell are unpinned (F4, F4b, F4c and F2b ESCAPED). The named property is true; the claimed coverage is false.
* **X3 "legal reads of every sibling re-arm NO latch"**: FALSE while green under F5 (a legal IRQ_STATUS read re-arms when it reads 0).
* **X3 "legal writes and other-register reads re-arm NO latch"**: FALSE while green under F3 and F3b (nonzero legal Set/Clear writes re-arm). These are the rows' own names, so this is L4 at minimum.
* **X4**: F1b/F1c show that "ZERO enable as the first access" is applied at the read site only. The row's name is accurate for what it does. Its header comment ("a latch guard conditioned ... on irq_enable ... lets such an access through") overclaims for the four write sites. L4.
* **X5**: I found no edit that passes it while false (Z4 covers `idata`). I did not attack it further.
* **NO**: it binds each text by ORDER, not by ACCESS. A site whose announce is emitted at a later access, but still in N1..N5 order, passes. I did not build this one; it is contrived and needs deferred emission. Disclose it.
* **Gate pins**: read, not run (no gate_*.sh). They hold against a duplicated green line:
  * the distinct-id pins (`cut -d' ' -f1 | sort -u | wc -l` over GREEN lines);
  * the literal `ROWS=37 of 37`;
  * `^S[1-5] .*ok$`, which cannot match SC1, SA1 or SF*.

  Reading found no weakness in the new pins.

## Q4 -- other things noticed
* The composite's two halves are disjoint by design, and each is blind on the other's axis. 11 of my 14 mutants are invisible both offline and in the guest, because the offline block never reads the results of repeated or narrow accesses and the guest is word-only. The one systemic repair is to follow every access in the P/X blocks with the full state, output and value check, rather than to add more rows.
* The offline block drives only 0x70 and 0 as data, and only nonzero seeded values for legal reads. Any value-partition mutant conditioned on the other side of that partition will pass (F3, F3b and F5 here).

## Final scratch state
* /tmp/gxopusf2x: dev_footbridge.c cmp == GXEMUL-SEC; sentinel cleared ("OFF RESTORED (cmp == SEC), sentinel cleared").
* /tmp/gxopusf2: dev_footbridge.c cmp == GXEMUL-SEC; binary rebuilt fresh as 9fa0c1f9 (== FIX); sentinel cleared ("GUEST RESTORED (cmp == SEC, binary fresh), sentinel cleared").
* Both re-verified by hand after the run: both `cmp` clean, no `.MUTANT` present.
* Nothing was written to GXEMUL-SEC, est/, build/, build-asan/ or /tmp/gxsec-build. No gate was run.

## Seat record
Opus 5 (claude-opus-5[1m]), measuring seat, repair pass of #545.

Read:
* brief_fbd5_f2.md and CHECKPOINT.md line 1;
* SEC dev_footbridge.c (the access function and its HEAD diff);
* regress/diff_footbridge.c (the P/X blocks);
* footbridge_sites_probe.py (arm S and its rows);
* the gate_arm.sh footbridge block;
* run_table3.sh and opus_p2's mkmut_p2.py.

Ran:
* 15 offline compiles and runs (FIX + 14 mutants);
* 15 guest builds and sites-probe runs (FIX + 14 mutants), plus the restore build.

Artifacts, all in this directory: mkmut_f2.py, run_off.sh, run_guest.sh, OFF.log, GUEST.log, off/, guest/.
