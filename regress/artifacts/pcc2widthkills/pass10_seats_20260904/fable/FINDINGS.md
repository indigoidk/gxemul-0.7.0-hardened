(Captured VERBATIM by the main loop from the Fable 5 seat's final message, 2026-09-04 ~13:29.  The seat
could not write this file itself: both its Write tool and a Bash heredoc were blocked by the
subagent report-file guardrail, and it said so.  HTML entities in the transport (&amp;, &gt;) are
un-escaped here; nothing else is changed.)

PASS10_FABLE_ALIVE_20260904

Liveness quote from `_scratchpad/CHECKPOINT.md`:
> **PART 9 DONE + PRESERVED** (`killtable2_20260903/part9/`: three .out with sentinels, build logs,

Tree read: `GXEMUL-SEC` at `b78bb0f` + uncommitted working set. Line numbers matched the brief throughout (`dev_pcc2.c` 749 lines, probe 1114 lines md5 `43471ae2`) — not a pristine-2021 copy.

---

# VERDICT: DO NOT CLOSE — narrowly, and NOT on any defect in the four rows.

**RULE RULING:** The **dissent's core reasoning FAILS** — its plausibility test is the wrong discriminator, and its claim "read as single-operand, the closure is complete" is **measurably false** (`&& idata != 2` is a single-operand form on a body-read lvalue that clean-sweeps 194/194 and is disclosed, not killed). The **main loop's DISPOSITION (ship the row) is RIGHT**, but its **proposed bound is self-refuting**: "PAIRS … where a cell is a reachable guest state" would force rowing `idata==2`, `TxICR 0x37` and `TxCTL 0xff` (all reachable guest states) that the same record *discloses*. Neither side's stated rule is adoptable. The principled, finite, derivable discriminator that includes `pendboth` and excludes `idata!=2` is: **a joint/multi-lvalue cell is in clause (d) exactly when the guarded body's OWN CODE tests that combination (each lvalue at a partition it distinguishes, read together in one operation); cells the body never distinguishes are disclosed under clause (e).** Keep the row; adopt that rule; add ONE contract sentence stating the discriminator. A closing pass cannot assert "zero floor breaches surviving adjudication" while the floor's own scope is this pass's open question.

The four `pendboth` rows: **sound.** Masked `ovfhi` rows + control: **sound.** Product code: **unchanged** (verified). Measurements: match, control misprediction honestly explained and correct. Record: honest except the missing discriminator sentence + minor items.

---

## Q1 — THE RULE QUESTION (at length)

**Setup, verified from source (not ratified):** guard is `if (len != 1 && writeflag == MEM_WRITE)` (`dev_pcc2.c:511`). The guarded body (`:513-543`) reads both pending counts and **tests `> 0` on each** (`:528`, `:533`; `reassert_interrupts` `:277`, `:280`). So `(pending1, pending2)` is a product of two body-tested `{0,>0}` partitions — that is the fact that puts the joint cell on the table.

**Where the dissent fails:**

1. *"`&& !(p1 && p2)` is not an edit anyone writes."* Wrong discriminator. The project's own class-closure amendment ("THE AMENDMENT THAT ACTUALLY ENDS CHAINS") is exactly this shape: *"a cell of one state space left empty … leaving the symmetric cell open … enumerate the full space from the function's own inputs, close every cell in ONE diff."* Three pending cells (neither / T1-only / T2-only) were pinned; the symmetric `(+,+)` was left open. `#499`'s cells were adjudicated by reachability-of-a-symmetric-cell, **not** by plausibility-of-expression. Point 1 is refuted by the carrier the main loop cites.

2. *"arbitrary BOOLEAN COMBINATIONS are exponential → #392."* This half is **correct and important**, but over-shoots. The fix is not "forbid multi-lvalue cells" — it is to bound the enumeration to the partitions the **body itself tests** (a fixed, small product), not a free boolean algebra. And "single-operand is complete" leaks (see below), so the dissent's own escape hatch fails.

3. *"row demand is PER ENUMERATED MUTANT → no row owed."* True rule, **wrong application.** The carrier: *"Rows are owed PER ENUMERATED MUTANT, never per refusing state; two states no enumerated mutant distinguishes collapse into one row."* Once point 1 falls, the conjunction **is** an enumerated (d) cell, distinguished from every existing row's state (no row holds both pending). So the per-mutant rule Opus cites **owes** the row. He wields a rule that supports the row to deny it.

**Where the main loop's bound fails (harder on the author, as asked):**

- **(a) Not finite as worded.** `pending_timer1/2` are `int`; their joint space is 2^64. Finiteness lives in the *predicate's* `{0,>0}` abstraction, not the lvalue. Taken literally the bound excludes its own motivating case.
- **(b) Self-refuting on "reachable guest state."** `idata==2` is a reachable guest state; so are `TxICR==0x37` and `TxCTL==0xff`. By the bound's own "reachable → row it" criterion, all must be rowed — yet the record **discloses** them. The main loop cannot both justify `pendboth` by reachability and disclose `idata!=2`, which is equally reachable. Applied consistently, "reachable guest state" **is** the unbounded growth the dissent fears.
- **(c) The "PAIRS" cap reintroduces #499.** `#499`'s class was 4 axes (width × component × direction × position). A rule that stops at pairs misses a 3-axis cell and pays another pass — the linear-convergence-by-cell the amendment exists to end.

**Measured leak (the sharp finding):** `&& idata != 2` is a **single-operand** clause-(d) form (`idata` is a body-read lvalue; rule (2) draws operands from body-read fields). No row drives a composed value of 2 at any arm (verified: `latch all`=3, `latch all one`=1, `latch all zero`=0; no `0x0002` written value anywhere in the probe). So it **clean-sweeps 194/194** and is disclosed, not killed. The dissent's "single-operand complete" is false as measured. The operative rule is already *not* "kill every single-operand form"; it is "kill the forms the body's logic distinguishes."

**Would my rule have found #499's cells?** Yes. `len` (guard operand → width), `writeflag` (body-read → direction), `relative_addr` (body-read → component/position via the case structure the body tests). Their cross-product **is** the width × component × direction × position space. The main loop's "pairs of body-read lvalues" does **not** reach it (`len` is a guard operand; component is a case-selector, not an lvalue value), so its bound fails to generalize to the very chain it cites. Mine subsumes it.

**The sentence I would put in the rule:**
> *Clause (d)'s DEPENDS-ON closure includes a JOINT cell over two or more of {the guard's operands, the lvalues the guarded body reads} exactly when the guarded body's OWN CODE distinguishes that cell — it tests each lvalue at the partition the cell fixes (e.g. `pending > 0`) and reads them together in one statement or semantic operation. The enumerated cells are the CROSS-PRODUCT of those per-lvalue body-tested partitions — never arbitrary boolean functions of the read-set — and a mutant exempting any single cell whose reachability is MEASURED is a floor breach. Close the whole cross-product in ONE diff and state in the contract which cells are rowed and which disclosed. A value or bit-combination the body never tests as a case (`idata == k`; a byte no conditional distinguishes) is disclosed under clause (e); a cell no access reaches is disclosed by name.*

Finite (product of small body-tested partition counts), derivable from the diff by reading (list the guard operands and the fields the guarded body reads, and for each the value-classes its own `if`s distinguish), non-exponential, and it subsumes single-operand forms, the pending 2×2, and #499's input-space cells.

**Disposition:** KEEP all four `pendboth` rows. My rule makes their inclusion *derived*, not asserted.

## Q2 — the four `pendboth` rows

- **`pendboth arm1` is a SOUND proof both counts are non-zero at the wide write.** `pcc_timer_tick` (`:180`) increments both counts; `DEVICE_TICK(pcc2)` (`:389-392`) calls `reassert` during free-run; `reassert` sets INT only under `pending>0 && IEN` (`:277-282`). Both timers are armed identically, so the same tick advances both — when T2's INT sets, `pending1>0` too. `r4s[1]`=T1ICR=`0x31` proves `pending1>0`; nothing decrements it before the declined wide write (intervening reads run under `step`, host timer stopped). Both non-zero at the write.
- **Load-sensitive?** Liveness yes, in the *same disclosed way* as `pend2` (the poll needs the SIGALRM/DEVICE_TICK; a starved host yields self-naming `no-breakpoint (FAILED FOR SOME OTHER REASON)`, not a false kill). The **value 0x31 is load-stable** (no count race, unlike the old exact-0x81). No worse than `pend2`, which the gate already carries.
- **`M_PENDBOTH` reds exactly `{pendboth decl (0), pendboth rb (0x20)}` — 192/194,** verified in `M_PENDBOTH.out`. Recomputed the landed value: `0x31 &~0x17 = 0x20`, `reassert` never clears INT. Matches.
- **`||` form** (`&& !(p1 || p2)`): caught by **existing** `pend1`/`pend2` — a single non-zero pending makes the write land, reddening those rows. That asymmetry (a single non-zero suffices for `||`, both needed for `&&`) is exactly why `&&` needed `pendboth` and `||` did not.
- **T1-label both-pending** cross cell: not separately rowed; the *symmetric* mutant is caught at T2ICR. A T1-only-exempting mutant is a **named residual → file `pcc2pendbothT1`** (disclose), not a live escape.

## Q3 — masked `ovfhi` rows + control

Mask `& 0x81` keeps bit 7 (count>=8) + CEN and drops the load-variable count low bits (4–6); `0x91 & 0x81 = 0x81`, so counts 8..15 all read 0x81 — correct. **Still kills** any TxCTL-guard mutant that lands the `ovfhi` wide write: `decl` catches *any* landing (value-blind); `rb` catches CEN/bit-7 change (idata=0 clears CEN → 0x80). No landing escapes both. **No longer kills** a landed write changing only bits 1–6 while keeping bits 0,7 — but `decl` still fires, so nothing lands undetected; masking loses no landing-detection. **Control** `M_TXCTL_OVFHI = && !(reg & 0xe0)` is a plausible high-count exemption; `0x81 & 0xe0 = 0x80 != 0` → lands → rows red. It proves masking did not make them vacuous. Right control.

## Q4 — three measurements vs Section 17 predictions

`PRETABLE_pass9.out` on disk == inlined; mtime **11:46:40 predates** `driver.log` 12:30:21 and launch 11:47:03 (test-first order holds). BASE 194/194 predicted+measured. `M_PENDBOTH` 192/194 predicted+measured, red set exactly the two `pendboth` rows. `M_TXCTL_OVFHI` **predicted 190, measured 188** — admitted. **Explanation is correct:** `rb t2ctl/t1ctl b27` hold `0xfc`; `0xfc & 0xe0 = 0xe0 != 0`, so the guard is off there too and the write lands to `0xff`; part 8 had already measured this at 184/190 with the same 6 reds. The prediction was written from intent, not from part 8's red set. Safe direction (caught by more, not fewer); no instrument defect.

## Q5 — smallest edit that passes 194 rows

`&& idata != 2` at the guards — total escape 194/194; no row drives composed value 2 (verified); **every** row stays green. Disclosed by name in the contract, and out of the (correctly formulated) (d) closure because value 2 is not a body-tested case. Siblings the contract also discloses: `TxICR != 0x37`, `TxCTL != 0xff`.

## Q6 — record honesty

**Verified true (audited vs source):** "product code unchanged" — `dev_pcc2.c` vs `b78bb0f` is **comments + one no-op typedef** `pcc2_w_fits_in_warned` (compile-time size assert, zero runtime code); no executable statement changed; the 32/12 numstat is entirely that. `TxICR {0x00,0x13,0x17,0x31}` — all four genuinely held by rows (`0x13` is the `rb/rb4/rb8/brd2` readback preset; not a phantom); live bits 0,1,2,4,5 both ways, 3,6,7 dead. `TxCTL {0x00,0x03,0x11,0x81,0xfc}` — all 8 bits both ways (recomputed). 194 rows: `BASE.out` 194/0-FAIL; gate pins 194 names + 194/194/0 and **PASSES** (`gate14_p10.log` "PASS (760 checks)", GATE_RC=0); "190→194" is vs pass 8, "60→194" vs HEAD — both true. Mutant diffs 2 lines each, binary newer than source, sentinel cleared.

**Owed / imprecise:**
1. **Missing discriminator sentence** (the Q1 gap; reason for DO NOT CLOSE): the record ships `pendboth` (joint IN) and discloses `idata!=2/0x37/0xff` (value OUT) with no stated principle; the main loop's proposed "reachable guest state" line is self-refuting. The contract owes one sentence (Q1). L4/L3, correctable in place — but the *rule* it rests on is a flagship-seat decision, not an author self-adoption.
2. **Named residual:** T1-label × both-pending cross cell → file `pcc2pendbothT1`.
3. **Working-set contamination** (disclosed in numstat): `regress/sgi_de_primop_probe.py` (20/6) is a different device; keep it out of this round's commit.
4. `tools/panel.sh` (3/1) root-shim — fine, but keep in its own commit.

No measurement-refuted sentence found; no count without a deriver.

## Denominator of my zero (what I walked)

`dev_pcc2.c`: full `DEVICE_ACCESS` switch (12 arms), helper, `pcc_timer_tick`, `reassert_interrupts`, `DEVICE_TICK`, width-bit enum, struct, `mvme_pcctworeg.h` defines; diffed in full vs `b78bb0f`. Probe: `session()`, `enc`, `program/program_free`, `setup`, `armval/cval`, all arm builders + sessions, `row()`, `BLOCKS12`. Measured: `BASE/M_PENDBOTH/M_TXCTL_OVFHI.out`, `driver.log`, `PRETABLE_pass9.out` (disk + mtime), `gate14_p10.log`. `gate_arm.sh` diff, CLAUDE.md amendment. Floor cells checked for a surviving breach: pending 2×2 (closed), single-operand `idata` (`idata!=2` escapes → disclosed), `TxICR 0x37`/`TxCTL 0xff` (disclosed). **No fresh mutant table** (read-only seat); the named escapes are derived from the row set + source and are consistent with the measured `M_PENDBOTH`/`M_TXCTL_OVFHI` behaviour. Premises **not** independently settled (named, not ratified): the OpenBSD clock/statclock steady-state claim (corroboration only — reachability is measured directly by the row); an exhaustive tree-wide grep for external pokes of `pending_*` (in-file writers confirmed; the device owns the field).
