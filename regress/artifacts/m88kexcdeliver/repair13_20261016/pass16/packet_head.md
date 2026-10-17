# PASS 16 -- `m88kexcdeliver` (#502): VERIFY THE ENUMERATION of repair 15 (probe v24), and adjudicate pass 15's findings

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  Opus, agy, kimi, deepseek and
minimax are DELIBERATELY NOT FIRED under that roster.  An ordinary regression-detector coverage review.  READ-ONLY: write
nothing to any project tree.  The tree under review is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` -- HEAD c64445fa (v23 is
committed: 16512e9c) plus the uncommitted probe v24 in the working tree; ignore the pristine upstream copy at
`C:/DocumentNoSnc/cc/GXEMUL/src/`.  Everything a packet-fed seat needs is inlined.

**Please do not simply ratify, and do not hunt cells the enumeration already names.**  This repair claims to complete the
class: `m88k_exception()` TESTS exactly four inputs (section 3), the floor is their product over the seven labels, and every
reachable cell is now rowed.  Your job is to check that claim -- the input set, the reachability rule, each row's credit, and
each disclosure -- not to re-open settled cells.

Open with your seat token -- `FABLE_M88KP16_20261016` / `ASTRA_M88KP16_20261016` / `GROK_M88KP16_20261016` /
`GLM_M88KP16_20261016` -- then ONE line: `VERDICT: CLOSE / DO NOT CLOSE (<one line>)`.

## 1. What pass 15 found, and how it was ruled (answers in `repair13_20261016/pass15/`)

* **GPT-6 Astra -- CLOSE**: all 28 state cells verified against the row definitions; no vacuous row; 78/78.
* **Grok 4.7 -- CLOSE**: 28/28 verified; withdrew its pass-14 positions D3 and D4; held `is_trap` a per-raise PARAMETER
  outside the floor's device-state axes, so the five frozen trap-in-slot cells clause (e).  Corrected the contract's
  vectors-0..3 pointer (`m88kexcdebt`, not `m88kexchwtraps`) -- applied in 16512e9c.
* **Fable 5.1 -- DO NOT CLOSE**: the enumeration omits `is_trap` (:816), the fourth input the delivery path tests.  By the
  carrier's generating-set clause and this chain's own `*tb` / `trapfrozen<L>` rows, a TRAP in a slot at the five instruction
  labels is floor; the five `!is_trap || (vector == L && cpu->delay_slot)` 73/73 escapes of table 19 were measured floor
  breaches.  Ten rows close it, "after which m88k_exception() has no untested input left".
* **GLM 5.3 -- DO NOT CLOSE**: the user-trap labels (0x80, 0x1c2, MVMEPROM_VECTOR, the default) reach the same delay-slot code
  and were neither rowed nor disclosed.
* **RULED (the argument, not the 2-2 count):** Fable's -- the carrier added the generating-set clause precisely because a bare
  state floor graded an input-bit escape as debt, and this chain repaired the identical shape in-round on passes 5 and 7.
  GLM's user-trap labels: DISCLOSED (Fable: outside the fix's seven labels; their delivery predates #502), with their escapes
  now MEASURED (table 20).  v23 was committed as 16512e9c with the chain recorded OPEN; repair 15 is this diff.

## 2. Settled premises (warrants inline; challenge any of them)

* The function TESTS exactly four inputs: `vector` (switch 1, :799, the shadow branch's DATA/INSTRUCTION_ACCESS tests,
  switch 2), `PSR & SFRZ` (:811, the only PSR bit masked or compared), `cpu->delay_slot` (:840 inside `if
  (update_shadow_regs)`, :865 on every path past the fallback -- and `X(br_n)` reads :865's write to keep the vector over the
  branch target), and `is_trap` (:816, inside the SFRZ block).  Everything else is copied, ORed or written.
* `is_trap = 1` comes only from `tcnd` / `tb0` / `tb1` (`cpu_m88k_instr.c:2529/:2551/:2564`); a user-mode trap naming a vector
  below 128 raises PRIVILEGE with is_trap 0; no instruction raises 7 or 10 any other way (there is no `tbnd`).  So the 8
  cells (BOUNDS or ERROR) x (any SFRZ, any slot) x (is_trap 0) are UNREACHABLE, and the grid has 48 reachable cells.
* Frozen rows put their slot fault in the div0 handler at 0x40 behind `br.n +8`, whose target is the SELF word planted after
  the handler -- never the row's own breakpoint (the `br.n +16` -> 0x50 trap of pass 14).  **One exception, found by table
  20 itself:** `trapfrozen9dslot` traps to OVERFLOW, whose entry IS 0x48 = the +8 target, so under the `:865` mutant it read
  DELIVER (73/84 against a predicted 72/84).  It now uses `br.n +16` (target 0x50; its breakpoint is 0x48); table 20b
  re-measured every mutant that touches it.  Every other frozen row's target differs from its breakpoint (checked).  `trapfrozen8dslot` follows
  `trapfrozen8`'s shape (first fault OVERFLOW, handler at 0x48, breakpoint 0x40), so its +8 target is 0x50's SELF, which is
  safe because its breakpoint is 0x40.
* The probe's code is the frozen instrument table 20 scored (AST-identical; the committed v24 differs only in the docstring).
