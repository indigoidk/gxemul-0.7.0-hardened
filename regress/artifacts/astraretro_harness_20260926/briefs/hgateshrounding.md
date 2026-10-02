ASTRA RETRO-REVIEW (HARNESS) `hgateshrounding` -- the GXemul fork's regression and pipeline code, 1 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HGATESHROUNDING_ALIVE` on its own line, then ONE verdict line:
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
| `regress/gate_sh_rounding.sh` | 1712 | 45 | 41 |

**Their rounds**, oldest first:

- `f52c2fe3` 2026-07-29 Fix #296: SuperH read the FPU rounding-mode field but never used it  [gate_sh_rounding.sh]
- `06445b53` 2026-07-30 Fix #297: ftrc converted with a raw C cast, so the guest's answer depended on the host  [gate_sh_rounding.sh]
- `51899d78` 2026-07-30 Fix #299: the single-precision sum was rounded twice; round-to-odd makes the first rounding harmless  [gate_sh_rounding.sh]
- `e3d972c1` 2026-07-30 Fix #303: every subnormal decoded wrong, on every architecture at once  [gate_sh_rounding.sh]
- `e644a300` 2026-07-30 Fix #300: the D-format store has nothing to round, so the arithmetic learned to  [gate_sh_rounding.sh]
- `54f72c06` 2026-07-31 Round 80 (#315, #316, #317): the SuperH halts a decode sweep cannot see  [gate_sh_rounding.sh]
- `6a2f41c2` 2026-07-31 Round 81 (#318): the store-queue flush round 80 refused to guess at  [gate_sh_rounding.sh]
- `f415b919` 2026-07-31 Round 79 (#314): SuperH answered a legal instruction by stopping  [gate_sh_rounding.sh]
- `3536d869` 2026-08-21 #443 pass 2: seven mutants all scored 29/29, and my own kill table said so  [gate_sh_rounding.sh]
- `6bec468c` 2026-08-21 #443 sh4pcicexit: one guest LOAD ended the host, on 116 of 137 offsets  [gate_sh_rounding.sh]
- `798cff34` 2026-08-21 flagship batch: two wrong records I shipped, and three FALSE ACCEPTS in the wiring checker  [gate_sh_rounding.sh]
- `a636a339` 2026-08-21 #448 sh4chcr: a LEGAL DMA configuration ended the host on its resource-select alone  [gate_sh_rounding.sh]
- `e841f443` 2026-08-21 #447 sh4valguards: one guest STORE ended the host, at four sites whose store positions differ  [gate_sh_rounding.sh]
- `f4374117` 2026-08-21 #449 sh4rtcsr: the host died nine milliseconds after the guest store, in a timer callback  [gate_sh_rounding.sh]
- `0678450e` 2026-08-22 #457 three guest stores ended the host process  [gate_sh_rounding.sh]
- `3ff21380` 2026-08-22 #454 the store-queue PREF transfer is judged READ type, and a gate row pinned the opposite  [gate_sh_rounding.sh]
- `759f7131` 2026-08-22 sh4_chcr: a two-character edit restored a host death at 18/18 -- add the L0 safety row  [gate_sh_rounding.sh]
- `927553fa` 2026-08-22 #452 sh4 TLB data array 2: decline the access instead of ending the host process  [gate_sh_rounding.sh]
- `9d5fd693` 2026-08-22 #456 the SH test machine could not deliver an interrupt at all  [gate_sh_rounding.sh]
- `b3ad305a` 2026-08-22 #451 sh4_sci_cmd(): decline the command instead of ending the host process  [gate_sh_rounding.sh]
- `dc0c9d50` 2026-08-22 #455 an interrupt at priority 0 ended the host process  [gate_sh_rounding.sh]
- `f532bb6a` 2026-08-22 #453 sh4_dmac_transfer(): the last guest-reachable host death, and hardware accuracy meant NOT sending the interrupt  [gate_sh_rounding.sh]
- `0bb8be2b` 2026-08-23 #459: one guest store to 0xffd80010 ended the host on 3 of 5 SH machines  [gate_sh_rounding.sh]
- `7e5c0f6c` 2026-08-23 #458: SH-4 read two of four interrupt priority registers, and SCIF's came       from a register this machine never maps  [gate_sh_rounding.sh]
- `98a34085` 2026-08-23 #460: GDROM_DATA had no legal first touch -- four exit(1) on one register  [gate_sh_rounding.sh]
- `ba30e64f` 2026-08-23 #461 both `default:` arms of the GD-ROM device ended the host process  [gate_sh_rounding.sh]
- `7c9dd9eb` 2026-08-24 #462 both arms of the GD-ROM DMA trigger (case 0x18) ended the host process on a guest store  [gate_sh_rounding.sh]
- `f1fa6a0a` 2026-08-25 #463 dreamcast_asic: one guest LOAD ended the host, at 64 byte addresses  [gate_sh_rounding.sh]
- `4d05cf0b` 2026-08-26 #465 dev_dreamcast_gdrom.c: data and data_len were released apart, and the detector ran in no gate  [gate_sh_rounding.sh]
- `5b5089d0` 2026-08-26 #465 pass 2: the panel refuted my own framing, and the "owed" rows already existed  [gate_sh_rounding.sh]
- `733a4b65` 2026-08-26 #464 pass 2: one wrong record, one filed escape, and two seats the harness was losing  [gate_sh_rounding.sh]
- `baacf9bb` 2026-08-26 #464 wdc: six unlatched fatal() bounded, and the detector's first gate  [gate_sh_rounding.sh]
- `05ec21e1` 2026-08-27 gate: apply the annotation 91bf4e9's message claimed, and record why it was missing  [gate_sh_rounding.sh]
- `91bf4e9e` 2026-08-27 gate: a source-count pin was RED for two rounds and nobody saw it  [gate_sh_rounding.sh]
- `095aa960` 2026-08-28 #489 gdrom: a guest-supplied length ended the host, and deleting the guard would have been worse  [gate_sh_rounding.sh]
- `d9efd339` 2026-08-29 #492 the six battery reds -- and a detector that passed its own kill table with an L2 breach live in it  [gate_sh_rounding.sh]
- `fb0cc783` 2026-08-29 #490 GD-ROM handle_command: two guest-reachable host kills, plus a wsl-dollar hook  [gate_sh_rounding.sh]
- `105c15c7` 2026-08-30 #496: the detector's first CLEAN baselines, two more escapes closed, and a selftest that broke because the tree got better  [gate_sh_rounding.sh]
- `439dfd05` 2026-08-30 #496 follow-up: two MEASURED escapes closed, and a deriver that matched itself  [gate_sh_rounding.sh]
- `beadf9a7` 2026-08-30 #496: five MEASURED escapes closed, and the axis nobody sampled  [gate_sh_rounding.sh]
- `c516a9c9` 2026-08-30 #496 GD-ROM: two guest-reachable host kills de-fatalised, plus the store that made a naive fix worse than the defect -- and the ADJUDICATION PASS  [gate_sh_rounding.sh]
- `79cd12e8` 2026-09-06 #502 pass 9-12 and #503: two fixes shipped, a filing overturned to a floor breach and repaired, and a detector's own contract predicting both of it...  [gate_sh_rounding.sh]
- `599a7a82` 2026-09-12 #525 (wdcaltdigin): the alt-status handler never decoded its offset ON THE READ SIDE, so a read of the Drive Address register returned the ALT-STAT...  [gate_sh_rounding.sh]
- `ca3be4eb` 2026-09-12 #528 (mapledmaaddr): a guest read of the Dreamcast Maple DMA-address register ended the emulator after computing the right value  [gate_sh_rounding.sh]
- `e16a8b7c` 2026-09-18 #533 landiskaux: landisk's wdc aux register sat at the PC-layout +0x206, so the kernel's soft reset landed on unmapped memory  [gate_sh_rounding.sh]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
