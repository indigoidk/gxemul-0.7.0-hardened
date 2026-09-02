# FABLE ADJUDICATION — 2026-09-02, first firing after the owner's hold expired

**Seat:** Agent tool, `model: "fable"`. Liveness token returned: `FABLE_SEAT_ALIVE_20260902`.
**Model version, self-declared per standing requirement:** `claude-fable-5`.
**File access proven:** it quoted a verbatim line from `_scratchpad/CHECKPOINT.md` and
confirmed HEAD `80cab9e` matched the checkpoint's own stamp.

*Rows adjudicated: `pcc2widthkills` (sev high) and `sgitexindex` (sev low), both HELD for
this seat by owner directive since 2026-08-31.*

---

## VERDICT LINE (verbatim from the seat)

> `pcc2widthkills` — DO NOW, FIRST: direction split YES (reads ACCEPT, writes decline +
> per-instance `(once)` latch), addition licence SATISFIED by the `#497` sgi_re exemplar,
> not by `#119`; `sgitexindex` — DO NOT CODE and DO NOT DROP: close DOCUMENTED-ONLY
> (`witness: none — no consumer, no channel`), reopen condition named; six-window single
> round REFUSED (multi-class bundle). And the brief carries the predicted wrong premise:
> its reachability framing is refuted by the project's own record — `OUTSTANDING_BUGS.md`
> measured HALF the ten kills guest-unreachable two days before this brief was written.

---

## THE THREE FRAMING ERRORS IT WAS ASKED TO FIND — ALL THREE MINE

### F1 — the reachability claim, and it was refuted by my own records

I wrote *"TEN live width kills"* and *"reachability is evidenced end to end."*
`OUTSTANDING_BUGS.md` § `widthkillclass` (2026-08-30, from a farmed codex run, mechanism
verified) says: **"It is now checked: 5 of the 10 width anchors are guest-reachable."**

An aligned non-byte m88k access can never carry an **odd** `relative_addr`, and
`%= PCC2_SIZE` (0x40) keeps odd offsets odd across all 64 aliases. So:

* **REACHABLE (5):** GENCTL `0x02`, T2CTL `0x16`, T2ICR `0x1a`, SCCERR `0x1c`, SCCTX `0x1e`
* **UNREACHABLE BY CONSTRUCTION (7):** VECBASE, PSCALEADJ, T1CTL, T1ICR, SCCICR, SCCRX,
  SCSIICR

**Verified here by opening the file before accepting it.** The row stays HIGH — the GENCTL
halfword kill is real and live — but a round record claiming ten guest-reachable kills
would be a WRONG RECORD, and the seven unreachable arms must be recorded as *reachability
refuted at OB:widthkillclass*, never left as blanks.

> *** THE FACT WAS FILED TWO DAYS BEFORE I WROTE THE BRIEF, IN THE FILE I APPENDED TO THE
> SAME NIGHT. ***  This is the carrier's grep-your-own-findings rule failing in practice: a
> warrant checked only against the facts in hand, defeated by a fact already held under a
> different label.

### F2 — the sibling-symmetry warrant is weaker than I framed it

My brief asked only *"does anything read `re_tex`?"* (it does not — 3 references, all
declaration, write and debug print). The companion fact I omitted: **the three sibling TLB
arrays ARE read** — `tileptr = d->re_tlb_a[tile_nr] << 16` at `dev_sgi_re.c:202`, with a
consumer-side bound above it. Verified here.

So the siblings' `>> 1` is **load-bearing** while TEX's scale governs **write-only state**.
*"Make TEX match its siblings"* is consistency among stores only one of which anyone
consults.

### F3 — "two dispositions" undercounted, and the strongest ACCEPT warrant went unstated

The file already holds **four** width dispositions: the timer block accepts wide writes by
`memcpy`; SCCRXIACK ignores `len` entirely; `#119`'s IPL/MASK decline; and — decisive —
**wide reads spanning GENCTL/VECBASE are ALREADY ACCEPTED today when the base offset lands
on an unchecked arm.** A word read at `0x00` (CHIPID) returns those same bytes through the
top-of-function `memcpy` with no kill.

> **The identical bytes flow or kill depending only on which case label the base hits.**
> The read-side kill defends nothing that is not already served one offset away. That is a
> stronger argument for the split than the one I gave the panel.

---

## ROW 1 — `pcc2widthkills`: DO NOW, FIRST IN QUEUE

**Q1.1 direction split — YES.** Verified by the seat: the `memcpy` serves every read before
the switch; **no arm computes a read value**; arms `break` to `return 1` with no common read
tail, so the sketch-rule early-return hazard does not apply here. Writes land only inside
arms, so a write decline is honest.

* **READS:** delete the kill, keep the value, **no latch** — there is no event to announce.
* **WRITES:** decline + latched announce.
* Apply one edit shape to all ten arms; the contract states the 5/7 reachability split.

**Q1.2 addition licence — SATISFIED, citing the right warrant.** Not `#119`'s function
statics. The in-tree exemplar for this exact shape is `dev_sgi_re.c`'s per-instance
`d->warned & SGIRE_W_*_LEN` bitfield with the `(once)` marker, shipped and panel-reviewed
across `#497`–`#500` — same defect class, same message shape.

> **Minimax's single-instance objection is real and INVERTED.** Single-instance means
> field-vs-static has **zero measurable delta**, so the licence cannot prefer the static —
> and the tiebreaker is that every new `static` adds two rows of filed `staticlatchscope`
> debt while a field adds none. Single-instance is also a **layout fact, not an
> invariant**: one `device_add` today, and multi-machine configs are legal.

**Deepseek's convert-the-`#119`-statics — NO.** That is `staticlatchscope`'s scope;
converting here widens the diff into unreviewed code for zero measured benefit.

**Witness note from the seat:** a rung-3 cold-debugger probe on mvme187 is **buildable** —
a planted m88k halfword load at `0xfff42002`, pre-fix symptom process exit, with VECBASE's
nonzero reset (`0x0f`) as the device-signature control.

---

## ROW 2 — `sgitexindex`: close DOCUMENTED-ONLY, `witness: none`

`re_tex` has **no consumer** — checked, three references, all declaration/write/debug. No
consumer means no observable, hence no witness above rung 1, and test-first says a defect
with no witness is **documented, not coded**. A detector row could only pin a
verbosity-gated `debug()` line defending write-only state — the "cannot hurt" accretion the
addition licence exists to refuse.

**But deepseek's DROP goes one step too far.** The decode inconsistency is a true record,
and the proposed `>> 1` "fix" would **import the siblings' debugger-path overrun** (TEX
under `>> 1` overruns `re_tex[112]` by 1–3 at `0xda`–`0xdf`; the brief's arithmetic and its
31-of-112 reachable figure both verified exact).

> **REOPEN CONDITION, named:** the first round that gives `re_tex` a consumer inherits the
> scale question and settles it **against that consumer's expectations, not by sibling
> analogy.**

**Q2.1 six-window single round — REFUSED.** It bundles at least three semantic classes
(read-exit de-fatalisation, index scale, OOB bounds), which the round-scope rule forbids.
The file's own comment already partitions those windows across named rows: `sgirekills`
(high, open), `sgireunmapped` (closed), `sgilinearoob` (med, open), `sgidewidth`,
`sgirelatchenum`.

> *The class closure the `#500` chain mandates is about ONE DETECTOR'S REPAIR CHAIN, not
> about bundling distinct defects — a distinction my brief had blurred.*

---

## A QUEUE GAP IT FOUND ON NO OPEN ROW AT ALL

`dev_pcc2.c`'s `default:` arm `exit(1)`s on any unimplemented offset — **killing reads the
`memcpy` had already served**, which is the ACCEPT shape again. Prose-deferred since the
nineteenth round and carried on **no open ledger row**. Different predicate class (offset
decode, not width), so it cannot join this round — but without a row, the round's contract
has nothing to point at when it declines to claim wide pcc2 reads are safe.

## RANKING

1. **`pcc2widthkills`** — live host death by an ordinary aligned halfword load.
2. **`sgirekills`** (high, open) — named for honesty, not scheduled here: the six RE read
   arms are the same live-kill severity and the natural next round.
3. **`sgitexindex`** — not scheduled; documented-only closure.

## WHAT IT FLAGGED RATHER THAN ASSERTED

Whether any real mvme187 driver performs the wide **writes** the decline will refuse.
OpenBSD/mvme88k writes timer and SCC registers bytewise in the sources it knows, and the
timer block already accepts wide writes — **"but that is a reading, not a measurement"**,
and the round owes an answer.
