ASTRA RETRO-REVIEW (HARNESS) `hbundle_tools1` -- the GXemul fork's regression and pipeline code, 4 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_TOOLS1_ALIVE` on its own line, then ONE verdict line:
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
| `tools/panel.sh` | 794 | 20 | 18 |
| `tools/derive_hygiene_pins.sh` | 341 | 1 | 0 |
| `tools/panel_ollama.py` | 150 | 4 | 2 |
| `tools/nightly_check.sh` | 118 | 1 | 1 |

**Their rounds**, oldest first:

- `4f79ff1f` 2026-08-17 panel.sh: the seat check counted a quota wall as an answer  [panel.sh]
- `581b8f36` 2026-08-17 The harness is now in git, and the migration broke one thing that caught itself  [nightly_check.sh, panel.sh, panel_ollama.py]
- `7fc3bbc5` 2026-08-17 panel.sh: my echo test was worse than the bug it fixed  [panel.sh]
- `f39b8984` 2026-08-21 #450 arcbiosubsan: ten uncast shifts, and the author had already cast four of them  [panel.sh]
- `7af59ade` 2026-08-22 Three seats were DOWN and the tooling scored them "answered"  [panel.sh]
- `45d74886` 2026-08-23 A wall is a moment, not a state -- and panel.sh could not see this one  [panel.sh]
- `e6c7e283` 2026-08-24 harness: a 402 wall read as a format miss, a gate that checked existence not tracked-ness, and two invisible ledger fields  [panel.sh]
- `faffad7a` 2026-08-25 panel.sh fires the kimi substitute, and teaching the checkers about it found three unread reviews  [panel.sh]
- `f255ad90` 2026-08-26 panel.sh said "re-firing once" and re-fired nothing  [panel.sh]
- `1f1a02bb` 2026-08-27 #473 wdc ATAPI DATAIN: bound the initial push, and stop reporting zero at the re-arm  [panel.sh]
- `832bed78` 2026-08-27 #478 wdc: an empty ring was read as a full sector, and 512 stale bytes went to the disk  [panel_ollama.py]
- `d64a1fc3` 2026-08-27 #475 wdc ATAPI: clamp the byte count to what REMAINS; plus #474's pass-2 second wave  [panel.sh]
- `673a7a7f` 2026-08-28 panel: migrate the glm seat to glm-5.3-flash:cloud, verified BEFORE the edit  [panel.sh]
- `55ef9db5` 2026-08-29 roster, by owner directive: kimi returns to its CLI, glm-5.3-flash -> glm-5.3 -- and file the RED battery that sat unread for five days  [panel.sh]
- `112867a6` 2026-08-30 #497 closes: the round's record, plus a live defect in panel.sh that was mine  [panel.sh]
- `3c8eb3a9` 2026-08-30 #497b: the panel found eight defects in my records commit, and one was a regression it shipped  [panel.sh]
- `43106c20` 2026-08-30 panelargvcap: panel.sh warned about the argv cap and then launched anyway  [panel.sh]
- `488d0472` 2026-08-30 panel.sh: a walled seat is told to re-fire by hand and now told WHERE the command is  [panel.sh]
- `a115a4aa` 2026-08-30 sgireunmapped pass 1: the option set is SIX-membered, and both new members were in the tree  [panel.sh]
- `70761347` 2026-09-05 pcc2widthkills passes 5-13 + the 2026-09-04 fix review: the fix approved block by block, the detector 190 -> 251 rows, pass 14 OWED (row stays open)  [panel.sh]
- `79cd12e8` 2026-09-06 #502 pass 9-12 and #503: two fixes shipped, a filing overturned to a floor breach and repaired, and a detector's own contract predicting both of it...  [panel_ollama.py]
- `257f56f1` 2026-09-07 #504 sgirandompixel: a failed pixel read handed the caller random() and the write stored it; plus the pass-2 receipt 79cd12e owed, and a measured f...  [panel.sh]
- `7a41b3fb` 2026-09-07 #505 #506 #507 #508: four test-first rounds, three new rung-3 witnesses, and a witness row that could not fail  [panel_ollama.py]
- `3e33201d` 2026-09-24 #546 hygienecensus: gate 6's readiness census was 24 probes stale and RED at HEAD -- re-derived by a tool, never by hand, and the tool went through...  [derive_hygiene_pins.sh]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
