# qhslowifetch pass 6 -- codex GPT-6 Astra's breaches B1, B2, B3 (p6_20261105/codex_codex_qhs_p6.txt), MEASURED 2026-11-05 before their repair

`b123_table.run.sh` (frozen copy of `b123_table.sh`) -> `b123_table/` (log: `b123_table_run.log`).  Scratch clone /tmp/gxqhs12 (`cp -a`
of build/) under a clone-local .MUTANT sentinel; the clone's `cpu_ppc_instr.c` and `cpu_ppc.h` cmp'd equal to GXEMUL-SEC's before the
first edit; the fix rebuilt fresh in the clone first (the freshness proof); restored, cmp-clean against GXEMUL-SEC, rebuilt fresh,
sentinel cleared.  Every build `fresh` (`cpu_ppc.o` newer than the source, `gxemul` newer than `cpu_ppc.o`).  Variants:
`b123_variant.py`, one exact edit each against the fix.

THE SPACE.  Arm (a)'s guard and its exit read `translation_readahead`, and the variants condition them on `cpu->pc` against `addr`
(pc's low two bits, which the prologue keeps while it aligns `addr`) and on MSR[ME].  So the read-ahead route at cpc700_pci's last
word -- the probe's `T ra` session: SRR0 sentinel, pc set, `continue`, `-T`, no breakpoint, so read-ahead runs -- is crossed over
pc's low two bits {00, 01, 10, 11} x MSR[ME] {clear, set}: 8 cells (`cell_witness.py <gxemul> <label> <pc> <msr>`).  Before this
repair the probe rowed three: (00, clear) `T ra`, (00, set) `T ra me`, (01, clear) `T ra odd`.

DERIVED BEFORE THE RUN, from the code (cpu_ppc_instr.c's prologue, cpu_dyntrans.c's read-ahead loop): the first fetch is slot 1
(addr 0xfec00004, which reads 0x23120e00, subfic) at pc = the entry pc; read-ahead translates slot 2 with pc = 0xfec00008 | (entry
pc & 3) and addr 0xfec00008, the -T halt fires (report 1, running cleared) and arm (a) returns; the subfic runs; the real fetch of
slot 2 halts again (report 2) and, its aligned pc equal to addr, arm (c) parks at that pc.  So on the fix every cell gives exit 0,
pc 0xfec00008 | (entry & 3), two reports both naming 0xfec00008, SRR0 kept and MSR as entered.  A guard that refuses a cell sends
its read-ahead failure on to arm (c), which parks at read-ahead time: ONE report, pc unchanged (the A1/A2 pattern of
p5_20261105/TRAODD_NOTE.md).  B3 sets MSR[ME] at read-ahead when pc != addr, and nothing after it reads MSR on this route.

MEASURED (cells: entry pc / MSR; `pc nonex msr`; every run exit 0, every halt naming 0xfec00008, SRR0 0x11111111, no checkstop or
UNIMPLEMENTED text):

| cell (pc low bits, ME) | entry      | MSR    | fix                   | B1 `&& !(pc & 2)`       | B2 `&& (!ME \|\| pc == addr)` | B3 `msr \|= pc != addr ? ME : 0` |
|---|---|---|---|---|---|---|
| 00, clear (`T ra`)     | 0xfec00004 | 0      | 0xfec00008  2  0      | 0xfec00008  2  0        | 0xfec00008  2  0          | 0xfec00008  2  0          |
| 00, set (`T ra me`)    | 0xfec00004 | 0x1000 | 0xfec00008  2  0x1000 | 0xfec00008  2  0x1000   | 0xfec00008  2  0x1000     | 0xfec00008  2  0x1000     |
| 01, clear (`T ra odd`) | 0xfec00005 | 0      | 0xfec00009  2  0      | 0xfec00009  2  0        | 0xfec00009  2  0          | 0xfec00009  2  **0x1000** |
| 01, set                | 0xfec00005 | 0x1000 | 0xfec00009  2  0x1000 | 0xfec00009  2  0x1000   | 0xfec00009  **1**  0x1000 | 0xfec00009  2  0x1000     |
| 10, clear              | 0xfec00006 | 0      | 0xfec0000a  2  0      | 0xfec0000a  **1**  0    | 0xfec0000a  2  0          | 0xfec0000a  2  **0x1000** |
| 10, set                | 0xfec00006 | 0x1000 | 0xfec0000a  2  0x1000 | 0xfec0000a  **1**  0x1000 | 0xfec0000a  **1**  0x1000 | 0xfec0000a  2  0x1000   |
| 11, clear              | 0xfec00007 | 0      | 0xfec0000b  2  0      | 0xfec0000b  **1**  0    | 0xfec0000b  2  0          | 0xfec0000b  2  **0x1000** |
| 11, set                | 0xfec00007 | 0x1000 | 0xfec0000b  2  0x1000 | 0xfec0000b  **1**  0x1000 | 0xfec0000b  **1**  0x1000 | 0xfec0000b  2  0x1000   |

Every cell matched its derivation.  The 82-row probe (table 6's instrument): the clone's fix 82/82, and **B1 82/82, B2 82/82, B3
82/82, each CONTROL=OK SYMPTOM=ABSENT RED=none** (`b123_table/probe82_{base,B1,B2,B3}.out`).  **So all three breaches are REAL:**
B1's refused cells (10 and 11, either ME) and B2's (unaligned with ME set) have no session, and B3's only observable is MSR on the
unaligned ME-clear cells, where `T ra odd` carries no msr row.

THE REPAIR THIS OWES (the class closure: passes 5 and 6 both found arm (a) x alignment cells).  Row the five missing cells as
sessions -- (01, set) entered at 0xfec00005, (10, clear/set) at 0xfec00006, (11, clear/set) at 0xfec00007 -- each pinning exit 0,
pc 0xfec00008 | low bits, two reports and MSR as entered; and add `T ra odd msr` (want 0).  The wants are this table's DERIVED
column, which the fix column confirms; none is read off a variant.  On the full grid: B1 reds the four nonex rows of the 10/11 cells,
B2 the three of the unaligned ME-set cells, B3 the msr rows of the three unaligned ME-clear cells (`T ra odd msr` among them).

## G1 and G2 -- the Gemini 4 Argon seat's pass-6 findings (_scratchpad/gweb/jobs_20261105_rounds/p6_qhs/gemini_web.out), MEASURED

Folded in by the coordinator after the table above ran.  `g12_table.run.sh` (frozen copy of `g12_table.sh`) -> `g12_table/` (log:
`g12_table_run.log`): the same discipline in a FRESH /tmp/gxqhs12 (`cp -a` of build/, clone-local .MUTANT, both sources cmp'd equal
to GXEMUL-SEC first, the fix rebuilt fresh first, restored cmp-clean and rebuilt, sentinel cleared).  Variants: `g12_variant.py`, one
exact edit each against the fix.

| variant | edit | 82-row probe (table 6's instrument) |
|---|---|---|
| fix (the clone's) | -- | 82/82, CONTROL=OK, SYMPTOM=ABSENT, RED=none |
| G1 | arm (b): `(cpu->pc & ~(uint64_t)3) != addr` -> `cpu->pc < addr` | **82/82**, CONTROL=OK, SYMPTOM=ABSENT, RED=none |
| G2 | arm (d): `cpu->cd.ppc.msr & PPC_MSR_ME` -> `cpu->cd.ppc.msr` | **82/82**, CONTROL=OK, SYMPTOM=ABSENT, RED=none |

**Both survive, and NO ROW CAN RED EITHER WITH THE EXISTING MACHINERY, so neither gets a row; both are disclosed.**  The reasons
are derived from the code and agree with every earlier table:

* **G1 differs from the fix only where the FIX TAKES arm (b).**  On every entry where the fix skips arm (b), `(pc & ~3) == addr`,
  which implies `pc >= addr`, so `pc < addr` is false there too; where the fix takes arm (b), G1 differs exactly when the moved pc
  lies above addr.  Arm (b) is taken only when the translator's OWN read raised the exception, and that has no producer here:
  cpu_dyntrans.c's quick lookup cache (`phys_page`) is filled only for pages with host memory (the generic lookup's
  `if (...host_load[index] != NULL) ...phys_page[index] = ppp;`), and a page with host memory never takes the translator's slow path
  (to_be_translated copies the word from the host page); every other page is re-translated by the generic lookup, which delivers
  the exception itself (`if (!ok) { ... cached_pc = cpu->pc; ...`) before the translator runs.  V2 (arm (b) deleted) and D11 (arm
  (b) without its refresh) are green in every table, which is that fact measured.  Gemini's derivation also misread two premises:
  the `isi` sessions never enter the failure block (the dispatch delivers their ISI), and their failing address is 0x20000000, not
  0x2000.
* **The coordinator's question -- "check what the isi session's setup allows" -- MEASURED:** `g12_explore.py` runs the isi setup
  with MSR[IP] added (msr = 0x60, so the ISI vector 0xfff00400 lies ABOVE the fetch 0x20000000), by continue (X1) and by one step
  (X2), on the fix and on G1.  Both legs: `[ memory_ppc: exception! vaddr=0x20000000 ... instr=4 ]` (the dispatch lookup's ISI),
  pc 0xfff00400, SRR0 0x20000000, MSR 0x60, the vector's zero word UNIMPLEMENTED -- the transcripts are byte-identical between the
  fix and G1 once the temporary path is normalised.  So a vector above addr is reachable, but never inside the translator's read.
* **G2 differs from the fix only where arm (d) is reached with MSR[ME] clear and another MSR bit set.**  Arm (d) is reached on no
  pmppc session (the window and slack sweeps, det_20261104/), and V4 (`if (0)`) and V5 (`if (1)`) at the same position are green in
  every table -- so no predicate in that position is observable.  Giving an existing ME-clear session another MSR bit does not
  bring it to arm (d): every -T session parks in arm (c) and every no -T fetch succeeds.

DISPOSITION: G1 joins the disclosed arm (b) class (D11, V2) and G2 the disclosed arm (d) class (D6, V4, V5) in the probe's clause
(e), each named; both run in table 7 predicted GREEN exactly.  Their producers are the ones the probe already discloses as absent:
for arm (d), a device declining an instruction fetch while running (the reconciliation's ROW 5, FILED pending X11); for arm (b)'s
taken side, a translator read that raises its own exception, which no measured session or machine produces (the probe's arm (b)
disclosure).  Neither is a new filing.

## G3 -- the Gemini seat's pass-6 replication (_scratchpad/gweb/jobs_20261105_rounds/p6_qhs_r2/gemini_web.out): NOT BUILT, covered

Arm (a)'s guard conjoined with `&& !cpu->running`.  Every rowed read-ahead failure is a -T halt, and memory.c clears running before
the read returns, so the conjunct is true on all of them; it differs from the fix only on a read-ahead fetch that fails with running
still 1, i.e. a device declining an instruction-width read while running.  det_20261104/window_sweep.out measured that producer
absent on pmppc: 422 sessions, real mode, no -T, every 4-byte offset of every `device list` window at MSR 0 and MSR[ME],
`WINDOW_SWEEP_NO_FETCH_EVIDENCE=0`, `WINDOW_SWEEP_ARM_D=NOT_REACHED` (without -T a non-existent address zero-fills, so only a device
can fail the read).  The probe's arm (d) disclosure named that producer but not this consequence for arm (a); repair 7 adds the
sentence and names `!cpu->running` there.  Per the coordinator, not built (the disclosure covers it).

## Repair 7b (2026-11-05) -- the coordinator: close the unaligned sessions' channel gaps rather than disclose them

**Step 1, the channel list** (read off the 103-row probe; `table7/probe103_frozen.py`):

| read-ahead session | session | pc | nonex | addr | stopped | msr | chkstop | srr0 | text / exc / unimpl / prompt / srr1 / lr |
|---|---|---|---|---|---|---|---|---|---|
| `T ra` (00, ME clear) | yes | yes | yes | yes | yes | yes | yes | yes | none |
| `T ra me` (00, ME set) | yes | yes | yes | -- | -- | yes | yes | yes | none |
| `T ra odd`, `o1m`, `o2`, `o2m`, `o3`, `o3m` | yes | yes | yes | -- | -- | yes | -- | -- | none |

Owed by sibling parity in each of the six: **srr0, chkstop, addr, stopped**.  `T ra me` lacked addr and stopped too (a disclosed
sentence until now), so repair 7b rows them there as well and the ME-set column stops being the exception: after it all eight cells
pin the same eight channels.  The text, exc, unimpl and prompt channels are pinned by NO read-ahead session (the 0x02040000
sessions carry them), and SRR1 and LR by none on this route -- not owed by parity; the probe now says why (item (b)).

**Step 2, MEASURED before any row** -- `b7b_table.run.sh` -> `b7b_table/` (log `b7b_table_run.log`): a fresh /tmp/gxqhs12 (`cp -a`
of build/), clone-local .MUTANT, both sources cmp'd equal to GXEMUL-SEC and to fix7 first, the fix rebuilt fresh first, restored
cmp-clean and rebuilt, sentinel cleared.  Variants: `b7b_variant.py`, one exact edit each.  Instrument: the 103-row table-7 probe.

| variant | edit | 103-row probe |
|---|---|---|
| fix (the clone's) | -- | 103/103 |
| R7b_a_srr0un | arm (a) writes SRR0 when pc != addr (R5_srr0_a's shape, gated) | **103/103 -- escapes: the srr0 gap is real** |
| R7b_a_chkun | the checkstop line printed on a read-ahead failure when pc != addr (B2_ra_chktext's shape, gated) | **103/103 -- escapes: the chkstop gap is real** |
| R7b_a_pcalign | arm (a) aligns pc when pc != addr (the nearest single edit to the halt address) | 97/103 -- already caught by the six unaligned pc rows |
| R7b_a_runun | arm (a) restores running when pc != addr (the nearest single edit to the stop) | 103/103 -- R5_arun's class: the real fetch's second -T halt stops the machine anyway, so a stopped row cannot see it either |
| R7b_f_me | the failure test `&& (msr & ME)` | 87/103 -- red only on ME-clear failing sessions (T cont, T step, again, T ra, T ra odd, o2, o3) |
| R7b_f_meclr | the failure test `&& !(msr & ME)` | 92/103 -- red only on ME-set ones (T me, T ra me, o1m, o2m, o3m) |
| R7b_f_ra | the failure test `&& translation_readahead` | 76/103 -- red only on sessions with a non-read-ahead failing fetch |
| R7b_f_unal | the failure test `&& cpu->pc != addr` | 87/103 -- red only on aligned failing sessions (T cont, T step, T me, again, T ra, T ra me) |

So **srr0 and chkstop close MEASURED gaps.  addr and stopped close none** -- no single edit in arm (a) moves the halt address
without moving pc (the halt address follows the slot and pc's page bits), and the real fetch's -T halt always stops the machine --
so their rows are parity rows owed by the sibling rule, each naming the mutants that already red `T ra addr` / `T ra stopped`.
The four failure-test narrowings (LATE_REPLICATIONS_20261105.md rows 33 and 41: "never built in tables 1-7") all red; a failure the
conjunct refuses skips the block and decodes the uninitialised fetch buffer ib, so WHICH rows red is stack-decided (W5/D7's class)
and only the sessions are predictable.  `T blr` stays green under the two that refuse its fetch (R7b_f_me, R7b_f_ra): one halt
report, pc = LR = 0x02040007, no UNIMPLEMENTED (sessions103_R7b_f_me/T_blr.txt) -- consistent with its stale ib holding the `blr`
word translated just before at 0x2004, which branches back to the same slot until the batch ends.  That is an INFERENCE from the
transcript, not a measurement of ib.  None of the four survives the rows, so none is a floor cell to row.

## Repair 8 (2026-11-05) -- codex GPT-6 Astra's pass-7 F1 and R1 (p7_20261105/codex_codex_qhs_p7.txt, DISPOSITION.md)

**MEASURED first** -- `b8_table.run.sh` -> `b8_table/` (log `b8_table_run.log`): a fresh /tmp/gxqhs12 (`cp -a` of build/), clone-local
.MUTANT, both sources cmp'd equal to GXEMUL-SEC and to fix7, the fix rebuilt fresh first, restored cmp-clean and rebuilt, sentinel
cleared.  Variants: `b8_variant.py`, one exact edit each, inserted in arm (c) before its park where V10_c_me_bad puts its transfer.
Instrument: the 129-row table-8 probe.

| variant | edit | 129-row probe | UNIMPLEMENTED printed in |
|---|---|---|---|
| fix (the clone's) | -- | 129/129 | isi, isi1, noT (the zero-word controls) |
| R8_c_meun_bad (F1) | arm (c): `if ((msr & ME) && pc != addr) goto bad;` | **129/129 -- escapes: the breach is real** | + T ra o1m, T ra o2m, T ra o3m |
| R8_c_clun_bad (mirror) | arm (c): `if (!(msr & ME) && pc != addr) goto bad;` | 128/129 -- `T_blr_unimpl` only | + T blr, T ra odd, T ra o2, T ra o3 |

So F1 was a floor cell: bad: (cpu_dyntrans.c, the `bad:` label), reached from a NON-read-ahead fetch as F1's real fetches are,
resets the slot, prints UNIMPLEMENTED at the unchanged pc, clears an
already-clear running and parks next_ic on nothing_call -- no pc, nonex, addr, stop, MSR, checkstop or SRR0 change -- and only the
unaligned ME-set cell reached it, which no non-read-ahead session holds (T me is aligned, T blr ME-clear).  The mirror was already
caught by `T blr unimpl` and is now caught on three read-ahead sessions too.

**THE CHANNEL RE-CHECK, from the block's own arms** (what each can put into a read-ahead session's transcript or registers):

| producer | channels | rowed on every read-ahead session after repair 8? |
|---|---|---|
| arm (a) return; arm (c) park | pc, nonex, addr, stopped | yes |
| arm (b) refresh-and-return | re-execution: nonex, pc, addr | yes |
| arm (d) machine check (ppc_exception) | pc -> 0x200, SRR0, SRR1, MSR (EE/RI/PR cleared), `[ PPC Exception` text, then the vector's zero word | pc, srr0, msr, unimpl yes; SRR1 and the exc text no -- see below |
| the checkstop fallback | checkstop text, stopped, pc | yes |
| bad: reached from a non-read-ahead fetch (a read-ahead transfer resets the slot and returns silently: `if (cpu->translation_readahead) return;` right after `ic->f = TO_BE_TRANSLATED;` at the label; this row said "bad: (any transfer to it)" -- codex pass 8, R1) | UNIMPLEMENTED text | **yes, from repair 8 (`unimpl`)** |
| the removed exit (pre-fix) | `read failed: TODO`, exit 1 | the session row (exit status), and the composite SYMPTOM key over every session |

Left unasserted on the read-ahead sessions, each for a stated reason: the `[ PPC Exception` text -- its only producer is
ppc_exception, which always moves pc to the vector and writes SRR0 = the faulting pc, both rowed (a single transfer cannot print it
and keep both); SRR1 -- written only by that same machine check, unreached on pmppc, and disclosed (pass 7 accepted it); the prompt --
the register rows read `none` without it; LR -- no arm writes it.  No other block-produced channel remains.

Repair 8's rows: `unimpl` (UNIMPLEMENTED absent) on all eight read-ahead sessions -> 137 rows; base 137/137 on build/ after both
clearance checks (CLEARANCE.txt, repair-8 section).  Table 9 (table9/VERDICT.md, PRETABLE_9.out first; COMPARE9_MISSES=0):
R8_c_meun_bad 134/137 on exactly the three unaligned ME-set unimpl rows, R8_c_clun_bad 133/137 on the three unaligned ME-clear ones
plus `T blr unimpl`; the probe's R1 paragraph corrected in place, quoting it.

## Repair 9 (2026-11-05) -- codex GPT-6 Astra's pass-8 B1 and R1 (p8_20261105/codex_codex_qhs_p8.txt, DISPOSITION.md)

**MEASURED first** -- `b9_table.run.sh` -> `b9_table/` (log `b9_table_run.log`): a fresh /tmp/gxqhs12 (`cp -a` of build/), clone-local
.MUTANT, both sources cmp'd equal to GXEMUL-SEC and to fix7, the fix rebuilt fresh first, restored cmp-clean and rebuilt, sentinel
cleared.  Variants: `b9_variant.py`, one conditional statement each, inserted immediately inside the failed-read block before arm
(a).  Instrument: the 137-row table-9 probe.

| variant | edit | 137-row probe |
|---|---|---|
| fix (the clone's) | -- | 137/137 |
| R9_tog_me1 (B1) | `if ((pc & 3) == 1) msr ^= ME;` | **137/137 -- escapes** (`T ra odd`, `T ra o1m` toggle twice) |
| R9_tog_me2 (B1's `== 2`) | the same at low bits 10 | **137/137 -- escapes** (`T ra o2`, `T ra o2m` toggle twice) |
| R9_tog_me0 | the same at low bits 00 | 133/137 -- `T cont msr`, `T step msr`, `T me msr`, `again msr` |
| R9_tog_me3 | the same at low bits 11 | 136/137 -- `T blr msr` |
| R9_tog_srr0_1 | `if ((pc & 3) == 1) srr0 ^= 0x100;` | **137/137 -- escapes** (the same cancellation, another state) |

THE MECHANISM: every read-ahead session enters the failure block TWICE -- the read-ahead failure (arm (a) returns), then the real
fetch (arm (c) parks) -- so anything the block toggles on pc's low bits is undone before the final state is read; only a ONE-ENTRY
failure at that pattern shows it.  **A one-entry 00 failure already exists:** `T cont`, `T step`, `T me` and `again` each enter the
block once at 0x02040000 (the failing first fetch is not read-ahead, and the -T halt is terminal), and R9_tog_me0 reds all four msr
rows.  `T blr` is the one-entry 11 failure (R9_tog_me3 reds it).  01 and 10 had none -- the breach.  Repair 9 adds `T blr o1` and
`T blr o2`: `T blr` with r3 = 0x02040005 / 0x02040006 (the breakpoint keeps read-ahead off, so the failing fetch enters the block
once and arm (c) parks it), each pinning `T blr`'s channels (session, pc, nonex, srr0, msr, chkstop, unimpl, lr).  The toggle of a
running flag is not in this family: the real fetch's -T halt clears running between the two entries, so such a toggle leaves
running 1 at arm (c) and checkstops or takes a machine check -- the chkstop, pc and srr0 rows see it (DERIVED from the code, not
measured).

Repair 9's rows: `T blr o1` and `T blr o2` (8 rows each) -> 153 rows, 20 sessions; base 153/153 on build/ after both clearance
checks (CLEARANCE.txt, repair-9 section).  Table 10 (table10/VERDICT.md, PRETABLE_10.out first; COMPARE10_MISSES=0): R9_tog_me1
152/153 (`T blr o1 msr`), R9_tog_me2 152/153 (`T blr o2 msr`), R9_tog_srr0_1 152/153 (`T blr o1 srr0`), R9_tog_me0 149/153 and
R9_tog_me3 152/153 as before.  R1 corrected in place, quoting it: in this note's repair-8 section and in the probe's loop comment.

## Repair 10 (2026-11-05) -- codex GPT-6 Astra's pass-9 B1 and R2 (p9_20261105/codex_codex_qhs_p9.txt, DISPOSITION.md)

**MEASURED first** -- `b10_table.run.sh` -> `b10_table/` (log `b10_table_run.log`): a fresh /tmp/gxqhs12, clone-local .MUTANT, both
sources cmp'd equal to GXEMUL-SEC and to fix7, the fix rebuilt fresh first, restored cmp-clean and rebuilt, sentinel cleared.
Variants: `b10_variant.py`, one conditional statement each at the top of the failed-read block.  Instrument: the 153-row probe.

| variant | edit | 153-row probe |
|---|---|---|
| fix (the clone's) | -- | 153/153 |
| R10_tog_srr0_meun (B1) | `if ((msr & ME) && pc != addr) srr0 ^= 0x100;` | **153/153 -- escapes** |
| R10_tog_srr0_me1 / _me2 / _me3 | the same gated on `(msr & ME) && (pc & 3) == 1` / `2` / `3` | **153/153 each -- escapes** |
| R10_tog_srr0_2 (R2's own variant) | `if ((pc & 3) == 2) srr0 ^= 0x100;` | 152/153 -- `T_blr_o2_srr0` only |

A toggle gated on BOTH alignment and ME runs on both visits of a two-entry read-ahead session with that ME state and cancels there;
it is seen only by a ONE-ENTRY failure in the same (low bits, ME) cell, and every unaligned one-entry failure was ME-clear.  Of pass
9's 16 combinations -- {00, 01, 10, 11} x {ME clear, set} x {two-entry, one-entry} -- three had no session: one-entry ME-set at 01,
10, 11.  Repair 10 adds them: `T blr m1`, `T blr m2`, `T blr m3` -- `T blr` with msr = 0x1000 and r3 = 0x02040005 / 0x02040006 /
0x02040007 -- each pinning `T blr`'s eight channels.  A condition that tells the two visits apart (translation_readahead) cannot
cancel, since it toggles on one visit only; running is 0 on both visits, so a condition on it reduces to one of these cells.
R2 (L4): `T blr o2 srr0`'s note named R9_tog_srr0_1, which it cannot catch (low bits 10 vs 01); it now names R10_tog_srr0_2.

Repair 10's rows: `T blr m1`, `T blr m2`, `T blr m3` (8 rows each) -> 177 rows, 23 sessions; base 177/177 on build/ after both
clearance checks (CLEARANCE.txt, repair-10 section).  Table 11 (table11/VERDICT.md, PRETABLE_11.out first; COMPARE11_MISSES=0):
R10_tog_srr0_meun 174/177 (the three m-sessions' srr0 rows), R10_tog_srr0_me1/_me2/_me3 176/177 each, R10_tog_srr0_2 175/177
(`T blr o2 srr0`, `T blr m2 srr0`).  The 16-cell grid is held whole (the probe's docstring names each cell's two sessions).

## Repair 11 (2026-11-05) -- codex GPT-6 Astra's pass-10 B1 and R1 (p10_20261105/codex_codex_qhs_p10.txt, DISPOSITION.md)

**MEASURED first** -- `b11_table.run.sh` -> `b11_table/` (log `b11_table_run.log`): a fresh /tmp/gxqhs12, clone-local .MUTANT, both
sources cmp'd equal to GXEMUL-SEC and to fix7, the fix rebuilt fresh first, restored cmp-clean and rebuilt, sentinel cleared.
Variants: `b11_variant.py`, one conditional statement each at the top of the failed-read block.  Instrument: the 177-row probe.
R11_tog_full (B1: `if ((pc & ~(uint64_t)0xb) != addr) srr0 ^= 0x100;`) and its eight low-bit x ME members R11_tog_full_<k><c|m>
(the same, also gated on `(pc & 3) == k` and ME clear or set): **177/177 each -- all nine escape.**  The masked read-ahead pcs
0xfec00008..b all become 0xfec00000 != addr, so the toggle fires on both visits and cancels; the masked one-entry pcs 0x02040000..7
all equal addr, so it never fires there.  The repair-10 pairs matched low bits and ME and still differed in the FULL pc.

**THE STRUCTURAL FIX:** each read-ahead cell gets a ONE-ENTRY PARTNER at the SAME full pc and MSR -- pc set to 0xfec00008 | low bits
directly and continued under -T, so the first fetch fails; a failed fetch is never translated, so no read-ahead follows, and arm (c)
parks it.  PRE-CHECK on build/ (cell_witness.py, `b11_table/partners_precheck/`): at each of 0xfec00008..b with MSR 0 and 0x1000,
exit 0, park at that pc, ONE halt report reading `memory READ: from non-existant paddr=0xfec00008 len=4 pc=0xfec0000X` -- the line
its two-entry pair prints twice -- SRR0 and MSR as entered, no checkstop or UNIMPLEMENTED text.

Repair 11's rows: the eight one-entry partners `T rp` .. `T rp o3m` (9 rows each, the read-ahead cell's channels) -> 249 rows, 31
sessions; base 249/249 on build/ after both clearance checks (CLEARANCE.txt, repair-11 section).  THE PAIRING INVARIANT, checked by
`pair_check.py` on the base run (base249/PAIRS.out) and on table 12's base leg (table12/PAIRS_base.out): PAIRS_OK=8/8 both times --
each partner's one halt report textually equals each of its pair's two (same paddr 0xfec00008, same full pc), the same msr command
and the same final pc, MSR and SRR0; a mismatched pair (T ra odd vs T rp o2) gives two distinct lines, so the check can fail.  Table
12 (table12/VERDICT.md, PRETABLE_12.out first; COMPARE12_MISSES=0): R11_tog_full 241/249 (all eight partners' srr0 rows), each
member 248/249 (its own cell's partner).  R1 corrected in place, quoting it, in the probe's docstring.

## Pass 11 records (2026-11-05) -- codex GPT-6 Astra's pass-11 R1 and R2; B1 graded clause-(e) debt (adj_p11_20261105/ADJ_MYTHOS_local.md, CLOSE-AFTER-RECORDS)

TEXT ONLY: no row, no variant, no table, no build.  Backups first: `ppc_ifetch_probe.py.pre_p11rec`, `gate_ppc.sh.pre_p11rec`.  The
edit scripts are kept beside this note (`p11rec_step_doc.py`, `p11rec_step_cmt.py`, `p11rec_step_gate.py`); the docstring was then
re-flowed to 131 columns, whitespace only (reflow_doc.py asserts it).

**R1 -- the pairing invariant (probe docstring).**  BEFORE: "So a toggle of pinned state under a condition on anything else the block
reads fires on both of the two-entry session's visits exactly when it fires on the partner's one -- it cancels on one side and shows
on the other -- and a condition on translation_readahead fires on one visit of the two-entry session and shows there."  AFTER: the
ruler's section-2 text, then that sentence quoted and marked FALSE (codex pass 11, R1; the ruler's reason: the block reads MSR, B1's
condition reads MSR, and the second visit's MSR is not the entry MSR).  THREE CHANGES to the ruler's text, each made on checking it
against the code:
* DROPPED the classification "a bit the block TESTS (MSR[ME], pc's low two bits)" / "a bit the block does not test" from the two
  enumerations, which now read "When the marker is MSR[ME] or one of pc's low two bits ..." and "When the marker is MSR[RI] (...),
  MSR[PMM], MSR[LE], or an SRR0 bit clear in the sentinel ...".  Arm (b)'s only pc test, `(cpu->pc & ~(uint64_t)3) != addr`
  (cpu_ppc_instr.c:4168), masks pc's low two bits OFF, so by the "tests means masks or compares" clause the ruling itself cites, the
  block does not test them; the ruling's verdict splits the family by generating-set membership, and the kept reason ("because those
  bits are held both ways") states it.
* NARROWED "the unaligned cells' pc rows" to "the pc rows of the unaligned cells carrying it": a one-bit marker reds only the cells
  whose pc carries that bit (bit 0: `T ra odd`, `T ra o1m`, `T ra o3`, `T ra o3m`, their partners and the matching `T blr` sessions;
  `T ra o2` and `T ra o2m` cancel like `T ra`).
* TAGGED the ME / pc catch "(DERIVED, not measured)", as the ruler tagged the RI escape: no self-referential member was built.

Verified by reading (the coordinator's checks):
* ME member, `if (translation_readahead || (msr & ME)) msr ^= ME` at the block's top.  `T ra me`: the read-ahead visit clears ME;
  the real fetch sees neither read-ahead nor ME; arm (c) parks (:4176-4178) before arm (d); final MSR 0 against `T ra me msr`'s want
  0x1000.  `T me` (one step) and `T rp me` enter once and clear it once: `T me msr`, `T rp me msr` (want 0x1000) red.  On the ME-clear
  cells it cancels (`T ra`) or never fires (`T rp`).
* pc member, `if (translation_readahead || (pc & 1)) pc ^= 1`.  The read-ahead loop (cpu_dyntrans.c:1937-1968) saves `baseaddr` but
  never restores cpu->pc, and the prologue (cpu_ppc_instr.c:4099-4102) keeps cpu->pc's low bits, so the read-ahead visit's write
  reaches the real fetch: `T ra odd` parks at 0xfec00008 against `T ra odd pc`'s want 0xfec00009; `T rp odd` (one entry at
  0xfec00009) parks at 0xfec00008, red on `T rp odd pc`; `T ra` cancels (0xfec00008 -> ..09 -> ..08).
* SRR0's sentinel 0x11111111: 0x100 set, 0x200 clear (computed).
* cpu_ppc.h: PPC_MSR_ME :166, PPC_MSR_PMM :174, PPC_MSR_RI :175, PPC_MSR_LE :176.  By macro name, src/cpus only writes RI and LE
  (cpu_ppc.c:297, :299, :335) and never uses PMM; every session that reaches the failure block enters with MSR 0 or 0x1000 (the isi
  sessions set 0x20 and never reach it), so all three are clear at entry.

**R2 -- the bound (probe docstring).**  BEFORE: "The bound: a condition on state the block neither reads nor writes -- the GPRs the
subfic changes, next_ic -- is outside it, as the field-write disclosure says."  AFTER: "The bound: a condition on state the block
does not READ: the GPRs the subfic changes (neither read nor written here) and next_ic (written by arm (b)'s refresh, arm (c)'s park
and the checkstop fallback, never read) is outside it.  This sentence called next_ic state the block "neither reads nor writes":
FALSE (codex pass 11, R2)."  ONE CHANGE to the ruler's text: its closing "as the field-write disclosure says" DROPPED -- that
disclosure covers writes to fields the block neither reads nor writes, not conditions on unread state, and next_ic is written.
Verified: next_ic is written at :4177 (arm (c)) and :4207 (checkstop fallback), and by arm (b)'s `quick_pc_to_pointers(cpu)` at
:4169.  pmppc's PPC750 is 32-bit (cpu_ppc.h:85, cpu_ppc.c:120), and the 32-bit build defines MODE32 and re-includes
quick_pc_to_pointers.h before cpu_ppc_instr.c (build/src/cpus/tmp_ppc_tail.c:83, :117-118, generated).  So the macro writes next_ic
at quick_pc_to_pointers.h:12-14 on a phys_page hit; otherwise ppc32_pc_to_pointers writes it at cpu_dyntrans.c:894-895, or its
generic fallback at :832-833.  The ruling's ":832" is the last of three sites; its claim holds on every path.  No line of
:4128-4208 reads next_ic or a GPR.

**Siblings of R1, comment-only.**  The same universal stood in the partner loop's header comment ("So a toggle conditioned on any of
those fires on both visits exactly when it fires on the partner's one") and in gate_ppc.sh's qhslowifetch block comment ("so a toggle
that cancels over the two-entry session's two visits shows once on its partner").  Both now carry the ruler's qualifier -- a
condition the toggle itself leaves unchanged; in the gate also "on state the block reads" -- and point to the docstring's SCOPE.  No
copy of R2's claim stood in the gate (its "refreshes next_ic" is true).

**B1** stays clause-(e) debt, disclosed by the R1 text; no row and no variant (the ruling: rowing the family bit by bit is the
linear-in-cells convergence the stop rule names).

**Proof** (`p11rec_proof.py` -> `p11rec_proof.out`, sentinel P11REC_PROOF_DONE).  Against table12/probe249_frozen.py and against the
pre_p11rec backup:
* the AST minus the docstring is EQUAL;
* the AST with every string constant masked is EQUAL;
* the token stream minus comments and the docstring is EQUAL.

Negative control: one printed string changed in a scratchpad copy gives DIFFERENT under both checks.  No printed string changed, so
the probe was not re-run.  The docstring has 275 lines, a maximum width of 131 and no trailing spaces.

gate_ppc.sh: the diff is line 301 becoming 301-302, inside the qhs block, and `bash -n` passes.  The #575 block is byte-identical
(md5 e31a0592ed42, 146 lines, before and after).  _scratchpad/w575/ was not touched; no build tree was touched; no git.  A stray
`__pycache__` (02:44-02:46 local, left by repair 7's variant imports) was removed from this directory.

*Corrected 2026-11-05 (main loop): this file's time-of-day stamps (removed: ~09:3xZ, ~10:1xZ, ~11:0xZ, ~12:0xZ, ~11:1xZ, ~12:0xZ) were GUESSES, taken from the main loop's own wrong clock, that ran up to 3.5 hours AHEAD of the real time; one section header was even out of order. The qhs landing-kit agent found them.  The file's own timestamps are the record: created 10:22Z, last written 12:03Z before this note (UTC).*
