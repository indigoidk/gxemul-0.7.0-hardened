# Reading task: oldrec528 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC528-c0fe` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #528 mapledmaaddr (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 8326-8482 of CHANGELOG_8d9df658.md; each line carries its own number -- cite those numbers)

```text
 8326| # `#528` (mapledmaaddr): an ordinary guest read of the Dreamcast Maple bus's DMA-address register ended the emulator — AFTER the model had computed the right value
 8327| 
 8328| **THE DEFECT.** `src/devices/dev_dreamcast_maple.c`, `DEVICE_ACCESS(dreamcast_maple)`, case `0x04`
 8329| (`MAPLE_DMAADDR`), read arm:
 8330| 
 8331| ```c
 8332| fatal("[ dreamcast_maple: TODO: read from dmaaddr ]\n");
 8333| odata = d->dmaaddr;
 8334| exit(1);
 8335| ```
 8336| 
 8337| The field is fully modelled: the write arm stores it, and `maple_do_dma_xfer()` consumes it (it tests `!d->enable` and
 8338| `addr & 0x1f`).  Its sibling `MAPLE_ENABLE` (`0x14`) answers the same shape of read quietly.  A guest reading back the
 8339| address it had just programmed killed the host process.
 8340| 
 8341| **THE FIX — ACCEPT (member 4 of the option set).**  Delete the `fatal()` and the `exit(1)`; keep the value, with no
 8342| latch and no announce — the read is implemented, so an "unimplemented" message would be a wrong record in product
 8343| code.  `break` into the common tail (which writes `odata` on a read), never `return`.  Upheld 9/9 at pass 1 and never
 8344| disputed afterwards.  **FAULT (member 5) is NOT AVAILABLE on SH4**: `memory_rw.c` has no `MEM_SH` exception arm, so a
 8345| handler's `return 0` silently skips the load and leaves the destination register untouched — worse than a decline
 8346| (the Opus seat, verified by the flagship seat).  *Filed: the carrier's member-5 clause should say "nor SH, where the
 8347| idiom silently skips the load" — not made here, because `tools/CLAUDE.md` carries an earlier session's unreviewed
 8348| delta and section J requires the two copies to match.*
 8349| 
 8350| **THE WITNESS.**  Rung 3, cold debugger, unmodified `-E dreamcast`, guest `mov.l` through real decode:
 8351| `regress/artifacts/mapledmaaddr/agy_maple_witness_20260912.py` — committed build **4/12** (`witness_committed.out`,
 8352| 12:43:56: the host dies on the first read with the TODO text), fix **12/12** (`witness_fix.out`, 12:45:03), same
 8353| script, committed leg first; liveness and device-signature (`MAPLE_SPEED` mask) controls green in both.  Admitted by
 8354| the flagship seat; its `read quiet` row (keyed on one literal) was ruled channel-invalid and NOT inherited.
 8355| 
 8356| ## The detector — `regress/maple_dmaaddr_probe.py`, 37 rows, `gate_sh_rounding.sh` (gate 10) pin 37
 8357| 
 8358| Every register access is a real SH4 guest instruction stepped through the debugger (the device is `DM_DEFAULT`, so
 8359| `dump`/`put` never reach it); every load destination is POISONED; the header carries a CONTRACT and a NOT COVERED list
 8360| (clause (e)).  Its value rows cover the accept cell, every other case label, all eight single-bit narrowings of the
 8361| selector (0x05 by `mov.b`, 0x06 by `mov.w`, 0x00, 0x0c, 0x14, 0x24, 0x44, 0x84), 16- and 8-bit reads, the consumer's
 8362| partitions and their joint cell, read side effects (clear, set or clear one bit, a sibling write), a third-read
 8363| counter, and survival.  **It took SEVEN kill tables**, and the history is the point of this block:
 8364| 
 8365| | table | instrument | runs | result |
 8366| |---|---|---|---|
 8367| | 1 `killtable_20260912/` | 16 rows | 14 | 12 exact; `M_RET0` hit its stated alternate, `M_ZEROEXIT` 13/16 |
 8368| | 2 `killtable2_20260912/` | 29 rows | 25 | 24 exact, zero escapes; one timing-dependent extra red |
 8369| | 3 `killtable3_20260912/` | 35 rows, grammar + counts | 32 | **32 exact, zero escapes** |
 8370| | 4 `killtable4_20260912/` | 35 rows, + blank/CR/prompt counts | 8 | 8 exact (targeted) |
 8371| | 5 `killtable5_20260912/` | 37 rows, exact owed transcript, pre-`quit` snapshot | 21 | 20 exact (the miss is on the OLD instrument, below) |
 8372| | 6 `killtable6_20260912/` | 37 rows, whole transcript through EOF | 17 | 17 exact |
 8373| | 7 `killtable7_20260912/` | **37 rows, full-line disassembly + EOF + exit status** | 21 | **21 exact**; BASE 37/37 x3 |
 8374| 
 8375| Each ran in a scratch clone of `build/` with a clone-local sentinel, a frozen instrument, a `PRETABLE.out` written
 8376| before it ran and a separate `POSTTABLE.out`; every restore was cmp-CLEAN and FRESH.  Tables 4–7 are TARGETED on a
 8377| stated superset warrant (each new silence condition only adds reds; value rows unchanged), measure BASE for a false red,
 8378| and re-run every predicted survivor on the PREVIOUS instrument too, so each escape is measured rather than inferred.
 8379| 
 8380| ## The silence channel — the lesson, because the floor held and the oracle kept failing
 8381| 
 8382| The floor (flagship ruling, pass 1): **silence over every read interval** — a diagnostic-alone reinstatement is half
 8383| of clause (b).  The ORACLE for it was replaced six times, and every replacement but the last was swept by a diagnostic
 8384| it could not see:
 8385| 
 8386| | oracle | swept by | found by |
 8387| |---|---|---|
 8388| | a literal (`dreamcast_maple` in the transcript) | `fatal("[ maple: DMAADDR read ]")` | codex, glm, kimi |
 8389| | a quiet grammar | `fatal("0x%08x\n", ...)` — the shape of a `print` answer | codex |
 8390| | grammar + per-class counts | `fatal("\n")` — the grammar's blank line | grok (read late) |
 8391| | + blank / CR / prompt counts, `quit` echo EXEMPT | `fatal("GXemul> quit\n")` 35/35 (the exemption) | Fable |
 8392| | exact owed transcript, pre-`quit` snapshot | `atexit()` printing after the snapshot — 37/37 | deepseek, kimi, glm; Opus measured |
 8393| | whole transcript through EOF | `abort()`/`_Exit(1)` at exit keyed on the field — 37/37; a disassembler swap; an exit handler outlasting a bounded read | Opus measured; codex, kimi, deepseek |
 8394| 
 8395| The shipped oracle compares each read session's WHOLE transcript, from the first prompt to the pty's EOF, with the
 8396| exact line sequence the commands owe — every echo, value, `put` confirmation, and every stepped instruction's
 8397| disassembly line IN FULL (`disasm_line()`, rendering `sh_cpu_disassemble_instr`'s text) — rejects any CR that is not
 8398| the pty's CRLF, and requires every read session to reach EOF inside the post-`quit` cap and to exit 0.
 8399| 
 8400| > **A SILENCE ORACLE BUILT AS A WHITELIST HAS A SHAPE TO HIDE IN; ONE THAT STOPS OBSERVING AT A POINT IN TIME HAS AN
 8401| > INTERVAL TO HIDE IN.**  Twice a repair reproduced the class inside itself: table 5's snapshot NARROWED the window
 8402| > table 4's whole-buffer grammar had covered (glm; table 5's PRETABLE had called it "a strict tightening"), and table
 8403| > 4's count shipped an exemption.  The class-closure rule fired at pass two and was applied at pass four.
 8404| 
 8405| **AND ONE WINDOW NO FINITE TEST CLOSES, DISCLOSED RATHER THAN ROWED** (the Opus seat, measured): a session spans, after
 8406| its first stepped instruction, only that instruction's device tick and the two ticks `cpu_run_deinit()` runs at
 8407| shutdown — about three.  A report keyed on a later tick (every 4th: 37/37, `M_TICKPERIODIC4`, a survivor BY DESIGN in
 8408| table 7) prints only when the guest runs freely.  Running longer only moves the window.  **And a coupling**: the
 8409| compared transcript runs through those shutdown ticks, so `read silent` also requires every dreamcast device to be
 8410| silent on them — a device that prints at shutdown will red all twelve sessions, and that red is NOT the DMAADDR read.
 8411| 
 8412| ## The grades
 8413| 
 8414| Flagship adjudication: `fable_pass2_20260912.md` (HOLD, the class closure) and `fable_close_20260912.md` (**CLOSES on
 8415| table 7**), both fired LAST and verified `claude-fable-5-1`.
 8416| 
 8417| * **The selector reads — FLOOR, on a replaced warrant**: the switch tests all eight bits of `relative_addr` by equality,
 8418|   so the mask-narrowed generating set is one cell per bit; all eight are rowed, and `case 0x00:` stacked on the label
 8419|   is FLOOR (codex).  Two-bit merges are multi-axis joints: (e).
 8420| * **The consumer's partitions — (e), rows L1, for TWO reasons the header had first written as one**: the alignment
 8421|   decline keys on the body-read field and is a value cell the body does not partition; `d->enable`, the read counter
 8422|   and `len` are OUTSIDE the DEPENDS-ON enumeration.  Clause (e) is THE CONTRACT, not a category defined by "body-read
 8423|   operand" (glm, minimax; the flagship seat took the wording error as its own).
 8424| * **Exit status at exit** (`abort()` / `_Exit(1)` keyed on the field) — a FLOOR breach (the exit half of the removed
 8425|   defect at a new site), **L1** because the detector never shipped.  **The host-exit `atexit` announce** — FLOOR, L1.
 8426|   **Text passed off as a disassembly line** — FLOOR, L1.  **The bounded post-`quit` read** — an oracle-completeness
 8427|   fix, L1.  **Emulated-time deferral past the session's span** — clause (e), a DISCLOSED WINDOW: forced, not chosen,
 8428|   because emulated time has no terminal event inside a session.
 8429| * **Proportion — NOT fully proportionate, "partly my fault" (the flagship seat)**: tables 3-5 ground one class cell by
 8430|   cell; the class-closure amendment should have gone straight to table 6's whole-transcript model.  **Net: about two
 8431|   avoidable tables (4 and 5).**  Tables 6-7 were legitimate: the emulated-time axis was genuinely new, and the in-band
 8432|   hardenings are floor and could not be filed.
 8433| * **THE ROUND'S ONE WRONG DISPOSITION OF SUBSTANCE was the adjudicator's own**: the pass-2 prescription "snapshot the
 8434|   buffer BEFORE `quit`" generalised a one-line exemption into an unbounded time window, and table 5 adopted it.  The
 8435|   Opus seat's correction — *"MODEL that echo, not stop short of it"* — is table 6.  The #499 shape (a breach reproduced
 8436|   inside its own repair), arriving from the adjudicator's chair.
 8437| 
 8438| > **BUILD A SILENCE ORACLE AS AN EXACT WHOLE-TRANSCRIPT COMPARE FROM THE START; NEVER ITERATE UP FROM A WHITELIST.**
 8439| > Filed as `silencewhitelist` so other detectors' silence rows are censused against it.
 8440| 
 8441| ## Pass 2 and the adjudication passes, by seat
 8442| 
 8443| Pass 2 (`panel_20260912_131634_maplepass2`, 7/7 scriptable + the Opus measuring seat): the token-free diagnostic, the
 8444| single-bit aliases, `relative_addr & 4` (grok), `len != 4` (glm, kimi), and seven survivors MEASURED 16/16 by Opus
 8445| (consumer-keyed declines and exits, a third-read counter).  deepseek's and minimax's "move the assignment out of the
 8446| `else`" is EQUIVALENT.  §F2 (`panel_20260912_143959_mapleadjud`, 7/7): codex (`case 0x00`, the bare-hex diagnostic,
 8447| the joint decline); kimi (`& ~0x01` / `& ~0x02` — a mov.b at 0x05 and a mov.w at 0x06 REACH the device, so the
 8448| contract's "an SH4 address error before the device" was true for mov.l only, an L4 corrected; `len == 1`; sibling
 8449| writes); grok (`fatal("\n")`, READ LATE — my summary of that pass carried its stale-comment finding and dropped its
 8450| survivor — and disposed of in-round: the ask-again cap counts asks, not findings); glm and minimax (grade wording).
 8451| Fable pass 2 (`fable_pass2_20260912.md`, verified `claude-fable-5-1`): HOLD, class closure.  Closing pass
 8452| (`panel_20260912_190504`, `opus_close_20260912/`): the time axis; codex's seat REFUSED by its content filter (a seat
 8453| failure), re-fired on a reworded brief at the final pass and answered.  Final pass (`panel_20260912_201452`,
 8454| `opus_final_20260912/`): exit status, disassembly prefix, bounded read, the tick window.  Fable last
 8455| (`fable_close_20260912.md`).  agy was DELIBERATELY NOT FIRED on any review pass (measurement reservation); it built the
 8456| witness.
 8457| 
 8458| ## Not changed (assessed, disclosed in the probe header)
 8459| 
 8460| An effect keyed on another exact value or on a bit all-ones does not set; high-bit masking (covered by the values,
 8461| not separately measured); an effect after the third read (counter > 3); an effect KEYED on sibling state the rows leave
 8462| at reset (`} else if (d->timeout) {`); side effects on sibling state never read back; environment-keyed effects;
 8463| 64-bit reads (no reachable 8-byte callback: `fmov` with SZ=1 issues two 4-byte accesses); a third `writeflag` value;
 8464| `fatal("")` (EQUIVALENT); output on a channel the pty does not carry (a file); the emulated-time window above.
 8465| **Clause (c)** is carried by the four control rows by construction and was never a kill-table leg.  **The DMA leg** —
 8466| what a read returns AFTER a transfer — is the separate row `mapledmaadvance`.
 8467| 
 8468| ## Gate
 8469| 
 8470| Gate 10 (`gate_sh_rounding.sh`): **PASS (391 checks), 0 FAIL** -- the mapledmaaddr section 37/37 with CONTROL=OK and
 8471| exit 0 (`artifacts/mapledmaaddr/gate_sh_rounding_20260912.log`), run ALONE from a frozen copy of the gate, on the probe
 8472| `cmp`-IDENTICAL to kill table 7's FROZEN7; two-part clearance first: `build/`, `build-asan/`, `/tmp/gxsec-build`
 8473| p1=CLEAN p2=FRESH, `est/` p1=CLEAN p2=N/A.  (The gate script's committed copy differs from the frozen copy it ran only
 8474| in the section's comment, corrected afterwards to cite tables 2-7 -- comment lines only, checked by diff.)  An earlier
 8475| run (PASS 391, `artifacts/mapledmaaddr/gate_sh_rounding_20260912_T4INSTRUMENT.log`) was on table 4's instrument and
 8476| certifies a SUPERSEDED probe only — the gate reads the probe at invocation.
 8477| 
 8478| **Harness and records riders.**  `SCORE_CLAIMS_MANIFEST` 28 -> **29** in `tools/precommit_check.sh`, deliberately: the
 8479| new gate pin (`mapledmaaddr rows run` 37, unquoted).  The final-pass codex seat file
 8480| (`panel_20260912_201452/codex.txt`) carried 75 NUL bytes, which make `grep` treat it as binary; the ARTIFACT copy is the
 8481| scratchpad original with those NULs removed (`cmp`-verified) and nothing else changed.
 8482| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_528: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC528: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
