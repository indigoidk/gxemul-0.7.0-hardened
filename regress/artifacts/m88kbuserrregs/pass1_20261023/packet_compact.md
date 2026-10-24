# PASS-1 DESIGN REVIEW -- round #570, ledger row `m88kbuserrregs` (research item T36) -- GXemul hardened fork
**Brief v1, COMPACT form (for packet-fed seats; it stands alone -- every premise and question of the FULL form is here).**  Drafted 2026-10-23.
Tree under review: `GXEMUL-SEC/` at HEAD `7fca7187` -- a RECORDS-ONLY commit on top of `66920157` (four records files, named in the FULL form); every
`src/` file and every top-level `regress/*.py` / `*.sh` is byte-identical at the two (section 4).  Built from
`GXEMUL-SEC/tools/BRIEF_TEMPLATE.md` (working tree).

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**  There are THREE pristine-2021-upstream
copies of GXemul under the project root (`./src/` and two under
`_archive/audit-results-*/builds/`).  They are NOT this fork.  If your line numbers
disagree with mine by hundreds you are reading one of them — say so rather than
reconciling.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — an index range, an offset, a count of
reachable addresses — ENUMERATE it rather than reasoning about it.**  Walk the values.
A derivation that skips one masking line reads exactly like a correct one.

**And ENUMERATE THE RIGHT DOMAIN — a domain is itself a premise.**  Ask what the PRODUCER of
these values can actually emit before you walk them.  Walking every member of a set you have
not audited is not enumeration; it is a derivation with more steps, and it reads exactly like
a correct one.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## 0. What this is, what this pass is for, and how to answer

**The project.**  GXemul is a computer-architecture emulator: a developer tool that runs legacy operating systems
inside a software sandbox.  This fork is a hardening effort -- ordinary software-correctness work on the emulator's
own C code and the regression tests that keep each correction fixed.  The *guest* is a program or OS running INSIDE
the emulator; the *host* is the emulator process.  A *variant* or *mutant* below is a deliberately altered copy of the
code, used to measure whether a regression test notices the alteration (standard mutation testing).

**The defect, in one paragraph.**  On the two 88K machines this tree models with MC88200 CMMUs (MVME187 and
LUNA-88K), when a guest load or store reaches a device that REFUSES it, the emulator raises the CPU's access exception
but leaves the CMMU's P-bus fault status register (PFSR, offset 0x108) and P-bus fault address register (PFAR,
offset 0x10c) holding whatever they held before, so a guest fault handler that reads them to classify the fault reads
stale values.  And at one LUNA-88K address (0x3ffffff0) the board device writes PFSR itself but then SERVES the access:
no exception, no PFAR.  It is a WRONG-RESULT defect; no host process ends anywhere in this round.

**This pass.**  PASS 1, before any edit: check the AGREED design (section 3) and the rows it owes, against the rung-3 witness (section 2).  Section 5 is settled -- re-open a premise only if it is false, and say so loudly; section 6 holds my least-sure premises AS QUESTIONS; section 7 is my partition -- check it.  READ-ONLY; nobody is asked to write a guest program or a code variant -- where a question needs one, it names the candidates the records already contain.

**This COMPACT form is self-contained:** every premise and question of the FULL form, some evidence condensed (each says so).

**Answer format -- VERDICT LINE FIRST:**
~~~~
VERDICT: READY | READY WITH CHANGES | NOT READY -- <one line>
Q1: <one line>   Q2: <one line>   Q3: <one line>   Q4: <one line>
~~~~
Then one section per question.  Mark each claim READ (you opened the source), DERIVED (from this packet) or NOT
CHECKABLE.  Where you answer a premise in section 6, cite it by its number (P1..P12).

---

## 1. The defect -- as the ledger row and the queue describe it (VERBATIM)

**Ledger row `m88kbuserrregs`** (`tools/pipeline/ledger.json` at HEAD `7fca7187`; identical at `66920157`): state `open`, sev `MED`, witness `none`, commits `''`.

TITLE (VERBATIM):
~~~~
cpus/memory_rw.c MEM_M88K device-failure arm + devices/dev_luna88k.c case 0x3ffffff0 -- a refused device access raises the access exception without writing the CMMU fault status (PFSR=BERROR) and fault address (PFAR); the LUNA probe address writes PFSR only, no PFAR and no exception -- WRONG-RESULT (the guest's trap handler reads PFSR 0 for a bus error, per the fork's own vmedefaultkill measurement)
~~~~
*The row's state note is VERBATIM in the FULL form; the facts in it that a question depends on are in sections 3 and 5.*

**`OUTSTANDING_BUGS.md`** (HEAD) -- the batch queue line (VERBATIM):
~~~~
   34| > 5. `m88kbuserrregs` (MED, new) -- 88K bus errors carry no PFSR/PFAR; the carrier of the reopened PFAR item.  T36;
   35| >    before any 88K fault round.
~~~~
---

## 2. The witness -- rung 3, RED on HEAD

The round's measuring seat, 2026-10-23, test-first, before any edit.  `regress/artifacts/m88kbuserrregs/witness_20261023/` -- UNTRACKED at HEAD; frozen by its MANIFEST.md5 (probe md5 `d59798b0...`).  Binary: a scratch clone of HEAD `66920157` (source identical to `7fca7187`).

### 2.1 The verdict, and the baseline row naming the files the seat expects the round to edit (WITNESS_REPORT.md, VERBATIM)
~~~~
    3| **VERDICT: RED ON HEAD -- the symptom reproduced, both halves, on unmodified in-tree machines.**
    4| `WITNESS_headbin.out`: `M88K_BUSERR_RESULT=16/24`, `M88K_BUSERR_CONTROL=OK`, `M88K_BUSERR_SYMPTOM=PRESENT 8/8`,
    5| `M88K_BUSERR_RED=uld pfsr,uld pfar,ust pfsr,ust pfar,vme pfsr,vme pfar,luna route,luna pfar`, sentinel
    6| `M88K_BUSERR_PROBE_DONE`.  The rig-shape run (`WITNESS_headbin_rig.out`) gives identical rows.
   ...
   22| | the three files the round will edit, HEAD blob vs GXEMUL-SEC working tree vs `build/` | all CLEAN: `memory_rw.c` 3d47dd66..., `dev_luna88k.c` 6ecc6908..., `dev_m8820x.c` 0d12cfaf... | `baseline_check.out` |
~~~~
### 2.2 The pre-fix run, whole (WITNESS_headbin.out -- VERBATIM except that runs of three or more padding spaces are collapsed to two; the rig-shape run differs only in its two label lines and its elapsed time)
~~~~
m88kbuserrregs RUNG-3 WITNESS (revision 1) -- binary=/tmp/gxt36/base/gxemul label=HEAD-66920157
machines: -E mvme88k -e mvme187 -M 64 and -E luna88k -e luna-88k (UNMODIFIED); luna shape: dummy raw image at 0x10000
seeds: dPFSR=0x5a5a5a5a dPFAR=0x13572468 iPFSR=0x2468ace0 iPFAR=0xbadf00d; want BERROR<<16=0x30000
row  got  want  note
neg apparatus  exit1/absent  exit1/absent  bogus subtype `187' -> no machine -> no register dump  ok
mv devsig  0xa90000/0xa90000  0xa90000/0xa90000  DEVICE SIGNATURE: mvme187 data/instr CMMU IDR (RAM reads 0)  ok
mv cmmu rt  0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d 0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d LIVENESS: four seeds stored and read back via the CMMU decode  ok
ok route  fall/r4=0x67000000  fall/r4=0x67000000  ld VME VBR 0xfff40088 (cased): served 0x67000000, no exception ok
ok regs  0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d 0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d an ACCEPTED device access writes no fault metadata  ok
uld route  v3/0x1002a/0xfff46010  v3/0x1002a/0xfff46010  ld 0xfff46010 (unreadable): vector 3, SXIP, DMA0 -- the exception is THIS access ok
uld pfsr  0x5a5a5a5a  0x30000  data CMMU PFSR after the fault (seeded 0x5a5a5a5a)  FAIL
uld pfar  0x13572468  0xfff46010  data CMMU PFAR after the fault (seeded 0x13572468)  FAIL
uld icmmu  kept  kept  instruction CMMU PFSR/PFAR keep their seeds  ok
ust route  v3/0x1002a/0xfff46010  v3/0x1002a/0xfff46010  st 0xfff46010 (unreadable): vector 3, SXIP, DMA0 -- the exception is THIS access ok
ust pfsr  0x5a5a5a5a  0x30000  data CMMU PFSR after the fault (seeded 0x5a5a5a5a)  FAIL
ust pfar  0x13572468  0xfff46010  data CMMU PFAR after the fault (seeded 0x13572468)  FAIL
ust icmmu  kept  kept  instruction CMMU PFSR/PFAR keep their seeds  ok
vme route  v3/0x1002a/0xfff40090  v3/0x1002a/0xfff40090  ld 0xfff40090 (VME pop. 1): vector 3, SXIP, DMA0 -- the exception is THIS access ok
vme pfsr  0x5a5a5a5a  0x30000  data CMMU PFSR after the fault (seeded 0x5a5a5a5a)  FAIL
vme pfar  0x13572468  0xfff40090  data CMMU PFAR after the fault (seeded 0x13572468)  FAIL
vme icmmu  kept  kept  instruction CMMU PFSR/PFAR keep their seeds  ok
luna devsig  0xa90000/0xa90000  0xa90000/0xa90000  DEVICE SIGNATURE: luna-88k data/instr CMMU IDR  ok
luna cmmu rt  0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d 0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d LIVENESS: the four seeds read back  ok
luna route  fall/0x0/0x0/r4=0x0  v3/0x1002a/0x3ffffff0/r4=0xdeadbeef ld 0x3ffffff0: a refused access raises vector 3, serves nothing FAIL
luna pfsr  0x30000  0x30000  data CMMU PFSR (seeded 0x5a5a5a5a)  ok
luna pfar  0x13572468  0x3ffffff0  data CMMU PFAR (seeded 0x13572468)  FAIL
luna icmmu  kept  kept  instruction CMMU PFSR/PFAR keep their seeds  ok
INFO ifetch  jmp (r5) to 0xfff46010: how=exit0 path=v2 SXIP=0xfff46013 iPFSR=0x2468ace0 iPFAR=0xbadf00d dPFSR=0x5a5a5a5a dPFAR=0x13572468 pre-read-msg=1 halt-msg=0 unasm=23/23
INFO unclaimed  ld 0x10000000 (no device, past RAM): how=exit0 path=fall r4=0x0 SXIP=0x0 dPFSR=0x5a5a5a5a dPFAR=0x13572468 iPFSR=0x2468ace0 iPFAR=0xbadf00d non-existant-msg=1 unasm=23/23
unasm  115/115  115/115  every placed word re-read by the disassembler  ok
SCORE 16/24
M88K_BUSERR_RESULT=16/24
M88K_BUSERR_CONTROL=OK
M88K_BUSERR_SYMPTOM=PRESENT 8/8
M88K_BUSERR_LABEL=HEAD-66920157
M88K_BUSERR_ELAPSED=0.030s
M88K_BUSERR_RED=uld pfsr,uld pfar,ust pfsr,ust pfar,vme pfsr,vme pfar,luna route,luna pfar
M88K_BUSERR_PROBE_DONE
~~~~
### 2.3 The 24 rows, enumerated (the drafter's enumeration of 2.2 -- 6 + 10 + 8 = 24)

* **The 6 CONTROL rows** (`CONTROL_ROWS`, probe line 583), all green: `neg apparatus`, `mv devsig`, `mv cmmu rt`,
  `luna devsig`, `luna cmmu rt`, `unasm`.
* **The 10 other scored rows that are GREEN on HEAD:** `ok route`, `ok regs`, `uld route`, `uld icmmu`, `ust route`,
  `ust icmmu`, `vme route`, `vme icmmu`, `luna pfsr`, `luna icmmu`.
* **The 8 RED rows -- the symptom, each classified STALE by the probe:** `uld pfsr`, `uld pfar`, `ust pfsr`,
  `ust pfar`, `vme pfsr`, `vme pfar`, `luna route`, `luna pfar`.
* Two INFO lines are printed and never scored: `INFO ifetch`, `INFO unclaimed`.
* The probe exits 0 only when every row passes AND every control passes (probe lines 583-605, section 2.12).

### 2.4 Why that is the symptom (WITNESS_REPORT.md, VERBATIM; its per-cell table repeats 2.2 and is in the FULL form)
~~~~
   80| **Why this is the symptom under test.**  The ruled fix writes PFSR = `0x00030000` and PFAR = the physical address
   81| in the refused-access arm, and routes the LUNA case through that arm.  On HEAD the exception IS taken (vector 3,
   82| SXIP naming the access instruction, DMA0 its address), yet the guest's own seeds survive in PFSR and PFAR: nothing
   83| was written.  The SYMPTOM line classifies each of the eight red rows as STALE -- the exact seed, or the LUNA
   84| fall-through serving 0 -- rather than OTHER, so none is red because of a death, a timeout, a missing device or a
   85| failed readback.
~~~~
### 2.5 Controls and INFO cells (CONDENSED from WITNESS_REPORT.md lines 91-122)

Apparatus negative (a bogus subtype: exit 1, no register dump); DEVICE SIGNATURE (both CMMUs' IDR 0x00a90000 on both
machines -- RAM and unclaimed addresses read 0); LIVENESS (the four seeds read back through the same decode, per
session); the read channel sees a model write (`luna pfsr`: seed -> 0x00030000); attribution (vector 3, fall-through
marker unset, SXIP 0x1002a = 0x10028 | V, DMA0 = the access's address); handler completed in every scored session;
`unasm` 115/115; NOT a single-step artifact (a free-running run gave the same stale registers, and the same LUNA
fall-through); dummy and rig LUNA shapes identical.  INFO `ifetch` (`jmp` to 0xfff46010): stepped, vector 2 comes from
the debugger's pre-read; free-running, the cpu stops before the vector runs (R1) -- NOT CLAIMED.  INFO `unclaimed` (`ld`
0x10000000): falls through, r4 = 0, no exception, seeds kept.

### 2.6 The measuring seat's FOUR premise corrections (CONDENSED from WITNESS_REPORT.md lines 124-141)

1. "A load or store to a physical address no device claims" does NOT reach the arm T36 repairs: it is served zeros
   with at most a warning (memory_rw.c:662-713) -- INFO `unclaimed`.  Only an access a device CLAIMS and REFUSES (returns
   0 with the cpu still running) reaches it: mvme187's `unreadable` windows and VME population 1.
2. On an unmodified luna-88k every device refusal also stops the cpu (read in the source, not measured) -- S3 -- so the
   generic arm is witnessed on mvme187 and luna-88k supplies only the probe-case half.
3. The LUNA half's pre-fix symptom is not "PFSR lacks the status": PFSR IS written today (`luna pfsr` green on HEAD);
   what is missing is PFAR and the exception, and the access is served 0.
4. `_scratchpad/gxprobe.py` was not used (MIPS presets); the probe drives the debugger on stdin, `vme_default_probe.py`'s
   shape.

### 2.7 Its three unfiled findings R1-R3 -- carried to Q4 as findings, by id (WITNESS_REPORT.md, VERBATIM)
~~~~
  143| ## Residuals found while measuring (for triage; NOT filed)
  144| 
  145| * **R1 -- an m88k instruction-fetch refusal halts the cpu.**  Free-running, the fetch raises vector 2.  Then
  146|   `cpu_m88k_instr.c:2989-2993` reaches the dyntrans `bad:` tail (`cpu_dyntrans.c:1983-2014`), which stops every
  147|   cpu before the handler runs (`explore2.out` case 2).  This blocks a free-running witness for T36's cmmu[0] cell.
  148|   The tail is generic dyntrans code, so other architectures may behave the same way (not measured).
  149| * **R2 -- single-stepping changes instruction-fetch fault behaviour.**  The step loop's disassembly pre-read
  150|   (`cpu_dyntrans.c:287-290`) is a `CACHE_INSTRUCTION` `memory_rw` WITHOUT `NO_EXCEPTIONS`.  So when the debugger
  151|   steps onto a refusing device, its own read raises the exception, and the vector then runs instead of the cpu
  152|   halting (INFO `ifetch`).  The debugger changes guest-visible state.
  153| * **R3 -- an unclaimed physical address raises no bus error at all on m88k.**  A read is served zeros and a write
  154|   is dropped; upstream TODOs at `memory_rw.c:682` and `:709-710`.  Whether real MVME187/LUNA hardware bus-errors
  155|   there is a board question (`_scratchpad/vmesbcp2.txt` is on disk).  It was not checked here.
~~~~
### 2.8 Owed (CONDENSED from WITNESS_REPORT.md lines 157-181)

The post-fix half of witness clause (i) (same script, all green, `SYMPTOM=ABSENT`) is OWED.  No variant was built.  Staging the probe needs a `check_probe_wiring.py` MANIFEST line.

### 2.9 / 2.10 -- the program listing and address table (FULL form only).  Each session: read both CMMUs' IDR, seed both CMMUs' PFSR and PFAR and read them back, make the access, then read the four registers in a handler that both exception vectors AND the no-exception fall-through reach.

### 2.11 The probe's ROWS with their predicted variants, then its CONTRACT (both CONDENSED by the drafter from probe lines 92-173; the variant names are the seat's DATED PREDICTIONS -- none was built)

| row(s) | channel | predicted variant |
|---|---|---|
| `ok route` | accepted VME VBR read: fall-through, r4 0x67000000 | `res <= 0` -> `res <= 1` |
| `ok regs` | the four seeds survive an accepted access | the writes OUTSIDE `res <= 0` |
| `uld route` | vector 3, SXIP, DMA0, r4 kept | the exception DROPPED (not "moved inside the NULL check": both CMMUs exist) |
| `uld pfsr` | data PFSR = 0x00030000 | no write (HEAD); raw 3; cmmu[0] instead of cmmu[1] |
| `uld pfar` | data PFAR = 0xfff46010 | no write; device-relative `paddr` (0x10); PFSR-only; cmmu[0] |
| `uld icmmu` | instruction CMMU keeps its seeds | writes on BOTH CMMUs or cmmu[0] only; the sibling cleared |
| `ust *` (four) | the same four channels for a STORE | conditioned on direction (`writeflag == MEM_READ`) |
| `vme *` (four) | the same at VME population 1; PFAR 0xfff40090 | keyed to one device (name, base or length) |
| `luna route` | vector 3, SXIP, DMA0 0x3ffffff0, r4 kept | the case left returning 1 |
| `luna pfsr` | data PFSR = 0x00030000 (GREEN on HEAD) | the case's write deleted, still returning 1 |
| `luna pfar` | data PFAR = 0x3ffffff0 | the PFSR-only body kept; device-relative `paddr` (0x0) |
| `luna icmmu` | instruction CMMU keeps its seeds | -- |

CONTRACT (clause e) -- CONDENSED from probe lines 148-173 (VERBATIM in the FULL form).  DESIGNED to catch the
pre-fix defect and the variants above.  NOT CLAIMED: translation ON (VA = PA in every session, so a PFAR := `vaddr`
repair is indistinguishable); an ABSENT CMMU (both machines always attach both, so a repair without the NULL check, or
with the exception moved inside it, passes every row); `no_exceptions` callers; INSTRUCTION-access refusals (R1, R2:
"The cmmu[0] cell is the round's to build"); an UNCLAIMED address (a different path); sub-word accesses and byte
addresses (PFAR byte vs word address); more than one cpu, `xmem`, the 88110; the OpenBSD reader itself and `badaddr()`;
the sibling-CMMU premise of the `icmmu` rows ("a round that decides the data-side bus error should clear cmmu[0]'s PFSR,
as the translation-fault path does, changes those wants"); PFSR/PFAR bits beyond the exact values written; MC88200
timing and the P-bus.

### 2.12 The prerequisite check and the exit (CONDENSED from probe lines 424-435, 468-475, 580-605)

A scored row prints a cause-free `died:`/`nodev`/`readback`/`handler` string instead of a value when its OWN session has no register dump, no device signature, a failed seed readback or an unfinished handler -- so a dead binary reds every scored row.  Rows print a `%-16s` name (unique, at most 15 characters), got, want, note, `ok`/`FAIL`; then `M88K_BUSERR_RESULT=n/24`, `_CONTROL=OK|FAIL`, `_SYMPTOM=PRESENT n/8|ABSENT|MIXED`, `_RED=...`, and the sentinel `M88K_BUSERR_PROBE_DONE`; exit 0 only when every row and control passes.

---

## 3. The settled design (VERBATIM)

### 3.1 The merged ruling -- `CRIT_RULINGS.md`: the T36 row and the order lines
~~~~
   14| | **T36** 88K bus-error PFSR/PFAR | Write `PFSR = CMMU_PFSR_BERROR << 16` and `PFAR = orig_paddr` on CMMU 0 (instruction) / 1 (data) inside the refused-device arm, NULL check around the two writes only, exception delivered outside it; `dev_luna88k.c:624-627`'s probe case returns 0 through the repaired generic path (its own PFSR-only write deleted). Packet citation corrected: `memory_rw.c:437` SAVES `orig_paddr`; `:494` makes `paddr` device-relative. `#568` unchanged (declines stay declines; population-1 faults gain metadata). `badaddr()` is NOT a sufficient oracle (OpenBSD's `eh.S` recovery path bypasses the PFSR read); the reader is `trap.c:326-335`'s `(dpfsr>>16)&7 == 3`, and a guest `ld` of CMMU `0x108`/`0x10c` is the cheap row. R2's reopened PFAR item is carried here; the translation-fault PFAR semantics in `memory_m88k.c` are NOT changed. | Astra Q2; Grok Q2 | READY -- round 2; precedes every later 88K fault round |
   ...
   22| **Order (both seats):** T1, T36, T2, N5, T11, T4.  N3 feature; N4 unscheduled.  T1 is not merged with N1/N2; T2 not with
   23| N3; T36's generic path and LUNA case are ONE round; T11's two exits and the cache bit are ONE round; T4's advertisement,
   24| decode, arithmetic, readback and `#407` row are ONE round.
~~~~
### 3.2 GPT-6 Astra -- `codex_rescrit.txt`: the verdict line and the whole Q2 section
~~~~
    1| VERDICT: OPEN -- Astra’s T1 repair is correct; PPC fault-delivery dependencies and incomplete VR41xx subpage support prevent approving all six as ready fix rounds.
   ...
   22| **Q2 — T36: coherent bus-error metadata before exception delivery**
   23| 
   24| Within the existing refused-device-access arm:
   25| 
   26| - Select **CMMU 0 for instruction access, CMMU 1 for data access**.
   27| - If that pointer exists, write `PFSR = CMMU_PFSR_BERROR << 16`—`0x00030000`—and `PFAR = orig_paddr`.
   28| - Keep the NULL check around **the register writes only**. Deliver the appropriate CPU access exception outside it.
   29| - Retain the existing exception-suppression condition.
   30| 
   31| One citation in the packet needs correction: [`memory_rw.c:437`](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/memory_rw.c:437) **saves** the original physical address; line 494 makes `paddr` device-relative. Neither that relative address nor the virtual address belongs in this bus-error PFAR.
   32| 
   33| LUNA’s special probe needs the same coherent behavior. Its [current case](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_luna88k.c:624) writes only data PFSR and returns success. Have it report failure through the repaired generic path, which owns the metadata and exception. Do not import the plain-RAM windows for absent CMMUs.
   34| 
   35| R2 does **not** justify changing existing translation-fault PFAR values to virtual addresses. The cited `memory_m88k.c` sites prove PFAR is modeled; they deliberately distinguish descriptor-address faults and write-protection behavior. Correct the false record and repair the missing **bus-error** PFAR.
   36| 
   37| Required observations are data-read, data-write and instruction refusals; correct CMMU/status/address; translated VA differing from PA; nonzero device base; absent CMMU; suppressed exceptions; successful accesses; and LUNA’s special case. The detector must distinguish omitted register writes, wrong addresses, wrong CMMU selection and missing exception delivery.
   38| 
   39| OpenBSD `badaddr()` supplies a recovery compatibility row, **not a sufficient metadata oracle**: its special recovery path can bypass ordinary trap handling. Explicit guest-visible PFSR/PFAR observations are needed.
   40| 
   41| **Preserve #568’s disposition.** Named unimplemented VME registers continue to decline with their latched announcements. Unmatched accesses continue to fault, now with complete metadata. The [preserved FAULT measurement](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/vmedefaultkill/measure_20261009/run_FAULT.out:6) establishes the missing metadata; it does not prove that correcting it makes named-register faults acceptable. OpenBSD also checks the faulting context and recovery state. Keep the seven established compatibility sites and the existing 38-row detector, adding metadata checks for actual faults.
~~~~
### 3.3 Grok 4.7 -- `grok_crit.txt`: the whole Q2 section (its verdict: "VERDICT: SETTLED -- ... T36 writes `BERROR<<16` and the saved physical address ...")
~~~~
   26| ## Q2. T36 — write `BERROR<<16` and `orig_paddr` on the faulting CMMU; the LUNA case returns 0
   27| 
   28| The premise that line 437 has already made `paddr` device-relative is reversed. `:437` saves `orig_paddr = paddr` while `paddr` is still the physical address. The subtraction is `:494`. By the failure arm (`:603-623`) `paddr` is the device offset. PFAR gets `(uint32_t)orig_paddr`.
   29| 
   30| On `res <= 0 && !no_exceptions`, under `MEM_M88K`, before `m88k_exception`:
   31| 
   32| - `cmmu = cpu->cd.m88k.cmmu[cache == CACHE_INSTRUCTION ? 0 : 1]`, the same index as `memory_m88k.c:112` (0 instruction, 1 data).
   33| - If non-NULL: `reg[CMMU_PFSR] = CMMU_PFSR_BERROR << 16` (`3<<16`, `0x00030000`) and `reg[CMMU_PFAR] = (uint32_t)orig_paddr`.
   34| - The NULL check wraps only those two writes. `m88k_exception` stays outside it. Do not clear the sibling. The page-fault path does (`memory_m88k.c:383-384`); the bus-error write does not. Do not touch `:399` (PFAR = 0 on write protection) or the `exit` at `:390-394`.
   35| 
   36| `dev_luna88k.c:624-627` writes PFSR on the data CMMU with no NULL check and no PFAR, then `break`s into `return 1` at `:930`, so the access succeeds and no exception is raised. Replace that body with `return 0` and delete the PFSR store. The common arm then writes the right CMMU and raises the exception. Do not delete the case. `default:` (`:909-924`) sets `cpu->running = 0` and returns 0, and `memory_rw.c:591-592` then returns failure before the exception arm. Do not port `DEV_RAM_FAIL`, the beyond-RAM hunk that comments the exception out, or the plain-RAM CMMU windows.
   37| 
   38| `#568` is unchanged as a decline. The 26 named-but-unimplemented VME registers still return success. Population-1 faults gain PFSR `0x00030000` and PFAR equal to the VME physical address. `regress/vme_default_probe.py` pins PC `0x18`, DMA0, DMT0, and decline-versus-fault. It does not read PFSR, so those oracles stay green. Do not add a `PFSR == 0` assertion, and do not turn population 2 into a fault.
   39| 
   40| The pin is not `badaddr()`. In OpenBSD 2.2 `eh.S`, `badaddr` sets `FLAG_IGNORE_DATA_EXCEPTION` and `Data_Precheck` (`eh.S:312`) branches to `ignore_data_exception` before any PFSR read. A `badaddr()`-only row stays green when the exception is raised and the PFSR write is gone. The reader is `trap.c:326-335`: `(frame->dpfsr >> 16 & 7) == 3` and `sxip` inside `guarded_access_start..end`. A raw `3` in the low bits fails that extract. `CMMU_PFAR` (`m882xx.h:50`) is defined and has no reader under `sys/arch/mvme88k`; the fault address `trap.c` uses is the data unit's DMA0. PFAR is still the register upstream writes and the guest can `ld` it at CMMU offset `0x10c`.
   41| 
   42| Rows: a guest `ld` of the data CMMU at `0x108` and `0x10c` after a population-1 VME load on unmodified mvme187, field `(>>16)&7` equal to 3, PFAR equal to `orig_paddr`. A second cell reads `cmmu[0]` after an instruction fetch. A (d) mutant that stores the device offset fails because the VME base is not 0. A (d) mutant that writes only `cmmu[0]` on a data access fails the data-CMMU read. A (d) mutant that stores raw 3 fails the field extract. An accept row: a population-2 decline still returns success and does not write PFSR. Clause (c) is a memory-path round: an absent device, recorded by construction. The stronger boot witness is `sxip` inside the guarded window recovering at `guarded_access_bad`; the register `ld` is the cheap one. Every later 88K round whose repair is "return 0 and raise data-access" depends on this writer. T1 does not.
~~~~
### 3.4 The port source -- upstream trunk against 0.7.0 (`trunk_src.diff`, VERBATIM): the arm hunk the ruling ports, and the `cpu_m88k.c` include hunk NEITHER seat nor the ruling names (S16, P1).  Upstream's beyond-RAM hunk (metadata on the UNCLAIMED path, exception commented out) and its `DEV_RAM_FAIL` device over 0x3ffffff0 are refused (3.3) and are in the FULL form.
~~~~
 4668|  #ifdef MEM_M88K
 4669| -					/*  TODO: This is enough for
 4670| -					    OpenBSD/mvme88k's badaddr()
 4671| -					    implementation... but the
 4672| -					    faulting address should probably
 4673| -					    be included somewhere too!  */
 4674| +					struct m8820x_cmmu *cmmu = cpu->cd.m88k.cmmu[cache == CACHE_INSTRUCTION ? 0 : 1];
 4675| +					if (cmmu != NULL) {
 4676| +						cmmu->reg[CMMU_PFSR] = CMMU_PFSR_BERROR << 16;
 4677| +						cmmu->reg[CMMU_PFAR] = orig_paddr;
 4678| +					}
 4679|  					m88k_exception(cpu, cache == CACHE_INSTRUCTION
 4680|  					    ? M88K_EXCEPTION_INSTRUCTION_ACCESS
 4681|  					    : M88K_EXCEPTION_DATA_ACCESS, 0);

cpu_m88k.c:
 1917| @@ -50,6 +50,7 @@
 1918|  #include "settings.h"
 1919|  #include "symbol.h"
 1920|  
 1921| +#include "thirdparty/m8820x.h"
 1922|  #include "thirdparty/m8820x_pte.h"
~~~~
---

## 4. Section C0 -- has this round already shipped?  (CONDENSED; VERBATIM in the FULL form)

HEAD moved during drafting, `66920157` -> `7fca7187`, records only; `git log 66920157..HEAD -- src regress/*.py regress/*.sh` is empty.  Last commits: `memory_rw.c` 50fb2ee0, `dev_luna88k.c` and `cpu_m88k.c` 79cd12e8, `dev_m8820x.c` 2a5bc480, `memory_m88k.c` the 0.7.0 import; `regress/m88k_buserr_probe.py` does not exist.  `CHANGELOG.md` names `m88kbuserrregs` 0 times (its `T36`/`PFAR` hits are the 2026-10-22 research filing and the `#433`-`#435` dev_m8820x.c blocks).  The witness directory holds 0 tracked files.  Ledger: `state='open' witness='none' commits=''`.  est/ copies of the four product files are byte-identical to HEAD; none is in `tools/est_divergence.txt`.  **VERDICT: THE ROUND HAS NOT RUN.**

---

## 5. SETTLED PREMISES -- re-inlined so nobody spends an answer re-deriving them

Settled by the crit adjudication (Astra and Grok, source read at `de8c7547`, no build), by the witness (section 2), and
RE-READ IN THIS SCOPE at HEAD `7fca7187`.  `memory_rw.c` line numbers unless another file is named.

* **S1 -- `orig_paddr` is PHYSICAL and in scope at the arm.**  The device block opens at :436
  (`if (paddr >= mem->mmap_dev_minaddr && paddr < mem->mmap_dev_maxaddr) {`); its first statement is
  `uint64_t orig_paddr = paddr;` (:437), after translation (:245-270); `paddr -= mem->devices[i].baseaddr;` (:494) makes
  `paddr` device-relative; the arm (:603-625) is inside the block.  (Both seats corrected the crit packet here.)
* **S2 -- the arm.**  `res = 0;` (:583); the device runs only `if (!no_exceptions || (flags & DM_READS_HAVE_NO_SIDE_EFFECTS))`
  (:584-585); a device that stopped the cpu exits at :591-592 BEFORE the arm; `if (res == 0) res = -1;` (:595-596);
  `if (res <= 0 && !no_exceptions) {` (:603) prints a `debug()` naming direction, device and device-relative `paddr`
  (:604-607), then under `#ifdef MEM_M88K` only `m88k_exception(cpu, cache == CACHE_INSTRUCTION ?
  M88K_EXCEPTION_INSTRUCTION_ACCESS : M88K_EXCEPTION_DATA_ACCESS, 0);` (:614-623; TODO at :615-619 "the faulting address
  should probably be included somewhere too!"), and `return MEMORY_ACCESS_FAILED;` (:624).  Served (`res >= 1`):
  `goto do_return_ok;` (:626).  A read buffer is zeroed before the device call (:491-492).
* **S3 -- only a CLAIMED-and-REFUSED access reaches the arm.**  Unclaimed addresses go to `Outside of physical RAM?`
  (:662-713): zeros, dropped writes, no exception, no CMMU write.  On unmodified luna-88k every device `return 0;` follows
  `cpu->running = 0;` (dev_luna88k.c `default:` :922-924; dev_mb89352.c 6 sites; dev_lunafb.c 4, `-X` only), so :591-592
  returns first; dev_le.c's `return 0;` lines are helpers, except :932 (unreachable per the witness); dev_m8820x.c always
  returns 1 (:529).
* **S4 -- MVME187's four refusal sources:** `unreadable` windows 0xfff46000 len 0x1000, 0xff780000 len 0x80000,
  0xffff0000 len 0x10000 (machine_mvme88k.c:106, :120, :123; dev_unreadable.c's access is `return 0;`, :41-44, DM_DEFAULT)
  and VME2 population 1 (dev_vme.c `default:` `return 0;`, :207-220).  The 26 named unimplemented VME2 registers
  (population 2) DECLINE: `return 1`, one latched announce each (:150-205).
* **S5 -- the `cache` class** (`cache = misc_flags & CACHE_FLAGS_MASK;` :242): data loads/stores and `xmem` pass
  `CACHE_DATA` (`| MEMORY_USER_ACCESS` for `.usr`; cpu_m88k_instr_loadstore.c:60-64); the instruction fetch passes
  `CACHE_INSTRUCTION` (cpu_m88k_instr.c:2989-2990); the debugger's memory reads/writes pass `CACHE_NONE | NO_EXCEPTIONS`
  (debugger_cmds.c:716-717, :1006-1008, :1459-1461, :1506-1507, :1918-1919); the disassembler's look-behind reads
  `CACHE_INSTRUCTION | NO_EXCEPTIONS` (cpu_m88k.c:1117-1120, :1180-1183); the single-step disassembly pre-read
  `CACHE_INSTRUCTION` WITHOUT `NO_EXCEPTIONS` (cpu_dyntrans.c:287-288; R2).
* **S6 -- cmmu[0] is instruction, cmmu[1] data:** memory_m88k.c:112 `cmmu[instr? 0 : 1]`; dev_m8820x.c:540-543;
  dev_mvme187.c:136-137, :148-149; dev_luna88k.c:946, :957; `cmmu[MAX_M8820X_CMMUS]`, MAX 8 (cpu_m88k.h:228, :268).
* **S7 -- who has CMMUs** (only dev_mvme187.c and dev_luna88k.c assign `cd.m88k.cmmu[`): MVME187 attaches both to the
  bootstrap cpu only (dev_mvme187.c:136-149), the only cpu emul.c starts (emul.c:747-748); LUNA-88K to every cpu below
  `ncpus` (dev_luna88k.c:934-965, :1074-1077).  The 88110 machines (testm88k, barem88k, mvme197) and mvme188 attach none
  (cpu_m88k.c:340-342); of testm88k's devices (irqc, cons, mp, fbctrl, disk, ether, rtc; machine_test.c:136-168, plus
  the framebuffer fbctrl creates) only dev_fb.c has a `return 0;` (:719-721, past `framebuffer_size`), and
  `dev_fb_resize()` keeps the mapped length equal to that size (:205-212) -- unreachable by a claimed access, my reading
  (P4); barem88k, mvme188, mvme197 install no devices.
* **S8 -- the registers.**  `CMMU_PFSR (0x108 / 4)`, `CMMU_PFAR (0x10c / 4)` (m8820x.h:65-66); `CMMU_PFSR_FAULT(pfsr)` is
  `((pfsr) >> 16) & 0x07`, `CMMU_PFSR_BERROR` 3 (:123, :125): so 0x00030000.  dev_m8820x.c serves reads from
  `regs[relative_addr / 4]` (:257-258), stores guest PFSR/PFAR writes (:437-461), is `DM_DEFAULT` (:545-547, so the
  debugger never reaches it), and indexes the CMMU of `d->cpu_nr` (:250-251).  `tlbdump` prints BATC/PATC, never `reg[]`.
* **S9 -- the translation-fault writers (NOT changed):** memory_m88k.c:382 writes `pfsr_status << 16` on the faulting
  CMMU and :383-384 resets the OTHER CMMU's PFSR to SUCCESS (no NULL test); PFAR = 0 on write-protect (:397-400) and =
  the faulting DESCRIPTOR's physical address on SUPER/SFAULT/PFAULT (:402-406).  NULL cmmu or invalid APR: physical =
  virtual (:130-144).
* **S10 -- delivery:** `m88k_exception` (cpu_m88k.c:689): SXIP = pc | V (:837), | E for instruction access (:859-860);
  pc = VBR + 8 * vector (:863); a second non-trap exception under SFRZ becomes ERROR (:811-819); DATA_ACCESS copies
  DMT0/DMD0/DMA0 (:908-912).  DMA0 = VIRTUAL `addr & ~0x3` (cpu_m88k_instr_loadstore.c:131); half/word/double accesses
  are alignment-checked first (:167-186), bytes are not; `ld.d`/`st.d` is one 8-byte `memory_rw`.  A failing load
  returns before writing its register (:189-195).
* **S11 -- the guest reader, OpenBSD 2.2 mvme88k** (section 8): eh.S saves BOTH CMMUs' PFSR in its exception-entry setup
  (:1013-1018); trap.c recovers a guarded kernel access only when `(frame->dpfsr >> 16 & 0x7) == 0x3` and sxip is inside
  the guarded window (:326-336), and calls `vm_fault()` for a user fault only when NEITHER ipfsr NOR dpfsr is BERROR
  (:405-411); `badaddr()`'s `FLAG_IGNORE_DATA_EXCEPTION` is tested before the PFSR save (eh.S:273-275, :311-312), so
  `badaddr()` never reads PFSR; nothing reads `CMMU_PFAR` or writes the hardware PFSR.
* **S12 -- the manual:** "The MC88200 CMMU includes a local status register, which the exception handler must read"
  (mc88100.txt:9447-9451; :9337-9341 for instruction access); the data P bus carries a word address plus byte enables
  (:7870-7874).  **No MC88200 manual is on disk**, so no local source says what PFAR holds after a bus error.
* **S13 -- the witness** (section 2): rung 3, two unmodified machines, 8 rows red on HEAD, every control green.
* **S14 -- C0: not shipped** (section 4).
* **S15 -- `#568` is unaffected in reach:** population 2 never reaches the arm; population 1 does.  None of the 107
  top-level `regress/*.py` at HEAD mentions PFSR or PFAR -- no committed detector reads them, `vme_default_probe.py`'s 38
  rows included.
* **S16 -- the arm compiles inside `cpu_m88k.c` (src/cpus/tmp_m88k_tail.c:38-40), which does not include
  `thirdparty/m8820x.h`** (cpu_m88k.c:53-55 include m8820x_pte.h, m88k_dmt.h, mvmeprom.h; no header pulls it in:
  `git grep 'm8820x\.h' HEAD -- src`).  `CMMU_PFSR`, `CMMU_PFAR`, `CMMU_PFSR_BERROR` live only in m8820x.h, included
  only by memory_m88k.c, dev_luna88k.c, dev_m8820x.c, dev_mvme187.c.  tmp_m88k_tail.c is GENERATED, though tracked
  (src/cpus/Makefile.skel:140-141).  Upstream added the include to cpu_m88k.c (3.4).  -> P1.
* **S17 -- shared files:** memory_rw.c, dev_luna88k.c, dev_m8820x.c, cpu_m88k.c are not in tools/est_divergence.txt and
  are byte-identical in est/.
* **S18 -- out of scope:** `m88kexit` (memory_m88k.c:390-394); `lunadefaultstop` (why the LUNA case must stay); R3;
  upstream's beyond-RAM hunk, `DEV_RAM_FAIL` device and plain-RAM CMMU windows.
* **S19 -- the LUNA case.**  The switch is on `addr = relative_addr + LUNA88K_REGISTERS_BASE` (dev_luna88k.c:558; base
  0x3ffffff0, :78), so a load OR store of ANY width starting at 0x3ffffff0 reaches `case 0x3ffffff0:` (:624); the early
  windows (fuse ROM 0x43000000, NVRAM 0x45000000 and 0x47000000, tri-port RAM 0x71000000) lie above it.  The case is
  `cpu->cd.m88k.cmmu[1]->reg[CMMU_PFSR] = CMMU_PFSR_BERROR << 16; break;` (:626-627; data CMMU always, no NULL test),
  and `break` reaches the tail `if (writeflag == MEM_READ) memory_writemax64(cpu, data, len, odata); return 1;`
  (:927-930) with `odata` 0.  The only returns: `return 1;` at :575, :587, :597, :607, :619, :930 and `return 0;` at
  :924 (in `default:`, after `cpu->running = 0;`); every case from :629 to :907 ends `break;`.

---

## 6. PREMISES STATED AS QUESTIONS -- check these; ratification is not wanted

* **P1 -- a fourth product file (S16).**  No seat, the ruling, nor the witness's list of "the three files the round
  will edit" (memory_rw.c, dev_luna88k.c, dev_m8820x.c; 2.1) names an include, and I read the repair as written as NOT
  COMPILING in the m88k unit without one.  Right?  If so, the placement on record is upstream's (cpu_m88k.c, 3.4):
  does m8820x.h (`BATC8`/`BATC9`, `INST_CMMU`/`DATA_CMMU`, `MAX_CMMUS`, `NBSG`, the `CMMU_*` family) collide with
  anything visible in cpu_m88k.c, and does cpu_m88k.c join the edit set (S17)?
* **P2 -- PFAR's low two bits.**  `orig_paddr` is the BYTE address, DMA0 the WORD address (S10), the data P bus carries a
  word address plus byte enables, and no MC88200 manual is on disk (S12).  After a byte or halfword bus error at a
  non-word-aligned address: `orig_paddr` (upstream's choice, 3.4) or `orig_paddr & ~3`?  The witness rows are all
  aligned words (sub-word is NOT CLAIMED).  Recorded with its warrant?  A sub-word row owed?
* **P3 -- the sibling.**  The translation path resets the other CMMU's PFSR (S9); the ruled bus-error path leaves it
  (Grok: "Do not clear the sibling"; the four `icmmu` rows pin `kept`).  OpenBSD 2.2 snapshots both PFSRs and its
  user-fault path branches on EITHER being BERROR (S11).  Can a stale sibling change what that guest does where a reset
  one would not?  Is `kept` right, and on what warrant?
* **P4 -- the NULL check.**  My reading of S7: no guest-reachable refused access by a cpu with a NULL `cmmu[]` slot exists
  on an unmodified machine (testm88k's one candidate, dev_fb.c:719-721, is fenced by `#182`'s length update).  If so the
  check rests on a TRANSFERRED WARRANT (upstream r6577(e); memory_m88k.c:131-132)
  under R13, and its variants (removed; the exception moved inside it) are unobservable at rung 3.  Check; name any
  configuration that reaches it.
* **P5 -- the instruction label of the selector the fix ADDS.**  Data label rowed.  Instruction label: free-running, the
  fetch raises vector 2 and the cpu stops before the vector's first instruction (R1); stepped, the exception comes from
  the debugger's pre-read (R2).  (i) row it stepped through R2's path, (ii) disclose under clause (e), (iii) sequence R1
  first?  Does (i) make a row depend on a defect a later round removes?
* **P6 -- the `no_exceptions` cell of the arm's guard.**  The witness's NOT CLAIMED reason ("the debugger's
  put/dump/unassemble never reach a DM_DEFAULT handler, memory_rw.c:584") is about the DEVICE CALL (:584-585); the guard
  still evaluates `!no_exceptions` with `res` forced to -1 (:595-596, :603), and debugger reads are
  `CACHE_NONE | NO_EXCEPTIONS` (S5).  Is that cell reachable in the witness's session shape?  A row owed?
* **P7 -- VA differs from PA.**  Astra requires it (3.2); every witness session runs untranslated (S9).  R5 draws swaps
  only from body-read fields: the m88k arm reads `cache` and (in `debug()`) the device-relative `paddr`; `vaddr` is read
  only in the compiled-out `MEM_MIPS` block -- so PFAR := `vaddr` is outside the (d) enumeration by the letter.  Owed
  anyway?  Is translation-on reachable in the session shape on unmodified mvme187 (the guest can store SAPR and BWP0-7
  via dev_m8820x.c :367-435, :463-486; the BATC lookup precedes the walk, memory_m88k.c:152-180)?
* **P8 -- the LUNA half changes what a booting guest sees.**  HEAD serves a load at 0x3ffffff0; after the fix it faults.
  Upstream's replacement says "Guest OSes such as OpenBSD probe memory by reading 0x3ffffff0." (3.4).  No OpenBSD/luna88k
  source is on disk.  Is a before/after boot-to-`login:` measurement on the luna rig owed (gate 7 boots it; it is part of
  the full battery, not a round's targeted gate unless the round runs it)?
* **P9 -- three in-code records go stale.**  dev_m8820x.c: "the model writes only PFSR and PFAR (memory_m88k.c:382-405)"
  (:293-294); "the fault path writes PFSR (memory_m88k.c:382-384, dev_luna88k.c:614) and PFAR (memory_m88k.c:399,405 ..."
  (:325-327; `:614` is ALREADY stale -- the write is at :626); "PFSR and PFAR written at :382-405" (:500-501); plus
  memory_rw.c's TODO (:615-619).  Corrected in THIS diff (L4), making dev_m8820x.c a comment-only edit site?
* **P10 -- the LUNA label's other cells.**  A store and any width reach the case (S19); the witness rows a word load.
  The new body tests neither; direction is rowed at mvme187 (`ust`).  Store row owed at the LUNA label, or clause (e)?
* **P11 -- the accept row.**  Grok: "a population-2 decline still returns success and does not write PFSR"; the witness
  uses the CASED VME VBR (`ok route`, `ok regs`).  Both served.  Sufficient, or is a population-2 row owed?
* **P12 -- the translation-fault accept control.**  The ruling forbids changing memory_m88k.c's PFAR semantics; no
  detector reads PFSR/PFAR (S15).  Owed by THIS diff, which does not touch memory_m88k.c, or outside the floor (rows are
  owed per enumerated variant of the diff, R7, R9)?

---

## 7. The drafter's partition of the arm and the LUNA case -- CHECK IT

*The predicates DOMINATING the edited lines (R5 clause 1), the two the fix ADDS, and the lvalues the guarded body reads
with the partition the body induces (R9).  15 axes.  "unrowed" is a status, not a verdict.*

| # | axis (where) | cells | held by | status |
|---|---|---|---|---|
| 1 | claim (scan :479-634) | claimed / unclaimed | INFO `unclaimed` | unclaimed is not this arm (S3, R3) |
| 2 | device call (:584-585) | called / not (`no_exceptions` + DM_DEFAULT) | -- | = P6 |
| 3 | cpu stopped by device (:591-592) | stopped / running | -- | returns before the arm; session ends -- unobservable |
| 4 | `res <= 0` after `0 -> -1` (:595-603) | served (>= 1) / refused (-1); 0 mapped away | `ok` rows / every refused row | both D2 edges rowed (R8) |
| 5 | `!no_exceptions` (:603) | clear / set | clear: all scored rows | set = P6, unrowed |
| 6 | the ADDED selector `cache == CACHE_INSTRUCTION ? 0 : 1` | instruction / other | other: uld, ust, vme, luna | instruction = P5, unrowed |
| 7 | the ADDED NULL check | non-NULL / NULL | non-NULL: all refused rows | NULL = P4, none reachable found |
| 8 | `writeflag` (`debug()` only, :605) | read / write | read: uld, vme, luna; write: ust | LUNA write = P10 |
| 9 | the refusing device (`debug()`, :607) | `unreadable` / VME pop. 1 / LUNA case | uld+ust / vme / luna | rowed |
| 10 | PFAR's operand (verbatim) | body-read swap: `paddr` (relative) | 0x10, 0x90, 0x0 vs absolute | rowed; `vaddr` = P7 |
| 11 | PFSR value (constant) | 0x00030000 / other | every refused row | rowed |
| 12 | sibling CMMU (not written) | kept / changed | four `icmmu` rows | rowed as kept -- P3 |
| 13 | width, alignment (not tested by the arm; clamp :495-524) | b/h/w/d; aligned / not | aligned word only | P2; sampled |
| 14 | which cpu | cpu 0 / 1..3 (luna `-n`) | cpu 0 | NOT CLAIMED |
| 15 | LUNA dispatch (`switch (addr)` :622) | the case / other labels / `default:` (stops cpu) | luna rows, word load | rowed for a word load |

**Floor reading (mine, check it against R7):** dominating predicates = rows 2-5; the device-state lvalue the repair
reads = the `cmmu[]` pointer (row 7); the fix ADDS rows 6 and 7, whose labels clause (d) weakens (R4).  Floor =
{refused, `no_exceptions` clear} x {data, instruction} x {non-NULL, NULL}, plus the served and `no_exceptions`-set cells.
The witness holds {refused, clear, data, non-NULL} and {served}; the rest are P5, P4, P6.

---

## 8. SOURCE, INLINED -- line numbers as read at HEAD `7fca7187` (COMPACT: the two edit regions whole, the rest carried by the premise lines cited)

*The FULL form inlines both enclosing functions whole (the sketch rule).  What is elided here is carried by S1-S3, S8-S10, S19, P9 and 2.7.*

### 8.1 `src/cpus/memory_rw.c` -- `MEMORY_RW_ONE_PAGE`: the device call, the arm, and the function's last lines
~~~~
  582| 
  583| 				res = 0;
  584| 				if (!no_exceptions || (mem->devices[i].flags &
  585| 				    DM_READS_HAVE_NO_SIDE_EFFECTS)) {
  586| 					bool running_before_device_access = cpu->running;
  587| 					res = mem->devices[i].f(cpu, mem, paddr,
  588| 					    data, len, writeflag,
  589| 					    mem->devices[i].extra);
  590| 
  591| 					if (running_before_device_access && !cpu->running)
  592| 						return MEMORY_ACCESS_FAILED;
  593| 				}
  594| 
  595| 				if (res == 0)
  596| 					res = -1;
  597| 
  598| 				/*
  599| 				 *  If accessing the memory mapped device
  600| 				 *  failed, then return with an exception.
  601| 				 *  (Architecture specific.)
  602| 				 */
  603| 				if (res <= 0 && !no_exceptions) {
  604| 					debug("[ %s device '%s' addr %08lx "
  605| 					    "failed ]\n", writeflag?
  606| 					    "writing to" : "reading from",
  607| 					    mem->devices[i].name, (long)paddr);
  608| #ifdef MEM_MIPS
  609| 					mips_cpu_exception(cpu,
  610| 					    cache == CACHE_INSTRUCTION?
  611| 					    EXCEPTION_IBE : EXCEPTION_DBE,
  612| 					    0, vaddr, 0, 0, 0, 0);
  613| #endif
  614| #ifdef MEM_M88K
  615| 					/*  TODO: This is enough for
  616| 					    OpenBSD/mvme88k's badaddr()
  617| 					    implementation... but the
  618| 					    faulting address should probably
  619| 					    be included somewhere too!  */
  620| 					m88k_exception(cpu, cache == CACHE_INSTRUCTION
  621| 					    ? M88K_EXCEPTION_INSTRUCTION_ACCESS
  622| 					    : M88K_EXCEPTION_DATA_ACCESS, 0);
  623| #endif
  624| 					return MEMORY_ACCESS_FAILED;
  625| 				}
  626| 				goto do_return_ok;
  627| 			}
      [... 628-783: the scan's step, the MIPS cache path, the RAM path (:662-713 is S3's unclaimed path) ...]
  784| do_return_ok:
  785| 	return MEMORY_ACCESS_OK;
  786| }
~~~~
### 8.2 `src/devices/dev_luna88k.c` -- `DEVICE_ACCESS(luna88k)`: the switch's first case, `default:`, the tail
~~~~
  556| 	struct tm *tmp;
  557| 	time_t timet;
  558|  	uint32_t addr = relative_addr + LUNA88K_REGISTERS_BASE;
   ...
  622| 	switch (addr) {
  623| 
  624| 	case 0x3ffffff0:
  625| 		/*  Accessed by OpenBSD/luna88k to trigger an illegal address  */
  626| 		cpu->cd.m88k.cmmu[1]->reg[CMMU_PFSR] = CMMU_PFSR_BERROR << 16;
  627| 		break;
  628| 
      [... 629-908: every case ends `break;` (S19) ...]
  909| 	default:
  910| 		if (writeflag == MEM_WRITE)
  911| 			debugmsg_cpu(cpu, SUBSYS_DEVICE, "luna88k", VERBOSITY_ERROR,
  912| 		    	    "unimplemented %i-bit WRITE to address 0x%x: 0x%x",
  913| 		    	    len * 8,
  914| 			    (int) addr,
  915| 			    (int) idata);
  916| 		else
  917| 			debugmsg_cpu(cpu, SUBSYS_DEVICE, "luna88k", VERBOSITY_ERROR,
  918| 		    	    "unimplemented %i-bit READ from address 0x%x",
  919| 		    	    len * 8,
  920| 			    (int) addr);
  921| 
  922| 		// Stop the emulation immediately.
  923| 		cpu->running = 0;
  924| 		return 0;
  925| 	}
  926| 
  927| 	if (writeflag == MEM_READ)
  928| 		memory_writemax64(cpu, data, len, odata);
  929| 
  930| 	return 1;
  931| }
~~~~
### 8.3 `src/cpus/tmp_m88k_tail.c` -- where `memory_rw.c` is compiled for m88k, and `cpu_m88k.c`'s includes (S16)
~~~~
   38| #define MEMORY_RW m88k_memory_rw
   39| #define MEM_M88K
   40| #include "memory_rw.c"

src/cpus/cpu_m88k.c:
   53| #include "thirdparty/m8820x_pte.h"
   54| #include "thirdparty/m88k_dmt.h"
   55| #include "thirdparty/mvmeprom.h"
~~~~
### 8.4 The guest reader -- OpenBSD 2.2 mvme88k (OUTSIDE the repository; absolute paths)
~~~~
C:\DocumentNoSnc\cc\GXEMUL\_guest-src-openbsd22\sys\arch\mvme88k\mvme88k\trap.c:
  326| 	if ((frame->dpfsr >> 16 & 0x7) == 0x3 && 		/* bus error */
  327| 		(frame->sxip & ~3) >= (unsigned)&guarded_access_start &&
  328| 		(frame->sxip & ~3) <= (unsigned)&guarded_access_end) {
  329| 
  330| 		frame->snip = ((unsigned)&guarded_access_bad    ) | FIP_V;
  331| 		frame->sfip = ((unsigned)&guarded_access_bad + 4) | FIP_V;
  332| 		frame->sxip = 0;
  333| 		frame->dmt0 = 0;/* XXX what about other trans. in data unit */
  334| 		frame->dpfsr = 0;
  335| 		return;
  336| 	}
   ...
  405| 	if ((frame->ipfsr >> 16 & 0x7) != 0x3 &&
  406| 		(frame->dpfsr >> 16 & 0x7) != 0x3) {
  407| 
  408| 		result = vm_fault(map, va, ftype, FALSE); 
  409| 		frame->ipfsr = frame->dpfsr = 0;
  410| 
  411| 	}

C:\DocumentNoSnc\cc\GXEMUL\_guest-src-openbsd22\sys\arch\mvme88k\mvme88k\eh.S:
  311| #define Data_Precheck \
  312| 	bb1.n   FLAG_IGNORE_DATA_EXCEPTION, FLAGS, ignore_data_exception
   ...
 1013| 	or.u	TMP, r0, hi16(CMMU_I)
 1014| 	ld	TMP2, TMP, lo16(CMMU_I) + 0x108
 1015| 	st	TMP2, r31, REG_OFF(EF_IPFSR)
 1016| 	or.u	TMP, r0, hi16(CMMU_D)
 1017| 	ld	TMP2, TMP, lo16(CMMU_D) + 0x108
 1018| 	st	TMP2, r31, REG_OFF(EF_DPFSR)
~~~~
*`memory_m88k.c`'s fault writers (S9), `m8820x.h` (S8) and the MC88100 passages (S12) are quoted in the premises; the FULL form inlines them.*

---

## 9. Detector-shape facts for Q3 (VERBATIM excerpts at HEAD)

* **Gates** (`regress/run.sh`:10): 1 build, 2 offline, 3 selftest_mutation, 4 mips, 5 crossfamily, 6 hygiene, 7 ab,
  8 upstream, 9 asan_sweep, 10 sh_rounding, **11 m88k_rounding**, 12 mips_rounding, 13 ppc, **14 arm**, 15 ppc_halt,
  16 mips_folds.
* **Gate 14** needs only the binary, but skips WHOLE if its first probe (`arm_flags_probe.py`) prints no result line
  (`gate_arm.sh`:100-106); it already runs five mvme187 probes (pcc2_width, pcc2_default, pcc2_c040, mk48_nvram and
  `#568`'s `vme_default_probe.py`, whose session shape the witness copied; :1800-1898).
* **Gate 11** (the m88k gate: m88k_rounding, m88k_idle, m8820x_sites, luna_intmask, m88k_exc, luna_absentcpu) skips
  WHOLE without the luna RIG IMAGE (`gate_m88k_rounding.sh`:32-39) or if its first probe prints no result (:45-51).  The
  witness probe needs no image by default; with an images directory it runs the LUNA session in the rig shape
  (identical rows).
* **Gate 6** counts `endswith(` and pty-driving tokens in non-artifacts `regress/**/*.py` (`gate_hygiene.sh`:151-153,
  :728-730); the probe has none (grep), so moving it should move no gate-6 pin (deriver: `tools/derive_hygiene_pins.sh`).
* **`check_probe_wiring.py`** reds an unlisted tracked-or-staged `.py` anywhere under `regress/`, artifacts included.
  `#568`'s detector line (HEAD):

~~~~
 2862|     "vme_default_probe.py":
 2863|         (CLASS_DETECTOR, "#568 vmedefaultkill: 38 rows on unmodified -E mvme88k -e mvme187 (rev 3); gated in gate_arm.sh (gate 14) under the stem vme_default, pinned at 38; kill table 2 ... [CONDENSED: the rest of the line records that table's scores]"),
~~~~
* **`#568`'s gate-14 pins -- the row-identity form for a probe whose row names contain spaces** (`regress/gate_arm.sh`, HEAD; line 1907, elided, is `for v in "neg apparatus" "session" ... "unasm"; do` naming all 38 rows):
~~~~
 1899| if ! grep -q "VME_DEFAULT_PROBE_DONE" "$VMEDLOG"; then
 1900|     check "vme default probe completed" "no" "yes"
 1901| else
 1902|     check "vme default probe completed" "yes" "yes"
 1903|     vres=$(sed -n 's/^VME_DEFAULT_RESULT=//p' "$VMEDLOG")
 1904|     check "vme_default rows run"     "${vres#*/}" 38
 1905|     check "vme_default rows correct" "${vres%/*}" "38"
 1906|     check "vme default controls" "$(grep -c '^VME_DEFAULT_CONTROL=OK$' "$VMEDLOG")" "1"
   ...
 1908|         check "vme default row: $v" "$(count "$VMEDLOG" "^$v  .*ok$")" "1"
 1909|     done
 1910|     check "vme default rows emitted" "$(( $(count "$VMEDLOG" " ok$") + $(count "$VMEDLOG" " FAIL$") ))" "38"
 1911|     check "vme default rows green"   "$(count "$VMEDLOG" " ok$")"   "38"
 1912|     check "vme default rows red"     "$(count "$VMEDLOG" " FAIL$")" "0"
 1913| fi
~~~~
* **`#569`'s gate-2 pins** -- the id lists held in the GATE, never read from the driver; every row by identity, exactly once; the denominator pinned by literal equality (`regress/gate_offline.sh`, HEAD):
~~~~
  205|     sed 's/^/       /' "$MLSLOG"
  206|     check     "m88k loadstore generator: row failures" \
  207|               "$(sed -n 's/^ROWS=[0-9]* FAIL=\([0-9]*\)$/\1/p' "$MLSLOG")" "0"
  208|     check     "m88k loadstore generator: rows run (the denominator is the pin)" \
  209|               "$(sed -n 's/^ROWS=\([0-9]*\) FAIL=[0-9]*$/\1/p' "$MLSLOG")" "123"
  210|     check     "m88k loadstore generator: completion sentinel" \
  211|               "$(grep -c '^M88KLS_DONE$' "$MLSLOG")" "1"
   ...
  228|     for _id in $_mls_ids; do
  229|         check "m88k loadstore generator: row $_id, exactly once" \
  230|               "$(grep -ow -- "$_id" "$MLSLOG" | wc -l | tr -d ' ')" "1"
  231|     done
~~~~
* **The gate library** (`regress/lib.sh`): `check` compares strings for equality, `check_min` is `-ge`, and `count FILE PATTERN` is `grep -ac -- PATTERN FILE` (:80-82, :91-93, :326-330).

---

## 10. The project rules the questions apply -- quoted with their bounds (load-bearing lines only)

**Provenance:** the WORKING-TREE carrier `GXEMUL-SEC/tools/CLAUDE.md` (4104 lines; HEAD's 3846-line copy lacks R2's
block and R8, adopted by owner ruling 2026-10-09).  Each block is VERBATIM; a block shorter than the FULL form's says
which lines it keeps.

**R1 -- THE FLOOR** (lines 1328-1333):
~~~~
> **THE FLOOR.** A detector is VACUOUS — replace it IN-ROUND — unless it (a) fails on the
> pre-fix build, (b) fails on a **VERBATIM REINSTATEMENT of the removed defect at EVERY fixed
> site**, and (c) fails on a **NULL MEDIUM** -- a product medium carrying none of the behaviour under
> test (the clause-(c) block below says what that is per instrument kind). Below the floor, the
> round's own claim to have "shipped a detector with the fix" is a WRONG RECORD, which the
> stopping rule already fixes in-round.
~~~~
**R2 -- clause (c): the runtime-probe null medium; the pre-fix build; the two record forms** (lines 1345-1346, 1350-1352, 1358-1367):
~~~~
> * a runtime probe: an ABSENT or NON-EMULATOR binary (every session dies), or a build WITHOUT the
>   device for a device round;
   ...
> **THE PRE-FIX BUILD IS CLAUSE (a)'S MEDIUM AND NEVER CLAUSE (c)'S.**  It carries every behaviour of the
> product, one of them wrong, so a detector can red on it and still pass a comment-only file -- `#446`,
> the instance that created this clause.  A table that wrote "null medium" over a pre-fix leg carries a
   ...
> **RECORD CLAUSE (c) IN ONE OF EXACTLY TWO FORMS, never as a bare clause letter beside a row name:**
> * `(c): measured at <artifact>` -- the leg was run and its receipt is durable;
> * `(c): by construction via <row/pin>, leg not run` -- e.g. the gate pins the row count by EQUALITY
>   and a named row reds on a dead run, or the differential `#include`s the product and its gate reds
>   on a compile failure.  **A by-construction claim is checked by READING that shape; where the reading
>   fails -- no runtime gate wiring, no pin, `check_min`, a control computed over the row list
>   (`all([])` is True) -- the leg is OWED** (7n-1's two: the unwired `ppc_rldicl_probe.py` and
>   `alpha_tbi_probe.py`).  Predict a dead run's score from the source, not from the row count (Astra
>   measured luna's at 0/14 with four gate checks red, and SGI's at 6/46 because six rows test only
>   exit status).
~~~~
**R3 -- clause (d)** (lines 1376-1377):
~~~~
> **(d) The detector must also fail when the fix is PRESENT but its REPAIR IS NULLED —
> the guard kept, its effect removed.**
~~~~
**R4 -- the first (d) shape** (lines 1429-1429):
~~~~
> * **fix ADDS a predicate** -> weaken the added one (unchanged; the original rule).
~~~~
**R5 -- the DEPENDS-ON bound** (lines 1448-1451):
~~~~
> > **DEPENDS ON enumerates exactly two things: (1) the predicates DOMINATING the diff's
> > edited lines, walked up only to the ENCLOSING FUNCTION BOUNDARY -- never into callees
> > or callers; and (2) for operand-swap forms, swaps drawn ONLY from fields the guarded
> > BODY reads (the guard-field/body-field grep the pre-table check already mandates).**
~~~~
**R6 -- joint cells: the body-tested partition** (lines 1464-1472):
~~~~
> > **DEPENDS-ON enumerates JOINT cells over the guard's operands and the body-read lvalues EXACTLY
> > WHEN THE GUARDED BODY'S OWN CODE DISTINGUISHES THEM.**  For each lvalue take the PARTITION the
> > body's own tests induce (`pending > 0` gives {0, >0}; `relative_addr == PCCTWO_T1ICR` gives
> > {T1, T2}); the enumerated cells are the CROSS-PRODUCT of those partitions -- never arbitrary
> > boolean functions of the read-set.  A mutant exempting a single cell whose reachability is
> > MEASURED is a floor breach; close the whole cross-product in ONE diff and write into the
> > contract which cells are rowed.  A value or combination the body never tests as a case
> > (`idata == k`; a byte no conditional distinguishes; both counts >= 2 where the body tests `> 0`)
> > is DISCLOSED under clause (e).
~~~~
**R7 -- the floor versus clause-(e) disclosure** (lines 1517-1522):
~~~~
> > **The rule ENUMERATES joint cells wherever the body distinguishes them; the FLOOR -- the cells a row
> > is OWED for -- is the cross-product of the guard's dominating predicates with the device-STATE lvalues
> > the fix's own repair path reads that are JOINTLY REACHABLE through its own data flow.**  The bits of
> > the single value being written are single-operand MARGINALS, not floor; joint cells outside the floor
> > are clause-(e) coverage debt, subject to the one ask-again.  A filter may reject or discharge a cell
> > but may demand a new row only for a floor cell -- so it cannot grow unbounded.
~~~~
**R8 -- rule D2** (lines 1557-1560):
~~~~
> > For a relational compare against a constant bound B that a fix DEPENDS ON (`X > B`, `e < 96`), each region of its
> > generating set is discharged by the row that varies under the LEAST-OBSERVABLE non-equivalent move of B: **X = B+1
> > for the region past the bound and X = B-1 for the region below it** (the "at" member is dead where the branch maps B
> > to itself).  **A far row proves the branch EXISTS and discharges the BRANCH partition; it never pins the BOUND.**
~~~~
**R9 -- the CHANNEL line** (lines 1741-1741):
~~~~
> | **CHANNEL** | for each row, name **the mutant it kills** and **the observable that differs under that mutant**. A row whose named channel cannot vary under its named mutant is VACUOUS BY CONSTRUCTION, and that is knowable at writing time, before any table runs | a survival oracle at a REFUSAL-EFFECT site: guarded and unguarded code both survive |
~~~~
**R10 -- clause (e): the contract** (lines 1801-1805):
~~~~
> **(e) THE CONTRACT.** The probe header names which edits this detector is designed
> to catch. *A detector that says so is falsifiable; one claiming completeness is
> not* -- and a later escape becomes "outside the contract" or "a breach of it",
> which are different dispositions, rather than an argument about overclaiming.
> Two lines in a header.
~~~~
**R11 -- clause (f): the anchor rule and its reviewer check** (lines 1814-1817, 1897-1898):
~~~~
> **Rows that assert only PAIRWISE DISTINCTNESS, or a same-path round-trip, test the decode
> against ITSELF.** They are therefore invariant under any edit that re-maps addresses
> INJECTIVELY over the probed set -- translations first among them -- and they catch a re-map
> only where it COLLIDES on that set.
   ...
> > ***"If every address in this device shifted one word, which row reds?"*** If the answer is
> > NONE, position is unpinned, whatever the row count.
~~~~
**R12 -- FAULT, and its availability on M88K** (lines 2036-2039, 2052-2057):
~~~~
> > this set said. ***  FAULT works because `memory_rw.c` dispatches an exception on a failed device access --
> > **for MIPS and M88K.  There is no Alpha equivalent.**  So `dev_unreadable.c`, which `machine_sgi.c`
> > installs ten times, does not transfer to an Alpha machine at all, and a round reaching for FAULT there owes
> > Alpha exception delivery first.
   ...
> > * **5 FAULT** -- deliver the architectural bus error, by MODELLING THE SPACE AS UNMAPPED.
> >   `src/devices/dev_unreadable.c` is a device whose entire access function is `return 0;`
> >   ("returns an error for all reads/writes"), and `machine_sgi.c` installs it TEN times so
> >   absent hardware faults, because the PROM and NetBSD probe those regions and RELY on the
> >   failure.  **This is why *`return 0` is not a decline* and *FAULT is a member* are both
> >   true: it is not a refusal, it is a positive statement that nothing is there.**
~~~~
**R13 -- the addition licence** (lines 2334-2335):
~~~~
> > **Additions to product code in a hardening fork are licensed by MEASURED DELTAS or by a
> > TRANSFERRED WARRANT -- never by "it cannot hurt."**
~~~~
**R15 -- the ask-again cap** (lines 2471-2475):
~~~~
> **CAPPED AT ONE ASK-AGAIN PER DETECTOR PER ROUND.** This is not the #392 chain — #392 was
> unbounded fix-of-fix passes with no stop condition; this is a single extra adversarial query
> against a clean table with a measured stop: nothing found, done; something found, row added
> under L1, done. **The cap IS the anti-#392 clause.** A second ask-again after an empty first
> is exactly where the chain starts, and anything found past the cap is FILED, never fixed.
~~~~
*R14 (witness clauses) is in the FULL form.  Not binding: de-escalation and accept-row failability (they bind a diff that deletes an `exit(`).*

---

## 11. QUESTIONS -- VERDICT LINE FIRST (format in section 0)

**Q1 -- the repair: complete and correct?**
(a) Is `cpu->cd.m88k.cmmu[cache == CACHE_INSTRUCTION ? 0 : 1]` right for every caller that can reach the arm (S5, S6)?
Name any caller the selector misroutes.  Multi-cpu luna: the arm uses the FAULTING cpu's CMMU, dev_m8820x.c serves
each CMMU from `d->cpu_nr` (S8) -- consistent?
(b) PFSR = 0x00030000 (S8; the translation path's `<< 16` encoding, S9) and PFAR = `orig_paddr` (S1): answer P2 with a
warrant, or say UNKNOWN.
(c) The NULL check around the two writes only, the exception outside: answer P4 -- reachable anywhere?  If not, is it
licensed (R13) and its variants disclosed rather than rowed?
(d) The vector expression, the `!no_exceptions` guard, the `debug()` line and `return MEMORY_ACCESS_FAILED` stay (S2).
Does the ruled design move any of them?
(e) The LUNA case becomes `return 0;`, its write deleted, the case kept (S19; deleting it reaches `default:`, which stops
the cpu, S3).  `return 0` skips the common tail, which only writes the read buffer `memory_rw` already zeroed and a
failing load never consumes (S10).  Confirm the path (:591-592 does not fire; `res` 0 -> -1; data CMMU; vector 3) and
say what changes for a STORE and for an instruction fetch at 0x3ffffff0 (P10).
(f) Answer P1.  (g) Answer P9; is the TODO (:615-619) replaced?
(h) Only a CLAIMED-and-REFUSED access reaches the arm (S3): unclaimed addresses get nothing, and on luna-88k only the
probe case reaches it.  What may the CHANGELOG and probe contract claim -- and disclaim -- about "88K bus errors"?
(i) Answer P3 and P8.
(j) Option set for the LUNA disposition (R12; FAULT works on M88K): (1) keep `return 1` and add PFAR -- ACCEPT with
metadata, no exception; (2) `return 0` into the arm -- FAULT, the ruling's choice; (3) upstream's `DEV_RAM_FAIL` device
-- FAULT by another device, refused; (4) delete the case -- `default:` stops the cpu, refused.  A member not named?  Grep
the fork for the idiom (`dev_unreadable.c` is the FAULT idiom; machine_mvme88k.c installs it three times, S4).

**Q2 -- the owed rows: complete, consistent, bounded?**
(a) Clause (a) = the witness (8 of 24 red, SYMPTOM PRESENT 8/8); the post-fix half (same script all green, ABSENT) is
owed.  Anything else?
(b) Clause (b) at EVERY fixed site.  My prediction, to be checked: reinstating the ARM alone (LUNA case fixed) reds the
six uld/ust/vme pfsr+pfar rows AND `luna pfsr` and `luna pfar` (the fixed case routes through the arm), `luna route`
staying green; reinstating the CASE alone (arm fixed) reds `luna route` and `luna pfar`, `luna pfsr` green.  Correct?
Any row red for the wrong reason?
(c) Clause (c) (R2): which null medium -- an absent or non-emulator binary, or "a build WITHOUT the device" (which
device?) -- and which of the TWO record forms?  A dead binary reds every scored row without claiming a cause (2.12) and
the exit is non-zero, but no gate pin exists yet (Q3).  Predict a dead run's score from the source.
(d) Clause (d): check section 7 against the code -- a missing dominating predicate, a wrong partition, a mislabelled
cell?  For each unrowed cell (P4, P5, P6, P7, P10, row 13 = P2): FLOOR (owed, R7) or CLAUSE (e) (disclosed with its
derivation)?
(e) For each variant the records name, which row reds -- or none, and is that a floor breach or disclosed debt?  From
the probe header (2.11): writes on cmmu[0] instead of cmmu[1]; raw 3 instead of `3 << 16`; device-relative `paddr` in
PFAR; PFSR-only; writes on BOTH CMMUs; the sibling cleared; conditioned on direction; keyed to one device; the exception
dropped; the writes outside `res <= 0`; `res <= 0` -> `res <= 1`; the LUNA case left returning 1; the LUNA write deleted
with the case still returning 1.  From Grok (3.3): "stores the device offset", "writes only cmmu[0] on a data access",
"stores raw 3".  From the NOT CLAIMED list: the NULL check removed or the exception moved inside it; PFAR := `vaddr`; a
sub-word address in PFAR.
(f) Answer P11 and P12.  Is `ok regs` the right channel for "a served access leaves PFSR/PFAR untouched"?
(g) R11: PFAR is pinned by absolute physical address at three device-relative offsets (0x10, 0x90, 0x0), PFSR by exact
value, the sibling by four exact seeds.  "If every address in this device shifted one word, which row reds?"
(h) R8: the one compare against a constant is `res <= 0` (B = 0; B+1 served = `ok` rows; B-1 refused = every refused
row; the at-B member mapped away).  Discharged?  Any other constant compare among the dominating predicates?
(i) R9, row by row: does each row's channel vary under its named variant?  Check especially `luna pfsr` (under which
variant does it red that no generic row also reds?) and the four `route` rows (which variant reds each?).
(j) Closed over the diff (R5, R7), with one ask-again after a clean table (R15)?

**Q3 -- detector shape and gate home**
(a) The probe moves to `regress/m88k_buserr_probe.py`, post-fix green with the same script.  Must anything in its header
(contract, NOT CLAIMED, the `icmmu` wants) change first?
(b) Gate 14 (binary only; hosts `#568`'s probe, which this one copied) or gate 11 (the m88k gate; skips whole without
the luna rig image) -- section 9.  Which, with which LUNA shape, and at what cost when the gate's first probe or image is
missing?
(c) MANIFEST lines in check_probe_wiring.py: `CLASS_DETECTOR` for `regress/m88k_buserr_probe.py`, and `CLASS_WITNESS`
for `artifacts/m88kbuserrregs/witness_20261023/m88k_buserr_probe.py` if that directory is committed (`#568`'s precedent).
Right?  Any other `.py` there the checker will see (the seat stored its scripts as `*.py.txt`)?
(d) Row identity as `#569` did it: the row list held in the GATE, every row by identity exactly once, the denominator by
literal equality, red = 0, CONTROL=OK, SYMPTOM=ABSENT, the sentinel `M88K_BUSERR_PROBE_DONE`.  These names contain
spaces: `#568`'s `count "$LOG" "^$v  .*ok$"` form (which the probe's `%-16s` format and 15-character assert keep
satisfiable) or `#569`'s `grep -ow` form?  A separate check per control?
(e) Ledger witness term `probe:regress/artifacts/m88kbuserrregs/witness_20261023/m88k_buserr_probe.py` (rung 3)?
(f) What must stay green and be measured: `vme_default_probe.py`'s 38 rows (S15) and, P8, the luna rig boot.  Astra
would add "metadata checks for actual faults" to that 38-row detector; the witness carries population 1 in its own
`vme` cell -- which, and does `#568`'s pin move?

**Q4 -- the standing licence.**  If, while verifying a claim, you found something ELSE -- say so.  In particular:
R1 (2.7) -- file it, as what, and is it a PREREQUISITE for the instruction label (P5)?  The source stops the faulting
cpu (cpu_dyntrans.c:2014) and requests the debugger (:2002, :2021); the transcript's "All machines stopped" is a one-cpu
machine.  R2 -- file it; does any COMMITTED stepped probe depend on the pre-read raising an exception?  R3 -- a board
question (`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\vmesbcp2.txt`:341-348 lists "Sources of Local BERR*" and "Bus Error
Processing"; body text not located) -- file or leave?  And anything the drafter got wrong in sections 5-7.

---

## 12. Paths

Every path this brief names was checked to exist at drafting time; the listing is in the FULL form, section 12.

