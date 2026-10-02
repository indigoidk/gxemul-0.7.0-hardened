# REPAIR 14 — THE ADJUDICATION PASS.  The panel shares its findings.

*Standing owner directive, 2026-08-30: "always adjudicate findings and make sure the full panel
shares findings."  This is a THIRD pass, not a tidy-up.  Until this step existed, every seat answered
blind to the other eight and the main loop silently arbitrated — so a seat could not correct another
seat's error, and a disagreement was settled by whoever wrote it up.*

**You are being shown what the other seats said, with my disposition on each.  Your job is to attack
the dispositions, not to restate your own answer.**

**VERDICT LINE FIRST.**  If you cannot read files, say which items you cannot settle from this packet
rather than guessing.

---

## 0. THE ONE QUESTION I MOST NEED ANSWERED

**I accepted TWELVE of the thirteen findings below and rejected one.**  That ratio is itself
suspicious: *a round that accepted everything has either had a very good panel or has stopped
arguing, and only a seat can tell me which.*

> ### **WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?**

Be specific. "All reasonable" is not an answer I can act on.

---

## 1. WHAT WAS UNANIMOUS — flag it if you think the unanimity is wrong

**Not one seat ratified Part A of the proposed repair.**  Every seat that engaged with the MANDATE
upheld it: repair 14 owes CLASS CLOSURE IN ONE DIFF, and folding in the three already-built probes
as they stand is **measured insufficient** (`t4clear.py` kills the TIME cell at 3/5 and scores the
INTSTAT cell at 5/5).

**Unanimity on a brief-supplied fact is worth nothing** — that is this project's own rule. So: is
the mandate itself right, or did nine seats inherit it from my framing?

---

## 2. THE FINDINGS, NUMBERED, WITH MY DISPOSITION

Each is stated in the finding seat's own terms.  My disposition follows in **bold**.

**A1 (grok, glm, minimax, kimi-k3 — four seats, independently).  The floor denominator counts the
wrong population.**  `23 + 8 + 10 + 5 = 46`, against a product of 56 — ten cells in no category.
grok supplied the mechanism: *"23 is a count of ACCEPTS ENTRIES rowed post-latch by repair 13, not of
product cells... the CONTROL writes `0x0201` / `0x0001` / `0` / `0x0200` / `0x0100` are five entries
of ONE cell."*  **ACCEPTED.**  Owed: a per-cell disposition table, re-derived — not a re-count.

**A2 (glm, kimi-k3, independently; grok from the other side).  P4 is FALSE.**  The latch-CLEAR state
is not driven by session 40 alone.  **ACCEPTED AND SETTLED BY READING**: the gate-run session calls
`POST()` nowhere and drives INTMASK 4R at `:735`, before its first refusal at `:741`.

**A3 (agy).  P1's early-return claim is FALSE**, refuted by the probe's own DISCLOSED block
(`crime_width_probe.py:269-272`): `goto crime_declined` → `return 1` is EQUIVALENT on every channel,
measured 40/40.  **ACCEPTED.**

**A4 (minimax).  Is `CRIME_HARDINT` its own case?**  **CHECKED AND REJECTED — the brief survives.**
`385-387` is the shared INTSTAT/INTMASK body; there is no HARDINT case, so seven labels stands.
*This is the one finding I did not accept, and it was settled by opening the file.*

**A5 (minimax).  "The leftover" is unspecified and the CONTROL body was never inlined.**
**ACCEPTED** — pass 2 inlines `229-423` entire.

**A6 (deepseek).  The enumeration is internally contradicted by the brief's own two extra axes.**
**ACCEPTED as a defect — but see DISAGREEMENT D1 on the remedy.**

**A7 (grok).  The missing floor cell, named with its oracle requirement: INTSTAT 4R, latch-CLEAR,
with `SOFTINT|HARDINT` SEEDED NONZERO.**  *"`t4clear.py` is the TIME shape, not the class."*
**ACCEPTED**, and it is sharper than my own criterion, which said "with an oracle" without saying
what the oracle must contain.

**A8 (grok).  `G_clr_imk4r` 187/188 must STAY the positive control** in the 188-row instrument, so
the next closing pass keeps a CLEAR-half control that is not TIME.  **ACCEPTED** — repair 14 owes a
check that it does not disturb what `gate line` observes.

**A9 (grok).  P1 was not the full enclosing function**; the omitted prelude at `229-235`
(`CONTROL = ENDIANESS 0x100` on every access) **IS** the warrant for the CONTROL-4R equivalence the
packet asserted without it.  **ACCEPTED — a §D violation of mine.**

**A10 (codex).  The domain is reachability-constrained, not a cross-product.**  *"Adding lane and
PROM-window state mechanically gives 224 nominal tuples, but that misrepresents reachability... the
CRIME switch matches the EXACT offset, so every named label has lane bit clear; a four-byte access to
a register's low lane reaches `default`."*  **ACCEPTED — see D1.**

**A11 (codex).  The shipped probe has NO direct value assertion for accepted CONTROL `lw +0x08`** —
it runs through `ACCEPTS` where its destination is overwritten; `devsig hi` checks REV and
`acc ctl ld` checks eight-byte CONTROL.  **ACCEPTED**; it independently confirms that table 11's
`C_ctl4r` leg was vacuous for want of an ORACLE rather than an ACCESS.

**A12 (kimi).  THE BRIEF'S OWN REPAIR LEAVES A CELL OPEN.**  The escapes table lists four; pass 8
measured five; the dropped one (`G_lane_ctl`) is the only evidence about the lane axis at CONTROL,
and Parts A/B/C never name `ctl4r.py`.  **ACCEPTED — CHECKED**: `G_lane_ctl` appears once in the
brief, only as a liveness control, and `grep -cE "ctl4r|lane"` over Parts A/B/C returns 0.
**A repair 14 built literally from my brief reproduces the very failure the round exists to end.**

**A13 (kimi).  `MATCHED N, WRONG 0` certifies OUTCOME CLASSES, not row content**, and the count was
stale (12 → 13).  **ACCEPTED — CHECKED**: three legs carry `ROWS I NAMED THAT DID NOT RED` as notes
inside a `MATCH`.  Corrected in place.

---

## 3. THE DISAGREEMENTS — both sides in their own words.  **Settle these by MEASUREMENT, not vote.**

### D1 — WHAT REPLACES THE 56-CELL PRODUCT?  deepseek vs codex.

> **deepseek:** *"Neither axis is a factor in the 56 product.  If `relative_addr & 4` partitions the
> handler, the domain is at least doubled before considering `cpu->pc`; therefore the proposed
> closure does not enumerate the full domain."*

> **codex:** *"Adding lane and PROM-window state mechanically gives 224 nominal tuples, but that
> still misrepresents reachability.  The MIPS producer checks natural alignment... The CRIME switch
> matches the exact offset, so every named label has lane bit clear.  A four-byte access to a
> register's low lane reaches `default`."*

**They agree the brief is self-contradictory and disagree on the replacement.**  deepseek reasoned
from the packet; codex read `cpu_mips_instr_loadstore.c` and the dispatch.  **My disposition: codex,
on the evidence — but I want deepseek's objection tested rather than outvoted**, because "reachable"
is exactly the kind of premise this project has been wrong about before.

> **THE QUESTION:** is codex's reachability argument correct, and does it hold for the SPLIT-WIDTH
> accesses (the `len` 3/5/6/7 tails) as well as the natural ones?  **A seat that can read
> `cpu_mips_instr_loadstore.c` should settle this rather than argue it.**

### D2 — HOW WIDE MUST THE MIRROR BE?  My brief vs grok vs glm.

> **my brief (Part A):** a pre-latch MIRROR of the post-latch sessions.

> **grok:** *"Part A as stated aims at the wrong set and the wrong oracle.  A pre-latch mirror of the
> 23 POST rows / of P1–P6 does not close the class."*

> **glm:** *"The pinned set may be larger than P4 admits (mirror narrower), while 'the CLEAR half is
> wholly unobserved' is overstated."*

**grok and glm both push NARROWER and more targeted than my mirror; they differ on the basis.**
My disposition: the criterion is *a cell is covered exactly when some session drives it BEFORE that
session's first refused access, with an oracle that observes it* — which prices the repair per cell.

> **THE QUESTION:** apply that criterion to all 56 cells and say how many rows it actually demands.
> If the answer is "more than the mirror", the criterion is wrong.

---

## 4. SEAT RECORD — operational, never agreement

* **codex REFUSED on the first firing** (content filter), and **ANSWERED on the re-fire** with
  neutral vocabulary, scoped reading and the edit-construction question dropped: 353 KB streamed,
  zero flags.  The cause was my brief, not the seat.
* **kimi** was sampled at 34 KB and recorded as "no verdict line"; it finished at **225 KB with a
  verdict**.  That earlier record is superseded, not quietly replaced.
* **panel.sh reported 8/8 while one was a refusal**; `seat_verdicts.py` caught it.  When two checks
  disagree, find out which is broken — I read the tail, and the extractor was right.
* **opus5** was still measuring when this packet was drafted; its findings are appended below.
* **fable5 HELD** until this packet is complete — standing directive, and not a seat failure.

---

## 4b. *** THE BUCKETS WERE RE-DERIVED, NOT INHERITED — AND THE ANSWER SETTLES D2. ***
## `BUCKETS8_rerun.out` (sentinel `BUCKETS8_DONE`), run STATICALLY against the shipped probe.

kimi's K2 said Part C must re-derive the buckets with `buckets8.py` rather than inherit them.  **Done,
and the tool answers the question the whole panel was circling** — it reports, per ACCEPTS entry, which
sessions drive it in EACH latch state, and flags any entry whose only driver is one of the two
sessions that carry no value oracle (26 `rearm once` post-latch, 40 `latch x5` pre-latch).

    ENTRIES DRIVEN LATCH-CLEAR ONLY BY SESSION 40      ENTRIES DRIVEN LATCH-SET ONLY BY SESSION 26
      1   sd  +0x0    REV                                1   sd  +0x0    REV
      3   sw  +0x0    REV                                3   sw  +0x0    REV
      8   lw  +0x8    CTL                                4   lw  +0x0    REV
     21   lw  +0x10   IST   <-- THE ESCAPING CELL        8   lw  +0x8    CTL   <-- C_ctl4r's vacuity
     32   sw  +0x38   TIM   <-- glm's cell
     33   lw  +0x38   TIM   <-- glm's cell             N_POST_BLIND = 4
     40   sw  +0x4    DFL
     46   ld  +0x278  DFL
    N_PRE_BLIND = 8

**IT CONFIRMS THREE SEAT FINDINGS MECHANICALLY, EACH FROM A DIFFERENT DIRECTION:**

* **entry 21 (`lw +0x10` IST) is PRE-BLIND** — exactly grok's missing floor cell (A7), and exactly the
  mutant (`G_clr_ist4r`) that every existing instrument scores clean;
* **entries 32/33 (TIM) are PRE-BLIND** — glm's cell, the one `t4clear.py` already covers;
* **entry 8 (`lw +0x8` CTL) is BOTH pre- AND post-BLIND** — which is codex's A11 (*the shipped probe
  has no direct value assertion for accepted CONTROL `lw +0x08`*) arrived at from the opposite end, and
  it is why table 11's `C_ctl4r` leg was vacuous.

> ### **SO REPAIR 14's ROW DEMAND IS NINE ENTRIES, DERIVED RATHER THAN GUESSED:
> ### {1, 3, 4, 8, 21, 32, 33, 40, 46}, of which {1, 3, 8} are blind in BOTH latch states.**
>
> **That settles D2 against my own Part A.**  A mirror of the post-latch sessions would have added
> rows for cells that are already covered while still missing entry 21.  Nine targeted carriers is
> both smaller and complete — and it is a count whose members are listed, which is what §C4 demands.

**WHAT I STILL WANT ATTACKED:** `buckets8.py`'s blindness test is *"is the only driver session 26 or
40?"*  That is necessary.  **Is it sufficient?**  A cell driven by a third session that HAPPENS to
have no oracle for that particular channel would pass this test and still be blind.  **Does such a
session exist?**  If so the nine is a floor, not the answer.

## 5. THE OPUS MEASURING SEAT — **IT INVALIDATES THE REPAIR DESIGN, AND IT MEASURED IT.**

**VERDICT: DO NOT SHIP REPAIR 14 AS PROPOSED.  P2 IS FALSE AND P3 IS FALSE.**  Six mutants, two
tables, every log ending `CRIMEP_DONE`, predictions matched **6 of 6**, predictions timestamped
23:58:36 / 00:04:17 against builds at 00:00:0x / 00:18:4x.

    base           188/188  OK                  harness validated
    PC_imk4r       187/188  gate line           POSITIVE CONTROL -- reproduces close-8 exactly
    M1_gotolatch   178/188  10 rows             decline-side latch, UNRESTRICTED -- KILLED
    M2_ld278clr    188/188  --                  *** ESCAPE, a FIFTH one, unnamed in the brief
    M4_timeplain   184/188  time lb/sb/lh/sh    DISCRIMINATING CONTROL -- exactly the 4 predicted
    M3_timelatch   188/188  --                  *** TOTAL ESCAPE -- the Q2 answer

### O1 — **P2 IS THE ACCEPT HALF OF A 112-CELL SPACE.**  This is the finding of the round.

> *"The 56-cell product describes only accesses that are SERVICED.  The DECLINE arm -- the thing
> `#529` ADDED -- has its own product `{len 1,2} x {R,W} x {7 labels} x {latch}`, and the enumeration
> contains NONE of it.  Part A (pre-latch mirror of accept cells) and Part B (HARD_RESET at CONTROL)
> are both accept-side, so NEITHER CAN REACH IT."*

**ACCEPTED.  It supersedes D1 entirely** — deepseek and codex were arguing about how to extend the
accept-side product while the missing half was a different arm of the same `if`.

### O2 — **P3 IS FALSE: THE K-FORM IS LOUD, NOT SILENT.**

> *"The K-form with the latch CLEAR falls into the decline arm, SETS the latch and PRINTS.  It
> escapes because the announce is STOLEN -- in `latch x5`'s prologue the count stays 1 -- not because
> it is absent.  The G-form, a bypass before the width test, is the silent one."*

**ACCEPTED, and it is the one that most changes what a repair must do.**  My brief reasoned *"it
declines silently, so a survived-host row cannot see it"* and aimed the repair at value oracles.
**Reasoning from "it is silent" points a repair at the wrong channel**: the observable that moves is
an announce COUNT being stolen, not a value going unread.

### O3 — Q2 ANSWERED WITH A MEASURED TWO-LINE EDIT: `M3_timelatch`, **188/188**.

```c
+			goto crime_declined;        /* moved INSIDE the latch block */
 		}
-		goto crime_declined;
+		if (relative_addr != CRIME_TIME)
+			goto crime_declined;
```

A narrow access at `CRIME_TIME` that is **not its session's first refusal** falls into the switch and
advances the guest clock — one of the four defects the fix's own comment says the `goto` prevents.
`M4_timeplain` (the same edit WITHOUT the latch conjunct) is killed 184/188 on exactly the four
predicted rows; adding the conjunct hides it completely.  **~2.2 million to one on the raw value, and
the liveness control reads `large` in BOTH runs**, so the channel is live and the difference is the
mutant.

> **Part A cannot test this AT ALL**: a pre-latch session by construction contains no refusal before
> the cell under test.

### O4 — THE DECLINE × LATCH-SET AXIS, DERIVED: 7 cells, **2 OPEN (REV and TIME)**.

The discriminator needs no run: *does any session refuse at this label more than ONCE?*  CONTROL,
INTSTAT, INTMASK and `default` are covered (M1 reds ten rows across them); DOG is equivalent by
construction (`break;`, no body); **REV and TIME are open**, each refused only once per session.

> ***AND THE PROBE ALREADY KNEW.***  `crime_width_probe.py:1077-1079` states the asymmetry in as many
> words — *"REV and TIME were each refused only once per session, first; every other label is refused
> again after the latch is set"* — derived for a DIFFERENT mutant, and nobody turned it around to ask
> what it implies for the `goto`.  **Two rows in one diff close the axis; cell-by-cell finds TIME this
> pass and REV the next.**

### O5 — `M2_ld278clr`, a FIFTH escape at 188/188 — **and it CONFIRMS section 4b independently.**

ACCEPTS entry **46** (`ld +0x278`) — one of the eight PRE-BLIND entries `buckets8.py` named, and the
only one with neither an equivalence derivation nor a measurement.  Guest-visible: `reg[79]` is not
rewritten by the prelude.  **The seat reached entry 46 by building a mutant; the deriver reached it by
reading sessions.  Two roads, same cell.**

### O6 — **Part A's denominator is 8, not 23** (`mirror14.py`: `N_ENTRIES_WITH_NO_PRELATCH_OBSERVER=8
of 46`).  **This matches `BUCKETS8_rerun.out`'s `N_PRE_BLIND=8` exactly, from a tool I called INDEPENDENT and which is NOT -- *** CORRECTED AFTER THIS PACKET WAS FIRED: the kimi CLI seat checked and mirror14.py is the SAME capture machinery as buckets8.py with the row-attribution off-by-one fixed (same regexes, same latch-split rule, same probe source).  A systematic capture bug would agree in both.  The 8=8 result is CORROBORATION, not independence.  The seats answered against the uncorrected wording, which is how it was caught. ***.**

### O7 — **Q3 IS UNANSWERABLE AS POSED, AND THE PROBE'S OWN HEADER SAYS SO.**

2 of the 5 HOST-DIAGNOSTIC and 6 of the 10 EQUIVALENT cells have **no listed members**
(`crime_width_probe.py:242-257`: *"a bucket whose members cannot be listed cannot be audited"*).
**My brief promoted those counts to a SETTLED PREMISE while its own source flags them unlistable.
8 of 46 cannot be checked by anyone.**  This is §C4 at its sharpest, and it answers the residual
doubt I raised in section 4b: **nine is a FLOOR, not the answer.**

### O8 — smaller, all with warrants

* Four unnamed axes collapse: `cpu->is_32bit` is **dead code on ip32** (subtype 32 → R4400 →
  `isa_level 3` → `is_32bit == 0`); `ncpus`; `use_fb`; `physical_ram_in_mb`.  `writeflag` is binary.
* **A domain dependency nobody has stated:** a real MIPS guest emits `len` in {1,2,4,8} exactly, but
  `memory_rw.c:495-523` CLAMPS `len` at a device's end and can emit 1..7 — inert here **only because
  `DEV_CRIME_LENGTH` is `0x280`, a multiple of 8.**  Change that constant and 3/5/6/7 become
  reachable.  *(This is the other half of D1, and it makes codex's reachability argument conditional
  on a constant rather than absolute.)*
* Part B rider: an accepted HARD_RESET write **terminates its session**, so it must be a session's
  last access — Part B costs one NEW SESSION per cell.
* A stale citation `#529`'s own diff created: `OUTSTANDING_BUGS.md:5574` cites `dev_sgi_ip32.c:698`;
  the diff adds 30 lines above it and the target is now **`:728`**.

### O9 — ITS OWN ERRORS, RECORDED BY THE SEAT RATHER THAN BY ME

A row-to-session off-by-one in its deriver (found pre-ship; `buckets8.py` unaffected); the backslash
trap twice; and **a CRLF script that exited 0 having built and run nothing** — caught only because two
seconds is impossible for two 17-minute probes.  No damage: the `cd` failed before the sentinel was
dropped.

**FOOTPRINT: clean.** No project tree written, all four fork copies still md5 `8c1d1545…`, clone
sentinel cleared, source `cmp`-clean, binary `-nt` source, `restored` byte-identical to `base`.

---

## 6. *** WHAT THIS DOES TO THE REPAIR, STATED PLAINLY BEFORE YOU ANSWER ***

**Parts A, B and C as written are accept-side and cannot reach the decline arm.**  The measured total
escape (`M3_timelatch`) lives there, and so does the derived REV/TIME pair.  So repair 14 is not a
matter of adding nine carriers — **the enumeration it was built on covers half the space.**

> **THE QUESTION FOR THIS PASS: is O1 right that the decline arm is a SECOND 56-cell product, or is
> it smaller?**  The decline arm has no `switch`; it reaches the common tail directly.  What
> partitions it, derived from the code rather than by analogy with the accept side?

---

If, while verifying a claim, you found something ELSE — say so.
