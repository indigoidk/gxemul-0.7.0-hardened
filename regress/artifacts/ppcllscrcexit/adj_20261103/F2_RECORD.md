# #579 `ppcllscrcexit` -- the F2 (adjudication) pass: what the roster said, what was CHECKED, and what waits for Fable

Recorded 2026-11-04 01:2x by the main loop (Opus 5.5).  **NO RULING IS MADE HERE.**  The owner holds Fable (2026-11-04 ~00:4x "hold
fable"); the F2 packet's dispositions were the main loop's PROPOSALS, and the final ruling on every line below is Fable's.  Cheap factual
claims were CHECKED (a grep or a count) and are recorded as facts.

**Packet:** `_scratchpad/panel_20261104_010140_f2_ppcllscrcexit/FULL.md` (48,584 bytes; the diff with 3 hunks, the handler at its
working-tree lines, the decoder KEY/ARM lines, Book I :451-460, findings F1-F22 and D1-D3 with PROPOSED dispositions, kill tables 2-4,
the pre-fix witness, the 83-row probe).  Fired 01:02.

## Seats (owner roster 2026-11-04 00:5x / 01:0x) -- 5 of 5 answered, each checked by CONTENT

| seat | file (panel dir unless noted) | verdict | liveness |
|---|---|---|---|
| Opus 5.5 Agent seat (READ-ONLY) | `opus5.txt` (extracted verbatim from the subagent transcript) | UPHOLD-WITH-CHANGES | token + CHECKPOINT.md's first line as it stood at 01:02; `agent_models.py`: clean, opus-5-5 x99 turns, one REFUSAL at 07:13:30Z by claude-opus-5-5, which the seat disclosed (it did not regenerate the material and proposed no test variants) |
| Grok 4.7 xhigh (plan mode) | `grok.txt` | UPHOLD-WITH-CHANGES | file-reading: cites working-tree lines 2276-2383, 4652, 4904-4910 |
| GPT-6 Astra (read-only) | `codex_ppcllscrcexit_f2.txt` | UPHOLD-WITH-CHANGES | file-reading (links into GXEMUL-SEC/src and regress) |
| GPT-6 Astra, second angle (F2/F3 fact check, `CODEX_PTR2.md`) | `codex_ppcllscrcexit_f2b.txt` | F2-WORDING WRONG; F3-WORDING RIGHT | quotes memory_rw.c:603-643, core/memory.c:645-651, cpu_ppc.c:318-339 |
| GLM 5.3 (packet-fed) | `ollama_glm.txt` | UPHOLD-WITH-CHANGES | names every premise it could not settle from the packet |
| Gemini 4 Argon (packet-fed, web2api proxy) | `_scratchpad/gweb/jobs_20261103_adj/ppcllscrcexit_f2/gemini_web.out` | UPHOLD-WITH-CHANGES (25 HOLDS, 0 BROKEN) | prompt token P-GWEBF2PPCLL-d7d1 returned; banked 01:03:22 |

NOT FIRED by the owner's roster: agy, deepseek, minimax, kimi.  Fable: HELD (not a seat failure, not agreement).

**Weight note (a fact about the answers, not a ruling):** Argon upheld all 25 items, including F14's proposed wording, which four other
seats refuted on reading; its answer adds no claim the others lack.  Count the arguments, not the seats.

## CHECKED facts (each a grep or a count, run 01:2x)

1. **F13 was NOT applied.**  `FABLE_ADJ.md` contains `2354` 0 times and `2355` 0 times (`2346`, the HEAD citation, twice).  The F2
   packet's "APPLIED in FABLE_ADJ.md" (FULL.md:299) was a WRONG RECORD of the main loop's, as was, by the main loop's account (no copy survives), an earlier checkpoint line "FABLE_ADJ.md :2355" -- of the main loop's.  Grok
   found it.
2. **F22's count:** the M3-M7 red union in table 4 (`SCORES4.txt`) is 40 names, so the rows that CANNOT vary under those variants number
   **43**, not 40 (Grok and Astra, independently).  The packet's "the 40 rows that cannot vary" named the wrong set.
3. **"The #216 returns below" is plural for one return:** in X(llsc) (2276-2383) the `#216` text sits at 2313 (load arm, ABOVE the store
   comment at 2333), 2340 (inside the #579 store comment) and 2368 (store arm, below).  Opus, Astra and GLM.
4. **F14:** the Book I v2.01 extract has no `31 532` or `31 596` entry (0 matches each) while XO 533 has two entries (lswx, :11615 and :12081) and XO 20 two (lwarx, :11453 and :12085); the third hit of the word-boundary pattern for `31 20`, :4311, is a form diagram, not an entry -- consistent with Opus's reading that XO 532/596 are unassigned in v2.01, so "other instructions" (the PROPOSED wording) is a new
   unverified claim.  Four seats rejected that wording.
5. **The docstring's "one or two" words per session and "differ in every byte"** are present (`ppc_llsc_probe.py`, 1 match each):
   `stw chain` and `stw twice` place three words, and the 4-byte and 8-byte patterns share their first four bytes (their VALUES differ).
   Astra.

## Open for Fable -- where the seats moved the PROPOSED dispositions (both sides in their own words where they differ)

* **F2 (the store comment's #216 sentence) -- the PROPOSED rewording is still false.**  Opus, Grok, Astra (both answers) and GLM: a
  failed PPC device access raises nothing (`memory_rw.c:603-643`, MIPS and M88K only), so "has already raised whatever exception or stop
  applies" repeats the overclaim.  Opus adds a fourth path no seat had named: a device handler that stops the CPU (`memory_rw.c:586-592`).
  Grok: the same "raised a DSI" sentence also stands in the older #216 comments at 2313-2315 and 2368-2370 (pre-existing text).
  Replacements offered: Astra-f2b "The #216 returns remain on failed memory accesses; a failure need not have raised a PPC exception or
  stopped the CPUs."; GLM "...whatever exception or stop, if any, applies has already been raised (a device failure raises none)";
  Astra-f2 "...preserving any exception or stop already produced by the memory path"; Opus a four-case enumeration (`opus5.txt`).
* **F3 -- the PROPOSED wording is true today.**  Astra-f2b: "F3's exact proposed replacement is right".  Opus: keep ", and none is
  required" (the actual warrant) and write "does not yet synchronise cpu->pc (ppcllscsrr0)" so the comment does not go false when that
  row lands.  Astra-f2: missing PC sync is a separate limitation, not the justification.
* **F10 (census) -- the PROPOSED repair would fail a correct build.**  Grok and Astra, independently: counting every placed word counts
  `neg`'s one word, so a correct run prints 35/36 against the gate's 35/35 pin; exclude the bogus-machine session.  Astra: today's
  denominator counts expected steps when the `unassemble` prompt exists, not parsed words.  Grok: the null medium then passes 14 rows.
* **F5/F7's "(d)" label.**  Grok: the rows are sibling parity with `stw ok` / `noresv`, not the pure-deletion (d) shape (M17/M21 do not
  re-introduce a kill).  Astra and GLM uphold them as L1.  (A rule question: which warrant carries these rows.)
* **F14 wording.**  Opus: "(20 and 84 with 512 added: unused, therefore illegal, extended opcodes in v2.01, Book I Appendix G; `goto bad`
  today)".  Grok: "unimplemented XOs".  Astra: "distinct XO values that miss this handler".  GLM: "encodings not routed to this handler,
  `goto bad` today".
* **F9's filing condition.**  Astra: "FILE only if in-bound" is backwards -- an in-bound obligation belongs in the round; an independent
  #216 defect is separate work.  GLM: leave it untriggered; no record may claim this round verified the #216 returns.
* **F11.**  Astra: one CR seed and TWO XER seeds; narrowing ONLY the RA mask is undetected (RA in {0, 6} is unchanged by `& 15`) -- narrow
  the coverage claim, no row automatically owed.
* **F15/F18 errata.**  Grok: `PRETABLE.out:38` also says the null medium fails every session -- an erratum beside that file too.
* **D2 (the store-pair label).**  Opus: DELETE (member 1) fits both pairs, with FAULT (member 5) unavailable on this CPU and not required.
  Grok: no member fits; record it in words.  Astra: CANNOT SETTLE (member 4 unsuitable; the menu text does not establish that none fits).
  GLM: words.
* **D3 (the 32-bit decoder and XO 84/214).**  Grok, Astra and Opus read no width test at 4904-4910.  GLM: REJECT "Grok settles it" -- the
  packet cannot settle it and the 32-bit leg runs XO 20/150 only; record "disclosed, unverified by this instrument".
* **New, outside the round (seats say so):** Opus -- the `0x87c0ffff` SRR1 mask drops MSR's upper half on 64-bit CPUs (UNSETTLED); the
  reservation compares effective addresses where Book II compares real ones.  Grok -- MODE32 `reg()` on a big-endian host reads the high
  half of `gpr[rt]` (pre-existing).  GLM -- the fixed rows' wants rest on four Book I/II citations the packet did not inline.
* **Docstring/comment wording (L4 candidates):** the "one or two" words, "differ in every byte", the absent-binary comment ("every row
  fails"), the load comment's "valid form" which rests on Book I :1110-1112 (Opus: cite it), F19's "ran to `quit'", F20's "every fixed
  row".

## What the round does next (no ruling needed)

Nothing is applied from this list.  The commit HOLDS for Fable's ruling on F1-F22, D1-D3 and the items above.  The Fable ruling packet is
this record plus the six answers; it is prepared and unsent while the owner holds Fable.

## MEASURED after the F2 pass (an Opus 5.5 measuring seat, 2026-11-04 02:1x; evidence `_scratchpad/opus_census579/`, answer.md there)

F10's census repair, run as COPIES of the probe (the repo file untouched, md5 dc191a6a0dc81cd0a47fc2853aa50703 before and after):

| probe | binary | RESULT | CONTROL | `unasm census` |
|---|---|---|---|---|
| repo (unmodified) | build/gxemul | 83/83 | OK | 35/35 ok |
| repo | /bin/true | 15/83 | FAIL | 0/0 ok |
| repo | a missing path | 1/83 | FAIL | 0/0 ok |
| repair B (count words PLACED, `neg` excluded) | build/gxemul | 83/83 | OK | 35/35 ok |
| repair B | /bin/true | 14/83 | FAIL | 0/35 FAIL |
| repair B | a missing path | 0/83 | FAIL | 0/35 FAIL |
| repair A (`neg` counted) | build/gxemul | 82/83 | FAIL | 35/36 FAIL (the probe reds itself) |

So the seats' prediction for A held exactly, and B fixes the row without changing any other row (the build outputs are identical, a
0-byte diff).  The gate's own scoring block, extracted verbatim and run on every output, passes the repo and B builds 97/97 and fails A
7/97; its literal pins never matched a null-medium output, old or new, so the old 0/0 was never a gate escape -- the defect was the
row's own verdict and the probe's prose.  Two record qualifiers it adds: "the null medium then passes 14 rows" is true of `/bin/true`
only (a missing binary passes 0); and under A the probe's own row wants 36/36, so it reds before the gate pin is consulted.  The repair
needs the docstring's "passes 15 rows" sentence changed in the same edit.  NOT APPLIED -- the F10 ruling is Fable's.

**Replicated** by a second, independent Opus 5.5 measuring seat (`_scratchpad/opus_20261104/m_579census/`, answer.md there; same-model replication, badge s): the same nine-run table -- A 35/36 FAIL with CONTROL=FAIL on the correct build, B 35/35 on it and 0/35 on both null media.  It adds one wrong record: the probe's comment at `ppc_llsc_probe.py:158` says an absent binary makes "every row fail", false as shipped (NOBIN 1/83) and true under either repair.
