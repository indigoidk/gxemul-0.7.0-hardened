# #529 crimewidthkill -- REPAIR 15, PASS 2: THE ADJUDICATION PASS (F2), with REPAIR 16 AS ITS DISPOSITION

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

This packet carries every seat's pass-2 findings, MY disposition on each, and the disagreements with both sides.  **The
load-bearing question is Q2: which of my dispositions is WRONG.**  Several of your pass-2 challenges could not be settled
from the pass-2 packet because it did not show the sessions they turned on; those sessions are inlined here (E1-E7) --
please re-check your own finding against them, and say plainly if it still stands.  A seat whose finding I ADOPTED
should scrutinise my ruling HARDER, not less: a ruling in your favour is the one you are least likely to test.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`** (the uncommitted #529 working set, `dev_sgi_ip32.c` md5 8c1d1545) and the
probes frozen under `GXEMUL-SEC/regress/artifacts/crimewidthkill/`.  Three pristine-2021-upstream copies of GXemul sit
under the project root; they are not this fork.  If you cannot read files that is expected -- the evidence is inlined.
Name any premise you cannot settle.  **Enumerate rather than reason** where a claim is arithmetic.  **VERDICT LINE FIRST.**
Language: ordinary bounds-and-error-handling review of an emulator device model.

**STATUS WHEN WRITTEN:** nothing of #529 is committed (HEAD f4f601c4); nothing will commit before #549 does and before
the GPT-6 Astra adjudicator confirms.  Repair 15's pass-2 roster: codex WALLED (usage limit, re-fire after 07:01);
kimi CLI 403 (its seat covered by kimi-k3:cloud, PACKET-FED); agy, grok, glm, deepseek, minimax, kimi-k3:cloud answered;
the dedicated adversarial grok job answered; the Fable seat answered after a fallback it recovered from (the fallback
text is kept, labelled NOT A SEAT ANSWER); the Opus measuring seat's answer is section 5.

## 1. WHAT CHANGED SINCE THE PASS-2 PACKET

* **Table 15a** (E9) measured the dedicated grok seat's candidate: `H_noresetclear` (the HARD_RESET branch's clear
  skipped) passes all **218** rows of repair 15's probe; so does `E_noendianclear` (the unconditional ENDIANESS clear
  skipped).
* **The Opus measuring seat** (section 5; verified claude-opus-5-5 throughout) measured the CONTROL arm's residue-text
  channel further and proposed a CONTROL-text count on the two existing ACCEPTS sessions, which already hold all ten
  accepted CONTROL writes in both latch states.
* **Repair 16** (E7) closes that channel as a CLASS in one diff: every clear the arm makes before its residue test --
  DOG, HARD_RESET, ENDIANESS -- now has a residue-count row in BOTH latch states:
  `ctlrst sw/sd msg` + `ctlrst sw/sd halt` (new sessions, latch CLEAR), `rst 4w/8w msg` (the reset sessions, a 0x0001
  twin first, latch SET at the 0x800), `rearm ctl msg` (latch SET) and `latch ctl msg` (latch CLEAR) on the ACCEPTS
  sessions.  226 rows.  Contract text: the class closure, and a list of the cells deliberately NOT rowed.
* **Table 16** (E10): 25 legs, predictions pre-registered in `PRETABLE16.out` before any build.

## 2. FINDINGS -- attribution, MY DISPOSITION, what I changed

**F1. The HARD_RESET clear skipped is undetected by all 218 rows** -- the dedicated adversarial grok seat; confirmed by the
Fable seat; MEASURED in table 15a.  **DISPOSITION: ACCEPTED, L2** (the ruling's 13/17 conditional on the arm's other
TESTED bit; the Fable seat graded it the same).  **CHANGED:** `ctlrst sw/sd msg` + halt (latch CLEAR) and `rst 4w/8w
msg` (latch SET).  Second consecutive pass finding a residue-of-a-clear cell in this arm -> the repair is the class
closure.

**F2. The ENDIANESS clear skipped is undetected too** -- the main loop; MEASURED in table 15a.  The Fable seat graded it
clause (e) (never tested) with "a text count there is a cheap optional strengthening, not owed".  **DISPOSITION:
ROWED AS THAT STRENGTHENING**, because the Opus seat's ACCEPTS-session counts carry it at no session cost (the two
0x0100 ACCEPTS entries).  **CHANGED:** `rearm ctl msg`, `latch ctl msg`.  See D4.

**F3 / F17. Width x direction x latch at INTSTAT and INTMASK: 8 of 16 cells unexercised** -- glm, kimi-k3:cloud,
deepseek, grok (panel) found the latch-SET 1-byte READ pair; the Opus seat's per-access census found all eight (1R with
the latch SET; 1W, 2R, 2W with it CLEAR) and measured six variants that pass all 218 rows there (`P_ist1r_set`,
`P_imk1r_set`, `C_istW_clr`, `C_ist2_clr`, `C_imkW_clr`, `C_imk2_clr`), with a positive control on a rowed cell
(`C_ist1r_clr`, detected 214/218).  The probe header claimed the whole {1,2} x {R,W} floor at every observable label.
**DISPOSITION (PROPOSED): NOT ROWED, disclosed** -- the decline does not test width within the narrow class nor
direction, so these are joints beyond the ruled floor {label} x {latch SET}; the header's claim is SCOPED ("each cell in
at least one latch state") and the contract names the eight cells.  **Cost if ruled owed: six sessions** (the Opus
seat's estimate).  **A RULE QUESTION -- D2.**

**F4. A clear gated on the width latch is undetected** (glm: the DOG clear; the same shape exists for HARD_RESET).  glm
also showed the contract's reason ("the CONTROL arm reads no latch") described the fixed build, not the space of edits.
**DISPOSITION: ROWED** -- `rearm ctl msg` (DOG, latch SET) and `rst 4w/8w msg` (HARD_RESET, latch SET) now carry both;
the wrong reason is removed from the contract.  **CHANGED:** as above; table 16 measures `L_dogclr` and `L_rstclr`.

**F5. The DOG stop-bit and re-arm shapes are unseen** -- glm, kimi-k3, deepseek.  **DISPOSITION: REJECTED ON THE
EVIDENCE** -- the ACCEPTS sessions (E3) write 0x0200 and continue; a re-arm reds `rearm once`, a stop reds
`rearm surv`/`latch surv`.  agy and grok verified it from the files.  A BRIEF DEFECT: those sessions were not inlined.

**F6. The `tl` rows' s1 should be large on the fixed build** -- deepseek.  **DISPOSITION: REJECTED** -- the 8-byte read
samples `d->reg[...]` before the switch's `crime_update_crime_time(d)`; the base leg measured raw 66/66/132/66 (E5); the
Opus seat measured it from the device side (s1 = 726/792/726/594 in its census run, exactly the tick's value).  See D1.

**F7. The next tick is 16383 steps after the first, not 16384** -- grok (panel).  **ACCEPTED, L4 in the pass-2 brief.**

**F8. Five completion times for four lanes** -- glm.  **REJECTED (explained):** 18 legs in 4 lanes = rounds of 5,5,4,4.

**F9. `said()` not inlined** -- glm, kimi-k3.  **ACCEPTED** -- E4.

**F10. The `tl <op> ctl` note wording** -- glm.  **REJECTED (kept):** verbatim the existing `time <op> ctl` notes.

**F11. agy's summary claimed 20 cells covered** while its matrix showed 3 ops at three labels.  **NOTED** -- that is F3.

**F12. Read the residue VALUE in the twin's text** -- glm; **and the Opus seat measured a variant only a value can see**
(F20).  **DISPOSITION: see F20.**

**F13. `-V -x` start semantics** -- kimi-k3.  **SETTLED** by grok (panel) from the source.

**F14. A latch-CLEAR-only exemption at INTSTAT/INTMASK/CONTROL** -- kimi-k3.  **PARTLY REJECTED, PARTLY F17**: the
single-axis latch-CLEAR cells are rowed (`istat lb`/`imask lb`, `sb08 msg`'s first `sb`, `sh08 run`'s first `sh`), but a
latch-CLEAR exemption keyed on width or direction at INTSTAT/INTMASK is one of F17's eight cells.

**F15. The pass-2 brief's "per label ... all four narrow ops each"** -- glm.  **ACCEPTED, L4 in the pass-2 brief.**

**F16. The fallback draft overstated** -- the Fable seat, on the text written in its name after two refusals.
**ACCEPTED** -- relabelled [NOT A SEAT ANSWER].

**F18. A latch-SET 2-byte CONTROL write with HARD_RESET clear** (`P_ctl2wrc_set`) passes all 218 rows -- the Opus seat;
host text only, and every latch-SET 2-byte write in the probe carries 0x0800.  **DISPOSITION (PROPOSED): disclosed**
(a width x bit joint).  Cheap alternative: one more latch-SET `sh 0x0201` store in the `sh08b` session.  **D5.**

**F19. A refusal at INTSTAT/INTMASK while the interrupt line is ALREADY asserted** (`P_istprev_set`) passes all 218 rows
-- the Opus seat: every row watches the line RISE, none watches it fall; even the plain INTSTAT swap is detected only
through the rise.  **DISPOSITION (PROPOSED): disclosed** (a state x label x latch joint).  **D5.**

**F20. The residue VALUE when the count does not move** (`D_dogbit0`: the DOG clear skipped when bit 0 is set) -- the
Opus seat, measured.  **DISPOSITION (PROPOSED): disclosed**; the alternative, a value-anchored text in the ctldog/ctlrst
rows, costs no session.  **D5.**

**F21. Count rows on the existing ACCEPTS sessions** -- the Opus seat's option.  **ADOPTED** (repair 16), and the same
idea applied to the reset sessions.

**F22. "Exactly ONE CRIME tick per session" is false: stepped sessions see THREE** (two after `quit`, from
`cpu_run_deinit`) -- the Opus seat.  Harmless for every row.  **ACCEPTED, L4** in the pass-2 brief's settled premises.

**F23. PRETABLE14's "DOG -> stop" example (the HARD_RESET test widened to DOG|HARD_RESET) is equivalent** -- DOG is
cleared before that test.  -- the Opus seat.  **ACCEPTED, L4**, recorded in POSTTABLE16 (PRETABLE14 is not edited).

**F24. Two sessions refuse at TIME with the latch set, not one** (the `dog` session too) -- the Opus seat.  Conclusion
unchanged.  **ACCEPTED, L4** in the pass-2 brief.

**F25. The gate pin is three lines** (`gate_arm.sh` 1916, 1921, 1922 all read 204) -- the Opus seat.  **ACCEPTED**: the
pin step moves all three.

## 3. DISAGREEMENTS AND RULE QUESTIONS -- please adjudicate, including your own

**D1 (F6).**  deepseek: s1 should be large.  Everyone else and two measurements: small.  **RULING: small.**  deepseek,
please re-walk it against E5.

**D2 (F3/F17) -- the eight INTSTAT/INTMASK width x direction x latch cells: floor, or disclosed?**  glm: below the
adjudicated floor, but the text claimed them.  kimi-k3: outside the printed enumeration, name them.  grok (panel):
outside this floor.  The Opus seat: "by the ruling's letter clause (e); by the probe's own text owed, or the text is a
wrong record ... the project's own precedent (the F2 2-byte cells) rowed a label x width narrowing rather than
disclosing it."  **MY PROPOSAL: disclosed, with the header's claim scoped** -- which corrects the wrong record without
adding rows.  The Opus seat's precedent point is the strongest argument against me: weigh it.

**D3 (was F4) -- resolved by rows** unless you judge the rows unlicensed (they catch measured variants; E10 shows it).

**D4 (F2) -- ENDIANESS rowed as a strengthening the Fable seat called "not owed".**  Is that licensed (a measured delta:
table 15a, and E10), or scope growth the adjudicator should reject?

**D5 (F18, F19, F20) -- the state- and value-conditioned cells: disclosed, or owed?**  Two have zero-session
alternatives (F18: one store in an existing session; F20: a value-anchored text).

## 3a. WHAT IS STILL OWED, AND WHERE I MIGHT BE FOOLING MYSELF

* **Owed:** codex (GPT-6 Astra) -- the pass-2 seat and a dedicated job -- after its 07:01 reset; then the Fable seat LAST
  and Astra's confirmation; nothing commits before #549 does.
* **Fooling myself, 1:** every rule question I proposed (D2, D5) resolves toward fewer rows, while every cell I DID row
  was cheap.  The measurements are here so that can be checked rather than trusted.
* **Fooling myself, 2:** I grew the repair beyond the one L2 cell (F2, F4, F21).  The warrant is the class-closure
  amendment and measured deltas; an adjudicator may call part of it unlicensed.
* **Fooling myself, 3:** this round's kimi seat is the PACKET-FED substitute (the CLI is 403 on its subscription).

## 4. EVIDENCE, VERBATIM

**E1 -- the CONTROL arm** (`dev_sgi_ip32.c` 8c1d1545, `case CRIME_CONTROL`):

```c
	case CRIME_CONTROL:	/*  0x008  */
		/*  TODO: 64-bit write to CRIME_CONTROL, but some things
		    (such as NetBSD 1.6.2) write to 0x00c!  */
		if (writeflag == MEM_WRITE) {
			/*
			 *  0x200 = watchdog timer (according to NetBSD)
			 *  0x800 = "reboot" used by the IP32 PROM
			 */
			if (idata & CRIME_CONTROL_DOG_ENABLE) {
				idata &= ~CRIME_CONTROL_DOG_ENABLE;
			}
			if (idata & CRIME_CONTROL_HARD_RESET) {
				int j;

				/*  This is used by the IP32 PROM's
				    "reboot" command:  */
				for (j=0; j<cpu->machine->ncpus; j++)
					cpu->machine->cpus[j]->running = 0;

				idata &= ~CRIME_CONTROL_HARD_RESET;
			}

			idata &= ~CRIME_CONTROL_ENDIANESS;

			if (idata != 0)
				fatal("[ CRIME_CONTROL: unimplemented "
				    "control 0x%016llx ]\n", (long long)idata);
		}
		break;

```

**E2 -- the INTSTAT/INTMASK session and its first four rows** (every 1-byte read at +0x10/+0x18 in the probe is the `lb' here -- the session's FIRST refusal -- or a free-running announce session's only refusal):

```python
for lbl, off in (("imask", 0x18), ("istat", 0x10)):
    A = Addr(CODE)
    c = []
    x, _ = st(A, "sd", CRIME + 0x18, BIT); c += x
    x, _ = st(A, "sd", CRIME + 0x20, BIT); c += x
    c += ["print cause"]
    x, _ = ld(A, "lb", CRIME + off, "a0"); c += x
    c += ["print cause"]
    x, _ = st(A, "sb", CRIME + off, 0xff); c += x
    c += ["print cause"]
    x, _ = ld(A, "lh", CRIME + off, "a1"); c += x
    c += ["print cause"]
    x, _ = st(A, "sh", CRIME + off, 0xffff); c += x
    c += ["print cause"]
    x, _ = ld(A, "lw", CRIME + off, "v0"); c += x
    c += ["print cause", "print a0", "print a1"]
    #  INTMASK read back by an accepted ld after the refused stores (kimi CLI, second closing pass: a landing that ORs
    #  into INTMASK keeps bit 28, so the reassert rows cannot see it), then a follow-up refusal at ANOTHER label (codex:
    #  a latch keyed on this one label is invisible to a session that refuses only here)
    x, _ = ld(A, "ld", CRIME + 0x18, "s2"); c += x
    x, _ = ld(A, "lb", CRIME + 0x07, "t1"); c += x
    c += ["print s2"]
    t, clean = session(c)
    row("%s pre" % lbl, ip2(nth(t, "cause", 0)), "clear", "IP2 low after SOFTINT's default-arm store")
    row("%s lb" % lbl, ip2(nth(t, "cause", 1)), "clear", "refused lb +0x%x: no reassert" % off)
    row("%s sb" % lbl, ip2(nth(t, "cause", 2)), "clear", "refused sb +0x%x: no reassert" % off)
    row("%s lh" % lbl, ip2(nth(t, "cause", 3)), "clear", "refused lh +0x%x: no reassert" % off)
```

**E3 -- ACCEPTS, the re-arm session (each accepted entry followed by a refusal -- so entries after the first run with the latch SET), and the latch session (every entry BEFORE the first refusal -- latch CLEAR)**:

```python
ACCEPTS = (("sd", 0x00, 0), ("ld", 0x00, 0), ("sw", 0x00, 0), ("lw", 0x00, 0),
           ("lwP", 0x00, 0), ("swP", 0x00, 0), ("sdP", 0x00, 0),
           ("lw", 0x08, 0), ("ld", 0x08, 0),
           ("sw", 0x08, 0x0201), ("sw", 0x08, 0x0001), ("sw", 0x08, 0), ("sw", 0x08, 0x0200),
           ("sd", 0x08, 0x0201), ("sd", 0x08, 0x0001), ("sd", 0x08, 0), ("sd", 0x08, 0x0200),
           ("sd", 0x10, 0), ("ld", 0x10, 0), ("sw", 0x10, 0), ("lw", 0x10, 0),
           ("sd", 0x18, 0), ("ld", 0x18, 0), ("sw", 0x18, 0), ("lw", 0x18, 0),
           ("sd", 0x30, 0), ("ld", 0x30, 0), ("sw", 0x30, 0), ("lw", 0x30, 0),
           ("sd", 0x38, 0), ("ld", 0x38, 0), ("sw", 0x38, 0), ("lw", 0x38, 0),
           ("sd", 0x40, 0), ("ld", 0x40, 0), ("sw", 0x40, 0), ("lw", 0x40, 0),
           ("sw", 0x34, 0x0badcafe), ("lw", 0x34, 0), ("sw", 0x04, 0), ("lw", 0x04, 0),
           ("ldP", 0x00, 0), ("sw", 0x08, 0x0100), ("sd", 0x08, 0x0100),
           ("sd", 0x278, 0), ("ld", 0x278, 0))
KINDS = ACCEPTS

...
for op, off, val in KINDS:
    c += accept(A, op, off, val)
    x, _ = ld(A, "lb", CRIME + 0x06, "v0"); c += x
t, clean = session(c + roundtrip(A))
row("rearm once", count(t, "-- declined.", clean), 1, "%d refusals, %d accepted kinds between: one notice"
    % (len(KINDS) + 1, len(KINDS)))
row("rearm surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "the whole interleave completes (a RAM trip)")

...
# ---- the latch: five refused accesses, one session, exactly one announce ----
A = Addr(CODE)
c = ["ra=0x%x" % RA]
#  PROLOGUE (the Opus closing seat): accepted accesses BEFORE the first refusal -- a notice PRE-SILENCED by an accepted
#  access (`d->warned |= CRIME_W_LEN;' in an accept arm, `pre4') shows as zero notices; and an accepted CONTROL write
#  whose unmodelled bit prints the CONTROL text, so a future second latch on THAT message reusing bit 0 (`ctl_collide')
#  shows the same way.  CLOSED OVER EVERY ARM AND EVERY BRANCH an accepted access can take and come back from (glm,
#  second closing pass: the REV arm; codex, grok, kimi, third closing pass: CONTROL's DOG_ENABLE branch -- the 0x01 write
#  here skipped it -- the REV redirect branch, and the INTSTAT case alone -- each reached only AFTER some session's
#  first refusal, where a pre-set is invisible):
#      CONTROL  sw 0x0201 (DOG set, leftover nonzero), sw 0x0001 (DOG clear, leftover nonzero), sw 0 (DOG clear,
#               leftover zero), lw (CONTROL's read side) -- the Opus third-closing seat, measured: a pre-set on the
#               read side, and (by reading) on the zero-leftover side, passed; HARD_RESET is disclosed (it stops the CPUs)
#      REV      lw from the PROM-probe window (the redirect branch) AND from ordinary code (the branch not taken)
#      INTSTAT, INTMASK   lw +0x10, lw +0x18        DOG  ld +0x30        TIME  ld +0x38
#      default  sw/lw +0x34 (4-byte, low lane), sd +0x278 (8-byte, far block)
#  *** Since the fourth closing pass the prologue IS the re-arm list, ACCEPTS (the kind x label cross): the Opus seat
#  measured a pre-set on an accepted 8-byte WRITE at +0x10, and one on CONTROL's 0x0200 cell, each 131/131. ***
for op, off, val in ACCEPTS:
    c += accept(A, op, off, val, reg="a2")
#  lh FIRST (Opus seat, F2): a latch whose bit is taken from the access -- `d->warned |= len' or `|= relative_addr' --
#  sets bit 0 only for a 1-byte access or an odd address, so the lh at +0x06 would leave it clear and the lb after it
#  would announce again.  With lb first, both shapes passed.
for op, off in (("lh", 6), ("lb", 7), ("lbu", 0x3f)):
    x, _ = ld(A, op, CRIME + off, "v0"); c += x
for op, off, val in (("sb", 0x37, 0xab), ("sh", 0x36, 0xabcd)):
    x, _ = st(A, op, CRIME + off, val); c += x
#  and refusals at CRIME_REV and CRIME_TIME AFTER the latch is set (the Opus third-closing seat, measured: a latch TEST
#  that lets one label through -- `|| relative_addr == CRIME_REV' -- passed, because REV and TIME were each refused only
#  once per session, first; every other label is refused again after the latch is set somewhere)
for off in (0x00, 0x38):
    x, _ = ld(A, "lb", CRIME + off, "v0"); c += x
t, clean = session(c + roundtrip(A))
row("latch x5", count(t, "-- declined.", clean), 1, "5 refused accesses, then +0x00, +0x38 -> one (once)")
row("latch surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives all five")
```

**E4 -- `said()`**:

```python
def said(t, ln, off, clean):
    """the whole announce, `(once)' marker included -- a reworded or unmarked announce reads 0"""
    return count(t, "unimplemented len=%d at 0x%x -- declined.  (once) ]" % (ln, off), clean)


```

**E5 -- the TIME rows on table 14's base leg (raw values; SMALL = 6,600,000)**:

```
time lb          small                small                after refused lb +0x38 (raw 66)          ok
time lb ctl      large                large                CONTROL: accepted ld moved TIME (raw 286786632) ok
time lb v0       0x0                  0x0                  refused lb +0x38 answers 0               ok
time once        1                    1                    first refusal at CRIME_TIME, then +0x07: one notice ok
time said        1                    1                    lb +0x38 (first refusal): its own announce ok
time sb          small                small                after refused sb +0x38 (raw 198)         ok
time sb ctl      large                large                CONTROL: accepted ld moved TIME (raw 286525140) ok
time lh          small                small                after refused lh +0x38 (raw 0)           ok
time lh ctl      large                large                CONTROL: accepted ld moved TIME (raw 286087428) ok
time lh v0       0x0                  0x0                  refused lh +0x38 answers 0               ok
time sh          small                small                after refused sh +0x38 (raw 66)          ok
time sh ctl      large                large                CONTROL: accepted ld moved TIME (raw 284334402) ok
tl lb            small                small                latch SET, refused lb +0x38: no clock step (raw 66) ok
tl lb ctl        large                large                CONTROL: accepted ld moved TIME (raw 426778572) ok
tl sb            small                small                latch SET, refused sb +0x38: no clock step (raw 66) ok
tl sb ctl        large                large                CONTROL: accepted ld moved TIME (raw 426521568) ok
tl lh            small                small                latch SET, refused lh +0x38: no clock step (raw 132) ok
tl lh ctl        large                large                CONTROL: accepted ld moved TIME (raw 426847080) ok
tl sh            small                small                latch SET, refused sh +0x38: no clock step (raw 66) ok
tl sh ctl        large                large                CONTROL: accepted ld moved TIME (raw 426933738) ok
time sd lb v0    0x0                  0x0                  refused lb at CRIME_TIME (seeded odd) answers 0 ok
time sd lh v0    0x0                  0x0                  refused lh at CRIME_TIME (seeded odd) answers 0 ok
```

**E6 -- every session holding an accepted 0x800 write before repair 16** (`sw08 halts', and `rst 4w'/`rst 8w' via `rst_session'):

```python
x, _ = st(A, "sw", CRIME + 0x08, 0x0800)
t, clean = session(x + AFTER + roundtrip(A))
row("sw08 halts", pr(t, "v1"), "0x%x" % SENT, "CONTROL: sw 0x800 +0x08 stops CPUs (crimectllane)")

...
def rst_session(op):
    """a refused lb sets the latch; then an accepted `op' of 0x800 at CONTROL stops every CPU (or does not).  #529
    repair 16: an accepted `op' of 0x0001 runs FIRST, with the latch CLEAR -- one CONTROL text, the text channel's
    in-session liveness half -- and the CONTROL-text count is returned: the 0x800 write's residue, latch SET."""
    A = Addr(CODE)
    c = []
    if op is not None:
        x, _ = st(A, op, CRIME + 0x08, 0x0001)
        c += x
    x, _ = ld(A, "lb", CRIME + 0x07, "v0")
    c += x
    if op is not None:
        x, _ = st(A, op, CRIME + 0x08, 0x800)
        c += x
    c += roundtrip(A)
    t, clean = session(c)
    return (pr(t, "v1"), (t.count("-- declined.") if clean else "unclean"),
            count(t, "CRIME_CONTROL: unimplemented", clean))


_rv, _rn, _rm = rst_session(None)
row("rst alive", _rv, "0x%x" % LIVE_VAL,
    "CONTROL: with NO 0x800 write the RAM round trip completes -- the halt oracle is live, not stuck")
row("rst alive once", _rn, 1, "CONTROL: the control session refused exactly once")
for _op, _w in (("sw", 4), ("sd", 8)):
    _rv, _rn, _rm = rst_session(_op)
    row("rst %dw" % _w, _rv, "0x%x" % SENT,
        "*** accepted %s 0x800 at CONTROL with the latch SET stops every CPU: the round trip after it does "
        "not run, so v1 keeps the SENTINEL (absent would mean the HOST died -- a different outcome) ***"
```

**E7 -- REPAIR 16, the whole diff** (probe f5e915f6 -> 1534bc9e):

```diff
--- /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/table14_20260926/crime_width_probe.table14.py	2026-09-26 00:27:18.403660000 -0500
+++ /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/table16_20260926/crime_width_probe.table16.py	2026-09-26 03:53:15.817624200 -0500
@@ -49,7 +49,9 @@
      The INTSTAT/INTMASK/TIME rows came from the pass-2 Opus seat, which MEASURED a decline narrowed to skip those
      labels passing the 40-row version of this detector 40/40 (opus_pass2_20260913/OPUS_REPORT.md); their 2-byte cells
      from the F2 pass (grok, glm): `len != 2 || relative_addr != CRIME_INTSTAT' passed the 71-row version.  So every
-     observable label carries the whole {1,2} x {R,W} refusal floor (CONTROL's reads and DOG have no body: below).
+     observable label carries the whole {1,2} x {R,W} refusal floor, each cell in at least ONE latch state (CONTROL's
+     reads and DOG have no body: below).  [Crossed with the latch state, INTSTAT and INTMASK exercise 4 of their 8
+     cells each -- see the contract block (#529 repair 16; the Opus seat, repair 15's pass 2).]
      *** THE sh08 AND sw08 CHANNELS EXIST BECAUSE OF A SEPARATE DEFECT, `crimectllane' (filed): the switch matches
      CRIME_CONTROL by its exact label 0x08 and reads the RAW idata, so a 32-bit write to the high half, or a halfword at
      +0x08, carries bit 11 into HARD_RESET, while NetBSD's +0x0c write does nothing.  A round that fixes that lane
@@ -349,8 +351,20 @@
   prints, and the prelude re-forces the register at every access, so the CONTROL text COUNT is the cell's one
   observable -- and no row read it in a session holding that write.  `ctldog sw msg'/`ctldog sd msg' are the pair
   (D_nodogclear, the DOG branch's clear deleted; table14_20260926/).  A SILENT decline of the DOG-only write
-  changes nothing any access can see: EQUIVALENT, disclosed.  The latch x DOG joint is clause (e): the CONTROL
-  arm reads no latch. ***
+  changes nothing any access can see: EQUIVALENT, disclosed.
+  REPAIR 16 (2026-09-26) CLOSES THE CONTROL ARM'S RESIDUE-TEXT CHANNEL AS A CLASS: every clear the arm makes before
+  its residue test (DOG 0x200, HARD_RESET 0x800, ENDIANESS 0x100) has a residue-count row in BOTH latch states --
+  DOG: `ctldog sw/sd msg' and `latch ctl msg' (CLEAR), `rearm ctl msg' (SET); HARD_RESET: `ctlrst sw/sd msg'
+  (CLEAR), `rst 4w/8w msg' (SET); ENDIANESS: `latch ctl msg' (CLEAR), `rearm ctl msg' (SET) -- and each TESTED bit
+  keeps its side-effect rows (DOG's stop and re-arm shapes: `rearm surv', `latch surv', `rearm once'; HARD_RESET's
+  stop: `sw08 halts', `rst 4w', `rst 8w', `ctlrst sw/sd halt').  Measured in table15a_20260926/ and
+  table16_20260926/.  NOT ROWED, disclosed as clause (e), each measured by the Opus seat on repair 15's pass 2
+  (opus_r15p2_20260926/): the residue VALUE when the count does not move (a DOG clear skipped when bit 0 is set);
+  a latch-SET 2-byte CONTROL write with HARD_RESET clear (host text only; every latch-SET 2-byte write here carries
+  0x0800); at INTSTAT and INTMASK, the width x direction x latch-state joints no session reaches (1R with the latch
+  SET; 1W, 2R, 2W with it CLEAR -- the decline tests neither width within the narrow class nor direction); and a
+  refusal at INTSTAT/INTMASK while the interrupt line is ALREADY asserted (every row here watches the line rise).
+  Whether those are floor is a question put to the adjudicators with these measurements. ***
 
 DISCLOSED, not rowed:
   * `goto crime_declined' -> `return 1' is EQUIVALENT on every channel: memory_rw pre-zeroes a device read buffer
@@ -893,9 +907,11 @@
 #  CHANNELS: TIME -- crime_update_crime_time() at the refused access moves the next sample by the wall-clock since
 #  the last update (large vs SMALL: the `time' rows' channel, and their disclosed tick assumption; the extra +0x07
 #  access adds debugger steps, never a TIME update, on a fix build); REV -- the arm's PROM-window hack redirects the
-#  pc to ra (the `rev pc' rows' channel).  All four narrow ops at each label, as repair 14's ruling said: the
-#  decline block tests neither width nor direction, and the four are the width x direction cells a leak keyed on
-#  either could use.
+#  pc to ra (the `rev pc' rows' channel).  All four narrow ops at each label because repair 14's ruling C asked for
+#  them -- a STRENGTHENING over the floor, which is {label} x {latch SET}: the decline block tests neither width
+#  within the narrow class nor direction.  (INTSTAT and INTMASK do not have all four in both latch states: see the
+#  contract block.  This said "the four are the width x direction cells a leak keyed on either could use" --
+#  repair 15's pass 2, four seats.)
 for op in ("lb", "sb", "lh", "sh"):
     A = Addr(CODE)
     c = []
@@ -940,6 +956,22 @@
     row("ctldog %s msg" % op, count(t, "CRIME_CONTROL: unimplemented", clean), 1,
         "%s 0x0200 then 0x0201 +0x08: ONE CONTROL text, the twin's" % op)
 
+# ---- #529 REPAIR 16: HARD_RESET's residue with the latch CLEAR (repair 15's pass 2) ----
+#  An accepted `sw'/`sd +0x08 = 0x0800' stops every CPU, and because the branch clears HARD_RESET before the residue
+#  test it prints nothing.  No row counted the CONTROL text in a session holding an accepted 0x0800 write, so a build
+#  that skipped that clear passed every row while the CPUs still stopped (table15a_20260926/).  The halt ends the
+#  guest's work, so the twin comes FIRST: 0x0001 (residue 0x1, one text), then 0x0800 as the session's last store.
+#  CHANNELS: the text count -- ONE on the fixed build, TWO if the clear is skipped -- and the halt: v1 left at the
+#  sentinel by the RAM trip that cannot run, which shows the 0x0800 write reached the arm.
+for op in ("sw", "sd"):
+    A = Addr(CODE)
+    x, _ = st(A, op, CRIME + 0x08, 0x0001)
+    y, _ = st(A, op, CRIME + 0x08, 0x0800)
+    t, clean = session(x + y + AFTER + roundtrip(A))
+    row("ctlrst %s msg" % op, count(t, "CRIME_CONTROL: unimplemented", clean), 1,
+        "%s 0x0001 then 0x0800 +0x08: ONE CONTROL text, the twin's" % op)
+    row("ctlrst %s halt" % op, pr(t, "v1"), "0x%x" % SENT, "%s 0x0800 +0x08 after the twin: CPUs stopped" % op)
+
 # ---- a refused store leaves the register it names untouched (CRIME_DOG seeded by an accepted sd) ----
 A = Addr(CODE)
 c = []
@@ -1050,6 +1082,12 @@
 row("rearm once", count(t, "-- declined.", clean), 1, "%d refusals, %d accepted kinds between: one notice"
     % (len(KINDS) + 1, len(KINDS)))
 row("rearm surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "the whole interleave completes (a RAM trip)")
+#  #529 repair 16: ACCEPTS holds ten accepted CONTROL writes -- 0x0201, 0x0001, 0, 0x0200, 0x0100 at both widths -- and
+#  here every one after the first entry runs with the latch SET.  The fixed build prints for the four with a nonzero
+#  residue (0x0201 and 0x0001, both widths).  A clear skipped for DOG or ENDIANESS adds texts; a latch-SET accepted
+#  write wrongly declined removes them.  (The Opus seat's option on repair 15's pass 2, replay-measured 4 on base.)
+row("rearm ctl msg", count(t, "CRIME_CONTROL: unimplemented", clean), 4,
+    "ten accepted CONTROL writes, latch SET: four print (0x0201, 0x0001 at both widths)")
 
 # ---- ACCEPT cells at the window's LAST 8-byte slot (+0x278; no case label, no prelude write) -- the far bound ----
 A = Addr(CODE)
@@ -1248,6 +1286,9 @@
 t, clean = session(c + roundtrip(A))
 row("latch x5", count(t, "-- declined.", clean), 1, "5 refused accesses, then +0x00, +0x38 -> one (once)")
 row("latch surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives all five")
+#  #529 repair 16: the same ten accepted CONTROL writes, here all BEFORE the first refusal -- latch CLEAR.
+row("latch ctl msg", count(t, "CRIME_CONTROL: unimplemented", clean), 4,
+    "ten accepted CONTROL writes, latch CLEAR: four print (0x0201, 0x0001 at both widths)")
 #  REPAIR 12 (closing pass 6; flagship ruling regress/artifacts/lcaisalane/FABLE_C4_RULING_20260915.md, part A): the two
 #  rows ACCEPTS feeds COUNT notices, so an ACCEPTED cell wrongly declined -- an accept guard GROWN by one conjunct, the
 #  de-escalation clause's own shape -- takes the session's one notice itself and the count stays 1: codex's C1 (CONTROL
@@ -1585,28 +1626,37 @@
 #  MEASURED BEFORE TRANSPLANTING (opus_close8_20260916/scripts/ctlreset.py): base 6/6; K_ctl4w_reset_post
 #  5/6 on its 4-byte row; K_ctl8w_reset_post 5/6 on its 8-byte row; G_glm_tim4clear 6/6 OFF-CELL.
 def rst_session(op):
-    """a refused lb sets the latch; then an accepted `op' of 0x800 at CONTROL stops every CPU (or does not)"""
+    """a refused lb sets the latch; then an accepted `op' of 0x800 at CONTROL stops every CPU (or does not).  #529
+    repair 16: an accepted `op' of 0x0001 runs FIRST, with the latch CLEAR -- one CONTROL text, the text channel's
+    in-session liveness half -- and the CONTROL-text count is returned: the 0x800 write's residue, latch SET."""
     A = Addr(CODE)
-    c, _ = ld(A, "lb", CRIME + 0x07, "v0")
+    c = []
+    if op is not None:
+        x, _ = st(A, op, CRIME + 0x08, 0x0001)
+        c += x
+    x, _ = ld(A, "lb", CRIME + 0x07, "v0")
+    c += x
     if op is not None:
         x, _ = st(A, op, CRIME + 0x08, 0x800)
         c += x
     c += roundtrip(A)
     t, clean = session(c)
-    return pr(t, "v1"), (t.count("-- declined.") if clean else "unclean")
+    return (pr(t, "v1"), (t.count("-- declined.") if clean else "unclean"),
+            count(t, "CRIME_CONTROL: unimplemented", clean))
 
 
-_rv, _rn = rst_session(None)
+_rv, _rn, _rm = rst_session(None)
 row("rst alive", _rv, "0x%x" % LIVE_VAL,
     "CONTROL: with NO 0x800 write the RAM round trip completes -- the halt oracle is live, not stuck")
 row("rst alive once", _rn, 1, "CONTROL: the control session refused exactly once")
 for _op, _w in (("sw", 4), ("sd", 8)):
-    _rv, _rn = rst_session(_op)
+    _rv, _rn, _rm = rst_session(_op)
     row("rst %dw" % _w, _rv, "0x%x" % SENT,
         "*** accepted %s 0x800 at CONTROL with the latch SET stops every CPU: the round trip after it does "
         "not run, so v1 keeps the SENTINEL (absent would mean the HOST died -- a different outcome) ***"
         % _op)
     row("rst %dw once" % _w, _rn, 1, "CONTROL: exactly one refusal announced in this session")
+    row("rst %dw msg" % _w, _rm, 1, "twin 0x0001 then, latch SET, 0x800: ONE CONTROL text, the twin's")
 
 # ---- P6: the remaining post-latch ACCEPT cells that carry a value, plus the two EXTRA accesses
 #      (DOG 4W high, the +0x04 write line). ----
```

**E8 -- the new mutants, verbatim** (`table16_20260926/mutants_16.py`, applied to 8c1d1545):

```python
if name == "base":
    pass
elif name == "H_noresetclear":
    sub(RST_CLEAR, "\t\t\t\t\tcpu->machine->cpus[j]->running = 0;\n\n\t\t\t}\n")
elif name == "E_noendianclear":
    sub("\t\t\tidata &= ~CRIME_CONTROL_ENDIANESS;\n\n\t\t\tif (idata != 0)\n", "\t\t\tif (idata != 0)\n")
elif name == "W_istlb":
    latch_cell("relative_addr == CRIME_INTSTAT && len == 1 && writeflag == MEM_READ")
elif name == "W_imklb":
    latch_cell("relative_addr == CRIME_INTMASK && len == 1 && writeflag == MEM_READ")
elif name == "L_dogclr":
    sub(DOG_CLEAR,
        ("\t\t\tif (idata & CRIME_CONTROL_DOG_ENABLE) {\n"
         "\t\t\t\tif (!(d->warned & CRIME_W_LEN))\n"
         "\t\t\t\t\tidata &= ~CRIME_CONTROL_DOG_ENABLE;\n"
         "\t\t\t}\n"))
elif name == "L_rstclr":
    sub(RST_CLEAR,
        ("\t\t\t\t\tcpu->machine->cpus[j]->running = 0;\n"
         "\n"
         "\t\t\t\tif (!(d->warned & CRIME_W_LEN))\n"
         "\t\t\t\t\tidata &= ~CRIME_CONTROL_HARD_RESET;\n"
         "\t\t\t}\n"))
elif name == "S_rst8clr":
    #  the CHANNEL check for the new `ctlrst sd halt' row: an ACCEPTED 8-byte 0x800 write with the latch CLEAR no longer
    #  stops the CPUs (the dedicated grok seat named this cell "real, and unrowed").  `sw08 halts' is 4-byte and `rst 8w'
    #  runs with the latch SET, so only the new row can see it.
    sub("\t\t\t\tfor (j=0; j<cpu->machine->ncpus; j++)\n"
        "\t\t\t\t\tcpu->machine->cpus[j]->running = 0;\n",
        "\t\t\t\tif (!(len == 8 && !(d->warned & CRIME_W_LEN)))\n"
        "\t\t\t\tfor (j=0; j<cpu->machine->ncpus; j++)\n"
        "\t\t\t\t\tcpu->machine->cpus[j]->running = 0;\n")
```

**E9 -- table 15a** (the 218-row repair-15 probe against the HARD_RESET and ENDIANESS clears):

```
H_noresetclear     OK       exact -- ESCAPE CONFIRMED (218/218)
E_noendianclear    OK       exact -- ESCAPE CONFIRMED (218/218)
CHECK15A_PASS
```

**E10 -- table 16** (repair 16's 222-row probe; 25 legs; predictions pre-registered in PRETABLE16.out):

```
base CRIMEP_RESULT=226/226 CRIMEP_CONTROL=OK done=1 FAILING:  04:15:01
G_lane_ctl CRIMEP_RESULT=225/226 CRIMEP_CONTROL=OK done=1 FAILING: p acc ctl4r 04:35:35
M3_timelatch CRIMEP_RESULT=222/226 CRIMEP_CONTROL=OK done=1 FAILING: tl lb, tl sb, tl lh, tl sh 04:56:11
M7_intmasklatch CRIMEP_RESULT=223/226 CRIMEP_CONTROL=OK done=1 FAILING: imask sb, imask lh, imask sh 05:16:46
E_noendianclear CRIMEP_RESULT=224/226 CRIMEP_CONTROL=OK done=1 FAILING: rearm ctl msg, latch ctl msg 05:37:22
G_glm_tim4clear CRIMEP_RESULT=224/226 CRIMEP_CONTROL=OK done=1 FAILING: c t4w gap, c t4r gap 04:15:01
K_ctl4w_reset_post CRIMEP_RESULT=225/226 CRIMEP_CONTROL=OK done=1 FAILING: rst 4w 04:35:35
M4_timeplain CRIMEP_RESULT=218/226 CRIMEP_CONTROL=OK done=1 FAILING: time lb, time sb, time lh, time sh, tl lb, tl sb, tl lh, tl sh 04:56:11
M8_ctllatch CRIMEP_RESULT=223/226 CRIMEP_CONTROL=OK done=1 FAILING: sb08 msg, sh08b run, gate run 05:16:46
W_istlb CRIMEP_RESULT=226/226 CRIMEP_CONTROL=OK done=1 FAILING:  05:37:22
G_clr_ist4r CRIMEP_RESULT=225/226 CRIMEP_CONTROL=OK done=1 FAILING: acc istat lw 04:15:01
K_ctl8w_reset_post CRIMEP_RESULT=225/226 CRIMEP_CONTROL=OK done=1 FAILING: rst 8w 04:35:35
M5_revlatch CRIMEP_RESULT=222/226 CRIMEP_CONTROL=OK done=1 FAILING: rl lb pc, rl lh pc, rl sb pc, rl sh pc 04:56:11
D_nodogclear CRIMEP_RESULT=222/226 CRIMEP_CONTROL=OK done=1 FAILING: ctldog sw msg, ctldog sd msg, rearm ctl msg, latch ctl msg 05:16:46
W_imklb CRIMEP_RESULT=226/226 CRIMEP_CONTROL=OK done=1 FAILING:  05:37:22
G_clr_ctl4r CRIMEP_RESULT=226/226 CRIMEP_CONTROL=OK done=1 FAILING:  04:15:01
M1_gotolatch CRIMEP_RESULT=208/226 CRIMEP_CONTROL=OK done=1 FAILING: sb08 msg, sh08b run, imask sb, imask lh, imask sh, istat sb, istat lh, istat sh, gate run, tl lb, tl sb, tl lh, tl sh, rl lb pc, rl lh pc, rl sb pc, rl sh pc, mid nodflt 04:35:35
M6_istlatch CRIMEP_RESULT=223/226 CRIMEP_CONTROL=OK done=1 FAILING: istat sb, istat lh, istat sh 04:56:11
H_noresetclear CRIMEP_RESULT=222/226 CRIMEP_CONTROL=OK done=1 FAILING: ctlrst sw msg, ctlrst sd msg, rst 4w msg, rst 8w msg 05:16:46
L_dogclr CRIMEP_RESULT=225/226 CRIMEP_CONTROL=OK done=1 FAILING: rearm ctl msg 05:37:22
G_clr_imk4r CRIMEP_RESULT=225/226 CRIMEP_CONTROL=FAIL done=1 FAILING: gate line 04:15:01
M2_ld278clr CRIMEP_RESULT=225/226 CRIMEP_CONTROL=OK done=1 FAILING: top8 clear 04:35:35
W_ctl8w CRIMEP_RESULT=223/226 CRIMEP_CONTROL=OK done=1 FAILING: rearm ctl msg, p acc ctl msg, rst 8w 04:56:11
S_rst8clr CRIMEP_RESULT=225/226 CRIMEP_CONTROL=OK done=1 FAILING: ctlrst sd halt 05:16:46
L_rstclr CRIMEP_RESULT=224/226 CRIMEP_CONTROL=OK done=1 FAILING: rst 4w msg, rst 8w msg 05:37:22

leg                  score      reds  control  verdict
base                 226/226       0  OK       exact
G_glm_tim4clear      224/226       2  OK       exact
G_clr_ist4r          225/226       1  OK       exact
G_clr_ctl4r          226/226       0  OK       exact (escape, as predicted)
G_clr_imk4r          225/226       1  FAIL     exact
G_lane_ctl           225/226       1  OK       exact
K_ctl4w_reset_post   225/226       1  OK       exact
K_ctl8w_reset_post   225/226       1  OK       exact
M1_gotolatch         208/226      18  OK       exact
M2_ld278clr          225/226       1  OK       exact
M3_timelatch         222/226       4  OK       exact
M4_timeplain         218/226       8  OK       exact
M5_revlatch          222/226       4  OK       exact
M6_istlatch          223/226       3  OK       exact
W_ctl8w              223/226       3  OK       exact
M7_intmasklatch      223/226       3  OK       exact
M8_ctllatch          223/226       3  OK       exact
D_nodogclear         222/226       4  OK       exact
H_noresetclear       222/226       4  OK       exact
S_rst8clr            225/226       1  OK       exact
E_noendianclear      224/226       2  OK       exact
W_istlb              226/226       0  OK       exact (escape, as predicted)
W_imklb              226/226       0  OK       exact (escape, as predicted)
L_dogclr             225/226       1  OK       exact
L_rstclr             224/226       2  OK       exact

CHECK16_PASS
```

## 5. THE SEATS' OWN WORDS, where a finding turns on them

**The dedicated adversarial grok seat** (`grok_dedicated_r15p2.txt`, verbatim):

```
I'll read the pass-2 brief in full first, then try to find the smallest `DEVICE_ACCESS(crime)` edit the 218-row probe would miss.The brief is in. Next I’ll check the device function and the 218-row probe against the source, and look for a decline or CONTROL edit those rows would still pass.The DOG and HARD_RESET arms are the likely gap. I’ll trace which accepted CONTROL writes the 218 rows actually observe, and whether `running = 0` can hide inside a `step`.**BREAK FOUND.** Delete one line in the `HARD_RESET` arm, `idata &= ~CRIME_CONTROL_HARD_RESET;`. An accepted `0x800` write still stops every CPU and now also prints the unimplemented-control line. All 218 rows stay green.

## The edit

In `DEVICE_ACCESS(crime)`, inside `case CRIME_CONTROL` (`GXEMUL-SEC/src/devices/dev_sgi_ip32.c`, the `CRIME_CONTROL_HARD_RESET` block):

```c
if (idata & CRIME_CONTROL_HARD_RESET) {
    int j;
    for (j=0; j<cpu->machine->ncpus; j++)
        cpu->machine->cpus[j]->running = 0;
    /* delete this line: */
    idata &= ~CRIME_CONTROL_HARD_RESET;
}
idata &= ~CRIME_CONTROL_ENDIANESS;
if (idata != 0)
    fatal("[ CRIME_CONTROL: unimplemented control 0x%016llx ]\n", ...);
```

It compiles: that statement is the only use of the cleared bit. `0x800` still takes the stop loop. After the deleted clear, `idata` is still `0x800`, the endian mask does not touch it, and `idata != 0` prints.

Rows that change: none.

## Why the halt rows stay green

Those are the only sessions that perform an accepted `0x800` write. None of them counts `CRIME_CONTROL: unimplemented`.

`sw08 halts` (latch clear, `sw`). The store runs, sets `running = 0`, and now prints. `fatal()` returns, so the process stays up. The later `print v1` is a debugger command. `roundtrip()` does `v1=0xdeadbeef` and then a `lw` that `machine_run` never issues, because `running` is already 0. `v1` stays `0xdeadbeef`. The row wants that sentinel. Green.

`rst 4w` / `rst 8w` (latch set). The opening `lb +0x07` still declines once and does not stop the CPU. The following `sw`/`sd` of `0x800` still stops it and now prints. `rst 4w` and `rst 8w` want `v1 == 0xdeadbeef`. Green. `rst 4w once` and `rst 8w once` count `-- declined.`; the new line is `unimplemented control`, which does not contain that string. Count stays 1. Green.

`rst alive` never writes `0x800`, so it never reaches the deleted statement.

## Why every text-count row stays green

Each of these sessions writes some other value, so the deleted clear does not run:

- `ctldog sw msg` and `ctldog sd msg` write `0x0200` then `0x0201`. No reset bit. The dog clear still silences `0x0200`; `0x0201` still prints once. Count stays 1.
- `p acc ctl msg` writes `0x01`, `0x0001`, `0x0201`, `0x0201`. Count stays 4.
- `sw08 msg ctl` and `acc ctl sd` write `0x01`. Count stays 1.
- `sb08 msg` and `sh08b msg` are narrow stores. They take the `goto` and never enter the arm. Count stays 0.
- `sh08 run`, `sh08b run`, and `gate run` are the same narrow path, so the CPUs still run and the RAM trip still returns `0x12345678`.

`rearm once` and `latch x5` never write `0x800` (a reset write cannot be followed by another access). Their `-- declined.` counts do not move.

## What else was swept

These stay caught, so they are not the break:

- Whole-label latch-set fall-through at `TIME`, `REV`, `INTSTAT`, `INTMASK`, and `CONTROL` (`tl *`, `rl * pc`, `istat sb/lh/sh`, `imask sb/lh/sh`, `sb08 msg`, `sh08b run`, `gate run`).
- `D_nodogclear`, dog-as-stop, and "dog suppresses the leftover print": `ctldog` goes to 0 or 2, or `rearm surv` / `latch said` dies because `0x0200` stops the CPU.
- A width-latch re-arm inside the dog branch: `rearm once` sees a second `-- declined.`
- Latch-clear `sd 0x800` that does not stop: real, and unrowed, but it is a new `len`/`warned` conjunct the arm does not test. The one-line delete needs no new conjunct.

The open cell is the residue half of a bit the arm does test. Dog's clear was given `ctldog` because silence is its only effect. Reset's clear does two things, and the rows that write `0x800` read only the stop.
```

**The Fable seat** (`fable5_r15p2.md`, verified claude-fable-5-1, verbatim):

```
# Fable 5.1 (claude-fable-5-1) — #529 crimewidthkill repair 15, PASS 2 — short review, my own words

FABLE5_R15P2_ALIVE_0926 — CHECKPOINT.md line 1: `# CHECKPOINT -- 2026-09-26 00:35 (087a90 sections rewritten; the peer's sections below are untouched)`

**VERDICT: DO NOT CLOSE. Repair 15's rows and table 14 are sound and exact, but one DERIVED floor escape (delete `idata &= ~CRIME_CONTROL_HARD_RESET;`) is graded L2 like its DOG twin — build it, add the pair in-round, pass-2 the repair; the ENDIANESS clear is clause (e), not L2; codex is walled and owes a re-fire.**

## Q1 — premises
- **(a) TRUE.** Fresh `pty.fork`+`os.execv` per session; the shared inputs are an immutable 16-byte `/tmp/dummy_crimep.bin` and the host clock, and the clock only feeds a within-session delta against a per-session `last_microseconds` (load-sensitive, disclosed, fails red not green). `-V -x` semantics not read from source; non-load-bearing given process isolation.
- **(b) TRUE, now verified to the instruction.** `machine.c:710 run_instr` precedes the tick loop at `:726`, so in the first `step` the s0 `ld` latches `last_microseconds` (adds nothing), then the one tick adds the µs since — 66–286 in every log. The len==8 read takes `odata` *before* the switch's `crime_update_crime_time`, so s1 reads the tick's value; both refusals `goto` past TIME on the fix. M3 exempts the latch-SET refusal → s1 ≈ 2.8e8. Sound.
- **(c) TRUE.** `case CRIME_REV` tests only the pc window — not `writeflag`, not `len` — so `lb/lh/sb/sh` at relative_addr 0 all redirect once the goto is skipped; M5 reds all four `rl … pc`, base reads `0xbfc05184`.
- **(d) TRUE as scoped, and the scope is the trap.** For the 0x0200 cell the three shapes are right (residue-print → D_nodogclear; DOG-as-stop → `rearm/latch surv`, which write 0x0200 then `roundtrip`; re-arm → `rearm once`/`latch x5`). But DOG is not the only tested bit with a "clear so the residue stays quiet" repair — HARD_RESET has the same one, unrowed (Q2).
- **(e) TRUE for the decline-suppression class.** REV/CONTROL/INTSTAT/INTMASK/TIME are the guest-observable arms; DOG is `break;`, `default` is host `debug()` (and rowed anyway by `nodflt`); mirrors 0x80–0x1ff are not redirected in code and fall to `default`; the prelude's `exit(1)` paths are construction invariants, inert at `-M 64`. The gap is on the accepted-CONTROL residue axis, not the label axis.

## Q2 — the floor on the composite
Decline-suppression {observable label × latch SET}: **5/5 carried** (M3 TIME 214, M5 REV 214, M6 INTSTAT 215, M7 INTMASK 215, M8 CONTROL 215; M1 reds all 18 latch-SET cells and, verified, no first-refusal row). Latch-CLEAR TIME carried by M4. Swept and clean.

**The miss — I agree with the dedicated seat.** Delete the HARD_RESET branch's `idata &= ~CRIME_CONTROL_HARD_RESET;`: the `running = 0` loop precedes it, so an accepted `0x800` still halts; `idata` stays `0x800`, the ENDIANESS mask does not touch it, `idata != 0` prints, `fatal()` returns. The only sessions writing an accepted `0x800` are `sw08 halts`, `rst 4w`, `rst 8w` (frozen probe line 1592 is the sole site); they read `v1 == SENT` (still true) and count `-- declined.` (unchanged); the six CONTROL-text rows (lines 648/704/722/940/1332/1464) hold no `0x800`; no control row moves. **All 218 green by derivation.** The probe's HARD_RESET disclosure (line 421, "nothing can follow it … unrowable") is about a *re-arm*, whose observable needs a later access; the residue print is emitted *during* the store and lands in the transcript, so this cell is rowable and simply unrowed.

**Grade: L2, the same as the DOG pair — not disclosed.** HARD_RESET is tested as a case (`if (idata & HARD_RESET)`), so it is in the CONTROL arm's generating set; the clear is that branch's repair; nulling a tested partition's repair is the canonical (d) mutant, and the round already graded the identical shape on DOG "L2, IN as the pair." Grading the twin lower would be the #499 two-of-a-two-by-two. Owed in-round, **test-first**: build D_noresetclear and show 218/218; add `ctlreset sw msg` / `ctlreset sd msg` (accepted `0x800` at +0x08 as the session's last access, count `CRIME_CONTROL: unimplemented` == 0, the halt `v1 == SENT` as the in-session liveness half so a dead channel cannot read 0 for free); show the pair reds the mutant, greens the fix, moves no other leg. Then close the class in the contract: each *tested* CONTROL bit carries a side-effect detector and a residue-print detector (DOG: ctldog + surv; HARD_RESET: rst + ctlreset).

**ENDIANESS — clause (e), not L2.** `idata &= ~CRIME_CONTROL_ENDIANESS;` is unconditional; the arm never branches on the bit, so it is outside the tested generating set {DOG, HARD_RESET} — which is how the probe's contract and my 2026-09-25 re-ruling already grade it. Under the #549 pin (TESTS = masks-or-compares *as a case*), an untested bit crossed with the relational `idata != 0` compare is the two-axis joint a probe discloses; grading it by consequence (the print is real — PROM/NetBSD write ENDIANESS, and the prelude re-forces CONTROL = 0x100) would reopen #548. Two honest riders: the deletion **also escapes 218/218** (the 0x0100 ACCEPTS writes run only inside `rearm`/`latch x5`, which count `-- declined.`), so the disclosure must say *escapes, disclosed* and name the residue-deletion form, which today it does not; and a text count in one of those sessions is a cheap optional strengthening, not owed.

## Q3 — the ctldog pair
**Sound.** Fix: 0x0200 clears DOG → residue 0 → silent; the 0x0201 twin prints once → count 1 (base logs 1/1). D_nodogclear: residue 0x200 prints → count 2 (D logs 2/2, FAIL). So the brief's question — can the row read ONE when 0x0200 *did* print — is answered by the mutant itself: it reads 2. The twin is a genuine in-session liveness half; a bare 0 cannot pass. The member neither the ruling nor the brief named is the HARD_RESET residue pair above.

## Q4 — table 14 vs predictions
**Exact, 18/18.** check14.py compares FAILING sets, tallies, denominator 218 and CONTROL per leg, refuses logs without `CRIMEP_DONE`, and would have flagged a predicted-red 218/218 as ESCAPE. PRETABLE14 (00:33:06) precedes the run (00:33:17) and every log. The 14 new rows red only under their named killers (tl: M1/M3/M4; rl: M1/M5; ctldog: D). No miss to explain. What the table cannot show is a mutant nobody built — which is the whole reason the ask-again found it.

## Where the colleague's draft is wrong or overstated
1. **"MEASURED floor breach" / "airtight" — overstated.** Nobody has built or run D_noresetclear; the dedicated seat's find and the draft's confirmation are both walks. This project's own rule (the #549 M_HUHV case: "it would sweep the table" is a measurement, never an inference) makes it a *derived* escape, measurement owed. I checked the specific way that lesson bit last time — a row already driving the value — and found none, so I expect the build to confirm; "expect" is the word.
2. **Q1(b)'s intra-step order was asserted without source.** It is correct — `run_instr` precedes the tick loop — but it had not been earned.
3. **Roster statement is stale.** The draft cites POSTTABLE ("codex pending to 07:01"); the live panel record says codex **WALLED MID-ANSWER** (830 b, usage limit) and owes one hand re-fire before the round closes; the kimi CLI stalled at 284 b but is COVERED by kimi-k3:cloud. Either way the chain is not closed on roster grounds, and Astra must confirm before any commit.
4. The draft does not answer the ENDIANESS question at all; it is answered above, and the grading line between HARD_RESET (tested → L2) and ENDIANESS (untested → clause e) is the same line the round drew for DOG vs ENDIANESS and the #549 pin drew for TxICR.
5. Minor: "#499 shape *verbatim*" — analogous, not verbatim. The non-blocking note that the latch-CLEAR first-refusal rows at INTSTAT/INTMASK/REV are green on all 18 legs is a true measurement (I ran it) and correctly not a repair-15 breach.

— Fable 5.1, flagship seat; the adjudication that follows this pass should hold the round on items Q2/roster and nothing else.
```

**The Opus measuring seat** (`opus_r15p2_20260926/opus5_r15p2.md`, verbatim):

```
OPUS5_R15P2_ALIVE_0926

`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\CHECKPOINT.md`, first line, verbatim:

> # CHECKPOINT -- 2026-09-26 00:35 (087a90 sections rewritten; the peer's sections below are untouched)

**VERDICT: THE RULED FLOOR IS CLOSED; THE CONTRACT'S CLAIM IS NOT.** All five latch-SET label swaps are killed. But TEN
non-equivalent mutants inside {observable label} x {latch state} score 218/218 on the frozen probe. Each has a
one-session discriminator that shows its guest-visible (or host-text) difference. A census of a full probe run finds 8 of
the 36 observable label x width x direction x latch cells exercised by NO session, all at INTSTAT/INTMASK. Whether those
cells are owed is the adjudicators' call: clause (e) by PRETABLE14's letter, owed by the probe's own contract text.

- **Q1(a)** TRUE for every row. Only three things cross sessions: the 16-byte dummy image (read-only), the host clock and
  host load. Load moves only the magnitude rows. Their measured margins: the largest non-leak s1 is 1914, SMALL/3448,
  and the smallest leak is 1.42e8, 21.6 x SMALL. Measured: 66 sessions, 66 fresh pids, and every session's device TIME
  and latch start at 0.
- **Q1(b)** TRUE, measured from the device side. In all four `tl` sessions: s0 latches `last_microseconds` and adds 0; the
  first-step tick adds 66 x 9-12 us; the +0x07 and +0x38 refusals make NO update; s1 returns exactly the tick's value
  (726/792/726/594, identical to the probe's printed `raw`). **One premise is wrong as stated:** the brief says
  "exactly ONE CRIME tick per session", and every stepped session (56 of 56) has THREE. The other two are
  `cpu_run_deinit`'s "two last ticks" after `quit` (`src/cpus/cpu.c:404-416`). They are harmless here because they come
  after the last print.
- **Q1(c)** TRUE, measured. `M5_revlatch` and `M1_gotolatch` red all four `rl` rows with pc = ra = 0x80004000 (table 14
  logs). The arm's only test is `cpu->pc` (`:344`), so width and direction cannot matter.
- **Q1(d)** FALSE. `D_nodogclear` was not the only DOG-partition mutant the 204 rows missed. `D_doglen8` (DOG cleared
  only at 8 bytes) also escaped them, and the pair kills it at `sw`. Both of those are derived from its measured
  discriminator and replay; it had no probe run. `D_doglatch` and `D_dogbit0` escape even the 218, and that is measured
  (Q2).
  PRETABLE14's own example of "DOG -> stop" (the `:364` test widened to DOG|HARD_RESET) is **EQUIVALENT**: `:362` has
  already cleared DOG before `:364` tests it. Measured: the CPU runs on and the texts match base in all three DOG
  sessions.
- **Q1(e)** The label list is complete. A narrow access at any non-label offset lands in `default:`, and the tail answers
  0 for every narrow read, fall-through or not. But "observable" depends on state:
  * REV only from the PROM window;
  * CONTROL only on writes, and only as host text when HARD_RESET is clear;
  * INTSTAT/INTMASK only when the reassert changes the line. **The probe exercises only the RAISE.** No refused access at
    those labels ever runs with the line already asserted (census), so the LOWER direction is unobserved even for the
    plain M6.
- **Q2** NOT ZERO. Ten measured 218/218 escapes, each with its log in `runs/` and every log ending `CRIMEP_DONE`:
  * `P_ist1r_set`, `P_imk1r_set`: INTSTAT/INTMASK, 1R, latch SET;
  * `C_istW_clr`, `C_ist2_clr`, `C_imkW_clr`, `C_imk2_clr`: INTSTAT/INTMASK, latch CLEAR, direction-only or width-only;
  * `P_ctl2wrc_set`: CONTROL 2W, latch SET, HARD_RESET clear;
  * `P_istprev_set`: INTSTAT, latch SET, line already asserted;
  * `D_doglatch`, `D_dogbit0`: the DOG partition.

  Positive control for the latch-CLEAR shape: `C_ist1r_clr` scored 214/218, red on exactly `istat lb/sb/lh/sh`, as
  pre-registered in `PRED_b3.out`.

  Denominator: 36 observable cells, 28 exercised by a rowed refusal, 8 exercised by none (table in section 4). Plus the
  value, state and DOG shapes listed there. Every candidate I did not build is listed with its reason.
- **Q3** The pair is the right member by the ruling's conditional, and its channel is sound against every single-edit
  DOG mutant I built. It can read ONE with the 0x0200 write printed only if the 0x0201 twin's print is also lost, and
  `p acc ctl msg` sees that loss. **Two members nobody named:**
  * a CONTROL-text COUNT row on the two EXISTING ACCEPTS sessions, which already hold the 0x0200 writes in BOTH latch
    states. It needs no new session and it kills `D_doglatch`, which the pair cannot see. Replay-measured, as
    pre-registered, as `rearm`/`latch x5`: base 4/4, `D_nodogclear` 6/6, `D_doglatch` 6/4, `D_doglen8` 5/5.
  * a value-anchored text: count `unimplemented control 0x0000000000000001` rather than the prefix. It kills
    `D_dogbit0` (measured: that build prints 0x201 where base prints 0x1, at both widths).
- **Q4** No difference. All 18 legs are EXACT, re-derived independently from each raw log's own row lines (`q4_check.py`),
  and all 18 logs end in `CRIMEP_DONE`. No row reds on a leg whose hunk does not reach it.

---

[... sections 1-3 on disk ...]

## 4. Q2 -- THE SWEEP AND ITS DENOMINATOR

**The ruled floor** is {observable label} x {latch SET}, discharged by the label-swap variant. It is **CLOSED**: M6, M7,
M8, M3 and M5 are killed in table 14 (215, 215, 215, 214 and 214 of 218), and my re-derived `P_ist_set`/`P_imk_set` are
byte-identical to M6/M7.

**The contract's own claim is wider.** The probe header, item 3 (`crime_width_probe.table14.py:52`): "every observable
label carries the whole {1,2} x {R,W} refusal floor". Repair 15's block (`:896-898`): "All four narrow ops at each
label ... the four are the width x direction cells a leak keyed on either could use". Crossed with the latch axis the
ruling added, that is the 36-cell table below. **MEASURED** by the census of a full 218/218 run, 66 sessions, the
latch state being the device's own `d->warned` at entry:

    label       1R-CLR   1R-SET   1W-CLR   1W-SET   2R-CLR   2R-SET   2W-CLR       2W-SET          exercised
    REV (win)   S14 S51  S29      S16      S31      S15      S30      S17          S32             8/8
    CONTROL     (reads: arm acts only on writes -- EQUIVALENT)  1W CLR/SET: S12/S12   2W CLR/SET: S11 S13 S44/S13 S20  4/4
    INTSTAT     S19 S46  --       --       S19      --       S19      --           S19             4/8
    INTMASK     S18 S47  --       --       S18      --       S18      --           S18             4/8
    TIME        S21 S49  S25 S40 S50  S22  S26      S23      S27 S40  S24          S28             8/8
    (S45/S50's REV refusals run from CODE, where the arm is inert; S40/S50's TIME refusals have no TIME sample after)

**The 8 empty cells are all at INTSTAT/INTMASK:** 1R with the latch SET, and 1W, 2R and 2W with the latch CLEAR. The
latch-CLEAR half is the sharper finding. There, not even the SINGLE-axis marginals are carried: `C_istW_clr` and
`C_imk2_clr` are one-conjunct narrowings. That is the shape of the F2 pass's `len != 2 || relative_addr != CRIME_INTSTAT`,
which the probe records (item 3) as having forced the 2-byte cells, plus a latch conjunct. In the latch-SET state every
single-axis marginal is carried, and only the (1, R) joint is empty.

**How to grade it** (a reading; the adjudicators rule):

* **By the ruling's letter it is clause (e).** Width and direction are not partitioned at the decline (`len` is only
  "not 8, not 4" there, and `writeflag` is not tested), so any width- or direction-keyed exemption is a joint.
  PRETABLE14's SIBLING PARITY check saw half of this, the latch-SET 1R pair, and disposed it exactly so
  (`PRETABLE14.out:117-124`). The same reasoning covers the six latch-CLEAR cells, but **nobody named them**.
* **By the probe's own text they are owed, or the text is a wrong record.** Item 3 (`:52`) and the repair-15 comment
  (`:896-898`) claim the {1,2}x{R,W} floor at every observable label. The only place that says it is latch-agnostic is PRETABLE14.out, and **the contract
  block in the probe (section 5 of the brief) discloses neither half**. As shipped, a reader of the contract believes
  INTSTAT/INTMASK carry all four cells in the sense TIME/REV now do. The project's own precedent (the F2 2-byte cells)
  rowed a label x width narrowing rather than disclosing it.
* **If owed, the cheapest closure is 6 new sessions.** One per latch-CLEAR cell at INTSTAT/INTMASK, since a session has
  only one first refusal. The two latch-SET 1R cells ride in two of them, after that first refusal. Each session carries
  the `pre`/`ctl` controls the istat/imask sessions use, and costs about 8-10 s. **If clause (e),** the probe's contract
  block must name the 8 cells and cite these runs.

**The other shapes measured** are all clause (e) by my reading, and are listed so a disclosure can name them:

* `P_ctl2wrc_set`: 2W x HARD_RESET-clear at CONTROL, latch SET. The only effect is host text, and every latch-SET 2W
  write in the probe carries 0x0800.
* `P_istprev_set`: INTSTAT, latch SET, falling through only while the line is already asserted. It scores 218/218
  because no refused access at 0x10/0x18 ever runs with `prev_asserted = 1`. It is a callee-state joint, which the Q3
  bound excludes, but its effect is guest-visible (IP2 dropped).
* `D_doglatch` scores 218/218. It is the "latch x DOG joint" the contract already discloses. Its only effect, the 0x0200
  text with the latch SET, sits in S36, where no row counts CONTROL text.
* `D_dogbit0` scores 218/218. It is a DOG x bit-0 idata joint: the count is unchanged and only the residue VALUE moves.

**Considered, NOT built, with the reason:**

1. **The latch-CLEAR plain label swap** at each label is killed by derivation: every observable label has a rowed
   latch-CLEAR refusal (table above), and `C_ist1r_clr` is the measured positive control for the shape.
2. **Width-only or direction-only narrowings of the latch-SET swap** are killed by derivation: every single-axis value is
   carried by a rowed latch-SET refusal at all five labels (table).
3. **CONTROL read-side exemptions** are EQUIVALENT (`:356`). CONTROL 2R-CLEAR is the one unexercised CONTROL cell, and it
   is one of these.
4. **REV exemptions outside the window** are EQUIVALENT (`:344`).
5. **DOG** is EQUIVALENT (`break;`). **`default`** is host text only. A latch-SET default exemption keyed on address bits
   7-8 clear would escape `mid nodflt`, whose latch-SET refusals all set those bits. It is clause (e) by the contract's
   own DOG/default disclosure.
6. **HARDINT-keyed label swaps** at INTSTAT/INTMASK/TIME/REV score 218/218 by construction: the only refusals with
   HARDINT != 0 are S20's three, all at CONTROL (`census_facts.out`). This is the same class as `P_istprev_set`.
7. **pc-keyed swaps at the non-REV labels** score 218/218 by construction: every refusal at TIME/INTSTAT/INTMASK/CONTROL
   runs from CODE. Those arms never read the pc, so it is not an axis under the DEPENDS-ON bound.
8. **Configuration-keyed swaps** (`use_fb`, RAM size) are dead code on `-M 64` non-graphics ip32. They are unrowable on
   one machine, which is the contract's existing class.
9. **TIME exemptions keyed on TIME or last_us values** leave nothing to row. The arm's own partitions are
   `last_us == 0`, never true at a latch-SET refusal (the first-step tick sets it in 56 of 56 sessions), and
   `delta < 0`, which is the host clock.
10. **`D_doglen8` and `D_dogstopwiden`** are built and discriminator-measured but NOT run through the probe. The first is
    predicted killed (`ctldog sw msg` only); the second is equivalent.
11. **The composite `D_nodogclear` + a latch on the CONTROL text** is two edits, outside the licensed multi-part shapes.
    Its latch half alone is killed by `p acc ctl msg` (4 -> 1).

## 5. Q3

The ruling's conditional ("if a body-tested-partition mutant escapes -> L2, IN as the pair") is met exactly. Table 14
reds only the pair under `D_nodogclear`, and sessions are independent, so it was 204/204 on the old rows. The pair is
the right member **of the two the ruling offered**, and its channel is sound. The measured DOG builds that print for
0x0200 read 2, never 1. A ONE with 0x0200 printed needs the 0x0201 twin's print lost as well, and that is a second
defect `p acc ctl msg` already counts. A dead channel reads 0 and a torn transcript reads `unclean`; both are red.

**Two members neither the ruling nor the brief named:**

* **Count rows on the existing ACCEPTS sessions.** S36 (`rearm`) holds all ten accepted CONTROL writes with the latch
  SET, 0x0200 at both widths included, and S50 (`latch x5`) holds them with the latch CLEAR (`accepts_ctl_writes.out`).
  Adding a CONTROL-text count to those two sessions changes no command list, needs no new session, and pins entries
  13/17 in BOTH latch states. The pair covers only latch CLEAR. Replay-measured with the probe's own command lists
  (`replay/`, all clean, one `-- declined.` each), as `rearm`/`latch x5`:

      base 4/4    D_nodogclear 6/6    D_doglatch 6/4    D_doglen8 5/5

  All four are exactly as pre-registered. **Cost:** the want is an aggregate over ten writes, and every future ACCEPTS
  edit moves it.
* **A value-anchored text** in the pair itself: `unimplemented control 0x0000000000000001` rather than the prefix. It
  kills `D_dogbit0` (measured: 0x201 printed where base prints 0x1, at both widths and in both latch states) at zero
  session cost. That is clause (f) applied to text: the count is a relative observable and the value is an anchored one.

[... sections 6-9 on disk: opus_r15p2_20260926/opus5_r15p2.md ...]
```

## 6. QUESTIONS (verdict line first; then one line per item; then reasons)

**Q1.** Adjudicate F1..Fn and D1..Dn: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with the reason.
**Q2. WHICH OF MY DISPOSITIONS IS WRONG?**  I accepted or rejected every finding in section 2 and ruled every disagreement in
section 3 -- that is a suspicious number of rulings by one party, and agreement is not evidence.  Name the one you would
overturn first.
**Q3. WHAT DID ALL OF US MISS?**  You now have every seat's findings and the new tables.
**Q4. REPAIR 16 (E7, E8, E10):** do the four new rows' channels vary under exactly their named mutants?  Is the class
closure in the contract text true as written -- each TESTED bit of the CONTROL arm carrying a side-effect detector AND a
residue-print detector?
**Q5. THE RULE QUESTIONS (D2, D3, D4):** floor or clause (e)?  The measured deltas are in E10.

If, while verifying a claim, you found something ELSE -- say so.
