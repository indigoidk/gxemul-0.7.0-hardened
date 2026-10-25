# PASS-1 DESIGN REVIEW -- research item T4, ledger row `wdclbaaddr` -- GXemul hardened fork

**Brief v1, PACKET form (for seats that cannot read files: every fact a question depends on is inlined, and nothing here asks you to open a file).**
Drafted 2026-10-24.  Tree under review: `GXEMUL-SEC/` at HEAD `cc1f69cc` -- a RECORDS-ONLY commit on top of
`cb21331c` (the `#571` landing).  `src/devices/dev_wdc.c` was last changed by `e16a8b7c` (`#533`, 2026-09-18); it is
byte-identical at HEAD, in the working tree and in `est/` (md5 `714071619d8f98e85fe48ae566139345`, section 4).  Built from
the working-tree copy of `GXEMUL-SEC/tools/BRIEF_TEMPLATE.md` (it differs from HEAD's; its scoped-settled-premise rule,
permitted-path check, §C5, §C6 and §C7 are applied).

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

**The defect, in plain terms.**  The emulator's IDE/ATA disk model (`src/devices/dev_wdc.c`) serves an ATA command issued
in LBA mode from the cylinder/head/sector (CHS) interpretation of the same taskfile bytes.  Two things combine: (1) the
LBA28 address arithmetic exists but is compiled out (`#if 0`) at BOTH media-access sites, `wdc__read()` and
`wdc__write()`, so every request is addressed with the CHS formula; and (2) the flag that arithmetic would test, `d->lba`,
is decoded from BIT 5 of the Device/Head (SDH) register, where ATA puts the LBA mode bit in BIT 6.  On the default 16-head,
63-sector geometry the sector the model serves differs from the sector the request named for EVERY LBA-mode media command
(S20: an enumeration over every head nibble and cylinder pair finds zero coincidences).  Measured on the committed build
(section 2): a READ of LBA 70 was served sector 69, a READ of LBA 256 was served sector 1007, a READ of LBA 0 was served a
sector of zeros, and a WRITE to LBA 70 landed at sector 69.

**This pass.**  PASS 1, a design review BEFORE any product edit.  The rung-3 witness was MEASURED on the committed
build (section 2).  Section 5 is settled, section 6 asks, section 7 is my DATA -- check it, do not ratify it; section
8 inlines every function an edit lands in.

**Hard limits.**  READ-ONLY.  Do not build, run, copy or modify anything in the repository.  Nobody is asked to write a
guest program, a probe or a code variant: where a question needs a construction, this brief supplies one (7.4 rows, 7.5
variants) and asks you to check or classify it, or asks which inputs a repair changes the answer for.

**This packet is complete for a seat that cannot read files.**  Every fact a question depends on is inlined: the source
as read at HEAD `cc1f69cc` (section 8), the primary sources' load-bearing lines (section 9), the measured witness
(section 2) and the records (section 1).  Paths appear only as citations.  If a premise cannot be settled from this
packet, say NOT CHECKABLE and name what you would need -- that is a useful answer, not a failure.

**The working tree is not clean** (20 tracked files differ from HEAD -- other sessions' work).  Every source line
quoted here is identical at HEAD and in the working tree; four files this round will also touch carry uncommitted
peer hunks: `regress/diff_wdc_identify.c`, `regress/gate_offline.sh`, `regress/gate_sh_rounding.sh`,
`tools/pipeline/check_probe_wiring.py`.

**The roster.**  GLM 5.3 and DeepSeek answer the PACKET form in two firings (Q1+Q2, then Q3+Q4); Gemini 4 Argon answers the
COMPACT form; Grok 4.7 and GPT-6 Astra answer the FULL form, and Astra then adjudicates.  Fable 5.1 is HELD; kimi and
minimax are not fired.  A seat that does not answer is a SEAT FAILURE; a seat deliberately not fired is neither a failure
nor agreement.

**Answer format -- VERDICT LINE FIRST:**
~~~~
VERDICT: READY | READY WITH CHANGES | NOT READY -- <one line>
Q1: <one line>   Q2: <one line>   Q3: <one line>   Q4: <one line>
~~~~
Then one section per question.  Mark each claim DERIVED (from this packet) or NOT CHECKABLE.
Cite by number: settled premises S1-S24, premises P1-P18, cells C1-C20, proposed rows N1-N9, variants V1-V20,
the sources' disagreements D1-D9 (3.5) and the rules R1-R23 (section 10).

---
## 1. The defect -- as the ledger row and the research record it

*A word about the quotations in this section.  The records file this defect under a severity class whose label this brief
does not reproduce; where that label (or a sentence built on it) occurs, it is replaced by a bracketed description and the
quotation is marked CONDENSED.  Every other word is verbatim.*

**1.1 The ledger row at HEAD** (`tools/pipeline/ledger.json`, parsed with python's `json`; `id`, `sev`, `state`, `opened`,
`witness`, `commits` VERBATIM):

    id wdclbaaddr   sev HIGH   state open   opened 2026-10-22   witness none   commits (empty)

Title (CONDENSED): *"devices/dev_wdc.c:wdc__read/wdc__write -- the LBA28 address computation is under `#if 0` and the
SDH decode takes the LBA flag from bit 5 (ATA: bit 6), so LBA-mode requests are addressed as cylinder/head/sector --
[the records' guest-data class], LATENT in this tree (wrong-sector reads and writes reach only a guest that ignores
IDENTIFY word 49, which this model stores as 0)"*

`state_note` (CONDENSED -- the class label bracketed; `[...]` marks each cut):
> QUEUE: external-research batch tail 2 of 6 [...].  Filed 2026-10-22 from the external-fixes research: [...] TRIAGE.md
> row T4 (class [the records' guest-data class]; reach K, guest kernel, firmware or device registers; effort: small;
> report rows: B F2, B rec.1).  [...]  Portable fix: partial, or an idea only -- the LBA28 idea of FreeBSD ports
> patch-src_devices_dev__wdc.c (also DragonFly DPorts), never the patch, which keys on `d->lba` decoded from bit 5.  [...]
> Live only for a guest that ignores word 49 (report B: FreeBSD 10+; UNVERIFIED here).  The round owes the word-49
> decision FIRST, then a bit-6 decode; [...] witness: none -- research finding, not yet reproduced here.

*(The row was filed two days before the witness in section 2 existed; its `witness: none` is true of HEAD.)*

**1.3 `adj_20261022/ADJ_RULINGS.md`** -- section B (lines 15-20, CONDENSED) and the queue tail (line 65, VERBATIM).  Its
header (line 4-5, VERBATIM): *"Both seats read source at HEAD de8c7547; neither built or ran anything."*
> * **T4 (IDE LBA):** FILE as [guest-data class] but mark **LATENT in this tree** -- IDENTIFY word 49 is stored 0
>   (`dev_wdc.c:374-377`), so a guest honouring it never addresses by LBA; the `#if 0` formula (`:470/:562`) means `d->lba`
>   is never read for an address.  Live only for a guest that ignores word 49 (report B says FreeBSD 10+; UNVERIFIED here).
>   DISAGREEMENT: Astra retains present-tense [guest-data reading] and batches it 3rd; Grok (the measurement above) says
>   latent, queue it, batch later, and decide word 49 FIRST.  Grok's argument is the measured one; adopted.  Both: do not
>   port the FreeBSD patch as-is (it keys on bit 5; a CHS `0xa0` sets bit 5); the round owes the word-49 decision and a
>   bit-6 decode.

> Tail, in order: T12 (settled DECLINE, narrow), T4 (word-49 decision first), T8 (after T7, same disposition), T10 (name
> ONE site; exclude the 2^24-byte MEMORY MOVE), T13, N3 (large design; file, do not fold into T6).

**1.5 The research report `B_distro_patches.md`** -- F2 and recommendation 1 (CONDENSED: `[...]` marks each cut; emphasis
dropped; nothing reworded):
> [...] the FreeBSD ports patch [...] Turns the `#if 0` LBA block on (`#if 1`), so
> `offset = 512*(((head&0xf)<<24) + (cyl<<8) + sector)` whenever `d->lba` is set. [...] The FreeBSD patch is unsafe to copy
> as written. The SDH decode at `dev_wdc.c:2015` ("`d->lba   = (idata >> 5) & 1;`") reads bit 5. ATA puts LBA in bit 6
> (0x40); bits 7 and 5 are obsolete and always written as 1.  NetBSD writes `WDSD_IBM (0xa0) | drive<<4 | head` for CHS
> requests. So with the FreeBSD patch, every NetBSD CHS request would be routed down the LBA formula. [...] Honouring LBA
> requests is independent of advertising LBA support. Advertising it would move NetBSD and Linux guests onto the new path.

Recommendation 1: *"FreeBSD ≥ 10 always uses LBA, as the port commit says, and any driver that ignores word 49 does too."*
The report's limit: FreeBSD's "LBA always" behaviour *"is taken from the port commit message; FreeBSD's ATA code was not
re-read."*

**1.6 Related rows** (ledger at HEAD; subjects CONDENSED, quotations VERBATIM): `wdccylwrap` (open) -- IDENTIFY word 1
truncates the cylinder count to 16 bits; its note: *"word 49 advertises no LBA so the CHS words are the guest's only
capacity"*.  `wdcaltoffset` (closed) -- the rung-3 malta precedent this round's witness copies.  `wdcaltdigin` (in work) --
its detector is the one wdc probe gate 10 runs single-leg (S16).  `wdcaltoffleg` (open) -- the two-leg wdc differentials
owe an exit status and a single-leg form (S16).  `wdcaltfixture` (open) -- its exemplar is the `&& !d->lba` qualification
(P17).  **`arcpartlba` is NOT a ledger row**: `OUTSTANDING_BUGS.md` 24253 says *"named in this file only: no ledger row of
its own"*, and 23432 describes it: *"the ARC partition LBA is multiplied by 512 in signed int and overflows"* -- the same
arithmetic class as the disabled formula's `512 * (int)` product (S6, P8).

---

## 2. The witness -- MEASURED on the committed build, before any product edit (VERBATIM)

**2.1 `regress/artifacts/wdclbaaddr/witness_20261024/RUN_IDENTITY.txt`** (whole file):
*`regress/artifacts/wdclbaaddr/witness_20261024/RUN_IDENTITY.txt` (working tree), lines 1-6:*
~~~~
1| run dir: /tmp/gxt2/work/t4/witness_20261024_170332
2| probe md5: 8f3632ffc1c982fd523c7fd28d86f15d
3| base binary: /tmp/gxt2/base/gxemul 2026-10-24_05:35:58 6159736b
4| base dev_wdc.c md5: 714071619d8f98e85fe48ae566139345 (== SEC)
5| rc: 0
6| finished: 2026-10-24 17:04:48
~~~~

**2.2 `RESULTS_base.txt`** (md5 `837b087c6c14b9bba3e17e23b3493f10`; it ends with the completion sentinel
`WDCLBA_PROBE_DONE`; the `got` column packs the two tag words as `(word1 << 16) | word0`, and the tag of sector `n` is
`(~n & 0xffff) << 16 | n`, so `0xffba0045` is sector 69 and `0xfc1003ef` is sector 1007):
*`regress/artifacts/wdclbaaddr/witness_20261024/RESULTS_base.txt` (working tree), lines 4-9, 12, 33-60:*
~~~~
 4| date      2026-10-24 17:03:32
 5| machine   evbmips -e malta   LITTLE endian   (machine desc UNMODIFIED)
 6| wdc       physical 0x180001f0 via bus_pci piix4_ide; KSEG1 0xffffffffb80001f0
 7| disk      /tmp/gxt2/work/t4/witness_20261024_170332/wdc-lba-scratch.img  (4096 sectors; tag n = (n, ~n))
 8| base bin  /tmp/gxt2/base/gxemul
 9| fix bin   (none -- WITNESS run)
    [... lines 10-11 omitted ...]
12| LEG base -- base build, judged against the HEAD column
    [... lines 13-32 omitted ...]
33|   row             got          head         fix         
34|   ram:identify      0x00005a5a   want 0x00005a5a   ok
35|   ram:chs         0x00005a5a   want 0x00005a5a   ok
36|   ram:sdh         0x00005a5a   want 0x00005a5a   ok
37|   ram:lba         0x00005a5a   want 0x00005a5a   ok
38|   ram:lba0        0x00005a5a   want 0x00005a5a   ok
39|   ram:lbawr       0x00005a5a   want 0x00005a5a   ok
40|   id w49          0x00000000   want 0x00000000   ok
41|   id geo          (16, 63)     want H,S!=0       ok
42|   chs s1          0xffff0000   want 0xffff0000   ok
43|   chs s2          0xfffe0001   want 0xfffe0001   ok
44|   chs h1          0xffc0003f   want 0xffc0003f   ok
45|   sdh rb          0x000000e5   want 0x000000e5   ok
46|   sdh rb2         0x000000b3   want 0x000000b3   ok
47|   lba 70          0xffba0045   head 0xffba0045 fix 0xffb90046 [HEAD] ok
48|   lba 256         0xfc1003ef   head 0xfc1003ef fix 0xfeff0100 [HEAD] ok
49|   lba 0           0x00000000   head !=0xffff0000 fix 0xffff0000 [HEAD] ok
50|   lba wr          0xffb90046   head 0xffb90046 fix 0x88887777 [HEAD] ok
51|   lba wr2         0x88887777   head 0x88887777 fix 0xffba0045 [HEAD] ok
52|   neg appar       0x00000001   want 0x00000000   ok
53| 
54|   19/19 passed
55|   CONTROL=PASS
56|   LEG base VERDICT: PASS
57| 
58| ======================================================================================
59| VERDICT   every leg passed its own column
60| WDCLBA_PROBE_DONE
~~~~

*(Lines 14-31 are the six sessions' command lines and their checks: each session's encodings agreed with the
disassembler -- 62/62, 50/50, 14/14, 36/36, 22/22, 306/306 words -- and each parked at its halt breakpoint.)*

**2.4 What the witness establishes, and what it does not** (the drafter's reading -- check it, P15):

* **Ladder clause (i)** (R17): the first half is met -- the symptom on the committed `dev_wdc.c` (md5 = HEAD), before any
  edit, matching the CHS predictions exactly (69; 1007 = H*S - 1; zeros; the write at 69).  The second half -- green
  post-fix with the same script -- is pending: no FIX-column run exists, and "red against FIX" is read from the printed
  `fix` wants.
* **Clause (ii)**: liveness -- the RAM round-trip in each session, each session parked, and the `chs` rows returning known
  tags through the same wdc decode; device signature -- the sector tags, which no RAM cell holds.  (`WITNESS.md` also
  counts the SDH read-back, which a RAM cell would mimic -- P15.)
* **Clause (iii)**: `evbmips -e malta` unmodified; the disk attached `-d iR:` (ordinary operation; the overlay keeps the
  image file unwritten).
* **The binary** is identified by its `dev_wdc.c` md5 and a clearance against that one file; whether `/tmp/gxt2/base` was
  built from HEAD or the working tree is not recorded (the five differing `src/` files are off the malta/wdc path).
* **The instrument is free-running** (`breakpoint add` + `continue`; the `lba0` transcript shows `BREAKPOINT: pc =
  0xffffffff80100050`), every program word cross-checked against the disassembler (490 of 490), and the transcript
  reports *"2 MB (5040 512-byte blocks)"* for the 4,096-sector file (S9).

---
## 3. The design and its sources -- and where they differ

**3.1 The main loop's design**, as handed to this drafter (`DRAFTER_INPUTS.md` 33-54; the coordinator's text, not a
repository record):
*(CONDENSED to its decisions; the FULL and COMPACT forms quote lines 33-54 whole.)*  1. THE REPAIR: decode the LBA flag
from bit 6 and keep the SDH read-back byte-exact; enable the LBA28 formula at BOTH sites; on IDENTIFY word 49 the main
loop's position, *"to be refuted"*, is *"KEEP word 49 = 0 in this round (every rig's guest would otherwise switch from CHS
to LBA addressing -- a guest-visible behaviour change on five rigs that needs its own measured warrant), and FILE the
advertisement as a follow-up whose gate is the five-rig boot battery"*; what must not change: the CHS formula, drive/head
decode, the ATAPI path, `#481`'s control-register handling, the `wdc_altstatus` region.  2. THE DETECTOR:
`regress/wdc_lba_probe.py`, *"two legs in one invocation like `wdc_altoffset_probe.py`"*, its floor, accept side, anchor,
null medium and dead-run score as in section 7; its gate home *"beside"* `wdc_altoffset_probe`.  3. FILINGS / RECORDS: the
word-49 follow-up; an LBA48 note (out of scope); the witness term (`probe:` if the base leg is measured red BEFORE the
edit, else `detector:`); a CHANGELOG that must not claim guests now use LBA and must say word 49 is unchanged.

**3.2 The research's fix** is B's recommendation 1 (1.5): decode bit 6; compute
`((head&0xf)<<24)|(cyl_hi<<16)|(cyl_lo<<8)|sector` at both sites; keep the SDH readback byte-exact; keep word 49 = 0.

**3.3 The adjudication** is `ADJ_RULINGS.md` B and D (1.3): file as latent; decide word 49 FIRST; do not port the patch.

**3.4 The FreeBSD / DragonFly patch** (`distro_patches/freebsd_ports/files/patch-src_devices_dev__wdc.c`, whole file,
VERBATIM; the DragonFly DPorts copy is byte-identical, `cmp` at drafting).  Its hunk offsets (274, 320) are upstream 0.7.0's
line numbers, not this fork's:
*`regress/artifacts/research_20261022/distro_patches/freebsd_ports/files/patch-src_devices_dev__wdc.c` at HEAD, lines 1-16:*
~~~~
 1| --- src/devices/dev_wdc.c.orig	2021-04-22 18:04:20 UTC
 2| +++ src/devices/dev_wdc.c
 3| @@ -274,12 +274,12 @@ void wdc__read(struct cpu *cpu, struct wdc_data *d)
 4|  	    + (int64_t)d->head * d->sectors_per_track[d->drive] +
 5|  	    (int64_t)d->heads[d->drive] * d->sectors_per_track[d->drive] * cyl);
 6|  
 7| -#if 0
 8| +#if 1
 9|  	/*  LBA:  */
10|  	if (d->lba)
11|  		offset = 512 * (((d->head & 0xf) << 24) + (cyl << 8)
12|  		    + d->sector);
13| -	printf("WDC read from offset %lli\n", (long long)offset);
14| +	debug("WDC read from offset %lli\n", (long long)offset);
15|  #endif
16|  
~~~~

*(Lines 17-30 are the `wdc__write()` hunk: the same two changes, `#if 0` to `#if 1` and `printf` to `debug`.)*

**3.5 Where the sources disagree -- D1-D9** (each with the premise that settles it or the question that asks it):

* **D1 -- which bit carries the LBA flag.**  The patch keys on the existing `d->lba` (bit 5, S1); B, the ruling and the
  main loop decode bit 6.  NetBSD's CHS select 0xa0 has bit 5 set (S13), so the patch would send every NetBSD CHS request
  down the LBA formula.  Settled against the patch (S1, S12, S13).
* **D2 -- the arithmetic.**  The `#if 0` text, the patch and the main loop write `512 * (((head & 0xf) << 24) + (cyl << 8)
  + sector)`; B the same value with `|`.  All operands are `int`, so the product overflows once the sum reaches 2^22 (S6) --
  a 2 GiB disk.  **None of the four sources names a 64-bit product** (P8, V15).
* **D3 -- the `printf`.**  The patch makes it `debug()`; B and the main loop are silent.  Enabled verbatim it writes to the
  host's stdout on every media command (Q1(c)).
* **D4 -- word 49.**  The ruling adopts Grok's "latent; decide word 49 first" over Astra's present-tense reading; B keeps 49 =
  0 as a separate decision; the main loop keeps it 0 and files the advertisement with "the five-rig boot battery" as its
  gate (P3-P6, Q3(a)).
* **D5 -- how the read-back stays byte-exact.**  Required by B and the main loop, specified by neither: with `lba` from bit
  6 and `sectorsize` still on bits 7-6, bit 6 is held twice and bit 5 by nothing (S1, S4; Q1(b)).
* **D6 -- the gate home.**  The main loop: put the probe beside `wdc_altoffset_probe.py` in the gates.  That probe is in NO
  gate, exempt as a two-leg differential -- the open debt `wdcaltoffleg` (S16, P7).
* **D7 -- the follow-up's gate.**  The main loop: "the five-rig boot battery".  One battery rig reaches `dev_wdc.c`, with an
  all-zero disk behind an overlay (S18, P5, P6).
* **D8 -- `lba 0`'s HEAD want.**  The witness: "NOT tag 0 (record the words seen)".  Derivable: offset -512, answered with
  zeros (S8); measured `0x00000000` (P11, N8).
* **D9 -- bits 7 and 5.**  B: *"obsolete and always written as 1"*; ATA-2: *"Bit 7 is reserved"*, *"Bit 5 is reserved"*
  (S12, P1).

---

## 4. Section C0 -- has this round already shipped?  NO.

`git log -1 -- src/devices/dev_wdc.c` is `e16a8b7c` (`#533 landiskaux`, 2026-09-18); `grep wdclbaaddr CHANGELOG.md` at HEAD
finds nothing; at 16:47 neither `regress/wdc_lba_probe.py` nor `regress/artifacts/wdclbaaddr/` existed, and by 17:07 both
did -- the witness instrument, written for this round and run at 17:03 (section 2).  `dev_wdc.c` is md5
`714071619d8f98e85fe48ae566139345` at HEAD, in the working tree and in `est/`.  The FULL form carries the commands and their
output VERBATIM.

---
## 5. SETTLED PREMISES -- re-inlined so nobody spends an answer re-deriving them

Settled by THIS drafting pass (each re-read at HEAD `cc1f69cc` in this scope, line cited; outputs in `C0_OUTPUT.txt`), by
the measured witness (section 2) and by the primary sources on disk (section 9).  Premises and warrants, not derivations;
section 8 carries the code.  This is the first brief of this campaign: nothing is carried from an earlier pass.

* **S1 -- the SDH arm** (`dev_wdc.c` 2006-2022).  Write: `sectorsize = (idata >> 6) & 3`, `lba = (idata >> 5) & 1`,
  `drive = (idata >> 4) & 1`, `head = idata & 0xf`.  Read: `(sectorsize << 6) + (lba << 5) + (drive << 4) + head`.  The
  four fields partition the byte, so the read-back is byte-exact today (measured: 0xe5 and 0xb3).
* **S2 -- the register value.**  For every register but data, `idata = data[0]` (1179-1191): 0..255.  A non-8-bit write is
  announced once and still takes `data[0]`.
* **S3 -- the writers.**  `sector`, `cyl_lo`, `cyl_hi`, `seccnt`, `sectorsize`, `lba`, `drive`, `head` are assigned ONLY in
  their register write arms (census: 1951, 1961, 1981, 2001, 2014-2017; no reset or command path assigns them).  So
  `head` is 0..15, `drive` 0..1, and `sector`, `cyl_lo`, `cyl_hi` 0..255.
* **S4 -- the readers.**  `d->lba` is read at 472 and 564 (both inside `#if 0`) and in the SDH arm (2008, 2012, 2020);
  `d->sectorsize` only in the SDH arm (2008, 2012, 2020; written at 2014).  No other file in `src/` names either:
  `struct wdc_data` is opaque outside `dev_wdc.c` (`src/include/wdc.h` 35; `bus_pci.c` only calls `wdc_set_io_enabled()`).
  `regress/diff_wdc_identify.c` `#include`s `dev_wdc.c` and pokes `d.lba = 1` in one alt-ctrl fixture (5293) that issues
  no READ or WRITE.
* **S5 -- the two media sites** compute `offset = 512 * (d->sector - 1 + (int64_t)d->head * spt + (int64_t)heads * spt *
  cyl)`, `cyl = d->cyl_hi * 256 + d->cyl_lo` (464-468, 557-561), in 64-bit arithmetic.  Each has ONE caller, in
  `wdc_command()`: the `WDCC_READ`/`WDCC_READMULTI` arm (967-974) and the `WDCC_WRITE`/`WDCC_WRITEMULTI` arm (976-983).
  Neither offset expression reads `cur_command`.
* **S6 -- the disabled formula** (472-474, 564-566): `offset = 512 * (((d->head & 0xf) << 24) + (cyl << 8) + d->sector)`.
  Every operand is `int`, so the product is formed in `int` and exceeds `INT_MAX` -- undefined behaviour -- once the sum
  reaches 2^22 = 4,194,304, a 2 GiB disk.  `build/Makefile` 9 compiles with `-O3` and no `-fwrapv`.  Each block also holds a
  `printf` (475, 567).
* **S7 -- the enclosing control flow.**  `wdc__read()`: a chunk loop of at most 64 sectors; the ring-room guard (514-528)
  `break`s out; `d->int_assert = 1;` (548) runs on every path; `diskimage_access()`'s return is discarded (531-533,
  538-539).  `wdc__write()` only records `write_in_progress`, `write_count`, `write_offset` (570-572); the data-port drain
  (1846-1880) later writes at `d->write_offset` and discards the return.  Both functions return `void`.
* **S8 -- out-of-range offsets** (`diskimage.c` 1531-1601, 1671-1698).  `diskimage_access()` subtracts
  `override_base_offset` (0 unless set); the internal function refuses `offset < 0` or an access past its limit -- a READ
  gets its buffer ZERO-FILLED, a WRITE is not performed (both return 0).  The read limit is the ADVERTISED capacity, the
  write limit the file size; reads past the file but inside the capacity are zero-filled too.  So a CHS request for
  sector 0 at head 0, cylinder 0 (offset -512) is served 512 zero bytes.
* **S9 -- the geometry** (`diskimage.c` 268-307; `dev_wdc.c` 2124-2130).  A non-floppy image without a `-d gH;S` override
  gets heads 16, sectors-per-track 63, cylinders = ceil(size / 516,096), capacity rounded up to whole cylinders.  The
  4,096-sector witness file: C 5, capacity 5,040 (its transcript: *"2 MB (5040 512-byte blocks)"*); the 64 MiB scratch
  image: C 131, capacity 132,048.  IDENTIFY words 1/3/6 report C/H/S, words 57-58 and 60-61 the capacity (432-442); IDP
  (0x91) is a TODO that changes nothing (985-989).
* **S10 -- IDENTIFY word 49** is 0 (374-377), under *"(0x200 = LBA, 0x100 = DMA support.)"*; word 53 is 0x0002, word 47
  0x8080.  Words are stored *"High byte, then low"* (328) and sent low byte first (1016-1020); a 16-bit read on a
  little-endian guest composes `byte0 | byte1 << 8` (1200-1202).
* **S11 -- `wdcreg.h`**: `wd_sector 3`, `wd_cyl_lo 4`, `wd_cyl_hi 5`, `wd_sdh 6`; `WDSD_IBM 0xa0` *"forced to 512 byte
  sector, ecc"*, `WDSD_CHS 0x00`, `WDSD_LBA 0x40`; `WDCC_READ 0x20`, `WDCC_WRITE 0x30`, `WDCC_READMULTI 0xc4`,
  `WDCC_WRITEMULTI 0xc5`, `WDCC_IDENTIFY 0xec`, `WDCC_READ_EXT 0x24`, `WDCC_WRITE_EXT 0x34`; `WDCE_ABRT 0x04`,
  `WDCE_IDNF 0x10`.  The 48-bit commands land in `wdc_command()`'s `default:` arm (1114-1164): ABRT, an interrupt, one
  announcement per device.
* **S12 -- ATA-2** (9.1): Device/Head is *"r L r DEV HS3 HS2 HS1 HS0"*, *"Bit 7 is reserved"*, *"Bit 5 is reserved"*; L
  selects CHS (0) or LBA (1); in LBA mode the head field is LBA 27-24, cylinder high 23-16, cylinder low 15-8, sector 7-0;
  *"LBA = ( (cylinder * heads_per_cylinder + heads ) * sectors_per_track ) + sector - 1"*; *"A host shall not attempt to use
  LBA addressing unless the device indicates the mode is supported."*; word 49 bit 9 *"is used to indicate if the device
  supports LBA mode addressing. If this bit is set, words 60-61 shall be valid."*; words 60-61: *"If the device does not
  support LBA mode, these words shall be set to 0."*; CHS sectors are numbered from 1 (at most 255), heads 0..15.
* **S13 -- NetBSD** (9.2): `wdccommand()` writes `WDSD_IBM | (drive << 4) | head`; an LBA request sets
  `head = (blkno >> 24) & 0x0f; head |= WDSD_LBA;`, a CHS request `head |= WDSD_CHS;` -- selects 0xa0|head (CHS) and
  0xe0|head (LBA).  `wd.c` 394-395 sets `WDF_LBA` only if word 49 carries `WDC_CAP_LBA`; the "ATA-4 requires LBA" path is
  `#if 0`.
* **S14 -- the patch** (3.4) flips both `#if 0` to `#if 1` and the `printf` to `debug()`; it changes neither the decode nor
  the arithmetic.  FreeBSD and DragonFly ship it byte-identically.
* **S15 -- the witness** (section 2): LBA 70 was served sector 69; LBA 256 sector 1007 (= H*S - 1); LBA 0 zeros; a WRITE to
  LBA 70 landed at sector 69 and left 70 intact; CHS reads served 0, 1 and 63 (= S); IDENTIFY gave (16, 63) and word 49 =
  0; SDH read back 0xe5 and 0xb3.
* **S16 -- the gate homes** (at HEAD).  Gate 10 (`gate_sh_rounding.sh`; `PMAX=${PMAX:-$ROOT/build/gxemul}` 33, `need_exec
  "$PMAX"` 37) runs `wdc_flood_probe.py` (1397), `wdc_altdigin_probe.py "$PMAX" GATE ...` (1484; denominator pinned to the
  literal 22 by EQUALITY, 1522-1523) and `landisk_aux_probe.py` (1696-1701).  **`wdc_altoffset_probe.py` runs in no
  gate**: `check_probe_wiring.py` exempts it until 2026-11-05, *"two-leg differential; wants a single-leg mode before gate
  10 can assert anything"* (3301-3303), noting *"four of its 18 rows want the committed build's defect, which the gate's one
  binary cannot supply"* (3299-3300).  `need_exec` (`lib.sh` 153-157) SKIPs the WHOLE gate on a missing or non-executable
  binary.
* **S17 -- the word-49 pin.**  Gate 2 (`gate_offline.sh` 1495-1511) compiles `regress/diff_wdc_identify.c` -- which
  `#include "../src/devices/dev_wdc.c"` (208) -- against the working tree.  Its `row_no_lba_claim()` (5606-5637) fails
  unless word 49 is `00 00`, prints *"(0x200 = LBA, 0x100 = DMA -- neither is implemented)"*, and says *"If LBA is ever
  implemented, this row must be re-authored in the SAME change -- that is the point of pinning it."*  The gate pins the row
  by NAME (`no unimplemented capability claimed`, 1895-1896); its comment (1890) reads *"word 49 <- 1 char: advertise LBA
  that is #if 0'd out"*; rows: `check_min ... 42` (1508-1509).
* **S18 -- which battery rigs reach `dev_wdc.c`.**  PMAX, ARC, SGI, LUNA88K and MVME88K disks are SCSI (`diskimage.c`
  1701-1711), so the pmax, arc and luna88k rigs never do.  Only landisk does, and only when the OPTIONAL
  `_images/wdc-scratch-64m.img` exists -- *"64 MiB of zeros"* (`images.md` 139), attached `-d iR:` through a pid-unique
  overlay (`drive_guest.py` 273-285).  Its disked boot issues *"3x 0xEC IDENTIFY, 3x 0x20 READ, 2x 0xC6 SETMULTI, 2x 0x91
  IDP, 2x 0x10 RECAL, 1x 0xF5 SEC_FREEZE_LOCK, 1x 0xC4 READMULTI"* and no WRITE (`drive_guest.py` 89-92, 97-99).  Without
  the image, *"`dev_wdc.c` has **zero rig coverage in the entire battery**"* (`images.md` 146).
* **S19 -- the committed wdc probes' SDH bytes**: 0xa0 (`wdc_altoffset_probe.py` 270, `wdc_altoffset_sig_probe.py` 93,
  `wdc_altdigin_probe.py` 116, 234) and 0xb0 (`wdc_altdigin_probe.py` 171, 230) -- bit 6 clear, so they stay CHS under a
  bit-6 decode.
* **S20 -- no coincidences** (C0, python): over every head 0..15 and cylinder 0..65535 the CHS index
  `sector - 1 + 63*head + 1008*cyl` never equals the LBA28 value `(head << 24) + (cyl << 8) + sector` (the sector term
  cancels; 0 pairs) -- so on 16/63 the fix changes the served sector of EVERY LBA-mode media command.
* **S21 -- the vehicle.**  `evbmips -e malta` is little-endian (`machine_evbmips.c` 57-62); its PIIX4 IDE function adds
  `wdc addr=...` whenever an IDE image is attached (`machine_evbmips.c` 100; `bus_pci.c` 505-507).
* **S22 -- the word-49 records** (CHANGELOG, VERBATIM, joined across line breaks).  `#405` (31191-31196): *"**Not touched,
  deliberately: word 49 (LBA support) stays zero.** The LBA offset arms in `wdc__read`/`wdc__write` are `#if 0`, and
  `d->lba` is parsed in the `wd_sdh` case and then never reaches an offset computation. Advertising LBA while still
  computing CHS offsets would send a guest's requests to the wrong place — the zero may be accidentally load-bearing.
  **#407 gated it**: a one-character edit setting word 49 to `2` passed all ten of this round's rows, so the deliberate zero
  is now asserted."*  `#409` (30930-30934): *"#407 called `[2*49+1] = 2` an "advertising LBA" mutant. That is the **low**
  byte, which is vendor-specific; LBA is `0x200`, the **high** byte. The in-tree OpenBSD guest settles it — its `wdc.c`
  takes capabilities from `tb[49] >> 8` and puts the low byte in `wdp_vendor3`, which is never read."*
* **S23 -- precedents.**  `#481` (CHANGELOG 17844-17856): this file's Device Control arm tested `WDCTL_4BIT` (0x08, *"use
  four head bits (wd1003)"*) where the reset bit is `WDCTL_RST` (0x04) -- a wrong-bit decode in this file.  `#533`'s
  `landisk_aux_probe.py`: a SINGLE-LEG wdc detector wired into gate 10 in the same commit (`check_probe_wiring.py`
  643-654).
* **S24 -- the witness instrument** (frozen copy, 8.11): usage `<base_bin> <fix_bin or -> <outdir>` (68-73); leg `base`
  always runs and is judged against the HEAD column, leg `fix` only when a second binary is given (616-618); exit 0 only
  when every leg passes (633); an unprinted register is `None` (450-453); a want derived from IDENTIFY is `None` when H or S
  is (487, 504-505); `"eq"` rows compare `got == want` (540), so `None == None` passes; `neg appar` is built from constants
  (526) and always passes; `lba 0`'s HEAD mode `nehead` passes anything but tag 0 and fails `None` (536-539);
  `Emu.send()` writes to the pty with no `OSError` handling (349-359), while `drain()` and `close()` catch it.

---

## 6. PREMISES STATED AS QUESTIONS -- check these; ratification is not wanted

* **P1 -- bits 7 and 5.**  B: *"obsolete and always written as 1"*; ATA-2: reserved (S12); drivers write 1 (S11, S13).
  Does any decision here depend on which?  (The read-back is their only consumer, S4.)
* **P2 -- what `sectorsize` is.**  The main loop: *"the pre-ATA WD1003 reading of bits 7-6"*.  The fork's header calls 0xa0
  *"forced to 512 byte sector, ecc"*; if that means bit 7 = ECC and a size code in bits 6-5 (01 = 512), a bits-7-6 field
  matches neither WD1003 nor ATA.  No WD1003 document is on disk.  Does the read-back design need the field's meaning?
* **P3 -- latent.**  With word 49 = 0, ATA-2 forbids a host from issuing LBA (S12) and NetBSD obeys (S13); only a host that
  ignores word 49 reaches the defect -- FreeBSD 10+ per a 2013 commit message, UNVERIFIED here.  Does "latent" change
  WHETHER to fix, or only WHEN?
* **P4 -- honouring LBA without advertising it.**  Today: no LBA support, words 60-61 nonzero (against "shall be set to
  0").  After the fix: LBA supported, bit 9 clear (against "is used to indicate").  Is that interim state acceptable, and
  which comment or record must say so?
* **P5 -- "five rigs".**  The main loop: advertising would switch "every rig's guest" to LBA, "a guest-visible behaviour
  change on five rigs".  S18: ONE battery rig reaches `dev_wdc.c`, with an all-zero disk behind an overlay.  Is there any
  rig, in the battery or outside it, on which advertising changes OBSERVABLE content?
* **P6 -- the follow-up's gate.**  Can "the five-rig boot battery" observe a word-49 change (S18)?  If not, what gate could
  license advertising (R13: a measured delta or a transferred warrant)?
* **P7 -- shape and home.**  The witness copies `wdc_altoffset_probe.py`'s two-leg shape, whose wiring is the open debt
  `wdcaltoffleg` (S16): its base leg wants the committed defect, which gate 10's single binary cannot supply.  Should the
  shipped detector take `wdc_altdigin_probe.py`'s single-leg form (the FIX column against `$PMAX`, a result line, a
  CONTROL line, the denominator pinned by equality) and keep both columns for the witness and the variant table?
* **P8 -- the `int` product** (S6, D2).  Is 64-bit widening part of "enable the LBA28 formula" in THIS round (it is
  `arcpartlba`'s class, 1.6), and can any row observe the unwidened form, whose behaviour past 2^22 is undefined (V15)?
* **P9 -- `& 0xf`.**  The main loop: *"`& 0xf` dropped (needs LBA >= 2^24 -- disclose)"*.  S3: `head` is masked to 0..15 at
  its only writer, so the variant is EQUIVALENT in every reachable state.  Agree?
* **P10 -- the witness's CHS read-backs** use sectors 71 and 70 with S = 63 -- addresses ATA-2 does not define (S12) --
  relying on unvalidated arithmetic.  Use the valid triples (head 1, sector 8) and (head 1, sector 7) instead (N7)?
* **P11 -- `lba 0`'s HEAD want** accepts anything but tag 0, recorded rather than predicted (S24).  S8 predicts zeros and
  zeros were measured.  Make the want that literal (N8)?
* **P12 -- the dead run** (R2, R22).  From the source (S24): if every session dies and the driver survives it, `chs h1`
  passes in both columns (want and got both `None`), `lba 256` in the HEAD column, and `neg appar` always -- 3/19 HEAD,
  2/19 FIX, CONTROL=FAIL, exit 1.  But a medium that exits at once may instead end the run in an uncaught `OSError` from
  `Emu.send()`, with no sentinel.  Which outcome, which gate pin reds on it, and should a `None` want fail its row?
* **P13 -- the read-back rows** 0xe5 and 0xb3 both have bits 7 and 5 set: neither tells byte-exact from "bits 7 and 5
  forced to 1".  Is a row with both clear owed (N4, 0x4c)?
* **P14 -- a bare 0x40 select.**  NetBSD writes 0xe0 (S13); which drivers write 0x40 is not checkable here.  Is the row owed
  anyway, because the added decode depends on bit 6 alone (N3)?
* **P15 -- the witness record.**  (a) `WITNESS.md` names the SDH read-back a device signature -- RAM would mimic it; (b) it
  cites *"the ORDER the oracle-correction rule demands"* where the governing rule is the ladder's clause (i) (R17); (c) the
  binary is fingerprinted by one source file (2.4).  Do any of these change the ledger term (Q3(c))?
* **P16 -- what a 4,096-sector image cannot see.**  Any request with `cyl_hi != 0` lands past the capacity (5,040) under
  BOTH readings, so both are zero-filled; likewise a head shift `<< k` for any k >= 12 versus `<< 24` (2^12 + 5 is already
  past the file, S8).  Pinning `cyl_hi` needs over 65,536 sectors -- where the 16-bit tag aliases, `TAG(65536) == TAG(0)`
  (C0) -- and pinning `<< 24` over 2^24 sectors (8 GiB; a sparse file).  Enlarge and widen the tag, or disclose (R6, R7)?
* **P17 -- a recorded alt-ctrl variant changes meaning.**  `wdcaltfixture`'s exemplar is `&& !d->lba`, and
  `OUTSTANDING_BUGS.md` 13001 says it *"defeats the abort on **every LBA-mode driver**"*.  At HEAD `d->lba` is bit 5 --
  1 for 0xa0 (CHS) and 0xe0 (LBA) alike; after the fix, 1 for LBA selects only.  The record becomes accurate only after
  this round.  Does any recorded score or committed row depend on the old meaning (S4, S19)?
* **P18 -- the option set** (R12).  For an LBA-mode media command on a device that does not advertise LBA: (a) honour it --
  member 7 IMPLEMENT, or 4 ACCEPT in that the right value is already computed in compiled-out code; (b) refuse it with ABRT,
  a FAULT-like answer through the error register (the in-file idiom: the no-disk arm, 947-954); (c) keep serving the CHS
  reading and document it; (d) honour and advertise.  Is a member missing?

---
## 7. The drafter's partition, cells, rows and variants -- as DATA: check them, do not ratify them

Values assume the witness image: 4,096 sectors in the file, H = 16, S = 63, capacity 5,040 (S9), sector `n` tagged
`TAG(n) = (~n & 0xffff) << 16 | n` (S15).  `R` = the read site (`wdc__read()`), `W` = the write site (`wdc__write()` plus the
drain), `L` = the decoded mode bit; HEAD = the committed build, FIX = the build after the proposed repair.

**7.1 The repair's input partition -- which inputs it changes the answer for** (Q1(a) checks it):

| input | HEAD | FIX | changed? |
|---|---|---|---|
| select bit 6 CLEAR (0x00-0x3f, 0x80-0xbf; e.g. 0xa0, 0xb0), any command | CHS formula | CHS formula | no |
| bit 6 SET (0x40-0x7f, 0xc0-0xff; e.g. 0xe0, 0x40), READ 0x20 / READMULTI 0xc4 | CHS index of the bytes | `(head << 24) + (cyl << 8) + sector` | YES, for every (head, cyl, sector) on 16/63 (S20) |
| bit 6 SET, WRITE 0x30 / WRITEMULTI 0xc5 | written at the CHS index | written at the LBA | YES |
| bit 6 SET, any other opcode (IDENTIFY, IDP, RECAL, SETMULTI, SET_FEATURES, security, DIAGNOSE, ATAPI, 48-bit, unknown) | no address computed | none | no (S5, S11) |
| bit 6 SET, LBA at or past the file's end (4,096 here) | (CHS reading) | zero-filled read; write past the file refused; the guest is not told (S8) | yes; no error is reported -- as for an out-of-range CHS request today |
| LBA >= 2^22 (a disk over 2 GiB) | (CHS reading) | right only if the product is 64-bit (S6) | depends on the repair (P8) |
| SDH read-back; drive bit 4; head nibble as a CHS head | as today | as today | must not change |

**7.2 Floor bookkeeping** (R1-R10, R14, R21, R22):

* **(a) pre-fix**: measured (section 2) -- the five symptom rows show the CHS reading on the committed build.
* **(b) verbatim reinstatement at EVERY fixed site**: the sites are (1) the decode (2015), (2) the read-site arm (470-476),
  (3) the write-site arm (562-568), (4) the read-back composition (2008-2009) if the repair changes it -- reinstated, they
  are V1, V14 (two halves) and V17, each predicted red by a witness row.
* **(c) null medium** (R2, R22): an ABSENT or NON-EMULATOR binary; gate 10's `need_exec` turns an absent one into a SKIP of
  the whole gate (S16), so the medium that exercises the probe is an executable that is not the emulator.  Predicted dead
  run: P12.  Record form: Q2(d).
* **(d) DEPENDS-ON** (R3-R5): (1) dominating predicates, to the function boundary -- at R and W only the new `if (d->lba)`;
  at the decode line the `io_enabled` test (1176), `case wd_sdh:` and the read/write split (2007), none changed by the fix;
  (2) swaps and added conjuncts from fields the guarded BODY reads -- `d->head`, `d->cyl_lo`, `d->cyl_hi` (via `cyl`),
  `d->sector`.  The body tests none of them, so no joint cells (R5) and an EMPTY body-induced partition for each (R6).
  Whether the single-axis cells C5-C11 are FLOOR or clause-(e) debt is Q2(a)'s question, not a settled premise.
* **GUARD vs BODY** (R10): the guard reads `d->lba` (written at 2015); the body reads `d->head` (same site, independent
  bit), `d->sector` (1961), `d->cyl_lo` (1981), `d->cyl_hi` (2001).  Disagreeing states (`lba = 1` with `head != 0`,
  `cyl_lo != 0`, `cyl_hi != 0` or `sector == 0`) are reachable by ordinary register writes.  SAMPLED: head {0}, cyl_lo
  {0, 1}, cyl_hi {0}, sector {0, 70} at R; head {0}, cyl {0}, sector {70} at W.
* **SIBLING PARITY**: R has three L=1 rows and three CHS rows; W has one L=1 row and no CHS row (C7, C9, C10).
* **CLAIM -> ROW**: the comments the repair adds (LBA served at the LBA; read-back byte-exact; word 49 stays 0) each owe a
  row (C2-C4/C8, C15-C17, C18).
* **(e)** the contract: 7.6.  **(f)** the anchor (R8): the sector tag names WHICH sector was served, through image content
  the decode does not produce; R8's check, adapted -- if every LBA moved by one sector, which row reds? -- all five `lba` rows.
* **R21 compare edges: N/A** (a bit test and a flag test; the disk-layer bounds are `#416`'s).  **R14: N/A** (no `exit(`
  deleted).

**7.3 The cells** (`W:` rowed by the witness; `OWED Nk` a proposed row; `(e)` disclosed; `IMAGE` not observable on a
4,096-sector image, P16):

| cell | what it is | status |
|---|---|---|
| C1 | R, L=0 (a CHS read stays CHS) | W: `chs s1`, `chs s2`, `chs h1` |
| C2 | R, L=1, sector != 0, cyl 0, head 0 | W: `lba 70` |
| C3 | R, L=1, sector 0, cyl_lo != 0 | W: `lba 256` |
| C4 | R, L=1, all zero (LBA 0) | W: `lba 0` |
| C5 | R, L=1, head != 0 | OWED N1 |
| C6 | R, L=1, cyl_hi != 0 | IMAGE |
| C7 | W, L=0 (a CHS write stays CHS) | OWED N6 |
| C8 | W, L=1, sector != 0, cyl 0, head 0 | W: `lba wr`, `lba wr2` |
| C9 | W, L=1, sector 0, cyl_lo != 0 | OWED N5 |
| C10 | W, L=1, head != 0 | OWED N2 |
| C11 | W, L=1, cyl_hi != 0 | IMAGE |
| C12 | decode: select 0xe0 (bits 7, 6, 5 set) | W: every `lba` row |
| C13 | decode: 0xa0 / 0xa1 (bit 6 clear, bits 7 and 5 set) | W: every `chs` row |
| C14 | decode: 0x40 (bit 6 set, bits 7 and 5 clear) | OWED N3 |
| C15 | read-back, bit 6 set | W: `sdh rb` (0xe5) |
| C16 | read-back, bit 6 clear, bit 5 set | W: `sdh rb2` (0xb3) |
| C17 | read-back, bits 7 and 5 clear | OWED N4 |
| C18 | IDENTIFY word 49 = 0 (the round's "unchanged" claim, at rung 3) | W: `id w49` |
| C19 | READMULTI / WRITEMULTI labels, seccnt > 1 | (e): neither enters the offset expression (S5) |
| C20 | big-endian guest (`-e maltabe`); drive 1 | (e): the arithmetic is byte-order-free (the tag read is not); drive 1 has no disk here and is refused first (947-954) |

**7.4 The rows I propose, as DATA** (Q2(c) corrects them).  Every want is a literal; "zeros" is `0x00000000`.  The CHS
triples are VALID for S = 63, cylinder 0: index 5 = (head 0, sector 6), 9 = (0, 10), 10 = (0, 11), 67 = (1, 5), 69 = (1, 7),
70 = (1, 8), 256 = (4, 5), 1007 = (15, 63) (C0 arithmetic).

| row | stimulus | HEAD (committed) | FIX | cell | detects |
|---|---|---|---|---|---|
| N1 `lba h1` | READ, select 0xe1, sector 5, cyl 0 -- in a session that also reads a tagged sector | TAG(67) `0xffbc0043` (CHS head 1, sector 5) | zeros (LBA 16,777,221 > 5,040) | C5 | V4r, V8, V15 if it wraps |
| N2 `lba h1 wr` | WRITE, select 0xe1, sector 5, payload `0x6666`, `0x9999`; read back index 67 (0xa1, s5) and 5 (0xa0, s6) | 67: `0x99996666`; 5: TAG(5) `0xfffa0005` | 67: TAG(67); 5: TAG(5) (write refused, S8) | C10 | V4w, V8 (write) |
| N3 `lba 40` | READ, select 0x40, sector 70, cyl 0 | TAG(69) `0xffba0045` | TAG(70) `0xffb90046` | C14 | V2, V3 |
| N4 `sdh rb3` | write 0x4c to SDH, read it back | `0x4c` | `0x4c` | C17 | V16, V17 |
| N5 `lba wr c1` | WRITE, select 0xe0, sector 0, cyl_lo 1, payload `0x5555`, `0xaaaa`; read back 256 (0xa4, s5) and 1007 (0xaf, s63) | 256: TAG(256) `0xfeff0100`; 1007: `0xaaaa5555` | 256: `0xaaaa5555`; 1007: TAG(1007) `0xfc1003ef` | C9 | V5w, V6w, V11 (write) |
| N6 `chs wr` | WRITE, select 0xa0, sector 10, cyl 0, payload `0x3333`, `0xcccc`; read back 9 (0xa0, s10) and 10 (0xa0, s11) | 9: `0xcccc3333`; 10: TAG(10) `0xfff5000a` | the same | C7 | V13w, V1 (write) |
| N7 | `lba wr` / `lba wr2` read back through the VALID triples (0xa1, s8) and (0xa1, s7), not (0xa0, s71) and (0xa0, s70) | wants unchanged | wants unchanged | C8 | (P10) |
| N8 | `lba 0`'s HEAD want becomes the literal zeros | zeros | TAG(0) `0xffff0000` | C4 | (P11) |
| N9 | only if P16 enlarges the image past 65,536 sectors AND the tag carries `n >> 16`: READ, select 0xe0, sector 0, cyl_lo 0, cyl_hi 1 | zeros (CHS cylinder 256 is past the capacity) | the tag of sector 65,536 | C6 | V7r, V10 |

**7.5 The variants, classified** (Q2(b) checks every line).  "W" = witness rows predicted red, "N" = proposed rows; "none"
is a prediction to be measured, not a measurement.

| # | variant | predicted red | drafter's class |
|---|---|---|---|
| V1 | decode back on bit 5 -- clause (b), site 1 | W: `chs s1` (TAG(1)), `chs s2` (TAG(2)), `chs h1` (zeros); N6 | floor (b) |
| V2 | decode on bit 7 | W: every `chs` row; N3 | detected |
| V3 | decode requires bit 6 AND bit 5 | W: none; N3 | floor (d): owed N3 |
| V4r / V4w | `if (d->lba && d->head == 0)` at R / at W | W: none; N1 / N2 | (d) or (e): Q2(a) |
| V5r / V5w | `if (d->lba && cyl == 0)` at R / at W | R: W `lba 256`; W-site: N5 | detected / owed N5 |
| V6r / V6w | `if (d->lba && d->sector != 0)` at R / at W | R: W `lba 256`, `lba 0`; W-site: N5 | detected / owed N5 |
| V7 | `if (d->lba && d->cyl_hi == 0)`, either site | none on this image (both readings past the capacity) | IMAGE (P16) |
| V8 | LBA formula without the head term | W: none; N1 (TAG(5)), N2 (index 5 gets the payload) | owed N1, N2 |
| V9 | head shifted `<< 20` -- any `<< k` with 2^k + 5 >= 4,096, i.e. k >= 12 (reads past the file are zeros, S8) | none on this image | IMAGE (P16) |
| V10 | `cyl_hi` dropped (`d->cyl_lo << 8`) | none on this image | IMAGE (P16, N9) |
| V11 | `+ d->sector - 1` in the LBA arm | R: W `lba 70` (TAG(69)), `lba 256` (TAG(255)), `lba 0` (zeros); W-site: W `lba wr`, `lba wr2`; N5 | detected |
| V12 | `& 0xf` removed | none, in any state | EQUIVALENT (S3, P9) |
| V13r / V13w | LBA formula whatever L is, at R / at W | R: W every `chs` row; W-site: W none, N6 | detected / owed N6 |
| V14 | one site enabled, the other left `#if 0` -- clause (b), sites 2 and 3 | read-only: W `lba wr`, `lba wr2`; write-only: W `lba 70`, `lba 256`, `lba 0` | floor (b) |
| V15 | LBA product left in `int` | W: none (every LBA < 2^22); N1 only if the build wraps (512 * 16,777,221 mod 2^32 = 2,560, i.e. LBA 5); a compiler-widened evaluation serves zeros like FIX | undefined behaviour: MEASURE at `-O3` (P8) |
| V16 | read-back forces bits 7 and 5 to 1 | W: none; N4 (`0xec`) | owed N4 |
| V17 | read-back left as `(sectorsize << 6) + (lba << 5) + ...` with `lba` from bit 6 -- clause (b), site 4 | W: `sdh rb2` (0xb3 reads 0x93); N4 (`0x6c`); `sdh rb` still passes | floor (b) |
| V18 | read-back drops bit 6 | W: `sdh rb` (0xe5 reads 0xa5) | detected |
| V19 | `if (d->lba && d->drive == 0)` | none: drive 1 has no disk here and is refused first (C20); `drive` is not a field the LBA body reads | outside R4: (e) |
| V20 | `write_offset` captured before the LBA arm runs (statement order in `wdc__write`) | W: `lba wr`, `lba wr2` | detected |

**7.6 The contract the probe header would carry** (clause (e), R7) -- the drafter's text, for Q2(e) to correct:

    CATCHES: the SDH decode moved off bit 6 or qualified by bits 7/5 (V1-V3); the LBA arm disabled, unconditional, or
      conditioned on head, cyl_lo or sector at EITHER site (V4-V6, V13, V14); the head term or the sector offset wrong
      (V8, V11); the read-back losing any bit or forcing bits 7/5 (V16-V18); word 49 advertised (C18).
    BLIND, BY CONSTRUCTION: cyl_hi and the head shift amount (V7, V9, V10) -- both readings of such a request fall past a
      4,096-sector image; the 64-bit product (V15) -- undefined behaviour, measured once and recorded; the MULTI labels
      and seccnt > 1 (C19); big-endian guests and drive 1 (C20); the 48-bit commands (no arm); the debug text.

**7.7 Shape, home and wiring** (the drafter's proposal; Q3(b) decides): ONE file, `regress/wdc_lba_probe.py`, with a
single-leg mode asserting the FIX column against one binary (a result line and a CONTROL line), wired into gate 10 beside
`wdc_altdigin_probe.py` with its denominator pinned by EQUALITY (S16); the two-column mode kept for the witness record and
the variant table; a `CLASS_DETECTOR` line in `check_probe_wiring.py`, plus a line for the frozen witness copy (S23).

---
## 8. SOURCE, INLINED -- line numbers as read at HEAD `cc1f69cc` (CONDENSED: cut to what the premises use; `[... lines a-b omitted ...]` marks every cut)

*(8.1 the struct fields and 8.2 the IDENTIFY words are not inlined in this form; S3, S9 and S10 quote what the questions
use.)*

**8.3 `wdc__read()`, WHOLE -- an edit site; every exit path and the common tail (S5-S7, R11):**
*`src/devices/dev_wdc.c` at HEAD, lines 456-483, 514-549:*
~~~~
456| /*
457|  *  wdc__read():
458|  */
459| void wdc__read(struct cpu *cpu, struct wdc_data *d)
460| {
461| #define MAX_SECTORS_PER_CHUNK	64
462| 	const int max_sectors_per_chunk = MAX_SECTORS_PER_CHUNK;
463| 	unsigned char buf[512 * MAX_SECTORS_PER_CHUNK];
464| 	int i, cyl = d->cyl_hi * 256+ d->cyl_lo;
465| 	int count = d->seccnt? d->seccnt : 256;
466| 	uint64_t offset = 512 * (d->sector - 1
467| 	    + (int64_t)d->head * d->sectors_per_track[d->drive] +
468| 	    (int64_t)d->heads[d->drive] * d->sectors_per_track[d->drive] * cyl);
469| 
470| #if 0
471| 	/*  LBA:  */
472| 	if (d->lba)
473| 		offset = 512 * (((d->head & 0xf) << 24) + (cyl << 8)
474| 		    + d->sector);
475| 	printf("WDC read from offset %lli\n", (long long)offset);
476| #endif
477| 
478| 	while (count > 0) {
479| 		int to_read = count > max_sectors_per_chunk?
480| 		    max_sectors_per_chunk : count;
481| 
482| 		/*  TODO: result code from the read?  */
483| 
     [... lines 484-513 omitted ...]
514| 		if (512 * to_read > (d->inbuf_tail - d->inbuf_head - 1 +
515| 		    WDC_INBUF_SIZE) % WDC_INBUF_SIZE) {
516| 			if (!d->warned_inbuf_overrun) {
517| 				d->warned_inbuf_overrun = 1;
518| 				/*  #484: names THIS function, not the producer.  The
519| 				    shared latch already removes the only other way to
520| 				    tell the two sites apart, so a message pointing at
521| 				    a guard that did not fire is a wrong record in
522| 				    product output.  */
523| 				fatal("[ wdc__read(): WARNING! wdc inbuf would"
524| 				    " overrun; refill refused. Increase"
525| 				    " WDC_MAX_SECTORS. ]\n");
526| 			}
527| 			break;
528| 		}
529| 
530| 		if (d->inbuf_head + 512 * to_read <= WDC_INBUF_SIZE) {
531| 			diskimage_access(cpu->machine, d->drive + d->base_drive,
532| 			    DISKIMAGE_IDE, 0, offset,
533| 			    d->inbuf + d->inbuf_head, 512 * to_read);
534| 			d->inbuf_head += 512 * to_read;
535| 			if (d->inbuf_head == WDC_INBUF_SIZE)
536| 				d->inbuf_head = 0;
537| 		} else {
538| 			diskimage_access(cpu->machine, d->drive + d->base_drive,
539| 			    DISKIMAGE_IDE, 0, offset, buf, 512 * to_read);
540| 			for (i=0; i<512 * to_read; i++)
541| 				wdc_addtoinbuf(d, buf[i]);
542| 		}
543| 
544| 		offset += 512 * to_read;
545| 		count -= to_read;
546| 	}
547| 
548| 	d->int_assert = 1;
549| }
~~~~

*(Lines 484-513 are one comment, the `#484` occupancy-bound note; no statement is omitted.)*

**8.4 `wdc__write()`, WHOLE -- the other edit site (S5-S7):**
*`src/devices/dev_wdc.c` at HEAD, lines 552-575:*
~~~~
552| /*
553|  *  wdc__write():
554|  */
555| void wdc__write(struct cpu *cpu, struct wdc_data *d)
556| {
557| 	int cyl = d->cyl_hi * 256+ d->cyl_lo;
558| 	int count = d->seccnt? d->seccnt : 256;
559| 	uint64_t offset = 512 * (d->sector - 1
560| 	    + (int64_t)d->head * d->sectors_per_track[d->drive] +
561| 	    (int64_t)d->heads[d->drive] * d->sectors_per_track[d->drive] * cyl);
562| #if 0
563| 	/*  LBA:  */
564| 	if (d->lba)
565| 		offset = 512 * (((d->head & 0xf) << 24) +
566| 		    (cyl << 8) + d->sector);
567| 	printf("WDC write to offset %lli\n", (long long)offset);
568| #endif
569| 
570| 	d->write_in_progress = d->cur_command;
571| 	d->write_count = count;
572| 	d->write_offset = offset;
573| 
574| 	/*  TODO: result code?  */
575| }
~~~~

**8.6 `DEVICE_ACCESS(wdc)` -- the register-value prologue, the SDH arm WITH its neighbours, and the common tail (S1-S3, R11):**
*`src/devices/dev_wdc.c` at HEAD, lines 1179-1191, 2006-2022, 2047-2054, 2060-2070:*
~~~~
1179| 	if (writeflag == MEM_WRITE) {
1180| 		if (relative_addr == wd_data)
1181| 			idata = memory_readmax64(cpu, data, len);
1182| 		else {
1183| 			/*  #464: latch the announcement; `idata = data[0]`
1184| 			    is the repair and stays outside the guard.  */
1185| 			if (len != 1 && !d->warned_nonbyte_write) {
1186| 				d->warned_nonbyte_write = 1;
1187| 				fatal("[ wdc: WARNING! non-8-bit access on "
1188| 				    "WRITE! ]\n");
1189| 			}
1190| 			idata = data[0];
1191| 		}
      [... lines 1192-2005 omitted ...]
2006| 	case wd_sdh:	/*  6: sectorsize/drive/head  */
2007| 		if (writeflag==MEM_READ) {
2008| 			odata = (d->sectorsize << 6) + (d->lba << 5) +
2009| 			    (d->drive << 4) + (d->head);
2010| 			debug("[ wdc: read from SDH: 0x%02x (sectorsize %i,"
2011| 			    " lba=%i, drive %i, head %i) ]\n", (int)odata,
2012| 			    d->sectorsize, d->lba, d->drive, d->head);
2013| 		} else {
2014| 			d->sectorsize = (idata >> 6) & 3;
2015| 			d->lba   = (idata >> 5) & 1;
2016| 			d->drive = (idata >> 4) & 1;
2017| 			d->head  = idata & 0xf;
2018| 			debug("[ wdc: write to SDH: 0x%02x (sectorsize %i,"
2019| 			    " lba=%i, drive %i, head %i) ]\n", (int)idata,
2020| 			    d->sectorsize, d->lba, d->drive, d->head);
2021| 		}
2022| 		break;
      [... lines 2023-2046 omitted ...]
2047| 	/*  Assert interrupt, if necessary:  */
2048| 	dev_wdc_tick(cpu, extra);
2049| 
2050| ret:
2051| 	if (writeflag == MEM_READ) {
2052| 		if (relative_addr == wd_data)
2053| 			memory_writemax64(cpu, data, len, odata);
2054| 		else {
      [... lines 2055-2059 omitted ...]
2060| 			if (len != 1 && !d->warned_nonbyte_read) {
2061| 				d->warned_nonbyte_read = 1;
2062| 				fatal("[ wdc: WARNING! non-8-bit access on "
2063| 				    "READ! ]\n");
2064| 			}
2065| 			data[0] = odata;
2066| 		}
2067| 	}
2068| 
2069| 	return 1;
2070| }
~~~~

**8.7 `wdc_command()` -- the callers of the two edit sites, and the no-disk refusal (S5, S11, P18):**
*`src/devices/dev_wdc.c` at HEAD, lines 947-954, 965-983:*
~~~~
947| 	if (!diskimage_exist(cpu->machine, d->drive + d->base_drive,
948| 	    DISKIMAGE_IDE)) {
949| 		debug("[ wdc: command 0x%02x drive %i, but no disk image ]\n",
950| 		    d->cur_command, d->drive + d->base_drive);
951| 		d->error |= WDCE_ABRT;
952| 		d->int_assert = 1;
953| 		return;
954| 	}
     [... lines 955-964 omitted ...]
965| 	switch (d->cur_command) {
966| 
967| 	case WDCC_READ:
968| 	case WDCC_READMULTI:
969| 		if (!quiet_mode)
970| 			debug("[ wdc: READ from drive %i, head %i, cyl %i, "
971| 			    "sector %i, nsecs %i ]\n", d->drive, d->head,
972| 			    d->cyl_hi*256+d->cyl_lo, d->sector, d->seccnt);
973| 		wdc__read(cpu, d);
974| 		break;
975| 
976| 	case WDCC_WRITE:
977| 	case WDCC_WRITEMULTI:
978| 		if (!quiet_mode)
979| 			debug("[ wdc: WRITE to drive %i, head %i, cyl %i, "
980| 			    "sector %i, nsecs %i ]\n", d->drive, d->head,
981| 			    d->cyl_hi*256+d->cyl_lo, d->sector, d->seccnt);
982| 		wdc__write(cpu, d);
983| 		break;
~~~~

**8.8** *(the write drain and the init-time geometry copy are not inlined in this form; S7 and S9 state what they do.)*

**8.9 `src/disk/diskimage.c` -- the access bounds and `diskimage_access()` (S8) -- the geometry and the default disk type are cut here; S9 and S18 quote them:**
*`src/disk/diskimage.c` at HEAD, lines 1591-1601, 1689-1697:*
~~~~
1591| 	if (!d->is_a_tape) {
1592| 		int64_t limit = writeflag ? d->total_size
1593| 		    : (int64_t) d->nr_of_logical_blocks * d->logical_block_size;
1594| 
1595| 		if (offset < 0 || (int64_t)len > limit ||
1596| 		    (int64_t)offset > limit - (int64_t)len) {
1597| 			if (!writeflag)
1598| 				memset(buf, 0, len);
1599| 			return 0;
1600| 		}
1601| 	}
      [... lines 1602-1688 omitted ...]
1689| 	offset -= d->override_base_offset;
1690| 	if (offset < 0 && offset + d->override_base_offset >= 0) {
1691| 		debug("[ reading before start of disk image ]\n");
1692| 		/*  Returning zeros.  */
1693| 		memset(buf, 0, len);
1694| 		return 1;
1695| 	}
1696| 
1697| 	return diskimage__internal_access(d, writeflag, offset, buf, len);
~~~~

**8.11 The witness instrument, FROZEN copy `regress/artifacts/wdclbaaddr/witness_20261024/wdc_lba_probe.frozen.py`
(md5 `8f3632ffc1c982fd523c7fd28d86f15d`) -- the mechanics S24 and P7, P10-P12 rest on:**
*`regress/artifacts/wdclbaaddr/witness_20261024/wdc_lba_probe.frozen.py` (working tree), lines 487-488, 504-505, 512-527, 530-540:*
~~~~
487|     hs = (TAG(H * S - 1)) if (H and S) else None   # lba 256 on the CHS (HEAD) decode
488|     wr = COMB(WR_W0, WR_W1)                         # 0x88887777, the written payload
     [... lines 489-503 omitted ...]
504|     rows.append(("chs h1", "control", COMB(chs.get("h1_lo"), chs.get("h1_hi")),
505|                  TAG(S) if S else None, TAG(S) if S else None, "eq"))
     [... lines 506-511 omitted ...]
512|     rows.append(("lba 70", "symptom", COMB(lba.get("l70_lo"), lba.get("l70_hi")),
513|                  TAG(69), TAG(70), "eq"))
514|     rows.append(("lba 256", "symptom", COMB(lba.get("l256_lo"), lba.get("l256_hi")),
515|                  hs, TAG(256), "eq"))
516|     l0 = sess.get("lba0", {})
517|     rows.append(("lba 0", "symptom", COMB(l0.get("l0_lo"), l0.get("l0_hi")),
518|                  TAG(0), TAG(0), "nehead"))     # HEAD: anything but tag 0; FIX: tag 0
519| 
520|     lw = sess.get("lbawr", {})
521|     rows.append(("lba wr", "symptom", COMB(lw.get("wr_lo"), lw.get("wr_hi")),
522|                  TAG(70), wr, "eq"))
523|     rows.append(("lba wr2", "symptom", COMB(lw.get("wr2_lo"), lw.get("wr2_hi")),
524|                  wr, TAG(69), "eq"))
525| 
526|     rows.append(("neg appar", "control", 0x0001, 0x0000, 0x0000, "neg"))
527|     return rows
     [... lines 528-529 omitted ...]
530| def row_ok(mode, got, want, column="HEAD"):
531|     if mode == "nz":
532|         H, S = got
533|         return bool(H) and bool(S) and H != 0 and S != 0
534|     if mode == "neg":
535|         return got != want          # the parser MUST report this mismatch as a FAIL
536|     if mode == "nehead":            # HEAD column: any served value but `want`; FIX column: exactly `want`
537|         if got is None:
538|             return False
539|         return got != want if column == "HEAD" else got == want
540|     return got == want
~~~~

**8.12** *(the gate wiring, gate 2's word-49 row, the rig driver and the vehicle: S16-S18 and S21 quote what is used.)*

---

## 9. Primary sources -- the load-bearing lines (VERBATIM)

*(S12 and S13 quote the ATA-2 and NetBSD lines the questions use, VERBATIM.  The ATA-2 text is X3T10/0948D
Revision 4c, 1996-03-18 -- by its own cover "not a completed standard".)*

---

## 10. The project rules the questions apply -- quoted with their bounds

CONDENSED: the rules the questions grade by are quoted VERBATIM (emphasis dropped) from the root `CLAUDE.md` with line
numbers; the rest are one-line PARAPHRASES, marked so.  The framing paragraph in section 0 defines the mutation-testing
words.

* **R1** (1328-1331): *"A detector is VACUOUS — replace it IN-ROUND — unless it (a) fails on the pre-fix build, (b) fails on
  a VERBATIM REINSTATEMENT of the removed defect at EVERY fixed site, and (c) fails on a NULL MEDIUM -- a product medium
  carrying none of the behaviour under test"*.
* **R2** (1345, 1359-1365): for *"a runtime probe: an ABSENT or NON-EMULATOR binary (every session dies)"*; recorded as
  *"`(c): measured at <artifact>`"* or *"`(c): by construction via <row/pin>, leg not run` -- e.g. the gate pins the row
  count by EQUALITY and a named row reds on a dead run"*; *"where the reading fails -- no runtime gate wiring, no pin,
  `check_min`, a control computed over the row list (`all([])` is True) -- the leg is OWED"*; *"Predict a dead run's score
  from the source, not from the row count"*.
* **R3** (1376-1377, 1392-1395): *"(d) The detector must also fail when the fix is PRESENT but its REPAIR IS NULLED — the
  guard kept, its effect removed."*  *"Take each predicate the fix DEPENDS ON and weaken it to the least-restrictive form
  that still reads like the same check: a mask narrowed (`& 3` -> `& 1`), a condition qualified (`if (X)` -> `if (X &&
  writeflag == MEM_WRITE)`), a bound relaxed."*
* **R4** (1448-1451): *"DEPENDS ON enumerates exactly two things: (1) the predicates DOMINATING the diff's edited lines,
  walked up only to the ENCLOSING FUNCTION BOUNDARY -- never into callees or callers; and (2) for operand-swap forms, swaps
  drawn ONLY from fields the guarded BODY reads"*.
* **R5** (1464-1465, 1470-1472): *"DEPENDS-ON enumerates JOINT cells over the guard's operands and the body-read lvalues
  EXACTLY WHEN THE GUARDED BODY'S OWN CODE DISTINGUISHES THEM."* ... *"A value or combination the body never tests as a
  case (`idata == k`; a byte no conditional distinguishes; both counts >= 2 where the body tests `> 0`) is DISCLOSED under
  clause (e)."*
* **R6-R9, PARAPHRASED**: R6 (1618-1630) a lvalue the body never tests is clause-(e) disclosure, EXHAUSTED or SAMPLED, and
  disclosure never demands a row; R7 (1801-1807) the probe header names what it catches, and a breach of that contract is
  L2; R8 (1888-1898) a detector claiming to pin WHERE an access lands needs one ANCHORED row -- *"If every address in this
  device shifted one word, which row reds?"*; R9 (1639-1650) a `PRETABLE.out`, written before table 1, is mandatory for a
  round shipping a table-backed detector.
* **R10** (1740-1741): GUARD FIELD vs BODY FIELD -- *"where they differ, grep whether they are written at the same sites. If
  not, the detector owes a state where they DISAGREE."*  CHANNEL -- *"A row whose named channel cannot vary under its named
  mutant is VACUOUS BY CONSTRUCTION"*.
* **R11, PARAPHRASED** (1991-1993): a proposed edit is a sketch until checked against the enclosing function's real control
  flow, every exit path and the common tail included.
* **R12** (2023-2024, 2028-2029, 2041, 2047, 2052): *"1 DELETE  ·  2 DECLINE (silent)  ·  3 DECLINE + BOUNDED (LATCHED)
  ANNOUNCE  · 4 ACCEPT  ·  5 FAULT  ·  6 BACKED ACCEPT  ·  7 IMPLEMENT"*; *"7 IMPLEMENT -- write the code.  All six members
  above presume the access is a REFUSAL DECISION, and that presumption fails for an UNIMPLEMENTED PATH."*; *"4 ACCEPT -- the
  model ALREADY computes the right value and then discards it."*; *"5 FAULT -- deliver the architectural bus error, by
  MODELLING THE SPACE AS UNMAPPED."*; *"BEFORE CHOOSING A MEMBER, CHECK IT IS AVAILABLE ON THIS CPU."*
* **R13** (2334-2335): *"Additions to product code in a hardening fork are licensed by MEASURED DELTAS or by a TRANSFERRED
  WARRANT -- never by "it cannot hurt.""*
* **R14-R16, PARAPHRASED**: R14 de-escalation -- N/A, no `exit(` is deleted; R15 one ask-again per detector per round; R16
  in-round repairs of detector material are licensed only as L1 construction, L2 floor breach, L3 undischarged obligation
  or L4 wrong record.
* **R17** (2788-2794): a witness is valid only if *"(i) it shows the defect symptom on the pre-fix committed HEAD and goes
  green post-fix with the same script"*, (ii) it carries *"a LIVENESS control (a known value returns through the same
  decode) AND a DEVICE-SIGNATURE control (the observed value could only have come from the device — RAM would answer
  differently"*, and *"(iii) the machine description and dispatch are committed and unmodified"*.
* **R18-R21, PARAPHRASED**: R18 `detector:` is not a rung and ranks below every access witness; R19 a stated premise is
  load-bearing and agreement with it is not evidence; R20 a count names its deriver; R21 compare edges -- N/A, no
  relational compare against a constant.
* **R22** (template 648-650): *"A by-construction claim fails its reading -- and the leg is owed -- when the probe has no
  runtime gate wiring, the gate pins with `check_min` or not at all, or the control is computed over the row list
  (`all([])` is True).  Predict a dead run's score from the source (some rows test only exit status)."*
* **R23, PARAPHRASED** (2877-2880): a round takes one site; a second joins only if witnessed, in the same device and
  semantic class, under one fix design and one detector.

---
## 11. QUESTIONS -- VERDICT LINE FIRST (format in section 0)

**Q1 -- the repair: complete, correct, and the right member?**

(a) **Premises, then the partition.**  Which of S1-S24 is false?  Answer P1-P4.  Then check 7.1 as a PARTITION OF INPUTS
(no edit text is wanted): for which (select byte, opcode, address) does the repair change what the model serves, and which
does it leave alone?  Must anything outside the four fixed sites (7.2(b)) change?

(b) **The decode and the read-back** (D5, P2, R13).  With `lba` from bit 6, `sectorsize` still holds bits 7-6: bit 6 held
twice, bit 5 by nothing.  Which mechanism -- (i) store the raw SDH byte, return it, derive `lba`/`drive`/`head` from it;
(ii) repurpose `sectorsize` to hold bits 7 and 5 (`idata & 0xa0`) and compose `| (lba << 6)`; (iii) a new one-bit field;
(iv) other?  For each: V16-V18, and the debug lines (2010-2012, 2018-2020).  An added field is an ADDITION (R13): is V17's
predicted delta (`sdh rb2` reading 0x93) its licence, or must it be measured?  If `sectorsize` loses its last reader, is
removing it in scope?

(c) **The arithmetic and the two sites** (D2, D3, P8, R11).  A 64-bit product at both sites (the CHS line's `(int64_t)`
idiom), or one helper returning the media offset for both?  What becomes of the `printf` calls (475, 567)?  Check the form
against each function's real control flow (8.3, 8.4; S7): the chunk loop, its `break`, the tail `d->int_assert = 1;`,
`wdc__write()`'s three assignments, and the drain that consumes `write_offset`.

(d) **The option set** (R12, P18).  Which member is the repair?  Is FAULT available here (ABRT through the error register,
as the no-disk arm does at 947-954), and is refusing LBA-mode media commands while word 49 = 0 more coherent under ATA-2
than honouring them (P4)?  Is a member unnamed?

(e) **What must NOT change**: the CHS formula, the drive and head decode, the ATAPI path, `#481`'s control-register
handling, the `wdc_altstatus` region, the SDH read-back.  Complete?  Is this ONE round under R23?

(f) **What else the repair carries**: a `/* #NNN: */` tag per edited site; the same bytes in `est/` and the build trees
(`dev_wdc.c` is shared, not a declared divergence); and which comments in `dev_wdc.c` become false once `d->lba` is read
for an address?

**Q2 -- the detector: complete, bounded, valid?**

(a) **The floor** (R1-R6, R10; 7.2, 7.3).  Grade C1-C20 as FLOOR, clause-(e) debt or NOT A CELL, citing the rule -- in
particular C5/C10 (head != 0: same write site as `lba`, independent bit), C7 (no CHS row at the write site), C9, and C6/C11
(cyl_hi, IMAGE).  Is a cell missing?

(b) **Classify V1-V20** (7.5): is each predicted red row right, and the class?  Which are EQUIVALENT in every state, and
which only on a 4,096-sector image?  For V15, which outcome do you expect at `-O3` without `-fwrapv`, and does it change
whether the source must be widened?  Is 7.2(d)'s list of dominating predicates complete, and is a variant missing from the
DEPENDS-ON closure (R4), including at the decode line?

(c) **The rows N1-N9** (7.4) as DATA: correct any want.  Can each row's channel vary under its variant (R10)?  N1 and N2
rest on S8's zero-fill and refused write: what keeps a zero row from passing when a session's reads fail (P12)?  Answer
P10, P11, P13, P14 and P16 (enlarge the image and widen the tag, or disclose).

(d) **Clause (c) and the dead run** (R2, R22, P12): which null medium, which record form, and is the predicted dead-run score
(3/19 HEAD, 2/19 FIX, CONTROL=FAIL, exit 1) right?  Should a `None` want fail its row, and should `neg appar` -- built from
constants, so it cannot fail -- become a real parser self-test or leave the score?

(e) **The contract and the anchor** (R7, R8; 7.6): correct the CATCHES / BLIND text.  "If every LBA moved by one sector,
which row reds?" -- and if every WRITE did?

**Q3 -- word 49 first; then shape, home, witness term and records**

(a) **Word 49** (D4, P3-P6; S12, S17, S18, S22).  Keep it 0 in this round?  If yes, what warrant (R13) and gate does the
advertisement need, given that no battery rig can observe it (S18)?  If no, what does advertising change on the one rig
that reaches `dev_wdc.c`, and which IDENTIFY words must move with bit 9 (words 60-61, S12)?

(b) **Shape and home** (P7; S16, S23; 7.7): single-leg in gate 10 beside `wdc_altdigin_probe.py`, the denominator pinned by
EQUALITY, a `CLASS_DETECTOR` line -- or the two-leg shape with a dated exemption, one more instance of the `wdcaltoffleg`
debt?  Name the result and control lines and the gate checks.

(c) **The witness term** (R17, R18, P15): `probe:regress/wdc_lba_probe.py -- rung 3, unmodified evbmips -e malta,
regress/artifacts/wdclbaaddr/witness_20261024/` once the fixed leg is green with the same script -- or `detector:`?  What
must the record show about ORDER (2.4)?

(d) **Records to touch in the SAME change** (R16 L4): `diff_wdc_identify.c`'s `row_no_lba_claim()` (S17 -- "must be
re-authored in the SAME change"; its FAIL text "neither is implemented" becomes false for LBA) and `gate_offline.sh`'s name
pin and comment -- both files carrying uncommitted peer hunks (section 0); the `&& !d->lba` records (P17); the IDENTIFY
word-49 comment (374-375).  Which are this round's obligations, which file as rows, and how is the commit kept to this
round's hunks?

(e) **The CHANGELOG block.**  Must claim: the witness; word 49 unchanged; LBA honoured for LBA-mode media commands only; the
48-bit commands not implemented (S11).  Must NOT claim that guests now use LBA (NetBSD and OpenBSD stay CHS while word 49 =
0; S13, S22), nor coverage of V7, V9, V10 unless rowed.  Anything else?  Filings: the advertisement (if kept 0); media
requests past the image that complete with no error (7.1); others?

**Q4 -- the standing licence**

If, while verifying a claim, you found something ELSE -- say so.  Candidates from drafting, to check rather than findings:

1. `dev_wdc.c`'s `#485` comment (1081-1082) and gate 2's comment (`gate_offline.sh` 1525-1526) say no ATA document exists
   "in this tree"; `#525`'s comment in the same file (640) cites `_scratchpad/ata2_x3t10_948d.txt`, which the carrier's
   list of manuals omits.
2. IDENTIFY word 53 = 0x0002 declares words 54-58 not valid while words 57-58 carry a capacity (S10).
3. A media request past the image completes with no error, CHS and LBA alike (7.1): a sibling to file?
4. `ADJ_RULINGS.md` B calls Grok's reading "the measurement" and "the measured one"; its header says neither seat built or
   ran anything (1.3).
5. The witness docstring (frozen copy, 14-15, joined) says *"Under the HEAD decode every 0xe0 is read as head=0"*; the
   operative fact is that every 0xa0 sets `lba = 1` (S1, D1).
6. `wdccylwrap` (1.6) concerns the same geometry: once LBA-mode requests are honoured, does a guest that ignores word 49 still
   depend on word 1 -- does that row's severity change?

---

## 12. Paths

Every repository path cited exists at HEAD, or (the witness and its frozen probe) in the working tree, untracked --
checked at drafting with `[ -e ]` and a `cmp` against `git show HEAD:` (0 missing); the FULL form lists them one per line.
