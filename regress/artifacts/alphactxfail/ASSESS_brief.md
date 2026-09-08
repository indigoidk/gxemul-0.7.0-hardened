# alphactxfail -- does swpctx ignore memory-access failures, and does it matter?

## 0. READING SCOPE

Read what you need under `GXEMUL-SEC/src/`, in particular `src/cpus/cpu_alpha_palcode.c`,
`src/core/memory.c` (the `load_64bit_word` / `store_64bit_word` helpers) and
`src/cpus/memory_alpha.c`. Please avoid `regress/artifacts/` and `tools/pipeline/ledger.json`.

Tree under review: `GXEMUL-SEC/src/`. Ignore the pristine 2021 `src/` at the project root.

**This is an error-handling review of existing code.** I am not asking for a guest sequence.

## 1. THE FILED CLAIM -- treat it as a claim

> *"`cpu_alpha_palcode.c` swpctx: the context save and load ignore every memory-access failure."*

**Not verified by me.** It came from another seat's reading on a different brief.

**Please do not simply ratify.** You have refuted premises of mine on three briefs tonight, which
is the behaviour I want. **Check the premises, not just the derivations.**

## 2. SETTLED FROM EARLIER PASSES -- inlined so you need not re-derive

These are your own findings from tonight, on the same handler, and I re-verified each myself:

* `swpctx` saves the outgoing context with a run of `store_64bit_word` / `store_32bit_word` calls
  at `cpu->cd.alpha.ctx + 0 .. +56`, then loads the incoming one with `load_64bit_word` calls at
  `cpu->cd.alpha.ctx + 0 ..`.
* the handler writes its result register at what is currently `r[ALPHA_A0]`; that is the separate
  row `alphaswpctxreg`, already designed, and **not** this brief's subject.
* the local `a0` (a `uint64_t` copied at function entry) is what supplies the new context, so the
  load-new-context step is unaffected by the result-register question.

## 3. QUESTIONS -- VERDICT LINE FIRST

**Q1. Do `load_64bit_word` and `store_64bit_word` report failure at all?** Quote their signatures
and bodies. If they return `void`, or return a value the caller could check but the ABI gives no
failure indication, say so -- **that changes this row from "the caller ignores errors" to "there is
nothing to ignore", which is a different defect with a different fix.**

**Q2. What does the underlying `memory_rw` call use for flags here?** Specifically whether these
helpers pass `NO_EXCEPTIONS`, and what that means for a failed translation: does the access
silently do nothing, return zeroes, or raise something?

**Q3. If a save or load DOES fail silently, what is the resulting machine state?** Concretely: a
half-saved outgoing context, or an incoming context partly loaded from zeroes. Say which fields
would be affected and whether the CPU continues executing with them.

**Q4. Is this reachable other than through a guest bug?** A context switch to an unmapped or
unbacked PCB address is presumably a kernel bug in the guest -- so the emulator's job is to behave
architecturally, not to be robust for its own sake. **What does the architecture say should happen?
If you cannot answer that from a manual present in this tree, say so** -- `_scratchpad/` contains
sixteen PDFs and **none of them is an Alpha reference**, so an architectural claim here cannot be
locally verified, and this project has shipped model-sourced citations before and is trying not to
again.

**Q5. Is there an in-tree idiom?** Do other PAL handlers, or other architectures' context-switch
paths, check these helpers' results? **Grep the fork rather than reasoning** -- a sibling that
checks would be strong evidence about what this one owes.

**Q6. Disposition and severity, argued.** Three possibilities I can see, and I want yours:
  * a real defect with an observable consequence -> a round;
  * a fidelity gap with no observable channel -> documented-only;
  * **not a defect at all**, because the helpers cannot fail in a way this handler could act on.

**Q7. Scope.** You ruled earlier that the six Alpha rows are six separate rounds. This row and
`alphaswpctxreg` are in the SAME handler, a few lines apart. **Does that change your ruling for
these two specifically** -- one round or two? Name the ONE fix design and ONE oracle if you say one.
