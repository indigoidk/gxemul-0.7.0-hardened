# RATING PASS — 15 open ledger rows that carry a WITNESS and NO SEVERITY

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Eight briefs of mine this week stated premises that
were false or too broad. On the most recent panel I stated a weakened premise about `#95` as
*settled*; three of six seats confirmed it and **one seat opened the file and refuted it** — the
refutation was right. **Where a claim below rests on a search or a title, ask what it would miss.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies of GXemul sit
under the project root and are NOT this fork; a seat reading one reports line numbers off by hundreds.

**SCOPE:** `GXEMUL-SEC/src/`, `GXEMUL-SEC/regress/*.py`, and
`GXEMUL-SEC/tools/pipeline/ledger.json` (the rows named below are in there, each with a
`state_note` carrying its evidence).

**VERDICT LINE FIRST.**

---

## §C — SETTLED PREMISES

**S1 — the gap, derived not guessed.** Of 187 open/in-work ledger rows, **87 carry no `sev` field at
all**, and **73 of those 87 already carry a witness**. Derive it yourself:

```python
op = [r for r in L['rows'] if r.get('state') in ('open','in work')]
un = [r for r in op if not r.get('sev')]
wit = [r for r in un if r.get('witness') and r.get('witness') != 'none']
```

**S2 — why that matters here.** This project's ordering rule is: *a witness makes an item ELIGIBLE;
rung is a floor on admissibility, never a priority; **SEVERITY and gate blind-spots order the
queue***. So an unranked witnessed row is invisible to the only ordering rule the project has.

**S3 — the severity vocabulary in use** is `high` / `med` / `low` in the `sev` field (lowercase). For
calibration, four rows currently rated `high`: a device with twelve live `exit()` calls reachable from
guest writes; a legal one-byte guest write that ends the process; a page-table walk returning a wrong
PFN; an exception path that stops every guest CPU.

**S4 — I DID NOT RATE THESE MYSELF, DELIBERATELY.** I wrote a keyword scan over titles and then
rejected its output as a **correlate**: what makes a row severe here is *a guest can reach it and
something bad happens*, and no keyword tests reachability. The list below is therefore a **READING
ORDER, not a grading**, and it may well be wrong about which rows deserve attention.

---

## The task

For **each** row id below: read its `state_note` in the ledger, then **read the source it names** and
answer three things.

1. **`sev`: high / med / low** — and say which of the two axes drives it: **guest reachability** and
   **consequence**. A row a guest cannot reach is not high however bad the consequence.
2. **A ONE-SENTENCE WARRANT quoting the source**, with file and a grep-able anchor (not a bare line
   number — same-file line numbers here go stale from the round's own edits).
3. **Whether the row's own `witness` actually supports it.** Several claim `probe:` or `harness:`
   witnesses; this project has twice found a witness that witnesses a *different path* from the one
   the row describes.

### The rows

**Product-code candidates (my scan put these first — challenge the ordering):**

```
gdromcondavail    COND_DATA_AVAIL permanently lies after an overread
asicindexcase     a deleted guard was ALSO a bounds check, so an indexing path is now unchecked
gdrompiooddlen    the GDROM PIO read guards ONE byte and then reads TWO
asickillsurvive   #463's four kill rows are SURVIVE-ONLY, so an OOB read is unobserved
gdromdmawidth     the DMA tail store ignores `len`
sh4pcic15         PCIC interrupt line 15 can never be delivered
asicpermute       `(relative_addr / 4) % 3` permutes the ASIC register index
asiceventaddr     SYSASIC_EVENT_TO_ADDR is correct only for e in [0,95]
wdcflood          wdc_command()'s default fatal() is unlatched
wdcperopcode      the unimplemented-command latch is per-DEVICE, not per-opcode
gdromallocpair    alloc_data() does not release before it allocates
pitclobber        an 8253 LATCH command clobbers the counter's programmed RW mode
shprotld          every SH TLB row runs privileged, so READ-side protection is untested
asicarray4        sizing the ASIC's four register arrays [4] instead of [3]
sh4frqcr          FRQCR is a bare latch with no reset value
```

## The questions

**Q1 — WHICH OF THESE FIFTEEN IS THE MOST SEVERE, and is any of them `high`?** I am not asking for a
ranking of all fifteen; I am asking which ones clear the `high` bar in S3's calibration, and why.

**Q2 — WHICH ARE NOT DEFECTS AT ALL?** This project has withdrawn two findings this week after a seat
read three lines above the quoted code (an `unsigned` declaration that made a whole negative-index
analysis void). **Assume at least one of these fifteen is like that and find it.**

**Q3 — WHAT DOES MY READING ORDER MISS?** The scan bucketed by title keywords. **Name any row in the
73 that my ordering demotes and should not** — you can enumerate them from the ledger with the S1
snippet. A row whose title sounds like harness plumbing but whose note describes a guest-reachable
defect is exactly what a keyword scan drops.

**Q4 — IS `sev` EVEN THE RIGHT AXIS?** The project orders by *severity and gate blind-spots*. If some
of these are better ordered by "no gate would ever catch this", say so and name them.

## What I am not asking

Do not write a patch, do not edit the ledger, and do not run builds, gates or probes. **Nothing ships
until the flagship adjudication on 2026-09-09** — this pass exists to make the queue orderable, not to
authorise work.

**If, while verifying a claim, you found something ELSE — say so.**
