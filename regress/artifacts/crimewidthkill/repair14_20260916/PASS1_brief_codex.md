# CRIME device-access width handling — detector coverage review (`#529`, repair 14 design)

*This is the codex-scoped variant of `PASS1_brief.md`.  It asks the same design questions in ordinary
engineering language, scopes the reading, and omits the one question §C5 records as reliably refused.
The substance is unchanged.*

## SCOPE YOUR READING

**Read only `GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/*.py`.**  Do not read `regress/artifacts/`,
`tools/pipeline/ledger.json`, or `CHANGELOG.md` — they are this project's accumulated campaign
records, they are large, and nothing in them is needed for these questions.  Every measurement you
need is inlined below.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**  There are three pristine-2021-upstream copies of
GXemul under the project root (`./src/` and two under `_archive/audit-results-*/builds/`).  They are
NOT this fork.  If your line numbers disagree with mine by hundreds you are reading one of them.

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise stated wrongly by the brief's author.
**Check the premises, not just the derivations.**  Where I state something as fact, ask whether it is
true.  A seat that re-derives a premise from something this brief did NOT give it is worth more than
a seat that agrees.

**Where this brief states an arithmetic claim — an index range, an offset, a count — ENUMERATE it
rather than reasoning about it.**  And enumerate the right DOMAIN: ask what the producer of these
values can actually emit before you walk them.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## 1. THE SUBJECT

`DEVICE_ACCESS(crime)` in `GXEMUL-SEC/src/devices/dev_sgi_ip32.c` handles guest accesses to the CRIME
system controller on SGI IP32.  A narrow access — `lb`, `lbu`, `lh`, `lhu`, `sb`, `sh` — is not
modelled.  `#529` changed that path from a terminating call into a **DECLINE**: the access is refused,
announced once behind a latch, and answered through the function's common tail.

That change shipped and is not under review.  **Under review is the regression detector that defends
it** — `GXEMUL-SEC/regress/crime_width_probe.py`, currently 188 rows — and specifically whether its
coverage matches the state space the handler actually partitions on.

The decline path and the common tail, verbatim:

```c
 296| 	} else {
 314| 		if (!(d->warned & CRIME_W_LEN)) {
 315| 			d->warned |= CRIME_W_LEN;
 316| 			fatal("[ crime: unimplemented len=%i at 0x%x -- declined."
 317| 			    "  (once) ]\n", (int) len, (int) relative_addr);
 318| 		}
 319| 		goto crime_declined;
 320| 	}
 321|
 322| 	switch (relative_addr) {
 324| 	case CRIME_REV:		/*  0x000  */
 353| 	case CRIME_CONTROL:	/*  0x008  */
 383| 	case CRIME_INTSTAT:	/*  0x010  */
 384| 	case CRIME_INTMASK:	/*  0x018  */
 388| 	case CRIME_DOG:		/*  0x030  */
 392| 	case CRIME_TIME:	/*  0x038  */
 396| 	default:
 409| 	}
 410|
 411|  crime_declined:
 414| 	d->reg[CRIME_HARDINT / sizeof(uint64_t)] = preserved_CRIME_HARDINT;
 415| 	d->reg[CRIME_INTSTAT / sizeof(uint64_t)] =
 416| 		(d->reg[CRIME_SOFTINT / sizeof(uint64_t)] |
 417| 		d->reg[CRIME_HARDINT / sizeof(uint64_t)]);
 418|
 419| 	if (writeflag == MEM_READ)
 420| 		memory_writemax64(cpu, data, len, odata);
 421|
 422| 	return 1;
 423| }
```

**The tail is COMMON and `crime_declined` is reached by `goto`.**  Worth noting because a
returning-early variant would skip both the interrupt recomputation and `memory_writemax64`.

---

## 2. THE CLAIM UNDER REVIEW — a coverage enumeration

The detector's coverage is described as a product of four factors:

> `{latch clear, latch set} × {len 4, len 8} × {read, write} × {REV, CONTROL, INTSTAT, INTMASK, DOG,
> TIME, default}` = 2 × 2 × 2 × 7 = **56 cells**, of which **23 are open and guest-visible**.  The
> disposition of the 46 ACCEPTS entries is stated as **23 rowed / 8 already-pinned / 10 equivalent /
> 5 host-diagnostic**.

**Two further factors are known to partition the same handler and are NOT in that product:**

* `relative_addr & 4` — the lane, tested at `:291` and again inside the `len == 4` arm at `:282`;
* `cpu->pc` — the PROM-window comparison at `:344`, `((uint32_t)cpu->pc & 0xffffff00) == 0xbfc05100`.

Both were examined in the previous review round and coverage was found to exist for them already.
They were therefore recorded as a **records defect** — the enumeration omitted them — rather than as
a coverage gap.

---

## 3. WHAT WAS MEASURED, so you do not have to take the enumeration on trust

Six variants of the accept path were built and scored against the shipped 188-row detector.  Each
variant adds one conjunct that makes the handler decline at ONE cell, silently, conditioned on the
latch state.  Scores (higher = fewer rows differ):

| variant | cell | score |
|---|---|---|
| TIME, latch clear | `CRIME_TIME`, 4-byte | 188/188 — **no row differs** |
| INTSTAT read, latch clear | `CRIME_INTSTAT`, 4-byte read | 188/188 — **no row differs** |
| lane at CONTROL | `CRIME_CONTROL` lane decode | 188/188 — **no row differs** |
| CONTROL write, `0x800` set, latch set | `CRIME_CONTROL`, 4-byte write | 188/188 — **no row differs** |
| the same at 8 bytes | `CRIME_CONTROL`, 8-byte write | 188/188 — **no row differs** |
| INTMASK read, latch clear | `CRIME_INTMASK`, 4-byte read | **187/188 — one row differs** (`gate line`) |
| CONTROL read, latch clear | `CRIME_CONTROL`, 4-byte read | 188/188 — believed EQUIVALENT (see below) |

**The INTMASK line is the control that makes the rest meaningful:** it shows the latch-clear state IS
observable when a row drives that cell with a value oracle.  So the 188/188 rows above mean *no row
observes that cell*, not *that cell has nothing to observe*.

**The CONTROL-read row is believed equivalent** because the session prelude writes `0x100` at `:231`,
so the high lane reads 0 either way.  That reasoning turns on the lane, not on the latch.

Three small purpose-built probes were then run.  One covers the TIME cell (2 of its 5 rows differ on
that variant).  One covers the CONTROL lane (1 of 9).  One covers both CONTROL-write cells (1 of 6
each).  **None of them covers the INTSTAT read cell** — it scores 5/5 against the TIME probe, i.e. no
row differs.

---

## 4. QUESTIONS

**Q1 — THE PREMISE AUDIT.**  Section 2 states the coverage domain as a four-factor product of 56
cells while section 2 also names two further factors of the same handler.  **Is the stated domain
correct?**  Read `DEVICE_ACCESS(crime)` and enumerate the factors the accept path actually partitions
on, from the function's own inputs.  If the product is larger than 56, say what it is and which
factors were omitted.

**Q2 — CLASSIFICATION.**  The 46 ACCEPTS entries are split **23 rowed / 8 already-pinned / 10
equivalent / 5 host-diagnostic**.  **Is an entry mis-filed?**  In particular, an entry recorded as
*equivalent* that is in fact observable would be a coverage gap wearing a disclosure's clothes.  The
CONTROL-read case above is the one I am least sure of: its equivalence argument is about the lane,
but it is being applied to a latch-state variant.  **Does that argument transfer?**

**Q3 — OPTION-SET COMPLETENESS.**  The proposed repair adds, in one change: (a) sessions that drive
each open cell with the latch CLEAR, carrying that cell's own value oracle; (b) at each CONTROL cell,
the `0x800` bit written both clear and set; (c) a contract block in the probe header naming which
cells are covered, which are equivalent with the derivation, and which are deliberately not.
**Is there a member of the option set this does not name?**  Grep `GXEMUL-SEC/regress/*.py` for how
other probes in this tree establish coverage of a state that requires a prior access to set up — the
tree's own precedents are part of the design space.

**Q4 — SHAPE.**  Part (a) proposes mirroring the existing latch-set sessions into latch-clear
equivalents, which roughly doubles the session count for those cells.  **Is the mirror the right
shape, or do some cells' two latch states collapse provably into one?**  If some collapse, say which
and give the warrant — and note that the CONTROL-read case is the template for what a collapse claim
has to look like, because it has a derivation AND a row that would differ if the derivation were
wrong.

---

If, while verifying a claim, you found something ELSE — say so.
