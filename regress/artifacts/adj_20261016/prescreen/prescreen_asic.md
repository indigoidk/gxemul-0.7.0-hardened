# Prescreen -- asiceventaddr group (the 2026-10-13 agy pack, re-read by grok, grok-reconcile and Gemini Argon)

PRESCREEN_ASIC_20261016.  Prepared 2026-10-16 for the adj_20261016 adjudicators (packet D input).  It sorts every
distinct grok / grok-reconcile / Argon finding of the seven asic jobs into DISPOSED / LIVE / REFUTED / CANNOT SETTLE.
agy's own flags were harvested on 10-13 (HARVEST.md :47-55, :78-84, :142-195) and are not re-screened.  Agreement
between seats counts for nothing.

**Mode.**  READ-ONLY.  Nothing was built, and no test, probe, gate or project tool was run.  The checks were:
- `git show e483d931:<path>`, `git grep`, `git diff -U0 e483d931` (hunk positions only), `git ls-files`;
- `md5sum`, `cmp`, and `tar -tzf` / `tar -xzOf` to stdout;
- `ls`, `awk` and `grep` over files.

This is the only file written.  Every evidence cell says whether it was READ (opened, grepped or run) or REASONED.

**Jobs:** adj_asic_ruling, asic_backfill, asic_docstring, asic_fixture, asic_gate, asic_seats, changelog_asic_draft.

**Files read.**
- Briefs `agypack_20261013/briefs/<id>.md` (7).
- grok: `agypack_20261013/<id>/grok_<id>.txt` (7) and `grok_reconcile_<id>.txt` (6; changelog_asic_draft has none).
- Argon: `_scratchpad/gweb/jobs_20261014_argonpack6/<id>/gemini_web.out` and `argon_bundle.manifest` (7), plus the seven
  sections of `_scratchpad/gweb/HARVEST_ARGON.md`.
- `agypack_20261013/HARVEST.md`.
- Dispositions and the final state:
  - ADJ;
  - the CONV R-list (:284-317) and the RUL lines cited below;
  - FB's SUMMARY.txt, STATUS.md, PRETABLE.out, PRETABLE_ADDENDUM.out, deliver/* and table2_20261013 (BASE.out head,
    SCORES.txt :280-330);
  - FPS, `FP/codex_rerun/{brief.md,codex_asicpass_records.txt,launch.log}`, `FP/grok_adversarial_finalpass.txt`, and
    from `FP/panel_20261013_234442` the SEATS.txt, the tail of codex.txt and agy.txt;
  - PIN and PINA;
  - PB, for overlap only, and CK's asic lines.
- At e483d931, via `git show`:
  - the header; dev_dreamcast_asic.c :182-192 at three commits; dev_dreamcast_gdrom.c :282-300 and :612-640;
  - src/core/memory.c :85-110; src/include/cpu.h :346-395; configure (`CFLAGS=` and :312-314);
  - tools/CLAUDE.md :2238-2252, :2360-2370, :2465, :2649-2666; tools/panel.sh (a refusal grep);
    tools/precommit_check.sh :887-907;
  - tools/pipeline/ledger.json, row asiceventaddr :24960-25097 and :25199-25210;
  - CHANGELOG.md headings, :198-204 and :2872-2876;
  - OUTSTANDING_BUGS.md :20100-20114, :21600-21614, :21862-21872, :24628-24642;
  - regress/pass2_ledger.tsv :92-96;
  - commits 9ca9ccae / 29b450ce / 4d7b2f41 where cited.
- Also: `_scratchpad/panel_20261009_192422/brief_sent.md:252-312` (the pass-1 R-list), the listings of
  `_scratchpad/panel_20260826_{222557,230207,235440}/`, and `fablequeue8n_20261009/astra_confirm/`.

**Abbreviations.**
- Seats: g = grok; gr = grok-reconcile; A = Argon.
- `H:` = `git show e483d931:`.  Paths are relative to `GXEMUL-SEC/regress/artifacts/` unless shown otherwise.
- ADJ = `asiceventaddr/adj_20261013/fable5_asic_adjudication.md` (v2 from :598).
- CONV = `asiceventaddr/converge_20261009/fable5_converge.md`.
- RUL = `asiceventaddr/f2_20261013/fable5/fable5_ruling.md`.
- FB = `asiceventaddr/f2_20261013/opus5_final/`.  Inside it: SUM = SUMMARY.txt; DRV = deliver/sysasic_range_check.py;
  CAS = deliver/sysasic_range_cases.c; HDIFF = deliver/dreamcast_sysasicvar.h.diff; GDIFF = deliver/gate_offline.sh.diff.
- FP = `asiceventaddr/finalpass_20261013/`; FPS = its `opus5/STATUS.md`.
- PIN = `agypack_20261013/asicpins_spec/grok_asicpins_spec.txt`; PINA = `agypack_20261013/asicpins_spec_adv/grok_asicpins_spec_adv.txt`.
- PB = `adj_20261016/packet_B_asic.md`.  HV = `agypack_20261013/HARVEST.md`.  CK = `_scratchpad/CHECKPOINT.md`.

**Timeline.**
- The briefs were written 10-13 ~20:50-21:00.
- ADJ v1 followed at 22:2x and v2 at 22:5x.
- FB finished 23:41; FP ran 10-13 23:44 -> 10-14 00:39.
- grok answered 10-14 22:43 -> 10-15 00:28.  On docstring, seats and changelog it had already read FB.
- The reconciles ran 10-15 02:41-04:20; Argon answered 10-15 00:10-12:39; PIN and PINA date from 10-15 04:41-05:37.

No seat was given ADJ.

**Seat notes that change how to read the answers.**
- grok AUTO-COMPACTED mid-answer on adj_asic_ruling and on asic_seats: each `.err` is 67 bytes reading
  "Auto-compacting conversation (80%/81% full)".
- `grok_reconcile_asic_docstring` SWAPS THE SEAT LABELS.  Its "AGY" reading is grok_asic_docstring.txt and its "GROK"
  reading is agy_asic_docstring.txt (DS26).
- agy gave no answer on two jobs:
  - adj_asic_ruling: rc 127, 0 b.  Its reconcile is grok vs Argon.
  - changelog_asic_draft: a 429 quota wall.  It has no reconcile.
- Argon's adj_asic_ruling verdict reads "73 TRUE, 0 FALSE", yet it graded four claims TRUE that the files refute
  (AR1, AR2, AR4, AR5).
- Argon's changelog_asic_draft bundle carried 29 indirect wdc473floor files and was truncated before every asic
  artifact.  No finding below rests on an indirect file.  Each one cites ledger.json, OUTSTANDING_BUGS.md or
  CHANGELOG.md, and all of those were checked at H:.

## adj_asic_ruling

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| AR1 | g, gr (A graded TRUE) | RUL:58-59 says "configure has sixteen `CFLAGS=` assignments": 16 match, but :39 is a comment, so 15 assign | DISPOSED | ADJ F34 :162-165 and §4 item 2 :458; GDIFF:64-65 says "sixteen configure lines spell `CFLAGS=`, fifteen assignments and a comment at :39"; H:configure has 16 hits and :39 is a comment [READ] | none |
| AR2 | g, gr (A rewrote the claim and graded it TRUE) | RUL:184 says "ID and TVAL derive their reference from the define itself"; that is false for TVAL | DISPOSED | ADJ §2 item 7 :259-262 and §4 item 3 :460; DRV:160-162 says "TVAL never reads a define" [READ] | none |
| AR3 | g, gr ("NEITHER"; A: "L1 applies") | RUL:56 and :288 grade a closing-pass floor breach L1, while carrier :2249 calls it L2 | DISPOSED | ADJ §2 item 9 :273-275 rules L1.  H:tools/CLAUDE.md:2364-2368: L1 = pre-ship construction, L2 = "the shipped detector" fails a floor clause.  regress/sysasic_range_check.py is absent at e483d931 (gr).  PB F3 also grades L1 [READ] | none: both labels mean repair in-round |
| AR4 | g, gr | RUL:182-183 "invented constants": PHYSICAL 2 is CACHE_NONE, and MEM_WRITE 1 is already the product value | DISPOSED | CAS:32-38 and :48-49 use memory.h's values ("2 is CACHE_NONE there"); "invented" appears in no deliver file [READ] | none |
| AR5 | g, gr (A graded TRUE) | RUL:83-84 puts "independently" inside the quoted false words, but F2_packet:86-87 says that was the true half | DISPOSED | HDIFF:19-23 = ADJ R3 :336-343 [READ].  The new text keeps "independently by two seats -- ONE MEASURING ... one REASONING", quotes the old sentence verbatim, and names the false part ("the measurement was one seat's") | none |
| AR6 | g, gr ("NEITHER"; A: TRUE) | RUL:16-18 says "kimi CLI walled", while SEAT_VERDICTS.txt:4 says "answered" and :11 says "0 walled" | DISPOSED | ADJ F38 :183-189 and §5 :489-493: a 403 wall that seat_verdicts.py misfiled (the HV:42-44 filing) [READ] | record the seat WALLED/COVERED (ADJ §5) |
| AR7 | g, gr sides with g (A: TRUE) | "three uncertain cells" (RUL:88) does not reconcile with SUMMARY's "the two cells" | REFUTED | RUL:88-89 names three row cells: n_exceeds/POL/SWEEP, orswap/PROD/RT, orswap/PROD/RTT.  build SUMMARY:59 counts two PREDICT entries, one of which names two rows [READ] | none; gr's ruling is wrong |
| AR8 | g, gr sides with g (A named the three) | "44 weakenings + 3 floor/breakage" (RUL:89) does not say which three | REFUTED | pass2_20261009/fable5/fable5_pass2.md:127-128 names them: N1_comment, rangeundef, refuseall, which is A's set [READ] | none; gr's ruling is wrong |
| AR9 | g, gr | RUL:267 "four folds then scored 26/26 and 27/27" appears in no named log | DISPOSED | "26/26 green ... for four variants" is fable5_pass2.md:4; "27/27" appears nowhere in pass2 or converge (grep); ADJ v2 item 9 :670-675 replaced the sentence [READ] | cite v2's sentence |
| AR10 | g, gr | section 0's MEASURED rows are in no log; `f2_20261013/fable5_meas/` is absent; the tarball was not opened | REFUTED | `tar -tzf f2_20261013/fable5/fable5_meas.tar.gz` lists meas/F2_MEAS.out, which holds wrong-refuse=1 at 42, pay=0x100000402, 8 IDENTICAL, and census_dummy base=1 guards=1.  The :24-25 path is stale: ADJ §2 item 10 :290-292, §4 item 1 :456 [READ] | cite the tarball |
| AR11 | g | RUL:22-24 "nothing was written into any project tree" was not inspected | CANNOT SETTLE | an absence of writes cannot be recovered now [REASONED].  F2_MEAS.out ("tree copy", "maple restored in the scratch copy: cmp-clean") is consistent with it [READ] | none |
| AR12 | g (gr and A against) | `0xffffffff80000000` (RUL:165-166) is not a logged value | REFUTED | H:OUTSTANDING_BUGS.md:24634 says "GCC yields `0xffffffff80000000` ... MEASURED"; FPS:97-99 measured it again [READ] | none |
| AR13 | g, A, gr | the 1-byte exemption "passes today" was never measured | DISPOSED | SUM:169-170: rsz1_96 is GREEN on PROTO2 and SHIPPED and red on the final SWEEP/TSWEEP [READ] | none |
| AR14 | A, g, gr | the F20 predictions (PHYSICAL->2, `& 2`, alias, a NULL serializer cpu) are unmeasured | DISPOSED | SUM:163-168: green on PROTO2 and SHIPPED, red on final ID+TVAL [READ] | none |
| AR15 | A, g, gr | 9270/9152 is unmeasured | DISPOSED | table2_20261013/BASE.out records lines=9270, erroring=9152 on both legs (gr); SUM:68-69; FPS:8 [READ] | none |
| AR16 | A | the runtime-typed exemption (RUL:145-147) is only PREDICTED | DISPOSED | SUM:72-78 (warrants/w2_rtbcp.out) and :172-173 (rt_bcpll red on POL RT/RTT) [READ] | none |
| AR17 | g, A (gr: wrong in all) | the sixth control, `offset`, has not been built | DISPOSED | SUM:192-195: offset reds PROD TVAL alone [READ] | none |
| AR18 | A | PRETABLE2, table 2, the clean-clone gate, propagation and pass 2 still await execution | DISPOSED | SUM sections 3-6 are done; propagation and the commit are the main loop's (SUM:291-303); pass 2 = FP [READ] | none |
| AR19 | g, gr | F13's archive membership was not checked with a tar listing | REFUTED | `tar -tzf build_20261009/killtable_20261009.tar.gz` lists killtable_20261009/PRODEQ.tsv and SCORES.txt, and no predict/pretable member.  PRODEQ is also extracted at asiceventaddr/killtable_20261009/PRODEQ.tsv, md5 66d6905a = the member [READ] | none |
| AR20 | g, A, gr | t9_syntaxonly.out is not in the artifacts | DISPOSED | SUM:248-253: stage7/t9_syntaxonly_pass2_20261009.out plus the final 9x2 re-run [READ] | none |
| AR21 | g | header md5 daccce33 was not recomputed | REFUTED | md5 of the header at H: = daccce33a5df9e7c3093c310153ce92e, the same as at 4d7b2f41 [READ] | none |
| AR22 | g, A | the peer hunks (gate_offline.sh :1741/:1834/:2276/:2280; check_probe_wiring.py :1407/:1522) were not re-diffed | REFUTED | `git diff -U0 e483d931` puts the peer hunks exactly there; the deliver hunks are at :183, :203 and :1460, so they are disjoint [READ] | none |
| AR23 | g, A | RUL:101's D2 quotation was not re-read | REFUTED | it matches the working tools/CLAUDE.md:1542 word for word [READ] | none |
| AR24 | g, gr, A | the docstrings' byte identity was not hashed | DISPOSED | superseded: the docstring was rewritten (SUM:84-90) [READ] | none |
| AR25 | g | F6: the prototype resolves only one word of CC | DISPOSED | SUM:97-99 and :211-212 (the whole command; legs L12 and L13) [READ] | none |
| AR26 | A (gr) | the ask-again and floor rules are cited at CLAUDE.md:2465 and :2649-2666 | REFUTED | H:tools/CLAUDE.md:2465 is ">" and :2649-2666 is the rung-2/harness text [READ].  The numbers are probably the root copy's, taken from codex.txt [REASONED] | none |
| AR27 | A | bundle omissions: grok_adversarial_f2, configure, CLAUDE.md, the gate, PRETABLE, the sources, and everything in the LEGEND past F21 | DISPOSED | packet-only; every underlying claim is settled in a row above [READ] | none |

## asic_backfill

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| BF1 | g, gr, A | the ledger's `commits` field is "9ca9cca" only | DISPOSED | ADJ R5 :353-355; HV:150 [READ] | none |
| BF2 | A, gr (FOR THE ADJUDICATOR 5), g (changelog R4) | the ledger `state_note` says the two-ended guard was "Added by `#467`/`#468` (`29b450c`)" | LIVE | H:ledger.json:24971 still carries it.  CONV R4 :289-290 owed "upper end #468, lower end #469, quoting the wrong attribution".  ADJ's R-list carries only `commits` (R5) and R7a/b (the inert remedy and 288) [READ] | annotate it in place (an R7d) and quote it: #468 29b450ce is the upper end; #469 4d7b2f41 added the lower end |
| BF3 | g, gr, A | `hold_question` credits RANGE_OK to 9ca9cca | DISPOSED | ADJ R6 :361-369 [READ] | none |
| BF4 | g, gr, A | "352 values" and "5.5x" are wrong (288, 4.5x) in header :111, pass2_ledger.tsv:93, the state_note and 29b450ce's message | DISPOSED | ADJ §0, R1 :310-323, R7b :383-389, R8 :391-395, R14 :447-450; HDIFF:40-50 [READ] | none |
| BF5 | g, gr, A | a raw newline splits the 9ca9cca receipt: pass2_ledger.tsv:93 stops after "a literal" and an opening backtick, and :94 holds the rest | LIVE | H:pass2_ledger.tsv:93 has 6 fields ending at that backtick; :94 has 1 field.  ADJ R8 :391-393 says "append to the LAST COLUMN of the same line" and names :93.  No record mentions the split (grep) [READ] | put R8's erratum at the END of physical line :94; appending to :93 splices it inside the backticked `\n`.  Keep the newline: merging the lines renumbers every later line |
| BF6 | g, gr, A | 9ca9cca's comment at :80 pairs 96..127 with +0x0c, +0x1c | DISPOSED | ADJ F9 :86-88; R9(iii) :405-407 [READ] | none |
| BF7 | g, gr, A | 9ca9cca's comment at :83-84 ("Same for 256..287") reads as mask_13[0], but it is mask_11[0]; 7 of the 9 mask words go unnamed | DISPOSED | ADJ F10/F11 :89-95 and v2 item 3 :625-627; R9(iii) [READ] | none |
| BF8 | g, gr | 9ca9cca's message names 96..127, 128..159 and >= 2048, and not 256..287 (agy said otherwise) | DISPOSED | ADJ F10, message half REFUTED, :91-92 [READ] | none |
| BF9 | g, gr | pass2_ledger.tsv:93's "the sibling citation at :190 still resolves" is false, because 9ca9ccae:190 reads "is LATENT" | REFUTED | 29b450ce:src/devices/dev_dreamcast_asic.c:190 IS the `dreamcast_sysasicvar.h:72` citation.  That commit's +2/-1 edit moved it from 9ca9ccae:189, and 29b450ce wrote the receipt [READ] | none |
| BF10 | g, A | claims in 9ca9cca's message are not in the diff: byte-identical in est/, the Section A sync, no build, the embargo | CANNOT SETTLE | est/ and build/ are untracked, and no artifact of their 08-26 state survives [REASONED] | the #466 block quotes them as the message's claims |
| BF11 | A | the message's no-bypass caller census cannot be settled from the diff | REFUTED | `git grep 'SYSASIC_TRIGGER_EVENT(' 9ca9ccae -- src/devices` finds 15 sites, each passing a SYSASIC_EVENT_* constant.  ADDR appears only in the header and in an asic.c comment [READ] | none |
| BF12 | g, gr, A | 29b450ce's :74-75 says "[0,95] ... NOW ENFORCED" over an upper-only guard | DISPOSED | ADJ F14 :102-104 and R4 :345-351; HDIFF:7-12 [READ] | none |
| BF13 | g | 29b450ce's V0-V3, VLA and `__STDC_VERSION__` claims have no transcript in the commit | DISPOSED | R10's block reports them as the message's claims (ADJ :410-418).  The C89, RT and RTT rows measure the live halves (SUM:57, :72-78) [READ] | none |
| BF14 | A | 29b450ce's header :80-81 says "REFUTED BY MEASUREMENT ... by two seats", but only one seat measured | DISPOSED | ADJ R3; HDIFF:17-23 [READ] | none |
| BF15 | A, gr | :118 "Adding an event >= 96 makes it live" is stale | DISPOSED | ADJ R2 :325-334; HDIFF:56-63 [READ] | none |
| BF16 | A | BITMASK's `1 << 31` at 31/63/95 is left unguarded | DISPOSED | filed as `sysasicbitmask31` (H:OUTSTANDING_BUGS.md:24630-24640); disclosed at DRV:163-167 [READ] | none |
| BF17 | A | 9ca9cca's "no compile-time check can catch the mutant" has since been refuted | DISPOSED | ADJ F12 :96-99; H: header :77-91 already records it [READ] | none |
| BF18 | A | 9ca9cca's gdrom precedent ("`_Static_assert` is C11 ...") is refuted inside gdrom.c itself | DISPOSED | H:dev_dreamcast_gdrom.c:617-628: "THE REASON GIVEN HERE ... IS REFUTED", corrected 2026-08-28 [READ] | the #466 block quotes it as refuted |
| BF19 | A | 9ca9cca broke asic.c's `:74` citation | DISPOSED | ADJ F13 :100-101; 29b450ce re-keyed it (+2/-1) [READ] | none |
| BF20 | g, gr, A | 4d7b2f41's subject does not mention #469 | DISPOSED | ADJ F18 :111-112 [READ] | none |
| BF21 | g, gr, A | "verified at four boundaries" lists five inputs (-1, 0, 95, 96, 128) | LIVE (minor; = CL3) | H:pass2_ledger.tsv:95: "verified at four boundaries: -1 refused, 0 and 95 compile, 96 and 128 refused".  CONV R11 :311-313 adopted an erratum; ADJ R8 covers :93 only [READ] | carry CONV R11's erratum, or rule it harmless (128 is an extra input, not a boundary) |
| BF22 | A | 4d7b2f41 committed no durable negative-control artifact | DISPOSED | the closure's detector is that artifact (FB deliver/; ADJ R5b :355-360) [READ] | none |
| BF23 | gr | hunk counts: 29b450ce's header +50/-13, its asic.c +2/-1, its CHANGELOG @@ -1,3 +1,83 @@; 4d7b2f41's header +13/-2 and CHANGELOG +10/-3 | DISPOSED | ADJ R10/R11 :410-422, F17 :109-110, F20 :115-117 [READ] | none |
| BF24 | gr (FOR THE ADJUDICATOR 1), g | "ship grok's heading family" (`## 2026-08-26 -- #466 ...`), copied from the two top blocks | REFUTED | H:CHANGELOG.md:1 and :59 are records blocks (`## <date> -- records:`).  Code rounds use `` # `#NNN` (slug): `` (:217, :898).  The 2026-08 neighbour is `## Round 467 (#467)` (:17787) [READ] | the commit unit uses the code-round form (Argon's drafts already do) or the 2026-08 form, never the records form |
| BF25 | A | 29b450ce's #467 claims (every pty probe converted; SAFE BY CONSTRUCTION) | DISPOSED | outside this group.  29b450ce:CHANGELOG.md:68 says "Scope is two probes", and 4d7b2f41 amended the lemma (@@ -31,9 +31,16 @@) [READ] | none |
| BF26 | A | 4d7b2f41's wdcringambig and shprotld claims are unsettled | DISPOSED | outside this group.  In H:ledger.json, wdcringambig is closed (cf300c0) and shprotld is its own open row [READ] | none |
| BF27 | A, gr | the BITMASK "+ RANGE_OK" remedy is inert (in the ledger state_note and entry [2]) | DISPOSED | ADJ R7a :371-382 and v2 item 7, R7(c) :650-658; matrix.html is regenerated [READ] | none |
| BF28 | A (FLAG 196), g (changelog R7) | the same inert remedy also stands at H:OUTSTANDING_BUGS.md:21609-21611 | LIVE (= CL4) | see CL4 | see CL4 |
| BF29 | g | no record says 9ca9cca had "no RANGE_OK at all" (the brief's premise) | DISPOSED | a grep of CHANGELOG, OUTSTANDING_BUGS, the ledger and pass2_ledger at H: finds no such sentence.  The fact itself is settled by every seat, and R6's text states it (ADJ :366-368) [READ] | none |
| BF30 | A | packet omissions: the panels, the review dir, the sources | DISPOSED | packet-only [READ] | none |

## asic_docstring

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| DS1 | g, A (ref), gr | the brief's "item 8" is not the docstring; the docstring is item 7 | DISPOSED | ADJ F24 :134-136 [READ] | none |
| DS2 | g, gr | regress/sysasic_range_check.py does not exist at e483d931 (tool denial) | DISPOSED | ADJ v2 item 4 :629-634: not a defect, since the brief named the untracked inputs [READ] | none |
| DS3 | g, A, gr | the sweep pins (9270/9152, 54 samples) are still TO-MEASURE, and no log names the driver | REFUTED | measured in table2_20261013/BASE.out on both legs.  DRV's md5 is 78b7fa63, the same in FB MANIFEST.md5:17 and PRETABLE_ADDENDUM.out.  FPS:8-9 re-ran the delivered driver in a fresh clone and BASE's row lines came out identical.  Residual true: BASE.out:1-3 name the header, cases and memory.h md5s but not the driver's [READ] | optional: add the driver's md5 as one identity line |
| DS4 | g, A, gr | the candidate's "the note says WHICH guard fired" is false | DISPOSED | DRV:82-89 [READ] | none |
| DS5 | A | "only one macro expands per line" is false | DISPOSED | DRV:38 and :44 say "one top-level ... invocation per line" [READ] | none |
| DS6 | g, A, gr | "a raise replaced in any spelling is caught" is false (census_dummy) | DISPOSED | DRV:170-173 [READ] | none |
| DS7 | g, gr | "2**32, the first value five weakenings admit" is false (256 and 129) | DISPOSED | DRV:22-26 [READ] | none |
| DS8 | g, gr | RUL:146 says "runtime e is int-typed", but RT/RTT run int, long long and unsigned long long | DISPOSED | DRV:27-28, :143-146 [READ] | none |
| DS9 | g, gr | RUL:184's ID/TVAL reference (= AR2) | DISPOSED | DRV:160-162 [READ] | none |
| DS10 | g, A, gr | the brief groups gcc 15, LP64, `% 10000`, `__builtin_expect` and `__typeof__` as one class | DISPOSED | DRV keeps them apart: :130-134, :147-150, :151-155 [READ] | none |
| DS11 | g, gr (#5); g on asic_fixture | the C89 row's `-Werror` is presented as part of "the header's own sentence" | LIVE (minor L4) | DRV:36-37 still says "the header's own sentence: ... clean under -std=c89 -pedantic-errors -Wall -Wextra -Werror".  H: header :83-84 has no -Werror.  CAS:366 correctly says "plus -Werror" [READ] | reword DRV:36-37: "the header's sentence (clean under -std=c89 -pedantic-errors -Wall -Wextra), compiled with -Werror" |
| DS12 | g, gr | does "2 earlier verdicts changed" belong in the docstring? | DISPOSED | SUM:183-184 calls it a transition record, so the docstring omits it, and DRV indeed does not carry it [READ] | none |
| DS13 | g, gr | RUL F8's t9 receipt is 6x2, but the final one is 9x2 | DISPOSED | SUM:248-253; DRV:48-49 [READ] | none |
| DS14 | g | "41 of the 43" was not re-counted | REFUTED | asiceventaddr/killtable_20261009/PRODEQ.tsv: 41 media are IDENTICAL in all four TUs, 2 differ, 3 are NOCOMPILE (plus HEAD) [READ] | none |
| DS15 | g | `_Bool` is disclosed but no log covers it | DISPOSED | DRV:138-139.  FPS:77-82 measured `_Bool` at 0/1: green and product-identical [READ] | none |
| DS16 | g | X128 has no sole kill, and the 17-row SCORES was not scanned | DISPOSED | FB table2_20261013/SCORES.txt:285-330: the sole-carrier list has no X128.  FB PRETABLE.out:43 lists X128 among the named refusals that TSWEEP also carries.  DRV claims no unique kill for it [READ] | none |
| DS17 | A | the proto2/candidate docstring still describes 15 rows | DISPOSED | DRV:16-18 [READ] | none |
| DS18 | A | STUB_PHYSICAL is 2 | DISPOSED | DRV:66-77; CAS:32-49 [READ] | none |
| DS19 | A | the 1-byte rank is not sampled | DISPOSED | SUM:67-69 [READ] | none |
| DS20 | A | proto2 lacks the memory.h drift grep, `-fsyntax-only` and `shlex` | DISPOSED | SUM:61-66, :91-101 [READ] | none |
| DS21 | A | the header's claims at :111, :80-81 and :118 | DISPOSED | HDIFF (R1, R3, R2) [READ].  Argon's own "3 x 32 = 96 DROPPED" is wrong: there are two dropped bands, 64 values.  Its 288 conclusion holds | none |
| DS22 | A | the F2 packet misattributed the ADDR variants (F1) | DISPOSED | RUL F1; ADJ §2 item 8 :264-266 [READ] | none |
| DS23 | A | "2 earlier verdicts changed" cannot be checked (cmp_proto is absent from the bundle) | DISPOSED | FB earlier74/COMPARE.out (SUM:177-184) [READ] | none |
| DS24 | A | RUL is PROVISIONAL on F20/F21 | DISPOSED | SUM:6-7 and section 4 [READ] | none |
| DS25 | gr | errors in agy's draft: TSWEEP counted twice; t_singleeval vs f_bcp/rt_bcpll; header lines L65 and L118; TVAL "only bit 32" | DISPOSED | ADJ §2 item 7 :262-264 calls agy's draft "a starting point ONLY"; DRV:16-18, :53-58, :97-99 [READ] | none |
| DS26 | gr | labels: the reconcile's "AGY" reading is grok's answer and its "GROK" reading is agy's | REFUTED (attribution) | the texts gr assigns to GROK are in agy_asic_docstring.txt:68, :99, :223; the texts it assigns to AGY are in grok_asic_docstring.txt:61, :69, :76 [READ] | swap gr's labels before crediting either seat |
| DS27 | A | packet omissions: cases.c, PRODEQ, SCORES, memory.h, configure, the gate, and the sources for `__builtin_expect`, `__typeof__` and t_singleeval | DISPOSED | packet-only [READ] | none |

## asic_fixture

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| FX1 | g, A, gr | the stub defines PHYSICAL as 2 (2 is CACHE_NONE; the product's is 32), and STUB_PHYSICAL = 2 | DISPOSED | SUM:61-66; t_phys2 and t_physand2 are red on the final ID+TVAL (SUM:165-167); CAS:48-49 [READ] | none |
| FX2 | g, A, gr | the memory_writemax64 stub discards cpu, so cpu->byte_order is never read | DISPOSED | the serializer's cpu is pinned (SUM:61-66) and t_sernull is red.  byte_order round-trips: PINA:32 and PB F6 (PB:79) [READ] | list byte_order in PIN's table (as PB F6 says) |
| FX3 | g, A, gr | the memory_writemax64 length is unpinned (5..7, or 8 with bit 128 set) | DISPOSED | the serializer length is pinned to 8 (SUM:61-66), and t_serlen is red (:173-174) [READ] | none |
| FX4 | g, A, gr | `c.mem = (struct memory *)&c` aliases the handle | DISPOSED | the handle is now a distinct memory object, retained apart (SUM:61-66), and t_memalias is red [READ] | none |
| FX5 | A | the stub's `struct cpu` puts `mem` at offset 0, while the product's starts with `machine`.  A TRIGGER that reached the handle by layout (`*(struct memory **)cpu`) would read want_mem on the stub and a different field in the product | LIVE (low) | CAS:42-47; H:cpu.h:346-348 (`machine` first) and :385 (`mem`).  PIN's table (:12-29) and PINA do not mention it [READ].  The masking itself is [REASONED] and unmeasured | disclose it in PIN's fixture-class table, or give the stub struct a leading pad field (one line) |
| FX6 | g, A | memory_rw's cpu is checked only through `mem == cpu->mem` | DISPOSED | cpu is pinned against a retained want_cpu (SUM:61-66), and t_rwcpu is red [READ] | none |
| FX7 | g, A, gr | TVAL leaves payload bits 33..63 unchecked | DISPOSED | DRV:163-167; FPS:97-99 [READ] | none |
| FX8 | g | TVAL's Python reference `1 << (e % 32)` at 31/63/95 was never checked against the compiler | DISPOSED | t_hack31 and b_1u_hack31 were measured in table 2; FPS:97-99; H:OUTSTANDING_BUGS.md:24634 [READ] | none |
| FX9 | g, gr | the proto2 docstring's counts contradict its code | DISPOSED | DRV was rewritten (:16-18, :38-46) [READ] | none |
| FX10 | g, gr | the stub's preamble names four rows, but its `#if` also covers cases 14 and 15 | DISPOSED | CAS:25-28 now names XT96, XTm1, RTT, ID, TSWEEP and TVAL [READ] | none |
| FX11 | g, gr | proto2 presents `-Werror` as part of the header's C89 sentence | LIVE (minor; = DS11) | DRV:36-37 still does [READ] | see DS11 |
| FX12 | g, A, gr | in the shipped candidate the handle, cache_flags and length are unpinned, `c.mem = NULL`, and there are 13 cases | DISPOSED | superseded (ADJ F7 :78-80) by the final ID/TVAL pins (SUM:61-66) [READ] | none |
| FX13 | g, gr | ID and TVAL compute their reference from the printed e, so a renumber inside 0..95 stays green | DISPOSED | disclosed at DRV:160-162 [READ] | none |
| FX14 | g | the stub's `struct memory` is incomplete, so the handle's contents are never read | DISPOSED | TRIGGER passes only the pointer, and its identity is pinned against a distinct object (SUM:61-66) [READ] | none |
| FX15 | gr | agy's memory.h/cpu.h/misc.h line numbers match no file | DISPOSED | ADJ F4 :62-70 and v2 item 2 :615-623; HV:194-195 [READ] | none |
| FX16 | gr | flags of 2 would send the product write through the MMU (memory_rw.c :186/:245; memory_sh.c :338-349) | DISPOSED | that is the product consequence F20 closes; t_phys2 is red [REASONED from gr's reading] | none |
| FX17 | A | the stub does not define MEM_READ | DISPOSED | a MEM_READ mutant fails to compile, so ID and TVAL go red; writes==1 and PIN's pin C (PIN:107-134) cover a wrong writeflag [READ] | none |
| FX18 | A | the drivers and src/core/memory.c are absent from the bundle | DISPOSED | packet-only [READ] | none |

## asic_gate

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| GT1 | g, gr (A: packet-only) | 16 `CFLAGS=` hits, 15 of them assignments | DISPOSED | = AR1 [READ] | none |
| GT2 | gr (agy right), g | grok's anchor assumes no leading whitespace, but configure:313 starts with a TAB | REFUTED (grok's anchor) | H:configure:313 is a TAB followed by `CFLAGS="-DNDEBUG $CFLAGS"`.  A column-0 anchor counts 0; `^[[:space:]]*...$` counts 1, and GDIFF:70 uses that form (`cat -A`, `grep -c`) [READ] | none |
| GT3 | g, gr, A | four quoted includers, no indirect inclusion, and gdrom.c:621 is only a comment | DISPOSED | the anchored lexical file pin, = 4 (SUM:98-100); legs L9/L10 (SUM:209-212) [READ] | none |
| GT4 | g, gr, A | the generated Makefile takes CC, CWARNINGS and COPTIM from the header, and -DNDEBUG rides in COPTIM | DISPOSED | ADJ F35 :166-170; gate block 2 reads CC from the generated Makefile (SUM:97-99) [READ] | none |
| GT5 | g, gr, A | `gate_skip` after a recorded failure exits 1, and need_file does the same | DISPOSED (holds) | lib.sh:137-145, as all three quote it [READ] | none |
| GT6 | g, gr, A | six status greps hardcode a run of spaces (:113, :115, :178, :619, :1358, :1360) at two different widths, and HEAD has no `srctl` | DISPOSED | ADJ F36 :171-174 filed `gatepaddedgreps`; the final srctl is `"^  $2 +PROD +$3 +"` (GDIFF:153) [READ] | none |
| GT7 | gr, A | two siblings: :1115 pins a padded row NAME (8 spaces), and :1351 matches `'^  (ok\|FAIL) '` | DISPOSED | covered by the same filing.  :1351 is a prefix match, and :1115 matches its %-44s printer (gr) [READ] | add :1115 to `gatepaddedgreps` as a name-column sibling |
| GT8 | gr | agy's errors: Makefile.skel:11, not :10; "originate exclusively"; srctl's leg gap; "+" at :1351 | DISPOSED | agy-only; the wiring reads the generated Makefile, and srctl uses ` +` [READ] | none |
| GT9 | A | 352/288 and the inert BITMASK remedy | DISPOSED | = BF4, BF27 [READ] | none |
| GT10 | A | configure and src/ are absent from the bundle | DISPOSED | packet-only [READ] | none |

## asic_seats

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| ST1 | g, gr (#11) | in the final-pass panel panel_20261013_234442, codex REFUSED (two `ERROR: This content was flagged ...` lines after the last `codex` line, no verdict) while SEATS.txt:2 says "362298b answered"; agy WALLED (429, "Resets in 1h44m"); the kimi CLI walled and was covered | LIVE | FP panel: SEATS.txt:2-3 and :11-16, the tail of codex.txt, agy.txt:1-2.  codex_rerun/launch.log: the records re-run answered (INCONSISTENT).  No agy re-fire exists under FP (ls).  H:tools/panel.sh has no content-filter test (grep).  PB F15 (:110) names the failures, but not the mis-score or a re-fire [READ] | record codex as REFUSED in the panel and covered by the re-run; agy WALLED (re-fire it once before the close, or record why not); kimi WALLED/COVERED.  Never copy SEATS.txt:2's "answered".  Record grok_adversarial_finalpass and the opus5 seat |
| ST2 | A (FLAG 18, §5.5), g (changelog R6), A (changelog) | the guard's August pass-2 panels -- panel_20260826_230207 (29b450c) and _235440 (4d7b2f4) -- are recorded on no ledger row, and they exist only in `_scratchpad` | LIVE | both dirs hold full seat sets (ls).  H:ledger.json cites _230207 once, in row seatthinkburn's byte table (:25210), and _235440 never (grep).  H:pass2_ledger.tsv:95-96 cite both.  CONV R6 :293-298 owed one entry per READ answer, _230207's deepseek as SEAT DOWN, and a durable freeze.  ADJ names _230207 only inside R11's CHANGELOG text (:423), and _235440 nowhere (grep) [READ] | copy both dirs durable (as pass 1 was, HV:153), then record each answer with its dir |
| ST3 | g, gr, A | the row records nothing from pass 1, the convergence, the build, pass 2 or F2 | DISPOSED | ADJ §5 :522-529 [READ] | none |
| ST4 | g, gr | SEAT_VERDICTS.txt has kimi "answered, NO VERDICT LINE" and "0 walled" | DISPOSED | ADJ F38 :183-189 and §5 :527-529 [READ] | none |
| ST5 | g, gr, A | codex's own verdicts are the lines after its last `codex` line (pass 1 :2225, pass 2 :3869, F2 :5657); the earlier ones are quotations, and SEAT_VERDICTS calls the seat a "SPLIT" | DISPOSED | ADJ F39 :190-195 and v2 item 10 :677-686 [READ] | none |
| ST6 | g, gr | SEAT_VERDICTS' byte column differs from SEATS.txt (it counts characters) | DISPOSED | ADJ F39/F40 and v2 item 14 :703-705 [READ] | none |
| ST7 | g, A, gr | grok's VERDICT sits mid-line; minimax's is in a fence; agy has a status line and a trailing GO-WITH-CHANGES | DISPOSED | ADJ F42 and F45 (:199-201, :209-210) [READ] | none |
| ST8 | A, gr (vs agy) | the pass-1 artifact panel has no seat copies | DISPOSED | ADJ v2 item 13 :698-701: copied at 22:2x, and `diff -rq` is IDENTICAL.  agy's flag was true at 21:06, so gr's "AGY wrong" ignores when agy answered [READ] | none |
| ST9 | g | ledger.json:62489 cites fablequeue8n_20261009/astra_confirm/codex_astra_asicconverge.txt instead of converge_20261009/codex_astra_converge.txt | REFUTED | `cmp`: IDENTICAL (10,466 b); the fablequeue8n copy is tracked (git ls-files) [READ] | none |
| ST10 | g, gr | answers still to record: ADJ v1 and v2, codex_asicconfirm, codex_asicadj (whose .err:31 is an earlier UNCHECKABLE turn) | DISPOSED | ADJ §5 :514-519 and v2's owed list :713-716 [READ] | record v2 as the standing verdict |
| ST11 | g, gr | seat+date collisions; entry [10] is dated 08-26 but recorded 10-09; entries [0] and [1] | DISPOSED | ADJ §5, F44 :204-209, v2 item 11 :688-691 [READ] | give each entry its ev |
| ST12 | A | "no grok_adversarial_* file exists under asiceventaddr/" | REFUTED | f2_20261013/grok_adversarial_f2.txt and finalpass_20261013/grok_adversarial_finalpass.txt both exist (ls) [READ] | none |
| ST13 | A | kimi-k3's "GAP AS STATED" is outside the brief's verdict vocabulary | DISPOSED | the verdict is recorded verbatim; nothing follows from it [READ] | none |
| ST14 | g | byte lengths were not stat()'d, and two artifact copies have no .err files | DISPOSED | ADJ F41 :197-198: the .err files were 0 bytes, so nothing is lost [READ] | none |
| ST15 | A | the bundle cuts pass-1 codex.txt before codex's own turn and leaves out the artifact copies | DISPOSED | packet-only; g and gr settle the verdict at :2224-2225 [READ] | none |

## changelog_asic_draft

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| CL1 | g (its draft uses CONV's numbering), A | TWO R-LISTS COLLIDE.  The brief and grok's draft number by CONV's R1-R13 (:284-317); the commit unit works from ADJ's renumbered R1-R14 (:304-450; HV:150-152; SUM:285-287).  The renumbering dropped five CONV items: R4's state_note half (BF2), R6 (ST2), R8's errata half (CL2), R11 (CL3), and R7's OUTSTANDING_BUGS carrier (CL4) | LIVE | both lists [READ].  The builder already caught one drop of this kind, gdrom.c's R10 (SUM:39-42) [READ] | before the commit unit runs, diff ADJ's list against CONV's and carry the five drops |
| CL2 | g (R8), A | the "never fired" and "HELD for opus5" text stands at three sites: ledger entry [9] at :25059 ("fable5 and opus5 were never fired"), CHANGELOG.md:2874-2875 ("now HELD for fable5, opus5 and deepseek") and OUTSTANDING_BUGS.md:21869.  But opus5 answered on 2026-08-26 (entry [10]) | LIVE | all three at H: [READ].  CONV R8 :302-305 owed an errata entry and a dated CHANGELOG correction.  ADJ §5 only discharges and defangs the marker (:526-527) [READ] | dated in-place corrections that quote and refute (CONV R8) |
| CL3 | g (R11); g, A, gr (four boundaries) | errors in two receipts.  pass2_ledger.tsv:95 (29b450c) credits "+opus5 Agent seat" and says "Fixed to ((e) >= 0 && (e) < 96)" (#469's fix) "at four boundaries" (five inputs).  :96 (4d7b2f4) puts 8of9 beside "SEVEN OF EIGHT SCRIPTABLE ANSWERED", and "UNANIMOUS" beside glm's refuted dissent.  The receipts' "b" counts are characters | LIVE | H:pass2_ledger.tsv:95-96 [READ].  CONV R11 :311-315 owes these errata; ADJ R8 covers :93 only (grep finds no :95/:96) [READ] | add ERRATA clauses; annotate, never renumber (CONV R11) |
| CL4 | g (R7), A (backfill FLAG 196, changelog) | H:OUTSTANDING_BUGS.md:21609-21611 still prescribes the inert remedy: "The remedy is already in the file and costs one token: give BITMASK the same `+ SYSASIC_EVENT_RANGE_OK(e)`" | LIVE | H: :21609 [READ].  CONV R7 :299-301 named this anchor.  ADJ v2 item 7 (:650-656) lists ledger :24971, :24998 and matrix.html:3435, and calls every other hit a quotation [READ].  Its quoted text is upper-case while :21609 is mixed-case [REASONED] | add :21609 to R7 and annotate it in place with R7(a)'s text |
| CL5 | g | "UNANIMOUS" is not in :96 | REFUTED | H:pass2_ledger.tsv:96 contains "UNANIMOUS VERDICT: the guard is COMPLETE" [READ] | none |
| CL6 | g | the five inputs behind "four boundaries" were not re-read | REFUTED | :95 lists -1, 0, 95, 96 and 128 [READ] | none |
| CL7 | g | the build SUMMARY's "47 of 47" vs RUL's "44 + 3" | DISPOSED | the three are N1_comment, rangeundef and refuseall (fable5_pass2.md:127-128); the final SUM partitions by clause (:135-148) [READ] | none |
| CL8 | g | the build's PRETABLE.out:2-3 describes a refusal that run_table.sh does not implement | DISPOSED | build_20261009/SUMMARY.txt:100-103: a wrong record left in place on purpose, to keep the mtime order proof [READ] | the closing block must not repeat :2-3 |
| CL9 | g | F2_packet:47 "no earlier verdict changed" vs Opus | DISPOSED | RUL adopts Opus's figure; FB earlier74/COMPARE.out (SUM:177-184) [READ] | none |
| CL10 | g | which five of the ten new lines error, and which two samples are duplicates? | DISPOSED | 9270/9152 is measured (BASE.out); the duplicates are (char)95 and (signed char)-1 (ADJ F32 :151-154) [READ] | none |
| CL11 | g | SEAT_VERDICTS: kimi, the bytes, codex's SPLIT | DISPOSED | = ST4-ST6 [READ] | none |
| CL12 | g | daccce33 was not recomputed | REFUTED | = AR21 [READ] | none |
| CL13 | g | `f2_20261013/fable5_meas/` is absent and the tarball was not extracted | REFUTED | = AR10 [READ] | none |
| CL14 | g | the named sources stop at F2, although FB, ADJ and FP exist | DISPOSED | the closing block must reach FB, FP and the pins round (SUM section 9) [READ] | none |
| CL15 | A | the state_note's 352; the BITMASK remedy; the stale witness and hold_question | DISPOSED | = BF4, BF27; ADJ R5b :355-360 and R6 :361-369 [READ] | none |
| CL16 | A | the state_note's "TWO SEATS INDEPENDENTLY REFUTED ... ONE OF THEM BUILT ALL FOUR VARIANTS" contradicts one-measured-one-reasoned, and the three seats named lower down | REFUTED | H:ledger.json:24971 has no "BY MEASUREMENT", so the sentence is true as written.  The three seats lower down attacked the warrant, which is a different claim.  ADJ R3 corrects the header's "BY MEASUREMENT" form [READ] | none |
| CL17 | A | OUTSTANDING_BUGS.md:20111-20112 ("FOUR have no seat entry at all (... asiceventaddr ...)") is stale | REFUTED | :20108-20112 is a census of seataudit_20260917/COVERAGE.txt, dated by that artifact, not a live status [READ] | none |
| CL18 | A | the two guard pass-2 panels are recorded nowhere | LIVE (= ST2) | see ST2 | see ST2 |
| CL19 | A (its own draft) | Argon's draft calls the bit-field `event_out_of_range` | REFUTED | it is `sysasic_event_lt_96` at 29b450ce:...h:126 and `sysasic_event_in_range` at H:...h:136 [READ] | do not adopt Argon's draft text |
| CL20 | A | the bundle lost the asic artifacts to truncation and carried 29 indirect wdc473floor files | DISPOSED | packet-only; no finding above rests on an indirect file [READ] | none |

## LIVE items for the adjudicators

1. **CL1 -- two R-lists collide.**  The commit unit's R-list (ADJ R1-R14, per HV:150-152 and SUM:285-287) is a
   renumbering of CONV's R1-R13 (:284-317), and it silently drops five CONV obligations: items 2-6 below.  Diff the two
   lists before the commit unit runs.  The builder already caught one drop of this kind: gdrom.c's R10 (SUM:39-42).
2. **BF2 -- the state_note's attribution (CONV R4).**  H:ledger.json:24971 still credits the two-ended guard to
   "`#467`/`#468` (`29b450c`)".  The fix is an in-place annotation: #468 added the upper end, #469 (4d7b2f41) the lower.
3. **ST2 / CL18 -- the August panels (CONV R6).**  The guard's own pass-2 panels, `_scratchpad/panel_20260826_230207`
   (29b450c) and `_235440` (4d7b2f4), are on no ledger row and sit only on a volatile path.
   - Copy both durable, then record each answer with its dir; _230207's deepseek is SEAT DOWN.
   - ADJ names _230207 only in R11's CHANGELOG text and never names _235440.
4. **CL2 -- the "never fired" errata (CONV R8).**  Three sites still carry it: ledger :25059 ("fable5 and opus5 were
   never fired"), CHANGELOG.md:2874-2875 and OUTSTANDING_BUGS.md:21869.  opus5 answered on 08-26.  ADJ §5 only
   discharges and defangs the marker, so the dated corrections are still owed.
5. **CL3 + BF21 -- the receipt errata (CONV R11).**  pass2_ledger.tsv:95 has an unsupported "+opus5 Agent seat"
   credit, a "Fixed to" sentence that describes #469, and "four boundaries" over five inputs.  :96 has 8of9 vs "SEVEN
   OF EIGHT" and "UNANIMOUS" vs glm's dissent; the "b" counts are characters.  ADJ R8 annotates :93 only.
6. **CL4 + BF28 -- the third R7 site.**  H:OUTSTANDING_BUGS.md:21609-21611 still prescribes the inert
   `+ SYSASIC_EVENT_RANGE_OK(e)` remedy.  CONV R7 named this anchor; ADJ v2 item 7's sibling sweep (:650-656) missed it.
7. **BF5 -- R8's anchor.**  The 9ca9cca receipt spans pass2_ledger.tsv:93-:94, joined by a raw newline.  R8's
   "append to the last column of the same line" at :93 would splice the erratum inside the backticked `\n`.  Anchor it
   at the end of :94, and do not merge the lines.
8. **ST1 -- the final-pass seat record (panel_20261013_234442).**
   - codex REFUSED (a content-filter ERROR, no verdict), but SEATS.txt:2 scored it "answered".  The records re-run
     covers it.
   - agy WALLED on a 429 and has no re-fire on record; the kimi CLI walled and was covered.
   - PB F15 names the failures but not the mis-score or the re-fire.
9. **DS11 + FX11 -- the C89 wording (minor L4).**  DRV:36-37 presents `-Werror` as part of "the header's own sentence";
   the header (:83-84) has none.  This is a one-clause rewording.
10. **FX5 -- stub layout (low, exotic).**  The stub's `struct cpu` puts `mem` at offset 0 (CAS:42-47), whereas the
    product's starts with `machine` (cpu.h:346-348).  A handle reached by layout would be masked.  Disclose it in
    PIN's fixture-class table, or add a leading pad field.

**Outside the screened set (not counted).**  FP's codex re-run (Q4) found that FB PRETABLE.out says "123 header media
(BASE, HEAD_e483d931 and 121 variants) + 9 product-TU".  SUM:126 has 114 header media + 9 TU = 123.
- Neither PIN nor PB carries it (grep).
- The file is the mtime order proof, so record the erratum beside it rather than edit it.

## Counts

| job | rows | DISPOSED | LIVE | REFUTED | CANNOT SETTLE |
|---|---|---|---|---|---|
| adj_asic_ruling | 27 | 17 | 0 | 9 | 1 |
| asic_backfill | 30 | 22 | 4 | 3 | 1 |
| asic_docstring | 27 | 23 | 1 | 3 | 0 |
| asic_fixture | 18 | 16 | 2 | 0 | 0 |
| asic_gate | 10 | 9 | 0 | 1 | 0 |
| asic_seats | 15 | 11 | 2 | 2 | 0 |
| changelog_asic_draft | 20 | 8 | 5 | 7 | 0 |
| **total** | **147** | **106** | **14** | **25** | **2** |

**Distinct LIVE items across the jobs: 10.**  Four rows are repeats and count once: BF21 = CL3, BF28 = CL4,
FX11 = DS11, CL18 = ST2.  **None of the ten touches the instrument's coverage or the pins spec except FX5 (low).**  Five
of them (items 2-6) are records that the renumbered R-list dropped; the other three are BF5, ST1 and DS11.
