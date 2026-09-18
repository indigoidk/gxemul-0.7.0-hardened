# `landiskaux` — PASS 1: landisk's wdc alt-status register is mapped 0x1da bytes from where the guest writes, and the fix is one `case`

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.
**Check the premises, not just the derivations.** Where I state something as fact, ask whether it
is true. A seat that re-derives a premise from something this brief did NOT give it is worth more
than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** There are THREE pristine-2021-upstream copies of
GXemul under the project root (`./src/` and two under `_archive/audit-results-*/builds/`). They
are NOT this fork. If your line numbers disagree with mine by hundreds you are reading one of
them — say so rather than reconciling.

**If you cannot read files that is expected** — every fact you need is inlined. Name any premise
you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — an address, a span, an offset — ENUMERATE it
rather than reasoning about it.** A derivation that skips one multiplier reads exactly like a
correct one, and this round is *entirely* one multiplier.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## 1. PREMISES ALREADY SETTLED, RE-INLINED SO NOBODY SPENDS AN ANSWER RE-DERIVING THEM

Settled 2026-09-18 by opening each file (re-derive any of them; do not take them from me):

* **`dev_wdc.c:2098` switches on `devinit->machine->machine_type` with exactly THREE cases** —
  `MACHINE_MACPPC` (`+0x160`), `MACHINE_HPCMIPS` (a hardcoded `0x14000386`, itself guarded on
  `devinit->addr == 0x14000180` and carrying a `/* TODO: Fix */`), and `MACHINE_IQ80321`
  (`+0x402`). **There is no `MACHINE_LANDISK`.**
* **There is NO `default:` arm.** The switch ends at `:2110` with a bare `}`. The value comes from
  a PRE-SWITCH initialisation at `:2095`: `alt_status_addr = devinit->addr + 0x206;`. *(The queue
  row said "falls through to the default"; the substance is right and the word is not, and it
  matters here because a `case` that assigns nothing simply keeps `:2095`'s value.)*
* **`alt_status_addr` is NOT inside the main device mapping.** `:2120` registers a SEPARATE
  **two-byte** device, `"wdc_altstatus"`, at that address. `:2122` registers the main device at
  `devinit->addr` for `DEV_WDC_LENGTH * devinit->addr_mult` bytes.
* **`DEV_WDC_LENGTH` is 8** (`dev_wdc.c:45`), and **landisk passes `addr_mult=2`** — read from the
  device string itself at `machine_landisk.c:87-88`:
  `"wdc irq=%s.cpu[%i].irq[0x%x] addr_mult=2 addr=0x14000000"`.
* **`devinit->addr_mult` exists** (`src/include/device.h:53`, `int addr_mult`) and `dev_wdc.c`
  already uses it at `:1174` (`relative_addr /= d->addr_mult`), `:2083` and `:2123`.
* **`MACHINE_LANDISK` is 6004** (`src/include/machine.h:268`).

Settled 2026-08-27 by a MEASURED BOOT CENSUS (`regress/artifacts/landiskaux/census_20260827/`),
which this brief's first draft did not carry — the omission it exists to avoid:

* **OpenBSD 7.6 issues exactly TWELVE byte writes to `0x1400002c` and ZERO reads**, reproduced on
  FOUR runs across TWO independent instruments (three pristine boots, one census-hook build).
* All twelve are `len=1`, all from `pc=0x8c15f6e8 <obio_iomem_write_1+0x8>`, all `no_exceptions=0`
  — **real guest stores, not debugger reads.**
* Six carry `0x08` (WDCTL_4BIT), five `0x02` (WDCTL_IDS), and **the FIRST carries `0x0c` =
  `WDCTL_RST | WDCTL_4BIT` — a real ATA SOFT RESET, silently discarded today.**
* **LIVENESS CONTROL from the same boot:** the command block at `0x14000000..0x1400000f` SUCCEEDS
  — 12,718 accesses, `wd0` attaches with correct geometry — so `devinit->addr` is RIGHT and the
  defect is a missing offset case, not a wrong base.
* `wdc_altstatus` at `0x14000206` receives **ZERO accesses for the entire boot.**

Settled 2026-09-11 by a codex FIX-DESIGN run (`codex_fixdesign_20260911.txt`), each re-checked here:

* `dev_wdc_altstatus_access` does **NOT** divide `relative_addr` by `addr_mult` — it tests
  `relative_addr != 0` and nothing else. **So the primary's two-byte stride does not require a
  two-byte auxiliary registration.**
* **Twelve one-byte writes at offset 0 cannot distinguish a length-1 from a length-2
  registration** — already filed as `wdcaltwidth`.
* **Direct calls to the auxiliary handler cannot test the missing machine case**, since they
  bypass init and address dispatch.
* Codex **declined to derive the replacement address from the permitted files**, calling it
  "Verified `A`". *That refusal is the live question this panel inherits — see Q2.*

**THE ARITHMETIC, enumerated rather than asserted:**

    main wdc device : 0x14000000 .. 0x14000000 + 8*2 - 1  =  0x14000000..0x1400000f   (16 bytes)
                      -- which is exactly what machine_landisk.c:86's own comment claims,
                         "wdc0 at obio0 port 0x14000000-0x1400000f irq 10"
    altstatus TODAY : 0x14000000 + 0x206                  =  0x14000206   (2 bytes)
    guest WRITES    : 0x1400002c                          (twelve measured Device Control writes)
    fix would give  : 0x14000000 + 0x16 * 2               =  0x1400002c
    collision check : 0x2c = 44 >= 16, so the two-byte altstatus lands BEYOND the main span.
                      NO COLLISION.  (Nobody had run this check; it is the one that could have
                      made the fix register a device inside an existing one.)

---

## 2. THE FULL ENCLOSING BLOCK (comments trimmed; every exit path shown)

```c
	alt_status_addr = devinit->addr + 0x206;

	/*  Special hacks for individual machines:  */
	switch (devinit->machine->machine_type) {
	case MACHINE_MACPPC:
		alt_status_addr = devinit->addr + 0x160;
		break;
	case MACHINE_HPCMIPS:
		/*  TODO: Fix  */
		if (devinit->addr == 0x14000180)
			alt_status_addr = 0x14000386;
		break;
	case MACHINE_IQ80321:
		alt_status_addr = devinit->addr + 0x402;
		break;
	}

	/*  Get disk geometries:  */
	for (i=0; i<2; i++)
		if (diskimage_exist(devinit->machine, d->base_drive +i, DISKIMAGE_IDE))
			diskimage_getchs(devinit->machine, d->base_drive + i,
			    DISKIMAGE_IDE, &d->cyls[i], &d->heads[i], &d->sectors_per_track[i]);

	memory_device_register(devinit->machine->memory, "wdc_altstatus",
	    alt_status_addr, 2, dev_wdc_altstatus_access, d, DM_DEFAULT, NULL);
	memory_device_register(devinit->machine->memory, devinit->name,
	    devinit->addr, DEV_WDC_LENGTH * devinit->addr_mult, dev_wdc_access,
	    d, DM_DEFAULT, NULL);
```

## 3. THE PROPOSED FIX — one `case`, and it is the whole diff

```c
	case MACHINE_LANDISK:
		alt_status_addr = devinit->addr + 0x16 * devinit->addr_mult;
		break;
```

---

## 4. THE QUESTIONS

**Q1 — IS THE MULTIPLIER FORM RIGHT, OR SHOULD IT BE A LITERAL?** The three existing cases all use
a BARE offset (`+0x160`, `+0x402`) or a hardcoded absolute (`0x14000386`); **not one of them
multiplies by `addr_mult`.** So the prescribed line is the only case of its kind in the switch. Is
`0x16 * addr_mult` the right shape — it tracks the register-spacing the machine declares — or is
the house idiom here a plain `+ 0x2c`, with the multiplier an over-generalisation from a single
data point? *Both resolve to the same address today; they differ only if a future landisk variant
declares a different `addr_mult`.*

**Q2 — WHERE DOES 0x16 COME FROM, AND IS IT LOAD-BEARING?** The claim is that the OpenBSD 7.6
driver writes `0x1400002c`, and `0x2c / 2 == 0x16`. **A wrong multiplier maps the register
SILENTLY** — no crash, no diagnostic, just a control register nobody reads. What independent
evidence fixes 0x16 rather than 0x2c-as-a-literal? Is there an SH4/landisk source that states the
alt-status/Device-Control register's offset in *register units*?

**Q3 — THE WITNESS.** *The row recorded `witness: none` until today, and a measured rung-4 boot
census had been sitting in its own artifacts directory since 2026-08-27 — corrected before this
brief was fired.*  What remains genuinely open is clause (i): a rung-2..4 witness is INVALID
unless it shows the symptom pre-fix AND goes green post-fix **with the same script**.  Only the
pre-fix half can exist yet. **That is an argument about ONE instrument, not a demonstration that no guest-path
witness exists.** Per this project's 2026-08-27 lifecycle ruling, a round may not be recorded as
rung-1 until one seat has been asked to try a rung-3 probe — and the last time that ask was made, a
seat built a witness in a SINGLE invocation. **Can a rung-3 probe reach this?** A guest store to
`0x1400002c` on unmodified `-E landisk` should be swallowed today and answered by `wdc_altstatus`
after the fix; a store to `0x14000206` should show the mirror image. If you can name that probe,
say so concretely; if you are confident none exists, say why in terms that are not about the
offline differential.

**Q4 — THE OPTION SET.** This is an ADDITION to product code, and the ADDITION LICENCE says
additions are licensed by a MEASURED DELTA or a TRANSFERRED WARRANT, never by "it cannot hurt".
The claimed delta is twelve measured Device Control writes landing on unmapped memory. **Is that
delta real and is the addition the right member?** Name the members you would consider — including
ones this brief has not: is there a case for fixing `machine_landisk.c` instead (declare the
altstatus address at the machine, not in the device), or for the HPCMIPS-style absolute?

**Q5 — WHAT IS THE SMALLEST EDIT** to the block in §2 that breaks a property this fix claims and
still passes whatever detector ships with it? And — separately — **does adding a fourth `case`
create any hazard for the existing three?** Note `MACHINE_HPCMIPS` already guards on
`devinit->addr == 0x14000180` while landisk's addr is `0x14000000`: close, and worth checking that
no machine reaches two arms.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
