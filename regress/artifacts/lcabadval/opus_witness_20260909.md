# `lcabadval` — RUNG-3 WITNESS, measured

**Seat:** Opus 5 measuring seat · **Date:** 2026-09-09/10 · **Task:** build the reproduce-before-edit
witness for `lcabadval`.

    LCABADVAL_RESULT=14/20      LCABADVAL_WITNESS=FAIL      LCABADVAL_ARMS=6

**RED: the six `<arm> legal` rows — one per value-guarded arm — and that is the defect.** Every one
of them drives a value the 21066/21066A hardware manual documents as legal for that register, and
every one ends the emulator process. The oracle polarity is the ladder's: each row's `want` is
`alive`, so the witness is RED on HEAD and goes green post-fix with the same script.

**Reproduction is CLEAN — all six deaths carry the arm's own diagnostic.** No death was for a
different reason; none landed in the `default:` arm; the negative control survived.

    log      GXEMUL-SEC/regress/artifacts/lcabadval/witness_20260909/HEAD_74daefd.out
    replica  GXEMUL-SEC/regress/artifacts/lcabadval/witness_20260909/HEAD_74daefd_run2.out
    probe    GXEMUL-SEC/regress/lca_badval_probe.py
    frozen   .../witness_20260909/lca_badval_probe.asrun.py   (md5 b703190ea75c771beb6ad09619a502d9,
                                                               byte-identical to the shipped probe)
    driver   .../witness_20260909/run_witness.sh

---

## 1. Two-part clearance — RUN, not asserted

Re-run inside the driver so its output is in the log rather than in a terminal I have to be believed
about:

    PART 1 PASS: build/src/devices/dev_lca.c == GXEMUL-SEC/src/devices/dev_lca.c
    PART 2 PASS: build/gxemul is NEWER than its dev_lca.c
    -rwx 6155592 2026-09-09 13:58:44.391022000 -0500  build/gxemul
    -rwx   17763 2026-09-09 13:58:29.121999100 -0500  build/src/devices/dev_lca.c
    MUTANT sentinel: absent (good)

`dev_lca.c` is a SHARED file — it is not among the six non-comment entries of
`tools/est_divergence.txt` (checked) — so `cmp` against SEC is the correct comparison and the
divergence-set carve-out does not apply. **Nothing was built and nothing was mutated.**

## 2. Provenance — git HEAD moved twice during this work, and `dev_lca.c` did not

The task named HEAD `74daefd`. The main loop committed while I measured, so the two logs record
`54a2eb4` and `e73623a`. **Checked rather than assumed:**

    git diff --stat 74daefd..HEAD -- src/devices/dev_lca.c src/include/thirdparty/alpha_lcareg.h
      -> EMPTY, and the working tree matches 74daefd for both files.

The intervening commits touch `dev_pcc2.c`, `mvme_pcctworeg.h`, `CHANGELOG.md` and
`pass2_ledger.tsv` only. The binary predates all of them (13:58) and part 1 passed against the
current tree, so **the measurement is valid for 74daefd, 54a2eb4 and e73623a alike.** The log's
`HEAD_74daefd` label names the code under test; the `HEAD:` line names the repo at run time. They
disagree on purpose and this paragraph is why.

## 3. Row table (both runs identical apart from that `HEAD:` line)

| row | got | want | |
|---|---|---|---|
| `conf live`     | `0x0->0x1`         | `0x0->0x1`         | ok |
| **`conf legal`**   | **`dead`**      | `alive`            | **FAIL** |
| `conf attrib`   | `yes`              | `yes`              | ok |
| `tbena live`    | `0x0->0x80`        | `0x0->0x80`        | ok |
| **`tbena legal`**  | **`dead`**      | `alive`            | **FAIL** |
| `tbena attrib`  | `yes`              | `yes`              | ok |
| `wbase0 live`   | `0x0->0x300800000` | `0x0->0x300800000` | ok |
| **`wbase0 legal`** | **`dead`**      | `alive`            | **FAIL** |
| `wbase0 attrib` | `yes`              | `yes`              | ok |
| `wmask0 live`   | `0x0->0x700000`    | `0x0->0x700000`    | ok |
| **`wmask0 legal`** | **`dead`**      | `alive`            | **FAIL** |
| `wmask0 attrib` | `yes`              | `yes`              | ok |
| `wbase1 live`   | `0x0->0x240000000` | `0x0->0x240000000` | ok |
| **`wbase1 legal`** | **`dead`**      | `alive`            | **FAIL** |
| `wbase1 attrib` | `yes`              | `yes`              | ok |
| `wmask1 live`   | `0x0->0x3ff00000`  | `0x0->0x3ff00000`  | ok |
| **`wmask1 legal`** | **`dead`**      | `alive`            | **FAIL** |
| `wmask1 attrib` | `yes`              | `yes`              | ok |
| `ctl noguard`   | `alive`            | `alive`            | ok |
| `ctl echo`      | `0x0->0x100000`    | `0x0->0x100000`    | ok |

## 4. The deaths, with their verbatim text

Echoed into the log by the probe itself, because an attribution row whose only evidence is a pty
buffer nobody preserved is a green row a later reader cannot check:

    TODO: Write to unimplemented bit of IOC_CONF: 0x2
    TODO: LCA_IOC_TB_ENA value  (0x81) has unimplemented bits.
    TODO: LCA_IOC_W_BASE0 value differs (0x280000000) from the only implemented values
    TODO: LCA_IOC_W_MASK0 value differs (0x100000) from the only implemented value
    TODO: LCA_IOC_W_BASE1 value differs (0x0) from the only implemented value
    TODO: LCA_IOC_W_MASK1 value differs (0xfff00000) from the only implemented value

Each literal was verified **unique in `src/`** (one hit each) before it was used as an oracle. The
one text that does *not* appear anywhere in either log is the `default:` arm's
`[ lca_ioc: unimplemented ... ]` — which is what a mis-aimed offset would have produced. **"Did it
fail for the reason under test?" — yes, six times out of six.**

## 5. The values, and why each `legal` one is legal

Every citation is a line I opened in `_scratchpad/21066_66a_hrm.txt`, not a page anchor from a seat.

| arm | offset | fork accepts | `live` | `legal` | manual warrant |
|---|---|---|---|---|---|
| `IOC_CONF` | `+0x020` | `{0,1}` | `0x1` | **`0x2`** | Table 6-10 `:10250-10254` — bits `<1:0>` are the **CFG AD<1:0> field**, so all four encodings are legal; S6.2.9 `:9217` says the same from the PCI side. The guard accepts **half of a documented two-bit field**. |
| `IOC_TB_ENA` | `+0x0a0` | `{0,0x80}` | `0x80` | **`0x81`** | Table 6-13 `:10443`,`:10453` — bits `63:8` and `6:0` are RES of **type X**; the manual's own type legend `:985-988` defines X as *"return UNPREDICTABLE results when read and are **ignored on write operations**"*. `0x81` differs from the accepted `0x80` in exactly one bit the hardware is documented to ignore. |
| `W_BASE0` | `+0x100` | `{0, 0x300800000}` | `0x300800000` | **`0x280000000`** | Figure 6-9 `:10556-10560` + Table 6-16 `:10562-10583` — WEN bit 33, SG bit 32, W_BASE`<31:20>`. So: WEN set, direct mapping, window base `0x80000000`, naturally aligned per `:10538-10539`, non-overlapping per `:10540-10541`. |
| `W_MASK0` | `+0x140` | `{0x700000}` | `0x700000` | **`0x100000`** | Table 6-6 `:9587`, encoding `0000 0000 0001` = 2 MB. |
| `W_BASE1` | `+0x120` | `{0x240000000}` | `0x240000000` | **`0x0`** | **S6.4.14 item 3 `:10791-10792`** — SROM *"Prevents the IOC from responding to itself by writing zero to the IOC_W_BASE1 and IOC_W_BASE0 registers"*. |
| `W_MASK1` | `+0x160` | `{0x3ff00000}` | `0x3ff00000` | **`0xfff00000`** | Table 6-6 `:9598`, encoding `1111 1111 1111` = 4 GB. |
| *control* `W_T_BASE0` | `+0x180` | *(no value guard)* | `0x100000` | — | implemented case, same switch, no predicate. |

**`wbase1 legal` is the sharpest row in the set and the one to put in front of a panel.** Zero is
not merely permitted — it is the value the manual **requires** the initialisation sequence to write,
and it is also the value the fork's own register reads back before anyone touches it. **Writing back
what you just read ends the emulator.**

**Table 6-6 has 13 legal W_MASK encodings** (derived, not transcribed:
`awk 'NR>=9586 && NR<=9598' … | wc -l` → 13). Each mask arm's predicate is a single `!=` against one
constant, so **12 of 13 are fatal at each register**, and neither register accepts the other's value.
Note `0000 0000 0000` = `0x0` is the legal 1 MB encoding, so writing zero to either mask register is
fatal too.

## 6. What made the deaths attributable

* **One process per arm.** `[A]` pre-read, `[B]` accepted store, `[C]` read-back and `[D]` the
  killing store are four guest instructions in the **same** emulator run. Between the store that
  lives and the store that dies, **only the value differs** — not the address, the width, the path
  or the process.
* **The pair is the oracle.** `0x0 -> <accepted>` from one address in one process. Unmapped space
  and a missed device both read `0` forever (`memory_rw.c`'s `#95` pre-zero), so a bare zero would
  prove nothing; **all six accepted values are non-zero**, so every `live` row carries a device
  signature as well as liveness.
* **The negative control does real work.** `W_T_BASE0` is handed `0x100000` — *the very value that
  kills at `W_MASK0`* — and stores and echoes it. That attributes the deaths to **the arm's
  predicate**, not to the value, the width, K0SEG, or writing into the IOC window at all.
* **Quadword only**, per S6.4; every access is a guest `stq`/`ldq`, never a debugger `put`/`dump`
  (`lca_ioc` is `DM_DEFAULT`, which `dump` skips). Stepped, never `continue`d.
* **`#516`'s confound is gone and was not relied on.** The ISA interrupt stubs are de-fatalised at
  `dev_lca.c:113-119`; no interrupt diagnostic appears in any log, and attribution is by text
  regardless.

## 7. Unexpected findings

**(a) Table C-3 (`:12662-12690`) is a NON-UNIFORM extraction stagger, and read naively it puts
`IOC_CONF` at `+0x40` — which is `IOC_STAT0`.** The address column is offset by one row against the
mnemonic column and there is a missing mnemonic cell partway down, so `:12667` renders as
`IOC_CONF … 1 8000 0040`. This is exactly the Figure-3.4 shape the carrier warns about: **a
calibration point taken from the top of the table certifies it, and everything below is wrong by
one.** It was not relied on. All seven offsets were taken from the **unstaggered prose** (S6.4.2
`:10231`, S6.4.6 `:10427`, S6.4.9 `:10546-10547`, S6.4.10 `:10595-10596`, S6.4.11 `:10645`), which
agrees with `alpha_lcareg.h` register for register — and the probe's attribution rows then measured
it. Three independent sources, per the carrier's straddle rule. *A future LCA round should read the
prose sections and never Table C-3.*

**(b) The store-before-check is real but is NOT observable at rung 3 today, so no row asserts it.**
Every arm does `d->field = idata;` before testing, so the refused value is already in the struct when
`exit(1)` runs — and the process ends, so no guest can read it. It becomes observable **only once
the kill is removed**, which makes it a fix-round row (*does the repair leave the register holding
the value it just refused?*), not a witness row. Recorded so the fix round does not rediscover it.

**(c) I put a wrong count in my own probe comment and corrected it before shipping.** The first
draft said "11 of 13" Table 6-6 encodings kill; it is 12 of 13. Caught by re-deriving instead of
trusting the sentence. The probe now carries the **deriver command** rather than only the literal,
and the witness was re-run on the corrected instrument — both logs are from that instrument
(md5 `b703190e…`).

**(d) No timeouts, no load sensitivity.** Two full runs; the diff between them is exactly one line,
the recorded git HEAD. Every session settled in the default `1.6s`/`2.2s` budget.

**(e) `tbena legal` MEASURES A CLAIM IN THIS ROW'S OWN FIX-DESIGN BRIEF FALSE — and the refutation
is the brief's own third row, not mine.** `FIXDESIGN_brief.md:41` records, from the codex seat:

> **`IOC_TB_ENA` is NOT a functional defect** — TEN has exactly two states and both are accepted
> (**0/2**)

Three rows above it, the same brief records — from the same seat, settling deepseek — that
**RES fields are type `X`, IGNORED ON WRITES**, and *"therefore the guards test the WHOLE 64-BIT
OPERAND while the hardware defines a … field; `0x7000ff` is functionally identical on real hardware
and ends the process."* **Applying that principle to `IOC_TB_ENA` is exactly the `0x81` row, and it
is RED.** `TODO: LCA_IOC_TB_ENA value  (0x81) has unimplemented bits.` — the host dies.

So the two rows contradict each other and the measurement settles it: **the `0/2` count is right
about the TEN *field* and wrong about the *register*.** It enumerates the field's two states and
misses the reserved-bit axis its own sibling row had already identified — the same
"count the dimension you were looking at" shape the carrier records elsewhere.

**Why this matters to the fix round rather than being bookkeeping:** carried forward unchallenged,
`0/2` licenses the round to ship **no `TB_ENA` arm and no `TB_ENA` row**, leaving a measured,
manual-backed host kill in place with a detector that is blind to it by construction. The realistic
guest path is the ordinary one: the reserved bits **read UNPREDICTABLE** (Table 6-13 `:10443`,
`:10453`; legend `:985-988`), so any driver doing a read-modify-write on `TB_ENA` can write a
non-zero reserved bit **without ever intending to**. Note also that `X` is not `MBZ` — the manual
defines `MBZ` separately at `:938-942` as raising an illegal-operand exception — so software is
positively permitted to leave these bits set.

*Count the arguments, not the seats: this is one seat's row refuted by the same seat's other row,
with a measurement deciding between them. It is offered as a finding for the fix-design panel to
adjudicate, not as a ruling from the measuring seat.*

## 8. Contract — what this witness does NOT establish

Stated so a later escape is *"outside the contract"* or *"a breach of it"* rather than an argument
about overclaiming:

* It does **not** establish that any shipped guest writes these values. It is a reachability proof,
  not a frequency claim.
* **It is a witness, not a detector.** `alive` greens equally for a silent accept, a latched
  announce, a decline that discards the value, and a full implementation. **A fix round owes rows
  that discriminate those** — at minimum a **read-back row per arm** (what did the repair do with
  the value?) and a **latch-count row** if the disposition is a bounded announce.
* The option set here is the six-member one, and **member 4 (ACCEPT) is live for at least
  `IOC_CONF`**: `dev_lca.c` already decodes `ioc_conf & 1` correctly for both cycle types after
  `#515`, so bits `<1:0>` are a two-bit field the model half-implements rather than an unserviceable
  access. `W_BASE`/`W_MASK`/`TB_ENA` are `TODO: Actually implement this` — member 3
  (**decline + latched announce**, house idiom `(once)`, N=1 per instance) is the transferable
  warrant, and `dev_lca.c`'s own `dev >= 21` arm (a commented-out `fatal()`/`exit(1)` replaced by
  `dev = 0`) is this file's in-tree graceful-degradation precedent.
* Six arms is the whole population of value-guarded arms in `lca_ioc`; the `default:` arm is a
  seventh, different kind of kill (unimplemented **offset**, not refused **value**) and is out of
  scope here.

## 9. Files written

    GXEMUL-SEC/regress/lca_badval_probe.py                                   (new)
    GXEMUL-SEC/regress/artifacts/lcabadval/witness_20260909/
        HEAD_74daefd.out                     the witness log (sentinel LCABADVAL_DONE present)
        HEAD_74daefd_run2.out                determinism replica
        lca_badval_probe.asrun.py            frozen instrument, cmp-clean vs the shipped probe
        run_witness.sh                       driver (clearance + frozen-copy check + probe)
        alpha_dummy.bin                      8 zero bytes, so the dir is self-contained
    GXEMUL-SEC/regress/artifacts/lcabadval/opus_witness_20260909.md          (this file)

Nothing else was touched. No existing file was edited; `src/`, `est/`, `build/` and `build-asan/`
were read only.
