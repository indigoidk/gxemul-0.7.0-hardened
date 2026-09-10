# `mipsextshift` -- a NEGATIVE shift count driven straight from a guest instruction word, on the primary architecture

Nonce: `CODEX_MIPSEXT_20260910`. Open with `VERDICT:` naming the disposition and the exact edit, then echo
the nonce.

Ordinary correctness maintenance on a CPU model in an emulator written in C99. **The tree is
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`**; three unrelated 2021-vintage copies sit elsewhere under the
project root. **Enumerate arithmetic; do not reason about it.** **Verdict line first.**

**Please do not simply ratify.** Five briefs of mine this week had premises refuted by a seat that opened
the file, and every refutation improved the round. **Check the premises, not just the derivations.**

## THE SITES

**`X(ext)`** in `src/cpus/cpu_mips_instr.c`:

```c
int msbd = ic->arg[2] >> 5, lsb = ic->arg[2] & 0x1f;
int size = msbd + 1;
uint32_t rs = reg(ic->arg[1]);
uint32_t x = (rs << (32-lsb-size)) >> (32-lsb-size);
reg(ic->arg[0]) = (int32_t) (x >> lsb);
```

`msbd` and `lsb` are each decoded independently in `0..31`, so `32 - lsb - size` ranges `-31..31`.
**Enumerating all 1024 pairs gives 496 with a NEGATIVE count**, which is undefined (C99 6.5.7p3). The left
operand is `uint32_t`, and **that is the trap**: a reader checking *"is this unsigned?"* passes the site,
because a negative COUNT is undefined whatever the operand's type.

**`X(dext)`** is the same shape at 64 bits and the cast makes it look guarded rather than fixed:

```c
uint64_t x = (rs << (uint64_t)(64-lsb-size)) >> (uint64_t)(64-lsb-size);
```

A negative `int` converted to `uint64_t` becomes an enormous positive value, so the count is then at or
beyond the width of the type — form (b) instead of form (a), still undefined. **The cast converts one
undefined form into another while reading as a precaution.**

## THE DESIGN QUESTION, and it is the whole round

**I believe this is a FIELD-VALIDATION defect rather than a shift defect, and that decides the fix.** MIPS
requires `lsb + size <= 32` for EXT (and the corresponding bound for the `dext` family); an encoding
violating it is architecturally **UNPREDICTABLE**. So masking the shift count would give a defined answer
to a question the guest was not entitled to ask, and would make invalid encodings look supported.

**But I am not confident about what the model should do instead, and that is what I want settled.**

## THE QUESTIONS

1. **PREMISES AS QUESTIONS.** Re-derive the ranges from the decoder. Are `msbd` and `lsb` really
   unconstrained in `0..31` at the point the handler runs, or does the DECODER already reject some
   encodings before the handler is reached? **If the decoder validates, the whole row collapses and I want
   to know.** Check `dextm` and `dextu` too: their variant adjustments to `msbd`/`lsb` happen somewhere,
   and where they happen decides where a bound belongs.
2. **WHAT DOES THE ARCHITECTURE ACTUALLY REQUIRE?** `_scratchpad/mips64_volII.txt` and
   `mips32_volII.txt` are local — read them rather than reasoning. Is the out-of-range case
   UNPREDICTABLE, or does it mandate a Reserved Instruction exception? **Those are different dispositions
   and this project has been burned by claiming an architecture mandates something it merely permits.**
3. **WHICH OPTION-SET MEMBER**, from {delete, silent decline, decline + latched announce, accept, fault,
   implement}? Note that a CPU instruction handler is not a device access, so the FAULT member here means
   the CPU's own exception mechanism rather than the memory layer's failed-device path. Say which
   mechanism this tree already has for an unimplemented or invalid encoding on MIPS, and whether these
   handlers can reach it — **grep the fork for how a neighbouring MIPS handler rejects an encoding, since
   the tree's own idiom is worth more than an argument.**
4. **THE SMALLEST HONEST EDIT for each of `ext`, `dext`, `dextm`, `dextu`** — and say whether they want
   ONE shared bound or four, given the variant adjustments.
5. **IS THERE A SIBLING WITH THE SAME SHAPE?** `X(ins)`, `X(dins)`, `X(dinsm)`, `X(dinsu)` are the insert
   counterparts. A recent census reported INS's middle shifts enumerate safely to `0..31` even for
   reversed fields — **re-check that**, because if it is wrong the round is bigger than I think.
6. **THE DETECTOR.** The floor needs failure on the pre-fix build, on a verbatim reinstatement, on a null
   medium, and on a NULLED REPAIR. Name the rows and per row the mutant it kills and the observable that
   differs. **The hard part here and I want it addressed directly: what IS the observable?** Undefined
   behaviour gives no portable wrong answer, so a row asserting a particular wrong result on the pre-fix
   build would be pinning one compiler's lowering. The project's `#510` precedent shipped on a sanitizer
   differential plus a source pin, and `build-asan/` already carries the undefined-behaviour sanitizer.
   **A caution from that round: the diagnostic count is not an execution count**, because the sanitizer
   suppresses repeats at an already-reported location.
7. If you found something else, say so.

Read-only: no builds, no probe runs, no edits, no patches. Prose and tables only.
