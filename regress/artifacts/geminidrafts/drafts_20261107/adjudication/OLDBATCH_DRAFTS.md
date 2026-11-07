# OLDBATCH_DRAFTS.md -- Gemini web's ADJUDICATION DRAFTS for the oldest open/held ledger rows (proposals for Fable, never rulings)

Built by mk_oldbatch.py from HEAD's ledger (rows ordered by the earliest date in the row; asanstale and gateflr skipped as
ruled-and-held-for-Mythos).  One line per row: Gemini's proposal, then the main loop's note.  A proposal is not acted on until the
flagship rules it; the main loop's note says only what it checked.

## batch 0 (cbba52c0) -- `oldbatch_0/gemini_web.out` (3,584 bytes; the bank's exit 1 = Gemini closed on the packet's own OLDBATCH line, not the job tag)

* ROW netmacdup: FILE -- Unreproduced research finding with a flawed existing patch.
* ROW citestale: DROP -- Previously adjudicated and rejected on measurement.
* ROW srclistsubdir: FIX-NOW -- Known trivial fix to the find command in the carrier.
* ROW secstalebinary: OWNER-DECISION -- Deleting untracked files requires the owner's call.
* ROW bugfilereverse: FILE -- Live issue that was scoped but deliberately not built in this session.
* ROW auditmap: DOCUMENT-AND-CLOSE -- Dashboard behavior was explicitly grandfathered by owner decision.
* ROW b101: DOCUMENT-AND-CLOSE -- Assessed and proven safe structurally; not a defect.

Main-loop note: `srclistsubdir`'s FIX-NOW is a carrier (CLAUDE.md) text edit -- carrier edits are the owner's, and tools/CLAUDE.md is never committed from this session, so it is OWNER in practice.

## batch 1 (cbba52c0) -- `oldbatch_1/gemini_web.out` (3,731 bytes)

* ROW b115: FIX-NOW -- a guest path exists, so the rung-3 attempt did not clear the issue.
* ROW b118: FILE -- host-only initialization issue out of bounds for guest exploitation.
* ROW b120: FIX-NOW -- requires explicit check condition return for unknown SCSI commands.
* ROW b122: FILE -- host-only parsing error, inaccessible to guests.
* ROW b126: FIX-NOW -- re-pin the test, then apply the one-line heuristic fix.
* ROW b1w: DOCUMENT-AND-CLOSE -- the remaining gaps were successfully split into new rows.
* ROW constblind: FILE -- harness debt that is unreachable by the guest.

Main-loop note: **`b115`'s FIX-NOW is WRONG** -- the row carries commit `00d546d` (its fix shipped) and its hold_question is a question for the batched flagship CLOSE pass about its rung-3 witness (`regress/artifacts/b115/rung3_20260913/`); what is owed is that answer, not a fix.

## batch 2 (cbba52c0) -- `oldbatch_2/gemini_web.out` (4,518 bytes)

* ROW evdeadarchive: FIX-NOW -- re-point the 297 fields at the real panel dirs and copy under regress/artifacts/
* ROW fbmode: FILE -- expand the item to include external-event handling and mask bits
* ROW hlen: CLOSE-OVERTAKEN -- the three rows grinding through the class have largely shipped their fixes
* ROW i8253zero: FIX-NOW -- hoist timer update into a helper and map count 0 to 65536
* ROW mrwstore2: DOCUMENT-AND-CLOSE -- manual permits partial execution so the divergence risk is refuted
* ROW n1: FILE -- needs a rung-3 witness attempt on evbmips -e malta before any fix
* ROW n3: OWNER-DECISION -- verify the two defences cover the traced sequence, then close

Main-loop notes: `i8253zero` (held, no commit) and `pit8253count0` (open, filed by #574: a zero count maps to a timer that never fires within a run) look like ONE defect -- a possible DUPLICATE for the flagship.  `mrwstore2` carries commit `0447c2e` and a hold_question saying it was REPRODUCED at rung 3 then re-ranked down -- a reproduced row is not closed by documentation alone; the question needs its answer.  `hlen`'s CLOSE-OVERTAKEN needs the carrier's three conditions (a discriminating control measured at HEAD, the carrying rows named, the control preserved durably) -- none is in the draft.

## batch 3 (cbba52c0) -- `oldbatch_3/gemini_web.out` (4034 bytes) -- NOT YET CHECKED by the main loop

* ROW optrow: CLOSE-OVERTAKEN -- The row's work shipped and the tool's blind spot was corrected.
* ROW pcheck: FILE -- Bare names and .py paths remain invisible to the pre-commit hook's section C.
* ROW pit8253bcdbinary: FILE -- BCD decoded as binary causes host timer drift, but no known guest triggers it.
* ROW pit8253lsbnotimer: FIX-NOW -- The model incorrectly keeps stale bytes in both one-byte arms against the datasheet.
* ROW seam: DOCUMENT-AND-CLOSE -- The original divergence is fixed at HEAD, leaving only coverage debt.
* ROW stateaudit0923: CLOSE-OVERTAKEN -- The audit's required holds and exemptions were wired by subsequent commits.
* ROW strad: DROP -- The assessor explicitly ruled to drop strad as currently filed.

## batch 4 (cbba52c0) -- `oldbatch_4/gemini_web.out` (5522 bytes) -- NOT YET CHECKED by the main loop

* ROW fbvolatile: DOCUMENT-AND-CLOSE -- 'assessed, not covered' property requires load-sensitive test, explicitly recorded with no filing needed.
* ROW ledgerstatelies: OWNER-DECISION -- ~50 mis-stated instances found across 5 classes, but owner must rule on priority and scope of the correction round.
* ROW m8invpred: DROP -- unanimous drop for a row whose only residual value is a lesson already recorded in the carrier.
* ROW m8probe: UNSETTLED -- codex research refuted the 'no in-tree probes' premise and marked it NEEDS-MEASUREMENT.
* ROW armbdt: CLOSE-OVERTAKEN -- commit 4dfc716 fixed it locally, pending re-run of gate_arm.sh at pin 43 and closure records.
* ROW b120r: UNSETTLED -- codex identified a consequence b120u wouldn't repair but requires a luna88k guest measurement before proceeding.
* ROW dfreq: DOCUMENT-AND-CLOSE -- stopping rule invoked because the witness does not reproduce the defect and a guest witness is outstanding.


## batch 5 (cbba52c0) -- `oldbatch_5/gemini_web.out` (4157 bytes) -- NOT YET CHECKED by the main loop

* ROW ip30abortkill: OWNER-DECISION -- blocked on missing Fable closure measurement
* ROW killartifacts: DROP -- explicitly folded into killdriverunTracked
* ROW killdriverunTracked: FILE -- harness work ranked below live defects
* ROW ledgerclosureby: FILE -- schema change deferred to state_semantics ratification
* ROW makercfalse: OWNER-DECISION -- verdict provisional pending mandated roster quorum
* ROW queueunrated: FILE -- requires read-only rating pass
* ROW lunafuse: FILE -- requires writing a non-trivial byte-merge helper without breaking setup

Main-loop note on batches 3-5 (23:4x): **`armbdt`'s CLOSE-OVERTAKEN mislabels it** -- `4dfc7165` IS the row's own round, #524 ("#524 (armbdt): an ARM block transfer through a cold host page ..."), and the row carries it in `commits`; nothing overtook it.  Like `b115`, what it owes is its held stage's answer, then closure by its own round.

## batch 6 (cbba52c0) -- `oldbatch_6/gemini_web.out` (3840 bytes)
* ROW rtcflood: FILE -- testmachine-only with no guest-visible harm, blocked on detector gap.
* ROW rtcstale18: FILE -- blocked on embargo and needs runtime measurement of rows to verify staleness.
* ROW scexempt: FILE -- ieee_store exemption was re-dated to 2026-12-10 by owner ruling.
* ROW smdatefmt: CLOSE-OVERTAKEN -- fix already shipped in tree silently, needs date handling confirmation before closing.
* ROW floodclass: FILE -- pending codex measurement of 68 device files with unlatched fatal().
* ROW isaorder: FIX-NOW -- use the pic1 fix idiom from 15 lines above to properly sequence the device_add.
* ROW ledgerboiler: OWNER-DECISION -- owner ruled against re-harvesting the 52 rows, preserving original seat files.

## batch 7 (cbba52c0) -- `oldbatch_7/gemini_web.out` (3366 bytes)
* ROW m88kexit: DOCUMENT-AND-CLOSE -- Not a live defect; sites are unreachable without code change.
* ROW pit8253flood: FIX-NOW -- Latch :342 to prevent unbounded fatal.
* ROW pitcount: FILE -- Model lacks decrementing count but the consequence is just a readback gap, not a hang.
* ROW pitlatch2: OWNER-DECISION -- Requires external datasheet to confirm latch behavior.
* ROW rtcbranch: FIX-NOW -- Add fatal_calls counter to assert 0 in the detector.
* ROW rtclen: FILE -- Test defect where the stub ignores len, hiding a fatal remove.
* ROW sh4bsclane: OWNER-DECISION -- Unknown SH-4 hardware behavior requires external manual.

## batch 8 (cbba52c0) -- `oldbatch_8/gemini_web.out` (5081 bytes)
* ROW sh4markspell: FIX-NOW -- teach the census to accept the _mark idiom used in other probes
* ROW sh4partialread: FILE -- keep as a design improvement rather than a bug, severity -
* ROW smfalsegreen: OWNER-DECISION -- implement refusal of subjects inside the harness's own directory
* ROW smsetuprow: FILE -- keep as mitigated apparatus debt, severity -
* ROW stalecopies: DOCUMENT-AND-CLOSE -- documentation gap, files were already moved out
* ROW warnnotfail: OWNER-DECISION -- distinguish working tree deletion (fail) from fresh clone (warn)
* ROW wdcoracle: FILE -- keep as a live design constraint for wdcnoirq/wdcflood

## batch 9 (cbba52c0) -- `oldbatch_9/gemini_web.out` (4569 bytes)
* ROW witnessunwired: FIX-NOW -- add a warning-level script check for file existence and at least one gate reference.
* ROW arcbiosubsan: OWNER-DECISION -- adjudicator executed a stale close despite a documented structural escape that proves a construction-rung witness insufficient.
* ROW arcbioswalk64: FIX-NOW -- correct the walker's offset from 0x34 to 0x40 so it reads IdentifierLength instead of AffinityMask.
* ROW bscunwired: FIX-NOW -- wire the probe into a gate, matching the template used for #443.
* ROW ctorabortclass: FIX-NOW -- fix the interrupt_handler_lookup abort now that #446 has shipped and unblocked it.
* ROW fbclearread: OWNER-DECISION -- the hold question is a standing policy question that the provided text cannot answer.
* ROW fbdisabled: FIX-NOW -- guard the timer accrual path with an enable check.

## batch 10 (cbba52c0) -- `oldbatch_10/gemini_web.out` (3168 bytes)
* ROW killedreports0: FILE -- A killed battery reported success because the exit code was masked by a pipe to tail.
* ROW m8lanecomment: FIX-NOW -- Update the lane comment to include memory_m88k.c to prevent future misattribution.
* ROW m8saprspy: FILE -- File as a shape pin to address callback-pointer blindness in the SAPR/UAPR arm.
* ROW nulheredoc: DOCUMENT-AND-CLOSE -- The symptom is gone and mechanically guarded.
* ROW pcicmergeA: DOCUMENT-AND-CLOSE -- No row was created because it would have cemented the defect, which is documented.
* ROW queuesubstr: DOCUMENT-AND-CLOSE -- The substring matching defect was found and fixed immediately.
* ROW sectionEnarrow: FIX-NOW -- Widen the precommit check E selector to include probes and rename the scope message.

## batch 11 (cbba52c0) -- `oldbatch_11/gemini_web.out` (3726 bytes)
* ROW sh4dmanop: FILE -- keep open but RE-TITLE to name the no-op itself
* ROW sh4latchcollide: FILE -- keep to document the fragility of the latch classes
* ROW sh4pcicvoid: DOCUMENT-AND-CLOSE -- recorded as a proof gap, not a defect in the fix
* ROW sh4rtcflags: FILE -- fixing requires advancing the counter, not just setting the flag, so it remains open debt
* ROW smcovered12: FILE -- records defect to correct when selfcheckman is dequeued
* ROW stdbufasan: DOCUMENT-AND-CLOSE -- already documented and fixed in-tree in three places
* ROW hpcshcpu: DROP -- cannot settle without an external SH3/SH4 identity source

## batch 12 (cbba52c0) -- `oldbatch_12/gemini_web.out` (3656 bytes)
* ROW sh4itlbpr: DOCUMENT-AND-CLOSE -- Architectural manual permits returning 0x20.
* ROW sh4sqwrite: FILE -- Confirmed fidelity gap (store bypasses MMU) but latent with no known guest dependency.
* ROW sh4tlbda2: DOCUMENT-AND-CLOSE -- The round is successfully discharged and constraints independently confirmed.
* ROW shprotld: FILE -- Confirmed coverage debt requiring a build queued behind the embargo.
* ROW gatebuildallow: OWNER-DECISION -- Owner must decide if the skipped gate lifts the LOW severity.
* ROW gdromdmawidth: DOCUMENT-AND-CLOSE -- Proposed fix would break booting Linux; assessed-not-changed.
* ROW gdromkeyindex: CLOSE-OVERTAKEN -- Core detector escapes overtaken by commit 7c9dd9e.

## batch 13 (cbba52c0) -- `oldbatch_13/gemini_web.out` (3179 bytes)
* ROW outcomegap: FIX-NOW -- Fix the empty ev field and date in r421.
* ROW probetimebased: FIX-NOW -- Apply ENUMERATE-FIRST + RATCHET in gate_hygiene.
* ROW sh4cpudevscope: FILE -- Product ownership defect, reachability holds it at low.
* ROW sh4frqcr: OWNER-DECISION -- Judgment call on whether the bare latch matters.
* ROW sh4iprunpinned: FILE -- Coverage debt, delivery consequences dormant.
* ROW sh4irlm: FILE -- Missing functionality, feature not a repair.
* ROW sh4pcic15: FILE -- Latent defect, loop bound wrong but no guest access.

## batch 14 (cbba52c0) -- `oldbatch_14/gemini_web.out` (3852 bytes)
* ROW sh4pclockquiet: FILE -- Coverage debt for timer 2 and diagnostic checks needs to be recorded and addressed.
* ROW sh4standinglower: FILE -- Valid coverage debt (detector gap) where a requested priority lowering is untested, though current code handles it.
* ROW sh4testclock: OWNER-DECISION -- Conflicting needs between testing TMU paths and preserving the missing-clock regression test.
* ROW verdictstate: FIX-NOW -- The positive controls already exist and are cheap to add to fix this clear testing gap.
* ROW asicannounce: FIX-NOW -- A bounded diagnostic is constructible and restores measurably destroyed self-announcing properties.
* ROW asiceventaddr: CLOSE-OVERTAKEN -- The comment-only disposition was refuted and a C89 build-time check was successfully shipped in #468.
* ROW gdromcondavail: FIX-NOW -- Guest can manually manipulate count to cause overreads that return 0xffff without clearing availability.

**Mechanical check, batches 6-14 (main loop, 23:5x): a FIX-NOW or CLOSE-OVERTAKEN on a row whose `commits` field is already set** (the b115/armbdt pattern):

* `smdatefmt` (batch 6): CLOSE-OVERTAKEN, but the row ALREADY carries commits 6e36943 -- its own round shipped; check what its held stage owes before acting.
* `probetimebased` (batch 13): FIX-NOW, but the row ALREADY carries commits abf665c -- its own round shipped; check what its held stage owes before acting.
* `asiceventaddr` (batch 14): CLOSE-OVERTAKEN, but the row ALREADY carries commits 9ca9cca -- its own round shipped; check what its held stage owes before acting.

## batch 15 -- `oldbatch_15/reply.txt` (3795 bytes)

* ROW gdromdmaclear: FILE -- coverage debt identified, not a live defect
* ROW gdromdmaguard: FILE -- untested zero-count boundary is coverage debt
* ROW gdromdriverclaims: DOCUMENT-AND-CLOSE -- citation re-derived and confirmed fine
* ROW panelcite0824: DOCUMENT-AND-CLOSE -- resolved in place by stripping the citation prefix
* ROW proberowsubset: FILE -- awaits the owner's separate harness round for explicit case selection
* ROW probeslow: CLOSE-OVERTAKEN -- folds into probetimebased per adjudication
* ROW sgirandomcolour: OWNER-DECISION -- regress hold is unsettled awaiting seat execution

## batch 16 -- `oldbatch_16/reply.txt` (4029 bytes)

* ROW asicarray4: DROP -- sizing to [4] violates hardware facts and costs a mutant kill.
* ROW asicindexcase: UNSETTLED -- needs to be built to test if the device-file guard catches the header entry point.
* ROW asickillsurvive: FIX-NOW -- update the oracle to check for 'survived 0x0' instead of just liveness.
* ROW gdrompiooddlen: UNSETTLED -- requires running a probe to prove an odd count survives to alloc_data.
* ROW seatthinkburn: DOCUMENT-AND-CLOSE -- detection is solved and mitigation is a documented operational rule to split briefs.
* ROW depsrm: FILE -- severity low, deferred by owner decision but kept to track the owed measurement.
* ROW gdromallocpair: FILE -- record the hazard so future rounds adding a third call site inherit the obligation.

## batch 17 -- `oldbatch_17/reply.txt` (3463 bytes)

* ROW m8sarrows: FIX-NOW -- add test row for guest-addressable cmmu_nr = 1 to break structural blindness
* ROW panelrefire: FILE -- automatic re-fire owes two negative controls before shipping
* ROW sysasicbitmask31: FIX-NOW -- replace inert bounds check with 1u << ((e) & 31)
* ROW wdcflagindep: FILE -- requires sibling handler reset coverage using the two-controller rig
* ROW wdcperopcode: DOCUMENT-AND-CLOSE -- the scalar spec choice is pinned by unimpl 2op and safe to defer
* ROW wdcsectorreset: FILE -- build and score the one-line wd_sector mutant first
* ROW armthumbabortkill: FIX-NOW -- delete cpu->running = 0 but keep return 0 at the 5 Thumb sites

## batch 18 -- `oldbatch_18/reply.txt` (4014 bytes)

* ROW asanbaselinedrift: FIX-NOW -- add soft-warning diff -rq check for stale ASan tree baseline
* ROW asanstaletree: OWNER-DECISION -- needs ruling on whether to invalidate the ASan baseline with a sync
* ROW asicoffsetkill: FILE -- keep as coverage debt against the detector
* ROW baretitle: FILE -- documentation debt of one bare row and 13 thin ones
* ROW bugfileledgerdir: FIX-NOW -- add reverse direction check from OUTSTANDING_BUGS.md to the ledger
* ROW closeassessrows: FIX-NOW -- audit the 12 members to re-open, re-file, or close with a commit
* ROW codexbriefscoping: OWNER-DECISION -- adjudicate whether section C5 remains in BRIEF_TEMPLATE.md

## batch 19 -- `oldbatch_19/reply.txt` (8123 bytes)

* ROW dashokclass: CLOSE-OVERTAKEN -- the landing closed the issue and only the scheduled Fable regress is owed
* ROW exitdenom: OWNER-DECISION -- requires a classification rule definition before the count can be fixed
* ROW fbclearidempotent: FILE -- isolated to its own row but research incomplete and code untouched
* ROW gdromdefaultstatusless: FIX-NOW -- tests are blinded by succeeding on bad input
* ROW killdrivercrash: FIX-NOW -- test drivers are blind to the exit status and could score a crash as a pass
* ROW landiskunmapped4: FILE -- unmapped writes confirmed but guest-visible harm not yet measured
* ROW offlinescope: DOCUMENT-AND-### dashokclass
* ROW dashokclass: OWNER-DECISION -- Regress validation batched for Sunday flagship sign-off.
* ROW exitdenom: FIX-NOW -- Classifier logic must be integrated into the tool.
* ROW fbclearidempotent: DOCUMENT-AND-CLOSE -- Claim verified by datasheet text, brief-ready.
* ROW gdromdefaultstatusless: CLOSE-OVERTAKEN -- Defect superseded by #490's stale quiet/how rows.
* ROW killdrivercrash: FIX-NOW -- Drivers must check both exit status and sentinel, not just loop completion.
* ROW landiskunmapped4: FILE -- Deterministic unmapped accesses with no guest harm established.
* ROW offlinescope: DOCUMENT-AND-CLOSE -- The true cost/scope is per-function fixture availability, not just file inclusion.

## batch 20 -- `oldbatch_20/reply.txt` (3995 bytes)

* ROW seatunfinished: FIX-NOW -- teach seat_verdicts.py the ends-inside-a-quote discriminator and report a distinct state
* ROW sgirekills: OWNER-DECISION -- held for flagship to review #564 regress scores and pending seat answers.
* ROW sgiretlbshiftub: FILE -- verified low severity signed shift UB on tileptr computation.
* ROW sh4valm33: FILE -- recorded as coverage debt requiring a build to measure rather than a live defect.
* ROW shortthreshold: FILE -- filed as a class to prevent unbounded fix-of-fix iterations.
* ROW wdccdbmidxfer: CLOSE-OVERTAKEN -- fix shipped in #477 but closure blocked by pending seat opus5 in research stage.
* ROW wdccylstale: FILE -- a ledger row was created for an existing bug-file entry describing stale atapi_len.

## batch 21 -- `oldbatch_21/reply.txt` (3991 bytes)

* ROW wdcnullxfer: DOCUMENT-AND-CLOSE -- State notes and recent entries confirm the fix and overlapping guards, with no other reachable dereferences.
* ROW wdcrearmzero: FILE -- The defect still owes a rung-3/4 witness that has crashed outside the fixture.
* ROW gdromlatchreuse: FILE -- Explicitly filed as coverage debt for a mutant that loses diagnostic separation.
* ROW gdromonce: FIX-NOW -- Requires only a one-line grep check to pin the suppression marker.
* ROW hygienenonexistant: FILE -- Fixing the gate requires a full rig census and an allowlist, properly filed as debt.
* ROW adjudglmtag: FIX-NOW -- The identified typo fix in the check loop was never actually committed and needs to be.
* ROW batteryblindstart: FIX-NOW -- A one-line file touch before the git call completely resolves the blind window.

## batch 22 -- `oldbatch_22/reply.txt` (6085 bytes)

* ROW divratchetband: OWNER-DECISION -- Design choice between two-sided band or equality-with-ritual requires owner ruling.
* ROW gdromfmt24: FILE -- Missing SPI/GD-ROM manuals make the correctness of the 0x24 format arm unsettleable locally.
* ROW gdromlatchcross: FIX-NOW -- The mutant rows are already built and measured; must transition into an implementation.
* ROW ghostround: OWNER-DECISION -- Deciding how to wire the ghost round checker into precommit alters commit requirements.
* ROW liveholdsphase: FIX-NOW -- Structural fix required to place the phase evaluation securely inside the live_holds() function.
* ROW agyreservation: FIX-NOW -- Must replicate the OLLAMA4 precedent in panel.sh to explicitly handle the agy tool reservation.
* ROW exitcensus: DROP -- The original tool was correctly restored and per-function attribution is deliberately rejected.

## batch 23 -- `oldbatch_23/reply.txt` (4851 bytes)

* ROW fableheldform: OWNER-DECISION -- question on the 2026-10-17 directive regarding closed rows with held questions
* ROW fbfiqsilent: FIX-NOW -- member 4 shape (delete the kill/silent return, keep the value) for FIQ_ENABLE_SET
* ROW gatedevicesplit: FIX-NOW -- split gate_devices.sh out from gate_arm.sh as forced by the probe addition
* ROW lcaconfbus1kill: CLOSE-OVERTAKEN -- defect removed by #515 (b4d4177), with detector as the control
* ROW otherkilldeath: FIX-NOW -- add the text membership test to the other kill row to make it symmetric
* ROW pcc2widthkills: CLOSE-OVERTAKEN -- shipped as b78bb0f and successors, owes PASS 14 as the control
* ROW ppcrldimimask: CLOSE-OVERTAKEN -- closed by #527 (22c278cd), owes the REGRESS test scores as control

## batch 24 -- `oldbatch_24/reply.txt` (3938 bytes)

* ROW ppcrlwimiwidth: OWNER-DECISION -- Awaiting flagship review and REGRESS scores.
* ROW randompixdiagonce: FILE -- Coverage debt not fixed in-round, to be filed for later.
* ROW relrefstale: FILE -- Structural tooling fix filed rather than built in the current round.
* ROW selftestaddition: FIX-NOW -- Convert the 9 mutants to not mutate live input data.
* ROW sgilinearoob: FIX-NOW -- Ship a bounds policy covering all 6 arms together.
* ROW sgimtewidth: FIX-NOW -- Land the unreachable width kill as a decline.
* ROW sgirebufuninit: FIX-NOW -- Initialize buf to prevent guest-visible host stack leak.

## batch 25 -- `oldbatch_25/reply.txt` (3100 bytes)

* ROW sgitexindex: FILE -- low severity, keep open until re_tex is consumed.
* ROW storesidedead: UNSETTLED -- census cut short before completion.
* ROW untokenedanswers: OWNER-DECISION -- blocked on owner ruling for roster exclusion recording.
* ROW wdcaltownership: FILE -- low severity mapping conflict.
* ROW wdcflagswap2: FILE -- transient over-refusal, filed rather than fixed.
* ROW wdcpktstatus: FIX-NOW -- mirror backend sense key into bits 7:4.
* ROW wdcprobeendian: FILE -- coverage debt pending BE rig.

## batch 26 -- `oldbatch_26/reply.txt` (4177 bytes)

* ROW wdcrearmwalk: FIX-NOW -- add a loop-to-exhaustion row to cover later chunk boundaries.
* ROW wdcringresetblind: FILE -- keep as low-severity debt since the blind spot is confirmed and structurally masked.
* ROW witnesssilent: OWNER-DECISION -- owner must dictate policy on requiring expected post-fix scores.
* ROW xscaleinten: UNSETTLED -- cannot execute the required closure regress check (30/30 vs 12/30) purely from text.
* ROW exit0oracle: DROP -- the relevant file is on the never-commit list, so the finding is recorded but unactionable.
* ROW gxprobepccache: CLOSE-OVERTAKEN -- fixed at source in send(), but must check if gxprobe.py is tracked.
* ROW mtetlbflood: FIX-NOW -- add the standard once-per-instance latch to the fatal() call.

## batch 27 -- `oldbatch_27/reply.txt` (4819 bytes)

* ROW sgirelatchenum: FIX-NOW -- convert to auto-incrementing bit position enum and verify byte-identical binaries
* ROW staticlatchscope: FIX-NOW -- migrate process-global function-static latches to per-instance struct fields
* ROW rulingnotinrow: FILE -- keep as debt to manually read the three named candidate rows for missing rulings
* ROW pcc2assertflood: FIX-NOW -- move debug logging to after the MIEN gate to report final effective state
* ROW pcc2c040kill: CLOSE-OVERTAKEN -- host kill removed by #512 (commit 9fa07fe)
* ROW pcc2counter8: FIX-NOW -- restrict write width and re-cut the affected detector rows
* ROW pcc2latchwidth48: FILE -- keep as low-severity coverage debt, or drop if queue needs pruning

## batch 28 -- `oldbatch_28/reply.txt` (4455 bytes)

* ROW pcc2pscaleflood: DROP -- explicitly marked to close as duplicate of pcc2huhflood's nine-site latch
* ROW pcc2widecompose: FILE -- marked as FILE-AND-LEAVE with no immediate defect to fix
* ROW lbsmask: FIX-NOW -- replace power-of-two assumption with modulo or proper mask
* ROW m88kbcndm6: FILE -- explicitly adjudicated as FILE, LOW coverage debt
* ROW m88kexcsfu1: FIX-NOW -- implement faithful SFU1 exception delivery including FP registers and scoreboard
* ROW m88kidledup: FILE -- explicitly adjudicated as FILE, LOW coverage debt
* ROW pcc2huhflood: FIX-NOW -- carrier of the floodclass round requiring the nine-site latch

## batch 29 -- `oldbatch_29/reply.txt` (4145 bytes)

* ROW pcc2iclrdec: FILE -- Coverage debt belongs to a future timer-semantics round
* ROW wdcbeoddtail: OWNER-DECISION -- Defect verified, but requires project owner to select from 3 distinct fix paths
* ROW wdccylwrap: FIX-NOW -- Replace clamping with a default translation geometry that fits 16 bits
* ROW wdcdiagerr: FIX-NOW -- Decouple the d->error variable to prevent one value serving two distinct registers
* ROW wdcfloodprobe: FILE -- Minor harness and records repair bundle for #464 material
* ROW wdcgeomparse: FILE -- Add missing differential row at the heads position for ULLONG_MAX
* ROW wdcidentorder: FILE -- Add missing row to verify IDENTIFY byte order instead of just ring occupancy

## batch 30 -- `oldbatch_30/reply.txt` (4447 bytes)

* ROW wdcstubtype: FILE -- The row is already explicitly marked as filed low-severity debt by the owner.
* ROW m88kdslotshadow: FIX-NOW -- A fix round is landing; the measurement of the handler-return row definitively settles the correct SNIP/SFIP behavior.
* ROW m88kexcdebt: FILE -- Explicitly filed as coverage debt and ranked below live defects.
* ROW m88kexcfrozendmt: FIX-NOW -- The bug is well-understood and a specific fix shape and row extension are provided.
* ROW m88kexchwtraps: OWNER-DECISION -- The manual is silent on the behavior, requiring a design decision on whether to deliver or decline.
* ROW pcc2anngrid: FILE -- Instructed to ride the next instrument change, keeping it filed as debt for now.
* ROW pcc2iackmodel: FIX-NOW -- The defect is clear and the exact pitfalls to avoid when modeling the fix are mapped out.

## batch 31 -- `oldbatch_31/reply.txt` (3482 bytes)

* ROW pcc2latchinst: FILE -- requires a two-instance-in-one-process fixture to distinguish the fields.
* ROW wdcwidthmatrix: DOCUMENT-AND-CLOSE -- text confirms completeness, not a live hole, reason is arithmetic.
* ROW asicplus2row: FIX-NOW -- add anchored row mask9b rt to claim the translation group.
* ROW batterymissedruns: FIX-NOW -- tools/nightly_check.sh needs to be executed to report missing verdicts.
* ROW briefforcedwrong: OWNER-DECISION -- modifying the artifact template affects future panels and requires owner decision.
* ROW codexsubjectrefusal: FIX-NOW -- ask codex the DESIGN question and let another seat answer REACHABILITY.
* ROW irqassertedunread: FILE -- scaffold cleanup for i960/riscv and track completion of CPU/PAL/chipset path for alpha.

## batch 33 -- `oldbatch_33/reply.txt` (4088 bytes)

* ROW mipstiny: OWNER-DECISION -- contradiction between Astra's resolution and the lack of counter-argument review requires flagship seat adjudication.
* ROW sgirandomskipput: OWNER-DECISION -- general fix collides with a shipped oracle, requiring explicit contract adjudication.
* ROW sgirelinb: FILE -- lacks hardware warrant to implement LIN_B as symmetric to LIN_A; awaits valid reference.
* ROW sgirenamedstmode: FIX-NOW -- laundering shape requires atomic update of both the code diagnostic and the test anchor.
* ROW sgitileptrsilent: OWNER-DECISION -- sibling parity exposes asymmetry but does not dictate closing it without design ruling.
* ROW wdcconsumedattempts: FILE -- unproven silent-corruption claim requires a rung-3 reproducer attempt before fixing.
* ROW alphaclrfen: FILE -- unverified report of missing PALcode case requires reading and confirmation.

## batch 34 -- `oldbatch_34/reply.txt` (3116 bytes)

* ROW alphactxfail: FILE -- Requires propagating context-memory failures through a defined failed-switch outcome.
* ROW alphafaultclaim: FILE -- Documentation and fault delivery need alignment.
* ROW alphapteprot: DOCUMENT-AND-CLOSE -- The contract is explicitly documented rather than a bug in caching.
* ROW alphaswpctxreg: FIX-NOW -- Fix register assignment from ALPHA_A0 to ALPHA_V0 as per the comment and ABI.
* ROW armbfiwidth: OWNER-DECISION -- Await measurement of width-32 lowering before shipping.
* ROW cxseatcheck: CLOSE-OVERTAKEN -- Defect is being addressed in #544 (e8a2bc).
* ROW dec21143deadclamp: DOCUMENT-AND-CLOSE -- Evidence shows guards are mathematically unreachable.

## batch 35 -- `oldbatch_35/reply.txt` (6228 bytes)

* ROW gateworktree: OWNER-DECISION -- whether to implement the narrower STAGED set check, as it changes commit requirements
* ROW gdrommappedvacuous: DROP -- already filed in OUTSTANDING_BUGS.md and warrant for this row has decayed
* ROW guestsrcunknown: FIX-NOW -- add a carrier line to CLAUDE.md pointing to _guest-src-openbsd22/
* ROW m88kexcdetectorl2: FIX-NOW -- perform the full table measurement on agy as explicitly ruled by the adjudicator
* ROW mtesrcdup: DOCUMENT-AND-CLOSE -- text states it is not a defect and is documented-only unless already editing
* ROW negrowclass: DROP -- warrant has decayed and it is tracked in OUTSTANDING_BUGS.md
* ROW printedvariants: DROP -- warrant has decayed and it is tracked in OUTSTANDING_BUGS.md

## batch 38 -- `oldbatch_38/reply.txt` (4982 bytes)

* ROW codexcyberflag: DOCUMENT-AND-CLOSE -- The row acts as a ledger entry for a measured phenomenon whose circumvention technique is known but needs formal promotion to a rule.
* ROW guardfailsopen: FIX-NOW -- The guard fails open due to an unhandled empty shell variable causing a syntax error that bypasses the refusal branch.
* ROW probecolorprompt: FILE -- The issue is a latent environment dependence affecting 52 files, explicitly deferred to avoid scope creep in the current round.
* ROW seattruncverdict: FIX-NOW -- A mechanical size comparison in seat_verdicts.py will trivially trap truncated responses masquerading as ratifications.
* ROW sgidefatalstale: FILE -- The text identifies stale commentary that misleads readers but acknowledges it does not affect execution, correctly deferring it to the owning rounds.
* ROW splitscorer: DROP -- The author confirmed the defect was introduced and subsequently repaired within the same session, leaving a population of zero at HEAD.
* ROW alphaintdeliver: FILE -- The row accurately records a missing subsystem tracking ticket spun out of a fixed kill adjudication.

**Mechanical check of these batches (FIX-NOW / CLOSE-OVERTAKEN on a row that already carries commits):**

* `dashokclass` (batch 19): CLOSE-OVERTAKEN, but the row already carries commits `dd2d4e01` -- its own round shipped; what it owes is its held stage.
* `wdccdbmidxfer` (batch 20): CLOSE-OVERTAKEN, but the row already carries commits `0922465` -- its own round shipped; what it owes is its held stage.
* `lcaconfbus1kill` (batch 23): CLOSE-OVERTAKEN, but the row already carries commits `41923ac` -- its own round shipped; what it owes is its held stage.
* `pcc2widthkills` (batch 23): CLOSE-OVERTAKEN, but the row already carries commits `b78bb0f` -- its own round shipped; what it owes is its held stage.
* `ppcrldimimask` (batch 23): CLOSE-OVERTAKEN, but the row already carries commits `7e39a49 22c278cd` -- its own round shipped; what it owes is its held stage.
* `pcc2c040kill` (batch 27): CLOSE-OVERTAKEN, but the row already carries commits `9fa07fe` -- its own round shipped; what it owes is its held stage.
* `alphaswpctxreg` (batch 34): FIX-NOW, but the row already carries commits `3031a30` -- its own round shipped; what it owes is its held stage.

## batch 32 -- `oldbatch_32/reply.txt` (5071 bytes)

* ROW lunaabsentmaskdecl: FILE -- keep as debt to ensure the missing substance from the 'file as rows' instruction is recovered.
* ROW lunadefaultstop: FILE -- keep as debt until a proper handler for the 1.76 GB unimplemented space is designed.
* ROW lunancpus3: OWNER-DECISION -- the closure strategy relies on an assumption that must be tested on the simulator first.
* ROW m88kexctaildefault: DOCUMENT-AND-CLOSE -- the issue explicitly states it is documented-only and the design option was deliberately not adopted due to blast radius.
* ROW m88kpsrmxm: FILE -- the defect is confirmed and requires a design because no fork currently fixes it.
* ROW m88ksfrzfatal: DOCUMENT-AND-CLOSE -- the text asserts this is not a correctness defect and merely documents a floodclass instance.
* ROW m88ktbnd: OWNER-DECISION -- the issue requires the owner to determine and name the specific path before it can be ranked or closed.

## batch 36 -- `oldbatch_36/reply.txt` (2676 bytes)

* ROW probeneedleterm: UNSETTLED -- full record is in OUTSTANDING_BUGS.md and unreadable here.
* ROW refilingclass: FILE -- severity med, tracking process failure where findings are re-derived and duplicated.
* ROW sessionechosat: UNSETTLED -- full record is in OUTSTANDING_BUGS.md and unreadable here.
* ROW sessionrefused: UNSETTLED -- full record is in OUTSTANDING_BUGS.md and unreadable here.
* ROW sgigbeconvover: FIX-NOW -- replace i < 512 with i < len
* ROW sgirebufshiftub: FILE -- severity LOW, pending check of whether UBSan sweep reaches this function.
* ROW sgireput8tail: FILE -- severity low, coverage debt that becomes live when sgirebufuninit ships.

## batch 37 -- `oldbatch_37/reply.txt` (4186 bytes)

* ROW sgirespanchk: OWNER-DECISION -- need to know if callers can present unaligned/oversized spans
* ROW sgirgbscanoutrow: FILE -- requires a different probe shape with a framebuffer oracle
* ROW sgiwidthwiredobl: FIX-NOW -- demote the stale contract in place and record the commit
* ROW shiftubcensus: FILE -- keep open as the class is only fractionally surveyed
* ROW ubsanshiftlane: DOCUMENT-AND-CLOSE -- the filed question about the UBSan sweep is fully answered
* ROW uninorthdevscan: DOCUMENT-AND-CLOSE -- verified that the width cannot exceed 32 bits, lacking guest visibility
* ROW armbfcdecode: OWNER-DECISION -- architectural claim remains unverified against local manuals

## batch 39 -- `oldbatch_39/reply.txt` (3870 bytes)

* ROW alphaswpctxmut: FIX-NOW -- build the described mutant and score the existing probe against it.
* ROW armbfxcells: FIX-NOW -- build the 4 named weakening cells and score the rows against them.
* ROW lcairqedgepin: FIX-NOW -- add the control row with OCW3 0x0a to 0x20 and LDBU 0x20 wanting 0x12.
* ROW sgilinearnegidxpostmortem: OWNER-DECISION -- three rule questions regarding premise-audit, template line, and C5 refusal delay.
* ROW wdcaltoffleg: FILE -- owes the parent's ok and completion of the single instrument implementation.
* ROW wdcsingleleg: FIX-NOW -- re-date the four EXEMPT entries naming this row so the debt names its round.
* ROW witnessclassdoor: FILE -- detector debt escapes through class field for >= 9 probes that are actually detectors.

## batch 40 -- `oldbatch_40/reply.txt` (4069 bytes)

* ROW exitunowned76: FILE -- tracking row for remaining error-exit sites, incomplete.
* ROW lcaiocstat0: FIX-NOW -- uniform store-and-echo is incorrect; specific register semantics must be implemented.
* ROW mapledmaaddr: OWNER-DECISION -- closure is recorded but REGRESS hold question requires flagship test verification.
* ROW mapledmaadvance: FILE -- unresolved semantic question lacking real hardware documentation to settle.
* ROW mipsextshift: OWNER-DECISION -- repairing undefined negative shifts on invalid encodings requires a panel design decision.
* ROW ppccr0modewidth: FIX-NOW -- use current operating mode instead of CPU model width in update_cr0().
* ROW ppcrlwhighhalf: FILE -- defect witnessed on committed HEAD but fix round explicitly remains unscheduled by owner.

## batch 41 -- `oldbatch_41/reply.txt` (4802 bytes)

* ROW sgimtetlbdefault: FIX-NOW -- guest-drivable unlatched fatal with a known, settled fix shape.
* ROW vmedefaultkill: OWNER-DECISION -- held on policy question about roster waivers only the owner can rule on.
* ROW agentmodelwall: DOCUMENT-AND-CLOSE -- establishes an operational rule for tool usage, not a code defect.
* ROW armbdtcombined: FILE -- pre-existing bypass issue filed under the stopping rule, to be tracked as debt.
* ROW censusprobescope: FILE -- lost counter-proposal from a closed round needs tracking.
* ROW killtablebaseline: FIX-NOW -- trivial two-line fix to prevent baseline script from lying via moving reference.
* ROW landiskboardreg: FILE -- discovered unmapped addresses requiring investigation before fix or severity assignment.

## batch 42 -- `oldbatch_42/reply.txt` (5230 bytes)

* ROW landiskintc: OWNER-DECISION -- severity/relevance requires reading SH7751R manual to see if missing extended block matters.
* ROW lcaisaqword: FILE -- real drivers rarely emit this, but it is a calibrated addressing defect to track.
* ROW lcaisasize: FIX-NOW -- capture (relative_addr >> 3) & 3 before shift to handle the 7 under-copied sizes.
* ROW multiaccesswarms: FILE -- requires manual census to identify and fix vacuous slow-path assertions in multi-access probes.
* ROW ppcgateimageskip: OWNER-DECISION -- needs testing/reading gate_ppc.sh to answer if probe blocks run before need_file.
* ROW ppcprobescorestale: FIX-NOW -- demote 'naive fix wrong' to a print to complete Part 2.
* ROW probeexitzero: FILE -- 26 probes violate the house idiom and must be standardized to prevent misleading gate authors.

## batch 43 -- `oldbatch_43/reply.txt` (3814 bytes)

* ROW probereadalign: FILE -- Left open intentionally as a class tracker to guard against future regressions.
* ROW sgideprimopstrengthen: FILE -- Coverage debt representing a non-floor-breaching detector strengthening.
* ROW ppc527residual: FILE -- Consolidates five remaining coverage and named measurement debts from #527.
* ROW silencewhitelist: FILE -- Acknowledged class of silence oracle debt awaiting its census.
* ROW carrierstalecopies: FIX-NOW -- Tangible file debris (CR/BEL/directories) sitting in the project root should be immediately purged.
* ROW 8259cmdhalt: FILE -- Held pending the results of the halt-class census job.
* ROW cellechoesbrief: FILE -- Owed tooling harness change to prevent future automated extraction loops.

## batch 44 -- `oldbatch_44/reply.txt` (3993 bytes)

* ROW changelogroundgap: FILE -- a tooling change owing two negative controls that must ship as its own harness round.
* ROW cpusexitsweep: FILE -- a census is a research item that generates rows, not a single defect to fix inline.
* ROW crimectlflood: FILE -- adding a latch here would immediately break an existing, coupled detector row.
* ROW crimeramexit: FILE -- the exit calls are machine-config gated, not guest-drivable.
* ROW crimesplitwidth: FILE -- this is a latent condition dependent on a device length constant rather than an active defect.
* ROW gdromacceptdmadebt: FILE -- fixing this coverage debt requires a new session rather than an in-round oracle edit.
* ROW gdromdmaflood: OWNER-DECISION -- disposition deliberately unchosen because silencing a success path might bury desired diagnostics.

## batch 45 -- `oldbatch_45/reply.txt` (5573 bytes)

* ROW gdromdmaxferflood: FILE -- flood is on a success path and fix requires carefully re-pinning a testing oracle first
* ROW guestloopdenial: OWNER-DECISION -- requires policy ruling on whether capping an explicit 16M hardware contract violates emulation fidelity
* ROW ip22legacyabort: FILE -- host kill is present but securely dead code; worth tracking to prevent blind regressions
* ROW ip30asdvasdvnb: FIX-NOW -- simply delete the meaningless and unlatched fatal() string on a perfectly functional arm
* ROW ip30setisrassign: FIX-NOW -- change buggy assignment operation to proper logical OR operation
* ROW ledgercommitsshape: FILE -- file a tooling ticket to deploy a commits_of(row) accessor instead of normalizing the ledger
* ROW lunafbhalt: FILE -- genuine CPU halts on ordinary offsets exist but are shielded by conditional X11 initialization

## batch 46 -- `oldbatch_46/reply.txt` (3033 bytes)

* ROW macepciwidth: FILE -- owes a rung-3 ATTEMPT before any round
* ROW manifestscope: FILE -- ships as its own HARNESS ROUND and owes two negative controls
* ROW mapledmahang: OWNER-DECISION -- the loop bound is a design question and is not derivable from the tree
* ROW mpipirealloc: FILE -- growth by accretion rather than a crash, requiring sustained guest cooperation
* ROW pciaddrreadclobber: FILE -- latent class across three files requiring a unified fix
* ROW pitmodebyteshared: FILE -- newly filed from a residual bullet to track a missing ledger row
* ROW probeblockingwait: FILE -- belongs with the round that builds the mapledmahang witness

## batch 47 -- `oldbatch_47/reply.txt` (3129 bytes)

* ROW sh4dmacnote: OWNER-DECISION -- Needs a rung-3 probe to determine if the generic path actually transfers.
* ROW untrackeddetectors: FIX-NOW -- The staging is complete but the commits are still owed.
* ROW wallverdictand: FIX-NOW -- Apply the documented fix shape for strong vs weak wall verdicts.
* ROW alphaifetchkill: FIX-NOW -- Apply the GENERIC three-hunk fix for the translation miss.
* ROW alphapcbbvirt: OWNER-DECISION -- A primary source check is required before designing a fix.
* ROW attribclosingadj: FILE -- A harness fix requiring controls, correctly filed as debt.
* ROW ayona3: FILE -- A flood output requiring a separate fix vehicle.

## batch 48 -- `oldbatch_48/reply.txt` (4534 bytes)

* ROW dashmalformedheld: FIX-NOW -- take fallback out of if not ents branch
* ROW devwritedata: OWNER-DECISION -- enumerate the 11 missing test sites
* ROW exemptcal: FIX-NOW -- add date.fromisoformat under try block
* ROW fbnobuild: FIX-NOW -- implement L4 repair draft with shared snapshot
* ROW fiqenableread: OWNER-DECISION -- choose which round to fold the FIQ fix into after datasheet confirm
* ROW hpcmipsc2: FIX-NOW -- re-base C2 on synthetic unrelated abort
* ROW ip30abortresidual: FILE -- coverage debt not owed before closure

## batch 49 -- `oldbatch_49/reply.txt` (4280 bytes)

* ROW landiskauxorder: FILE -- Disposition 3 prevents amending the shipped code, converting the gap to filed debt.
* ROW lcaconfbit1: OWNER-DECISION -- Cannot proceed without HRM specifications on guest-visible return values.
* ROW lcaisaphyshit: DOCUMENT-AND-CLOSE -- The defect is explicitly stated as closed by construction in #540.
* ROW lcawidefold: DOCUMENT-AND-CLOSE -- Alignment dependency explains the behavior; it only requires documentation.
* ROW m5dayb: OWNER-DECISION -- Needs a tie-breaker between fable5 and glm on adding the optional 23rd test case.
* ROW pcc2c040debugchan: FILE -- It is explicitly identified as disclosed coverage debt above the floor.
* ROW pcc2c040latchswap: FIX-NOW -- Elevated to a reachable MED hazard, necessitating the pre-set fix.

## batch 50 -- `oldbatch_50/reply.txt` (3565 bytes)

* ROW physupdtlb: FILE -- keep as debt to add a PHYSICAL guard preventing guest VA replacement.
* ROW ptywaitstatus: FILE -- policy dictates fixing probes individually per round, not as a sweep.
* ROW seatprescriptiondiff: FIX-NOW -- add mechanical check for FIXDIFF to row mappings.
* ROW seatsreadburnsplit: FILE -- debt remains to read the 23 genuine unread seat answers.
* ROW wdcaddr2: DROP -- no measured delta today, so the addition licence does not license it.
* ROW wdcrstbitonly: OWNER-DECISION -- missing the required offset-0 test row writing 0x0a or 0x02 to prove the defect.
* ROW agentrefusal: FILE -- keep as debt to build a tracked credit check in its own harness round.

## batch 51 -- `oldbatch_51/reply.txt` (3738 bytes)

* ROW alphavmkillfirst: FILE -- keeping as debt for a low-severity undetected test exit
* ROW armdacr2kill: FIX-NOW -- change case 2 in arm_check_access() to treat as no-access instead of exiting fatally
* ROW armdesc3kill: FIX-NOW -- route ARMv4/v5 descriptor type 3 to FAULT or IMPLEMENT to avoid fatal exit
* ROW armvecrecurse: FILE -- keep as debt (high severity) for guest-drivable host process death via nested prefetch aborts
* ROW brieftplstale: FIX-NOW -- use the find/md5 deriver for tree warnings and add the M3 fact to section C5
* ROW cxlaunchempty: FIX-NOW -- implement variable read and empty refusal (exit 9) before cd
* ROW cxlaunchquotation: OWNER-DECISION -- held pending Fable's answer on V6/V7 passes to rule on the landed launcher

## batch 52 -- `oldbatch_52/reply.txt` (3670 bytes)

* ROW excvecrecurse: FIX-NOW -- add nested-abort guard or disable translation on vector fetch
* ROW fbcsrdecodelanes: FILE -- device decode deviation requires masking fix (severity MED)
* ROW fbgateidentity: FILE -- gate counts rows instead of matching names (severity LOW)
* ROW fbirqdeliverywitness: FIX-NOW -- add the missing CPU IRQ line witness test
* ROW fbirqsoftunimpl: FIX-NOW -- implement +0x190/+0x290 write latching
* ROW fbm2findings: FILE -- non-blocking further findings (severity MED)
* ROW fbptymock: FILE -- teardown failure paths need a mock binary (severity LOW)

## batch 53 -- `oldbatch_53/reply.txt` (3777 bytes)

* ROW lcaandlen: FILE -- the lane selector logic weakening is a tracked test gap.
* ROW lcauninitbyte: DOCUMENT-AND-CLOSE -- the bug is effectively dead since the guest halts before consumption.
* ROW ptyprobepins: OWNER-DECISION -- precommit hook needs a ruling on whether to check staged vs working tree.
* ROW sgimtereadiness: FILE -- legacy promptless probe is grandfathered and needs conversion in a future round.
* ROW astraharnesslow: FILE -- meta-tracker must stay open until all 237 sub-rows are processed.
* ROW armbdtreadiness: FILE -- owner ruled to allowlist readiness check by name instead of converting it yet.
* ROW fbbufbounds: FILE -- bounds check execution order relative to declined accesses needs repair.

## batch 54 -- `oldbatch_54/reply.txt` (3578 bytes)

* ROW fbcallerctx: FILE -- test harness mock limitations (where dummy CPUs pass all caller state conditions) are known test debt but do not crash the emulator.
* ROW fbclrdest: FILE -- unobserved test state for a narrow IRQ clear is low-priority debt.
* ROW fbenablewidth: FILE -- test condition conjuncts trivially passing all rows without proving correctness is a coverage gap, not a runtime crash.
* ROW fbirqstuck: FIX-NOW -- stuck CPU interrupt lines indicate a functional lockup defect in the device model.
* ROW fblatchhistory: FILE -- untestable warn-once latch re-arming is low-severity technical debt.
* ROW fbtimercomments: FIX-NOW -- provably false comments in the test framework misguide future triage and should be immediately corrected.
* ROW hygienecensusexotic: FILE -- owner explicitly ruled to file exotic input crashes as acceptable script limitations rather than fixing.

## batch 55 -- `oldbatch_55/reply.txt` (3511 bytes)

* ROW hygienecensusholes: UNSETTLED -- Text does not provide enough information to determine disposition without external files.
* ROW asanstaleobjs: UNSETTLED -- Cannot verify object staleness without filesystem access.
* ROW attrcheckgaps: OWNER-DECISION -- The hold question actively asks for a decision on which control proves the tripwire.
* ROW deletecheckhead: UNSETTLED -- Cannot verify index vs worktree check without the script text.
* ROW fbbounddebt: UNSETTLED -- Claims about mutant cells cannot be verified without source.
* ROW fbboundmodes: UNSETTLED -- Timer mode execution paths cannot be verified without source code.
* ROW fbdrainonepass: UNSETTLED -- Performance halving claim cannot be verified without executing the benchmark.

## batch 56 -- `oldbatch_56/reply.txt` (3516 bytes)

* ROW fbdrainxdisable: FILE -- open bug with evidence in OUTSTANDING_BUGS.md
* ROW fbharnessedits: FILE -- open logic debt identified in #548
* ROW svbackspace: FIX-NOW -- regex pattern escape bug in python script
* ROW asanfifteen: FIX-NOW -- script references wrong count for AB_EXEMPT
* ROW exemptdistinct: FILE -- missing date uniqueness enforcement in probe wiring
* ROW fbctrlcmdkill: OWNER-DECISION -- Fable 5.1 walled, awaiting regression scores for #567
* ROW fbctrloffkill: FIX-NOW -- check offsets in dev_fbctrl.c to prevent emulator kill

## batch 57 -- `oldbatch_57/reply.txt` (3423 bytes)

* ROW fbctrlportdebt: FIX-NOW -- measured one-diff close already exists and passes (61/61)
* ROW fbctrltwoinst: FILE -- per-device latch lacks multi-instance test coverage (LOW severity)
* ROW fbpendingselfcheckG: FILE -- self-checks are structurally weaker than #551's but test passes (LOW severity)
* ROW panelwallquote: FIX-NOW -- script misclassifies valid seats as walled due to quotes
* ROW scoreclaimsrawdoc: FIX-NOW -- parser fails on prefixed strings but reports successful check
* ROW seatverdictsubs: FIX-NOW -- parser misinterprets 403 access denial as a missing verdict
* ROW wdcidcomparators: FILE -- explicit owner ruling dictates filing the remaining 104 comparators

## batch 58 -- `oldbatch_58/reply.txt` (3769 bytes)

* ROW wdcidlane: FIX-NOW -- add the piped self-mutant lane to reject the M19 log rewrite
* ROW wdcrowpin: CLOSE-OVERTAKEN -- #551e already catches deleted covered rows via call counts
* ROW wdcverdictone: CLOSE-OVERTAKEN -- #551f reds the count check anyway
* ROW analyze8robust: FILE -- defer fix since it is only needed if reused
* ROW commitinflight: FIX-NOW -- add a check keyed on the launch log's completion line to section G
* ROW wdcidresetcells: FIX-NOW -- fold the unmeasured reset shapes into wdcidlane's table
* ROW idlesslow: FILE -- keep as tracker until all 94 rows are promoted

## batch 59 -- `oldbatch_59/reply.txt` (2930 bytes)

* ROW armmmuvehicle: FIX-NOW -- build the test vehicle with the 9 design opus5 changes
* ROW M2_gdromnodatawidth: FILE -- MED
* ROW addovftie: FILE -- MED
* ROW alphatbilowerwidth: FILE -- MED
* ROW alphatinyzero: FILE -- MED
* ROW arccursorbound: FILE -- HIGH
* ROW arcsgiprivate: FILE -- HIGH

## batch 60 -- `oldbatch_60/reply.txt` (2764 bytes)

* ROW arczeroalloc: FIX-NOW -- guest can trigger host exit via 0-length disk I/O
* ROW armabortdest: FILE -- emulation inaccuracy but no host crash
* ROW armalignexc: FILE -- emulation inaccuracy but no host crash
* ROW armcachecleanload: FILE -- emulation inaccuracy but no host crash
* ROW armcachegeom: FILE -- emulation inaccuracy but no host crash
* ROW armcolddump: FILE -- test harness deficiency, no host crash
* ROW armcp15cp14exits: FIX-NOW -- guest can trigger host exit via coprocessor instructions

## batch 61 -- `oldbatch_61/reply.txt` (3439 bytes)

* ROW armcpabsent: DOCUMENT-AND-CLOSE -- existing prose entry requires no second tracker.
* ROW armdwordalign: DOCUMENT-AND-CLOSE -- existing prose entry requires no second tracker.
* ROW armendianexit: FILE -- HIGH severity reachable exit() requires a fix.
* ROW armfastrotxor: FILE -- MED severity logic bug overwriting rotation loss.
* ROW armfoldp1hide: FILE -- MED severity lost guest-visible register updates.
* ROW armliteralrot: FILE -- MED severity incorrect LDR unaligned shortcut.
* ROW armmemcpyoverlap: FILE -- MED severity unsafe overlapping memcpy calls.

## batch 63 -- `oldbatch_63/reply.txt` (2529 bytes)

* ROW asanexit1subtype: FILE -- missed event ends emulator process
* ROW asccmddma: FILE -- DMA reads CDB from private DEC buffer
* ROW ascoutresid: DOCUMENT-AND-CLOSE -- measured choice #283 stays
* ROW ascpiozero: FILE -- PIO DATA_IN pushes zeros from unpopulated data
* ROW ascwidecount: FILE -- negative len2 passes guards and overflows memcpy
* ROW astraretrolow: FILE -- class row pending promotion of members
* ROW bgezfallstore: FILE -- BGEZ rows score branched when both stores run

## batch 64 -- `oldbatch_64/reply.txt` (2671 bytes)

* ROW bscd3clear: FILE -- Debt recorded as NEW MED in the disposition draft.
* ROW cachecleanrdmask: FILE -- Debt recorded as NEW MED, confirming #346 behavior.
* ROW countunreadable: FILE -- Diagnostic text can be zeroed out by lib.sh.
* ROW crimebankorder: OWNER-DECISION -- Waiting for a boot witness before modifying interleaved registers.
* ROW crimecontroldebt: FILE -- Acknowledged strengthening debt from PR 529.
* ROW crimectllane: FILE -- Known channel bypass requiring re-derivation.
* ROW cuebomparse: FIX-NOW -- Clear defect where parser and sniffer disagree on UTF-8 BOM handling.

## batch 65 -- `oldbatch_65/reply.txt` (5303 bytes)

* ROW dectxzero: FILE -- The macro aborts the emulator on a valid glibc free-via-realloc, which requires tracking as a guest-triggerable death.
* ROW diagdivchained: OWNER-DECISION -- The severity is disputed based on hypothetical vs. live harness failure rules and requires flagship arbitration.
* ROW diagdivtruncarg: OWNER-DECISION -- The severity is disputed based on hypothetical vs. live harness failure rules and requires flagship arbitration.
* ROW diagdivunaryop: OWNER-DECISION -- The severity is disputed based on hypothetical vs. live harness failure rules and requires flagship arbitration.
* ROW diskwritefullstore: FILE -- The test harness cannot execute its intended failure state verification.
* ROW divbyinfnan: FILE -- Must remain tracked as debt until the required rung-3 probe can be constructed to witness the bug.
* ROW drecalccap: FILE -- The floppy image geometry recalculation mismatch remains a medium severity flaw to be tracked.

## batch 67 -- `oldbatch_67/reply.txt` (3732 bytes)

* ROW fbpcibus255zero: FIX-NOW -- PCI empty bus reads should return 0xFFFFFFFF instead of leaving the pre-zeroed 0
* ROW fbresizeoverlap: FILE -- Issue confirmed but lacks inline detail for an immediate fix, requires filing as MED debt
* ROW fbs3early: FIX-NOW -- Reorder the IRQEnable sample to occur after the FIQ decline pairs
* ROW fbsignalcoverage: FIX-NOW -- Enforce a minimum callback serviced count rather than relying solely on wall-time
* ROW fbslicehide: FIX-NOW -- Restore the third cumulative delivery expectation to 85.89934592 to properly expose the freeze
* ROW gateupstreamstatus: FIX-NOW -- Prevent the sed pipe from masking the loader exit status using pipefail or PIPESTATUS
* ROW gdroma88zeroinit: FIX-NOW -- Inject a non-zero pre-state to properly validate condition clearance

## batch 68 -- `oldbatch_68/reply.txt` (5146 bytes)

* ROW gdromacceptseed: FILE -- Unseeded DMA logic is verified right under KERNEL precondition; filed as MED debt.
* ROW gdromcondhow: OWNER-DECISION -- Disputed HIGH severity regarding the live decline path explicitly awaits a flagship rule decision.
* ROW gdromdmareentr: FIX-NOW -- Unbounded DMA recursion exhausting the host stack is a confirmed crash-on-malformed-input defect.
* ROW geomparsercheck: FILE -- Parser self-check failing to reach the compare block is a MED testing harness gap.
* ROW geomtypewitness: FILE -- The lack of guard witnessing on s/i rows is a documented MED test coverage gap.
* ROW gssiglblid: FIX-NOW -- The register constant failing to encompass its own documented highest register is a logic defect.
* ROW guestrelbin: FIX-NOW -- A relative path executing post-chdir breaks binary resolution; trivial to fix by absolutizing the path.

## batch 71 -- `oldbatch_71/reply.txt` (2172 bytes)

* ROW jazzlbmask: FILE -- Logged as MED with NT startup dependencies.
* ROW jazzpendingovf: FILE -- Confirmed new MED with overflow consequences.
* ROW lcaabsentpass: FILE -- Drafted as new MED.
* ROW lebufsize: FILE -- Confirmed new MED for LANCE rejection window.
* ROW lerxstaleenp: FILE -- Confirmed new MED for stale ENP.
* ROW letxrestart: FILE -- Confirmed new MED, widened by external fixes research.
* ROW letxshortage: FILE -- Confirmed new MED for partial frame pending.

## batch 75 -- `oldbatch_75/reply.txt` (2883 bytes)

* ROW mboutcapacity: FIX-NOW -- HIGH severity null pointer dereference or buffer overflow crash vector that must be fixed.
* ROW mipsbadvpnscale: FILE -- Unreproduced MED severity research finding to track in the defect backlog.
* ROW mipscachepriv: FILE -- MED severity state-mutation issue prior to privilege checks should be tracked.
* ROW mipscmpdenorm: FILE -- MED severity incorrect exception dispatch should be tracked.
* ROW mipscop0tail: FIX-NOW -- HIGH severity denial-of-service where a guest instruction halts the host emulator.
* ROW mipspsfault: FILE -- MED severity architectural compliance issue in exception signaling.
* ROW mipsr3kpcpriv: FILE -- Existing MED severity issue tracked in OUTSTANDING_BUGS requires filing.

## batch 79 -- `oldbatch_79/reply.txt` (3963 bytes)

* ROW ne2krxfilter: FILE -- Confirmed MED severity bug, explicitly verified as NOT FIXED by #554.
* ROW ne2krxphy: FILE -- Confirmed MED severity bug, explicitly verified as NOT FIXED by #554.
* ROW ne2ktsrstale: FILE -- Confirmed MED severity bug, explicitly verified as NOT FIXED by #554.
* ROW ne2kzerordc: FILE -- Confirmed MED severity bug, explicitly verified as NOT FIXED by #554.
* ROW oddoptinyband: FILE -- Confirmed MED severity bug, explicitly verified as NOT FIXED by #554.
* ROW ofopenexit: OWNER-DECISION -- The Argon scoping proposes a DECLINE + latched announce strategy requiring ruler approval.
* ROW ofpeerexit: OWNER-DECISION -- The Argon scoping proposes an ACCEPT strategy (return 0 with guarded deref) requiring ruler approval.

**Mechanical check of these batches (FIX-NOW / CLOSE-OVERTAKEN on a row that already carries commits):**

* none

## batch 62 -- `oldbatch_62/reply.txt` (3044 bytes)

* ROW armmrcr15flags: FILE -- Missing Rd=R15 flag semantics are still unpatched in dispatcher.
* ROW armoddpair: FILE -- Undefined LDRD/STRD pair transfer behavior remains listed in OUTSTANDING_BUGS.md.
* ROW armsa1110areset: FILE -- Contradictory SA-1110 reset state is confirmed unpatched.
* ROW armv6cachefmt: FILE -- Hardcoded v4/v5 layout requires addressing for v6.
* ROW armwarmflags: FILE -- Regression harness failure indicating ignored load/store remains unfixed.
* ROW armxchgname: FILE -- Interrupted reporting turns missing result into clean-slate SKIP.
* ROW asanemptyalias: FILE -- Parse failure for alias-less help line remains unfixed, conceded as MED severity.

## batch 66 -- `oldbatch_66/reply.txt` (3532 bytes)

* ROW dyncacheoffset32: FILE -- confirmed new high, conditional on cache size, not fixed yet.
* ROW ecoffoffsetspan: FILE -- confirmed high where table-offset guards admit negative offsets.
* ROW emulgzipfail: FILE -- confirmed high where gzip load failure terminates process.
* ROW fbdrainl2stale: FILE -- drafted as new med for phase 3 termination.
* ROW fbdrainloadpass: FILE -- revised to new med regarding the guest clock failure.
* ROW fbexternalclock: FILE -- confirmed new med missing timer consumption.
* ROW fbforkstatus: FILE -- conceded med due to ignored fork/waitpid failure.

## batch 69 -- `oldbatch_69/reply.txt` (2605 bytes)

* ROW heartirqdelivery: FILE -- keep as debt to track the existing outstanding bug entry
* ROW hpcenumstatus: FILE -- keep as debt for missing exit status evaluation
* ROW hpchenumrc: FILE -- keep as debt for subtype census failure on -H status
* ROW hrecordowed: FILE -- keep as debt until all 27 string-fix members are made or dropped
* ROW hygieneartifactlive: FILE -- keep as debt for the gate_hygiene masking bug
* ROW hygieneasczero: FILE -- keep as debt for the failing gate_hygiene pattern
* ROW hygienepmaxrawpanic: FILE -- keep as debt for the grep panic character bit 7 bug

## batch 70 -- `oldbatch_70/reply.txt` (2625 bytes)

* ROW hygienesweepmissing: UNSETTLED -- cannot be settled without regress/gate_hygiene.sh
* ROW i960disasmspan: UNSETTLED -- cannot be settled without cpu_i960_instr.c
* ROW ieeedsubsweep: UNSETTLED -- cannot be settled without regress/diff_ieee_store.c
* ROW ieeeinfrnvac: UNSETTLED -- cannot be settled without regress/diff_ieee_store.c
* ROW ieeequantumband: UNSETTLED -- cannot be settled without regress/diff_ieee_store.c
* ROW ieeesignmustdiffer: UNSETTLED -- cannot be settled without regress/diff_ieee_store.c
* ROW ieeesliverinf: UNSETTLED -- cannot be settled without regress/diff_ieee_store.c

## batch 72 -- `oldbatch_72/reply.txt` (2847 bytes)

* ROW lunabreaktmo: FILE -- Active MED severity defect in test script, not fixed.
* ROW lunaothersidle: FILE -- Active MED severity defect in test script, not fixed.
* ROW m88forkprobe: FILE -- Active MED severity probe defect, not fixed.
* ROW m88kbcndnest: FIX-NOW -- Host recursion without bound is a crash-on-malformed-input defect.
* ROW m88kconvdelivery: DROP -- Already tracked as an existing prose entry in OUTSTANDING_BUGS.md.
* ROW m88kconvodd: FIX-NOW -- Stopping the CPU is a crash-on-malformed-input defect; message needs fixing.
* ROW m88kdivcontext: FILE -- Active MED severity bug, not fixed.

## batch 73 -- `oldbatch_73/reply.txt` (3829 bytes)

* ROW m88kdumptail: FILE -- confirmed medium-severity parser defect missing guest-visible stores.
* ROW m88kextcross: FILE -- confirmed medium-severity logic defect in ext sign-extension.
* ROW m88kfpr0stop: FILE -- confirmed high-severity defect where rD=r0 stops the CPU incorrectly.
* ROW m88kidleslotsem: FILE -- confirmed prose entry for existing bug, properly consolidated.
* ROW m88knegdiv: FILE -- confirmed medium-severity div trapping defect.
* ROW m88kpairpadding: FILE -- confirmed medium-severity decoder defect rejecting valid register pairs.
* ROW m88kpsrbokill: FILE -- confirmed high-severity defect where BO bit flip stops the CPU.

## batch 74 -- `oldbatch_74/reply.txt` (3005 bytes)

* ROW m88ksddovf: FILE -- keep as debt, severity MED
* ROW m8dirtyfast: FILE -- keep as debt, severity MED
* ROW m8invcpuoneowner: FILE -- keep as debt, severity MED
* ROW m8inve9astorevac: FILE -- keep as debt, severity MED
* ROW m8invreadrc: FILE -- keep as debt, severity MED
* ROW m8supersegrow: FILE -- keep as debt, severity MED
* ROW mbcdbincomplete: FILE -- keep as debt, severity MED

## batch 76 -- `oldbatch_76/reply.txt` (3577 bytes)

* ROW mipsreadpriv: FILE -- Missing mfc0/dmfc0 READ-side check on fast paths
* ROW mipsresetalias: FILE -- Reboot sentinel incorrectly parses VIRTUAL address low bits
* ROW mipsrihang: FILE -- RI classification returns before missing PC, progressing observation gap
* ROW mipsrp54host: FILE -- Directed conversion regression matching host nearest
* ROW mipssamepcstore: FILE -- Load-to-store conversion incorrectly gated when store is at exception vector
* ROW mipssubmin: FILE -- SUB/DSUB overflow logic incorrectly evaluates MIN traps
* ROW mipssuperseg: FILE -- Supervisor mode translation incorrectly refuses mapped sseg/xsseg/csseg

## batch 77 -- `oldbatch_77/reply.txt` (3129 bytes)

* ROW mipssynci: FILE -- confirmed as a valid unhandled decoder case with MED severity.
* ROW mipstinyenable: FILE -- confirmed missing enabled-trap condition in coproc with MED severity.
* ROW mipstinyhostzero: FILE -- confirmed host rounding escape from the tiny trap with MED severity.
* ROW mipstinyprerm: FILE -- correctly extracted from OUTSTANDING_BUGS with MED severity.
* ROW mipstrapgate: FILE -- confirmed as ruler's addition for missing/reversed ISA gates with MED severity.
* ROW mk48aliasrow: FILE -- confirmed missing mutation coverage, upgraded to MED by harness consolidation.
* ROW mk48howdrop: FILE -- drafted as a new MED severity defect in test coverage/session logic.

## batch 78 -- `oldbatch_78/reply.txt` (3459 bytes)

* ROW mpstartupsp: FILE -- confirmed-new issue with known contract violation; retain as technical debt.
* ROW ne2kdmacmd: FILE -- confirmed-new issue from Astra wave 1; retain as technical debt.
* ROW ne2kloopback: FILE -- confirmed-new issue from Astra wave 1; retain as technical debt.
* ROW ne2kmontally: FILE -- confirmed-new issue from Astra wave 1; retain as technical debt.
* ROW ne2kparsync: FILE -- confirmed-new issue regarding TAP filtering; retain as technical debt.
* ROW ne2krxbudget: FILE -- confirmed-new high severity issue conditional on ingress bursts; retain as technical debt.
* ROW ne2krxfcs: FILE -- confirmed-new issue from Astra wave 1; retain as technical debt.

## batch 80 -- `oldbatch_80/reply.txt` (3475 bytes)

* ROW optinyband: FILE -- documented bug with confirmed MED severity.
* ROW optpinor: FILE -- documented recursive stack growth bug with HIGH severity.
* ROW osiopdnadexit: FILE -- tracked class row site with missing cases leading to exit, HIGH severity.
* ROW osiopregexit: FILE -- tracked class row site for register switch exit, HIGH severity.
* ROW osiopselectzero: FILE -- tracked class row site for scsi_ids_to_select==0 exit, HIGH severity.
* ROW osiopzeroram: FILE -- unguarded helpers rejecting zero-filled RAM causing halt, MED severity.
* ROW palgateabsent: FILE -- CPU stop defect conceded as MED severity instead of HIGH.

## batch 81 -- `oldbatch_81/reply.txt` (3080 bytes)

* ROW pcc2byterdovw: FILE -- Keep as debt (MED)
* ROW pcc2ctlhang: FILE -- Keep as debt (MED)
* ROW pcc2rxiackwrite: FILE -- Keep as debt (MED)
* ROW pcc2timerlanes: FILE -- Keep as debt (MED)
* ROW pitcounteraxis: FILE -- Keep as debt (MED)
* ROW pittickabsent: FILE -- Keep as debt (MED)
* ROW ppcbatppkill: FIX-NOW -- Replace fatal()+exit(1) with proper DSI/ISI exception generation

## batch 82 -- `oldbatch_82/reply.txt` (3059 bytes)

* ROW ppcbatstale: FILE -- severity MED, no witness yet, probe owed before edit
* ROW ppcdatahow: FILE -- open issue from regression harness, not fixed
* ROW ppcdsformxo: CLOSE-OVERTAKEN -- fixed by #571 and F2 adjudicators ruled LANDING
* ROW ppcenabldeliv: FILE -- tracks existing prose entry in OUTSTANDING_BUGS.md, not fixed
* ROW ppcfmarn: FILE -- tracks existing prose entry in OUTSTANDING_BUGS.md, not fixed
* ROW ppcfmasingle: FILE -- severity HIGH, stops emulator, rung-3 witness owed
* ROW ppcfprfclass: FILE -- tracks existing prose entry in OUTSTANDING_BUGS.md, not fixed

## batch 83 -- `oldbatch_83/reply.txt` (2544 bytes)

* ROW ppcfpstatus: FILE -- MED severity debt for missing FPSCR bit derivation in arithmetic handlers.
* ROW ppclfsupreload: FILE -- MED severity debt for regression harness issue preloading f1.
* ROW ppcllscsrr0: FILE -- MED severity debt for stale SRR0 on DSI during llsc.
* ROW ppcnanpayload: FILE -- MED severity debt for NaN payload loss in arithmetic handlers.
* ROW ppcsinglealias: FILE -- MED severity debt for fadds/fsubs not narrowing precision.
* ROW ppctblcarry: FIX-NOW -- keep TBL 32-bit in X(mftb)
* ROW ppcveinhibit: FILE -- MED severity debt for overwrites despite enabled VE.

## batch 84 -- `oldbatch_84/reply.txt` (3422 bytes)

* ROW probewiringheredocstrip: OWNER-DECISION -- A RULE QUESTION for the flagship regarding severity.
* ROW probewiringinterpopt: OWNER-DECISION -- A RULE QUESTION for the flagship regarding severity.
* ROW pvrdirtyregion: FIX-NOW -- Prevents a confirmed SIGFPE on zero display width.
* ROW pvrpal8888trunc: FIX-NOW -- Prevents data loss/truncation of a 32-bit palette entry.
* ROW qharmarchlevel: DROP -- Already tracked as an existing prose entry.
* ROW qharmexalign: DROP -- Already tracked as an existing prose entry.
* ROW qharmmediaver: DROP -- Already tracked as an existing prose entry.

## batch 85 -- `oldbatch_85/reply.txt` (2890 bytes)

* ROW qharmsxtadd: FILE -- open defect not fixed by #555, keep as MED debt.
* ROW qharmvsixunal: FILE -- open defect not fixed by #555, keep as MED debt.
* ROW qhfcsrflags: FILE -- open defect not fixed by #555, keep as MED debt.
* ROW qhlancestp: FILE -- open defect not fixed by #555, keep as MED debt.
* ROW qhm88kstops: FILE -- open defect not fixed by #555, keep as HIGH debt.
* ROW qhmbbufendstops: FIX-NOW -- bounds protection is needed to prevent indexed access out of bounds while averting a CPU stop.
* ROW qhmbphasestops: FIX-NOW -- remove the CPU stop but keep the early return for unsupported phases.

## batch 86 -- `oldbatch_86/reply.txt` (3916 bytes)

* ROW qhmbunimplstops: FIX-NOW -- clear mb89352_abort_on_unimplemented_stuff
* ROW qhmipsfastpriv: FILE -- keep as debt, severity MED
* ROW qhmipsps: FILE -- keep as debt, severity MED
* ROW qhppcdecode: FILE -- keep as debt, severity HIGH
* ROW qhppciphack: FILE -- keep as debt, severity HIGH
* ROW qhppcni: FILE -- keep as debt, severity MED
* ROW qhrdhwrpolicy: FILE -- keep as debt, severity HIGH

## batch 87 -- `oldbatch_87/reply.txt` (3548 bytes)

* ROW qhscifssr: FILE -- The issue is an existing bug not fixed by #555.
* ROW qhshdecode: FILE -- The issue is an existing bug not fixed by #555.
* ROW qhshfpexcept: FILE -- The issue is an existing bug not fixed by #555.
* ROW qhshsqat: FILE -- The issue is an existing bug not fixed by #555.
* ROW qhx11fifo: FILE -- The issue is an existing bug not fixed by #555.
* ROW ramnulltail: FILE -- The issue is a confirmed new bug not fixed by #554.
* ROW ramspaninval: FILE -- The issue is an existing bug not fixed by #554.

## batch 88 -- `oldbatch_88/reply.txt` (4327 bytes)

* ROW rldiclvacrow: FILE -- guest-visible wrong register value qualifies as a MED severity issue.
* ROW rotcsentinelc: FILE -- draft identifies rotated-immediate halt leaving sentinel as an outstanding MED issue.
* ROW rtcpendovf: FILE -- negative wrap on pending_interrupts breaks the documented delivery behavior.
* ROW scsicapnosense: FILE -- CHECK CONDITION returning with a cleared sense latch fits MED severity.
* ROW sentinelrawswap: FILE -- unrecorded flag-probe sentinels checking raw token deadbeef must be tracked.
* ROW sgialiaspace: FIX-NOW -- exit(1) process termination perfectly matches the project mandate of fixing crash-on-malformed-input defects.
* ROW sgiat1count: OWNER-DECISION -- requires flagship ruling on HIGH severity policy when a preventative check misses a class without a live instance.

## batch 90 -- `oldbatch_90/reply.txt` (3665 bytes)

* ROW sh4tmupending: FIX-NOW -- cap the underflow accumulation to a single status bit
* ROW sh4utlbmultihit: FIX-NOW -- modify UTLB walker to check all entries for multihits
* ROW shbcr3mask: FIX-NOW -- mask out reserved bits 12:1 on write
* ROW shblreset: CLOSE-OVERTAKEN -- overtaken by commit bb672a16, awaiting Fable review
* ROW shdnoperand: FIX-NOW -- zero denormalized operands on read if FPSCR.DN=1
* ROW shfcnvsdfpul: CLOSE-OVERTAKEN -- overtaken by commit 7ccd4e42, awaiting Fable review
* ROW shfmovalign: FILE -- record the redundant alignment check as technical debt

## batch 91 -- `oldbatch_91/reply.txt` (4093 bytes)

* ROW shhaltsilent: FILE -- MED severity, test harness strictly enforces survival
* ROW shifetchkill: FIX-NOW -- HIGH severity, guest instruction fetch can kill emulator process
* ROW shinttieorder: FILE -- MED severity, interrupt priority logic deviation
* ROW shnestedbranch: FILE -- MED severity, incorrect exception handling for nested delay slot
* ROW shoddprfield: OWNER-DECISION -- Needs ruling on out-of-bounds struct access severity
* ROW shrcr1af: FILE -- MED severity, existing tracked defect
* ROW shreservedexit: FIX-NOW -- HIGH severity, guest memory access kills emulator

## batch 92 -- `oldbatch_92/reply.txt` (2734 bytes)

* ROW shresetinit: FILE -- legitimate defect confirmed by Astra, needs tracking.
* ROW shrtcsrkey: FILE -- confirmed outstanding issue in emulator state.
* ROW shslotres: FILE -- identified incorrect trap code needs tracking.
* ROW shtcrunf: FILE -- verified TCR write bug in OUTSTANDING_BUGS.md.
* ROW shuseraddr: FILE -- verified user access bug in OUTSTANDING_BUGS.md.
* ROW shwcrreset: FILE -- verified WCR3 reset bug in OUTSTANDING_BUGS.md.
* ROW siuparenarith: FILE -- regression harness identified parsing defect, needs tracking.

## batch 94 -- `oldbatch_94/reply.txt` (4692 bytes)

* ROW timerhundredexpands: FILE -- keep as debt (MED) due to CANNOT-FAIL regression harness defect.
* ROW timerupdrow: FILE -- keep as debt (MED) due to test coverage gap missing a state store.
* ROW upstreambinarydiff: FILE -- keep as debt (MED) due to SELECTS-NOTHING silent pass on binary diffs.
* ROW vgadirtyarm: OWNER-DECISION -- flagship must adjudicate disputed HIGH severity regarding unmeasured redraw time.
* ROW wdcblock0survive: FILE -- keep as debt (MED) due to CANNOT-FAIL block 0 survival oracle flaw.
* ROW wdcchildstatus: OWNER-DECISION -- flagship must answer rule question on HIGH grading for preventive check missing a severe class.
* ROW wdccontrol0discard: FILE -- keep as debt (MED) because control 0 probe failures are discarded.

## batch 95 -- `oldbatch_95/reply.txt` (2395 bytes)

* ROW wdcnien: FILE -- Missing nIEN check in wdc.
* ROW wdcopcodealloc: FILE -- Allocation failure skips cases.
* ROW wdcphasefixture: FILE -- Ten-byte fixtures miss dispatch.
* ROW wdcslavegeomgrep: FILE -- Grep matches capacity-only string.
* ROW wdcsoftresetflush: FILE -- Missing flush on soft reset.
* ROW wdcstalephasepkt: FILE -- Phase reset masks packet-flag removal.
* ROW wdctimeoutscore: FILE -- Timeout scored as measured failure.

## batch 96 -- `oldbatch_96/reply.txt` (3928 bytes)

* ROW wirereassign: OWNER-DECISION -- The flagship reviewer must rule on the severity definition for static checker defects.
* ROW writeflusherr: FILE -- Keep as debt, MED severity, as the guest-triggerable host data loss is confirmed but unwitnessed in a new probe.
* ROW x11alloc32: FIX-NOW -- Integer wrap on resize allocation requires an immediate overflow check before memory allocation.
* ROW xscalecp6exits: FIX-NOW -- Guest instructions terminating the host process directly violate the emulator's robustness constraints and must be handled as exceptions.
* ROW heldrecedits: FIX-NOW -- Apply the 30 held doc and comment string edits to the source tree after rebasing on HEAD.
* ROW armspsrthumb: FILE -- Keep as debt (MEDIUM); requires a rung-3 probe to successfully witness the CPU behavior before fixing.
* ROW armusrstop: FILE -- Unwitnessed guest DoS must be reproduced by a rung-3 probe before committing a fix; keep as debt.

## batch 99 -- `oldbatch_99/reply.txt` (4006 bytes)

* ROW agyselfupdate: FILE -- all three seats filed as low and it owes a script fix for the pre-flight check mapping.
* ROW asccmdwidecount: FILE -- all three seats filed as high but it still owes a rung-3 witness attempt prior to editing.
* ROW batterystandby: OWNER-DECISION -- the remedy requires an owner decision regarding the machine's power policy.
* ROW dashmissingd: OWNER-DECISION -- requires Q2 adjudicator ruling and owner weighing on a new entry-scoped token.
* ROW m88kresidtbdslot: FILE -- predicted coverage gap is not yet measured and gets kept as low-severity debt.
* ROW m88kutrapdslot: FILE -- disclosed clause-(e) coverage debt classified as voluntary and tracked as low severity.
* ROW mipssyscallprom: FILE -- all three seats filed as high but it owes manual review of the AI attempt before counting as a witness.

## batch 100 -- `oldbatch_100/reply.txt` (3695 bytes)

* ROW ofemulnodata: FIX-NOW -- gating at the decoders is required for the crash defect
* ROW panelshrefused: OWNER-DECISION -- owner must rule whether to bypass the never-commit policy
* ROW seatverdictrefusal: FILE -- low severity behavior to be disclosed and kept as debt
* ROW wdczerolendatain: FILE -- low severity presentation issue lacking a rung-3 consequence proof
* ROW cxlaunchcov: DOCUMENT-AND-CLOSE -- no floor breach and already disclosed in the contract
* ROW dashokcov: FILE -- ranked below live defects, kept as debt for a future round
* ROW ip30stallgreen: FIX-NOW -- requires a per-session completion marker

## batch 103 -- `oldbatch_103/reply.txt` (3616 bytes)

* ROW m88kbuserrregs: CLOSE-OVERTAKEN -- #570 landed, pending Fable 5.1 hold.
* ROW m88kscaledbyte: CLOSE-OVERTAKEN -- #569 landed, pending Fable 5.1 hold.
* ROW vmeprobedebt: FILE -- explicitly ranked as coverage debt.
* ROW vmewarnedbit: FIX-NOW -- one shared macro fixes both sides of the index edit.
* ROW wdclbaaddr: OWNER-DECISION -- procedural ruling on roster-excused seats required.
* ROW alphamakedep: FIX-NOW -- one-line build dependency port.
* ROW armmmufaultlog: FIX-NOW -- one-line log flood fix port.

## batch 104 -- `oldbatch_104/reply.txt` (2951 bytes)

* ROW ascbugprintf: FILE -- Keep as debt (LOW)
* ROW asccfg1id: FILE -- Keep as debt (MED)
* ROW ascselatn: FILE -- Keep as debt (MED)
* ROW be300fbbpp: FILE -- Keep as debt (MED)
* ROW bpstringarg: OWNER-DECISION -- Needs upstream deletion porting or a bespoke design.
* ROW bt459retrace: FILE -- Keep as debt (MED)
* ROW cdcapround: FILE -- Keep as debt (MED)

## batch 108 -- `oldbatch_108/reply.txt` (2641 bytes)

* ROW ioasicintrclr: FIX-NOW -- port rpajarola e108b54
* ROW leloopback: FIX-NOW -- port rpajarola d1f0720
* ROW lermd3fcs: FIX-NOW -- port rpajarola d1f0720
* ROW lesarom: FIX-NOW -- port rpajarola 0c1e6d1
* ROW m88kcarryundec: FIX-NOW -- port r6577(n) X(sub) for 0x74 and design carry forms
* ROW m88koutsideram: FIX-NOW -- port ajfa mvme187 4a01173 patch 02 / upstream 4e3e72b1
* ROW m88kpsrreserved: FIX-NOW -- port ajfa mvme187 4a01173 patch 01 mask

**Mechanical check of these batches (FIX-NOW / CLOSE-OVERTAKEN on a row that already carries commits):**

* `ppcdsformxo` (batch 82): CLOSE-OVERTAKEN, but the row already carries commits `cb21331c` -- its own round shipped; what it owes is its held stage.
* `shblreset` (batch 90): CLOSE-OVERTAKEN, but the row already carries commits `bb672a16` -- its own round shipped; what it owes is its held stage.
* `shfcnvsdfpul` (batch 90): CLOSE-OVERTAKEN, but the row already carries commits `7ccd4e42` -- its own round shipped; what it owes is its held stage.
* `m88kbuserrregs` (batch 103): CLOSE-OVERTAKEN, but the row already carries commits `c8fcb5ff` -- its own round shipped; what it owes is its held stage.
* `m88kscaledbyte` (batch 103): CLOSE-OVERTAKEN, but the row already carries commits `66920157` -- its own round shipped; what it owes is its held stage.

## batch 89 -- `oldbatch_89/reply.txt` (3312 bytes)

* ROW sgideprimbitslive: OWNER-DECISION -- The severity is disputed and explicitly flagged as a rule question for the flagship reviewer.
* ROW sgilosent2: FILE -- Uncontested MED severity issue to be tracked as debt.
* ROW sgilwreadzero: OWNER-DECISION -- The severity upgrade is disputed and explicitly flagged as a rule question for the flagship reviewer.
* ROW sh4c7fetch: FILE -- Uncontested (conceded) MED severity issue to be tracked as debt.
* ROW sh4hangoracle: FILE -- Uncontested (conceded) MED severity issue to be tracked as debt.
* ROW sh4rptincompleterun: FILE -- Uncontested MED severity issue to be tracked as debt.
* ROW sh4tmuirqidx: FILE -- Uncontested MED severity issue to be tracked as debt.

## batch 93 -- `oldbatch_93/reply.txt` (2016 bytes)

* ROW stalelbsbound: FILE -- Keep as debt; severity MED
* ROW subpagecache: FILE -- Keep as debt; severity MED
* ROW swpctxnoop: FILE -- Keep as debt; severity MED
* ROW symdemanglebound: FILE -- Keep as debt; severity HIGH
* ROW taprxquota: FILE -- Keep as debt; severity HIGH
* ROW tcpdebugopts: FILE -- Keep as debt; severity HIGH
* ROW thumbrorstale: FILE -- Keep as debt; severity MED

## batch 97 -- `oldbatch_97/reply.txt` (4004 bytes)

* ROW armmsrmodedebt: FIX-NOW -- gate parser check must be keyed on verdict, repair and re-table owed
* ROW armthumbabtlr: FIX-NOW -- correct Thumb-state abort return address offsets
* ROW armusrwarmap: FIX-NOW -- fast path lacks invalidation on mode change and bypasses AP check
* ROW fablequeueregress: FIX-NOW -- check_fable_queue.py skips fable5 regress holds by continuing early
* ROW headerstaleobj: FIX-NOW -- propagate_all_trees.sh leaves objects compiled against old headers stale
* ROW nullmediumlegs: FILE -- alpha_tbi_probe.py null-medium leg is still owed
* ROW nullmediumsweep: FIX-NOW -- provide the owed reproducible census of the clause (c) labels

## batch 98 -- `oldbatch_98/reply.txt` (3463 bytes)

* ROW pcc2c040assertxor: FILE -- Owner answered to keep the written rule, stays clause-(e) debt.
* ROW pcc2c040warnedeq: FILE -- Ranked below live defects as clause-(e) debt.
* ROW ppcshiftwide: OWNER-DECISION -- Waiting on owner's call regarding the witness block reach.
* ROW ppcsrdmissing: OWNER-DECISION -- Waiting on owner's call regarding the witness block reach.
* ROW sgirecontentslice: FILE -- Coverage debt designated to ship the next time the instrument is opened.
* ROW stagetokenscontrols: FIX-NOW -- Shape to adopt is already defined as a single commit with 7 variants and a re-pin.
* ROW vmewidthlanes: FILE -- Marked LOW severity because the in-tree guest does not trigger the sub-word access fault.

## batch 102 -- `oldbatch_102/reply.txt` (4408 bytes)

* ROW fbctrlvec128: FIX-NOW -- requires a rung-3 witness and a disposition for len > 8 stores on both arms
* ROW gate16fence: FIX-NOW -- wrap each probe launch in timeout(1) and red on exit 124
* ROW ip30selftest3233: FIX-NOW -- add a sixteenth case where all 33 rows are ok and RESULT=32/33 that must red
* ROW rldiclanchor: FIX-NOW -- anchor observed GOT values on the existing per-row grep lines
* ROW armrebootmagic: FIX-NOW -- gate the word to cats with PROM emulation and appropriate privilege level
* ROW i8259eoiirr: OWNER-DECISION -- requires owner ruling on roster seats, Fable hold, and filing of Argon's answers
* ROW lecsrmask: OWNER-DECISION -- requires owner ruling on roster seats, Fable hold, and unmeasured variant table

## batch 106 -- `oldbatch_106/reply.txt` (3560 bytes)

* ROW dc7085trdy: FILE -- research finding not yet reproduced locally, kept as MED debt.
* ROW dcgdromabort: FILE -- research finding not yet reproduced locally, kept as MED debt.
* ROW dupidcheck: CLOSE-OVERTAKEN -- remedy ships in its own separate harness round with negative controls.
* ROW dyntransnoexc: FILE -- research finding not yet reproduced locally, kept as MED debt.
* ROW eaglecfglanes: FILE -- research finding not yet reproduced locally, kept as MED debt.
* ROW eaglememctl: FILE -- research finding not yet reproduced locally, kept as MED debt.
* ROW emulflushcpu0: FILE -- research finding not yet reproduced locally, kept as MED debt.

## batch 107 -- `oldbatch_107/reply.txt` (2584 bytes)

* ROW gcc16unused: FILE -- a design is owed for the unused locals
* ROW i8259icw4: FIX-NOW -- port rs6000 598ab10 is available
* ROW i8259isrnever: FIX-NOW -- port rs6000 598ab10, rs6000 174448c is available
* ROW intenablelatency: FILE -- a design is owed for the interrupt delivery delay
* ROW ioasic3minscc: FIX-NOW -- port rpajarola 7aeae85 is available
* ROW ioasic3minscsi: FIX-NOW -- port rpajarola bee311c is available
* ROW ioasicesar: FIX-NOW -- port rpajarola e108b54 is available

## batch 111 -- `oldbatch_111/reply.txt` (4610 bytes)

* ROW mipscountidle: FIX-NOW -- port jroark 45b34df
* ROW mipscountrate: FIX-NOW -- port jroark dabf5ce and b041121
* ROW mipscountread: FIX-NOW -- port jroark dc55abc and 445d32d
* ROW mipsdivwrap: FIX-NOW -- port CHERI 1236c18 result value only
* ROW mipsebase: FIX-NOW -- port klx3300 8f94a57
* ROW mipsmovciundec: FILE -- keep as debt until a design is provided
* ROW mipspagemaskdead: CLOSE-OVERTAKEN -- handle in VR41xx 1 KB-page round (T11)

## batch 112 -- `oldbatch_112/reply.txt` (3762 bytes)

* ROW mipspromemulexc: FILE -- lack of a complete portable fix and reproducer means it stays as MED debt.
* ROW mipsr3010irq: FILE -- lack of a complete portable fix and reproducer means it stays as MED debt.
* ROW mipsrecipdecode: FILE -- requires a structural design since no portable fix exists, keep as MED debt.
* ROW mipssubpageram: FIX-NOW -- register the whole page for sub-page devices.
* ROW mipssyncmips1: FILE -- missing a portable fix design, keep as MED debt.
* ROW mk48clock: FIX-NOW -- port ajfa mvme187 4a01173 patch 06.
* ROW mk48multibyte: FIX-NOW -- port ajfa mvme187 4a01173 patch 06.

## batch 116 -- `oldbatch_116/reply.txt` (3552 bytes)

* ROW ppcintentrymsr: FIX-NOW -- Port commits and clear ME along with IR/DR flush
* ROW ppcisisrr1: FIX-NOW -- Port partial fixes excluding no-execute/guarded ISI bit
* ROW ppclswizero: FIX-NOW -- Port the mentioned commits to fix zero-fills and shifts
* ROW ppclswxundec: FIX-NOW -- Port the mentioned commits to decode lswx/stswx
* ROW ppcoeundec: FIX-NOW -- Port partial OE fixes, excluding CA rewrite
* ROW ppcpterc: FIX-NOW -- Port with changes to keep RW pages read-only until first store
* ROW ppcsprg2drop: FIX-NOW -- Port the commit and enforce privilege check on SPRG2 writes

## batch 120 -- `oldbatch_120/reply.txt` (3795 bytes)

* ROW vr4131regmap: FILE -- lacks a manual to verify the register map, explicitly ruled not to port as-is
* ROW vr4131siuinuse: FIX-NOW -- port jroark 3c3d5cb to register the extra SIU as not in use
* ROW vr41xx1kpage: FILE -- no fork fixes it and a design for 1 KB-page translation is owed
* ROW x11cursorclip: FIX-NOW -- port rpajarola fe69c7b and clamp against visible size in dev_fb_setcursor
* ROW x11keycodes: FIX-NOW -- port rpajarola 1a27ff9 to support evdev keycodes
* ROW drvdiscrimloss: FILE -- positive control remedy is not mandatory now but kept as low-severity debt
* ROW m88kifetchhalt: FILE -- impact on multi-cpu and other ISAs is unmeasured, needs a proper design to land

**Mechanical check of these batches (FIX-NOW / CLOSE-OVERTAKEN on a row that already carries commits):**

* none

## batch 101 -- `oldbatch_101/reply.txt` (4086 bytes)

* ROW mtedeclinecov: FILE -- Explicitly marked as coverage debt and ranked below live defects.
* ROW mteimplement: FILE -- Feature work requiring linear semantics, not a defect.
* ROW mtesrcfill: OWNER-DECISION -- Clarification of hardware behavior is needed to determine the correct semantics.
* ROW mtestartread: OWNER-DECISION -- Requires hardware documentation to rule if a read starts the engine.
* ROW ppcrldiclbanner: FILE -- Cosmetic split note issue deliberately deferred to a future probe edit round.
* ROW sgimteystep: FIX-NOW -- Unlatched fatal message missing a newline creates a log flood vulnerability.
* ROW fbctrlobsgrid: FILE -- The owner already ruled to land this coverage gap as filed debt.

## batch 105 -- `oldbatch_105/reply.txt` (2615 bytes)

* ROW clmpccmsvr: FIX-NOW -- Portable fix available upstream.
* ROW configurerpath: FIX-NOW -- Portable fix available from Fedora.
* ROW cpunewstores: FIX-NOW -- Portable fix available upstream.
* ROW cpurunningtype: FIX-NOW -- Portable fix available upstream.
* ROW dbgdevremove: FILE -- HIGH severity and a design is owed.
* ROW dbgmakedep: FIX-NOW -- Portable fix available upstream.
* ROW dc7085cts: FIX-NOW -- Portable fix available upstream.

## batch 109 -- `oldbatch_109/reply.txt` (2669 bytes)

* ROW m88kwtbit: DOCUMENT-AND-CLOSE -- text explicitly rules 'do not port .wt-as-a-hint'
* ROW m88kxmemr0: FILE -- no fix found and a design is owed, keep as MED debt.
* ROW m88kxmemusr: FILE -- no fix found and a design is owed, keep as MED debt.
* ROW m88kzeroword: FIX-NOW -- port ajfa mvme187 4a01173 patch 01.
* ROW mb89352bfint: FIX-NOW -- port upstream a1cafe7c.
* ROW mb89352fmtargs: FIX-NOW -- port upstream 8f4c717f.
* ROW mb89352psns: FIX-NOW -- port upstream a1cafe7c.

## batch 110 -- `oldbatch_110/reply.txt` (3526 bytes)

* ROW mb89352scmd: FIX-NOW -- portable fix is fully identified from upstream commits
* ROW mc146818reg63: FIX-NOW -- portable fix is ready from rpajarola 871e551
* ROW mc146818settime: FILE -- fix is partial/conceptual and requires avoiding upstream bugs
* ROW mc146818uie: FIX-NOW -- portable fix is ready from rpajarola 871e551
* ROW mips4kcfpu: FILE -- fix is partial and has cascading dependencies on evbmips defaults
* ROW mipscop0cpu: FIX-NOW -- portable fix is ready from rpajarola 12306ee
* ROW mipscop1xcpu: FILE -- no portable fix available, explicit design is owed

## batch 113 -- `oldbatch_113/reply.txt` (3037 bytes)

* ROW natconnfail: FIX-NOW -- port rpajarola 1c18c2b
* ROW natdhcpreply: FIX-NOW -- port jroark ba17c36
* ROW ns16550iirid: FIX-NOW -- port jroark 2a1a395
* ROW osiopcalltemp: FIX-NOW -- port ajfa mvme187 4a01173 patch 04
* ROW osiopdmainval: FIX-NOW -- port ajfa mvme187 4a01173 patch 04
* ROW osiopsigp: FIX-NOW -- port ajfa mvme187 4a01173 patch 04
* ROW osiopwidelanes: FIX-NOW -- port ajfa mvme187 4a01173 patch 04

## batch 114 -- `oldbatch_114/reply.txt` (2741 bytes)

* ROW pccmosnmi: FIX-NOW -- port the masking of rs6000 bb32945
* ROW pcicfgaddrlow: FIX-NOW -- port rs6000 eb4c571
* ROW pckbcauxecho: FIX-NOW -- port routing part of rs6000 d2ff00e, rs6000 94e3ed4
* ROW pckbcgetid: FIX-NOW -- port rs6000 94e3ed4
* ROW pckbcledparam: FIX-NOW -- port rs6000 d2ff00e, rs6000 c861ff6
* ROW pckbcselftest: FIX-NOW -- port rs6000 9bda09a, rs6000 ca2377f, rs6000 c861ff6 (not the IBM-specific extra 0xB2)
* ROW pmax3minslotnr: FIX-NOW -- port rpajarola 042b61b

## batch 115 -- `oldbatch_115/reply.txt` (2006 bytes)

* ROW pmaxsystype: FIX-NOW -- Port available from rpajarola 12306ee
* ROW ppc601xlateexit: FILE -- Needs a design, no portable fix available
* ROW ppc64xlateexit: FILE -- Requires a large design (64-bit page-table walker)
* ROW ppccrnandundec: FIX-NOW -- Port available from rs6000 2ec64fd
* ROW ppcdcbiundec: FIX-NOW -- Ports available from rs6000
* ROW ppcdecwrite: FIX-NOW -- Port available from rs6000 241f5e2
* ROW ppcexcfatal: FIX-NOW -- Port upstream 6d2d8bf0 at INFO level

## batch 117 -- `oldbatch_117/reply.txt` (3552 bytes)

* ROW ppctlbieseg: FIX-NOW -- port rs6000 59cc410 and 3dafe76
* ROW ppctwundec: FIX-NOW -- port rs6000 0281590, 6ac4dc4, 8bcf95a, ef62ef6
* ROW ppcupdatera0: FILE -- lack of a complete portable fix; requires independent work
* ROW pristinesecondref: OWNER-DECISION -- non-defect records request; requires maintainer ruling
* ROW rarpaddr: FIX-NOW -- port rpajarola a4f5ea2
* ROW scc3minlines: FIX-NOW -- port rpajarola 5d3e9ee
* ROW sccintpend: FIX-NOW -- port rpajarola 2dfd6ec, 7aeae85, a99af56

## batch 118 -- `oldbatch_118/reply.txt` (2937 bytes)

* ROW sccloopback: FIX-NOW -- port rpajarola 2dfd6ec, rpajarola a99af56
* ROW sccresets: FIX-NOW -- port rpajarola 2dfd6ec, rpajarola a99af56
* ROW sccwr0ptr: FIX-NOW -- port rpajarola 2dfd6ec
* ROW scsievpd: FIX-NOW -- port rs6000 554e135, rs6000 24cb943
* ROW scsimodeselhdr: FIX-NOW -- port rpajarola d685ed0, rpajarola 39f3fbf keeping #133's 256..8192 bound
* ROW scsimodesensepc: FIX-NOW -- port rs6000 9ef1d3e, rs6000 24cb943
* ROW shsyncodisasm: FIX-NOW -- port pkgsrc patch-src_cpus_cpu__sh.c

## batch 119 -- `oldbatch_119/reply.txt` (3370 bytes)

* ROW shsyncofeature: OWNER-DECISION -- requires owner to decide on adopting the NOP
* ROW singlestepdecl: FIX-NOW -- port upstream 6d2d8bf0
* ROW smpcodeinval: FILE -- wait for T147 or implement full all-CPU write revocation
* ROW tapeeofzero: FILE -- requires a proper design, no portable fix exists
* ROW tcemptyslot: FIX-NOW -- port rpajarola 042b61b
* ROW tlbwrrandom: FIX-NOW -- port upstream 90db505f with WIRED guard
* ROW vr4131hibernate: FILE -- needs verification against actual VR4131 manual

## batch 122 -- `oldbatch_122/reply.txt` (3049 bytes)

* ROW m88kbuserrdebt: FILE -- keep as debt for detector coverage.
* ROW m88kcitedrift570: FILE -- re-key citations in a dedicated records round.
* ROW ppc64on32gate: FILE -- uniform fix for the missing width gate requires its own round.
* ROW ppcdisasmfpupd: FILE -- requires a disassembler-only edit with its own census oracle.
* ROW ppcdisasmxo: FILE -- requires an oracle-correction order to un-fold XO from displacement.
* ROW ppcldxabsent: FILE -- requires adding opcodes to prevent guest-cpu-stop on indexed loads.
* ROW wdclbaadvertise: FILE -- guest-visible behaviour change requires measured warrant gate.

## batch 123 -- `oldbatch_123/reply.txt` (4439 bytes)

* ROW wdclbaimage: FILE -- Coverage debt for larger image testing.
* ROW wdcmediastatus: FILE -- Pre-existing defect not fixed in the current round.
* ROW wiringwitnessclass: FIX-NOW -- Perform MANIFEST re-classification of earlier entries.
* ROW algorisaintclear: FILE -- Wrong result on Algor reads, but no witness machine to verify against.
* ROW i8259aeoi: DOCUMENT-AND-CLOSE -- The output line doesn't consult ISR so no interrupt is lost.
* ROW i8259cascline: FILE -- Coverage debt for a session with two pic2 sources.
* ROW i8259icwreset: FIX-NOW -- Requires two straightforward assignments in the ICW1 arm.

## batch 124 -- `oldbatch_124/reply.txt` (3304 bytes)

* ROW i8259ltim: DOCUMENT-AND-CLOSE -- The emulator model is edge-only and documented guests use edge mode.
* ROW i8259ocw2nonspec: FILE -- Low severity wrong-result that is explicitly excluded from this round's edits.
* ROW i8259ocw3revert: DOCUMENT-AND-CLOSE -- The approximation is unobserved by documented guests.
* ROW i8259priority: DOCUMENT-AND-CLOSE -- Missing priority inhibition does not impact known guests as they mask in handlers.
* ROW i8259smm: DOCUMENT-AND-CLOSE -- SMM absence is functionally benign since ISR inhibition is already absent.
* ROW lecsr12readback: DOCUMENT-AND-CLOSE -- The read-back behavior is pinned by contract rows and documented.
* ROW lecsr3inert: DOCUMENT-AND-CLOSE -- Stored CSR3 bits are unconsulted because the model does not emulate DMA byte lanes.

## batch 127 -- `oldbatch_127/reply.txt` (3406 bytes)

* ROW armldrexprev6: FIX-NOW -- requires an ARMv6 version check to prevent executing undefined instructions.
* ROW armstrexgranule: FIX-NOW -- requires correcting the mask to use high bits instead of low bits.
* ROW bootblockzeroaddr: FIX-NOW -- host process should not exit(1) on malformed guest disk images.
* ROW bt455offsetovf: FILE -- genuine out-of-bounds write but practically unreachable count.
* ROW catsmemwrap: FIX-NOW -- requires a 64-bit cast to handle >4GB RAM arguments properly.
* ROW debugmsgalloc: FILE -- host OOM missing NULL checks is low priority.
* ROW debugmsgstrdup: FILE -- host OOM missing NULL checks is low priority.

## batch 128 -- `oldbatch_128/reply.txt` (3188 bytes)

* ROW dec5800ncpushift: FIX-NOW -- Signed 32-bit shift overflows when ncpus >= 31, causing undefined behavior.
* ROW decpromstrcap: FIX-NOW -- Unbounded memory reads allow guest to force host into infinite loops or excessive work.
* ROW devstrnamequote: FIX-NOW -- Subtracting 2 from length 1 causes underflow to SIZE_MAX and buffer issues.
* ROW dyntransstatsbuf: FIX-NOW -- snprintf size parameter must be the remaining buffer size, not the total size.
* ROW ecoffclampdead: FIX-NOW -- fread overwrites the clamped length by reading the full chunk_size, causing out-of-bounds writes.
* ROW fbscaledownoob: FIX-NOW -- Rounding up can push update_y2 past the end of the framebuffer, causing OOB reads.
* ROW hpcmipsalloc: FIX-NOW -- Unchecked malloc allows snprintf to write to a NULL pointer if allocation fails.

## batch 131 -- `oldbatch_131/reply.txt` (4595 bytes)

* ROW leineastop: FILE -- WRONG-RESULT defect that does not cause a crash on malformed input.
* ROW m88kaluignored: FIX-NOW -- Malformed undecoded input crashes the emulator via goto bad, violating robustness goals.
* ROW m88kfpprivvector: OWNER-DECISION -- Conflicting Motorola manual entries require an authoritative source to resolve.
* ROW m88kfstcrro: FILE -- WRONG-RESULT defect (supervisor only) that does not crash the emulator.
* ROW m88kldausr: FILE -- WRONG-RESULT defect skipping a privilege check that does not crash the emulator.
* ROW m88kldcrunimpl: FIX-NOW -- Unimplemented register access crashes the emulator via run-loop termination, violating robustness goals.
* ROW m88kr0overflow: FILE -- WRONG-RESULT defect skipping architectural exceptions that does not crash the emulator.

## batch 132 -- `oldbatch_132/reply.txt` (2948 bytes)

* ROW m88kresetpsr: FILE -- The dispute pass already ruled FILE for this register reset defect.
* ROW m88krteabort: FILE -- Included in the cpusexitsweep umbrella for CPU-STOP issues.
* ROW m88ksfudecodestop: FILE -- The code candidates review consensus ruled FILE with Astra's corrected vectors.
* ROW m88kstcrunimpl: FILE -- Included in the cpusexitsweep umbrella for supervisor CPU-STOP defects.
* ROW machinewatchwrap: FILE -- Latent watchpoint wrap defect filed via Argon file audits.
* ROW mc146818gmtime: FILE -- Host-only NULL dereference filed via Argon audits.
* ROW mipsbc0fnop: FILE -- Consensus is FILE as part of the mipscop0tail round.

## batch 135 -- `oldbatch_135/reply.txt` (3602 bytes)

* ROW mipsr5900lqsq: FILE -- ASTRA_VS_FABLE consensus identifies this as a valid debt item for R5900 LQ/SQ.
* ROW mipsrorvgate: FILE -- Despite the pre-R2 premise being rated UNSETTLED, the consensus FILE designation remains for the rest of the scope.
* ROW mipsshiftrsvd: FILE -- Consensus FILE for handling reserved shift encodings by architecturally raising RI instead of halting.
* ROW mipsspecial2rsvd: FILE -- Missing SPECIAL2 cases should raise an RI exception rather than terminating via the default goto bad.
* ROW mipsspecial3undec: FILE -- Unimplemented SPECIAL3 function codes need architectural RI signaling instead of an emulator stop.
* ROW mipsspecialrsvd: FILE -- Reserved SPECIAL codes erroneously trigger a CPU stop instead of throwing the mandated RI exception.
* ROW mipstlbpfnhigh: FIX-NOW -- 32-bit bitwise NOT on pmask zero-extends to 64-bit, catastrophically clearing the high physical address bits.

## batch 136 -- `oldbatch_136/reply.txt` (3404 bytes)

* ROW mipswaitcode: FILE -- Marked explicitly as a consensus FILE in the ledger evidence.
* ROW mipsx64missing: FILE -- Marked explicitly as a consensus FILE in the ledger evidence.
* ROW mk48gmtime: FIX-NOW -- Critical but simple host-side NULL dereference.
* ROW mpipimemmove: FIX-NOW -- Direct calculation error in memmove sizing that breaks the IPI queue.
* ROW nanencoding: FILE -- Marked explicitly as a consensus FILE in the ledger evidence.
* ROW ns16550out2hold: FIX-NOW -- Clear state machine logic gap causing stuck device lines.
* ROW palputslen: FIX-NOW -- Unbounded iteration allowing trivial infinite looping or wrapping defects.

**Mechanical check of these batches (FIX-NOW / CLOSE-OVERTAKEN on a row that already carries commits):**

* none

## batch 121 -- `oldbatch_121/reply.txt` (3305 bytes)

* ROW m88klepsrbo: FILE -- Defect is source-established and outside current contract, severity MED.
* ROW m88kstepprefetch: FILE -- Debugger state change class, low severity.
* ROW m88kunclaimedberr: OWNER-DECISION -- Awaiting hardware documentation to confirm BERR behavior.
* ROW m88kxmemaddrovl: FILE -- Unmeasured wrong-address defect outside current contract, severity MED.
* ROW mvme187cmmuowner: FILE -- Bootstrap CPU mismatch defect is unmeasured and outside contract.
* ROW rosterexcused: FIX-NOW -- Tooling change needed to allow stage token to record owner-excluded seats.
* ROW shdrivercliff: FIX-NOW -- Harness round needed to extend wiring checks to shell drivers.

## batch 125 -- `oldbatch_125/reply.txt` (3506 bytes)

* ROW lecsr3stopclear: FILE -- behaviour is a lack of guarantee rather than required
* ROW lecsrgateoutdir: FIX-NOW -- pass LOGDIR and update the probe invocation
* ROW lediagfmt: FILE -- deferred formatting cast fixes for a future round
* ROW lestopgate: FILE -- gating behaviour change requires its own witness probe
* ROW pit8253count0: FIX-NOW -- map 0 to 65536 to prevent the timer from firing too rarely
* ROW pit8253pendingptr: DOCUMENT-AND-CLOSE -- no live code depends on the stale copy
* ROW pit8253retireguard: FIX-NOW -- write the classifier-stopped rows and correct the docstring

## batch 126 -- `oldbatch_126/reply.txt` (2656 bytes)

* ROW adbstalelisten: FILE -- out of bounds read stays within host buffer limits so it does not crash host
* ROW arcbiosenvalloc: FILE -- host out of memory crash is outside the strict guest malformed-input threat model
* ROW arcsgi64vector: FILE -- wrong-result without guest-triggerable host crash
* ROW armbxalignstop: FIX-NOW -- guest instruction can trigger forbidden CPU halt (guest DoS)
* ROW armclrexundec: FIX-NOW -- guest instruction can trigger forbidden CPU halt (guest DoS)
* ROW armexregstop: FIX-NOW -- guest instruction can trigger forbidden CPU halt (guest DoS)
* ROW armldrexbhdspin: FIX-NOW -- guest instruction triggers emulated CPU livelock (guest hang)

## batch 129 -- `oldbatch_129/reply.txt` (3994 bytes)

* ROW i8259icwmask: OWNER-DECISION -- Needs owner ruling on whether to clear ier and expose latched requests.
* ROW i8259initread: FIX-NOW -- Missing writeflag test allows reads to advance init_state.
* ROW i8259pollcomment: FIX-NOW -- The comment misidentifies the 0x0c command.
* ROW includeddeps: FIX-NOW -- Included sources are missing from Makefile prerequisites.
* ROW iso9660dupname: FILE -- A duplicate string match in directory records triggers a fatal exit.
* ROW jazziodfltflood: FIX-NOW -- Guest-drivable unlatched fatal() causes log flooding.
* ROW jazzvecdeassert: CLOSE-OVERTAKEN -- Fixed in 2a24d9b7 but awaiting Fable regress review.

## batch 130 -- `oldbatch_130/reply.txt` (4328 bytes)

* ROW jazzvecrowsowed: FILE -- the F2 pass fix was not shipped because it owes a re-run and pass, making it technical debt.
* ROW kn01bytewrite: FIX-NOW -- clear out-of-bounds memory write on the host buffer requires an immediate patch to return early on invalid length.
* ROW kn230irqwrong: FIX-NOW -- incorrect interrupt line assertion causes emulator logic errors and must be routed to mips_irq_3.
* ROW lancetxtempty: DOCUMENT-AND-CLOSE -- explicitly recognized as a documentation/carrier note rather than a bug in product code.
* ROW lediagfmt32: FIX-NOW -- diagnostic format string mismatch causes undefined behavior and requires a simple typecast.
* ROW legate4le0: FILE -- a gap in test coverage should be logged as low-severity technical debt.
* ROW leiadrbit0: DOCUMENT-AND-CLOSE -- the behavior is an interpretation of the datasheet that is already documented and appropriately issues a warning.

## batch 133 -- `oldbatch_133/reply.txt` (4193 bytes)

* ROW mipsbc1ccstop: OWNER-DECISION -- The outcome of nonzero cc on ISA I-III is not settled by the cited manuals.
* ROW mipscfc0rsvd: FILE -- Consensus FILE for missing RI exception on MIPS32/64 reserved COP0 rs 2.
* ROW mipscop2retrap: FILE -- Consensus FILE for COP2 raising CpU without checking Status.CU2.
* ROW mipscop3isa3: FILE -- Consensus FILE for COP3 incorrectly raising CpU instead of RI on ISA III.
* ROW mipscop3pmaxstop: FILE -- Consensus FILE for COP3 NOP-filtering leading to goto bad CPU-STOP on pmax.
* ROW mipsderetabsent: FILE -- Consensus FILE for DERET being permitted without EJTAG debug mode.
* ROW mipsdrotrundec: FILE -- Consensus FILE for missing DROTR/DROTR32/DROTRV decoding causing goto bad.

## batch 134 -- `oldbatch_134/reply.txt` (4525 bytes)

* ROW mipsdsbranch: FIX-NOW -- remove the goto bad and emulate the unpredictable behavior without halting
* ROW mipseidicu0: FIX-NOW -- add cop0_availability_check before setting or clearing Status.IE
* ROW mipshc1undec: FILE -- severity MED, pending actual hardware FPU resolution
* ROW mipsisa2cop3ls: OWNER-DECISION -- owner must rule on the filing bar for a -C-only CPU
* ROW mipsllzero: FIX-NOW -- remove the goto bad and treat load-linked to $zero as a valid operation
* ROW mipsmuldivrd: FIX-NOW -- remove the goto bad for nonzero rd and ignore the rd field
* ROW mipspromwordbe: FIX-NOW -- store the default PROM word after the machine configures endianness

## batch 137 -- `oldbatch_137/reply.txt` (3663 bytes)

* ROW pciabsentallones: DOCUMENT-AND-CLOSE -- explicitly documented as emulator-compatibility oracle
* ROW pcibarsizeflag: FIX-NOW -- clear flag on target change
* ROW ppc4xxcacheundec: FIX-NOW -- add missing cases to prevent CPU-STOP
* ROW ppcbranch32width: FIX-NOW -- mask bounds based on 32-bit mode
* ROW ppccntlzwrc: FIX-NOW -- implement Rc=1 condition
* ROW ppcdisasmfp63: FILE -- low severity missing disassembler cases
* ROW ppcdivwhostdiv: OWNER-DECISION -- held for owner input on HOST band classifier

## batch 138 -- `oldbatch_138/reply.txt` (3971 bytes)

* ROW ppceciwxundec: FILE -- LOW severity, missing cases for optional external-control instructions cause CPU-STOP.
* ROW ppcfpreservedrc: OWNER-DECISION -- Owner must explicitly prioritize either Book I compliance or the strict detector property.
* ROW ppcmcrxrundec: FILE -- LOW severity, missing case for an optional, phased-out instruction causes CPU-STOP.
* ROW ppcmtdcrnop: OWNER-DECISION -- Needs architectural direction from the owner since no DCR state currently exists to mutate.
* ROW ppcmtmsrlbit: FIX-NOW -- Missing privilege check enables a user-mode guest to trivially trigger a CPU-STOP (VM escape/DoS).
* ROW ppcmulhdundec: FILE -- MED severity, legal 64-bit instructions lacking cases cause a user-mode CPU-STOP.
* ROW ppcmulhwreserved: FIX-NOW -- Defective bitmask extracts reserved bit 21, routing valid instructions to a CPU-STOP.

## batch 139 -- `oldbatch_139/reply.txt` (2659 bytes)

* ROW ppcmull64: FILE -- mulli and mullw produce incorrect results on 64-bit models and need fixing.
* ROW ppcprogvector: OWNER-DECISION -- owner decision 9 defers the missing program exception vector to a separate round.
* ROW ppcsf0addr: FILE -- 64-bit models with SF=0 incorrectly use untruncated effective addresses.
* ROW ppcslbundec: FILE -- SLB instructions crash the emulator via goto bad instead of raising an exception.
* ROW ppcsr64stop: FILE -- segment register instructions crash 64-bit models instead of acting correctly or excepting.
* ROW ppcsrr1sf: FILE -- interrupt entry loses the SF bit in SRR1, breaking 64-bit mode on return.
* ROW ppcstfiwxundec: FILE -- stfiwx instruction crashes the emulator rather than functioning or raising a program exception.

## batch 140 -- `oldbatch_140/reply.txt` (3188 bytes)

* ROW ppcsubfcca32: FILE -- keep as debt, severity MED
* ROW ppcxo64stop: FILE -- keep as debt, severity MED
* ROW ps2biosreturnaddr: FIX-NOW -- move return_addr to machine-specific state and add bounds check
* ROW ps2gmtime: FIX-NOW -- add NULL check for tm_ptr before accessing its members
* ROW pxrowloop: FIX-NOW -- clamp lw to the framebuffer boundaries before the loop
* ROW r3kbevbase: FILE -- keep as debt, severity LOW
* ROW ramallocnull: FIX-NOW -- wrap strdup and malloc calls with NULL checks

## batch 141 -- `oldbatch_141/reply.txt` (3139 bytes)

* ROW rs5c313gmtime: DROP -- unreachable by guest input
* ROW scsicapacitytrunc: FILE -- valid wrong-result defect for large disk images
* ROW shblundriven: FILE -- valid coverage debt for exception codes while BL is set
* ROW shrfcrkey: FIX-NOW -- require B'101001 in upper 6 bits of idata for RFCR writes
* ROW shsleepblwake: FILE -- valid wrong-behaviour defect for SH4 sleep state
* ROW sprstringsbound: DOCUMENT-AND-CLOSE -- bounded input from ppc_spr.h makes the OOB impossible
* ROW srecbytecount: DROP -- benign overflow only affecting a debug print for impossibly large files

## batch 142 -- `oldbatch_142/reply.txt` (3542 bytes)

* ROW strtoullbase: FIX-NOW -- add base and overflow tests to mystrtoull
* ROW vr41xxgiuwidth: FIX-NOW -- widen giuint to 32-bit and use unsigned shift
* ROW wdcatadocstale: FIX-NOW -- remove the four stale document comments
* ROW wdcchssector0: FIX-NOW -- add 0-check for CHS sector
* ROW wdcerraddr: FILE -- moot until wdcmediastatus reports errors (LOW)
* ROW wdcidpignored: FILE -- requires IDP command implementation (MED)
* ROW wdciordybit: OWNER-DECISION -- must be decided alongside wdclbaadvertise

## batch 143 -- `oldbatch_143/reply.txt` (3858 bytes)

* ROW jazzvecreopen: OWNER-DECISION -- Waiting for Fable to adjudicate the follow-up round on the conditional deassert guard
* ROW shfpprreserved: OWNER-DECISION -- A policy decision is required for handling SH-4 undefined operations
* ROW shnanquiet: FIX-NOW -- Canonicalise SH NaN results to quiet NaN
* ROW gate13deadlegs: FIX-NOW -- Add dead-binary and /bin/true runs to gate 13
* ROW mipscpuconstruct: FIX-NOW -- Add config0 initialization for the three failing CPUs
* ROW mpupcsyncrow: FIX-NOW -- Add a test row raising RI/CpU without PC sync
* ROW mpuprobetmpdir: FILE -- The text explicitly defers this cleanup code change to a future round

## batch 144 -- `oldbatch_144/reply.txt` (3904 bytes)

* ROW ppcexcsrr1mask: FILE -- low severity missing exception-cause bits implementation deferred
* ROW ppcllsc216text: FILE -- low severity comment correction deferred
* ROW ppcllscprobeext: FILE -- low severity test extensions filed but not owed
* ROW ppcllscrealaddr: FILE -- low severity architectural theoretical mismatch with no guest witness
* ROW ppcmode32gprhi: FILE -- low severity pre-existing endianness bug in 32-bit register read
* ROW seatsreadstemcollide: FIX-NOW -- fix panel regex truncation to include suffix and add controls
* ROW arcmemdescnr: FIX-NOW -- implement adjudicated boundary membership and safe arithmetic

## batch 145 -- `oldbatch_145/reply.txt` (3447 bytes)

* ROW codeqlscope: FIX-NOW -- apply the two wording edits to tools/mkplan.py before applying dismissals
* ROW dcstdincap: FILE -- the phase-2 instruction files every filing of this round LOW
* ROW fmttruncinherited: FILE -- inherited narrowings the format round left as they were
* ROW memccoverdebt: FILE -- building the sketched rows would turn the families from disclosed to measured
* ROW memrwtreadahead: FILE -- memory_rw's -T path halts on a read-ahead fetch, filed regardless
* ROW ppcbranchlowbits: FILE -- contract filed it separately; fixing it changes what is reached in #582
* ROW ppccrdecodeshift: FILE -- no product change is owed, building variants turns reasoning to measurement

## batch 146 -- `oldbatch_146/reply.txt` (3824 bytes)

* ROW ppccrr5predict: FILE -- the pass-1 ruling allows predictions and flags it as low risk debt.
* ROW ppcifetchdeclineprod: CLOSE-OVERTAKEN -- fixing vgagfxwindowend removes the producer.
* ROW ppcifetchibinit: DOCUMENT-AND-CLOSE -- the shipped fix returns on failed reads, neutralizing the stale decode.
* ROW ppcmpcheckstop: FILE -- the final ruling explicitly chose to file the multiprocessor case as debt.
* ROW ppcvecaddr: FILE -- a specific machine measurement is owed and must be tracked.
* ROW pvrdepth2bpp: OWNER-DECISION -- requires a ruling on whether other probes overlap body-read fields.
* ROW pvrmodvolbit26: FILE -- debt remains filed until a primary source manual is obtained.

## batch 147 -- `oldbatch_147/reply.txt` (3957 bytes)

* ROW pvrswapdebt: FILE -- Explicitly filed as coverage debt and ranked below live defects.
* ROW pvruvfpundet: FILE -- Filed as an unknown that needs to be settled by a specific future measurement.
* ROW vgagfxwindowend: FIX-NOW -- Fixing the off-by-one error directly removes the producer for another bug.
* ROW fbsdramwidth: FILE -- Rated low severity with no wrong values, ranked below fbsdramwrites.
* ROW fbsdramwrites: OWNER-DECISION -- Needs an owner call on implementing member 7 since no guest can validate it.
* ROW fmtmissargwitness: DROP -- Explicitly documented that the owner may drop it and the fix is already in.
* ROW asicarraygeom: FIX-NOW -- The closing row is already built, measured, and ready to lift.

## batch 148 -- `oldbatch_148/reply.txt` (3522 bytes)

* ROW asicpermute: FILE -- Needs the free-running shape to observe interrupt delivery.
* ROW fbclearaliases: FILE -- The fold is shared with other timer cases, making a localized fix inappropriate.
* ROW probeabsentraise: FILE -- Fails in the safe direction, making it a robustness gap rather than a live defect.
* ROW wdcaltfixture: FILE -- Requires a new fixture prologue to properly cover driver-set fields.
* ROW wdcaltwidth: FILE -- Access width is unpinned; filed to be addressed in scope alongside wdcwidthmatrix.
* ROW wdccdbaccum: FILE -- Fixing the shared ring ambiguity breaks existing probes that fake a CDB.
* ROW wdcexpecteddata: FILE -- Requires a costly WRITE-command staging sequence to test the accept side.

**Mechanical check of these batches (FIX-NOW / CLOSE-OVERTAKEN on a row that already carries commits):**

* `jazzvecdeassert` (batch 129): CLOSE-OVERTAKEN, but the row already carries commits `2a24d9b7` -- its own round shipped; what it owes is its held stage.
* `codeqlscope` (batch 145): FIX-NOW, but the row already carries commits `ccd1c502` -- its own round shipped; what it owes is its held stage.

## batch 900 -- `oldbatch_900/reply.txt` (1403 bytes)

* ROW g3nologselfpin: FILE -- Explicitly marked as a low-severity debt to file since it is not a floor breach or landing blocker.
* ROW gate3runbound: FILE -- Explicitly filed from research as owed low-severity debt for a missing timeout bound.

**Mechanical check of these batches (FIX-NOW / CLOSE-OVERTAKEN on a row that already carries commits):**

* none

## batch 911 -- `oldbatch_911/reply.txt` (2464 bytes)

* ROW b120r: OWNER-DECISION -- The row requires a guest measurement on luna88k before a round can proceed.
* ROW asicindexcase: FIX-NOW -- The final form specifies a silent fall-through decline via a guarded arm joining the existing epilogue.
* ROW asanstaleobjs: FILE -- The finding and evidence are fully tracked externally in OUTSTANDING_BUGS.md as a LOW severity debt.

## batch 912 -- `oldbatch_912/reply.txt` (2151 bytes)

* ROW deletecheckhead: UNSETTLED -- evidence resides in an external file (OUTSTANDING_BUGS.md).
* ROW fbbounddebt: UNSETTLED -- evidence resides in external files (OUTSTANDING_BUGS.md and artifacts).
* ROW fbboundmodes: UNSETTLED -- evidence resides in external files (OUTSTANDING_BUGS.md and artifacts).

## batch 913 -- `oldbatch_913/reply.txt` (1868 bytes)

* ROW gdrompiooddlen: DOCUMENT-AND-CLOSE -- the row's own evidence confirms the defect is a latent structural hazard with no reachable route.
* ROW hygienecensusholes: FILE -- the issue identifies real evasion gaps in the test suite but is explicitly ranked below live defects.
* ROW fbdrainonepass: FILE -- this represents a valid but low-severity performance enhancement that remains open.

## batch 914 -- `oldbatch_914/reply.txt` (2281 bytes)

* ROW hygienesweepmissing: FILE -- Test harness allows missing diagnostic-division sweeps without gate failure (severity HIGH).
* ROW i960disasmspan: FIX-NOW -- Buffer over-read on the bad path and single-step path should be trivially fixed by increasing the buffer size.
* ROW ieeedsubsweep: FILE -- Test harness only counts differences and misses subnormal bit-forcing mutants (severity MED).

## batch 915 -- `oldbatch_915/reply.txt` (2082 bytes)

* ROW ieeeinfrnvac: UNSETTLED -- Ruling and evidence reside in an external file that must be read.
* ROW ieeequantumband: UNSETTLED -- Ruling and evidence reside in an external file that must be read.
* ROW ieeesignmustdiffer: UNSETTLED -- Ruling and evidence reside in an external file that must be read.

## batch 916 -- `oldbatch_916/reply.txt` (1870 bytes)

* ROW m8probe: OWNER-DECISION -- Awaits batched flagship close pass due to unmeasured NetBSD/MP reachability and lack of manual.
* ROW probeneedleterm: DROP -- Row is a sync artifact with a decayed warrant that already exists in the bug file.
* ROW ieeesliverinf: FILE -- Unfixed floating-point truncation bug confirmed by the regression harness.

## batch 917 -- `oldbatch_917/reply.txt` (3517 bytes)

* ROW storesidedead: FILE -- Keep as debt (med) to execute the owed census re-fire with an extensional file list.
* ROW sessionechosat: FIX-NOW -- Anchor the SH probes' liveness regex to reject the debugger's command echo.
* ROW sessionrefused: FIX-NOW -- Ensure sh_intprio/sh_iprbcd distinguish host death from explicit refusal.

## batch 918 -- `oldbatch_918/reply.txt` (1158 bytes)

* ROW xscaleinten: UNSETTLED -- missing file contents and probe execution results needed to answer the hold question

**Mechanical check of these batches (FIX-NOW / CLOSE-OVERTAKEN on a row that already carries commits):**

* none
