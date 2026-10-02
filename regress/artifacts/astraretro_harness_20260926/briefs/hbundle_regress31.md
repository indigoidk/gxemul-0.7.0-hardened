ASTRA RETRO-REVIEW (HARNESS) `hbundle_regress31` -- the GXemul fork's regression and pipeline code, 7 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_REGRESS31_ALIVE` on its own line, then ONE verdict line:
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
| `regress/sh_tlbmulti_probe.py` | 194 | 1 | 1 |
| `regress/landisk_aux_probe.py` | 193 | 2 | 0 |
| `regress/readiness_predicate_test.py` | 193 | 6 | 6 |
| `regress/repro_m8sarpurge.c` | 191 | 2 | 2 |
| `regress/selftest_mutation.sh` | 191 | 8 | 8 |
| `regress/sh4_rtcsr_witness.py` | 183 | 1 | 1 |
| `regress/repro_m8invread.c` | 181 | 1 | 1 |

**Their rounds**, oldest first:

- `2050c501` 2026-07-27 Round 55: a regression harness, and the retirement of two gates that could not fail  [selftest_mutation.sh]
- `3eaaf3a4` 2026-07-29 Fix #292: single-precision float results were 1 ulp low half the time  [selftest_mutation.sh]
- `64400062` 2026-07-29 Fix #294: cvt.w honours the FPU rounding mode; trunc.w provably does not  [selftest_mutation.sh]
- `e3d972c1` 2026-07-30 Fix #303: every subnormal decoded wrong, on every architecture at once  [selftest_mutation.sh]
- `37963fd9` 2026-08-01 Round 87 (#326): twenty-four legal PowerPC encodings stopped the emulator, and every floating-point record form was one of them  [selftest_mutation.sh]
- `064caaf6` 2026-08-02 Round 72 (#331-#334): there was no gradual underflow, and three architectures were relying on it  [selftest_mutation.sh]
- `26c133a2` 2026-08-13 #392 pass-2e: the un-fakeable claim survived in three more places  [readiness_predicate_test.py]
- `2b42203a` 2026-08-13 #392 pass-2b: half the fix shipped with no detector, and the truth table never tested the echo  [readiness_predicate_test.py]
- `4565dab8` 2026-08-13 #392 pass-2d: my anti-fake nonce does not bind, and a claimed correction never landed  [readiness_predicate_test.py]
- `6c74b31a` 2026-08-13 #392: the readiness predicate matched the same prompt twice  [readiness_predicate_test.py]
- `a21af04e` 2026-08-13 #399: four gate scripts did not know which gate they were, and a shipped record repeated one of them  [selftest_mutation.sh]
- `c9429e4d` 2026-08-13 #392 pass-2f: my citation "fix" shipped a new wrong claim, and the census has two working evasions  [readiness_predicate_test.py]
- `e8b4233f` 2026-08-13 #392 pass-2c: the pin proved token counts, not arms — and the fixed anchor still had a one-word evasion  [readiness_predicate_test.py]
- `2134a984` 2026-08-16 #436: the detectors could all have stopped detecting, and nothing would have said so  [selftest_mutation.sh]
- `840de826` 2026-08-16 Three failures rendered as one blank cell, and a gate so the third cannot recur  [repro_m8sarpurge.c]
- `84504b1a` 2026-08-16 R8 (#434): a guest READ of six CMMU registers purged the whole translation cache  [repro_m8invread.c]
- `96c91405` 2026-08-16 The seats-read gate vouched for answers nobody opened, and it hid a wrong diagnosis  [repro_m8sarpurge.c]
- `f4374117` 2026-08-21 #449 sh4rtcsr: the host died nine milliseconds after the guest store, in a timer callback  [sh4_rtcsr_witness.py]
- `0678450e` 2026-08-22 #457 three guest stores ended the host process  [sh_tlbmulti_probe.py]
- `bb8efbf0` 2026-09-18 #535 pcc2c040mienannounce: #512's detector missed the cell a real driver writes -- and ran in no gate at all  [landisk_aux_probe.py]
- `e16a8b7c` 2026-09-18 #533 landiskaux: landisk's wdc aux register sat at the PC-layout +0x206, so the kernel's soft reset landed on unmapped memory  [landisk_aux_probe.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
