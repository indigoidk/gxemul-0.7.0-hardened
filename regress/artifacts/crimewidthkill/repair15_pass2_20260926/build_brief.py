#!/usr/bin/env python3
"""build_brief.py -- assemble #529 repair 15's PASS-2 brief from VERBATIM excerpts (never retyped): the CRIME access
function and its time/tick code from dev_sgi_ip32.c 8c1d1545, the probe helpers from the frozen table-14 probe, the
repair-15 diff, every mutant hunk, tables 12/13a and (when present) table 14's lanes and check14.out.  Each excerpt is
taken by an ANCHOR, and a missing anchor is a hard failure -- a brief that silently drops a block is the defect this
script exists to prevent.  Writes pass2_brief.md beside this file; prints its size and every section's byte count."""
import io, os, re, sys

SEC = r"C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC"
A = os.path.join(SEC, r"regress\artifacts\crimewidthkill")
T14 = os.path.join(A, "table14_20260926")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "pass2_brief.md")


def rd(p):
    return io.open(p, encoding="utf-8", errors="replace", newline="").read().replace("\r\n", "\n")


def between(text, start, end, incl_end=True):
    i = text.find(start)
    if i < 0:
        sys.exit("ANCHOR MISSING: %r" % start[:60])
    j = text.find(end, i + len(start))
    if j < 0:
        sys.exit("END ANCHOR MISSING: %r" % end[:60])
    return text[i:j + (len(end) if incl_end else 0)]


def hunks(p):
    return "\n".join(l for l in rd(p).split("\n") if re.match(r"^[+-][^+-]", l))


ip32 = rd(os.path.join(SEC, r"src\devices\dev_sgi_ip32.c"))
probe = rd(os.path.join(T14, "crime_width_probe.table14.py"))
fn_access = between(ip32, "DEVICE_ACCESS(crime)\n{", "\treturn 1;\n}\n")
fn_time = between(ip32, "void crime_update_crime_time(struct crime_data* d)", "DEVICE_TICK(crime)\n{", False)
fn_tick = between(ip32, "DEVICE_TICK(crime)\n{", "}\n")
helpers = between(probe, "def session(cmds, settle=1.5, spin=1.2):", "def said(t, ln, off, clean):", False)
consts = between(probe, "CODE = 0x80001000", "PROBE_PC = 0xbfc05180", False).rstrip("\n")
consts_line = probe[probe.find("PROBE_PC = 0xbfc05180"):].split("\n")[0]
nth_mag = between(probe, "def nth(t, reg, n):", "def ip2(v):", False) + "\n" + \
    between(probe, "SMALL = 66 * 100000", "for op in (\"lb\", \"sb\", \"lh\", \"sh\"):", False)
time_rows = between(probe, "for op in (\"lb\", \"sb\", \"lh\", \"sh\"):\n    A = Addr(CODE)\n    c = []\n"
                           "    x, _ = ld(A, \"ld\", CRIME + 0x38, \"s0\"); c += x\n    if op",
                    "        row(\"time said\", said(t, 1, 0x38, clean), 1, \"lb +0x38 (first refusal): its own announce\")\n")
rev_rows = between(probe, "for op in (\"lb\", \"lh\"):\n    A = Addr(CODE)\n    x, _ = ld(A, op, CRIME + 0, \"v0\", at=PROBE_PC)",
                   "        % (1 if op == \"sb\" else 2))\n")
latch_rows = between(probe, "for op, off in ((\"lh\", 6), (\"lb\", 7), (\"lbu\", 0x3f)):",
                     "row(\"latch surv\", pr(t, \"v1\"), \"0x%x\" % LIVE_VAL, \"host survives all five\")\n")
diff = rd(os.path.join(HERE, "probe_r15.diff"))
R14M = os.path.join(A, r"repair14_20260916\mutants")
T13M = os.path.join(A, r"table13a_20260925\mutants")
muts = []
for m in ("M1_gotolatch", "M3_timelatch", "M4_timeplain", "M5_revlatch", "M6_istlatch"):
    muts.append((m, hunks(os.path.join(R14M, m + ".diff"))))
for m in ("M7_intmasklatch", "M8_ctllatch"):
    muts.append((m, hunks(os.path.join(T13M, m + ".diff"))))
for m in ("G_glm_tim4clear", "G_clr_ist4r", "G_clr_ctl4r", "G_clr_imk4r", "G_lane_ctl", "K_ctl4w_reset_post",
          "K_ctl8w_reset_post", "M2_ld278clr", "W_ctl8w"):
    muts.append((m, hunks(os.path.join(R14M, m + ".diff"))))
dmut = os.path.join(T14, r"mutants\D_nodogclear.diff")
muts.append(("D_nodogclear", hunks(dmut) if os.path.exists(dmut) else "(built by table 14's driver)"))
t12 = "".join(rd(os.path.join(A, r"repair14_20260916\logs\lane%d.out" % i)) for i in range(4))
t13 = "".join(rd(os.path.join(A, r"table13a_20260925\logs\lane%d.out" % i)) for i in range(3))
t12 = re.sub(r" CRIMEP_CONTROL=\S+", lambda m: m.group(0), t12)
lanes14 = [os.path.join(T14, r"logs\lane%d.out" % i) for i in range(4)]
chk = os.path.join(T14, "check14.out")
if os.path.exists(chk) and all(os.path.exists(p) for p in lanes14):
    t14 = "".join(rd(p) for p in lanes14)
    c14 = rd(chk)
    have14 = True
else:
    t14 = c14 = "*** TABLE 14 HAS NOT FINISHED -- this brief is a DRAFT and must not be fired. ***\n"
    have14 = False
pretable = rd(os.path.join(T14, "PRETABLE14.out"))
pred = between(pretable, "PREDICTIONS -- exact red sets", "Every pre-existing row's colour", False)

F = "```"
S = []
S.append(("opener", """# #529 crimewidthkill -- REPAIR 15, PASS 2 (closing pass on the repair diff; the floor question on the composite)

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`** (the uncommitted #529 working set) **and the
frozen probe `GXEMUL-SEC/regress/artifacts/crimewidthkill/table14_20260926/crime_width_probe.table14.py`.**
There are THREE pristine-2021-upstream copies of GXemul under the project root (`./src/` and two
under `_archive/audit-results-*/builds/`).  They are NOT this fork.  If your line numbers disagree
with mine by hundreds you are reading one of them -- say so rather than reconciling.

**If you cannot read files that is expected** -- every fact you need is inlined below.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim -- an index range, an offset, a count of
reachable addresses -- ENUMERATE it rather than reasoning about it.**  Walk the values.
A derivation that skips one masking line reads exactly like a correct one.

**And ENUMERATE THE RIGHT DOMAIN -- a domain is itself a premise.**  Ask what the PRODUCER of
these values can actually emit before you walk them.

**VERDICT LINE FIRST**, so your answer survives truncation.  Then one line per question below,
then your reasons.  Language: this is ordinary bounds-and-error-handling review of an emulator's
device model; "declined" means an access the model refuses and answers with 0.
"""))
S.append(("status", """## 1. STATUS -- WHAT HAS AND HAS NOT SHIPPED (checked when this brief was written)

* **#529 is NOT committed.**  HEAD is `f4f601c4` (#548).  #529's working set is uncommitted and
  will not commit before #549 does, nor before the GPT-6 Astra adjudicator confirms.
* The working probe `regress/crime_width_probe.py` is still the 204-row `a0af7c92`.  Repair 15 exists
  ONLY as the frozen 218-row copy under review (`f5e915f6`), built by a script from `a0af7c92`.
* The gate pin in `regress/gate_arm.sh` still reads 204; moving it to 218 is OWED after this pass,
  citing table 14's base leg.

**WHAT #529 IS.**  One guest `lb/lbu/lh/lhu/sb/sh` anywhere in the SGI O2's CRIME register window used
to END THE PROCESS.  #529 declines the narrow width instead: announced once per device (a latched
`fatal()`, which prints and returns), a read answered 0 through the common tail, a write dropped --
and the register switch SKIPPED, because falling through it would let a declined halfword stop every
CPU (CONTROL), redirect the PC (REV), reassert the interrupt line (INTSTAT/INTMASK) or advance the
clock (TIME).  The detector is a 204-row probe, reviewed across fourteen repairs.
"""))
S.append(("why", """## 2. WHY REPAIR 15 EXISTS

The flagship adjudicator's first-hand re-ruling (2026-09-25) set the floor for the
DECLINE-SUPPRESSION class -- a `goto crime_declined` that is skipped for one label once the width latch
is already SET -- as **{observable skipped label} x {latch SET}**.  Table 12 had measured the class:

    M3_timelatch  (TIME exempted once the latch is set)   204/204  -- NOTHING SAW IT
    M5_revlatch   (REV  exempted once the latch is set)   204/204  -- NOTHING SAW IT
    M4_timeplain  (TIME exempted in EITHER latch state)   200/204  killed by the `time' rows
    M6_istlatch   (INTSTAT exempted once the latch set)   201/204  killed by the `istat' rows

and table 13a measured the two labels that were only DERIVED covered:

    M7_intmasklatch  201/204  killed (imask sb/lh/sh)      M8_ctllatch  201/204  killed (sb08 msg, sh08b run, gate run)

M3/M5 escaped because every session that refused at TIME or REV did so as that session's FIRST
refusal (latch CLEAR), and the one session that refuses there with the latch SET (`latch x5`) does it
from ordinary code (REV's redirect needs the PROM window) with no TIME sample afterwards.  **Repair 15
adds, per label, sessions whose FIRST refusal is at +0x07 (sets the latch) and whose SECOND is at the
label**, all four narrow ops each, reading the arm's own side effect.  It also adds the pair the
adjudicator's repair-14 ruling made conditional for ACCEPTS entries 13/17 (CONTROL's DOG_ENABLE-only
writes) -- see section 6.
"""))
S.append(("settled", """## 3. PREMISES ALREADY SETTLED, RE-INLINED SO NOBODY SPENDS AN ANSWER RE-DERIVING THEM

Each was RE-READ in this scope while this brief was written (citations are to the working tree):

* **`fatal()` prints and returns; it never ends the process.**  `src/core/debugmsg.c`, the whole body:
  `va_list argp; va_start(argp, fmt); va_debug(argp, fmt); va_end(argp);`
* **Every probe session is a FRESH emulator** (`session()` below: `pty.fork()` + `os.execv(BIN, [...
  "-E", "sgi", "-e", "ip32" ...])`), so the width latch starts CLEAR in every session.  Adding a
  session cannot change another session's rows.
* **Exactly ONE CRIME tick per probe session, at its first step.**  `src/machines/machine.c`: a tick
  function starts with `ticks_till_next[n] = 0` and `ticks_reset_value[n] = 1 << tickshift`; each pass
  of the loop does `ticks_till_next[te] -= single_step ? 1 : N_SAFE_DYNTRANS_LIMIT;` and fires while
  `<= 0`.  CRIME registers with `CRIME_TICKSHIFT` = 14, so the next tick is 16384 single steps away,
  and a probe session steps a few dozen instructions.
* **The CRIME access function, verbatim** (`src/devices/dev_sgi_ip32.c`, md5 8c1d1545):

""" + F + "c\n" + fn_access + F + """

* **The TIME update and the tick, verbatim:**

""" + F + "c\n" + fn_time + fn_tick + F + """
"""))
S.append(("helpers", """## 4. THE PROBE'S HELPERS, VERBATIM (from the frozen table-14 probe)

""" + F + "python\n" + consts + "\n" + consts_line + "\n\n" + helpers + "\n" + nth_mag + F + """

The PRE-EXISTING rows that refuse at TIME and REV (latch CLEAR at the refusal), and the `latch x5`
session's later refusals at +0x00 and +0x38 (latch SET, from CODE, no TIME sample after):

""" + F + "python\n" + time_rows + "\n" + rev_rows + "\n...\n" + latch_rows + F + "\n"))
S.append(("diff", """## 5. THE DIFF UNDER REVIEW -- `regress/crime_width_probe.py` a0af7c92 -> f5e915f6, WHOLE

""" + F + "diff\n" + diff + F + "\n"))
S.append(("ctldog", """## 6. THE ENTRIES-13/17 CHANNEL CHECK (the repair-14 ruling's conditional, run for this repair)

The ruling's words: *"name the mutant each kills and the observable that differs ... If a
body-tested-partition mutant escapes -> L2, IN as the pair; if the count cannot vary under any such
mutant -> clause (e), disclosed."*  ACCEPTS entries 13/17 are accepted `sw`/`sd +0x08 = 0x0200`
(DOG_ENABLE alone).  The prelude re-forces CONTROL = ENDIANESS at every access, so the stored value is
visible to nothing; the arm clears DOG, the residue is 0, nothing prints and nothing stops.  The
mutant that moves the cell: **D_nodogclear**, the DOG branch's `idata &= ~CRIME_CONTROL_DOG_ENABLE;`
deleted, which makes the arm print for 0x0200.  Before repair 15 five rows counted
`CRIME_CONTROL: unimplemented` -- `sw08 msg ctl` (session writes sw 0x01), `sb08 msg` and `sh08b msg`
(REFUSED narrow writes, declined before the arm), `acc ctl sd` (sd 0x01), `p acc ctl msg` (sd 0x01,
sw 0x0001, sw 0x0201, sd 0x0201) -- and NONE of their sessions writes 0x0200; the ACCEPTS sessions
that do write it count only `-- declined.`.  So repair 15 adds `ctldog sw msg` / `ctldog sd msg`: one
session per width, the 0x0200 write then its 0x0201 twin (the in-session liveness half), expecting ONE
text.  A silent decline of the 0x0200 write still reads one -- disclosed as EQUIVALENT.
"""))
S.append(("mutants", """## 7. THE MUTANTS, VERBATIM HUNKS (each applied to dev_sgi_ip32.c 8c1d1545; every re-derived edit was
checked byte-identical to the diff its earlier table preserved)

""" + "\n".join("**%s**\n\n%s\n%s\n%s\n" % (m, F, h, F) for m, h in muts)))
S.append(("tables", """## 8. MEASUREMENTS

**Table 12** (repair 14, 204 rows; `repair14_20260916/logs/lane*.out`, verbatim):

""" + F + "\n" + t12 + F + """

**Table 13a** (the INTMASK/CONTROL swaps and a base leg on probe a0af7c92, 204 rows; verbatim):

""" + F + "\n" + t13 + F + """

**Table 14 PREDICTIONS**, written in `PRETABLE14.out` BEFORE any build (its mtime proves the order), verbatim:

""" + F + "\n" + pred + F + """

**Table 14 RESULTS** (218 rows; four lanes; `table14_20260926/logs/lane*.out` and `check14.out`, verbatim):

""" + F + "\n" + t14 + "\n" + c14 + F + "\n"))
S.append(("numstat", """## 9. WHAT THIS PACKET SHOWS OF #529's FILES

    regress/crime_width_probe.py      repair 15's diff: INLINED whole (section 5)
    src/devices/dev_sgi_ip32.c        UNCHANGED by repair 15; the whole access function INLINED as context
    regress/gate_arm.sh               UNCHANGED by repair 15; the 204 -> 218 pin is OWED after this pass
    records (CHANGELOG, ledger, MANIFEST, carrier)   NOT SHOWN -- not written yet; they follow this pass
"""))
S.append(("questions", """## 10. QUESTIONS (verdict line first; then one line per question; then reasons)

**Q1. PREMISE AUDIT -- each stated as a question.  Check the ones you can; name the ones you cannot.**
  (a) Is it true that a session's rows cannot be moved by adding OTHER sessions (fresh emulator per
      session)?  Is there any state that crosses sessions -- a file, the dummy RAM image, the host clock?
  (b) Is it true that the `tl` rows' s1 stays SMALL on the fixed build?  Walk the updates to
      `d->reg[TIME]` in a `tl` session step by step: the s0 load, the tick, the +0x07 refusal, the
      refusal at 0x38, the s1 load.  Where exactly can an update happen, and is the fixed build's s1
      the value left by the tick?
  (c) Is it true that the REV arm's redirect fires for all four narrow ops once the goto is skipped --
      including the WRITES, and including `lh` (a 2-byte access at +0x00)?
  (d) Is it true that D_nodogclear is the ONLY mutant of the CONTROL arm's DOG partition that no row
      saw before repair 15?  (Think of DOG treated as a stop bit; DOG suppressing the residue print; a
      re-arm inside the DOG branch.)
  (e) Is the five-label enumeration complete?  The switch's labels are REV, CONTROL, INTSTAT, INTMASK,
      DOG, TIME and `default:` -- which of them has a guest-observable effect that a suppressed decline
      would expose, and is any offset outside those labels observable some other way?

**Q2. THE FLOOR QUESTION, ON THE COMPOSITE.**  After repair 15, does any mutant exist in the
decline-suppression class {observable label} x {latch SET} -- or in the enumeration the contract claims
(section 5's contract block) -- that the 218 rows do not see?  Name the label, the latch state and the
row you expect to stay green.  **The closing condition is zero breaches WITH THE DENOMINATOR: say which
cells and shapes you swept.**  A bare "none found" does not close.

**Q3. THE 13/17 DISPOSITION.**  The ruling offered two dispositions (L2 pair, or clause-(e) disclosure).
Is the pair the right member, and is there a member neither the ruling nor this brief named?  Is the
pair's channel sound -- can `ctldog <w> msg` read ONE on a build where the 0x0200 write DID print?

**Q4. TABLE 14 AGAINST ITS PREDICTIONS.**  Section 8 shows the pre-registered red sets and the results.
Does any leg's result differ from its prediction, and if so which of the three explanations fits
(mis-built mutant, dead target, mis-cut row)?  Does any row red on a leg where no hunk reaches it?

If, while verifying a claim, you found something ELSE -- say so.
"""))

body = "\n".join(t for _, t in S)
nf = sum(1 for l in body.split("\n") if l.startswith(F))
if nf % 2:
    sys.exit("UNBALANCED CODE FENCES: %d" % nf)
io.open(OUT, "w", encoding="utf-8", newline="").write(body)
print("wrote %s: %d bytes, table14 %s" % (OUT, len(body.encode("utf-8")), "INCLUDED" if have14 else "PENDING (DRAFT)"))
for name, t in S:
    print("  %-10s %6d" % (name, len(t.encode("utf-8"))))

# ---- the CODEX variant (BRIEF_TEMPLATE.md section C5): ordinary engineering vocabulary, the reading scoped away from
# ---- the archive, and CHECK questions only -- no request to construct an edit that re-opens a defect (rule 3).
CODEX_SCOPE = """
**READING SCOPE FOR THIS SEAT.**  Everything you need is inlined above.  If you verify anything, read ONLY
`GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/*.py`.  Do NOT read `GXEMUL-SEC/regress/artifacts/`, `_scratchpad/`,
`GXEMUL-SEC/CHANGELOG.md` or `GXEMUL-SEC/tools/pipeline/`.  The device file is
`GXEMUL-SEC/src/devices/dev_sgi_ip32.c` (function `DEVICE_ACCESS(crime)`).
"""
CODEX_Q = """## 10. QUESTIONS (verdict line first; then one line per question; then reasons)

**Q1. PREMISE AUDIT -- each stated as a question.  Check the ones you can; name the ones you cannot.**
  (a) Is it true that a session's rows cannot be moved by adding OTHER sessions (a fresh emulator per
      session)?  Is there any state that crosses sessions -- a file, the dummy RAM image, the host clock?
  (b) Is it true that the `tl` rows' s1 stays SMALL on the fixed build?  Walk the updates to
      `d->reg[TIME]` in a `tl` session step by step and say where an update can happen.
  (c) Is it true that the REV arm's PC redirect is reached by all four narrow ops once the decline is
      bypassed -- including the writes and the 2-byte `lh` at +0x00?
  (d) Is the five-label list complete?  The switch's labels are REV, CONTROL, INTSTAT, INTMASK, DOG, TIME
      and `default:`.  Which have a guest-visible effect that a bypassed decline would expose?

**Q2. CHECK THE COVERAGE CLAIM, BY READING THE ROWS.**  The contract claims each guest-visible label has a
row that observes a narrow access reaching the register switch AFTER the width latch is already set.  For
each of INTSTAT, INTMASK, CONTROL, TIME and REV, name the row(s) that observe it, or say that none does.
Say which label/latch cells you checked, so a "none missing" answer carries its denominator.

**Q3. THE ENTRIES-13/17 PAIR.**  Is the `ctldog <w> msg` channel sound -- can it read ONE on a build where
the 0x0200 write DID print?  Is there a better disposition than the pair or a written disclosure?

**Q4. TABLE 14 AGAINST ITS PREDICTIONS.**  Does any leg's result differ from its pre-registered red set?
Does any row fail on a leg whose edit cannot reach it?

If, while verifying a claim, you found something ELSE -- say so.
"""
cbody = "\n".join((CODEX_Q if n == "questions" else t) for n, t in S)
cbody = cbody.replace("killed by the `time' rows", "detected by the `time' rows") \
    .replace("killed (imask sb/lh/sh)", "detected (imask sb/lh/sh)") \
    .replace("killed (sb08 msg, sh08b run, gate run)", "detected (sb08 msg, sh08b run, gate run)") \
    .replace("201/204  killed by the `istat' rows", "201/204  detected by the `istat' rows")
cbody = cbody.replace("**VERDICT LINE FIRST**", CODEX_SCOPE + "\n**VERDICT LINE FIRST**", 1)
_t_old = "# #529 crimewidthkill -- REPAIR 15, PASS 2"
_p_old = ("frozen probe `GXEMUL-SEC/regress/artifacts/crimewidthkill/table14_20260926/crime_width_probe.table14.py`.**")
for _o in (_t_old, _p_old):
    if cbody.count(_o) != 1:
        sys.exit("CODEX VARIANT ANCHOR MISSING: %r" % _o[:50])
cbody = cbody.replace(_t_old, "# #529 (the CRIME narrow-width decline) -- REPAIR 15, PASS 2") \
    .replace(_p_old, "probe `GXEMUL-SEC/regress/crime_width_probe.py` (a0af7c92) with the repair-15 diff that section 5\n"
                     "inlines WHOLE applied to it -- the repaired probe is exactly that file plus that diff.**")
for w in ("kill", "Kill", "KILL", "host dies", "HOST DIES"):
    if w in cbody:
        print("  NOTE codex variant still contains %r at %d site(s)" % (w, cbody.count(w)))
OUTC = os.path.join(HERE, "pass2_brief_codex.md")
io.open(OUTC, "w", encoding="utf-8", newline="").write(cbody)
print("wrote %s: %d bytes" % (OUTC, len(cbody.encode("utf-8"))))

# ---- the DEDICATED ADVERSARIAL GROK job (owner, 2026-09-24: every panel adds one) -- a pointer plus a charge ----
FROZEN = r"C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\repair15_pass2_20260926\pass2_brief.md"
GROK = """# DEDICATED ADVERSARIAL SEAT -- #529 repair 15, pass 2

Read the brief at `%s` in full first (it inlines the device function, the probe helpers, the repair
diff, every mutant and every table).  You are READ-ONLY: do not modify any file.

YOUR JOB IS TO BREAK IT, not to review it.  Find the SMALLEST edit to `DEVICE_ACCESS(crime)` in
`GXEMUL-SEC/src/devices/dev_sgi_ip32.c` that still compiles and that the 218-row probe would NOT detect,
where the edit either
  (i)   lets a narrow access reach the register switch at a guest-visible label in SOME latch state
        (the decline-suppression class -- the brief's section 2), or
  (ii)  changes what an ACCEPTED access at CONTROL does to the DOG / HARD_RESET / residue handling in a way
        no row reads (the entries-13/17 area -- section 6), or
  (iii) breaks any other claim in the contract block of section 5.
For each candidate: the exact edit, the rows you expect to change and the rows you expect to STAY GREEN,
and why each stays green (walk the session).  Be concrete: a candidate without a named green row is not
an answer.  If you find none, list the candidate shapes you tried and why each is caught -- that list is
the denominator, and "none found" without it does not count.

VERDICT LINE FIRST (BREAK FOUND / NO BREAK FOUND with the denominator).
""" % FROZEN
OUTG = os.path.join(HERE, "pass2_grok_adversarial.md")
io.open(OUTG, "w", encoding="utf-8", newline="").write(GROK)
print("wrote %s: %d bytes" % (OUTG, len(GROK.encode("utf-8"))))
