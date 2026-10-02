VERDICT: 1 adopt, 3 adopt-with-changes, 0 reject, of 4 answers

FABLE_FARM_f1a_ALIVE_0926

First line of `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`, verbatim:
`# CHECKPOINT -- 2026-09-26 09:35 (087a90 sections rewritten; the peer's sections below are untouched)`

CODEX FARM 2026-09-26 -- FABLE ADJUDICATION, batch f1a (Fable 5.1, Agent-tool seat, adjudicator hat)

**What I read and how.**  Everything below is against committed HEAD `8ea26abb` via `git -C GXEMUL-SEC show HEAD:<path>`
(the working tree carries a staged `OUTSTANDING_BUGS.md` and `ledger.json` and an unstaged 20-line comment addition to
`src/devices/dev_pcc2.c`; `regress/gate_arm.sh` is CLEAN now although all four answers say it was modified when they ran).
Manuals under `_scratchpad/*.txt`; the OpenBSD guest source at `C:\DocumentNoSnc\CC\GXEMUL\_guest-src-openbsd22\` (project
root, not under GXEMUL-SEC); upstream's own `doc/machine_mvme88k.html` at the project root.  I built nothing, ran no
emulator, and wrote only this file.

**Seat identity, recorded because it matters for the confirmation step:** all FOUR briefs were REFUSED by GPT-6 Astra
(content filter, `access_programs.c` refusal text in every `.launch.log`) and all four answers are from the
`gpt-daybreak-blue-latest` fallback at ultra.  So the seat that is to confirm these dispositions has not yet read the
material; record the answers by their actual model, not as Astra.

**A premise every answer shares, checked once:** HEAD is `8ea26abb` (`git log -1`), so "at HEAD" in all four means the
same tree I checked.

---

## 1. `sgirekills` -- **ADOPT**

**Answer's verdict:** "Re-scope to five reachable MTE command exits and witness STIPPLE first."

**Premises checked, all TRUE at HEAD:**
* 13 `exit(1)` texts in `src/devices/dev_sgi_re.c`; seven in comments (`:273 :315 :453 :457 :931 :1187 :1493`); six
  active at `:1498 :1506 :1582 :1587 :1598 :1720` -- re-derived by `grep -n` and reading each hit.
* `:1705/:1710/:1718` -- `if (len == 4) ... else if (len != 4) ... else { fatal(); exit(1); }`: the third arm is dead
  (exact complements).  Owned by `sgimtewidth` at `OUTSTANDING_BUGS.md:14719-14740`, which also records the
  do-not-resurrect trap.
* Trigger values: `src` at `:1480` IS the selector `(mode & 0xe0) >> 5` (the answer's table tests the variable `src`,
  not `src_tlb`; both hold the same value, `:1501`), `depth = 8 << field` at `:1479` (field 3 -> 64, unnamed by the
  header), masks at `crmfbreg.h:253-273`, `MTE_MODE_STIPPLE 0x400`, `MTE_MODE_COPY 0x800`, `MTE_TLB_LIN_A 4`.  `sw 0x400`
  reaches `:1498` with every other register at reset (`memset` at `:848`; the STIPPLE test precedes the `src` test and
  the switch), so it is state-independent.  `sw 0x60` -> src 3 > `MTE_TLB_C`; `sw 0x810`, `sw 0x110`, `sw 0x10` (reset
  BYTEMASK 0 != 0xffffffff at `:1596`) as stated.
* Path: `machine_sgi.c:500` `dev_sgi_re_init(..., 0x15000000)`; `dev_sgi_re.c:854` MTE at `+0x3000`; `:1689`
  `startFlag = relative_addr & CRIME_DE_START` (`crmfbreg.h:316`, 0x800); `:1807-1808` `do_mte_transfer()` called
  synchronously inside the guest store.  KSEG1 `0xb5003800` -> physical `0x15003800`.
* `src` is consumed only under COPY (`:1564-1568`), so the `:1504` guard kills a FILL over an irrelevant field --
  the answer's split-the-predicate point holds.
* `sgi_re_width_probe.py` has NO `ld kill` rows (only comment history at `:29 :33 :46 :48 :370 :527`); `gate_arm.sh
  @HEAD:1418` row list carries none, `:1457-1460` pin 46/46/0, `:1432-1438` say the six rows are gone.  It excludes
  `DEVICE_ACCESS(sgi_mte)` at `:54-57`.
* `sgi_mte_fill_probe.py:27` "STILL NOT WIRED INTO A GATE" -- and `gate_arm.sh@HEAD` never names it (only
  `gate_hygiene.sh:417`'s harness allowlist does).  Its `:58 :86-87` disclose the LINEAR deaths; no row drives
  `dst_tlb` 4/5 (every `fill()`/copy row writes dst selector 0/1/2, `:296-348`).
* `OUTSTANDING_BUGS.md:18842/18847` assigns `sgirekills` FIVE command exits; `:18114-18142` records `#513` (five
  ACCEPTs + TEX latched decline, 30/44 -> 44/44); `:14259-14260` scopes the row to "inside a `DEVICE_ACCESS`", which
  is lexically false for the five (all in `do_mte_transfer()`, a plain function -- reached synchronously from the
  callback, so the practical claim survives).
* Ledger `@HEAD:29730` witness field still names the six `<site> ld kill` rows (they no longer exist -- the row has NO
  valid witness pointer at HEAD); `:30155` (codex research) says the re-pin blocker is discharged; `:30159`
  hold_question still asks TEX accept-vs-decline, which `#513` settled (decline); `:30160` state_note opens on the
  obsolete "six rows assert the host still dies" obligation and its own later text says `:1463/:1471/...` -- the sites
  are at `:1498/:1506/:1582/:1587/:1598/:1720` today.
* Precedents cited: `:1491-1494` (exit commented out, fatal kept), `:1133-1146` (latched decline, `SGIRE_W_PRIM_OP`),
  `:1214-1219` (`goto de_declined`), `:1855-1857` (silent ignore), `:264-269` "probably not correct", next free latch
  bit `1 << 13` at `:165-169`.  Device signature `0x1e000000` = `CRIME_DE_IDLE|SETUP_IDLE|PIXPIPE_IDLE|MTE_IDLE`
  (`crmfbreg.h:423-426`, served at `:1844-1848`).  Liveness control claim ("reset TLB A is invalid, one-pixel tiled
  fill returns harmlessly"): `horrible_getputpixel` `:258` `re_tlb_a[0] << 16` = 0, bit 31 clear, `:312-317` returns
  before any write.  TRUE.

**Premises found FALSE:** none.

**Ruling: ADOPT.**  The re-scope is what `OUTSTANDING_BUGS.md:18847` already says; the option analysis per site is the
right one (latched DECLINE of the WHOLE command before any PUT, distinct bit per site because the STIPPLE and SRC tests
precede the switch and are not mutually exclusive with the LINEAR-arm tests in one session; IMPLEMENT only where a
CRM source arrives, and none is on disk -- the answer's manual grep is right, no `_scratchpad` text covers the MTE).
No closure is proposed, so the closure conditions are not in play.

**Next action (one round, HIGH):** run the rung-3 witness FIRST -- one session per site on unmodified
`-E sgi -e ip32 -M 64`, starting with `sw 0x400` to `0xb5003800` (STIPPLE, state-independent), using
`sgi_mte_fill_probe.py`'s existing harness, `live` and `devsig` controls (`:357-365`), expecting `exit1` with
`[ sgi_mte: unimplemented MTE_MODE_STIPPLE ]` as attribution; preserve under `regress/artifacts/sgirekills/`.  Then
the design brief from `tools/BRIEF_TEMPLATE.md` with `do_mte_transfer()` inlined in full (it is `void`; the caller's
`memory_writemax64` tail at `:1810-1811` is untouched by a decline inside the callee), and the records corrections
the answer's section 6 lists: re-point the ledger `witness`, clear the discharged TEX `hold_question`, demote the
state_note head, retitle to "five command exits (+ one dead width arm owned by `sgimtewidth`)".  Priority **HIGH** --
five one-store guest kills on an in-tree machine, today.

**What the answer missed (mine):**
* Two UNLATCHED `fatal()`s a guest drives with the same START bit: `:1492` (every odd `dst_y_step` transfer) and
  `:1680` (every `dst_tlb` 3/6/7 transfer).  Not kills; guest-drivable floods -- the `floodclass` shape.  The new latch
  design should take them in the same bitfield or say why not (LOW).
* The de-escalation clause's ACCEPT rows are owed for the LINEAR arm: no in-tree row exercises a legal LINEAR fill
  (depth 8, COPY clear, bytemask `0xffffffff`), so a decline that over-refuses would go unnoticed; and the resulting
  detector needs a GATE HOME -- `sgi_mte_fill_probe.py` is unwired, which is the `wiringcliff` class this tree has
  already paid for once (`mk48`, `gate_arm.sh:1743-1747`).
* Reachability at rung 4 is not argued either way; the LINEAR arm's own comments (`:1604-1635`) say the O2 PROM
  drives it, which makes a bytemask-0 or depth-16 PROM fill a plausible boot-time kill on a real image.  Nothing here
  measures it; the rung-3 witness is the right first step.

---

## 2. `pcc2widthkills` -- **ADOPT WITH CHANGES**

**Answer's verdict:** "Finish and verify pass 14, then close/retitle the row -- do not edit `dev_pcc2.c`."

**Premises checked, all TRUE at HEAD:**
* Twelve `len != 1 && writeflag == MEM_WRITE` guards at `dev_pcc2.c:508 519 541 553 574 611 620 634 648 668 687 711`;
  each calls `pcc2_width_decline()` (`:462-469`, per-instance latch) and `break`s; reads served by the `memcpy` above
  the switch (`:482-495`).  Zero `exit(1)` in any guard; the file's sole `exit(1)` is `:435` (interrupt-line
  `default:`), unrelated.
* Pre-fix: `b78bb0f^` shows ten `exit(1)` guards and two `#119` warn-once statics (IPL, MASK) -- "ten of twelve" was
  historically right and is zero-of-twelve now.  `b78bb0f` (2026-09-03) and `70761347` (2026-09-05, "pass 14 OWED") exist
  with those subjects.
* Gate: `gate_arm.sh@HEAD:1669-1692`, 251 rows, both halves pinned (`:1689-1691`).  Witness artifact
  `regress/artifacts/pcc2widthkills/witness_20260903_PREFIX.out` reads 4/10 with `half rd/word rd/half wr` `exit1`.
* Ledger `:32459` `commits: "b78bb0f"` only; `:32460-32461` title/witness describe the PREFIX build; `:33948`
  hold_question still gives the 5/7 split and asks for the ten-arm edit; `:33949` state_note carries "pass 14 is
  drafted (fix_pcc2_p15.py: +18 rows -> 269, 8 mutants, PRETABLE_pass14, plus a pre-repair breach witness)";
  `:33950` "reopened ... pass 14 owed at the 2026-09-05 commit".  `OUTSTANDING_BUGS.md:15011-15021` (`pcc2w14`) says
  the same and names the prerequisite `pcc2defaultkill`, FIXED as `#501` at `:15023-15032`.
* Alignment: `cpu_m88k_instr_loadstore.c:169` `addr & (LS_SIZE - 1)` -> a guest 8-byte access needs an 8-aligned
  address and no guard start is 8-aligned; only SCCERR (`0x1c`) is 4-aligned; GENCTL (`0x02`) takes a halfword only.
  So `OUTSTANDING_BUGS.md:14166-14170`'s "plain aligned 4-byte read of `PCCTWO_GENCTL`" is impossible (the c040
  probe's own comment at `:323-326` measured the misalignment exception).  The answer's correction stands.
* Operator-only sites: debugger `put b` uses `NO_EXCEPTIONS` (`debugger_cmds.c:1506-1507`) and PCC2 is `DM_DEFAULT`
  (`:829-831`), so `memory_rw.c:584` skips the callback -- `pcc2_default_probe.py:115` measured exactly that;
  `put h/w/d` go through `store_16/32/64bit_word` with plain `CACHE_DATA` (`memory.c:782 :806 :827`) and reach it.
* `gate_arm.sh:1670-1671` "Twelve width-guard blocks ... ended the host" -- overclaims (ten did); `pcc2_width_witness.py:16-20`
  itself says ten.  `pcc2_width_probe.py:421-434` carries the corrected six/six census.
* Manual: `vmesbcp2.txt:4653-4656` (8/16/32-bit CSR access), `:4857-4872` GENCTL, so a host exit and a guest fault
  are both wrong for a documented width; COMPOSE is `pcc2widecompose` (`OUTSTANDING_BUGS.md:15400-15424`) with its
  reopen condition.

**Premises found FALSE:** none.

**Closure conditions:** the shipped fix (`b78bb0f`) has a measured, gated detector (251 rows; kill tables under
`regress/artifacts/pcc2widthkills/`), so "fix shipped with a measured detector" is met -- EXCEPT that the row's own
record makes pass 14 a floor-shaped obligation on that detector (two one-sided generating-set cells and an uncrossed
INT x other-timer axis, `OUTSTANDING_BUGS.md:15012-15019`).  Closure is available only when pass 14 has landed.

**Ruling: ADOPT WITH CHANGES.**  The changes:
1. "Finish and verify pass 14" must include pass 14's OWN valid pass 2 (the repair-chain rule: a floor-bound diff owes a
   pass, closing on the first VALID pass with zero surviving breaches AND its denominator stated) -- not just the
   8-mutant table.
2. The gate pin moves to 269 in BOTH halves (`gate_arm.sh:1689-1691`) in the same commit as the 18 rows; the row-name
   list at `:1684` gains the 18 names.
3. Records in the same commit: `commits` field -> `b78bb0f, 7076134, <pass-14 sha>`; retitle from "TEN live width
   kills" to the direction split, with the PREFIX witness kept as the pre-fix witness; fix `gate_arm.sh:1670-1671`
   (ten of twelve killed; two were `#119` latches); correct `OUTSTANDING_BUGS.md:14166-14170` in place (halfword at
   GENCTL, word at SCCERR only, no 8-byte guest reach); `:14188-14190` "no mvme88k rig" is superseded for PROBES only
   (see item 4 under `vmedefaultkill`: there is still no OS boot rig).
4. Downgrade `sev` from `high` on retitle: no guest-reachable defect remains at HEAD.

**Next action:** the pass-14 detector round (+18 rows to 269, eight mutants, pre-repair breach witness, its own pass 2),
then close.  Priority **LOW** on this brief's scale (no guest-visible defect today; latent detector coverage) -- but
it is an L2-class obligation the queue's own rule says to discharge, so it goes behind the live HIGH rows, not off
the list.

**What the answer missed (mine):**
* `pcc2_width_probe.py:811-816` (`c040ok()`): its comment still says a GENCTL lane carrying 0x04 "would kill the host
  through reassert_interrupts()" -- stale since `9fa07fe`, same class as the `:399-401`/`:1364-1365` texts the answer
  did flag.  The assertion itself is still right (it keeps the C040 announce/suppression out of width rows).
* The pass-14 draft lives in the ledger note as `fix_pcc2_p15.py` with no path; before that round starts, find or
  re-derive it -- a drafted-but-unlocated artifact is the volatile-path class.

---

## 3. `pcc2c040kill` -- **ADOPT WITH CHANGES** (a CLOSE; held to the closure conditions)

**Answer's verdict:** "normalize the records, split the GENCTL-mask debt, and close pcc2c040kill as fixed."

**Premises checked, all TRUE at HEAD:**
* Historical kill: `9fa07fe^:src/devices/dev_pcc2.c:271-276` -- `if (GENCTL & PCC2_C040) { fatal("pcc2: C040 interrupt
  assertions... TODO\n"); exit(1); }` as the FIRST statement of `reassert_interrupts()`.  HEAD: the test is at
  `:390-397`, sets `assert = 0` after the IPL recalculation, latched on `PCC2_W_C040`; `:399-402` assert/deassert.
  `fatal()` returns (`debugmsg.c:384-391`).
* Ten `reassert_interrupts(d)` callers at `:438 455 514 606 629 643 657 664 677 717`; GENCTL resets to 0 (`:803`); the
  only store to offset 2 is `:513`; the counter `memcpy` arms start at 0x04+ (`:531-537`) and CHIPID/CHIPREV writes
  are dropped (`:499-505`), so the GENCTL arm's own call at `:514` was always the first hit.  Ten callers, one
  decision, zero kills -- correct.
* `:513` `d->pcctwo_reg[relative_addr] = idata;` -- unmasked.  `vmesbcp2.txt:4866-4870`: word-view bits 14..11 are `R`
  (byte bits 6..3), C040/MIEN/FAST/DR0 `R/W`.  So `st.b 0x78` sets four read-only bits and `:482-484` reads them back.
  A live MED defect (guest-visible, contrary to the manual), NOT a kill.  The parent's own ledger `note` already
  names it as "A SECOND, SMALLER FINDING" with no row id; `grep` finds no row for it (only `pcc2genctlc040alias`,
  ledger `:42511`, which is the header trap).
* `mvme_pcctworeg.h:134-143`: `PCC2_GENCTL_C040 0x03`, annotated WRONG, zero consumers in `src/` (git grep).
* Detector gate `gate_arm.sh@HEAD:1721-1737`, 18 named rows, both halves pinned.  Artifacts: `witness_HEAD_20260907.raw`
  3/4 with `c040 kill died(exit1)` and the pre-fix attribution text; `witness_FIX512_final.raw` 7/7;
  `r535_20260918/opus535/r2_BASE.raw` 18/18; `fbd5/q2_20260923/r3f_20260923/gate_arm/pcc2_c040.log` 18/18.  All
  tracked (`git ls-files`).
* `:374-378` says `assert = 0` -> `return` "is a one-token mutant every shipped row passes";
  `ctlq_20260909/repaired_M_return.raw` reads `RESULT=14/16` with `c040 noassert`/`c040 noassert2` FAIL.  The HEAD
  comment is a wrong record; the correction is the unstaged 20-line working-tree edit (another round's in-flight
  work), NOT committed.
* `:380-386` attributes the "via the EIPL* pins at the level programmed in the SCSI Interrupt Control Register"
  wording to the GENCTL page; that sentence is `vmesbcp2.txt:4395-4399` (the 53C710 section); the GENCTL page's own
  C040 text is `:4908-4915`.  Wrong attribution, right conclusion.
* `OUTSTANDING_BUGS.md:21831-21834`: assess 9/9 REAL-AND-RIGHTLY-FIXED (2026-09-18); `:21840-21842` `#535`, 18 rows,
  gated.  Ledger: assess 9 distinct seats, review 9, design 7 (no agy, no opus5 -- those panels predate the
  2026-09-15 agy directive), research 1 (codex); `closure` block empty; the `hold_question` (`:35105`) WAS answered
  by the flagship pass of 2026-09-09 (entries "RULING on part (a)" and "RULING-CELL-SETTLED") and then partly
  overturned by `#535`'s measured MIEN|C040 cell -- it is discharged with that history, not open.
* Children: `pcc2c040ctlq` `in work` (`:42895`), commit `1f2b27a`, ONE entry, its state_note says it "owes its own
  pass on the diff per the repair-chain rule, batched into #518's pass-2 window" -- the ledger row records no such
  pass; `pcc2c040assertrow` `held` by OWNER DECISION 2026-09-18 (`:42497`: re-fire four packet-fed seats on the real
  material); `pcc2c040mienannounce` closed (`bb8efbf`); `pcc2c040latchswap` open MED with a MEASURED 17/17 escape of
  the shipped detector; `pcc2c040debugchan` open LOW, MEASURED 17/17.
* Probe rows the mask fix would move: `pcc2_width_probe.py:693-696` `rb genctl lo` expects `0x11` (bit 0x10 is
  read-only per the manual; masked, it reads `0x01`); `pcc2_c040_probe.py:224` `BENIGN = 0x10` (control still survives
  under a mask; its prose must stop implying 0x10 is writable); `pcc2_default_probe.py:239-240` round-trips `0x82`
  (DR0|MIEN, both writable) and stays green.

**Premises found FALSE:** none.

**Closure conditions:** MET on the mechanical test -- a fix shipped (`9fa07fe`, plus `1f2b27a` and `bb8efbf`) with a
measured detector (pre-fix red / post-fix green on the same script, kill tables, gated at 18 rows), assess 9/9.  Not
an OVERTAKEN closure, so the three-condition test does not apply.  I looked for a live defect the closure would hide
and found none that is not either (a) the MED mask defect the answer splits out, or (b) an already-filed child row.

**Ruling: ADOPT WITH CHANGES.**  The changes, each a condition of the closure commit:
1. File the GENCTL read-only-bits defect as its own MED row BEFORE closing (the parent's note is the only place it
   lives today); its fix is `(old & 0x78) | (idata & 0x87)` per the VECBASE/`dev_sii.c` idiom, and its round revises
   `rb genctl lo` and the two prose sites above.
2. Record the disposition of `pcc2c040ctlq`'s owed pass 2: either cite where `1f2b27a`'s diff was reviewed (the ledger
   row has nothing after its one implement entry) or fire it.  A parent closed over a follow-up whose floor-bound diff
   had no pass is the repair-chain rule's exact failure.
3. Name in the closure note, by id: `pcc2c040ctlq` (in work), `pcc2c040assertrow` (held, owner re-fire owed),
   `pcc2c040latchswap` (MED, measured escape), `pcc2c040debugchan` (LOW, measured escape), `pcc2genctlc040alias`, and
   the new mask row -- so a reader never sees a clean close over five open descendants.
4. Land the records L4s: the `:374-378` false sentence (the correction exists uncommitted -- coordinate with its
   owner rather than duplicate the edit), the `:380-386` attribution, `pcc2_width_probe.py:399-401 :1364-1365`,
   `OUTSTANDING_BUGS.md:15341-15356` (present-tense kill, "witness not yet run"), `:18520-18532` (16 rows -> 18).
   Mark the `hold_question` discharged with the 2026-09-09 ruling + `#535` history.
5. Run `check_stage_panels.py` on the closure commit rather than asserting the design stage's 7 seats pass; if it
   reds, that is the owner's call (the panels predate the agy directive), not a reason to skip it.

**Next action:** a records commit doing 1-5, then close the parent as FIXED with witness `probe:regress/pcc2_c040_probe.py`.
Priority **LOW** for the closure act; **MED** for the mask defect it files.

**What the answer missed (mine):**
* The order matters: closing the parent while `dev_pcc2.c:374-378` still states a false measured-sounding negative in
  the shipped comment would make the closure a wrong record on its own product line; the correction must land first
  or in the same commit.
* The `pcc2_c040_probe.py:3-13` DEFECT header is written in the present tense ("The C040 test is the FIRST thing in
  that helper") -- fine as a witness's pre-fix description, but a "since `9fa07fe`" line would stop it reading as a
  live claim.

---

## 4. `vmedefaultkill` -- **ADOPT WITH CHANGES**

**Answer's verdict:** "build the missing MVME187 rung-3 witness, then split unsupported-access FAULT from register-lane
handling."

**Premises checked, all TRUE at HEAD:**
* `src/devices/dev_vme.c:137-143`: `default:` with two direction-specific `debug()` calls and ONE `exit(1)` at `:143`;
  `:62-66` preload; the switch cases are `0, GCSRCTL, TCR, T1CMP, T1COUNT, TCTL, IRQEN, IRQL3, IRQL4, VBR` (`:70-135`)
  -- ten.  `mvme88k_vme.h:46-81` defines 36 word registers `0x00..0x8c`; `:40-42` "rather insane access rules".
  Arithmetic 4086 = 3952 + 26 + 108 and 1014 aligned uncased starts in six runs -- re-derived, correct.
* `debugmsg.c:365-376`: `debug()` early-outs at default verbosity while executing (`v` goes -1); single-step adds one
  and the message prints -- so the invisibility needs a FREE-RUNNING witness, as the answer says.  `fatal()` has no
  early-out.
* `machine_mvme88k.c:94-96` attaches `vme` at `VME2_BASE`; `:106 :120 :123` install `unreadable` three times; `:127-135`
  MVME188/197 are TODO-only.  `memory_rw.c:584-585` skips the callback for `no_exceptions` on a `DM_DEFAULT` device
  (`dev_vme.c:166`) -- a debugger peek is not a witness; `:595-624` converts `return 0` to `m88k_exception(...DATA_ACCESS, 0)`.
* VBR seed `VME2_SET_VBR0(6) + VME2_SET_VBR1(7)` = `0x67000000` (`:161-162`, `mvme88k_vme.h:257-260`).  `0x30` is
  `VME2_DMACTL`, uncased.  Big-endian `memory_writemax64` (`memory.c:104-108`, `cpu_m88k.c:130`) -> the ledger's
  "byte read at 0x89-0x8b returns 0x67000000 under a decline" is wrong (it would return 0x00); the answer's correction
  stands.
* Ledger `vmedefaultkill` note (`:45105`, 15 KB): opens with DECLINE + promoted announce, then records "OWNER RULING
  2026-09-11: FAULT -- `return 0`", then the reopened codex verdict "FAULT for the unsupported-access fallback; handle
  register byte lanes separately", and CONSOLIDATES what is still owed: a population-3 (lane) decision not inherited
  from population 1, "a stated position on population 2 -- whether an unimplemented-but-documented register should
  fault or be backed", and the rung-3 attempt.  The answer reports that state accurately.
* No committed VME probe/gate (`git grep` at HEAD over `regress/` outside artifacts: nothing);
  `regress/artifacts/vmedefaultkill/` is UNTRACKED (four files on disk, none in `git ls-files`) while
  `regress/artifacts/faultpair/` is tracked.
* Manuals: `mc88100.txt:8018-8025` (fault reply -> data access exception), `:9310-9329` (nonexistent address, bus
  error); `vmesbcp2.txt:76-78` says this file is Part 2 (Chapters 5-9), `:399-428` is only the Chapter 4 TOC, and the
  VMEchip2 LCSR body is ABSENT -- one `$FFF400xx` mention in the whole file (`:4324`, GPIO2 on the VBR word).
  `:2262-2277` is VSBchip2's reserved-register rule, not transferable.  So there is no local primary source for what
  VMEchip2 does on an unimplemented LCSR offset -- the answer's honesty about `OUTSTANDING_BUGS.md:18773-18774` is right.

**Premises found FALSE:** none.  (No closure is proposed.)

**Ruling: ADOPT WITH CHANGES.**  The recommendation is sound and matches the ledger's ruling and owed list.  The changes
come from material the answer did not open, and the first one bears directly on the population-2 decision the ledger
says the round owes:

1. **The in-tree OpenBSD guest source reaches this `default:` at ATTACH, by reading.**  `_guest-src-openbsd22/sys/arch/
   mvme88k/conf/GENERIC:69` has `vme0 at mainbus0 addr 0xfff40000`; `dev/vme.c:73-103` `vmematch()` returns 1 with no
   probe; `vmeattach()` (`:321-360`) calls `vme2chip_init()` for BUS_PCCTWO unconditionally (the `scon` test at `:349`
   only prints); `vme2chip_init()` (`:443-527`) does `tctl &= ~SYSFAIL` (cased) and then **reads `vme2_masterctl`
   (`0x28`, `vme.h:169`) -- uncased -> `exit(1)`** -- and would go on to write `master3/master4/master4mod/masterctl`
   (`0x1c/0x20/0x24/0x28`, all uncased) and read/write `gcsrctl`, `irql4`, `irqen` (cased).  `vme2abort()` (`:570-584`)
   reads `irqstat` (`0x68`) and writes `irqclr` (`0x74`), both uncased, on the ABORT-switch NMI.
   **Two consequences.**  (a) Under BLANKET FAULT for population 2, that kernel takes a kernel-mode data access fault
   in `vme2chip_init()` with no `pcb_onfault` set -> `trap.c:158-166` prints "Data access fault" and `panic()`s: the
   host kill becomes a guest panic at attach -- better than today, still not a boot.  Under BACKED ACCEPT (the file's
   own `T1CMP`/`VBR` storage idiom, `:85-88 :131-135`; the master decoders have no emulator-side effect while the
   VME windows are `unreadable`) the attach proceeds.  So the population-2 position must be put to the owner WITH
   this evidence; "explicitly labelled FAULT-as-model-limitation" for the 26 named bases is not adopted as written.
   (b) It is NOT a proof that a stock boot dies here: upstream's `doc/machine_mvme88k.html:106-128` shows an OpenBSD
   **4.4** RAMDISK completing `vme0 at pcctwo0 offset 0x40000 / using BUG parameters / vme to cpu irq level 1:1 /
   vmes0 at vme0` on this same `dev_vme.c` -- so the 4.4 `vme.c` touches only the cased registers (the ten cases look
   carved to exactly that path).  The tree's guest source is 2.2; upstream's documented boot is 4.4/4.5; no image of
   either is in the tree (`_images/` holds only landisk; the doc says to fetch 4.5 from ftp).  Both are readings.
   The rung-3 attempt stays the next step; a rung-4 attempt with the 4.5 RAMDISK is the cheap follow-up the doc's own
   recipe gives.
2. **Witness both DIRECTIONS.**  The answer's core sequence (`ld` from `base+0x30`) reaches only the MEM_READ branch;
   add a `st` to an uncased offset (`0x28` is the driver-relevant one).  The two `debug()` branches differ, the exit is
   shared, and under FAULT both must deliver DATA_ACCESS.  Keep the answer's free-running form and its controls
   (`0x67000000` at `0xfff40088` is a genuine device signature; RAM reads 0).
3. **Population 3 is 30 lanes if "implemented" means "cased"** (10 cases x 3), not 12: the six debug-and-break cases
   (`GCSRCTL, TCR, IRQEN, IRQL3, IRQL4`, offset 0) have interior lanes too.  The ledger's 12 counts only the four with
   backing store.  The lane decision must say which population the other 18 belong to.
4. **Commit the untracked `regress/artifacts/vmedefaultkill/` files** the ledger ruling cites (`codex_design_20260911`,
   `codex_faultreopen_20260911`) before anything cites them again -- volatile-path rule.
5. Records: `OUTSTANDING_BUGS.md:18769` "a machine this project actively boots" -- there is NO mvme88k OS boot rig
   (`pcc2_width_witness.py:45`; the gates construct mvme187 from a load file); correct to "constructs and probes".
   `:18773-18774` "the bus error real VME hardware would" -> "the exception `memory_rw.c` delivers", as the answer says.

**Next action:** the rung-3 witness (both directions, free-running, controls as above, preserved durably), then the
design brief carrying the population split with item 1's evidence for the owner's population-2 decision.  Priority
**HIGH** -- one aligned guest load on an in-tree machine ends the process today, with no diagnostic.

**What else the answer missed (mine, LOW):** under FAULT the host prints nothing at default verbosity either
(`memory_rw.c:604` is `debug()`), so the row's opening complaint -- an unexplained death -- moves from the host to the
guest.  Whether the FAULT path gets a once-per-offset host-side announce is a design question the brief should ask
explicitly rather than inherit from the "announce is moot" line in the ledger.

---

## Cross-cutting

* Tally of premises: I checked ~70 `path:line` claims across the four answers; every one held.  What changed three
  rulings was material outside the answers' reading -- chain obligations behind the two closures, and the guest
  source plus upstream doc for the VME row.  That is the pattern the carrier predicts for a reading seat: right on the
  file, silent on what the file does not say.
* All four are Daybreak answers.  The confirming seat (GPT-6 Astra) refused the briefs at the content filter; the
  confirmation pass should use the neutral wording the carrier prescribes, or it will refuse this file's subject
  matter too.
* Nothing here was built, run, or edited; the only file written is this one.
