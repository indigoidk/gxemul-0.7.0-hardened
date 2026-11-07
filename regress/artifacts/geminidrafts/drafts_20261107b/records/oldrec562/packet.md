# Reading task: oldrec562 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC562-1dd2` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #562 armmsrmodekill (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 4161-4323 of CHANGELOG_8d9df658.md; each line carries its own number -- cite those numbers)

```text
 4161| # `#562` (armmsrmodekill): one privileged guest `MSR` naming a mode this model does not bank -- or an SPSR restore whose SPSR names one, including an SPSR never written -- ended the emulator; the mode field is declined now and announced once per site, defended by a 47-row detector whose review chain ran five repairs
 4162| 
 4163| **The defect, witnessed at rung 3.**  `arm_load_register_bank()` and `arm_save_register_bank()` in
 4164| `src/cpus/cpu_arm.c` switch on the seven mode values this model banks (USR 10, FIQ 11, IRQ 12, SVC 13, ABT 17, UND 1b,
 4165| SYS 1f -- six banks, USR and SYS share one), and their `default:` arms called `fatal(); exit(1);`.  Three guest
 4166| instructions write CPSR's mode field: `msr_imm` (`MSR CPSR_c,#0x14` = 0xE321F014), `arm_pop`'s `LDM {..pc}^` SPSR
 4167| restore, and the data-processing S-to-PC restore (`MOVS pc,lr`).  Any of them naming an unmodelled mode reached Load's
 4168| `default:` and ended the process -- and **no MSR is needed**: `cpu_new()` zero-fills the CPU and nothing initialises
 4169| the SPSRs, so the first `MOVS pc,lr` from the boot SVC32 before any exception has written `spsr_svc` loads mode 0x00
 4170| and dies (grok, pass 1).  `regress/arm_msrmode_probe.py` on the unmodified `-E testarm`, HEAD `ef577140`: the 17-row
 4171| witness scored 14/17 -- `kill 14`, `kill 15` and `save 2s` dead, every control green
 4172| (`artifacts/armmsrmodekill/witness_20261007/run_head.out`); the shipped 47-row detector scores 18/47 on HEAD, 29
 4173| named reds (`killtable5_20261008/run_head.out`), and 47/47 on the fix (`run_fixed.out`).
 4174| 
 4175| **The disposition -- member 3, and it is a POLICY.**  DDI 0100I A2.5.7 (`_scratchpad/ddi0100i.txt:1877-1879`): "If any
 4176| other value is programmed into the mode bits M[4:0], the result is UNPREDICTABLE"; the glossary (`:45062-45065`):
 4177| UNPREDICTABLE "must not halt or hang the processor"; ARMv7 (`ddi0406.txt:143212`) lets it be UNDEFINED.  Declining
 4178| the MODE FIELD only, with the instruction's other effects applied, is this emulator's choice, not an architectural
 4179| requirement; codex's pass-1 dissent (decline the whole operation) is recorded below.
 4180| 
 4181| **What ships.**
 4182| * `src/cpus/cpu_arm.c` -- `arm_mode_is_modelled()`, extern (the DPI template is compiled as its own object), whose
 4183|   case list is Save's and Load's; Save's and Load's `default:` arms become per-CPU latched backstops that announce
 4184|   `(once)` and return -- no `exit(1)`, no rollback.  After the fix they are reached only once an unmodelled mode is
 4185|   ALREADY in CPSR, which only a debugger `cpsr=` assignment can put there; their comments name exactly which callers
 4186|   then reach each (Save: a guest MSR, a DPI S-to-PC, exception/IRQ entry; Load: a DPI S-to-PC executed in the planted
 4187|   mode only).
 4188| * `src/cpus/cpu_arm_instr.c` -- `msr_imm`: a mode-field write naming an unmodelled mode announces once and clears
 4189|   `ARM_FLAG_MODE` from the LOCAL mask before `switch_register_banks` is computed (`ic->arg[]` is a cached translation
 4190|   and is not written); `arm_pop`'s `^` restore: an unmodelled SPSR mode keeps the CURRENT mode in M[4:0], every other
 4191|   bit from the SPSR, no early return (the PC load must run).
 4192| * `src/cpus/cpu_arm_instr_dpi.c` -- the S-to-PC restore takes the same policy through a `new_cpsr` local, only when an
 4193|   SPSR was copied (`spsr_copied`).
 4194| * `src/include/cpu_arm.h` -- `ARM_MODEWARN_{MSR,POP,DPI,SAVE,LOAD}`, `uint32_t mode_warned` in `struct arm_cpu` (zero
 4195|   at `cpu_new`), and the helper's prototype.  `est/` byte-identical.  Build trees: REBUILT CLEAN on 2026-10-09 (every
 4196|   object deleted -- see THE GATE below for why the two-part clearance was not enough); `gate14_20261009/cleanbuild.out`: `build/`
 4197|   (223 objects), `/tmp/gxsec-build` and `build-asan/` (224 each) emptied and rebuilt, parts 1 and 2 ok on all four
 4198|   files and NO object older than `cpu_arm.h` in any of the three.  `est/`: part 1 ok, part 2 N/A (a source tree) --
 4199|   recorded in `gate14_run2.out`'s clearance header, which `cleanbuild.out` does not cover.
 4200| * `regress/arm_msrmode_probe.py` (NEW, 47 rows in 43 sessions) -- real guest instructions on the unmodified
 4201|   `-E testarm -M 64`, 47 scored rows across 43 fresh emulator sessions (three rows are static; `live` and `pc adv`
 4202|   share one), liveness and device-signature controls, selected encoding fields checked (`enc ok`) with the planted
 4203|   MSR-session streams checked word for word; a GENERATED grid (`grid msr`, `grid dpi`, `grid pop`, `grid cov`, owner
 4204|   ruling 2026-10-08) observes every non-equivalent G1 cell -- (path, outcome, bit, polarity), aggregated over labels
 4205|   and latch states -- by complementary pairs, every msr label against every
 4206|   mode bit, all 25 unmodelled values on each path and all four `arm_pop` enclosing cells.  Its header is the CONTRACT
 4207|   (clause (e)) and the NOT CLAIMED list.  The committed text is the measured probe plus module-docstring corrections
 4208|   only, AST-identical (`killtable5_20261008/SHIPPED_vs_FROZEN.txt`).
 4209| * `regress/gate_arm.sh` -- gate 14 runs it, before `gate_end`: parse before score, CONTROL OK, exit 0, rows run /
 4210|   correct / emitted pinned at 47, REDS none, and no FAIL row under the trailer (the Opus seat measured a synthetic
 4211|   log with a FAIL row and a 47/47 trailer passing every other check).
 4212| * `tools/pipeline/check_probe_wiring.py` -- the probe as a gated DETECTOR, and one MANIFEST line per `.py` file under
 4213|   `regress/artifacts/armmsrmodekill/`, derived by `manifest562.py` at staging time (RESEARCH for the Opus seat's
 4214|   scripts and the frozen instruments, TOOL for the helper's mutators); `tools/precommit_check.sh` --
 4215|   `SCORE_CLAIMS_MANIFEST` 32 -> 33 (`check_score_claims.py`: SCORE_CLAIMS_PINNED=33, PASS).
 4216| 
 4217| **THE CHAIN -- one fix, five detector repairs.**  The product code has been unchanged since repair 2 (comments only
 4218| after it); every pass after pass 2 found holes in the DETECTOR, never in the fix.
 4219| * **Pass 1** (`panel_pass1_20261007`; the Opus 5.5 seat `witness_20261007/opus_pass1.md`): member 3 at all three guest
 4220|   writers, not at the bank helpers; the zero-SPSR route (grok); restore guards owed two rows (opus, kimi-k3, deepseek,
 4221|   minimax, agy).  **§F2** (`panel_f2_20261007`, `witness_20261007/opus_f2.md`) -- dispositions judged wrong: agy 3, Opus
 4222|   3 (5, 7, 11), codex 2 (6, 11), grok 1, glm 1, kimi-k3 1, deepseek 0, minimax 0.  Taken in: `put` writes MEMORY, so
 4223|   the backstop route is the debugger's `cpsr=` assignment (codex 11); the helper extern, not `static` (codex 9);
 4224|   accept rows for both restores (Opus 5); T/execution state on restore NOT made coherent by a mode filter (codex 6) --
 4225|   disclosed, and filed as `armspsrthumb`.
 4226| * **Table 1** (`killtable_20261007/`): 20 mutants on the 25-row probe; the three shared-latch mutants escaped 25/25,
 4227|   so `latch ind` was added before anything shipped (L1) -- 26 rows: base 26/26 before and after, HEAD 16/26, all four
 4228|   shared-latch mutants red (run 2a was aborted: its want omitted the `once` token, fixed and base 25/26).
 4229| * **Pass 2** (`panel_pass2_20261007`, `opus_pass2_20261007/`): codex DO-NOT-SHIP; the Opus seat MEASURED three floor
 4230|   breaches -- deleting a latch's `|=` line at four sites, and `mask &= ~0x0f` in `msr_imm`, each 26/26 -- and the
 4231|   restore rows ran from SVC only.  **Repair 2** (`killtable2_20261007/`, 38 rows): tables 2 and 3, 36 + 6 mutants, all
 4232|   red but `O_mask_nibble` on the OLD 37-row probe (37/37, the escape reproduced); baselines 37/37 and 38/38.
 4233| * **Repair 2's pass** (`panel_pass2r_20261007`, `opus_pass2r_20261007/`): the Opus seat built 23 fix-side mutants and
 4234|   21 kept 38/38 (helper projection widened, restore keep-mode mask narrowed x7, label x latch x outcome x6, I forced on
 4235|   a decline, three enclosing predicates).  Same class twice -> **repair 3 = CLASS CLOSURE** (`killtable3_20261008/`,
 4236|   40 rows): 65 mutants, all red, baselines 40/40.
 4237| * **Repair 3's pass** (`panel_pass2r3_20261008`, `opus_pass2r3_20261008/`): 14 of 20 kept 40/40 (the helper widened to
 4238|   undriven bits, decline flag provenance x7, the S-instance enclosing cells); the seat's 42-row closure probe killed
 4239|   all 14.  Owner ruling 2026-10-08: close, one more pass, commit.  **Repair 4** (`killtable4_20261008/`, 43 rows): 91
 4240|   runs of 85 distinct mutants, all red.
 4241| * **Repair 4's pass** (`panel_pass2r4_20261008`, `opus_pass2r4_20261008/`): 15 of 18 kept 43/43 -- the closure covered
 4242|   WIDENING but not NARROWING (helper `& 0x17` admits 0x18-0x1a), not a constant forced to the expected polarity, not
 4243|   the msr decline per label, not T while latched.  Owner ruling 2026-10-08: **repair 5 GENERATES the coverage**.
 4244|   **Repair 5** (`killtable5_20261008/`, 47 rows): 110 runs, 104 distinct mutants, 103 red; every lane 47/47 before and
 4245|   after.  The one at 47/47, `M_msr_argmask` (the decline also writes the cached `ic->arg[1]`), is detected by none
 4246|   of the shipped 47 rows: each of their re-executions of an MSR crosses a debugger interaction, and `debugger()`
 4247|   clears every dyntrans translation when it interacts, so each is re-translated (a guest loop inside one `step N`
 4248|   does see it -- the filed prototype below).  Repair 5's NOT CLAIMED had said the grid pinned it -- FALSE,
 4249|   corrected comment-only.
 4250| * **The final pass** (`panel_pass2r5_20261009`, `opus_pass2r5_20261009/`): grok SHIP-WITH-CHANGES with 0 floor
 4251|   breaches; codex DO-NOT-SHIP with one class, which the Opus seat MEASURED: five one-line edits made only while the
 4252|   site's latch is CLEAR -- forcing N, or OR-ing in the old CPSR's bits 31:8, on the first DPI or pop decline, and forcing
 4253|   N on a latch-clear pop accept -- each 47/47; and two msr label x latch cells (`M_msr_clr0f_irq_first`,
 4254|   `M_msr_skip_irq_first`) 47/47.  The bodies never test bits 31:8, so the cells sit outside the joint-cell floor; the
 4255|   contract CLAIMED them, so it was one clause-(e) breach.  **Owner ruling 2026-10-09: commit, file the rest** -- the
 4256|   contract narrowed comment-only (the Opus seat's suggested text), NOT CLAIMED extended, and the measured closures
 4257|   (a zero-observation reorder of the restore grid sessions: the five go red at 46/47, fix 47/47; and a 48th loop row:
 4258|   fix 48/48, `M_msr_argmask` 47/48, HEAD 18/48) filed as `armmsrmodedebt`.  `M_msr_argmask`: DISCLOSURE (grok, codex,
 4259|   minimax, agy, the Opus seat -- the carrier's DEPENDS-ON bound covers dominating predicates and operand swaps, not an
 4260|   added persistent side effect) against OWED (deepseek, glm, kimi-k3 -- the fix's own comment names the invariant);
 4261|   the loop row is filed, not owed.
 4262| 
 4263| **The gate -- and what it caught.**  Gate 14's FIRST run on the round's code, alone (2026-10-09 08:14-09:58,
 4264| `gate14_20261009/gate14_run1.out`): 1106 of 1110 -- the new msrmode section all green (47/47, REDS none, no FAIL row) and
 4265| the four xscale checks RED, `ANCHOR_ISRC` and `ANCHOR_EXC` at 28/30.  **I first reasoned this could not be #562's -- the
 4266| anchor reads the interrupt source before the program's only MSR -- and the measurement said otherwise**: a HEAD build
 4267| 30/30 twice, both #562 builds 28/30 twice (`xscale_ab.out`).  The cause is the BUILD, not the fix: #562 grew `struct
 4268| arm_cpu` ahead of the i80321 fields, this build tracks no header dependencies, and every #562 build had rebuilt only
 4269| `src/cpus/*.o`, so `dev_i80321.o` -- the only object outside `src/cpus` that reads a field past the insertion -- kept
 4270| the old layout and set `isrc` at the old offset.  The two-part clearance had passed on all three trees.  `cd` is the
 4271| last member of `struct cpu`, so no subsequent `struct cpu` member shifted, and every other non-CPU ARM access
 4272| precedes the insertion; the msrmode probe drives `-E testarm`, which attaches no i80321, so the kill tables are
 4273| unaffected by this mismatch.  All three trees were rebuilt clean (xscale then scored 30/30 twice on `build/` and on
 4274| `/tmp/gxsec-build`, `xscale_clean.out`) and gate 14 re-run alone, 2026-10-09 10:08-11:52: **PASS, 1110 of 1110**
 4275| (`gate14_run2.out`; the msrmode section 47/47, xscale 30/30).  The gap is filed as `headerstaleobj`.  After the
 4276| second run GPT-6 Astra's confirmation corrected three comments -- two in the probe's docstring, one in the gate
 4277| section; the committed probe stays AST-identical to the measured one and the gate's code identical to its tested
 4278| copy (`gate14_20261009/*.TESTED.*`), so neither run is re-owed.
 4279| 
 4280| **The panel.**  Every pass fired GPT-6 Astra (codex at `ultra`), grok 4.7 (xhigh), agy (`gemini-3.8-flash-high`),
 4281| glm-5.3, deepseek-v4-pro, minimax-m3 and the kimi seat, plus the Opus 5.5 measuring seat through the Agent tool --
 4282| claude-opus-5-5 throughout by its transcripts (`agent_models.py`: every #562 seat `clean`).  **Fable 5.1 was
 4283| DELIBERATELY NOT FIRED on any pass** (owner instruction, 2026-10-07): the main loop (Opus 5.5) adjudicated each
 4284| pass, badge A.  **After the owner lifted that hold (2026-10-09), Fable 5.1 adjudicated the main loop's nine rulings
 4285| before the commit** (`regress/artifacts/armmsrmodekill/fable_adjudication_20261009/fable5_adjudication562.md`): RATIFY WITH CHANGES (3), all nine upheld -- R6
 4286| included: none of the final pass's escapes is a floor cell under the rules as written -- and its three records
 4287| corrections applied.  **The kimi
 4288| seat was the packet-fed `kimi-k3:cloud` on every pass** -- the kimi CLI was not launched on pass 1, §F2 and pass 2,
 4289| and returned "403 ... subscription does not have access to Kimi Code" on the four later passes, COVERED by the
 4290| substitute.  **The implementation helper (an Opus 5.5 agent) hit the account's weekly limit after repair 5's tables
 4291| finished**; their results were collected from its clone by the main loop.  **Calibration, recorded rather than
 4292| absorbed** (from each pass's `seat_verdicts.py` table): agy voted SHIP on repair 2's, 3's and 4's passes and minimax
 4293| on repair 2's and 3's, and after each of those passes the measuring seat built escapes (21 of 23, 14 of 20, 15 of 18);
 4294| codex voted DO-NOT-SHIP on pass 2 and on all four repair passes, and its final-pass prediction measured true;
 4295| deepseek's `spsr_copied` prediction (repair 2's pass) was measured KILLED, 37/38, and its final-pass G3 objection
 4296| confused the restore label with the accepted target; kimi-k3's final-pass ELSE (the DPI `default:` arm is new
 4297| behaviour, S-to-PC from USR/SYS being fatal at HEAD) is FALSE -- HEAD's switch had no `default:` either, so USR/SYS
 4298| fell through with CPSR unchanged onto a modelled Load, which the new arm reproduces (Fable 5.1's R4).  **Records errors in the chain, corrected:** the pass-2 brief
 4299| pasted run 2a's aborted 25/26 lines unmarked (kimi-k3, deepseek); repair 5's G1 sentence, `grid cov`'s scope, the
 4300| debugger's `step call` exception and the latch-clear contract claim (grok, codex, the Opus seat; probe docstring,
 4301| comment-only); PRETABLE5's withdrawn predictions (an appended, dated CORRECTIONS section; its text above is kept);
 4302| and the Opus seat posted predicted mutant scores mid-run on repair 4's pass and withdrew them itself -- every number
 4303| in this block comes from a driver's own output file.  **GPT-6 Astra's confirmation of the final package**
 4304| (`astra_confirm_20261009/codex_confirm562.txt`, at `ultra`): **CONFIRM WITH CHANGES (13)**, all records corrections and
 4305| all applied before this commit -- among them, two sentences of mine it found FALSE: "no stepping row can see"
 4306| `M_msr_argmask` (the loop prototype is a counterexample) and "`propagate_all_trees.sh` would have reported a header
 4307| as stale" (it relinks unconditionally and can report clearance success over stale objects).  It confirmed the probe's
 4308| executable source identical to the measured probe, the stale-object account and its scope, and both gate results.
 4309| 
 4310| **Dissent recorded, not absorbed:** codex's pass-1 whole-operation decline (preserve flags and masks, skip the
 4311| return's PC load) -- not adopted: grok ruled field-only under the owner's arrangement (grok rules Astra's findings),
 4312| and codex's own §F2 answer on that ruling was "The rejection is permissible; the warrant is false" -- neither policy
 4313| is architecturally mandatory, and the shipped one is recorded as a choice.  And deepseek's, glm's and kimi-k3's
 4314| final-pass grade of `M_msr_argmask` as OWED, carried verbatim into `armmsrmodedebt`.
 4315| 
 4316| **FILED** (OUTSTANDING_BUGS, 2026-10-09): `armusrstop` (MEDIUM -- a USR/SYS-mode `LDM {..pc}^` or `MSR SPSR_x` stops the
 4317| CPU at a `default:` that sets `running = 0`; the Opus seat, pass 1), `armspsrthumb` (MEDIUM -- a restore that sets T
 4318| keeps decoding ARM words until the run loop is next entered; first filed as "T not honoured", corrected from the
 4319| source before this block was written), `armmmuvehicle` (MEDIUM -- an MMU-on rung-3 vehicle, owed before
 4320| `armthumbabortkill` by that row's own reopen condition), `armmsrmodedebt` (LOW -- the detector's measured residue and
 4321| its measured closures), `headerstaleobj` (MEDIUM, harness -- a header change leaves stale objects that the
 4322| two-part clearance cannot see; found by this round's gate).  The next commit owes `#562`'s pass-2 receipt (`src/` changed) and the row's `commits` field.
 4323| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_562: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC562: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
