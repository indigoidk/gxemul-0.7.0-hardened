# #568 (vmedefaultkill) -- REPAIR 1: fix568b + probe REVISION 3 + KILL TABLE 2 -- the builder's spec

DRAFT (2026-10-21 00:4x).  Inputs: the adjudication pass (`vme/f2/`): findings F1-F18, disputes D1-D5, Fable 5.1's F2
answer (`vme/f2/out/fable5_f2.md`); the GLM / Astra / grok F2 answers may still amend this spec -- the coordinator
re-issues it if they do.  Nothing here is built yet.

## 0. Order -- and the one thing to measure FIRST

1. **M_IDATA on the FROZEN rev-2 instrument** (`killtable1_20261020/vme_default_probe.frozen.py`, md5 19de15b3) over
   fix568 (md5 4e3e7fc2) with ONE edit: in the population-2 arm, `if (writeflag == MEM_WRITE)` -> `if (idata)`.
   PREDICTED 34/34 (F1, GPT-6 Astra).  **If it reds, STOP and report: F1 is refuted and rev 3's zero-store row is not owed.**
2. fix568b: `python vme/fix/mk_fix568b.py <fix568> <out>`; record its md5.  Then compare `dev_vme.o` built from fix568
   and from fix568b with `objdump -d` (text only): the ONLY code difference must be the read announce's format string and
   its cast (D1).  Record the comparison output -- "comment-only" is a measured claim, never an asserted one.
3. Probe rev 3 (section 1), its docstring (section 2), and its PRETABLE2 (section 3) -- PRETABLE2 written and saved
   BEFORE table 2's first build; its row list DIFFED against PRETABLE.out + PRETABLE_ADDENDUM_v2.out + PRETABLE1B.txt's
   prescribed rows (the #490 rule).
4. Table 2 (section 4) in a fresh scratch clone, frozen rev-3 instrument, sentinel discipline as table 1.
5. Report; the coordinator then wires gate 14 to rev 3 and runs the block-only gate both ways and the full gate 14.

## 1. Probe REVISION 3 (from rev 2, md5 19de15b3) -- rows

New rows (names <= 15 chars; check the `%-16s` two-space anchor against every existing name it prefixes):

| row | where | want | kills | channel |
|---|---|---|---|---|
| `p2 zero wr` | its OWN short free-running session (do NOT put it inside `announce_pair`: that changes a 26-count literal) | exactly one `WR_LINE % (off, 4, 0)` for an UNTOUCHED population-2 register, 1 `[ vme:` line in total, breakpoint reached, liveness | M_IDATA | announce FORM: write-form `0x0 -- declined` vs read-form `served 0x0` |
| `p2 nw rd 2` | the non-word session: a second pass over its three non-word READS at CODE2 with its own breakpoint and LIVE2 | 0 `[ vme:` lines in pass 2 | M_LATCHLEN4 | pass-2 line count (0 vs 3) |
| `p2 nw wr 2` | same, the three non-word WRITES | 0 lines in pass 2 | M_LATCHLEN4 | pass-2 line count (0 vs 3) |
| `p1 quiet` | the EXISTING free-running population-1 census session: `count('[ vme:')` over its continue text | 0 | M_DFATAL | host text (0 vs 988).  Varies ONLY because that session free-runs at verbosity 0 -- NEVER put it in a stepped session |

* `p2 zero wr`: use `st r0, r3, <off>` -- r0 is hardwired zero, so no seed.  Check the encoder and `unasm`'s expectation
  accept rs = 0.  Pick a population-2 offset NO other row touches (FB: 0x04..0x8c minus those any session uses) so the
  latch is clear at that store.  ONE width (len 4) is enough (F1/FB: the swap tests idata's zero-ness; len is untested).
* `p1 widths` (EXISTING row) gains two LANE-0 accesses at word-aligned population-1 offsets no other row touches:
  `ld.hu` (a destination seeded with the sentinel, which must survive) and `st.b`; want 8/8 faults (was 6/6).  Kills
  M_LANE0H (the `ld.hu`) and M_LANE0B (the `st.b`) -- TWO legs (FB's F10(c) refinement).
* CONTROL split (F8): `CONTROL_ROWS = session, live, neg apparatus, unasm, vbr reset, free neg ctl`.  `cased census`,
  `t1cmp rt`, `free ctl` and `free quiet` become ordinary scored rows.  Write the DEFINITION beside `CONTROL_ROWS`:
  *a row whose unique role is an apparatus or medium proof; a row a product edit can red is scored, never CONTROL.*
* Stop wording (F9, AX's text): replace "(FAILED FOR SOME OTHER REASON)" with neutral, cause-free text, e.g.
  `dependent check not exercised: pass 1 did not complete`, `dependent check not exercised: pass 1 produced no
  announce`, `unexpected stop pc=0x18 before announce verification`.  The rows stay RED.
* `unasm`'s count literal (1426 today) is re-derived BY HAND for the new placed words, never computed from the session
  lists (the probe's own rule).
* Row count: 34 + 4 = **38**.

## 2. Rev 3's docstring (F7, F12)

* Replace "NO KILL TABLE EXISTS FOR THIS REVISION ..." with citations of BOTH table-1 artifacts (KILLTABLE1_VS_PRETABLE.out,
  table1b/KILLTABLE1B.out) and their instrument (frozen md5 19de15b3...) and fix (4e3e7fc2...); KEEP the rev-2 per-row
  predictions as DATED PREDICTIONS, and mark which per-mutant counts in the ROW PLAN were measured and which were never
  built ("a latch set at one constant bit (51)", "a per-direction latch (52)").
* Correct "every session that touches the device opens with `ld r30,r3,0x88`" (the control session reads VBR into r5 after
  an `or`; the cased census into r13).
* Durable citations only: `regress/artifacts/vmedefaultkill/probe_20261020/` (run2_*.out, dmt0_predictions.txt,
  trial2_FIX568.out, explore2_FIX.out, vme_default_probe.v1.py.txt) and the kill-table dirs -- no scratchpad path.
* CONTRACT -- NOT CLAIMED additions: word-aligned narrow/double accesses at the population-2 registers no non-word row
  touches (GL F10); population-2 non-word offsets, cross-width latch reuse, store-data patterns are SAMPLED (AX F9); the
  fault rows pin `return 0`, DMA0 and DMT0, NOT the two `debug()` lines' text (GK, AX); `default:`'s write debug prints
  `(int)idata` -- a pre-existing truncation in host-debug text (FB F12); D7's negative control lives in the table only
  (a neutered typedef has no runtime row; GK F6); any unsampled population-1 interior added as a label (`case 0x91:`,
  GK/FB); population 4 (a cased base at len != 4) is SERVICED by its cased arm with the `vmewidthlanes` lane defect --
  it does NOT fault (AX F3).
* One design sentence (FB): a sub-word start inside a population-2 word maps onto that register's own latch bit
  (0x29 >> 2 == 10 == MASTERCTL's), so if `vmewidthlanes` later services such starts through the arm, one latch per
  register still holds.

## 3. PRETABLE2 -- before the first build

The four checks of the carrier's PRE-TABLE CHECK, as recorded OUTPUT: sibling parity; CLAIM -> ROW for every added
comment sentence (fix568b's rewritten comments included); GUARD FIELD vs BODY FIELD with the partition the body induces
per lvalue; and per row the mutant it kills and the observable that differs.  Plus the DIFF of rev 3's row list against
every earlier prescribed row (table 1's PRETABLE + ADDENDUM + table 1b's PRETABLE1B).

## 4. TABLE 2 -- legs (every table-1 and table-1b leg REGENERATED on fix568b, plus the new ones)

* References: BASE (fix568b + rev 3, expect 38/38), HEAD (expect the population rows red), NULL (the vme `device_add`
  removed), BASE_FINAL after restore.
* Regenerated: M_EXIT M_DROPMCTL M_DROPMISC M_ADD94 M_LATCHONE M_LATCHNOSET M_LATCHRDSET M_LATCHCLRW M_LATCHCLRW_POST
  M_WDEBUG M_RDEBUG M_ANNLEN4 M_TRUNC M_WRFAULT M_LENFAULT M_STORE M_ODATA0 M_SERVED0 M_FLTBREAK M_FLTLEN M_FLTWR
  M_NOONCE M_DROPTCTL M_CAPNARROW M_DROPIRQEN M_T1CMPWRDROP M_ADD90 -- the anchors on the read-announce line change
  under D1 (M_RDEBUG, M_NOONCE, M_SERVED0): update their find-strings, never their intent.
* New: M_IDATA (F1), M_LATCHLEN4 (`if (len == 4)` before the latch SET, the check untouched), M_DFATAL (`default:`'s
  read `debug(` -> `fatal(`), M_LANE0H (`if (len == 2 && (relative_addr & 3) == 0) break;` before `return 0`),
  M_LANE0B (the `len == 1` twin), M_ONENARROW (both arm literals `1ULL` -> `1u`; record the host and WHICH row reds --
  the kill is UB-mediated (FB)).
* Predicted survivors: M_ODATA0, M_SERVED0 (equivalent today).  Every other leg must red at least one row; a leg that
  survives is a RESULT -- report it with the three-way diagnosis (mis-built / dead target / mis-cut row).

## 5. Constraints

READ-ONLY on every project tree except `regress/artifacts/vmedefaultkill/` (results are copied there by the
coordinator unless told otherwise); a scratch clone in WSL /tmp; `.MUTANT` sentinel; `[ gxemul -nt source ]` after every
build; the FROZEN rev-3 copy runs every leg; restore and cmp before clearing the sentinel; no git writes.

## 6. AMENDMENTS from the adjudication answers (applied to the sections above; the later text governs)

### From GPT-6 Astra's F2 answer (vme/f2/out/codex_vmef2.txt, PROCEED WITH CHANGES)
* **F6 -- the gate block needs a pin the score-claims checker RECOGNISES** (`tools/pipeline/check_score_claims.py`: PIN
  = `check\s+"(\S+)\s+rows\s+run"\s+"[^"]*"\s+(\d+)` -- a ONE-TOKEN stem, an UNQUOTED literal).  The block's "vme default
  rows ..." checks are invisible to it (Astra ran it: SCORE_CLAIMS_PINNED=36).  Add, parsing VME_DEFAULT_RESULT=n/N:
  `check "vme_default rows run" "${vres#*/}" 38` and `check "vme_default rows correct" "${vres%/*}" "38"`; THEN raise
  SCORE_CLAIMS_MANIFEST 36 -> 37.  The probe docstring's historical `N/34` claims need a same-line `34-row` era marker
  or the checker flags them stale against the 38 pin.  (Coordinator's part: gate_arm.sh and precommit_check.sh.)
* **F8 -- the CONTROL definition must not claim a cause:** `vbr reset` and `free neg ctl` also depend on product
  behaviour, so CONTROL=FAIL means "a PREREQUISITE failed", never "the apparatus is at fault".  Word the definition
  beside CONTROL_ROWS so.
* **F12 -- keep part of F10(b) in NOT CLAIMED:** `p1 quiet` over the read-only census cannot see the two `debug()` calls
  DELETED (silent either way) nor a WRITE-side `debug(` -> `fatal(` (the census stores nothing).  Extend the quiet count
  over the free-running `p1 widths` session too (it carries st.b / st.h / st.d faults), so write-side promotion is seen;
  the deletion stays NOT CLAIMED.  Leg M_DFATALW (the WRITE-branch `debug(` -> `fatal(`) joins table 2.
* **F13 -- the dependent-red annotation includes `vbr rt` / `t1count inc` under M_DROPTCTL.**
* **D5 -- do not assert the UB outcome:** record M_ONENARROW's compiler, flags, host and the row that reds; no portable
  claim either way.
* **The second-pass rows verify completion and liveness before accepting zero announcements**; an unexecuted pass stays red.
* **D5's pass-1 record is WRONG at default verbosity:** `probe_20261020/explore2_FIX.out` section (b) MEASURED eight
  free-running population-1 faults printing 0 `[ vme:`, 0 memory_rw 'failed' and 0 'exception DATA_ACCESS' lines (the
  stepped counterpart prints 8 of each).  The round's records say so; the CPU does NOT announce a free-running fault.

### From GLM 5.3's F2 answer (vme/f2/out/glm_f2.txt, PROCEED WITH CHANGES; it overturned its own D3 and D4 positions)
* **`vbr reset` stays in CONTROL_ROWS** but under GPT-6 Astra's definition -- CONTROL=FAIL means a PREREQUISITE failed,
  not that the apparatus is at fault -- and the docstring says plainly that a DEVINIT-seed edit reds it (GLM's Q2:
  otherwise a product kill prints as CONTROL=FAIL, the class F8 polices).
* **PRETABLE2 pre-states the NULL leg's expected failures PER CLASS** (CONTROL and scored rows both red by design after
  the split), so the double FAIL does not read as an apparatus fault.
* **PRETABLE2 pins M_ONENARROW's mechanism:** which register owns bit 3 (SLAVELMOD2, 0x0c) and that it is touched before
  MISC in the same session -- a future reorder would otherwise orphan the x86-64 kill silently.
* **Timeout red vs assertion red:** every free-running row's got-text names a timeout (`no-prompt` / `no-breakpoint`)
  distinctly from an assertion mismatch, so a load-induced red is never investigated as a product kill.
* **The contract states the `fatal()` premise:** the decline-and-announce design and `p1 quiet`'s channel rest on
  `fatal()` printing and RETURNING (it does not exit); say so as a premise, with the green tables as its measurement.
* **"Object code identical" stays a measured claim** -- the F2 disposition text that asserted it is corrected to defer to
  the objdump comparison (section 0 step 2).
* Row count 38 holds: `p1 quiet` is a NEW row; `free quiet` remains a separate (now scored) row.
* OFFERED, NOT ADOPTED unless a rig exists: GLM's Q4(2) -- boot the in-tree OpenBSD 2.2 guest under the fixed binary and
  read its `(once)` lines as the reach census (expect four at attach).  No mvme187 OpenBSD boot image is known on this
  host; if none, the comment's reach claim stays a SOURCE-READING claim and says so.

### From Grok 4.7's F2 answer (vme/f2/out/grok_f2.txt, PROCEED WITH CHANGES) -- and the F2 pass's close
* **Per-site neutral wording (D3 refined):** pass 2 after a pass-1 miss -> `dependent check not exercised`; pass 1 completed
  but silent -> `pass 1 silent` (that IS the announce channel, not a non-completion); the non-word session, `p1 census` and
  `p1 widths` -> `unexpected stop pc=0x... before the row's check`.  All stay red.  One sentence stamped everywhere is wrong.
* **Vacuity traps, each a condition the row must meet:** `p2 zero wr` checks the WRITE-FORM LITERAL (never a count of
  `[ vme:` lines -- the read-form line would satisfy a count); it stores r0 and seeds NOTHING into r0 (the m88k core stops
  the CPU when r0 is non-zero); `p2 nw rd 2` / `p2 nw wr 2` run in the SAME process as pass 1 (a new gxemul memsets the
  latch, so a separate process is green under M_LATCHLEN4).
* **Do not write the 7554 figure into the changelog unless it is re-derived there** (grok did not re-derive it).
* **grok's Q4 claim "free-running faults do emit host text (exception DATA_ACCESS at VERBOSITY_INFO)" is REFUTED BY
  MEASUREMENT:** `probe_20261020/explore2_FIX.out` (b) shows 8 faults taken (r1 = 8) and NO DATA_ACCESS line in the verbatim
  continue segment; the stepped (b') run prints 8.  The instrument is preserved beside it as `explore2.py.txt`.
* **F2 CLOSED on 4 of 4 roster seats** (Fable 5.1, GPT-6 Astra, GLM 5.3, Grok 4.7; Argon's pass-2 answer still pending).
  Final: F1 upheld and MEASURED (M_IDATA 34/34 survivor on frozen rev 2); F3 OVERTURNED to "attach reaches four" by all
  four; D1 ALIGN unanimous; D2/D3/D4 upheld with the refinements above; D5 macro FILED.
