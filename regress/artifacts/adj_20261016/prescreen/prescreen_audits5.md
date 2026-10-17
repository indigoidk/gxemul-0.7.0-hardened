# Prescreen -- grok's premise audits, set 5 (agypack_20261013)

Written 2026-10-16 for the adjudication panel. **Tree: `GXEMUL-SEC` at HEAD `e483d931`.** Tracked files were read only with
`git show e483d931:<path>`. The working tree's uncommitted edits were not used as evidence; the one exception is labelled
(records_three/F5). Untracked round artifacts were read from disk. This file is the only write; nothing was built or run
beyond `git` reads, greps, and Python regex or arithmetic evaluated on literal strings.

**Jobs (11):** diagdiv_three, osiop_three, sgi_harness_five, sgire_pcc2_vme, of_two, pvr_gdrom_four, net_three, loaders_four,
fb_vga_x11_five, cpu_policy_two, records_three. These are premise audits of 39 ledger rows; every row is HIGH and open at HEAD.

**Seats.** grok answered all eleven (`<id>/grok_<id>.txt`).
- Per its `.err` files, grok's context auto-compacted mid-run on six jobs: sgi_harness_five, sgire_pcc2_vme, loaders_four,
  fb_vga_x11_five, cpu_policy_two and records_three.
- The `*.walled402.txt` files for loaders_four, fb_vga_x11_five and records_three are earlier walled attempts, not answers.
- By its own FLAG lines, grok read the WORKING TREE for net_three and pvr_gdrom_four, because its terminal was denied.
- **agy: no answer exists for any of the eleven** (no `agy_<id>.txt`), and HARVEST.md / HARVEST_AUTO.md carry no disposition
  for these ids (grepped).
- **Argon: not yet** (queued).

**Files read by every job:**
- `regress/artifacts/agypack_20261013/briefs/<id>.md` (all eleven are in `briefs/`; none is in `briefs_next/`)
- `<id>/grok_<id>.txt`, plus `.err`
- HARVEST.md, HARVEST_AUTO.md
- `e483d931:tools/pipeline/ledger.json`, `e483d931:OUTSTANDING_BUGS.md`

Each table below lists that job's further files.

**Method and disclosure.**
- I did diagdiv_three first-hand.
- Seven read-only helper agents verified the other ten jobs. They were the same model as this author, not panel seats, and
  were told to open every claim at e483d931.
- I re-checked the load-bearing items first-hand: every FILE, the time-critical item, the cross-job classes, and a sample of
  REFUTED and RECORD CORRECTION items. Each table's "Files read" line lists those spot-checks.
- One helper value was wrong and is corrected in place (fb_vga_x11_five/F9).
- Four categories were normalised so the same kind of finding grades the same way across jobs: pvr_gdrom_four/F2 and F4,
  net_three/F4, cpu_policy_two/F13.

**Categories.**
- DISPOSED: a ledger row or record at HEAD (or HARVEST.md) already handles it.
- CONFIRMED: verified; it becomes a FILE, a RECORD CORRECTION (RC) or a BRIEF PREMISE (BP).
- REFUTED: the committed source contradicts grok. "REFUTED (record holds)" or "(doubt settled)" means grok flagged
  something as unverified, the record survived the check, and nothing is owed.
- CANNOT SETTLE: names the one read or run that settles it.

Evidence marks: **READ** means opened at e483d931, or on disk for untracked artifacts or manuals; **REASONED** means
inference. Abbreviations: OB = `OUTSTANDING_BUGS.md`@e483d931; D = `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`;
HD = `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`; `ledger.json:N` = the HEAD blob's line.

---

## diagdiv_three  (rows diagdivunaryop, diagdivchained, diagdivtruncarg; grok 8 FLAGs; agy: none; Argon: not yet)

Files read (author, first-hand):
- e483d931: `regress/diag_div_sweep.py` (whole; last changed 6a5267c0), `regress/gate_hygiene.sh:752-846` and the same
  lines at 7440e129 and 1202d342, `git show --format= 1329d894 -- regress/gate_hygiene.sh` (hunks).
- e483d931: ledger.json:59702-59765, :60384, :28725; OB:22832-22846, :23343-23352, :23368;
  `tools/pipeline/check_probe_wiring.py:1446`, `:3172-3186`, `:3240`; `src/` (`git grep` for the three shapes and the two
  macros).
- Under `regress/artifacts/astrafiling_20261002/`: `agy/agy_highfacts.txt:9-14`, `agy/agy_highfacts2.txt:5-8`,
  `grok/grok_filehigh.txt:47-49` plus a phrase count over `grok/*.txt`, `afile_09/codex_afile_09.txt:7-12`,
  `FILING_OVERLAY.tsv:99-102` (cols 3-4), `mk_overlay.py.txt:146`, `fix_overlay_high.py.txt:32`.
- Under `regress/artifacts/astraretro_harness_20260926/`: `hbundle_regress33/codex_hbundle_regress33.txt:20,22,24`,
  `HARNESS_DISPOSITIONS.md:560-562`.
- The regexes at :89, :104 and :107 were evaluated on literal strings with `python -c`; no file was written.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok | The three rows are three mechanisms, not one defect: unary is a detection miss at :89 (absent from both counters); chained is the unanchored `CONST` (:104) plus the greedy capture (:107), so the call is counted but classed constant; truncarg is the :99 slice consumed at :112 | CONFIRMED (BP) | READ diag_div_sweep.py:89 `if re.search(r'[\w\)\]]\s*[/%]\s*[\w\(]', args):`; :99 `frag = ' '.join(args.split())[:150]`; :104 `CONST` (no end anchor); :107 `([\w\(][^,\)]*)`; :112 `var = [h ... if nonconst(h[3])]` | One script and one gate, so one round can take all three, but each owes its own mutant/row. chained and truncarg share `nonconst` and :112-113 |
| F2 | grok | :107 repeats the `[\w\(]` divisor class, so a fix at :89 alone still classes a unary/dereference divisor as constant. Today a call that also carries a constant division is counted in TOTAL but classed constant | CONFIRMED (BP) | READ :89, :107. Evaluated: `x / 2, n / -d` is detected, nonconst False; `x / 2, n / *p` likewise | Brief: the unary repair has two sites, :89 and :107 |
| F3 | grok | `diagdivunaryop`'s title over-claims: a PARENTHESISED unary or dereference (`n / (-d)`, `n / (*p)`) is detected and classed NON-CONSTANT. Only the unparenthesised `-d` / `+d` / `*p` forms (and `% -d`) drop | CONFIRMED (RC) | READ :89 accepts `(`; :107-109. Evaluated: `n / (-d)` detect True, nonconst True; `n / -d` False/False; `n % -d` False. The finding's own examples are unparenthesised (codex_hbundle_regress33.txt:20) | Retitle ledger.json:59703 and OB:23344: "...rejects an UNPARENTHESISED unary-operator or dereference divisor" |
| F4 | grok | `diagdivchained`'s title over-claims "leading constant divisor": `n / sizeof(int) / d` is classed NON-CONSTANT because `)` ends the capture. The miss is a leading numeric literal or a bare `sizeof x` | CONFIRMED (RC) | READ :104 (`sizeof\b`), :107 (`[^,\)]*`). Evaluated: `n / 4 / d` False; `n / sizeof(int) / d` True; `n / sizeof x / d` False | Retitle ledger.json:59725 and OB:23347: "leading numeric-literal or bare-`sizeof` divisor" |
| F5 | grok | `diagdivtruncarg` blinds BOTH counters only for a call already counted (previously constant-only). A NEW call whose only division lies past the cut still raises DIAG_DIV_TOTAL, because :89 tests the full `args` | CONFIRMED (BP) | READ :89 (full `args`), :99 (slice), :112; gate_hygiene.sh:840-841 TOTAL "21". Evaluated: a 140-character constant prefix plus `b / d` gives nonconst(frag) False, nonconst(full) True. The original finding states the previously-constant case (codex_hbundle_regress33.txt:24) | Brief: the row and mutant start from an existing constant-only call. The title stands |
| F6 | grok | All three rows attribute "(grok/grok_filehigh.txt: nothing live ends the process today)" to grok's file, which does not contain it. It is the overlay generator's paraphrase | CONFIRMED (RC) | READ grok_filehigh.txt:47-49 (:47 "NOT HIGH: the divisor regex drops a unary or a dereference, and no dropped CALLS-argument guest-zero division still raises SIGFPE"). The phrase occurs 0 times in that file. It originates at mk_overlay.py.txt:146 / fix_overlay_high.py.txt:32 and is carried at ledger.json:59710/:59732/:59754 and OB:23345/:23348/:23351 (also FILING_OVERLAY.tsv:99, sgilwreadzero) | Mark it a paraphrase, or quote :47 / :48 / :49 |
| F7 | grok | The rows' "verbatim" `"Q1: CAN PASS \| Q2: NO LONGER \| Q3: NONE FOUND"` is not a contiguous string in agy_highfacts.txt:11-13 | CONFIRMED (RC) | READ agy_highfacts.txt:11 `Q1: CAN PASS -- regress/diag_div_sweep.py:89, ... \| Q2: NO LONGER -- ... \| Q3: NONE FOUND -- ...` (same shape at :12, :13) | Change "verbatim" to "the verdict tokens, citations elided" in the three state_notes and OB rows |
| F8 | grok | The clause credited to "agy's fact table" ("agy found no current missed guest-zero ... shape") is GPT-6 Astra's prescribed wording. agy said it misstates its line by omitting Q1 CAN PASS, and the overlay's provenance note never reached the rows | CONFIRMED (RC) | READ afile_09/codex_afile_09.txt:8/:10/:12 ("should say agy found no current missed ..."); agy_highfacts2.txt:6-8 ("CLAUSE MISSTATES ... completely omits"); FILING_OVERLAY.tsv:100-102 col 4 "the agy clause is GPT-6 Astra's wording (afile_09)". The ledger state_notes lack this | Attribute the clause to Astra (afile_09) in the three state_notes and OB rows |
| F9 | grok | The seat artifacts' gate citations predate #556: agy_highfacts.txt:11-13 cites `gate_hygiene.sh:793-794`, and afile_07/codex_afile_07.txt:34/:37/:40 cites `:755-765,788-794,835` | CONFIRMED (BP) | READ 7440e129 = 1202d342: gate_hygiene.sh:793-794 is the NONCONST check, :835 TOTAL "21". e483d931: NONCONST :796-797, TOTAL :840-841, ratchet comment :758-768, :793 `DIVSWEEP=`, :794 the `if`. `git show --format= 1329d894` (#556) adds 3 lines at @@-173 and 3 at @@-817 | The artifacts are dated and stay. The brief cites :796-797 / :840-841, or the check labels |
| F10 | grok | Q2/Q3 "NONE FOUND" (no live guest-zero instance in src/) is not shown by the lines agy cites; :76 and :89 are the scanner | CANNOT SETTLE | READ agy_highfacts.txt:11-13. Single-line `git grep` at e483d931 finds no unary/deref divisor and no numeric-then-variable chain on a debug/fatal/debugmsg line. The only const-then-variable chains in src are unused macros: dc21285reg.h:284 `UART_BRD` and z8530reg.h:344 `TCONST_TO_BPS` (`git grep` matches only their #defines). Multi-line and >150-character arguments are not covered | One run: the sweep from a clean e483d931 checkout with the :89/:107 class widened to admit `-+*~!&` and classification on the full args, diffed against the stock NONCONST list |
| F11 | grok | The gate's missing-script `else` (gate_hygiene.sh:842-843, a `note` only) is a separate condition | DISPOSED | READ gate_hygiene.sh:842-843; row `hygienesweepmissing` (ledger.json:60384; OB:23368) | none |

Aside, not grok's and not counted: `check_probe_wiring.py:3179` (HEAD) cites `gate_hygiene.sh:331 note "diag_div_sweep.py or
python3 missing ..."`. At HEAD that note is :843.

---

## osiop_three  (rows osiopdnadexit, osiopregexit, osiopselectzero; grok 7 FLAGs; agy: none; Argon: not yet)

Files read (helper), all @e483d931:
- `src/devices/dev_osiop.c`, `src/include/thirdparty/osiopreg.h`, `src/machines/machine_mvme88k.c`, `src/cpus/cpu_m88k.c`,
  `src/core/debugmsg.c`, `src/include/memory.h`, `src/devices/{dev_i80321,dev_algor,dev_bebox,dev_footbridge}.c`.
- D and `astraretro_20260926/adjudication/fable_batch3e.md`; `astrafiling_20261002/grok/grok_filehigh2.txt` and
  `afile_01/codex_afile_01.txt`; `regress/artifacts/queuetriage/codex_exitaudit_20260910.txt`;
  `regress/artifacts/osiopexits/codex_triage_20260910.txt`.
- `git grep` over regress (artifacts excluded); the 1202d342 OB diff; `8ea26abb:src/machines/machine_mvme88k.c`.

Author spot-checks: dev_osiop.c:938-956, :1143-1152, :625-657; osiopreg.h:103, :116.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok | `osiopregexit` and `osiopdnadexit` are one `exit(1)` statement, and the class row counts it as "one register default" | CONFIRMED (RC) | READ dev_osiop.c:947 `relative_addr = origofs;`. The register switch (:969) has no DNAD/ADDER case, so the access reaches :1143 `default:` and then :1152 `exit(1);`. ledger.json:46578 "one register default"; fable_batch3e.md:83 "...DNAD or ADDER -- see (b). Same umbrella as F1, a distinct predicate" | Each row names the other and the shared :1143-1152. The round that takes :1152 owns both predicates, or `osiopdnadexit` folds into `osiopregexit` |
| F2 | grok | `osiopselectzero` and `osiopregexit` carry byte-identical titles that name no site, and the governing D:681/:683 name none either | CONFIRMED (RC) | READ ledger.json:60869 and :60891 both read "a SITE of the existing class row `exitunowned76` (dev_osiop.c), id reserved by the ruling..."; the same at OB:22961/:22964; D:681/:683 "FILED-BY-PROSE at the file level". The sites are already written at astrafiling_20261002/grok/grok_filehigh2.txt:9-10 | Retitle with sites: `osiopselectzero` = dev_osiop.c:654-656 (SELECT with a zero ID bitmap); `osiopregexit` = :1143-1152. Cite fable_batch3e.md:77/:83 |
| F3 | grok | `exitunowned76`'s note still says the nine prescribed osiop repair rows are "Not filed individually yet" | CONFIRMED (RC) | READ ledger.json:46578 "NINE REPAIR ROWS PRESCRIBED ... Not filed individually yet". 1202d342 (#554) filed three ids. The SELECT-validation row covers two sites, and only :656 got an id; multi-select :668 has none | Add a dated note on `exitunowned76`: register default -> `osiopregexit` + `osiopdnadexit`; SELECT validation -> `osiopselectzero` (:656 only) |
| F4 | grok | fable_batch3e.md:77 names two guest inputs, both descriptors. A third exists: a non-table-indirect SELECT whose DBC[23:16] is 0 | CONFIRMED (BP) | READ :627 `table_indirect_addressing = dcmd & 2;`; :629 `scsi_ids_to_select = (dbc >> 16) & 0xff;`; :640 `if (table_indirect_addressing) {`; :654-656 `if (scsi_ids_to_select == 0) { fatal(...); exit(1);` | Brief: three inputs. Immediate ID 0 is the cheapest witness and needs no descriptor; the others are a mapped descriptor with bits 23:16 zero, and a descriptor read fault |
| F5 | grok | "byte 2" in fable_batch3e.md:77 is ambiguous; the code takes bits 23:16 | CONFIRMED (BP) | READ :651 `scsi_ids_to_select = (word >> 16) & 0xff;`. read_word applies BE32_TO_HOST (:237-238) on big-endian m88k (cpu_m88k.c:130), so bits 23:16 are the guest byte at descriptor+1 | Brief says "bits 23:16 (guest address +1 on MVME187)" |
| F6 | grok | D:700 says one aligned `ld`, but an aligned store also writes the word (:952-953) and then exits at :1152 | DISPOSED | READ ledger.json:60913 title "...one aligned access reaches exit(1) at :1152"; grok_filehigh2.txt:11 "load or store"; ledger.json:46578 "the word path also stores to DNAD and ADDER before reaching the unhandled-register default" | none |
| F7 | grok | ADDER is read-only per osiopreg.h, yet the 32-bit path stores guest writes into `d->reg[0x3c]` | CONFIRMED (BP) | READ osiopreg.h:116 `OSIOP_ADDER 0x3c /* ro: Adder Sum Output */`; dev_osiop.c:952-953 `if (writeflag == MEM_WRITE) *p = idata;`; DNAD is rw (osiopreg.h:103). No record mentions ADDER being ro (grep: 0) | Brief: DNAD (rw) and ADDER (ro) need different option-set members. An ADDER write is not a backed accept |
| F8 | grok | fable_batch3e.md:83 cites machine_mvme88k.c:108-112, but the code is :109-112 | REFUTED | READ machine_mvme88k.c:108 `/*  53C710 SCSI at 0xfff47000:  */` heads the snprintf/device_add at :109-112. The blob is unchanged since the import | none |
| F9 | grok | dev_i80321.c:378-384 has the same "read from 0x" fatal + exit(1) default | DISPOSED | READ dev_i80321.c:377-384; it is in `exitunowned76`'s census (codex_exitaudit_20260910.txt:89) | none |
| F10 | grok | No committed probe or gate reaches osiop | DISPOSED | READ `git grep -i -e osiop -e fff47 -e scsi_ids_to_select e483d931 -- regress ':!regress/artifacts'` returns 0; ledger.json:46578 "NOTHING IN THIS TREE EXERCISES THEM" | Brief: the rung-3 vehicle is the cold-debugger session shape of mk48_nvram_probe.py:138-140 on unmodified `-E mvme88k -e mvme187`. REASONED: one aligned 32-bit load of 0xfff47028 reaches :1152 |
| F11 | grok | grok did not re-derive the class's "two dead exits" split | DISPOSED | READ :873-874 is dead (outer cases 0x00/0x40/0x80/0xc0 at :379/:624/:767/:865). :610 is dead only while :1152 stays fatal. Both are recorded with warrants at ledger.json:46578 ("fixing the register default could REVIVE it") | The `osiopregexit` brief carries the revival dependency |

---

## sgi_harness_five  (rows sgialiaspace, sgiat1count, sgideprimbitslive, sgilwreadzero, sgirespanchk; grok 21 FLAGs; agy: none; Argon: not yet)

Files read (helper), all @e483d931 unless another commit is named:
- `src/devices/dev_sgi_re.c`, `src/promemul/arcbios.c`, `src/core/memory.c`, `src/cpus/memory_rw.c`, `src/core/debugmsg.c`,
  `src/debugger/debugger_cmds.c`, `src/cpus/cpu_mips_instr_loadstore.c`, `src/cpus/cpu_mips_instr_unaligned.c`,
  `src/include/thirdparty/crmfbreg.h`, `src/include/devices.h`, `src/machines/machine_sgi.c`, `src/machines/machine.c`.
- `regress/sgi_re_width_probe.py`, `regress/sgi_re_unmapped_probe.py`, `regress/sgi_de_primop_probe.py` (also @e5867e45,
  @1329d894, @3d7c61bb), `regress/gate_ab.sh` (also @1202d342, @1329d894^).
- D, `astraretro_20260926/adjudication/fable_batch3b.md` (fb3b), HD.
- `hbundle_regress9`/`11`/`24` and `hsgideprimopprobe` codex answers; `astrafiling_20261002/agy/agy_highfacts.txt`;
  `regress/artifacts/sgirespanchk/codex_span_20260907.txt` and `SPAN_brief.md`.
- ledger @a264a34d; OB @1202d342 and @1202d342^.

Author spot-checks: ledger rows `sgilinearoob` / `sgirespanchk` (titles, cross-mentions, `opened`); dev_sgi_re.c:1137-1147;
arcbios.c:1134-1150; fb3b:211-234; OB:14998-14999.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok | sgirespanchk's LINEAR writes (dev_sgi_re.c:705-707, :784-786) and `sgilinearoob` are one defect | CONFIRMED (RC) | READ dev_sgi_re.c:653 "The over-run itself stays filed as sgilinearoob"; :727-729 "...ONE design". ledger.json:31225, the sgilinearoob title, covers TLB_A/B/C plus LINEAR_A/B; D:605 "Rider to `sgilinearoob`". Neither row names the other (author checked) | Fold sgirespanchk (HIGH, ledger.json:41197) into sgilinearoob (med, :31224), or cross-link them. The grade split is the open `shoddprfield` rule question (OB:22834-22835) |
| F2 | grok | The TLB loops "belong only to sgirespanchk" (sgilinearoob's OB body leaves out the 253..255 walks) | REFUTED | READ ledger.json:31225 title covers TLB_A/B/C; :31232 "TLB_A/B/C 255 258 uint16_t[256] *** OOB BY THREE ***". Only the OB:14796 body lacks the 2026-09-08 extension | Optional: refresh OB:14796 so it names the TLB arms |
| F3 | grok | sgilwreadzero's device cites (:731-733, :810-812) are sgilinearoob's read side; its oracle (sgi_re_width_probe.py:338-341) is the row's own claim | CONFIRMED (BP) | READ dev_sgi_re.c:715-716 "The [tlbi+1] here has the SAME exposure as the write's ... which is `sgilinearoob'" (twin at :794-795); HD:202 | Brief: the OOB consequence is sgilinearoob's read site. Add a cross-reference; not a duplicate |
| F4 | grok | sgiat1count and sgideprimbitslive share an oracle shape (count 1, alive/how dropped) but are not one defect; sgialiaspace shares no site | DISPOSED | READ HD:621 and HD:1044 file them separately; codex_hbundle_regress9.txt:6; codex_hsgideprimopprobe.txt:6 | none |
| F5 | grok | The OB:23333 dispute bracket says this check would accept a process-ending regression, but :339-340 fails on death (agy Q1 FAILS) | REFUTED | READ OB:23333 states Astra's rule as a disjunction ("process-ending or out-of-bounds") and already says agy's table "does not test Astra's regression argument". Astra's case is the accept arm: codex_hbundle_regress11.txt:6; sgi_re_width_probe.py:336 "This row is what kills M1" | BP: sgilwreadzero's HIGH can rest only on the OOB/accept arm (M1), not on host death |
| F6 | grok | sgialiaspace: the TYPE alias "silicon graphics" (machine_sgi.c:726) also contains a space and is missed | DISPOSED | READ codex_hbundle_regress24.txt:10 names all three aliases (machine_sgi.c:726, 740); HD:371. machine.c:218-258: a lost TYPE alias calls fatal() and returns 0 (:258); only the subtype pair reaches `exit(1)` (:212) | BP: carry all three aliases. Only the subtype pair has the exit consequence |
| F7 | grok | gate_ab.sh:322-336 holds the extractor, but the assertion is at :339 | CONFIRMED (BP) | READ gate_ab.sh:325 `alias_list()`, :338 check_min, :339 `check "machines upstream had that HEAD lost" "$n_lost" "0"`. At 1202d342 these were :322 and :335-336; #556 (1329d894) shifted them +3 | Brief cites :325 and :338-339 |
| F8 | grok | The governing cite sgi_re_unmapped_probe.py:643-656 is the acc lo/hi loop plus the RESULT banner; wr/rd lat1 are at :591-598 | REFUTED | READ: the same cite list carries :589-598 (rows at :592, :597). :643-656 is the aggregation behind codex_hbundle_regress9.txt:6 "would leave all 50 rows green". The file is unchanged since de1a0de2 | none |
| F9 | grok | wr/rd lat1 are not the only rows that ignore alive: acc lo/hi (:643-652) and xwin wr/rd (:626-631) do too | DISPOSED | READ: true for those rows, but codex_hbundle_regress9.txt:6 scopes the row to the only sessions with an already-set catch-all latch. A death is caught by `rd sent` (:389) / `wr then live` (:579). The general class is `ptywaitstatus` (ledger.json:51975) | none |
| F10 | grok | sgi_de_primop_probe.py:929-932 says a host death in any dec b* row shows as a missing message, but a death after the first decline still scores 1 | CONFIRMED (RC) | READ probe:929-931 "a host death in any of them would show as a missing message"; :922-925 `row("dec b%d", t.count(declined(_op)), 1` with alive/how unused; dev_sgi_re.c:1139-1146 latches, so the message prints once | Rider on sgideprimbitslive: correct the comment in that round |
| F11 | grok | The cited :1379-1385 does not contain the n25 line row (it is at :1391) | CONFIRMED (BP) | READ probe:1379-1385 is the DISCLOSED comment; the session is :1387-1390 and the row :1391. At e5867e45 it was :1383; #556 shifted it +8 | Brief cites :1387-1392 |
| F12 | grok | The cited :1446-1451 is NOROW text, not dec b* or n25 line | CONFIRMED (BP) | READ probe:1443-1452 is NOROW at HEAD. At e5867e45, :1446-1451 was the OPUS500_RESULT/DONE banner (codex_hsgideprimopprobe.txt:6); it is now :1454-1459 | Brief cites :1454-1459 |
| F13 | grok | The cited OB:14986-14995 is the mtetlbflood section | CONFIRMED (BP) | READ OB:14986 "### `mtetlbflood` (low)". The sgideprimrdpair text cited at 1202d342 is now OB:15037 (+51) | Brief cites OB:15037 |
| F14 | grok | OB:14998-14999 says sgideprimop "does exit(1)", but the live default arm is a latched fatal() plus break | CONFIRMED (RC) | READ OB:14998-14999 "*does* `exit(1)`" and ledger.json:34830 (mtetlbflood) "and DOES exit(1)." Against them: dev_sgi_re.c:1139-1146 latched `fatal(... declined. (once) ...)`, `break;`. sgideprimop is closed (author checked) | Correct both mtetlbflood texts: "did until #500; now a latched decline" |
| F15 | grok | agy_highfacts.txt:25 Q2 cites only the default arm (:1139-1147), but n25 line's 0x01000000 hits case DE_PRIM_LINE (:966-968) | CONFIRMED (BP) | READ agy_highfacts.txt:25; probe:1389 stores 0x01000000; dev_sgi_re.c:966-968 `case DE_PRIM_LINE: if (drawmode & DE_DRAWMODE_XFER_EN) fatal(...)` (no latch, no exit) | Brief names both protected arms |
| F16 | grok | n25 rect (:1289) counts XFER_LINE against 0 and ignores alive | REFUTED | READ probe:1286-1291: one session scores `n25 rect` and `n25 rectliv`, and :1291 consumes alive | none |
| F17 | grok | sgirespanchk's grade does not reconcile: HIGH (ledger.json:41198, OB:16344) vs MED->LOW (OB:16363-16364, state_note) | REFUTED | READ OB:16344 "(HIGH; it said LOW until #554 re-graded it, 2026-10-02...)"; ledger.json:41203 opens "[2026-10-02] RE-GRADED low -> HIGH by #554". The MED/LOW text is dated history | none. The live grade conflict is HIGH vs sgilinearoob's med (F1) |
| F18 | grok | D:615 cites OB:16292, but the sgirespanchk heading is OB:16344 | CONFIRMED (BP) | READ D:615; at 1202d342 OB:16292 IS the heading, moved +52 by HEAD | Brief cites OB:16344 |
| F19 | grok | ledger.json:41200 has `opened` empty although the row was filed 2026-09-07 | CONFIRMED (RC) | READ ledger.json:41200 `"opened": ""`; :41203 "FILED 2026-09-07"; already empty at filing commit a264a34d. Three other rows share the blank: sgilinearnegidxpostmortem, sgirgbscanoutrow, sgirebufshiftub | Set "2026-09-07" (moot if folded per F1) |
| F20 | grok | The title calls the LINEAR accesses "write loops"; they are two assignments | CONFIRMED (RC) | READ ledger.json:41201 "write loops"; dev_sgi_re.c:706-707 and :785-786 are two stores each | Wording; moot if folded per F1 |
| F21 | grok | OB:16379-16382 and ledger.json:41203 still say non-CPU callers (the debugger `put`) were not enumerated and that an audit "is running" | CONFIRMED (RC) | READ OB:16379-16382. Already answered: codex_span_20260907.txt:5184 (put d -> store_64bit_word, no alignment) and :5189 (the 1 KiB split lets only TLB_A/TLB_C/LINEAR_A arrive whole). fb3b:213-225: the guest's ARC GetFileInformation/Seek reach it (arcbios.c:1140-1147 store 8 bytes at guest A1 with no alignment check; author checked). fb3b:228-233 riders were never applied: dev_sgi_re.c:653-654/:766-767 still say "NOT guest-reachable", and ledger.json:31232 "OPERATOR-REACHABLE, NOT GUEST-REACHABLE" | Rewrite as answered: the debugger AND guest ARC calls reach TLB_A, TLB_C, LINEAR_A. Apply the fb3b riders. sgirespanchk's "unreachable" title framing needs the same correction |
| F22 | grok | D:615's "guest accesses cross the arrays at :501/:564/:707" is contradicted, because the checked guest paths cannot produce an unaligned span | REFUTED | READ arcbios.c:1140 `uint64_t addr = cpu->cd.mips.gpr[MIPS_GPR_A1];`, :1145-1147 `store_64bit_word(cpu, addr + 0, 0); ...` with no alignment test; memory.c:782-783 passes len 8 unchanged; memory_rw.c:183-227 has no alignment test; OB:16371 is scoped to "the normal SGI CPU access paths checked" | The stale records point the other way (see F21) |
| F23 | grok | D:615 leaves out the TLB_B (:540) and LINEAR_B (:786) writes the title names | REFUTED | READ crmfbreg.h:232/:237 + machine_sgi.c:500: TLB_B and LINEAR_B end on 1 KiB boundaries (0x15001400, 0x15001800), where MEMORY_RW splits (memory_rw.c:104 `MRW_SPLIT_MASK 0x3ff`). The halves arrive as len != 8 and are declined. fb3b:216-220 and codex_span:5189 agree | none: the three listed lines are the reachable set |
| F24 | grok | arcbios.c:1140 is only the A1 load and names no CRIME RE window | REFUTED | READ arcbios.c:1140 is the guest-chosen destination; :1145-1147 make three 8-byte stores to it; handles 0-2 are reached with no Open (:1978-1989, :2839) | none |
| F25 | grok | OB:14805 "len == 8 forces 8-byte alignment" is false | CONFIRMED (RC) | READ OB:14805 "...unreachable today for exactly one reason: `len == 8` forces 8-byte alignment."; dev_sgi_re.c:718-720 "THAT IS FALSE: WIDTH DOES NOT IMPLY ALIGNMENT". Diagnosed at ledger.json:31230 (2026-08-31) and fb3b:231 but never applied; the same wording is in ledger.json:31229 (sgilinearoob witness) | Correct OB:14805 and ledger.json:31229 in place |
| F26 | grok | OB:14831-14833 "the shipped code kills the host before reaching the store" is stale | CONFIRMED (RC) | READ OB:14831-14832; the same sentence is in ledger.json:31230. dev_sgi_re.c:438-441 "#497: ... now DECLINES"; :664-669 latched fatal() | Correct both: the narrow access is declined by the latched width guard |
| F27 | grok | The note's "de_reg reaches at most 512" conflicts with a 1024-element declaration | REFUTED (record holds) | READ dev_sgi_re.c:1157 `relative_addr &= ~CRIME_DE_START;` (0x0800), :1160 regnr <= 511, :1172 `[regnr+1]` <= 512; :183 + devices.h:409 de_reg[1024]. 512 is the highest index, not the size | none |
| F28 | grok | The note's "zerobuf is page-shortened, never enlarged" was not re-read | REFUTED (record holds) | READ dev_sgi_re.c:1641-1644 caps the length at sizeof(zerobuf); :1646-1650 can only shorten it | none |
| F29 | grok | The read twins (TLB :523-527, :547-551, :571-575; LINEAR :731-733, :810-812) have the same span shape though the title names only writes; the TEX index was not re-checked | DISPOSED | READ dev_sgi_re.c:715-716 and :794-795 assign the LINEAR reads to sgilinearoob; ledger.json:29912 "a mirrored read arm makes it a second SITE of that class"; fb3b:221-222; TEX :586 in bounds per ledger.json:31232 | none (covered by sgilinearoob / sgitexindex; sgilinearoob's title still says "write" only) |

---

## sgire_pcc2_vme  (rows sgirekills, pcc2widthkills, pcc2c040kill, vmedefaultkill; grok 27 FLAGs; agy: none; Argon: not yet)

Files read (helper), all @e483d931:
- `src/devices/{dev_sgi_re,dev_pcc2,dev_vme,dev_unreadable}.c`, `src/include/thirdparty/{mvme_pcctworeg,mvme88k_vme}.h`,
  `src/include/devices.h`, `src/machines/machine_mvme88k.c`, `src/core/{debugmsg,emul,memory}.c`, `src/cpus/memory_rw.c`,
  `src/cpus/cpu_m88k_instr_loadstore.c`.
- `regress/{sgi_re_width_probe,sgi_mte_fill_probe,pcc2_width_probe,pcc2_width_witness,pcc2_c040_probe}.py`,
  `regress/gate_arm.sh`, `regress/gate_hygiene.sh`, `tools/pipeline/check_probe_wiring.py` (grep).
- `regress/artifacts/vmedefaultkill/measure_20261009/run_{HEAD,FAULT,DECLINE}.out`,
  `pcc2widthkills/witness_20260903_PREFIX.out`, `pcc2c040kill/witness_{HEAD,FIX512}_20260907.raw` (tracked; checked
  byte-identical to the HEAD blobs).
- HD (grep), `fablequeue7n_20261009/astra_7n4/codex_astra.txt` (grep); 70761347~1:OUTSTANDING_BUGS.md;
  `_guest-src-openbsd22/sys/arch/mvme88k/dev/vme.c` (disk, outside git).

Author spot-checks: live-exit census of dev_pcc2.c (only :435), dev_vme.c (:143) and dev_sgi_re.c (comment-stripped: :1498,
:1506, :1582, :1587, :1598, :1720); dev_pcc2.c:420-438; dev_vme.c:40-70, :128-170; memory.c:84-109; mvme_pcctworeg.h:14-22;
mvme88k_vme.h:80, :257-260; cpu_m88k_instr_loadstore.c:160-176; the vmedefaultkill note's (A) text; the four rows' titles,
commits and last entries.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok | The sgirekills `witness` field still says the six `<site> ld kill` rows are the live rung-3 symptom, "re-measured on every battery". Those rows are gone | CONFIRMED (RC) | READ ledger.json:29911; gate_arm.sh:1442 "The six `<arm> ld kill' rows are GONE"; sgi_re_width_probe.py:33 "NO LONGER EXIST". The title (:29907), the 2026-09-08 state_note tail (:30359) and entry 39 record the removal; the witness field was never rewritten | Rewrite the witness: those rows witnessed the #513 read-arm class. The six remaining exits have no witness (F4) |
| F2 | grok | sgi_re_width_probe.py:40-52 still says an 8-byte `ld` ends the host (citing dev_sgi_re.c "lines 245...362"), and its :31-38 correction covers only the paragraphs above | CONFIRMED (RC) | READ :31 "THE TWO PARAGRAPHS ABOVE ARE #497's AND #499's"; :42-45 "STILL ENDS THE HOST ... (dev_sgi_re.c lines 245 262 279 296 346 362)"; :48. dev_sgi_re.c:245 is blank and :362 a comment | Fold into `sgidefatalstale` (ledger.json:42991, LOW, open; OB:18235), the same class |
| F3 | grok | The sgirekills note opens "21 live terminating calls inside DEVICE_ACCESS", but all six remaining exits are in do_mte_transfer / DEVICE_ACCESS(sgi_mte) | DISPOSED | READ ledger.json:29912 "21 IS THE FILE TOTAL, NOT THE HANDLER'S ... Corrected 2026-08-30"; :30359 traces 21 -> 19 -> 12 -> "ACTIVE exit( ... 6"; entry 39 (2026-09-09) | none |
| F4 | grok | The five live exits are all in `do_mte_transfer` (STIPPLE, src > TLB_C, LIN COPY, depth != 8, bytemask), reachable, and exercised by no probe or gate row | CONFIRMED (BP) | READ dev_sgi_re.c:1496-1498, :1504-1506, :1580-1582, :1585-1587, :1596-1598, reached via :1807-1808. `git grep` of the five fatal strings in regress (artifacts excluded) finds no MTE hit. sgi_mte_fill_probe.py:58 avoids the LINEAR exits and runs in no gate (it is only on gate_hygiene.sh:420's grandfather list). Reachability is by reading only. The row's exit lines moved +35 | Brief: 5 live + 1 dead (F5), no witness, a rung-3 attempt owed; cite by symbol, not line |
| F5 | grok | The dead sgi_mte `else` exit (:1718-1720; `len == 4` / `len != 4` are complements) is one defect with `sgimtewidth`; the other five are a different defect | DISPOSED | READ ledger.json:31212 sgimtewidth witness "the final else is UNREACHABLE"; :31213; dev_sgi_re.c:1705/:1710; sgi_re_width_probe.py:56-57 | none. The brief says "5 live + 1 unreachable" |
| F6 | grok | Both PCC2 titles still say the host dies ("TEN live width kills"; "ends the host in reassert_interrupts()"), but HEAD declines | CONFIRMED (RC) | READ ledger.json:32661, :34835. dev_pcc2.c:508 (and 11 sibling guards) `if (len != 1 && writeflag == MEM_WRITE)` calls `pcc2_width_decline` (:462-469, fatal only); :390-397 C040 latched fatal then `assert = 0`; the only exit in the file is :435 (author checked). The state_notes already admit it: :34150 "THE TITLE'S 'TEN LIVE WIDTH KILLS' IS STALE" and :34847 "COMMITTED AS `9fa07fe`...". Commits b78bb0f / 9fa07fe are recorded | Rewrite both titles: say the fix shipped and why each row stays open (as was done for sgirekills) |
| F7 | grok | Both PCC2 witness fields report pre-fix scores (4/10, 3/4) while the gate expects 251 and 18 green | REFUTED | READ ledger.json:32662, :34846 "Committed build 3/4 ... fix 4/4 with the SAME script"; gate_arm.sh:1684-1686 (the witness "is NOT run here -- its job was to exist before the edit"); witness_20260903_PREFIX.out `PCC2W_RESULT=4/10`; witness_HEAD_20260907.raw `PCC2C040_RESULT=3/4`; witness_FIX512 4/4 | none: test-first witness records |
| F8 | grok | The pcc2widthkills note says "every register in the block ... ends the host process otherwise" | DISPOSED | READ ledger.json:32663 (2026-08-31 filing text); :34150 "reads ACCEPT ... writes DECLINE"; dev_pcc2.c:67-70 is past tense | none (F6 covers the title) |
| F9 | grok | The note and OB:14220-14221 say "a plain aligned 4-byte read of `PCCTWO_GENCTL`" ends the host; grok refutes it from the write-only guard | CONFIRMED (RC) | READ: the example was never deliverable, even before the fix. GENCTL is offset 0x02 (mvme_pcctworeg.h:18), and the m88k faults a misaligned access before memory_rw (cpu_m88k_instr_loadstore.c:168-172 `if (addr & (LS_SIZE - 1))`; author checked). The PREFIX witness used `ld.h` at GENCTL. Related: hold_question :34149 still says "FIVE" where dev_pcc2.c:105-106 says SIX | Correct the example to "an aligned halfword access" (pre-fix); reads are accepted at HEAD |
| F10 | grok | The note's "There is no mvme88k rig" is contradicted later in the same note (mvme187 constructs; the gate runs PCC2 probes) | REFUTED | READ ledger.json:32663 "A rig is what a rung-4 BOOT needs"; dev_pcc2.c:92-93 "no mvme187 boot runs in this harness"; gate_arm.sh:1737 "mvme88k/mvme187 constructs from the PROM" | none |
| F11 | grok | The OB sections for both PCC2 rows still describe live kills (old exit shape, stale lines, "Witness owed ... Not yet run") | CONFIRMED (RC) | READ OB:14194-14205 (`if (len != 1)` ... `exit(1)`); :15386, :15392-15393, :15406-15407. Neither heading has a FIXED banner (contrast :14245 "FIXED -- `#500`"). The fixes are recorded at :15457, :13985, :21896 | Add FIXED banners: b78bb0f (pcc2widthkills); #512 / 9fa07fe (pcc2c040kill) |
| F12 | grok | pcc2c040kill's state_note line cites have moved (exit :414, C040 arm :369-376, "Line 459", call-site list, bugs "line 14553") | CONFIRMED (BP) | READ ledger.json:34847 (dated blocks 09-04..09-08). HEAD: dev_pcc2.c:435, :390-397, :514; calls at :438/:455/:514/:606/:629/:643/:657/:664/:677/:717; OB:15386. Correct when written (70761347~1:OB:14553) | Brief uses current anchors; the dated text stays |
| F13 | grok | The state_note says the row was "added 2026-09-04", but the first ledger pickaxe is 70761347 (2026-09-05) | REFUTED | READ 70761347 "2026-09-05 04:03 ... the 2026-09-04 fix review" closes the 09-04 session; 70761347~1:OB:14553 holds `### pcc2c040kill` | none |
| F14 | grok | pcc2_c040_probe.py:7 still shows the pre-fix fatal "(:275)", and :10 says the C040 test is "the FIRST thing in that helper" | CONFIRMED (RC) | READ pcc2_c040_probe.py:7, :10; dev_pcc2.c:293-296 "#512: the C040 test used to sit HERE ... now lives beside the MIEN test"; the probe's :240-241 corrects only the message string | Fold into `pcc2contractstale` (OB:23660; a member of class row `astraharnesslow`, ledger.json:56292), which covers the same header's CONTRACT paragraph (:52-56) |
| F15 | grok | pcc2_width_probe.py:851 says a landed GENCTL write carrying C040 "ends the host" | CONFIRMED (RC) | READ pcc2_width_probe.py:850-852; the same claim at :370-372, :824-826 (the `c040ok` rationale) and the printed NOROW :1383-1384 "still ends the host". #556 corrected only :410-413 (hpcc2widthprobe:F4, HD:979) | Extend the hpcc2widthprobe:F4 correction to these four sites |
| F16 | grok | pcc2widthkills and pcc2c040kill share the GENCTL arm (:507-516) but are two predicates; no pair of the four rows is one defect | DISPOSED | READ ledger.json:34150 "the C040 bit; that is [[pcc2c040kill]], a separate row"; OB:15402-15404; dev_pcc2.c:508-515 | none |
| F17 | grok | The note's citation of mvme_pcctworeg.h:9-10 (CSRs accessible at 8/16/32 bits) was "not opened" | REFUTED (record holds) | READ mvme_pcctworeg.h:9-10 "...can be accessed as bytes (8 bits), two-bytes (16 bits), or four-bytes (32 bits)." | none |
| F18 | grok | vmedefaultkill: "installs it unconditionally on a machine this project actively boots" | CONFIRMED (RC) | READ machine_mvme88k.c:83, :95-96 (MVME187 arm only); :127-135 install no vme; dev_pcc2.c:92-93 "no mvme187 boot runs in this harness". ledger.json:45732 later narrows the install site but never "actively boots"; OB:18823-18824 corrects neither | Fix OB:18823-18824 and the note: gate_arm.sh constructs mvme187 for cold-debugger probes; no boot |
| F19 | grok | The note's finding (A), "a byte or halfword read at 0x89-0x8b ... returns 0x67000000", is unobservable (grok's reason: `exit(1)` runs first) | CONFIRMED (RC) | READ: (A) explicitly concerns the code after `exit(1)` is deleted ("DELETING `exit(1)` DOES NOT GIVE ZERO READS"), so grok's reason misses its scope. (A) is still wrong: dev_vme.c:65-66 loads `odata = d->reg[...]`, but memory.c:104-108 (big-endian) delivers only the low `len` bytes, so from the reset VBR word 0x67000000 (dev_vme.c:161-162; mvme88k_vme.h:257-260) a byte or halfword read at 0x89-0x8b returns 0x00 / 0x0000 (author checked). REASONED: a nonzero alias needs a guest VBR write with nonzero low bytes. The owner-ruling paragraph repeats the error | Correct (A) and its repeat. `vmewidthlanes` (ledger.json:62462) already carries the correct lane rule |
| F20 | grok | OB:18827-18828 still says `return 0` gives "the bus error real VME hardware would"; the note's own seat text calls that unproved | CONFIRMED (RC) | READ OB:18827-18828; ledger.json:45732 "That hardware claim remains unproved ... The round's record must say it that way." | Correct OB:18827-18828 to "an access the emulator cannot service" |
| F21 | grok | The note's "every other unimplemented-register kill in this queue announces with `fatal()`" was not re-derived | REFUTED (record holds in substance) | READ (heuristic scan) src/devices/*.c: 102 statement-form `exit(1)` sites. dev_vme.c:143 is the only one whose nearest preceding announcement is `debug()`. 11 others announce with `printf()` (also always visible); the rest use `fatal()` | none. Optional wording: "a visible fatal()/printf()" |
| F22 | grok | The note's six-run list of uncased offsets (10/7/2/2/4/989) was "not re-walked" | REFUTED (record holds) | READ dev_vme.c:70-131 cases {0x00, 0x2c, 0x4c, 0x50, 0x54, 0x60, 0x6c, 0x80, 0x84, 0x88}; uncased words 0x04-0x28 = 10, 0x30-0x48 = 7, 0x58-0x5c = 2, 0x64-0x68 = 2, 0x70-0x7c = 4, 0x8c-0xffc = 989; total 1014 (VME_LEN :50) | none |
| F23 | grok | The 2026-10-09 measurement was not opened, and guest touches of uncased offsets "are not a source line in this tree" | REFUTED (record holds) | READ run_HEAD.out "NO (rc=1)" at all 7 sites; run_FAULT.out "0x00000018" at all 7 and "PFSR(r10)=0x00000000 PFAR(r12)=0x00000000"; run_DECLINE.out reads 0x00000000, liveness 0x1234. Guest source (outside git) _guest-src-openbsd22/.../dev/vme.c:452, :467, :480, :482, :494, :576, :581 | none. Whether a real boot travels these paths is still unmeasured, as the note says |
| F24 | grok | The note cites machine_mvme88k.c:35 for the board's Ethernet; :35 is the MPU/CMMU line | CONFIRMED (RC) | READ machine_mvme88k.c:35 "88100 MPU, two MC88200..."; :37 "82596CA LAN Ethernet"; :105-106 "ie0 ethernet: TODO" -> unreadable. Unchanged since import, so it was wrong when written | Change :35 to :37, or cite by text |
| F25 | grok | No regress probe or gate reaches dev_vme.c | CONFIRMED (BP) | READ `git grep -e dev_vme -e vmedefault -e VME2_ -e vme_sites e483d931` over regress (artifacts excluded) -> rc=1; the rung-3 probe exists only as tracked artifact `regress/artifacts/vmedefaultkill/measure_20261009/vme_sites_probe.py.txt` | The round builds and wires its detector; gate_arm.sh already drives mvme187 (:1688, :1739) |
| F26 | grok | grok's fact table lists ten "named registers with a header offset and no case" | REFUTED | READ mvme88k_vme.h:46-81: 36 named offsets from 0x00 to 0x8c, ten cased, so 26 named and uncased. grok omits SADDR2, SLAVELMOD1/2, SLAVECTL, MASTER1/2, DMAMODE..DMASTAT, SETSOFTIRQ, IRQL1/2, MISC | The brief must not inherit "ten". Population 2 remains the six registers the guest touches |
| F27 | grok | vmedefaultkill and vmewidthlanes share the `default:` exit site (dev_vme.c:137-143) | DISPOSED | READ ledger.json:45732 "Populations 3 and 4 are filed as vmewidthlanes"; :62462 | none |

---

## of_two  (rows ofopenexit, ofpeerexit; grok 8 FLAGs; agy: none; Argon: not yet)

Files read (helper), @e483d931 unless another commit is named:
- `src/promemul/of.c`, `src/include/of.h`, `src/include/misc.h`, `src/cpus/cpu_ppc_instr.c`, `src/cpus/cpu_arm_instr.c`,
  `src/machines/machine_macppc.c`, `src/machines/machine.c`, `src/core/main.c` (grep).
- CHANGELOG.md and REVIEW_FINDINGS.md (grep).
- D, `astraretro_20260926/adjudication/grok_20261002/grok_rule3h.txt`;
  `astrafiling_20261002/grok/{grok_filehigh,grok_filehigh2}.txt`, FILING_REPORT.txt (grep),
  `afile_01/codex_afile_01.txt`; `regress/artifacts/queuetriage/codex_exitaudit_20260910.txt`.
- `git grep` over regress (artifacts excluded); the 1202d342 diff; 8ea26abb:OB and of.c/of.h blob hashes;
  39748e3c:src/promemul/of.c.

Author spot-checks: of.c `exit(1)` census (seven calls: :394, :448, :549, :577, :1100, :1120, :1201; :1185 is a comment);
of.c:383-396, :1076-1104; cpu_ppc_instr.c:3950-3962, :4394-4406; cpu_arm_instr.c:985-995, :5026-5040; of_emul_init callers
(only machine_macppc.c:99, after the `prom_emulation` gate at :93-94); main.c:442-443 (`-Q`); machine.h:206-210 (`md` is a
union of arc/pmax/of_data; only MIPS machines set arc/pmax); machine.c:66-67 (memset). Ledger and OB grep for `of_emul`,
`of_data`, `44ee0002` and `ef8c64be` returned no row.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok | `ofopenexit` gives no path:line in its title, its OB heading or D:945 | CONFIRMED (RC) | READ ledger.json:58801; OB:22952; D:945 have no line. The site is of.c:446-448 `if (s[0]) { printf("Unimplemented OF_SERVICE(open)..."); exit(1);`, already at grok_filehigh.txt:34 | Add `src/promemul/of.c:446-448` to the title and the OB heading |
| F2 | grok | "any nonempty pathname" does not hold when the first guest byte is unreadable | CONFIRMED (BP) | READ of.c:428-432: a failed memory_rw breaks before :438 `s[s_len++] = ch;`; :444 `s[s_len] = 0;`; :446 `if (s[0])`; :451 `return 0;` | Brief predicate: it exits iff the byte at OF_GET_ARG(0) is readable and nonzero. The unreadable pointer is a ready control row |
| F3 | grok | `of__open` (and `of__peer`) run only when nargs == 1 and nret == 1; any other arity stops the CPU rather than exiting | CONFIRMED (BP) | READ of.c:1070-1071 (`"peer"` / `"open"`, 1, 1); :1170-1171 `strcmp(...) == 0 && nargs == os->n_args && nret == os->n_ret_args`; :1178-1186 unknown service -> `cpu->running = 0;` | Both briefs state the one-in/one-out gate |
| F4 | grok | grok_rule3h.txt:77 cites the skeletal-OF "NOT a safety bug" sentence at OB:2742-2743; it has moved and does not name these exits | CONFIRMED (BP) | READ 8ea26abb:OB:2742-2745 = HEAD OB:2753-2756 "Known residual (NOT a safety bug...): macppc OpenFirmware is skeletal ... `getprop` gaps". HEAD :2742-2743 is the NE2000 note | Brief cites :2753-2756; that label covers the getprop stall, not of.c:394/:448 |
| F5 | grok | `ofpeerexit`'s "handle is not the root" is wrong: the code special-cases handle 0, and the root is handle 1 | CONFIRMED (RC) | READ of.c:385-388 `if (handle == 0) { /* Return the handle of the root node (1): */ ... return 0; }`; :391-394 OF_FIND miss -> exit(1); :968-969 "Root = device 1"; exact form already at grok_filehigh2.txt:13 | Retitle: "...when the handle is nonzero and no OF device carries it" |
| F6 | grok | D:956's "five other `exit(1)` sites" leaves out :448, so its census does not match the file | REFUTED | READ seven `exit(1)` calls (author checked). :448 is bundle_promemul:F1, ruled in the same ruling (grok_rule3h.txt:76-77, :90; D:945); D:956 counts the sites "seen and left untraced", which are exactly the other five | none |
| F7 | grok | D:956's ":1185 says one of them exists to defeat the debugger" misreads the #219 comment | CONFIRMED (BP) | READ of.c:1184-1186 "#219: ... cpu->running=0 already halts cleanly ...; the exit(1) only defeats the debugger." + `cpu->running = 0;`. The comment describes the exit #219 REMOVED (39748e3c:of.c:1170-1171), not any of the five | The brief drops that clause; optionally add a dated note on `ofpeerexit` |
| F8 | grok | D:956 says the peer exit is absent from OB and DISPOSITIONS, but it is at OB:22973 now | DISPOSED | READ OB:22973 and ledger.json:61044, filed by 1202d342 (#554); D:956 is ruling text written before the filing | none |
| F9 | grok | grok's fact table lists of_emul's `of_data == NULL` -> `exit(1)` at :1100 among "init or dispatcher failures"; it is guest-reachable | CONFIRMED (FILE) | READ of.c:1096-1100 `if (of_data == NULL) { fatal(...); exit(1); }`. The trap words decode with no privilege or machine test: cpu_ppc_instr.c:4400-4402 `if (iword == 0x44ee0002) ... instr(openfirmware)`; cpu_arm_instr.c:5034-5036 `else if (iword == 0xef8c64be) ... instr(openfirmware)`. `md.of_data` is set only at of.c:1078 in `of_emul_init`, called only at machine_macppc.c:99 after `if (!machine->prom_emulation) return;`. The `md` union is otherwise set only on MIPS machines, and the machine struct is memset (author checked). :549/:577 are init-only and :1120/:1201 dead (helper). No existing row | FILE a new HIGH row: one guest instruction (user mode included) exits the host on every ARM machine and on every PPC machine except macppc with prom emulation. Could share a round with the two OF rows |
| F10 | grok | Whether a real NetBSD/macppc boot issues OF `open` or `peer` is unknown (neither row has a witness) | CANNOT SETTLE | READ: regress (artifacts excluded) has 0 hits for of_emul, of__open, of__peer or the trap word; gate_ppc.sh:165 and gate_ppc_halt.sh:60 "never executed"; no "Unimplemented OF_SERVICE" record | One `-E macppc -e g4` boot of netbsd401-macppc-GENERIC (gate_ppc.sh:162), watching both diagnostics. REASONED: rung 3 needs no boot (machine_macppc.c:152-154 plants the trap word) |
| F11 | grok | :448 and :394 are two sites, not one defect | DISPOSED | READ of.c:446-448 vs :391-394; already separate rows (ledger.json:58800, :61044) | none |

---

## pvr_gdrom_four  (rows pvrdirtyregion, pvrrenderexit, gdromcondhow, gdromdmareentr; grok claims 17 FLAGs; agy: none; Argon: not yet)

Files read (helper), all @e483d931 unless another commit is named:
- `src/devices/dev_pvr.c`, `src/include/thirdparty/dreamcast_pvr.h`, `src/devices/dev_fb.c`, `src/cpus/memory_rw.c`,
  `src/cpus/memory_sh.c`, `src/core/memory.c`, `src/core/debugmsg.c`, `src/devices/dev_dreamcast_gdrom.c`,
  `src/devices/dev_dreamcast_maple.c`.
- `regress/gdrom_cond_probe.py` (also @7440e129, @1329d894, @3d7c61bb), `regress/gdrom_default_probe.py`,
  `regress/gate_sh_rounding.sh`, `regress/gate_hygiene.sh`.
- D, `astraretro_20260926/devpvr/codex_devpvr.txt`, `adjudication/fable_batch1a_ruling.md` (grep),
  `panel_high/{SEATS_20260930,IDMAP}.md`, `panel_high/seats_20260930/{agy_dev,grok_dev}.txt`; HD;
  `astrafiling_20261002/{afile_07/codex_afile_07.txt, briefs/afile_07.md, FILING_OVERLAY.tsv}`.
- db8b1a33:OB; the 1202d342 OB diff; `git grep` over top-level `regress/*.py` and `*.sh`.

Author spot-checks: dev_pvr.c:1080-1086, :1225-1226, :1307, :1412-1420; gdrom_cond_probe.py:408-437, :500-517.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok | grok read the working tree, not e483d931, so its line numbers are working-tree numbers | CONFIRMED (BP) | READ `git diff --stat e483d931`: of grok's files only ledger.json, gate_sh_rounding.sh and gdrom_default_probe.py differ. Its ledger and gate_hygiene lines still match HEAD. Its gate_sh_rounding :1253/:1258/:1301-1302 are HEAD :1243/:1248/:1291-1292. Its gdrom_default_probe.py :1527-1534/:1599 do not exist at HEAD (1418 lines): the accept session is :1339-1345, and the row at :1400 checks only `"Transfering" in t and alive` | Brief uses HEAD lines, not grok's |
| F2 | grok | The filing commit and its OB diff were not verified | REFUTED (doubt settled) | READ: the oldest `git log -S'"id": "<id>"'` hit is 1202d342 for all four ids (#554, 2026-10-02 14:47); its OB diff adds the four headings | none. The brief may cite 1202d342 |
| F3 | grok | No two of the four rows are one defect | CONFIRMED (BP) | READ: distinct sites (dev_pvr.c:2307-2338 vs :868/:1084/:1245/:1419; gdrom_cond_probe.py:428/:508 vs dev_dreamcast_gdrom.c:1502-1503). The nearby rows (pvrpal8888trunc, gdromdmawidth, gdromdmaflood, gdromdmaxferflood, storesidedead, ptywaitstatus) are each a different defect | No merge |
| F4 | grok | pvrdirtyregion's title and state_note cite no path:line for the function, the division, the zero-width formula, DIWADDRL or SIGFPE | CONFIRMED (RC) | READ ledger.json:58184 row, OB:22925-22926 and D:723: no path:line anywhere. The original finding has them: devpvr/codex_devpvr.txt:6 ("dev_pvr.c:2629 ... An aligned alternate-VRAM word write ... divides by zero at :2325") | Add dev_pvr.c:2307-2338, :2325-2326, :572-589 and :2629 to the row; cite codex_devpvr.txt:6 |
| F5 | grok | pvrdirtyregion's title is truncated at "with ordinary geometry..." | CONFIRMED (RC) | READ ledger title and OB:22925 end "with ordinary geometry..."; the full text is in the state_note and D:723 | Complete the ledger title and OB:22925 from D:723 |
| F6 | grok | "SIGFPE" is never observed and is a host-specific outcome | CONFIRMED (BP) | READ ledger witness ""; no artifact dir; dev_pvr.c:2325 `new_y1 = low / bytes_per_line;` has no zero test. REASONED: division by zero is undefined behaviour in C; SIGFPE is the x86-64 outcome, and an AArch64 divide returns 0 | Brief: SIGFPE is a prediction; a witness is owed (a run settles it) |
| F7 | grok | "any multi-byte VRAM write" fits the handler paths, but the plain window's dyntrans fast path feeds the tick a page-rounded range | CONFIRMED (BP) | READ dev_pvr.c:2686-2689 (DM_DYNTRANS_OK + WRITE_OK); memory_rw.c:536-546 (running min/max of `paddr & ~offset_mask` / `paddr \| offset_mask`); memory.c:280-288; dev_pvr.c:2408-2410; memory_sh.c:373-376. REASONED: a one-byte store in DIWADDRL's page, or two stores in pages either side within one tick, also straddles | Brief names the tick as a third caller with a wider trigger set |
| F8 | grok | Zero width is reachable only with pixelmode 2 or 3, DIWSIZE DPL 0 and DIWCONF_LR | CONFIRMED (BP) | READ dev_pvr.c:576 `(d->xsize + 1) * sizeof(uint32_t)`, :579-584 (bpp), :586 `/= bytes_per_pixel`, :588-589 (LR `/= 2`): 4/3 and 4/4 give 1, then 0. Seven arms recompute the geometry (:1772, :1785, :1813, :1825, :1837, :2044, :2106) | Brief carries the exact zero-width condition |
| F9 | grok | The inverted-region discard happens only when the update rect is empty; a power-of-two stride clamps to 0 | CONFIRMED (BP) | READ dev_pvr.c:2328 `if (d->fb_update_y1 < 0 \|\| new_y1 < d->fb_update_y1)`. The rect is reset to -1 at :2453-2454 and :2575-2576 (after every redraw), so empty is its normal state; :2333-2334 clamps only a negative y1. REASONED: on a non-empty rect, the rows above it are silently not redrawn (partial loss) | Brief states both cases |
| F10 | grok | pvrrenderexit's OB:2721-2723 no longer points at the med-DoS paragraph (now :2731-2733) | REFUTED | READ db8b1a33:OB:2721-2723 is exactly "...render/texture-loop `exit(1)`s (med DoS): lines 868...", and the title qualifies its cite "at db8b1a33" (OB:24108, :24139 agree) | none. The brief may add HEAD :2731-2733 |
| F11 | grok | :1084 is a single check before the command loop, not inside a loop | CONFIRMED (RC) | READ dev_pvr.c:1082-1085 at the top of pvr_render (`if ((fb_render_cfg & ...MASK) != 0x1) { printf(...); exit(1); }`); the loop starts at :1174. Title "render and texture loops" and OB:2731 "...loop `exit(1)`s ... 1084"; the deferral reason (OB:2732-2733) does not describe :1084 | Title and OB: three loop exits (:868, :1245, :1419) plus one pre-loop config exit (:1084) |
| F12 | grok | One STARTRENDER write with the default render config reaches :1084; no TA command is needed | CONFIRMED (BP) | READ dev_pvr.c:1672-1675 (STARTRENDER calls `pvr_render`); no gate (:1616-1644); DEVINIT memset (:2673); `pvr_reset()` is an empty TODO (:1447-1450); `pvr_reset_ta()` writes only DIWCONF (:1437). So FB_RENDER_CFG stays 0 and :1082 exits (mask 0x07, dreamcast_pvr.h:140) | Brief: the rung-3 witness for :1084 is one guest store |
| F13 | grok | Fact table: list commands 2, 3, 5, 6 and 7 hit the default; zwrite is at :1226; the mode-1 precondition covers only :868 and :1245 | REFUTED | READ dev_pvr.c:1307 `case 7:	// vertex`, so only 2, 3, 5 and 6 reach :1417-1419; `zwrite =` is at :1225 (author checked); :1082-1085 runs before all three loop exits including :1419; :868 is further gated at :764 and :766 | Correct these in the brief's fact table |
| F14 | grok | gdromcondhow's title cites moved: :419->:428-429, :499->:508-509, :410-411->:416-417, :493->:502-503, :224-233->:227-235 | CONFIRMED (RC) | READ 7440e129:gdrom_cond_probe.py: :419 `row("R1b a88 trk"`, :499 `row("R2b cond trk"`, etc. Correct when filed (1202d342, 14:47); #556 (1329d894, 18:09) inserted notes. HEAD :428, :508, :416, :502, :227 (author checked :408-437, :500-517). Only the state_note says "at 7440e129" | Add "at 7440e129" to the title's cites, or re-key them to anchors such as `row("R1b a88 trk"`; the brief uses HEAD lines |
| F15 | grok | R3 (:436) and R4 (:516) also omit `how`, so R1b/R2b are not the only decline rows without the survival check | CONFIRMED (FILE -> fold into `gdromcondhow`) | READ gdrom_cond_probe.py:433-436 and :513-516 count diagnostics only (`row("R3 a88 x3", "%d" % t.count(A88_TEXT), "1"`); only R1 (:416), R2 (:502) and R13 (:970) carry `how`; the probe's own rule at :410-412 says "a decline row asserts BOTH". REASONED: an exit that fires only after the latch is set passes every row | Fold R3/R4 into gdromcondhow's scope (its HIGH rule question is already open) |
| F16 | grok | "the destination inside the trigger window" is broader than the truth: only a transfer starting exactly at +0x18 recurses | CONFIRMED (RC) | READ dev_dreamcast_gdrom.c:1696-1697 (window 0x005f7400, length 0x80); :1387 `case 0x18:`; :1626-1630 (unaligned offsets return before the tail); memory_rw.c:494, :587-589 dispatch once at the start offset. Already stated at panel_high/seats_20260930/agy_dev.txt:73 and briefs/afile_07.md:56, but the title and OB:22874 kept "inside the trigger window" | Title: "the masked destination is exactly 0x005f7418" |
| F17 | grok | The recursion needs a nonzero byte in `d->data[0..7]`, not "a staged word" | DISPOSED | READ D:292 "re-entry is data-dependent (bytes 0..7 of the staged data fold into the trigger value)"; memory.c:71-75; agy_dev.txt:11-12 | none (optionally fix the title wording together with F16) |
| F18 | grok | Witness idea: a staged TOC aimed at +0x18 has a nonzero first byte | DISPOSED | READ D:292-293 "a diskless TOC staging sequence reaches it"; dev_dreamcast_gdrom.c:753 `memset(d->data, 0xff, d->cnt)`, :755 `d->data[0*4] = 0x10` | Carry into the brief as the witness recipe |
| F19 | grok | Host-stack exhaustion was never measured, and the arm itself calls no exit() | CONFIRMED (BP) | READ ledger.json:56468 witness ""; no artifact dir; fable_batch1a_ruling.md:134 is a reading. The re-entrant length is cut to 0x68 (memory_rw.c:523), while the arming words and `d->data` are unchanged (:1389-1395; `idata = 0` only at :1507) | Brief: "exhausts the host stack" is REASONED; a rung-3 witness is owed (a run settles it) |
| F20 | grok | The "Transfering" fatal() prints on every entry, every recursion level included | DISPOSED | READ rows `gdromdmaxferflood` and `gdromdmaflood` (both MED, open) describe the unlatched fatal() at dev_dreamcast_gdrom.c:1497-1499 | none here |
| F21 | grok | Maple sibling: dev_dreamcast_maple.c:264-265 writes to a guest-chosen receive_addr with PHYSICAL and was not traced for re-entry | REFUTED | READ maple.c:265 `4, MEM_WRITE, NO_EXCEPTIONS \| PHYSICAL);` (all 12 Maple memory_rw calls carry NO_EXCEPTIONS); memory_rw.c:241 and :584-585 call a handler under NO_EXCEPTIONS only for DM_READS_HAVE_NO_SIDE_EFFECTS devices; Maple (:653-654) and GD-ROM DMA (:1696-1697) are DM_DEFAULT | No row |
| F22 | grok | The palette load at dev_pvr.c:838 is a separate defect | DISPOSED | READ row `pvrpal8888trunc` (MED, open) "dev_pvr.c:838 loads a 32-bit palette entry into `uint16_t c32`" | none |
| F23 | grok | No top-level probe or gate reaches pvr_extend_update_region, pvr_render, or a GD-ROM DMA aimed at its own +0x18 | CONFIRMED (BP) | READ `git grep -i -E 'pvr\|STARTRENDER\|DIWADDR\|texture_pixelformat'` over top-level regress finds only the SH4 CPU's own PVR register and a comment; `git grep 5f7418 -- regress` returns 0; the DMA destinations used are 0x11223344 and 0x0c008000 | All three device rows owe a rung-3 witness; gdrom_default_probe.py:1332-1348 is the nearest template |

---

## net_three  (rows ne2krxbudget, taprxquota, tcpdebugopts, dectxzero; grok 11 FLAGs; agy: none; Argon: not yet)

Files read (helper), all @e483d931 unless another commit is named:
- `src/net/{net,net_tap,net_ip}.c`, `src/include/{net,misc}.h`, `src/core/debugmsg.c`, `src/include/thirdparty/tulipreg.h`,
  `src/devices/{dev_ne2000,dev_dec21143,dev_le,dev_ether,dev_sgi_mec}.c`, `src/include/testmachine/dev_ether.h`,
  `src/machines/machine_arc.c`, `machine_pmax.c` (grep).
- `regress/gate_build.sh`, `gate_hygiene.sh` (grep); CHANGELOG.md (grep); D.
- db8b1a33:OB; `git log -S`; the 1202d342 OB diff; `git status --porcelain` (metadata only).

Author spot-checks: dev_dec21143.c:272-310, :350-372; a ledger sweep of every DEC21143/tulip mention (no RX-drain row).

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok | grok read the working tree, so its line numbers were unchecked against HEAD | REFUTED (doubt settled) | READ `git status --porcelain`: none of the cited src files is modified. Every source line re-read at e483d931 matches, as do ledger.json:57283/:58427/:58647/:61133. One fact-table slip: net_ip.c:653 is `goto ret;` | none |
| F2 | grok | grok did not run the filing-commit pickaxe; it guessed 1202d342 from the reflog | REFUTED (doubt settled) | READ `git log -S` -> 1202d342 for all four ids; its added headings equal HEAD OB:22895/:22934/:22937/:22976 | none |
| F3 | grok | No two of the four rows are one defect: ne2krxbudget and taprxquota meet at `net_ethernet_rx_avail`; tcpdebugopts and dectxzero share dec21143's TX buffer | CONFIRMED (BP) | READ dev_ne2000.c:452 `while (net_ethernet_rx_avail(net, &d->nic))` vs net_tap.c:107 `for (;;)`; dev_dec21143.c:788-789 `realloc` vs net_ip.c:443 `for (i=34+20; i<data_offset; i++)` | Keep four rows; cross-reference the two pairs |
| F4 | grok | ne2krxbudget and taprxquota state the mechanism with no path:line ("the lines are only in untracked DISPOSITIONS.md:886/:889") | CONFIRMED (RC) | READ ledger.json:58427/:58434/:58647/:58654: no path:line. But `git cat-file -e e483d931:regress/artifacts/astraretro_20260926/DISPOSITIONS.md` exits 0, so D is TRACKED; grok's "untracked" is wrong | Add dev_ne2000.c:333-341, :450-473; net_tap.c:104-135; net.c:293-295 to the rows |
| F5 | grok | D:886's `net.c:302` is wrong as a universal ingress mechanism | REFUTED | READ D:886 "net.c:302 polls distributed-network input again on every iteration": already limited to distributed mode | No record correction |
| F6 | grok | On TAP, rx_avail returns at net.c:293-296 before :302; sustained TAP input is taprxquota's loop inside the first rx_avail call | CONFIRMED (BP) | READ net.c:293-295 `if (net->tapdev) { net_tap_rx_avail(net); return net_ethernet_rx(...)`; non-TAP refill at :302-330 (distributed) and :334-335 (NAT) | Brief names the refill path per mode (TAP, distributed, NAT) |
| F7 | grok | The title's "per-tick" misses the second caller: the tick also runs at the end of register accesses | CONFIRMED (BP) | READ dev_ne2000.c:649-650 `done: dev_ne2000_tick(cpu, extra);`; :531 and :540 return before it; :438-440 | A witness can drive the loop from a register access |
| F8 | grok | Among sibling NICs, "none is the invalid-ring / OVW-clear / no-budget shape" | REFUTED (in part) | READ dev_dec21143.c:356-366 `while (d->cur_rx_buf == NULL) { if (!net_ethernet_rx_avail(...)) return 0; ... if (dec21143_rx_drop_packet(...)) continue;`. The drop frees and NULLs the buffer (:301-306), and drops EVERY packet until a setup frame arrives (:295-301; `d->drop_packet == NULL` always drops). It is TAP-only (:276-277) and has no budget (author checked). grok is right about LANCE (dev_le.c:719-720). No ledger row names dec21143_rx or rx_drop_packet (author checked) | Action: FILE candidate, or fold into ne2krxbudget (panel decides). An unbudgeted RX drain on the DEC21143 under sustained TAP input |
| F9 | grok | taprxquota treats every nonnegative `read` as the hang condition, but the tree does not show a TAP returns 0 | DISPOSED | READ D:901 "Whether a TAP can deliver a zero-length frame ... is UNSETTLED; settling it takes ..."; net_tap.c:128-129 (0 -> continue), :131-135 | none |
| F10 | grok | `net_tcp_rx_avail` has the same never-incremented counter, but its loop is bounded | CONFIRMED (BP) | READ net_ip.c:1487 `int received_packets_this_tick = 0;`, tested at :1497 with no `++` in :1485-1650; loop :1491 bounded by MAX_TCP_CONNECTIONS (net.h:126 = 100). No record names it | Sibling line in taprxquota's brief (dead cap, bounded loop) |
| F11 | grok | tcpdebugopts: HEAD OB:2731 is the dev_pvr bullet; the TCP clause is at :2741 | CONFIRMED (BP) | READ db8b1a33:OB:2731 "TCP-debug options over-read (`net_ip.c`, debug-verbosity only)", so the pin is correct; HEAD :2741 has the same text | Brief cites HEAD :2741; no correction (the pin names its commit) |
| F12 | grok | `dev_ne2000.c:278` is the buffer declaration; the 2048 is at :117 | REFUTED | READ :278 `unsigned char buf[NE_MAX_TX];`, :117 `#define NE_MAX_TX 2048`; the title's ":278 is a 2048-byte buffer" is accurate | none (optionally add :117) |
| F13 | grok | The dec21143 cite `:788-809` misses the first-segment allocation at :772-773 (single-segment frames included) | CONFIRMED (RC) | READ dev_dec21143.c:772-773 `malloc(bufsize == 0 ? 1 : bufsize)`, :802, :808-809 transmit: an exact-length allocation outside the cited range | Cite `dev_dec21143.c:772-809` in ledger.json:61133 and OB:22976 |
| F14 | grok | dev_ether and dev_sgi_mec also transmit from fixed arrays, so they are unaffected | CONFIRMED (BP) | READ: there are 5 `net_ethernet_tx(` callers (dec21143.c:808, ether.c:171, le.c:438, ne2000.c:303, sgi_mec.c:358); dev_ether.c:54 `buf[DEV_ETHER_BUFFER_SIZE]` (0x4000); dev_sgi_mec.c:91 `cur_tx_packet[MAX_TX_PACKET_LEN]` (1700) | Brief census: exact-length buffers in dec21143 and le; fixed arrays in ne2000, ether, sgi_mec |
| F15 | grok | Reaching the TCP dump needs more than NET debug: no TAP, an IPv4/TCP frame to the gateway, len >= 54, data-offset nibble >= 6 | CONFIRMED (BP) | READ net.c:432-434 (TAP returns before `net_ip`); net.c:484-486; net_ip.c:982 `packet[14] == 0x45`; :988 `(packet[23] == 6 && len < 54)`; :443 | The title's CONDITIONAL lists only verbosity; the brief adds these |
| F16 | grok | dectxzero's "glibc answers realloc(p, 0) with NULL" has no in-tree citation | CANNOT SETTLE | READ dev_dec21143.c:788-789 and misc.h:190-192 (exit only on NULL). No record measures `realloc(p, 0)`; OB:8961 covers only `malloc(0)` ("Harmless on glibc (unique non-NULL)") | One run on the Gentoo build host: `printf("%p\n", realloc(malloc(1), 0))` |
| F17 | grok | (in passing) dectxzero's state_note is a 400-character cut that starts mid-sentence in another finding | CONFIRMED (RC) | READ ledger.json:57290 begins "re 160/320/640, not 80 (80 is text mode) -- wording only." (the tail of vgadirtyarm, D:377-381) and ends inside mbcdbincomplete (D:384). Same cause as loaders_four/F1 (mk_filing.py.txt:187) | Re-cut to D:382-383; a class decision with loaders_four/F1 |
| F18 | grok | (fact table) For a continuation with no first segment, the :781 fatal does not exit and falls through to `realloc(NULL, len)` | CONFIRMED (BP) | READ dev_dec21143.c:780-789 `if (d->cur_tx_buf == NULL) fatal(...)`, then the same `realloc`; with len 0 that is `malloc(0)`. The fatal has no latch | Brief: a repair at :788 covers `realloc(p, 0)` and `realloc(NULL, 0)` |
| F19 | grok | No regress probe or gate reaches any of the four paths | CONFIRMED (BP) | READ: case-insensitive git grep over regress for ne2000, dec21143, tulip, net_tap, net_ip, net_ethernet, rx_avail, tapdev, lance, cur_tx_buf finds only gate_build.sh:167-170 comments. The arc rig instantiates the NE2000 (machine_arc.c:209-212) and pmax adds LANCE (machine_pmax.c:129) | No witness exists; the arc and pmax rigs are candidate vehicles |

---

## loaders_four  (rows ecoffoffsetspan, emulgzipfail, symdemanglebound, i960disasmspan; grok 11 FLAGs; agy: none; Argon: not yet)

Files read (helper), all @e483d931 unless another commit is named:
- `src/file/{file,file_ecoff,file_elf,file_macho}.c`, `src/include/{misc,cpu,cpu_i960}.h`, `src/core/emul.c`,
  `src/symbol/{symbol,symbol_demangle}.c`, `src/machines/{machine,machine_playstation2,machine_pmax}.c`,
  `src/cpus/{cpu_i960,cpu_i960_instr,cpu_dyntrans,tmp_i960_head,tmp_i960_tail}.c`.
- CHANGELOG.md, REVIEW_FINDINGS.md; `regress/gdrom_data_probe.py`.
- D, `astraretro_20260926/adjudication/{fable_batch2c.md, grok_20260930/grok_check2c.txt, fable_brief_batch3g.md}`,
  `symbol/codex_symbol.txt`, `astrafiling_20261002/FILING.tsv` and `mk_filing.py.txt`.
- `git show 8dd86b5a -- src/file/file_ecoff.c`; `git log -L` on file_ecoff.c.

Author spot-checks: file_ecoff.c:268-286, :318-338 (`f_symptr` is `off_t`, :67); mk_filing.py.txt:78-86, :180-192 (tracked at
e483d931).

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok | The ecoffoffsetspan state_note does not quote its own bullet: it opens inside symdemanglebound's and ends inside ascwidecount's | CONFIRMED (RC) | READ ledger.json:57444 "...cut at 400 characters): disk image -- the fork's src/file threat model (#14-#66). * `ecoffoffsetspan`...". Generator: astrafiling_20261002/mk_filing.py.txt:187 `text[max(0, m.start() - 60):m.end() + 300]` and :83 `src=clean(src, 400)` (author checked). The 60-character lead-in is by design and the prefix does not declare it. Helper heuristic: in 122 of 190 GOVERNING TEXT notes the row's id first appears past character 20 (not a census) | Class fix, one mechanical pass: declare the lead-in in the prefix, or trim to the row's own bullet. No per-row edits. Same class as net_three/F17 |
| F2 | grok | The title over-claims: the guards admit a negative offset only when the table length covers its magnitude (<= 256 MB) | CONFIRMED (RC) | READ file_ecoff.c:322-326 `(uint64_t) f_symptr + (uint64_t) sizeof(struct ms_sym) * (uint32_t) f_nsyms > (uint64_t) file_size \|\| ... > LOADER_MAX_TABLE_BYTES` (author checked); :414-421 has the same shape; misc.h:217 (256 MB); OB:22904 "(the guards do not admit every negative value)" while :22901 has no condition | Retitle as conditional: offset fields 0xF0000000-0xFFFFFFFF whose magnitude the table length covers |
| F3 | grok | The row misses the first use of `f_symptr`: it is seeked unchecked at :278, and a short symhdr read exits at :284, before `file_size` and before either guard | CONFIRMED (BP) | READ file_ecoff.c:270 `if (f_symptr != 0 && f_nsyms != 0)`, :278 `fseek(f, f_symptr, SEEK_SET);`, :281-284 `exit(1);`, :300-304 file_size (author checked). Unchanged since the import (39748e3c). No other row names ECOFF | Fold into the ecoffoffsetspan scope |
| F4 | grok | The title drops the bullet's "or read the WRONG bytes" | CONFIRMED (RC) | READ D:451 "...short read, or read the WRONG bytes"; ledger.json:57437 ends "...on the resulting short read" | Add "or reads the wrong bytes" |
| F5 | grok | "#59/#62 skip-a-bad-table policy" carries no citation, and CHANGELOG credits skip-instead-of-exit only to #66 | REFUTED | READ REVIEW_FINDINGS.md:92 (#59) "bogus => graceful skip; add the missing `fread` check"; :95 (#62); file_ecoff.c:327-328 `fatal` then `goto skip_normal_coff_symbols` | none (cite REVIEW_FINDINGS.md:92/:95 if a brief quotes the policy) |
| F6 | grok | The MS-COFF short-read exit at :333-337 is the fread check #59 itself added | CONFIRMED (BP) | READ `git show 8dd86b5a` adds `if (fread(ms_sym_buf ...) != ...) { ... exit(1); }`; CHANGELOG.md:20851 | Brief: #59's skip policy is partly defeated by #59's own exit-on-short-read |
| F7 | grok | Whether `fseek` to a negative `off_t` gives a short read (exit) or reads other bytes depends on the host libc | CANNOT SETTLE | READ file_ecoff.c:278, :332, :428, :439 ignore the fseek return; :333-337, :429-431, :440-443 exit only on a short count | One run on the build host: `fseek(f,-16,SEEK_SET)`; print the return, errno and `ftell` |
| F8 | grok | emulgzipfail gives no file:line in its title, state_note, D:843 or OB:22931 | CONFIRMED (RC) | READ ledger.json:58405/:58412 and D:843: no path; emul.c:609-616 `if (decompress_gzip_to(...) != 0) { fatal(...); unlink(...); exit(1); }` | Add `src/core/emul.c:609-616` (helper :82-124) |
| F9 | grok | The exit covers all three `-1` causes of `decompress_gzip_to`, including fork, waitpid and exec failures | CONFIRMED (BP) | READ emul.c:86-88 (fork), :115-117 (waitpid), :120-123 (child status), :97/:110 `_exit(127)`. The host-side sibling `emulmkstempexit` was graded LOW (D:850) | Brief grades the input-driven case (valid magic, corrupt body) apart from host failures |
| F10 | grok | The probe comment's `emul.c:75-110` cites a helper that spans :82-124 | REFUTED | READ gdrom_data_probe.py:82; emul.c:72-81 is the doc comment, :84 fork, :105-107 execl/execlp: the span covers what it is cited for | none |
| F11 | grok | The symdemanglebound state_note ends mid-sentence at "from a" | DISPOSED | READ ledger.json:57422 prefix "cut at 400 characters" (declared); the full text is at D:446-449 | none |
| F12 | grok | `add_symbol_name` has callers outside the four loaders, including the nm-format reader at symbol.c:333 (`b4`, `%79s`) | DISPOSED | READ symbol.c:296 `char b4[80];`, :333; D:840 "symbol:F1 ... DUPLICATE-OF-ROW symdemanglebound"; codex_symbol.txt:4 | The symdemanglebound brief carries the folded fifth feeder (a stack buffer); the row names only "four loaders" |
| F13 | grok | The i960 trace/single-step path is only in the title; the bullet's `cpu_dyntrans.c:2011-2012` skips the disassemble while tracing, and the trace read is at :282-296 | DISPOSED | READ cpu_dyntrans.c:2011; :285-286 `instr[1 << DYNTRANS_INSTR_ALIGNMENT_SHIFT]` = 4 bytes (cpu_i960.h:42); ruling fable_batch2c.md:57 "the trace path cpu_dyntrans.c:285-296 hands a ... 4-byte buffer" | The brief cites :282-296 from the ruling |
| F14 | grok | The bullet's "the `bad:` path every instruction word takes" is false for readahead | REFUTED | READ the only setter is cpu_dyntrans.c:1944 (translate tail); i960's switch is only `default: goto bad;` (cpu_i960_instr.c:198-201), so :1990-1991 never fires for i960 | none (the breakpoint half is F15) |
| F15 | grok | A breakpoint hit skips `bad:` but disassembles the same 4-byte `ib` at cpu_dyntrans.c:1829: a third reader | CONFIRMED (BP) | READ cpu_dyntrans.c:1799, :1826-1829 `if (!cpu->machine->instruction_trace) { ... DISASSEMBLE(cpu, ib, 1, 0);`, :1848 | Fold into the i960disasmspan scope: three readers (:2012, :295-296, :1829) |
| F16 | grok | The i960disasmspan state_note ends at "a four-byte over" | DISPOSED | READ ledger.json:57070 (cut declared); D:306-307 "of the emulator's own stack feeding a diagnostic, after which the CPU stops" | Brief quotes D:306-307 |
| F17 | grok | i960disasmspan and OB-24 share cpu_i960.c:462/:464 but are different defects; OB-24 has no row | DISPOSED | READ D:326; OB:24159 "named in this file only: no ledger row of its own"; fable_batch2c.md:60 "Independent of F1" | none |
| F18 | grok | No pair of the four rows is one defect | DISPOSED | READ D:840; D:850 "Propose LOW `emulmkstempexit`"; OB:23320 | none |

---

## fb_vga_x11_five  (rows fbctrlcmdkill, fbsdrampair, vgadirtyarm, x11alloc32, dyncacheoffset32; grok 9 FLAGs; agy: none; Argon: not yet)

Files read (helper), all @e483d931 unless another commit is named:
- `src/devices/{dev_fbctrl,dev_fb,dev_footbridge (also @8ea26abb),dev_vga}.c`,
  `src/include/{thirdparty/dc21285reg.h,memory.h,devices.h,cpu.h,misc.h}`, `src/console/x11.c`,
  `src/cpus/{memory_rw,memory_arm,cpu_dyntrans,cpu}.c` (+ `git grep update_translation_table`), `src/core/{main,emul_parse}.c`,
  `src/machines/machine.c`, `regress/fbctrl_port_probe.py`.
- OB (also @8ea26abb :21964-21973, @db8b1a33 :5866-5882); D, `astraretro_20260926/bundle_console/codex_bundle_console.txt`;
  `astrafiling_20261002/afile_07/codex_afile_07.txt` and `briefs/afile_07.md`; `regress/artifacts/n6/p1_20260919/fable_p1_packet.md`,
  n6/p2_20260919 (grep).
- On disk: `_scratchpad/cxfarm4_20260919/out/codex_m2_sdramclass.txt` (untracked), `_scratchpad/dc21285.txt`.

Author spot-checks: dev_footbridge.c `exit(1)` census and :730-761; dev_vga.c:728-766; memory.h:149-151 (`size_t len`); the
VGA END-row arithmetic, recomputed; the fbdeclinefive / fbsdrampair rows.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok | fbctrlcmdkill's "any command other than 0-2" refers to the value stored as an `int`; a DATA write whose low 32 bits are 0/1/2 is serviced | DISPOSED | READ dev_fbctrl.c:51 `int port[...]`, :110 `uint64_t idata`, :150 `d->port[d->current_port] = idata;`; OB:22622-22623 "The DATA path's width handling ... belongs to this round too" | The brief carries it |
| F2 | grok | fbsdrampair's "HEAD :712, :737" no longer points at the reads | CONFIRMED (RC) | READ dev_footbridge.c:732/:757 are the case labels and :734-735/:759-760 `fatal` + `exit(1)` (author checked); :712 is inside the TIMER_1_CLEAR comment and :737 is `switch (idata) {`. Stale numbers at ledger.json:52840 and OB:22034; D:808 has the correct :732-735/:757-760 | Name the construct ("the SDRAM_BA_MASK / SDRAM_BA_OFFSET read arms"), or cite :734-735 / :759-760 at e483d931 |
| F3 | grok | dc21285.txt:5878 is Table 7-7's intro line; `8FFC0000h` prints at :5893 beside "128MB", and "No window" (:5895) has no value | CONFIRMED (BP) | READ dc21285.txt:5878 "Table 7-7 lists...", :5882 `00000000h` ... :5893 "128MB        8FFC0000h", :5895 "No window". Calibrated against dc21285reg.h:141 (`SDRAM_MASK_256KB 0x00000000`): extracted values sit one row above their labels; the prose is at :5867-5871 | No title change; the brief carries the row-offset check and cites the prose |
| F4 | grok | OB:24181 maps a different span of dc21285.txt (5868-5881) to this row | REFUTED | READ OB:24108 "(lines as of `db8b1a33` -> the id...)"; db8b1a33:OB:5868 "### The eight footbridge sites": bugs-file lines, not datasheet lines | none |
| F5 | grok | The census "seven guest-reachable exits remain (fbdeclinefive 5, fbsdrampair 2)" is stale | CONFIRMED (RC) | READ OB:2690-2692, :22029-22031; ledger.json:6103 ("now seven"). `fbdeclinefive` is closed on 4264ee20 (#545, 2026-09-23) (author checked); only dev_footbridge.c:735 and :760 remain as executable guest exits, plus DEVINIT :864/:900. The file is identical at 8ea26abb, so D:808's "two of the seven remaining" was stale at its own check commit | Dated note at OB:2690-2692 and :22031 ("overtaken by #545: two remain"); correct D:808 |
| F6 | grok | The title's credits to "codex M2" (0/2 backing fields, 0/2 consumers) and "fable5 D4" could not be verified | REFUTED (record holds) | READ disk:codex_m2_sdramclass.txt:83 "**0/2 backing fields** and **0/2 consumers outside these cases**"; ledger.json:6306 "D4: ... the SDRAM pair separate, member 3 by default"; :6287 | none. The M2 file lives only in `_scratchpad`; a durable copy is worth considering |
| F7 | grok | D:808 cites OB:21966-21972, but that text is now :22029-22036 | DISPOSED | READ D:806 "(mine, each checked at 8ea26abb)"; 8ea26abb:OB:21966-21972 holds it | none (dated cite) |
| F8 | grok | The vgadirtyarm state_note still says "~-1.7e9 dirty-row origin ... walks it for hours" though the title withdraws both | DISPOSED | READ ledger.json:57268 ends "[title corrected: Astra afile_07 (withdraws its earlier figures, holds HIGH on this basis)...]"; title :57261 | none |
| F9 | grok | The ~-1.7e9 origin is refuted because the START row is small (y >= about -819) | REFUTED | READ dev_vga.c:732 `int x, y, x2, y2, r, base;`, :740 `r = relative_addr - base;`, :741 y small (as grok says), but :743 `y2 = (r+len-1) / (d->max_x * 2);` with `size_t len` (memory.h:151) is computed in size_t; :764 `if (y2 < d->update_y1) d->update_y1 = y2;`, :765 `if (y2 > d->update_y2) ...`. REASONED (LP64, GCC modulo conversion; r = -2, len = 1; helper's arithmetic re-computed by the author): int y2 = -1717986919 at max_x 80, **-858993460 at 160** (the helper wrote +858993459 there, which was wrong), +1717986918 at 320, +858993459 at 640. Astra afile_07:100 holds HIGH on ":743,764-765"; :102 leaves the conversion UNSETTLED | BP: the ~-1.7e9 origin IS reproducible, through y2 (:743/:764), at max_x 80 (-0.86e9 at 160). At 320/640, y2 is a huge END row (:765) the graphics loop (:352) walks. Measure on the build host |
| F10 | grok | The state_note's producer clause is cut off at "ARM subp" | DISPOSED | READ ledger.json:57268 (400-character cut, declared); D:379-380 "ARM subpage/tiny-page translation (memory_arm.c:235); the one ARM machine with a VGA is cats" | none |
| F11 | grok | "Untracked ONLY through MEMORY_NOT_FULL_PAGE" is not established | REFUTED (record holds) | READ memory_rw.c:526-528 gates write tracking (:536-547) on `update_translation_table != NULL`, `!(ok & MEMORY_NOT_FULL_PAGE)` and DM_DYNTRANS_OK; all 11 CPU inits set update_translation_table; dev_vga.c:1314-1316; the only live producer is memory_arm.c:235 (memory_rw.c:339/:426 are inside `#if 0`) | none |
| F12 | grok | The graphics redraw at :352-356 runs only when `cur_mode != MODE_CHARCELL`; DEVINIT starts in MODE_CHARCELL | CONFIRMED (BP) | READ dev_vga.c:588-593 (text vs graphics update); :1277 `d->cur_mode = MODE_CHARCELL;`; a mode change resets the rectangle at :950-954 | Brief: the "hours" case needs graphics mode at tick time |
| F13 | grok | x11alloc32's title, state_note and OB:22928 cite no path | CONFIRMED (RC) | READ ledger.json:58383/:58390: no path; x11.c:441-442 `malloc((size_t)new_xsize * new_ysize * alloc_depth / 8)`, :446 memset; cap dev_fb.c:147-150; only caller :229; D:850 "`x11.c:632` is the second site of `x11alloc32`" | Add x11.c:441-446 and :632, dev_fb.c:147-150 and :229 |
| F14 | grok | The wrap occurs only at some colour depths and only at scaledown 1 | CONFIRMED (RC) | READ x11.c:428-432 (24 becomes 32, 15 becomes 16); dev_fb.c:202-203 divides by the scaledown, :902 takes it from `machine->x11_md.scaledown` (default 1, machine.c:90; `-Y` main.c:490-499); codex_bundle_console.txt:4 "With scale 1 and a 24-bit X display". REASONED (32-bit size_t): depth 32 wraps from side 11586; depth 16 only at 16384^2; depth 8 never | Retitle as conditional: scaledown 1 and X depth 24/32 with side >= 11586 |
| F15 | grok | `x11_fb_init`'s `alloclen` at x11.c:632 is "a different expression and not this row" | REFUTED | READ D:850 "`x11.c:632` is the second site of `x11alloc32`"; x11.c:632 `alloclen = xsize * ysize * alloc_depth / 8;` | Carry :632 into the row (F13) |
| F16 | grok | fbctrl command 1 (SET_RESOLUTION) passes guest-chosen X1/Y1 to `dev_fb_resize` -> `x11_fb_resize`: a guest route into x11alloc32 | CONFIRMED (BP) | READ dev_fbctrl.c:75-79 `x1 = d->port[DEV_FBCTRL_PORT_X1]; ... dev_fb_resize(d->vfb_data, x1, y1);`; framebuffer depth 24 (:177-179); dev_fb.c:153-165 passes 16384^2 at 24 bpp on 32-bit; dev_fb.c:229 makes the X call | Witness route: an ILP32 build with `-X`, a test machine, SET_RESOLUTION with sides 11586-16384 |
| F17 | grok | No pair among the five rows is one defect; `fbctrloffkill` is the separate offset sibling | DISPOSED | READ OB:22625 `fbctrloffkill`; dev_fbctrl.c:157-160 offset `default:`; fbsdrampair already covers both registers | none |
| F18 | grok | dyncacheoffset32 cites :797-833 as the call site, but the call is the `I` macro at :114 | DISPOSED | READ cpu_dyntrans.c:114 `#define I ic = ...next_ic ++; ic->f(cpu, ic);`; D:951 "`:830-833` publishes instruction pointers from it, and `:114` calls the resulting host function pointer" | Optionally add :114 to the title |
| F19 | grok | The dyncacheoffset32 state_note is cut down to a grade fragment | DISPOSED | READ ledger.json:58764 "...conditional on the oversized configured cache [title corrected: Astra afile_01, D:962, :966]"; full text at D:951/:962/:966 | none |
| F20 | grok | The chain walk and DYNTRANS_INVALIDATE_TC_CODE also read the truncated offsets, and a truncation to 0 collides with the end-of-chain marker | CONFIRMED (BP) | READ cpu_dyntrans.c:770-772 `while (physpage_ofs != 0) { ppp = ... translation_cache + physpage_ofs`, :787, :807, :1347-1362; cpu.h:82 `next_ofs; /* (0 for end of chain) */`; :606-610 (64-aligned cursor steps) | Brief carries the other readers and the end-of-chain collision (only if the cursor hits a multiple of 2^32) |
| F21 | grok | A product that wraps to exactly 0 becomes `malloc(0)`, whose result depends on the host, so the wrap alone is not an exit(1) | CANNOT SETTLE | READ x11.c:441 `CHECK_ALLOCATION(...malloc(...))`; misc.h:190-192 exits only on NULL. REASONED: the product is 0 only at 16384^2 for depth 16/32 | One run: `malloc(0)` on the target ILP32 libc (NULL means exit(1); non-NULL means an under-sized allocation) |

---

## cpu_policy_two  (rows qharmexalign, qhrdhwrpolicy; grok 12 FLAGs; agy: none; Argon: not yet)

Files read (helper), all @e483d931 unless another commit is named:
- `src/cpus/{cpu_arm,cpu_arm_instr,cpu_arm_coproc,cpu_arm_instr_loadstore,cpu_mips_instr,cpu_mips,cpu_dyntrans}.c`,
  `tmp_{arm,mips}_{head,tail}.c`, `src/include/{cpu_arm,cpu_mips,mips_cpu_types}.h`, `src/include/thirdparty/armreg.h`,
  `src/machines/{machine_test,machine_vocore,machine_pmax,machine_arc,machine_evbmips}.c`.
- OB, CHANGELOG.md, `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`.
- db8b1a33: OB, cpu_arm_instr.c, cpu_mips_instr.c, cpu_dyntrans.c; `git log -S`; the c29a5fd3 OB diff.
- On disk: `_scratchpad/ddi0100i.txt` (2,199,364 B), `_scratchpad/mips32_volII.txt` (775,072 B),
  `_scratchpad/agypack_20261013/mk_briefs4.py` and `mk_briefs5.py`.

Author spot-checks: cpu_arm.c:120-132; `git grep ARM_CONTROL_ALIGN`; OB:4208-4222; ddi0100i.txt:8609-8615; mips32_volII.txt:1233-1240;
cpu_mips_instr.c:5580-5598, :5672-5698; mips_cpu_types.h:96-108; cpu_mips.h:48-56; machine_test.c:406/:412; rows `armalignexc`
and `armsa1110areset`; mk_briefs4.py:12-20; HARVEST_AUTO.md:275.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok | The brief lists both rows as `(?, open)`, but the ledger says HIGH | CONFIRMED (BP) | READ ledger.json:61253, :61275 `"sev": "HIGH"`. The brief builder reads the wrong key: disk:_scratchpad/agypack_20261013/mk_briefs4.py:17 `r.get("severity", "?")` (the key is `sev`), reused by mk_briefs5.py; its `[:240]` cut also truncates titles. Already harvested with no disposition at HARVEST_AUTO.md:275 (armdesc3kill_prep) | Cross-job: fix the builder (`severity` -> `sev`). Every brief in this set shows "(?, open)". No queue row |
| F2 | grok | qharmexalign's title says both cited passages record LDREX and STREX, but passage 1 names only ldrex | CONFIRMED (RC) | READ db8b1a33:OB:3625-3626 "`ldrex` HALTS the / emulator on an unaligned address" (no strex); :4181-4202 names both; IDLESS_DISPOSITIONS.md:159 filed it as "unaligned ldrex stops the CPU" | Reword the title (ledger.json:61274, OB:23897): passage 1 records the ldrex halt, passage 2 both |
| F3 | grok | "This tree sits permanently at (A,U) = (0,0)" (HEAD OB:4213) is false | CONFIRMED (RC) | READ cpu_arm.c:128-129 `cpu->cd.arm.control = ARM_CONTROL_PROG32 \| ... \| ARM_CONTROL_ALIGN;` (0x0002, cpu_arm.h:305) (author checked); cpu_arm_coproc.c:135 `cpu->cd.arm.control = cpu->cd.arm.r[rd];`; :144-147 debug only; cpu_arm_instr.c:1689-1692 "nothing consults it". The same facts are filed as `armsa1110areset` and `armalignexc` (MED, open) | Correct OB:4213: A is SET at reset, guest-writable, stored and never consulted; there is no U. Cross-reference the two rows |
| F4 | grok | The passage's "choice under latitude" (OB:4218-4220) contradicts the title's "mandatory when (A,U) is not (0,0)" at the reset state | CONFIRMED (RC) | READ ddi0100i.txt:8611 "If CP15 register 1(A,U) != (0,0) and Rd<1:0> != 0b00, an alignment exception will be taken." and :8613-8614 (UNPREDICTABLE only at (0,0)) (author checked); also :14664. With reset A=1 (F3), the handlers never read `control` (cpu_arm_instr.c:2053-2057, :2098-2102) | Annotate OB:4218-4220: the latitude exists only while the guest-visible A and U are 0; at the reset value the abort is mandated, so the title governs |
| F5 | grok | The passage's ARM ARM quotations are unverifiable (ddi0100i is not in the tree) | REFUTED (doubt settled) | READ disk ddi0100i.txt:8611-8614 (LDREX, A4-53), :14664-14667 (STREX, A4-203), Table A2-10 :3178/:3200/:3221, glossary :45064 "UNPREDICTABLE instructions must not halt or hang the processor" | none (the brief cites these lines) |
| F6 | grok | The passage's `arm_exception()` mechanics (OB:4221-4227) were not re-opened | REFUTED (doubt settled) | READ cpu_arm.c:712-714, :717 (pc+8), :783; cpu_arm.h:218-219 fsr/far; armreg.h:385 `FAULT_ALIGN_0 0x01`; callers cpu_arm_instr.c:1018/:1031/:1044; ddi0100i.txt:29062 | none |
| F7 | grok | The bugs-file pins are db8b1a33 lines and differ at HEAD | CONFIRMED (BP) | READ db8b1a33 2617-2619 / 3625-3626 / 4181-4202 = HEAD 2625-2627 / 3645-3646 / 4208-4229 (same text) | The pins are correct for their commit; the brief uses the HEAD lines |
| F8 | grok | IDLESS_DISPOSITIONS.md:159's C cites are db8b1a33 lines; the MIPS cites at :120 still match HEAD | CONFIRMED (BP) | READ db8b1a33 cpu_arm_instr.c:2018-2022 / :2063-2067 = HEAD :2053-2057 / :2098-2102; cpu_mips_instr.c:5692-5695 and cpu_dyntrans.c:2014 unchanged | Brief uses HEAD lines |
| F9 | grok | qhrdhwrpolicy's "unimplemented RDHWR selector stops the CPU" is false for selector 29 | CONFIRMED (RC) | READ cpu_mips_instr.c:5689-5690 `case 29: ic->f = instr(reserved);` (RI via X(reserved)); :5679/:5684 implement cases 0 and 2; :5692-5695 default `fatal` + `goto bad` (author checked); mips32_volII.txt:1237 "If access is not allowed or the register is not implemented, a Reserved Instruction Exception is signaled" (author checked) | Retitle: an RDHWR selector other than 0, 2 or 29 (including Release-2 registers 1 and 3) stops the CPU where the architecture requires a value or RI |
| F10 | grok | On the default arm, `fatal` prints only outside readahead, `goto bad` is unconditional, and there is no `exit(` | CONFIRMED (BP) | READ cpu_dyntrans.c:1988, :1990-1991 (readahead returns early), :2002, :2014 `cpu->running = 0;`; debugmsg.c:384-391 | Brief: the stop happens on real execution; the CPU drops to the debugger; the host does not exit |
| F11 | grok | "(MIPS32r2-only)" is wrong: the gate also admits MIPS64r2 5KE, the testmips/baremips default | CONFIRMED (RC) | READ cpu_mips_instr.c:5584-5585 (`isa_level < 32 \|\| isa_revision < 2` -> RI); mips_cpu_types.h:102 4KEc (32,2), :104 5KE (64,2), :105 24KEc (32,2); machine_test.c:406/:412 `strdup("5KE")` (author checked); CHANGELOG.md:21344 "only exists on emulated MIPS32r2" | Annotate OB:2626 and CHANGELOG.md:21344: MIPS32r2 and MIPS64r2 (4KEc, 24KEc, 5KE) |
| F12 | grok | "no audit-path exposure" is wrong | REFUTED | READ OB:2620-2621 defines the audit path as pmax/arc; machine_pmax.c:957-963 (level 1) and machine_arc.c:262/:266 (level 3) fail the :5584-5585 gate, which grok itself concedes | That clause stands; only "(MIPS32r2-only)" needs the F11 fix |
| F13 | grok | Neither ledger row carries a C source line | CONFIRMED (RC) | READ ledger.json:61259 "(lines 2617-2619 at db8b1a33)", :61281 "(lines 3625-3626; 4181-4202 at db8b1a33)"; the C sites are only in IDLESS_DISPOSITIONS.md:120/:159 | Add cpu_arm_instr.c:2053-2057 / :2098-2102, cpu_mips_instr.c:5692-5695, cpu_dyntrans.c:2014 to the rows |
| F14 | grok | The two rows share no site; LDREX and STREX are already one id | DISPOSED | READ ledger.json:61251 (MIPS) and :61273 (both ARM sites) are separate rows | none |
| F15 | grok | Cross-references: armmmuvehicle lists qharmexalign; qharmvsixunal is the word-load rotate remainder; qhppciphack / qhm88kstops split db8b1a33:2616 | DISPOSED | READ ledger.json:62253; OB:24527; qharmvsixunal title; IDLESS_DISPOSITIONS.md:118-119 | none (the rows exist) |
| F16 | grok | A CP15 endianness switch is `fatal` + `exit(1)` (cpu_arm_coproc.c:175-177), a separate path | DISPOSED | READ cpu_arm_coproc.c:175-177; row `armendianexit` (HIGH, open) | none |
| F17 | grok | (fact table) Other CPU stops on the same decode paths: LDREX with PC, STREX with a bad register, R5900 SPECIAL3 | CONFIRMED (BP) | READ cpu_arm_instr.c:4198-4201 `fatal("ldrex with pc register: TODO\n"); goto bad;`, :4213-4217 "strex with bad register"; cpu_mips_instr.c:5578-5581 "TODO: R5900 128-bit stores" + `goto bad`. Ledger grep finds no row (mipscop0tail covers COP0 arms only) | Brief lists them as out of scope; grok did not call them defects; the panel may FILE |
| F18 | grok | No regress probe or gate names ldrex, strex, rdhwr or HWREna | CONFIRMED (BP) | READ case-insensitive git grep over regress -> no hit; cpu_arm_instr.c:4104-4192 has no CPU-version test before the LDREX match at :4193 | Brief: a rung-3 cold-debugger probe on unmodified `-E testarm` reaches X(ldrex)'s guard with the MMU off (no armmmuvehicle needed); RDHWR rd=1 reaches the stop on testmips' default 5KE |
| F19 | grok | grok said the RDHWR default arm "matches the file's ordinary unimplemented goto bad" without counting | CONFIRMED (BP) | READ in X(to_be_translated) (cpu_mips_instr.c:4270-5732), `grep -c`: 40 lines with `goto bad`, 17 with `instr(reserved)` | Brief: the default arm follows the file's majority disposition; an outlier only against case 29 and the ISA gate |

---

## records_three  (rows stateaudit0923, untrackeddetectors, wirereassign; grok 24 FLAGs; agy: none; Argon: not yet)

Files read (helper), @e483d931 unless another commit is named:
- ledger.json (+ @4264ee20); OB; CHANGELOG.md.
- `tools/pipeline/check_probe_wiring.py` (+ @db8b1a33, @1202d342, @04500deb), `tools/precommit_check.sh`,
  `tools/nightly_check.sh`, `tools/pipeline/check_cited_artifacts.py`, `tools/pipeline/gen_dashboard.py` (blame),
  `tools/CLAUDE.md`.
- `regress/run.sh` and all 16 GATES scripts (gate_arm.sh also @4264ee20^; gate_sh_rounding.sh also @db8b1a33, @1202d342);
  `regress/{crime_width_probe,lca_isalane_probe (also @8bd97e4d/@a11eaac4/@1329d894),gdrom_default_probe,sh4_bsc_width_probe}.py`;
  `src/core/debugmsg.c`, `src/devices/dev_sh4.c`, `src/include/thirdparty/sh4_bscreg.h`.
- `regress/artifacts/stateaudit_20260923/{FINAL.md, untracked_cited_dirs.txt, cited_paths_missing.txt, APPLIED_CLAIMS.txt,
  seats/fable_adjudication.md, derivers/cited_paths.py}`; HD; `astrafiling_20261002/agy/agy_highfacts.txt`;
  `regress/artifacts/fbd5/r3_m9_20260923/*`; `regress/artifacts/lcalenzerodrop/killtable_20260918/{logs/probe_base.raw,
  lca_isalane_probe.frozen.py}`.
- On disk: `stateaudit_20260923/peer_carriers/MANIFEST.txt`, stat of the two D6 copies and of `regress/lca_isaphys_probe.py`,
  listings of seven `_scratchpad/panel_20260827_*` dirs, `_scratchpad/nightly/verdict_*` (four), and the live root CLAUDE.md
  (diff only).

Author spot-checks: `git cat-file -e` and first-add commits for crime_width_probe.py (7440e129), lca_isalane_probe.py
(8bd97e4d) and lca_isaphys_probe.py (untracked, on disk); check_probe_wiring.py:3095-3101, :3870-3875, :3936-3946;
precommit_check.sh:35-38, :544-551; row `wiringcliff`; and, as the one read of the working tree for the time-critical residual,
the uncommitted check_probe_wiring.py:3112-3115.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| F1 | grok | The brief's pickaxe recipe `git log -S'"id": "<id>"'` "returned no hash" | REFUTED | READ: run as written, it returns 4264ee20 (stateaudit0923), 686d179c (untrackeddetectors), 1202d342 (wirereassign) | none |
| F2 | grok | The brief's "?" severity is HIGH for all three rows | CONFIRMED (BP) | READ ledger.json:48833, :53033, :59946 `"sev": "HIGH"`, all `"state": "open"`. Same builder defect as cpu_policy_two/F1 | Brief carries HIGH/open (cross-job builder fix) |
| F3 | grok | The stateaudit0923 title and OB:22109/:22115 "gate 6 is red at HEAD (pty 70/46...)" are stale | DISPOSED | READ row `hygienecensus` closed on 3e33201d (2026-09-24); gate_hygiene.sh:388 `EXPECT_PTY_PROBES=74`, :599, :669. Disk: `_scratchpad/nightly/verdict_20261011_180002.txt` "HEAD=e483d931 ... PASS 6. gate_hygiene" (TREE_DIRTY=YES); gate 6 also passed 09-27 and 10-04 | Mark the title clause and hold (1) discharged by hygienecensus/3e33201d |
| F4 | grok | "thirteen exemptions lapse 2026-09-28" was true at 4264ee20; none of those dates remain at HEAD | DISPOSED | READ `exemptcliff` closed 04500deb ("#550 DISPERSES the block -- ten dates, 2026-10-08 to 2026-12-03"); `fbdrainwire` closed f4f601c4; `wdcidselfcheck` closed f5e155ac; `scexempt` open (gate_offline.sh:2343 `ieee_store:2026-12-10`) | Mark hold (2) discharged, citing those rows |
| F5 | grok | The ip30 re-dated exemption is 2026-10-15 and "does not expire it on this audit's date"; it has lapsed TODAY (2026-10-16) | CONFIRMED (FILE -> fold into `wiringcliff`; act today) | READ check_probe_wiring.py:3097-3098 `"artifacts/ip30abortkill/ip30_abort_probe.py": ("2026-10-15",`; :3873 `today = datetime.date.today().isoformat()`; :3941-3943 `elif d < today: fails.append("EXPIRED EXEMPTION ...`; precommit_check.sh:546-550: a wiring fail calls `bad` (:37 counts a failure); none of the 16 gates runs the probe; "2026-10-15" is in no ledger/OB text (author checked). Working tree (uncommitted; read only for this residual): check_probe_wiring.py:3112-3113 still `("2026-10-15",` | From 2026-10-16 precommit section R refuses every commit until the ip30 entry is re-dated or wired; fold into `wiringcliff` (med, in work). Next due: ppc_rldicl and alpha_tbi 10-22, lca_badval 10-23, lca_widewrite 10-26, lca_isalane 10-27 |
| F6 | grok | The title's "nothing on disk lost" drops FINAL.md's own qualifier | CONFIRMED (RC) | READ FINAL.md:26-28 "Not yet run, and it could still falsify the claim: the peer made 97 Bash calls ... no pre-09-21 baseline"; ledger.json:53032 and OB:22109 state it without the qualifier; no later record closes it | Reword: "no deletion found by name-status (0 D); not closed" |
| F7 | grok | D3's in-place correction is itself stale ("HEAD's gate_arm.sh still counts E ids over ALL lines"), because the same commit added the green-line check | CONFIRMED (RC) | READ CHANGELOG.md:2168-2169 (4264ee20); gate_arm.sh:1156-1160 blamed to 4264ee20 (`grep -E '^E[0-6] .*ok$'`); 4264ee20^:gate_arm.sh:1114 was the all-lines form | Wording: "the pre-#545 HEAD's" (4264ee20 is #545) |
| F8 | grok | D1's cites gdrom_default_probe.py:160-166/:1186-1187/:1608-1610 hold no dma-alias rows at HEAD (the rows are :702/:707) | DISPOSED | READ ledger `gdromdmadefault` entry [13] "...(working tree only; HEAD has neither) ... OWED with the uncommitted repairB/U5 work"; HEAD probe (1418 lines) has `row("dma alias"` :702, `"dma alias x1"` :707 | none |
| F9 | grok | D8's three cites no longer hold those texts | CONFIRMED (RC) | READ: none of D8's stale numbers is in HEAD; check_probe_wiring.py:946-947 crime_width "226 rows ... pins 226"; gate_arm.sh:1881-1882 lists the eleven-plus kill tables; the remaining 141s describe frozen 141-row instruments | Mark D8 discharged by #529's commit 7440e129 |
| F10 | grok | OB:22122-22123 says gen_dashboard.py:143-146 and :173 were both written by 09ded75, but :143 is 581b8f365 | REFUTED (immaterial) | READ blame: :143 `if not ents:` is 581b8f365; :144-146 and :173 are 09ded75c4. The record says the fallback sits "inside `if not ents:`", an existing guard | none. D2 is carried by `dashmalformedheld` (open, LOW) |
| F11 | grok | D6's two "made" durable copies exist on disk but in no commit | CONFIRMED (RC) | READ `git cat-file -e` fails at e483d931 for regress/artifacts/n6/p1_20260919/fable5_p1_20260919.md and regress/artifacts/ip30abortkill/PROBEATTACK_grok_20260917.txt (on disk, 22,624 B and 13,519 B); ledger.json:6397 and :49347 call them "Durable copy MADE ... (cmp-verified)"; CHANGELOG.md:2091 still cites `_scratchpad/n6/...` | Add "on disk, untracked at e483d931" at OB:22118; the exposure joins D7's owner decision |
| F12 | grok | D7's "18 cited dirs hold no tracked file": armmsrmodekill is now tracked, and the other 17 were not re-counted | CONFIRMED (RC) | READ untracked_cited_dirs.txt (18 dirs); `git ls-tree -r` at e483d931: armmsrmodekill 846 files, ppcwitnessmaskoracle 5, the other 16 have 0 | D7 now stands at 16 of 18 |
| F13 | grok | Hold item (3) still asks for the #545 commit, which is the filing commit 4264ee20 itself | DISPOSED | READ ledger.json:53038 "(3) the #545 commit and its Fable hold"; 4264ee20 "#545 fbdeclinefive"; fbdeclinefive closed with fable5 review [19] and regress [75] entries | Mark hold (3) discharged |
| F14 | grok | D5's M9 33/37 (fbd5/r3_m9_20260923/) was not opened | DISPOSED | READ R3.log:2 "PREDICTION: ... M9 33/37 ...", :8 "SITES M9 ROWS=33 of 37 ... red: N1,N2,N0,NO", :11 "R3_DONE"; sites_M9.log 33 ok / 4 FAIL | none (the premise holds) |
| F15 | grok | D9's 21 `ollama_` mismatches and the alphatbinegsel path were not re-checked | CONFIRMED (RC) | READ: 21 ledger lines (ledger.json:13310 .. :27763) cite `_scratchpad/panel_20260827_*/{glm,deepseek,minimax}.txt`; all seven dirs hold only `ollama_{deepseek,glm,minimax}.txt`. ledger.json:41125's ev `regress/artifacts/alphatbinegsel/opus_pass2_20260910.md` does not exist; the tracked file is `regress/artifacts/ppcrldiclzero/pass2_20260910/opus_pass2_20260910.md`. No row other than stateaudit0923 carries D9 | Correct the 22 citations in place (L4) |
| F16 | grok | Witness counts 883 + 1650, 81 and 1170 were not re-counted | DISPOSED | READ APPLIED_CLAIMS.txt CLAIM 001..081 (81); cited_paths_missing.txt:1 "cited paths: 883"; peer_carriers/ holds 1171 files on disk = 1170 + MANIFEST.txt; seats/fable_adjudication.md:32 "1650 cited / 58 unresolved" (a seat's run) | none (residual: re-deriving 1650 needs one run of derivers/cited_paths.py) |
| F17 | grok | Hold items (4)/(5) were not re-checked; FINAL.md:73's tools/CLAUDE.md "+133/-12" was not re-measured | CONFIRMED (BP) | READ (4): #529 landed as 7440e129; the peer's #540-#544 rows have no commits. (5): e483d931:tools/CLAUDE.md (last commit 38040aca, 2026-09-10) vs the live root CLAUDE.md diffs +263/-21 | Brief: (4) partly discharged; (5) open and widened to +263/-21 |
| F18 | grok | The untrackeddetectors title, OB:20509-20519 ("?? untracked -- `git log --all` EMPTY") and "STILL OWED: the COMMIT itself" are stale | CONFIRMED (RC) | READ regress/lca_isalane_probe.py added in 8bd97e4d (2026-09-18, #530); regress/crime_width_probe.py in 7440e129 (2026-10-02, #529), together with gate_arm.sh (author checked both). Their own rows are closed: `lcaisalane` (ledger.json:38507), `crimewidthkill` (:43913) | Close untrackeddetectors with commits 8bd97e4d and 7440e129 |
| F19 | grok | The recorded sizes and line counts (119,216; 99,545; "99 KB / 1370") do not match HEAD | CONFIRMED (RC) | READ HEAD blobs: 140,482 B / 1827 lines and 101,859 B / 1396 lines. 1370 is the killtable_20260918 frozen copy. "352 rows" holds: HEAD is code-identical to the frozen instrument, whose tracked base log ends `LCAISALANE_RESULT=352/352` ... `LCAISALANE_DONE` | Fold into F18's closure note (keep the dated values; add the HEAD sizes) |
| F20 | grok | The cited gate_arm.sh:1658 and "the COMMITTED gate_arm.sh has ZERO references" are stale | CONFIRMED (RC) | READ gate_arm.sh:1654-1658 is a #500 comment; :1887 `python3 -u crime_width_probe.py "$PMAX" gate`; pins at :1936/:1941/:1942 (226) | Fold into F18's closure |
| F21 | grok | The state_note still calls the missing EXPECT_ROWS row "floor clause (c)", which the bugs file corrected the same day as a conflation | CONFIRMED (RC) | READ ledger.json:48838 "Neither probe has an EXPECT_ROWS identity row (floor clause (c))"; OB:20546-20548 "USED TO READ '(floor clause (c))' ... A CONFLATION -- CORRECTED 2026-09-17" | Correct the state_note to match OB:20546-20554 |
| F22 | grok | "lca_isalane_probe.py is in NO gate" is contradicted by gate_hygiene.sh:420 | REFUTED | READ gate_hygiene.sh:420 names it only in `GRANDFATHERED_PROMPTLESS` (:414-422), a census list; no invocation in any of the 16 gates; check_probe_wiring.py:3075 `("2026-10-27",` | none (BP: its exemption is due 2026-10-27) |
| F23 | grok | wirereassign's cited lines are pinned to older revisions | CONFIRMED (BP) | READ state_note (ledger.json:59952) and HD:721/:1159 cite `check_probe_wiring.py:2833-2839` with no revision (only HD:734 says "db8b1a33"). The varmap is at 2833/2878 in db8b1a33, 3165/3210 in 1202d342, and 3243-3249/:3288 at HEAD; the BSCPROBE block is gate_sh_rounding.sh:1335-1340 at HEAD | Brief carries HEAD lines; optionally qualify the state_note "@db8b1a33" |
| F24 | grok | HD:734's "a non-.py reassignment is ignored and the file guard skips" does not fit a cited site whose only assignment is .py | REFUTED | READ HD:734's parenthetical describes the failure path and does not claim a live reassignment; the state_note already records agy's "Q3: NONE FOUND" (agy_highfacts.txt:19) | none |
| F25 | grok | grok re-checked only the cited gate for the reassignment shape | CONFIRMED (BP) | READ all 16 gates with the checker's own ASSIGN_RE (:3194): 10 variables take a .py value (gate_hygiene 4, gate_sh_rounding 6); none is reassigned and none used before assignment | wirereassign is latent at HEAD in both halves |
| F26 | grok | HIGH dispute: nothing on the BSC path the detector protects ends the process at HEAD | CONFIRMED (BP) | READ debugmsg.c:384-391 (fatal returns); dev_sh4.c:1674-1685 latched fatal, `return !partial`; callers `break` at :2306-2307 and :2317-2318; dev_sh4.c's live exits are only :2833 (`#ifdef SH4_DEBUG`) and :3008/:3014/:3020 (setup). 13 HEAD rows carry "HIGH IS DISPUTED" with no ruling | Brief carries the code fact; severity stays the flagship's rule question |
| F27 | grok | The checker's selftest never builds a non-.py reassignment | CONFIRMED (BP) | READ selftest :3545-3859, mutants M0-M15: none edits an assignment; only M13 (:3816-3820) touches the variable path | A wirereassign round owes one selftest mutant per half |
| F28 | grok | "sh4_bsc16_report is the outlier among 16-bit BSC registers ... WCR1 at :2326 stores with no width report" | REFUTED | READ sh4_bscreg.h:56 `SH4_WCR1 0xff800008 /* 32bit */`; dev_sh4.c:2328; :1602-1604 names the 16-bit siblings | none |
| F29 | grok | No pair of the three rows is one defect | CONFIRMED (BP) | READ untrackeddetectors = domain() :3323 + GHOST arm :3901-3909 (686d179c); wirereassign = exec_sites' varmap :3243-3249/:3288; lca_isaphys_probe.py is still untracked on disk (35,039 B; the peer's in-work lcaisaphys) and not in HEAD's MANIFEST | Three separate rows |
| F30 | grok | VERDICT: "the present-tense titles are stale against e483d931" | REFUTED (for wirereassign) | READ check_probe_wiring.py:3243-3249 still builds `varmap` over the whole file from `.py` assignments only, and :3288 `t = varmap.get(v.group(1), "")`; only its line cites are stale (F23). The verdict holds for stateaudit0923 (F3, F4, F6) and untrackeddetectors (F18) | Do not close wirereassign on staleness |

---

## CONFIRMED and CANNOT SETTLE items for the adjudicators

**Act today (time-critical)**
- records_three/F5: HEAD's checker treats the ip30 wiring exemption as expired from 2026-10-16, so precommit section R
  refuses every commit (check_probe_wiring.py:3097-3098, :3941-3943; precommit_check.sh:546-550). The uncommitted working-tree
  copy carries the same date (:3112-3113). Re-date or wire it under `wiringcliff`. The next to fall due is 2026-10-22.

**FILE**
- of_two/F9: NEW HIGH row. `of_emul`'s `of_data == NULL` -> `exit(1)` (of.c:1098-1100) is one guest instruction away on every
  ARM machine (cpu_arm_instr.c:5034-5036) and on every PPC machine except macppc with prom emulation
  (cpu_ppc_instr.c:4400-4402; of_data is set only at of.c:1078 via machine_macppc.c:99). No existing row.
- pvr_gdrom_four/F15: fold into `gdromcondhow`. R3/R4 (gdrom_cond_probe.py:436, :516) also omit `how`.
- records_three/F5: fold into `wiringcliff` (above).

**Cross-job classes (one decision each; the members are listed per job below)**
- Brief builder: `_scratchpad/agypack_20261013/mk_briefs4.py:17` reads `severity` (the key is `sev`), and its `[:240]` cut
  truncates titles. Every brief in this set says "(?, open)" for rows that are HIGH/open (cpu_policy_two/F1,
  records_three/F2). It was already harvested, with no disposition, at HARVEST_AUTO.md:275.
- Retro-row GOVERNING TEXT windows start 60 characters before the row's own id and are cut at 400
  (astrafiling_20261002/mk_filing.py.txt:187, :83). The "cut at 400 characters" prefix does not declare the lead-in, so notes
  open inside a neighbour's bullet (loaders_four/F1, net_three/F17). The helpers' two heuristic counts (122 of 190; ~57 of 221)
  use different criteria and are not a census: derive before citing.
- #556 (1329d894, 2026-10-02 18:09) inserted notes into probes and gates after the #554 filing (1202d342, 14:47), so the
  filing's line cites moved: diagdiv_three/F9, sgi_harness_five/F7, F11, F12, pvr_gdrom_four/F14. Cite anchors or HEAD lines.
- Rows that carry no source path:line: of_two/F1, osiop_three/F2, pvr_gdrom_four/F4, net_three/F4, loaders_four/F8,
  fb_vga_x11_five/F13, cpu_policy_two/F13.

**RECORD CORRECTIONS**
- diagdiv_three/F3: retitle diagdivunaryop to "UNPARENTHESISED unary/dereference divisor" (ledger.json:59703, OB:23344).
- diagdiv_three/F4: retitle diagdivchained to "leading numeric-literal or bare-`sizeof` divisor" (ledger.json:59725, OB:23347).
- diagdiv_three/F6: "(grok/grok_filehigh.txt: nothing live ends the process today)" is the overlay's paraphrase, not grok's
  text. Mark it as such or quote grok_filehigh.txt:47-49 (three state_notes; OB:23345/:23348/:23351).
- diagdiv_three/F7: "verbatim" Q1/Q2/Q3 is a condensation of agy_highfacts.txt:11-13.
- diagdiv_three/F8: the "agy's fact table" clause is GPT-6 Astra's wording (afile_09:8/:10/:12; FILING_OVERLAY.tsv:100-102
  col 4); agy disowned it (agy_highfacts2.txt:6-8).
- osiop_three/F1: osiopregexit and osiopdnadexit share dev_osiop.c:1143-1152; each row should name the other, or fold.
- osiop_three/F2: osiopselectzero and osiopregexit have identical titles that name no site. Use :654-656 and :1143-1152
  (grok_filehigh2.txt:9-10).
- osiop_three/F3: exitunowned76's note (ledger.json:46578) still says "Not filed individually yet".
- sgi_harness_five/F1: sgirespanchk (HIGH) duplicates sgilinearoob (med); fold or cross-link. The grade is the `shoddprfield`
  question.
- sgi_harness_five/F10: sgi_de_primop_probe.py:929-932's comment is false after the first latched decline; add it as a rider on
  sgideprimbitslive.
- sgi_harness_five/F14: mtetlbflood's "sgideprimop DOES exit(1)" (OB:14998-14999, ledger.json:34830) should read "a latched
  decline since #500".
- sgi_harness_five/F19: sgirespanchk `opened` "" should be 2026-09-07 (moot if folded).
- sgi_harness_five/F20: "write loops" should be "write pairs" (moot if folded).
- sgi_harness_five/F21: the "non-CPU callers not enumerated / audit running" text (OB:16379-16382, ledger.json:41203) is answered.
  The debugger AND guest ARC GetFileInformation/Seek reach TLB_A/TLB_C/LINEAR_A (codex_span_20260907.txt:5184, :5189;
  fb3b:213-225; arcbios.c:1140-1147). The fb3b:228-233 riders were never applied: dev_sgi_re.c:653-654/:766-767 and
  ledger.json:31232 still say "NOT guest-reachable".
- sgi_harness_five/F25: OB:14805 and ledger.json:31229 still say "len == 8 forces 8-byte alignment" (false per
  dev_sgi_re.c:718-720).
- sgi_harness_five/F26: OB:14831-14833 and ledger.json:31230 still say "kills the host before the store" (stale since #497).
- sgire_pcc2_vme/F1: the sgirekills witness field (ledger.json:29911) names `ld kill` rows that are GONE (gate_arm.sh:1442).
- sgire_pcc2_vme/F2: sgi_re_width_probe.py:40-52 still says an 8-byte `ld` ends the host; fold into `sgidefatalstale`.
- sgire_pcc2_vme/F6: the pcc2widthkills / pcc2c040kill titles say "kill" while HEAD declines (fixes b78bb0f / 9fa07fe);
  rewrite them.
- sgire_pcc2_vme/F9: "a plain aligned 4-byte read of GENCTL" was never deliverable (GENCTL = 0x02; m88k alignment fault).
  Make it "an aligned halfword".
- sgire_pcc2_vme/F11: add FIXED banners to OB:14188-14205 and OB:15386-15407.
- sgire_pcc2_vme/F14: pcc2_c040_probe.py:7/:10 is stale; fold into `pcc2contractstale` (OB:23660).
- sgire_pcc2_vme/F15: pcc2_width_probe.py:370-372, :824-826, :850-852, :1383-1384 still say C040 "ends the host"; extend
  hpcc2widthprobe:F4.
- sgire_pcc2_vme/F18: vmedefaultkill's "unconditionally ... actively boots" (OB:18823-18824; ledger.json:45732) is wrong; it is
  MVME187-only, and the machine is constructed, not booted.
- sgire_pcc2_vme/F19: the vmedefaultkill note's (A) "returns 0x67000000" is wrong. A byte or halfword read delivers the low
  lanes, which are 0 from reset (memory.c:104-108).
- sgire_pcc2_vme/F20: OB:18827-18828's "the bus error real VME hardware would" is unproved (as the note itself says).
- sgire_pcc2_vme/F24: machine_mvme88k.c:35 should be :37 (Ethernet).
- of_two/F1: ofopenexit should carry of.c:446-448.
- of_two/F5: retitle ofpeerexit to "a nonzero handle that no OF device carries" (of.c:385-394).
- pvr_gdrom_four/F4: pvrdirtyregion should carry dev_pvr.c:2307-2338/:2325-2326/:572-589/:2629 (codex_devpvr.txt:6).
- pvr_gdrom_four/F5: complete pvrdirtyregion's truncated title (ledger; OB:22925) from D:723.
- pvr_gdrom_four/F11: :1084 is a pre-loop config exit, not a loop exit (title; OB:2731).
- pvr_gdrom_four/F14: gdromcondhow's title cites are 7440e129 lines; add "at 7440e129" or re-key them to anchors.
- pvr_gdrom_four/F16: gdromdmareentr recurses only for a masked destination of exactly 0x005f7418 (title; OB:22874).
- net_three/F4: ne2krxbudget and taprxquota should carry dev_ne2000.c:333-341/:450-473, net_tap.c:104-135, net.c:293-295.
- net_three/F13: tcpdebugopts should cite dev_dec21143.c:772-809, not :788-809.
- net_three/F17: dectxzero's state_note window opens inside vgadirtyarm's bullet; re-cut it to D:382-383 (class above).
- loaders_four/F1: the GOVERNING TEXT lead-in is undeclared (class above).
- loaders_four/F2: ecoffoffsetspan's title needs the admission condition (file_ecoff.c:322-326; misc.h:217).
- loaders_four/F4: ecoffoffsetspan's title drops "or read the WRONG bytes" (D:451).
- loaders_four/F8: emulgzipfail should carry emul.c:609-616.
- fb_vga_x11_five/F2: fbsdrampair's "HEAD :712, :737" should be :734-735 / :759-760, or name the construct.
- fb_vga_x11_five/F5: the "seven exits remain" census (OB:2690-2692, :22031; D:808) is stale since #545; two remain.
- fb_vga_x11_five/F13: x11alloc32 should carry x11.c:441-446 and :632, and dev_fb.c:147-150 / :229.
- fb_vga_x11_five/F14: x11alloc32 is conditional on scaledown 1 and X depth 24/32 with side >= 11586.
- cpu_policy_two/F2: qharmexalign's title: passage 1 records only ldrex.
- cpu_policy_two/F3: OB:4213 "permanently (A,U) = (0,0)" is false; A is set at reset (cpu_arm.c:128-129).
- cpu_policy_two/F4: OB:4218-4220's "latitude" holds only at A=U=0. At reset the alignment abort is mandated
  (ddi0100i.txt:8611).
- cpu_policy_two/F9: retitle qhrdhwrpolicy: selector 29 raises RI; only the default arm stops the CPU.
- cpu_policy_two/F11: "MIPS32r2-only" (OB:2626, CHANGELOG.md:21344) should read MIPS32r2/MIPS64r2; 5KE, the testmips default,
  is exposed.
- cpu_policy_two/F13: both rows should carry their C sites.
- records_three/F6: "nothing on disk lost" drops FINAL.md:26-28's own "not yet run" qualifier.
- records_three/F7: CHANGELOG.md:2168-2169 "HEAD's ... ALL lines" should read "the pre-#545 HEAD's".
- records_three/F9: D8 is discharged by 7440e129.
- records_three/F11: D6's two "durable copies" are untracked at e483d931 (ledger.json:6397, :49347).
- records_three/F12: D7 now stands at 16 of 18.
- records_three/F15: 21 ledger cites name `<seat>.txt` for `ollama_<seat>.txt`, and alphatbinegsel's ev (ledger.json:41125) is
  mis-pathed.
- records_three/F18: close untrackeddetectors. Both detectors were committed (8bd97e4d, 7440e129) and both owner rows are
  closed.
- records_three/F19: fold the HEAD sizes into F18's closure note.
- records_three/F20: fold the moved gate_arm.sh cite (:1887; pins :1936/:1941/:1942) into F18's closure note.
- records_three/F21: untrackeddetectors' "(floor clause (c))" is the conflation OB:20546-20554 corrected.

**BRIEF PREMISES**
- diagdiv_three:
  - F1: three mechanisms (:89 / :104+:107 / :99+:112).
  - F2: the unary repair has two sites (:89 and :107).
  - F5: truncarg needs an already-counted call.
  - F9: cite gate_hygiene.sh:796-797 / :840-841.
- osiop_three:
  - F4: a third SELECT input (immediate DBC[23:16] = 0, the cheapest witness).
  - F5: "byte 2" means bits 23:16 (descriptor+1, big-endian).
  - F7: ADDER is ro (osiopreg.h:116) yet is stored.
- sgi_harness_five:
  - F3: sgilwreadzero's OOB consequence is sgilinearoob's read site.
  - F7: gate_ab.sh:325/:338-339.
  - F11: n25 line row :1387-1392.
  - F12: banner :1454-1459.
  - F13: OB:15037.
  - F15: protected arms :966-968 and :1139-1147.
  - F18: OB:16344.
- sgire_pcc2_vme:
  - F4: 5 live MTE exits + 1 dead, no witness, rung-3 owed.
  - F12: dated pcc2c040kill lines; use current anchors.
  - F25: nothing reaches dev_vme.c; the probe exists only as an artifact.
- of_two:
  - F2: an unreadable first byte does not exit.
  - F3: the 1-in/1-out gate (of.c:1170-1171).
  - F4: the skeletal-OF sentence is now OB:2753-2756.
  - F7: D:956's ":1185" clause misreads #219.
- pvr_gdrom_four:
  - F1: grok's gate/probe lines are working-tree lines.
  - F3: four distinct defects.
  - F6: SIGFPE is host-specific and unmeasured.
  - F7: the tick is a third caller, with a page-rounded range.
  - F8: the exact zero-width condition.
  - F9: inversion only from an empty rect.
  - F12: one STARTRENDER store reaches :1084.
  - F19: stack exhaustion is unmeasured.
  - F23: no probe reaches the three device paths.
- net_three:
  - F3: four distinct defects.
  - F6: per-mode refill paths (TAP returns at net.c:293-295).
  - F7: the tick also runs on register access.
  - F10: dead counter in net_tcp_rx_avail, bounded loop.
  - F11: HEAD :2741.
  - F14: the TX buffer census.
  - F15: TCP-dump reach conditions.
  - F18: `realloc(NULL, 0)` fall-through.
  - F19: no probe; arc/pmax rigs as vehicles.
- loaders_four:
  - F3: the unguarded symhdr seek/exit at file_ecoff.c:278-284 belongs to ecoffoffsetspan's scope.
  - F6: #59's own exit-on-short-read.
  - F9: three `-1` causes, two of them host failures.
  - F15: a third reader of the 4-byte `ib` (cpu_dyntrans.c:1826-1829).
- fb_vga_x11_five:
  - F3: the dc21285.txt Table 7-7 row offset.
  - F12: the "hours" walk needs graphics mode.
  - F16: fbctrl SET_RESOLUTION is a guest route into x11alloc32.
  - F20: other readers of the truncated offset, and the end-of-chain collision.
- cpu_policy_two:
  - F1: the builder bug (class).
  - F7, F8: HEAD lines.
  - F10: CPU stop, not host exit.
  - F17: unrowed LDREX-pc / STREX-bad-reg / R5900 stops; the panel may FILE.
  - F18: testarm/testmips rung-3 vehicles.
  - F19: `goto bad` is the file's majority disposition.
- records_three:
  - F2: HIGH/open.
  - F17: hold (4) partly discharged; hold (5) widened to +263/-21.
  - F23: HEAD lines (varmap :3243-3249/:3288; BSC block :1335-1340).
  - F25: no live reassignment instance in the 16 gates.
  - F26: nothing on the BSC path ends the process; HIGH is the rule question.
  - F27: the selftest lacks reassignment mutants.
  - F29: three separate defects.

**CANNOT SETTLE**
- diagdiv_three/F10: whether any live guest-zero shape exists beyond the single-line greps. One run: the widened sweep from a
  clean e483d931 checkout.
- of_two/F10: whether a real boot reaches OF open/peer. One `-E macppc -e g4` NetBSD boot (rung 4); a cold-debugger trap-word
  probe gives rung 3.
- net_three/F16: glibc `realloc(p, 0)`. One run on the build host: `printf("%p\n", realloc(malloc(1), 0))`.
- loaders_four/F7: `fseek` to a negative `off_t`. One run: print the return value, errno and `ftell`.
- fb_vga_x11_five/F21: `malloc(0)` on the target ILP32 libc.

**REFUTED items that still carry an action**
- net_three/F8: grok's "no sibling NIC has the shape" is refuted. dev_dec21143.c:356-366 is an unbudgeted RX drop loop under
  TAP: every packet is dropped until a setup frame arrives (:295-306). No row exists. FILE, or fold into `ne2krxbudget`.
- fb_vga_x11_five/F9: grok's refutation of the ~-1.7e9 origin is itself refuted. y2 (:743) is computed in size_t and lowers
  update_y1 at :764 (max_x 80: -1717986919). This is a premise for vgadirtyarm's brief; measure on the build host.
- sgi_harness_five/F5: sgilwreadzero's HIGH can rest only on the accept/OOB arm (M1), not on host death (BRIEF PREMISE).

## Counts

| job | findings | DISPOSED | CONFIRMED (FILE / RC / BP) | REFUTED | CANNOT SETTLE |
|---|---|---|---|---|---|
| diagdiv_three | 11 | 1 | 9 (0 / 5 / 4) | 0 | 1 |
| osiop_three | 11 | 4 | 6 (0 / 3 / 3) | 1 | 0 |
| sgi_harness_five | 29 | 4 | 15 (0 / 8 / 7) | 10 | 0 |
| sgire_pcc2_vme | 27 | 5 | 14 (0 / 11 / 3) | 8 | 0 |
| of_two | 11 | 2 | 7 (1 / 2 / 4) | 1 | 1 |
| pvr_gdrom_four | 23 | 4 | 15 (1 / 5 / 9) | 4 | 0 |
| net_three | 19 | 1 | 12 (0 / 3 / 9) | 5 | 1 |
| loaders_four | 18 | 6 | 8 (0 / 4 / 4) | 3 | 1 |
| fb_vga_x11_five | 21 | 7 | 8 (0 / 4 / 4) | 5 | 1 |
| cpu_policy_two | 19 | 3 | 13 (0 / 6 / 7) | 3 | 0 |
| records_three | 30 | 6 | 18 (1 / 10 / 7) | 6 | 0 |
| **total** | **219** | **43** | **125 (3 / 61 / 61)** | **46** | **5** |

Notes on the counts:
- Findings are distinct findings, not FLAG lines. grok's FLAG totals were 8 / 7 / 21 / 27 / 8 / 17 / 11 / 11 / 9 / 12 / 24;
  REFUTED statements and fact-table claims add the rest, and repeated FLAGs are merged.
- Of the 46 REFUTED, 14 are labelled "record holds", "doubt settled" or "immaterial": grok flagged something unverified and
  the record survived, rather than grok asserting a falsehood. They are sgi_harness_five F27, F28; sgire_pcc2_vme F17, F21,
  F22, F23; pvr_gdrom_four F2; net_three F1, F2; fb_vga_x11_five F6, F11; cpu_policy_two F5, F6; records_three F10.
