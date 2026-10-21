# The OpenFirmware-emulation exit family (src/promemul/of.c) -- scoping before its round

**Format:** open with the token `ARGON_OFEXITS_20261021`, then ONE line `VERDICT: ONE ROUND | SEVERAL ROUNDS -- <one line>`, then your
findings.  Every disagreement with a ledger row (L) is a line of its own starting `FLAG:`, citing `<label>:<line>` for both
sides.  Facts and derivations only; agreement is not wanted -- these rows were filed from readings, and the round will
measure whatever you predict.

**This is a reading task on the ATTACHED file `argon_bundle_1.txt` (read it to the end) and this message only.**  It is an
emulator's OpenFirmware PROM emulation; a guest reaches it by executing a magic instruction word that the ARM and PowerPC
decoders route to it (AI, PI).

**The question.**  For EACH `exit(1)` in OF (lines 394, 448, 549, 577, 1100, 1120, 1201):
1. REACH -- which guest instruction sequence, on which machines (only MP sets of_data), reaches it; at what privilege
   level (SWI and sc are executable from user mode); or UNREACHABLE with the reason from the code.
2. THE OPTION-SET MEMBER (R:O1) you would choose, PER ARCHITECTURE where they differ, checking availability (R:O2): in
   particular, for OF:1100 (no of_data), whether the right disposition is to let the magic word execute as the ordinary
   instruction it encodes (AI's SWI exception, PI's system-call exception) on machines without OpenFirmware -- a decoder-
   or X(openfirmware)-level check -- rather than any edit inside of_emul.  Trace the caller's tail for each option
   (R:O6): X(openfirmware) sets the pc from the link register after of_emul returns.
3. WHAT A DETECTOR MUST PIN: the decline/exception rows on a machine without OpenFirmware, and the accept rows on macppc
   that the fix must not break (R:O7).
Then: may these sites share one round under R:O5 (same device, same semantic class, one detector, no new oracle), or how
many rounds; and is ARM's `0xef8c64eb` reboot magic (AI, X(reboot)) the same class or a different row.  If you run short,
finish the sites you started and name the ones you did not reach.
