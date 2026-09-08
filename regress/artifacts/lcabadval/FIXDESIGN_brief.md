# `lcabadval` fix design — six arms, and the panel has already narrowed which are defective

**VERDICT LINE FIRST.**

**The tree is `GXEMUL-SEC/src/`** — ignore the pristine 2021 copy at the project root.
**The manual is local:** `_scratchpad/21066_66a_hrm.txt` (Alpha 21066/21066A HRM, 13,876 lines).

**Please do not simply ratify.** Everything in section 2 below came from a six-seat panel and four
of those findings CORRECTED me. **Check the premises, not just the derivations** — and in
particular check §2's claims against the manual yourself, because I am now one layer removed from
it.

## 1. THE SITE

`DEVICE_ACCESS(lca_ioc)` in `src/devices/dev_lca.c`. Six arms **store the written value and then
test it**, ending the process on anything outside a narrow set:

```c
	case LCA_IOC_CONF:      d->conf = idata;          if (idata & ~1)                     -> exit(1)
	case LCA_IOC_TB_ENA:    d->tb_ena = idata;        if (idata & ~IOC_TB_ENA_TEN)        -> exit(1)
	case LCA_IOC_W_BASE0:   d->window_base_0 = idata; if (idata != 0 && idata != 0x300800000ULL) -> exit(1)
	case LCA_IOC_W_MASK0:   d->window_mask_0 = idata; if (idata != 0x700000ULL)           -> exit(1)
	case LCA_IOC_W_BASE1:   d->window_base_1 = idata; if (idata != 0x240000000ULL)        -> exit(1)
	case LCA_IOC_W_MASK1:   d->window_mask_1 = idata; if (idata != 0x3ff00000ULL)         -> exit(1)
```

plus a `default:` arm that ends the process on **reads as well as writes**. `fatal()` only prints
(`debugmsg.c:384` has no early-out); the explicit `exit(1)` is what terminates.

`machine_alpha.c:61` installs this device on `alphabook1` only.

## 2. WHAT THE PANEL ESTABLISHED — six seats, and four of these corrected me

| claim | who |
|---|---|
| `IOC_W_MASK<31:20>` has **13** legal values (Table 6-6, a doubling run 1 MB → 4 GB, each `2^k − 1`); the fork accepts **one** per register, so **12/13 rejected each** | confirmed by codex, glm, kimi, minimax, grok |
| **RES fields are type `X` — IGNORED ON WRITES**, not must-be-zero (`:955`, `:985`) | codex, settling deepseek's challenge |
| **therefore the guards test the WHOLE 64-BIT OPERAND while the hardware defines a 12-bit field**; `0x7000ff` is functionally identical on real hardware and ends the process | deepseek raised, codex settled |
| bases must **align naturally to window size** and windows **must not overlap** (`:9618`, §6.4.9). With the two accepted bases FIXED, window 0 admits only the four sizes through 8 MB and window 1 the eleven through 1 GB | codex |
| **`IOC_CONF` is a TWO-bit field**, so `idata & ~1` rejects **2 of 4** defined settings | codex |
| **`IOC_TB_ENA` is NOT a functional defect** — TEN has exactly two states and both are accepted (**0/2**) | codex |
| **the manual REQUIRES initialising BOTH base registers to zero (§6.4.14, `:10788`), and `W_BASE1` rejects exactly that** | codex |
| the registers are **64-bit, quadword access only**; §6.4 excludes longword (`:10175`) | codex |

*** AND A TRAP A NAIVE FIX WALKS INTO, from deepseek: the `2^k − 1` invariant must be applied to
the SHIFTED FIELD. `(idata & (idata + 1)) == 0` on the full register value REJECTS the legal
`0x700000`, because `0x700000 & 0x700001 == 0x700000`. The guard is `f = idata >> 20;
(f & (f + 1)) == 0`. ***

## 3. WHAT IS NOT SETTLED

* **Whether the model's own address decode uses these registers at all.** If it does not, accepting
  a value the model then ignores is a different disposition from accepting one it honours.
* **What `W_BASE` legally accepts.** The manual enumerates no whitelist for it — deepseek warned
  explicitly against widening that accept set without evidence.
* **Whether any guest reaches these writes.** No reproduction exists.

## 4. QUESTIONS

**Q1. PER ARM, what should it do?** The dispositions available are: delete the termination; decline
the write silently; decline with a once-only announcement (this fork's house style, `(once)` being
the plurality marker — derive the count, do not quote mine); accept and store; accept with backing
storage so reads return it. **Give one per arm with its reason**, and note that `W_MASK` and
`W_BASE` have different characters because the manual enumerates legal values for one and not the
other. **Say explicitly if `TB_ENA` should be left alone** — the panel says it is not a functional
defect.

**Q2. Should the guards test the FIELD or the OPERAND?** Given RES bits are ignored on writes,
a faithful model arguably ignores them too. **Does the fix mask before testing, and if so, with
what mask per register?**

**Q3. Grep the fork for an existing idiom before reasoning from first principles.** How do other
chipset models in `src/devices/` handle a register value they do not model? Name the closest
analogue and say whether it transfers. **And check the SIBLING arms in this same file** — that
comparison has settled this question on other rows.

**Q4. What observable distinguishes a correct fix from an incomplete one?** Name the specific state
or output a regression row should assert, so that a later partial implementation does not read as
complete. In particular: what distinguishes "the write was accepted and stored" from "the write was
accepted and discarded"?

**Q5. Is a reproduction possible on unmodified `-E alpha -e alphabook1`?** A working Alpha probe
harness exists at `regress/alpha_swpctx_v0_probe.py` (pty, `put`/`step`/`print`, an Alpha encoder,
measured today). **If a guest write to these registers is reachable, say what the sequence is; if
not, say so plainly.**
