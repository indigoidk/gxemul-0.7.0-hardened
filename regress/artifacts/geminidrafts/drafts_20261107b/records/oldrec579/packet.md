# Reading task: oldrec579 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC579-81d2` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #579 ppcllscrcexit (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 868-1030 of CHANGELOG_521d136a.md; each line carries its own number -- cite those numbers)

```text
  868| # `#579` Records (follow-up, 2026-11-04): `ppcllscrcexit` names its landing commit `dc35d1be`; the committed-tree proofs; the pass-2 receipt
  869| 
  870| `git ls-tree dc35d1be`, md5s hashed in Python from the committed bytes: `src/cpus/cpu_ppc_instr.c` blob `8797a48c3110`, md5 `29963c800505`; `regress/ppc_llsc_probe.py` blob `5c8a6a58df97`, md5 `6ecf66745f53`; `regress/gate_ppc.sh` blob `370dcea54378`, md5 `0632bde42a09`.  The working tree matches each (cpu_ppc_instr.c same, ppc_llsc_probe.py same, gate_ppc.sh same).
  871| 
  872| The row's `commits` field names `dc35d1be` and its state note gives the landing date, 2026-11-04 (it said 2026-11-03, the day the fix was built; the CHANGELOG block and OUTSTANDING_BUGS say 11-04).  The `regress/pass2_ledger.tsv` receipt line for `dc35d1be`, a landing line in OUTSTANDING_BUGS.md's `#579` section and `matrix.html` re-rendered complete this records commit.
  873| 
  874| # `#579` (2026-11-03) -- `ppcllscrcexit`: the PowerPC load-reserve / store-conditional handler no longer ends the emulator process on the four bit-31 forms the decoder delivers to it
  875| 
  876| **The defect.**  `src/cpus/cpu_ppc_instr.c`, `X(llsc)` (HEAD `ebe5af82` :2276-2374): the opcode-31 decoder keys on the ten-bit extended
  877| opcode alone (`xo = (iword >> 1) & 1023`, :4643) and its arm at :4895-4900 sends every word with XO 20 (lwarx), 84 (ldarx), 150 (stwcx.)
  878| or 214 (stdcx.) to the handler with the raw word, so both values of bit 31 arrive.  The handler recomputed `rc = iw & 1` and ended the
  879| process -- `fatal()` + `exit(1)` -- at :2305-2308 on lwarx/ldarx with the bit set and at :2331-2334 on stwcx./stdcx. with it clear.  One
  880| guest instruction, any privilege level (no MSR[PR] test on the path), every modelled CPU (`tmp_ppc_tail.c` builds the 64-bit and the
  881| MODE32 decoders from this one source).  Filed 2026-10-02 from the Astra review campaign; external-research batch item 2 (T3, `regress/
  882| artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md` D).  #216 had already converted the two memory-fault exits in the same function;
  883| these two remained.  Two record corrections: the filing's "stwcx./stdcx. with Rc=0" names the DOTTED mnemonic, which means bit 31 = 1 -- the
  884| killing store words are the undotted encodings; and the ledger note's decoder citations ":4614, :4866-4871" were stale (:4643 and
  885| :4895-4900 at HEAD).  The guard citations had not drifted.
  886| 
  887| **The architecture, read in the local extracts and nowhere else.**  Book I v2.01 (`_scratchpad/ppc_uisa_book1_v201.txt`) :432-433
  888| "Reserved fields in instructions are ignored by the processor", :438-439 "/" denotes a reserved field, :1109-1114 an invalid form is a
  889| wrongly coded field "excluding the opcode fields and reserved fields", :1116-1120 "Any attempt to execute an invalid form of an
  890| instruction will either cause the system illegal instruction error handler to be invoked or yield boundedly undefined results",
  891| :1122-1128 the Store Conditional instructions are among those whose field "other than that specified in the layout diagram" makes the form
  892| invalid; Book II v2.01 (`_scratchpad/ppc_vea_book2_v201.txt`) :1264 the lwarx/ldarx layouts show bit 31 as "/", :1305 and :1307 the
  893| stwcx./stdcx. layouts show "1", :1323 and :1337 the CR0 results.  So the load pair's bit-31-set words are VALID forms whose reserved bit
  894| the processor ignores, and the store pair's bit-clear words are INVALID forms with two permitted outcomes, of which executing the defined
  895| store-conditional is one (its result is achievable by executing stwcx. itself -- the boundedly-undefined bound, :451-452 completed by
  896| `ppc_pem_32and64_2005.txt:6213`; the definition is the LEFT column of Book I :451-458 -- the right column is an interleaved Programming Note on system registers -- and the empty-sequence reading, that doing nothing is also inside the bound, is reasoned, not quoted, and nothing here rests on it: MYTHOS_F2R D1).  F2R D1's obligation -- the four extract lines the shipped comments rest on, read before commit -- is discharged by `regress/artifacts/ppcllscrcexit/adj_20261103/STEP1_RECORD_CHECKS.md`: Book I :430-436 and :1107-1120, Book II :1259-1266 and :1301-1309, each saying what the comment claims.  The eleven modelled CPUs (`cpu_ppc.h:75-88`) predate the ISA revision that gave the load-reserve low
  897| bit a hint meaning; ignoring the bit is right under both readings.
  898| 
  899| **The ruling (pass 1; `regress/artifacts/ppcllscrcexit/adj_20261103/FABLE_ADJ.md`, Fable 5.1 in the main loop, on 4 of 4 roster seats
  900| for the bug-review and fix-draft briefs -- GLM 5.3, Grok 4.7, GPT-6 Astra, Gemini 4 Argon -- and 3 of 4 for the manual, siblings and
  901| port briefs, Astra owed; the five bug-review stage dirs `_scratchpad/panel_20261103_1030{44,45}_next5_ppcllscrcexit{,_draft}/`,
  902| `_scratchpad/panel_20261103_1112{21,22,24,25}_next5_ppcllscrcexit_{manual,siblings,witness,port}/`, the Gemini-web packets under
  903| `_scratchpad/gweb/jobs_20261102_next5/ppcllscrcexit*/` and Argon's adjudication proposals under `_scratchpad/gweb/jobs_20261103_adj/
  904| ppcllscrcexit_*/`; the answer index is `adj_20261103/ANSWERS.tsv`).  Draft A for both pairs: DELETE (member 1) for the load pair -- a
  905| valid form, the value was always acceptable -- and ACCEPT (member 4) for the store pair -- an invalid form whose defined-operation result
  906| is a permitted outcome the body already computes.  In the words the F2 ruling requires for the record (MYTHOS_F2R D2): the guard is deleted and the core executes the defined store-conditional, CR0 update included -- a permitted outcome of the invalid form (Book I v2.01 1.9.2); the illegal-instruction outcome is unavailable on this core and not required.  No announce: there is no event a guest needs told about, and a `(once)` message would be
  907| a wrong record for the load pair.  Draft B, an illegal-instruction Program interrupt, REJECTED on three grounds, any one sufficient: it is
  908| prohibited for the load pair; for the store pair it buys no conformance A lacks while being IMPLEMENT -- `ppc_exception()` (`cpu_ppc.c:
  909| 318-345`) has no Program vector constant (`cpu_ppc.h:252-257`), writes SRR1 as `msr & 0x87c0ffff` with no illegal-instruction cause bit,
  910| and takes SRR0 from a `cpu->pc` that `X(llsc)` never synchronises; and a mixed design splits one defect across a reserved-versus-required
  911| bit for no guest benefit.  The tentative draft's third hunk (`+ ll_bit = 0` in the failure arm) was a FALSE ADDITION -- the line exists at
  912| :2346 -- so Grok and Astra were right against GLM and Argon on that point; the ruling checked it in the source.  Count the arguments, not
  913| the seats: the deciding argument was the Book I/II text, which no bug-review seat had, and the manual brief's three answering seats
  914| (Grok, GLM, Argon) all read it the same way.
  915| 
  916| **The witness (rung 3).**  `regress/ppc_llsc_probe.py` (the detector below) run against the COMMITTED `build/gxemul` (two-part
  917| clearance passed: `cmp` clean against SEC, binary 2026-11-03 08:52 newer than the 11-02 source) BEFORE the edit:
  918| `regress/artifacts/ppcllscrcexit/witness_20261103/prefix.out`, written 23:15:14 -- `PPC_LLSC_RESULT=44/73`, `CONTROL=OK`,
  919| `SYMPTOM=PRESENT`; the 29 red rows are exactly the six bit-31 sessions (lwarx and ldarx with bit 31 set, stwcx. and stdcx. with it clear,
  920| on the PPC970 of unmodified `-E bareppc -M 64`; lwarx and stwcx. again on `-C PPC603`) and their dependent rows, and every one of those
  921| six transcripts (`prefix_sessions/`) ends at the step with the handler's text `ll: rc-bit set?` or `sc: rc-bit not set?` and exit status 1.
  922| The same script on the rebuilt `build/gxemul` after the edit: `postfix.out`, 23:17:12 -- `73/73`, `SYMPTOM=ABSENT`.  Same script,
  923| opposite colour; the pre-fix record predates the source edit (23:16), which makes `prefix.out` the order proof.  The FINAL 83-row
  924| instrument was then run on HEAD's source in the scratch clone (HEAD's `cpu_ppc_instr.c` written in and rebuilt):
  925| `prefix_final2.out` 2026-11-04 00:51 -- `50/83`, `CONTROL=OK`, `SYMPTOM=PRESENT`, the 33 red rows being the bit-31 sessions and their rows;
  926| and on `build/gxemul` after the edit: `postfix_final2.out` 00:5x -- `83/83`.  A run against a reconstructed pre-fix tree supplies a red,
  927| not an authentic pre-edit date; the date is `prefix.out`'s.  Liveness: the valid lwarx loads a non-palindromic eight-byte pattern (the
  928| 4-byte and 8-byte loads assemble different VALUES), the valid stwcx. after it stores its bytes and sets CR to 0x2fffffff from a seed of
  929| 0xffffffff; architecture signature: the loaded value, the stored bytes, the CR value (the no-reservation path gives 0x0fffffff, so the
  930| control demands the success value); a bogus-machine negative control runs no guest.  `prefix_run2_apparatus.out` is an earlier pre-fix
  931| run kept for the record: its three red control rows were the probe's own 32-bit-leg apparatus (a 64-bit sentinel read back truncated, an
  932| 8-digit `dump` address the parser refused), fixed in the probe before the witness run; the defect rows were identical.
  933| 
  934| **The fix** (`git diff`: 1 file, 3 hunks, +18 -9).  In `X(llsc)`: the two guards are DELETED, the now-unread `rc` is dropped from the
  935| declaration, and a `#579` comment stands at each site recording the per-pair reason.  The comment wording is the F2 ruling's (MYTHOS_F2R parts 5-6), applied verbatim.  The store site carries F3's sentence -- "this core defines no Program-interrupt constant and sets no illegal-instruction cause bit in SRR1, and none is required" -- and F2's: "The #216 return below stays: it follows a failed memory access, after which the memory path may already have raised an exception or stopped the CPUs, or raised nothing at all (a failed device access raises no PPC exception); this handler adds nothing either way."  Nothing else moves: every exit path (the #216 returns and the reservation-failure
  936| return) was already inside the valid-form body, the function has no common tail after the if/else, and `old_so` is read before the removed
  937| store guard in both versions.  Not touched, on purpose: the decoder arm (routing the bit-31 forms to `goto bad` would trade a host kill for
  938| a CPU-STOP), the #216 returns, the CR0/XER-SO logic, the all-CPU reservation clear, `X(invalid)`, the fetch exit (`qhslowifetch`, the next
  939| row), the disassembler (`cpu_ppc.c` prints `lwarx`/`stwcx.` for both bit-31 values; disclosed), and the pre-existing comment "copied to to
  940| bit 4" (upstream text about CR0; the code is right; assessed, not changed).  Byte-identical in `GXEMUL-SEC` and `est/`; propagated to and
  941| rebuilt in all three build trees (part 1 `cmp` clean and part 2 binary newer on each, re-checked 2026-11-04 00:5x and 01:10; `est/` is a
  942| source tree, part 2 N/A).
  943| 
  944| **The detector.**  `regress/ppc_llsc_probe.py` -- 83 rows over 23 cold `-E bareppc -M 64` debugger sessions (PPC970; a `-C PPC603` leg
  945| runs the word forms): a control and a bogus-machine negative control; the four valid forms (`lw ok`, `ld ok`, `stw ok`, `std ok`); six
  946| reservation and XER[SO] controls (`noresv`, `mismatch`, `chain`, `so`, `nso` -- SO on a failure --, `twice` -- a second store-conditional
  947| after a success --) and a field-decode control (`ra` -- RA = 6, RT = 17, RB = 20); the four bit-31 forms (`lw rc1`, `ld rc1`, `stw rc0`, `std rc0`) wanting the SAME
  948| observables as their valid twins, and two reservation sessions on them (`rc1 resv` -- a bit-31-set lwarx whose reservation a stwcx.
  949| consumes --, `rc0 noresv` -- a bit-clear stwcx. with no reservation); on the 32-bit CPU the two valid and the two bit-31 word forms; and the
  950| `unasm census` at 35/35 placed words.  Every fixed form's row group demands the value, the bytes or the CR; its `session`, `pc` and `seed` rows
  951| carry the exit status, the program counter and the seed (F2R F20).  Names are at most 16 characters in an 18-wide column.  Protocol: `PPC_LLSC_RESULT=n/N`, `CONTROL`, `SYMPTOM` (`PRESENT` when any
  952| transcript carries the handler's fatal text), `RED`, `PPC_LLSC_PROBE_DONE`.  Wired into `regress/gate_ppc.sh` as the `#579` block before
  953| the NetBSD prerequisite (the #571 shape): sentinel once and last, the four protocol keys once each, RESULT pinned at `83/83` by equality,
  954| CONTROL=OK, SYMPTOM=ABSENT, RED=none, all 83 names, the census at 35/35, rows run/green/red 83/83/0; gate 13 alone: PASS, 290 checks
  955| (`regress/artifacts/ppcllscrcexit/gate_20261104/`).  `tools/precommit_check.sh` `SCORE_CLAIMS_MANIFEST` 43 -> 44 (the probe's docstring is
  956| checked; two phrases the checker read as score claims were reworded).
  957| 
  958| **The kill tables** (`regress/artifacts/ppcllscrcexit/killtable_20261103/`, in the scratch clone `/tmp/gx579`, a `cp -a` of `build/`
  959| after the fix; baseline = the post-fix working set, `cmp` clean before variant 1; each table's `PRETABLE*.out` precedes its BASE run by
  960| mtime; the clone's binary rebuilt and checked newer on every build; clone left clean).  Table 1 measured the 73-row probe, table 2 the
  961| 77-row one, table 3 the four edits the pass-2 seats predicted would escape, and TABLE 4 -- the record's table -- all twenty-one variants
  962| against the FINAL 83-row probe (`table4/SCORES4.txt`):
  963| 
  964| | variant | what | table 4 | red rows |
  965| |---|---|---|---|
  966| | BASE4 | the post-fix working set | 83/83 | -- |
  967| | M1_loadguard | (b) the load guard reinstated verbatim (`rc` as `iw & 1`) | 66/83 | the three bit-31 load sessions and `rc1 resv` |
  968| | M2_storeguard | (b) the store guard reinstated verbatim | 67/83 | the three bit-31 store sessions and `rc0 nr` |
  969| | M3_loadinv | (d) `if (load)` inverted | 47/83 | every value / bytes / CR row that depends on the path |
  970| | M4_loadrekey | (d) `if (load && !(iw & 1))` | 75/83 | `lw rc1`, `ld rc1`, `lw32 rc1` value and cr, `rc1 resv` |
  971| | M5_ldarxlen | (d) `len = 8` dropped on LDARX | 81/83 | `ld ok value`, `ld rc1 value` |
  972| | M6_stdcxlen | (d) `len = 8` dropped on STDCX | 81/83 | `std ok bytes`, `std rc0 bytes` |
  973| | M7_len8all | (d) `len` defaults to 8 | 67/83 | the word-form value, bytes and tail rows |
  974| | M8_loadnoop | a no-op `return` at the load site | 78/83 | the bit-31 load values and `rc1 resv` |
  975| | M9_storenoop | a no-op `return` at the store site | 76/83 | the bit-31 store bytes and cr, `rc0 nr cr` |
  976| | M10_noeq | EQ not set on success | 75/83 | every success-path cr row |
  977| | M11_noso | XER[SO] copy dropped on success | 82/83 | `so cr` |
  978| | M12_noresv | the reservation test nulled | 71/83 | `noresv`, `mismatch`, `chain`, `twice`, `nso`, `rc0 nr` bytes and cr |
  979| | M13_noclear | the failure-path `ll_bit` clear dropped | 81/83 | `chain bytes`, `chain cr` |
  980| | M14_noallclr | the success-path all-CPU clear dropped | 81/83 | `twice bytes`, `twice cr` |
  981| | M15_nora | the RA base dropped | 82/83 | `ra value` |
  982| | M16_mask15 | the register-field masks narrowed to 4 bits | 82/83 | `ra value` |
  983| | M17_rc1noresv | a bit-31-set lwarx loads but does not reserve | 81/83 | `rc1 resv bytes`, `rc1 resv cr` |
  984| | M18_nofailso | the failure-path XER[SO] copy dropped | 82/83 | `nso cr` |
  985| | M19_succll1 | the success-path clear sets `ll_bit = 1` | 81/83 | `twice bytes`, `twice cr` |
  986| | M20_nodsiret | the load-side #216 DSI `return` deleted | 83/83 | -- (DISCLOSED: the #216 paths are outside the contract) |
  987| | M21_rc0skipresv | a bit-clear stwcx. skips the reservation test | 81/83 | `rc0 nr bytes`, `rc0 nr cr` |
  988| | NULL4 | (c) `/bin/true` as the binary | 15/83, CONTROL=FAIL | -- |
  989| | NOBIN4 | (c) a missing path | 1/83, CONTROL=FAIL | -- |
  990| 
  991| Floor: (a) measured at `witness_20261103/prefix.out` (44/73, before the edit) and `prefix_final2.out` (50/83, the final instrument);
  992| (b) M1 and M2, each guard at its own site; (c) measured on the shipped probe at `f2r_20261104/probe_true.out` and `probe_absent.out` -- /bin/true 14/83 and a
  993| missing binary 0/83, CONTROL=FAIL and the census 0/35 FAIL on both, `neg apparatus` red on both; table 4's NULL4 15/83 and NOBIN4 1/83
  994| predate census repair B (`table4/ADDENDUM_20261104.md`); the gate pins RESULT by equality.  DISCLOSED: the 14 `session` rows are
  995| exit-status oracles a non-emulator passes.  (d) the predicates dominating the deleted lines are `if (load)` and the `switch (xo)` arms that set `load` and `len`
  996| (M3-M7); for a pure deletion the removed predicate re-introduced under a different predicate (M17 at the load success, M21 at the store
  997| test).  M17, M18 and M21 escaped the 77-row probe (M17 and M18 measured at 77/77 in table 3; M21 predicted by reading -- no 77-row session
  998| runs a bit-clear stwcx. without a reservation) and the six rows added for them (L1, pre-ship) red each one in table 4.  Their warrant, settled by
  999| F2R F5: each is the removed predicate re-introduced under another predicate, and the row pins the shipped comment's own claim that the bit-set form "runs this one body" -- inside the DEPENDS-ON bound; sibling parity is a second warrant, not a competing one.
 1000| 
 1001| **Pass 2 (the real diff)** ran on 4 of 4 roster seats (`_scratchpad/panel_20261103_231958_p2_ppcllscrcexit/`: GLM 5.3, Grok 4.7,
 1002| GPT-6 Astra by the pointer form, Gemini 4 Argon through `_scratchpad/gweb/jobs_20261103_adj/ppcllscrcexit_pass2/`): all said the CODE is
 1003| right and asked for changes to comments and the probe.  **The F2 adjudication pass** (`_scratchpad/panel_20261104_010140_f2_ppcllscrcexit/`,
 1004| fired 2026-11-04 01:02) put the main loop's PROPOSED dispositions F1-F22 / D1-D3 to the 00:5x roster -- the Opus 5.5 Agent seat (READ-ONLY;
 1005| `agent_models.py`: claude-opus-5-5 throughout, one disclosed refusal), Grok 4.7, GPT-6 Astra (two angles), GLM 5.3, Argon -- 5 of 5
 1006| answered.  Four seats refuted the proposed F2 rewording; Grok and Astra independently found that the proposed census repair would fail a
 1007| correct build (35/36) unless the bogus-machine session is excluded; F22's count is 43, not 40; and F13's "APPLIED" was a wrong record of the
 1008| main loop's (CHECKED: `FABLE_ADJ.md` holds neither 2354 nor 2355).  The record of every answer, the CHECKED facts and the open questions:
 1009| `regress/artifacts/ppcllscrcexit/adj_20261103/F2_RECORD.md`.  **The F2 ruling of record** is `adj_20261103/MYTHOS_F2R.md` -- Claude Mythos 5.1 in Claude Code Cloud, the owner's route for a step Fable 5.1's own cloud run could not take (its F2 run was stopped by a safeguard: `_scratchpad/mythos_20261104/579/fable_cloud_stopped.md`): 25 rulings, 21 fix-in-round, 7 filed, 5 rejected, SHIP-WITH-CHANGES; a same-model replication (`MYTHOS_F2R_r2.md`) reached the same verdict.  Applied in its order: the two product comment sentences (F2, F3), census repair B (the census counts the words PLACED, known before the run, `neg` excluded) and the docstring and note edits (F14, F19, F20).  Measured at `f2r_20261104/`: build 83/83, /bin/true 14/83, a missing binary 0/83, census 35/35 / 0/35 / 0/35, gate 13 alone PASS 290; the shipped census code is the measuring seat's repair B by syntax-tree identity (`f2r_20261104/SOURCE_IDENTITY.md`).  **The repair's pass 2** (`_scratchpad/panel_20261104_110801_p2r_ppcllscrcexit/`: Grok 4.7, GLM 5.3, cloud Fable 5.1, cloud Mythos 5.1, Gemini 4 Argon) found docstring wording errors only, fixed as v2 (docstring only).  Its adjudication went to cloud Fable 5.1, whose safeguards stopped it (`[cyber]`, request req_011CgiKT7rpt2wbXguEUPErn); the Mythos retry, reworded in plain terms, is the closing ruling (`adj_20261103/MYTHOS_F2P2R.md`): 14 rulings, 0 floor gaps, D1 EQUIVALENT (the literal-35 denominator and the re-keyed one-word exclusion give the same output on every medium), D2 FILE (gate 13's dead-binary legs, a harness row), CHAIN CLOSED, SHIP.  **The regress review** (Fable-only; cloud Fable 5.1, `adj_20261103/FABLE_REGRESS.md`): 31 checks, 0 floor breaches, 6 record findings, all applied -- R1-R3 in the probe docstring, R4 `killtable_20261103/table4/ADDENDUM_20261104.md`, R5 `killtable_20261103/PRETABLE.errata.md` (with F2R F18's two lines), R6 the gate comment's label (its Book I 1.5.2 and 1.9.2 citations checked true at :430 and :1107) -- together with the closing ruling's RB-only disclosure and re-wrap.  F2R F15 and F16 are a dated corrections section in `adj_20261103/FABLE_ADJ.md`.  Every docstring edit leaves the probe's syntax tree equal to the measured copy (`SOURCE_IDENTITY.md`, its v2 and L4 lines).
 1010| 
 1011| **Seats.**  Pass 1, roster per the owner's ruling of 2026-11-03 12:0x: GLM 5.3 (packet-fed), Grok 4.7 xhigh (file-reading, plan mode),
 1012| GPT-6 Astra (file-reading, read-only; its pass-1 stage answers are the `_r2` re-fires after the 11-03 login expiry), Gemini 4 Argon
 1013| (packet-fed, through the local web2api proxy); Fable 5.1 adjudicated pass 1 in the main loop (23:0x).  Pass 2: the same four.  F2: the
 1014| owner's 2026-11-04 00:5x roster -- the Opus 5.5 Agent seat, Grok, Gemini web (Argon), GLM 5.3, Astra.  DELIBERATELY NOT FIRED under those
 1015| rosters: agy, deepseek, minimax, kimi-k3 and the kimi CLI (their pass-1 answers, fired before the 12:0x ruling, stay on disk marked OUTSIDE
 1016| the roster; none was weighed in a ruling, and the twenty-one that section G found unrecorded at this landing were read then and
 1017| recorded -- see "Out-of-roster answers" below).  From the F2 ruling on, the Claude seats ran in Claude Code Cloud (owner 2026-11-04: cloud routines, not Agent seats): cloud Fable 5.1's F2 run and its F2P2R adjudication were stopped by safeguards -- two seat failures, recorded by name -- and Mythos 5.1 took both steps.  The repair's pass 2: Grok, GLM, cloud Fable, cloud Mythos, Argon; GPT-6 Astra walled until 2026-11-09 (a seat failure).  The regress review: cloud Fable 5.1.
 1018| 
 1019| **Assessed, not changed.**  `X(invalid)` (:241-245) is unreachable from a translated call on PPC (the generator's filler slots; no producer
 1020| emits the sign-extending-double index) -- the siblings brief's reading, accepted as an assessment, no row.  The bit-31 CPU-STOPs the
 1021| siblings sweep named are already filed: `ppccntlzwrc`, `ppcoeundec`, `ppcfpreservedrc`; the fetch exit is `qhslowifetch`; the stale-SRR0
 1022| row `ppcllscsrr0` is adjacent and not folded in (a different fix, a different oracle).  The rs6000 fork's d13a974 / 3c00042 are #216's
 1023| shape (already here) and 3dafe765 is `ppcllscsrr0`'s: NOTHING TO PORT, the research note's "nothing safe to copy" now has its reason.
 1024| 
 1025| **Assessed, not changed (F2R D3).**  The 32-bit ldarx/stdcx. forms: read by three file-reading seats (no width test at :4651-4653 or :4904-4910), not measured by this instrument; disclosed as #571 left primary opcodes 58 and 62.
 1026| 
 1027| **Filed, not fixed here.**  From F2R (7): the #216 comments' "raised a DSI" beside the new sentence (also the closing ruling's P10); the #216 returns' missing detecting variant; the 32-bit ldarx/stdcx. width question (noted on #571's disclosure, `ppc64on32gate`); `ppc_exception`'s SRR1 mask `0x87c0ffff`; the reservation keyed on the effective rather than the real address; MODE32 `reg()` reading a 64-bit gpr's high half on a big-endian host (Grok); the unsynchronised PC and stale SRR0 (`ppcllscsrr0`).  From the closing ruling: D2's harness row (gate 13 runs the two dead-binary legs and pins 14/83, 0/83, CONTROL=FAIL, census 0/35) and D1's INFO (a word count for `neg` no other session has).  From the regress review: the load-side address anchor (DATA and DATA2 hold one pattern), `std ok`'s free tail row, `ra r3 kept`'s note, and the `seed` rows' redundancy.  From the out-of-roster answers: the upstream CR0 comment's "bit 4" (on `ppcllsc216text`).
 1028| 
 1029| **Out-of-roster answers, read at landing.**  Section G refused the first commit attempt: the ledger cites the six 2026-11-03 pass-1 panel directories, and twenty-one answers in them were recorded nowhere -- the agy CLI (gemini-3.8-flash-high, file-reading) in all six, and deepseek-v4-pro:cloud, kimi-k3:cloud and minimax-m3:cloud in the five stage panels (their bug-review answers were already recorded).  All were fired before the owner's 12:0x roster ruling and none was weighed in a ruling; each was read whole and is recorded on the row.  Two findings, both records: (1) five of them (agy twice, deepseek, kimi-k3, minimax) flag the upstream store-conditional comment's "copied to to bit 4 of Condition Register Field 0" -- the code's 0x10000000 is CR0's fourth bit, bit 3 -- filed on `ppcllsc216text` with the #216 comments; (2) checking agy's S7 against the ledger showed the 32-bit ldarx/stdcx. item already carried by `ppc64on32gate`, #571's disclosure, so it is noted there as the F2 ruling directs instead of being filed as a new row.  Two packet-fed seats (kimi-k3, minimax) read the draft's third hunk as adding a failed-store reservation clear; HEAD already has it (:2345 before the fix), as agy, Grok and Astra read, and the shipped diff adds no such line.  The rest agrees with the shipped disposition or was settled by the rulings: the Program-interrupt proposals (deepseek, minimax) are refuted for the load pair by Book I 1.5.2 and are neither available nor required for the store pair (F2R D2); S7 is `qhslowifetch`; ncpus > 1 and unaligned EAs (Book II :1289 permits boundedly undefined results) are disclosed in the probe's contract; a `fatal()`-only variant reds gate 13's `PPC_LLSC_SYMPTOM=ABSENT` check.  The probe also gained its own `check_probe_wiring.py` MANIFEST entry (section R, which could not see the file while it was untracked).
 1030| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_579: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC579: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
