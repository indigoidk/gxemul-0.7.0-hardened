# PASS 15 -- `m88kexcdeliver` (#502): VERIFY THE ENUMERATION of repair 14 (probe v23), and adjudicate pass 14's findings

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  The other five (Opus, agy,
kimi, deepseek, minimax) are DELIBERATELY NOT FIRED under that roster.  An ordinary regression-detector coverage review.
READ-ONLY: write nothing to any project tree.  The tree under review is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` (HEAD
7b23b785 plus the uncommitted probe v22 + v23 in the working tree); ignore the pristine upstream copy at
`C:/DocumentNoSnc/cc/GXEMUL/src/`.  Everything a packet-fed seat needs is inlined.

**Please do not simply ratify, and do not hunt cells the enumeration already names.**  Passes 13 and 14 each found cells of
one class -- the delay-slot axis -- open, so by the carrier's class-closure rule this repair closes the WHOLE space in one
diff and states which cells it rows and which it deliberately does not.  This pass's job is to VERIFY THAT ENUMERATION:
is it complete, is every cell really reached by the row credited with it, and is every disclosure correctly classified.

**One correction to the naming, before anything else:** HEAD's probe is ALREADY v21 (`m88k_exc_probe.v20.frozen.py` and
`.v21.frozen.py` are earlier records-only revisions).  So the pass-14 packet's "v20" is **v22** (repair 13, the four
`dslot*` rows), and this repair is **v23**.  `repair13_20261016/NAMING.txt` maps every file.

Open with your seat token -- `FABLE_M88KP15_20261016` / `ASTRA_M88KP15_20261016` / `GROK_M88KP15_20261016` /
`GLM_M88KP15_20261016` -- then ONE line: `VERDICT: CLOSE / DO NOT CLOSE (<one line>)`.

## 1. What pass 14 found (all four answers are in `repair13_20261016/pass14/`)

* **Fable 5.1 -- DO NOT CLOSE.** The delivery path TESTS two state values, `PSR & SFRZ` (:811) and `cpu->delay_slot` (:840,
  and :865 whose write `X(br_n)` reads to keep the exception vector over the branch target).  By the carrier's floor bound --
  the guard's dominating predicates (the switch-1 labels) x the state values the repair path tests that are jointly reachable
  -- the floor for this axis is **{7 labels} x {SFRZ} x {delay_slot} = 28 cells**; v22 rowed 19.  It also overturned its own
  pass-13 F2: BOUNDS/ERROR in a slot are FLOOR ("manual silence decides what a row may CLAIM, not whether the cell is owed"),
  and named a geometry trap (below).
* **GPT-6 Astra -- DO NOT CLOSE.** The same BOUNDS/ERROR cells floor; the SFRZ re-route's non-trap and trap sides x {slot}
  floor; the fallback clause (e).  Predicted `if (!is_trap && !cpu->delay_slot)` and `if (!is_trap || cpu->delay_slot)` at
  :816 sweep v22 63/63.
* **Grok 4.7 -- CLOSE.** Fallback and frozen sites clause (e) ("`if (!is_trap && !cpu->delay_slot)` ... is the disclosed
  joint: it adds `delay_slot` to the `is_trap` test"); BOUNDS/ERROR disclosed.  Found `OUTSTANDING_BUGS.md` stale.
* **GLM 5.3 -- CLOSE**, with the frozen-site label "a guess" and the advice to MEASURE it: "Running the already-designed
  `errdslot` is the cheapest way to convert this guess into a warrant."

## 2. What was measured since (logs and PRETABLEs in `regress/artifacts/m88kexcdeliver/repair13_20261016/`)

* **Table 17 (v22):** Astra's two re-route mutants and GLM's fallback mutant each **63/63** -- all three escapes real.
* **Table 18 (a candidate, NOT shipped):** five rows covering ten site cells -- every mutant killed -- but two of its rows used
  `br.n +16` inside the handler at 0x40, whose target 0x50 IS the ERROR entry: a mutant that loses the ERROR delivery would
  land on the row's own breakpoint and read DELIVER.  Fable named the trap; v23 uses `br.n +8` in every handler.
* **Table 19 (v23, the shipped form)** and **table 19b (Fable's two predicted v22 sweeps, measured on v22):** section 4.
* **Gate 11 ran on v22**: PASS, 110 checks (`gate11.out`) -- Fable's pass-14 answer said no gate run existed; it did, in this
  directory.  Gate 11 re-runs on v23 before the commit.

## 3. Settled premises (warrants inline; challenge any of them)

* `m88k_exception()` (section 6, HEAD, untouched) TESTS `vector`, `!implemented` (799), `PSR & SFRZ` (811), `is_trap` (816,
  only inside the SFRZ block), and `cpu->delay_slot` (840 inside `if (update_shadow_regs)`; 865 on every path past the
  fallback).  No other PSR bit is masked or compared.
* `X(br_n)` (`cpu_m88k_instr.c:92-106`): sets `delay_target`, `delay_slot = TO_BE_DELAYED`, runs the slot's handler, then
  `if (!(cpu->delay_slot & EXCEPTION_IN_DELAY_SLOT)) { delay_slot = NOT_DELAYED; pc = delay_target; ... } else delay_slot =
  NOT_DELAYED;` -- so :865's write decides whether a slot fault keeps its vector.
* `X(tb1)` (`:2553-2565`): `SYNCH_PC`; a user-mode trap naming a vector below 128 raises PRIVILEGE with is_trap 0; otherwise
  `m88k_exception(vector, 1)`.  No delay-slot guard.
* The probe plants `br .` (SELF) at every listed vector entry, then a row's handler words at `8*handler_at`, then SELF after
  them -- so `br.n +8` at 0x40 targets the SELF at 0x48 (two-word handler) or, from 0x44, the SELF at 0x4c (three-word).
* The second fault of every two-fault row runs FROZEN (each handler keeps SFRZ set); EPSR keeps the first fault's PSR.
