# `fbctrlportkill` -- the two-step host kill where the FIRST step looks handled

Nonce: `CODEX_FBCTRL_20260910`. Open with `VERDICT:` naming the disposition and the exact edit, then echo
the nonce.

Ordinary robustness maintenance on a test-framebuffer device in an emulator written in C99. **The tree is
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`**; three unrelated 2021-vintage copies sit elsewhere under the
project root. **Verdict line first.**

**Please do not simply ratify.** Four briefs of mine this week had premises refuted by a seat that opened
the file, and every refutation improved the round. **Check the premises, not just the derivations.**

## THE DEFECT

`src/devices/dev_fbctrl.c`. Two arms of one `switch`, and the interesting part is their ORDER:

```c
case DEV_FBCTRL_PORT:
        ...
        d->current_port = idata;                       /*  STORED FIRST  */
        if (idata >= DEV_FBCTRL_NPORTS)
                fatal("[ WARNING: fbctrl port number is out of range! ]\n");   /*  warned SECOND  */
        break;

case DEV_FBCTRL_DATA:
        if (d->current_port < 0 || d->current_port >= DEV_FBCTRL_NPORTS) {
                fatal("[ fbctrl port number is out of range! ]\n");
                exit(1);
        }
        ...
```

**The port arm STORES an out-of-range selector and warns about it afterwards. It does not reject it.**
The data arm then ends the emulator on that same stored value. A reader auditing the port arm sees a range
check and a diagnostic and concludes the case is handled; the check does nothing but print.

**AND THE TWO GUARDS TEST DIFFERENT QUANTITIES.** The port arm tests `idata`, a `uint64_t`; the data arm
tests `d->current_port`, an `int` (verified in the struct). The store between them TRUNCATES. So writing
`0xffffffff` warns and lands `current_port == -1`, killing through the `< 0` half; writing `0x100000000`
warns and truncates to a perfectly valid `0`, so the warning fires about a value that turns out fine.
**The warning does not mark the killing set.**

`DEV_FBCTRL_NPORTS` is 8 and `machine_test.c` attaches the device at two sites, so it is on the `testmips`
and `testarm` machines -- the ones this project's own gates drive.

## THE QUESTIONS

1. **PREMISES AS QUESTIONS.** Are the arms really in that order? Is `current_port` really a signed `int`,
   making the `< 0` half live rather than dead code? Is the device really attached on machines the gates
   drive? **If the `< 0` half is unreachable, say so with the warrant -- a dead path recorded with its
   reason is a result, not an absence.**
2. **THE ORDER QUESTION, which is the round's real content.** I believe **refusing the store in the PORT
   arm closes the DATA kill without touching the DATA arm at all** -- one line moved, and it makes the
   DATA guard the belt-and-braces it already reads as. Do you agree? What does a guest see if its port
   write is refused: does anything read `current_port` back, and would leaving the PREVIOUS port selected
   be better or worse than leaving an invalid one selected?
3. **WHICH OPTION-SET MEMBER**, from {delete, silent decline, decline + latched announce, accept, fault,
   backed accept, implement}? Note the existing warning is UNLATCHED and per-access, so a guest looping on
   the port register floods the log -- if you keep an announce it needs the house latch idiom. **And check
   the member is AVAILABLE**: a bus fault needs the memory layer to deliver one, which this tree does for
   two CPU families only, and this device sits on both a MIPS and an ARM test machine, so the answer may
   differ per machine.
4. **THERE ARE MORE KILLS IN THIS FILE and I want them separated, not swept in.** `fbctrl_command()` has
   a `default:` that dies on an unimplemented command, and `DEVICE_ACCESS(fbctrl)` has its own `default:`
   that dies on an unimplemented offset. Which belong to THIS round and which are separate? A round takes
   one site unless a second is the same semantic class under one fix design with one detector.
5. **THE DETECTOR.** The vacuity floor needs failure on the pre-fix build, on a verbatim reinstatement of
   the removed kill, on a null medium, AND on a NULLED REPAIR. Name the rows, and per row **the mutant it
   kills and the observable that differs under it.**
   **Two traps to route around, both of which have cost this project a round recently:** *"the host
   survived"* is not a channel at a refusal site, because guarded and unguarded code both survive once the
   kill is gone; and a row that asserts only *"the access ran to completion"* is SURVIVE-ONLY and cannot
   tell two arms apart when both complete. **A row must observe something that differs between the arms**
   -- here, presumably what `current_port` becomes and whether a subsequent DATA access reaches the port
   the guest intended.
6. **IS THERE A VALUE WHERE THE INTENDED BEHAVIOUR IS AMBIGUOUS?** `current_port` is signed and the guest
   supplies 64 bits. Say what the model should do with a negative, a huge, and a truncating value, and
   whether the three want the same answer.
7. If you found something else, say so.

Read-only: no builds, no probe runs, no edits, no patches. Prose and tables only.
