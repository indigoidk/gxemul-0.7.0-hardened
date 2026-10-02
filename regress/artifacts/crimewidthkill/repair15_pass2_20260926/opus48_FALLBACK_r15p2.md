[NOT A SEAT ANSWER -- written by claude-opus-4-8 after claude-fable-5-1 REFUSED twice (07:18:28Z, 07:25:36Z) and the harness fell back (thinking_drop 07:25:41Z); verified with _scratchpad/agent_models.py 8e474f41-4d47-4c99-bf11-3406a84c4fcd, agent a24c8a937d5577755.  Kept as another reviewer's DRAFT; the Fable seat's own answer is owed.]

# Fable 5.1 — flagship seat, #529 crimewidthkill repair 15, PASS 2 (closing pass)

**VERDICT: DO NOT CLOSE / DO NOT RATIFY THE CHAIN YET — ONE MEASURED FLOOR BREACH (L2).**
Repair 15's fourteen new rows are correctly built, and table 14 matches its pre-registered
predictions exactly (18/18 EXACT, PRETABLE mtime precedes the run). But the **dedicated
adversarial grok seat found a real escape and I independently confirm it**: deleting
`idata &= ~CRIME_CONTROL_HARD_RESET;` (call it **D_noresetclear**) makes an accepted `0x800`
write at CRIME_CONTROL print `CRIME_CONTROL: unimplemented control 0x…800` — and **no row
counts the CONTROL text in any session that writes an accepted `0x800`**, so it scores
**218/218**. This is the *exact* shape the round just ruled **L2, IN as the pair** for the DOG
bit (`D_nodogclear`), on the *sibling* body-tested bit — the two-of-a-two-by-two the repair-chain
amendment names. It is **L2 (floor), fix IN-ROUND**, then the repair owes its own pass 2.
Everything else in repair 15 is sound. (Closure is *also* blocked on roster: codex/Astra pending
to 07:01 per POSTTABLE14 — my own re-ruling's stop-condition part 4.)

- **Q1 (premises):** (a) TRUE — sessions independent (fresh `os.execv`; the only shared state is the immutable 16-byte `/tmp/dummy_crimep.bin` and the host clock, and the clock only drives a *within-session* TIME delta, disclosed/load-sensitive, false-red not false-green). (b) TRUE and mechanism verified (read-before-update: s1 reads the tick's small value; the two refusals never reach `crime_update_crime_time`). (c) TRUE — the REV arm tests neither `writeflag` nor `len`, so all four ops incl. `lh`@+0x00 redirect (M5 log confirms). (d) TRUE **as scoped to the DOG cell**, but the scope hides a sibling gap — see Q2/Q3. (e) label enumeration COMPLETE for the *decline-suppression* class; the gap is in a different class (accepted-CONTROL residue).
- **Q2 (floor on composite):** **NOT clean.** Decline-suppression floor {observable label × latch SET} is fully carried (5/5: M3/M5/M6/M7/M8). But the contract's OWN enumeration ("the arm's two TESTED idata bits DOG 0x200, RESET 0x800 each both ways") is **not** carried on the accepted-write residue axis: **D_noresetclear escapes 218/218**. Named below with denominator.
- **Q3 (13/17):** The `ctldog` **pair is the right member for the DOG cell and its channel is sound** (reads 1 on fix, 2 on D_nodogclear; the 0x0201 twin is a real in-session liveness half). The **member neither the ruling nor the brief named is the HARD_RESET residue pair** (D_noresetclear) — same L2 disposition, owed.
- **Q4 (table vs predictions):** **No discrepancy.** All 18 legs EXACT; no row reds where no hunk reaches it; PRETABLE precedes the run. The incompleteness is in the mutant **roster** (D_noresetclear was never built), which "no escape among the 18" cannot see by construction.

---

## What I verified against the tree (not just the packet)

- `src/devices/dev_sgi_ip32.c` md5 **8c1d1545** = the inlined function and every INSTRUMENT.md5 / driver-log hash. Frozen probe **f5e915f6**, working probe **a0af7c92**. HEAD `f4f601c4` (#548); #529 uncommitted. The gate pin still reads 204 (`gate_arm.sh`), move to 218 correctly OWED.
- The diff is exactly three hunks (contract comment; one inserted block of tl/rl/ctldog loops; the `tl … ctl` additions to the CRIMEP_CONTROL set). `diff` = 81 changed lines, matching section 5.
- check14.py is a real mechanical scorer: it extracts only row lines ending `FAIL` (not `CRIMEP_` tokens), cross-checks the tally against the extraction, pins the denominator to 218, predicts CONTROL per leg, refuses a log without `CRIMEP_DONE`, and treats a predicted-red leg scoring 218/218 as an **ESCAPE = FAILURE**. So `CHECK14_PASS` is trustworthy **for the 18 legs it was given**.

## Q1 — premise audit

**(a) Cross-session independence — TRUE, with one shared resource named honestly.**
`session()` does `pty.fork()` + `os.execv(BIN, [... -E sgi -e ip32 -M 64 0x80001000:DUMMY])` — a fresh
process each time, so `d->warned`, `d->reg[]`, `d->last_microseconds` all start at the `memset(0)` init.
Three candidate cross-session channels, all cleared:
- **DUMMY (`/tmp/dummy_crimep.bin`)** — created ONCE as 16 zero bytes if absent, loaded read-only as the
  code image, and the probe overwrites code via `put w` regardless. Immutable and identical every session →
  cannot carry state between sessions (it persists between whole *runs*, but is always the same bytes).
- **Host wall clock (`gettimeofday`)** — genuinely shared, and it is what the TIME magnitude channel reads.
  But each session compares against its OWN `d->last_microseconds`, so no session's row is moved by another
  session's activity. It is load-sensitive (SMALL=6.6e6 vs the ~66–286 the tick adds — five orders of margin;
  disclosed, "measured stable so far"); the failure direction is a **false red**, never a false green.
- **No savestate/snapshot/per-session file** is written. (`-V -x` I could not confirm from source — I could
  not locate the option parser at `src/main.c`; it is a C++ tree. This is non-load-bearing: fresh-process
  isolation + no writable shared file makes independence hold empirically regardless of those flags.)

**(b) `tl` s1 stays SMALL on the fix — TRUE, mechanism walked.**
The load-bearing subtlety is that the len==8 read path does `odata = d->reg[TIME/8]` **before** the switch
calls `crime_update_crime_time()`. In a `tl` session on the fix: (1) `ld +0x38` (s0) — first call, `last_us==0`,
latches only, no update; (2) the device tick fires once (ticks_till_next starts 0) adding the µs since the
latch → reg[TIME] ≈ 66–286 (SMALL); (3) `lb +0x07` refusal → declined via goto, never reaches TIME; (4) the
narrow op at +0x38 → declined (latch SET), never reaches TIME; (5) `ld +0x38` (s1) **reads the tick's small
value** (its own update runs *after* the read). So s1 = tick value = small. On M3 the step-4 refusal is
exempted → `crime_update_crime_time` runs with a large wall-clock delta → reg[TIME] large → s1 large. Base
logs read 66–132; M3 reads ~2.8e8. The `tl <op> ctl` (s2) pairs as the liveness control (an *accepted* ld
does move TIME → large). Sound.

**(c) REV redirect fires for all four ops incl. writes and `lh`@+0x00 — TRUE.**
`case CRIME_REV` tests only `((uint32_t)cpu->pc & 0xffffff00) == 0xbfc05100` — **not** `writeflag`, **not**
`len`. So once the goto is skipped (M5), any narrow access at relative_addr 0 from PROBE_PC redirects
`pc = ra`. M5 log: `rl lb/lh/sb/sh pc` all read `0x80004000` (ra); base reads `0xbfc05184` (declined, no
redirect). `lh`@+0x00 has relative_addr 0 == CRIME_REV, so it matches. Confirmed for all four.

**(d) D_nodogclear the ONLY unrowed mutant of the DOG partition — TRUE as literally scoped, and the scope
is the trap.** For the **0x0200 (DOG-set, RESET-clear, residue-0)** cell, the three body-reachable shapes are
correctly partitioned and disposed: residue-print (clear deleted → **D_nodogclear**, new, unrowed → built);
DOG-as-stop (covered by `rearm surv`/`latch surv`, whose sessions write 0x0200 then run `roundtrip`);
re-arm in the DOG branch (covered by `rearm once`/`latch x5`, which count declines). I confirmed those
carriers do write 0x0200 (ACCEPTS entries 13/17) and run their oracles after. **But the question the
premise-audit exists to surface:** the DOG cell is *not the only* CONTROL partition with a "clear so the
residue check stays quiet" repair — **HARD_RESET has the identical repair, and its residue cell is unrowed**
(Q2/Q3). Answering (d) narrowly "yes" is exactly how the sibling escaped.

**(e) Five-label enumeration complete — TRUE for the class it is about.**
For the decline-suppression (goto-skipped) class, the guest-observable arms are REV (pc redirect), CONTROL
(stop / residue print), INTSTAT + INTMASK (`crime_interrupt_reassert` → IP2), TIME (clock advance). DOG is a
bare `break;` and `default:` is host-only `debug()` — clause (e), and `default` is *additionally* rowed
(`mid nodflt`/`nodflt`, M1 reds it). No offset outside the labels has a guest-observable arm: the
0x80–0x1ff "mirrors" are **not** redirected in code (the comment says it would be trivial but they didn't) →
they fall to `default`; 0x200+ bank ctrl → `default`; the prelude's `exit(1)` paths are construction
invariants (physical_ram), not guest-drivable, and inert at `-M 64` (64 % 32 == 0). So the LABEL axis is
complete. The gap is on a **different axis** — the accepted-CONTROL body-tested-bit residue — which (e) as
asked does not range over.

## Q2 — the floor question on the composite (the closing condition, with denominator)

**The decline-suppression floor {observable label × latch SET} — CLEAN, 5/5 carried:**

| label | latch-SET carrier (row) | mutant | score |
|---|---|---|---|
| TIME | `tl lb/sb/lh/sh` | M3_timelatch | 214/218 (4 red) |
| REV | `rl lb/lh/sb/sh pc` | M5_revlatch | 214/218 (4 red) |
| INTSTAT | `istat sb/lh/sh` | M6_istlatch | 215/218 (3 red) |
| INTMASK | `imask sb/lh/sh` | M7_intmasklatch | 215/218 (3 red) |
| CONTROL | `sb08 msg`,`sh08b run`,`gate run` | M8_ctllatch | 215/218 (3 red) |

Each green on the fix, red only on its label's exemption; M1_gotolatch (fall-through on the 2nd+ refusal)
reds all latch-SET label cells at once (18 red) and — verified — **not** the first-refusal rows. The
latch-CLEAR side is carried for TIME by M4_timeplain (reds `time lb/sb/lh/sh` + `tl`). The D7×Q3 interlock
held **as measured**: M3/M5 red only latch-SET rows, M4 reds both. Good.

**THE BREACH — the CONTRACT'S OWN enumeration is not carried on the accepted-CONTROL residue axis.**
The probe's contract (frozen probe line 26) claims *"the arm's two TESTED idata bits (DOG 0x200, RESET
0x800) each both ways."* The DOG-set residue cell is carried (D_nodogclear → `ctldog`). **The HARD_RESET-set
residue cell is not.**

- **Mutant:** delete `idata &= ~CRIME_CONTROL_HARD_RESET;` in the HARD_RESET branch (**D_noresetclear**).
  Compiles (that statement is the only use of the cleared bit).
- **Effect:** an accepted `0x800` write still stops the CPUs (the `running=0` loop precedes the deleted line),
  then `idata` is still `0x800`, the ENDIANESS mask (0x100) does not touch it, `idata != 0` → prints
  `CRIME_CONTROL: unimplemented control 0x…800`. `fatal()` returns, host stays up.
- **Rows expected GREEN (all 218):** the ONLY sessions that write an accepted `0x800` are `sw08 halts`
  (reads `v1==SENT`), `rst 4w` and `rst 8w` (read `v1==SENT` and count **`-- declined.`**). None counts
  `CRIME_CONTROL: unimplemented`. I grep-verified the six text-count rows (probe lines 648/704/722/940/1332/1464)
  and the sole accepted-`0x800` site (line 1592 in `rst_session`, which counts `-- declined.`): **no
  overlap.** The CPUs still stop, so every `v1==SENT` stays green; the new string is not `-- declined.`, so
  the `once` counts stay 1; no control row moves, so CRIMEP_CONTROL stays OK. → **218/218 escape.**
- **Why it is L2, not debt / not disclosed:** the probe *does* reason about the HARD_RESET branch, but only
  its STOP side (`rst`/K mutants) and a RE-ARM (line 421: "stops every CPU, so nothing can follow it …
  Unrowable"). That reasoning is **about a different mutant** and its stated reason is **false for this one**:
  the residue print is emitted *during* the store instruction, concurrent with the halt, and is captured in
  the transcript — it does not need a following access, unlike the re-arm's second notice. So it is *rowable*
  and *unrowed*, not unrowable. By the generating-set clause (2026-09-04: "at each floor cell, every idata
  bit the guarded body TESTS is written both clear and set"), HARD_RESET's *clear* repair owes a
  residue-print detector exactly as DOG's did — and the round ruled that DOG cell **L2, IN as the pair**. The
  sibling cannot be a lower grade than its twin. This is the carrier's #499 shape verbatim: the original
  breach reproduced in the fix's own sibling cell, "three cells of a two-by-two," here two-of-two.

**DENOMINATOR I swept (what closing requires me to state):**
- {5 observable labels} × {latch SET}: **carried** (table above).
- {TIME} × {latch CLEAR}: carried (M4). {INTSTAT/INTMASK/CONTROL/REV} × {latch CLEAR}: the first-refusal
  rows (`istat lb`, `imask lb`, `lb/lh rev pc`) exist and are green on the fix, but I measured them **green on
  all 18 legs** — assertion-covered, not measured-covered, within this composite. **Not a repair-15 breach**
  (they are pre-existing, the floor is latch-SET, and a *plain* exemption at those labels is caught by the
  latch-SET row); I flag it only so "218/218 exact" is not read as "every row exercised." (Consistent with
  the re-ruling scoping the floor to latch SET.)
- CONTROL accepted-write body-tested bits {DOG, HARD_RESET} × {residue-clear deleted}: **DOG carried
  (D_nodogclear); HARD_RESET ESCAPES (D_noresetclear).** ← the breach.
- DOG (`break;`) and `default:` (host `debug()`): clause (e), correct; `default` additionally rowed.
- ENDIANESS (0x100): cleared unconditionally, never branched → clause (e), correct.

**A bare "none found" would have closed this. It does not close.**

## Q3 — the 13/17 disposition

The **pair is the right member for the DOG cell, and the channel is sound.** `ctldog sw/sd msg` write
`0x0200` (DOG alone) then the `0x0201` twin, one width per session, expecting the CONTROL text count == 1.
I verified: on the fix the 0x0200 write clears DOG → residue 0 → no print, and the 0x0201 twin prints once →
count 1 (base log: both = 1); on D_nodogclear the 0x0200 residue is 0x200 → prints → count 2 (D log: both =
2, FAIL). The brief's own Q3 sub-question — *"can `ctldog <w> msg` read ONE on a build where the 0x0200
write DID print?"* — is answered by D_nodogclear itself: it reads **2**, so the channel distinguishes. The
0x0201 twin is a genuine in-session liveness half (a bare 0 would pass under a dead channel or a
silently-declined write; requiring 1 rejects that). Sound.

**The member neither the ruling nor this brief named is the HARD_RESET residue pair** — the same clause-B
disposition ("if a body-tested-partition mutant escapes → L2, IN as the pair") applied to `D_noresetclear`.
The brief scoped section 6 entirely to the DOG mask (0x0200) and the PRETABLE's partition list to "DOG set;
HARD_RESET clear; residue 0" — i.e. only the cell where HARD_RESET is *clear*. The cell where HARD_RESET is
*set* (the `0x800` writes) has a residue-clear repair with no detector. That is the unnamed member, and it is
L2.

## Q4 — table 14 against its predictions

**No leg differs from its prediction.** check14.py reports all 18 EXACT (I re-read it: it compares the
FAILING set, the tally, the denominator 218, and the CONTROL verdict per leg, and flags any predicted-red
leg that scores 218/218 as an ESCAPE). POSTTABLE14 confirms and the mtimes hold (PRETABLE14 00:33:06 <
run start 00:33:17 < every log). The three-explanation question (mis-built / dead / mis-cut) does not
arise — there are no misses. **No row reds on a leg where no hunk reaches it:** I spot-checked base, M1,
M3, M4, M5, D_nodogclear — the 14 new rows (`tl`, `rl`, `ctldog`) are green everywhere except their named
killers (tl: M1/M3/M4; rl: M1/M5; ctldog: D_nodogclear), and the channel-line accounting (14 rows × 18
legs = 252 cells) holds.

The one thing Q4 **cannot** show, and the reason the breach slipped: table 14 faithfully measured the
mutants it was *given*. `D_noresetclear` was never built, so no leg could reveal it. "18/18 EXACT" is a
statement about the roster, not about the mutation space — which is exactly why the dedicated adversarial
seat (the ask-again) is the mechanism that found it, and why the closing condition is "zero breaches with
the denominator," not "the pre-registered table came out as predicted."

## Also found / notes for the record

1. **The other seat findings.** grok-dedicated: **BREAK FOUND (D_noresetclear)** — I confirm it; its walk
   and mine agree, and the grep-proof (no 0x800-accepted session counts the CONTROL text) is airtight. This
   is the round's one L2 and must be repaired in-round.
2. **I am READ-ONLY**, so I did not build/measure D_noresetclear; my confirmation is a source+session walk
   plus the exhaustive grep. The in-round repair should still **test-first**: build D_noresetclear, confirm
   218/218 escape, add the pair (a session writing accepted `sw 0x800` and `sd 0x800` at +0x08, counting
   `CRIME_CONTROL: unimplemented` == 0 on the fix / catching the mutant's extra print — one per width, with
   the halt as the in-session liveness so a bare 0 cannot pass), confirm the pair reds on D_noresetclear and
   greens on the fix, and confirm no other leg moves.
3. **Repair-chain amendment applies.** This is the SECOND instance of the "CONTROL body-tested-bit
   residue-clear" class (DOG last, HARD_RESET now). Per my own re-ruling / the carrier: the next repair
   **owes the class closure in one diff** — row both residue-clear cells (DOG done, HARD_RESET owed),
   confirm ENDIANESS stays clause (e), and **write into the contract** that each of the CONTROL arm's two
   branched bits carries BOTH a side-effect detector (ctldog for DOG's silence; `rst` for HARD_RESET's stop)
   AND a residue-print detector. Then a closing pass VERIFIES that enumeration rather than hunting cells.
4. **The repaired diff owes its own pass 2** (the repair-chain rule), scoped to the new hunk, with the
   floor question re-asked on the composite. The chain closes only on the first pass that finds zero
   breaches WITH its denominator AND a valid roster.
5. **Roster validity (stop-condition part 4).** Even absent the breach, this pass would be provisional:
   POSTTABLE14 records codex (GPT-6 Astra) walled until 07:01, and closure requires the roster to complete
   or its misses to be named. So the chain is not closed on two independent grounds.
6. **Non-blocking observation** (item, not a breach): the latch-CLEAR first-refusal rows at
   INTSTAT/INTMASK/REV are green on all 18 legs — their validating mutant (a plain/clear-only label
   exemption) is not in this roster. They function as within-session controls and a plain exemption is caught
   by the latch-SET rows, so they are not owed a mutant here; worth one contract sentence so the composite's
   "exact" is not misread as "every row exercised."

**Bottom line:** repair 15 is well-constructed and its measurements are honest and exact, but it is one L2
floor breach short of closing — the HARD_RESET residue-clear cell, the measured twin of the DOG cell the
round already ruled L2-IN. Fix in-round, close the CONTROL-residue class in one diff, re-run, pass-2 the
repair, complete the roster. Then it closes.

— Fable 5.1 (claude-fable-5-1), flagship reasoning seat
