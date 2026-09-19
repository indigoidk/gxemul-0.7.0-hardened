OPUS_SEAT_ALIVE_20260918_540P1
claude-opus-5[1m] -- "# CHECKPOINT -- 2026-09-18 21:3x   HEAD: cdbe7d7 #537 fbsmlane: #442's harness printed a verdict token its own self-mutant lane could never read -- the lane runs, pinned on R3"
VERDICT: GO-WITH-CHANGES -- the two-token fix is correct and minimal, and (d) is observationally equivalent. The changes are to the detector. The CONTROL=DEAD path prints RESULT=0/0, which an N==M scorer counts as an ESCAPE for (c) and for every host-death mutant. The mirror of (e), PHYSICAL only at ports >= 0x200, sweeps all 13 rows because the witness makes no post-arm access below 0x200.

# #540 lcaisaphys, pass 1: Opus 5 seat

**How I worked:** read-only. No builds, no emulator runs, and no writes except this file.
- **Read in full:** `dev_lca.c`, `memory_rw.c`, `memory_alpha.c`, `lca_isaphys_probe.py`, `cpu_alpha_instr_loadstore.c`, and the witness artifacts.
- **Read in part:** `cpu_alpha_palcode.c` (swpctx and wrfen), `core/memory.c` (the load/store helpers and `memory_warn_about_unimplemented_addr`), `dev_ns16550.c`, `dev_pccmos.c`, `dev_ether.c`, `bus_isa.c`, `cpu_dyntrans.c`, `machine_alpha.c`, `main.c` and `emul.c` for `-M`, and the headers.
- **Scope:** I read beyond the brief's four files but stayed inside the scope the launcher gave me. I did not open any other seat's file in this panel directory.
- **HEAD moved during this pass.** CHECKPOINT.md said `e0be9b2` when I first read it. It now says `cdbe7d7` (#537, the peer session). `git diff --stat e0be9b2 cdbe7d7 -- src/ regress/lca_isaphys_probe.py` is empty, so every line cited below is the same at both commits.
- **Uncommitted change:** the working tree carries a comment-only change to `cpu_alpha_palcode.c`, at line 421 and below. It is after swpctx, so the swpctx line numbers below are the same as HEAD.

---

## Q1 -- PREMISE AUDIT

### 1a. §4: are `CACHE_NONE | PHYSICAL` and bare `PHYSICAL` the same for a device address? Every read of `cache`, enumerated

`CACHE_DATA` = 0, `CACHE_INSTRUCTION` = 1, `CACHE_NONE` = 2 (`include/memory.h:122-124`). So **bare `PHYSICAL` means `cache == CACHE_DATA`, not `CACHE_NONE`.** The two forms carry different `cache` values, and the question is only where that difference is read.

`grep -nw cache cpus/memory_rw.c` finds 8 reads, plus the assignment at :242:

| line | read | compiled for MEM_ALPHA? | reached by a flat ISA address? |
|---|---|---|---|
| :252 | `cache==CACHE_INSTRUCTION ? FLAG_INSTR` in the translate call | yes | **no**: skipped under `PHYSICAL` |
| :610 | `cache == CACHE_INSTRUCTION ? EXCEPTION_IBE : EXCEPTION_DBE` | no (`#ifdef MEM_MIPS`) | n/a. It is on the device-failure path, so MIPS would reach it |
| :620 | `m88k_exception(... cache == CACHE_INSTRUCTION ...)` | no (`#ifdef MEM_M88K`) | n/a |
| :646 | `!(misc_flags & PHYSICAL) && cache != CACHE_NONE` | no (MEM_MIPS MMU3K block) | n/a |
| :649 | `memory_cache_R3000(cpu, cache, ...)` | no (same block) | n/a |
| :698 | `cache != CACHE_NONE && ...` | **never** (inside `#if 0`) | n/a |
| :748 | `update_translation_table(..., cache == CACHE_INSTRUCTION ? ... : ok - 1, ...)` | yes | only on the RAM path |
| :758 | `(ok == 2 && cache == CACHE_DATA)` → `invalidate_code_translation(paddr, INVALIDATE_PADDR)` | yes | only on the RAM path |

The brief's "three `#ifdef` blocks" is right as a count of blocks: they hold four reads. The fifth MIPS read, at :698, is dead everywhere.

**Only three reads compile for Alpha: :252, :748 and :758.** Of those:
- :252 is skipped under PHYSICAL.
- **:748 does not tell 0 from 2**: both are "not CACHE_INSTRUCTION", so both yield `ok - 1`.
- **:758 is the only place where bare PHYSICAL and `CACHE_NONE|PHYSICAL` differ.** On a READ, `CACHE_DATA` calls `invalidate_code_translation`.

Neither :748 nor :758 is reachable from a flat ISA address while `paddr >= physical_max`:
- A device hit returns in the dispatch, at :624 or :626.
- A device miss above `physical_max` returns through the unimplemented-address branch at :663-712.

**So §4's premise holds, but it depends on the RAM configuration.** `-M` accepts 1..1048576 MB (`core/main.c:415-416`), and `physical_max` is MB × 1 MiB (`core/emul.c:459` → `core/memory.c:166`). `0x1d0000000 / 0x100000 = 0x1d00 = 7424`. So:
- **With `-M` ≤ 7424 the two forms are identical on every input.**
- **With `-M` ≥ 7425**, an ISA port with no registered device lands in RAM and reaches :748 and :758. :758 then invalidates code translations for that physical page. `DYNTRANS_INVALIDATE_TC_CODE` returns immediately unless code has been translated from that page, so the only effect is a semantically neutral re-translation. That is still equivalent. See Q2 (d) and residual E2.

### 1b. Could anything on the Alpha path make the nested address legitimately virtual?

**No.**
- The nested address is built inside `DEVICE_ACCESS(lca_isa)` from a device-relative offset. At that point the outer access has already been dispatched by PHYSICAL address (`memory_rw.c:436-481`).
- The nested call is a direct `cpu->memory_rw` slow-path call. The Alpha dyntrans fast path (`LS_N` in `cpu_alpha_instr_loadstore.c`) is only ever keyed by a guest load or store's own vaddr, never by the nested address. The nested call can only WRITE a fast-path entry, and only on the RAM path (see E2).
- `alpha_userland_memory_rw` is compiled (`cpu_alpha.c:670-676`) but never assigned. Nothing references it. Userland mode also has no devices.
- `LCA_ISA_BASE` is an emulator-internal placement with no architectural meaning. `alpha_lcareg.h:45-46` put the architectural sparse I/O space at `0x1c0000000..0x1dfffffff`, so on a real 21066, `0x1d0000000` is sparse offset `0x10000000` (PCI I/O address 0x800000), not a flat ISA alias. No guest OS has any reason to map it. A guest whose page table does map VA `0x1d0000000` does so for its own reasons, such as user memory at 7.25 GiB, and that is the hazard in 1c(ii).
- The brief's snippet elides `memory_alpha.c:75-88`: the `exit(1)` and three remaps. That is harmless here. None of the remap predicates matches `0x1d0000000..0x1d000ffff`:
  - `(vaddr & ~0x7fff) == 0x10000000`: no
  - `(vaddr & ~0x1fff) == 0x20000000`: no
  - `(vaddr & ~0xffffff) == 0xfffffe0000000000`: no
  - `vaddr == 0xfffffffd80000000`: no
- The upstream import already had the defect. `git log -L` on the write arm shows only `39748e3` ("unmodified upstream baseline") and `8bd97e4` (#530, which kept `CACHE_NONE`). Upstream also already had `PHYSICAL` on every other device-to-device nested forward in the tree:

  | file | forward | `PHYSICAL);` at `39748e3` |
  |---|---|---|
  | `dev_pccmos.c` | pccmos → mc146818 | 3 |
  | `dev_ps2_spd.c` | → wdc | 2 |
  | `dev_sh4.c` | SCI | 2 |

  So `lca_isa`'s two calls are the only nested forwards without it: upstream residue, not a policy. That is a stronger warrant than "it is physical by construction".

### 1c. Corrections to §2's premises

- **(i) "The forward works ONLY while ptbr == 0" is missing a condition.** Both identity paths also require kernel mode: `memory_alpha.c:62` and `:73` each test `!userMode`, where `userMode = ps & ALPHA_PSL_USERMODE`.
  - In user mode the inner VA walks even at ptbr == 0. With `base = 0`, physical page 0 is read as an L1 table.
  - The correct statement is "only while ptbr == 0 **and** PS<CM> = kernel".
  - The witness is in kernel mode, and its own arming proves it: a privileged PAL call from user mode halts the CPU (`cpu_alpha_palcode.c:183-191`), and swpctx ran.
  - §5's "K0SEG is identity before any walk" likewise holds in kernel mode only.
- **(ii) §2's outcome list covers only the MISS case.** Reading the walk (`memory_alpha.c:104-197`) gives two more outcomes:
  - **Deeper miss.** In a process context whose L1[0] is valid (any process with user memory below 8 GiB), the walk goes further and also prints `TODO: pte2 not valid.` or `TODO: pte3 not valid.`. That is two unlatched `fatal()` lines per access, not one.
  - **Hit.** The whole port range maps to L1[0] → L2[0x3a0] → L3[0..7]: `0x1d0000000 >> 23 & 0x3ff = 0x3a0`, and `>> 13 & 0x3ff` = 0..7 across 64 KiB. If the current page table maps any of those user VAs, the forward silently goes to that page:
    - kernel ISA reads return that process's bytes;
    - ISA writes land in its memory.

    This is a user→kernel influence channel: while such a process is current, it can forge LSR, PIC, PIT and RTC values. It is derived by reading, not witnessed.
- **(iii) The ISA device list in §2 is incomplete.** `bus_isa_init` also registers a second ns16550 at `+0x2f8` and lpt at `+0x378`. It registers wdc at `+0x1f0`/`+0x170` only when IDE images exist. I checked every registration and all are `DM_DEFAULT`:
  - `dev_8259.c:277-279`
  - `dev_8253.c:386-388`
  - `dev_pccmos.c:149-151`
  - `dev_ns16550.c:353-355`
  - `dev_lpt.c:135-136`
  - `dev_wdc.c:2132-2136`
  - `dev_pckbc.c:1241-1242`
  - `dev_mc146818.c:681-683`

  So §4's `NO_EXCEPTIONS` argument covers the whole window. None of this changes a conclusion.

### 1d. Siblings: the same defect elsewhere?

**In `src/devices/*.c` there is none.** Census method: comments stripped, arguments joined, the 7th argument classified.
- The regex made 60 hits. One is a false match on the string literal in `dev_pccmos.c:103`'s `fatal("[ pccmos: memory_rw() error! ]")`, which leaves **59 calls**.
- **56 pass `PHYSICAL`**: 38 `NO_EXCEPTIONS|PHYSICAL`, 16 bare, 2 `CACHE_NONE|PHYSICAL`. The per-file figures match the brief exactly.
- **3 do not pass it**: `dev_lca.c:301` and `:305` (this defect), and `dev_ether.c:188`.

`dev_ether.c:188` is **not the same class.** The test-machine `DEV_ETHER_MAC` arm writes 6 bytes to a guest-supplied pointer (`idata`). `include/testmachine/dev_ether.h` never says whether that pointer is virtual or physical, so this is an unspecified-ABI question, not a physical-by-construction forward. At most, file it as an ABI note.

**The census is complete for devices because nothing else routes around it.** No device calls the `load_*`/`store_*` helpers (grep: 0) or `translate_v2p` (grep: 0 outside comments).

**Outside devices, the same class exists in the Alpha PAL.** This is found-something-else item E1.

### 1e. Severity: MED or HIGH?

**MED as witnessed. HIGH is justified only with a hit-case witness.**
- **Host impact in every case:** no crash and no memory-safety effect. The cost is one or two unlatched `fatal()` lines per ISA access, and `-q` cannot silence them.
  - One amplification, derived and not measured: a polled console driver waits on `LSR.TXRDY`, which now reads a permanent false 0. Each character then costs the driver's whole poll-timeout loop, and every iteration prints. That turns "one line per access" into "thousands of lines per console character".
- **Witnessed (miss) case:** the guest loses all ISA I/O silently. Reads return 0 with success, and writes are abandoned with no fault (#215). This covers the console, PIC, PIT, RTC (via pccmos), 8042, LPT and IDE.
- **Unwitnessed (hit) case:** guest-integrity corruption across the user/kernel boundary, as in 1c(ii). If the round wants HIGH, it owes that witness, sketched under Q4.
- **Reach:** rung 3 only. Nothing I read suggests an Alpha OS reaches steady-state paging in this emulator: there is no interrupt delivery, per `dev_lca.c`'s #516 comment, and see E1. Rung measures reachability, not harm, so this does not lower the harm ranking.

---

## Q2 -- THE CANDIDATE WEAKENINGS

Each candidate is scored as a mutant applied to the FIXED build (13/13).

Row key:

| # | row | # | row |
|---|---|---|---|
| 1 | alive | 8 | sp lsr ans |
| 2 | live | 9 | sp lsr |
| 3 | flat lsr | 10 | w lands |
| 4 | ram plant | 11 | r miss |
| 5 | ptbr miss | 12 | w miss |
| 6 | ptbr sent | 13 | row count |
| 7 | pte2 todo | | |

| cand | vs the fix | first input where they differ | rows red | result |
|---|---|---|---|---|
| **(a)** PHYSICAL on write only | DIFFERENT | step G: the first post-arm sparse READ (LDBU `SP(0x3fd)`). In general, any sparse read with ptbr != 0 or in user mode | 9 sp lsr, 11 r miss | **KILLED 11/13** |
| **(b)** PHYSICAL on read only | DIFFERENT | step H: the first post-arm sparse WRITE (STB `SP(0x3ff)`) | 10 w lands, 12 w miss | **KILLED 11/13** |
| **(c)** `NO_EXCEPTIONS\|PHYSICAL` on both | DIFFERENT, and broken even at ptbr == 0 | step A: STB 0xaa → `SP(0x64)`. The 8042 handler is skipped (`memory_rw.c:584-585`) and the write reports OK (`:603` falls through to `do_return_ok`). The following LDBU `SP(0x60)` returns the :491 zero-fill | **2 live**, so CONTROL=DEAD, RESULT=0/0, exit 2. No defect row is evaluated. Ungated, sp lsr and w lands would also be red; r miss and w miss would be green | **KILLED only if the scorer treats DEAD / exit != 0 as a kill** |
| **(d)** bare PHYSICAL on both | **EQUIVALENT** | none with `-M` ≤ 7424. With `-M` ≥ 7425, the first READ of a device-less port reaches :758, and that is a no-op unless code was translated from the page | none | **EQUIVALENT. Record the derivation; do not try to kill it** |
| **(e)** PHYSICAL only when `relative_addr < 0x200` | DIFFERENT | step G: the first post-arm access to a port ≥ 0x200 | 9, 10, 11, 12 | **KILLED 9/13**, the same 4 rows as the committed build |
| **(e')** mirror: PHYSICAL only when ≥ 0x200, or any predicate true at both 0x3fd and 0x3ff | DIFFERENT | the first post-arm access below 0x200 (8042, PIC, PIT, RTC, IDE). **The witness makes none** | none | **ESCAPES 13/13** |
| **(f)** PHYSICAL only when `len == 1`, or only when `ofs == 0` | DIFFERENT | the first post-arm `ldl`/`stl`/`ldq`, which covers every width a 21066 driver uses | none. Every witness sparse access is BWX, len 1, so ofs is always 0 | **ESCAPES 13/13** |
| **(g)** forward to `ALPHA_K0SEG_BASE \| (LCA_ISA_BASE+ra)` with no PHYSICAL | DIFFERENT | the first sparse access in user mode. K0SEG identity needs `!userMode` (`memory_alpha.c:62`) | none. The probe never leaves kernel mode | **ESCAPES 13/13** |
| **(h)** virtual first, retry PHYSICAL on failure (a plausible "defensive" edit) | DIFFERENT (hit case) | any post-arm access | 11, 12: the first attempt still prints the miss line | **KILLED 11/13** |

Notes:

- **The candidates no row sees are (e'), (f), (g) and the equivalent (d).**
- **(c) and every host-death mutant take the same apparatus path.**
  - If the host dies at step G, the `print`s never arrive, `live` reads `absent`, and the probe emits `CONTROL=DEAD`, `RESULT=0/0` and exit 2.
  - **A scorer that tests N == M reports that as an ESCAPE**, and host death is the class this fork cares about most.
  - The scorer rule is: ESCAPED only if exit 0 **and** `LCAISAPHYS_RESULT=13/13`; anything else is KILLED, with the red rows or the dead control recorded.
  - The structural alternative: gate on rows 4-7 (plus `flat lsr`, which defines `sp lsr`'s want) and score `live` and `alive` as ordinary rows. (c) then reds `live`, `sp lsr` and `w lands` for 10/13, a row-level kill on three channels.
- **Floor bookkeeping.** This is my reading, for the adjudicator:
  - The fix adds a flag, not a predicate. Inside `DEVICE_ACCESS(lca_isa)`, the predicates dominating the two edited calls are `len == 0` and `writeflag == MEM_WRITE`. `lca_isa` has no device state.
  - So the floor cells are {read, write} × {len > 0}, and both are rowed.
  - Reinstating the defect at each fixed site gives (a) and (b), and both are killed.
  - (e'), (f) and (g) are clause-(e) coverage debt. The body never tests port ranges; it tests `len` only against 0; and `ofs` is off the repair path.
- **Two of the three gaps cost one row each, in the existing session:**
  - **(e'):** repeat the 8042 self-test after swpctx: STB 0xaa → `SP(0x64)`, then LDBU `SP(0x60)` = 0x55. That pins the port axis at a second device below 0x200, with a protocol-reply signature.
  - **(f):** one `ldl SP(0x3fd)` (ofs 1, value `LSR << 8`, masked) and one `stl` of `0x5a000000` to `SP(0x3ff)` (lane 3). **These are the widths a real 21066 driver uses.** The 21066 is implver 0 (EV4; `cpu_alpha.h:61`), and BWX arrived with EV56. The emulator decodes BWX without gating, as #530's own comment says. So the witness proves reachability, but only through instructions the modelled CPU lacks.
  - **(g)** needs a 3-level mapping of the sparse window plus a switch to user mode. Disclose it in the contract rather than rowing it.

---

## Q3 -- OPTION-SET COMPLETENESS

1. **The two `PHYSICAL` tokens.** This is correct and minimal, and independent of both mode and ptbr.
   - At ptbr == 0 in kernel mode it reproduces today's behaviour exactly: the identity mask is a no-op on the range, and none of the four remap/exit predicates match.
   - The #430 split never fires for len 1.
   - It matches the tree's seven sibling device-to-device forwards (1b).
   - Keeping `CACHE_NONE` instead of using bare `PHYSICAL`, as those siblings do, is a minimal-diff choice. By 1a it is equivalent.
2. **Call the target handler directly.** This is a restructuring, and it loses `memory_rw`'s #95 zero-fill, length truncation, watchpoints and the running check.
3. **Register the ISA devices at the sparse window.** Also a restructuring: the byte-lane encoding still needs a shim.
4. **Not named in the brief: forward through the K0SEG alias.** This is WRONG. It works only in kernel mode (:62), still calls the translator, and is invisible to all 13 rows (Q2 (g)). Name it so nobody reaches for it as "the Alpha way".
5. **Not named in the brief: temporarily NULL `cpu->translate_v2p`.** `memory_rw.c:245` treats NULL as physical, so this is the same effect as PHYSICAL achieved by mutating global state. Strictly worse.
6. **`NO_EXCEPTIONS|PHYSICAL`.** Rejected, as in the brief: it skips every `DM_DEFAULT` handler, and 1c(iii) shows that is all of them.

**Member (1) is the smallest correct one.** The only residual left after (1) depends on the RAM configuration, and every PHYSICAL form except (6) shares it (E2).

---

## Q4 -- THE WITNESS

**Do the controls prove what their notes claim? Yes, with three refinements:**
- **`live`** also proves the pre-arm **WRITE** arm: the 0xaa command had to arrive for a 0x55 reply to exist. It is a two-arm liveness control, and its note undersells it.
- **`flat lsr`** is a device signature by construction:
  - `dev_ns16550.c:127` ORs `TXRDY|TSRE` on every access;
  - unbacked space above `physical_max` reads 0 (`memory_rw.c:681-683`).
- **`ptbr miss`** also pins two things:
  - the swpctx TB flush (`cpu_alpha_palcode.c:314`). Without it, step C's identity fast-path entry would serve step F, no miss would print, and the probe would go DEAD;
  - kernel mode (see 1c(i)).
- **`pte2 todo` absent** rules out a stop at L2 but not at L3: `TODO: pte3 not valid.` is never checked. That is harmless given the planted zero L1[0]. Add `TODO: pte3` to the absence test for completeness.

**Is the CONTROL=DEAD gate sufficient? Yes, for its stated purpose,** which is never reading defect rows over an unarmed vehicle.
- `ptbr miss`, `ptbr sent` and `pte2 todo` together establish that a raw VA walks the planted table and misses. Nothing between steps F and H can disarm it: the only PAL call is at step E.
- **As a detector the gate is too broad.** It gates on the liveness rows too, which is the 0/0 hazard in Q2. Split arming controls (gate) from liveness controls (scored).

**Could the defect rows be red for another reason, such as the outer K0SEG access failing? No.** The transcript excludes it four ways:

1. The miss lines carry exactly `0x00000001d00003fd` and `...3ff`. Only `DEVICE_ACCESS(lca_isa)` computes those addresses, so the outer access entered the handler with the right `relative_addr`. A failed K0SEG access would have printed `0xfffffc01...`.
2. `[ writing to device 'lca_isa' addr 00007fe0 failed ]`: the outer store reached the handler (`0x7fe0 = 0x3ff << 5`) and failed because the inner call failed.
3. `sp lsr ans` = completed, with `t6 = 0x0`, not SENT.
   - An outer fault leaves SENT (the #215 early return in `LS_GENERIC_N`).
   - `SENT & 0x60` is also 0. **So `sp lsr` alone cannot tell an outer fault from a false zero; row 8 is what separates them.**
4. The post-arm FLAT observer reached the UART (`read from reg 7`), so K0SEG accesses work after the arm.

**One weak spot, which is witness hygiene rather than a detector gap:** step D's scratch baseline is **0**. That is the same value a failed read zero-fills (#244, #95). So `w lands` = 0x0 on its own cannot tell "store abandoned" from "observer failed". Use a nonzero baseline such as 0xa5. No `dev_lca.c` mutant can reach the observer, because FLAT never enters `lca_isa`.

**The shipped instrument differs from the measured one.**
- `INSTRUMENT.md5` names `205b0715…`, which is the frozen copy.
- The working-tree probe is `60d4223d…`: a **docstring-only** edit at 19:25:52 (the 8/13 → 9/13 tally correction plus the MEASURED note). The run was at 19:25:36.
- It is behaviourally identical, because the docstring is never printed. But the kill table's base run must use, and hash, the file that ships.

**Hit-case witness, if the round wants HIGH.** It costs three `put d` entries before the arm. A PTE is `PFN << 32 | 1`: `ALPHA_PTE_VALID = 1` and `ALPHA_PTE_TO_PFN = >> 32`.
- Build the chain L1[0] → L2 page, L2[0x3a0] → L3 page, L3[0] → data page.
- Plant a distinctive byte at `data + 0x3fd`.
- Before the fix: a sparse LDBU of 0x3fd returns that byte, and a sparse STB 0x5a to 0x3ff lands at `data + 0x3ff`.
- After the fix: the reads and writes reach LSR and SCR.

It also gives the value channel a positive pre-fix signature, which a false zero cannot provide.

---

## FOUND SOMETHING ELSE

- **E1. The same defect class outside devices: the Alpha PAL treats the PCBB as virtual.**
  - swpctx saves and loads the PCB through `store_64bit_word`/`load_64bit_word` (`cpu_alpha_palcode.c:231-247`, `:275-291`), and wrfen does the same (`:222`).
  - Those helpers call `memory_rw` with `CACHE_DATA` and no PHYSICAL (`core/memory.c:782-783`, `:890-891`).
  - The architectural PCBB is a physical address. The in-tree anchor is `alpha_rpb.h:316`: `pcs_halt_pcbb /* phys addr of halt PCB */`. The Alpha ARM itself is not in the local manual set.
  - As with `lca_isa`, identity hides this at the first swpctx (ptbr == 0, kernel mode). The witness also sidesteps it by passing a K0SEG PCB.
  - At any later swpctx given a physical PCBB:
    - the save walks the outgoing table and is abandoned on a miss;
    - the nine loads return zeros on a miss (#244 zero-fill; `load_64bit_word` ignores the return), so **ptbr silently becomes 0 and identity mode returns**;
    - on a hit, the next context, ptbr included, is read from the outgoing process's memory.
  - Verified by reading; not witnessed. **File it as its own row.** It is not a device and not this round.
- **E2. A residual that depends on the RAM configuration, which the fix introduces. LOW; disclose it in the contract.**
  - With `-M` ≥ 7425, the fixed forward to a device-less port reaches `memory_rw.c:738-750`.
  - That call to `update_translation_table` has **no PHYSICAL guard**, and `cpu_dyntrans.c`'s update installs `vaddr_page` unconditionally. So it maps **user VA page 0x1d0000000 → the host page of PA 0x1d0000000**. That overrides the current process's own mapping until the next swpctx INVALIDATE_ALL or tbi.
  - Before the fix, under paging, this cannot happen: the walk either misses or installs the guest's own mapping.
  - Bare PHYSICAL and `CACHE_NONE|PHYSICAL` share the residual; only `NO_EXCEPTIONS` avoids it, and (c) is otherwise wrong.
  - The same mechanism applies to every non-`NO_EXCEPTIONS` PHYSICAL call that reaches RAM: 16 bare plus 2 `CACHE_NONE|PHYSICAL` in devices. I verified the mechanism by reading, but **not its reachability per device**. File it as a hypothesis.
- **E3. Pre-existing config gap.** On alphabook1, `-M` ≥ 6145 already places RAM under `LCA_IOC_BASE` (0x180000000). Nothing caps `-M` for this machine (`machine_memsize_fix`, `MACHINE_DEFAULT_RAM(alpha)`).
- **E4. A guest-drivable host kill at `memory_alpha.c:75-78`.** It is an `exit(1)` for vaddr `0xfffffffd80000000` in kernel mode at ptbr == 0. It is probably already in the cpusexitsweep census, but the queue files are outside my read scope, so I did not check.
- **E5. A non-architectural decode.** A guest's K0SEG access to `0x1d0000000+port` reaches the ISA devices directly, although on a real LCA that address is sparse-space offset 0x10000000. This is pre-existing, out of scope, and recorded only because it bears on "physical by construction": physical in the emulator's map, meaningless in the hardware's.

---

## CHANGES I'D ASK FOR, in order

1. **Kill-table scorer:** ESCAPED only if exit 0 and `RESULT=13/13`. DEAD or exit 2 on a mutant is KILLED, with the channel named. Or gate on rows 4-7 plus `flat lsr` only.
2. **Add a post-arm 8042 self-test row below 0x200.** It kills (e').
3. **Add a post-arm `ldl`/`stl` pair at 0x3fd and 0x3ff** (the 21066 width), or disclose (f) in the contract.
4. **Contract:** disclose (g) (user mode, unrowed) and E2 (`-M` ≥ 7425), and record (d) as EQUIVALENT with the :758 derivation.
5. **Witness hygiene:** use a nonzero SCR baseline at step D, add `TODO: pte3` to the absence row, and hash the probe that ships.
6. **Severity:** MED as witnessed. The hit-case witness above decides whether HIGH is earned.
7. **File E1** (PAL PCBB as virtual) as a sibling row.
