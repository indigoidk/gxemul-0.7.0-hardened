# **FIND THE NEXT CRITICAL BUG.**  Guest-reachable host deaths this queue has NOT yet named.

## VERDICT LINE FIRST.  TREE: `GXEMUL-SEC/src/` -- three pristine-2021 `src/` copies sit under the
## PROJECT root and are NOT this fork; line numbers off by hundreds mean you read one.
## **DO NOT RATIFY THE QUEUE.**  §S3 is the point: what has everyone MISSED?

## S1 -- THE STANDING SHAPE OF THIS DEFECT CLASS (settled; do not re-derive)

`fatal()` **prints and returns** -- `debugmsg.c`, no early-out, cannot be silenced by `-q`.  The
`exit(1)` beside it is the kill.  A guest store or load that reaches such a site **ends the
emulator process**.

Recent members, all found this way and all real:
* `armmsrmodekill` -- ONE privileged `MSR CPSR_c,#0x14` from the boot mode ends the process.
  **Gate 14's 358 real-decode checks never feed that encoding.**
* `lcaconfbus1kill`, `pcc2c040kill`, `gdromexitsix`, `sgireunmapped`, `sh4chcr` -- same family.

**THE DISPOSITION MENU HAS SEVEN MEMBERS** and choosing before checking availability is a recorded
error: 1 DELETE, 2 DECLINE silent, 3 DECLINE + LATCHED ANNOUNCE, 4 ACCEPT, 5 FAULT, 6 BACKED
ACCEPT, 7 IMPLEMENT.  **Member 5 FAULT is NOT available on Alpha** -- `memory_rw.c` dispatches an
exception on a failed DEVICE access for MIPS and M88K only.

## S2 -- WHAT I WANT

**A ranked shortlist of guest-reachable host deaths that are NOT already in the queue.**  Search
`GXEMUL-SEC/src/devices/*.c` and `GXEMUL-SEC/src/cpus/*.c`.

The queue already holds (do not re-report these): `armmsrmodekill`, `armthumbabortkill`,
`cpusexitsweep`, `lcaconfbus1kill`, `pcc2c040kill`, `gdromexitsix`, `sgireunmapped`, `sh4chcr`,
`sh4dmacie`, `gdromdmadefault`, `lcashiftub`, `lcaconfwidth`, `alphapfnoffset`,
`alphaswpctxptbr`, `diskimagesign`, `wdc*`, `crimewidthkill`, `sgimtedepth4dead`,
`mapledmaaddr`, `pcc2widthkills`.  **Check `GXEMUL-SEC/OUTSTANDING_BUGS.md` and
`tools/pipeline/ledger.json` before claiming anything is new.**

For each candidate, give me:
1. **file:line and the exact code**;
2. **GUEST REACHABILITY** -- what instruction, from what mode/state, reaches it.  *** THIS IS THE
   PART THAT MATTERS AND THE PART THIS PROJECT MOST OFTEN GETS WRONG. ***  A site reachable only
   from emulator setup code is a different, lesser defect.  **Trace instruction -> value -> the
   guard, and say CONFIRMED or BELIEVED.**
3. **which of the seven members fits, and whether that member is AVAILABLE on that CPU**;
4. **is it fed by any existing gate?**  A site no gate reaches is ranked higher -- gate blind-spots
   order this queue.
5. **severity**, and why.

## S3 -- *** THE QUESTION THAT IS ACTUALLY WORTH YOUR TIME ***

This project has swept `exit(` several times.  **So do not just re-run that sweep.**

> **What guest-reachable HOST DEATH or GUEST-STATE CORRUPTION does this codebase have that an
> `exit(` grep CANNOT find?**

Candidates I can think of and cannot evaluate -- attack these and add your own:
* `cpu->running = 0` halts that strand the guest (the `armthumbabortkill` shape) in devices or
  other CPUs;
* `abort()`, `assert()`, a NULL deref reachable from a guest store, an unchecked `malloc`;
* an out-of-bounds array index computed from a guest-supplied offset **that does not kill the host
  but silently corrupts a neighbouring field** -- this project has one of those already
  (`asicindexcase`), so the class is proven live;
* an unchecked `memory_rw` return, where a failed access is treated as a success.

**A grep finds a KEYWORD.  Name the ones that need a READING.**

## S4 -- HONESTY CLAUSE

**If the honest answer is "the `exit(` family is well swept and the remaining members are already
queued", say that.**  An empty result WITH ITS DENOMINATOR (what you searched, how) is a real
answer and closes a question.  A manufactured finding costs a round.

And if you find something that is NOT in the classes above -- say so anyway.  The standing licence
in this project is that a seat which finds something else while verifying a claim reports it.
