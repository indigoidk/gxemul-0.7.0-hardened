# `fbctrlcmdkill` (`#567`) -- PASS 3: the repair's own pass.  The detector grew 99 -> 106 -> 123 rows after F2; this pass VERIFIES ITS ENUMERATION

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises, not
just the derivations.**  Where I state something as fact, ask whether it is true.  A seat that re-derives a premise from
something this brief did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`, its WORKING TREE (nothing of this round is
committed).**  Ignore every other `src/` under the project root (pristine 2021 upstream copies).  The working tree also
carries UNRELATED uncommitted edits (`dev_lca.c`, `dev_pcc2.c`, `dev_sh4.c`, `cpu_alpha_palcode.c`,
`regress/diff_wdc_identify.c`, `regress/gate_offline.sh` and others) -- not this round; ignore them.  Frozen copies of
this pass's files are in `regress/artifacts/fbctrlcmdkill/pass3_20261019/frozen/` -- cite those.

**If you cannot read files that is expected** -- every fact you need is inlined.  Name any premise you cannot settle from
this packet rather than guessing at it.  **Where this brief states an arithmetic claim -- a count of rows, a set of cells
-- ENUMERATE it rather than reasoning about it**, and enumerate the right domain: ask what the producer of a value can
actually emit before walking it.

**VERDICT LINE FIRST**, so your answer survives truncation.  READ-ONLY: write nothing to any project tree.

## Why this pass exists, and what would close it

F2 (the adjudication pass on pass 2) converged three ways -- GPT-6 Astra, Grok 4.7, GLM 5.3 -- on two gaps in the 99-row
detector: WIDTH x BOUND EDGE (the only accepted `sd` was an effect-free NOP; only `sb` and `sw` held both edges of the bound) and
the latch's PERSISTENCE (no refusal after an accept or a read).  The repair is new floor-bound material, so it owes its
own pass (the repair-chain rule).  **Two consecutive passes breached one class -- width -- so by the class-closure
amendment this repair closes the WHOLE class in one diff from an explicit enumeration, and THIS PASS VERIFIES THAT
ENUMERATION rather than hunting cells one at a time.**  It closes on a VALID pass that finds zero floor breaches surviving
adjudication, with the zero carried with its denominator (which cells, which mutant shapes were swept).

The PRODUCT (`src/devices/dev_fbctrl.c`) is UNCHANGED since pass 2.  Only the DETECTOR and its gate block changed.

## What this pass reviews -- each file against the copy F2 reviewed, with its disclosure

```
 132   49  regress/fbctrl_cmd_probe.py       INLINED -- the whole v2 -> v4 diff, code and header (section 5)
  25   18  regress/gate_mips_folds.sh        INLINED -- the whole v2 -> v4 block diff (section 6)
   2    1  tools/precommit_check.sh          INLINED (section 6): the manifest comment's row count
   0    0  src/devices/dev_fbctrl.c          UNCHANGED since pass 2 (md5 490b57d8...); the post-fix arm in section 1
```

## SETTLED PREMISES -- recorded resolutions, re-inlined so nobody spends an answer re-deriving them

* **`fatal()` prints and RETURNS** (`src/core/debugmsg.c`'s `fatal()`: no early-out, no exit).  Every refusal row rests
  on it.
* **Pass 1** (`pass1_20261018/ADJUDICATION_p1.md`): member 3 -- refuse every 64-bit DATA value other than 0, 1 and 2 at
  COMMAND BEFORE the store, COMMAND unchanged, one `warned_cmd` latch, one `(once)` announce naming the full value.
* **The witness** (rung 3, unmodified `-E testmips`, HEAD's binary): 2/12; 12/12 on the fix
  (`pass1_20261018/WITNESS_headbin.out`).
* **Pass 2 and F2** (`pass2_20261018/`, `pass2_20261018/f2/F2_DISPOSITIONS.md`, inlined below): all three seats SHIP WITH
  CHANGES at each pass; their findings and my dispositions are in the F2 record.
* **The arm never tests `len`.**  `memory_readmax64(cpu, data, len)` consumes it to build the 64-bit `idata` before the
  switch; nothing after that reads `len` except `memory_writemax64()` on the read path.  So a width-conditioned edit is an
  ADDED test, and it can hide in any cell held at one width only -- which is why the enumeration crosses every partition
  with width.
* **Floor clause (c)** is recorded `(c): measured at <artifact>` or `(c): by construction via <row/pin>, leg not run`;
  for a runtime probe the null medium is an absent or non-emulator binary.
* **Rule D2**: a compare against a constant bound B is pinned by the rows at the bound's two edges -- here 2 (accepted)
  and 3 (refused) -- and a far row never pins the bound.
* **The 16-byte store** (testppc `stvx`/`stvxl`): the callback receives all 16 bytes and `memory_readmax64()` drops the
  prefix before the compare -- disclosed as NOT CLAIMED (6) and filed as `fbctrlvec128` (F2's G3: the earlier wording,
  "the device never sees the rest", was wrong and is corrected).
* **Not fired, by the owner's 2026-10-17 roster:** Opus 5.5, agy, kimi, deepseek, minimax.  Fable 5.1 is tried once per
  pass; it walled at pass 2 and F2 (HTTP 429), recorded as a seat failure and held, never as agreement.


## 1. The product, unchanged since pass 2 -- the post-fix access function in full (every exit path and the tail)

```c
DEVICE_ACCESS(fbctrl)
{
	struct fbctrl_data *d = (struct fbctrl_data *) extra;
	uint64_t idata = 0, odata = 0;

	if (writeflag == MEM_WRITE)
	        idata = memory_readmax64(cpu, data, len);

	switch (relative_addr) {

	case DEV_FBCTRL_PORT:
		if (writeflag == MEM_READ)
			odata = d->current_port;
		else if (idata >= DEV_FBCTRL_NPORTS) {
			/*  #549: an out-of-range selector is REFUSED, and
			    current_port keeps its previous, always-valid value.
			    It used to be stored as an int with only a warning:
			    9 made the next DATA access end the emulator in the
			    range check below, and a wide value was truncated
			    onto a legal port (0x100000003 selected port 3).
			    Announced once per device.  */
			if (!d->warned_port) {
				fatal("[ fbctrl: port number 0x%llx is out of range; "
				    "the selector is unchanged (once) ]\n",
				    (unsigned long long) idata);
				d->warned_port = 1;
			}
		} else
			d->current_port = idata;
		break;

	case DEV_FBCTRL_DATA:
		/*  #549: unreachable while the PORT arm refuses; kept as a
		    tripwire for a later edit that lets a bad selector in.  */
		if (d->current_port < 0 || d->current_port
		    >= DEV_FBCTRL_NPORTS) {
			fatal("[ fbctrl port number is out of range! ]\n");
			exit(1);
		}

		if (writeflag == MEM_READ)
			odata = d->port[d->current_port];
		else if (d->current_port == DEV_FBCTRL_PORT_COMMAND &&
		    idata > DEV_FBCTRL_COMMAND_GET_RESOLUTION) {
			/*  #567: a command other than NOP, SET_RESOLUTION and
			    GET_RESOLUTION is REFUSED before it is stored: COMMAND
			    keeps its previous value and nothing executes.  It used
			    to reach fbctrl_command()'s default: and end the
			    emulator, FILL (3) and COPY (4) included -- the header
			    names them under a TODO and gives them no ports.  The
			    compare is on all 64 bits: the cell is an int, so a
			    wide 0x100000001 used to be stored as 1 and run
			    SET_RESOLUTION.  Announced once per device.  */
			if (!d->warned_cmd) {
				fatal("[ fbctrl: command 0x%llx is not supported; "
				    "the command port is unchanged (once) ]\n",
				    (unsigned long long) idata);
				d->warned_cmd = 1;
			}
		} else {
			d->port[d->current_port] = idata;
			if (d->current_port == DEV_FBCTRL_PORT_COMMAND)
				fbctrl_command(cpu, d);
		}

		break;

	default:
		fatal("[ dev_fbctrl: unimplemented relative addr 0x%x ]\n",
		    (int)relative_addr);
		exit(1);
	}

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}
```

## 2. F2's record -- every finding, the convergences, and what each changed (`pass2_20261018/f2/F2_DISPOSITIONS.md`)

**Roster.**  GPT-6 Astra (`codex_fbcmdf2.txt`, 05:58; token `ASTRA_FBCMD_F2_20261019`), Grok 4.7 xhigh (`grok_f2.txt`,
06:11; `GROK_FBCMD_F2_20261019`), GLM 5.3 (`glm_f2.txt`, 06:04, packet-fed; `GLM_FBCMD_F2_20261019`).  Each answer
carries its token and a verdict line and was read in full.  **All three: SHIP WITH CHANGES.**  Fable 5.1: walled, HTTP 429
(`fable5_f2_WALL.txt`) -- a SEAT FAILURE, held with a question under the owner's 2026-10-17 directive, never agreement.
Opus 5.5, agy, kimi, deepseek and minimax DELIBERATELY NOT FIRED (the owner's 2026-10-17 roster).  Rulings: Astra, Grok and
GLM, by the owner's directive; where the three converge the main loop records the ruling, and where they split it says so.

## Where the three converge

**G1 -- F2 WAS NOT REPAIRED BY v2: WIDTH x BOUND EDGE.**  Astra (FLAG 1; Q3 `M_sd_no_dispatch`, `M_sd_bound0`), Grok
(FLAG 1; Q3 "`sd` bound up by one" and its `sh` twin).  v2's only accepted `sd` was a NOP -- an empty case body -- and only
`sb` and `sw` held both edges of the bound (accept 2, refuse 3; `sw` by the seeds and `R:3`).  **Kill table 3a (`killtable3a_20261019/`, run before any repair)
MEASURED the class's seven open cells ESCAPING v2, 99/99 each:** E15 sd dispatch skipped (= Astra's `M_sd_no_dispatch`),
E16 sd bound 0 (= `M_sd_bound0`), E17 sh bound 1, E18 sd bound 3 (= Grok's), E19 sh bound 3 (= Grok's twin), E20 the
latch cleared by an accept, E21 the latch cleared by a read.  **Disposition: L1 (pre-ship construction -- nothing is
committed), and clause (d) in shape (the fix's own bound relaxed at one width).**  Two consecutive passes (pass 2's E13,
F2's E15-E19) breached ONE class, so by the class-closure amendment the repair owes the CLASS: v3 held accept 2 and refuse 3
at every width with an observable dispatch (`A:edges`, `R:edges`); then **reading the arm for the rest of the class found
seven more open cells at the bound's edges alone -- width x LATCH, where a bound relaxed in one (width, latch) cell
restores the host kill -- so v4 closes the whole class in one diff** (`killtable4_20261019/PRETABLE_ADDENDUM_t4.out` holds
the enumeration, written before v4 ran).

**G2 -- LATCH PERSISTENCE.**  Astra (FLAG 2; Q4), Grok (FLAG 3; Q4): no session refused after an accept or a read; E20/E21
escaped v2 (table 3a).  **Disposition: L1; the contract's "announced once per device" had no row at that cell (CLAIM ->
ROW).**  v3's T2 refuses 3, accepts a NOP, reads COMMAND, refuses 5, refuses `sd 0x100000005`: one announce.

**G3 -- NOT CLAIMED (6)'s MECHANISM SENTENCE WAS FALSE.**  Astra, Grok; GLM's F19 concurs.  The callback RECEIVES all 16
bytes (`memory_rw` hands the device the caller's buffer and `len`; a 16-byte store at DATA fits the window);
`memory_readmax64()` drops the prefix while building `idata`, before the compare.  "The device never sees the rest" put the
loss in the wrong place.  **L4 in the probe's contract -- corrected in v4's.**  And the packet's `machine_test.c:337` is
testmips's OWN install; testppc's comes through `default_test()` at `:154` (Astra, Grok) -- **L4 in my packet; the records
cite `:154`.**  Grok adds the consequence: a 128-bit value whose low half is 1 still runs SET_RESOLUTION -- "this round's
width bug one step further out", which is how the filing names it.

**G4 -- THE GATE BLOCK HAS NEVER RUN IN SITU.**  Astra (FLAG 3), GLM (FLAG 1; Q2), Grok (F18 REFINE).  The replay sourced
the block's lines with a stub `check()` and an injected `fcrc`: the launch line, the real `check()`, the exit propagation
and gate 16's two device probes side by side never executed together.  **Disposition: OWED BEFORE COMMIT** -- one real
`gate_mips_folds.sh` run on the fix's binary (expect green) and one on HEAD's (expect nonzero, naming the block's rows),
`LOGDIR` in scratch, preserved under `wiring_20261019/`.  My F18 "no change" answered only the trailer half.

**G5 -- RECORDS OWED.**  Astra (FLAG 3), Grok (F15, D5), GLM (F15): `fbctrlvec128` as its own ledger row;
`gatedevicesplit`'s row AND `OUTSTANDING_BUGS.md` carry the gate-16 stop -- in GLM's form, *a third device probe lands only
with the split or with a pin on the launch count* (the stop is procedural, not mechanical, and the records say so).
**Owed in commit B.**

## Single-seat findings

* **S1 (GLM FLAG 2) -- census blast radius.**  `tools/precommit_check.sh`'s manifest comment says *"pinned UNQUOTED in
  gate_mips_folds.sh at 95 rows"* -- stale since v2 (99) and again at v3/v4.  **L4 in my working tree: corrected to the
  final count; the records are grepped for stale 95/99/106 row counts before commit.**
* **S2 (GLM FLAG 3) -- E8's name.**  E8 SETS THE LATCH ON AN ACCEPT (`d->warned_cmd = 1;` after the store), not a pre-set:
  a pre-set would silence every first refusal.  The probe's mutant list already says "set by an accept"; my F2 packet said
  "pre-set".  **L4 in the packet; the CHANGELOG says "set by an accept".**
* **S3 (GLM FLAG 4, Q4.4) -- two scope lines.**  "A read stores nothing" was pinned at COMMAND and X1 only (Y1 is read once
  in every session); the `noset` channel is live only in STEPPED sessions (F free-runs).  **Accepted: both go into v4's
  contract** (v4's M3 also reads COMMAND at four widths).
* **S4 (Astra, Grok F20) -- "two stores into `port[]`" was wrong.**  GET_RESOLUTION makes four X1/Y1 assignments, plus the
  dynamic DATA store; `DEVINIT` `memset`s the struct.  **L4 in my packet; the conclusion -- no other writer of COMMAND --
  stands.**
* **S5 (Grok F2 REFINE; Astra Q2) -- "stored and runs at every width" overclaimed** the `sd` NOP.  **v3/v4: GET runs (X1
  zeroed) at every width; the contract says which value is seen to run at which width, and a NOP is stored, not claimed to
  run.**
* **S6 (Astra D2 REFINE) -- describe E14's closure without implying every latch x wide behaviour is covered.**  **Accepted:
  NOT CLAIMED (0) stays and says so.**
* **S7 (GLM F17) -- the unlisted-value class closes only by reshaping the product's compare into an enumeration of accepted
  values.**  **Recorded in NOT CLAIMED (2) as one clause; no reshape here (no measured delta licenses it).**
* **S8 (Astra F14, GLM F14, Grok F14) -- the census split is a plan, not done.**  Correct: commit A is still owed.

## Q2 -- "which of my accepted dispositions is wrong?"

Astra: **F2** (its completeness).  Grok: **F2**, **F1's mechanism sentence**, and **F18's** "no change" (half right).  GLM:
**F18** (the launch line unowned) and **F14** (accepted as a plan, not done).  Every one is taken above (G1, G3, G4, S8).
Upheld by all three: F3, F4, F5, F6, F7, F9, F10, F11, F12, F13, F16, F17 and D3.  GLM withdrew its own F8/D2 wording
("exploitable", "needs a row more than a mutant") -- a seat being harder on its own finding, as asked.

## Q3 -- clean sweeps of the shipped composite (v2)

Astra: `M_sd_no_dispatch`, `M_sd_bound0` (= E15, E16).  Grok: E18 and its `sh` twin E19.  GLM: the three disclosed
families -- value carve-out (2), latch x wide alias (0), 16-byte (6).  **E15-E19 MEASURED escaping v2 (table 3a);** GLM's
three are disclosed by the contract, and the seats agree disclosure is the honest disposition for each.

## What the repair is now, and what it owes

**v3** (106 rows, 24 sessions) = v2 + `A:edges` + `R:edges` + T2's NOP and read between refusals.  Legs: fix 106/106,
HEAD 42/106.  **Kill table 3** (`killtable3_20261019/`) re-ran all 32 mutants and both null media on v3.

**v4** (123 rows, 27 sessions) = v3 + `W:latch` (sd 3 with the latch clear; sb, sh, sw 3 with it set; GET by sb, sh, sd
with it set) + `W:sb` (the latch set by a byte refusal) + `M3` (width at a non-COMMAND port and on the read path).  v3's
rows unchanged.  **Kill table 4** (`killtable4_20261019/`, predictions written first): both legs, all 44 mutants on v4,
the 12 new ones also on v3.

**The repair chain:** v3/v4 are repairs made in response to F2, so they owe their OWN pass -- effort scoped to the v3+v4
diff, the floor question asked of the shipped composite, and, by the class-closure amendment, **the closing pass VERIFIES
THE ENUMERATION** (`PRETABLE_ADDENDUM_t4.out`) rather than hunting cells.  Then Astra confirms before commit.

**Fable's held question:** *"F2 converged three ways on WIDTH x BOUND EDGE and latch persistence (G1, G2); v4 closes the
whole width class in one diff from an explicit enumeration.  Is that enumeration complete for the DATA arm -- does any
partition the arm's code distinguishes, crossed with width, lack a row or a disclosure?"*

## 3. THE ENUMERATION THIS PASS VERIFIES -- `killtable4_20261019/PRETABLE_ADDENDUM_t4.out`, VERBATIM (written before v4 ran)

```
#567 fbctrlcmdkill -- PRE-TABLE ADDENDUM for kill table 4, written 2026-10-19 BEFORE probe v4's legs and BEFORE the table
runs (this file's mtime is the order proof).  INSTRUMENT: probe v4 (the session scratchpad's fbctrl_cmd_probe.v4.py, md5
7ab10a31ef08984589a00ef1243e830c, built by mk_probe_v4.py from v3 by exact-anchor edits; frozen into the table's
directory when it runs).  v3's sessions and rows are UNCHANGED; v4 adds three sessions, 17 rows, and lb/lh/ld to the
assembler (encodings pinned by hand: lb t6 0x810e0010, lh t7 0x850f0010, ld s0 0xdd100010).

WHY: THE CLASS-CLOSURE AMENDMENT.  Two consecutive passes breached ONE class -- WIDTH: pass 2's E13 (the gate qualified by
width) and F2's E15-E19 (the dispatch skipped, and the bound moved, at one width).  v3 closed width x bound edge and width x
dispatch.  Reading the arm for the REST of the class found seven more open cells at the bound's edges alone, where a
width-and-latch-conditioned bound RESTORES THE HOST KILL (sd 3 with the latch clear; sb, sh, sw 3 with it set) -- the
cells a third pass would have found one at a time.  So the repair closes the whole class in ONE diff and the contract
names every cell.

THE ENUMERATION -- the partitions the fixed DATA arm's code distinguishes, crossed with WIDTH (len: the arm never tests
it; memory_readmax64() consumes it to build idata).  (* = new in v4)
  bound edge x latch x width:
                         sb               sh             sw                  sd
      accept 2, clear    A:get            A:edges        C, every seed       A:edges
      accept 2, set      W:latch*         W:latch*       L                   W:latch*
      refuse 3, clear    R:sb3, W:sb*     R:edges        R:3, L, T2, F       W:latch*
      refuse 3, set      W:latch*         W:latch*       W:latch*            R:edges
  the latch SET by a refusal at a width (seen by a later refusal staying silent):
                         W:sb* (sb 3)     R:edges (sh 3) T2, L (sw 3)        W:latch* (sd 3)
  the latch TESTED by a refusal at a width (silent with it set):
                         W:latch* (sb 3)  W:latch*, W:sb* (sh)  T2 (sw 5), W:latch* (sw 3)  R:edges, T2 (sd)
  an accept's dispatch at a width (GET zeroes X1):  sb A:get, W:latch*; sh A:edges, W:latch*; sw C, L; sd A:edges, W:latch*
  an accept's store at a width (read back):         sb A:get; sh A:set; sw L, T2; sd A:nop, W:latch*
  a NON-COMMAND port write at a width (stored, not refused):  sb, sh, sd M3*; sw M2 and every seed
  a READ at a width (returns the cell, stores nothing, runs nothing):  lb, lh, ld M3*; lw M1, M3*
  wide values (sd only -- the width pin):  R:w0..R:w3, R:m1d, T2 (unchanged)
DELIBERATELY NOT COVERED (disclosed, unchanged): value carve-outs, including an interior accepted value at one width
(`&& !(len == 1 && idata == 1)` -- NOT CLAIMED (2)); the latch set x a wide ALIAS (0); a 16-byte store (6).

CHANNEL -- each new row, the mutant it kills, and the observable that differs under it:
  wl alive       E22-E25 (the bound relaxed in one width x latch cell)   the session dies: 3 runs FILL -> default: exit(1)
  wl once        E27 (an sd refusal does not set the latch), E29 (the latch not tested at sb/sh)   announce count 1 -> 2+
  wl sb/sh/sd get x1   E26 (GET refused with the latch set, sb/sh/sd); E22-E25 by death   X1 0 -> 0x7b (or '-')
  wl cmd         E26   COMMAND 2 -> 0 (nothing stored)
  wb once        E28 (a byte refusal does not set the latch), E29   announce count 1 -> 2
  wb cmd         D8 (a refusal stores) at sb/sh with the latch set    COMMAND 0 -> 3/4
  x2 sb/sh/sd    E30 (the port test bypassed for non-word stores)   X2 3/4/5 -> its old value
  m3 quiet       E30   announce count 0 -> 1
  rdw lb         E33 (the read predicate qualified by width: an lb read returns nothing and stores 0)   2 -> 0
  rdw lh/ld/lw   E32 (an lb read stores 0 after returning -- E12 at one width), E33   2 -> 0
  rdw x1         E31 (an ld read runs the command)   X1 123 -> 0
  The channel claim is checkable at writing time for every row above, and this table checks it.

PREDICTIONS
* legs: FIX 123/123, CONTROL=OK (sessions clean 27).  HEAD's binary 51/123: v3's 42, plus M3's nine rows green (the fix
  changes neither a non-COMMAND store nor the read path); W:latch and W:sb die at their first write (FILL reaches default:).
* the twelve NEW mutants, each ESCAPING v3 (106/106, CONTROL=OK -- the cells v3 leaves open) and RED on v4:
    E22_sdclear3     W:latch dies at its first write: wl alive, wl once ('-'), the three gets, wl cmd; sessions clean 26  -> 116/123
    E23_sbset3       W:latch dies at sb 3, after the sd 3's announce: wl alive, the gets, wl cmd, sessions clean;
                     wl once stays green ('0x3' printed first)                                                       -> 117/123
    E24_shset3       the same, at sh 3                                                                               -> 117/123
    E25_swset3       the same, at sw 3                                                                               -> 117/123
    E26_setnarrow    the three gets (0x7b) and wl cmd (0x0)                                                          -> 119/123
    E27_sdnoset      wl once (0x3,0x3: sb 3 announces, then sets)                                                    -> 122/123
    E28_sbnoset      wb once (0x3,0x4)                                                                               -> 122/123
    E29_testnarrow   wl once (0x3,0x3,0x3), wb once (0x3,0x4); R:edges stays green (its sh 3 is its first refusal)   -> 121/123
    E30_portwidth    x2 sb, x2 sh, x2 sd (X2's old value), m3 quiet (1)                                              -> 119/123
    E31_ldreaddisp   rdw x1 (0x0)                                                                                    -> 122/123
    E32_lbreadstore  rdw lh, rdw ld, rdw lw (0x0); rdw lb stays green (it returns 2 before the store)                 -> 120/123
    E33_lbreadpred   rdw lb, lh, ld, lw (0x0)                                                                        -> 119/123
* the 32 earlier mutants: every one RED on v4 (v3's rows are unchanged, so each keeps its v3 kills).  B_gateoff 51/123
  (= HEAD: the refusal gone, W:latch and W:sb die, M3 green).
* the null media: CONTROL=FAILED, and exactly ONE more green row than table 3's v3 null (`m3 quiet', an announce count that
  reads 0 on a session that never started) -- 17/123 if table 3 measures 16/106 as PRETABLE_ADDENDUM_t3.out predicts.
```

## 4. The tables after F2, compact (full logs in each table's directory)

```
#567 kill table 3 (2026-10-19 06:07:58-06:30:12) against PRETABLE_ADDENDUM_t3.out (written 06:06, before it ran).
Instrument: probe v3, 106 rows (probe.v3.frozen.py.txt, md5 74bcb8363688db0e1b95121bb3ea336a).  Clone /tmp/gx567;
baseline the fix: base 106/106 CONTROL=OK.  Restore: part 1 (source == the fix) and part 2 (binary newer) passed;
sentinel cleared.  Every log ends FBCMD_DONE (37 checked: base, 32 mutants, 2 null media, 2 legs).

PREDICTION 'every one of the 32 RED': HELD -- 32 of 32 red (score < 106 or CONTROL=FAILED).

mutant          v2 (t2)    v3 (t3)    predicted held?
B_gateoff       38/99      42/106               
D1_u32          91/99      98/106               
D2_gt1          67/99      68/106                 CONTROL=FAILED
D3_gt0          62/99      63/106                 CONTROL=FAILED
D4_ge0          62/99      63/106                 CONTROL=FAILED
D5_len4         88/99      92/106               
D6_shared       97/99      104/106              
D7_debug        98/99      105/106              
D8_store        88/99      94/106               
D9_anyport      58/99      63/106                 CONTROL=FAILED
D10_nolatch     98/99      104/106              
E1_gt3          79/99      83/106               
E2_nopref       96/99      103/106              
E3_setref       93/99      100/106              
E4_hoist        77/99      84/106               
E5_signed       93/99      100/106              
E6_readdisp     72/99      79/106               
E7_anyport      74/99      81/106               
E8_latchpre     88/99      94/106               
E9_argtrunc     94/99      101/106              
E10_operand     38/99      42/106               
E11_intcast     80/99      87/106               
E12_elseif      97/99      104/106              
E13_lenne4      89/99      92/106               
E14_latchwide   97/99      104/106              
E15_sdnodisp    (3a: 99/99) 105/106    105/106   HELD
E16_sdbound0    (3a: 99/99) 104/106    104/106   HELD
E17_shbound1    (3a: 99/99) 104/106    104/106   HELD
E18_sdbound3    (3a: 99/99) 103/106    103/106   HELD
E19_shbound3    (3a: 99/99) 102/106    102/106   HELD
E20_latchacc    (3a: 99/99) 105/106    105/106   HELD
E21_latchread   (3a: 99/99) 105/106    105/106   HELD
C_absent        15/99      16/106     16/106    HELD  CONTROL=FAILED
C_bintrue       15/99      16/106     16/106    HELD  CONTROL=FAILED

The seven table-3a escapes, row for row (the addendum named the rows): E15 acc sd get x1; E16 acc sd get x1 + acc
edges quiet; E17 acc sh get x1 + acc edges quiet; E18 edge alive + edge cmd + sessions clean 23 (edge once green:
the sh 3 announce prints first -- as predicted); E19 edge alive + edge cmd + edge once ('-') + sessions clean 23;
E20 and E21 two once (0x3,0x5).  Every predicted row and no other.
Null media: CONTROL=FAILED, 16/106 each -- the eleven noset rows and five announce counts (acc nop/set/get/edges
quiet, x2 quiet) read 0 on a session that never started; acc set res and sessions clean are among the red. HELD.
Legs on v3 (v3leg_*.out, the same frozen probe): the fix 106/106, HEAD's binary 42/106.

WHAT FOLLOWED: reading the arm for the rest of the WIDTH class found seven more open cells (width x latch x edge)
and three partitions held at one width only (latch set / tested, a non-COMMAND store, a read) -- v4 and kill table 4
(killtable4_20261019/PRETABLE_ADDENDUM_t4.out, written before either ran).  v3 is history; table 4 measures what ships.
```

```
#567 kill table 4 (2026-10-19 06:30:31-07:03:14) against PRETABLE_ADDENDUM_t4.out (written 06:2x, before v4's legs and
before the table).  Instrument: probe v4, 123 rows (probe.v4.frozen.py.txt, md5 7ab10a31ef08984589a00ef1243e830c); the twelve
new mutants also on probe v3 (probe.v3.frozen.py.txt, md5 74bcb8363688db0e1b95121bb3ea336a -- table 3's instrument).  Clone
/tmp/gx567, baseline the fix; HEAD's binary from /tmp/gx566 (its dev_fbctrl.c == HEAD's, binary newer, checked by the driver
before the legs).  Restore: part 1 (source == the fix) and part 2 (binary newer) passed; sentinel cleared.  Every log ends
FBCMD_DONE (60 checked: 2 legs, 32 + 12 mutants on v4, 12 on v3, 2 null media).

EVERY PREDICTION HELD, ROW FOR ROW.

legs              predicted        measured
  the fix         123/123, OK      123/123, CONTROL=OK, rc 0
  HEAD            51/123           51/123 (v3's 42 + M3's nine rows; W:latch and W:sb die at their first write)

the twelve new mutants -- on v3 every one ESCAPES (106/106, CONTROL=OK, rc 0); on v4 every one is RED:
  mutant           v4 predicted  v4 measured  red rows (measured)
  E22_sdclear3     116/123       116/123      wl alive, wl once (-), wl sb/sh/sd get x1 (-), wl cmd (-), sessions clean 26
  E23_sbset3       117/123       117/123      wl alive, the three gets (-), wl cmd (-), sessions clean 26 -- wl once green
  E24_shset3       117/123       117/123      the same
  E25_swset3       117/123       117/123      the same
  E26_setnarrow    119/123       119/123      wl sb/sh/sd get x1 (0x7b), wl cmd (0x0)
  E27_sdnoset      122/123       122/123      wl once (0x3,0x3)
  E28_sbnoset      122/123       122/123      wb once (0x3,0x4)
  E29_testnarrow   121/123       121/123      wl once (0x3,0x3,0x3), wb once (0x3,0x4)
  E30_portwidth    119/123       119/123      x2 sb (0x0), x2 sh (0x0), x2 sd (0x0), m3 quiet (1)
  E31_ldreaddisp   122/123       122/123      rdw x1 (0x0)
  E32_lbreadstore  120/123       120/123      rdw lh, rdw ld, rdw lw (0x0) -- rdw lb green, as predicted
  E33_lbreadpred   119/123       119/123      rdw lb, rdw lh, rdw ld, rdw lw (0x0)

the 32 earlier mutants on v4 -- predicted "every one RED; B_gateoff 51/123 (= HEAD)": HELD.
  B_gateoff 51   D1_u32 115   D2_gt1 76 (CONTROL=FAILED)   D3_gt0 71 (FAILED)   D4_ge0 71 (FAILED)   D5_len4 102
  D6_shared 121   D7_debug 122   D8_store 110   D9_anyport 75 (FAILED)   D10_nolatch 119
  E1_gt3 92   E2_nopref 120   E3_setref 117   E4_hoist 101   E5_signed 117   E6_readdisp 95   E7_anyport 97
  E8_latchpre 111   E9_argtrunc 118   E10_operand 51   E11_intcast 104   E12_elseif 118   E13_lenne4 105
  E14_latchwide 121   E15_sdnodisp 121   E16_sdbound0 120   E17_shbound1 120   E18_sdbound3 114   E19_shbound3 114
  E20_latchacc 122   E21_latchread 122                                                     (each of 123)

null media (c), on v4: C_absent and C_bintrue each CONTROL=FAILED, 17/123 -- predicted "exactly one more green row than
table 3's v3 null (`m3 quiet')", and table 3 measured 16/106: HELD.  The seventeen: the eleven `noset' rows and six
announce counts that read 0 on a session that never started (acc nop/set/get/edges quiet, x2 quiet, m3 quiet);
`acc set res' and `sessions clean' are among the red.

THE CHANNEL CLAIM, checked as the mandated pre-table check asks: every new row's named mutant reddened that row, through the
named observable.  `wb cmd' (named for D8 -- a refusal that stores -- at sb/sh with the latch set) is red under D8 on v4:
D8_store.raw reads `wb cmd got=0x4 want=0x0 FAIL' (the refused sh 4 stored) beside `two cmd got=0x5' (T2's refused 5).
NO NEW ROW IS VACUOUS: each of the seventeen is red under at least one mutant built --
  wl alive E22-E25   wl once E22, E27, E29   wl sb/sh/sd get x1, wl cmd E22-E26   wb once E28, E29   wb cmd D8
  x2 sb/sh/sd, m3 quiet E30   rdw lb E33   rdw lh/ld/lw E32, E33   rdw x1 E31

THE WIDTH CLASS, as enumerated: every cell of PRETABLE_ADDENDUM_t4.out's grid is held by a named session, and every mutant
built to open one of the cells v3 left open is red on v4 and green on v3 -- the twelve rows above, measured in one table
on one build per mutant.
```

## 5. The detector, v2 -> v4 (the whole diff; v3 was the intermediate measured by table 3)

```diff
--- probe v2 (F2's frozen copy)
+++ probe v4 (the tree)
@@ -18,6 +18,9 @@
        regress/artifacts/fbctrlcmdkill/draft_20261018/PRETABLE.out, section 1); 0x100000003, 0x100000000, 0x100000001,
        0x100000002 and 0xffffffffffffffff by sd.  The wide aliases of ACCEPTED commands are the width pin: a compare on
        the stored int would run NOP (COMMAND reads 0), SET_RESOLUTION (COMMAND reads 1) or GET_RESOLUTION (X1/Y1 read 0).
+  A:edges  ACCEPT GET_RESOLUTION -- the at-bound 2 -- by sd and by sh: each dispatch zeroes X1 (123 -> 0), so dispatch
+       at both widths is observable; COMMAND reads 2, no announce.
+  R:edges  REFUSE 3 -- past the bound -- by sh, then by sd, on the seeded device: alive, COMMAND keeps 2, one announce.
   A:n  ACCEPT, latch clear, one width each: NOP by sd after COMMAND 2 (COMMAND reads 0, X1 keeps 123); SET_RESOLUTION by sh with X1 = Y1 = 0
        (dev_fb_resize() prints `size too small (0 x 0); ignored.` -- a fatal() that returns; COMMAND reads 1; and the resolution-change debug() line
        prints -- the noset rows' channel, shown live); GET_RESOLUTION by sb after X1 = 123, Y1 = 77 (both read 0; COMMAND reads 2).  No command announce in any of them.
@@ -26,8 +29,15 @@
   M1   a READ of COMMAND does not execute it: COMMAND = 2 by a GET, X1 = 123, PORT=0, read DATA twice (2, 2), PORT=1,
        read X1 twice (123, 123): a re-executed GET would zero X1, and a read that STORED would zero the second read.
   M2   a DATA write of 3 to a NON-COMMAND port (PORT=3, X2) is ordinary storage: reads back 3, no announce.
-  T2   three refusals -- 3, 5, then sd 0x100000005 with the latch SET: ONE command announce, naming 0x3; COMMAND
-       keeps its power-on 0.
+  M3   WIDTH at a non-COMMAND port and on the read path: 3, 4 and 5 stored at X2 by sb, sh and sd (each reads
+       back; no announce); then COMMAND = 2 by a GET, X1 = 123, and COMMAND read by lb, lh, ld and lw -- 2 each,
+       so no read stored anything -- and X1 still 123, so no read ran the GET.
+  T2   refuse 3; ACCEPT a NOP; READ COMMAND; refuse 5; refuse sd 0x100000005 -- the latch persists across the accept
+       and the read: ONE command announce, naming 0x3; COMMAND reads 0.
+  W:latch  WIDTH x LATCH at the bound's edges: sd 3 with the latch CLEAR (refused and announced -- an sd refusal
+       sets the latch), then sb, sh and sw 3 with it SET (refused, silent), then GET by sb, sh and sd with it SET
+       (each zeroes X1 again; COMMAND reads 2).
+  W:sb  the latch SET by a byte refusal: sb 3 (announced), then sh 4 (silent); COMMAND keeps 0.
   P1   selector refused first (PORT=9, #549's announce), then command 4 refused: one announce of each kind.
   P2   the reverse order: command 4, then selector 9: one of each.
   F    FREE-RUNNING: PORT=0, DATA=3, then continue to a breakpoint -- the announce must print: under free-running
@@ -36,52 +46,81 @@
 
 CONTRACT (clause e) -- AN ENUMERATION.
 THE FLOOR.  The fixed DATA arm's refusal branch tests the access direction, the port (`current_port == COMMAND`), the
-written value (`idata > DEV_FBCTRL_COMMAND_GET_RESOLUTION`, on all 64 bits the device receives) and the latch
+written value (`idata > DEV_FBCTRL_COMMAND_GET_RESOLUTION`, on all 64 bits memory_readmax64() builds) and the latch
 (`!warned_cmd`); the accept branch stores the value and, at COMMAND, dispatches it.  Every cell of those is held:
-  the value  at the bound, 2 (A:get, and every seed); below it, 1 (A:set) and 0 (A:nop); past it, 3 (R:3, R:sb3, L,
-             T2, F -- rule D2's B+1 edge), 4 (R:4, R:sh4, P1, P2), 5 (R:5, T2), 0xffffffff (R:m1w) and all-ones (R:m1d)
-  its width  refused: sb (R:sb3), sh (R:sh4), sw (R:3, R:4, R:5, R:m1w), sd (R:w3, R:w0, R:w1, R:w2, R:m1d, T2);
-             accepted: sb (A:get), sh (A:set), sd (A:nop), sw (L, every seed).  The four wide values whose low word
-             is 0..3 are the width pin: a compare on the low word accepts w0-w2
-  the port   COMMAND (every R and A session, L, T2, P1, P2, F) and not COMMAND (M2: 3 at X2 is data)
-  the latch  clear (the first refusal of every R session, L, T2, P1, P2, F) and set (L's three accepts, T2's second
-             refusal and its third, a WIDE one); the selector's latch apart from it, in both orders (P1, P2)
-  direction  a write (all) and a read (M1: COMMAND and X1 each read twice -- a read returns the cell, runs nothing
-             and stores nothing)
+  the value  at the bound, 2 (A:get, A:edges, W:latch, every seed); below it, 1 (A:set) and 0 (A:nop); past it, 3
+             (R:3, R:sb3, R:edges, W:latch, W:sb, L, T2, F -- rule D2's B+1 edge), 4 (R:4, R:sh4, W:sb, P1, P2), 5
+             (R:5, T2), 0xffffffff (R:m1w) and all-ones (R:m1d)
+  the port   COMMAND (every R, A and W session, L, T2, P1, P2, F) and not COMMAND (M2 and M3: 3, 4 and 5 at X2 are data)
+  the latch  clear (the first refusal of every R and W session, L, T2, P1, P2, F) and set -- then crossed with a later
+             refusal (R:edges, W:latch, W:sb, T2), a wide refusal (T2's sd 0x100000005), an accept (L, T2's NOP,
+             W:latch's three GETs) and a read (T2): nothing clears it; the selector's latch apart from it, in both
+             orders (P1, P2)
+  direction  a write (all) and a read (M1: COMMAND and X1 each read twice; M3: COMMAND by lb, lh, ld and lw) -- a read
+             returns the cell, runs nothing and stores nothing.  "Stores nothing" is pinned at COMMAND and X1; Y1 is
+             read once per session
+WIDTH -- the class two consecutive passes breached (pass 2's E13; F2's E15-E19), closed in ONE diff.  The arm never
+tests len -- memory_readmax64() consumes it to build idata -- so an edit conditioned on width can hide in any cell held
+at one width only; every partition above is held at EVERY width (the enumeration, written before it was measured:
+regress/artifacts/fbctrlcmdkill/killtable4_20261019/PRETABLE_ADDENDUM_t4.out):
+  edge x latch   accept 2, latch clear: sb A:get, sh A:edges, sw C and the seeds, sd A:edges
+                 accept 2, latch set:   sb, sh and sd W:latch, sw L
+                 refuse 3, latch clear: sb R:sb3 and W:sb, sh R:edges, sw R:3, L, T2 and F, sd W:latch
+                 refuse 3, latch set:   sb, sh and sw W:latch, sd R:edges
+  the latch SET by a refusal at sb (W:sb), sh (R:edges), sw (T2) and sd (W:latch), each seen by a later refusal staying
+                 silent; TESTED -- a refusal with it set stays silent -- at sb (W:latch), sh (W:latch, W:sb), sw (T2's
+                 5, W:latch) and sd (R:edges, T2)
+  an accept is dispatched -- GET zeroes X1 -- at every width (sb A:get, W:latch; sh A:edges, W:latch; sw C, L; sd
+                 A:edges, W:latch) and stored at every width (sb A:get, sh A:set, sw L, sd A:nop)
+  a non-COMMAND store at every width (sb, sh and sd M3; sw M2 and every seed); a read at every width (lb, lh and ld
+                 M3; lw M1 and M3)
+  wide values exist only at sd -- the width pin: the four whose low word is 0..3 (R:w0..R:w3) are refused, where a
+                 compare on the low word would run NOP, SET or GET
 EFFECTS, each held by the sessions named:
-  a refused command keeps COMMAND's previous value -- 2 (every R class), 0 (T2)
+  a refused command keeps COMMAND's previous value -- 2 (every R class, R:edges), 0 (T2, W:sb)
   a refused command executes nothing -- no GET (X1 and Y1 kept, with a GET in COMMAND: every R class) and no SET (no
-      resolution-change line: every R class's `noset' row; A:set's `acc set res' shows that channel live).  A NOP has
-      no observable effect and is not claimed.
-  the first refusal announces once, naming the full value -- every R class, T2 (0x3; then 5 and a wide value silent),
-      P1 and P2 (beside #549's selector announce), F (free-running: fatal() prints where debug() would not)
-  an accepted command is stored and runs -- NOP (A:nop, L), SET_RESOLUTION (A:set, L: the resize line),
-      GET_RESOLUTION (A:get, L, C), at every width (A: sd, sh, sb; L: sw), with the latch clear (A) and set (L)
-  every session survives and exits 0 -- `sessions clean', pinned to the literal 22
-Measured (regress/artifacts/fbctrlcmdkill/): kill table 2 re-ran every mutant built -- 25 -- on this 99-row probe, and
-every one is red (killtable2_20261019/): the gate removed (the pre-#567 arm, 38/99), the compare narrowed to 32 bits, to
-`int' or made signed, its bound moved down by one, two and three or up by one, its operand swapped for the resident
-cell, the gate qualified by width (byte and halfword escaping, or every non-word access refused), the latch shared,
-never set, set by an accept, or bypassed for wide values once set, the announce demoted to debug() or its argument
-truncated, the refused value stored, the port test dropped, a NOP or a SET refused alone, the dispatch hoisted out of
-the store branch, made unconditional on the port, or added to the read path, and the read path falling into the store
-branch.  Tables 1, 1b and 2a (killtable1_20261018/, killtable1b_20261018/, killtable2a_20261019/) measured them on the
-95-row v1, where three escaped -- the reason this probe has 99 rows.
-On a dead binary 15 rows read green -- the eleven `noset' rows and four announce counts, which read 0 on a session that
+      resolution-change line: every R class's `noset' row; A:set's `acc set res' shows that channel live).  That line
+      is a debug() which prints while STEPPING, so `noset' is a claim about stepped sessions; F free-runs and is not
+      read for it.  A NOP has no observable effect and is not claimed to run.
+  the first refusal announces once, naming the full value -- every R class; R:edges, W:latch and W:sb, whose later
+      refusals stay silent; T2 (0x3, then 5 and a wide value silent across a NOP and a read); P1 and P2 (beside #549's
+      selector announce); F (free-running: fatal() prints where debug() would not)
+  an accepted command is stored -- every accept reads back -- and GET_RESOLUTION is seen to RUN (X1 zeroed) at every
+      width, with the latch clear (A:get, A:edges, C) and set (L, W:latch); SET_RESOLUTION is seen to run by sh (A:set)
+      and sw (L: the resize line); a NOP is stored (A:nop by sd, L by sw) and not claimed to run
+  every session survives and exits 0 -- `sessions clean', pinned to the literal 27
+Measured (regress/artifacts/fbctrlcmdkill/): kill table 4 re-ran every mutant built -- 44 -- on this 123-row probe, and
+every one is red (killtable4_20261019/): the gate removed (the pre-#567 arm, 51/123 -- HEAD's own score), the compare
+narrowed to 32 bits, to `int' or made signed, its bound moved down by one, two and three or up by one, its operand
+swapped for the resident cell, the gate qualified by width (byte and halfword escaping, or every non-word access
+refused), the latch shared, never set, set by an accept, or bypassed for wide values once set, the announce demoted to
+debug() or its argument truncated, the refused value stored, the port test dropped, a NOP or a SET refused alone, the
+dispatch hoisted out of the store branch, made unconditional on the port, or added to the read path, the read path
+falling into the store branch; and, at one width, the dispatch skipped or the bound moved down or up (E15-E19), the
+latch cleared by an accept or a read (E20, E21), the bound relaxed in one (width, latch) cell or GET refused at three
+widths once the latch is set (E22-E26), the latch set or tested at only some widths (E27-E29), the port test bypassed
+for non-word stores (E30), and a read running the command (ld), storing after it returns (lb) or returning nothing
+(lb) (E31-E33).  The twelve E22-E33 were measured in the same table on the 106-row v3, and every one escaped it whole.
+Earlier tables measured the rest on v1 (95 rows: tables 1, 1b, 2a), v2 (99: 2, 3a) and v3 (106: 3): v1 let three
+escape, v2 seven and v3 twelve -- the reason this probe has 123 rows.
+On a dead binary 17 rows read green -- the eleven `noset' rows and six announce counts, which read 0 on a session that
 never started; `acc set res' and `sessions clean' are among the red -- so gate 16 requires FBCMD_CONTROL=OK, pins the
-score by equality and checks every row by name (kill table 2's null media).
+score by equality and checks every row by name (kill table 4's null media).
 NOT CLAIMED (disclosed).  (0) The latch SET crossed with a wide ALIAS of an accepted command (w0-w2): T2's third
 refusal is a wide non-alias (0x100000005), which pins the latch-set x wide cell; an edit exempting only the aliases of
-0-2 once the latch is set is a value carve-out, (2).  (1) A refusal that STORES a value aliasing the previous COMMAND:
-w2 truncates to 2 and its `cmd' row cannot vary; ten classes and T2 pin the store (table 2, D8).  (2) Values and bits
-not listed: the compare is relational, so its generating set is its regions, held at their edges; single-bit coverage
-like #549's session B is not claimed, and an edit refusing every listed value but exempting one unlisted (`&& idata
-!= 6') passes.  (3) A second fbctrl instance (#549's fbctrltwoinst, filed): warned_cmd is per device and the probe
-drives one.  (4) The device's other offsets (fbctrloffkill, filed).  (5) fbctrl_command()'s default:, kept as a
-tripwire: unreachable while the arm refuses, so no row reaches it on the fixed device.  (6) A 16-BYTE store: testppc's
-stvx/stvxl reach this arm with len 16, and memory_readmax64() keeps 64 bits, so a 128-bit value whose low half is 0, 1
-or 2 is accepted -- the device never sees the rest.  This MIPS probe cannot issue one; filed with #549's PORT arm, which
-shares it, as fbctrlvec128.
+0-2 once the latch is set is a value carve-out, (2) -- E14's measured closure does not reach it.  (1) A refusal that
+STORES a value aliasing the previous COMMAND: w2 truncates to 2 and its `cmd' row cannot vary; ten classes, T2 and W:sb
+pin the store (D8).  (2) Values and bits not listed: the compare is relational, so its generating set is its regions,
+held at their edges; single-bit coverage like #549's session B is not claimed, and an edit refusing every listed value
+but exempting one unlisted (`&& idata != 6'), or an accepted value at one width, passes -- only a compare reshaped into
+an enumeration of the accepted values would close that family.  (3) A second fbctrl instance (#549's fbctrltwoinst,
+filed): warned_cmd is per device and the probe drives one.  (4) The device's other offsets (fbctrloffkill, filed).  (5)
+fbctrl_command()'s default:, kept as a tripwire: unreachable while the arm refuses, so no row reaches it on the fixed
+device.  (6) A 16-BYTE store: testppc (default_test() installs this device) issues stvx/stvxl, which reach this arm
+with len 16; the callback receives all 16 bytes, but memory_readmax64() builds idata from the low 64, so the prefix is
+dropped before the compare and a 128-bit value whose low half is 0, 1 or 2 is accepted and runs (a low half of 1 runs
+SET_RESOLUTION) -- this round's width defect one width out.  This MIPS probe cannot issue one; filed with #549's PORT
+arm, which shares it, as fbctrlvec128.
 FILL (3) and COPY (4) are refused because nothing implements them (the header lists them under a TODO); a round that
 implements one moves its rows from the refusal list to the accept list.
 
@@ -108,7 +147,7 @@
 RES_RE = re.compile(r"\[ dev_fbctrl: changing resolution to ")   # a debug() line: prints while stepping
 REG = dict(zr=0, t0=8, t1=9, t2=10, t3=11, t4=12, t5=13, t6=14, t7=15, s0=16, s1=17, s2=18, s3=19, s4=20, s5=21,
            s6=22, s7=23)
-OPS = dict(sb=0x28, sh=0x29, sw=0x2b, sd=0x3f, lw=0x23)
+OPS = dict(sb=0x28, sh=0x29, sw=0x2b, sd=0x3f, lw=0x23, lb=0x20, lh=0x21, ld=0x37)
 
 
 def ins(op, rt, off, base="t0"):
@@ -126,6 +165,9 @@
 assert ins("sw", "zr", 0) == 0xad000000
 assert ins("sb", "t1", 0x10) == 0xa1090010
 assert ins("sh", "t1", 0x10) == 0xa5090010
+assert ins("lb", "t6", 0x10) == 0x810e0010
+assert ins("lh", "t7", 0x10) == 0x850f0010
+assert ins("ld", "s0", 0x10) == 0xdd100010
 assert ANCHOR == 0x3c0f0000
 
 #  register plan, the same in every session: s1..s3 = 1..3, s5 = 5, s6 = 9 (a refused selector), t5 = 123, t6 = 77
@@ -312,8 +354,8 @@
     return (op, reg, 16)
 
 
-def get(reg):
-    return ("lw", reg, 16)
+def get(reg, op="lw"):
+    return (op, reg, 16)
 
 
 SEED = [sel("zr"), put("s2"),                     # COMMAND = 2: a GET (headless: X1 = Y1 = 0)
@@ -343,6 +385,11 @@
     row("ref %s once" % name, ",".join(S["cmd"]) or "-", "0x%x" % shown, "one announce, the full value")
     row("ref %s noset" % name, S["res"], 0, "no SET ran: no resolution-change line")
 
+RE = track(session("R:edges", SEED + [put("s3", "sh"), put("s3", "sd")] + READ3, BASE_REGS, ["t2", "t3", "t4"], stub))
+row("edge alive", alive(RE), "alive", "sh 3, then sd 3, at COMMAND: the past-bound 3 refused at both widths")
+row("edge cmd", hx(RE["vals"].get("t2")), "0x2", "COMMAND keeps 2")
+row("edge once", ",".join(RE["cmd"]) or "-", "0x3", "one announce, the first value; the latch then set")
+
 A0 = track(session("A:nop", SEED + [put("zr", "sd")] + READ3, BASE_REGS, ["t2", "t3", "t4"], stub))
 row("acc nop cmd", hx(A0["vals"].get("t2")), "0x0", "NOP by sd is stored: COMMAND reads 0")
 row("acc nop x1", hx(A0["vals"].get("t3")), "0x7b", "NOP touches nothing else")
@@ -358,6 +405,13 @@
 row("acc get x1", hx(A2["vals"].get("t3")), "0x0", "and runs: X1 123 -> 0")
 row("acc get y1", hx(A2["vals"].get("t4")), "0x0", "and Y1 77 -> 0")
 row("acc get quiet", len(A2["cmd"]), 0, "no command announce")
+A3 = track(session("A:edges", [sel("s1"), put("t5"), sel("zr"), put("s2", "sd"), sel("s1"), get("t3"),
+                               put("t5"), sel("zr"), put("s2", "sh"), sel("s1"), get("t4"), sel("zr"), get("t2")],
+                   BASE_REGS, ["t3", "t4", "t2"], stub))
+row("acc sd get x1", hx(A3["vals"].get("t3")), "0x0", "GET_RESOLUTION by sd runs: X1 123 -> 0")
+row("acc sh get x1", hx(A3["vals"].get("t4")), "0x0", "and by sh: X1 123 -> 0 again")
+row("acc edges cmd", hx(A3["vals"].get("t2")), "0x2", "the at-bound 2 accepted by sd and by sh")
+row("acc edges quiet", len(A3["cmd"]), 0, "no command announce")
 
 L = track(session("L", [sel("zr"), put("s3"),                                   # refuse 3: the latch is SET
                         sel("s1"), put("t5"), sel("zr"), put("s2"),             # GET with X1 = 123
@@ -380,11 +434,40 @@
 M2 = track(session("M2", [sel("s3"), put("s3"), get("t2")], BASE_REGS, ["t2"], stub))
 row("x2 three", hx(M2["vals"].get("t2")), "0x3", "3 at X2 is ordinary storage")
 row("x2 quiet", len(M2["cmd"]), 0, "no command announce")
+M3 = track(session("M3", [sel("s3"), put("s3", "sb"), get("t2"), put("s4", "sh"), get("t3"), put("s5", "sd"),
+                          get("t4"), sel("zr"), put("s2"), sel("s1"), put("t5"), sel("zr"),
+                          get("t6", "lb"), get("t7", "lh"), get("s0", "ld"), get("t1"), sel("s1"), get("s7")],
+                   BASE_REGS, ["t2", "t3", "t4", "t6", "t7", "s0", "t1", "s7"], stub))
+row("x2 sb", hx(M3["vals"].get("t2")), "0x3", "3 at X2 by sb is ordinary storage")
+row("x2 sh", hx(M3["vals"].get("t3")), "0x4", "4 by sh")
+row("x2 sd", hx(M3["vals"].get("t4")), "0x5", "5 by sd")
+row("m3 quiet", len(M3["cmd"]), 0, "no command announce")
+row("rdw lb", hx(M3["vals"].get("t6")), "0x2", "COMMAND read by lb")
+row("rdw lh", hx(M3["vals"].get("t7")), "0x2", "by lh")
+row("rdw ld", hx(M3["vals"].get("s0")), "0x2", "by ld")
+row("rdw lw", hx(M3["vals"].get("t1")), "0x2", "and by lw after them: no read stored anything")
+row("rdw x1", hx(M3["vals"].get("s7")), "0x7b", "no read ran GET: X1 keeps 123")
 
-T2 = track(session("T2", [sel("zr"), put("s3"), put("s5"), put("s7", "sd"), get("t2")],
+T2 = track(session("T2", [sel("zr"), put("s3"), put("zr"), get("t3"), put("s5"), put("s7", "sd"), get("t2")],
                    BASE_REGS + [("s7", 0x100000005)], ["t2"], stub))
-row("two once", ",".join(T2["cmd"]) or "-", "0x3", "3, 5, then sd 0x100000005 with the latch set: one announce")
+row("two once", ",".join(T2["cmd"]) or "-", "0x3", "3; a NOP and a read; 5; sd 0x100000005: one announce")
 row("two cmd", hx(T2["vals"].get("t2")), "0x0", "COMMAND keeps its power-on 0")
+W1 = track(session("W:latch", [sel("zr"), put("s3", "sd"),                    # sd 3, the latch CLEAR: refused, announced
+                               put("s3", "sb"), put("s3", "sh"), put("s3"),   # sb, sh, sw 3, the latch SET: silent
+                               sel("s1"), put("t5"), sel("zr"), put("s2", "sb"), sel("s1"), get("t3"),  # GET by sb
+                               put("t5"), sel("zr"), put("s2", "sh"), sel("s1"), get("t4"),             # GET by sh
+                               put("t5"), sel("zr"), put("s2", "sd"), sel("s1"), get("t6"),             # GET by sd
+                               sel("zr"), get("t2")],
+                   BASE_REGS, ["t3", "t4", "t6", "t2"], stub))
+row("wl alive", alive(W1), "alive", "sd 3, the latch clear; sb, sh, sw 3, the latch set: refused at every width")
+row("wl once", ",".join(W1["cmd"]) or "-", "0x3", "one announce: the sd 3 set the latch; sb, sh, sw 3 silent")
+row("wl sb get x1", hx(W1["vals"].get("t3")), "0x0", "GET by sb with the latch set runs: X1 123 -> 0")
+row("wl sh get x1", hx(W1["vals"].get("t4")), "0x0", "and by sh")
+row("wl sd get x1", hx(W1["vals"].get("t6")), "0x0", "and by sd")
+row("wl cmd", hx(W1["vals"].get("t2")), "0x2", "the last GET is stored")
+W2 = track(session("W:sb", [sel("zr"), put("s3", "sb"), put("s4", "sh"), get("t2")], BASE_REGS, ["t2"], stub))
+row("wb once", ",".join(W2["cmd"]) or "-", "0x3", "sb 3 set the latch: the sh 4 after it stays silent")
+row("wb cmd", hx(W2["vals"].get("t2")), "0x0", "COMMAND keeps its power-on 0")
 P1 = track(session("P1", [sel("s6"), put("s4"), get("t2")], BASE_REGS, ["t2"], stub))
 row("p1 port", P1["port"], 1, "the refused selector announced once")
 row("p1 cmd", ",".join(P1["cmd"]) or "-", "0x4", "and the refused command, on its own latch")
@@ -396,8 +479,8 @@
 row("free alive", F["status"], "SURVIVED", "free-running past the refusal to the anchor")
 row("free once", ",".join(F["cmd"]) or "-", "0x3", "fatal() prints while free-running (debug() would not)")
 
-row("sessions clean", sum(1 for S in ALL if S["status"] == "SURVIVED" and S["exit"] == 0), 22,
-    "all 22 sessions ran to the end and exited 0")
+row("sessions clean", sum(1 for S in ALL if S["status"] == "SURVIVED" and S["exit"] == 0), 27,
+    "all 27 sessions ran to the end and exited 0")
 
 try:
     os.unlink(stub)
```

## 6. The gate wiring, v2 -> v4, and the manifest comment

```diff
--- gate 16 block v2 (F2's frozen copy)
+++ gate 16 block v4 (the tree)
@@ -4,18 +4,23 @@
 #  reached fbctrl_command()'s default: and ended the emulator, and a wide value was stored into the
 #  int cell as its low word, so 0x100000001 ran SET_RESOLUTION.  #567 refuses every other 64-bit
 #  value before the store (COMMAND keeps its value, nothing runs) and announces once per device.
-#  regress/fbctrl_cmd_probe.py drives real guest sb/sh/sw/sd/lw on an unmodified testmips, like the
-#  #549 probe above, so it too runs before the pmax-kernel check.  THE CONTRACT is its header.
-#  Kill table 2 (regress/artifacts/fbctrlcmdkill/killtable2_20261019/) re-ran all 25 mutants built
-#  for this round on its 99 rows -- every one red -- and two null media: on a binary that runs
-#  nothing, 15 absence rows read green and the record still parses, so this block requires
-#  CONTROL=OK, pins the score by EQUALITY, and checks EVERY row by name (pass 2: a row swapped for
-#  an unrelated unique green one keeps every count).
+#  regress/fbctrl_cmd_probe.py drives real guest sb/sh/sw/sd and lb/lh/lw/ld on an unmodified
+#  testmips, like the #549 probe above, so it too runs before the pmax-kernel check.  THE CONTRACT is
+#  its header, and it enumerates every partition of the arm crossed with access WIDTH (the class two
+#  review passes found open).  Kill table 4 (regress/artifacts/fbctrlcmdkill/killtable4_20261019/)
+#  re-ran all 44 mutants built for this round on its 123 rows -- every one red, the twelve built
+#  last having escaped the 106-row v3 -- and two null media: on a binary that runs nothing, 17
+#  absence rows read green and the record still parses, so this block requires CONTROL=OK, pins the
+#  score by EQUALITY, and checks EVERY row by name (pass 2: a row swapped for an unrelated unique
+#  green one keeps every count).
 #  `gatedevicesplit` (#498) grows by this second device probe in a CPU gate.  That is debt, not a
-#  fit: pass 2 asked that it not be called fine (Grok 4.7), and that the split land before a third
-#  device probe enters this gate (GLM 5.3).
+#  fit: pass 2 asked that it not be called fine (Grok 4.7), and the STOP is recorded on that row --
+#  a third device probe lands here only with the split or with a pin on this gate's launch count
+#  (GLM 5.3).  Like #549's, the launch below has no timeout: a wedged probe hangs the gate, which is
+#  visible and not a false pass (filed for both blocks as `gate16fence`).
 #  The probe prints a row's status AFTER got/want, unlike the #549 probe, so every row count below
-#  uses one anchored pattern, FCROW; it counts 99 rows in each of kill table 2's 28 logs.
+#  uses one anchored pattern, FCROW; it counts 123 rows in each of kill table 4's 48 logs on v4, and
+#  this block, replayed on them, is green only on the fix (wiring_20261019/GATE16_REPLAY_v4.out).
 FCLOG=$LOGDIR/fbctrl_cmd_probe.log
 FCROW='^  [^ ].* got=[^ ]* +want=[^ ]* +'
 FCNAMES=("live" "devsig" "ref 3 alive" "ref 3 cmd" "ref 3 x1" "ref 3 y1" "ref 3 once" "ref 3 noset"
@@ -27,10 +32,13 @@
          "ref w3 noset" "ref w0 alive" "ref w0 cmd" "ref w0 x1" "ref w0 y1" "ref w0 once" "ref w0 noset"
          "ref w1 alive" "ref w1 cmd" "ref w1 x1" "ref w1 y1" "ref w1 once" "ref w1 noset" "ref w2 alive"
          "ref w2 cmd" "ref w2 x1" "ref w2 y1" "ref w2 once" "ref w2 noset" "ref m1d alive" "ref m1d cmd"
-         "ref m1d x1" "ref m1d y1" "ref m1d once" "ref m1d noset" "acc nop cmd" "acc nop x1" "acc nop quiet"
-         "acc set cmd" "acc set ran" "acc set res" "acc set quiet" "acc get cmd" "acc get x1" "acc get y1"
-         "acc get quiet" "latch get x1" "latch nop cmd" "latch set cmd" "latch set ran" "latch once"
-         "rdcmd val" "rdcmd again" "rdcmd noexec" "rdx1 again" "x2 three" "x2 quiet" "two once" "two cmd"
+         "ref m1d x1" "ref m1d y1" "ref m1d once" "ref m1d noset" "edge alive" "edge cmd" "edge once"
+         "acc nop cmd" "acc nop x1" "acc nop quiet" "acc set cmd" "acc set ran" "acc set res" "acc set quiet"
+         "acc get cmd" "acc get x1" "acc get y1" "acc get quiet" "acc sd get x1" "acc sh get x1"
+         "acc edges cmd" "acc edges quiet" "latch get x1" "latch nop cmd" "latch set cmd" "latch set ran"
+         "latch once" "rdcmd val" "rdcmd again" "rdcmd noexec" "rdx1 again" "x2 three" "x2 quiet" "x2 sb"
+         "x2 sh" "x2 sd" "m3 quiet" "rdw lb" "rdw lh" "rdw ld" "rdw lw" "rdw x1" "two once" "two cmd"
+         "wl alive" "wl once" "wl sb get x1" "wl sh get x1" "wl sd get x1" "wl cmd" "wb once" "wb cmd"
          "p1 port" "p1 cmd" "p2 cmd" "p2 port" "free alive" "free once" "sessions clean")
 fcrc=0
 python3 -u fbctrl_cmd_probe.py "$PMAX" > "$FCLOG" 2>&1 || fcrc=$?
@@ -50,8 +58,8 @@
     check "fbctrl command probe exit 0 (nonzero: a crash or a red row)" "$fcrc" "0"
     fcres=$(sed -n 's/^FBCMD_RESULT=//p' "$FCLOG")
     #  Pinned UNQUOTED under a one-token stem, so check_score_claims.py sees the pin (as #549's).
-    check "fbctrl_cmd rows run" "${fcres#*/}" 99
-    check "fbctrl_cmd rows correct" "${fcres%/*}" "99"
+    check "fbctrl_cmd rows run" "${fcres#*/}" 123
+    check "fbctrl_cmd rows correct" "${fcres%/*}" "123"
     check "fbctrl_cmd rows failed" "$(grep -cE "${FCROW}FAIL  " "$FCLOG")" "0"
     #  Reconcile the rows printed with the trailer, and require each row name once (#549 F2).
     check "fbctrl_cmd rows emitted match the trailer total" \
@@ -63,9 +71,8 @@
              sort | uniq -d | wc -l)" "0"
     #  And EVERY expected row by NAME, green exactly once: counts and uniqueness cannot tell an expected
     #  row from an unrelated unique one put in its place (pass 2, GPT-6 Astra).
-    check "fbctrl_cmd named rows" "${#FCNAMES[@]}" 99
+    check "fbctrl_cmd named rows" "${#FCNAMES[@]}" 123
     for v in "${FCNAMES[@]}"; do
         check "  fbctrl_cmd row: $v" "$(grep -cE "^  ${v} +got=[^ ]* +want=[^ ]* +ok  " "$FCLOG")" "1"
     done
 fi
-
```

```diff
diff --git a/tools/precommit_check.sh b/tools/precommit_check.sh
index c157ab43..48f41b14 100644
--- a/tools/precommit_check.sh
+++ b/tools/precommit_check.sh
@@ -353,7 +353,10 @@ elif out=$(python "$SCORECHK" 2>&1); then
 	#  the stem, and only a docstring at regress/<stem>_probe.py or regress/<stem>.py; no comment line
 	#  names ip30_abort and the probe lives under artifacts/, so for this pin it checks no prose -- only
 	#  the pin is counted.
-	SCORE_CLAIMS_MANIFEST=35
+	#  RAISED 35 -> 36 ON 2026-10-18, DELIBERATELY.  One newly gated probe: fbctrl_cmd_probe.py
+	#  (#567, pinned UNQUOTED in gate_mips_folds.sh at its final 123 rows; 95 when this line was
+	#  first written, before the review passes grew it).
+	SCORE_CLAIMS_MANIFEST=36
 	_spinned=$(printf '%s\n' "$out" | sed -n 's/^SCORE_CLAIMS_PINNED=//p')
 	if [ -z "$_spinned" ]; then
 		bad "check_score_claims printed no SCORE_CLAIMS_PINNED line -- the count cannot be pinned"
```

## 7. The block run IN SITU (F2's G4) -- `wiring_20261019/INSITU.md`

# `#567` gate 16 run IN SITU -- F2's G4 (2026-10-19 07:30:37-07:31:35)

**What was owed.**  F2's three seats (GPT-6 Astra, Grok 4.7, GLM 5.3) all named it: the offline replay sourced the
block's lines with a stub `check()` and an injected `fcrc`, so the launch line, `lib.sh`'s real `check()`, the exit
status and `#549`'s probe running beside this one had never executed together.

**What ran.**  The real `regress/gate_mips_folds.sh` from the working tree (md5 `80462d1f85cdd5a6fcdf8b63fd265f67`), with
the 123-row probe (`regress/fbctrl_cmd_probe.py`, md5 `d1a69bb13488797b7c5103cc50b6d54d` -- table 4's frozen v4 with
its final header; its code AST-identical to `killtable4_20261019/probe.v4.frozen.py.txt`), `LOGDIR` in scratch, once
per binary, by `insitu_20261019/insitu567.sh`.  Clearance before the runs: `build/` part 1 and part 2 ok; `/tmp/gx566`
holds HEAD's `dev_fbctrl.c` and a binary newer than it.

| binary | how | gate rc | gate 16 | the `#567` block |
|---|---|---|---|---|
| `build/gxemul` (the fix) | the gate's DEFAULT `PMAX` | 0 | **PASS, 159 checks** | 133 checks, 0 red |
| `/tmp/gx566/gxemul` (HEAD) | `PMAX=` | 1 | **FAIL, 75 of 159** | 133 checks, **75 red** -- every red check in the gate is this block's |

On HEAD's binary `#549`'s block stays green (HEAD carries `#549`) and the fold rows read 14/14, so the gate's failure
is attributable to this block alone; its reds are the probe's exit status, the score, the failed-row count and 72
named rows (`ref 3 alive  got=DIED/1` first).  Both gate logs, both probe logs and `#549`'s probe logs are in
`insitu_20261019/` (completion lines present: `INSITU_DONE`; each probe log ends `FBCMD_DONE`).

**So G4 is discharged**: the launch line runs the shipped probe on the default binary, `check()` grades it, the exit
status propagates (rc 0 / rc 1), and the two device probes coexist in one run of gate 16.

The offline replay of the same block on all 48 table-4 logs and five hand-made broken logs is
`GATE16_REPLAY_v4.out`: 133 checks green only on the fix; every mutant, both null media and all five broken logs red;
the block's own FCROW counts 123 rows in each of the 48 logs.

## What is still OWED, and where I may be fooling myself

* **The enumeration is mine.**  I wrote it by reading the arm for the partitions its code distinguishes and crossing each
  with width.  If I missed a partition, every cell of it is missing too -- and the tables cannot show that, because a
  table only measures the mutants someone thought to build.  That is why question 1 is first.
* **I graded every post-F2 finding L1** (pre-ship construction: nothing is committed) and treated the width cells as a
  CLASS CLOSURE rather than as floor -- width is not a partition the arm's code tests (it never reads `len`), so the
  joint-cells floor does not reach it; two consecutive passes breaching it is what pulled it in.  A seat that would grade
  any of these as a floor breach of the SHIPPED composite should say so: the disposition is the same (fixed in-round)
  but the record differs.
* **The contract claims a holder for every cell.**  A claim with no row behind it is a wrong record (L4).
* **Fable 5.1 walled at pass 2 and F2.**  It is tried once more on this pass; a wall is a seat failure, held with a
  question, never agreement.
* **Nothing is committed.**  After this pass: Astra's confirm, then commit A (`#564`'s census repair, alone) and commit B
  (`#567`).

## Questions

1. **VERIFY THE ENUMERATION** (section 3).  Does any partition the fixed DATA arm's code distinguishes, crossed with
   width, lack a row or a disclosure?  If so: the cell, the smallest edit that hides in it, and the row you expect to
   stay green.  If not, SAY WHAT YOU WALKED -- the partitions and widths -- so a zero carries its denominator.
2. **CHECK THE CHANNELS AGAINST THE LOGS.**  For each of the 17 new rows the addendum names the mutant it kills and the
   observable that differs; table 4 measured them (section 4).  Is any kill an accident -- red for a reason other than
   the one named -- and is any new row green under every mutant built (vacuous)?
3. **A CLEAN SWEEP OF THE SHIPPED COMPOSITE** (the fix + probe v4 + gate block v4)?  Name the edit exactly and the row
   you expect to stay green, and say whether it lies INSIDE the enumerated class (a breach) or outside it (a disclosure,
   existing or owed).
4. **WHICH OF MY RECORDS IS WRONG?**  The contract v4 (section 5, the header), the F2 record (section 2) and its
   classifications, the table comparisons (section 4).  Name any claim no row supports, any count that is off, and any
   grading you would make differently.
5. **The block run in situ** (section 7): does it discharge F2's G4 -- the launch line, the real `check()`, the exit
   status, and `#549`'s probe running beside this one?
6. **What did all of us miss?**
