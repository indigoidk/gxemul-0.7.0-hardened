# PASS-2 DIFF REVIEW -- research item T18, ledger row `lecsrmask`, round `#573` (tentative) -- GXemul hardened fork

Written 2026-10-25 05:3x by the main loop.  PASS 2: the review of the REAL DIFF and the REAL measurements, after pass 1
(`pass1_20261025/packet.md`), its corrections (`PASS1_CORRECTIONS.md`) and its adjudication (`PASS1_RULINGS.md`; the
F2 packet `f2_20261025/F2_PACKET.md`, Astra's `codex_t18f2.txt` the ruling of record: RATIFY WITH CHANGES, WRONG: D2, F22).
Tree under review: `GXEMUL-SEC/src/` at HEAD `2956c32d`.  **The product edit exists only in a scratch clone and a scratch
copy; nothing is committed and the working tree's `dev_le.c` is still HEAD's.**

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

Pass 1 of this round stated two premises wrongly and the seats caught both; its adjudication overturned two of the main
loop's dispositions.  **Check the premises, not just the derivations.**  **The tree under review is `GXEMUL-SEC/src/`**
(three pristine-2021-upstream copies sit under the project root).  **If you cannot read files that is expected** -- the diff,
the detector's row table and every measurement are inlined; name any premise you cannot settle rather than guessing.
**VERDICT LINE FIRST.**  Nobody is asked to write a guest program, a probe or a code variant; the variant classifications
of the F2 packet (4.3) stand as the seats left them and are NOT re-asked here.

**Reading scope (file-reading seats):** `GXEMUL-SEC/src/`; `GXEMUL-SEC/regress/*.py` and `*.sh`; under
`GXEMUL-SEC/regress/artifacts/lecsrmask/`: `witness_20261025/`, `floor_20261025/`, `killtable_20261025/` (PRETABLE.out,
README.txt), `pass1_20261025/` (the brief, the seven pass-1 answers, PASS1_CORRECTIONS.md, PASS1_RULINGS.md, `f2_20261025/`
with its packet and five answers, `final_045716/` -- this pass's measurements and the frozen final probe); the manuals by
absolute path `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\lance\TM1986.txt`, `...\am79c90_bitsavers.txt`.  Do not read the
other `regress/artifacts/` directories, `tools/pipeline/ledger.json`, `CHANGELOG.md` or `OUTSTANDING_BUGS.md`.  **Do not
read `pass2_20261025/` beyond this packet -- the other seats' answers to it land there.**  Do not build or run anything.

**Roster:** GLM 5.3 and DeepSeek (packet-fed, two firings: Q1+Q2, then Q3+Q4), Grok 4.7 (file-reading), GPT-6 Astra
(file-reading; it ADJUDICATES this pass afterwards), Gemini 4 Argon: **SEAT FAILURE for this pass unless its meter refills**
(the agy transport is quota-walled for ~5 days; the web route's meter read 0.0% at 04:45 after the pass-1 firings), recorded
by name.  Fable 5.1 HELD (its question, superseded by the narrowing, is in `FABLE_HOLD_QUESTION.md`).  kimi, minimax and
the Opus seat deliberately not fired.

**Answer format -- VERDICT LINE FIRST:**
~~~~
VERDICT: SHIP | SHIP WITH CHANGES | DO NOT SHIP -- <one line>
Q1: <one line>   Q2: <one line>   Q3: <one line>   Q4: <one line>
~~~~
Mark claims READ / DERIVED / NOT CHECKABLE.  Cite hunks H1-H2, rows N1-N20, legs L0-L3, rules by name.

---

## 1. What changed since pass 1 -- the design as ruled (PASS1_RULINGS.md, abridged)

* **CSR3 only.**  The store of CSR3 is masked `& 0x0007` (both AMD manuals: TM1986 1734 "Reserved and read as 0", the
  C-LANCE 1222-1223; MAME's `CSR3_MASK`).  **CSR1 and CSR2 retain the model's existing behaviour (stored whole)** -- the
  Am7990 manual leaves their read-back unspecified ("Must be zero" 1749; bare "Reserved." 1695), MAME keeps both writable
  on the Am7990 for a board diagnostic's sake, the C-LANCE text reads CSR2's reserved bits as zero and says only "Must be
  zero" for CSR1 bit 0.  An interpreted reading, recorded as one; the CSR1/CSR2 read-back question is FILED
  (`lecsr12readback`) with both readings.  The research row's "port rpajarola e108b54" (all three masks) is therefore
  NARROWED: his masks are C-LANCE semantics for a 3MIN port this fork does not carry, with no chip named.
* **Form A** (an explicit `case 3:` arm; CSR1/CSR2 stay in `default:` with a comment saying this MODEL stores them whole,
  not that the Am7990 does).
* **The odd-address warning at `le_chip_init` 180-182 stays** (CSR1 unmasked, so it is reachable).
* **Both STOP comments in `DEVICE_ACCESS(le)` corrected as L4 records** (same file, not the same function): the manuals
  say CSR1-3 are accessible only while STOP is SET; the old comments said the opposite; the model's acceptance of either
  state is unchanged and filed (`lestopgate`).
* **The detector**: 20 rows; three SYMPTOM rows on CSR3 (`csr3 all` 0xffff->0x0007, `csr3 hi` 0x0008->0x0000, `csr3 mix`
  0x0015->0x0005), one kept row (`csr3 bits` 0x0005), three CONTRACT rows pinning CSR1/CSR2 stored-whole at identity wants
  (`csr1 all` 0xffff, `csr1 odd` 0x1235, `csr2 all` 0xffff), `csr2 lo`, `csr1 even`, `csr1 top` (insurance), the two
  signature rows, four liveness rows, four stable rows.  The park control verifies the breakpoint pc.  A red CONTRACT row
  fails the leg but not CONTROL.  Floor: labels are the floor siblings (D2 overturned); kept/dropped coverage is contract
  (clause e).  Clause (d) variant table: OWED (`killtable_20261025/README.txt`); clauses (a) (b) (c): measured (section 3).

## 2. THE DIFF -- `src/devices/dev_le.c`, HEAD `2956c32d` -> the patched copy (VERBATIM, `diff -u`; 2 hunks, 35 changed lines)

```
diff --git "a/C:\\DocumentNoSnc\\cc\\GXEMUL\\GXEMUL-SEC\\src\\devices\\dev_le.c" "b/C:\\DocumentNoSnc\\cc\\GXEMUL\\GXEMUL-SEC\\regress\\artifacts\\lecsrmask\\pass1_20261025\\final_045716\\dev_le.c.fix.txt"
index 1155aeb5..a1a51ffe 100644
--- "a/C:\\DocumentNoSnc\\cc\\GXEMUL\\GXEMUL-SEC\\src\\devices\\dev_le.c"
+++ "b/C:\\DocumentNoSnc\\cc\\GXEMUL\\GXEMUL-SEC\\regress\\artifacts\\lecsrmask\\pass1_20261025\\final_045716\\dev_le.c.fix.txt"
@@ -881,8 +881,25 @@ void le_register_write(struct le_data *d, int r, uint32_t x)
 		d->reg[r] |= (x & LE_INEA);
 		break;
 
+	case 3:
+		/*
+		 *  #573: CSR3 is BSWP|ACON|BCON; bits 15:3 are "Reserved and read
+		 *  as 0" (Am7990 Technical Manual, 1986, p. 1-22; the Am79C90
+		 *  datasheet says the same).
+		 */
+		d->reg[r] = x & 0x0007;
+		break;
+
 	default:
-		/*  CSR1, CSR2, and CSR3:  */
+		/*
+		 *  CSR1 and CSR2 are stored whole.  The Am7990 manual leaves their
+		 *  read-back unspecified (CSR1 bit 0 "Must be zero", CSR2 bits 15:8
+		 *  "Reserved" -- constraints on the host's writes); the later Am79C90
+		 *  (C-LANCE) reads CSR2's reserved bits as zero and says no more
+		 *  about CSR1 bit 0; another emulator keeps both writable on the
+		 *  Am7990 for a board diagnostic's sake.  An interpreted reading,
+		 *  recorded as one: see the #573 record.
+		 */
 		d->reg[r] = x;
 	}
 }
@@ -984,20 +1001,20 @@ DEVICE_ACCESS(le)
 			    "%02x", d->reg_select, (int)odata);
 
 			/*
-			 *  A read from csr1..3 should return "undefined"
-			 *  result if the stop bit is set.  However, Ultrix
-			 *  seems to do just that, so let's _not_ print
-			 *  a warning here.
+			 *  #573: CSR1..3 are accessible only while the STOP bit
+			 *  is SET (a read with STOP clear is "undefined" on the
+			 *  chip).  Ultrix reads them with STOP set, which is the
+			 *  in-spec case; nothing is announced either way.
 			 */
 		} else {
 			debugmsg(d->subsys, "register", VERBOSITY_DEBUG,
 			    "WRITE to register 0x%02x: 0x%02x",
 			    d->reg_select, (int)idata);
 			/*
-			 *  A write to from csr1..3 when the stop bit is
-			 *  set should be ignored. However, Ultrix writes
-			 *  even if the stop bit is set, so let's _not_
-			 *  print a warning about it.
+			 *  #573: a write to CSR1..3 with STOP CLEAR is the one
+			 *  the chip ignores; writes with STOP set are the normal
+			 *  case (Ultrix does exactly that).  The model accepts
+			 *  both -- gating on STOP is filed, not implemented.
 			 */
 			le_register_write(d, d->reg_select, idata);
 		}
```

**H1** is the store: the `default:` arm that stored CSR1-3 whole becomes an explicit `case 3:` (the mask) plus a `default:`
(CSR1/CSR2 stored whole, the comment recording the interpreted reading).  `r` reaches this switch only as `d->reg_select`
= `idata & (N_REGISTERS - 1)` (RAP arm, `DEVICE_ACCESS(le)` line 1015; `N_REGISTERS` 4), so `default:` serves exactly 1
and 2.  **H2** is the two comment corrections in `DEVICE_ACCESS(le)`'s RDP arm; no code changes there.

The whole of `le_register_write()` after the edit (VERBATIM from the patched copy):

```c
void le_register_write(struct le_data *d, int r, uint32_t x)
{
	switch (r) {
	case 0:	/*  CSR0:  */
		/*  Some bits are write-one-to-clear:  */
		if (x & LE_BABL)
			d->reg[r] &= ~LE_BABL;
		if (x & LE_CERR)
			d->reg[r] &= ~LE_CERR;
		if (x & LE_MISS)
			d->reg[r] &= ~LE_MISS;
		if (x & LE_MERR)
			d->reg[r] &= ~LE_MERR;
		if (x & LE_RINT)
			d->reg[r] &= ~LE_RINT;
		if (x & LE_TINT)
			d->reg[r] &= ~LE_TINT;
		if (x & LE_IDON)
			d->reg[r] &= ~LE_IDON;

		/*  Some bits are write-only settable, not clearable:  */
		if (x & LE_TDMD)
			d->reg[r] |= LE_TDMD;
		if (x & LE_STRT) {
			d->reg[r] |= LE_STRT;
			d->reg[r] &= ~LE_STOP;
		}
		if (x & LE_INIT) {
			if (!(d->reg[r] & LE_STOP))
				debugmsg(d->subsys, "register write", VERBOSITY_WARNING,
				    "attempt to INIT before STOPped!");
			d->reg[r] |= LE_INIT;
			d->reg[r] &= ~LE_STOP;
		}
		if (x & LE_STOP) {
			d->reg[r] |= LE_STOP;
			/*  STOP takes precedence over STRT and INIT:  */
			d->reg[r] &= ~(LE_STRT | LE_INIT);
		}

		/*  Some bits get through, both settable and clearable:  */
		d->reg[r] &= ~LE_INEA;
		d->reg[r] |= (x & LE_INEA);
		break;

	case 3:
		/*
		 *  #573: CSR3 is BSWP|ACON|BCON; bits 15:3 are "Reserved and read
		 *  as 0" (Am7990 Technical Manual, 1986, p. 1-22; the Am79C90
		 *  datasheet says the same).
		 */
		d->reg[r] = x & 0x0007;
		break;

	default:
		/*
		 *  CSR1 and CSR2 are stored whole.  The Am7990 manual leaves their
		 *  read-back unspecified (CSR1 bit 0 "Must be zero", CSR2 bits 15:8
		 *  "Reserved" -- constraints on the host's writes); the later Am79C90
		 *  (C-LANCE) reads CSR2's reserved bits as zero and says no more
		 *  about CSR1 bit 0; another emulator keeps both writable on the
		 *  Am7990 for a board diagnostic's sake.  An interpreted reading,
		 *  recorded as one: see the #573 record.
		 */
		d->reg[r] = x;
	}
}
```

## 3. THE MEASUREMENTS -- the final detector revision, md5 `6259ce546ddb88fbd1c27be5d091348d` (538 lines), frozen per run

Clones: the pristine HEAD clone `/tmp/gxt17/base` (binary md5 `6c27af7b`, built from a git-archive export of `0b09e7b6`,
whose `dev_le.c` is byte-identical to `2956c32d`'s -- md5 `3eab9c96`) and the fix clone `/tmp/gxt18/fix` (a `cp -a` of the
base clone with the patch applied, `dev_le.o` removed, `make -j4` rc 0, binary md5 `a82cd71f`, newer than its `dev_le.c`).
Copied to `regress/artifacts/lecsrmask/pass1_20261025/final_045716/` (RESULTS_*.txt, raw transcripts, RUN_IDENTITY.txt).

| leg | binary | mode / column | result | rc |
|---|---|---|---|---|
| HEAD column | base | witness mode (base vs HEAD column) | LE_CSRMASK_CONTROL_base=OK LE_CSRMASK_RESULT_base=20/20 | 0 |
| L0 (clause a) | base = pre-fix | GATE (FIX column) | LE_CSRMASK_CONTROL=OK LE_CSRMASK_RESULT=17/20 | 1 |
| L3 (clause c) | `/bin/false` | GATE | LE_CSRMASK_CONTROL=FAIL LE_CSRMASK_RESULT=0/20 | 1 |
| L1 | fix | GATE (FIX column) | LE_CSRMASK_CONTROL=OK LE_CSRMASK_RESULT=20/20 | 0 |
| L2 | base, fix | two legs: base vs HEAD, fix vs FIX | LE_CSRMASK_CONTROL_base=OK LE_CSRMASK_RESULT_base=20/20 LE_CSRMASK_CONTROL_fix=OK LE_CSRMASK_RESULT_fix=20/20 | 0 |

The L0 row table (the three symptom rows red, everything else green):

```
  row          got        head       fix       
  ram:csr0     0x5a5a     want 0x5a5a     ok
  ram:csr3     0x5a5a     want 0x5a5a     ok
  ram:csr2     0x5a5a     want 0x5a5a     ok
  ram:csr1     0x5a5a     want 0x5a5a     ok
  csr0 reset   0x0004     want 0x0004     ok
  rap mask     0x0003     want 0x0003     ok
  csr3 all     0xffff     head 0xffff   fix 0x0007   [FIX] FAIL
  csr3 bits    0x0005     want 0x0005     ok
  csr3 hi      0x0008     head 0x0008   fix 0x0000   [FIX] FAIL
  csr3 mix     0x0015     head 0x0015   fix 0x0005   [FIX] FAIL
  csr2 all     0xffff     want 0xffff     ok
  csr2 lo      0x00a5     want 0x00a5     ok
  csr1 all     0xffff     want 0xffff     ok
  csr1 odd     0x1235     want 0x1235     ok
  csr1 even    0x1236     want 0x1236     ok
  csr1 top     0x8000     want 0x8000     ok
  stable:csr0  0x0004     want 0x0004     ok
  stable:csr3  0xffff     want 0xffff     ok
  stable:csr2  0xffff     want 0xffff     ok
  stable:csr1  0xffff     want 0xffff     ok

  17/20 passed
```

Clause (b): the verbatim reinstatement of `d->reg[r] = x;` at the one fixed site IS the pre-fix build, so L0 discharges it.
Clause (c): `(c): measured at regress/artifacts/lecsrmask/pass1_20261025/final_045716/RESULTS_L3_nullmedium.txt`.
Clause (d): OWED (the variants of the F2 packet 4.3, classified by three seats, not built -- `killtable_20261025/README.txt`
says why).  The earlier revisions' legs are preserved too (`floor_20261025/` for the 18-row revision: 14/18 and 0/18).

## 4. The landing as planned (section 3 of PASS1_RULINGS.md and `landing_plan`), for Q3

`src/devices/dev_le.c` (H1+H2; byte-identical in `est/`; build trees rebuilt with CLEARANCE.out); `regress/le_csrmask_probe.py`
(the final revision); the 17-row witness copy renamed `witness_20261025/le_csrmask_probe.frozen.py` (CLASS_WITNESS); the
`gate_arm.sh` block (sentinel first, control = 1, 20 named rows, denominators by equality 20/20/0; its own reason line,
citing the gate's accretion note and the OWED `gatedevicesplit` row); MANIFEST lines in `check_probe_wiring.py`;
`derive_hygiene_pins.sh --grandfather le_csrmask_probe.py` + `--write`; the CHANGELOG block; OUTSTANDING_BUGS; the ledger
row (state held until the seat outcomes are graded; witness `probe:` naming the 17-row witness and the final instrument's
base/fix legs); the pass-2 receipt; matrix and fable_queue regenerated.  Filings: `lecsr12readback`, `lestopgate`,
`lecsr3stopclear`, `lediagfmt` (`%i` with `uint64_t` at 1019-1020; `%x` at 1039-1040; `%05x` at 911/921), `lecsr3inert`,
the carrier's source-list item; OWED: the variant table, Argon's F2 and pass-2 answers.

---

**THIS FIRING ANSWERS Q1 AND Q2 ONLY.**  Q3 and Q4 go to a separate firing of this same packet; do not answer them here.  Keep hidden reasoning short and put the VERDICT line and the answers in the response itself.

## 5. QUESTIONS -- VERDICT LINE FIRST

**Q1 -- the diff.**  (a) Is H1 exactly the ruled design -- the CSR3 mask, form A, `default:` serving 1 and 2 only (enumerate
the reachable `r`), nothing else changed?  Is the comment honest: does it assert anything as the Am7990's silicon behaviour
rather than as this model's retained behaviour and an interpreted reading?  (b) Is H2 right: do the corrected comments state
the manuals' condition (accessible only while STOP is SET), keep the Ultrix observation as reported, and say the model still
accepts either state?  (c) Anything the diff should carry and does not -- a `#573` tag at each site, the `le_chip_init`
warning left alone, no change to the read path?

**Q2 -- the detector and its evidence.**  (a) Do the five legs in section 3 discharge the ladder's clause (i) (symptom on the
pre-fix committed build, green post-fix, same script) and floor clauses (a) (b) (c)?  Is "(b) discharged by L0" sound for a
one-site fix?  (b) Is the contract header (the frozen probe's docstring) consistent with the rows -- CATCHES, OUTSIDE, ANCHOR,
the session-order sentence, the CONTROL/contract distinction?  (c) Is recording clause (d) as OWED, with the seats'
classifications as predictions, the honest record -- and does the shipped detector's claim stay within the carrier's floor
(a detector that fails (a) (b) (c) is above the vacuity floor; (d) is the null-repair clause ruled 2026-08-23)?  Say plainly
if you read the carrier as forbidding a landing with (d) owed.

**Q3 -- the landing and the records.**  (a) The `probe:` term: `probe:regress/le_csrmask_probe.py -- rung 3, unmodified
pmax -e 3100, witness_20261025/ (17-row witness, before the edit); the final instrument's L2 under pass1_20261025/final_*`
-- right, and is the ORDER evidence sufficient (timestamps and md5s in the RUN_IDENTITY files)?  (b) The ledger row closes
NARROWED: the CSR3 half fixed, the CSR1/CSR2 half withdrawn-and-filed as `lecsr12readback` -- is a closure the right state, or
does the row stay open until the filed row is ruled?  (c) The CHANGELOG block must claim and must not claim what (section 1's
distinctions: retained behaviour vs silicon; read-back-only TRUE of the CSR3 store, FALSE of a CSR1 mask; both STOP
preservation readings; the census population of the #572 follow-up)?  (d) The gate block and the hygiene pins: anything the
plan in section 4 misses (precommit sections R, L, H, O, W, U, P, F)?

**Q4 -- the standing licence.**  If, while verifying a claim, you found something ELSE -- say so.  Candidates: (1) the
witness copy renamed to `.frozen.py` becomes a `.py` the hygiene census might count (it `pty.fork`s) -- does `py_code()`
exclude `artifacts/`?  (2) `csr3 mix`'s HEAD want 0x0015 is a prediction until the final set -- confirm it against section 3.
(3) The `rap mask` row's WARNING line in the gate log -- does any gate check count WARNING lines?
