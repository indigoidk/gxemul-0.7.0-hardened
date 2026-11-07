# Reading task: oldrec526 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC526-ab3a` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #526 xscaleinten (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 8598-8721 of CHANGELOG_8d9df658.md; each line carries its own number -- cite those numbers)

```text
 8598| # `#526` (xscaleinten): reading the i80321 interrupt-enable register ended the emulator — AFTER the model had already loaded the correct value into the destination register
 8599| 
 8600| **THE DEFECT.** `arm_coproc_i80321_6()` — coprocessor 6 on `-E iq80321` (and Iyonix), installed by
 8601| `machine_iq80321.c` — handles `crm 0 / crn 0` as the interrupt-enable register.  Its load arm read:
 8602| 
 8603| ```c
 8604| cpu->cd.arm.r[rd] = cpu->cd.arm.i80321_inten;
 8605| fatal("TODO: XScale read from inten?\n");
 8606| exit(1);
 8607| ```
 8608| 
 8609| **The destination received the modelled value and the host process then died.**  The register is fully
 8610| modelled in both directions: the store arm writes the same field, and `dev_i80321.c` consumes it
 8611| (`d->enable = &cpu->cd.arm.i80321_inten`).  A guest reading back its own interrupt enables — which is
 8612| what firmware does — ended the emulator.
 8613| 
 8614| **THE SIBLING IN THE SAME SWITCH IS THE WARRANT.**  `crn 4` (isteer) has the identical load/store
 8615| shape and its read carries no diagnostic and no exit.  `crn 0`'s kill is the switch's outlier —
 8616| upstream residue, the exit the author reached while developing, not a policy.
 8617| 
 8618| **THE FIX — ACCEPT (member 4 of the option set).**  Delete the two lines; keep the value.  No latch
 8619| and no announce: the read is implemented, so a bounded "unimplemented" message would be a wrong
 8620| record in product code.  The write arm, and the three kills this round RETAINS in the same handler —
 8621| the isteer non-zero write, the isrc write (`TODO: XScale int ack?`) and the unknown-tuple exit — are
 8622| untouched and rowed as controls.  Every seat that read-the-source in two passes upheld ACCEPT.
 8623| 
 8624| **THE WITNESS, and one thing it does NOT establish.**  Rung 3, cold debugger, unmodified in-tree
 8625| `iq80321`: `regress/artifacts/xscaleinten/agy_xscale_witness_20260911.py`, committed build **11/26**,
 8626| fix **26/26** (`witness_committed.out`, `witness_fix.out`).  **Test-first ORDER is not established by
 8627| these artifacts**: `witness_fix.out` carries the EARLIER mtime (`02:20:10` against `02:20:23`), and
 8628| nothing records that the committed leg was run before the edit.  What IS established, three times, is
 8629| that the committed source reproduces the death from a clean rebuild: every kill table's HEAD leg
 8630| (11/26, 12/29, 12/30).  *Recorded as a reproducible pre-fix measurement, not as test-first.*
 8631| 
 8632| ## The detector — `regress/xscale_inten_probe.py`, 30 rows, `gate_arm.sh` pin 30
 8633| 
 8634| Promoted from the witness with codex's repairs (`codex_promote_20260912b.txt`, answered after the
 8635| cybersecurity filter refused the first wording): a RESULT/CONTROL/DONE protocol, captured values kept
 8636| when a later step dies with unreached rows reported **BLOCKED** (not failed, not passed), a non-zero
 8637| exit on any non-passing row, and three new rows — `D_OP1` (read with opcode1 = 1),
 8638| `INTEN_WRITE_PRESERVES_ISTEER`, and `D_CRM1_TMR0` (crm isolation at crn 0).  Pass 2 added the
 8639| thirtieth, `RD0_ALLONES`.  The header carries a CONTRACT and a NOT COVERED list (clause (e)).
 8640| 
 8641| | table | instrument | legs | result |
 8642| |---|---|---|---|
 8643| | 1 `killtable_20260911/` | witness, 26 rows | 7 | M1 23, M5 25, M_OPCODE2 19, M_NREAD 19, M_RD15 25 — all killed |
 8644| | 2 `killtable2_20260912/` | 29 rows | 10 | 9 on prediction; HEAD predicted 13/29, measured 12/29 (a BLOCKED row counted as a pass in the prediction's arithmetic) |
 8645| | 3 `killtable3_20260912/` | 30 rows | 12 | **12 on prediction**; BASE 30/30, HEAD 12/30, every mutant killed |
 8646| 
 8647| Each table ran in a scratch clone of `build/` with a clone-local sentinel, a frozen instrument, a
 8648| `PRETABLE.out` written before it ran and a separate `POSTTABLE.out`; each restore was cmp-CLEAN and
 8649| FRESH.  Table 3's frozen instrument is `cmp`-identical to the shipped probe.
 8650| 
 8651| ## Pass 2, and the two survivors it found
 8652| 
 8653| A nine-seat pass 2 (`_scratchpad/panel_20260912_095235_xscalepass2`, the Opus measuring seat, then a
 8654| §F2 adjudication pass `panel_20260912_104522_xpadjud`, then Fable) asked one question: *is there a
 8655| clause-(d) mutant this detector does not see?*  **Two, both measured by the Opus seat at 29/29 against
 8656| the 29-row instrument, and both confirmed LIVE kills** (`artifacts/xscaleinten/opus_pass2_20260912/`):
 8657| 
 8658| * **`if (rd == 0) { fatal; exit(1); }`** after the load.  Every inten read in the probe landed in r3-r7,
 8659|   r9, r10 or r15.  `xscale_XM_RD0.log` 29/29; `live_XM_RD0_r0.log` dies, `_r9.log` survives.
 8660| * **`if (i80321_inten & 0x00400000) { fatal; exit(1); }`** — bit 22.  The rows drove inten = 0, S1,
 8661|   S2 and bit 28 only; union `0xFFA5F05F`, so bits `0x005A0FA0` were never set.  `xscale_XM_MAGICBIT.log`.
 8662| 
 8663| **One row closes both:** `RD0_ALLONES` writes all-ones to inten and reads it into a poisoned r0.
 8664| Table 3: `M_RD0` 29/30 and `M_MAGICBIT` 29/30, **each failing `RD0_ALLONES` alone**; no other leg's
 8665| failure set changed.
 8666| 
 8667| **THE GRADE — CLAUSE (e), BOTH CELLS; THE ROW IS L1 CONSTRUCTION.**  Ruled by the flagship seat (Fable 5.1, last, on
 8668| 7/7 scriptable seats plus Opus), against a three-seat minority that held `rd == 0` as a floor cell by
 8669| operand swap.  The floor is the cross-product of the dominating predicates (`crm == 0`, `crn == 0`,
 8670| `l_bit`) with the device-STATE lvalues the repair reads; the body reads `rd` as an INDEX and inten as a
 8671| SOURCE and tests neither, so both exits are the `idata == k` shape.  The swap reading was rejected on its
 8672| own consequence: it makes `rd == 0` floor only because `crn == 0` happens to dominate -- had the arm been
 8673| `crn 4`, `rd == 4` would be floor and `rd == 0` not.  **Grading by coincidence is the same vice as
 8674| grading by cost, and my own provisional lean ("floor, because one cheap row pins each") was that vice;
 8675| it is overturned.**  THE RULE THE NEXT PURE DELETION INHERITS, when its guarded body tests nothing: the
 8676| floor is clause (b)'s verbatim reinstatement plus the dominating predicates' accept cell; every
 8677| re-introduction keyed on a body-read operand the body does not test is clause (e), disclosed BY CLASS in
 8678| the CONTRACT; a row added for one is L1 -- licensed because cheap, never graded floor because cheap.
 8679| *And the row's reach, stated rather than implied (codex): all-ones pins every single-bit-SET predicate on
 8680| inten, not bit-CLEAR or multi-bit patterns.*
 8681| 
 8682| **What the NOT COVERED list now says, because the row closes two partitions and not the class:** an exit
 8683| keyed on `rd == k` for an undriven k, or on an exact inten VALUE, is not pinned — the body indexes by
 8684| `rd` and copies inten, and tests neither; an exit keyed on `isteer != 0` is EQUIVALENT on this
 8685| instrument (isteer can only become non-zero through a write that itself exits); no session makes more
 8686| than five inten reads; the ANCHOR rows raise only irq 28.
 8687| 
 8688| **Two kill CHANNELS named, because the row names overstate them (kimi):** `ANCHOR_CONTRAST` kills M1 by
 8689| HOST DEATH at the read, not through its named "spins, 0x18 never reached" channel; and `D_RESET` /
 8690| `D_ZERO` cannot vary under a wrong-source mutant whose substitute is also zero (isteer, isrc and tmr0 are
 8691| all 0 in a stepped session) -- they earn their place against the reinstatement class, not that one.
 8692| 
 8693| ## Wrong records corrected in-round (L4, found by the panels)
 8694| 
 8695| * **The CONTRACT said M5 was "the read loading another register".**  The measured M5 redirects BOTH
 8696|   directions of the crn-0 arm to isteer (`mut_xscale_t2.py`); a read-only redirect was never built.
 8697|   Two seats (glm, deepseek) then argued M5's 27/29 was inconsistent or its row vacuous — both from the
 8698|   read-only premise; `probe_M5.raw` refutes it (the isteer row reads S1, so the WRITE was redirected).
 8699| * **"4th read"** in the D arm was the fifth inten read (codex).
 8700| * **The probe had no CONTRACT header at all** until the CHANGELOG draft's own review said so — a floor
 8701|   clause, supplied before the pass-2 panel saw the probe.
 8702| * **My pass-2 brief called the DC21285 read a quiet-source precedent.**  `dev_footbridge.c` still
 8703|   carries its `fatal` + `exit` there; it is a DISPOSITION precedent only (codex, grok).
 8704| 
 8705| ## Seats
 8706| 
 8707| Pass 2: codex, kimi (CLI), grok, glm, deepseek, minimax, kimi-k3:cloud — 7/7 scriptable answered;
 8708| **minimax was labelled ECHO-ONLY by `panel.sh` and was a real answer** (it found the inten-bit
 8709| survivor) — a seat-check false positive, recorded.  Opus 5 measured.  **agy DELIBERATELY NOT FIRED**
 8710| (owner reservation for measurement).  §F2 adjudication: the same seven answered; Opus not re-fired
 8711| (its measurements were in the packet).  Fable 5.1 adjudicated LAST, after every other seat, as a subagent pinned to `model: fable` that opened by
 8712| naming itself `claude-fable-5-1` (verified, not assumed); it also closed the repair chain on this pass --
 8713| zero floor breaches, with the denominator: M_RD0, M_MAGICBIT (and the PPC round's four) measured killed,
 8714| the rest enumerated as (e).
 8715| 
 8716| ## Gate
 8717| 
 8718| `gate_arm.sh` (gate 14) with the new xscale section — parse before score, RESULT/CONTROL/DONE each
 8719| exactly once, rows run / correct / emitted pinned to the literal 30, FAIL and BLOCKED both zero:
 8720| **gate 14 PASS, 922 checks** -- the 914 of `#519`'s run plus this section's eight, every xscale row `ok` (parses, controls OK, exit 0, run 30, correct 30, emitted 30, FAIL 0, BLOCKED 0); GATE_EXIT=0; run from a FROZEN copy of `gate_arm.sh`; log `regress/artifacts/xscaleinten/gate_arm_20260912.log`.  Build trees: two-part clearance RUN before the gate, not asserted -- `cpu_arm_coproc.c` p1=CLEAN p2=FRESH in `build/`, `build-asan/` and `/tmp/gxsec-build`; `est/` p1=CLEAN, p2 N/A (source tree, no binary); the probe `cmp`-IDENTICAL to kill table 3's frozen instrument.
 8721| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_526: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC526: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
