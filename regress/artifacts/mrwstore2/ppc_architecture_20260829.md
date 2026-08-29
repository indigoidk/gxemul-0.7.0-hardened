# `mrwstore2` — the hold question ANSWERED from the local PowerPC manuals, 2026-08-29

**Reading only.  No build, no probe, no edit.**

The row's hold question is explicit about what would decide it:

> *"what does real PPC hardware do on a straddling store whose second half faults, and is our
> current behaviour actually wrong?  **If we cannot establish the hardware behaviour, then 'fix'
> is unwarranted.**"*

**We CAN establish it.**  Four PowerPC manuals have been sitting in `_scratchpad/` — and the
carrier records that they were UNDOCUMENTED in its own source list until 2026-08-27, *"while a
PowerPC straddling-store defect (`mrwstore2`) was being recorded with no reference to any of
them."*  This is that reference.

## THE CONTROLLING TEXT — §6.1.4 "Partially Executed Instructions"

`_scratchpad/ppc_pem_32and64_2005.txt`, read at `:10679-10687`.  Verbatim:

```
:10680  The architecture permits certain instructions to be partially executed when an
        alignment exception or DSI exception occurs, or an imprecise floating-point
        exception is forced by an instruction that causes an alignment or DSI exception.

:10683  Non-multiple/string store instructions that cause an alignment or DSI exception --
        Some bytes just before the boundary may have been updated.

:10685  In the cases above, the number of registers and the amount of memory altered are
        implementation, instruction, and boundary-dependent.  However, memory protection
        is not violated.

:10687  Partial execution is not allowed when integer LOAD operations (except
        multiple/string operations) cause an alignment or DSI exception.
```

And the restart half, at `:4763` of the same manual:

```
        Any other load or store instruction may be partially executed and then aborted
        after having accessed a portion of the memory operand, and then re-executed
        (i.e., restarted, by the processor or the operating system).
```

Corroborated independently in Book III, `_scratchpad/ppc_oea_book3_v201.txt:2297-2312`: a
Store may *"not be performed or might be only partially performed"*, listing *"The Store
instruction causes a Data Storage exception"* as one of the cases; and at `:2302-2306`, an
operand crossing a virtual page boundary has *"the accesses to the components of the operand in
each page ... treated as separate and independent accesses."*

## WHAT THAT ANSWERS

**Question: does real hardware write the head before faulting on the tail?**  ANSWER: **it is
permitted to** — *"some bytes just before the boundary may have been updated"* — and the amount
is explicitly **implementation-dependent**.  The architecture mandates NEITHER behaviour for
non-multiple stores; it licenses both.

**Question: is our current behaviour wrong?**  ANSWER: **no, not architecturally.**  Head
written, tail faults, instruction restarted, head written again is precisely the
partial-execution-then-re-execution sequence §6.1.4 describes.  For ordinary storage the second
write is idempotent and invisible, which is why the architecture is relaxed about it.

> ### *** SO THE DISPOSITION FOLLOWS, AND FOR A STRONGER REASON THAN THE QUESTION ANTICIPATED.
> ### The question said 'if we CANNOT establish the hardware behaviour, then fix is
> ### unwarranted'.  We CAN establish it, and it says the behaviour is PERMITTED. ***
>
> **DOCUMENTED-ONLY.**  Not "unwarranted because unknown" but "unwarranted because the
> architecture explicitly allows what we do, and pins the amount as implementation-dependent."
> A fix that made the head write atomic-with-the-tail would make this emulator MORE strict than
> the architecture — which is the divergence-from-real-hardware risk the row already suspected,
> now confirmed from the manual rather than feared.

## THE ONE THING THIS DOES **NOT** SETTLE, stated so it is not read as more than it is

§6.1.4 is about **architectural correctness**, not about **MMIO side effects**.  The row's
symptom is that an MMIO head sees the write TWICE, and a device side effect is not idempotent
the way storage is.  The architecture does not carve out caching-inhibited storage in §6.1.4.

**But that gap does not reopen the fix**, because the amount altered is implementation-dependent:
a guest that issues a misaligned store spanning a page boundary into MMIO has no architectural
guarantee about how many times the head is written, so **there is no correct behaviour for us
to converge on.**  The honest statement is that the guest's construct is outside what the
architecture promises, not that our emulation of it is wrong.

*Relevant nearby text worth a future reader's time: `:11878` treats `stwcx.`/`stdcx.` and
Caching Inhibited specially, and `:9548` addresses caching-inhibited/write-through access
granularity.  Neither governs the ordinary non-multiple store this row is about, but both are
where a MMIO-specific rule would live if one existed.*

## STATUS

The hold question is **discharged on its own terms**.  What remains is a records action
(record the disposition and cite these lines), not a research one.

*Provenance discipline: every line above was read from the local extracted text at the line
numbers given, not from recollection of the architecture.  This project shipped ARM page
numbers from panel output in three rounds and adopted the read-it-locally rule afterwards; the
PowerPC manuals have been present since at least 2026-08-27 and this row had never used them.*
