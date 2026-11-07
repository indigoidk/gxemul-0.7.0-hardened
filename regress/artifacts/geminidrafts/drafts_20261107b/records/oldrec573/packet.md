# Reading task: oldrec573 (Gemini web; 2026-11-06)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC573-afa2` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #573 lecsrmask (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (verbatim, CHANGELOG.md lines 1567-1701 at HEAD 116c5aa9)

```markdown
# `#573` Records (follow-up, 2026-10-25): `lecsrmask` names its landing commit `9ac43a17`; the committed-tree proofs; the pass-2 receipt

`git ls-tree 9ac43a17` shows `regress/le_csrmask_probe.py` at `100644 blob e19c4f591507a34670ac9dae03021cb709ec462d` with blob md5 `4aa4b22155c87af8809c2b3602d98540` -- the revision every leg of
`regress/artifacts/lecsrmask/pass1_20261025/final_055141/` froze (LF, no CR byte); the committed `src/devices/dev_le.c` blob md5 is
`55d47bdae4109bd1ef48d94421909bbc`, the file the fix legs were built from (`final_055141/dev_le.c.fix.txt`); the committed `regress/gate_arm.sh` carries the #573 block
and its `rows run` pin, `tools/precommit_check.sh` SCORE_CLAIMS_MANIFEST=41, `regress/gate_hygiene.sh` EXPECT_PTY_PROBES=79 with
`le_csrmask_probe.py` grandfathered, `tools/pipeline/check_probe_wiring.py` the two MANIFEST keys.  Landing numstat (310 files):
60 0 regress/gate_arm.sh; 3 2 regress/gate_hygiene.sh; 547 0 regress/le_csrmask_probe.py; 29 9 src/devices/dev_le.c; 12 0 tools/pipeline/check_probe_wiring.py; 1 1 tools/precommit_check.sh.  The ledger row's `commits` field names `9ac43a17`; its state stays `held` (the Fable question, the roster question, the
clause-(d) decision -- `hold_question`).  The PASS-2 RECEIPT line is appended to `regress/pass2_ledger.tsv` (precommit section F).

# `#573` (lecsrmask): the LANCE model stored every bit a guest wrote to CSR3, where the Am7990 implements three and reads the rest as zero -- the CSR3 store is masked to BSWP|ACON|BCON; CSR1 and CSR2 stay stored whole, on purpose, and the record says why

**The defect** (`lecsrmask`, MED, WRONG-RESULT; filed 2026-10-22 from the external-fixes research, T18 of its batch, as "CSR1-3
store all 16 bits (implemented-bit masks missing) -- port rpajarola e108b54").  `src/devices/dev_le.c`'s `le_register_write()`
handled CSR0 bit by bit and stored CSR1, CSR2 and CSR3 whole (`default:` / `d->reg[r] = x;`).  For CSR3 that is wrong on the
chip this model names ("LANCE ethernet, as used in DECstations" -- the Am7990): the Am7990 LANCE Technical Manual (AMD 1986,
`_scratchpad/lance/TM1986.txt` 1734) gives CSR3 bits 15:03 as *"Reserved and read as "O"."* and the Am79C90 C-LANCE datasheet
(`am79c90_bitsavers.txt` 1222-1223) as *"Reserved. Read as zeroes. Write as zeroes."* -- so a guest that wrote 0xffff read back
0xffff where the chip answers 0x0007.  **The rung-3 witness** (`regress/artifacts/lecsrmask/witness_20261025/`, cold debugger on the
UNMODIFIED `pmax -e 3100`, guest `sh`/`lhu` through the real decode at KSEG1 0xb8100000/0xb8100004, binary `6c27af7b` built from a
git-archive export of HEAD `0b09e7b6` whose `dev_le.c` -- md5 `3eab9c96` -- is byte-identical to this commit's parent's) measured it
2026-10-25 03:47-03:49, BEFORE any edit: `RESULTS_base.txt` 17/17 against the HEAD column (its FIX column carried the three-mask
design later withdrawn -- CSR2 `0x00ff`, CSR1 `0x1234` -- and is not the contract; only its HEAD column is evidence), with the symptom rows reading back
0xffff / 0xffff / 0x1235 for CSR3 / CSR2 / CSR1 writes of 0xffff / 0xffff / 0x1235, the device-signature rows `csr0 reset` 0x0004
and `rap mask` 0x13 -> 0x0003 green, the RAM liveness row green in every session and 69/69 hand-encoded words matching the
emulator's disassembler.

**The narrowing, and the evidence** (pass 1 of this round, adjudicated 2026-10-25 -- `pass1_20261025/PASS1_RULINGS.md`; the ruling of
record is GPT-6 Astra's `f2_20261025/codex_t18f2.txt`, RATIFY WITH CHANGES).  The research row proposed all three of rpajarola's
masks (CSR1 `& 0xfffe`, CSR2 `& 0x00ff`, CSR3 `& 0x0007`).  Only the CSR3 mask is established for the Am7990:
* the Am7990 manual says read-as-zero for RAP (`TM1986.txt` 1539) and CSR3 (1734) and NOT for CSR1 bit 0 (*"Must be zero."*, 1749
  -- a constraint on the host's writes) or CSR2 bits 15:8 (bare *"Reserved."*, 1695);
* the C-LANCE datasheet reads CSR2's reserved bits as zero (1161-1163) but says only *"Must be zero."* for CSR1 bit 0 too
  (1138-1142), and its Appendix B (3411) lists CSR1/CSR2 among the two chips' differences;
* MAME's `am79c90.cpp` (fetched 2026-10-25) stores CSR1 whole on both chips and CSR2 whole on the Am7990 -- masked only on the
  Am79C90 -- its comments citing a MIPS RS2030 system diagnostic that *"requires these bits to be writable"* and *"assuming this
  is older device behaviour"*;
* rpajarola's commit `e108b546` (fetched the same day) applies the masks for a 3MIN (KN02-BA) IOASIC LANCE port this fork does not
  carry, citing that PROM's `3/ni/regs` test; it names no chip.
So CSR1 and CSR2 **retain the model's existing behaviour** -- stored whole -- an interpreted reading recorded as one, and the
CSR1/CSR2 read-back question is FILED (`lecsr12readback`) with both readings; a per-chip model flag is the port if a C-LANCE
instance is ever added.  Pass 1's brief had stated two premises wrongly and the seats caught both: *"no LANCE datasheet is on disk"*
(both manuals have sat in `_scratchpad/lance/` since 2026-07-25 -- the carrier's `ls _scratchpad/*.pdf` does not descend) and
*"the Am7990 manual's prose carries no read-as-zero sentence"* (a `head -40` cut the grep before the register pages) --
`pass1_20261025/PASS1_CORRECTIONS.md` C1-C15.

**What ships** (one product file, byte-identical in `GXEMUL-SEC/` and `est/`; one new detector; the gate, manifest and hygiene
wiring).
* `src/devices/dev_le.c` -- `le_register_write()`: an explicit `case 3:` stores `x & 0x0007` with the two manuals cited; the
  `default:` arm (now CSR1 and CSR2 only -- `r` is `d->reg_select = idata & (N_REGISTERS - 1)`, so 0..3) keeps `d->reg[r] = x;`
  under a comment recording the interpreted reading.  The odd-address warning at `le_chip_init` stays (CSR1 is not masked, so
  it is reachable).  Two comments in `DEVICE_ACCESS(le)`'s RDP arm (reads/writes of CSR1..3 "if the stop bit is set") INVERTED the
  manuals' condition -- CSR1-3 are *"Accessible only when the STOP bit of CSR0 is a ONE"* (TM1986 1733; C-LANCE 1123-1124), and
  with STOP clear *"a READ operation will return undefined data. WRITE operation is ignored"* (TM1986 1572-1582; C-LANCE 915-924)
  -- and are corrected as records (L4), attributing the Ultrix observation to the old comment; the model's acceptance of either STOP state is
  unchanged and filed (`lestopgate`).  Two hunks (29 added, 9 removed); `#573` tags.
* The guest-visible change is the CSR3 read-back only: `reg[3]` has no reader but the indexed RDP read (`grep -n 'reg\[3\]'`
  matches nothing; the three implemented bits are never consulted by the model either -- filed, `lecsr3inert`).  A CSR1 mask would
  NOT have been read-back-only: `le_chip_init` builds `init_block_addr` from `reg[1]` and `le_read_16bit` preserves bit 0, so an
  odd initialisation block would have moved one byte (codex, pass 1) -- one reason the narrowing is also the safer change.
* `regress/le_csrmask_probe.py` -- the detector, 20 rows on the unmodified `pmax -e 3100`, no image: the three SYMPTOM rows
  `csr3 all` (0xffff -> 0x0007), `csr3 hi` (0x0008 -> 0x0000, the dropped boundary bit with bit 0 clear) and `csr3 mix` (0x0015 ->
  0x0005, kept bits with a dropped bit -- it reds a saturating clamp and a mask conditioned on bit 3, the escapes two seats
  named); the kept row `csr3 bits` (0x0005); three CONTRACT rows pinning CSR1/CSR2 stored-whole at identity wants (`csr1 all`
  0xffff, `csr1 odd` 0x1235, `csr2 all` 0xffff -- a later per-chip change re-pins them under the oracle-correction order);
  `csr2 lo`, `csr1 even` (0x1236, the kept boundary bit), `csr1 top` (insurance); the two signature rows; four liveness and four
  repeatability rows.  The park control verifies the breakpoint banner's pc against the halt address; CONTROL is the control-kind rows (liveness,
  signature, kept-bits, repeatability) plus the word encodings and the park checks, so a red SYMPTOM or CONTRACT row fails the leg
  but not CONTROL by itself; each CSR session writes 0xffff first, which is load-bearing against an OR-accumulating store and says so.
  The header carries the CONTRACT (CATCHES / OUTSIDE / ANCHOR).  Wired into `regress/gate_arm.sh` in the same commit (sentinel
  first, one control line, 20 named rows matched by the house idiom -- `count()` is `grep -ac`, BASIC regex, and the block's first
  draft's `+` matched ZERO rows in the dry run -- then `rows run` 20 / `rows green` 20 / `rows emitted` 20 / `rows red` 0 as four
  equality checks, the `rows run` pin raising `SCORE_CLAIMS_MANIFEST` 40 -> 41 in `tools/precommit_check.sh`; its own reason line -- the gate is the tree's
  device-probe gate by accretion and `gatedevicesplit` stays OWED, not compounded silently); MANIFEST lines in
  `tools/pipeline/check_probe_wiring.py` for the detector and for the 17-row witness copy
  (`witness_20261025/le_csrmask_probe.frozen.py`, CLASS_WITNESS); `regress/gate_hygiene.sh` re-derived by
  `tools/derive_hygiene_pins.sh` (`--grandfather le_csrmask_probe.py`, then `--write`): EXPECT_PTY_PROBES 78 -> 79, the probe grandfathered as promptless (it drains on timeouts and watches the breakpoint banner).

**Measured** (every number names its artifact; the instrument is frozen per run, and every score below is READ from the final
cycle's `RUN_IDENTITY.txt` by the landing generator, never typed):
* `pass1_20261025/final_055141/` (`RUN_IDENTITY.txt`; one frozen copy of the instrument for every leg, md5 `4aa4b221`, 547 lines): HEAD column on the pre-fix build 20/20, CONTROL=OK (`RESULTS_head_column.txt`); **L0, the pre-fix build in GATE mode (the FIX column): 17/20, CONTROL=OK -- `csr3 all`, `csr3 hi`, `csr3 mix` red** (`RESULTS_L0_prefix_gate.txt`; floor clause (a)); **L4, the verbatim reinstatement -- `d->reg[r] = x;` put back inside the new `case 3:`, rebuilt, binary `b21866ff`: 17/20, the same three rows red** (`RESULTS_L4_reinstatement.txt`; clause (b), a separately built and measured leg after a pass-2 seat objected to reading L0 as (b)); **L3, the null medium `/bin/false`: 0/20, CONTROL=FAIL** (`RESULTS_L3_nullmedium.txt`; `(c): measured at` that path); **L1, the fix build in GATE mode: 20/20, CONTROL=OK** (`RESULTS_L1_fix_gate.txt`); **L2, the two-leg run with the same script: base vs HEAD column 20/20, fix vs FIX column 20/20** (`RESULTS_L2_twoleg.txt`).  Fix binary `b578bf21` (the base clone plus this patch, `dev_le.o` removed, `make -j4`, binary newer than source), its `dev_le.c` md5 `55d47bda` == this commit's file.
* Earlier revisions, preserved because each instrument carries its own numbers: the comment-only predecessor of the landed
  instrument (md5 `6259ce54`, 538 lines; the code AST-identical to the landed file, the docstring and one comment corrected on
  pass 2) measured in `pass1_20261025/final_045716/` -- HEAD column 20/20, L0 17/20, L3 0/20, L1 20/20, L2 20/20 + 20/20 -- the
  set pass 2 and its adjudication reviewed; the 18-row revision (three masks) `pass1_20261025/det18_HEAD/` 18/18 HEAD column and
  `floor_20261025/` L0 14/18 / L3 0/18; the 17-row witness as above.
* **Clause (d) -- the variant table -- is OWED, not measured** (`killtable_20261025/README.txt`; `PRETABLE.out` written before
  it).  (d) IS a floor clause in the carrier; it is recorded here UNMEASURED, as owed, with no breach and no measurement claimed --
  whether the round lands with that debt filed is the OWNER'S decision for this round (the row's `hold_question`, item 4): the
  main loop read the 2026-10-21 direction for classifier-stopped measurement work (hold it, file the measurement as owed, land
  on the plain regression legs) as applying here, and the adjudication pass (Grok, F2b) read `#567`'s "land with filed debt" as
  having filed NON-floor coverage debt after its floor rows were added -- so no earlier ruling is cited as the licence, and the
  record says OWED and nothing more (the pass-2 brief of this round had understated (d) as "the separate null-repair clause";
  the adjudication pass corrected that premise): the F2 packet's variants V7'-V10', V21-V25 were classified by three seats (predicted red sets in `f2_20261025/F2_PACKET.md`
  4.3) and not built in this session, under the standing rule after a classifier stop of the main loop's own response (the
  `#567` "land with filed debt" precedent) [2026-11-02, records: withdrawn by the sentence above, which says the adjudication pass (Grok, F2b) read `#567` as filing NON-floor coverage debt, "so no earlier ruling is cited as the licence"].  The contract names what the rows are known to catch; the table is a filed obligation.

**The panels.**  Pass 1 (`pass1_20261025/`): GPT-6 Astra NOT READY, Grok 4.7 NOT READY (both on the CSR1/CSR2 premise), GLM 5.3
READY WITH CHANGES (two firings), DeepSeek NOT READY / READY WITH CHANGES, Gemini 4 Argon READY WITH CHANGES by the session-cookie
web route (`argon_api_Q12/`, `argon_api_Q34/`) after its agy transport walled on quota at launch (resets ~5 days); Fable 5.1 HELD
(`FABLE_HOLD_QUESTION.md`); kimi, minimax and the Opus seat deliberately not fired (`SEATS_NOT_FIRED_20261025.txt`).  The
adjudication pass (`f2_20261025/`): Astra RATIFY WITH CHANGES (WRONG: D2 -- kept/dropped bits are contract coverage, the labels are
the floor; F22 -- "Write as zeroes" constrains the writer), Grok, GLM x2 and DeepSeek x2 RATIFY WITH CHANGES; Argon's F2 answer
OWED (the web meter was exhausted by the pass-1 firing).  **Pass 2** (`pass2_20261025/`, on the real diff and the measured legs): GPT-6 Astra, Grok 4.7, GLM 5.3 (two firings) and
DeepSeek (two firings) -- all SHIP WITH CHANGES, no product-code defect; 44 findings consolidated with dispositions in
`pass2_20261025/f2_20261025/F2B_PACKET.md` and ruled in `PASS2_RULINGS.md`.  Its **adjudication pass F2b** (`pass2_20261025/
f2_20261025/`): Astra RATIFY WITH CHANGES (WRONG: F28 -- the pins should bind to the shipped population; not adopted, the deriver's
output governs under the owner's 2026-09-23 census ruling), Grok RATIFY WITH CHANGES (WRONG: F23's rule text, F25's licence
sentence, F39, F40 -- `#567`'s "land with filed debt" filed non-floor cells, so the clause-(d)-owed landing is the owner's
decision for this round, now the row's hold question), GLM A RATIFY WITH CHANGES (WRONG: F10 -- a mask whose VALUE varies with
bit 3 passes every CSR3 row, so the CATCHES bullet was narrowed and that family disclosed OUTSIDE; F25 -- the TM1986 line
1572-1582 cited, Appendix B attributed), GLM B, DeepSeek A (WRONG: F28, the colloquial sense of "promptless"; not adopted) and
DeepSeek B RATIFY WITH CHANGES.  Every seat ratified L4 -- the reinstatement BUILT inside the landed structure -- as clause (b)'s
leg (DeepSeek's pass-2 objection to reading the pre-fix build as (b) was right and the main loop conceded it), and `held` as the
landing state.  The probe's docstring and one code comment were corrected on pass 2 and F2b (eight record changes; the code
AST-identical to the pass-2 revision 6259ce54), the fix clone rebuilt from the comment-corrected patch, and all six legs
re-measured on one frozen copy before landing.  Argon: a seat failure on pass 2 and F2b (meter 0 of 2400 until 07:30:45 CDT),
re-fired after the reset -- *corrected in place 2026-10-25: that clause was written at 06:25 in the past tense while the
re-fire had not yet run; it ran 07:35-07:44 and the four answers are filed in the second records commit, with the
pass-1 F2 pair still owed (the sender slept at 8.3% of the meter until 12:32:15 CDT)*; Fable 5.1 HELD with its question; kimi, minimax and the Opus review seat not fired by roster.

**Records and filings.**  `OUTSTANDING_BUGS.md` 2026-10-25: `lecsrmask` NARROWED (the CSR3 half fixed; the CSR1/CSR2 half
withdrawn and filed; the ledger row lands `held` for the Fable question and the owner's roster question and closes NARROWED when
they are discharged -- a round may not close while a stage awaits a seat); filed `lecsr12readback`, `lestopgate`, `lecsr3stopclear` (CSR3 cleared by STOP per both manuals, and the
LACK of a preservation guarantee for CSR1/CSR2 across STOP -- the Am7990 manual itself says they "must be reloaded" (TM1986 1513)
and are "normally not affected ... recommended to reload" (2853-2857), while the Am79C90 datasheet's Table B-1 characterises the
Am7990 as NOT preserving them (3411 right column; 3686-3687): the sources differ and all three readings are recorded; the model
leaves CSR1-3 untouched by a STOP write -- CSR3 never cleared, CSR1/CSR2 trivially kept -- and `#573` adds no STOP behaviour), `lediagfmt` (`uint64_t` values passed
to `%i` at 1019-1020, `%x` at 1039-1040, `%05x` at 911/921) (lines of 9ac43a17^; at 987cb596 `%i` :1039-1040, `0x%06x`/`0x%08x` :1059-1060, `%05x` :928/:938), `lecsr3inert`, and the carrier's source-list item; OWED: the variant
table; Argon's F2, pass-2 and F2b answers (the web meter read 0 of 2400 from the pass-1 firing until its 07:30:45 CDT reset,
after which they are re-fired and filed in the records commit -- *corrected in place 2026-10-25: the FIRST records commit,
94b247db, predates the re-fire; the pass-2 and F2b answers are filed in the SECOND; the pass-1 F2 pair is still owed*).  **A follow-up to `#572`'s follow-up `2956c32d`**: its census population -- the 78 counts the
peer's untracked `regress/lca_isaphys_probe.py`, which the gate counts because the battery runs in this tree; the committed-HEAD
defect was the NAME SET (`wdc_lba_probe.py` promptless and not grandfathered), not the tracked count (77 = the old pin).

```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_573: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC573: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
