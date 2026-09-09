# `lcaconfbus1kill` — the revised design, after you withdrew your own fixture

**VERDICT LINE FIRST.**  **The tree is `GXEMUL-SEC/src/`** — ignore the 2021 copy at the project root.

**Almost everything below is your own prior work, and I want you harder on it than you were the
first time.** In particular: **you withdrew the fixture you originally prescribed.** That withdrawal
is the most useful thing in the file and it leaves a hole this brief has to fill.

## 1. WHERE THIS STANDS

`DEVICE_ACCESS(lca_pci_conf)` ends the host when `LCA_IOC_CONF` holds a value its own guard accepts.
A rung-3 witness shipped in `7c2f8e4` (`regress/lca_confbus_probe.py`, HEAD 3/4).

**SETTLED ACROSS TWO OF YOUR PASSES, each verified by me:**

* `dev = (tag >> 11) & 0x1f` is correct; `bus = (tag >> 16) & 0xff` is the missing half — 8 bits,
  and `bus_pci_decompose_1()` already uses that mask and shift, `cur_bus` and each device's `bus`
  are plain `int`, and `bus_pci_data_access()` does exact tuple equality. No one-bit representation
  constrains the range.
* **DO NOT choose the decoding branch from the extracted bus field** — primary-bus IDSEL bits
  overlap it, and keeping `bus == 1` in the forwarding call collapses every type-1 destination onto
  bus 1.
* **Premise 4 of mine was false:** `bus_pci_data_access` returns all-ones for **register 0 only**,
  ZERO for any other register, and prints a diagnostic on every write.
* **The manual is local now** (`_scratchpad/21066_66a_hrm.txt`) and I verified three claims by
  reading: the shift of 5 (`:8840`), `ad<1:0>` from IOC_CONF (`:9216`), and §6.2.18 master abort
  returning *"arbitrary data with error status ... which causes an instruction exception"* (`:9486`).
  **So all-ones is an emulator-compatibility oracle, not a hardware contract.**
* **A guest source tree is local**: `_guest-src-openbsd22/`. You cited `lca_pci.c:142` from it.

## 2. WHAT YOU WITHDREW, AND WHY IT MATTERS

You originally prescribed a model-level routing fixture with synthetic devices on bus 1 and another
bus. On self-review you established there is **no existing mechanism to populate that bus on
unchanged `alphabook1`** — `MACHINE_SETUP(alpha)` adds `lca`, whose initializer adds only
`i82378zb` at 0:7:0, and the generic `device_add()` parser offers no attachment for a PCI function
on that existing bus. **You withdrew the fixture as a prerequisite**, and proposed instead passive
host-debugger observation at `bus_pci_setaddr()` / `bus_pci_data_access()`, citing the existing
precedent at `sgi_eaddr_probe.py:35`.

**And you found a routing defect that needs NO synthetic device:** unconditional forwarding of a
type-1 cycle with bus zero can select the existing primary-bus `i82378zb`, because the backend
receives no cycle type and cannot reject the alias. **Your own words: identifying it did not repair
the proposed fix.**

## 3. QUESTIONS

**Q1. GIVE THE ACTUAL DIFF.** Not the shape — the lines. It must decode `bus`, must not choose the
branch from the extracted bus field, and must not alias a type-1 cycle with bus zero onto the
primary bus. **If that cannot be done without a cycle-type argument reaching the backend, say so** —
that is a real answer and it makes this a larger round than one arm.

**Q2. Is the host-debugger observation actually buildable here?** You cited `sgi_eaddr_probe.py:35`
as precedent. **Does that technique transfer to this call site**, and what exactly would it assert?
If it needs a debugger this environment lacks, say so plainly.

**Q3. The OpenBSD consequence — check it in the local tree.** You wrote that `lca_conf_read()`
initialises its result to all-ones and reads only if `badaddr()` succeeds, so absence normalises to
all-ones **at any register offset**, and a faultless backend zero at a nonzero offset changes that.
**Verify that against `_guest-src-openbsd22/sys/arch/alpha/pci/lca_pci.c` and say whether the guest
would actually observe the difference**, or whether the probe path never reaches a nonzero register.

**Q4. What observable distinguishes a correct fix from an incomplete one?** Specifically: what
should a regression row assert so that a fix which decodes `bus` but still aliases bus zero onto the
primary bus does not read as complete?

**Q5. Scope.** Does this round take only the configuration handler's termination and its missing
decode, or does the bus-zero alias have to land in the same diff? **Argue the case for the narrower
round first, then say which you hold.**
