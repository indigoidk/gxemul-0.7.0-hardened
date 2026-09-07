# WITNESS DESIGN — `lcaconfwidth`: can a rung-3 probe show the kill message naming a value the guard accepts?

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Today four of my own censuses each keyed on one
spelling and missed a variant, and **your own census of this row corrected me in both directions**
(309 sites not 226; 18 proximate not 15). **Assume something below is wrong and find it.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies sit under the
project root and are NOT this fork.

**SCOPE:** `GXEMUL-SEC/src/devices/dev_lca.c`, `src/machines/machine_alpha.c`,
`src/include/thirdparty/alpha_lcareg.h`, `src/cpus/cpu_alpha*`, `GXEMUL-SEC/regress/alpha_harness_probe.py`.

**VERDICT LINE FIRST.**

---

## §C — SETTLED PREMISES, each verified by reading today

**S1 — THE DEFECT, in full.**

```c
	case LCA_IOC_CONF:
		if (writeflag == MEM_READ) {
			odata = d->ioc_conf;
		} else {
			d->ioc_conf = idata;              /* the FULL 64-bit value is stored */
			if (idata & ~1) {                 /* the guard sees all 64 bits */
				fatal("TODO: Write to unimplemented bit of"
				    " IOC_CONF: 0x%x\n", (int)idata);   /* the message sees 32 */
				exit(1);
			}
		}
		break;
```

**S2 — THE DISCRIMINATING VALUE.** A store of `0x100000000` sets bit 32. `idata & ~1` is true, so the
process dies — but `(int)idata` is **`0`**, and `0` is a value this guard **accepts**. *The kill
message names an acceptable value while killing on an unacceptable one.*

**S3 — ADDRESSES.** `alpha_lcareg.h`: `LCA_IOC_BASE 0x180000000ULL`,
`LCA_IOC_CONF (LCA_IOC_BASE + 0x020)` = **`0x180000020`**. Registered by
`memory_device_register(..., "lca_ioc", LCA_IOC_BASE, 0x20000000, dev_lca_ioc_access, ...)`.

**S4 — REACHABILITY.** `machine_alpha.c:61` does `device_add(machine, "lca")` inside
**`case ST_ALPHABOOK1:` only** — not for `alphaserver4100` or `3000/300`.

**S5 — THE TECHNIQUE ALREADY WORKS ON THAT MACHINE.**
`regress/alpha_harness_probe.py` ran today on an unmodified `-E alpha -e alphabook1` and scored
**7/9**, with `live` (guest store then load through RAM), `exec` (a guest LDAH/LDA pair reached a
register) and `palgate` all green. It builds K0SEG addresses with `k0(x) = 0xfffffc0000000000 | x`
and K0SEG translation is `vaddr & 0x000003ffffffffff`, so **`k0(0x180000020)` should reach physical
`0x180000020`** with no page tables involved.

**S6 — WHAT AN EARLIER DRAFT OF THAT HARNESS GOT WRONG, because the same trap applies here.** Every
structure was planted at `0x20010000`+ while `-M 64` gives 64 MB of RAM. Out-of-range writes are
**discarded** and reads **return zeros**, silently, so three rows would have gone green while
measuring nothing. The repair added `assert max(...) < 64*1024*1024` and a run-time `swpctx mapped`
row. **A device register at `0x180000020` is NOT RAM and NOT subject to that assert** — which is the
question below.

---

## The questions

**Q1 — IS THE WITNESS CONSTRUCTIBLE?** A guest 64-bit store of `0x100000000` to `k0(0x180000020)` on
stock `alphabook1`, with the oracle being the **`fatal()` text** — `IOC_CONF: 0x0` for the defect,
`IOC_CONF: 0x100000000` (or the correct rendering) once fixed. **Say plainly if it is not, and why** —
that is a real answer and changes the round to documented-only.

**Q2 — THE CONTROL THAT SEPARATES 'MEASURED THE DEVICE' FROM 'WROTE INTO NOTHING'.** S6's trap in its
device form: if `k0(0x180000020)` does *not* land on the LCA window, the store goes to unmapped space
and **nothing happens at all** — no message, no exit — which looks like "the guard did not fire".
**What positive control proves the store reached `dev_lca`?** A read-back of `d->ioc_conf` via
`LCA_IOC_CONF` read is one candidate; a store of a *legal* value (`0x1`) that survives is another.
**Which, and is either sufficient alone?**

**Q3 — DOES THE STORE EVEN CARRY 64 BITS?** `len` reaches the handler and `memory_readmax64` builds
`idata` from it. **Check what an Alpha `stq` to a device produces here**, and whether the emulator
splits or narrows it before `dev_lca_ioc_access` sees it. If `idata` cannot hold bit 32 at this site,
S2 is wrong and the row is much weaker.

**Q4 — IS `exit(1)` SURVIVABLE AS AN ORACLE?** The probe must read the message the emulator printed
*before* it died. `alpha_harness_probe.py` runs under `-V` single-step with a pty. **Does the text
reach the pty before exit, and can the probe distinguish this kill from the other ten live `exit(1)`
sites in `dev_lca.c`** — including the two bare `fatal()+exit(1)` interrupt stubs that kill with the
same status?

**Q5 — WHAT IS THE SMALLEST EDIT that fixes the message and still leaves the row's oracle green?** The
intended repair is `%" PRIx64 "` with the cast dropped, matching the **five sibling arms twelve lines
away that already use `(uint64_t)idata`** (`:225 :240 :255 :279 :294`). **Is `PRIx64` already used in
this tree, and does any gate or hygiene grep match on the current text of this message?**

## What I am not asking

Do not write a patch or a probe, and do not run anything. **Nothing ships until the flagship
adjudication on 2026-09-09.**

**If, while verifying a claim, you found something ELSE — say so.**

*(Note: the codex seat refused the sibling census brief for this row on its content filter — the
shape "find the value that defeats the check" reads as offensive tooling even when the subject is a
diagnostic's correctness. This is a correctness question about a printf format specifier.)*
