<!-- SUPERSEDED 2026-09-17 -- DO NOT BUILD FROM THIS FILE -->

# *** SUPERSEDED.  DO NOT BUILD FROM THIS FILE OR FROM THE SPEC IT AMENDS. ***

**The eight amendments below were reconciled on 2026-09-17 and the answer was REWRITE, NOT
PATCH.**  The seat that wrote the original spec was asked to be harder on its own work than on
anyone else's, and ruled against it: *"Eight amendments on a spec that already disagreed with
itself (12 sessions vs 15 data rows) is a `#392` shape.  A builder applying them in order will get
1+6 wrong and will either treat `save 2s` as a duplicate of `kill 15` or REPLACE `kill 15` with
it, losing the `== 0x14` pin."*

> ## BUILD FROM `WITNESSSPEC_REWRITE_grok_20260917.txt` IN THIS DIRECTORY.
> It is standalone: 17 rows, 13 sessions, the CONTROL=DEAD set, the plant layouts, the tally
> (`14/17 -> 17/17`, **not** the `14/16 -> 16/16` the old spec claimed) and the clause-(e)
> disclosures.  No sticky notes.

**This file is kept for PROVENANCE ONLY** -- it records which amendments were right, which were
half-right, and which were aimed at the wrong document.  Reading it as instructions will build the
wrong probe.  Its conclusion is deleted rather than demoted, per the carrier's own rule that a
superseded rule must not keep the closing position of authority.

**Where each amendment landed:**

| # | subject | disposition in the rewrite |
|---|---|---|
| 1 | kill-row oracle: EOF ALONE => RED | **ADOPTED**, and it forces three further changes -- POST want becomes `m=13 sp once`, `DEST+4` is poisoned, and the tally names its reds |
| 2 | spec self-contradicts on session count | **ADOPTED and the number corrected again**: 13 sessions, not 12 and not 15 |
| 3 | the two RED rows may be duplicates | **HALF-RIGHT, and it misreads its own case.** The original two reds were `kill 14` and `kill 15` -- two LOAD holes catching `== 0x14` -- not Load vs Save. **Score `save 2s`, KEEP `kill 15`.** |
| 4 | accept rows check ARRIVAL not PRESERVATION | **ADOPTED as the canary, FOLDED into S7-S11 rather than new rows.** Its SVC32 complaint was against a generic heading; the `same svc` row was already right (SP unchanged IS the preservation check) |
| 5 | stimulus clears I\|F, so interrupts are on | **TRUE OF THE ENCODING, INERT FOR THIS PROBE** -- ARM IRQ dispatch is inside `if (!single_step)`, `fiq_asserted` has ZERO occurrences in `src/`, and the debugger `timer_stop()`s. Pinned by **stay on `step`, never `continue`**; do NOT change the stimulus to `#0xD4` |
| 6 | the spec's fake-green mechanism is the wrong one | **ADOPTED**, and it interacts with 1: the `enc ok`/`no cbit`/dump controls are **necessary and NOT sufficient**; the anti-false-green is one `WORDS` dict plus a per-session plant-dump |
| 7 | do not copy `arm_flags_probe.py`'s `session()` | **ADOPTED** |
| 8 | Alpha spec lacks `CONTROL=DEAD` / `RESULT=0/0` | **BELONGS ON THE ALPHA SPEC, NOT THIS ONE** -- it was misfiled here |

---

# *** READ THIS BEFORE BUILDING `regress/arm_msrmode_probe.py`. ***
# The spec in `WITNESSSPEC_grok_20260917.txt` is AMENDED. Build the amended form, not the spec.

**WHY THIS FILE EXISTS, and it is not ceremony.** `#490` ran its pre-table check, prescribed two
rows at 16:05, and **lost both** when the row list was rewritten from a later panel's findings at
18:45. A measuring seat then built both mutants and both escaped the committed detector -- two
floor breaches the round's own artifact had predicted and specified. **Nothing was forgotten in the
sense of never known: the knowledge sat in the file that exists to be consulted at row-writing
time, and did not survive a rewrite in a DIFFERENT artifact.**

So the amendments live **beside the spec**, not in a ledger row, not in a checkpoint, not in a
panel transcript.

---

## AMENDMENT 1 -- *** THE KILL-ROW ORACLE IN THE SPEC IS BACKWARDS. DO NOT BUILD IT AS WRITTEN. ***

**Spec says:** an armed kill row is RED on pty EOF **AND** the exact text
`arm_load_register_bank: unimplemented mode 20`.

**BUILD INSTEAD:** on an armed kill row, **EOF ALONE => RED. The text is the DIAGNOSIS, not half
the trigger.** Record the text; do not gate on it.

**The mutant the AND cannot see** -- named by the glm seat, and it is the most plausible near-miss
fix anyone would actually write: **a build that still `exit(1)`s but with a REWORDED MESSAGE.**
The spec itself spotlights the `%i`-vs-`0x14` confusion, which makes *"fix the format string,
forget the `exit(1)`"* the obvious wrong repair. That mutant produces EOF and no matching text, so
the AND never fires, **the row goes GREEN, and the witness certifies a build in which a guest `MSR`
still kills the emulator.**

> **THE AND BUYS PROTECTION AGAINST A FALSE-RED AND PAYS WITH A FALSE-GREEN. For a CERTIFICATION
> witness that is the wrong trade, because the false-green is the direction that ships a defect.**

Under `EOF alone => RED` the feared cases still close correctly:

    crash elsewhere in the armed window  -> RED   conservative, and acceptable: any death in the
                                                  armed MSR's window satisfies the row's claim
    prints the line but does NOT exit    -> GREEN CORRECT.  The defect IS the process death.
                                                  A surviving process with a diagnostic is the fix.

**Buffering is not an objection** (checked, not assumed): `exit()` flushes stdio, stderr is
unbuffered, and a pty is line-buffered at the trailing newline -- so the defect's own death
preserves its own text. Buffering threatens only SIGNAL deaths, which is mutant territory.

*Single-seat finding, UNCORROBORATED: deepseek and minimax answered the same brief and neither
reached it. Recorded that way deliberately -- it is not a panel consensus. It is adopted because
the argument is sound, not because it was outvoted.*

---

## AMENDMENT 2 -- THE SPEC SELF-CONTRADICTS ON SESSION COUNT. RESOLVE BEFORE WRITING ROWS.

It states **"one fresh emulator process per data row"** and **"12 guest sessions"** for **15 data
rows**. `12 < 15`. Either three sessions host two rows each -- which reintroduces exactly the
sharing hazards the one-process rule exists to prevent -- or the count is wrong.

**Publish the row -> session schedule as a table in the probe header before writing any row.**
The spec's own stated exemptions (`enc ok` and the identity row have no session; `live` and
`pc adv` share one) account for some of the gap; make the arithmetic explicit rather than implied.

---

## AMENDMENT 3 -- THE TWO RED ROWS MAY BE DUPLICATES, WHICH WOULD HIDE HALF THE DEFECT

The spec expects `14/16 -> 16/16`, i.e. exactly TWO rows change colour, on the grounds that the fix
touches **two** `default:` arms (Load and Save).

**But pre-fix, the Save arm is not independently reachable** -- Load kills on ENTRY to the reserved
mode, so any Save-side row dies at its FIRST `MSR` with the identical EOF signature.

> **So the second red row differs from the first ONLY IF ITS STIMULUS CONTAINS A SECOND MODE
> WRITE.** If both are a single `MSR #0x14`, they are duplicates: **a Load-only fix turns both
> green and the witness certifies a build that still dies on the write OUT of the reserved mode.**

Write the second red row as `MSR #0x14` **then** `MSR #0x13` (the spec calls this shape `save 2s`
and disclosed it rather than scoring it). Its channel is
`arm_save_register_bank: unimplemented mode 20`.

---

## AMENDMENT 4 -- THE ACCEPT ROWS CHECK ARRIVAL AND NOT PRESERVATION

Two defects in the accept side:

* **SVC32 is incoherent as stated.** The spec's accept oracle is *"SP changed from boot value to
  0"*, but `MSR #0x13` from SVC32 hits the SAME-MODE SKIP -- save/load are never called -- so SP
  **cannot** change. That row's expectation must be *mode still `0x13`, SP UNCHANGED at `BOOT_SP`,
  and I|F cleared* (the c-byte write clears them), which the spec does say elsewhere. **Make the
  row's want match its own stimulus.**
* **A fix that repairs both LOAD arms and no-ops the SAVE arm passes every accept row**, because
  nothing checks that the outgoing bank was PRESERVED. Add a canary: write a known value to
  `r13`/`r14` before the switch and verify it is restored after returning, for every mode except
  USR32 (which is one-way).

---

## AMENDMENT 5 -- THE STIMULUS UNMASKS INTERRUPTS. KNOW IT BEFORE IT SURPRISES A ROW.

`MSR CPSR_c, #0x14` writes the WHOLE control byte, and bits 6-7 of `0x14` are **zero** -- so it
**clears I and F**, enabling IRQ and FIQ.

Pre-fix this is invisible (death is synchronous at the CPSR write). **Post-fix, the guest sits in a
reserved mode with interrupts enabled**, and any pending source takes an exception whose bank-save
runs with the reserved mode current -- so the Save arm can be entered ASYNCHRONOUSLY and row timing
becomes nondeterministic. Whether `testarm` has a pending source at that point is **not
established**; if a post-fix row flickers, this is the first thing to suspect.

---

## WHAT IS NOT AMENDED, AND WAS INDEPENDENTLY CONFIRMED

* **`0xE321F014` is correct.** Verified field-by-field against `to_be_translated` by the authoring
  seat AND hand-decoded independently by glm. `0x14` = **20** decimal, so `%i` prints `mode 20`.
* **`testarm` boots SVC32 (`0x13`) privileged, MMU off, T clear, SP `0x03fff000`** -- smoked on the
  committed binary, not inferred from the create path.
* **Ban `#0`** -- but NOT as a fake-green. `ARM_MODE_USR26` is `0x00` and there is no
  `case ARM_MODE_USR26` anywhere in `src/`, so `#0` reaches the same `default:` and KILLS. Ban it
  because it rows the **26-bit** hole, not the reserved 32-bit hole under test.
* *** THIS BULLET USED TO SAY "copy helpers from `arm_flags_probe.py`, NOT `arm_bfx_width_probe.py`,
  because BFX's `printed()` matches a bare `0x...` while the debugger prints `r0 = 0x...`".
  THAT REASON IS FALSE AND THE INSTRUCTION WOULD BREAK EVERY `print` ROW. ***
  `debugger_parse_expression` returns `PARSE_NUMBER` on success, so **`print <reg>` emits a BARE
  `0x...` line**; the `reg` command is the one that prints `r0 = 0x...`.  A builder who "fixed" the
  regex to expect `r0 = 0x` would score **every** `print` as ABSENT.
  **COPY `printed()` FROM `regress/lca_isalane_probe.py:398`** -- a 352-row instrument that works:
      `printed()` is the FIRST-match form: a `re.search` for the literal `print <reg>`,
      then optional whitespace, then a capture of `0x` + hex digits.  Read it from
      `regress/lca_isalane_probe.py:397-399` and COPY IT VERBATIM -- do not retype it, and
      do not reproduce it in this file, because the last attempt to quote it here had its
      backslashes eaten crossing a heredoc and landed as a regex split across two lines.
  and note `arm_flags_probe.py` **has no `printed()` at all**, so the original advice was not merely
  wrongly-reasoned, it was unfollowable.
  *Caught by the same seat that wrote the original instruction, on a later firing, and VERIFIED
  here against the probe before landing -- a wrong reason gets reused, and this one was sitting in
  the file whose title says READ BEFORE BUILDING.*
* **Never debugger-write `cpsr`.** That would skip Load and let the next guest `MSR` hit Save -- a
  state a guest cannot occupy on HEAD, i.e. laundering Save's unreachability.

---

*Sources, all durable and beside this file:* `WITNESSSPEC_grok_20260917.txt` (the spec),
`ADJUDICATION_glm_20260917.txt` (amendments 1-5), `ADJUDICATION_deepseek_20260917.txt` and
`ADJUDICATION_minimax_20260917.txt` (answered; neither reached amendment 1),
`REACHABILITY_grok_20260917.txt` (the CONFIRMED defect trace).

---

## AMENDMENT 6 -- *** THE FAKE-GREEN MECHANISM NAMED IN THE SPEC (AND EARLIER IN THIS FILE) IS THE
## WRONG ONE.  GUARDING IT WOULD GUARD THE WRONG THING. ***

The spec, and my own earlier summary of it, say the hazard is: *if the CPU were already in USR32,
the mask fires, nothing switches, and THE KILL ROWS GO GREEN while the defect is live.*

**Measured against the row polarities, that is false.**  Already-USR32 gives `m=10`, alive, no Load
line -- and the row's want is the POST value `m=13`, so it goes **RED**.  That is a WRONG-REASON
FAIL (an `armed` / CONTROL failure), not a false green.  It still aborts the table, which is why
the arming prefix is right; but it is not the thing that could certify a live defect.

**THE REAL MSR FAKE-GREEN IS THE OPPOSITE SHAPE:**

    encoding is a nop  /  c-bit not set  /  the MSR is never stepped
        -> CPU stays SVC32, process alive, no Load line
        -> which is EXACTLY THE POST-FIX DECLINE APPEARANCE
        -> GREEN, on a build where the defect is live and simply was not exercised

> **A row that never fires its stimulus is indistinguishable from a row whose stimulus was
> correctly declined -- unless something proves the stimulus HAPPENED.**

**WHAT CATCHES IT, and all three are already in the spec -- they were just attributed to the wrong
hazard:** `enc ok` (verify imm + rotate + c-bit + SPSR-clear, NOT merely the MSR mask -- a mask-only
check blesses `#0x10`, which is USR32 and modelled), a `no cbit` row, and **the dump taken BEFORE
the MSR** so the arming word is on record independently of what the MSR then does.

*Same shape as the `#0` correction and the `printed()` correction: the ADVICE survives and the
REASON was wrong.  A wrong reason gets reused -- here it would have sent a builder to guard the
USR32 path, which reds honestly, while the path that actually greens went unguarded.*

---

## AMENDMENT 7 -- *** DO NOT COPY `arm_flags_probe.py`'s `session()` WRAPPER.  IT DUMPS ONCE, AT
## THE END, AND THIS PROBE'S PROCESS IS DEAD BY THEN. ***

`arm_flags_probe.py` takes its `dump` **after the whole program has run**.  That is fine for a probe
whose guest survives.

**This probe's guest calls `exit(1)`.**  The arming evidence -- `MRS r0,cpsr` stored at DEST -- must
be dumped **after `step 2` and BEFORE the killing `step`**.  A trailing dump cannot recover it,
because the process it would have read is gone.

    COPY from arm_flags_probe.py:   wait / send / rd, sw(), the -A colour trap, the stub load
    DO NOT COPY:                    its session() wrapper
    BUILD INSTEAD:                  an in-stream dump between the arming steps and the kill step

*This is also why the MSR probe is the right one to build FIRST: it is the only one of the three
that forces the mid-session dump, so building it proves that machinery before Thumb inherits it.
Thumb may use a trailing dump -- `-V` returns after `running = 0` and memory is still there.*

---

## AMENDMENT 8 -- A NOTE THAT BELONGS TO THE ALPHA SPEC, RECORDED HERE SO IT IS NOT LOST

`lca_isaphys`'s spec states its stop condition in PROSE (*"if `ptbr miss` / `ptbr sent` are red,
stop"*) and **does not emit `CONTROL=DEAD` / `RESULT=0/0`**.  Both ARM specs do.

**A failed `swpctx` would then yield a mid-score (~10/13) with the defect rows GREEN, and a
`RESULT=` grep will not refuse it.**  When that probe is built, copy the ARM token: emit
`LCAISAPHYS_CONTROL=DEAD` and `LCAISAPHYS_RESULT=0/0` and stop, rather than scoring a table whose
vehicle was never armed.

*The general rule, which is one idea rather than three checklists:* **a positive, un-fakeable
observable that the bad path is ARMED, checked on the SAME PROCESS that will issue the stimulus,
before any defect row is read -- and red there is SETUP-FAILED, not "no defect".**
