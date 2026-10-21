VERDICT: 4 of 4 sub-claims are wrong records at HEAD -- `kept below' points at the wrong five rows (and was positionally true in no revision on record), the banner credits ROTL32 that no row consumes, `EVERY want ... never from the tree' fails on two tree-sourced wants and three non-rldiclx ones, and the CONTRACT's `every entry ... built and scored' has no built mutant behind 7 of its 14 entries; all four are comment/print-only L4s that no gate or checker reads, and 5b is the weakest (its rldicl-value core is true).

Seat: records check, READ-ONLY.  Liveness: RLDFLAG_ALIVE_20261020; first line of
`_scratchpad/CHECKPOINT.md`: `# CHECKPOINT -- 2026-10-07 11:3x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)`

Tree: `GXEMUL-SEC`, HEAD `5dbc000e`.  `regress/ppc_rldicl_probe.py` is clean in the working tree and
`cmp`-identical to `git show HEAD:` (md5 `9cc0ee84`, the same bytes as #565's staged copy
`gatewire_20261018/nullmedium/identity/ppc_rldicl_probe.frozen.py.txt`).  The reviewer
(`_scratchpad/gweb/jobs_20261018_argonpack17/rldiclf2/gemini_web.out`, FLAG lines 4 and 5, Q3 items 3
and 4) read an earlier draft, so its `P:` numbers sit 3-4 lines low; every number below is HEAD's, from
`grep -n`.  Nothing was built, run or written outside this directory.  Artifact paths below are
relative to `regress/artifacts/ppcrldiclzero/` unless they start `regress/`, `src/` or `tools/`.

---

## 4 -- `the five flipped rows being exactly the ones kept below'  ->  WRONG RECORD (L4)

**HEAD says** (`grep -n`):

    554:#  MEASURED: witness 19/27 committed and 24/27 fixed, the five flipped rows being
    555:#  exactly the ones kept below.  **THIS FILE HAS 19 ROWS, NOT 24** [19-row era: 24 since

**(a) Position at HEAD -- the reviewer is right.**  Every row the sentence means is ABOVE it; the rows
below it are a different five.

| row | line | above/below :555 | flips on the pre-fix build? |
|---|---|---|---|
| zx32 rldicl | 433 | above | yes (t1 and t2) |
| rot8 rldicl | 437 | above | yes |
| vac neighbour | 482 | above | yes |
| census wrong | 531 | above | yes |
| census zero | 533 | above | yes |
| cand session | 602 | **below** | no |
| cr parsed | 603 | **below** | no |
| sh63 rldicl | 605 | **below** | yes (t2 only -- the row did not exist in the witness) |
| sh32 rldicl | 607 | **below** | yes (t2 only) |
| rc cr0 | 609 | **below** | yes (t2 only) |

`killtable_20260910/t2/SCORES.txt`: HEAD and M_ORIG legs `16/24`, failing the five above PLUS
`sh63 rldicl, sh32 rldicl, rc cr0`; `cand session` and `cr parsed` stay green.  So 3 of the 5 rows below
flip, as the reviewer said.  None of the five below exists in the witness at all.

**(b) Can `kept below' honestly mean `kept in this file'?**  The surrounding sentences:

    549:#  So this detector is scoped to X(rldicl).  The three sibling rows stay in the
    550:#  witness at regress/artifacts/ppcrldiclzero/, which is the EVIDENCE for those two
    551:#  filed rows and is correctly red there.  When either is fixed, its rows move here
    552:#  or into a detector of its own -- that is a decision for those rounds, not this one.
    553:#
    554:#  MEASURED: witness 19/27 committed and 24/27 fixed, the five flipped rows being
    555:#  exactly the ones kept below.  ...

*`kept'* reads as "kept in this detector", in contrast with "stay in the witness" at :549-550, and the
round's own `killtable_20260910/PRETABLE.out:106-108` paraphrases it that way: *"19/27 on the witness, of
which the five rows kept in the shipped detector are the flipped ones"*.  Under that reading the claim is
TRUE (all five flipped rows are among the 19 this file kept; the three red-in-both rows stayed behind).
*`below'* has no non-positional reading, and at HEAD a positional reader lands on the pass-2 five -- the
same count, so nothing looks wrong.  Worse, #565's own note in this block uses `below' positionally for
exactly those rows: `:556` "see #565's note below" and `:560` "the five rows under `ROWS ADDED BY PASS 2'
below make it 24".  Within six lines, "the five ... below" names two different five-row sets.

**(c) Which five flipped.**  Recomputed row by row from the two witness logs (27 rows each; committed 19
ok, fix 24 ok):

    FLIPPED (5): zx32 rldicl, rot8 rldicl, vac neighbour, census wrong, census zero   (all FAIL -> ok)
    RED IN BOTH: rldimi sh8, rldimi sh32, rlwimi wide                                 (the three sibling rows)

`killtable_20260910/t1/SCORES.txt` (the 19-row instrument): BASE `19/19`; HEAD and M_ORIG `14/19`
failing exactly those five.

**(d) History.**  `git log -L 554,555` traces HEAD's sentence to `e777ff06:438-439` (blame: `e777ff06` for
:554, `8d038908` for :555 because #565 rewrapped that line).  Position of the block in every revision on
record:

| revision | sentence at | rows below it |
|---|---|---|
| earliest frozen drafts, `killtable_20260910/t0_apparatus_failure/` and `t1/ppc_rldicl_probe.frozen.py` (byte-identical, 2026-09-10 14:31/14:34) | :424-425 | **none** -- the block sits after all 19 rows, directly above `SCORE + DONE` |
| pass-2 seat's `pass2_20260910/opus_probe_plus3.py` (15:08) | :444-445 | **none** -- it inserted the pass-2 rows ABOVE the block |
| `e777ff06` (== `t2/ppc_rldicl_probe.frozen.py`, md5 `7ea10ea4`), copy A | :438-439 | the 5 pass-2 rows |
| `e777ff06`, copy B | :504-505 | **none** -- only the CONTRACT (grok_p2 noticed this one) |
| `a05660af` | A :537-538, B :603-604 | as `e777ff06` |
| HEAD (copy A only) | :554-555 | the 5 pass-2 rows |

`#565` (`8d038908`, hunk `@@ -585,27 +609,6 @@`) deleted **copy B** -- the one after the pass-2 rows,
`a05660af:588-608` -- and kept copy A.  **The deletion did not make `below' false**: copy A has had the same
five pass-2 rows below it since `e777ff06`, and before pass 2 the block had nothing below it at all.
"Below" was positionally true in no revision on record.

**Disposition: WRONG RECORD (L4), correct in place.**  Severity low: a comment, read by no gate or
checker (`git grep` at HEAD over `tools/` and `regress/*.{sh,py}`: the only hit is the probe).

**Replacement** (the record it replaces is quoted above, `:555`): keep the sentence; make it
`exactly the ones kept below [#NNN: ABOVE this block, not below it -- see its end].` on its own line, and
append to the block, after `:565`, a dated note naming the five rows, saying they sit ABOVE, that the five
below are pass 2's (three flip pre-fix, `t2/SCORES.txt`), and that deleting copy B did not move copy A.
Exact text in `flags45.diff` hunks 3-4.

---

## 5a -- the banner's `:6878 (ROTL32)'  ->  WRONG RECORD (L4)

**HEAD says:**

    392:print("wants derived from _scratchpad/ppc_pem_32and64_2005.txt:29736 (rldiclx),"
    393:      " :6878 (ROTL32)")

**Enumeration, not the file's own sentence** (`enum_rows.py`, AST only, output `enum_HEAD.out`).
24 `row(` calls; the want of each:

| line | row | want expression | want comes from |
|---|---|---|---|
| 413 | session | `"exit0"` | literal |
| 414 | live | `hex(0x1234)` | literal |
| 416 | seed holds | `hex(SENT)` | own constant |
| 418 | src intact | `hex(RS_VAL)` | own constant |
| 429 | disasm xcheck | `"6/6"` | own count |
| 433 | zx32 rldicl | `want_rldicl(RS_VAL, 0, 32)` | rldiclx (rotl64, mask_b_63) |
| 435 | zx32 rldicr | `want_rldicr(RS_VAL, 0, 31)` | rldicrx (rotl64, mask_0_e) |
| 437 | rot8 rldicl | `want_rldicl(RS_VAL, 8, 0)` | rldiclx |
| 439 | rot8 rldicr | `want_rldicr(RS_VAL, 8, 63)` | rldicrx |
| 445 | naive fix wrong | `"differs"` | literal; got compares rotl64/mask_b_63 against want_rldicl |
| 454 | neg apparatus | `"exit1/-0x1"` | the tree's exit status + own default |
| 465 | bits32 live | `hex(0x1234)` | literal |
| 467 | bits32 rld bad | `"TODO"` | the tree's decoder text `TODO: rld` |
| 480 | vacuous cell | `want_rldicl(RS_VAC, 0, 32)` | rldiclx |
| 482 | vac neighbour | `want_rldicl(RS_VAC, 0, 0)` | rldiclx |
| 529 | census run | `len(uniq)` | own count |
| 531 | census wrong | `0` | literal; per-cell expectation `want_rldicl` at :523 |
| 533 | census zero | `0` | literal; same loop |
| 535 | disasm total | `"%d/%d" % (disasm_checked, disasm_checked)` | own count |
| 602 | cand session | `"exit0"` | literal |
| 603 | cr parsed | `"yes"` | literal |
| 605 | sh63 rldicl | `want_rldicl(RS_VAL, 63, 0)` | rldiclx |
| 607 | sh32 rldicl | `want_rldicl(RS_VAL, 32, 32)` | rldiclx |
| 609 | rc cr0 | `hex(0x40000000)` | literal (CR0=GT) |

Helper call sites at HEAD: `rotl32` only at :283 and :288 (inside `want_rlwinm` / `want_rlwimi`);
`mask32` only at :283, :287; **`want_rldimi`, `want_rlwinm`, `want_rlwimi`: zero call sites**; the
`RLDIMI`/`RLWINM`/`RLWIMI` encoders: zero call sites.  **No scored row reaches ROTL32, directly or
transitively.**  The file's own sentence (`:178-179`, "NO ROW IN THIS FILE CONSUMES want_rldimi, mask32,
want_rlwinm OR want_rlwimi") is CONFIRMED by enumeration, and the banner contradicts it.

**Where it came from:** the banner is the family witness's, verbatim
(`opus_ppc_rldicl_witness_20260910.py:317`), where rows `rlwinm` (:497), `rlwimi wide` (:499) and
`rlwimi sh0` (:502) did consume rotl32.  `e777ff06` dropped those rows and kept the banner -- the
carried-across class.

**Nuance that shapes the fix:** `_scratchpad/ppc_pem_32and64_2005.txt:6878` (1,451,137 bytes, not empty)
defines BOTH "1. ROTL64 or rotate64" and "2. ROTL32 or rotate32", and every rldicl/rldicr want uses
rotl64.  So the LINE survives and the LABEL is the false part.  The banner also omits `:29822` (rldicrx,
`m <- MASK(0, e)`), the source of the two rldicr control wants.  (`:29736` is rldiclx's RTL, verified.)

**Disposition: WRONG RECORD (L4).**  Low severity: gate 13 (`regress/gate_ppc.sh:182-200`) reads only the
sentinel, `^<row>  .*ok$`, lines ending ` ok`/` FAIL` and `^SCORE `; no tool greps the banner.  **Replacement:** `" :6878 (ROTL32)")` ->
`" :29822 (rldicrx), :6878 (ROTL64)")`, with a four-line comment above the print quoting the old
label and why (`flags45.diff` hunk 2).  This is the one runtime-visible edit in the diff.

---

## 5b -- `EVERY `want' in this probe is computed from those five lines, never from the tree.'  ->  WRONG RECORD (L4), the weakest of the four

**HEAD says:**

    57:EVERY `want' in this probe is computed from those five lines, never from the tree.

("those five lines" = the rldiclx RTL quoted at :47-51.)  From the table in 5a:

* **computed from those five lines:** the six `want_rldicl` rows (zx32 / rot8 / sh63 / sh32 rldicl,
  vacuous cell, vac neighbour), plus the comparisons behind `census wrong`, `census zero` and
  `naive fix wrong` -- 9 rows;
* **architectural but from OTHER text:** `zx32 rldicr`, `rot8 rldicr` (rldicrx, MASK(0, e) is not one of
  the five lines) and `rc cr0` (a hard-coded CR0=GT, the Rc=1 rule at `:29748`) -- 3 rows;
* **from the TREE:** `bits32 rld bad` wants `"TODO"` and passes only if the transcript contains the
  decoder's own `TODO: rld` text; `neg apparatus` wants `exit1`, gxemul's exit status for an unknown
  machine -- 2 rows;
* **apparatus literals and own counts:** session, live, seed holds, src intact, disasm xcheck, bits32
  live, census run, disasm total, cand session, cr parsed -- 10 rows.  (9 + 3 + 2 + 10 = 24.)

**Disposition: WRONG RECORD (L4).**  Both halves of a capitalised universal are false: "from those five
lines" fails even under the charitable "architectural value wants" reading (the rldicr controls and
`rc cr0`), and "never from the tree" fails on `bits32 rld bad` -- the very row the pass-2 seat already
flagged for pinning the tree's diagnostic (`pass2_20260910/opus_pass2_20260910.md:269-275`, its F1).
Only the narrowest reading -- "the rldicl register-value wants" -- is true, and that core (no rldicl want
is copied from the handler) is the sentence's purpose and holds.  The file's own precedent puts this in
L4: #565 corrected the same docstring's universal "every instruction word placed is disassembled ... and
compared" in place (`[#565, 2026-10-18: NOT every word ...]`, :79-83).  An adjudicator who reads `want'
as "rldicl value want" can grade it OVER-BROAD BUT DEFENSIBLE; the case against that is the two
tree-sourced wants, which no reading of "never from the tree" admits.

**Replacement:** keep `:57`; append the dated bracket in `flags45.diff` hunk 1 (true of the rldicl value
wants; the rldicr controls use rldicrx :29822; `rc cr0` is a literal CR0=GT; apparatus rows want literals;
`bits32 rld bad` and `neg apparatus` want the tree's decoder text and exit status).  It is inside the
docstring, so section U reads it: it adds no `N/M` (re-run of U's own rule on both copies: 2 claims
considered, 0 stale, before and after).

**Siblings (carrier rule 2), not edited:**
* `:88` "TEST-FIRST SHAPE: every `want' is the ARCHITECTURAL value" -- untrue of the two tree-sourced rows
  and the apparatus rows (the rldicr and CR0 wants ARE architectural).  The hunk-1 bracket names it, so
  `:88` needs no edit of its own.
* **Product code:** `src/cpus/cpu_ppc_instr.c:2470-2471` "The wants come from the rldiclx RTL in the
  architecture manual, not from this tree" -- said of the WITNESS, whose rldimi/rlwinm/rlwimi wants come
  from other RTLs and ROTL32 and whose `bits32 rld bad` reads the tree's text.  The same over-breadth, in
  `src/`; outside this diff.
* The witness's own docstring `:35` carries the sentence verbatim; it is frozen evidence -- leave it.

---

## 5c -- the CONTRACT's `every entry was established by a mutant that was built and scored'  ->  WRONG RECORD (L4)

**HEAD says:**

    615:#  is MEASURED -- every entry was established by a mutant that was built and scored,
    616:#  not by reasoning about the row set.

**Count:** CAUGHT 11 entries (`:618-622`, semicolon-separated), NOT CAUGHT 3 (`:625-629`) -- 14, as the
reviewer said.  **Mutants that exist:** `killtable_20260910/mutate.py` -- M_ORIG, M_NAIVE, M_MASKEND,
M_NOAND, M_SH5, M_MB5, M_CR0, M_NOMASK (8) plus BASE and the whole-file HEAD leg; the pass-2 seat added
**M_ROTAMT** (`pass2_20260910/opus_mutate.py`, run only against the 19-row instrument).  No other
emulator mutant exists for this handler: the pass-2 drivers run exactly BASE, M_ORIG, M_SH5, M_MB5,
M_ROTAMT, M_CR0 (+ M_NOMASK); #565's only mutant was the identity-body null medium (its other builds are
the real pre-#522 tree, `02af7f3e`, and HEAD).  (The reviewer's
14-vs-8 count was a pigeonhole argument, not proof -- one mutant can establish two entries -- so each entry
was mapped.)

| # | entry | built and scored? | evidence | status |
|---|---|---|---|---|
| C1 | the mask variable | M_ORIG (`tmp2 \|=` -> `tmp \|=`) | t2 16/24 | MAPPED |
| C2 | the mask bit positions | M_MASKEND (`63-mb` -> `62-mb`: every bit one place over, UB at mb == 63) | t2 20/24 | MAPPED |
| C3 | the mask end bound | **none** -- the loop-bound form `mb <= 62` was "Recorded rather than re-run" (`killtable_20260910/PRETABLE.out:270-274`, `mutate.py:55-60`); pass 2: "by derivation it scores 17/19" (`opus_pass2_20260910.md:130-131`) | -- | UNMAPPED |
| C4 | `&` -> `\|` | M_NAIVE | t2 16/24 | MAPPED |
| C5 | the mask ignored entirely | M_NOMASK | t2 19/24 | MAPPED |
| C6 | the mb-field decode INCLUDING its high bit | M_MB5 | t2 19/24 | MAPPED (the high bit; the low five bits have no mutant) |
| C7 | rotate-versus-shift | **none**; its own parenthetical "(the census sees SHL(all-ones,n) != all-ones)" IS reasoning about the row set | -- | UNMAPPED |
| C8 | the rotate AMOUNT at SH=0, 8, 32 and 63 | M_SH5 for 32/63 (t2 22/24); M_ROTAMT for 8 against the 19-row instrument only (`opus_killtable_SCORES.txt` 18/19, `rot8 rldicl` sole killer); nothing for SH=0 (both are the identity there) | | PARTIAL |
| C9 | the destination width | **none** | -- | UNMAPPED |
| C10 | the `ra`-field decode for ra >= 16 | **none** -- pass 2's "DESTS reach r29, so `& 15` aliases r16..r29 and reds the census" (`opus_pass2:210-211`) is reasoning | -- | UNMAPPED |
| C11 | the record form's CR0 result | M_CR0 | t2 23/24 | MAPPED |
| N1 | `rs`-field `& 31` -> `& 15` escapes | **none** -- `opus_pass2:209-212`, reasoned from SRC = 3 | -- | UNMAPPED |
| N2 | edits conditioned on `ra == 0` | **none** | -- | UNMAPPED |
| N3 | rotate-amount edits that are the identity at all four rowed SH | **none** at 24 rows; class precedent only: M_SH5 escaped the 19-row instrument 19/19 when the rowed SH were 0 and 8 | -- | UNMAPPED (precedent) |

**Tally: 6 mapped, 1 partial, 7 with no built mutant** (C3, C7, C9, C10, N1, N2, N3).  Every unmapped
entry is very likely TRUE by derivation -- the finding is the meta-claim, not the boundary.

**Provenance of the error:** the box was transcribed from the pass-2 seat's section 4, headed
"Measured, the boundary is:" (`opus_pass2_20260910.md:214-226`), which already mixed measured and reasoned
entries; `e777ff06` then strengthened "Measured" into "every entry ... built and scored, not by reasoning
about the row set".  The carrier grades exactly this as L4: *a record that asserts a MEASUREMENT that was
not made*.

**Disposition: WRONG RECORD (L4).**  **Replacement:** keep `:615-616`; append the dated bracket in
`flags45.diff` hunk 5, naming the seven reasoned entries and the mutant behind each of the rest.

---

## The proposed edits -- `flags45.diff` (NOT applied anywhere)

Five hunks against HEAD's `regress/ppc_rldicl_probe.py`, built by `mk_diff.py` (each anchor must match
exactly once) and checked by `verify_diff.py` (`#NNN` is a placeholder for the round that lands them):

* AST outside the docstring: 396 constants before and after, **exactly one differs** -- the banner.  No
  verdict logic, no row, no want changes.
* Section U's rule on the docstring, both copies: 2 `N/M` claims considered, 0 stale.
* Gate 13: no added line ends ` ok`/` FAIL` or starts `SCORE `; the row list, run/green/red counts and
  `SCORE 24/24` are untouched.  Section R's SELFLABEL reads only lines 1-6, untouched.
* ASCII-only, LF-only, compiles; 647 -> 674 lines; longest added line 96.

## Knock-on: `tools/pipeline/check_probe_wiring.py`

HEAD `:1717`, the MANIFEST note for `killtable_20260910/t2/ppc_rldicl_probe.frozen.py`:

    ... byte-identical to the shipped regress/ppc_rldicl_probe.py [#565: AS SHIPPED AT e777ff06 --
    a05660af changed its helper oracles, and #565 its comments and one printed note, since; NL7]

That bracket enumerates every change to the shipped probe since `e777ff06`, so **any** commit of this diff
makes it incomplete (it would still be true of #565's own change).  It should then read:

    [#565: AS SHIPPED AT e777ff06 -- a05660af changed its helper oracles, #565 its comments and one
    printed note, and #NNN its comments and its `wants derived from' banner, since; NL7]

If the banner hunk is left out, drop "and its `wants derived from' banner".  `:1710` (the probe's own
MANIFEST note) stays true.  The working-tree copy of `check_probe_wiring.py` is dirty (+15 lines, another
process); none of those lines touches the rldicl notes.

**Optional, same edit:** `ppcrldiclbanner` (LOW, open) says "A round touching the probe's docstring ... can
close it" -- its WITNESS label (`:2`, `:389`), the `ppc_rldicl_witness.py` usage string (`:101`) and the
split `vacuous cell` note sit in the same file.

**Noticed in passing, outside these four:** `killtable_20260910/t2/SCORES.txt` line 1 still reads
`#521 mk48nvramkill KILL TABLE` -- the wrong-round header the pass-2 seat named (its R6) was corrected by hand
in `t1/` only.  #565's notes and hunk 5 above both cite that file; no record names the header.

## Files (all in this directory)

`FLAGS45.md` (this), `flags45.diff`, `probe_proposed.py` (HEAD + the diff), `mk_diff.py`,
`verify_diff.py`, `enum_rows.py` + `enum_HEAD.out`, and read-only extracts `probe_HEAD.py`,
`probe_e777ff06.py`, `probe_a05660af.py`, `probe_pre565.py`, `cpw_HEAD.py`, `csc_HEAD.py`,
`CHANGELOG_HEAD.md`.
