# GXemul hardened fork -- OWNER-DECISION DIGEST: 103 filed issues that wait on the project owner's call (a defensive project's queue triage)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork fixes
crash-on-malformed-input defects and keeps a ledger of every filed issue.  An earlier triage pass proposed, for each row below,
that it needs the OWNER's decision (not more engineering), with a one-line reason; some rows also carry the question they are
held for.  You cannot read files; work from these lines.  This is a DRAFT for the owner, not a ruling.

## The rows (id, state, severity -- the triage pass's reason | the row's own held question, both trimmed)

* `alphapcbbvirt` (open, sev med) -- A primary source check is required before designing a fix.
* `arcbiosubsan` (held, sev -) -- adjudicator executed a stale close despite a documented structural escape that proves a construction-rung witness insufficient.  | HOLD Q: REGRESS stage. The fix removed UB at ten uncast `buf[3]<<24` sites in arcbios.c and the witness is `construction:gate-9` (a freshly rebuilt instrumented tree: 2 UBSan left-shift lines on each of the five reaching SGI subtypes pre-fix, 0 pos
* `armbfcdecode` (open, sev low) -- architectural claim remains unverified against local manuals
* `armbfiwidth` (open, sev med) -- Await measurement of width-32 lowering before shipping.  | HOLD Q: `armbfiwidth` IS THE THIRD SITE OF AN IDIOM `#510` FIXED AT TWO, AND SIX SEATS AGREE ITS FORM DOES NOT TRANSFER -- so the question is not whether to fix it but WHAT THE ROUND MAY CLAIM.  SETTLED: UBFX/SBFX encode widthm1 so their width is n
* `asanstaletree` (open, sev med) -- needs ruling on whether to invalidate the ASan baseline with a sync
* `attrcheckgaps` (open, sev MED) -- The hold question actively asks for a decision on which control proves the tripwire.  | HOLD Q: Build FIRST the per-run resolution tripwire: every 7-40 hex ledger token must resolve to exactly one commit, or the gate fails (the flagship seat's ruling).  Which control proves it -- a synthetic two-commit shared prefix through the real m
* `b120r` (held, sev -) -- The row requires a guest measurement on luna88k before a round can proceed.  | HOLD Q: SCSI reports a length that can exceed what the guest asked for. The hold says 'offer as a rider in b120u's first panel'. QUESTION: does this need its own round, or does b120u's fix cover it? Be concrete: name a guest-observable consequence 
* `batterystandby` (open, sev MED) -- the remedy requires an owner decision regarding the machine's power policy.
* `bpstringarg` (open, sev LOW) -- Needs upstream deletion porting or a bespoke design.
* `briefforcedwrong` (open, sev low) -- modifying the artifact template affects future panels and requires owner decision.  | HOLD Q: Should the three-question set's `WHICH IS WRONG?  Assume at least one is' be softened to permit `none, and the forcing assumption is unwarranted' as a first-class answer?  It is a measured-effective adversarial device (it has found four wro
* `codexbriefscoping` (open, sev low) -- adjudicate whether section C5 remains in BRIEF_TEMPLATE.md
* `crimebankorder` (open, sev LOW) -- Waiting for a boot witness before modifying interleaved registers.
* `cxlaunchquotation` (held, sev LOW) -- held pending Fable's answer on V6/V7 passes to rule on the landed launcher  | HOLD Q: REVIEW (held 2026-10-18 by fableheldform; Fable walled on V6 and V7, 2026-10-17): regress/artifacts/cxlaunchland_20261016/v6pass/packet_cxland_v6_FABLE.md and v7pass/packet_cxland_v7_FABLE.md -- does the landed launcher (7aa2c41f) stand?  |
* `dashmissingd` (open, sev LOW) -- requires Q2 adjudicator ruling and owner weighing on a new entry-scoped token.
* `dashokclass` (held, sev LOW) -- Regress validation batched for Sunday flagship sign-off.  | HOLD Q: REVIEW (held 2026-10-18 by fableheldform; Fable walled on V7, 2026-10-17): regress/artifacts/dashokclass_20261016/v7pass/packet_dashok_v7_FABLE.md -- does the landing (dd2d4e01) stand?  ||  REGRESS (held 2026-10-17 at the dashokclass landin
* `devwritedata` (open, sev LOW) -- enumerate the 11 missing test sites  | HOLD Q: Audit, not a finding: of 151 `memory_writemax64(cpu, data' sites, 11 lack a MEM_READ / != MEM_WRITE test within the two preceding lines -- a correlate (the guard may sit further up).  Enumerate the 11 and say for each whether a WRITE can re
* `diagdivchained` (open, sev HIGH) -- The severity is disputed based on hypothetical vs. live harness failure rules and requires flagship arbitration.
* `diagdivtruncarg` (open, sev HIGH) -- The severity is disputed based on hypothetical vs. live harness failure rules and requires flagship arbitration.
* `diagdivunaryop` (open, sev HIGH) -- The severity is disputed based on hypothetical vs. live harness failure rules and requires flagship arbitration.
* `divratchetband` (open, sev -) -- Design choice between two-sided band or equality-with-ritual requires owner ruling.
* `fableheldform` (held, sev MED) -- question on the 2026-10-17 directive regarding closed rows with held questions  | HOLD Q: (held 2026-10-18; Fable 5.1 walled on this row's design pass at ~16:22, HTTP 429): (1) DESIGN -- regress/artifacts/fableheldform/design_20261018/packet_ASTRA.md: is option A right -- the walls and not-fired passes tokened HELD, the nine clo
* `fbclearread` (held, sev -) -- the hold question is a standing policy question that the provided text cannot answer.  | HOLD Q: RUNG-3 ATTEMPT DISCHARGED 2026-09-13: WITNESSED (regress/artifacts/fbclearread/rung3_20260913/).  QUESTION for the batched flagship close pass: does the rung-3 witness plus the shipped detector close this row, or is anything still owed (e.g
* `fbctrlcmdkill` (held, sev HIGH) -- Fable 5.1 walled, awaiting regression scores for #567  | HOLD Q: RESEARCH + REVIEW (Fable walled on #567's passes 1, 2, F2 and 3, 2026-10-18/19): the questions the other seats answered -- pass 2 (regress/artifacts/fbctrlcmdkill/pass2_20261018/packet_FABLE.md), F2 (pass2_20261018/f2/packet_FABLE.md) and p
* `fbsdramwrites` (open, sev LOW) -- Needs an owner call on implementing member 7 since no guest can validate it.
* `fiqenableread` (open, sev MED) -- choose which round to fold the FIQ fix into after datasheet confirm  | HOLD Q: Confirm against dc21285.txt Table 7-10 and the FIQEnable prose that +0x288 reads back the enable mask; if so, fold into the n6 ACCEPT round's sibling-parity or its own round?
* `gatebuildallow` (open, sev low) -- Owner must decide if the skipped gate lifts the LOW severity.
* `gateworktree` (open, sev med) -- whether to implement the narrower STAGED set check, as it changes commit requirements
* `gdromcondhow` (open, sev HIGH) -- Disputed HIGH severity regarding the live decline path explicitly awaits a flagship rule decision.
* `gdromdmaflood` (open, sev MED) -- disposition deliberately unchosen because silencing a success path might bury desired diagnostics.
* `ghostround` (open, sev -) -- Deciding how to wire the ghost round checker into precommit alters commit requirements.  | HOLD Q: FOR THE OWNER (2026-11-06): Wire `check_ghost_rounds.py` (default: a round block's header-named and `in work` rows must be closed or name the round; cutoff 2026-11-05) into precommit_check.sh as a soft section, a hard section, or not at all
* `guestloopdenial` (open, sev LOW) -- requires policy ruling on whether capping an explicit 16M hardware contract violates emulation fidelity
* `i8259eoiirr` (held, sev MED) -- requires owner ruling on roster seats, Fable hold, and filing of Argon's answers  | HOLD Q: OWNER RULING OWED (2026-10-25): (1) the two stages hold the roster's answering seats (Astra adjudicating, Grok, GLM, DeepSeek); kimi, minimax and the Opus review seat DELIBERATELY NOT FIRED under your roster (the `rosterexcused` question); 
* `i8259icwmask` (open, sev LOW) -- Needs owner ruling on whether to clear ier and expose latched requests.
* `ip30abortkill` (held, sev HIGH) -- blocked on missing Fable closure measurement  | HOLD Q: CLOSURE REVIEW (held 2026-10-18; Fable 5.1 tried once on the closure check and walled, HTTP 429; the owner's 2026-10-17 Fable hold): (1) does ip30abortkill's close stand -- #531's floor on the shipped 33-row instrument measured (clause (a) 
* `jazzvecreopen` (open, sev LOW) -- Waiting for Fable to adjudicate the follow-up round on the conditional deassert guard
* `landiskintc` (open, sev med) -- severity/relevance requires reading SH7751R manual to see if missing extended block matters.
* `lcaconfbit1` (open, sev LOW) -- Cannot proceed without HRM specifications on guest-visible return values.  | HOLD Q: HRM S6.2.9: IOC_CONF<1:0> 00/01 are type-0/type-1 config cycles; 10/11 are not configuration-cycle types.  Should lca_pci_conf decline (or bus-abort-model) accesses while CONF bit 1 is set, and what guest-visible value should a declined con
* `lecsrmask` (held, sev MED) -- requires owner ruling on roster seats, Fable hold, and unmeasured variant table  | HOLD Q: OWNER RULING OWED (2026-10-25): (1) the two stages hold the roster's answering seats (Astra adjudicating, Grok, GLM, DeepSeek; Argon's web-route pass-1 answer); kimi, minimax and the Opus review seat DELIBERATELY NOT FIRED under your roster
* `ledgerboiler` (held, sev -) -- owner ruled against re-harvesting the 52 rows, preserving original seat files.  | HOLD Q: OWNER DECIDED 2026-09-13 (default adopted by owner leave, reversible): NO re-harvest of the 52 archived rows' seat entries.  The forward-only check stands; the seat files remain under _scratchpad/panel_*/ for any row that later needs its re
* `ledgerstatelies` (open, sev -) -- ~50 mis-stated instances found across 5 classes, but owner must rule on priority and scope of the correction round.  | HOLD Q: The SEMANTICS half is discharged (state_semantics written, owner-ratified 2026-08-25, all five observed states documented against a 270-row census).  The other half -- ~50 mis-stated instances across five classes -- is NOT, and it is its ow
* `lunancpus3` (open, sev low) -- the closure strategy relies on an assumption that must be tested on the simulator first.
* `m5dayb` (open, sev LOW) -- Needs a tie-breaker between fable5 and glm on adding the optional 23rd test case.  | HOLD Q: Add M5a0 and raise precommit's selftest pin 22 -> 23, or keep the stamped-date gap disclosed as it is?  (fable5: optional, not owed.)
* `m88kexchwtraps` (open, sev low) -- The manual is silent on the behavior, requiring a design decision on whether to deliver or decline.
* `m88kfpprivvector` (held, sev LOW) -- Conflicting Motorola manual entries require an authoritative source to resolve.  | HOLD Q: Held per the R32 adjudication (Fable DROP, Astra HOLD, Argon HOLD; ASTRA_VS_FABLE.md section 2, section 4 item 5, section 6): is a user-mode fldcr/fstcr/fxcr of fcr1-fcr61 architected as the privilege-violation vector 6 the model takes, or 
* `m88ktbnd` (open, sev low) -- the issue requires the owner to determine and name the specific path before it can be ranked or closed.
* `m88kunclaimedberr` (open, sev LOW) -- Awaiting hardware documentation to confirm BERR behavior.
* `m8probe` (held, sev -) -- Awaits batched flagship close pass due to unmeasured NetBSD/MP reachability and lack of manual.  | HOLD Q: m8820x PROBE_USER/PROBE_SUPER are dropped, so SSR answers a deterministic miss. The hold says no measured guest issues probes and it needs the translation walk. QUESTION, two parts. (a) REACHABILITY: is there any in-tree guest that issues a
* `makercfalse` (open, sev -) -- verdict provisional pending mandated roster quorum  | HOLD Q: Cause is now MEASURED (wsl -- bash -c drops $? and $VARS even single-quoted; escape or use a script file) and was already recorded in nightly_battery.sh's header on 2026-08-17 and in af4884c on 2026-08-20, both predating this row. THREE QUE
* `mapledmaaddr` (held, sev high) -- closure is recorded but REGRESS hold question requires flagship test verification.  | HOLD Q: REVIEW (held 2026-10-18 by fableheldform; Fable was not fired on the closure check, having walled that morning): regress/artifacts/mapledmaaddr/close_20261018/packet_close528_ASTRA.md -- may the row close: #528 finished on 2026-09-12 and no
* `mapledmahang` (open, sev MED) -- the loop bound is a design question and is not derivable from the tree
* `mipsbc1ccstop` (held, sev LOW) -- The outcome of nonzero cc on ISA I-III is not settled by the cited manuals.  | HOLD Q: Question (held per the R78 adjudication): find an applicable MIPS I-III rule, erratum or hardware measurement for the outcome of a nonzero cc field in BC1 on ISA I-III; the MIPS32 UNPREDICTABLE rule is not enough (cpu_mips_instr.c:5057-5066
* `mipsextshift` (open, sev med) -- repairing undefined negative shifts on invalid encodings requires a panel design decision.
* `mipsisa2cop3ls` (held, sev LOW) -- owner must rule on the filing bar for a -C-only CPU  | HOLD Q: Question (DISPUTED, owner's filing-bar call, to be aligned with the ppcmulhwreserved/m88kaluignored reserved-encoding bar): is a reserved/unusable-encoding defect on a -C-only CPU with no default machine worth its own row? (cpu_mips_instr.c
* `mipstiny` (open, sev MED) -- contradiction between Astra's resolution and the lack of counter-argument review requires flagship seat adjudication.  | HOLD Q: The fork's own comment and the reviewing seat give OPPOSITE readings of the same MIPS sentence, and both are reasoned.  Which is right: is IEEE/MIPS after-rounding tininess judged on the value rounded to the destination PRECISION with an UN
* `mtesrcfill` (open, sev LOW) -- Clarification of hardware behavior is needed to determine the correct semantics.
* `mtestartread` (open, sev LOW) -- Requires hardware documentation to rule if a read starts the engine.
* `n3` (held, sev -) -- verify the two defences cover the traced sequence, then close
* `ofopenexit` (open, sev HIGH) -- The Argon scoping proposes a DECLINE + latched announce strategy requiring ruler approval.
* `ofpeerexit` (open, sev HIGH) -- The Argon scoping proposes an ACCEPT strategy (return 0 with guarded deref) requiring ruler approval.
* `panelshrefused` (held, sev LOW) -- owner must rule whether to bypass the never-commit policy  | HOLD Q: panel.sh is on the never-commit list (it carries unreviewed deltas): may this fix land as its own reviewed commit of panel.sh, or must it wait for those deltas to be reviewed first?
* `pitlatch2` (held, sev -) -- Requires external datasheet to confirm latch behavior.
* `ppcdivwhostdiv` (held, sev HIGH) -- held for owner input on HOST band classifier  | HOLD Q: Owner question (CHECKPOINT 2026-11-02, decision 1/2): how are HOST-band rows (where the emulator process can end) to be witnessed and worked under the main-loop classifier? The whole RANKED_OPEN_v3 HOST band shares this witness shape and th
* `ppcfpreservedrc` (held, sev LOW) -- Owner must explicitly prioritize either Book I compliance or the strict detector property.  | HOLD Q: Owner question carried from the N10 adjudication: keep the stop on fcmpu/mcrfs bit 31, or treat bit 31 as ignored per Book I (cpu_ppc_instr.c:5443-5450; CHANGELOG.md:36652)? A fix must keep the detector property that a case which forgets to
* `ppcgateimageskip` (held, sev med) -- needs testing/reading gate_ppc.sh to answer if probe blocks run before need_file.  | HOLD Q: REVIEW (held 2026-10-18 by fableheldform; Fable was not fired on the #527 closure check, having walled that morning): regress/artifacts/ppcrlwimiwidth/close_20261018/packet_close527b_ASTRA.md, as corrected by packet_close527c_ASTRA.md -- ma
* `ppcmtdcrnop` (held, sev LOW) -- Needs architectural direction from the owner since no DCR state currently exists to mutate.  | HOLD Q: Held per the N8 adjudication (Fable FILE, Astra HOLD, Argon HOLD; ASTRA_VS_FABLE.md section 2 and section 6): which supported configuration has a writable PPC405GP DCR, and what model state must a write change? And what must the case 0x1c3 
* `ppcprogvector` (open, sev MED) -- owner decision 9 defers the missing program exception vector to a separate round.
* `ppcrlwimiwidth` (held, sev high) -- Awaiting flagship review and REGRESS scores.  | HOLD Q: REVIEW (held 2026-10-18 by fableheldform; Fable was not fired on the #527 closure check, having walled that morning): regress/artifacts/ppcrlwimiwidth/close_20261018/packet_close527_ASTRA.md -- is anything still owed before ppcrlwimiwidth a
* `ppcshiftwide` (open, sev high) -- Waiting on owner's call regarding the witness block reach.
* `ppcsrdmissing` (open, sev high) -- Waiting on owner's call regarding the witness block reach.
* `pristinesecondref` (open, sev LOW) -- non-defect records request; requires maintainer ruling
* `probewiringheredocstrip` (open, sev HIGH) -- A RULE QUESTION for the flagship regarding severity.
* `probewiringinterpopt` (open, sev HIGH) -- A RULE QUESTION for the flagship regarding severity.
* `ptyprobepins` (open, sev MED) -- precommit hook needs a ruling on whether to check staged vs working tree.
* `pvrdepth2bpp` (open, sev LOW) -- requires a ruling on whether other probes overlap body-read fields.
* `secstalebinary` (open, sev LOW) -- Deleting untracked files requires the owner's call.
* `sgiat1count` (open, sev HIGH) -- requires flagship ruling on HIGH severity policy when a preventative check misses a class without a live instance.
* `sgideprimbitslive` (open, sev HIGH) -- The severity is disputed and explicitly flagged as a rule question for the flagship reviewer.
* `sgilinearnegidxpostmortem` (open, sev low) -- three rule questions regarding premise-audit, template line, and C5 refusal delay.
* `sgilwreadzero` (open, sev HIGH) -- The severity upgrade is disputed and explicitly flagged as a rule question for the flagship reviewer.
* `sgirandomcolour` (held, sev high) -- regress hold is unsettled awaiting seat execution  | HOLD Q: REVIEW (held 2026-10-18 by fableheldform; Fable walled on the closure-records review's pass 1 and was not fired on pass 2): regress/artifacts/sgirandomcolour/closure_20261018/packet_rc_FABLE.md and the delta, packet_rcd_ASTRA.md -- do the 7
* `sgirandomskipput` (open, sev med) -- general fix collides with a shipped oracle, requiring explicit contract adjudication.
* `sgirekills` (held, sev high) -- held for flagship to review #564 regress scores and pending seat answers.  | HOLD Q: RESEARCH + REVIEW (held 2026-10-18 by fableheldform; Fable walled on #564's passes 1, 2 and 3, 2026-10-17/18): the questions the other seats answered -- pass 1's design (regress/artifacts/sgirekills/pass1_564_20261017/packet_564p1_FABLE.md)
* `sgirespanchk` (open, sev HIGH) -- need to know if callers can present unaligned/oversized spans
* `sgitileptrsilent` (open, sev low) -- sibling parity exposes asymmetry but does not dictate closing it without design ruling.
* `sh4bsclane` (held, sev -) -- Unknown SH-4 hardware behavior requires external manual.
* `sh4dmacnote` (open, sev LOW) -- Needs a rung-3 probe to determine if the generic path actually transfers.
* `sh4frqcr` (open, sev low) -- Judgment call on whether the bare latch matters.
* `sh4testclock` (open, sev -) -- Conflicting needs between testing TMU paths and preserving the missing-clock regression test.
* `shfpprreserved` (open, sev LOW) -- A policy decision is required for handling SH-4 undefined operations
* `shoddprfield` (open, sev LOW/HIGH (disputed)) -- Needs ruling on out-of-bounds struct access severity
* `shsyncofeature` (open, sev LOW) -- requires owner to decide on adopting the NOP
* `smfalsegreen` (held, sev -) -- implement refusal of subjects inside the harness's own directory  | HOLD Q: OWNER DECIDED 2026-09-13 (default adopted by owner leave, reversible): selfcheck refuses subjects inside the harness's OWN directory only, not every non-src subject.  Reason: the narrower refusal removes the false-green case measured withou
* `untokenedanswers` (open, sev MED) -- blocked on owner ruling for roster exclusion recording.  | HOLD Q: [ANSWERED 2026-11-06 by Fable 5.1: the flagship's discriminator question -- the recorder's declaration read as a token (the review entry; regress/artifacts/holdphase/ruling_20261106/RULING.md, Q2).]  STILL THE OWNER'S, and not blocking the 
* `vgadirtyarm` (open, sev HIGH) -- flagship must adjudicate disputed HIGH severity regarding unmeasured redraw time.
* `vmedefaultkill` (held, sev high) -- held on policy question about roster waivers only the owner can rule on.  | HOLD Q: RESEARCH + REVIEW (held 2026-10-21 at #568): the owner's 2026-10-20 roster fired FOUR seats (Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3); opus5, agy, kimi, deepseek and minimax were deliberately not fired and their entries carry the non-answ
* `warnnotfail` (held, sev -) -- distinguish working tree deletion (fail) from fresh clone (warn)  | HOLD Q: OWNER DECIDED 2026-09-13 (default adopted by owner leave, reversible): a precommit checker MISSING from a working tree FAILS; missing from a fresh clone (no .git history of it) WARNS.  Reason: deletion in a working tree is the failure the c
* `wdcbeoddtail` (open, sev med) -- Defect verified, but requires project owner to select from 3 distinct fix paths
* `wdcchildstatus` (open, sev HIGH) -- flagship must answer rule question on HIGH grading for preventive check missing a severe class.
* `wdciordybit` (open, sev LOW) -- must be decided alongside wdclbaadvertise
* `wdclbaaddr` (held, sev HIGH) -- procedural ruling on roster-excused seats required.  | HOLD Q: OWNER RULING OWED (2026-10-25): the pass-1 and pass-2 stages hold 6/9 seat answers plus the Fable 5.1 answer delivered through the Claude Code cloud route (RATIFY WITH CHANGES, applied); kimi, minimax and the Opus review seat were DELIBERAT
* `wdcrstbitonly` (open, sev LOW) -- missing the required offset-0 test row writing 0x0a or 0x02 to prove the defect.  | HOLD Q: Add an offset-0 row writing a NON-ZERO, RST-CLEAR byte (0x0a or 0x02) to the malta wdc_altdigin instrument (which already has a table) and show `if (idata)' reds it.  Cross-machine; not landisk's.
* `wirereassign` (open, sev HIGH) -- The flagship reviewer must rule on the severity definition for static checker defects.
* `witnesssilent` (open, sev low) -- owner must dictate policy on requiring expected post-fix scores.

## What to return

Group the rows into THEMES -- decisions that, once made, settle many rows at once (for example: a policy for all rows of one
kind, a tooling question, a seat or roster question, an accept-the-debt question).  For EACH theme give:
1. the decision in one sentence, phrased as a question the owner can answer;
2. the options (two to four), with the cost of each in a phrase;
3. a RECOMMENDED default and why, in one sentence;
4. the row ids it settles.
Then list any row that fits no theme, with its own one-line question.  Order themes by how many rows they settle.
Every row id above must appear exactly once.

End with one line: `OWNERDIGEST: <t> THEMES, <n> ROWS PLACED, <s> SINGLETONS`.
