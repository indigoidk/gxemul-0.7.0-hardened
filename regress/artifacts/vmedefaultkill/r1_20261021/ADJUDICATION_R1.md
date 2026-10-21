# #568 vmedefaultkill -- the REPAIR-DIFF PASS (R1): adjudication (main loop; roster complete 02:29, Argon 03:04)

Roster (owner 2026-10-20: GLM 5.3 + grok + Astra + Fable; Argon as a second packet-fed lens):
| seat | transport | verdict | file |
|---|---|---|---|
| Fable 5.1 | Agent, file-reading | CLOSE -- zero, with a denominator | fable5_r1.md (02:02) |
| GPT-6 Astra (ultra) | codex, file-reading | CLOSE -- zero; two attributions + records | out/codex_vmer1.txt |
| GLM 5.3 | Ollama, packet-fed (COMPACT) | REPAIR AGAIN -- records-only repair + one "conditional escape" | out/glm_r1.txt |
| Grok 4.7 xhigh | grok CLI, file-reading | CLOSE -- zero, with a denominator; records | out/grok_r1.txt |
| Grok 4.7 xhigh, adversarial job | grok CLI, Q2 only | CLOSE -- no one-edit mutant passes; one credit false | out/grokadv_r1.txt |
| Argon | gemini_webapi, packet-fed, one bundle | first send SEAT FAILURE (transport, 02:46:54; retry stopped 02:51); RE-SENT extended-off: REPAIR AGAIN (02:58) -- adjudicated below, no floor breach; oracle audit 7 HOLDS (03:04) | gweb/jobs_20261021_argonpack23/vmer1, jobs_20261021_argonpack24/vmer1o |

**Argon's failure, measured, and why the re-send changes one setting.**  Control passed 02:20:51 (7.2% of the meter);
the packet went at 02:21:51 and attempt 1 died at 02:46:54 -- "The connection to Gemini was lost while generating the
response, and recovery timed out" -- exactly pass 2's failure (three times, 25 min each, two bundles 118 KB), so bundle
size is not the cause (this job was ONE 42 KB bundle).  Its automatic retry was STOPPED at 02:51 at the other session's
request (its armed run waits on any python.exe of mine).  `_scratchpad/gweb/GXGW_LOG.txt` shows the variable: every
"connection lost" failure ran with `extended True` (10-14 23:08 and 23:36, 10-21 00:08/01:03/01:29, 02:46); the 10-14
job's retry with `extended False` returned in 266 s, and ~60 jobs from 10-15 00:01 to 10-18 06:08 ran `extended False`
and ALL returned (33-1808 s).  The default went back to True on 10-20 (two returns at 447 s and 544 s, then these
deaths).  So the re-send runs `GXAR_EXTENDED=0` -- against the owner's 2026-10-14 "thinking level High", which the
sender's own default encodes -- because at High this job type never answers; the deviation is recorded, not hidden, and
the seat label says "extended False".

**Argon RE-SENT 02:5x with extended thinking off, and both jobs answered** (one sender; meter 86.2% -> 49.9%: the repair
job's packet cost 33.3%).  `vmer1` (the floor attack, 02:58): VERDICT REPAIR AGAIN, "8 ATTACKS 6 BROKEN 1 HOLDS 1
UNSETTLED".  `vmer1o` (the probe's oracle audit, 03:04, 310 s): CANNOT SETTLE, "8 ATTACKS 0 BROKEN 7 HOLDS 1 UNSETTLED" --
every row's oracle holds against shapes (a)-(e); the one UNSETTLED is the helper code its bundle deliberately left out
(VSIG, GUARD, HANDLER, the encoders), which the file-reading seats read whole.  It also re-derived `unasm`'s 1441.
Adjudicating vmer1's six BROKEN claims against the source and the measured tables:
* ESCAPE 1 -- the latch SET skipped for a zero-valued store (`if (writeflag != MEM_WRITE || idata != 0)` on the set):
  CONFIRMED, MEASURED 38/38 (table 2d M_ZEROSET, prediction first).  NEW: no other seat named it.  GRADED clause (e) --
  a store-data value exemption (the body tests no value of idata); `p2 zero wr` pins the announce's FORM, not the SET.
  The probe's disclosure named only "unsampled k", and 0 IS sampled -- so the NOT CLAIMED bullet now names this cell.
* ESCAPE 2 -- `!odata` on the direction test or the set: EQUIVALENT (odata is 0 on every write, every population-2 word
  is 0): the direction-test form is table 2c's M_DIRODATA (the fix's own binary); the set form MEASURED 38/38 (table 2d
  M_SETODATA).
* ESCAPE 3 -- `default:` narrowed to `relative_addr <= 0xffc` (0xffd..0xfff serviced): CONFIRMED 38/38 (table 2d
  M_DFLTFFC) -- the undriven-interior class already disclosed beside 0x91; the example added.  Fable's "any range
  narrowing" overclaimed (Grok said so too).
* BROKEN 4, 5, 6 are kill ATTRIBUTIONS, not escapes: the negated-latch operand swap reds `p2 ann wr` (not `p2 ann rd`);
  a set conditioned on `!idata` reds `p2 ann wr` pass 1 (52 lines); a latch field moved into `d->reg[]` reds `p2 wr census`
  (the set dirties the word a later load serves) -- each edit is killed by another row.  4 and 6 are the corrections
  Astra and Grok already made.
* UNSETTLED 7 (`if (!idata) return 0;` in default:) was MEASURED killed before the answer arrived: table 2c's M_DFLTIDZ,
  36/38 (`p1 fault wr` stores WVAL, non-zero).
* Its verdict line says the bit list "omits bits 6 and 9"; its own body recomputes 0x0a180802 and says the list HOLDS --
  the verdict line is the wrong half (the carrier's read-the-body rule).
**So Argon's REPAIR AGAIN does not survive adjudication as a floor breach**: its three survivors are clause (e) or
equivalent, each measured, and none is an operand swap of a predicate the fix depends on.  It found one cell no other seat
named (M_ZEROSET), which is what a second lens is for.
Opus 5.5 is the MEASURING seat (tables 2b, 2c, the clean clone) and was not fired as a review seat; agy, kimi, deepseek
and minimax deliberately not fired (owner roster).

## Measured during the pass (predictions written first)
* Table 2b (killtable2_20261021/table2b/, PRETABLE2B 02:12:02): M_IDATABIT1 `&& !(idata & 2)' on the direction test
  38/38 as predicted -- clause (e), the SAMPLED store-data slice; MEASURED for bit 1.
* Table 2c (table2c/, PRETABLE2C 02:24:51), GLM's three: M_DFLTIDNZ 29/38 and M_DFLTIDZ 36/38 as predicted (GLM's
  conditional escape REFUTED in both polarities); M_DIRODATA 38/38 and its binary is BYTE-IDENTICAL to the fix's --
  odata is assigned only on a read (dev_vme.c:78-79), so the conjunct is constant-true on the write path: an
  EQUIVALENT mutant, not a sampled slice (PRETABLE2C's reason was weaker than the truth; corrected in KILLTABLE2C.out).
* Gate-14 block alone on a CLEAN clone of HEAD 86114a90: HEAD FAIL 27 of 45, fix PASS 45 (vme/gate3/mini3_*.out).
* The always-clear store-data bits, COMPUTED (python over the five values): low word {1, 11, 19, 20, 25, 27}
  (complement of OR 0xf5e7f7fd = 0x0a180802); high word 22 clear (set: 34 38 40 41 44 45 49 53 56 60); 28 of 64.
  GLM's high-set list wrongly included 46, hence its "27".

## Dispositions, finding by finding
FLOOR (the closing question):
* THE CHAIN CLOSES: zero floor breaches SURVIVING ADJUDICATION on the full named roster -- Fable, Astra, Grok and the
  adversarial Grok job CLOSE, each with its own denominator; GLM's one floor-relevant item refuted by measurement
  (table 2c).  Validity: the repair diffs were delivered whole (fix 4 hunks, probe 13; the COMPACT packet carried the
  row contract instead of the probe diff); the roster is complete; Argon (a second packet-fed lens, not a roster seat)
  is recorded below whatever it returns.  Astra's denominator adds direct selector substitutions of
  `switch (relative_addr)'; Grok's adds the {0,1} weakenings of the direction test (`if (writeflag)',
  `writeflag != 0' -- equivalents on the values this handler is called with) -- no survivor in either.
* Grok: two latch-index edits pass and are EQUIVALENT, not breaches -- `1ULL' -> `2ULL' and `(relative_addr >> 2) ^ 1'
  (each applied to the test AND the set: a private bit per register survives); GLM named the first and `|=' -> `^='.
  Recorded in the contract as derived equivalents, not built.  `default:''s refusal narrowed to exempt an undriven
  interior (`relative_addr != 0x91') or an unrowed lane-0 cell passes 38/38 -- inside the contract's population-1
  exclusion, clause (e); now named there.  Grok also notes the first seat's "any relative_addr test" row overstates the
  mechanism (`relative_addr != 0' does not split the 26) while its kill (`p2 ann rd') holds.
* GLM "conditional escape" (`default:' `return 0;' -> `if (idata != 0) return 0;'): REFUTED -- table 2c, both
  polarities killed; GLM's packet did not carry the population-1 store values (WVAL, NARROW, DHI:DLO, all non-zero) or
  the read-side idata = 0 (dev_vme.c:73-76).
* GLM latch-state credit "order-dependent": SETTLED BY READING -- the set (dev_vme.c:193) precedes the direction test
  (:194), so Fable's `p2 ann rd' credit is right.
* Astra: two of Fable's kill attributions are WRONG, no survivor follows -- M_LATCHRDSET reds `p2 ann wr' + `p2 nw wr 2'
  (KILLTABLE2:27), not `p2 ann wr 2' (pass 1's read after each write latches it); a latch set redirected into d->reg[]
  does not red `p2 rd census' (odata is preloaded at :78-79 before the set).  ACCEPTED as corrections to fable5_r1.md's
  table; the census is unchanged.
* Astra: "34 legs" are measurement counts, not 34 members of an exhaustive enumeration.  ACCEPTED (wording).
RECORDS (comment/records only; owe no pass of their own):
* SAMPLED disclosure must name the untested slice (Fable, Astra, GLM): ACCEPTED -- the probe's NOT CLAIMED store-data
  bullet names the five values, the 28-bit clear set, bit 1 MEASURED (2b) vs the rest DERIVED, `idata == k' for unsampled
  k, the latch-test twin derived; `default:''s idata refusal is NOT in the slice (2c killed both polarities); the odata
  twin is EQUIVALENT (2c).  GLM's named equivalents (`1ULL' -> `2ULL', `|=' -> `^=') added as derived, not built.
* CONTROL definition self-contradiction (Astra): ACCEPTED -- reworded around the prerequisite role.
* Section 3d's "a reorder of POP2 could move the kill" (Astra): ACCEPTED -- under a bit-3 collision one of SLAVELMOD2/MISC
  is silenced in ANY order (25 lines); a reorder changes which, not the kill.  Reworded.
* Fable's "both UB alternatives on different builds" (Astra): unsupported -- only the fold-to-0 shape was built.
  Recorded against fable5_r1.md; the shipped text already says the masked shape was not built.
* cpw_block568.txt:25 "byte-identical" (Fable; Astra: TWO hunks, now more): ACCEPTED -- "docstring/comment text only,
  AST-identical (docstring removed)".  MANIFEST CLASS for the frozen copies: Fable and Grok said WITNESS (and Astra let
  it "stand"), reading the #471 comment as defining WITNESS -- REJECTED ON THE HISTORY, not the vote: `git blame' puts
  that comment and `CLASS_RESEARCH = "research"' in the same commit, #471's 0a7c4687 (2026-08-27), while
  `CLASS_WITNESS' dates from 85bc6ab4 (2026-08-21).  The comment defines RESEARCH ("the instruments preserved beside a
  kill table"); precedent is mixed (#539/#545 WITNESS, #530 TOOL).  RESEARCH kept, the reason written into the block.
* SCORE_CLAIMS_MANIFEST still 36; MANIFEST block not in the tree (Fable, Astra): OWED at commit, as planned.
* CHANGELOG draft (Fable Q3 4/5/7; Astra): ACCEPTED -- Opus 5.5 MEASURED and was not fired as a review seat; "every
  MUTANT leg's prediction written first" (the reference runs and objdump objects preceded PRETABLE2, its section 0 says
  so); attach consequence "would end the emulator at its first MASTERCTL read, witnessed at that site" (source-derived,
  not a boot); rev 2's full gate ran on build/gxemul with the peer's uncommitted PCC2/LCA/SH4/Alpha edits.
* KILLTABLE2_VS_PRETABLE2.out:9 "first build log 01:16:55" (Fable, Astra): ACCEPTED -- 01:16:55 is configure (RUNLOG:2),
  the first BUILD 01:17:37 (RUNLOG:3); a correction APPENDED to that file, the line kept and quoted.
* PRETABLE2.out:72 "the 20 population rows die on HEAD" (Astra): its prose omits the four rev-3 rows that :236 adds
  (24 red measured, 24 predicted in PRETABLE2_predictions.json -- MATCH).  PRETABLE2.out is NOT edited: its mtime is the
  order proof.  Recorded here and in the CHANGELOG.
* "comment-only" / "object code otherwise identical" in vme/f2/owed.md:2-3 and Fable's F2 (Fable, Astra): SUPERSEDED by
  OBJDUMP_fix568_vs_fix568b.txt; a supersession header is added when f2/ is copied to the artifacts.
* GLM: Fable's verdict-line exception (D5 not in the shipped docstring) is STALE -- true at 02:02, discharged by the
  section-3d correction applied ~02:08.  No action.
FILED (not this round):
* `free quiet' has zero measured kills (Fable): FILE with `vbr rt' and `t1count inc' (dependent-only kills), naming the
  three absent legs: a cased arm's debug() -> fatal() promotion; a VBR write-path break; a T1COUNT write-path break.

---

*** CORRECTION, appended 2026-10-21 after GPT-6 Astra's records confirmation: the Argon paragraph above says the
extended-on runs on 10-20 were "two returns at 447 s and 544 s, then these deaths" and that "at High this job type never
answers".  Both overstate it.  #568's own PASS 1 Argon packet ran with extended thinking ON and returned, in 383 s
(_scratchpad/gweb/GXGW_LOG.txt, `JOB vmep1 packet: reply 22043 chars in 383 s (extended True ...)`).  What is measured:
#568's pass-2 packet (three attempts) and the repair pass's first packet, both extended-on, died at ~25 minutes with
"connection lost while generating"; every extended-off job since 2026-10-15 returned.  The re-send with extended thinking
off is a disclosed fallback for those failures, not evidence that extended thinking always fails. ***
