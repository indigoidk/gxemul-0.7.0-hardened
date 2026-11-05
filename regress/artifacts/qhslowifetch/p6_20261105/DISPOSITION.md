# qhslowifetch PASS 6 -- disposition (main loop, 2026-11-05)

Seats: codex GPT-6 Astra at `ultra` ANSWERED (codex_codex_qhs_p6.txt, verdict line `CODEXP6QHS: 41 CELLS SWEPT 3 BREACHES 3 FALSE
RECORDS VERDICT:REPAIR`; it read the packet and source, built and ran nothing).  Gemini 4 Argon x2 (jobs p6_qhs, p6_qhs_r2) came back
with NO verdict line -- format misses, not readings (gweb/rounds.log 02:16:50 / 02:17:20 local).  glm-5.3 SEAT DOWN (monthly usage
limit, SEAT_NOTE.md).  grok-4.7 SEAT FAILURE: the HTTP 402 billing wall of 11-05 02:3xZ (owner: continue without
grok, re-fire only when the owner says the balance is topped up).  So this pass rests on ONE answering seat; a seat failure is never
agreement.

## codex's findings, as stated (DERIVED from the source and the rows, not measured)

* B1 -- arm (a)'s guard conjoined with `!(cpu->pc & 2)`: every rowed read-ahead failure has pc bit 1 clear (T ra / T ra me at
  0xfec00008, T ra odd at 0xfec00009), so all 82 rows stay green.
* B2 -- arm (a)'s guard made `translation_readahead && (!(msr & ME) || pc == addr)`: the (unaligned pc, ME set) read-ahead cell has
  no session.
* B3 -- arm (a)'s return preceded by `msr |= (pc != addr ? ME : 0)`: T ra odd has no msr row.
* R1 -- "MSR is rowed on every -T session" (two occurrences) is false of T ra odd.  R2 -- the higher-mask disclosure "no rowed failing
  fetch carries such a bit" is too broad (0x02040004 carries bit 18; 0xfec00008 bits 22-31; `~0x40003` is caught by T blr).  R3 --
  the `|| cpu->pc != addr` failure-test disclosure is obsolete: T ra odd now supplies a successful unaligned -T fetch, so that widening
  is detected (its pc and nonex rows).

## Disposition (by the standing rules; no new ruling is needed)

* B1-B3 are in-bound: each edits arm (a), the predicate dominating the read-ahead return, using operands the block already reads (pc
  alignment, MSR[ME]) -- clause (d)'s DEPENDS-ON enumeration.  If measured (repair 7 measures them FIRST: r7_20261105/B123_NOTE.md),
  they are floor breaches, L2, repaired in-round.
* Pass 5 also found arm (a) x alignment cells (p5_20261105/TRAODD_NOTE.md).  Two consecutive passes, one class: the class-closure rule
  applies -- repair 7 owes the whole arm-(a) read-ahead space in one diff, {pc low bits 00, 01, 10, 11} x {MSR[ME] clear, set} = 8
  cells (three rowed today: T ra, T ra me, T ra odd), each pinning session, pc, nonex and msr, with the contract naming the cells.
* R1-R3 are wrong records (L4), corrected in place by repair 7; R3's widening becomes a measured variant.
* Repair 7 is delegated to an implementer (Opus 5.5 subagent) under the round's scratch-clone recipe; pass 7 follows on its diff.
* The two Gemini format misses are NOT resent against this diff: repair 7 supersedes it, and Gemini's capacity goes to the pass-7
  packet instead.

## ADDENDUM -- Gemini's re-sent reading arrived (the sender re-sent the format-missed job)

`p6_qhs` answered at 02:23 local (gweb/jobs_20261105_rounds/p6_qhs/gemini_web.out; `GWEBP6QHS: 4 ATTACKS 2 BROKEN 2 HOLDS 0 UNSETTLED
DRAFTABLE:NO`); `p6_qhs_r2` failed to send (TimeoutError) -- a seat failure for that replication.  So the earlier line "NOT resent"
is overtaken: the sender resent `p6_qhs` on its own.  Gemini's two items, both DERIVED (not measured), both handed to the repair-7
implementer to MEASURE first and close only if a variant scores 82/82:
* G1 -- arm (b)'s `(pc & ~3) != addr` made `pc < addr`: every rowed `!=` cell has the post-exception pc BELOW addr (isi: 0x400 <
  0x2000), so the "aligned pc differs and pc > addr" cell is unrowed.
* G2 -- arm (d)'s `msr & ME` made `msr`: survives if no session reaching arm (d) has ME clear with another MSR bit set.
* Its "false record" -- "the pre-fix build scores 40 of the 82 rows with the symptom PRESENT" read as "40 rows show the symptom" --
  is an AMBIGUITY, not a falsehood (40/82 green, 42 red, SYMPTOM=PRESENT); repair 7 rewrites the sentence unambiguously.  The pvr
  probe's matching sentence (r2 records: "scores 42 of the 68 rows with the symptom PRESENT") carries the same ambiguity: fix it
  with pvr's pass-3 disposition.

## ADDENDUM -- Gemini's replication answered on its second send

`p6_qhs_r2` (gweb/jobs_20261105_rounds/p6_qhs_r2/gemini_web.out; no verdict line, so the sender scored it exit 1 -- it is a reading
all the same, read in full).  New item G3: arm (a)'s guard conjoined with `&& !cpu->running` keeps all 82 rows green, because every
rowed read-ahead failure comes from a -T halt and memory.c clears `running` first.  The (read-ahead failure, running == 1) cell is the
one the probe already DISCLOSES as measured unreached on pmppc -- Gemini says so itself -- so G3 is inside the stated non-coverage, not a
breach; the repair-7 implementer was told to keep that disclosure and name `&& !cpu->running` among its forms.  Its other checks
(T ra odd, T blr, the 13 sessions, 40/82, PRETABLE_6's "at least" record) HOLD.

## CORRECTION -- the G3 answer's file was OVERWRITTEN; this record is now its only copy

The addendum above cites `gweb/jobs_20261105_rounds/p6_qhs_r2/gemini_web.out` for G3.  That answer (2,971 bytes, 02:37:35 local, no
verdict line) was overwritten when the sender RE-SENT the job at 02:53:00 local: the file now holds a different reading (2,164 bytes,
`GWEBP6QHSR: 5 ATTACKS 0 BROKEN 5 HOLDS 0 UNSETTLED DRAFTABLE:YES`), banked as `gemini_p6_qhs_r2.md` beside this file.  So G3's
substance survives only as quoted above; the two readings of one replication disagree (G3 vs nothing found), and G3 stands as
recorded -- it lies inside the disclosed non-coverage either way.  The sender now keeps an earlier answer in a `prev_<time>/`
directory before any re-send (gweb/run_gweb_rounds.sh, 2026-11-05), and every Gemini answer of this round is banked here.

*Corrected 2026-11-05 (main loop): this file's time-of-day stamps (removed: ~09:3xZ, ~09:5xZ, ~10:3xZ, ~11:1xZ) were GUESSES that ran up to 3.5 hours AHEAD of the clock; the qhs landing-kit agent found them by checking against the files' own timestamps.  The file's own timestamps are the record: created 08:24Z, last written 08:54Z before this note (UTC).*
