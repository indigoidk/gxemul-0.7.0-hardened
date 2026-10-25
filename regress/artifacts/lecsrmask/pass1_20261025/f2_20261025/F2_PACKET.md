# ADJUDICATION PASS (F2) -- research item T18, ledger row `lecsrmask`, pass 1 -- GXemul hardened fork

Written 2026-10-25 05:0x by the main loop.  This is the THIRD pass of the round's pass 1 (template §F2): every seat's
findings on the pass-1 design brief, consolidated and numbered, with the main loop's DISPOSITION on each, the
DISAGREEMENTS listed separately with both sides, and the three adjudication questions.  Tree under review:
`GXEMUL-SEC/src/` at HEAD `2956c32d` (`src/devices/dev_le.c` unchanged since `5bf592d6`; identical in the working tree
and in `est/`).  **No product edit has been made yet.**

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

The pass-1 brief stated two premises wrongly and the seats caught both (F1, F3 below).  **Check the premises, not just
the derivations.**  A seat that re-derives a fact from something this packet did NOT give it is worth more than a seat
that agrees.  **The tree under review is `GXEMUL-SEC/src/`** (three pristine-2021-upstream copies sit under the project
root; line numbers off by hundreds mean you are reading one).  **If you cannot read files that is expected** -- every
fact this pass depends on is inlined in section 1; name any premise you cannot settle rather than guessing.  **VERDICT
LINE FIRST.**

**Self-review disclosed.**  A seat whose own finding appears below is adjudicating its own work: be HARDER on it, and
check that the DISPOSITION is right, not merely that the finding was.  A ruling that ADOPTS your position is the one you
are least likely to test -- test it.

**Reading scope (file-reading seats):** `GXEMUL-SEC/src/`; `GXEMUL-SEC/regress/artifacts/lecsrmask/pass1_20261025/`
(`packet.md` = the pass-1 brief; the seven seat answers `codex_t18p1.txt`, `grok_t18p1.txt`, `ollama_glm_t18p1_Q12.txt`,
`ollama_glm_t18p1_Q34.txt`, `ollama_deepseek_t18p1_Q12.txt`, `ollama_deepseek_t18p1_Q34.txt`; `PASS1_CORRECTIONS.md`;
the frozen detector `le_csrmask_probe.frozen.py.txt`; `det18_HEAD/`), `GXEMUL-SEC/regress/artifacts/lecsrmask/witness_20261025/`
and `.../floor_20261025/`, and the manuals by ABSOLUTE path `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\lance\TM1986.txt` and
`...\am79c90_bitsavers.txt`.  **Do not read other files under `regress/artifacts/`, nor `tools/pipeline/ledger.json`,
`CHANGELOG.md` or `OUTSTANDING_BUGS.md`.**  Do not build or run anything; do not propose reproduction recipes.

**The roster for this pass:** GPT-6 Astra (ADJUDICATES -- its answer is the ruling of record, provisional until the
roster completes), Grok 4.7, GLM 5.3 and DeepSeek (packet-fed, two firings: part A = F1-F24, part B = D1-D5 + Q2 + Q3),
Gemini 4 Argon (web route; its pass-1 answer was not yet in when this packet was written -- F25 holds its place).
Fable 5.1 HELD; kimi, minimax, Opus seat deliberately not fired.

**Answer format -- VERDICT LINE FIRST:**
~~~~
VERDICT: RATIFY | RATIFY WITH CHANGES | NOT RATIFY -- <one line>
WRONG: <the F/D numbers whose disposition you overturn, or "none">
~~~~
Then: Q1 -- one line per F1-F25 and D1-D5: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, with the reason.  Q2 -- WHICH OF
MY ACCEPTED DISPOSITIONS IS WRONG?  I accepted twenty of twenty-five findings and ruled five disagreements my own way;
that is a suspicious number and agreement is not evidence.  Q3 -- WHAT DID ALL OF US MISS?  Mark claims READ / DERIVED
/ NOT CHECKABLE.

---

## 1. The facts this pass rests on -- VERIFIED by the main loop after pass 1 (each a reading of a file, or a measurement)

**1.1 The Am7990 LANCE Technical Manual (AMD, 1986; the chip the DECstation 3100 carries)** --
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\lance\TM1986.txt`, VERBATIM lines:

```
1539:                Reserved and read as zeroes.                             RINT            <- RAP bits 15:02
1545:     01 :00 CSR(1 :0) CSR address select. READ/WRITE.
1695: 01  STRT START enables the LANCE to send and                                   15:08 RES Reserved.      <- CSR2
1697:             receive packets, perform direct memory ac- 07:00 IADR The high order 8 bits of the address of the first
1732: CONTROL AND STATUS REGISTER 1 (CSR1)                                           Bit Name Description
1733: READ/WRITE: Accessible only when the STOP bit of CSRo is
1734:                                                                                15:03 RES Reserved and read as "O".   <- CSR3
1745: 15:01 IADR  The low order 15 bits of the address of the first
1746: 00          word (lowest address) in the Initialization
1749:             Must be zero.                                                                                           <- CSR1 bit 0
2853: ...                                                                       CSR1 and CSR2 are normally not affected when the Stop bit is
2854:                                                                           set in CSRo. (When the Stop bit is set, CSR3 is cleared and
2855: ...                                                                       CSRo is set to 0004 Hex, Stop bit set.) However, it is recom-
2856: ...                                                                       mended to reload CSR1 and CSR2 whenever the Stop bit is
2857: ...                                                                       set.
```

**1.2 The Am79C90 C-LANCE datasheet (AMD, "PRELIMINARY")** -- `...\am79c90_bitsavers.txt` (the pass-1 brief's 9.1 has the
raw two-column lines): CSR1 bits 15:01 IADR, bit 00 "Must be zero." (1138-1142); CSR2 bits 15:08 "RES  Reserved. Read as
zeroes. Write as zeroes." (1161-1163); CSR3 bits 15:03 "RES  Reserved. Read as zeroes. Write as zeroes." (1222-1223);
RAP bits 15:02 "RES  Reserved. Read as zeroes. Write as zeroes." (949-950); all three CSRs "Accessible only when the STOP
bit of CSR0 is a ONE" (1123-1124, 1146-1147, 1197-1198); Appendix B (3411): *"b) CSR1 and CSR2 contents are preserved
[C-LANCE] | b) CSR1 and CSR2 are not preserved when [STOP is set, LANCE]"* -- the two chips differ in these registers.

**1.3 MAME's `am79c90.cpp` (a second emulator modelling BOTH chips)** -- fetched 2026-10-25 04:4x from
`https://raw.githubusercontent.com/mamedev/mame/master/src/devices/machine/am79c90.cpp`, register-write handler, VERBATIM:

```
		case 1: // Least significant 15 bits of the Initialization Block
			// Datasheet says "must be zero", but doesn't indicate what
			// happens if it's written non-zero. Must be writable to pass
			// system diagnostic on MIPS RS2030.
			if (m_csr[0] & CSR0_STOP)
				m_csr[1] = data;
			break;

		case 2: // Most significant 8 bits of the Initialization Block
			// The C-LANCE datasheet explicitly states these bits read and
			// write as zero, while LANCE datasheet just says "reserved".
			// MIPS RS2030 diagnostic requires these bits to be writable,
			// so assuming this is older device behaviour.
			if (m_csr[0] & CSR0_STOP)
				m_csr[2] = (type() == AM7990) ? data : (data & 0x00ff);
			break;

		case 3: // Bus master interface
			if (m_csr[0] & CSR0_STOP)
				m_csr[3] = data & CSR3_MASK;
			break;
```

**1.4 The upstream commit the research row ports** -- `rpajarola/gxemul` `e108b546`, "3MIN: the LANCE ethernet, through the
IOASIC", fetched 2026-10-25 05:0x (page summary; short exact quotes): the commit message says *"CSR1..3 of the LANCE keep
only their implemented bits, which 3/ni/regs checks"* and *"This layout was checked against the KN02-BA PROM's own
loopback test"*; its `dev_le.c` hunk adds `/* CSR1: the init block address is word aligned */` `d->reg[r] = x & 0xfffe;`,
`/* CSR2: only the high 8 bits of the address */` `d->reg[r] = x & 0x00ff;`, `/* CSR3: BSWP, ACON, and BCON */`
`d->reg[r] = x & 0x0007;`.  The words "Am7990" and "C-LANCE" do not appear in it.  The 3MIN (DECstation 5000/1xx, KN02-BA)
is a machine this fork does NOT emulate the LANCE of (`machine_pmax.c` 286-289 comments it out); the PROM test he cites
ran against his fork's model, and **which LANCE part the KN02-BA carries is NOT ESTABLISHED here**.

**1.5 What this fork's model serves.**  `dev_le.c` is "LANCE ethernet, as used in DECstations" (header comment); one
`le_register_write()` for every instance; callers: `machine_pmax.c` KN01/3100 (line 129) and KN230 (708),
`dev_turbochannel.c` 227 (the PMAD-AA option), `dev_luna88k.c` 1086.  The witness machine is the KN01 (Am7990; the brief's
D2).  Every reader of `reg[1..3]`, grepped at HEAD: `reg[1]` and `reg[2]` once each at `le_chip_init` 179 (the init-block
address, whose bit 0 `le_read_16bit` preserves -- F2); `reg[d->reg_select]` once at the RDP read (981); nothing reads
`reg[3]` by index.  `le_register_write` has one caller (1002).  The STOP bit is written only by the CSR0 arm (864, 871,
874) and `dev_le_init` (1077).

**1.6 Measured before any edit** (`regress/artifacts/lecsrmask/floor_20261025/RUN_IDENTITY.txt`): with the pass-1
(three-mask) detector revision, L0 = the pre-fix build in GATE mode (FIX column) `LE_CSRMASK_RESULT=14/18 CONTROL=OK` rc=1;
L3 = the null medium `/bin/false` `LE_CSRMASK_RESULT=0/18 CONTROL=FAIL` rc=1 -- `(c): measured at
regress/artifacts/lecsrmask/floor_20261025/RESULTS_L3_nullmedium.txt`.  The witness: 17/17 HEAD column (03:47-03:49);
the 18-row revision 18/18 HEAD column (04:05); binary `6c27af7b` from a git-archive export of `0b09e7b6`.

**1.7 The #572 hygiene follow-up LANDED** as `2956c32d` (05:0x): `gate_hygiene.sh` pin 77 -> 78 and `wdc_lba_probe.py`
grandfathered, written by `derive_hygiene_pins.sh`; the report afterwards reads got == pinned on every census.

---

## 2. The findings, F1-F25 -- attribution, the main loop's DISPOSITION, what changed

| # | finding | raised by | disposition | what changed |
|---|---|---|---|---|
| F1 | The CSR1 (`0xfffe`) and CSR2 (`0x00ff`) masks are not established for the Am7990: its manual says "Must be zero" (a write constraint) and "Reserved." only (1.1); the C-LANCE text does not bind the Am7990 bit-for-bit (1.2 Appendix B); MAME keeps both writable on the Am7990 because a MIPS RS2030 hardware diagnostic requires it (1.3); rpajarola's masks are C-LANCE semantics ported without distinguishing the chip (1.4) | grok (NOT READY), codex (P1 "incompletely established", P2 "too strong"), DeepSeek (NOT READY on P1), GLM (P1 "an interpreted reading, not a settled fact") | **ACCEPTED -- the repair is NARROWED to CSR3** (`x & 0x0007`, settled by BOTH manuals and MAME).  CSR1 and CSR2 stay stored whole, as the Am7990 does; the record says why; the CSR1/CSR2 read-back question is FILED as its own row carrying both readings (1.3 vs 1.4).  **This is D1.** | the design (section 4); the detector's CSR1/CSR2 rows become CONTRACT rows pinning stored-whole; the ledger row's closure records the narrowing |
| F2 | S6/P5 ("read-back only") false: CSR1 bit 0 feeds `init_block_addr`, and `le_read_16bit` preserves bit 0, so a CSR1 mask would move an odd init block one byte for every machine | codex | ACCEPTED (moot under F1, recorded) | the "read-back only" sentence is withdrawn from every record |
| F3 | "TM1986 carries no 'read as zeroes' sentence" was false -- RAP 1539 and CSR3 1734 say it; CSR2 1695 says only "Reserved." | grok, codex | ACCEPTED -- L4; the drafting grep was cut by `head -40` (a phantom absence) | PASS1_CORRECTIONS.md C1; the CHANGELOG block will carry the lines |
| F4 | V18 reds N7 N8 N9 N10 (not N7 N9); V19 reds all eight CSR rows (N8 and N12 were omitted) | GLM (both), DeepSeek (V19), grok (V19 N12), codex (V19) | ACCEPTED (verified by arithmetic) | the variant table is rebuilt for the narrowed design (section 4.3) |
| F5 | Grade C1-C6 as clause-(e) mask-contract obligations, not six floor cells: the dominating predicate is the selector switch, the three labels are the floor siblings, and promoting kept/dropped bits to floor cells extends R5 | codex; grok, GLM and DeepSeek graded them FLOOR | **REFINED -- D2.**  Under the narrowing the edited arm is ONE label (CSR3); its kept/dropped partition is rowed either way (N7, N8, the new `csr3 hi`), and the sibling labels CSR1/CSR2 are rowed as contract rows.  Which rule-reading is right changes no row here; Astra rules it for the record | none rowed; the contract names the cells |
| F6 | Clause (b) owes a verbatim restoration at EVERY fixed site; V1 restored all three at once | codex | ACCEPTED; under F1 there is one fixed site, so one verbatim revert discharges (b) (V1' in 4.3) | the table |
| F7 | The CATCHES / OUTSIDE contract of brief 7.6 is absent from the probe's header | codex | ACCEPTED -- L1 pre-ship | the header gains the contract (4.4) |
| F8 | Docstring defects: "every want is a literal" excludes the stable rows; "the last RDP value read a second time" is wrong (the ALL value is read twice, immediately); N12 is not a dropped-bit-alone input; the mnemonic fraction reads like a failure | codex, grok, GLM | ACCEPTED -- L1 | the docstring is corrected; the mnemonic count is labelled informational |
| F9 | Both STOP comments at 986-991 and 996-1001 invert the datasheet's condition ("Accessible only when the STOP bit ... is a ONE"); the Ultrix notes record in-spec accesses | codex, GLM, grok, DeepSeek | ACCEPTED as a finding; disposition is **D3** (fix both in the same change as L4 records -- codex, GLM; or file -- grok) | my ruling: fix both in-round, comments only |
| F10 | `dev_le.c` 1017-1020 passes `uint64_t idata` to `%i` -- a variadic-format mismatch | codex | ACCEPTED -- FILED (not this round's edit) | a records row |
| F11 | "big-endian host" should read "big-endian emulated machine" (`is_bigendian` is the emulated CPU's byte order, line 1064) | codex | ACCEPTED | wording |
| F12 | S14's population: the census counts the tree the battery runs in, which holds the peer's untracked `lca_isaphys_probe.py`; tracked HEAD was 77 = the old pin; the committed defect was the NAME SET (`wdc_lba_probe.py` not grandfathered) | codex (and grok: S14 read differently after `--write`) | ACCEPTED; the follow-up landed (1.7); its CHANGELOG paragraph gains this sentence in the T18 landing | records |
| F13 | A mask conditioned on the written value's bit 0 would pass every row, because every CSR2/CSR3 stimulus (0xffff, 0x00a5, 0x0005) has bit 0 set; a dropped-bit-alone row with bit 0 clear closes it | GLM (proposed `csr2 hi` = 0x0100 -> 0) | **ACCEPTED for the register that is masked: a `csr3 hi` row (write 0x0008, HEAD 0x0008, FIX 0x0000)** -- **D4** asks whether it is OWED (floor) or OPTIONAL (clause e) | one row, 19 total |
| F14 | Under the narrowing, N9/N11/N12's FIX wants become identity (0xffff / 0xffff / 0x1235) so the rows guard against a CSR1/CSR2 mask being introduced | grok | ACCEPTED -- they are CONTRACT rows: a later C-LANCE-style change re-pins them under the oracle-correction order | the row table (4.2) |
| F15 | The #572 hygiene omission is its own commit, before this round lands | GLM, DeepSeek, grok, codex | DONE -- `2956c32d` (1.7) | -- |
| F16 | MANIFEST lines for the frozen copies: both `.py.txt` copies share a basename; say which lands as `.py` | GLM | ACCEPTED: the 17-row WITNESS copy lands as `witness_20261025/le_csrmask_probe.frozen.py` (CLASS_WITNESS); the pass-1 copy stays `.py.txt` (it is the shipping file's own revision, not a separate instrument) | the landing checklist |
| F17 | The gate block needs its OWN reason line; cite `gate_arm.sh`'s accretion discussion (1289-1300: "it has become the tree's general DEVICE-probe gate by accretion"), not the cats/stub paragraph | GLM, codex | ACCEPTED | the gate block's comment |
| F18 | R13's "same script" is the shipping revision; name both directories (`witness_20261025/`, the detector re-measure) and say which carries `probe:` | GLM, codex | ACCEPTED | the witness term's text |
| F19 | Null medium: "by construction, leg not run" until measured | codex | RESOLVED -- measured (1.6); it will be re-measured on the shipping revision | -- |
| F20 | Filings: D4's two behaviours as two rows (STOP gating; CSR3 cleared on STOP plus the Am7990's CSR1/CSR2-not-preserved note); row 9 does not carry the second; the carrier's source list; the Am7990 datasheet proper | grok, DeepSeek, GLM, codex | ACCEPTED; plus F10's row and F1's CSR1/CSR2 read-back row | the landing's filings (4.6) |
| F21 | No third recent hygiene omission (#570/#571 detectors use `subprocess.run`, not `pty.fork`) | codex, GLM | NOTED | -- |
| F22 | M4's description was wrong: "Write as zeroes" means the write is accepted with zeros stored, not declined | GLM | ACCEPTED | the option-set text |
| F23 | V16's "CSR0 also masked" is false (slot 0 is never used); V12 differs in initialised device data too, not only the warning | codex | ACCEPTED (V16 dropped; V12' restated) | the variant table |
| F24 | A one-halfword window shift lands RDP on an unimplemented offset (ports are 4 bytes apart); a one-WORD shift exchanges them; N5/N6 red either way | grok, codex, GLM | ACCEPTED | the contract's anchor sentence |
| F25 | (placeholder) Gemini 4 Argon's pass-1 answer -- not in when this packet was written; it will be adjudicated in the same way when it lands | -- | PENDING | -- |

---

## 3. Disagreements D1-D5 -- both sides, my ruling, its warrant.  Parties: adjudicate your OWN dispute.

**D1 -- which masks ship.**
* *All three, as a model policy* (GLM Q12: "Ship 0xfffe, but the contract and CHANGELOG must record it as an interpreted
  reading"; the research row and rpajarola's commit).
* *CSR3 only* (grok: "CSR1 0xfffe and CSR2 0x00ff are not established for the Am7990 the 3100 carries, and the detector's
  FIX column would freeze them"; codex: "The record must distinguish that warrant from a proven answer to P1"; DeepSeek:
  NOT READY on P1).
* **Ruling: CSR3 only.**  Warrant: 1.1 (the Am7990 manual specifies read-as-zero for RAP and CSR3 and NOT for CSR1/CSR2),
  1.3 (an independent emulator keeps CSR1/CSR2 writable on the Am7990 on the strength of a hardware diagnostic for an
  Am7990 board), 1.2 (the two chips are documented to differ in CSR1/CSR2), 1.5 (every machine this model serves is
  believed to carry the Am7990).  The counter-evidence (1.4, a DEC PROM test that passes with the masks) is on a machine
  this fork does not emulate the LANCE of and whose part is not established; if the KN02-BA carries a C-LANCE the two
  readings are consistent -- a per-chip flag like MAME's `type()` would be the port, filed.  **Where I might be fooling
  myself:** MAME's note is a comment about a diagnostic's requirement, not the diagnostic itself; neither manual states
  CSR1/CSR2's read-back; and narrowing a research row filed as "port e108b54" is a scope change the owner reads in the
  status line.

**D2 -- floor grading of the kept/dropped cells** (F5).  Codex: clause (e) obligations, labels are the floor siblings;
grok/GLM/DeepSeek: floor.  **Ruling: REFINED** -- for a constant AND mask the body "tests" every bit it keeps or drops,
so {kept, dropped} is the body-induced partition of the written value, and R4's "labels as siblings" holds alongside;
under the narrowing both readings owe the same rows.  Astra rules the general question for the record; nothing here
hangs on it.

**D3 -- the inverted STOP comments** (F9).  Fix both in the same change as L4 records (codex, GLM) vs file (grok: "this
round does not touch those lines").  **Ruling: fix both in-round** -- comments only, no behaviour, in the function the
round already edits; shipping a fix that cites the datasheet beside two comments that invert it is the confusion L4
exists to prevent.  The Ultrix observations stay, with their corrected meaning.

**D4 -- is `csr3 hi` owed or optional** (F13).  GLM: "Optional, not a floor breach" (a two-token mutant outside the named
space); the main loop: cheap and it closes a real blind spot (every driven CSR3 value had bit 0 set).  **Ruling: ADD it as
L1 construction; whether it is floor or clause (e) is for Astra** -- a filter may not demand a row, but the author may
add one before shipping.

**D5 -- N14 (`csr1 top`)**: subsumed by N11 (DeepSeek, codex, grok) vs keep as insurance (grok, codex, GLM).  **Ruling:
keep, labelled as top-edge insurance** -- it costs one read in an existing session.

---

## 4. The revised design and detector -- as DATA: check them, do not ratify them

**4.1 The product edit** (`le_register_write()`, the `default:` arm; the whole function is in the pass-1 brief 8.2).
Two forms, for the panel to choose between:

Form A (explicit CSR3 arm, the others stay in `default:`):
```c
	case 3:	/*  #573: CSR3 is BSWP|ACON|BCON; bits 15:3 "Reserved and read as 0"
		    (Am7990 Technical Manual 1-22; Am79C90 datasheet CSR3)  */
		d->reg[r] = x & 0x0007;
		break;

	default:
		/*  CSR1 and CSR2 are stored whole, as the Am7990 does: bit 0 of CSR1
		    "Must be zero" and bits 15:8 of CSR2 "Reserved" are constraints
		    on the host's writes, not read-as-zero bits (the C-LANCE reads
		    them as zero; see the #573 record).  */
		d->reg[r] = x;
	}
```
Form B: explicit `case 1: case 2:` carrying that comment, then `default:` for CSR3.  Either way: one product file, the
same bytes in `est/`, rebuilt binaries in the build trees; the odd-address warning at `le_chip_init` 180-182 STAYS (it is
reachable: CSR1 is not masked); the two STOP comments corrected (D3); `#573` tags.

**4.2 The rows** (19; one fresh emulator per session; every CSR want is a literal, the stable rows want their first
observation):

| # | row | session | stimulus | HEAD | FIX | kind |
|---|---|---|---|---|---|---|
| N1-N4 | `ram:<s>` | each | RAM round-trip 0x5a5a | 0x5a5a | 0x5a5a | control |
| N5 | `csr0 reset` | csr0 | RAP=0, read RDP | 0x0004 | 0x0004 | control (signature) |
| N6 | `rap mask` | csr0 | RAP:=0x13, read RAP | 0x0003 | 0x0003 | control (signature) |
| N7 | `csr3 all` | csr3 | write 0xffff, read | 0xffff | **0x0007** | SYMPTOM |
| N8 | `csr3 bits` | csr3 | write 0x0005, read | 0x0005 | 0x0005 | control (kept, bit 0 set) |
| N8b | `csr3 hi` | csr3 | write 0x0008, read | 0x0008 | **0x0000** | SYMPTOM (dropped boundary bit alone, bit 0 clear) |
| N9 | `csr2 all` | csr2 | write 0xffff, read | 0xffff | 0xffff | CONTRACT (stored whole) |
| N10 | `csr2 lo` | csr2 | write 0x00a5, read | 0x00a5 | 0x00a5 | control |
| N11 | `csr1 all` | csr1 | write 0xffff, read | 0xffff | 0xffff | CONTRACT (stored whole) |
| N12 | `csr1 odd` | csr1 | write 0x1235, read | 0x1235 | 0x1235 | CONTRACT (bit 0 stored) |
| N13 | `csr1 even` | csr1 | write 0x1236, read | 0x1236 | 0x1236 | control |
| N14 | `csr1 top` | csr1 | write 0x8000, read | 0x8000 | 0x8000 | control (insurance) |
| N15-N18 | `stable:<s>` | each | the ALL value read again at once | = first | = first | control |

Pre-fix GATE (FIX column) predicted **17/19** (N7, N8b red); fix 19/19; null medium 0/19.

**4.3 Variants under the narrowed fix** (classify: DETECTED with its red rows / EQUIVALENT / OUT OF CONTRACT):

| # | variant | predicted red rows | class |
|---|---|---|---|
| V1' | the CSR3 store reverted to `x` (= HEAD; the one fixed site) | N7 (0xffff), N8b (0x0008) | floor (a)/(b) |
| V7' | CSR3 mask 0x000f | N7 (0x000f), N8b (0x0008) | DETECTED |
| V8' | CSR3 mask 0x0003 | N7 (0x0003), N8 (0x0001) | DETECTED |
| V9' | CSR3 mask 0x0006 | N7 (0x0006), N8 (0x0004) | DETECTED |
| V10' | the CSR3 store writes the constant 0x0007, ignoring `x` | N8 (0x0007), N8b (0x0007) | DETECTED |
| V21 | a CSR1 mask 0xfffe introduced | N11 (0xfffe), N12 (0x1234) | DETECTED -- the contract rows |
| V22 | a CSR2 mask 0x00ff introduced | N9 (0x00ff) | DETECTED -- the contract row |
| V23 | CSR3 OR-accumulated (`\|= x & 0x0007`, no clear) | N8 (0x0007), N8b (0x0007) | DETECTED |
| V24 | the CSR3 mask applied only when bit 0 of `x` is set | N8b (0x0008) | DETECTED -- the row F13 added |
| V25 | the CSR3 mask applied at the CSR2 label instead (labels swapped) | N7 (0xffff), N8b (0x0008), N9 (0x0007), N10 (0x0005) | DETECTED |
| V12' | the mask applied at the RDP read instead of the store | none | EQUIVALENT in every state (no model code reads `reg[3]`) -- disclosed |
| V13' | the mask conditioned on STOP being set | none (STOP set throughout) | OUT OF CONTRACT -- disclosed |
| V14' | the mask conditioned on a 16-bit access width | none (every write is `sh`) | OUT OF CONTRACT -- disclosed |
| V20 | null medium `/bin/false` | all 19, CONTROL=FAIL | floor (c), re-measured |

**4.4 The contract** (goes into the probe's header, F7): CATCHES -- any change to the CSR3 mask constant (N7); a CSR3
store that ignores the written value (N8, N8b); a mask conditioned on the written value's low bit (N8b); the CSR3 mask
moved to another label (N7/N9/N10); a CSR1 or CSR2 mask introduced (N9, N11, N12 -- the stored-whole contract, re-pinned
under the oracle-correction order if a C-LANCE model variant is ever added); the revert.  OUTSIDE -- the mask applied at
the read instead of the store (no observable differs); a mask conditioned on STOP (all rows run with STOP set); on access
width (all writes 16-bit); the CSR0 arm; INIT and `init_block_addr`; the big-endian emulated machines.  ANCHOR -- `csr0
reset` and `rap mask` pin the two ports by the reset value and the RAP masking: a one-word window shift exchanges them,
a one-halfword shift lands RDP on an unimplemented offset; either reds N5 and N6.

**4.5 The table legs**: L0 pre-fix GATE (17/19), L1 fix GATE (19/19), L2 two-leg (base vs HEAD column, fix vs FIX column,
the `probe:` warrant), L3 null medium, then V7'-V10', V21-V25 on the fix clone; all in `cp -a` clones under `/tmp`, never
`build/`; `PRETABLE.out` before L0; logs copied to `regress/artifacts/lecsrmask/killtable_20261025/`.

**4.6 Filings** (rows, not this round's edits): (a) `lecsr12readback` -- CSR1 bit 0 / CSR2 15:8 read-back: the Am7990
stores them (1.1, 1.3) and the C-LANCE reads them as zero (1.2, 1.4); a per-chip model flag is the port if a C-LANCE
instance (the 3MIN's IOASIC LANCE) is ever added; (b) `lestopgate` -- CSR1-3 accessible only with STOP set, the model
accepts them always; (c) `lecsr3stopclear` -- CSR3 cleared by STOP (and the Am7990's CSR1/CSR2 not preserved across it);
(d) `lerapfmt` -- F10's format mismatch; (e) the carrier's primary-source list not descending into `_scratchpad/lance/`.

**4.7 Records**: the CHANGELOG block claims the rung-3 witness (unmodified `pmax -e 3100`, before the edit, order shown by
the artifacts' own timestamps and md5s); CSR3 `& 0x0007` with 1.1/1.2 lines; CSR1/CSR2 left stored whole and WHY (1.1,
1.3, 1.4); the narrowing of the research row and the filed sibling; the STOP comments corrected; what the detector
catches and does not; the floor legs with their artifacts; the two-column judging convention.  It does NOT claim that any
shipped driver observes the defect, nor that the Am7990 manual says CSR1/CSR2 read as zero.

---

## 5. Still OWED, and where I might be fooling myself

* The narrowing (D1) rests on a comment in another emulator about a diagnostic, on manual silence, and on a chip-identity
  belief for four machines; the strongest counter-evidence (1.4) is unverified as to chip.  A seat with a primary source
  on the KN01's, PMAD-AA's or KN02-BA's LANCE part, or on the RS2030 diagnostic, settles it.
* The detector's CSR1/CSR2 rows now PIN a behaviour the manuals leave unspecified; that is a contract, stated as one.
* Nothing has been built or measured on the narrowed design yet: 4.2's 17/19 and 4.3's red sets are PREDICTIONS; the
  revised probe will be re-measured on the HEAD clone (HEAD column) and the floor legs re-run before the table.
* Argon's pass-1 answer (F25) and Fable's held question are outstanding; this ruling is provisional on them.
* The pass-1 brief's roster line called Opus "NOT FIRED as a review seat" and this round used no sub-agent at all --
  consistent, but say so if you read it otherwise.

## 6. The three questions

1. **Adjudicate F1-F25 and D1-D5** -- UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with the reason.  For D1
   say which evidence item in section 1 you weigh most and why.
2. **WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?**  Twenty accepted, five ruled my way.
3. **WHAT DID ALL OF US MISS?**  You now have every seat's output (the pass-1 directory) and the verified facts of
   section 1.
