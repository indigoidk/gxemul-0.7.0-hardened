# #571 (`ppcdsformxo`) pass-1 brief -- drafter's notes

Drafted 2026-10-24 against HEAD `add098b9`.  Read-only on the project.  Line numbers are HEAD's (identical in the working
tree for every file cited here except where marked).  Dispositions only: no rulings by the drafter.

## Files and sizes

| file | bytes | what it is |
|---|---:|---|
| `brief_FULL.md` | 180,424 | file-reading seats (Grok, GPT-6 Astra) |
| `brief_COMPACT.md` | 87,672 | stands alone; Argon through agy |
| `brief_PACKET.md` | **74,595** | packet-fed seats (GLM 5.3, DeepSeek); 74,811 once the launcher inserts its Q12/Q34 line (simulated in memory) |
| `C0_OUTPUT.txt` | 7,861 | the §C0 commands' output |
| `LS_PERMITTED.txt` | 2,619 | the permitted-path check |

* Sections 5, 6, 7 and 11 are byte-identical across all three briefs (checked).  Each brief has exactly one line matching
  `^## [0-9]+[.] QUESTIONS.*`, and its `~~~~` fences are balanced.
* `brief_COMPACT.md`: the coordinator's message quotes 144,491 bytes.  That was the first build.  It was rebuilt to
  87,672 bytes (same shared sections) before the message arrived, and has not been touched since.  It is still above
  the 70 KB aim.  `brief_FULL.md` was rebuilt in the same run (180,424 bytes).  Per the coordinator's instruction,
  neither has changed since.
* `brief_PACKET.md` follows the coordinator's spec with one deviation: section 8.9 carries `cpu_ppc.c` 1468-1551, not
  1468-1530.  Line 1530 is `if (fpreg)`, so a cut there splits a statement, and P10's guest-invisibility premise rests
  on the `running` preview at 1535-1550.  Section 8.7 also keeps the `lwa` cast lines 119-125, which P3 relies on.

## A. Inconsistencies between the research rulings, the witness and the source

1. **`ldu` with RA = RT.**  `CRIT_RULINGS.md:15` says "disclosed, not checked".  `grok_crit.txt:58` says "not checked
   ... Left disclosed".  `codex_rescrit.txt:55` says "`ldu` forbids RA=0 and RA=RT ... Distinguish invalid forms
   explicitly rather than executing them as plain `ld`/`std`", which can also be read as covering only the reserved XO
   values.  Disposition: put to the panel as D1, Q1(d).
2. **Witness machine.**  `CRIT_RULINGS.md:15`, `codex_rescrit.txt:62` and `grok_crit.txt:62,66` name `testppc`.  The
   witness ran on `-E bareppc -M 64` (`WITNESS_REPORT.md:13`).  Both default to PPC970 (`machine_test.c:448-457`), but
   only `testppc` calls `default_test()` (`:444`).  Disposition: D4, P12.
3. **Rung-3 shape and clause (a).**  `grok_crit.txt:64` makes its clause-(a) row a `stdu` store row, and `:66` proposes
   one `stdu`, one `ldu`, one `lwa`, one XO-0 `std`, with an `stw` for liveness.  The witness places no store and uses
   `li` (`WITNESS_REPORT.md:85-86`).  Disposition: D3, D5, Q2(a).  The store rows are owed red on the base binary, on
   the T36 precedent (`m88kbuserrregs/table1_20261023/prefix_HEAD.out`).
4. **The store half is stated as fact.**  The ledger title, `OUTSTANDING_BUGS.md:25264-25266` and `ADJ_RULINGS.md:10`
   all say "`stdu` stores at EA+1 and skips the update", but only the loads were measured (`WITNESS_REPORT.md:85-86`).
   Disposition: the briefs label it PREDICTED (section 2, P9).
5. **Ledger `witness: none` is stale.**  The row's `state_note` ends "not yet reproduced here", but a rung-3 witness now
   exists in `witness_20261024/` (uncommitted).  Disposition: a records update at landing.  Q3(e) proposes
   `probe:regress/artifacts/ppcdsformxo/witness_20261024/ppc_dsform_probe.py`.
6. **The ledger row has no `stages` key** (`C0_OUTPUT.txt` part 4), even though the research and adjudication panels
   ran (`research_20261022/crit_20261022/`, `adj_20261022/`).  Disposition: stage entries that name their panel
   directories are owed (sections G and H).  Not edited.
7. **A wrong citation line.**  `codex_rescrit.txt:59` cites `ppc_pem_32and64_2005.txt:11974` for "split or trap".
   :11974 is the heading; the sentence is at :11975.  Disposition: the briefs cite :11975 (P8) and :11974-11975 (FULL
   8.12).
8. **Disassembler range.**  The task and `pass1_20261024/fable5.HELD.txt` cite `cpu_ppc.c:1468-1517`.  At HEAD the arm
   runs 1468-1601: the mnemonic switch ends at 1528, the operand print is 1529-1534, and the running preview is
   1535-1600.  Disposition: FULL inlines 1468-1601; PACKET inlines 1468-1551 (see above).
9. **The witness census pins the folded disassembly.**  `ppc_dsform_probe.py:363-379` (`expect_unasm`) expects `ld` plus
   the raw halfword for every opcode-58 word.  If the disassembler is repaired in this round, `unasm census` goes red
   post-fix by design.  Disposition: Q1(g) and Q2(j) (re-pin first, R16).
10. **The D-form control cannot see the 58/62-only scope.**  The design scopes the clear to opcodes 58/62
    (`CRIT_RULINGS.md:15`) and says "Ordinary D-form immediates must remain untouched" (`codex_rescrit.txt:45`).  But
    the witness's `lwz` control uses displacement +8 (`ppc_dsform_probe.py:224`), whose low bits are 00, so it reads the
    same either way.  Disposition: P14, C21/C22, Q2(e).
11. **A behaviour change no research text names.**  The existing guard at `cpu_ppc_instr.c:4338-4342` makes
    `ldu`/`stdu` with RA = 0 stop the CPU once `update` is set.  Today those words execute as `ld`/`std` at the absolute
    address (DS || XO).  `grok_crit.txt:58` notes the guard but not today's behaviour.  Disposition: P5, C6/C17.
12. **Table slots that end the process.**  Slots 11/27/43/59 of `tmp_ppc_loadstore.c` (`:905`, `:921`, `:937`, `:953`)
    are `ppc_instr_invalid` (`cpu_ppc_instr.c:241-245`: `fatal(...); exit(1);`).  Any flag set with size 3, zero 0 and
    load selects them, and no research text mentions this.  Disposition: P3.
13. **32-bit CPUs.**  PEM 2005 :6253 says opcodes 58/62 are illegal on 32-bit implementations.  `grok_crit.txt:60`
    says "Disclosed, not fixed here"; CRIT and Astra are silent.  The tree already gates `rld*` on 32-bit CPUs
    (`cpu_ppc_instr.c:4602-4606`) but leaves `stdx`/`stdux` ungated (`:4921-4922`, `:4967-4968`).  Disposition: D2,
    Q1(e), P7.
14. **Unimplemented indexed siblings.**  `ldx`/`ldux`/`lwax`/`lwaux` have no `PPC_31_*` define, so they reach
    `cpu_ppc_instr.c:5172` (`default:goto bad;`) on every CPU.  The witness lists them as NOT CLAIMED
    (`WITNESS_REPORT.md:89-90`), and a title/state-note grep of the ledger at HEAD found no row for them.
    Disposition: a Q4 candidate; not filed.
15. **Update suppression on access failure.**  `codex_rescrit.txt:60` asks for "suppressed base update on access
    failure" rows.  That behaviour lives in the handler (`cpu_ppc_instr_loadstore.c:87-94`, `:174-185`), which the
    repair does not edit, so it is a callee under the DEPENDS-ON bound.  Whether it can be reached on `bareppc` with
    translation off is not established; `memory_ppc.c:307-323` raises only on a translation miss.  Disposition: C26,
    asked as "(e)?".
16. **S5's wording is loose.**  It says "a storage interrupt from `memory_ppc.c`".  In fact `memory_ppc.c:313` raises
    the 603 software TLB-miss vectors (0x10-0x12) and `:322-323` raises ISI/DSI.  The premise's conclusion (no Program
    or Alignment interrupt anywhere) stands.  Disposition: FULL 8.6 shows the `git grep` output.  Not edited
    (do-not-change instruction).

## B. Records and launch notes for the coordinator

17. **Roster cell.**  The FULL and COMPACT section-0 rosters say GLM and DeepSeek get "COMPACT, two firings"; PACKET's
    roster says "this PACKET-FED form".  `launch_p1.sh:11-26` splits `packet_compact.md`, so it must split the packet
    file instead if the Ollama seats are to get it.
18. **Stale launcher comment.**  `launch_p1.sh:2-4` says "Argon NOT FIRED, agy/kimi/minimax/Opus-seat DELIBERATELY NOT
    FIRED".  But `launch_p1.sh:36` fires agy with `gemini-4-argon-high`, and `pass1_20261024/roster_NOT_FIRED.txt` and
    `argon_transport_20261024.txt` record Argon as fired through agy.  The briefs follow the latter.
19. **Argon's reading scope.**  `launch_p1.sh:36` invites Argon to open everything under
    `regress\artifacts\ppcdsformxo\`, which includes `pass1_20261024/`, where the other seats' answers land.  The
    briefs' section 0 limits it to `witness_20261024/`.
20. **Astra's reading scope.**  `launch_p1.sh:30` tells Astra "every path it cites is committed or frozen and you may
    open it".  The FULL brief marks the research artifacts and the ledger as record citations not to be opened (the
    §C5 archive scoping), and inlines their T2 passages instead.
21. **Unfrozen receipts.**  `WITNESS_REPORT.md:92-111` points at build and run receipts in the session scratchpad
    (`build_base.out`, `baseline_*.txt`, `cpu_ppc_instr.HEAD.c`, `run_dsform_witness.*`).  These are neither in
    `witness_20261024/` nor in its `MANIFEST.md5`.  Under the volatile-path rule, freeze them beside the witness before
    it is committed.
22. **Dirty working-tree files.**  `tools/BRIEF_TEMPLATE.md` and `tools/pipeline/check_probe_wiring.py` differ from
    HEAD (peer edits; 20 such files in all, `C0_OUTPUT.txt` part 5).  The briefs follow the working-tree template,
    which is a superset of HEAD's.  They quote `check_probe_wiring.py` at HEAD.
23. **Cosmetic, left as is.**  FULL and COMPACT 9.5 quote `ppc_rldicl_probe.py` through :496, which cuts the
    `bits32 rld bad` row call mid-statement (it continues at :497).  PACKET quotes :494-497.
24. **Codex vocabulary.**  The FULL brief quotes the research seats verbatim, including "dies" (`grok_crit.txt:62`) and
    "mutant" (`:64`).  §C5 records vocabulary as one codex refusal trigger.  The risk is low (two words inside a quoted
    record), but noted.
