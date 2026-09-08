# DESIGN — `lcabadval`: eleven live terminating calls in `dev_lca.c`, six of them value guards

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** You have refused four of my rounds today by
ratifying the edit and rejecting the witness, and each time the missing row caught something real.
**This brief proposes a six-armed change; assume the enumeration is wrong somewhere.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**

**SCOPE:** `GXEMUL-SEC/src/devices/dev_lca.c`, `src/include/thirdparty/alpha_lcareg.h`,
`src/machines/machine_alpha.c`, `GXEMUL-SEC/regress/lca_confwidth_probe.py`.

**VERDICT LINE FIRST.**

## §C — SETTLED PREMISES, all re-derived today

**S1 — ELEVEN LIVE `exit(1)`, in four classes.** `grep -cE '^[[:space:]]+exit\(1\);'` gives 12; one
(`:129`) is inside a commented-out block, so **11 live**:

    :73  :85    INTERRUPT STUBS   lca_interrupt_assert / _deassert -- bare fatal()+exit(1), NO GUARD
    :134          BUS             bus != 0  (i.e. d->ioc_conf & 1)
    :163          RANGE           ofs > len
    :215 :235 :250 :265 :289 :304  VALUE GUARDS -- the six below
    :324          DEFAULT ARM     unimplemented offset

**S2 — THE SIX VALUE GUARDS, enumerated by reading `if (idata`:**

    :203  IOC_CONF   idata & ~1
    :231  TB_ENA     idata & ~IOC_TB_ENA_TEN
    :246  W_BASE0    idata != 0ULL && idata != 0x300800000ULL
    :261  W_MASK0    idata != 0x700000ULL
    :285  W_BASE1    idata != 0x240000000ULL
    :300  W_MASK1    idata != 0x3ff00000ULL

**So the accept-row set is SIX, not four** — an earlier census in this row's own record dropped
`W_BASE1` and `W_MASK1`, and that is now corrected.

**S3 — THE TEXT-ORACLE PREREQUISITE IS DISCHARGED.** This row's rows must match the `fatal()` TEXT
rather than the exit status, because the two interrupt stubs kill with the same status as every value
guard. `#506` (committed today, `7a41b3f`) repaired both narrowing diagnostics to
`0x%" PRIx64` with `(uint64_t)idata`, so the IOC_CONF arm's text is now sound — measured HEAD 4/6 ->
fix 6/6 by `regress/lca_confwidth_probe.py`.

**S4 — REACHABILITY IS ESTABLISHED AND THE MACHINE IS PROVEN.** `machine_alpha.c:61` adds `"lca"`
under `case ST_ALPHABOOK1:` only, and `lca_confwidth_probe.py` already drives a guest `stq` into
`LCA_IOC_CONF` on stock `alphabook1`, kills the host, and reads the diagnostic out of the pty.

**S5 — `dev >= 21` IS THIS FILE'S OWN FIX PRECEDENT.** At `:127-130` the guard survives but its
`fatal()` + `exit(1)` are commented out and `dev = 0;` executes instead — *delete the kill, substitute
a safe default, keep going*, decided in this very file by someone else.

## The questions

**Q1 — ONE ROUND OR SEVERAL?** Six value guards share a shape but not a semantics: two are bitmask
tests (`& ~mask`) and four are equality tests against a single accepted constant, one of which accepts
two values. **Does one fix design cover all six**, or does the round scope split — and if it splits,
where?

**Q2 — WHICH OPTION-SET MEMBER PER ARM?** DELETE · DECLINE (silent) · DECLINE + LATCHED ANNOUNCE ·
ACCEPT · FAULT · BACKED ACCEPT · IMPLEMENT. **S5 is an in-file precedent for a sixth thing — decline
with a safe default.** Note FAULT needs the CPU family's exception delivery; this is Alpha, and a
prior finding recorded that **Alpha has no `memory_rw` exception path equivalent to MIPS/M88K**, so
check rather than assume.

**Q3 — THE ACCEPT ROWS.** The de-escalation clause says a fix removing a host-fatal guard owes a row
per predicate proving legal writes still land. **For each of the six, name the value a guest can put
in the predicate's operand** — and say which of the six cannot carry an accept row at all (a
write-1-to-clear bit, a read-only field, or a value the store arm filters before the predicate sees
it).

**Q4 — THE INTERRUPT-STUB CONFOUND.** `:73`/`:85` are bare `fatal()`+`exit(1)` with the ISA PIC chain
wired to them, so **any interrupt ends the host with the same status as the guards under test**.
Does that make the stubs a prerequisite of this round rather than a sibling — and if the rows match
text, is that sufficient?

**Q5 — THE SMALLEST EDIT that breaks the fix and still passes. Name the row you expect to stay
green.** With six arms I expect the clause-(d) family to have an easy target: a repair applied to five
arms and not the sixth, or conditioned on a field the guarded body reads.

## What I am not asking

Do not write a patch or a probe and do not run anything. **Nothing ships until the flagship
adjudication on 2026-09-09.**

**If, while verifying a claim, you found something ELSE — say so.**
