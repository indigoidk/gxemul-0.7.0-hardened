# LCA configuration decode — review YOUR OWN prescription, harder than you reviewed mine

**VERDICT LINE FIRST.**

**The tree under review is `GXEMUL-SEC/src/`.** Ignore any other `src/` at the project root — a
pristine 2021 upstream copy lives there and reports line numbers off by hundreds.

**This is a self-review and the standing rule for one is: be HARDER on your own finding than on
anyone else's, and answer whether the FIX is right, not merely whether the finding was. Those are
different claims and the second does not follow from the first.** A ruling that adopts your own
position is the one you are least likely to test.

## 1. WHAT YOU SAID YESTERDAY

Reviewing my fix design you returned **REVISE**, and I accepted all of it:

* `dev = (tag >> 11) & 0x1f` is correct — validated over 4,194,304 encode/decode combinations,
  which you labelled an arithmetic check and not an emulator test.
* My sketch decoded `dev` and not `bus`. Minimum correction:
  ```c
  } else {
      bus = (tag >> 16) & 0xff;
      dev = (tag >> 11) & 0x1f;
  }
  ```
* **Do not choose the decoding branch from the extracted bus field** — primary-bus IDSEL bits
  overlap it, and keeping `bus == 1` in the forwarding call collapses every type-1 destination
  onto bus 1.
* My premise 4 was false: `bus_pci_data_access` returns all-ones for **register 0 only**, ZERO for
  every other register, and prints a diagnostic on every write.
* My discriminating row cannot discriminate, and has three false-positive traps: the probe address
  encodes bus ZERO and reaches the no-IDSEL fallback to device 0; a failed load leaves the
  destination register untouched so the row re-reads the all-ones already there; and `printed`
  uses `re.search`, taking the first observation.
* You prescribed instead: keep the signature check as an empty-ID completion check with an
  independently identified result and a distinct prior destination value, **and add a model-level
  routing fixture observing the exact bus/device/function/register passed onward**, with distinct
  synthetic devices on bus 1 and another bus, including write dispatch and preservation of
  primary-bus decoding.

## 2. WHAT HAS CHANGED SINCE — the manual is local now, and I verified your citations

I fetched the manual at your citation and **read the three load-bearing passages rather than
trusting the page anchors**, because this project once shipped ARM manual page numbers that came
from panel output rather than from a manual. `_scratchpad/21066_66a_hrm.txt`, 13,876 lines:

* `:8840` §6.2.6 — *"CPU physical address bits <31:7> are used for PCI address bits <26:2>"*.
  **CONFIRMED: the shift of 5.**
* `:9216` §6.2.9 — *"PCI address bits ad<1:0> come directly from configuration cycle type register
  (IOC_CONF, Section 6.4.2) bits <1:0>"*. **CONFIRMED: cycle type, not bus.**
* `:9486` §6.2.18 — *"the IOC returns arbitrary data with error status to the CPU, which causes an
  instruction exception"*, plus an internal interrupt and ERR/CODE=1/CMD/ADDR/LOST logging.
  **CONFIRMED: absent-device reads are not all-ones on real hardware.**

**One narrowing I recorded against you, and I want you to check it:** you wrote *"bits 23..2 from
CPU address bits 28..7"*. The manual's general sparse rule is the WIDER `<31:7> -> <26:2>` with the
same shift. I concluded your range is the PCI type-1 config format, which §6.2.9 defers to
explicitly, and that therefore **the field positions rest on the PCI specification and not on this
manual** — so a round must cite them accordingly. **Is that right, or did I narrow it wrongly?**

## 3. QUESTIONS — all about YOUR prescription

**Q1. Is the model-level routing fixture actually buildable in this tree, or did you prescribe an
instrument that does not exist?** Name the concrete mechanism. If it needs a synthetic device on
bus 1, say exactly how one is added on `-E alpha -e alphabook1` **without modifying the committed
machine description** — because a machine or `device_add` introduced *in order to* reach the site
is laundering, not witnessing, and this project rejects it by rule. If it cannot be done that way,
say so plainly; that is a real answer and it changes the round's shape.

**Q2. Your own decode: is `bus = (tag >> 16) & 0xff` right, and is 8 bits the right width?** Check
it against the PCI type-1 field layout AND against what this model's backend can actually consume.

**Q3. §6.2.18 says real hardware raises an instruction exception on master abort. The tree cannot
do that on Alpha. Does that make the whole IMPLEMENT disposition wrong** — i.e. is forwarding to a
backend that silently returns all-ones/zero a *worse* model than what is there now, on any
axis a guest can observe? Argue the strongest case AGAINST your own recommendation.

**Q4. WHICH OF YOUR OWN FIVE FINDINGS IS THE WEAKEST, and what would refute it?** Name it
explicitly with the count. A review that stands entirely behind itself has stopped arguing.

**Q5. Scope.** You listed `lca_ioc`'s default arm, the two interrupt handlers and `lca_isa`'s guard
as remaining. Of those, which belongs in THIS round under a one-site rule, and which are separate
rounds? Give an ordering with reasons.
