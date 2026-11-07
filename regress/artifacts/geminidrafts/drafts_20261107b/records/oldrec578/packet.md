# Reading task: oldrec578 (Gemini web; 2026-11-06)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC578-5546` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #578 jazzvecdeassert (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 1254-1400 at HEAD 116c5aa9; each line carries its own number -- cite those numbers)

```text
 1254| # `#578` Records (follow-up, 2026-11-02): `jazzvecdeassert` names its landing commit `2a24d9b7`; the committed-tree proofs; the pass-2 receipt
 1255| 
 1256| `git ls-tree 2a24d9b7` shows `regress/jazz_vector_probe.py` at `100644 blob 3389480fccb0bfc407fd6658cdf0e2f0bca2c067`, blob md5 `37cbfc835297` (the shipped 26-row revision: AST-identical to table 3's as-run copy `7b3e17e7d3f0` with the module docstring dropped, `regress/artifacts/jazzvecdeassert/killtable3_20261102/ASRUN_NOTE3.txt` listing the four docstring-only edits; LF, no CR byte); `src/devices/dev_jazz.c` at blob `e64e8704a21a...`, md5 `098103e4f82e` -- the twin-neutral comment wording, the copy propagated to build-asan/ and /tmp/gxsec-build (`landing_20261102/PROP_FINAL.out`: part 1 cmp CLEAN per tree's reference, part 2 binary newer; build/ carries est's copy, md5 `4a94958aa2fd`, same function); `regress/gate_mips.sh` md5 `ecf7c231666b`, `regress/gate_hygiene.sh` `86763930b8d0`, `tools/precommit_check.sh` `3a1a09798ec3`, `tools/pipeline/check_probe_wiring.py` `26a8c3a32610` (HEAD's copy plus the #578 block; the peer's uncommitted lines stay in the working tree).  `git diff --numstat 2a24d9b7^ 2a24d9b7`: `7 2 src/devices/dev_jazz.c; 318 0 regress/jazz_vector_probe.py; 28 0 regress/gate_mips.sh; 1 1 regress/gate_hygiene.sh; 11 3 tools/precommit_check.sh; 39 0 tools/pipeline/check_probe_wiring.py`; 179 artifact files under `regress/artifacts/jazzvecdeassert/`.  Gates 1 and 4 on the propagated tree before the landing: `landing_20261102/GATE14_RUN_wsl2.txt` (arc 13/13, the `#578` block 26/26, REGRESS_PASS).  The hook: 0 hard, 5 soft (`_scratchpad/w578/landing/bk_20261102_220009_10692/commit.out`).  The row's `commits` field now names `2a24d9b7`; its state stays `held` for the hold question (Fable as the main-loop adjudicator rather than a seat; Astra walled through pass 2 and F2; the deletion ruling).
 1257| 
 1258| Ledger (the `commits` field and the state note's date), this block, the `regress/pass2_ledger.tsv` receipt line, a landing line in OUTSTANDING_BUGS.md's `#578` section, `matrix.html` and `fable_queue.md` re-rendered.
 1259| 
 1260| # `#578` (2026-11-02) -- `jazzvecdeassert` (OB-22): a Jazz interrupt-source access no longer deasserts the CPU's IRQ3 while JAZZ lines are pending
 1261| 
 1262| **The defect.**  `src/devices/dev_jazz.c`, `DEVICE_ACCESS(jazz_jazzio)` (HEAD `50f9c601` :696-697): every access to the pica_jazzio
 1263| register (physical 0xf0000000, 4 bytes: offset 0 the local-bus interrupt-source vector the guest reads to find which JAZZ line is pending,
 1264| offset 2 PICA_SYS_LB_IE, stored by the model as `jazz_timer_value`) ended with an unconditional `INTERRUPT_DEASSERT(d->mips_irq_3)` under
 1265| "This is needed by Windows NT during startup".  A guest servicing one line read the vector and thereby lowered the CPU's IRQ3 while a
 1266| second JAZZ line was still pending and enabled -- a level interrupt dropped until a line was asserted anew (a still-enabled UART's tick,
 1267| `dev_ns16550.c:92-97`; the interval timer's tick, `dev_jazz.c:294-308`; any new device assert) or EXT_IMASK TRANSITIONED into the enabled
 1268| state (:466-469; a same-value rewrite heals nothing).  OB-22 is this file's oldest open entry (triage of 2026-07, "self-healing,
 1269| correctness-only, would touch the verified arc boot"); its remedy wording there ("without clearing int_asserted") named the wrong repair.
 1270| Severity LOW as measured: OpenBSD's `pica_iointr` loops on the vector until it reads 0 and arms the interval timer, so the drop heals within
 1271| a tick on that guest; NT unmeasured (no image).  Upstream residue (the comment and the statement are the 0.7.0 import's).  Not a host
 1272| failure path.
 1273| 
 1274| **The witness (rung 3).**  `regress/artifacts/jazzvecdeassert/witness_20261102/jazz_vector_witness.py` (13 rows, built on the harness
 1275| library `_scratchpad/gxprobe.py`) on the UNMODIFIED in-tree `-V -e pica` (the rig kernel loaded for construction only): two ns16550 UARTs
 1276| (`machine_arc.c` wires them to jazz.8 and jazz.9) are made to assert their lines by genuine guest stores to MCR and IER through XKPHYS
 1277| (one-instruction stubs run with `step`; a UART asserts synchronously inside the IER store when MCR.IENABLE is set), EXT_IMASK is written to
 1278| 0x2, and COP0 Cause's IP3 bit is read with `print cause`.  On a fresh clone of HEAD built in WSL: `witness_head.out` 11/13 -- `jz ip after`
 1279| (IP3 after the vector read, both lines pending) and `jz ip com1` read 0 against 0x800 -- with the liveness control `jz ip one` (IP3 set
 1280| after the first IER store) and the device-signature control `jz vec` (the vector reads 0x24 = (8 + 1) << 2, which RAM cannot answer) green;
 1281| the same script on the fixed clone: 13/13.  Written 20:16:03, before the fix applier (20:16:39) existed.
 1282| 
 1283| **The fix.**  The statement is DELETED and a seven-line `#578` comment stands where it was (`killtable3_20261102/product_final.diff`, +7 -2;
 1284| `product_c.diff` is the table-3 wording before agy's F2 change 5): the tail used to deassert on every access, dropping a level interrupt
 1285| while JAZZ lines were still pending until a line was asserted anew or the enable mask re-admitted it; the CPU line is kept equal to "a
 1286| JAZZ line pending and enabled" by `jazz_interrupt_assert()`, `jazz_interrupt_deassert()` and the EXT_IMASK arm; an access to this register
 1287| no longer touches it -- wording true of both twins (SEC's predicate is the IP3 bit of EXT_IMASK, est's the per-line enable bits).  Byte-identical in `GXEMUL-SEC` and
 1288| `est/` (the function is identical in both twins although `dev_jazz.c` is a divergence-set file; est keeps the pre-#69 per-line predicate
 1289| `int_asserted & int_enable_mask & 0x7fff` in ITS three writers).  Pass 1 proposed a CONDITIONAL deassert (`if (!((int_asserted & 0x7fff)
 1290| && (int_enable_mask & R4030_EXT_IP3))) INTERRUPT_DEASSERT(...)`) and five of seven seats preferred it for robustness; the ruling is the
 1291| DELETION, on (i) the checked writer census -- `mips_irq_3` is written by the assert handler (:144), the deassert handler (:154) and the mask
 1292| arm (:467/:469) and nowhere else, the MIPS `mtc0 Cause` arm writes IP0/IP1 only (`cpu_mips_coproc.c:949-954`), so by induction the line is
 1293| EQUAL to the predicate and the conditional's guard can never fire with an effect; (v) the house form (the tree's other controllers keep
 1294| their CPU line from their handlers); with (ii) the measured equivalence (M_del 13/13, M_cond 22/22 and 26/26) recorded as ENTAILED by (i)
 1295| rather than independent of it, and (iii) the est-compile fact (est has no `R4030_EXT_IP3`) recorded as a convenience, both per the Opus
 1296| seat's F2.  The NT-startup risk -- if NT relied on the blanket deassert as a stand-in for LB_IE masking -- falls on both forms equally and
 1297| is carried by `jazzlbmask`.  The invariant holds in est over est's own predicate by the same induction; est's copy is UNMEASURED (no
 1298| binary, and the probe's EXT_IMASK = 0x2 would mask lines 8/9 under est's per-line predicate).
 1299| 
 1300| **The detector.**  `regress/jazz_vector_probe.py` -- 26 rows, SELF-CONTAINED (its own pty driver, prompt-detected `GXemul>`, no import
 1301| outside the standard library), on the arc rig binary gate 4 already boots (`-V -e pica`): the two UART lines, the vector at 32 and 8 bits,
 1302| stores to offsets 0, 2 (a 16-bit nonzero LB_IE) and 3, reads of offsets 1 and 2, the mask off and on, nothing pending, and the "Windows NT"
 1303| case (a vector read with nothing pending: IP3 already clear on every build, a no-regression row).  Names stay at 13 characters or fewer
 1304| (`%-14s`; gate 4 anchors `^name  .*ok$` with two spaces -- the padded-column trap).  The driver records any timed-out or failed command
 1305| (`JAZZVEC_DRIVER=bad`; a store the debugger never executed would otherwise read exactly like a fixed build on every later IP3 row) and ends
 1306| with `JAZZVEC_RESULT=n/N`, `JAZZVEC_DRIVER`, `JAZZVEC_DONE`.  `regress/gate_mips.sh` gains the `#578` block after the arc boot: rows run 26
 1307| by EQUALITY, rows correct, the driver flag, the 26 names, the completion sentinel; the pty transcript lands in `$LOGDIR`.  Contract
 1308| (the probe's docstring): lines 8 and 9 and mask values 0x2 and 0 are driven; every access-label cell of the enclosing function's own tests
 1309| -- {0, 2, default} x {read, write} -- is rowed with lines pending; `len` 1/2/4, `idata` 0/nonzero and `jazz_timer_value` 0/0x0f are each
 1310| driven on both sides, so a re-introduction of the deleted statement keyed to any one of them AT THE VALUES THE ROWS DRIVE reds; OpenBSD/arc's three
 1311| access shapes to this register are named: the vector read as a BYTE (`inb(PVIS)`) is rowed, and its two LB_IE halfword stores (0 at
 1312| initcpu; the COM enable bits at intr_establish) are disclosed and filed (`jazzvecrowsowed`, Grok F2); a predicate separating values inside a
 1313| driven side (`idata & 0xff00`) and any other conjunction are clause-(e) debt, disclosed; a re-introduction keyed to lines the rows do not
 1314| drive or to another mask value is disclosed.  SCORE_CLAIMS_MANIFEST 42 -> 43; gate 6's `EXPECT_PTY_PROBES` 80 -> 81 (the probe is
 1315| prompt-detecting, not promptless; written by `derive_hygiene_pins.sh --write`); `check_probe_wiring.py` gains the MANIFEST key and one entry
 1316| per artifact script.
 1317| 
 1318| **The tables** (`regress/artifacts/jazzvecdeassert/`; scratch clones of the HEAD tree only, a `.MUTANT` sentinel per clone, each
 1319| `<leg>.raw` naming its binary, md5, freshness and the instrument's md5; each `PRETABLE*.out` written before its table's first leg, the
 1320| corrections and refuted predictions in SIBLING files):
 1321| 
 1322|     table 1  killtable_20261102/   the 13-row witness, the CONDITIONAL form, 7 forms   base 11/13  fixed 13/13  null 0/13
 1323|              the reinstated statement and four re-keyed forms 11/13 each; the deletion and a mask-free form 13/13 (equivalent)
 1324|              (run 1 refused: the presence pin matched twice -- the conditional's two lines also exist in jazz_interrupt_deassert --
 1325|              so the mutator was re-anchored on the fix's comment line, PRETABLE_CORRECTION.out)
 1326|     table 2  killtable2_20261102/  the 22-row detector, the DELETION form, 8 forms     base 15/22  fixed 22/22  null 0/22
 1327|              re-introductions keyed to the offset (0: 18; not 0: 18; 2: 20) or the direction (read 17, write 20) red; the
 1328|              conditional 22/22 (equivalent); keyed to undriven lines 22/22 (disclosed); one prediction refuted (18 not 19: a drop
 1329|              just before com0's IER is cleared is not healed while com1 stays pending -- "com1 inherits", PRETABLE2_CORRECTION.out)
 1330|     table 3  killtable3_20261102/  the SHIPPED 26 rows, 15 forms                       base 17/26  fixed 26/26  null 0/26
 1331|              the eight forms of table 2 again (21, 21, 20, 22, 24; 26, 26; base-equal 17) and the seven the pass-2 seats named:
 1332|              default-arm write 24/26, idata nonzero 23/26, idata zero 19/26, LB_IE nonzero 21/26, len 2 25/26, the byte vector
 1333|              read 25/26, offset 3 24/26.  EVERY prediction of PRETABLE3.out (21:06:01, before base_head.raw 21:07:50) matched in
 1334|              score and in red set; JAZZVEC_DRIVER=ok on every leg but the null medium.
 1335| 
 1336| Floor: (a) 17/26 on HEAD; (b) the removed statement reinstated (the comment stays, so the binary's md5 differs from HEAD's -- cause not
 1337| established; the `strings` comparison run here cannot see a `__LINE__` immediate; the likely cause, reasoned by Grok, Opus and agy and not
 1338| measured, is `CHECK_ALLOCATION` at `dev_jazz.c:712` formatting `__LINE__` -- 712 on HEAD, 718 under the reinstated statement -- while
 1339| `#577`'s `cpu_sh.c` has no such site after its edit; the settling check is `objdump -d` or `cmp -l` on `dev_jazz_init`); (c) measured, `/bin/true` as the medium; (d) the fix depends on no predicate of its own (a pure deletion), so the (d)
 1340| forms are the deleted behaviour re-introduced under the enclosing function's own tests -- {offset} x {direction}, all six cells rowed and
 1341| each single-cell form red -- plus the single-input families above; (e) the contract; (f) not applicable (no address decode changed).
 1342| The instrument table 3 ran is preserved as `jazz_vector_probe.ASRUN.py` (md5 7b3e17e7d3f0); the shipped probe differs from it by one
 1343| docstring passage (the contract's "at the values the rows drive" wording, Opus F2 change 1; `ASRUN_NOTE3.txt`) and by nothing else -- the
 1344| two ASTs are identical with the module docstring dropped.  Two driver edits preceded table 3 and are recorded in the same note: the
 1345| `quit` command had set the failure flag on every run (dryrun26/), and two docstring literals were reworded for section U.
 1346| 
 1347| **The panel** (owner roster 2026-11-02 20:5x: Grok 4.7 xhigh, the four Ollama cloud seats glm-5.3 / deepseek-v4-pro / minimax-m3 /
 1348| kimi-k3, Opus 5.5 as the Agent seat, GPT-6 Astra on the hotmail login; Fable 5.1 adjudicating in the main loop, not a seat; agy and the
 1349| Gemini web route not fired).  Pass 1 (`regress/artifacts/jazzvecdeassert/pass1_20261102/`, the design brief with the conditional form): Opus PROCEED WITH
 1350| CHANGES (6) -- argued the DELETION from the writer census and predicted the conditional's equivalence; Grok PWC (2); Astra PWC (2); glm
 1351| PWC (2); kimi PWC (2); minimax PWC (3); deepseek PROCEED.  Pass 2 (`regress/artifacts/jazzvecdeassert/pass2_20261102/`, the deletion, the 22-row detector, both tables): Opus
 1352| SHIP WITH CHANGES (5), Grok SWC (3), glm SWC (3), deepseek SWC (3), minimax SWC (3), kimi SWC (2); Astra SEAT WALLED (0-byte answer, the
 1353| hotmail login's limit).  Every seat held the deletion; every seat found the contract sentence "every access label ... read and write" false
 1354| -- the (default, write) cell had no row -- and the (d) enumeration incomplete over `idata`, `len` and `jazz_timer_value`; Grok added the
 1355| guest's own BYTE vector read (`inb(PVIS)`) and offset 3; Opus the driver failure flag, the gate's transcript path and sentinel, est's
 1356| own predicate, "reinstated" not "verbatim", and the comment's three over-statements; Grok that `dev_algor.c` deasserts on a read, so the
 1357| comment's "as in the tree's other interrupt controllers" was false and is gone.  Repaired in-round (the unrowed label cell is a floor cell
 1358| under the joint-cell reading, L2, and the contract an L4 wrong record); twenty-three findings F1-F23 and their dispositions are in
 1359| `regress/artifacts/jazzvecdeassert/briefs_20261102/brief_jazzvecdeassert_f2.md` section 0.  The repair's own pass (F2, `regress/artifacts/jazzvecdeassert/f2_20261102/`): Opus RATIFY WITH CHANGES (4) -- zero floor breaches
 1360| with the denominator stated (the six label cells, the three single-input families, the conjunction forms), so the repair chain closes on
 1361| this pass; its four changes: the contract's "any ONE of them reds" overstated (holds at the driven values; `idata & 0xff00` predicted
 1362| 26/26, DISCLOSED -- corrected in the docstring), the `strings` check cannot settle F12 (recorded above), whether a guest reads LB_IE at 16
 1363| bits was not checked (disclosed in the contract), and the startup prompt wait's result is unchecked by the driver flag (filed,
 1364| `jazzvecrowsowed`); Grok RATIFY WITH CHANGES (1) -- zero floor breaches, and the D3/F5 claim that the byte read is the ONE conjunction the
 1365| guest exercises is false: it read the OpenBSD/arc source and found two LB_IE halfword stores (`initcpu`'s 0 and `intr_establish`'s mask
 1366| with COM bits 0x0100 and 0x0200), neither rowed, `idata & 0x0100` at offset 2 predicted to keep every row green -- filed, the contract
 1367| corrected; GLM 5.3 RATIFY WITH CHANGES (2) -- the docstring's 'becomes true' was edge wording for a level handler, and the clause-(e)
 1368| example was mislabelled (both corrected); kimi RWC (2) and minimax RWC (2), fired under the earlier roster, each named a disclosure gap
 1369| (undriven values; the default cell's offset refinements), now disclosed by name; deepseek SEAT DOWN (HTTP 502); agy (gemini-4-argon-high, file-reading, fired
 1370| under the owner's 21:3x roster) pass 2 SHIP WITH CHANGES (4) and F2 RATIFY WITH CHANGES (5) -- its items 1-3 were the corrections already
 1371| on disk, which it checked; item 4 the same `strings` point; item 5 a real catch: the applier wrote SEC's "EXT_IMASK.IP3" comment into
 1372| est, whose enable predicate is per-line, so the sentence was false of est -- the comment is now twin-neutral ("a JAZZ line pending and
 1373| enabled"; "the enable mask re-admitted it") in both trees, `product_final.diff`, propagated and rebuilt (`regress/artifacts/jazzvecdeassert/landing_20261102/PROP_FINAL.out`), gates 1 and 4 re-run
 1374| (`regress/artifacts/jazzvecdeassert/landing_20261102/GATE14_RUN_wsl2.txt`: arc 13/13, the block 26/26, REGRESS_PASS); Astra SEAT
 1375| WALLED.  Every answering seat found zero floor breaches, so the repair chain closes on this pass
 1376| 
 1377| **Not changed (assessed, intentionally left).**  LB_IE's enable bits are unmodelled (`jazzlbmask`; the NT risk above is carried there);
 1378| the vector scan at offset 0 ignores `int_enable_mask` (`jz vec masked` pins the current behaviour; noted under `jazzlbmask`); the
 1379| `default:` arm's unlatched `fatal()` is guest-drivable (`jazziodfltflood`, filed; `jazz_20`/`jazz_a0` share the shape); clearing
 1380| MCR.IENABLE with the UART's IER/IIR condition true neither asserts nor deasserts (`ns16550out2hold`, filed; pass-1 F9); the "Linux?" tick
 1381| arm is inert under single-step and unchanged.  Three strengthenings the F2 pass named (a zero halfword LB_IE store row, lbiew at 0x0300, the startup-wait flag) are
 1382| filed, not shipped: the chain closed and the shipped instrument is the one table 3 measured.
 1383| 
 1384| **Harness, in this commit.**  `tools/precommit_check.sh` section B compared every changed `src/` file against build/ with SEC as the
 1385| reference; build/ is compiled from est/ (`gate_build.sh:4`), so for a path in `tools/est_divergence.txt` the reference is est's copy --
 1386| the section now derives that, as section A already did; this landing is the first edit to a divergence-set file since the section existed
 1387| and would have been refused on a clean tree (the carrier's 2026-08-31 note predicted the shape).  Two-part clearance before the commit
 1388| (`regress/artifacts/jazzvecdeassert/landing_20261102/PREP.out`): build/ (reference est), build-asan/ and WSL `/tmp/gxsec-build` (reference SEC) each cmp CLEAN with
 1389| the binary newer than the source; est/: source tree, part 2 N/A.  Gates 1 and 4 run end to end on the applied tree before the commit
 1390| (`regress/artifacts/jazzvecdeassert/landing_20261102/GATE14_RUN_wsl.txt`): gate 1 rebuilt build/ and /tmp/gxsec-build and published the arc binary to the rig; gate 4's arc boot completed 13/13 steps and the `#578` block read `jazz_vector driver completed every command ok`, rows run 26, rows correct 26, all 26 names present -- REGRESS_PASS, GATE_COVERAGE=2/16 (SUBSET: 1 4); the first attempt, launched from git-bash, SKIPPED both gates on `/mnt/c` paths and is kept beside it as `regress/artifacts/jazzvecdeassert/landing_20261102/GATE14_RUN.txt` (`REGRESS_PASS_WITH_GAPS` is what a battery launched from the wrong shell looks like).
 1391| 
 1392| **Records.**  `OUTSTANDING_BUGS.md`: OB-22's six carriers (:2037, :2509, :2605, :2869, :2926, :2965 at 50f9c601) marked fixed in place,
 1393| the :2965 remedy wording corrected; a dated tail section with the fix, three filings (`jazziodfltflood`, `ns16550out2hold`,
 1394| `jazzvecrowsowed`) and the `jazzlbmask` notes.  Ledger: row `jazzvecdeassert` OPENED and set `held` in one commit (witness
 1395| `probe:regress/artifacts/jazzvecdeassert/witness_20261102/jazz_vector_witness.py`; seat entries for pass 1, pass 2 and F2 naming their
 1396| dirs; Astra's pass-2/F2 marker and the Fable-as-adjudicator question in its hold question), the three filed rows opened; `matrix.html`
 1397| and `fable_queue.md` re-rendered from the ledger.  Process notes honoured from `#576`/`#577`: one sibling file per prediction set, never
 1398| rewritten; the as-run instrument preserved at run time; `cp -p` for artifact copies; a 30-minute table per repair rather than a repaired
 1399| row inserted into a table that already ran.
 1400| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_578: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC578: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
