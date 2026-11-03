F2 VERDICT: RATIFY WITH CHANGES (4)

OPUS 5.5 seat, #578 `jazzvecdeassert`, the F2 adjudication of pass 2 and of the repair. Read-only: HEAD `50f9c601` via `git show`,
the artifacts read in place, nothing built or run against a tree. Tags: **M** = MEASURED (a command I ran), **R** = READ, **Z** =
REASONED. The deletion and the repair are right, and the repair chain may close on this pass: **zero floor breaches**, with the
denominator in Q4. The four changes are all records or a one-line driver fix. Two of them correct dispositions that adopted MY
pass-2 positions, which is where I looked hardest.

## What I checked

* **M** `_scratchpad/w578/jazz_vector_probe.py` and `killtable3_20261102/jazz_vector_probe.ASRUN.py`: both md5 7b3e17e7d3f0, `cmp`
  identical.
* **M** Every table-3 raw: score, red set and DRIVER match section 2 EXACTLY. That covers all 18 legs: base 17, fixedc 26,
  absent 0 with DRIVER=bad, M_b 17 (the same nine), and the fourteen mutants as tabulated. Every other leg reads DRIVER=ok.
* **M** Order: PRETABLE3.out 21:06:01 < base_head.raw 21:07:50. The instrument's mtime is 21:07:34, AFTER PRETABLE3. ASRUN_NOTE3.txt
  discloses the two edits that account for that (the close() flag fix, and docstring score spellings), and neither touches a row.
  This is accepted, but the record should say the predictions were written against the dry-run instrument (dryrun26/), not the
  as-run one.
* **M** Gate NEW2 vs HEAD: one block. The 26 loop names equal the 26 `row()` names. `JAZZVEC_DONE`, the DRIVER check and the
  EQUALITY pin are present.
* **M** Stub `sh v0,0(at)` = opcode 0x29 -> 0xa4220000, correct. `lbie rb` reads back 0x0f after the halfword store, which shows
  `len == 2` reached `case 2:`.
* **M** Writers of Cause, re-censused for the comment's equality claim (`git grep 'reg\[COP0_CAUSE\] *[&|]\?='`). Only
  `cpu_mips.c:1887/1892` (line assert/deassert) touch IP bits. The others are ExcCode/CE/BD and the compare bit 0x8000
  (`cpu_mips_coproc.c:828`). Nothing else clears 0x800.
* **M** OUTSTANDING_BUGS at HEAD: the six prose carriers are exactly :2037, :2509-2510, :2605, :2869, :2926 and :2965.

## Q1 -- which disposition is wrong

**1. The contract sentence built from F2/F3/F4 (my C2) overclaims, and the overclaim is mine first.** It says the other inputs
are "each driven at two or more values ... **so a re-introduction keyed to any ONE of them reds**." That holds only for predicates
that SEPARATE the driven values. My pass-2 C2 said "both polarities of both families die", and that was true only of the ==0/!=0
split. The packet now generalises it to "any one", which is false (**Z**, predicted from the row sequence, not built):

| one-input re-introduction (inserted after the #578 comment) | driven values it cannot separate | predicted |
|---|---|---|
| `if (idata & 0xff00) INTERRUPT_DEASSERT(...)` | idata in {0, 0x0f, 0x5a} | **26/26** |
| `if (d->jazz_timer_value > 0x0f) ...` | {0, 0x0f} | **26/26** |
| `if (len == 8) ...` | len in {1, 2, 4} | 26/26 if an 8-byte access reaches a 4-byte device unsplit; **not settled** (memory_rw's truncation path decides) |

The first one is the guest-visible one. If OpenBSD's `out16(PICA_SYS_LB_IE, mask)` sets bits for lines 8 and up (local line *n*
-> bit *n*), every LB_IE write that enables a UART line would drop IRQ3. Whether OpenBSD's mask has high-byte bits is **not
checkable here**: the OpenBSD arc `jazzio.c` source is not in this tree. The settling fact is that driver's LB_IE values.

**Grade: clause (e), not floor.** `idata`, `len` and `jazz_timer_value` are not tested by the body, so D2's reasoning holds.
**But the sentence is an L4 wrong record**, a coverage claim that a construction refutes. Correct it in place with the carrier's
7n-5 vocabulary: idata SAMPLED at {0, 0x0f, 0x5a}, len at {1, 2, 4}, jazz_timer_value at {0, 0x0f}. Then say a re-introduction
keyed to a predicate that separates those values reds, and one that does not (examples above) is disclosed. Optionally, store
`0x10f` instead of `0x0f` in lbiew: one constant closes the `& 0xff00` slice, and that byte still reads back 0x0f. That re-runs
table 3 (~90 s), and nothing is owed. **(Change 1.)**

**2. F12 is right to keep "cause not established", but the check it names cannot settle it, and that error is mine too.** My
addendum suggested `strings ... "line 71"`. **`FAILURE()` passes `__LINE__` as an `int` argument to `snprintf`** (`misc.h:181-184`:
`"%s, line %i, function %s().\n"`). The line number is an instruction immediate, not a string, so `strings` on any pair of binaries
is blind to it. The discriminator is: build HEAD plus a COMMENT-ONLY insertion of the same number of lines above `:712`, change no
code, and compare md5. If it differs, line shift is the cause. Alternatively, `objdump -d` the two `dev_jazz.o` and look for a
single changed immediate. **(Change 2: correct F12's named check.)**

**3. D3's line is right in KIND, and its census is one seat's recollection.** "Row the conjunctions the real guest exercises" is
bounded, by the reference driver's access shapes, which is the right bound against the unbounded alternative. But nobody derived
those shapes from the driver. `jz ip vecb` rows `inb(PVIS)` because Grok remembered it. **A second candidate the same rule would
row, if it is real: an `in16` READ of LB_IE** (read-modify-write in `pica_intr_establish`). Its escape is
`if (len == 2 && writeflag == MEM_READ) ...`, predicted **26/26** (**Z**: the only offset-2 read is `ld8`). **Not settleable
here**, for the same missing-source reason. Ruling as I would write it: UPHOLD D3's line; record that the census is unverified; if
the driver does an `in16`, add an `lhu` (0x94220000) row at VEC+2. **(Part of change 1's contract wording.)**

**4. F19/F8: "it can only false-FAIL" has one hole (**R**, from the driver).** `Emu.__init__` calls `self.wait(timeout=30)` and
discards the result. If the startup prompt arrives after 30 s, it lands after the first command's mark. Every later `send()` then
returns one prompt early, with no timeout, so `bad` is never set. In practice a desynchronised run will not score 26/26, and the
EQUALITY pin catches it, so this is low. The fix is one line: `if not self.wait(timeout=30): self.bad = True`. **(Change 3.)**

The other dispositions I UPHOLD as written. In particular: F1 (the default-write cell is body-distinguished in the `default:` arm's
read/write `fatal()` texts; M_dfltw 24/26 **M**); F5/F6; F7; F10 (est's three writers, read at pass 2); F11; F13-F15; F17; F18;
F20-F23. F16: UPHOLD with one note. The derived index at `:24266/:24273/:24281` also names OB-22, mapping old line numbers, and
the landing should leave it consistent. **(Part of change 4.)** D1: UPHOLD Opus's wording, because a tick re-asserts a line.
D2: UPHOLD (debt), with change 1's wording.

## Q2 -- the floor, asked of the shipped composite

**No floor breach found (Z, backed by M rows).** The body-tested partitions are three:
* `relative_addr` {0, 2, default}, from the switch;
* `writeflag` {R, W}, tested inside `case 2` and `default`;
* in `case 0`, the scan over `int_asserted`, {nothing pending, lowest line *i*}.

The six label x writeflag cells are each rowed with lines pending, and each one's single-cell re-introduction is MEASURED red:
* (0,R) M_offs0 / M_rd / M_vecb;
* (0,W) M_offs0 / M_wr;
* (2,R) M_offs2 / M_rd;
* (2,W) M_offs2 / M_wr / M_len2;
* (default,R) M_offsne0 / M_rd;
* (default,W) M_dfltw / M_off3.

For the scan partition, {none, 8, 9} are rowed (`vec none`/`nt`, `vec`, `vec com1`/`onevec`), and lines 0-7 and 10-14 are
disclosed (M_uart 26/26 **M**). There is no guard (pure deletion), so clause (d) is the re-introduction family above.

**Smallest guest-visible escape I can name: `if (idata & 0xff00) INTERRUPT_DEASSERT(d->mips_irq_3);`, predicted 26/26.** It is
clause (e) by D2's grading, FILE. Runner-up: `if (len == 2 && writeflag == MEM_READ)`, 26/26, clause (e), FILE (and ROW if
OpenBSD reads LB_IE with in16, per D3).

## Q3 -- the shipped comment (1a)

**True as written (Z + M).**
* "on every access": the rows show it at all six cells on HEAD (base_head red at after/vecb/vecw/lbie/lbiew/dflt/dfltw).
* "until a line was asserted anew or EXT_IMASK re-enabled IP3": "re-enabled" correctly implies a false-to-true transition, and a
  same-value write heals nothing, as stated.
* "kept equal to 'a line 0-14 pending and EXT_IMASK.IP3 set'": 0x7fff is lines 0-14. The census above finds no other writer of
  Cause bit 0x800, and the state starts equal (memset, line low).
* "an access to this register no longer touches it": true.
* It makes no claim about other controllers.

One nit, no change owed: "dropping a level interrupt" is HEAD's behaviour. The tense reads right only because "used to" governs
the whole sentence.

## Q4 -- does the chain close?

**Yes: zero floor breaches, on a valid pass** (the diff was delivered, the raws were readable, and the roster is named in the
packet). **Denominator:**
* **Cells:** 6 label x writeflag cells, with 2 default offsets inside the default cell, plus 3 scan-partition classes rowed
  (0-7 and 10-14 disclosed).
* **Measured shapes:** the 14 re-introductions in table 3, which red as tabulated except the two disclosed equivalents
  (M_cond, M_uart).
* **Reasoned shapes beyond the table:** 6 one-input predicates (`idata & 0xff00`, `idata == 0x0f`, `jazz_timer_value > 0x0f`,
  `len == 8`, `int_enable_mask & IP4`, `odata == 0x28`), and 2 two-input ones (`len == 2 && R`, `len == 2 && relative_addr == 0`).
* **Result of the reasoned shapes:** `idata == 0x0f` reds lbiew; `odata == 0x28` reds onevec. All the others escape, and all of
  them are outside the body-tested partition, so they are disclosed or to be filed, not floor.

What does NOT close is change 1's L4: it is a records correction in place and does not reopen the chain.

## Changes

1. Contract: replace "so a re-introduction keyed to any ONE of them reds" with the SAMPLED/EXHAUSTED statement and its
   non-separating examples; note D3's census is unverified and name the possible `in16` LB_IE read. Optionally lbiew `0x10f`.
   File `idata & 0xff00` with its predicted 26/26.
2. F12: the settling check is a comment-only N-line rebuild compared by md5 (or an `objdump` immediate diff), never `strings`.
   `__LINE__` is an int immediate.
3. Driver: set `bad` when the startup prompt times out.
4. Records: the predictions were written against dryrun26/'s instrument (disclosed in ASRUN_NOTE3, so say so in the round block);
   keep the OB-22 index lines :24266-24281 consistent with the six carriers.

**What I could not settle:** OpenBSD arc's LB_IE write values and whether it reads LB_IE at 16 bits (the source is not in this
tree); and whether an 8-byte access reaches `jazz_jazzio` with `len == 8`.

F2 VERDICT: RATIFY WITH CHANGES (4)
