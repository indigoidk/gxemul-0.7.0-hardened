# T2 (`ppcdsformxo`, round `#571`) PASS 2 -- the main loop's dispositions, by id (2026-10-24 10:0x-10:2x)

Pass-2 brief: `packet.md` (FULL 228,802 b; GPT-6 Astra + Grok 4.7), `packet_compact.md` (88,607 b; Gemini 4 Argon through
agy), `packet_packetfed.md` (74,373 b) split `packet_glm_Q12.md` / `packet_glm_Q34.md` (GLM 5.3, DeepSeek v4-pro).  Verdict
words: READY TO LAND | LAND WITH CHANGES | DO NOT LAND.  Dispositions are stated by id and answer-file:line; no reachability
paths and no variant edits are restated here (the measured records live in `../table1_20261024/`).

## SEATS -- seven answers from FIVE reviewing seats (Astra reviews this pass and then adjudicates it), every one verified by CONTENT

| seat | file | bytes | verdict | class | content check |
|---|---|---|---|---|---|
| GPT-6 Astra (gpt-6-astra / ultra, pointer form) | `codex_t2p2.txt` | 19,037 | LAND WITH CHANGES | file-reading | `cxlaunch_t2p2_stdout.txt`: rc 0, refusal 0, "ran: model: gpt-6-astra / reasoning effort: ultra"; answers Q1-Q4; opened the WT arm, `cpu_dyntrans.c`, PREDICTIONS, the leg logs |
| Grok 4.7 (xhigh, plan mode, WORKING tree) | `grok_t2p2.txt` | 18,986 | LAND WITH CHANGES | file-reading | exit 0; answers Q1-Q4; opened the arm, `opcodes_ppc.h`, `tmp_ppc_loadstore.c`, `lib.sh`, five leg logs, `extsw`, `cmpd` |
| Gemini 4 Argon through agy (gemini-4-argon-high) | `argon_agy_t2p2.txt` | 58,734 | LAND WITH CHANGES | file-reading (agy `--add-dir`) | exit 0, empty .err, no cross-seat text.  **Q1 verifiable and right (its line numbers match the WT).  Q2(a), Q2(b) and Q3(f) are CONFABULATED** -- see F25 |
| GLM 5.3, Q1-Q2 firing | `ollama_glm_t2p2_Q12.txt` | 13,207 | LAND WITH CHANGES | packet-fed | Q1(a-e), Q2(a-e) only; every claim labelled READ / REASONED / NOT CHECKABLE; re-derived every leg's red set |
| GLM 5.3, Q3-Q4 firing | `ollama_glm_t2p2_Q34.txt` | 14,642 | LAND WITH CHANGES | packet-fed | Q3(a-g), Q4 only; same labelling; found five PRETABLE omissions nobody else did (F7) |
| DeepSeek v4-pro, Q1-Q2 firing | `ollama_deepseek_t2p2_Q12.txt` | 6,609 | LAND WITH CHANGES | packet-fed | Q1(a-e), Q2(a-e) only; no echo, no thinking burn |
| DeepSeek v4-pro, Q3-Q4 firing | `ollama_deepseek_t2p2_Q34.txt` | 5,778 | LAND WITH CHANGES | packet-fed | Q3(a-g), Q4 only; no echo, no thinking burn |
| Fable 5.1 | `fable5.HELD.txt` | -- | HELD by the owner | -- | the hold question is on the row |
| kimi, minimax, Opus-as-seat | `roster_NOT_FIRED.txt` | -- | DELIBERATELY NOT FIRED | -- | by the owner's 2026-10-23/24 roster; not failures, not agreement |

**Seven of seven answers: LAND WITH CHANGES.  No seat found a product-code defect; every change is to records, comments or
the detector's docstring.**  The count is not the evidence -- the arguments are checked below, and one seat's Q2 is rejected.

## MAIN-LOOP CHECKS (measured by reading before any ruling; each names what it settles)

* **M1** `wc -l regress/ppc_dsform_probe.py` = 836 at md5 `0266228894811ba6c51cff82585753c9` (K5); the drafts said 834.
* **M2** `PASS1_RULINGS.md` section F lists ELEVEN amended dispositions in F1 (A3, A6, A9/B9, B2, B7, B10, B11/B13, B12, C4,
  Q3, Q5); `BUILD_SPEC.md` section 10 packages them as eight builder items (K11).
* **M3** `grep -n 'ra == 0 && update' src/cpus/cpu_ppc_instr.c` (WT = the committed numbering) -> :4367 (K8).
* **M4** `BUILD_SPEC.md:179-180` (no boot A/B owed: no PowerPC guest image boots through opcodes 58/62) and `:233-234` (the
  "at least fourteen" census notes `extsw`'s MODE32 handler diagnoses and returns) (K12).
* **M5** The leg drivers existed only in the session scratchpad (`s6_leg.run-083428.sh`, `legs571.run-083428.py`); SCORES.txt
  names the stamp `083332` (K4).  `s6_all.out:1-2` names `083428` and pins `legs571.run-083428.py` at md5 `5371d362`.
* **M6** `gate_ppc.sh:103 need_exec "$PMAX"` SKIPs gate 13 before the `#571` block on an absent binary (K3).
* **M7** PRETABLE.out :56 `ldu value`, :58 `ldu ds0 value`, :61 `lwa ds0 value` name no L4b though `L4b_case58HEAD.out`'s RED
  line holds all three; :74 `stdu ds0 value`, :75 `stdu alias val` name no L4c though `L4c_case62HEAD.out` reds both; the
  siblings :59 `lwa value` and :71 `stdu value` do name L4b / L4c.  GLM Q34's five omissions CONFIRMED.
* **M8** The probe docstring :66-67 carries the `-T` (`halt_on_nonexistant_memaccess`) failing-access sentence (C5).
* **M9** The gate-13 `gate_begin` title string is printed by `lib.sh:73-77` and pinned by no script (grep of regress/ and
  tools/ for the title text: only `gate_ppc.sh:98`).
* **M10** `L10_updall.out:40` loads session `pc=0x10060 todo_ra0=1` with BOTH `ld ra0` and `lwa ra0` unwritten (:28-29);
  `L9a_xo0asxo1.out:40` `pc=0x10064` with `lwa ra0` READ (:29) and `ld ra0` unwritten (:28); both store sessions stop at
  `pc=0x100c0` (`std ra0`).  The probe places `lwa ra0` before `ld ra0` (:350-351).  So L10's loads session stopped at the
  `lwa` word (XO 2), L9a's at the `ld` word (XO 0): Astra's correction of the drafts' "an RA = 0 XO-0 word" is RIGHT; SCORES.txt's
  own wording ("the RA = 0 words now REFUSE") is right as it stands.
* **M11** Argon's Q2(a)/(b) row and leg names -- `stdu rars`, `std low4`, `lwa pos value`, `ldu neg val`, `stdu window`,
  `xo58_3 stop`, `L6c`, `L11a`, the values `0x3028` and `0x1122334455667788`, "L1 BASE 11/39", "unasm census ... 78" -- occur
  ZERO times in `regress/ppc_dsform_probe.py`, in `pass1_20261024/BUILD_SPEC.md`, in the pass-1 brief and in the pass-2
  compact packet it was given.  Its K14 claim ("the stores session still runs `examine 0x0 0x20`", probe :517) is false:
  the probe contains no `examine` command at all (it uses `dump`).
* **M12** The ledger's `sev` vocabulary has no `design`; one row (`cpusexitsweep`) carries `RESEARCH`.

## K -- the drafter's seventeen inconsistencies: disposition and landing spot

| K | what | seats | disposition |
|---|---|---|---|
| K1 | probe `row()` comment "14, not 15 ... misses the pin" FALSE: a 15-character name gets two spaces (16 misses) | all seven agree it is false; Astra, Grok: correct the comment; GLM Q34: erratum, "the panel should choose explicitly"; DeepSeek, Argon: L4 on the CHANGELOG | **D1 -> EDIT** (below) |
| K2 | session count: the gate comment reads as nine; CHANGELOG "EIGHT ... on bareppc" | all | L4: gate comment edited (comment-only, `gate_fix.diff`); drafts corrected |
| K3 | SCORES L5b "the gate's sentinel pin reds" | DeepSeek, GLM, Astra, Grok, Argon | L4: dated correction block in SCORES.txt (M6); clause (c) stays on L5 |
| K4 | driver names `083332`; drivers not beside the table | DeepSeek, GLM (L3 relocate), Astra (L1), Grok, Argon | preserved as `table1_20261024/drivers/*.txt` + `MANIFEST.md5` (10:1x); SCORES correction block |
| K5 | 834 vs 836 lines | all | L4: drafts corrected; BUILD_REPORT addendum.  After D1 the shipped file is 845 lines -- the records state the MEASURED instrument (836 / `0266228`) and the SHIPPED one (845 / `59e83491`) side by side |
| K6 | PRETABLE CHANNEL for `lwa ra0 value` names L9b | all; GLM +5 omissions (F7); Astra +2 channel claims (F7) | L4 by carried erratum (SCORES/BUILD_REPORT); PRETABLE unedited (its mtime is the order proof) |
| K7 | the STD case comment's terseness about the `stdu` RA = 0 stop | Grok (L4, add); DeepSeek; Astra (L1); GLM, Argon (accurate) | D2: no product edit |
| K8 | CHANGELOG `:4338-4342` -> `:4367-4371` | all | L4: corrected (M3) |
| K9 | "three harness files" | all | L4: "four", `precommit_check.sh` bullet added |
| K10 | "std at DS = 0 and RA = 0" reads as the NOT CLAIMED joint | all | L4: two words named |
| K11 | "eight amendments" | all | L4: eleven dispositions / eight spec items (M2) |
| K12 | BUILD_REPORT lacks the fourteen/`extsw` and no-boot sentences; OB C4 wording | all; GLM: the "its own round" sentence is NOT against F1; Grok, Astra: it pre-authorises | L4: BUILD_REPORT addendum; OB reworded "does not pre-authorise a uniform sweep" (keeps "its own round") |
| K13 | times (PRETABLE "~08:0x" vs 07:56:54; gate end 09:05:23; PREDICTIONS 08:32:01) | all | L4: BUILD_REPORT addendum with the mtimes; PRETABLE by erratum |
| K14 | PRETABLE section 4's 0x0 window | Astra, Grok (no stores row uses it; the stop sessions keep their own zero windows) | L4 erratum; Argon's `examine 0x0` claim REJECTED (M11) |
| N14 | DRAFTER_INPUTS line numbers | -- | scratchpad input only |
| N15 | DRAFTER_INPUTS "HEAD 87a766e0" | -- | scratchpad input only |
| N16 | launcher verdict vocabulary | -- | fixed before firing |
| N17 | roster record says Astra adjudicates only | -- | `roster_NOT_FIRED.txt` wording -> "reviews this pass, then adjudicates" |

## FINDINGS F1..F28 (attributed; disposition = ACCEPTED / REJECTED / REFINED, and what changed)

* **F1** (all seven) The product diff is exactly A1-A4 as amended: both case bodies mask locally, the ten table indices are
  15/31, 47/63, 10/26, 7/23, 39/55, none reaches 11/27/43/59, both `goto bad`s land on the common tail, nothing written before
  the jump outlives it, two `#571` tags.  ACCEPTED; no product-code change.
* **F2** (Astra Q3 K1; Grok Q3(a); DeepSeek Q34 :12; GLM Q34 :18; Argon Q3(a)) K1 -- the probe comment's reason is false.
  **D1** below.  APPLIED 10:11 as a docstring/comment-only edit (`probe_docfix.diff`).
* **F3** (all) K2 -- ACCEPTED; gate comment edited; drafts corrected.
* **F4** (DeepSeek Q34 :65; GLM Q34 :33; Astra Q2 K3; Grok Q2(d); Argon Q2) K3 -- ACCEPTED (M6); SCORES correction block.
* **F5** (DeepSeek Q34 :42; GLM Q34 :42; Astra Q3(g); Grok Q3(g); Argon Q3(g)) K4 -- ACCEPTED (M5); drivers preserved.
* **F6** (all) K5 -- ACCEPTED (M1).
* **F7** (GLM Q34 :48: five PRETABLE channel omissions; Astra Q2(c): `lwz value` is not green under every leg -- L8c removes its
  readback; `unasm census` is not emitted red under L5b -- the exception precedes every row) -- ACCEPTED (M7): all seven
  channel corrections go into ONE carried erratum (SCORES.txt + BUILD_REPORT.md); PRETABLE's per-row "kills" lists are
  recorded as pre-table PREDICTIONS of channel, incomplete, never the kill map (the kill map is SCORES's RED column).
* **F8** (all) K8 -- ACCEPTED (M3).
* **F9** (all) K9 -- ACCEPTED.
* **F10** (all) K10 -- ACCEPTED.
* **F11** (all) K11 -- ACCEPTED (M2).
* **F12** (all) K12 -- ACCEPTED (M4); the OB sentence: REFINED per GLM (deferring the sweep is not pre-authorising it) while
  adding the explicit "does not pre-authorise" clause Grok and Astra wanted.
* **F13** (DeepSeek, GLM, Astra, Grok, Argon) K13 -- ACCEPTED: BUILD_REPORT states the mtimes; PRETABLE by erratum.
* **F14** (Astra Q4; Grok Q3(g)) K14 -- ACCEPTED as erratum; Argon's variant REJECTED (M11).
* **F15** (DeepSeek Q34 :18; GLM Q34 :24, L3; Grok Q3(b), L4; Argon Q3(b); Astra Q3(b): `PASS1_RULINGS.md:239` and BUILD_SPEC
  already name "HEAD plus two keys") The landing copy of `check_probe_wiring.py` must be named in a shipped record.
  ACCEPTED/REFINED: the commit message names the staged HEAD-blob copy (10:0x); the CHANGELOG's wiring-checker bullet
  carries the provenance since the final clearance (it did not before -- Astra, adj/final); the landing script stages
  `staged/check_probe_wiring.py.txt` and nothing else of that file.
* **F16** (DeepSeek Q34 :14; GLM Q34 :22; Grok Q3(a) L4; Astra L1; Argon: not required) The gate-13 title -- ACCEPTED: the
  string is unpinned (M9); ` + #571 DS-form` appended (`gate_fix.diff`).
* **F17** (Astra Q2(b) "additional L4 correction": the drafts' explanation of the L9a/L10 misses -- "an RA = 0 XO-0 word" -- is
  false for L10, whose loads session stops at the RA-zero `lwa` (XO 2); GLM Q12 :29 and Grok Q2(b) derive the same PCs)
  ACCEPTED (M10): SCORES.txt's per-leg lines (:21, :23) stand; its SUMMARY line (:29) carries the same XO-0 wording and is
  corrected by SCORES's addendum item 3; the CHANGELOG and commit drafts are reworded.
* **F18** (Grok Q1(c): add the `stdu` RA = 0 clause to the STD comment, L4; DeepSeek Q12 :29: a record improvement; Astra Q1(c):
  optional L1 clarity; GLM Q12 :19: accurate as written, no licence; Argon Q1(c): no product edit) **D2** below.
* **F19** (Astra Q4: RT = EA holds only on a successful access [Grok Q2(e) too]; "ld/lwa/std leave RA alone" needs the RT = RA
  qualification; only `stdu neigh` grades flanks; GLM Q12 Q2(e): the sign-of-DS x RA joints and the reserved corners are
  mentioned nowhere -- "one contract sentence owed"; Astra Q2(e): "no dedicated sign/alias-refinement bullet", FILE under
  R7/R7b) ACCEPTED: all four folded into the docstring/comment-only repair (`probe_docfix.diff`: the CLAIMED sentence, NOT CLAIMED
  bullet 1, and one new NOT CLAIMED bullet naming the sign x RA joints and the reserved corners as non-floor, not rowed).
  **F2 (both adjudicators) REFINED the new bullet's WARRANT**: "the case bodies read neither the sign of DS nor RA" was false
  -- the mask copies the DS sign bit into `imm`; what the bodies lack is a BRANCH on it, and they do not read `ra`.  Replaced
  in a SECOND docstring-only revision (`repair_p2/probe_docfix2.diff`, md5 3efd8cbec746b8224c32d6827b42db46, 847 lines), which also discloses Astra's F26
  cells (`stdu` with RA = RS at DS = 0; the reserved encodings at a positive DS); re-measured as prefix_BASE3 / fixed3 / gate13c.
* **F20** (Astra Q1(d) DERIVED) The drafts' "decoded unchanged" shorthand for 32-bit CPUs is inaccurate: the arm persists but
  its MODE32 decode and refusal behaviour change.  ACCEPTED: CHANGELOG and OB drafts reworded.
* **F21** (Astra Q4 B1/F1) The CHANGELOG's universal "each source eight distinct bytes" is false for the alias store (its source
  is its old base).  ACCEPTED: drafts qualified (the probe docstring :33-34 already carries the exception).
* **F22** (Astra Q4 C4: "LOW was not established by the design-only ruling"; Grok Q4: "the ruling is design, without LOW")
  REFINED: the ledger row's `sev` becomes `RESEARCH` (the vocabulary's existing value for a design row, M12) and the OB
  entry reads "(design, open)"; the commit message's "LOW, design" becomes "design".  **F2: Astra UPHELD RESEARCH; Grok
  OVERTURNED it** -- the ledger's one RESEARCH row (`cpusexitsweep`) was relabelled because a census with no witness is not a
  defect severity, this row's census is done and what is open is a future fix, and the ledger allows an unset severity.
  **RULED FOR GROK** (M13: 244 rows carry no `sev` key and five carry `null`; the precedent's own state_note says what Grok
  read): the row lands with NO severity; the OB entry reads "(design, open; no severity assigned)".
* **F23** (GLM Q34 :28) C5 not checkable from the packet -- SETTLED by M8: the contract carries the `-T` sentence.
* **F24** (GLM Q34 :40, :38) witness term "16 of 16 legs red" drops L5b; CHANGELOG "HEAD c8fcb5ff's source" misnames HEAD --
  ACCEPTED, both reworded.
* **F25** (main loop, M11) **Argon's Q2(a), Q2(b) and Q3(f) describe an instrument that does not exist**: row names, leg names,
  seed values and scores found nowhere in the round's files, stated with file links and line numbers.  Its Q1 (line numbers
  that match the WT) and its K1/K2/K4/K13/K12 agreements are consistent with the file-verified seats and are counted only as
  such.  DISPOSITION: a SEAT DEFECT -- CONFABULATED INSTRUMENT -- recorded on the row's agy entry; no finding is credited to
  Argon alone this pass; its agreement adds no weight (owner 2026-10-02 on agy's agreement, applied to the transport).  Not the
  carrier's "read another copy" class: no copy anywhere carries those names.  **F2 (Astra) EXTENDS the rejected scope:** Argon
  also fabricates material in Q2(c), Q2(d), Q2(e), Q3(d) and Q3(e); its coverage agreement is removed from F26's attribution.
  Grok adds the invented `lwa neg value`, the score "11/39", a fake freeze md5 and the `examine` command; "that wider set
  does not change the credit decision".
* **F26** (the four Q2(e) readings -- Astra, Grok, GLM Q1-2, DeepSeek Q1-2 -- plus GLM's and DeepSeek's Q3(d) on the contract; Argon excluded under F25) The ask-again in coverage form: every enumerated cell is rowed or disclosed; the unobserved cells are
  the disclosed joints, RA = RT, the positive-word `lwa`, 32-bit, translation on / indexed / failing access / disassembler,
  plus the sign x RA samples and reserved corners now disclosed by F19.  No seat names a floor cell with neither a row nor a
  bullet; no L2.  ACCEPTED: no new row.  **F2 (Astra) REFINES: "every enumerated cell is rowed or disclosed" was FALSE at pass 2
  -- `stdu` with RA = RS at DS = 0, and the reserved encodings at a positive DS (the rows use DS = -0x10 / -0x30), were
  neither rowed nor mentioned.  Both are disclosed by the second docstring revision as remaining non-floor coverage debt;
  the no-new-row conclusion stands.**
* **F27** (Astra Q3 K2) `DETECTOR_FREEZE.txt`'s header says all eight sessions use `bareppc`; item 8 is `nosuchmachine`.
  ACCEPTED: the FREEZE addendum corrects it.
* **F28** (Grok Q2(c), Astra Q2(c), Argon Q2(c)) K6's correction already sits in DETECTOR_FREEZE and in L9b's RED line; one
  sentence in BUILD_REPORT makes it discoverable.  ACCEPTED (part of F7's erratum).

## DISPUTES D1..D2 (both sides in their own words; the ruling and its warrant)

* **D1 -- K1: edit the probe's false comment (re-freeze) or carry an erratum?**
  GLM Q34 :18: "any edit re-freezes the instrument and falsifies the 'measured by the FROZEN detector md5 0266228...' citations
  in DETECTOR_FREEZE, the SCORES header and the MANIFEST key ... re-freezing and re-measuring 17 legs to delete one comment is
  disproportionate -- but the panel should choose explicitly, because shipping a knowingly false sentence in the frozen
  instrument is also against the round's discipline."
  Grok Q3(a): "Correct the comment and do not repeat the mechanism in the CHANGELOG.  A comment edit changes md5 02662288...;
  BUILD_SPEC section 10 item 5 then re-runs the pre-fix and post-fix detector.  Exhibit the comment-only diff.  The sixteen
  legs stay the record of the behaviour."  Astra Q3 K1: "Correct the probe comment and the CHANGELOG's credit".
  **RULING: EDIT, in the form Grok names.**  Warrant: the carrier's L4 -- a wrong record is corrected IN PLACE, and a shipped
  comment is a record; the cost objection is answered by the DIFF being docstring/comment-only (verified mechanically by
  stripping the docstring and comments from both revisions and comparing the remainder: identical), so the sixteen legs'
  scores remain the record of the behaviour and only clause (a) and the post-fix run are re-measured on the shipped md5.
  The MANIFEST key carries no md5 (checked), so it needs no edit.  The seat's cost argument is recorded, and the owed
  re-measure is `prefix_BASE2.out`, `fixed2.out` and `gate13b_20261024.out` (ran 10:15-10:16: 22/39 with the identical RED
  line; 39/39; PASS 193 -- the ruling's measured condition is MET).  Applied 10:11:
  `probe_docfix.diff` -- md5 `0266228894811ba6c51cff82585753c9` (836 lines, 40,883 b) -> `59e83491a5819a599c610b1aa8e8b847`
  (845 lines, 41,610 b); the frozen revision is kept at `../table1_20261024/` (BASELINE.out, DETECTOR_FREEZE.txt) and the
  CHANGELOG states both revisions.
* **D2 -- K7: must the STD case's product comment state the `stdu` RA = 0 stop?**
  Grok Q1(c): "It does not state that `stdu` with RA=0 now stops.  The code does stop it (`update = 1`, then the same guard).
  Add that clause.  Licence L4 (site comment)."  DeepSeek Q12 :29: "a record improvement (L4)".
  Astra Q1(c): "The store comment's cross-reference is sufficient; explicitly mentioning `stdu`'s RA-zero refusal would be
  optional L1 clarity."  GLM Q12 :19: "Accurate as written; optionally tighten; no R-L licence (no false statement)."  Argon
  Q1(c): "`K7` requires no product edit."
  **RULING: NO product edit.**  Warrant: L4 is the licence for a WRONG record, and no seat says the comment is wrong -- it reads
  "as for PPC_HI6_LD above", and the LD comment it incorporates states the RA = 0 guard; `case 1: update = 1` sits three lines
  below; the contract's BEHAVIOUR CHANGES and the CHANGELOG name both stops.  The product-file cost is real: a comment edit
  to `cpu_ppc_instr.c` re-opens est/ propagation, three build-tree rebuilds and the two-part clearance for a derivable
  sentence.  Grok's dissent is carried here verbatim; **F2 question.**

## OWED, AND WHERE I MIGHT BE FOOLING MYSELF

* The re-measure of the revised detector (`prefix_BASE2.out` on the BASE binary 3cd0501c; `fixed2.out` on build/gxemul a142d92a;
  gate 13 alone) ran 10:15-10:16 and read 22/39 PRESENT 17/17 with the identical RED line, 39/39 ABSENT, PASS 193 with the
  `#571` block all ok -- D1's measured condition is met (`../table1_20261024/repair_p2/remeasure.out`).
* The DETECTOR_FREEZE / SCORES / BUILD_REPORT addenda (F4, F5, F7, F13, F14, F27, the revision note) were written at 10:2x, each
  a dated block quoting what it corrects; PRETABLE.out and PREDICTIONS.txt are never edited.  The adjudication packet's
  "five hunks" for the probe diff is wrong: it has THREE hunks (five wording changes); Astra counted them.

## F2 -- THE ADJUDICATION (added 10:4x)

**F2 -- GPT-6 Astra, `adj/codex_t2p2adj.txt` (10:29, gpt-6-astra / ultra, refusal 0): `VERDICT: AMEND -- The decoder and
measured regression floor stand, but four accepted dispositions leave incomplete record repairs.`**  UPHELD: F1-F18, F22, F23,
F27, F28, D1, D2 ("the STD comment's cross-reference is accurate; the omitted explicit clause does not require another
product edit"; RESEARCH "avoids inventing an established severity").  REFINED, all applied: **F19** -- propagate "performs no
base update" (not "leaves RA alone") and the successful-access condition into the landing drafts; describe the sign argument
as the absence of a distinguishing TEST, not of reading the displacement bits (the bodies do read them) -> the second
docstring revision; **F20/F21** -- extend the carried erratum to PRETABLE.out:31 ("32-bit CPUs decode unchanged") and :66
("sources = 8 distinct bytes", unconditional) -> SCORES addendum 2; **F25** -- Argon's fabrication extends to Q2(c)-(e), Q3(d),
Q3(e); **F26** -- two non-floor classes were neither rowed nor disclosed -> disclosed by the second revision.  Two records
defects of the repair itself: DETECTOR_FREEZE's addendum sentence "Every run in this directory before this addendum" wrongly
covers the three revised runs (prefix_BASE2 / fixed2 / gate13b preceded the addendum too) -> corrected by a further item;
the roster is "seven answers from FIVE reviewing seats" -> corrected above.  CHAIN: "This pass closes the existing floor-bound
repair chain with zero floor breaches" -- denominator: the probe diff's three hunks (five wording changes), the gate diff's two
hunks, the three re-measured runs, against the shipped composite and the existing floor enumeration; the docstring repair
"changes no score or decision-bearing observable consumed by the gate or kill table".  `LANDING: GO WITH THE CHANGES NAMED
ABOVE -- Complete and review the record corrections; no additional decoder change or regression row is justified.`  The
second docstring revision it caused is re-measured like the first (prefix_BASE3 / fixed3 / gate13c) before the landing, and
the final commit text goes back to Astra for the exact-text clearance it said it could not give unexhibited.

**F2 -- Grok 4.7, `adj/grok_t2p2adj.txt` (10:41, xhigh, plan mode, exit 0): `VERDICT: AMEND -- The product diff and the
detector's behaviour stand.  Two accepted repairs are wrong records: the new docstring warrant that the case bodies read
neither the sign of DS nor RA, and sev=RESEARCH on ppc64on32gate.`**  UPHELD: F1-F18, F21, F23, F26-F28, D1 ("the ruling in
this seat's favour ... the RED line of prefix_BASE2.out is byte-identical"), D2 ("the dissent ruled against this seat, and the
ruling is right").  REFINED: **F19** -- three of the four docstring edits match the code; the warrant is false ("`imm =
(int16_t)(iword & ~3)` copies the DS sign bit into `imm`.  The case bodies do not branch on that sign, and they do not read
`ra`") -> the second revision carries Grok's sentence; **F20** -- PRETABLE.out:31 must be quoted in the erratum (done, SCORES
addendum 2 item 7, written after Astra's answer); **F25** -- the fabricated set is wider (above).  **OVERTURNED: F22** (above;
ruled for Grok).  CHAIN: "The floor chain closes.  There is no clean-sweep mutant, no vacuous row, and no non-varying channel.
The denominator is probe_docfix.diff (three hunks, five logical edits), gate_fix.diff (two hunks), and the three re-measured
runs"; "The records do not close until the false warrant is replaced.  That replacement is one sentence.  It does not reopen
the sixteen legs and does not owe a new kill table."  `LANDING: GO WITH THE CHANGES NAMED ABOVE -- ship the product diff and
the detector behaviour; replace the sign warrant, leave ppc64on32gate severity unset, and quote PRETABLE.out:31 in the
erratum before the commit is the landed record.`

**FINAL EXACT-TEXT CLEARANCES -- GPT-6 Astra, `adj/final/codex_t2final.txt` (10:47-11:0x) and `codex_t2final2.txt`
(11:1x-11:3x), both `VERDICT: GO WITH THE EDITS BELOW` / `LANDING: HOLD`; a third reading follows the corrections below.**
READING 1 named twelve wrong records.  Ten were completed by the second reading: the probe's parenthesis "the common tail
tests only imm == 0 and ra == 0 && update" omitted the tail's `ra == 0` zero-base selection -> a THIRD docstring-only revision
(`repair_p2/probe_docfix3.diff`, one line; md5 `e0a1e67eb0283abccde3bbd53952487a`, 848 lines), re-measured as prefix_BASE_r3 /
fixed_r3 / gate13r3; the state-note prefix named revision 1 -> it names the shipped md5 and three revisions; the pass-1 grok
adjudication note repeated the false 15-character rationale -> corrected; the codex pass-2 note's "no base update with the RT =
RA case" -> "ld/lwa/std perform no base update; an aliasing load still changes RA through its destination write"; the design
row's "licensed fix shape ... applied uniformly" -> "a prospective design for its own round ... does not pre-authorise a uniform
sweep"; "twenty-eight findings, every one a ... defect" -> "twenty-eight numbered findings whose required changes concern
records, comments and contract wording"; F26's "(all seven)" -> the readings that answered Q2(e), Argon's excluded; F15's
"the CHANGELOG bullet says the same" was false -> the bullet now carries the provenance; DETECTOR_FREEZE item 4 listed
`fixed_witness8.out` among the detector runs -> item 6 separates it (it ran the WITNESS, md5 5e96b69d); BUILD_REPORT addendum
2's "both adjudicators ... six re-measured runs" overstated their scope -> addendum 3 records revisions 2 and 3 separately.
ONE WAS LEFT INCOMPLETE ("four reviewing seats" survived in two ledger-ops sentences) and ONE WAS WRONGLY REJECTED by the main
loop: the frozen witness copy's MANIFEST class.  The rejection rested on precedent -- HEAD's MANIFEST classes an earlier round's
frozen rung-3 witness (m88kbuserrregs) and #539's post-fix-green witness as CLASS_WITNESS; vmedefaultkill's two were cited
too, WRONGLY (its sites probe reports outcomes without grading the defect; its free-run companion asserts the pre-fix symptom
-- reading 3) -- and on the claim that the checker gives WITNESS no definition beyond its name.  **That claim was false**: `check_probe_wiring.py:55-57` defines the line -- "A DETECTOR
asserts the REPAIRED property: it is GREEN once the defect is gone.  A WITNESS asserts the PRE-FIX SYMPTOM: it is RED once the
defect is gone."  The frozen copy asserts the repaired property (5/8 on HEAD, 8/8 post-fix), so it is a preserved instrument:
CLASS_RESEARCH (#471), as Astra ruled twice.  The precedents conflict with the definition and do not amend it; they are FILED
as `wiringwitnessclass` (LOW, records).  READING 2 (11:1x-11:3x) named ten records: the two "four reviewing seats" sentences; "Seven seats agreeing" above; F26's
attribution (four Q2(e) readings plus the two Q3-4 firings' Q3(d)); this file's K-table skipped the brief's K7 and shifted
K7-K13 by one (restored; the NOTES-only items are N14-N17); the witness class and this paragraph's account of it; "three
docstring-only revisions" -> docstring/comment-only (revision 1 also changed a comment outside the docstring); the CHANGELOG's
"no PowerPC guest image boots in this tree" -> "no PowerPC guest image in this tree's battery boots through opcodes 58/62";
and "eleven applied" -> the true count.  NINE were applied at 11:4x; the last was NOT: the stale "eleven applied" survived in
the commit message, the CHANGELOG block and a ledger note, and the ledger's state-note prefix still omitted the final-clearance
occasion.  READING 3 (11:4x-12:0x, `codex_t2final3.txt`) named seven: those two; BUILD_REPORT addendum 3's "Eleven applied, one
rejected" (corrected by addendum 4, which carries the CLASS_RESEARCH reversal and the filing); the ledger prefix's "four rows
filed" -> five; a DeepSeek note's "F6/K4" -> F5/K4; vmedefaultkill wrongly grouped among the post-fix-green witnesses (removed
from the new row, the OB bullet, the CHANGELOG and this paragraph); "docstring-only repair" at F19 -> docstring/comment-only;
and reading 2's "ALL APPLIED" claim, premature.  All seven applied (12:0x); the corrected texts went back to Astra for a fourth
reading, and the reading that says GO is the clearance the commit rests on.  F22: unset severity confirmed at every reading.

**THE ONE ADJUDICATOR DISAGREEMENT -- F22 (the design row's severity): Astra UPHOLD RESEARCH, Grok OVERTURN to unset.**  Ruled
for Grok on the measured precedent (M13).  Everything else the two adjudicators agree on, including the chain's closure and the
two-sided "GO WITH THE CHANGES NAMED".  Both lists of changes are applied; the second docstring revision is re-measured before
the landing, and the final commit text goes to Astra for the exact-text clearance.

* **M13** `tools/pipeline/ledger.json`: 1,079 rows; 244 have no `sev` key, 5 have `sev: null`; `cpusexitsweep` is the only
  `RESEARCH` and its state_note describes a census ("src/cpus/ holds 111 exit( across 23 files ... THE COUNT IS AN UPPER BOUND").
* A repair made in response to a pass 2 owes its own pass 2 (carrier): the F2 adjudication packet inlines BOTH repair diffs
  (`probe_docfix.diff`, `gate_fix.diff`) and asks the adjudicators whether the chain closes -- zero floor breaches, with the
  denominator being those two diffs and the three re-measured runs.
* Seven answers from five reviewing seats agreeing on the records defects is not evidence of the records' completeness: the drafter found seventeen, the
  seats added eleven more (F7, F15-F22, F24, F27) -- a correction is not safer than the thing it corrects, so the landing
  drafts get one more read against the files before the commit (the carrier's second-review-pass rule).
* Argon (F25): a confident, detailed, wrong description that passes every size check and reads like a reading.  The owner's
  roster keeps the seat; this record keeps its answer as a reading of Q1 only.
