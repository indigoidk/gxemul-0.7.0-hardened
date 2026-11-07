# Reading task: oldest-rec-570 (Gemini web; 2026-11-06)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC570-b1fc` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #570 m88kbuserrregs (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.

## The round block (verbatim, CHANGELOG.md lines 2055-2272 at HEAD)

```markdown
# `#570` (m88kbuserrregs): a refused m88k device access raised the access exception without recording the bus error in the CMMU -- PFSR (BERROR) and PFAR (the physical address) are now written on the faulting side's CMMU, LUNA-88K's probe address faults through the same arm instead of being served 0, and a 31-row rung-3 detector gates it in gate 14

**The defect** (`m88kbuserrregs`, MED; filed 2026-10-22 from the external-fixes research, T36 of its batch; the carrier
of the reopened PFAR item).  `src/cpus/memory_rw.c`'s MEM_M88K device-failure arm -- reached when a device CLAIMS an
address and its handler REFUSES the access (`res <= 0`) with exceptions enabled -- raised `M88K_EXCEPTION_DATA_ACCESS` /
`INSTRUCTION_ACCESS` and wrote nothing into the CMMU: `PFSR` kept whatever it held and `PFAR` never carried the faulting
address, while a guest fault handler (OpenBSD/mvme88k's `trap.c:326-335`, `:405-411`) reads `PFSR`'s fault field to
tell a bus error from a translation fault.  `src/devices/dev_luna88k.c`'s `case 0x3ffffff0:` -- the address
OpenBSD/luna88k touches to provoke an illegal-address fault -- wrote `cmmu[1]`'s PFSR directly, served the load as 0 and
raised no exception at all.  The rung-3 witness (`regress/artifacts/m88kbuserrregs/witness_20261023/`, cold debugger on
UNMODIFIED mvme187 and luna-88k, HEAD `66920157` = `7fca7187` in source) is RED on HEAD: 16/24, eight symptom rows red
for the reason under test -- after a refused load and a refused store at mvme187's `unreadable` window (`0xfff46010`) and
a refused load at VME population 1 (`0xfff40090`), the data CMMU still holds the probe's seeds in PFSR (`0x5a5a5a5a`,
wanted `0x00030000`) and PFAR (`0x13572468`, wanted the address), and the instruction CMMU keeps its seeds; on luna-88k
the load at `0x3ffffff0` is served 0 with no vector and PFAR keeps its seed.  Six controls green (both CMMUs' IDR read
`0x00a90000`, a value RAM cannot return; the four seeds round-trip; SXIP/DMA0 attribute each exception to its access; a
free-running control shows the same stale registers).  The witness also corrected three premises the research row
carried: an access to an address NO device claims never reaches this arm (served zeros, no exception -- filed as
`m88kunclaimedberr`); on an unmodified luna-88k every other device refusal stops the cpu before the arm (so the generic
half is witnessed on mvme187); and the LUNA case already wrote PFSR -- what it lacked was PFAR and the exception.

**What ships** (four product files, byte-identical in `GXEMUL-SEC/` and `est/`; three harness files).
* `src/cpus/memory_rw.c` -- in the MEM_M88K arm the upstream TODO ("the faulting address should probably be included
  somewhere too") is replaced by the writes: `cmmu = cpu->cd.m88k.cmmu[cache == CACHE_INSTRUCTION ? 0 : 1]` (0 = the
  instruction CMMU, 1 = the data CMMU, `memory_m88k.c`'s index); if non-NULL, `reg[CMMU_PFSR] = CMMU_PFSR_BERROR << 16`
  (the field OpenBSD extracts with `(pfsr >> 16) & 7`) and `reg[CMMU_PFAR] = (uint32_t) orig_paddr` -- the PHYSICAL
  address saved at the top of the scan, before `paddr` was made device-relative.  The sibling CMMU is not written; a cpu
  without a CMMU gets no write and still takes the exception; the `res <= 0 && !no_exceptions` guard, the `debug()` line,
  the vector expression and `return MEMORY_ACCESS_FAILED` are untouched (NO_EXCEPTIONS callers -- the debugger -- never
  reach the writes).  PFAR is written unmasked, upstream's form; whether MC88200 silicon forces its low two bits is
  UNKNOWN (no MC88200 manual on disk) and the detector's accesses are all word-aligned.
* `src/cpus/cpu_m88k.c` -- `#include "thirdparty/m8820x.h"` after the existing `m8820x_pte.h` include: the arm is compiled
  inside this translation unit through `tmp_m88k_tail.c`, and `CMMU_PFSR`, `CMMU_PFAR` and `CMMU_PFSR_BERROR` exist only
  in that header, so the repair as the research ruling wrote it did not compile.  Found by the pass-1 brief's drafter,
  confirmed by all four seats (a FOURTH product file no ruling had named).  Upstream adds the same include to this file
  (before `m8820x_pte.h` there; the position is not load-bearing).
* `src/devices/dev_luna88k.c` -- `case 0x3ffffff0:` becomes `return 0;`: the access is REFUSED and takes the common arm
  (vector 3, PFSR and PFAR in the data CMMU for a load or store; a fetch takes the instruction CMMU and vector 2).  The
  case is KEPT: without it the access reaches `default:`, which stops the cpu.  Its own PFSR write is deleted (it wrote
  `cmmu[1]` even for an instruction access).  `return 0` skips the common tail, which only writes the already-zeroed
  read buffer that a failing load never consumes.  Option set recorded in `pass1_20261023/PASS1_RULINGS.md` A10: keep
  `return 1` + PFAR (ACCEPT with metadata), `return 0` (FAULT, chosen), upstream's `DEV_RAM_FAIL` device or
  `dev_unreadable` at the address (FAULT by another device), delete the case (stops the cpu), the LUNA house-style
  `cpu->running = 0` (stops the cpu).
* `src/devices/dev_m8820x.c` -- COMMENT-ONLY: four sentences that said the model writes PFSR/PFAR only at
  `memory_m88k.c:382-405` (and one that cited `dev_luna88k.c:614` for a write now gone) name `memory_rw.c`'s arm.
  Rewrapped so the line count is unchanged (a `FAILURE()` macro embeds `__LINE__`); the object `dev_m8820x.o` is
  byte-identical before and after (`table1_20261023/objmd5_work_before.txt` / `_after.txt`) -- the "comment-only" claim
  is a measurement.
* `regress/m88k_buserr_probe.py` (new; 836 lines) -- the detector, revision 2 of the witness probe (the witness file
  itself is kept byte-identical under `witness_20261023/`, md5 `d59798b0`).  TWO IDENTITIES: the MEASURED instrument is
  rev 2, md5 `d57c12ab` (frozen before any table as `table1_20261023/m88k_buserr_probe.rev2.frozen.py.txt`; every
  score, the gate receipt and the MANIFEST's measured line name it); the SHIPPED file is DOCUMENTATION revision 2c, md5
  `a49f417d37484071143de7e13637f4a4` -- a docstring-only re-freeze made after pass 2 (the executable `REVISION = 2` and
  every line outside the module docstring byte-identical: with the docstring stripped both files are 28,722 bytes and
  `cmp` clean, the AST's 209 statements identical; `repair1_20261024/rev2b.docstring.diff`, `rev2b_equivalence.txt`),
  rerun on the fixed and the HEAD binaries and compared ROW BY ROW with `fixed.out` / `prefix_HEAD.out` (31/31 and 21/31,
  all 33 row/INFO lines and the CONTROL / SYMPTOM / sentinel lines identical; `repair1_20261024/rev2b_rowcompare.txt`).
  The docstring grew by 12 lines, so a citation into the probe's CODE must name its revision (`REVISION = 2` is at rev-2
  `:238` and rev-2b `:250`).  The intermediate revisions (`fe8cc784`, `9046d774` = 2b; each matched row by row) are kept in
  `repair1_20261024/superseded_fe8cc784/` and `superseded_9046d774/`.  The historical receipts stay measurements of rev 2's bytes; the
  documentation-only equivalence is what carries them to the shipped file.  31 rows, cold-debugger sessions piped on
  unmodified `-E mvme88k -e mvme187` and `-E luna88k -e luna-88k` (a 4-byte dummy image by default; the rig image
  measured identical): the 24 witness rows -- six controls (`neg apparatus`, `mv devsig`, `mv cmmu rt`, `luna devsig`,
  `luna cmmu rt`, `unasm` = 192 placed words re-read by the disassembler, pinned by equality), `ok route`/`ok regs` (a
  SERVED access -- VME's cased VBR register -- leaves all four seeds untouched: the accept side), and per refused cell
  (`uld`, `ust`, `vme`, `luna`) `route` (the vector, SXIP and DMA0), `pfsr` (`0x00030000` by value), `pfar` (the absolute
  physical address by value: `0xfff46010`, `0xfff40090`, `0x3ffffff0` -- PFAR is pinned absolutely, never by distinctness,
  so a shifted register decode reds) and `icmmu` (the sibling keeps its two seeds) -- plus the seven rows the pass-1
  adjudication added for the floor cells the witness did not hold: `ifetch route` (an attribution row: vector 2 / SXIP),
  `ifetch pfsr`, `ifetch pfar`, `ifetch dcmmu` (the INSTRUCTION label of the selector the fix adds, reached by stepping
  onto the `unreadable` window -- the channel is the step loop's disassembly pre-read, `m88kstepprefetch`, DISCLOSED in
  the contract: when that is fixed these rows red for an unrelated reason and are re-rooted), `dbg noexc` (a debugger
  `dump` of the refusing window in a dedicated session: zeros returned, four seeds unchanged, no vector, cpu running --
  the `!no_exceptions` conjunct of the guard), and `null surv` / `null route` (mvme187 `-n 2`: `pause 1` starts cpu 1,
  which the machine gave no CMMU -- `focus 1` sets its pc, registers and VBR; it performs the refused data load, whose
  handler stores a HANDLED marker while the fall-through would store FELL, then jumps into the refusing window for an
  instruction-fetch refusal with `cmmu[0] == NULL`; the session must survive both and HANDLED/FELL must read set/clear --
  the NULL check's data AND instruction cells in one session.  That second fault arrives while PSR.SFRZ is still set
  from the first, so `m88k_exception` delivers it as ERROR, vector 10 (`cpu_m88k.c:811-819`); no `rte` clears it --
  an `rte` would resume at SNIP, the FELL store -- and the arm and its NULL test run before the exception either way).
  Scoring: `M88K_BUSERR_RESULT=<ok>/31`, `_CONTROL=OK|FAIL`, `_SYMPTOM=PRESENT n/10 | ABSENT | MIXED` over the ten
  symptom rows, `_RED=<names>`, sentinel `M88K_BUSERR_PROBE_DONE`, non-zero exit on any red.  The CONTRACT names what
  is NOT CLAIMED: PFAR's low two bits (sub-word accesses), a translated session (VA != PA -- a programmed BATC could
  separate them; `vaddr` is not an operand the arm reads), a LUNA store (direction is pinned by `ust`), a STEPPED
  instruction fetch at `0x3ffffff0` (HEAD's case wrote `cmmu[1]`'s PFSR for any access class and served it; the fix
  deletes that write; the cell is LUNA dispatch x instruction label, clause (e)), the unclaimed-address path, luna
  `-n 2..4`, `xmem`, the 88110 machines, a free-running instruction-fetch refusal (`m88kifetchhalt`), the DELIVERY of
  the instruction label's exception on a CMMU-less cpu (`null route` scores the DATA label's delivery; `null surv`
  scores survival only -- the two-cpu session's INFO line prints cpu 1's end pc, unscored), and the PRESERVATION OF
  ANOTHER CPU'S CMMU REGISTERS during a CMMU-less cpu's fault (a `null owner` row is filed in `m88kbuserrdebt`, not
  rowed here -- DeepSeek's pass-2 "CMMU-owner confusion" breach claim, rejected under the DEPENDS-ON bound: the guarded
  body distinguishes NULL from non-NULL and instruction from other, never the owner).  Under a GLOBAL widening of the
  arm (L18/L19) the served rows `ok route` / `ok regs` red through their PREREQUISITE strings (`prereq:nodev`,
  `prereq:readback`) -- the only channel reachable, because the probe's own seed stores and IDR loads are served CMMU
  accesses that fault first; the header disclosed those channels from revision 2.
* `regress/gate_arm.sh` (+31) -- the `#570` block directly after `#568`'s (so after `arm_flags_probe.py`'s skip chain, which
  the block's comment discloses: an earlier `gate_skip` prevents this block from running, and a downstream pin cannot
  prove execution): the probe run with `|| true`; the sentinel exactly once; rows run == 31 and rows correct == 31 by
  LITERAL equality; `CONTROL=OK` and `SYMPTOM=ABSENT` once each; every one of the 31 row identities held in the gate and
  counted exactly once as an `ok` line (`#568`'s anchored `count "$LOG" "^$v  .*ok$"` form -- the names carry spaces);
  no `check_min`.
* `tools/pipeline/check_probe_wiring.py` (+11) -- `CLASS_DETECTOR` for `m88k_buserr_probe.py` (gate 14, pinned at 31) and
  `CLASS_WITNESS` for `artifacts/m88kbuserrregs/witness_20261023/m88k_buserr_probe.py` (the directory's only `.py`; the
  builder's helpers are `*.py.txt`).

**Measured** (`regress/artifacts/m88kbuserrregs/table1_20261023/`; every score against its instrument revision and
denominator -- detector rev 2 frozen before any table, md5 `d57c12ab`, N = 31; witness rev 1, N = 24).  Pre-fix on the
HEAD binary `21/31`, `SYMPTOM=PRESENT 10/10`, the ten predicted reds (`prefix_HEAD.out`; the frozen detector's mtime
precedes every edit); fixed `31/31 ABSENT` (`fixed.out`); the frozen witness on the fixed binary `24/24 ABSENT`
(`fixed_witness24.out`, witness clause (i)).  Floor: (b) the arm reinstated verbatim with the LUNA case fixed `21/31`
and `16/24` (`L3_*`), the case reinstated with the arm fixed `29/31` and `22/24` (`L4_*`); (c) measured at `L5_stub.out`
-- an exit-1 non-emulator in the binary's place scores `1/31` (`neg apparatus` passes by design), `CONTROL=FAIL`,
`SYMPTOM=MIXED`, exit 1 -- and `L5b_absent.out` (binary absent: `FileNotFoundError`, no rows, no sentinel; the gate's
sentinel pin is what reds); (d) the selector weakened to always-data `28/31` (L6: `ifetch pfsr`/`pfar`), always-
instruction `19/31` (L6b), the `!no_exceptions` conjunct dropped `30/31` (L7: `dbg noexc`), the NULL check removed
`29/31` (L8: `null surv` dies, `null route`), the NULL check conditioned on the data label only `30/31` (L8b: `null surv`
dies on cpu 1's instruction fetch -- the instruction x NULL joint cell), the exception moved inside the NULL check
`30/31` (L9: `null route` FELL); the named variants: raw 3 `26/31` (L10), device-relative `paddr` in PFAR `26/31`
(L11), PFSR only `26/31` (L12), both CMMUs `26/31` (L13), sibling cleared `26/31` (L14), read-only `29/31` (L15),
excluding the VME device `29/31` (L16), the exception dropped `22/31` (L17), the writes before the outer guard `6/31`
(L18 -- the probe's own seed readbacks fail first, as predicted), `res <= 1` `4/31` (L19), the LUNA write deleted with
the case still returning 1 `28/31` (L21), the LUNA case deleted `27/31` (L22); L20 = L4 (HEAD's case verbatim IS
"returning 1 with its write"), not run.  **27 measurements, 27 MATCH their `PRETABLE.out` prediction** (written
22:28, before any table), each leg's red set equal to the predicted set (`SCORES.txt`) -- L22's prediction lives at
`BUILDER_QUESTIONS.md` Q18 / `BUILD_SPEC.md` section 11 Q18 (22:29 / 22:31, before the 23:08 leg), which
`SCORES.txt`'s criterion line now names; `table1_20261023/PRETABLE_NOTE_20261024.md` records that provenance, the
PRETABLE's draft-to-final question-id map, AMENDMENT 1's self-stated time against the file's mtime, and two sentences of
the PRETABLE superseded by the probe as built (its `R-d` "pauses cpu 0 before cpu 1 runs" -- cpu 0 parks in its
handler's `br .` self-loop and stays running, the probe sends `pause 1` and never `pause 0`; its CL7 mapping of "still
takes the exception" to `null route` establishes DATA delivery only).  `SCORES.txt`'s SYMPTOM column is cut at 60
characters (a note in the file points at the leg `.out` files, which carry the full line).  The two-part clearance is
CLEAN and FRESH on `build/`, `build-asan/`, `/tmp/gxsec-build` and the work clone, `est/` a source tree (part 2 N/A),
re-run after the gates unchanged (`CLEARANCE.out`, `CLEARANCE_final.out`); `build/`'s five peer-edited files are
md5-identical before and after.  GATE 14 `REGRESS_PASS`, 1310 checks, 0 FAIL -- the `#570` block 31/31 and `#568`'s
`vme_default` pin 38/38 unchanged (`gates/gate14_run.out`; it ran alone as a harness-tracked background job of 7974 s
because the gate exceeds the foreground cap); GATE 11 `REGRESS_PASS`, 111 checks (`gates/gate11_run.out`); no committed
probe or gate references `0x3ffffff0` (`gates/grep3ffffff0.out`).  The LUNA change is guest-visible, so the luna rig
image was booted to `login:` with the base and the fixed binary (`boot_ab/`): both reach it (7,651,336,103 and
7,550,665,157 instructions; the consoles differ only in the overlay name, the loader spinner, one line break and the
date).

**Panel.**  Pass 1 (`pass1_20261023/`): GPT-6 Astra (ultra, file-reading), Grok 4.7 (xhigh, plan mode), GLM 5.3 and
DeepSeek v4-pro (packet-fed, Q1-2 / Q3-4 firings) -- all READY WITH CHANGES; the changes: the `m8820x.h` include
(unanimous), and the three floor cells beyond the witness.  Adjudicated by GPT-6 Astra (`adj/codex_t36p1adj.txt`):
VERDICT AMEND -- the repair retained; the NULL-CMMU cell is REACHABLE on an unmodified machine (the debugger's `pause`
command starts a CMMU-less cpu on mvme187 `-n 2`, `debugger_cmds.c:1302`) and therefore floor, against three seats'
"unreachable"; the instruction x NULL JOINT cell owed (closed conjunctively by the two-cpu session); `ifetch route` vacuous
against the always-data selector (the vector expression reads `cache` independently) and kept as an attribution row;
the main loop's C5 (an accessing-cpu NULL dereference in `dev_m8820x.c:108`) REJECTED -- `m8820x_command()` receives the
OWNING cpu (`:250`, `:284`) -- and then MEASURED absent by the builder (`explore_20261023/`, E3); GLM's "RED for an
unrelated reason when `m88kstepprefetch` is fixed" upheld over Grok's "GREEN"; the boot A/B ordered before the kill
table.  The builder's 22 questions are ruled in `BUILD_SPEC.md` section 11 (the stepped two-cpu session; ERROR/vector 10
accepted; N = 31; L6b/L8b/L22 added).  Pass 2 on the diff (`pass2_20261023/`): GPT-6 Astra, Grok 4.7 and GLM 5.3 (two firings) SHIP WITH CHANGES; DeepSeek Q1-2 DO NOT SHIP on one claimed clause-(d) breach ("CMMU-owner confusion" -- a fallback to the bootstrap cpu's CMMU when the faulting cpu has none), Q3-4 SHIP WITH CHANGES; Gemini 4 Argon -- back on the roster the same night (the account fixed; `agy models` lists `gemini-4-argon-high`, so it read the tree through agy) -- SHIP WITH CHANGES.  No seat found an executable defect; every change is a comment, a docstring, gate prose or a record.  The F2 adjudication (`f2/codex_t36f2.txt`, GPT-6 Astra on five reviewing seats): VERDICT AMEND -- the repair and the bounded floor upheld, no L2 breach; DeepSeek's breach REJECTED under the DEPENDS-ON bound and the joint-cell rule (the guarded body distinguishes NULL from non-NULL and instruction from other, never the owner; E excludes cpu-number products) and FILED as clause-(e) debt (`m88kbuserrdebt`), with "preservation of another cpu's CMMU registers is not scored" written into the contract; GLM's errata-only position on the frozen detector header overruled in favour of ONE documentation-only re-freeze (revision 2b, both identities recorded, the runtime unchanged), and its "wrong channel names" diagnosis rejected (the prerequisite channels were already explicit in the header); Argon's P10 mechanism ("the real fetch passes NO_EXCEPTIONS") refuted on `cpu_m88k_instr.c:2989-2990`, its pre-fix red list, L6b score and L5 description excluded from every record, its two extra shifted citations adopted and an eighth found by Astra; the gate comment's two missing qualifiers upheld against Argon's "acceptable"; Astra withdrew its own five-citation census and its "record Argon NOT FIRED" instruction.  The pre-commit repair (`repair1_20261024/`, by the Opus builder): the five product-comment corrections with line counts kept and `dev_m8820x.o` re-measured identical, the docstring-only revision 2b of the shipped detector rerun on both binaries and compared row by row with the measured runs, the gate comment's qualifiers in the live and staged gate identically, the staged gate copy renamed to `.sh.txt`, the dated `PRETABLE_NOTE_20261024.md` and the `SCORES.txt` criterion/truncation lines, propagation to est/ and the three build trees with the two-part clearance re-run; no further leg, boot or gate was required.  Fable 5.1 HELD by the owner on both passes (the hold
question is on the ledger row); Gemini 4 Argon NOT FIRED on pass 1 (its transport had failed four controls on
2026-10-23 -- a seat failure, not agreement) and FIRED on pass 2 through agy (file-reading; `argon_transport_20261024.txt`);
kimi, minimax and Opus-as-seat DELIBERATELY NOT FIRED under the owner's 2026-10-23/24 roster (Opus 5.5 built and
measured the round; agy fired only as Argon's transport -- one Gemini-family lens).

**What the records claim, and do not.**  `#570` records metadata for CLAIMED, REFUSED, unsuppressed device accesses that
pass the running-transition check, on the two MC88200 machines, and routes LUNA's probe case into that path.  It does
NOT claim: an unclaimed physical address (still served zeros / dropped, no exception, no CMMU write -- `m88kunclaimedberr`);
luna-88k's other device refusals (they still stop the cpu before the arm); a free-running instruction-fetch refusal
(`m88kifetchhalt` halts the faulting cpu before any handler runs); NO_EXCEPTIONS callers; the translation-fault PFSR/PFAR
semantics of `memory_m88k.c` (unchanged); PFAR's low two bits; the sibling CMMU's hardware latch semantics ("no guest can
observe the sibling" is NOT claimed -- the detector pins it `kept` as the ruling's premise); CMMU-less machines (unchanged).

**Filed** (ledger rows, all source-derived unless stated): `m88kifetchhalt` (MED -- a refused m88k instruction fetch takes
vector 2 and the dyntrans `bad:` tail stops the FAULTING cpu and requests the debugger before the handler runs; the
witness measured it on a one-cpu machine), `m88kstepprefetch` (LOW -- the step loop's disassembly pre-read fetches
without NO_EXCEPTIONS, so the debugger raises the guest's instruction-access exception; this round's four `ifetch` rows
and the null session's instruction cell ride it, disclosed), `m88kunclaimedberr` (LOW, research -- whether real MVME187 /
LUNA hardware asserts BERR* on an unclaimed address is a board question; the only lead is `vmesbcp2.txt`'s contents
list), `mvme187cmmuowner` (LOW -- MVME187 attaches its CMMUs to `cpus[bootstrap_cpu]` but registers their windows with
`addr2=0/1`, so with the random-bootstrap option selecting a NONZERO bootstrap cpu the register decoder dereferences
`cpus[0]`'s NULL pointer; Astra's finding, conditional, unmeasured), `m88kcitedrift570` (LOW -- EIGHT line citations
into `cpu_m88k.c` and `dev_luna88k.c` in tracked regress files shifted by this round's +4 lines in each file, plus
`repro_m8sarpurge.c:14` naming the LUNA PFSR writer this round removed; filed, not swept -- two are gate-run probes
whose md5s the gate logs print, and several were already stale), `m88kbuserrdebt` (LOW -- the detector's clause-(e)
cells, listed in the contract above).  C5 was filed by the main loop and WITHDRAWN in adjudication (not a defect: a
reading error, the function boundary unread; the builder then measured its absence, `explore_20261023/` E3).  This
round's own diff also shifted a citation inside a file it edits -- `dev_m8820x.c:361`'s `cpu_m88k.c:354-355` -> `:358-359`
-- corrected in the pre-commit repair.

**Pre-commit repair** (`repair1_20261024/`, after pass 2 and its adjudication; comment, docstring and record work only;
no leg, boot or gate re-run was required).  In the diff: `dev_m8820x.c:361`'s shifted citation; `memory_rw.c`'s
"NO_EXCEPTIONS callers (the debugger)" -> "(e.g. the debugger's dump)" (the debugger's STEP pre-read is unsuppressed and
is this round's own `ifetch` channel; `dev_luna88k.c:613-614` is a non-debugger suppressed caller); `dev_m8820x.c`'s
"~10^5 times per boot" scoped to the translation-fault writer it was measured on (the arm's count is unmeasured) and
"the model writes only PFSR and PFAR" narrowed to the model's FAULT PATHS (IDR is initialised at `dev_mvme187.c:139,151`
/ `dev_luna88k.c:953,964`); `memory_rw.c`'s CMMU-less sentence narrowed to what is scored (above).  Every product edit
kept its file's line count (`FAILURE()` embeds `__LINE__` at `dev_m8820x.c:537`; the hunks are equal-range, lines were
widened rather than words dropped -- `memory_rw.c`'s comment reaches 97 columns against the file's 107); every one of
the 224 objects and the binary re-measured BYTE-IDENTICAL (`dev_m8820x.o`, `cpu_m88k.o`, `dev_luna88k.o`, `gxemul` --
`repair1_20261024/objmd5_before.txt` / `_after.txt`); est/ mirrored; the three build trees re-propagated with their
binaries unchanged (`931e69fa`, `9d0e0680`, `8d882c05`) and the two-part clearance re-run (`CLEARANCE_repair1.out`), so
the gate receipts were run on the binary the shipped sources produce.  The builder also carried the gate comment's two
qualifiers into the probe's title sentence and the MANIFEST comment (the same unqualified claim, the grep-for-siblings
rule).  The shipped
detector's documentation revision 2c (above); the gate comment's opening sentence qualified -- a CLAIMED, REFUSED,
UNSUPPRESSED access that passes the running-transition check records its bus error WHEN THE SELECTED CMMU EXISTS -- in
the live and the staged gate identically (gate 14's run used the pre-edit file, md5 `5ee94e61`; a dated
`gates/PROVENANCE_20261024.md` says so; the raw receipt is not relabelled); the staged gate copy renamed `.sh.txt`; the
MANIFEST text names both probe identities and L22's prediction provenance.

**Records.**  The ledger row's witness is `probe:regress/artifacts/m88kbuserrregs/witness_20261023/m88k_buserr_probe.py`
(rung 3, RED on HEAD, the same frozen script GREEN post-fix; it implies no instruction-fetch or boot coverage); its state
is `held` for Fable 5.1 with the hold question; its landing commit is named in the follow-up records commit.  Six
departures from the build spec are recorded by the builder (`BUILD_REPORT.md` section 6) and accepted: the include's
position is this tree's, not upstream's (the comment claims only that upstream adds the same include); the staged
checker copy is `check_probe_wiring.py.txt`; the harness insertions were made after propagation rather than before the
pre-fix run (the staged and working-tree insertions are measured identical; gate 14 never ran the block pre-fix -- clause
(a) is measured at the probe, and the gate's literal pins would red that receipt by inspection, not by a run); gate 14
ran as a tracked background job (alone, private `LOGDIR`, 7974 s); the unfrozen detector was smoke-run once on the HEAD
binary before the freeze (identical rows to the official pre-fix run); `dev_m8820x.c`'s comments were rewrapped to keep
the line count.  The landing commits the HEAD-based staged `check_probe_wiring.py.txt` (this round's two MANIFEST
entries only; the peer's uncommitted lines are restored to the working tree afterwards) and never the peer's files.

```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?

End with one line: `RECBLOCK_570: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC570: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
