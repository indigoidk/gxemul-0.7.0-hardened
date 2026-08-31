# Read-only review of the `#497` diff — control flow, and one cross-file claim

**Tree: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\src\`.  IGNORE ANY OTHER `src/` under the
project root — three pristine-2021-upstream copies live there, and a seat that reads one
reports line numbers off by hundreds.  If your line numbers disagree with mine by more than a
few, say so rather than reconciling silently.**

**READ-ONLY.  Do not build, do not run the emulator, do not write to any tree.** Another seat
is running a kill table right now against this very diff and its oracles are wall-clock
sensitive; a concurrent build corrupts its measurement rather than merely slowing it.

## The diff under review

`GXEMUL-SEC/regress/artifacts/widthkillclass/opus_impl_20260830/fix497.diff` — 217 lines,
128 added. It de-fatalises six width guards in `DEVICE_ACCESS(sgi_re)` (`src/devices/
dev_sgi_re.c`, lines 221–384). Each of six address windows currently reads:

```c
        if (len != 8) {
                fatal("TODO: unimplemented len=%i for CRIME_RE_TLB_A\n", len);
                exit(1);
        }

        if (writeflag == MEM_WRITE) { ... } else { fatal(...); exit(1); }
```

and becomes a latched decline spliced as an `else if`, so control falls to the function's
common tail rather than returning early.

## Please do not simply ratify

Two premises this project supplied today were refuted by seats that ran something instead of
agreeing — a census where `grep` counted commented-out code as live, and a "host memory
safety" phrase that `offsetof` showed to be intra-struct corruption. **Check the premises.**

## The questions

**Q1 — THE SKETCH RULE, and it is the one that has actually bitten here.** A proposed edit is
not a fix until it has been run against the enclosing function's REAL control flow. Four
independent readers once wrote `if (r == 3) return;` into a function whose last three lines
are `if (writeflag == MEM_READ) memory_writemax64(cpu, data, len, odata); return 1;` — an
early return skips that and hands a guest read an untouched buffer.

**For EACH of the six sites: does the spliced `else if` reach the common tail on every path?**
Show me the control flow, not an assurance. In particular: after a DECLINED access, what does
the function return, and what does the guest see in its load buffer?

**Q2 — A CROSS-FILE CLAIM I WANT CHECKED INDEPENDENTLY.** The LINEAR site comments assert that
the `len == 8` requirement is the only thing preventing an out-of-bounds array write, because
`tlbi = ((relative_addr & 0x7f) >> 2) & 0x1f` reaches 31 and the store writes `[tlbi+1]` into
a `[32]` array — and that **8-byte alignment keeps `tlbi` even and therefore ≤ 30**, with the
alignment supplied by MIPS raising ADES/ADEL, citing `src/cpus/cpu_mips_instr_loadstore.c`.

**Open that file and tell me whether the alignment claim holds.** Can a guest reach
`DEVICE_ACCESS(sgi_re)` with `len == 8` and a `relative_addr` that is NOT 8-byte aligned —
by any path: an unaligned load/store variant (`ldl`/`ldr`/`sdl`/`sdr`), a different CPU family
sharing this device, DMA, or the debugger? **If yes, the OOB is reachable TODAY and this round
is understated.** If no, say what enforces it.

**Q3 — THE LATCHES.** The fix adds six per-site `int warned_*` fields. Check: are they in
`struct sgi_re_data` (the one `malloc` that serves all four handlers)? Does each site test and
set its OWN bit, with no sharing? Does each message carry the `(once)` marker — the fork's
plurality suppression form, 9 of 14 sites? **And the one that matters most: can any OTHER
code path set one of these fields?** A latch a neighbour can set is silenced by benign traffic.

**Q4 — WHAT DOES A DECLINED READ RETURN?** `odata` is never assigned anywhere in this handler
and every read arm currently `exit(1)`s, so the common tail's `memory_writemax64()` is **dead
code today**. This fix makes it live for the first time on a declined 4-byte read. Confirm
`odata`'s initialisation and say what value the guest actually gets. A defined 0 is fine; an
uninitialised stack value is not, and "it happens to be zeroed" is a different claim from "it
is initialised."

**Q5 — ANYTHING THE DIFF CHANGES THAT ITS COMMENTS DO NOT MENTION.** Write commit messages
from the diff, never from intent. Is there any hunk whose effect is not described by the
comment above it?

## Output

**VERDICT LINE FIRST** so it survives truncation, then Q1–Q5 with file:line evidence you have
actually read. An honest UNKNOWN outranks a confident guess. If you find nothing wrong, say
that plainly rather than manufacturing a finding — but say which of the five you were able to
settle from the source and which you were not.
