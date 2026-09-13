# `mapledmaaddr` PASS 1 — design review BEFORE the edit: disposition and detector

VERDICT LINE FIRST, then the liveness token `PASS1_MAPLE_20260912`.

**ONE QUESTION: is the proposed fix right, and what must its detector pin so that a wrong fix cannot pass it?**

This is a correctness review of an emulator device model.  **Please do not simply ratify** — a recent panel had seven
of nine seats confirm a premise a brief stated wrongly, and an earlier brief on THIS row gave a "settled premise" that
was true of a different device.  **Check the premises, not just the derivations.**  Premises below are stated as
questions where they are checkable.

## THE TREE

`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\src\` (ignore any other `src/` under the project root: pristine 2021 copies).

## THE DEFECT

`src/devices/dev_dreamcast_maple.c`, attached unconditionally by `machine_dreamcast.c:149` (before the `prom_emulation`
early return), registered `DM_DEFAULT` at physical `0x5f6c00`, length `0x100`.  A guest READ of MAPLE_DMAADDR (+0x04)
computes the stored value and then ends the emulator process.  **THE WHOLE ENCLOSING FUNCTION**, every exit path:

```c
DEVICE_ACCESS(dreamcast_maple)
{
	struct dreamcast_maple_data *d = (struct dreamcast_maple_data *) extra;
	uint64_t idata = 0, odata = 0;

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len);

	switch (relative_addr) {

	case 0x04:	/*  MAPLE_DMAADDR  */
		if (writeflag == MEM_WRITE) {
			d->dmaaddr = idata;
		} else {
			fatal("[ dreamcast_maple: TODO: read from dmaaddr ]\n");
			odata = d->dmaaddr;
			exit(1);
		}
		break;

	case 0x10:	/*  MAPLE_RESET2  */
		if (writeflag == MEM_WRITE && idata != 0)
			fatal("[ dreamcast_maple: UNIMPLEMENTED reset2 value 0x%08x ]\n", (int)idata);
		break;

	case 0x14:	/*  MAPLE_ENABLE  */
		if (writeflag == MEM_WRITE)
			d->enable = idata;
		else
			odata = d->enable;
		break;

	case 0x18:	/*  MAPLE_STATE  */
		if (writeflag == MEM_WRITE) {
			switch (idata) {
			case 0:	break;
			case 1:	maple_do_dma_xfer(cpu, d);
				break;
			default:fatal("[ dreamcast_maple: UNIMPLEMENTED state value %i ]\n", (int)idata);
			}
		} else {
			/*  Always return 0 to indicate DMA xfer complete.  */
			odata = 0;
		}
		break;

	case 0x80:	/*  MAPLE_SPEED  */  /* write stores d->timeout = (idata >> 16) & 0xffff; read returns d->timeout << 16 */
		...
	case 0x8c:	/*  MAPLE_RESET  */  /* write: fatal() on a value not in {0x6155404f, 0x61557f00}; then d->enable = 0 */
		...
	case 0xe8:	/*  UNKNOWN_0xe8  */ /* write: fatal() unless idata == 1 */
		...
	default:  /* fatal("UNIMPLEMENTED read from/write to addr ...") for either direction -- no exit */
	}

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}
```

`maple_do_dma_xfer()` (the ONLY other writer of `d->dmaaddr` besides the write arm and zero-initialisation) walks the
descriptor list and, at its tail, `d->dmaaddr = addr;` — the address past the last descriptor (a `// TODO: Should the DMA
address be updated?` sits above it) — then raises SYSASIC_EVENT_MAPLE_DMADONE.

## THE PROPOSED FIX — ACCEPT (option-set member 4)

Delete `fatal(...)` and `exit(1)`; keep `odata = d->dmaaddr;`.  **The sibling `MAPLE_ENABLE` read arm is quiet**
(`odata = d->enable;`), which makes DMAADDR's kill this switch's outlier.  No latch: the read is implemented.
Recorded consequence, from an earlier review: the edit does NOT change the cursor computation, but it DOES change its
OBSERVABILITY — a read that used to stop the process now returns the field, including a post-DMA cursor.

## PREMISES — as questions

1. Is the value real hardware returns from a MAPLE_DMAADDR read the programmed address, the post-transfer cursor, or
   something else?  *No local Dreamcast/Holly documentation exists in `_scratchpad/` (check `ls _scratchpad/*.pdf`).*  If
   it cannot be settled, does ACCEPT (return the model's field) still dominate the alternatives?
2. Is there any caller or path for which `writeflag` is neither MEM_WRITE nor MEM_READ?  The `else` covers it: before, it
   terminated; after, it assigns `odata` and returns 1 WITHOUT the common-tail write.
3. Is the DMA-cursor question (`d->dmaaddr = addr` at the transfer tail) a SEPARATE row, as an earlier review ruled, or
   must this round decide it?

## THE DETECTOR, as an earlier design review specified it (`regress/artifacts/mapledmaaddr/codex_detector_*.txt`)

Rung-3 guest loads/stores on unmodified `-E dreamcast` (a witness is being built now by the measuring seat):
* several distinct values written and read back EXACTLY — nonzero HIGH bits and nonzero LOW FIVE bits (catches a
  constant, a zero, alignment masking);
* a second write REPLACES what the read reports (catches a snapshot that never updates);
* the process survives past the read (a marker instruction runs) and the `TODO: read from dmaaddr` text is ABSENT
  (catches "keep fatal(), delete only exit(1)");
* after an INDEPENDENTLY demonstrated transfer (a supported command whose response lands in a pre-filled receive buffer —
  NOT `MAPLE_STATE == 0`, which reads 0 always), the read equals the field.

## QUESTIONS

1. **Is ACCEPT right?**  Consider the full option set: DELETE, DECLINE, DECLINE+LATCHED ANNOUNCE, ACCEPT, FAULT (is it
   even available on an SH4 machine? `memory_rw.c` delivers a failed device access as an exception for MIPS and M88K),
   BACKED ACCEPT, IMPLEMENT.
2. **Which wrong fix passes the detector above?**  Name the exact edit.  Is the DMA leg necessary for the floor, or is it
   coverage of the separate cursor row?  What does clause (d) enumerate for a PURE DELETION whose guarded body is
   `odata = d->dmaaddr;` — the dominating predicates are `relative_addr == 0x04` and `writeflag != MEM_WRITE`?
3. **Which premise above is false?**


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
