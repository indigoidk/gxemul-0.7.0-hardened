You are a researcher for a C hardware emulator project (the GXemul hardened fork).  The tree is
`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`; ignore any other `src/`.  Read-only: change no file and build nothing.

Ledger row `armthumbabortkill` (HIGH, open): "cpu_arm.c: FIVE Thumb sites halt the emulator AFTER the abort is already
delivered and T cleared -- the halt PREVENTS THE GUEST'S ..." (read the row in
`tools\pipeline\ledger.json`, id `armthumbabortkill`, and any `OUTSTANDING_BUGS.md` text naming it).

FIRST LINE: `VERDICT: <what the five sites should do, in one phrase>`.  Then:
1. The five sites, file:line each, the exact statements, and the path by which a guest reaches each (which Thumb
   instructions, which abort).
2. What the ARM architecture requires after a data or prefetch abort taken from Thumb state -- cite
   `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\ddi0100i.txt` or `ddi0406.txt` by line (grep them; do not rely on memory).
3. The option set with the tree's own precedent for each (grep `src\cpus\cpu_arm*.c` for how other abort sites
   continue), and which the architecture supports.
4. The witness: the smallest guest sequence on an unmodified in-tree ARM machine (`-E testarm`, `cats` or `netwinder`)
   that reaches one site (describe it), with its controls; and which existing gate (`regress\gate_arm.sh`) or probe
   already comes closest.
5. Anything in the row's text that the tree contradicts.
Say what you read (file:line) and what you inferred.
