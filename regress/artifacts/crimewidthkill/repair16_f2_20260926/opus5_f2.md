OPUS5_F2 -- #529 repair 15 adjudication pass (F2) and repair 16. Measuring seat: Opus 5.5, Agent tool.

**VERDICT: REPAIR 16'S ROWS ARE RIGHT, AND ONE ADOPTED OPTION OF MINE IS WRONG AS FRAMED.**

- **The dispositions.** I uphold the conclusion of every disposition except one, and refine four wordings.
- **The one to overturn is the F20/D5 "value-anchored text in the ctldog/ctlrst rows".** It is my own repair-15
  proposal. As a substitute for the prefix count it is measured blind to `H_noresetclear`, which is the round's own
  L2 cell.
- **The eight new rows.** All eight now carry a measured kill. `ctlrst sw halt` gets its kill only from my
  `S_rst4clr` (224/226), and that run also reports CONTROL=FAIL.
- **The class closure** holds for the residue COUNT: 3 clears x 2 latch states x 2 widths. It does not hold for the
  residue CHANNEL. `M_ctldebug`, which demotes the arm's `fatal()` to `debug()`, passes all 226 rows (measured).
  The reason is that every session that counts the text is stepped.
- **Wrong records to correct:**
  - E7's md5;
  - E10's row count;
  - the latch state claimed for the rearm session;
  - the universal claim "none watches the line fall".

Everything below is under `repair16_f2_20260926/opus_f2/` unless another path is given. The probe measured is repair
16's frozen `table16_20260926/crime_width_probe.table16.py`, md5 **5f770991**. The build tree was my own clone
`/tmp/gxopus_r15p2`.

## Q1 -- one line each

- **F1 UPHOLD, L2.** `H_noresetclear` passes all 218 rows (table 15a) and scores 222/226 in table 16, red on exactly
  the four HARD_RESET residue rows. The arm tests HARD_RESET as a case, and nulling its clear is the (d) shape this
  round already graded L2 for DOG.
- **F2 UPHOLD, as a strengthening (see D4).** `E_noendianclear` goes from 218/218 to 224/226. My `E_endlatch` (the
  clear skipped only with the latch SET) scored 225/226, red on `rearm ctl msg` only. So each ACCEPTS row carries its
  own latch-state half.
  **REFINE:** the contract lists ENDIANESS next to the two TESTED bits and never says it is clause (e). Say so, or the
  grade is lost at the next edit.
- **F3 / F17 UPHOLD: not rowed, disclosed** (see D2). The scoped header claim is **true**. My static replay of
  5f770991 (`static_census_5f770991.out`) reaches every width x direction cell at INTSTAT and INTMASK in at least one
  latch state. In the full product each label reaches 4 of its 8 cells, and the eight empty cells are unchanged from
  the 218-row probe.
- **F4 UPHOLD.**
  - `L_dogclr` scores 225/226, caught by `rearm ctl msg`.
  - `L_rstclr` scores 224/226, caught by `rst 4w/8w msg`.
  - The wrong reason, "the CONTROL arm reads no latch", is gone from the contract (checked in the diff).
- **F5 UPHOLD the rejection.** The static replay of 5f770991 shows both sessions hold `0x0200` at both widths:
  - the rearm session (S38) has all ten accepted CONTROL writes with the latch SET;
  - the latch session (S52) has all ten with it CLEAR.

  Each variant has a row that sees it:
  - a DOG stop reds `rearm surv` or `latch surv`;
  - a re-arm reds `rearm once`;
  - a pre-set reds `latch x5` or `latch said`.
- **F6 UPHOLD the rejection.** This has been measured twice. My device-side census logs no TIME update at either
  refusal, and s1 equals the tick's value.
- **F7 UPHOLD.** After the first firing, `ticks_till_next` = 0 - 1 + 16384 = 16383, so the next firing comes 16383
  steps later.
- **F8 UPHOLD.** 18 legs over 4 lanes split 5, 5, 4, 4, which gives five completion rounds.
- **F9, F10, F11 UPHOLD.**
- **F13 UPHOLD.** In `src/core/main.c:473-476`, `-V` sets `single_step` and `debugger_enter_at_end_of_run`. The second
  flag is why a halted session stays at the prompt, so `print v1` still answers; every halt row depends on it.
  `-x` (`:487-488`) only calls `console_allow_slaves(1)`.
- **F14 UPHOLD, wording REFINE.**
  - The plain latch-CLEAR label swap is rowed at every label, so rejecting it is right.
  - The sentence "the single-axis latch-CLEAR cells are rowed" is false if "single-axis" means one conjunct beyond the
    label. `C_istW_clr` (direction only) and `C_imk2_clr` (width only) are one-conjunct latch-CLEAR narrowings.
  - On the shipped probe, `C_istW_clr` scores **226/226** (batch f2b).
  - Write "label-only" instead.
- **F15, F16 UPHOLD.**
- **F18 UPHOLD, disclosed.** At {CONTROL, latch SET} each tested bit is written both ways across the two widths:
  - HARD_RESET is clear in `sb 0xff`, and set in `sh 0x0900`/`0x0a00`/`0xffff` and in the `gate` session's
    `sh 0x0800`;
  - DOG is written both ways;
  - the residue is both zero and nonzero.

  So the generating set is met without width, and `P_ctl2wrc_set` is a width x bit joint. It scores **226/226** on
  the shipped probe (batch f2b).
- **F19 UPHOLD, disclosed; REFINE the wording.** "Every row watches the line rise, none watches it fall" is false as a
  universal. `istw mid` and `p istw mid` both watch the line fall after an accepted INTMASK store. It is true scoped
  to REFUSED accesses: no refusal at 0x10/0x18 runs with `prev_asserted = 1`. The contract's "(every row here watches
  the line rise)" should read "every refusal row". `P_istprev_set` scores **226/226** on the shipped probe
  (batch f2b).
- **F20 UPHOLD the disclosure; OVERTURN the alternative's framing** (Q2). `D_dogbit0` scores **226/226** on the
  shipped probe (batch f2b).
- **F21 UPHOLD (adopted); REFINE a comment.**
  - The comment at probe `:1086` and E3's heading say the entries "after the first" run with the latch SET. In fact
    **every** entry does, the first included, because the refused `lb +0x07` at `:1018` comes before the loop.
  - Measured in this session on repair 15's census: latch = 1 at entry 1 (`sd +0x00`).
  - This does not affect the count, because the CONTROL writes are entries 10-17, 42 and 43.
- **F22, F23, F24, F25 UPHOLD.** POSTTABLE16 carries F23, and its item 4 moves all three pin lines from 204 to 226.
- **D1 UPHOLD:** small.
- **D2 UPHOLD: clause (e).** The eight cells are disclosed and the header claim is scoped. I withdraw my own
  precedent argument (Q5).
- **D3 UPHOLD: licensed** (Q5).
- **D4 UPHOLD: a licensed strengthening, which the contract should label as one** (Q5).
- **D5 UPHOLD all three disclosures, with two conditions.**
  - The F20 alternative is acceptable only as an ADDED predicate, never as a replacement (Q2).
  - The F18 alternative (one latch-SET `sh 0x0201` in `sh08b`) changes an existing session. `M8_ctllatch` and
    `M1_gotolatch` would newly red `sh08b msg`, so both owe a re-run. It is licensed but not owed.

## Q2 -- the disposition I would overturn first

**The F20 alternative as the packet frames it: "a value-anchored text in the ctldog/ctlrst rows, costs no session."**
It comes from my repair-15 answer, which said to count the anchored text "rather than the prefix". **That is wrong as
a substitute.**

**Measured.** `replay_ctl.out` replays the probe's own sessions from its recorded command lists:

    session         base         H_noresetclear      D_nodogclear       D_dogbit0
    ctlrst sw/sd    [0x1]        [0x1, 0x800]        [0x1]              [0x1]
    ctldog sw/sd    [0x1]        [0x1]               [0x200, 0x201]     [0x201]
    anchored count  1 / 1        ctlrst: 1 (!)       ctldog: 0          ctldog: 0

- **Under `H_noresetclear`,** the count of `control 0x0000000000000001` in `ctlrst` is 1, exactly as on the fixed
  build. A `ctlrst` row counting the anchored text instead of the prefix would be green on the round's own L2 cell.
- **In `ctldog` it only appears to work.** There the `0x0201` twin carries the DOG bit, so a skipped DOG clear also
  changes the twin's value. The `0x0001` twin in `ctlrst` carries no HARD_RESET.
- **The aggregate rows have the same trap.** A substituted anchor in `rearm/latch ctl msg` would miss the two extra
  `0x100` texts that `E_noendianclear` prints.

**The correct form.** Keep the prefix count and ADD the anchored count (equivalently, compare the multiset of printed
values). That keeps every current kill and adds `D_dogbit0`. Whether to do it at all is D5. The substitution must
not happen.

**Second, a lesser item:** F19's universal wording (Q1).

## Q3 -- what all of us missed

1. **The residue CHANNEL: `M_ctldebug` scores 226/226** (measured, and pre-registered in `PRED_f2.out`).
   - Every session that counts `CRIME_CONTROL: unimplemented` is stepped, and `debug()` prints while stepping. The
     default-arm `nodflt` rows depend on that same fact.
   - So demoting the CONTROL arm's `fatal()` to `debug()` passes every row. Free-running, the text vanishes
     (`disc_f2.out`):

         base:        1 free-running, 1 stepped
         M_ctldebug:  0 free-running, 1 stepped

   - The contract says repair 16 "CLOSES THE CONTROL ARM'S RESIDUE-TEXT CHANNEL AS A CLASS". That is true of the
     count and not of the channel.
   - The decline notice has item 5, with free-running rows on every axis. This print has none.
   - **Grade, by my reading: clause (e).** The fix never touches this upstream code, and the effect is host text only.
     So disclose it. Alternatively, row it as a licensed strengthening with a measured delta: one free-running session
     in `disc_f2.py`'s shape (an accepted `sw 0x0001` at +0x08, then `continue`, wanting 1), about 5 s.
2. **`ctlrst sw halt` had no measured kill.** Table 16 names no mutant for it, and POSTTABLE16's claim that "every new
   row fails under exactly its named mutants" lists none for it either.
   - `S_rst4clr` is the 4-byte, latch-CLEAR mirror of `S_rst8clr`. It scores **224/226 with CONTROL=FAIL**, red on
     `sw08 halts` and `ctlrst sw halt`. The row is now discharged.
   - Its only co-detector is a CRIMEP_CONTROL row, so the probe reports a genuine detection as a control failure. The
     gate goes red either way, through `crime width controls` and the row count.
3. **The halt rows' stated reason relies on an indirect signal.** The comment says v1 at the sentinel "shows the
   0x0800 write reached the arm". It only shows that SOME write halted the CPU.
   - I built `T_halttwin`, in which any nonzero residue also stops the CPU. In `ctlrst` the `0x0001` twin halts and
     the `0x0800` store never runs.
   - Measured on the probe's own `ctlrst sw` session (`pc_ctlrst.out`), `T_halttwin` reads the same as the fixed
     build: v1 = `0xdeadbeef`, one CONTROL text (`0x1`), and AFTER's `print pc` = `0x8000102c` in both.
   - **I expected the pc to separate the two cases, and it does not:** a store that halts the CPU leaves the pc on
     itself.
   - The only in-session difference is the count of `All machines stopped` notices, 3 against 4. That is too fragile to
     row.
   - So there is no cheap row that makes the stated reason true. The protection comes from other sessions.
     `T_halttwin` is caught by `p acc ctl msg`, `rearm ctl msg`, `rearm surv`, `latch ctl msg`, `latch surv` and
     `rst 4w/8w once` (derived; I did not run the probe on it).
   - **Fix the comment, not the rows:** "the halt shows a write stopped the CPU; that it was the 0x0800 rests on the
     twin not halting, which `rearm surv`/`latch surv` pin".
4. **Four records.** Two are in the packet (E7's md5 label and E10's "222-row"). The other two are in repair 16's text:
   the rearm latch-state comment and F19's wording. Details are under "Found while verifying". The `ctlrst` halt-row
   comment in item 3 would make a fifth.

## Q4 -- repair 16's rows

**Channels.** Every new row turns red under exactly its named mutants.

- I re-derived table 16 myself from each log's own row lines, not from `check16.py` (`t16_check.out`): all 25 legs
  are EXACT.
- `ctlrst sw halt` is now measured, by `S_rst4clr`.
- I added two per-cell legs of my own. Both were pre-registered (`PRED_f2.out` 05:46:26, batch start 05:47:01) and
  both came out exact:
  - `H_rstclr4clr`, the HARD_RESET clear skipped only for a 4-byte write with the latch CLEAR: red on
    `ctlrst sw msg` only;
  - `E_endlatch`, the ENDIANESS clear skipped only with the latch SET: red on `rearm ctl msg` only.

**The class closure is true as written, for the COUNT.**

- The static replay of 5f770991 confirms every latch state the contract claims:
  - `ctlrst` (S35, S36): both writes CLEAR;
  - `rst` (S65, S66): the twin CLEAR and the 0x800 SET;
  - `rearm` (S38): all ten writes SET;
  - `latch x5` (S52): all ten CLEAR.
- Every (clear, latch state) pair has a row that moves.
- The side-effect half also holds:
  - HARD_RESET's stop is covered in all four (width, latch) cells: `sw08 halts` (a CONTROL row) and `ctlrst sw halt`,
    `ctlrst sd halt`, `rst 4w`, and `rst 8w`;
  - DOG's stop and re-arm shapes are covered in both latch states.

It should state three limits:

- it pins the count, not the value (`D_dogbit0`, 226/226, already disclosed);
- it pins the count, not the channel (`M_ctldebug`, 226/226, **not disclosed**);
- HARD_RESET's re-arm or pre-set cannot be rowed (already disclosed).

**Targeting.** `rst_session` changed an existing session. The kills that rest on it (`K_ctl4w_reset_post`,
`K_ctl8w_reset_post`, `W_ctl8w`) were re-run in table 16 and are still red. The rule was honoured.

## Q5 -- the rule questions

- **D2 is clause (e), and I withdraw my precedent argument as a floor argument.**
  - The F2 pass's 2-byte rows predate the #549 pin (TESTS = masks or compares as a case).
  - At the decline, `len` is compared only as {8, 4, else}, and `writeflag` is not compared at all. No skipped arm at
    INTSTAT or INTMASK tests either one. So width within the narrow class, and direction, are not floor axes there.
  - By today's rule, the F2 rows were a strengthening.
  - What made the pass-2 state a wrong record was the header claiming the whole floor. The scoping fixes that, the
    scoped claim is measured true, and the contract names all eight cells.
  - If the adjudicators want the cells rowed anyway, it costs six sessions.
- **D3 is licensed.**
  - `L_dogclr` and `L_rstclr` are latch x clear joints inside a skipped arm. That is outside the Q3 bound, so they are
    clause (e).
  - Each has a measured escape against the 218-row probe.
  - The rows cost almost nothing: the aggregate needs no new session, and the reset rows add one accepted store to two
    existing sessions whose dependent kills were re-run.
- **D4 is licensed on the same warrant:** a measured delta at zero sessions. Label ENDIANESS as a strengthening in the
  contract.

## Found while verifying

1. **E7's md5 is wrong.** The packet says "f5e915f6 -> 1534bc9e", but table 16 ran **5f770991**. That md5 appears in
   `logs/INSTRUMENT.md5`, PRETABLE16, POSTTABLE16 and the driver's `want_md5`.
   - E7's 71 changed lines are byte-identical to the real f5e915f6 -> 5f770991 diff (checked). The content is right;
     only the label is stale.
   - E10's "222-row probe" is stale in the same way (226).
   - Both strings are hard-coded in `build_f2.py` (lines 114 and 119). PRETABLE16's first lines record that a 222-row
     draft existed and was replaced. This is the frozen-number class, appearing in the brief.
2. **The rearm latch-state wording** (F21 in Q1).
3. **A small slip in PRETABLE16.** Its derivation says "Every refusal in this session is at +0x06". The first refusal
   is at +0x07. It does not change any prediction.
4. **F19's universal wording** (Q1).

## Measured this pass

Every log below ends in `CRIMEP_DONE` (checked with `tail -1`). The mutants were built in `/tmp/gxopus_r15p2`
(`build_f2.sh`, sentinel-guarded), and their diffs are in `mutants/`.

    batch f2a (PRED_f2.out 05:46:26 < start 05:47:01)             batch f2b (PRED_f2b.out 05:54:32 < start 06:07:48)
    S_rst4clr     224/226 CONTROL=FAIL  sw08 halts, ctlrst sw halt   D_dogbit0      226/226 OK  (disclosed cell)
    M_ctldebug    226/226 OK            -- escape                    P_ctl2wrc_set  226/226 OK  (disclosed cell)
    H_rstclr4clr  225/226 OK            ctlrst sw msg                P_istprev_set  226/226 OK  (disclosed cell)
    E_endlatch    225/226 OK            rearm ctl msg                C_istW_clr     226/226 OK  (disclosed cell)
    all eight exactly as pre-registered; logs in runs/

The other evidence:

- **One-session discriminators:** `disc_f2.out`, free-running versus stepped.
- **The halt-row check:** `pc_ctlrst.out`, the `ctlrst sw` session on the fixed build and on `T_halttwin` (built for
  this check only; no probe run).
- **Replays of the probe's own sessions:** `replay_ctl.out`, on five builds.
- **Session record and static replay of 5f770991:** `sessions_5f770991.json` and `static_census_5f770991.out`
  (68 sessions, 226 rows).
- **The independent table-16 check:** `t16_check.out`.
- **Two identity checks:**
  - My `P_ist1r_set` and `P_imk1r_set` are byte-identical to table 16's `W_istlb` and `W_imklb`.
  - My restored binary is byte-identical to both table 16's base and table 14's base.

**What I did not do:**

- I did not re-run the probe's plain base leg on 5f770991. Table 16 has it at 226/226, and my restored binary is
  byte-identical to that leg's binary.
- The replays and discriminators use a verbatim copy of the probe's `session()`, not the probe itself.
- The latch states of the new sessions come from the static replay, cross-checked for the unchanged sessions by
  repair 15's measured census (66 of 66 agreed). I did not run a census binary on 5f770991.
- I did not read the other seats' F2 answers.

## Restore

- `/tmp/gxopus_r15p2/src/devices/dev_sgi_ip32.c` compares clean (`cmp`) against the working copy (md5 8c1d1545).
- Its binary is newer than the source and byte-identical to table 14's base.
- There is no `.MUTANT` in either clone.
- `/tmp/gxopus_r14` was never written: its source still compares clean and it has no sentinel.
- No emulator or probe process is left running.
- Nothing under `C:\DocumentNoSnc\cc\GXEMUL` was written except `repair16_f2_20260926/opus_f2/` and this file.
