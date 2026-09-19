# Research job A -- `alphaifetchkill`: what should a failed Alpha instruction-fetch translation do?

    VERDICT: <option letter> -- <one line naming the deciding fact>

Put the verdict line first.  The tree is `GXEMUL-SEC/` at HEAD `cdbe7d7`; ignore any other `src/` under the project
root (pristine 2021 upstream).  **Read ONLY these files:**

    GXEMUL-SEC/src/cpus/cpu_dyntrans.c       the PC-to-pointers slow path (lines ~600-800) and the run loop
    GXEMUL-SEC/src/cpus/memory_alpha.c       alpha_translate_v2p() and its not_found path
    GXEMUL-SEC/src/cpus/cpu_alpha.c          the Alpha CPU run/exception entry points, if any
    GXEMUL-SEC/src/cpus/cpu_alpha_palcode.c  how a halt or a PAL entry is modelled
    GXEMUL-SEC/src/cpus/cpu_mips.c           ONLY as a comparison: how MIPS raises a TLB miss on instruction fetch

**The observed defect (read cpu_dyntrans.c ~670-734 to confirm):** a failed instruction-fetch translation is assumed to
have raised an exception and moved the PC; the code re-looks-up `cpu->pc`, retries translate_v2p, and on a second
failure prints "FATAL: could not find physical address of the exception handler?" and calls `exit(1)`.  Alpha's
translator returns 0 without moving the PC, so on Alpha that path ENDS THE EMULATOR PROCESS.

**Candidate dispositions -- for each, trace what happens next (cite file:line), whether the process survives, what
the guest observes, and whether it is a FIX or a FEATURE (implementing Alpha memory-management faults is a feature
and out of scope):**

    (a)  replace the exit(1) with halting that CPU only: `cpu->running = 0' plus a latched message
    (b)  on the retry failure, return without a translation and let the run loop try again (loop forever?)
    (c)  keep exit(1) for non-Alpha, add an Alpha-specific branch that halts the CPU
    (d)  deliver an Alpha fault (ITB miss) through PALcode -- say whether the tree has ANY machinery for this
    (e)  anything else the code suggests

Then: (1) does the same path end the process on any OTHER architecture whose translator can return 0 without moving
the PC?  Name them from the code, not from memory.  (2) What does `cpu->running = 0` do to the emulator as a whole when
it is the only CPU -- clean shutdown, debugger prompt, or something else?  Cite where.
If you found anything else, say so briefly.
