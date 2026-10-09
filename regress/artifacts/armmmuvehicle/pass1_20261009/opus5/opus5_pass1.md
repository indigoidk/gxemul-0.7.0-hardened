OPUS_SEAT_ALIVE_20261009_MMUV
# CHECKPOINT -- 2026-10-07 11:3x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)

VERDICT: BUILD WITH CHANGES (9) -- the vehicle WORKS on unmodified `-E testarm` (MMU on and stepping in section 0; data and prefetch aborts reach handlers via 0x10/0x0c with LR/SPSR/FSR/FAR exactly as predicted -- all MEASURED), but two premises are wrong (`dump` cannot see the c8 hole; `put h` is exceptions-ENABLED), the L2 table sits INSIDE the L1 table, and the rows as written kill only 1 of 11 one-edit MMU-path mutants under the arming-dump session shape of the template §2.12 names (2 of 11 if the controls run in one debugger interaction) -- MEASURED kill table, section 2; the nine changes proposed there kill the other ten (brief rows + proposed rows: 11 of 11).

Seat: opus5 (Agent tool, claude-opus-5-5), FILE-READING + MEASURING.  No `A` badge (I wrote nothing under review).
MEASURED = run by me on the binary named in section 0.  READ = source reading.  PREDICTED = not run.

## 0. Provenance

* Tree: `GXEMUL-SEC/` WORKING tree (with the uncommitted #562 ARM files), copied by `tar` (src/, configure,
  Makefile.skel, experiments/, doc/) into WSL `/tmp/gxopusmmuv`; `./configure`; `rm src/cpus/*.o`; `make`.
  `cmp`-clean against the working tree for 12 files (cpu_arm.c, cpu_arm_instr.c, cpu_arm_instr_dpi.c, cpu_arm.h,
  memory_arm.c, cpu_arm_coproc.c, cpu_dyntrans.c, debugger.c, debugger_cmds.c, memory.c, memory_rw.c,
  machine_test.c); `gxemul` built 13:43:13, `-nt` every checked source; md5 `3bac199f02fb7b603e5c3e0441f6a5b3`.
  The brief's §4 is VERBATIM `GXEMUL-SEC/src/cpus/memory_arm.c` (working tree), lines 63-277 -- checked.
* Driver: a copy of `arm_msrmode_probe.py`'s `session()` (pty, `-V -A -E testarm -M 64 0x8000:<16 zero bytes>`).
  No project tree was written; no git command was run.  (First build attempt failed: the tar omitted `experiments/`,
  which `make` needs for `make_index.sh`; copied and rebuilt.  The base clone is still `cmp`-clean and `-nt` after the
  table: mutants were built in eleven COPIES, each carrying its own `.MUTANT` sentinel.)
* Artifacts are VOLATILE (session scratchpad + WSL /tmp).  Copy `<scratchpad>/mmuv/opus5_meas/` into
  `regress/artifacts/armmmuvehicle/` BEFORE any record cites a number from it: `meas1_base.out` + `T_base_*.txt`,
  `meas2_base.out` + `T2_*.txt`, `meas3_base.out` + `T3_*.txt`, `kt.run-20261009_141134.py` (the frozen instrument;
  md5 9a33dfc2... = kt.py), `kt_out/KT_*.out` + per-session transcripts, `mutants.py`, `build_mutants.out` (mutant
  md5s), `PREDICTIONS_before_table.txt` (14:01:56, ten minutes before the table started at 14:11:34).

## 0b. The six things I was asked to settle by running -- exact outputs

(a) **MMU on, stepping on in section 0: YES.**  `T_base_ctl.txt`: `[ enabling the MMU ]` after the MCR c1 at 0x8018, then the c8 and 15
    more instructions executed (trace `801c .. 8058`, the `b .`); readbacks MRC c1 = `0x00001137`, MRC c2 = `0x00004000`, remap VA 0x00200000 -> `0x33333333`, page map VA
    0x00400000 -> `0x66666666`, AP=0 load VA 0x00600000 -> `0x66666666`, LIVE after M `0x11111111`, marker `0xc1`;
    zero fault diagnostics.
(b) **Data abort -> handler at 0x10: YES.**  `T_base_dtrans.txt`:
    `{ arm memory fault: vaddr=0x00100000 domain=0 dav=1 ap=0 access=0 user=0 d=0x00000000 d2=0xffffffff pc=0x00008018 }`
    `[ arm_exception(): DATA ABORT, far=0x00100000 fsr=0x05 ]`, `00000010:  ea00213a    b 0x8500`; handler readbacks
    LR_abt `0x00008020`, SPSR_abt `0x000000d3`, CPSR `0x000000d7`, FSR `0x00000005`, FAR `0x00100000`, marker `0xda`.
(c) **Prefetch abort -> handler at 0x0c: YES.**  `T_base_ptrans.txt`: `{ arm memory fault: vaddr=0x00100000 ...
    pc=0x00100000 }`, `[ arm_exception(): PREFETCH ABORT ]`, vector 0x0c -> 0x8400; LR_abt `0x00100004`, SPSR `0xd3`,
    CPSR `0xd7`, FSR `0xa7` (my sentinel 0xA4A5A6A7, cut to 8 bits by the c5 WRITE, untouched by the abort), FAR
    `0xfa4f0f00` (sentinel, untouched), marker `0xbf`.
(d) **`dump` of an unmapped VA after M:** `0x00100000  (memory access failed)` -- likewise 0x00123450, 0x00401000,
    0x00500000 and the halt stub 0x03fff020; mapped VAs print the TRANSLATED word (`0x00200000  33333333 ...`).
(e) **put-w warm translation: YES without c8, NO with c8 -- but only inside ONE debugger interaction.**  `e_noflush`:
    the guest load of the unmapped VA returned `0xcafef00d` with no fault; `e_flush`: abort, FSR 0x05, FAR 0x00100000;
    `e_noflush_reentry`: an extra `step 1` interaction alone makes it abort (details 1b).
(f) **Implicit touches:** none in the vehicle's flow; three exceptions-ENABLED debugger paths exist (the per-step
    disassembly fetch; `put h`/`put w` after M, which inject a guest abort) -- 1c, 1-extra.

## 1. Premise audit

1a | **MEASURED: the handler is reached THROUGH THE TABLE; the generic `could not find physical address of the
exception handler` exit is NOT reachable on this path -- an unmapped vector page instead recurses until SIGSEGV.**
  * Normal case (`T_base_dtrans.txt`): trace `8000 8004 8008 800c 8010 8014 8018 10 8500 ... 8528 852c`.  READ path:
    `arm_exception()` ends `quick_pc_to_pointers(cpu)` -> `phys_page[0]` (cleared by the c8) -> `arm_pc_to_pointers` ->
    generic -> `host_load[0]` (cleared) -> `translate_v2p(0x10, FLAG_INSTR)` = `arm_translate_v2p_mmu`, section 0.
    There is no physical fetch path; the only "other way" is a cached `phys_page[0]`/`host_load[0]`, which c8 clears.
  * **Without the c8 a stale translation DOES serve the vector fetch** -- proved by my own setup error
    (`T_base_thumb_dabt.txt`: a stimulus preset `r1=0x100000` overwrote the TTB operand, so the table denied
    section 0): the vector at 0x0c was still fetched and executed (branch to 0x8400) from the page-0 translation the
    `put w` of the vector words had warmed in the same interaction.
  * **Vector page genuinely unmapped** (`T3_vec_unmapped.txt`; section 0 through a coarse table at 0x3000, page 0
    unmapped, pages 8/9 identity; one data abort; pty drained to EOF): **47,591 nested `{ arm memory fault ...}` in
    10.6 s, 10,473,809 bytes, process ended by signal(11)**; "could not find physical" occurs ZERO times.  READ
    mechanism: `arm_exception` -> `quick_pc_to_pointers` -> generic -> `translate_v2p` fails -> `arm_exception(PREF_ABT)`
    -> `quick_pc_to_pointers` -> ..., before control ever returns to the generic function's second-chance lookup.
    A guest that unmaps its own vectors and takes any abort kills the host: OUT OF SCOPE, but FILE it
    (proposed id `armvecrecurse`).
  * Probe consequence: a driver that stops reading the pty scores that storm as ALIVE (the child blocks on a full pty
    and is SIGKILLed by the driver: meas1 printed `alive (SIGKILLed by driver)` over 40,402 faults).  Classify by the
    marker/DEST, never by liveness alone, or drain to EOF.

1b | **MEASURED: c8 INVALIDATE_ALL drops every DATA and VECTOR translation that could be stale -- and the c8 matters
ONLY for translations made inside the same `step` interaction.**
  * `e_noflush` (no c8; `put w 0x00100000,0xCAFEF00D` in the SAME interaction as the `step`): the guest
    `ldr r3,[r5]` of the UNMAPPED VA returned **0xcafef00d**, no fault; the brief's `remap`/`page map` loads returned
    the IDENTITY words **0x22222222 / 0x44444444** instead of 0x33333333 / 0x66666666.  In the same transcript the
    disassembler printed `ldr r3,[r8] <0x00200000: 0x33333333>` (its NO_EXCEPTIONS peek walks the table) one line
    before the guest stored 0x22222222.
  * `e_flush` (same, with c8): abort, FAR 0x00100000, FSR 0x05, handler ran.
  * `e_noflush_reentry` (no c8, plants separated from the stimulus by `step 1` + a dump): **abort** -- the debugger's
    re-entry ("Clear all dyntrans translations", `debugger.c`) had already dropped the put-w translation.
  * `e_guestwarm_noflush` / `_flush` (the GUEST loads 0x00100000 with the MMU off, then M, then loads again, in ONE
    `step`): no c8 -> **0xcafef00d** stale; c8 -> abort.  The only c8 witness that survives a debugger re-entry.
  * The VECTOR page, as a measured pair: in meas1's `vec_unmapped` the vector words were `put w` in the same
    interaction (page 0 warm), the c8 executed after M, and the vector fetch then WALKED and faulted at 0x10 (first
    faults: 0x00100000, then 0x00000010, then 0x0000000c ...); in the accidental run above, where the c8 never
    executed, the same warm page-0 entry SERVED the vector fetch.  So c8 is what makes the vector fetch use the table.
  * READ: INVALIDATE_ALL walks `vph_tlb_entry[]` and clears host_load, host_store, phys_addr, phys_page, the
    is_userpage bit and vaddr_to_tlbindex of every valid entry; `update_translation_table` creates each host_load entry
    together with a vph entry (evicting with invalidation when full), so no orphan survives.  NOT dropped, and not
    needed by the vehicle: `cur_ic_page`/`next_ic` of the page executing the MCR (straight-line code after it runs from
    the physical page resolved before it), the per-PHYSICAL-page ic arrays, `translation_table` (re-keyed on ttb),
    same-page PC-relative literal folds.  Decoding: only opcode2 is tested -- CRm is ignored (`c8,c5,0`, `c8,c6,0` also
    flush ALL).

1c | **MEASURED: nothing implicit touches an unmapped address in the vehicle's flow -- but three debugger paths are
exceptions-ENABLED MMU accesses, and one of them runs on every step.**
  * Halt stub 0x03fff020 and prom emulation's OpenFirmware hook word `0xef8c64be` at 0x03fffff8 (same last MB): never
    touched; after M, `dump 0x03fff020` -> `(memory access failed)` (`T_base_ctl.txt`).  LR_svc still holds
    0x03fff020, so an accidental `mov pc,lr` would prefetch-abort with LR_abt 0x03fff024 (PREDICTED) -- distinguishable
    from the pref row's 0x00100004.  Console 0x10000000: never touched.  `print pc/cpsr/lr/sp`: registers only.
  * **The single-step disassembly fetch** (`cpu_dyntrans.c`, single-step block: `memory_rw(..., cached_pc, ...,
    CACHE_INSTRUCTION)`, no `NO_EXCEPTIONS`) walks the table for the NEXT instruction before it executes.  Benign on
    identity section 0; but when dyntrans holds a cached code page the table now denies, THIS read raises the prefetch
    abort, prints `XXX_run_instr(): could not read the instruction`, and `I;` then executes the VECTOR instead
    (`T_base_thumb_dabt.txt`, at 0x8014 -- the c8 right after the M write never executed).  Single-step and free-run
    differ exactly on stale code pages.
  * The disassembler's LDR/STR operand peek is NO_EXCEPTIONS (`ldr r3,[r5] <0x00100000>`: no value, no fault).
  * **Debugger `put h`/`put w` after the M bit inject a GUEST data abort** (MEASURED; `put d` too by reading --
    `store_64bit_word`, `CACHE_DATA`) -- see 1-extra.

1d | **MEASURED: right, with two consequences the brief does not draw.**  Reset control = **0x1136** (ICACHE|S|DATA32|
PROG32|CACHE|ALIGN): `prom_emulation` defaults to 1 (`machines/machine.c` `m->prom_emulation = 1;`, cleared only by
`-Q`); with `-Q` it is **0x1236** (R).  Privileged AP=0: load OK (0x66666666), store FSR 0x0d (`T_base_perm.txt`).
**Consequences:** (i) USER-permission accesses differ -- S: user has no access (MEASURED: `ldrt` from the AP=0 section ->
FSR 0x0d, diag `user=1`); R: user read-only.  (ii) `arm_check_access`'s `case 2: return 1;` (the R arm) is UNREACHABLE
on default testarm, so a mutant there escapes every privileged row (M_ckR, section 2) -- unless the guest writes c1
with S=0,R=1 itself (MRC / BIC #0x100 / ORR #0x200 / ORR #1 / MCR: MEASURED working, row X.sr).

1e | **MEASURED, all four:** `data trans` 0x05 (diag `domain=0 dav=1 d=0x00000000`); `page trans` 0x07 (diag
`d=0x00005001 d2=0x00000000`); `domain` 0x19; `perm` 0x0d (diag `access=1`).  **Coarse descriptor in domain 3:**
**0x37** with domain 3 a client (DACR 0x00000041; `T_base_pgtrans_dom3.txt`) and **0x3b** -- a DOMAIN fault, checked
before the L2 read -- with the brief's DACR 0x00000001 (`T_base_pgdomain_dom3.txt`).  Architecture (READ,
`_scratchpad/ddi0100i.txt:29076-29084`, Table B4-1): Translation/Section domain **Invalid**, Translation/Page domain
**Valid**.  So the coarse path's un-zeroed domain is REQUIRED, while `case 0: domain = 0;` is an emulator CHOICE for an
invalid field -- and with the coarse table in domain 0 and every L1 fault word all-zero, the brief's rows can observe
NEITHER.

1f | **MEASURED: none of the handler's own instructions can fault; the STACK is the trap.**  SP_abt is never loaded:
`print sp` = **0x0** in ABT mode.  A handler opening `str r3,[sp,#-4]!` (`T_base_nested.txt`) nests a data abort at FAR
**0xfffffffc**, overwrites LR_abt (**0x8508**) and SPSR_abt (**0xd7**), and livelocks (trace `10 8500 10 8500 ...`, DEST
never written, one unlatched `[ WARNING! Exception caused no mode change? mode 0x17 ]` per nest).  Also lethal (READ):
dereferencing FAR; `MRC/MCR p15` with Rd = PC (`exit(1)`, `cpu_arm_coproc.c` `if (rd == ARM_PC)`); c13 PID != 0
(`exit(1)`); a c1 write that flips bit 7 (BIG, `exit(1)`) -- the brief's MRC/ORR/MCR preserves bit 7 (MEASURED 0x1137).

1-extra | **Two premises are WRONG (MEASURED):**
  * §1.6 "the byte/halfword `put` paths ... use CACHE_NONE | NO_EXCEPTIONS" is true for `put b` and FALSE for `put h`
    (`debugger_cmds.c` `res = store_16bit_word(...)` -> `core/memory.c` `store_16bit_word` -> `CACHE_DATA`).
    `T2_put_after_m2.txt`: after M, `put h 0x00100008,0x6666` printed the fault diag and `[ arm_exception(): DATA
    ABORT, far=0x00100008 fsr=0x05 ]`, then `pc=0x10 cpsr=0xd7 lr=0x8028`; `put b` printed `FAILED!` and changed
    nothing; a following `put w` from ABT nested (LR 0x18, `T_base_put_after_m.txt`).  Any post-M re-plant to an
    unmapped VA silently drives the guest into its abort handler.
  * §2.2 "Prove the hole with debugger `dump UNMAP`": `dump` CANNOT observe the hole.  memory_rw never consults
    host_load (it always walks), and every interaction has already cleared all translations.  In `e_noflush` the guest
    read 0xcafef00d at the unmapped VA inside the step, and the very next `dump 0x00100000` printed
    `0x00100000  (memory access failed)`.  `hole dump` pins only the walk's NO_EXCEPTIONS path.

## 2. The smallest edit that breaks the MMU fault path and keeps the proposed rows green

**MEASURED kill table.**  (B rows pin exactly the observables §3 names for each row, plus the handler marker.)  Eleven single-edit mutants of the MMU fault path, each built in its own copy of the
scratch clone (`rm src/cpus/*.o`; distinct md5s in `build_mutants.out`), scored by a FROZEN prototype of the vehicle
(`kt.run-20261009_141134.py`) carrying the brief's rows as written -- **B**, 24 rows: the controls run in shape A (plants
and `step` in ONE interaction) and shape B (the msrmode arming `step` + dump re-entry first), each abort row its own
process in shape B -- and the rows I propose -- **X**, 17 rows.  Predictions written 14:01:56, table started 14:11:34.

| mutant (one edit) | B (brief) | X | killed by |
|---|---|---|---|
| BASE | 24/24 | 17/17 | -- (control: no false red, 12 instruments concurrent) |
| M_dabtret: `retaddr += 4;` deleted (DATA_ABT) | **23/24** | 17/17 | B.dtrans lr = 0x801c |
| M_c8nop: c8's `INVALIDATE_ALL` call deleted | **22/24, shape A only** -- shape B and every abort row green | 15/17 | B.remapA 0x22222222, B.pagemapA 0x44444444; X.guestwarm post 0x22222222, X.ttbswitch 0x22222222 |
| M_farpage: `far = vaddr` -> `vaddr & ~0xfffU` | 24/24 ESCAPE | 16/17 | X.dtrans_odd far = 0x123000 |
| M_dom0: `case 0: domain = 0;` deleted | 24/24 ESCAPE | 16/17 | X.faultdesc fsr = 0xf5 |
| M_pgdom0: coarse `case 0:` gains `domain = 0;` | 24/24 ESCAPE | 16/17 | X.pgtrans_d3 fsr = 0x07 |
| M_domPS: coarse `FAULT_DOMAIN_P` -> `_S` | 24/24 ESCAPE | 16/17 | X.pgdom_d3 fsr = 0x39 |
| M_permPS: `FAULT_PERM_P` -> `_S` | 24/24 ESCAPE | 16/17 | X.pageperm fsr = 0x0d |
| M_l2idx11: coarse index `>> 10` -> `>> 11` | 24/24 ESCAPE | 11/17 | X.pageperm (0x07), X.ctl2 x4 (aborts, no marker) |
| M_ckR: `case 2: return 1;` -> `return 2;` (R arm) | 24/24 ESCAPE | 16/17 | X.sr (store accepted, no handler) |
| M_ttbstale: `\|\| ttb != last_ttb` dropped | 24/24 ESCAPE | 16/17 | X.ttbswitch = 0x33333333 |
| M_c2mask: `ttb &= 0xffffc000;` deleted | 24/24 ESCAPE | 16/17 | X.c2low (prefetch storm, 32,417 faults -> unarmed) |

**So the brief's rows kill 1 of 11 under the session shape §2.12 prescribes and 2 of 11 if the controls share one
interaction; nine one-edit mutants are TOTAL escapes, and the c8 no-op escapes under the prescribed shape.**  Every B
escape was predicted before the table ran.  One predicted VALUE was wrong and is recorded as such: M_c8nop's
X.ttbswitch read 0x22222222, not my 0x33333333 -- the pre-M guest entry for page 0x200 was never replaced, so every
later load of that page, across the TTB switch, read the identity word; the RED verdict was right.

**The smallest edit, as asked:** three ONE-CHARACTER total escapes -- `FAULT_PERM_P`->`FAULT_PERM_S`,
`FAULT_DOMAIN_P`->`FAULT_DOMAIN_S`, `>> 10`->`>> 11` -- keep all 24 proposed rows green (MEASURED); the most
consequential is the c8 no-op, the vehicle's own arming step, invisible to every proposed row in the prescribed shape.
`page trans` is the instructive green: under `>> 11` the shifted index reads garbage that is ALSO type 0, so "fault,
FSR 0x07" is the answer for ANY index error landing on zeros.  **A translation-fault row cannot pin an index; only a
MAPPED entry at a NONZERO index can** -- clause (f)'s anchor rule at L2.

**The brief's other candidates, not built (PREDICTED):** FAR assignment dropped -> killed (B.dtrans far reads the reset
0); `domain << 4` dropped -> killed (B.domain 0x09); TRANS_S/TRANS_P swapped -> killed; PREF/DATA swapped -> killed
(LR 0x801c, wrong marker); section base mask narrowed -> killed only for bits 20-22 (remap base 0x003, AP=0 base
0x006); dropping any of bits 23-31 escapes everything, since no planted base sets them -- a remap target like PA
0x03D00000 (inside 64 MB) covers bits 20 and 22-25.

**Two escapes pin emulator CHOICES, not architecture -- label them so if adopted:** M_dom0 (section-translation domain
is Invalid, Table B4-1) and M_c2mask (TTB bits 13:0 are should-be-zero on ARMv4/v5).  The rest are architecture.

**THE CHANGES (9), each MEASURED green on BASE and each killing at least one escape above:**
1. **c8 witness = the guest-warm row** (`nop` / guest `ldr` of the remap VA with the MMU off / arm / `ldr` again, all in
   ONE `step`): must read the REMAPPED word.  Delete "prove the hole with `dump`" (1-extra).
2. **Non-aligned stimulus VAs** for every data-abort row (0x00123458: FAR read back whole).
3. **Coarse table in a nonzero domain**: page-trans FSR 0x37 with DACR client, and a coarse DOMAIN-fault row, 0x3b.
4. **A MAPPED L2 entry at a NONZERO index** (entry 2: VA 0x00402000 -> PA 0x00702000).
5. **A page-permission row** (small page AP=0: load accepted, store FSR 0x0f).
6. **A TTB-switch row** (second table at 0xC000 that also maps section 0; `mcr c2` + c8; the remap VA reads the new
   target).
7. **A guest-written S=0,R=1 row** (AP=0: load accepted, store 0x0d) -- the only way to reach the R arm on testarm.
8. **Move the L2 table out of 0x4000-0x7FFF** (e.g. 0x3000) and keep section 0 mapped in every table (3(iii), 1a).
9. **Session hygiene:** an 8-bit FSR sentinel (low nibble even); per-process `MRC c2`/`c3` readbacks as CONTROLS; no
   `put h/w/d` after the M bit; classify storms by marker, never liveness; the `-V` trace as the step-count proof
   (section 4); and a prompt-detecting session (3(i)).
Optional, as disclosed POLICY pins: the type-0 L1 word with domain bits (kills M_dom0) and the TTB-low-bits row (kills
M_c2mask).

## 3. Option-set completeness

3(i) PACKAGING | **One importable gated detector (the `sh4_pcic_probe.py` shape), plus a frozen-copy rule for
consumers.**  READ: `arm_msrmode_probe.py` is NOT importable -- no `main()`/`__main__` guard, its 47 rows run at module
level and `BIN = sys.argv[1]` is read at import -- so "build from its machinery" means COPY its `session()`, which is
what I did.  `sh4_pcic_probe.py` (`def main()` + `if __name__ == "__main__"`) is imported by 10 regress files
(`import sh4_pcic_probe as P`) and is `CLASS_DETECTOR` in `check_probe_wiring.py`'s MANIFEST; a pure library would be
`CLASS_TOOL` (precedent `drive_guest.py`, "the pty driver library every rig probe imports") and owes no gate.  Either
of the first two options works; reject the self-contained copy (three consumers would re-learn the c8 / L2-overlap /
FSR-mask lessons in three divergent vehicles).  **The member nobody named: an importing consumer's kill table freezes
ITS probe but imports the LIVE vehicle** -- the frozen-copy rule then does not hold for the half of the instrument that
plants, arms and parses.  Freeze the vehicle beside the consumer (`cp`), or have the vehicle print a content hash the
consumer's log records.
**And a harness cost the brief does not name (READ, `regress/gate_hygiene.sh`):** a NEW pty probe that copies
`arm_msrmode_probe.py`'s fixed-delay `session()` is a "NEW PROMPTLESS PTY PROBE" and reds gate 6 until it is either
grandfathered (`tools/derive_hygiene_pins.sh --grandfather`; the list itself records that arm_msrmode_probe.py got in
by a 2026-09-23 OWNER RULING) or given prompt detection.  `arm_bdt_probe.py` (#524) already carries the #392 shape --
`wait_prompt()` / `send()` keyed on `"GXemul>"` after a fresh `mark` -- and counts toward `EXPECT_CONVERTED`.  **Build
the vehicle's TRANSPORT on arm_bdt's `send()` and keep msrmode's ROW machinery (MARK split, `dumped()`, plant
checks).**  It is also faster -- my fixed-delay sessions cost ~17-30 s per process -- and it cannot truncate under load
or stop reading during a storm, which is what made meas1 score a dying recursion as "alive".  Move the hygiene pins
deliberately in the same commit (`derive_hygiene_pins.sh`, never by hand).

3(ii) ROW SET vs the three consumers |
  * **armthumbabortkill.**  Needs a Thumb entry helper (MEASURED: `bx r5` to 0x8101 -> cpsr 0xf3, the Thumb `ldr` ran
    and aborted: `[ arm_exception(): DATA ABORT, far=0x00100000 fsr=0x05 ]`, then `could not load with immediate
    offset`, `emul: All machines stopped.`, pc 0x10, cpsr 0xd7, **LR_abt 0x8107** -- the defect, reproduced on this
    vehicle).  Two of the five sites are not reachable the obvious way: (1) the PC-relative literal load uses
    `CACHE_INSTRUCTION` (READ, Thumb pc-relative `case 2/3`), so it raises a PREFETCH abort (vector 0x0c, no FAR/FSR)
    for a data read, and its literal must sit in unmapped memory within +1 KB of a mapped instruction -- put the Thumb
    code at the END of section 0 (e.g. `ldr r0,[pc,#4]` at 0x000FFFF8 -> literal 0x00100000, unmapped section 1;
    PREDICTED from the source, not run); the brief's map allows it.
    (2) The instruction-fetch site (`could not read the instruction`) is unreachable by a BX (MEASURED: the generic
    pc_to_pointers prefetch-aborts first, LR 0x00100003, handler in ARM state); by READING it needs a STALE code
    translation (the ARM-state analog is MEASURED in 1c) --
    so the vehicle must offer **arming WITHOUT the c8** as an explicit, labelled option (the `e_guestwarm` shape), with
    a control row proving the staleness is the cause.  The SP-relative sites need `sp=` an unmapped VA in SVC.
  * **armdesc3kill.**  Needs a free L1 index for a type-3 word (e.g. VA 0x009 -> TTB+0x24) -- available -- and must stay
    OUT of L1 indices 0x400-0x4FF while the L2 table sits at 0x5000 (3(iii)).
  * **armdacr2kill.**  Needs a 0b10 DACR field on the domain of a mapped SECTION, or of a coarse table whose L2 entry is
    VALID (READ: a type-0 L2 entry takes the translation fault before `arm_check_access` is called).  The `r2` preset
    supports it.
  * High vectors (c1.V): no consumer needs them -- NOT CLAIMED.  USR: `ldrt`/`strt` give user-permission accesses from
    SVC with no mode switch (MEASURED: `ldrt` LIVE -> 0x11111111; `ldrt` AP=0 -> FSR 0x0d `user=1`); needed only if
    the vehicle claims `arm_check_access`'s user axis (AP=1/AP=2 rows).  Re-planting after an abort in one process:
    don't -- post-M `put h/w` injects aborts (1-extra); one process per abort row.

3(iii) ACCIDENTAL REACH |
  * **The brief's L2 table at 0x5000 is INSIDE the L1 table's 16 KB (0x4000-0x7FFF), so every L2 word is ALSO an L1
    descriptor for VA 0x400xxxxx-0x4FFxxxxx.**  MEASURED (`T2_l2inl1_mgr.txt`): with DACR 0xC0000001 a guest `ldr` of
    VA 0x40000000 returned **0x66666666** -- PA 0x00600000, through the L2 word 0x00600FF2 read as an L1 SECTION in
    domain 15 -- and `dump 0x40000000` showed it; with DACR 0x00000001 it took a domain fault, FSR **0xf9**
    (`T2_l2inl1_dacr1`).  Any L2 tiny-page entry (low bits 11) a consumer plants there is simultaneously an L1 type-3
    descriptor, i.e. the `armdesc3kill` `exit(1)` on any walk of those VAs; and a consumer mapping VA 0x400xxxxx
    overwrites the L2.  Nothing in the vehicle walks those VAs today -- move the L2 table out anyway (e.g. 0x3000).
  * `armdacr2kill`: unreachable -- DACR 0x1 (and my 0x41, 0xC0000001) carry no 0b10 field.
  * Vector-fetch exit: unreachable (1a); the real hazard is the SIGSEGV recursion if a table unmaps page 0.
  * **A clobbered arming operand turns a row into a storm.**  The arming reads TTB/DACR from debugger presets r1/r2; a
    consumer presetting r1 for its own stimulus silently re-points the TTB (MEASURED, my own error: r1 = 0x00100000 made
    the data word 0x11100111 a coarse descriptor in domain 8 -> 17,400+ nested prefetch aborts).  Read TTB/DACR back
    with MRC into DEST as CONTROLS in every process (the brief's `ttb rd` only in the control process), or load the
    arming operands PC-relative from a literal pool in the code page.

3(iv) MEMBERS NOT NAMED | arming WITHOUT c8 as a supported variant; a guest-warm c8 row; an L2 anchor at a NONZERO index;
a TTB-switch row; an 8-bit FSR sentinel; per-process TTB/DACR readbacks; the `-V` trace and the fault diag as oracle
channels (section 4); drain-to-EOF (or marker-only classification) for storms; the L2 move; the type-0 L1 descriptor
with nonzero domain bits as an explicit POLICY pin (disclose it as such -- the architecture says Invalid).

## 4. Session plan

**Shape: one non-aborting control process, then ONE PROCESS PER ABORT ROW** (the brief's call, and MEASURED
correct: an abort is one-way and a post-M `put` cannot repair state).  Sharing aborts via handler return
(`subs pc,lr,#4`) would drag #562's DPI S-to-PC restore into the vehicle -- don't.  Cost MEASURED: ~30 s per
process at 0.25 s/command (~85 `put w`; meas1, 20 processes in ~10 min), ~17 s at 0.1 s per put (kt.py; BASE 24/24 + 17/17 with 12 instruments running
concurrently).

**Exact step counts, MEASURED from the `-V` trace (each line is one executed instruction):**

| row | sequence | steps |
|---|---|---|
| data abort (dtrans/pgtrans/domain) | 6 arming + faulting LDR + vector `B` + 11 handler instrs through the marker STR | **19** (`8000..8018 10 8500..8528`) |
| perm (accept LDR, STR, MOV, faulting STR) | 6 + 4 + vector + 11 | **22** (`..8024 10 8500..8528`) |
| prefetch via `B` (2 sentinel MCRs first) | 2 + 6 + `B` + vector + 11 | **21** (`..8020 c 8400..8428`) |
| prefetch via `BX` (ARM or Thumb target) | 6 + `BX` + vector + 11 | **19** -- the aborted fetch costs ZERO steps |

The abort costs exactly the faulting instruction's own step; the vector `B` is the next step.  For a Thumb-target `BX`
the abort is raised at the top of the NEXT `run_instr` and the vector executes in that same step (trace `8018 c 8400`).

**Is the last-store marker enough?  No -- necessary, not sufficient.**  It proves the handler's last store ran; it does
not prove WHICH instruction aborted or that the expected vector was taken (a data abort from the wrong instruction, or
an overrun into the LR stub with a shared marker, also writes it).  Use, in addition: distinct markers per handler
(0xda/0xbf, MEASURED); the `-V` TRACE -- assert the exact address subsequence [stimulus pc, 0x10|0x0c, handler..marker
STR], parsed only AFTER the first `step` echo because `unassemble` prints the same format; the fault diag's `pc=` field
and the `[ arm_exception(): DATA ABORT, far=..., fsr=... ]` line; and LR itself.  Overrun is harmless (handlers end in
`b .`; the trace shows the repeats); underrun reds the marker.

## 5. Something else

* **The Thumb LR claim is TRUE, and the prefetch half is wrong too (MEASURED).**  Data abort from a Thumb `ldr` at
  0x8100: LR_abt **0x8107**; DDI 0100I Table A6-1 (`_scratchpad/ddi0100i.txt:20352`) gives the instruction + 8 =
  0x8108 (and its note at :20368-20369 says the skip-return for a Thumb data abort is `SUBS PC,R14,#6`, confirming +8).
  Prefetch abort via `bx` to 0x00100001: LR_abt **0x00100003** (`T_base_thumb_pabt.txt`); Table A6-1 gives the aborted
  fetch + 4 = 0x00100004.  Cause (READ): `cpu->pc` carries the Thumb bit in Thumb state (`arm_cpu_interpret_thumb_SLOW`
  insists on `pc & 1`), so `retaddr = (addr|1) + 4 + 2` = addr + 7 and `(addr|1) + 2` = addr + 3 -- both ODD and one
  short.  "pc + 6" in the brief is right in cpu->pc terms.  ARM-state controls are correct (0x8020 for 0x8018;
  0x00100004 for `bx` to 0x00100000).  Owned by `armthumbabortkill`.
* **`armvecrecurse`** (1a): guest-reachable host SIGSEGV via unbounded exception recursion when the active table unmaps
  the vector page.  File it; it is the more severe sibling of the vector-fetch exit the brief names.
* **FSR is 8 bits on WRITE, so a sentinel must be <= 0xff.**  MEASURED: `mcr c5` of 0xA4A5A6A7 reads back **0xa7**
  (`cpu_arm_coproc.c` `cpu->cd.arm.fsr = cpu->cd.arm.r[rd] & 0xff;`); a 32-bit compare reds a correct build.  FAR keeps
  all 32 bits (0xFA4F0F00 survived the prefetch abort).  Choose an FSR sentinel no data abort can write: low nibble
  even (data-abort FS values are 5/7/9/b/d/f), e.g. 0xA4.  Also (READ, `ddi0100i.txt:29046-29047`): whether a
  prefetch abort updates FSR/FAR is IMPLEMENTATION DEFINED, so the sentinel rows pin an emulator choice -- fine for a
  detector, but say so.
* **The default CPU's own ID register says it has no Thumb, yet the model executes BX and Thumb** (MEASURED above).
  READ: `src/include/thirdparty/arm_cputypes.h` `CPU_ID_SA1110 0x6901b110` -- architecture field (bits 19:16) 0x1 =
  `CPU_ID_ARCH_V4`, where `CPU_ID_ARCH_V4T` is 0x2.  A guest reading MRC c0 is told ARMv4.  Not a defect for this
  round; one line in `armthumbabortkill`'s record (its witness runs Thumb on a model whose ID says it cannot).
* Floods (READ + MEASURED): the `{ arm memory fault ...}` diag and `[ WARNING! Exception caused no mode change? ...]`
  are unlatched; a guest can print them without bound (47,591 in 10 s).  The `floodclass` family; out of scope.
