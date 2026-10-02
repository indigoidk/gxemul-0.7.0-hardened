ASTRA RETRO-REVIEW (HARNESS) `hgateoffline` -- the GXemul fork's regression and pipeline code, 1 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HGATEOFFLINE_ALIVE` on its own line, then ONE verdict line:
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
| `regress/gate_offline.sh` | 2398 | 83 | 76 |

**Their rounds**, oldest first:

- `2050c501` 2026-07-27 Round 55: a regression harness, and the retirement of two gates that could not fail  [gate_offline.sh]
- `3eaaf3a4` 2026-07-29 Fix #292: single-precision float results were 1 ulp low half the time  [gate_offline.sh]
- `db562cfb` 2026-07-29 Use plainer words in the docs and comments  [gate_offline.sh]
- `51899d78` 2026-07-30 Fix #299: the single-precision sum was rounded twice; round-to-odd makes the first rounding harmless  [gate_offline.sh]
- `e3d972c1` 2026-07-30 Fix #303: every subnormal decoded wrong, on every architecture at once  [gate_offline.sh]
- `064caaf6` 2026-08-02 Round 72 (#331-#334): there was no gradual underflow, and three architectures were relying on it  [gate_offline.sh]
- `bf4a1e98` 2026-08-11 Round 116 (#375): pin the mips_loadstore[] index coupling as a checked invariant  [gate_offline.sh]
- `26c133a2` 2026-08-13 #392 pass-2e: the un-fakeable claim survived in three more places  [gate_offline.sh]
- `28ac1f8b` 2026-08-13 #400: the SH-4 timer pinned itself at zero, and a booting guest's clock stopped  [gate_offline.sh]
- `2b42203a` 2026-08-13 #392 pass-2b: half the fix shipped with no detector, and the truth table never tested the echo  [gate_offline.sh]
- `4565dab8` 2026-08-13 #392 pass-2d: my anti-fake nonce does not bind, and a claimed correction never landed  [gate_offline.sh]
- `6c74b31a` 2026-08-13 #392: the readiness predicate matched the same prompt twice  [gate_offline.sh]
- `7dde2b81` 2026-08-13 #401: the eleven rows never once exercised the modulo, which is the correction  [gate_offline.sh]
- `e8b4233f` 2026-08-13 #392 pass-2c: the pin proved token counts, not arms — and the fixed anchor still had a one-word evasion  [gate_offline.sh]
- `085766ac` 2026-08-14 #407: #405's detector had four holes and a note that was wrong the flattering way  [gate_offline.sh]
- `154d21cd` 2026-08-14 #414: every -d g disk and every floppy reported zero capacity, from one multiplication with two factors nobody computed  [gate_offline.sh]
- `2e709cdb` 2026-08-14 #405: ATA IDENTIFY packed its capacity bytes with `% 255`, not `& 255`  [gate_offline.sh]
- `4b1432b1` 2026-08-14 #417: #416's own bound disarmed the rows that tested it, and its sense latch outlived the failure it described  [gate_offline.sh]
- `6ab49ad5` 2026-08-14 #410: the wdc detector is DONE, against a written condition instead of a feeling  [gate_offline.sh]
- `994d8ea0` 2026-08-14 #412: every floppy in this fork tells the guest it holds 2 TiB  [gate_offline.sh]
- `a68ddbc1` 2026-08-14 #413: #412's prose was wrong in four places -- a floppy answers nothing, because no device asks for one  [gate_offline.sh]
- `b355dcdb` 2026-08-14 #406: a prose "DEVINIT" in a comment globbed the whole directory into autodev.c  [gate_offline.sh]
- `b460e3db` 2026-08-14 #418: the documented `d:` override did nothing, and the obvious place to fix it rounds the advertised capacity up  [gate_offline.sh]
- `bd5b9104` 2026-08-14 #403: gcov said the interrupt line had never run, and fourteen wrong versions passed  [gate_offline.sh]
- `c6169e06` 2026-08-14 #416: one guest WRITE past the end of a 10 KB image grew it to 512 MB, and the guest was told it succeeded  [gate_offline.sh]
- `e86e293a` 2026-08-14 #408: the round that fixed stale citations made the identical error, and the detector was relying on -O2 to hide UB  [gate_offline.sh]
- `f70db4bb` 2026-08-14 #409: #408's UB fix cost 148 seconds, and it poisoned one stub out of three  [gate_offline.sh]
- `2458cfba` 2026-08-15 R5 (#430, #431): memory_rw translated the first page and then copied straight past it  [gate_offline.sh]
- `35302f2b` 2026-08-15 R6 (#432): a guest-written zero made the footbridge timer divide by zero  [gate_offline.sh]
- `4dc1ff8c` 2026-08-15 R2 follow-up: the census could delete the caller's directory, and the round overstated itself  [gate_offline.sh]
- `81506bd8` 2026-08-15 R2 (#424): the parser selftest ran nowhere, and could not see a mutant that moves text  [gate_offline.sh]
- `84f442d7` 2026-08-15 R6 pass 2: three mutants survived all fifteen rows, and one record was false  [gate_offline.sh]
- `863d2389` 2026-08-15 R4 (#427, #428, #429): the timer core clamped one end of a frequency and left the other unbounded  [gate_offline.sh]
- `a20ebc5a` 2026-08-15 R3 (#425, #426): the gate graded constants the run never used, and a green row said so  [gate_offline.sh]
- `cdc48499` 2026-08-15 R4 follow-up: the round's detector certified six things it could not see  [gate_offline.sh]
- `f92e5a1c` 2026-08-15 R1 (#422, #423): the harness could not be pointed anywhere else, and kept no wall time  [gate_offline.sh]
- `12ea008c` 2026-08-16 R7 pass 2: the fold is right, the detector defending it was not  [gate_offline.sh]
- `2134a984` 2026-08-16 #436: the detectors could all have stopped detecting, and nothing would have said so  [gate_offline.sh]
- `2a5bc480` 2026-08-16 R9 (#435): half this device's translation-cache purges were for registers nothing reads  [gate_offline.sh]
- `66b03678` 2026-08-16 R7 (#433): an ordinary guest register read terminated the host, on the rig that boots  [gate_offline.sh]
- `6adccce0` 2026-08-16 A panel-completeness audit found a surviving mutant, and the audit is the finding  [gate_offline.sh]
- `84504b1a` 2026-08-16 R8 (#434): a guest READ of six CMMU registers purged the whole translation cache  [gate_offline.sh]
- `cedc80d5` 2026-08-16 R7 addendum: the panel had already found both, and nobody had read it  [gate_offline.sh]
- `581b8f36` 2026-08-17 The harness is now in git, and the migration broke one thing that caught itself  [gate_offline.sh]
- `abd7bad9` 2026-08-17 #436 pass 2: four defeats, and the worst was in the control I had just added  [gate_offline.sh]
- `f8db56cc` 2026-08-17 A seat ran a gate and deadlocked, and its failure was the most useful of the pass  [gate_offline.sh]
- `4d0981dc` 2026-08-18 #437: SYNCHRONIZE CACHE told the guest its data was safe and synced the wrong file  [gate_offline.sh]
- `09b1059f` 2026-08-19 selfmutant6: the last two disk controls, and a THIRD apparatus hazard class  [gate_offline.sh]
- `17de78a0` 2026-08-19 regress: a detector for #429's RTC range check (gate 2: 245 -> 254 checks)  [gate_offline.sh]
- `20ce22e9` 2026-08-19 sh4_tmu: pin the half of this harness's own claim that nothing asserted  [gate_offline.sh]
- `27dd47a0` 2026-08-19 rtcdet pass 3: the measure seat found the cheapest escape on record, and Fable found six wrong records  [gate_offline.sh]
- `6014b7e7` 2026-08-19 selfmutant6 CLOSED: the fifth control, and the first committed footbridge witness  [gate_offline.sh]
- `7e3b1204` 2026-08-19 Fable adjudicates the witness ladder, closes gate3scope, and the SELFCHECK gap is gated  [gate_offline.sh]
- `9976161a` 2026-08-19 gate_hygiene was LATENTLY RED at HEAD, and the probe that caused it shipped unwired  [gate_offline.sh]
- `cd32ed2a` 2026-08-19 rtcdet pass 2: the panel found a real escape, and two of its three claims did not survive  [gate_offline.sh]
- `e051fc51` 2026-08-19 m437ord: gate the ordering rule #437 shipped without, and it takes TWO overlays  [gate_offline.sh]
- `eaff9a30` 2026-08-19 selfmutant6: two of five controls built, and the blocker was a MISSING VERDICT TOKEN  [gate_offline.sh]
- `3193d566` 2026-08-20 #442 fbpending: an overflowed counter stopped the emulated clock for 40 seconds  [gate_offline.sh]
- `6e369434` 2026-08-20 smdatefmt: a malformed exemption date never expired, in BOTH manifests  [gate_offline.sh]
- `af40df5a` 2026-08-20 Five seats voted to drop constblind as "already fixed" -- and the live instance was mine, from hours earlier  [gate_offline.sh]
- `6b6d5965` 2026-08-21 #446 pass 2: sixteen mutants, sixteen passed -- and a comment-only file passed too  [gate_offline.sh]
- `bcdbfb88` 2026-08-21 #446 sgiarcbiosoob: a heap overflow no harness had run, and not where ASan pointed  [gate_offline.sh]
- `29b450ce` 2026-08-26 #467 + #468: the pty deadline means SILENCE, and the ASIC domain is now ENFORCED  [gate_offline.sh]
- `00d546de` 2026-08-27 #472 b115: an unaligned overlay read took its bytes from the wrong layer  [gate_offline.sh]
- `0922465f` 2026-08-27 #477 wdc ATAPI: a guest data-port WRITE could free the transfer being delivered  [gate_offline.sh]
- `09362f0e` 2026-08-27 #488 diskimage: a short read in a NON-FINAL iteration corrupted twice, and the round that touched these exact lines was asking a different question  [gate_offline.sh]
- `1cec2daf` 2026-08-27 #476 wdc: #475's clamp WOKE a NULL dereference -- two guest accesses killed the host  [gate_offline.sh]
- `1f1a02bb` 2026-08-27 #473 wdc ATAPI DATAIN: bound the initial push, and stop reporting zero at the re-arm  [gate_offline.sh]
- `3403c013` 2026-08-27 #482 wdc: the abort row could not say which state gated the abort  [gate_offline.sh]
- `7d0b63d4` 2026-08-27 #480 wdc: the detector could not see its own call  [gate_offline.sh]
- `867c697b` 2026-08-27 #481 wdc: the reset bit was the head-count bit  [gate_offline.sh]
- `ce75b1d2` 2026-08-27 #483 wdc: the sweep pinned the decode across 256 values and the purge at none  [gate_offline.sh]
- `cf300c07` 2026-08-27 #484 wdc: a full ring reported itself empty, and the next push destroyed a byte  [gate_offline.sh]
- `d64a1fc3` 2026-08-27 #475 wdc ATAPI: clamp the byte count to what REMAINS; plus #474's pass-2 second wave  [gate_offline.sh]
- `d8191881` 2026-08-27 #485 wdc: 242 of 256 opcodes ended a command and never raised its interrupt  [gate_offline.sh]
- `d894e35d` 2026-08-27 #474 footbridge TIMER_x_CLEAR read-clears; plus #473's pass-2 corrections  [gate_offline.sh]
- `83df95c3` 2026-09-05 Retrospective re-check batch 3a (dev_wdc.c #337..#464): every fix holds; two guest-visible ATAPI defects filed MEDIUM, seven LOW rows, two merges, ...  [gate_offline.sh]
- `cdbe7d75` 2026-09-18 #537 fbsmlane: #442's harness printed a verdict token its own self-mutant lane could never read -- the lane runs, pinned on R3  [gate_offline.sh]
- `408accf7` 2026-09-19 gate 2: SC_EXEMPT's two dates had passed on 2026-09-02 with no owner -- re-dated to 2026-09-27 by owner ruling, in its own commit  [gate_offline.sh]
- `4264ee20` 2026-09-23 #545 fbdeclinefive: five footbridge register accesses the DC21285 does not define ended the process -- they are declined and announced once each, d...  [gate_offline.sh]
- `f4f601c4` 2026-09-24 #548 fbdrainwire: #442's drain probe wired into gate 14 on all four timers before its exemption lapsed -- and three floor breaches of #442's own de...  [gate_offline.sh]
- `04500deb` 2026-09-26 #550 exemptredate: the ten probe-wiring exemptions due 2026-09-27 re-dated one by one, each to its own owed-work date (2026-10-08 .. 2026-12-03), a...  [gate_offline.sh]
- `f5e155ac` 2026-09-26 #551 wdcidselfcheck: gate 2's wdc_identify self-check exemption discharged, not re-dated -- diff_wdc_identify.c gains a self-check on its two compa...  [gate_offline.sh]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
