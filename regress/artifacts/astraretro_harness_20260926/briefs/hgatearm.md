ASTRA RETRO-REVIEW (HARNESS) `hgatearm` -- the GXemul fork's regression and pipeline code, 1 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HGATEARM_ALIVE` on its own line, then ONE verdict line:
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
| `regress/gate_arm.sh` | 1867 | 68 | 54 |

**Their rounds**, oldest first:

- `a06e92fb` 2026-07-31 Round 71 (#311, #312, #313): ARM -- two wrong flags and one more halt  [gate_arm.sh]
- `0c1eb584` 2026-08-01 Round 78 addendum (#322) + round 84: the panel overturned one call and stopped another  [gate_arm.sh]
- `cbbe1ec0` 2026-08-01 Round 78 (#319, #320, #321): ARM rotations answered by halting -- and a carry read off the complement  [gate_arm.sh]
- `85bc4673` 2026-08-02 Round 90 (#329): the Thumb shift paths, where the flags came from a register the instruction never named  [gate_arm.sh]
- `d6f3d750` 2026-08-02 Round 77 (#328): three flag defects in the Thumb interpreter  [gate_arm.sh]
- `597a71b5` 2026-08-03 Round 83 (#340): folding a compare into a branch changed the flags  [gate_arm.sh]
- `4b031420` 2026-08-05 Round 93 (#342): the XOR-swap fold had no "two distinct registers" guard  [gate_arm.sh]
- `be6ea08a` 2026-08-05 Round 97 (#346): the cache-clean fold ignored the stride its own arithmetic assumed  [gate_arm.sh]
- `d143bd5b` 2026-08-05 Round 94 (#345): the cache-clean fold matched a loop's shape and ignored its registers  [gate_arm.sh]
- `dea2fefd` 2026-08-05 Round 98 (#347): the second cache-clean fold skipped a loop and updated nothing  [gate_arm.sh]
- `307b1b82` 2026-08-10 Round 100 (#351, #352, #353): the idle-loop fold skipped its writes, aliased a register, and hung the guest  [gate_arm.sh]
- `704036ef` 2026-08-10 Round 99 (#348, #349, #350): the cache-clean folds learned their exit flags  [gate_arm.sh]
- `7d3238f0` 2026-08-10 Round 101 (#354): the memcpy fold moved the bytes but never published the registers  [gate_arm.sh]
- `1751ae27` 2026-08-11 Round 108 (#362): unaligned word loads returned the aligned word, unrotated  [gate_arm.sh]
- `221328df` 2026-08-11 Round 104 (#358): five folds were doing work no test could see, and #357 removed the only witness  [gate_arm.sh]
- `2c615c3c` 2026-08-11 Round 112 (#367): path attribution stops being a comment and becomes a checked quantity  [gate_arm.sh]
- `38537dee` 2026-08-11 Round 102 (#355, #356): the strlen fold answered a question the architecture never asked, and never came up for air  [gate_arm.sh]
- `396c3f8a` 2026-08-11 Round 106 (#360): the row that asserted an absence still passed when the fold was dead  [gate_arm.sh]
- `42bd6822` 2026-08-11 Round 113 (#368): the copyin fold's rotation shipped unreachable, and its row is a cross-path XOR  [gate_arm.sh]
- `5ae6c0e9` 2026-08-11 Round 115 (#372): the general-path word STORE ignored byte order, because its arm was dead code  [gate_arm.sh]
- `5b225bc3` 2026-08-11 Round 107 (#361): the last two folds with markers but no rows, and a negative arm that was vacuous alone  [gate_arm.sh]
- `91f58cde` 2026-08-11 Round 105 (#359): a fold that copied half the bytes passed every check in the gate  [gate_arm.sh]
- `a280ee92` 2026-08-11 Round 111 (#365): "unreached" was wrong -- the sites were reached and nothing DISCRIMINATED the fix  [gate_arm.sh]
- `aed12e44` 2026-08-11 Round 103 (#357): the load/store template masked the base writeback, so a post-index loop could not advance  [gate_arm.sh]
- `e89e3db2` 2026-08-11 Round 110 (#364): the row-to-site table was inverted, so two shipped rotations were never measured  [gate_arm.sh]
- `276fd0b2` 2026-08-12 Round 120 (#379): #378's pass-2 findings -- a false-green route and five record errors  [gate_arm.sh]
- `3757175a` 2026-08-12 #387: #386's pass-2 — the +2-offset detector, the kind pin, eight record precisions  [gate_arm.sh]
- `5f60d0d0` 2026-08-12 Round 124 (#384): #382/#383's pass-2 findings -- a tag split, a copyout coverage gap, records  [gate_arm.sh]
- `813ee67a` 2026-08-12 #386: swp — byte-order on both sides, rotate on the load, aligned word for both accesses  [gate_arm.sh]
- `c113e677` 2026-08-12 Round 123 (#382): the copyin/copyout folds moved byte-reversed words on a BE guest  [gate_arm.sh]
- `e9230ad6` 2026-08-12 Round 119 (#378): a BE guest's LDM/STM through a warm page was byte-reversed  [gate_arm.sh]
- `495a07a6` 2026-08-13 #389 pass-2: eleven records corrections, and two mutant gaps the battery could not see  [gate_arm.sh]
- `8b1a7fdf` 2026-08-13 #390: one scratch word, two roles — a PC-relative store's base was four bytes high  [gate_arm.sh]
- `d6f860d2` 2026-08-13 #389: LDRD/STRD — two 32-bit words, not one 64-bit swap  [gate_arm.sh]
- `6014b7e7` 2026-08-19 selfmutant6 CLOSED: the fifth control, and the first committed footbridge witness  [gate_arm.sh]
- `24b5ac84` 2026-08-26 exemplar audit chunk 4: gate 14 is 358 checks, not 261 -- in two places  [gate_arm.sh]
- `105c15c7` 2026-08-30 #496: the detector's first CLEAN baselines, two more escapes closed, and a selftest that broke because the tree got better  [gate_arm.sh]
- `e363582a` 2026-08-30 #497 pass 2: the detector ships, and the panel found a MEASURED escape plus two gate defects of mine  [gate_arm.sh]
- `4daa506e` 2026-08-31 the L2 repair had the same defect one level down, and the rule that caught it is now written  [gate_arm.sh]
- `938b328e` 2026-08-31 #499 L2: two mutants swept the detector clean, one restoring the round's own witness  [gate_arm.sh]
- `9409a827` 2026-08-31 the weekly battery failed on Sunday and nobody looked; the next one would have failed too  [gate_arm.sh]
- `9f666a8d` 2026-08-31 #499 sgireunmapped: a 2080-byte door closed, with the order proof re-run locally  [gate_arm.sh]
- `cb28a6f5` 2026-08-31 #498 sgidewidth: a guest `sb` ended the host -- and the OBVIOUS fix scores 24/25  [gate_arm.sh]
- `de1a0de2` 2026-08-31 #499 pass 4: close the CLASS, not the cells -- 36 -> 48 rows  [gate_arm.sh]
- `e898c845` 2026-08-31 #498 pass 2: the shipped detector had TWO more 25/25 escapes, both one keystroke  [gate_arm.sh]
- `80cab9e3` 2026-09-01 #500 follow-up: the CLASS CLOSURE -- and a repair of mine that its own verification sweep falsified  [gate_arm.sh]
- `840f3d0a` 2026-09-01 #500 sgideprimop: a drawing op a guest never chose, and the reset value was one  [gate_arm.sh]
- `41a4b1e4` 2026-09-02 #500 pass 9: I stopped asking for mutants and asked which symmetry was half-closed; two seats found two  [gate_arm.sh]
- `559ebcf6` 2026-09-02 #500 pass 8: the accept side carried all 24 low bits since pass 4; the decline side carried none  [gate_arm.sh]
- `55e4f539` 2026-09-02 #500 pass 7: the repair for "green for the wrong reason" was itself green for the wrong reason, twice  [gate_arm.sh]
- `560fa6dc` 2026-09-02 #500 pass 6: two floor breaches, an empty corner of a two-by-two, and a record that did not match its own artifact  [gate_arm.sh]
- `8b20eac1` 2026-09-02 #500 pass 5: the disposition I had ACCEPTED was wrong, and a seat overturned it by reading  [gate_arm.sh]
- `b78bb0f6` 2026-09-03 #500 pass 15 + pcc2widthkills: the closure that opened six registers is closed, and twelve width kills become a direction split  [gate_arm.sh]
- `f52c1579` 2026-09-03 #500 pass 14: the closing pass found a FAMILY of five zero registers, one session closed it, and the contract now states what rows cannot close  [gate_arm.sh]
- `70761347` 2026-09-05 pcc2widthkills passes 5-13 + the 2026-09-04 fix review: the fix approved block by block, the detector 190 -> 251 rows, pass 14 OWED (row stays open)  [gate_arm.sh]
- `ecc4d3be` 2026-09-05 #501 pcc2defaultkill: the default: arm of DEVICE_ACCESS(pcc2) no longer ends the host; reads keep the served byte, writes are declined, one latched...  [gate_arm.sh]
- `257f56f1` 2026-09-07 #504 sgirandompixel: a failed pixel read handed the caller random() and the write stored it; plus the pass-2 receipt 79cd12e owed, and a measured f...  [gate_arm.sh]
- `7a41b3fb` 2026-09-07 #505 #506 #507 #508: four test-first rounds, three new rung-3 witnesses, and a witness row that could not fail  [gate_arm.sh]
- `e302c98c` 2026-09-08 #513 sgirekills: six host kills removed from dev_sgi_re read arms, and the detector that shipped with them survived four adversarial passes  [gate_arm.sh]
- `4dfc7165` 2026-09-12 #524 (armbdt): an ARM block transfer through a cold host page spliced bytes across a word boundary -- the same LDM/STM at the same unaligned base r...  [gate_arm.sh]
- `7e39a49e` 2026-09-12 #527 (ppcrlwimiwidth, ppcrldimimask): rlwimi rotated a 32-bit word at 64-bit width and never wrote a wrapping mask's high word; rldimi's rotate loo...  [gate_arm.sh]
- `eb26590b` 2026-09-12 #526 (xscaleinten): a guest read of the i80321 interrupt-enable register ended the emulator after loading the right value  [gate_arm.sh]
- `fd150657` 2026-09-12 #519 (sgirandomcolour): the colour-mode PUT default arm stored four host random() bytes into guest memory -- reachable with the documented DE_MODE_...  [gate_arm.sh]
- `bb8efbf0` 2026-09-18 #535 pcc2c040mienannounce: #512's detector missed the cell a real driver writes -- and ran in no gate at all  [gate_arm.sh]
- `78360718` 2026-09-19 #539 n6: the footbridge IRQEnable read computed the right value and then ended the process -- the exit is gone, the value stays; the probes' kill c...  [gate_arm.sh]
- `eec0f4a3` 2026-09-19 #536 wiringcliff: two probes wired into gate_arm.sh, eleven exemptions re-dated to 2026-09-27 by owner ruling -- and the checker's selftest derives...  [gate_arm.sh]
- `4264ee20` 2026-09-23 #545 fbdeclinefive: five footbridge register accesses the DC21285 does not define ended the process -- they are declined and announced once each, d...  [gate_arm.sh]
- `f4f601c4` 2026-09-24 #548 fbdrainwire: #442's drain probe wired into gate 14 on all four timers before its exemption lapsed -- and three floor breaches of #442's own de...  [gate_arm.sh]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
