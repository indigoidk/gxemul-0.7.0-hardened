# lecsrmask -- pass 1 (design review) and its adjudication pass (F2): the rulings of record

Written 2026-10-25 05:1x by the main loop.  Inputs: the pass-1 brief `packet.md` and its seven seat answers
(`codex_t18p1.txt`, `grok_t18p1.txt`, `ollama_glm_t18p1_Q12/Q34.txt`, `ollama_deepseek_t18p1_Q12/Q34.txt`,
`argon_api_Q12/gemini_web.out` and `argon_api_Q34/gemini_web.out` -- the Argon seat by the web route after its agy
transport walled); the corrections record `PASS1_CORRECTIONS.md` (C1-C15); the F2 packet `f2_20261025/F2_PACKET.md`
and its answers (`codex_t18f2.txt` -- GPT-6 Astra, the ADJUDICATING seat; `ollama_glm_t18f2_A/B.txt`;
`ollama_deepseek_t18f2_A/B.txt`; `grok_t18f2.txt`; Argon's F2 answer OWED -- `argon_transport_20261025.txt`).
Fable 5.1 HELD with its question (`FABLE_HOLD_QUESTION.md`); kimi, minimax and the Opus seat deliberately not fired.

## 1. The verdict of record (GPT-6 Astra, `codex_t18f2.txt`): RATIFY WITH CHANGES -- WRONG: D2, F22

> "retain the CSR3-only repair and 19-row design; correct the evidence claims and floor classification before landing."

Seat verdicts on the F2 packet: Astra RATIFY WITH CHANGES (WRONG: D2, F22); GLM part A RATIFY WITH CHANGES (none
overturned; F1/F20 refined); GLM part B RATIFY WITH CHANGES (no D overturned; three premise errors in accepted text);
DeepSeek A RATIFY WITH CHANGES (F1 refined; F4/F25 cannot settle); DeepSeek B RATIFY WITH CHANGES (WRONG: D4 -> owed);
grok: see section 5 when it lands; Argon: OWED (meter).

## 2. The design, as ruled

* **The repair is CSR3 only** (D1 UPHELD/REFINED by every seat that answered it): `le_register_write()` masks the CSR3
  store with `0x0007`; CSR1 and CSR2 **retain the model's existing behaviour** -- stored whole -- consistent with MAME's
  reported diagnostic requirement.  Form A (an explicit `case 3:` arm; the stored-whole registers stay in `default:`),
  per Astra ("preferably Form A") and GLM B (Q3.5: a default that masks would silently mask any register added later).
  Weight: the Am7990 manual itself (packet 1.1) -- CSR3 "Reserved and read as 0" vs CSR1 "Must be zero" vs CSR2 bare
  "Reserved." -- with MAME (1.3) as the positive evidence that stored-whole is a defensible default.  Unverified chip
  identities of the KN230 / PMAD-AA / luna88k instances do not block the change: both manuals agree on CSR3 (Astra).
* **The record must NOT say** "as the Am7990 does", nor that the C-LANCE reads CSR1 bit 0 as zero: the C-LANCE text says
  only "Must be zero" for CSR1 bit 0 too, and MAME stores CSR1 whole on both chips; a C-LANCE identification would
  settle CSR2 only (GLM B Q2.1, Astra Q2).  The stored-whole choice is an interpreted reading, recorded as one -- in the
  code comment, the probe's docstring and the CHANGELOG.
* **The odd-address warning at `le_chip_init` 180-182 stays** (reachable, since CSR1 is not masked).
* **Both STOP comments in `DEVICE_ACCESS(le)` (986-991, 996-1001) are corrected in the same change as L4 records**
  (D3 refined: same FILE, not the same function; the Ultrix observation is preserved as reported, not as verified).
* **Filed, not fixed** (section 4).

## 3. The detector, as ruled

* Rows: the 20-row revision (`le_csrmask_probe.py`, final md5 in the landing record): `csr3 all` (0xffff -> 0x0007,
  symptom), `csr3 bits` (0x0005, kept), `csr3 hi` (0x0008 -> 0x0000, symptom; D4: OWED under clause (e) once the
  contract promises to catch a low-bit-conditioned mask -- DeepSeek B, Astra, GLM B), `csr3 mix` (0x0015 -> 0x0005,
  symptom; added after GLM B's Q3.3 -- a mask conditioned on bit 3, the bit `csr3 hi` drives, escaped the 19-row set --
  and Argon Q12's saturating-clamp mutant, which the same row reds), the CSR1/CSR2 CONTRACT rows at identity wants
  (F14), `csr1 top` kept as disclosed insurance (D5), the stable rows kept as scored controls.
* **Floor classification (D2 OVERTURNED by Astra):** the floor obligation is the selector LABELS (CSR1, CSR2, CSR3 --
  the siblings of the edited `switch`); kept/dropped bit coverage is clause (e) contract coverage, not a floor cell
  extension of rule D2.  The rows do not change; the record's wording does.
* **The park control** now verifies the breakpoint banner's pc against the halt address (Astra Q3.1: the pass-1
  revision accepted any `BREAKPOINT: pc` line).
* **The contract header** limits "any mask constant change" to the low 16 bits (F7), names the inter-register
  retention and long-term retention limits (Astra Q3.3), states V12's equivalence as "no reader except the indexed RDP
  read-back" (Astra Q3.4), and corrects the anchor mechanism (F24: a four-byte window shift lands one port on the other
  and the other on an unimplemented offset -- not an exchange).
* **Instrument identity (Astra Q3.5, F18):** the 17-row witness (`witness_20261025/`), the 18-row revision
  (`pass1_20261025/det18_HEAD/`, `floor_20261025/`) and the FINAL revision each carry their own measurements; only the
  final instrument's base/fix evidence earns the `probe:` term.
* **Clause (d) variants** (packet 4.3: V7'-V10', V21-V25) are classified by the seats and NOT built in this session:
  the main loop's own response was classifier-stopped once today (on re-emitting the brief), and the standing rule after
  such a stop is to land on the plain regression legs with the variant measurement recorded as OWED (the `#567`
  precedent) -- see the CHANGELOG block.  Clauses (a), (b) and (c) are measured legs (the pre-fix GATE run IS the
  verbatim revert at the one fixed site; the null medium is `/bin/false`).

## 4. Dispositions of the other findings (F-numbers from the F2 packet; Astra's ruling where it differs)

| F | ruling of record | what the landing does |
|---|---|---|
| F1 | REFINE -- "retained emulator behaviour", not silicon behaviour; C-LANCE CSR1 read-zero unestablished | wording in code comment, docstring, CHANGELOG, the filed row |
| F2 | UPHOLD | "read-back only" withdrawn from every record |
| F3 | UPHOLD (L4) | CHANGELOG quotes TM1986 1539 / 1695 / 1734 / 1749 |
| F4 | UPHOLD | the pass-1 tables stand corrected by PASS1_CORRECTIONS C5 |
| F5 | REFINE -> D2 overturned (labels floor; bits clause (e)) | wording |
| F6 | UPHOLD | one verbatim revert = the pre-fix GATE leg |
| F7 | REFINE (low 16 bits) | contract header |
| F8 | UPHOLD | docstring corrected (historical artifacts untouched) |
| F9 | UPHOLD -> D3 | both comments corrected in-round |
| F10 | UPHOLD; broaden the filing (Astra Q3.2: `%x` with `uint64_t relative_addr`/`odata` at 1039, `%05x` at 911) | filed as one records row |
| F11 | UPHOLD | wording |
| F12 | UPHOLD (correction record: working-tree census vs committed name-set defect) | CHANGELOG #572 follow-up addendum sentence |
| F13 | UPHOLD -> D4 owed | `csr3 hi` |
| F14 | UPHOLD | contract rows |
| F15 | UPHOLD (`2956c32d`) | -- |
| F16 | UPHOLD | the 17-row witness copy lands as `.frozen.py` CLASS_WITNESS; later revisions stay `.py.txt` |
| F17 | UPHOLD | the gate block's own reason line |
| F18 | REFINE (three instruments named) | the witness term's text |
| F19 | UPHOLD; the final revision owes its own null-medium leg | measured again on the final revision |
| F20 | REFINE -- record the LACK of a preservation guarantee for CSR1/CSR2 across STOP (TM1986 1513 reload requirement; 2853 "normally not affected"; C-LANCE Appendix B non-preservation), not a required value | the filed row carries both texts |
| F21 | REFINE (scoped observation only) | -- |
| F22 | OVERTURN -- "Write as zeroes" constrains the writer; it does not establish what a prohibited write stores | option-set wording in the record |
| F23 | REFINE (V12' = observational equivalence over reachable states) | docstring |
| F24 | REFINE (anchor mechanism) | docstring |
| F25 | CANNOT SETTLE (Argon pending/owed) | -- |

Disagreements: D1 CSR3-only (upheld by all); D2 overturned (Astra); D3 refined (same file, not same function);
D4 refined (owed under clause (e) via the contract's own text); D5 upheld.

## 5. Grok's F2 answer and Argon's -- appended when they land

**grok (`grok_t18f2.txt`, 05:0x): RATIFY WITH CHANGES -- WRONG: none.**  It tried to break D1 (its own pass-1 position) and
found it stronger: it reports the PMAD-AA TURBOchannel Ethernet specification (DEC 1990; the document `dev_le.c`'s header
says the model follows; web-sourced, NOT on disk -- recorded as grok's reading) giving CSR3 <15:3> "Reserved. Ignored on
write; read as zeros", CSR2 <15:8> "Reserved. Write with zeros." (no read-as-zero sentence), CSR1 bit 0 "must be zero" as
an alignment constraint, and CSR1/CSR2 writes stored while STOP is set.  Its changes, all applied: (F14) CONTRACT rows must
not fail CONTROL -- a red contract row fails the leg, CONTROL stays with the apparatus; (Q3) the csr3 SESSION ORDER is
load-bearing for an OR-accumulating store (0xffff first, then the later values), stated in the docstring; (F2) "read-back
only" is TRUE of the CSR3 store that ships and FALSE of a CSR1 mask -- the record says both; (F17) the gate block's reason
line also cites `gate_arm.sh`'s own `gatedevicesplit` OWED note so another device probe is not compounded silently; (F20)
filing (c) quotes all three preservation sentences (TM1986 2853-2857, C-LANCE Appendix B item 12, and PMAD-AA errata 6 as
grok's reading); (D1) the form-A comment says this MODEL stores CSR1/CSR2 whole, not that the Am7990 does; (D3) the
corrected comments state the datasheet condition and that the model accepts either way.  Fable's held question is
superseded by the narrowing (re-stated in `FABLE_HOLD_QUESTION.md`).

Argon: OWED -- the web meter was exhausted at 04:45 by the pass-1 Q34 packet (`argon_transport_20261025.txt`).

## 6. Filings this round makes (records rows, not edits)

1. `lecsr12readback` -- CSR1 bit 0 and CSR2 bits 15:8 read-back: unspecified by the Am7990 manual; CSR2 documented
   read-zero on the C-LANCE only, CSR1 bit 0 unspecified on both; MAME keeps both writable on the Am7990 (RS2030
   diagnostic note); rpajarola e108b54 masks all three for a 3MIN port this fork lacks.  A per-chip model flag is the
   port if a C-LANCE instance is ever added.  Chip identities of the KN230, PMAD-AA and luna88k instances: unverified.
2. `lestopgate` -- CSR1-3 accessible only while STOP is set (both manuals); the model accepts them always (the Ultrix
   observation in the corrected comments).
3. `lecsr3stopclear` -- CSR3 cleared by RESET or by setting STOP (TM1986 2854; C-LANCE 1199-1200); the model clears it
   only at init.  Plus: no preservation guarantee for CSR1/CSR2 across STOP (TM1986 1513 vs 2853; Appendix B).
4. `lediagfmt` -- `dev_le.c` passes `uint64_t` values to `%i` (1019-1020), `%x` (1039-1040) and `%05x` (911, 921).
5. `lecsr3inert` -- the three implemented CSR3 bits (BSWP/ACON/BCON) are stored and never consulted by the model
   (GLM B Q3.4).
6. The carrier's primary-source list is derived by `ls _scratchpad/*.pdf`, which does not descend into
   `_scratchpad/lance/` (the round's own false "no datasheet on disk" premise).
7. The clause-(d) variant table for this detector (packet 4.3's V7'-V10', V21-V25): OWED.
8. The Argon F2 answer: OWED (meter); the Fable question: HELD.
