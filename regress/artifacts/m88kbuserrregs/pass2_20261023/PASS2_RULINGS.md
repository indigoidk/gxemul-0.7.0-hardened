# T36 (`m88kbuserrregs`, round `#570`) -- pass-2 review of the diff: the main loop's dispositions (2026-10-24 ~03:2x)

Evidence basis so far: FOUR reviewing seats answered on the diff -- GPT-6 Astra as reviewer (`codex_t36p2.txt`, 22,900 b),
Grok 4.7 (`grok_t36p2.txt`, 26,882 b), GLM 5.3 (`ollama_glm_t36p2_Q12.txt` 14,353 b + `_Q34.txt` 12,891 b), DeepSeek
(`ollama_deepseek_t36p2_Q12.txt` 5,699 b + `_Q34.txt` 3,050 b); all read whole.  Gemini 4 Argon is FIRING as this is
written (through agy, file-reading, `argon_agy_t36p2.txt`; `argon_transport_20261024.txt`) and its answer is added to
section E's basis.  Fable 5.1 HELD (`fable5.HELD.txt`).  agy (other than as the Argon transport), kimi, minimax, Opus-as-
seat DELIBERATELY NOT FIRED (`roster_NOT_FIRED.txt`).  Verdicts: Astra SHIP WITH CHANGES; Grok SHIP WITH CHANGES; GLM
SHIP WITH CHANGES (both firings); DeepSeek Q1-2 **DO NOT SHIP** (one claimed floor breach, D1 below), Q3-4 SHIP WITH
CHANGES.  **These dispositions are PROVISIONAL until GPT-6 Astra adjudicates them from `f2/packet.md`.**

## A. The executable diff -- SHIPS AS IS (all five readings; no executable defect, no floor breach)

* **A1** The four hunks are exactly the adjudicated repair A1-A7 as amended (codex:11-19, grok:11-17, glm-Q12:30,
  deepseek-Q12:9).  The include's presence is warranted by the compile need (the three macros live only in `m8820x.h`);
  its POSITION is not load-bearing and is NOT upstream's (upstream puts it before `m8820x_pte.h`) -- the product comment
  claims only "upstream adds the same include", which is true and sufficient (all five).
* **A2** The LUNA `return 0` skips an inert tail (the pre-zeroed read buffer); `default:` still stops the cpu (L22 measured).
* **A3** `dev_m8820x.c` is comment-only; the object is byte-identical (S21, measured).  Any further comment edit must keep
  the line count (`FAILURE()` embeds `__LINE__` at `:537`) and the object compare is redone.

## B. Comment sentences IN THE DIFF that are wrong records -- FIX BEFORE COMMIT (L4, comment-only, line counts kept,
## est/ mirrored, object compare redone, clearance re-run on the three build trees)

* **B1 (P2)** `dev_m8820x.c:361` cites `cpu_m88k.c:354-355`; the four added include lines moved that loop to `:358-359`
  (all five; confirmed by the main loop).  Same-width digit edit.  The regress-file citations that shift by the same four
  lines -- five into `cpu_m88k.c` (`diff_m8820x.c:996`, `diff_m8invread.c:161`, `luna_intmask_probe.py:23`,
  `m8820x_sites_probe.py:27`, `readiness_predicate_test.py:70`) and, found by Argon (`argon_agy_t36p2.txt:11`,
  confirmed: `case INT_ST_MASK0` HEAD `:813` -> `:817`), two into `dev_luna88k.c` (`luna_intmask_probe.py:2`,
  `m8820x_sites_probe.py:23`) -- SEVEN in all, are FILED as named citation debt, not swept (two are gate-run probes
  whose md5s the gate logs print; "do not apply an indiscriminate +4", codex:52; several were already stale at HEAD).
* **B2 (P1)** `memory_rw.c`'s "NO_EXCEPTIONS callers (the debugger) never get here" -- the operative claim is TRUE (the
  `:603` guard), the parenthetical is a false identity in both directions: the debugger's step pre-read is NOT suppressed
  and DOES reach the arm (R2 -- this round's own `ifetch` channel), and `dev_luna88k.c:613-614` is a non-debugger
  NO_EXCEPTIONS caller (codex:32, grok:45, glm-Q34:11; GLM-Q12:14 "not an L4, a one-word fix").  Reword: "NO_EXCEPTIONS
  callers (e.g. the debugger's dump) never get here; the test above keeps them out."
* **B3 (P4)** `dev_m8820x.c:326-333` folds the arm into the sentence counted "~10^5 times per boot" -- a count measured
  on the translation-fault writer only; the arm's count is unmeasured (codex:40,44; grok:49; glm-Q12:12; deepseek-Q12:21).
  Scope the count to `memory_m88k.c:382-405`'s writer; name the arm without a number.
* **B4 (D1)** `dev_m8820x.c:293-294` "the model writes only PFSR and PFAR" is literally false: the model also initialises
  IDR (`dev_mvme187.c:139,151`, `dev_luna88k.c:953,964`) (codex:39,230; grok:51).  Narrow to "the model's FAULT PATHS
  write only PFSR and PFAR".  (GLM-Q12:30 read "only" as still true over the added writer -- true of the fault path, which
  is what the narrowing says.)
* **B5 (P15 / M6)** `memory_rw.c:623-625` "A cpu without a CMMU gets no write and still takes the exception" asserts an
  observable consequence for BOTH access labels; `null route` scores delivery for the DATA label only, `null surv`'s want
  is delivery-independent, and under L9/L17 cpu 1 ends at `0xfff46010` (no instruction exception) while `null surv`
  stays green (the drafter's N1; all five seats confirm the missing observable).  E's survival ruling discharges the FLOOR
  cell (all five: no new row owed; codex:97, grok:96, glm-Q12:18, glm-Q34:12, deepseek-Q12:15 grades it L4).  The
  CLAIM -> ROW rule still applies to the sentence: narrow it in the diff -- "A cpu without a CMMU gets no write; the
  exception call is unchanged (the data-access delivery is scored by `null route`; the instruction label's delivery on a
  CMMU-less cpu is survival-only, not rowed)" -- and write the no-row sentence in the CHANGELOG beside the R1/R2
  re-root obligation.

## C. The detector and its floor -- DISCHARGED on (a)-(d); one claimed breach REJECTED (D1); records corrections owed

* **C1 clause (a)** measured at the probe: `prefix_HEAD.out` 21/31 PRESENT 10/10, `fixed.out` 31/31 ABSENT, the frozen
  witness 16/24 -> 24/24 (`fixed_witness24.out`).  **P8 record form:** "measured at prefix_HEAD.out (probe level); the
  gate block was inserted after propagation, so gate 14 never ran it pre-fix; its literal pins (`rows correct == 31`,
  `SYMPTOM=ABSENT` x1) would red that receipt by inspection -- not run."  NEVER the clause-(c) by-construction form for
  (a) -- that form is textually scoped to (c) (codex:75-80, grok:55, glm-Q12:22, glm-Q34:14, deepseek-Q12:33).
* **C2 clause (b)** L3 21/31 + 16/24, L4 29/31 + 22/24, each red for the reason under test (`luna route` green under L3
  because the HEAD arm still raises the exception; `luna pfsr` green under L4 because the case's own write is back).
* **C3 clause (c)** measured at `L5_stub.out` (1/31, CONTROL=FAIL, sentinel printed) and `L5b_absent.out` (no sentinel).
* **C4 clause (d)** every floor cell rowed with a channel that moves: data x present (L6b, L10-L15), instruction x present
  (L6: `ifetch pfsr/pfar/dcmmu`), data x absent (L8/L9: `null route`), instruction x absent (L8b: `null surv`), the
  `no_exceptions`-set cell (L7: `dbg noexc`), the served cell (`ok route`/`ok regs`, whose only reachable channel under
  a global widening is the prerequisite string -- L18 25 red, L19 27 red -- as the header now names).  27/27 MATCH.
* **C5 `ifetch route`** vacuous against L6 by disclosure; its own variant is L17 (red through the handler prerequisite).
* **C6 the one ask-again (R15), all seats' candidates, graded:** (i) the instruction x NULL DELIVERY (exception moved
  inside the NULL check for the instruction label only -- Grok AA5, Astra AA1): CLAUSE (e) under E's survival ruling,
  with the explicit no-row sentence (B5); (ii) a stepped instruction fetch at `0x3ffffff0` (Astra AA2, Grok AA4, P6):
  CLAUSE (e) -- the joint cell licenses no device/address products; owes a NOT-CLAIMED line (D3); (iii) LUNA store, VA !=
  PA (`PFAR = vaddr`), sub-word PFAR (`& ~3`): CLAUSE (e), already disclosed; (iv) a third cache class routed to the
  instruction side (GLM-Q12 AA1 `cache == CACHE_DATA ? 1 : 0`): CLAUSE (e) with the main loop's census -- the
  unsuppressed `CACHE_NONE` callers in the tree are `dev_ether.c:189` (test-machine DMA into RAM), `dev_lca.c:310,314`
  (Alpha), `dev_ps2_stuff.c:280,284` (PS2) and `promemul/arcbios.c` (MIPS); none is an m88k refusing-device access, so no
  caller reaches the arm with `cache == CACHE_NONE` unsuppressed on the two MC88200 machines (settling fact grepped
  2026-10-24 ~03:1x); (v) writes relocated into each device handler (GLM AA2), an extra write to a never-consulted
  register (GLM AA3), first-refusal-only writes (GLM AA4), writes on cpu-stopping refusals (GLM AA5): CLAUSE (e) --
  outside the repair's read set or outside A8's claim; L3 catches (v)'s first form anyway.
* **D1 -- DeepSeek-Q12:39,52's claimed FLOOR BREACH (L2): "CMMU-owner confusion" -- a variant that uses the bootstrap
  cpu's CMMU when the faulting cpu's pointer is NULL (`cpus[0]->cd.m88k.cmmu[sel]`), under which `null route` and `null
  surv` stay green.  REJECTED as a breach; CLAUSE (e).**  The (d) rule enumerates the predicates dominating the edited
  lines and operand swaps drawn from fields the guarded BODY reads; the joint-cell rule crosses them "EXACTLY WHEN THE
  GUARDED BODY'S OWN CODE DISTINGUISHES THEM" -- the body distinguishes `cmmu == NULL` from not, and nothing in it
  distinguishes WHICH cpu owns a CMMU; the variant is an ADDED fallback, not a weakening of an existing predicate.
  Astra reached the same grade from the other side (codex:142: "AA6 wrong-CPU CMMU selection ... CLAUSE (e); beyond the
  adjudicated CPU-independent cross-product").  Disclosed in the contract as coverage debt (a `null owner` row -- cpu 0's
  registers re-seeded by its handler and read back unchanged after cpu 1's two faults -- is buildable later; it is not
  owed by this diff).  The adjudicator is asked to rule D1 explicitly.

## D. Records -- what the CHANGELOG, OUTSTANDING_BUGS, ledger, header and gate comment must say (owed before commit)

* **D2 the shipped probe's header (frozen rev 2, md5 `d57c12ab`, N = 31):** FOUR sentences are wrong records or missing
  -- P3 "upstream's placement" (FALSE); P10 the R2-fixed behaviour worded as fact (source-derived prediction); P6 no
  NOT-CLAIMED line for a stepped instruction fetch at `0x3ffffff0`; F15 (glm-Q34:20) the named channels of `ok route`/
  `ok regs` (the operative channel is the prerequisite string).  P13 ("DATED PREDICTIONS ... UNTIL THE TABLE RUNS") is
  stale-but-true at freeze time.  **DISPUTE D2:** re-freeze (edit the SHIPPED copy's docstring, record both md5s, re-run
  the probe on the fixed and the HEAD binaries to show the 31 rows unchanged -- Astra codex:157, Grok grok:90) versus
  errata-only (GLM glm-Q12:8, glm-Q34:6 -- "do not edit the frozen header; byte identity is worth more").  **RULING:**
  one docstring-only re-freeze of the SHIPPED `regress/m88k_buserr_probe.py` (rev 2b) fixing P3, P10, P6, F15 and P13
  together; the measured rev-2 artifact (`table1_20261023/m88k_buserr_probe.rev2.frozen.py.txt`) is untouched and stays
  the instrument of record; rev 2b is run once on `/tmp/gxt36/work/gxemul` (31/31) and once on `/tmp/gxt36/base/gxemul`
  (21/31) to show the row logic unchanged; the CHANGELOG, the MANIFEST line and the gate receipt name BOTH md5s and the
  docstring-only diff (`table1_20261023/rev2b.docstring.diff`).  Reason: a committed detector whose header carries a
  known false sentence is a wrong record from day one, and the cost is seconds; GLM's objection is met by keeping the
  frozen artifact byte-identical.
* **D3 the gate comment (P14)** omits "unsuppressed" and the CMMU-less exclusion -- add both qualifiers in the live
  `gate_arm.sh` AND the staged copy identically (comment-only; the gate's md5 changes; record that gate 14 ran the pre-edit
  file `5ee94e61`, and do not re-run a 2.2-hour gate for a comment).
* **D4 the MANIFEST sentence** "kept as `*.py.txt` / `*.sh.txt`" is false while `staged/gate_arm.sh` keeps its `.sh`
  suffix (P12): rename the staged copy to `gate_arm.sh.txt` (Q19) and note the rename in `staged/README.txt`; the
  `.staged.diff`'s `+++` path text is left as written.  Qualify "27 of 27 measurements as predicted" with "(L22's
  prediction: BUILD_SPEC §11 Q18, dated before the leg)".
* **D5 PRETABLE / SCORES provenance (P5, P11):** PRETABLE.out is never edited (the order proof); a dated note
  `table1_20261023/PRETABLE_NOTE_20261024.md` records that L22's prediction lives at BUILDER_QUESTIONS Q18 /
  BUILD_SPEC §11 Q18 (mtimes 22:29 / 22:31, before the 23:08 leg), maps PRETABLE's draft question ids to the final ones,
  and notes AMENDMENT 1's self-stated time vs the file mtime; SCORES.txt gains one line saying the SYMPTOM column is cut
  at 60 characters and the leg `.out` files carry the full line.
* **D6 the CHANGELOG `#570` block** must carry: A8's claim and disclaimers verbatim (never "every 88K bus error", never
  "parity with MIPS"); HEAD's two wrongs (no generic-arm metadata; the LUNA case served the access and wrote the data
  PFSR for ANY access class); every score with its artifact and instrument revision (rev 2 `d57c12ab` N = 31; rev 1
  `d59798b0` N = 24; rev 2b's md5 once made); clause (a) in C1's form; (c) measured; the 20 variant builds + 7 other
  measurements = 27, L20 = L4 not run; the boot A/B at its ceiling (both reach `login:`, markers 1:1:1; instruction
  counts 7,651,336,103 vs 7,550,665,157, a difference of 100,670,946 with no base/base control -- NOT attributed; the
  logs do not show whether the boot touched `0x3ffffff0`); the NULL check's licence now MEASURED (L8/L8b, P9); R2 and the
  SFRZ/ERROR mechanism with the re-root obligation; the no-row sentence for instruction x NULL delivery; the `ok route`/
  `ok regs` channel correction (F15); the stepped-LUNA-fetch clause-(e) sentence (CL13); C5 withdrawn with E3; C4
  conditional, unmeasured; the include rationale with P3's erratum; all six builder departures (gate 14 as a 7974-s
  background job on `build/gxemul` 931e69fa; harness insertions after propagation; `.py.txt` checker copy; the pre-freeze
  smoke run; the rewrap; the include-position rationale).
* **D7 OUTSTANDING_BUGS** closes only the bounded metadata defect; files R1 (with the stepped rows' re-root obligation),
  R2, R3, C4-conditional, the five regress citations (B1) and the D1 coverage debt; marks C5 WITHDRAWN with E3's
  receipt.  **D8 ledger:** state `held`, the hold question from `fable5.HELD.txt`, witness
  `probe:regress/artifacts/m88kbuserrregs/witness_20261023/m88k_buserr_probe.py` (rung 3; implies no instruction-fetch or
  boot coverage), stage entries for `pass1_20261023/` and `pass2_20261023/` naming every seat's file, HELD and NOT FIRED
  entries distinct per seat, commits named in the follow-up.  **D9 commit scoping (glm-Q34:22):** the landing commits
  the HEAD-based staged `check_probe_wiring.py.txt` (the peer's 15 uncommitted lines excluded) and never the peer's
  files; `wt_after` merges restore the peer's lines.

* **D10 -- Gemini 4 Argon's answer (`argon_agy_t36p2.txt`, FIRED through agy, file-reading; SHIP WITH CHANGES; read
  whole).**  Adds: F1.3 the two `dev_luna88k.c` citations (adopted into B1); F5.2 PRETABLE `R-d`'s "pauses cpu 0" vs the
  probe's parked `br .` loop (adopted into D5's note and the CHANGELOG); F6 the ledger's pass-2 entry records Argon
  FIRED (D8); AA8/AA9 clause (e).  CHECKED AND REFUTED by the main loop: its P10 "sharpening" (that `ToBeTranslated`
  reads with `NO_EXCEPTIONS`, `cpu_dyntrans.c:309-310`) -- the real fetch `cpu_m88k_instr.c:2989-2990` and the display
  read `cpu_dyntrans.c:306-309` both pass `CACHE_INSTRUCTION` alone; its pre-fix red list and L6b score misread the
  artifacts (`prefix_HEAD.out`, `SCORES.txt`); its L5 description is not the builder's leg.  Its "acceptable" on P13/P14
  does not overturn D3 (cheap, comment-only).  Counted as the fifth reviewing seat of the F2 basis.

## E. ADJUDICATED by GPT-6 Astra, 2026-10-24 ~03:5x (`f2/codex_t36f2.txt`, 21,546 b): VERDICT AMEND -- "FIVE reviewing
## seats; uphold the executable repair and bounded floor, but correct the citation census, header-edit list, and evidence
## records.  No L2 breach established."  Where E differs from A-D, E rules.

**UPHELD:** A1-A3; B2-B5 (with E's exact B5 wording); C1-C5; D1 (`null owner` FILED under clause (e), NOT owed now --
"survival is a real channel, but proves neither instruction exception delivery nor preservation of another CPU's
registers"; file the gap and state it in the contract); D3 (P1 and P14 both corrected in place -- Argon's "acceptable"
rejected: naming control rows does not qualify the categorical opening sentence; the conditions are `!no_exceptions` and
selected `cmmu != NULL`); D4; D8-D9.  Least-certain upholds: D1 and B5/C4 (they rest on E's adjudicated boundary of the
NULL-cell obligation).

**AMENDED:**
* **B1 / D7 -- EIGHT shifted citation sites, not seven:** `regress/diff_m8invread.c:643` cites `dev_luna88k.c:926-957`
  (`add_cmmu_for_cpu`, HEAD `:934` -> working tree `:938`).  The eight: `diff_m8820x.c:996`; `diff_m8invread.c:161,643`;
  `luna_intmask_probe.py:2,23`; `m8820x_sites_probe.py:23,27`; `readiness_predicate_test.py:70`.  Separately,
  `regress/repro_m8sarpurge.c:14` still names the removed LUNA PFSR writer -- filed as HISTORICAL WRITER-CENSUS debt, not
  a ninth shift.  No instrument is swept; "do not copy replacement ranges indiscriminately; some citations were already
  stale".
* **D2 -- the re-freeze list corrected:** REMOVE F15 (the `ok route`/`ok regs` prerequisite channels are ALREADY explicit
  at probe `:118` -- GLM-Q34:20,41's diagnosis rejected; Astra-as-reviewer had seen the disclosure, codex_t36p2:113);
  ADD the probe's own "(the debugger)" parenthetical at `:45` (B2's counterpart), the explicit "instruction x NULL
  exception delivery has no scored row; survival is scored" sentence, D1's "preservation of another CPU's CMMU registers
  during a NULL-owning CPU's fault is not scored" disclosure, and P10 at BOTH `:152-155` and `:170-172`.  P13 is
  reworded as pre-table predictions subsequently compared with the measured table (incl. Q18's provenance for L22) -- it
  was valid when frozen and is not independently an L4.  The executable `REVISION = 2` at `:238` stays; the file is
  DOCUMENTATION revision 2b.  Record both complete hashes, the documentation-only diff, the verification that everything
  outside the module docstring is unchanged, and the two new pre/post receipts compared ROW BY ROW (not totals); the raw
  gate receipt (binary `931e69fa`, gate `5ee94e61`, probe `d57c12ab`) is not relabelled -- a dated provenance addendum
  beside it.  "The two reruns alone do not demonstrate every old mutation result or make the old gate receipt a rev-2b
  measurement; the verified documentation-only relationship supplies that justification."
* **D5 -- `SCORES.txt:4`'s criterion sentence itself is corrected** (add BUILD_SPEC §11 Q18) beside the truncation notice
  (regeneration unnecessary; measured lines preserved); the PRETABLE note makes explicit: R-d's "pauses cpu 0" and AM-7's
  "R-d stands" are SUPERSEDED (cpu 0 parks in `H`'s `br .` and stays running; the probe sends `pause 1`, never `pause 0`);
  CL7's `null route` mapping establishes DATA delivery only.
* **D6 -- the CHANGELOG describes the prerequisite channels as ALREADY disclosed, not newly corrected**; it conditions A8's
  claim on "the selected CMMU exists"; it carries both probe identities and the PRETABLE/SCORES provenance.
* **C6 -- two statements:** P6's disclosure points to D2 (not D3); "test-machine DMA into RAM" overstates `dev_ether.c:
  183-189` (the destination is guest-supplied) -- "a test-machine caller" is the census fact; machine applicability
  sustains the (e) grade.
* **Argon's findings (Q5):** F1.1/F1.2 confirm B1; F1.3 correct but incomplete (the eighth site); F2 confirm; F3 confirm
  (its own `CACHE_NONE` claim corrected: the pre-read passes `CACHE_INSTRUCTION`); **F4 REJECTED** (an unknown `k` does not
  keep `~10^5 + k` at `~10^5`; B3 stands); F5.1/F5.2 confirm (narrowed: `pause 1` IS sent); F6 confirm; F7.1 notice
  suffices; F7.2 rename; AA8/AA9 clause (e); P13 not independently L4; **P14 "acceptable" REJECTED**.  **P10: the main
  loop's refutation CONFIRMED** (`cpu_m88k_instr.c:2989` passes `CACHE_INSTRUCTION` without `NO_EXCEPTIONS`;
  `cpu_dyntrans.c:306-309` is an unsuppressed delay-slot display read); Argon's numbers (the pre-fix red list, L6b 20/31,
  the L5 description) are excluded from every record.
* **Astra's own adopted positions (Q4):** F9's blanket L4 label weakened (P13); AA6's rationale replaced ("CPU-independent
  cross-product" too loose -- the bounded read set, the body-induced partition and E's exclusion of CPU-number products
  are the grounds); the five-citation census (codex_t36p2:52) and the "Argon NOT FIRED" instruction (`:196`) WITHDRAWN.
* **No further mutation leg, boot pair or full gate is required** by these amendments, "provided the documented code
  equivalence and object identity hold" -- the probe reruns, the renewed object comparison and the refreshed clearance
  remain required; historical receipts retain validity for their original bytes.
