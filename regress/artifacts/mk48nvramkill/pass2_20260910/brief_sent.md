# `#521` mk48nvramkill -- PASS 2 on the real diff

Nonce: `PASS2_MK48_20260910`. Open with `VERDICT:` (RATIFY / NOT-RATIFY / BREACH-FOUND), then echo the
nonce.

Ordinary correctness review of a device model in an emulator written in C99. **The tree is
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`**; three unrelated 2021-vintage copies sit elsewhere under
the project root. If you cannot open files, answer from this packet alone and SAY SO -- the packet is
self-contained and names any premise you cannot settle from it.

**Please do not simply ratify.** Three briefs of mine this week had premises refuted by a seat that opened
a file, and each refutation improved the round. **Check the premises, not just the derivations.**

## THE DEFECT (witnessed at rung 3 BEFORE the edit)

`dev_mk48txx.c` registers the MK48T08 for `MK48TXX_LEN` = `MK48T08_CLKSZ` = **8192** bytes. An accept
block passed everything OUTSIDE `[MK48T08_CLKOFF, MK48T08_CLKOFF + MK48TXX_ISEC)` to the RAM path via
`goto ret`. With `CLKOFF` = `0x1ff0` and `ISEC` = `9` the switch was reached for `0x1ff0..0x1ff8`, and it
holds exactly ONE case, `CLKOFF + MK48TXX_ICSR` = `0x1ff8`. **The other eight offsets fell to `default:`
and called `exit(1)`.** `machine_mvme88k.c` attaches the device unconditionally in its MVME187 arm.

**MEASURED, not argued:** a rung-3 witness on unmodified `-E mvme88k -e mvme187` scored **15/47** on the
committed build, all 15 controls green and all 32 kill rows red. **The killing population is SIXTEEN
cells** (eight offsets x read and write), and **the kill is WIDTH-INDEPENDENT** -- `len` never enters the
guard, so `ld`, `ld.h` and `ld.bu` all die at the same start offset.

**Those eight are ORDINARY NVRAM on this part**, which is what licenses accepting them. `mk48txxreg.h`
says the first bank of eight registers at `(nvramsz - 16)` -- exactly `0x1ff0` -- is *"available only on
more recent MK48Txx models"*, naming them IFLAGS, IASEC, IAMIN, IAHOUR, IADAY, IINTR, IWDOG. They are the
MK48T59's alarm and watchdog bank; this file implements the MK48T08 alone. Storage already existed
(`reg` is `MK48TXX_LEN` bytes).

## THE DIFF, verbatim and complete (1 hunk(s), 31 changed lines)

```diff
diff --git a/src/devices/dev_mk48txx.c b/src/devices/dev_mk48txx.c
index 5ef0f8c..16174d7 100644
--- a/src/devices/dev_mk48txx.c
+++ b/src/devices/dev_mk48txx.c
@@ -84,7 +84,36 @@ DEVICE_ACCESS(mk48txx)
 	if (writeflag == MEM_READ)
 		odata = d->reg[relative_addr];
 
-	if (relative_addr < MK48T08_CLKOFF ||
+	/*  #521 (mk48nvramkill): the lower bound was MK48T08_CLKOFF, i.e. 0x1ff0,
+	    and it was missing its `+ MK48TXX_ICSR'.  The switch below holds exactly
+	    ONE case, MK48T08_CLKOFF + MK48TXX_ICSR (0x1ff8), so the eight offsets
+	    0x1ff0..0x1ff7 fell through it to a `default:' that calls exit(1) --
+	    EIGHT bytes inside the device's own 8192-byte registration ending the
+	    emulator process on an ordinary access.  MEASURED at rung 3 BEFORE this
+	    edit, on unmodified `-E mvme88k -e mvme187':
+	        artifacts/mk48nvramkill/opus_mk48_nvram_witness_20260910.py
+	        artifacts/mk48nvramkill/opus_witness_run_20260910.txt  -- 15/47,
+	            all 15 controls green and all 32 kill rows red.
+	    THE POPULATION IS SIXTEEN CELLS, NOT EIGHT: every offset kills in BOTH
+	    directions, ld.bu and st.b alike, and all sixteen were driven.  The kill
+	    is WIDTH-INDEPENDENT -- `len' never enters the guard, so ld / ld.h /
+	    ld.bu all die at the same start offset and there is no width axis here.
+
+	    THOSE EIGHT ARE ORDINARY NVRAM ON THIS PART, which is what licenses
+	    accepting them rather than declining.  mk48txxreg.h says the first bank
+	    of eight registers at (nvramsz - 16) -- exactly 0x1ff0 -- is "available
+	    only on more recent MK48Txx models", and names them IFLAGS, IASEC,
+	    IAMIN, IAHOUR, IADAY, IINTR, IWDOG.  They are the MK48T59's alarm and
+	    watchdog bank; this file implements the MK48T08 alone, where the region
+	    is plain non-volatile RAM.  Storage already existed -- `reg' is
+	    MK48TXX_LEN bytes -- so this is a BOUNDARY CORRECTION, not new policy,
+	    and no vendored constant is wrong.
+
+	    The upper bound stays at MK48TXX_ISEC deliberately: it routes the
+	    time-of-day registers to this same path, which is correct because
+	    mk48txx_update_regs() writes into this very array, and moving it would
+	    be a different change.  */
+	if (relative_addr < MK48T08_CLKOFF + MK48TXX_ICSR ||
 	    relative_addr >= MK48T08_CLKOFF + MK48TXX_ISEC) {
 		/*  Reads and writes to the RAM part of the mk48txx, or
 		    the clock registers, are OK:  */
```

## THE DETECTOR AND ITS KILL TABLE

Shipped detector `regress/mk48_nvram_probe.py`, 48 rows. It is the round's witness with ONE row inverted:
the witness asserted 16 offset-named death messages -- green only while the defect LIVES -- and the
detector asserts ZERO instead.

Table 2, `regress/artifacts/mk48nvramkill/killtable_20260910/t2/SCORES.txt`, scratch clone, one frozen
instrument for every leg, restore verified on both parts:

```
=== SUMMARY ===
BASE      MK48_RESULT=48/48      
M_OLD     MK48_RESULT=15/48      rd 1ff0,rd 1ff0,rd 1ff1,rd 1ff1,rd 1ff2,rd 1ff2,rd 1ff3,rd 1ff3,rd 1ff4,rd 1ff4,rd 1ff5,rd 1ff5,rd 1ff6,rd 1ff6,rd 1ff7,rd 1ff7,wr 1ff0,wr 1ff0,wr 1ff1,wr 1ff1,wr 1ff2,wr 1ff2,wr 1ff3,wr 1ff3,wr 1ff4,wr 1ff4,wr 1ff5,wr 1ff5,wr 1ff6,wr 1ff6,wr 1ff7,wr 1ff7,msg silent
M_HALF    MK48_RESULT=31/48      rd 1ff4,rd 1ff4,rd 1ff5,rd 1ff5,rd 1ff6,rd 1ff6,rd 1ff7,rd 1ff7,wr 1ff4,wr 1ff4,wr 1ff5,wr 1ff5,wr 1ff6,wr 1ff6,wr 1ff7,wr 1ff7,msg silent
M_ICSR    MK48_RESULT=47/48      csr rise
M_NULL    MK48_RESULT=22/48      live absent,nvram0 absent,devsig yr,devsig mon,devsig mday,devsig wday,ok rd,ok rd,csr rise,rd 1ff0,rd 1ff0,rd 1ff1,rd 1ff1,rd 1ff2,rd 1ff2,rd 1ff3,rd 1ff3,rd 1ff4,rd 1ff4,rd 1ff5,rd 1ff5,rd 1ff6,rd 1ff6,rd 1ff7,rd 1ff7,msg silent
HEAD      MK48_RESULT=15/48      rd 1ff0,rd 1ff0,rd 1ff1,rd 1ff1,rd 1ff2,rd 1ff2,rd 1ff3,rd 1ff3,rd 1ff4,rd 1ff4,rd 1ff5,rd 1ff5,rd 1ff6,rd 1ff6,rd 1ff7,rd 1ff7,wr 1ff0,wr 1ff0,wr 1ff1,wr 1ff1,wr 1ff2,wr 1ff2,wr 1ff3,wr 1ff3,wr 1ff4,wr 1ff4,wr 1ff5,wr 1ff5,wr 1ff6,wr 1ff6,wr 1ff7,wr 1ff7,msg silent
RESTORED  MK48_RESULT=48/48      
KILLTABLE_DONE
```

**TABLE 1 FOUND A FLOOR BREACH AND IT WAS REPAIRED IN-ROUND.** `M_ICSR` -- moving the accept block's
UPPER bound to `CLKOFF + ICSR` -- escaped **47/47**. The mutated condition
`addr < 0x1ff8 || addr >= 0x1ff8` is a **tautology**, so the switch is never reached and `0x1ff8` is
served as plain RAM; the control register silently stops working. The rows aimed at that offset could not
see it because they are **survive-only** there: they assert the access ran to completion, which is true on
the RAM path too. The repair is one row, `csr rise`, reading the case's SIDE EFFECT -- writing the READ
bit 0 to 1 calls `mk48txx_update_regs()`, so the row clears the control register, poisons a clock slot,
drives the edge and reads the slot back.

## THE QUESTIONS

1. **IS THE FIX RIGHT?** Is `CLKOFF + MK48TXX_ICSR` the correct lower bound, or should it be something
   else? Does the change swallow, or otherwise disturb, the one case the switch legitimately implements?
2. **IS THE UPPER BOUND STILL RIGHT?** It is deliberately unchanged at `MK48TXX_ISEC`, which routes the
   time-of-day registers to the RAM path. Is that correct, harmless, or a separate defect?
3. **A FLOOR PROBLEM I WANT SCRUTINISED RATHER THAN WAVED THROUGH.** This diff **removes no kill
   statement** -- it makes the existing `default:` arm UNREACHABLE. So floor clause (b), a verbatim
   reinstatement of the removed defect, cannot be satisfied literally: reinstating that arm with the
   corrected boundary is a no-op or dead code and no channel can distinguish it. I substituted `M_OLD`,
   restoring the old dispatch. **Is that substitution legitimate, or is the round claiming a floor it does
   not meet?**
4. **WHAT MUTANT ESCAPES THIS 48-ROW INSTRUMENT?** The table found one breach already and I would rather
   find the second here than after shipping. Name a concrete edit and say which row you predict it
   reddens, or say plainly that you predict none within the enumerated class -- and if so, state the class
   BOUNDARY, i.e. which edits are outside it and are therefore disclosed debt rather than rowed.
5. **IS ANY OF THE 48 ROWS VACUOUS?** A row whose named channel cannot vary under its named mutant is
   vacuous by construction. I already know `ok rd/wr 1ff8` were vacuous against `M_ICSR` and that is what
   the new row repairs. **Is any OTHER row in the same position?**
6. **A SECOND, NON-FATAL DEFECT sits three lines above and is deliberately OUT OF SCOPE**: the accept path
   reads and writes exactly ONE byte whatever `len` says, so a four-byte read of the clock block returns a
   single zero-extended byte. Is leaving it out of this round right, or does routing eight more offsets to
   that path make it this round's business?
7. Anything else.

Read-only: no builds, no probe runs, no edits.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
