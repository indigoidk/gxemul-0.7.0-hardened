ASTRA RETRO-REVIEW (HARNESS) `hcheckprobewiring` -- the GXemul fork's regression and pipeline code, 1 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HCHECKPROBEWIRING_ALIVE` on its own line, then ONE verdict line:
`VERDICT: <n> findings (<k> CANNOT-FAIL, <s> SELECTS-NOTHING, <x> STATUS-LAUNDERED, <e> ENCODING, <r> RECORD, <o> OTHER);
<c> items checked clean`

**Why you are asked.**  This fork of GXemul 0.7.0 guards several hundred correction rounds with its own regression
harness: Python probes that drive the emulator's debugger through a pty, gate scripts that score them, offline C
differentials, and pipeline checkers run before every commit.  The harness was reviewed as it landed, but mostly
before you (GPT-6 Astra) joined the review panel on 2026-09-04 -- this is your first reading of most of it.  A
regression row that cannot fail is worse than no row, because it reports coverage that does not exist; please look
for exactly that, and do not simply ratify.

**The tree.**  Repository `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` (git).  Review HEAD ONLY: `git show HEAD:<path>`;
a file's history `git log --format='%h %ad %s' --date=short -- <path>`; one round's change
`git show --format= <sha> -- <path>`.  The WORKING TREE carries other people's uncommitted work -- do not read from
disk.  The emulator source the probes exercise is `src/` in the same repository, at HEAD.

**What counts as a finding.**
1. **CANNOT-FAIL** -- a row or check whose expected value is also what the code would produce WITHOUT the correction
   it guards (for example a survive-only row at a site where the corrected code refuses and the uncorrected code also
   survives), an expectation computed from the value it checks, a row that compares a thing with itself, or a check
   whose failure branch is unreachable.  Name the row and say what both versions of the code would produce.
2. **SELECTS-NOTHING** -- a regex, grep, awk range or parser that can match nothing and then reports success or zero
   (a count of 0 read as "no failures"; a missing section read as a pass; a padded-column pattern longer than its
   column).  Name the input on which it selects nothing.
3. **STATUS-LAUNDERED** -- a failure that surfaces as success: an exit status lost in a pipe or `|| true`, a timeout
   or killed run scored as complete (no completion sentinel checked), a skip scored as a pass, a build failure scored
   as a detection.
4. **ENCODING** -- a hand-assembled instruction word or register value whose fields do not encode what its comment
   says (a wrong register field typically yields 0, which rows expecting 0 accept by accident).  Decode it from the
   manual (`ls _scratchpad/*.txt` under the project root) and cite the line.
5. **RECORD** -- a docstring, comment or header whose claim about the code (a row count, what a row catches, a
   score) is false of the code at HEAD.  Line-number drift is NOT a finding.
6. **OTHER** -- a real defect of the harness that fits none of the above (a load-sensitive wall-clock oracle, a
   shared temporary path two gates both write, a probe no gate runs).

**The files** (lines = the fork's net addition since the import `39748e3c`):

| file | lines | rounds | before 2026-09-04 |
|---|---|---|---|
| `tools/pipeline/check_probe_wiring.py` | 3590 | 119 | 69 |

**Their rounds**, oldest first:

- `798cff34` 2026-08-21 flagship batch: two wrong records I shipped, and three FALSE ACCEPTS in the wiring checker  [check_probe_wiring.py]
- `85bc6ab4` 2026-08-21 probewiring: four rounds of detectors that no gate has ever run  [check_probe_wiring.py]
- `a636a339` 2026-08-21 #448 sh4chcr: a LEGAL DMA configuration ended the host on its resource-select alone  [check_probe_wiring.py]
- `e841f443` 2026-08-21 #447 sh4valguards: one guest STORE ended the host, at four sites whose store positions differ  [check_probe_wiring.py]
- `f39b8984` 2026-08-21 #450 arcbiosubsan: ten uncast shifts, and the author had already cast four of them  [check_probe_wiring.py]
- `f4374117` 2026-08-21 #449 sh4rtcsr: the host died nine milliseconds after the guest store, in a timer callback  [check_probe_wiring.py]
- `0678450e` 2026-08-22 #457 three guest stores ended the host process  [check_probe_wiring.py]
- `927553fa` 2026-08-22 #452 sh4 TLB data array 2: decline the access instead of ending the host process  [check_probe_wiring.py]
- `b3ad305a` 2026-08-22 #451 sh4_sci_cmd(): decline the command instead of ending the host process  [check_probe_wiring.py]
- `dc0c9d50` 2026-08-22 #455 an interrupt at priority 0 ended the host process  [check_probe_wiring.py]
- `0bb8be2b` 2026-08-23 #459: one guest store to 0xffd80010 ended the host on 3 of 5 SH machines  [check_probe_wiring.py]
- `7e5c0f6c` 2026-08-23 #458: SH-4 read two of four interrupt priority registers, and SCIF's came       from a register this machine never maps  [check_probe_wiring.py]
- `98a34085` 2026-08-23 #460: GDROM_DATA had no legal first touch -- four exit(1) on one register  [check_probe_wiring.py]
- `ba30e64f` 2026-08-23 #461 both `default:` arms of the GD-ROM device ended the host process  [check_probe_wiring.py]
- `7c9dd9eb` 2026-08-24 #462 both arms of the GD-ROM DMA trigger (case 0x18) ended the host process on a guest store  [check_probe_wiring.py]
- `f1fa6a0a` 2026-08-25 #463 dreamcast_asic: one guest LOAD ended the host, at 64 byte addresses  [check_probe_wiring.py]
- `29b450ce` 2026-08-26 #467 + #468: the pty deadline means SILENCE, and the ASIC domain is now ENFORCED  [check_probe_wiring.py]
- `baacf9bb` 2026-08-26 #464 wdc: six unlatched fatal() bounded, and the detector's first gate  [check_probe_wiring.py]
- `0922465f` 2026-08-27 #477 wdc ATAPI: a guest data-port WRITE could free the transfer being delivered  [check_probe_wiring.py]
- `09362f0e` 2026-08-27 #488 diskimage: a short read in a NON-FINAL iteration corrupted twice, and the round that touched these exact lines was asking a different question  [check_probe_wiring.py]
- `0a7c4687` 2026-08-27 #471 probewiringscope: the checker can see below regress/ top level at last  [check_probe_wiring.py]
- `23430365` 2026-08-27 #479 wdc: a new command did not reset what the old one left  [check_probe_wiring.py]
- `3403c013` 2026-08-27 #482 wdc: the abort row could not say which state gated the abort  [check_probe_wiring.py]
- `3cdb58a5` 2026-08-27 records: wdcfloodstale measured, not inferred -- three legs, and the control is the point  [check_probe_wiring.py]
- `6378bed5` 2026-08-27 harness: a rung-3 witness for the ring -- and it found a STALE BINARY with no mutant in the story  [check_probe_wiring.py]
- `77b7c03a` 2026-08-27 #485 pass 2: the detector was below the floor TWICE, and the pass the round skipped found it  [check_probe_wiring.py]
- `7d0b63d4` 2026-08-27 #480 wdc: the detector could not see its own call  [check_probe_wiring.py]
- `832bed78` 2026-08-27 #478 wdc: an empty ring was read as a full sector, and 512 stale bytes went to the disk  [check_probe_wiring.py]
- `867c697b` 2026-08-27 #481 wdc: the reset bit was the head-count bit  [check_probe_wiring.py]
- `ce75b1d2` 2026-08-27 #483 wdc: the sweep pinned the decode across 256 values and the purge at none  [check_probe_wiring.py]
- `d8191881` 2026-08-27 #485 wdc: 242 of 256 opcodes ended a command and never raised its interrupt  [check_probe_wiring.py]
- `ebd23b18` 2026-08-27 records: a committed detector row whose stimulus a later round silently invalidated  [check_probe_wiring.py]
- `ed3f9cce` 2026-08-27 records: a queue row read FIXED and OPEN in two consecutive lines -- and a seat believed the tick  [check_probe_wiring.py]
- `095aa960` 2026-08-28 #489 gdrom: a guest-supplied length ended the host, and deleting the guard would have been worse  [check_probe_wiring.py]
- `19d1dc8a` 2026-08-28 R2 pass 1, the measuring seat: three MEASURED escapes -- and two of them this round's own PRETABLE.out had already prescribed rows for  [check_probe_wiring.py]
- `38b07dc3` 2026-08-28 gdromexitsix: the vanished witness rebuilt, MEASURED RED, and preserved this time  [check_probe_wiring.py]
- `7084b364` 2026-08-28 adjudication 2026-08-28: the pre-table block is MANDATORY, and four held stages answered  [check_probe_wiring.py]
- `c43ce978` 2026-08-28 gdromexitsix R2: the measured mutant table, one real defect FIXED, and PLUMBING THAT IS NOT YET COVERAGE  [check_probe_wiring.py]
- `e1547bfe` 2026-08-28 #489's headline claim is MEASURED, not derived: 7 heap-buffer-overflow WRITEs through the real guest path  [check_probe_wiring.py]
- `3521a225` 2026-08-29 #493 wdcaltoffset: a durable rung-3 witness for a live sev-high defect that had been measured twice and could be re-run neither time  [check_probe_wiring.py]
- `d9efd339` 2026-08-29 #492 the six battery reds -- and a detector that passed its own kill table with an L2 breach live in it  [check_probe_wiring.py]
- `fb0cc783` 2026-08-29 #490 GD-ROM handle_command: two guest-reachable host kills, plus a wsl-dollar hook  [check_probe_wiring.py]
- `105c15c7` 2026-08-30 #496: the detector's first CLEAN baselines, two more escapes closed, and a selftest that broke because the tree got better  [check_probe_wiring.py]
- `1d2e8288` 2026-08-30 records: the width guard is holding an OOB WRITE shut -- and #497's witness obligation was discharged by a seat, 26/26  [check_probe_wiring.py]
- `439dfd05` 2026-08-30 #496 follow-up: two MEASURED escapes closed, and a deriver that matched itself  [check_probe_wiring.py]
- `577ce69f` 2026-08-30 records: the WIDTH-KILL class, the sgi_re cluster -- and my premise was false  [check_probe_wiring.py]
- `67120fd6` 2026-08-30 #495 wdc: a host store during an ATAPI DATA-IN transfer was pushed into the ring, and the guest read its own bytes back as disk data  [check_probe_wiring.py]
- `7be9f804` 2026-08-30 #496 L2 + L4: a one-line edit disabled the exemption-expiry mechanism and scored 21/21  [check_probe_wiring.py]
- `9ccb47bc` 2026-08-30 adjudication: the seat found FOUR of my six dispositions wrong, and D4 was measured  [check_probe_wiring.py]
- `ae68e297` 2026-08-30 wdcaddtoinbufbound: a rung-3 witness, built and green -- and it refutes two premises of the brief that asked for it  [check_probe_wiring.py]
- `beadf9a7` 2026-08-30 #496: five MEASURED escapes closed, and the axis nobody sampled  [check_probe_wiring.py]
- `c1254506` 2026-08-30 #494 wdc: the alt-ctrl handler never decoded its own offset, so a store to a read-only register aborted a live transfer  [check_probe_wiring.py]
- `c516a9c9` 2026-08-30 #496 GD-ROM: two guest-reachable host kills de-fatalised, plus the store that made a naive fix worse than the defect -- and the ADJUDICATION PASS  [check_probe_wiring.py]
- `e0adc7ce` 2026-08-30 #497: the round is MEASURED -- two 35-row tables, the escape found and repaired, floor (a)-(f) all discharged  [check_probe_wiring.py]
- `e363582a` 2026-08-30 #497 pass 2: the detector ships, and the panel found a MEASURED escape plus two gate defects of mine  [check_probe_wiring.py]
- `f42d747d` 2026-08-30 records: #484 closed ONE of the two rows it claims, and a measured clause-(d) escape  [check_probe_wiring.py]
- `387b9809` 2026-08-31 sgidewidth measured: a rung-3 witness, a 25-row table -- and the obvious fix is the wrong one  [check_probe_wiring.py]
- `598030ce` 2026-08-31 #499 table: three accept rows discharged, and a carrier rule falsified the day it was minted  [check_probe_wiring.py]
- `748c9daf` 2026-08-31 sgireunmapped is WITNESSED at rung 3 (32/32) -- and the ninth seat changed the round  [check_probe_wiring.py]
- `938b328e` 2026-08-31 #499 L2: two mutants swept the detector clean, one restoring the round's own witness  [check_probe_wiring.py]
- `9f666a8d` 2026-08-31 #499 sgireunmapped: a 2080-byte door closed, with the order proof re-run locally  [check_probe_wiring.py]
- `cb28a6f5` 2026-08-31 #498 sgidewidth: a guest `sb` ended the host -- and the OBVIOUS fix scores 24/25  [check_probe_wiring.py]
- `de1a0de2` 2026-08-31 #499 pass 4: close the CLASS, not the cells -- 36 -> 48 rows  [check_probe_wiring.py]
- `e898c845` 2026-08-31 #498 pass 2: the shipped detector had TWO more 25/25 escapes, both one keystroke  [check_probe_wiring.py]
- `840f3d0a` 2026-09-01 #500 sgideprimop: a drawing op a guest never chose, and the reset value was one  [check_probe_wiring.py]
- `3fb1f8f6` 2026-09-02 #500 pass 12: the panel MEASURED two clean sweeps my "no floor breach" pass had missed, and three seats found the red I left one line below the one...  [check_probe_wiring.py]
- `560fa6dc` 2026-09-02 #500 pass 6: two floor breaches, an empty corner of a two-by-two, and a record that did not match its own artifact  [check_probe_wiring.py]
- `b78bb0f6` 2026-09-03 #500 pass 15 + pcc2widthkills: the closure that opened six registers is closed, and twelve width kills become a direction split  [check_probe_wiring.py]
- `f52c1579` 2026-09-03 #500 pass 14: the closing pass found a FAMILY of five zero registers, one session closed it, and the contract now states what rows cannot close  [check_probe_wiring.py]
- `70761347` 2026-09-05 pcc2widthkills passes 5-13 + the 2026-09-04 fix review: the fix approved block by block, the detector 190 -> 251 rows, pass 14 OWED (row stays open)  [check_probe_wiring.py]
- `ecc4d3be` 2026-09-05 #501 pcc2defaultkill: the default: arm of DEVICE_ACCESS(pcc2) no longer ends the host; reads keep the served byte, writes are declined, one latched...  [check_probe_wiring.py]
- `79cd12e8` 2026-09-06 #502 pass 9-12 and #503: two fixes shipped, a filing overturned to a floor breach and repaired, and a detector's own contract predicting both of it...  [check_probe_wiring.py]
- `257f56f1` 2026-09-07 #504 sgirandompixel: a failed pixel read handed the caller random() and the write stored it; plus the pass-2 receipt 79cd12e owed, and a measured f...  [check_probe_wiring.py]
- `41923ac8` 2026-09-07 lcaconfbus1kill: a rung-3 witness, and the defect is MEASURED -- an ACCEPTED write arms a host kill  [check_probe_wiring.py]
- `5dcdb92b` 2026-09-07 #509 follow-up: the manifest entry, the pass-2 receipt, and the commit the ledger did not name  [check_probe_wiring.py]
- `7a41b3fb` 2026-09-07 #505 #506 #507 #508: four test-first rounds, three new rung-3 witnesses, and a witness row that could not fail  [check_probe_wiring.py]
- `7c2f8e4a` 2026-09-07 lcairqstubkill WITNESSED: four guest instructions end the host through a documented 8042 register  [check_probe_wiring.py]
- `c0c7f55d` 2026-09-07 #510 armbfxwidth32: UBFX and SBFX built their mask with an undefined shift  [check_probe_wiring.py]
- `1106b882` 2026-09-08 LCA cluster + alphaswpctxreg: a six-seat panel, three of my claims corrected, and the codex content-filter trigger measured by a one-variable exper...  [check_probe_wiring.py]
- `2ab3d2f0` 2026-09-08 #514 pass 2: the product fix is ratified 6/6 and every other finding was in my detector or my records -- four repaired in-round, one claim withdraw...  [check_probe_wiring.py]
- `3031a306` 2026-09-08 #514 alphaswpctxreg: the context-switch primitive returned its result in the register the ABI tells the caller to discard -- one identifier, rung-3...  [check_probe_wiring.py]
- `9fa07fe9` 2026-09-08 #512 pcc2c040kill: one legal guest byte store ended the host  [check_probe_wiring.py]
- `b4d4177c` 2026-09-08 #515 lcaconfbus1kill: one variable meant two things, so a value the register's own guard ACCEPTS armed a host kill in a different handler  [check_probe_wiring.py]
- `bee05ce5` 2026-09-08 #514: the last two escapes pass 4 left open are closed by binding each observation to its STEP, and the repair is measured  [check_probe_wiring.py]
- `f4fecb7f` 2026-09-08 #514 pass 5: my binding repair LOST coverage the positional rule had, and the fix is to compose them rather than replace one with the other  [check_probe_wiring.py]
- `fa5e4e37` 2026-09-08 #514 pass 3: a seat measured two apparatus false passes, one of which I had introduced in the pass-2 repair -- and a duplicate-key guard caught me ...  [check_probe_wiring.py]
- `74daefdd` 2026-09-09 #516 lcairqstubkill: every ISA interrupt on alphabook1 routed into a function whose whole body was fatal()+exit(1)  [check_probe_wiring.py]
- `e73623ab` 2026-09-09 records: the night's adjudications -- 7g-1 ruled FLOOR on a measured 14/14 escape, the pcc2 C040 residual cell settled and a dead accept row found,...  [check_probe_wiring.py]
- `1ce82969` 2026-09-10 #509 follow-up (sgimtelabelcells): the detector was blind at two of three dispatch labels -- two rows close the floor breach 7g-1 found, measured 1...  [check_probe_wiring.py]
- `1f2b27ab` 2026-09-10 #512 follow-up (pcc2c040ctlq): the accept row the de-escalation clause owed was keyed on the fix's own retired text and could not fail -- measured ...  [check_probe_wiring.py]
- `21e75609` 2026-09-10 #521 (mk48nvramkill): EIGHT ordinary NVRAM bytes inside a device's own mapped range ended the emulator -- the accept block's lower bound was one te...  [check_probe_wiring.py]
- `65b007bf` 2026-09-10 #520 (alphatbinegsel): a guest TBIA flushed ONE page -- the selector was compared UNSIGNED, so both documented invalidate-everything values took th...  [check_probe_wiring.py]
- `7d5e0666` 2026-09-10 records: #521's pass-2 receipt, the PowerPC witness, and a third design review that corrected my premises again  [check_probe_wiring.py]
- `7d7e0559` 2026-09-10 records+evidence: the night's three rounds land their measurements while TWO STAY HELD -- #518 on three mutants that still escape its own 67-row in...  [check_probe_wiring.py]
- `e2e5a195` 2026-09-10 records: the NVRAM host kill is WITNESSED AT RUNG 3 and MEASURED 15/47 -> 46/47, and two seats reached the same register-bank finding by different ...  [check_probe_wiring.py]
- `e777ff06` 2026-09-10 #522 (ppcrldiclzero): rldicl wrote ZERO to its destination on every execution — the mask was accumulated into the rotated value and ANDed with a va...  [check_probe_wiring.py]
- `4dfc7165` 2026-09-12 #524 (armbdt): an ARM block transfer through a cold host page spliced bytes across a word boundary -- the same LDM/STM at the same unaligned base r...  [check_probe_wiring.py]
- `599a7a82` 2026-09-12 #525 (wdcaltdigin): the alt-status handler never decoded its offset ON THE READ SIDE, so a read of the Drive Address register returned the ALT-STAT...  [check_probe_wiring.py]
- `7e39a49e` 2026-09-12 #527 (ppcrlwimiwidth, ppcrldimimask): rlwimi rotated a 32-bit word at 64-bit width and never wrote a wrapping mask's high word; rldimi's rotate loo...  [check_probe_wiring.py]
- `a616d20b` 2026-09-12 #518 (lcabadval): six LCA IOC write arms ended the emulator on values the 21066/21066A manual makes legal -- including the zero SROM is REQUIRED to...  [check_probe_wiring.py]
- `ca3be4eb` 2026-09-12 #528 (mapledmaaddr): a guest read of the Dreamcast Maple DMA-address register ended the emulator after computing the right value  [check_probe_wiring.py]
- `eb26590b` 2026-09-12 #526 (xscaleinten): a guest read of the i80321 interrupt-enable register ended the emulator after loading the right value  [check_probe_wiring.py]
- `fd150657` 2026-09-12 #519 (sgirandomcolour): the colour-mode PUT default arm stored four host random() bytes into guest memory -- reachable with the documented DE_MODE_...  [check_probe_wiring.py]
- `09ded75c` 2026-09-18 #534 stagetokens: four tools read one ledger field, each with its own copy of what it meant  [check_probe_wiring.py]
- `3c41f011` 2026-09-18 records: 8bd97e4's pass 2 -- DOES NOT CLOSE; the width row covers one of twelve reachable cells, and the rule question goes to the §F2 pass and fable5  [check_probe_wiring.py]
- `4653ecfb` 2026-09-18 records: the owner-ordered missing seats, all fired -- and one of them measured an L2 in a shipped detector  [check_probe_wiring.py]
- `686d179c` 2026-09-18 #531 ip30abortkill + #532 stagetokens: four guest-reachable abort() calls, and the gates that reddened because the record got more honest  [check_probe_wiring.py]
- `8bd97e4d` 2026-09-18 #530 lcaisalane: a guest byte access to an ISA port 2 or 3 mod 4 ended the host -- shipped with the width row its own closing verdict owed  [check_probe_wiring.py]
- `bb8efbf0` 2026-09-18 #535 pcc2c040mienannounce: #512's detector missed the cell a real driver writes -- and ran in no gate at all  [check_probe_wiring.py]
- `e16a8b7c` 2026-09-18 #533 landiskaux: landisk's wdc aux register sat at the PC-layout +0x206, so the kernel's soft reset landed on unmapped memory  [check_probe_wiring.py]
- `78360718` 2026-09-19 #539 n6: the footbridge IRQEnable read computed the right value and then ended the process -- the exit is gone, the value stays; the probes' kill c...  [check_probe_wiring.py]
- `a11eaac4` 2026-09-19 #538 lcalenzerodrop closes: #530's width row pinned one byte lane of four -- all four rowed, 17/17 as predicted, reproduced on the final instrument  [check_probe_wiring.py]
- `eec0f4a3` 2026-09-19 #536 wiringcliff: two probes wired into gate_arm.sh, eleven exemptions re-dated to 2026-09-27 by owner ruling -- and the checker's selftest derives...  [check_probe_wiring.py]
- `4264ee20` 2026-09-23 #545 fbdeclinefive: five footbridge register accesses the DC21285 does not define ended the process -- they are declined and announced once each, d...  [check_probe_wiring.py]
- `3e33201d` 2026-09-24 #546 hygienecensus: gate 6's readiness census was 24 probes stale and RED at HEAD -- re-derived by a tool, never by hand, and the tool went through...  [check_probe_wiring.py]
- `f4f601c4` 2026-09-24 #548 fbdrainwire: #442's drain probe wired into gate 14 on all four timers before its exemption lapsed -- and three floor breaches of #442's own de...  [check_probe_wiring.py]
- `04500deb` 2026-09-26 #550 exemptredate: the ten probe-wiring exemptions due 2026-09-27 re-dated one by one, each to its own owed-work date (2026-10-08 .. 2026-12-03), a...  [check_probe_wiring.py]
- `8ea26abb` 2026-09-26 #549 fbctrlportkill: the test machines' framebuffer controller stored an out-of-range port selector and the next DATA access ended the emulator pro...  [check_probe_wiring.py]
- `db8b1a33` 2026-09-26 #553 latecodex: the codex seat re-fires #550, #551 and #549 promised landed after those commits -- adjudicated under the late-dissent rule, their c...  [check_probe_wiring.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
