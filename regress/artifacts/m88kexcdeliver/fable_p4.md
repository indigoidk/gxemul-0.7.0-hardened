# Fable 5.1 review seat -- m88kexcdeliver (#502) PASS 4 (the closing pass on the v4 repair), 2026-09-06 ~08:45-09:02
# Preserved verbatim from the Agent-seat return (the seat writes no file of its own).  Liveness token returned:
# FABLE_M88KEXC_P4_ALIVE_20260906, with the brief's first line quoted.

**VERDICT: ONE MORE REPAIR -- the {class} x {SFRZ set, non-trap} cells. Not the two v4 repairs, which both hold. The Opus
measuring seat's table 5 (`_scratchpad/m88kexc/opus_p4_logs/`, 08:28-08:34, frozen v4 md5 0d5c0f33, clone re-baselined from SEC,
restore-from-SEC `cmp` per mutant, BASE 23/23 both ends, sentinel cleared) scored `M_SFRZMIS` 23/23 and `M_OVFSUPONLY` 23/23. I
rule the first a floor breach (L2) and the second clause-(e) debt; a valid closing pass cannot carry a surviving 23/23 in the (d)
closure, so this pass does not close.**

**Repair 1 (indclr / M_NOIND) -- UPHOLD.** BASE `indclr` psr=0x8000000b epsr=0x80000000 (the EPSR channel also proves the `stcr`
landed); `M_NOIND.out` psr=0x80000009 bad=psr, 22/23; the mutant edits the real token (`| M88K_PSR_IND` -> `| 0`, anchor `disable
interrupts,`); gate pin names the row. Frozen md5 = shipped probe (0d5c0f33), durable copies identical to scratch.

**Repair 2 (HALT classifier / M_NOSTOP) -- UPHOLD, one REFINE.** `EXPECT_VECTOR` 0x032/0x072 and `pc != 8 * V_DIV0` verified;
`M_NOSTOP.out` resid50/sfu1h -> STOP, 21/23; HEAD sfu1h now STOP (first divu halts on 0x008 != 0x072). REFINE: `halted` accepts any
`"stopped"` substring, which makes its `"machines stopped"` term dead and disagrees with `stopped` at anchor `stopped = "machines
stopped" in tr`. Equivalent today (the only other emitters, `cpu_dumpinfo` and `debugger.c` anchor `", stopped"`, are INFO-level
and never follow `continue`), but a future diagnostic wording containing "stopped" re-opens exactly the gap codex named.
`halted = diag is not None and stopped` -- narrowing only, so it owes a BASE re-run, not a table.

**SFD1 -- yes, and now MEASURED, not argued:** `M_NOSFD1.out` **1/23** (08:31): 21 rows bad=psr (0x80000003) **and sfu1h STOP at
pc=0x44** -- the handler's legal divu executed instead of raising SFU1, a second, behavioural channel. The exact-compare argument
holds because SFD1 transitions 0->1 on every first-fault row (the IND gap was a 1->1 transition) and the write is an OR-in (anchor
`m88k_stcr(cpu, cpu->cd.m88k.cr[M88K_CR_PSR]`), so no bit can vanish except by editing its own token. Manual: `mc88100.txt:2036-2038`,
`:8715-8722`, `:9153-9154`.

**The breach, and my warrant.** `M_SFRZMIS` (`if (!is_trap)` -> `if (!is_trap && vector == M88K_EXCEPTION_MISALIGNED_ACCESS)`,
anchor `Non-trap exceptions when the shadow freeze bit`) sweeps 23/23 because `error` is the only frozen non-trap row and its second
fault is a misaligned `ld`. Both axes are body-tested partitions of predicates that DOMINATE the diff's tail labels -- `switch
(vector)` and `if (cpu->cd.m88k.cr[M88K_CR_PSR] & M88K_PSR_SFRZ)` -- and the pair is jointly reachable in one instruction (an `add`
overflow inside any handler). The clause-(e) counter-reading ("the frozen path erases the class, so class is untested there") fails
because switch 1 tests the class BEFORE the freeze test and the frozen path's outcome depends on it -- sfu1h is itself a frozen
non-trap row whose class decides HALT vs re-route. This is the `pendboth` shape. **Closure is finite and one diff:** frozen non-trap
cells reachable for classes 4 (rowed), 5, 6 (contrived: handler `stcr` MODE-clear with SFRZ kept, then a privileged op), 8 (handler
`stcr` SFD1-clear then `divu`), 9 (handler `add r2,r3,r4`, one word); 7 and 10 have no non-trap route. Each row is `error` with a
different handler word and identical expectations (0x50, shadows frozen at 0x10006/0x1000a/0x1000e, EPSR 0x80000002). Owes one
table: M_SFRZMIS plus one exemption variant (`&& vector != DIV0`) plus BASE.

`M_OVFSUPONLY` (implemented only if MODE set, at OVF) 23/23 -- **clause (e), not floor**: `m88k_exception` never TESTS MODE (only
reads it in the OR-in); the tests are in the caller `X(tb0)` and callee `m88k_stcr`, outside the function boundary. Disclose:
user-mode instruction rows exist for classes 5/6/8; 4 and 9 have none; 7 and 10 have no user route by construction (`X(tb0)`: any
user trap < 128 raises PRIVILEGE). If a diff is being cut anyway, `umisalign`/`uovf` are two words each.

**Denominator I consider closed** (tables 3/4/4b/5): 12 reachable class x route cells (7-insn, 10-insn disclosed); fallback
on/off/stop (M_REVERT 3/22, M_DELIVERALL 21/23, M_NOSTOP 21/23); tail labels/bound/return (M_NAIVE 3/22, M_TAILLE 21/22,
M_TAILRETURN 2/23 -- 4b's anchor is the new arm's `break`); {SFRZ} x {is_trap} 4 cells incl. frozen-shadow polarity both ways
(M_SFRZTRAP 21/22, M_UPDSHADOWTRAP 22/23 via `error`); VBR; PSR SFRZ/IND/SFD1/MODE/C all measured; EPSR (M_NOEPSR 2/23, M_EPSRAFTER
2/23 re-measured on v4); shadows (NOSHADOW/SNIPX 3/23 -- survivors usertb+HALT rows and dslot+HALT rows respectively, verified;
DSLOT/SFIPNOTGT/DSLOTSWAP 21/22); LEVEL 3/23. **Open:** {class} x {frozen, non-trap} for 5/8/9 (above). **Disclosed:** {class} x
{MODE}, {class} x {delay_slot} beyond DIV0 (deferred to `m88kdslotshadow` -- the arm is known wrong, so more pins are more re-pins),
M_DELAYALWAYS, vectors 0..3, DMT-frozen, SSBR, fcr2/4/5, first-exception SFU1, exact INFO.

**Records (L4, fold before commit):** (a) `m88kexctaildefault` and `m88kmxmkill` are in `ledger.json` (opened 2026-09-06) but have
**zero** mentions in `OUTSTANDING_BUGS.md` (`m88ktbnd` only inside the m88kexcdebt parenthetical) -- `check_bugfile_sync.py`'s own
rule is "every OPEN ledger row must be findable in OUTSTANDING_BUGS.md". (b) CHANGELOG :134 lists `m88kexctaildefault` as "earlier
from this campaign" while :121 says it was never filed until now -- :134 is the wrong one. (c) CHANGELOG :62 "gate 11 pins 22/22" and
:140 "22/22, probe_v3_fix_final.out" are stale against the 23/23 gate pin and `probe_v4_fix_final.out`. (d) codex F15 unapplied:
product comment `(shadows updated normally)` is true only for an unfrozen trap naming 10; frozen, it takes the is_trap exemption with
shadows frozen. (e) `Table 6-3: NIP = the branch target` (product comment and probe docstring): Table 6-3 says the shadows copy
XIP/NIP/FIP; the delay-slot values are `mc88100.txt:2093-2104`. (f) Gate comment names `killtable4/` but not `killtable4b/`, where
M_TAILRETURN's 2/23 lives. **Also found, LOW, documented-only:** the re-route's `fatal("[ SFRZ already set in PSR => ERROR ]")` is a
guest-drivable unlatched `fatal()` (supervisor-only: any fault inside a handler), pre-existing but now reachable by seven more
classes -- floodclass.

Read-only throughout: no file under GXEMUL-SEC/build/est/build-asan edited, nothing built or run; every score above is quoted from
a named `.out` whose `M88KEXC_DONE` sentinel I checked.

# Main-loop disposition (2026-09-06 09:0x): every item applied -- rows errpriv/errunimpl/errdiv0/errovf + umisalign/uovf (v5,
# table 5 = killtable5/, all killed as PRETABLE5 predicted); classifier REFINE applied; (a) bug-file block added; (b) CHANGELOG
# corrected; (c) restated at 29/29 / probe_v5_fix_final.out; (d) and (e) product comments corrected and propagated (rebuild_fix2.log);
# (f) gate comment names killtable4b/ and killtable5/; m88ksfrzfatal filed LOW.
