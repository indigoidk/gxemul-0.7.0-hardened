# CHECK A PROPOSED TEST CONSTRUCTION — is this witness sound, and are its controls adequate?

**VERDICT LINE FIRST**, then the body.

Scope your reading to **`GXEMUL-SEC/src/`** and **`GXEMUL-SEC/regress/`**. Ignore any other `src/`
you can reach — three pristine 2021 upstream copies sit under the project root and give line numbers
off by hundreds.

**I am asking you to CHECK A CONSTRUCTION I SUPPLY and to audit its premises.** Do not write the
probe. Judge whether the construction below would establish what I claim it establishes, and say
where it would not.

This is ordinary regression-test adequacy review: the question is whether a proposed test
distinguishes the two code states it is supposed to distinguish, and whether its controls rule out
the alternative explanations.

---

## The behaviour under test, verified by reading both functions

`dev_lca.c` has two device handlers that share one field. Verbatim.

**Writer — `DEVICE_ACCESS(lca_ioc)`, `case LCA_IOC_CONF`:**

```c
	case LCA_IOC_CONF:
		if (writeflag == MEM_READ) {
			odata = d->ioc_conf;
		} else {
			d->ioc_conf = idata;
			/*  Only bit 0 is implemented so far, the PCI bus 0 vs
			    bus non-0 selection bit.  */
			if (idata & ~1) {
				fatal("TODO: Write to unimplemented bit of"
				    " IOC_CONF: 0x%" PRIx64 "\n", (uint64_t)idata);
				exit(1);
			}
		}
		break;
```

A write of `0x1` gives `idata & ~1 == 0`, so it is **accepted** and stored.

**Reader — `DEVICE_ACCESS(lca_pci_conf)`.** Between function entry and the line below there is only
address arithmetic (`reg`, `tag`) — **no guard and no early return**, which I checked:

```c
	bus = d->ioc_conf & 1;

	if (bus == 0) {
		for (dev=0; dev<21; dev++)
			if (tag & (0x800 << dev))
				break;
		if (dev >= 21) {
			/*  fatal("[ LCA: No bus 0 device? TODO ]\n");
			exit(1);  */
			dev = 0;
		}
	} else {
		fatal("TODO. Non-zero bus.\n");
		exit(1);
	}
```

So the claim is: **an accepted write to one register arms an `exit(1)` in a different handler, on a
later access.** `fatal()` does not itself terminate (it calls the returning printer `va_debug()`);
the explicit `exit(1)` does.

**Mapping, from `DEVINIT(lca)`:**

    memory_device_register(..., "lca_pci_conf", LCA_PCI_CONF, 0x20000000, dev_lca_pci_conf_access, ...)
    memory_device_register(..., "lca_ioc",      LCA_IOC_BASE, 0x20000000, dev_lca_ioc_access,      ...)

    LCA_IOC_BASE  0x180000000     LCA_IOC_CONF  LCA_IOC_BASE + 0x020
    LCA_PCI_CONF  0x1e0000000

`device_add(machine, "lca")` appears under `ST_ALPHABOOK1` and no other subtype.

---

## The proposed construction

`regress/lca_confwidth_probe.py` already exists and already drives a guest `stq` of `0x1` to
`LCA_IOC_CONF` on unmodified `alphabook1`, then reads it back with a guest `ldq` through the same
decode. It uses K0SEG addressing (`K0SEG = 0xfffffc0000000000`, `k0(p) = K0SEG | p`), plants 64-bit
operands in RAM with debugger `put d`, and loads them with `ldq` because the address needs bits
63..42 and some operands need bit 32.

**The proposal is ONE additional session in that file:**

    S1  guest stq  0x1  ->  k0(LCA_IOC_CONF)      accepted; d->ioc_conf = 1
    S2  guest ldq  from k0(LCA_PCI_CONF + 0)      any access in the window reaches `bus = ...`
        expected on the committed build:  host exits, "TODO. Non-zero bus." on stderr
        expected after a fix:             host survives, session completes

**Proposed controls:**

* **MATCHED SURVIVING CONTROL (the one I think does the real work).** The *same* `ldq` at the *same*
  address and width, in a session where S1 is **omitted** so `ioc_conf` stays 0. If that session
  survives, the kill is attributable to the **value**, not to the address, the width, or the fact
  that the window is touched at all.
* **LIVENESS.** The existing `ioc rt` row already proves the CONF decode is reached and answers: a
  guest `stq` of `0x1` followed by a guest `ldq` returns `0x1` through the same decode.
* **DEVICE SIGNATURE.** The literal `TODO. Non-zero bus.` is emitted by this arm and nothing else —
  RAM would return data, and an unmapped address would behave differently again.

**Three traps that file already documents and pays for**, so a new session should not rediscover
them: debugger `dump` skips `DM_DEFAULT` handlers; a debugger `put d` of a killing value **is** a
host kill but is **not** a guest instruction, so it does not witness anything; and HAE at window
offset 0 silently succeeds, so a *miss* control must not use `LCA_IOC_BASE + 0`.

---

## Questions

1. **Does S2 actually reach `bus = d->ioc_conf & 1`?** I claim any access in the `lca_pci_conf`
   window does, because there is no guard or early return before it. **Check that against the whole
   function**, including anything before the excerpt I quoted, and including whether `len`, the
   access width, or `writeflag` could route elsewhere.

2. **Is `LCA_PCI_CONF + 0` a sound choice of offset,** or does offset 0 have the same "silently
   succeeds" property that `LCA_IOC_BASE + 0` (HAE) has? If it is a bad choice, which offset in that
   window is a clean one, and why?

3. **Is the matched surviving control sufficient to attribute the kill to the VALUE?** What
   alternative explanation survives both sessions? I am specifically worried that something *other*
   than `ioc_conf` differs between S1-present and S1-absent runs — e.g. side effects of the extra
   store, or state the first access leaves behind.

4. **Is a READ the right access for S2, or should it be a write?** The handler runs for both. Is
   there any reason the read path would not reach the same line?

5. **What does this construction NOT establish?** I claim it shows a guest-drivable host exit
   reachable through two ordinary accesses with no rejected value. I am *not* claiming any shipped
   guest does this. Is the weaker claim correctly scoped, and is there a stronger claim the same
   construction would support?

6. If, while checking this, you found something **else** about either handler — say so.

## Rules

* Answer from the source; name file and function for every behaviour you assert.
* **Give the denominator**: how much of each handler you actually read.
* A clean "your construction fails at step N because X" is the most useful answer you can give.
