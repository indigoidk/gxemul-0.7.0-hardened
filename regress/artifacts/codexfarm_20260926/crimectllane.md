You are a researcher for a C hardware emulator project (the GXemul hardened fork).  The tree is
`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`; ignore any other `src/`.  Read-only: change no file and build nothing.

Queue row `crimectllane` (being filed with change #529; its text is in
`C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\records\bugs529.md`):
`src\devices\dev_sgi_ip32.c`, `DEVICE_ACCESS(crime)`, `case CRIME_CONTROL:` matches the exact label 0x08 and acts on the
raw value of whatever width reaches it, so a 32-bit write of 0x800 to +0x08 (the HIGH half of the 64-bit register on
this big-endian machine) stops every CPU while the 32-bit write to +0x0c that NetBSD 1.6.2 makes (the arm's own TODO)
does nothing.

FIRST LINE: `VERDICT: <what a correct lane model must decide, in one phrase>`.  Then:
1. From the tree only (`dev_sgi_ip32.c`, `src\include\thirdparty\crimereg.h`, the machine setup in
   `src\machines\machine_sgi.c`, any PROM or OS notes present): every piece of evidence about how CRIME_CONTROL's bits
   map to byte lanes and what 32-bit accesses at +0x08 and +0x0c should do.  Mark what is documentation and what is
   only this emulator's choice.
2. How the 4-byte READ and WRITE paths of the width arm (~lines 260-296) already treat +0x08 versus +0x0c (which half
   each takes), and whether the CONTROL switch arm is consistent with them.
3. Which rows of `regress\artifacts\crimewidthkill\final529r17_20260926\crime_width_probe.r17.py` rely on the current
   behaviour (the `sw08`/`sh08` rows, `acc ctl4r`, `acc ctl0c`, ...), and what each would need if the lane were fixed.
4. The smallest guest witness a fix would need (describe it), and what boot evidence would settle the lane question.
Say what you read (file:line) and what you inferred.
