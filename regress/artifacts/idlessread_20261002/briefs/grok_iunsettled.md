THREE UNSETTLED QUEUE ENTRIES -- the manuals they call unopened or absent are on this machine; read them and settle each

Open with the token `GROK_IUNSETTLED_ALIVE_1002` on its own line and the first line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md` quoted verbatim, then ONE verdict line:
`VERDICT: <s> settled, <u> still unsettled, of 3`.

READ-ONLY.  Write nothing, build nothing, run no emulator.

**Context.**  The id-less review of `OUTSTANDING_BUGS.md` left five entries UNSETTLED.  Three of them say a manual was
not opened, or that there is none in the tree.  The seats read the git tree `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`;
the manuals are OUTSIDE it, as extracted text in `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\`:
`sh4_programming.txt`, `sh7750_hardware.txt`, `ppc_uisa_book1_v201.txt` (Book I), `ppc_vea_book2_v201.txt` (Book II),
`ppc_oea_book3_v201.txt` (Book III), `ppc_pem_32and64_2005.txt`, `ppc_pem32_rev2_2001.txt`.  I have NOT checked
whether they settle anything -- that is the question.  Please do not assume they do: "the manual is silent" is a real
answer, and so is "this manual does not cover AltiVec".

**The three entries** (queue line numbers as the file stands on disk; the source files named are unmodified on disk):

1. `OUTSTANDING_BUGS.md:2947-2948` -- whether the SH-4 `FSCA` store owes the mode-aware rounding store.  The ruling
   said: "The handler stores through ieee_store_float_value.  The manual was not opened."  Source:
   `src/cpus/cpu_sh_instr.c` (search `fsca`).  What does the SH-4 manual say about how FSCA's two results are rounded
   or how exact they are, and does FPSCR.RM apply to them?
2. `OUTSTANDING_BUGS.md:5650-5654` -- the `lvx` / `stvx` effective-address mask rule; the ruling said the PowerPC
   manual was not opened and "the queue itself says the mask rule is uncitable".  Source: `src/cpus/cpu_ppc_instr.c`
   (search `lvx`, `stvx`).  Do any of the five PowerPC texts define these two instructions at all?  If none does, say
   which document would (and that it is not here).
3. `OUTSTANDING_BUGS.md:5655-5661` -- the architectural rule for an unaligned `lwarx`, and whether a `stwcx.` that
   fails part-way must drop the reservation.  The ruling said "there is no PowerPC manual in the tree".  Source:
   `src/cpus/cpu_ppc_instr.c` (search `llsc`, `lwarx`, `stwcx`), `src/cpus/cpu_ppc.c` (`ppc_exception`).

**How to read the manuals** (each of these has cost this project a wrong citation):
* `wc -c` the file first -- a zero-byte extraction reports nothing for everything.
* Quote the manual VERBATIM with `file:line`, the line number taken from `grep -n` (not counted by hand).
* Prefer the prose to an extracted table or figure: `pdftotext -layout` staggers a table's names against its values.
  If you must cite a table row, calibrate it against a row whose answer the source already pins.
* An absence claim is only as good as the span you read: say which lines you read to conclude "it does not say".

**For each entry, ONE line:**
`<n> | SETTLED: <what the manual says, quoted, file:line> / STILL UNSETTLED: <what you read and what it does not say> | THEN: <what the queue entry should become: a closing sentence (give it), or NEW <HIGH|MED|LOW> <id> "<title>" with the source line that is wrong, or what measurement or document would settle it> | <the lines you read: manual and source>`

End with `DENOMINATOR: <a> of 3 entries read in the queue, the source and at least one manual`.
