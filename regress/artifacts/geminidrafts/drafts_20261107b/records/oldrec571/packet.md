# Reading task: oldest-rec-571 (Gemini web; 2026-11-06)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC571-bf5b` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #571 ppcdsformxo (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.

## The round block (verbatim, CHANGELOG.md lines 1865-2040 at HEAD)

```markdown
# `#571` (ppcdsformxo): the PowerPC decoder folded the DS-form XO bits into the displacement, so `ldu` and `lwa` ran as `ld` at EA+1 / EA+2 and `stdu` ran as `std` at EA+1 with no base update -- opcodes 58 and 62 now decode their five forms, reserved encodings and the RA = 0 update forms stop the cpu, and a 39-row rung-3 detector gates it in gate 13

**The defect** (`ppcdsformxo`, HIGH; filed 2026-10-22 from the external-fixes research, T2 of its batch; class
GUEST-CORRUPTION).  `src/cpus/cpu_ppc_instr.c`'s D/DS-form load/store arm takes the whole low halfword as the
displacement (`imm = (int16_t)iword`) for all 24 of its primary opcodes and gives opcodes 58 (`PPC_HI6_LD`) and 62
(`PPC_HI6_STD`) one fixed decode each -- an 8-byte load / store with no update -- although in the DS form the low two
bits of the halfword are the XO field that selects `ld` / `ldu` / `lwa` (58) and `std` / `stdu` (62).  So on a 64-bit
CPU every `ldu` loaded from EA+1 and performed no base update, every `lwa` loaded a DOUBLEWORD from EA+2 instead of a
sign-extended word, and every `stdu` -- the instruction every PowerPC64 stack frame is pushed with -- stored its 8
bytes at EA+1 and left the stack pointer alone.  The rung-3 witness (`regress/artifacts/ppcdsformxo/
witness_20261024/`, cold debugger on UNMODIFIED `bareppc -M 64` = PPC970, HEAD `add098b9` = `c8fcb5ff` in source) is RED
on HEAD: 5/8, three symptom rows red for the reason under test -- `ldu value` names offset 0x21 of a counting pattern
whose architectural EA is offset 0x20, `ldu RA after` shows RA = 0x20080 where EA (0x20020) was owed, `lwa value` is
the doubleword at offset 0x8a where the sign-extended word at 0x88 (`0xffffffff88898a8b`) was owed; the controls are
green (`ld` at XO 0 with a negative DS reads the right doubleword, `lwz` on the same pattern reads the right word, a
liveness `li`, a 13/13 disassembly census, a bogus-machine-TYPE negative control).  The store half is not in the witness
(three store-bearing witness attempts were stopped before writing); it is measured RED on the base binary by the
detector's own pre-fix run (`table1_20261024/prefix_BASE.out`, 17 of 39 red, below).

**What ships** (one product file, byte-identical in `GXEMUL-SEC/` and `est/`; four harness files).
* `src/cpus/cpu_ppc_instr.c` -- inside the arm's inner `switch (main_opcode)`, `case PPC_HI6_LD:` and
  `case PPC_HI6_STD:` become DS-form decodes: each re-assigns the shared `imm` to `(int16_t)(iword & ~3)` -- EXTS(DS ||
  0b00), enumerated equal for every DS and XO because the clear never reaches the halfword's sign bit -- so the table
  index (`imm == 0` selects the `_0` handler family) and `ic->arg[2]` both see the masked displacement, and dispatches on
  `iword & 3`: 58 -> `ld` (XO 0), `ldu` (XO 1, `update`), `lwa` (XO 2, `size` 2 and `zero` 0: the existing
  sign-extending word handler `ppc_instr_lwa`, slot 10 of the generated `ppc_loadstore[]`), reserved XO 3 -> the arm's
  bare `goto bad`; 62 -> `std` (XO 0), `stdu` (XO 1), reserved XO 2 and 3 -> `goto bad`.  No handler changes: every form
  selects a slot the generated table already holds (`ld` 15/31, `ldu` 47/63, `lwa` 10/26, `std` 7/23, `stdu` 39/55 --
  `tmp_ppc_loadstore.c:893-958`), and none reaches `ppc_instr_invalid` (slots 11/27/43/59, `load && !zero && size == 3`).
  TWO BEHAVIOUR CHANGES besides the displacement: a reserved XO, which executed as `ld`/`std` at EA+2 / EA+3, now stops
  the cpu through the common tail (`cpu_dyntrans.c:2004-2014`: `UNIMPLEMENTED instruction at 0x...`, printed under
  single-step too; nothing is delivered to the guest -- the tree has no Program interrupt), and `ldu`/`stdu` with RA = 0,
  which executed at the absolute address EXTS(DS || XO) with no update, now reach the arm's EXISTING `ra == 0 && update`
  guard (`:4367-4371` in the committed file) and stop -- the disposition every other update form in the arm already takes.  `ldu` with RA = RT
  (an invalid form; Book I allows boundedly undefined results) is DISCLOSED, not checked -- the handler loads RT and then,
  when the access succeeds, writes RA = RT with EA, as the sibling update loads do; `stdu` with RA = RS is VALID and stores the old RS before the
  update.  32-bit CPUs: opcodes 58 and 62 are illegal on 32-bit implementations (PEM :6253); before and after this fix a
  32-bit CPU decodes them through the same arm (one source builds both decoders); the MODE32 table holds real doubleword
  handlers (`tmp_ppc_loadstore.c:1923+`), so no host exit either way; after the fix the legal forms select those
  handlers and reserved XO / RA = 0 updates stop there too; no width test this round (filed, below).  The shared
  assignment at `:4295` and the other 22 opcodes of the arm are NOT touched.  Option set recorded in
  `pass1_20261024/PASS1_RULINGS.md` A3 / A6 / D1 / D2.
* `regress/ppc_dsform_probe.py` (new; 848 lines, 41,889 bytes, md5 `e0a1e67eb0283abccde3bbd53952487a`; the FROZEN and MEASURED revision is
  836 lines, 40,883 bytes, md5 `0266228894811ba6c51cff82585753c9` -- the shipped file differs by THREE docstring/comment-only
  revisions, from pass 2, its adjudication and the final clearance (`table1_20261024/repair_p2/probe_docfix.diff`,
  `probe_docfix2.diff`, `probe_docfix3.diff`), each verified code-identical by stripping docstring and comments from both
  revisions and re-measured: `prefix_BASE2.out`, `prefix_BASE3.out` and `prefix_BASE_r3.out` 22/39 with the identical red set,
  `fixed2.out`, `fixed3.out` and `fixed_r3.out` 39/39, gate 13 PASS 193 each time) -- the detector, the promoted copy of the
  witness probe (the
  witness file stays byte-identical under `witness_20261024/`, md5 `5e96b69df49ac82e10b3118780899549`; its build and run
  receipts are frozen in `witness_20261024/receipts/`).  Frozen before its first run at md5
  `0266228894811ba6c51cff82585753c9` (`table1_20261024/BASELINE.out`, `DETECTOR_FREEZE.txt`).  SEVEN stepped guest sessions on `-E bareppc -M 64` and one negative session: loads (the five witness words plus
  `ld`/`ldu`/`lwa` at DS = 0, `ld`/`lwa` with RA = 0 from a seeded low-memory window, a `lwz` at +6 whose displacement
  has non-zero low bits -- the control that sees a mask applied to every opcode), stores (`std`, `stdu`, `stdu` at DS = 0,
  `stdu rA,DS(rA)`, `std` at DS = 0 and `std` with RA = 0 (two words; their joint cell is NOT CLAIMED), a `stw` at +6; every destination read back by the debugger's `dump` over a
  pre-seeded window EA-1 .. EA+11 -- the flanks graded for the ordinary `stdu` only -- each source eight distinct bytes
  except the alias store's, which is its old base), five stop sessions (58/XO 3, 62/XO 2, 62/XO 3,
  `ldu` RA = 0, `stdu` RA = 0 -- each a liveness `li` then the word LAST, since `bad:` clears `running`), and the
  negative apparatus.  Every word is produced by the probe's encoder; the disassembly census compares every placed word
  against the tree's CURRENT disassembler text (which folds XO -- see the filing) with the expected XO taken from a
  label-keyed map, and the three witness words are pinned to their literals.  Row names are capped at 14 characters by an
  assert in `row()` -- a margin: the gate's `%-16s` column gives a 15-character name its two spaces as well (16 misses).
  The measured revision's comment stated the stricter, false reason; pass 2 (K1, dispute D1 in `PASS2_RULINGS.md`)
  corrected it in place in the docstring/comment-only revision above.  Protocol: `PPC_DSFORM_RESULT=ok/N`,
  `PPC_DSFORM_CONTROL=OK|FAIL`, `PPC_DSFORM_SYMPTOM=PRESENT n/m|ABSENT|MIXED`, `PPC_DSFORM_RED=<names>|none`,
  sentinel `PPC_DSFORM_PROBE_DONE`; non-zero exit on any red.
* `regress/gate_ppc.sh` (gate 13) -- a `#571` block directly after the `#565` rldicl block and BEFORE the NetBSD image
  `need_file`, on the same machine as the register probes: the probe into `$LOGDIR` with `|| true`; every protocol key
  counted exactly once in any form and then its accepted value once (`RESULT=39/39`, `CONTROL=OK`,
  `SYMPTOM=ABSENT`, `RED=none`); the sentinel once; every one of the 39 row names once and green; rows emitted /
  green / red pinned by literal; the gate's title gains ` + #571 DS-form`.
* `tools/pipeline/check_probe_wiring.py` -- two MANIFEST keys: `ppc_dsform_probe.py` CLASS_DETECTOR (gate 13,
  39 rows, the table path) and `artifacts/ppcdsformxo/witness_20261024/ppc_dsform_probe.py` CLASS_RESEARCH -- the frozen
  copy asserts the REPAIRED property (5/8 on HEAD, 8/8 post-fix), so by the checker's own WITNESS/DETECTOR line (`:55-57`: a
  WITNESS asserts the pre-fix symptom and is RED once the defect is gone) it is a preserved instrument, not a witness; an earlier
  round's post-fix-green frozen witness (`m88kbuserrregs`) and #539's post-fix entries are classed WITNESS against that line and
  are filed (`wiringwitnessclass`).  Landed as the
  HEAD blob plus exactly these two keys (`table1_20261024/staged/check_probe_wiring.py.txt`); the working tree's uncommitted
  peer lines are not committed.
* `tools/precommit_check.sh` -- `SCORE_CLAIMS_MANIFEST` 38 -> 39 with its dated line: the one newly gated probe,
  `ppc_dsform_probe.py`, pinned UNQUOTED in `gate_ppc.sh` at 39 rows under the stem `ppc_dsform`; its docstring is checked.

**Measured** (`regress/artifacts/ppcdsformxo/table1_20261024/`; every score against its instrument revision and
denominator; the instrument md5 in `BASELINE.out`; `PRETABLE.out` written before table 1, `PREDICTIONS.txt` per leg
before each leg).
* Pre-fix, the BASE binary (`c8fcb5ff`'s `src/`, which HEAD `add098b9` leaves unchanged; binary md5 `3cd0501c`): `prefix_BASE.out` **22/39, CONTROL=OK,
  SYMPTOM=PRESENT 17/17** -- the 17 symptom rows (`ldu value`, `ldu RA after`, `ldu ds0 value`, `lwa value`, `lwa ds0 value`,
  `lwa ra0 value`, `stdu value`, `stdu neigh`, `stdu RA after`, `stdu ds0 value`, `stdu alias val`, `stdu alias RA`,
  `xo58_3 bad`, `xo62_2 bad`, `xo62_3 bad`, `ldu ra0 bad`, `stdu ra0 bad`), each red by the misdirected address, the
  shifted destination window or the missing stop; every control green.  This is the STORE half's clause-(a) artifact.
* Post-fix: `fixed.out` **39/39, ABSENT, RED=none**; the frozen 8-row witness `fixed_witness8.out` **8/8, ABSENT** (clause
  (a), same script as the witness).
* The kill table (`SCORES.txt`; `PREDICTIONS.txt` written per leg before any leg ran; sixteen variant legs, each a
  discarded clone of the fixed tree with a `.MUTANT` sentinel): clause (b) `L3` both case bodies reinstated 22/39, `L4b`
  the 58 case alone 31/39, `L4c` the 62 case alone 30/39; clause (c) `L5` the identity body (the no-op handler for both
  opcodes) 17/39 CONTROL=FAIL -- **(c): measured at `L5_identity.out`**; `L5b` the binary absent: no sentinel; clause (d)
  `L6a`/`L6b` update dropped 37/39, 36/39; `L7` the raw displacement kept 27/39; `L8a`/`L8b` the `lwa` width and extension
  nulled 36/39 each; `L8c` `lwa` at size 3 with `zero` 0 selects the invalid handler and ENDS THE EMULATOR on the loads
  session -- 25/39, the exit recorded on the session line, the sentinel still printed (scored as emulator termination,
  never as a wrong-width transfer); growth `L9a` XO 0 as XO 1 33/39, `L9b` EA+1 on XO 0 33/39, `L10` update on every form
  31/39, `L11` the mask on the shared assignment 37/39 (the two D-form scope rows), `L12a`/`L12b` a reserved test opened
  38/39 each.  Fourteen legs at their written prediction exactly; `L9a` and `L10` two rows REDDER than predicted (the
  session-liveness rows: a word with RA = 0 that the variant turns into an update form refuses and stops its session before
  the liveness `li` -- L9a at the `ld ra0` word, L10 at the `lwa ra0` word, both store sessions at `std ra0`;
  `L10_updall.out:40`, `L9a_xo0asxo1.out:40`) -- prediction misses recorded in `SCORES.txt`, no detector miss, no leg green,
  no leg red for another reason.
* Two-part clearance (`CLEARANCE.out`): build/ CLEAN + FRESH (gxemul `a142d92a`), build-asan/ CLEAN + FRESH (`79d75442`),
  /tmp/gxsec-build CLEAN + FRESH (`14ede3bd`); est/: source tree, part 2 N/A.
* Gate 13 alone (`gate13_20261024.out`, `bash run.sh 13`, build/gxemul `a142d92a`): **PASS, 193 checks, REGRESS_PASS** --
  the `#571` block's 53 checks all ok (39 rows by name, census 108/108, rows run/green/red 39/39/0; the gate's detector
  log preserved as `gate13_ppc_dsform.log`); the siblings unchanged (rlwimi 28/28, rldimi 29/29, rldicl 24/24 with one
  SCORE line) and the image-gated rounding probe green -- the one other consumer of the edited arm (its FP D-forms and
  `stw`; its displacements are all multiples of 4, so it is collateral, not low-bit coverage).
* No boot A/B is owed (`BUILD_SPEC.md` section 8): no PowerPC guest image in this tree's battery boots through opcodes 58/62
  (Argon's pass-1 census), so the stepped detector is
  the round's only runtime instrument; the gate's detector log is preserved with its completion line.

**Panel.**  Pass 1 (`pass1_20261024/`): GPT-6 Astra (ultra, file-reading, pointer form), Grok 4.7 (xhigh, plan mode),
Gemini 4 Argon (file-reading through agy, `gemini-4-argon-high`; transport and reading-scope caveat in
`argon_transport_20261024.txt`), GLM 5.3 and DeepSeek v4-pro (packet-fed, the 74,595-byte PACKET form split Q1-2 /
Q3-4) -- seven answers: five READY WITH CHANGES, DeepSeek NOT READY twice (on a 32-bit width test, ruled (i) disclose,
and on the store rows, specified in B1/B6).  Fable 5.1 HELD by the owner (hold question in `fable5.HELD.txt`); kimi,
minimax and the Opus seat deliberately not fired by roster (`roster_NOT_FIRED.txt`).  The main loop's 31 dispositions
and eight disputes are `PASS1_RULINGS.md` (A1-A9, B1-B13, C1-C9, D1-D8, with five measured main-loop checks M1-M5);
ADJUDICATED by GPT-6 Astra (`adj/codex_t2p1adj.txt`, AMEND: eleven dispositions amended -- A3, A6, A9/B9, B2, B7, B10,
B11/B13, B12, C4, Q3, Q5, written as the eight items of `BUILD_SPEC.md` section 10 -- and it withdrew its own (ii) and
"all 22 labels" claims) and by Grok 4.7 (`adj/grok_t2p1adj.txt`, AMEND) -- the two adjudicators disagreed on ONE point
(whether the DS = 0 x RA = 0 refusal cells are floor) and the main loop ruled for Grok on the carrier's pass-11 bound,
trimming Astra's eight added legal-access cells to the five single-axis marginals (section F2).  Grok also raised the
padded-column trap on the proposed names (names capped at 14 -- a margin: measured at pass-2 drafting, the gate's
`%-16s` column still gives a 15-character name its two spaces, so the recorded "misses the pin" reason was false) and
caught a false citation in A3.  Pass 2 (`pass2_20261024/`): GPT-6 Astra, Grok 4.7, Gemini 4 Argon through agy, GLM 5.3 and DeepSeek v4-pro (Q1-2 / Q3-4
firings) -- seven answers, seven LAND WITH CHANGES, no product-code defect; twenty-eight numbered findings (`PASS2_RULINGS.md`
F1-F28; the drafter's own seventeen inconsistencies among them) whose required changes concern records, comments and contract
wording, two disputes: D1 (the probe's false names-cap comment) ruled EDIT -- the docstring/comment-only revision above, re-measured; D2
(the STD comment's missing `stdu` RA = 0 clause) ruled no product edit, Grok's dissent carried.  Argon's Q2 described rows,
legs and scores that exist nowhere in the round's files (F25) and is credited for Q1 only.  F2 adjudication (`adj/`): GPT-6 Astra AMEND -- the decoder and the measured floor stand; four accepted dispositions (F19, F20, F21, F26) left incomplete record repairs, all applied; two defects of the repair's own records corrected (DETECTOR_FREEZE's over-wide sentence, the roster count); the chain closed with zero floor breaches over the probe diff's three hunks, the gate diff's two hunks and the three re-measured runs; LANDING: GO WITH THE CHANGES NAMED; Grok 4.7 AMEND -- the product diff and the detector's behaviour stand; two accepted repairs were wrong records: the docstring's sign warrant (replaced in the second docstring/comment-only revision: the bodies copy the DS sign into imm and never branch on it, and do not read RA) and sev=RESEARCH on ppc64on32gate (OVERTURNED on the precedent's meaning: severity left unset); PRETABLE :31 quoted in the erratum; the floor chain closes; LANDING: GO WITH THE CHANGES NAMED.  Astra's exact-text readings of the landed texts (`adj/final/codex_t2final*.txt`): reading 1 named twelve record corrections -- ten completed, one left incomplete and one wrongly rejected (the frozen witness copy's MANIFEST class: the checker's WITNESS/DETECTOR line governs, the copy asserts the repaired property, so it is CLASS_RESEARCH, and the mis-classed precedents are filed as wiringwitnessclass); reading 2 named ten -- nine applied, one (the stale count sentences) left incomplete; reading 3 named seven, applied; each later reading is recorded in PASS2_RULINGS.md, and the reading that says GO is the clearance this commit rests on.

**What the records claim, and do not.**  The detector claims the five legal DS forms at DS != 0, at DS = 0 and (the
non-update forms) at RA = 0, the three reserved encodings, the two RA = 0 update stops, and the D-form scope controls
(a load and a store whose displacement has non-zero low bits), on PPC970 with translation off.  NOT CLAIMED, disclosed
in the probe's contract: `ldu` RA = RT (D1); 32-bit CPUs (illegal opcodes, decoded through the same arm, so their MODE32
  decode and refusal behaviour change with this fix exactly as the 64-bit one's; the future fix is the
`rld*` width idiom applied to the whole ungated set, filed); the DS = 0 x RA = 0 update cells (multi-axis joint, the only
observer of an update conditioned on a non-zero displacement); a positive-word `lwa` (the sign is the callee's cast);
translation on, MSR SF, page-crossing EAs, the indexed forms, an access that fails (the translation-off failure path
exists but is gated by `-T`, which the probe does not pass); the disassembler's mnemonics (the census attests opcode,
RT/RS, RA and the raw halfword against the CURRENT text, never the form).  Three premises of the pass-1 brief were
corrected in the record rather than carried: "the two uses of `imm` matter only for DS = 0" (inverted: `arg[2]` matters
for every XO != 0 word; the index use is unobservable on PPC970), "a base not a multiple of 8 gives an unaligned
`ld`/`std`" (base residue 4 plus displacement residue 4 is aligned), and "`lwa` left at size 3 consumes the neighbour
word" (with `zero` 0 it selects `ppc_instr_invalid` and exits the emulator -- the probe records the exit and still
prints its sentinel).

**Filed** (ledger rows, all source-derived unless stated): `ppcdisasmxo` (LOW -- `cpu_ppc.c:1495-1517` prints `ld`/`std`
with the XO folded into the displacement for every opcode-58/62 word; guest-invisible; witness = the frozen census lines
`ld r5,-95(r21)` / `ld r6,10(r22)`; its fix owes the oracle-correction order: re-pin the census first),
`ppcdisasmfpupd` (LOW -- the disassembler has no case for `LFDU`/`LFSU`/`STFDU`/`STFSU`, which execute since `#310` and
disassemble as an unimplemented primary opcode), `ppcldxabsent` (MED -- `ldx`/`ldux`/`lwax`/`lwaux` have no `PPC_31_*`
define and reach opcode 31's `default: goto bad` on every CPU while `stdx`/`stdux` are implemented: a legal 64-bit
guest load stops the cpu; witness shape: one stepped `ldx` word on HEAD PPC970), `ppc64on32gate` (design -- at least
fourteen 64-bit-only forms decode ungated on 32-bit CPUs (`cmpd`, `cmpld`, `ld`, `std`, `rfid`, `mtmsrd`, `ldarx`,
`stdcx.`, `stdx`, `stdux`, `extsw`, `sld`, ...; `extsw` counted although its MODE32 handler diagnoses and returns),
eleven more are absent on every width; the licensed fix is the `rld*`
idiom (PEM :6253 + the opcode-30 precedent) applied to the ungated implemented set in its own round), `wiringwitnessclass`
(LOW, records -- HEAD's wiring MANIFEST classes post-fix-green frozen witness copies CLASS_WITNESS against the checker's own
WITNESS/DETECTOR line; found by the final exact-text clearance).
The five filed ids have zero rows in the HEAD ledger and in the working-tree ledger (C0 part 4 for the first four; re-checked at landing). [2026-11-02, records: true only before filing -- this landing commit, cb21331c, added all five rows, so each has a ledger row at cb21331c and at 987cb596]

**Records.**  The ledger row's witness is `probe:regress/artifacts/ppcdsformxo/witness_20261024/ppc_dsform_probe.py`
(rung 3, the LOAD half; the store half's clause-(a) artifact is `table1_20261024/prefix_BASE.out`), state `held` (the Fable 5.1 review is owed under the owner's hold; its question is on the row),
commits named by the follow-up records commit, as every landing in this batch.  The brief's own defects are recorded in `PASS1_RULINGS.md` C8 (the session list omitted the negative
control; "every path exists at HEAD" was false for the untracked witness paths; P2 inverted; the `lwa size 3` gloss).
CRIT's `testppc` is `bareppc` (both PPC970; `bareppc` has no devices).  Pass-2 receipt: `regress/pass2_ledger.tsv`,
added by the follow-up records commit.

```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?

End with one line: `RECBLOCK_571: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC571: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
