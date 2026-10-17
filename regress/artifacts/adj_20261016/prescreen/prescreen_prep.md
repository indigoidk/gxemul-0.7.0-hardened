# Prescreen -- future-round prep group (the 2026-10-13 agy pack, re-read by grok, grok-reconcile and Gemini Argon)

PRESCREEN_PREP_20261016.  Prepared 2026-10-16 for the adj_20261016 adjudicators.  It sorts the seats' findings into one
short table per job.  It re-grades nothing already ruled.  Agreement between seats counts for nothing.

**Jobs (14):** armvecrecurse_prep, armmmuvehicle_prep, armthumbabortkill_prep, armdesc3kill_prep, armexits_db8b1a33,
excvecrecurse_prep, arcbios_three, ascwidecount_prep, crimectllane_prep, mb89352_five, m88k_four, ppc_six, sh_two,
mips_two.

**Mode.**  READ-ONLY.  Nothing was built, and no test, probe, gate or project tool was run.  Every check is a
`git show e483d931:<path>` (line numbers by `grep -n` or `awk NR`), a `git grep` at e483d931, a read of an untracked
artifact or a `_scratchpad/*.txt` manual, or a `python` JSON read of `git show e483d931:tools/pipeline/ledger.json`.
**This is the only file written.**  Never read: the working tree's `src/` and `tools/` (they carry uncommitted edits), and
the project root's pristine `src/`.  (Disclosure: two `grep.exe.stackdump` crash files from a crashed MSYS `grep`
appeared while this task's read-only sub-agents were running, at 11:32:54 in `regress/artifacts/agypack_20261013/` and
at 11:35:28 at the repo root.  Both are git-ignored (`.gitignore:5` `*.stackdump`).  They were left in place: their
writer is not certain, because other sessions share the tree.)  **Tree:** `GXEMUL-SEC` HEAD `e483d931` (`git rev-parse HEAD` = e483d93119da...,
checked 2026-10-16).

**Who did the reading.**  Eight jobs were read and checked by this prescreen directly: crimectllane_prep, sh_two,
mips_two, m88k_four, ppc_six, mb89352_five, ascwidecount_prep and arcbios_three.  The other six went to five read-only
sub-agents given these same rules: armvecrecurse_prep together with excvecrecurse_prep, armmmuvehicle_prep,
armthumbabortkill_prep, armdesc3kill_prep and armexits_db8b1a33.  Some sub-agent rows were spot-checked here; each one
checked is marked **[spot-checked]**.

**Files read, per job.**
- `regress/artifacts/agypack_20261013/briefs/<id>.md`;
- `.../agypack_20261013/<id>/grok_<id>.txt` (+ `.err`);
- `grok_reconcile_<id>.txt` where it exists: armmmuvehicle, armthumbabortkill, armdesc3kill, armexits;
- `_scratchpad/gweb/jobs_20261014_argonpack6/<id>/gemini_web.out` + `argon_bundle.manifest`, for the first seven ids.
  **Argon is NOT YET banked** for ascwidecount_prep, crimectllane_prep, mb89352_five, m88k_four, ppc_six, sh_two and
  mips_two: their dirs hold a packet and no `gemini_web.out`.
- Dispositions: `agypack_20261013/HARVEST.md`, `HARVEST_AUTO.md` (agy's FLAG lines, for provenance only), and
  `recordfix_20261013/adj_20261013/fable5_records_adjudication.md`, sections 1 (:21-68), 6 (:150-162) and v2.6
  (:266-276).
- Evidence as cited: e483d931 `src/`, `regress/`, `OUTSTANDING_BUGS.md`, `CHANGELOG.md`, `tools/pipeline/ledger.json`;
  untracked artifacts under `regress/artifacts/`; and `_scratchpad/{ddi0100i,ddi0406,mc88100,mips32_volII,mips_r4000,
  ppc_pem32_rev2_2001,ppc_uisa_book1_v201,sh7750_hardware}.txt`.

**agy's harvest.**  agy answered only four of these jobs:
- armmmuvehicle_prep: 27 flags.  Records adjudication §1 verified 4 of them; the other 23 were NOT adjudicated.
- armthumbabortkill_prep: 6 flags.  §1 and §6 cover F1; v2.6 corrects F2.
- armdesc3kill_prep: 4 flags.  No disposition.
- armexits_db8b1a33: 9 flags.  No disposition.

The rest got no agy findings: armvecrecurse, excvecrecurse and arcbios were walled (`RESOURCE_EXHAUSTED`, 0-byte
answer), and the last seven never landed.  So **DISPOSED is possible only on armmmuvehicle, armthumbabortkill and
armdesc3kill** (the last through v2.6:267).  `(=agy)` in a seats cell marks provenance only.

**grok auto-compacted mid-answer** on ten of these jobs: armvecrecurse, armmmuvehicle, armthumbabortkill, armexits,
ascwidecount, mb89352_five, m88k_four, ppc_six, sh_two and mips_two.  The tell is a 67-byte `grok_<id>.err` reading
`Auto-compacting conversation (81% full)... Conversation compacted.`  Treat their early facts as summaries.  Every row
below was checked against the file, not against the seat.

**Seats.**
- `grok` = grok-4.7 xhigh, its first answer.
- `grok-rec` = grok's reconcile run of agy vs grok.
- `Argon` = Gemini 4 Argon, packet-fed.  Its flags of the form "X not in the bundle, so UNSETTLED" are about the
  PACKET.  They get one row per job and become no round action.
- **Categories:** DISPOSED / CONFIRMED / REFUTED / CANNOT SETTLE, each with `· READ` (the evidence was opened) or
  `· REASONED` (the inference goes beyond what was opened).
- **Disposition words:**
  - FILE: a new row.  The ledger and OUTSTANDING_BUGS were grepped first.
  - ADD TO <row>: the finding extends an existing row.
  - already filed / ALREADY-FILED: no new action.
  - RECORD CORRECTION: an L4 fix to a record.
  - agy flag wrong (AGY-FLAG-WRONG): one of agy's undisposed harvested flags is refuted.
  - BRIEF PREMISE: a fact the future round's brief must state.
  - PACKET: Argon transport only.
  - none.
- Unprefixed paths are tracked files at e483d931.  `disk:` marks an untracked artifact.

---

## armvecrecurse_prep

Seats: grok 19,676 b (auto-compacted) · grok-rec none · Argon 25,939 b · agy walled.  Sub-agent read.  **[spot-checked]**:
- F2: 220,005 = 200,000 + 5 + 20,000 (`meas3.py.txt:121`), and the excerpt's line 1 calls T3 "The full transcript".
- F3: T3 holds 997 fault lines, 995 warnings and 996 PREFETCH ABORT.
- F4: `meas3.py.txt:83`, `:104-108`.
- F12: `src/cpus/memory_mips.c:122` includes `memory_mips_v2p.c`, whose `:452` calls `mips_cpu_exception`.

Abbreviations: `M/` = `regress/artifacts/armmmuvehicle/pass1_20261009/opus5/opus5_meas/`; `P/` =
`regress/artifacts/armmmuvehicle/pass1_20261009/`.  Both are tracked since 200671b6.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok | the meas3 artifacts were committed in 200671b6; they are not untracked, as the brief said | CONFIRMED · READ | `git show --stat 200671b6`; `git cat-file -e e483d931:` finds all four tracked; the disk md5 equals the blob md5 | BRIEF PREMISE: read them with `git show e483d931:` |
| F2 | Argon (grok contra) | T3_vec_unmapped.txt is the full 3,120-line transcript, so the row's "head-and-tail excerpt" is false | REFUTED · READ | `M/meas3.py.txt:121` writes `txt[:200000] + "\n...\n" + txt[-20000:]`; `M/T3_vec_unmapped.txt:2843` is that `...`; blob 220,005 b | the row stands.  RECORD CORRECTION at `M/T3_vec_unmapped.excerpt.txt:1`, whose header mislabels its parent: "meas3's 220,005-byte head+tail excerpt; the 10.47 MB transcript was never kept" |
| F3 | grok, Argon | 47,591 counts only `{ arm memory fault` lines, and that includes the initiating data abort.  The mode warnings are not counted, and the first abort (SVC32->ABT32) does not warn | CONFIRMED · READ | `M/meas3.py.txt:122`; `M/meas3_base.out:39`; `src/cpus/cpu_arm.c:758`; the T3 excerpt has 997 fault lines and 995 warnings | RECORD CORRECTION at `ledger.json:62375-62376`, `OUTSTANDING_BUGS.md:24623-24624`: "47,591 fault lines: 1 data abort + 47,590 nested; warnings uncounted" |
| F4 | grok | "in 10.6 s" is the driver's whole part-2 wall time, not the length of the storm | CONFIRMED · READ | `M/meas3.py.txt:83` (t0) before `:104-107` (46 puts at 0.1 s, 5 register sets at 0.3 s, `rd(1.6)`: at least 7.7 s of setup) | RECORD CORRECTION, same sites: "10.6 s = the whole driver run (>=7.7 s setup); storm <=2.9 s" |
| F5 | grok | 10,473,809 b and 47,591 cannot be recounted: the transcript was never kept, and `meas3_base.out` ("the run log") is a 2,267-b driver summary | CONFIRMED · READ | `M/meas3.py.txt:121-125`; `git cat-file -s`: meas3_base.out 2,267, T3 220,005 | RECORD CORRECTION at `ledger.json:62376`: "meas3_base.out = driver summary; the 10.47 MB transcript was not kept" |
| F6 | grok | the run was `-V -A -E testarm -M 64 0x8000:STUB`, driven by debugger `put w` + `step 9`, not a bare `-E testarm` | CONFIRMED · READ | `M/meas3.py.txt:76-80` | BRIEF PREMISE: a rung-3 cold-debugger session on unmodified testarm; quote the command line |
| F7 | grok | "does not map the vector page" is not enough on its own: a warm phys_page/host_load serves the vector, and MMU-off or NOEXCEPTIONS raises nothing | CONFIRMED · READ | `src/cpus/cpu_dyntrans.c:659-662`, `:867-869`; `src/cpus/memory_arm.c:57-59`, `:258-259`; `P/opus5/opus5_pass1.md:57-60`; `M/meas3.py.txt:34` (c8 `0xEE080F17`) | BRIEF PREMISE: the recursion needs a cold vector page (c8 after planting); put that condition in the title |
| F8 | grok | "takes any abort ... ends the host" fails for RESET, FIQ, ARM_CONTROL_V, DACR 2 and L1 type 3 | REFUTED · READ | RESET and FIQ are not aborts; RESET, DACR 2 and type 3 `exit(1)` (`cpu_arm.c:708-711`; `memory_arm.c:78-79`, `:252-254`), so the host still ends; V only moves the vector page (`cpu_arm.c:781-782`) | none.  Brief note: with DACR 2 or type 3 the host ends by exit(1) (armdacr2kill, armdesc3kill), not by recursion |
| F9 | grok, Argon | the mechanism and "the exit never appears" sentences carry no path:line; `arm_exception(PREF_ABT)` is shorthand for `ARM_EXCEPTION_PREF_ABT` | CONFIRMED · READ | `ledger.json:62376`; `OUTSTANDING_BUGS.md:24624-24626` | BRIEF PREMISE: cite `cpu_arm.c:780-783` -> `quick_pc_to_pointers.h:29` -> `cpu_dyntrans.c:867-888`, `:679-680` -> `memory_arm.c:268-269`; the exit is `cpu_dyntrans.c:729-732` |
| F10 | grok; Argon (UNSETTLED) | `arm_exception`'s `quick_pc_to_pointers` is the non-MODE32 macro (h:29 -> `arm_pc_to_pointers`); the inline phys_page form serves only `cpu_arm_instr.c` | CONFIRMED · READ | `src/include/quick_pc_to_pointers.h:5`, `:29`; `cpu_arm.c:82`; `src/cpus/tmp_arm_tail.c:8`, `:62-63`; `src/cpus/tmp_arm_head.c:30` | BRIEF PREMISE (= excvec F4) |
| F11 | Argon (grok contra) | the generic lookup's second chance assumes translate_v2p only sets the PC, and ARM "violates" that by nesting pc_to_pointers | REFUTED · READ | every exception-delivering CPU nests the same way: `src/cpus/cpu_ppc.c:341-344`, `cpu_mips.c:2219-2223`, `cpu_sh.c:1088`, `cpu_m88k.c:980` | BRIEF PREMISE: the defect is a vector fetch that faults again inside the nested call; nesting itself is normal |
| F12 | grok | MIPS sibling: `memory_mips.c` never calls `mips_cpu_exception`, so a fetch miss dies at `cpu_dyntrans.c:732` | REFUTED · READ **[spot-checked]** | `src/cpus/memory_mips.c:122` `#include "memory_mips_v2p.c"`; `memory_mips_v2p.c:452-456` | none (MIPS nests one level and cannot recurse: kseg0/1 vectors, `cpu_mips.c:2165-2168`; grok's excvec answer has this right) |
| F13 | grok; Argon (UNSETTLED) | siblings: PPC has the same re-entry (unmeasured); M88K the same via SFRZ->ERROR; Alpha raises nothing and exits at :732; RISC-V/i960 exception functions are uncalled TODOs | CONFIRMED · READ | `src/cpus/memory_ppc.c:313`, `:322-326`; `cpu_ppc.c:335-344`; `cpu_m88k.c:811-818`, `:863`, `:980`; `memory_m88k.c:417-419`; `memory_alpha.c:197-198` | ADD TO excvecrecurse (its PPC and M88K legs); Alpha is already filed: alphaifetchkill |
| F14 | grok; Argon (UNSETTLED) | no top-level regress probe or gate reaches the recursion; the ARM exception probes are `arm_flags_probe.py` (UND) and `xscale_inten_probe.py` (IRQ 0x18); the only driver is `M/meas3.py.txt` | CONFIRMED · READ | `regress/arm_flags_probe.py:78`; `regress/xscale_inten_probe.py:576`; `git grep -l ee010f10\|'enabling the MMU'\|ARM_CONTROL_MMU -- regress/*.py regress/gate_*.sh`: rc 1 | BRIEF PREMISE: no detector exists; the vehicle is armmmuvehicle |
| F15 | grok | "the queue's HIGH item after the two rounds in flight" is the brief's framing, not the row's; the owner's order is wdc473floor -> asiceventaddr -> armmmuvehicle | CONFIRMED · READ | `ledger.json:62366`; `OUTSTANDING_BUGS.md:24616`; `ledger.json:52069-52072` (excvecrecurse HIGH, open since 09-19) | BRIEF PREMISE: armvecrecurse rides on armmmuvehicle; the older row excvecrecurse covers the same ARM defect |
| F16 | grok | the title's "SIGSEGV" is unsupported; the artifact records only signal(11) | REFUTED · REASONED | `M/meas3_base.out:36` `status=signal(11)` (11 is SIGSEGV on Linux) | none (stack exhaustion as the cause is still inferred: excvec F11) |
| F17 | Argon | `P/PASS1_brief_20261009.md:77-78` ("byte/halfword put ... NO_EXCEPTIONS") is wrong: `put h` takes a data abort | CONFIRMED · READ | `M/T2_put_after_m2.txt:170-173`; `P/fable5/fable5_pass1.md:26`; `ledger.json:62335` | already recorded on armmmuvehicle (`ledger.json:62335`); not this row |
| F18 | Argon | the abort LR (+8/+4) in `P/PASS1_brief_20261009.md:76` holds only in ARM state; Thumb gives +7/+3 | CONFIRMED · READ | `cpu_arm.c:712-717`; `OUTSTANDING_BUGS.md:24651-24658` | already filed: armthumbabtlr (`ledger.json:62400`) |
| F19 | Argon | bundle-gap flags (6): meas3_base.out + opus5_pass1.md, quick_pc_to_pointers.h, cpu_arm.h/armreg.h/tmp_arm_*.c, sibling cpu_*.c, sibling memory_*.c + memory_rw.c, regress/*.py | CONFIRMED · READ | disk:`_scratchpad/gweb/jobs_20261014_argonpack6/armvecrecurse_prep/argon_bundle.manifest` ("DIR SKIPPED src/cpus", "NOT FOUND regress/*.py") | PACKET only.  Settled at F3-F5, F10, F12-F13, F14 |

Counts (armvecrecurse_prep): DISPOSED 0 · CONFIRMED 14 (ADD-TO-ROW 1, ALREADY-FILED/RECORDED 2, RECORD 3, BRIEF 7,
PACKET 1) · REFUTED 5 · CANNOT SETTLE 0 · total 19.

## armmmuvehicle_prep

Seats: grok 24,827 b (auto-compacted) · grok-rec 13,769 b · Argon 32,384 b · agy answered 27 flags (records-adj §1
verified 4; the other 23 were NOT adjudicated, and several are refuted below).  Sub-agent read.  **[spot-checked]**:
- F6: `OUTSTANDING_BUGS.md:24523-24524`.
- F16: `regress/pit8253_latch_probe.py:11-16`.
- F19: `src/cpus/memory_arm.c:161-176`.  The coarse `dav == 0` domain test precedes the L2 fetch.
- F24: `machine.c:62` `machine_new`, `:85`; `git grep machine_create`: 0.
- F30: `ledger.json:48116` carries `:1808` with no shift note; `:48071` carries both.  `P/` = `regress/artifacts/armmmuvehicle/pass1_20261009/`
(tracked).  `A/` = `regress/artifacts/agypack_20261013/`.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok, Argon (=agy) | `src/cpus/cpu_arm_memory.c` does not exist; the walk is `memory_arm.c` (278 lines) | DISPOSED · READ | disk:`fable5_records_adjudication.md:64` | none |
| F2 | grok, Argon (=agy) | `machine_test.c` defines only barearm and testarm; cats is `machine_cats.c` (SA110) | DISPOSED · READ | disk:`fable5_records_adjudication.md:64`; `src/machines/machine_test.c:172-231`; `machine_cats.c:135-137` | none (the extension is F7) |
| F3 | grok, grok-rec (=agy) | `-A` turns colorized output off; it is not "raw mode" | DISPOSED · READ | disk:`fable5_records_adjudication.md:64`; `src/core/main.c:317-318` | none (agy's line cites are wrong: F11) |
| F4 | Argon (=agy) | agy's "wfi" is `X(reboot)` (iword 0xef8c64eb); armsa1110areset is the reset ALIGN default | DISPOSED · READ | disk:`fable5_records_adjudication.md:64`; `src/cpus/cpu_arm_instr.c:1002`, `:5031-5033`; `cpu_arm.c:129` | none |
| F5 | Argon | armthumbabortkill's sites moved +50, not +42 | DISPOSED · READ | disk:`fable5_records_adjudication.md:67` | none here (cross-job) |
| F6 | Argon | the row says unmapped vectors end at cpu_dyntrans.c's "could not find physical address" exit (alphaifetchkill); its own pass 1 measured recursion to signal 11 instead | CONFIRMED · READ | `ledger.json:62253`; `OUTSTANDING_BUGS.md:24523-24524` vs `:24624-24626`; `ledger.json:62376` ("appears ZERO times"); `cpu_arm.c:783`; `memory_arm.c:268-269` | RECORD CORRECTION at `ledger.json:62253`, `OUTSTANDING_BUGS.md:24523-24524`: "an abort recurses to host SIGSEGV (armvecrecurse), not the cpu_dyntrans.c exit" |
| F7 | grok, grok-rec, Argon | cats boots with the MMU on: all 4096 L1 entries are planted (PA = VA mod 256 MB) and DACR is ORed with 3, so the boot table cannot fault | CONFIRMED · READ | `src/cpus/cpu_arm.c:231-244`; `machine_cats.c:84-85`, `:131`; `memory_arm.c:80-81` | BRIEF PREMISE |
| F8 | grok, grok-rec | CP15 lives in `cpu_arm_coproc.c` (the brief omits it); a c1 write stores control and swaps translate_v2p on an M change, and invalidates nothing | CONFIRMED · READ | `src/cpus/cpu_arm_coproc.c:134-143` (only c8 invalidates, `:237-242`) | BRIEF PREMISE: c8 after M (Hole 2, `P/PASS1_brief_20261009.md:93-94`) |
| F9 | Argon | Argon's sequence has the c1 write "invalidate translation caches", and so puts c8 before M | REFUTED · READ | `cpu_arm_coproc.c:134-143` has no invalidate call (that file was not in Argon's bundle) | drop; c8 stays after M |
| F10 | grok, grok-rec, Argon | the minimal sequence decodes as claimed: MCR c2 0xEE021F10, MCR c3 0xEE032F10, MRC c1 0xEE110F10, ORR 0xE3800001, MCR c1 0xEE010F10, MCR c8 0xEE080F17 | CONFIRMED · READ | `cpu_arm_instr.c:5012-5015`, `:4499-4524`, `:4611-4613`; `cpu_arm.c:2695-2705`; `src/cpus/cpu_arm_instr_dpi.c:190-191`; `P/fable5/exp.py.txt:113-120` (the same words, run) | BRIEF PREMISE.  Correct grok's ORR cite: `:1234` is `X(dpis_imm_rotc)`, used only with S + a rotate |
| F11 | grok, grok-rec (=agy) | the pass-1 command `gxemul -V -A -E testarm -M 64` has no load argument, so it exits "No filename given"; agy's cites (main.c:560-565, :286-288) are wrong | CONFIRMED · READ | `src/core/main.c:578-584`, `:317-318`; `regress/arm_msrmode_probe.py:284-285`; `P/PASS1_brief_20261009.md:124` | BRIEF PREMISE (already at `ledger.json:62309`).  agy's flag at disk:`A/HARVEST_AUTO.md:182` carries the wrong lines |
| F12 | grok | pass-1 brief §1.7 is stale: `arm_msrmode_probe.py` was committed at 4f908ad5, after the 13:19 panel, and its "ten other probes" importing sh4_pcic_probe are 5 probes + 5 witnesses | CONFIRMED · READ | `P/PASS1_brief_20261009.md:83-87`; `git log --diff-filter=A` 4f908ad5; `regress/sh4_chcr_witness.py:61` | BRIEF PREMISE |
| F13 | grok, grok-rec, Argon (=agy) | `put h`/`w`/`d` go through `store_*bit_word`, which uses CACHE_DATA (exceptions on, translation warmed); only `put b`/`s`/`z` and `dump` use NO_EXCEPTIONS; `put q` is TODO.  agy's d/q and Argon's blanket "put warms" are wrong | CONFIRMED · READ | `src/debugger/debugger_cmds.c:1459-1461`, `:1506-1507`, `:1523`, `:1558`, `:1563-1566`; `src/core/memory.c:782-783`, `:827-828`; `memory_rw.c:744-746` | BRIEF PREMISE (the `put h` part is already at `ledger.json:62326`, `:62335`) |
| F14 | grok, grok-rec, Argon (=agy) | the "hole dump" row cannot pin c8: `dump` walks translate_v2p with NO_EXCEPTIONS and never reads host_load, and entering the debugger also invalidates | CONFIRMED · READ | `debugger_cmds.c:716-717`; `memory_rw.c:248-250`; `src/debugger/debugger.c:791-797` | BRIEF PREMISE (already at `ledger.json:62317`, `:62335`; the host_load reason is new) |
| F15 | grok-rec, grok | agy's "entering the debugger unconditionally invalidates": it returns first while a step-N count remains, and resets only CPUs with a translation cache | CONFIRMED · READ | `debugger.c:781-784`, `:792-796` | agy flag wrong (disk:`A/HARVEST_AUTO.md:179`): note it in the harvest; no row change |
| F16 | grok, grok-rec, Argon | "first ARM probe that runs guest code with the MMU ON" is literally false: 4 committed cats probes run arm T with the boot MMU on; none arms M/TTB/DACR from the guest; agy's "zero probes" is wrong | CONFIRMED · READ | `P/PASS1_brief_20261009.md:33-34`; `regress/pit8253_latch_probe.py:11-16`, `:75-79`; `regress/fbpending_drain_probe.py:217-221`; `regress/fbpending_witness.py:152-158`; `regress/footbridge_sites_probe.py:205-211`; `git grep` of regress/*.py for E3800001/EE021F10/EE032F10/EE080F17: 0 | BRIEF PREMISE: this is the first guest-ARMED MMU vehicle |
| F17 | grok, grok-rec, Argon (=agy) | the pass-1 map puts the L2 table at 0x5000, inside the 16 KB L1 at [0x4000,0x8000) | CONFIRMED · READ | `P/PASS1_brief_20261009.md:130-131` | BRIEF PREMISE (already at `ledger.json:62309`, `:62326`) |
| F18 | grok | the pass-1 rows stay green under three walk edits: delete `domain = 0`; `>> 10` -> `>> 9`/`>> 8`; section mask -> 0x00700000 | CONFIRMED · READ | `memory_arm.c:157`, `:167`, `:244`; `P/PASS1_brief_20261009.md:142-150` | BRIEF PREMISE (already at `ledger.json:62277`-`:62335`) |
| F19 | grok | the coarse-table domain check runs BEFORE the L2 fetch: with DACR 0x1, a domain-3 coarse descriptor gives FSR 0x3b even when the L2 entry is invalid (DDI 0100I: 0x37) | CONFIRMED · READ **[spot-checked]** | `memory_arm.c:161-176`; `_scratchpad/ddi0100i.txt:28866-28879`, `:28924-28925`; `P/opus5/opus5_meas/T_base_pgdomain_dom3.txt:186-187` | FILE: new LOW row (no ledger/OUTSTANDING_BUGS entry) |
| F20 | grok | the CPU type word does encode MMU support: ARM_NO_MMU is set on 6 rows, and nothing reads it | CONFIRMED · READ | `src/include/arm_cpu_types.h:40`, `:60-61`, `:68`, `:70-72`; `cpu_arm.c:178`, `:498`; `memory_arm.c:198` | BRIEF PREMISE (prose at `OUTSTANDING_BUGS.md:3037-3043`; no ledger row) |
| F21 | grok, grok-rec | CP15 is written by guest MCR and by machine setup (cats), never by the debugger; agy's "MCR is the sole mechanism" is wrong | CONFIRMED · READ | `cpu_arm.c:128-137`, `:192-196`, `:231-234`; `cpu_arm_coproc.c:135`, `:191-195`, `:203`; `git grep` control/ttb/dacr in `src/debugger`: 0 | BRIEF PREMISE |
| F22 | grok-rec, Argon | c8's INVALIDATE_ALL helper also clears is_userpage, the valid bit and vaddr_to_tlbindex | CONFIRMED · READ | `cpu_dyntrans.c:1019`, `:1028-1034`, `:1276-1288` | BRIEF PREMISE |
| F23 | grok-rec, grok | agy's memory_arm.c walk line numbers run 9-14 low; its flag that grok_adversarial's `:166-167` contradicts HEAD is false | CONFIRMED · READ | `memory_arm.c:155`, `:157-158`, `:162`, `:166-167`, `:170-174`, `:186`, `:239-250`, `:257` | agy flags wrong (disk:`A/HARVEST_AUTO.md:187`, `:189-192`, `:195`): note them in the harvest |
| F24 | grok-rec, grok | `machine_new` exists and sets prom_emulation = 1; there is no `machine_create`, so agy's "correction" is wrong | CONFIRMED · READ | `src/machines/machine.c:62`, `:85`; `git grep machine_create e483d931 -- src`: 0 | agy flag wrong (disk:`A/HARVEST_AUTO.md:186`): drop it |
| F25 | grok | this job's brief is wrong twice: the row names no `_scratchpad` panel dir, and the pass-1 artifacts are tracked | CONFIRMED · READ | disk:`A/briefs/armmmuvehicle_prep.md:7`, `:15-16`; `ledger.json:62260-62334`; `git ls-tree` of `P/` | BRIEF PREMISE: read the pass-1 answers with `git show e483d931:regress/artifacts/armmmuvehicle/pass1_20261009/...` |
| F26 | grok | the pass-1 answers cite memory_arm.c in the pass-1 brief's inline numbering (= file line + 109), plus a stale machine.c:79 and coproc :230 | CONFIRMED · READ | `P/PASS1_brief_20261009.md:243`, `:266`, `:356`; `machine.c:85`; `cpu_arm_coproc.c:237-239` | BRIEF PREMISE: inline code with its file line numbers; leave the frozen answers |
| F27 | grok, Argon (=agy) | pass-1 answers state premises without path:line; kimi.txt (403) and codex.txt/codex_neutral.txt are seat failures, not answers | CONFIRMED · READ | `P/panel_20261009_131958/grok.txt:7-15`; `kimi.txt:2`; `codex.txt:463-464`; `codex_neutral.txt` (0 b); `ledger.json:62301`, `:62309` | BRIEF PREMISE (no round action) |
| F28 | grok, grok-rec | the pass-1 measurements (47,591 faults then signal 11; Fable's 11 sessions) were not re-run at e483d931 | CANNOT SETTLE · READ | `P/opus5/opus5_meas/meas3_base.out`; `P/fable5/S_S*.txt` (11 files) | one run: build e483d931 and re-run `opus5_meas/meas3.py.txt`'s vector-unmapped session |
| F29 | Argon | grok_adversarial's "Thumb LR = pc + 6" conflicts with Fable's measured +7/+3 | REFUTED · READ | `P/grok_adversarial.txt:49` "With bit 0 set that is (instruction_address + 7)" | none |
| F30 | Argon | armthumbabortkill's Hole 9 `:1808 default:` is `:1858` at HEAD | CONFIRMED · READ **[spot-checked]** | `cpu_arm.c:1858-1861`.  `ledger.json:48071` is covered by the queued "+42 -> +50"; the entry note `ledger.json:48116` cites `:1808` with no shift statement | RECORD CORRECTION at `ledger.json:48116` only: "`:1808 default:`" -> "`:1858 default:` (e483d931)" |
| F31 | Argon | bundle-gap flags (6): memory_arm.c, cpu_arm_coproc.c, cpu_arm.h, debugger.c, the regress/*.py grep, the pass-1 panel answers | CONFIRMED · READ | disk:`_scratchpad/gweb/jobs_20261014_argonpack6/armmmuvehicle_prep/argon_bundle.manifest:6`, `:10`, `:15` | PACKET only.  Settled at F18/F19/F23, F8/F21, F13-F15, F16, F26/F27 |

Counts (armmmuvehicle_prep): DISPOSED 5 · CONFIRMED 23 (FILE-new 1, RECORD 2, AGY-FLAG-WRONG 3, BRIEF 16, PACKET 1)
· REFUTED 2 · CANNOT SETTLE 1 · total 31.

## armthumbabortkill_prep

Seats: grok 18,760 b (auto-compacted) · grok-rec 14,112 b · Argon 42,837 b · agy answered 6 flags.  Sub-agent read.
**[spot-checked]**:
- F3: `memory_rw.c:591-592`, `:603-624`.
- F6: `src/cpus/cpu_arm.c:1726-1736`.  After an aborted `arm_pop`, `pc = r[PC]` = the vector, then +2.
- F8: `cpu_arm.c:1604-1605` passes CACHE_INSTRUCTION, and `_scratchpad/ddi0100i.txt:23050-23051` reads "Exceptions /
  Data Abort.".
- F10: `cpu_arm.c:717`; `ddi0100i.txt:2108`, `:2154`.
- F13: `memory_arm.c:69-100`.
- F18: `cpu_arm.h:116-122`.
- F22: `git grep arm_setup_initial_translation_table -- src/machines` gives 5 hits.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok, grok-rec, Argon (=agy) | the ledger's "#562 shifts cpu_arm.c by +42" is +50 (1227/1557/1600/1629/1653 -> 1277/1607/1650/1679/1703; Hole 9's `:1808` -> `:1858`); agy's `:489`/`:62253` are the wrong rows | DISPOSED · READ | disk:`regress/artifacts/recordfix_20261013/adj_20261013/fable5_records_adjudication.md:67`, `:158`; `686d179c:src/cpus/cpu_arm.c:1808` `default:`; `cpu_arm.c:1858` | none beyond the queued `ledger.json:48071` "+42" -> "+50" (it fixes every pre-#562 number in that note).  The entry note at `:48116` still says `:1808` with no shift: armmmuvehicle F30 |
| F2 | Argon | Hole 9's `:1808 default:` is now two stops, `:1807` and `:1860` | REFUTED · READ | `686d179c:cpu_arm.c:1808` is the outer `default:`; its stop `:1810` became HEAD `:1860`; HEAD `:1805-1807` is an `else` arm | none (label `:1858`, stop `:1860`) |
| F3 | grok, grok-rec, Argon | the title's "abort ALREADY DELIVERED" holds only for MMU faults; memory_rw also fails silently when (a) a device returns <= 0, (b) a device clears running, (c) `-T` meets an unimplemented paddr | CONFIRMED · READ | `src/cpus/memory_rw.c:591-592`, `:603-624` (exceptions only under MEM_MIPS/MEM_M88K), `:676-679`; `src/core/memory.c:645-651`; only (a) leaves running=1 | RECORD CORRECTION `ledger.json:48066`: "AFTER the abort is already delivered" -> "after an MMU-fault abort is delivered; a failing device raises none" |
| F4 | grok, grok-rec, Argon | "all seven testarm devices return 1": true; but `dev_mp` PAUSE_CPU and an unimplemented `dev_ether` command clear running (path b), so Argon's "only MMU faults" is wrong | CONFIRMED · READ | `src/machines/machine_test.c:136-168`; `src/devices/dev_mp.c:130-136`, `:254`; `src/devices/dev_ether.c:177-179` | BRIEF PREMISE: path (a) cannot occur on testarm; path (b) can, with the CPU already halted |
| F5 | Argon, grok-rec (vs agy) | the settled member 1 deletes only `running = 0` and keeps five unlatched `fatal()`s; the ARM single-register twin prints nothing, while the ARM ifetch and swp twins do print | CONFIRMED · READ | `src/cpus/cpu_arm_instr_loadstore.c:233-239`, `:367-373`; `src/cpus/cpu_arm_instr.c:4087-4091`, `:1517-1520`; `ledger.json:48071` (Hole 13); `src/core/debugmsg.c:384-391` | BRIEF PREMISE: what happens to the fatal (keep, latch or drop) is OPEN; "match the ARM path" does not decide it |
| F6 | Argon | a Thumb POP without PC (and a PUSH) that takes a data abort ends at pc = vector + 2 (0x12): `arm_pop` returns, then the caller adds 2 | CONFIRMED · READ **[spot-checked]** | `cpu_arm.c:1726-1736`, `:1720-1722` -> `:1864`; `cpu_arm.c:781`; no row in a ledger/OUTSTANDING_BUGS grep | ADD TO armthumbabortkill: the Hole 13 0x12 hazard happens today at PUSH and POP-without-PC |
| F7 | grok-rec, Argon, grok (vs agy) | site `:1277` can be reached through a stale warm dyntrans entry; agy's "never executes" holds only on a cold miss | CONFIRMED · READ | `src/cpus/cpu_dyntrans.c:659-662`, `:867-869`; `memory_rw.c:248`; `ledger.json:48071` | BRIEF PREMISE (already at `:48071`) |
| F8 | grok, grok-rec, Argon (=agy) | Thumb LDR(3) passes CACHE_INSTRUCTION, so it raises a PREFETCH abort with no FAR/FSR; DDI 0100I says Data Abort.  The note's UNVERIFIED candidate is verified by reading | CONFIRMED · READ **[spot-checked]** | `cpu_arm.c:1604-1605`; `memory_rw.c:252`; `src/cpus/memory_arm.c:268-269`; `_scratchpad/ddi0100i.txt:23050-23051`; records-adj §1: "consistent, not re-derived" | FILE: new sibling row (the fix is CACHE_DATA at `:1605`; witness rides on armmmuvehicle).  Then change `:48071`'s "UNVERIFIED" |
| F9 | grok-rec, Argon (=agy) | Thumb aborts save LR_abt = instr+7 (data) / target+3 (prefetch) because cpu->pc carries bit 0 | CONFIRMED · READ | `cpu_arm.c:676`, `:712-717`, `:1266`; `ledger.json:62405-62406` | already filed: armthumbabtlr |
| F10 | Argon | Thumb UND, and the live Thumb SWI at `:1803`, save LR = instr+3 where DDI 0100I gives instr+2; armthumbabtlr calls the T?2:4 term "right" for SWI/UND | CONFIRMED · READ | `cpu_arm.c:676`, `:717`, `:1803`; `_scratchpad/ddi0100i.txt:2108`, `:2154`; `OUTSTANDING_BUGS.md:24656-24657` | ADD TO armthumbabtlr: bit 0 also makes SWI/UND one too high |
| F11 | Argon, grok | nine more Thumb `running = 0` stops are guest-reachable decode halts (ALU ops, MOV Rd,PC, hi-reg ADD/CMP, BLX Rm, BKPT, 0xDE**, BLX bit 0, main opcodes 0x5/0xa/0xc); `:1621` cannot fire | CONFIRMED · READ | `cpu_arm.c:1543-1546`, `:1557-1561`, `:1584-1592`, `:1739-1741`, `:1805-1808`, `:1817-1820`, `:1858-1861`; `ledger.json:48005` | already filed: cpusexitsweep (triage at `:48005`) |
| F12 | Argon | `:1269` ("called when not in THUMB mode") is guest-reachable: an SPSR restore can set T with an even PC | CONFIRMED · REASONED | `cpu_arm_instr.c:1852`; `cpu_arm.c:1266-1269`; `cpu_dyntrans.c:255`; `OUTSTANDING_BUGS.md:24507-24510`; `ledger.json:48005` calls it "an emulator invariant" | ADD TO armspsrthumb: its LDM^ path ends at the `:1269` halt |
| F13 | grok, grok-rec, Argon (agy differs) | at `memory_arm.c:79` (dav==2), deleting the exit falls into `case 3` (full access), and `return 0` gives a PERMISSION fault, not a domain fault; agy's `FAULT_DOMAIN_S` form cannot sit inside `arm_check_access` | CONFIRMED · READ | `memory_arm.c:69-100`, `:78-81`, `:162-164`, `:240-250`, `:257`; `_scratchpad/ddi0100i.txt:28701` "0b10 Reserved ... UNPREDICTABLE" | ADD TO armdacr2kill: a domain fault needs a dav==2 test beside the walker's dav==0 tests |
| F14 | grok, grok-rec, Argon | at `memory_arm.c:254` (type 3), deleting only the exit falls to `exception_return` with fs=2 (terminal exception), not a translation fault | CONFIRMED · READ | `memory_arm.c:125` "int fs = 2", `:252-257`, `:271-273`; `src/include/thirdparty/armreg.h:378` | ADD TO armdesc3kill: DELETE is not FAULT; FAULT sets `fs = FAULT_TRANS_S` as `:158` does |
| F15 | grok, Argon | the `cpu_dyntrans.c:729-733` exit on the fetch path: on ARM the `arm_exception` -> `quick_pc_to_pointers` recursion comes first | CONFIRMED · READ | `cpu_dyntrans.c:679-733`; `cpu_arm.c:783`; `ledger.json:62375-62376`; `:51863` | already filed: armvecrecurse (ARM) / alphaifetchkill (Alpha) |
| F16 | grok-rec, grok, Argon (vs agy) | the `exit(1)` at `cpu_arm_instr.c:72` is compiled out | CONFIRMED · READ | `cpu_arm_instr.c:41` (`/* #define GATHER_BDT_STATISTICS */`), `:44`, `:72` | BRIEF PREMISE: twelve live `exit(` in the four files, plus that dead one |
| F17 | grok-rec, grok, Argon (vs agy) | `cpu_arm.c:736` exits only for exception_nr 5, and no caller passes 5, RESET or FIQ | CONFIRMED · READ | `src/include/cpu_arm.h:124-126`, `:135`; `cpu_arm.c:735-736`; every caller: `cpu_arm.c:1803`, `:2727`, `cpu_arm_instr.c:1018`, `:1031`, `:1044`, `cpu_dyntrans.c:209`, `memory_arm.c:269`, `:273` | BRIEF PREMISE: a host-only exit |
| F18 | grok-rec, grok, Argon (vs agy) | the nearest house idiom is the per-CPU `mode_warned` bits (MSR 0x01, POP 0x02, DPI 0x04, SAVE 0x08, LOAD 0x10); `memory_arm.c` has no latch | CONFIRMED · READ | `cpu_arm.h:118-122`, `:207`; `cpu_arm.c:594`, `:652`; `cpu_arm_instr.c:840`, `:1827`; `src/cpus/cpu_arm_instr_dpi.c:241` | BRIEF PREMISE: a new ARM_MODEWARN_* bit plus "(once)" (agy's lines and bit values are wrong) |
| F19 | grok-rec (vs agy) | `arm_translate_v2p_mmu` spans `:114-277`, not 106-281 | CONFIRMED · READ | `memory_arm.c:114`, `:277` (278-line file) | BRIEF PREMISE (citation only) |
| F20 | grok-rec, grok, Argon (vs agy) | the silent-failure returns at `cpu_arm_instr.c:1735`/`:1945` are in `arm_pop`/`arm_push` (which Thumb POP/PUSH call), not in bdt_load/store | CONFIRMED · READ | `cpu_arm_instr.c:1621`, `:1868`, `:1992`, `:2024`; `cpu_arm.c:1720`, `:1727` | BRIEF PREMISE (the path in F6) |
| F21 | grok-rec, grok, Argon (=agy) | the SA1110 "no Thumb" question is already ANSWERED: no per-CPU Thumb capability exists, and T alone selects the interpreter | CONFIRMED · READ | `src/include/arm_cpu_types.h:39-42`, `:82`; `cpu_dyntrans.c:255`; `ledger.json:48071` "ANSWERED 2026-10-09"; records-adj §1: consistent, not re-derived | BRIEF PREMISE: settled; do not re-ask |
| F22 | grok | five machines install the MMU-on boot table (cats, iq80321, iyonix, netwinder, rpi); testarm, barearm, androidarm and hpcarm boot with it off | CONFIRMED · READ | `src/machines/machine_cats.c:131`, `machine_iq80321.c:89`, `machine_iyonix.c:95`, `machine_netwinder.c:70`, `machine_rpi.c:53`, `machine_androidarm.c:64`, `machine_hpcarm.c:63`; `ledger.json:48098` ("THE THREE ARM MACHINES") | BRIEF PREMISE for armmmuvehicle: nine ARM setups, not three |
| F23 | Argon | the immediate-offset stop prints "could not load ..." for STR/STRB/STRH too | CONFIRMED · READ | `cpu_arm.c:1647-1649` | BRIEF PREMISE: if the fatal stays, fix its wording |
| F24 | Argon | bundle-gap flags (3): ddi0100i.txt; cpu_arm.h, tmp_arm_head/tail.c, cpu_arm_instr_misc.c, src/core/memory.c; the ledger-cited artifact files | CONFIRMED · READ | disk:`_scratchpad/gweb/jobs_20261014_argonpack6/armthumbabortkill_prep/argon_bundle.manifest:1-28` | PACKET only.  Settled at F8/F10, F17/F18, F3 |
| F25 | grok, grok-rec, Argon (=agy) | exit census: no guest-producible `exit(` in `cpu_arm.c`/`cpu_arm_instr.c` from Thumb; the seven coprocessor exits are unreachable in Thumb state; `memory_arm.c:79`/`:254` are reachable from Thumb with the MMU on | DISPOSED · READ | disk:`fable5_records_adjudication.md:267` (v2.6); `src/cpus/cpu_arm_coproc.c:62`, `:177`, `:264`, `:322`, `:331`, `:417`, `:528` | none (Argon's verdict line says "10 exit sites", against its own 13-site list) |

Counts (armthumbabortkill_prep): DISPOSED 2 · CONFIRMED 22 (FILE-new 1, ADD-TO-ROW 5, ALREADY-FILED 3, RECORD 1,
BRIEF 11, PACKET 1) · REFUTED 1 · CANNOT SETTLE 0 · total 25.

## armdesc3kill_prep

Seats: grok 15,134 b · grok-rec 13,157 b · Argon 23,033 b · agy answered 4 flags.  Sub-agent read.  **[spot-checked]**:
- F17: `src/cpus/memory_arm.c:136`, `:169` mask with `0x0fffffff`, and no ledger or OUTSTANDING_BUGS row mentions it.
- F4/F5: `_scratchpad/ddi0100i.txt:29371-29372`, `:29760-29763`.
- F7: `_scratchpad/ddi0406.txt:66175-66181`; `src/include/arm_cpu_types.h:36`, `:77-78`, `:102-103`.
- The noticed coarse-L2 item, N2.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok-rec, Argon | `memory_arm.c:254` is reached by any MMU-on access whose walk fetches a type-3 L1 word (data `memory_rw.c:248`, fetch `cpu_dyntrans.c:679`) | DISPOSED · READ | disk:`regress/artifacts/recordfix_20261013/adj_20261013/fable5_records_adjudication.md:267`; `src/cpus/memory_arm.c:140-155`, `:252-254` | none (v2.6 says it for Thumb; the same walker) |
| F2 | grok, grok-rec (Argon: VERIFIED) | "any guest that uses fine page tables kills the host at its first translation" is too broad: it needs the MMU walker, a non-NULL L1 page and a fetched `d&3==3`.  MMU off, NULL pages, dyntrans hits and the boot `0xc02` sections never reach it | CONFIRMED · READ | `OUTSTANDING_BUGS.md:22132`; disk:`regress/artifacts/astraretro_20260926/DISPOSITIONS.md:329`; `memory_arm.c:54-59`, `:118`, `:140-141`; `src/cpus/cpu_arm.c:118`, `:244`; `src/cpus/cpu_dyntrans.c:658-662` | RECORD CORRECTION: `OUTSTANDING_BUGS.md:22132` (+ `DISPOSITIONS.md:329`) -> "kills the host at the first MMU-on walk that fetches a type-3 L1 entry" |
| F3 | grok-rec | once narrowed, the HIGH grade may not stand | REFUTED · REASONED | `memory_arm.c:131-155`; `cpu_dyntrans.c:658-680`; `memory_rw.c:245-252` | none.  Keep HIGH: a VA under a type-3 entry never caches a translation (its walk never completes), so the first access through any fine table dies |
| F4 | grok, Argon (=agy) | "Type 3 is a LEGAL ARMv4/v5 descriptor" has no citation | CONFIRMED · READ | `ledger.json:53074`; `OUTSTANDING_BUGS.md:22131`; `_scratchpad/ddi0100i.txt:29760-29763` | RECORD CORRECTION: cite ddi0100i.txt:29760-29763 (B4.8.1); RESERVED in VMSAv6 at :29371-29372 |
| F5 | grok, grok-rec | the legality cannot be verified (no manual in the tree), so it may not be marked VERIFIED | REFUTED · READ | `_scratchpad/ddi0100i.txt:29371-29372` "physical address of a fine second-level table prior to VMSAv6" | BRIEF PREMISE: type 3 is legal before VMSAv6 (ARMv4/v5).  The local manual settles it |
| F6 | grok, grok-rec | "1 KB pages" does not describe the L1 default; the tree's only 1 KB type 3 is the coarse-L2 non-XScale arm | REFUTED · READ | `_scratchpad/ddi0100i.txt:29793` "translation information for 1KB of memory", `:29801`; `memory_arm.c:198-207` | BRIEF PREMISE: a fine table is 4 KB of 1 KB entries mapping 64 KB/4 KB/1 KB pages (:29795-29802).  IMPLEMENT means that walk; do not copy the coarse 1 KB arm |
| F7 | grok | the default reads no CPU type, so ARMv6/v7 types (ARM1136, CORTEX-A5, SnapdragonS2) take the same exit; the CPU table has no ARM-level field | CONFIRMED · READ | `src/include/arm_cpu_types.h:36`, `:77-78`, `:102-103`; `memory_arm.c:252-254`; `_scratchpad/ddi0406.txt:66175-66181` | BRIEF PREMISE: type 3 is a fine table only before VMSAv6, RESERVED in VMSAv6, a PXN section or a Translation fault on v7.  The disposition depends on architecture level |
| F8 | Argon | the row quotes member 5 as `fs = FAULT_TRANS_S; goto exception_return` and drops `domain = 0;` (`:157`), without which the FSR gets `(d>>5)&15` | CONFIRMED · READ | `memory_arm.c:152`, `:157-159`, `:272`; `OUTSTANDING_BUGS.md:22133-22134`; `_scratchpad/ddi0100i.txt:29076` | BRIEF PREMISE: quote :157-159 in full and state the FSR domain value used |
| F9 | grok, grok-rec | `FABLE_P1_ANSWER.md:41` puts the idiom at `:257`, the `exception_return:` label | CONFIRMED · READ | disk:`regress/artifacts/fbd5/p1_20260919/FABLE_P1_ANSWER.md:41`; `memory_arm.c:257`; `ledger.json:52227` | none: already corrected (`ledger.json:52227`, `p1_findings.md:123-124`) |
| F10 | grok (=agy) | the "kimi CLI, fbdeclinefive pass 1; fable5 Q5" attribution has no file:line; the entry's `ev` is a directory | CONFIRMED · READ | `ledger.json:53074`, `:53088`; `OUTSTANDING_BUGS.md:22135-22136`; disk:`regress/artifacts/fbd5/p1_20260919/p1_findings.md:35-39` | RECORD CORRECTION: cite p1_findings.md:35-39 and FABLE_P1_ANSWER.md:41 |
| F11 | grok, grok-rec | "the sites probe's arm T scaffold" has no path:line, and that scaffold never writes a `[1:0]=11` word (it walks the boot `0xc02` sections) | CONFIRMED · READ | `OUTSTANDING_BUGS.md:22134-22135`; `regress/footbridge_sites_probe.py:205-214`; `regress/gate_arm.sh:1081-1082`; `cpu_arm.c:244` | RECORD CORRECTION: "arm T = regress/footbridge_sites_probe.py:211 (cats, boot MMU on)" |
| F12 | grok, grok-rec (=agy) | no committed probe or gate writes a type-3 L1 word; `witness` is ""; armmmuvehicle is a separate, unbuilt testarm row | CONFIRMED · READ | `ledger.json:53079`, `:62247-62253`; `src/machines/machine_test.c:187-203`; `src/machines/machine_cats.c:131` | BRIEF PREMISE: a rung-3 attempt is owed.  cats already boots with the MMU on, so armmmuvehicle is optional, not a prerequisite |
| F13 | grok, grok-rec | agy's "zero regress probes reach the MMU translation path" is false: gate 14 runs three cats arm-T probes through `arm_translate_v2p_mmu` (L1 type 2 only) | CONFIRMED · READ | `regress/gate_arm.sh:1081-1082`, `:1220-1222`, `:1799-1800`; `regress/fbpending_drain_probe.py:215-217`; `regress/footbridge_sites_probe.py:13-18` | BRIEF PREMISE: the walker is reached; the default is not |
| F14 | grok-rec, Argon | the default exits before `:258` tests `no_exceptions`, so FLAG_NOEXCEPTIONS callers (the debugger's watchpoint translate) die too | CONFIRMED · READ | `memory_arm.c:252-259`; `src/debugger/debugger_cmds.c:461-462`; `memory_rw.c:250` | BRIEF PREMISE: a FAULT via `goto exception_return` honours `no_exceptions`; the debugger is a second route |
| F15 | grok, grok-rec, Argon | member 5 lands safely (PREF/DATA_ABT map to ABT32), but a fetch abort whose handler PC also fails ends at `cpu_dyntrans.c:729-733` | CONFIRMED · READ | `memory_arm.c:268-276`; `src/include/cpu_arm.h:124-126`, `:133-134`; `cpu_arm.c:671-674`, `:735-736`; `cpu_dyntrans.c:720-733`; `ledger.json:51859-51863` | BRIEF PREMISE; the second hazard is already filed: alphaifetchkill |
| F16 | Argon, grok | a NULL L1 host page leaves `d = 0`, so the walk takes case 0 (a translation fault), not an external abort | CONFIRMED · READ | `memory_arm.c:118`, `:140-141`, `:157-159`; `src/core/memory.c:536-537` | BRIEF PREMISE (by design; not a type-3 route) |
| F17 | Argon | the walker masks the TTB and L2-table physical addresses with `0x0fffffff`, dropping bits [31:28]; tables above 256 MB are read from the wrong place (rpi defaults to 512 MB) | CONFIRMED · READ **[spot-checked]** | `memory_arm.c:136` `ttb & 0x0fffffff`, `:169` `addr & 0x0fffffff`; `src/machines/machine_rpi.c:69` (512); `src/machines/machine_iq80321.c:68-69`; ledger/OUTSTANDING_BUGS grep `0x0fffffff`: no row | FILE: new row (not armdesc3kill) |
| F18 | Argon | IMPLEMENT will meet the pc-relative literal fold at `cpu_arm_instr.c:4785-4786`, which "assumes 4KB pages" | CONFIRMED · READ | `src/cpus/cpu_arm_instr.c:4774-4795`; `ledger.json:58338-58341` | BRIEF PREMISE for IMPLEMENT; same 1 KB class as `subpagecache` (consider adding it there) |
| F19 | grok, grok-rec, Argon | the L1 default is the file's outlier: every other bad L1/L2 state goes to `exception_return`; the only other exit is `:78-79` (armdacr2kill) | CONFIRMED · READ | `memory_arm.c:78-79`, `:157-250`; `src/cpus/memory_mips_v2p.c:185-187` | BRIEF PREMISE (sibling disposition; #238's MIPS precedent) |
| F20 | grok-rec | line drift: agy :156->155 (switch), :158-160->157-159 (idiom), :275->276 (return), cpu_arm.c:616->666 (`arm_exception`); grok machine_cats.c:136->137, and memory_m88k.c:408-413 calls `debugmsg_cpu`, not `fatal` | CONFIRMED · READ | `memory_arm.c:155-159`, `:235`, `:257`, `:276`; `cpu_arm.c:616`, `:666`; `machine_cats.c:137`; `src/cpus/memory_m88k.c:409-413` | BRIEF PREMISE: switch :155, idiom :157-159, label :257, return :276, `arm_exception` cpu_arm.c:666 (agy miscounted; it did not read a stale copy) |
| F21 | Argon | bundle-gap flags (5): ddi0100i.txt + armreg.h; fbd5/ + the sites probe; DISPOSITIONS.md; cpu_arm.c + cpu_arm_instr_loadstore.c; regress/*.py + gate_*.sh | CONFIRMED · READ | `_scratchpad/gweb/jobs_20261014_argonpack6/armdesc3kill_prep/argon_bundle.manifest:4-17` | PACKET only, no round action.  Settled at F4/F5, F10, F11, F2, F15, F12/F13 |
| F22 | Argon | `cpu_arm_coproc.c` has "6 active" fatal+exit sites | REFUTED · READ | `src/cpus/cpu_arm_coproc.c:62`, `:177`, `:264`, `:322`, `:331`, `:417`, `:528` (seven) | none (the count belongs to armexits) |

Counts (armdesc3kill_prep): DISPOSED 1 · CONFIRMED 17 (FILE 1, RECORD 5 [one already made], BRIEF 10, PACKET 1) ·
REFUTED 4 · CANNOT SETTLE 0 · total 22.

## armexits_db8b1a33

Seats: grok 26,337 b (auto-compacted) · grok-rec 12,071 b · Argon 36,344 b · agy answered 9 flags.  Rows
`armendianexit`, `xscalecp6exits` and `armcp15cp14exits` (the seven sibling exits of `src/cpus/cpu_arm_coproc.c`).
Sub-agent read.  `D` = `regress/artifacts/astraretro_20260926/DISPOSITIONS.md` (tracked).  **[spot-checked]**:
- F3: `OUTSTANDING_BUGS.md:18738-18740` vs `cpu_arm_coproc.c:319-322`.
- F5: `cpu_arm_coproc.c:157-177`; `cpu_arm.c:128-137`; `machine_test.c:179`.
- F14: the only `coproc[6]` installs are `machine_iq80321.c:57` and `machine_iyonix.c:64`; `coproc[14]` is installed
  only when `ARM_XSCALE`, `cpu_arm.c:178-179`.
- F15: `regress/xscale_inten_probe.py:381`, `:396`, `:426`; `gate_arm.sh:1852`.
- F20: `cpu_arm_coproc.c:124-135`.  No ledger hit for `armcp15c1fallthrough`.
- F27: `cpu_arm_coproc.c:322` is `exit(1);`.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok, grok-rec (=agy) | armendianexit's note and queue body cite `OUTSTANDING_BUGS.md:18721-18722` with no commit; at HEAD those lines are the mapledmaaddr oracle, and the seven-sibling sentence is `:18773-18774` (the titles do say "at db8b1a33") | CONFIRMED · READ | `OUTSTANDING_BUGS.md:18721-18722`, `:18772-18774`, `:22878`; `ledger.json:56564`; `db8b1a33:OUTSTANDING_BUGS.md:18720-18722` | RECORD CORRECTION: `:22878` and `ledger.json:56564` -> "18721-18722 at db8b1a33 (HEAD :18773-18774)" |
| F2 | grok, grok-rec (=agy) | the prose's cpu_arm.c cites drifted +50: :2677->:2727, :616->:666, :634->:684, :2660->:2710 (agy's "+47" was measured to the function start) | CONFIRMED · READ | `OUTSTANDING_BUGS.md:18756`, `:18761`, `:18763`; `src/cpus/cpu_arm.c:666`, `:684`, `:2710`, `:2727` | RECORD CORRECTION: add "at db8b1a33", or re-key to :2727/:666/:684/:2710 |
| F3 | grok, grok-rec | the xscaleinten prose says case 4 (isteer) "carries no fatal() and no exit()"; a nonzero isteer store fatals and exits, as it has since the import | CONFIRMED · READ **[spot-checked]** | `OUTSTANDING_BUGS.md:18738-18740`; `src/cpus/cpu_arm_coproc.c:319-322`; `CHANGELOG.md:4670-4671` (already the true, narrower form) | RECORD CORRECTION: `:18740` -> "its load arm carries neither; a nonzero store exits (:322)" |
| F4 | grok, grok-rec | the same paragraph's inten-load quote (`fatal("TODO: XScale read from inten?")`; `exit(1)`) is stale and needs repair | REFUTED · READ | `eb26590b` (#526) deleted those lines; `OUTSTANDING_BUGS.md:19542` "SHIPPED as `#526`"; a dated filing text is history (`astraretro_20260926/adjudication/fable_batch2a.md:125`) | none |
| F5 | grok, grok-rec, Argon (Argon says VERIFIED while describing the compare) | "a c1 write that toggles the B bit" mis-states the predicate: the old B is rebuilt from byte_order.  On barearm (BE, reset B=0), a write that keeps B clear dies, and one that sets B survives | CONFIRMED · READ **[spot-checked]** | `cpu_arm_coproc.c:157-162`; `cpu_arm.c:123`, `:128-129`; `src/machines/machine_test.c:179`; `src/core/emul.c:652`, `:738`; `ledger.json:56557`; `OUTSTANDING_BUGS.md:22877`; `D:137` | RECORD CORRECTION: "toggles the B bit" -> "writes a B bit unequal to (byte_order == BE)" (titles + D:137) |
| F6 | grok, grok-rec, Argon (UNSETTLED) | "a bare deletion breaks the translate-time byte-order premise" is false: the c1 path only reads byte_order, so after a deletion the LDM/STM gate still sees the old order.  What breaks is the guest's B switch, silently ignored | CONFIRMED · READ | `cpu_arm_coproc.c:158`, `:169-170`; `src/cpus/cpu_arm_instr.c:4846-4849`, `:4857-4858`; control.B read only at `cpu_arm_coproc.c:157-162`, `cpu_arm.c:490-492` | RECORD CORRECTION: D:138-139 (quoted at `ledger.json:56564`) -> "bare deletion keeps byte_order; implementing the switch breaks the premise" |
| F7 | grok, grok-rec | the #378 comment says `invalidate_translation_caches(INVALIDATE_ALL)` re-picks cached ic->f; that branch drops vph TLB entries only, and code handlers need `arm_invalidate_code_translation` | CONFIRMED · READ | `cpu_arm_coproc.c:170-172`; `cpu_arm.c:115-117`; `src/cpus/tmp_arm_tail.c:26`, `:30`; `src/cpus/cpu_dyntrans.c:1276-1288`, `:1324`; an unapplied L4 at `D:350-351` (`OUTSTANDING_BUGS.md:24259-24260`) | BRIEF PREMISE: apply D:350-351's L4 in the armendianexit round |
| F8 | grok | #378's "every other write is machine setup" was never enumerated | CONFIRMED · READ | every byte_order writer is init/load-time: `cpu_arm.c:123`, `machine_test.c:179`, `src/core/emul.c:652`, `:738`, `:743`, `src/file/file.c:212`; `git grep 'byte_order *='` finds no runtime writer | BRIEF PREMISE: the premise holds; list the writers |
| F9 | grok, grok-rec, Argon | xscalecp6exits' title says "the entry's other three siblings are armcp15cp14exits"; the complement of three CP6 sites in seven is four (armendianexit too) | CONFIRMED · READ | `ledger.json:57217`; `OUTSTANDING_BUGS.md:22886`, `:18773-18774`; `ledger.json:56557` | RECORD CORRECTION: "the entry's other four siblings: armcp15cp14exits (3) and armendianexit" |
| F10 | grok, grok-rec (=agy) | agy: xscalecp6exits and armcp15cp14exits are an artificial split, because D:284 says "the six siblings are one entry, one id owed" | REFUTED · READ | `D:279` "recorded, not final"; `D:298-299` (Batch 2c ruled 2026-09-30); `D:335-336` assigns 322/331/417 to xscalecp6exits, and the other three "keep their owed id" | none; the brief cites D:335-336 |
| F11 | grok-rec, Argon (=agy) | armcp15cp14exits bundles three predicates on two coprocessors, and its `:528` is the same unknown:-label class as xscalecp6exits' `:417` | CONFIRMED · READ | `cpu_arm_coproc.c:60-62`, `:261-264`, `:414-417`, `:524-528`; `ledger.json:60722`; `OUTSTANDING_BUGS.md:18774-18775`; `_scratchpad/ddi0100i.txt:9008-9014` | BRIEF PREMISE: an id bundle, not a round (one site per round); cross-reference :417/:528 |
| F12 | grok, grok-rec, Argon | the rd==ARM_PC test runs before the crn switch, so any rd=15 CP15 transfer dies at `:62` before reaching `:177`/`:264`; it is the only rd==PC exit in src/cpus | CONFIRMED · READ | `cpu_arm_coproc.c:60-65` | BRIEF PREMISE: witnesses for :177/:264 use rd != 15 |
| F13 | Argon (+grok's CP6 RD15 row) | CP6 and CP14 have no rd==PC test (an MRC to r15 writes r[15]); armmrcr15flags names CP6 only, and `:62` is CP15's version of the same Rd=15 case | CONFIRMED · READ | `cpu_arm_coproc.c:311`, `:437-438`; `OUTSTANDING_BUGS.md:23069` (Argon cited :23035); `D:312-314`; `_scratchpad/ddi0100i.txt:9335-9339`, `:8972-8974`; `regress/xscale_inten_probe.py:512-528` | ADD TO armmrcr15flags: CP14 has the same shape; cross-reference armcp15cp14exits :62 |
| F14 | grok, grok-rec, Argon | reach per site: CP15 on every ARM CPU; CP14 only on ARM_XSCALE CPUs; CP6 only on iq80321 and iyonix.  No privilege check; ARM state only.  "XScale CP6" over-states the install | CONFIRMED · READ **[spot-checked]** | `cpu_arm.c:175`, `:178-179`; `src/machines/machine_iq80321.c:57`; `machine_iyonix.c:64`; `src/cpus/cpu_arm_instr.c:967-973`, `:5012-5015`; the NULL branch at `cpu_arm.c:2706-2711` does not exit | BRIEF PREMISE: state the install condition per site; the NULL branch is armcpabsent (`OUTSTANDING_BUGS.md:23978`) |
| F15 | grok, grok-rec, Argon | xscalecp6exits' witness field is empty, but gate 14's `xscale_inten_probe.py` already drives all three CP6 deaths as CONTROLS that assert the host dies (E_UNKNOWN, S_ISRC_WR, SIB_WRITE) | CONFIRMED · READ **[spot-checked]** | `ledger.json:57222`; `regress/xscale_inten_probe.py:23-24`, `:375-384` (->:417), `:390-399` (->:331), `:418-429` (->:322); `regress/gate_arm.sh:1852`; `CHANGELOG.md:4676-4678`; the death test's weakness is xscaldiedor (`OUTSTANDING_BUGS.md:23768`) | BRIEF PREMISE: a rung-3 witness exists; the fix round RE-PINS those three rows first (oracle-correction order) |
| F16 | grok, grok-rec, Argon (UNSETTLED) | no regress probe or gate executes `:62`, `:177`, `:264` or `:528`; the c1 store path runs only on LE cats with B clear | CONFIRMED · READ | 0 hits for c13, rd=15 CP15 or CP14 words in the 125 top-level regress .py/.sh files; c1 store 0xEE010F10 only in `regress/footbridge_sites_probe.py:206-208`, `fbpending_drain_probe.py:221`, `pit8253_latch_probe.py:73`, `fbpending_witness.py:155` | BRIEF PREMISE: a rung-3 attempt is owed; the cats c1-store probes are the nearest vehicle |
| F17 | grok, grok-rec, Argon | `:264` fires on pid != 0 after the store (an MCR of 0 survives); control/translate_v2p, pid, isteer and isrc are all stored BEFORE their exits; nothing is stored before :62/:417/:528 | CONFIRMED · READ | `cpu_arm_coproc.c:135`, `:140-142`, `:254-256`, `:260-264`, `:318-322`, `:329-331`, `:414-417`, `:524-528` | BRIEF PREMISE: a decline at the exit site leaves that write applied |
| F18 | grok, Argon | sibling census: CP15's six unimplemented arms fatal with the exit commented out; only the four write arms and the two unknown: labels exit (grok calls the CP15 default the outlier; Argon calls :417/:528 the outliers) | CONFIRMED · READ | commented: `cpu_arm_coproc.c:58`, `:87`, `:102`, `:128`, `:287`, `:294`; live: `:417`, `:528`, `:177`, `:264`, `:322`, `:331`; `cpu_arm.c:2727` (live UND); `cpu_arm.c:585-600` (#562's "(once)" latch) | BRIEF PREMISE: give the census and #562's latch idiom, not an outlier verdict |
| F19 | Argon | the m88k sibling (PSR BO flip) refuses the store and stops the CPU; ARM stores control and then exits the process | CONFIRMED · READ | `src/cpus/cpu_m88k.c:522-533`, `:553`; `D:557-563` names armendianexit as the precedent | BRIEF PREMISE (already filed: m88kpsrbokill) |
| F20 | grok, Argon | a c1 store with opcode2 outside {0,1} prints a fatal and falls through into the control write: an ARMv6 CPACR write overwrites control and can reach `:177` | CONFIRMED · READ **[spot-checked]** | `cpu_arm_coproc.c:124-135`; `_scratchpad/ddi0100i.txt:28052-28056` (opcode2 0b010 = CPACR); `src/machines/machine_rpi.c:63` (ARM1136JSR1); proposed at `D:195-197`, excluded as contingent (`astrafiling_20261002/afile_01/codex_afile_01.txt:66`); no ledger/queue row | FILE: `armcp15c1fallthrough` (MED).  The CPU half of its contingency is met (rpi is ARMv6); the guest half is open |
| F21 | grok, Argon | armmmuvehicle's path inventory names armendianexit and armcp15cp14exits, because its guest must MCR c1 | CONFIRMED · READ | `ledger.json:62253`; `OUTSTANDING_BUGS.md:24520-24527` | BRIEF PREMISE (armmmuvehicle): its c1 MCR keeps B == byte_order (B clear on testarm; barearm dies, F5) and uses rd != 15 |
| F22 | grok | `regress/arm_flags_probe.py:871` cites cr7 as `cpu_arm_coproc.c:209-215`; cr7 is `:221-228` (the cite drifted when #378 added its comment) | CONFIRMED · READ | `regress/arm_flags_probe.py:871`; `cpu_arm_coproc.c:221-228` | RECORD CORRECTION: `:871` -> ":221-228" (anchor `case 7`) |
| F23 | Argon, grok | armendianexit's governing text ends inside ppcllscrcexit's; xscalecp6exits' starts inside alphatinyzero's; alphatinyzero's ends at "322/33" | CONFIRMED · READ | `ledger.json:56564`, `:57224`, `:57202` | FILE: one instance of the governing-text window defect (filed once, ppc_six F7) |
| F24 | Argon | the titles cite bare exit(1) lines rather than guard blocks, and armcp15cp14exits states "the id is assigned HERE" without a citation | REFUTED · READ | the titles name exits and each cited line IS the exit (`cpu_arm_coproc.c:264`, `:322`, `:331`, `:417`, `:528`); `ledger.json:60722` and `OUTSTANDING_BUGS.md:22956` cite "D:335-336 and D:284" | none |
| F25 | grok-rec (=agy, disputed) | agy: "no second entry is opened" is contradicted by three ledger rows and three queue headings | REFUTED · READ | `OUTSTANDING_BUGS.md:22877` "an id for an entry this file already carries in prose" (same at `:22886`, `:22955`) | none |
| F26 | grok-rec (=agy, disputed) | agy: `:18778-18779`'s "re-verified by opening cpu_arm.c" is refuted because the kills live in cpu_arm_coproc.c | REFUTED · READ | `OUTSTANDING_BUGS.md:18772-18773` places the kills in `cpu_arm_coproc.c`; the cpu_arm.c elements are the UND facts at `:18756-18765` | none |
| F27 | grok-rec (=agy, disputed) | agy: xscalecp6exits' `:322` is the fatal() string and the exit is `:323` | REFUTED · READ **[spot-checked]** | `cpu_arm_coproc.c:322` "exit(1);", `:323` "}" | none |
| F28 | grok-rec | seat span slips: footbridge's c1 words are `:206-208`; X(mcr_mrc) closes at `:973`, arm_mcr_mrc at `:2713`; testarm's SA1110 is `machine_test.c:214` (`:208` is barearm) | CONFIRMED · READ | `regress/footbridge_sites_probe.py:205-209`; `cpu_arm_instr.c:967-973`; `cpu_arm.c:2693-2713`; `machine_test.c:208`, `:214` | BRIEF PREMISE (use these spans) |
| F29 | Argon | bundle-gap flags (5, plus the gap halves of 2 more): OB :18721-18722 and :16997-17000, DISPOSITIONS.md + astrafiling, cpu_arm_instr.c, arm_msrmode_probe.py, the CP6 installer, regress/*.py + gate_*.sh | CONFIRMED · READ | disk:`_scratchpad/gweb/jobs_20261014_argonpack6/armexits_db8b1a33/argon_bundle.manifest:8-13`, `:30`, `:32` | PACKET only.  Settled at F1, F10/F24, F6, F14, F15/F16 |

Counts (armexits_db8b1a33): DISPOSED 0 · CONFIRMED 23 (FILE 2 [F20 new; F23 the shared window filing], ADD-TO 1, RECORD
7, BRIEF 12, PACKET 1) · REFUTED 6 · CANNOT SETTLE 0 · total 29.

## excvecrecurse_prep

Seats: grok 22,750 b · grok-rec none · Argon 42,311 b · agy walled.  Sub-agent read (shared with armvecrecurse).
**[spot-checked]**:
- F5: `OP1:207`, `:222-223`.
- F6, the SH half: `cpu_sh.c:910-918`, `:1015-1021`.
- F8: `src/cpus/cpu_ppc.c:102-103` is a comment.  `M/` and `P/` as above.  `DISP` =
`regress/artifacts/astraretro_20260926/DISPOSITIONS.md`.  `OP1` =
`regress/artifacts/alphaifetchkill/p1_20260919/panel_20260919_003152/opus5_p1.md`.  Both are tracked.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok, Argon | excvecrecurse's ARM leg and armvecrecurse are ONE defect, and neither record names the other | CONFIRMED · READ | `ledger.json:52068-52084` and `:62369-62378` have no cross-reference; nor do `OUTSTANDING_BUGS.md:22014-22015` and `:24620-24628` (only `ledger.json:62335`, on armmmuvehicle, names armvecrecurse) | RECORD CORRECTION: cross-reference at `ledger.json:52075` ("ARM leg measured 2026-10-09 as armvecrecurse") and `:62376`.  One round |
| F2 | grok, Argon | the state_note's `cpu_arm.c:731-733` (and `DISP:159`'s `:733`) no longer point at the vector store and call | CONFIRMED · READ | `src/cpus/cpu_arm.c:731-733` are now the IRQ32/FIQ32 SPSR cases; the store and call are at `:780-783` (#562 added 50 lines) | RECORD CORRECTION at `ledger.json:52075`: `cpu_arm.c:731-733` -> `:780-783` (leave the dated DISP) |
| F3 | grok | `DISP:161` "OUTSTANDING_BUGS.md:21950 says MED": `:21950` is blank now, and the heading at `:22014` says HIGH | CONFIRMED · READ | `OUTSTANDING_BUGS.md:21950`, `:22014` (it was `:21950` at db8b1a33) | BRIEF PREMISE: cite `:22014` (DISP was right when written) |
| F4 | grok (contradicts its armvec answer) | arm_exception's call runs the MODE32 macro (h:9-14 hit, h:15-16 miss) | REFUTED · READ | `cpu_arm.c:82` includes the header before MODE32 is defined (`tmp_arm_tail.c:8`), so h:29 applies | BRIEF PREMISE (= armvec F10) |
| F5 | grok; Argon (code VERIFIED, run UNSETTLED) | "Witness (Opus): ... one jump ... then SIGSEGV" is the Opus PREDICTION; the only run was meas3's `ldr` (armvecrecurse), which this row does not cite | CONFIRMED · READ | `OP1:207` "derived by reading and NOT witnessed", `:222-223` "Predicted"; `ledger.json:52074-52075`; `M/meas3.py.txt:74-77` | RECORD CORRECTION at `ledger.json:52075`: "Witness (Opus):" -> "Predicted (OP1:222-223); ARM leg measured as armvecrecurse (ldr, not jump)" |
| F6 | grok; Argon (UNSETTLED) | "NOT READ: SH BL / M88K CMMU" is answerable: SH stops at depth 2 (BL forces reset to P2); M88K recurses only with supervisor APR_V | CONFIRMED · READ | `src/cpus/cpu_sh.c:910-918`, `:1015-1021`; `src/cpus/memory_sh.c:373-376`; `cpu_m88k.c:811-818`, `:863`, `:980`; `memory_m88k.c:143-144`, `:417-419` | RECORD CORRECTION at `ledger.json:52073/52075`, `OUTSTANDING_BUGS.md:22014-22015`: "(possibly SH, M88K)" -> "(M88K when SAPR.V set; SH bounded)" |
| F7 | grok; Argon (UNSETTLED) | PPC leg: `ppc_translate_v2p` raises before `return 0`, and `ppc_exception` leaves IR set and nests pc_to_pointers, so it has the same unbounded shape (unmeasured) | CONFIRMED · READ | `memory_ppc.c:313`, `:322-326`; `cpu_ppc.c:335-344`, `:105-110` (initial IBATs cover both vector bases); real hardware clears IR/DR on exception entry (`_scratchpad/ppc_pem32_rev2_2001.txt:11486`) | BRIEF PREMISE: read, not measured; it needs the guest to reprogram the IBATs |
| F8 | Argon | the initial MSR sets IR\|DR (citing `cpu_ppc.c:102`) | REFUTED · READ **[spot-checked]** | `src/cpus/cpu_ppc.c:102-103` is a commented-out line | drop |
| F9 | grok; Argon (Alpha only) | siblings: MIPS cannot recurse (kseg0/1 vectors, EXL forces kernel mode); Alpha raises nothing and exits at :732; RISC-V/i960 exception functions are uncalled | CONFIRMED · READ | `cpu_mips.c:2165-2168`, `:2212`, `:2219-2223`; `memory_alpha.c:192-198`; `cpu_riscv.c:316-323`; `cpu_i960.c:366-373`; `OUTSTANDING_BUGS.md:21996` | BRIEF PREMISE; Alpha is already filed: alphaifetchkill (`ledger.json:51859`) |
| F10 | Argon (grok contra) | the generic lookup's contract forbids translate_v2p nesting pc_to_pointers, and ARM breaks it | REFUTED · READ | PPC, MIPS, SH and M88K all nest: `cpu_ppc.c:341-344`, `cpu_mips.c:2219-2223`, `cpu_sh.c:1088`, `cpu_m88k.c:980` | BRIEF PREMISE (= armvec F11) |
| F11 | grok | "a predicted host stack overflow" is not in the measurement: only signal(11) via WTERMSIG, no backtrace | CONFIRMED · READ | `M/meas3.py.txt:111-114`; `M/meas3_base.out:36`; `ledger.json:52073` already says "predicted" | BRIEF PREMISE: signal 11 measured, stack exhaustion inferred.  Open: one backtraced rerun |
| F12 | grok, Argon | 47,591 counts the initiating abort and no warnings | CONFIRMED · READ | `M/meas3.py.txt:122`; `cpu_arm.c:758`; `M/meas3_base.out:39` | RECORD CORRECTION (= armvec F3; one edit) |
| F13 | grok | `meas3_base.out` is 2,267 b; the 10,473,809-b buffer was not kept; "could not find ... zero times" is the script's own print | CONFIRMED · READ | `git cat-file -s`; `M/meas3.py.txt:121-125`; `M/meas3_base.out:37` | RECORD CORRECTION (= armvec F5; one edit) |
| F14 | grok | "a guest that unmaps its own vectors ... ends the emulator" was never run as a guest image; the session was debugger put/step | CONFIRMED · READ | `M/meas3.py.txt:76-80` | BRIEF PREMISE (= armvec F6) |
| F15 | grok | the fault line and the mode warning are "both quiet_mode-gated" | REFUTED · READ | `cpu_arm.c:758-760` has no quiet_mode test, and `fatal()` never returns early (`src/core/debugmsg.c:384-391`); only `memory_arm.c:261` is gated | BRIEF PREMISE: the warning prints even under -q |
| F16 | grok | the c8 in the meas3 prefix is why the vector fetch walked the table; without it a warm page-0 translation serves the vector | CONFIRMED · READ | `M/meas3.py.txt:34`; `P/opus5/opus5_pass1.md:57-60` | BRIEF PREMISE (= armvec F7) |
| F17 | grok; Argon (UNSETTLED) | no regress/*.py or gate_*.sh drives the path ("testarm never enables the MMU") | CONFIRMED · READ | `regress/arm_writeback_probe.py:123-125`; `regress/gate_arm.sh:96`; `regress/xscale_inten_probe.py:52` (iq80321 PROM turns the MMU on, `src/machines/machine_iq80321.c:86-89`, but nothing unmaps the vector page) | BRIEF PREMISE (= armvec F14) |
| F18 | Argon | neither row's title or OUTSTANDING_BUGS entry cites source lines | CONFIRMED · READ | `ledger.json:52073`, `:62376`; `OUTSTANDING_BUGS.md:22014-22015`, `:24624-24626` | BRIEF PREMISE (= armvec F9) |
| F19 | Argon | bundle-gap flags (10): meas3/T3, DISP + harness dispositions, quick_pc_to_pointers.h + tmp_arm_*, memory_ppc.c + tmp_ppc_*, SH, M88K, MIPS/Alpha/RISC-V/i960/memory_rw.c, 7 headers, regress/*.py + gate_*.sh, the `git log -S` output | CONFIRMED · READ | disk:`_scratchpad/gweb/jobs_20261014_argonpack6/excvecrecurse_prep/argon_bundle.manifest` | PACKET only.  Settled at F12-F13, F2/F3/F6, F4, F7, F9, F17 |

Counts (excvecrecurse_prep): DISPOSED 0 · CONFIRMED 15 (RECORD 6 [two shared with armvec], BRIEF 8, PACKET 1) ·
REFUTED 4 · CANNOT SETTLE 0 · total 19.  (Apparatus aside, checked: three of the seven Argon banks, excvecrecurse,
armexits and arcbios_three, still record `transport=manual (owner pasted)` in `gemini_web.argv`.  That is the default the
other four argv files mark "CORRECTED 2026-10-16".  See the noticed list.)

## arcbios_three

Seats: grok 18,294 b · grok-rec none · Argon 33,822 b · agy walled.  Rows `arccursorbound`, `arcsgiprivate` and
`arczeroalloc` are three defects.  None is a pair with another.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok, Argon | the arccursorbound and arczeroalloc titles carry no source path:line | CONFIRMED · READ | `ledger.json:58691`, `:58713`; `OUTSTANDING_BUGS.md:22940`, `:22943` | BRIEF PREMISE: cite `src/promemul/arcbios.c:208-219`, `:240-252`; `:1754-1759`, `:1835-1840` |
| F2 | grok, Argon | "walk 2^31 cells" is 2^31-1: `ESC[r;2147483647H` gives `console_curx` 2147483646, and `i<=stop` runs 2147483647 times | CONFIRMED · READ | `arcbios.c:213-218`, `:243`, `:248` | RECORD CORRECTION (minor): title "2^31-1 cells" |
| F3 | grok | the walk is not a defined putcell sequence: `2*(x + console_maxx*y)` is signed `int` and overflows at x >= 2^30 | CONFIRMED · READ | `arcbios.c:122-123` | BRIEF PREMISE: the walk is UB past x = 2^30.  The witness need not run it to the end |
| F4 | grok | only the `atoi != 2` arm walks to `console_curx` (0 and 1 included); `ESC[2K` stops at maxx-1; the hardware-cursor clamp is not stored back | CONFIRMED · READ | `arcbios.c:241-247`, `:380-383` | BRIEF PREMISE (the witness uses `ESC[K`) |
| F5 | Argon | with `ESC[2K` and curx >= maxx, case 'K' "walks backwards / does 0 iterations" | REFUTED · READ | `arcbios.c:248` `for (i=start; i<=stop; i++)` runs zero times when start > stop | none (harmless) |
| F6 | Argon | through '\t' curx can reach 2147483647, and `i <= stop` then overflows `i` | REFUTED · READ | `arcbios.c:358-360`: a tab yields the next multiple of 8 (at most 2147483640 without overflow); INT_MAX comes only from signed overflow in that tab arithmetic | BRIEF PREMISE: the tab arithmetic itself overflows (UB) at curx >= 2147483641 |
| F7 | grok, Argon | arczeroalloc has two twin sites (Read `:1754-1759`, Write `:1835-1840`), one defect; handle 2 (stderr) also takes the malloc arm | CONFIRMED · READ | `arcbios.c:1754-1759`, `:1835-1840` | BRIEF PREMISE: one round, both arms |
| F8 | grok | DEC PROM, named as the cap's model ("#191"), also refuses A2 <= 0 with `(int32_t)A2 > 0 &&`; ARC lets 0 through | CONFIRMED · READ | `src/promemul/dec_prom.c:139-140`, `:458-459`; `arcbios.c:1750-1754` | BRIEF PREMISE: the in-tree idiom for the fix |
| F9 | grok, Argon | whether `malloc(0)` returns NULL, and so whether `CHECK_ALLOCATION` exits, is not in the tree | CANNOT SETTLE · REASONED | `src/include/misc.h:181-192` (exit only on NULL); `src/disk/diskimage_scsicmd.c:148-150` (#243 shape) | one run: `malloc(0) == NULL?` on the build host's libc.  glibc is expected non-NULL, so the HIGH grade is the question (contrast dectxzero, F11) |
| F10 | Argon | in Write, an A2 with bit 31 set fails the 64 MiB uint64 cap, so A2 == 0 is the only zero-length case that reaches malloc | CONFIRMED · READ | `arcbios.c:1835-1842` | BRIEF PREMISE (witness: A2 = 0 on a disk handle) |
| F11 | Argon | arczeroalloc is dectxzero's class (zero-size allocation -> NULL -> CHECK_ALLOCATION exit), cited as `OUTSTANDING_BUGS.md:22892` | CONFIRMED · READ | `OUTSTANDING_BUGS.md:22895` (dectxzero; `:22892` is vgadirtyarm) | BRIEF PREMISE: cross-reference dectxzero.  Its `realloc(p,0)` is NULL on glibc; `malloc(0)` is F9's open question |
| F12 | grok, Argon | arcsgiprivate cites `:1271`, the `MACHINE_SGI` test; the call is `:1272` | CONFIRMED · READ | `arcbios.c:1271-1272` | RECORD CORRECTION (minor): title `:1271` -> `:1271-1272` |
| F13 | grok | the SGI default clears only the current CPU's `running`; non-SGI private calls and the standard ARC default return EINVAL and do not stop | CONFIRMED · READ | `arcbios.c:1220-1226`, `:1273-1279`, `:2035-2037` | BRIEF PREMISE: the house idiom is EINVAL; the SGI default is the file's outlier |
| F14 | grok | slot 0x04 (its case is commented out) reaches the default; 64-bit slots are i*8, and `/=2` runs only after `arcbios_sgi_emul`, so 0x14/0x1c/0x24 are never matched in 64-bit mode | CONFIRMED · READ | `arcbios.c:1180` (`vector = cpu->pc & 0xfff`, no halving), `:1188-1193`, `:1285-1286` (halving on the standard path only), `:3213-3227` | BRIEF PREMISE (the witness vectors).  Also ADD TO arcsgiprivate: in 64-bit mode slot i dispatches as 32-bit slot 2i, so services are MIS-ROUTED, not only stopped |
| F15 | Argon | arcsgiprivate's `state_note` holds only "CONFIRMED-NEW HIGH arcsgiprivate": the window dropped the governing sentence | CONFIRMED · READ | `ledger.json:58742`; disk:`regress/artifacts/astraretro_20260926/DISPOSITIONS.md:950` | FILE: one instance of the governing-text window defect (filed once, ppc_six F7) |
| F16 | grok | `DISPOSITIONS.md:927` says CONFIRMED-FILED arcsgiprivate; `:950` and the ledger say CONFIRMED-NEW HIGH | CONFIRMED · READ | disk:`DISPOSITIONS.md:927`, `:950`, `:519` ("the AMENDMENT governs") | none: the amendment governs and the ledger follows it |
| F17 | grok | the rows' `GXEMUL [087a90]` does not resolve as a git revision | REFUTED · READ | `ledger.json:58707` "Filed by GXEMUL [087a90] (main loop)": a session tag | none |
| F18 | grok | no regress probe or gate reaches any of the three paths | CONFIRMED · READ | `git grep handle_esc_seq\|arcbios_putcell\|console_curx\|arcbios_sgi_emul\|ARC_PRIVATE\|unimplemented SGI\|CHECK_ALLOCATION` e483d931 `regress/*.py regress/gate_*.sh`: 0 | BRIEF PREMISE: witnesses are new (PICA for the console, SGI for the private vector) |
| F19 | Argon | bundle-gap flags (5): DISPOSITIONS.md + astrafiling/ (three rows); `src/include/misc.h`; sibling `src/promemul/*.c`; `regress/*.py`; `regress/gate_*.sh` | CONFIRMED · READ | `_scratchpad/gweb/jobs_20261014_argonpack6/arcbios_three/argon_bundle.manifest` ("DIR SKIPPED", "NOT FOUND regress/*.py") | PACKET only.  Settled at F9 (misc.h), F8 (dec_prom.c), F16 (DISPOSITIONS), F18 (regress) |

Counts (arcbios_three): DISPOSED 0 · CONFIRMED 15 (FILE 1 [the shared window filing], ADD-TO 1 [F14], RECORD 2,
BRIEF 9, PACKET 1, none 1) · REFUTED 3 · CANNOT SETTLE 1 · total 19.

## ascwidecount_prep

Seats: grok 18,561 b · grok-rec none · Argon not yet · agy not landed.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok | the row's `state_note` is a spliced 400-char window: it opens inside ecoffoffsetspan's text, the row's own sentence starts in the previous row's window (`:57444`), and `:1155` lands in ascoutresid's note (`:57488`) | CONFIRMED · READ | `ledger.json:57466` (opens ":414-444); defeats the #59/#62 skip-a-bad-table policy.") | FILE: one instance of the governing-text window defect (filed once, ppc_six F7) |
| F2 | grok | the title and heading state the mechanism with no path:line | CONFIRMED · READ | `ledger.json:57459`; `OUTSTANDING_BUGS.md:22904` | BRIEF PREMISE: cite `src/devices/dev_asc.c:577-584`, `:610-621`, `:662-668`, `:1154-1155` |
| F3 | grok | "yields a negative len2" is implementation-defined: a uint32 sum >= 0x80000000 assigned to `int`.  The adjudication kept the C99 qualifier ("gives -1 on gcc") and the title drops it | CONFIRMED · READ | `dev_asc.c:577-578`; disk:`regress/artifacts/astraretro_20260926/adjudication/fable_batch2e.md:70-71` | RECORD CORRECTION: title "...narrows to a negative int (implementation-defined; gcc wraps)..." |
| F4 | grok | the worked 0xffffffff -> -1 needs TCM == 0: with TCM in 1..255 the uint32 sum wraps to TCM*256-1.  A 512 programmed as TCL 0 / TCM 2 gives len2 = 511, because the epilogue clears `reg_ro` only | CONFIRMED · READ | `dev_asc.c:577-578`, `:755-761` (reg_ro), `:1234-1236` (wo->ro copy); 0xffffffff + 0x200 = 0x1ff mod 2^32 | BRIEF PREMISE: the witness must hold TCM at 0, or pick wide values whose uint32 sum is >= 0x80000000 |
| F5 | grok | not one defect with ascoutresid (the positive-clamp report at the same epilogue) or asccmddma (COMMAND phase, same unmasked store) | CONFIRMED · READ | `ledger.json:57480`, `:57502`; `dev_asc.c:755-761`, `:984-1000` | BRIEF PREMISE: three rows, one store path (`:1154-1155`) |
| F6 | grok (sibling note; the exit is this prescreen's reading) | COMMAND-phase DMA takes the same wide count into `int len` and hands it to `scsi_transfer_allocbuf` as size_t.  A sum >= 0x80000000 asks malloc for ~2^64 bytes, and the OOM arm calls `exit(1)`.  No row covers it | CONFIRMED · READ | `dev_asc.c:892` (`int ok, len, i, ch`), `:987-992`, `:1154-1155` (unmasked store); `src/disk/diskimage_scsicmd.c:147-155`; ASC rows ascwidecount/ascoutresid/asccmddma/ascpiozero do not cover it | FILE: new, HIGH candidate (a guest-reachable host exit).  pmax OpenBSD issues SELATN\|DMA on every command (`dev_asc.c:1014-1015`).  Witness: rung 3 on pmax, a 32-bit store of 0xffffffff to NCR_TCL, then SELATN\|DMA |
| F7 | grok | no regress probe or gate drives a continued DATA_OUT DMA or programs NCR_TCL wide | CONFIRMED · READ | `git grep NCR_TCL\|ascwidecount\|dev_asc_transfer\|1c300000` e483d931 `regress/*.py regress/gate_*.sh`: 0 | BRIEF PREMISE: the witness is new (pmax) |

Counts (ascwidecount_prep): DISPOSED 0 · CONFIRMED 7 (FILE 2 [one is the shared window filing], RECORD 1, BRIEF 4) ·
REFUTED 0 · CANNOT SETTLE 0 · total 7.

## crimectllane_prep

Seats: grok 14,377 b · grok-rec none · Argon not yet · agy not landed.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok | the ledger title states every premise with no path:line | CONFIRMED · READ | `ledger.json:56208` | BRIEF PREMISE: cite `src/devices/dev_sgi_ip32.c:282-287` (lane merge), `:353-381` (CONTROL), `:396-407` (default) |
| F2 | grok | the title's "acts on the raw idata of any width" is false since #529: a len other than 4/8 is declined before the switch | CONFIRMED · READ | `dev_sgi_ip32.c:296-319` "goto crime_declined" (before `:322`); `OUTSTANDING_BUGS.md:22741` "whatever width reaches" | RECORD CORRECTION: `ledger.json:56208` "of any width" -> "of the width that reaches it (len 4 or 8; others declined, #529)" |
| F3 | grok | the probe comment says a halfword at +0x08 carries bit 11 into HARD_RESET; the probe's own sh08 rows want no halt | CONFIRMED · READ | `regress/crime_width_probe.py:59-60` vs `:806-809` "CPUs NOT stopped"; `dev_sgi_ip32.c:305-306` | RECORD CORRECTION: `crime_width_probe.py:59-60` drop "or a halfword at +0x08" |
| F4 | grok | "the +0x0c write NetBSD makes" rests only on the arm's TODO, which gives no width | CONFIRMED · READ | `dev_sgi_ip32.c:354-355` "some things (such as NetBSD 1.6.2) write to 0x00c"; `OUTSTANDING_BUGS.md:22751` | BRIEF PREMISE: unwitnessed; the guest witness `:22751` asks for is still owed |
| F5 | grok | `OUTSTANDING_BUGS.md:22755-22756` "reaches only reserved high-word bits" is unsupported: crimereg.h never says reserved | REFUTED · READ | `src/include/thirdparty/crimereg.h:51` "Only lower 14 bits are valid" | none |
| F6 | grok | the "default arm's log" is `debug()`: silent free-running at default verbosity; the measured dflt=1 came from a stepped run | CONFIRMED · READ (the "stepped" part REASONED from pc +4) | `src/core/debugmsg.c:368-376`; `dev_sgi_ip32.c:403-407`; `regress/artifacts/crimewidthkill/opus_pass1_20260913/out/rows_base.out:20` (pc advanced one instruction) | BRIEF PREMISE: the +0x0c channel shows only when stepping or with -v |
| F7 | grok | crime's exact-label switch is "the outlier" against the `& ~7` switches of mace and MEC | REFUTED · READ | `dev_sgi_ip32.c:740` (macepci) and `:865` (sgi_ust) are also `switch (relative_addr)`; `& ~7` only at `:579` and `src/devices/dev_sgi_mec.c:486` | BRIEF PREMISE: exact-label switches in 3 of the file's 4 handlers |
| F8 | grok | CONTROL never holds a written value: every access forces reg[CONTROL] = ENDIANESS before the merge, and the arm never writes idata back | CONFIRMED · READ | `dev_sgi_ip32.c:231`, `:280-288`, `:353-381` | BRIEF PREMISE: a lane fix must say what CONTROL reads back |

Counts (crimectllane_prep): DISPOSED 0 · CONFIRMED 6 (RECORD 2, BRIEF 4) · REFUTED 2 · CANNOT SETTLE 0 · total 8.

## mb89352_five

Seats: grok 31,963 b · grok-rec none · Argon not yet · agy not landed.  Rows: `qhm88kstops`, `qhmbbufendstops`,
`qhmbphasestops`, `qhmbunimplstops`, `mboutcapacity` (all in `src/devices/dev_mb89352.c`, the luna88k SCSI chip).  No
pair is one defect.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok | qhm88kstops omits the nonzero-count prerequisite: a zero-count DREG read only warns, calls no helper and does not stop | CONFIRMED · READ | `src/devices/dev_mb89352.c:637-650` | BRIEF PREMISE: the witness needs TC != 0 and `xferp == NULL` |
| F2 | grok | qhm88kstops points only at prose line 2616 at db8b1a33, a three-topic bullet (PPC MSR.IP / m88k CMMU / dev_mb89352 "fatal errors"); the file has no fatal()/exit() and the stop is `:146`; `OUTSTANDING_BUGS.md:24136` maps 2616 to m88kexit only | CONFIRMED · READ | `ledger.json:61347`; `dev_mb89352.c:143-147`; `OUTSTANDING_BUGS.md:24136` | RECORD CORRECTION: add `dev_mb89352.c:143-147` to the row.  The :24136 fix is shared with ppc_six F13 |
| F3 | grok | the write twin with `xferp == NULL` logs and returns without stopping; ASC and OSIOP never clear `running` | CONFIRMED · READ | `dev_mb89352.c:213-217` | BRIEF PREMISE: the sibling disposition is DECLINE |
| F4 | grok | qhmbunimplstops glosses `:312` as "a halfword or word callback access"; the guard is `len != 1` (any non-byte length) | CONFIRMED · READ | `ledger.json:61391`; `dev_mb89352.c:304` | RECORD CORRECTION (minor): "any len != 1" |
| F5 | grok | qhmbbufendstops hands "the empty-status consequence" to b120, but b120's statement of record says the controller reports 0x00 GOOD.  On MB89352 an empty-status read stops the CPU at `:176` | CONFIRMED · READ | `ledger.json:61413` vs `ledger.json:3760` "the controller then reports 0x00 GOOD"; `src/disk/diskimage_scsicmd.c:1380-1388` (no status, `return 1`); `dev_mb89352.c:173-177` | RECORD CORRECTION: name which row owns the MB89352 `:176` outcome, and qualify b120's "0x00 GOOD" by controller |
| F6 | grok | write completion, like read completion, never resets `transfer_bufpos` (only SELECT `:402` and XFR `:429` do).  XFR of DATAIN/STAT/MSGIN allocates nothing: a second empty-buffer `:176` route that needs no unknown CDB | CONFIRMED · READ | `dev_mb89352.c:402`, `:429`, `:275-284`, `:497-506` | BRIEF PREMISE: extends the row's residual |
| F7 | grok | mboutcapacity's "16-byte block" and `p[16..511]` are example numbers: allocbuf mallocs exactly `want_len`, and the first store index is the command length (the cursor is not reset) | CONFIRMED · READ | `src/disk/diskimage_scsicmd.c:147-151`; `dev_mb89352.c:402`, `:429` | BRIEF PREMISE |
| F8 | grok | mboutcapacity's `state_note` is cut mid-token; its tail opens vgadirtyarm's note | CONFIRMED · READ | `ledger.json:57246`, `:57268` (opens "25-246, :268-280, :476-495; diskimage_scsicmd.c:888-892)") | FILE: one instance of the governing-text window defect (filed once, ppc_six F7) |
| F9 | grok | `DISPOSITIONS.md:482-484` makes MODE SELECT's `data_out_len = 12` + `return 2` a rider on mboutcapacity; the title, heading and bullet omit it | CONFIRMED · READ | disk:`regress/artifacts/astraretro_20260926/DISPOSITIONS.md:482-484`; `diskimage_scsicmd.c:1287-1291` | RECORD CORRECTION: add the rider (`diskimage_scsicmd.c:1287-1291`) to mboutcapacity's note/heading |
| F10 | grok | the NULL store is not a consequence of `return 2` alone: it needs a later DREG write with TC != 0, `data_out` still NULL and `bufpos < len`; an SCMD_XFR DATAOUT in between reallocates | CONFIRMED · READ | `dev_mb89352.c:275-280`, `:637-650`; `diskimage_scsicmd.c:888-892` | BRIEF PREMISE: witness = SELECT, WRITE CDB, TC load, DREG write (no XFR) |
| F11 | grok | b120's closure clause "both commands round the length UP before allocating" is not evidence against mboutcapacity: allocbuf allocates exactly `want_len`, and WRITE resizes without allocating | CONFIRMED · REASONED | `ledger.json:3760`; `diskimage_scsicmd.c:147-151`, `:888-892` | BRIEF PREMISE (which "both commands" b120 meant was not traced) |
| F12 | grok | the XFR DATAOUT comment cites `diskimage_scsicmd.c:778`/`:788`, now READ's `break;` and a blank; the WRITE offset test is `:888` | CONFIRMED · READ | `dev_mb89352.c:443-446`; `diskimage_scsicmd.c:778`, `:788`, `:888` | RECORD CORRECTION: re-key the comment to the `data_out_offset != size` anchor |
| F13 | grok | no regress probe or gate names the device or its DREG helpers | CONFIRMED · READ | `git grep -i mb89352` e483d931 `regress/*.py regress/gate_*.sh`: 0 | BRIEF PREMISE: witnesses are new (luna88k rig) |

Counts (mb89352_five): DISPOSED 0 · CONFIRMED 13 (FILE 1 [the shared window filing], RECORD 5, BRIEF 7) · REFUTED 0 ·
CANNOT SETTLE 0 · total 13.

## m88k_four

Seats: grok 25,869 b · grok-rec none · Argon not yet · agy not landed.  Rows: `m88kbcndnest`, `m88kconvodd`,
`m88kfpr0stop`, `m88kpsrbokill`.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok | m88kconvodd and m88kfpr0stop share `case 0x21` but are two predicates (`d == 0` vs an odd register); `d == 0` is tested first | CONFIRMED · READ | `src/cpus/cpu_m88k_instr.c:3197`, `:3317-3329`, `:3337-3348` | BRIEF PREMISE: two rows, one decoder block |
| F2 | grok | the manual cites (mc88100 :1630-1634, :2001-2006, :3523-3525, :5189-5191, :5676-5678) are "not in the tree", so unverifiable | REFUTED · READ | `_scratchpad/mc88100.txt:1633` "can be specified as beginning with r31"; `:2002` "set by an stcr or xcr"; `:3523-3525`; `:5189-5191`; `:5676-5678` | BRIEF PREMISE: cite these manual lines; they support all three rows |
| F3 | grok | trnc.sd tests `s2 & 1`, but its fatal says "truncation into uneven register" and prints `d` | CONFIRMED · READ | `cpu_m88k_instr.c:3346-3347` | BRIEF PREMISE: fix the message in the m88kconvodd round |
| F4 | grok | the odd-register and `d == 0` stops are skipped under translation readahead, and their `fatal()` runs unguarded during readahead | CONFIRMED · READ | `cpu_m88k_instr.c:3203`, `:3236`, `:3327`; `src/cpus/cpu_dyntrans.c:1990-1991` | BRIEF PREMISE: "stops" means on execution |
| F5 | grok | m88kfpr0stop's "arithmetic/convert" class leaves out fcmp, one of the 8 counted sites | CONFIRMED · READ | `cpu_m88k_instr.c:3294-3299`; `ledger.json:57723` | RECORD CORRECTION: title -> "every FP arithmetic/convert/compare decode (8 sites)" |
| F6 | grok | the manual's FP unimplemented-opcode exception is SFU1-precise + FPECR_FUNIMP in-tree, and SFU1 delivery itself halts every CPU (m88kexcsfu1) | CONFIRMED · READ | `cpu_m88k_instr.c:1225-1229`; `src/cpus/cpu_m88k.c:753-755`, `:799-807`; `ledger.json:36853` (m88kexcsfu1) | BRIEF PREMISE: m88kfpr0stop's fix depends on m88kexcsfu1, because raising SFU1 still halts |
| F7 | grok | bcnd rider (i), "three or more untaken outers", passes `ics[1025]` only when the target's index is >= 1023 (S + K >= 1026) | CONFIRMED · READ | disk:`regress/artifacts/astraretro_20260926/DISPOSITIONS.md:566-568`; `src/include/cpu_m88k.h:170-173`; `src/include/cpu.h:81` | BRIEF PREMISE: cite the governing amendment `DISPOSITIONS.md:553` (position-dependent; it governs per `:519`), not the riders |
| F8 | grok | bcnd rider (ii) says the taken outer uses "its own delay_target"; the field is shared | CONFIRMED · READ | `src/cpus/tmp_m88k_bcnd.c:313-318`, `:325`; disk:`DISPOSITIONS.md:570-571` vs `:553` | as F7 (the amendment already governs) |
| F9 | grok | m88kpsrbokill's "writes PSR": the flipped value is never stored (the return at `:532` precedes the store at `:553`) | CONFIRMED · READ | `cpu_m88k.c:522-532`, `:553` | BRIEF PREMISE (`m88k_exc_probe.py:244`'s "stores ... after its checks" is accurate) |
| F10 | grok | rte reaches the BO stop through `m88k_stcr` without X(stcr)'s abort: it carries on through the NIP/FIP sequence in the same burst | CONFIRMED · READ | `cpu_m88k_instr.c:2249` (no running test) vs `:843-847` | BRIEF PREMISE: two stop shapes (abort vs deferred) |
| F11 | grok | xcr also calls `m88k_stcr` (the manual: BO "set by an stcr or xcr"), so xcr reaches the same stop; the title names only stcr/rte | CONFIRMED · READ | `cpu_m88k_instr.c:2224-2231`; `_scratchpad/mc88100.txt:2002` | RECORD CORRECTION: add xcr to `ledger.json:60781` |
| F12 | grok | `DISPOSITIONS.md:561`'s "greps for endianness, PSR_BO, byte order find nothing" is false (PSR_BO is in src) | REFUTED · READ | the grep was a filing check over the queue (`:560-561`); `8ea26abb:OUTSTANDING_BUGS.md` has 0 such m88k lines | none |
| F13 | grok | no probe executes any of the four stop paths (m88k_exc_probe.py discloses BO/MXM as untested) | CONFIRMED · READ | `regress/m88k_exc_probe.py:85`; `git grep uneven\|d = 0 in\|PSR_BO\|<the four ids>` e483d931 `regress/*.py regress/gate_*.sh`: only `m88k_idle_probe.py:24` (bcnd_n_eq0 idle fold) | BRIEF PREMISE: all four witnesses are new |

Counts (m88k_four): DISPOSED 0 · CONFIRMED 11 (RECORD 2, BRIEF 9) · REFUTED 2 · CANNOT SETTLE 0 · total 13.

## ppc_six

Seats: grok 27,785 b · grok-rec none · Argon not yet · agy not landed.  Rows: `ppcbatppkill`, `ppcfmasingle`,
`ppcllscrcexit`, `qhppcdecode`, `qhppciphack`, `qhslowifetch`.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok | ppcbatppkill attributes `memory_ppc.c:273-276` to `ppc_bat_block` | REFUTED · REASONED (reads the record's arrow as flow) | `ledger.json:56322` reads "`ppc_bat_block` -> `:273-276`", a flow arrow: `src/cpus/memory_ppc.c:69-73` return 0, `:273-276` exits | none |
| F2 | grok | `ppc_pem32_rev2_2001.txt` is not in the tree, so `:13503-13519` (and the `:13312` variant) cannot be checked | REFUTED · READ | `_scratchpad/ppc_pem32_rev2_2001.txt:13503-13519` (Fig. 7-9: block protection violation -> ISI/DSI); `:13312` (§7.5.4 prose) | BRIEF PREMISE: cite :13312 (prose) with :13503-13519 |
| F3 | grok | the BAT exit precedes the FLAG_NOEXCEPTIONS test, and it is the file's outlier: a page-table protection failure delivers DSI/ISI with DSISR_PROTECT | CONFIRMED · READ | `memory_ppc.c:273-276`, `:299-300`, `:315-323` | BRIEF PREMISE: FAULT is available on PPC (the DSI machinery is in this function) |
| F4 | grok | ppcfmasingle cites `OUTSTANDING_BUGS.md:1705`/`:1712` with no pin; at HEAD the twelve-encodings header is `:1708` and the fmadds/fmsubs bullet `:1715` | CONFIRMED · READ | `ledger.json:56337`; `OUTSTANDING_BUGS.md:1708`, `:1715` | RECORD CORRECTION: `:1705, :1712` -> `:1708, :1715` (or pin "at 1202d342") |
| F5 | grok | the L4 rider `DISPOSITIONS.md:26-27`'s `:1610`/`:1712`/`:3085` drifted; `:1612` still points fnmadd/fnmsub at `ppc_halt_probe.py:260` (now a comment) | CONFIRMED · READ | `OUTSTANDING_BUGS.md:1612`, `:1618` (#555 "THIS IS NO LONGER OPEN"), `:3096-3099` (#555 correction) | none: already corrected in place by #555 |
| F6 | grok | fnmadds/fnmsubs have no in-tree encoding, so "they stop at `:5218`" is not established | REFUTED · READ | `_scratchpad/ppc_uisa_book1_v201.txt:11759` "59 30 ... fnmsubs", `:11761` "59 31 ... fnmadds"; `src/cpus/cpu_ppc_instr.c:5197-5218` (`xo & 31` handles 18/20/21/25 only) | BRIEF PREMISE: cite Book I :11759-11761 |
| F7 | grok | ppcfmasingle's and ppcllscrcexit's `state_note`s open with the tail of the PREVIOUS row's disposition.  Measured here as SYSTEMIC: of 221 rows carrying "GOVERNING TEXT (from the dispositions file, cut at 400 characters): ", 117 do not name their own id in the window's first 60 characters, 41 carry their own "* \`id\`" bullet mid-window, and 37 never name their own id (arcsgiprivate keeps only its verdict token) | CONFIRMED · READ | `ledger.json:56344`, `:56586`, `:58742`, `:57466`, `:57246`.  Deriver: python json over `git show e483d931:tools/pipeline/ledger.json`, rows whose `state_note` holds that prefix, own-id offset within the window | FILE: new records-tooling row (#554's filer, 1202d342: the window should start at the row's own disposition).  No row exists: ledger titles and OUTSTANDING_BUGS greps for "cut at 400" / "GOVERNING TEXT" give 0 hits |
| F8 | grok | ppcfmasingle and qhppcdecode share the opcode-59 site `:5216-5218`.  qhppcdecode's ten names span two sites: fmadds/fmsubs/fsqrts/fres at `:5218` (opcode 59) and fctid/fctidz/fcfid/fcmpo/fsqrt/frsqrte at `:5410` (opcode 63).  The governing amendment `IDLESS_DISPOSITIONS.md:92` assigns fmadds/fmsubs to ppcfmasingle ("do not double-file") | CONFIRMED · READ | `ledger.json:61318`, `:56337`; disk:`regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md:41`, `:92`; `cpu_ppc_instr.c:5216-5218`, `:5410` | RECORD CORRECTION: qhppcdecode title -> eight encodings (drop fmadds/fmsubs, cross-ref ppcfmasingle).  Ruling owed: is the opcode-59 hole one round? |
| F9 | grok | `OUTSTANDING_BUGS.md:1708`/`:1715` still say twelve encodings halt, fnmadd/fnmsub included; they are decoded since #344.  The gate comment carries its #556 correction; this paragraph has none | CONFIRMED · READ | `OUTSTANDING_BUGS.md:1708`, `:1715` (no correction through `:1724`); `cpu_ppc_instr.c:5263-5269`; `regress/ppc_halt_probe.py:278-279` "FIXED"; `regress/gate_ppc_halt.sh:42-44` | RECORD CORRECTION: append a #556-style correction at `OUTSTANDING_BUGS.md:1708` ("ten"; fnmadd/fnmsub fixed by #344) |
| F10 | grok | qhppciphack's title misplaces the mechanism: MSR.IP does select 0xfff00000 in `ppc_exception`; the stop is the reboot hack on ANY MSR write with IP set (`running = 0`, no exit) | CONFIRMED · READ | `src/cpus/cpu_ppc.c:288-292`, `:337-339`; `src/include/cpu_ppc.h:171` | RECORD CORRECTION: title -> "writing MSR with IP set stops the CPU (NetBSD/prep reboot hack, cpu_ppc.c:288-292)" |
| F11 | grok | the IP stop is reachable from rfi (SRR1 low 16 bits), rfid (its mask includes bit 6), mtmsr, and wrteei once IP is set | CONFIRMED · READ | `cpu_ppc_instr.c:2835-2838`, `:2845-2850`, `:2905`, `:2930-2932` | BRIEF PREMISE |
| F12 | grok | qhslowifetch's PPC `exit(1)` (with `goto bad` commented out) is the directory's outlier: sh/m88k (and alpha/i960/riscv per grok) `goto bad`, and ARM returns | CONFIRMED · READ | `cpu_ppc_instr.c:4115-4120`; `src/cpus/cpu_sh_instr.c:4055-4056`; `src/cpus/cpu_m88k_instr.c:2991-2992` | BRIEF PREMISE: the house idiom is `goto bad` |
| F13 | grok | `OUTSTANDING_BUGS.md:24135` maps prose 2614-2615 to armthumbabortkill only (the PPC half is the #555 row qhslowifetch); `:24136` maps 2616 to m88kexit only (qhppciphack and qhm88kstops also claim 2616) | CONFIRMED · READ | `OUTSTANDING_BUGS.md:24135-24136`, `:23888-23892`, `:23906-23907` | RECORD CORRECTION: add the three "(a #555 row above)" ids to :24135/:24136.  The table at `:24108` promises "the id or ids" per passage.  The three #558 MB89352 rows also come from passage 2616 (`ledger.json:61391`, `:61413`) and were filed after the table |
| F14 | grok | no regress probe or gate reaches ppcbatppkill, ppcllscrcexit, qhppciphack or qhslowifetch (only `ppc_halt_probe.py`'s PEND rows reach the decode sites) | CONFIRMED · READ | `git grep BAT exception\|ppc_bat\|lwarx\|stwcx\|llsc\|MSR_IP\|Reboot hack\|read failed: TODO\|<ids>` e483d931 `regress/*.py regress/gate_*.sh`: 0 | BRIEF PREMISE: witnesses are new |

Counts (ppc_six): DISPOSED 0 · CONFIRMED 11 (FILE 1, RECORD 5, BRIEF 4, already-corrected 1) · REFUTED 3 · CANNOT
SETTLE 0 · total 14.

## sh_two

Seats: grok 21,289 b · grok-rec none · Argon not yet · agy not landed.  Rows: `shifetchkill`, `shreservedexit`.  The
working tree's dirty `dev_sh4.c` was not read.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok | the rows are two predicates in one function: a privileged FLAG_INSTR fetch >= 0xe4000000 exits at `:379-381`; privileged data in [0xe4000000, 0xefffffff] exits at `:398-400` | CONFIRMED · READ | `src/cpus/memory_sh.c:379-381`, `:385-387`, `:398-400` | BRIEF PREMISE: two sites, not one defect |
| F2 | grok | shifetchkill's reach "VBR +0x100 / +0x600" is incomplete: TLB miss enters at VBR+0x400; resets go to 0xa0000000 with VBR=0; BL set forces RESET_POWER; an unknown EXPEVT exits before the fetch | CONFIRMED · READ | `src/cpus/cpu_sh.c:955`, `:962`, `:1023-1025`, `:1015-1021`, `:910-917`, `:1083-1085` | BRIEF PREMISE: name +0x400 and every PC-setting branch as routes |
| F3 | grok | prose `OUTSTANDING_BUGS.md:8196` (= db8b1a33:8148, pinned by shreservedexit) cites `memory_sh.c:358-364` for the hole exit; at HEAD that is the user branch, and the exit is `:398-400` | CONFIRMED · READ | `OUTSTANDING_BUGS.md:8196`; `memory_sh.c:359-371` vs `:398-400` | RECORD CORRECTION: `:8196` `:358-364` -> `:398-400` (fetch `:379-381`).  Leave the seat artifact `grok_ititles.txt:33` (`:365-400`) as is |
| F4 | grok | shreservedexit's title omits that a FLAG_NOEXCEPTIONS lookup returns paddr 0; only accesses without NO_EXCEPTIONS die | CONFIRMED · READ | `memory_sh.c:390-392`; `src/cpus/memory_rw.c:241`, `:248-252` | BRIEF PREMISE |
| F5 | grok | the prose's manual quotes "Reserved area" / "Operation is not guaranteed" cannot be checked | REFUTED · READ | `_scratchpad/sh7750_hardware.txt:8757` "Operation is not guaranteed if an area designated as a reserved area ..."; `:9015` "H'E400 0000 Reserved area" | BRIEF PREMISE: cite those two manual lines |
| F6 | grok | `IDLESS_DISPOSITIONS.md:406` bundles the fetch into shreservedexit; `:428` (governing per `:12-13`) limits it to data; a brief citing :406 re-merges the rows | CONFIRMED · READ | disk:`regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md:12-13`, `:406`, `:428` | BRIEF PREMISE: cite :428 |
| F7 | grok | `regress/sh_halt_probe.py:421` "P4 is direct-mapped (memory_sh.c:373-377)" cites the P1/P2 block; P4 is `:384-387` | CONFIRMED · READ | `regress/sh_halt_probe.py:421`; `memory_sh.c:373-377`, `:384-387` | RECORD CORRECTION: the probe comment `:373-377` -> `:384-387` |
| F8 | grok | the check file's "nothing can install a host page for the range" (`fable_batch3d.md:50`) is not fully verified | CONFIRMED · REASONED | `memory_rw.c:663` (`paddr >= mem->physical_max`: no install), `:745` (`&& !no_exceptions`); `src/devices/dev_sh4.c`: 0 `DM_DYNTRANS_OK` | BRIEF PREMISE: every cold privileged fetch of the range reaches `:379` |

Counts (sh_two): DISPOSED 0 · CONFIRMED 7 (RECORD 2, BRIEF 5) · REFUTED 1 · CANNOT SETTLE 0 · total 8.

## mips_two

Seats: grok 24,944 b · grok-rec none · Argon not yet · agy not landed.  Rows: `mipscop0tail`, `mipsresetalias`.  They are
two defects: a decode-time `goto bad` vs an execute-time `X(reboot)`.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok | neither title nor its governing sentence carries a source path:line; the cites live only in `fable_batch3b.md:54-56` / `:69-73` | CONFIRMED · READ | `ledger.json:57811`, `:57833`; `OUTSTANDING_BUGS.md:22916`, `:22919` | BRIEF PREMISE: cite `src/cpus/cpu_mips_instr.c:4918-4928`, `:5008-5027`, `:4666-4669` |
| F2 | grok | "EI/DI off-R5900" is a `goto bad` only for COP0 fn 0x38/0x39 (CO set) off-R5900; MIPS32r2 EI/DI (MFMCz 0x6000) installs `reserved` or `ei_or_di` | CONFIRMED · READ | `cpu_mips_instr.c:4918-4928`, `:4981-5007` | RECORD CORRECTION: `ledger.json:57811` -> "R5900 EI/DI (COP0 fn 0x38/0x39) on non-R5900 CPUs" |
| F3 | grok | `goto bad` does not stop the CPU during translation readahead | CONFIRMED · READ | `src/cpus/cpu_dyntrans.c:1990-1991`, `:2014` | BRIEF PREMISE: the stop is on execution |
| F4 | grok | "stops the emulator" means one CPU's `running = false`, with no exit; the run continues while another CPU runs | CONFIRMED · READ | `cpu_mips_instr.c:2617`; `src/machines/machine.c:742-746`; `src/debugger/debugger.c:72` | BRIEF PREMISE (both rows): a CPU stop, which ends emulation on a single-CPU machine |
| F5 | grok | the #235 comment and CHANGELOG say ordinary RAM takes BP, but the mask installs reboot at every VA whose bits 28:0 are 0x1fc00000 (kuseg TLB aliases included) | CONFIRMED · READ | `cpu_mips_instr.c:4663-4667`; `CHANGELOG.md:21312-21313` | already filed: mipsresetalias (correct the #235 comment when fixed) |
| F6 | grok | the ruling's cites drifted: `OUTSTANDING_BUGS.md:2604-2605`->`:2612-2613`, `:2668-2671`->`:2676-2679`, `:2601-2619`->header `:2609`/"~5 remain" `:2620`, `CHANGELOG.md:20236-20238`->`:21311-21313` | CONFIRMED · READ | `OUTSTANDING_BUGS.md:2612-2613`, `:2676-2677`; `CHANGELOG.md:21311-21313`; correct at the pins: `8ea26abb:OUTSTANDING_BUGS.md:2604-2605`, `db8b1a33:CHANGELOG.md:20236-20238` | BRIEF PREMISE: cite HEAD lines.  No record correction (the ruling pins 8ea26abb, `fable_batch3b.md:8-14`) |
| F7 | grok | `fable_batch3b.md:79` "all say phys": the CHANGELOG #235 paragraph never says phys | CONFIRMED · READ | `CHANGELOG.md:21311-21313`; "phys" only at `OUTSTANDING_BUGS.md:2613`, "physical" at `cpu_mips_instr.c:4662` | none (artifact wording; the intent stands) |
| F8 | grok | the entry note's `[087a90]` does not resolve as a git revision | REFUTED · READ | `ledger.json:57827` "Filed by GXEMUL [087a90] (main loop)": a session tag | none |
| F9 | grok | `mips_r4000.txt:1150/1154/1158` cannot be checked (no such file in git) | REFUTED · READ | `_scratchpad/mips_r4000.txt:1150` Breakpoint, `:1154` Reserved Instruction, `:1158` Coprocessor Unusable | BRIEF PREMISE: cite those three lines |
| F10 | grok (sibling note; the exit is this prescreen's reading) | `syscall 0x30378` installs promemul at any PC and mode, and X(promemul)'s default is `fatal` + `exit(1)` for machine types with no PROM layer: testmips, cobalt, hpcmips, algor | CONFIRMED · READ | `cpu_mips_instr.c:4650-4656`, `:2635-2651` "Unimplemented machine type for PROM magic trap"; `src/include/machine.h:228-236`; ledger/OUTSTANDING_BUGS grep "magic trap"/"promemul": no row | FILE: new, HIGH candidate (a guest syscall exits the host).  Witness: rung 3 `-E testmips`, iword 0x00C0DE0C |
| F11 | grok (sibling note) | X(ei_or_di), MIPS32r2 EI/DI, never calls `cop0_availability_check`, while the manual requires CpU when CP0 is unusable | CONFIRMED · READ | `cpu_mips_instr.c:2719-2726` (vs `:2614`, `:3241`); `_scratchpad/mips32_volII.txt:597`, `:630` "a Coprocessor Unusable Exception is signaled"; ledger grep `ei_or_di`: 0 | FILE: new, MED (a wrong exception: user-mode EI/DI writes Status.IE) |
| F12 | grok | no regress probe or gate names either decoder path | CONFIRMED · READ | `git grep 0x30378\|1fc00000\|COP0_EI\|MFMCz\|ei_r5900\|<ids>` e483d931 `regress/*.py regress/gate_*.sh`: 0 | BRIEF PREMISE: witnesses are new |

Counts (mips_two): DISPOSED 0 · CONFIRMED 10 (FILE 2, RECORD 1, BRIEF 5, already-filed 1, none 1) · REFUTED 2 · CANNOT
SETTLE 0 · total 12.

---

## Noticed while checking (no seat raised these; each was verified here)

| N | found by | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| N1 | this prescreen (mb89352 F4) | the `len != 1` diagnostic's format has three conversions and two arguments: undefined behaviour on every non-byte MB89352 access, reachable by the guest; `debugmsg_cpu` has no format attribute | CONFIRMED · READ | `src/devices/dev_mb89352.c:305-309` "unimplemented LEN: %i-bit access, address 0x%x: 0x%x" (args: `len * 8`, `relative_addr`); `src/include/misc.h:270`; ledger/OUTSTANDING_BUGS grep of the format text: 0 | FILE (LOW), or fold into the qhmbunimplstops round (same site `:304-313`) |
| N2 | armdesc3kill sub-agent; **[spot-checked]** | a coarse-L2 type-3 entry is treated as a 1 KB tiny page on non-XScale cores, but DDI 0100I makes coarse 0b11 an extended small page and allows tiny pages only in fine tables | CONFIRMED · READ | `src/cpus/memory_arm.c:198-207`; `_scratchpad/ddi0100i.txt:29574`, `:29801`; ledger/OUTSTANDING_BUGS grep "tiny page": 0 | FILE candidate (ARM walker fidelity); brief it with armdesc3kill's IMPLEMENT member |
| N3 | this prescreen (apparatus) | 3 of the 7 Argon banks (armexits_db8b1a33, excvecrecurse_prep, arcbios_three) still record `transport=manual (owner pasted)` in `gemini_web.argv`, the default the other four mark "CORRECTED 2026-10-16" | CONFIRMED · READ | `_scratchpad/gweb/jobs_20261014_argonpack6/{armexits_db8b1a33,excvecrecurse_prep,arcbios_three}/gemini_web.argv:1` | RECORD CORRECTION (gweb bank, not the queue) |

Checked and dropped:
- `ESC[row;colH` leaves the ROW unclamped too (`arcbios.c:212-219`).  But `scroll_if_necessary()` runs after every
  character (`:377`) and resets `console_cury` to `maxy-1` (`:297-298`), so only the column (arccursorbound) is
  unbounded.
- The armmmuvehicle sub-agent flagged as unraised the point that a barearm c1 read-modify-write exits.  The seats DID
  raise it, as armexits F5 (grok, grok-rec, Argon), so it is counted there and not here.

## CONFIRMED and CANNOT SETTLE items for the adjudicators

Grouped by what each item becomes.  Every item names its job and F#; the evidence is in that job's table.

### A. FILE: new rows (each grep found no existing row)
1. **ppc_six F7: the ledger's "GOVERNING TEXT (... cut at 400 characters)" window is misaligned, and the fault is
   systemic.**  Of the 221 rows that carry it, 117 do not name their own id in the window's first 60 characters, 41 carry
   their own `* \`id\`` bullet mid-window, and 37 never name their own id.  This is a records-tooling row against
   #554's filer (1202d342).  Instances in this group: ppcfmasingle, ppcllscrcexit, ascwidecount (ascwidecount F1),
   mboutcapacity (mb89352 F8), arcsgiprivate (arcbios F15), and armendianexit, xscalecp6exits and alphatinyzero
   (armexits F23).
2. **mips_two F10 (HIGH candidate):** `syscall 0x30378` at any PC and mode installs promemul.  On testmips, cobalt,
   hpcmips and algor, X(promemul)'s default calls `fatal` + `exit(1)` (`cpu_mips_instr.c:2649-2650`).  The arm has no
   CU0 or mode check.  On pmax, arc, sgi, evbmips and ps2 the same word reaches PROM emulation from user mode at any PC:
   the address-gate shape that #235 fixed for BREAK, still open for SYSCALL.  Witness: rung 3 `-E testmips`, iword
   0x00C0DE0C.
3. **ascwidecount F6 (HIGH candidate):** in ASC COMMAND-phase DMA, a wide TCL/TCM store narrows to a negative `int
   len`.  `scsi_transfer_allocbuf` then asks for about 2^64 bytes, and its OOM arm calls `exit(1)`
   (`dev_asc.c:987-992`; `diskimage_scsicmd.c:147-155`).  pmax OpenBSD reaches SELATN|DMA on every command.
4. **mips_two F11 (MED):** X(ei_or_di), the MIPS32r2 EI/DI, never calls `cop0_availability_check`.  User mode can
   write Status.IE where the manual says CpU (`mips32_volII.txt:597`, `:630`).
5. **armdesc3kill F17:** the ARM walker masks the TTB and L2-table physical addresses with `0x0fffffff`.  Tables above
   256 MB are read from the wrong place (rpi defaults to 512 MB).
6. **armmmuvehicle F19 (LOW):** the coarse-table domain fault is raised before the L2 fetch: FSR 0x3b where DDI 0100I
   gives 0x37 for an invalid L2 entry.
7. **armthumbabortkill F8:** Thumb LDR(3) passes CACHE_INSTRUCTION, so it raises a Prefetch Abort with no FAR/FSR.  The
   manual says Data Abort.  It is a sibling row of armthumbabortkill.  Then mark `ledger.json:48071`'s "UNVERIFIED"
   candidate verified.
8. **armexits F20 (MED), `armcp15c1fallthrough`:** a c1 store with opcode2 outside {0,1} prints a fatal and falls
   through into the control write (`cpu_arm_coproc.c:124-135`).  An ARMv6 CPACR write (rpi's ARM1136JSR1) overwrites
   control and can reach armendianexit's `exit(1)`.  It was proposed at `DISPOSITIONS.md:195-197`, excluded as
   contingent, and never filed.
9. **(noticed) N1 (LOW):** MB89352's `len != 1` diagnostic has three format conversions for two arguments; or fold it
   into the qhmbunimplstops round.
10. **(noticed) N2:** a coarse-L2 type 3 is treated as a 1 KB tiny page on non-XScale cores, against DDI 0100I.

### B. ADD TO an existing row
- armvecrecurse F13 -> **excvecrecurse**: add its PPC and M88K legs (both read, not measured).
- armthumbabortkill F6 -> **armthumbabortkill**: a Thumb POP-without-PC or PUSH that aborts resumes at vector+2.
- armthumbabortkill F10 -> **armthumbabtlr**: Thumb SWI/UND save LR = instr+3 (the manual says +2).
- armthumbabortkill F12 -> **armspsrthumb**: the LDM^/SPSR T-with-even-PC path ends at the `cpu_arm.c:1269` halt.
- armthumbabortkill F13 -> **armdacr2kill**: a bare delete gives full access, and `return 0` gives a permission fault,
  not a domain fault.
- armthumbabortkill F14 -> **armdesc3kill**: a bare delete gives fs=2 (terminal exception); FAULT must set
  FAULT_TRANS_S.
- armdesc3kill F18 -> **subpagecache** (consider): the pc-relative literal fold assumes 4 KB pages; it is a BRIEF
  PREMISE for IMPLEMENT.
- arcbios_three F14 -> **arcsgiprivate**: 64-bit SGI private calls are mis-routed, because `arcbios_sgi_emul` never
  halves the vector (`arcbios.c:1180` vs `:1285-1286`).  Slot i dispatches as 32-bit slot 2i.
- armexits F13 -> **armmrcr15flags**: CP14 has the same MRC-to-r15 shape as CP6.  Cross-reference
  armcp15cp14exits `:62`.

### C. RECORD CORRECTIONS (L4; the record and the corrected text are in each row)
- **armvecrecurse / excvecrecurse, one defect filed twice:**
  - excvec F1: cross-reference the two rows; it is one round.
  - excvec F2: `ledger.json:52075` `cpu_arm.c:731-733` -> `:780-783`.
  - excvec F5: "Witness (Opus)" -> "Predicted".
  - excvec F6: SH is bounded; M88K only when SAPR.V is set.
  - armvec F3 / excvec F12: 47,591 = 1 data abort + 47,590 nested; warnings uncounted.
  - armvec F4: 10.6 s is the whole driver run.
  - armvec F5 / excvec F13: the transcript was never kept.
  - armvec F2: the `T3_vec_unmapped.excerpt.txt:1` header mislabels its parent.
- armmmuvehicle F6: `ledger.json:62253`, `OUTSTANDING_BUGS.md:24523-24524`: unmapped vectors recurse (armvecrecurse);
  they do not reach the cpu_dyntrans exit.
- armmmuvehicle F30: `ledger.json:48116` `:1808 default:` -> `:1858`.  (`:48071` is covered by the queued "+42" ->
  "+50".)
- armmmuvehicle F15, F23, F24: agy's harvested flags at `HARVEST_AUTO.md:179`, `:186` and `:187-195` are wrong:
  debugger invalidation is conditional, the walk line numbers are off, and `machine_new` is not `machine_create`.  Note
  this against agy's harvest.
- armthumbabortkill F3: `ledger.json:48066` "abort ALREADY DELIVERED" holds for MMU faults only.
- armdesc3kill:
  - F2: `OUTSTANDING_BUGS.md:22132` -> "the first MMU-on walk that fetches a type-3 L1 entry".
  - F4: cite `ddi0100i.txt:29760-29763` (RESERVED in VMSAv6, `:29371-29372`).
  - F10: cite `fbd5 p1_findings.md:35-39` / `FABLE_P1_ANSWER.md:41`.
  - F11: "arm T = `regress/footbridge_sites_probe.py:211`".
- arcbios_three F2: "2^31" -> "2^31-1".  F12: `:1271` -> `:1271-1272`.
- ascwidecount F3: the title's negative len2 is an implementation-defined narrowing (gcc wraps).
- crimectllane:
  - F2: `ledger.json:56208` "of any width" -> "of the width that reaches it (4 or 8; others declined, #529)".
  - F3: `regress/crime_width_probe.py:59-60`: drop "or a halfword at +0x08".
- mb89352_five:
  - F2: qhm88kstops: add `dev_mb89352.c:143-147`.
  - F4: qhmbunimplstops: "any len != 1".
  - F5: b120's "reports 0x00 GOOD" vs qhmbbufendstops: name which row owns the MB89352 `:176` empty-status stop.
  - F9: mboutcapacity: add the MODE SELECT rider (`diskimage_scsicmd.c:1287-1291`).
  - F12: `dev_mb89352.c:443-446` stale `diskimage_scsicmd.c:778/:788` -> the `data_out_offset != size` anchor (`:888`).
- m88k_four F5: m88kfpr0stop: "arithmetic/convert/compare (8 sites)".  F11: m88kpsrbokill: add xcr.
- ppc_six:
  - F4: ppcfmasingle `:1705, :1712` -> `:1708, :1715`.
  - F8: qhppcdecode -> eight encodings, per `IDLESS_DISPOSITIONS.md:92`.  **Ruling owed:** is the opcode-59 hole (with
    ppcfmasingle) one round?
  - F9: `OUTSTANDING_BUGS.md:1708`/`:1715` still say "twelve" with fnmadd/fnmsub; append the #556-style correction.
  - F10: qhppciphack: the stop is ANY MSR write with IP set (`cpu_ppc.c:288-292`); vector selection works.
  - F13: `OUTSTANDING_BUGS.md:24135`/`:24136` omit the #555 rows qhslowifetch, qhppciphack and qhm88kstops.
- sh_two F3: `OUTSTANDING_BUGS.md:8196` `memory_sh.c:358-364` -> `:398-400`.  F7: `regress/sh_halt_probe.py:421`
  `:373-377` -> `:384-387`.
- mips_two F2: mipscop0tail -> "R5900 EI/DI (COP0 fn 0x38/0x39) on non-R5900 CPUs".
- armexits_db8b1a33:
  - F1: `OUTSTANDING_BUGS.md:22878` + `ledger.json:56564` -> "18721-18722 at db8b1a33 (HEAD :18773-18774)".
  - F2: prose cpu_arm.c cites +50 (pin to db8b1a33, or re-key).
  - F3: `OUTSTANDING_BUGS.md:18740`'s "isteer carries no fatal() and no exit()" is false (`cpu_arm_coproc.c:319-322`).
  - F5: "toggles the B bit" -> "writes a B bit unequal to (byte_order == BE)".  On barearm a B-preserving c1 RMW dies.
  - F6: `DISPOSITIONS.md:138-139` (quoted at `ledger.json:56564`): a bare deletion keeps byte_order; implementing the
    switch breaks the premise.
  - F9: the xscalecp6exits title has "other three siblings" where there are four.
  - F22: `regress/arm_flags_probe.py:871` cr7 cite -> `:221-228`.
- (noticed) N3: three Argon `gemini_web.argv` files record the uncorrected transport.

### D. BRIEF PREMISES: facts each future round's brief must state (details in the tables)
- **armvecrecurse / excvecrecurse:**
  - armvec F1 (artifacts tracked), F6/excvec F14 (cold-debugger rung 3, the command line), F7/excvec F16 (needs a cold
    vector page: c8 after planting).
  - armvec F9/excvec F18 (cite the call chain), F10/excvec F4 (h:29 macro), F11/excvec F10 (nesting is normal).
  - armvec F14/excvec F17 (no probe; the vehicle is armmmuvehicle), F15 (queue order).
  - excvec F3 (`OUTSTANDING_BUGS.md:22014`), F7 (the PPC leg is read, and needs the guest to reprogram the IBATs), F9
    (MIPS immune, Alpha = alphaifetchkill), F15 (the warning prints under -q).
- **armmmuvehicle:**
  - F7 (cats boots MMU-on and cannot fault), F8 (c8 after M), F10 (the six-word sequence decodes; it was already run),
    F11 (the command needs a load argument).
  - F12 (`arm_msrmode_probe.py` committed at 4f908ad5), F13 (`put h`/`w`/`d` warm the translation; `b`/`s`/`z`/`dump`
    do not), F14 (`dump` cannot pin c8).
  - F16 (the first guest-ARMED MMU vehicle; four cats probes already run MMU-on), F17 (the L2 table sits inside the L1),
    F18 (three walk edits pass the pass-1 rows).
  - F20 (ARM_NO_MMU is never read), F21 (no debugger CP15 writer), F22 (what c8 clears).
  - F25 (read pass 1 with `git show`), F26 (+109 inline numbering), F27 (uncited premises; seat failures).
- **armthumbabortkill:**
  - F4 (testarm devices: path (a) is impossible, (b) is possible), F5 (what happens to the fatal is OPEN), F7 (`:1277` is
    reached only via a stale warm entry).
  - F16 (`cpu_arm_instr.c:72` is compiled out), F17 (`cpu_arm.c:736` is host-only), F18 (house idiom: the `mode_warned`
    bits).
  - F19, F20 (line and function citations), F21 (the SA1110 Thumb question is settled), F22 (nine ARM setups; five boot
    MMU-on), F23 (the "could not load" wording on stores).
- **armdesc3kill:**
  - F5 (type 3 is legal pre-VMSAv6), F6 (a fine table = 1 KB entries mapping 64 K/4 K/1 K pages), F7 (it depends on
    architecture level; RESERVED in v6, PXN/Translation in v7).
  - F8 (quote `domain = 0`), F12 (rung-3 attempt owed; cats suffices), F13 (the arm-T probes reach the walker), F14
    (NOEXCEPTIONS and debugger callers die too).
  - F15 (member 5 lands; the second hazard is alphaifetchkill), F16 (a NULL L1 page is case 0), F19 (outlier, #238
    precedent), F20 (HEAD lines).
- **arcbios_three:**
  - F1 (cite sites), F3 (signed overflow at x >= 2^30), F4 (only `ESC[K`/`ESC[0K`/`ESC[1K` walk), F7 (two twin malloc
    sites), F8 (DEC's `(int32_t)A2 > 0` idiom).
  - F10 (A2 = 0 is the only zero case), F11 (cross-ref dectxzero `:22895`), F13 (EINVAL is the house idiom), F14 (witness
    vectors; 64-bit SGI slots), F18 (no probe).
  - F6 (as a note: the tab arithmetic overflows at curx >= 2147483641).
- **ascwidecount:** F2 (cite the sites), F4 (the witness needs TCM 0, or wide values with sum >= 0x80000000), F5 (three
  rows, one store path), F7 (no probe).
- **crimectllane:** F1 (cite the sites), F4 (the NetBSD +0x0c write is unwitnessed), F6 (the default arm's log shows only
  when stepping or with -v), F7 (exact-label switches in 3 of 4 handlers), F8 (CONTROL never holds a written value).
- **mb89352_five:**
  - F1 (TC != 0 needed), F3 (the write twin declines), F6 (cursor resets only at SELECT/XFR; a second empty-buffer route).
  - F7 (the 16/512 numbers are examples), F10 (the NULL-store witness sequence), F11 (b120's "round UP" clause is not
    evidence), F13 (no probe).
- **m88k_four:**
  - F1 (two predicates, one block), F2 (cite `mc88100.txt:1633`, `:2002`, `:3523-3525`, `:5189-5191`, `:5676-5678`),
    F3 (the trnc.sd message prints d), F4 (readahead).
  - F6 (the m88kfpr0stop fix depends on m88kexcsfu1), F7/F8 (cite amendment `DISPOSITIONS.md:553`, not the riders), F9
    (the flipped PSR is never stored), F10 (rte's deferred stop), F13 (no probe).
- **ppc_six:**
  - F2 (cite `ppc_pem32_rev2_2001.txt:13312` + `:13503-13519`), F3 (FAULT is available: DSI/ISI with DSISR_PROTECT), F6
    (cite Book I `:11759-11761`).
  - F11 (rfi/rfid/mtmsr/wrteei reach the IP stop), F12 (`goto bad` is the house idiom for a failed ifetch), F14 (no probe).
- **sh_two:**
  - F1 (two sites), F2 (VBR +0x400 and every PC-setting branch), F4 (NOEXCEPTIONS returns), F5 (cite
    `sh7750_hardware.txt:8757`, `:9015`).
  - F6 (cite `IDLESS_DISPOSITIONS.md:428`, not `:406`), F8 (no warm page can bypass `:379`).
- **mips_two:** F1 (cite the sites), F3 (readahead), F4 (a one-CPU stop), F6 (cite HEAD lines), F9 (cite
  `mips_r4000.txt:1150`/`:1154`/`:1158`), F12 (no probe).
- **armexits_db8b1a33:**
  - F7 (apply `DISPOSITIONS.md:350-351`'s unapplied L4 on the #378 comment), F8 (no runtime byte_order writer), F11 (an
    id bundle, not a round; cross-reference :417/:528), F12 (:62 pre-empts :177/:264 when rd=15).
  - F14 (install condition per site: CP15 all, CP14 ARM_XSCALE, CP6 iq80321/iyonix), **F15 (gate 14's
    `xscale_inten_probe.py` rows E_UNKNOWN/S_ISRC_WR/SIB_WRITE assert the three CP6 deaths: the fix round re-pins them
    FIRST)**, F16 (no probe reaches :62/:177/:264/:528), F17 (four exits sit after their stores).
  - F18 (census + #562's latch idiom `cpu_arm.c:585-600`), F19 (m88kpsrbokill sibling), F21 (the armmmuvehicle c1 MCR
    keeps B == byte_order and rd != 15), F28 (spans).

### E. Already filed: no new action
- armvecrecurse F17 (`put h`, already on armmmuvehicle at `ledger.json:62335`).
- armvecrecurse F18 and armthumbabortkill F9 (armthumbabtlr).
- armthumbabortkill F11 (cpusexitsweep).
- armthumbabortkill F15 and armdesc3kill F15 (armvecrecurse / alphaifetchkill).
- excvecrecurse F9, Alpha leg (alphaifetchkill).
- mips_two F5 (mipsresetalias; correct the #235 comment when it is fixed).
- armdesc3kill F9 (already corrected at `ledger.json:52227`).
- ppc_six F5 (already corrected in place by #555 at `OUTSTANDING_BUGS.md:1618`, `:3098-3099`).
- armexits F14 (the NULL-coprocessor branch: armcpabsent) and F19 (the m88k PSR sibling: m88kpsrbokill).

### F. CANNOT SETTLE (and the one read or run that would settle each)
- arcbios_three F9: does `malloc(0)` return NULL on the build host's libc?  One C one-liner under WSL Gentoo.  glibc is
  expected to return non-NULL, which makes arczeroalloc's HIGH the real question.
- armmmuvehicle F28: re-run `opus5_meas/meas3.py.txt`'s vector-unmapped session on an e483d931 build (the pass-1 counts
  were not re-measured at HEAD).
- excvecrecurse F11 (sub-question; the row itself is CONFIRMED): is signal 11 stack exhaustion?  One backtraced meas3
  rerun.
- armexits_db8b1a33: none.

### G. PACKET (one line, no round action)
All seven banked Argon jobs carry a bundle-gap row (armvec F19, armmmu F31, armthumb F24, armdesc3 F21, excvec F19,
arcbios F19, plus armexits).  The bundle builder skips `src`, `src/cpus`, `regress` and `regress/artifacts` as "too
broad" and reports `regress/*.py` / `regress/gate_*.sh` as NOT FOUND: globs are not expanded.  So every prep packet
lacked the regress grep its brief asks for.  Every underlying question was settled from the tree by grok or by this
prescreen.  This is a note for the packet builder.

The seven queued Argon packets have the same gaps: ascwidecount, crimectllane, mb89352_five, m88k_four, ppc_six, sh_two
and mips_two.  Each `argon_bundle.manifest` shows `NOT FOUND regress/*.py` and `NOT FOUND regress/gate_*.sh`, so when
those answers bank they will carry the same flags.  Each of those jobs' "no probe or gate" row above already settles
the question.

## Counts

One row per distinct finding.  Each row has exactly one category.  The breakdown columns split CONFIRMED by what the
finding becomes.  "RECORD" includes AGY-FLAG-WRONG.  "already" includes already-corrected records.

| job | DISPOSED | CONFIRMED | REFUTED | CANNOT SETTLE | total | CONFIRMED -> FILE-new / ADD-TO / already / RECORD / BRIEF / PACKET / none |
|---|---|---|---|---|---|---|
| armvecrecurse_prep | 0 | 14 | 5 | 0 | 19 | 0 / 1 / 2 / 3 / 7 / 1 / 0 |
| armmmuvehicle_prep | 5 | 23 | 2 | 1 | 31 | 1 / 0 / 0 / 5 / 16 / 1 / 0 |
| armthumbabortkill_prep | 2 | 22 | 1 | 0 | 25 | 1 / 5 / 3 / 1 / 11 / 1 / 0 |
| armdesc3kill_prep | 1 | 17 | 4 | 0 | 22 | 1 / 0 / 1 / 4 / 10 / 1 / 0 |
| armexits_db8b1a33 | 0 | 23 | 6 | 0 | 29 | 2* / 1 / 0 / 7 / 12 / 1 / 0 |
| excvecrecurse_prep | 0 | 15 | 4 | 0 | 19 | 0 / 0 / 0 / 6 / 8 / 1 / 0 |
| arcbios_three | 0 | 15 | 3 | 1 | 19 | 1* / 1 / 0 / 2 / 9 / 1 / 1 |
| ascwidecount_prep | 0 | 7 | 0 | 0 | 7 | 2* / 0 / 0 / 1 / 4 / 0 / 0 |
| crimectllane_prep | 0 | 6 | 2 | 0 | 8 | 0 / 0 / 0 / 2 / 4 / 0 / 0 |
| mb89352_five | 0 | 13 | 0 | 0 | 13 | 1* / 0 / 0 / 5 / 7 / 0 / 0 |
| m88k_four | 0 | 11 | 2 | 0 | 13 | 0 / 0 / 0 / 2 / 9 / 0 / 0 |
| ppc_six | 0 | 11 | 3 | 0 | 14 | 1 / 0 / 1 / 5 / 4 / 0 / 0 |
| sh_two | 0 | 7 | 1 | 0 | 8 | 0 / 0 / 0 / 2 / 5 / 0 / 0 |
| mips_two | 0 | 10 | 2 | 0 | 12 | 2 / 0 / 1 / 1 / 5 / 0 / 1 |
| **TOTAL (14 jobs)** | **8** | **194** | **35** | **2** | **239** | **12* / 8 / 8 / 46 / 111 / 7 / 2** |
| noticed while checking (N1-N3) | 0 | 3 | 0 | 0 | 3 | 2 / 0 / 0 / 1 / 0 / 0 / 0 |

`*` Five of the twelve FILE rows are one filing: the governing-text window defect (ppc_six F7, the filing itself, plus
its instances at armexits F23, arcbios F15, ascwidecount F1 and mb89352 F8).  So the seats raised **eight distinct new
rows**:
- the window defect;
- mips_two F10 `syscall 0x30378` exit (HIGH candidate);
- ascwidecount F6 COMMAND-DMA allocbuf exit (HIGH candidate);
- mips_two F11 ei_or_di CpU;
- armdesc3kill F17 TTB/L2 28-bit mask;
- armmmuvehicle F19 coarse domain order;
- armthumbabortkill F8 Thumb LDR(3) prefetch abort;
- armexits F20 `armcp15c1fallthrough`.

Two more are noticed candidates: N1 (the MB89352 format mismatch) and N2 (the coarse type-3 tiny page).  No
seat-raised finding was found already filed under another id except those in section E.

Deriver for the per-job columns: count the `| F<n> |` rows under each `## <job>` heading by the first word of the
category cell.  That count was re-run after the last edit: 239 rows, which matches the table.
