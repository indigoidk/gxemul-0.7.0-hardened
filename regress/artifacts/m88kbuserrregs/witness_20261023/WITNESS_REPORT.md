# m88kbuserrregs (T36) -- pre-fix reproduction, rung 3 -- 2026-10-23

**VERDICT: RED ON HEAD -- the symptom reproduced, both halves, on unmodified in-tree machines.**
`WITNESS_headbin.out`: `M88K_BUSERR_RESULT=16/24`, `M88K_BUSERR_CONTROL=OK`, `M88K_BUSERR_SYMPTOM=PRESENT 8/8`,
`M88K_BUSERR_RED=uld pfsr,uld pfar,ust pfsr,ust pfar,vme pfsr,vme pfar,luna route,luna pfar`, sentinel
`M88K_BUSERR_PROBE_DONE`.  The rig-shape run (`WITNESS_headbin_rig.out`) gives identical rows.

* **Generic refused-access arm** (`src/cpus/memory_rw.c:603-625`, MEM_M88K block `:614-623`), on `-E mvme88k -e
  mvme187`: a refused data load, a refused data store, and a refused load at a second refusing device each raise
  the data-access exception (vector 3, SXIP = the access, DMA0 = its address), and the data CMMU's PFSR and PFAR
  still hold the values the guest itself stored there before the access.
* **LUNA probe address** (`src/devices/dev_luna88k.c:624-627`), on `-E luna88k -e luna-88k`: the load at
  `0x3ffffff0` raises nothing and is served 0; PFSR is written (`0x00030000`), PFAR keeps the guest's stored value.

This is the reproduction only.  No product file was edited, no mutant was built, nothing was committed.

## Baseline and build receipts (named baseline: HEAD 66920157)

| check | result | artifact |
|---|---|---|
| HEAD | `66920157bbdd42349835695b3e813ce721f12132` | `baseline_check.out` |
| the three files the round will edit, HEAD blob vs GXEMUL-SEC working tree vs `build/` | all CLEAN: `memory_rw.c` 3d47dd66..., `dev_luna88k.c` 6ecc6908..., `dev_m8820x.c` 0d12cfaf... | `baseline_check.out` |
| the same three, scratch clone vs GXEMUL-SEC (WSL `cmp`) | all CLEAN | `build_base.out` |
| every git-tracked `src/` file outside `tools/est_divergence.txt`, `build/` vs GXEMUL-SEC | 498 of 499 identical; the one difference is `src/machines/.index`, a GENERATED file (`makeautomachine.sh` picks up a comment line from `machine_sgi.c`; the committed copy is stale) | `baseline_check.out` |
| GXEMUL-SEC working tree vs HEAD, tracked `src/` | 500 of 505 identical; 5 carry uncommitted peer work: `cpu_alpha_palcode.c`, `dev_lca.c`, `dev_pcc2.c`, `dev_sh4.c`, `mvme_pcctworeg.h` -- and `build/` carries them too | `baseline_check.out` |
| those 5 in the clone | REPLACED BY HEAD BLOBS before the build (two of them, `dev_pcc2.c` and `mvme_pcctworeg.h`, are on the mvme187 machine) | `headblobs_MD5.txt`, `build_base.out` (`HEAD-BLOB`) |
| the six declared divergence paths | left as `build/` has them (est-shaped: no ne2000 device, est's `machine_arc.c`/`dev_jazz.c`) -- the ARC/Jazz/ne2000 layer, which neither mvme187 nor luna-88k instantiates.  Per the carrier, no SEC `cmp` for these | -- |
| clean | `src/cpus` `make clean` (generated tables, generators, objects), every other `.o`, the binary | `build_base.out` |
| build | `make -j8` in WSL Gentoo, foreground: `MAKE_RC=0`, 0 error lines, 0 warnings, 223 objects; `generate_m88k_loadstore` regenerated `tmp_m88k_loadstore.c` (`make_base.log:227-228`, 198 functions) | `build_base.out`, `make_base.log` |
| binary | `/tmp/gxt36/base/gxemul`, md5 `2efeec559ec5b3d16b200cccf4203631`, 19:43:15; `[ gxemul -nt ... ]` FRESH for `memory_rw.c`, `dev_luna88k.c`, `dev_m8820x.c`, `tmp_m88k_loadstore.c`, `dev_pcc2.c` | `build_base.out`, `run_witness.out` |
| instrument | the probe that produced both outputs is md5 `d59798b0383f433b191e214e7848fe49`, the file in this directory | `run_witness.out`, `MANIFEST.md5` |

`build/` was only read (`cp -a` source).  No build tree was mutated, so no `.MUTANT` sentinel was owed.

## What the probe does

`m88k_buserr_probe.py` (header = rows, mutant per row, CONTRACT, citations).  Stepped cold-debugger sessions, the
debugger fed on stdin (`vme_default_probe.py`'s shape); a 4-byte dummy raw image at `0x10000`; no device_add and
no machine edit.  Every session runs one program; only the access word and its registers change:

1. `ld` the data and instruction CMMU **IDR** (offset `0x000`) -- device signature;
2. `st` four distinct seeds into both CMMUs' **PFSR** (`0x108`) and **PFAR** (`0x10c`), then `ld` all four back --
   liveness through the same decode;
3. **the access under test** at `0x10028`;
4. the reads of the four registers happen in a handler `H` (`0x10100`) that BOTH paths reach: the vectors
   (`0x10` instruction access, `0x18` data access; VBR is 0 at reset, measured) set a marker in r7 and branch to
   `H`; an access that raises nothing falls through (marker r6) and branches to the same `H`.  So the reads happen
   regardless of whether the exception redirects the pc -- the second option the brief offered.

Seeds: data PFSR `0x5a5a5a5a`, data PFAR `0x13572468`, instruction PFSR `0x2468ace0`, instruction PFAR
`0x0badf00d`.  Neither PFSR seed carries BERROR in the field a guest tests (`(x >> 16) & 7` = 2 and 0).

### Guest addresses and register offsets, with their sources

| what | value | source |
|---|---|---|
| CMMU IDR / PFSR / PFAR offsets | `0x000` / `0x108` / `0x10c` | `m8820x.h:60`, `:65`, `:66`; read `dev_m8820x.c:257-258`; PFSR/PFAR guest-stored `:437-461`; IDR never stored `:262-272` |
| BERROR status | `CMMU_PFSR_BERROR << 16` = `0x00030000` | `m8820x.h:125`, field extract `:123` |
| IDR seed | `0x00a90000` = `(M88200_ID << 21) \| (9 << 16)`, `M88200_ID` 5 | `m8820x.h:152`; `dev_mvme187.c:139`, `:151`; `dev_luna88k.c:949`, `:960` |
| mvme187 data / instruction CMMU | `0xfff7f000` / `0xfff77000`; cmmu[1] / cmmu[0] | `mvme187.h:57`, `:56`; `dev_mvme187.c:136-137`, `:140-142`, `:148-149`, `:154-156`; `dev_m8820x.c:540-543` |
| luna-88k cpu-0 data / instruction CMMU | `0xfff06000` / `0xfff07000` | `luna88k_board.h:163`, `:162`; `dev_luna88k.c:934-965`, `:1074` |
| refusing device 1 | `0xfff46010` in `unreadable addr=0xfff46000 len=0x1000` (device-relative `0x10`) | `machine_mvme88k.c:106`; `dev_unreadable.c` (`return 0;`) |
| refusing device 2 | `0xfff40090`, VME population 1 (device-relative `0x90`) | `mvme88k_vme.h:44`; `machine_mvme88k.c:95-96`; `dev_vme.c:207-220` |
| accepted access (control) | `0xfff40088`, VME VBR, served `0x67000000` | `mvme88k_vme.h:80`; `dev_vme.c:144`, `:238-239` |
| LUNA probe address | `0x3ffffff0` (= `LUNA88K_REGISTERS_BASE`) | `dev_luna88k.c:78`, `:624-627`, `:990-992` |
| vectors, SXIP, DMA0 | vector 2 / 3, pc = VBR + 8 * vector, SXIP = pc \| V (`0x2`) | `cpu_m88k.h:202-203`; `cpu_m88k.c:837`, `:863`, `:908-912`; `m88k_psl.h:90` |

## What it observed (`WITNESS_headbin.out`; raw transcripts in `transcripts_headbin/`)

"Before" is the readback after seeding (every session read back exactly the four seeds).

| cell | access | route (vector / SXIP / DMA0) | data PFSR after | data PFAR after | instr. CMMU after |
|---|---|---|---|---|---|
| `ok` (mvme187) | `ld` 0xfff40088, accepted | none, falls through; r4 = `0x67000000` | `0x5a5a5a5a` (seed) | `0x13572468` (seed) | seeds |
| `uld` (mvme187) | `ld` 0xfff46010, refused | **3** / `0x1002a` / `0xfff46010`; r4 kept | **`0x5a5a5a5a` (seed)** -- want `0x00030000` | **`0x13572468` (seed)** -- want `0xfff46010` | seeds |
| `ust` (mvme187) | `st` 0xa5a5a5a5 to 0xfff46010 | **3** / `0x1002a` / `0xfff46010` | **seed** -- want `0x00030000` | **seed** -- want `0xfff46010` | seeds |
| `vme` (mvme187) | `ld` 0xfff40090, refused | **3** / `0x1002a` / `0xfff40090`; r4 kept | **seed** -- want `0x00030000` | **seed** -- want `0xfff40090` | seeds |
| `luna` (luna-88k) | `ld` 0x3ffffff0 | **none**: falls through, SXIP 0, DMA0 0, **r4 = 0 (served)** -- want vector 3, r4 kept | `0x00030000` (written by the case) | **`0x13572468` (seed)** -- want `0x3ffffff0` | seeds |

**Why this is the symptom under test.**  The ruled fix writes PFSR = `0x00030000` and PFAR = the physical address
in the refused-access arm, and routes the LUNA case through that arm.  On HEAD the exception IS taken (vector 3,
SXIP naming the access instruction, DMA0 its address), yet the guest's own seeds survive in PFSR and PFAR: nothing
was written.  The SYMPTOM line classifies each of the eight red rows as STALE -- the exact seed, or the LUNA
fall-through serving 0 -- rather than OTHER, so none is red because of a death, a timeout, a missing device or a
failed readback.

**The ledger's citation of the fork's own measurement, checked:** `vmedefaultkill/measure_20261009/run_FAULT.out`
reads PFSR 0 and PFAR 0 after a FAULT, on a variant build, with UNSEEDED registers.  Zero is also the reset
value, so that run could not tell "not written" from "written zero".  The seeds here can.

### Controls (all green; CONTROL rows plus a per-session prerequisite check in every scored row)

* **apparatus negative** -- bogus subtype `187` exits 1 with no register dump (`neg apparatus`;
  `transcripts_headbin/neg_apparatus.txt`): the session oracle can go red.
* **DEVICE SIGNATURE** -- both CMMUs' IDR read `0x00a90000` on both machines (`mv devsig`, `luna devsig`, and the
  prerequisite of every scored session).  RAM cannot answer it: the windows are far past the 64 MB of RAM, and
  an unclaimed address reads 0 (INFO `unclaimed`).
* **LIVENESS through the same decode** -- the four seeds stored and read back (`mv cmmu rt`, `luna cmmu rt`, and
  per session).
* **The read channel can see a write** -- `luna pfsr`: the same handler reads PFSR change from the seed to
  `0x00030000` when the model writes it (`dev_luna88k.c:626`).  So the unchanged seeds in the generic cells come
  from a channel that is sensitive to a model-side write, not from a blind read.
* **Attribution** -- route rows: vector 3 entered, fall-through marker unset, SXIP `0x1002a` = `0x10028 | V`, DMA0 =
  the access's own address.
* **Handler completed** -- pc `0x10114` and r31 `0x5678` in every scored session.
* **`unasm` 115/115** -- every placed word re-read by the disassembler; a literal derived by hand.
* **Not a single-step artifact** -- free-running to a breakpoint (`explore2.out` case 1: the exploration program,
  same access and seeds, shorter preamble): vector 3, data PFSR `0x5a5a5a5a`, data PFAR `0x13572468`.  The LUNA cell
  free-running (`explore2.out` case 3): falls through, r4 = 0, PFSR `0x00030000`, PFAR seed.
* **LUNA shape** -- dummy raw image and the rig shape (`-d R:<liveimage> boot`, cwd `_images/`) give identical rows
  (`WITNESS_headbin_rig.out`, `transcripts_headbin_rig/`; first seen in `explore1.out` cases 5 and 6).

### INFO cells (measured, never scored)

* **Instruction-fetch refusal** (`jmp` to 0xfff46010).  Stepped: vector 2, SXIP `0xfff46013`, instruction-CMMU
  PFSR/PFAR still the seeds, and the transcript carries the debugger pre-read's "could not read the instruction"
  message, not the halt message.  Free-running (`explore2.out` case 2): `to_be_translated(): read failed: TODO`,
  `UNIMPLEMENTED instruction at 0x10`, `All machines stopped`; pc `0x10`, SXIP `0xfff46013`, the vector's first
  instruction never ran.  The stepped delivery comes from the debugger's own disassembly fetch, so it is not
  counted as a witness.  The cmmu[0] cell is left to the round (NOT CLAIMED).
* **Unclaimed physical address** (`ld` 0x10000000 on mvme187: past RAM, below every device): falls through, r4 = 0,
  no exception, all four seeds kept, one `memory READ: from non-existant paddr=0x10000000` line.

## Corrections to the brief's premises, each measured or read here

1. **"A load or store to a physical address no device claims" does not reach the arm T36 repairs.**  It takes
   `memory_rw.c:662-713` (served zeros, at most a warning; under `-T`, `core/main.c:465-466`, every cpu stops) --
   INFO `unclaimed`.  The arm is reached only by an access a device CLAIMS and REFUSES (returns 0 while the cpu
   keeps running): mvme187's `unreadable` windows (`machine_mvme88k.c:106`, `:120`, `:123`) and VME population 1.
2. **On an unmodified luna-88k, every device refusal also stops the cpu** (this was read in the source, not
   measured).  Every `return 0;` in `dev_luna88k.c` (1, the `default:` at `:909-924`), `dev_mb89352.c` (6) and
   `dev_lunafb.c` (4; that device exists only with `-X`) comes immediately after `cpu->running = 0`, so
   `memory_rw.c:591-592` returns before the arm.  The `dev_le` access function returns `retval` >= 1.  `le_sram`'s
   `return 0` (`dev_le.c:932`) cannot be reached, because its window is `SRAM_SIZE` long and `memory_rw.c:495-523`
   clamps `len` to the window.  `dev_m8820x` always returns 1.  So the generic arm is witnessed on mvme187, and
   luna-88k supplies only the probe-case half.
3. **The LUNA half's pre-fix symptom is not "PFSR lacks the status".**  PFSR IS written today (`luna pfsr` is
   green on HEAD).  What is missing is PFAR and the exception, and the access is served 0.
4. **`_scratchpad/gxprobe.py` was not used.**  It carries MIPS presets and installs MIPS stubs when constructed.
   This probe uses no pty at all: it uses `vme_default_probe.py`'s piped-stdin shape.  The free-running
   exploration copied that file's own `run_pty`.

## Residuals found while measuring (for triage; NOT filed)

* **R1 -- an m88k instruction-fetch refusal halts the cpu.**  Free-running, the fetch raises vector 2.  Then
  `cpu_m88k_instr.c:2989-2993` reaches the dyntrans `bad:` tail (`cpu_dyntrans.c:1983-2014`), which stops every
  cpu before the handler runs (`explore2.out` case 2).  This blocks a free-running witness for T36's cmmu[0] cell.
  The tail is generic dyntrans code, so other architectures may behave the same way (not measured).
* **R2 -- single-stepping changes instruction-fetch fault behaviour.**  The step loop's disassembly pre-read
  (`cpu_dyntrans.c:287-290`) is a `CACHE_INSTRUCTION` `memory_rw` WITHOUT `NO_EXCEPTIONS`.  So when the debugger
  steps onto a refusing device, its own read raises the exception, and the vector then runs instead of the cpu
  halting (INFO `ifetch`).  The debugger changes guest-visible state.
* **R3 -- an unclaimed physical address raises no bus error at all on m88k.**  A read is served zeros and a write
  is dropped; upstream TODOs at `memory_rw.c:682` and `:709-710`.  Whether real MVME187/LUNA hardware bus-errors
  there is a board question (`_scratchpad/vmesbcp2.txt` is on disk).  It was not checked here.

## Owed, and not done

* The post-fix half of witness clause (i): the same script all green (`M88K_BUSERR_SYMPTOM=ABSENT`) after the
  round's fix.  This is OWED to the round.  Two of the want strings are shown to be reachable on HEAD by the same
  formatter: `0x30000` is produced by `luna pfsr`, and the `v3/0x1002a/<addr>` route is produced by the three
  generic route rows.  The PFAR wants have never yet been produced by a model write.
* No mutant was built.  The mutant names given for each row in the header are dated predictions.
* The contract's NOT CLAIMED cells: translation on (VA differs from PA), an absent CMMU (the NULL check),
  `no_exceptions` callers, instruction access, sub-word accesses and byte addresses, more than one cpu, xmem, the
  88110, and the OpenBSD reader / `badaddr()` recovery.  A rung-4 boot would be the stronger witness; it was not
  attempted.
* The icmmu rows encode the ruling's "do not clear the sibling" (Grok Q2).  If the round decides otherwise, those
  wants change.

## Landing notes for the main loop

* Git was used only for object reads (`rev-parse`, `log`, `show`, `ls-files`).  Nothing is staged.
* When `m88k_buserr_probe.py` is staged it needs a `tools/pipeline/check_probe_wiring.py` MANIFEST line.  That
  checker reads tracked-or-staged files only (`domain()`), so the untracked file reds nothing today.  The
  exploration and driver scripts are kept as `*.py.txt` / `*.sh.txt` on purpose.
* The WSL scratch clone `/tmp/gxt36/base` is kept.  It is a named baseline (HEAD 66920157 plus the five HEAD
  blobs; binary md5 `2efeec55...`) for the round's kill tables.  `/tmp` is volatile, and every number cited here
  is in this directory.
* To re-run: `python3 m88k_buserr_probe.py <gxemul> [label] [images-dir]`, with
  `M88K_BUSERR_DUMP=<dir>` to keep the session transcripts.  The exact driver is `run_witness.sh.txt`.

## Files in this directory

`m88k_buserr_probe.py` (the probe), `WITNESS_headbin.out` / `WITNESS_headbin_rig.out` (the pre-fix runs),
`transcripts_headbin/` / `transcripts_headbin_rig/` (8 raw sessions each), `run_witness.sh.txt` / `run_witness.out`
(driver + its receipt), `build_base.sh.txt` / `build_base.out` / `make_base.log` (build), `baseline_check.sh.txt` /
`baseline_check.out` / `headblobs_MD5.txt` (baseline), `explore1.py.txt` / `explore1.out` (first stepped exploration,
including the rig-vs-dummy comparison), `explore2.py.txt` / `explore2.out` (free-running exploration),
`MANIFEST.md5`.
