# ADJUDICATION PASS (F2) -- `lcaisalane`: which disposition for the LCA sparse-I/O lane guard?  Liveness token `LCAISALANE_F2_20260913`.

VERDICT LINE FIRST: one of `A` (decline all five), `B` (accept all five by folding), `C` (decline only the three cells
that end the process today; leave the rest as they are), or `OTHER: <one sentence>` -- then the token.

This is a routine correctness review of an open-source hardware emulator (GXemul, a hardened fork). Please check the
premises, not only the reasoning, and say what you could not check.  **Ratification is not wanted**: the first ruling
on this row was written on six of nine seats and REVERSED when the last two arrived, so the dispute below is live.
Tree under review: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` ONLY -- ignore any other `src/` you find.  Packet-fed
seats: every fact you need is inlined; do not plan to read files, and name any premise you cannot settle from here.

## THE FUNCTION (src/devices/dev_lca.c, HEAD, the whole handler -- every exit path)

```c
DEVICE_ACCESS(lca_isa)
{
	unsigned int ofs, i;
	uint8_t byte;

	relative_addr >>= 5;

	ofs = relative_addr & 3;
	if (ofs > len) {
		fatal("[ ofs=%i len=%i in lca_isa access function. "
		    "aborting ]\n", ofs, len);
		exit(1);
	}

	if (writeflag == MEM_WRITE) {
		byte = data[ofs % len];
		return cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +
		    relative_addr, &byte, 1, writeflag, CACHE_NONE);
	}

	cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE + relative_addr,
	    &byte, 1, MEM_READ, CACHE_NONE);

	for (i=0; i<len; i++)
		data[i] = i == ofs? byte : 0x00;

	return 1;
}
```

`relative_addr >> 5` is the ISA port number P (this one shift is the Alpha 21066 sparse-space remap, verified against
the HRM by five seats); `ofs = P & 3` is the byte LANE.  On a real 21066 the only accesses are LDL/STL/LDQ/STQ
(`len` 4 or 8), so `ofs <= 3 < len` and the guard can never fire: the byte sits in lane `ofs` of the longword,
which is exactly what `data[ofs]` implements.  **The emulator's Alpha CPU does not gate the byte/word instructions
(BWX: `ldbu` 0x0a, `ldwu` 0x0c, `stw` 0x0d, `stb` 0x0e -- `ALPHA_FEATURE_BWX` is defined and never read)**, so a
guest can issue `len` 1 and 2 accesses here, and `memory_rw`'s 1 KB split hands it `len` 3, 5, 6, 7 heads/tails.

## SETTLED PREMISES (each settled on pass 1 by opening the file named; re-stated because the questions depend on them)

* S1. `fatal()` does not exit and cannot be silenced by `-q` (`src/core/debugmsg.c`); the `exit(1)` is the only kill.
* S2. A handler `return 0` on Alpha leaves a LOAD's destination register UNCHANGED and execution continuing
  (`cpu_alpha_instr_loadstore.c`, `LS_GENERIC_N`: `if (!cpu->memory_rw(...)) return;` before the register write;
  `memory_rw.c` raises an exception only under `MEM_MIPS` / `MEM_M88K`).  For a STORE a `return 0` is unobservable
  to the guest.  So member 5 (FAULT) is UNAVAILABLE on Alpha.
* S3. The pty witness `regress/lca_isalane_probe.py` (`-E alpha -e alphabook1`, rung 3) on HEAD, measured:
  ```
  live         0x55 == 0x55   8042 self-test reply through lca_isa at ofs 0            ok
  ofs1 zero    0x0  != 0x60   byte read of ISA 0x3fd (UART LSR), lane 1                FAIL   <- false success
  ofs1 answer  completed      the handler returned 1: the guest was ANSWERED zero        ok     (wants `completed`)
  ofs1 wide    0x60           the SAME address at len 4 packs the LSR byte in lane 1     ok
  ofs2 exit    dead != alive  byte read of ISA 0x3fe (MSR), lane 2 -- process ENDED      FAIL
  ofs3 exit    dead != alive  byte read of ISA 0x3ff (scratch), lane 3 -- process ENDED  FAIL
  LCAISALANE_RESULT=13/16
  ```
  Every 8250 driver polls LSR, so the byte-width path matters to any guest that uses BWX on this machine.
  The witness's `ofs1 answer` row encodes the ACCEPT contract (it wants `completed`); under a decline it stays red.
  Its sentinel `0x0bad1dea` has bits 5-6 set, so `ofs1 zero` masked to 0x60 cannot tell the sentinel from the LSR.
* S4. Nothing boots on `alphabook1`, so NO guest-driver measurement can discriminate the dispositions: whichever is
  chosen is an emulator policy for an access the 21066 never makes.

## THE CELL TABLE (len x ofs), TODAY

```
            ofs 0         ofs 1               ofs 2               ofs 3
  len 1     serve         READ: zero, ok      EXIT                EXIT
                          WRITE: lands data[0]
  len 2     serve         serve (data[1])     READ: zero, ok      EXIT
                                              WRITE: lands data[0]
  len 3     serve         serve               serve               READ: zero, ok / WRITE: lands data[0]
  len 4,8   serve (hardware-legal: data[ofs] is the lane byte)
  len 5..7  serve
```
"zero, ok" = the downstream byte is fetched from the right port and then DISCARDED; the guest gets 0 with success.
"lands data[0]" = `ofs % len` folds the equality cell onto index 0, so a `stb` to a port 1 mod 4 (PIC IMR 0x21/0xa1,
UART IER 0x3f9, RTC data 0x71) or a `stw` to a port 2 mod 4 WORKS TODAY.

## FINDINGS F1..F8 (pass 1, with the main loop's disposition)

* F1 (codex, grok, kimi-k3, minimax, opus5, fable5) -- the EXIT cells (1,2) (1,3) (2,3) are a guest-drivable process
  kill.  ACCEPTED: this is the defect; every option below removes it.
* F2 (codex, opus5) -- the equality READ cells (1,1) (2,2) (3,3) are a false success: right port fetched, 0 returned.
  ACCEPTED as a defect.
* F3 (grok, kimi-k3, minimax, fable5) -- the equality WRITE cells land today via `data[ofs % len]`.  ACCEPTED, and it is
  what reversed the first ruling: a decline there REGRESSES stores that work now.
* F4 (opus5, fable5) -- `len` reaches 3, 5, 6, 7 through the split; (3,3) is a third equality cell.  ACCEPTED.
* F5 (opus5, codex) -- the read arm ignores the nested `memory_rw` result and `byte` is uninitialised on its failure.
  REFINED DOWN on 2026-09-11 by a reading seat that walked every failing path: none delivers the uninitialised byte to
  a guest (device matches `memset` first; the one non-zeroing return fires only after `cpu->running = 0`).  Robustness,
  not a leak.
* F6 (codex, opus5) -- both nested `memory_rw` calls omit `PHYSICAL`.  FILED separately (`lcaisaphys`); not this round.
* F7 (opus5) -- the size field a<4:3> is discarded and the quadword row mis-routes by three ports.  FILED (`lcaisasize`,
  `lcaisaqword`); not this round.
* F8 (reading seat, 2026-09-11) -- cell (2,1) is NOT an equality cell, is served today, and forwards `data[1]`, the
  HIGH byte of the guest's word, to port P.  Under the lane idiom (the byte for lane `ofs` is `data[ofs]`, correct for
  len 4) that is consistent; under a "the addressed byte is the low byte of a narrow access" reading it is the wrong
  byte.  NOT YET DISPOSED -- no side of the dispute addressed it.

## THE DISPUTE (D1), both sides in their own words

* **A -- DECLINE ALL FIVE** (codex, grok, opus5; the first ruling): `ofs >= len` -> latched `fatal(... (once))`, `return 0`
  on both directions (register unchanged), per-instance latch bit.  Warrant: the ADDITION LICENCE -- *"a newly chosen
  emulation contract"* (codex) for BWX-width accesses to a sparse window the 21066 HRM does not define; member 3 changes
  nothing about any hardware-legal access.  Cost, admitted on the record: it STOPS the equality writes that land today.
* **B -- ACCEPT ALL FIVE BY FOLDING** (fable5, minimax, glm, kimi-k3): delete the guard; `ofs = (relative_addr & 3) % len`
  on BOTH arms (the read packs `data[ofs % len] = byte`).  fable5, verbatim: *"the write arm ALREADY SERVES them TODAY --
  `byte = data[ofs % len]` has exactly one live effect, folding `ofs == len` onto index 0 ... upstream wrote it
  precisely to accept the equality cell on writes"*; and *"There is no principled line between (1,1) and (1,2): if the
  lane folds onto the buffer at equality it folds beyond it too.  So the choice is ACCEPT-all-five or DECLINE-all-five,
  and DECLINE-all-five regresses two guest-visible write cells."*  Warrant: the write arm's own idiom (a transferred,
  in-function warrant).  The first ruling's objection: at (2,3) the port's byte lands in the HIGH half of the word.
* **C -- NEW, from the main loop, and it is the one to attack hardest because it is mine**: remove ONLY the kill.
  Decline the three cells that exit today (`ofs > len`, latched announce, `return 0`), leave the equality cells exactly
  as they behave now (writes land; reads still false-zero -- F2 stays open as its own row), and change nothing that a
  guest can observe working today.  Its case: the smallest edit that closes the HIGH defect with no regression, and it
  defers the A-vs-B contract to a row that can carry it.  Its weakness, stated: it is exactly the "line with no
  principle" fable5 describes -- (1,1) writes land while (1,2) writes are refused -- and it leaves a known false
  success (F2) shipped.

## QUESTIONS

1. **Adjudicate D1: A, B, C or OTHER**, with the warrant you rely on.  If you supported A or B on pass 1, be HARDER on
   your own side than on the other: which of your side's claims is weakest?  In particular: does B's "transferred
   warrant" survive the fact that the write arm's fold may be an accident of `% len` rather than a design, and does A's
   addition-licence argument survive the fact that A REMOVES a behaviour that works today?
2. **Adjudicate F1..F8: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE**, one line each.  F8 needs a disposition under
   whichever option you pick: is (2,1)'s `data[1]` right, wrong, or undefined?
3. **Which of the main loop's dispositions above is wrong?**  I have accepted six findings, refined one and left one
   open; say which acceptance you would overturn.
4. **What did all nine of us miss?**  In particular: is there a guest-visible observable -- anything at all on this
   machine -- that would DISCRIMINATE A from B from C, so the choice could rest on a measurement instead of an argument?


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
