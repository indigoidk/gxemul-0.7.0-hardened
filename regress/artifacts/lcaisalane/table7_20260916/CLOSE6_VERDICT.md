# CLOSING PASS 6 — **THE CHAIN DOES NOT CLOSE.** Fable 5.1 adjudication, 2026-09-17.

*This supersedes the closing assessment in `CLOSE6_FINDINGS.md`, which read the panel as three-yes /
one-dissent. That reading was wrong, and the reason it was wrong is recorded below rather than
quietly fixed.*

**Adjudicator identity proven:** Fable 5.1 (`claude-fable-5-1`), with `CHECKPOINT.md`'s first line
quoted verbatim.

---

## THE RULING

> **DO NOT CLOSE ON THIS PASS.** A file-reading seat named a clause-(d)-shaped mutant predicted to
> clean-sweep 352/352. Its producer and reachability are now VERIFIED in source. It is neither
> measured nor disclosed, so the floor question is OPEN and the zero is not carried over its full
> denominator. One bounded pass is owed. **The fix, the L4 grading, and the m_lenzero disposition are
> all sound** — the gap is the detector's width coverage, not the repair.

---

## *** MY PACKET OMITTED THE STRONGEST SEAT'S DISSENT.  THAT IS THE FINDING. ***

I framed the split as *"three file-reading seats say yes; the one dissent (glm) is packet-fed and
settled by the artifacts."* **Codex is file-reading, it is the max-effort seat, it produced the
largest answer, and it did not say yes.** At `codex.txt:6804` it wrote:

> *"**Measurement still needed:** this mutant against the composite, plus a focused control observing
> a 16-byte PROM-helper write reaching the handler and forwarding correctly. **The predicted sweep
> must not be recorded as measured.**"*

and

> *"The delivered evidence is valid for Table 7; its denominator does not establish complete closure."*

**HOW I MISSED IT, stated mechanically so it is fixable rather than moralised about:** codex streams
its reasoning into the output file. I read the TAIL — which this project's own convention says is
where a codex answer lives — and the tail held the end of its *reasoning*. Its verdict and its named
mutant sit at roughly line 6800 of a 563 KB file. I then "verified" the seat with a census of my own:
byte size plus a count of on-topic keywords. **That census cannot distinguish an answer from a
dissent**, and it returned ANSWERED for a seat whose verdict was NOT-COMPLETE.

**This is the UNREAD REVIEW class — three prior recorded instances in this project — committed on the
largest answer in the panel.**

## THE MUTANT, AND WHY IT IS INSIDE THE ENUMERATION

    dev_lca.c:299    if (writeflag == MEM_WRITE)   ->   if (writeflag == MEM_WRITE && len <= 8)

`writeflag == MEM_WRITE` DOMINATES the edited line `byte = data[ofs]` (`:300`, the hunk's own change),
and `len` is a body-read lvalue. **The joint-cell ruling's own worked example is exactly this shape**
— *"a condition qualified (`if (X)` → `if (X && writeflag == MEM_WRITE)`)"*. It diverges from base
**only at len > 8**, which no probe row drives (the probe is instruction-driven; max STQ = 8), so it
scores **352/352 — a clean sweep.**

## THE PRODUCER IS REAL, AND FABLE VERIFIED IT IN SOURCE RATHER THAN ACCEPTING CODEX'S TRACE

    memory.c:839, :841-853        store_buf issues memory_rw at psize in {1024, 256, 64, 16, 4, 1}
    memory_rw.c:150-151, :187     the split granule is 1024, NOT 8 (MRW_SPLIT_MASK = 0x3ff), so a
                                  16-aligned len-16 access passes WHOLE to the device
    memory_rw.c:587-589           the device is called with that len
    dev_lca.c:547-548             lca_isa is registered over 2 MB (0x10000 << 5) -- no clamp below 1024
    cpu_alpha_palcode.c:121,:144  PROM GETENV calls store_buf(cpu, a2, s, len) with a2 GUEST-SUPPLIED

**So a guest can drive a len-16 write into the sparse window and it reaches the handler whole.**

**AND THE CONTRACT IS A WRONG RECORD ABOUT REACHABILITY REGARDLESS — L4 AT MINIMUM.**
`lca_isalane_probe.py:136` discloses the width set as *"1/2/4/8 plus the 1 KB split"*, which **omits
the 16/64/256 cells that reach the handler unsplit.** So the cell is not disclosed either, and the
clause-(e) escape hatch is not available as the contract currently stands.

## THE OWED STEP — BOUNDED, WITH A MEASURED STOP.  This is not a #392 risk.

One pass, one named question: **build `len<=8` against the composite** (confirm 352/352) and **settle
len>8 reachability to this handler.** Then:

* **escapes AND len>8 is guest-reachable → L2**, add a len>8 row in-round, and decide separately
  whether the fix forwarding ONE byte of an N-byte store is acceptable or itself filed;
* **escapes but unreachable → clause-(e) DEBT**, disclose the `store_buf`-reachable width cell.

Either branch is cheap and terminates. The `:136` width-set line is corrected either way.

## WHAT FABLE UPHELD, each verified rather than deferred to

* **L4 not L2 on the kbcmd-post note** — the row fires (`WWall` reds it at all four widths) and the
  phantom-read shape is carried by `kbcq dib`. Only the prose was inverted. Correct in place: done.
* **m_lenzero closes glm's objection** — and Fable sharpened *why*: glm's trilemma dissolves because
  its premise C is mis-stated. The fifteen legs do not exhaust the enumeration; **m_lenzero is the
  sixteenth**, measured separately at 37/37 and equivalent-by-no-producer.
* **R1 (`&byte, len`): contract-naming discharges it — but my RATIONALE was loose.** I justified it as
  "inside clause (2) because `len` is a body-read lvalue"; Fable: clause (2) is the construction method
  for guard-operand-swap mutants, and a forward-transfer-width change is not one — *"if that loose
  reading were the test, DEPENDS-ON would be unbounded."* **The distinction that actually matters:
  `&byte, len` diverges WITHIN the probed width set (catchable, so a contract line suffices); codex's
  `len<=8` diverges only OUTSIDE it (uncatchable, so it cannot be discharged that way).**
* **R3: file the row AND keep the disclosure — both, not either.** Fable verified the sole-red claims
  (`probe_cdxZL3.raw` exactly one FAIL, `probe_W23.raw` exactly one at `:276`). The header line is
  *"where knowledge goes to not-fire"* — nothing surfaces it when someone edits `dev_pckbc.c`. **And
  `nox` is not a guaranteed tripwire:** a real 0x61 implementation could keep "two reads differ" true
  (liveness green) while breaking the exactly-one-parity-flip COUNT the kill depends on.

## A SECOND SEAT-HANDLING FAILURE IN THE SAME PANEL

**The kimi CLI WALLED MID-ANSWER and I did not notice**, because I ran my own census instead of
reading the one `panel.sh` had already written. `SEATS.txt` in the panel dir says:

    kimi     : 2457488b  *** WALLED MID-ANSWER -- content then a wall notice ***
            wall: auth_error: 403 You've reached your weekly (7-day) usage limit
            A WALL IS A MOMENT, NOT A STATE -- RE-FIRE THIS SEAT ONCE BY HAND
    deepseek : 2961b  CHECK (no verdict token)

That is 2.4 MB of real content ending mid-sentence in a quota notice — **the exact wall shape this
project records for this exact seat**, and the one a size check scores as the best answer in the
panel. My census returned ANSWERED for it.

> **THE TOOL CAUGHT ALL OF IT AND I SUBSTITUTED A WORSE CHECK.**  `panel.sh` flagged the wall, told me
> to re-fire by hand, and additionally flagged deepseek as CHECK for a missing verdict token. Three
> signals, written to a file in the panel dir, unread. *A check that exists and is not consulted is
> indistinguishable from one that was never built.*
