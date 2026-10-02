ASTRA RETRO-REVIEW (HARNESS) `hbundle_regress27` -- the GXemul fork's regression and pipeline code, 5 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_REGRESS27_ALIVE` on its own line, then ONE verdict line:
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
| `regress/mips_fixedmode_probe.py` | 280 | 3 | 3 |
| `regress/luna_intmask_probe.py` | 279 | 1 | 1 |
| `regress/alpha_pfnoffset_probe.py` | 276 | 2 | 0 |
| `regress/lca_irqstub_uart_probe.py` | 266 | 2 | 0 |
| `regress/gate_ppc.sh` | 264 | 12 | 11 |

**Their rounds**, oldest first:

- `37daeeef` 2026-07-31 Fix #304/#305: the PowerPC narrowed with a host cast, and threw away every NaN it touched  [gate_ppc.sh]
- `622a90a7` 2026-07-31 regress: three round-70B rows could not fail  [gate_ppc.sh]
- `638eff28` 2026-07-31 Fix #309/#310: two more decoders that stopped the machine on legal code  [gate_ppc.sh]
- `161641c4` 2026-08-01 Round 73 (#324, #325): PowerPC mtfsf wrote half its fields into thin air, fctiwz turned a NaN into zero, and the gate row recording that had been m...  [gate_ppc.sh]
- `37963fd9` 2026-08-01 Round 87 (#326): twenty-four legal PowerPC encodings stopped the emulator, and every floating-point record form was one of them  [gate_ppc.sh]
- `ad0e67da` 2026-08-01 Round 88 (#327): VX and FEX were stored, and the ISA defines them as derived  [gate_ppc.sh]
- `130ff1b5` 2026-08-02 Round 89 (#330): the exception causes VX and FEX had nothing to derive from  [gate_ppc.sh]
- `936a434f` 2026-08-02 Round 91 (#336): PowerPC double arithmetic never read its own rounding mode  [gate_ppc.sh]
- `b677ed9d` 2026-08-02 Round 92 (#335): fmadd rounded twice, and whether that was wrong depended on the compiler  [gate_ppc.sh]
- `6f916cd5` 2026-08-05 Round 96 (#344): the negative multiply-adds were never decoded, and halted the emulator  [gate_ppc.sh]
- `d492ddee` 2026-08-05 Round 95 (#343): the fused multiply-adds raised none of their exception causes  [gate_ppc.sh]
- `a3bb9191` 2026-08-12 Round 117 (#376): the #295 detector its reverting mutant demanded  [mips_fixedmode_probe.py]
- `bc42b2ad` 2026-08-12 Round 118 (#377): #376's pass-2 findings -- a wrong measured fact in three records, and a fourth mutant  [mips_fixedmode_probe.py]
- `6c74b31a` 2026-08-13 #392: the readiness predicate matched the same prompt twice  [mips_fixedmode_probe.py]
- `cf4b083c` 2026-08-19 #438 exitsweep: a guest store to INT_ST_MASK0-3 ended the emulator process  [luna_intmask_probe.py]
- `2956c7e8` 2026-09-07 #509 sgimtedepth4dead: `depth == 4' is unreachable, so tiled MTE always took CI  [alpha_pfnoffset_probe.py]
- `7a41b3fb` 2026-09-07 #505 #506 #507 #508: four test-first rounds, three new rung-3 witnesses, and a witness row that could not fail  [alpha_pfnoffset_probe.py]
- `fa5e4e37` 2026-09-08 #514 pass 3: a seat measured two apparatus false passes, one of which I had introduced in the pass-2 repair -- and a duplicate-key guard caught me ...  [lca_irqstub_uart_probe.py]
- `74daefdd` 2026-09-09 #516 lcairqstubkill: every ISA interrupt on alphabook1 routed into a function whose whole body was fatal()+exit(1)  [lca_irqstub_uart_probe.py]
- `7e39a49e` 2026-09-12 #527 (ppcrlwimiwidth, ppcrldimimask): rlwimi rotated a 32-bit word at 64-bit width and never wrote a wrapping mask's high word; rldimi's rotate loo...  [gate_ppc.sh]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
