ASTRA RETRO-REVIEW (HARNESS) `hprecommitcheck` -- the GXemul fork's regression and pipeline code, 1 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HPRECOMMITCHECK_ALIVE` on its own line, then ONE verdict line:
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
| `tools/precommit_check.sh` | 1306 | 45 | 37 |

**Their rounds**, oldest first:

- `1ba2cd4e` 2026-08-17 harness: track the carrier, and gate the copy that makes tracking possible  [precommit_check.sh]
- `581b8f36` 2026-08-17 The harness is now in git, and the migration broke one thing that caught itself  [precommit_check.sh]
- `c3d13e57` 2026-08-17 harness: gate the flagship seat's OWED work, not just its missing work  [precommit_check.sh]
- `27dd47a0` 2026-08-19 rtcdet pass 3: the measure seat found the cheapest escape on record, and Fable found six wrong records  [precommit_check.sh]
- `7570f1d8` 2026-08-19 precommit_check.sh: the checker that gates every commit had 11 measured defects  [precommit_check.sh]
- `aa10c9f1` 2026-08-19 witness field: enforce the ladder's own rule, and its first run found a gap in the ladder  [precommit_check.sh]
- `0d0283c9` 2026-08-20 The matrix is a generated file and nothing checked that it was regenerated  [precommit_check.sh]
- `4f342a27` 2026-08-20 Records cluster panelled, and a seat broke the brief's letter to serve its purpose  [precommit_check.sh]
- `9296fc6f` 2026-08-20 The ledger recorded seats as AGREEING when it only knew they were FIRED  [precommit_check.sh]
- `b16a0eee` 2026-08-20 A row that exists only in the ledger is work a fresh session will not see  [precommit_check.sh]
- `b584682f` 2026-08-20 m88k cluster panelled, and the queue's held-stage list is now DERIVED after it drifted  [precommit_check.sh]
- `fd0ddefb` 2026-08-20 optrow: the audit is done, its answer is "one", and it is now mechanised because audits expire  [precommit_check.sh]
- `85bc6ab4` 2026-08-21 probewiring: four rounds of detectors that no gate has ever run  [precommit_check.sh]
- `c2cf7bc9` 2026-08-21 The queue gate matched ids by substring, so it was green over the one thing it exists to catch  [precommit_check.sh]
- `0678450e` 2026-08-22 #457 three guest stores ended the host process  [precommit_check.sh]
- `6b89e1ca` 2026-08-22 Receipt SHA, two closures, and a brittle check of my own  [precommit_check.sh]
- `8185920e` 2026-08-22 Track which seat was RIGHT, not just which seat answered  [precommit_check.sh]
- `9d5fd693` 2026-08-22 #456 the SH test machine could not deliver an interrupt at all  [precommit_check.sh]
- `2965aa1b` 2026-08-23 #459 records: close sh4pclock, file four, grade nine seats  [precommit_check.sh]
- `3ad72e04` 2026-08-23 harness: score-claims gate, verdict-extractor fix, floor clause (d), 2 filings  [precommit_check.sh]
- `6bfbb9f8` 2026-08-23 precommit W: the queue file must not advertise shipped work (six were)  [precommit_check.sh]
- `740213a2` 2026-08-23 precommit W: a ledger row's state must agree with what shipped  [precommit_check.sh]
- `8eeeea21` 2026-08-23 verdict extractor: a measured regression in my own fix, and the guard that fixes it  [precommit_check.sh]
- `e4390ea0` 2026-08-23 #459 pass-2 corrections: three wrong records, all found by measurement  [precommit_check.sh]
- `e9f8c0cc` 2026-08-23 harness pass 2: two measured false passes fixed, verdict detector shipped  [precommit_check.sh]
- `6852e574` 2026-08-24 precommit X: a cited measurement must exist, and the gate that says so is tested  [precommit_check.sh]
- `4d05cf0b` 2026-08-26 #465 dev_dreamcast_gdrom.c: data and data_len were released apart, and the detector ran in no gate  [precommit_check.sh]
- `bdb55664` 2026-08-26 five held-stage seats: a slack ratchet, four PowerPC manuals, and a one-word escape  [precommit_check.sh]
- `25da4045` 2026-08-27 precommit Y: guard tracked text files against NUL bytes  [precommit_check.sh]
- `832bed78` 2026-08-27 #478 wdc: an empty ring was read as a full sector, and 512 stale bytes went to the disk  [precommit_check.sh]
- `095aa960` 2026-08-28 #489 gdrom: a guest-supplied length ended the host, and deleting the guard would have been worse  [precommit_check.sh]
- `fb0cc783` 2026-08-29 #490 GD-ROM handle_command: two guest-reachable host kills, plus a wsl-dollar hook  [precommit_check.sh]
- `7be9f804` 2026-08-30 #496 L2 + L4: a one-line edit disabled the exemption-expiry mechanism and scored 21/21  [precommit_check.sh]
- `af62a068` 2026-08-30 wdcatapistswap regress review: PASS, and it found the round clobbering its own logs  [precommit_check.sh]
- `beadf9a7` 2026-08-30 #496: five MEASURED escapes closed, and the axis nobody sampled  [precommit_check.sh]
- `c516a9c9` 2026-08-30 #496 GD-ROM: two guest-reachable host kills de-fatalised, plus the store that made a naive fix worse than the defect -- and the ADJUDICATION PASS  [precommit_check.sh]
- `e61ccd89` 2026-08-30 wdcatapistswap: the accept side of #495's guard, and a floor breach found while pinning it  [precommit_check.sh]
- `599a7a82` 2026-09-12 #525 (wdcaltdigin): the alt-status handler never decoded its offset ON THE READ SIDE, so a read of the Drive Address register returned the ALT-STAT...  [precommit_check.sh]
- `7e39a49e` 2026-09-12 #527 (ppcrlwimiwidth, ppcrldimimask): rlwimi rotated a 32-bit word at 64-bit width and never wrote a wrapping mask's high word; rldimi's rotate loo...  [precommit_check.sh]
- `ca3be4eb` 2026-09-12 #528 (mapledmaaddr): a guest read of the Dreamcast Maple DMA-address register ended the emulator after computing the right value  [precommit_check.sh]
- `09ded75c` 2026-09-18 #534 stagetokens: four tools read one ledger field, each with its own copy of what it meant  [precommit_check.sh]
- `e16a8b7c` 2026-09-18 #533 landiskaux: landisk's wdc aux register sat at the PC-layout +0x206, so the kernel's soft reset landed on unmapped memory  [precommit_check.sh]
- `eec0f4a3` 2026-09-19 #536 wiringcliff: two probes wired into gate_arm.sh, eleven exemptions re-dated to 2026-09-27 by owner ruling -- and the checker's selftest derives...  [precommit_check.sh]
- `04500deb` 2026-09-26 #550 exemptredate: the ten probe-wiring exemptions due 2026-09-27 re-dated one by one, each to its own owed-work date (2026-10-08 .. 2026-12-03), a...  [precommit_check.sh]
- `8ea26abb` 2026-09-26 #549 fbctrlportkill: the test machines' framebuffer controller stored an out-of-range port selector and the next DATA access ended the emulator pro...  [precommit_check.sh]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
