FABLE_SEAT_ALIVE_20260919_N6F2
# CHECKPOINT -- 2026-09-19 01:4x

VERDICT: SHIP the v4 diff (fix, bridge, arm E, teardown, gate) -- no floor breach (a)-(f) found; two L4 record
precisions to apply in-round (one sentence each, no code semantics change); the ruling is PROVISIONAL on 8 of 9
seats and the round's only measurement is the main loop's -- discharge the independent measurement with ONE bounded
agy build (the independent road) rather than waiting on the Opus reset, and say "main-loop measurement only" in the
record if the owner ships before it lands.

## Q1 -- is the v4 diff right?  YES, checked hunk by hunk against the packet.
* FIX: member 4, `odata = d->irq_enable` kept, fatal()+exit(1) deleted from the READ branch only; write branch and
  every other case untouched.  Correct and minimal.
* BRIDGE: K arm -> `0xE590718C` (ldr r7,[r0,#396]) in all three probes; complaint text "ENABLE CLEAR"; K predicates
  require complaint AND exit==1 (measured load-bearing: x_exit2, y_sigkill, z_silentexit each RED 3/3).
* ARM E encodings re-decoded by hand: E5D09188 ldrb (P=U=B=L=1), E280AD06 = add sl,r0,#6 ROR 26 = 0x180,
  E1DAB0B8 = ldrh fp,[sl,#8] (SH=01), E580818C str to +0x18c.  All as labelled; D1 compares them at run time anyway.
* FLOOR: (a) pre-fix RED 10/19; (b) verbatim reinstatement -> E0 dies; (c) identity rows E0/E1/E2/E3/E6/E5 carry
  values; (d) the dominating predicate is `writeflag == MEM_WRITE` -- weakened forms (len guard, value guard on
  irq_enable, re-exit on zero / nonzero) are each caught by a named row; the body reads one field and tests nothing,
  so no joint cells; (e) contract present with (a)-(d) disclosures; (f) E5 anchors Clear through the Set read path,
  E3/E6 anchor lanes, K anchors the neighbour at +0x18c.  No breach.
* TEARDOWN (the part I was asked to be hardest on): the drain loop's correctness rests on rd() returning True on a
  select timeout and False only on EOF/EIO.  I CHECKED it (one grep, declared below): sites `rd` :184-196 and
  Session.rd :295-306 both do exactly that.  So the drain is bounded by the deadline or EOF, never by a quiet 100 ms.
  The HARNESS-KILL / HARNESS-CLOSE labels are ATTRIBUTION ONLY -- no predicate reads `signal`; survived() needs
  exit==0 and K needs exit==1 -- so neither label can turn a red green or a green red.  That is the right shape.
  `gone` on ECHILD skips the kill: correct.  Status is computed BEFORE close() in every arm, so the drain setting
  dead/dead[0] on EOF cannot retro-flip a SURVIVED to HOST-DIED.
* GATE: E2 want 0x60002002 = P|Q, E0 want 0; excerpt grep `E(C1|A1|[0-6]) ` exact.  One precision below.

## Q2 -- which of your dispositions is wrong?
* F16, F17, F18 rejections: UPHELD (two files; NO-PROMPT branch runs no arm; I=0 is the immediate form -- the bit-25
  decode above confirms it on every E word).
* D1 UPHELD as hardening, L1.  D3 UPHELD: (r) is the value form of the width cell; E3 wants 0x02 and any non-
  equivalent width guard leaves odata 0 (initialised at function top) -- arithmetic on one row, no table owed.
* THE ONE DISPOSITION I OVERTURN IN PART: D2 / the contract's "a kept diagnostic (E4)".  E4's oracle is
  `not E["fatals"]`, and `fatals` is `\[[^\r\n\]]*footbridge[^\r\n\]]*\]` -- a BRACKETED line containing the word
  "footbridge".  A diagnostic reinstated with other text (no brackets, or without the device name) ESCAPES E4.  The
  ruling "different text must still red E4" is true only for text that keeps the bracket-and-name shape.  Not a
  floor breach (no floor clause requires this cell) but the contract overclaims -> L4: state E4's real predicate
  ("no bracketed diagnostic naming footbridge") and list the bare-text form under NOT COVERED.  One sentence.
* Gate comment L4 (cosmetic, one token to strengthen): "with the count above, each E0-E6 appears exactly once" is
  not what the pair proves -- a duplicated ok E2 plus a FAIL E3 gives ok-count 7 and distinct-ids 7.  It is
  caught by the every-row-green check, so the gate is sound; either soften the sentence or count distinct ids over
  the OK lines (`grep -E '^E[0-6] .*ok$' | cut -d' ' -f1 | sort -u | wc -l`), which proves the claim by itself.
* Applied §F2 corrections I audited and keep: budgets 20+10 s (patience only); `gone`; HARNESS-CLOSE; keys-required
  T rows; bit-30-only; z_silentexit.  Nit, not a defect: when the child dies in the last 50 ms poll gap the kill
  lands on a zombie and waitpid returns the PRODUCT status under a HARNESS-KILL label (e.g. "HARNESS-KILL(None)"
  beside exit=1).  Label only when `sig == SIGKILL`; file otherwise.  Also `eof` is not returned, so "the expiry
  is recorded" means only the label -- return it if you want the record to say WHICH deadline expired.
* My own p1 record: the "no such sentence exists" claim about OUTSTANDING_BUGS was FALSE (:2681-2682 says it in
  other words).  L4 against me; correct in place as you did.

## Q3 -- roster.
Opus and codex(§F2) are SEAT FAILURES, kimi's stall a new class -- all correctly recorded as failures, none as
agreement.  The doctrine says a ruling short of the roster is provisional on its face and "if a seat cannot be run,
STOP AND ASK THE OWNER".  My read: the DIFF is right on 8/9 and four measured tables; what is missing is
INDEPENDENCE of measurement, not measurement.  agy is the roster's compile-and-measure front end on a road
independent of the Agent tool (the #462 precedent) and answered §F2 -- one bounded job (copy the tree, build base +
mutant (a) + z_silentexit, run the sites probe, never write GXEMUL-SEC) discharges F22's substance in one invocation.
Recommend: fire that, commit when it lands; if the owner prefers to ship first, the record must say "main-loop
measurement only; independent measurement OWED (Opus walled, agy not yet asked)".  Do not hold for the Opus reset
specifically.

## Q4 -- standing licence, what we all missed.
1. E4's text-shape blindness (above) -- nobody in F1-F23 or D2 read the regex against the ruling.
2. The sites probe's teardown correctness rested on a rd() convention no seat stated for THAT file (kimi read
   Session.rd; the sites probe has its own local rd).  Checked here: same convention.  Say so in the header.
3. Records: the E rows use r1/r2, which arm L scores as A2 -- disclosed; fine.  The witness/drain headers now say
   "the enable registers play no part" -- true.

SEAT RECORD: fable5 (Claude Fable 5.1), ninth seat + adjudicator.  Read: (1) f2_packet_BUILT.md, (2) the brief
digest, (3) diff539_4files.v4.patch and diff539_gate.v4.patch.  (4) no seat file opened.  ONE declared step outside
the four-file bound: `grep -n -A12 "def rd"` on footbridge_sites_probe.py and fbpending_drain_probe.py, because the
teardown ruling turned on it and it was checkable in seconds.  Nothing run, nothing edited in any project file.
