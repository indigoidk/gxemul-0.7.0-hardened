# PASS-1 DESIGN REVIEW -- round #571, ledger row `ppcdsformxo` (research item T2) -- GXemul hardened fork

**Brief v1, PACKET-FED form (for the seats that cannot read files: GLM 5.3 and DeepSeek).  It stands alone.  The FULL form
(`pass1_20261024/packet.md`) is the AUTHORITY; sections 5, 6, 7 and 11 here are byte-identical to it, and every other
section is cut or condensed and says so.**  Drafted 2026-10-24.
Tree under review: `GXEMUL-SEC/` at HEAD `add098b9` -- a RECORDS-ONLY commit on top of `c8fcb5ff`, the tree the witness
measured; every source file quoted here is byte-identical at HEAD and in the working tree.

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

---

## 0. What this is, what this pass is for, and how to answer

**This is the PACKET-FED form of this brief.**  You cannot read files, and that is expected: every fact a question depends
on is inlined below.  Where you need a fact this packet does not carry, name it NOT CHECKABLE rather than guessing.  The
FULL form is the authority: where this packet condenses a source, a record or a rule, it says so, and the FULL form
carries the text VERBATIM with line numbers.  Sections 5, 6, 7 and 11 are identical to the FULL form, so a reference
there to a section this packet cuts (8.1, 8.3-8.6, 8.10-8.14) is answered by the premise that cites it (S3, S5, S6, S11,
S12, P8).

**The project.**  GXemul is a computer-architecture emulator (it runs legacy operating systems in a software sandbox);
this fork does ordinary software-correctness work on its C code and keeps each correction fixed with regression tests.
*Guest* = the program inside the emulator; *host* = the emulator process; a *variant* = a deliberately altered copy of
the code used to measure whether a test notices (mutation testing).

**The defect, in one paragraph.**  On the 64-bit PowerPC CPU this tree models (PPC970, the default CPU of the in-tree
`testppc` and `bareppc` machines) the decoder treats primary opcode 58 as ONE instruction (`ld`, an 8-byte load) and
primary opcode 62 as ONE instruction (`std`, an 8-byte store), and takes the displacement from the word's whole low
halfword.  In the architecture these are DS-form opcodes: the word's two lowest bits are an extended opcode (XO) that
selects `ld`/`ldu`/`lwa` (58) or `std`/`stdu` (62), and the displacement is the 14-bit DS field with two zero bits
appended.  So today `ldu` loads from EA+1 and does not write EA into RA, and `lwa` loads a whole doubleword from EA+2
instead of a sign-extended word from EA -- both MEASURED (section 2) -- while, as read from the source and NOT measured,
`stdu` stores 8 bytes at EA+1 without writing RA, and the three illegal XO values execute as `ld`/`std` at EA+2 or EA+3.
Guest-visible wrong loads and misdirected stores; no emulator process ends anywhere in this round.

**This pass.**  PASS 1: a design review BEFORE any edit.  The fix design was adjudicated and AGREED by two seats on
2026-10-22 (section 3).  A rung-3 witness reproduced the LOAD half on the committed tree (section 2); **the STORE half is
not in the witness.**  Check the design and the regression rows it owes.  Section 5's premises are settled -- re-open one
only if you find it false, and say so loudly.  Section 6 states the premises I am least sure of AS QUESTIONS.  Section 7
is my own partition of the cells -- check it, do not ratify it.  Nobody is asked to write a guest program or a code
variant: where a question needs a construction, it names what the records already contain and asks you to classify it,
or asks which inputs a repair changes the answer for.

**The working tree** has 20 files differing from HEAD (other sessions' work); none is a PowerPC source file.

**The roster for this pass** (owner roster of 2026-10-23/24), recorded so that a missing answer is read as what it is:

| seat | transport | class | packet |
|---|---|---|---|
| GLM 5.3 (`glm-5.3:cloud`) | Ollama cloud | PACKET-FED | this PACKET-FED form, two firings: Q1+Q2, then Q3+Q4 |
| DeepSeek (`deepseek-v4-pro:cloud`) | Ollama cloud | PACKET-FED | this PACKET-FED form, two firings: Q1+Q2, then Q3+Q4 |
| Grok 4.7 (xhigh, plan mode) | `grok --prompt-file` | FILE-READING | FULL |
| Gemini 4 Argon (`gemini-4-argon-high`) | agy, `--add-dir GXEMUL-SEC` | FILE-READING | COMPACT (one Gemini-family lens) |
| GPT-6 Astra | codex, pointer form | FILE-READING | FULL; reviews on this pass, then ADJUDICATES the consolidated findings |
| Fable 5.1 | -- | HELD | the owner's Fable hold (2026-10-21, "Hold fable reviews until usage reset"); its hold question is filed beside this pass as `fable5.HELD.txt` |
| kimi, minimax | -- | NOT FIRED | not on this roster |
| Opus 5.5 | -- | NOT FIRED as a review seat | it is this round's measuring / builder sub-agent (it built the scratch tree and ran the witness) |

A seat that does not answer is a SEAT FAILURE; a seat deliberately not fired is neither a failure nor agreement.

**Answer format -- VERDICT LINE FIRST:**
~~~~
VERDICT: READY | READY WITH CHANGES | NOT READY -- <one line>
Q1: <one line>   Q2: <one line>   Q3: <one line>   Q4: <one line>
~~~~
Then one section per question.  Mark each claim READ (you opened the source), DERIVED (from this packet) or NOT
CHECKABLE.  Cite premises by number (P1..P15) and cells by number (C1..C26).

---

## 1. The defect -- as the ledger row and the queue describe it (VERBATIM)

**Ledger row `ppcdsformxo`** (`tools/pipeline/ledger.json` at HEAD `add098b9`): state `open`, sev `HIGH`, opened `2026-10-22`, witness `none`, commits `''`.

TITLE (VERBATIM):
~~~~
cpu_ppc_instr.c:X(to_be_translated) D/DS-form arm -- primary opcodes 58/62 keep the DS-form XO bits in the displacement, so `ldu`/`lwa` execute as `ld` at EA+1/EA+2 and `stdu` executes as `std` at EA+1 with no RA update -- GUEST-CORRUPTION (misdirected 8-byte stores; wrong loads; 64-bit CPUs, PPC970 is the testppc/bareppc default)
~~~~

STATE_NOTE (VERBATIM):
~~~~
QUEUE: external-research batch 4 of 10 (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md D).  Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T2 (class GUEST-CORRUPTION; reach U, user mode; effort: small; report rows: A4-13).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/9a05a7b0221023cee81965edb6354367a393b107.  Our site at de8c7547: src/cpus/cpu_ppc_instr.c:4277, :4288, :4295, :4307, :4320 (decode re-read for this triage); src/machines/machine_test.c:448-457.  Portable fix: none -- a design is owed (rs6000 9a05a7b only aborts on it: do not port).  Filing check (TRIAGE.md): 0 hits for DS-form / lwa / stdu / ldu.  Confirmed by both adjudicating seats (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md A): stdu stores at EA+1 and skips the update, ldu/lwa load the wrong data, and no alignment exception exists to intercept it.  Design owed; nothing safe to copy (D4) -- rs6000 9a05a7b only aborts the host (F).  witness: none -- research finding, not yet reproduced here.
~~~~

**`OUTSTANDING_BUGS.md` at HEAD**, the queue head (line 33), VERBATIM (its filing at lines 25264-25268 repeats the title):
~~~~
   33| > 4. `ppcdsformxo` (HIGH, new) -- DS-form XO bits: ldu/lwa/stdu run as ld/std at EA+1/+2.  T2; design owed.
~~~~

**Two things the witness changes about these records, stated so nobody reconciles them:** (1) `witness: none` is stale
-- a rung-3 witness exists (section 2) and is not yet in the ledger; (2) the title's "`stdu` executes as `std` at EA+1 with
no RA update" is a SOURCE READING -- the witness measured the three loads only.  (The state note's ":4277, :4288, :4295,
:4307, :4320" at `de8c7547` are still the right lines at HEAD: the file has not changed since `7e39a49e`.)

---

## 2. The witness -- rung 3, RED on HEAD, LOADS ONLY  (its tables and findings VERBATIM; the raw transcripts are in the FULL form)

**Where:** `regress/artifacts/ppcdsformxo/witness_20261024/`, frozen by `MANIFEST.md5` (6/6 OK at drafting), uncommitted.

**What it did (no program listing).**  A stepped cold-debugger session on the UNMODIFIED `-E bareppc -M 64` (PPC970;
`msr = 0x0`: translation off, SF = 0).  The debugger writes a counting byte pattern at DATA = 0x20000 (byte DATA+k is k),
so a loaded value NAMES its offset; the guest sets each base to 0x20080; every word comes from the probe's encoder.  It
steps one `ld` (XO 0), `ldu` (XO 1), `lwa` (XO 2) and a D-form `lwz` control, then a liveness `li`; then reruns the
commands on a bogus machine TYPE.  **No store instruction is placed in the guest.**

**Result, rows, the offset each load used and RA -- `WITNESS_REPORT.md`, VERBATIM:**
~~~~
7| **Result: `PPC_DSFORM_RESULT=5/8`, `PPC_DSFORM_CONTROL=OK`, `PPC_DSFORM_SYMPTOM=PRESENT 3/3`,
8| `PPC_DSFORM_RED=ldu value,ldu RA after,lwa value`; sentinel `PPC_DSFORM_PROBE_DONE` is the last
9| line of `WITNESS_headbin.out`; probe exit status 1 (`PROBE_RC=1`, by design on any red row).**
  ...
30| ## Rows
31| 
32| | row | got | want | status |
33| |---|---|---|---|
34| | ld value | 0x1011121314151617 | 0x1011121314151617 | ok |
35| | ldu value | 0x2122232425262728 | 0x2021222324252627 | RED |
36| | ldu RA after | 0x20080 | 0x20020 | RED |
37| | lwa value | 0x8a8b8c8d8e8f9091 | 0xffffffff88898a8b | RED |
38| | lwz value | 0x88898a8b | 0x88898a8b | ok |
39| | live | 0x1234 | 0x1234 | ok |
40| | unasm census | 13/13 | 13/13 | ok |
41| | neg apparatus | exit1/-0x1 | exit1/-0x1 | ok |
  ...
43| ## Per instruction: the offset the loaded value names, and RA
44| 
45| Offsets are from DATA = 0x20000; every base was set by the guest to 0x20080.
46| 
47| | instruction | architectural EA | loaded value names | RA after | RA architectural |
48| |---|---|---|---|---|
49| | `ld r4,-112(r20)`, XO 0 | 0x20010 (offset 0x10) | doubleword at offset 0x10 | r20 = 0x20080 | 0x20080 (unchanged) |
50| | `ldu r5,-96(r21)`, XO 1 | 0x20020 (offset 0x20) | doubleword at offset 0x21 | r21 = 0x20080 | 0x20020 (RA <- EA) |
51| | `lwa r6,8(r22)`, XO 2 | 0x20088 (offset 0x88) | DOUBLEWORD at offset 0x8a | r22 = 0x20080 | 0x20080 (unchanged) |
52| | `lwz r7,8(r23)`, D-form | 0x20088 (offset 0x88) | zero-extended word at offset 0x88 | r23 = 0x20080 | 0x20080 (unchanged) |
~~~~

**The reds, the controls and the disassembler observation -- VERBATIM:**
~~~~
59| All three reds are the decode behaviour under test, and the controls that make them attributable
60| are green (`PPC_DSFORM_CONTROL=OK`):
61| 
62| - **ldu value** -- the value names offset 0x21 = the architectural EA + 1, which is RA + the raw
63|   low halfword 0xffa1 (-95): the XO bit is folded into the displacement.  The defect, not the
64|   apparatus: `ld` at XO 0 with a negative DS from the same base value is green, so the DS sign
65|   extension is decoded correctly and the difference is the XO bits.
66| - **ldu RA after** -- r21 still holds 0x20080; EA was not written back.  The committed decode
67|   treats opcode 58 as a non-update doubleword load whatever XO is.
68| - **lwa value** -- a full doubleword from offset 0x8a = the architectural EA + 2 (RA + raw low
69|   halfword 0x000a), not the sign-extended word at offset 0x88.  The `lwz` control reads that same
70|   word correctly (0x88898a8b), so the pattern and the EA are as intended and only lwa's decode
71|   differs: wrong address (XO folded in) and wrong width and extension.
72| 
73| Corroboration from a separate code path: the `step 13` trace in `RAW_headbin_main.txt` is the
74| disassembler's running form, and it prints the same folded addresses and values
75| (`<0x20021: 0x2122232425262728>`, `<0x2008a: 0x8a8b8c8d8e8f9091>`).  The `unassemble` census is
76| 13/13; for the three opcode-58 words the disassembler prints `ld` with displacements -112, -95 and
77| 10, i.e. the XO bits folded into the displacement (an observation about the disassembler: the
78| census confirms each word's opcode, RT, RA and raw low halfword, not architecture).
~~~~

**Not covered (the probe's CONTRACT) -- VERBATIM:**
~~~~
83| ## Not covered (the probe's CONTRACT)
84| 
85| - **The store forms `std` and `stdu` (primary opcode 62) are NOT covered** -- no store
86|   instruction is placed in the guest; stores are a later step.
87| - The illegal XO values (opcode 58 XO 3; opcode 62 XO 2 or 3); the invalid update forms (`ldu`
88|   with RA = 0 or RA = RT); 32-bit CPUs; translation on; 64-bit mode (MSR SF set); EAs with a
89|   non-zero high half; displacements and bases other than those above; page-crossing EAs; the
90|   indexed forms `ldx`, `ldux`, `lwax`, `lwaux`.
~~~~

**The negative-control FINDING** -- a bogus machine SUBTYPE is not rejected by this emulator, so the control makes the
machine TYPE bogus (the bogus-TYPE session exits 1 with "Sorry, emulation "nosuchmachine" is unknown.").  The probe's
docstring, VERBATIM:
~~~~
71|     neg apparatus  the same command stream against a bogus machine TYPE exits 1 with no register
72|                    dump, so every register oracle above can go red (a bogus SUBTYPE is not
73|                    rejected, which is why the TYPE is the one made bogus)
~~~~

**The three opcode-58 `unassemble` observations -- `WITNESS_headbin.out`, VERBATIM:**
~~~~
21| OBS unasm ld  10020: e894ff90 ld r4,-112(r20) | want ld r4,-112(r20) | same  [placed as ld: opcode 58 RT 4 RA 20 DS -28 XO 0; raw low half 0xff90]
22| OBS unasm ldu 10024: e8b5ffa1 ld r5,-95(r21) | want ld r5,-95(r21) | same  [placed as ldu: opcode 58 RT 5 RA 21 DS -24 XO 1; raw low half 0xffa1]
23| OBS unasm lwa 10028: e8d6000a ld r6,10(r22) | want ld r6,10(r22) | same  [placed as lwa: opcode 58 RT 6 RA 22 DS 2 XO 2; raw low half 0x000a]
~~~~

### THE STORE HALF IS NOT IN THE WITNESS -- stated plainly

No `std`, `stdu` or other opcode-62 word was executed.  Their pre-fix behaviour is PREDICTED from the source -- the arm
(section 8.2) keeps the XO bits in `imm = (int16_t)iword;` and its `case PPC_HI6_STD:  size=3; break;` ignores XO -- and is
NOT measured:

* `std` (XO 0): correct -- 8 bytes at EA, RA unchanged;
* `stdu` (XO 1): 8 bytes at **EA+1**, RA **unchanged**;
* opcode 62 with XO 2 / XO 3 (illegal): 8 bytes at **EA+2** / **EA+3**, as if `std`.

**The round's detector must ROW the store forms and measure those rows RED on the BASE binary before the fix lands** --
the T36 precedent: `#570` ran its FINAL 31-row instrument on the pre-fix HEAD binary and preserved the run as
`regress/artifacts/m88kbuserrregs/table1_20261023/prefix_HEAD.out`, whose summary reads (VERBATIM lines, cuts marked `...`):
~~~~
M88K_BUSERR_RESULT=21/31
M88K_BUSERR_CONTROL=OK
M88K_BUSERR_SYMPTOM=PRESENT 10/10
  ...
M88K_BUSERR_LABEL=PREFIX-HEAD-7fca7187
  ...
M88K_BUSERR_PROBE_DONE
~~~~
Q2(a) asks which store rows, with which observable, discharge clause (a) for that half.

**The build** (receipts paraphrased; FULL form): a fresh scratch build whose PowerPC files `cmp` clean against GXEMUL-SEC,
binary md5 `3cd0501cf7c854e0662797ccee1fce64`.

---

## 3. The settled design (VERBATIM) -- and where its sources differ

**3.1 The merged ruling -- `CRIT_RULINGS.md` (2026-10-22; GPT-6 Astra and Grok 4.7 read source at `de8c7547` and the
local manuals, built and ran nothing; "On every design question the two seats agree").  Its T2 row, VERBATIM:**
~~~~
15| | **T2** PPC DS-form decode | `imm = (int16_t)(iword & ~3)` for opcodes 58/62 only; five legal forms (`ld`/`ldu`/`lwa`, `std`/`stdu`) with the table both seats give; reserved XO must not execute as `ld`/`std` (the existing `goto bad`); NO blanket alignment exception (the PEM permits split or trap; `#430/#431` keep the split; the EA+1 defect is the decoder, not alignment); nothing to port (rs6000 `9a05a7b` rejected). `ldu` RA=RT invalidity disclosed, not checked (no program exception exists in this tree). Witness on unmodified `testppc` (PPC970) with IR/DR clear -- independent of N3. | Astra Q3; Grok Q3 | READY -- round 3 |
~~~~

**3.2 GPT-6 Astra's T2 answer -- `codex_rescrit.txt` Q3, VERBATIM:**
~~~~
43| **Q3 — T2: decode DS forms explicitly; preserve supported unaligned RAM behavior**
44| 
45| For DS forms only, separate the low two XO bits and clear them **before sign-extending the displacement**. Ordinary D-form immediates must remain untouched.
46| 
47| | Primary opcode | XO | Form | Transfer | Base update |
48| |---|---:|---|---|---|
49| | `0x3a` | 0 | `ld` | 8 bytes | None |
50| | `0x3a` | 1 | `ldu` | 8 bytes | After successful access |
51| | `0x3a` | 2 | `lwa` | 4 bytes, sign-extended to 64 bits | None |
52| | `0x3e` | 0 | `std` | 8 bytes | None |
53| | `0x3e` | 1 | `stdu` | 8 bytes | After successful access |
54| 
55| Other XO values are reserved. `ldu` forbids RA=0 and RA=RT. `stdu` forbids RA=0, but RA=RS is valid: store the old source value, then update RA. Distinguish invalid forms explicitly rather than executing them as plain `ld`/`std`.
56| 
57| The existing handler machinery supplies the required width, sign and update behavior, including [update after successful memory access](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/cpu_ppc_instr_loadstore.c:174).
58| 
59| **A blanket alignment exception is not part of this repair.** The [local PowerPC manual](C:/DocumentNoSnc/CC/GXEMUL/_scratchpad/ppc_pem_32and64_2005.txt:11974) permits ordinary misaligned integer operations either to trap or to split, depending on implementation. This tree deliberately supports the latter path through #430/#431. Preserve it for ordinary supported RAM. Clearing XO bits does not ensure natural alignment: the base can be unaligned, and DS displacement has only four-byte granularity.
60| 
61| No vetted external repair was established. Reject rs6000 `9a05a7b`’s host abort.
62| 
~~~~

**3.3 Grok 4.7's T2 answer -- `grok_crit.txt` Q3, VERBATIM:**
~~~~
44| ## Q3. T2 — mask the DS XO; five legal forms; no alignment exception; nothing to port
45| 
46| `cpu_ppc_instr.c:4295` takes `imm = (int16_t)iword` and `:4307` / `:4320` treat primary opcodes `0x3a` and `0x3e` as one form each: 8 bytes, no update. Book I (the local `ppc_uisa_book1_v201` text) gives XO in bits 30:31 and the displacement as `EXTS(DS || 0b00)`.
47| 
48| For every legal XO, `imm = (int16_t)(iword & ~3)`.
49| 
50| | opcode | XO | form | width | update |
51| |---|---|---|---|---|
52| | 58 | 0 | `ld` | 8, zero-extend | no |
53| | 58 | 1 | `ldu` | 8 | yes |
54| | 58 | 2 | `lwa` | 4, sign-extend (`size=2`, `zero=0`; the cast is `cpu_ppc_instr_loadstore.c:119-120`) | no |
55| | 62 | 0 | `std` | 8 | no |
56| | 62 | 1 | `stdu` | 8 | yes |
57| 
58| `ldu` with RA=0 already hits `:4338-4341` (`goto bad`) once `update` is set. `ldu` with RA=RT is invalid in Book I and is not checked. This round does not add that check: the only refusal on hand is `goto bad`, a CPU-stop, and this tree's exception list (`cpu_ppc.h:252-257`) has no program exception. Left disclosed. Reserved XO (58/3, 62/2, 62/3) must not fall through as `ld`/`std`. They take the same `goto bad` an unrecognized opcode already takes. One row: opcode 58 with XO=3 does not load 8 bytes and does not update RA.
59| 
60| Unaligned accesses stay as `#431` left them. `cpu_ppc_instr_loadstore.c` performs the access; there is no PPC alignment vector. The EA+1 store is the decoder, and it disappears once the low two bits are masked. A genuinely unaligned EA (RA not a multiple of 8, DS a multiple of 4) is still performed. Do not port rs6000 `9a05a7b`. The same arms fire on 32-bit CPUs, where 58/62 are not the 32-bit ISA. Disclosed, not fixed here. XO=0 `ld`/`std` are already right and are the accept side.
61| 
62| The witness runs with MSR IR and DR clear. On PPC970 a translated access dies in the N3 exit before the store is observable. `testppc` defaults to PPC970 (`machine_test.c:450`). With translation off, `memory_ppc.c:258-261` is the identity map.
63| 
64| Floor: (a) `stdu` with XO=1, DS nonzero, RA≠0, 8-aligned EA, stores at EA+1 and leaves RA unchanged. (b) Restore `(int16_t)iword` and `update=0` for opcode 62. (c) Identity body: decode, retire, memory and RA unchanged. (d) Three nulls of the same guard: displacement masked but `update` left 0 (RA unchanged); `update` set but the raw `int16_t` kept (store at EA+1); `lwa` left at `size=3` (the neighbour word is consumed). Accept: XO=0 `std` still stores the whole doubleword at EA and does not write RA. A growth mutant that adds 1 to XO=0 reds that row. `lwa` oracle: a negative word, sign-extended, the next 4 bytes a sentinel.
65| 
66| Rung-3: cold debugger, unmodified `testppc`, translation off, real decode, real `memory_rw` into RAM. One `stdu`, one `ldu`, one `lwa`, one XO=0 `std`. Liveness is an `stw` of a known word.
~~~~

**3.4-3.5** The filing's adjudication and triage confirm T2 as classed and list rs6000 `9a05a7b` as do-not-port (FULL form, VERBATIM).

**3.6 Where these sources differ -- the drafter's reading, for you to settle (each is also asked in section 11):**

* **D1 -- `ldu` with RA = RT.**  CRIT: "`ldu` RA=RT invalidity disclosed, not checked (no program exception exists in this
  tree)."  Grok: "`ldu` with RA=RT is invalid in Book I and is not checked. ... Left disclosed."  Astra: "`ldu` forbids
  RA=0 and RA=RT. ... Distinguish invalid forms explicitly rather than executing them as plain `ld`/`std`."  Astra's last
  sentence can be read as covering RA = RT, or only the reserved XO values (which are what "executing them as plain
  `ld`/`std`" literally describes).  Which, and does it change the design?  (Q1(d).)
* **D2 -- 32-bit CPUs.**  Grok: "The same arms fire on 32-bit CPUs, where 58/62 are not the 32-bit ISA. Disclosed, not
  fixed here."  Astra and CRIT say nothing.  (Q1(e).)
* **D3 -- the two row lists differ.**  Astra: signed and zero/non-zero displacements, both `lwa` signs and its four-byte
  width, exact store destinations, neighbouring bytes, update / non-update, valid source/base aliasing, invalid/reserved
  forms, suppressed base update on access failure, D-form controls.  Grok: a floor (a)-(d), an XO-0 accept row with a
  growth variant, an `lwa` oracle, one reserved-XO row -- and Grok's clause-(a) row is a STORE row, the half the witness
  does not have.  (Q2.)
* **D4 -- the witness machine.**  CRIT and both seats name `testppc`; the witness ran on `bareppc` (P12).
* **D5 -- the rung-3 shape.**  Grok proposed "One `stdu`, one `ldu`, one `lwa`, one XO=0 `std`.  Liveness is an `stw` of a
  known word"; the witness has no store and uses an `li` for liveness.  (Q2(a).)

---

## 4. Section C0 -- NOT SHIPPED: no CHANGELOG line, commit message or detector names the row at HEAD (FULL form: the output VERBATIM).

---

## 5. SETTLED PREMISES -- re-inlined so nobody spends an answer re-deriving them

Settled by the 2026-10-22 adjudication (section 3), the 2026-10-24 witness (section 2), and lines RE-READ AT HEAD
`add098b9` for this brief (each premise names where; excerpts in section 8).  Re-open one only if you find it false.

* **S1 -- the opcodes.**  `#define	PPC_HI6_LD		0x3a`, `#define	PPC_HI6_STD		0x3e`
  (`src/include/opcodes_ppc.h`): 58 and 62.
* **S2 -- the arm.**  `X(to_be_translated)`'s D/DS-form arm is ONE `case` list of 24 primary opcodes -- LBZ, LBZU, LHZ,
  LHZU, LHA, LHAU, LWZ, LWZU, **LD**, LFD, LFDU, LFS, LFSU, STB, STBU, STH, STHU, STW, STWU, **STD**, STFD, STFDU, STFS,
  STFSU (22 D-form opcodes plus the two DS-form ones).  It computes `imm = (int16_t)iword;` ONCE for all 24 before its
  inner switch, whose `case PPC_HI6_LD:   load=1; size=3; break;` and `case PPC_HI6_STD:  size=3; break;` never look at
  XO (8.2).  It leaves by `break` (to the common tail, which executes the new instruction) or by `goto bad`; no other
  `case` falls into it.
* **S3 -- the architecture** (Book I v2.01, 8.10).  DS-form: OPCD 0:5, RT/RS 6:10, RA 11:15, DS 16:29, XO 30:31 (IBM bit
  numbers); EA = (RA|0) + EXTS(DS || 0b00).  Opcode 58: XO 0 `ld` (8 bytes), XO 1 `ldu` (8 bytes, RA <- EA), XO 2 `lwa`
  (EXTS of 4 bytes).  Opcode 62: XO 0 `std`, XO 1 `stdu` (RA <- EA).  The opcode maps leave 58/XO 3 and 62/XO 2-3 EMPTY,
  and an empty cell is an ILLEGAL instruction, whose execution invokes "the system illegal instruction error handler"
  and "will have no other effect".  Invalid forms: `ldu` with RA = 0 or RA = RT; `stdu` with RA = 0 (RA = RS is valid);
  an invalid form "will either cause the system illegal instruction error handler to be invoked or yield boundedly
  undefined results".
* **S4 -- the witness** (section 2).  On HEAD's `src/` (`c8fcb5ff` == `add098b9`): `ldu` loaded the doubleword at EA+1 and
  left RA unchanged; `lwa` loaded the DOUBLEWORD at EA+2; `ld` (XO 0, negative DS) and the D-form `lwz` read correctly;
  `live`, the 13/13 `unassemble` census and the bogus-TYPE control are green.  Loads only.
* **S5 -- the exceptions this tree delivers on PowerPC.**  `src/include/cpu_ppc.h` defines `PPC_EXCEPTION_DSI` 0x3, `ISI`
  0x4, `EI` 0x5, `FPU` 0x8, `DEC` 0x9, `SC` 0xc and nothing else; every `ppc_exception(` call at HEAD (`git grep`) raises
  DEC, EI, FPU, SC, or a storage interrupt from `src/cpus/memory_ppc.c`.  No Program (0x700) and no Alignment (0x600)
  interrupt is raised anywhere.
* **S6 -- `goto bad`.**  `bad:` in the common tail (`src/cpus/cpu_dyntrans.c`, 8.3) clears the translation; during
  translation read-ahead it returns; otherwise it prints `UNIMPLEMENTED instruction at 0x...` (`VERBOSITY_ERROR`),
  disassembles the word unless single-stepping or tracing, sets `cpu->running = 0` and resets the debugger.  It ends no
  process and delivers nothing to the guest: the CPU stops.
* **S7 -- the table and the flags** (`src/cpus/generate_ppc_loadstore.c`; the generated, committed
  `src/cpus/tmp_ppc_loadstore.c`, 8.8).  The arm picks `ppc_loadstore[size + 4*zero + 8*load + (imm==0? 16 : 0) +
  32*update]` (`ppc32_loadstore` on a 32-bit CPU) unless the case set `ic->f` itself (the FP forms do).  `size` 0..3 = 1,
  2, 4, 8 bytes; `zero` = zero-extend (loads only; the arm leaves it 1 for stores); `imm == 0` selects the `_0` family.
  Slots 11, 27, 43, 59 (an 8-byte SIGN-extending load) are `ppc_instr_invalid`, whose body is
  `fatal("PPC: invalid(): INTERNAL ERROR\n"); exit(1);` (8.6).  The other slots name existing handlers, among them
  `ppc_instr_lwa` (slot 10, a sign-extending word load), `ppc_instr_ldu` (47) and `ppc_instr_stdu` (35 and 39).
* **S8 -- the generic handler** (`LS_GENERIC_N`, `src/cpus/cpu_ppc_instr_loadstore.c`, 8.7).  EA = `reg(ic->arg[1]) +
  (int32_t)ic->arg[2]` (64-bit arithmetic on a 64-bit CPU); a load calls `memory_rw` and THEN writes RT; a store copies RS
  into a buffer and THEN calls `memory_rw`; an update form then writes RA <- EA, only if `memory_rw` succeeded.  On a
  64-bit CPU every table handler first does `if (!cpu->is_32bit) { LS_GENERIC_N(cpu, ic); return; }`.
* **S9 -- one source, two decoders.**  `src/cpus/cpu_ppc_instr.c` "is compiled twice (DYNTRANS_DUALMODE_32)"
  (`src/cpus/cpu_ppc.c`, beside `update_cr0`): once for 64-bit CPUs, once with `MODE32` for 32-bit CPUs (`cpu->is_32bit =
  (cpu->cd.ppc.bits == 32)` chooses).  An edit to the arm changes both.
* **S10 -- two consumers.**  `git grep 'PPC_HI6_LD\b\|PPC_HI6_STD\b' HEAD -- src` lists only the decoder arm, the
  disassembler arm (`src/cpus/cpu_ppc.c`) and the two defines.
* **S11 -- 64-bit-only opcodes.**  PEM 2005 :6253: "The following primary opcodes are defined for 64-bit implementations
  only and are illegal on 32-bit implementations: 2, 30, 58, 62" (8.12).
* **S12 -- the tree's own 32-bit idioms** (8.5).  `rld*` (opcode 30, 64-bit-only) on a 32-bit CPU: `fatal("TODO: rld* in
  32-bit mode?\n")` outside read-ahead, then `goto bad`.  `stdx`/`stdux` (opcode 31, 64-bit-only): implemented, no width
  test.  `ldx`/`ldux`/`lwax`/`lwaux`: no `PPC_31_*` define, so they reach opcode 31's `default:goto bad;` on every CPU.
* **S13 -- nothing to port.**  rs6000 `9a05a7b` only aborts the emulator on these opcodes (both seats; section 3).
* **S14 -- no blanket alignment exception** (all three research texts, section 3).
* **S15 -- gate-home facts** (section 9).  `regress/gate_ppc.sh` (gate 13) runs three register-to-register PowerPC probes on
  `-E bareppc -M 64` BEFORE `need_file "$IMAGES/netbsd401-macppc-GENERIC"`; the only skip points ahead of them are
  `need_exec "$PMAX"` and the `python3` check; `ppc_rldicl_probe.py` is pinned there at 24 rows by name.  `regress/gate_arm.sh`
  (gate 14)'s `#570` block "runs only if none of this gate's eleven earlier skip points fired".
* **S16 -- the promotion precedent.**  `#570` promoted its witness to `regress/m88k_buserr_probe.py` (31 rows, gated, pinned
  by name, `CLASS_DETECTOR`) and kept the witness byte-identical in its artifacts directory as `CLASS_WITNESS`; its kill
  table's frozen instrument, drivers and staged copies are `*.py.txt` / `*.sh.txt`, outside the wiring checker's domain.
* **S17 -- not shipped** (section 4).

---

## 6. PREMISES STATED AS QUESTIONS -- check these; ratification is not wanted

* **P1 -- ENUMERATE the repaired displacement.**  `imm = (int16_t)(iword & ~3)` clears the word's two lowest bits (XO) and
  sign-extends the low halfword.  I claim it equals EXTS(DS || 0b00) for every DS and every XO, because the clear never
  touches the halfword's sign bit.  Walk DS = -8192, -1, 0, +1, +8191 against XO 0..3 (twenty cells); does any differ?
* **P2 -- the two uses of `imm`.**  The arm uses `imm` in the table index (`imm==0? 16 : 0`, the `_0` family) and as
  `ic->arg[2]`.  I read every `_0` handler on a 64-bit CPU as handing the access to the GENERIC handler, which ADDS
  `(int32_t)ic->arg[2]` anyway (`LS_GENERIC_N` is compiled only under `#ifndef LS_IGNOREOFS`, so a `_0` pass reuses the
  generic function its non-`_0` pass defined; 8.7, 8.8).  If so, on PPC970 the `_0` half is unobservable by value, the
  result rests on `ic->arg[2]` alone, and the two uses matter only for DS = 0 words whose XO is non-zero.  Check; what
  does it imply for rows at DS = 0?
* **P3 -- the slots.**  `ld` -> 15 / 31 (`_0`); `ldu` -> 47 / 63; `lwa` -> 10 / 26 (`size` 2, `zero` 0 -- `ppc_instr_lwa`,
  which casts the word through `(int32_t)`); `std` -> 7 / 23 and `stdu` -> 39 / 55 (the arm leaves `zero` 1 for stores;
  slots 3 / 19 / 35 / 51 hold the same handlers).  Check against 8.8; can any flag combination the design plausibly
  produces for these forms land on 11 / 27 / 43 / 59 (`ppc_instr_invalid`)?
* **P4 -- update order** (S8).  `stdu` with RA = RS stores RS's OLD value and then writes RA <- EA (Book I: valid); `ldu`
  with RA = RT writes RT with the doubleword and then RA (= RT) <- EA, so RT ends holding EA.  Check.
* **P5 -- RA = 0 after the repair.**  The arm's existing guard -- `if (ra == 0 && update) { ... fatal("TODO: ra=0 &&
  update?\n"); goto bad; }` after the table selection (the D/DS-form arm's copy; the indexed arm has a second) -- reaches
  `goto bad` for `ldu`/`stdu` with RA = 0 once the repair sets `update`.  Today those words execute as `ld`/`std` from the
  ABSOLUTE address (DS || XO), no update.  So the repair turns "executes at an absolute EA+1" into "the CPU stops".  Check;
  is that change right?
* **P6 -- no illegal-instruction delivery exists** (S5, S6): the only disposition for an illegal PowerPC encoding is `goto
  bad`.  Did I miss a Program-interrupt path (grep `ppc_exception(`, `0x700`, `PROGRAM` under `src/cpus/`)?
* **P7 -- the 32-bit sibling census** (S12).  One 64-bit-only family is gated on 32-bit CPUs (`rld*`), one is not
  (`stdx`/`stdux`), one is absent everywhere (`ldx`/`ldux`/`lwax`/`lwaux`).  Complete?  Is any other 64-bit-only
  instruction in `X(to_be_translated)` gated or ungated (`mulld`, `divd`, `sld`, `srd`, `srad`, `extsw`, `cntlzd`, `td`,
  `ldarx`/`stdcx.` ...)?
* **P8 -- the EA domain after the repair.**  No alignment gate exists on this path: no alignment vector (S5); the fast path
  hands every unaligned non-byte access to the generic handler (`if (addr & (LS_SIZE-1)) { LS_GENERIC_N(cpu, ic); return;
  }`); on PPC970 every access is generic anyway (S8).  Book III v2.01's Alignment-interrupt list (8.11) names no big-endian
  single-register fixed-point load or store; the PEM (:11975) says a misaligned access "may either cause an alignment
  exception or ... break the memory access into multiple, smaller accesses".  So after the repair the EA can be ANY byte
  address -- a base that is not a multiple of 8 gives an unaligned `ld`/`std` -- as for `lwz` today.  Check; does
  anything in the design assume a 4- or 8-aligned EA?
* **P9 -- the predicted pre-fix stores** (section 2): `std` correct; `stdu` at EA+1, RA unchanged; 62/XO 2 and XO 3 at EA+2
  and EA+3.  Check against 8.2 and 8.7.
* **P10 -- the disassembler shares the fold, and is guest-invisible.**  Its load/store arm takes `imm = (int16_t)(iword &
  0xffff);` and prints `ld` for every opcode-58 word and `std` for every opcode-62 word, with no XO test (8.9); the
  witness's `unassemble` shows `ld r5,-95(r21)` for an `ldu` word and `ld r6,10(r22)` for an `lwa` word.  The debugger's
  `unassemble` calls it with `running = 0` (`len = cpu_disassemble_instr(m, c, buf, 0, addr);`,
  `src/debugger/debugger_cmds.c`), which reads nothing; the instruction trace calls it with `running = 1`, and for loads it
  previews a `NO_EXCEPTIONS` read of the computed address (the witness's `<0x20021: ...>`).  Neither writes guest state.
  Check both claims.
* **P11 -- the witness's validity (R14).**  (i) RED on HEAD shown; the post-fix GREEN half owed.  (ii) Liveness = `live`;
  the ladder's "device-signature" control is written for device access -- here its role (the value could only have come
  from the decode under test) is played by the counting pattern, which names the offset, beside the green `ld` (XO 0) and
  `lwz` controls on the same pattern.  (iii) Unmodified `bareppc`, no CPU override.  Sufficient for a DECODE witness, or is
  a control missing?
* **P12 -- `testppc` versus `bareppc`.**  The design names `testppc`; the witness used `bareppc`.  Both are `machine_test.c`
  entries whose `MACHINE_DEFAULT_CPU` sets `machine->cpu_name = strdup("PPC970");`; `bareppc` has no devices.  Equivalent
  for every row this round owes?
* **P13 -- clause (b)'s fixed sites.**  Three edited decoder lines -- the displacement line and the two XO-blind `case`
  lines -- plus the disassembler's displacement and two mnemonic lines if Q1(g) joins it.  Any other site?
* **P14 -- the D-form control cannot see the repair's scope.**  The design clears the low two bits for opcodes 58 and 62
  ONLY.  The witness's `lwz` control has displacement +8 (low bits 00), so it reads the same whether the clear reaches
  58/62 only or every opcode of the arm.  Check; Q2(e) asks what row that owes.
* **P15 -- a `goto bad` word ends its session's execution.**  `bad:` sets `cpu->running = 0`, so the words after it in a
  stepped session do not run.  The shipped `ppc_rldicl_probe.py` puts its 32-bit `goto bad` word LAST in its own session,
  after a liveness `li` (9.5: rows `bits32 live`, `bits32 rld bad`).  So each illegal-XO word, and each RA = 0 update
  word after the repair, needs its own session or the last slot of one.  Check.

---

## 7. The drafter's partition of the arm -- CHECK IT, do not ratify it

Inputs to the edited lines: the primary opcode (24 labels, S2), XO (2 bits), DS (14 bits signed; the body tests
`imm == 0`), RA (the body tests `ra == 0`), RT/RS where Book I distinguishes RA = RT or RA = RS, and the CPU width (S9).
`update`, `size` and the extension are DERIVED from (opcode, XO), so the axes "opcode x XO x update x size/extension"
collapse onto the eight (opcode, XO) pairs crossed with what the body tests.  "Today" is HEAD; "MEASURED" is the witness;
"predicted" is read from the source.  The last column is my guess for you to correct: FLOOR = a row is owed (R7); (e) =
disclosed under the contract (R10).

| cell | the word | today (HEAD) | after the design | evidence today | FLOOR / (e)? |
|---|---|---|---|---|---|
| C1 | 58/0 `ld`, DS != 0, RA != 0 | MEM(EA,8) -- correct | same | MEASURED green (`ld value`) | FLOOR (XO-0 control) |
| C2 | 58/0 `ld`, DS = 0 | correct (`_0` handler) | same | none | (e)? |
| C3 | 58/0 `ld`, RA = 0 | MEM(DS||00, 8), absolute -- correct | same | none | (e)? |
| C4 | 58/1 `ldu`, DS != 0, RA != 0, RA != RT | MEM(EA+1,8); RA unchanged | MEM(EA,8); RA <- EA | MEASURED red (2 rows) | FLOOR |
| C5 | 58/1 `ldu`, DS = 0 | MEM(RA+1,8); RA unchanged | MEM(RA,8); RA <- RA (update INVISIBLE) | none | FLOOR? (P2) |
| C6 | 58/1 `ldu`, RA = 0 | MEM(DS||01, 8), absolute; no update | `goto bad` -- CPU stops | none | FLOOR? (P5) |
| C7 | 58/1 `ldu`, RA = RT != 0 (invalid) | MEM(EA+1,8) into RT | RT = EA (P4) | none | (e) per CRIT -- D1 |
| C8 | 58/2 `lwa`, DS != 0, word bit 31 SET | 8 bytes from EA+2 | EXTS(MEM(EA,4)) | MEASURED red | FLOOR |
| C9 | 58/2 `lwa`, word bit 31 CLEAR | 8 bytes from EA+2 | MEM(EA,4), high half 0 | none | (e)? |
| C10 | 58/2 `lwa`, DS = 0 | 8 bytes from RA+2 | EXTS(MEM(RA,4)) | none | FLOOR? (P2) |
| C11 | 58/2 `lwa`, RA = 0 | absolute EA+2, 8 bytes | absolute, EXTS word | none | (e)? |
| C12 | 58/3 (illegal) | 8 bytes from EA+3 into RT | `goto bad`; RT, RA unchanged | none | FLOOR |
| C13 | 62/0 `std`, DS != 0, RA != 0 | MEM(EA,8) <- RS -- correct (predicted) | same | none | FLOOR (XO-0 control) |
| C14 | 62/0 `std`, DS = 0 or RA = 0 | correct (predicted) | same | none | (e)? |
| C15 | 62/1 `stdu`, DS != 0, RA != 0 | MEM(EA+1,8) <- RS; RA unchanged (predicted) | MEM(EA,8) <- RS; RA <- EA | none | FLOOR (clause (a) for stores) |
| C16 | 62/1 `stdu`, DS = 0 | MEM(RA+1,8) <- RS; RA unchanged (predicted) | MEM(RA,8) <- RS; RA <- RA (INVISIBLE) | none | FLOOR? (P2) |
| C17 | 62/1 `stdu`, RA = 0 (invalid) | MEM(DS||01, 8) <- RS, absolute (predicted) | `goto bad` | none | FLOOR? (P5) |
| C18 | 62/1 `stdu`, RA = RS != 0 (VALID) | MEM(EA+1,8) <- RS; RA unchanged (predicted) | MEM(EA,8) <- old RS; RA <- EA | none | FLOOR? (Astra: valid aliasing) |
| C19 | 62/2 (illegal) | MEM(EA+2,8) <- RS (predicted) | `goto bad`; memory, RA unchanged | none | FLOOR |
| C20 | 62/3 (illegal) | MEM(EA+3,8) <- RS (predicted) | `goto bad` | none | FLOOR |
| C21 | a D-form LOAD whose displacement has non-zero low two bits | EA = RA + D | unchanged -- must NOT be cleared | none (`lwz` uses +8) | FLOOR? (P14) |
| C22 | a D-form STORE, same | EA = RA + D | unchanged | none | FLOOR? (P14) |
| C23 | D-form update forms; FP D-forms | unchanged | unchanged | none | (e)? |
| C24 | 58 / 62 on a 32-bit CPU | 8-byte `ld`/`std` with the fold | per Q1(e) | none | per Q1(e) |
| C25 | the disassembler's text per (opcode, XO) | `ld`/`std` + raw halfword | per Q1(g) | MEASURED (census, 3 opcode-58 words) | per Q1(g) |
| C26 | an update form whose access FAILS (Astra: "suppressed base update on access failure") | RA not written (S8) | same -- the handler is not edited | none | (e)? -- a callee property; and I believe no data access fails on `bareppc` with translation off, while translation on PPC970 meets the separate N3 exit first |

Twenty-six cells.  Which "?" cells are FLOOR, which (e), and is a cell missing or mislabelled (Q2(d))?

---

## 8. SOURCE, INLINED -- HEAD `add098b9` line numbers (CUT: 8.1, 8.3-8.6, 8.10-8.14 are in the FULL form; S3, S5, S6, S11, S12, P8 state what the premises take from them)

**8.2 THE EDIT SITE -- the D/DS-form arm, WHOLE** (`src/cpus/cpu_ppc_instr.c` 4268-4352; the `ra == 0 && update` block is
lines 4338-4342; after `break` the common tail executes the new instruction, `goto bad` stops the CPU -- S6):
~~~~
4268| 
4269| 	case PPC_HI6_LBZ:
4270| 	case PPC_HI6_LBZU:
4271| 	case PPC_HI6_LHZ:
4272| 	case PPC_HI6_LHZU:
4273| 	case PPC_HI6_LHA:
4274| 	case PPC_HI6_LHAU:
4275| 	case PPC_HI6_LWZ:
4276| 	case PPC_HI6_LWZU:
4277| 	case PPC_HI6_LD:
4278| 	case PPC_HI6_LFD:
4279| 	case PPC_HI6_LFDU:	/*  #310  */
4280| 	case PPC_HI6_LFS:
4281| 	case PPC_HI6_LFSU:	/*  #310  */
4282| 	case PPC_HI6_STB:
4283| 	case PPC_HI6_STBU:
4284| 	case PPC_HI6_STH:
4285| 	case PPC_HI6_STHU:
4286| 	case PPC_HI6_STW:
4287| 	case PPC_HI6_STWU:
4288| 	case PPC_HI6_STD:
4289| 	case PPC_HI6_STFD:
4290| 	case PPC_HI6_STFDU:	/*  #310  */
4291| 	case PPC_HI6_STFS:
4292| 	case PPC_HI6_STFSU:	/*  #310  */
4293| 		rs = (iword >> 21) & 31;
4294| 		ra = (iword >> 16) & 31;
4295| 		imm = (int16_t)iword;
4296| 		load = 0; zero = 1; size = 0; update = 0; fp = 0;
4297| 		ic->f = NULL;
4298| 		switch (main_opcode) {
4299| 		case PPC_HI6_LBZ:  load=1; break;
4300| 		case PPC_HI6_LBZU: load=1; update=1; break;
4301| 		case PPC_HI6_LHA:  load=1; size=1; zero=0; break;
4302| 		case PPC_HI6_LHAU: load=1; size=1; zero=0; update=1; break;
4303| 		case PPC_HI6_LHZ:  load=1; size=1; break;
4304| 		case PPC_HI6_LHZU: load=1; size=1; update=1; break;
4305| 		case PPC_HI6_LWZ:  load=1; size=2; break;
4306| 		case PPC_HI6_LWZU: load=1; size=2; update=1; break;
4307| 		case PPC_HI6_LD:   load=1; size=3; break;
4308| 		case PPC_HI6_LFD:  load=1; size=3; fp=1;ic->f=instr(lfd);break;
4309| 		case PPC_HI6_LFDU: load=1; size=3; fp=1; update=1;
4310| 				   ic->f=instr(lfdu); break;	/*  #310  */
4311| 		case PPC_HI6_LFS:  load=1; size=2; fp=1;ic->f=instr(lfs);break;
4312| 		case PPC_HI6_LFSU: load=1; size=2; fp=1; update=1;
4313| 				   ic->f=instr(lfsu); break;	/*  #310  */
4314| 		case PPC_HI6_STB:  break;
4315| 		case PPC_HI6_STBU: update=1; break;
4316| 		case PPC_HI6_STH:  size=1; break;
4317| 		case PPC_HI6_STHU: size=1; update=1; break;
4318| 		case PPC_HI6_STW:  size=2; break;
4319| 		case PPC_HI6_STWU: size=2; update=1; break;
4320| 		case PPC_HI6_STD:  size=3; break;
4321| 		case PPC_HI6_STFD: size=3; fp=1; ic->f = instr(stfd); break;
4322| 		case PPC_HI6_STFDU: size=3; fp=1; update=1;
4323| 				   ic->f = instr(stfdu); break;	/*  #310  */
4324| 		case PPC_HI6_STFS: size=2; fp=1; ic->f = instr(stfs); break;
4325| 		case PPC_HI6_STFSU: size=2; fp=1; update=1;
4326| 				   ic->f = instr(stfsu); break;	/*  #310  */
4327| 		}
4328| 		if (ic->f == NULL) {
4329| 			ic->f =
4330| #ifdef MODE32
4331| 			    ppc32_loadstore
4332| #else
4333| 			    ppc_loadstore
4334| #endif
4335| 			    [size + 4*zero + 8*load + (imm==0? 16 : 0)
4336| 			    + 32*update];
4337| 		}
4338| 		if (ra == 0 && update) {
4339| 			if (!cpu->translation_readahead)
4340| 				fatal("TODO: ra=0 && update?\n");
4341| 			goto bad;
4342| 		}
4343| 		if (fp)
4344| 			ic->arg[0] = (size_t)(&cpu->cd.ppc.fpr[rs]);
4345| 		else
4346| 			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
4347| 		if (ra == 0)
4348| 			ic->arg[1] = (size_t)(&cpu->cd.ppc.zero);
4349| 		else
4350| 			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);
4351| 		ic->arg[2] = (ssize_t)imm;
4352| 		break;
~~~~

**8.7 The load/store handler template -- the address, failure-return and update lines** (`src/cpus/cpu_ppc_instr_loadstore.c`;
`LS_GENERIC_N` is the generic handler, `LS_N` the fast path; the generator includes the file once per flag combination, and
`#ifndef LS_IGNOREOFS` means a `_0` pass reuses the generic function its non-`_0` pass defined):
~~~~
41| #ifndef LS_IGNOREOFS
42| void LS_GENERIC_N(struct cpu *cpu, struct ppc_instr_call *ic)
43| {
44| #ifdef MODE32
45| 	uint32_t addr =
46| #else
47| 	uint64_t addr =
48| #endif
49| 	    reg(ic->arg[1]) +
50| #ifdef LS_INDEXED
51| 	    reg(ic->arg[2]);
52| #else
53| 	    (int32_t)ic->arg[2];
54| #endif
  ...
87| #ifdef LS_LOAD
88| 	if (!cpu->memory_rw(cpu, cpu->mem, addr, data, sizeof(data),
89| 	    MEM_READ, CACHE_DATA)) {
90| 		/*  Exception.  */
91| 		if (!cpu->running)
92| 			cpu->cd.ppc.next_ic = &nothing_call;
93| 		return;
94| 	}
  ...
119| #ifndef LS_ZERO
120| 	    (int32_t)
121| #else
122| 	    (uint32_t)
123| #endif
124| 	    ((data[0] << 24) + (data[1] << 16) +
125| 	    (data[2] << 8) + data[3]);
  ...
174| 	if (!cpu->memory_rw(cpu, cpu->mem, addr, data, sizeof(data),
175| 	    MEM_WRITE, CACHE_DATA)) {
176| 		/*  Exception.  */
177| 		if (!cpu->running)
178| 			cpu->cd.ppc.next_ic = &nothing_call;
179| 		return;
180| 	}
181| #endif
182| 
183| #ifdef LS_UPDATE
184| 	reg(ic->arg[1]) = addr;
185| #endif
186| }
  ...
190| void LS_N(struct cpu *cpu, struct ppc_instr_call *ic)
191| {
192| #ifndef MODE32
193| 	/************************************************************/
194| 	/* For now, 64-bit access is done using the slow fallback.  */
195| 	if (!cpu->is_32bit) {
196| 		LS_GENERIC_N(cpu, ic);
197| 		return;
198| 	}
199| #endif
200| 
201| 
202| #ifdef MODE32
203| 	uint32_t addr =
204| #else
205| 	uint64_t addr =
206| #endif
207| 	    reg(ic->arg[1])
208| #ifdef LS_INDEXED
209| 	    + reg(ic->arg[2])
210| #else
211| #ifndef LS_IGNOREOFS
212| 	    + (int32_t)ic->arg[2]
213| #endif
214| #endif
215| 	    ;
  ...
224| #ifdef LS_UPDATE
225| 	uint32_t new_addr = addr;
226| #endif
227| 
228| #ifndef LS_B
229| 	if (addr & (LS_SIZE-1)) {
230| 		LS_GENERIC_N(cpu, ic);
231| 		return;
232| 	}
233| #endif
  ...
327| #ifdef LS_UPDATE
328| 	reg(ic->arg[1]) = new_addr;
329| #endif
~~~~

**8.8 The table -- the slots the five forms and the `invalid` entries occupy** (`src/cpus/tmp_ppc_loadstore.c`, generated and
committed; slot n = line - 894, index = size + 4*zero + 8*load + 16*(imm==0) + 32*update -- the arm's own expression at
4335-4336; each line VERBATIM, the slot annotation added):
~~~~
893| void (*ppc_loadstore[64])(struct cpu *, struct ppc_instr_call *) = {
897| 	ppc_instr_std,      <- slot 3
901| 	ppc_instr_std,      <- slot 7
904| 	ppc_instr_lwa,      <- slot 10
905| 	ppc_instr_invalid,      <- slot 11
909| 	ppc_instr_ld,      <- slot 15
913| 	ppc_instr_std_0,      <- slot 19
917| 	ppc_instr_std_0,      <- slot 23
920| 	ppc_instr_lwa_0,      <- slot 26
921| 	ppc_instr_invalid,      <- slot 27
925| 	ppc_instr_ld_0,      <- slot 31
929| 	ppc_instr_stdu,      <- slot 35
933| 	ppc_instr_stdu,      <- slot 39
937| 	ppc_instr_invalid,      <- slot 43
941| 	ppc_instr_ldu,      <- slot 47
945| 	ppc_instr_stdu_0,      <- slot 51
949| 	ppc_instr_stdu_0,      <- slot 55
953| 	ppc_instr_invalid,      <- slot 59
957| 	ppc_instr_ldu_0      <- slot 63
~~~~

**8.9 The disassembler's load/store arm** (`src/cpus/cpu_ppc.c` 1468-1551 -- the operand print and the `running` preview
included; the arm goes on to print the previewed value and ends at 1601):
~~~~
1468| 	case PPC_HI6_LD:
1469| 	case PPC_HI6_LWZ:
1470| 	case PPC_HI6_LWZU:
1471| 	case PPC_HI6_LHZ:
1472| 	case PPC_HI6_LHZU:
1473| 	case PPC_HI6_LHA:
1474| 	case PPC_HI6_LHAU:
1475| 	case PPC_HI6_LBZ:
1476| 	case PPC_HI6_LBZU:
1477| 	case PPC_HI6_LFD:
1478| 	case PPC_HI6_LFS:
1479| 	case PPC_HI6_LMW:
1480| 	case PPC_HI6_STD:
1481| 	case PPC_HI6_STW:
1482| 	case PPC_HI6_STWU:
1483| 	case PPC_HI6_STH:
1484| 	case PPC_HI6_STHU:
1485| 	case PPC_HI6_STB:
1486| 	case PPC_HI6_STBU:
1487| 	case PPC_HI6_STMW:
1488| 	case PPC_HI6_STFD:
1489| 	case PPC_HI6_STFS:
1490| 		/*  NOTE: Loads use rt, not rs, but are otherwise similar
1491| 		    to stores  */
1492| 		load = 0; wlen = 0;
1493| 		rs = (iword >> 21) & 31;
1494| 		ra = (iword >> 16) & 31;
1495| 		imm = (int16_t)(iword & 0xffff);
1496| 		fpreg = 0;
1497| 		switch (hi6) {
1498| 		case PPC_HI6_LD:  load=1; wlen = 8; mnem = "ld"; break;
1499| 		case PPC_HI6_LWZ:  load=1; wlen = 4;
1500| 			mnem = power? "l" : "lwz"; break;
1501| 		case PPC_HI6_LWZU: load=1; wlen = 4;
1502| 			mnem = power? "lu" : "lwzu"; break;
1503| 		case PPC_HI6_LHZ:  load=1; wlen = 2;
1504| 			mnem = "lhz"; break;
1505| 		case PPC_HI6_LHZU: load=1; wlen = 2;
1506| 			mnem = "lhzu"; break;
1507| 		case PPC_HI6_LHA:  load=2; wlen = 2;
1508| 			mnem = "lha"; break;
1509| 		case PPC_HI6_LHAU: load=2; wlen = 2;
1510| 			mnem = "lhau"; break;
1511| 		case PPC_HI6_LBZ:  load=1; wlen = 1;
1512| 			mnem = "lbz"; break;
1513| 		case PPC_HI6_LBZU: load=1; wlen = 1;
1514| 			mnem = "lbzu"; break;
1515| 		case PPC_HI6_LFD:  load=1; fpreg=1; wlen=8; mnem = "lfd"; break;
1516| 		case PPC_HI6_LFS:  load=1; fpreg=1; wlen=4; mnem = "lfs"; break;
1517| 		case PPC_HI6_STD:  wlen=8; mnem = "std"; break;
1518| 		case PPC_HI6_STW:  wlen=4; mnem = power? "st" : "stw"; break;
1519| 		case PPC_HI6_STWU: wlen=4; mnem = power? "stu" : "stwu"; break;
1520| 		case PPC_HI6_STH:  wlen=2; mnem = "sth"; break;
1521| 		case PPC_HI6_STHU: wlen=2; mnem = "sthu"; break;
1522| 		case PPC_HI6_STB:  wlen=1; mnem = "stb"; break;
1523| 		case PPC_HI6_STBU: wlen=1; mnem = "stbu"; break;
1524| 		case PPC_HI6_LMW:  load=1; mnem = power? "lm" : "lmw"; break;
1525| 		case PPC_HI6_STMW: mnem = power? "stm" : "stmw"; break;
1526| 		case PPC_HI6_STFD: fpreg=1; wlen=8; mnem = "stfd"; break;
1527| 		case PPC_HI6_STFS: fpreg=1; wlen=4; mnem = "stfs"; break;
1528| 		}
1529| 		debug("%s\t", mnem);
1530| 		if (fpreg)
1531| 			debug("f");
1532| 		else
1533| 			debug("r");
1534| 		debug("%i,%i(r%i)", rs, imm, ra);
1535| 		if (!running)
1536| 			break;
1537| 		addr = (ra==0? 0 : cpu->cd.ppc.gpr[ra]) + imm;
1538| 		if (cpu->cd.ppc.bits == 32)
1539| 			addr &= 0xffffffff;
1540| 		symbol = get_symbol_name(&cpu->machine->symbol_context,
1541| 		    addr, &offset);
1542| 		if (symbol != NULL)
1543| 			debug(" \t<%s", symbol);
1544| 		else
1545| 			debug(" \t<0x%" PRIx64, (uint64_t) addr);
1546| 		if (wlen > 0 && load && wlen > 0) {
1547| 			unsigned char tw[8];
1548| 			uint64_t tdata = 0;
1549| 			int i, res = cpu->memory_rw(cpu, cpu->mem, addr, tw,
1550| 			    wlen, MEM_READ, NO_EXCEPTIONS);
1551| 			if (res) {
~~~~

---

## 9. Detector-shape facts for Q3 -- CONDENSED (the FULL form quotes each VERBATIM at HEAD)

* **9.1 Gate 13 (`regress/gate_ppc.sh`).**  Its only skip points before its three register-to-register PowerPC blocks are
  `need_exec "$PMAX"` and the `python3` check; the blocks (`ppc_rlwimi_probe.py` pinned at 28 rows, `ppc_rldimi_probe.py` at
  29, `ppc_rldicl_probe.py` at 24) all run on `-E bareppc -M 64` BEFORE `need_file "$IMAGES/netbsd401-macppc-GENERIC"`,
  after which a missing image SKIPs the rest of the gate.  The `#565` block checks `PPC_RLDICL_PROBE_DONE` exactly once,
  then each of the 24 rows by name with `count "$RLCLOG" "^$v  .*ok$"` = 1, then rows run 24, green 24, red 0, and exactly
  one `SCORE 24/24` line.  Its header records the zero-offset trap, VERBATIM:
~~~~
47| # The two non-update rows assert the mirror image, that the base is UNCHANGED --
48| # and their displacement and index are NONZERO on purpose. With a zero offset
49| # the effective address equals the base, so a wrongly-updating implementation
50| # would write back exactly the value the row expects: the same seat found both
51| # controls vacuous that way.
~~~~

* **9.2 Gate 14 (`regress/gate_arm.sh`), the `#570` block:** the sentinel present and exactly once; `M88K_BUSERR_RESULT=`
  parsed with both halves pinned to 31; `M88K_BUSERR_CONTROL=OK` once; `M88K_BUSERR_SYMPTOM=ABSENT` once; each of 31 rows by
  name `^$v  .*ok$` = 1; emitted 31, green 31, red 0.  Its comment says it "runs only if none of this gate's eleven earlier
  skip points fired".

* **9.3 The MANIFEST at HEAD** (`tools/pipeline/check_probe_wiring.py`): `#570` lists `"m88k_buserr_probe.py"` as
  `CLASS_DETECTOR` ("... gated in gate_arm.sh (gate 14) under the stem m88k_buserr, pinned at 31; ...") and its witness
  `"artifacts/m88kbuserrregs/witness_20261023/m88k_buserr_probe.py"` as `CLASS_WITNESS`; its kill table's frozen
  instrument, drivers and staged copies "are kept as *.py.txt / *.sh.txt, outside this checker's domain".

* **9.4 `regress/lib.sh`:** `check NAME GOT WANT` passes on string equality; `count FILE PATTERN` is `grep -ac -- PATTERN FILE`
  (0 when the file is missing).

* **9.5 `regress/ppc_rldicl_probe.py`:** its `disasm xcheck` control -- each placed word "is disassembled by the tree's own
  disassembler (cpu_ppc.c, a DIFFERENT code path from the execute handler in cpu_ppc_instr.c) and compared against the
  operands the encoder intended.  Guards the hand-assembled-encoding trap." -- and its 32-bit session inside the gated
  detector (a `-C PPC603` session whose `li` runs and whose `rld*` word reaches `goto bad`), whose rows read, VERBATIM:
~~~~
494|     "PPC603 (32-bit): the guest still runs -- li executes")
495| row("bits32 rld bad", "TODO" if "TODO: rld" in b32T else "no-msg", "TODO",
496|     "decoder prints `TODO: rld* in 32-bit mode?' and goes to bad -- unreachable")
497| 
~~~~

* **9.6 The witness probe's `row()`** prints each row as `"%-16s %-20s %-20s %-52s %s"` after `assert len(name) <= 15, name`
  and a DUPLICATE-ROW-NAME assert, so a gate's `^name  ` (name plus two spaces) cannot match a neighbour.

---

## 10. The project rules the questions apply -- CONDENSED to the sentences the questions use, each with its bound

Each quotation below is VERBATIM from the working-tree carrier `tools/CLAUDE.md` (byte-identical to the root `CLAUDE.md`;
HEAD's copy lacks R2's block and R8, adopted 2026-10-09), joined across line breaks with its `>` quote markers removed.  The
FULL form quotes every block whole with line numbers.

* **R1 -- THE FLOOR (:1328-1333).** "A detector is VACUOUS — replace it IN-ROUND — unless it (a) fails on the pre-fix build, (b) fails on a **VERBATIM REINSTATEMENT of the removed defect at EVERY fixed site**, and (c) fails on a **NULL MEDIUM** -- a product medium carrying none of the behaviour under test"  Bound: "Below the floor, the round's own claim to have "shipped a detector with the fix" is a WRONG RECORD"
* **R2 -- clause (c) (:1340-1367).** "an instruction-handler round: an IDENTITY BODY (decode and retire, write nothing) -- the recommended default"; "a runtime probe: an ABSENT or NON-EMULATOR binary (every session dies), or a build WITHOUT the device for a device round;"  "**THE PRE-FIX BUILD IS CLAUSE (a)'S MEDIUM AND NEVER CLAUSE (c)'S.**"  The two forms: "* `(c): measured at <artifact>` -- the leg was run and its receipt is durable;" and "* `(c): by construction via <row/pin>, leg not run` -- e.g. the gate pins the row count by EQUALITY and a named row reds on a dead run, or the differential `#include`s the product and its gate reds on a compile failure."  Bound: "**A by-construction claim is checked by READING that shape; where the reading fails -- no runtime gate wiring, no pin, `check_min`, a control computed over the row list (`all([])` is True) -- the leg is OWED**"
* **R3 -- clause (d) (:1376-1377).** "**(d) The detector must also fail when the fix is PRESENT but its REPAIR IS NULLED — the guard kept, its effect removed.**"
* **R4 -- the (d) shape when the fix adds a predicate (:1428-1430).** "* **fix ADDS a predicate** -> weaken the added one"
* **R5 -- the DEPENDS-ON bound (:1448-1451).** "**DEPENDS ON enumerates exactly two things: (1) the predicates DOMINATING the diff's edited lines, walked up only to the ENCLOSING FUNCTION BOUNDARY -- never into callees or callers; and (2) for operand-swap forms, swaps drawn ONLY from fields the guarded BODY reads (the guard-field/body-field grep the pre-table check already mandates).**"
* **R6 -- joint cells (:1464-1472).** "For each lvalue take the PARTITION the body's own tests induce (`pending > 0` gives {0, >0}; `relative_addr == PCCTWO_T1ICR` gives {T1, T2}); the enumerated cells are the CROSS-PRODUCT of those partitions -- never arbitrary boolean functions of the read-set."  Bound: "A value or combination the body never tests as a case (`idata == k`; a byte no conditional distinguishes; both counts >= 2 where the body tests `> 0`) is DISCLOSED under clause (e)."
* **R7 -- floor versus (e) (:1517-1522).** "**The rule ENUMERATES joint cells wherever the body distinguishes them; the FLOOR -- the cells a row is OWED for -- is the cross-product of the guard's dominating predicates with the device-STATE lvalues the fix's own repair path reads that are JOINTLY REACHABLE through its own data flow.**"  Bound: "A filter may reject or discharge a cell but may demand a new row only for a floor cell -- so it cannot grow unbounded."
* **R8 -- rule D2 (:1557-1566).** "For a relational compare against a constant bound B that a fix DEPENDS ON (`X > B`, `e < 96`), each region of its generating set is discharged by the row that varies under the LEAST-OBSERVABLE non-equivalent move of B: **X = B+1 for the region past the bound and X = B-1 for the region below it**"  Bound: "**Bound: at most two rows per compare the fix depends on -- the compare's own two edges.**"
* **R9 -- the CHANNEL line (:1741).** "for each row, name **the mutant it kills** and **the observable that differs under that mutant**. A row whose named channel cannot vary under its named mutant is VACUOUS BY CONSTRUCTION, and that is knowable at writing time, before any table runs"
* **R10 -- clause (e), the contract (:1801-1805).** "The probe header names which edits this detector is designed to catch. *A detector that says so is falsifiable; one claiming completeness is not*"
* **R11 -- the anchored row and its check (:1888-1898).** "**A DETECTOR CLAIMING TO PIN *WHERE* AN ACCESS LANDS MUST CARRY AT LEAST ONE ANCHORED ROW: an oracle tied to a SPECIFIC CELL by a channel OUTSIDE the decode under test**"  Check: "***"If every address in this device shifted one word, which row reds?"*** If the answer is NONE, position is unpinned, whatever the row count."
* **R12 -- the option set (:2023-2072).** "**1 DELETE  ·  2 DECLINE (silent)  ·  3 DECLINE + BOUNDED (LATCHED) ANNOUNCE  · 4 ACCEPT  ·  5 FAULT  ·  6 BACKED ACCEPT  ·  7 IMPLEMENT**"  Its availability rule: "**BEFORE CHOOSING A MEMBER, CHECK IT IS AVAILABLE ON THIS CPU.**  The set is a menu of dispositions, not a menu of things every machine can do"  And: "**Before choosing, GREP THE FORK FOR AN EXISTING IDIOM -- the tree's own precedents are part of the design space.**" ... "**And grep for the SIBLING HANDLERS' disposition in the same file**"
* **R13 -- the addition licence (:2334-2335).** "**Additions to product code in a hardening fork are licensed by MEASURED DELTAS or by a TRANSFERRED WARRANT -- never by "it cannot hurt."**"
* **R14 -- the witness clauses (:2788-2796).** "(i) it shows the defect symptom on the pre-fix committed HEAD and goes green post-fix with the same script"; "(ii) **for ACCESS witnesses (rungs 3–4)** it carries a LIVENESS control (a known value returns through the same decode) AND a DEVICE-SIGNATURE control (the observed value could only have come from the device — RAM would answer differently;" ... "(iii) the machine description and dispatch are committed and unmodified — a machine or `device_add` introduced IN ORDER TO reach the site is laundering, not witnessing."
* **R15 -- the ask-again cap (:2471-2483).** "**CAPPED AT ONE ASK-AGAIN PER DETECTOR PER ROUND.**"  Bound: "Everything ONE ask returns is disposed of INDIVIDUALLY under L1–L4 and the floor — and **a floor breach among the findings is L2, repaired in-round however late it is found.**"
* **R16 -- the oracle-correction rule (:2511-2513).** "**Re-pin the oracle FIRST. Measure the COMMITTED build RED under the new expectations. THEN change the code.**"
* **R17 -- round scope (:2877-2880).** "A round takes ONE site; a second joins only if it is witnessed, in the SAME device and SAME semantic class under the third doctrine arm (so one fix design covers both), and covered by the SAME detector with no new oracle."
* **R18 -- the dispatch-LABEL clause (:1503).** "a dispatch LABEL is a floor axis of an edited guard when the selector's value FLOWS INTO an lvalue the guarded body reads or writes within the enclosing function (there, `dst_mode = (dst_tlb << 10) + ...` two lines above a repair of `dst_mode |= RGBA`), or when the body re-tests it after the join (TxICR); a label that reaches the edit and touches nothing the body reads is clause (e) (the `mode & COPY` shape)." ... Bound: "The floor it adds is {labels} x the guard operand's body-tested partition -- six cells there, two rows owed -- never the labels' cross-product with everything."
* **R19 -- "tests" means masks or compares (:1545-1547).** "**A RELATIONAL compare such as `idata >= 8` tests NO bit: its generating set is its three regions, below / at / past the bound**"
* *Not binding here: the de-escalation clause binds a diff that DELETES an `exit(` -- this diff deletes none; the XO-0 rows are owed as CONTROLS (section 7).*

---

**THIS FIRING ANSWERS Q3 AND Q4 ONLY.**  Q1 and Q2 went to a separate firing of this same packet; treat the settled design as given here and do not answer them.  Keep hidden reasoning short and put the VERDICT line and the answers in the response itself.

## 11. QUESTIONS -- VERDICT LINE FIRST (format in section 0)

**Q1 -- the repair: complete and correct for the five forms, the illegal XO values, the invalid update forms and 32-bit
CPUs; and is the disassembler in this round?**

(a) **The five forms with the arm's existing flags.**  The design (3.1) takes `imm = (int16_t)(iword & ~3)` for opcodes 58
and 62 ONLY and selects the form by XO; Grok's table (3.3) maps the forms onto the arm's flags -- `ld` load, size 3; `ldu`
the same plus `update`; `lwa` load, size 2, `zero` 0; `std` size 3; `stdu` size 3 plus `update`.  Check each against the
table (8.8, S7) and the generic handler (8.7, S8): does every form select an existing slot, can any reach
`ppc_instr_invalid` (P3), does any need a handler change?  Answer P1 and P2.

(b) **Where the repaired displacement must be visible.**  Which DS/XO inputs make the arm's two uses of `imm` (the table
index and `ic->arg[2]`) matter if they ever see different values (P2)?  Does the design's text guarantee both see the
masked value, or must the round's record say where the assignment sits relative to the table index?  Answer as a
partition of inputs; do not supply an edit.

(c) **The illegal XO values (58/3, 62/2, 62/3).**  Today they execute as `ld`/`std` at EA+3, EA+2, EA+3.  The design:
"reserved XO must not execute as `ld`/`std` (the existing `goto bad`)".  Book I calls them ILLEGAL (S3), architecturally
a Program interrupt, which this tree lacks (S5, P6).  Under the option set and its availability rule (R12): which member
is `goto bad` for an instruction (CPU stop, `UNIMPLEMENTED instruction`, nothing delivered to the guest)?  Is there a
member the design did not name?  Grep the fork for the idiom: the arm's own RA = 0 guard prints `fatal("TODO: ra=0 &&
update?\n")` outside read-ahead and then `goto bad`; opcode 31's and opcode 30's `default:goto bad;` are silent and leave
the message to `bad:` (8.3, 8.5).  Should the illegal-XO arm print its own message?  Does it owe a latch (it cannot
repeat: the CPU stops on the first)?

(d) **The invalid update forms.**  RA = 0 (`ldu`, `stdu`): the existing guard reaches `goto bad` once `update` is set -- a
behaviour change (P5); right?  RA = RT (`ldu`): rule on D1 (3.6) with a reason.  The arm's sibling update loads (`lbzu`,
`lhzu`, `lhau`, `lwzu`) do not check RA = RT either (8.2), and Book I allows "boundedly undefined results" for an invalid
form (S3).  What does the handler do with RA = RT today and after the repair (P4), and is "disclosed, not checked" right?
Does anything in the design treat the VALID `stdu` RA = RS as invalid?

(e) **32-bit CPUs.**  No width test in the arm, and the same source builds the 32-bit decoder (S9); PEM :6253 makes 58 and 62
ILLEGAL on 32-bit implementations (S11).  Today a 32-bit CPU executes them as 8-byte `ld`/`std` with the fold; after the
repair, with no test, it would execute `ldu`/`lwa`/`stdu` too.  Options I can name: (i) disclose, not fixed here (Grok,
D2); (ii) the tree's own opcode-30 idiom -- `if (cpu->cd.ppc.bits == 32) { ... goto bad; }` (8.5, S12) -- applied to
58/62; (iii) let 32-bit CPUs decode the 64-bit forms with no record.  Which, and why?  If (ii): is it licensed by R13 (a
transferred warrant -- the `rld*` idiom plus PEM :6253), does it pass R17 while `stdx`/`stdux` stay ungated (P7), and
what row proves it (9.5's `bits32` rows are the shape)?  If (i): what must the contract disclose?

(f) **Alignment.**  The research texts reject a blanket alignment exception (S14).  Answer P8: does anything in the design
or its rows depend on a 4- or 8-aligned EA?

(g) **The disassembler -- this round, or filed?**  It shares the fold and is guest-invisible (P10).  FOR joining: every
PowerPC probe's disassembler cross-check is this tree's guard against the hand-assembled-encoding trap -- each placed
word "is disassembled by the tree's own disassembler (cpu_ppc.c, a DIFFERENT code path from the execute handler in
cpu_ppc_instr.c) and compared against the operands the encoder intended" (9.5) -- and for 58/62 that path shares the
defect, so it confirms opcode, RT, RA and the raw halfword but never the FORM.  AGAINST: R17 admits a second site only if
"covered by the SAME detector with no new oracle"; a repaired disassembler changes the census oracle (section 2's census
pins today's folded text), an oracle correction (R16) with its own order obligation; and it has no guest effect.  Which?
If it joins: what does the census expect, and in what order is it re-pinned?  If filed: what does the detector's contract
say about the census?

(h) **Anything else the repair must carry** -- a CHANGELOG round block, a `/* #571: */` tag at each edited site, the
ledger `witness` term (Q3(e)).  Is there a design element none of the three research texts named?

**Q2 -- the owed detector rows: complete, consistent, bounded?**

(a) **Clause (a) for BOTH halves (R1).**  LOAD half: the witness is the pre-fix red (5/8: `ldu value`, `ldu RA after`,
`lwa value`).  STORE half: nothing measured.  Which store rows -- `std` (XO 0), `stdu` (XO 1) value and RA, the illegal
62/2 and 62/3 -- with which observable discharge (a) for that half, given they must run on the BASE binary before the fix
(the T36 precedent, section 2)?  For each: what reads back the destination -- the debugger's `dump` (outside the decode),
a reload by a different instruction (which?), or both -- and which neighbouring bytes must be shown unchanged so a store
at EA+1 cannot pass (Astra's "exact store destinations, neighboring bytes", 3.2)?

(b) **Clause (b), verbatim reinstatement at EVERY fixed site (R1).**  Sites per P13.  Which rows red when HEAD's arm is
reinstated verbatim; does any red for the wrong reason (e.g. a session that stops early, P15)?

(c) **Clause (c), the null medium (R2).**  For an instruction-handler round the recommended medium is an IDENTITY BODY --
here, opcodes 58/62 decoded to a body that neither accesses memory nor writes RT or RA (Grok's "(c) Identity body: decode,
retire, memory and RA unchanged", 3.3).  Which medium, and which of the TWO record forms -- `(c): measured at <artifact>`
or `(c): by construction via <row/pin>, leg not run`?  If by construction, name the pin and the row that reds on a dead
run, and predict the dead run's score from the probe's source (`neg apparatus` and `unasm census` do not depend on the
loads).

(d) **Clause (d), the DEPENDS-ON enumeration (R3-R7, R18, R19).**  The predicates dominating the edited lines inside
`X(to_be_translated)`: the primary-opcode `case` labels and the XO test the repair adds (and a width test if Q1(e) adds
one).  The body after the edit tests `imm == 0`, `ra == 0 && update`, `fp`, `ra == 0` (8.2).  Check section 7 against the
code: a dominating predicate missing, a partition wrong, a cell mislabelled?  For each "?" cell: FLOOR (R7) or CLAUSE (e)
(with its derivation), and why -- especially C5 / C10 / C16 (DS = 0, P2), C6 / C17 (RA = 0, P5), C18 (`stdu` RA = RS),
C21 / C22 (the D-form labels under R18), C24 and C26.

(e) **The variants the records already name -- classify them** (the template's smallest-edit question in its checkable
form).  Grok's floor text (3.3) names three (d) nulls -- "displacement masked but `update` left 0 (RA unchanged)",
"`update` set but the raw `int16_t` kept (store at EA+1)", "`lwa` left at `size=3` (the neighbour word is consumed)" --
and a growth variant for the accept row ("A growth mutant that adds 1 to XO=0 reds that row").  For each: which row of the
set you would ship reds, or none does -- and then is it a floor breach or disclosed debt?  The same question as a
partition: which instructions must the repair NOT change, and which row shows it (P14)?

(f) **Controls.**  Are `ld value` (MEASURED green) and an `std` row (C13) enough as XO-0 controls, or is one owed at DS = 0
or RA = 0 too?  Is the `lwz` D-form control kept, or replaced by C21 / C22?

(g) **The anchor rule (R11).**  Loads: the debugger-written counting pattern names the offset each load used -- anchored
by a channel outside the decode.  Stores: what anchors the destination (Q2(a))?  "If every address shifted by one byte,
which row reds?" -- answer it for your store rows, and say whether the 8-byte source value needs eight distinct bytes.

(h) **Rule D2 (R8).**  I find no relational compare against a constant among the predicates the repair depends on: the
`case` labels and XO values are equality tests, `ra == 0`, `imm == 0` and `update` are equality / truth tests, a width
test would be `bits == 32`.  So D2 would be N/A -- confirm, or name the compare.

(i) **The CHANNEL line (R9).**  Three to check.  (1) An update row at DS = 0 cannot vary under "update dropped": EA = RA, so
RA <- EA rewrites the value RA holds -- gate 13's header records the same trap for the FP update forms (9.1).  Which
update rows must use DS != 0?  (2) An illegal-XO row: its channel (RT sentinel kept, RA unchanged, memory unchanged, the
stop message), and must it sit last in its own session (P15)?  (3) `lwa`'s sign: the witness's word 0x88898a8b has bit
31 set, so zero- and sign-extension differ there -- is a positive-word `lwa` row (C9) owed, or (e)?

(j) **The `unassemble` census.**  It expects the tree's CURRENT text for opcode 58 (`ld` + the raw halfword), so it
"confirms each word's opcode, RT, RA and raw low halfword, not architecture" (section 2).  If the disassembler joins
(Q1(g)), the expectation is an oracle correction -- re-pin FIRST, measure HEAD RED under the re-pin, THEN change the code
(R16); if filed, the census stays an observation and the contract says it cannot attest the XO.  Which?  Should the
expected mnemonic come from the row's INTENDED form (its label) rather than the encoder's XO field -- otherwise a wrong
XO in an encoder call yields matching text on both sides?

(k) **Bounded?**  Is the row set closed over the diff (R5, R7), with one ask-again after a clean table (R15)?

**Q3 -- the detector shape and its gate home**

(a) **The detector.**  The witness probe becomes the base of `regress/ppc_dsform_probe.py`; the witness copy stays
byte-identical in `witness_20261024/` as the pre-fix witness (S16).  Sessions: the loads; the stores; one per illegal-XO
word and per RA = 0 update word (each stops the CPU, P15); a 32-bit session if Q1(e) chooses a width test; the census.
How many sessions, in what order, and what in the witness's header (CONTRACT, NOT CLAIMED, the SYMPTOM set, the census
expectations) must change before it moves?

(b) **Gate home: gate 13 (`gate_ppc.sh`) or gate 14 (`gate_arm.sh`)** -- S15, 9.1, 9.2.  Which, where in the file, and what
does the choice cost when an earlier prerequisite of that gate is missing?

(c) **The MANIFEST lines** in `tools/pipeline/check_probe_wiring.py` (9.3, at HEAD): one `CLASS_DETECTOR` line for
`regress/ppc_dsform_probe.py` naming its gate and pin, and one `CLASS_WITNESS` line for
`artifacts/ppcdsformxo/witness_20261024/ppc_dsform_probe.py` once that directory is committed.  Right?  Is anything else
there a `.py` the checker will see (`ppc_dsform_dummy.bin` is not), and should kill-table drivers and frozen copies be
`*.py.txt` as in `#570`?

(d) **Row-identity pinning as `#570` did it in gate 14 (9.2):** the completion sentinel present and exactly once; `RESULT=`
parsed with both halves pinned to a literal; `CONTROL=OK` once; `SYMPTOM=ABSENT` once; every row by name via
`count "$LOG" "^$v  .*ok$"` = 1; rows emitted / green / red pinned (red = 0).  The witness probe already prints names in a
`%-16s` column under a 15-character assert (9.6).  Anything to add -- a liveness row per session, a pin on `RED=`?

(e) **The ledger witness term:** `probe:regress/artifacts/ppcdsformxo/witness_20261024/ppc_dsform_probe.py` (rung 3).  Right?

(f) **What else must stay green.**  The repair edits the arm EVERY PowerPC D-form load and store passes through (S2).  Which
of gate 13's other blocks -- `rlwimi` (28 rows), `rldimi` (29), `rldicl` (24), the NetBSD-image-gated rounding probe (138
rows, whose FP rows use `lfs`/`stfs`/`lfd`/`stfd` and their update forms) -- actually execute the arm, and which other gate
or rig is a PowerPC D-form consumer the round must re-run?

**Q4 -- the standing licence**

If, while verifying a claim, you found something ELSE -- say so.  Two candidates from drafting, for checking rather than as
findings: (1) the disassembler's fold (Q1(g)) -- if filed, with what severity and witness?  (2) `ldx`, `ldux`, `lwax`,
`lwaux` have no `PPC_31_*` define and reach opcode 31's `default:goto bad;` on every CPU (S12): a 64-bit guest's indexed
doubleword or word-algebraic load stops the emulator, while `stdx`/`stdux` are implemented.  I found no ledger row naming
them (a title / state-note grep at HEAD).  Real, already filed under another name, and in or out of scope (R17)?

---

## 12. Paths -- every repository path cited exists at HEAD (checked at drafting); the FULL form lists them one per line.
