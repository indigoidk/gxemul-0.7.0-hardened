
## 2026-10-02 -- GXEMUL [087a90]: `#557` audits the rows closed with no commit: 18 commits fields filled, 4 members added to `closeassessrows`, one parked repair landed, one held

**What this is.**  `#555` found that a 2026-08-27 sweep had closed ledger rows on an assess-stage sign-off and filed
the class row `closeassessrows` with eight members.  The population the class draws from is every row `closed` with an
empty `commits` field -- 47 at `#555`.  grok read the 37 no seat had read (`regress/artifacts/closeassess_20261002/
grok/grok_closedcensus.txt`: 20 shipped, 14 nothing owed, 3 work still alive, 0 not determined, of 37 rows); GPT-6 Astra confirmed or overturned each and looked every commit up in `git log`
(`aconf_census/codex_aconf_census.txt`: 34 confirmed, 3 wrong, 0 not checked, of 37 rows; commits to fill: 9 confirmed of 9).  Every sha below was re-checked when this text was generated: the commit
exists and touches the file Astra named, or names the row or its round in its subject.

**Shipped, the commits field now filled -- 18** (17 of the twenty the census found shipped, plus `xfamscope`, one
of the ten rows grok had read before the census, whose two commits Astra looked up on the closing check; of the other
three shipped rows, two are left empty on purpose below and `boilerplateprefix`'s is filled by the post step):
* `alphatbinegsel` -- `65b007bf` (names the row and #520; touches src/cpus/cpu_alpha_palcode.c)
* `divsweeplines` -- `6a5267c0` (touches regress/diag_div_sweep.py: newline preservation and the line calculation)
* `fbwitness` -- `6014b7e7` (the first committed footbridge witness; touches regress/footbridge_sites_probe.py)
* `hookctlgate` -- `e61ccd89` (touches tools/precommit_check.sh: introduces the hook-control gate)
* `hookdurability` -- `e61ccd89` (adds tools/hooks/round_reminder.sh)
* `lcalenzerodrop` -- `a11eaac4` (names the row and #538; touches regress/lca_widewrite_probe.py)
* `ledgerwitness` -- `aa10c9f1` (touches tools/pipeline/check_witness.py and tools/precommit_check.sh)
* `m88kexcrrtrapmode` -- `79cd12e8` (names #502; touches regress/m88k_exc_probe.py)
* `mk48nvramkill` -- `21e75609` (names the row and #521; touches src/devices/dev_mk48txx.c)
* `nineseatreminder` -- `1202d342` (#554's commit; touches tools/hooks/round_reminder.sh)
* `novpadfourth` -- `e61ccd89` (touches tools/precommit_check.sh: the GXWSLTREE comparisons)
* `panelargvcap` -- `43106c20` (names the row; touches tools/panel.sh)
* `ppcrldiclzero` -- `e777ff06` (names the row and #522; touches src/cpus/cpu_ppc_instr.c)
* `propagatecpsilent` -- `67120fd6` (adds tools/propagate_all_trees.sh with copy verification)
* `scorehyphenfp` -- `7440e129` (#529's commit; touches tools/pipeline/check_score_claims.py)
* `smhang` -- `1a85e27c` (touches regress/selfmutant.py: the timeout -- the row's standing regression is NOT shipped (a member below))
* `wdcwidth4` -- `e61ccd89` (touches regress/wdc_addtoinbuf_probe.py (wdcatapistswap))
* `xfamscope` -- `636c0239 a4c86f11` (636c0239 (#420 final panel) introduces the per-rig budget scoping and a4c86f11 completes the stale-comment correction in regress/gate_crossfamily.sh (Astra, aconf_557 D: looked up on the closing check; grok had read the row before the census and found the edits made))
* `asanunbuildable` -- left EMPTY on purpose: the closure was a local build-tree back-fill, not a tree change
  (`c7b32355` is the records commit that recorded it).
* `wiringshghost` -- left EMPTY on purpose: no commit shipped the deletion of the three `.sh` manifest keys, which
  existed only in a working tree; `686d179c` recorded the resolution (`check_probe_wiring.py:1157-1176`) and is named
  in the row's note as provenance.  (Astra, on this unit's closing check, correcting its own census line.)

**Nothing owed -- 14** (retired, duplicate, answered by a ruling, documented-only): `b118L`, `devexit`, `b82`, `b75`,
`rtcdet`, `wdchpcmipsaddr`, `countderiver`, `preserveinstrument`, `rung1exempt`, `sgilinearnegidx`, `multilabelfloor`,
`highrankunmeasured`, `probedeathoracle`, `grokampkill` -- each with the one fact that shows it, in grok's census.

**Work still alive -- 4 added as MEMBERS of `closeassessrows` (12 now: `m8latch`, `gcsections`, `ns16550`, `pcchalt`, `wdcstandby`, `rtcnarrow`, `scunbacked`, `m437multi`, `cmtattr`, `gdromcontractresidual`, `smhang`, `unreadseats23`).**  Nothing is
re-opened here; each member's ledger row carries a note; one decision per member is the class row's work.
* `cmtattr` -- the CLOSE WITH NOTE says the soft rows must sit in the adjudication queue and lengthening ids shorter than 4 is FILED rather than done; no later entry shows either (grok; Astra confirmed).
* `gdromcontractresidual` -- the two contract corrections are NOT at HEAD (regress/gdrom_default_probe.py:56 bare M3, :119 the undated escape record) and the gdromdmasilent re-measurement is OWED (Astra, overturning grok).  The parked 2026-09-17 edit that carries them is NOT landed by #557: Astra's review (aconf_parked, 2c) found it also adds two executable rows and tightens a third (54 -> 56 row() sites; the gate pins 60 rows and the working probe makes 62), i.e. a detector change belonging to M2_gdromnodatawidth and gdromacceptdmanum, and its docstring contradicts the gdromdmasilent record in one place; it waits for a round of its own.
* `smhang` -- the timeout shipped (1a85e27c) but the row's standing 'SETUP within T seconds' regression is explicitly deferred (the fable5 ruling of 2026-08-19 in the row's entries: 'this should be its own round') with no carrier (Astra, overturning grok).
* `unreadseats23` -- the 23 answers were read, and the same note leaves four checks undone (a gate that matches the probe's printed strings; the PUT@8 contract overclaim; the `rgb not corrupt` inequality; no ABGR row) -- pending checks, not established defects (Astra: sgi_re_rgb_probe.py:343 already asserts the exact value).

**Two repairs the census found UNCOMMITTED since 2026-09-17, both reviewed by Astra (`aconf_parked`: boilerplateprefix HOLD; gdromcontractresidual HOLD):**
* `boilerplateprefix` -- LANDED by this commit.  The parked repair of `tools/pipeline/check_boilerplate.py` (the
  comparison key is the whole seat note, not its first 60 characters) was right in its code and wrong in its comment:
  the quoted preamble is 81 characters, not 66; "the day it landed" was written for a landing that never happened;
  "recall" overstated what the old key lost; the file's header still promised a prefix comparison and said the check
  was outside the hard gate (it is in it: `precommit_check.sh` section O).  Corrected, and its controls re-run on the
  day (`draft/boilerplate_controls_20261002.out`: the untouched ledger passes; one identical paragraph injected across
  four seat cells after the cutoff reds it and names the row).
* `gdromcontractresidual` -- HELD.  The parked edit of `regress/gdrom_default_probe.py` is not the docstring
  correction it looked like: it also adds two executable rows and tightens a third (`row()` call sites 54 -> 56; the
  gate pins 60 rows and the working probe makes 62), which is a detector change belonging to `M2_gdromnodatawidth` and
  `gdromacceptdmanum` and owes a round with a pass on the diff; and one of its claims contradicts the `gdromdmasilent`
  record.  The parked file stays in the working tree, uncommitted; the row is a member above.

**What the gates said when the fields were filled** (`#557`'s precheck of 19:10; the repairs ride in this commit, each
derived from the staged ledger by the gate's own rule and asserted against the names the hook printed):
* section K (a row closed with commits names its witness): 3 rows had no witness field -- `fbwitness`, `ledgerwitness`,
  `xfamscope`, harness rounds, each given `harness:<what proved it>` from its closing commit's own message -- and 2
  (`lcalenzerodrop`, `nineseatreminder`) had one the checker could not read: `harness: ` with a space, re-shaped, text unchanged;
* section I (a closed row that changed code owes a regress review): 8 rows -- `fbwitness`, `lcalenzerodrop`, `ledgerwitness`, `m88kexcrrtrapmode`, `nineseatreminder`, `scorehyphenfp`, `smhang`, `xfamscope` -- had never been reviewed or held,
  because section I keys on the commits field.  Each now carries a `[HELD AWAITING SEAT: fable5]` regress entry and a
  `hold_question`; the Fable agent seat is deliberately not fired (owner, 2026-10-02), so they wait for the batched sign-off;
* section L (the ledger names the work that shipped): `hrecordowed`, filed by `#556` with an empty field, now names `1329d894`
  (a pre-existing `#556` leftover the same precheck found -- a code commit against an OPEN row with an empty field is
  HARD there -- not a consequence of the fills);
* and the generated block of `tools/pipeline/fable_queue.md` is regenerated from the staged ledger so the eight holds
  are NAMED in the queue ("holding and queueing are one action"); the file is committed as HEAD plus that block only.

**That is the class seen from the gates' side:** K's witness rule and I's missing-regress rule both key on the commits
field, so a row closed with no commit escapes exactly those two and owes nothing under those two rules.  Filling eighteen fields
produced thirteen obligations at once (3 + 2 under K, 8 under I).

**Not done:** the re-open decisions for the 12 members (the owner's or the flagship's); the detector round
for the parked `gdrom_default_probe.py` edit; of the three rows grok read before this census and left out of the
class, `m8sarseq` (carried by `m8sarrows`) and `m437rtmp` (owing no code) keep empty commits fields -- nothing shipped
under them to attribute -- and `xfamscope`'s is filled above.
