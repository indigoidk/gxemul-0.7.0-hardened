# armmmuvehicle -- read-only research (agy)

Open with `VERDICT: <one line>`. READ-ONLY: do not build, do not run gxemul, do not write any file except your answer.
Tree under review: C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\src\ only -- ignore any other src\ under C:\DocumentNoSnc\cc\GXEMUL
(pristine 2021 upstream).  Cite file:line for every fact, found by grep -n.

The project needs a debugger-driven ARM test vehicle on the unmodified `-E testarm` machine that runs guest code
with the MMU ENABLED, so later rounds can exercise translation-fault paths.  Answer with facts from the source:

1. Which ARM CPU types can `-E testarm` be given (`-C`), and which of them does this emulator treat as supporting
   Thumb (find the flag/table)?  What is testarm's default CPU?
2. How does this emulator enable the ARM MMU (CP15 c1 bit), where does it read the translation table base (c2) and
   domain access control (c3), and which descriptor formats does the translation walk accept (memory_arm.c)?
3. What is the minimal set of guest instructions / debugger writes to: build a one-entry section-mapped table in
   RAM, set c2/c3, set c1.M, and keep executing at the same virtual address?  Does `put` write physical or virtual
   memory, and does the debugger `step` keep working after the MMU turns on?
4. What does the emulator do on a translation fault for (a) an instruction fetch, (b) a data load -- which
   exception, which FSR/FAR updates, which file:line?
5. Name any place in that path that ends the process (exit(1)) or stops the CPU (running = 0) on guest input.
