FABLEADJ_FBS
model: Fable 5.1 (claude-fable-5-1)
Adjudication of GPT-6 Astra's (`grok_20261106/astra_FBS/codex_ASTRACONF_FBS.txt`, DISSENT 2) and Grok 4.7's
(`grok_20261106/grok_FBS.txt`, DISSENT 4) reviews of my REGRESS ruling (`fable_20261106/item1/RULING.md`) on #585
`fbsdrampair`.  Both seats confirm the floor (a)-(f) and dissent only from "no wrong record" / unconditional LAND.
Every point below was checked by opening the file named; nothing was judged.  Read-only: no build, gate, probe or panel.

HEAD is `ab39ba0d`, one commit past the ruling's `2632277f`; `git diff --stat 2632277f ab39ba0d` touches only
`tools/pipeline/check_probe_wiring.py`, so every line number in the ruling, the staged kit and this file still holds.

## The points, one by one

**A1 = G2 (BOTH seats): the `fbsdramwrites` state_note repeats the rejected reset premise.  ACCEPT.  L4.**
`_scratchpad/wfbs/landing/files_fbs.py:290` -> `landing/ledger.json:76565` (and `pretest_records/ledger.json:76565`): "the
datasheet gives the full semantics (two uint32 fields, reset 00FC0000h and 0, ...)".  Present tense, unmarked, in the ledger
row the kit will commit.  `adj_p1_20261105/RESET_PREMISE_NOTE.md:15` ("in normal operation BOTH registers reset to 0") and the
staged fix comment itself (`staged/dev_footbridge.c:746-748`: "0 is also both registers' normal reset value; 00FC0000h is only
the mask's blank-ROM-programming default") refute it.  Re-read in the datasheet, not taken from the seats: `dc21285.txt:3206`
"Blank ROM Programming ... When this mode is enabled:" governs `:3225` (the 00FC0000h line); 7.3.9 carries "Reset value: 0." at
`:5859` and `:5873`, 7.3.10's Offset field "Reset value: 0." at `:5912`.  The sentence is a paraphrase of `ADJ_MYTHOS.md:67`,
which carried the pass-1 packet's false premise even while ruling ZERO on other grounds -- the generator copied the premise
without the correction.  The OUTSTANDING one-liner (`landing/OUTSTANDING_BUGS.md:26699`) and the CHANGELOG block
(`CHANGELOG_block_fbs.md:23-24`) do NOT carry it; Grok's scoping is right.  **Harder on my ruling:** C30 read the #585 row and
C32 the OUTSTANDING section; neither opened the generated `fbsdramwrites` row.  The omission is mine.

**A2 (Astra): probe `:203-204` overclaims "any extra footbridge diagnostic reds the row".  ACCEPT.  L4.**
`staged/footbridge_sites_probe.py:850` (M3 `SM["fatals"] == [SD_MASK]`), `:860` (O3), `:868` (X1 `== [SD_MASK, SD_OFFSET]`) and
`:905` (U1 `not SU["fatals"]`) compare the WHOLE list, so the sentence is true of them.  It is false of W1 (`:877-878`: only
`SD_MASK not in` / `SD_OFFSET not in`), W2 (`:880`: `startswith("[ footbridge write to sdram_ba_")`, then `==` on the filtered
list) and B1/B2/B3 (`:892`, `:895`, `:898`: `count(...) == 1`).  An extra bracketed line from a write arm reds nothing (no read
arm runs in W, and B's counts are unchanged); an extra line from a READ arm reds M3/O3/X1 but not B1/B2.  Source-derived, as
Astra says; no measurement claims otherwise.  Not a (d) matter: the write arms are byte-unchanged (ruling C07) and outside the
diff's two hunks.  **Harder on my ruling:** C17 checked the parenthetical lists at `:208-218`; C34 cited `:203-204` for the
misname half, which IS true (B1/B2's counts change) -- and I did not check the "any extra" clause beside it.

**G1 (Grok): ruling C08 says member 6 "was declined for want of a consumer and is carried by `fbsdramwrites`".  ACCEPT, and
the proposed rewording is also wrong.  L4 (against my ruling).**  `ADJ_MYTHOS.md:67`: the filing names **member 7 IMPLEMENT**
as the joint disposition and declines it "because it still lacks a consumer to validate against"; `files_fbs.py:289` and
`OUTSTANDING_BUGS.md:26699` say member 7.  Member 6 (constant-backed ACCEPT, the reset-value design, `ADJ_MYTHOS.md:75`) was
rejected at `:30` and `:35` for want of a **WARRANT** ("gates on a warrant ... needs the warrant that is absent"), not of a
consumer.  So C08 misattributes both the reason and the carrier, and Grok's replacement ("member 6 was declined for want of a
consumer") keeps the first error.  C32's "slightly loose" caution was about the comment's "keeping writes is filed" and stands.

**G3 (Grok): "arm M's reads" for arm U at probe `:200`, `:420`, `:900` and `gate_arm.sh:1172`.  ACCEPT, plus a fifth site.  L4.**
Arm M is three loads of +0x100 into r7, r8, r9 (`staged/footbridge_sites_probe.py:371-373`); arm U is ONE load of +0x100 into r7
and ONE of +0x104 into r9 (`:423-424`).  All four cited sites say "arm M's reads" / "M's reads with the MMU left ON"; so does
**`CHANGELOG_block_fbs.md:28`** ("U repeats M's reads with the MMU on"), which neither seat named, and its copy
`pretest_records/CHANGELOG.md:28`.  The addresses at `:201` and U1's oracle (`:905`: alive, no diagnostic, r7 = r9 = 0) are
true, so C19 and clause (f) stand.  Comment- and docstring-only: the AST-minus-docstrings identity is unaffected by construction.

**G4 (Grok): F2 attributes the sub-word read's 0 to "the pre-zeroed buffer".  ACCEPT.  L4.**  The width variant is
`writeflag == MEM_READ && len == 4` (`table1_20261105/fbs_variants_1.py:111`); a byte/halfword read therefore takes the write arm,
whose `switch (idata)` hits `SDRAM_MASK_256KB` (= 0) and `break`s (`staged/dev_footbridge.c:756-768`, then `:775`), and the
common tail RUNS: `:802-803` `memory_writemax64(cpu, data, len, odata)` with `odata` still 0 (`:511` initialises it; neither
read arm assigns it).  The guest reads 0 because the tail writes 0 over `len` bytes; `memory_rw.c:491-492`'s pre-zero is the
reason the EARLY RETURN is equivalent (`fbs_variants_1.py:204-205`, probe NOT COVERED (1)) -- a path the tail does not reach.
The wrong reason is repeated in `REGRESS_fbs.json` (both copies: `fable_20261106/item1/` and `landing/:12`, "it still reads 0
(memory_rw.c #95 pre-zero)") and lands in `landing/ledger.json:76576` as `fbsdramwidth`'s state_note.  The 56/56 measurement,
the derived offset form, the 7n-5 grade and LOW all stand.

## Shared / tally
Six points raised (Astra 2, Grok 4), FIVE distinct -- A1 and G2 are the same finding, and both seats are right.  All six
ACCEPTED, none REJECTED (G1's proposed wording is corrected, not its finding).  No floor breach is alleged by either seat and
none exists: every repair is to text, none to executable code, and no number in any record changes.  My ruling's four floor
numbers, the (d) enumeration, the B2 settlement and F1/F2's dispositions are confirmed by both seats and re-read here.

## FINAL DISPOSITION: LAND AFTER RECORD REPAIRS (all L4; no detector or code repair; no table, probe or gate run owed)
1. `_scratchpad/wfbs/landing/files_fbs.py:290` -- replace "reset 00FC0000h and 0" with "normal reset 0 for both -- the ruling's
   '00FC0000h' is the mask's blank-ROM-programming default only, the pass-1 packet premise corrected in
   adj_p1_20261105/RESET_PREMISE_NOTE.md"; regenerate `ledger.json` (row at `:76565`), `OUTSTANDING_BUGS.md` and `matrix.html`
   through the kit, never by hand.
2. `staged/footbridge_sites_probe.py:203-204` -- scope the sentence: "... so a misnamed register or HEAD's exit text kept
   without its exit reds B1/B2 and the list rows; ANY extra footbridge diagnostic reds only the rows that compare the whole
   list (M3, O3, X1, U1) -- W1 tests only the two read texts, W2 filters by the write-announce prefix, B1-B3 count named texts."
3. `staged/footbridge_sites_probe.py:200`, `:420`, `:900`; `staged/gate_arm.sh:1172`; `CHANGELOG_block_fbs.md:28` -- "arm M's
   reads" / "M's reads" -> "one read of each register (+0x100 into r7, +0x104 into r9)" with the MMU left on.
4. `REGRESS_fbs.json` (the landing copy the kit reads, and the item1 copy) `fbsdramwidth` state_note -- "(memory_rw.c #95
   pre-zero)" -> "(the common tail writes odata, still 0; the pre-zero is the early return's reason, not this path's)";
   regenerate the ledger row at `:76576`.
5. `RULING.md` before it is banked as `regress_20261106/REG_FABLE.md` -- correct C08 in place (member 6 rejected for want of a
   WARRANT, ADJ_MYTHOS.md:30/:35; `fbsdramwrites` names member 7, declined for want of a consumer, :67) and F2's reason as in 4,
   each quoting the text it refutes; append a dated postscript naming this adjudication and the five repairs, and amend the
   REGRESS_fbs.json `paragraph`'s "the CHANGELOG block, the ledger row and the OUTSTANDING section are true of what ships ...
   no repair owed" to say which records were repaired before landing.  Bank this file beside it as `regress_20261106/ADJ_FBS.md`.
After 2-3: re-run the kit's identity and manifest steps (PROBE_IDENTITY / AST minus docstrings must still read True against
`table1_20261105/probe56_frozen.py`; MD5SUMS, MANIFEST).  Docstring and comment edits cannot change that identity, so table 1,
the settle run and the DRYRUN replay remain measurements of the shipping instrument; the two-part clearance of the build trees
stays the landing window's step (PRETEST step 3), unchanged.

FABLEADJ_FBS: 6 ACCEPTED 0 REJECTED VERDICT:LAND-AFTER-RECORDS
