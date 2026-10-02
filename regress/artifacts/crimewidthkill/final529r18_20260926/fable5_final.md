FABLE_529_FINAL_ALIVE_0926
CHECKPOINT.md line 1, verbatim: `# CHECKPOINT -- 2026-09-30 11:35 PAUSE POINT, nothing running, codex walled until 14:22 (re-run scheduled 14:27) (087a90 sections rewritten; the peer's sections below are untouched)`

VERDICT: SHIP WITH CHANGES -- the code and every row ship untouched; the three wrong dispositions are all text: the final probe is r20 (one L4 comment r18 left standing), the records still name r18 as the committed bytes, and the carrier replacement carries a second stale sentence.

# Fable 5.1 (claude-fable-5-1) -- #529 crimewidthkill, THE FINAL ADJUDICATION (last seat; GPT-6 Astra confirms), 2026-09-30

## What I checked myself, so READ can be told from VERIFIED

* HEAD is `db8b1a33` (`git log`), and it carries #549 and #553, so the ordering condition is met.  **HEAD's
  `src/devices/dev_sgi_ip32.c` is md5 4088baa8 -- the PRE-FIX file** (`fatal("crime access len = %i!\n", len);
  exit(1);` at HEAD:291-292).  The fix is the WORKING TREE's modified file, md5 8c1d1545 (`git status`: ` M`): width arm
  `:275-320`, the latch `:314-315`, `goto crime_declined` `:319`, the label `:411`.  Every `:NNN` below is into 8c1d1545
  unless marked HEAD.  The packet's instruction "read committed files with `git show HEAD`" therefore points a reader at
  the wrong file for the round's own product file -- see G.
* md5s RUN, not read: r17 2fe7123b, r18 81f8894e, r19 735bba9f; `accepts_block.txt` is byte-identical in r18 and r19
  (`cmp`); the actual `diff` r17 -> r18 is exactly mk_r18's six pairs plus the block replacement, and r18 -> r19 is
  exactly the one pair at r19:60-61.
* r19's base leg LANDED while this seat was writing (11:56:09): `probe_base_r19.raw` ends `FAILING:` (empty) /
  `CRIMEP_RESULT=226/226` / `CRIMEP_CONTROL=OK` / `CRIMEP_DONE`; `MD5.txt` reads 735bba9f / base b5b99e6d / 5f770991 /
  `PROBE_RC=0 WALL=1235s`; 233 lines, 23 `(raw` rows; its diff against table 16's base log is 24 pairs -- lines 84, 85,
  89, 90, 92, 94, 95, 97, 99, 100, 101, 103, 176, 195, 204, 205, 207, 208 (18 `(raw N)` rows) and 108, 109, 110, 112,
  214, 217 (the six note rows) -- and a diff filtered of `(raw` and the three note strings prints nothing.
* The accepts-46 durable copy is complete: `final529r17_20260926/opus_acc46/runs/` holds 102 files, the same count as the
  seat's scratchpad; `PREDICT46.out` (md5 24c95593, 08:48:04) precedes `build46.out` (08:48:41), the capture (08:51) and
  every replay lane (09:12-09:49); `SUM46.out` (d1d57a9e) reads `EXACT=92 DIFF=0 ABSENT=0`; `ANALYZE46.out` gives
  31 / 4 / 1 / 10 and names the four CONTROL-only cells.
* I did not open `seats_20260930/grok_529final.txt`: its brief says this seat rules without seeing it.

## A0 -- r19

The corrected sentence is TRUE of the code.  A 4-byte write at +0x0c has `relative_addr & 4` set, so `:282-284` clears
and stores the LOW word of `reg[1]`; `switch (0x0c)` matches no case (`case CRIME_CONTROL` is 0x008, `:353`) and reaches
`default:` `:396`, whose write branch `:403-407` prints the diagnostic -- the CONTROL arm is bypassed.  Measured:
`opus_pass1_20260913/out/rows_base.out:20` (`sw CTL+0c 0x800 ... dflt=1 ... halted=no`) against `:21` (`sw CTL+08 0x800
... halted=yes`) and `:22-24` ("All machines stopped.").  `mk_r19.py.txt` keeps mk_r18's AST-minus-docstring guard and
refuses on a non-unique find-text; the diff is the one pair.  The r19 base leg is green (above).

Does r19 change any answer?  Not A, B, C, E or F.  It changes D: every draft still names r18 as the committed bytes
(D.1).  And r19 is not the final text either: one comment in the probe is a wrong record (A.7), so **r20 owes**, with its
own base leg; the r18 and r19 legs stand as measurements of these code bytes.

## A -- the six corrected sentences, each read against 8c1d1545 and the logs

1. Stepping (r19:15-17) -- TRUE.  `<RUN>` writes `continue` (`:614-615`); the `free ... said` rows split the transcript
   at "continue" (`:1314-1315`); table 16's base log `:152-161` carries them.
2. TIME's range (r19:174-176) -- TRUE.  `to_add = delta * 66` (`:165`) and the register is written only inside `if
   (to_add >= 1)` (`:167-172`), so TIME after any update is a multiple of 66 and is 0 until the first non-zero delta:
   killtable4's base `:77` reads `(raw 0)`, r18's base `:84` `(raw 66)`, table 16's `:84` `(raw 132)`; "see TIME below"
   resolves to `:191-193` (42 of 800).  "small" is a property of these logs, not of the code, and the sentence says so.
5. The landing bullet (r19:471-473) -- TRUE for the same reason; a store <= 0xffff is 65,535 ticks against the rows'
   0.1 s = 6,600,000-tick threshold.
6. TIME's upper word (r19:491-497) -- TRUE.  `sd +0x38` stores all 64 bits (`:277`); `sw +0x38` has `relative_addr & 4
   == 0` and stores `idata << 32` -- the UPPER word (`:286-287`); `case CRIME_TIME` calls the update AFTER the store
   (`:392-393`) and it truncates to 32 bits only when `to_add >= 1`.  "no row seeds TIME's upper word": the only TIME
   seeds are `sd +0x38, 0x11111111` (`:1445`, `:1553`), upper word zero.
7. Selection (r19:498-501) -- TRUE.  `memory_writemax64` (HEAD `src/core/memory.c:89-109`) serialises the low `len` bytes
   of `odata` (big-endian `buf[len - 1 - i]`), so a refused lb/lh returns bytes 0-1, which `& 0xffff0000` leaves 0.
8. Bit 0 (r19:529-533) -- TRUE.  `opus_r15p2_20260926/accepts_ctl_writes.out` lists `sw/sd 0x1` and `0x201` in S36
   (latch SET) and S50 (latch CLEAR); the arm's only test that sees bit 0 is the relational `idata != 0` (`:377`).  **This
   corrects MY OWN F2 item 12**, which wrote "written by no accepted row"; I take the correction.

Items 3 and 4 (inside the ACCEPTS block): 11 and 15 are named (r19:258, :289); the three-write count is gone -- `p acc
ctl msg` wants 4 (`:1600`), the block says 10, 11 and 15 from repair 13 and 14 from repair 14 (r19:273-274), and the
four writes are in the code (`:1559-1562`).  "r17's equals r16's but for three row notes" I did not diff myself; Astra's
first audit did, independently of the generator (whose normalisation is wider -- D.2).

**A.7 -- one sentence the six do not reach, and it is a WRONG RECORD (L4).**  r19:1584-1589: *"THE CELL NO INSTRUMENT IN
THIS CAMPAIGN OBSERVED ... IT WAS BLIND IN BOTH LATCH STATES ... CLEAR driven only by session 40, SET only by sessions 19
and 26, and all three are oracle-less for this cell."*  Session 19 issues the accepted `lw +0x10` after four refusals
(`:893`, latch SET) and `istat ctl` reads IP2 "set" from its reassert (`:907`); a silent decline of entry 21 there reds it
-- MEASURED, `SUM46.out` row `21 S`: 224/226, red={istat ctl, p acc istat lw}.  The file contradicts itself: its own
ACCEPTS block lists entry 21 as pinned post-latch by `istat ctl` (r19:249).  The codex accepts46 twin named this ("the
'oracle-less' description ... is too broad"; the 4-byte VALUE is what repair 14 added), and r18 acted on the twin's other
qualification (entry 34) but not this one -- an unread finding inside a review the block cites as agreeing.  What was
unobserved was the 4-byte VALUE (the width axis); the SET-state DECLINE was observable all along.

> L4 -> **r20**: comment-only, AST-guarded exactly as mk_r18, the sentence corrected and its correction dated -- e.g.
> "THE 4-BYTE VALUE NO INSTRUMENT IN THIS CAMPAIGN OBSERVED ... The VALUE was unread in BOTH latch states ... The DECLINE
> of the access was observable with the latch SET all along: session 19's accepted lw +0x10 reasserts and `istat ctl'
> reads IP2, so a silent decline there reds it (k21S 224/226, final529r17_20260926/opus_acc46/SUM46.out); with the latch
> CLEAR it was driven only by session 40, which is oracle-less.  [This said "BLIND IN BOTH LATCH STATES ... all three are
> oracle-less" until r20 -- the codex accepts46 twin; this file's own ACCEPTS block already listed entry 21 as pinned
> post-latch by `istat ctl'.]"  r20 owes its own base leg (the F2 condition, unchanged).  **r20 is the closing text
> revision**: a text finding after it that is not a coverage claim a measurement refutes goes into the CHANGELOG as a
> known wrong record, not into an r21.

## B -- the ACCEPTS-46 block

TRUE, and it does not overclaim on any count.  31 + 4 + 1 + 10 = 46 (r19:281-303); the 31 are `ANALYZE46.out`'s set; the
four CONTROL-only cells (5C `rev pc ctl`, 25C `gate line`, 25S `imask ctl`, 41C `devsig`/`dflt ctl`) match
`ANALYZE46.out`; the per-entry red sets at r19:289-294 match `SUM46.out` rows 10, 11, 14 and 15; the historical
23 / 8 / 10 / 5 is kept as a quotation and refuted below it (the quote-what-you-refute form).  The codex twin's partition
is the same partition in set terms -- its 27 + 8 = 35 ROWED are Opus's 31 + 4, then 10 EQUIVALENT, 1 HOST-DIAGNOSTIC,
entry 34 SET-only -- so the provenance line is fair.

One qualifier is missing and should ride in r20 (a clause, not a wrong disposition): *"every one of the 92 cells MEASURED
by a SILENT decline of exactly that access"* -- for the 31 guest-visible entries, `rearm *` (S38) and `latch *` (S52),
which DO hold the access, were served from the inertness capture BY DERIVATION (`opus_accepts46.md`, RAN 4; `SUM46.out`
prints `fromcache=` per cell).  The derivation is sound -- those sessions' rows are two announce counts, a RAM trip and
the CONTROL-text count, none of which a silent, text-free decline can move -- but "MEASURED" should carry it in the
block; Astra's second audit said the same of the records.

## C -- entry 34: clause (e), not floor

Under the rules as I set them: (i) the (d) DEPENDS-ON closure enumerates a joint only where the guarded body's own code
distinguishes it.  The width arm distinguishes `len` in {8, 4, else} (`:275`, `:280`, `:296`) and, at len 4, `relative_addr
& 4` (`:282`); the skipped dispatch distinguishes LABELS (`:322-396`).  Nothing in the enclosing function distinguishes
+0x40 from +0x278: both are `default:`, whose only test is `writeflag` (`:397`).  An offset within a label is not a
body-induced partition.  (ii) The 09-25 clause's axis is {guest-observable label} x {latch}; entry 34's cell is {default,
8W, latch CLEAR}, and that cell is HELD at +0x278 -- k45C 221/226, five rows red (`top8 st+ld`, `top8 clear`, `top4 rhi`,
`top4 rlo`, `hi keeps`).  (iii) The 2026-09-09 join: the selector flows into `d->reg[relative_addr / 8]` in the ACCEPT
arms, which the goto does not skip and the decline body does not read; the decline reads and writes `d->warned` and
prints `relative_addr` -- no join on the offset.  (iv) The contract discloses this exact class twice already (r19:452-458,
the unrowed-slot bullet; r19:459-462, "a fall-through only at +0x40").  So an edit that silently declines only `sd +0x40`
is outside the contract as stated -- clause (e) -- and *"a filter may demand a new row only for a floor cell"* forbids
ordering one.

Hardest on my own rule: the one reading that makes it floor treats the OFFSET as a label, which would make every one of
the 0x280 / 8 slots a floor axis -- the `#392` shape.  Rejected.  The cheap strengthening (seed nonzero at `:1447` and
`:1555`, re-want `acc 40 sw` / `p acc 40 sw` as 0x0a0b0c0d89abcdef) is FILED as `crimecontroldebt` item 8 with its cost:
S55 and S58 carry entries 8-11, 14, 15, 19, 21, 23, 24, 30, 31 and 34-37 (`SUM46.out`'s rerun columns), so every recorded
kill touching them re-runs.  Not in-round.  The packet's own grading stands; the codex phrase "not a measured escape
result" is slightly off -- it IS measured (k34C 226/226 on S55, S52 by derivation) as a non-observation; nothing hangs on
the wording.

## D -- the records

**D.1 WRONG RECORD, all four drafts: the committed bytes are named as r18.**  `changelog529.md:69` ("r18 ... the
committed bytes"), `msg529.txt:11` ("new, r18") and `:30` ("The committed text is r18"), `ledger_529.py:253` and
`:257-258` ("a base leg on the final bytes (final529r18_20260926/probe_base_r18.raw)") and `:266` ("(r18)").  After A0 the
final was r19; after this ruling it is r20.  Each must name the final revision's directory and md5 and ITS base leg, with
the r18 and r19 legs as history (the r18 leg stays cited under F as the r18 measurement).  The `records_drafts.md` header
itself cites `final529r19_20260928/`; the directory is `final529r19_20260930/`.

**D.2 The inlined copy is not the record, by its own words** ("THIS INLINED COPY IS NOT RE-RENDERED").  I checked the
scratchpad originals (`...\8e474f41-...\scratchpad\records\`, 2026-09-28 22:01): the second audit's corrections ARE there
-- the generator sentence (`changelog529.md:82-84`: mk_r17 normalises every eligible row-note argument), "substantive
corrections ... a second audit ... found eight more" (`:96-98`), "A probe comment ... a second probe comment called
`crimebankorder` filed" (`bugs529.md:19-20`), the SUMMARY-versus-EXCERPT logic (`ledger_529.py:123-131`).  Astra's
confirmation must read the RENDERED records -- the commit's CHANGELOG, OUTSTANDING_BUGS and ledger diff -- not the
inlined copy.

**D.3 HIGH is RIGHT, and I take the overturn.**  The rule both seats used (`codexfarm_20260926/adjudication/
fable_brief_f1c.md:30`): *"HIGH -- a guest can end the emulator process, corrupt memory outside a buffer, or hang it,
today."*  A 32-bit `sw 0x800` at +0x08 lands in the upper word (`:286-287`; `crimereg.h:51` "Only lower 14 bits are
valid"), the arm tests the raw `idata` (`:364`) and stops every CPU (`:369-370`); `machine_run` returns false,
`emul.c:1052-1058` (HEAD) breaks out of the run loop unless `debugger_enter_at_end_of_run`, and `main.c:807-821` (HEAD)
returns 0.  The process ends on a store the header says touches nothing.  Measured: `rows_base.out:21-24`.  My MED
argument (`fable_f1c.md:48`: the guest gains no capability it lacks through the modelled 64-bit HARD_RESET) is true and
is a RANKING argument; the rule grades consequence, and Astra (`codex_astraconfirm_farm_f1c.txt`, `crimectllane:F4`) was
right that an available legitimate shutdown does not exempt an unintended one.  The drafts record it exactly that way
(`bugs529.md:20-25`).  One wording fix, `bugs529.md:21`: "ends the emulation in ordinary execution" -> "in ordinary
single-machine execution without `debugger_enter_at_end_of_run` (`emul.c:1053` enters the debugger instead)".

**D.4 Missing from the chain narrative** (`changelog529.md:87-100`), two seat failures the records elsewhere admit: this
seat's first firing of the final packet hit its session limit on 2026-09-26 (the packet's own `:10-11`), and the 09-25
re-ruling's first answer fell back to opus-4-8 after two refusals before the resumed agent answered first-hand
(`rerule_20260925/fable5_rerule_529_20260925.md:3`).  One sentence each, beside the codex and kimi failures already
named -- otherwise "full-roster" reads cleaner than it was.

**D.5 Assembly steps the drafts promise; the confirmation should check them, not read them.**  The working tree still
pins 204 (`regress/gate_arm.sh:1916`, `:1921`, `:1922`) and `tools/pipeline/check_probe_wiring.py:874` still says "141
rows ... pin 141".  When the pin moves to 226, its comment block (`gate_arm.sh:1896-1915`: "no fresh base leg is owed ...
204") must cite the FINAL base leg (r20's) -- the #462 order rule that comment itself invokes.

**D.6 Verified true as drafted:** `crimectllane` is filed nowhere today (0 mentions in `tools/pipeline/ledger.json`, none
in OUTSTANDING_BUGS.md); ledger [154] is the 2026-09-18 fable5 entry citing the volatile brief, which
`ledger_529.py:145-152` repairs; `flagship_20260918/` holds the answer and its brief; POSTTABLE16's dated CORRECTIONS
section carries item 13 a-d; the drafts' `M7` / `M8` 223/226 are at `POSTTABLE16.out:23-24`; `ctl0c_discharge_20260917/
VERDICT.md` reads 204/204 -> 202/204 with exactly the pair red; the witness is 3/15 -> 15/15.

## E -- the carrier's Q3 clause

**ADOPT the codex replacement, with THREE corrections, not one.**
(a) The packet's: "INTMASK and CONTROL-write label-swaps remain individually owed measurements under the ruling" -> "were
measured DETECTED: table 13a `M7_intmasklatch` / `M8_ctllatch` 201/204 each (Astra's 2026-09-28 recount; the CHANGELOG
draft cites the same), table 16 223/226 each (`POSTTABLE16.out:23-24`)".
(b) A second stale sentence the packet did not find: *"The demonstrated remaining holes are TIME and REV with the latch
SET: `M3_timelatch` and `M5_revlatch` escape at 204/204"* -- present tense in a clause that is read in the present, and
false since repair 15: table 14 214/218 both, table 16 222/226 both (`POSTTABLE16.out`; Astra's recount agrees).  Write
it as history: "were the demonstrated holes at repair 14 (204/204, `repair14_20260916/POSTTABLE.out`), closed by repair 15
(table 14 214/218; table 16 222/226)".
(c) Add the sentence this round measured and the next reuse will meet: "An OFFSET within one label is not an axis unless
the body distinguishes it: `#529`'s entry 34 (`sd +0x40`, latch CLEAR) is unrowed while its label cell is held at +0x278
-- the unrowed-slot class, clause (e)."
Everything else in the codex text is more faithful than mine: my "it reads, writes and tests nothing" is false of the
repair path (it reads and writes `d->warned` at `:314-315` -- the omission is the JUMP); "the guard's own partition" is an
undefined formula where the pass-11 definition (repair-path reads, jointly reachable) is the defined one; the
third-disjunct form removes the contradiction with the 2026-09-09 fallback; DISCHARGE as measured DETECTION per label,
state-conditioned variants included, is the ruling's meaning; and "table 11's K2 PER-ROW" is the precise form.  Keep the
one-dispatch bound and the first-reuse check.

## F -- the base leg on r18

TRUE as stated, verified against the files: `MD5.txt` (81f8894e / b5b99e6d / 5f770991, `PROBE_RC=0 WALL=1258s`); the raw
ends `FAILING:` (empty), 226/226, OK, DONE; `DIFF_vs_table16_base.txt` has 24 pairs -- 18 `(raw N)` rows (84, 85, 90,
91, 92, 95, 96, 97, 99, 100, 101, 103, 176, 195, 204, 205, 207, 208) and 6 note rows (108, 109, 110, 112, 214, 217) from
the three strings mk_r17 rewrote; 23 `(raw` rows in the log = 22 TIME + `gate hardint` (`:79`, "raw 32"); the four
unchanged TIME rows are `time sb`, `time sh`, `tl sb`, `tl sh`; no want, got or verdict column differs.  r19's leg
(above) has the same shape: 24 pairs, a different subset of TIME rows (89, 90 and 94 differ there where 91 and 96 did for
r18 -- run-to-run, by construction), the same six note rows, nothing else.

## G -- WHICH DISPOSITIONS ARE WRONG: THREE, all text; plus four changes that are not wrong dispositions

1. **(A0 / D) "r18 ... the committed bytes"** in all four drafts and the ledger `regress` entry -- wrong after A0 and
   wrong again after this ruling.  Change: name the final revision (r20), its directory and md5, and its base leg; the
   r18 and r19 legs as history.  Lines checked: `changelog529.md:69`; `msg529.txt:11`, `:30`; `ledger_529.py:253`,
   `:257-258`, `:266`; `records_drafts.md`'s header (`final529r19_20260928/`).
2. **(A) "r18 = r17 plus six corrected sentences and the block" is not the final text.**  r19:1584-1589 is a wrong record
   about coverage, refuted by `SUM46.out` row `21 S` and by the probe's own ACCEPTS block (r19:249), named by the cited
   codex twin and left standing.  Change: r20, comment-only, AST-guarded, dated; its own base leg; B's derivation clause
   rides with it.  Lines checked: r19:893, :907, :249, :1584-1589.
3. **(E) "ONE PART OF IT IS STALE": two parts are.**  The M3 / M5 "remaining holes" sentence is false since repair 15
   (table 14 214/218; table 16 222/226).  Change: adopt with corrections (a), (b) and (c).  Lines checked: the third
   paragraph of the replacement block in `codexfarm_20260926/codex_carrierq3.txt`; `POSTTABLE16.out` (M3 and M5 at
   222/226).

Not wrong, but change the wording or the instruction: (i) B's "MEASURED" gains the derivation clause; (ii) D's "ordinary
execution" gains the single-machine / no-debugger qualifier; (iii) D's chain narrative gains the two seat failures;
(iv) **the packet's "read committed files with `git show HEAD`" is the wrong tree for the round's own product file** --
HEAD's `dev_sgi_ip32.c` is the pre-fix 4088baa8, and every `:NNN` in the probe, the Opus report and this ruling is into
the working tree's 8c1d1545.  Astra's second audit read HEAD ("Source citations refer exclusively to db8b1a33": its
`:279`, `:295`, `:326`, `:337`, `:342-343` are HEAD's numbers) -- harmless for the lane, which the fix does not touch, but a
confirmation of the DECLINE against HEAD finds no `crime_declined` and no latch; the grok brief inherited the same
instruction.  Point Astra's confirmation at 8c1d1545, or at the committed file after the commit.

Right and unchanged: C (clause (e)); D's HIGH; F.

**Conditions of SHIP, in order:** r20 generated (mk_r20 with the AST guard) and its base leg green beside its `MD5.txt`;
the four records re-rendered to r20 and read by Astra in rendered form; the carrier clause landed with (a)-(c); the
assembly's pin moves citing r20's leg; #549-first is already satisfied at HEAD.  No row is owed; no product code changes;
`dev_sgi_ip32.c` stays 8c1d1545.

-- Fable 5.1, flagship seat, adjudicating last; read-only except this file; nothing built or run.
