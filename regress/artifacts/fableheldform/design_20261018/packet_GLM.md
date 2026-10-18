**Your token: `GLM_FHF_P1_20261018`** -- open your answer with it.

You cannot read files; every fact you need is inlined after the brief.  Where a question needs a fact this packet does not hold, say "not checkable from the packet".

# `fableheldform` -- how should sixteen walled Fable entries be recorded, when nine of them sit on rows already CLOSED?  A design question about records (pass 1)

**Please do not simply ratify.**  A recent panel had seven of nine seats confirm a premise its brief stated wrongly.
Check the premises, not just the derivations.  The tree under review is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` (ignore
any other `src/` under the project root).  READ-ONLY.

## The defect (filed by `#566`, 2026-10-18, as row `fableheldform`, MED)

The owner's 2026-10-17 directive: *"do not block a ruling or a commit on Fable: Astra + Grok + GLM 5.3 rule; Fable's stage
is recorded as a HELD marker carrying its question (`[HELD AWAITING SEAT: fable5]` plus a `hold_question`) and is answered
when the seat comes back.  Still try Fable once per pass (a wall is a moment, not a state) and record a wall as a SEAT
FAILURE, never as agreement."*

Since then sixteen `fable5` ledger entries on ten rows recorded a wall or a deliberate non-firing in PROSE ("NOT FIRED",
"SEAT FAILURE", "HTTP 429") with NO stage token.  `tools/pipeline/stage_tokens.py` `is_answer()` returns True for ANY
entry without a token, so the checkers count each of these as Fable having ANSWERED -- the agreement the directive says a
wall must never be.  The census, derived from the ledger at 16:1x today, is `CENSUS.txt` (inlined below for the
packet-fed seat): 16 entries; NINE of the ten rows are CLOSED (`sgirekills`, `sgirandomcolour`, `mapledmaaddr`,
`xscaleinten`, `ppcrldimimask`, `ppcrlwimiwidth`, `ppcgateimageskip`, `cxlaunchquotation`, `dashokclass`), one is in work
(`wiringcliff`).  All nine closed rows already carry a `hold_question` -- for their REGRESS stage (regress is FABLE-ONLY,
batched), not for the walled review.

## The rule the fix collides with

`tools/pipeline/check_stage_panels.py` (precommit section H; `H_excerpt.txt`): `STAGES = ("assess", "research",
"review")`; for each, a LIVE hold (a `[HELD AWAITING SEAT: X]` marker with no later answer from X in the same phase) on a
row whose state is `closed` is a violation, CLOSED-WHILE-HELD: *"a round may not close while a stage awaits a seat"*.
The `regress` phase is not in `STAGES`, so a REGRESS hold does not block a close.

**Measured today, one hour ago, on `ip30abortkill`'s closure:** my draft recorded Fable's walled closure review as a
`[NOT A SEAT ANSWER]` entry and closed the row; GPT-6 Astra's confirm overturned it -- *"substitutes a non-answer record for
the review hold ... the draft reports review `ok 9/9`, using historical answers, with no review hold.  Retain `state: in
work`, omit the closure object"*.  That row was committed `held` (state semantics: *"Something outstanding, waiting on a
NAMED party or event, and carrying the QUESTION it is held for"*).  If that ruling is right, the nine closures above got
past section H only because of this very defect.

## Options for the nine closed rows (the set is not claimed complete -- name a member it lacks)

* **A. REOPEN.**  Give each of the sixteen entries the HELD token (keeping its prose and receipt), extend each row's
  `hold_question` with the walled stage's question, and move the nine rows `closed` -> `held`.  Their closure objects:
  kept as the drafted closure, or moved into the state note?  The dashboard then shows nine rows held for Fable.
* **B. KEEP CLOSED, NON-ANSWER TOKEN.**  Mark each entry `[NOT A SEAT ANSWER]` -- not an answer, not a hold.  The form
  Astra overturned this afternoon: the review stage then reads complete on older answers and the gap is invisible.
* **C. KEEP CLOSED, CARRIED ON REGRESS.**  B, plus the walled review's question carried on the row's REGRESS hold.  The form
  I chose for `ip30abortkill` before Astra's confirm.
* **D. LEAVE AS IS.**  The defect.

## Questions (answer each; premises are stated as questions on purpose)

1. **Which option, and why?**  Is A what the owner's directive and section H jointly require, or is there a reading of
   "do not block a ruling or a commit on Fable" under which a CLOSE (a state change) is not something Fable may hold?
2. **`cxlaunchquotation` and `dashokclass`**: Fable ANSWERED their earlier passes (V3-V6 / V2-V6, same review stage) and
   walled only on the last (V7).  Is that review stage held, or discharged by the earlier answers?  (The repair-chain rule
   says the chain closes on the first VALID pass that finds zero breaches, and a valid pass has its roster complete or its
   misses NAMED.)  Same question for `sgirekills`, whose research AND review walls are `#564`'s passes 1-3.
3. **The conversion's form**: prefix the token to the existing entry (one entry, provenance kept), or add a new marker
   beside a re-tagged old one?  Note `stage_tokens.is_held()` keys on the literal and `live_holds()` discharges a marker
   only by a LATER answer from that seat in the same phase.
4. **Is this an OWNER decision** (reopening nine closed rows) rather than a seats' one?  If so, what is the single
   question to put to the owner?
5. **Which of my premises is wrong?**  In particular: is the census complete (16 / 10)?  Does any of the nine rows have a
   later Fable answer that already discharges its stage?

Answer format: open with your token, then ONE line `VERDICT: <option> -- <one line>`, then `FLAG:` lines for any premise
you find false (with `file:line` or census evidence), then short answers to 1-5.

## INLINED: CENSUS.txt
```
fableheldform census -- the WORKING-TREE ledger at HEAD 8faf4a16 plus uncommitted lines, derived 2026-10-18 16:14 by the main loop.
Selection: fable5 entries dated 2026-10-17 or later that stage_tokens.is_answer() counts as ANSWERS and that are not
held, whose first 400 characters say NOT FIRED / SEAT FAILURE / walled / not tried / HTTP 429 / Fable limit.
Each line: row (state) | entry index | phase | date | first 160 characters of the note.

wiringcliff (in work; hold_question SET)
   [28] design 2026-10-18 | #565 PASS 1 (the design brief): NOT FIRED -- Fable adjudication is held by the owner's 2026-10-17 directive (walled again, HTTP 429, at 04:57 on 2026-10-18).
   [32] review 2026-10-18 | #565 PASS 2 and the F2 shared-findings pass: NOT FIRED -- Fable adjudication is held by the owner's 2026-10-17 directive (walled again, HTTP 429, at 04:57 on 20
      other fable5 [1] design 2026-09-09 answer=True held=False | ADJUDICATED BY THE MAIN LOOP RUNNING AS FABLE 5.1 (owner directive 2026-09-09: "proceed with fable for any adj
      other fable5 [23] review 2026-09-18 answer=True held=False | #536/#537 PASS 2 (panel_20260918_190341) + §F2 (panel_20260918_193405), one brief for both rounds.  #536 (this
      other fable5 [41] design 2026-10-18 answer=False held=True | wiringcliff [HELD AWAITING SEAT: fable5] #566 PASS 1 (the design brief): Fable 5.1 was NOT TRIED -- an omissio
      other fable5 [48] review 2026-10-18 answer=False held=True | wiringcliff [HELD AWAITING SEAT: fable5] #566 PASS 2 and F2: not tried on pass 2 (the same omission); TRIED on
sgirekills (closed; hold_question SET)
   [45] research 2026-10-17 | #564 PASS 1: SEAT FAILURE -- Fable 5.1 walled on a usage limit (HTTP 429) before answering; held by owner ruling 2026-10-17.
   [49] review 2026-10-17 | #564 PASS 2: SEAT FAILURE -- Fable 5.1, HTTP 429 (req_011Cg8sdDCAa8pN7M1hJcL8e).
   [56] review 2026-10-18 | #564 PASS 3: SEAT FAILURE -- Fable 5.1, HTTP 429 (req_011Cg9EoXxm9pFQX8N6At43T), its third wall this round; the re-fire-once rule discharged.
      other fable5 [28] review 2026-09-08 answer=True held=False | PASS 2 ON THE DIFF.  preserved for the 2026-09-09 adjudication.
      other fable5 [38] review 2026-09-08 answer=True held=False | PASS 4, the closing pass.  preserved for the 2026-09-09 adjudication.
sgirandomcolour (closed; hold_question SET)
   [28] review 2026-10-18 | sgirandomcolour CLOSURE-RECORDS review, pass 1: SEAT FAILURE -- Fable 5.1, HTTP 429 (req_011Cg9W6JNR2wZurX4nyBy3Y); held by the owner's 2026-10-17 directive.
   [32] review 2026-10-18 | sgirandomcolour CLOSURE-RECORDS review, pass 2 (the delta): DELIBERATELY NOT FIRED -- walled (HTTP 429) on pass 1 minutes earlier, and Fable adjudication is hel
      other fable5 [22] review 2026-09-10 answer=True held=False | ADJUDICATED BY THE MAIN LOOP RUNNING AS FABLE 5.1 (owner directive), on 6 of 7 scriptable transports (kimi via
mapledmaaddr (closed; hold_question SET)
   [50] review 2026-10-18 | mapledmaaddr CLOSURE check: NOT FIRED -- Fable adjudication is held by the owner's 2026-10-17 directive (walled, HTTP 429, at 04:57 the same day).  [2026-10-18,
      other fable5 [45] review 2026-09-12 answer=True held=False | Fable 5.1, fired LAST as a subagent pinned to model fable, READ-ONLY (gate 10 running); opened by naming itsel
      other fable5 [46] review 2026-09-12 answer=True held=False | Fable 5.1, fired LAST, READ-ONLY (gate 10 concurrent); opened by naming itself claude-fable-5-1 (verified).  C
xscaleinten (closed; hold_question SET)
   [21] review 2026-10-18 | xscaleinten CLOSURE check: NOT FIRED -- Fable adjudication is held by the owner's 2026-10-17 directive (walled, HTTP 429, at 04:57 the same day).  [2026-10-18, 
      other fable5 [17] review 2026-09-12 answer=True held=False | Fable 5.1, fired LAST as a subagent pinned to model fable; opened by naming itself claude-fable-5-1 (verified)
ppcrldimimask (closed; hold_question SET)
   [21] review 2026-10-18 | #527 CLOSURE check: NOT FIRED -- Fable adjudication is held by the owner's 2026-10-17 directive (walled again, HTTP 429, at 04:57 on 2026-10-18).
      other fable5 [17] review 2026-09-12 answer=True held=False | Fable 5.1, fired LAST as a subagent pinned to model fable; opened by naming itself claude-fable-5-1 (verified)
ppcrlwimiwidth (closed; hold_question SET)
   [21] review 2026-10-18 | #527 CLOSURE check: NOT FIRED -- Fable adjudication is held by the owner's 2026-10-17 directive (walled again, HTTP 429, at 04:57 on 2026-10-18).
      other fable5 [17] review 2026-09-12 answer=True held=False | Fable 5.1, fired LAST as a subagent pinned to model fable; opened by naming itself claude-fable-5-1 (verified)
ppcgateimageskip (closed; hold_question SET)
   [3] review 2026-10-18 | #527 CLOSURE check: NOT FIRED -- Fable adjudication is held by the owner's 2026-10-17 directive (walled again, HTTP 429, at 04:57 on 2026-10-18).
cxlaunchquotation (closed; hold_question SET)
   [12] review 2026-10-17 | V3 PASS: SEAT FAILURE -- the Fable 5.1 agent STALLED again (stream watchdog, 600 s), after reading the launcher and before writing an answer; most likely the wh
   [26] review 2026-10-17 | V6 PASS: SEAT FAILURE -- Fable 5.1 walled on a usage limit ("You've reached your Fable limit", HTTP 429) at 07:17, after writing a stub whose only content is tw
   [30] review 2026-10-17 | V7 PASS: SEAT FAILURE -- Fable 5.1 walled on a usage limit (HTTP 429, "You've reached your Fable limit") before writing anything, its fourth wall that day; its 
      other fable5 [4] review 2026-10-16 answer=True held=False | PASS 2: SHIP WITH CHANGES (2) -- Fable 5.1, in two parts: its first run FELL BACK to claude-opus-4-8 after two
      other fable5 [8] review 2026-10-16 answer=True held=False | ADJUDICATION PASS (v2): SEAT FAILURE -- the Fable 5.1 agent STALLED (stream watchdog, no progress for 600 s) a
      other fable5 [18] review 2026-10-17 answer=True held=False | V4 PASS: SHIP WITH CHANGES (7) -- Fable 5.1 (claude-fable-5-1 throughout, no fallback): the v4 CONTRACT's 'eve
      other fable5 [22] review 2026-10-17 answer=True held=False | V5 PASS: SHIP WITH CHANGES (5) -- Fable 5.1 (claude-fable-5-1 throughout, agent_models.py), measuring in a mir
dashokclass (closed; hold_question SET)
   [29] review 2026-10-17 | V7 PASS: SEAT FAILURE -- Fable 5.1 walled on a usage limit (HTTP 429, "You've reached your Fable limit") at 09:13 before writing anything, its third wall that m
      other fable5 [2] review 2026-10-16 answer=True held=False | PASS 2 (v1): SHIP WITH CHANGES (7) -- Fable 5.1 (agent_models.py: clean claude-fable-5-1): the refill measured
      other fable5 [6] review 2026-10-16 answer=True held=False | ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- Fable 5.1 (clean claude-fable-5-1), measuring in a mirror: bo
      other fable5 [15] review 2026-10-17 answer=True held=False | V3 PASS: SHIP WITH CHANGES (3) -- Fable 5.1 (clean claude-fable-5-1), measuring in a mirror: both v3 receipts 
      other fable5 [17] review 2026-10-17 answer=True held=False | V4 PASS: SHIP WITH CHANGES (18) -- Fable 5.1 (claude-fable-5-1 throughout), measuring in a mirror (its receipt
      other fable5 [21] review 2026-10-17 answer=True held=False | V5 PASS: SHIP WITH CHANGES (10) -- Fable 5.1 (claude-fable-5-1 throughout), measuring in a mirror: 96/96 and t
      other fable5 [25] review 2026-10-17 answer=True held=False | V6 PASS: SHIP WITH CHANGES (8) -- Fable 5.1 (claude-fable-5-1 wrote the answer; the seat refused twice mid-run

TOTAL: 16 entries on 10 rows
```

## INLINED: check_stage_panels.py (section H), the stage loop
```python
186:             d = by_stage.setdefault(ent.get("phase"), {})
187:             d.setdefault("seats", set()).add(ent.get("seat"))
188:             d["newest"] = max(d.get("newest", ""), ent.get("date", ""))
189: 
190:         for stage in STAGES:
191:             info = by_stage.get(stage)
192:             if not info:
193:                 continue                       # stage never ran; not this check's business
194:             if "seats" not in info:
195:                 #  #534 F2 pass (codex, Opus): a stage whose only entry is a LIVE hold was skipped
196:                 #  here, before any hold test, so a CLOSED row could carry one with H green.
197:                 live0 = st.live_holds(info.get("_all", []))
198:                 if live0 and row.get("state") == "closed":
199:                     violations.append((row["id"], "CLOSED-WHILE-HELD", stage, 0,
200:                                        ["a round may not close while a stage awaits a seat"]))
201:                 elif live0:
202:                     held.append((row["id"], stage, 0, ", ".join(live0), "",
203:                                  (row.get("hold_question") or "").strip()))
204:                 continue
205:             got, newest = info["seats"], info.get("newest", "")
206:             #  #534 (heldmasked, an L3 of this round per its pass 2): a LIVE hold -- a named seat not
207:             #  answered in this stage at a strictly later date -- beats a full count.  Before this,
208:             #  the count test ran first, so an owner-decision hold over nine misdirected answers
209:             #  reported `ok 9/9` and the row could be CLOSED with H, I and the wall all green
210:             #  (Opus, measured).  A DISCHARGED marker does not hold a full stage.
211:             live = st.live_holds(info.get("_all", []))
212:             if len(got) >= n_seats and not live:
213:                 complete += 1
214:                 if listing:
215:                     print("  ok    %-14s %-9s %d/%d" % (row["id"], stage, len(got), n_seats))
216:                 continue
217:             #  HELD is checked BEFORE the one-seat "filed" shortcut, so a stage that is
218:             #  genuinely waiting on a named seat is reported as waiting even if only one
219:             #  other seat has answered so far.
220:             #  ... and ONLY a live hold holds a SHORT stage either.  A marker every named seat has
221:             #  since answered is history: treating it as a hold printed "awaiting: fable5" over
222:             #  pcc2c040kill's 8/9 review whose real gap is agy (codex + Opus, #534 F2 pass).
223:             if live:
224:                 if row.get("state") == "closed":
225:                     violations.append((row["id"], "CLOSED-WHILE-HELD", stage, len(got),
226:                                        ["a round may not close while a stage awaits a seat"]))
227:                 else:
228:                     #  Every marker, de-duplicated, order preserved -- so two holds report
229:                     #  two seats and the operator sees the whole debt.
230:                     names = list(live)
231:                     held.append((row["id"], stage, len(got), ", ".join(names),
232:                                      newest, (row.get("hold_question") or "").strip()))
```

## INLINED: stage_tokens.py, is_held / is_answer / live_holds
```python
     1	def is_held(e):
     2	    return HELD in _note(e)
     3	
     4	
     5	def exempts_stage(e):
     6	    n = _note(e)
     7	    #  HELD and NOTSEAT both dominate: a hold is a promise and NOTSEAT says "this entry only" -- an
     8	    #  entry carrying either can never exempt the stage, whatever else it quotes (minimax, #534 pass 2:
     9	    #  the docstring promised this of NOTSEAT and the code did not deliver it).
    10	    return (not is_held(e)) and NOTSEAT not in n and any(t in n for t in STAGE_EXEMPT)
    11	
    12	
    13	def is_answer(e):
    14	    n = _note(e)
    15	    if HELD in n or NOTSEAT in n or ANNOTATION in n or NOPANEL in n:
    16	        return False
    17	    return True          # RE_READ entries ARE answers; so is every untokened entry
    18	
    19	def live_holds(entries):
    20	    """Seats still awaited in one (row, phase): named by a HELD entry and NOT answered by that seat
    21	    in this stage at a STRICTLY LATER date -- the carrier's discharge rule, applied here so every
    22	    reader agrees on it.  (#534 pass 2, codex + Opus: two of the three stages that showed a full count
    23	    over a hold were DISCHARGED holds, and one was live; a reader must tell them apart.)"""
    24	    out = []
    25	    for h in entries:
    26	        if not is_held(h):
    27	            continue
    28	        hd = h.get("date") or ""
    29	        named = held_seats(h)
    30	        if not named:
    31	            #  a hold in no parseable shape can never be discharged by an answer -- it holds until
    32	            #  someone writes it properly; a malformed marker must not read as "nothing owed"
    33	            #  (codex, #534 F2 pass: `[HELD AWAITING SEAT: glm,]` let a closed row pass H and I)
    34	            if MALFORMED not in out:
    35	                out.append(MALFORMED)
    36	            continue
    37	        for seat in named:
    38	            done = any((e.get("seat") or "").lower() == seat and is_answer(e)
    39	                       and (e.get("date") or "") > hd for e in entries)
    40	            if not done and seat not in out:
    41	                out.append(seat)
    42	    return out
```
