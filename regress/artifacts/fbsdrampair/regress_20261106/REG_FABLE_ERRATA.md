# REG_FABLE.md -- errata (2026-11-06)

`REG_FABLE.md` beside this file is Fable 5.1's REGRESS ruling on `#585` (`fbsdrampair`) as the landing commit `54613aa1` banked it --
`_scratchpad/fable_20261106/item1/RULING.md` byte for byte (20942 bytes, md5 `66a216cfa5171b43e19c288569b30e93`).  It is kept as written; this note corrects it,
each item quoting the text it refutes.  By the owner's flow of 2026-11-06 ("Land commit and have astra and Grok review then sending
back to Fable"), GPT-6 Astra (`ASTRACONF_FBS.txt`, DISSENT 2 points) and Grok 4.7 (`GROKCONF_FBS.txt`, DISSENT 4 points) reviewed
the ruling once the landing commit was in its hook, and Fable 5.1 adjudicated their reviews (`ADJ_FBS.md`, `FABLEADJ_FBS: 6 ACCEPTED 0 REJECTED VERDICT:LAND-AFTER-RECORDS`).
All three answers and their briefs are banked beside this file.  Short paths are under `regress/artifacts/fbsdrampair/`; line
numbers are those of the files as `54613aa1` holds them.

## 1. C08 -- the member, and the reason (ADJ_FBS.md G1, from Grok 4.7)

`REG_FABLE.md:26` says: "member 6 (BACKED ACCEPT) was declined for want of a consumer and is carried by `fbsdramwrites`."

Member 6 -- the constant-backed ACCEPT, i.e. the reset-value design (`adj_p1_20261105/ADJ_MYTHOS.md:75`) -- was rejected for want
of a WARRANT, not of a consumer: it "gates on a warrant" (`ADJ_MYTHOS.md:30`) and "needs the warrant that is absent" (`:35`).
`fbsdramwrites` names member 7 IMPLEMENT as the joint disposition, and member 7 is the one declined for want of a consumer: "it
still lacks a consumer to validate against" (`ADJ_MYTHOS.md:67`).  Grok's proposed rewording ("member 6 was declined for want of
a consumer") kept the first error; the adjudication corrected it.  C32's "slightly loose" caution, about the fix comment's
"keeping writes is filed", stands.

## 2. F2 -- why a diverted sub-word read still reads 0 (ADJ_FBS.md G4, from Grok 4.7)

`REG_FABLE.md:86` says a sub-word read at exactly +0x100 or +0x104 "still reads 0 (the pre-zeroed buffer)".

The width conjunct (`writeflag == MEM_READ && len == 4`, `table1_20261105/fbs_variants_1.py:111`) sends a byte or halfword read
into the WRITE arm with `idata` 0: at +0x100 `switch (idata)` matches `SDRAM_MASK_256KB` (0) and breaks
(`src/devices/dev_footbridge.c:756-768`); at +0x104 `idata != 0` is false (`:787`).  The common tail then RUNS --
`if (writeflag == MEM_READ) memory_writemax64(cpu, data, len, odata);` (`:802-803`) -- with `odata` still 0 (declared `= 0` at
`:516`; neither SDRAM arm assigns it).  The guest reads 0 because the tail writes 0.  `src/cpus/memory_rw.c:491-492`'s pre-zero
(#95) is the reason an EARLY RETURN is equivalent (`table1_20261105/fbs_variants_1.py:204-205`; the probe's NOT COVERED (1)) -- a
path that skips the tail, not this one.  The measurement (56 of 56), the derived offset form, the 7n-5 grade and LOW stand.  The
same reason was in the `fbsdramwidth` ledger row's state note, which carried F2's filing; that row is corrected in place.
(ADJ_FBS.md's G4 cites `:511` for the declaration; at `54613aa1` the line is `:516`.)

## 3. "No wrong record" (ADJ_FBS.md A1 = G2, A2, G3)

`REG_FABLE.md:3` says "every record checked is true of what ships; no floor breach, no repair owed", and `:87` "No wrong record
found in the fix, the probe, the gate block, the CHANGELOG block, the ledger row or the OUTSTANDING section."

"No floor breach" stands: both reviews confirm the floor (a)-(f), and every finding is text -- none in executable code, no number
changed.  The rest does not.  Besides items 1 and 2, the records carried three wrong statements the ruling passed:
* A1 (GPT-6 Astra and Grok 4.7): the `fbsdramwrites` row's state note gave the datasheet as "reset 00FC0000h and 0" -- the pass-1
  packet's premise, which `adj_p1_20261105/RESET_PREMISE_NOTE.md:15` corrects ("in normal operation BOTH registers reset to 0";
  00FC0000h is the mask's blank-ROM-programming default).  C30 read the `fbsdrampair` row and C32 the OUTSTANDING section;
  neither opened the generated `fbsdramwrites` row.
* A2 (GPT-6 Astra): the probe's "any extra footbridge diagnostic reds the row" is true of M3, O3, X1 and U1, which compare the
  whole list, and false of W1 (it tests only the two read texts), W2 (it filters by the write-announce prefix) and B1-B3 (they
  count named texts).
* G3 (Grok 4.7, with a fifth site the adjudication found): arm U was called "arm M's reads" / "M's reads" in the probe's
  docstring and two comments, gate 14's comment and the `#585` CHANGELOG block.  Arm M is three loads of +0x100; arm U is one load
  of +0x100 into r7 and one of +0x104 into r9.

So the verdict, as adjudicated, is LAND AFTER RECORD REPAIRS.

## 4. The repairs, as made

The landing commit `54613aa1` was already in its hook when the adjudication was written (the commit is dated 2026-11-06T22:52:53Z;
`ADJ_FBS.md` was written at 2026-11-06T23:43:10Z), so the repairs follow it in the records commit that names it, rather than preceding it.
Each corrects its record in place and quotes what it replaces:
1. A1 -- `tools/pipeline/ledger.json`, the `fbsdramwrites` state note: "normal reset 0 for both", with the old parenthesis quoted.
2. A2 and G3 -- `regress/footbridge_sites_probe.py`: the docstring's arm-U row and the sentence after it, and the two arm-U comments.
3. G3 -- `regress/gate_arm.sh`: gate 14's footbridge comment.
4. G3 and the REGRESS amendment -- `CHANGELOG.md`'s `#585` block: arm U's sentence, and the REGRESS paragraph amended ("no repair
   owed" held for the fix and the detector, not for the records).
5. G1 and G4 -- this note (items 1 and 2) for the ruling, and the `fbsdramwidth` state note in the ledger.
Beside them: `fbsdrampair`'s state note names the adjudication; its regress stage records the two reviews (objection) and the
adjudication (approved); OUTSTANDING_BUGS.md's `#585` section names the adjudication, and its `fbsdramwidth` line, whose title the
landing cut mid-word, is restored whole.

Proofs, from the bytes the records commit stages (`_scratchpad/wfbs/landing/mk_hashfollow_fbs.py`):
* the probe (blob `7b1f3bf22e0fe9e2f260a32cb8fab202a7a920ea`, md5 `2e8a7cbe2af7aed9e9fabdf25cfe8f65`): its AST with every docstring removed equals the landed probe's and
  `table1_20261105/probe56_frozen.py`'s, and its tokens outside comments and the module docstring are the landed ones -- so table 1,
  the settle run and the replay still measure the shipping instrument;
* gate 14 (blob `7461dfd25e3edf16216e20db92e0171738d36314`, md5 `47be54a210da24efc42a32b2c1f12027`): the diff touches comment lines only, and `bash -n` passes.
