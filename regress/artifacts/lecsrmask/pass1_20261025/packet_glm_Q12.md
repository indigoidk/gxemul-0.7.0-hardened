# PASS-1 DESIGN REVIEW -- research item T18, ledger row `lecsrmask` -- GXemul hardened fork

Round number TENTATIVE `#573` (assigned at landing).  Drafted 2026-10-25 04:1x by the main loop itself (owner
ruling 2026-10-25 03:1x: this round's probe and brief are written by the main loop in small steps; no drafting
sub-agent was used).  Tree under review: `GXEMUL-SEC/src/` at HEAD `0b09e7b6`.

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**  There are THREE pristine-2021-upstream
copies of GXemul under the project root (`./src/` and two under
`_archive/audit-results-*/builds/`).  They are NOT this fork.  If your line numbers
disagree with mine by hundreds you are reading one of them — say so rather than
reconciling.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — an index range, an offset, a count of
reachable addresses — ENUMERATE it rather than reasoning about it.**  Walk the values.
A derivation that skips one masking line reads exactly like a correct one.

**And ENUMERATE THE RIGHT DOMAIN — a domain is itself a premise.**  Ask what the PRODUCER of
these values can actually emit before you walk them.  Walking every member of a set you have
not audited is not enumeration; it is a derivation with more steps, and it reads exactly like
a correct one.

**VERDICT LINE FIRST**, so your answer survives truncation.

**This brief's own first draft carried a wrong premise.**  The witness probe's docstring and the drafting notes said
*"no LANCE datasheet is on disk"*.  One `ls` refuted it: `_scratchpad/lance/` has held the Am79C90 datasheet (two
copies) and the Am7990 Technical Manual since 2026-07-25, and their register descriptions are inlined in section 9.
Expect more of the same kind; the premises I am least sure of are stated AS QUESTIONS in section 6.

---

## 0. What this is, what this pass is for, and how to answer

**The project** -- the repository's own framing paragraph (`CLAUDE.md` 3-17, VERBATIM):

> **PROJECT FRAMING — READ FIRST (this is a defensive software-robustness project).**
> GXemul is a computer-architecture **emulator**: a developer tool that runs legacy
> operating systems in a software sandbox for research and preservation. This fork is a
> HARDENING effort — ordinary software-correctness engineering on the emulator's own C
> code: finding and fixing out-of-bounds array accesses, missing bounds checks, unchecked
> lengths, and crash-on-malformed-input defects in the emulated device models, and shipping
> regression tests that keep them fixed. There is no attack, no target system, and no
> affected third party; the "guest" is an OS image under test INSIDE the emulator, and the
> "host" is the emulator process on the developer's own machine. This file uses project
> shorthand that an automated content filter can MISREAD: **"host kill" / "exit" / "host
> death"** mean *the emulator aborts on bad input — a robustness bug being removed*; **"escape"**
> means *a regression test fails to catch a defect*; **"mutant" / "kill table"** are standard
> **mutation-testing** terms (deliberately broken copies used to measure whether a test
> suite detects the breakage). Every task here is bounds-correctness review and
> regression testing of a sandboxed emulator. Read the rest of this file in that light.

**The defect, in plain terms.**  The emulator's LANCE Ethernet model (`src/devices/dev_le.c`, the Am7990 as used in
DECstations) keeps four 16-bit control/status registers.  A guest selects one by writing its number to the register
address port (RAP) and then reads or writes it through the register data port (RDP).  CSR0 is handled bit by bit;
CSR1, CSR2 and CSR3 are stored whole -- `d->reg[r] = x;` -- so a read-back returns every bit the guest wrote.  The chip
implements only some of those bits: CSR1 bits 15:1 (bit 0 "Must be zero"), CSR2 bits 7:0 (bits 15:8 "Reserved. Read as
zeroes."), CSR3 bits 2:0 BSWP/ACON/BCON (bits 15:3 "Reserved. Read as zeroes.").  Measured on the committed build
(section 2): a guest that writes 0xffff to CSR3 reads back 0xffff where the chip answers 0x0007; CSR2 0xffff reads
0xffff (chip 0x00ff); CSR1 0xffff reads 0xffff (chip 0xfffe) and CSR1 0x1235 reads 0x1235 (chip 0x1234).  A
WRONG-RESULT class defect: no process termination, no memory-safety consequence -- a register read-back that disagrees
with the hardware.

**The defect, in the repository's own words** (each quotation VERBATIM; section 1 carries the sources):

* The site (`dev_le.c` 884-886): *"`default:`"* / *"`/*  CSR1, CSR2, and CSR3:  */`"* / *"`d->reg[r] = x;`"*.
* The research record (`A_github_forks.md` row 26): *"CSR1 &= 0xfffe, CSR2 &= 0x00ff, CSR3 &= 0x0007 (only the
  implemented bits)."* ... *"devices/dev_le.c:884-886 stores all 16 bits."*
* The datasheet (`am79c90_bitsavers.txt` 1162-1163, CSR2 bits 15:08): *"RES   Reserved. Read as zeroes. Write as
  zeroes."*; (1222-1223, CSR3 bits 15:03): *"RES  Reserved. Read as zeroes. Write as zeroes."*; (1138-1142, CSR1):
  *"15:01    IADR  The low order 15 bits of the address"* ... *"00"* ... *"Must be zero."*

**This pass.**  PASS 1: a design review BEFORE any product edit.  **The rung-3 witness EXISTS and was MEASURED on the
committed build** (section 2): 17/17 rows passed the committed-build (HEAD) column, with the three symptom rows showing
the stored bits; the shipping detector revision (18 rows) was then re-measured 18/18 against the same column.  Section
3 is the design and its sources; section 5's premises are settled (each re-read at HEAD in THIS scope, with its line);
section 6 states the ones I am least sure of AS QUESTIONS; section 7 is my partition, my floor cells, the rows I propose
and the variants I classify -- as DATA: check them, do not ratify them.  The whole enclosing function of every proposed
edit (`le_register_write()`, and `DEVICE_ACCESS(le)` for the alternative that masks at the read) is inlined in
section 8.

**Hard limits.**  READ-ONLY.  Do not build, run, copy or modify anything in the repository.  Nobody is asked to write a
guest program, a probe or a code variant: where a question needs a construction, this brief supplies one (7.4 rows,
7.5 variants) and asks you to check or classify it, or asks which inputs a repair changes the answer for.

**Reading scope (seats that can read files).**  `GXEMUL-SEC/src/` (in particular `devices/dev_le.c`,
`include/thirdparty/if_lereg.h`, `include/thirdparty/dec_kn01.h`, `machines/machine_pmax.c`,
`devices/dev_turbochannel.c`, `devices/dev_luna88k.c`, `cpus/memory_rw.c`); the top-level `GXEMUL-SEC/regress/*.py`
and `*.sh`; `GXEMUL-SEC/tools/pipeline/check_probe_wiring.py` and `GXEMUL-SEC/tools/derive_hygiene_pins.sh`; and THESE
artifact files only -- the witness, `GXEMUL-SEC/regress/artifacts/lecsrmask/witness_20261025/` (`RESULTS_base.txt`,
`RUN_IDENTITY.txt`, `le_csrmask_probe.frozen.py.txt`, `raw/`), the detector revision under review,
`GXEMUL-SEC/regress/artifacts/lecsrmask/pass1_20261025/le_csrmask_probe.frozen.py.txt` and its HEAD-column re-measure
`pass1_20261025/det18_HEAD/RESULTS_base.txt`, and from the research record `GXEMUL-SEC/regress/artifacts/research_20261022/`
the files `A_github_forks.md` and `TRIAGE.md`.  **Do not read anything else under `GXEMUL-SEC/regress/artifacts/` -- in
particular nothing else in `lecsrmask/pass1_*/`, where the other seats' answers to THIS brief land -- and do not read
`GXEMUL-SEC/tools/pipeline/ledger.json`, `CHANGELOG.md` or `OUTSTANDING_BUGS.md`:** what this brief needs from them is
inlined VERBATIM (sections 1, 5, 8).  The files outside the repository are cited by ABSOLUTE path:
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\lance\am79c90_bitsavers.txt` (Am79C90 C-LANCE datasheet, AMD, "PRELIMINARY"),
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\lance\am79c90_mit.txt` (a second copy of the same datasheet),
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\lance\TM1986.txt` (Am7990 LANCE Technical Manual, AMD, 1986),
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\lance\lance_nb.c` (NetBSD `dev/ic/lance.c`) and
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\lance\linux_declance.c` (Linux `drivers/net/ethernet/amd/declance.c`); their
load-bearing lines are in section 9.

**The working tree is not clean.**  At drafting, 20 tracked files differed from HEAD (other sessions' work):
`regress/artifacts/recordfix_20261002/chk_hrec.py.txt`, `regress/diff_wdc_identify.c`, `regress/gate_offline.sh`,
`regress/gate_sh_rounding.sh`, `regress/gdrom_default_probe.py`, `regress/sh4_chcr_probe.py`,
`regress/wdc_addtoinbuf_probe.py`, `src/cpus/cpu_alpha_palcode.c`, `src/devices/dev_lca.c`, `src/devices/dev_pcc2.c`,
`src/devices/dev_sh4.c`, `src/include/thirdparty/mvme_pcctworeg.h`, `tools/BRIEF_TEMPLATE.md`, `tools/CLAUDE.md`,
`tools/PIPELINE.md`, `tools/adjudicate.sh`, `tools/panel.sh`, `tools/pipeline/check_probe_wiring.py`,
`tools/pipeline/fable_queue.md`, `tools/pipeline/ledger.json`.  None of the five under `src/` is on the pmax/LANCE path.
`src/devices/dev_le.c` is byte-identical at HEAD, in the working tree and in the `est/` twin (`cmp`, section 4), and the
witness binary was built from a git-archive export of HEAD -- committed bytes, not the working tree.  Untracked and
this round's own: `regress/artifacts/lecsrmask/`.  (`regress/lca_isaphys_probe.py` is another session's untracked probe.)

**The roster for this pass** (the T4 launcher is the shape; owner rulings 2026-10-23/24/25), so that a missing answer is
read as what it is:

| seat | transport | class | packet |
|---|---|---|---|
| GLM 5.3 (`glm-5.3:cloud`) | Ollama cloud | PACKET-FED | the PACKET form, two firings: Q1+Q2, then Q3+Q4 |
| DeepSeek (`deepseek-v4-pro:cloud`) | Ollama cloud | PACKET-FED | the PACKET form, two firings: Q1+Q2, then Q3+Q4 |
| Grok 4.7 (xhigh, plan mode) | `grok --prompt-file` | FILE-READING | FULL |
| Gemini 4 Argon (`gemini-4-argon-high`) | agy, `--add-dir GXEMUL-SEC` | FILE-READING | FULL (pointer) |
| GPT-6 Astra | codex, pointer form | FILE-READING | FULL; then ADJUDICATES the consolidated findings |
| Fable 5.1 | -- | HELD (owner's hold of 2026-10-21, still in force 2026-10-25) | its question is recorded; the cloud route may carry it |
| kimi, minimax | -- | NOT FIRED | not on this roster |
| Opus 5.5 | -- | NOT FIRED | not on this roster; no sub-agent was used this round |

A seat that does not answer is a SEAT FAILURE; a seat deliberately not fired is neither a failure nor agreement.

**Answer format -- VERDICT LINE FIRST:**
~~~~
VERDICT: READY | READY WITH CHANGES | NOT READY -- <one line>
Q1: <one line>   Q2: <one line>   Q3: <one line>   Q4: <one line>
~~~~
Then one section per question.  Mark each claim READ (you opened the source), DERIVED (from this packet) or NOT
CHECKABLE.  Cite by number: settled premises S1-S16, premises P1-P12, cells C1-C6, rows N1-N18, variants V1-V20, the
sources' points of difference D1-D4 (3.4) and the rules R1-R21 (section 10).

---

## 1. The defect -- as the ledger row and the research record it

**1.1 The ledger row** (`tools/pipeline/ledger.json`, row `lecsrmask`, VERBATIM):

> id `lecsrmask` · sev `MED` · opened `2026-10-22` · state `open` · witness `none`
> title: *"devices/dev_le.c:le_register_write -- CSR1-3 store all 16 bits (implemented-bit masks missing) --
> WRONG-RESULT"*
> state_note: *"Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row
> T61 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: one-line; report rows: A2-26).
> Source URLs: https://github.com/rpajarola/gxemul/commit/e108b546b2e6217ad30bb688b4cbb029755ce230.  Our site at
> de8c7547: src/devices/dev_le.c:884-886.  Portable fix: yes -- port rpajarola e108b54.  Filing check (TRIAGE.md): 0
> hits.  witness: none -- research finding, not yet reproduced here."*

(The `witness: none` is the state at filing; section 2 is the witness this round measured.)

**1.2 The research record** (`regress/artifacts/research_20261022/A_github_forks.md`, VERBATIM):

> `| 26 | https://github.com/rpajarola/gxemul/commit/e108b546b2e6217ad30bb688b4cbb029755ce230 (CSR1-3) | dev_le.c
> le_register_write | CSR1 &= 0xfffe, CSR2 &= 0x00ff, CSR3 &= 0x0007 (only the implemented bits). | CORRECTNESS |
> STILL OPEN | devices/dev_le.c:884-886 stores all 16 bits. |`

Its sibling in the SAME function, filed separately and NOT this round's (row 9, VERBATIM, for scope):

> `| 9 | https://github.com/rpajarola/gxemul/commit/d1f0720ac94c3a261bbecca8e870addc9c106556 (STOP/STRT) | dev_le.c
> le_register_write | Setting STOP resets CSR0 to STOP alone, as on the Am7990. STRT turns TXON/RXON back on unless
> DTX/DRX is set. | CORRECTNESS | STILL OPEN | STOP clears only STRT+INIT (devices/dev_le.c:873-877); STRT does not set
> TXON/RXON (:862-865); le_register_fix keeps the "Works with Ultrix" variant that clears only IDON (:803-812).
> rpajarola reports that Ultrix 4.5 and the BSDs still work with the datasheet behaviour. |`

**1.3 The triage row** (`TRIAGE.md` 92, VERBATIM):

> `| T61 | `devices/dev_le.c:le_register_write` -- CSR1-3 store all 16 bits (implemented-bit masks missing) --
> WRONG-RESULT | dev_le.c:884-886 | K | UNFILED (0 hits) | one-line | port [rpajarola e108b54](...) (Y) | A2-26 |`

**1.4 The site** (`dev_le.c`, VERBATIM; the whole function is in 8.2):

```c
	default:
		/*  CSR1, CSR2, and CSR3:  */
		d->reg[r] = x;
	}
```

---

## 2. The witness -- MEASURED on the committed build, before any product edit (VERBATIM)

**2.1 Identity** (`regress/artifacts/lecsrmask/witness_20261025/RUN_IDENTITY.txt`, VERBATIM):

```
RUN_IDENTITY -- T18 lecsrmask WITNESS (rung 3: guest instructions on the UNMODIFIED pmax -e 3100, before any product edit)
run dir        /tmp/gxt18/witness_034758   (2026-10-25 03:49:18)
binary         /tmp/gxt17/base/gxemul  md5 6c27af7b04742d72385426e304633c99  built 2026-10-25 03:47:49.519713686
sources        a git-archive export of HEAD 0b09e7b6 (top-level files, src, experiments, man, doc, demos, test), ./configure && make -j4 in WSL Gentoo
dev_le.c       md5 3eab9c96d4823113941271ad415daf5d  (the default-arm store 'd->reg[r] = x;' present x1)
probe          le_csrmask_probe.frozen.py.txt  md5 df5ab57408d1db812d66bb0b42564fb0  482 lines (kept as .py.txt until the landing's MANIFEST entry names it)
result         LE_CSRMASK_RESULT_base=17/17  LE_CSRMASK_CONTROL_base=OK
```

**2.2 The run** (`witness_20261025/RESULTS_base.txt`, VERBATIM):

```
======================================================================================
lecsrmask -- RUNG-3 WITNESS + DETECTOR on unmodified `pmax -e 3100` (KN01 LANCE CSR1-3)
======================================================================================
date      2026-10-25 03:47:58
machine   pmax -e 3100 (DECstation 3100, KN01)   LITTLE endian   (machine desc UNMODIFIED)
lance     registers physical 0x18100000; RDP KSEG1 0xffffffffb8100000, RAP +4
base bin  /tmp/gxt17/base/gxemul
fix bin   (none -- WITNESS run)

--------------------------------------------------------------------------------------
LEG base -- base build, judged against the HEAD column
--------------------------------------------------------------------------------------
    [base_csr0] /tmp/gxt17/base/gxemul -V -E pmax -e 3100 0xffffffff80100000:/tmp/gxt18/witness_034758/out/raw/base_csr0.bin
    encodings: 15/15 words, 14/15 mnemonics agree with the disassembler
    parked at 0xffffffff80100034: yes   (1.52 s)
    [base_csr3] /tmp/gxt17/base/gxemul -V -E pmax -e 3100 0xffffffff80100000:/tmp/gxt18/witness_034758/out/raw/base_csr3.bin
    encodings: 17/17 words, 15/17 mnemonics agree with the disassembler
    parked at 0xffffffff8010003c: yes   (1.51 s)
    [base_csr2] /tmp/gxt17/base/gxemul -V -E pmax -e 3100 0xffffffff80100000:/tmp/gxt18/witness_034758/out/raw/base_csr2.bin
    encodings: 17/17 words, 15/17 mnemonics agree with the disassembler
    parked at 0xffffffff8010003c: yes   (1.51 s)
    [base_csr1] /tmp/gxt17/base/gxemul -V -E pmax -e 3100 0xffffffff80100000:/tmp/gxt18/witness_034758/out/raw/base_csr1.bin
    encodings: 20/20 words, 19/20 mnemonics agree with the disassembler
    parked at 0xffffffff80100048: yes   (1.51 s)

  row          got        head       fix       
  ram:csr0     0x5a5a     want 0x5a5a     ok
  ram:csr3     0x5a5a     want 0x5a5a     ok
  ram:csr2     0x5a5a     want 0x5a5a     ok
  ram:csr1     0x5a5a     want 0x5a5a     ok
  csr0 reset   0x0004     want 0x0004     ok
  rap mask     0x0003     want 0x0003     ok
  csr3 all     0xffff     head 0xffff   fix 0x0007   [HEAD] ok
  csr3 bits    0x0005     want 0x0005     ok
  csr2 all     0xffff     head 0xffff   fix 0x00ff   [HEAD] ok
  csr2 lo      0x00a5     want 0x00a5     ok
  csr1 odd     0x1235     head 0x1235   fix 0x1234   [HEAD] ok
  csr1 even    0x1234     want 0x1234     ok
  csr1 top     0x8000     want 0x8000     ok
  stable:csr0  0x0004     want 0x0004     ok
  stable:csr3  0xffff     want 0xffff     ok
  stable:csr2  0xffff     want 0xffff     ok
  stable:csr1  0x1235     want 0x1235     ok

  17/17 passed
  CONTROL=PASS
  LEG base VERDICT: PASS

LE_CSRMASK_CONTROL_base=OK
LE_CSRMASK_RESULT_base=17/17
======================================================================================
VERDICT   every leg passed its own column
LECSRMASK_PROBE_DONE
```

**What each row is.**  `ram:<s>`: a `sh`/`lhu` round-trip of 0x5a5a through KSEG0 RAM in every session -- the LIVENESS
control (the same store/load shapes that drive the device).  `csr0 reset`: RAP = 0, read RDP -> 0x0004 = `LE_STOP`,
the model's reset value -- a DEVICE-SIGNATURE control (RAM would read 0; `d->reg[0] = LE_STOP` at `dev_le_init`).
`rap mask`: write 0x13 to RAP, read RAP -> 0x0003 -- a second signature (`idata & (N_REGISTERS - 1)`).  The three
SYMPTOM rows print BOTH columns: `head` is what the committed build stores, `fix` what the chip holds; on the HEAD column
they pass because the committed build is being judged against itself (test-first: the same script, judged against the
FIX column, is the detector's pre-fix RED -- 7.7 leg L0).  `stable:<s>`: the first RDP value read a second time.
"14/15 mnemonics" counts the disassembler's RENDERING of each word against the probe's mnemonic string; the WORD
comparison (15/15) is the control, the mnemonic a secondary rendering (the `b 0x` self-loop and `ori` vs `li` renderings
account for the misses).

**2.3 The shipping detector revision -- re-measured.**  After the witness, two L1 (pre-ship construction) changes were
made to the probe and it was re-run on the same clone, HEAD column:

* `csr1 even` now drives **0x1236** (bit 1 SET -- the kept boundary bit of the 0xfffe mask) instead of 0x1234; a mask
  narrowed to 0xfffc reds it, which 0x1234 would have passed.  Rule D2 (R5) applied at the shipping revision.
* a **`csr1 all`** row (write 0xffff, read; HEAD 0xffff, FIX 0xfffe) for SIBLING PARITY with the `csr2 all` / `csr3 all`
  rows: the write-all-ones row reads back exactly the mask, so ANY single change to that register's mask reds it.
* the docstring's false "no LANCE datasheet is on disk" was replaced by the datasheet citations (section 9).

Re-measured 2026-10-25 04:0x on binary `6c27af7b` (the witness binary, unchanged): **18/18 passed, CONTROL=PASS,
`LE_CSRMASK_RESULT_base=18/18`**, the four symptom rows reading `0xffff / 0xffff / 0xffff / 0x1235` against FIX wants
`0x0007 / 0x00ff / 0xfffe / 0x1234`.  Preserved at `regress/artifacts/lecsrmask/pass1_20261025/det18_HEAD/RESULTS_base.txt`;
the revision under review is the frozen copy `pass1_20261025/le_csrmask_probe.frozen.py.txt` (its md5 is in that
directory's `FROZEN.md5`).  Section 7.4 is its row table.

**2.4 ORDER.**  Witness measured 03:47-03:49; detector re-measured 04:0x; **no product edit has been made** --
`dev_le.c` is md5 `3eab9c96` at HEAD, in the working tree and in the clone.  The ladder's clause (i) (symptom on the
pre-fix committed HEAD, green post-fix with the same script) is discharged by 7.7's legs L0/L1/L2, which run after the
edit; the `probe:` witness term (R13) is claimed only once L2 is green.

---

## 3. The design and its sources -- and where they differ

**3.1 The proposed edit** (a SKETCH until checked against the whole function, 8.2; `#573` tentative).  Replace the
`default:` arm of `le_register_write()`:

```c
	case 1:	/*  #573: CSR1 is IADR[15:1]; bit 0 "Must be zero" (Am79C90 CSR1)  */
		d->reg[r] = x & 0xfffe;
		break;

	case 2:	/*  #573: CSR2 is IADR[23:16]; bits 15:8 "Reserved. Read as zeroes."  */
		d->reg[r] = x & 0x00ff;
		break;

	default:	/*  #573: CSR3 is BSWP|ACON|BCON; bits 15:3 "Reserved. Read as zeroes."  */
		d->reg[r] = x & 0x0007;
	}
```

`r` is `d->reg_select`, which the RAP arm stores as `idata & (N_REGISTERS - 1)` (S1), so `default:` after explicit
`case 1:` and `case 2:` is exactly CSR3.  **Alternative form (B):** one table,
`static const uint16_t le_csr_wmask[N_REGISTERS] = { 0xffff, 0xfffe, 0x00ff, 0x0007 };` and
`d->reg[r] = x & le_csr_wmask[r];` in the existing `default:` arm -- a one-line diff whose index-0 entry is never used
(CSR0 is `case 0:`), which is the argument against it.  Both are "port rpajarola e108b54" in substance; the research row
records his masks, not his form.

**3.2 The consumer that changes.**  `le_chip_init()` (8.1, line 179) builds `init_block_addr = (d->reg[1] & 0xffff) +
((d->reg[2] & 0xff) << 16)` and at 180-182 warns `"WARNING! address not word aligned?"` when it is odd.  With CSR1's
bit 0 dropped at the store, that condition can never be true: **the check becomes unreachable code**.  Options:
(i) delete the three lines, recording the datasheet reason at the store; (ii) leave it (a check that cannot fire --
this project's own "check-that-cannot-fail" class, i.e. a wrong record in product code); (iii) move the diagnostic to
the CSR1 store, latched `(once)`, firing when a guest writes bit 0 set (the datasheet's "Must be zero" being violated).
**Proposal: (i)**, in the same change (R14: L4-adjacent -- product code asserting a check the fix makes impossible).
The `(d->reg[2] & 0xff)` in the same expression becomes redundant but harmless; left alone.

**3.3 Who else runs this model.**  `dev_le_init` is called from `machine_pmax.c` for the KN01 (3100, line 129) and the
KN230 (line 708), from `dev_turbochannel.c:227` (the PMAD-AA option on the 5000/200), and from `dev_luna88k.c:1086`
(a big-endian host; `is_bigendian` affects SRAM byte order only, 8.1).  The register path is shared, so the fix changes
CSR1-3 read-back on all of them.  The witness machine (3100) is the one every DECstation gate boots.

**3.4 Sources, and where they differ (D1-D4).**

* **D1 -- CSR1 bit 0.**  The Am79C90 datasheet says bit 0 *"Must be zero."* -- a constraint on what the host WRITES --
  and its register figure draws the bit as `'0'`; it does NOT say "read as zeroes" for it, as it does for CSR2 15:8 and
  CSR3 15:3.  rpajarola masks it (`&= 0xfffe`).  The weakest of the three premises (P1).
* **D2 -- which chip.**  The DECstation 3100 carries the Am7990 (LANCE); the two datasheets on disk are the Am79C90
  (C-LANCE, "PRELIMINARY").  The Am7990 Technical Manual (1986) draws the same layout (CSR1 `IADR` with a `0` at bit 0;
  CSR2 `RES` / `IADR` split at 8; CSR3 `RES` / `BSWP ACON BCON`) and says *"CSR3 is cleared"* by reset and *"CSR1, CSR2
  undefined by reset"*, but its extracted text carries no "read as zeroes" sentence (P2).
* **D3 -- the drivers never set the bits.**  NetBSD `lance.c` writes `LE_CSR1, a` / `LE_CSR2, a >> 16` / `LE_CSR3,
  sc->sc_conf3`; Linux `declance.c` writes `leptr & 0xFFFF` / `leptr >> 16` / `lp->busmaster_regval` (9.3).  With a
  24-bit DMA address `a >> 16` has bits 15:8 clear, so a shipped driver never observes the defect; a guest sees it only
  by reading back after writing unimplemented bits (a diagnostic, a PROM self-test, a probe).  The severity MED stands on
  that reading (P10).
* **D4 -- what the datasheet says that the model does not do, and this round does NOT touch:** CSR1-3 are *"Accessible
  only when the STOP bit of CSR0 is a ONE"* (the model accepts them always -- the comment at 996-1001 says Ultrix writes
  them with STOP clear); *"CSR3 is cleared by RESET or by setting the STOP bit in CSR0"* (the model's `le_register_fix`
  clears only IDON on STOP, "Works with Ultrix", 802-812); *"CSR1, CSR2 undefined by reset"* (the model zeroes them).
  Filing candidates (Q3e), not rows.

**3.5 The option set** -- for a WRONG-RESULT register decode, not the de-fatalisation set (R11):
**M1 mask at the store** (3.1; rpajarola's form; the stored value IS the chip's value, so every reader of `reg[]` sees
it) · **M2 mask at the read-back** (`DEVICE_ACCESS(le)` `case 0:` read, 8.3: `odata = d->reg[sel] & mask[sel]`; the
stored value keeps the written bits and the INIT consumer keeps its parity check live) · **M3 both** ·
**M4 decline-and-announce a write that sets reserved bits** (the datasheet's "Write as zeroes" violated -- an addition
needing a warrant under R10; no shipped driver does it, so none is offered) · **M5 document only**.  **Proposal: M1.**
Grep the fork for the existing idiom before choosing (Q1d): the nearest precedent I know is `#572`'s select-byte
read-back (`dev_wdc.c`, `sdh_resv = idata & 0xa0`), which stores the implemented bits at the write.

---

## 4. Section C0 -- has this round already shipped?  NO.

```
$ git log -1 --format='%h %ad %s' --date=short -- src/devices/dev_le.c
5bf592d6 2026-07-26 Round 43 (#274, #275): LANCE -- descriptors held forever instead of dropped or failed
$ grep -c lecsrmask CHANGELOG.md
0
$ ls regress/ | grep -iE '^le_|lance|csrmask'
(nothing)
$ cmp src/devices/dev_le.c ../est/src/devices/dev_le.c && echo IDENTICAL
IDENTICAL
$ git status --porcelain -- src/devices/dev_le.c
(clean)
```

---

## 5. SETTLED PREMISES -- re-inlined so nobody spends an answer re-deriving them

Settled by this round's drafting, each RE-READ at HEAD `0b09e7b6` in THIS scope (line numbers as read; the same in the
working tree) or by the witness run (section 2):

* **S1** `le_register_write()` 839-888: `case 0:` handles CSR0 bit by bit (844-882); `default:` stores whole, 884-886.
  Its only caller is `DEVICE_ACCESS(le)` line 1002, passing `d->reg_select`; the RAP write arm stores
  `d->reg_select = idata & (N_REGISTERS - 1)` (1015) with `N_REGISTERS` 4 (79) -- so `r` is always in {0,1,2,3} and
  `default:` serves exactly CSR1, CSR2, CSR3.  (Measured: `rap mask` 0x13 -> 0x0003.)
* **S2** `uint16_t reg[N_REGISTERS]` (99); `x` is `uint32_t` (839); the store already truncates to 16 bits.
* **S3** The RDP read returns `d->reg[d->reg_select]` unmasked (981); the common tail `do_return:` writes `odata` and
  ticks the device (1036-1045).  For CSR1-3 the read-back is the guest's only direct channel.
* **S4** The register window is registered `DM_DEFAULT` at `baseaddr + 0x100000` (1108-1109); on the KN01 `baseaddr` is
  `KN01_SYS_LANCE` = 0x18000000 (`dec_kn01.h` 136; `machine_pmax.c` 129-131) -> registers at physical 0x18100000,
  RDP = KSEG1 0xb8100000, RAP = 0xb8100004, 16-bit ports.  `DM_DEFAULT` means the debugger's `dump`/`put` do not
  reach the handler, which is why the probe drives it with guest `sh`/`lhu`.  Witnessed by the two signature rows.
* **S5** Reset state: `d->reg[0] = LE_STOP` (1077) = 0x0004 (`if_lereg.h` 363); `reg[1..3]` are 0 from the `memset`
  (1060).  Measured: `csr0 reset` 0x0004.
* **S6** Readers of `reg[1..3]`: `le_chip_init` 179 builds `init_block_addr` from `reg[1] & 0xffff` and
  `reg[2] & 0xff`; 180-182 warns on an odd address; **`reg[3]` is read nowhere** (`grep -n 'reg\[3\]'` matches
  nothing; BSWP/ACON/BCON configure bus byte lanes the model does not emulate).  So CSR3's only observable is its
  read-back, CSR2's reserved byte is already invisible to the consumer, and CSR1's bit 0 reaches only the parity warning.
* **S7** `le_register_write` is non-static and has exactly one caller in the tree (1002).
* **S8** `if_lereg.h` defines `LE_CSR0..3` (344-347), `LE_BSWP 0x4` (367), `LE_MODE 0x0` (368); no ACON/BCON names
  exist in the tree.
* **S9** The datasheet lines quoted in 9.1 are READINGS of `am79c90_bitsavers.txt`, cross-checked identical in
  `am79c90_mit.txt`; whether the C-LANCE text binds the Am7990 model is P2.
* **S10** `dev_le.c` is identical at HEAD, in the working tree and in `est/` (section 4); its last change was
  `5bf592d6` (2026-07-26).
* **S11** The witness: binary `6c27af7b` built from a git-archive export of HEAD `0b09e7b6`; 17/17 HEAD column,
  CONTROL=OK; the detector revision 18/18 HEAD column on the same binary (2.1-2.3).
* **S12** The probe never writes CSR0's STRT or INIT, so every CSR1-3 write it makes happens with STOP set -- the state
  the datasheet requires for CSR1-3 access.
* **S13** Every probe write is a 16-bit `sh`: `memory_readmax64(cpu, data, 2)` (944) yields a 16-bit `idata`.
* **S14** `regress/gate_hygiene.sh` pins the count of pty-forking probes (`EXPECT_PTY_PROBES=77` at HEAD, line 388)
  and the set of promptless ones (`GRANDFATHERED_PROMPTLESS`, 414-424).  `tools/derive_hygiene_pins.sh` run read-only
  at drafting reports **got 78 vs pinned 77** and names `wdc_lba_probe.py` as NEW PROMPTLESS -- i.e. `#572`'s landing
  left gate 6 red at HEAD (an obligation of `#572`, not of this round; see Q3c).  This round's probe is also a
  pty-forking promptless probe (it drains on timeouts and watches for the breakpoint banner) and owes the same two
  edits, in the same commit as its wiring.
* **S15** `regress/gate_arm.sh` hosts non-ARM image-free `"$PMAX" gate` probes (the `sgi_re_*` family, 1603-1623 is
  one block) with `PMAX=${PMAX:-$ROOT/build/gxemul}` (80), and records why at 1070-1073 (VERBATIM): *"IT LIVES HERE,
  in the ARM gate, for the same reason m8820x_sites_probe.py lives in gate_m88k_rounding.sh: `cats` is an ARM machine
  and this gate already writes the four-byte raw stub that makes such a machine construct.  A new gate script would
  move GATE_MANIFEST, which is a bigger claim than one probe is worth."*  `run.sh` pins `GATE_MANIFEST=16`.
* **S16** `tools/pipeline/check_probe_wiring.py` holds a MANIFEST with one `(CLASS, note)` line per `.py` under
  `regress/` (artifacts included); an unlisted file is RED.  `#572`'s entry (VERBATIM, 3246-3250): *"`wdc_lba_probe.py`:
  (CLASS_DETECTOR, "#572 wdclbaaddr: wdc LBA-mode address decode -- SDH decodes the LBA flag from bit 6 (was bit 5) and
  the 64-bit LBA28 arm is enabled at both read and write sites.  33 rows on unmodified evbmips -e malta; wired in
  gate_sh_rounding.sh (gate 10) in the same commit, pinned at 33; kill tables ..."*.  Frozen witness copies land as
  `*.frozen.py` with `CLASS_WITNESS`; until then they are kept as `.py.txt`.

---

## 6. PREMISES STATED AS QUESTIONS -- check these; ratification is not wanted

* **P1** CSR1 bit 0 READS BACK as 0 on the chip.  The datasheet says *"Must be zero."* and draws `'0'`; it writes "Read
  as zeroes" only for CSR2 15:8 and CSR3 15:3.  Is masking bit 0 at the store right, or does the chip latch the bit as
  written (so CSR1's mask is 0xffff, and `csr1 all` / `csr1 odd` have the wrong FIX wants)?  rpajarola masks it; is
  that a datasheet reading or a choice?
* **P2** The Am79C90 register semantics bind the Am7990 model (D2).  If a seat knows the Am7990 datasheet proper (not on
  disk -- `am7990_ds.txt` is an unreadable scan), say what it says for CSR2 15:8 and CSR3 15:3.
* **P3** CSR2 bits 15:8 read as zero -> mask 0x00ff.
* **P4** CSR3 bits 15:3 read as zero -> mask 0x0007.
* **P5** The read-back is the fix's only guest-visible consequence (S6): no model code reads `reg[3]`; `reg[2]` is
  already masked by its consumer; `reg[1]`'s bit 0 feeds only the parity warning.  Is there a reader I missed (grep
  `reg\[` and `reg_select`)?
* **P6** `default:` after `case 1:`/`case 2:` is exactly CSR3 (S1).  Is there any path by which `le_register_write`
  sees `r` outside 0..3?
* **P7** STOP gating (D4) stays OUT of this round and is filed; the detector does NOT pin a STOP-clear write.  Should it?
  (A row writing CSR0.STRT first, then CSR3 0xffff, would pin the model's un-gated acceptance -- a behaviour the datasheet
  calls out of spec -- and would go red if a later round implemented the gating.  My reading: disclose, do not row.)
* **P8** A 32-bit `sw` to RDP (len 4) carries `idata` bits 31:16, which the `uint16_t` store already drops; the
  width axis lives in the caller and is outside the DEPENDS-ON closure (R3).  Agree?
* **P9** Deleting the unreachable parity warning (3.2 (i)) is in this round's scope rather than a separate records
  round; and (iii) -- relocating it to the store as a latched announce -- is an addition without a warrant (R10).
* **P10** Severity MED / WRONG-RESULT stands (D3).  Does any firmware or self-test a DECstation runs read back CSR1-3
  after writing unimplemented bits (the KN01 PROM's `t 0/le`?), which would raise the reach?
* **P11** The rows' HEAD and FIX wants (7.4) are right, including `csr1 all` = 0xfffe and `csr1 odd` = 0x1234.
* **P12** The dead-run prediction: `le_csrmask_probe.py /bin/false GATE` -> every session's spawn produces no debugger,
  `unassemble` returns nothing (encodings 0/n), no breakpoint hit, every capture register `None` -> **0/18**,
  `LE_CSRMASK_CONTROL=FAIL`, exit 1.

---

## 7. The partition, cells, rows and variants -- as DATA: check them, do not ratify them

**7.1 Partition of inputs.**  (register `r`, bit `b`, STOP state, access width).  The repair changes what the model
STORES (and therefore reads back) for exactly: `r = 1, b = 0`; `r = 2, b in 8..15`; `r = 3, b in 3..15`.  It leaves
alone: `r = 0` (any bit; a different arm); `r = 1, b in 1..15`; `r = 2, b in 0..7`; `r = 3, b in 0..2`.  STOP state and
width do not enter the edited arm's own tests (S12, P8).

**7.2 The floor** (R1-R4):
* **(a)** the probe in GATE mode (FIX column) on the pre-fix build: predicted **14/18**, the four symptom rows red
  (leg L0, 7.7).
* **(b)** verbatim reinstatement of `d->reg[r] = x;` at the one fixed site = the pre-fix build: 14/18 (V1).
* **(c)** null medium, a runtime probe: an absent / non-emulator binary -- `(c): measured at <killtable artifact>`,
  planned as leg L3 with `/bin/false`; predicted 0/18, CONTROL=FAIL (P12).
* **(d)** DEPENDS-ON: the predicate dominating the edited lines inside `le_register_write` is `switch (r)` with the
  labels {1, 2, 3}; the body masks `x` and tests nothing on it, so each label's generating set is {its kept bits, its
  dropped bits}, with the boundary bits -- CSR1 bits 0/1, CSR2 bits 7/8, CSR3 bits 2/3 -- the D2 edges (R5).
  **Cells C1-C6:** C1 CSR1 dropped (bit 0) · C2 CSR1 kept (bits 1 and 15 rowed) · C3 CSR2 dropped (15:8) ·
  C4 CSR2 kept (7:0) · C5 CSR3 dropped (15:3) · C6 CSR3 kept (2:0).  All six are rowed (7.4).
  **Not cells (clause (e), R6):** the STOP state (S12, P7); the access width (P8); the CSR0 arm; big-endian hosts
  (3.3); the INIT path (no INIT is issued).

**7.3 Sibling parity.**  One arm serves three labels, so the siblings are the LABELS.  Each has an ALL row (write 0xffff;
reads back exactly the mask, so ANY single change M -> M' to that register's mask reds it: 0xffff & M' = M' != M) and
a KEPT row with the kept boundary bit set (CSR1 0x1236 bit 1; CSR2 0x00a5 bit 7; CSR3 0x0005 bit 2).  CSR1 additionally
carries `odd` (the research row's named symptom; the dropped boundary bit alone) and `top` (bit 15).  The asymmetry --
no `0x0100`-only row for CSR2, no `0x0008`-only row for CSR3 -- is covered by the ALL rows under the claim just stated;
**check that claim rather than the count.**

**7.4 Rows N1-N18** (the shipping revision; one fresh emulator per session; wants are literals; `channel` names the
observable that differs and the variant it reds on):

| # | row | session | stimulus | HEAD | FIX | kind | channel (reds on) |
|---|---|---|---|---|---|---|---|
| N1-N4 | `ram:<s>` | each | `sh`/`lhu` 0x5a5a via KSEG0 RAM | 0x5a5a | 0x5a5a | control | liveness; a dead run (V20) |
| N5 | `csr0 reset` | csr0 | RAP=0, read RDP | 0x0004 | 0x0004 | control | device signature; V20; a window translation (R7) |
| N6 | `rap mask` | csr0 | RAP:=0x13, read RAP | 0x0003 | 0x0003 | control | signature; V20 |
| N7 | `csr3 all` | csr3 | RAP=3, write 0xffff, read | 0xffff | **0x0007** | symptom | read-back; V1 V7 V8 V9 V11 V18 V19 |
| N8 | `csr3 bits` | csr3 | write 0x0005, read | 0x0005 | 0x0005 | control | read-back; V8 V9 V10 V19 |
| N9 | `csr2 all` | csr2 | RAP=2, write 0xffff, read | 0xffff | **0x00ff** | symptom | read-back; V1 V5 V6 V11 V18 V19 |
| N10 | `csr2 lo` | csr2 | write 0x00a5, read | 0x00a5 | 0x00a5 | control | read-back; V6 V10 V11 V19 |
| N11 | `csr1 all` | csr1 | RAP=1, write 0xffff, read | 0xffff | **0xfffe** | symptom | read-back; V1 V2 V3 V4 V19 |
| N12 | `csr1 odd` | csr1 | write 0x1235, read | 0x1235 | **0x1234** | symptom | read-back; V1 V2 V10 |
| N13 | `csr1 even` | csr1 | write 0x1236, read | 0x1236 | 0x1236 | control | read-back; V3 V10 V19 |
| N14 | `csr1 top` | csr1 | write 0x8000, read | 0x8000 | 0x8000 | control | read-back; V4 V10 V19 |
| N15-N18 | `stable:<s>` | each | the first RDP value read again | = first | = first | control | a device answering differently on two reads; V20 |

Each `csrN` session: RAP := N; write the ALL value; read RDP twice (`all`, `stable`); then each accept value, read once.
CONTROL = every control row + every session's word-encoding check + every halt-breakpoint hit.

**7.5 Variants V1-V20 -- my predictions; classify each as DETECTED (name the red rows), EQUIVALENT (no observable
differs), or OUT OF CONTRACT (differs, but by an axis 7.6 discloses):**

| # | variant (applied to the M1 fix) | predicted red rows | class |
|---|---|---|---|
| V1 | revert: `d->reg[r] = x;` for all three (= HEAD) | N7 N9 N11 N12 | floor (a)/(b) |
| V2 | CSR1 mask 0xffff (CSR1 unmasked) | N11 (0xffff) N12 (0x1235) | (d) widened |
| V3 | CSR1 mask 0xfffc | N11 (0xfffc) N13 (0x1234) | (d) narrowed at the kept edge |
| V4 | CSR1 mask 0x7ffe | N11 (0x7ffe) N14 (0x0000) | (d) narrowed at bit 15 |
| V5 | CSR2 mask 0x01ff | N9 (0x01ff) | (d) widened at the dropped edge |
| V6 | CSR2 mask 0x007f | N9 (0x007f) N10 (0x0025) | (d) narrowed at the kept edge |
| V7 | CSR3 mask 0x000f | N7 (0x000f) | (d) widened |
| V8 | CSR3 mask 0x0003 | N7 (0x0003) N8 (0x0001) | (d) narrowed at the kept edge |
| V9 | CSR3 mask 0x0006 | N7 (0x0006) N8 (0x0004) | (d) narrowed at bit 0 |
| V10 | store the mask constant, ignoring `x` (`d->reg[r] = M`) | N8 (0x0007) N10 (0x00ff) N12 (0xfffe) N13 (0xfffe) N14 (0xfffe); the ALL rows PASS | repair nulled on the kept side |
| V11 | CSR2 and CSR3 masks swapped | N7 (0x00ff) N9 (0x0007) N10 (0x0005); N8 passes (0x0005 & 0xff) | label swap |
| V12 | mask at the READ instead of the store (M2 form) | none -- identical read-back | EQUIVALENT for this probe; differs only in the INIT consumer's parity warning (3.2) -- disclosed |
| V13 | mask only when STOP is set (`if (d->reg[0] & LE_STOP) ... & M else x`) | none (STOP set throughout, S12) | OUT OF CONTRACT -- STOP axis disclosed (P7) |
| V14 | mask only for 16-bit writes (a `len` test in the caller) | none (all writes are `sh`, S13) | OUT OF CONTRACT -- width axis disclosed (P8) |
| V15 | CSR1 mask written `x & ~1` | none | EQUIVALENT (same value) |
| V16 | form (B) table with index 0 = 0xfffe (CSR0 also masked) | none (the CSR0 arm never reaches the table; `csr0 reset` reads the reset value) | EQUIVALENT for this probe -- noted against form (B) |
| V17 | the parity-warning deletion reverted (check kept, unreachable) | none | EQUIVALENT (records only) |
| V18 | one mask for all three (`x & 0xfffe` everywhere) | N7 (0xfffe) N9 (0xfffe) | label collapse |
| V19 | masks shifted one label (CSR1 gets 0x00ff, CSR2 0x0007, CSR3 0xfffe) | N7 (0xfffe) N9 (0x0007) N10 (0x0005) N11 (0x00ff) N13 (0x0036) N14 (0x0000) | label shift |
| V20 | null medium: `/bin/false` as the binary | all 18 (`None`), CONTROL=FAIL | floor (c) |

**7.6 The contract** (probe header, R6): CATCHES -- any single change to any one register's mask (the ALL rows); a
store that ignores the written value; masks swapped, shifted or collapsed across the three labels; the revert.
EQUIVALENT / OUTSIDE -- masking at the read instead of the store (same read-back); a mask conditioned on STOP (every row
runs with STOP set); a mask conditioned on access width (every write is 16-bit); edits to the CSR0 arm; the INIT path and
`init_block_addr` (no INIT is issued); the big-endian host path.  **Anchor (R7):** `csr0 reset` and `rap mask` pin the
two ports by their reset value and their masking -- a translation of the window by one halfword makes the RDP rows read
RAP's value or RAM, so position is pinned by the signatures rather than by the symptom rows.

**7.7 The variant table -- legs, in order.**  L0 base GATE on the HEAD clone (FIX column): 14/18 expected -- floor (a).
L1 fix GATE on the fix clone: 18/18.  L2 two-leg `probe <base> <fix>`: base vs HEAD column 18/18 AND fix vs FIX column
18/18 -- the witness shape, and the warrant for the `probe:` term (R13).  L3 null medium (V20).  Then V2-V11, V18, V19
on the fix clone.  V12-V17 are classified, not built, unless a seat disputes the class.  All runs in `cp -a` clones under
`/tmp` -- never `build/` (R20) -- with a clone-local sentinel and a `cmp`-against-SEC restore per variant;
`PRETABLE.out` written BEFORE L0 (R19); logs copied to `regress/artifacts/lecsrmask/killtable_20261025/` before any
record cites them.

**7.8 Home, wiring and the pins** (Q3): `regress/gate_arm.sh`, a block modelled on the `sgi_re_unmapped` one (S15) --
`python3 le_csrmask_probe.py "$PMAX" GATE > "$LELOG"`, sentinel `LECSRMASK_PROBE_DONE` first, control
`^LE_CSRMASK_CONTROL=OK$` = 1, a per-row `check` for each of the 18 names, and the denominators by EQUALITY (emitted 18,
green 18, red 0); a `CLASS_DETECTOR` MANIFEST line and a `CLASS_WITNESS` line for the frozen witness copy (renamed
`le_csrmask_probe.frozen.py`) in `check_probe_wiring.py` (S16); `derive_hygiene_pins.sh --grandfather
le_csrmask_probe.py` then `--write` in the SAME commit as the wiring (S14; gate 6's own history says a probe shipping
with its wiring forces the gate run).

**7.9 The witness term**: `probe:regress/le_csrmask_probe.py -- rung 3, unmodified pmax -e 3100,
regress/artifacts/lecsrmask/witness_20261025/`, claimed once L2 is green with the same script; `detector:` otherwise.

---

## 8. SOURCE, INLINED -- line numbers as read at HEAD `0b09e7b6` (identical in the working tree)

**8.1 `src/devices/dev_le.c` -- the constants, the struct's register fields, and the INIT consumer's head**

```c
  79: #define	N_REGISTERS		4
  80: #define	SRAM_SIZE		(128*1024)
  81: #define	ROM_SIZE		32
  ...
  84: struct le_data {
  85: 	struct nic_data	nic;
  86: 
  87: 	int		subsys;		/*  for debugmsg  */
  88: 
  89: 	struct interrupt irq;
  90: 	int		irq_asserted;
  91: 
  92: 	uint64_t	buf_start;
  93: 	uint64_t	buf_end;
  94: 	int		len;
  95: 
  96: 	uint8_t		rom[ROM_SIZE];
  97: 
  98: 	int		reg_select;
  99: 	uint16_t	reg[N_REGISTERS];
 100: 
 101: 	int		is_bigendian;
 ...
 174: static void le_chip_init(struct le_data *d)
 175: {
 176: 	uint16_t tmp;
 177: 	uint8_t macaddr[6];
 178: 
 179: 	d->init_block_addr = (d->reg[1] & 0xffff) + ((d->reg[2] & 0xff) << 16);
 180: 	if (d->init_block_addr & 1)
 181: 		debugmsg(d->subsys, "initialization block", VERBOSITY_WARNING,
 182: 		    "WARNING! address not word aligned?");
 183: 
 184: 	debugmsg(d->subsys, "initialization block", VERBOSITY_DEBUG,
 185: 	    "init_block_addr = 0x%06x", d->init_block_addr);
 186: 
 187: 	d->mode = le_read_16bit(d, d->init_block_addr + 0);
```

(`le_chip_init` goes on to read the whole initialisation block from the SRAM at that address; it is called from
`le_register_fix()` when CSR0.INIT is set, which the probe never sets.)

**8.2 `le_register_write()` -- the WHOLE function (the edit lands in its `default:` arm)**

```c
 834: /*
 835:  *  le_register_write():
 836:  *
 837:  *  This function is called when the value 'x' is written to register 'r'.
 838:  */
 839: void le_register_write(struct le_data *d, int r, uint32_t x)
 840: {
 841: 	switch (r) {
 842: 	case 0:	/*  CSR0:  */
 843: 		/*  Some bits are write-one-to-clear:  */
 844: 		if (x & LE_BABL)
 845: 			d->reg[r] &= ~LE_BABL;
 846: 		if (x & LE_CERR)
 847: 			d->reg[r] &= ~LE_CERR;
 848: 		if (x & LE_MISS)
 849: 			d->reg[r] &= ~LE_MISS;
 850: 		if (x & LE_MERR)
 851: 			d->reg[r] &= ~LE_MERR;
 852: 		if (x & LE_RINT)
 853: 			d->reg[r] &= ~LE_RINT;
 854: 		if (x & LE_TINT)
 855: 			d->reg[r] &= ~LE_TINT;
 856: 		if (x & LE_IDON)
 857: 			d->reg[r] &= ~LE_IDON;
 858: 
 859: 		/*  Some bits are write-only settable, not clearable:  */
 860: 		if (x & LE_TDMD)
 861: 			d->reg[r] |= LE_TDMD;
 862: 		if (x & LE_STRT) {
 863: 			d->reg[r] |= LE_STRT;
 864: 			d->reg[r] &= ~LE_STOP;
 865: 		}
 866: 		if (x & LE_INIT) {
 867: 			if (!(d->reg[r] & LE_STOP))
 868: 				debugmsg(d->subsys, "register write", VERBOSITY_WARNING,
 869: 				    "attempt to INIT before STOPped!");
 870: 			d->reg[r] |= LE_INIT;
 871: 			d->reg[r] &= ~LE_STOP;
 872: 		}
 873: 		if (x & LE_STOP) {
 874: 			d->reg[r] |= LE_STOP;
 875: 			/*  STOP takes precedence over STRT and INIT:  */
 876: 			d->reg[r] &= ~(LE_STRT | LE_INIT);
 877: 		}
 878: 
 879: 		/*  Some bits get through, both settable and clearable:  */
 880: 		d->reg[r] &= ~LE_INEA;
 881: 		d->reg[r] |= (x & LE_INEA);
 882: 		break;
 883: 
 884: 	default:
 885: 		/*  CSR1, CSR2, and CSR3:  */
 886: 		d->reg[r] = x;
 887: 	}
 888: }
```

**8.3 `DEVICE_ACCESS(le)` -- the WHOLE handler (the RDP/RAP ports; the M2 alternative would edit its `case 0:` read)**

```c
 936: DEVICE_ACCESS(le)
 937: {
 938: 	struct le_data *d = (struct le_data *) extra;
 939: 	uint64_t idata = 0, odata = 0;
 940: 	int retval = 1;
 941: 	size_t i;
 942: 
 943: 	if (writeflag == MEM_WRITE)
 944: 		idata = memory_readmax64(cpu, data, len);
 945: 
 946: #ifdef LE_DEBUG
 947: 	if (writeflag == MEM_WRITE) {
 948: 		fatal("[ le: write to addr 0x%06x: ", (int)relative_addr);
 949: 		for (i=0; i<len; i++)
 950: 			fatal("%02x ", data[i]);
 951: 		fatal("]\n");
 952: 	}
 953: #endif
 954: 
 955: 	/*  Read from station's ROM (ethernet address):  */
 956: 	if (relative_addr >= 0xc0000 && relative_addr <= 0xfffff) {
 957: 		uint32_t a;
 958: 		int j = (relative_addr & 0xff) / 4;
 959: 		a = d->rom[j & (ROM_SIZE-1)];
 960: 
 961: 		if (writeflag == MEM_READ) {
 962: 			odata = (a << 24) + (a << 16) + (a << 8) + a;
 963: 		} else {
 964: 			fatal("[ le: WRITE to ethernet addr (%08lx):",
 965: 			    (long)relative_addr);
 966: 			for (i=0; i<len; i++)
 967: 				fatal(" %02x", data[i]);
 968: 			fatal(" ]\n");
 969: 		}
 970: 
 971: 		retval = 13;	/*  13 cycles  */
 972: 		goto do_return;
 973: 	}
 974: 
 975: 
 976: 	switch (relative_addr) {
 977: 
 978: 	/*  Register read/write:  */
 979: 	case 0:
 980: 		if (writeflag==MEM_READ) {
 981: 			odata = d->reg[d->reg_select];
 982: 			debugmsg(d->subsys, "register", VERBOSITY_DEBUG,
 983: 			    "READ from register 0x%02x: 0x"
 984: 			    "%02x", d->reg_select, (int)odata);
 985: 
 986: 			/*
 987: 			 *  A read from csr1..3 should return "undefined"
 988: 			 *  result if the stop bit is set.  However, Ultrix
 989: 			 *  seems to do just that, so let's _not_ print
 990: 			 *  a warning here.
 991: 			 */
 992: 		} else {
 993: 			debugmsg(d->subsys, "register", VERBOSITY_DEBUG,
 994: 			    "WRITE to register 0x%02x: 0x%02x",
 995: 			    d->reg_select, (int)idata);
 996: 			/*
 997: 			 *  A write to from csr1..3 when the stop bit is
 998: 			 *  set should be ignored. However, Ultrix writes
 999: 			 *  even if the stop bit is set, so let's _not_
1000: 			 *  print a warning about it.
1001: 			 */
1002: 			le_register_write(d, d->reg_select, idata);
1003: 		}
1004: 		break;
1005: 
1006: 	/*  Register select:  */
1007: 	case 4:
1008: 		if (writeflag==MEM_READ) {
1009: 			odata = d->reg_select;
1010: 			debugmsg(d->subsys, "register select", VERBOSITY_DEBUG,
1011: 			    "READ: 0x%02x", (int)odata);
1012: 		} else {
1013: 			debugmsg(d->subsys, "register select", VERBOSITY_DEBUG,
1014: 			     "WRITE: 0x%02x", (int)idata);
1015: 			d->reg_select = idata & (N_REGISTERS - 1);
1016: 
1017: 			if (idata >= N_REGISTERS)
1018: 				debugmsg(d->subsys, "register select", VERBOSITY_WARNING,
1019: 				    "WARNING! register %i (max is %i)",
1020: 				    idata, N_REGISTERS - 1);
1021: 		}
1022: 		break;
1023: 
1024: 	default:
1025: 		if (writeflag==MEM_READ) {
1026: 			debugmsg(d->subsys, "access", VERBOSITY_WARNING,
1027: 			    "read from UNIMPLEMENTED addr 0x%06x",
1028: 			    (int)relative_addr);
1029: 		} else {
1030: 			debugmsg(d->subsys, "access", VERBOSITY_WARNING,
1031: 			    "write to UNIMPLEMENTED addr 0x%06x: "
1032: 			    "0x%08x", (int)relative_addr, (int)idata);
1033: 		}
1034: 	}
1035: 
1036: do_return:
1037: 	if (writeflag == MEM_READ) {
1038: 		memory_writemax64(cpu, data, len, odata);
1039: 		debugmsg(d->subsys, "access", VERBOSITY_DEBUG,
1040: 		    "read from addr 0x%06x: 0x%08x", relative_addr, odata);
1041: 	}
1042: 
1043: 	dev_le_tick(cpu, extra);
1044: 
1045: 	return retval;
1046: }
```

(Note the two comments at 986-991 and 996-1001: the first has "if the stop bit is set" where the datasheet's condition
is the opposite -- CSR1-3 are accessible only WHILE STOP IS SET -- a comment defect in the same arm, records-only.)

**8.4 `dev_le_init()` -- the registration (VERBATIM, the load-bearing part)**

```c
1052: void dev_le_init(struct machine *machine, struct memory *mem, uint64_t baseaddr,
1053: 	uint64_t buf_start, uint64_t buf_end, const char *irq_path, int len)
1054: {
 ...
1059: 	CHECK_ALLOCATION(d = (struct le_data *) malloc(sizeof(struct le_data)));
1060: 	memset(d, 0, sizeof(struct le_data));
 ...
1064: 	d->is_bigendian = machine->cpus[0]->byte_order == EMUL_BIG_ENDIAN;
 ...
1076: 	/*  Initial register contents:  */
1077: 	d->reg[0] = LE_STOP;
 ...
1099: 	memory_device_register(mem, "le_sram", baseaddr,
1100: 	    SRAM_SIZE, dev_le_sram_access, (void *)d,
1101: 	    DM_DYNTRANS_OK | DM_DYNTRANS_WRITE_OK
1102: 	    | DM_READS_HAVE_NO_SIDE_EFFECTS, d->sram);
 ...
1108: 	memory_device_register(mem, name2, baseaddr + 0x100000,
1109: 	    len - 0x100000, dev_le_access, (void *)d, DM_DEFAULT, NULL);
1110: 
1111: 	machine_add_tickfunction(machine, dev_le_tick, d, LE_TICK_SHIFT);
```

**8.5 The callers and the constants**

```c
machine_pmax.c  129: 		dev_le_init(machine, mem, KN01_SYS_LANCE,
                130: 		    KN01_SYS_LANCE_B_START, KN01_SYS_LANCE_B_END,
                131: 		    tmpstr, 4*1048576);
machine_pmax.c  708: 		dev_le_init(machine, mem, KN230_SYS_LANCE,         (KN230 arm)
dev_turbochannel.c 227: 		dev_le_init(machine, mem, baseaddr, 0, 0,     (PMAD-AA option)
dev_luna88k.c  1086: 	dev_le_init(devinit->machine, devinit->machine->memory, LANCE_ADDR - 0x100000, 0, 0, n, DEV_LE_LENGTH);
dec_kn01.h      136: #define KN01_SYS_LANCE		0x18000000	/* LANCE chip */
                137: #define KN01_SYS_LANCE_B_START	0x19000000	/* 64 KB LANCE Buffer */
                138: #define KN01_SYS_LANCE_B_END	0x19010000
if_lereg.h      344: #define	LE_CSR0		0
                345: #define	LE_CSR1		1
                346: #define	LE_CSR2		2
                347: #define	LE_CSR3		3
                363: #define	LE_STOP		0x0004
                367: #define	LE_BSWP		0x4
                368: #define	LE_MODE		0x0
```

---

## 9. Primary sources -- the load-bearing lines (VERBATIM)

**9.1 Am79C90 C-LANCE datasheet** (`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\lance\am79c90_bitsavers.txt`; the
`pdftotext -layout` extraction interleaves two columns -- the CSR1/CSR2 text is the RIGHT column of 1121-1167 and the
CSR3 text the LEFT column of 1194-1230; `am79c90_mit.txt` carries the identical lines at the same numbers).  Raw lines:

```
1121: Bit       Name  Description                              Control and Status Register 1 (CSR1)
1123:                 TRANSMIT DEMAND, when set,               READ/WRITE:    Accessible only when the STOP bit
1124:                 causes the C-LANCE to access the                        of CSR0 is a ONE and RAP = 01.
1125: 03        TDMD  Transmit Descriptor Ring without                        The C-LANCE preserves the con-
1126:                 waiting for the polltime interval to                    tents of CSR1 after STOP.
1128:                 the C-LANCE's response to a Trans-            15                               10
1130:                 mit Descriptor Ring entry insertion by                                                      `0'
1131:                 the host.                                                                      IADR
1132:                                                                                                (15:01)
1136:                 short time after it is written because   Bit      Name  Description
1138: 02        STOP  when TDMD was set. It is also            15:01    IADR  The low order 15 bits of the address
1139:                 cleared by RESET or by setting the       00             of the first word (lowest address) in
1140:                 STOP bit. Writing a "0" in this bit has                 the Initialization Block.
1142:                                                                         Must be zero.
1144:                 STOP disables the C-LANCE from           Control and Status Register 2 (CSR2)
1146:                 RESET. The C-LANCE remains in-           READ/WRITE:    Accessible only when the STOP bit
1147:                 active and STOP remains set until                       of CSR0 is a ONE and RAP = 10.
1148:                 the STRT or INIT bit is set. If STRT,                   The C-LANCE preserves the con-
1149:                 INIT and STOP are all set together,                     tents of CSR2 after STOP.
1151:                 only STOP will be set.                        15        87                     0
1155:                 ONLY and set by RESET. Writing a                                               IADR (23:16)
1156:                 "0" to this bit has no effect. STOP is                                                    RES
1160:                                                          Bit      Name  Description
1161:                 START enables the C-LANCE to             15:08
1162: 00        INIT  send and receive packets, perform        07:00    RES   Reserved. Read as zeroes. Write as
1163:                 direct memory access, and do buffer               IADR  zeroes.
1165:                 set prior to setting the STRT bit. Set-                 The high order 8 bits of the address
1166:                 ting STRT clears the STOP bit.                          of the first word (lowest address) in
1167:                                                                         the initialization Block.
1194: Control and Status Register 3 (CSR3)                   Initialization
1195: CSR3 allows redefinition of the Bus Master interface.
1197: READ/WRITE:  Accessible only when the STOP bit
1198:    15        of CSR0 is ONE and RAP = 11.              Chip initialization includes the reading of the initializa-
1199:              CSR3 is cleared by RESET or by            tion block in memory to obtain the operating parame-
1200:              setting the STOP bit in CSR0.             ters. The following is a definition of the Initialization
1202:                                     3 2 10
1204:                                  BCON                  The Initialization Block is read by the C-LANCE when
1205:                                  ACON                  the INIT bit in CSR0 is set. The INIT bit should be set be-
1206:                                  BSWP                  fore or concurrent with the STRT bit to insure proper pa-
1207:                                  RES                   C-LANCE has read the Initialization Block, IDON is set
1216: Bit    Name  Description                                               RDRA (15:00)   IADR +16
1222: 15:03   RES  Reserved. Read as zeroes. Write as                        LADRF (31:16)  IADR +10
1223: 02     BSWP  zeroes.
1225: 01     ACON
1226: 00     BCON  BYTE SWAP allows the chip to oper-                        PADR (47:32)   IADR +06
```

CONDENSED reading (mine; check it against the raw lines above): **CSR1** -- bits 15:01 `IADR`, "The low order 15 bits
of the address of the first word (lowest address) in the Initialization Block."; bit 00 -- "Must be zero." (drawn `'0'`
in the figure).  **CSR2** -- bits 15:08 `RES`, "Reserved. Read as zeroes. Write as zeroes."; bits 07:00 `IADR`, "The
high order 8 bits of the address ...".  **CSR3** -- bits 15:03 `RES`, "Reserved. Read as zeroes. Write as zeroes.";
02 `BSWP`; 01 `ACON`; 00 `BCON`.  All three: "Accessible only when the STOP bit of CSR0 is a ONE"; CSR1/CSR2 preserved
after STOP; "CSR3 is cleared by RESET or by setting the STOP bit in CSR0."

**9.2 Am7990 LANCE Technical Manual, AMD 1986** (`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\lance\TM1986.txt`; the chip
the DECstation 3100 carries):

```
 441: error status flags and control bits. CSR1 and CSR2 contain the          input to the LANCE), and Soft Reset (by setting the stop bit in
 442: address of the Initialization Block. CSR3 contains control bits         CSRo). Reset causes the LANCE to cease operation and clear
 443: to configure Byte Swap (BSWP), ALE Control (ACON), and                  its internal logic.
 444: Byte Control (BCON). The Initialization Block contains pointers
 446: to the descriptor rings and their length.                               Control Status Registers (CSRo CSR3) contents are affected
 447:                                                                         as follows:
 449: message descriptor entry is four words long. There are sepa-            - CSRo is cieared. (Stop bit gets set.)
 450: rate descriptor rings for transmitting and receiving. Packets to        - CSR3 is cleared.
 451: be transmitted are loaded into buffers by the CPU and the               - CSR1, CSR2 undefined by reset.
 530: 15                                                                               2 1-0
 531:                                                                                  I 00 CSR1
 532:                                                                   IADR
 534: 15                                                              87                      ICSR2
 535:                         RES
 536:                                                                         IADR
 538: 15                                                                         I I I I 3 210
 540:                                                                   RES         BSWP ACON BCON CSR3
 544:                     Figure 1-3 Control and Status Registers in LANCE
 631: Table 1-1 shows how to program CSR3 when interfaced to                  of the LANCE. The user must make sure to process all the
 632: different processors. CSR1 and CSR2 are programmed to con-              transmitted or received packets and rearrange the packets
 633: tain a pointer to the Initialization Block.
```

(The figure's register layout matches the C-LANCE's: CSR1 `IADR` with `00` at bit 0; CSR2 `RES` over `IADR`, split at
bit 8; CSR3 `RES` then `BSWP ACON BCON`.  The manual's extracted prose carries no "read as zeroes" sentence -- P2.)

**9.3 Drivers** -- NetBSD `dev/ic/lance.c` (`_scratchpad\lance\lance_nb.c`):

```
 295: 	(*sc->sc_wrcsr)(sc, LE_CSR3, sc->sc_conf3);
 302: 	(*sc->sc_wrcsr)(sc, LE_CSR1, a);
 303: 	(*sc->sc_wrcsr)(sc, LE_CSR2, a >> 16);
```

Linux `declance.c` (`_scratchpad\lance\linux_declance.c`):

```
 313: 	writereg(&ll->rap, LE_CSR1);
 314: 	writereg(&ll->rdp, (leptr & 0xFFFF));
 315: 	writereg(&ll->rap, LE_CSR2);
 316: 	writereg(&ll->rdp, leptr >> 16);
 317: 	writereg(&ll->rap, LE_CSR3);
 318: 	writereg(&ll->rdp, lp->busmaster_regval);
```

**9.4 A records note about the sources themselves.**  The carrier's primary-source list is derived by
`ls _scratchpad/*.pdf`, which does not descend into `_scratchpad/lance/`; that is how a first draft of this round came
to say "no LANCE datasheet is on disk".  The `_scratchpad/am7990_idle_descriptor_verdict.md` research note (#274/#275)
cites the same Technical Manual by its bitsavers path.  Filing candidate for the carrier (Q4), not this round's code.

---

## 10. The project rules the questions apply -- quoted with their bounds (abridged; the carrier is the authority)

* **R1 The vacuity floor.** A detector is VACUOUS unless it (a) fails on the pre-fix build, (b) fails on a VERBATIM
  REINSTATEMENT of the removed defect at EVERY fixed site, (c) fails on a NULL MEDIUM.  A breach is L2: replace in-round.
* **R2 Clause (c), recorded in one of two forms:** `(c): measured at <artifact>` or `(c): by construction via <row/pin>,
  leg not run`; for a runtime probe the null medium is an absent or non-emulator binary; the pre-fix build is never (c)'s
  medium.
* **R3 Clause (d), DEPENDS-ON, bounded:** the predicates DOMINATING the diff's edited lines, walked up only to the
  ENCLOSING FUNCTION; operand swaps drawn only from fields the guarded BODY reads.  Never into callers or callees.
* **R4 Joint cells / labels:** a block serving several case labels has the LABELS as siblings; the floor is the labels
  crossed with the body-tested partition; a value the body never tests as a case is clause (e).
* **R5 Rule D2 (compares):** a relational compare against a constant B is pinned by rows at B-1 and B+1.  **Question
  for this round (Q2a):** a MASK tests no compare; is its analogue "the two boundary bits, one kept and one dropped,
  each rowed alone", and do the ALL rows discharge the dropped side for every bit at once?
* **R6 Clause (e), the contract:** the probe header names what it catches and what it does not; a later escape is
  then "outside the contract" or "a breach", not an argument.
* **R7 Clause (f), the anchor:** "if every address in this device shifted one word, which row reds?" -- a detector
  pinning WHERE an access lands needs one row anchored by a channel outside the decode (a reset value, a side effect).
* **R8 Sibling parity:** for each arm the diff touches, compare its observable channels against its nearest sibling
  arm; an asymmetry is a row owed or a sentence owed.
* **R9 CHANNEL:** for each row, name the variant it reds on and the observable that differs; a row whose channel cannot
  vary under its named variant is vacuous by construction.
* **R10 The addition licence:** additions to product code are licensed by a MEASURED DELTA or a TRANSFERRED WARRANT --
  never by "it cannot hurt".
* **R11 Option-set completeness:** before choosing a disposition, grep the fork for the existing idiom and for the
  sibling handlers' disposition; name a member before dismissing it.
* **R12 The witness ladder, rung 3:** a real guest instruction through real address decode and real `memory_rw` on an
  UNMODIFIED in-tree machine; INVALID without (i) the symptom on the pre-fix committed HEAD and green post-fix with the
  same script, (ii) a LIVENESS control and a DEVICE-SIGNATURE control, (iii) no machine or device added to reach the site.
* **R13 The `probe:` term** is claimed only when the same script shows the symptom pre-fix and green post-fix; the
  record must show ORDER (witness before the edit).  `detector:<path>` is the term for a fix shipped with a measured
  detector and no guest-path witness, and never satisfies the reproduce-first step.
* **R14 L1-L4 and the stopping rule:** a finding is fixed in-round only as L1 pre-ship construction, L2 floor breach, L3
  undischarged obligation, L4 wrong record; everything else is FILED.
* **R15 The ask-again:** once the table is clean, ask the panel ONCE more for another variant; capped at one ask per
  detector per round; the cap counts asks, not findings.
* **R16 The repair chain:** a repair made in response to a pass 2 owes its own pass 2; the chain closes on the first
  VALID pass finding zero floor breaches, with its denominator stated.
* **R17 Citation form:** same-file references by construct name or position; cross-file by verified-unique grep anchor
  or a line number WITH the commit it was read at.
* **R18 §C5 (the codex seat):** ordinary engineering language; reading scoped to `src/` and `regress/*.py`; never ask
  for "the smallest edit that re-opens this" -- supply the candidates and ask which are equivalent (7.5 does).
* **R19 PRETABLE.out**, written BEFORE table 1 (sibling parity, claim->row, guard-field/body-field with the partition
  each lvalue induces, channel per row).
* **R20 Variant tables run in `cp -a` clones**, never in `build/`; clone-local sentinel; restore verified by `cmp`
  against GXEMUL-SEC and a rebuilt binary; `/tmp` evaporates, so artifacts are copied into `regress/artifacts/` before
  any record cites them.
* **R21 The hygiene-pin coupling** (gate 6's own comment, 547-550): *"a probe that ships in the same commit as its gate
  wiring cannot skip this pin, because the wiring forces a gate run."*  Three recorded instances of a probe landing with
  the pin unmoved; `#572` is a fourth (S14).

---

**THIS FIRING ANSWERS Q1 AND Q2 ONLY.**  Q3 and Q4 go to a separate firing of this same packet; do not answer them here.  Keep hidden reasoning short and put the VERDICT line and the answers in the response itself.

## 11. QUESTIONS -- VERDICT LINE FIRST (format in section 0)

**Q1 -- the repair: right masks, right form, right member?**

(a) **Premises.**  Which of S1-S16 is false?  Answer P1-P6 and P9-P10.  In particular P1: does the Am7990/Am79C90 read
CSR1's bit 0 back as zero, or preserve it?  If you can settle P2 from a source this brief does not have, name it.

(b) **The partition** (7.1), as INPUTS -- no edit text is wanted: for which (register, bit) does the repair change what
the model stores, and is anything outside the one arm affected (S6: readers of `reg[1..3]`)?  Enumerate the readers;
do not reason about them.

(c) **The consumer** (3.2): with CSR1 bit 0 dropped at the store, `le_chip_init`'s odd-address warning is unreachable.
Delete it in this change (i), keep it (ii), or relocate it as a latched announce (iii)?  Which is consistent with R10 and
R14, and what must the change's comment say?

(d) **Form and member** (3.1, 3.5): explicit `case 1:`/`case 2:`/`default:` or the table (B)?  M1 (store) or M2
(read-back)?  Grep the fork for the idiom a device uses when a register has reserved bits that read as zero, and name
the file.  Is a member unnamed?

(e) **What must NOT change:** the CSR0 arm (842-882), the RAP masking (1015), the read path (979-991) under M1, the
SRAM window, the three other machines' behaviour except the read-back (3.3).  Complete?  Is this ONE round -- or does
D4 (STOP gating, CSR3-cleared-on-STOP) belong in it under the reopening rule?

(f) **What else the repair carries:** `/* #573: */` tags; the same bytes in `est/` (shared file, not a declared
divergence) and in the build trees with a rebuilt binary; the comment defect at 986-991 (8.3 note) -- fix in the same
change as a records correction, or file?

**Q2 -- the detector: complete, bounded, valid?**

(a) **The floor and the cells** (R1-R5; 7.2).  Grade C1-C6 as FLOOR, clause-(e) debt or NOT A CELL, citing the rule.
Answer R5's question: what is rule D2's analogue for a MASK, and do the ALL rows (N7, N9, N11) discharge the dropped
side for EVERY bit of each mask at once (7.3's claim)?  Is a cell missing -- in particular, is the STOP state (P7) or
the access width (P8) inside the DEPENDS-ON closure (R3) or outside it?

(b) **Classify V1-V20** (7.5): is each predicted red-row set right, and the class?  Which are EQUIVALENT in every
state, and which only on this probe's inputs?  Is a variant missing from the closure -- one that keeps all three masks
and still returns a wrong read-back on some input the probe drives?

(c) **The rows N1-N18** (7.4) as DATA: correct any want (P11).  Can each row's channel vary under its named variant
(R9)?  Is `csr1 top` (N14) earning its place, or is it subsumed by N11?  Should the per-session `stable` rows count
toward the score or fold into CONTROL?

(d) **Clause (c) and the dead run** (R2, P12): is `/bin/false` the right null medium for a runtime probe, is the
predicted 0/18 / CONTROL=FAIL / exit 1 right, and is the record form `(c): measured at <artifact>`?

(e) **The contract and the anchor** (R6, R7; 7.6): correct the CATCHES / OUTSIDE text; "if the register window moved by
one halfword, which row reds?"

**Q3 -- shape, home, witness term, records, filings**

(a) **Witness term** (R12, R13; 7.9): `probe:` once L2 is green with the same script -- what must the record show about
ORDER (2.4)?  Does the git-archive clone build satisfy "the committed build"?

(b) **Home and wiring** (S15, S16; 7.8): `gate_arm.sh` beside the `sgi_re_*` blocks (the precedent's own reason is
quoted in S15), or `gate_mips.sh` (the pmax gate, which boots a rig image this probe does not need)?  Name the gate
checks: sentinel first, control = 1, 18 per-row checks, denominators by equality (18 / 18 / 0).

(c) **The hygiene pins** (S14, R21): this round's commit runs `derive_hygiene_pins.sh --grandfather le_csrmask_probe.py`
and `--write` in the same commit as the wiring.  **And `#572`'s own omission** -- `wdc_lba_probe.py` NEW PROMPTLESS,
pin 77 vs 78, gate 6 red at HEAD, the weekly battery due 2026-10-25 18:00 -- is an L4 wrong record of a CLOSED round:
fix it in its own follow-up commit BEFORE this round lands (the late-dissent rule's "never amend under a closed round's
number" governs code, not a records pin)?  Or fold it into this round's hygiene edit with its provenance stated?

(d) **Records in the SAME change:** the CHANGELOG block must claim: the witness (rung 3, 3100, unmodified); the masks
and their datasheet lines; the unreachable warning's disposition; that the fix changes READ-BACK only (S6); that STOP
gating and CSR3-cleared-on-STOP are NOT implemented (D4).  It must NOT claim that any shipped driver observes the
defect (D3).  Anything else?

(e) **Filings** (R14 "everything else is FILED"): D4's two datasheet behaviours the model lacks (CSR1-3 accessible only
with STOP set; CSR3 cleared on STOP) -- one row or two, and does research row 9 (1.2) already carry the second?  The
comment defect at 986-991.  The carrier's primary-source list missing `_scratchpad/lance/` (9.4).  Others?

**Q4 -- the standing licence**

If, while verifying a claim, you found something ELSE -- say so.  Candidates from drafting, to check rather than
findings:

1. The RAP write arm masks `reg_select` to 0..3 but warns at `idata >= N_REGISTERS` (1017-1020) -- the datasheet's RAP
   has bits 1:0 only; is a write of 0x13 a guest error the warning should keep announcing, and is that warning latched?
2. `le_register_write`'s `x` is `uint32_t` while every caller passes a `uint64_t idata`; harmless today (P8) -- a
   records note or nothing?
3. The two comments at 986-1001 contradict the datasheet's condition in one of them (8.3 note).
4. `init_block_addr`'s `(d->reg[2] & 0xff)` becomes a second mask of an already-masked value after M1 -- leave, or
   simplify in the same change?
5. The witness probe's "14/15 mnemonics" line: the word check is 15/15; is the mnemonic rendering count worth printing,
   or does it invite a reader to see a failure that is not one?
6. `#572`'s hygiene omission (Q3c) -- is there a THIRD recent landing with the same gap (`derive_hygiene_pins.sh`
   names only `wdc_lba_probe.py` today, so probably not; confirm)?

---

## 12. Paths

* Tree: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\` (git root), HEAD `0b09e7b6`; the twin `C:\DocumentNoSnc\cc\GXEMUL\est\`.
* The site: `GXEMUL-SEC/src/devices/dev_le.c` -- `grep -n 'CSR1, CSR2, and CSR3' src/devices/dev_le.c`.
* The witness: `GXEMUL-SEC/regress/artifacts/lecsrmask/witness_20261025/` (`RESULTS_base.txt`, `RESULTS_base.err`,
  `RUN_IDENTITY.txt`, `le_csrmask_probe.frozen.py.txt` md5 `df5ab57408d1db812d66bb0b42564fb0`, `raw/` x8).
* The detector revision under review: `GXEMUL-SEC/regress/artifacts/lecsrmask/pass1_20261025/le_csrmask_probe.frozen.py.txt`
  (md5 in `FROZEN.md5` beside it), its HEAD-column re-measure `pass1_20261025/det18_HEAD/RESULTS_base.txt`.
* This brief: `pass1_20261025/packet.md` (FULL), `packet_packetfed.md` (the packet-fed form), the Q12/Q34 splits.
* Sources outside the repo, absolute: `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\lance\am79c90_bitsavers.txt`,
  `...\am79c90_mit.txt`, `...\TM1986.txt`, `...\lance_nb.c`, `...\linux_declance.c`.
* Research: `GXEMUL-SEC/regress/artifacts/research_20261022/A_github_forks.md` (rows 9, 26), `TRIAGE.md` (T61).
