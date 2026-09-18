# `#530 lcaisalane` -- claims in THIS TREE that closing pass 5 REFUTED

**Same construction as `../crimewidthkill/CORRECTIONS.md`, and for the same reason.** Everything under this directory
is EVIDENCE -- frozen instruments preserved as run, briefs preserved as sent, a seat report in the seat's own words.
**Editing any of them would falsify the record**: a frozen probe that no longer matches the run it is the artifact of
is worse than a wrong sentence, because the score it produced can no longer be re-derived from it.

So the refuted claims stay, and this file is the pointer -- **in the directory a grep-reader is already searching**,
which is the carrier's own finding about why demoting a claim in place fails (*the reuser is searching for the
SUBJECT, not reading the paragraph*).

**POINTER, not a second copy.** The finding lives in `opus_c5_20260915/OPUS_ANSWER.md`; the live corrections are in
`../../lca_isalane_probe.py` (the contract block) and `fix530_20260914/table6/POSTTABLE.out` (the FLOOR line). If this
file disagrees with those, THEY are right.

---

## THE ONE SENTENCE WORTH CARRYING OUT OF THIS PASS

> **A forward-COUNT row needs a COUNTER or an ALTERNATOR. A one-shot LATCH cannot carry this class.**

Repair 5 put CMOS REG C at lane 1 and ns16550 IIR at lane 2. `dev_mc146818.c:565` -- the read does
`d->reg[MC_REGC*4] = 0x00;`, so a second read finds it already zero, and the write path is a plain assignment.
`dev_ns16550.c:211-213` -- the read clears `IIR_TXRDY` once; the write path is `d->fcr = idata;`.

**Both are one-shot latches. A latch separates ZERO accesses from AT LEAST ONE. It can never separate ONE from TWO --
which is exactly and only what a forward-count class asks.** Every count mutant that leaves the first access intact
and adds a second is invisible to them *by construction*. That is the mechanical cause of all three RB1 breaches
below: the emulator-TODO stub was carrying those cells alone because **the stub is an ALTERNATOR and its neighbours
were LATCHES**.

---

## 1. "never as the sole carrier" -- MEASURED FALSE THREE TIMES

The claim the row set was built to satisfy, and the ruling's RB1.

| mutant | score | what actually reds |
|---|---|---|
| `WWall` (write x DUPLICATE, ungated) | 169/185 | **sixteen stub rows and NOTHING ELSE** -- no `kbcq * dib`, no `iir st*`, no `cmos w*`, no `tailq w t*`. Sole carrier at lanes 0, 1 AND 2: **twelve cells** |
| `RWall` (read x ADD-OTHER) | 167/185 | 16 stub + 2 `tailr` -- every direct lane |
| `RD2post` (read x DUPLICATE, after the loop) | 161/185 | no architectural carrier at lanes 1 or 2 |

**It occurs at TWO SITES in the live probe** (the contract block, and again in the `4l rdq` preamble) -- both corrected,
per the grep-for-siblings rule, which is what found the second one.

## 2. "the forward-count class CLOSED BY ENUMERATION SINCE REPAIR 5 ... in either form"

The class is **EIGHT cells**, derived from the handler rather than from the findings: `DEVICE_ACCESS(lca_isa)` emits
exactly ONE 1-byte bus forward per access, and the one-edit perturbations of a one-element sequence are **DROP**
(length 0), **SWAP** (length 1, direction flipped), **DUPLICATE** (length 2, same direction) and **ADD-OTHER**
(length 2, mixed), over **two arms**.

The contract names two: the write arm's ADD-OTHER (`x_wfallthru`) and the read arm's DUPLICATE (`RD2`). Measured this
pass: the write arm's DUPLICATE **escapes** at the tails and at len 6 (`WWtail`, `WW6`, both 185/185); DROP and SWAP on
both arms had never been built by any pass (`Wdrop` 136, `WXR` 140, `Rdrop` 127, `RXW` 143 -- all caught, none an
escape).

## 3. "DIRECT cells ... every one rowed"

False for the write-DUPLICATE and read-ADD cells: at lanes 0/1/2 they are rowed by the stub **alone**, which the same
header forbids two lines earlier.

## 4. "the zero/nonzero partition is rowed on both sides"

A **marginal** over all cells, written in a form that reads as a per-cell claim. Three joints measured empty:
lane 3 x zero store (`cdxZL3` 185/185), tail x nonzero store (`dNZtail` 185/185), any lane x zero delivered byte
(`RD2z` 185/185). The axis stays clause-(e) DEBT and not floor -- the write body tests no bit of the value -- but the
debt must be disclosed per cell rather than claimed closed.

## 5. "a DIRECTION swap ... is a different class, caught by the value rows"

It is a **cell of this class** (the SWAP shape), and the second half is half true in the half that matters. The value
rows catch the **missing read** -- `RXW` 143/185, and all 42 of its reds are read-value rows with **zero** stub rows,
so the access *count* is still one -- and **nothing whatever observes the acquired WRITE**. Independent proof: restore
the read and keep the write (`RWall`) and the detector falls to 167/185, the stub and two `tailr` rows. The sentence
also conflated SWAP with ADD-OTHER, which are different shapes.

---

## Where the refuted sentences still sit, and why they stay

| file | kind |
|---|---|
| `fix530_20260914/lca_isalane_probe.r6.frozen.py` | frozen instrument |
| `fix530_20260914/lca_isalane_probe.FIX_r6.asrun.py` | as-run instrument (FIX_r6 185/185) |
| `fix530_20260914/lca_isalane_probe.HEAD_r6.asrun.py` | as-run instrument (HEAD_r6 112/185) |
| `fix530_20260914/table6/lca_isalane_probe.table6.py` | **the instrument kill table 6 ran** |
| `opus_c5_20260915/instrument/lca_isalane_probe.c5.frozen.py` | the frozen copy closing pass 5 measured against |
| `c5_20260915/brief_sent.md`, `brief_sent.packet.md` | the briefs AS SENT to the panel |

`opus_c5_20260915/OPUS_ANSWER.md` also contains the sentences -- **as quotations inside its own refutation of them**,
which is the form this project mandates and is not a stale claim.

## What is NOT changed by any of this

**`HEAD_r6` 112/185 and `FIX_r6` 185/185 are correct and were re-verified**, and `PREDICT_r6.out` was checked and found
**clean** -- its 30 named new reds are exactly the 30 in `HEAD_r6.out`'s new sessions, recorded as checked rather than
left blank, because an unrun check and a clean one must not render the same.

**And the FIX itself is correct and untouched.** Six passes now agree. Every finding above is against the DETECTOR and
its record, not against `dev_lca.c`.
