# sgirekills STEP 1 -- the RE-PIN.  Design the rows BEFORE the code changes.

**PLEASE DO NOT RATIFY.**  Every round I designed alone this session had a hole a panel found
afterwards -- twice a floor-shaped one I had graded as debt.  **This brief exists so the hole is
found before the rows are written**, so the useful reply is the weakness, not agreement.

**Tree: `GXEMUL-SEC/`.**

---

## 0.  READING SCOPE

**Please read only `src/` and `regress/*.py`.**  Do not read `regress/artifacts/`,
`tools/pipeline/ledger.json`, `CHANGELOG.md` or `OUTSTANDING_BUGS.md` -- they are this project's
own archive of a hardening campaign and are not needed for this question.  Everything required is
inlined below.


## 1.  WHAT THIS IS

Six RE read arms in `dev_sgi_re.c` end the host on a legal 8-byte `ld`.  The round is SANCTIONED
(2026-09-02 flagship adjudication: *"the natural next round"*), scoped to ONE class -- read-exit
de-fatalisation.  **FIVE arms become ACCEPT** (TLB_A/B/C, LINEAR_A/B); **TEX becomes a latched
DECLINE**, because its index repair is under a standing DO-NOT-CODE.

**THE ORACLE-CORRECTION RULE FIXES THE ORDER:** re-pin the rows FIRST, measure the COMMITTED build
RED under the new expectations, and only then edit.  **This is step 1; no code has changed.**

## 2.  THE ROWS AS THEY STAND -- one loop, six rows, all wanting death

```python
 266| # ------------------------------------------------ contract / non-regression
 267| #  THE LEFTOVER, MEASURED AT EVERY WINDOW rather than argued from the pairing:
 268| #  len == 8 passes the width guard and reaches the still-live read kill.
 269| for nm, base, sym, _a in SITES:
 270|     A = Addr(CODE)
 271|     t, alive, how = session(load(A, base, OP_LD_V0_AT))
 272|     ok_txt = ("TODO: read from " + sym) in t
 273|     row(nm + " ld kill", how + ("+txt" if ok_txt else "-txt"), "exit1+txt",
 274|         "len=8 READ STILL KILLS THE HOST here -- untouched (sgirekills)")
```

## 3.  THE HELPERS, all already in the file

```python
 180| def run_ops(ops, at):
 181|     put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
 182|     put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
 183|             "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, OP_NOP)]
 184|     return put + ["pc=0x%x" % at, "step %d" % len(ops)]
 185| 
 186| def store(A, addr, op=OP_SW_T0_A3, val="0x12345678"):
 187|     return ["a3=0x%x" % addr, "t0=%s" % val] + run_ops([op], A.take(1))
 188| 
 189| #  THE DESTINATION REGISTER IS PRESET TO A SENTINEL, NOT TO 0.
 190| #  Preset to 0 the row cannot tell "the common tail ran and wrote odata (0)"
 191| #  from "the load never completed at all" -- both leave v0 == 0.  With a
 192| #  sentinel the two separate: a declined read that reaches the tail yields 0,
 193| #  and a read that faulted or never landed yields the sentinel.
 194| SENTINEL = 0xdeadbeef
 195| 
 196| def load(A, addr, op=OP_LW_V0_AT):
 197|     return ["at=0x%x" % addr, "v0=0x%x" % SENTINEL] + run_ops([op], A.take(1))
 198| 
 199| print("#497 widthkillclass DETECTOR -- binary=%s label=%s" % (BIN, LABEL))
```

Plus `ACC_VAL = "0x1122334455667788"` -- chosen so **every halfword lane is load-bearing**;
`OP_SD_T0_A3` (8-byte store) and `OP_LD_V0_AT` (8-byte load).

## 4.  THE ARM UNDER TEST (TLB_A; _B/_C identical, LINEAR noted below)

```c
 420| 	if (relative_addr >= CRIME_RE_TLB_A && relative_addr < CRIME_RE_TLB_B) {
 421| 		if (len != 8) {
 422| 			if (!(d->warned & SGIRE_W_TLBA_LEN)) {
 423| 				d->warned |= SGIRE_W_TLBA_LEN;
 424| 				fatal("[ sgi_re: unimplemented len=%i for "
 425| 				    "CRIME_RE_TLB_A -- declined.  (once) ]\n",
 426| 				    (int) len);
 427| 			}
 428| 		} else if (writeflag == MEM_WRITE) {
 429| 			int tlbi = ((relative_addr & 0x1ff) >> 1) & 0xff;
 430| 			for (size_t hwi = 0; hwi < len; hwi += sizeof(uint16_t)) {
 431| 				d->re_tlb_a[tlbi] = data[hwi]*256 + data[hwi+1];
 432| 				debug("d->re_tlb_a[%i] = 0x%04x\n", tlbi, d->re_tlb_a[tlbi]);
 433| 				tlbi++;
 434| 			}
 435| 		} else {
 436| 			fatal("TODO: read from CRIME_RE_TLB_A\n");
 437| 			exit(1);
 438| 		}
```

**The store packs FOUR BIG-ENDIAN HALFWORDS per 8-byte access**, incrementing the index once per
halfword.  LINEAR_A/B are `uint32_t[32]` and pack TWO WORDS.  An ACCEPT read must return the inverse
of that loop.

## 5.  WHAT `#499` ALREADY MEASURED ABOUT ORACLES HERE -- do not re-derive it, ATTACK it

Its `other decl` row pins THREE channels, and its comment records the alternatives it measured
VACUOUS:

* **SURVIVAL ALONE IS VACUOUS.**  Reinstating the death as `exit(0)` prints the announce and then
  dies; the survival+text oracle scored GREEN with the process dead.  Filed as `exit0oracle`.
* **A WRITE-ONLY oracle misses two mutants:** `return 0` (which `memory_rw.c` coerces to -1, raising
  a bus error) and `exit(0)` placed in the READ branch only.
* **The destination register is preset to a SENTINEL, not 0**, precisely so *"the common tail ran
  and wrote odata (0)"* and *"the load never completed"* are distinguishable.
* A TEXT channel must be **ONE CONTIGUOUS literal** including the address and data fields: the bare
  phrase cross-matches six other width declines and one from a different device.

## 6.  MY PROPOSED RE-PIN -- attack this

Five ACCEPT arms: store `ACC_VAL` at the window base, load it back, want the packed value.
TEX: survival + the contiguous decline literal + a defined zero.

## 7.  QUESTIONS

**Q1 (THE ONE I KNOW IS WEAK).  A same-address store-then-load tests the DECODE AGAINST ITSELF.**
This project's anchor rule says such a row is invariant under any INJECTIVE re-map of the probed
set -- a translation slides every cell and the round trip still passes.  **What is the cheapest
ANCHOR?**  Candidates: read back at a DIFFERENT offset than the store; key on the store's own debug
line, which names the INDEX; or store at two offsets and require no collision.  **Which actually
pins position, and which merely looks like it does?**

**Q2.  How many rows per arm, and where?**  The far-bound rule says an accept row at a window's BASE
tests the near bound twice and the far bound never.  Five arms x two bounds is ten rows on top of
the existing 35 -- **is that the right cost, or does an anchored form make one row enough?**

**Q3.  What does the TEX decline row need that the `#499` template does not already give it?**  Its
ACCEPT is the only one barred, so it is the arm most likely to be re-opened later -- what should the
row assert NOW so that a future ACCEPT round REDDENS it rather than silently replacing it?

**Verdict line first** -- the row set you would write -- then the body.  **A verdict that merely
agrees is the least useful reply.**
