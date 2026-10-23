# GAPS.md -- the external-fixes research filing: what is unsettled, judged, or worth the coordinator's eye (2026-10-22)

Drafts in this directory: `ledger_rows.json` (126 rows), `ob_section.md`, `corrections.md`, `commit_msg.txt`,
`PRETEST.md`, `R1_tree_diff_20261022.txt`.  Builders and the pretest are under `work/`.  ADJ = `ADJ_RULINGS.md`
(`regress/artifacts/research_20261022/adj_20261022/`).

## The three that matter most

1. **Section D can red this commit because of the research directory, not the filing.**  The commit adds
   `regress/artifacts/research_20261022/distro_patches/netbsd_pkgsrc/netbsd_src_refs/wdcreg.h` (NetBSD's file, 74
   lines).  D resolves each added `name.h:N` citation with `git ls-files "*/name.h" | head -1`, and `regress/...` sorts
   ahead of `src/include/thirdparty/wdcreg.h`.  The T95 widening edits `closeassessrows`' state_note, so that whole JSON
   line is re-added, including its old `wdcreg.h:138`.  Result: `bad "cited wdcreg.h:138 but ... has only 74 lines"`
   (emulated in PRETEST.md section 5; the real D reads unstaged `git diff -U0`, so whether it fires depends on how the
   commit tool runs the precommit).  The hazard is permanent once that file is tracked: any later edit that re-adds a
   `wdcreg.h:N` line hits it again.  Options, the coordinator's call:
   (a) store the five `netbsd_src_refs/` sources under a non-source suffix (e.g. `wdcreg.h.txt`) -- report B cites
       that directory, so its paths would need the same suffix;
   (b) leave `netbsd_src_refs/` untracked -- report B's citations would then point at untracked files;
   (c) drop the `closeassessrows` ledger op and keep its OB note -- this avoids this one instance only.
   Only `wdcreg.h` collides today (`git ls-files` finds no fork `atareg.h`, `wd.c`, `wdc.c` or `ata_wdc.c`).  The
   research directory's other `.c/.h` names are `patch-src_...` files, which match no fork basename.

2. **No precommit check catches a duplicate ledger id.**  The requested control "duplicate one id (must red)" stays
   green: both `ctl_dupnew` (a new row twice) and `ctl_dupold` (a new row renamed to the existing `letxrestart`) pass
   P, W, O, H, K, Q2, I2, I, L and X (PRETEST.md section 4).  `check_bugfile_sync.py` keys a dict on the id, so a second
   row silently replaces the first.  Only this drafter's own guard (`work/pre/pretest_build.py`, `guard_ids`) refuses
   them, and the commit tooling does not run it.  Uniqueness was checked mechanically for this filing (item 4), but
   nothing will check the next one.  A uniqueness check is a tool change that owes its own negative controls, so it is
   filed here and not built.

3. **The row count follows the adjudication, with two departures and one addition to confirm.**
   **126 rows** = 121 TRIAGE.md UNFILED + 4 (ADJ C: N1-N4) + 1 owner option (ADJ E).
   * **N5 is not a new row.**  It is `ppcbatppkill` (open, HIGH, filed 2026-10-02): "a BAT hit with PP=00, or a store
     through a read-only BAT, reaches fatal()+exit(1) instead of a DSI/ISI" (`memory_ppc.c` `ppc_bat_block` ->
     `:273-276`).  The Grok seat searched for the message text "TODO: BAT exception", and that row does not quote it.
     A second row would repeat the duplicate-row defect that ADJ B T136 is consolidating.  N5 is therefore recorded
     on `ppcbatppkill` (ledger op and OB note).
   * **No separate PFAR row.**  My first draft split T36 into a `memory_rw.c` row and a `lunaprobepfar` row for R2.
     ADJ D5/E made T36 the carrier, so the split and the id `lunaprobepfar` are withdrawn.  T36's row (`m88kbuserrregs`)
     names both halves and the reopening.
   * **The owner-option row `pristinesecondref` (LOW) is filed** because ADJ E says the second reference "is FILED as
     an owner option".  The coordinator's summary of E did not mention it.  If it is not wanted, there are 125 rows,
     and the CHANGELOG R1 note (`cl_r1a_new`), which names the row, must be edited to match.

## Ids

4. **Collisions: none.**  The 126 new ids were checked against these sets, with no hit:
   * the 941 ids at HEAD and the 941 in the working-tree ledger (identical sets);
   * each other;
   * the 8,786 code spans and every heading word in HEAD's OUTSTANDING_BUGS.md;
   * the code spans in CHANGELOG.md;
   * bare-word occurrences in both files.
   Each id is 4-25 characters, `[a-z0-9]` only.  The id `lunaprobepfar` was used in a first draft and is withdrawn
   (item 3).  Nothing else had to be resolved.
5. **Nine new ids appear twice or more in the bug file.**  The OPEN LIST head entry lists the batch, and the R2
   correction names `m88kbuserrregs`.  For these nine, P cannot see a missing bullet: `ctl_dropbatch` stays green.
   The pretest checks one bullet per row mechanically instead ("lead ids == new ids, each exactly once").  The
   drop-bullet control uses `lermd3fcs`, which is named nowhere else.

## Class, severity and reach judgments

6. Severity is the coordinator's class rule: HOST-STOP and GUEST-CORRUPTION are HIGH; WRONG-RESULT, CPU-STOP and
   HOST-UB are MED; HYGIENE, BUILD and FEATURE are LOW.  The cases where the rule and the content pull apart:
   * **T4 `wdclbaaddr` is HIGH while LATENT here** (ADJ B).  The class is unchanged, so the severity is too.  The
     latency is in the title and the state_note.
   * **T17 `dbgdevremove` is HIGH by class** although its input is debugger-user only (reach C, ADJ B).
   * **T141 `mb89352fmtargs` is HOST-UB, MED.**  ADJ B says "not hygiene, at least MED" but names no class, so HOST-UB
     is my label.  It appears in no TRIAGE.md count.
   * **T139 and T140 (guest-drivable host log floods) are LOW by class.**  The fork's #278 measured 70-140x slowdowns
     from a flood of the same shape.
   * **T30 `mipsrecipdecode` is MED by class.**  It includes a guest re-trap livelock and an ungated flood.
   * **E1 `pristinesecondref`** is HYGIENE (records and harness), LOW.  It is an option, not a defect.
   * **N4 `ppc601xlateexit`, reach K\*, is my reading.**  ADJ gives no reach.  The PPC601 model exists
     (`cpu_ppc.h:78`), but no `src/machines/*.c` names it as a default, so it needs `-C PPC601`.  `ppc_bat()` carries
     the same exit at `:96-99`, behind the one at `:263`.
   * **N2 `m88kxmemusr`, reach U, is my reading**, and the defect rests on the GPT-6 Astra seat's reading of two code
     sites that disagree (`:2359` vs `:3604-3607`).  The manual's encoding table (`mc88100.txt:6488-6514`) does not
     render bit positions in the text extraction, so I could not settle the U bit position myself.
7. Port confidence:
   * **T4: Y -> P (idea only).**  ADJ B and F rule out the FreeBSD/DragonFly patch as a patch.
   * **T127: Y -> UNVERIFIED** (ADJ B).
   * **T1: stays "yes".**  Both seats agree that a port exists; its shape is disputed (D1), which the state_note
     says.

## How the rulings were applied

8. **B, on rows I do not file.**
   * **T6** is applied in `qhslowifetch`'s QUEUE note (reach U on 32-bit; PPC970 stops first at N3; the fix is not
     N3/N4/N5's).
   * **T14, T15 and T16 (FILED rows outside the batch) are NOT edited.**  These are `ctorabortclass` (reach C),
     `ns16550`, carried by `closeassessrows` (word it "observed with the recorded compiler at -O0/-O1", per
     OB:6146-6174), and `qhselectretry` (reach C).  None of my text calls T15 a host kill.  If those records should
     carry the amendment, they owe a ledger op each.
9. **T9 and `b120`.**  ADJ B says T9 is "carried in b120's record".  The per-controller outcomes are already in
   `b120`'s record, but WRITE AND VERIFY(10) is not (0 mentions).  So a `b120` state_note prepend carries T9's data-loss
   finding and the SPC citation.  This goes slightly past the literal ruling; drop the op if it is not wanted.
10. **T136.**  `m88kmxmkill` is set from `open` to `dropped`, and its state_note says why.  `m88kpsrmxm` (MED, the
    manual-cited title) is the carrier and names the alias in its state_note.  The precedents are the dropped
    duplicates `ledgersevmissing` and `pitlsb`.
    * The choice of carrier is mine.  The other way round, keeping the older row, also fits "keep both histories".
    * No `alias` key is added to the schema, because no tool reads one.
    * `m88kmxmkill` has no entries and no hold, so H, I and I2 do not change (pretest: 46 held stages before and after).
11. **D.**  The QUEUE markers on existing rows are `corrections.md` ledger ops (`ppcllscrcexit` 2, `qhslowifetch` 3,
    `mvme187memcoob` 8, `pvrrenderexit` 10, `fbsdrampair` tail 1).  `exitunowned76` carries three positions in one
    note:
    * batch 8: the dev_mvme187.c exits, after the bounds repair;
    * tail 3: dev_clmpcc.c;
    * tail 4: ONE dev_osiop.c site.
    TRIAGE.md and ADJ D do not name which osiop site.  The note leaves it to that round, from the reserved ids
    `osiopselectzero`, `osiopregexit` and `osiopdnadexit`.
12. **A wording slip in ADJ D5.**  It says "`memory_rw.c:437` has already made `paddr` device-relative".  At HEAD,
    `:437` saves `orig_paddr` and `:494` makes `paddr` device-relative.  The T36 note states it that way.

## R1, R2 and the gate_ab.sh question

13. **RECORDS_VERDICTS.md R1 has two imprecisions; corrections.md uses the measured figures.**
    * **The `1U <<` sites.**  It says "at two sites"; there are THREE (`generate_arm_r.c:139`, `:200`, `:279`).
    * **The extras.**  It says "every one a generated `tmp_*.c`"; 50 are `cpus/tmp_*.c`, and the other 9 are
      `devices/autodev.c`, `machines/automachine.c`, six font files and `include/ppc_spr_strings.h`.  ADJ E's figures
      agree with mine.
    * **The `configure` half is now settled locally.**  I compared against the research agent's tarball, whose sha256
      I recomputed as `79c4437c...8e83`: `configure` gains the 21-line GNU89-inline probe (`:565-585`, the fork's #9).
    * **Missing files, new here.**  The full-tree diff also shows 23 release files missing from 39748e3c: seven
      Makefiles and 16 test install/boot scripts.  TRIAGE.md's "61 generated files" counts the two crash dumps, which
      are not generated.
14. **Volatile path.**  The CHANGELOG note cites `regress/artifacts/research_20261022/R1_tree_diff_20261022.txt`.
    Copy this directory's `R1_tree_diff_20261022.txt` there in the same commit.  The tarball it measured lives only in
    the session scratchpad (`ghresearch/reports/dl_070/`).
15. **gate_ab.sh.**  `gateab_r1b` (line 4) is drafted and marked a SEPARATE commit, as ADJ E says.  Keep it out of
    the records commit for a second reason: a `regress/*.sh` path makes check L grade the commit as authorship, not
    records-only.  Not drafted, and outside the instructed grep:
    * `gate_ab.sh:2` ("against pristine 0.7.0");
    * `gate_upstream.sh:46` and `build_asan.sh:56`, which build or read the same "pristine" tree;
    * `README.md:103` (the commit table: "unmodified upstream baseline") and `:249` ("pristine `39748e3`").
      README is a record and could take a pointer like `ob_r1c`.
16. **The other grep hits.**  OB:2843 and CHANGELOG:22346/:22383 say "pristine baseline" in est/-era text.  They do
    not name 39748e3c and are left alone.  The two `R1 (c)` pointers (OB:10407-10409, CHANGELOG:23640-23643) are
    marked OPTIONAL: ADJ E puts the correction beside CHANGELOG:24451-24462 and forbids re-attributing old A/B results,
    and both pointers re-attribute nothing.  PRETEST.md's `root_min` tree shows they can be omitted with every check
    still green.  The 39748e3c commit message itself cannot be corrected in place: it is not rewritten (ADJ E).

## Smaller things

17. **Citations.**  The new rows cite 249 line ranges at de8c7547.  All are inside their files.  219 have a title
    keyword within 6 lines.  The other 30, in 11 rows, I read by eye: all match the defect.  The lines the adjudication
    cited and I reused were also read: `memory_ppc.c:263-266`, `:285-288`, `:69-73`, `:314-326`;
    `memory_rw.c:259-268`; `cpu_ppc_instr.c:4115-4119`; `dev_wdc.c:374-377`; `cpu_mips_coproc.c:2040-2041`,
    `:2168-2169`; and the widening lines in `dev_le.c`, `cpu_mips_coproc.c`, `cpu_dyntrans.c`, `cpu_mips.h`,
    `cpu_mips.c` and `dev_vr41xx.c`.
18. **TRIAGE.md (c) records defects outside this brief.**
    * R3 (`fbsdrampair`'s stale title citation) is mentioned in its QUEUE marker; the title is not edited.
    * R5 is carried by `ppcexcfatal`'s state_note.
    * R6 (`ppcbatstale`'s title), R7 (`b120`'s id and title mismatch) and R8 (`ctorabortclass`'s discharged hold) are
      untouched.
19. **The commit message assumes four things.**
    * The research directory is added in this commit.
    * The optional pointers are applied.
    * `matrix.html` is regenerated (section Q; the pretest shows base renders HEAD's tracked `matrix.html` byte for
      byte, and root renders with 888 in work).
    * The two corrections land in this commit.
    Edit the message if any of these changes: messages are written from the diff.  `fable_queue.md` needs no
    regeneration (I2: 46 held stages before and after).
20. **Wording.**  Titles reuse TRIAGE.md's wording (file:function -- what is wrong -- class), with the backticks
    stripped from the leading path.  They are technical, not ASD-STE100.  The new OB heading is about 150 characters,
    like its neighbours.  OB bullets are wrapped at 120 columns, and no id span is split.
21. **HEAD drift.**  The working-tree ledger already differs from HEAD (another session).  The OLD anchors are content
    strings, and `work/pre/pretest_build.py` refuses any that do not occur exactly once.  If HEAD moves, re-run it and
    `work/pre/run_pretest.sh` before committing.
22. **Attribution.**  `commit_msg.txt` ends with the Fable 5.1 trailer, as asked.  The drafts were produced by an Opus
    5.5 sub-agent, in case the trailer should say so too.

## Decided by the coordinator, 2026-10-22 (applied in `staged/`)

* Item 1: the five `netbsd_src_refs/` sources now carry a `.txt` suffix, with a README; no ledger op is dropped.
  The staged pretest's D emulation runs over the renamed directory.
* Item 2: no row in this commit.  The gap is written as OWED in `commit_msg.txt` and in the CHANGELOG records block,
  and is filed in the hash follow-up.
* Item 3: N5 stays on `ppcbatppkill`; `pristinesecondref` is kept (126 rows); `m88kpsrmxm` stays the carrier; the
  `b120` WRITE AND VERIFY note is kept.
* Item 14: `R1_tree_diff_20261022.txt` is in `regress/artifacts/research_20261022/` (md5 equal to this directory's
  copy), and RECORDS_VERDICTS.md's R1 details are corrected in place.
* The staged set's working-tree input md5 is in `staged/WT_INPUT_MD5.txt`.  The pipeline refuses to copy
  `ledger.WT.json` unless the working-tree ledger still has it.

GAPS_DONE
