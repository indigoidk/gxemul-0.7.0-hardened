# `vmedefaultkill` (#568, HIGH) -- PASS 2 (diff review): the fix as it now sits in the working tree, its 34-row rung-3 detector, the gate-14 block, and KILL TABLE 1 (measured)

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises, not
just the derivations.**  Where I state something as fact, ask whether it is true.  A seat that re-derives a premise from
something this brief did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/` -- its WORKING TREE, on committed HEAD `{HEAD}`.**  The
round's edits are UNCOMMITTED there (section 3 lists every file).  There are THREE pristine-2021-upstream copies of GXemul
under the project root (`./src/` and two under `_archive/audit-results-*/builds/`); they are NOT this fork.  If your line
numbers disagree with mine by hundreds you are reading one of them -- say so rather than reconciling.  **Another session's
uncommitted edits also sit in this working tree** (`dev_pcc2.c`, `dev_lca.c`, `dev_sh4.c`, `cpu_alpha_palcode.c`,
`mvme_pcctworeg.h` among them): they are NOT part of this round -- ignore them, and do not cite their line numbers.

**If you cannot read files that is expected** -- every fact you need is inlined.  Name any premise you cannot settle from
this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim -- an offset set, a bit index, a count -- ENUMERATE it rather than reasoning
about it.**  **And ENUMERATE THE RIGHT DOMAIN**: ask what the PRODUCER of the values can emit (here: which `relative_addr` /
`len` pairs the m88k load/store path delivers to a device) before you walk them.

**VERDICT LINE FIRST**, so your answer survives truncation.

## 1. The round in one paragraph

`src/devices/dev_vme.c`'s `DEVICE_ACCESS(vme)` named ten offsets of its 4 KiB window and sent every other offset to
`default:`, which printed with `debug()` (silent at default verbosity while free-running) and called `exit(1)` -- the
emulator ended with no visible reason on any unnamed offset.  The device exists only on `-E mvme88k -e mvme187`
(window 0xfff40000-0xfff40fff).  **Two owner rulings fixed the disposition (S2, S3 below); pass 1 (4 of 4 roster seats
plus a second packet-fed lens, all PROCEED WITH CHANGES) reviewed the sketch and the detector plan; this pass reviews
what was BUILT and MEASURED.**  The disposition itself is not open here unless you can show the code does not implement
it.

## 2. SETTLED PREMISES (re-inlined so nobody spends an answer re-deriving them)

* **S1** `dev_vme.c` was untouched since the 0.7.0 import before this round (`git log` lists one commit, `39748e3c`).
* **S2 OWNER RULING 2026-09-11 -- population 1 (word starts the header does not name, 0x90..0xffc, and every sub-word
  start): FAULT** (`return 0`; `memory_rw.c` turns a handler's `return 0` into an m88k data-access exception for a guest
  load/store).  Justified as "an access the emulator cannot service", NOT as a claim about the real VMEchip2, whose
  register chapter is not on disk.
* **S3 OWNER RULING 2026-10-09 -- population 2 (the 26 header-named register word starts with no case): DECLINE +
  ANNOUNCE ONCE** -- "reads 0, writes dropped, one `fatal()` per register, `(once)` marker", the shape of `#501`'s arm in
  `dev_pcc2.c`.  BACKED ACCEPT (inventing storage) was ruled NOT licensed.
* **S4** populations 3 (sub-word starts inside the ten CASED words) and 4 (a CASED base at len != 4) are FILED as
  `vmewidthlanes` (LOW).  This round DISCLOSES that they reach the fault, and pins ONE interim row as a named channel.
* **S5 (pass 1, re-derived by five readers)** the census is 10 cased / 26 population-2 / 988 population-1 word starts.
* **S6 (pass 1, all five)** `d->reg[w] == 0` for every population-2 word for the device's life: the only writers of
  `d->reg[]` are the T1CMP, T1COUNT, TCTL and VBR arms (indices 20, 21, 24, 34) and DEVINIT's VBR seed; an 8-byte store
  writes one element; `DM_DEFAULT` gives no host fast path.
* **S7 (pass 1, qualified by four seats)** `return 0` -> a data-access exception (vector 3; VBR 0 at reset -> PC 0x18)
  for a GUEST load/store.  NO_EXCEPTIONS callers (the debugger's `dump`/`put`, the disassembler, `memory.c` helpers)
  never reach the handler -- silent success with a zero fill, identical before and after.  An INSTRUCTION fetch takes
  vector 2 and then halts the emulation (pre-existing for every faulting fetch).  A second fault while PSR.SFRZ is set
  becomes ERROR (PC 0x50), so every stepped fault row has a session of its own.
* **S8 (pass 1, three seats by reading `cpu_m88k_instr_loadstore.c`)** the producer domain is naturally-aligned
  accesses only: a misaligned halfword/word/double traps on alignment BEFORE the device; `ld.d`/`st.d` is ONE len-8 call;
  nothing crosses the 1 KiB splitter or the device end.
* **S9 (MEASURED, probe revision 2)** DMT0 = 0x423d (word load into r4), 0x433d (into r6), 0x403f (word store), 0x4211
  (byte at addr & 3 == 1), 0x420d (halfword at addr & 2 == 2); DMA0 is the WORD address.  Eight values PREDICTED from the
  CPU code before the first run, all eight measured as predicted.
* **S10 (MEASURED, 2026-10-20 re-witness on HEAD 5dbc000e)** 7 of 7 guest sites end the emulator (rc 1); a free-running
  MASTERCTL read dies with NO `[ vme:` text.

**Pass-1 dispositions the build implements (condensed; the full record is `pass1_20261020/ADJUDICATION_p1.md`):**
D1 exact case labels (one dissent, Fable, for a bound test in `default:` -- recorded, main loop kept labels);
D2 no `odata = 0`, a comment states the zero-storage invariant, **and the read announce prints the served value**;
D3 the write announce prints all 64 bits (`0x%llx` of `(unsigned long long) idata`); D4 sub-word starts inside
population-2 words FAULT as the interim, disclosed, pinned by two rows; D5 population 1 keeps both `debug()` lines,
`exit(1)` -> `return 0`, comment "an offset this model does not service"; D6 the guest comment corrected (MASTERCTL is
READ then written back; IRQSTAT read, IRQCLR never written when it reads 0); D7 a compile-time capacity check on the latch.

**ONE KNOWN DEVIATION, DISCLOSED BY THE AUTHOR -- please rule on it (Q2c):** D2's record names the read-announce form
`-- served 0x%llx` with `(unsigned long long) odata`.  **The built code prints `-- served 0x%x` with `(unsigned) odata`.**
`odata` is `uint64_t`, assigned `d->reg[relative_addr / sizeof(uint32_t)]` -- a `uint32_t` element -- so its high 32 bits
are zero for every read this arm serves and the printed TEXT is identical today.  Nothing in the build record says why the
form changed; I found it while writing this brief.

## 3. The round's files (`git diff --numstat` plus the new files), each marked

{NUMSTAT}

## 4. The diff of `src/devices/dev_vme.c`, verbatim (`git diff -- src/devices/dev_vme.c`)

```diff
{DIFF}
```

## 5. The whole device AFTER the fix, numbered from the working file (struct, the access function with its common tail, DEVINIT)

```c
{FUNC}
```

## 6. The detector: `regress/vme_default_probe.py` (new, 34 rows)

{PROBEPATH}

Its own docstring's ROW PLAN, verbatim (each row with the mutant it is designed to catch and the channel that differs):

```
{ROWS}
```

## 7. The gate-14 block (`regress/gate_arm.sh`), verbatim from the diff

```diff
{GATE}
```

## 8. KILL TABLE 1 -- MEASURED in a scratch clone of HEAD, one build per leg, the probe frozen for the whole table

{KILLTABLE}

## 9. Questions

**Q1 -- premise audit.**  Check each, by reading or enumerating rather than by agreeing:
* (a) The 26 labels are exactly the header-named register WORD STARTS in 0x04..0x8c minus the ten cased offsets -- no
  more, no fewer, no duplicate.  (Enumerate against section 5's labels and S5's census.)
* (b) `relative_addr >> 2` over the 26 labels takes 26 DISTINCT values, the largest 35 (MISC 0x8c), so a `uint64_t`
  latch has room and the typedef evaluates to an array of size 1 -- and narrowing either the field or the `1ULL` to 32
  bits makes it size -1.  (Leg M_CAPNARROW measured the field form as a failed build.)
* (c) At the population-2 arm, for a READ, `odata` already holds `d->reg[relative_addr / 4]`, which is 0 (S6), and the
  common tail then writes it to the guest and returns 1.  For a WRITE the arm stores nothing.
* (d) `return 0` in `default:` is reached by exactly: the 988 population-1 word starts, every sub-word start inside a
  population-2 word, and every sub-word start inside a cased word (population 3) -- and by nothing a guest could reach
  before this round without dying.  Use S8's producer domain.
* (e) Each kill-table leg is ONE edit of the fix and was built fresh (section 8's md5s and build log lines).

**Q2 -- the diff, hunk by hunk.**  (a) Does each hunk implement S2/S3 and D1-D7 against the function's REAL control flow
(section 5, common tail included)?  (b) Is any ADDED comment sentence false or stronger than the code?  (c) **Rule on the
disclosed D2 deviation**: keep `0x%x`/`(unsigned)` (lossless today) or align with D2's `0x%llx`/`(unsigned long long)`
(symmetric with the write announce; robust if a later `vmewidthlanes` fix ever composes a 64-bit `odata` for an `ld.d`)?
Give the reason either way.  (d) Anything in the gate block that cannot fail, or that fails for a reason other than the
one it names?

**Q3 -- the ask-again (capped at ONE per detector per round; this is it).**  Kill table 1 is clean except for the legs
predicted equivalent.  **What is the SMALLEST EDIT to `dev_vme.c` that breaks the ruled behaviour (S2/S3/D2-D7) and still
passes all 34 rows?**  Name the row you expect to stay green, and the observable that would differ for a guest.  Edits
already measured are in section 8 -- do not re-propose them.  Describe edits in words or as a one-line diff; do not build
anything.

**Q4 -- the vacuity floor, clause by clause.**  (a) fails pre-fix; (b) fails on a verbatim reinstatement of `exit(1)`;
(c) fails on a NULL medium -- this round's is a build WITHOUT the vme device, recorded as `(c): measured at <artifact>`;
(d) fails when the fix is present but its repair is NULLED -- enumerate the predicates DOMINATING the edited lines (to the
enclosing function boundary) and the body-read lvalues, and the dispatch-LABEL axis (each label's value flows into the
latch index) -- and say which (d) cell, if any, no leg or row covers; (e) the CONTRACT (the docstring's NOT CLAIMED list)
-- is anything missing that a reader would assume is covered?; (f) ANCHORING -- "if every address in this device shifted
one word, which row reds?"  If the answer for some class of rows is NONE, name the class.

Two measured facts for (d)-(f), from section 8: **`cased census` and `t1cmp rt` are CONTROL rows**, so a dropped cased
label (M_DROPTCTL) is detected as CONTROL=FAIL -- a product mutant reported under the apparatus reason, though `tctl rt`
also reds.  Is a CONTROL row the right home for a row that a product edit can red, or should `cased census` be a scored
detector row with a separate apparatus control?  And the PER-ROW KILL CENSUS lists the rows no leg reds: name any
non-CONTROL row in it that should have a measured kill and does not (table 1b was built for `cased wr` and `p1 p2 edge`).

**Q5 -- records.**  (a) The probe docstring says "NO KILL TABLE EXISTS FOR THIS REVISION" and calls every mutant outcome
PREDICTED.  After table 1 that sentence is a wrong record; the plan is to replace it with a citation of the preserved table
(a docstring-only edit -- the measured instrument is the frozen copy, md5 named in section 8).  Is that the right repair,
and is anything else in the docstring now false?  (b) Observation (b) in section 8: **12 red rows print "(FAILED FOR SOME
OTHER REASON)" although the stop IS the leg's edit** -- the second-pass rows ("pass 1 not completed" / "pass 1 silent") and
the non-word rows under M_WRFAULT/M_LENFAULT, where for M_LENFAULT they ARE the named channel.  The gate counts them red
either way.  Is the row text a wrong record that must change before shipping, or an accurate statement that the row's own
precondition failed?  If it must change, say to what -- and note any wording change is an instrument change that owes a
re-run of the table.

If, while verifying a claim, you found something ELSE -- say so.

## 10. Answer format

Open with your token (first line), then ONE line `VERDICT: SHIP | SHIP WITH CHANGES | DO NOT SHIP -- <one line>`, then
Q1..Q5 in order.  Number every finding `F<n>`, give it a severity (FLOOR BREACH / WRONG RECORD / DEFECT / NIT) and say
what would settle it if you could not.  Facts and flags; no restating the brief.
