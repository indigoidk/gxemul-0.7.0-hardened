# PANEL: two uncommitted emulator fixes, `#524` and `#525`, each already NOT RATIFIED once

**VERDICT LINE FIRST**, on its own line, so it survives truncation. Then your reasoning.

Ordinary correctness review of an instruction interpreter and a disk-controller model in an
emulator written in C99. Nothing here is security work.

## YOU MAY NOT NEED TO READ ANY FILE — every fact is inlined below

If you are a packet-fed seat (you cannot open files), **answer from this packet alone and say so**;
that is an honest and useful answer. **If you CAN read files, the tree under review is
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\src\` — three unrelated 2021-vintage copies of `src/` sit
elsewhere under the project root and will give you line numbers off by hundreds.**

**Both changes are UNCOMMITTED — they are in the working tree, not at HEAD.**

## *** PLEASE DO NOT RATIFY. ***

Six times today a review pass has refuted a load-bearing premise of mine, every time correctly.
**Check the premises, not just the derivations.** Both of these diffs have already been through one
adversarial pass and **both came back NOT RATIFIED**; the findings are inlined so you can attack
them too, not just the code. **"Your fix is wrong" and "your correction is wrong" are the most
valuable answers here.**

---

# ROUND `#524` — `armbdt`, ARM block data transfer

## The defect

`arm_pop()` (LDM) and `arm_push()` (STM) in `cpu_arm_instr.c` each hold one running
`uint32_t addr = *np` and branch on host page residency per register:

* **FAST path** (page resident): `p32[(addr & 0xfff) >> 2]` — the `>> 2` truncates the low two
  bits, which is **architecturally correct**: DDI0100I LDM(1) p.A4-37 and STM(1) p.A4-190 both say
  to *ignore the least significant two bits of the address*.
* **SLOW path** (cold page): passed the **RAW, UNMASKED `addr`** to `memory_rw`, whose
  `offset = paddr & offset_mask` is **page-granularity, not word-rounded**, and whose transfer is a
  raw `memcpy`.

**So an unaligned base spliced bytes across an architectural word boundary, and the same instruction
at the same base returned DIFFERENT BYTES according to host page-cache warmth — a condition
invisible to the guest architecture.**

## The fix (both sites)

```c
-   if (!cpu->memory_rw(cpu, cpu->mem, addr, data,
+   if (!cpu->memory_rw(cpu, cpu->mem, addr & 0xfffffffc, data,
        sizeof(data), MEM_READ, CACHE_DATA)) {      /* and MEM_WRITE at the other site */
```

**The mask must NOT move to function entry:** `if (w_bit) *np = addr;` uses the unmasked running
value, and Mode 4 writeback derives from unmasked Rn. In-tree precedent: the code generator emits
`addr &= 0xffc;` — masking the ACCESS while leaving writeback alone.

## Measured (rung 3, cold debugger, unmodified in-tree `testarm`, pty-driven)

| leg | score |
|---|---|
| fix applied | **25/25** |
| committed HEAD, pre-fix | **17/25** |
| mask at ENTRY instead | **20/25 — killed by the writeback rows** |
| one site only (either) | 21/25 |
| null medium | 6/25 |
| restored baseline | 17/25 = HEAD |

**The pre-existing `arm_writeback_probe.py` scores the entry-mask mutant 22/22 — identical to a
correct build.** The probe is structurally blind to it.

## What the first adversarial pass found (NOT RATIFIED)

1. **The masks are locally correct**, and for an aligned base both changes are strict no-ops
   including across 32-bit wraparound.
2. **"Only two sites on the BDT path" was WRONG.** Two *combined-instruction handlers* replace
   LDM/STM outright and never reach the fixed helpers: `netbsd_memset` does
   `memset(page + (addr & 0xfff), 0, 128)` — raw page offset, no rounding, and its guards check page
   bounds and source values but **never reject an unaligned address**; `netbsd_memcpy` copies
   through raw `& 0xfff` offsets **while its register-publication reads use `& 0xffc`** — one
   handler, two address rules. *(Pre-existing; filed separately, not fixed in this round.)*
3. **Thumb callers entering these helpers get the fix automatically** (no Thumb-specific
   raw-address branch), but a **separate** unfixed issue exists: the helper's PC handling clears
   both low PC bits while Thumb POP's spec preserves the halfword address and specifies
   interworking.
4. **The helpers are not restricted to RAM** — an unaligned address can reach device dispatch, and
   rounding can change a device-relative offset near a device boundary.
5. **A2-42 specifies additional UNPREDICTABLE behaviour for ARMv6 unaligned multiword accesses to
   Device or Strongly Ordered memory**, so "all callers simply ignore those bits" is too broad.
6. The edit rounds the **virtual** address before translation, and `memory_rw` splits translated
   accesses at 1 KB — **"the old call can touch, and fault on, a page the corrected call never
   accesses."**

---

# ROUND `#525` — `wdcaltdigin`, the WDC alt-status handler

## The defect

`DEVICE_ACCESS(wdc_altstatus)` computes `odata = status_byte(d, cpu)` **unconditionally**, then:

```c
	if (writeflag==MEM_READ)
		debug("[ wdc: read from ALTSTATUS ... ]", (int)odata);
	else if (relative_addr != 0) { /* #494: decline the WRITE */ }
	else { /* Alt Ctrl write, #481 */ }
	...
	if (writeflag == MEM_READ)
		data[0] = odata;
	return 1;
```

**`relative_addr` was tested in exactly ONE place — inside the `else` of `writeflag == MEM_READ`.
So the READ path never decoded its offset, and a read of offset 1 (the Drive Address register,
`0x3f7` on the PC layout) returned the ALT-STATUS byte.** The region is registered two bytes wide.

**This is the symmetric cell of `#494`, which closed the WRITE half of the same `if` and left this
one open.** {READ, WRITE} × {offset 0, offset 1} — three cells were closed.

## The fix

```c
	if (writeflag==MEM_READ) {
		if (relative_addr != 0) {
			odata = 0;          /* declined; the common tail writes it out */
		} else
			debug("[ wdc: read from ALTSTATUS ... ]", (int)odata);
	} else if (relative_addr != 0) {
```

Registration deliberately NOT narrowed (owner ruling: decode the read).

## Measured (rung 3, unmodified in-tree machine)

HEAD **14/16** (both offset-1 read rows return the status byte — `0x51` at power-on, `0x58` armed);
fix **16/16**. The status byte S is **nonzero**, which is what makes the clause-(d) mutant
non-vacuous: that mutant keeps the offset guard and deletes `odata = 0`, so if S were 0 the fixed
and broken builds would return the identical byte.

## What the first adversarial pass found (NOT RATIFIED)

1. All four cells verified; the unbraced `else` binds to the inner `if`; braces 6/6.
2. **`status_byte()` has no device-state mutation**, and the `INTERRUPT_DEASSERT` / `int_assert = 0`
   acknowledgement lives in the *main* register handler and is **absent** from this one — so a
   declined read acknowledges nothing. *(Its complete call chain was not verified.)*
3. **The comment overclaimed twice** and both were narrowed: "matches no hardware on any layout"
   (the evidence does not support a universal claim), and "a correct guest reads here expecting a
   floppy effect" (ditto).
4. A refinement: **`DEV_FDC_LENGTH` is 6, so the floppy controller does NOT register `0x3f7`
   today** — the documented collision is **prospective**, not live.
5. **Detector coverage and a selector audit remain unverified.**

---

# THE QUESTIONS — answer as many as you can judge

1. **Is either fix WRONG?** Not incomplete — wrong. Say so plainly with the mechanism.
2. **`#524`: is `addr & 0xfffffffc` the right form**, and is masking the VIRTUAL address before
   translation the right place, given finding 6 (it can change which page is touched)? **Would
   masking after translation be more correct, or worse?**
3. **`#524`: findings 4 and 5 say the low bits are NOT universally ignorable** — device dispatch and
   ARMv6 Device memory. **Does that make the fix wrong for some caller, or is it a disclosure?**
4. **`#525`: is returning 0 right?** Alternatives: leave the buffer untouched, return `0xff`, return
   the last written value, or fault. **Each has a different failure mode — rank them.**
5. *** THE ONE I MOST WANT ATTACKED, on both rounds: WHAT SELECTOR COULD EITHER REPAIR'S EFFECT BE
   CONDITIONED ON THAT THE DETECTOR NEVER VARIES? *** A sibling round in this project found **six
   mutants scoring a TOTAL ESCAPE** because every detector row probed a single position, and each
   mutant conditioned the repair on a tile or coordinate selector. **`#524` has 25 rows and `#525`
   has 16. Name a conditioning that both a plausible edit could produce and the rows could not
   see.**
6. **Should `#524` and `#525` be one commit or two?** They are different files, different devices,
   different defects — but both are "a handler ignored part of its own address."
7. **What is the smallest edit that breaks either fix and still passes its detector?**

**An honest "I could not settle that from this packet" is a real answer and is preferred over a
guess.** If you can read files and your line numbers disagree with this packet by hundreds, you are
reading a different copy of the tree — say so.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
