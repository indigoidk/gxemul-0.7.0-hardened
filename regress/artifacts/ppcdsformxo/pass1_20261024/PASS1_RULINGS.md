# T2 (`ppcdsformxo`, round `#571`) PASS 1 -- the main loop's dispositions, by id (2026-10-24 07:3x)

Basis: SEVEN answers from FOUR reviewing seats, all verified by CONTENT (verdict line first, substantive bodies, no
cross-seat text in Argon's; `argon_transport_20261024.txt` carries the reading-scope caveat): GPT-6 Astra
(`codex_t2p1.txt`, READY WITH CHANGES), Grok 4.7 (`grok_t2p1.txt`, READY WITH CHANGES), Gemini 4 Argon through agy
(`argon_agy_t2p1.txt`, READY WITH CHANGES), GLM 5.3 (`ollama_glm_t2p1_Q12.txt` / `_Q34.txt`, READY WITH CHANGES x2),
DeepSeek v4-pro (`ollama_deepseek_t2p1_Q12.txt` / `_Q34.txt`, NOT READY x2 -- on the 32-bit width test and on the store
rows being unspecified).  Fable 5.1 HELD (`fable5.HELD.txt`); kimi / minimax / Opus-as-seat DELIBERATELY NOT FIRED
(`roster_NOT_FIRED.txt`).  The brief the seats answered: `packet.md` (Astra, Grok), `packet_compact.md` (Argon),
`packet_packetfed.md` split Q12/Q34 (GLM, DeepSeek).  Line numbers are HEAD `add098b9`.

## MAIN-LOOP CHECKS (measured by reading before any ruling below; each names what it settles)

* **M1 `bad:` prints under single-step.**  `src/cpus/cpu_dyntrans.c:2004-2014`: `debugmsg_cpu(..., VERBOSITY_ERROR,
  "UNIMPLEMENTED instruction at 0x...")` is unconditional; only `DISASSEMBLE` is skipped when `single_step ||
  instruction_trace` (:2011-2012); then `cpu->running = 0` (:2014).  Settles D2's channel question: a stepped stop
  session can key on the `UNIMPLEMENTED instruction` line without any added `fatal()`.
* **M2 the 32-bit table has real doubleword handlers.**  `src/cpus/tmp_ppc_loadstore.c:1923+`: slot 7 `ppc32_instr_std`,
  10 `ppc32_instr_lwa`, 11 `ppc32_instr_invalid`, 15 `ppc32_instr_ld`, 39 `ppc32_instr_stdu`, 47 `ppc32_instr_ldu`.
  Settles GLM-Q12's NOT CHECKABLE: a 32-bit CPU executing opcode 58/62 today does NOT exit the host.
* **M3 the Q4(2) family is unfiled.**  `grep -i -E 'lwax|ldux|lwaux|\bldx\b' OUTSTANDING_BUGS.md` = 0 hits; the same
  terms over all 1,079 ledger rows = 0 hits.  The disassembler's missing `LFDU/LFSU/STFDU/STFSU` cases are ALSO unfiled:
  the only ledger row naming `lfdu` is `ppclfsupreload` (the rounding probe's preload of f1), a different defect.
* **M4 the macppc image is present** (`_images/netbsd401-macppc-GENERIC`), so gate 13's rounding probe (the one other
  consumer of the edited arm) can be re-run here; gate 13's rldicl block ends at `regress/gate_ppc.sh:~201` and
  `need_file "$IMAGES/netbsd401-macppc-GENERIC"` follows it.
* **M5 the brief's P2 sentence is inverted** (Grok, Codex agree): the `ic->arg[2]` use of `imm` matters for EVERY
  XO != 0 word; the `imm == 0` table-index use is unobservable on PPC970 (both `_0` and non-`_0` handlers delegate to
  the one generic function, which adds `arg[2]`).  "The two uses matter only for DS = 0" is the wrong way round.

## A -- the repair (Q1)

* **A1 ACCEPT -- decode-only, five forms onto existing slots.**  Unanimous (5/5): `ld` 15/31, `ldu` 47/63, `lwa` 10/26
  (`size` 2, `zero` 0 -- the sign extension is the existing `(int32_t)` cast), `std` 7/23, `stdu` 39/55; none reaches
  `ppc_instr_invalid` (11/27/43/59 = `load && !zero && size == 3`); no handler edit.  P1 enumerated by four seats:
  `(int16_t)(iword & ~3)` == EXTS(DS || 0b00) in all twenty cells (the clear never touches bit 15).
* **A2 ACCEPT -- ONE masked `imm` feeds BOTH consumers.**  The repair re-assigns the shared `imm` INSIDE
  `case PPC_HI6_LD:` / `case PPC_HI6_STD:` of the inner switch, so the table index (:4335, `imm==0 ? 16 : 0`) and
  `ic->arg[2]` (:4351) both see the masked value (Argon, Codex, Grok, GLM, DeepSeek).  Grok's bound is recorded: a second
  variable read by only one of the two sites does not implement the design.  The record states this (M5).
* **A3 ACCEPT -- reserved XO (58/3, 62/2, 62/3): bare `default: goto bad;`, no own message, no latch.**  Argon censused
  every `goto bad` site in `X(to_be_translated)`: the pre-`goto bad` `fatal("TODO ...")` form (:4340 the RA = 0 update
  guard, :4604 the `rld*` width guard; *this line first also listed :4815 and :4997 from Argon's census -- Grok's
  adjudication found :4815 is the `break` after `tlbsync`'s `nop`, so the two unverified citations are withdrawn*)
  marks forms the tree knows and does not serve -- NOT only "valid-but-unimplemented features" (Astra's adjudication:
  the RA = 0 guard diagnoses an INVALID form, the `rld*` guard an ILLEGAL instruction; that characterisation is
  withdrawn); reserved/unrecognised encodings use the bare default (:4531, :4609, :5172, :5218, :5410, :5426).  Codex and GLM concur.  Grok and DeepSeek wanted a `fatal("TODO: ...")` line -- Grok's
  reason (the `bad:` disassembly is skipped under `step`) is TRUE and does not bear: the `UNIMPLEMENTED instruction`
  line itself prints under `step` (M1) and is the row's channel.  Option-set member: DECLINE with the common tail's own
  bounded announce (member 3; bounded by construction because the CPU stops on the first hit).  DeepSeek's "FAULT
  (member 5)" is a mislabel: nothing is delivered to the guest.
* **A4 ACCEPT -- RA = 0 update forms reach the EXISTING guard** (:4338-4342) once `update` is set: a BEHAVIOUR CHANGE
  (today: an absolute-address access at EXTS(DS || XO), no update; after: CPU stop), unanimous, consistent with every
  other update form in the arm, Book I's invalid-form rule allows it; rowed (B6) and CHANGELOG-disclosed as one of TWO
  behaviour changes (the other: reserved XO now stops).
* **A5 ACCEPT -- D1 `ldu` RA = RT stays "disclosed, not checked"** (unanimous; the contract states the post-repair
  result RT = EA; sibling update loads do not check it either).  `stdu` RA = RS is VALID and nothing in the design
  rejects it (the handler copies RS before `memory_rw` and writes RA after success).
* **A6 ACCEPT option (i) -- 32-bit CPUs: DISCLOSE, no width test this round.**  Grok, Argon, GLM against Codex and
  DeepSeek (option (ii), the `rld*` idiom).  Reasons: the witnessed defect is the XO fold on the 64-bit CPU; a width gate
  is a DIFFERENT claim (illegal opcode, not wrong form) with no witness and no row that is not a pin of illegal execution;
  R17 (one site; a second only if witnessed, same class, same detector) bars it; and the census both Codex and Argon
  supplied shows TWELVE ungated 64-bit-only forms in the same function (`cmpdi`/`cmpldi`, `ld`, `std`, `rfid`, `mtmsrd`,
  `ldarx`, `stdcx.`, `stdx`, `stdux`, `extsw`, `sld`) plus eleven absent ones (`tdi`, `td`, `ldx`, `ldux`, `lwax`, `lwaux`,
  `mulld`, `divd`, `srd`, `srad`, `cntlzd`), so gating 58/62 alone adds a THIRD policy to one function.  Option (ii) is the
  licensed FUTURE fix (transferred warrant: the `rld*` idiom + PEM :6253) and is FILED with the census (C4).  The
  contract must say: 58/62 are illegal on 32-bit implementations, are decoded and executed there before and after this
  fix (before: 8-byte `ld`/`std` with the fold; after: the five forms), no width test, no 32-bit session rowed.  M2
  records that none of this exits the host.  *This is dispute D1; Codex proposed (ii) and must be harder on it.*
* **A7 ACCEPT -- no alignment assumption** (unanimous).  Codex's qualification is adopted into the record: the brief's
  P8 wording "a base that is not a multiple of 8 gives an unaligned `ld`/`std`" is false as stated (base residue 4 plus
  displacement residue 4 is aligned); the witness itself measured successful unaligned 8-byte loads at 0x20021/0x2008a.
* **A8 ACCEPT -- the disassembler is FILED, not joined** (unanimous): guest-invisible (`running = 0` returns before the
  preview; the `running = 1` preview is a `NO_EXCEPTIONS` read), a different file, and joining it would re-pin the
  census oracle (R16 order obligation).  The detector's census keeps the CURRENT text (`ld`/`std` + raw halfword) and
  the contract says it attests opcode, RT/RS, RA and the raw low halfword, never the form (C1).
* **A9 ACCEPT -- records the repair carries**: CHANGELOG round block naming the DS correction and the TWO behaviour
  changes (A4, A3); `/* #571: */` at each edited line (the mask line and the two case lines); the ledger `witness`
  term (B12); the MODE32 twin's status stated beside the (e) disclosure (GLM: the same edit recompiles into the
  32-bit decoder and selects from `ppc32_loadstore`, M2); the contract (B11).

## B -- the detector (Q2, Q3)

* **B1 ACCEPT -- clause (a) for the STORE half is a SEPARATE pre-fix artifact**: the grown detector runs on the BASE
  binary (`/tmp/gxt2/base/gxemul`, HEAD c8fcb5ff source, md5 3cd0501c) BEFORE the C edit, preserved as
  `prefix_BASE.out` beside `prefix_HEAD.out`'s shape from `#570`; the frozen loads-only witness attests the load half
  only (GLM-Q34, Grok).  Store anchor = the debugger's `dump` over a byte-resolved, pattern-pre-seeded window
  (EA-1 .. EA+11, so an 8-byte store at EA+1/+2/+3 reds the flank and the body), 8 DISTINCT source bytes not occurring
  in the pattern; a `lwz` (D & 3 == 0) reload may corroborate but is not the anchor (Codex, Grok, Argon, GLM against
  DeepSeek's reload-by-`ld`, rejected: another DS-form load is a second observation from the decoder under change).
* **B2 ACCEPT -- graded RA rows for the XO-0 controls and `lwa`**: `ld RA after`, `lwa RA after`, `std RA after`
  (DS != 0) promoted from the witness's ungraded `obs()` lines (GLM D-A, Codex, Argon, Grok): they kill the
  update-everything and XO-0-plus-one growth variants, which the value rows cannot see.
* **B3 ACCEPT -- every RA-channel row uses DS != 0** (GLM D-D, gate 13's own header trap): `ldu RA after`,
  `stdu RA after`, the three B2 rows, `stdu alias RA` if shipped.
* **B4 ACCEPT -- DS = 0 value rows ARE shipped** (`ldu ds0 value`, `lwa ds0 value`, `stdu ds0 value`; value/destination
  channel only): the body tests `imm == 0` and the repair flips that slot there; on BASE they red through the value
  channel (RA + 1 / RA + 2).  Codex, Argon, DeepSeek FLOOR; GLM "ship them"; Grok (e).  One instruction each in an
  existing session.  *Dispute D4.*
* **B5 ACCEPT -- C9 (positive-word `lwa`) is (e), NOT rowed**: the extension is the callee's `(int32_t)` cast, outside
  the DEPENDS-ON bound; C8's negative word separates sign- from zero-extension and width on one row (Codex, Grok, GLM,
  DeepSeek against Argon).  **C18 (`stdu` RA = RS) is (e) by the rule and SHIPPED BY CHOICE** (`stdu alias val`,
  `stdu alias RA`, DS != 0): `stdu r1,-N(r1)` is the form every guest's stack push uses, so the row is the boot-path
  proxy; Codex "retain", Grok "ship if budget allows", GLM "free row", Argon FLOOR, DeepSeek (e).  *Dispute D5.*
* **B6 ACCEPT -- stop sessions**: 58/3, 62/2, 62/3 (each `li` liveness then the word LAST, own session; channels: the
  `UNIMPLEMENTED instruction` line (M1), RT sentinel intact / RA unchanged, the memory window unchanged for the stores),
  and the RA = 0 update words `ldu r,DS(0)` / `stdu r,DS(0)` at BOTH DS != 0 and DS = 0 (Codex: the DS = 0 refusal cell
  is the only observer of an "update only when imm != 0" variant; the body tests both `imm == 0` and `ra == 0 && update`,
  so the joint cell is inside the clause-(d) letter; cost two one-second sessions).  Grok, Argon, GLM, DeepSeek had one
  per form.  *Dispute D3.*  Session total: loads, stores, seven stops, negative apparatus = TEN.
* **B7 ACCEPT -- C21 is FLOOR and C22 is shipped**: one D-form LOAD with D & 3 != 0 (`lwz` at +6 reads 0x06070809 of
  the counting pattern; a blanket mask would read +4) and one D-form STORE with D & 3 != 0 (`stw` at +6).  The witness's
  `lwz` +8 control is KEPT (it corroborates `lwa`'s word) -- it cannot do C21's job (P14, GLM D-C).  Codex's "R18
  applies to all 22 D-form labels" is NOT adopted as a row demand: rows are owed PER ENUMERATED MUTANT (the shared
  assignment masked for every opcode is ONE mutant, killed by C21); the other labels are disclosed, and the rounding
  probe (FP D-forms + `stw`, image-gated, image present M4) is re-run as the collateral consumer.  *Dispute D6.*
* **B8 ACCEPT -- clause (c) = IDENTITY BODY for 58/62 (decode, retire, no memory, no RT/RA write; reserved XO retired,
  not stopped), MEASURED in the kill table, record form `(c): measured at <artifact>`** (Grok, Argon, GLM; Codex's
  by-construction form is admissible only once the gate wiring exists and is not chosen).  Predicted on the frozen
  8-row witness: 4/8 (`ld value`, `ldu value`, `ldu RA after`, `lwa value` red; `lwz value`, `live`, `unasm census`,
  `neg apparatus` green), CONTROL=FAIL, SYMPTOM=PRESENT 3/3 (Codex, GLM).  The detector's own prediction is derived
  from ITS frozen source before its leg runs (never carried from the 8-row instrument -- `#570` B3).  *Dispute D7.*
* **B9 ACCEPT -- clause (b) legs**: full verbatim reinstatement of HEAD's arm, plus Grok's three per-site partials
  (mask restored / cases kept -> `ldu value`, `lwa value`, `stdu value` red, stops green; 58-case restored / mask kept ->
  `ldu RA after`, `lwa value` (width), `xo58_3 bad` red while `ldu value` stays GREEN; 62-case restored / mask kept ->
  `stdu RA after`, `xo62_2 bad`, `xo62_3 bad` red while `stdu value` stays green).  On a reinstated build nothing stops,
  so no row reds for the wrong reason; the P15 hazard bites the FIXED build's green run and is caught by the
  emitted-row pin.
* **B10 ACCEPT -- the named (d) nulls and growth variants, with the brief's gloss CORRECTED**: (i) mask kept, `update`
  left 0 -> the RA rows (DS != 0) and the RA = 0 stop rows (which lose their stop); (ii) `update` set, raw `int16_t`
  kept -> every value/destination row; (iii) `lwa` left at `size` 3 WITH `zero` 0 selects slot 11 = `ppc_instr_invalid`
  = `fatal` + `exit(1)` -- a HOST EXIT, not "the neighbour word consumed" (Codex, Grok, GLM D-B): the coherent null is
  the whole XO-2 branch reverted to the XO-0 flags (slot 15, 8 bytes) -> `lwa value` red; `lwa` with `zero` left 1
  (zero-extension) -> `lwa value` red only against the sign-extended oracle (the witness word has bit 31 set); the
  size-3/zero-0 form is run as its own leg and scored as "host exit, sentinel absent" (the gate's sentinel pin); (iv) XO-0
  plus one / update-everything -> B2's RA rows; (v) the mask applied to every opcode at the shared assignment -> C21;
  (vi) `if (xo == 2) goto bad` leaving XO 3 storing -> `xo62_3 bad` (separate sessions, Grok).
* **B11 ACCEPT -- the census and the contract**: `unassemble` every placed word in every session BEFORE stepping (it
  executes nothing); expectations stay the CURRENT text; two strengthenings: the expected XO comes from a label-keyed
  map (`ld` 0, `ldu` 1, `lwa` 2, `std` 0, `stdu` 1), never from the encoder tuple (Argon, Codex), and the three witness
  words are pinned to their literals `e894ff90` / `e8b5ffa1` / `e8d6000a` (Grok).  Contract: CLAIMED = the five forms,
  the three reserved XOs, the two RA = 0 stops, the D-form scope controls; NOT CLAIMED = RA = RT (D1), 32-bit (A6, with
  the post-fix delta), translation on / MSR SF / page-crossing / indexed forms / access failure (C26) / the
  disassembler's mnemonics; the census sentence; the P15 rule.  The witness probe's `/tmp` dummy file becomes a
  `tempfile.mkdtemp` directory in the promoted copy (Argon; the `ppc_rlwimi_probe.py` idiom).
* **B12 ACCEPT -- gate 13, MANIFEST, ledger term** (unanimous): the block goes in `regress/gate_ppc.sh` AFTER the
  `#565` rldicl block and BEFORE `need_file "$IMAGES/netbsd401-macppc-GENERIC"`, on `-E bareppc -M 64`, pinned in the
  `#565`/`#570` shape (sentinel exactly once; `RESULT=` both halves to the literal N; `CONTROL=OK`, `SYMPTOM=ABSENT`,
  `RED=none` each exactly once; every row by name `count "^$v  .*ok$"` = 1; rows emitted / green / red pinned; a
  `live` row per session); two MANIFEST keys relative to `regress/` -- `ppc_dsform_probe.py` CLASS_DETECTOR (gate 13,
  pin N) and `artifacts/ppcdsformxo/witness_20261024/ppc_dsform_probe.py` CLASS_WITNESS; frozen copies and drivers
  `*.py.txt` / `*.sh.txt`; ledger witness `probe:regress/artifacts/ppcdsformxo/witness_20261024/ppc_dsform_probe.py`
  scoped in the state note to the LOADS, with `prefix_BASE.out` named as the store half's clause-(a) artifact.
* **B13 ACCEPT -- D2 is N/A** (unanimous: equality and truth tests only).  **Bounded**: the set closes at the arm's own
  tests; one ask-again after a clean table (R15).

## C -- filings and record corrections (Q4 and the seats' extra findings)

* **C1 FILE LOW -- the disassembler folds XO into the displacement and prints `ld`/`std` for every 58/62 word**
  (`cpu_ppc.c:1495, 1498, 1517`); witness = the frozen census lines (`ld r5,-95(r21)` for the `ldu` word); its eventual
  fix owes the R16 order (re-pin the census first).  Unanimous.
* **C2 FILE LOW -- the disassembler has no case for `LFDU`/`LFSU`/`STFDU`/`STFSU`** (they execute since `#310` and
  disassemble as an unimplemented primary opcode) -- Codex, Grok, Argon; unfiled (M3).
* **C3 FILE MED -- `ldx`/`ldux`/`lwax`/`lwaux` (opcode 31 XO 21/53/341/373) have no `PPC_31_*` define and reach
  `default: goto bad` on every CPU, while `stdx`/`stdux` are implemented**: a legal 64-bit guest instruction stops the
  emulator (CPU stop, not host exit).  Unfiled (M3).  Its own round; rung-3 witness shape: one stepped `ldx` word on
  HEAD PPC970.
* **C4 FILE (design) -- the 32-bit gating census** (A6): twelve ungated and eleven absent 64-bit-only forms in
  `X(to_be_translated)`; the licensed fix is the `rld*` idiom applied uniformly, in its own round.
* **C5 RECORD -- the brief's C26 premise "no data access fails on `bareppc` with translation off" is FALSE as stated**
  (Codex: `memory_rw.c:695` / `core/memory.c:645`, the halt-on-nonexistent-memory path).  Classification unchanged
  ((e), callee); the sentence is corrected in this record and in the round block.
* **C6 RECORD -- P8's "a base not a multiple of 8 gives an unaligned `ld`/`std`" is false as stated** (A7).
* **C7 RECORD -- CRIT's `testppc` is `bareppc`** in the witness and the detector (GLM D4; both are PPC970, M-equivalent
  for every rowed access; `bareppc` has no devices).
* **C8 RECORD -- the brief's own defects**: Q3(a)'s session list omitted the negative apparatus (restored, B6); section
  12's "every path exists at HEAD" is false for the untracked witness paths (they exist in the working tree; the
  MANIFEST line is conditioned on the commit) (GLM-Q34); P2 inverted (M5); the `lwa size 3` gloss (B10).
* **C9 RECORD -- DeepSeek's "FAULT (member 5)" label for `goto bad`** is wrong (A3); its NOT READY verdicts rest on D1
  and on the store rows being unspecified -- B1/B6 specify them.

## D -- the disputes, each side in its own words, with the ruling (for the adjudicator)

* **D1 -- 32-bit width test.**  Codex: "choose option (ii). Add the `bits == 32` refusal for primary opcodes 58/62,
  before XO-form dispatch. The opcode-30 precedent and PEM :6253 provide R13's transferred warrant. This stays within the
  same decoder site under R17."  DeepSeek: "I choose option (ii) ... within R17 (same site, same semantic class) and
  requires a 32-bit session row (C24)."  Grok: "Disclose ... Do not add the width test in this round. The filed defect is
  the XO fold on the 64-bit CPU. A width gate is a different claim (illegal opcode versus wrong form), it is not
  witnessed, and R17 keeps `stdx`/`stdux` where they are ... Gating 58/62 alone would be a third policy in the same
  function."  Argon: "Twelve 64-bit-only forms ... are ungated on 32-bit CPUs. Adding [the gate] to opcodes 58/62 alone
  is outside the round's witness ... whereas gating all twelve belongs to a dedicated round."  GLM: "(i), disclose: the
  adjudicated design includes no width test ... R17 bars an unwitnessed addition ... (ii) is the licensed future fix."
  RULING A6: (i), file C4.
* **D2 -- a `fatal()` line before the reserved-XO `goto bad`.**  Grok: "Print a `fatal("TODO: ...")` before `goto bad`
  ... Under `step`, `bad:` skips `DISASSEMBLE` ... A row that keys off the disassembly line inside `bad:` fails on a
  stepped session."  DeepSeek: "print a similar message outside read-ahead to distinguish it from an unrecognized
  opcode."  Codex: "follow the silent local `default:goto bad` idiom without another diagnostic or latch."  Argon:
  "Pre-`goto bad` `fatal("TODO: ...")` calls ... are used only for valid architectural features not yet implemented.
  Reserved/illegal XO values ... are invalid instruction forms, so bare `default: goto bad;` is the exact fork idiom."
  GLM: "No own message: the fork's idiom for 'encoding not in the table' is silent `goto bad` leaving the message to
  `bad:`."  RULING A3: bare; the channel is the `UNIMPLEMENTED instruction` line, which M1 shows prints under `step`.
* **D3 -- RA = 0 update stops at both DS partitions.**  Codex: "C6/C17 need both zero and nonzero displacement:
  dropping update at DS=0 is invisible in a valid update access, but changes an RA=0 refusal into an access. The invalid
  joint cells close that otherwise invisible channel."  Grok / Argon / GLM / DeepSeek: one stop session per form
  (DS != 0).  RULING B6: both partitions (four stop sessions), on the joint-cell letter and the two-second cost.
* **D4 -- DS = 0 value rows.**  Grok: "C2, C3 (e) ... DS=0 and RA=0 `ld` are already correct; the index split is
  invisible on PPC970 ... P2's 'only DS=0' clause is the wrong place to spend a row."  Codex: "C5/C10/C16 remain
  address/value floor cells, although they cannot distinguish equivalent table halves."  Argon: FLOOR with the channel
  "loaded value at RA vs RA + 1".  GLM: "floor cells by R7's letter ... I recommend shipping (one row each, live
  channel)."  RULING B4: ship, value channel.
* **D5 -- C9 and C18.**  Argon: C9 "FLOOR (D3) ... kills any sign-extension mutant that unconditionally sets high bits";
  C18 "FLOOR (D3) -- kills a decoder mutant ... that mistakenly adds `if (ra == rs && update) goto bad;`."  Codex: C9
  "(e): loaded-word sign is not a decoder body partition"; C18 "(e) as an alias axis; useful additional coverage that I
  would retain."  Grok: C9 "(e) Bit 31 clear does not separate sign-extend from zero-extend"; C18 "(e) ... Ship it if
  the row budget allows: `stdu r1,-N(r1)` is the form guests use."  RULING B5: C9 (e) not rowed; C18 (e) rowed by
  choice.
* **D6 -- C21/C22 scope.**  Codex: "R18 applies to all 22 D-form labels ... C21/C22 cannot be one representative each
  while C23 is blanket disclosure. Their scope controls need nonzero low displacement bits. This does not authorize
  crossing every label with arbitrary data."  Grok: "C21 FLOOR ... C22 (e) Same shared assignment as C21. One odd load
  kills it."  Argon: both FLOOR, one each.  GLM: C21 owed, C22 "one cheap row -- recommend shipping."  RULING B7: one
  load + one store representative; rows per enumerated mutant; the rest disclosed with the rounding-probe re-run.
* **D7 -- clause (c) record form.**  Codex: "`(c): by construction via ld value and gate 13's named-row equality plus
  literal N/N pins, leg not run` ... not yet discharged at HEAD."  DeepSeek: by construction.  Grok: "Record it as `(c):
  measured at <artifact>` after the leg runs."  Argon, GLM: measured.  RULING B8: measured.
* **D8 -- the store anchor.**  DeepSeek: "reload destination with a correct `ld` XO=0 and compare."  Codex: "Use the
  debugger's direct memory dump as the primary destination anchor. A `lbz` or `lwz` reload can corroborate it; another
  DS-form load alone is insufficient independence."  Grok: "A reload by `ld` is a second observation from a decoder
  this round is also changing. `dump` is the anchor."  RULING B1: `dump`.

## E -- build order (the spec the builder receives, by id)

1. Freeze the witness (untouched; its receipts are in `witness_20261024/receipts/`).  2. Write `PRETABLE.out` (sibling
parity across the five forms and the D-form siblings; claim -> row; guard-field / body-field with the partitions the body
induces -- `imm == 0`, `ra == 0 && update`; CHANNEL per row with its mutant) BEFORE any table.  3. Promote the probe to the
grown detector (B2-B7, B11) and run it on BASE -> `prefix_BASE.out` (store half RED, load half RED, controls green) BEFORE
the C edit; run the frozen witness post-fix later for its same-script GREEN.  4. The repair (A1-A4) in a scratch clone
`/tmp/gxt2/fix`; the detector GREEN there; the frozen witness GREEN there.  5. Kill table in the clone: (b) full + three
partials (B9); (c) identity body (B8); (d) nulls and growth variants (B10); clone-local sentinel; frozen driver copy.
6. Gate 13 block (B12), MANIFEST, `check_probe_wiring.py` at HEAD + two keys; rounding probe re-run (M4).  7. Pass 2 on the
diff; F2; land (`commit_unit2.py`); follow-up records.

## F -- THE ADJUDICATION (added 07:4x)

**F1 -- GPT-6 Astra, `adj/codex_t2p1adj.txt` (07:31, gpt-6-astra / ultra, verdict in stdout, refusal 0): `VERDICT:
AMEND -- FOUR reviewing seats, seven answers including Astra's prior review; retain the repair, correct the incomplete
floor and the erroneous supporting claims.`**  Three of its checkable claims were re-verified by the main loop before
adoption: the probe prints `PPC_DSFORM_PROBE_DONE` after ANY subprocess return (`ppc_dsform_probe.py:324-331, 486-492`),
`cmpd`/`cmpld` are selected ungated at `cpu_ppc_instr.c:4624-4630`, and gate 13's protocol idiom counts every KEY line
in any form and then the well-formed one (`gate_ppc.sh:140-144, 197-200`).  Every amendment is ACCEPTED:

* **A3** rationale corrected: the pre-`goto bad` `fatal()` sites are NOT only valid-but-unimplemented features (the RA = 0
  guard diagnoses an invalid form; the `rld*` guard an illegal instruction); the bare refusal stands because the common
  tail's `UNIMPLEMENTED instruction` line is the stepped diagnostic (M1).  The `#571` comment must not carry the false
  census.
* **A6** retained as (i) with the rationale amended (R17 does not categorically forbid a same-site width check; the
  `rld*` warrant is available; "a third policy" withdrawn) and the disclosure widened: in MODE32 the legal forms select
  the MODE32 handlers (M2) while reserved XO and the RA = 0 update forms now stop there too.  Astra withdrew its pass-1
  claim that (ii) was required.
* **A9 / B9** site inventory corrected to A2's localization: the edited sites are the TWO CASE BODIES (each carries its
  own mask); there is no independently restorable shared mask line.  Clause (b) = each case reinstated verbatim (its
  local mask goes with it) and both together; "raw `imm` kept with the XO dispatch kept" is a SEMANTIC PARTIAL, named as
  such.
* **B2** mutant naming split: "XO 0 decoded as XO 1" (transfer kept, RA changes -> the RA rows) and "EA + 1 on XO 0"
  (transfer changes, RA kept -> the value/destination rows) are two legs.
* **B7** rationale corrected: the other 22 D-form labels are not owed rows because they do NOT REACH the inner DS-case
  edits (A2), not "per enumerated mutant"; the odd load is the blanket-mask control, the odd store retained coverage; if
  the builder edits the shared assignment instead, the dominating-label analysis is redone.  Astra withdrew "all 22".
* **B10** two predictions corrected: the raw-displacement leg reds the 58/1, 58/2, 62/1 value/destination rows ONLY (XO-0
  and D-form controls stay green); the `lwa size 3 / zero 0` leg terminates the EMULATOR, not the Python detector --
  the probe records the return, supplies missing register values, emits failed rows and still prints DONE -- so it is
  scored as "emulator terminated; that session's rows red; CONTROL=FAIL; sentinel present", never as a wrong-width
  transfer and never as a missing sentinel.
* **B11 / B13** completeness: EIGHT legal-access cells were missing from the floor by the same joint-cell reasoning
  B4/B6 adopted -- `ld` {DS = 0; RA = 0; both}, `lwa` {RA = 0 at DS != 0; RA = 0 at DS = 0}, `std` {DS = 0; RA = 0;
  both} -- value/destination channel each, no new session (RA = 0 cells use a seeded low-memory window reachable by the
  14-bit DS; the DS = 0 and RA = 0 cell uses address 0).  N becomes about 46; the literal follows the frozen detector.
* **B12** protocol precision: count EVERY occurrence of each protocol key in any form (== 1), then its sole accepted
  value (== 1) -- the `gate_ppc.sh:140` idiom; MANIFEST classification is required at STAGING (HEAD
  `check_probe_wiring.py` domain), not only at commit.
* **C4** census: at least FOURTEEN ungated 64-bit-only forms (`cmpd`, `cmpld` added); "decoder-ungated" is not "same
  runtime behaviour" (`extsw` in MODE32 diagnoses and returns); the filing does not pre-authorise a uniform sweep.
* **Q3** qualifications adopted into the PRETABLE's CHANNEL column: numeric RA write-back at DS = 0 cannot detect a
  dropped update; DS = 0 value rows cannot distinguish table halves; unchanged RA alone cannot prove a refusal; RA rows
  cannot detect an address-only increment; `stdu neigh` stays green under the identity body.  Names fit with session
  prefixes (`stdu ra0z live` = 14).  The negative-apparatus session intentionally has no guest liveness.
* **Q5** order adopted (BUILD_SPEC section 10): reconcile the edit-site inventory and the joint-cell/channel enumeration
  BEFORE PRETABLE is finalised; FREEZE the detector's rows and oracles BEFORE its BASE run; write each leg's prediction
  from the frozen detector source BEFORE the leg runs (the identity leg's 4/8 belongs to the witness, not the detector);
  no by-construction claim before the gate block exists.
* UPHELD by Astra: A1, A2, A4, A5, A7, A8; B1, B3, B4, B5, B6, B8; C1, C2, C3, C5, C6, C7, C8, C9 (closest
  qualifications: B4/B6 channels kept distinct; C5 conditional; B1's anchor matters more than eight distinct bytes --
  eight bytes are sufficient, not necessary, and the alias row's source equals its base; A5's RT = EA presumes a
  successful access).

**F2 -- Grok 4.7, `adj/grok_t2p1adj.txt`: PENDING at 07:4x (its opening line only); appended on arrival.**

**F2 -- Grok 4.7, `adj/grok_t2p1adj.txt` (07:4x, xhigh, plan mode, exit 0): `VERDICT: AMEND -- basis is four reviewing
seats (seven answers); B6's four RA=0 stops are not floor, and B10's host-exit leg is not a missing probe sentinel.`**
The two adjudicators AGREE on D1, D2, D4, D5, D6, D7, D8, on B10's sentinel correction, on A6/C4's census (fourteen
ungated implemented forms; the absent eleven are `goto bad` on every width, so the future `rld*`-gate round targets the
ungated IMPLEMENTED set), on A3's rationale, on B7's rounding-probe overclaim (the rounding probe's D-form displacements
are all multiples of 4, so its re-run is collateral "still executes" and cannot see the shared-mask variant -- C21 is
that control), on C5 (the failure path is gated by `-T`, `halt_on_nonexistant_memaccess`, which the probe does not
pass; still (e), callee) and on the build order.  They DISAGREE on ONE point and the main loop rules it:

* **D3 -- the RA = 0 stop cells at DS = 0.**  Astra: keep four sessions ("R6 expressly crosses body-tested partitions
  ... Their cost is irrelevant to the obligation").  Grok: "The carrier's pass-11 bound ... makes the floor the guard's
  dominating predicates crossed with device-state lvalues the repair path itself reads.  The repair writes `imm` and
  `update`.  It does not read `ra`.  `imm == 0` crossed with `ra == 0` is a multi-axis joint, which that same bound
  leaves as clause (e) debt.  The ruling's other ground, 'two one-second sessions,' is the addition licence's forbidden
  'it cannot hurt.'"  **RULING: Grok.**  The carrier's pass-11 text is the quoted rule ("the FLOOR -- the cells a row is
  OWED for -- is the cross-product of the guard's dominating predicates with the ... lvalues the fix's own repair path
  reads ... joint cells outside the floor are clause-(e) coverage debt, subject to the one ask-again"), and the
  generating-set clause makes the single-axis marginals (`imm == 0`; `ra == 0`) the obligation at each floor cell, never
  their product.  So: B6 = ONE RA = 0 stop session per update form at DS != 0 (`ldu ra0`, `stdu ra0`); the DS = 0 x RA = 0
  cells are DISCLOSED under (e) with Astra's observation recorded (they are the only observer of an "update only when
  `imm != 0`" variant).  **The same bound trims Astra's eight legal-access cells (F1, B11/B13) to the FIVE single-axis
  marginals**: `ld ds0 value`, `ld ra0 value`, `lwa ra0 value`, `std ds0 value`, `std ra0 value`; the three joints
  (`ld` DS = 0 & RA = 0, `std` DS = 0 & RA = 0, `lwa` RA = 0 & DS = 0) are disclosed.  Sessions: EIGHT (loads, stores,
  five stops, negative apparatus).  N about 39 (14 + 12 + 10 + 3); the literal follows the frozen instrument.
* **B10 scoring (both adjudicators):** the `lwa size 3 / zero 0` leg is scored by the session's `how=exit1` on a REAL
  machine plus the transcript line `PPC: invalid(): INTERNAL ERROR` (`cpu_ppc_instr.c:243-244`), its session's rows red,
  CONTROL=FAIL, sentinel PRESENT.
* **B12 names (Grok):** the witness prints `%-16s` and asserts `len(name) <= 15`; the gate pin `^name  ` needs TWO
  spaces after the name, so a 15-character name passes the assert and MISSES the pin (the padded-column trap).  RULING:
  names are capped at 14 characters (the probe's assert becomes `<= 14`, with a comment naming the pin); every proposed
  name is 14 or shorter.
* **A2 (Grok):** "inside the two cases" is a SUFFICIENT shape, not the only one (one masked assignment after the inner
  switch and before `:4335` also feeds both consumers once reserved XO has left).  The spec keeps the inside-the-cases
  shape; the record states the invariant (one `imm`, both consumers), not the syntax.
* **A3 (Grok):** the `:4815` citation was false (the `break` after `tlbsync`'s `nop`); corrected in place above.
* **D4 (both):** the DS = 0 value rows are shipped for the ADDRESS channel; the record must not say they prove the
  table-half selection (both halves delegate to the generic handler on PPC970).
* Grok UPHELD: A1, A2, A4, A5, A7, A8, A9, B1, B2, B3, B4, B5, B8, B9, B11, B13, C1-C3, C5-C9 (least sure: B4, C5,
  A2's "INSIDE" -- each with the qualification recorded above).
